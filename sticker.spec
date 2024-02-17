# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['sticker_gui.py'],
    pathex=['/Users/spark/Documents/Office/NiziPowerSaleSticker/venv/lib/python3.11/site-packages'],
    binaries=[],
    datas=[('assets/Roboto-Regular.ttf', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='sticker',
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
    icon=['logo.ico'],
)
app = BUNDLE(
    exe,
    name='sticker.app',
    icon='logo.ico',
    bundle_identifier=None,
)
