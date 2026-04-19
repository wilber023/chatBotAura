#!/bin/bash
# Script para levantar el entorno local en caliente (Hot Reload)

echo "🚀 Iniciando Aura AI Agent en modo Desarrollo..."

# Verifica si el ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "⚠️  No se encontró el entorno virtual 'venv'. Créalo e instala los 'requirements.txt'."
    exit 1
fi

source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

echo "Cargando Uvicorn..."
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
