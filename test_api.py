#!/usr/bin/env python3
"""
Script de prueba para la API de respuesta automática.
Envía ejemplos de posts con diferentes sentimientos y muestra las respuestas.
"""

import requests
import json

API_URL = "http://127.0.0.1:8000/respuesta_automatica/"

# Ejemplos de posts con diferentes sentimientos
test_cases = [
    {
        "nombre": "Caso Negativo",
        "post_text": "Es la tercera vez que me fallan la entrega, su servicio es pésimo y necesito una solución YA."
    },
    {
        "nombre": "Caso Positivo",
        "post_text": "¡Excelente servicio! La atención fue rapidísima y el producto llegó en perfectas condiciones. Muy recomendado."
    },
    {
        "nombre": "Caso Neutro",
        "post_text": "Recibí mi pedido hoy. Todo parece estar en orden."
    },
    {
        "nombre": "Caso Negativo 2",
        "post_text": "Llevo 2 horas esperando una respuesta del soporte. Esto es inaceptable."
    }
]

def test_api():
    """Prueba la API con diferentes casos de sentimiento."""
    print("=" * 80)
    print("🧪 PRUEBA DE API - Respuesta Automática con Análisis de Sentimiento")
    print("=" * 80)
    print()
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\n{'─' * 80}")
        print(f"📝 {test_case['nombre']} ({idx}/{len(test_cases)})")
        print(f"{'─' * 80}")
        print(f"Texto del cliente:")
        print(f"  \"{test_case['post_text']}\"")
        print()
        
        try:
            # Hacer la petición a la API
            response = requests.post(
                API_URL,
                json={"post_text": test_case['post_text']},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Resultado:")
                print(f"  🎭 Sentimiento: {result['sentimiento_detectado']}")
                print(f"  📊 Confianza: {result['confianza_sentimiento']:.2%}")
                print(f"  💬 Respuesta generada:")
                print(f"     \"{result['respuesta_automatizada']}\"")
                print(f"  🤖 Modelo: {result['modelo_generacion']}")
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"  {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se pudo conectar a la API")
            print("   Asegúrate de que el servidor esté ejecutándose en http://127.0.0.1:8000")
            break
        except requests.exceptions.Timeout:
            print("❌ Error: Timeout - La API tardó demasiado en responder")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    print()
    print("=" * 80)
    print("✨ Prueba completada")
    print("=" * 80)

if __name__ == "__main__":
    test_api()
