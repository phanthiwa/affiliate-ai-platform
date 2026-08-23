from typing import List, Optional
import uuid
import datetime
from app.models.schemas import (
    ProductBase, BatchGenerationRequest, BatchGenerationResponse,
    GeneratedClipItem, VideoStatus, ScoringWeights
)
from app.data.thai_products_mock import SAMPLE_THAI_PRODUCTS
from app.services.scoring_engine import score_product_catalog
from app.agents.script_writer import generate_thai_script_for_product
from app.agents.storyboard_director import convert_script_to_storyboard
from app.providers.google_flow_provider import GoogleFlowVideoProvider

# Stock preview video URLs for realistic creator studio preview
STOCK_PREVIEW_VIDEOS = [
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyBlazes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"
]

PEAK_TIME_SLOTS_THAI = [
    "11:30 น. (ช่วงพักเที่ยง คนเริ่มไถฟีด)",
    "12:15 น. (พีคไถฟีดซื้อของ Shopee/TikTok)",
    "13:00 น. (ก่อนเริ่มงานบ่าย)",
    "18:30 น. (ช่วงเดินทางกลับบ้าน)",
    "19:45 น. (ช่วงทองหลังอาหารเย็น)",
    "20:30 น. (พีคช้อปปิ้งไลฟ์สด)",
    "21:15 น. (ช่วงผ่อนคลายก่อนนอน)",
    "22:00 น. (ดีลรอบดึก Flash Sale)"
]

def generate_daily_batch_clips(
    request: BatchGenerationRequest,
    weights: ScoringWeights = ScoringWeights()
) -> BatchGenerationResponse:
    # 1. Score catalog to find top products
    scored_products = score_product_catalog(SAMPLE_THAI_PRODUCTS, weights)
    
    # Filter products if requested, else select top 3 High Priority
    selected_products: List[ProductBase] = []
    if request.product_ids and len(request.product_ids) > 0:
        id_set = set(request.product_ids)
        selected_products = [p for p in SAMPLE_THAI_PRODUCTS if p.id in id_set]
    
    if not selected_products:
        # Pick top 3 highest opportunity products
        selected_products = scored_products[:3]

    target_count = request.target_clip_count or 15
    variants_per_product = max(1, target_count // len(selected_products))
    
    generated_items: List[GeneratedClipItem] = []
    scripts_with_shots = []

    clip_counter = 0
    for p_idx, prod in enumerate(selected_products):
        for angle_idx in range(variants_per_product):
            if len(generated_items) >= target_count:
                break

            dur = request.preferred_durations[clip_counter % len(request.preferred_durations)]
            script = generate_thai_script_for_product(prod, angle_index=angle_idx, duration_sec=dur)
            shots = convert_script_to_storyboard(script)
            script.storyboard_shots = shots
            scripts_with_shots.append((script, shots))

            time_slot = PEAK_TIME_SLOTS_THAI[clip_counter % len(PEAK_TIME_SLOTS_THAI)]
            preview_video = STOCK_PREVIEW_VIDEOS[clip_counter % len(STOCK_PREVIEW_VIDEOS)]

            item = GeneratedClipItem(
                clip_id=f"CLIP-TH-{datetime.datetime.now().strftime('%m%d')}-{clip_counter+1:02d}",
                product_id=prod.id,
                product_title_th=prod.title_th,
                product_thumbnail=prod.thumbnail_url,
                sale_price=prod.sale_price,
                commission_rate=prod.commission_rate,
                angle_type=script.angle_type,
                hook_text_th=script.hook_text_th,
                duration_sec=script.target_duration_sec,
                script=script,
                compliance={
                    "status": script.compliance_status,
                    "notes": script.compliance_notes or ["ผ่านเกณฑ์มาตรฐาน อย. และ สคบ. 100%"]
                },
                google_flow_ready=True,
                preview_video_url=preview_video,
                scheduled_time_slot_th=time_slot,
                status=VideoStatus.READY_FOR_REVIEW
            )
            generated_items.append(item)
            clip_counter += 1

    # Format Google Flow batch export
    flow_provider = GoogleFlowVideoProvider()
    google_flow_payload = flow_provider.export_batch_flow(scripts_with_shots)

    batch_id = f"BATCH-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"

    return BatchGenerationResponse(
        batch_id=batch_id,
        total_generated=len(generated_items),
        clips=generated_items,
        google_flow_payload=google_flow_payload,
        summary_message_th=f"สร้างชุดคอนเทนต์ประจำวัน {len(generated_items)} คลิปเรียบร้อยแล้ว พร้อมส่งต่อไปยัง Google Flow และตั้งเวลาโพสต์ช่วงเวลาทอง!"
    )
