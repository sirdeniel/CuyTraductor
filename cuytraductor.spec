# -*- mode: python ; coding: utf-8 -*-


block_cipher = None
added_files = [
    # ( 'src/README.txt', '.' ),
    # ( '/mygame/data', 'data' ),
    # ( '/mygame/sfx/*.mp3', 'sfx' )
    ('assets/*.glade', 'assets'),
    ('assets/*.png', 'assets'),
    ('assets/style.css', 'assets'),
    ('assets/*.gif', 'assets'),
    ('assets/*.ico', 'assets'),
    ('apimodel.json', '.'),
    ('docsettings.json', '.')
]

a = Analysis(['cuytraductor.py'],
             pathex=['D:/sirdeniel/coding/CuyTranslator'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='cuytraductor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='assets/logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='cuytraductor')
