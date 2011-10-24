#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from distutils.core import setup
import py2exe
import os

#import babel

# Remove the build folder, a bit slower but ensures that build contains the latest
import shutil
shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)

from glob import glob

# Inculsion des fichiers de données
#################################################################################################
# Fichiers MSVC
data_files = [("Microsoft.VC90.CRT", glob(r'msvcr90.dll')), 
              ("Microsoft.VC90.CRT", glob(r'Microsoft.VC90.CRT.manifest')),
              "configuration.cfg"]


options = {    "py2exe" : { "compressed": True,
                           
                            "optimize": 2,
                            
                            "bundle_files": 3,
                            
                            'packages' : ['pytz', 'win32api'],
                            
                            'excludes' : ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
                                          'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
                                          'Tkconstants', 'Tkinter', 'pydoc', 'doctest', 'test', 'sqlite3',
                                          "PyQt4", "PyQt4.QtGui","PyQt4._qt",
                                          "matplotlib", "numpy",
                                          "scipy.sparse", "scipy.lib"],
                            
                            'dll_excludes' : ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl85.dll',
                                              'tk85.dll', "UxTheme.dll", "mswsock.dll", "POWRPROF.dll",
                                              "QtCore4.dll", "QtGui4.dll",
                                              ],

                            'includes' : ['cairo', 'wx.lib.wxcairo'],
                            'packages' : ['cairo', 'ctypes'],
                            
#                            'dll_includes' : ["libcairo-2.dll"],

#                            "dll_excludes":["wxMSW26uh_vc.dll","gdiplus.dll","libgdk-win32-2.0-0.dll","libgobject-2.0-0.dll","libgdk_pixbuf-2.0-0.dll",],
#                            "packages": ["matplotlib","pytz","matplotlib.numerix.random_array"],
                            
                            #"excludes" : ['scipy.interpolate' ],
                            #"includes": ['_scproxy'],
                            #"packages": [ 'scipy.factorial'],
                                   }     }

#icon = "D:\\Documents\\Developpement\\PySyLic\\PySyLiC 0.31\\Images\\icone.ico"
setup(
      #com_server=['myserver'],
      options = options,
#      zipfile = None,
#      console=["PySyLic.py"],
      data_files = data_files,
      windows=[{"script" :"Sequence.py",
#                "icon_resources":[(1, icon)],
                #"other_resources": [(24,1,manifest)]
                }]
    )


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
manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!-- Copyright (c) Microsoft Corporation.  All rights reserved. -->
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <noInheritable/>
    <assemblyIdentity
        type="win32"
        name="Microsoft.VC90.CRT"
        version="9.0.21022.8"
        processorArchitecture="x86"
        publicKeyToken="1fc8b3b9a1e18e3b"
    />
    <file name="msvcr90.dll" /> <file name="msvcp90.dll" /> <file name="msvcm90.dll" />
</assembly>
"""