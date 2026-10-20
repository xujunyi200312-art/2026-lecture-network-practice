# Week 05 observations

## Task 1
/31 returns both endpoints as usable on a point-to-point link; /32 returns the single host. The third tuple value is the all-host-bits-one endpoint, not an actual broadcast for these two cases.
10.20.30.70 matches 10.0.0.0/8, 10.20.0.0/16, 10.20.30.0/24, and 10.20.30.64/26 (plus the default /0); longest-prefix match chooses /26 and lab-rack-2.
Duplicate identical prefixes retain the first inserted next hop; different networks of equal length cannot both match one address. All ten supplied checks pass.

## Task 2
Ethernet has private IPv4 192.168.219.101/24 and external IPv4 116.42.166.72, supporting at least one NAT; without the router WAN address the exact number is unproven.
The hotspot changed the private address to 172.20.10.5/28, gateway to 172.20.10.1, and public address to 39.7.24.63: a different local address pool and Internet egress, while private addressing remained in use.
In the official Path B trace, Discover is 0.0.0.0 → 255.255.255.255 because the client lacks an assigned address; the server grants 86400 seconds with renewal at 43200 seconds.

## Task 3
I grouped routes in dictionaries by prefix length, searched longest first, and retained the first duplicate: O(N + L) storage with dictionary overhead, where L ≤ 33.
Lookup performs at most L masked dictionary probes (expected O(L), bounded by IPv4 width rather than route count); 20000 answers match, with 11.893 s versus 0.006 s and 1840.1× speedup in this run.
A bitwise trie maps naturally to predictable hardware stages; Python dictionaries do their core probing in compiled code, avoiding the interpreted per-bit traversal overhead.
