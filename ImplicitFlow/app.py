import identity.web
import requests
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session

import app.config

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


# Primera etapa del flujo de autorización (Implicit Flow)
@app.route("/login")  # Define la ruta en Flask para manejar las solicitudes a /login
def login(): 
    auth_url = (
        f"{app.config['AUTHORITY']}/oauth2/v2.0/authorize"
        f"?client_id={app.config['CLIENT_ID']}"
        f"&response_type=token"
        f"&redirect_uri={url_for('auth_response', _external=True)}"
        f"&scope={' '.join(app_config.SCOPE)}"
        f"&prompt=select_account"
    )
    return redirect(auth_url)

# Segunda etapa del flujo de autorización: manejar la respuesta de autenticación (Implicit Flow)
@app.route(app_config.REDIRECT_PATH, methods=["GET", "POST"])
def auth_response(): 
    if request.method == "POST":
        access_token = request.form.get("access_token")
        if access_token:
            session["access_token"] = access_token
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))
    return render_template("auth_response.html")

# Para cerrar la sesión
@app.route("/logout")  # Define ruta Flask para logout
def logout(): 
    session.pop("access_token", None)
    return redirect(url_for("index"))

# Controla solo mostrar la página principal solo si el usuario está autenticado y tiene todo lo necesario
@app.route("/")
def index():
    if not app.config["CLIENT_ID"]:
        return render_template('config_error.html')
    if "access_token" not in session:
        return redirect(url_for("login"))
    return render_template('index.html', user={"name": "User"}, version=__version__)

# Define la ruta que maneja solicitudes a /call_downstream_api
@app.route("/call_downstream_api")
def call_downstream_api():
    if "access_token" not in session:
        return redirect(url_for("login"))
    api_result = requests.get(
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + session["access_token"]},
        timeout=30,
    ).json()
    return render_template('display.html', result=api_result)

# Para ejecutar la aplicación
if __name__ == "__main__":
    app.run()