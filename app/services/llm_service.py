from app.utils.logger import logger
import random

class LLMService:
    """
    Servicio encargado de interactuar con un Large Language Model (ej. HuggingFace, OpenAI).
    Actualmente usa un fallback de templates en caso de que un LLM ruteado no esté disponible,
    emulando comportamientos según contexto y sentimiento.
    """
    
    def __init__(self):
        self.model_name = "Rule-Based-LLM-Stub"
        
    async def generate_response(self, text: str, sentiment: str, confidence: float) -> str:
        """Aquí en el futuro harás llamadas reales a transformers text-generation apis."""
        
        logger.info(f"Generando respuesta para text con sentimiento {sentiment}")
        
        if confidence < 0.5:
            return "Gracias por tu mensaje. Un agente humano revisará tu caso en breve para darte atención personalizada."
            
        templates = {
            "NEGATIVO": [
                "Lamentamos escuchar eso. Por favor, permítenos investigar a fondo lo que sucede.",
                "Entiendo perfectamente tu frustración. Estoy aquí para ayudarte a resolver este inconveniente.",
                "Siento mucho que estés de este modo. Vamos a solucionarlo juntos."
            ],
            "POSITIVO": [
                "¡Qué excelente noticia! Nos alegra mucho saber tu opinión positiva.",
                "¡Gracias por tus comentarios! Es genial leer que tuviste una buena experiencia.",
                "¡Nos reconforta saberlo! Seguimos a tu disposición."
            ],
            "NEUTRO": [
                "Gracias por compartir esa información. La hemos tomado en cuenta.",
                "Entendido. Si tienes alguna duda específica, no dudes en preguntarme.",
                "Mensaje recibido. ¿Hay algo más en lo que pueda apoyarte hoy?"
            ]
        }
        
        # Simulación de tiempo de generación
        import asyncio
        await asyncio.sleep(0.3)
        
        possible_responses = templates.get(sentiment, templates["NEUTRO"])
        return random.choice(possible_responses)

# Instancia singleton
llm_service = LLMService()
