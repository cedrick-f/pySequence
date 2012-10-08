#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               constantes SSI                            ##
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


####################################################################################
#
#   Définition des constantes pour la spécialité SIN
#
####################################################################################
PointsDeVue_SSI =  [u"Système souhaité",
                   u"Système réel",
                   u"Système réel",
                   u"Système simulé",
                   u"Système simulé"
                   ]


CentresInterets_SSI = [u"Analyser un système fonctionnellement et structurellement",
                       u"Expérimenter et mesurer sur un système réel pour évaluer ses performances",
                       u"Analyser des constituants d’un système réel d’un point de vue structurel et comportemental",
                       u"Concevoir et utiliser un modèle relatif à un système en vue d’évaluer les performances de la chaîne d’information",
                       u"Concevoir et utiliser un modèle relatif à un système en vue d’évaluer les performances de la chaîne d’énergie"
                       ]







dicSavoirs_SSI = {"A1" : [u"Analyser le besoin",
                         {"A1.1" : [u"Besoin, finalités, contraintes, cahier des charges",
                                   [u"Décrire le besoin",
                                    u"Présenter la fonction globale",
                                    u"Identifier les contraintes (fonctionnelles, sociétales, environnementales, etc.)",
                                    u"Ordonner les contraintes (critère, niveau, flexibilité)"]],
                                    
                          "A1.2" : [u"Analyse fonctionnelle externe - Expression fonctionnelle du besoin",
                                   [u"Présenter à l’aide d’un diagramme des interacteurs une réponse technique à un besoin"]
                                   ],
                          
                          "A1.3" : [u"Fonctions d’usage, de service, d’estime",
                                   [u"Identifier et caractériser les fonctions de service"]
                                   ],
                         }],
                 
                  "A2" : [u"Analyser le système",
                         {"A2.1" : [u"Système - Frontière d’étude - Environnement",
                                   [u"Définir le système et sa frontière d’étude",
                                    u"Analyser l’environnement d’un système, ses contraintes",
                                    u"Décrire le fonctionnement d’un système",
                                    u"Identifier des évolutions possibles d’un système"]],
                                    
                          "A2.2" : [u"Architectures fonctionnelle et organique d’un système",
                                   [u"Identifier les fonctions techniques",
                                    u"Déterminer les constituants dédiés aux fonctions d’un système et en justifier le choix",
                                    u"Identifier les niveaux fonctionnels et organiques d’un système",
                                    u"Présenter les architectures fonctionnelle et organique d’un système à l’aide d’un diagramme FAST",
                                    u"Proposer des évolutions sous forme fonctionnelle",
                                    u"Relier le coût d’une solution technique au besoin exprimé"]],
                          
                          "A2.3" : [u"Impact environnemental",
                                    [u"Évaluer l’impact environnemental (matériaux, énergie, nuisances)"]],
                          
                          "A2.4" : [u"Matière d’oeuvre, valeur ajoutée, flux",
                                    [u"Identifier la matière d’oeuvre et la valeur ajoutée",
                                     u"Représenter les flux (matière, énergie, information) à l’aide d’un actigramme A-0 de la méthode SADT"]],
                          
                          "A2.5" : [u"Chaîne d’information",
                                    [u"Identifier et décrire la chaîne d’information du système"]],
                          
                          "A2.6" : [u"Chaîne d’énergie",
                                    [u"Identifier et décrire la chaîne d’énergie du système",
                                     u"Analyser les apports d’énergie, les transferts, le stockage, les pertes énergétiques",
                                     u"Réaliser le bilan énergétique d’un système"]],
                          
                          "A2.7" : [u"Systèmes logiques évènementiels - Langage de description : graphe d’états, logigramme, GRAFCET, algorigramme",
                                    [u"Décrire et analyser le comportement d’un système"]],
                          
                          "A2.8" : [u"Systèmes asservis",
                                    [u"Différencier un système asservi d’un système non asservi"]],
                          
                          "A2.9" : [u"Composants réalisant les fonctions de la chaîne d’énergie",
                                    [u"Identifier les composants réalisant les fonctions Alimenter, Distribuer, Convertir, Transmettre",
                                     u"Justifier la solution choisie"]],
                          
                          "A2.10" : [u"Composants réalisant les fonctions de la chaîne d’information",
                                    [u"Identifier les composants réalisant les fonctions Acquérir, Traiter, Communiquer",
                                     u"Justifier la solution choisie"]],
                          
                          "A2.11" : [u"Réversibilité d’une source, d’un actionneur, d’une chaîne de transmission",
                                    [u"Analyser la réversibilité d’un composant dans une chaîne d’énergie"]],
                          
                          "A2.12" : [u"Système de numération, codage",
                                    [u"Analyser et interpréter une information numérique"]],
                          
                          "A2.13" : [u"Modèle OSI",
                                    [u"Décrire l’organisation des principaux protocoles"]],
                          
                          "A2.14" : [u"Réseaux de communication - Support de communication - Notion de protocole, paramètres de configuration - Notion de trame, liaisons série et parallèle",
                                    [u"Analyser les formats et les flux d’information",
                                     u"Identifier les architectures fonctionnelle et matérielle",
                                     u"Identifier les supports de communication",
                                     u"Identifier et analyser le message transmis, notion de protocole, paramètres de configuration"]],
                          
                          "A2.15" : [u"Architecture d’un réseau (topologie, mode de communication, type de transmission, méthode d’accès au support, techniques de commutation)",
                                    [u"Identifier les architectures fonctionnelle et matérielle d’un réseau"]],
                          
                          "A2.16" : [u"Matériaux",
                                    [u"Identifier la famille d’un matériau",
                                     u"Mettre en relation les propriétés du matériau avec les performances du système"]],
                          
                          "A2.17" : [u"Comportement du solide déformable",
                                    [u"Analyser les sollicitations dans les composants",
                                     u"Analyser les déformations des composants",
                                     u"Analyser les contraintes mécaniques dans un composant"]],
                          }],
                 
                "A3" : [u"Caractériser des écarts",
                       {"A3.1" : [u"Analyse des écarts",
                                 [u"Traiter des données de mesures (valeur moyenne, médiane, caractéristique, etc.)",
                                  u"Identifier des valeurs erronées",
                                  u"Quantifier des écarts entre des valeurs attendues et des valeurs mesurées",
                                  u"Quantifier des écarts entre des valeurs attendues et des valeurs obtenues par simulation",
                                  u"Quantifier des écarts entre des valeurs mesurées et des valeurs obtenues par simulation",
                                  u"Rechercher et proposer des causes aux écarts constatés"]]
                        
                        }],
                 
                 
                 
                 
                 
                 
                 "B1" : [u"Identifier et caractériser les grandeurs agissant sur un système",
                         {"B1.1" : [u"Frontière de l’étude",
                                   [u"Isoler un système et justifier l’isolement",
                                    u"Identifier les grandeurs traversant la frontière d’étude"]],
                                    
                          "B1.2" : [u"Caractéristiques des grandeurs physiques (mécaniques, électriques, thermiques, acoustiques, lumineuses, etc.)",
                                   [u"Qualifier les grandeurs d’entrée et de sortie d’un système isolé",
                                    u"Identifier la nature (grandeur effort, grandeur flux)",
                                    u"Décrire les lois d’évolution des grandeurs",
                                    u"Utiliser les lois et relations entre les grandeurs"]],
                          
                          "B1.3" : [u"Matériaux",
                                    [u"Identifier les propriétés des matériaux des composants qui influent sur le système"]],
                          
                          "B1.4" : [u"Énergie et puissances - Notion de pertes",
                                    [u"Associer les grandeurs physiques aux échanges d’énergie et à la transmission de puissance",
                                     u"Identifier les pertes d’énergie"]],
                          
                          "B1.5" : [u"Flux d’information",
                                    [u"Identifier la nature de l’information et la nature du signal"]],
                          
                          "B1.6" : [u"Flux de matière",
                                    [u"Qualifier la nature des matières, quantifier les volumes et les masses"]],
                          }],
                 
                 "B2" : [u"Proposer ou justifier un modèle",
                         {"B2.1" : [u"Chaîne d’énergie",
                                   [u"Associer un modèle à une source d’énergie",
                                    u"Associer un modèle aux composants d’une chaîne d’énergie",
                                    u"Déterminer les points de fonctionnement du régime permanent d’un actionneur au sein d’un procédé"]],
                                    
                          "B2.2" : [u"Chaîne d’information",
                                   [u"Associer un modèle aux composants d’une chaîne d’information"]],
                          
                          "B2.3" : [u"Ordre d’un système",
                                    [u"Identifier les paramètres à partir d’une réponse indicielle",
                                     u"Associer un modèle de comportement (1er et 2nd ordre) à une réponse indicielle"]],
                          
                          "B2.4" : [u"Systèmes logiques à évènements discrets - Langage de description : graphe d’états, logigramme, GRAFCET, algorigramme",
                                    [u"Traduire le comportement d’un système"]],
                          
                          "B2.5" : [u"Liaisons",
                                    [u"Construire un modèle et le représenter à l’aide de schémas",
                                     u"Préciser les paramètres géométriques",
                                     u"Établir la réciprocité mouvement relatif/actions mécaniques associées"]],
                          
                          "B2.6" : [u"Graphe de liaisons",
                                    [u"Construire un graphe de liaisons (avec ou sans les efforts)"]],
                          
                          "B2.7" : [u"Modèle du solide",
                                    [u"Choisir le modèle de solide, déformable ou indéformable selon le point de vue",
                                     u"Modéliser et représenter géométriquement le réel"]],
                          
                          "B2.8" : [u"Action mécanique",
                                    [u"Modéliser les actions mécaniques de contact ou à distance"]],
                          
                          "B2.9" : [u"Modèle de matériau",
                                    [u"Choisir ou justifier un modèle comportemental de matériau"]],
                          
                          "B2.10" : [u"Comportement du solide déformable",
                                    [u"Caractériser les sollicitations dans les composants",
                                     u"Caractériser les déformations des composants",
                                     u"Caractériser les contraintes mécaniques dans un composant"]],
                          
                          "B2.11" : [u"Modélisation plane",
                                    [u"Justifier la pertinence de la modélisation plane"]]
                          }],
                 
                 "B3" : [u"Résoudre et simuler",
                         {"B3.1" : [u"Principe fondamental de la dynamique (PFD) - Principes fondamentaux d’étude des circuitse",
                                   [u"Établir de façon analytique les expressions d’efforts (force, couple, pression, tension, etc.) et de flux (vitesse, fréquence de rotation, débit, intensité du courant, etc.)",
                                    u"Traduire de façon analytique le comportement d’un système"]],
                                    
                          "B3.2" : [u"Paramètres d’une simulation",
                                   [u"Adapter les paramètres de simulation, durée, incrément temporel, choix des grandeurs affichées, échelles, à l’amplitude et la dynamique de grandeurs simulées"]],
                          
                          "B3.3" : [u"Ordre d’un système",
                                    [u"Interpréter les résultats d’une simulation fréquentielle des systèmes du 1er et du 2nd ordre"]],
                          
                          "B3.4" : [u"Comportement du solide déformable",
                                    [u"Déterminer les parties les plus sollicitées dans un composant",
                                     u"Déterminer les valeurs extrêmes des déformations",
                                     u"Déterminer des concentrations de contraintes dans un composant"]],
                          
                          "B3.5" : [u"Modélisation plane",
                                    [u"Déterminer le champ des vecteurs vitesses des points d’un solide"]],
                          }],
                 
                 "B4" : [u"Valider un modèle",
                         {"B4.1" : [u"Modèle de connaissance",
                                   [u"Vérifier la compatibilité des résultats obtenus (amplitudes et variations) avec les lois et principes physiques d’évolution des grandeurs",
                                    u"Comparer les résultats obtenus (amplitudes et variations) avec les données du cahier des charges fonctionnel"]],
                                    
                          "B4.2" : [u"Matériaux",
                                   [u"Adapter les paramètres de simulation, durée, incrément temporel, choix des grandeurs affichées, échelles, à l’amplitude et la dynamique de grandeurs simuléesIdentifier l’influence des propriétés des matériaux sur les performances du système",
                                    u"Proposer des matériaux de substitution pour améliorer les performances du système"]],
                          
                          "B4.3" : [u"Structures",
                                    [u"Valider l’influence de la structure sur les performances du système",
                                     u"Proposer des modifications structurelles pour améliorer les performances du système"]],
                          
                          "B4.4" : [u"Grandeurs influentes d’un modèle",
                                    [u"Modifier les paramètres d’un modèle"]],
                          }],
                 }



dicCompetences_SSI =  {"A" : [u"Analyser",
                             {"A1" : [u"Analyser le besoin",
                                      {"A1.1" : u"définir le besoin",
                                       "A1.2" : u"définir les fonctions de service",
                                       "A1.3" : u"identifier les contraintes",
                                       "A1.4" : u"traduire un besoin fonctionnel en problématique technique"}],
                              "A2" : [u"Analyser le système",
                                      {"A2.1" : u"identifier et ordonner les fonctions techniques qui réalisent les fonctions de services et respectent les contraintes",
                                       "A2.2" : u"identifier les éléments transformés et les flux",
                                       "A2.3" : u"décrire les liaisons entre les blocs fonctionnels",
                                       "A2.4" : u"identifier l’organisation structurelle",
                                       "A2.5" : u"identifier les matériaux des constituants et leurs propriétés en relation avec les fonctions et les contraintes"}],
                              "A3" : [u"Caractériser des écarts",
                                      {"A3.1" : u"comparer les résultats expérimentaux avec les résultats simulés et interpréter les écarts",
                                       "A3.2" : u"comparer les résultats expérimentaux avec les critères du cahier des charges et interpréter les écarts",
                                       "A3.3" : u"comparer les résultats simulés avec les critères du cahier des charges et interpréter les écarts"}]},
                             ],
                      
                      "B" : [u"Modéliser",
                             {"B1" : [u"Identifier et caractériser les grandeurs agissant sur un système",
                                      {"B1.1" : u"définir, justifier la frontière de tout ou partie d’un système et répertorier les interactions",
                                       "B1.2" : u"choisir les grandeurs et les paramètres influents en vue de les modéliser"}],
                              "B2" : [u"Proposer ou justifier un modèle",
                                      {"B2.1" : u"associer un modèle à un système ou à son comportement",
                                       "B2.2" : u"préciser ou justifier les limites de validité du modèle envisagé"}],
                              "B3" : [u"Résoudre et simuler",
                                      {"B3.1" : u"choisir et mettre en oeuvre une méthode de résolution",
                                       "B3.2" : u"simuler le fonctionnement de tout ou partie d’un système à l’aide d’un modèle fourni"}],
                              "B4" : [u"Valider un modèle",
                                      {"B4.1" : u"interpréter les résultats obtenus",
                                       "B4.2" : u"préciser les limites de validité du modèle utilisé",
                                       "B4.3" : u"modifier les paramètres du modèle pour répondre au cahier des charges ou aux résultats expérimentaux",
                                       "B4.4" : u"valider un modèle optimisé fourni"}]},
                             ],
                      
                      "C" : [u"Expérimenter",
                             {"C1" : [u"Justifier le choix d’un protocole expérimental",
                                      {"C1.1" : u"identifier les grandeurs physiques à mesurer",
                                       "C1.2" : u"décrire une chaîne d’acquisition",
                                       "C1.3" : u"identifier le comportement des composants",
                                       "C1.4" : u"justifier le choix des essais réalisés"}],
                              "C2" : [u"Mettre en oeuvre un protocole expérimental",
                                      {"C2.1" : u"conduire les essais en respectant les consignes de sécurité à partir d’un protocole fourni",
                                       "C2.2" : u"traiter les données mesurées en vue d’analyser les écarts"}]}
                             ],
                      
                      "D" : [u"Communiquer",
                             {"D1" : [u"Rechercher et traiter des informations",
                                      {"D1.1" : u"rechercher des informations",
                                       "D1.2" : u"analyser, choisir et classer des informations"}],
                              "D2" : [u"Mettre en oeuvre une communication",
                                      {"D2.1" : u"choisir un support de communication et un média adapté, argumenter",
                                       "D2.2" : u"produire un support de communication",
                                       "D2.3" : u"adapter sa stratégie de communication au contexte"}]}
                             ]
                      }


dicCompetences_prj_SSI =  {"B" : [dicCompetences_SSI["B"][0],
                                 {"B3" : [dicCompetences_SSI["B"][1]["B3"][0],
                                          {"B3.2" : dicCompetences_SSI["B"][1]["B3"][1]["B3.2"]}],
                                  "B4" : dicCompetences_SSI["B"][1]["B4"]}],
                           
                           "C" : dicCompetences_SSI["C"],
                           
                           "D" : dicCompetences_SSI["D"]}
                           
#################################################################################################################################
#
#        Les indicateurs de compétences
#                (True = revue ; False = soutenance)
#
#################################################################################################################################
dicIndicateurs_prj_SSI = {"B3" : [[u"Les paramètres influents sont identifiés", True],
                                  [u"Les limites de simulation sont correctement définies", True]
                                  ],
                          "B4" : [[u"Les résultats sont correctement interprétés", False],
                                  [u"Ces limites sont explicitées", False],
                                  [u"Les paramètres modifiés sont pertinents", False],
                                  [u"Le modèle modifié répond aux attentes ", False]
                                  ],
                          "C1" : [[u"Les grandeurs spécifiques (d'entrée, sortie, matière d'œuvre…) sont correctement identifiées", True],
                                  [u"Les éléments de la chaîne sont correctement identifiés ", True],
                                  [u"Les choix et réglages des capteurs et appareils de mesure sont correctement explicités", True],
                                  [u"Un protocole expérimental adapté de recueil de résultats est conçu ou complété, validé et mis en œuvre", True],
                                  [u"Le comportement est précisément décrit", False]],
                          "C2" : [[u"Les capteurs et appareils de mesure sont correctement mis en œuvre", True],
                                  [u"Le système étudié est correctement mis en œuvre", True],
                                  [u"Les règles de sécurité sont connues et respectées", True],
                                  [u"Les résultats sont présentés clairement", True],
                                  [u"Le protocole d'essai est respecté", True],
                                  [u"Les méthodes et outils de traitement sont cohérents avec le problème posé", True],
                                  [u"Les résultats sont correctement analysés", False]],
                          "D1" : [[u"Les outils de recherche documentaire sont bien choisis", False],
                                  [u"Les techniques de recherche documentaire sont maîtrisées", False],
                                  [u"Les informations conservées sont opportunes", False],
                                  [u"Le classement des données permet de les retrouver rapidement", False]
                                  ],
                          "D2" : [[u"Les outils de communication sont maîtrisés", False],
                                  [u"Le support utilisé est adapté", False],
                                  [u"La production finale permet la compréhension du problème et de sa résolution ", False],
                                  [u"La production respecte le cahier des charges (écrit/oral, texte/vidéo, durée, public visé, …)", False]
                                  ]
                              }
     
#################################################################################################################################
#
#        Les poids des indicateurs de compétences
#
#################################################################################################################################
dicPoidsIndicateurs_prj_SSI = {"B" : [40, 
                                      {"B3" : [20,20],
                                       "B4" : [15,15,15,15]}],
                               "C" : [40,
                                      {"C1" : [8,8,7,10,5],
                                       "C2" : [8,8,8,9,10,9,10]}],
                               "D" : [20, 
                                      {"D1" : [10,5,5,10],
                                       "D2" : [20,10,20,20],
                                        }]
                               }
