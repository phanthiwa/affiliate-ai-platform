# Technical & Operational Risk Assessment

---

## 1. Risk Matrix

| Risk ID | Category | Risk Description | Severity | Likelihood | Mitigation Strategy |
|---|---|---|---|---|---|
| **R-01** | Legal / Compliance | Generated scripts violate Thai FDA (อย.) or OCPB (สคบ.) advertising laws. | **CRITICAL** | HIGH | Implement dedicated **AI Compliance Agent** with hardcoded regex and semantic checks for banned medical/cosmetic claims; enforce human sign-off before publishing. |
| **R-02** | Platform TOS | Automated publishing triggers platform shadowbans or API suspensions (TikTok Shop / Shopee / Meta). | **HIGH** | MEDIUM | Use only official Open APIs; support controlled rate limiting, randomized publishing jitter, and OAuth2 token refresh flows. Never scrape with headless browsers in production. |
| **R-03** | AI Quality | Generated Thai scripts sound robotic, unnatural, or culturally tone-deaf. | **HIGH** | MEDIUM | Calibrate LLM system prompts with Thai colloquialisms, sentence ending particles (ค่ะ, ครับ, นะคะ, เลยแก), creator slang, and few-shot examples from viral 1M+ Thai creators. |
| **R-04** | Latency & Video Rendering | Video rendering with FFmpeg / AI generative models causes high latency and server timeouts. | **HIGH** | HIGH | Asynchronous task workers (Celery/Asyncio queue); decoupled rendering pipeline; return optimistic UI states and real-time SSE progress updates. |
| **R-05** | API Cost Escalation | High volume of video generation and multi-variant LLM calls escalates compute/API costs. | **MEDIUM** | MEDIUM | Tiered generation strategy: cheap LLMs for initial scoring/tagging; reserve heavy multimodal models for final video rendering; cache product intelligence cards. |
| **R-06** | Data Staleness | Affiliate product prices and commission rates change dynamically on e-commerce platforms. | **MEDIUM** | HIGH | Regular background cron syncs (every 6 hours); re-score products before launching creative campaigns. |

---

## 2. Regulatory & Compliance Deep-Dive (Thailand Market)

### Key Regulations:
1. **Cosmetics Act B.E. 2558 (2015)**: Strictly forbids claims of permanent alteration or instant cure without clinical trial backing.
2. **Consumer Protection Act B.E. 2522 (1979)**: Requires transparent disclosure of affiliate/sponsored links (`#สปอนเซอร์`, `#นายหน้า`, `#affiliate`) and prohibits bait-and-switch pricing.
3. **Food Act B.E. 2522 (1979)**: Dietary supplements cannot claim therapeutic or medicinal properties.

### System Safeguards:
- Pre-publish automated verification with line-by-line highlight of risky assertions.
- One-click "Apply Safe Revision" button for creators.
