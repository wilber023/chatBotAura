#!/bin/bash
# Script para iniciar la API en producción usando Docker Compose

export ENVIRONMENT="production"

echo "==========================================="
echo "🚀 Desplegando AURA AI Agent en Producción"
echo "==========================================="

echo "📦 Construyendo y levantando contenedores..."
docker-compose down
docker-compose up -d --build

echo ""
echo "✅ Despliegue exitoso."
echo "📜 Puedes ver los logs con: docker-compose logs -f aura_api"
echo "📍 API escuchando en el puerto 8000"
