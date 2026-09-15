from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import ConversationSession
from app.schemas.dto import DemoIdentityRequest, DemoIdentityResponse
from app.services.identity_service import IdentityVerificationService, DemoIdentityVerificationService

router = APIRouter(prefix="/identity", tags=["identity"])

@router.post("/verify-demo", response_model=DemoIdentityResponse)
def verify_demo_identity(req: DemoIdentityRequest, db: Session = Depends(get_db)):
    session = db.query(ConversationSession).filter(ConversationSession.id == req.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    collected = session.collected_data or {}
    provided_name = collected.get("name", "Artisan")

    result = IdentityVerificationService.process_identity_document(
        provided_name=provided_name,
        document_type=req.document_type,
        image_b64=req.image_b64
    )

    collected["identity_verified"] = False
    collected["identity_status"] = "DOCUMENT_ATTACHED"
    collected["identity_document_type"] = req.document_type
    session.collected_data = collected
    session.current_state = "USER_PHOTO_CAPTURE"

    db.commit()

    arta_msg = result["arta_response_ta"] if session.language == "ta" else result["arta_response_en"]

    return DemoIdentityResponse(
        verified=result["verified"],
        extracted_name=result["extracted_name"],
        match_confidence=result["match_confidence"],
        status=result["status"],
        arta_response=arta_msg
    )
