// human_tracking.js
const Human = require('@vladmandic/human');
const fs = require('fs');
const canvas = require('canvas'); // You may need to install the 'canvas' package

const config = {
  // Configuration options for the Human library
  backend: 'tensorflow', // Use TensorFlow backend
  modelBasePath: 'https://vladmandic.github.io/human/models/', // Base path for model files
  face: { enabled: true },
  body: { enabled: true },
  hand: { enabled: true },
};

const human = new Human.Human(config);

async function detect(inputImagePath) {
  // Load the image into a canvas
  const img = await canvas.loadImage(inputImagePath);
  const inputCanvas = canvas.createCanvas(img.width, img.height);
  const ctx = inputCanvas.getContext('2d');
  ctx.drawImage(img, 0, 0);

  // Run the Human library detection
  const result = await human.detect(inputCanvas);

  // Output the results
  console.log('Body:', result.body);
  // Add any additional processing or output here

  // Optionally, save the annotated image
  const outCanvas = human.draw.all(inputCanvas, result);
  const outBuffer = outCanvas.toBuffer('image/jpeg');
  fs.writeFileSync('output.jpg', outBuffer);
}

// Replace 'input.jpg' with the path to your input image file
detect('input.jpg').catch(console.error);
