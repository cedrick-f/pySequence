#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                  CompilImages                           ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2011 Cédrick FAURY

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# Programme de compilation des images .png en un unique fichier icones.py
#
# !!!  Effacer toutes les lignes de icones.py après la remarque :
#          " Supprimer tout ce qui suit avant compilation "
#


#from img2py import *
import wx.tools.img2py
import os
import glob

# Dossier contenant les images ##########################################################################################
dosImages = "Images"

# Fichier de sortie
fichIcone = "src/Images.py"

#Images
listFich = os.listdir(dosImages)
listFich = glob.glob(os.path.join(dosImages, "*.*"))
print listFich
# Fichiers Icone & Logo #############################################################################


FichiersImages = {}
for f in listFich:
    print os.path.splitext(f)[1]
    print os.path.basename(f)
    
    if os.path.isfile(f) and os.path.splitext(f)[1] in ['.jpg', '.png', '.ico']:
        nom = os.path.splitext(os.path.basename(f))[0]
        FichiersImages[nom] = f
        
print FichiersImages
#####################################################################################################
# Compilation de tout ca ..........

for idFichierImage in FichiersImages.keys():
    wx.tools.img2py.img2py(FichiersImages[idFichierImage], fichIcone,
           imgName = str(idFichierImage),
           append = True, icon = True,
           functionCompatible = True)

