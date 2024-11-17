from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input
import numpy as np
import os

app = Flask(__name__)

# Cargar el modelo
model_path = "./modelos/modelo_papa.keras"
model = tf.keras.models.load_model(model_path)

# Etiquetas de las clases
class_labels = ['Late-Blight', 'Pudricion_Parda', 'Sana', 'Tizon_Temprano', 'Virus']

# Endpoint para predecir
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No se proporcionó ninguna imagen."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No se seleccionó ninguna imagen."}), 400
    
    try:
        # Procesar la imagen
        img = tf.keras.utils.load_img(file, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Realizar predicción
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)
        clase_predicha = class_labels[predicted_class]
        probabilidad_clase = predictions[0][predicted_class] * 100

        return jsonify({
            "predicted_class": clase_predicha,
            "confidence": f"{probabilidad_clase:.2f}%"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta principal (opcional, para probar desde el navegador)
@app.route('/')
def home():
    return "API para detección de enfermedades en papa."

if __name__ == '__main__':
    app.run(debug=True)
