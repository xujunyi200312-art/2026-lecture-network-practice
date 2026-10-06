### Task 1
For www.korea.ac.kr I queried 198.41.0.4, 210.101.61.1 and 163.152.11.6, obtaining 163.152.6.10 in three queries; the root returned a .kr delegation rather than the host's address because it serves the root zone.
My resolver follows glue when present; without usable glue it starts a separate root-based lookup for the nameserver name. The captured Korea University walk used glue and incurred zero extra nameserver lookups; no-glue handling was tested with simulated responses, not observed in this capture.
The five-name verification passed under the lab's rules: Microsoft returned 104.75.39.192 iteratively versus 104.74.176.230 via dig, consistent with its observed Akamai CNAME chain and CDN answer variation, not proof of a particular location; the subsequent test also passed. Queries clear RD and have loop/depth limits; a laptop normally sends one request to its recursive resolver.

### Task 2
In my six-packet capture, packet 2 is a delegation (0 answers, 6 NS authority records, 10 additional records), while packet 6 is an authoritative A answer; the largest DNS message is 341 bytes (383-byte Ethernet frame).
The last-two-label rule wrongly calls wikipedia.org -> dyna.wikimedia.org third-party: Wikimedia operates Wikipedia and its own CDN. Using the documented/course CDN cohort, 7/10 sites changed address sets across resolvers or networks; Ethernet had 24/36 successes and phone-hotspot 36/36, with Ethernet Quad9 timeouts excluded.
Only Adobe and Apple changed across networks with a resolver label held fixed (2/10); differing IPs do not prove a nearer replica without location/latency evidence. The hostname-evidence-only cohort excluding Netflix's unverified website CDN endpoint gives 7/9; cohort definitions and sources are in report.md.

### Task 3
The baseline's fixed 60-second lifetime returns expired short-TTL records and unnecessarily refreshes long-TTL records; my TTL-aware dictionary cache reduces upstream queries from 325 to 275, raises hit rate from 67.5% to 72.5%, and returns zero stale answers.
For this workload with an empty initial cache and TTL-respecting answers, the minimum is 275: fetch each name on its first request and then on the first request after expiry. Shifting an earlier refresh to the first uncovered request preserves coverage and cannot shorten its expiry, so refreshing earlier cannot reduce this minimum.
www.microsoft.com is especially poorly handled: its 20-second TTL and highest request weight make the baseline's 60-second retention expose many requests to expired data. The measured simulated time falls from 6.5 s to 5.5 s.
