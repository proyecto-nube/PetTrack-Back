from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os
from typing import List

from . import models, schemas
from .database import Base, engine, get_db
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Auth Service")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# --- Funciones de seguridad ---
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

# --- Decorador de roles ---
def role_required(allowed_roles: List[str]):
    def wrapper(user: models.User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para esta acción")
        return user
    return wrapper

# --- Endpoints ---
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="El email ya está en uso")
    
    if user.role not in ["user", "doctor", "admin"]:
        raise HTTPException(status_code=400, detail="Rol no válido")
    
    if len(user.password) > 72:
        raise HTTPException(status_code=400, detail="La contraseña no puede superar 72 caracteres")

    hashed_pw = pwd_context.hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        role=user.role,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not user or not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    }

@app.get("/profile", response_model=schemas.UserResponse)
def get_profile(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/users", response_model=List[schemas.UserResponse])
def list_users(current_user: models.User = Depends(role_required(["admin", "doctor"])), db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# ======================================
# 🔹 Nuevo endpoint para dashboard por rol
# ======================================
@app.get("/dashboard/{role}")
def dashboard(role: str, current_user: models.User = Depends(get_current_user)):
    if role == "admin":
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Acceso restringido a administradores")
        return {"message": f"Bienvenido al dashboard de administrador, {current_user.username}"}
    
    elif role == "doctor":
        if current_user.role != "doctor":
            raise HTTPException(status_code=403, detail="Acceso restringido a doctores")
        return {"message": f"Bienvenido al dashboard de doctor, {current_user.username}"}
    
    elif role == "user":
        if current_user.role != "user":
            raise HTTPException(status_code=403, detail="Acceso denegado a este recurso")
        return {"message": f"Bienvenido al dashboard de usuario, {current_user.username}"}
    
# ============================================================
# 🔹 Eliminar usuario (solo admin)
# ============================================================
@app.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(role_required(["admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()
    return {"message": f"Usuario con ID {user_id} eliminado correctamente"}


# ============================================================
# 🔹 Editar usuario (solo admin)
# ============================================================
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    updated_data: schemas.UserUpdate,  # debes crear este esquema en schemas.py
    db: Session = Depends(get_db),
    current_user: models.User = Depends(role_required(["admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar campos básicos (solo si vienen en la solicitud)
    if updated_data.username:
        user.username = updated_data.username
    if updated_data.email:
        user.email = updated_data.email
    if updated_data.role:
        if updated_data.role not in ["user", "doctor", "admin"]:
            raise HTTPException(status_code=400, detail="Rol no válido")
        user.role = updated_data.role
    if updated_data.password:
        user.hashed_password = pwd_context.hash(updated_data.password)

    db.commit()
    db.refresh(user)
    return user

@app.on_event("startup")
def startup_event():
    port = int(os.getenv("PORT", 8000))
    app_name = os.getenv("APP_NAME")
    auth_api_url = os.getenv("AUTH_API_URL")
    print(f"✅ {app_name} listening on http://localhost:{port}")
    print(f"Auth Service is running. API URL: {auth_api_url}")
    print("Ready to handle authentication requests.")