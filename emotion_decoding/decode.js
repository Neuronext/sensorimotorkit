const config = { backend: 'webgl' };
const Human = new Human.Human(config);
// const Human = require('human').default;
const tf = require('@tensorflow/tfjs-node');

// Initialize Human with desired configuration
const config = {
  backend: 'tensorflow',
  face: {
    enabled: true,
    detector: { rotation: true },
    emotion: { enabled: true },
  },
};

const human = new Human(config);

// Function to detect emotions
async function detectEmotion(imagePath) {
  const image = await tf.node.decodeImage(await tf.node.readFile(imagePath));
  const result = await human.detect(image);
  if (result.face.length > 0) {
    console.log('Emotions:', result.face[0].emotion);
  } else {
    console.log('No faces detected');
  }
}

// Replace with your image path
detectEmotion('.test.jpg');
