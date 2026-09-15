import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import ConversationSession, Artisan, ConversationMessage
from app.schemas.dto import VoiceInputRequest, VoiceInputResponse
from app.services.extraction_service import ExtractionService
from app.services.arta_service import ArtaService

from sqlalchemy.orm.attributes import flag_modified

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

# Onboarding State Machine order
STATE_FLOW = [
    "LANGUAGE_SELECTION",
    "NAME_COLLECTION",
    "AGE_COLLECTION",
    "DOCUMENT_CAPTURE",
    "USER_PHOTO_CAPTURE",
    "EXPERIENCE_COLLECTION",
    "CRAFT_COLLECTION",
    "PROFILE_CONFIRMATION",
    "HOME"
]

@router.post("/voice-input", response_model=VoiceInputResponse)
def process_onboarding_voice(req: VoiceInputRequest, db: Session = Depends(get_db)):
    session = db.query(ConversationSession).filter(ConversationSession.id == req.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    collected = dict(session.collected_data or {})
    
    # Extract data from natural transcript
    extracted = ExtractionService.extract_onboarding_info(
        transcript=req.transcript,
        field_target=req.field_target or session.current_state.lower()
    )

    collected.update(extracted)
    session.collected_data = collected
    flag_modified(session, "collected_data")

    # Move state machine forward
    curr_idx = STATE_FLOW.index(session.current_state) if session.current_state in STATE_FLOW else 0
    next_idx = min(len(STATE_FLOW) - 1, curr_idx + 1)
    session.current_state = STATE_FLOW[next_idx]

    arta_info = ArtaService.get_arta_prompt(
        current_state=session.current_state,
        language=session.language,
        custom_params=collected
    )

    db.commit()
    db.refresh(session)

    return VoiceInputResponse(
        session_id=session.id,
        extracted_data=extracted,
        current_state=session.current_state,
        arta_response=arta_info["arta_text"],
        missing_fields=[],
        is_complete=(session.current_state in ["PROFILE_CONFIRMATION", "HOME"])
    )

@router.post("/confirm-profile")
def confirm_profile(session_id: str, db: Session = Depends(get_db)):
    session = db.query(ConversationSession).filter(ConversationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    data = session.collected_data or {}
    
    artisan_name = data.get("name")
    artisan_age = data.get("age")
    exp_years = data.get("experience_years", 0)
    craft = data.get("craft_expertise", "Handicrafts")

    if not artisan_name or not artisan_age:
        raise HTTPException(
            status_code=400,
            detail="Name and age must be provided by the user before confirming profile."
        )

    artisan_id = f"ART-{uuid.uuid4().hex[:6].upper()}"
    artisan = Artisan(
        id=artisan_id,
        name=artisan_name,
        age=int(artisan_age),
        preferred_language=session.language,
        experience_years=int(exp_years) if exp_years else 0,
        craft_expertise=craft,
        identity_status="DOCUMENT_ATTACHED"
    )
    
    db.add(artisan)
    session.artisan_id = artisan.id
    session.current_state = "HOME"
    db.commit()

    return {
        "status": "SUCCESS",
        "artisan_id": artisan.id,
        "name": artisan.name,
        "current_state": "HOME",
        "message": f"Artisan profile created for {artisan.name}."
    }
