from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.core.config import get_settings

settings = get_settings()

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """Verifica el API Key inyectado en el header de las peticiones protegidas."""
    if settings.ENVIRONMENT == "development":
        # En desarrollo, permitimos uso abierto o logs especiales si no viene key
        pass

    if api_key_header == settings.API_KEY_SECRET:
        return api_key_header
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail="Could not validate API KEY"
    )
