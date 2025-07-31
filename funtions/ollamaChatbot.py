import ollama
import json
import os

CONFIG_FILE = "config.json"

def cargar_configuracion():
    """Carga la configuración desde config.json."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Error al leer config.json. Usando configuración por defecto.")
    # Configuración por defecto si hay error
    return {
        "nombre_correo": "Usuario",
        "email": "",
        "datos_contacto": "",
        "modelo": "llama2",
        "temperatura": 0.7
    }

def chatbot(userQuestion):
    config = cargar_configuracion()

    nombre = config.get("nombre_correo", "Usuario")
    email = config.get("email", "")
    contacto = config.get("datos_contacto", "")
    modelo = config.get("modelo", "llama2")
    temperatura = config.get("temperatura", 0.7)

    prompt = f"""Eres un asistente profesional que redacta correos electrónicos para "{nombre}" en español.
Redacta un correo formal en respuesta a la siguiente solicitud o situación: 

El correo debe tener saludo, cuerpo del mensaje y despedida. y mi nombre "{nombre}"""

    response = ollama.generate(
        model=modelo,
        prompt=prompt,
        stream=False,
        options={"temperature": temperatura}
    )
    return response["response"]
