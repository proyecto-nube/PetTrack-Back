FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copiar certificados correctos desde /certs dentro del servicio
COPY certs/BaltimoreCyberTrustRoot.crt.pem /etc/ssl/certs/BaltimoreCyberTrustRoot.pem
COPY certs/DigiCertGlobalRootCA.crt.pem /etc/ssl/certs/DigiCertGlobalRootCA.pem

# Variable SSL para que Python use los certificados
ENV SSL_CERT_FILE=/etc/ssl/certs/BaltimoreCyberTrustRoot.pem

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
