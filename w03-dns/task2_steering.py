#!/usr/bin/env python3
"""DNS measurements on labelled networks; no dig installation required.

Collect once on each real network, using distinct --network labels.
--report produces a draft until out/classification.json has been reviewed.
Classification format: {site: {"cdn": true/false/null,
 "third_party": true/false/null, "reason": "evidence and source"}}.
"""
import argparse
import concurrent.futures
import datetime
import json
from pathlib import Path
import re
import uuid

import dns.exception
import dns.rdatatype
import dns.resolver

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
SITES = [
    'www.microsoft.com', 'www.netflix.com', 'www.adobe.com', 'www.cnn.com',
    'www.apple.com', 'www.korea.ac.kr', 'www.stanford.edu', 'www.bbc.co.uk',
    'www.spotify.com', 'www.github.com', 'www.wikipedia.org', 'www.nytimes.com',
]
RESOLVERS = {'system': None, 'google': '8.8.8.8', 'quad9': '9.9.9.9'}


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def measure(site, resolver_label):
    row = {'site': site, 'resolver': resolver_label, 'started_at': utcnow(),
           'chain': [site], 'hops': [], 'addresses': [], 'queries': [],
           'status': 'error'}
    try:
        server = RESOLVERS[resolver_label]
        resolver = dns.resolver.Resolver(configure=server is None)
        if server:
            resolver.nameservers = [server]
        resolver.timeout = 2
        resolver.lifetime = 5
        resolver.cache = None
        row['configured_nameservers'] = [str(x) for x in resolver.nameservers]

        def ask(name, typ):
            query = {'name': name, 'type': typ, 'time': utcnow()}
            row['queries'].append(query)
            try:
                answer = resolver.resolve(name, typ, search=False,
                                          raise_on_no_answer=False)
                query['response'] = answer.response.to_text()
                query['server'] = str(answer.nameserver)
                return answer
            except dns.exception.DNSException as exc:
                query['error'] = str(exc)
                raise

        current = site
        seen = set()
        for _ in range(20):
            if current in seen:
                raise RuntimeError('CNAME loop detected')
            seen.add(current)
            answer = ask(current, 'CNAME')
            if answer.rrset is None:
                break
            target = answer.rrset[0].target.to_text().rstrip('.').lower()
            row['hops'].append({'from': current, 'to': target,
                                'ttl': answer.rrset.ttl})
            row['chain'].append(target)
            current = target
        else:
            raise RuntimeError('CNAME hop limit reached')

        # Ask for the original name too: preserve the actual A answer and any
        # changed alias chain, since DNS answers can rotate between requests.
        answer = ask(site, 'A')
        if answer.rrset is None:
            raise RuntimeError('No IPv4 A answer')
        row['addresses'] = sorted({r.address for r in answer.rrset})
        row['address_canonical_name'] = answer.canonical_name.to_text().rstrip('.').lower()
        row['a_answer_aliases'] = [
            {'from': rr.name.to_text().rstrip('.'),
             'to': rr[0].target.to_text().rstrip('.'), 'ttl': rr.ttl}
            for rr in answer.response.answer if rr.rdtype == dns.rdatatype.CNAME
        ]
        row['chain_changed_between_queries'] = row['address_canonical_name'] != current
        row['final_name'] = current
        row['status'] = 'ok'
    except (dns.exception.DNSException, OSError, RuntimeError, ValueError) as exc:
        row['error'] = type(exc).__name__ + ': ' + str(exc)
    row['finished_at'] = utcnow()
    return row


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)


def collect(network):
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    run_id = stamp + '-' + uuid.uuid4().hex[:8]
    run = {'id': run_id, 'network': network, 'started_at': utcnow(), 'measurements': []}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        jobs = [pool.submit(measure, s, r) for s in SITES for r in RESOLVERS]
        for i, future in enumerate(concurrent.futures.as_completed(jobs), 1):
            row = future.result()
            run['measurements'].append(row)
            print(f"[{i:02}/36] {row['resolver']:6} {row['site']:22} "
                  f"{', '.join(row['addresses']) if row['status'] == 'ok' else row['error']}",
                  flush=True)
    run['finished_at'] = utcnow()
    run['measurements'].sort(key=lambda r: (r['site'], r['resolver']))
    slug = re.sub(r'[^a-zA-Z0-9_-]', '_', network)[:50] or 'network'
    run_path = OUT / 'networks' / f'{slug}-{run_id}.json'
    write_json(run_path, run)

    # Rebuild the combined file from all preserved runs, including failures.
    combined = {site: {'measurements': []} for site in SITES}
    for path in sorted((OUT / 'networks').glob('*.json')):
        prior = json.loads(path.read_text(encoding='utf-8-sig'))
        for row in prior['measurements']:
            combined[row['site']]['measurements'].append(
                dict(row, network=prior['network'], run_id=prior['id']))
    write_json(OUT / 'chains.json', combined)
    successes = sum(r['status'] == 'ok' for r in run['measurements'])
    print(f'\nSaved {run_path}\nUpdated {OUT / "chains.json"}')
    print(f'{successes}/36 successful. Failures are recorded, never counted as different IPs.')


def last_two(name):
    return '.'.join(name.rstrip('.').lower().split('.')[-2:])


def report():
    data = json.loads((OUT / 'chains.json').read_text(encoding='utf-8-sig'))
    review_path = OUT / 'classification.json'
    review = json.loads(review_path.read_text(encoding='utf-8-sig')) if review_path.exists() else {}
    lines = ['# DNS steering report', '',
             'Rule under test: label a site third-party when the final CNAME name and '
             'the original site have different last-two-label suffixes. This is a '
             'heuristic, not a reliable ownership or CDN test.', '',
             'Suffixes below are NOT verified DNS zone boundaries or public-suffix-aware domains.', '',
             '| Site | Network / run | Resolver | Chain length | Final name / suffix | '
             'Third-party (reviewed) | Rule verdict | A addresses |',
             '|---|---|---|---:|---|---|---|---|']
    differing, comparable = 0, 0
    errors, mismatch = [], []
    labels = set()
    for site, item in data.items():
        checked = review.get(site, {})
        third = checked.get('third_party')
        truth = 'unknown' if third is None else ('yes' if third else 'no')
        # Use the latest attempted run on each network, including failed rows.
        latest_runs = {}
        for row in item['measurements']:
            label = row['network']
            labels.add(label)
            latest_runs[label] = max(latest_runs.get(label, ''), row['run_id'])
        successful = []
        for row in item['measurements']:
            if row['run_id'] != latest_runs[row['network']]:
                continue
            if row['status'] != 'ok':
                errors.append(f"- {site} / {row['network']} / {row['resolver']}: {row.get('error')}")
                continue
            successful.append(row)
            final = row['final_name']
            verdict = last_two(final) != last_two(site)
            if third is not None and verdict != third:
                mismatch.append(f"- {site}: rule says {verdict}, reviewed third-party={third}. "
                                + checked.get('reason', 'Evidence still needed.'))
            lines.append(f"| {site} | {row['network']} / {row['run_id']} | {row['resolver']} | "
                         f"{len(row['hops'])} | {final} / {last_two(final)} | {truth} | "
                         f"{'yes' if verdict else 'no'} | {', '.join(row['addresses'])} |")
        if checked.get('cdn') is True:
            # Comparisons are between different resolvers within one run, or
            # the same resolver on different networks. Do not compare retries.
            pairs = [(a, b) for i, a in enumerate(successful) for b in successful[i+1:]
                     if (a['run_id'] == b['run_id'] and a['resolver'] != b['resolver'])
                     or (a['network'] != b['network'] and a['resolver'] == b['resolver'])]
            if pairs:
                comparable += 1
                differing += any(set(a['addresses']) != set(b['addresses']) for a, b in pairs)
    lines += ['', '## Networks and steering', '', 'Networks: ' + ', '.join(sorted(labels)), '',
              'Only latest runs per network are compared. Failed queries are excluded.', '']
    if comparable:
        lines.append(f'{differing} of {comparable} reviewed CDN-hosted sites returned different '
                     'IPv4 address sets across resolvers or networks.')
    else:
        lines.append('PENDING: classify CDN-hosted sites with evidence before calculating X of N.')
    lines += ['', 'Different addresses demonstrate answer variation, not necessarily nearby replicas. '
              'Time variation, load balancing and anycast also limit the conclusion.', '',
              '## Classification review and counterexample', '']
    lines += sorted(set(mismatch)) or ['PENDING: identify and explain an actual rule misclassification.']
    for site in SITES:
        lines.append(f"- {site}: {review.get(site, {}).get('reason', 'PENDING ownership/CDN review')}")
    notes_path = OUT / 'measurement_notes.md'
    if notes_path.exists():
        lines += ['', notes_path.read_text(encoding='utf-8-sig'), '']
    capture_path = OUT / 'capture_notes.md'
    lines += ['', '## Capture evidence', '',
              capture_path.read_text(encoding='utf-8-sig') if capture_path.exists() else
              'PENDING: add query/response transaction IDs, delegation and answer packet numbers, '
              'and the largest DNS message size from the submitted capture.', '',
              '## Query failures', '']
    lines += errors or ['None in the selected runs.']
    (OUT / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Saved out/report.md.' + (' PENDING sections still need completion.'
          if any('PENDING' in line for line in lines) else ' Review the conclusions before submission.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--collect', action='store_true')
    action.add_argument('--report', action='store_true')
    parser.add_argument('--network', help='Actual network label, e.g. ethernet or phone-hotspot')
    args = parser.parse_args()
    if args.collect and not args.network:
        parser.error('--collect requires --network so each measurement keeps its network label')
    OUT.mkdir(exist_ok=True)
    if args.collect:
        collect(args.network)
    else:
        report()
