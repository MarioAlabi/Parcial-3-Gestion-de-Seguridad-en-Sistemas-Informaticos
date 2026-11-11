FROM python:3.11-slim

# Evitar generación de .pyc y permitir que los logs salgan inmediatamente a la consola
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Exponer el puerto de la aplicación Flask
EXPOSE 5000

# Usuario no privilegiado para mejores prácticas de seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Comando de inicio
CMD ["python", "app.py"]

