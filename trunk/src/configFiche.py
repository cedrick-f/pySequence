#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
configFiche.py
paramètres de configuration graphique de la fiche pédagogique de s�quence
*************
*   STIDD   *
*************
Copyright (C) 2011  
@author: Cedrick FAURY

"""

import ConfigParser


#
# Données pour le tracé
#
# Marges
margeX = 0.04
margeY = 0.05

# Ecarts
ecartX = 0.03
ecartY = 0.03

# Rectangle de l'intitulé
posIntitule = (0.72414-0.25, 0.05)
tailleIntitule = (0.2, 0.1)
IcoulIntitule = (0.2,0.8,0.2)
BcoulIntitule = (0.2,0.8,0.2)

# Objectifs
posCI = (0.05, 0.04)
tailleCI = (0.18, 0.12)
IcoulCI = (0.9,0.8,0.8)
BcoulCI = (0.3,0.2,0.25)

# Rectangle des objectifs
posObj = (0.262, 0.06)
tailleObj = (0.2, 0.08)
IcoulObj = (0.8,0.9,0.8)
BcoulObj = (0.25,0.3,0.2)

# Zone d'organisation de la séquence (grand cadre)
posZOrganis = (0.05, 0.19)
tailleZOrganis = (0.72414-0.1, 0.95)

# Zone de déroulement de la séquence
posZDeroul = (0.06, 0.2)
tailleZDeroul = [None, None]

# Zone du tableau des Systèmes
posZSysteme = [None, 0.17]
tailleZSysteme = [None, None]
wColSysteme = 0.035
xSystemes = {}

# Zone du tableau des démarches
posZDemarche = [None, 0.17]
tailleZDemarche = [0.08, None]
xDemarche = {"I" : None,
             "R" : None,
             "P" : None}

# Zone des intitulés des séances
posZIntSeances = [0.06, None]
tailleZIntSeances = [0.72414-0.12, None]
hIntSeance = 0.02

# Zone des séances
posZSeances = (0.08, 0.28)
tailleZSeances = [None, None]
wEff = {"C" : None,
             "G" : None,
             "D" : None,
             "E" : None,
             "P" : None,
             }
hHoraire = None
ecartSeanceY = None



def str2coord(str):
    l = str.split(',')
    return eval(l[0]), eval(l[1])

def coord2str(xy):
    return str(xy[0])+","+str(xy[1])

def str2coul(str):
    l = str.split(',')
    return eval(l[0]), eval(l[1]), eval(l[2]), eval(l[3])

def coul2str(rgba):
    if len(rgba) == 3:
        a = 1
    else:
        a = rgba[3]
    return str(rgba[0])+","+str(rgba[1])+","+str(rgba[2])+","+str(a)



def enregistrerConfigFiche(nomFichier):
    config = ConfigParser.ConfigParser()

    section = "Intitule de la sequence"
    config.add_section(section)
    config.set(section, "pos", coord2str(posIntitule))
    config.set(section, "dim", coord2str(tailleIntitule))
    config.set(section, "coulInt", coul2str(IcoulIntitule))
    config.set(section, "coulBord", coul2str(BcoulIntitule))
    
    section = "Centre d'interet"
    config.add_section(section)
    config.set(section, "pos", coord2str(posCI))
    config.set(section, "dim", coord2str(tailleCI))
    config.set(section, "coulInt", coul2str(IcoulCI))
    config.set(section, "coulBord", coul2str(BcoulCI))
    
    section = "Objectifs"
    config.add_section(section)
    config.set(section, "pos", coord2str(posObj))
    config.set(section, "dim", coord2str(tailleObj))
    config.set(section, "coulInt", coul2str(IcoulObj))
    config.set(section, "coulBord", coul2str(BcoulObj))

    section = "Zone d'organisation"
    config.add_section(section)
    config.set(section, "pos", coord2str(posZOrganis))
    config.set(section, "dim", coord2str(tailleZOrganis))

    section = "Zone de deroulement"
    config.add_section(section)
    config.set(section, "pos", coord2str(posZDeroul))

    section = "Tableau systemes"
    config.add_section(section)
    config.set(section, "posY", str(posZSysteme[1]))
    config.set(section, "col", str(wColSysteme))

    section = "Tableau demarche"
    config.add_section(section)
    config.set(section, "posY", str(posZDemarche[1]))
    config.set(section, "dimX", str(tailleZDemarche[0]))
    
    section = "Intitule des seances"
    config.add_section(section)
    config.set(section, "posX", str(posZIntSeances[0]))
    config.set(section, "dimX", str(tailleZIntSeances[0]))
    config.set(section, "haut", str(hIntSeance))

    section = "Seances"
    config.add_section(section)
    config.set(section, "pos", coord2str(posZSeances))
        
    config.write(open(nomFichier,'w'))
    
    
    
    
    
    
def ouvrirConfigFiche(nomFichier):
    print "ouvrirConfigFiche"
    global posIntitule, tailleIntitule, IcoulIntitule, BcoulIntitule, \
           posCI, tailleCI, IcoulCI, BcoulCI, \
           posObj, tailleObj, IcoulObj, BcoulObj, \
           posZOrganis, tailleZOrganis, \
           posZDeroul, wColSysteme, hIntSeance, posZSeances
           
           
    config = ConfigParser.ConfigParser()
    config.read(nomFichier)
    
    section = "Intitule de la sequence"
    posIntitule = str2coord(config.get(section,"pos"))
    tailleIntitule = str2coord(config.get(section,"dim"))
    IcoulIntitule = str2coul(config.get(section,"coulInt"))
    BcoulIntitule = str2coul(config.get(section,"coulBord"))
    
    section = "Centre d'interet"
    posCI = str2coord(config.get(section,"pos"))
    tailleCI = str2coord(config.get(section,"dim"))
    IcoulCI = str2coul(config.get(section,"coulInt"))
    BcoulCI = str2coul(config.get(section,"coulBord"))
    
    section = "Objectifs"
    posObj = str2coord(config.get(section,"pos"))
    tailleObj = str2coord(config.get(section,"dim"))
    IcoulObj = str2coul(config.get(section,"coulInt"))
    BcoulObj = str2coul(config.get(section,"coulBord"))

    section = "Zone d'organisation"
    posZOrganis = str2coord(config.get(section,"pos"))
    tailleZOrganis = str2coord(config.get(section,"dim"))
    
    section = "Zone de deroulement"
    posZDeroul = str2coord(config.get(section,"pos"))

    section = "Tableau systemes"
    posZSysteme[1] = config.getfloat(section,"posY")
    wColSysteme = config.getfloat(section,"col")

    section = "Tableau demarche"
    posZDemarche[1] = config.getfloat(section,"posY")
    tailleZDemarche[0] = config.getfloat(section,"dimX")
    
    section = "Intitule des seances"
    posZIntSeances[0] = config.getfloat(section,"posX")
    tailleZIntSeances[0] = config.getfloat(section,"dimX")
    hIntSeance = config.getfloat(section,"haut")
    
    section = "Seances"
    posZSeances = str2coord(config.get(section,"pos"))
    
    
    
    