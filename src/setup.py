#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                  Setup                                  ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014 Cédrick FAURY - Jean-Claude FRICOU
##
## pySéquence : aide à la construction
## de Séquences et Progressions pédagogiques
# et à la validation de Projets

#    pySequence is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
    
#    pySequence is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pySequence; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
Module Setup
************

Script pour générer un pack avec executable :
    C:/Users/Cedrick/AppData/Local/Programs/Python/Python36-32/python setup.py build
"""
    
PATH_PYTHON36 = "C:/Users/Cedrick/AppData/Local/Programs/Python/Python36-32"

import sys, os
# if hasattr(sys, 'setdefaultencoding'):
#     sys.setdefaultencoding('utf8')
# else:
#     reload(sys)  # Reload does the trick!
#     sys.setdefaultencoding('utf-8')
print(sys.getdefaultencoding())


from version import __version__, GetVersion_cxFreeze, __mail__, __appname__

import cairocffi
# import cairocffi.ffi_build
    

## Remove the build folder, a bit slower but ensures that build contains the latest
import shutil
shutil.rmtree("build", ignore_errors=True)

import enchant.utils
le = []
if sys.platform == "win32":
    enchant_files = enchant.utils.win32_data_files() 
    for d, s in enchant_files:
        for f in s:
            if d =='':
                le.append((f, os.path.join(d, os.path.split(f)[1])))
            else:
                le.append((f, os.path.join('..',d, os.path.split(f)[1])))
enchant_files = le

#enchant_files = [([r.replace("\\", "/") for r in a], b.replace("\\", "/")) for b, a in enchant_files]
#print enchant_files

# Inculsion des fichiers de données
#################################################################################################

includefiles = ['LICENSE.txt', 
                     'fichier_prj.ico', 
                     'fichier_seq.ico',
                     'fichier_prg.ico', 
                     'etablissements.xml',
                     'JoursFeries.xml',
                     'd3.min.js',
#                      'fiche.html',
                     'splash.png',
                     ('../tables', "../tables"),
                     ('../templates', "../templates"),
#                      ('../BO', "../BO"),
                     ('../icones', "../icones"),
                     ('../referentiels', "../referentiels"),
#                     ('C:\\Python27\\lib\\site-packages\\enchant\\share\\enchant\\myspell', 'share/enchant/myspell'), 
#                     ('C:\\Python27\\lib\\site-packages\\enchant\\*.dll', ''),
#                     ('C:\\Python27\\lib\\site-packages\\enchant\\share\\enchant\\ispell', 'share/enchant/ispell'),
#                     ('C:\\Python27\\lib\\site-packages\\enchant\\lib\\enchant\\*.dll', 'lib/enchant'),
                     ]
if sys.platform == "win32":
    includefiles.extend(["../VCRUNTIME140.dll"])
    
# includefiles.extend(enchant_files)

#includefiles.extend(glob(r"*.xlsx"))
#includefiles.extend(glob(r"*.xls"))
#includefiles.extend(glob(r"*.xlsm"))
# for p in ['C:\\Python27\\Lib\site-packages\\html5lib',
#             'C:\\Python27\\Lib\\site-packages\\xhtml2pdf',
#             'C:\\Python27\\Lib\\site-packages\\PIL',
#             "C:\\Python27\\Lib\\site-packages\\enchant"]:
#     if not p in sys.path:
#         sys.path.append(p)



# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]

# _browserModule = win32com.client.gencache.EnsureModule(
#         "{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}", 0, 1, 1)

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'build_exe': 'build/bin',
                     'include_msvcr': True,
                     'add_to_path': True,
                     "packages": ["reportlab",'encodings', 'asyncio', '_cffi_backend'\
                                  ],#,'cairocffi._generated.ffi' \#"os", "xhtml2pdf","html5lib", "enchant", , "wx.lib.pdfwin", "PIL"], 
#                      "zip_includes": ["xhtml2pdf", "xhtml2pdf.pisa","html5lib", "xhtml2pdf.w3c", "encodings.ascii"],
                
                     "optimize" : 1,
#                      'compressed': True,
#                      'append_script_to_exe':False,
#                      'copy_dependent_files':True,
#                     "path" : ["../packages/html5lib"],#, "../packages/xhtml2pdf",  "../packages/xhtml2pdf/w3c"],
#                     "zip_includes": [("../packages/html5lib/", "html5lib"),
#                                      ("../packages/xhtml2pdf/w3c/css.py", "xhtml2pdf/w3c/css.py")],
                     "namespace_packages" : ["xhtml2pdf", "html5lib", "xhtml2pdf.w3c"],
                     "excludes": ["tkinter", "cffi",
                                  '_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
                                  'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
                                  'Tkconstants', 'pydoc', 'doctest', 'test', 'sqlite3',
                                  "PyQt4", "PyQt4.QtGui","PyQt4._qt",
                                  "matplotlib",
                                  "numpy",
                                  ],
                     "include_files": includefiles,
                     "bin_path_includes": binpathincludes,
                     'bin_excludes' : ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl85.dll',
                                              'tk85.dll', "UxTheme.dll", "mswsock.dll", "POWRPROF.dll",
                                              "QtCore4.dll", "QtGui4.dll" ],
                   
                     }


#bdist_rpm_options = {'bdist_rpm': 'build/bin',
#                     "packages": ["os", "xhtml2pdf","html5lib", "enchant", "reportlab"], 
#                     "includes": ["xhtml2pdf", "xhtml2pdf.pisa","html5lib", "xhtml2pdf.w3c", "encodings.ascii"],
#                     "optimize" : 0,
#                     "namespace_packages" : ["xhtml2pdf", "html5lib", "xhtml2pdf.w3c"],
#                     "include_files": includefiles,
#                     }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if not "beta" in __version__:
    if sys.platform == "win32":
        base = "Win32GUI"


name = __appname__
version = GetVersion_cxFreeze()
author = "Cédrick FAURY & Jean-Claude FRICOU"
author_email = __mail__.replace("#", '@')
description = "pySéquence"
url = "https://github.com/cedrick-f/pySequence"
long_description = "aide à la création de séquences pédagogiques et à la validation de projets"
lic = "GPL"

if __name__ == '__main__':
    if sys.platform == "win32":
        from cx_Freeze import setup, Executable
        cible = Executable( script = "wx_pysequence.py",
                            targetName="Sequence.exe",
                            base = base,
#                             compress = True,
                            icon = os.path.join("", 'logo.ico'),
                            initScript = None,
#                             copyDependentFiles = True,
#                             appendScriptToExe = False,
#                             appendScriptToLibrary = False # disparu à partir de cx_freeze 5 !
                            )
    
    
        setup(  name = name,
                version = version,
                author = author,
                author_email = author_email,
                url = url,
                description = description,
                long_description = long_description,
                license = lic,
                options = {"build_exe": build_exe_options,
                           "build": {'build_exe': 'build'},
                           "install" : {'install_exe': 'build'},
                           },
        #        include-msvcr = True,
                executables = [cible])
    
    else:
        from setuptools import setup, find_packages
        print("PACKAGES", find_packages())
        setup(  name = name,
                version = version,
                author = author,
                author_email = author_email,
                url = url,
                description = description,
                long_description = long_description,
                license = license,
                scripts=["wx_pysequence.py"],
                package_dir = {'':''},
                packages = find_packages(),
                install_requires=['python-wxgtk3.0',
                                  'python-reportlab',
                                  'pyenchant',
                                  'xhtml2pdf',
                                  'xlrd',
                                  'xlwt',
                                  'comtypes',
                                  'pyperclip']
                )



# Nettoyage (on enlève les python36.dll en trop
def supprimer(racine, nomFichier, parent = "", niveau = 0):
    # chemin absolu de la racine
    abspath = os.path.join(parent, racine)
    if os.path.isdir(abspath):
        for fd in os.listdir(abspath):
            supprimer(fd, nomFichier, abspath, niveau+1)
    elif os.path.split(abspath)[1] == nomFichier:
        os.remove(abspath)
        print(abspath)
supprimer('build/bin/lib', 'python36.dll')
supprimer('build/bin/lib', 'VCRUNTIME140.dll')
            
