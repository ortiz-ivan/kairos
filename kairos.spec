# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file para Kairos

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Recolectar datos de paquetes que tienen archivos estáticos
datas = []
datas += collect_data_files('flask')
datas += collect_data_files('jinja2')

# Agregar directorios de la aplicación (solo los que existen)
datas.append(('templates', 'templates'))
datas.append(('migrations', 'migrations'))
datas.append(('.env.example', '.'))
datas.append(('requirements.txt', '.'))

# Archivos de configuración
datas.append(('config.py', '.'))
datas.append(('wsgi.py', '.'))

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'flask',
        'flask_sqlalchemy',
        'flask_migrate',
        'werkzeug',
        'werkzeug.security',
        'sqlalchemy',
        'sqlalchemy.orm',
        'jinja2',
        'markupsafe',
        'click',
        'itsdangerous',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Kairos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # False para GUI sin consola
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
