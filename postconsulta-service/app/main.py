from fastapi import FastAPI
from app.database import Base, engine
from app import postconsultas

# Crear las tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PostConsulta Service")

# Registrar el router
app.include_router(postconsultas.router)

@app.get("/")
def root():
    return {"message": "Servicio de Postconsultas activo 🚀"}
