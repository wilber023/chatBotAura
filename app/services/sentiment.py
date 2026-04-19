import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import asyncio
from app.utils.logger import logger
from app.core.config import get_settings

settings = get_settings()

class SentimentAnalyzer:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.id_to_label = {0: "NEGATIVO", 1: "NEUTRO", 2: "POSITIVO"}
        self._is_loaded = False

    def load_model(self):
        """Carga sincrónicamente los modelos para inicializar la memoria."""
        if self._is_loaded: return
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(settings.SENTIMENT_MODEL_NAME)
            self.model = AutoModelForSequenceClassification.from_pretrained(settings.SENTIMENT_MODEL_NAME)
            self._is_loaded = True
        except Exception as e:
            logger.error(f"Error al cargar el modelo de sentimiento: {e}")
            raise e

    def _analyze_sync(self, text: str) -> dict:
        """Función bloqueante que realmente hace el cálculo en PyTorch"""
        if not self._is_loaded:
            raise RuntimeError("El modelo no está cargado. Llama a load_model() primero.")
            
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class_id = torch.argmax(probabilities).item()
        confidence = probabilities[0, predicted_class_id].item()
        sentiment_label = self.id_to_label.get(predicted_class_id, "DESCONOCIDO")
        
        return {
            "label": sentiment_label,
            "confidence": confidence
        }

    async def analyze_sentiment(self, text: str) -> dict:
        """
        Función asíncrona que mueve la inferencia a un threadpool
        para no bloquear el Event Loop de FastAPI.
        """
        return await asyncio.to_thread(self._analyze_sync, text)

# Instancia singleton
sentiment_analyzer = SentimentAnalyzer()
