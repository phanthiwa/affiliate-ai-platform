from app.models.schemas import (
    ProductBase, ProductIntelligenceCard, PainPoint, Objection, HookTemplate
)

def generate_product_intelligence_card(product: ProductBase) -> ProductIntelligenceCard:
    # Comprehensive 11-Section Product Intelligence Card tailored to Thai consumers
    
    if "ใบบัวบก" in product.title_th or "เซรั่ม" in product.title_th:
        return ProductIntelligenceCard(
            product_id=product.id,
            product_summary_th=f"{product.title_th} เซรั่มฟื้นฟูผิวแพ้ง่าย ลดรอยดำรอยแดงจากสิว ราคาคุ้มค่า ฿{product.sale_price} ค่าคอมมิชชั่นสูง {product.commission_rate}%",
            target_audience_th="วัยรุ่นและคนทำงานอายุ 18-35 ปี ที่มีปัญหาผิวเป็นสิวเรื้อรัง ผิวแพ้แมสก์ หน้ามันขาดน้ำ และต้องการสกินแคร์ราคาจับต้องได้",
            customer_pain_points=[
                PainPoint(issue_th="สิวเห่อซ้ำซากใช้อะไรก็แพ้ แสบหน้า", emotional_trigger="ขาดความมั่นใจ กลัวโดนทักเรื่องหน้าพัง"),
                PainPoint(issue_th="รอยดำรอยแดงจากสิวจางช้ามาก แต่งหน้ากลบไม่มิด", emotional_trigger="เสียเวลาแต่งหน้านาน เปลืองคอนซีลเลอร์"),
                PainPoint(issue_th="สกินแคร์เคาน์เตอร์แบรนด์ราคาแพงเกินงบ", emotional_trigger="ความกังวลเรื่องค่าใช้จ่าย")
            ],
            usp_th=[
                "สารสกัด Cica เข้มข้น 95% มาตรฐานแล็บเกาหลี",
                "เนื้อเซรั่มบางเบา ซึมไวใน 3 วินาที ไม่เหนียวเหนอะหนะ",
                "0% แอลกอฮอล์ พาราเบน และน้ำหอมสังเคราะห์ ผิวแพ้ง่ายใช้ได้ 100%"
            ],
            reasons_to_buy=[
                f"ราคาโปรเปิดตัวลด {product.discount_pct:.0f}% เหลือเพียง ฿{product.sale_price}",
                f"รีวิวเฉลี่ย {product.rating} ดาว จากผู้ใช้จริงกว่า {product.review_count:,} คน",
                "เห็นผลการปลอบประโลมผิวอย่างชัดเจนใน 7 วัน"
            ],
            purchase_objections=[
                Objection(objection_th="กลัวใช้แล้วแพ้ สิวเห่อกว่าเดิม", counter_argument_th="ผ่านการทดสอบ Dermatologist Tested จากสถาบันแพทย์ผิวหนัง"),
                Objection(objection_th="ของแท้ไหม ทำไมราคาถูกจัง", counter_argument_th="เป็น Official Store ส่งตรงจากบริษัท มีเลข อย. ชัดเจน")
            ],
            competitor_comparison_th="เข้มข้นกว่าแบรนด์ทั่วไปในท้องตลาด 2 เท่า แต่ราคาถูกกว่าแบรนด์นำเข้าเกือบ 50% และให้ค่าคอมมิชชั่นสูงถึง 25%",
            content_opportunities=[
                "วิดีโอซูมผิวหน้า 7 วัน (Day 1 vs Day 7)",
                "ทดสอบความซึมไวบนหลังมือและกระดาษซับมัน",
                "POV ป้ายยาเพื่อนที่มีปัญหาสิวประจำเดือน"
            ],
            recommended_angles=[
                "1. Problem → Solution (สิวแพ้แมสก์หายได้ใน 7 วัน)",
                "2. Authentic Casual (รีวิวโนสปอน ใช้เองจนหมดขวดที่ 3)",
                "3. Bargain Deal (ป้ายยาโปร 1 แถม 1 กดในตะกร้าด่วน)"
            ],
            recommended_hooks=[
                HookTemplate(hook_type="SHOCK_PAIN", hook_text_th="ใครที่ผิวพังเพราะสิวซ้ำซาก หยุดดูคลิปนี้ก่อนจะเสียเงินซื้อครีมแพง!", estimated_retention_3s=89.2),
                HookTemplate(hook_type="CURIOSITY", hook_text_th="ทำไมคนใน TikTok ถึงแห่ตุนเซรั่มขวดเขียวตัวนี้กันคนละ 3 ขวด?", estimated_retention_3s=86.5),
                HookTemplate(hook_type="AUTHENTIC_PROOF", hook_text_th="หน้าสดโนฟิลเตอร์ให้ดูเลย 7 วันที่แล้วกับวันนี้ ผิวคนละเรื่อง!", estimated_retention_3s=92.0)
            ],
            recommended_cta_th="รีบกดสั่งในตะกร้าสีเหลืองมุมซ้ายล่าง ตอนนี้มีคูปองลดเพิ่มอีก 50 บาท ส่งฟรีด้วยนะแก!"
        )
    elif "นวด" in product.title_th:
        return ProductIntelligenceCard(
            product_id=product.id,
            product_summary_th=f"{product.title_th} หมอนนวดแก้ปวดเมื่อยคอบ่าไหล่ระบบ 4D ไร้สาย นวดลึกถึงเส้นเหมือนมีหมอนวดมาทำให้ที่บ้าน",
            target_audience_th="พนักงานออฟฟิศ ฟรีแลนซ์ คนขับรถนานๆ และผู้สูงอายุที่มีปัญหาปวดเมื่อยกล้ามเนื้อเรื้อรัง",
            customer_pain_points=[
                PainPoint(issue_th="นั่งหน้าคอมทั้งวัน ปวดคอบ่าไหล่จนปวดหัวไมเกรน", emotional_trigger="ทรมาน ทำงานไม่มีสมาธิ รบกวนการนอน"),
                PainPoint(issue_th="ไม่มีเวลาไปร้านนวด และค่านวดครั้งละ 400-600 บาทเปลืองมาก", emotional_trigger="เปลืองเงิน เปลืองเวลาเดินทาง")
            ],
            usp_th=[
                "หัวนวดซิลิโคน 4D จำลองแรงกดนิ้วมือคนแท้ๆ ไม่เจ็บกระดูก",
                "ระบบประคบอุ่นอินฟราเรด 42 องศา คลายเส้นเลือดฝอย",
                "ไร้สาย แบตเตอรี่อึดใช้งานได้ 7 วันต่อการชาร์จ 1 ครั้ง"
            ],
            reasons_to_buy=[
                f"ค่าคอมมิชชั่นสูงมาก ฿{product.estimated_commission:.2f} ต่อออเดอร์",
                "ประหยัดค่านวดรายเดือน ซื้อครั้งเดียวใช้ได้ทั้งบ้าน",
                "พกพาไปนวดในรถหรือที่ทำงานได้ตลอดเวลา"
            ],
            purchase_objections=[
                Objection(objection_th="กลัวแรงนวดเบา นวดไม่โดนเส้น", counter_argument_th="ปรับความแรงได้ 3 ระดับ มอเตอร์พลังสูงแรงบิดลึกถึงกล้ามเนื้อชั้นใน"),
                Objection(objection_th="กลัวเครื่องหนักเมื่อยแขน", counter_argument_th="ดีไซน์สายสะพายมือแบบฟรีแฮนด์ นั่งทำงานไปนวดไปได้สบายๆ")
            ],
            competitor_comparison_th="เหนือกว่าหมอนนวดทั่วไปตรงที่ไร้สายจริง ประคบอุ่นได้เร็วใน 10 วินาที และหัวนวดนิ่มไม่กระแทกกระดูกสันหลัง",
            content_opportunities=[
                "POV นั่งทำงานหลังขดหลังแข็ง แล้วกดเปิดสวิตช์ฟินทันที",
                "ซื้อเป็นของขวัญเซอร์ไพรส์พ่อแม่วัยเกษียณ",
                "คำนวณความคุ้มค่า เทียบกับค่านวดแผนไทย 1 ปี"
            ],
            recommended_angles=[
                "1. Office Syndrome Savior (ช่วยชีวิตมนุษย์ออฟฟิศ)",
                "2. Cost Comparison (เทียบความคุ้มค่าค่านวด)",
                "3. Gift for Parents (ของขวัญวันเกิดพ่อแม่)"
            ],
            recommended_hooks=[
                HookTemplate(hook_type="DIRECT_PAIN", hook_text_th="ใครที่ตื่นมาแล้วคอแข็ง หันซ้ายหันขวาไม่ได้ แกต้องดูสิ่งนี้!", estimated_retention_3s=94.5),
                HookTemplate(hook_type="CURIOSITY", hook_text_th="ยอมรับว่าตอนแรกคิดว่าของเล่น แต่พอลองใช้จริง... ไม่ต้องไปร้านนวดอีกเลย!", estimated_retention_3s=91.0)
            ],
            recommended_cta_th="พิกัดอยู่ในตะกร้าซ้ายมือ จัดโปรลดราคาพิเศษเหลือ ฿690 เฉพาะในไลฟ์/คลิปนี้เท่านั้น!"
        )
    else:
        # Generic high-performing template
        return ProductIntelligenceCard(
            product_id=product.id,
            product_summary_th=f"{product.title_th} สินค้าขายดี {product.total_sales:,} ชิ้น ค่าคอม {product.commission_rate}% กำไรดี ปิดการขายง่าย",
            target_audience_th="ผู้ใช้งานโซเชียลมีเดียในไทยที่ชอบสินค้าไลฟ์สไตล์ สะดวกสบาย คุ้มค่า คุ้มราคา",
            customer_pain_points=[
                PainPoint(issue_th="เสียเวลากับปัญหาจุกจิกในชีวิตประจำวัน", emotional_trigger="ความหงุดหงิด ต้องการความสะดวกรวดเร็ว"),
                PainPoint(issue_th="สินค้าเดิมที่ใช้อยู่พังง่าย ไม่ทนทาน", emotional_trigger="เสียดายเงินที่จ่ายไป")
            ],
            usp_th=[
                "วัสดุเกรดพรีเมียม ใช้งานได้ยาวนาน",
                "ดีไซน์ทันสมัย มินิมอล ใช้งานง่ายใน 1 นาที",
                f"ราคาพิเศษลดเหลือเพียง ฿{product.sale_price}"
            ],
            reasons_to_buy=[
                f"คะแนนรีวิวสูง {product.rating} ดาว จากผู้ใช้งานจริง",
                "การันตีความคุ้มค่า สินค้าส่งไวจากไทย"
            ],
            purchase_objections=[
                Objection(objection_th="ลังเลว่าจะได้ใช้บ่อยไหม", counter_argument_th="เป็นของใช้ประจำวัน ช่วยประหยัดเวลาได้ทุกวัน")
            ],
            competitor_comparison_th="ราคาถูกกว่าท้องตลาด 30-50% และคุณภาพวัสดุตรงปก ไม่จกตา",
            content_opportunities=[
                "คลิปแกะกล่อง Unboxing และทดลองใช้งานทันที",
                "คลิปเปรียบเทียบ ก่อน vs หลัง ใช้งาน"
            ],
            recommended_angles=[
                "1. Problem → Solution",
                "2. Price / Value Deal (ดีลเด็ดประจำวัน)"
            ],
            recommended_hooks=[
                HookTemplate(hook_type="DISCOVERY", hook_text_th="เพิ่งค้นพบไอเทมลับที่ทำให้ชีวิตง่ายขึ้น 10 เท่า!", estimated_retention_3s=88.0)
            ],
            recommended_cta_th="จิ้มตะกร้าสีเหลืองตรงนี้ด่วนๆ ก่อนของจะหมดสต็อกนะทุกคน!"
        )
