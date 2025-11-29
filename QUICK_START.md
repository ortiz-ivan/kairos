# ⚡ Quick Start para Desarrollo

## 🎯 Antes de Empezar (Solo Primera Vez)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar pre-commit
pre-commit install

# 3. Listo! ✨
```

## 📝 Flujo de Desarrollo

### 1️⃣ Hacer Cambios

```bash
# Editar archivos con tu IDE favorito
code models/producto.py
```

### 2️⃣ Verificar Localmente

```bash
# Opción A: Usando pytest directamente
pytest

# Opción B: Usando script de desarrollo
python dev.py test

# Opción C: Con cobertura
pytest --cov=. --cov-report=html
```

### 3️⃣ Preparar Commit

```bash
# Agregar cambios
git add .

# Pre-commit se ejecuta automáticamente
# Si falla, verás errores - algunos se arreglan automáticamente
# Si hay cambios auto-arreglados, debes hacer add nuevamente

git add .
git commit -m "Mensaje descriptivo"
```

### 4️⃣ Push

```bash
git push origin nombre-rama
```

### 5️⃣ Pull Request

- GitHub Actions ejecuta automáticamente todos los tests
- Si pasa (✅), el PR está listo para review
- Si falla (❌), revisa los logs y haz cambios

## 🛠️ Comandos Más Usados

```bash
# Testing
pytest                          # Tests rápidos
pytest -v                       # Con detalle
pytest -k "producto"           # Solo tests que coincidan
pytest --lf                    # Último test que falló
pytest tests/test_products_crud.py::test_products_crud  # Test específico

# Code Quality (Pre-commit)
pre-commit run --all-files     # Ejecutar todos los hooks
python dev.py lint            # Mismo pero más simple
python dev.py format          # Formatear con Black

# Debugging
pytest --pdb                  # Abre debugger en falla
pytest -s                     # Muestra prints
pytest -x                     # Para en el primer fallo
```

## ❌ Algo Falló?

### Tests Fallan

```bash
# Ver error detallado
pytest tests/test_archivo.py -v --tb=short

# Ver todos los prints
pytest -s

# Abrir debugger en la línea del error
pytest --pdb
```

### Pre-commit Falla

```bash
# Ver qué hooks fallaron
pre-commit run --all-files

# Usualmente se auto-arregla:
# 1. Pre-commit modifica archivos
# 2. Revisar cambios: git diff
# 3. Hacer add nuevamente: git add .
# 4. Intentar commit nuevamente
```

### GitHub Actions Falla

1. Ir a: https://github.com/ortiz-ivan/kairos/actions
2. Seleccionar el PR que falló
3. Ver logs de la falla
4. Hacer cambios localmente
5. Push nuevamente (Actions se ejecuta automáticamente)

## 📚 Documentación Completa

- **`README.md`** - Setup, estructura, features
- **`TESTING_GUIDE.md`** - Testing detallado y troubleshooting
- **`CI_CD_SETUP_SUMMARY.md`** - Resumen de configuración CI/CD

## 💡 Pro Tips

✅ **Hacer pre-commit antes de cada commit:**

```bash
pre-commit run --all-files
```

✅ **Verificar cobertura de tests:**

```bash
pytest --cov=. --cov-report=html
# Abre htmlcov/index.html en navegador
```

✅ **Ejecutar solo los tests que cambiaste:**

```bash
pytest tests/test_products_crud.py -v
```

✅ **Ver qué cambios hizo Black:**

```bash
python dev.py format --check
```

❌ **NO** hacer force push a main:

```bash
# ❌ NUNCA
git push -f origin main

# ✅ SIEMPRE
git push origin feature-branch
# y luego abrir PR
```

---

**¿Preguntas?** Ver `TESTING_GUIDE.md` o `README.md`

**Happy coding! 🚀**
