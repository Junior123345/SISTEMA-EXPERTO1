from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from dotenv import load_dotenv
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input
import os
import numpy as np
from io import BytesIO

app = Flask(__name__)

# Configuración de la clave secreta para sesiones seguras
app.secret_key = os.getenv("SECRET_KEY", "clave_secreta_segura")

# Configuración de cookies para producción
app.config['SESSION_COOKIE_SECURE'] = os.getenv("SESSION_COOKIE_SECURE", False)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Cargar el modelo
model_path = "./modelos/modelo_papa.keras"
print("Cargando el modelo...")
try:
    model = tf.keras.models.load_model(model_path)
    print("Modelo cargado correctamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {str(e)}")
    model = None

# Etiquetas de las clases
class_labels = ['Late-Blight', 'Pudricion_Parda', 'Sana', 'Tizon_Temprano', 'Virus']

# Recomendaciones para cada clase
all_recommendations = {
    "Late-Blight": [
        "Realizar aplicaciones preventivas de fungicidas de contacto, como cúpricos o mancozeb.",
        "Evitar los riegos excesivos y mantener el campo con un buen drenaje.",
        "Eliminar residuos de cultivos anteriores y plantas voluntarias.",
        "Usar variedades resistentes con resistencia horizontal.",
        "Planificar la siembra para evitar periodos de alta humedad y bajas temperaturas.",
        "Realizar el corte del follaje dos semanas antes de la cosecha para minimizar la infección en tubérculos."
    ],
    "Tizon_Temprano": [
        "Utilizar semillas de buena calidad y fertilización adecuada para evitar el estrés de las plantas.",
        "Aplicar fungicidas de contacto al inicio de la temporada, como Mancozeb o Clorotalonil.",
        "Implementar rotación de cultivos con plantas no hospederas.",
        "Cortar el follaje al menos 10 días antes de la cosecha para evitar infecciones en tubérculos.",
        "Mantener los tubérculos almacenados en ambientes frescos y con buena ventilación."
    ],
    "Pudricion_Parda": [
        "Usar semillas certificadas y libres de enfermedad.",
        "Realizar rotaciones con gramíneas como maíz, sorgo o arroz para reducir la presencia de bacterias.",
        "Cultivar papa en tierras nuevas o libres de antecedentes de la enfermedad.",
        "Lavar y desinfectar herramientas de corte y maquinaria con sulfato de cobre al 10% o formalina.",
        "Optimizar el drenaje del suelo para evitar encharcamientos.",
        "Eliminar plantas voluntarias y malezas que puedan servir como reservorios de la bacteria."
    ],
    "Sana": [
        "La planta está sana. Mantenga prácticas adecuadas de cultivo."
    ],
    "Virus": [
        "Usar tubérculos-semilla certificados y libres de virus.",
        "Implementar cultivos trampa en los bordes del campo para desviar áfidos.",
        "Monitorear áfidos mediante trampas adhesivas y aplicar insecticidas adecuados.",
        "Eliminar plantas infectadas, malezas y plantas voluntarias que actúen como reservorios.",
        "Desinfectar herramientas, maquinaria, calzado y vestimenta entre actividades.",
        "Realizar rotaciones de cultivos con especies no hospederas para reducir la acumulación de virus en el suelo.",
        "Reducir el tráfico en el campo para evitar la diseminación mecánica."
    ]
}

# Ruta principal para la interfaz gráfica
@app.route('/')
def home():
    return render_template('index.html')

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
        print("Procesando la imagen...")
        img = tf.keras.utils.load_img(BytesIO(file.read()), target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Realizar predicción
        print("Realizando predicción...")
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)
        clase_predicha = class_labels[predicted_class]
        probabilidad_clase = predictions[0][predicted_class] * 100

        # Obtener recomendaciones específicas
        recomendaciones = all_recommendations.get(clase_predicha, ["No hay recomendaciones disponibles para esta clase."])

        print(f"Predicción exitosa: {clase_predicha} ({probabilidad_clase:.2f}%)")
        return jsonify({
            "predicted_class": clase_predicha,
            "confidence": f"{probabilidad_clase:.2f}%",
            "specific_recommendations": recomendaciones
        })
    except Exception as e:
        print(f"Error procesando la imagen: {str(e)}")
        return jsonify({"error": f"Error procesando la imagen: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
