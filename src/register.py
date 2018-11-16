#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                  register                               ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2012 Cédrick FAURY - Jean-Claude FRICOU
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
Module register
***************

Enregistrement de pySéquence dans la base de registre (Windows)

(Des)Activation du mode protégé d'Adobe Reader

"""

import winreg, os

EXT_FICHIER_SEQ = ".seq"
TYPE_FICHIER_SEQ = "Fiche de Séquence Pédagogique"
KEY_TYPE_SEQ = "pySequence.sequence"
ICON_SEQ = "fichier_seq.ico"

EXT_FICHIER_PRJ = ".prj"
TYPE_FICHIER_PRJ = "Fiche de validation de Projet"
KEY_TYPE_PRJ = "pySequence.projet"
ICON_PRJ = "fichier_prj.ico"


def Register(PATH):
    try:
        app = "\""+os.path.join(PATH, "Sequence.exe")+"\" \"%1\""
        # Clefs relatives aux "séquences"
        key_ext = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_SEQ)
        winreg.SetValueEx(key_ext, '', 0, winreg.REG_SZ, KEY_TYPE_SEQ)
        winreg.CloseKey(key_ext)
        
        
        key_typ = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell\\open\\command")#, 0, _winreg.KEY_NOTIFY)
        winreg.SetValueEx(key_typ, '', 0, winreg.REG_SZ, app)
        winreg.CloseKey(key_typ)
        
        icone = os.path.join(PATH, ICON_SEQ)
        key_ico = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\DefaultIcon")#, 0, _winreg.KEY_NOTIFY)
        winreg.SetValueEx(key_ico, '', 0, winreg.REG_SZ, icone)
        winreg.CloseKey(key_ico)
        
        key_typ = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ)#, 0, _winreg.KEY_NOTIFY)
        winreg.SetValueEx(key_typ, '', 0, winreg.REG_SZ, TYPE_FICHIER_SEQ)
        winreg.CloseKey(key_typ)
        
        
        # Clefs relatives aux "projets"
        key_ext = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_PRJ)
        winreg.SetValueEx(key_ext, '', 0, winreg.REG_SZ, KEY_TYPE_PRJ)
        winreg.CloseKey(key_ext)
        
        key_typ = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell\\open\\command")#, 0, _winreg.KEY_NOTIFY)
        winreg.SetValueEx(key_typ, '', 0, winreg.REG_SZ, app)
        winreg.CloseKey(key_typ)
        
        icone = os.path.join(PATH, ICON_PRJ)
        key_ico = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\DefaultIcon")#, 0, _winreg.KEY_NOTIFY)
        winreg.SetValueEx(key_ico, '', 0, winreg.REG_SZ, icone)
        winreg.CloseKey(key_ico)
        
        key_typ = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ)#, 0, _winreg.KEY_NOTIFY)
        winreg.SetValueEx(key_typ, '', 0, winreg.REG_SZ, TYPE_FICHIER_PRJ)
        winreg.CloseKey(key_typ)
        
        return True
    except:
        return False




def UnRegister():
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_SEQ)
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell\\open\\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell\\open")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\DefaultIcon")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ)
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_PRJ)
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell\\open\\command")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell\\open")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\DefaultIcon")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ)
        except:
            pass
        return True
    except:
        return False

def UnRegister2():

    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_SEQ)
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell\\open\\command")
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell\\open")
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell")
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\DefaultIcon")
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ)

    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_PRJ)
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell\\open\\command")
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell\\open")
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell")
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\DefaultIcon")
    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ)

    
def IsRegistered():
    try:
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_SEQ)
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ)
        return True
    except:
        return False
    
    
    
def getIcone(nomFichier):
    extension = os.path.splitext(nomFichier)[1]
    print(extension)
    key_ext = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, extension)
    (valeur,typevaleur) = winreg.QueryValueEx(key_ext,'')
    print(valeur)
    winreg.CloseKey(key_ext)
    key_ico = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, valeur+"\\DefaultIcon")
    (valeur,typevaleur) = winreg.QueryValueEx(key_ico,'')
    winreg.CloseKey(key_ico)
    fichier = valeur.split(',')[0]
    if os.path.splitext(fichier)[1] == '.ico':
        print(fichier)
    
    return


########################################################################################
# [HKEY_CURRENT_USER\Software\Adobe\Acrobat Reader\10.0\Privileged]
# "bProtectedMode"=(0 = off; 1 = on)
########################################################################################
def EnableProtectedModeReader(val = 1):
#     REG_PATH = r"Software\Adobe\Acrobat Reader\10.0\Privileged"
    try:
        REG_PATH = r"Software\Adobe\Acrobat Reader\DC\Privileged"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                           winreg.KEY_WRITE)
        winreg.SetValueEx(key, "bProtectedMode", 0, winreg.REG_DWORD, val)
        winreg.CloseKey(key)
    except WindowsError:
        return
    
def GetProtectedModeReader():
#     REG_PATH = r"Software\Adobe\Acrobat Reader\10.0\Privileged"
    try:
        REG_PATH = r"Software\Adobe\Acrobat Reader\DC\Privileged"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                           winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(key, "bProtectedMode")
        winreg.CloseKey(key)
        return value
    except WindowsError:
        return None

#Register(u"\"D:\\Developpement\\Sequence\\src\\dist\\Sequence.exe\" \"%1\"")
#UnRegister()


#getIcone(u'D:\\DropBox\\strategie_peda\\Formation_vague2\\Répartition pôle-référent-version4.pdf')

#UnRegister2()
#print IsRegistered()



