# 🌟 AURA AI Agent
**AURA (Análisis de Reconexión Humana Asistida)**

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

AURA es un agente conversacional avanzado diseñado específicamente para brindar **atención inteligente, empática y contextual**. Combina un profundo procesamiento de lenguaje natural (mediante Análisis de Sentimientos con Transformers) con una orquestación robusta usando una arquitectura limpia (*Clean Architecture*) orientada a microservicios.

Un motor de nivel empresarial, construido para ser escalable, seguro e integrarse transparentemente en ecosistemas backend modernos.

---

## 🚀 Arquitectura del Sistema

El sistema implementa separación de responsabilidades estricta para garantizar mantenibilidad a largo plazo:

- 🛡️ **Routing & API (`app/api`):** Punto principal de entrada. Exposición de rutas, validación de schemas con Pydantic y seguridad de acceso mediante inyección de dependencias.
- 🧠 **Services (`app/services`):** El "Cerebro" de AURA. Orquesta el análisis inferencial mediante RoBERTa (asíncrono) y genera respuestas dinámicas empáticas.
- ⚙️ **Core (`app/core`):** Inicialización global, gestión estructurada por variables de entorno y carga temprana de modelos IA en el ciclo de vida de la aplicación.
- 💾 **Persistence (`app/db`):** Interfaz robusta sobre SQLAlchemy para retener el contexto transaccional y el historial de comportamiento de las sesiones.

### 🌊 Flujo de Interacción
1. Recepción segura del **Input** en `POST /api/v1/chat`.
2. Validaciones de esquema y autenticación dinámica.
3. El `ResponseGenerator` inicia el proceso y registra el estado en la memoria volátil.
4. Delega la inferencia emocional a CPU/GPU mediante PyTorch.
5. Inyección condicional en el **LLM Service** o plantillas inteligentes dinámicas.
6. Commit automático en base de datos para seguimiento y análisis posterior.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología Principal |
| :--- | :--- |
| **Framework Web** | FastAPI + Uvicorn |
| **Inteligencia Artificial** | HuggingFace `Transformers` + `PyTorch` (`RoBERTa`) |
| **Validación de Datos** | Pydantic v2 + Pydantic Settings |
| **Persistencia** | SQLAlchemy (Compatible con PostgreSQL/MySQL/SQLite) |
| **Testing & CI** | Pytest + HTTPX |
| **Contenedores y Ops** | Docker Multi-Stage + Docker Compose |

---

## 📦 Despliegue Rápido (Desarrollo Local)

1. **Clona el repositorio e inicializa el entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # venv\Scripts\activate   # En Windows
   ```

2. **Instala las dependencias principales:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicia el Servidor con Auto-Reload:**
   ```bash
   bash scripts/start.sh
   ```
   > 📍 Tu API estará documentada e interactiva en: `http://localhost:8000/api/v1/docs`

---

## 🐳 Despliegue en Producción (Docker)

AURA está contenerizado listo para orquestación en la nube empleando las mejores prácticas de seguridad (non-root users). Ejecuta el entorno completo con un comando:

```bash
bash scripts/deploy.sh
```

---

## 🧪 Calidad y Pruebas Unitarias

Mantén la confiabilidad del código ejecutando la suite de Pytest (Asegúrate de que estás en tu entorno virtual):

```bash
pytest -v
```

---

<div align="center">
  <br>
  <i>Hecho por el equipo de AURA AI para el Agente de la APP AURA (Análisis de Reconexión Humana Asistida).</i>
</div>