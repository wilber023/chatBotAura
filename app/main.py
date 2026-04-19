from fastapi import FastAPI
from app.core.config import get_settings
from app.core.lifespan import lifespan
from app.api.routes import api_router

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A modern AI Agent API for sentimental analysis and chat responding.",
    lifespan=lifespan,
    docs_url=f"{settings.API_V1_STR}/docs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Integrar todos los endpoints de nuestra API en V1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["System"])
async def root():
    """Endpoint vital para comprobar el estado de los contenedores o Load Balancers."""
    return {"status": "ok", "app": settings.PROJECT_NAME, "version": settings.VERSION}
