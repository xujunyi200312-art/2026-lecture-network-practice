# Task 2: measurement status and interpretation

## Measurements actually performed

`traceroute.txt` contains three local Windows traces captured on 2026-10-28.
They use the assignment's targets, a 30-hop limit, and a 500 ms per-probe timeout.
The Korea University and anycast traces use IPv4; the Stanford trace uses IPv6.
The timeout and address-family difference limit direct latency comparisons.

- **A2:** Hop 1 is 192.168.219.1 and hop 2 is 112.145.216.178 on the domestic trace. Hop 2 is the first visible public address, not established evidence of the exact campus exit. Campus membership and the location of this access network were not independently verified.
- **A3:** Stanford resolves to stanford.netlifyglobalcdn.com. Its responding hops mostly remain below 10 ms; the transient 35–41 ms response at hop 8 is followed by lower RTTs. There is no sustained approximately 100 ms step from which to infer an ocean crossing. No submarine cable identification is justified. Neither this trace nor the Korea trace reaches its destination within 30 hops.
- **A4:** 1.1.1.1 responds at hop 12 with 12/11/11 ms. This supports a low-latency path to the selected anycast replica, not an exact geographic location; hop count is not physical distance.
- **A5:** ICMP Time Exceeded or Echo Reply may be filtered or rate limited even while data forwarding works. Alternatively, probes or replies may be lost due to congestion, routing failure or unreachable destinations; replies may also arrive after this short timeout. Hop 10 on the anycast path is silent but hops 11 and 12 respond, so that hop's silence is not evidence that the end-to-end path failed.

## Parts B and C: missing observations

No Docker executable or standard Docker installation was found; WSL cannot start because its service is disabled (ERROR_SERVICE_DISABLED).
No FRR containers were launched. No router tables, cut/restore timings or cost-change timing were captured. The three required files `route-before.txt`, `route-after.txt`, and `reconverge.txt` are intentionally absent rather than populated with invented data.
The assignment's fallback requires attributed classmate captures and their real timings; none have been provided. Parts B and C therefore remain incomplete.

The configuration does not explicitly set hello/dead intervals. Obtain their actual values with `show ip ospf interface` in the running routers instead of treating assumed defaults as measurements.
The supplied script lowers r1's interface administratively, so r1 can detect that local failure immediately; a remote silent-neighbour failure may instead wait for the dead timer. Restore timing involves neighbour discovery, adjacency/database synchronisation and SPF. A cost change needs LSA propagation and SPF without waiting for a failed-neighbour timer; which operation is faster must still be measured.

## Completing the remaining measurements on Docker/Linux

1. Start the supplied routing topology and wait for FULL neighbours. Save `show ip ospf neighbor` and `show ip ospf interface` for all three routers.
2. Save all three routers' OSPF tables to `out/route-before.txt`. Identify a learned route to a subnet not directly connected to that router (B2).
3. Record a monotonic start time, lower the intended r1-r2 interface, and poll until every router has the expected alternate routes. Save all three tables to `out/route-after.txt` and record elapsed time and poll resolution in `out/reconverge.txt`.
4. Restore the interface and measure until the expected original routes and adjacencies return. Append the restoration time.
5. Save tables before changing r1's net_a cost from 10 to 100; apply the change and time until the expected next hop/cost is installed. Save the final tables and append the measured time. Restore the cost afterward.
6. Update observation.md with the actual B2/B4/B5/C3 findings, then rerun both required checks.

Do not treat the supplied script's first text difference as proof of convergence: its `cut` command captures only r1 and compares raw output, which can change because a route age changed. Its restore/cost commands use fixed sleeps, not actual convergence measurements. Validate next hops, costs and all routers explicitly.
