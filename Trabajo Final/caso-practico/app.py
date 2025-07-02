import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import joblib
import os

# --- 1. CARGAR EL MODELO ENTRENADO ---
# Se ejecuta una sola vez al iniciar la aplicación.
MODEL_PATH = os.path.join('modelo', 'modelo_prioridad.pkl')
try:
    model = joblib.load(MODEL_PATH)
    print(f"Modelo cargado exitosamente desde '{MODEL_PATH}'")
except FileNotFoundError:
    messagebox.showerror(
        "Error Crítico",
        f"No se encontró el archivo del modelo en '{MODEL_PATH}'.\n\nAsegúrate de ejecutar primero el notebook 'entrenamiento_modelo.ipynb' para generar el modelo."
    )
    # Si no hay modelo, la aplicación no puede funcionar.
    exit()
except Exception as e:
    messagebox.showerror("Error Crítico", f"Ocurrió un error al cargar el modelo: {e}")
    exit()


# --- 2. CONFIGURACIÓN DE LA INTERFAZ ---
# Estas listas deben coincidir con los datos usados en el entrenamiento.
TIPOS_TRAMITE = [
    "Licencia de Construcción", "Licencia de Funcionamiento", "Pago de Impuestos",
    "Solicitud de Partida de Nacimiento", "Permiso para Evento Público", "Reclamo de Servicio"
]
AREAS = ["Desarrollo Urbano", "Tesorería", "Registro Civil", "Seguridad Ciudadana", "Servicios Públicos"]
CANALES_ENTRADA = ["Presencial", "En Línea", "Telefónico"]

# Diccionario de colores para los resultados, mejora la usabilidad.
PRIORIDAD_COLORES = {
    'Urgente': 'red',
    'Alta': 'orange red',
    'Media': 'dark orange',
    'Baja': 'forest green'
}


# --- 3. FUNCIÓN PRINCIPAL DE PREDICCIÓN ---
def predecir_prioridad():
    """Recoge los datos de la interfaz, los valida y realiza la predicción."""
    
    # A. RECOGER DATOS DE LA INTERFAZ
    tipo_tramite = combo_tipo.get()
    area = combo_area.get()
    canal = combo_canal.get()
    docs_completos = bool(check_docs_var.get())
    urgencia_declarada = bool(check_urgencia_var.get())

    # B. VALIDAR ENTRADAS
    if not tipo_tramite or not area or not canal:
        messagebox.showwarning("Campos Incompletos", "Por favor, selecciona una opción en todos los menús desplegables.")
        return

    try:
        monto = float(entry_monto.get())
        dias = int(entry_dias.get())
        if monto < 0 or dias < 0:
            messagebox.showwarning("Datos Inválidos", "El monto y los días no pueden ser negativos.")
            return
    except ValueError:
        messagebox.showerror("Error de Entrada", "Por favor, ingresa valores numéricos válidos para 'Monto' y 'Días'.")
        return

    # C. PREPARAR DATOS PARA EL MODELO
    # Crear un DataFrame con los mismos nombres de columna que en el entrenamiento.
    # El orden debe ser exactamente el mismo.
    input_data = pd.DataFrame({
        'tipo_tramite': [tipo_tramite],
        'area_responsable': [area],
        'canal_entrada': [canal],
        'monto_asociado': [monto],
        'documentos_completos': [docs_completos],
        'solicitante_declara_urgencia': [urgencia_declarada],
        'dias_desde_solicitud': [dias]
    })
    
    # D. REALIZAR PREDICCIÓN
    try:
        prediccion_array = model.predict(input_data)
        probabilidades = model.predict_proba(input_data)
        
        prediccion_final = prediccion_array[0]
        confianza = probabilidades.max() * 100
        
        # E. MOSTRAR RESULTADOS EN LA INTERFAZ
        resultado_texto.set(f"Prioridad Predicha: {prediccion_final}")
        confianza_texto.set(f"Confianza: {confianza:.2f}%")
        
        # Cambiar el color del texto del resultado según la prioridad
        color_resultado = PRIORIDAD_COLORES.get(prediccion_final, 'black')
        label_resultado.config(foreground=color_resultado)

        # F. SIMULAR ALERTA EN LA CONSOLA
        print("--- ALERTA DE SISTEMA (SIMULACIÓN) ---")
        print(f"Trámite evaluado. Prioridad asignada: {prediccion_final}")
        print(f"Notificando al área de {area} y al ciudadano (simulado).")
        print("---------------------------------------")

    except Exception as e:
        messagebox.showerror("Error de Predicción", f"Ocurrió un error al predecir: {e}")


# --- 4. CREACIÓN DE LA VENTANA Y WIDGETS ---
root = tk.Tk()
root.title("Sistema Automatizado de Gestión Documental")
root.geometry("450x420")
root.resizable(False, False)

# Estilo para los widgets
style = ttk.Style(root)
style.theme_use('clam') # Un tema moderno

# Frame principal para organizar los elementos
frame = ttk.Frame(root, padding="20")
frame.pack(fill=tk.BOTH, expand=True)

# --- Creación de cada widget ---
# Fila 0: Tipo de Trámite
ttk.Label(frame, text="Tipo de Trámite:").grid(row=0, column=0, sticky=tk.W, pady=4)
combo_tipo = ttk.Combobox(frame, values=TIPOS_TRAMITE, state="readonly")
combo_tipo.grid(row=0, column=1, sticky=tk.EW, padx=5)

# Fila 1: Área Responsable
ttk.Label(frame, text="Área Responsable:").grid(row=1, column=0, sticky=tk.W, pady=4)
combo_area = ttk.Combobox(frame, values=AREAS, state="readonly")
combo_area.grid(row=1, column=1, sticky=tk.EW, padx=5)

# Fila 2: Canal de Entrada
ttk.Label(frame, text="Canal de Entrada:").grid(row=2, column=0, sticky=tk.W, pady=4)
combo_canal = ttk.Combobox(frame, values=CANALES_ENTRADA, state="readonly")
combo_canal.grid(row=2, column=1, sticky=tk.EW, padx=5)

# Fila 3: Monto Asociado
ttk.Label(frame, text="Monto Asociado (S/):").grid(row=3, column=0, sticky=tk.W, pady=4)
entry_monto = ttk.Entry(frame)
entry_monto.grid(row=3, column=1, sticky=tk.EW, padx=5)
entry_monto.insert(0, "0.0")

# Fila 4: Días desde Solicitud
ttk.Label(frame, text="Días desde Solicitud:").grid(row=4, column=0, sticky=tk.W, pady=4)
entry_dias = ttk.Entry(frame)
entry_dias.grid(row=4, column=1, sticky=tk.EW, padx=5)
entry_dias.insert(0, "0")

# Fila 5: Checkboxes
check_docs_var = tk.IntVar()
check_docs = ttk.Checkbutton(frame, text="¿Documentos Completos?", variable=check_docs_var)
check_docs.grid(row=5, column=0, columnspan=2, pady=8, sticky=tk.W)

check_urgencia_var = tk.IntVar()
check_urgencia = ttk.Checkbutton(frame, text="¿Solicitante Declara Urgencia?", variable=check_urgencia_var)
check_urgencia.grid(row=6, column=0, columnspan=2, pady=2, sticky=tk.W)

# Fila 7: Botón para predecir
boton_predecir = ttk.Button(frame, text="EVALUAR PRIORIDAD", command=predecir_prioridad)
boton_predecir.grid(row=7, column=0, columnspan=2, pady=15, ipady=5)

# Fila 8 y 9: Etiquetas para mostrar el resultado
resultado_texto = tk.StringVar()
label_resultado = ttk.Label(frame, textvariable=resultado_texto, font=("Helvetica", 14, "bold"), anchor="center")
label_resultado.grid(row=8, column=0, columnspan=2, pady=(10, 0))

confianza_texto = tk.StringVar()
label_confianza = ttk.Label(frame, textvariable=confianza_texto, font=("Helvetica", 10, "italic"), anchor="center")
label_confianza.grid(row=9, column=0, columnspan=2)

# Configurar el grid para que la columna 1 se expanda
frame.columnconfigure(1, weight=1)

# --- 5. INICIAR LA APLICACIÓN ---
root.mainloop()