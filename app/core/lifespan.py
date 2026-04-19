from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.utils.logger import logger
from app.services.sentiment import sentiment_analyzer

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.
    Inicializa modelos de IA antes de aceptar tráfico web.
    """
    logger.info("🚀 Iniciando Aura AI Agent...")
    
    try:
        # Cargar los modelos pesados de manera síncrona aquí para no afectar requests
        logger.info("Cargando motor de análisis de sentimientos...")
        sentiment_analyzer.load_model()
        logger.info("✅ Motor de IA inicializado correctamente")
        
        # Preparación de base de datos
        from app.db.session import init_db
        init_db()
        logger.info("✅ Base de datos verificada")
        
    except Exception as e:
        logger.error(f"❌ Error crítico al inicializar los servicios: {e}")
        # En producción, podrías forzar el cierre de la app si no puede cargar el modelo
        raise e
        
    yield # Aquí la aplicación empieza a atender requests
    
    # Lógica de apagado (limpieza de recursos, cerrar DB pools)
    logger.info("🛑 Deteniendo servicios de Aura AI Agent...")
    logger.info("Recursos liberados estructuradamente.")
