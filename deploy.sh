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

# Determinar el gestor de paquetes y el paquete venv específico de la versión
PKG_MANAGER="apt-get"
if command -v apt &> /dev/null; then
    PKG_MANAGER="apt"
fi
PYTHON_VERSION_MAJOR_MINOR=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
VENV_PACKAGE="python${PYTHON_VERSION_MAJOR_MINOR}-venv"

if ! python3 -c "import venv" &> /dev/null; then
    echo -e "${RED}❌ El módulo 'venv' de Python no está instalado (se necesita el paquete '${VENV_PACKAGE}').${NC}"
    read -p "¿Deseas que el script intente instalarlo usando 'sudo'? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        echo "Intentando instalar '${VENV_PACKAGE}' con '${PKG_MANAGER}'..."
        if sudo ${PKG_MANAGER} update && sudo ${PKG_MANAGER} install -y ${VENV_PACKAGE}; then
            echo -e "${GREEN}✅ '${VENV_PACKAGE}' instalado correctamente.${NC}"
        else
            echo -e "${RED}❌ Falló la instalación de '${VENV_PACKAGE}'. Por favor, instálalo manualmente.${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}Instalación cancelada. El script no puede continuar sin 'python3-venv'.${NC}"
        exit 1
    fi
fi

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

    # Verificar que el entorno se creó correctamente
    if [ ! -f "venv/bin/pip" ]; then
        echo -e "${RED}❌ Falló la creación del entorno virtual. Asegúrate de que '${VENV_PACKAGE}' está instalado.${NC}"
        exit 1
    fi
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
./venv/bin/pip install --upgrade pip > /dev/null 2>&1

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
