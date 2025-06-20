// script.js (igual que antes)
let model;

async function loadModel() {
  model = await tf.loadLayersModel('model_tfjs/model.json');
  console.log("✅ Modelo cargado.");
}

loadModel();

function preprocessImage(img) {
  return tf.tidy(() => {
    return tf.browser.fromPixels(img)
      .resizeNearestNeighbor([150, 150])
      .toFloat()
      .div(255.0)
      .expandDims();
  });
}

async function predictImage(img) {
  const tensor = preprocessImage(img);
  const score = (await model.predict(tensor).data())[0];
  tensor.dispose();

  const dogProb = score;
  const catProb = 1 - score;
  let label, prob;
  if (dogProb > catProb) {
    label = "🐶 Perro";
    prob = dogProb;
  } else {
    label = "🐱 Gato";
    prob = catProb;
  }

  document.getElementById('result').innerText =
    `Predicción: ${label} (${(prob * 100).toFixed(2)}%)`;
}

document.getElementById('imageInput').addEventListener('change', (evt) => {
  const file = evt.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const imgEl = document.getElementById('preview');
    imgEl.src = e.target.result;
    imgEl.style.display = 'block';
    imgEl.onload = () => predictImage(imgEl);
  };
  reader.readAsDataURL(file);
});
