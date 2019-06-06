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

"""
Module util_path
****************

Gestion des dossiers

"""

import os, sys
import imp



DEBUG = False


#import _winreg


if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf8')
else:
    imp.reload(sys)  # Reload does the trick!
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf-8')

FILE_ENCODING = sys.getfilesystemencoding() 
SYSTEM_ENCODING = sys.getdefaultencoding()#sys.stdout.encoding#
# sys.getfilesystemencoding = lambda: 'UTF-8'
print("FILE_ENCODING", FILE_ENCODING)
print("SYSTEM_ENCODING", SYSTEM_ENCODING)


#
# Les deuxlignes suivantes permettent de lancer le script .py depuis n'importe
# quel répertoire  sans que l'utilisation de chemins
# relatifs ne soit perturbée
#
# if getattr(sys, 'frozen', False):
#     # If the application is run as a bundle, the pyInstaller bootloader
#     # extends the sys module by a flag frozen=True and sets the app 
#     # path into variable _MEIPASS'.
#     PATH = sys._MEIPASS
# else:
PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
if PATH not in os.environ:
    os.environ["PATH"] += os.pathsep + PATH
# #PATH = os.path.split(PATH)[0]
# os.chdir(PATH)
sys.path.append(PATH)

# PATH = os.getcwd()

# A décommenter pour générer la doc Sphinx
# PATH = os.path.dirname(os.path.abspath(__file__))


if sys.platform == 'win32':
    #On récupèreﾠ le dossier "Application data" 
    #On lit la clef de registre indiquant le type d'installation
    import winreg

    try:
        # Vérifie si pySequence est installé
        regkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\pySequence')
        (value, keytype) = winreg.QueryValueEx(regkey, 'DataFolder')
        APP_DATA_PATH = value
        
        # pySequence installé : on récupère le dossier d'installation
        try:
            regkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\pySequence 1.0_is1')
            (value, keytype) = winreg.QueryValueEx(regkey, 'Inno Setup: App Path')
            INSTALL_PATH = value
        except:
            try:
                regkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\pySequence')
                (value, keytype) = winreg.QueryValueEx(regkey, 'UninstallPath')
                INSTALL_PATH = value
            except:
                print("install_path non trouvé")
                
        INSTALL_PATH = os.path.join(os.path.split(INSTALL_PATH)[0], 'bin')
        print("pySequence installé dans", INSTALL_PATH)
        print("pySequence démarré dans", PATH)
        
        if INSTALL_PATH == PATH:
            # On est bien en train d'éxécuter la version "installée"
            if not os.path.exists(APP_DATA_PATH):
                os.makedirs(APP_DATA_PATH)
        else:
            INSTALL_PATH = None
            print("Version PORTABLE", PATH)
        
        
    except:
        INSTALL_PATH = None
        APP_DATA_PATH = PATH
        print("Version PORTABLE : ", PATH)
        
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
    """ Renvoie le chemin <path> relatif à <start> 
    """
    try:
        return os.path.relpath(path, start)
    except:
#         print "echec relpath"
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
#     path = path.encode(SYSTEM_ENCODING)
#     return path  
#        except:
#            return self.path    
    
######################################################################################  
def toFileEncoding(path):
    return path
# #    try:
#     path = path.decode(SYSTEM_ENCODING)
#     return path.encode(FILE_ENCODING)
#    except:
#        return path


######################################################################################  
def verifierPath(path):
    pathv = ""
    if os.path.isfile(path):
        pathv = path
    else:
        arg2 = path#.decode('utf-8')
        if os.path.isfile(arg2):
            pathv = arg2
        else:
            arg2 = path.encode('utf-8')
            if os.path.isfile(arg2):
                pathv = arg2
                    
    return pathv


######################################################################################  
def nomCourt(nomFichier):
    """ Renvoie le nom du fichier au format court (pour affichage = encodé en SystemEncoding)
        <nomFichier> encodé en FileEncoding
    """
    return toSystemEncoding(os.path.splitext(os.path.split(nomFichier)[1])[0])






print("Dossier COMMUN pour les données :", APP_DATA_PATH)
print("Dossier USER pour les données :", APP_DATA_PATH_USER)

TABLE_PATH = os.path.join(os.path.abspath(os.path.join(PATH, os.pardir)), r'tables')
#print u"Dossier des tableaux Excel :", TABLE_PATH

BO_PATH = os.path.join(os.path.abspath(os.path.join(PATH, os.pardir)), r'BO')
if not os.path.exists(BO_PATH):
    BO_PATH = os.path.join(PATH, r'BO')

DOSSIER_ICONES = os.path.join(os.path.abspath(os.path.join(PATH, os.pardir)), r'icones')
if not os.path.exists(DOSSIER_ICONES):
    DOSSIER_ICONES = os.path.join(PATH, r'icones')
#HTML_PATH = os.path.join(os.path.abspath(os.path.join(PATH, os.pardir)), r'html')

TEMPLATE_PATH = os.path.join(os.path.abspath(os.path.join(PATH, os.pardir)), r'templates')
if not os.path.exists(TEMPLATE_PATH):
    TEMPLATE_PATH = os.path.join(PATH, r'templates')


#print "programdata", os.environ['ALLUSERSPROFILE']