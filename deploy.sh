#!/bin/bash

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Iniciando Despliegue Automatizado de ChatBot Aura${NC}"
echo "==================================================="

# 1. Verificación de Prerrequisitos
echo -e "\n${YELLOW}🔍 Verificando sistema...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no está instalado.${NC}"
    exit 1
fi
echo "✅ Python 3 detectado"

# 2. Configuración del Entorno Virtual
echo -e "\n${YELLOW}🛠️  Configurando entorno virtual...${NC}"

# Si el activador del venv no existe o no es ejecutable, recreamos el entorno.
if [ ! -x "venv/bin/activate" ]; then
    if [ -d "venv" ]; then
        echo "Entorno virtual existente parece corrupto o incompleto. Recreando..."
        rm -rf venv
    fi
    echo "Creando nuevo entorno virtual..."
    python3 -m venv venv
else
    echo "Entorno virtual detectado y es válido."
fi

# 3. Instalación de Dependencias
echo -e "\n${YELLOW}📦 Instalando/Actualizando dependencias...${NC}"

if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ No se encontró el archivo requirements.txt. No se pueden instalar las dependencias.${NC}"
    exit 1
fi

echo "Actualizando pip..."
./venv/bin/pip install --upgrade pip > /dev/null

if ./venv/bin/pip install -r requirements.txt; then
    echo -e "${GREEN}✅ Dependencias instaladas correctamente.${NC}"
else
    echo -e "${RED}❌ Error instalando dependencias.${NC}"
    exit 1
fi

# 4. Configuración de Variables de Entorno
echo -e "\n${YELLOW}⚙️  Verificando configuración...${NC}"
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "⚠️  No se encontró archivo .env. Creando uno desde .env.example..."
        cp .env.example .env
        echo -e "${YELLOW}⚠️  IMPORTANTE: Se ha creado un archivo .env por defecto.${NC}"
        echo -e "${YELLOW}   Por favor, edítalo si necesitas configurar tokens específicos.${NC}"
    else
        echo -e "${RED}❌ No se encontró .env ni .env.example.${NC}"
    fi
else
    echo "✅ Archivo .env detectado."
fi

# 5. Gestión del Proceso
echo -e "\n${YELLOW}🔄 Gestionando servicio...${NC}"

# Buscar y matar proceso anterior si existe (buscando uvicorn combined_api:app)
PID=$(pgrep -f "uvicorn combined_api:app")
if [ ! -z "$PID" ]; then
    echo "Deteniendo instancia anterior (PID: $PID)..."
    kill $PID
    sleep 2
fi

# 6. Ejecución
echo -e "\n${GREEN}🚀 Desplegando servicio...${NC}"
echo "El servicio se ejecutará en segundo plano (nohup)."
echo "Logs disponibles en: server.log"

nohup ./venv/bin/uvicorn combined_api:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

NEW_PID=$!
echo -e "${GREEN}✅ Servicio iniciado con PID: $NEW_PID${NC}"
echo -e "📍 API disponible en: http://localhost:8000"
echo -e "📄 Documentación: http://localhost:8000/docs"
echo "==================================================="
