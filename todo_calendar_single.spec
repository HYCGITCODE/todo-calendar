# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Todo Calendar
Single-file executable with all dependencies
"""

import os
from PyInstaller.utils.hooks import collect_all, collect_data_files

# Collect all PyQt6 data and binaries
pyqt6_datas, pyqt6_binaries = collect_all('PyQt6')

block_cipher = None

# Define all data files to include
datas = [
    # Assets folder with styles
    ('assets', 'assets'),
    
    # QSS stylesheet files
    ('assets/styles/default.qss', 'assets/styles/default.qss'),
    
    # Database schema (not the actual db file with user data)
    ('src/database/', 'src/database'),
    
    # Include any other data files
    ('src/data/', 'src/data'),
]

# Add PyQt6 data files
datas += pyqt6_datas

# Define binaries to include
binaries = pyqt6_binaries

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        # PyQt6 modules
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.sip',
        
        # SQLAlchemy modules
        'sqlalchemy',
        'sqlalchemy.dialects',
        'sqlalchemy.dialects.sqlite',
        'sqlalchemy.dialects.sqlite.pysqlite',
        'sqlalchemy.pool',
        'sqlalchemy.event',
        
        # Date utilities
        'dateutil',
        'dateutil.parser',
        'dateutil.relativedelta',
        
        # Other common hidden imports
        'pkg_resources.py2_warn',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'matplotlib',
        'numpy',
        'pandas',
        'tkinter',
        'unittest',
    ],
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
    a.datas,
    [],
    name='Todo Calendar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
