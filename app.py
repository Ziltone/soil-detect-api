from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load Model
model = tf.keras.models.load_model("best_soil_model.h5")
soil_classes = ["Alluvial", "Black", "Clay", "Laterite", "Loamy", "Red", "Sandy", "Sandy Loam"]

@app.route('/')
def home():
    return "Flask Server is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    try:
        image = Image.open(file).resize((224, 224))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)

        prediction = model.predict(image)
        predicted_class = soil_classes[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        return jsonify({"soil_type": predicted_class, "confidence": confidence})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
