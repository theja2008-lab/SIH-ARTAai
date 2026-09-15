import math
from typing import Dict, Any

class PricingService:
    """
    Dedicated Fair Pricing Engine for Traditional Artisans.
    Computes transparent, reproducible pricing ranges based on labor, material, complexity,
    and artisan experience without opaque black-box AI hallucination.
    """
    
    # Base labor rate per hour for skilled traditional craft (INR)
    BASE_HOURLY_RATE = 180.0

    # Material cost indices per item (INR estimated base)
    MATERIAL_BASE_COST = {
        "teak wood": 1200.0,
        "teak": 1200.0,
        "wood": 800.0,
        "rosewood": 1600.0,
        "brass": 1400.0,
        "bronze": 1800.0,
        "clay": 300.0,
        "terracotta": 400.0,
        "silk": 1500.0,
        "cotton": 500.0,
        "marble": 2000.0
    }

    # Craft complexity multipliers
    COMPLEXITY_MULTIPLIER = {
        "low": 1.0,
        "medium": 1.25,
        "high": 1.5,
        "intricate": 1.8
    }

    @classmethod
    def calculate_fair_price(
        cls,
        craft_category: str,
        material: str,
        work_hours: int,
        experience_years: int,
        complexity: str = "high"
    ) -> Dict[str, Any]:
        """
        Computes suggested min, max, recommended price and factor breakdown.
        """
        hours = max(1, work_hours)
        exp = max(0, experience_years)
        
        # 1. Labor Factor
        labor_cost = hours * cls.BASE_HOURLY_RATE

        # 2. Material Factor
        mat_key = material.lower().strip() if material else "wood"
        mat_cost = cls.MATERIAL_BASE_COST.get(mat_key, 800.0)

        # 3. Complexity Multiplier
        comp_mult = cls.COMPLEXITY_MULTIPLIER.get(complexity.lower(), 1.4)

        # 4. Master Artisan Skill Premium (5% bonus per 5 years experience, max 40%)
        exp_bonus_percent = min(0.40, (exp // 5) * 0.05)
        skill_premium = (labor_cost + mat_cost) * exp_bonus_percent

        # Total Estimated Value
        raw_total = (labor_cost + mat_cost + skill_premium) * comp_mult

        # Fair Range calculation (±10% range rounded to nearest 100)
        recommended = round(raw_total / 100.0) * 100.0
        suggested_min = round((recommended * 0.90) / 100.0) * 100.0
        suggested_max = round((recommended * 1.10) / 100.0) * 100.0

        explanation_ta = (
            f"{hours} மணி நேர உழைப்பு (₹{int(labor_cost)}) + "
            f"{material} பொருள் (₹{int(mat_cost)}) + "
            f"{exp} வருட கைவினை அனுபவம் மற்றும் நுட்பமான வேலைப்பாடு. "
            f"பரிந்துரைக்கப்பட்ட நியாயமான விலை: ₹{int(suggested_min):,} - ₹{int(suggested_max):,}."
        )

        explanation_en = (
            f"{hours} hours labor (₹{int(labor_cost)}) + "
            f"{material} raw material (₹{int(mat_cost)}) + "
            f"{exp} years master craftsmanship experience. "
            f"Suggested fair price range: ₹{int(suggested_min):,} – ₹{int(suggested_max):,}."
        )

        return {
            "suggested_min": float(suggested_min),
            "suggested_max": float(suggested_max),
            "recommended_price": float(recommended),
            "factor_breakdown": {
                "labor_cost": float(labor_cost),
                "material_cost": float(mat_cost),
                "skill_premium": float(skill_premium),
                "complexity_multiplier": comp_mult,
                "work_hours": hours,
                "experience_years": exp
            },
            "explanation_ta": explanation_ta,
            "explanation_en": explanation_en
        }
