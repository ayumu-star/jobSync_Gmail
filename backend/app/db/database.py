# backend/app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 開発用に SQLite を使用（同じフォルダに app.db ができます）
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# SQLite で必要な設定
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
