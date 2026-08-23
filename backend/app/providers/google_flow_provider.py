from typing import List, Dict, Any
import datetime
import uuid
from app.models.schemas import (
    ThaiScript, StoryboardShot, GoogleFlowNodePayload, GoogleFlowBatchExport
)

class GoogleFlowVideoProvider:
    def __init__(self, webhook_url: str = "https://flow.google.internal/webhook/v1/generate-clips"):
        self.webhook_url = webhook_url

    def build_node_payload(self, script: ThaiScript, shots: List[StoryboardShot]) -> GoogleFlowNodePayload:
        visual_prompts = []
        burned_captions = []

        for shot in shots:
            visual_prompts.append({
                "shot_index": shot.shot_number,
                "timing": f"{shot.start_sec:.1f}s - {shot.end_sec:.1f}s",
                "ai_prompt": shot.image_prompt_for_ai,
                "camera_movement": shot.camera_direction,
                "b_roll": shot.b_roll_suggestion
            })
            burned_captions.append({
                "start_time": shot.start_sec,
                "end_time": shot.end_sec,
                "text_th": shot.on_screen_text_th,
                "style": {
                    "font": "Prompt-Bold",
                    "font_size": 42,
                    "color": "#FFFFFF",
                    "stroke_color": "#000000",
                    "stroke_width": 3,
                    "position": "bottom_center_y_80pct"
                }
            })

        return GoogleFlowNodePayload(
            clip_id=f"GF-CLIP-{uuid.uuid4().hex[:8].upper()}",
            product_title=script.product_title_th,
            duration_sec=script.target_duration_sec,
            aspect_ratio="9:16",
            thai_voice_actor="th-TH-PremwadeeNeural (Natural Thai Female 20s)",
            voiceover_script=script.full_voiceover_th,
            visual_prompts=visual_prompts,
            burned_captions=burned_captions,
            webhook_callback_url=f"http://localhost:8000/api/v1/video/webhook/callback?clip_id={script.id}"
        )

    def export_batch_flow(self, scripts_with_shots: List[tuple[ThaiScript, List[StoryboardShot]]]) -> GoogleFlowBatchExport:
        nodes = []
        for script, shots in scripts_with_shots:
            nodes.append(self.build_node_payload(script, shots))

        return GoogleFlowBatchExport(
            batch_id=f"GF-BATCH-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}",
            generated_at=datetime.datetime.now().isoformat(),
            total_clips=len(nodes),
            target_daily_output=15,
            google_flow_nodes=nodes
        )
