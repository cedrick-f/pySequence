# -*- mode: python -*-
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None
#('C:/Users/Cedrick/Documents/Developp/pysequence/ressources/api-ms-win/*.*', '.'),

datas = [('LICENSE.txt', '.'), 
                     ('fichier_*.ico', '.'), 
                     ('etablissements.xml', '.'),
                     ('JoursFeries.xml', '.'),
                     ('d3.min.js', '.'),
                     ('splash.png', '.'),
                     ('../tables/*.*', "./tables"),
                     ('../templates/*.*', "./templates"),
                     ('../icones/*.*', "./icones/"),
                     ('../referentiels/*.*', "./referentiels")
                     ]
                     
datas += collect_data_files('cairocffi')
datas += collect_data_files('reportlab')

a = Analysis(['wx_pysequence.py'],
             pathex=['C:/Users/Cedrick/Documents/Developp/pysequence/src', 
                     'C:/Users/Cedrick/Documents/Developp/pysequence/ressources/api-ms-win',
                     #'C:/Users/Cedrick/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/enchant',
                     #'C:/Users/Cedrick/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/cairocffi'
                     ],
             binaries=[('C:/Users/Cedrick/AppData/Local/Programs/Python/Python36-32/python36.dll', '.')
                       ],
             datas=datas,
             hiddenimports=['_cffi_backend', 'cairocffi', 'wx', 'wx._xml', 'enchant', 
                            'reportlab.graphics.barcode.common', 'reportlab.graphics.barcode.code128',
                            'reportlab.graphics.barcode.code93', 'reportlab.graphics.barcode.usps',
                            'reportlab.graphics.barcode.code39','reportlab.graphics.barcode.usps4s',
                            'reportlab.graphics.barcode.ecc200datamatrix'
                            ],
             hookspath=[],
             runtime_hooks=[],
             excludes=['numpy'],
             win_no_prefer_redirects=True,
             win_private_assemblies=True,
             cipher=block_cipher,
             noarchive=False)
a.binaries -= TOC([('sqlite3.dll', None, None),
  ('libopenblas.JKAMQ5EVHIVCPXP2XZJB2RQPIN47S32M.gfortran-win32.dll', None, None),
])


#a.datas += [('logo.png','C:\\Users\\vijay\\System\\icon\\logo.png','DATA')]
pyz = PYZ(a.pure, 
		  a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='pySequence',
          icon='logo.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='pySequence')
