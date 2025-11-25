FROM python:3.11-slim

# Crear carpeta de trabajo
WORKDIR /app

# Copiar requirements primero
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la app completa
COPY . .

# Crear carpeta de certificados dentro de la imagen
RUN mkdir -p /app/certs

# Copiar certificados desde tu repo
COPY certs /app/certs

# Permisos opcionales (si es necesario)
RUN chmod -R 644 /app/certs

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
