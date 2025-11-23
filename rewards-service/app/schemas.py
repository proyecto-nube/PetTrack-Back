from pydantic import BaseModel
from datetime import datetime

class RewardCreate(BaseModel):
    title: str
    desc: str
    cost: int
    img: str

class RewardResponse(RewardCreate):
    id: str

class RedemptionCreate(BaseModel):
    user_id: str
    reward_id: str
    reward_name: str
    points: int

class RedemptionResponse(RedemptionCreate):
    id: str
    status: str
    created_at: datetime
