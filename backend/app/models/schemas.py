from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid
from datetime import datetime

class PlatformEnum(str, Enum):
    TIKTOK_SHOP = "TIKTOK_SHOP"
    SHOPEE_VIDEO = "SHOPEE_VIDEO"
    FB_REELS = "FB_REELS"

class OpportunityClassification(str, Enum):
    HIGH_PRIORITY = "HIGH_PRIORITY"
    TEST = "TEST"
    WATCH = "WATCH"
    KILL = "KILL"

class ComplianceStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"

class VideoStatus(str, Enum):
    DRAFT = "DRAFT"
    GENERATING = "GENERATING"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    PUBLISHED = "PUBLISHED"
    WINNER = "WINNER"
    UNDERPERFORMING = "UNDERPERFORMING"
    ARCHIVED = "ARCHIVED"

# --- SCORING WEIGHTS ---
class ScoringWeights(BaseModel):
    demand: float = 0.25
    growth: float = 0.15
    commission: float = 0.15
    review_quality: float = 0.10
    price_attractiveness: float = 0.10
    competition: float = 0.10
    content_potential: float = 0.10
    trend_momentum: float = 0.05

# --- PRODUCT SCHEMAS ---
class ProductBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    external_id: str
    title_th: str
    title_en: Optional[str] = None
    category: str
    brand: Optional[str] = None
    original_price: float
    sale_price: float
    discount_pct: float
    commission_rate: float  # e.g., 20.0 for 20%
    estimated_commission: float
    total_sales: int
    monthly_sales: int
    daily_sales_velocity: int
    growth_rate_7d: float
    rating: float
    review_count: int
    competition_index: float  # 0 to 100 (lower is better/less saturated)
    product_url: str
    thumbnail_url: str
    platform_source: PlatformEnum
    tags: List[str] = []

class ProductWithScores(ProductBase):
    demand_score: float
    trend_score: float
    competition_score: float
    content_potential_score: float
    opportunity_score: float
    classification: OpportunityClassification
    ai_reasons: List[str] = []
    top_recommended_angle: Optional[str] = None

# --- PRODUCT INTELLIGENCE CARD (11 Sections) ---
class PainPoint(BaseModel):
    issue_th: str
    emotional_trigger: str

class Objection(BaseModel):
    objection_th: str
    counter_argument_th: str

class HookTemplate(BaseModel):
    hook_type: str
    hook_text_th: str
    estimated_retention_3s: float

class ProductIntelligenceCard(BaseModel):
    product_id: str
    product_summary_th: str
    target_audience_th: str
    customer_pain_points: List[PainPoint]
    usp_th: List[str]
    reasons_to_buy: List[str]
    purchase_objections: List[Objection]
    competitor_comparison_th: str
    content_opportunities: List[str]
    recommended_angles: List[str]
    recommended_hooks: List[HookTemplate]
    recommended_cta_th: str

# --- SCRIPT & STORYBOARD SCHEMAS ---
class StoryboardShot(BaseModel):
    shot_number: int
    start_sec: float
    end_sec: float
    visual_description_th: str
    image_prompt_for_ai: str
    camera_direction: str  # e.g. "Close-up zoom in", "POV over-the-shoulder"
    on_screen_text_th: str
    voiceover_th: str
    b_roll_suggestion: str
    sound_effect_cue: Optional[str] = None

class ThaiScript(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    product_title_th: str
    angle_type: str
    target_duration_sec: int  # 15, 20, 30, 45, 60
    style_persona: str
    hook_text_th: str
    body_text_th: str
    cta_text_th: str
    full_voiceover_th: str
    word_count: int
    compliance_status: ComplianceStatus = ComplianceStatus.PASS
    compliance_notes: List[str] = []
    storyboard_shots: List[StoryboardShot] = []

# --- GOOGLE FLOW SPECIFIC SCHEMAS ---
class GoogleFlowNodePayload(BaseModel):
    clip_id: str
    product_title: str
    duration_sec: int
    aspect_ratio: str = "9:16"
    thai_voice_actor: str = "th-TH-PremwadeeNeural"
    voiceover_script: str
    visual_prompts: List[Dict[str, Any]]
    burned_captions: List[Dict[str, Any]]
    webhook_callback_url: Optional[str] = None

class GoogleFlowBatchExport(BaseModel):
    batch_id: str
    generated_at: str
    total_clips: int
    target_daily_output: int = 15
    google_flow_nodes: List[GoogleFlowNodePayload]

# --- BATCH GENERATION SCHEMAS ---
class BatchGenerationRequest(BaseModel):
    product_ids: Optional[List[str]] = None
    target_clip_count: int = 15
    preferred_durations: List[int] = [15, 20, 30]
    platforms: List[PlatformEnum] = [PlatformEnum.TIKTOK_SHOP, PlatformEnum.SHOPEE_VIDEO, PlatformEnum.FB_REELS]

class GeneratedClipItem(BaseModel):
    clip_id: str
    product_id: str
    product_title_th: str
    product_thumbnail: str
    sale_price: float
    commission_rate: float
    angle_type: str
    hook_text_th: str
    duration_sec: int
    script: ThaiScript
    compliance: Dict[str, Any]
    google_flow_ready: bool = True
    preview_video_url: str
    scheduled_time_slot_th: str
    status: VideoStatus = VideoStatus.READY_FOR_REVIEW

class BatchGenerationResponse(BaseModel):
    batch_id: str
    total_generated: int
    clips: List[GeneratedClipItem]
    google_flow_payload: GoogleFlowBatchExport
    summary_message_th: str

# --- DASHBOARD & RECOMMENDATION SCHEMAS ---
class DailyAIActionRecommendation(BaseModel):
    id: str
    priority: str
    headline_th: str
    reasoning_th: str
    recommended_product_id: str
    recommended_action: str
    estimated_daily_gmv_potential: float
    badge_label: str

class DashboardOverviewMetrics(BaseModel):
    total_gmv_thb: float
    total_commission_thb: float
    total_orders: int
    total_views: int
    avg_ctr_pct: float
    avg_conversion_pct: float
    daily_clips_target: int = 15
    daily_clips_produced_today: int
    top_winning_hook_th: str
    top_performing_angle: str
    daily_recommendations: List[DailyAIActionRecommendation]

# --- VOICEOVER TO REALISTIC VIDEO STUDIO SCHEMAS ---
class VoiceoverGenerationRequest(BaseModel):
    product_title_th: str
    voiceover_script: Optional[str] = None
    duration_sec: float = 20.0
    style_mode: str = "AVATAR_HYBRID"  # AVATAR_HYBRID, CINEMATIC_BROLL, UGC_VIRAL
    product_thumbnail: Optional[str] = None

class VoiceoverGenerationResponse(BaseModel):
    video_id: str
    product_title_th: str
    style_mode: str
    duration_sec: float
    sanitized_script: str
    compliance_status: str
    compliance_flags: List[str] = []
    shots: List[StoryboardShot]
    google_flow_prompts: List[Dict[str, Any]]
    capcut_draft_payload: Dict[str, Any]
    summary_th: str

# --- PROMPT TO READY VIDEO ENGINE (GOOGLE FLOW STYLE) SCHEMAS ---
class PromptToVideoRequest(BaseModel):
    prompt: str
    voice_gender: str = "female"  # female, male
    style_mode: str = "AVATAR_HYBRID"  # AVATAR_HYBRID, CINEMATIC_BROLL, UGC_VIRAL
    duration_sec: int = 20

class PromptToVideoResponse(BaseModel):
    video_id: str
    user_prompt: str
    product_title_th: str
    product_thumbnail: str
    style_mode: str
    voice_gender: str
    duration_sec: int
    full_voiceover_th: str
    social_caption: str
    compliance_status: str
    compliance_flags: List[str] = []
    shots: List[StoryboardShot]
    summary_th: str
