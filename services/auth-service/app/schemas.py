from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Creación de usuario ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str  # 'user', 'doctor', 'admin'

# --- Login ---
class UserLogin(BaseModel):
    username: str
    password: str

# --- Respuesta general ---
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True

# --- Token ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- 🔹 NUEVO esquema para editar usuarios ---
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
