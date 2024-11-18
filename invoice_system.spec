# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['invoice_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('invoice_system.db', '.'),
        ('assets/logo.ico', 'assets')  # Updated to use logo.ico
    ],
    hiddenimports=[
        'customtkinter.widgets',
        'customtkinter',
        'tkinter',
        'sqlite3',
        'reportlab',
        'reportlab.lib',
        'reportlab.pdfbase',
        'reportlab.platypus',
        'PIL'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Invoice System',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/logo.ico'  # Updated to use logo.ico
)
