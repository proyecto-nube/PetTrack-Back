from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import jwt
import httpx
from .config import (
    AUTH_SERVICE_URL,
    PETS_SERVICE_URL,
    APPOINTMENTS_SERVICE_URL,
    SECRET_KEY,
    ALGORITHM,
)
from .proxy import forward_request

app = FastAPI(title="API Gateway")

# ======================================
# 🔹 Configurar CORS para acceso desde React local
# ======================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",        # producción
        "http://127.0.0.1",
        "http://localhost:5173",   # desarrollo (Vite)
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ======================================
# 🔹 Rutas Proxy para Microservicios
# ======================================
@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def auth_proxy(path: str, request: Request):
    """Proxy para el servicio de autenticación"""
    return await forward_request(request, AUTH_SERVICE_URL, f"/{path}")

@app.api_route("/pets/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def pets_proxy(path: str, request: Request):
    """Proxy para el servicio de mascotas"""
    return await forward_request(request, PETS_SERVICE_URL, f"/{path}")

@app.api_route("/appointments/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def appointments_proxy(path: str, request: Request):
    """Proxy para el servicio de citas"""
    return await forward_request(request, APPOINTMENTS_SERVICE_URL, f"/{path}")

@app.api_route("/postconsult/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def postconsult_proxy(path: str, request: Request):
    """Proxy para el servicio de postconsultas"""
    return await forward_request(request, POSTCONSULT_SERVICE_URL, f"/{path}")

@app.api_route("/rewards/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def rewards_proxy(path: str, request: Request):
    """Proxy para el servicio de recompensas"""
    return await forward_request(request, REWARDS_SERVICE_URL, f"/{path}")

# ======================================
# 🔹 Endpoint raíz (salud del gateway)
# ======================================
@app.get("/")
def root():
    return {
        "message": "🚀 API Gateway operativo",
        "routes": ["/auth/*", "/pets/*", "/appointments/*", "/dashboard"],
        "services": {
            "auth": AUTH_SERVICE_URL,
            "pets": PETS_SERVICE_URL,
            "appointments": APPOINTMENTS_SERVICE_URL,
        },
    }

# ======================================
# 🔹 Nuevo endpoint: /dashboard
#    Detecta el rol del usuario automáticamente
# ======================================
@app.get("/dashboard")
async def redirect_dashboard(token: str = Depends(oauth2_scheme)):
    """
    Analiza el token JWT y redirige al dashboard correspondiente según el rol.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        if not role:
            raise HTTPException(status_code=400, detail="Token sin rol")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/dashboard/{role}",
                headers={"Authorization": f"Bearer {token}"}
            )
            return response.json()

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
