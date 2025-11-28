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
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
PETS_SERVICE_URL = os.getenv("PETS_SERVICE_URL", "http://pets-service:8000")
APPOINTMENTS_SERVICE_URL = os.getenv("APPOINTMENTS_SERVICE_URL", "http://appointment-service:8000")
REWARDS_SERVICE_URL = os.getenv("REWARDS_SERVICE_URL", "http://rewards-service:8000")
POSTCONSULT_SERVICE_URL = os.getenv("POSTCONSULT_SERVICE_URL", "http://postconsult-service:8000")
