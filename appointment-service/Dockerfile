FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del servicio
COPY . .

# Exponer puerto (Azure asignará PORT dinámicamente, 8002 es fallback)
EXPOSE 8002

# Iniciar app usando PORT de Azure o 8002 como fallback
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8002}"]
