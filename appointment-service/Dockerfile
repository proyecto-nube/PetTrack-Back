FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8002

WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del servicio
COPY . .

# Exponer puerto
EXPOSE 8000

# Iniciar app correctamente apuntando al main que sí existe
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
