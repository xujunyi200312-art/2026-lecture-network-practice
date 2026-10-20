# Week 05 — Address and DHCP study

## Measurement status

The first network was measured on this Windows computer on 2026-10-20
(Asia/Shanghai). Raw interface and route output is in `addresses.json`.
The public IPv4 request was repeated outside the restricted execution sandbox
using `curl -4 --noproxy "*" https://api.ipify.org`.
The second network was measured after switching to a phone hotspot; the
Ethernet interface was disconnected and the active IPv4 default route used
172.20.10.1 through WLAN, confirming that the Internet path had changed.
The DHCP section uses the course-authorized official-trace alternative, not
a capture of this computer.

## A1–A4: Current Ethernet network

| Item | Observed value |
|---|---|
| Interface | Realtek PCIe GbE Family Controller, Ethernet |
| Local IPv4 | 192.168.219.101 |
| Subnet mask | 255.255.255.0 (/24) |
| Network | 192.168.219.0/24 |
| First usable host | 192.168.219.1 |
| Last usable host | 192.168.219.254 |
| Broadcast | 192.168.219.255 |
| Default gateway | 192.168.219.1 |
| DHCP server | 192.168.219.1 |
| Public IPv4 seen by ipify | 116.42.166.72 |

Manual calculation: /24 leaves 8 host bits, so the block contains 2^8 = 256
addresses. ANDing the last octet, 101 (01100101), with 0 (00000000) gives 0;
the first three octets are unchanged. The network is therefore 192.168.219.0.
Setting all 8 host bits gives .255; excluding network and broadcast leaves
.1 through .254, or 254 ordinary usable hosts. The implemented
`network_range("192.168.219.0/24")` confirms
`("192.168.219.1", "192.168.219.254", "192.168.219.255")`.

The gateway .1 is inside this usable range. On this ordinary Ethernet subnet,
the host must reach the gateway directly by ARP before it can send off-subnet
traffic. Special point-to-point or explicit on-link configurations can differ;
the observed route here is the ordinary directly connected case.

## A5: NAT evidence and limits

192.168.219.101 belongs to the RFC 1918 private block 192.168.0.0/16.
116.42.166.72 is outside the private ranges and is the external IPv4 observed
for the direct HTTPS connection. For this private-address IPv4 connection,
the difference supports at least one address-translation boundary.
It does not distinguish one NAT from two.

To distinguish them, inspect the local router's WAN IPv4 and compare it with
116.42.166.72. A private or shared WAN address with a different external IPv4
would support an additional upstream NAT; a matching public WAN address would
be consistent with a single router NAT. A traceroute can provide clues but
cannot count NAT devices reliably. The shared block 100.64.0.0/10 is not
RFC 1918 space; seeing it suggests provider address sharing, but alone does
not prove exactly two translations. Router WAN data was not collected here,
so the exact NAT count remains unknown.

## B1–B3: Two-network comparison

| Item | network-1-ethernet | network-2-phone-hotspot |
|---|---|---|
| Local IPv4 | 192.168.219.101 | 172.20.10.5 |
| Mask | 255.255.255.0 (/24) | 255.255.255.240 (/28) |
| Network | 192.168.219.0 | 172.20.10.0 |
| Usable range | 192.168.219.1–192.168.219.254 | 172.20.10.1–172.20.10.14 |
| Broadcast | 192.168.219.255 | 172.20.10.15 |
| Gateway | 192.168.219.1 | 172.20.10.1 |
| Public IPv4 | 116.42.166.72 | 39.7.24.63 |

Hotspot calculation: /28 leaves four host bits, making blocks of 16 addresses.
The last-octet AND is 5 (00000101) AND 240 (11110000) = 0. Therefore the
network is 172.20.10.0, the broadcast is .15, and the 14 usable addresses run
from .1 to .14. `network_range("172.20.10.0/28")` returns exactly
`("172.20.10.1", "172.20.10.14", "172.20.10.15")`. Gateway .1 is on-link.

Both local and public addresses changed. The hotspot assigned a different
private subnet and mask from the Ethernet router, explaining the local change.
The direct external IPv4 measurement changed because traffic now used a
different Internet egress. What remained the same was the use of private
client addressing and an on-subnet gateway; the actual address values and
subnet size changed.

172.20.10.5 is in RFC 1918's 172.16.0.0/12 block; 39.7.24.63 is not private.
This supports at least one translation for hotspot IPv4 traffic. The phone's
upstream IPv4 was not measured, so a second carrier NAT is possible but not
established. A cellular network label alone cannot determine the NAT count.

## C1–C4: Official DHCP trace (Path B)

Source archive:
https://www-net.cs.umass.edu/wireshark-labs/wireshark-traces-9e.zip

Source capture: `dhcp-wireshark-trace1-1.pcapng`. The submitted `dhcp.pcapng`
is the six DHCP packets filtered from that capture, preserving packet contents
and timestamps. `dhcp-fields.tsv` contains the extracted fields in the order:
frame, source IPv4, destination IPv4, DHCP message type, lease seconds, offered
IPv4, broadcast flag, renewal seconds.

| Frames in filtered capture | Message | Source → destination | Server lease |
|---|---|---|---|
| 1–2 | Discover (1) | 0.0.0.0 → 255.255.255.255 | Not a server offer |
| 3–4 | Offer (2) | 192.168.86.1 → 192.168.86.65 | 86400 seconds |
| 5 | Request (3) | 0.0.0.0 → 255.255.255.255 | — |
| 6 | Ack (5) | 192.168.86.1 → 192.168.86.65 | 86400 seconds |

Discover uses 0.0.0.0 because the client has not yet acquired an IPv4 address
it can use as its source. It broadcasts to 255.255.255.255 because it does not
yet know which DHCP server can configure it. The 7776000-second value in
Discover is a client request; it is not the lease granted by the server.

The server offers and acknowledges 86400 seconds = 24 hours. The trace
explicitly supplies renewal time T1 = 43200 seconds = 12 hours. At that time,
the client normally attempts to renew by sending DHCPREQUEST to its server
while continuing to use the existing lease. If renewal fails, it later tries
rebinding; it must stop using the address if the lease expires.

The observed Ack is unicast to 192.168.86.65. The server now knows the selected
address and the client's hardware address, and the broadcast flag is clear,
allowing delivery to a client that can receive unicast before configuration is
complete. This does not require assuming the client already fully configured
the address: even the Offer is unicast in this trace. Clients requiring
broadcast delivery can set the broadcast flag.

## Attribution

Wireshark lab trace files from J.F. Kurose and K.W. Ross,
*Computer Networking: A Top-Down Approach*, 9th ed.
https://gaia.cs.umass.edu/kurose_ross/
Copyright 1996-2025 J.F. Kurose, K.W. Ross. All Rights Reserved.
