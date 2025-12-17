import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.settings import SESSION_SECRET_KEY
from app.api.auth import router as auth_router
from app.api.gmail import router as gmail_router
from app.api.events import router as events_router

app = FastAPI(title="JobSync API", version="0.1.0")

frontend = os.getenv("FRONTEND_BASE_URL", "").rstrip("/")  # ← 末尾/も事故りやすいので除去

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
if frontend:
    origins.append(frontend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    same_site="lax",
    https_only=True,
)

app.include_router(auth_router, prefix="/api")
app.include_router(gmail_router, prefix="/api")
app.include_router(events_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}
