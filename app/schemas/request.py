from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    """Estructura de la petición entrante del usuario."""
    post_text: str = Field(
        ...,
        min_length=1, 
        max_length=2000, 
        description="El texto proporcionado por el usuario para su análisis y respuesta.",
        examples=["Es la tercera vez que me fallan la entrega, necesito ayuda ya."]
    )
    user_id: Optional[str] = Field(
        default=None, 
        description="Identificador opcional del usuario para mantener el contexto."
    )
