# Week 04 observations

## Task 1 - Reliable delivery
I chose stop-and-wait: when an ACK is lost, the receiver must ACK the repeated sequence number without appending its payload again; old ACKs must not advance the sender. Loss would stall a sender without a timeout, while blindly appending retransmissions would corrupt the result.
For 2,000 bytes, the minimum is 250 data packets (500 transmissions including one ACK each). Seed 246 used 323 data sends (1.292x), or 614 data-plus-ACK sends (1.228x); seed 999 used 299 (1.196x), or 578 total (1.156x). Channel-created duplicate copies are counted separately in extra-validation.json.
Both required seeds passed, plus 260 varied-payload/edge/stress cases, including empty input and 30% loss, 50% duplication and 80% reordering; the implementations only call the channel's send/receive methods.

## Task 2 - Real TCP capture and throughput (SECOND SESSION PENDING)
In the own-machine capture, packets 1/2/3 are SYN/SYN-ACK/ACK; client/server ISNs are 612231287/3473258583. Client SYN: MSS 1460, WS shift 8 (x256), SACK permitted; server SYN-ACK: MSS 1360, WS shift 13 (x8192), SACK permitted. Independently selected ISNs distinguish connection incarnations and make old-segment confusion and off-path guessing harder; Wireshark's relative zero is only a display convention.
The client advertises 255 x 256 = 65,280 bytes in packet 3, then 8186 x 256 = 2,095,616 in packet 5848; the next packet's estimated bytes in flight is 1,649,500, below that window. SYN windows are unscaled. This does not establish a unique bottleneck: loss/reordering, congestion-window growth, path capacity and server/TLS delays remain possible (see measurement-analysis.md).
The current Ethernet session (2026-10-13 21:16, host clock) measured median 184.02 Mbps, min-max 132.17-207.26 Mbps (40.80% relative spread), and median TCP handshake 13.17 ms. A second genuine network/time session is still missing; no comparison is claimed. A longer RTT slows ACK-clocked slow start and limits window/RTT throughput, but these five samples alone do not isolate causality.

## Task 3 - Congestion control
The fixed window is the worst neighbour despite its 986.75 packets/1000-slot goodput: 37.40% loss, 2340 retransmissions and an 8.7625-packet average queue waste capacity and delay other traffic. My conservative startup (threshold 16), additive growth and 0.75 multiplicative backoff achieve 964.00 (97.70% of baseline), 0.461% loss, 18 retransmissions and queue 4.4695: strong.
The window oscillates rather than converging to a constant (18.22-31.94 across the final 1000 ACK events); it spends time near the approximately 20-packet pipe and probes into the 10-packet queue. Loss feedback is delayed, so brief overshoot is expected; a recovery ACK budget avoids cutting repeatedly for the same flight.
Changing backoff from 0.50 to 0.75 raised goodput from 837.25 to 964.00 while queue rose from 3.0610 to 4.4695; 0.80 reached 975.25 but queue 5.20675 failed the limit. These measured comparisons use the unchanged bench.py and only ACK/loss feedback.
