# Task 2 measurement evidence

Status: Part A complete; Part B has one actual network session and needs a second.

## Capture provenance and scope

`tcp.pcapng` is an original capture from this Windows machine's Ethernet adapter on 2026-10-13 at 21:15:22 (host local clock), not a textbook trace. It contains exactly one connection from a pilot download to `speed.cloudflare.com`, filtered from the capture to exclude other connections. The pilot session stopped after four successful downloads and a connection failure; it is not included in the five-run throughput result.

The original capture filter was `tcp port 443 and tcp portrange 55000-55099`. The submitted capture contains only the IPv4 connection 192.168.219.100:55000 to 172.66.0.218:443; the TLS SNI is speed.cloudflare.com. There are 6,381 packets over 0.2135197 s. `packet-fields.csv` preserves fields used for the analysis. There are no other application connections in this filtered file. As expected for a network capture, local addressing and interface metadata remain.

SHA-256: `f70c22b70a9229cb5be76143dda0ba03aed28449b2a5d25be53d8cf1334d603d`.

## Handshake and windows

| Packet | Direction | Flags | Raw sequence | Raw acknowledgment | Time from SYN |
|---|---|---|---:|---:|---:|
| 1 | client to server | SYN | 612231287 | 0 | 0 ms |
| 2 | server to client | SYN, ACK | 3473258583 | 612231288 | 10.6431 ms |
| 3 | client to server | ACK | 612231288 | 3473258584 | 10.6906 ms |

Each SYN consumes one sequence number. Client options are MSS 1460, window-scale shift 8 (factor 256), and SACK permitted. Server options are MSS 1360, shift 13 (factor 8192), and SACK permitted. The 65,535-byte windows in SYN packets are not scaled; scaling applies after negotiation.

Packet 3 advertises 255 x 256 = 65,280 bytes. Later, client packet 5848 advertises 8,186 x 256 = 2,095,616 bytes. Server packet 5849 has Wireshark's largest estimated outstanding data, 1,649,500 bytes (about 78.7% of that advertised window). The client's largest advertised window is 4,194,048 bytes. There are no `tcp.analysis.window_full` flags.

The analyzer flags 245 retransmissions, 205 out-of-order packets, 17 previous-segment-not-captured events and 5 spurious retransmissions (categories can overlap). These are capture-derived classifications, not a measured network packet-loss rate; host capture/offload and missing observations can affect them. Thus the capture suggests receive flow control was not the limiting factor at the cited point, but does not prove which of congestion control, loss, path capacity or server behaviour dominated the whole transfer.

## First measurement session

The validated session used five separate curl processes, HTTP/1.1 over IPv4, a fresh local port per run, and the unchanged endpoint `https://speed.cloudflare.com/__down?bytes=5000000`. HTTP errors, short payloads and connection failures are rejected. IPv4 and distinct local ports were selected after the pilot encountered a connection failure. Each successful run downloaded exactly 5,000,000 bytes, with a one-second gap between runs. Both sessions must use these same settings for comparability.

| Run | Mbps | TCP handshake (ms) | Total (s) |
|---|---:|---:|---:|
| 1 | 184.024 | 13.170 | 0.217363 |
| 2 | 198.580 | 10.595 | 0.201430 |
| 3 | 168.700 | 13.542 | 0.237107 |
| 4 | 207.264 | 10.864 | 0.192991 |
| 5 | 132.175 | 13.718 | 0.302630 |

Median 184.024 Mbps; range 132.175-207.264 Mbps; range width 75.089 Mbps; relative spread `(max-min)/median` 40.80%. Median handshake is 13.170 ms, measured as curl `time_connect - time_namelookup`. Throughput includes DNS, TCP, TLS and response-start overhead, so it is end-to-end short-transfer throughput rather than raw link capacity. The script's `ttfb_s` excludes DNS and TCP setup but includes TLS and server wait.

Scheduling, variable queueing, DNS/edge selection, retransmissions and server response time can vary between runs. In these samples the two fastest transfers also have the shorter handshakes, consistent with RTT affecting ACK-clocked growth; five observations cannot establish RTT as the sole cause. A larger RTT requires more in-flight bytes for the same throughput, and slows congestion-window growth per second during slow start.

## Required remaining session

Switch to a second authorized network and run from `w04-tcp`:

```text
python task2_measure.py --label "phone tethering" --port-base 55120
python test_tasks.py
python ../check.py w04
```

Use a truthful label. If only one network is available, the assignment permits two very different times of day, labelled as such; this only measures time variation, not a network difference. After collecting the second session, add its median, spread, median handshake time and a comparison here and in observation.md. Do not submit this partial state as complete.
