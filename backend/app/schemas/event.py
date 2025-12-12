# app/schemas/event.py
from datetime import datetime
from pydantic import BaseModel

class EventBase(BaseModel):
    company_name: str | None = None
    title: str
    event_type: str
    start_at: datetime
    end_at: datetime | None = None
    location: str | None = None
    memo: str | None = None
    source: str
    status: str

class EventRead(EventBase):
    id: int
    email_id: int | None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
