#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               constantes ETT                            ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2013 Cédrick FAURY - Jean-Claude FRICOU

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
#   Définition des constantes pour l'enseignement transversal
#
####################################################################################
Enseigmenent = [u"STI2D-ETT", u"STI2D : Enseignement Technologique Transversal"]

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


PositionCibleCI = ['   _   ',
                     '   _   ',
                     'M  _F  ',
                     'M  _ S ',
                     'M  _  C',
                     'ME _ SC',
                     ' E _F  ',
                     ' E _ S ',
                     ' E _  C',
                     ' EI_ SC',
                     '  I_F  ',
                     '  I_ S ',
                     '  I_  C',
                     'M I_ SC',
                     'MEI_   '
                   ]





dicSavoirs = {"1" : [u"Principes de conception des systèmes de développement durable",
                  {"1.1" : [u"Compétitivité et créativité",
                            {"1.1.1" : [u"Paramètres de la compétitivité ",
                                        [u"Importance du service rendu (besoin réel et besoin induit)",
                                         u"Innovation (de produit, de procédé, de marketing)",
                                         u"Recherche de solutions techniques (brevets) et créativité, stratégie de propriété industrielle (protection du nom, du design et de l’aspect technique), enjeux de la normalisation",
                                         u"Design produit et architecture",
                                         u"Ergonomie : notion de confort, d’efficacité, de  sécurité dans les relations homme – produit, homme – système"]],
                             "1.1.2" : [u"Cycle de vie d'un produit et choix techniques, économiques et environnementaux",
                                        [u"Les étapes du cycle de vie d’un système",
                                         u"Prise en compte globale du cycle de vie"]],
                             "1.1.3" : [u"Compromis complexité – efficacité – coût",
                                        [u"Relation Fonction/Coût/Besoin",
                                         u"Relation Fonction/Coût/Réalisation",
                                         u"Relation Fonction/Impact environnemental"]]}],
                   "1.2" : [u"Éco conception",
                            {"1.2.1" : [u"Étapes de la démarche de conception",
                                        [u"Expression du besoin",
                                         u"Spécifications fonctionnelles d’un système (cahier des charges fonctionnel)"]],
                             "1.2.2" : [u"Mise à disposition des ressources",
                                        [u"Coûts relatifs, disponibilité, impacts environnementaux des matériaux",
                                         u"Enjeux énergétiques mondiaux : extraction et transport, production centralisée, production locale"]],
                             "1.2.3" : [u"Utilisation raisonnée des ressources",
                                        [u"Propriétés physico-chimiques, mécaniques et thermiques des matériaux",
                                         u"Impacts environnementaux associés au cycle de vie du produit",
                                         u"Efficacité énergétique d’un système",
                                         u"Apport de la chaîne d’information associée à la commande pour améliorer l’efficacité globale d’un système"]]}]}
                  ],
           "2" : [u"Outils et méthodes d’analyse et de description des systèmes",
                  {"2.1" : [u"Approche fonctionnelle des systèmes",
                            {"2.1.1" : [u"Organisation fonctionnelle d’une chaîne d'énergie",
                                        [u"Caractérisation des fonctions relatives à l’énergie : production, transport, distribution, stockage, transformation, modulation.",]],
                             "2.1.2" : [u"Organisation fonctionnelle d’une chaîne d’information",
                                        [u"Caractérisation des fonctions relatives à l'information : acquisition et restitution, codage et traitement, transmission",]]}],
                   "2.2" : [u"Outils de représentation",
                            {"2.2.1" : [u"Représentation du réel",
                                        [u"Croquis (design produit, architecture)",
                                         u"Représentation volumique numérique des systèmes",
                                         u"Exploitation des représentations numériques"]],
                             "2.2.2" : [u"Représentation du symboliques",
                                        [u"Représentation symbolique associée à la modélisation des systèmes : diagrammes adaptés SysML, graphe de flux d’énergie, schéma cinématique, schéma électrique, schéma fluidique.",
                                         u"Schéma architectural (mécanique, énergétique, informationnel)",
                                         u"Représentations des répartitions et de l’évolution des grandeurs énergétiques (diagramme, vidéo, image)",
                                         u"Représentations associées au codage de l’information : variables, encapsulation des données"]]}],
                   "2.3" : [u"Approche comportementale",
                            {"2.3.1" : [u"Modèles de comportement",
                                        [u"Principes généraux d’utilisation",
                                         u"Identification et limites des modèles de comportements,  paramétrage associé aux progiciels de simulation",
                                         u"Identification des variables du modèle, simulation et comparaison des résultats obtenus au système réel ou à son cahier des charges"]],
                             "2.3.2" : [u"Comportement des matériaux",
                                        [u"Matériaux composites, nano matériaux. Classification et typologie des matériaux",
                                         u"Comportements caractéristiques des matériaux selon les points de vue",
                                         u"Mécaniques (efforts, frottements, élasticité, dureté, ductilité)",
                                         u"Thermiques (échauffement par conduction, convection et rayonnement, fusion, écoulement)",
                                         u"Ėlectrique (résistivité, perméabilité, permittivité)"]],
                             "2.3.3" : [u"Comportement mécaniques des systèmes",
                                        [u"Équilibre des solides : modélisation des liaisons, actions mécaniques, principe fondamental de la statique, résolution d’un problème de statique plane",
                                         u"Résistance des matériaux : hypothèses et modèle poutre, types de sollicitations simples, notion de contrainte et de déformation, loi de Hooke et module d’Young, limite élastique, étude d’une sollicitation simple"]],
                             "2.3.4" : [u"Structures porteuses",
                                        [u"Aspects vibratoires",
                                         u"Transfert de charges"]],
                             "2.3.5" : [u"Comportement énergétique des systèmes",
                                        [u"Analyse des pertes de charges fluidiques, caractéristiques des composants",
                                         u"Les paramètres de gestion de l’énergie liés au stockage et aux transformations",
                                         u"Conservation d’énergie, pertes et rendements, principe de réversibilité",
                                         u"Natures et caractéristiques des sources et des charges",
                                         u"Caractérisation des échanges d’énergie entre source et charge : disponibilité, puissance, reconfiguration, qualité, adaptabilité au profil de charge, régularité"]],
                             "2.3.6" : [u"Comportements informationnels des systèmes",
                                        [u"Caractérisation de l’information : expression, visualisation, interprétation, caractérisations temporelle et fréquentielle",
                                         u"Modèles de description en statique et en dynamique",
                                         u"Modèles algorithmiques : structures algorithmiques élémentaires (boucles, conditions, transitions conditionnelles). Variables"]]}]}
                  ], 
           "3" : [u"Solutions technologiques",
                  {"3.1" : [u"Structures matérielles et/ou logicielles",
                            {"3.1.1" : [u"Choix des matériaux",
                                        [u"Principes de choix, indices de performances, méthodes structurées d’optimisation d’un choix, conception multi contraintes et multi objectifs",]],
                             "3.1.2" : [u"Typologie des solutions constructives des liaisons entre solides",
                                        [u"Caractérisation des liaisons sur les systèmes",
                                         u"Relation avec les mouvements / déformations et les efforts"]],
                             "3.1.3" : [u"Typologie des solutions constructives de l’énergie",
                                        [u"Système énergétique mono source",
                                         u"Système énergétique multi source et  hybride"]],
                             "3.1.4" : [u"Traitement de l’information",
                                        [u"Codage (binaire, hexadécimal, ASCII) et transcodage de l’information, compression, correction",
                                         u"Programmation objet : structures élémentaires de classe, concept d'instanciation",
                                         u"Traitement programmé : structure à base de microcontrôleurs et structures spécialisées (composants analogiques et/ou numériques programmables)",
                                         u"Systèmes événementiels : logique combinatoire, logique séquentielle",
                                         u"Traitement analogique de l’information : opérations élémentaires (addition, soustraction, multiplication, saturation)"]]}],
                   "3.2" : [u"Constituants d’un système",
                            {"3.2.1" : [u"Transformateurs et Modulateurs d’énergie associés",
                                        [u"Adaptateurs d’énergie : réducteurs mécaniques, transformateurs électriques parfaits et échangeurs thermiques",
                                         u"Actionneurs et modulateurs : moteurs électriques et modulateurs, vérins pneumatiques et interfaces, vannes pilotées dans l’habitat pour des applications hydrauliques et thermiques",
                                         u"Accouplements permanents ou non, freins",
                                         u"Convertisseurs d'énergie : ventilateurs, pompes, compresseurs, moteur thermique",
                                         u"Éclairage"]],
                             "3.2.2" : [u"Stockage d’énergie",
                                        [u"Constituants permettant le stockage sous forme :\n" \
                                         u"- mécanique, hydraulique ou pneumatique : sous forme potentielle et/ou cinétique\n" \
                                         u"- chimique : piles et accumulateurs, combustibles, carburants, comburants\n" \
                                         u"- électrostatique : condensateur et super condensateur\n" \
                                         u"- électromagnétique\n" \
                                         u"- thermique : chaleur latente et chaleur sensible",]],
                             "3.2.3" : [u"Acquisition et codage de l’information",
                                        [u"Capteurs : approche qualitative des capteurs, grandeur mesurée et grandeurs d’influence (parasitage, sensibilité, linéarité)",
                                         u"Conditionnement et adaptation du capteur à la chaîne d’information, échantillonnage, blocage",
                                         u"Filtrage de l’information : types de filtres (approche par gabarit)",
                                         u"Restitution de l’information : approche qualitative des démodulations (transducteurs Voix, Données, Images ; commande des  pré-actionneurs)"]],
                             "3.2.4" : [u"Transmission de l’information, réseaux et internet",
                                        [u"Transmission de l’information (modulations d’amplitude, modulations de fréquence, modulations de phase)",
                                         u"Caractéristiques d’un canal de transmission, multiplexage",
                                         u"Organisations matérielle et logicielle d’un dispositif communicant : constituants et interfaçages",
                                         u"Modèles en couche des réseaux, protocoles et encapsulation des données",
                                         u"Adresse physique (MAC) du protocole Ethernet et adresse logique (IP) du protocole IP. Lien adresse MAC/IP : protocole ARP",
                                         u"Architecture client/serveur : protocoles FTP et HTTP",
                                         u"Gestion d'un nœud de réseau par le paramétrage d'un routeur : adresses IP, NAT/PAT, DNS, pare-feu"]]}]}
                  ],}




dicCompetences =  {"O1" : [u"Caractériser des systèmes privilégiant un usage raisonné du point de vue développement durable",
                              {"CO1.1" : u"Justifier les choix des matériaux, des structures d'un système et les énergies mises en oeuvre dans une approche de développement durable",
                               "CO1.2" : u"Justifier le choix d'une solution selon des contraintes d'ergonomie et d'effets sur la santé de l'homme et du vivant"}],
                      "O2" : [u"Identifier les éléments permettant la limitation de l’Impact environnemental d’un système et de ses constituants",
                              {"CO2.1" : u"Identifier les flux et la forme de l'énergie, caractériser ses transformations et/ou modulations et estimer l'efficacité énergétique globale d'un système",
                               "CO2.2" : u"Justifier les solutions constructives d'un système au regard des impacts environnementaux et économiques engendrés tout au long de son cycle de vie"}],
                      "O3" : [u"Identifier les éléments influents du développement d’un système",
                              {"CO3.1" : u"Décoder le cahier des charges fonctionnel d'un système",
                               "CO3.2" : u"Evaluer la compétitivité d'un système d'un point de vue technique et économique"}],
                      "O4" : [u"Décoder l’organisation fonctionnelle, structurelle et logicielle d’un système",
                              {"CO4.1" : u"Identifier et caractériser les fonctions et les constituants d'un système ainsi que ses entrées/sorties",
                               "CO4.2" : u"Identifier et caractériser l'agencement  matériel et/ou logiciel d'un système",
                               "CO4.3" : u"Identifier et caractériser le fonctionnement temporel d'un système",
                               "CO4.4" : u"Identifier et caractériser des solutions techniques relatives aux matériaux, à la structure, à l'énergie et aux informations (acquisition, traitement, transmission) d'un système"}],
                      "O5" : [u"Utiliser un modèle de comportement pour prédire un fonctionnement ou valider une performance",
                              {"CO5.1" : u"Expliquer des éléments d'une modélisation proposée relative au comportement de tout ou partie d'un système",
                               "CO5.2" : u"Identifier des variables internes et externes utiles à une modélisation, simuler et valider le comportement du modèle",
                               "CO5.3" : u"Evaluer un écart entre le comportement du réel et le comportement du modèle en fonction des paramètres proposés"}],
                      "O6" : [u"Communiquer une idée, un principe ou une solution technique, un projet, y compris en langue étrangère",
                              {"CO6.1" : u"Décrire une idée, un principe, une solution, un projet en utilisant des outils de représentation adaptés",
                               "CO6.2" : u"Décrire le fonctionnement et/ou l'exploitation d'un système en utilisant l'outil de description le plus pertinent",
                               "CO6.3" : u"Présenter et argumenter des démarches, des résultats, y compris dans une langue étrangère"}]}


#################################################################################################################################
#
#        Les indicateurs de compétences
#                (True = revue ; False = soutenance)
#
#################################################################################################################################
dicIndicateurs_prj = {"CO1.1" : [[u"La justification des propriétés physico-chimiques, mécaniques ou thermiques des matériaux est claire et concise", False],
                                    [u"Les coûts relatifs, la disponibilité et les impacts environnementaux des matériaux sont évoqués", False],
                                    [u"La relation entre la morphologie des structures et les moyens de réalisation est explicitée de manière claire et concise", False],
                                    [u"La morphologie des structures est justifiée par l'usage et le comportement mécanique", False],
                                    [u"Le choix des énergies mises en oeuvre est justifié, l'efficacité énergétique est évoqué", False]
                                   ],
                         "CO1.2" : [[u"La justification des paramètres de confort et la réponse apportée par le système est abordée", False],
                                    [u"Les contraintes de sécurité sont signalés", False],
                                    [u"La prévention des conséquences prévisibles sur la santé est expliquée", False]
                                   ],
                         "CO2.1" : [[u"Les flux d'énergie sont décrits", False],
                                    [u"La forme de l'énergie est précisée", False],
                                    [u"Les caractéristiques des transformations ou modulations sont précisées", False],
                                    [u"La quantification de l'efficacité énergétique globale est précisée", False]
                                   ],
                         "CO2.2" : [[u"Les solutions constructives sont identifiées", False],
                                    [u"Le cycle de vie du système et de ses composants est identifié", False],
                                    [u"La relation fonction/Impact environnemental est précisée aux étapes essentielles", False],
                                    [u"La relation Fonction/Coût/Besoin est justifiée", False],
                                    [u"Le compromis technico-économique est justifié", False]
                                   ],
                         "CO6.1" : [[u"L'(les) outil(s) de représentation est (sont) correctement utilisé(s) pour la description", False],
                                    [u"Les outils de représentation sont correctement décodés", False],
                                    [u"La description est compréhensible", False]
                                   ],
                         "CO6.2" : [[u"L'(les) outil(s) de description utilisé(s) est (sont) adapté(s) au propos", False],
                                    [u"L'(les) outil(s) de description est (sont) correctement utilisé(s)", False],
                                    [u"La description du fonctionnement est concise et correcte", False]
                                   ],
                         "CO6.3" : [[u"La présentation est claire et concise", False],
                                    [u"La démarche est argumentée", False],
                                    [u"Les résultats sont présentés et commentés de manière claire et concise", False],
                                    [u"L'expression est claire et rigoureuse", False],
                                    [u"Le vocabulaire nécessaire est maîtrisé", False]
                                   ],
                         "CO8.0" : [[u"Les paramètres du modèle sont justifiés", False],
                                     [u"Leurs influences respectives sont explicitées", False],
                                     [u"La limite d'utilisation du modèle est justifiée", False],
                                     [u"Les variables mesurées sont pertinentes", False],
                                     [u"Les écarts sont expliqués de manière cohérente pour valider une solution technique", False]
                                    ]
                     }

#################################################################################################################################
#
#        Les poids des indicateurs de compétences
#
#################################################################################################################################
dicPoidsIndicateurs_prj = {"O1" : [20,
                                     {"CO1.1" : [20,10,10,15,20], 
                                      "CO1.2" : [5,15,5]}],
                              "O2" : [15,
                                      {"CO2.1" : [10,10,10,10],
                                       "CO2.2" : [15,15,10,10,10]}],
                              "O6" : [45,
                                      {"CO6.1" : [8,8,10],
                                       "CO6.2" : [8,8,10],
                                       "CO6.3" : [8,10,10,10,10]}],
                              "O8s" : [20,
                                       {"CO8.0" : [20,15,15,20,30]}]
                              }

#################################################################################################################################
#
#        Les constantes pour les grilles d'évaluation de projet
#
#################################################################################################################################
Fichier_GRILLE = ["Grille_evaluation_STI2D_soutenance.xlsm", "Grille_evaluation_STI2D_soutenance.xls"]

Cellules_NON =  {"CO1.1"  : [(5,4), (6,4), (7,4), (8,4), (9,4)],
                     "CO1.2"  : [(10,4), (11,4), (12,4)],
                     "CO2.1"  : [(14,4), (15,4), (16,4), (17,4)],
                     "CO2.2"  : [(18,4), (19,4), (20,4), (21,4), (22,4)],
                     "CO6.1"  : [(24,4), (25,4), (26,4)],
                     "CO6.2"  : [(27,4), (28,4), (29,4)],
                     "CO6.3"  : [(30,4), (31,4), (32,4), (33,4), (34,4)],
                     "CO8.0" : [(36,4), (37,4), (38,4), (39,4), (40,4)]
                     }

#################################################################################################################################
#
#        Les cellules "Savoirs" dans le tableau de bilan
#
#################################################################################################################################
fichierProgressionProgramme = u"ETT_Synthese.xlsx"
dicCellSavoirs = {"1.1.1" : [8,12],
                  "1.1.2" : [13,14],
                  "1.1.3" : [15,17],
                 
                  "1.2.1" : [18,18],
                  "1.2.2" : [19,20],
                  "1.2.3" : [21,24],
                  
                  "2.1.1" : [26,26],
                  "2.1.2" : [27,27],
                  
                  "2.2.1" : [28,30],
                  "2.2.2" : [31,34],
                  
                  "2.3.1" : [35,37],
                  "2.3.2" : [38,42],
                  "2.3.3" : [43,44],
                  "2.3.4" : [45,46],
                  "2.3.5" : [47,51],
                  "2.3.6" : [52,54],
                  
                  "3.1.1" : [56,56],
                  "3.1.2" : [57,58],
                  "3.1.3" : [59,60],
                  "3.1.4" : [61,65],
                  
                  "3.2.1" : [66,70],
                  "3.2.2" : [71,71],
                  "3.2.3" : [72,75],
                  "3.2.4" : [76,82]
                                
                 }

################################################################
#
#
#             Changement de grille 2014
#
################################################################
#
#             Les indicateurs
#
#####################################
#dicIndicateurs_prj = {"CO1.1" : [[u"Le choix des matériaux et/ou des matériels est justifié, des critères d'éco conception sont pris en compte", False],
#                                    [u"La structure matérielle et/ou informationnelle est correctement justifiée", False]                                 
#                                   ],
#                         "CO1.2" : [[u"La justification des paramètres de confort et/ou la réponse apportée par le système aux contraintes de préservation de la santé et du respect de la sécurité sont explicitées", False]
#                                   ],
#                         "CO2.1" : [[u"Les flux et la forme de l'énergie et/ou de l'information sont décrits de façon qualitative", False],
#                                    [u"Les caractéristiques d'entrées sorties des transformations ou modulations sont correctement précisées", False],
#                                    [u"L'analyse globale d'une chaine (énergie, action, information) est correctement réalisée", False]
#                                   ],
#                         "CO2.2" : [[u"La relation entre une fonction, des solutions et leur impact environnemental ou sociétal est précisée ", False],
#                                    [u"Le compromis technico économique et/ou la prise en compte des normes et réglementations est expliqué ", False]
#                                   ],
#                         "CO6.1" : [[u"La description du principe ou de la solution est synthétique et correcte", False]
#                                   ],
#                         "CO6.2" : [[u"La description du fonctionnement ou de l'exploitation du système est synthétique et correcte", False]
#                                   ],
#                         "CO6.3" : [[u"Le choix de la démarche retenue est argumentée", False],
#                                    [u"Les résultats sont présentés et commentés de manière claire et concise", False]
#                                   ],
#                         "CO8.0" : [[u"Les solutions techniques envisagées sont correctement analysées au regard des résultats d'expérimentations et/ou de tests et/ou de simulations", False],
#                                     [u"L'origine des écarts entre les résultats obtenus et les exigences du cahier des charges est correctement identifiée", False]
#                                    ]
#                     }
#
#################################################
#################################################################################################################################
#
#        Les poids des indicateurs de compétences
#
#################################################################################################################################
#dicPoidsIndicateurs_prj = {"O1" : [20,
#                                     {"CO1.1" : [35,35], 
#                                      "CO1.2" : [30]}],
#                              "O2" : [15,
#                                      {"CO2.1" : [20,20,20],
#                                       "CO2.2" : [20,20]}],
#                              "O6" : [45,
#                                      {"CO6.1" : [25],
#                                       "CO6.2" : [25],
#                                       "CO6.3" : [25,25]}],
#                              "O8s" : [20,
#                                       {"CO8.0" : [60,40]}]
#                              }
#
#
#################################################################################################################################
#
#        Les constantes pour les grilles d'évaluation de projet 
#
#            PLUS NECESSAIRE LA COLONNE NON N'EXISTE PLUS
#
#################################################################################################################################
#Fichier_GRILLE = ["Grille_soutenance_STI2D_2014.xlsm", "Grille_soutenance_STI2D_2014.xlsx"]
#
#Cellules_NON =  {"CO1.1"  : [(5,4), (6,4), (7,4), (8,4), (9,4)],
#                     "CO1.2"  : [(10,4), (11,4), (12,4)],
#                     "CO2.1"  : [(14,4), (15,4), (16,4), (17,4)],
#                     "CO2.2"  : [(18,4), (19,4), (20,4), (21,4), (22,4)],
#                     "CO6.1"  : [(24,4), (25,4), (26,4)],
#                     "CO6.2"  : [(27,4), (28,4), (29,4)],
#                     "CO6.3"  : [(30,4), (31,4), (32,4), (33,4), (34,4)],
#                     "CO8.0" : [(36,4), (37,4), (38,4), (39,4), (40,4)]
#                     }
#
##############################################################################
