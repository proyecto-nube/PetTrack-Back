# =========================
# Dockerfile - Postconsult Service
# =========================

FROM python:3.11-slim

# 1️⃣ Variables de entorno
ENV PYTHONUNBUFFERED=1

# 2️⃣ Directorio de trabajo
WORKDIR /app

# 3️⃣ Instalar dependencias del sistema necesarias para SSL
RUN apt-get update \
    && apt-get install -y ca-certificates wget \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copiar el código de la app
COPY ./app ./app

# 6️⃣ Copiar certificado DigiCert desde ./certs/ y actualizar trust store
# En CI/CD, este archivo se crea desde un secret antes del build
# COPY ./certs/DigiCertGlobalRootG2.crt.pem /usr/local/share/ca-certificates/DigiCertGlobalRootG2.crt
# RUN update-ca-certificates

# 7️⃣ Puerto expuesto
EXPOSE 8000

# 8️⃣ Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
