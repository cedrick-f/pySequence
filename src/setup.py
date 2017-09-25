#!/usr/bin/python
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
## et à la validation de Projets

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

u"""
Module Setup
************

Script pour générer un pack avec executable :
    c:\python27\python setup.py build
    
"""


import sys, os
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf8')
else:
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

from version import __version__, GetVersion_cxFreeze    
    
    
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
                     'etablissements.xml',
                     'JoursFeries.xml',
                     'splash.png',
                     ('../tables', "../tables"),
                     ('../BO', "../BO"),
                     ('../icones', "../icones"),
                     ('../referentiels', "../referentiels"),
#                     ('C:\\Python27\\lib\\site-packages\\enchant\\share\\enchant\\myspell', 'share/enchant/myspell'), 
#                     ('C:\\Python27\\lib\\site-packages\\enchant\\*.dll', ''),
#                     ('C:\\Python27\\lib\\site-packages\\enchant\\share\\enchant\\ispell', 'share/enchant/ispell'),
#                     ('C:\\Python27\\lib\\site-packages\\enchant\\lib\\enchant\\*.dll', 'lib/enchant'),
                     ]
if sys.platform == "win32":
    includefiles.extend([('C:\Users\Cedrick\Documents\Developp\Microsoft.VC90.CRT', "Microsoft.VC90.CRT"),])
    
includefiles.extend(enchant_files)

#includefiles.extend(glob(r"*.xlsx"))
#includefiles.extend(glob(r"*.xls"))
#includefiles.extend(glob(r"*.xlsm"))
for p in ['C:\\Python27\\Lib\site-packages\\html5lib',
            'C:\\Python27\\Lib\\site-packages\\xhtml2pdf',
            'C:\\Python27\\Lib\\site-packages\\PIL',
            "C:\\Python27\\Lib\\site-packages\\enchant"]:
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

# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'build_exe': 'build/bin',
                     "packages": ["os", "xhtml2pdf","html5lib", "enchant", "reportlab"], 
                     "includes": ["xhtml2pdf", "xhtml2pdf.pisa","html5lib", "xhtml2pdf.w3c", "encodings.ascii"],
                
                     "optimize" : 0,
#                      'compressed': True,
#                      'append_script_to_exe':False,
#                      'copy_dependent_files':True,
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
                     "bin_path_includes": binpathincludes,
                     'bin_excludes' : ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl85.dll',
                                              'tk85.dll', "UxTheme.dll", "mswsock.dll", "POWRPROF.dll",
                                              "QtCore4.dll", "QtGui4.dll" ]}


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


name = u"pySéquence"
version = GetVersion_cxFreeze()
author = u"Cédrick FAURY & Jean-Claude FRICOU"
author_email = "cedrick.faury@ac-clermont.fr"
description = u"pySéquence"
url = "https://github.com/cedrick-f/pySequence"
long_description = u"aide à la création de séquences pédagogiques et à la validation de projets"
license = "GPL"

if __name__ == '__main__':
    if sys.platform == "win32":
        from cx_Freeze import setup, Executable
        cible = Executable( script = "wx_pysequence.py",
                            targetName="Sequence.exe",
                            base = base,
                            compress = True,
                            icon = os.path.join("", 'logo.ico'),
                            initScript = None,
                            copyDependentFiles = True,
                            appendScriptToExe = False,
                            appendScriptToLibrary = False # disparu à partir de cx_freeze 5 !
                            )
    
    
        setup(  name = name,
                version = version,
                author = author,
                author_email = author_email,
                url = url,
                description = description,
                long_description = long_description,
                license = license,
                options = {"build_exe": build_exe_options,
                           "build": {'build_exe': 'build'},
                           "install" : {'install_exe': 'build'},
                           },
        #        include-msvcr = True,
                executables = [cible])
    
    else:
        from setuptools import setup, find_packages
        print "PACKAGES", find_packages()
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

