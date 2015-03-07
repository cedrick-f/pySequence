#!/usr/bin/python
# -*- coding: utf-8 -*-

##################################################################################################
#
#    Script pour générer un pack avec executable :
#    c:\python27\python setup.py build
#
##################################################################################################

import sys, os
from glob import glob
from cx_Freeze import setup, Executable

reload(sys)
sys.setdefaultencoding('utf-8')
    
## Remove the build folder, a bit slower but ensures that build contains the latest
import shutil
shutil.rmtree("build", ignore_errors=True)

# Inculsion des fichiers de donn�es
#################################################################################################
includefiles = [('Microsoft.VC90.CRT', "Microsoft.VC90.CRT"),
                     'gpl.txt', 
                     'fichier_prj.ico', 'fichier_seq.ico',
                     'etablissements.xml',
                     ('../tables', "../tables"),
                     ('../BO', "../BO"),
                     ('../referentiels', "../referentiels")]
#includefiles.extend(glob(r"*.xlsx"))
#includefiles.extend(glob(r"*.xls"))
#includefiles.extend(glob(r"*.xlsm"))
for p in ['C:\\Python27\\Lib\site-packages\\html5lib',
            'C:\\Python27\\Lib\\site-packages\\xhtml2pdf',
            'C:\\Python27\\Lib\\site-packages\\PIL']:
    if not p in sys.path:
        sys.path.append(p)

#sys.path = ['', 'C:\\Python27\\Lib\\idlelib', 
#            'C:\\Python27\\lib\\site-packages\\setuptools-3.6-py2.7.egg', 
#            'C:\\Python27\\lib\\site-packages\\xmind-0.1a.0-py2.7.egg', 
#            'C:\\Python27\\lib\\site-packages\\distribute-0.7.3-py2.7.egg', 
#            'C:\\Python27\\lib\\site-packages\\six-1.8.0-py2.7.egg', 
#            'C:\\Python27\\lib\\site-packages\\python_dateutil-2.2-py2.7.egg', 
#            'C:\\Python27\\lib\\site-packages\\comtypes-1.1.1-py2.7.egg', 
#            'C:\\Python27\\lib\\site-packages\\xlutils-1.7.1-py2.7.egg', 
#            'C:\\Python27\\lib\\site-packages\\pillow-2.7.0-py2.7-win32.egg', 
#            'C:\\Python27\\lib\\site-packages\\html5lib-1.0b3-py2.7.egg', 
#            'C:\\Python27\\lib\\site-packages\\xhtml2pdf-0.0.6-py2.7.egg', 
#            'C:\\Python27\\python27.zip', 'C:\\Python27\\DLLs', 
#            'C:\\Python27\\lib', 
#            'C:\\Python27\\lib\\plat-win', 
#            'C:\\Python27\\lib\\lib-tk', 
#            'C:\\Python27', 
#            'C:\\Python27\\lib\\site-packages', 
#            'C:\\Python27\\lib\\site-packages\\win32', 
#            'C:\\Python27\\lib\\site-packages\\win32\\lib', 
#            'C:\\Python27\\lib\\site-packages\\Pythonwin', 
#            'C:\\Python27\\lib\\site-packages\\wx-3.0-msw',
#            'C:\\Python27\\Lib\site-packages\\html5lib',
#            'C:\\Python27\\Lib\\site-packages\\xhtml2pdf',
#            'C:\\Python27\\Lib\\site-packages\\Pillow-2.7.0-py2.7-win32\\PIL']



# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'build_exe': 'build/bin',
                     "packages": ["os", "xhtml2pdf","html5lib"], 
                     "includes": ["xhtml2pdf", "xhtml2pdf.pisa","html5lib", "xhtml2pdf.w3c"],
                     "optimize" : 0,
#                     "path" : ["../packages/html5lib"],#, "../packages/xhtml2pdf",  "../packages/xhtml2pdf/w3c"],
#                     "zip_includes": [("../packages/html5lib/", "html5lib"),
#                                      ("../packages/xhtml2pdf/w3c/css.py", "xhtml2pdf/w3c/css.py")],
                     "namespace_packages" : ["xhtml2pdf", "html5lib", "xhtml2pdf.w3c"],
                     "excludes": ["tkinter",
                                  '_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
                                  'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
                                  'Tkconstants', 'pydoc', 'doctest', 'test', 'sqlite3',
                                  "PyQt4", "PyQt4.QtGui","PyQt4._qt",
                                  "matplotlib",
                                  "numpy",
                                  ],
                     "include_files": includefiles,
                     'bin_excludes' : ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl85.dll',
                                              'tk85.dll', "UxTheme.dll", "mswsock.dll", "POWRPROF.dll",
                                              "QtCore4.dll", "QtGui4.dll" ]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
#if sys.platform == "win32":
#    base = "Win32GUI"


cible = Executable(
    script = "sequence.py",
    base = base,
    compress = True,
    icon = os.path.join("", 'logo.ico'),
    initScript = None,
    copyDependentFiles = True,
    appendScriptToExe = False,
    appendScriptToLibrary = False
    )


setup(  name = "pySequence",
        version = "6.0.0.6",
        author = "Cédrick FAURY & Jean-Claude FRICOU",
        description = u"pySéquence",
        options = {"build_exe": build_exe_options},
#        include-msvcr = True,
        executables = [cible])
