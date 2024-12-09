import os

# Configuración de la aplicación
AUTHORITY= os.getenv("AUTHORITY")

# ID del cliente de la aplicación registrada
CLIENT_ID = os.getenv("CLIENT_ID")
# Secreto del cliente generado por la aplicación: nunca lo subas al control de versiones
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
 
# Ruta de redirección después del login 
REDIRECT_PATH = "/getAToken"  

# Endpoint de la API a la que se llama
ENDPOINT = 'https://graph.microsoft.com/v1.0/me'  

# Ámbito de los permisos requeridos
SCOPE = ["User.Read"]

# Dice a la Flask-session extension almacenar las sesiones en el sistema de archivos
SESSION_TYPE = "filesystem" 