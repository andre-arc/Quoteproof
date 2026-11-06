# Is HTTP/3 (QUIC) faster than HTTP/2 on lossy mobile networks?

**Short answer:** Often yes, especially in the tail and when the network is lossy or the user is moving. But the gain is smaller than the theory suggests, it depends heavily on congestion control and implementation, and it can turn negative on fast links, on weak or old phones, and when packets are reordered. Measured gains come from faster handshakes and better loss recovery more than from removing head-of-line blocking.

## Key findings

### 1. Why HTTP/3 should help under loss (mechanism)
- With HTTP/2 over TCP, "a lost or reordered packet causes all active transactions to experience a stall regardless of whether that transaction was directly impacted by the lost packet" ([RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.html)). HTTP/2's own spec says "TCP head-of-line blocking is not addressed by this protocol" ([RFC 9113](https://www.rfc-editor.org/rfc/rfc9113.html)).
- In QUIC, "only streams with data in that packet are blocked waiting for a retransmission" ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html)). Loss of a packet that carries several streams still blocks all of them ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html)).
- QUIC's loss recovery treats tail loss more gently: "QUIC does not collapse the congestion window when the PTO expires, since a single packet loss at the tail does not indicate persistent congestion" ([RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html)).
- Connection setup is cheaper. 0-RTT lets clients "send data immediately", which "requires some form of prior communication or configuration" ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html)). QUIC also "allows connections to migrate to a new network path" ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html)), which matters for mobile users.

### 2. What production operators report (mostly favourable, mostly tail)
- Google (2017): QUIC "reduces latency of Google Search responses by 8.0% for desktop users and by 3.6% for mobile users". Google warns that "mobile" here "refers to both a difference in operating environment as well as a difference in implementation" ([Google SIGCOMM 2017](https://courses.cs.washington.edu/courses/cse550/21au/papers/CSE550.quic.pdf)).
- Meta (2020): "a 20 percent tail latency reduction … relative to HTTP/2". QUIC improved video "with an outsized impact on networks with relatively poorer conditions, especially those in emerging markets" ([Meta Engineering](https://engineering.fb.com/2020/10/21/networking-traffic/how-facebook-is-bringing-quic-to-billions/)).
- Uber: "a reduction of 10-30 percent in tail-end latencies for HTTPS traffic at scale in our rider and driver apps" ([Uber](https://www.uber.com/blog/employing-quic-protocol/)).
- Cloudflare (2020) had a more mixed result. HTTP/3 was faster on a 15 KB page (443 ms vs 458 ms), but "once we increase the page size to 1MB that advantage disappears". HTTP/3 "still trails HTTP/2 performance, by about 1-4% on average in North America" ([Cloudflare](https://blog.cloudflare.com/http-3-vs-http-2/)).
- A practitioner caveat: "Getting robust performance measurements from real HTTP/3 deployments remains difficult" ([APNIC/Akamai](https://blog.apnic.net/2023/10/09/measuring-http-3-real-world-performance/)).

### 3. Controlled lab studies
- "In lossy networks, QUIC clearly outperforms the current Web stack". However, "Tuning TCP closes the gap to QUIC and shows that TCP is still very competitive to QUIC" ([Wolsing et al., ANRW 2019](https://irtf.org/anrw/2019/anrw2019-final25-acmpaginated.pdf)).
- "QUIC’s removal of HOL (head-of-line) blocking has little impact on Page Load Time and Speed Index relative to congestion control for real-world web-pages". Overall performance "is largely determined by the server’s choice of congestion-control algorithm" ([Yu & Benson, WWW 2021](https://cs.brown.edu:443/~tab/papers/QUIC_WWW21.pdf)).
- The same study found an implementation-specific reversal: "Cloudflare is the only exception to this pattern, where H3 performed much worse than H2 during 1% added loss" ([Yu & Benson](https://cs.brown.edu:443/~tab/papers/QUIC_WWW21.pdf)).
- The handshake advantage depends on transfer size: it "has a significant impact on connections whose payload is less than 1MB, but negligible impact otherwise" ([Yu & Benson](https://cs.brown.edu:443/~tab/papers/QUIC_WWW21.pdf)).

### 4. Mobile and cellular specifically, where sources disagree
- **Against:** "QUIC’s performance diminishes on mobile devices and over cellular networks". Its "improvements diminish or disappear entirely when running on mobile devices". "In the case of 3G, we see the benefits of QUIC diminish". "In presence of packet re-ordering, QUIC performs significantly worse than TCP in many scenarios" ([Kakhki et al., IMC 2017](https://www.cl.cam.ac.uk/teaching/1011/R02/papers/imc17-final39.pdf)). Reordering is common on cellular links.
- **For:** "QUIC-based operations are advantageous in case of users that move". HTTP/3 "offers a clear advantage, especially with respect to HTTP/2, due to the reduced connection establishment time" ([IMDEA 2021](https://dspace.networks.imdea.org/bitstream/20.500.12761/973/1/MedNetCom2021.pdf)).
- The two sides are not reconciled. The IMC 2017 study tested an early Google QUIC on 2013–2014 phones ("all of QUIC’s performance gains are diminished on phones from 2013 and late 2014"). Newer devices and IETF QUIC may behave differently, but no source here re-ran that test.

### 5. Costs and counter-evidence
- On fast links, "the UDP+QUIC+HTTP/3 stack suffers a data rate reduction of up to 45.2% compared to the TCP+TLS+HTTP/2 counterpart". "On weaker clients such as mobile devices, the gap is even larger". "the impact is hidden over 4G but unleashed over 5G". Average PLT was "3.0% longer than HTTP/2’s". The authors put the root cause at "high receiver-side processing overhead … QUIC’s user-space ACKs" ([Zhang et al., WWW 2024](https://arxiv.org/pdf/2310.09423)).
- Energy: "HTTP/3 frequently requires more energy than the previous versions of the protocol". In a browsing-like pattern, though, "HTTP/3 can be more energy efficient" ([arXiv 2502.19997](https://arxiv.org/html/2502.19997v1)).
- Reachability: between "3% … and 5% … of networks block all UDP traffic", and for HTTP "this fallback is TLS over TCP" ([RFC 9308](https://datatracker.ietf.org/doc/rfc9308/)).
- Over GEO satellite, page download time "doubles when using GQUIC as opposed to the performance with optimized split TCP connections" ([arXiv 1810.04970](https://arxiv.org/pdf/1810.04970.pdf)).
- A 2024 study sums up the overall picture: "While optimized H2 can match H3 in some settings, H3 is more robust overall" ([arXiv 2409.16267](https://arxiv.org/html/2409.16267v3)).

## Trade-offs at a glance

| Condition | Likely winner | Main reason | Evidence |
| :-- | :-- | :-- | :-- |
| Lossy link, default TCP stack | HTTP/3 | loss recovery and congestion control, no TCP HOL | Wolsing 2019, Meta, Uber |
| Lossy link, tuned TCP/HTTP/2 | Roughly even | the gap closes | Wolsing 2019 |
| Tail and poor-network users | HTTP/3 | 10–30% and 20% tail cuts reported | Uber, Meta |
| Users moving or new connections | HTTP/3 | fewer handshake RTTs, migration | IMDEA 2021, Yu & Benson (<1 MB) |
| Heavy packet reordering | HTTP/2 (in 2017 tests) | QUIC reordering threshold | Kakhki 2017 |
| Fast 5G or Wi-Fi, large downloads | HTTP/2 | receiver CPU overhead of QUIC | Zhang 2024 |
| Old or weak phones | HTTP/2 or even | CPU-bound userspace stack | Kakhki 2017, Zhang 2024 |
| UDP-blocking networks | HTTP/2 (fallback) | 3–5% of networks block UDP | RFC 9308 |

## Recommendations
1. **Enable HTTP/3 and keep HTTP/2 as the fallback.** Browsers and clients already race or fall back, so the downside on UDP-hostile networks is limited, and the tail-latency upside on poor networks is the most consistent finding.
2. **Measure p75–p99, not means.** The production wins are in the tail, and averages can show HTTP/3 slightly behind ([Cloudflare](https://blog.cloudflare.com/http-3-vs-http-2/)).
3. **Choose and tune congestion control first.** Two independent lab studies find it matters more than the protocol itself under loss.
4. **Watch client CPU and battery** on low-end Android and on fast 5G, where QUIC's userspace overhead can reverse the gain.

## Open questions
- No source here gives a modern, controlled HTTP/3 vs HTTP/2 comparison on real lossy LTE/5G with current IETF QUIC stacks on current phones. The main negative mobile result (IMC 2017) is from early Google QUIC.
- None of the sources quantified Wi-Fi-to-cellular handover gains from connection migration in production.
- Google's mobile figures mix network effects with app-implementation differences, as the paper itself notes.

> Checked 83 quotes: 81 verified, 0 misattributed (source corrected), 1 not found, 1 fetch failed (1 confirmed manually). Dropped 1 (1 not found, 0 unconfirmed, 0 superseded). Kept 82.
