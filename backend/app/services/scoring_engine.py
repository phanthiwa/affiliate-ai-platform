from typing import List
from app.models.schemas import (
    ProductBase, ProductWithScores, ScoringWeights, OpportunityClassification
)

def calculate_product_scores(
    product: ProductBase, 
    weights: ScoringWeights = ScoringWeights()
) -> ProductWithScores:
    # 1. Demand Score (0 - 100)
    # Velocity > 500 sales/day is 100 score
    velocity_score = min(100.0, (product.daily_sales_velocity / 600.0) * 100.0)
    monthly_score = min(100.0, (product.monthly_sales / 20000.0) * 100.0)
    demand_score = round(velocity_score * 0.6 + monthly_score * 0.4, 1)

    # 2. Growth / Trend Momentum (0 - 100)
    # 7-day growth > 40% is high momentum
    growth_score = min(100.0, max(0.0, (product.growth_rate_7d / 50.0) * 100.0))
    trend_score = round(growth_score, 1)

    # 3. Commission Appeal Score (0 - 100)
    # Commission rate >= 25% is max, or estimated THB commission >= 100 THB
    rate_score = min(100.0, (product.commission_rate / 25.0) * 100.0)
    thb_score = min(100.0, (product.estimated_commission / 100.0) * 100.0)
    commission_score = round(rate_score * 0.5 + thb_score * 0.5, 1)

    # 4. Review Quality Score (0 - 100)
    # Rating 4.9+ and > 5,000 reviews
    rating_norm = max(0.0, (product.rating - 4.0) / 1.0) * 100.0  # 4.0 to 5.0 scale
    review_vol_norm = min(100.0, (product.review_count / 15000.0) * 100.0)
    review_quality_score = round(min(100.0, rating_norm * 0.7 + review_vol_norm * 0.3), 1)

    # 5. Price Attractiveness (Sweet spot for Thai TikTok/Shopee impulse buys: 150 - 700 THB)
    if 120.0 <= product.sale_price <= 690.0:
        price_attractiveness_score = 95.0
    elif product.sale_price < 120.0:
        price_attractiveness_score = 85.0  # low ticket, low margin
    else:
        price_attractiveness_score = 70.0  # higher ticket, needs longer consideration
    if product.discount_pct >= 40.0:
        price_attractiveness_score = min(100.0, price_attractiveness_score + 5.0)

    # 6. Competition Inverse Score (Lower competition index = higher score)
    competition_score = round(max(0.0, 100.0 - product.competition_index), 1)

    # 7. Content Potential Score (High visual demo potential for video formats)
    category_visual_scores = {
        "Skincare / Beauty": 94.0,
        "Home & Living / Kitchen": 92.0,
        "Health & Wellness / Gadgets": 95.0,
        "Tech Gadgets / Creator Gear": 90.0,
        "Home & Living / Cleaning": 96.0,
        "Tech Gadgets / Mobile Accessories": 80.0
    }
    content_potential_score = category_visual_scores.get(product.category, 85.0)

    # Calculate Weighted Opportunity Score
    total_weights = (
        weights.demand + weights.growth + weights.commission + 
        weights.review_quality + weights.price_attractiveness + 
        weights.competition + weights.content_potential + weights.trend_momentum
    )
    
    raw_opp_score = (
        (demand_score * weights.demand) +
        (growth_score * weights.growth) +
        (commission_score * weights.commission) +
        (review_quality_score * weights.review_quality) +
        (price_attractiveness_score * weights.price_attractiveness) +
        (competition_score * weights.competition) +
        (content_potential_score * weights.content_potential) +
        (trend_score * weights.trend_momentum)
    ) / total_weights

    opportunity_score = round(raw_opp_score, 1)

    # Classification
    if opportunity_score >= 82.0:
        classification = OpportunityClassification.HIGH_PRIORITY
    elif opportunity_score >= 72.0:
        classification = OpportunityClassification.TEST
    elif opportunity_score >= 60.0:
        classification = OpportunityClassification.WATCH
    else:
        classification = OpportunityClassification.KILL

    # Generate AI Reasons
    ai_reasons = []
    if product.growth_rate_7d >= 30.0:
        ai_reasons.append(f"ยอดความต้องการ 7 วันล่าสุดพุ่งขึ้น +{product.growth_rate_7d:.1f}%")
    if product.commission_rate >= 20.0:
        ai_reasons.append(f"ค่าคอมมิชชั่นสูง {product.commission_rate:.0f}% (รับ ~฿{product.estimated_commission:.2f}/ออเดอร์)")
    if product.competition_index <= 40.0:
        ai_reasons.append("ระดับการแข่งขันในตลาดนายหน้ายังต่ำ โอกาสติดฟีดง่าย")
    if product.rating >= 4.85:
        ai_reasons.append(f"รีวิวดีเยี่ยม {product.rating} ดาว ปิดการขายง่าย ลดอัตราตีกลับ")

    top_angles = {
        "Skincare / Beauty": "Before/After + ปัญหาผิวเป็นสิวซ้ำซาก",
        "Home & Living / Kitchen": "สาธิตการใช้งานจริง 5 วินาที + เทียบกับวิธีเดิม",
        "Health & Wellness / Gadgets": "POV มนุษย์เงินเดือนปวดคอบ่าไหล่ + รีวิวประคบอุ่น",
        "Tech Gadgets / Creator Gear": "ป้ายยาสายทำคลิป/ไลฟ์สด + ไม่ต้องง้อคนช่วยถ่าย",
        "Home & Living / Cleaning": "คลิปทำความสะอาดแบบ Satisfying ชวนดูจบ"
    }

    return ProductWithScores(
        **product.model_dump(),
        demand_score=demand_score,
        trend_score=trend_score,
        competition_score=competition_score,
        content_potential_score=content_potential_score,
        opportunity_score=opportunity_score,
        classification=classification,
        ai_reasons=ai_reasons,
        top_recommended_angle=top_angles.get(product.category, "Problem → Solution")
    )

def score_product_catalog(
    products: List[ProductBase], 
    weights: ScoringWeights = ScoringWeights()
) -> List[ProductWithScores]:
    scored = [calculate_product_scores(p, weights) for p in products]
    # Sort descending by opportunity score
    scored.sort(key=lambda x: x.opportunity_score, reverse=True)
    return scored
