from typing import List, Dict

class MemoryService:
    """
    Servicio para manejar el contexto (Short-term memory) de la conversacion.
    En un entorno real, interaccionaría con Redis o la base local de conversaciones.
    """
    def __init__(self):
        # Almacenamiento en memoria volátil (Mock)
        self._store = {}
        
    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self._store:
            self._store[session_id] = []
            
        self._store[session_id].append({"role": role, "content": content})
        
        # Mantener solo los últimos 10 mensajes
        if len(self._store[session_id]) > 10:
            self._store[session_id].pop(0)
            
    def get_context(self, session_id: str) -> List[Dict[str, str]]:
        return self._store.get(session_id, [])

memory_service = MemoryService()
