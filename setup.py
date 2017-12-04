#!/usr/bin/python
# -*- coding: utf-8 -*-

##################################################################################################
#
#    Script pour générer un pack Linux (.deb) :
#    python setup.py --command-packages=stdeb.command bdist_deb
#
##################################################################################################

import sys, os
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf8')
else:
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

from glob import glob

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
                     'splash.png',
                     ('../tables', "../tables"),
                     ('../BO', "../BO"),
                     ('../referentiels', "../referentiels")]
    
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



# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'build_exe': 'build/bin',
                     "packages": ["os", "xhtml2pdf", "html5lib", "enchant", "reportlab", "wx.lib.pdfwin"], 
                     "includes": ["xhtml2pdf", "xhtml2pdf.pisa","html5lib", "xhtml2pdf.w3c", "encodings.ascii"],
                
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
                                  "matplotlib", "cffi",
                                  "numpy",
                                  ],
                     "include_files": includefiles,
                     "bin_path_includes": binpathincludes,
                     'bin_excludes' : ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl85.dll',
                                              'tk85.dll', "UxTheme.dll", "mswsock.dll", "POWRPROF.dll",
                                              "QtCore4.dll", "QtGui4.dll" ]}







name = u"pySequence"
version = GetVersion_cxFreeze()
author = u"Cédrick FAURY & Jean-Claude FRICOU"
author_email = "cedrick.faury@ac-clermont.fr"
description = u"pySéquence"
url = "https://github.com/cedrick-f/pySequence"
long_description = u"aide à la création de séquences pédagogiques et à la validation de projets"
license = "GPL"


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
        package_dir = {'':'src'},
        packages = find_packages('src'),
        install_requires=['python-wxgtk3.0',
                          'python-reportlab',
                          'pyenchant',
                          'xhtml2pdf',
                          'xlrd',
                          'xlwt',
                          'comtypes',
                          'pyperclip'],
        package_data = {'' : ['LICENSE.txt', 
                              'fichier_prj.ico', 
                              'fichier_seq.ico',
                              'etablissements.xml',
                              'splash.png',
                              'tables/*.*',
                              'BO/*.*',
                              'referentiels/*.*']
                              }
        )

