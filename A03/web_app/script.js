let model;
async function cargarModelo() {
 model = await tf.loadGraphModel('modelo_tfjs/model.json');
 console.log("Modelo cargado");
}
cargarModelo();
// Canvas
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
ctx.fillStyle = 'black';
ctx.fillRect(0, 0, canvas.width, canvas.height);
let pintando = false;
canvas.addEventListener('mousedown', () => { pintando = true; });
canvas.addEventListener('mouseup', () => { pintando = false; ctx.beginPath(); });
canvas.addEventListener('mousemove', dibujar);
function dibujar(e) {
 if (!pintando) return;
 ctx.lineWidth = 15;
 ctx.lineCap = 'round';
 ctx.strokeStyle = 'white';
 ctx.lineTo(e.offsetX, e.offsetY);
 ctx.stroke();
 ctx.beginPath();
 ctx.moveTo(e.offsetX, e.offsetY);
}
function predecir() {
 let imgData = ctx.getImageData(0, 0, 280, 280);
 let tensor = tf.browser.fromPixels(imgData, 1)
 .resizeNearestNeighbor([28, 28])
 .mean(2)
 .toFloat()
 .div(255.0)
 .reshape([1, 28, 28, 1]);
 model.executeAsync(tensor).then(pred => {
 const prediccion = pred.arraySync()[0];
 const clase = prediccion.indexOf(Math.max(...prediccion));
 document.getElementById('resultado').innerText = "Predicción: " + clase;
 });
}