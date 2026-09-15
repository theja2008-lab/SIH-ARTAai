import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import ConversationSession, Artwork
from app.schemas.dto import ArtworkUploadResponse
from app.services.vision_service import AiVisionService

router = APIRouter(prefix="/artworks", tags=["artworks"])

@router.post("/upload", response_model=ArtworkUploadResponse)
async def upload_artwork(
    session_id: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    session = db.query(ConversationSession).filter(ConversationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    artwork_id = f"ARTW-{uuid.uuid4().hex[:6].upper()}"
    image_url = f"/assets/images/sample_teak_carving.jpg" # Sample demo image path

    # Analyze artwork using Vision Service
    vision_result = AiVisionService.analyze_artwork(
        image_data="",
        filename=file.filename if file else "artwork.jpg"
    )

    artwork = Artwork(
        id=artwork_id,
        session_id=session_id,
        image_url=image_url,
        detected_craft=vision_result["craft_category"],
        detected_material=vision_result["detected_material"],
        detected_complexity=vision_result["apparent_complexity"],
        vision_raw_output=vision_result
    )
    db.add(artwork)
    
    session.current_state = "VOICE_DESCRIPTION"
    db.commit()

    return ArtworkUploadResponse(
        artwork_id=artwork.id,
        image_url=image_url,
        detected_craft=vision_result["craft_category"],
        detected_material=vision_result["detected_material"],
        detected_complexity=vision_result["apparent_complexity"]
    )
