import smtplib
from email.mime.text import MIMEText
import json
import os
from configuration import loadSettings

def sendMail():
    from App import layoutAnswer, layoutmail
    """
    Función para enviar un correo electrónico con la respuesta del chatbot.
    """
    try:
        config = loadSettings()
        # Antes de ocultar el frame:
        respuesta_guardada = layoutAnswer.get("1.0", "end-1c").strip()
        correo_guardado = layoutmail.get("1.0", "end-1c").strip()

    # Luego los usas en sendMail

        nombre_remitente = config.get("nombre_correo", "Usuario")
        remitente_email = config.get("email", "")
        password_smtp = config.get("contraseña", "")  

        respuesta_chatbot = layoutAnswer.get("1.0", "end-1c").strip()
        destinatario_email = layoutmail.get("1.0", "end-1c").strip()
        
        if not destinatario_email or not remitente_email or not respuesta_chatbot or not password_smtp:
            print("Error: Los campos de correo, nombre, contraseña o respuesta del chatbot están incompletos.")
            return

        asunto = "Respuesta de tu chatbot"
        cuerpo_mensaje = f"Hola,\n\n"
        cuerpo_mensaje += f"Aquí está la respuesta generada por el chatbot:\n\n"
        cuerpo_mensaje += f"{respuesta_chatbot}\n\n"
        cuerpo_mensaje += f"Saludos cordiales,\n{nombre_remitente}"
        
        msg = MIMEText(cuerpo_mensaje)
        msg["Subject"] = asunto
        msg["From"] = remitente_email
        msg["To"] = destinatario_email

        # Enviar el correo real
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remitente_email, password_smtp)
            server.send_message(msg)
        
        print("✅ Correo enviado correctamente a:", destinatario_email)
        print("Asunto:", asunto)
        print("Contenido:\n", cuerpo_mensaje)

    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
