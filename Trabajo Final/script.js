let model;

window.addEventListener("load", async () => {
  model = await tf.loadLayersModel("modelo_tfjs/model.json");
  console.log("✅ Modelo cargado");
});

const imageUpload = document.getElementById("imageUpload");
const previewImage = document.getElementById("previewImage");
const resultDiv = document.getElementById("result");
const predictBtn = document.getElementById("predictBtn");

imageUpload.addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    previewImage.src = reader.result;
    resultDiv.textContent = "";
    resultDiv.classList.remove('result-clean', 'result-dirty');
    resultDiv.style.display = 'none';
  };
  reader.readAsDataURL(file);
});

predictBtn.addEventListener("click", async () => {
  if (!previewImage.src || !model) return;

  const imageTensor = tf.tidy(() => {
    return tf.browser.fromPixels(previewImage)
      .resizeNearestNeighbor([128, 128])
      .toFloat()
      .div(255.0)
      .expandDims();
  });

  const prediction = await model.predict(imageTensor).data();
  const score = prediction[0];
  const porcentaje = (score * 100).toFixed(2);
  const porcentajeinverso = ((1 - score) * 100).toFixed(2);

  const esSucia = score > 0.5;

  const texto = esSucia
    ? `🟥 Calle sucia (${porcentaje}%)`
    : `🟩 Calle limpia (${porcentajeinverso}%)`;

  resultDiv.textContent = texto;
  resultDiv.style.display = 'block';
  resultDiv.classList.remove('result-clean', 'result-dirty');
  resultDiv.classList.add(esSucia ? 'result-dirty' : 'result-clean');

  imageTensor.dispose();
});
