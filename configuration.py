import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar, IntVar, BooleanVar, W, LEFT, HORIZONTAL, Text, END
import json
import os

# Define the configuration file path
CONFIG_FILE = "config.json"

# Las variables de configuración de Tkinter ya NO son globales aquí.
# Serán inicializadas dentro de mostrarConfiguracion.

def loadSettings():
    """Loads configuration settings from a JSON file."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                settings = json.load(f)
                # Ensure new fields exist even if loaded from an older config file
                default_settings = getDefaultSettings()
                for key, value in default_settings.items():
                    if key not in settings:
                        settings[key] = value
                return settings
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {CONFIG_FILE}. Using default settings.")
            return getDefaultSettings()
    return getDefaultSettings()

def saveSettings(settings):
    """Saves configuration settings to a JSON file."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        print("✅ Configuración guardada en el archivo.")
    except IOError as e:
        print(f"Error: Could not save configuration to {CONFIG_FILE}. {e}")

def getDefaultSettings():
    """Returns a dictionary with default configuration settings."""
    return {
        "tema": "superhero",
        "fuente_size": 10,
        "auto_scroll": True,
        "sonido": True,
        "modelo": "llama2",
        "temperatura": 0.7,
        "email": "",
        "nombre_correo": "",
        "ruta_firma_png": "",
        "datos_contacto": ""
    }

def mostrarConfiguracion(mainWindow, mainFrame, chatFrame, onCloseCallback):

    chatFrame.pack_forget()

    configFrame = ttk.Frame(mainFrame)
    configFrame.pack(fill=BOTH, expand=True)


    currentSettings = loadSettings()

   
    themeVar = StringVar(value=currentSettings.get("tema", "superhero"))
    fontSize = IntVar(value=currentSettings.get("fuente_size", 10))
    autoScroll = BooleanVar(value=currentSettings.get("auto_scroll", True))
    notificationSound = BooleanVar(value=currentSettings.get("sonido", True))
    modelVar = StringVar(value=currentSettings.get("modelo", "llama2"))
    temperatureVar = ttk.DoubleVar(value=currentSettings.get("temperatura", 0.7))
    emailVar = StringVar(value=currentSettings.get("email", ""))
    nameVar = StringVar(value=currentSettings.get("nombre_correo", ""))
    PaswordMail = StringVar(value=currentSettings.get("PaswordMail", ""))
    signaturePathVar = StringVar(value=currentSettings.get("ruta_firma_png", ""))
    

    def goBackToChat():
        if onCloseCallback:
            onCloseCallback()
        else:
            configFrame.destroy()
            chatFrame.pack(fill=BOTH, expand=True)

    titleLabel = ttk.Label(configFrame, text="⚙️ Configuración", font=("Segoe UI", 16, "bold"))
    titleLabel.pack(pady=20)

    canvasWidget = ttk.Canvas(configFrame, height=300)
    scrollBar = ttk.Scrollbar(configFrame, orient="vertical", command=canvasWidget.yview)

    canvasWidget.pack(side="left", fill="both", expand=True, padx=(20, 0))
    scrollBar.pack(side="right", fill="y", padx=(0, 20))

    scrollableFrame = ttk.Frame(canvasWidget)

    scrollableFrame.bind(
        "<Configure>",
        lambda e: canvasWidget.configure(scrollregion=canvasWidget.bbox("all"))
    )

    canvasWidget.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvasWidget.configure(yscrollcommand=scrollBar.set)


    themeFrame = ttk.LabelFrame(scrollableFrame, text="🎨 Apariencia", padding=15)
    themeFrame.pack(fill=X, pady=10, padx=20)

    ttk.Label(themeFrame, text="Tema:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    themeCombo = ttk.Combobox(
        themeFrame,
        textvariable=themeVar,
        width=15,
        values=["superhero"]
    )
    themeCombo.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    def applyTheme(*args):
        mainWindow.config(themename=themeVar.get())

    themeVar.trace_add("write", applyTheme)

    modelFrame = ttk.LabelFrame(scrollableFrame, text="Modelo IA", padding=15)
    modelFrame.pack(fill=X, pady=10, padx=20)

    ttk.Label(modelFrame, text="Modelo:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    modelCombo = ttk.Combobox(modelFrame, textvariable=modelVar, width=15,
                                values=["llama3.2:1b", "tinyllama", "llama2", "vicuna"])
    modelCombo.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    ttk.Label(modelFrame, text="Temperatura:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
    tempScale = ttk.Scale(modelFrame, from_=0.1, to=1.0, orient=HORIZONTAL,
                           length=150, variable=temperatureVar) # Changed textvariable to variable
    tempScale.grid(row=1, column=1, padx=5, pady=5, sticky=W)

    tempLabel = ttk.Label(modelFrame, text=f"{temperatureVar.get():.1f}")
    tempLabel.grid(row=1, column=2, padx=5, pady=5, sticky=W)

    def updateTemp(val):
        tempLabel.config(text=f"{float(val):.1f}")

    tempScale.configure(command=updateTemp)

    emailFrame = ttk.LabelFrame(scrollableFrame, text="📧 Correo", padding=15)
    emailFrame.pack(fill=X, pady=10, padx=20)


    ttk.Label(emailFrame, text="Email:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    emailEntry = ttk.Entry(emailFrame, textvariable=emailVar, width=25)
    emailEntry.grid(row=0, column=1, padx=5, pady=5, sticky=W)


    ttk.Label(emailFrame, text="Contraseña Email:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
    passwordEntry = ttk.Entry(emailFrame, textvariable=PaswordMail, width=25, show="*")
    passwordEntry.grid(row=1, column=1, padx=5, pady=5, sticky=W)


    nameFrame = ttk.LabelFrame(scrollableFrame, text="nombre", padding=15)
    nameFrame.pack(fill=X, pady=10, padx=20)

    ttk.Label(nameFrame, text="nombre para el correo").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    nameEntry = ttk.Entry(nameFrame, textvariable=nameVar, width=25)
    nameEntry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    # New section for other settings
    otherSettingsFrame = ttk.LabelFrame(scrollableFrame, text="⚙️ Otros Ajustes", padding=15)
    otherSettingsFrame.pack(fill=X, pady=10, padx=20)

    ttk.Label(otherSettingsFrame, text="Ruta de Firma Digital (PNG):").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    signaturePathEntry = ttk.Entry(otherSettingsFrame, textvariable=signaturePathVar, width=35)
    signaturePathEntry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    ttk.Label(otherSettingsFrame, text="Datos de Contacto:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
    contactDetailsTextWidget = Text(otherSettingsFrame, wrap=WORD, width=35, height=7, font=("Segoe UI", 9))
    contactDetailsTextWidget.grid(row=1, column=1, padx=5, pady=5, sticky=W)
    contactDetailsTextWidget.insert(END, currentSettings.get("datos_contacto", ""))


    def saveConfiguration():
        configuration = {
            "tema": themeVar.get(),
            "fuente_size": fontSize.get(),
            "auto_scroll": autoScroll.get(),
            "sonido": notificationSound.get(),
            "modelo": modelVar.get(),
            "temperatura": temperatureVar.get(),
            "email": emailVar.get(),
            "nombre_correo": nameVar.get(),
            "ruta_firma_png": signaturePathVar.get(),
            "datos_contacto": contactDetailsTextWidget.get("1.0", END).strip(),
            "PaswordMail": PaswordMail.get()
        }

        saveSettings(configuration)

        titleLabel.config(text="✅ Configuración guardada")
        configFrame.after(2000, lambda: titleLabel.config(text="⚙️ Configuración"))

    def resetConfiguration():
        defaultSettings = getDefaultSettings()
        themeVar.set(defaultSettings["tema"])
        fontSize.set(defaultSettings["fuente_size"])
        autoScroll.set(defaultSettings["auto_scroll"])
        notificationSound.set(defaultSettings["sonido"])
        modelVar.set(defaultSettings["modelo"])
        temperatureVar.set(defaultSettings["temperatura"])
        emailVar.set(defaultSettings["email"])
        nameVar.set(defaultSettings["nombre_correo"])
        PaswordMail.set(defaultSettings["nombre_correo"])
        signaturePathVar.set(defaultSettings["ruta_firma_png"])
        
        contactDetailsTextWidget.delete("1.0", END)
        contactDetailsTextWidget.insert(END, defaultSettings["datos_contacto"])
        
        tempLabel.config(text=f"{defaultSettings['temperatura']:.1f}")
        saveSettings(defaultSettings)

    # Botones de configuración movidos al final
    configButtonsFrame = ttk.LabelFrame(scrollableFrame, text="buttons", padding=15)
    configButtonsFrame.pack(fill=X, pady=10, padx=20)

    backButton = ttk.Button(configButtonsFrame, text="Volver", bootstyle="success", width=10, command=goBackToChat)
    backButton.pack(pady=5)

    saveButton = ttk.Button(configButtonsFrame, text="Guardar", bootstyle="success", width=10 , command=saveConfiguration)
    saveButton.pack(pady=5)

    resetButton = ttk.Button(configButtonsFrame, text="Restablecer", bootstyle="primary", width=10, command=resetConfiguration)
    resetButton.pack(padx=5)

    return configFrame
