from dotenv import load_dotenv
import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
import identity.web
import requests
import app_config

# Cargar el archivo .env
load_dotenv()

# Verificar que las variables se cargan correctamente
print(f"CLIENT_ID: {os.getenv('CLIENT_ID')}")
print(f"AUTHORITY: {os.getenv('AUTHORITY')}")
print(f"CLIENT_SECRET: {os.getenv('CLIENT_SECRET')}")

# Definimos versión
__version__ = "1.0.0"

# Inicializar la aplicación, para crear una instancia
app = Flask(__name__, static_url_path='', static_folder='static')
app.config.from_object(app_config)  # Importa la configuración desde app_config
assert app.config["REDIRECT_PATH"] != "/", "REDIRECT_PATH must not be /"  # Comprueba que la redirect URL no es / que sería la raíz del sitio
Session(app)

# Configuración del middleware ProxyFix para el desarrollo local, modifica el esquema de la URL para que funcione en local
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Actualizar variables Globales de Jinja
app.jinja_env.globals.update(Auth=identity.web.Auth)  # Agrega variable global llamada Auth, será accesible desde los HTMLs

# Inicialización del Objeto de Autenticación
print("Initializing Auth object")
auth = identity.web.Auth(
    session=session,
    authority=app.config["AUTHORITY"],
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
)

# Primera etapa del flujo de autorización
@app.route("/login")
def login(): 
    print("Login route accessed")
    return render_template("login.html", version=__version__, **auth.log_in(
        scopes=app_config.SCOPE,
        redirect_uri=url_for("auth_response", _external=True),
        prompt="select_account",
    ))

# Segunda etapa del flujo de autorización: manejar la respuesta de autenticación
@app.route(app_config.REDIRECT_PATH)
def auth_response(): 
    print("Auth response route accessed")
    result = auth.complete_log_in(request.args)
    if "error" in result:
        print("Authentication error:", result)
        return render_template("auth_error.html", result=result)
    return redirect(url_for("index"))

# Para cerrar la sesión
@app.route("/logout")
def logout(): 
    print("Logout route accessed")
    return redirect(auth.log_out(url_for("index", _external=True)))

# Controla solo mostrar la página principal solo si el usuario está autenticado y tiene todo lo necesario
@app.route("/")
def index():
    print("Index route accessed")
    if not (app.config["CLIENT_ID"] and app.config["CLIENT_SECRET"]):
        print("Config error: CLIENT_ID or CLIENT_SECRET missing")
        return render_template('config_error.html')
    if not auth.get_user():
        print("No authenticated user, redirecting to login")
        return redirect(url_for("login"))
    return render_template('index.html', user=auth.get_user(), version=__version__)

# Define la ruta que maneja solicitudes a /call_downstream_api
@app.route("/call_downstream_api")
def call_downstream_api():
    print("Call downstream API route accessed")
    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        print("Error obtaining token:", token)
        return redirect(url_for("login"))
    api_result = requests.get(
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        timeout=30,
    ).json()
    return render_template('display.html', result=api_result)

# Para ejecutar la aplicación
if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
