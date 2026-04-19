from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse, AIMetadata
from app.services.response_generator import response_generator
from app.api.deps import get_db
from app.db.models import ChatItem
from app.core.security import get_api_key
from app.utils.logger import logger
import uuid

api_router = APIRouter()

@api_router.post("/chat", response_model=ChatResponse)
async def process_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Recibe el texto del usuario, analiza su estado emocional 
    y genera una respuesta inteligente guardando el contexto.
    """
    logger.info(f"Procesando nueva petición - Auth Key Used: {'Yes' if api_key else 'No'}")
    
    session_id = request.user_id if request.user_id else str(uuid.uuid4())
    
    try:
        # Invocamos la Lógica de Negocio
        result = await response_generator.process_chat(request.post_text, session_id)
        
        # Persistencia (Log en Base de datos)
        chat_record = ChatItem(
            session_id=session_id,
            user_message=request.post_text,
            bot_response=result["response"],
            sentiment_label=result["metadata"]["sentiment_label"],
            sentiment_confidence=result["metadata"]["sentiment_confidence"]
        )
        db.add(chat_record)
        db.commit()
        
        # Ensamblar Respuesta Completa
        return ChatResponse(
            conversation_id=session_id,
            response_text=result["response"],
            ai_metadata=AIMetadata(**result["metadata"])
        )
    except Exception as e:
        logger.error(f"Error procesando la solicitud: {e}")
        raise HTTPException(status_code=500, detail="Error interno en el motor de IA.")
