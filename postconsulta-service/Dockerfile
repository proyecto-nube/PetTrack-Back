# =============================
# Imagen base ligera de Python
# =============================
FROM python:3.11-slim

# Configuración básica
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias del proyecto
COPY requirements.txt .

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto de la aplicación
EXPOSE 8004

# Comando de arranque
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]
