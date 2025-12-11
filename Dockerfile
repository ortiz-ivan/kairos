# Multi-stage Dockerfile para Kairos
# Etapa 1: builder (instalar dependencias)
# Etapa 2: runtime (imagen final lean)

FROM python:3.10-slim AS builder

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Instalar dependencias de compilación (necesarias para algunos paquetes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y crear wheels
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir -r requirements.txt -w /wheels

# ========================================
# Etapa 2: Runtime
# ========================================
FROM python:3.10-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_ENV=production

# Instalar solo dependencias de runtime (no de compilación)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar wheels de la etapa builder e instalar
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

# Copiar código de la aplicación
COPY . /app

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Exponer puerto
EXPOSE 8000

# Comando de inicio: ejecutar Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]
