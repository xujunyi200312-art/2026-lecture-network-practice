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

## Parts B and C: real local FRR measurements

Performed on this computer in Ubuntu 24.04 under WSL 2, Docker Engine 29.9.2 / Compose 5.6.1, official quay.io/frrouting/frr:9.1.0 image (runtime banner 9.1_git).
All measurements are from the local running routers; no classmate data or simulated routing-table outputs were used.

| Network | Subnet | Attached routers |
|---|---|---|
| net_a | 172.19.0.0/16 | r1 eth0, r3 eth1 |
| net_b | 172.20.0.0/16 | r1 eth1, r2 eth0 |
| net_c | 172.21.0.0/16 | r2 eth1, r3 eth0 |

**B2:** Initially r1 learns net_c, r2 learns net_a, and r3 learns net_b via OSPF, each at cost 20 with two equal-cost next hops. None has a direct interface in its respective remote subnet. This demonstrates actual route learning, rather than merely listing connected interfaces.

| Event | First matching observation after command start |
|---|---:|
| Administrative interface down | 0.165082 s |
| Remote neighbour disappears after the cut | 33.551300 s |
| Interface restored, original routes restored | 15.011630 s |
| r1 eth0 cost 10→100, net_c uses r2 only | 0.181552 s |
| Supplement: silent packet loss, interface remains UP | 33.645213 s |
| Supplement: remove packet-loss rules, restore original routes | 19.361510 s |

**B3/B4:** The experiment lowers r1 eth1, its verified interface to r2. r1's net_c route loses the r2 next hop and uses r3; net_b becomes an OSPF route via r3 at cost 30. r2's net_a route uses r3 only, and r3's net_b route uses r2 only. Complete before/after tables for all routers are in route-before.txt and route-after.txt.
All three route metrics and next hops were checked, excluding volatile uptime fields. The route change is much faster than the peer's dead timer: r1 immediately knows its own interface is down and can advertise that change across the remaining triangle. The remote neighbour record still appears in route-after.txt because adjacency expiry is a separate event.

**B5:** We waited for r2's old adjacency to expire before bringing r1 eth1 up. Restoration requires neighbour discovery, adjacency/database exchange and SPF; it is not the reverse of local failure detection. The measured 15-second route restoration need not equal one hello period because adjacency and SPF scheduling add delay. route-restored.txt records the returned ECMP paths.

**C1/C2/C3:** Increasing r1 eth0's OSPF cost to 100 leaves all interfaces up. r1's route to net_c remains cost 20 but loses the next hop through r3, leaving r2 only. route-cost-before.txt and route-cost-after.txt contain all routers' tables. Cost update latency is much lower than silent-failure detection in this run, but the administrative link-down was also fast. The small 0.165/0.182-second difference is within the command/poll overhead and is not evidence of a meaningful relative speed advantage.

**Silent-failure control:** Temporary INPUT/OUTPUT drop rules were placed only inside r1's network namespace on eth1. The interface stayed UP, so the routers had to notice missing hello packets. Rerouting took about 34 seconds, consistent with the remaining portion of the 40-second dead interval (failure did not occur exactly when the last hello was received). Rules were removed after measurement, and the baseline routes were checked again. This supplements, rather than replaces, the assignment's administrative cut.

## Method, limits and reproducibility

- The live interface output confirms Hello=10 s, Dead=40 s and Wait=40 s; the starter config leaves these defaults implicit. See ospf-environment.txt.
- Timings use a monotonic clock starting immediately before the change command. Polls run in parallel across three routers with a 0.2-second sleep between nonmatching samples; Docker and vtysh add overhead. Reported times are first observations, not exact packet-level convergence timestamps. A previous nonmatching sample is useful resolution context but is not a precise lower bound for all routers, whose samples are not perfectly simultaneous.
- Cost-change timing checks r1's affected destination; all three tables are captured afterward. Administrative down/restoration checks all three complete OSPF table signatures. Each scenario was measured once; these are observations, not a statistical benchmark.
- The supplied scenario.sh compares raw route text and captures only r1, so it was not used as the timing oracle. Dedicated measure_ospf.py and measure_silent_failure.py collect the data. They restore the interface/cost and remove the temporary namespace firewall rules.
- The starter Docker Hub tag did not exist; compose.yml uses the official same-version Quay image. Explicit interface_name settings prevent Docker network attachment order from swapping eth0/eth1. vtysh.conf files enable integrated configuration and remove startup warnings.
- To reproduce on a Docker Linux host: start `docker compose --profile routing up -d r1 r2 r3`, wait for FULL neighbours, then run `python3 w06-routing/measure_ospf.py` and `sudo python3 w06-routing/measure_silent_failure.py`. Keep WSL running throughout. The supplement needs host iptables/nsenter. Compose must support interface_name.

References: [FRRouting official releases](https://github.com/FRRouting/frr/releases), [Docker Engine Ubuntu installation](https://docs.docker.com/engine/install/ubuntu/).
