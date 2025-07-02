import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import date, timedelta
import os

# --- 1. CONFIGURACIÓN INICIAL ---

# Inicializar Faker para generar datos ficticios en español
fake = Faker('es_ES')

# Parámetros de generación
NUM_TRAMITES = 2500
FECHA_HOY = date.today()

# Listas de opciones para las variables categóricas
TIPOS_TRAMITE = [
    "Licencia de Construcción", "Licencia de Funcionamiento", "Pago de Impuestos",
    "Solicitud de Partida de Nacimiento", "Permiso para Evento Público", "Reclamo de Servicio"
]
AREAS = ["Desarrollo Urbano", "Tesorería", "Registro Civil", "Seguridad Ciudadana", "Servicios Públicos"]
CANALES_ENTRADA = ["Presencial", "En Línea", "Telefónico"]

# --- 2. FUNCIONES AUXILIARES PARA LÓGICA MÁS REALISTA ---

def generar_monto_asociado(tipo_tramite):
    """Genera un monto monetario basado en el tipo de trámite."""
    if tipo_tramite == "Licencia de Construcción":
        return round(random.uniform(5000, 200000), 2)
    elif tipo_tramite == "Licencia de Funcionamiento":
        return round(random.uniform(500, 2500), 2)
    elif tipo_tramite == "Pago de Impuestos":
        return round(random.uniform(100, 10000), 2)
    elif tipo_tramite == "Permiso para Evento Público":
        return round(random.uniform(200, 1500), 2)
    else:
        return 0.0 # Reclamos y partidas no tienen monto directo

def documentos_estan_completos(canal):
    """La probabilidad de que los documentos estén completos depende del canal."""
    if canal == "En Línea":
        # Es más probable que los formularios online obliguen a subir todo
        return random.choices([True, False], weights=[0.9, 0.1])[0]
    else:
        # En presencial o teléfono es más fácil que falte algo
        return random.choices([True, False], weights=[0.7, 0.3])[0]

def asignar_prioridad_con_puntuacion(row):
    """
    Asigna una prioridad usando un sistema de puntuación.
    Esto crea una lógica más compleja que el modelo deberá aprender.
    """
    score = 0
    # Penalización máxima si faltan documentos
    if not row['documentos_completos']:
        score += 5
    # Los reclamos son muy importantes
    if row['tipo_tramite'] == 'Reclamo de Servicio':
        score += 4
    # La urgencia declarada por el ciudadano cuenta mucho
    if row['solicitante_declara_urgencia']:
        score += 3
    # Penalización por retraso
    if row['dias_desde_solicitud'] > 30:
        score += 4
    elif row['dias_desde_solicitud'] > 15:
        score += 2
    # Montos altos pueden requerir más atención
    if row['monto_asociado'] > 50000:
        score += 1

    # Convertir puntuación a una categoría de prioridad
    if score >= 7:
        return 'Urgente'
    elif score >= 5:
        return 'Alta'
    elif score >= 2:
        return 'Media'
    else:
        return 'Baja'


# --- 3. GENERACIÓN PRINCIPAL DEL DATASET ---

print("Generando dataset mejorado...")
lista_tramites = []
for i in range(NUM_TRAMITES):
    tipo_tramite = random.choice(TIPOS_TRAMITE)
    canal = random.choice(CANALES_ENTRADA)
    
    # Generar fecha de solicitud en los últimos 60 días
    fecha_solicitud = fake.date_between(start_date='-60d', end_date='today')
    dias_transcurridos = (FECHA_HOY - fecha_solicitud).days
    
    tramite = {
        'id_tramite': 1000 + i,
        'nombre_solicitante': fake.name(),
        'dni_solicitante': fake.doi(),
        'fecha_solicitud': fecha_solicitud,
        'tipo_tramite': tipo_tramite,
        'area_responsable': random.choice(AREAS),
        'canal_entrada': canal,
        'monto_asociado': generar_monto_asociado(tipo_tramite),
        'documentos_completos': documentos_estan_completos(canal),
        'solicitante_declara_urgencia': random.choices([True, False], weights=[0.15, 0.85])[0], # Pocos declaran urgencia
        'dias_desde_solicitud': dias_transcurridos
    }
    lista_tramites.append(tramite)

# Convertir la lista de diccionarios a un DataFrame de Pandas
df = pd.DataFrame(lista_tramites)

# Aplicar la lógica de puntuación para crear la columna 'prioridad'
df['prioridad'] = df.apply(asignar_prioridad_con_puntuacion, axis=1)

# Reordenar columnas para que el CSV sea más legible
column_order = [
    'id_tramite', 'nombre_solicitante', 'dni_solicitante', 'fecha_solicitud',
    'tipo_tramite', 'area_responsable', 'canal_entrada', 'monto_asociado',
    'documentos_completos', 'solicitante_declara_urgencia', 'dias_desde_solicitud',
    'prioridad' # La columna objetivo al final
]
df = df[column_order]


# --- 4. GUARDAR Y MOSTRAR RESULTADOS ---

# Asegurarse de que el directorio 'data/' exista
if not os.path.exists('data'):
    os.makedirs('data')

output_path = 'data/tramites_municipales.csv'
df.to_csv(output_path, index=False, date_format='%Y-%m-%d')

print(f"\n¡Dataset generado y guardado exitosamente en '{output_path}'!")
print(f"Total de registros: {len(df)}")

print("\n--- Primeras 5 filas del nuevo dataset ---")
print(df.head())

print("\n--- Distribución de prioridades generadas ---")
print(df['prioridad'].value_counts())