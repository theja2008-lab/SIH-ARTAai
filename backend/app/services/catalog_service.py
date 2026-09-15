import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.models import Catalog, CatalogField, PriceEstimate, Artwork, Artisan
from app.services.pricing_service import PricingService

class CatalogService:
    """
    Catalog Engine — Builds dynamic product catalogs, tracks field provenance
    (ARTISAN, AI_VISION, AI_INFERENCE, AI_GENERATED), handles corrections and approvals.
    """

    @classmethod
    def create_catalog_from_voice_and_vision(
        cls,
        db: Session,
        artisan_id: str,
        artwork_id: str,
        extracted_data: Dict[str, Any],
        vision_data: Dict[str, Any]
    ) -> Catalog:
        """
        Synthesizes artisan voice input and vision analysis into a structured catalog with field provenance.
        """
        artisan = db.query(Artisan).filter(Artisan.id == artisan_id).first()
        exp = artisan.experience_years if artisan else 25

        catalog_id = f"CAT-{uuid.uuid4().hex[:6].upper()}"
        
        product_name = extracted_data.get(
            "product_name", vision_data.get("suggested_product_name", "Handcarved Teak Sculpture")
        )
        craft_category = extracted_data.get(
            "craft_category", vision_data.get("craft_category", "Traditional Wood Craft")
        )
        primary_material = extracted_data.get(
            "primary_material", vision_data.get("detected_material", "Teak Wood")
        )
        work_hours = extracted_data.get("work_hours", 20)
        description = extracted_data.get(
            "description", "Handcrafted traditional item made with fine craftsmanship."
        )
        cultural_sig = extracted_data.get(
            "cultural_significance", "Traditional heritage craft technique."
        )

        # Estimate price
        pricing = PricingService.calculate_fair_price(
            craft_category=craft_category,
            material=primary_material,
            work_hours=work_hours,
            experience_years=exp
        )

        catalog = Catalog(
            id=catalog_id,
            artisan_id=artisan_id,
            artwork_id=artwork_id,
            product_name=product_name,
            craft_category=craft_category,
            subcategory=extracted_data.get("subcategory", "Sculpture"),
            primary_material=primary_material,
            work_hours=work_hours,
            production_days=extracted_data.get("production_days", 3),
            description=description,
            cultural_significance=cultural_sig,
            price_amount=pricing["recommended_price"],
            status="DRAFT"
        )
        db.add(catalog)
        db.flush()

        # Add Field Provenance entries
        fields_config = [
            ("product_name", product_name, "ARTISAN" if "product_name" in extracted_data else "AI_GENERATED", "CONFIRMED" if "product_name" in extracted_data else "SUGGESTED"),
            ("craft_category", craft_category, "AI_VISION", "SUGGESTED"),
            ("primary_material", primary_material, "ARTISAN" if "primary_material" in extracted_data else "AI_VISION", "CONFIRMED"),
            ("work_hours", str(work_hours), "ARTISAN", "CONFIRMED"),
            ("experience_years", str(exp), "ARTISAN", "CONFIRMED"),
            ("description", description, "AI_GENERATED", "SUGGESTED"),
            ("price_amount", f"₹{int(pricing['recommended_price']):,}", "AI_INFERENCE", "SUGGESTED")
        ]

        for fname, fval, fsource, fstatus in fields_config:
            cfield = CatalogField(
                catalog_id=catalog_id,
                field_name=fname,
                field_value=fval,
                source=fsource,
                status=fstatus,
                confirmed_by_artisan=(fsource == "ARTISAN")
            )
            db.add(cfield)

        # Add PriceEstimate record
        price_rec = PriceEstimate(
            catalog_id=catalog_id,
            suggested_min=pricing["suggested_min"],
            suggested_max=pricing["suggested_max"],
            recommended_price=pricing["recommended_price"],
            final_price=pricing["recommended_price"],
            factor_breakdown=pricing["factor_breakdown"],
            explanation_ta=pricing["explanation_ta"],
            explanation_en=pricing["explanation_en"]
        )
        db.add(price_rec)

        db.commit()
        db.refresh(catalog)
        return catalog

    @classmethod
    def correct_catalog_field(
        cls,
        db: Session,
        catalog_id: str,
        field_name: str,
        new_value: Any,
        source: str = "ARTISAN"
    ) -> Catalog:
        """
        Applies a natural voice correction override to a catalog field.
        """
        catalog = db.query(Catalog).filter(Catalog.id == catalog_id).first()
        if not catalog:
            raise ValueError("Catalog not found")

        if field_name in ["price_amount", "price"]:
            catalog.price_amount = float(new_value)
            if catalog.price_estimate:
                catalog.price_estimate.final_price = float(new_value)
        elif hasattr(catalog, field_name):
            setattr(catalog, field_name, new_value)

        # Update field provenance status
        field_rec = db.query(CatalogField).filter(
            CatalogField.catalog_id == catalog_id,
            CatalogField.field_name == field_name
        ).first()

        if field_rec:
            field_rec.field_value = str(new_value)
            field_rec.source = source
            field_rec.status = "CONFIRMED"
            field_rec.confirmed_by_artisan = True
        else:
            new_f = CatalogField(
                catalog_id=catalog_id,
                field_name=field_name,
                field_value=str(new_value),
                source=source,
                status="CONFIRMED",
                confirmed_by_artisan=True
            )
            db.add(new_f)

        db.commit()
        db.refresh(catalog)
        return catalog
