from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Reward(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    desc: str
    cost: int
    img: str

class Redemption(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    reward_id: str
    reward_name: str
    points: int
    status: str = "Pendiente"
    created_at: datetime = datetime.utcnow()
