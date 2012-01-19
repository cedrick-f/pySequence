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

# Les icones des branches de l'abre et un curseur perso
import images

import ConfigParser


#
# Les deuxlignes suivantes permettent de lancer le script sequence.py depuis n'importe
# quel répertoire sans que l'utilisation de chemins
# relatifs ne soit perturbée
#
import sys, os
import _winreg

FILE_ENCODING = sys.getfilesystemencoding()

PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
#PATH = os.path.split(PATH)[0]
os.chdir(PATH)
sys.path.append(PATH)
print "Dossier de l'application :",PATH


# 
# On récupère là le dossier "Application data" 
# où devra être enregistré le fichier .cfg de pysylic
#

# On récupère le répertoire d'installation de pySyLiC
try:
    regkey = _winreg.OpenKey( _winreg.HKEY_CLASSES_ROOT, 'pySequence.sequence\\DefaultIcon',0, _winreg.KEY_READ)
    (value,keytype) = _winreg.QueryValueEx(regkey , '') 
    INSTALL_PATH = os.path.dirname(value.encode(FILE_ENCODING))
except:
    INSTALL_PATH = '' # Pas installé sur cet ordi
    
print "Dossier d'installation :", INSTALL_PATH
PORTABLE = not(os.path.abspath(INSTALL_PATH) == os.path.abspath(PATH))


if not PORTABLE: # Ce n'est pas une version portable qui tourne
    # On lit la clef de registre indiquant le type d'installation
    try: # Machine 32 bits
        regkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\pySequence', 0, _winreg.KEY_READ )
    except: # Machine 64 bits
        try :
            regkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Wow6432Node\\pySequence', 0, _winreg.KEY_READ )
        except:
            PORTABLE = True # en fait, pySequence n'est pas installé !!!
    
if not PORTABLE:
    try:
        (value,keytype) = _winreg.QueryValueEx(regkey, 'DataFolder' ) 
        APP_DATA_PATH = value
    except:
        import wx
        dlg = wx.MessageDialog(None, u"L'installation de pySequence est incorrecte !\nVeuillez désinstaller pySequence puis le réinstaller." ,
                               u"Installation incorrecte",
                               wx.OK | wx.ICON_WARNING
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()
        APP_DATA_PATH = PATH
        
    if not os.path.exists(APP_DATA_PATH):
        os.mkdir(APP_DATA_PATH)    
        
else: # C'est une version portable qui tourne
    APP_DATA_PATH = PATH
    print "Version portable !!"
        
print "Dossier pour les données :", APP_DATA_PATH
    
    
####################################################################################
#
#  Gestion des erreurs
#
####################################################################################    
ERROR_FILE = os.path.join(APP_DATA_PATH, 'pySequence.exe' + '.log')
print "Fichier erreur :",ERROR_FILE

import traceback

def _exceptionhook(typ, value, traceb):
    """ On catch une exception """
    frame=traceb.tb_frame
    print >>sys.stderr,"\n"
    traceback.print_tb(traceb)
    print >>sys.stderr,"\nType : ",typ,"\n"
    print >>sys.stderr,"ValueError : ",value
    sys.exit()

class RedirectErr:
    #
    # Redirige la sortie des erreurs pour envoyer l'erreur par mail
    #
    def __init__(self,stderr):
        self.stderr=stderr
        self.content=""
        self.error_occured=False
        self.file_error=None

    def write(self,text):
        #
        # A la premiere erreur, on enregistrer la fonction de sortie
        #
        if not self.error_occured:
            #
            # Première erreur
            # on ouvre le fichier qui contient les erreurs
            self.file_error=open(ERROR_FILE,'w')
            self.error_occured=True
        if self.file_error is not None:
            self.file_error.write(text)
            self.file_error.flush()

if not PORTABLE:
    sys.excepthook = _exceptionhook
    sys.stderr=RedirectErr(sys.stderr)


####################################################################################
#
#   Définition des images
#
####################################################################################
dicimages = {"Seq" : images.Icone_sequence,
               "Com" : images.Icone_competence,
               "Sav" : images.Icone_savoirs,
               "Obj" : images.Icone_objectif,
               "Ci" : images.Icone_centreinteret,
               "Sys" : images.Icone_systeme,

                       }
imagesSeance = {"R" : images.Icone_rotation,
                "S" : images.Icone_parallele,
                "E" : images.Icone_evaluation,
                "C" : images.Icone_cours,
                "ED" : images.Icone_ED,
                "AP" : images.Icone_AP,
                
                "P"  : images.Icone_projet,
                "SA" : images.Icone_synthese_Act,
                "SS" : images.Icone_synthese_Seq}



####################################################################################
#
#   Définition des constantes pour l'enseignement transversal
#
####################################################################################
dicCompetencesET = {"O1" : [u"Caractériser des systèmes privilégiant un usage raisonné du point de vue développement durable",
                          {"CO1.1" : [u"Justifier les choix des matériaux, des structures d'un système et les énergies mises en oeuvre dans une approche de développement durable",],
                           "CO1.2" : [u"Justifier le choix d'une solution selon des contraintes d'ergonomie et d'effets sur la santé de l'homme et du vivant",]}],
                  "O2" : [u"Identifier les éléments permettant la limitation de l’Impact environnemental d’un système et de ses constituants",
                          {"CO2.1" : [u"Identifier les flux et la forme de l'énergie, caractériser ses transformations et/ou modulations et estimer l'efficacité énergétique globale d'un système"],
                           "CO2.2" : [u"Justifier les solutions constructives d'un système au regard des impacts environnementaux et économiques engendrés tout au long de son cycle de vie"],}],
                  "O3" : [u"Identifier les éléments influents du développement d’un système",
                          {"CO3.1" : [u"Décoder le cahier des charges fonctionnel d'un système"],
                           "CO3.2" : [u"Evaluer la compétitivité d'un système d'un point de vue technique et économique"],}],
                  "O4" : [u"Décoder l’organisation fonctionnelle, structurelle et logicielle d’un système",
                          {"CO4.1" : [u"Identifier et caractériser les fonctions et les constituants d'un système ainsi que ses entrées/sorties"],
                           "CO4.2" : [u"Identifier et caractériser l'agencement  matériel et/ou logiciel d'un système"],
                           "CO4.3" : [u"Identifier et caractériser le fonctionnement temporel d'un système"],
                           "CO4.4" : [u"Identifier et caractériser des solutions techniques relatives aux matériaux, à la structure, à l'énergie et aux informations (acquisition, traitement, transmission) d'un système"]}],
                  "O5" : [u"Utiliser un modèle de comportement pour prédire un fonctionnement ou valider une performance",
                          {"CO5.1" : [u"Expliquer des éléments d'une modélisation proposée relative au comportement de tout ou partie d'un système"],
                           "CO5.2" : [u"Identifier des variables internes et externes utiles à une modélisation, simuler et valider le comportement du modèle"],
                           "CO5.3" : [u"Evaluer un écart entre le comportement du réel et le comportement du modèle en fonction des paramètres proposés"]}],
                  "O6" : [u"Communiquer une idée, un principe ou une solution technique, un projet, y compris en langue étrangère",
                          {"CO6.1" : [u"Décrire une idée, un principe, une solution, un projet en utilisant des outils de représentation adaptés"],
                           "CO6.2" : [u"Décrire le fonctionnement et/ou l'exploitation d'un système en utilisant l'outil de description le plus pertinent"],
                           "CO6.3" : [u"Présenter et argumenter des démarches, des résultats, y compris dans une langue étrangère",]}]}





dicSavoirsET = {"1" : [u"Principes de conception des systèmes de développement durable",
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



                         


####################################################################################
#
#   Définition des constantes pour la spécialité ITEC
#
####################################################################################

CentresInteretsITEC = [u"Besoin et performance d'un système",
                       u"Compétitivité, design et ergonomie des systèmes",
                       u"Eco-conception des mécanismes",
                       u"Structure, matériaux et protections d'un système",
                       u"Transmission de mouvement et de puissance d'un système",
                       u"Procédés de réalisation"
                       ]

dicCompetencesITEC = {"O7" : [u"Imaginer une solution, répondre à un besoin",
                          {"CO7.itec1" : [u"Identifier et justifier un problème technique à partir de l'analyse globale d'un système (approche Matière - Energie - Information)"],
                           "CO7.itec2" : [u"Proposer des solutions à un problème technique identifié en participant à des démarches de créativité, choisir et justifier la solution retenue"],
                           "CO7.itec3" : [u"Définir, à l'aide d'un modeleur numérique, les formes et dimensions d'une pièce d'un mécanisme à partir des contraintes fonctionnelles, de son principe de réalisation et de son matériau"],
                           "CO7.itec4" : [u"Définir, à l'aide d'un modeleur numérique, les modifications d'un mécanisme à partir des contraintes fonctionnelles"],}],
                  "O8" : [u"Valider des solutions techniques",
                          {"CO8.itec1" : [u"Paramétrer un logiciel de simulation mécanique pour obtenir les caractéristiques d'une loi d'entrée/sortie d'un mécanisme simple"],
                           "CO8.itec2" : [u"Interpréter les résultats d'une simulation mécanique pour valider une solution ou modifier une pièce ou un mécanisme"],
                           "CO8.itec3" : [u"Mettre en oeuvre un protocole d'essais et de mesures, interpréter les résultats"],
                           "CO8.itec4" : [u"Comparer et interpréter le résultat d'une simulation d'un comportement mécanique avec un comportement réel"],}],
                  "O9" : [u"Gérer la vie du produit",
                          {"CO9.itec1" : [u"Expérimenter des procédés pour caractériser les paramètres de transformation de la matière et leurs conséquences sur la définition et l'obtention de pièces"],
                           "CO9.itec2" : [u"Réaliser et valider un prototype obtenu par rapport à tout ou partie du cahier des charges initial"],
                           "CO9.itec3" : [u"Intégrer les pièces prototypes dans le système à modifier pour valider son comportement et ses performances",]}]}


dicSavoirsITEC = {"1" : [u"Projet technologique",
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

####################################################################################
#
#   Définition des constantes pour la spécialité EE
#
####################################################################################

CentresInteretsEE = [u"Typologie des sytèmes énergétiques",
                       u"Production d'énergie",
                       u"Transport, stockage et distribution de l'énergie et réseaux spécifiques",
                       u"Efficacité énergétique passive",
                       u"Efficacité énergétique passive"
                       ]

dicCompetencesEE = {"O7" : [u"Imaginer une solution, répondre à un besoin",
                          {"CO7.ee1" : [u"Participer à une démarche de conception dans le but de proposer plusieurs solutions possibles à un problème technique identifié en lien avec un enjeu énergétique"],
                           "CO7.ee2" : [u"Justifier une solution retenue en intégrant les conséquences des choix sur le triptyque Matériau - Energie - Information"],
                           "CO7.ee3" : [u"Définir la structure, la constitution d'un système en fonction des caractéristiques technico-économiques et environnementales attendues"],
                           "CO7.ee4" : [u"Définir les modifications de la structure, les choix de constituants et du type de système de gestion d'une chaîne d'énergie afin de répondre à une évolution d'un cahier des charges"],}],
                  "O8" : [u"Valider des solutions techniques",
                          {"CO8.ee1" : [u"Renseigner un logiciel de simulation du comportement énergétique avec les caractéristiques du système et les paramètres externes pour un point de fonctionnement donné"],
                           "CO8.ee2" : [u"Interpréter les résultats d'une simulation afin de valider une solution ou l'optimiser"],
                           "CO8.ee3" : [u"Comparer et interpréter le résultat d'une simulation d'un comportement d'un système avec un comportement réel"],
                           "CO8.ee4" : [u"Mettre en oeuvre un protocole d'essais et de mesures sur le prototype d'une chaîne d'énergie, interpréter les résultats"],}],
                  "O9" : [u"Gérer la vie d'un système",
                          {"CO9.ee1" : [u"Expérimenter des procédés de stockage, de production, de transport, de transformation, d'énergie pour aider à la conception d'une chaîne d'énergie"],
                           "CO9.ee2" : [u"Réaliser et valider un prototype obtenu en réponse à tout ou partie du cahier des charges initial"],
                           "CO9.ee3" : [u"Intégrer un prototype dans un système à modifier pour valider son comportement et ses performances",]}]}


dicSavoirsEE = {"1" : [u"Projet technologique",
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
                                                [u"Loi de dcommande, paramètres du modèle de comportement, paramètres de l'environnement. Validation du comportement énergétique d'une structure par simulation. Validation du comportement du système de gestion d'une chaîne d'énergie par simulation"]],
                            "2.5" : [u"Critères de choix de solutions",
                                     [u"Constituants matériels et logiciels associés aux fonctions techniques assurées par la chaîne d'énergie et répondant aux performances attendues. Type de système de gestion de l'énergie. Interfaces entre le système de gestion de l'énergie et la chaîne d'énergie. Capteurs. Protections contre les surintensités et contre les surcharges. Conducteurs",
                                      u"Coût global d'un système : investissement initial, maintenance, entretien, adaptation à l'usage, consommation énergétique"]]
                          }],
                          
                  "3" : [u"Transports et distribution d'énergie, études de dossiers technologiques",
                         {"3.1" : [u"Produstion et transport d'énergie",
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
                                 [u"Protocole d'essais, essais et caractérisation des écarts par rapport au comportement attendu. Essais hors énergie, essais statiques en énergie, essais dynamiques. Démarche raisonnée d'identification des causes des écarts et de résolution des problèmes. Paramètres à ajuster pour un fonctionnement spécifié d'un système ou d'un constituant"]]}]
                          }]
                  }

####################################################################################
#
#   Définition des constantes pour la spécialité AC
#
####################################################################################

CentresInteretsAC = [u"Participation à une étude architecturale",
                       u"Vérification de la résistance",
                       u"Protection",
                       u"Le confort",
                       u"Organisation de réalisation",
                       u"Vie en oeuvre",
                       u"Reconditionnement de l'ouvrage",
                       u"Valorisation de la fin de vie de l'ouvrage"
                       ]

dicCompetencesAC = {"O7" : [u"Imaginer une solution, répondre à un besoin",
                          {"CO7.ac1" : [u"PArticiper à une étude architecturale, dans une démarche de développement durable"],
                           "CO7.ac2" : [u"Proposer/Choisir des solutions techniques répondant aux contraintes et attentes d'une construction"],
                           "CO7.ac3" : [u"Concevoir une organisation de réalisation"],}],
                  "O8" : [u"Valider des solutions techniques",
                          {"CO8.ac1" : [u"Simuler un comportement structurel, thermique et acoustique de tout ou partie d'une construction"],
                           "CO8.ac2" : [u"Analyser les résultats issus de simulations ou d'essais de laboratoire"],
                           "CO8.ac3" : [u"Analyser/Valider les choix structurels et de confort"],}],
                  "O9" : [u"Gérer la vie d'un système",
                          {"CO9.ac1" : [u"Améliorer les performances d'une construction du point de vue énergétique, domotique et informationnel"],
                           "CO9.ac2" : [u"Identifier et décrire les causes de désordre dans une construction"],
                           "CO9.ac3" : [u"Valoriser la fin de vie du produit : déconstruction, gestion des déchets, valorisation des produits",]}]}


dicSavoirsAC = {"1" : [u"Projet technologique",
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

####################################################################################
#
#   Définition des constantes pour la spécialité SIN
#
####################################################################################

CentresInteretsSIN = [u"Configuration et performances du traitement de l'information",
                       u"Instrumentation/Acquisition et restitution de grandeurs physiques",
                       u"Communication de l'information/Au sein d'un système",
                       u"Gestion de l'information/Structures matérielles et logicielles associées au traitement de l'information",
                       u"Communication entre systèmes",
                       u"Traitement analogique de l'information",
                       u"Cycle de vie d'un produit"
                       ]

dicCompetencesSIN = {"O7" : [u"Imaginer une solution, répondre à un besoin",
                          {"CO7.sin1" : [u"Décoder la notice technique d'un système, vérifier la conformité du fonctionnement"],
                           "CO7.sin2" : [u"Décoder le cahier des charges fonctionnel décrivant le besoin exprimé, identifier la fonction définie par un besoin exprimé, faire des mesures pour caractériser cette fonction et conclure sur sa conformité"],
                           "CO7.sin3" : [u"Exprimer le principe de fonctionnement d'un système à partir des diagrammes SysML pertinents. Repérer les constituants de la chaîne d'énergie et d'information"],}],
                  "O8" : [u"Valider des solutions techniques",
                          {"CO8.sin1" : [u"Rechercher et choisir une solution logicielle ou matérielle au regard de la définition d'un système"],
                           "CO8.sin2" : [u"Etablir pour une fonction précédemment identifiée, un modèle de comportement à partir de mesures faites sur le sytème"],
                           "CO8.sin3" : [u"Traduire sous forme graphique l'architecture de la chaîne d'information identifiée pour un système et définir les paramètres d'utilisation du simulateur"],
                           "CO8.sin4" : [u"Identifier les variables simulées et mesurées sur un système pour valider le choix d'une solution"],}],
                  "O9" : [u"Gérer la vie d'un système",
                          {"CO9.sin1" : [u"Utiliser les outils adaptés pour planifier un projet (diagramme de Gantt, chemin critique, données économiques, réunions de projet)"],
                           "CO9.sin2" : [u"Installer, configurer et instrumenter un système réel. Mettre en oeuvre la chaîne d'acquisition puis acquérir, traiter, transmettre et restituer l'information"],
                           "CO9.sin3" : [u"Rechercher des évolutions de constituants dans le cadre d'une démarche de veille technologique, analyser la structure d'un système pour intervenir sur les constituants dans le cadre d'une opération de maintenance"],
                           "CO9.sin4" : [u"Rechercher et choisir de nouveaux constituants d'un système (ou d'un projet finalisé) au regard d'évolutions technologiques, socioéconomiques spécifiées dans un cahier des charges. Organiser le projet permettant de maquettiser la solution choisie",]}]}

dicSavoirsSIN = {"1" : [u"Projet technologique",
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
                  


####################################################################################
#
#   Les constantes valables pour tous les enseignements
#
####################################################################################
TypesActivite = {"ED" : u"Activité d'étude de dossier",
                 "AP" : u"Activité pratique",
                 "P"  : u"Activité de projet",
                }

TypesSeance = {"C"  : u"Cours",
               "SA" : u"Synthèse d'activité",
               "SS" : u"Synthèse de séquence",
               "E"  : u"Evaluation",
               }
TypesSeance.update(TypesActivite)
TypesSeance.update({"R" : u"Rotation d'activités",
                    "S" : u"Activités en parallèle"})

TypesSeanceCourt = {"ED" : u"Etude de dossier",
                    "AP" : u"Activité pratique",
                    "P"  : u"Projet",
                    "C"  : u"Cours",
                    "SA" : u"Synt. d'activité",
                    "SS" : u"Synt. de séquence",
                    "E"  : u"Evaluation",
                    "R"  : u"Rotation",
                    "S"  : u"Parallèle"}

listeTypeSeance = ["ED", "AP", "P", "C", "SA", "SS", "E", "R", "S"]
listeTypeActivite = ["ED", "AP", "P"]



Demarches = {"I" : u"Investigation",
             "R" : u"Résolution de problème",
             "P" : u"Projet"}

DemarchesCourt = {"I" : u"Investigation",
             "R" : u"Rés. de problème",
             "P" : u"Projet"}

listeDemarches = ["I", "R", "P"]
listEnseigmenent = ['ET', 'ITEC', 'AC', 'EE', 'SIN']
listeEffectifs = ["C", "G", "D" ,"E" ,"P"]

####################################################################################
#
#   Définition des options de la classe
#
####################################################################################
CentresInteretsET = None
Effectifs = {"C" : [u"Classe entière",      32, u"Classe entière"],
             "G" : [u"Effectif réduit",     16, u"Effectif réduit"],
             "D" : [u"Demi-groupe",         8,  u"Demi-groupe"],
             "E" : [u"Etude et Projet",     4,  u"Etude ou Projet"],
             "P" : [u"Activité Pratique",   2,  u"Act. Pra."],
             }

def DefOptionsDefaut():
    global  CentresInteretsET
    
    #
    # Options générales
    #
    
    CentresInteretsET = [u"Développement durable et compétitivité des produits",
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

    
    Effectifs["C"][1] = 32
    Effectifs["G"][1] = 16
    Effectifs["D"][1] = 8
    Effectifs["E"][1] = 4
    Effectifs["P"][1] = 2
                 
    
DefOptionsDefaut()

####################################################################################
#
#   Les constantes par Enseignement
#
####################################################################################
CentresInterets = {'ET'     : CentresInteretsET,
                   'ITEC'   : CentresInteretsITEC, 
                   'AC'     : CentresInteretsAC, 
                   'EE'     : CentresInteretsEE, 
                   'SIN'    : CentresInteretsSIN}

dicCompetences = {'ET'     : dicCompetencesET,
                  'ITEC'   : dicCompetencesITEC, 
                  'AC'     : dicCompetencesAC, 
                  'EE'     : dicCompetencesEE, 
                  'SIN'    : dicCompetencesSIN}

dicSavoirs = {'ET'     : dicSavoirsET,
              'ITEC'   : dicSavoirsITEC, 
              'AC'     : dicSavoirsAC, 
              'EE'     : dicSavoirsEE, 
              'SIN'    : dicSavoirsSIN}

def getListCI(txt):
    return txt.splitlines()

def getTextCI(lst):
    t = u""
#    print lst
    for i, ci in enumerate(lst):
#        print i, ci
        t += ci
        if i != len(lst)-1:
            t += "\n"
    return t

def getTxtEffectifs():
    t = u""
    for i, eff in enumerate(listeEffectifs):
        t += str(Effectifs[eff][1]) +" "
    return t


    
def setValEffectifs(txt):
    lst = txt.split()
    for i, eff in enumerate(listeEffectifs):
        Effectifs[eff][1] = eval(lst[i])
#    print Effectifs

def setEffectifs(txt, effectifs):
    lst = txt.split()
    for i, eff in enumerate(listeEffectifs):
        effectifs[eff][1] = eval(lst[i])
    
    
def strEffectif(e):
    eff = Effectifs[e]
    if eff[1] == 1:
        eleves = u"élève"
    else:
        eleves = u"élèves"
    return eff[0]+" ("+str(eff[1])+" "+eleves+")"

def findEffectif(lst, eff):
#    print "findEffectif", lst, eff
    continuer = True
    i = 0
    while continuer:
        if i > len(lst):
            continuer = False
        else:
            if lst[i][:2] == Effectifs[eff][0][:2]:
                continuer = False
            else:
                i += 1 
    return i


#def ouvrirConfig():
#    print "ouvrirConfig"
#    global CentresInterets
#    
#    config = ConfigParser.ConfigParser()
#    config.read(os.path.join(PATH,'configuration.cfg'))
#    
#    section = "Centres d'interet"
#    l = [""] * len(config.options(section))
#    for o in config.options(section):
#        l[eval(o)-1] = unicode(config.get(section,o), 'cp1252')
#    CentresInterets = l
#        
#    section = "Effectifs classe"
#    for k in Effectifs.keys():
#        Effectifs[k][1] = config.getint(section,k)

def getSavoir(seq, code, dic = None, c = None):
    if dic == None:
        dic = dicSavoirs[seq.classe.typeEnseignement]
    if c == None:
        c = len(code.split("."))
    if dic.has_key(code):
        return dic[code][0]
    else:
        cd = code[:-2*(c-1)]
        return getSavoir(seq, code, dic[cd][1], c-1)
    
    
    
def getCompetence(seq, code, dic = None, c = None):
#    print "getCompetence", code, dic, c
    if dic == None:
        dic = dicCompetences[seq.classe.typeEnseignement]
    if c == None:
        c = len(code.split("."))
    if dic.has_key(code):
        return dic[code][0]
    else:
#        cd = code[1:-2*(c-1)]
        cd = code.split(".")[0][1:]
        return getCompetence(seq, code, dic[cd][1], c-1)
    
    

#ouvrirConfig()

