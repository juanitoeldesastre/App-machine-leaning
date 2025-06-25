# Predicción de Rotación de Empleados

Esta Tarea es un proyecto web que predice la probabilidad de que un empleado abandone una empresa, utilizando una red neuronal entrenada con Keras1 y exportada en TensorFlow.js.

---

### Problemas

Una de las partes más difíciles fue **exportar el modelo a TensorFlow\.js**. Me aparecía este error al intentar convertir el archivo `.h5`:

![Error](https://github.com/juanitoeldesastre/taller-ml-apps/tree/main/A03/Employee-Churn/img/CAPTURA.png)

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


## ⚙️ Preprocesamiento

* ✔️ One-hot encoding para variables categóricas
* ✔️ Escalado de características numéricas usando `StandardScaler`
* ✔️ División 80/20 para entrenamiento/prueba
* ✔️ Se guardó el orden de columnas en `feature_columns.txt`
* ✔️ Se exportó el `scaler.json` con medias y desviaciones estándar

📌 Las variables categóricas fueron transformadas con **one-hot encoding**.

![One-hot encoding](https://github.com/juanitoeldesastre/taller-ml-apps/tree/main/A03/Employee-Churn/img/Code1.png)

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

## 🌐 Aplicación Web

El modelo fue exportado y cargado en una WebApp desarrollada con:

* HTML + CSS
* JavaScript (`script.js`)
* TensorFlow\.js

La interfaz permite ingresar datos de un empleado y obtener la probabilidad de rotación:

![Formulario Web](https://github.com/tu-usuario/tu-repo/ruta/formulario-web.png)

---

## 🧪 Resultado

Ejemplo de predicción con datos ficticios:

![Resultado](https://github.com/tu-usuario/tu-repo/ruta/resultado-prediccion.png)

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

## 🧠 Conclusión

Este proyecto no solo ayudó a entender el proceso completo de desarrollo de un modelo de ML, sino también los retos de **compatibilidad de versiones** y la **implementación en frontend con TensorFlow\.js**.

---

Si subes las imágenes al repositorio, recuerda reemplazar las URLs tipo:

```markdown
![Texto](https://github.com/tu-usuario/tu-repo/ruta/imagen.png)
```

por la URL real de tu imagen.

¿Quieres que también te genere automáticamente las imágenes de ejemplo si me pasas capturas?
