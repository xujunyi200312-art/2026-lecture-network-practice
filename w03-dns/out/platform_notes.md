# Windows execution and verification

The lab was run directly on Windows with Python 3.13.16, dnspython 2.8.0, Wireshark/TShark 4.6.9 and ISC dig 9.16.50. Docker/WSL could not create its virtual disk, so the native Windows route was used.

`test_tasks.py` has a two-line compatibility change: DNS response flags are accepted as either `0`/`1` or `False`/`True` (case-insensitive). TShark 4.6.9 on this machine emits the latter. The check still requires both queries and responses; no pass condition was removed. `bench.py` is unchanged.

The actual user-run verification produced 5/5 ok; the full tests produced 12 passed, 0 failed and 3 skipped. The three skips are the original human-reviewed requirements: root start, no-glue handling, and the cache lower-bound argument. They are not automated passes. See `verify.txt`, `tests.txt`, `observation.md` and the submitted capture for evidence.

The resolver was corrected to evaluate additional NS addresses against the responding parent zone, rather than insisting that every nameserver name belong to the delegated child zone. This permits root referrals such as .com served by nameservers in .net. Its mock regression tests covered timeout failover, CNAME restart/loop termination, absent glue, root sibling-domain glue, path ordering, non-recursive queries, and TCP fallback. Mock tests do not replace the five-name live verification.
