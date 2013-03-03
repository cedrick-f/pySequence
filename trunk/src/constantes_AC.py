#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               constantes AC                             ##
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
#   Définition des constantes pour la spécialité AC
#
####################################################################################
Enseigmenent = [u"STI2D-AC", u"STI2D : Architecture et Construction"]

CentresInterets = [u"Participation à une étude architecturale",
                       u"Vérification de la résistance",
                       u"Protection",
                       u"Le confort",
                       u"Organisation de réalisation",
                       u"Vie en oeuvre",
                       u"Reconditionnement de l'ouvrage",
                       u"Valorisation de la fin de vie de l'ouvrage"
                       ]



dicSavoirs = {"1" : [u"Projet technologique",
                         {"1.1" : [u"La démarche de projet",
                                   [u"Environnement économique et professionnel",
                                    u"Planification d'un projet de construction : découpage en phase, diagramme de Gantt, notion de chemin critique",
                                    u"Pilotage d'un projet : revue de projet, notion de coût et de budget, élaboration d'un bilan d'expérience en vue de traçabilité. Travail collaboratif : ENT, base de données, formats d'échange, carte mentale, flux opérationnels",
                                    u"Evaluation de la prise de risque dans un projet par le choix des solutions technologiques (innovations technologiques, notion de coût global, veille technologique",
                                    u"Outils de communication technique : croquis, maquette, représentation normalisée, modeleur volumique et module métier, notice descriptive"]
                                    ],
                            "1.2" : [u"Projet architectural",
                                   [u"Analyse fonctionnelle adaptée à la construction. Organigramme fonctionnel",
                                    u"Conception bioclimatique. Système porteurs. Conformité aux règlementations",
                                    u"Association de dispositions constructives et de performances attendues : - isolation thermique et acoustique, éclairage, qualité de l'air - accessibilité du cadre bâti pour personnes en situation de handicap, prédimensionnements architecturaux, architecture bioclimatique"
                                    ]
                                   ],
                          "1.3" : [u"Etablir une organisation de réalisation",          
                                    [u"Phasage des opérations. Logistique de chantier. Validations de procédés de mise en oeuvre. Impact carbone. Tri des déchets"
                                     ]]
                         }],
                  "2" : [u"Conception d'un ouvrage",
                         {"2.1" : [u"Paramètres influant la conception",
                                   [u"Repérage des caractéristiques propres de solutions architecturales : - articulation entre les grandes étapes de l'histoire des constructions et leur contexte socio-économique - principales réalisations des bâtisseurs depuis le XVIII° siècle - composition architecturale : vocabulaire, éléments de syntaxe, proportion, échelle - références culturelles, historiques, sociales",
                                    u"Le confort : - hygromthermique - acoustique - visuel - repiratoire",
                                    u"Choix des sources d'énergie du projet : - transformation de l'énergie - coût des énergies - association de sources d'énergie - cheminement physique des flux de fluide dans une construction",
                                    u"Infrastructure et superstructure : - éléments de géologie, caractéristiques physiques et mécaniques des sols - éléments de structure porteuse - éléments d'enveloppe du bâtiment - cloisonnement",
                                    u"Aménagement du territoire : - typologies des ouvrages (ponts, routes, barrages, lieu de production d'énergie) - impact environnemental lié à l'aménagement de l'espace public",
                                    u"Aménagement urbain : - distribution des fluides, des énergies - collecte et traitement des effluents - aménagement des espaces communs - éclairage public"
                                    ]],
                                    
                          "2.2" : [u"Solutions technologiques",
                                   [u"Maîtrise des consommations d'énergie : -performances thermiques du bâti - gains passifs (enveloppe, écrans solaire, éclairage naturel). Maîtrise des pertes : - températures ambiantes de confort intermittence des consignes - gestion d'éclairage et d'écrans solaires - récupération d'énergie - pilotage d'énergie - pilotage global de l'énergie sur site",
                                    u"Assurer la stabilité : - charmente - porteurs verticaux et horizontaux - liaison au sol, stabilité des terres, drainage",
                                    u"Le confort : - thermique - acoustique - visuel - respiratoire"]],
                          "2.3" : [u"Modélisations, essais et simulations",
                                    [u"Etude des structures : - modélisation, degré d'hyperstaticité, typologie des charges, descente de charges, force portante du sol, sollicitations et déformations des structures - comportement élastique, élastoplastique - rupture fragile, ductilité - coefficients de sécurité - moment quadratique, principe de superposition, répartition des déformations dans une section de poutre soumise à de la flexion simple",
                                     u"Confort hygromthermique : - caractéristiques et comportements thermiques des matériaux et parois",
                                     u"Confort acoustique : - transmission du bruit au travers d'une paroi - les pièges à sons - loi de masse - phénomène de résonnance - temps de réverbération",
                                     u"Confort visuel : - éclairement, luminance, facteur de lumière du jour - stratégie de l'éclairement naturel",
                                     u"Confort respiratoire : - conditions d'hygiène, pollution - renouvellement d'air, VMC"
                                     ]],
                          }],
                          
                  "3" : [u"Vie de la construction",
                         {"3.1" : [u"Améliorer les performances de la construction",
                                   [u"Protection anti intrusion. Gestion des accès. Pilotage d'automatismes (volets, brise-soleil... Réseaux Voix, Données, Images. Centralisation des commandes. Instrumentation d'équipements (relevé et affichage de consommation, etc.). Pilotage à distance (téléphone, internet, etc.). Asservissement de systèmes (coupure du chauffage sur ouverture de fenêtre, etc.)",
                                   
                                    u"Gestion du réseau de transport. Comptage et facturation de l'énergie. Impact environnemental"]],
                          "3.2" : [u"Gestion de la vie d'une construction",
                                   [u"Cycle vie de l'ouvrage : - matériaux de la construction (extraction, transformation, mise en oeuvre) - énergie grise - procédés et matériels de déconstruction - législation en vigueur - traçabilité",
                                    u"- Planification de la déconstruction d'un ouvrage - typologie des déchets, valorisation, traitements",
                                    u"Inventorier la nature des pathologies : - histoire des matériaux de la construction, leur évolution dans le temps - nature et évolutions des sols",
                                    u"- Techniques de relevé des constructions (imagerie, topographie, métré, prélèvement d'échantillon)"]]
                                    }]}


dicCompetences =  {"O7" : [u"Imaginer une solution, répondre à un besoin",
                              {"CO7.ac1" : u"Participer à une étude architecturale, dans une démarche de développement durable",
                               "CO7.ac2" : u"Proposer/Choisir des solutions techniques répondant aux contraintes et attentes d'une construction",
                               "CO7.ac3" : u"Concevoir une organisation de réalisation"}],
                      "O8" : [u"Valider des solutions techniques",
                              {"CO8.ac1" : u"Simuler un comportement structurel, thermique et acoustique de tout ou partie d'une construction",
                               "CO8.ac2" : u"Analyser les résultats issus de simulations ou d'essais de laboratoire",
                               "CO8.ac3" : u"Analyser/Valider les choix structurels et de confort"}],
                      "O9" : [u"Gérer la vie d'un système",
                              {"CO9.ac1" : u"Améliorer les performances d'une construction du point de vue énergétique, domotique et informationnel",
                               "CO9.ac2" : u"Identifier et décrire les causes de désordre dans une construction",
                               "CO9.ac3" : u"Valoriser la fin de vie du produit : déconstruction, gestion des déchets, valorisation des produits"}]}


#################################################################################################################################
#
#        Les indicateurs de compétences
#                (True = revue ; False = soutenance)
#
#################################################################################################################################
dicIndicateurs_prj = {"CO7.ac1" : [[u"Le besoin relatif au projet est identifié", True],
                                       [u"Les fonctions principales du projet sont identifiées", True],
                                       [u"Les critères du CDC du projet sont décodés", True],
                                       [u"La démarche d'analyse du problème est mise en oeuvre", True],
                                       [u"Les principaux points de vigilance (économiques, développement durable, intégration en site) relatifs au projet sont identifiés", True]
                                        ],
                         "CO7.ac2" : [[u"Des pratiques de travail collaboratives sont mise en oeuvre", True],
                                       [u"Les moyens conventionnels de représentation des solutions sont correctement utilisés (croquis, schémas, ...)", True],
                                       [u"Les contraintes de normes, propriétés industrielle et brevet sont identifiées", True],
                                       [u"Les solutions techniques proposées sont pertinentes des points de vue développement durable et économique", True],
                                       [u"Les caractéristiques comportementales de la solution retenue répondent au CDC", True],
                                       [u"Les choix sont explicités dans une démarche d'analyse globale de réponse au CDC", True],
                                       [u"Une recherche systématique de produit innovant est effectuée", True]
                                        ],
                         "CO7.ac3" : [[u"Le phasage des opérations de réalisation est réaliste, le chemin critique est identifié", True],
                                       [u"Les procédés de mise en oeuvre sont choisis et justifiés", True],
                                       [u"La logistique de réalisation répond aux contraintes techniques et de site du chantier", True],
                                       [u"Les impacts environnementaux sont identifiés, des solutions de limitation sont proposées", True]
                                        ],
                         "CO8.ac1" : [[u"Les variables du modèle sont identifiées", True],
                                       [u"Leurs influences respectives sont identifiées", True],
                                       [u"Les scénarios de simulation sont appliqués", True],
                                       [u"Les conditions de l'essai sont identifiées et justifiées", True]
                                        ],
                         "CO8.ac2" : [[u"Les observations et mesures sont méthodiquement menées", True],
                                       [u"Les incertitudes sont estimées", True],
                                       [u"L'interprétation des résultats est cohérente", True],
                                       [u"Les résultats de la simulation et les mesures sont corrélés (validation des modèles)", True]
                                        ],
                         "CO8.ac3" : [[u"Une démarche d'analyse de la structure est mise en oeuvre", True],
                                       [u"Les écarts entre les performances attendues et celles consécutives aux choix effectués sont établis", True],
                                       [u"Les contraintes de normes, proporiétés industrielles et brevets sont identifiées", True],
                                       [u"Les impacts environnementaux sont identifiés, des solutions de limitation sont proposées", True]
                                        ],
                         "CO9.ac1" : [[u"Un bilan des performances de la construction existante est établi", True],
                                       [u"Les besoins de l'usager sont traduits en solutions technologiques", True],
                                       [u"Le contexte normatif est précisé", True],
                                       [u"Une réalisation permet de constater les améliorations attendues", True],
                                       [u"L'adaptabilité de la construction rénovée est prise en compte", True]
                                        ],
                         "CO9.ac2" : [[u"Une investigation est réalisée", True],
                                       [u"Les désordres et leurs causes sont identifiés", True],
                                       [u"Des solutions de remédiation sont envisagées", True]
                                        ],
                         "CO9.ac3" : [[u"Une analyse de cycle de vie de tout ou partie d'une construction est menée", True],
                                      [u"Les contraintes normatives (au sens du développement durable) sont répertoriées", True],
                                      [u"Une procédure de valorisation des produits est proposée", True]
                                      ]}



#################################################################################################################################
#
#        Les poids des indicateurs de compétences
#
#################################################################################################################################
dicPoidsIndicateurs_prj   = {"O7" : [20, 
                                        {"CO7.ac1" : [5,10,5,5,10],
                                         "CO7.ac2" : [5,5,5,5,10,5,4],
                                         "CO7.ac3" : [7,7,7,5]}],
                                "O8" : [40,
                                        {"CO8.ac1" : [10,10,10,5],
                                         "CO8.ac2" : [10,5,10,10],
                                         "CO8.ac3" : [10,10,5,5]}],
                                "O9" : [30,
                                        {"CO9.ac1" : [10,10,10,15,10],
                                         "CO9.ac2" : [5,10,5],
                                         "CO9.ac3" : [10,5,10]}]
                                }


#################################################################################################################################
#
#        Les constantes pour les grilles d'évaluation de projet
#
#################################################################################################################################
Fichier_GRILLE = ["Grille_evaluation_STI2D_AC_revues.xlsm", "Grille_evaluation_STI2D_AC_revues.xls"]

Cellules_NON =   {"CO7.ac1" : [(5,4), (6,4), (7,4), (8,4), (9,4)],
                     "CO7.ac2" : [(10,4), (11,4), (12,4), (13,4), (14,4), (15,4), (16,4)],
                     "CO7.ac3" : [(17,4), (18,4), (19,4), (20,4)],
                     "CO8.ac1" : [(22,4), (23,4), (24,4), (25,4)],
                     "CO8.ac2" : [(26,4), (27,4), (28,4), (29,4)],
                     "CO8.ac3" : [(30,4), (31,4), (32,4), (33,4)],
                     "CO9.ac1" : [(35,4), (36,4), (37,4), (38,4), (39,4)],
                     "CO9.ac2" : [(40,4), (41,4), (42,4)],
                     "CO9.ac3" : [(43,4), (44,4), (45,4)]}

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
