# backend/app/api/events.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user_id
from app.schemas.event import EventRead
from app.models.event import Event
from app.services.gmail_sync import sync_gmail_messages

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/sync", response_model=list[EventRead])
def sync_events(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    Gmail からメールを同期して events を更新し、その一覧を返す
    """
    events = sync_gmail_messages(db, user_id)
    return events


@router.get("/", response_model=list[EventRead])
def list_events(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    現在登録されている予定一覧を返す
    """
    events = (
        db.query(Event)
        .filter(Event.user_id == user_id)
        .order_by(Event.start_at)
        .all()
    )
    return events

