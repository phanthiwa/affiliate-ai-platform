import uuid
import re
from typing import List, Dict, Any, Optional
from app.models.schemas import StoryboardShot, ComplianceStatus
from app.agents.compliance_agent import check_and_sanitize_thai_script

SAMPLE_IMAGE_ASSETS = [
  "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&auto=format&fit=crop&q=80", # skincare
  "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=800&auto=format&fit=crop&q=80", # air fryer
  "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop&q=80", # earbuds
  "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&auto=format&fit=crop&q=80", # tumbler
  "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&auto=format&fit=crop&q=80", # camera / gadget
  "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&auto=format&fit=crop&q=80", # smartwatch
]

def generate_ready_video_from_prompt(
    prompt: str,
    voice_gender: str = "female",
    style_mode: str = "AVATAR_HYBRID",
    duration_sec: int = 20
) -> Dict[str, Any]:
    """
    Deconstructs user natural language prompt into an end-to-end ready-to-post video package:
    - High-converting Thai voiceover script
    - 4-shot storyboard breakdown with timestamps
    - Photorealistic AI video prompts (4k cinematic / digital human avatar)
    - Ready-to-copy social post caption with hashtags
    """
    raw_prompt = prompt.strip()
    if not raw_prompt:
        raw_prompt = "รีวิวสินค้าขายดีใน TikTok Shop"

    # Extract keywords or product hint from prompt
    product_name = "สินค้าตัวนี้"
    if "หม้อทอด" in raw_prompt:
        product_name = "หม้อทอดไร้น้ำมัน Smart Air Fryer"
        thumb = SAMPLE_IMAGE_ASSETS[1]
    elif "เซรั่ม" in raw_prompt or "หน้าใส" in raw_prompt or "ผิว" in raw_prompt or "คอลลาเจน" in raw_prompt:
        product_name = "เซรั่มไฮยาเข้มข้น ผิวฉ่ำโกลว์"
        thumb = SAMPLE_IMAGE_ASSETS[0]
    elif "หูฟัง" in raw_prompt or "บลูทูธ" in raw_prompt or "เบส" in raw_prompt:
        product_name = "หูฟังบลูทูธไร้สาย ตัดเสียงรบกวน ANC"
        thumb = SAMPLE_IMAGE_ASSETS[2]
    elif "แก้ว" in raw_prompt or "เก็บความเย็น" in raw_prompt:
        product_name = "แก้วเก็บความเย็นสแตนเลส 316 ขนาด 900ml"
        thumb = SAMPLE_IMAGE_ASSETS[3]
    elif "นาฬิกา" in raw_prompt or "smartwatch" in raw_prompt.lower():
        product_name = "สมาร์ทวอทช์วัดสุขภาพ แบตอึด 14 วัน"
        thumb = SAMPLE_IMAGE_ASSETS[5]
    else:
        # Generic extract from prompt
        words = [w for w in raw_prompt.replace("รีวิว", "").replace("สร้างวิดีโอ", "").split(" ") if len(w) > 2]
        product_name = words[0] if words else "ไอเทมสุดฮิต"
        thumb = SAMPLE_IMAGE_ASSETS[0]

    dur = max(15, min(60, int(duration_sec)))
    
    # Generate high-converting 4-shot script
    hook_text = f"หยุดเลื่อนผ่านคลิปนี้ก่อน! ใครยังไม่มี {product_name} พลาดมากกก"
    demo_text = f"น้องตัวนี้คือใช้ง่ายสุดๆ แก้ปัญหาได้ตรงจุด ดีไซน์มินิมอล วัสดุพรีเมียมเกินราคาไปเยอะมาก"
    proof_text = f"การันตียอดขายทะลุหมื่นชิ้น รีวิว 4.9 ดาว ใครได้ลองใช้ก็ติดใจทุกคน"
    cta_text = f"ตอนนี้ใน TikTok Shop จัดโปรลดพิเศษอยู่นะคะ จิ้มที่ตะกร้าสีเหลืองมุมซ้ายล่างได้เลยค่ะ!"

    full_voiceover = f"{hook_text} {demo_text} {proof_text} {cta_text}"
    comp_status, sanitized_voiceover, comp_flags = check_and_sanitize_thai_script(full_voiceover)

    # 4 Shot timing
    t1 = round(dur * 0.18, 1)
    t2 = round(dur * 0.50, 1)
    t3 = round(dur * 0.80, 1)
    t4 = float(dur)

    # Realistic visual prompts
    if style_mode == "CINEMATIC_BROLL":
        p1 = f"Ultra-realistic 4K commercial shot of {product_name}, elegant studio soft lighting, dramatic shallow depth of field, 9:16 vertical framing, premium advertisement"
        p2 = f"Extreme macro close-up of hands touching and demonstrating {product_name}, warm natural morning light, highly detailed textures, smooth cinematic motion"
        p3 = f"Aesthetic Thai home interior showcase with {product_name} displayed prominently on wooden table, soft bokeh, magazine photography look"
        p4 = f"Hero product close up of {product_name} with gleaming light ray effect, pulsing glowing discount tag, high conversion commercial ending"
    elif style_mode == "UGC_VIRAL":
        p1 = f"Authentic POV mobile camera holding up {product_name} in cozy Thai bedroom, shocked and delighted facial expression, genuine UGC aesthetic, 9:16"
        p2 = f"Real-life unboxing and live demonstration of {product_name}, hands holding product closely to smartphone lens, authentic raw lighting"
        p3 = f"Happy Thai creator smiling genuinely holding {product_name} next to cheek, glowing natural complexion, satisfied customer review vibe"
        p4 = f"Creator pointing dynamic finger directly down-left towards TikTok yellow shopping basket sticker, enthusiastic smile"
    else: # AVATAR_HYBRID
        p1 = f"Photorealistic Thai digital creator talking to camera while holding {product_name}, studio lighting, natural blinking and facial expression, 4k vertical 9:16"
        p2 = f"Smooth cut to product in action: detailed hands-on demonstration of {product_name}, bright daylight, crisp 4k resolution"
        p3 = f"Close up of smiling Thai creator showing positive review rating card next to {product_name}, soft rim lighting, premium influencer look"
        p4 = f"Thai creator enthusiastically pointing down-left to TikTok Shop yellow basket icon with animated coupon popups"

    shots: List[StoryboardShot] = [
        StoryboardShot(
            shot_number=1,
            start_sec=0.0,
            end_sec=t1,
            visual_description_th="เปิดตัวด้วย Hook ดึงดูดสายตา โชว์หน้าคนรีวิวคู่กับสินค้าแบบชัดเจน",
            image_prompt_for_ai=p1,
            camera_direction="Dynamic zoom-in 1.2x to product",
            on_screen_text_th=hook_text,
            voiceover_th=hook_text,
            b_roll_suggestion="เอฟเฟกต์ตกใจ + ซูมเข้า",
            sound_effect_cue="Whoosh + Pop SFX"
        ),
        StoryboardShot(
            shot_number=2,
            start_sec=t1,
            end_sec=t2,
            visual_description_th="สาธิตการใช้งานจริง โชว์ความคุ้มค่าและฟังก์ชันเด่น",
            image_prompt_for_ai=p2,
            camera_direction="Over-the-shoulder POV panning",
            on_screen_text_th=demo_text,
            voiceover_th=demo_text,
            b_roll_suggestion="ภาพซูมจุดเด่นสินค้า",
            sound_effect_cue="Satisfying Click SFX"
        ),
        StoryboardShot(
            shot_number=3,
            start_sec=t2,
            end_sec=t3,
            visual_description_th="แสดงผลลัพธ์และความพึงพอใจ พร้อมรีวิว 4.9 ดาว",
            image_prompt_for_ai=p3,
            camera_direction="Slow cinematic push-in",
            on_screen_text_th=proof_text,
            voiceover_th=proof_text,
            b_roll_suggestion="ภาพดาว 5 ดาว",
            sound_effect_cue="Sparkle Ding SFX"
        ),
        StoryboardShot(
            shot_number=4,
            start_sec=t3,
            end_sec=t4,
            visual_description_th="กระตุ้นการสั่งซื้อ ชี้เป้าตะกร้าสีเหลืองมุมซ้ายล่าง",
            image_prompt_for_ai=p4,
            camera_direction="Static frame with pulsing pointer",
            on_screen_text_th=cta_text,
            voiceover_th=cta_text,
            b_roll_suggestion="ลูกศรชี้ตะกร้าเหลือง",
            sound_effect_cue="Cash Register Kaching SFX"
        )
    ]

    # Ready-to-post social caption & hashtags
    social_caption = (
        f"ของมันต้องมีจริงตัวนี้! {product_name} ใช้ง่าย คุ้มค่าเกินราคามากกก พิกัดในตะกร้าเหลืองซ้ายล่างเลยน้าา 🛒✨\n\n"
        f"#รีวิวของดี #{product_name.replace(' ', '')} #TikTokShopช้อปกันวันเงินออก #นายหน้าtiktok #ป้ายยาของใช้ในบ้าน #ของดีบอกต่อ"
    )

    return {
        "video_id": str(uuid.uuid4()),
        "user_prompt": raw_prompt,
        "product_title_th": product_name,
        "product_thumbnail": thumb,
        "style_mode": style_mode,
        "voice_gender": voice_gender,
        "duration_sec": dur,
        "full_voiceover_th": sanitized_voiceover,
        "social_caption": social_caption,
        "compliance_status": comp_status,
        "compliance_flags": comp_flags,
        "shots": shots,
        "summary_th": f"สร้างวิดีโอรีวิวสำเร็จรูปพร้อมโพสต์สำหรับ '{product_name}' ความยาว {dur} วินาที เรียบร้อยแล้ว!"
    }
