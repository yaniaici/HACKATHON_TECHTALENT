import ollama
import json
import logging
from typing import Dict, Any
import requests

class OllamaClient:
    def __init__(self, model_name: str = "llama2"):  # Cambiado de "phi" a "llama2"
        self.model_name = model_name
        self.base_url = "http://localhost:11434"
        self.timeout = 30  # Timeout de 30 segundos

    def generate_response(self, prompt: str, context: str = "") -> str:
        try:
            full_prompt = self._build_prompt(prompt, context)
            
            # Configuración ultra-rápida para respuestas < 1 minuto
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': self._get_system_prompt()
                    },
                    {
                        'role': 'user',
                        'content': full_prompt
                    }
                ],
                options={
                    'num_predict': 100,    # Reducido de 200 a 100 tokens
                    'temperature': 0.3,     # Reducido de 0.7 a 0.3 (más determinístico)
                    'top_p': 0.7,          # Reducido de 0.9 a 0.7
                    'repeat_penalty': 1.0,  # Sin penalización de repetición
                    'num_ctx': 512,         # Contexto limitado
                    'num_thread': 4,        # Usar 4 threads
                    'num_gpu': 1,           # Usar GPU si está disponible
                    'stop': ["\n\n", "###"] # Parar en saltos de línea
                }
            )
            return response['message']['content']
        except Exception as e:
            logging.error(f"Error al generar respuesta con Ollama: {e}")
            return "Lo siento, no puedo procesar tu consulta en este momento. Inténtalo de nuevo más tarde."
    
    def _get_system_prompt(self) -> str:
        return """Asistente del Marketplace Tarragona. Responde breve y directo en español."""
    
    def _build_prompt(self, user_query: str, context: str = "") -> str:
        return f"Contexto: {context}\nPregunta: {user_query}\nRespuesta:"
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión con Ollama
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            # Intentar hacer una consulta simple
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': 'Hola, ¿estás funcionando?'
                    }
                ]
            )
            return True
        except Exception as e:
            logging.error(f"Error al conectar con Ollama: {e}")
            return False 