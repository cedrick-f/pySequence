#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               constantes                                ##
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


'''
Created on 26 oct. 2011

@author: Cedrick
'''


#
# Les deuxlignes suivantes permettent de lancer le script sequence.py depuis n'importe
# quel répertoire sans que l'utilisation de chemins
# relatifs ne soit perturbée
#
import sys, os
PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
#PATH = os.path.split(PATH)[0]
os.chdir(PATH)
sys.path.append(PATH)
print "Dossier de l'application :",PATH

####################################################################################
#
#   Définition des constantes
#
####################################################################################
import ConfigParser
CentresInterets = [u"Développement durable et compétitivité des produits",
                   u"Design, créativité et innovation",
                   u"Caractéristiques des matériaux et structures",
                   u"Solutions constructives des matériaux et des structures",
                   u"Dimensionnement des structures et choix des matériaux",
                   u"Efficacité énergétique liée au comportement des matériaux et des structures",
                   u"Formes et caractéristiques de l'énergie",
                   u"Organisation structurelle et solutions constructives des chaînes d'énergie",
                   u"Amélioration de l'efficacité énergétique dans les chaînes d'énergie",
                   u"Amélioration de la gestion de l'énergie",
                   u"Formes et caractéristiques de l'information",
                   u"Organisation structurelle et solutions constructives des chaînes d'information",
                   u"Commande temporelle des systèmes",
                   u"Informations liées au comportement des matériaux et des structures",
                   u"Optimisation des paramètres par simulation globale"
                   ]

Effectifs = {"C" : [u"Classe entière",      32],
             "G" : [u"Effectif réduit",     16],
             "D" : [u"Demi-groupe",         8],
             "E" : [u"Etude et Projet",     4],
             "P" : [u"Activité Pratique",   2],
             }


def ouvrirConfig():
    print "ouvrirConfig"
    global CentresInterets
    
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(PATH,'configuration.cfg'))
    
    section = "Centres d'interet"
    l = [""] * len(config.options(section))
    for o in config.options(section):
        l[eval(o)-1] = unicode(config.get(section,o), 'cp1252')
    CentresInterets = l
        
    section = "Effectifs classe"
    for k in Effectifs.keys():
        Effectifs[k][1] = config.getint(section,k)

ouvrirConfig()

    
Competences = {"CO1.1" : u"Justifier les choix des matériaux, des structures d'un système et les énergies mises en oeuvre dans une approche de développement durable",
               "CO1.2" : u"Justifier le choix d'une solution selon des contraintes d'ergonomie et d'effets sur la santé de l'homme et du vivant",
               "CO2.1" : u"Identifier les flux et la forme de l'énergie, caractériser ses transformations et/ou modulations et estimer l'efficacité énergétique globale d'un système",
               "CO2.2" : u"Justifier les solutions constructives d'un système au regard des impacts environnementaux et économiques engendrés tout au long de son cycle de vie",
               "CO3.1" : u"Décoder le cahier des charges fonctionnel d'un système",
               "CO3.2" : u"Evaluer la compétitivité d'un système d'un point de vue technique et économique",
               "CO4.1" : u"Identifier et caractériser les fonctions et les constituants d'un système ainsi que ses entrées/sorties",
               "CO4.2" : u"Identifier et caractériser l'agencement  matériel et/ou logiciel d'un système", 
               "CO4.3" : u"Identifier et caractériser le fonctionnement temporel d'un système",
               "CO4.4" : u"Identifier et caractériser des solutions techniques relatives aux matériaux, à la structure, à l'énergie et aux informations (acquisition, traitement, transmission) d'un système",
               "CO5.1" : u"Expliquer des éléments d'une modélisation proposée relative au comportement de tout ou partie d'un système",
               "CO5.2" : u"Identifier des variables internes et externes utiles à une modélisation, simuler et valider le comportement du modèle",
               "CO5.3" : u"Evaluer un écart entre le comportement du réel et le comportement du modèle en fonction des paramètres proposés",
               "CO6.1" : u"Décrire une idée, un principe, une solution, un projet en utilisant des outils de représentation adaptés",
               "CO6.2" : u"Décrire le fonctionnement et/ou l'exploitation d'un système en utilisant l'outil de description le plus pertinent",
               "CO6.3" : u"Présenter et argumenter des démarches, des résultats, y compris dans une langue étrangère",
               }


TypesActivite = {"ED" : u"Activité d'étude de dossier",
                 "AP" : u"Activité pratique",
                 "P" : u"Activité de projet",
                }

TypesSeance = {"C" : u"Cours",
               "SA" : u"Synthèse d'activité",
               "SS" : u"Synthèse de séquence",
               "E" : u"Evaluation",
               }
TypesSeance.update(TypesActivite)
TypesSeance.update({"R" : u"Rotation d'activités",
                    "S" : u"Activités en parallèle"})

TypesSeanceCourt = {"ED" : u"Etude de dossier",
                    "AP" : u"Activité pratique",
                    "P" : u"Projet",
                    "C" : u"Cours",
                    "SA" : u"Synt. d'activité",
                    "SS" : u"Synt. de séquence",
                    "E" : u"Evaluation",
                    "R" : u"Rotation",
                    "S" : u"Parallèle"}

listeTypeSeance = ["ED", "AP", "P", "C", "SA", "SS", "E", "R", "S"]
listeTypeActivite = ["ED", "AP", "P"]



Demarches = {"I" : u"Investigation",
             "R" : u"Résolution de problème",
             "P" : u"Projet"}
listeDemarches = ["I", "R", "P"]


