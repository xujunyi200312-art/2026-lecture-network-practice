#!/usr/bin/env python3
"""Collect real FRR tables and monotonic convergence times (run on Docker host)."""
import concurrent.futures
import datetime
import ipaddress
import json
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
ROUTERS = ('r1', 'r2', 'r3')
DC = ['docker', 'compose', '--profile', 'routing']

def command(args):
    return subprocess.check_output(args, cwd=HERE.parent, text=True, stderr=subprocess.STDOUT)

CONTAINERS = {r: command(DC + ['ps', '-q', r]).strip() for r in ROUTERS}

def execute(r, args):
    return command(['docker', 'exec', CONTAINERS[r]] + args)

def vty(r, text):
    return execute(r, ['vtysh', '-c', text])

def addresses(r):
    return {row['ifname']: a['local']
            for row in json.loads(execute(r, ['ip', '-j', '-4', 'addr']))
            for a in row['addr_info'] if row['ifname'] != 'lo'}

IPS = {r: addresses(r) for r in ROUTERS}
NETWORKS = {}
for r in ROUTERS:
    for row in json.loads(execute(r, ['ip', '-j', '-4', 'addr'])):
        for a in row['addr_info']:
            if row['ifname'] != 'lo':
                NETWORKS[r, row['ifname']] = str(ipaddress.ip_network(
                    f"{a['local']}/{a['prefixlen']}", strict=False))
A, B, C = NETWORKS['r1', 'eth0'], NETWORKS['r1', 'eth1'], NETWORKS['r2', 'eth1']
assert NETWORKS['r3', 'eth1'] == A
assert NETWORKS['r2', 'eth0'] == B
assert NETWORKS['r3', 'eth0'] == C

def normalize(raw):
    return {prefix: sorted((route['metric'], tuple(sorted(
                (hop.get('ip', ''), hop.get('interfaceName', ''),
                 bool(hop.get('directlyConnected', False)))
                for hop in route['nexthops'] if hop.get('active'))))
            for route in routes) for prefix, routes in raw.items()}

def snapshot():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        return dict(zip(ROUTERS, pool.map(
            lambda r: json.loads(vty(r, 'show ip route ospf json')), ROUTERS)))

def signature(raw):
    return {r: normalize(raw[r]) for r in ROUTERS}

def wait_for(predicate, timeout=100, start=None):
    start = time.monotonic() if start is None else start
    previous = 0.0
    while time.monotonic() - start < timeout:
        raw = snapshot()
        elapsed = time.monotonic() - start
        if predicate(raw):
            return raw, previous, elapsed
        previous = elapsed
        time.sleep(.2)
    raise RuntimeError('Convergence condition not reached before timeout')

def all_full():
    for r in ROUTERS:
        nbrs = json.loads(vty(r, 'show ip ospf neighbor json'))['neighbors']
        if len(nbrs) != 2 or any(not n['nbrState'].startswith('Full')
                                 for values in nbrs.values() for n in values):
            return False
    return True

def capture(name):
    text = [f'Captured locally: {datetime.datetime.now().astimezone().isoformat()}']
    for r in ROUTERS:
        text += [f'\n===== {r} =====', vty(r, 'show ip route ospf'),
                 vty(r, 'show ip ospf neighbor')]
    (OUT / name).write_text('\n'.join(text), encoding='utf-8')

def entry(metric, *hops):
    return [(metric, tuple(sorted(hops)))]

def direct(iface):
    return ('', iface, True)

def via(r, iface, outgoing):
    return (IPS[r][iface], outgoing, False)

def config_cost(cost):
    return execute('r1', ['vtysh', '-c', 'configure terminal', '-c',
                          'interface eth0', '-c', f'ip ospf cost {cost}'])

def main():
    OUT.mkdir(exist_ok=True)
    print('Waiting for all six FULL neighbour relations...', flush=True)
    deadline = time.monotonic() + 100
    while not all_full():
        if time.monotonic() > deadline:
            raise RuntimeError('Neighbours did not become FULL')
        time.sleep(1)
    baseline, _, _ = wait_for(lambda raw: all(len(raw[r]) == 3 for r in ROUTERS))
    base_sig = signature(baseline)
    capture('route-before.txt')
    (OUT / 'ospf-environment.txt').write_text(
        command(['docker', 'version']) + command(['docker', 'compose', 'version']) +
        command(['uname', '-a']) + '\nInterface addresses: ' + json.dumps(IPS, indent=2) +
        ''.join(f'\n===== {r} =====\n' + vty(r, 'show version') +
                vty(r, 'show ip ospf interface') + vty(r, 'show running-config')
                for r in ROUTERS), encoding='utf-8')
    expected_cut = {
        'r1': {A: entry(10, direct('eth0')),
               B: entry(30, via('r3', 'eth1', 'eth0')),
               C: entry(20, via('r3', 'eth1', 'eth0'))},
        'r2': {A: entry(20, via('r3', 'eth0', 'eth1')),
               B: entry(10, direct('eth0')), C: entry(10, direct('eth1'))},
        'r3': {A: entry(10, direct('eth1')),
               B: entry(20, via('r2', 'eth1', 'eth0')),
               C: entry(10, direct('eth0'))}}
    measurements = []
    raw_records = {'before': baseline}
    try:
        start = time.monotonic()
        execute('r1', ['ip', 'link', 'set', 'eth1', 'down'])
        raw, lower, upper = wait_for(lambda raw: signature(raw) == expected_cut, start=start)
        measurements.append(dict(event='interface_down', lower_s=lower, upper_s=upper))
        raw_records['after_cut'] = raw
        capture('route-after.txt')
        print(f'Interface down: routes correct within {upper:.3f} s', flush=True)

        # Let the peer's 40-second dead interval expire before restoring.
        # This wait is outside the measured route-convergence time.
        deadline = time.monotonic() + 50
        while '1.1.1.1' in json.loads(vty('r2', 'show ip ospf neighbor json'))['neighbors']:
            if time.monotonic() > deadline:
                raise RuntimeError('Peer neighbour did not expire')
            time.sleep(.5)
        peer_dead = time.monotonic() - start
        measurements.append(dict(event='peer_neighbour_expiry', upper_s=peer_dead))

        start = time.monotonic()
        execute('r1', ['ip', 'link', 'set', 'eth1', 'up'])
        raw, lower, upper = wait_for(lambda raw: signature(raw) == base_sig, start=start)
        measurements.append(dict(event='interface_restore', lower_s=lower, upper_s=upper))
        raw_records['restored'] = raw
        capture('route-restored.txt')
        print(f'Restore: routes correct within {upper:.3f} s', flush=True)

        capture('route-cost-before.txt')
        start = time.monotonic()
        config_cost(100)
        desired_c = entry(20, via('r2', 'eth0', 'eth1'))
        raw, lower, upper = wait_for(
            lambda raw: normalize(raw['r1']).get(C) == desired_c, start=start)
        measurements.append(dict(event='cost_10_to_100', lower_s=lower, upper_s=upper))
        raw_records['cost_changed'] = raw
        capture('route-cost-after.txt')
        print(f'Cost change: r1 next hop correct within {upper:.3f} s', flush=True)
    finally:
        execute('r1', ['ip', 'link', 'set', 'eth1', 'up'])
        config_cost(10)
        (OUT / 'measurement-raw.json').write_text(json.dumps({
            'addresses': IPS, 'subnets': {'A': A, 'B': B, 'C': C},
            'measurements': measurements, 'snapshots': raw_records}, indent=2), encoding='utf-8')
    wait_for(lambda raw: signature(raw) == base_sig)
    lines = ['Real local Docker/FRR experiment; monotonic clock.',
             'Time origin: immediately before issuing the change command.',
             'Poll sleep: 0.2 s, plus Docker/vtysh overhead. Each sample queries three routers concurrently.',
             'Bounds: last nonmatching poll completion < convergence observation <= first matching poll completion.',
             'These are observation bounds, not exact packet-level timestamps.',
             'Down/restore: all three complete OSPF route metrics and active next hops match the expected state.',
             'Cost change: r1 route to net_c changes from ECMP to r2 only; all three tables captured.',
             'After down measurement, wait for r2 to expire r1 before restoration; this is not included in down time.',
             'Hello/dead intervals: see ospf-environment.txt (10 s / 40 s).', '']
    for row in measurements:
        lines.append(json.dumps(row))
    (OUT / 'reconverge.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Measurements saved; link and cost restored.', flush=True)

if __name__ == '__main__':
    main()
