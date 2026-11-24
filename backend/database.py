import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.sql import func

# On Vercel serverless, root filesystem is read-only; use /tmp for sqlite
if os.environ.get("VERCEL"):
    DATABASE_URL = "sqlite:////tmp/credang.db"
else:
    DATABASE_URL = "sqlite:///./credang.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id              = Column(Integer, primary_key=True)
    email           = Column(String, unique=True, index=True, nullable=False)
    name            = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    google_id       = Column(String, nullable=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

class EmailLog(Base):
    __tablename__ = "email_logs"
    id              = Column(Integer, primary_key=True)
    user_id         = Column(Integer, nullable=False)
    recipient_name  = Column(String)
    recipient_email = Column(String)
    subject         = Column(Text)
    body            = Column(Text)
    status          = Column(String, default="queued")
    error_msg       = Column(Text, nullable=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    sent_at         = Column(DateTime(timezone=True), nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
