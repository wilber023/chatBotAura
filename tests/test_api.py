from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_endpoint_no_auth_provided_development():
    """Prueba que el chat responda bien cuando la app arranca en desarrollo aunque falte el API Key"""
    response = client.post(
        "/api/v1/chat",
        json={"post_text": "Este es un mensaje de prueba excelente."}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response_text" in data
    assert "ai_metadata" in data
    assert data["ai_metadata"]["sentiment_label"] in ["POSITIVO", "NEGATIVO", "NEUTRO"]

def test_chat_endpoint_with_auth_key():
    """Prueba que el chat valide la llave enviada"""
    response = client.post(
        "/api/v1/chat",
        json={"post_text": "Hola"},
        headers={"X-API-KEY": "super_secret_default_key"}
    )
    assert response.status_code == 200

def test_chat_endpoint_invalid_body():
    """Valida los chequeos de Pydantic en los request"""
    response = client.post(
        "/api/v1/chat",
        json={"wrong_field": "Hola"}
    )
    assert response.status_code == 422 # Unprocessable Entity
