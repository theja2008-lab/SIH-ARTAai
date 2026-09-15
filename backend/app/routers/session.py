import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import ConversationSession, ConversationMessage, Artisan
from app.schemas.dto import SessionStartRequest, SessionResponse
from app.services.arta_service import ArtaService

router = APIRouter(prefix="/session", tags=["session"])

@router.post("/start", response_model=SessionResponse)
def start_session(req: SessionStartRequest, db: Session = Depends(get_db)):
    session_id = f"SES-{uuid.uuid4().hex[:6].upper()}"
    
    session = ConversationSession(
        id=session_id,
        current_state="LANGUAGE_SELECTION",
        language=req.language,
        collected_data={}
    )
    db.add(session)
    
    arta_prompt = ArtaService.get_arta_prompt("LANGUAGE_SELECTION", req.language)
    
    msg = ConversationMessage(
        session_id=session_id,
        sender="ARTA",
        message_text=arta_prompt["arta_text"],
        language=req.language
    )
    db.add(msg)
    db.commit()
    db.refresh(session)
    
    return SessionResponse(
        session_id=session.id,
        current_state=session.current_state,
        language=session.language,
        collected_data=session.collected_data or {},
        arta_message=arta_prompt["arta_text"]
    )

@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(ConversationSession).filter(ConversationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    arta_prompt = ArtaService.get_arta_prompt(session.current_state, session.language)
    
    return SessionResponse(
        session_id=session.id,
        current_state=session.current_state,
        language=session.language,
        collected_data=session.collected_data or {},
        arta_message=arta_prompt["arta_text"]
    )
