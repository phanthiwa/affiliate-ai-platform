from typing import List
from app.models.schemas import (
    DailyAIActionRecommendation, DashboardOverviewMetrics, ScoringWeights
)
from app.data.thai_products_mock import SAMPLE_THAI_PRODUCTS
from app.services.scoring_engine import score_product_catalog

def get_executive_daily_recommendations(weights: ScoringWeights = ScoringWeights()) -> List[DailyAIActionRecommendation]:
    scored = score_product_catalog(SAMPLE_THAI_PRODUCTS, weights)
    recs: List[DailyAIActionRecommendation] = []

    if len(scored) >= 1:
        top1 = scored[0]
        recs.append(DailyAIActionRecommendation(
            id="rec-001",
            priority="HIGH_PRIORITY",
            headline_th=f"🔥 สั่งทำวิดีโอ 5 คลิป สำหรับ '{top1.title_th[:25]}...'",
            reasoning_th=f"ความต้องการในตลาดพุ่งขึ้น +{top1.growth_rate_7d:.1f}% ใน 7 วัน และค่าคอมมิชชั่นสูง {top1.commission_rate:.0f}% แนะนำทดสอบมุมมอง Problem→Solution ด่วน!",
            recommended_product_id=top1.id,
            recommended_action="CREATE_BATCH_CLIPS",
            estimated_daily_gmv_potential=top1.sale_price * 120,
            badge_label="⚡ แนะนำสูงสุดวันนี้"
        ))

    if len(scored) >= 2:
        top2 = scored[1]
        recs.append(DailyAIActionRecommendation(
            id="rec-002",
            priority="SCALE_OPPORTUNITY",
            headline_th=f"📈 ขยายผลมุมมองใหม่สำหรับ '{top2.title_th[:25]}...'",
            reasoning_th="สินค้ามียอดขายมั่นคงและรีวิว 4.88 ดาว แนะนำทำคลิปสาย 'ป้ายยาโปรเด็ด' 5 คลิปสำหรับ Shopee Video",
            recommended_product_id=top2.id,
            recommended_action="SCALE_CAMPAIGN",
            estimated_daily_gmv_potential=top2.sale_price * 180,
            badge_label="🚀 โอกาสสเกลยอดขาย"
        ))

    if len(scored) >= 3:
        top3 = scored[2]
        recs.append(DailyAIActionRecommendation(
            id="rec-003",
            priority="HIGH_MARGIN",
            headline_th=f"💰 ไอเทมทำกำไรสูง '{top3.title_th[:25]}...'",
            reasoning_th=f"ค่าคอมมิชชั่นต่อออเดอร์สูงถึง ~฿{top3.estimated_commission:.2f} การแข่งขันยังต่ำ เหมาะสำหรับทำคลิปเจาะกลุ่มมนุษย์ออฟฟิศ 5 คลิป",
            recommended_product_id=top3.id,
            recommended_action="CREATE_HIGH_MARGIN_CLIPS",
            estimated_daily_gmv_potential=top3.sale_price * 60,
            badge_label="💎 ค่าคอมสูงสุด"
        ))

    return recs

def get_dashboard_metrics(weights: ScoringWeights = ScoringWeights()) -> DashboardOverviewMetrics:
    recs = get_executive_daily_recommendations(weights)
    return DashboardOverviewMetrics(
        total_gmv_thb=1482950.0,
        total_commission_thb=342890.0,
        total_orders=3840,
        total_views=1240500,
        avg_ctr_pct=4.82,
        avg_conversion_pct=5.41,
        daily_clips_target=15,
        daily_clips_produced_today=15,
        top_winning_hook_th="หน้าสดโนฟิลเตอร์ให้ดูเลย 7 วันก่อนกับวันนี้...",
        top_performing_angle="Problem → Solution (ปัญหาผิวเรื้อรัง)",
        daily_recommendations=recs
    )
