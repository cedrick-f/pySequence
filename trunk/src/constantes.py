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

# Les constantes par type d'enseignement
from constantes_ETT import *
from constantes_SIN import *
from constantes_AC import *
from constantes_ITEC import *
from constantes_EE import *
#from constantes_SSI import *

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
#   Quelques couleurs ...
#
####################################################################################
COUL_OK  = "GREEN3"
COUL_NON = "TOMATO1"
COUL_BIEN = "GOLD"
COUL_BOF = "ORANGE"

####################################################################################
#
#   Définition des images
#
####################################################################################
dicimages =   {"Seq" : images.Icone_sequence,
               "Cla" : images.Icone_classe,
               "Com" : images.Icone_competence,
               "Sav" : images.Icone_savoirs,
               "Obj" : images.Icone_objectif,
               "Ci"  : images.Icone_centreinteret,
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

imagesProjet = {"Prj" : images.Icone_projet,
                "Elv" : images.Icone_eleve,
                'Prf' : images.Icone_prof2,
                "Sup" : images.Icone_support,
                "Tac" : images.Icone_projet
                }

imagesTaches =  {'Ana' : images.Icone_CdCF, 
                 'Con' : images.Icone_conception, 
                 'DCo' : images.Icone_conception,
                 'Rea' : images.Icone_fabrication, 
                 'Val' : images.Icone_validation,
                 'Rev' : images.Icone_evaluation,
                 'R1'  : images.Icone_evaluation,
                 'R2'  : images.Icone_evaluation,
                 'S'  : images.Icone_evaluation}
                

imagesCI = [images.CI_1, images.CI_2, images.CI_3, images.CI_4,
            images.CI_5, images.CI_6, images.CI_7, images.CI_8,
            images.CI_9, images.CI_10, images.CI_11, images.CI_12,
            images.CI_13, images.CI_14, images.CI_15, images.CI_16]             


####################################################################################
#
#   Définition des compétences les projets
#
####################################################################################
def getCompetencesProjet(dic):
    """ Renvoie un dict des compétences à évaluer en projet :
        = certaines compétences de l'ET
        + les compétences de l'enseignement de spécialité
    """
    d = {"O1" : dicCompetencesET["O1"],
         "O2" : dicCompetencesET["O2"],
         "O6" : dicCompetencesET["O6"]
         }

    d.update(dic)
    
    d["O8"][1]["CO8.es"] = [u"Justifier des éléments d'une simulation relative au comportement de tout ou partie d'un système et les écarts par rapport au réel", 5, True]
    return d

dicCompetencesITEC_prj = getCompetencesProjet(dicCompetencesITEC)
dicCompetencesEE_prj = getCompetencesProjet(dicCompetencesEE)
dicCompetencesAC_prj = getCompetencesProjet(dicCompetencesAC)
dicCompetencesSIN_prj = getCompetencesProjet(dicCompetencesSIN)



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
Enseigmenent = {'ET'   : u"Enseignement Technologique Transversal",
                'ITEC' : u"Innovation Technologique et éco-conception",
                'AC'   : u"Architecture et Construction",
                'EE'   : u"Energies et Environnement",
                'SIN'  : u"Systèmes d'Information et Numérique"}


####################################################################################
#
#   Définition des options de la classe
#
####################################################################################
CentresInteretsET = None
PositionCibleCIET = None

Effectifs = {"C" : 32,
             "G" : None,
             "D" : None, 
             "E" : None, 
             "P" : None,
             }

NomsEffectifs= {"C" : [u"Classe entière",       u"Classe entière"],
                 "G" : [u"Effectif réduit",      u"Effectif réduit"],
                 "D" : [u"Demi-groupe",          u"Demi-groupe"],
                 "E" : [u"Etude et Projet",      u"Etude ou Projet"],
                 "P" : [u"Activité Pratique",    u"Act. Pra."],
                 }


# Tout ce qui concerne les effectifs
listeEffectifs = ["C", "G", "D" ,"E" ,"P"]

NbrGroupes = {"G" : 2, # Par classe
              "E" : 4, # Par grp Eff réduit
              "P" : 8, # Par grp Eff réduit
              }

CouleursGroupes = {"C" : (0.3,0.3,0.7),
                   "G" : (0.4,0.5,0.4),
                   "D" : (0.7,0.3,0.3),
                   "E" : (0.3,0.5,0.5), 
                   "P" : (0.5,0.3,0.5), 
                   }

def getTxtEffectifs():
    """ Pour les OPTIONS :
        Met les paramètres d'effectifs à la queue dans un string
    """
    return ""
    t = u""
    for i, eff in enumerate(listeEffectifs):
        t += str(Effectifs[eff]) +" "
    return t


def setValEffectifs(txt):
    """ Pour les OPTIONS :
        Récupère les paramètes d'effectifs à partir d'un string
    """
    return
    lst = txt.split()
    for i, eff in enumerate(listeEffectifs):
        Effectifs[eff] = eval(lst[i])



    
    
def strEffectif(classe, e, n = 0, eleve = True):
    if e == "C":
        return str(classe.effectifs[e])
    else:
        lsteff = classe.effectifs[e]
        if type(lsteff[0]) == list:
            lsteff = lsteff[0]
        if n == -1:
            mini, maxi = min(lsteff), max(lsteff)
            if mini != maxi:
                eff_str = str(mini) + "-" + str(maxi)
            else:
                eff_str = str(mini)
            eleves = u"élèves"
        else:
            eff_str = str(lsteff[n])
            if lsteff[n] == 1:
                eleves = u"élève"
            else:
                eleves = u"élèves"
        if eleve:
            return eff_str+" "+eleves
        else:
            return eff_str

def strEffectifComplet(classe, e, n = 0):
    tit_eff = NomsEffectifs[e][0]
    return tit_eff+" ("+strEffectif(classe, e, n)+")"


def partitionne(total, ngroupe):
    if type(total) != list:
        d, r = divmod(total, ngroupe)
        lst = [d] * ngroupe
        for i in range(r):
            lst[i] += 1
        return lst
    else:
        lst = []
        for tot in total:
            lst.append(partitionne(tot, ngroupe))
        return lst
        


def calculerEffectifs(classe):
    classe.effectifs['G'] = partitionne(classe.effectifs['C'], classe.nbrGroupes['G'])
    classe.effectifs['D'] = partitionne(classe.effectifs['G'], 2)
    classe.effectifs['E'] = partitionne(classe.effectifs['G'], classe.nbrGroupes['E'])
    classe.effectifs['P'] = partitionne(classe.effectifs['G'], classe.nbrGroupes['P'])
    

    
# Calcul inverse UNIQUEMENT POUR COMPATIBILITE !!
def revCalculerEffectifs(classe, effG, effE, effP):
    classe.nbrGroupes['G'] = classe.effectifs['C'] // effG
    classe.nbrGroupes['E'] = effG // effE
    classe.nbrGroupes['P'] = effG // effP
    calculerEffectifs(classe)
    

def findEffectif(lst, eff):
    continuer = True
    i = 0
    while continuer:
        if i > len(lst):
            continuer = False
        else:
            if lst[i][:2] == NomsEffectifs[eff][0][:2]:
                continuer = False
            else:
                i += 1 
    return i



#def DefOptionsDefaut():
#    global  CentresInteretsET, PositionCibleCIET
#    
#    #
#    # Options générales
#    #
#    
#    CentresInteretsET = [u"Développement durable et compétitivité des produits",
#                       u"Design, créativité et innovation",
#                       u"Caractéristiques des matériaux et structures",
#                       u"Solutions constructives des matériaux et des structures",
#                       u"Dimensionnement des structures et choix des matériaux",
#                       u"Efficacité énergétique liée au comportement des matériaux et des structures",
#                       u"Formes et caractéristiques de l'énergie",
#                       u"Organisation structurelle et solutions constructives des chaînes d'énergie",
#                       u"Amélioration de l'efficacité énergétique dans les chaînes d'énergie",
#                       u"Amélioration de la gestion de l'énergie",
#                       u"Formes et caractéristiques de l'information",
#                       u"Organisation structurelle et solutions constructives des chaînes d'information",
#                       u"Commande temporelle des systèmes",
#                       u"Informations liées au comportement des matériaux et des structures",
#                       u"Optimisation des paramètres par simulation globale"
#                       ]
#
#    PositionCibleCIET = ['   _   ',
#                         '   _   ',
#                         'M  _F  ',
#                         'M  _ S ',
#                         'M  _  C',
#                         'ME _ SC',
#                         ' E _F  ',
#                         ' E _ S ',
#                         ' E _  C',
#                         ' EI_ SC',
#                         '  I_F  ',
#                         '  I_ S ',
#                         '  I_  C',
#                         'M I_ SC',
#                         'MEI_   '
#                       ]
#
##    Effectifs["C"][1] = 32
##    Effectifs["G"][1] = 16
##    Effectifs["D"][1] = 8
##    Effectifs["E"][1] = 4
##    Effectifs["P"][1] = 2
#                 
#    
#DefOptionsDefaut()

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

dicCompetences_prj = {'ITEC'   : dicCompetencesITEC_prj, 
                      'AC'     : dicCompetencesAC_prj, 
                      'EE'     : dicCompetencesEE_prj, 
                      'SIN'    : dicCompetencesSIN_prj}


NRB_COEF_COMP_S = {'ITEC'   : 0, # Nombres de coef pour les compétences "Soutenance"
                   'AC'     : 0, 
                   'EE'     : 0, 
                   'SIN'    : 0}     


dicCompetences_prj_simple = {}
for k,v in dicCompetences_prj.items():
    NRB_COEF_COMP_R = 0     # Nombre de coef pour les compétences "Revue"
    dic = {}
    for d in v.values():

        dic.update(d[1])
        
        for l in d[1].values():
            if len(l) > 2:
                NRB_COEF_COMP_R += l[1]
            else:
                NRB_COEF_COMP_S[k] += l[1]
                
    dicCompetences_prj_simple[k] = dic


dicCompetences_prj_revues = {}
for k,v in dicCompetences_prj.items():
    dic = {}
#    print k
    for c, d in v.items():
#        print "   ", c,d
        ddic = {}
#        print dic
        for kk, vv in d[1].items():
#            print "      ", kk, vv
            if len(vv) > 2:
                ddic[kk] = d[1][kk]
        if ddic != {}:
            dic.update({c : [d[0], ddic]})
        
        
    dicCompetences_prj_revues[k] = dic
#print dicCompetences_prj_revues["ITEC"]

dicSavoirs = {'ET'     : dicSavoirsET,
              'ITEC'   : dicSavoirsITEC, 
              'AC'     : dicSavoirsAC, 
              'EE'     : dicSavoirsEE, 
              'SIN'    : dicSavoirsSIN}




def getListCI(txt):
    return txt.splitlines()

def getTextCI(lst):
    t = u""
    for i, ci in enumerate(lst):
        t += ci
        if i != len(lst)-1:
            t += "\n"
    return t



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
    
    
def getAllCodes(dic):
    lst = dic.keys()
    for k in dic.keys():
        if len(dic[k]) > 1 and type(dic[k][1]) == dict:
            lst.extend(getAllCodes(dic[k][1]))
    return lst





#ouvrirConfig()
#filterUnits="userSpaceOnUse"
FILTRE1 = """<filter id="f1"  x="-10%" y="-10%" width="200%" height="200%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="0.003" result="blur"/>
      <feOffset in="blur" dx="0.003" dy="0.003" result="offsetBlur"/>
      <feSpecularLighting in="blur" surfaceScale="5" specularConstant=".75" 
                          specularExponent="20" lighting-color="#bbbbbb"  
                          result="specOut">
        <fePointLight x="-5000" y="-10000" z="20000"/>
      </feSpecularLighting>
      <feComposite in="specOut" in2="SourceAlpha" operator="in" result="specOut"/>
      <feComposite in="SourceGraphic" in2="specOut" operator="arithmetic" 
                   k1="0" k2="1" k3="1" k4="0" result="litPaint"/>
      <feMerge>
        <feMergeNode in="offsetBlur"/>
        <feMergeNode in="litPaint"/>
      </feMerge>
    </filter>"""
    
FILTRE2 = """<filter id="f1" x="0" y="0" width="200%" height="200%">
              <feOffset result="offOut" in="SourceAlpha" dx="0.006" dy="0.006" />
              <feGaussianBlur result="blurOut" in="offOut" stdDeviation="0.003" />
              <feBlend in="SourceGraphic" in2="blurOut" mode="normal" />
                </filter>"""

FILTRE3 = """<filter id = "f1">
        <feGaussianBlur in = "SourceAlpha" stdDeviation = "0.02" result = "blur1"/>
        <feSpecularLighting result = "specOut" in = "blur1" specularConstant = "1.2" specularExponent = "12" lighting-color = "#bbbbbb">
            <feDistantLight azimuth = "45" elevation = "45"/>
        </feSpecularLighting>
        <feComposite in = "SourceGraphic" in2 = "specOut" operator = "arithmetic" k1 = "0" k2 = "1" k3 = "1" k4 = "0"/>
    </filter>
            """
            
FILTRE4 = """
<filter id='f1'  x='0' y='0' width='200%' height='200%'>      
    <feGaussianBlur id='fgb' in='SourceAlpha' stdDeviation='0.004' result='blur'/>      
    <feOffset id='fof' in='blur' dx='0.004' dy='0.004' result='offsetBlur'/>      
    <feSpecularLighting id='fsl' in='blur' surfaceScale='4' specularConstant='.75' specularExponent='32' lighting-color='gray' result='specOut'>        
        <fePointLight id='fpl' x='-5000' y='-10000' z='20000'/>      </feSpecularLighting>      
    <feComposite in='specOut' in2='SourceAlpha' operator='in' result='specOut'/>      
    <feComposite id='fco' in='SourceGraphic' in2='specOut' operator='arithmetic' k1='0' k2='1' k3='1' k4='0' result='litPaint'/>      
    <feMerge>        
        <feMergeNode in='offsetBlur'/>        
        <feMergeNode in='litPaint'/>      
    </feMerge>    
</filter>
"""

def getElementFiltre(filtre):
    from xml.dom.minidom import parseString
    doc = parseString(filtre)
    return doc.documentElement



#######################################################################################
#
#    Données pour la gestion des fichiers .seq et .prj
#
#######################################################################################
FORMAT_FICHIER = {'seq' : u"Séquence (.seq)|*.seq|",
                  'prj' : u"Projet (.prj)|*.prj|"}
TOUS_FICHIER = u"Tous les fichiers|*.*'"

MESSAGE_ENR = {'seq' : u"Enregistrer la séquence sous ...",
               'prj' : u"Enregistrer le projet sous ..."}
MESSAGE_DEJA = {'seq' : u"La séquence est déja ouverte.\nVoulez vous ignorer les changements et rouvrir la séquence ?",
                'prj' : u"Le projet est déja ouvert.\nVoulez vous ignorer les changements et rouvrir le projet ?"}
TITRE_DEFAUT = {'seq' : u"Nouvelle séquence",
                'prj' : u"Nouveau projet"}
MESSAGE_FERMER = {'seq' : u"La séquence a été modifiée.\nVoulez vous enregistrer les changements ?",
                  'prj' : u"Le projeta été modifié.\nVoulez vous enregistrer les changements ?"}



#######################################################################################
#
#    Données concernant les projets
#
#######################################################################################
#NOM_JALONS = {'S' : u"Soutenance finale"}


PHASE_TACHE = ['Ana', 'Con', 'DCo', 'Rea', 'Val', 'Rev']
NOM_PHASE_TACHE = {'Ana' : u"Spécification - Planification", 
                   'Con' : u"Conception préliminaire",
                   'DCo' : u"Conception détaillée",
                   'Rea' : u"Prototypage", 
                   'Val' : u"Qualification - Intégration - Validation",
                   'R1'  : u"Revue de projet n°1",
                   'R2'  : u"Revue de projet n°2",
                   'Rev' : u"Revue intermédiaire",
                   'S'   : u"Soutenance finale"}

CODE_PHASE_TACHE = {'Ana' : u"SP", 
                    'Con' : u"Cp",
                    'DCo' : u"Cd",
                    'Rea' : u"Pr", 
                    'Val' : u"QIV",
                    'R1'  : u"R1",
                    'R2'  : u"R2",
                    'Rev' : u"Ri",
                    'S'   : u"S"}


def getLstPhase():
    lst = []
    for k in PHASE_TACHE:
        if not k in ["R1", "R2", "S"]:
            lst.append(NOM_PHASE_TACHE[k])
    return lst


COUL_ELEVES = [((0.85,0.85,0.95,0.2), (0,0,0,1)),
               ((0.7,0.7,0.8,0.2), (0,0,0,1)),
               ((0.85,0.85,0.95,0.2), (0,0,0,1)),
               ((0.7,0.7,0.8,0.2), (0,0,0,1)),
               ((0.85,0.85,0.95,0.2), (0,0,0,1)),
               ((0.7,0.7,0.8,0.2), (0,0,0,1))]

DUREE_PRJ = 70
DELTA_DUREE = 5
DELTA_DUREE2 = 15



DISCIPLINES = ['Tec', 'Phy', 'Mat', 'LV1', 'Phi', 'Spo']
NOM_DISCIPLINES = {'Tec' : u"Technologie", 
                   'Phy' : u"Physique/Chimie", 
                   'Mat' : u"Mathématiques", 
                   'Phi' : u"Philosophie", 
                   'LV1' : u"Langue vivante",
                   'Spo' : u"Education physique",
                   'Aut' : u"Autre discipline"}

COUL_DISCIPLINES = {'Tec' : u"Technologie", 
                    'Phy' : u"Physique/Chimie", 
                    'Mat' : u"Mathématiques", 
                    'Phi' : u"Philosophie", 
                    'LV1' : u"Langue vivante",
                    'Spo' : u"Education physique",
                    'Aut' : u"Autre discipline"}


def getLstDisciplines():
    lst = []
    for k in DISCIPLINES:
        lst.append(NOM_DISCIPLINES[k])
    return lst


