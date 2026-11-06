# Is HTTP/3 (QUIC) faster than HTTP/2 on lossy mobile networks?

**Short answer:** Usually yes for the things users feel on poor mobile links: tail latency, stalls and rebuffering, request errors, and surviving network changes. The gain grows with loss rate and round-trip time. It is not universal. Much of it comes from faster handshakes and from congestion-control or implementation choices rather than from the protocol design alone. On high-bandwidth 5G links with weaker phones, HTTP/3 can be *slower* because of client CPU cost.

## Key findings

### 1. Mechanism: why loss hurts HTTP/2 more
- HTTP/2 multiplexes over one TCP connection, but "because the parallel nature of HTTP/2's multiplexing is not visible to TCP's loss recovery mechanisms," "a lost or reordered packet causes all active transactions to experience a stall" ([RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.html)).
- QUIC "incorporates stream multiplexing and per-stream flow control" and provides "reliability at the stream level and congestion control across the entire connection" ([RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.html)). It "does not provide any means of ensuring ordering between bytes on different streams" ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html)), so a loss on one stream does not block the others.
- Loss recovery is more precise. QUIC packet numbers are "strictly increasing within a packet number space and directly encodes transmission order", whereas "TCP conflates transmission order at the sender with delivery order at the receiver" (the cause of retransmission ambiguity). QUIC also "supports many ACK ranges, as opposed to TCP's three SACK ranges" ([RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html)).
- Handshake: "Absent packet loss, most new connections can be established and secured within a single round trip" ([RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html)). 0-RTT lets a client send data before the handshake completes ([RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html)), but it "creates an exposure to replay attack" ([RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.html)).
- Mobility: "Connection migration uses connection identifiers to allow connections to transfer to a new network path" ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html)). Only clients can migrate in QUIC v1 ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html)).

### 2. Production data (real users, mostly mobile apps)
- **Meta (Facebook app):** for video, mean time between rebuffering improved "by up to 22 percent" and "the rate of video stalls was reduced by 20 percent", "with an outsized impact on networks with relatively poorer conditions, especially those in emerging markets". For API requests over HTTP/3 vs HTTP/2, "a 6 percent reduction in request errors, a 20 percent tail latency reduction" ([Meta Engineering](https://engineering.fb.com/2020/10/21/networking-traffic/how-facebook-is-bringing-quic-to-billions/)).
- **Uber (rider and driver apps):** on networks where "most connections were lossy, causing TCP to retransmit 3.5 percent of total packets" and loss reached "as high as 7 percent" at congested sites, with "the 75th percentile of TCP back-off … almost three seconds", QUIC brought "a reduction of 10-30 percent in tail-end latencies" ([Uber](https://www.uber.com/blog/employing-quic-protocol/)).
- **Google (secondhand, via ISOC Pulse):** "an 8% average reduction" in search load time on desktop "and 3.6% on mobile"; "for the slowest 1% of Google users, it was up to 16% faster"; and "up to 20% less video stalling" ([Internet Society Pulse](https://pulse.internetsociety.org/en/blog/measuring-http-3-real-world-performance/)).
- **Akamai / Wix (via APNIC):** "about 69% of HTTP/3 connections reach a throughput of 5 Mbps or more" (vs 56% for HTTP/2) on a Latin American live stream. Wix saw "up to 33% improvements in the mean" for connection setup. APNIC also notes "most (public) comparisons … are based on lab testing" ([APNIC 2023](https://blog.apnic.net/2023/10/09/measuring-http-3-real-world-performance/)).
- **Cloudflare 2024:** "At P95, Cloudflare is 116 ms faster for connection times when HTTP/3 is enabled". This measures connection time, not page load ([Cloudflare](https://blog.cloudflare.com/network-performance-update-security-week-2024/)).

### 3. Controlled experiments under emulated loss
- Wolsing et al.: "In lossy networks, QUIC clearly outperforms the current Web stack, which we mainly attribute to its ability to progress streams independently of head-of-line blocking" ([arXiv 1906.07415](https://arxiv.org/pdf/1906.07415)). The same study warns that "tuning TCP parameters is not negligible", says the overall advantage is "mostly caused by QUIC's reduced RTT design during connection establishment", and still finds that "QUIC still outperforms even our tuned variant of TCP" ([arXiv abstract](https://arxiv.org/abs/1906.07415)).
- Liu et al. (2024): HTTP/2 and HTTP/3 were similar at low loss, but "when the packet loss reaches or exceeds 8%, H3 significantly outperforms H2". At 12% loss, "H2 required an average of 113.42 seconds" versus about 21 s for H3. During a simulated IP change "under conditions of 4% packet loss and 50ms delay, the H2 client … took an average of 56.7 seconds" (H3: 6.6 s). The caveat: "H2 with the right congestion control algorithm (CCA) can achieve performance comparable to H3" ([ar5iv 2409.16267](https://ar5iv.labs.arxiv.org/html/2409.16267); see also ["H3 excels under high-loss and high-latency conditions"](https://arxiv.org/abs/2409.16267)).
- HTTP/3 draft-27 Lighthouse study (loss up to 1.4%): "H3's aggregate score flattened out as more loss was introduced whereas TCP+TLSv1.3's curve decayed almost linearly". Yet "TCP+TLSv1.3 still performed better in a trial with 2000ms delay" ([ar5iv 2004.01978](https://ar5iv.labs.arxiv.org/html/2004.01978)).
- Real mobile networks (MONROE, Europe): "QUIC reacts better to the vagaries of channel quality experienced by mobile nodes" ([IMDEA](https://dspace.networks.imdea.org/bitstream/20.500.12761/973/1/MedNetCom2021.pdf)).

### 4. Counter-evidence and caveats
- **Implementation and congestion control matter more than the protocol design.** Yu & Benson found QUIC's "overall performance is largely determined by the server's choice of congestion-control algorithm" and is "inherently tied to implementation design choices, bugs, and configurations" ([Brown, WWW'21](https://cs.brown.edu:443/~tab/papers/QUIC_WWW21.pdf)). Throughput "varies widely between client and server implementations from 90 Mbit/s to 4900 Mbit/s" ([arXiv 2309.16395](https://arxiv.org/abs/2309.16395)).
- **Fast 5G plus a weak phone favours HTTP/2.** On fast links the HTTP/3 stack "suffers a data rate reduction of up to 45.2%". The root cause is "high receiver-side processing overhead", with "considerably higher CPU usage than HTTP/2" ([arXiv 2310.09423](https://arxiv.org/pdf/2310.09423)). "QUIC performs worse than HTTP/2 in Ethernet and 5G scenarios"; "On weaker clients such as mobile devices, the gap is even larger"; over 4G "the performance difference is not that significant", and "the impact is hidden over 4G but unleashed over 5G" ([ar5iv 2310.09423](https://ar5iv.labs.arxiv.org/html/2310.09423)). Below ~600 Mbps the two perform similarly ([arXiv 2310.09423](https://arxiv.org/pdf/2310.09423)).
- **Mobile gains are smaller than desktop gains.** "Its advantages, however, diminish across the board and at times are not statistically significant". QUIC can also be unfair to competing TCP flows, consuming "more than half of the bottleneck bandwidth" ([APNIC 2018](https://blog.apnic.net/2018/01/29/measuring-quic-vs-tcp-mobile-desktop/)).
- **YouTube:** "the legacy setup (TCP) either outperforms or performs the same as the QUIC-enabled browser for more than 60% of cases". Fallback to TCP is blind, "not distinguishing between failures caused by middleboxes and that caused by network congestion" ([arXiv 2203.11977](https://arxiv.org/pdf/2203.11977)).
- **UDP reachability:** "between 3% … and 5% … of networks block all UDP traffic", but "there is little evidence of other forms of systematic disadvantage to UDP traffic" ([RFC 9308](https://www.rfc-editor.org/rfc/rfc9308.txt)).
- **Old gQUIC results don't generalize:** a 2016 study with Chromium's toy QUIC found "Results were similar for the two transport protocols" ([KTH](https://www.kth.se/social/files/573b9e20f276545953b688f3/Performance%20testing%20TCP%20and%20QUIC.pdf)).

## Recommendations

| Situation | HTTP/3 vs HTTP/2 | Why |
|---|---|---|
| Lossy / high-RTT cellular (3G/4G, congested cells, emerging markets) | **HTTP/3 likely faster**, especially at the tail | Fewer RTTs to connect, no cross-stream HOL blocking, better loss recovery (Meta, Uber, Google, Liu et al.) |
| Users switching Wi-Fi ↔ cellular | **HTTP/3** | Connection migration avoids reconnecting (RFC 9000, Liu et al.) |
| High-bandwidth 5G / large downloads on mid-range phones | **HTTP/2 may be faster** | QUIC's receiver CPU cost (arXiv 2310.09423) |
| Networks that block UDP (~3–5%) | HTTP/2 (fallback) | RFC 9308 |

In practice: enable HTTP/3 with HTTP/2 fallback (the standard Alt-Svc setup). Choose a mature QUIC stack and a good congestion controller such as BBR. Measure p95/p99 latency and stalls on your own mobile real-user metrics rather than medians. Tune your TCP/HTTP/2 baseline before comparing, or the comparison overstates QUIC's gain.

## Trade-offs
- Most of the gain is in tail latency and stalls; median page-load gains are small (single-digit %).
- Higher CPU and battery cost on the client for UDP/QUIC processing in user space.
- 0-RTT speedups come with replay risk; restrict them to idempotent requests.
- Results depend on implementation, so a vendor's numbers may not transfer to your stack.

## Open questions
- How much of the lossy-network benefit comes from removing HOL blocking, and how much from handshake RTT and congestion control? Wolsing et al. credit HOL avoidance under loss; Yu & Benson argue congestion control dominates for real pages.
- There is little recent, independent, page-load-level data on real lossy cellular links. Most comparisons are lab-based or come from vendors.
- How do newer kernel/UDP offloads (GSO/GRO) and hardware offload change the 5G CPU-bound picture?

---
Claims checked: 75; verified 73 (69 by script + 4 confirmed manually after a fetch failure), misattributed (fixed) 0, dropped 5 (2 quotes not found in source; 3 verified but qualified/superseded by their own source page) — 70 claims kept.
