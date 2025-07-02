import pandas as pd
import random
from statistics import mode

tramites = [
    "Licencia de funcionamiento",
    "Permiso de construcción",
    "Certificado de posesión",
    "Conexión de servicios básicos",
    "Solicitud de limpieza pública",
    "Autorización de eventos",
    "Inscripción en el registro municipal",
    "Permiso de publicidad exterior",
    "Cambio de uso de suelo",
    "Certificado de defensa civil"
]

resultados = ["Aceptado", "En espera", "Rechazado"]
areas = [
    "Licencias", "Urbanismo", "Catastro", "Servicios Públicos",
    "Medio Ambiente", "Defensa Civil", "Atención al Ciudadano"
]

tramites_data = []
for i in range(300):
    tramite = random.choices(
        tramites,
        weights=[0.15, 0.13, 0.12, 0.10, 0.08, 0.08, 0.08, 0.08, 0.09, 0.09],
        k=1
    )[0]

    if tramite == "Licencia de funcionamiento":
        tiempo = random.randint(180, 300); frustracion = random.randint(4, 5)
    elif tramite == "Permiso de construcción":
        tiempo = random.randint(120, 240); frustracion = random.randint(4, 5)
    elif tramite == "Certificado de posesión":
        tiempo = random.randint(90, 150); frustracion = random.randint(3, 5)
    elif tramite == "Conexión de servicios básicos":
        tiempo = random.randint(30, 90); frustracion = random.randint(2, 4)
    elif tramite == "Solicitud de limpieza pública":
        tiempo = random.randint(20, 60); frustracion = random.randint(1, 3)
    elif tramite == "Autorización de eventos":
        tiempo = random.randint(60, 150); frustracion = random.randint(2, 4)
    elif tramite == "Inscripción en el registro municipal":
        tiempo = random.randint(30, 90); frustracion = random.randint(2, 3)
    elif tramite == "Permiso de publicidad exterior":
        tiempo = random.randint(100, 180); frustracion = random.randint(3, 5)
    elif tramite == "Cambio de uso de suelo":
        tiempo = random.randint(150, 250); frustracion = random.randint(4, 5)
    else:
        tiempo = random.randint(100, 180); frustracion = random.randint(3, 5)

    tramites_data.append({
        "ID": i + 1,
        "Trámite": tramite,
        "Tiempo de Atención (min)": tiempo,
        "Área Responsable": random.choice(areas),
        "Resultado": random.choices(resultados, weights=[0.6, 0.3, 0.1])[0],
        "Nivel de Frustración (1-5)": frustracion
    })

df = pd.DataFrame(tramites_data)

# Estadísticas: media y moda
stats = df.groupby("Trámite").agg({
    "Tiempo de Atención (min)": "mean",
    "Nivel de Frustración (1-5)": "mean"
})
stats["Frustración Moda"] = df.groupby("Trámite")["Nivel de Frustración (1-5)"].agg(lambda x: mode(x))
stats = stats.rename(columns={
    "Tiempo de Atención (min)": "Tiempo Medio (min)",
    "Nivel de Frustración (1-5)": "Frustración Media"
})
stats["Tiempo Medio (min)"] = stats["Tiempo Medio (min)"].round(2)
stats["Frustración Media"] = stats["Frustración Media"].round(2)

# Mostrar resultados
stats.reset_index(inplace=True)
print(stats)
