# Week 06 observations

## Task 1
I retain the first discovered equal-cost route, with sorted neighbours and a (distance, node-name) heap giving deterministic ties; a real router may instead install ECMP next hops.
At u, traffic for w goes through x: u-x-y-w costs 3, compared with 5 on the direct u-w link.
After cutting u-x, w changes from x to w, and x/y/z change from x to v; v keeps next hop v (the equal-cost route to w via v loses to the direct route discovered first).

## Task 2 — partially measured; OSPF experiment pending
The domestic trace first reaches a public address at hop 2 (112.145.216.178), but this alone does not identify a campus boundary; Stanford resolves to a CDN and shows no sustained ocean-crossing jump, so neither an ocean hop nor a cable can be identified from this capture.
1.1.1.1 is reached at hop 12 in 11–12 ms, consistent with a nearby network replica but not proof of its city; missing replies can reflect ICMP filtering/rate limiting or actual loss/unreachability, and hop 10's silence followed by successful hops 11–12 demonstrates that silence need not mean forwarding failure.
Docker is unavailable and WSL reports ERROR_SERVICE_DISABLED: B2/B4/B5/C3 have not been measured, and no classmate data were supplied; detection, adjacency formation and LSA/SPF delays must be compared using real timings before claiming completion (see task2-notes.md).

## Task 3
I keep distances, selected parents and tree edges (O(V) extra storage beyond the O(V+E) graph/table); unchanged events and worsening non-tree edges skip SPF, while improvements or earlier equal-cost parents and damaged tree edges trigger the provided counted SPF.
Across 1,000 events, all tables match the reference: 346 SPF runs versus 1,001, avoiding 65.43%; 9,000 additional events across 30 small graphs also match, including ties and disconnected components.
The supplied harness reports 1.75 s versus 1.24 s, but only the optimized run includes 1,000 validation SPFs; without validation both runs measured 0.45 s versus 1.20 s. Reduced SPF can lower router CPU load, but memory, bookkeeping and worst-case event workload still matter; these Python times alone do not establish production router performance.
