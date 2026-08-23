from typing import List
import uuid
from app.models.schemas import ProductBase, ThaiScript, ComplianceStatus
from app.agents.compliance_agent import check_and_sanitize_thai_script

CREATIVE_ANGLES = [
    {
        "id": "PROBLEM_SOLUTION",
        "name_th": "ปัญหา → ทางออก (Problem → Solution)",
        "hook_template": "ใครที่เจอปัญหา{pain_point} หยุดดูคลิปนี้ก่อน!",
        "persona": "เพื่อนสนิทแนะนำของดี"
    },
    {
        "id": "BEFORE_AFTER",
        "name_th": "ก่อนใช้ vs หลังใช้ (Before → After)",
        "hook_template": "เทียบให้ดูชัดๆ ระหว่างมีตัวนี้ กับไม่มี... ชีวิตต่างกันขนาดไหน!",
        "persona": "รีวิวเรียลๆ 100%"
    },
    {
        "id": "PRICE_VALUE",
        "name_th": "ป้ายยาโปรเด็ด คุ้มเกินราคา (Price / Value Deal)",
        "hook_template": "แก! อันนี้คือเกินไปมาก ราคาหลักร้อยแต่คุณภาพเทียบหลักพัน!",
        "persona": "สายช้อปดีลเด็ด"
    },
    {
        "id": "THINGS_I_WISH_I_KNEW",
        "name_th": "สิ่งที่น่าจะรู้ก่อนซื้อ (Things I Wish I Knew)",
        "hook_template": "3 ข้อที่ควรรู้ก่อนกดสั่ง {product_name} พลาดแล้วจะเสียดาย!",
        "persona": "ผู้เชี่ยวชาญแนะนำอย่างจริงใจ"
    },
    {
        "id": "POV_DAILY_LIFE",
        "name_th": "POV ในชีวิตประจำวัน (Day in My Life)",
        "hook_template": "POV: เมื่อคุณเพิ่งเจอไอเทมลับที่ทำให้ชีวิตง่ายขึ้น 10 เท่า!",
        "persona": "ครีเอเตอร์ไลฟ์สไตล์"
    }
]

def generate_thai_script_for_product(
    product: ProductBase,
    angle_index: int = 0,
    duration_sec: int = 20
) -> ThaiScript:
    angle = CREATIVE_ANGLES[angle_index % len(CREATIVE_ANGLES)]
    
    # Context-aware tailoring for Thai affiliate creators
    if "ใบบัวบก" in product.title_th or "สกินแคร์" in product.category.lower() or "beauty" in product.category.lower():
        if angle["id"] == "PROBLEM_SOLUTION":
            hook = "ใครที่ผิวพัง หน้าเป็นสิวซ้ำซากใช้อะไรก็ไม่หาย หยุดฟังทางนี้ก่อน!"
            body = (
                f"คือเมื่อก่อนเราเป็นคนที่ผิวแพ้ง่ายมาก จนมาเจอ {product.title_th} ตัวนี้ "
                f"เขามีสารสกัด Cica เข้มข้น เนื้อเซรั่มบางเบา ซึมไวมาก ไม่เหนียวเหนอะหนะ "
                f"เราทาเช้า-เย็น ต่อเนื่องแค่ 7 วัน รอยสิวกับรอยแดงคือจางลงแบบเห็นได้ชัด ผิวดูแข็งแรงขึ้นเยอะมาก"
            )
            cta = f"ตอนนี้ใน TikTok Shop จัดโปรลดเหลือ ฿{product.sale_price} มีคูปองส่งฟรีด้วย กดสั่งที่ตะกร้าเหลืองมุมซ้ายล่างได้เลยนะ!"
        elif angle["id"] == "BEFORE_AFTER":
            hook = "หน้าสดโนฟิลเตอร์ให้ดูเลย 7 วันก่อนกับวันนี้ ผิวคนละเรื่อง!"
            body = (
                f"เมื่อก่อนคือรอยสิวเยอะมาก แต่พอลองใช้ {product.title_th} ขวดยังไม่ทันหมด "
                f"ผิวสงบลงเยอะมาก สิวใหม่ไม่ค่อยขึ้น แล้วเนื้อสัมผัสคือสบายผิวสุดๆ "
                f"ไม่มีแอลกอฮอล์ ไม่มีน้ำหอม ผิวแพ้ง่ายใช้ได้สบายใจ 100%"
            )
            cta = f"ราคาโปรเปิดตัวคุ้มมาก แค่ ฿{product.sale_price} แนะนำให้ตุน 2 ขวดไปเลย จิ้มตะกร้าซ้ายมือด่วน!"
        else:
            hook = "แก! เซรั่มขวดนี้คือเกินเรื่องมาก ถูกและดีมีอยู่จริง!"
            body = (
                f"ไม่แปลกใจเลยทำไมคนรีวิวกันเยอะมาก {product.title_th} "
                f"คุณภาพเทียบสกินแคร์เคาน์เตอร์แบรนด์ได้เลย ทาแล้วผิวฉ่ำฟู สิวแห้งไว "
                f"ที่สำคัญคือให้ค่าคอมและส่วนลดจุกๆ ใครยังไม่มีต้องมีติดโต๊ะเครื่องแป้งไว้เลย"
            )
            cta = "พิกัดอยู่ที่ตะกร้าสีเหลืองมุมซ้ายล่าง รีบกดก่อนของจะหมดสต็อกนะทุกคน!"
            
    elif "นวด" in product.title_th or "health" in product.category.lower():
        if angle["id"] == "PROBLEM_SOLUTION":
            hook = "ใครที่ตื่นมาแล้วปวดคอบ่าไหล่จนหันคอไม่ได้ แกต้องมีตัวนี้ด่วน!"
            body = (
                f"เป็นมนุษย์ออฟฟิศนั่งจ้องคอมทั้งวัน เส้นตึงจนปวดหัวไมเกรน "
                f"ตั้งแต่ได้ {product.title_th} มา คือช่วยชีวิตมาก! "
                f"เขามีระบบประคบอุ่น 42 องศา หัวนวด 4D กดลึกถึงเส้นเหมือนคนมานวดให้จริงๆ "
                f"ที่สำคัญคือไร้สาย นั่งทำงานไปนวดไปได้เลย สบายตัวขึ้นเยอะมาก"
            )
            cta = f"จากราคาเต็ม ฿{product.original_price} วันนี้ลดเหลือ ฿{product.sale_price} พิกัดตะกร้าซ้ายล่าง กดเลย!"
        else:
            hook = "ตอนแรกคิดว่าเป็นของเล่น แต่พอลองใช้จริง... บอกลาร้านนวดไปเลย!"
            body = (
                f"ประหยัดค่านวดเดือนละเป็นพัน {product.title_th} นวดโคตรฟิน "
                f"หัวนวดนิ่มไม่เจ็บกระดูก ปรับแรงได้ 3 ระดับ ชาร์จครั้งเดียวใช้ได้ยาวๆ ทั้งสัปดาห์ "
                f"ใครที่พ่อแม่บ่นปวดหลัง หรือตัวเองเป็นออฟฟิศซินโดรม ตัวนี้คุ้มค่าที่สุด"
            )
            cta = "กดสั่งในตะกร้าเหลืองหน้าร้านตรงนี้ได้เลย จัดส่งไว มีรับประกันสินค้าด้วยนะ!"
    else:
        # High-converting generic framework
        hook = f"เพิ่งค้นพบไอเทมลับที่ทำให้ชีวิตง่ายขึ้น 10 เท่า! ตัวนี้เลย {product.brand or 'แบรนด์นี้'}"
        body = (
            f"ใครที่กำลังมองหา {product.title_th} บอกเลยว่าตัวนี้ตอบโจทย์มาก "
            f"ยอดขายทะลุ {product.total_sales:,} ชิ้น รีวิว {product.rating} ดาว แน่นมาก "
            f"วัสดุดีตรงปก ใช้งานง่าย ประหยัดเวลาชีวิตไปได้เยอะจริงๆ"
        )
        cta = f"ราคาพิเศษวันนี้ลดเหลือเพียง ฿{product.sale_price} เท่านั้น รีบจิ้มตะกร้าซ้ายมือเลย!"

    raw_voiceover = f"{hook} {body} {cta}"
    
    # Run through compliance agent
    compliance_status, sanitized_script, flags = check_and_sanitize_thai_script(raw_voiceover)
    
    return ThaiScript(
        id=str(uuid.uuid4()),
        product_id=product.id,
        product_title_th=product.title_th,
        angle_type=angle["name_th"],
        target_duration_sec=duration_sec,
        style_persona=angle["persona"],
        hook_text_th=hook,
        body_text_th=body,
        cta_text_th=cta,
        full_voiceover_th=sanitized_script,
        word_count=len(sanitized_script.split()),
        compliance_status=compliance_status,
        compliance_notes=[f"{f['detected_term']} -> {f['suggested_replacement']}" for f in flags]
    )
