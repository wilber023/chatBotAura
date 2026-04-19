from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class AIMetadata(BaseModel):
    sentiment_label: str
    sentiment_confidence: float
    model_used: str
    processing_time_ms: float

class ChatResponse(BaseModel):
    """Estructura de la respuesta enriquecida devuelta por la API."""
    conversation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    response_text: str
    ai_metadata: AIMetadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
