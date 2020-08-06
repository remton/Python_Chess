# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['chess.py'],
             pathex=['C:\\Users\\remto\\PycharmProjects\\Chess'],
             binaries=[],
             datas=[('Images/*.png', 'Images')],
             hiddenimports=['numpy', 'tkinter', 'copy', 'math'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='chess',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='chess')
