"""Funciones comunes de ayuda a lo largo de todo el código."""
import uuid

def generate_conversation_id() -> str:
    """Genera un UUID único para el rastreo de contexto."""
    return str(uuid.uuid4())

def sanitize_text(text: str) -> str:
    """Limpia el texto de entrada previniendo excesos de espacios u ocultamiento de inyecciones."""
    return " ".join(text.split()).strip()
