#!/usr/bin/env python3
"""Supplement: drop packets on r1-r2 while keeping interface carrier up."""
import json
import time
import measure_ospf as m

def main():
    assert m.all_full(), 'Run after the triangle has fully reconverged'
    baseline = m.signature(m.snapshot())
    pid = m.command(['docker', 'inspect', '--format', '{{.State.Pid}}',
                     m.CONTAINERS['r1']]).strip()
    base = ['nsenter', '-t', pid, '-n', 'iptables', '-w']
    rules = [['INPUT', '-i', 'eth1', '-m', 'comment', '--comment', 'week06-silent-failure', '-j', 'DROP'],
             ['OUTPUT', '-o', 'eth1', '-m', 'comment', '--comment', 'week06-silent-failure', '-j', 'DROP']]
    applied = []
    m.capture('route-silent-before.txt')
    start = time.monotonic()
    result = {}
    try:
        for rule in rules:
            m.command(base + ['-I'] + rule)
            applied.append(rule)
        desired_r1 = m.entry(20, m.via('r3', 'eth1', 'eth0'))
        desired_r2 = m.entry(20, m.via('r3', 'eth0', 'eth1'))
        raw, previous, elapsed = m.wait_for(
            lambda raw: m.normalize(raw['r1']).get(m.C) == desired_r1 and
                        m.normalize(raw['r2']).get(m.A) == desired_r2,
            start=start)
        result.update(event='silent_packet_loss', last_nonmatching_poll_s=previous,
                      first_matching_poll_s=elapsed, routes=raw)
        m.capture('route-silent-after.txt')
        result['interface_during_failure'] = json.loads(
            m.execute('r1', ['ip', '-j', 'link', 'show', 'eth1']))
        print(f'Silent failure: alternate paths observed by {elapsed:.3f} s', flush=True)
    finally:
        for rule in reversed(applied):
            m.command(base + ['-D'] + rule)
    restore_start = time.monotonic()
    _, previous, elapsed = m.wait_for(lambda raw: m.signature(raw) == baseline, start=restore_start)
    result['restore_first_matching_poll_s'] = elapsed
    m.OUT.joinpath('silent-failure.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    with m.OUT.joinpath('reconverge.txt').open('a', encoding='utf-8') as f:
        f.write('\nSupplement: silent packet loss simulated by INPUT/OUTPUT DROP rules on r1 eth1 only.\n')
        f.write('Interface remains UP; no host-network firewall rules are modified. Both rules removed afterward.\n')
        f.write(f'Alternate routes on r1 and r2 first observed at {result["first_matching_poll_s"]:.6f} s; '
                f'previous nonmatching poll ended at {result["last_nonmatching_poll_s"]:.6f} s.\n')
        f.write(f'After rules were removed, baseline routes returned by {elapsed:.6f} s.\n')
    print('Supplement complete; rules removed and baseline routes restored.', flush=True)

if __name__ == '__main__':
    main()
