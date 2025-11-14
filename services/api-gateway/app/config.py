import os
from dotenv import load_dotenv

load_dotenv()

# ===============================
# 🔹 Configuración general
# ===============================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# ===============================
# 🔹 URLs de microservicios
# ===============================
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
PETS_SERVICE_URL = os.getenv("PETS_SERVICE_URL")
APPOINTMENTS_SERVICE_URL = os.getenv("APPOINTMENTS_SERVICE_URL")
