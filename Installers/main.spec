# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('../libs', 'libs'), ('../CopyFiles.xml', '.'), ('../iu/copyfiles_main_wdw.ui', 'iu'), ('../iu/copy.ico', 'iu'), ('../iu/process.ico', 'iu')
    ],
    hiddenimports=[
    'customtkinter','_cffi_backend','colorama','prettytable',
    'pycryptodome','pytz','tzlocal','CTkMessagebox', 'pyqt', 'numpy'
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
    name='CopyFiles-Python',
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
    icon=['../iu/copy.ico'],
    xml=['../CopyFiles.xml'],
    iu=['../iu/copyfiles_main_wdw.ui', '../iu/copy.ico', '../iu/process.ico'],
    onefile=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CopyFiles_python'
)
