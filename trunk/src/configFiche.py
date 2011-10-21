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

#
# Donn�es pour le tracé
#

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
tailleZOrganis = (0.72414-0.05, 0.95)

# Zone de déroulement de la séquence
posZDeroul = (0.06, 0.2)
tailleZDeroul = [None, None]

# Zone du tableau des Systèmes
posZSysteme = [None, 0.17]
tailleZSysteme = [None, None]
wColSysteme = 0.035

# Zone du tableau des démarches
posZDemarche = [None, 0.17]
tailleZDemarche = [0.08, None]
xDemarche = {"I" : None,
             "R" : None,
             "P" : None}

# Zone des intitulés des séances
posZIntSeances = [0.06, None]
tailleZIntSeances = [0.72414-0.06, None]
hIntSeance = 0.02

# Zone des séances
posZSeances = (0.07, 0.28)
tailleZSeances = [None, None]
wEff = {"C" : None,
             "G" : None,
             "D" : None,
             "E" : None,
             "P" : None,
             }
hHoraire = None
ecartY = None


