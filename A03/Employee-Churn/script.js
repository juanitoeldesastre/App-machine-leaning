let model;
let scaler = null;

// Cargar el modelo
tf.loadLayersModel('modelo_tfjs/model.json').then(m => {
  model = m;
  console.log("✅ Modelo cargado");
}).catch(err => {
  console.error("❌ Error al cargar el modelo:", err);
});

// Cargar scaler.json
fetch("scaler.json")
  .then(res => res.json())
  .then(data => {
    scaler = data;
    console.log("✅ Escalador cargado");
  })
  .catch(err => {
    console.error("❌ Error al cargar scaler.json:", err);
  });

document.getElementById('predict-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  if (!model || !scaler) {
    alert("Modelo o escalador no cargado aún. Espera un momento.");
    return;
  }

  const formData = new FormData(e.target);

  // Crear objeto de entrada con valores por defecto (0 en one-hot)
  const input = {
    Age: parseFloat(formData.get('Age')),
    DistanceFromHome: parseFloat(formData.get('DistanceFromHome')),
    Education: parseFloat(formData.get('Education')),
    MonthlyIncome: parseFloat(formData.get('MonthlyIncome')),
    NumCompaniesWorked: parseFloat(formData.get('NumCompaniesWorked')),
    TotalWorkingYears: parseFloat(formData.get('TotalWorkingYears')),
    YearsAtCompany: parseFloat(formData.get('YearsAtCompany')),

    // One-hot (BusinessTravel)
    "BusinessTravel_Non-Travel": 0,
    "BusinessTravel_Travel_Frequently": 0,
    "BusinessTravel_Travel_Rarely": 0,

    // One-hot (Department)
    "Department_Human Resources": 0,
    "Department_Research & Development": 0,
    "Department_Sales": 0,

    // One-hot (JobRole)
    "JobRole_Healthcare Representative": 0,
    "JobRole_Human Resources": 0,
    "JobRole_Laboratory Technician": 0,
    "JobRole_Manager": 0,
    "JobRole_Manufacturing Director": 0,
    "JobRole_Research Director": 0,
    "JobRole_Research Scientist": 0,
    "JobRole_Sales Executive": 0,
    "JobRole_Sales Representative": 0,

    // One-hot (OverTime)
    "OverTime_No": 0,
    "OverTime_Yes": 0
  };

  // Activar la categoría seleccionada
  input[`BusinessTravel_${formData.get('BusinessTravel')}`] = 1;
  input[`Department_${formData.get('Department')}`] = 1;
  input[`JobRole_${formData.get('JobRole')}`] = 1;
  input[`OverTime_${formData.get('OverTime')}`] = 1;

  // Crear array ordenado según scaler.columns
  const inputArray = scaler.columns.map(col => input[col] || 0);

  // Normalizar entrada
  const normalizedInput = inputArray.map((val, i) =>
    (val - scaler.mean[i]) / scaler.scale[i]
  );

  // Crear tensor y predecir
  const inputTensor = tf.tensor2d([normalizedInput]);
  const prediction = model.predict(inputTensor);
  const result = await prediction.data();
  const probability = result[0];

  // Mostrar resultado
  document.getElementById('result').textContent =
    `Probabilidad de rotación: ${(probability * 100).toFixed(2)}%`;
});
