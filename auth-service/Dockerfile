FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias de sistema necesarias para pymysql y certificados
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando para arrancar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
