# create_tables.py
from app.database import Base, engine
from app.models.user import User
from app.models.email import Email
from app.models.event import Event

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print(Base.metadata.tables.keys())
