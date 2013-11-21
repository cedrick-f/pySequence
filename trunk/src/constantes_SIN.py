#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               constantes SIN                            ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2011 Cédrick FAURY - Jean-Claude FRICOU

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
Enseigmenent = [u"STI2D-SIN", u"STI2D : Systèmes d'Information et Numérique"]

CentresInterets = [u"Configuration et performances du traitement de l'information",
                       u"Instrumentation/Acquisition et restitution de grandeurs physiques",
                       u"Communication de l'information/Au sein d'un système",
                       u"Gestion de l'information/Structures matérielles et logicielles associées au traitement de l'information",
                       u"Communication entre systèmes",
                       u"Traitement analogique de l'information",
                       u"Cycle de vie d'un produit"
                       ]


dicSavoirs = {"1" : [u"Projet technologique",
                         {"1.1" : [u"La démarche de projet",
                                   {"1.1.1" : [u"Les projets industriels",
                                               [u"Typologie des entreprises industrielles et des projets techniques associés (projets locaux, transversaux, \"joint venture\")",
                                                u"Phases d'un projet industriel (marketing, pré conception, pré industrialisation et conception détaillé, industrialisation, maintenance et fin de vie)",
                                                u"Principes d'organisation et planification d'un projet (développement séquentiel, chemin critique, découpage du projet en fonctions élémentaires ou en phases) Gestion, suivi et finalisation d'un projet (coût, budget, bilan d'expérience)"]
                                               ],
                                    "1.1.2" : [u"Les projets pédagogiques et technologiques",
                                               [u"Etapes et planification d'un projet technologique (revues de projets, travail collaboratif en équipe projet : ENT, base de données, formats d'échange, carte mentale, flux opérationnels)",
                                                u"Animation d'une revue de projet ou management d'une équipe projet",
                                                u"Evaluation de la prise de risque dans un projet par le choix des solutions technologiques (innovations technologiques, notion de coût global, veille technologique)"]
                                               ]
                                    }],
                          "1.2" : [u"Mise en oeuvre d'un système",
                                   [u"Décodage des notices techniques d'un système et des procédures d'installation",
                                    u"Compte-rendu de la mise en oeuvre d'un système, en utilisant un langage technique précis",
                                    u"Identification des dysfonctionnements et/ou description des solutions"]
                                   ],
                          "1.3" : [u"Description et représentation",          
                                    [u"Décodage d'un cahier des charges fonctionnel décrivant un besoin exprimé",
                                    u"Identification des fonctions définies par l'expression du besoin. Caractérisation de leurs performances à partir de mesures, conclusions sur leur conformité au regard du cahier des charges",
                                    u"Propositions d'évolutions pour chaque fonction caractérisée à partir d'un schéma de principe relatif à son fonctionnement, en repérant les constituants des chaînes d'énergie et d'information",
                                    u"Réalisation d'une représentation fonctionnelle (schémas blocs, norme SysML)",
                                    u"Représentation du comportement des constituants (dans les domaines temporel et/ou fréquentiel)"]],
                         }],
                  "2" : [u"Maquettage des solutions constructives",
                         {"2.1" : [u"Conception fonctionnelle d'un système local",
                                   [u"Acquisition, conditionnement et filtrage d'une information (sous forme analogique)",
                                    u"Conversion d'une information (CAN et CNA)",
                                    u"Traitement d'une information numérique",
                                    u"Traitement d'une information analogique",
                                    u"Traitement programmé et composants programmables",
                                    u"Modulation, démodulation d'un signal porteur d'une information : amplitude, fréquence, phase",
                                    u"Multiplexage d'une information et codage d'une transmission en bande de base",
                                    u"Transmission d'une information (liaison filaire et non filaire)",
                                    u"Restitution d'une information : voix, données, images"]],
                                    
                          "2.2" : [u"Architecture fonctionnelle d'un système communicant",
                                   [u"Modèles en couche des réseaux, protocole Ethernet et adresse logique (IP) du protocole IP. Lien adresse MAC/IP : Protocole ARP",
                                    u"Architecture client/serveur",
                                    ]],
                          "2.3" : [u"Modélisations et simulations",
                                    [u"Modèle de comportement fréquentiel relatif à la fonction filtrage (bande-passante, fréquence de coupure)",
                                     u"Diagramme états-transitions pour un système événementiel",
                                     u"Modèle de comportement : utilisation de librairies logicielles et paramétrage de caractéristiques",
                                     u"Architecture de la chaîne d'information et paramétrage du simulateur",
                                     u"Simulations et analyses des résultats",
                                     u"Identification des variables simulées et mesurées sur le système pour valider le choix d'une solution"]]
                          }],
                "3" : [u"Réalisation et qualification d'un prototype",
                       {"3.1" : [u"Réalisation d'un prototype",
                                 [u"Implémentation d'un programme dans un composant programmable",
                                  u"Interfaçage de composants",
                                  u"Interconnexion des fonctions distribuées",
                                  u"Programmation de l'interface de communication",
                                  u"Conditionnement des grandeurs acquises (convertir, amplifier, traiter)",
                                  u"Adaptation d'une chaîne d'acquisition aux caractéristiques des grandeurs à acquérir",
                                  u"Recette du prototype au regard des spécifications attendues du cahier des charges"]],
                        "3.2" : [u"Gestion de la vie d'un système",
                                 [u"Validation d'un prototype",
                                  u"Procédures d'intervention",
                                  u"Mise à jour d'un système d'information",
                                  u"Rédaction d'un compte-rendu sur l'activité de maintenance",
                                  u"Performances d'un projet finalisé",
                                  u"Etude prospective technique et économique",
                                  u"Proposition d'une solution et organisation du nouveau projet"]]
                        }]}



dicCompetences = {"O7" : [u"Imaginer une solution, répondre à un besoin",
                              {"CO7.sin1" : u"Décoder la notice technique d'un système, vérifier la conformité du fonctionnement",
                               "CO7.sin2" : u"Décoder le cahier des charges fonctionnel décrivant le besoin exprimé, identifier la fonction définie par un besoin exprimé, faire des mesures pour caractériser cette fonction et conclure sur sa conformité",
                               "CO7.sin3" : u"Exprimer le principe de fonctionnement d'un système à partir des diagrammes SysML pertinents. Repérer les constituants de la chaîne d'énergie et d'information"}],
                      "O8" : [u"Valider des solutions techniques",
                              {"CO8.sin1" : u"Rechercher et choisir une solution logicielle ou matérielle au regard de la définition d'un système",
                               "CO8.sin2" : u"Etablir pour une fonction précédemment identifiée, un modèle de comportement à partir de mesures faites sur le sytème",
                               "CO8.sin3" : u"Traduire sous forme graphique l'architecture de la chaîne d'information identifiée pour un système et définir les paramètres d'utilisation du simulateur",
                               "CO8.sin4" : u"Identifier les variables simulées et mesurées sur un système pour valider le choix d'une solution",}],
                      "O9" : [u"Gérer la vie d'un système",
                              {"CO9.sin1" : u"Utiliser les outils adaptés pour planifier un projet (diagramme de Gantt, chemin critique, données économiques, réunions de projet)",
                               "CO9.sin2" : u"Installer, configurer et instrumenter un système réel. Mettre en oeuvre la chaîne d'acquisition puis acquérir, traiter, transmettre et restituer l'information",
                               "CO9.sin3" : u"Rechercher des évolutions de constituants dans le cadre d'une démarche de veille technologique, analyser la structure d'un système pour intervenir sur les constituants dans le cadre d'une opération de maintenance",
                               "CO9.sin4" : u"Rechercher et choisir de nouveaux constituants d'un système (ou d'un projet finalisé) au regard d'évolutions technologiques, socioéconomiques spécifiées dans un cahier des charges. Organiser le projet permettant de maquettiser la solution choisie"}]}




#################################################################################################################################
#
#        Les indicateurs de compétences
#                (True = revue ; False = soutenance)
#
#################################################################################################################################
dicIndicateurs_prj = {"CO7.sin1" : [[u"La traduction de la notice du système permet de décrire une procédure", True],
                                        [u"Le système est installé et paramétré", True],
#                                        [u"Les critères du CDC du projet sont décodés", True],
                                        [u"Les mesures sont effectuées et comparées aux caractéristiques de la notice technique", True],
                                        [u"Un rapport de mise en oeuvre et d'essais est rédigé", True]
                                        ],
                         "CO7.sin2" : [[u"Le besoin est identifié", True],
                                       [u"La fonction est identifiée", True],
                                       [u"Une procédure pertinente est proposée et mise en oeuvre", True],
                                       [u"La fonction est caractérisée", True],
                                        [u"Un rapport de conformité est rédigé", True]
                                        ],
                         "CO7.sin3" : [[u"Le système est modélisé à l'aide de diagrammes conformes", True],
                                        [u"Les diagrammes permettant d'exprimer le principe de fonctionnement sont utilisés", True],
                                        [u"Les interactions avec la chaîne d'énergie sont identifiées", True],
                                        [u"Les constituants sont identifiés", True]
                                        ],
                         "CO8.sin1" : [[u"La définition du système est exprimée correctement", True],
                                       [ u"Une liste non exhaustive de solutions pertinentes est établie", True],
                                       [ u"Le choix de la solution est argumenté", True]
                                        ],
                         "CO8.sin2" : [[u"Les mesures nécessaires sont effectuées", True],
                                       [ u"Un modèle de comportement pertinent est établi", True],
                                       [ u"Les paramètres du modèle sont renseignés pour limiter les écarts avec les mesures", True],
                                       [ u"Le modèle de comportement est complété si nécessaire", True]
                                        ],
                         "CO8.sin3" : [[u"La chaîne d'information est modélisée par des diagrammes adaptés (SysML)", True],
                                       [ u"Le diagramme états/transitions est programmé", True],
                                       [ u"Le diagramme paramétrique est renseigné", True]
                                        ],
                         "CO8.sin4" : [[u"Les grandeurs caractéristiques du système simulé sont identifiées", True],
                                       [ u"Les variables caractéristiques du système mesuré sont identifiées", True],
                                       [ u"Les paramètres du système simulé sont affinés pour réduire les écarts avec le système réel", True],
                                       [ u"Les conditions de simulation sont argumentées pour valider le choix d'une solution", True]
                                        ],
                         "CO9.sin1" : [[u"Le CDC fonctionnel est analysé et reformulé", True],
                                       [ u"Les données économiques sont identifiées", True],
                                       [ u"Les chemins critiques sont mis en évidence et les dates de réunions de projet sont fixées", True]
                                        ],
                         "CO9.sin2" : [[u"La notice du système est décodée", True],
                                        [u"Le système est installé et paramétré", True],
                                        [u"Les grandeurs caractéristiques sont identifiées et le système est instrumenté de manière adaptée", True],
                                        [u"Les grandeurs sont acquises, traitées et transmises", True],
                                        [u"Les contraintes temporelles et fréquentielles sont respectées, l'information est restituée", True]
                                        ],
                         "CO9.sin3" : [[u"Une veille technologique est effectuée et une liste non exhaustive de l'évolution des constituants est établie", True],
                                        [u"Les procédures adaptées d'intervention sur les contsituants sont proposées", True],
                                        [u"L'intervention de maintenance sur le système est planifiée et la continuité de service assurée", True],
                                        [u"Le rapport de maintenance est établi", True]
                                        ],
                         "CO9.sin4" : [[u"Le nouveau cahier des charges fonctionnel est décodé et traduit en proposition d'action", True],
                                       [u"Les contraintes socio-économiques sont identifiées", True],
                                       [u"Des constituants sont choisis et justifiés", True],
                                       [u"Un diagramme de Gantt est établi", True],
                                       [u"Le prototypage rapide de la solution est organisé", True]
                                       ]}
                  
dicPoidsIndicateurs_prj =  {"O7" : [40,
                                        {"CO7.sin1" : [6,10,10,6],
                                         "CO7.sin2" : [6,6,10,6,6],
                                         "CO7.sin3" : [10,10,8,6]}],
                                "O8" : [40,
                                        {"CO8.sin1" : [6,6,10],
                                         "CO8.sin2" : [6,10,6,6],
                                         "CO8.sin3" : [6,10,6],
                                         "CO8.sin4" : [10,6,6,6]}],
                                "O9" : [20,
                                        {"CO9.sin1" : [5,5,10],
                                         "CO9.sin2" : [5,10,5,5,5],
                                         "CO9.sin3" : [5,5,5,5],
                                         "CO9.sin4" : [5,5,5,5,10]}]
                                }

#################################################################################################################################
#
#        Les constantes pour les grilles d'évaluation de projet
#
#################################################################################################################################
Fichier_GRILLE = ["Grille_evaluation_STI2D_SIN_revues.xlsm", "Grille_evaluation_STI2D_SIN_revues.xls"]

Cellules_NON =  {"CO7.sin1" : [(5,4), (6,4), (7,4), (8,4)],
                     "CO7.sin2" : [(9,4), (10,4), (11,4), (12,4), (13,4)],
                     "CO7.sin3" : [(14,4), (15,4), (16,4), (17,4)],
                     "CO8.sin1" : [(19,4), (20,4), (21,4)],
                     "CO8.sin2" : [(22,4), (23,4), (24,4), (25,4)],
                     "CO8.sin3" : [(26,4), (27,4), (28,4)],
                     "CO8.sin4" : [(29,4), (30,4), (31,4), (32,4)],
                     "CO9.sin1" : [(34,4), (35,4), (36,4)],
                     "CO9.sin2" : [(37,4), (38,4), (39,4), (40,4), (41,4)],
                     "CO9.sin3" : [(42,4), (43,4), (44,4), (45,4)],
                     "CO9.sin4" : [(46,4), (47,4), (48,4), (49,4), (50,4)]}

#################################################################################################################################
#
#        Les cellules "Savoirs" dans le tableau de bilan
#
#################################################################################################################################
fichierProgressionProgramme = u"SSI_Synthese.xlsx"
dicCellSavoirs = {"A1.1" : [10,13],
                  "A1.2" : [14,15],
                  "A1.3" : [16,16],
                 
                  "A2.1" : [18,21],
                  "A2.2" : [22,27],
                  "A2.3" : [28,28],
                  "A2.4" : [29,30],
                  "A2.5" : [31,31],
                  "A2.6" : [32,34],
                  "A2.7" : [35,36],
                  "A2.8" : [37,37],
                  "A2.9" : [38,39],
                  "A2.10" : [40,41],
                  "A2.11" : [42,42],
                  "A2.12" : [43,43],
                  "A2.13" : [44,44],
                  "A2.14" : [45,48],
                  "A2.15" : [49,49],
                  "A2.16" : [50,51],
                  "A2.17" : [52,54],

                  "A3.1" : [56,61],
                        
                  "B1.1" : [65,66],
                  "B1.2" : [67,70],
                  "B1.3" : [71,71],
                  "B1.4" : [72,73],
                  "B1.5" : [74,74],
                  "B1.6" : [75,75],
                 
                  "B2.1" : [77,79],
                  "B2.2" : [80,80],
                  "B2.3" : [81,82],
                  "B2.4" : [83,83],
                  "B2.5" : [84,86],
                  "B2.6" : [87,87],
                  "B2.7" : [88,89],
                  "B2.8" : [90,90],
                  "B2.9" : [91,91],
                  "B2.10" : [92,94],
                  "B2.11" : [95,95],
                 
                  "B3.1" : [97,98],
                  "B3.2" : [99,99],
                  "B3.3" : [100,100],
                  "B3.4" : [101,103],
                  "B3.5" : [104,104],
                 
                  "B4.1" : [106,107],
                  "B4.2" : [108,109],
                  "B4.3" : [110,111],
                  "B4.4" : [112,112],
                  
                  "C1.1" : [116,118],
                  "C1.2" : [119,120],
                  "C1.3" : [121,122],
                 
                  "C2.1" : [124,125],
                  "C2.2" : [126,126],
                  "C2.3" : [127,127],
                  "C2.4" : [128,128],
                  "C2.5" : [129,130],
                 
                  "D1.1" : [134,135],
                  "D1.2" : [136,136],
                  "D1.3" : [137,141],
                  
                  "D2.1" : [143,143],
                  "D2.2" : [144,147]
                  
                 }