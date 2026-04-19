import pytest
from app.services.sentiment import sentiment_analyzer

@pytest.mark.asyncio
async def test_sentiment_analysis_pipeline():
    """
    Test para validar si el servicio wrappea correctamente el modelo.
    Este test asumirá que los modelos están cargados en la fase de prueba local.
    """
    # Triggereamos de forma sincrona la inicialización manual en el entorno de pruebas
    sentiment_analyzer.load_model()
    
    result = await sentiment_analyzer.analyze_sentiment("Esto es horrible y detestable")
    
    assert "label" in result
    assert "confidence" in result
    assert result["label"] == "NEGATIVO"
    assert result["confidence"] > 0.5
