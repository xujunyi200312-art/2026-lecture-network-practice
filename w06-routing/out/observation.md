# Week 06 observations

## Task 1
I retain the first discovered equal-cost route, with sorted neighbours and a (distance, node-name) heap giving deterministic ties; a real router may instead install ECMP next hops.
At u, traffic for w goes through x: u-x-y-w costs 3, compared with 5 on the direct u-w link.
After cutting u-x, w changes from x to w, and x/y/z change from x to v; v keeps next hop v (the equal-cost route to w via v loses to the direct route discovered first).

## Task 2
The domestic trace first shows a public address at hop 2 (112.145.216.178), but cannot establish a campus boundary; Stanford resolves to a CDN with no visible sustained ocean-crossing latency jump, so a cable cannot be identified. Anycast 1.1.1.1 responds at hop 12 in 11–12 ms, consistent with a nearby replica; stars can mean ICMP filtering/rate limiting or actual loss/unreachability, not necessarily broken forwarding.
All three FRR routers learn their non-direct subnet at cost 20. Administrative r1-r2 interface-down reroutes all three tables by 0.165 s, while the peer neighbour expires by 33.551 s; a separate silent packet-loss experiment reroutes by 33.645 s, consistent with the remaining portion of the measured Hello 10 s / Dead 40 s timer.
Restoring the interface restores the original tables by 15.012 s (neighbour discovery, adjacency exchange and SPF); changing r1-net_a cost 10→100 moves net_c traffic from ECMP to r2 alone by 0.182 s. Cost updates avoid failure-detection delay and beat silent failure here, but do not measurably beat locally signalled interface-down; measurements include polling/command overhead (details in task2-notes.md).

## Task 3
I keep distances, selected parents and tree edges (O(V) extra storage beyond the O(V+E) graph/table); unchanged events and worsening non-tree edges skip SPF, while improvements or earlier equal-cost parents and damaged tree edges trigger the provided counted SPF.
Across 1,000 events, all tables match the reference: 346 SPF runs versus 1,001, avoiding 65.43%; 9,000 additional events across 30 small graphs also match, including ties and disconnected components.
The supplied harness reports 1.75 s versus 1.24 s, but only the optimized run includes 1,000 validation SPFs; without validation both runs measured 0.45 s versus 1.20 s. Reduced SPF can lower router CPU load, but memory, bookkeeping and worst-case event workload still matter; these Python times alone do not establish production router performance.
