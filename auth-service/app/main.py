from fastapi import FastAPI, Depends, HTTPException, status, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
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

# --- Funciones de seguridad ---
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Token no encontrado en cookie")
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
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

    response = JSONResponse(content={
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    })
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="None",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return response

@app.post("/logout")
def logout():
    response = JSONResponse(content={"message": "Sesión cerrada correctamente"})
    response.delete_cookie("access_token")
    return response

@app.get("/profile", response_model=schemas.UserResponse)
def get_profile(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/users", response_model=List[schemas.UserResponse])
def list_users(current_user: models.User = Depends(role_required(["admin", "doctor"])), db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/dashboard/{role}")
def dashboard(role: str, current_user: models.User = Depends(get_current_user)):
    if role == "admin" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acceso restringido a administradores")
    if role == "doctor" and current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Acceso restringido a doctores")
    if role == "user" and current_user.role != "user":
        raise HTTPException(status_code=403, detail="Acceso denegado a este recurso")
    return {"message": f"Bienvenido al dashboard de {role}, {current_user.username}"}

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(role_required(["admin"]))):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"message": f"Usuario con ID {user_id} eliminado correctamente"}

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, updated_data: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(role_required(["admin"]))):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
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

@app.get("/health")
def health():
    return {"status": "Auth service is healthy"}

@app.get("/")
def root():
    return {"message": "Welcome to the Auth Service"}

@app.on_event("startup")
def startup_event():
    print("Auth service started correctly inside Azure Container")