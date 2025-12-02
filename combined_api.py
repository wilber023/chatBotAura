from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# --- 1. CONFIGURACIÓN Y CARGA DE MODELOS ---

import random

# --- 1. CONFIGURACIÓN Y CARGA DE MODELOS ---

# Modelo de Análisis de Sentimiento (Clasificación)
# Mantenemos RoBERTa porque es rápido y preciso para la clasificación
SENTIMENT_MODEL_NAME = "UMUTeam/roberta-spanish-sentiment-analysis"
try:
    print(f"⏳ Cargando modelo de sentimiento: {SENTIMENT_MODEL_NAME}...")
    tokenizer_sent = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_NAME)
    model_sent = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_NAME)
    id_to_label = {0: "NEGATIVO", 1: "NEUTRO", 2: "POSITIVO"} 
    print(f"✅ Modelo de sentimiento cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar modelo de sentimiento: {e}")
    raise e

# --- 2. DEFINICIÓN DE ESTRUCTURAS DE DATOS ---

app = FastAPI(
    title="API de Respuesta Automática (Templates)",
    description="Clasifica el sentimiento y genera una respuesta rápida usando templates predefinidos.",
    version="3.0.0"
)

class ClientPost(BaseModel):
    """Estructura de la entrada del cliente."""
    post_text: str

class AutomatedResponse(BaseModel):
    """Estructura de la respuesta de la API."""
    sentimiento_detectado: str
    confianza_sentimiento: float
    respuesta_automatizada: str
    modelo_generacion: str = "Template-Based-System"

# --- 3. FUNCIONES AUXILIARES DE LA LÓGICA ---

def classify_sentiment(text: str) -> tuple[str, float]:
    """Clasifica el sentimiento usando el Modelo RoBERTa."""
    inputs = tokenizer_sent(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model_sent(**inputs)
        
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class_id = torch.argmax(probabilities).item()
    confidence = probabilities[0, predicted_class_id].item()
    sentiment_label = id_to_label.get(predicted_class_id, "DESCONOCIDO")
    
    return sentiment_label, confidence

def get_template_response(sentiment: str, confidence: float) -> str:
    """
    Selecciona una respuesta predefinida basada en el sentimiento.
    """
    
    # Templates de respuestas enfocados en salud emocional juvenil, abuso de sustancias y aislamiento
    templates = {
        "NEGATIVO": [
            "Siento mucho que estés pasando por esto. 😔 No estás solo/a. A veces hablar con alguien de confianza o un profesional puede hacer una gran diferencia. ¿Te gustaría que te comparta números de ayuda profesional?",
            "Entiendo que te sientas así, y es valiente reconocerlo. 💪 El aislamiento o el consumo pueden parecer salidas, pero hay formas más seguras de sanar. Aquí estamos para escucharte sin juzgar.",
            "Tu bienestar es lo más importante. Si sientes que la situación te sobrepasa, por favor busca apoyo inmediato. Hay personas capacitadas esperando para ayudarte a salir de este bache. 🤝",
            "Es normal sentirse abrumado a veces. Recuerda que este momento difícil no define tu futuro. 🌱 ¿Has intentado hablar con algún consejero o adulto de confianza sobre lo que sientes?"
        ],
        "POSITIVO": [
            "¡Qué bueno leer eso! 🎉 Reconocer tus logros y momentos buenos es clave para tu salud emocional. ¡Sigue cuidándote así!",
            "¡Esa es la actitud! 💪 Cada paso positivo cuenta, ya sea en superar hábitos o en conectar con otros. ¡Estamos orgullosos de tu progreso!",
            "¡Me alegra mucho que te sientas mejor! 🌟 Mantener esa conexión contigo mismo y con los demás es fundamental. ¡Sigue adelante!",
            "¡Excelente! Ver el lado positivo y buscar el bienestar es un gran superpoder. ✨ Sigue fortaleciendo esa red de apoyo y hábitos saludables."
        ],
        "NEUTRO": [
            "Gracias por compartirlo. Recuerda que cuidar tu mente es tan importante como cuidar tu cuerpo. 🧠 Si tienes dudas sobre salud emocional o consumo, aquí podemos orientarte.",
            "Te escuchamos. A veces solo necesitamos un espacio seguro para expresarnos. Si necesitas consejos sobre cómo manejar el estrés o la soledad, no dudes en preguntar. 🛡️",
            "Entendido. Si tú o alguien que conoces necesita información sobre prevención de adicciones o apoyo emocional, cuenta con nosotros. 🤝",
            "Gracias por tu mensaje. Mantenerse informado y conectado es vital. ¿Hay algún tema específico sobre bienestar juvenil del que te gustaría saber más? 📚"
        ]
    }
    
    # Selección de respuesta
    # Si la confianza es muy baja (< 50%), usamos una respuesta genérica de seguridad
    if confidence < 0.5:
        return "Gracias por tu mensaje. Un agente humano revisará tu caso en breve para darte la mejor atención."
        
    # Seleccionamos una respuesta aleatoria del grupo correspondiente
    possible_responses = templates.get(sentiment, templates["NEUTRO"])
    return random.choice(possible_responses)

# --- 4. ENDPOINT PRINCIPAL DEL PIPELINE ---

@app.post("/respuesta_automatica/", response_model=AutomatedResponse)
async def automated_response_pipeline(post: ClientPost):
    """
    Ejecuta el pipeline: Clasificación de sentimiento -> Selección de Template.
    """
    client_text = post.post_text
    
    # PASO 1: Clasificación de Sentimiento
    sentimiento, confianza = classify_sentiment(client_text)
    
    # PASO 2: Selección de Respuesta (Template)
    respuesta_generada = get_template_response(sentimiento, confianza)
    
    # Devolver la respuesta final
    return AutomatedResponse(
        sentimiento_detectado=sentimiento,
        confianza_sentimiento=confianza,
        respuesta_automatizada=respuesta_generada
    )
