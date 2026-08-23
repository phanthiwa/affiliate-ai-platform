from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional
from app.models.schemas import (
    ProductWithScores, ScoringWeights, ProductIntelligenceCard,
    BatchGenerationRequest, BatchGenerationResponse, GoogleFlowBatchExport,
    DashboardOverviewMetrics, DailyAIActionRecommendation, PlatformEnum
)
from app.data.thai_products_mock import SAMPLE_THAI_PRODUCTS
from app.services.scoring_engine import score_product_catalog, calculate_product_scores
from app.agents.product_analyst import generate_product_intelligence_card
from app.agents.compliance_agent import check_and_sanitize_thai_script
from app.agents.executive_agent import get_dashboard_metrics, get_executive_daily_recommendations
from app.services.batch_engine import generate_daily_batch_clips

router = APIRouter(prefix="/api/v1")

@router.get("/dashboard/overview", response_model=DashboardOverviewMetrics)
def api_get_dashboard_overview():
    """Get high-level creator KPIs and 'What should I do today?' directives."""
    return get_dashboard_metrics()

@router.get("/recommendations/daily", response_model=List[DailyAIActionRecommendation])
def api_get_daily_recommendations():
    """Get actionable daily recommendations."""
    return get_executive_daily_recommendations()

@router.get("/products", response_model=List[ProductWithScores])
def api_list_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    platform: Optional[PlatformEnum] = Query(None, description="Filter by platform"),
    search: Optional[str] = Query(None, description="Search keyword in Thai or English"),
    min_commission: Optional[float] = Query(None, description="Min commission rate %"),
    demand_weight: float = 0.25,
    growth_weight: float = 0.15,
    commission_weight: float = 0.15,
    competition_weight: float = 0.10
):
    """List and score Thai affiliate products with configurable opportunity algorithm."""
    weights = ScoringWeights(
        demand=demand_weight,
        growth=growth_weight,
        commission=commission_weight,
        competition=competition_weight
    )
    scored = score_product_catalog(SAMPLE_THAI_PRODUCTS, weights)
    
    # Filter
    results = scored
    if category and category != "ALL":
        results = [p for p in results if category.lower() in p.category.lower()]
    if platform:
        results = [p for p in results if p.platform_source == platform]
    if search:
        search_lower = search.lower()
        results = [
            p for p in results 
            if search_lower in p.title_th.lower() or (p.title_en and search_lower in p.title_en.lower()) or any(search_lower in tag.lower() for tag in p.tags)
        ]
    if min_commission is not None:
        results = [p for p in results if p.commission_rate >= min_commission]

    return results

@router.get("/products/{product_id}/intelligence", response_model=ProductIntelligenceCard)
def api_get_product_intelligence(product_id: str):
    """Deep product analysis & 11-section intelligence card."""
    prod = next((p for p in SAMPLE_THAI_PRODUCTS if p.id == product_id), None)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return generate_product_intelligence_card(prod)

@router.post("/batch/generate-15-clips", response_model=BatchGenerationResponse)
def api_generate_daily_batch(request: BatchGenerationRequest = Body(...)):
    """Generate 10-15 high-converting Thai script/storyboard variants tailored for Google Flow."""
    return generate_daily_batch_clips(request)

@router.post("/content/batch-approve")
def api_batch_approve_clips(clip_ids: List[str] = Body(...)):
    """5-Minute rapid approval for 10-15 daily clips."""
    return {
        "status": "SUCCESS",
        "approved_count": len(clip_ids),
        "message_th": f"อนุมัติคอนเทนต์จำนวน {len(clip_ids)} คลิปเรียบร้อยแล้ว! ส่งต่อไปยังคิวโพสต์อัตโนมัติตามช่วงเวลาทอง",
        "clip_ids": clip_ids
    }

@router.post("/compliance/check")
def api_check_compliance(text: str = Body(..., embed=True)):
    """Validate and sanitize Thai scripts against FDA / OCPB rules."""
    status, sanitized, flags = check_and_sanitize_thai_script(text)
    return {
        "status": status,
        "original_text": text,
        "sanitized_text": sanitized,
        "flags": flags
    }

@router.get("/video/tts-audio")
async def api_get_tts_audio(text: str = Query(...), voice: str = Query("female")):
    """Synthesize natural Thai speech audio for video player."""
    from fastapi.responses import Response
    from app.services.video_factory import synthesize_thai_audio, VOICE_FEMALE, VOICE_MALE
    
    selected_voice = VOICE_MALE if voice == "male" else VOICE_FEMALE
    audio_bytes = await synthesize_thai_audio(text, selected_voice)
    if not audio_bytes:
        raise HTTPException(status_code=500, detail="Failed to synthesize Thai speech")
        
    return Response(content=audio_bytes, media_type="audio/mpeg")
