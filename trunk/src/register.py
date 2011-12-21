#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
register.py
Aide à la réalisation de fiches pédagogiques de séquence
*************
*   STIDD   *
*************
Copyright (C) 2011  
@author: Cedrick FAURY

"""

import _winreg, os

EXT_FICHIER = ".seq"
TYPE_FICHIER = u"Séquence Pédagogique STI2D"
KEY_TYPE = "pySequence.sequence"
ICON = "logo.ico"


def Register(PATH):
    try:
        key_ext = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, EXT_FICHIER)
        _winreg.SetValueEx(key_ext, '', 0, _winreg.REG_SZ, KEY_TYPE)
        _winreg.CloseKey(key_ext)
        
        app = "\""+os.path.join(PATH, "Sequence.exe")+"\" \"%1\""
        key_typ = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE+"\\shell\\open\\command")#, 0, _winreg.KEY_NOTIFY)
        _winreg.SetValueEx(key_typ, '', 0, _winreg.REG_SZ, app)
        _winreg.CloseKey(key_typ)
        
        icone = os.path.join(PATH, ICON)
        key_ico = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE+"\\DefaultIcon")#, 0, _winreg.KEY_NOTIFY)
        _winreg.SetValueEx(key_ico, '', 0, _winreg.REG_SZ, icone)
        _winreg.CloseKey(key_ico)
        
        key_typ = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE)#, 0, _winreg.KEY_NOTIFY)
        _winreg.SetValueEx(key_typ, '', 0, _winreg.REG_SZ, TYPE_FICHIER)
        _winreg.CloseKey(key_typ)
        
        return True
    except:
        return False




def UnRegister():
    try:
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, EXT_FICHIER)
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE+"\\shell\\open\\command")
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE+"\\shell\\open")
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE+"\\shell")
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE+"\\DefaultIcon")
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE)
        return True
    except:
        return False
    
    
def IsRegistered():
    try:
        _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, EXT_FICHIER)
        _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE)
        return True
    except:
        return False
    
    
    
def getIcone(nomFichier):
    extension = os.path.splitext(nomFichier)[1]
    print extension
    key_ext = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, extension)
    (valeur,typevaleur) = _winreg.QueryValueEx(key_ext,'')
    print valeur
    _winreg.CloseKey(key_ext)
    key_ico = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, valeur+"\\DefaultIcon")
    (valeur,typevaleur) = _winreg.QueryValueEx(key_ico,'')
    _winreg.CloseKey(key_ico)
    fichier = valeur.split(',')[0]
    if os.path.splitext(fichier)[1] == '.ico':
        print fichier
    
    return
#Register(u"\"D:\\Developpement\\Sequence\\src\\dist\\Sequence.exe\" \"%1\"")
#UnRegister()


#getIcone(u'D:\\DropBox\\strategie_peda\\Formation_vague2\\Répartition pôle-référent-version4.pdf')




