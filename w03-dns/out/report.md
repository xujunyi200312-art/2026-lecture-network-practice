# DNS steering report

Rule under test: label a site third-party when the final CNAME name and the original site have different last-two-label suffixes. This is a heuristic, not a reliable ownership or CDN test.

Suffixes below are NOT verified DNS zone boundaries or public-suffix-aware domains.

| Site | Network / run | Resolver | Chain length | Final name / suffix | Third-party (reviewed) | Rule verdict | A addresses |
|---|---|---|---:|---|---|---|---|
| www.microsoft.com | ethernet / 20261006T102539Z-3b88e8f4 | google | 2 | e13678.dscb.akamaiedge.net / akamaiedge.net | yes | yes | 104.94.218.45 |
| www.microsoft.com | ethernet / 20261006T102539Z-3b88e8f4 | system | 2 | e13678.dscb.akamaiedge.net / akamaiedge.net | yes | yes | 104.94.218.45 |
| www.microsoft.com | phone-hotspot / 20261006T103031Z-116c05f7 | google | 2 | e13678.dscb.akamaiedge.net / akamaiedge.net | yes | yes | 104.94.218.45 |
| www.microsoft.com | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 2 | e13678.dscb.akamaiedge.net / akamaiedge.net | yes | yes | 23.0.194.92 |
| www.microsoft.com | phone-hotspot / 20261006T103031Z-116c05f7 | system | 2 | e13678.dscb.akamaiedge.net / akamaiedge.net | yes | yes | 104.94.218.45 |
| www.netflix.com | ethernet / 20261006T102539Z-3b88e8f4 | google | 1 | www.prod.ftl.netflix.com / netflix.com | no | no | 207.45.72.1, 207.45.73.1 |
| www.netflix.com | ethernet / 20261006T102539Z-3b88e8f4 | system | 1 | www.prod.ftl.netflix.com / netflix.com | no | no | 207.45.72.1, 207.45.73.1 |
| www.netflix.com | phone-hotspot / 20261006T103031Z-116c05f7 | google | 1 | www.prod.ftl.netflix.com / netflix.com | no | no | 207.45.72.1, 207.45.73.1 |
| www.netflix.com | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 1 | www.prod.ftl.netflix.com / netflix.com | no | no | 207.45.72.1, 207.45.73.1 |
| www.netflix.com | phone-hotspot / 20261006T103031Z-116c05f7 | system | 1 | www.prod.ftl.netflix.com / netflix.com | no | no | 207.45.72.1, 207.45.73.1 |
| www.adobe.com | ethernet / 20261006T102539Z-3b88e8f4 | google | 2 | a1319.dscr.akamai.net / akamai.net | yes | yes | 182.162.106.139, 182.162.106.144 |
| www.adobe.com | ethernet / 20261006T102539Z-3b88e8f4 | system | 2 | a1319.dscr.akamai.net / akamai.net | yes | yes | 23.76.153.115, 23.76.153.121 |
| www.adobe.com | phone-hotspot / 20261006T103031Z-116c05f7 | google | 2 | a1319.dscr.akamai.net / akamai.net | yes | yes | 23.32.4.11, 23.32.4.122, 23.32.4.123, 23.32.4.138, 23.32.4.24, 23.32.4.25, 23.32.4.27, 23.32.4.8, 23.32.4.9 |
| www.adobe.com | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 2 | a1319.dscr.akamai.net / akamai.net | yes | yes | 23.44.175.16, 23.44.175.17 |
| www.adobe.com | phone-hotspot / 20261006T103031Z-116c05f7 | system | 2 | a1319.dscr.akamai.net / akamai.net | yes | yes | 23.67.53.113, 23.67.53.145 |
| www.cnn.com | ethernet / 20261006T102539Z-3b88e8f4 | google | 1 | cnn-tls.map.fastly.net / fastly.net | yes | yes | 151.101.131.5, 151.101.195.5, 151.101.3.5, 151.101.67.5 |
| www.cnn.com | ethernet / 20261006T102539Z-3b88e8f4 | system | 1 | cnn-tls.map.fastly.net / fastly.net | yes | yes | 146.75.51.5 |
| www.cnn.com | phone-hotspot / 20261006T103031Z-116c05f7 | google | 1 | cnn-tls.map.fastly.net / fastly.net | yes | yes | 151.101.131.5, 151.101.195.5, 151.101.3.5, 151.101.67.5 |
| www.cnn.com | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 1 | cnn-tls.map.fastly.net / fastly.net | yes | yes | 151.101.131.5, 151.101.195.5, 151.101.3.5, 151.101.67.5 |
| www.cnn.com | phone-hotspot / 20261006T103031Z-116c05f7 | system | 1 | cnn-tls.map.fastly.net / fastly.net | yes | yes | 146.75.51.5 |
| www.apple.com | ethernet / 20261006T102539Z-3b88e8f4 | google | 3 | e6858.dsce9.akamaiedge.net / akamaiedge.net | yes | yes | 23.49.205.28 |
| www.apple.com | ethernet / 20261006T102539Z-3b88e8f4 | system | 3 | e6858.dsce9.akamaiedge.net / akamaiedge.net | yes | yes | 104.94.216.37 |
| www.apple.com | phone-hotspot / 20261006T103031Z-116c05f7 | google | 3 | e6858.dsce9.akamaiedge.net / akamaiedge.net | yes | yes | 23.221.151.70 |
| www.apple.com | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 3 | e6858.dsce9.akamaiedge.net / akamaiedge.net | yes | yes | 23.0.193.49 |
| www.apple.com | phone-hotspot / 20261006T103031Z-116c05f7 | system | 3 | e6858.dsce9.akamaiedge.net / akamaiedge.net | yes | yes | 23.41.89.203 |
| www.korea.ac.kr | ethernet / 20261006T102539Z-3b88e8f4 | google | 0 | www.korea.ac.kr / ac.kr | no | no | 163.152.6.10 |
| www.korea.ac.kr | ethernet / 20261006T102539Z-3b88e8f4 | system | 0 | www.korea.ac.kr / ac.kr | no | no | 163.152.6.10 |
| www.korea.ac.kr | phone-hotspot / 20261006T103031Z-116c05f7 | google | 0 | www.korea.ac.kr / ac.kr | no | no | 163.152.6.10 |
| www.korea.ac.kr | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 0 | www.korea.ac.kr / ac.kr | no | no | 163.152.6.10 |
| www.korea.ac.kr | phone-hotspot / 20261006T103031Z-116c05f7 | system | 0 | www.korea.ac.kr / ac.kr | no | no | 163.152.6.10 |
| www.stanford.edu | ethernet / 20261006T102539Z-3b88e8f4 | google | 1 | stanford.netlifyglobalcdn.com / netlifyglobalcdn.com | yes | yes | 15.197.167.90, 3.33.186.135 |
| www.stanford.edu | ethernet / 20261006T102539Z-3b88e8f4 | system | 1 | stanford.netlifyglobalcdn.com / netlifyglobalcdn.com | yes | yes | 15.197.167.90, 3.33.186.135 |
| www.stanford.edu | phone-hotspot / 20261006T103031Z-116c05f7 | google | 1 | stanford.netlifyglobalcdn.com / netlifyglobalcdn.com | yes | yes | 15.197.167.90, 3.33.186.135 |
| www.stanford.edu | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 1 | stanford.netlifyglobalcdn.com / netlifyglobalcdn.com | yes | yes | 15.197.167.90, 3.33.186.135 |
| www.stanford.edu | phone-hotspot / 20261006T103031Z-116c05f7 | system | 1 | stanford.netlifyglobalcdn.com / netlifyglobalcdn.com | yes | yes | 15.197.167.90, 3.33.186.135 |
| www.bbc.co.uk | ethernet / 20261006T102539Z-3b88e8f4 | google | 2 | bbc.map.fastly.net / fastly.net | yes | yes | 151.101.0.81, 151.101.128.81, 151.101.192.81, 151.101.64.81 |
| www.bbc.co.uk | ethernet / 20261006T102539Z-3b88e8f4 | system | 2 | bbc.map.fastly.net / fastly.net | yes | yes | 146.75.48.81 |
| www.bbc.co.uk | phone-hotspot / 20261006T103031Z-116c05f7 | google | 2 | bbc.map.fastly.net / fastly.net | yes | yes | 151.101.0.81, 151.101.128.81, 151.101.192.81, 151.101.64.81 |
| www.bbc.co.uk | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 2 | bbc.map.fastly.net / fastly.net | yes | yes | 151.101.0.81, 151.101.128.81, 151.101.192.81, 151.101.64.81 |
| www.bbc.co.uk | phone-hotspot / 20261006T103031Z-116c05f7 | system | 2 | bbc.map.fastly.net / fastly.net | yes | yes | 146.75.48.81 |
| www.spotify.com | ethernet / 20261006T102539Z-3b88e8f4 | google | 1 | atc.spotify.map.fastly.net / fastly.net | yes | yes | 151.101.131.42, 151.101.195.42, 151.101.3.42, 151.101.67.42 |
| www.spotify.com | ethernet / 20261006T102539Z-3b88e8f4 | system | 1 | atc.spotify.map.fastly.net / fastly.net | yes | yes | 146.75.51.42 |
| www.spotify.com | phone-hotspot / 20261006T103031Z-116c05f7 | google | 1 | atc.spotify.map.fastly.net / fastly.net | yes | yes | 151.101.131.42, 151.101.195.42, 151.101.3.42, 151.101.67.42 |
| www.spotify.com | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 1 | atc.spotify.map.fastly.net / fastly.net | yes | yes | 151.101.131.42, 151.101.195.42, 151.101.3.42, 151.101.67.42 |
| www.spotify.com | phone-hotspot / 20261006T103031Z-116c05f7 | system | 1 | atc.spotify.map.fastly.net / fastly.net | yes | yes | 146.75.51.42 |
| www.github.com | ethernet / 20261006T102539Z-3b88e8f4 | google | 1 | github.com / github.com | unknown | no | 20.200.245.247 |
| www.github.com | ethernet / 20261006T102539Z-3b88e8f4 | system | 1 | github.com / github.com | unknown | no | 20.200.245.247 |
| www.github.com | phone-hotspot / 20261006T103031Z-116c05f7 | google | 1 | github.com / github.com | unknown | no | 20.200.245.247 |
| www.github.com | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 1 | github.com / github.com | unknown | no | 20.27.177.113 |
| www.github.com | phone-hotspot / 20261006T103031Z-116c05f7 | system | 1 | github.com / github.com | unknown | no | 20.200.245.247 |
| www.wikipedia.org | ethernet / 20261006T102539Z-3b88e8f4 | google | 1 | dyna.wikimedia.org / wikimedia.org | no | yes | 103.102.166.224 |
| www.wikipedia.org | ethernet / 20261006T102539Z-3b88e8f4 | system | 1 | dyna.wikimedia.org / wikimedia.org | no | yes | 103.102.166.224 |
| www.wikipedia.org | phone-hotspot / 20261006T103031Z-116c05f7 | google | 1 | dyna.wikimedia.org / wikimedia.org | no | yes | 103.102.166.224 |
| www.wikipedia.org | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 1 | dyna.wikimedia.org / wikimedia.org | no | yes | 103.102.166.224 |
| www.wikipedia.org | phone-hotspot / 20261006T103031Z-116c05f7 | system | 1 | dyna.wikimedia.org / wikimedia.org | no | yes | 103.102.166.224 |
| www.nytimes.com | ethernet / 20261006T102539Z-3b88e8f4 | google | 3 | nytimes.map.fastly.net / fastly.net | yes | yes | 151.101.1.164, 151.101.129.164, 151.101.193.164, 151.101.65.164 |
| www.nytimes.com | ethernet / 20261006T102539Z-3b88e8f4 | system | 3 | nytimes.map.fastly.net / fastly.net | yes | yes | 146.75.49.164 |
| www.nytimes.com | phone-hotspot / 20261006T103031Z-116c05f7 | google | 3 | nytimes.map.fastly.net / fastly.net | yes | yes | 151.101.1.164, 151.101.129.164, 151.101.193.164, 151.101.65.164 |
| www.nytimes.com | phone-hotspot / 20261006T103031Z-116c05f7 | quad9 | 3 | nytimes.map.fastly.net / fastly.net | yes | yes | 151.101.1.164, 151.101.129.164, 151.101.193.164, 151.101.65.164 |
| www.nytimes.com | phone-hotspot / 20261006T103031Z-116c05f7 | system | 3 | nytimes.map.fastly.net / fastly.net | yes | yes | 146.75.49.164 |

## Networks and steering

Networks: ethernet, phone-hotspot

Only latest runs per network are compared. Failed queries are excluded.

7 of 10 reviewed CDN-hosted sites returned different IPv4 address sets across resolvers or networks.

Different addresses demonstrate answer variation, not necessarily nearby replicas. Time variation, load balancing and anycast also limit the conclusion.

## Classification review and counterexample

- www.wikipedia.org: rule says True, reviewed third-party=False. The chain ends at dyna.wikimedia.org. Wikipedia is a [Wikimedia project](https://www.wikimedia.org/), and Wikimedia operates its own CDN: [Wikimedia CDN documentation](https://wikitech.wikimedia.org/wiki/CDN). Different domain suffixes do not imply a different organization. This is the observed false positive of the rule.
- www.microsoft.com: Observed edgekey.net/edgesuite.net chain identifies Akamai as a third-party CDN. [Akamai edge-hostname documentation](https://techdocs.akamai.com/edge-hostnames/docs/edge-hn-terminology)
- www.netflix.com: First-party classification follows [course Task 2](https://github.com/codingchild2424/2026-lecture-network-practice/blob/main/w03-dns/task2.md). The chain stays in netflix.com. [Netflix Open Connect](https://openconnect.netflix.com/Open-Connect-Briefing-Paper.pdf) documents its own video CDN; querying www.netflix.com does not itself measure video delivery or prove this web endpoint is Open Connect.
- www.adobe.com: Observed edgekey.net/edgesuite.net chain identifies Akamai as a third-party CDN. [Akamai edge-hostname documentation](https://techdocs.akamai.com/edge-hostnames/docs/edge-hn-terminology)
- www.cnn.com: Observed map.fastly.net chain identifies a third-party Fastly CDN endpoint. [Fastly routing documentation](https://www.fastly.com/documentation/guides/concepts/routing-traffic-to-fastly/)
- www.apple.com: Observed edgekey.net/edgesuite.net chain identifies Akamai as a third-party CDN. [Akamai edge-hostname documentation](https://techdocs.akamai.com/edge-hostnames/docs/edge-hn-terminology)
- www.korea.ac.kr: No CNAME in these measurements, and [course Task 2](https://github.com/codingchild2424/2026-lecture-network-practice/blob/main/w03-dns/task2.md) identifies this site as non-CDN. No-CNAME alone would not establish that for arbitrary sites.
- www.stanford.edu: Observed stanford.netlifyglobalcdn.com points to Netlify, a third-party CDN provider. [Netlify support discussion](https://answers.netlify.com/t/how-can-i-change-which-netlify-site-my-hostname-is-pointing-to/3259).
- www.bbc.co.uk: Observed map.fastly.net chain identifies a third-party Fastly CDN endpoint. [Fastly routing documentation](https://www.fastly.com/documentation/guides/concepts/routing-traffic-to-fastly/)
- www.spotify.com: Observed map.fastly.net chain identifies a third-party Fastly CDN endpoint. [Fastly routing documentation](https://www.fastly.com/documentation/guides/concepts/routing-traffic-to-fastly/)
- www.github.com: Observed chain remains within github.com. DNS alone does not establish whether this endpoint uses an external CDN or a first-party distributed frontend. CDN/third-party status remains unconfirmed, so this site is excluded from the CDN-only denominator; its address variation is retained in the all-sites comparison.
- www.wikipedia.org: The chain ends at dyna.wikimedia.org. Wikipedia is a [Wikimedia project](https://www.wikimedia.org/), and Wikimedia operates its own CDN: [Wikimedia CDN documentation](https://wikitech.wikimedia.org/wiki/CDN). Different domain suffixes do not imply a different organization. This is the observed false positive of the rule.
- www.nytimes.com: Observed map.fastly.net chain identifies a third-party Fastly CDN endpoint. [Fastly routing documentation](https://www.fastly.com/documentation/guides/concepts/routing-traffic-to-fastly/)

## Measurement scope and interpretation

Two actual network runs were recorded on 2026-10-06: `ethernet` and `phone-hotspot`. The raw files record UTC start/end times, CNAME hops, TTLs, full DNS response text, errors and the server used for every successful query.
Ethernet: 24/36 successful (system and Google each 12/12; Quad9 0/12). Phone hotspot: 36/36 successful. Quad9 timeouts on Ethernet are unavailable observations, not changed address sets; they do not by themselves prove deliberate blocking.
The successful system-resolver queries used 168.126.63.1 on Ethernet and 172.20.10.1 on the hotspot. Google used 8.8.8.8; Quad9 used 9.9.9.9. The system resolver's configured list contains additional fallback servers, recorded in chains.json.

### Counts and denominator

The CDN cohort contains ten sites: Microsoft, Netflix, Adobe, CNN, Apple, Stanford, BBC, Spotify, Wikipedia and NYTimes. It includes first-party CDNs, following the course's Netflix classification. Korea University is excluded following the lab's non-CDN example; GitHub is unconfirmed and excluded rather than assumed non-CDN.

- **7 of 10 CDN-classified sites** changed IPv4 address sets across a resolver or network comparison: Microsoft, Adobe, CNN, Apple, BBC, Spotify and NYTimes.
- Across all twelve measured sites, **8 of 12** changed; GitHub is the additional site.
- Comparing different resolvers within the same network: **6/10** on Ethernet, **7/10** on phone hotspot (Ethernet has only system/Google available).
- Holding the resolver label fixed and comparing networks: **2/10**, Adobe and Apple. This holds for Google alone as well as the system resolver; the latter's upstream server also changes with the network. There is no valid cross-network Quad9 pair.
- A stricter cohort requiring hostname-level CDN evidence excludes Netflix's website endpoint: **7/9**. Its first-party video CDN is documented, but this DNS measurement did not query video hosts.

These results support DNS-answer variation, not proof of geographical proximity. There were no replica location or latency measurements, the runs occurred at different times, and public resolvers may use anycast. Equal IP sets do not prove equal physical replicas. The CNAME walk and final A query were separate requests; none of the successful measurements reported a changed canonical name between them.

### Ownership rule and final-zone terminology

The deliberately simple rule compares only the last two labels of the original and final CNAME names. It misclassifies Wikipedia as third-party because wikipedia.org differs from wikimedia.org, although both belong to the Wikimedia organization. The reviewed classification corrects this using ownership evidence. A CDN is not necessarily a third party.
For the requested final-zone column, the table reports the final hostname and its two-label suffix, not a measured SOA zone apex. The naive suffix ac.kr (and co.uk in the input BBC name) is not a registrable organization domain; it must not be interpreted as one. No CNAME also does not exclude an anycast CDN.



## Capture evidence

The submitted `dns.pcapng` contains six packets captured on my Ethernet interface, filtered from the original capture to keep only `www.korea.ac.kr`. Packet numbers below refer to this six-packet file.

| Query | Response | Server | Transaction ID | Interpretation |
|---:|---:|---|---|---|
| 1 | 2 | 198.41.0.4 | 0x2033 | Root delegates to .kr |
| 3 | 4 | 210.101.61.1 | 0xe064 | .kr server delegates to korea.ac.kr |
| 5 | 6 | 163.152.11.6 | 0xdb88 | Authoritative A answer: 163.152.6.10 |

Packet 2 has zero answers, six authority NS records and ten additional records (IPv4/IPv6 glue). Packet 4 has zero answers, two authority NS records and two additional records. Packet 6 has AA set and one answer A record. Thus packet 2 is my delegation example and packet 6 is my final-answer example; the same DNS message format contains different sections.

Packet 2 is the largest response: **341 bytes of DNS message**, or **383 bytes for the entire Ethernet frame** shown in Wireshark's Length column. Its UDP length is 349 bytes, including the eight-byte UDP header. The six NS records and ten glue records make it larger than the final single-A-record response. It was also the largest DNS response in the original capture, before filtering.


## Query failures

- www.microsoft.com / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.405 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
- www.netflix.com / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.403 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
- www.adobe.com / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.406 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
- www.cnn.com / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.403 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
- www.apple.com / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.411 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
- www.korea.ac.kr / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.402 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
- www.stanford.edu / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.402 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
- www.bbc.co.uk / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.409 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
- www.spotify.com / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.407 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
- www.github.com / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.408 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
- www.wikipedia.org / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.403 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
- www.nytimes.com / ethernet / quad9: LifetimeTimeout: The resolution lifetime expired after 5.408 seconds: Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.; Server Do53:9.9.9.9@53 answered The DNS operation timed out.
