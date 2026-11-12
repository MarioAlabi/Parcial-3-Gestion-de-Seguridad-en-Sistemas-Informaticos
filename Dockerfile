FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias
COPY Laboratorio_XSS/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el ecosistema del proyecto (Portal, Ebooks, Revista, Informes, PDFs, Simulador)
COPY . .

WORKDIR /app/Laboratorio_XSS

EXPOSE 5000

# Usuario no privilegiado para buenas prácticas de seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "app.py"]
