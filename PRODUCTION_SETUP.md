# Configuración de Producción - Kairos

Este documento describe cómo desplegar Kairos en un entorno de producción usando Docker y docker-compose.

## 📋 Requisitos

- Docker y docker-compose instalados
- Variables de entorno configuradas en un archivo `.env`
- PostgreSQL 15+ para base de datos en producción
- (Opcional) Nginx como reverse proxy

## 🏗️ Estructura

### Archivos de Configuración

1. **config.py**
   - Configuración basada en ambiente (Development, Production, Testing)
   - Maneja rutas de base de datos, cookies seguras, niveles de logging
   - Lee variables de entorno y proporciona valores por defecto seguros

2. **wsgi.py**
   - Punto de entrada para servidores WSGI (Gunicorn)
   - Exporta la instancia de la app: `app`
   - Comando recomendado:
     ```bash
     gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 wsgi:app
     ```

3. **.env.example**
   - Plantilla de variables de entorno
   - Copiar a `.env` y llenar con valores reales
   - **NUNCA** commitear `.env` a control de versiones

4. **Dockerfile**
   - Build de imagen Docker multi-stage
   - Imagen base: `python:3.10-slim` (lean, segura)
   - Características:
     - Build optimizado (builder + runtime)
     - Usuario no-root: `appuser` (uid 1000)
     - Health check con curl: `GET /health`
     - Gunicorn pre-configurado (4 workers, 120s timeout)

5. **.dockerignore**
   - Excluye archivos innecesarios del build context
   - Reduce tamaño de imagen: .git, __pycache__, *.db, logs/, .env, venv/, etc.

6. **docker-compose.yml**
   - Stack local para desarrollo/staging
   - Servicios:
     - **web**: Flask app en Gunicorn (puerto 8000)
     - **db**: PostgreSQL 15 (puerto 5432)
     - **nginx**: Reverse proxy (puerto 80)
   - Volumes:
     - `postgres_data`: Persistencia de BD
     - Bind mount (código, solo lectura en prod)
   - Health checks en ambos servicios
   - Comando de inicialización: `flask db upgrade`

7. **nginx.conf**
   - Configuración de reverse proxy
   - Rate limiting por zona (API, general)
   - Headers de seguridad (X-Forwarded-*, WebSocket support)
   - Gzip compression habilitada

## 🚀 Deployment

### 1. Preparar variables de entorno

```bash
cp .env.example .env
# Editar .env con valores reales:
# - SECRET_KEY: Token aleatorio seguro (al menos 32 caracteres)
# - DATABASE_URL: postgresql://user:pass@db:5432/kairos
# - ADMIN_PASSWORD: Contraseña admin inicial
# - SENTRY_DSN: (Opcional) Para error tracking
```

### 2. Levantar stack completo

```bash
# Desarrollo/staging
docker-compose up -d

# Build de imagen (si hay cambios en Dockerfile)
docker-compose build --no-cache
docker-compose up -d

# Ver logs
docker-compose logs -f web
docker-compose logs -f db
```

### 3. Ejecutar migraciones de base de datos

El docker-compose.yml incluye el comando automáticamente:
```bash
flask db upgrade
```

Si necesitas ejecutarlo manualmente:
```bash
docker-compose exec web flask db upgrade
```

### 4. Verificar health check

```bash
# Desde el host
curl http://localhost:8000/health
# Respuesta esperada: {"status":"ok","database":"connected"}

# Desde el container web
docker-compose exec web curl http://localhost:8000/health
```

### 5. Crear usuario admin (si aplica)

```bash
docker-compose exec web flask shell
>>> from models_alchemy import db, User
>>> admin = User(...)
>>> db.session.add(admin)
>>> db.session.commit()
```

## 🔒 Seguridad

### En Producción:

1. **SECRET_KEY**: Generar con `os.urandom(24).hex()` o `secrets.token_hex(24)`
   ```python
   import secrets
   print(secrets.token_hex(24))
   ```

2. **DATABASE_URL**: Usar credenciales fuertes en PostgreSQL
   ```
   postgresql://kairos_user:strong_password_here@db.example.com:5432/kairos_db
   ```

3. **HTTPS**: Configurar certificado SSL en Nginx/reverse proxy
   - Redirigir HTTP → HTTPS
   - HSTS headers: `Strict-Transport-Security: max-age=31536000`

4. **Environment variables**: Usar secrets management
   - AWS Secrets Manager
   - HashiCorp Vault
   - GitHub Secrets (para CI/CD)

5. **Cookies seguras**:
   - `SESSION_COOKIE_SECURE=True` (solo HTTPS)
   - `SESSION_COOKIE_SAMESITE=Strict` (CSRF protection)
   - `SESSION_COOKIE_HTTPONLY=True` (no accessible from JS)

6. **Rate limiting**: Configurado en nginx.conf
   - API endpoints: 100 req/s
   - General: 500 req/s

### Logs

- Incluidos en stdout/stderr del container (Docker standard)
- Redireccionar a servicio de logging:
  - ELK Stack (Elasticsearch, Logstash, Kibana)
  - Splunk
  - Datadog
  - Sentry (para errores)

## 📊 Monitoreo

### Health Check Endpoint

```
GET /health
```

Respuesta:
```json
{
  "status": "ok",
  "database": "connected"
}
```

Status codes:
- `200`: Healthy
- `503`: Unhealthy (DB disconnected)

### Métricas (Opcional)

Agregar Prometheus/Grafana:
```dockerfile
# En docker-compose.yml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

## 🔄 CI/CD Integration

### GitHub Actions (ejemplo)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build image
        run: docker build -t kairos:latest .
      - name: Push to registry
        run: docker push kairos:latest
      - name: Deploy
        run: |
          ssh user@prod.example.com 'cd /app && docker-compose pull && docker-compose up -d'
```

## 📝 Logs

- Flask: `logs/kairos.log` (local dev)
- Docker: `docker-compose logs [service]`
- Nginx: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`

## 🛑 Troubleshooting

### Container no inicia
```bash
docker-compose logs web
# Verificar: SECRET_KEY, DATABASE_URL, permisos de directorios
```

### Health check falla
```bash
docker-compose exec web flask shell
>>> from models_alchemy import db
>>> db.session.execute('SELECT 1')
# Verificar conexión a BD
```

### Database migration error
```bash
docker-compose exec web flask db current
docker-compose exec web flask db heads
docker-compose exec web flask db upgrade
```

### Limpiar todo y reiniciar
```bash
docker-compose down -v  # Elimina volumes
docker-compose up -d --build
docker-compose exec web flask db upgrade
```

## 📚 Referencias

- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Flask-Migrate: https://flask-migrate.readthedocs.io/
- Gunicorn: https://gunicorn.org/
- Docker: https://docs.docker.com/
- Nginx: https://nginx.org/en/docs/

---

**Última actualización**: 2025-12-11
**Versión de Python**: 3.10+
**Base de datos**: PostgreSQL 15+
