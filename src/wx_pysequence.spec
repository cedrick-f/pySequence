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
                     
                     
datas += collect_data_files('wx.lib.wxcairo')                     
datas += collect_data_files('cairocffi')
datas += collect_data_files('reportlab')


#import wx_pysequence
#import pathlib
#pys_dir = pathlib.Path(wx_pysequence.__file__).parent
#pys_dll = [(str(dll), '.') for dll in pys_dir.glob('*.dll')]

binaries = [('C:/Users/Cedrick/AppData/Local/Programs/Python/Python36-32/python36.dll', '.'),
           ]
#binaries += pys_dll
                      
a = Analysis(['wx_pysequence.py'],
             pathex=['C:/Users/Cedrick/Documents/Developp/pysequence/src', 
                     #'C:/Users/Cedrick/Documents/Developp/pysequence/ressources/api-ms-win',
                     'C:/Windows/SysWOW64/downlevel',
                     #'C:/Users/Cedrick/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/wx',
                     #'C:/Users/Cedrick/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/enchant',
                     #'C:/Users/Cedrick/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/cairocffi'
                     ],
             binaries=binaries,
             datas=datas,
             hiddenimports=['wx', 'wx._xml', 'wx.lib.wxcairo', 
             				'_cffi_backend', 'cairocffi', 'enchant',
             				'cairosvg',
                            'reportlab.graphics.barcode.common', 'reportlab.graphics.barcode.code128',
                            'reportlab.graphics.barcode.code93', 'reportlab.graphics.barcode.usps',
                            'reportlab.graphics.barcode.code39','reportlab.graphics.barcode.usps4s',
                            'reportlab.graphics.barcode.ecc200datamatrix'
                            ],
             hookspath=['C:/Users/Cedrick/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/cairocffi',
             			'C:/Users/Cedrick/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/wx'],
             runtime_hooks=['hook-wxcairo.py'],
             excludes=['numpy', 'lib2to3'],
             win_no_prefer_redirects=True,
             win_private_assemblies=True,
             cipher=block_cipher,
             noarchive=False)
a.binaries -= TOC([
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
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='pySequence')
