# API de Respuesta Automática con Análisis de Sentimiento

API de FastAPI que combina análisis de sentimiento y generación de respuestas automáticas para atención al cliente.

## 🏗️ Arquitectura del Pipeline

El sistema funciona en tres etapas secuenciales:

1. **Clasificación de Sentimiento**: Utiliza RoBERTa para determinar si el texto es NEGATIVO, POSITIVO o NEUTRO
2. **Construcción del Prompt Condicional**: Genera instrucciones específicas según el sentimiento detectado
3. **Generación de Respuesta**: Un LLM genera la respuesta apropiada basándose en el prompt

## 🚀 Configuración del Entorno

### 1. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate  # En Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el servidor

```bash
uvicorn combined_api:app --reload
```

El servidor estará disponible en: `http://127.0.0.1:8000`

## 📚 Documentación de la API

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🧪 Ejemplo de Uso

### Solicitud POST a `/respuesta_automatica/`

```json
{
  "post_text": "Es la tercera vez que me fallan la entrega, su servicio es pésimo y necesito una solución YA."
}
```

### Respuesta

```json
{
  "sentimiento_detectado": "NEGATIVO",
  "confianza_sentimiento": 0.991,
  "respuesta_automatizada": "Lamentamos profundamente el inconveniente con su pedido. Entendemos completamente su frustración. Para poder revisar a fondo su caso y darle una solución inmediata, ¿podría facilitarnos su número de pedido o un contacto donde podamos comunicarnos directamente? Pedimos disculpas por las molestias.",
  "modelo_generacion": "dccuchile/bert-base-spanish-wwm-uncased"
}
```

## 🔧 Modelos Utilizados

- **Análisis de Sentimiento**: `UMUTeam/roberta-spanish-sentiment-analysis`
- **Generación de Texto**: `dccuchile/bert-base-spanish-wwm-uncased` (placeholder)

> **Nota**: Para producción, se recomienda usar un LLM más potente como Llama-3-8B o Mistral, que requiere más recursos computacionales.

## 📝 Estructura del Proyecto

```
chatbot-service/
├── combined_api.py       # API principal con el pipeline completo
├── requirements.txt      # Dependencias de Python
└── README.md            # Este archivo
```

## ⚠️ Consideraciones

- La primera ejecución descargará los modelos (puede tomar varios minutos)
- Los modelos grandes requieren suficiente RAM/VRAM
- Para producción, considera usar GPU para mejor rendimiento
# chatBotAura
