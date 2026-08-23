import uuid
from typing import List, Dict, Any, Optional
from app.models.schemas import StoryboardShot, ComplianceStatus
from app.agents.compliance_agent import check_and_sanitize_thai_script

def analyze_and_segment_voiceover(
    product_title_th: str,
    voiceover_script: str,
    duration_sec: float = 20.0,
    style_mode: str = "AVATAR_HYBRID",
    product_thumbnail: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes Thai voiceover content, segments it into 4 high-converting shots (Hook, Demo, Proof, CTA),
    and generates photorealistic visual prompts for video generation models (Kling, Runway, Hedra, Luma).
    """
    clean_title = product_title_th.strip() if product_title_th else "สินค้าสุดคุ้ม"
    raw_script = voiceover_script.strip() if voiceover_script else f"ทุกคนคะ ตัวนี้คือ {clean_title} ที่กำลังฮิตมากๆ ในติ๊กต็อกตอนนี้ ใช้ง่ายสุดๆ แค่เปิดสวิตช์ก็ทำงานทันที ใครมีปัญหาต้องลองเลยค่ะ ตอนนี้มีโปรลดราคาพิเศษ จิ้มตะกร้าสีเหลืองซ้ายล่างได้เลยค่ะ"
    
    # Check FDA/OCPB compliance
    comp_status, sanitized_script, comp_flags = check_and_sanitize_thai_script(raw_script)
    
    # Split text into sentences / phrases
    sentences = [s.strip() for s in sanitized_script.replace("\n", " ").split(" ") if s.strip()]
    total_words = len(sentences)
    
    dur = max(10.0, float(duration_sec))
    
    # 4 Timing buckets:
    # Shot 1 (0-3.5s or 18%): The Thumb-Stopping Hook
    # Shot 2 (18% - 50%): Product Demonstration / Problem Solving
    # Shot 3 (50% - 80%): Social Proof / Key Benefit Outcome
    # Shot 4 (80% - 100%): Call to Action & Urgency
    
    t1_end = min(3.5, round(dur * 0.18, 1))
    t2_end = round(dur * 0.50, 1)
    t3_end = round(dur * 0.80, 1)
    t4_end = dur
    
    # Assign script text chunks
    w1_end = max(1, int(total_words * 0.20))
    w2_end = max(w1_end + 1, int(total_words * 0.50))
    w3_end = max(w2_end + 1, int(total_words * 0.80))
    
    chunk_hook = " ".join(sentences[:w1_end]) or f"หยุดดูคลิปนี้ก่อน! ใครยังไม่มี {clean_title} พลาดมาก"
    chunk_demo = " ".join(sentences[w1_end:w2_end]) or "สาธิตการใช้งานจริง ใช้ง่ายมาก ประหยัดเวลาไปได้เยอะ"
    chunk_proof = " ".join(sentences[w2_end:w3_end]) or "คนรีวิวเพียบ คุณภาพดีเกินราคา คุ้มค่าสุดๆ"
    chunk_cta = " ".join(sentences[w3_end:]) or "กดสั่งซื้อในตะกร้าเหลืองมุมซ้ายล่าง ตอนนี้มีโปรส่งฟรี!"

    # Realistic visual style prompts depending on style_mode
    if style_mode == "CINEMATIC_BROLL":
        prompt_1 = f"Cinematic 4k commercial shot of {clean_title}, floating product with soft studio lighting, high-end reflection, shallow depth of field, 9:16 vertical angle, photorealistic, 8k resolution, ultra detailed"
        prompt_2 = f"Extreme macro close-up shot of hands interacting with {clean_title}, natural warm morning sunlight, showing product textures and premium materials, smooth 60fps motion"
        prompt_3 = f"Aesthetic living room counter setup with {clean_title} functioning perfectly, modern cozy Thai home interior, cinematic color grading, bokeh background"
        prompt_4 = f"Hero product shot of {clean_title} center stage with sparkling light effect, neon discount badge in background, smooth camera push-in"
    elif style_mode == "UGC_VIRAL":
        prompt_1 = f"Authentic Thai creator POV holding up {clean_title} in front of smartphone camera, casual bedroom background, expressive shocked face, natural room lighting, vertical 9:16"
        prompt_2 = f"Hands-on unboxing and demonstration of {clean_title}, authentic real-world testing, showing instant satisfaction and ease of use, natural hand motion"
        prompt_3 = f"Side-by-side before and after result using {clean_title}, genuine happy reaction, high clarity mobile video aesthetic"
        prompt_4 = f"Creator smiling enthusiastically pointing down to the bottom left corner where the yellow shopping basket is, clear dynamic gesture"
    else: # AVATAR_HYBRID (Default & Most Realistic)
        prompt_1 = f"Hyper-realistic Thai influencer in modern minimal studio, speaking directly to camera while holding {clean_title}, expressive eyes and natural facial movements, 4k ultra-realistic portrait lighting, vertical 9:16"
        prompt_2 = f"Seamless cut to close-up product in-action demo of {clean_title}, clean hands operating it smoothly, bright aesthetic daylight, macro product focus"
        prompt_3 = f"Close up of satisfied Thai user smiling after using {clean_title}, showing glowing confidence and positive results, studio softbox illumination"
        prompt_4 = f"Thai creator gesturing and pointing finger down-left towards TikTok Shop yellow basket icon, cheerful warm smile, high conversion commercial style"

    shots: List[StoryboardShot] = [
        StoryboardShot(
            shot_number=1,
            start_sec=0.0,
            end_sec=t1_end,
            visual_description_th="เปิดฉากด้วย Hook ดึงดูดสายตา โชว์หน้าคนรีวิวคู่กับสินค้าแบบชัดเจน",
            image_prompt_for_ai=prompt_1,
            camera_direction="Dynamic zoom-in 1.2x to creator face",
            on_screen_text_th=chunk_hook[:35] + ("..." if len(chunk_hook) > 35 else ""),
            voiceover_th=chunk_hook,
            b_roll_suggestion="เอฟเฟกต์ซูมสั่นเบาๆ หรือสติกเกอร์ตกใจ 0.3s",
            sound_effect_cue="Whoosh + Pop SFX"
        ),
        StoryboardShot(
            shot_number=2,
            start_sec=t1_end,
            end_sec=t2_end,
            visual_description_th="สาธิตฟังก์ชันการทำงานจริง ให้เห็นว่าใช้งานง่ายและแก้ปัญหาได้ทันที",
            image_prompt_for_ai=prompt_2,
            camera_direction="Over-the-shoulder POV to hands",
            on_screen_text_th="✨ ใช้ง่าย สะดวก ไม่ยุ่งยาก",
            voiceover_th=chunk_demo,
            b_roll_suggestion="ภาพซูมจุดเด่นของวัสดุ / ปุ่มกด",
            sound_effect_cue="Satisfying Click / Mechanism SFX"
        ),
        StoryboardShot(
            shot_number=3,
            start_sec=t2_end,
            end_sec=t3_end,
            visual_description_th="แสดงผลลัพธ์และความประทับใจ พร้อมเน้นย้ำความคุ้มค่าและรีวิวผู้ใช้จริง",
            image_prompt_for_ai=prompt_3,
            camera_direction="Slow cinematic push-in",
            on_screen_text_th="⭐️ รีวิว 4.9 ดาว การันตีของแท้ 100%",
            voiceover_th=chunk_proof,
            b_roll_suggestion="ไอคอน 5 ดาว หรือกรอบคอมเมนต์รีวิว",
            sound_effect_cue="Sparkle Chime SFX"
        ),
        StoryboardShot(
            shot_number=4,
            start_sec=t3_end,
            end_sec=t4_end,
            visual_description_th="กระตุ้นการตัดสินใจซื้อ ชี้เป้าตะกร้าสีเหลืองมุมซ้ายล่างพร้อมโปรโมชั่น",
            image_prompt_for_ai=prompt_4,
            camera_direction="Static frame with animated pulsing basket pointer",
            on_screen_text_th="🛒 จิ้มตะกร้าซ้ายล่าง รับส่วนลดพิเศษ!",
            voiceover_th=chunk_cta,
            b_roll_suggestion="ลูกศรสีส้มกระพริบชี้ตำแหน่งตะกร้า TikTok / Shopee",
            sound_effect_cue="Cash Register Kaching SFX"
        )
    ]

    # Google Flow / AI Video payload structure
    google_flow_prompts = [
        {
            "shot": s.shot_number,
            "timeframe": f"{s.start_sec}s - {s.end_sec}s",
            "duration": round(s.end_sec - s.start_sec, 1),
            "image_prompt": s.image_prompt_for_ai,
            "motion_prompt": f"{s.camera_direction}, photorealistic 4k, smooth cinematic video",
            "subtitle_th": s.on_screen_text_th,
            "voice_segment": s.voiceover_th
        }
        for s in shots
    ]

    capcut_draft_payload = {
        "version": "1.0",
        "aspect_ratio": "9:16",
        "total_duration_sec": dur,
        "product_name": clean_title,
        "tracks": {
            "audio_voiceover": {
                "source": "custom_uploaded_audio",
                "duration": dur
            },
            "video_segments": [
                {
                    "shot_index": s.shot_number,
                    "start": s.start_sec,
                    "end": s.end_sec,
                    "description": s.visual_description_th,
                    "prompt": s.image_prompt_for_ai
                }
                for s in shots
            ],
            "captions": [
                {
                    "start": s.start_sec,
                    "end": s.end_sec,
                    "text": s.on_screen_text_th
                }
                for s in shots
            ]
        }
    }

    return {
        "video_id": str(uuid.uuid4()),
        "product_title_th": clean_title,
        "style_mode": style_mode,
        "duration_sec": dur,
        "sanitized_script": sanitized_script,
        "compliance_status": comp_status,
        "compliance_flags": comp_flags,
        "shots": shots,
        "google_flow_prompts": google_flow_prompts,
        "capcut_draft_payload": capcut_draft_payload,
        "summary_th": f"สร้างวิดีโอรีวิว 4 ช็อตสมจริง ความยาว {dur} วินาที พร้อมจับคู่เสียงพากย์และซับไตเติลเรียบร้อย"
    }
