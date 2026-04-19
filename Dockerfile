# Etapa 1: Base Ligera
FROM python:3.11-slim as base

# Evitar escritura de bytecode y limpiar buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Etapa 2: Constructor (Builder)
FROM base as builder

# Instalar herramientas para compilar dependencias (ej: C++)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalar en un prefix para poder copiar fácilmente a producción
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa 3: Producción (Runtime)
FROM base as runtime

# Crear usuario no root para seguridad
RUN useradd -m -s /bin/bash appuser
WORKDIR /app

# Copiar paquetes de Python
COPY --from=builder /root/.local/ /home/appuser/.local/
ENV PATH=/home/appuser/.local/bin:$PATH

# Crear directorio de cache de HF con permisos y DB local (opcional)
RUN mkdir -p /app/huggingface_cache && chown -R appuser:appuser /app

# Copiar el código de la aplicación
COPY --chown=appuser:appuser . /app/

# Configurar variables de modelos
ENV HF_HOME=/app/huggingface_cache
ENV ENVIRONMENT=production

# Cambiar a usuario no privilegiado
USER appuser

# Exponer el puerto
EXPOSE 8000

# Descargar y cachear los modelos ANTES del inicio en producción (Opcional pero recomendado para evitar timeouts)
# RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; AutoTokenizer.from_pretrained('UMUTeam/roberta-spanish-sentiment-analysis'); AutoModelForSequenceClassification.from_pretrained('UMUTeam/roberta-spanish-sentiment-analysis')"

# Ejecutamos Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
