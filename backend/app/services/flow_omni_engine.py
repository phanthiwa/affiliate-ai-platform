import uuid
from typing import List, Dict, Any, Optional
from app.models.schemas import StoryboardShot, ComplianceStatus
from app.agents.compliance_agent import check_and_sanitize_thai_script
from app.data.thai_products_mock import SAMPLE_THAI_PRODUCTS

def generate_flow_omni_storyboard(
    product_id: Optional[str] = None,
    product_title_th: Optional[str] = None,
    product_thumbnail: Optional[str] = None,
    category: Optional[str] = None,
    usp_th: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Generates a 10-second 5-scene POV Storyboard in 'Bright Premium Lifestyle' style
    and a ready-to-copy Universal Prompt tailored for Flow Omni (Omni Flash 10s model).
    
    Rules:
    - Exactly 10 seconds total (5 scenes x 2 seconds each)
    - No human characters / faces, first-person POV hands only
    - Automatically selected fitting luxury props (white marble, dewy leaves, morning sunbeams, stone pedestal)
    - Ends with a cinematic Hero Shot
    - Includes 10s natural Thai friend-to-friend voiceover, SFX, light BGM, and short cute Thai text
    """
    # If product_id is provided, auto-pull data from winning products catalog
    target_product = None
    if product_id:
        target_product = next((p for p in SAMPLE_THAI_PRODUCTS if p.id == product_id), None)
    
    if target_product:
        title = target_product.title_th
        thumb = target_product.thumbnail_url
        cat = target_product.category
        usps = target_product.tags
    else:
        title = product_title_th.strip() if product_title_th else "เซรั่มไฮยาลูรอนเข้มข้น ผิวฉ่ำโกลว์"
        thumb = product_thumbnail or "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&auto=format&fit=crop&q=80"
        cat = category or "สกินแคร์ / ความงาม"
        usps = usp_th or ["ผิวฉ่ำวาว", "ซึมไว 3 วิ", "สารสกัดพรีเมียม"]

    clean_short_title = title.split(" ")[0] if title else "สินค้านี้"

    # Auto-select Bright Premium Lifestyle Props & Action Choreography based on product category
    if "หม้อทอด" in title or "ครัว" in cat:
        prop_surface = "เคาน์เตอร์ครัวหินอ่อนสีขาวและกระจกใส แสงแดดเช้าส่องสะท้อนอบอุ่น"
        hand_action_1 = "มือ POV เอื้อมหยิบจับด้ามจับหม้อทอดสีมินิมอลอย่างนุ่มนวล"
        hand_action_2 = "มือ POV ดึงลิ้นชักหม้อทอดออกอย่างลื่นไหล เผยถาดอบเคลือบเทฟลอนเงางาม"
        hand_action_3 = "กล้อง Macro ซูมมือวางอาหารลงในตะแกรง เสียงดังกรอบน่าทาน"
        hand_action_4 = "มือ POV วางจานอาหารสีขาวเคียงข้างหม้อทอดและใบโรสแมรี่สด"
        hand_action_5 = "Hero Shot หม้อทอดไร้น้ำมันตั้งตระหง่านกลางแท่นหินสีเบจ แสงแดดยามเช้าเรืองรอง"
        sfx_1, sfx_2, sfx_3, sfx_4, sfx_5 = "Soft whoosh", "Smooth drawer click", "Crispy sizzle chime", "Delicate plate tap", "Sparkle chime"
        on_text_1, on_text_2, on_text_3, on_text_4, on_text_5 = "ทอดกรอบ ไร้น้ำมัน!", "จุเยอะ 5.5 ลิตร", "ล้างง่าย ไม่ติดกระทะ", "ประหยัดเวลามากก", "จิ้มตะกร้าซ้ายล่างเลย!"
        vo_script = f"ทุกคน หม้อทอดตัวนี้คือที่สุด! จุเยอะ 5.5 ลิตร ทอดกรอบไม่อมน้ำมัน ล้างง่ายสุดๆ จิ้มตะกร้าเหลืองเลยน้า"
        english_item = f"minimalist smart air fryer with premium matte finish"
    elif "หูฟัง" in title or "อิเล็กทรอนิกส์" in cat or "ไอที" in cat:
        prop_surface = "โต๊ะทำงานไม้โอ๊คสีมินิมอลคลีนตา แสงแดดอบอุ่นส่องผ่านมู่ลี่"
        hand_action_1 = "มือ POV เอื้อมหยิบเคสกล่องชาร์จหูฟังทรงกลมมนสวยงามขึ้นมา"
        hand_action_2 = "มือ POV ดีดเปิดฝาเคสหูฟังแบบแม่เหล็กเบาๆ ไฟสถานะ LED สว่างวาบ"
        hand_action_3 = "กล้อง Macro โคลสอัพมือหยิบก้านหูฟังขึ้นมา โชว์ดีไซน์พรีเมียมโค้งมน"
        hand_action_4 = "มือ POV วางเคสหูฟังข้างสมุดโน้ตและแก้วกาแฟมินิมอลอย่างลงตัว"
        hand_action_5 = "Hero Shot หูฟังไร้สายและเคสเปล่งประกายกลางแท่นหินอ่อน แสงสะท้อนสีทองนวล"
        sfx_1, sfx_2, sfx_3, sfx_4, sfx_5 = "Gentle pick-up whoosh", "Crisp magnetic snap", "Subtle power chime", "Gentle desk tap", "Tech shimmer SFX"
        on_text_1, on_text_2, on_text_3, on_text_4, on_text_5 = "เบสแน่น ตัดเสียงกริบ!", "เปิดปุ๊บ ต่อปั๊บ", "แบตอึด 40 ชม.", "ดีไซน์สวย มินิมอล", "กดสั่งในตะกร้าเลย!"
        vo_script = f"หูฟังไร้สายตัวนี้เสียงดีเกินราคามาก! ตัดเสียงรบกวนเงียบกริบ แบตอึด 40 ชม. สั่งในตะกร้าเหลืองได้เลย"
        english_item = f"sleek wireless ANC earbuds with charging case"
    elif "แก้ว" in title or "ของใช้" in cat:
        prop_surface = "โต๊ะไม้สไตล์มินิมอลเคียงข้างหน้าต่าง แสงแดดยามเช้าประกายระยิบระยับ"
        hand_action_1 = "มือ POV เอื้อมไปจับด้ามแก้วสแตนเลสสีพาสเทลขึ้นมาอย่างมั่นคง"
        hand_action_2 = "มือ POV หมุนเปิดฝาแก้วอย่างนุ่มนวล โชว์ช่องใส่หลอดและยางกันรั่ว"
        hand_action_3 = "กล้อง Macro มือเทน้ำแข็งและน้ำผลไม้ใสลงในแก้ว ไอน้ำเย็นสดชื่น"
        hand_action_4 = "มือ POV วางแก้วลงข้างผลส้มสดและใบไม้สีเขียวสะอาดตา"
        hand_action_5 = "Hero Shot แก้วเก็บความเย็นตั้งสง่างามกลางแท่นหินทราเวอร์ทีน ละอองแสงทองส่องสว่าง"
        sfx_1, sfx_2, sfx_3, sfx_4, sfx_5 = "Solid cup pick-up", "Smooth lid twist", "Ice cubes clinking + water pour", "Solid base placement tap", "Sparkle chime"
        on_text_1, on_text_2, on_text_3, on_text_4, on_text_5 = "เก็บเย็นข้ามวัน!", "สแตนเลส 316 แท้", "ไม่เป็นไอน้ำเกาะ", "ขนาดใหญ่ 900ml", "จิ้มตะกร้าซ้ายล่าง!"
        vo_script = f"แก้วเก็บความเย็นตัวโปรด! ใส่น้ำแข็งข้ามวันไม่ละลาย สแตนเลส 316 แท้ จิ้มตะกร้าเหลืองซ้ายล่างเลยน้า"
        english_item = f"aesthetic pastel stainless steel 900ml thermal tumbler"
    else: # Default: Skincare / Beauty (Premium Glass Serum Bottle)
        prop_surface = "เคาน์เตอร์หินอ่อนสีขาวนวล ประกายแสงแดดเช้าส่องสะท้อนหรูหรา"
        hand_action_1 = "มือผู้หญิงเรียวสวย POV เอื้อมไปหยิบขวดเซรั่มแก้วขึ้นมาจากเคาน์เตอร์"
        hand_action_2 = "มือ POV หมุนคลายเกลียวฝาดรอปเปอร์อย่างนุ่มนวล ยกหลอดแก้วใสขึ้น"
        hand_action_3 = "กล้อง Macro ปลายดรอปเปอร์หยดเนื้อเซรั่มใส 1 หยดลงบนหลังมืออย่างนุ่มนวล"
        hand_action_4 = "มือ POV วางขวดเซรั่มลงข้างใบไม้สีเขียวสดและหยดน้ำใสบริสุทธิ์"
        hand_action_5 = "Hero Shot ขวดเซรั่มแก้วเปล่งประกายกลางแท่นหินอ่อนสีเบจ ลำแสงสีทองเรืองรอง"
        sfx_1, sfx_2, sfx_3, sfx_4, sfx_5 = "Gentle glass pick-up chime", "Tactile cap twist & pop", "Crisp water drop ripple", "Delicate glass placement tap", "Sparkle ding chime"
        on_text_1, on_text_2, on_text_3, on_text_4, on_text_5 = "ผิวฉ่ำโกลว์ใน 3 วัน!", "เนื้อใส ซึมไวมาก", "หยดเดียว เติมน้ำให้ผิว", "สารสกัดพรีเมียม", "กดสั่งในตะกร้าเลย!"
        vo_script = f"ทุกคน ตัวนี้ใช้ดีมาก ผิวฉ่ำโกลว์ใสขึ้นจริง เนื้อบางเบา ซึมไว ไม่เหนอะหนะ จิ้มตะกร้าซ้ายล่างได้เลยน้า!"
        english_item = f"luxury aesthetic glass serum bottle with dropper"

    comp_status, sanitized_vo, comp_flags = check_and_sanitize_thai_script(vo_script)

    # Build 5 Storyboard Shots (2.0s each)
    shots: List[StoryboardShot] = [
        StoryboardShot(
            shot_number=1,
            start_sec=0.0,
            end_sec=2.0,
            visual_description_th=f"ฉากเปิด: {hand_action_1} บน {prop_surface}",
            image_prompt_for_ai=f"Scene 1 (0-2s): POV high-angle view with slow smooth push-in. Well-manicured hand picks up {english_item} from sunlit white marble vanity, warm morning sunbeam flare, Bright Premium Lifestyle, 4k",
            camera_direction="POV High-Angle with Slow Push-in",
            on_screen_text_th=on_text_1,
            voiceover_th=sanitized_vo[:len(sanitized_vo)//4],
            b_roll_suggestion="ประกายแสงสะท้อนเลนส์ (Lens flare) นุ่มนวล",
            sound_effect_cue=sfx_1
        ),
        StoryboardShot(
            shot_number=2,
            start_sec=2.0,
            end_sec=4.0,
            visual_description_th=f"ฉากสำรวจ: {hand_action_2}",
            image_prompt_for_ai=f"Scene 2 (2-4s): Seamless cut to 45-degree close-up with soft rotational movement. POV hand gently opens and inspects {english_item}, crisp product textures, 4k",
            camera_direction="Close-up 45-degree with Smooth Orbit",
            on_screen_text_th=on_text_2,
            voiceover_th=sanitized_vo[len(sanitized_vo)//4:len(sanitized_vo)//2],
            b_roll_suggestion="แสงตกกระทบผิวสัมผัสวัสดุ",
            sound_effect_cue=sfx_2
        ),
        StoryboardShot(
            shot_number=3,
            start_sec=4.0,
            end_sec=6.0,
            visual_description_th=f"ฉากสาธิต: {hand_action_3}",
            image_prompt_for_ai=f"Scene 3 (4-6s): Extreme macro slow-motion focus. POV hand demonstrating active usage of {english_item}, satisfying tactile feedback, soft bokeh background, 4k",
            camera_direction="Extreme Macro with Subtle Slow-Motion",
            on_screen_text_th=on_text_3,
            voiceover_th=sanitized_vo[len(sanitized_vo)//2:len(sanitized_vo)*3//4],
            b_roll_suggestion="ภาพหยดน้ำ / การทำงานแบบสโลว์โมชัน",
            sound_effect_cue=sfx_3
        ),
        StoryboardShot(
            shot_number=4,
            start_sec=6.0,
            end_sec=8.0,
            visual_description_th=f"ฉากวางเคียงคู่พร็อพ: {hand_action_4}",
            image_prompt_for_ai=f"Scene 4 (6-8s): Smooth cut to medium POV panning shot. POV hand gracefully sets down {english_item} next to fresh botanical green leaves and water drops on sunlit table, 4k",
            camera_direction="Medium POV Shot with Dutch Tilt Pan",
            on_screen_text_th=on_text_4,
            voiceover_th=sanitized_vo[len(sanitized_vo)*3//4:],
            b_roll_suggestion="ใบไม้สีเขียวสดและหยดน้ำสะท้อนแสงแดด",
            sound_effect_cue=sfx_4
        ),
        StoryboardShot(
            shot_number=5,
            start_sec=8.0,
            end_sec=10.0,
            visual_description_th=f"ฉากจบ: {hand_action_5}",
            image_prompt_for_ai=f"Scene 5 (8-10s): Final Hero Shot. Cinematic slow orbit zoom-out centering {english_item} on luxury travertine stone pedestal bathed in brilliant warm morning sunbeams, 4k",
            camera_direction="Hero Shot with Cinematic Orbit & Zoom-Out",
            on_screen_text_th=on_text_5,
            voiceover_th="จิ้มตะกร้าเหลืองซ้ายล่างได้เลยน้า!",
            b_roll_suggestion="ละอองแสงทองส่องสว่างเรืองรอง",
            sound_effect_cue=sfx_5
        )
    ]

    # Universal Flow Omni Prompt formatted for 1-Click Copy
    universal_flow_omni_prompt = f"""Create a hyper-realistic 10-second vertical 9:16 commercial video strictly following the 5-panel reference storyboard image. Bright Premium Lifestyle aesthetic, clean morning sunlight with soft warm flares, pastel white marble and light beige minimal interior, 4K commercial color grading, 60fps ultra-smooth motion. The physical appearance and branding of {english_item} must remain 100% consistent across all 5 scenes without morphing. No human face visible throughout the entire clip, only a gentle well-manicured hand in first-person POV perspective.

[SCENE BREAKDOWN & CAMERA CHOREOGRAPHY]
- Scene 1 (0.0s - 2.0s): POV high-angle view with slow smooth push-in. Hand smoothly picks up {english_item} from sunlit white marble vanity with subtle lens flare.
  • On-Screen Text: "{on_text_1}" (clean aesthetic modern Thai font, centered-top, cute minimal drop shadow, yellow-white tint).
  • Sound Effect: {sfx_1}.

- Scene 2 (2.0s - 4.0s): Seamless transition to 45-degree close-up with soft rotational camera movement. POV hand gently interacts with and inspects {english_item}.
  • On-Screen Text: "{on_text_2}" (cute Thai subtitle below frame).
  • Sound Effect: {sfx_2}.

- Scene 3 (4.0s - 6.0s): Extreme macro slow-motion focus. POV hand demonstrates active feature in-use with satisfying tactile feedback and soft bokeh.
  • On-Screen Text: "{on_text_3}" (gentle floating text).
  • Sound Effect: {sfx_3}.

- Scene 4 (6.0s - 8.0s): Smooth cut to medium POV panning shot. POV hand gracefully places {english_item} down next to fresh dewy botanical green leaves and water droplets.
  • On-Screen Text: "{on_text_4}" (minimal badge text).
  • Sound Effect: {sfx_4}.

- Scene 5 (8.0s - 10.0s): Final Hero Shot. Cinematic slow orbit zoom-out centering {english_item} on a luxury travertine stone pedestal bathed in brilliant warm morning sunbeams with sparkling dust particles.
  • On-Screen Text: "{on_text_5}" (pulsing cute Thai CTA sticker with yellow shopping basket icon).
  • Sound Effect: {sfx_5}.

[AUDIO & VOICEOVER]
• Background Music (BGM): Upbeat, light, acoustic-pop lo-fi piano and subtle acoustic guitar melody, cheerful and relaxing, mixed at 30% volume so voiceover is crystal clear.
• Thai Voiceover (Natural friendly conversational tone "เพื่อนรีวิวให้เพื่อน", exactly 10 seconds total):
  "{sanitized_vo}"

[RULES & CONSTRAINTS]
No English text, no foreign logos, no digital watermarks. Consistent lighting and exact product packaging preservation matching the uploaded image throughout all 10 seconds."""

    return {
        "video_id": str(uuid.uuid4()),
        "product_title_th": title,
        "product_thumbnail": thumb,
        "category": cat,
        "style_mode": "BRIGHT_PREMIUM_LIFESTYLE",
        "total_duration_sec": 10.0,
        "shots_count": 5,
        "shots": shots,
        "universal_flow_omni_prompt": universal_flow_omni_prompt,
        "full_voiceover_th": sanitized_vo,
        "compliance_status": comp_status,
        "compliance_flags": comp_flags,
        "summary_th": f"สร้าง Storyboard 5 ช่อง (10 วิ) สไตล์ Bright Premium Lifestyle พร้อม Flow Omni Prompt สำเร็จ!"
    }
