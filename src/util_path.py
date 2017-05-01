#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                  util_path                              ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2015 Cédrick FAURY - Jean-Claude FRICOU

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

Copyright (C) 2015
@author: Cedrick FAURY

"""

DEBUG = False


#import _winreg
import os, sys

if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf8')
else:
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('utf-8')

FILE_ENCODING = sys.getfilesystemencoding() 
SYSTEM_ENCODING = sys.getdefaultencoding()#sys.stdout.encoding#
# sys.getfilesystemencoding = lambda: 'UTF-8'
print "FILE_ENCODING", FILE_ENCODING
print "SYSTEM_ENCODING", SYSTEM_ENCODING


#
# Les deuxlignes suivantes permettent de lancer le script .py depuis n'importe
# quel répertoire  sans que l'utilisation de chemins
# relatifs ne soit perturbée
#
# PATH = os.path.dirname(os.path.abspath(sys.argv[0])).decode(FILE_ENCODING)
# #PATH = os.path.split(PATH)[0]
# os.chdir(PATH)
# sys.path.append(PATH)

# PATH = os.getcwd()
PATH = os.path.dirname(os.path.abspath(__file__))


if sys.platform == 'win32':
    #On récupèreﾠ le dossier "Application data" 
    #On lit la clef de registre indiquant le type d'installation
    import _winreg

    try:
        # Vérifie si pySequence est installé
        regkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\pySequence')
        (value, keytype) = _winreg.QueryValueEx(regkey, 'DataFolder')
        APP_DATA_PATH = value
        
        # pySequence installé : on récupère le dossier d'installation
        try:
            regkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\pySequence 1.0_is1')
            (value, keytype) = _winreg.QueryValueEx(regkey, 'Inno Setup: App Path')
            INSTALL_PATH = value
        except:
            try:
                regkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\pySequence')
                (value, keytype) = _winreg.QueryValueEx(regkey, 'UninstallPath')
                INSTALL_PATH = value
            except:
                print u"install_path non trouvé"
                
        INSTALL_PATH = os.path.join(os.path.split(INSTALL_PATH)[0], 'bin')
        print u"pySequence installé dans", INSTALL_PATH
        print u"pySequence démarré dans", PATH
        
        if INSTALL_PATH == PATH:
            # On est bien en train d'éxécuter la version "installée"
            if not os.path.exists(APP_DATA_PATH):
                os.makedirs(APP_DATA_PATH)
        else:
            INSTALL_PATH = None
            print u"Version PORTABLE", PATH
        
        
    except:
        INSTALL_PATH = None
        APP_DATA_PATH = PATH
        print u"Version PORTABLE : ", PATH
        
    sys.path.append(os.path.join(PATH, 'bin'))


else:
    INSTALL_PATH = None
    import subprocess
    #import standardpaths
    #import version
    
    #standardpaths.configure(application_name="pySequence", organization_name=version.__author__)
    #datalocation = standardpaths.Location.app_local_data.value
    
    #datalocation = standardpaths.get_writable_path('app_local_data')
    #datalocation = standardpaths.get_writable_path(standardpaths.Location.app_local_data)
    
    
    datalocation = os.getenv('APPDATA')
    if datalocation != None:
        datalocation = os.path.join(datalocation, "pySequence")
        if not os.path.exists(datalocation):
            subprocess.call("mkdir -p %s" %datalocation, shell=True)
        APP_DATA_PATH = datalocation
    else:
        APP_DATA_PATH = PATH
        


ERROR_FILE = os.path.join(APP_DATA_PATH, 'pySequence.exe' + '.log')
LOG_FILE = os.path.join(APP_DATA_PATH, 'log' + '.log')
    
if DEBUG:    
    sys.stdout = open(LOG_FILE, "w")



# execution du pySequence "installé"
if INSTALL_PATH is not None and INSTALL_PATH == PATH:
    APP_DATA_PATH_USER = os.path.join(os.getenv('APPDATA'), 'pySequence')
    if not os.path.isdir(APP_DATA_PATH_USER):
        os.mkdir(APP_DATA_PATH_USER)
# execution du pySequence "portable"
else:
    APP_DATA_PATH = PATH
    APP_DATA_PATH_USER = PATH


def samefile(path1, path2):
    return os.path.normcase(os.path.normpath(os.path.abspath(path1))) == \
           os.path.normcase(os.path.normpath(os.path.abspath(path2)))


######################################################################################  
def testRel(path, start):
    u""" Renvoie le chemin <path> relatif à <start> 
    """
    try:
        return os.path.relpath(path, start)
    except:
        return path
    
    
#######################################################################################  
#
#    Tout ce qui concerne l'encodage des caractères
#
#######################################################################################  
#print "defaultencoding", sys.getdefaultencoding()
#print "stdin, stdout", sys.stdin.encoding,sys.stdout.encoding

  
######################################################################################  
def toSystemEncoding(path): 
    
#        try:
#     path = path.decode(FILE_ENCODING)
    return path
    path = path.encode(SYSTEM_ENCODING)
    return path  
#        except:
#            return self.path    
    
######################################################################################  
def toFileEncoding(path):
    return path
#    try:
    path = path.decode(SYSTEM_ENCODING)
    return path.encode(FILE_ENCODING)
#    except:
#        return path
    
    
######################################################################################  
def nomCourt(nomFichier):
    u""" Renvoie le nom du fichier au format court (pour affichage = encodé en SystemEncoding)
        <nomFichier> encodé en FileEncoding
    """
    return toSystemEncoding(os.path.splitext(os.path.split(nomFichier)[1])[0])






print u"Dossier COMMUN pour les données :", APP_DATA_PATH
print u"Dossier USER pour les données :", APP_DATA_PATH_USER

TABLE_PATH = os.path.join(os.path.abspath(os.path.join(PATH, os.pardir)), r'tables')
#print u"Dossier des tableaux Excel :", TABLE_PATH

BO_PATH = os.path.join(os.path.abspath(os.path.join(PATH, os.pardir)), r'BO')
DOSSIER_ICONES = os.path.join(os.path.abspath(os.path.join(PATH, os.pardir)), r'icones')
#HTML_PATH = os.path.join(os.path.abspath(os.path.join(PATH, os.pardir)), r'html')


#print "programdata", os.environ['ALLUSERSPROFILE']