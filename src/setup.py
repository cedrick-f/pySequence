#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys, os
from glob import glob
from cx_Freeze import setup, Executable

## Remove the build folder, a bit slower but ensures that build contains the latest
import shutil
shutil.rmtree("build", ignore_errors=True)

# Inculsion des fichiers de données
#################################################################################################
includefiles = [('Microsoft.VC90.CRT', "Microsoft.VC90.CRT"),
                     'gpl.txt']
includefiles.extend(glob(r"*.xlsx"))
includefiles.extend(glob(r"*.xls"))
includefiles.extend(glob(r"*.xlsm"))


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




#from distutils.core import setup
#import py2exe
#import os
#import matplotlib
##import babel
#
## Remove the build folder, a bit slower but ensures that build contains the latest
#import shutil
#shutil.rmtree("build", ignore_errors=True)
#shutil.rmtree("dist", ignore_errors=True)
#
#from glob import glob
#
## Inculsion des fichiers de données
##################################################################################################
## Fichiers MSVC
#data_files = [("Microsoft.VC90.CRT", glob(r'msvcr90.dll')), 
#              ("Microsoft.VC90.CRT", glob(r'Microsoft.VC90.CRT.manifest'))]
#
## Traductions
##data_files.extend([(os.path.join("locale", "en", "LC_MESSAGES"), glob(r'pysylic.mo'))])
#
## Fichiers Matplotlib
#data_files.extend(matplotlib.get_py2exe_datafiles())


#'Image', 'ImageFilter', '_umfpack', 'core.abs', 'core.max', 'core.min', 'core.round', 'email.Generator',
#'email.Iterators', 'email.Utils','lib.add_newdoc','nose', 'nose.plugins', 'nose.plugins.base',
#'nose.plugins.builtin', 'nose.plugins.errorclass', 'nose.tools', 'nose.util',
#excludes = []
##excludes = [ 'scipy.factorial',   'pkg_resources',
##'scikits.umfpack', 'sparsetools.bsr_matmat_pass2', 'sparsetools.bsr_matvec', 'sparsetools.bsr_matvecs',
##'sparsetools.bsr_sort_indices', 'sparsetools.bsr_transpose', 'sparsetools.coo_matvec', 'sparsetools.coo_tocsr',
##'sparsetools.coo_todense', 'sparsetools.csc_tocsr', 'sparsetools.csr_count_blocks', 'sparsetools.csr_matmat_pass1',
##'sparsetools.csr_tobsr', 'sparsetools.csr_tocsc', 'sparsetools.dia_matvec', 'sparsetools.get_csr_submatrix',
##'testing.Tester', 'numpy.absolute', 'numpy.arccos', 'numpy.arccosh', 'numpy.arcsin', 'numpy.arcsinh',
##'numpy.arctan', 'numpy.arctanh', 'numpy.bitwise_and', 'numpy.bitwise_or', 'numpy.bitwise_xor', 'numpy.bool_',
##'numpy.cast', 'numpy.ceil', 'numpy.complexfloating', 'numpy.conj', 'numpy.conjugate', 'numpy.core.add',
##'numpy.core.cdouble', 'numpy.core.complexfloating', 'numpy.core.conjugate', 'numpy.core.csingle',
##'numpy.core.double', 'numpy.core.float64', 'numpy.core.float_', 'numpy.core.inexact',
##'numpy.core.intc', 'numpy.core.isfinite', 'numpy.core.isnan', 'numpy.core.maximum', 'numpy.core.multiply',
##'numpy.core.number', 'numpy.core.single', 'numpy.core.sqrt', 'numpy.cosh', 'numpy.divide', 'numpy.double',
##'numpy.fabs', 'numpy.float64', 'numpy.float_', 'numpy.floor', 'numpy.floor_divide', 'numpy.fmod', 'numpy.greater',
##'numpy.hypot', 'numpy.inexact','numpy.int32', 'numpy.invert', 'numpy.isfinite', 'numpy.isinf', 'numpy.left_shift',
##'numpy.less', 'numpy.log', 'numpy.logical_and', 'numpy.logical_not', 'numpy.logical_or', 'numpy.logical_xor',
##'numpy.maximum', 'numpy.minimum', 'numpy.negative', 'numpy.not_equal', 'numpy.power', 'numpy.random.rand',
##'numpy.random.randn', 'numpy.remainder', 'numpy.right_shift', 'numpy.sign', 'numpy.single', 'numpy.sinh',
##'numpy.tan', 'numpy.tanh', 'numpy.true_divide', 'scipy.float64', 'scipy.special.gammaln']
#
#options = {    "py2exe" : { "compressed": 2,
#                           
#                            "optimize": 2,
#                            
#                            "bundle_files": 3,
#                            
#                            'packages' : ['pytz', 'win32api'],
#                            
#                            'excludes' : ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
#                                          'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
#                                          'Tkconstants', 'Tkinter', 'pydoc', 'doctest', 'test', 'sqlite3',
#                                          "PyQt4", "PyQt4.QtGui","PyQt4._qt",
#                                          "matplotlib.backends.backend_qt4agg", "matplotlib.backends.backend_qt4", "matplotlib.backends.backend_tkagg",
#                                          "matplotlib.numerix", #"matplotlib._cntr",
#                                          "numpy.core._dotblas",
##                                          "matplotlib._delaunay",
##                                          "scipy.sparse", 
#                                          ],
#                            'dll_excludes' : ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl85.dll',
#                                              'tk85.dll', "UxTheme.dll", "mswsock.dll", "POWRPROF.dll",
#                                              "QtCore4.dll", "QtGui4.dll" ],



#                            "dll_excludes":["wxMSW26uh_vc.dll","gdiplus.dll","libgdk-win32-2.0-0.dll","libgobject-2.0-0.dll","libgdk_pixbuf-2.0-0.dll",],
#                            "packages": ["matplotlib","pytz","matplotlib.numerix.random_array"],
                            
                            #"excludes" : ['scipy.interpolate' ],
                            #"includes": ['_scproxy'],
                            #"packages": [ 'scipy.factorial'],
#                                   }     }

#icon = "D:\\Developpement\\PySyLic\\PySyLiC 0.31\\Images\\icone.ico"
#setup(
#      #com_server=['myserver'],
#      options = options,
#      #zipfile = None,
##      console=["PySyLic.py"],
#      data_files = data_files,
#      windows =[{"script" :"pyLogyc.py",#console =[{"script" :"PySyLic.py",#
##                "icon_resources":[(1, icon)],
#                #"other_resources": [(24,1,manifest)]
#                }]
#    )


#
# Plein de "manifest" ...
#

#manifest = """
#<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
#<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
#manifestVersion="1.0">
#<assemblyIdentity
#    version="0.64.1.0"
#    processorArchitecture="x86"
#    name="Controls"
#    type="win32"
#/>
#<description>pySyLiC</description>
#<dependency>
#    <dependentAssembly>
#        <assemblyIdentity
#            type="win32"
#            name="Microsoft.Windows.Common-Controls"
#            version="6.0.0.0"
#            processorArchitecture="X86"
#            publicKeyToken="6595b64144ccf1df"
#            language="*"
#        />
#    </dependentAssembly>
#</dependency>
#</assembly>
#"""
#
#manifest = """
#<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
#<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
#manifestVersion="1.0">
#<assemblyIdentity
#    version="0.64.1.0"
#    processorArchitecture="x86"
#    name="Controls"
#    type="win32"
#/>
#<description>Your Application</description>
#<dependency>
#    <dependentAssembly>
#        <assemblyIdentity
#            type="win32"
#            name="Microsoft.Windows.Common-Controls"
#            version="6.0.0.0"
#            processorArchitecture="X86"
#            publicKeyToken="6595b64144ccf1df"
#            language="*"
#        />
#    </dependentAssembly>
#</dependency>
#</assembly>
#"""
#
#
#
#manifest = """
# <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
#    <assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
#     <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
#        <security>
#         <requestedPrivileges>
#            <requestedExecutionLevel level="asInvoker" uiAccess="false"></requestedExecutionLevel>
#         </requestedPrivileges>
#        </security>
#     </trustInfo>
#     <dependency>
#        <dependentAssembly>
#         <assemblyIdentity type="win32" name="Microsoft.VC90.DebugCRT" version="9.0.21022.8" processorArchitecture="x86" publicKeyToken="1fc8b3b9a1e18e3b"></assemblyIdentity>
#        </dependentAssembly>
#     </dependency>
#     <dependency>
#        <dependentAssembly>
#         <assemblyIdentity type="win32" name="Microsoft.VC80.CRT" version="8.0.50727.762" processorArchitecture="x86" publicKeyToken="1fc8b3b9a1e18e3b"></assemblyIdentity>
#        </dependentAssembly>
#     </dependency>
#    </assembly>
#
#"""
#
#
#manifest = """
#<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
#<!-- Copyright (c) Microsoft Corporation.  All rights reserved. -->
#<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
#    <noInheritable/>
#    <assemblyIdentity
#        type="win32"
#        name="Microsoft.VC90.CRT"
#        version="9.0.21022.8"
#        processorArchitecture="x86"
#        publicKeyToken="1fc8b3b9a1e18e3b"
#    />
#    <file name="msvcr90.dll" /> <file name="msvcp90.dll" /> <file name="msvcm90.dll" />
#</assembly>
#"""