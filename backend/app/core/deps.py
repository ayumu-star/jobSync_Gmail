# backend/app/core/deps.py

from typing import Generator

from fastapi import HTTPException, status
from starlette.requests import Request

# ★ ここがポイント：database.py の get_db をそのまま再利用する
from app.database import get_db as _get_db


# --------------------------
# DB セッション依存性
# --------------------------
def get_db() -> Generator:
    """
    app.database.get_db をそのままラップして、
    他のモジュールからは app.core.deps.get_db を使うようにする。
    """
    yield from _get_db()


# --------------------------
# セッションから user_id を取り出す
# （gmail.py で使われている）
# --------------------------
def get_current_user_id(request: Request) -> int:
    """
    セッションに保存された user_id を取得する。
    ログインしていなければ 401 を返す。
    """
    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return user_id


# --------------------------
# （オプション）User オブジェクトを直接使いたい場合
# events.py で current_user を受け取るために使う想定
# --------------------------
def get_current_user_id(request: Request) -> str:
    """
    セッションから google_id を取り出してユーザーIDとして返す
    """
    user_id = request.session.get("google_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ログインしてください",
        )

    return user_id

