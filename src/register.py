#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                  register                               ##
##                     enregistrement de pySequence                        ##
##                     dans la base de registre de Windows                 ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2012 Cédrick FAURY - Jean-Claude FRICOU

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
register.py
Aide à la réalisation de fiches pédagogiques de séquence
*************
*   STIDD   *
*************
Copyright (C) 2011  
@author: Cedrick FAURY

"""

import _winreg, os

EXT_FICHIER_SEQ = ".seq"
TYPE_FICHIER_SEQ = u"Fiche de Séquence Pédagogique"
KEY_TYPE_SEQ = "pySequence.sequence"
ICON_SEQ = "fichier_seq.ico"

EXT_FICHIER_PRJ = ".prj"
TYPE_FICHIER_PRJ = u"Fiche de validation de Projet"
KEY_TYPE_PRJ = "pySequence.projet"
ICON_PRJ = "fichier_prj.ico"


def Register(PATH):
    try:
        app = "\""+os.path.join(PATH, "Sequence.exe")+"\" \"%1\""
        # Clefs relatives aux "séquences"
        key_ext = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_SEQ)
        _winreg.SetValueEx(key_ext, '', 0, _winreg.REG_SZ, KEY_TYPE_SEQ)
        _winreg.CloseKey(key_ext)
        
        
        key_typ = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell\\open\\command")#, 0, _winreg.KEY_NOTIFY)
        _winreg.SetValueEx(key_typ, '', 0, _winreg.REG_SZ, app)
        _winreg.CloseKey(key_typ)
        
        icone = os.path.join(PATH, ICON_SEQ)
        key_ico = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\DefaultIcon")#, 0, _winreg.KEY_NOTIFY)
        _winreg.SetValueEx(key_ico, '', 0, _winreg.REG_SZ, icone)
        _winreg.CloseKey(key_ico)
        
        key_typ = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ)#, 0, _winreg.KEY_NOTIFY)
        _winreg.SetValueEx(key_typ, '', 0, _winreg.REG_SZ, TYPE_FICHIER_SEQ)
        _winreg.CloseKey(key_typ)
        
        
        # Clefs relatives aux "projets"
        key_ext = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_PRJ)
        _winreg.SetValueEx(key_ext, '', 0, _winreg.REG_SZ, KEY_TYPE_PRJ)
        _winreg.CloseKey(key_ext)
        
        key_typ = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell\\open\\command")#, 0, _winreg.KEY_NOTIFY)
        _winreg.SetValueEx(key_typ, '', 0, _winreg.REG_SZ, app)
        _winreg.CloseKey(key_typ)
        
        icone = os.path.join(PATH, ICON_PRJ)
        key_ico = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\DefaultIcon")#, 0, _winreg.KEY_NOTIFY)
        _winreg.SetValueEx(key_ico, '', 0, _winreg.REG_SZ, icone)
        _winreg.CloseKey(key_ico)
        
        key_typ = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ)#, 0, _winreg.KEY_NOTIFY)
        _winreg.SetValueEx(key_typ, '', 0, _winreg.REG_SZ, TYPE_FICHIER_PRJ)
        _winreg.CloseKey(key_typ)
        
        return True
    except:
        return False




def UnRegister():
    try:
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_SEQ)
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell\\open\\command")
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell\\open")
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell")
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\DefaultIcon")
        _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ)
        try:
            _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_PRJ)
            _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell\\open\\command")
            _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell\\open")
            _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell")
            _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\DefaultIcon")
            _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ)
        except:
            pass
        return True
    except:
        return False

def UnRegister2():

    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_SEQ)
    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell\\open\\command")
    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell\\open")
    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\shell")
    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ+"\\DefaultIcon")
    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ)

    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_PRJ)
    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell\\open\\command")
    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell\\open")
    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\shell")
    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ+"\\DefaultIcon")
    _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_PRJ)

    
def IsRegistered():
    try:
        _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, EXT_FICHIER_SEQ)
        _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, KEY_TYPE_SEQ)
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

#UnRegister2()
#print IsRegistered()



