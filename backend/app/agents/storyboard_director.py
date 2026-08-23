from typing import List
from app.models.schemas import ThaiScript, StoryboardShot

def convert_script_to_storyboard(script: ThaiScript) -> List[StoryboardShot]:
    shots: List[StoryboardShot] = []
    dur = script.target_duration_sec

    # Shot 1: The 0-3s Hook (Crucial for thumb-stopping virality)
    shots.append(StoryboardShot(
        shot_number=1,
        start_sec=0.0,
        end_sec=min(3.0, dur * 0.15),
        visual_description_th="โคลสอัพหน้าครีเอเตอร์ทำหน้าตกใจ/แสดงปัญหา พร้อมชูสินค้าให้เห็นทันที",
        image_prompt_for_ai=f"Thai creator holding {script.product_title_th}, dynamic expressive facial reaction, clean studio lighting, high resolution, 9:16 vertical video style",
        camera_direction="Fast zoom-in to product",
        on_screen_text_th=script.hook_text_th[:40] + ("..." if len(script.hook_text_th) > 40 else ""),
        voiceover_th=script.hook_text_th,
        b_roll_suggestion="ตัดภาพปัญหาหน้าจอหรือภาพเปรียบเทียบ 0.5 วินาที",
        sound_effect_cue="Whoosh SFX + Pop Sound"
    ))

    # Shot 2: Demonstration & Problem Empathy
    shots.append(StoryboardShot(
        shot_number=2,
        start_sec=3.0,
        end_sec=dur * 0.45,
        visual_description_th="สาธิตการหยิบใช้งานจริง โฟกัสฟังก์ชันเด่นของสินค้าให้เห็นชัดเจน",
        image_prompt_for_ai=f"Close-up hands using {script.product_title_th}, realistic Thai home background, bright aesthetic daylight, macro product shot",
        camera_direction="Over-the-shoulder POV panning",
        on_screen_text_th="🌟 แก้ปัญหาได้ตรงจุด / ใช้ง่ายมาก",
        voiceover_th=script.body_text_th[:len(script.body_text_th)//2],
        b_roll_suggestion="ภาพซูมเนื้อสัมผัส หรือปุ่มเปิดทำงาน",
        sound_effect_cue="Subtle upbeat rhythmic music"
    ))

    # Shot 3: Key Benefit & Social Proof
    shots.append(StoryboardShot(
        shot_number=3,
        start_sec=dur * 0.45,
        end_sec=dur * 0.80,
        visual_description_th="แสดงผลลัพธ์หลังใช้งาน (ผิวดูดีขึ้น / คลายปวดเมื่อย / ใช้งานเสร็จเรียบร้อย)",
        image_prompt_for_ai=f"Happy Thai woman smiling with glowing natural look, holding {script.product_title_th}, satisfying outcome",
        camera_direction="Smooth slow-motion push in",
        on_screen_text_th="✅ รีวิว 4.9 ดาว การันตีของแท้",
        voiceover_th=script.body_text_th[len(script.body_text_th)//2:],
        b_roll_suggestion="ภาพแชทรีวิวจากผู้ใช้จริง หรือคอมเมนต์ลูกค้า",
        sound_effect_cue="Ding / Sparkle SFX"
    ))

    # Shot 4: High-Conversion Call to Action (CTA)
    shots.append(StoryboardShot(
        shot_number=4,
        start_sec=dur * 0.80,
        end_sec=float(dur),
        visual_description_th="ชี้มือไปที่มุมซ้ายล่าง พร้อมลูกศรชี้ไปยังตะกร้าสินค้าสีเหลือง",
        image_prompt_for_ai="Animated finger pointing down left to TikTok shop yellow basket icon, flashing discount coupon banner",
        camera_direction="Static frame with animated pulsing CTA sticker",
        on_screen_text_th="👇 จิ้มตะกร้าซ้ายล่าง รับโค้ดส่งฟรี!",
        voiceover_th=script.cta_text_th,
        b_roll_suggestion="ภาพกดคูปองส่วนลดในแอปพลิเคชัน",
        sound_effect_cue="Cash register chime SFX"
    ))

    return shots
