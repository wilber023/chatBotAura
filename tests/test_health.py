from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Validar que el endpoint de estado general funciona correctamente."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Aura AI Agent" in data["app"]
