from app.services.sentiment import sentiment_analyzer
from app.services.llm_service import llm_service
from app.services.memory_service import memory_service
import time

class ResponseGenerator:
    """Orquestador principal que une el análisis AI con los motores LLM y la memoria."""
    
    @staticmethod
    async def process_chat(text: str, session_id: str) -> dict:
        start_time = time.time()
        
        # 1. Guardar contexto del usuario
        memory_service.add_message(session_id, "user", text)
        
        # 2. Análisis del texto
        sentiment_result = await sentiment_analyzer.analyze_sentiment(text)
        sentiment_label = sentiment_result["label"]
        confidence = sentiment_result["confidence"]
        
        # 3. Generación de respuesta con contexto y sentimiento
        response_text = await llm_service.generate_response(
            text=text,
            sentiment=sentiment_label,
            confidence=confidence
        )
        
        # 4. Guardar salida en memoria
        memory_service.add_message(session_id, "assistant", response_text)
        
        end_time = time.time()
        elapsed_ms = (end_time - start_time) * 1000
        
        return {
            "response": response_text,
            "metadata": {
                "sentiment_label": sentiment_label,
                "sentiment_confidence": confidence,
                "model_used": llm_service.model_name,
                "processing_time_ms": elapsed_ms
            }
        }

# Objeto exportable
response_generator = ResponseGenerator()
