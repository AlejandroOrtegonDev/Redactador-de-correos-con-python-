from tkinter import *
from tkinter import ttk
from funtions.ollamaChatbot import chatbot
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Text, WORD, END
from funtions.buttonSendInf import enviar
from funtions.sendEmail import sendMail
from funtions.deleteButom import reset
from configuration import mostrarConfiguracion, loadSettings

initial_settings = loadSettings()

ventana = ttk.Window(themename=initial_settings.get("tema", "superhero"))
ventana.title("Escritor correos")
ventana.geometry("500x650")
ventana.resizable(False, False)
ventana.iconbitmap("src/icon.ico")
navbar = ttk.Frame(ventana, padding=5)
navbar.pack(fill=X)

frame_principal = ttk.Frame(ventana)
frame_principal.pack(fill=BOTH, expand=True)

frame_chat = ttk.Frame(frame_principal)
frame_chat.pack(fill=BOTH, expand=True)

frame_config_instance = None

def abrir_configuracion():
    global frame_config_instance
    if frame_config_instance is None or not frame_config_instance.winfo_exists():
        frame_config_instance = mostrarConfiguracion(ventana, frame_principal, frame_chat, cerrar_configuracion)
    else:
        frame_config_instance.tkraise()

def cerrar_configuracion():
    global frame_config_instance
    if frame_config_instance is not None and frame_config_instance.winfo_exists():
        frame_config_instance.destroy()
        frame_config_instance = None
    frame_chat.pack(fill=BOTH, expand=True)

btn_config = ttk.Button(navbar, text="⚙️", bootstyle="info-outline", command=abrir_configuracion)
btn_config.pack(side=LEFT, padx=5)

common_width = 52

layoutAnswer = Text(frame_chat, state=DISABLED, wrap=WORD, width=common_width, height=15, font=("Segoe UI", 10))
layoutAnswer.pack(pady=10)

emaillayout_container = ttk.Frame(frame_chat)
emaillayout_container.pack(pady=5)

email_label = ttk.Label(emaillayout_container, text="Correo al cual desea enviar mensaje")
email_label.pack(anchor=W, padx=5)

emaillayout = ttk.Frame(emaillayout_container)
emaillayout.pack()

layoutmail = Text(emaillayout, wrap=WORD, width=common_width, height=2, font=("Segoe UI", 10))
layoutmail.pack(pady=5, padx=5)

layoutAsk = Text(frame_chat, wrap=WORD, width=common_width, height=4, font=("Segoe UI", 10))
layoutAsk.pack(pady=5)

button_container = ttk.Frame(frame_chat)
button_container.pack(pady=10)

boton = ttk.Button(button_container, text="generar", width=10, bootstyle="success-outline", command=lambda: enviar(layoutAsk, layoutAnswer))
boton.pack(side=LEFT, padx=5)

botonReset = ttk.Button(button_container, text="limpiar",width=10, bootstyle="danger-outline", command=lambda: reset(layoutAsk, layoutAnswer))
botonReset.pack(side=LEFT, padx=5)

botonSendMail = ttk.Button(frame_chat, text="Enviar correo", width=12, bootstyle="success", command=sendMail)
botonSendMail.pack(pady=10)

ventana.mainloop()
