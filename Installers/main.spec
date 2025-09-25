# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=[('../libs', 'libs'), ('../../Images/smpp_sim_icon_red.ico', 'Images'), ('../../smpptransmitter/helloworldusim.ijc', 'ijc'), ('../../smpptransmitter/SMPP_Transmitter.xml', '.')],
    hiddenimports=[
    'customtkinter','_cffi_backend','colorama','prettytable',
    'pycryptodome','pytz','tzlocal','CTkMessagebox'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SMPP-Transmitter-Python',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['../../Images/smpp_sim_icon_red.ico'],
    ijc=['../../smpptransmitter/helloworldusim.ijc'],
    xml=['../../smpptransmitter/SMPP_Transmitter.xml'],
    onefile=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SMPP_Transmitter_python'
)
