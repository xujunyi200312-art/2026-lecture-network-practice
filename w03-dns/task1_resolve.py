#!/usr/bin/env python3
"""Week 3 · Task 1 — Build your own iterative resolver.

Textbook §2.4.2 - §2.4.3.

`dig +trace` walks root -> TLD -> authoritative for you. In this task you do
that walk yourself: start at a root server, read the delegation it returns,
ask the next server, and keep going until somebody answers authoritatively.

You may shell out to `dig` for the transport, or use a DNS library
(`dnspython` is in the container). Either is fine - what matters is that
*you* follow the delegations rather than letting a tool do it.

    python3 task1_resolve.py www.korea.ac.kr
    python3 task1_resolve.py --verify        # check yourself against dig

Pass condition
--------------
`--verify` resolves five names with your resolver and with `dig`, and the
addresses must agree. A name behind a CDN may legitimately return a different
address each time; the harness compares the *set of authoritative nameservers*
you ended at for those, not the address.
"""
import argparse, subprocess, sys

# Root servers. Everything starts here; there is no earlier step.
ROOT_SERVERS = [
    "198.41.0.4",       # a.root-servers.net
    "199.9.14.201",     # b.root-servers.net
    "192.33.4.12",      # c.root-servers.net
]

# (name, kind).  "stable" names must match dig exactly.  "cdn" names are served
# from many replicas and may legitimately give you a different address than dig
# got a second earlier - for those we only require that you reached an answer.
VERIFY_NAMES = [
    ("www.korea.ac.kr", "stable"),
    ("dns.google", "stable"),
    ("en.wikipedia.org", "stable"),
    ("www.stanford.edu", "stable"),
    ("www.microsoft.com", "cdn"),
]


import dns.exception, dns.flags, dns.message, dns.name, dns.query, dns.rcode, dns.rdatatype

class Resolver:
    """IPv4 iterative resolver; every outgoing query has RD cleared."""

    def resolve(self, name):
        self.path = []
        self.events = []
        self.visited = set()
        address = self._resolve(name, 0, frozenset())
        return address, list(self.path)

    def _resolve(self, name, depth, active):
        name = dns.name.from_text(name).canonicalize().to_text()
        if depth > 32 or name in active:
            raise RuntimeError("CNAME/nameserver loop or depth limit: " + name)
        return self._walk(name, ROOT_SERVERS, depth, active | {name})

    def _query(self, name, server):
        if len(self.path) >= 128:
            raise RuntimeError("Query limit reached")
        query = dns.message.make_query(name, dns.rdatatype.A)
        query.flags &= ~dns.flags.RD
        self.path.append(server)
        self.events.append({"name": name, "server": server, "transport": "UDP"})
        response = dns.query.udp(query, server, timeout=2)
        if response.flags & dns.flags.TC:
            if len(self.path) >= 128:
                raise RuntimeError("Query limit reached")
            self.path.append(server)
            self.events.append({"name": name, "server": server, "transport": "TCP"})
            response = dns.query.tcp(query, server, timeout=2)
        return response

    def _walk(self, name, servers, depth, active, zone="."):
        if depth > 32:
            raise RuntimeError("Delegation depth limit reached")
        errors = []
        qname = dns.name.from_text(name)
        parent_zone = dns.name.from_text(zone)
        for server in servers:
            key = (name, server)
            if key in self.visited:
                continue
            self.visited.add(key)
            try:
                response = self._query(name, server)
                if response.rcode() != dns.rcode.NOERROR:
                    raise RuntimeError(dns.rcode.to_text(response.rcode()))

                # Only accept an authoritative answer for the current name.
                if response.flags & dns.flags.AA:
                    for rrset in response.answer:
                        if rrset.name == qname and rrset.rdtype == dns.rdatatype.CNAME:
                            target = rrset[0].target.to_text()
                            return self._resolve(target, depth + 1, active)
                    for rrset in response.answer:
                        if rrset.name == qname and rrset.rdtype == dns.rdatatype.A:
                            return rrset[0].address
                    raise RuntimeError("Authoritative response has no A/CNAME")

                referrals = [r for r in response.authority
                             if r.rdtype == dns.rdatatype.NS
                             and qname.is_subdomain(r.name)
                             and r.name.is_subdomain(parent_zone)
                             and r.name != parent_zone]
                if not referrals:
                    raise RuntimeError("No relevant delegation")
                referral = max(referrals, key=lambda r: len(r.name.labels))
                names = [r.target for r in referral]

                # Scope additional addresses to the responding parent zone, not
                # the child zone. A root referral for .com may legitimately name
                # a.gtld-servers.net; rejecting that address creates circular
                # .com/.net nameserver lookups. Still ignore unrelated records.
                glue = {}
                for rrset in response.additional:
                    if (rrset.rdtype == dns.rdatatype.A and rrset.name in names
                            and rrset.name.is_subdomain(parent_zone)):
                        glue[rrset.name] = [r.address for r in rrset]

                # Try all available glue addresses before resolving NS names.
                addresses = list(dict.fromkeys(
                    ip for ns in names for ip in glue.get(ns, [])))
                if addresses:
                    try:
                        return self._walk(name, addresses, depth + 1, active,
                                          referral.name.to_text())
                    except (dns.exception.DNSException, OSError, RuntimeError) as exc:
                        errors.append(str(exc))

                for ns in names:
                    if ns in glue:
                        continue
                    try:
                        self.events.append({"no_glue": ns.to_text(), "for": name})
                        address = self._resolve(ns.to_text(), depth + 1, active)
                        return self._walk(name, [address], depth + 1, active,
                                          referral.name.to_text())
                    except (dns.exception.DNSException, OSError, RuntimeError) as exc:
                        errors.append(str(exc))
            except (dns.exception.DNSException, OSError, RuntimeError) as exc:
                errors.append(server + ": " + str(exc))
        detail = "; ".join(errors[-3:]) or "all candidates already visited"
        raise RuntimeError("Could not resolve " + name + ": " + detail)


# ------------------------------------------------------------------- harness
def dig_answer(name):
    """What the system resolver says, for comparison."""
    out = subprocess.run(["dig", "+short", name, "A"],
                         capture_output=True, text=True).stdout
    return [l for l in out.split() if l and l[0].isdigit()]


def verify():
    r, failures = Resolver(), 0
    for name, kind in VERIFY_NAMES:
        try:
            addr, path = r.resolve(name)
        except NotImplementedError:
            print("Nothing implemented yet - write Resolver.resolve first.")
            return 1
        except Exception as e:
            print(f"  FAIL  {name:<22} your resolver raised {e!r}")
            failures += 1
            continue
        expected = dig_answer(name)
        if addr in expected:
            note = ""
        elif kind == "cdn":
            note = "  <- differs, but this name is CDN-hosted. Explain it."
        else:
            note = "  <- should have matched"
            failures += 1
        print(f"  {'FAIL' if note.endswith('matched') else 'ok  '}  {name:<22} "
              f"you={addr:<16} dig={','.join(expected) or '-'}   "
              f"hops={len(path)}{note}")
    print(f"\n  {len(VERIFY_NAMES) - failures}/{len(VERIFY_NAMES)} ok")
    return 1 if failures else 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("name", nargs="?", default="www.korea.ac.kr")
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()

    if a.verify:
        sys.exit(verify())

    addr, path = Resolver().resolve(a.name)
    for i, server in enumerate(path, 1):
        print(f"  {i}. asked {server}")
    print(f"\n  {a.name} -> {addr}")


if __name__ == "__main__":
    main()
