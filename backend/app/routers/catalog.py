from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import ConversationSession, Artwork, Catalog, CatalogField, PriceEstimate, Artisan
from app.schemas.dto import (
    CatalogExtractRequest, CatalogResponse, CatalogFieldDTO, PriceEstimateDTO,
    CorrectFieldRequest, ApproveCatalogRequest
)
from app.services.extraction_service import ExtractionService
from app.services.catalog_service import CatalogService
from app.services.arta_service import ArtaService

router = APIRouter(prefix="/catalogs", tags=["catalogs"])

@router.post("/extract-from-voice", response_model=CatalogResponse)
def extract_catalog_from_voice(req: CatalogExtractRequest, db: Session = Depends(get_db)):
    session = db.query(ConversationSession).filter(ConversationSession.id == req.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    artwork = db.query(Artwork).filter(Artwork.id == req.artwork_id).first()
    vision_data = artwork.vision_raw_output if artwork else {}

    # Extract structured catalog data from artisan voice transcript
    extracted = ExtractionService.extract_catalog_info(
        transcript=req.transcript,
        vision_data=vision_data
    )

    artisan_id = session.artisan_id or "ART-0001"

    # Synthesize & build full catalog with provenance entries
    catalog = CatalogService.create_catalog_from_voice_and_vision(
        db=db,
        artisan_id=artisan_id,
        artwork_id=req.artwork_id,
        extracted_data=extracted,
        vision_data=vision_data
    )

    session.current_state = "ARTISAN_REVIEW"
    db.commit()

    fields_dto = [
        CatalogFieldDTO(
            field_name=f.field_name,
            field_value=f.field_value,
            source=f.source,
            status=f.status,
            confirmed_by_artisan=f.confirmed_by_artisan
        )
        for f in catalog.fields
    ]

    p_est = catalog.price_estimate
    price_dto = PriceEstimateDTO(
        suggested_min=p_est.suggested_min,
        suggested_max=p_est.suggested_max,
        recommended_price=p_est.recommended_price,
        factor_breakdown=p_est.factor_breakdown or {},
        explanation_ta=p_est.explanation_ta,
        explanation_en=p_est.explanation_en
    )

    return CatalogResponse(
        catalog_id=catalog.id,
        product_name=catalog.product_name,
        craft_category=catalog.craft_category,
        subcategory=catalog.subcategory,
        primary_material=catalog.primary_material,
        secondary_materials=catalog.secondary_materials,
        work_hours=catalog.work_hours,
        experience_years=catalog.artisan.experience_years if catalog.artisan else 25,
        description=catalog.description,
        cultural_significance=catalog.cultural_significance,
        fields=fields_dto,
        price_estimate=price_dto,
        status=catalog.status
    )

@router.post("/{catalog_id}/correct", response_model=CatalogResponse)
def correct_catalog_field(catalog_id: str, req: CorrectFieldRequest, db: Session = Depends(get_db)):
    catalog = CatalogService.correct_catalog_field(
        db=db,
        catalog_id=catalog_id,
        field_name=req.field_name,
        new_value=req.new_value,
        source=req.source
    )

    fields_dto = [
        CatalogFieldDTO(
            field_name=f.field_name,
            field_value=f.field_value,
            source=f.source,
            status=f.status,
            confirmed_by_artisan=f.confirmed_by_artisan
        )
        for f in catalog.fields
    ]

    p_est = catalog.price_estimate
    price_dto = PriceEstimateDTO(
        suggested_min=p_est.suggested_min,
        suggested_max=p_est.suggested_max,
        recommended_price=p_est.recommended_price,
        factor_breakdown=p_est.factor_breakdown or {},
        explanation_ta=p_est.explanation_ta,
        explanation_en=p_est.explanation_en
    )

    return CatalogResponse(
        catalog_id=catalog.id,
        product_name=catalog.product_name,
        craft_category=catalog.craft_category,
        subcategory=catalog.subcategory,
        primary_material=catalog.primary_material,
        secondary_materials=catalog.secondary_materials,
        work_hours=catalog.work_hours,
        experience_years=catalog.artisan.experience_years if catalog.artisan else 25,
        description=catalog.description,
        cultural_significance=catalog.cultural_significance,
        fields=fields_dto,
        price_estimate=price_dto,
        status=catalog.status
    )

@router.post("/{catalog_id}/approve")
def approve_catalog(catalog_id: str, db: Session = Depends(get_db)):
    catalog = db.query(Catalog).filter(Catalog.id == catalog_id).first()
    if not catalog:
        raise HTTPException(status_code=404, detail="Catalog not found")

    catalog.status = "READY_FOR_MARKET"
    db.commit()

    return {
        "status": "READY_FOR_MARKET",
        "catalog_id": catalog.id,
        "message": "Product catalog approved and ready for marketplace."
    }
