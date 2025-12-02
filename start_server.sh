#!/bin/bash

# Script para iniciar el servidor de desarrollo
# Asegúrate de haber activado el entorno virtual primero

echo "🚀 Iniciando servidor de FastAPI..."
echo "📍 La API estará disponible en: http://127.0.0.1:8000"
echo "📚 Documentación Swagger UI: http://127.0.0.1:8000/docs"
echo ""
echo "⚠️  NOTA: La primera vez que ejecutes la API, descargará los modelos"
echo "   de HuggingFace. Esto puede tomar varios minutos."
echo ""

./venv/bin/uvicorn combined_api:app --reload --host 0.0.0.0 --port 8000
