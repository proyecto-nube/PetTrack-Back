from fastapi import FastAPI, HTTPException
from bson import ObjectId
from .database import get_collection
from .models import Reward, Redemption
from .schemas import RewardCreate, RewardResponse, RedemptionCreate, RedemptionResponse

app = FastAPI(title="Rewards Service", version="1.0")

rewards_col = get_collection("rewards")
redemptions_col = get_collection("redemptions")

# ------------------------
# 1️⃣ Crear recompensa
# ------------------------
@app.post("/rewards", response_model=RewardResponse)
def create_reward(data: RewardCreate):
    doc = data.dict()
    result = rewards_col.insert_one(doc)
    return {**doc, "id": str(result.inserted_id)}

# ------------------------
# 2️⃣ Listar recompensas
# ------------------------
@app.get("/rewards", response_model=list[RewardResponse])
def list_rewards():
    rewards = list(rewards_col.find({}))
    for r in rewards:
        r["id"] = str(r["_id"])
        del r["_id"]
    return rewards

# ------------------------
# 3️⃣ Registrar canje
# ------------------------
@app.post("/redeem", response_model=RedemptionResponse)
def redeem_reward(data: RedemptionCreate):
    doc = {
        "user_id": data.user_id,
        "reward_id": data.reward_id,
        "reward_name": data.reward_name,
        "points": data.points,
        "status": "Pendiente",
    }
    result = redemptions_col.insert_one(doc)
    return {**doc, "id": str(result.inserted_id)}

# ------------------------
# 4️⃣ Historial de canjes por usuario
# ------------------------
@app.get("/redemptions/{user_id}", response_model=list[RedemptionResponse])
def user_redemptions(user_id: str):
    docs = list(redemptions_col.find({"user_id": user_id}))
    redemptions = []
    for d in docs:
        d["id"] = str(d["_id"])
        del d["_id"]
        redemptions.append(d)
    return redemptions
