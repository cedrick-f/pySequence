#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Script pour générer un pack avec executable :
# c:\python26\python setup.py build

import sys, os
from glob import glob
from cx_Freeze import setup, Executable

## Remove the build folder, a bit slower but ensures that build contains the latest
import shutil
shutil.rmtree("build", ignore_errors=True)

# Inculsion des fichiers de données
#################################################################################################
includefiles = [('Microsoft.VC90.CRT', "Microsoft.VC90.CRT"),
                     'gpl.txt', 
                     'etablissements.txt',
                     ('../tables', "../tables")]
#includefiles.extend(glob(r"*.xlsx"))
#includefiles.extend(glob(r"*.xls"))
#includefiles.extend(glob(r"*.xlsm"))


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], 
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
if sys.platform == "win32":
    base = "Win32GUI"

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
        version = "3.17",
        author = "Cedrick FAURY & Jean-Claude FRICOU",
        description = u"Aide à la réalisation de fiches  de séquence pédagogiques et à la validation de projets",
        options = {"build_exe": build_exe_options},
#        include-msvcr = True,
        executables = [cible])
