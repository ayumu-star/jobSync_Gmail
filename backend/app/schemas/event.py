# backend/app/schemas/event.py
from datetime import datetime
from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    start_at: datetime
    end_at: datetime | None = None
    location: str | None = None
    memo: str | None = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    location: str | None = None
    memo: str | None = None


class EventRead(EventBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
