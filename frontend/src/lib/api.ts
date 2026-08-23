export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface Product {
  id: string;
  external_id: string;
  title_th: string;
  title_en?: string;
  category: string;
  brand?: string;
  original_price: number;
  sale_price: number;
  discount_pct: number;
  commission_rate: number;
  estimated_commission: number;
  total_sales: number;
  monthly_sales: number;
  daily_sales_velocity: number;
  growth_rate_7d: number;
  rating: number;
  review_count: number;
  competition_index: number;
  product_url: string;
  thumbnail_url: string;
  platform_source: string;
  tags: string[];
  demand_score: number;
  trend_score: number;
  competition_score: number;
  content_potential_score: number;
  opportunity_score: number;
  classification: 'HIGH_PRIORITY' | 'TEST' | 'WATCH' | 'KILL';
  ai_reasons: string[];
  top_recommended_angle?: string;
}

export interface ProductIntelligenceCard {
  product_id: string;
  product_summary_th: string;
  target_audience_th: string;
  customer_pain_points: { issue_th: string; emotional_trigger: string }[];
  usp_th: string[];
  reasons_to_buy: string[];
  purchase_objections: { objection_th: string; counter_argument_th: string }[];
  competitor_comparison_th: string;
  content_opportunities: string[];
  recommended_angles: string[];
  recommended_hooks: { hook_type: string; hook_text_th: string; estimated_retention_3s: number }[];
  recommended_cta_th: string;
}

export interface GeneratedClipItem {
  clip_id: string;
  product_id: string;
  product_title_th: string;
  product_thumbnail: string;
  sale_price: number;
  commission_rate: number;
  angle_type: string;
  hook_text_th: string;
  duration_sec: number;
  script: {
    id: string;
    hook_text_th: string;
    body_text_th: string;
    cta_text_th: string;
    full_voiceover_th: string;
    style_persona: string;
    storyboard_shots: {
      shot_number: number;
      start_sec: number;
      end_sec: number;
      visual_description_th: string;
      image_prompt_for_ai: string;
      camera_direction: string;
      on_screen_text_th: string;
      voiceover_th: string;
      sound_effect_cue?: string;
    }[];
  };
  compliance: {
    status: string;
    notes: string[];
  };
  google_flow_ready: boolean;
  preview_video_url: string;
  scheduled_time_slot_th: string;
  status: string;
}

export interface BatchGenerationResponse {
  batch_id: string;
  total_generated: number;
  clips: GeneratedClipItem[];
  google_flow_payload: any;
  summary_message_th: string;
}

export interface DashboardOverview {
  total_gmv_thb: number;
  total_commission_thb: number;
  total_orders: number;
  total_views: number;
  avg_ctr_pct: number;
  avg_conversion_pct: number;
  daily_clips_target: number;
  daily_clips_produced_today: number;
  top_winning_hook_th: string;
  top_performing_angle: string;
  daily_recommendations: {
    id: string;
    priority: string;
    headline_th: string;
    reasoning_th: string;
    recommended_product_id: string;
    recommended_action: string;
    estimated_daily_gmv_potential: number;
    badge_label: string;
  }[];
}

export async function fetchDashboardOverview(): Promise<DashboardOverview> {
  const res = await fetch(`${API_BASE}/dashboard/overview`);
  if (!res.ok) throw new Error('Failed to fetch dashboard overview');
  return res.json();
}

export async function fetchProducts(params?: Record<string, string>): Promise<Product[]> {
  const query = new URLSearchParams(params || {}).toString();
  const res = await fetch(`${API_BASE}/products?${query}`);
  if (!res.ok) throw new Error('Failed to fetch products');
  return res.json();
}

export async function fetchProductIntelligence(productId: string): Promise<ProductIntelligenceCard> {
  const res = await fetch(`${API_BASE}/products/${productId}/intelligence`);
  if (!res.ok) throw new Error('Failed to fetch product intelligence');
  return res.json();
}

export async function triggerDailyBatchClips(productIds?: string[]): Promise<BatchGenerationResponse> {
  const res = await fetch(`${API_BASE}/batch/generate-15-clips`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      product_ids: productIds,
      target_clip_count: 15,
      preferred_durations: [15, 20, 30]
    })
  });
  if (!res.ok) throw new Error('Failed to generate batch clips');
  return res.json();
}

export async function batchApproveClips(clipIds: string[]) {
  const res = await fetch(`${API_BASE}/content/batch-approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(clipIds)
  });
  if (!res.ok) throw new Error('Failed to batch approve clips');
  return res.json();
}

export interface VoiceoverGenerationRequest {
  product_title_th: string;
  voiceover_script?: string;
  duration_sec?: number;
  style_mode?: string;
  product_thumbnail?: string;
}

export interface VoiceoverGenerationResponse {
  video_id: string;
  product_title_th: string;
  style_mode: string;
  duration_sec: number;
  sanitized_script: string;
  compliance_status: string;
  compliance_flags: string[];
  shots: {
    shot_number: number;
    start_sec: number;
    end_sec: number;
    visual_description_th: string;
    image_prompt_for_ai: string;
    camera_direction: string;
    on_screen_text_th: string;
    voiceover_th: string;
    b_roll_suggestion: string;
    sound_effect_cue?: string;
  }[];
  google_flow_prompts: {
    shot: number;
    timeframe: string;
    duration: number;
    image_prompt: string;
    motion_prompt: string;
    subtitle_th: string;
    voice_segment: string;
  }[];
  capcut_draft_payload: any;
  summary_th: string;
}

export async function generateVideoFromVoiceover(payload: VoiceoverGenerationRequest): Promise<VoiceoverGenerationResponse> {
  const res = await fetch(`${API_BASE}/video/generate-from-voiceover`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to generate video from voiceover');
  return res.json();
}

export interface PromptToVideoRequest {
  prompt: string;
  voice_gender?: string;
  style_mode?: string;
  duration_sec?: number;
}

export interface PromptToVideoResponse {
  video_id: string;
  user_prompt: string;
  product_title_th: string;
  product_thumbnail: string;
  style_mode: string;
  voice_gender: string;
  duration_sec: number;
  full_voiceover_th: string;
  social_caption: string;
  compliance_status: string;
  compliance_flags: string[];
  shots: {
    shot_number: number;
    start_sec: number;
    end_sec: number;
    visual_description_th: string;
    image_prompt_for_ai: string;
    camera_direction: string;
    on_screen_text_th: string;
    voiceover_th: string;
    b_roll_suggestion: string;
    sound_effect_cue?: string;
  }[];
  summary_th: string;
}

export async function generateVideoFromPrompt(payload: PromptToVideoRequest): Promise<PromptToVideoResponse> {
  const res = await fetch(`${API_BASE}/video/prompt-to-video`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to generate video from prompt');
  return res.json();
}

export interface FlowOmniStoryboardRequest {
  product_id?: string;
  product_title_th?: string;
  product_thumbnail?: string;
  category?: string;
  usp_th?: string[];
}

export interface FlowOmniStoryboardResponse {
  video_id: string;
  product_title_th: string;
  product_thumbnail: string;
  category: string;
  style_mode: string;
  total_duration_sec: number;
  shots_count: number;
  shots: {
    shot_number: number;
    start_sec: number;
    end_sec: number;
    visual_description_th: string;
    image_prompt_for_ai: string;
    camera_direction: string;
    on_screen_text_th: string;
    voiceover_th: string;
    b_roll_suggestion: string;
    sound_effect_cue?: string;
  }[];
  universal_flow_omni_prompt: string;
  full_voiceover_th: string;
  compliance_status: string;
  compliance_flags: string[];
  summary_th: string;
}

export async function generateFlowOmniStoryboard(payload: FlowOmniStoryboardRequest): Promise<FlowOmniStoryboardResponse> {
  const res = await fetch(`${API_BASE}/video/flow-omni-storyboard`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to generate Flow Omni storyboard');
  return res.json();
}
