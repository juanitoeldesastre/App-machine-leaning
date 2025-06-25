# Predicción de Rotación de Empleados

Esta Tarea es un proyecto web que predice la probabilidad de que un empleado abandone una empresa, utilizando una red neuronal entrenada con Keras1 y exportada en TensorFlow.js.

---

### Problemas

Una de las partes más difíciles fue **exportar el modelo a TensorFlow\.js**. Me aparecía este error al intentar convertir el archivo `.h5`:

![Error al exportar modelo](https://raw.githubusercontent.com/juanitoeldesastre/taller-ml-apps/main/A03/Employee-Churn/img/CAPTURA.png)

> Este error se debía a que faltaba el archivo `inference.so` en Windows. Intenté varias veces sin éxito.

### Solución

Decidí exportarlo desde **Linux usando WSL**, ya que por mi experiencia nunca falla.

* Cree un entorno virtual con `miniconda`
* Entré a la carpeta del proyecto desde WSL
* Ejecuté:

```bash
tensorflowjs_converter --input_format=keras modelo.h5 modelo_tfjs/
```

✅ ¡Y funcionó!

---

## Entrenamiento del Modelo

### Dataset

* Dataset: **IBM HR Analytics Employee Attrition**
* Enlace: [Kaggle - IBM HR Analytics Dataset](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
* Archivo utilizado: `WA_Fn-UseC_-HR-Employee-Attrition.csv`

### Variables

| Tipo        | Variables principales                                                                                |
| ----------- | ---------------------------------------------------------------------------------------------------- |
| Numéricas   | `Age`, `DistanceFromHome`, `Education`, `MonthlyIncome`, `YearsAtCompany`, `TotalWorkingYears`, etc. |
| Categóricas | `BusinessTravel`, `Department`, `JobRole`, `OverTime`                                                |
| Objetivo    | `Attrition` (Yes = 1, No = 0)                                                                        |

---

## Preprocesamiento

* ✔️ One-hot encoding para variables categóricas
* ✔️ Escalado de características numéricas usando `StandardScaler`
* ✔️ División 80/20 para entrenamiento/prueba
* ✔️ Se guardó el orden de columnas en `feature_columns.txt`
* ✔️ Se exportó el `scaler.json` con medias y desviaciones estándar para mi webapp con tfjs

📌 Las variables categóricas fueron transformadas con **one-hot encoding**.

**BusinessTravel:**

| Código | Valor              |
|--------|--------------------|
| 1      | Travel_Rarely      |
| 2      | Travel_Frequently  |
| 3      | Non-Travel         |

**Department:**

| Código | Valor                   |
|--------|-------------------------|
| 1      | Sales                   |
| 2      | Research & Development  |
| 3      | Human Resources         |

**JobRole:**

| Código | Valor                     |
|--------|---------------------------|
| 1      | Sales Executive           |
| 2      | Research Scientist        |
| 3      | Laboratory Technician     |
| 4      | Manufacturing Director    |
| 5      | Healthcare Representative |
| 6      | Manager                   |
| 7      | Sales Representative      |
| 8      | Research Director         |
| 9      | Human Resources           |

**OverTime:**

| Código | Valor |
|--------|-------|
| 1      | Yes   |
| 2      | No    |

---

**One-hot encoding** transforma valores categoricos (strings) en columnas binarias volviendolo facil de interpretar para la maquina, un modelo matematico no puede interpretar un texto. Es mas sencillo dibujarlo como una matriz

![One-hot encoding](https://raw.githubusercontent.com/juanitoeldesastre/taller-ml-apps/main/A03/Employee-Churn/img/BusinessTravelCode.png)

**Attrition** convertir a binario para que la respuesta pase de `true` or `false` a `1` y `0`

**Escalar** valores numericos con `StandardScaler` de `Scikit-learn` para que mi modelo procese mejor los datos numéricos.

---

## Modelo de Red Neuronal

```python
model = Sequential([
    InputLayer(input_shape=(25,)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
```

* Función de pérdida: `binary_crossentropy`
* Optimizador: `adam`
* Métrica: `accuracy`
* Épocas: 50
* Tamaño de lote: 16

---

## Aplicación Web

El modelo fue exportado a tfjs y cargado en una WebApp desarrollada con:

* HTML + CSS
* JavaScript (`script.js`)
* TensorFlow\.js

La interfaz simple permite ingresar datos de un empleado y obtener la probabilidad de rotación:

![Formulario Web](https://raw.githubusercontent.com/juanitoeldesastre/taller-ml-apps/main/A03/Employee-Churn/img/webapp.png)

---

## 📁 Estructura del Proyecto

```
Employee-Churn/
├── modelo.h5
├── modelo_tfjs/           # Modelo exportado para TF.js
│   ├── model.json
│   └── group1-shard*.bin
├── scaler.json            # Media y escala para normalizar
├── feature_columns.txt    # Orden de columnas
├── index.html
├── style.css
├── script.js
├── README.md
```

---