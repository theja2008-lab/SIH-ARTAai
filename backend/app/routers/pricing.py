from fastapi import APIRouter, HTTPException
from app.services.pricing_service import PricingService

router = APIRouter(prefix="/pricing", tags=["pricing"])

@router.get("/estimate")
def get_price_estimate(
    craft_category: str = "Traditional Wood Craft",
    material: str = "Teak Wood",
    work_hours: int = 20,
    experience_years: int = 25,
    complexity: str = "high"
):
    result = PricingService.calculate_fair_price(
        craft_category=craft_category,
        material=material,
        work_hours=work_hours,
        experience_years=experience_years,
        complexity=complexity
    )
    return result
