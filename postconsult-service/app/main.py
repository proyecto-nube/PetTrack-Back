from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import requests
import os

from .database import get_collection
from .models import Reward, Redemption
from .schemas import RewardCreate, RewardResponse, RedemptionCreate, RedemptionResponse

app = FastAPI(title="Rewards Service", version="1.0")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

rewards_col = get_collection("rewards")
redemptions_col = get_collection("redemptions")

# ----------------------------------------------------
# ➤ Obtener usuario desde el auth-service (incluye rol)
# ----------------------------------------------------
def get_user(token: str = Depends(oauth2_scheme)):
    r = requests.get(
        f"{AUTH_SERVICE_URL}/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Token inválido")
    return r.json()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ----------------------------------------------------
# 1️⃣ Crear recompensa (solo ADMIN)
# ----------------------------------------------------
@app.post("/rewards", response_model=RewardResponse)
def create_reward(data: RewardCreate, user=Depends(get_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede crear recompensas")

    doc = data.dict()
    result = rewards_col.insert_one(doc)
    return {**doc, "id": str(result.inserted_id)}

# ----------------------------------------------------
# 2️⃣ Listar recompensas (admin, doctor, owner)
# ----------------------------------------------------
@app.get("/rewards", response_model=list[RewardResponse])
def list_rewards(user=Depends(get_user)):
    if user["role"] not in ["admin", "doctor", "owner"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    rewards = list(rewards_col.find({}))
    for r in rewards:
        r["id"] = str(r["_id"])
        del r["_id"]
    return rewards

# ----------------------------------------------------
# 3️⃣ Registrar canje (solo OWNER)
# ----------------------------------------------------
@app.post("/redeem", response_model=RedemptionResponse)
def redeem_reward(data: RedemptionCreate, user=Depends(get_user)):
    if user["role"] != "owner":
        raise HTTPException(status_code=403, detail="Solo los dueños pueden canjear recompensas")

    # Validar que solo canjee para sí mismo
    if data.user_id != str(user["id"]):
        raise HTTPException(status_code=403, detail="Solo puedes canjear tus propias recompensas")

    doc = {
        "user_id": data.user_id,
        "reward_id": data.reward_id,
        "reward_name": data.reward_name,
        "points": data.points,
        "status": "Pendiente",
    }
    result = redemptions_col.insert_one(doc)
    return {**doc, "id": str(result.inserted_id)}

# ----------------------------------------------------
# 4️⃣ Ver redenciones por usuario
#     owner → solo las suyas
#     admin → todas
# ----------------------------------------------------
@app.get("/redemptions/{user_id}", response_model=list[RedemptionResponse])
def user_redemptions(user_id: str, user=Depends(get_user)):
    if user["role"] == "owner" and user_id != str(user["id"]):
        raise HTTPException(status_code=403, detail="Solo puedes ver tus propios canjes")

    docs = list(redemptions_col.find({"user_id": user_id}))
    redemptions = []
    for d in docs:
        d["id"] = str(d["_id"])
        del d["_id"]
        redemptions.append(d)
    return redemptions

# Healthcheck
@app.get("/health")
def health():
    return {"service": "rewards-service", "status": "ok"}
