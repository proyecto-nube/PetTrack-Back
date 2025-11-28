import os
from dotenv import load_dotenv

load_dotenv()

# 🔐 Validar que SECRET_KEY esté configurada
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # 🔄 Fallback para desarrollo - NO usar en producción
    import secrets
    SECRET_KEY = secrets.token_urlsafe(32)
    print(f"⚠️  SECRET_KEY no configurada. Usando fallback temporal: {SECRET_KEY[:10]}...")
    print("🚨 IMPORTANTE: Configura SECRET_KEY en variables de entorno para producción!")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY_BASE64 = os.getenv("SECRET_KEY_BASE64")
