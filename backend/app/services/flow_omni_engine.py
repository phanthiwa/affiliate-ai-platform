import uuid
from typing import List, Dict, Any, Optional
from app.models.schemas import StoryboardShot, ComplianceStatus
from app.agents.compliance_agent import check_and_sanitize_thai_script
from app.data.thai_products_mock import SAMPLE_THAI_PRODUCTS

# Curated High-Definition Scene Imagery for Winning Products (5 distinct scenes per product)
PRODUCT_SCENE_ASSETS: Dict[str, List[str]] = {
    # 1. หมอนนวดคอบ่าไหล่ไร้สาย (Massager)
    "massager": [
        "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=800&auto=format&fit=crop&q=80", # Scene 1: POV Pick up
        "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?w=800&auto=format&fit=crop&q=80", # Scene 2: Close-up Power on
        "https://images.unsplash.com/photo-1600334129128-685c5582fd35?w=800&auto=format&fit=crop&q=80", # Scene 3: Macro Kneading demo
        "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&auto=format&fit=crop&q=80", # Scene 4: POV Place on cozy sofa
        "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=800&auto=format&fit=crop&q=80", # Scene 5: Hero Shot on pedestal
    ],
    # 2. เซรั่มใบบัวบก / สกินแคร์ (Serum / Cica)
    "serum": [
        "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&auto=format&fit=crop&q=80", # Scene 1: POV Pick up
        "https://images.unsplash.com/photo-1608248597359-52e646277038?w=800&auto=format&fit=crop&q=80", # Scene 2: Close-up Open dropper
        "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&auto=format&fit=crop&q=80", # Scene 3: Macro Droplet on skin
        "https://images.unsplash.com/photo-1617897903246-719242758050?w=800&auto=format&fit=crop&q=80", # Scene 4: Place with green leaves
        "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800&auto=format&fit=crop&q=80", # Scene 5: Hero Shot with sunbeam
    ],
    # 3. แก้วเก็บความเย็น 900ml (Tumbler)
    "tumbler": [
        "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&auto=format&fit=crop&q=80", # Scene 1: POV Pick up
        "https://images.unsplash.com/photo-1577937927133-66ef06acdf18?w=800&auto=format&fit=crop&q=80", # Scene 2: Open lid inspect
        "https://images.unsplash.com/photo-1556881286-fc6915169721?w=800&auto=format&fit=crop&q=80", # Scene 3: Pour icy cold drink
        "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=800&auto=format&fit=crop&q=80", # Scene 4: Set on aesthetic table
        "https://images.unsplash.com/photo-1589365278144-c9e705f843ba?w=800&auto=format&fit=crop&q=80", # Scene 5: Hero Shot on pedestal
    ],
    # 4. ขาตั้งกล้อง AI เซลฟี่ 360 (Tripod)
    "tripod": [
        "https://images.unsplash.com/photo-1589739900243-4b52cd9b104e?w=800&auto=format&fit=crop&q=80", # Scene 1: POV Pick up
        "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&auto=format&fit=crop&q=80", # Scene 2: Snap mount smartphone
        "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop&q=80", # Scene 3: Auto 360 rotation demo
        "https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?w=800&auto=format&fit=crop&q=80", # Scene 4: Set on studio desk
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&auto=format&fit=crop&q=80", # Scene 5: Hero Shot with studio light
    ],
    # 5. กันแดดสูตรน้ำนม (Sunscreen)
    "sunscreen": [
        "https://images.unsplash.com/photo-1556228722-d0b5d124b899?w=800&auto=format&fit=crop&q=80", # Scene 1: POV Pick up
        "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=800&auto=format&fit=crop&q=80", # Scene 2: Open cap
        "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800&auto=format&fit=crop&q=80", # Scene 3: Smooth matte blend
        "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=800&auto=format&fit=crop&q=80", # Scene 4: Set with sunglasses & beach light
        "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800&auto=format&fit=crop&q=80", # Scene 5: Hero Shot glowing skin
    ],
    # 6. เจลดับกลิ่นชักโครกรูปดอกไม้ (Toilet Gel)
    "toilet_gel": [
        "https://images.unsplash.com/photo-1584824486509-112e4181ff6b?w=800&auto=format&fit=crop&q=80", # Scene 1: POV Pick up syringe tube
        "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800&auto=format&fit=crop&q=80", # Scene 2: Remove silicone nozzle cap
        "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=800&auto=format&fit=crop&q=80", # Scene 3: Stamp cute flower gel
        "https://images.unsplash.com/photo-1507652313519-d4e9174996dd?w=800&auto=format&fit=crop&q=80", # Scene 4: Clean aesthetic bathroom vibe
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&auto=format&fit=crop&q=80", # Scene 5: Hero Shot refreshing scent
    ]
}

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
        title = product_title_th.strip() if product_title_th else "เซรั่มใบบัวบก Cica Intense Calming"
        thumb = product_thumbnail or "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&auto=format&fit=crop&q=80"
        cat = category or "สกินแคร์ / ความงาม"
        usps = usp_th or ["ลดสิว", "ผิวฉ่ำโกลว์", "ซึมไว 3 วิ"]

    # Category matching for 5 distinct scene images
    if "หมอนนวด" in title or "นวด" in title or "massager" in str(product_id).lower():
        scene_images = PRODUCT_SCENE_ASSETS["massager"]
        prop_surface = "โซฟาพักผ่อนโทนอบอุ่นและโต๊ะไม้โอ๊ค แสงแดดยามบ่ายส่องผ่านมู่ลี่"
        hand_action_1 = "มือ POV เอื้อมหยิบหมอนนวดหนังพรีเมียมสีมินิมอลขึ้นมาอย่างนุ่มนวล"
        hand_action_2 = "มือ POV กดปุ่มเปิดสวิตช์ ไฟ LED สว่างขึ้น ระบบประคบอุ่นพร้อมทำงาน"
        hand_action_3 = "กล้อง Macro โคลสอัพหัวนวด 4D หมุนคลึงเป็นจังหวะ นุ่มลึกผ่อนคลาย"
        hand_action_4 = "มือ POV วางหมอนนวดลงบนโซฟาเคียงข้างหมอนอิงและชาสมุนไพรอุ่นๆ"
        hand_action_5 = "Hero Shot หมอนนวดไฟฟ้าตั้งสง่างามกลางแท่นหินสีเบจ แสงเรืองรองพรีเมียม"
        sfx_1, sfx_2, sfx_3, sfx_4, sfx_5 = "Soft leather pick-up whoosh", "Crisp power click + gentle chime", "Gentle deep motor hum", "Soft cushion placement tap", "Sparkle chime + cash kaching"
        on_text_1, on_text_2, on_text_3, on_text_4, on_text_5 = "ปวดคอบ่าไหล่ ต้องลอง!", "ระบบประคบอุ่น 42°C", "นวดลึกถึงเส้น 4 มิติ", "แบตอึด ใช้งานไร้สาย", "จิ้มตะกร้าซ้ายล่างเลย!"
        vo_script = "ปวดคอบ่าไหล่ต้องลองตัวนี้! หมอนนวดไร้สาย นวดลึกถึงเส้น ประคบอุ่นฟินมาก จิ้มตะกร้าเหลืองเลยน้า"
        english_item = "ergonomic cordless neck and shoulder heating massager"

    elif "แก้ว" in title or "tumbler" in str(product_id).lower():
        scene_images = PRODUCT_SCENE_ASSETS["tumbler"]
        prop_surface = "โต๊ะไม้สไตล์มินิมอลเคียงข้างหน้าต่าง แสงแดดยามเช้าประกายระยิบระยับ"
        hand_action_1 = "มือ POV เอื้อมไปจับด้ามแก้วสแตนเลสสีพาสเทลขึ้นมาอย่างมั่นคง"
        hand_action_2 = "มือ POV หมุนเปิดฝาแก้วอย่างนุ่มนวล โชว์ช่องใส่หลอดและยางกันรั่ว"
        hand_action_3 = "กล้อง Macro มือเทน้ำแข็งและน้ำผลไม้ใสลงในแก้ว ไอน้ำเย็นสดชื่น"
        hand_action_4 = "มือ POV วางแก้วลงข้างผลส้มสดและใบไม้สีเขียวสะอาดตา"
        hand_action_5 = "Hero Shot แก้วเก็บความเย็นตั้งสง่างามกลางแท่นหินทราเวอร์ทีน ละอองแสงทองส่องสว่าง"
        sfx_1, sfx_2, sfx_3, sfx_4, sfx_5 = "Solid cup pick-up", "Smooth lid twist", "Ice cubes clinking + water pour", "Solid base placement tap", "Sparkle chime"
        on_text_1, on_text_2, on_text_3, on_text_4, on_text_5 = "เก็บเย็นข้ามวัน!", "สแตนเลส 316 แท้", "ไม่เป็นไอน้ำเกาะ", "ขนาดใหญ่ 900ml", "จิ้มตะกร้าซ้ายล่าง!"
        vo_script = "แก้วเก็บความเย็นตัวโปรด! ใส่น้ำแข็งข้ามวันไม่ละลาย สแตนเลส 316 แท้ จิ้มตะกร้าเหลืองซ้ายล่างเลยน้า"
        english_item = "aesthetic pastel stainless steel 900ml thermal tumbler"

    elif "ขาตั้งกล้อง" in title or "tripod" in str(product_id).lower():
        scene_images = PRODUCT_SCENE_ASSETS["tripod"]
        prop_surface = "โต๊ะทำงานสตูดิโอสไตล์โมเดิร์น แสงไฟนุ่มนวลระดับโปร"
        hand_action_1 = "มือ POV เอื้อมหยิบขาตั้งกล้องอัจฉริยะสีดำด้านทรงกระบอกขึ้นมา"
        hand_action_2 = "มือ POV กางตัวยึดสมาร์ทโฟนออกอย่างมั่นคง ล็อคแน่นหนา"
        hand_action_3 = "กล้อง Macro ซูมระบบหมุนรอบตัว 360 องศา AI ตรวจจับใบหน้าลื่นไหล"
        hand_action_4 = "มือ POV วางขาตั้งกล้องเคียงข้างแล็ปท็อปและไฟสตูดิโอมินิมอล"
        hand_action_5 = "Hero Shot ขาตั้งกล้อง AI Tracking หมุนสง่างามกลางแท่นโชว์แสงเรืองรอง"
        sfx_1, sfx_2, sfx_3, sfx_4, sfx_5 = "Tech pick-up whoosh", "Smooth clamp lock sound", "Futuristic tracking servo hum", "Sturdy base placement tap", "High-tech chime"
        on_text_1, on_text_2, on_text_3, on_text_4, on_text_5 = "หมุนตามตัว 360°!", "ไม่ต้องต่อบลูทูธ", "AI ล็อคหน้าแม่นยำ", "สายทำคลิปต้องมี", "กดสั่งในตะกร้าเลย!"
        vo_script = "สายทำคลิปไลฟ์สดต้องมี! ขาตั้งกล้อง AI หมุนตามตัว 360 องศา ไม่ง้อตากล้อง สั่งในตะกร้าเหลืองได้เลย"
        english_item = "AI face tracking 360 smart motorized livestreaming tripod"

    elif "กันแดด" in title or "sunscreen" in str(product_id).lower():
        scene_images = PRODUCT_SCENE_ASSETS["sunscreen"]
        prop_surface = "โต๊ะกระจกใสริมสระน้ำ แสงแดดธรรมชาตินุ่มนวลสะท้อนประกายน้ำ"
        hand_action_1 = "มือ POV หยิบหลอดกันแดดสีขาวมินิมอลขึ้นมาอย่างทะมัดทะแมง"
        hand_action_2 = "มือ POV หมุนเปิดฝาเกลียว เผยหัวบีบเรียวเล็กควบคุมปริมาณได้ดี"
        hand_action_3 = "กล้อง Macro มือบีบเนื้อน้ำนมลงบนผิว เกลี่ยแล้วแตกตัวซึมหายทันที"
        hand_action_4 = "มือ POV วางหลอดกันแดดลงข้างแว่นตากันแดดและหมวกสานชายหาด"
        hand_action_5 = "Hero Shot หลอดกันแดดเปล่งประกายกลางแท่นหินอ่อน โดดเด่นกลางแสงแดด"
        sfx_1, sfx_2, sfx_3, sfx_4, sfx_5 = "Gentle bottle pick-up", "Twist cap pop", "Smooth lotion glide SFX", "Clean placement tap", "Sunbeam sparkle ding"
        on_text_1, on_text_2, on_text_3, on_text_4, on_text_5 = "บางเบา คุมมัน 12 ชม.", "SPF50+ PA++++", "หน้าไม่วอก ไม่เยิ้ม", "ไม่อุดตันผิว", "จิ้มตะกร้าซ้ายล่าง!"
        vo_script = "กันแดดน้ำนมลูกรัก! บางเบาคุมมัน 12 ชั่วโมง หน้าไม่วอกไม่เยิ้ม ทาทับเมคอัพได้ จิ้มตะกร้าเหลืองเลยน้า"
        english_item = "ultra-light matte sunscreen milk bottle with SPF50+"

    elif "เจลดับกลิ่น" in title or "toilet" in str(product_id).lower():
        scene_images = PRODUCT_SCENE_ASSETS["toilet_gel"]
        prop_surface = "ชั้นวางของห้องน้ำสไตล์โมเดิร์นสีขาว สะอาด สดชื่น"
        hand_action_1 = "มือ POV เอื้อมหยิบกระบอกเจลรูปดอกไม้สีพาสเทลขึ้นมา"
        hand_action_2 = "มือ POV ปลดฝาครอบซิลิโคนออก พร้อมใช้งาน"
        hand_action_3 = "กล้อง Macro มือปั๊มเนื้อเจลใสรูปดอกไม้ติดขอบกระจกอย่างสวยงาม"
        hand_action_4 = "มือ POV วางกระบอกเจลลงข้างก้านไม้หอมและต้นไม้ประดับห้องน้ำ"
        hand_action_5 = "Hero Shot กระบอกเจลดับกลิ่นตั้งสง่างาม ท่ามกลางบรรยากาศหอมสดชื่น"
        sfx_1, sfx_2, sfx_3, sfx_4, sfx_5 = "Clean tube pick-up", "Cap pop sound", "Satisfying gel stamp squish + chime", "Delicate shelf placement", "Fresh breeze chime"
        on_text_1, on_text_2, on_text_3, on_text_4, on_text_5 = "กลิ่นหอม สดชื่นทันที!", "เจลดอกไม้น่ารัก", "ดับกลิ่นนาน 30 วัน", "ห้องน้ำหอมฟุ้ง", "จิ้มตะกร้าซ้ายล่าง!"
        vo_script = "เจลดับกลิ่นชักโครกรูปดอกไม้! ปั๊มเดียวห้องน้ำหอมสดชื่น ดับกลิ่นยาวนาน 30 วัน สั่งในตะกร้าเหลืองเลยน้า"
        english_item = "aromatic floral toilet stamp gel syringe dispenser"

    else: # Default: Skincare / Serum (เซรั่มใบบัวบก / สกินแคร์)
        scene_images = PRODUCT_SCENE_ASSETS["serum"]
        prop_surface = "เคาน์เตอร์หินอ่อนสีขาวนวล ประกายแสงแดดเช้าส่องสะท้อนหรูหรา"
        hand_action_1 = "มือผู้หญิงเรียวสวย POV เอื้อมไปหยิบขวดเซรั่มแก้วขึ้นมาจากเคาน์เตอร์"
        hand_action_2 = "มือ POV หมุนคลายเกลียวฝาดรอปเปอร์อย่างนุ่มนวล ยกหลอดแก้วใสขึ้น"
        hand_action_3 = "กล้อง Macro ปลายดรอปเปอร์หยดเนื้อเซรั่มใส 1 หยดลงบนหลังมืออย่างนุ่มนวล"
        hand_action_4 = "มือ POV วางขวดเซรั่มลงข้างใบไม้สีเขียวสดและหยดน้ำใสบริสุทธิ์"
        hand_action_5 = "Hero Shot ขวดเซรั่มแก้วเปล่งประกายกลางแท่นหินอ่อนสีเบจ ลำแสงสีทองเรืองรอง"
        sfx_1, sfx_2, sfx_3, sfx_4, sfx_5 = "Gentle glass pick-up chime", "Tactile cap twist & pop", "Crisp water drop ripple", "Delicate glass placement tap", "Sparkle ding chime"
        on_text_1, on_text_2, on_text_3, on_text_4, on_text_5 = "ผิวฉ่ำโกลว์ใน 3 วัน!", "เนื้อใส ซึมไวมาก", "หยดเดียว เติมน้ำให้ผิว", "สารสกัดพรีเมียม", "กดสั่งในตะกร้าเลย!"
        vo_script = "ทุกคน ตัวนี้ใช้ดีมาก ผิวฉ่ำโกลว์ใสขึ้นจริง เนื้อบางเบา ซึมไว ไม่เหนอะหนะ จิ้มตะกร้าซ้ายล่างได้เลยน้า!"
        english_item = "luxury aesthetic glass serum bottle with dropper"

    comp_status, sanitized_vo, comp_flags = check_and_sanitize_thai_script(vo_script)

    # Build 5 Storyboard Shots (2.0s each) with dedicated scene images & video motion types
    shots: List[StoryboardShot] = [
        StoryboardShot(
            shot_number=1,
            start_sec=0.0,
            end_sec=2.0,
            visual_description_th=f"ฉาก 1: {hand_action_1} บน {prop_surface}",
            image_prompt_for_ai=f"Scene 1 (0-2s): POV high-angle view with slow smooth push-in. Well-manicured hand picks up {english_item} from sunlit white marble vanity, warm morning sunbeam flare, Bright Premium Lifestyle, 4k",
            camera_direction="POV High-Angle with Slow Push-in",
            on_screen_text_th=on_text_1,
            voiceover_th=sanitized_vo[:len(sanitized_vo)//4],
            b_roll_suggestion="ประกายแสงสะท้อนเลนส์ (Lens flare) นุ่มนวล",
            sound_effect_cue=sfx_1,
            scene_image_url=scene_images[0],
            video_motion_type="zoom_in"
        ),
        StoryboardShot(
            shot_number=2,
            start_sec=2.0,
            end_sec=4.0,
            visual_description_th=f"ฉาก 2: {hand_action_2}",
            image_prompt_for_ai=f"Scene 2 (2-4s): Seamless cut to 45-degree close-up with soft rotational movement. POV hand gently interacts with and inspects {english_item}, crisp product textures, 4k",
            camera_direction="Close-up 45-degree with Smooth Orbit",
            on_screen_text_th=on_text_2,
            voiceover_th=sanitized_vo[len(sanitized_vo)//4:len(sanitized_vo)//2],
            b_roll_suggestion="แสงตกกระทบผิวสัมผัสวัสดุ",
            sound_effect_cue=sfx_2,
            scene_image_url=scene_images[1],
            video_motion_type="pan_right"
        ),
        StoryboardShot(
            shot_number=3,
            start_sec=4.0,
            end_sec=6.0,
            visual_description_th=f"ฉาก 3: {hand_action_3}",
            image_prompt_for_ai=f"Scene 3 (4-6s): Extreme macro slow-motion focus. POV hand demonstrating active usage of {english_item}, satisfying tactile feedback, soft bokeh background, 4k",
            camera_direction="Extreme Macro with Subtle Slow-Motion",
            on_screen_text_th=on_text_3,
            voiceover_th=sanitized_vo[len(sanitized_vo)//2:len(sanitized_vo)*3//4],
            b_roll_suggestion="ภาพหยดน้ำ / การทำงานแบบสโลว์โมชัน",
            sound_effect_cue=sfx_3,
            scene_image_url=scene_images[2],
            video_motion_type="macro_pulse"
        ),
        StoryboardShot(
            shot_number=4,
            start_sec=6.0,
            end_sec=8.0,
            visual_description_th=f"ฉาก 4: {hand_action_4}",
            image_prompt_for_ai=f"Scene 4 (6-8s): Smooth cut to medium POV panning shot. POV hand gracefully sets down {english_item} next to fresh botanical green leaves and water drops on sunlit table, 4k",
            camera_direction="Medium POV Shot with Dutch Tilt Pan",
            on_screen_text_th=on_text_4,
            voiceover_th=sanitized_vo[len(sanitized_vo)*3//4:],
            b_roll_suggestion="ใบไม้สีเขียวสดและหยดน้ำสะท้อนแสงแดด",
            sound_effect_cue=sfx_4,
            scene_image_url=scene_images[3],
            video_motion_type="dutch_tilt"
        ),
        StoryboardShot(
            shot_number=5,
            start_sec=8.0,
            end_sec=10.0,
            visual_description_th=f"ฉาก 5: {hand_action_5}",
            image_prompt_for_ai=f"Scene 5 (8-10s): Final Hero Shot. Cinematic slow orbit zoom-out centering {english_item} on luxury travertine stone pedestal bathed in brilliant warm morning sunbeams, 4k",
            camera_direction="Hero Shot with Cinematic Orbit & Zoom-Out",
            on_screen_text_th=on_text_5,
            voiceover_th="จิ้มตะกร้าเหลืองซ้ายล่างได้เลยน้า!",
            b_roll_suggestion="ละอองแสงทองส่องสว่างเรืองรอง",
            sound_effect_cue=sfx_5,
            scene_image_url=scene_images[4],
            video_motion_type="cinematic_orbit"
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
