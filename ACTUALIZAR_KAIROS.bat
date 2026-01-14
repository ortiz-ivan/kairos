@echo off
REM Script para actualizar Kairos preservando los datos existentes

echo.
echo ============================================================
echo           ACTUALIZAR KAIROS - Preservar Datos
echo ============================================================
echo.
echo Este script:
echo 1. Hace backup de tu base de datos actual
echo 2. Regenera el ejecutable con PyInstaller
echo 3. Restaura los datos (si existian)
echo.
echo IMPORTANTE:
echo - Tu base de datos esta en: %%APPDATA%%\Kairos\datos\kairos.db
echo - Los datos NO se perderan durante la actualizacion
echo.

pause

REM Crear directorio de backup si no existe
if not exist "backup" mkdir backup

REM Hacer backup de la BD actual (si existe)
echo Haciendo backup de datos existentes...
if exist "%APPDATA%\Kairos\datos\kairos.db" (
    echo Copiando base de datos...
    copy "%APPDATA%\Kairos\datos\kairos.db" "backup\kairos_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db" >nul
    echo ✅ Backup creado: backup\kairos_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db
) else (
    echo ℹ️  No hay base de datos existente para respaldar
)

echo.
echo Regenerando ejecutable...
python -m PyInstaller kairos.spec -y

echo.
echo ✅ Actualizacion completada!
echo.
echo Para usar la nueva version:
echo 1. Ve a la carpeta 'dist'
echo 2. Ejecuta 'INICIAR_KAIROS.bat'
echo.
echo Tus datos siguen seguros en: %%APPDATA%%\Kairos\datos\kairos.db
echo.

pause
