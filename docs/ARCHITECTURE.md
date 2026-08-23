# Architecture Specification: AI Affiliate Content Automation Platform (Affiliate Growth OS)
## With 10–15 Daily Clips Batch Engine & Google Flow Video Pipeline

---

## 1. System Overview & Philosophy

The **Affiliate Growth Operating System** is built for high-throughput Thai affiliate content creators who need to generate **10–15 high-converting video clips daily** for **TikTok Shop, Shopee Video, and Facebook Reels**.

To achieve this velocity without sacrificing creative quality or legal compliance, the architecture integrates a **Batch Creative Matrix Engine** and a dedicated **Google Flow / Google AI Video Provider**.

```mermaid
graph TD
    subgraph "1. Daily Product Selection (Top 2-3 Products)"
        Recs["Executive AI: 'วันนี้ทำอะไรดี?'"] --> TopProd[Top 3 High Opportunity Products]
    end

    subgraph "2. Batch Generation Matrix (10-15 Clips/Day)"
        TopProd --> Matrix[Batch Creative Matrix: 3 Products x 4-5 Angles = 12-15 Scripts]
        Matrix --> ThaiScript[Thai Natural Scripts: 15s-30s]
        ThaiScript --> Storyboards[Shot-by-Shot Storyboards & Timing Cues]
        Storyboards --> Compliance[AI Compliance & Legal Guardrails: Thai FDA/OCPB]
    end

    subgraph "3. Video Generation Engine (Google Flow & Fallbacks)"
        Compliance --> GFlow[Google Flow Video Provider / Webhook Bridge]
        GFlow --> Assets[Generated Video Clips + Thai Voiceover + Subtitles]
    end

    subgraph "4. 5-Minute Batch Approval & Publishing"
        Assets --> BatchUI[Batch Review & 1-Click Approve Studio]
        BatchUI --> Scheduler[Peak Time Auto-Scheduler: 11:30 & 19:30 BKK]
        Scheduler --> Platforms[TikTok Shop / Shopee Video / FB Reels]
    end

    subgraph "5. Continuous Learning Feedback"
        Platforms --> Perf[Performance Analytics & Attribution]
        Perf --> Winning[Winning Pattern Library & Vector Memory]
        Winning --> Recs
    end
```

---

## 2. Google Flow Video Provider & Webhook Bridge

The platform provides a dedicated `GoogleFlowVideoProvider` that seamlessly interfaces with Google Flow / Google Vertex AI / Veo / Imagen workflows.

```mermaid
sequenceDiagram
    autonumber
    participant Platform as Affiliate Growth OS Backend
    participant DB as PostgreSQL
    participant GFlow as Google Flow Workflow / Webhook
    participant Storage as Video Artifact Storage
    participant UI as Creator Studio (Next.js)

    Platform->>Platform: Generate 12-15 Thai Storyboards with Visual Prompts
    Platform->>GFlow: POST /webhook/google-flow/batch-generate {job_id, clips: [...]}
    Note over GFlow: Google Flow processes prompt nodes,<br/>image/video synthesis & text overlays
    GFlow-->>Platform: 202 Accepted (Batch Job Queued)
    
    loop Polling / Webhook Callback
        GFlow->>Platform: POST /api/v1/video/webhook/callback {job_id, clip_id, video_url, status}
        Platform->>DB: Update Video Asset Record (Status: READY_FOR_REVIEW)
        Platform-->>UI: Real-time UI notification via SSE
    end
    
    UI->>UI: Creator completes 5-Minute Batch Review & Approves
    UI->>Platform: POST /api/v1/content/batch-approve {approved_ids: [...]}
```

---

## 3. High-Level Technology Stack

| Layer | Technology Choice | Rationale |
|---|---|---|
| **Frontend UI** | **Next.js 14 (App Router) + TypeScript + TailwindCSS + Shadcn UI** | High-performance batch approval studio, real-time video player grid, Thai typography. |
| **Backend API & Orchestrator** | **FastAPI (Python 3.11+) + AsyncPG + Celery Worker** | High-concurrency async generation, event bus, and webhook callback receivers. |
| **Database & Vector Store** | **PostgreSQL 16 + pgvector** | Relational metrics, campaign tracking, and semantic search for winning Thai hooks. |
| **Video Engine Layer** | **Google Flow Provider + FFmpeg Processing Layer + Mock Provider** | Native Google Flow integration, local FFmpeg fallback for instant testing. |
| **Storage** | **S3-compatible Object Storage (MinIO / Cloudflare R2 / Google Cloud Storage)** | Secure hosting for generated video renders and audio tracks. |

---

## 4. Provider Abstraction Layer (Zero Vendor Lock-in)

```mermaid
classDiagram
    class VideoProvider {
        <<interface>>
        +generate_batch(storyboard_list) BatchJobResult
        +get_job_status(job_id) JobStatus
        +export_flow_payload(storyboard) FlowSchemaJSON
    }
    class GoogleFlowVideoProvider {
        +webhook_url: str
        +api_key: str
        +generate_batch(storyboard_list)
        +format_for_google_flow()
    }
    class FFmpegLocalProvider {
        +render_local_composition()
    }
    class MockVideoProvider {
        +generate_mock_video_preview()
    }

    VideoProvider <|-- GoogleFlowVideoProvider
    VideoProvider <|-- FFmpegLocalProvider
    VideoProvider <|-- MockVideoProvider
```
