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
