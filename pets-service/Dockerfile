FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Copiar certificado dentro de la imagen
COPY certs/BaltimoreCyberTrustRoot.pem /etc/ssl/certs/BaltimoreCyberTrustRoot.pem

# Variables SSL para Python
ENV SSL_CERT_FILE=/etc/ssl/certs/BaltimoreCyberTrustRoot.pem
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/BaltimoreCyberTrustRoot.pem

# Iniciar FastAPI con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
