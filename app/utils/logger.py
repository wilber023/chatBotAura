import logging
import sys

def setup_custom_logger(name: str):
    """
    Configura de manera profesional el Logger para la consola y archivo (opcional).
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar duplicar handlers si la función se llama varias veces
    if not logger.handlers:
        # Console Formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        
        logger.addHandler(ch)
        
    return logger

# Instancia global del logger para la app
logger = setup_custom_logger("AURA_AGENT")
