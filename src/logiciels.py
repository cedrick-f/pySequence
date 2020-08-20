#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               Constantes                                ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2011-2013 Cédrick FAURY - Jean-Claude FRICOU
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
Module logiciels
*****************

Gestion des logiciels utilisables en séance ou projet.

"""

import images

# Pour enregistrer en xml
import xml.etree.ElementTree as ET

import util_path
import wx, os
from widgets import safeParse, scaleImage
# Logiciels de modélisation
# Caractère de préfixe :
#   . = bouton radio
#   x = case à cocher
#   _ = texte libre (avec case à cocher)
#   
# LOGICIELS = [(".Solidworks", [".Motion",
#                              ".Meca3D",
#                              "xFlowSim",
#                              "xSimulation",
#                              "_"],
#               ),
#              (".CATIA", []),
#              (".Inventor", []),
#              (".AutoCAD", []),
#              (".Top Solid", []),
#              (".Solidedge", []),
#              (".Pro Engineer", []),
#              (".FreeCAD", []),
#              (".Sketchup", []),
#              
#              (".MATLAB", ["xSimulink",
#                          "xStateflow",
#                          "xSimscape",
#                          "xSimElectronics",
#                          "xSimPowerSystems",
#                          "xSimMechanics",
#                          "_"]),
#              (".SciLAB", ["xXcos"]),
#              (".LabView", []),
#              ("_", [])
#              ]
# 
# IMG_LOGICIELS = {"Solidworks" : images.Logiciel_SW,
#                  "MATLAB" : images.Logiciel_MATLAB,
#                  "LabView" : images.Logiciel_LV,
#                  "CATIA" : images.Logiciel_CATIA,
#                  "AutoCAD" : images.Logiciel_Autocad,
#                  "Python" : images.Logiciel_Python,
#                  "Solidedge" : images.Logiciel_SEdge,
#                  "Inventor" : images.Logiciel_Inventor,
#                  "Top Solid" : images.Logiciel_Topsolid,
#                  "FreeCAD" : images.Logiciel_FreeCAD,
#                  "Sketchup" : images.Logiciel_Sketchup
#                  }



FICHIER_LOGICIELS = "logiciels.xml"

class Logiciel():
    def __init__(self):
        self.nom = ""
        self.description = ""
        self.type = 0
        self.image = None
        self.modules = []
    
    ######################################################################################  
    def setBranche(self, branche):
        """ Lecture d'une branche XML 
            contenant les caractéristiques d'un logiciels
        """

        self.nom  = branche.get("nom", "")

        self.type = int(branche.get("type", "0"))
                        
        self.description = branche.get("description", None)
        
        f = branche.get("image", None)
        if f is not None and hasattr(images, f):
            self.image = getattr(images, f)

        
        for m in branche:
            mo = Logiciel()
            mo.setBranche(m)
            self.modules.append(mo)
            
            
            
def charger_logiciels():
    fichier = open(os.path.join(util_path.APP_DATA_PATH_USER, FICHIER_LOGICIELS),'r', encoding='utf-8')
    parser = ET.XMLParser(encoding="utf-8")
    root = ET.parse(fichier, parser = parser).getroot()
    fichier.close()
    LOGICIELS = []
    for l in root:
        lo = Logiciel()
        lo.setBranche(l)
        LOGICIELS.append(lo)
    return LOGICIELS


def charger_images(logiciels):
    IMG_LOGICIELS = {}
    for l in logiciels:
        if l.image is not None:
            IMG_LOGICIELS[l.nom] = l.image
            
        for m in l.modules:
            if m.image is not None:
                IMG_LOGICIELS[m.nom] = m.image
    return IMG_LOGICIELS


if __name__ == "__main__":
    print(charger_logiciels())

