# Product Requirements Document (PRD)
## Project: AI Affiliate Growth Operating System (Thailand Market)

---

## 1. Executive Summary & Market Target

### 1.1 Objective
Build an autonomous AI Affiliate Growth Operating System tailored for Thai creators on TikTok Shop, Shopee Video, and Facebook Reels. The system transforms the workflow from manual product scouting and fragmented scripting into an intelligent recommendation-driven growth loop: **Find → Analyze → Create → Test → Publish → Measure → Learn → Scale**.

### 1.2 Target User Persona
- **Primary User**: "K. Aom" - Professional Thai Affiliate Content Creator (50K - 1M+ followers / Agency running multiple creator channels).
- **Core Needs**:
  1. Discovering high-commission, low-saturation breakout products before competitors.
  2. Generating natural Thai scripts (หลีกเลี่ยงภาษาหุ่นยนต์ / ครีเอเตอร์สไตล์ธรรมชาติ) that convert viewers in the first 3 seconds.
  3. Batch-producing 5-10 controlled creative variants (Hook testing, CTA testing).
  4. Staying 100% compliant with Thai FDA (อย.) and the Office of the Consumer Protection Board (สคบ.).
  5. Knowing precisely what to do every morning to maximize GMV and affiliate payout.

---

## 2. Core Modules & Functional Specifications

### Module 1: Executive Dashboard & "What Should I Do Today?"
- **Daily Directive Panel**: AI-synthesized priority actions (e.g., *"แนะนำให้ทำวิดีโอ 3 ตัวสำหรับ 'เซรั่มใบบัวบก' วันนี้ เนื่องจากความต้องการใน Shopee พุ่งขึ้น 41% และสินค้านี้ให้ค่าคอม 25%"*).
- **KPI Summary**: Total GMV (฿), Affiliate Commission Earned (฿), Orders, Views, Blended CTR (%), Conversion Rate (%).
- **Creative Leaderboard**: Top 5 Winning Hooks, Top Creative Angles, Underperforming Creatives flagged for sunsetting.

### Module 2: Market & Product Discovery Engine
- **Multi-Source Ingestion**: Aggregation from TikTok Shop Trending, Shopee Best Sellers, and Social Buzz.
- **Configurable Opportunity Scoring Algorithm**:
  $$\text{Score} = w_1 \cdot \text{Demand} + w_2 \cdot \text{Growth} + w_3 \cdot \text{Commission} + w_4 \cdot \text{ReviewQuality} + w_5 \cdot \text{PriceAppeal} + w_6 \cdot \text{CompetitionInverse} + w_7 \cdot \text{ContentPotential} + w_8 \cdot \text{TrendMomentum}$$
- **Opportunity Classification**: `HIGH_PRIORITY` (Score $\ge 85$), `TEST` ($70-84$), `WATCH` ($50-69$), `KILL` ($< 50$).

### Module 3: Product Intelligence Agent
- **Automated Intelligence Card**:
  1. Product Summary & Pricing/Commission breakdown.
  2. Target Audience Demographics & Psychographics in Thailand.
  3. Real Customer Pain Points & Purchase Objections.
  4. Unique Selling Proposition (USP) vs Top 3 Competitors.
  5. Top 10 Recommended Content Angles & Top 5 Hook Templates.

### Module 4: Thai Script & Creative Engine
- **Duration Profiles**: 15s (Quick impulse buy), 20s (Problem-solution), 30s (Review/Demo), 45s (Storytelling), 60s (Comprehensive unboxing/comparison).
- **Style Presets**:
  - `FRIENDLY_EXPERT` (เพื่อนผู้เชี่ยวชาญแนะนำ)
  - `EXCITED_BARGAIN_HUNTER` (สายป้ายยา ดีลเด็ด ลดกระหน่ำ)
  - `AUTHENTIC_CASUAL` (รีวิวเรียลๆ ใช้เองจริง 100%)
  - `STORYTELLER` (เล่าเรื่องปัญหาส่วนตัวจนเจอทางแก้)
- **Controlled Variant Generation**:
  - Angle A: Problem $\to$ Solution
  - Angle B: Before $\to$ After
  - Angle C: Price / Value Deal
  - Angle D: "Things I wish I knew" (สิ่งที่น่าจะรู้ก่อนซื้อ)
  - Angle E: Myth vs Reality (ความเชื่อผิดๆ)

### Module 5: Storyboard & Video Factory
- **Shot-by-Shot Director**: Camera angles, duration, on-screen Thai typography (Text hooks), Voiceover timing, B-roll suggestions, and sound effects.
- **Video Assembly Pipeline**: Automated TTS (Thai natural voice), image/clip synthesis, auto-caption generation with highlight colors, background music ducking, and export via FFmpeg.

### Module 6: AI Compliance & Legal Guardrail Agent
- **Regulatory Rule Engine**:
  - Thai FDA (อย.) Health & Cosmetic claims scanner (e.g., flagging forbidden words like *"รักษาหายขาด", "ขาวทันทีใน 3 นาที", "ลดน้ำหนัก 10 กิโลใน 7 วัน"*).
  - Thai OCPB (สคบ.) pricing accuracy and mandatory affiliate disclosure (`#สปอนเซอร์`, `#นายหน้า`, `#affiliate`).
  - Misleading claims and copyright risk prevention.
- **Verdict Output**: `PASS`, `WARNING` (auto-fixed with safe alternative), `FAIL` (blocks publishing).

### Module 7: Human Approval & Video Review Studio
- **Rapid Review Interface**: Side-by-side video playback, inline subtitle/hook editor, voice changer, one-click scene regenerator, instant approve/reject/reschedule buttons.

### Module 8: Multi-Platform Publishing Center
- **Direct Dispatch**: TikTok Shop Showcase, Shopee Video, Facebook Reels.
- **Metadata Management**: Optimized Thai captions, viral hashtags, tagged product anchor links, and scheduled time slots based on Thai consumer peak activity (11:30-13:30, 19:30-22:30).

### Module 9: Performance Analytics & Attribution
- Ingestion of view completion rates, CTR, orders, GMV, and net commission.
- Multi-dimensional slicing by Hook category, Video duration, Voice actor, and Posting time.

### Module 10: AI Performance Analyst & Self-Learning Loop
- **Root-Cause Attribution**: Explain WHY a video went viral or flopped.
- **Winning Pattern Extraction**: Store winning structures into vector memory to automatically inform future generations.
- **Automated A/B Experiments**: Track multi-variant campaigns, declare statistically significant winners, and spawn 5 iterative variants of the winner.

---

## 3. Non-Functional Requirements

1. **Latency**: Script generation $< 3$ seconds, Video render preview $< 30$ seconds (mock/standard render).
2. **Localization**: Thai language UI & LLM outputs; clean Thai typography (Noto Sans Thai / Sarabun support).
3. **Availability**: 99.9% uptime target; resilient offline mock mode when external platform APIs are rate-limited.
4. **Data Isolation**: Multi-tenant workspace data boundaries and encrypted credentials.
