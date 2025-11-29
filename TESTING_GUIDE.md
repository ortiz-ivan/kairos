# Guía de Testing y Quality Assurance

## 🧪 Testing Local

### Instalación Inicial (Solo una vez)

```bash
# Instalar todas las dependencias de desarrollo
pip install -r requirements.txt

# Instalar pre-commit hooks (importante!)
pre-commit install
```

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con output detallado
pytest -v

# Ejecutar un archivo específico
pytest tests/test_products_crud.py -v

# Ejecutar un test específico
pytest tests/test_products_crud.py::test_products_crud -v

# Ejecutar con reporte de cobertura
pytest --cov=. --cov-report=html --cov-report=term-missing

# Ver reporte de cobertura en navegador
pytest --cov=. --cov-report=html
# Abrir: htmlcov/index.html
```

### Pre-commit Hooks

**¿Qué son?** Validaciones automáticas que se ejecutan **antes** de hacer commit.

**Instalado automáticamente después de:** `pre-commit install`

**Hooks activos:**

1. **trailing-whitespace** - Elimina espacios al final de líneas
2. **end-of-file-fixer** - Asegura newline al final de archivos
3. **check-yaml** - Valida sintaxis YAML
4. **check-json** - Valida sintaxis JSON
5. **check-merge-conflict** - Detecta marcas de merge conflict
6. **debug-statements** - Detecta `pdb`, `breakpoint()`, etc.
7. **black** - Formatea código Python (máx 88 caracteres)
8. **flake8** - Linting (máx 120 caracteres, detecta errores comunes)
9. **isort** - Ordena imports automáticamente

**Ejecutar manualmente (sin hacer commit):**

```bash
# Ejecutar todos los hooks en todos los archivos
pre-commit run --all-files

# Ejecutar hook específico
pre-commit run black --all-files
pre-commit run flake8 --all-files
pre-commit run isort --all-files

# Ejecutar en archivos staged solamente
pre-commit run
```

**Flujo típico de desarrollo:**

```bash
# 1. Hacer cambios en código
vim models/producto.py

# 2. Preparar para commit
git add .

# 3. Pre-commit se ejecuta automáticamente
# Si hay errores, se muestran y algunos se auto-arreglan
# Debes revisar los cambios y hacer add nuevamente

git add .  # Re-agregar archivos arreglados

# 4. Hacer commit
git commit -m "Agregar validación de productos"

# 5. Push
git push
```

## 🚀 GitHub Actions (CI/CD)

**¿Qué es?** Tests que se ejecutan automáticamente en GitHub cuando haces:

- Push a `main` o `develop`
- Pull Request a `main` o `develop`

**Matriz de testing:** Python 3.9, 3.10, 3.11

**Pasos del workflow:**

1. Checkout del código
2. Instalación de Python y dependencias
3. Ejecución de pytest
4. Reporte de cobertura a Codecov

**Ver resultados:**

1. Ir a: https://github.com/ortiz-ivan/kairos/actions
2. Seleccionar el workflow "Tests"
3. Ver detalles de ejecución

**Badge de status:**

```markdown
![Tests](https://github.com/ortiz-ivan/kairos/actions/workflows/tests.yml/badge.svg)
```

## 📊 Cobertura de Tests

**Verificar cobertura localmente:**

```bash
pytest --cov=. --cov-report=html --cov-report=term-missing

# Ver reporte en navegador (abrir htmlcov/index.html)
```

**Objetivo:** >80% de cobertura en código de negocio (modelos, servicios)

- Las rutas (routes/) y templates NO necesitan 100% cobertura
- Los tests mismos NO se incluyen en la cobertura

**Archivos con baja cobertura actual:**

- `app.py` (0%) - No probado en tests integración
- `routes/` (13-52%) - Requiere tests de integración HTTP
- `manage.py` (0%) - Comandos CLI

## 📋 Configuración de Linting

### Black

- Formateador de código automático
- Línea máxima: 88 caracteres (configurable en `pyproject.toml`)
- Modifica archivos in-place

### Flake8

- Linter que detecta:
  - Errores de sintaxis
  - Imports no utilizados (F401)
  - Variables no utilizadas (F841)
  - Líneas demasiado largas (E501)
  - Espacios en blanco incorrectos (E302, E305)
  - Nombres ambiguos (E741)

**Excepciones configuradas:**

- `E203` - Espacio antes de `:` en slices
- `W503` - Line break before binary operator

### isort

- Ordena imports automáticamente
- Perfil: `black` (compatible con Black)
- Agrupa: `future`, `stdlib`, `third-party`, `first-party`, `local`

## 🔧 Configuración de Herramientas

**Archivos de configuración:**

- `.pre-commit-config.yaml` - Definición de hooks
- `pytest.ini` - Configuración de pytest
- `setup.cfg` - Configuración de cobertura y pytest
- `.github/workflows/tests.yml` - Workflow de GitHub Actions
- `pyproject.toml` - Configuración de Black (no creado, usa defaults)

## 📝 Workflow Recomendado

### Antes de Push

```bash
# 1. Ejecutar tests localmente
pytest

# 2. Ejecutar pre-commit
pre-commit run --all-files

# 3. Verificar cobertura
pytest --cov=. --cov-report=term-missing

# 4. Hacer cambios si es necesario
git add .
git commit -m "Mensaje descriptivo"

# 5. Push
git push origin feature/nombre-feature
```

### En Pull Request

1. GitHub Actions ejecuta automáticamente
2. Esperar a que los checks pasen ✅
3. Si falla, revisar logs en Actions tab
4. Hacer cambios localmente
5. Commit y push (Actions se ejecutan nuevamente)

### Después de Merge

- Main branch está protegido
- Solo se puede mergear si los tests pasan
- No se puede forzar push a main

## 🐛 Troubleshooting

**Los tests pasan localmente pero fallan en GitHub:**

- Diferencias de SO (Windows vs Linux)
- Diferencias de versión de Python
- Variables de entorno no configuradas

**Pre-commit deja archivo modificado:**

- Black y isort modifican archivos automáticamente
- Revisar cambios: `git diff`
- Hacer add nuevamente: `git add .`
- Intentar commit nuevamente

**Reporte de cobertura bajo:**

- Agregar tests a `tests/` directorio
- Usar fixtures de `conftest.py`
- Cubrir casos de error y excepciones

**Linting fallos que no entiendo:**

```bash
# Ver detalles específicos
flake8 archivo.py --show-source

# Ver todas las violations
flake8 . --statistics
```

## 📚 Referencias

- [pytest docs](https://docs.pytest.org/)
- [pre-commit docs](https://pre-commit.com/)
- [Black docs](https://black.readthedocs.io/)
- [flake8 docs](https://flake8.pycqa.org/)
- [isort docs](https://pycqa.github.io/isort/)
- [GitHub Actions docs](https://docs.github.com/en/actions)
