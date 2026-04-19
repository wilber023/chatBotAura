from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class ChatItem(Base):
    __tablename__ = "chat_history"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    session_id = Column(String, index=True, nullable=False)
    user_message = Column(String, nullable=False)
    bot_response = Column(String, nullable=False)
    sentiment_label = Column(String)
    sentiment_confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
