# backend/gmail_service.py
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from fastapi import HTTPException
import base64
from email.utils import parsedate_to_datetime
from typing import List

from app.creds import load_credentials, save_token_to_db
from app.database import SessionLocal


# ============================
# 共通ヘルパ
# ============================

SCOPES = ["https://mail.google.com/"]


def get_header(headers, name: str):
    lname = name.lower()
    for h in headers:
        if h["name"].lower() == lname:
            return h["value"]
    return None


def base64_decode(data: str) -> str:
    return base64.urlsafe_b64decode(data).decode(errors="ignore")


def get_body(body: dict | None):
    if not body:
        return None
    if body.get("size", 0) > 0 and "data" in body:
        return base64_decode(body["data"])
    return None


def get_parts_body(body: dict):
    if (
        body.get("size", 0) > 0
        and "data" in body
        and body.get("mimeType") == "text/plain"
    ):
        return base64_decode(body["data"])
    return None


def get_parts(parts: list[dict]):
    for part in parts:
        if part.get("mimeType") == "text/plain":
            body = part.get("body", {})
            if "data" in body:
                b = base64_decode(body["data"])
                if b:
                    return b

        if "body" in part:
            b = get_parts_body(part["body"])
            if b:
                return b

        if "parts" in part:
            b = get_parts(part["parts"])
            if b:
                return b
    return None


def get_email_body(payload: dict):
    body = payload.get("body", {})
    body_data = get_body(body) if body.get("size", 0) > 0 else None

    parts_data = None
    if "parts" in payload:
        parts_data = get_parts(payload["parts"])

    return body_data if body_data is not None else parts_data


# ============================
# Credentials（DB版）
# ============================

def get_credentials(user_id: int) -> Credentials:
    """
    DB に保存された Gmail token から Credentials を取得。
    期限切れなら refresh → DB 更新。
    """
    try:
        creds = load_credentials(user_id)
    except Exception:
        raise HTTPException(status_code=401, detail="Gmail認証が必要です")

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        db = SessionLocal()
        try:
            save_token_to_db(user_id, creds.to_json())
        finally:
            db.close()

    return creds


# ============================
# Gmail メール取得
# ============================

def get_emails(user_id: int, max_results: int = 10) -> List[dict]:
    """
    指定ユーザーの Gmail からメールを取得して返す
    """
    creds = get_credentials(user_id)

    service = build("gmail", "v1", credentials=creds)

    messages = (
        service.users()
        .messages()
        .list(userId="me", maxResults=max_results)
        .execute()
        .get("messages", [])
    )

    email_list: List[dict] = []

    for message in messages:
        m_data = (
            service.users()
            .messages()
            .get(userId="me", id=message["id"])
            .execute()
        )

        headers = m_data["payload"]["headers"]
        body_text = get_email_body(m_data["payload"])

        email_list.append(
            {
                "id": message["id"],
                "date": get_header(headers, "date"),
                "from": get_header(headers, "from"),
                "to": get_header(headers, "to"),
                "subject": get_header(headers, "subject"),
                "snippet": m_data.get("snippet", ""),
                "body": body_text[:1000] if body_text else "",
            }
        )

    return email_list
