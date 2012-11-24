#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               constantes ITEC                           ##
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
#   Définition des constantes pour la spécialité ITEC
#
####################################################################################

CentresInterets_ITEC = [u"Besoin et performance d'un système",
                       u"Compétitivité, design et ergonomie des systèmes",
                       u"Eco-conception des mécanismes",
                       u"Structure, matériaux et protections d'un système",
                       u"Transmission de mouvement et de puissance d'un système",
                       u"Procédés de réalisation"
                       ]



dicSavoirs_ITEC = {"1" : [u"Projet technologique",
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
                          "1.2" : [u"Créativité et innovation technologique",
                                   [u"Méthodes de créativité rationnelles et non rationnelles (lois d'évolutions et principes d'innovation, contradictions, relations entre solutions techniques et principes scientifiques/technologiques associées, méthodes de brainstorming)",
                                    u"Contraintes de règlementation, normes, propriété industrielle et brevets",
                                    u"Dimension Desing d'un produit, impact d'une approche Design sur les fonctions, la structure et les solutions techniques",
                                    u"Intégration des fonctions et optimisation du fonctionnement : approche pluritechnologique et transferts de technologie"]],
                          "1.3" : [u"Description et représentation",
                                   [u"Analyse fonctionnelle (selon les normes en vigueur : cahier des charges fonctionnel, indices de flexibilité)",
                                    u"Représentation d'une idée, d'une solution : croquis, schémas de principe à main levée",
                                    u"Schémas cinématique (minimal ou non) et structurel"]]
                          }],
                  "2" : [u"Conception mécanique des systèmes",
                         {"2.1" : [u"Conception des mécanismes",
                                   [u"Modification d'un mécanisme : définition volumique et numérique (CAO 3D) des modifications d'un mécanisme à partir de contraintes fonctionnelles",
                                    u"Définition volumique et numérique (CAO 3D) des formes et dimensions d'une pièce, prise en compte des contraintes fonctionnelles",
                                    u"Influence du principe de réalisation et du matériau choisis sur les formes et dimensions d'une pièce simple",
                                    u"Choix d'une solution : critères de choix associés à une conception ou à l'intégration d'une solution dans un système global - coût, fiabilité, environnement, ergonomie et design - Matrice de comparaison de plusieurs critères",
                                    u"Formalisation et justification d'une solution de conception : illustrations 3D (vues photos réalistes, éclatés, mises en plan, diagramme causse effet, carte mentale, présentation PAO)"]],
                          "2.2" : [u"Comportement d'un mécanisme et/ou d'une pièce",
                                   [u"Simulations mécaniques : modélisation et simulation (modèle simplifié et modèle numérique, validation des hypothèses)",
                                    u"Résistance des matériaux : hypothèses et modèle poutre, types de sollicitations simples, notion de contraintes et de déformation, loi de Hooke et module d'Young, limite élastique, étude d'une sollicitation simple",
                                    u"Equilibre des solides : modélisation des liaisons, actions mécaniques, principe fondamental de la statique, résolution d'un problème de statique plane",
                                    u"Mouvements des mécanismes : modélisation des liaisons, trajectoires, vitesses, accélérations, mouvements plans, résolution graphique d'un problème de cinématique plane",
                                    u"Impacts environnementaux des solutions constructives : unité fonctionnelle, unités associées",
                                    u"Interprétation des résultats d'une simulation : courbe, tableau, graphe, unités associées",
                                    u"Scénario de simulation pour comparer et valider une solution, modifier une pièce ou un mécanisme"]]
                          }],
                  "3" : [u"Prototypage de pièces",
                         {"3.1" : [u"Procédés de transformation de la matière",
                                   [u"Principes de transformation de la matière (ajout, enlèvement, transformation et déformation de la matière)\n" \
                                    u"Paramètres liés aux procédés\n" \
                                    u"Limitations, contraintes liées :\n" \
                                    u"- aux matériaux\n" \
                                    u"- aux possibilités des procédés\n" \
                                    u"- aux coûts\n" \
                                    u"- à l'environnement",
                                    u"Expérimentation de procédés, protocole de mise en œuvre, réalisation de pièces prototypes",
                                    u"Prototypage rapide : simulation et préparation des fichiers, post traitement de la pièce pour une exploitation en impression 3D",
                                    u"Coulage de pièces prototypées en résine et/ou en alliage métallique (coulée sous vide)"]],
                          "3.2" : [u"Essais, mesures et validation",
                                   [u"Conformité dimensionnelle et géométrique des pièces en relation avec les contraintes fonctionnelles de la maquette numérique",
                                    u"Essais mécaniques sur les matériaux (traction, compression, flexion simple, dureté)",
                                    u"Intégration d'une ou plusieurs pièces dans un système (graphe de montage, assemblages, réglages, essais)",
                                    u"Mesure et validation de performances : essais de caractérisation sur une pièce ou sur tout ou partie d'un système (efforts, déformation, matériau, dimensions, comportements statique, cinématique, énergétique)"]]
                          }]
                  }



dicCompetences_ITEC = {"O7" : [u"Imaginer une solution, répondre à un besoin",
                              {"CO7.itec1" : u"Identifier et justifier un problème technique à partir de l'analyse globale d'un système (approche Matière - Energie - Information)",
                               "CO7.itec2" : u"Proposer des solutions à un problème technique identifié en participant à des démarches de créativité, choisir et justifier la solution retenue",
                               "CO7.itec3" : u"Définir, à l'aide d'un modeleur numérique, les formes et dimensions d'une pièce d'un mécanisme à partir des contraintes fonctionnelles, de son principe de réalisation et de son matériau",
                               "CO7.itec4" : u"Définir, à l'aide d'un modeleur numérique, les modifications d'un mécanisme à partir des contraintes fonctionnelles"}],
                      "O8" : [u"Valider des solutions techniques",
                              {"CO8.itec1" : u"Paramétrer un logiciel de simulation mécanique pour obtenir les caractéristiques d'une loi d'entrée/sortie d'un mécanisme simple",
                               "CO8.itec2" : u"Interpréter les résultats d'une simulation mécanique pour valider une solution ou modifier une pièce ou un mécanisme",
                               "CO8.itec3" : u"Mettre en oeuvre un protocole d'essais et de mesures, interpréter les résultats",
                               "CO8.itec4" : u"Comparer et interpréter le résultat d'une simulation d'un comportement mécanique avec un comportement réel"}],
                      "O9" : [u"Gérer la vie du produit",
                              {"CO9.itec1" : u"Expérimenter des procédés pour caractériser les paramètres de transformation de la matière et leurs conséquences sur la définition et l'obtention de pièces",
                               "CO9.itec2" : u"Réaliser et valider un prototype obtenu par rapport à tout ou partie du cahier des charges initial",
                               "CO9.itec3" : u"Intégrer les pièces prototypes dans le système à modifier pour valider son comportement et ses performances"}]}


#################################################################################################################################
#
#        Les indicateurs de compétences
#                (True = revue ; False = soutenance)
#
#################################################################################################################################
dicIndicateurs_prj_ITEC = {"CO7.itec1" : [[u"Le besoin relatif au projet est identifié et justifié", True],
                                           [u"Les fonctions principales du projet sont identifiées", True],
                                           [u"Les critères du CDC du projet sont décodés", True],
                                           [u"La démarche d'analyse du problème est pertinente", True],
                                           [u"Les principaux points de vigilance relatifs au projet sont identifiés", True]
                                          ],
                           "CO7.itec2" : [[u"Les grandes étapes d'une démarche de créativité sont franchies de manière cohérente", True],
                                          [u"Les moyens conventionnels de représentation des solutions sont correctement utilisés (croquis, schémas, ...)", True],
                                          [u"Les contraintes de normes, propriétés industrielle et brevet sont identifiées", True],
                                          [u"Les solutions techniques proposées sont pertinentes", True],
                                          [u"Les caractéristiques comportementales de la solution retenue répondent au CDC", True],
                                          [u"Les choix sont explicités et la solution justifiée en regard des paramètres choisis", True],
                                          ],
                           "CO7.itec3" : [[u"La démarche de création est rationnelle", True],
                                          [u"Les contraintes fonctionnelles sont traduites de manière complète", True],
                                          [u"Les formes et dimensions sont compatibles avec le principe de réalisation, le matériau choisi et les contraintes subies", True]
                                          ],
                           "CO7.itec4" : [[u"Les modifications respectent les contraintes fonctionnelles", True],
                                          [u"La procédure de modification est rationnelle", True]
                                          ],
                           "CO8.itec1" : [[u"Les variables du modèle sont identifiées", True],
                                          [u"Leurs influences respectives sont identifiées", True],
                                          [u"Les paramètres saisis sont réalistes", True]
                                          ],
                           "CO8.itec2" : [[u"Les scénarios de simulation sont identifiés", True],
                                          [u"Les paramètres influents sont identifiés", True],
                                          [u"Les conséquences sur le mécanisme sont identifiées", True],
                                          [u"Les modifications proposées sont pertinentes", True],
                                         ],
                           "CO8.itec3" : [[u"Les conditions de l'essai sont identifiées et justifiées", True],
                                          [u"Le protocole est adapté à l'objectif", True],
                                          [u"Les observations et mesures sont méthodiquement menées", True],
                                          [u"Les incertitudes sont estimées", True],
                                          [u"L'interprétation des résultats est cohérente", True]
                                         ],
                           "CO8.itec4" : [[u"Les résultats de la simulation et les mesures sont corrélés", True],
                                          [u"L'analyse des écarts est méthodique", True],
                                          [u"L'interprétation des résultats est cohérente", True]
                                          ],
                           "CO9.itec1" : [[u"Les paramètres significatifs à observer sont identifiés", True],
                                          [u"Le protocole est adapté à l'objectif", True],
                                          [u"Des conséquences pertinentes sont identifiées", True]
                                         ],
                           "CO9.itec2" : [[u"Un moyen de prototypage réaliste est choisi en regard de la partie de CDC à respecter", True],
                                          [u"La réalisation du prototype est conforme à une procédure valide", True],
                                          [u"Les caractéristiques à valider sont identifiées", True],
                                          [u"La corrélation des caractéristiques permet de valider le prototype par rapport au CDC", True]
                                         ],
                           "CO9.itec3" : [[u"Les pièces prototypes s'insèrent dans le mécanisme", True],
                                          [u"Une procédure d'essai pertinente est définie", True],
                                          [u"L'essai est méthodiquement réalisé et le comportement du mécanisme relevé", True],
                                          [u"L'interprétation des résultats est pertinente", True]
                                         ]}


#################################################################################################################################
#
#        Les poids des indicateurs de compétences
#
#################################################################################################################################
dicPoidsIndicateurs_prj_ITEC =   {"O7" : [40, 
                                          {"CO7.itec1" : [5,5,5,7,7],
                                           "CO7.itec2" : [5,5,5,7,7,7],
                                           "CO7.itec3" : [7,7,7],
                                           "CO7.itec4" : [7,7]}],
                                  "O8" : [40, 
                                          {"CO8.itec1" : [7,6,7],
                                           "CO8.itec2" : [6,7,7,7],
                                           "CO8.itec3" : [6,7,6,6,7],
                                           "CO8.itec4" : [7,7,7]}],
                                  "O9" : [20,
                                          {"CO9.itec1" : [9,9,9],
                                           "CO9.itec2" : [9,9,9,9],
                                           "CO9.itec3" : [9,9,9,10]}]}

# Nombre indicateurs = 42