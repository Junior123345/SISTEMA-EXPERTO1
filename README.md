Detector de Enfermedades en Papa
Este proyecto utiliza Flask y TensorFlow para detectar enfermedades en plantas de papa a partir de imágenes. También incluye autenticación de usuario mediante Google OAuth y un panel para gestionar el historial de consultas.

Características principales
Diagnóstico:
Tizón tardío
Tizón temprano
Pudrición parda
Virus
Plantas sanas
Recomendaciones específicas basadas en el diagnóstico.
Autenticación de usuario con Google OAuth.
Panel de usuario para consultar el historial de diagnósticos.
Configuración segura con sesiones protegidas.
Requisitos previos
Python 3.8 o superior
Bibliotecas necesarias (se instalan desde requirements.txt):
Flask
Authlib
TensorFlow
NumPy
Instalación
Clona el repositorio:

bash
Copiar código
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
Crea y activa un entorno virtual:

bash
Copiar código
python -m venv env
source env/bin/activate   # Linux/MacOS
env\Scripts\activate      # Windows
Instala las dependencias:

bash
Copiar código
pip install -r requirements.txt
Configuración
Configura tus credenciales de Google OAuth:

Ve a Google Cloud Console.
Crea un proyecto y habilita las APIs:
Google People API
Google OAuth 2.0
Configura las "URIs de redirección autorizadas":
http://127.0.0.1:5000/login/callback
http://localhost:5000/login/callback
Descarga el archivo client_secret.json y colócalo en la raíz del proyecto.
Configura las variables de entorno:

Define una clave secreta para Flask:
bash
Copiar código
export SECRET_KEY="clave_secreta_segura"  # Linux/MacOS
set SECRET_KEY=clave_secreta_segura       # Windows
Coloca tu modelo preentrenado en la carpeta modelos/ con el nombre modelo_papa.keras.

Ejecución
Inicia la aplicación:

bash
Copiar código
python app.py
Abre tu navegador y ve a:

arduino
Copiar código
http://127.0.0.1:5000
Uso
Inicio de sesión:

Haz clic en "Iniciar sesión con Google".
Autoriza la aplicación.
Serás redirigido al panel de usuario.
Subir imágenes:

Sube una imagen de una planta de papa.
Recibe el diagnóstico y las recomendaciones específicas.
Estructura del proyecto
php
Copiar código
<PROYECTO>/
│
├── app.py                  # Archivo principal de la aplicación
├── client_secret.json      # Credenciales de Google OAuth
├── requirements.txt        # Lista de dependencias
├── modelos/
│   └── modelo_papa.keras   # Modelo entrenado para detección
├── templates/
│   ├── index.html          # Página principal
│   └── dashboard.html      # Panel de usuario
├── static/
│   ├── css/                # Estilos CSS
│   └── js/                 # Scripts JavaScript
└── README.md               # Documentación del proyecto
Tecnologías utilizadas
Flask: Framework web.
TensorFlow: Para la detección de enfermedades.
Authlib: Para la autenticación con Google OAuth.
Bootstrap: Para el diseño de la interfaz.
NumPy: Procesamiento de datos.
Contribuciones
Si quieres contribuir al proyecto:

Haz un fork del repositorio.
Crea una rama para tus cambios:
bash
Copiar código
git checkout -b feature/nueva-funcion
Realiza tus cambios y súbelos:
bash
Copiar código
git commit -m "Descripción de tus cambios"
git push origin feature/nueva-funcion
Envía un Pull Request.
Licencia
Este proyecto está licenciado bajo la MIT License.

Autor
[Tu Nombre]
Correo: [tuemail@example.com]
LinkedIn: https://www.linkedin.com/in/tu-perfil
GitHub: https://github.com/tu-usuario

Notas adicionales
Este proyecto fue diseñado para fines educativos y demostrativos.
Para producción:
Usa SESSION_COOKIE_SECURE = True.
Despliega en un servidor HTTPS.
Utiliza un administrador de secretos para manejar las credenciales de manera segura.