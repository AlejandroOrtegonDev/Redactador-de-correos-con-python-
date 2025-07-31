from funtions.ollamaChatbot import chatbot

# esta funcion es para el boton botonSend

def enviar(layoutAsk, layoutAnswer):
 
    entrada = layoutAsk.get("1.0", "end").strip()
    if entrada:
        layoutAnswer.config(state="normal")
        respuesta = chatbot(entrada)
        layoutAnswer.insert("end", f"Tú: {entrada}\nBot: {respuesta}\n\n")
        layoutAnswer.config(state="disabled")
        layoutAsk.delete("1.0", "end")