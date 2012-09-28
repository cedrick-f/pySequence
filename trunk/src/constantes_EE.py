#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               constantes EE                             ##
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
#   Définition des constantes pour la spécialité EE
#
####################################################################################

CentresInterets_EE = [u"Typologie des sytèmes énergétiques",
                       u"Production d'énergie",
                       u"Transport, stockage et distribution de l'énergie et réseaux spécifiques",
                       u"Efficacité énergétique passive",
                       u"Efficacité énergétique active"
                       ]

dicCompetences_EE = {"O7" : [u"Imaginer une solution, répondre à un besoin",
                          {"CO7.ee1" : [u"Participer à une démarche de conception dans le but de proposer plusieurs solutions possibles à un problème technique identifié en lien avec un enjeu énergétique",7],
                           "CO7.ee2" : [u"Justifier une solution retenue en intégrant les conséquences des choix sur le triptyque Matériau - Energie - Information",6],
                           "CO7.ee3" : [u"Définir la structure, la constitution d'un système en fonction des caractéristiques technico-économiques et environnementales attendues",4],
                           "CO7.ee4" : [u"Définir les modifications de la structure, les choix de constituants et du type de système de gestion d'une chaîne d'énergie afin de répondre à une évolution d'un cahier des charges",4],}],
                  "O8" : [u"Valider des solutions techniques",
                          {"CO8.ee1" : [u"Renseigner un logiciel de simulation du comportement énergétique avec les caractéristiques du système et les paramètres externes pour un point de fonctionnement donné",3],
                           "CO8.ee2" : [u"Interpréter les résultats d'une simulation afin de valider une solution ou l'optimiser",4],
                           "CO8.ee3" : [u"Comparer et interpréter le résultat d'une simulation d'un comportement d'un système avec un comportement réel",3],
                           "CO8.ee4" : [u"Mettre en oeuvre un protocole d'essais et de mesures sur le prototype d'une chaîne d'énergie, interpréter les résultats",5],}],
                  "O9" : [u"Gérer la vie d'un système",
                          {"CO9.ee1" : [u"Expérimenter des procédés de stockage, de production, de transport, de transformation, d'énergie pour aider à la conception d'une chaîne d'énergie",3],
                           "CO9.ee2" : [u"Réaliser et valider un prototype obtenu en réponse à tout ou partie du cahier des charges initial",4],
                           "CO9.ee3" : [u"Intégrer un prototype dans un système à modifier pour valider son comportement et ses performances",4]}]}


dicSavoirs_EE = {"1" : [u"Projet technologique",
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
                          "1.2" : [u"Paramètres de la compétitivité",
                                   [u"Conformité à une norme. L'ergonomie : sécurité dans les relations homme - système, maintenabilité, fiabilité. Innovation technologique : intégration des fonctions et optimisation du fonctionnement, solutions intégrant des énergies renouvelables. Influence de la durée de vie des constituants"]
                                   ],
                          "1.3" : [u"Vérification des performances",          
                                    [u"Contraintes du cahier des charges : performances, qualité, sécurité, temps caractéristiques",
                                    u"Recette du prototype au regard des besoins formalisés dans le cahier des charges",
                                    u"Intégration des fonctions et optimisation du fonctionnement : approche pluritechnologique et transferts de technologie"]],
                          "1.4" : [u"Communication technique",
                                   [u"Compte rendu d'une activité de projet. Présentation d'une intention de conception ou d'une solution. Animation d'une revue de projet"]]
                         }],
                  "2" : [u"Conception d'un système",
                         {"2.1" : [u"Approche fonctionnelle d'une chaîne d'énergie",
                                   [u"Structure fonctionnelle d'une chaîne d'énergie, graphe de structure d'une chaîne d'énergie",
                                    u"Schéma de transfert d'énergie",
                                    u"Structures d'alimentation en énergie multi-transformateur"]],
                                    
                          "2.2" : [u"Approche fonctionnelle du système de gestion de la chaîne d'énergie",
                                   [u"Gestion de l'information dédiée aux applications énergétiques, caractéristiques des fonctions des systèmes",
                                    u"Fonctions de communication homme-système : types et caractéristiques",
                                    u"Autour d'un point de fonctionnement donné, systèmes asservis ou régulés : - représentation fonctionnelle (schéma blocs, chaîne d'action et de retour, correcteur - grandeur réglée, réglante et pertubatrice"]],
                          "2.3" : [u"Paramètres influant la conception",
                                    [u"Efficacité énergétique passive et active d'un système"]],
                          "2.4" : [u"Approche comportementale",
                                    {"2.4.1" : [u"Comportement énergétique des systèmes",
                                                [u"Comportement dynamique d'un mécanisme. Théorème de l'énergie cinétique. Inertie ramenée sur l'arbre primaire. Exploitation d'une maquette numérique et d'un résultat de simulation",
                                                 u"Comportement temporel des constituants d'une chaîne d'énergie, représentation. Caractéristiques et comportements thermique et acoustique des matériaux et parois d'un bâtiment",
                                                 u"Charge d'une chaîne d'énergie : définition, types de charges, caractérisation",
                                                 u"Optimisation des échanges d'énergie entre source et charge, amélioration de l'efficacité énergétique : disponibilité, puissance, reconfiguration, qualité, adaptabilité au profil de charge, inertie, régularité, modes de fonctionnement (marche, arrêt, intermittence)"]],
                                     "2.4.2" : [u"Gestion de l'énergie en temps réel",
                                                [u"Contrôle instantané du fonctionnement du système en vue d'un maintien au plus près d'un point de fonctionnement",
                                                 u"Diagramme états - transitions pour un système évènementiel"]],
                                     "2.4.3" : [u"Validation comportementale par simulation",
                                                [u"Loi de dcommande, paramètres du modèle de comportement, paramètres de l'environnement. Validation du comportement énergétique d'une structure par simulation. Validation du comportement du système de gestion d'une chaîne d'énergie par simulation"]]
                                     }],
                            "2.5" : [u"Critères de choix de solutions",
                                     [u"Constituants matériels et logiciels associés aux fonctions techniques assurées par la chaîne d'énergie et répondant aux performances attendues. Type de système de gestion de l'énergie. Interfaces entre le système de gestion de l'énergie et la chaîne d'énergie. Capteurs. Protections contre les surintensités et contre les surcharges. Conducteurs",
                                      u"Coût global d'un système : investissement initial, maintenance, entretien, adaptation à l'usage, consommation énergétique"]]
                          }],
                          
                  "3" : [u"Transports et distribution d'énergie, études de dossiers technologiques",
                         {"3.1" : [u"Production et transport d'énergie",
                                   [u"Types et caractéristiques des centrales électriques, hydrauliques, thermiques. Types de solutions de production d'énergies renouvelables, caractéristiques",
                                    u"Structure d'un réseau de transport et de distribution d'énergie électrique, caractéristiques et pertes",
                                    u"Distribution de l'énergie électrique",
                                    u"Structure d'un réseau de production, de transport et de distribution de fluides",
                                    u"Gestion du réseau de transport. Comptage et facturation de l'énergie. Impact environnemental"]]}],
                "4" : [u"Réalisation et qualification d'un prototype",
                       {"4.1" : [u"Réalisation d'un prototype",
                                 [u"Décodage de notices techniques et des procédures d'installation",
                                  u"Agencement, paramétrage et interconnexion de constituants de la chaîne d'énergie",
                                  u"Mise en oeuvre d'un système local de gestion de l'énergie",
                                  u"Mise en oeuvre d'un système de télégestion et de télésurveillance"]],
                        "4.2" : [u"Sécurité",
                                 ["Techniques liées à la sécurité : notion de redondance, auto-surveillance. Prévention des risques : prévention intrinsèque, protection, information"]],
                        "4.3" : [u"Essais et réglages en vue d'assurer le fonctionnement et d'améliorer les performances",
                                 [u"Protocole d'essais, essais et caractérisation des écarts par rapport au comportement attendu. Essais hors énergie, essais statiques en énergie, essais dynamiques. Démarche raisonnée d'identification des causes des écarts et de résolution des problèmes. Paramètres à ajuster pour un fonctionnement spécifié d'un système ou d'un constituant"]]
                        }]
                          
                  }

#################################################################################################################################
#
#        Les indicateurs de compétences
#                (True = revue ; False = soutenance)
#
#################################################################################################################################

dicIndicateurs_prj_EE = {"CO7.ee1" : [[u"Le besoin relatif au projet est identifié et justifié",True],
                                    [u"Les fonctions principales du projet sont identifiées",True],
                                    [u"Les critères du CDC du projet sont décodés",True],
                                    [u"Les contraintes de normes, propriété industrielle et brevets sont identifiées",True],
                                    [u"La démarche d'analyse du problème est pertinente",True],
                                    [u"Les principaux points de vigilance relatifs au projet sont identifiés",True],
                                    [u"Les grandes étapes d'une démarche de créativité sont franchies de manière cohérente",True]
                                    ],
                   "CO7.ee2" : [[u"Les solutions techniques proposées sont pertinentes",True],
                                    [u"Les caractéristiques comportementales de la solution retenue répondent au CDC",True],
                                    [u"Les choix sont explicités et la solution justifiée en intégrant les conséquences sur le tryptique (matériau - énergie - information)",True],
                                    [u"Les moyens conventionnels de représentation des solutions sont correctement utilisés (croquis, schémas, ...)",True],
                                    [u"Les moyens informatiques de représentation sont correctement utilisés",True],
                                    [u"La structure est correctement définie",True]
                                    ],
                     "CO7.ee3" : [[u"La solution choisie pour la gestion de l'énergie est adaptée à l'évolution du CDC",True],
                                    [u"Les modifications proposées répondent à l'évolution du CDC",True],
                                    [u"La procédure de modification est rationnelle",True],
                                    [u"Le choix des constituants et l'organisation de la chaîne d'énergie est pertinente",True]
                                    ],
                     "CO7.ee4" : [[u"Le type de système de gestion de l'énergie choisi est adapté à la demande",True],
                                    [u"Les modifications respectent les contraintes du CDC",True],
                                    [u"La procédure de modification est rationnelle",True],
                                    [u"Le choix des constituants est pertinent",True]
                                    ],
                     "CO8.ee1" : [[u"Les variables du modèle sont identifiées",True],
                                    [u"Leurs influences respectives sont identifiées",True],
                                    [u"Les paramètres saisis sont réalistes",True]
                                    ],
                     "CO8.ee2" : [[u"Les scénarios de simulation sont identifiés",True],
                                    [u"Les paramètres influents sont identifiés",True],
                                    [u"Les conséquences sur le mécanisme sont identifiées",True],
                                    [u"Les modifications proposées sont pertinentes",True]
                                    ],
                     "CO8.ee3" : [[u"Les résultats de la simulation et les mesures sont corrélés",True],
                                    [u"L'analyse des écarts est méthodique",True],
                                    [u"L'interprétation des résultats est cohérente",True]
                                    ],
                     "CO8.ee4" : [[u"Les conditions de l'essai sont identifiées et justifiées",True],
                                    [u"Le protocole est adapté à l'objectif",True],
                                    [u"Les observations et mesures sont méthodiquement menées",True],
                                    [u"Les incertitudes sont estimées",True],
                                    [u"L'interprétation des résultats est cohérente et pertinente",True]
                                    ],
                     "CO9.ee1" : [[u"Les paramètres significatifs à observer sont identifiés",True],
                                    [u"Le protocole est adapté à l'objectif",True],
                                    [u"Des caractéristiques pertinentes et leurs conséquences constructives sont identifiées",True]
                                    ],
                     "CO9.ee2" : [[u"Un type de prototype est choisi en regard de la partie de CDC à respecter",True],
                                    [u"La réalisation du prototype est conforme à une procédure valide",True]
                                    ]}

#################################################################################################################################
#
#        Les poids des indicateurs de compétences
#
#################################################################################################################################
dicPoidsIndicateurs_prj_EE =   {"O7" : [40, 
                                          {"CO7.ee1" : [4,4,5,4,5,4,4],
                                           "CO7.ee2" : [5,5,5,5,5,5],
                                           "CO7.ee3" : [5,5,5,5],
                                           "CO7.ee4" : [5,5,5,5]}],
                                  "O8" : [40, 
                                          {"CO8.ee1" : [7,6,7],
                                           "CO8.ee2" : [6,7,7,7],
                                           "CO8.ee3" : [6,6,7],
                                           "CO8.ee4" : [7,7,7,6,7]}],
                                  "O9" : [20,
                                          {"CO9.ee1" : [9,9,9],
                                           "CO9.ee2" : [9,9,9,9],
                                           "CO9.ee3" : [9,9,9,10]}]}

# Nombre indicateurs = 39