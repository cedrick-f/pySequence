#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               Constantes                                ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2011-2013 Cédrick FAURY - Jean-Claude FRICOU

#    pySequence is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
    
#    pySequence is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pySequence; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


'''
Created on 26 oct. 2011

@author: Cedrick
'''
import wx

# Les icones des branches de l'abre et un curseur perso
import images

import time

import sys





#print sys.argv
#PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
##PATH = os.path.split(PATH)[0]
#os.chdir(PATH)
#sys.path.append(PATH)
#print u"Dossier de l'application :",PATH
#
#
## 
## On récupère là le dossier "Application data" 
## où devra être enregistré le fichier .cfg de pySequence
##
#
## On récupère le répertoire d'installation de pySequence
#try:
#    import _winreg
#    regkey = _winreg.OpenKey( _winreg.HKEY_CLASSES_ROOT, 'pySequence.sequence\\DefaultIcon',0, _winreg.KEY_READ)
#    (value,keytype) = _winreg.QueryValueEx(regkey , '') 
#    INSTALL_PATH = os.path.dirname(value.encode(FILE_ENCODING))
#except:
#    INSTALL_PATH = '' # Pas installé sur cet ordi
#    
#
#PORTABLE = not(os.path.abspath(INSTALL_PATH) == os.path.abspath(PATH))


#TABLE_PATH = os.path.join(os.path.abspath(os.path.join(PATH, os.pardir)), r'tables')
##print u"Dossier des tableaux Excel :", TABLE_PATH
#
#BO_PATH = os.path.join(os.path.abspath(os.path.join(PATH, os.pardir)), r'BO')
#
#if not PORTABLE: # Ce n'est pas une version portable qui tourne
#    # On lit la clef de registre indiquant le type d'installation
#    try: # Machine 32 bits
#        regkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\pySequence', 0, _winreg.KEY_READ )
#    except: # Machine 64 bits
#        try :
#            regkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Wow6432Node\\pySequence', 0, _winreg.KEY_READ )
#        except:
#            PORTABLE = True # en fait, pySequence n'est pas installé !!!
#    
#if not PORTABLE:
#    try:
#        (value,keytype) = _winreg.QueryValueEx(regkey, 'DataFolder' ) 
#        APP_DATA_PATH = value
#    except:
#        dlg = wx.MessageDialog(None, u"L'installation de pySequence est incorrecte !\nVeuillez désinstaller pySequence puis le réinstaller." ,
#                               u"Installation incorrecte",
#                               wx.OK | wx.ICON_WARNING
#                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
#                               )
#        dlg.ShowModal()
#        dlg.Destroy()
#        APP_DATA_PATH = PATH
#        
#    if not os.path.exists(APP_DATA_PATH):
#        os.mkdir(APP_DATA_PATH)    
#    print "Dossier d'installation :", INSTALL_PATH
#    
#else: # C'est une version portable qui tourne
#    APP_DATA_PATH = PATH
#    print "Version portable !!"
#        
#print u"Dossier pour les données :", APP_DATA_PATH



    
####################################################################################
#
#  Gestion des erreurs
#
####################################################################################    

#import traceback
#
#def _exceptionhook(typ, value, traceb):
#    """ On catch une exception """
#    frame=traceb.tb_frame
#    print >>sys.stderr,"\n"
#    traceback.print_tb(traceb)
#    print >>sys.stderr,"\nType : ",typ,"\n"
#    print >>sys.stderr,"ValueError : ",value
#    sys.exit()
#
#class RedirectErr:
#    #
#    # Redirige la sortie des erreurs pour envoyer l'erreur par mail
#    #
#    def __init__(self,stderr):
#        self.stderr=stderr
#        self.content=""
#        self.error_occured=False
#        self.file_error=None
#
#    def write(self,text):
#        #
#        # A la premiere erreur, on enregistrer la fonction de sortie
#        #
#        if not self.error_occured:
#            #
#            # Première erreur
#            # on ouvre le fichier qui contient les erreurs
#            self.file_error=open(ERROR_FILE,'w')
#            self.error_occured=True
#        if self.file_error is not None:
#            self.file_error.write(text)
#            self.file_error.flush()
#
#if not PORTABLE:
#    ERROR_FILE = os.path.join(APP_DATA_PATH, 'pySequence.exe' + '.log')
#    print "Fichier erreur :",ERROR_FILE
#    sys.excepthook = _exceptionhook
#    sys.stderr=RedirectErr(sys.stderr)

####################################################################################
#
#   Quelques constantes liées aux projets
#
####################################################################################
_R1 = 'R1'
_R2 = 'R2'
_R3 = 'R3'
_Rev = 'Rev'
_S = 'S'
TOUTES_REVUES = [_R1, _R2, _R3, _Rev]
TOUTES_REVUES_EVAL = [_R1, _R2, _R3]
TOUTES_REVUES_SOUT = [_R1, _R2, _R3, _Rev, _S]
TOUTES_REVUES_EVAL_SOUT = [_R1, _R2, _R3, _S]
DUREE_REVUES = 0.25 # Durée "factice" : uniquement pour que CalcH renvoie 0

####################################################################################
#
#   Gestion des erreurs ...
#
####################################################################################
#class Erreur():
#    def __init__(self, code, message):
#        self.code = code
#        self.message = message
    
ERR_PRJ_EQUIPE = 1
ERR_PRJ_SUPPORT = 2
ERR_PRJ_ELEVES = 4
ERR_PRJ_TACHES = 8
ERR_PRJ_T_VERSION = 16
ERR_PRJ_T_TYPENS = 32
ERR_PRJ_C_TYPENS = 64 # Code du référentiel non trouvé

ERR_INCONNUE = 65536

ERREURS = {ERR_PRJ_EQUIPE :     u"Equipe pédagogique",
           ERR_PRJ_SUPPORT :    u"Support",
           ERR_PRJ_ELEVES :     u"Eleve",
           ERR_PRJ_TACHES :     u"Tâche : %s",
           ERR_PRJ_T_VERSION :  u"Problème de version",
           ERR_PRJ_T_TYPENS :   u"Type d'enseignement incompatible",
           ERR_PRJ_C_TYPENS :   u"Référentiel %s non trouvé !",
           ERR_INCONNUE     :   u"?? Erreur inconnue !"
           }


#############################################################################################################
class Erreur():
    def __init__(self, num = 0, info = None):
        self.num = num
        self.info = info
    
    def getOkErr(self):
        if self.num == 0:
            return u"Ok"
        else:
            return u"Erreur"


    def getMessage(self):
        print self.info, ERREURS[self.num]
        if self.info != None:
            return ERREURS[self.num] %self.info
        else:
            return ERREURS[self.num]
        
MOIS = [u'Janvier', u'Février', u'Mars', u'Avril', u'Mai', u'Juin', 
        u'Juillet', u'Août', u'Septembre', u'Octobre', u'Novembre', u'Décembre']
JOURS = [u'Lundi', u'Mardi', u'Mercredi', u'Jeudi', u'Vendredi', u'Samedi', u'Dimanche']

####################################################################################
#
#   Quelques fonctions ...
#
####################################################################################
   
def getAnneeScolaire():
    """ Renvoie la première année de l'année scolaire en cours
    """
    date = time.localtime()
    if date.tm_mon >= 9:
        annee = date.tm_year
    else:
        annee = date.tm_year-1
    return annee

def getAnneeScolaireStr():
    annee = getAnneeScolaire()
    return str(annee)+"-"+str(annee+1)
    
def getSingulierPluriel(txt, pluriel = False):
    if pluriel:
        return txt.replace("(", "").replace(")", "")
    else:
        return txt.replace("(s)", "").replace("(x)", "")

    
    
#    
# Fonction pour indenter les XML générés par ElementTree
#
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            
            
def ellipsizer(txt, lg):
    t = txt[:lg]
    if len(t) < len(txt):
        t += u"..."
    return t

def lettreCol(num):
    return chr(65+num)

######################################################################################  
def supprime_accent(ligne):
    """ supprime les accents du texte source """
    accents = { u'a': [u'à', u'ã', u'á', u'â'],
                u'e': [u'é', u'è', u'ê', u'ë'],
                u'i': [u'î', u'ï'],
                u'u': [u'ù', u'ü', u'û'],
                u'o': [u'ô', u'ö'] }
    for (char, accented_chars) in accents.iteritems():
        for accented_char in accented_chars:
            ligne = ligne.replace(accented_char, char)
    return ligne

####################################################################################
#
#   Quelques caractères spéciaux ...
#
####################################################################################
CHAR_POINT = u"\u25CF" 
CHAR_FLECHE = u"\u2192" 

####################################################################################
#
#   Quelques couleurs ...
#
####################################################################################
COUL_OK  = "LIMEGREEN"
COUL_NON = "TOMATO1"
COUL_BIEN = "GOLD"
COUL_BOF = "ORANGE"
COUL_PARTIE = {'C' : "DEEPPINK2",
               'S' : "BLUEVIOLET",
               ''  : "FIREBRICK"}

def getCoulPartie(partie):
    if partie in COUL_PARTIE.keys():
        return COUL_PARTIE[partie]
    else:
        return COUL_PARTIE['']
#COUL_REVUE = "DEEPPINK2"#"FIREBRICK"
#COUL_SOUT = "BLUEVIOLET"#"MEDIUMBLUE"
COUL_ABS = "GREY"#"MEDIUMBLUE"
COUL_COMPETENCES = (0.6, 0.0, 0.0, 1.0)




####################################################################################
#
#   Définition des images
#
####################################################################################
dicimages =   {"Seq" : images.Icone_sequence,
               "Prj" : images.Icone_projet,
               "Cla" : images.Icone_classe,
               "Com" : images.Icone_competence,
               "Sav" : images.Icone_savoirs,
               "Obj" : images.Icone_objectif,
               "Ci"  : images.Icone_centreinteret,
               "Sys" : images.Icone_systeme,
               "Sea" : images.Icone_seance,

                       }
imagesSeance = {"R" : images.Icone_rotation,
                "S" : images.Icone_parallele,
                "E" : images.Icone_evaluation,
                "C" : images.Icone_cours,
                "ED" : images.Icone_ED,
                "AP" : images.Icone_AP,
                "TD" : images.Icone_TD,
                "P"  : images.Icone_projet,
                "SA" : images.Icone_synthese_Act,
                "SS" : images.Icone_synthese_Seq,
                "HC": images.Icone_maison,
                "ST" : images.Icone_usine,
                'Prf' : images.Icone_prof2}

imagesProjet = {"Prj" : images.Icone_projet,
                "Elv" : images.Icone_eleve,
                'Prf' : images.Icone_prof2,
                "Sup" : images.Icone_support,
                "Tac" : images.Icone_projet
                }

imagesProgression = {"Prg" : images.Icone_progression,
                    "Elv" : images.Icone_eleve,
                    'Prf' : images.Icone_prof2,
                    'Cal' : images.Icone_calendrier,
                    "Seq" : images.Icone_sequence,
                    "Prj" : images.Icone_projet,
                    }

imagesTaches =  {'Sup' : images.Icone_CdCF, 
                 'Ana' : images.Icone_CdCF, 
                 'Con' : images.Icone_conception, 
                 'DCo' : images.Icone_conception,
                 'Rea' : images.Icone_fabrication, 
                 'Val' : images.Icone_validation,
                 'XXX' : images.Icone_preparation,
                 'Rev' : images.Icone_evaluation,
                 'R1'  : images.Icone_revue,
                 'R2'  : images.Icone_revue,
                 'R3'  : images.Icone_revue,
                 'S'  : images.Icone_soutenance}
                

imagesCI = [images.CI_1, images.CI_2, images.CI_3, images.CI_4,
            images.CI_5, images.CI_6, images.CI_7, images.CI_8,
            images.CI_9, images.CI_10, images.CI_11, images.CI_12,
            images.CI_13, images.CI_14, images.CI_15, images.CI_16]             

# Avatar
TAILLE_AVATAR = ()
def ReSize_avatar(img):
    w, h = img.GetSize()
    wf, hf = 200.0, 100.0
    r = max(w/wf, h/hf)
    _w, _h = w/r, h/r
    return img.ConvertToImage().Scale(_w, _h).ConvertToBitmap()

AVATAR_DEFAUT = ReSize_avatar(images.avatar.GetBitmap())            
            
####################################################################################
#
#   Les constantes valables pour tous les enseignements
#
####################################################################################
TYPE_ENSEIGNEMENT_DEFAUT = "SSI"

# Le fichier contenant les CI STI2D ETT par académie
FICHIER_CI_STI2D_ETT = "CI_STI2D_ETT.xml"


####################################################################################
#
#   Définition des options de la classe
#
####################################################################################

Effectifs = {"C" : 36,
             "G" : None,
             "D" : None, 
             "E" : None, 
             "P" : None,
             }



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

   
    
def strEffectif(classe, e, n = 0, eleve = True):
    if e == "C":
        return str(classe.effectifs[e])
    else:
        if e in classe.effectifs:
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
        else:
            return u""

def strEffectifComplet(classe, e, n = 0):
    tit_eff = classe.GetReferentiel().effectifs[e][0]
    num_eff = strEffectif(classe, e, n)
    if num_eff != u"":
        return tit_eff+" ("+num_eff+")"
    else:
        return tit_eff


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
    





######################################################################################
#
#   Quelques fonctions partagées
# 
######################################################################################

# pour convertir "liste d'indicateurs selectionnés" <--> "texte pour engegistrement"
def toList(txt):
    lst = txt.split()
    l = []
    for i in lst:
        l.append(eval(i))
    return l

def toTxt(lst):
    t = ''
    for i in lst:
        t += str(i) + ' '
    return t

#############################################################################################################
def mergeDict(D, d):
    for K in D.keys():
        if K in d.keys():
            D[K] += d[K]
    for k, v in d.items():
        if not k in D.keys():
            D[k] = v
           
#############################################################################################################
def trier(l):
    """
    """
    #print "trier", l
    if len(l) > 0:
        if '.' in l[0]:
            return sorted(l, key=lambda c: eval(c.split('.')[-1]))
        else:
            try:
                return sorted(l, key=lambda c: eval(c))
            except:
                return sorted(l)
    else:
        return l
   

#ouvrirConfig()
#filterUnits="userSpaceOnUse"

FILTRE5 = """<filter id = "f1" width = "200%" height = "200%">
    <feOffset result = "offOut" in = "SourceGraphic" dx = "%1" dy = "%1"/>
    <feColorMatrix result = "matrixOut" in = "offOut" type = "matrix" values = "0.2 0 0 0 0 0 0.2 0 0 0 0 0 0.2 0 0 0 0 0 1 0"/>
    <feGaussianBlur result = "blurOut" in = "matrixOut" stdDeviation = "%2"/>
    <feBlend in = "SourceGraphic" in2 = "blurOut" mode = "normal"/>
</filter>""".replace("%1", str(.3)).replace("%2", str(0.03))

FILTRE1 = """<filter id="f1"  x="-10%" y="-10%" width="200%" height="200%" filterUnits="">
      <feGaussianBlur in="SourceAlpha" stdDeviation="%1" result="blur"/>
      <feOffset in="blur" dx="%1" dy="%1" result="offsetBlur"/>
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
    </filter>""".replace("%1", str(0.002*100)).replace("%2", str(0.03))
    
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
FORMAT_FICHIER = {'seqprj' : u"Fichier pySéquence (.seq .prj . prg)|*.seq;*.prj;*.prg|",
                  'seq' : u"Séquence (.seq)|*.seq|",
                  'prj' : u"Projet (.prj)|*.prj|",
                  'prg' : u"Progression (.prg)|*.prg|"}

FORMAT_FICHIER_CLASSE = {'cla' : u"Classe pySéquence (.cla)|*.cla|"}


TOUS_FICHIER = u"Tous les fichiers|*.*'"

MESSAGE_ENR = {'seq' : u"Enregistrer la séquence sous ...",
               'prj' : u"Enregistrer le projet sous ...",
               'prg' : u"Enregistrer la progression sous ...",
               'cla' : u"Enregistrer la classe sous ..."}

MESSAGE_DEJA = {'seq' : u"La séquence est déja ouverte.\n\n%s\n\nVoulez vous ignorer les changements et rouvrir la séquence ?",
                'prj' : u"Le projet est déja ouvert.\n\n%s\n\nVoulez vous ignorer les changements et rouvrir le projet ?",
                'prg' : u"La progression est déja ouverte.\n\n%s\n\nVoulez vous ignorer les changements et rouvrir la progression ?",
                'cla' : u"La classe est déja ouverte.\n\n%s\n\nVoulez vous ignorer les changements et rouvrir la classe ?"}

TITRE_DEFAUT = {'seq' : u"Nouvelle séquence",
                'prj' : u"Nouveau projet",
                'prg' : u"Nouvelle progression"}

MESSAGE_FERMER = {'seq' : u"La séquence a été modifiée.\n\n%s\n\nVoulez vous enregistrer les changements ?",
                  'prj' : u"Le projet a été modifié.\n\n%s\n\nVoulez vous enregistrer les changements ?",
                  'prg' : u"La progression a été modifiée.\n\n%s\n\nVoulez vous enregistrer les changements ?"}


LONGUEUR_INTITULE_ARBRE = 30

DELTA_DUREE = 5 # Tolérance (+-) pour la durée du projet (en %)
DELTA_DUREE2 = 15

#try:
#    with open('etablissements.txt') as f:
#        ETABLISSEMENTS_PDD = f.read().encode(sys.getdefaultencoding()).splitlines()
#        print u"Import établissements réussie !"
#except:
#    ETABLISSEMENTS_PDD = [u"La Fayette (Clermont Fd)",
#                          u"Blaise Pascal (Clermont Fd)",
#                          u"Paul Constans (Montluçon)",
#                          u"Albert-Londres (Cusset)",
#                          u"Pierre-Joël Bonté (Riom)",
#                          u"Albert Einstein (Montluçon)",
#                          u"Jean Monnet (Aurillac)",
#                          u"Jean Monnet (Yzeure)",
#                          u"Jean Zay (Thiers)",
#                          u"Godefroy de Bouillon (Clermont Fd)",
#                          u"Charles et Adrien Dupuy (Le Puy en Velay)"]

# La liste complète des établissements scolaires en France !!
import getEtab
ETABLISSEMENTS = getEtab.ouvrir()


JOURS_FERIES = getEtab.ouvrir_jours_feries()
#print "JOURS_FERIES", JOURS_FERIES

class Discipline():
    def __init__(self, Id, nom, code, coul):
        self.id = Id
        self.nom = nom
        self.code = code
        self.coul = coul
        self.domaine = 'all'


# Disciplines "Prof"
DISCIPLINES = ['SII', 'Tch', 'Phy', 'Mat', 'Svt', 'LV1', 'Phi', 'Spo', 'Aut']#, 'GE', 'CM', 'SA']
NOM_DISCIPLINES = {'Tec' : u"Sciences Industrielles de l'Ingénieur", 
                   'SII' : u"Sciences Industrielles de l'Ingénieur", 
                   'Tch' : u"Technologie", 
                   'Phy' : u"Physique/Chimie", 
                   'Mat' : u"Mathématiques", 
                   'Svt' : u"Sciences de la Vie et de la Terre",
                   'Phi' : u"Philosophie", 
                   'LV1' : u"Langue vivante",
                   'Spo' : u"Education physique et sportive",
                   'Aut' : u"Autre discipline",
                   'GE'  : u"Génie Électrique", 
                   'CM'  : u"Construction Mécanique",
                   'SA'  : u"Sciences Appliquées"}

CODE_DISCIPLINES = {'Tec' : u"SII", 
                    'SII' : u"SII",
                    'Tch' : u"Techno", 
                   'Phy' : u"PC", 
                   'Mat' : u"M", 
                   'Svt' : u"SVT",
                   'Phi' : u"Phi", 
                   'LV1' : u"LV",
                   'Spo' : u"EP",
                   'Aut' : u"Autre discipline",
                   'GE'  : u"GE", 
                   'CM'  : u"CM",
                   'SA'  : u"SA"}

COUL_DISCIPLINES = {'Tec' : (0, 0, 0), 
                    'SII' : (0, 0, 0), 
                    'Tch' : (0, 0, 0), 
                    'Phy' : (0.7, 0.2, 0), 
                    'Mat' : (0, 0.7, 0.2), 
                    'Svt' : (0.1, 0.7, 0.1),
                    'Phi' : (0.2, 0, 0.7), 
                    'LV1' : (0.45, 0.45, 0),
                    'Spo' : (0, 0.45, 0.45),
                    'Aut' : (0.45, 0, 0.45),
                    'GE' : (0, 0, 0), 
                    'CM' : (0, 0, 0),
                    'SA' : (0.7, 0.2, 0)}

AFFICHER_DISC_FICHE = True
AFFICHER_DISC_ARBRE = True

def getLstDisciplines():
    lst = []
    for k in DISCIPLINES:
        lst.append(NOM_DISCIPLINES[k])#+' ('+CODE_DISCIPLINES[k]+')')
    return lst







#
#
#
#
#
LONG_MAX_PROBLEMATIQUE = 600 # Nombre maxi de caractères affichés sur la fiche
LONG_MAX_FICHE_VALID = 2000  # Nombre maxi de caractères affichés dans le tableau de la fiche de validation
LIMITE_GRAND_PETIT_CARACT = 500 # Limite en nombre de caractères pour l'utilisation d'une plus petite police
#TIP_PROBLEMATIQUE =   u"Indiquer :\n" \
#                      u"- description du contexte dans lequel l’objet du projet va être intégré ;\n" \
#                      u"- fonctionnalités de cet objet ;\n" \
#                      u"- caractéristiques fonctionnelles et techniques."
                      
TIP_PB_LIMITE = u"\n(%s caractères maxi)" %str(LONG_MAX_PROBLEMATIQUE)
                      
#TIP_CONTRAINTES =    u"Indiquer :\n" \
#                     u"- coût maximal ;\n" \
#                     u"- nature d’une ou des solutions techniques ou de familles de matériels," \
#                     u" de constituants ou de composants ;\n" \
#                     u"- environnement."
#                                     
#TIP_PRODUCTION =     u"Indiquer :\n" \
#                     u"- documents de formalisation des solutions proposées ;\n" \
#                     u"- sous-ensemble fonctionnel d’un prototype, éléments d’une maquette" \
#                     u" réelle ou virtuelle ;\n" \
#                     u"- supports de communication."                             
      
#<?xml version="1.0" encoding="utf-8"?>
BASE_FICHE_HTML_ELEVE = u"""
<HTML>
    <p style="text-align: center;"><font size="12"><b>Elève</b></font></p>
    <p id="nom">Nom-Prénom</p>
    <img id="av" src="" alt=" ">
    <table border="0">
        <tbody>
            <tr id = "ld" align="right" valign="middle">
            <td width="110"><span style="text-decoration: underline;">Durée d'activité :</span></td>
            </tr>
            
            <tr  id = "le" align="right" valign="middle">
            <td><span style="text-decoration: underline;">Evaluabilité :</span></td>
            <td></td>
            </tr>
            {{tableau}}
        </tbody>
    </table>
</HTML>
"""


BASE_FICHE_HTML_SEANCE = u"""
<HTML>
    <p style="text-align: center;"><font size="12"><b>Séance</b></font></p>
    <p id="int">_</p>
    <p id="typ">_</p>

</HTML>
"""

BASE_FICHE_HTML_CALENDRIER = u"""
<HTML>
    <font size="12"><b><h1 id = "titre" style="text-align: center;">Calendrier</h1></b></font>
    <img id="img" src="" alt=""> 
</HTML>
"""

BASE_FICHE_HTML_CI = u"""
<HTML>
    <font size=11><font color="red"><b><h1 id = "titre" style="text-align: center;">_</h1></b></font></font>
    <dl id = "ci">
        <dt> </dt> <dd> </dd>
    </dl>
    <font size=8 color="dark red"><b><p id="nomPb"> </p></b></font>
    <ul id = "pb">
        <li> </li>
    </ul>

</HTML>
"""

BASE_FICHE_HTML_COMP = u"""
<HTML>
    <font size="12" color="green"><b><h1 id = "titre" style="text-align: center;"> </h1></b></font>
    <dl id = "list">
        <dt> </dt> <dd> </dd>
    </dl> 
</HTML>
"""

BASE_FICHE_HTML_COMP_PRJ = u"""
<HTML>
    <font size="12" color="green"><b><h1 id = "titre" style="text-align: center;"> </h1></b></font>
    <p style="font-size:11px" id="int"> </p>
    <ul id = "indic">
    </ul> 
    <ul id = "leg">
    </ul> 
</HTML>
"""

BASE_FICHE_HTML_SAV = u"""
<HTML>
    <font size="12" color="blue"><b><h1 id = "titre" style="text-align: center;">_</h1></b></font>
    <dl id = "list">
        <dt> </dt> <dd> </dd>
    </dl> 

</HTML>
"""

BASE_FICHE_HTML_SYSTEME = u"""
<HTML>
    <p style="color:blue;text-align: center;font-size: 16">Système</p>
    <p id="nom">_</p>
    <p id="nbr">_</p>
    <img id="img">

</HTML>
"""


BASE_FICHE_HTML_SUPPORT = u"""
<HTML>
    <font size="12"><b><h1 style="text-align: center;">Support</h1></b></font>
    <p id="nom"> </p>
    
    <table border="0" width="500">
        <tbody>
        <tr  valign="top">
            <td align="left" valign="top" width="300"><div id="des"> </div></td>
            <td alig="right" valign="top"><img id="img" src=" " alt=" "></td>
        </tr>
        
        </tbody>
    </table>
    
    

</HTML>
"""

BASE_FICHE_HTML_PROB = u"""
<HTML>
<font size="12" color="green"><b><h1 id = "titre" style="text-align: center;">Problématique</h1></b></font>

<p id="txt"> </p>
<p id="int"> </p>

</HTML>
"""

BASE_FICHE_HTML_PROJET = u"""
<HTML>
<font size="12" color="darkred"><b><h1 id = "titre" style="text-align: center;">Projet</h1></b></font>

    <p id="int">_</p>

</HTML>
"""


BASE_FICHE_HTML_TACHE = u"""
<HTML>
<font size="12" color="green"><b><h1 id = "titre" style="text-align: center;">_</h1></b></font>
    <table border="0" width="400">
        <tbody>
        <tr align="right" valign="top">
            <td><p id="txt"> </p></td>
            <td width = "20"><img id="icon" src="" alt=" "></td>
        </tr>
        <tr align="left" valign="top">
            <td colspan=2><p id="int"> </p></td>
        </tr>
        
        <tr id = "ldes" align="left" valign="top" bgcolor="#f0f0f0">
            <td colspan=2>
                <b>Description détaillée de la tâche"</b>
                <span id="des"> </span>
            </td>
        </tr>
        </tbody>
    </table>

</HTML>
"""

BASE_FICHE_HTML_SEQ = u"""
<HTML>
    <p style="text-align: center;"><font size="12"><b>Séquence</b></font></p>
    <p id="nom">Intitulé</p>
    <img id="ap" src="" alt=" "> 
</HTML>
"""

BASE_FICHE_HTML_PRJ = u"""
<HTML>
    <p style="text-align: center;"><font size="12"><b>Projet</b></font></p>
    <p id="nom">Intitulé</p>
    <img id="ap" src=" " alt=" "> 
</HTML>
"""

BASE_FICHE_HTML_PROF = u"""
<HTML>
    <p style="text-align: center;"><font size="12"><b>Professeur</b></font></p>
    <table border="0" width="300">
        <tbody>
        <tr align="right" valign="top">
            <td width="200"><p id="nom">Nom Prénom</p></td>
            <td rowspan=2><img id="av" src=" " alt=" "></td>
        </tr>
        <tr align="right" valign="top">
            <td><p id="spe"> </p></td>
        </tr>
        </tbody>
    </table>
</HTML>
"""



BASE_FICHE_HTML_PERIODES = u"""
<HTML>
    <font size=11><b><h1 id = "titre" style="text-align: center;">_</h1></b></font>
    <p id="txt"> </p>
    <img id="img" src=" " alt=" "> 
</HTML>
"""


BASE_FICHE_HTML = u"""
<HTML>
    <font size="11"><b><h1 id = "titre" style="text-align: center;">_</h1></b></font>
    <p id="txt"> </p>
    <img id="img" src="" alt="i"> 
</HTML>
"""

                            
xmlVide = """
<?xml version="1.0" encoding="UTF-8"?>
<richtext version="1.0.0.0" xmlns="http://www.wxwidgets.org">
  <paragraphlayout textcolor="#000000" fontsize="8" fontstyle="90" fontweight="90" fontunderlined="0" fontface="MS Shell Dlg 2" alignment="1" parspacingafter="10" parspacingbefore="0" linespacing="10">
    <paragraph>
      <text></text>
    </paragraph>
  </paragraphlayout>
</richtext>"""

TxtRacineSeance = """
<?xml version="1.0" encoding="UTF-8"?>
<richtext version="1.0.0.0" xmlns="http://www.wxwidgets.org">
  <paragraphlayout textcolor="#000000" fontsize="8" fontstyle="90" fontweight="90" fontunderlined="0" fontface="MS Shell Dlg 2" alignment="1" parspacingafter="10" parspacingbefore="0" linespacing="10">
    <paragraph fontweight="92" alignment="1" parspacingafter="20" parspacingbefore="0">
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">"Utilisation de la branche "</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">S&#233;ances</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">ajouter</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" une "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">s&#233;ance</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" : faire un "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">clic-droit</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" sur la branche "</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">S&#233;ances</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text></text>
    </paragraph>
    <paragraph leftindent="200" leftsubindent="0">
      <image imagetype="15">
        <data>89504E470D0A1A0A0000000D49484452000000E20000002808020000006C01B1520000000373424954080808DBE14FE000000AFF49444154789CED9C7F5013671AC7BF4B3650C2012141B43D6D814431B5DC8980A7F4EEC65604E13A8A4AB9E95D0F5A6A136C4D055BA79ED69ED31EB4F4041144C19B3248994E872AC5B6429B6887BBEBD90E126A87D65393C09DE799FEA0903BC680B09BBD3F76139210026212C0D9CFBC03BBEF8FE77976F2CDB3FB6EDE5D02B3038661663A049ED90B0920B1768625A25311331B00CF2C2760A603E0E1991C5EA63C7380C9655AAE44B9CC0F91F0F04C08C9FD97A0391BF70200AE7E81CDE7B9EA47D60167B1D33823B1F1F07070322DCF46FB0954F60340F9BAB1E60FB5F87026C2E2E17184009058CB942BF1C93167453AE4D78613A8ECC7D2643426708D0D27500934A7A27D00B93100F0575BD22D57E29700809A9A1A7F1D05CF9D46414181E32E09401D74FC93DEBCFD4AECEF4592966B28CF461D2B5C099A53A169C2A5F348622F0664E84C44A50E10235A87242D57B3D488B41CE02C928C00B015C8CDCDF5E7B1F1DC19343434B8D49000AA6EE6813DB9CBD0A9047A91A44334B05F89FDB67E72E092437E85194B0198718CBD6C1DC0550012AC01F6F017B23CDE8674DA3322C98872251ED101663CDE844BF626099AEDD7AF1234A7DE828F9151AA7740601A14DCA4BD10314DD3414141144579C116CFEC204880BB43E9683115142874DB810400099A13B1993DDD4B106D86A11FFF144329739EE39BA1E90780A5325B4E75A11FED18370AE835934400F9602CEE22BDF06BD3C8081D12428E8C586FDF14CF2CE1268DDE1F027ACD581AE5BE030900FD688F40A792AB6A38814BC0CE1368CE46E75A005C66AD1B40A31200AEF6E2EA04FE2ACF8C8DB2CFA0AE0F0A7E114B0808EB28ED056D0D8F8C0487848CD2DEC8CC3CB3030141C44803FED623581AC52964707090244992240502014110DC49BFB209952E43FBB1F99853C5A57137A7363739746E721DB5D5D6384231420128CA3B2B0718862B3C770C0CC308498C3A641E93C9241289C2C2C2828383499224271EEBED50BC6787F19E359ED9895EAF974AA50B172E6413AAFF64CAEB9467EA984C26001289243C3C1CECB5A98FD6D16D3D7AD4BEED455D7950A9F639510E5A062AD3B87D63555AC2C9AC2FDA9F99BB6B1234DB234AE37467D5B1331D88AF71F9406FDCB8313C3C4C5114C3300CC304303EC3250A063E2EC6AA37BECECFFBBAE488D15623537FFCBFF66DB25BB2A3290C5B336661868BA6B0344E77561D33F391F8BC8071D28BD56A7554919F4EFA0CBC36E999680AD5DB76129BDE54E3A9823663C1B3B7953FBD18ED6DD123539F498B66301B62F1359E8FD15FEB4D7D9E4D8D6DEF6163862C3A630BDE6B35DAB25151F89A233D6000A6A72A3D5C240D1749C34545DA71ADDCB6A6283CEB383A5E4A104977689C476DD7DABA15ED5863DB9DC88E6DA37A3BEB31BDDAC87576353816FF9154E7F07AAAD213E2931C7A6A77701DB8D82672E1D6947BA7B3A878D6A99F64CAC5E1BB626C3D852DE931404CE6469CFCD8A653CE37A3D999F0E2FDEF5AFACC96BEAED28BD96B8E1A1D5BEDDB69E5E6965CAC7CB5CBD257910646B333E1E4C62E4B9FD9D2F72E0E541BC100E8B8B8E4CD3EF3E154C665ECB86D74ECBBB2A1CF6CE97B37BF73CFC1335C18E30CB2457370DFB2963EB3A5CF6C294F75DF33B5C2D267B6F4995B72EB4B6CF18F77613C9A1A7F6A53B767536ECB03CB56E93A2FCC944E3DAAD4CB326D531184AACDAB26A746CF4727B12933160064E99BB0AF52E3DC7CF922F233D9058AB1EA179EE8D04F65E141CFE58BE8D8B742142916453E5AD779851DB372E3FA295E51AC7CF5B9340058B721175FE97B2632080090C525D567AD3F62AB71DB53BB3D522C8A1467357872D17AEA7CFE0B8E73460F4EC751525CA6D35D98DAD1F99569C9D450914270A45418ECD56DAA4CB432B519EE07F9F2ABA839BCA7A3734F7CA458142916ADDCD381FAF7CF60EC0BCA38C7702B95F9EF982DDFB3A522CDA5951937760AC65D0D722556DD66B654E3A948B168A7D65DCF9EAAF58FE21DB3E57B73F7ABC9538D7FA2A3705B00BCDD585D525CD6A9BBE0FF7CEA9969C8B44DB5B82947CFCEC35AE3FFA1B73764D47AD428E3B3A279BF21B9F4F301CB775CE97E25B9EEB4060C63F31B13A780ADC65875A03E3F23150C239327775C31D82CD823B46FC4C4295077A0DAE8E4CBCD814C66C7390C57830E25665BFBE7C52B2F5E31BAE969B8DC991C17CD8031B69E3AEFC145E68664E78193391D9B9232B8E7EEF96F3756BF565CA6EBBCE0C3CFCB6DF1B64C01C4C7C96DCA648539965FB9F46AA8487192A92FA750674FD72566653ADCB591A565AD7CEBB4C621B5A41DD0955ECC11454588A2124F6ED01D7E18602053EDCA7F8BAD3C8DDFD97A66E675BC9C288A2AD4B0A398BDF15111A2A808B6C6E15BE7E0CE9D1DA79E8E61B818E48A763B5BB96AEF03CF3F2373D3735DD12B7871558428AAE0B2C2533695A9342D0ADBC0E7B51E9DBACB67AC524B4ACA747ECEA91E754AD4D7D7E7E5E51D3F7E7CEA7FA3CE3D91790C50DA4FF06D2AA2258BDD3154A4E4A2E15CA11CA8A9A96197457F7C2560ED12C1F08877168B0C0D0D4544440C0D0D4DA1AF6697E4FD8CFEC30F7BC5F19DCEF2F855A66B5FB2DBD74DDF3EF6F8B3BBF73CBF62C572FF78BF2B50F089DE9ABEC40AA0A1A161686868D1A2450A8562D1A245212121C4F45F37D2A622328F41D9CAECBA9CB2B8E8B3B106652B539B61A8A83973D70CCBF4CCF6056FC47DAE51477BC5F19D8EA34CE177A57A96E96DCCF4336A19A65579ACA50DC0EA83FAB19F9F6A330C15298B9B1CFBFAF4A4EFA6F456FD4A225A90F3D5FE5AF57DFEF43B978B0B0BE6CF6BAC3FF47A4999AECB2F67FFF1113870EB323554A4D8EF39192E77AF562C96C7C57F56F42797FB50AB735CC6F9F57A3C5AFDC10F96EB3FB42BA3FDEB772E1747AC56ABD56A8D8A8AACFBF381D2E2329DCEE7332ACFDCBA4CE58FE4746772F3A5C54D390D857264D4EA0FDAEB88940A83BC705F7C917D4420498CD020F8F744CD11588DD2344DD3F4BC48494D75F11B25655D5D3EBC9F1A10408CD0100A26EC308DDFF4E585E798C2C9EAE4B58CFD01E87B42E97F0D10F78A0382845E906A000285023081131F13CFF42000678D521445D37464A4E450F9CB452FBCB277DFAEC4C484C9AC4C87511A57CDB8FB473417C438FCB1F424464C19FBD1F96FC14DCA0B0F99D034828228CA1BA6781C19A1DC6894A2288AA2A4D288D292DDCAA2D7FF50DDE80BD78102CC0FA1632514E0E1913D1F13282415F3A180B79E5E2280112F99E2192388845DA3D7AE5D9F374F4A51D4AF1F1B7BAD832418EC4CDC37101369147E5BC8C73327B06B34E967EB8F56BFFEF0430F1204B1AD202F3363EDCC06E65B998E7F7D05CFAC65686888D5E8F2C454F5B38FEFFEFD1FCF7DFAC16BC5BBB73CBAB5EFFBFFCC6C6C3E94A9CB6B800607074D26935EAF37994C376EDCB05AF98BCBD905C330D7AE5DFFE98AB5AAA77316CC978AC5A15D5DDDCB962D118B433B75DDCBEE97FB3398D0D0D0E0E060A150C8DE3DF2DF499F2449914824954A010C0F0FF32FDB9F6DDC77EF8F9727A6BEFC927AB13C1AC06F1EDBA82EDCABFDE89DC395254F3EB5737DFA43FE0C263838582A958A44228140007F5E9B9224191616B670E1428944C23E8AE537D73C53E1EDC66AC75D8542A1D1FEFD9B6FBE934A234242440A85C29FC1088542F6397D2EA17A4B2E6D2AC2D36A5370B3C8D1D1519AA6678D46B53BC2B371E2BF87D64DDE153D47D6A950AB7DE68E7FC8D38EC9F46DD69627939312944FFFF627F1F7FBD33541106EDE7A0243857DF9C8EA83FA738553B81071580C0520A396695511AAB60985CA3A6673F834656A38F4F32750FFE98E695E258D1BFED1B66CE187D4D1F553F3121C181080E0909090E9799F83C8E5B15F7DF99719714D1084E3DFFF036FD1E4C33BF0E2200000000049454E44AE426082</data>
      </image>
      <text></text>
    </paragraph>
    <paragraph>
      <text></text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">supprimer</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" une "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">s&#233;ance</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">", faire un "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">clic-droit</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" sur la s&#233;ance &#224; supprimer."</text>
      <text fontsize="10" fontface="Tahoma"></text>
    </paragraph>
    <paragraph leftindent="200" leftsubindent="0">
      <image imagetype="15">
        <data>89504E470D0A1A0A0000000D49484452000001150000004D08020000000726679B0000000373424954080808DBE14FE00000135149444154789CED9D7B545357BEC7BF270952C2A881F090AA144878A9B415D05B988E8B918785324A95625DB783D67682B6D5013BDE567B9DF1B6B754C72AA9966298D6DAD435D382228E0A57D0EA72EED52E5E6AA98A4D027DE30B0CA2209070EE1F2709799C04088110DD9F7516EBB0CF6FFFF62FC9F9E5F7DBFBECEC4DD1340D028160179CC1042A73282AA7722C4C21105C0EBDFF28A5F1948E78A9D270B932270D15B42CD539C61108E31CC67F2A73424BB214344DD3345D11755961B89C2A23CE432058C590BF45858B99935419E3310311491790CC4394521A1F2F95E6E88AF4395EA5BE80CAA9B4A9C438CC1108AE0907C0A79F5ECF9014A751C61D9DCA9CD0CB9B9880A4C82AC9962A0171EE195A1FA2F2B65502C0D9BCCB194C89A4F86DA9124A697C1A2A7452B2540B254A69765E5485659823105C14DA980A0900482A6845419C8994A482A64D0AE30A148A82B8B8025DD2C79C1B9798C9EB94181A2010EE074CC7DF5265345D21292EAF643C64404C96AA94C61BFA48E68E611D33254895D1344D6794531419D523DC07700040298D37DCCCCA2B8D7191A1E2F0A8B3BA1C6D80B8AC743100288F949C6555264ECF82512D4B254A698E5409A4CA6845415CE315D20122B8383C0010A76735865214531257A0382306648A827893B2DC4D5154289507204E22B1127FC4B9F2815A920ADA424938F2181DFA6608045786A2C9FC0302C15E069D7F402010AC42FC8740B01FE23F0482FDF09CD22AA51F537800211DCEFB097BFCE79BC66FAE5E6DF5F5F37BECB1C76C889D3C79F2CE9D3BBE3E3ED7AE5F9F3D7B766060204DD306CF89913D88B7517DCE83FBC5715F624FFEE6C1F7080B0FEBEDE955A954D6640E1D3A44D108F0F76F6E6EF6F3F30B0C0CD46AB50F72D821DC97D8E33F2291A8BDFD168FC7FDFAC205D66CA4B3B3332A2A6AF2E4C937DBDABC85C2471F7DF4B3CF3EBB70E1C288AD2510C61776F67F1E7FFCF1D6D6D64BDF5C2CF9FC8BA5CB9E03609C9BFDF8E38F3366CCE8BADB75AFA7E7F2E58BA74E9EE45094BFBFBFC3ACBE0F681A41288E781053DFF189FDE36F0101014F2FFC5D6F4FCF179F7FAED168286AE0516C7BFBAD8E8E8EAFBEFAEAC68D1BE1E19114A829010153A74ED56AB50E329B4018178C68FC5A2010A4FD2EBDB7A7A76CFF81BEBE3E43FCE9686BADAFAD292B2BBB74F1A25028D4F66B1313130170B95C07983C1C7648B04334C66D121E201C307FA7ADADADF2C8517777F7C5CF6672B9DC7F1C3C5179A167692C75ABFD1A28AE8FAF0F683C956AF22B568AA20CE36F6BB3900D3C5F822656EDDE284BC2C61234194E862C909E8CF9CD5867758C63680C6A001B2FF5EF1E59AB84F1C8AA55ABCC4A46FAFC47ABD50A85C2D4F4A78F551C3970F0008F3BF15071DD9949FFF6735BEF1F1327C5FDFA3713274EE4F178C6BD2313BC91009C0652BCD1D46EB3A5762C2E194E3970A41A4786F972EC31C00AD9D9D90E6C9CE074E472B965E148FD8749C98442E1A2C5995F7CF1CF27EFFCE873BD6416F593EFC2CC8519E983568F10012DF852809522ECD4FBCF0E09E601004E9FC077310814609F043FB4005ED8781CF999D853AC738C1D127CB91F2B93B0B10429497AC97358AC425926029997BD7F4033134CBE03E60974FAD7DD4259124EDD4276303617433907FB66EB64998A6B934C0D284193918550E3F9E3C837C4257D8C223C20386CFEC1B19335EE15271F9A786FEA8CA8F93F5F9E3CD37728B5528271EA388E7861730C226AD104ACCD024E20D69074DD428251FA8476EC69C17C118EA80011E6B5601DB01200B0F3B85E12D821D1FB9837CA9250659C7409F0DD7EAC6B0744A84B44FA7E4080A07AC45603006A115B0B0010A12E063BAB8DD43206185BA82FB1416F9FA6E516B7B593DBE388A113AD56EBEEEEAED1681CA08B3018EE5C044CD4060934EE13DCACC9F03EFDF4D3E5CB970FF7AF9996D2A327DFF8A46D59CD85299ED7C2D216F3DBD5752FBCD05950F04442822D03BD91006C6C07DA713A1129DE680212808D367B2C479AB1390450213D04F27A76B541C0660936EB0BC430F21F35AA9870A4C2E9448478016A14AB06EA1A0217D488004B6F2748802F6DF7A9BC819BBAD316358FE2F07E1D8287780E7876DCDBABF5F4E4F5F6F68F5C1561507AB46869E3B4A811E1675586C738C370FF1A73F8D8A92DFB3B9A7FD61EFEED5B133A0E5F3D7C28521CFE64D4A3F52FBC7079E9D2AC4D9B3C3D3D59DB8E10E95223862011760EA5AFAF823C06E9C07C2F14B703DE6C326AEB031236F04659264E31F9DE1062CB50F8A593FB9B108A4BF5F7691D70D3DFEBEDF5F0F4EC238F01C6042E45050B39FF6AE646F8E93EBBCECE4E1E8FC7E3F1B85C2EB38AD448E75F97579EDC5ADED570411D384BECF6C8F4F8D79647EC95375E69EAE5203629892F977F9C94A4FCF65BB0CD9B4C09C6E913882D466C31624F20301811ED380548CC469C0530FBA16A550BE62723A8C5C24318C9767C27B050628908F3D4A8BA655AA88F4E11227D14B230E03B35E65BB15057CB6820A45743BB71D1DF4FD334C8E15A477F3FEDC6459FD197556B6B6B5B5B5B7777B7E149E688FA3F5FFEEBABBF1CE8BA78EE9A6F58B89FD02D6B5A53D2BCC5009A5E7CA9A1F08339198BE2962C3973E0C0E167331796EE178585F5F7F773387A8FF5364DD554BA146EE7719465A22E1160FAF72AEC69C1660956B60CB4DBA4425026F6149B5AD3AE973C87C5FB079498C722A388B7B9184DDEA61A6EE9AEFED0821FCCD4EA0D30B6106AA01D1BCF619F049B8D6B99E2A8F902B4FE203805854221140AA74D9B361082EC78FEC3B841DDB9AFFF50D8D278BEDDF3E14051A45FB4FB371FBDB58C11D068344549497E4A654CE612771AFFFB45C9CDE0A065870FFBF8F83002C6CF7FC694E13CC31989B697FA7733E3D7C7BEE53C15C9EDEB734CC6D5DDDDEDE5E5D5DDDDED106D84417173E31E6BEA5F10D60F402E97F378BC808080D0D0D08080004F4F4FCE4034180E1C0EA7B9E5FB35F2EB2DCA1E0F2FEFA0303F6157D396B5C906011E8FF7E4B66D6AB7090D07CAEE51885B9AE5F7FDF76579797D7D7D0E7B65AE033DDA47D5AB82497CC124BE60D2AB558ED5ACDA953C29A15035FA2F611C1FC6DCBD7BF7DEBD7B1A8D8659900DF6CDDFB973E7CE7F7E54CBE9D1C644FB06CD0CE276344B5745F9F8F818167A03307BCE9C991FFDED069F5F5BBABFBBAF776E7ABAF7C993FFF3F1C70EB81F47423B163B2AF80C5D1B3D9A1FB06A5772264A6E77B5DFEE6A3F17AEA872A872D19A63B74FAD1639FF2676D601DAE493ECEFEF37DCE10CF6F8CF4FBF5C3DDDC87DEE897E7F7F9EFA86BA203B60E6CC0800FA85AF7503B54F2626A61C3AD41111515F56DED975276EC912F78913ED68CED5A1319ADD5CD595BA39E121CC79C89A55C9CEEF76DF57C7601FAE3DFE13FCC8F445B3AEED3A8ECB57AEBF1CAB0A7E64CAB973E76A6B6B6B6A6A6A6A6A9893DADADAFAFA7A773E3FF2CD377F899AF5C3F9AFCF8788E2162EB4A33997871ECDEFC8E485D9B5AFAF2A54191556E54D4EF8B0D9ECBC2A6F72C287D5BB164CE60B27F317E8E4AD16E6FD314138F9D56A2BD5F3AAA12A4C109AD402DDACBB2A9CFC6AB5B91EE7471287C41F4BECF11F7777F7CD794B8A56FCEA8317A72E5D94D0D6D6A6D168B45A6DBF11CCBFD7AF5F9F3A7DFAA25DBB7C3EFC30F6B9A51E1E1E7634E7EAE83E86D13A5276A81B171D8CF299CC5F67E8FD18B7683847CDA6ADF850DD75B3612B36BE58A4B2557829ECE39BEA0F9258AB97AE9467F25FC6C737D55D374B57D66D2C384E0374D5BAD907163574DD5477DD2CC57B4C9FC9588FF563D6CC27EAEBCE3BDF57D88EC1DCC7DEF16B5F5FDFC4F9439AA1A32322C2ACE0FE5E09E0A5A2A2316C4DB4BABA6B75F3AEA7A2F9EB4ABB76245B139BFBB66C4D088090357F5AF17A850A08B15AB8E829CBC7677AC9E485D9F8269411485E988D7C45339270E5126AE4D1FC4D8CEC0A26D160D5C342FE3BDB37BEF95A4CCCE3C37AD9E301E7AC5F350A0BE18F2FCC5FEF181C216B0AF3E7CA8F56D1A68D1ACE8D0A558A8B432C64AD6E4D60E5E7EAAE1BCC214D3113B37100F8FBBEC2FC77B6D7D59F7776BC61B1CD3664FDB75187C6687670AB7615A99873D5B18335B1A1229A1689E7D47CAB64AEFE536E681D35872A55340D5A5571A876656A928D42930EB4F909EB79707824F6BC57A832EB7C0FE52580C6C301FE7FDF57F8EE3BDBEBEBCE3B7FCC6038E307CE59FFED8162281FC35055597E2F26872BBCF8BAF98DCBCBAFBD2CA2819CF52BFDB3F89F0158BEF2F7FA8AC0DCC86F5FF4F3AA01F0FB92AEF9B60A0D55CCCF590B01D04879AF7E6B5A4C94DF9B7A4BA42C6236605C68D9F3AF6CD8F85AF4B849E42C320973C8FAF1A3C2EEDD03F30F12C3B8F77A9D3EFFA06ABD77BEB8FE544EF0A08563CDE3514FB4FEA45B9BE997D66BCB9E7FE58D8DAF45478F0B177A6802F74BC5C0FC83EEEEEEE9D3A74746464E9F3EDDD3D393CBE53A2C7F73CD7DEE8763B5521A4FF66C1D651E0EF0FFC7BEC22DF9DB1B1ACE3BDB962131C8FEF5B630BD9F52657405D246D7834678075B54AFCC494385C506E38EF6137A549FFFB8FE61C6147FDF7D7BDFDF92BFBDBE611C0C2758DA670AD3FFD1ED5F7F460CA032274701F35F0C0C895419ED5A7BDDB31B2CCE3D73C6C10D392A471EE8730F9B94BFB6A55858C25AE84C9887877E7E3E7BFEF6DECA97FEF41FE32691B386B5FDEB95D278E32DE9E399CDB58D2294529A9D77F66C5E28C5720D4A697C7C4E4E3CB3CBA9EE9A4EDBD077B437BF60DAA241C64A431601755083A5D21CBD1A7D0D56CBAC1ACCC6041ED5AB0559B77828189EBC6BB55A5F1FEFDD85EFFCD5A9891C8743F56AE16673CD356BFBD78B7337E9F611466579B164532ECCB69E17E7CA75BB6D9FC955586E768FB38D91729AAE9014A765436ED8E07EE83BDA5B489AB468141ED91B8238F78CEE594C4554DEB64A0C6E70DEE50C9A1EC8E62C0D00C0B821ABC1EC3C3C51FBFD2D9AA2380F4DE08EFCF0F498E0C68543548D9F031460EA3CCC74161F1FEFF777FCF9BD2DDB2F367EED14C3288AF3831A01BFB235F6C303F393ECE5CB6919D39D4E83A48296A522354392565E294B4579B124430631A2909746A18296A5CA64263A94571A515C4C197ECE26512052BFD970645C5CA4EE8455529CC1AE9645A7959C92B521004A697C689E6E9FE3B848255207AAB31B5CB0DE3899639501200EB7FA3EB0112CD0A8DA51F723B747E380DF6F6BB57077D7681CA16AFCD0AB61711E8D46A3D1688442AFADF96F48F2B6FCA570DFD81B36810B7F4F6D88B706B0BE7E88C97FA9329ACEC8A1CA2B65A97A07CA40B12443A6BB2633F13023E20A14C64141297DDB5A83669240AA35B51692C340298D37F4E894D278CB95D8866230BB8CCDF7C1020E8550A12654E89815733A6EDF9E3E6D5A47C75D87681B27B8F360709E9F7EFAC5D757A8D168B29ECB3108783D84F9C13D4EB4D00656F6AF0700A4AE2F684C4B6B64BE9759B79E3F7B5901B67DEAAD31F41DEDADE93C3B78CAA4431797A03C5272D6ACFA500CB62663CD60C20830384FCCDC0515952798E5D457E56497977DC21CCE36D02A1C80D9BF3E4DD7270E2DC992EBBF74C5E95971FADB501C8EBC50130971EE2649711A45C54B43658A0283029BBDEA5473494BB5D62461DCE260B7AD387753944E6FF6E5A83843E1300C663380F57D208C1883F394977DF2EE965D1A8D664BFE86B7FFBBC0D9760D8ECDF9079539D4DB91F627510F3086F9078E5DEB509FBF753850A7D3899C35EFD489038CF3C4C63CB6ECDF57E7FCE1F99933C3D6E6FE797976D6530B7EEB6C03E1E6E6063BE61F30036FC47908A34A7898C8E03C005E5BB7EA8D37F3B55AEDEBEB57BF93FFBEB3AD1B045BF3475DEE7928C11531EBDEC4C63C161C1478F5EA75A1D0CBCD6DBCCF6F26BF5FB83F682E4A11E848296AB626559D6BEBAA63D0B7D15C94626F6305DBFF6BD52B1BB66EDB2D2D78CBD1E63998F1EEDF84C1692E4A89DE30A354AD4ED6FD5B548DD52CBF42ADCEDD16DE50B53A646CAC0A595DA55E6D5FD52953FCBEFABFA38E35679420FEE3EA3417ADDA30A3542D35384CC86A76176916ADAD4A1E23E7796020F99B8BD37CEC60CD8AA759A38D202537374520C8AD0613A3A2A30502DDBF30CEF8981253792325FA1CCC705E9D2B48292ACA1D2C5B34AACBD6D61034B800C47F5C9FB9E15616E9A8B914BE5BAD9626A33A37FAE0330D6AB55AAD2EC5B6A266B09418CB0F4ACD862B4FABD56A75E98A9A0D3BAB0711666F6B381AC62FC47F5C9F9A2B56B67D99FBCC82100068565E42CD8668814020103CBBB7E68A8AA5C4587E70E6BECB2CD79CFCF40A5C52DA8E1F56DA1A8686710CF11F172764C13373F71E1DFC0B7C45A95A8F2EC058968C1E63D9D69842FCC7D50959BD7EC5DE678D7A2DCD454566EE14229E81BDDB8CBB199625EC88C2E7EA0346F5D1BD761A38C4B65C12E23FAE4FB254DDF0EEA567F5CF7F566181F9577CB2B4E15DE85228A60F6F59C28ACE39050281E02856D86DDF90DA7249C8FA3BA30299FF763F61E7FC370281601BE23F0482FD10FF2110EC87F80F81603FC47F0804FB21FE4320D80F997F3DBAF0788E7C8785DEDE5D5D5DCC702A613C40E20F81603F24FE8C1672B9DCD92610461D32FF602CE8ECEC6C6D6D552814ADADAD77EFDEEDEFBFAF16107D7098387162404040686868404080A7A72787C321F1672CE0F1787C3E5F281402B877EF1EF9CE72513C3C3C8442219FCFE77275ABCA93F83316F4F5F5757777DFBE7DBBABAB4BA3D190F7DC45717373E3F3F993264DF2F0F0E0F178144511FF190B98F59DFBFAFAB45A2D79C35D178AA2783C1E8FC7E372B9BA8569C9C73906306FB2F15F822B425194F95FF271120876F3FFF6DA42B01ED999360000000049454E44AE426082</data>
      </image>
      <text></text>
    </paragraph>
    <paragraph>
      <text></text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">d&#233;placer</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" une "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">s&#233;ance</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">", la "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">faire glisser</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" &#224; l'emplacement souhait&#233;."</text>
      <text></text>
    </paragraph>
  </paragraphlayout>
</richtext>

"""

TxtRacineEleve = """<?xml version="1.0" encoding="UTF-8"?>
<richtext version="1.0.0.0" xmlns="http://www.wxwidgets.org">
  <paragraphlayout textcolor="#000000" fontsize="8" fontstyle="90" fontweight="90" fontunderlined="0" fontface="MS Shell Dlg 2" alignment="1" parspacingafter="10" parspacingbefore="0" linespacing="10">
    <paragraph fontweight="92" alignment="1" parspacingafter="20" parspacingbefore="0">
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">"Utilisation de la branche "</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">El&#232;ves</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text></text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">ajouter</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" un "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">&#233;l&#232;ve</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" : faire un "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">clic-droit</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" sur la branche "</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">El&#232;ves</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">.</text>
      <text></text>
    </paragraph>
    <paragraph leftindent="200" leftsubindent="0">
      <image imagetype="15">
        <data>89504E470D0A1A0A0000000D49484452000000C50000002B08020000004714DB550000000373424954080808DBE14FE000000AEC49444154789CED9C7B5053571EC7BF37B901130A84047954A924C147B44E45D4163ADB5AE451A8E363B5ECB6B5B0655DD42A0AF6E5A3769976456911A8BC949D3235D26E47ABEE5A94366077A7DDDA0E03D48E2DAD9240B7CB0A550AEC322134DC9BB37F24818424A07013B0E63367E0E4FCCEF99DDF856F7EE724393714DC0821C49DD379703F3480A8A3EEF837376EA2DC308B87C98537D90178F845E1D193072E71A227094EA7601E0060653C1AE2DD189187DB191A002438BD1EF758B5AA2E0CD7AB6B81781428B053EBE6D83CDC7ED0E6DFBDD87002DF0D354BB0DCAA53752DAADD199487DB167A0CBB55EA52BD8FC3C0E9F5A8AC30CBAB20031F57A07A449F6ECC5B8AAA48007632F5F04B870690A93B06715A5586A5AD171BEACCD58221F548703A0EEA13A86C43AC02D55A408187DAB0D3BE4F1D72239153816A60653C22E0D1D31D040DA0D827ED11BBF5CEF4331CC8C9408EA53902A86E458E1CD062A51CAA46477DBAF13D90930154A0BAD63D57E161AA30D67A67BF6069A18AC24A20360015DD80C4419FEA0A0028C8400ECC89CAC31D020520EA24391D873DB6F9C9D49291015C18F9CA6EA3F1889BA3F43095D9BC79F350DD929FC418DE3F59BD5FB0F37D9C5E8F8615006CF2506A6AAA1B02F530F551A954D60F6900E8C6AF2B46F63B6CCA498E4C1E3C3863ACFDD3A8180699B61E7E471FFF679683505896F5F6F6661886035F1E5C86371FA1BE6CB898F1F612D85B27A4A7B65E9AE2D10FCA318DE6E0EC80C1C0FAF8D0068371E2AE3CB88E9F59B4FDC46BEBC5BC2007561AB77E92646379B9A972AD8FFF2B39C5A78C832C0722183018843E3E832C17B9CE83CBE053944CCAFBB4953F2FC8FC4FEFEBEBA3699AA6693E9F4F8FE38CDB9123E6D777068608F860186E8E4F11622E1EA6328410018D41AB677D4747874824F2F3F3130A85135AEFCC134CDC85C50FE1CE9B07B7D1D2D222954A67CE9C49D334077AF208EA0EA7A3A303804422F1F7F79FE8793AE296A2DE2E126F570FB7688BE3FD96976ADD34FB788A7A9B7845B1162050EFB00A55BD5D145FAA9DFCF0265CACD1E9740303030CC3104246D553CD268AA2628A34A30BCAE5D16B8B5FFF263DED9BDCB2210129323FFADF3FB6286EC98F3ACB6F79999B24A8CECA9BDB78215366F5A73799E20EF71F41A1BBC2705519BE2A0080D16824849836E23C405314438D20A648034D51CC6BCA16D2927222751445110CEFA35D545A6B4E616D76E65A9CA9D14EC48F7BA2250444ABC8ACCB0C77326FF8B3D989EE09C375C5797AE101115917092184B414464717B6104208B998158188AC8B56BF262F3F696BCE607592223C691DCE9CD75A1240B6FFF2B2561080B41627FA8BA4FE22A9BF28BBD6CE6AAEABB3FDD71C43FDCB9122E90EB5EDA86DB5966ED93B965B1E3AF363A9946E33CD9868BF78B51627462E5C32ECD9D6E42F92FA2F5C12B9AD16DAB2B8A180416AB749E38AB50E029B8A651441395DEFACB2D6D08A57B389A228CAE6CD2AB377D715EDF9BF615DA20C9025AFC6A98F2C82B23CEBD53B235F9A7FB2BFABB7BFAB29AF79FDF272ADB575A89E50D0FBD7542C7BADA9BFAB280144BD33F2D4EAA6FEAEDEFEAE93C837ED6E50DF3CE7ADAEDE92383262AC5D1DF5FBAEAEEAEAEDEF3A99DEB0A7B0CE2660879E1D9AB0E5C57455B5DA34B0AEBA32F5C54CB9C3E1CECBBD0B1E686CB8E47E4139971378008E1D3B666FB0642D42CE2FCC7EA306D014C524E33C71F33D99AD1F9EC2DA6439002812D762DF61B5ADF94A33D2934DB74BC8339FFF5D7DCBCD1C726FBDD28CFA7D8B45816251E0E3950D574D6396AD7E547173412D7B6D7B0200C4AF4AC5D72DAD637A76628A5F95FAF6D93A00509FFF266F5BFCA8C39D90BBFF5063E3A59B0BDB1DD000D2D2D21C58344531B3B33F37D5A3951ACD951328542539E8C895BEAC13810575C99EFA062C0CDC33D472B6AE286185DDD4D6A36EAE31FDBDDE122B3F6AFB21F663C7743E96E711266CCDCDDD5AA69521B779ED5B32277D46E7DDAAD227376CDDBDF7B9A8A84563F575074ED63B4D51CCEC13292D967D95F3F104AEDCF7A9CFAA96E67DD1D37FDD5C2EBFBAB4F29CDABC252404443657094B8BB638FFEDF4A43810A288585A7F5563F13014E15045365789CAFC52DBDDBD830B19CB8FFDA8513C3B32C912D7E14C61C9997B9FDBA2703ADC7901C1DDA1C1EF56951ED87FA8B1E1D214D98F3B213A6565040068AA4F7C0E2062650AB2DFA8B1D3932BF7E317CE5546AD49960DB72812D62C3B7E4E6D952412F21BF39A53444101A2A0A853AB1A4B620102C5A617D28F9B1ACFE1694BCFE4B4FA57A24441596AD328B2776150802828C0D462F5F4B09ACE911F9B9E76A346F1ECC044E4C9AB50797CFEAA58E7C34729264C92CACD3DD4D878C94D3B28E782A286F7439AA29854A82C2FE66A3651C91500109D9181CB4AD5C5AC08CB0A585E5E6E3A4FF7D155DE8A39FC0103379FE0EAF5FA808000BD5E7F137DD52F48CE267597C47232F16DCBA2850F74B47F65AA5FEBF8F1890D5B77ED796EF162972F7CD3BCF81FB71813E71801A8542ABD5E1F1616A6542AC3C2C2ACF293ED3B034947CDDBF18B478F9ADB2D5B7457873B3675678F2F992B9FEC28A614778706FFA5AAF460EEA1A6A6C9DC9E4FF8F31697BFFF645BDA8A1F93884252BECE399A39CB9DF34EC9328290E0E9556FBF7930F75063938B173EFBB92D7071BEC0B9F75BF563DE668E4278E6073F65723BEF2F03A3D168341A8382022BFF9C9FBEF1F917DDB2F0D933A1FCE44553061694E77B9D261B939858966559767AA0E448E9FED75DB6F0F17894818580EFD83AA1FC74B72FFBAF1EEA1E31CF5BC081A678F012F041BC9C44EAC11E0AB01513C3302CCB06064ADE2C7825FBF957F7EE7B212A2A92DB390759FCD08BD0BB58F3F4B64C484F3231A3ED46C3BFF93F331C9CF76559787B330C17AEEE100C8C0331310CC3308C541A9097BB2B23FBE01F4BABB89DD48B8F601F562E6100AEEF47F012D0CA6028C1D5896F0A3070E4EA8EC09BC69098DADBAF4D9F2E6518E6374F0CDF5D2911C2F4AA9E6B2887620227FB710F93C8909896DCFF6879E9C1D8471EA4286ACBE6B4E4A415630F7601E3D4D388BB423D4C0A7ABDDE24A6455171995B37ECDAFDA78BFFFCE0C0FE5DEB1EDFD875E33F9312D278F414131D1DE8E7DBD6DA16141A1ACA18AE7EF7DD8F62C9804ED7D9D9A9D3E98C2C4B0821C4D8DEF2456BF3E706F0454D37F883E6ACFB504101A7F1DFD11042DADBAFDDB778C5A63FA484044BC562DFA6A6CB0B16CC118B7D1B1A2F2F983FCAB1352EF1F5F5150A85028180A2A871E627C134A1974E27EEEDE96CD5FA0787FC24F0F2D3E9101232A0D71B8D4642F1BA3BAEF4B47F2910F0F93CFAAE697CAF41A311E0F98BC3C2C2B8BD985BA0F31C8A81FD8F4D5A005C33EB9E198BA2E25E79397376443880279F589D99B5B7F6C3F74A0EE73EF3FB9D8F263EE29E308442A1542A1589447C3E7F9C7A124F9FEEAF54F60B859288D95DD7AFDFD5D3D3F96DF38C84449AC7638D467D5FF7B71F170AF894D09B3630C63EB9D0F786403163BE7CF51AA5526976F1C37124E759FCDD87F3EFD87C83A72BF0698010180A80137E388EDDC03B4FDF9AC9B61F9E4AC657C07D2F5975FE144F7D3FE6D877AB4AAD1F2A954A75ED679D9DD7A5D2001F1F9192DB2B758E402030DD7F271008C6A927966166CD9AD5A9D13477754967CC08D7E9C21EB8FFB3B6B6D8871F360C327FDF9DD5ED77639061698128543677A66CFE2CD9BD124988978F68383F0D8AB1EC006A9F0580D63244E6E3BF6F7274814E1814C31BE0364186EDC127139BAE361FBFFD129FC851BB031F0CE25939CAE2B1BB1ECB0E8C23D42365AFAF59F7CCD22591E565796E5B0A288A1ABA3FF8FF5C8904D454A2A4F50000000049454E44AE426082</data>
      </image>
      <text></text>
    </paragraph>
    <paragraph>
      <text></text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">supprimer</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" un "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">&#233;l&#232;ve</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" : faire un "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">clic-droit</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" sur l'&#233;l&#232;ve &#224; supprimer."</text>
      <text></text>
    </paragraph>
    <paragraph leftindent="200" leftsubindent="0">
      <image imagetype="15">
        <data>89504E470D0A1A0A0000000D49484452000000CE000000400802000000DDC7DF3B0000000373424954080808DBE14FE00000122B49444154789CED5D6D5413D7BA7E2601A9412110821F05040C05B478ABA01EB0E71C6E2B082EDA5A8BD8552DF5A80DB415052B5AB5F658D1568B1254FC00C5DB52ED072A62452CA05D1615AA06B1A57E600850B1620D8508050492CCFD31494842822424A4689E350B76DED9F3EC3D334FDEFDCECC7E33044992B0C002D38366EE0E58F0A44087D4AA52838252AB0000A7620822E6D40076C982C7133400A84A0D225411942AE8AE119E4EE663A6456C16F4130AAF16C813904A94C47BA9550A4F27D3C307BE6F163C567854ACD6EDF08252ABA88F4A07772A862A6BD4D162B0C002D0007C71C101A5095E2AE3A7421FA762BC6EACA33C9D202A3B3AB58A13BF8E9B914B69ED546E06775678CF3A55A9D1097EF924499264BEDF0D81CEA62D78C240922429E005AA0DA00A8B8017A856979B4F92643E57F13F902720492D75F2B9CACA1658A0C0A306503509A68703084FE455E49EC2A9DC8AA8088ED63AE1E9244992B37209C272ED6A8112BD4A8DE3ED579A90AC29164E4454456E8C42693DEB54A5C6A45601E1E9A4801758516909D62CA040923D07C1405EBE6248555DA5F45E025EA0EAF8A859871A40D5B6B0C00282B43C98B2604060793065C100C122350B060816A9593040B0324BAB044198A55DB3E3498E8C8D20B58A8A0A0683515E5E3E6AF468BBE1C3251289A7A7A7BDBD7DEF5BF9A73F7107BD2CE609FD825130C200FA7576B6B3B3F3B992925F2A2AEE8B443F9C3D3B6CD8B0CFB66EED3FB3058F13FAEBD51E3C78F0574B53F2B6E52F067B7474DC2B2BFBF99B6FCF7575755A5959373535ADDFB0613B8F67948E5A30D861B8D4DADBDBBF2F283876EC002F65318B65A7B4AF783FB2B6F6DEC143C573E6BE16B7245E26935DE6F3A74E99628CDE3E2E581C660A56E2DD0253D0F607E4A4EE30C940A9E51ECFDD9F9922BADF78FE5CAAB5B51A098D46F3F41CFDD1BAD74522F182052939B9B971EFBDD7AFFE5AF058C0C0588DCF2F4CDBF1EED664EE9D3B22CAF2DB6F7F68D461B3997BF6BC7BEBE6651AADCFAD3822270A3ED45FC37A3668D09AFA5D01715EF4E88ACDB541DFD5AA3D49AEBB46645E4C6D3655CF4C0403BD5AC5B5DB292987972C99C5E7DFF4F0180560C182CDA74F6FA3D369004EE6FD343DC4DFC6C6DACDCDF978EE8655ABB7EF4BDF6F65A5BDADA5518806E667E3A6C13B01C01139D3B14695C41139917053A9927506C12FCA2DEB8F606124508ED997D53757D9EA7639CE7A209AA9D6CEED1AC0437FDA1EFDADAAF835C17112F93C1BCDB541872B4B010081539E2FF1B305443199573200C0257FD1782DD39F5DC793A1D788B3B5112FBB7354ED878014958FB381B580BF8A25177055B1940100EA80598A72DFD9A88FE8339BC152CBFEFAE891A3474FE4958C1C61FFFBEF0D4F3FEDA4D41980BA3B7F3437B7B2D94C00CECE0EA3474A235EFEB78F77402A6FBB26912382816220D411371B0DEB8B6E883515BCA3A95B520BC5A8F5C0522176A8B49B1289B347E4969410ECC8C60EA82BC611390E7AD3F68028F9127873D800F0A0D52F7446892B00514CE6AFA963A67AFF7205A133485754555CF43A2F222768237075E7959F4FAE734F775531CE03E629CA9B00774559F5C45F50A864137008980764013BB435D193ED02B0039806005800D401B7FBCC66F0006A636333EF8D3704828EB0B0A96969C71E88FF52EA0C406CEC2B94CE442271DE89D2A9537DE2DE7BA9B353CBB1F7190BD4E08726048FD55CC58D029F0B3E174B1D01008EC8E1AA581C911385A521E07311012C9D0E37260E729133598FBDC82843B4BFA6B15AD1CDE5457A503D92560D75F733D82322A84B29D7F10AB9307CD90044B9952EB35C018033664460632B3574E69D2F20320B88CC82983AAAB26D8407B342DCAA831FC851114A6F3D01040AF5F45287629BA652B30270D55653375BBFEEABADFF6FD2C71BBE5DBDFA8DEDDB8F5656D6F5AC909353ECE3EBD6D2D276EE8278F1E2E53D2B847AE0AC1079D570F3500FCE98A83D8D800CCC2F47F474F8002991389081800C041C41F074F80060C2BD1A0119C803769CC66D31E66728462E05C941853AF95A833F21D603292A2AFFA106EBB9E087F4BADBFAD36AA04AFC57A0079BA3616D166543A13F0A76B67EA256010051E58D3133C84533C850978C7279DCC6610E2B7DD0A6BD812C40F560FB03FEC02100C0344000F82BD49305BCDDEBCEF6645B00F82B3CA53E6CB42FBEF80280BE7FD376EFE6F3F923478E8C8D59BB7EC3372B125F2F29A9F8F0C3CC3367AE88C57F7576765557DFFDF8E3CF69341A87F3F4D91F6FBD39EFCD9F7EFA49B371470403858D8010C54C843AAAAC12A3B011006E0A719B098E23DC81F5D4D98D841B131C006264087B3D4662CCA7D49981001DB1605E19DCFDBBE5925784800C045483DF8BE0F4A7ED03443187FF880A76D7D41F05B67722E542EC6DBBA706DADB2A7D9E1A345C5A99624901286FF0B9C2A27442FE8AE5916CCACDFDF566A3BDF5D65B00F4FA7BFDC68D582E37FFFBEF1F3E7C386EDCB865711BD7FDF7C4A8514E6BD7BE2993C9D2D2721213F77EFE79C1CC99818B16CDE4A5E60407BF9A7DE488A7A7A740A096D4E233563EEAF1B9F817B48CA16A503DC119C8EBB5AE1E68C49A1A70359A16222003C51E88302EAD4E886232AB7DE74C8DB7533737B756B06DBDB46F023C682D75B4D5224D0D27A4845F0FCB3A204911BD9501B3810B7D669B0DDCD68FCD9001B4B0B070E5EAD5555555FBF6EF073066CC986DC969499B4E787BCFDFB7EFE4FDFB0F860CB11689C41B377EF9E65B194181F36E090457CACB1FB6B733996A9773A11E283EA350CF991E6328004A8E35C86B442DF351678E7275FAE3E6656022DC00382247E9C91CE12E467F26AB77D3F6008739ACB44624276FAE0D52D3197B96F79DDC3A00A8FAED0FED6202408DC2F60C4DAB8613BAA038DF753DA2AB0B8097B678AB17B6430A4F0620076AFBD6073643AE40E3972D035074FAF4BEFDFB41A3757674F83DFBEC5336239C9DC7FFF8636973F3D5AEAE87D6D64FB19CD8972E6627AE5A356CD8B0E8F9F3594E4E5B9293B77EF6999CC511C1C01AE5082844F18B0875507C64E220356D5C8CF9D900B0FC087222C17F51613CADDEA7461CA8C17A2E1696AB846B4A12002A77250E72B1FE88DAD6CBCF80EF0F34E2AC03F88A4DB28EE8B8FFA22F6D4FB83A730BABF39ADDE3ED50F5DB1FA510971E2E480040DDEF787E526E660101002EF98BD868D61AFBB7E6D588FD26DA6A9AD7A93B21376096A2AC7161B80F4802004C03960239809FE2FE852E367775365561F581CDC009DF070F1DFABEA868D3C71F8F1933A6A3A3E39B6FBFDDBEBDF8A588FDD45A929401C48D1B3977EFA5EECFC8F0F1F139969B4B10C4CCF0701B1B1B0004413C99333BE4477B715855C545AF079EE4F36C03B9EAAE11E5B602F5FB6A8FE783A9F9F3E6CD9F2777AC363636139F7BCE89D57DE39B206800468D9A38E17F66FAFAFA0298FDEAAB86F7F77104C7EF59DE77E789F3930C515BDD35A2F02FDE9CF186050CE68271A64656DEBAE5E4E4AB617470F0BC7F5F6614FEC70DFBBF07100FC41B4AA07544F89B0F13C6915A7575359B3DA7A7FDEE3D6B994CA6C733D05EB158B6D7283CE6C2E23D7BF6EE1DDCBBA02F6263639565E348ED96A076F448172D2BA46E0281C0DBDBDB28AD00888E8E36169505A646565696EA47E3F89BFAFA761ACDBAA77DE4C8E70A8A0C7DBE63C1E305E378B5FCBCFFD3B1C6073AEE991B30D17EF19E3D54A1B34B52D344AF6FA17748F5E5D002A9546A63632391488CC0F564C3868E51C3A5EE4C89CD102D7EC73C195386DD6151063A35622B826635CD134F59192131A4B3536A6B6BD5D969B982E92F3AA4A8F9935623868FB396B566CB98EA0FEEB6D0FFE949D0095997D408FA78D8D939D4D6B64B6A0C0FF964834E101E2CDAB96ABA8FB3FCBCB4B4B4585959595959D15567FE188C81CF98EA9490D674C8642449C2B2FC7D16998CB4A6A34BE53B5B5F5FFFE79F7FB6B7B74BA5D2419C3165ACDB48A462B1C0E81008042C16CBC5C5C54AD724ECBEC0FC195316ADFDED117131024E403DC036F46647EEF1DC3973676CDEFC61E6FEA5AA3A834AC6D4D7879666A4A7FC67F1623A9D6E8C6EAB8134F552B88469C760DA3198764B0A8DCB2CDC196217BC4B68FA5D30D3A28676A0039002E4DF2D63AAEF204D79BC843B432291DDDCD6D8DCD658EE2D28342AF9D8B882E6B3EF8C3549CF7DC7FD835F76D59C3AD3D09AAC5B80068A80CA981A31C281CF974FB459B060B354713D7832EFA78E8E2E0054C6D4CEB4ED5AEE5AA9BD9743EF1F9D2761CA085758C99FECED49953DE36243CC1F71F77101B031691B9F7FD56C7DD0384F6260151005FCCB50A9657F7D74EA3F5E3B9177B1B353F2FBEF0D007A664C516565C6547CC2324D96EE5F3C8DCAF6D2F3079A4DEAD5425E8EBEBC2A769750C55898601FBCBB5AA35C98601FBCBB68E70C7B06CB9E31435E5FA731615930CB7E49918ECD138A20DC15CC52DB0A64B57C2DCB7E49913A8F76A7027C7570D7A68DDBCCE5DB34B5D6042C04B2816273674CC9C1F1EE9E8DDCEDED14EFDF084A4D8D21347E274BBE57A65A4253C415AF1CF373B2672C57466AAA2D2ACBB8B46E0B768BDB1AAE6CC19A457B84BD19AF3F93D9204E9BAE75F3C30BB32219EF22B341DCD67078217F0DEF34099085CB271E7DE54A5B83B8ADE130B652F19D8247C7A9C6E85123BE3AB8EB938DDBCAF857075E6B1A4A8307A078006EE68C29394EE56604FA7A01C0A9182FF9FB3504BC0AF99BAD4A136ECC2207FC97C9C6BE53D4D67065CBF5398C5EB3F4A624A5C77902F08C5BB1E09240D89BF195B09E33D61535435E8E56560879391ABF0AAA81EACAEBB8B46E12C389C9709A73807F4BA89B470D72B56DDA56567655BF9D361DEE9837634AF90A98245F41493C0740556545202F311C0038115181D48B5F14160D0CC4B7D4336ED72753B24E1692EA8D2ACB2A46A1E05A1F8D5A37D75561E137E23611B5A4866A54D3E6D4E450AA6D8047529D78C3AC195350FE5E7DA9DEEF072261CAD8B670E71E215516161CBB14E0359624C772265FBA5545ADFD2E4BD93A2E1D3F25244990C2FCE39717864FEFC5A8163B6B16B4963DBC7D7160EB2EA146DCDDDB6581CAD9A6D4F6E9A66D65037995A0F56C45015F9935634A0E4E7C493E66529199CA0B37AAF2B24BB9B374BDB08F34ED6581B7C09FE1ECC07076F0FB685CEEC977C792181B93B8F0CB2886B303C3F924DE54C81D98E27B6B91B303C3D97F956F76DA0BBD19E59BE8E3D542B7966D21D7FA393B309C1D18CEF19ACEF5914E65E408F6979F6FFFE4936D6503E6DB343A415D81EE005CCC9831A58AF074012FC88B08E2094AA8120100DC7C321C5595BABA61ACE0ADDB25742334B9B12D59A3A1E969F71AD3E4265EB79DB3F4EC3D9E7A4D2DC6D0E4C6D01E65AD46F5B247DCC9C638D5AEAA547B046432994C267376763AB06FEBC2B7577CB0E6FD49939EEBDB21311EA8F0722960F0CC0E2A632A79CB1665C6545313F3A508F9241F65C6D49CB9739519530D0D0D9B9292BA2938F125256A9F48F94CFBEE52CF6A16F41194CEA452A9542A653B39EE4DDB14BB64AD19D4E60FCC043C80918336634A67586000D523435A3DB7ED0FA151A0AA33894422954A9D9C1CB76FFB68D9FB1B5699586DBDB8DB419C3165CA01B48F08FDECCF9EC39956E3C0A1A7CE241289442261B11C923FFD20F183CDDF1CF972C03A93E292E2EAEAEAEBEBEBEAEA3A9832A694186245744A4110663B9D7F67287576E7CE5D369B25914822E7BE33304DD36844A714D63A26570CB28C290AA3874B7F6B22DC98341B6B234CF8A66188351DE410E34F3F3103082875E63F256CEFEECD2FFCEF343A9D783BE63F6161D34DDD789714B7C518354C0A68392FC6915A7D7DBBCB689D195346979A0753226C04BF8EDE2131C2002D95C2C64622310695D9D12901A5B38993C33EDA75F0C3A4D5C5FF9CBA79D3AAB96F253EC579C1D4AD0FA16384ADD4D35102982C8DC5808CA9FE6088B595EF08F8C258D90004D069242A33C3C60A77EEDC0D981A967F226B72C084E26F475FB952317EFC33E338A3A5C2A299E12F9ABE0B84569DC1F23AB3C70C3EDE9C80A961278E674D0E780EC0CAC4F73E58FB89542A5DB9223669A399DF5532C832A63412A62DD0405464485464C88DEBBFDCB8FE0B6519624DBF77EF3E8BE5D0DCFCC0BC47CF0852FB3A3B7BF5CA95E74A4A7CBCBD9FF1F2BAFAF3CF13264CF86CEBD6952B56F49F5C15AA3F0001A0A5A5A5BEBE5E2010D4D7D7B7B6B6CA648F43B06574CC9E35FDF579EF8C717BFAB5D921EDEDED03DCFAF0E1C3870E1D6A6D6D4D10C420CE98B2B2B26230182C160BC0C3870F9FE4F71FF68E9DA9EBCDD5F4D0A143592C1683C1A0D3E986BFBB5D57C6944C26A332A68ACFDD8A5B12FF5244848932A6BABABADADBDB9B9B9BDBDADA2412C96092DA4731E6EEC100C1FAD3030C06C3CECE6EE8D0A1FF0F1DB51AB032A2FA330000000049454E44AE426082</data>
      </image>
      <text></text>
    </paragraph>
  </paragraphlayout>
</richtext>

"""


TxtRacineEquipe = """<?xml version="1.0" encoding="UTF-8"?>
<richtext version="1.0.0.0" xmlns="http://www.wxwidgets.org">
  <paragraphlayout textcolor="#000000" fontsize="8" fontstyle="90" fontweight="90" fontunderlined="0" fontface="MS Shell Dlg 2" alignment="1" parspacingafter="10" parspacingbefore="0" linespacing="10">
    <paragraph fontweight="92" alignment="1" parspacingafter="20" parspacingbefore="0">
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">"Utilisation de la branche "</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">Equipe</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">ajouter</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" un "</text>
      <image imagetype="15" fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">
        <data>89504E470D0A1A0A0000000D49484452000000180000001808020000006F15AAAF0000000373424954080808DBE14FE0000003CA49444154388DADD56D4C5B551800E073DBFBD172CBBD2DB71FD2022DB4AC03D7751D32D886A2712698CCF881CE650931137FF9C34497C51935216AF4870966C698C8D4B80CE6548851EB66305337A3086903146ADBD17665742BA59FDCDBDEDEF6965E7F6010CB6217C3FBEB9CE4BC4FDEF3BE3939902008603B42B42DCA9D42A5D25A91CFFEF7197863954A84F26C0C959072CA281289378805F78FCEC951B54A42E97A6CF71CAE005DFC76E87BFB678944D2DA6A68B3B59A773DAC6BBAAF58C839262E84FCBFCB6B08959A724E9D178BE1DDB69ECDF9C5220FC30800005A6F768ECD249337BF1E7DF7D2F837045EF3CC530F241948A7D5E6B96596E522515A21C7D2CC5A9AE69E7FE10C412AD7957834F49D7DEC78FF897FA0BF79BE3072F6C4F08511A3BEA1FB80154681D717CCB1BC5EAF37D4AB6F84E304898951CDBECEC7B95CDAED727C7CF68BB7DFF9D4BAA7FD5F3D0200C008FAE4D13792B1C80F3F5D6DACAF4BA49238A25C0C2D31EC2D92C069A630EBF645A2ECE55F26611174E5B7F9DEDEBE75A51C0200E032C5B1E38345E1754C949662A88290AA14B8F22EB31812A65DFE6834D3BAA3657E21702D70637F47FBC9936F6E24968F3F9B59BD1E0CD66A6CC11073F4C84108A5318267694F2CC5F125692D85483079F0FAF29EDDB6D3A787ABAAF0DB8C7F3D32A9E8B8FDAB43F7EEF557D78DD9E71E7AD00A397C8F1D6AE701ECF6467029E2F238FA9FED7FF1A5011C976D4E84CA9EC8CA928F8DFB0182A6D3CCFB1F7D084439BE90EFDEDFACA48851BBCB64546772D0ABAF7DA2505065159457C4D0AB935333088A88D0AADE479F1EFEF25C3CC6A4E99C73EEE6BCE7962F90786FF0CC56E5363DBA32E1C425F0C1768B6547432ABED2B9B71343A5C512144F70F144E695536F7575756F550000E2818181CD7B9A6692CBC1069DD6D0B2D3686A326835969D2D9F8F5D8E256843BD1E11F28D8D4652A1AC0C69B5DAD9A9AB350A9224C92A4A4510329D5E8B23709341D0D54A57B349AFEB0F93B9AD9A9057B81A8A6235942A1E4F4697C2C5741C88456204EBE8D877CD9FDD65B2B83D8BE6BBA9F32343957B0400D050D54C26EB0F84383657E28B02806A9B8C5D070C74492208102AE25094AB0C09A5122EC5F40D75A1F0F2F48C3B4F337C2AB9E45D884423859CFBB9BE3618D2AAD4CD95A1225FA896E104411C39F6C4F49CEFD2F8CF3936EF9CF17C3034756E78962FAE4DCC2E1A9B5B2B433CCFE1325C55A79329D48FF4DC9FCD667F9D70FCE90DAC95E0BEBEC31004CDB85C24A9BAA38A8050C2A4381001A5466DB5B4CCBB3DE1C84A215FA09426FBC5F0CBA7064D26F356A8FC89FCEFD8B65FE42FDD99AB3DC740662B0000000049454E44AE426082</data>
      </image>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">professeur</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" &#224; l'&#233;quipe p&#233;dagogique, faire un "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">clic-droit</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" sur la branche "</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">Equipe p&#233;dagogique</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">.</text>
      <text fontsize="10" fontface="Tahoma"></text>
    </paragraph>
    <paragraph leftindent="200" leftsubindent="0">
      <image imagetype="15">
        <data>89504E470D0A1A0A0000000D49484452000001230000002E0802000000ECABE8100000000373424954080808DBE14FE000000D2449444154789CED9D7B5053571EC7BF975CA4C40A21A1D817AE9050A02D335A840A6D1DAB8886652AB62C3B3BB5E0A825B6154D6C6D3BB4B44EADAC56916C7D1176D6A9A9D3E940B56891B4413B4E77163B1418B7B4F84882DAB5A5D32266640C14939CFDE326E1E645822684C7FDCC19BDF79CDF39F77B92F3BBE791732F143846092124D41238261E34807415D774FCA55D46855A02C784242CD4023838A6049CA771708C05E3C8D3769762B7D8394A88A34548098D1C0E8E4042038010470B318B15ABFE0C1FF6F9CA2AC4D11C94D7E17C2074E42F014E61932110657923A082393846056DFBDF8895A36D827D78B62E603A1A9BD118B0C2BC1050C11C1CA3821E216D772916304746AC3C894A4787C0740E4CCC4954E6E032B0400000DF30FD12AB9374EA1E8538EA8F31BB8F3502404A060ECFB595E1D166651DCEB362B6D4A2116E36AC2AF8A89A73697EF5F01C1C23420328BB79088292C3A5F6382356D621B708388579065BE31B09012E7F864D7D80186D8B916FC0A2421C74B4F51C68D9BDA51FC6A585B87C0ACFB22E7DFE3BCCFB0E0020465B3A3E6CC66E371B474C4A060E2F41A3271B860D7E546DF70855E0E0183D34803DD34B9E761B3D960AF0B59FB32623B4CC2DDF806F1623518CD9C096526CB1A74BC02AD9A7B110B38D2877B9B473EF94E26EC38A396FC04F85C8F7580E0060B6CFAA0947AC0207C7E81969F478FB8C6AD6E7622CC46A1703218E16E2B463D09803C438ADDF78C61F1BFF557170DC195E57F92F1BB1C865CD5D0009002045ECA5118BB1C008AD01970528157BB4F0C3B80F9705C8153A5FC8DE13DA620CF8C66EC3CEC5949322C6AC4B6874B7F1BF6A7DFE5581836354A4D7932BC48943F5C429F23A795E459EEFB09D5DE92657AE93E7EBEDFFB232BEAB22E92A0F79D3DDE347303EE97C211579B7DB35C661339C8B558EAD64179B7A7B5E9F55F35E0500848363F450F0B9EF71E49FA146F52355307ED112A32D11F39A6FCB66F47ADA6514E17618738C9EE0CCD3824FFE126C49B01D6FA9BD1D9BB5D61AF4A2E9533C093CE9F775D71E38505353334AB11C539475EBD6398EFDE8D326296BAD35C5C5C5A156C1316951ABD56C4FA331559F04597BE040A825704C21E8293BEB700C02876E992F5DE7F5F4F3FEB004A0588BC512111161369B035016C784228287FB6658660BCC11D3C2DD5327EA3C2D805C32D25418FD4422EEA203D0B70F0D59A64FA78786AC775E14C7C4E20F0B2E5D0BBB64444A9C8754CED3F04B3FEFA9448A47596F5902E01E83434391D3A7DFB204A27FE49850F0282A4114F6EF6E5E4A9CAD21F5F7F7D3344DD3348FC7E33C0D436612CE83D91C98513421B6C031D5208484D3B8C5BAC7F6F4F4F0F9FCA8A8A8C8C8482F7B44F4CAEC6CA51E00A09151944C330642430BE10217EE38B8A0D3E9AE5EBD7AE3C68D5BB76E8501805E994DB1C956EA86ADA52AD284BCC9EF6B21FF96B8300982333D3D3DD7AE5D33994C168BC5DEA76555EB86378EB4C8939C32485544251D8BD61E2AC6E65BD06EE00B366887630C7B96442DDC67087DF30858D0AE1744F1058BF71842AE247481CDCD9B37070707CD663321C4D77B4486BBBB6CA59E3975746F1A1973EC62E32162DC4382FF1D18F67CF0E3EA921F2BF73B5C4B5CF6D58DD32F8947558E561EB570FF38754EADBCF060C967A6BE536509A117139A00E2D4ACAC562BD37781D9CB7FE83F3138A348620D1EEDEEA191259DAB606C754575C54ABD445E515ADBC0B89AA6A1B6B440EA6EA357162BD29A08218434A59DD361024030BC9211A4D0AD3982158AB215F85C63B89372C646EDED6ACB4C1287E6D20F3F3CBFADED6CC83F01E2BD8D85012879E2BAD3E8B145CE3C4202FD854ED4E631EE97A43873E69C0E9016D85C4DD3D059BD59EAC146929C86DA3C4AA601A4AA0932EA24C1BEDB19349F63B9543C5BFA1C3E6FB20FAEB48AE885FBBB4100D2BD6769345F14CD1745F315CD6EA9B663AD22BAE0105ADF9ECB176DD43AE75ADF6C37536C5C683FF5568EFD60DF7AE68A4BF7199CD56A15D10BF737DB0AB7A73A17EE2A78589BCDDE559B617F0EDBDEE5D4735D3CCA6634B87626C0B6F7ABDADACF8EAB3E8D8DAFD1A3D3FC4D250520DD5CDDD9A081A6A1B3285FE2D146AA22849082068A9A28AB96B6CF2878C1D0740CCF2D4D0012F296E3C8578E798CEDBADA4D73DF78B8DED46B34F576ECE82A5C78C0C04E751CE7EE36361423736B87A957990BA2DD34F7C8F20E53AFD1D45B8F5DCC840FAD5D0FFDABD7B837C7A519BA1FA3B5E2E233BD46536FFDEAB6F2EA93AE4DA6B56207F61B4DBD1D3B50BEC6AEC751B8BBE0616D5FBE2CF6A04D5B5DF14843AFD1D46B34EDCE81EBA9E7BA7896CD68706BE3F8E4F0BECAF7ABDADBCE86D0D5BC3BDAC89E26494E3BA3D8E9EA2B92FCA2CE0699DDD1DC6DF44A99520F485544579DD57961624CD4824BF79747B0222F1100C44B57A0E243AD73F2852EACCE5B0200482C7B6D55ABCE9FF74A745FE8426BC563FC58013FF62F07DB2E327932972FF3F309D6CCAD1B720160C933C5F841D7ED96AA2A4B74D5632FDCA760776DE2E4791F152CDB6FB77339F55C17CFB2BD55F0FEFB667E72785FE5B6AAF6F6B3FE7D02638ADDD3D8F3B4E1557EA94A57DD99E73A7F93E41775D6A2C236C674B39124C35658525D91DA3E121DEF04F34EA7DD5BDEDA569E162BE0C70AF899E5ADF8E8F8490CDFFF88B386D144AEFED468FA9D09CA5C9754E296D767E19EB218743FFAC8E297B6C4328DD1B40F6B6205FC4DCD703DF555178F977017EC70B6500D2347200C0024F216A7C7435BE452790B335B632739E66F12790B7BD9DFD586193D3AE518E710047396AC3DAECED8F1ED75D36FB6D0F95EC6C1135ADB049A109084E454D8630C7B767DB45A9A0342C4928CD68B7A7B090E858E8384E4541CDCB5CF797DC543457C95E331175A8F312B3786A663DF317A5C2FED26D897368284974E7FBB2DB3EBA2C1F5D483BD1FB259C1D1CC1967FBFBB6AAF6902C90786F63E3E86DE12184047345E4D48983E90579AC856F716E41E6C727B4AC3B74EEAEF61D5D45FCB8187E5CFA9167DAF72E0208C4B2CDAB3F66224FE005BB655E49EB3BE9FC38B996C945DE4A8B8BE1C7C530318E02D9C163394E96EEB980CCD48B6BE262F871E96FA4D6317AD8661E05BB1A38696B5ECF1CCF7FEBD1575F16BB9E7AA88B6FD9DE3A135BCF5659D53EF63D9B77579BBACFEAD7D4D89E04FDEA62D8E28778834381D9133C3030101313333030E087AD76B3F0B8B46FEFA2805C389068370B2B25EDA76509BE4DC70973D2E6F75CFDAFE3D46AB5FEFC73CFCA551BDF2C7FF5B1C7E68C998CBBA6F1BED659973E6405A056AB070606E2E3E3535353E3E3E3B93E2D749C3CFEF1BCE4C450AB987C58AD56ABD51A17177BF09FBBB6575675748C8B0512CED380208F1E3D844B7BFE2CE4DF5BF4C31655D99FC6787833498303C6CD2C168BC562B9275658B377DBF6CAAAF68EB11A4612AF6D8C7B6AC646A006D1C373F411985DF6C5B5B2C05E37A0E47E702D17E354DB48B0DDCC6C365B2C96D858E13FAADED9B8E9BDD7C77618E90ED7A7611A4D0D59404DC577A94C2ADCDDCC6C369BCD66912866E7F6373FA8AC0AB680B0306AC882709EE754AE4FC3FD332C57AE53B3046111E101F0B6304C0BE7814CF3F2797304090A0E37BB7AF5977BEE1199CDE6A2BFBDE4480F0BC35D41FE526E59F09311F7DD6D615E39E7C2889EA6915179B559D53A0F3F8BE995D9C5504F94DFCB4624416036F4A1ED7FBC3FCC0178BB81C5828808B339104571F8CF90190E379B9BB1ACF6C0F6454F3F611CA0A47F2DC95860FB7B42A7F5C1FD52A6F13073BA255168063CBFB147AFCC4E529C718ACDAAD6B5E437666F4DD5115D6376B1327F52B89417A685D3A933918A40BDF983028602541487BF44D060DC6CDEE3CB9ABE50AF2F2B5FF0D4E3AAEA37D6BCF8DADB6BC7F26714CAA39B01081BDEE2A1ABCEB2EF156E914B2061B68948ECBB453838C6358C9B7D714C9D316FCEAC590F7474740A858259B31E68D29C0AB5346084D123ABA7738C1F35322A8F79EB76697535804619A5A80580D226A292B2F3D8B2B8458C2FD46A75A82570040641F4DD73D273CA5E5979AEEBFB735DDF3FFA48C2CB656F7EDD5CFFFA6BEB5E28D9D0FBFBCFA116081AC0A143874A4A4A5C1224F2162207006864D44E8D5C95A4CCCE431321CC7E47BD325BA1385741880AD0C8A8ADCACDD2E49D49E72A9874BD32BB5899AF46B122AD89B448018D4CA603C695A7B1DFE40CA0BFBFBFA7A747A7D3F5F4F4DCBC79D36AE5265A138917D7143207CCEE9C7B678A8431D1BFFEFA9B48144351F06FCB4EE099316346646464787838455134007737039CA76F59A97AFD853A54ABD9CF7566556F664E9352B3607B6CB49672FCA589529DA4200D8A3C0A4D442555A982569DC040D3349FCF17894400060707A7EC26B549C386F5AB5E58B5214992B0FE95E2F8F8F89068888C8C1489447C3EDFFBFB1EF5CAECA4BA221D6991D89619FDC26D88282544058D8CA2F2EC03CC710B4DD35151510F3EF8A05028645EB1126A451C778AA6717E680584878733EF7B0C0F0FF7BECA9F657BA45ADF5877064590E4172169A746EED55D24C96967F29C0CF44A5963BE4A2E55115D6A76F1053DA4E36AF8E80C8FC78B8C8CA4693A3A3A9A73338E80405194E31DC6FF071D4DBE680D7AA3FF0000000049454E44AE426082</data>
      </image>
      <text fontweight="92"></text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text></text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">supprimer</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" un "</text>
      <image imagetype="15" fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">
        <data>89504E470D0A1A0A0000000D49484452000000180000001808020000006F15AAAF0000000373424954080808DBE14FE0000003CA49444154388DADD56D4C5B551800E073DBFBD172CBBD2DB71FD2022DB4AC03D7751D32D886A2712698CCF881CE650931137FF9C34497C51935216AF4870966C698C8D4B80CE6548851EB66305337A3086903146ADBD17665742BA59FDCDBDEDEF6965E7F6010CB6217C3FBEB9CE4BC4FDEF3BE3939902008603B42B42DCA9D42A5D25A91CFFEF7197863954A84F26C0C959072CA281289378805F78FCEC951B54A42E97A6CF71CAE005DFC76E87BFB678944D2DA6A68B3B59A773DAC6BBAAF58C839262E84FCBFCB6B08959A724E9D178BE1DDB69ECDF9C5220FC30800005A6F768ECD249337BF1E7DF7D2F837045EF3CC530F241948A7D5E6B96596E522515A21C7D2CC5A9AE69E7FE10C412AD7957834F49D7DEC78FF897FA0BF79BE3072F6C4F08511A3BEA1FB80154681D717CCB1BC5EAF37D4AB6F84E304898951CDBECEC7B95CDAED727C7CF68BB7DFF9D4BAA7FD5F3D0200C008FAE4D13792B1C80F3F5D6DACAF4BA49238A25C0C2D31EC2D92C069A630EBF645A2ECE55F26611174E5B7F9DEDEBE75A51C0200E032C5B1E38345E1754C949662A88290AA14B8F22EB31812A65DFE6834D3BAA3657E21702D70637F47FBC9936F6E24968F3F9B59BD1E0CD66A6CC11073F4C84108A5318267694F2CC5F125692D85483079F0FAF29EDDB6D3A787ABAAF0DB8C7F3D32A9E8B8FDAB43F7EEF557D78DD9E71E7AD00A397C8F1D6AE701ECF6467029E2F238FA9FED7FF1A5011C976D4E84CA9EC8CA928F8DFB0182A6D3CCFB1F7D084439BE90EFDEDFACA48851BBCB64546772D0ABAF7DA2505065159457C4D0AB935333088A88D0AADE479F1EFEF25C3CC6A4E99C73EEE6BCE7962F90786FF0CC56E5363DBA32E1C425F0C1768B6547432ABED2B9B71343A5C512144F70F144E695536F7575756F550000E2818181CD7B9A6692CBC1069DD6D0B2D3686A326835969D2D9F8F5D8E256843BD1E11F28D8D4652A1AC0C69B5DAD9A9AB350A9224C92A4A4510329D5E8B23709341D0D54A57B349AFEB0F93B9AD9A9057B81A8A6235942A1E4F4697C2C5741C88456204EBE8D877CD9FDD65B2B83D8BE6BBA9F32343957B0400D050D54C26EB0F84383657E28B02806A9B8C5D070C74492208102AE25094AB0C09A5122EC5F40D75A1F0F2F48C3B4F337C2AB9E45D884423859CFBB9BE3618D2AAD4CD95A1225FA896E104411C39F6C4F49CEFD2F8CF3936EF9CF17C3034756E78962FAE4DCC2E1A9B5B2B433CCFE1325C55A79329D48FF4DC9FCD667F9D70FCE90DAC95E0BEBEC31004CDB85C24A9BAA38A8050C2A4381001A5466DB5B4CCBB3DE1C84A215FA09426FBC5F0CBA7064D26F356A8FC89FCEFD8B65FE42FDD99AB3DC740662B0000000049454E44AE426082</data>
      </image>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">professeur</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" : faire un "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">clic-droit</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" sur le professeur &#224; supprimer."</text>
      <text></text>
    </paragraph>
    <paragraph leftindent="200" leftsubindent="0">
      <image imagetype="15">
        <data>89504E470D0A1A0A0000000D49484452000000E10000003C08020000001F714ADC0000000373424954080808DBE14FE00000111C49444154789CED9D7B585357B6C0D7C90348C22321102B0AE5110A68A90F4405ADA353B484B1954B29EDE7288E8F016DB5176C9DAA1DFBF51B1F532F45B0BE90DEB62372AD437DB5C560D14EADDE81118830A002265154AE010D210609487272EE1F79903749482094F3FBCE976FB3B2F6DA7B9F2CD639FB9CB3CE46300C031C1C378630DA1D5053918D20D915863241616262A16074FA83E3461040509888E8639B5F38D5812AB253808B1DE538C99C59708F1FB3900000120AF855396CBBEAB173AAAA9CD609CE51CCA5FE09E0E40EE38C24968EF515D9FA81553F08A9CB839FD9D9DA38AC39580F0666C3C065A3B24E12995B6DA462AAA3930D4AB4A70C463A8343186A68568680331A108EFD9301D5B991063FB9A0303105B818866118BF20C1BA81EAA698120CC3308C9B559C925D0115D991CD3B3075DD8CB24CC39F7868E58AECC8DC58C3A6D939556A158C1B9B9B570166740625FC82A6946CB33A6A6C199AD521E08C388455F3BA21A1808F69A9CA6103BFB93A2BD5C6A36F42C652F5590227350B9A5A2B5A9BA038451708AB9BF976290B5A9B120AB61835AD8B6A29C5D0D42A30D5D193B0976624149FAB306B07006C199AC0EA1070461C17CCEBF53D7EC889D090CA82C2C4C8B20CBE5EE4E337570FD9075B7486D32B9C11C4AC8F46C624149F33BA12A40D2782F232F33F7FC5B9E2848CA59CA8D8EADCBC0AB31A3628B3A362ABCBCA05860D69A3AF46C249CDD2EAE8D5D2D81194975567A5724C756C1F1ADBB621E08C1826A76509057CC3733543414256564242019F5FA0F91CAC98C5C54CCEF3F403928DCADC2C8386060583924191AED6A01DAD65231D7587CDB5683C342B43C0190D6088EF753FAD03DF0E47D946B8593A9FB45BC715FDC171016E729FC93E06AF1EA500D7C2E9A22D3A38630204C3EFD7E3B83763328EE28C2B4823DF24822023DFA815F023899BE3641F55A95015DA4F22D3ACABC51D7517B7E065BBD73F0C8E298EF8687757DB33F9630F2F3F3A33824020AA852A15CABF799177ED142BD08B392979C6ACA54EED27CEF8C56E1FE57E5F7CBEFC6F5D5D92695342E3664C897A9133297C8172A0AFAEFA649BA08AEEEF1BC862F26A4E1089A4976624EB57542A152412D9793DC7192FD83DAFEF933F9548FEEFECA9BC8ACAEF7C69FEABDE5C24E9412605053DEBEF90CBFB459D3206DD53DA834A65FDEFBCF785AF5F80BA96B8B3ED87F2D3ABD7BE0F000882B8D5B11E3F1F7573EC9ED753A8DE932647AD7FF77046DADBE2EEC7E77EFC1702F24762C1355E630DEF26814860D0194404C242FC2AB979F7EFFEEBF6AD0B674FEE5AF587D766C62D70C500707EF538386722913DD2DFFE8BE4B1E8C23FAE84054FEEEA96D0C801F7DA1EF4C81FFAF9D2643D03FFBED92AEA94FF74F91A8980FCF2CF1B6FBCB172DAF478E7761D679CE0F8BC9EE6CD58BE7A9F12DBE14990523C3D18BE9440062DE0B9282282D5370A3A3B9F4E7921E6065F785B783F614EFC962D3BCD5BF18733E910A2FDEBCA4FB05908E00F6792607B19B4E8749260FB25D8A3A7F9493194030040743C94CED008EFD7435AADC626A8CBDAEA6D000BE8062DDFD729E0B8378EFB68EFD32777EFDC993861465DEDF7D9EBE65DFAC7754F5F855CD6FCB83B54A1A24C643EF3F2A4DFB9DB31FDA519FBF79752A996AF46496185DA1DFDE14C3AEC03D8DC3D946604D46580A00C201E4AC36045B1C69BF765C1198034218014DAC2E03D217C2ED1542D2E83CD60E2FD386301C7EF333DEDEEAC2CFF363CC887EE33F97479D3EC8469C12141EFACFE1D27695A803FF5B9E0C0C6DB756BD7AC3D79F2C2C489936DB22881B453101A07D1436A0AE10A1DD8005933A0E4D2A0C36D3E0510A6A95ECC83CC38078786E35638EEA30860996FA6040587A42E4BBD23941FFDEFABD76A1E5CF8B9E9DF8DC227B23EAAB7FFD417A3DFDDB88D46F3B6C3A804DAE83064F65F743C2C9082C01F42A55029D1FB42BFBA103E01D81761D79870DC1102001C3B76CCAE4F353DB22755350DB5B5F5C27B0FDF58F6565F1FB1A3A3472AEBFBF172F38DE687E72B9B53FF2397C1603AB3B37428CD82BA2C280DD31EF4AD52CEB32D2AE3B837240058B56A955D9F6A7EA9E631BD48F171B14FFB1435BCA6B933E75EFCB952A942C45DFDE2AEA79FEFCF9B3FFF377677C71F42A56031C74D6AE89A1268A3C3127F68D18552A3EA12D87E17B2F0503AC6717CCE14C18E7AD872558562912F4E090A0D957474C6C546EF3D70B85BD6337D6ACC8DBA2BB3A64F0B098FB2CBE6BE7468FB095A0C9D2F3A0242BACD47CDE27A284D824AADE3EE4B07A837D06CA9855BAAA25BD7603EC07C001003F7A4B60C0000EB8E1C292A2AB277EC382E65FDFAF5FA7F3AEEA30989F3BE69FA452AEB09E8EDF56606D268D4A0B0C96B248F3B1E5FEF952BC4D27BC7BFFCCBEA0DBB8326870E61880EA5DAB48E92539A99F8E65370261D32D55229AC2803F03753B5A51656C060F52B3F419AD08C666666A64343C419054A4A4A8C248EFBA88787A73F33502C96F83C689F444088346F22D173CE9CD97985575F5D1077E8F8D955BF5F78E27F8A3FF8708F352B12482BB64D2E81B432338A2DB530ABD6264D9C31CAB09ECD9BC0F4E97CF458206C630606503CBC1032796278C4FCC45099CA0BC3100F42BF87C7283C9F6A890185F26E3751D4437C863AC11A8AA29E9E9E4AA5D209B6C6379E4498E88386D2959E1EE61F3972DC8730958A46F17C3E64726DFD4D8F869B7133A71109D029968A3A4574BA74DDCA38121214C89AE0B07DA773574A4208A479E1E04572C233A30303288D461A18500DDFD438E7190A77BB0877A510CD32AFE0B88F2A15033EDE341542CC589EF6F597271F8925AF2C48E435341F2CAE793E88BE6ECD4C5EF3BDD75217396CDFE93CEC21BE1C8E10119502758263F50F0C50683405EA8C983CBE212248189370F50E319AA5F95D7A7A7A48241289442212890882387E0D5FA1E8A779D302274FF266B05E4B5ED8DBDB7BB5BAEE568B10559156AE5C8A20484363A39F5FA09306E20406941899082A158661806FEEB3A9541899080ABD7F769148D4D5D5D5D7D787A2280CE73E9352310098CA93420302044C604D8B8DB971B3B95DF468E0D90033805DCE6DFF70EB3E36DBBE6B4F2300866FEEB719C1E7F3DBDBDB65329942A1C030CCF163BD2F83058C2475D92768D2B4A0B8690B3274DF725E5F6BA5EE486611AD3B72C4E06FD35DE218967630CEB011894400E0EFEFEFE7E707A392BB3CC26FB93068DAD55BE546BA2F95EE4BA5FB6EAC74AE65E181C5BE0B0F09473FE6B968D3A7B7B7B7BFBF5FA954BAE43D252A15AA54F43AD7A633C15CB9A3850716A743994C2E91C925F551FC4AA71A8FD8F4A3ECF2860857753E66CADC3A5EC3A839A8A193AA542AFDF832BEF2423100C3C03A0C53DA53FE4184AD75F151E118600010BE697DB8D3DA1A1976EDCCFFE8CFEFC7C54D1FF9A6ADEF27BBE328F7FBE23F6F5B9E93B3F2E8E7EF5D3AB7E5DEED8B4AE5B37EB9B4EAE72F6AAB4EF8FA7905B298F535271AEB2F1855542A15F6B6E57C5C1A4717BF9E59FBE1FA43423D6165AEDFC2C3778CCA95B97E0B0F5F3CF0AA1F95E9477D55A36F5198FB9F0B997E1B2F5AA89E7B11848716320D6A017647F32DD36FE345433B162319C089D243BB77E58F4A34B5EEA476FBE8A2A4E5DB3FFE7AFECBF3FF97C7FBFA9BF3CD0DA7CB8EE55CFBE5805CD6E4ED4D7EF0A0B3B95938A0C0B8E547654FC4BA5AE2CEB6E3C73EB7B72DA7A3D91DAEDA96EC93362D3B1B1BE047DDAC3B1BD56F5157869A1D7BE1B0542EBEBE17B6AF3D22B426BCF5C29762E9C124B3D5BF5D53924E7D07BE144BE5E26FD7D46D2FB8840160959B679C5E765D2E96CAC5DFC267EA7358AD1DCB6E024113279C283DB467573EAFAE61849DD4AA8BE279A14E2662C345B9F8FADE5B6F52375FB4A2367BE7D14DE10010BEE9833FD4F085D684CB924D1F2ED46A2E7E3D53A7B0F8F54CB8C1BF0370A7F516D4EC98490DA05303DEFCAAEEB6D0B21D63346EBA3B9FC76BB063D02E66DCE5855AFF97B5CB0E66C95AF8A6437B4ECF395F99BFD84CA3984141C8BF09F03B5B8466AB5B2AAF39293DF8CAA0A4D254CD126A375DBEE2DD6D1F8DCEB9A9298ECFEBD579A1498B38142F22C5D38341A7043268139E8B2222487DA3A0B5F5C96416FB36BFF31CB7263A7AAAC5BC50C315CC0617C4D15F7346B7CE8E8922985B06472D32BB680D06AEBC655279E088505D16FE78B6665664048645B0E36B6E0BD4DF7E5FA26B1D6ABEAB1062186042EE77B56B384956847AF6C1A460B61C1615035F7D764868D0B7A106AEEFBF6A37FDEBEE7C5E5DC308DD6DB2EA698EFBA82E2FF44E5BCFDB19F3100F99362FB45FA1A24C64926DCD0BD5BD4C995FD09462B222A3594D2EA424160A0C1774C0306E6C6EA4C63513B262CD2D5A83B976CE14C58FA3B218541623F6E329E7CEBF13814144F69635C733A82C0695751E56AAFB0000303BE6F65A1683CA8AFB30A6ECE06FAD0935554CC32766B1BCE433DE5EECA3581683CA6250593995466A164E470D786E42E0F1BFEDDFB3279F37325328AB4EEAF87D26755E68D2CB33053E934F97372D7E651A52D79A9A14AF00D2CD16118D426E6CAE5BBB666DEEE64F6C4DBB63E754F12131B35060FC90AB099CD4AC94737CA838970B057CDD0A7D9CA3FC82C4CC72C1520088D9B20322F32A724CDEE0ECC26B4FB0244F22CF336A28E96087E4A04654302867BF77B9A3C0B84B26C2257992252665B342C372D8A6F3924DFA5DD5531B1A954AA552A958AC80AFBEF86CCD1F3FD8BAFDFD993347F3A0EF6679A1ECA8581BD6431214EE2C4E888914B436E9167C32ADCE39CA85146B5119C71C6A0745511445D1C000FFA283BB3FDD937FFDFA684EA1C6545EA8763DBEC8B20C5B1638E56C2968DA59A82F71EDB17E2C6F6AF41D54A954A2281A10E0BF3FFFE34FF7E4F3AEBBF2A06F35C013601879A1342FD2BCF8D8D81742BAC58FE6CE9CEBE941D1E5856EDBBACB91BC50416B53424CA4A56F75E7A36A07D55BCCC97C75764E498671D6C8084D02AC6D4BFEABEB7256A82DC291DBC09C832A954AA552C96432F2FEBA75EFEE7C97B66E05B7CA0BD52CF2C96657C456EF2C17E4E4E8960E8BDDC18656137DCE96829D9199854B3531B5223B32170AF86CCD9BA00000D8393B2E15DD53973D48C8000A0862EB69D97843E7A0EDED0F0303994AA532FDAD0D23D02E81800CA040265A547083BCD0EADC4824576DB2808FE5B001807394DF9AA895424201BF8A0302531FD5CCB2748A595CAC8A0386F9F91C004D6A72900F7AAF1B09A1133CC94E783290001E6422601E9677EDD802019D83C6CD4E2E3AFCE96F17CD2312913F66AF4E4E4E7269CB0A14EE4B61A2370A60FE7719D61B627F3871D087420C0B0D99F47C3091E60D00A27BF7F20AF37579A16D0FBC87C80B753D454545EADCE5018552282175F6129F299D10487F653977EB38731E08ABDBDB1FCE884FFEF85069D1EE6D572A4B44A2CEB7566DD9F78D6B279E1E4498404323FC3539772525257D7D7DC1C1C1313131C1C1C1341A6D1CE5857A9049311320069C958184000C38C9D4E8E34982F6F687B3E624737F28899FF5D295BF075DBFDE3475EA0B53D841A8F0620AE795A14D0C0B04C0E27BE81DBFF6A4CB0B6D6BEFA86FB8F94CD6A3E8963C68E18B3A45037D37B579A116E73F386E4574147BD69CE41FBE2B899F351D00FEB4E5DDAD1FED4151F44F1FACDFB9AB60C8EA2E655CE4859ABEFA02C7888CF4C519E98B9B6F3536DF6A544B3CC8C48E8E474C2643267B32BA3BD0711F55E7857A3198547AC06BC90BAF56D55CADAEBBD572579B172A6A686C5CB16AF4F3428D5E1ED4D3D3231289F87CBE4824EAEDED55A9F00479F3A4A526BDFDFB0DCF874C7A236D715F5FDF4836EDE3E343A150C864B2FA318C61C551A3BC50EE859FDB3B65EABCD0BF9FAC75CFBC50128944A552994C2600F4F7F70F67CAF8ABE740E127A3D22E8542613299542A954824C2385CD356A150F4F5F5C96432B95CAECEEA1AED1EE118432693A954AAAFAF2F8542219148E3CE47D557AA150A058AA2E36DEC63050441F4DF5332EE7C543D5EFD4F1C7743BDEAB1EEF3FF0172302F9AB1CDBAE50000000049454E44AE426082</data>
      </image>
      <text></text>
    </paragraph>
  </paragraphlayout>
</richtext>

"""

TxtRacineObjectif = """<?xml version="1.0" encoding="UTF-8"?>
<richtext version="1.0.0.0" xmlns="http://www.wxwidgets.org">
  <paragraphlayout textcolor="#000000" fontsize="8" fontstyle="90" fontweight="90" fontunderlined="0" fontface="MS Shell Dlg 2" alignment="1" parspacingafter="10" parspacingbefore="0" linespacing="10">
    <paragraph fontweight="92" alignment="1" parspacingafter="20" parspacingbefore="0">
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">"Utilisation de la branche "</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">Objectifs</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text></text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"S&#233;lectionner les "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">objectifs p&#233;dagogiques</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" de la s&#233;quence dans les branches "</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">Comp&#233;tences</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" et "</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">Savoirs</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text></text>
    </paragraph>
    <paragraph leftindent="200" leftsubindent="0">
      <image imagetype="15">
        <data>89504E470D0A1A0A0000000D494844520000008D0000004308020000002EDE11360000000373424954080808DBE14FE00000122849444154789CED9C7B549357B6C0F797374980105E824840C24B5E2AA210159D8ADA206DAD43B177B47ADBCE24B65D6B46BCD3C7EDD435B476B5D3C700B5BDB30AEBDEDE8B635B454A4129B1208858A1167C40948709EFA7BC122024401EE7FE910721094A22E858F25B2CD69773F6397B9FB3B3BF73BEEF6CC01042F0C06018F6E09DD8B907847B575FCEFF1E69D4F1C9C9F7ED283A6B01FC6DC722D7F8D87DFC8423E091C61E2B8F9E7BF9A9A6AC7CEA4229A652FD4C22ADD9B68D4C263F34B3EC9880B3587A3127A72196337AE9A2CA89A172751B170A1B13765CF8E8E30559CCECD880A99F2627274BDF7D5775F326ABAC34EECDB7F02B7CB0655EB1AFBEBAAAAC54A356971D39323E3EFE480C5DE2602621529A99A95128225E78A1B1B454D9D34BEAED47044CE5B90CE7E818FCF4532DE5E5AA8686ED9F7E6ADA0B86CDB98F60427E02BC9D0B4D0B687500D46E0300A82C83232DD6354DE70198B45A0C0B17946B7C6C563C350B85B44B97A20E1EBC9597E71919F9E43B7FF1FDE36BBE870EEDFCCBDB81BBB84DE78AD8DBB661539397CF9C99ABC79018A8E5E97EF263E6D6CC84FC1408998F8D0649A326E9DBE0441EACCBB6DA4949DBCD9CB4E0CC7F68D6306B1F31F0B74F1CDF78A3ADAECE2522223C3A1A00028283B5557E016CF9468EA8A262DDB1F7BB7625C273CF99F715120327FD617FB6EE8B99CE837C803D16276504F6E45A69A9A10913FC00CA47AC6C0E000045A550644B3B6BB06168F30119713B2E0E2154F2C517A3A3A3C812E73FFADBF4F474E5BFEDEFEDE9362E0780E82C7409A19C33283A4BFF73067548D0BE33A843822E497492396750F40584104212B44F2B838CAAB290B61F2D972EA01C7DC38E56D42141FB8C6A9104FDF5FACCF5BED97A0D1A2F5DD0179A28322AD136DF67E86D6E19E392BF66599239A3B3337AB6A9C6E5D1866B33ABF6591A1168E3E972412186D42AC5249340B8949B4BB859DF18FCCBDA2D5B8844A2C19D2A95AAAEBA9A241657E5E7E34023FCE6DB56365BA3D16CDEB34727C1043F29641B7FCD47A09D016C0060407B1E1C1981901838990025B9B04E02F9090000E9C9F0553614816E9128C9851D290065B0CE108512D8AA5D3C98BA2647F2F4CB0913F293212D1B8A0092B6031B8C1618BD46ED4A96D4024F9829E225437B19EC69D1950040530DACAB01008000A88D86E3A5906E26632809898193DBA1C8928C963F1A0632BBDC18D3E15F800FD6581E11212727C7DFD111D46A3C85E2201D95E27008074A85C242E469107E5A89341A8A543249A76B54AAF96ED2A550320200D0D4029D6B8CD433C10F208D07697A413613B602BC3DCFF56304DA01D27800D950546A5923B440E53658196041919FD44C1113F293C157DF4388B98C5149530B74264392C57E0000C08F01E5F71E88F9F0E71E11E1E0C183860FD7BEF847C8E6CDB7150A3716CB389800804020F804B2EB636212F6EE6DF8FCB39843874CB58E403B037630A1C910524CF09382F89EA68214F61B6FB498F0D2BDE56773241B00209D0769A0FB1ADAAE8809F9C9509107C747F411E0A2F7D93D988FCCFCAD02289A6344B3F67B632F1EA8FBECF8B288889E9A1A85420100939393DA0BB55ADD5C59C90C0BBB7CFAF45DCE668B4AB36FC0818499AD4E7A3240DB2C234202C0B7CD683647A09D01BC00238911A880D92500A0BD799AC384F418008023D970420A2B99966402205E0A252D161469BF553AABB485FA28D495B440A55EC6DC60DD58CC65F4B44BE1893906A2EBDF7CF8738F68D67EEF372F1CF82939794A2E27321857BEFEDA352464A8AE1E30CC337AEDF09D3B0098078B75F7A34F56E559DED034D5C07E80933CDDC74AFD5D1B18FA4229EC9FDDF4481EE427EB1E86B4B5C72FCC94681F8FBE6A83341EBCD466A66F0420196AD7000074DE803DC64B2363C68CB46C68B2A4E84819D426C30180CE36E8048011F84AA26BA52B8119196D2B1383D3B22DCB68311E08480146E0ED1B70920769C6FD9B5935D7884C9F733BDBDA5ADF7B9FFABBE73DFCFDFBC5E2B1F272BC4AE5B06D1B73C50A8D5A33F8D971E6AB8722D6AF3799B17B3DE75A24006AA34D437EC158A427EB95B0AED4269907B6C7C2FB725F7F7FC2B1779BFF9AD63B2123FE81475CBD1AC3309A9B5B775616B5B767F9071FB243436D55A7239D07F10027F2FE759FFF0D246D87347FDDB5367A6C9379704CE3C940FDD5AB835F7FE355554D54A97A62D63A243FB761E7CE397BB1369EEC58C3BDCE9F22376C800D1B7E16089046B375D7AE8769961D73EE734EA85228905AF3704CB1730F2C9F3F19408021FB71EEBF0073AE4FD6F562CF63596416C64F76169BFBAC4F0F4ED9F9EFA7E4A3EBE393DCDCDC165BD7AF98FBAC4FF3A1A7A74728BCDDD9D9695E353838C859D6CC500ADBDB5A1F5CD1526601E2E9F265218311D2DA3A2A125D1C1B534E4F6BA854E4E14AF5F05AD158571DCE98B839E4FFEA5ED3571876ACC2F6782A2E2EFBF6DBC2AEAE6E0A65B9A7A7DF850BDF3118CE48E3E6B7F2494F108753AB19C3795BFD7A98CE3417B2ACEEE6F5D1D1D105B47BA961E33EA2A9A9A9AB8B49243A90482422918CC74349C9E7E1E1C18E4E1B26A49D3B02046A0D8180576300381C06180618E4944A0EBEF6FE820F608960633C0507070F0F5F3C77EE231A8DAC524D8F2B3AE3B7FCBB97D70E0AC59940205C685E77A99D333C86536B3495D7BB84A2C18989A901A97A614D9F03011FC3F88287A2EA2162A39F300C7BFEF9BDF1F1BF9B9E82294CC80CA8E9939463000A696338B3C28BDEE143EFF07082B317EF0C92B7F411B7E6542813B866A92F023E666081A656C04F846294C505000071268793799F83CAC704DBD7A7B3670B1186C6C6648097F677A85DA81C35023AD6EC4E1F0FF51A22384EDF52B0C2D89E30D9A790B6A7BCF0DA9AB56B8D9B8B3339582214EBB3368AA160411CC5CDD23BE9D785ED7E62AC1C8DE6B6B8857DEF153434DCE340A5D264E303AE3409E0F06AC0397804D29D1801BEAEBF8D5638A9BB2412C9ECD6E2A25CC810CD4C29372B8B0B5AEF19C5973893C3E1F339DACFBA3ABE6056F94C28CEB4D5069138F3406A75756AA0F6B349AD3893C3C9CCE49B04F34C80EBB4CCEAD0BCE0E161A39F7E38FF1D2BD055A504860B8342A66D7A0A61AEA7718E25F8E521BDA4A821B507A826B1811B1AE5A45C31F54B8BD2DFDF7F567B71516E7544B0E971BA801F981A518C1042A20C61A276F2AA85A127102AE665271E00EDC5B14CB1A11C69ABF80210F0031B8F6A635394927B20530CECC32732E2E2324408551D1699D50254A736EED6F7704CEBC99900CFE29A7528CE3CA0B30E1547348A6C9B385BC101404E4E8E55BF01A0A3EFCE579F9F958DC901C3C646651289DCCBC7DD67D9325F168BC50E59B13AC19BC56204C58FD2C345131EBEEC350482D9835A5C68A04989B8591897F13A1700809D9412975D200080B89424364060689CE142D73C2549EB66EE6E1E089B05CD42C84ED47ED90353ABAB67CFA3D852AD5E97AE4F71512EE84B2C36610747407622C61718A2FF218203006DCAD1FC7FD75EFB25D47FFD9BAF66B48BFB27E5D3EE443FE2A86B8F48EAC5F4055021A441681A8FC73BBB7BB907ACBD523794949464AA961D1C519D5BB4B0F78EB80CD14C9EA4D93CDEBB765E1D72B310426877C1026E7BE68DD5F7BDE191E10962A392DA22A8FCBFA818B64AA5EEE9EF53AAD4B1614F3838902727A764B209C3E0542A6577CFB8A3A3A35937DCD73320357066B4023E5FC00E8EA84EFD4400A0BD2FF276CF6B360505D9712949DC99B6B3D0860E7B8E5A63D84929602463DE449CC9CF140370B39028234ED8FC701728ABDF1BD50B6F4E3A8CB1562EA3453A00863939539D5CA0B5B913D02AD984FCCB2F4F4BA593BB76C57138EB007025253F3EF3CC33FDFDFD9E9E9E26671FECC35522E0041A0A79C508B85C5186BE88578CB8206E9ED38EEAD4402C55DFF2301B206BA62D405C86A8EA309B7DF8280F4BC4B2E332445526B527CC7B641F3E3123C32B46661D06835E675C86A8CA72AEDA6261F5FB88BEBEBE2B55971B9A6FEE7D25A6AEB6D9C9991EBED64FDE4B0CF28D6C6D6DB976AD77D7AEA49B374B399C6884A0BCFCB29393EBB452E948F7898C8C5A30ABC5999C0370A2EAF0C39DAB4789D5F73D2F2FAFE4DFA68485868F4A6517F3DB87458C770EFDF3A7B2DB03037D77EEB41108849696ABB1B15108E10A0A7F3C7DBAACA7B79B46C57774742C86F54B075BDEEF89C4777AE5D57892D203171F1414040062B1B8A0B090E5EB1B1E1E8EC30DB158CB944A5546E6D747DF39D6D0D0505151B17FFF7E6767E745B07FA9608B9F060707F3CEE674B4757FF05E3A0E671A91050505EDED4D542A81E517B173C79CA96476ACC2C6F7E5E3E3E3643299442259AC9D9898E8EAEAF2F3F3A350280F669E1D1DF6FC88C783053877B7F310B0FBE9F1C0F6FC088944323830D0D7D3D32CACEF6B6874C2E3BCC32302A2567BF82CF765B116D0443B60C3FAF46371F1687FFFDDB6B689EE6E4D773713A115343A09E1FA4627869432823B8914B6921214C65A1E3A255338BB7BC46DDAB448A62F29AC8EA7EACA4A545F1F46A512E5720A85D23321BFD4D745F1C27BC4389318AE4A0DDE9DAA76E911894B2B1AEECA3AA4637F3F73C6F450C38EF5E0D3D2D2AC6AB03521A16E60A0ACBE5E4EA1F44A247D1269A37448E1A602B99AD4A556764CD7D4F4DCEE94FB466DD8BAE7D96BD7AFBBB258A10FFC275376AC8EA79191112A8D76F0ADB7BC69B4B2F3E787AF5F77EE27923AA76E8D8F832B6579907FF0FA001F6F2F2F1F1FA452C2A4028FC72F86DD4B0DABD7A73778BC6D3E3E3BFFE3CF88EA201F1F6F6F6A2AF9E187FFFDE6D4B34F3FE5EFB39C3E34D45A5343DDB8D1CBD1E9DCF785381797FF29CCB7FF95C08363B59FBABABA7E3C750ADD6E8CF9CD36F78DB13817C6505FDFCDDA5A697FBFB4BB7BA7541AEEE0B0EFCACF1D03FDECE50E113B1313F7FE3E2A6AB585F35C71262730B51A00F4A710B698BF645E9CDBF23EA2BEBEBEE0C3579CC79438A710F7F070FF78CE8D86DB6D57AF9224D21422B17D6C4C30264AD9EE1FECEB30363659D520BF3C483DFCDEA7919191467D08F8D8B1509D77047C3E3CF483ECC70CAB9F733B3A3A8E1F3F49A6382425D0DDE9CDB53F9C3AFF717A5B71C9647B47BFA899BECCAB97A8D81AE50C6A796E79D747E7FAF25AB1A70EBEA27DAD3E1B431E8B59AE91212568E6785BC0376420992624658A6792872CA609FD1AB0DA4F2C162B322AE8EA504059DDF8DE277D5FD9BB0C48AD2D77EF08FB6FAF7427F969A06F5CF65D33FAC775A73A88A2ADDC14B53A7A5548B0D96B75EE6E5E76E2EC3C03F6E12A7D325F44EA2702601F3ECACBD665F5090AB279BBB9161392B4E89287B2B88F342B68F1B03ADF4826934D4D4A99DE2155D3DCE3053D52893C617FFC9F5F8EE26FF127531C7F143513DC563EFFD21B1FBFFBFE5B87FE10E6EF3DDD74E5931713BFFCAF2F4C146B9342666585180221311B84CD62AD330B040020281066BCCEB59C90A4C5903CF448B382160FABF38DCE9E2DEEEE1EA391EF7AFAAFBDA6DAFE9FDFB59754B6467B394835A416826B09C5C16F63AC1F83525B2938F5E5B1CA1F4EF613DD625F7C73D7D3CF58D6CFCD42A898975D20106772027353B4093EA20C5DF217F7F50C6181000405427D16D8FD799459418B87D5F7BDD5AB23542A487A6A27111BEE1AE80ADEB202A8D327CE5575750D601455C81AB6ACBFF1BFBF78FFD4F7FF3CF9D3CD9F3A71648A9B2FCB3F2060F6BFFA1167720C73286E166A73F9F42979E2A2DC6A5D1D3B294558C0D7BB693E09498F342B68F1B0FA3977D5AAD09090155353F875EBBC6B6A48743A2734CCBD28B75A357ED79F36DD206CAEEF92DF9D74090E8A58E90C4323EADBADBDD72ACA49442267F3E699734576528A70562E0F9B0D4723306D3A4F1C8F17074682A98D47912EA732EBBE0949EC479915B478D8B22FBF75EB7661E195975F7EF6B3CF72AE5DEF2710288057B5B55DEFECB8E5EDCD5A1514E6EA48A139903DDC9CFAFBBB2ED5DC4E58BF6A53F46AA95AF3FB3FFD6931C6B014B03A9E341A4D7878586969F5E8A8F299DD9B2F57BC11BB3A92C9A0EFDDFAA41BF37940D318861C69746767171767465BF7C0AD96212A85A2D120174FCFC518C012C1C6F3A78D1BA35A5AEEB258B4E51E0E2E5482B7BB87A7C77226D31D015EA5464A35AEEDAEEC62EDAD2BD76E78BA79F8797BBAAD5AF544C21CFF7CD3CE3CB03D3FE2C30FB3A2A2365FAEA8181D9549C646C7650A84109D46A753A92422413EDE2F974B1D28449627E5C9E7F66CDC1CBFB0762F356C3FCF2510644585674878DC946CD09988BCBD08642246C0C988F8710A11E7B89C4622B91048A4908DF1EB636317D0E2A589EDF1343C3C7CAE201F1062B8B850A934BAA3139942A69029443259D4D878B7B515D49AF04D9BD6C76E58588B9726F6BCB0C7037BBED1E3C1FF035B1E1F91C7CCE33B0000000049454E44AE426082</data>
      </image>
      <text></text>
    </paragraph>
  </paragraphlayout>
</richtext>

"""

TxtRacineSysteme = """<?xml version="1.0" encoding="UTF-8"?>
<richtext version="1.0.0.0" xmlns="http://www.wxwidgets.org">
  <paragraphlayout textcolor="#000000" fontsize="8" fontstyle="90" fontweight="90" fontunderlined="0" fontface="MS Shell Dlg 2" alignment="1" parspacingafter="10" parspacingbefore="0" linespacing="10">
    <paragraph fontweight="92" alignment="1" parspacingafter="20" parspacingbefore="0">
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">"Utilisation de la branche "</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">Syst&#232;mes</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">ajouter</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" un "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">syst&#232;me</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" ou un "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">autre mat&#233;riel</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" : faire un "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">clic-droit</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" sur la branche "</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">Syst&#232;mes et mat&#233;riels</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">.</text>
      <text fontsize="10" fontface="Tahoma"></text>
    </paragraph>
    <paragraph leftindent="200" leftsubindent="0">
      <image imagetype="15">
        <data>89504E470D0A1A0A0000000D494844520000015A000000430802000000529D5AC60000000373424954080808DBE14FE000000F1649444154789CED9D7F5014679AC7BFC30CB20CA70E3384C8AEBA30A341C9B91B01A752B5775BAE6186443D238958755559C2B15B13268A8BE44C8239B7B8CD0ABA2812508678159625A9AD2D51703D8CCB8C712DB7AE2A351948AE92502ACEE0E652616F8FC58E9683420F7D7F74CFEF9E1FE8C030E4F9D45BDAF3F6F33EEFB7DFE97EFA797BBA1B09C7712008820092E22D802088F9828CFF4F2291C457C78281B22D22719179960ADEA6FDF861197889A22A91C0D064812008010A07044108C4381C6CD5C1A68BADCBB9A0C980264D74A64AF4ECC49AD9954310F1C13F1C28D16380CD009B013D1BA273E07F78F4595087A80FAD07E3210FC8A0E65B75C007A8B1C7B41782484064BE1F9A76E0F269B48C0340D3839EE4FB2CE87B68597389B8E0713C776AEEB510443C91F03F8C49249282B7B926032E9DF43B36F6EC44F68070E66C32E0E6699835786F3D0080C10BA7A0DF893205007CF1319EB3A36707560200BA4EA305E829C24DE0870A5CF900370B50A6C015FE3CACF4B71CC79A0D7E6EAF7A140459EEF1EDF123B74D888EBC6E459B8B09BE7C0BCEFEF6980E3241CC2F2A2B2B45EBBDD94155CA6F2E8DBC586740DD080A2D4265CB006C6AC00E68F0C311D4003DEB5177127DC0561D56012D17B1B108FB4FE12AD06440071F4D94E82982F922A0C0CDD3A84987ED29DC3C8DC274D80AB0C60EC38E40CB7A7FB79E70D0146079CAAF472F213ABAFA110AF990A181AD002D96C882B3073004949595C572F80962DED0D5D5156A95371CB4DE7F117CDAAC81CD00F041C18E2B4F612B0035AE388071DC04EA0CC049F459FC3D29910DD41950E7AE58058081791C00BEF02C885A86722BE6D32F0A7810ED087EC90518AC815FDE212AF8A41DFF20DA05412C746422757614DAD164C056A00FB834824D1A2007972C00507312009A0CA883703EF71294E75784EA36C012E80BE536C8720628D1E3B91AA2444F512419418227A7D8915BD2D13BD2FBAE0753E087CBE54A494961593606BE08226A52A4C85AECCA56B0298B92C35BFA8403257A0AF09C4558CE66700300D037808A1DC0C74252DDA441CD47A839893D3BA15602001458055C1DC74D050C9AA04BF4C1045B06BB1D0F61099F1E230E03BC59C31A8D3B479889E01146264992FD408D6FC96270BBE1E4A42B2D4D363939FDF0AE08227AEEBB30F2B7A411066B322358FA8483715C4E87CD207CEA3AED3EDEC6719901ECC23276C0B61EE02FC58D0340C708EA0CA8F818CF9D46CF0ED89E02003078E162C85E6B022C4F89B80D657975DCA7C78FC26EDC383A6EE13D03007C31E29E3E8CCF40F05777A4FFA8964825D353AE181CC3F7262753D3D2A65CB1C83408226AA412498E2AE94F0EE99A4C6137BE73E78E4C2693C96452A9542291781E59F2FB6541DC9906B68287C8D813909F4EB7F39712FBAF273DBD56CAB2B13980272626D2D3D327262662E28D20A2472693F65F9D2E7E6C1A405757D7A64D9BE472F992254B525353653299271C885D3BF067AB1A5706BE41B12098583DDAC5B90B41C497E1E161954AB57CF9724F82C0D7470E0709775B51ECA178402C2C464747012895CAA54B97FAD67BC3013D9CEBE1A72693673986C76F986860D923DF89B3B75AF4C2677BAB7EFD99ED1F5F7E79566FF78E07963DF2C6DC4FCDBB16DC86CD6F02F6BABB77EFDEBB778F65598EE37CDFD0213CB3C0113E040C2487592EF6D65F7D5EF1E2E7F56D76778DA6AAFFF665A366467ECCD54B367A3DCC9712A8AAA8C5D98E63F34FE7022FE0FC76EAE9E969915D3D9AC9C2371C0E88D5FB8D384E28018C5C38839277AAF093CA0BF6CA873B6DC6506D0C095095FDF2DE62C77CD4B9808972B0E97D079198F5ECC07EA117CF3EA3C97EE679F4BE6F172ACD7B976E6C73800338476BF152B96AA95CB554BED712B4565836EF5DBAFD37B0FEDB7AB9EA6766FF56BB2D6EB3BD3FDBE8FE18CA8F7BE1C46EBEC7E213F600B56D451E31F6B6228F247096DDAAA256BB9F412855EB0AD77B55B55904A97B2DB09FD818D86FE086F895C71F7FD236F049DCCFBDF3BF808B6A67A7701001612867AFD8DFFF3D9E2FCE0172363F8B33FDEE7820F4CD996BD6BF96D7ED1C639C63838787766C34D97DD77A96F54DCCD93268DF1C748E35EBC1996BD69F7976D039C638C7BA71E4841D1C00EBD063EF8C31C78BB880B641CBB01EB8BE6D8C718E7557D8F61FBBE86B6F3E76E0F1B3638C738C713615698CAF5674F599F95517FB3ACA5EAD52FB1944A5EAC061B431CEB1EE8AAE1DF297F18E7FBF624DFCF5D7FFF2E880ED93F81F70F3BB70D1EDED140EE28CE30F6750B2590D009AE2121C6831FBAFBE36848ACDFCC3E6EAAA7F2DB70E47BCE95368653D902FCF50C8334A3B6CD7F936DA679F8E7226A27D738F1E0074DBCAF0D9B0C3678D26B7B073FBD36D6E11BA6D659DE72E0280F9FDCF0FEFD6051944A1EACDB7ABD4425F6E859E7EC59BF8F1DBF74ED41F3C3A30F049749B468483C2416466336A9B8FEFB7DAF6AFCB50C8331472ED7E2B3ACF5D84379673FE1A665259F13BC6F97F7C69D607ACE582DA46742E1475D505C679023FC950C86B2CE0A0DF55FFD99136BBBDAD7EA864738E88C10C54851013D82440FFB7B31EE52302CD1AC29428A17010010EDE4B80B12FE6735D1B0E7F78CBF957A17CFA8B0D1DE7CDE03877BF39B96BE1AEB1B71EE9AC78A6081CA759B5C17AFD86DB8347A1672127772D3A8E9CB0FBF525B22191FC88B7428EF1F28707B543D7ED1C879CE2E7D17BEC782FB6156B440D66A02A7859B4894FE1F7743E22341C3C3A60FB6416BFAC842ED1EDED140E2220EC9AB3533E38DF51B07D738EB746A3DFAE7DF7BCD9F3E571D01F19383CB4539E992ECF2C38B36DE0F8268083E6A57D15EFF295E7F163B7E5E617AD3F2F9067569BF956DC1BEB32D3E599E97C8DC7A16F11F5E36719D8CAB29BF7F9E41B7FFFCACB1A0EE0D455AFE475BC9BB7FF25B5A8C10C54892D8B34113DE9093942FDD101CA11448BEF60854612FCDB23D1DEEE7D66E1A9C7A4F726E7FE9905F33EE5B967C68F6F8A49C7B3CCA5BDF20B5B9C8DC1CF8FCF3E4FAC7B72F4CBFFF67CFC6AF47FFFF9855DAFEF7F253FFF8938A899C77C6B91F4D2B0F79985898989152B56AC5DBB76C58A1569696952A99437A3EC605E72F1DCBB85B9EA78AB888A91D6A39F1FDE158F5810CCB2471F79AFF3AD43F5470707E9CAE28340E12002B33A59102923AD5B94F2653B3FAB7BBBEABB71CF3023147BBB5EBEACE0CC3FC54FAA2FD3D3D3D3D3D39999191DFF71E450FDD181419A35F8144E7CF70E80EE4A8C4CACA653DE0B6061C8AEFACFBF55C5B6DF594363E877F2EFC788BB543E16B85C2E97CBF54886B2FDF8C1CA5D6FBC4AB3861942D9413816C924932ED09FB39DE7F8C60296655D2E574686F2ADA69FFF8A660D0080A424C9A40BC9D2C896941D84E3DB8B5D7FBE2559A9484A498E414848C2A26429B845517C2D449448446201CBB22CCBAA54E98D875E7F6DFFA19EB3BF8DB7CA3833E5C2170CB2FECE0544D88D291C842347C1DAC761FB1FE97D36062F4773B99092C2B2B17045F04CB2F0C4822FBFFCEA9147542CCBEAB61B7D6D2EDFF8A60FF822291E4D73A9952C10FDAB538920922458AD6257AB62F3EEE3AF6FDF5EB17CF9D75FDF8D893702408A0C9E5850A02D6E6F3BBCE9473F50A6722F197EFC74F18FDC56F7E32931A1A06B074462E38905677B7EDD70A89565D943F5B56FFEF258BC752524140E88C4C6130B0A0BBEBF72E57706073F552A152B577EE70FFD7F8CB7B4C483C20191C0E43EA6F1C40200AFD454BEFE46BDCBE57A6D9FF160FD5BF1569778D0B503228139DBF36BDF8F8505DFCFC95EF997BFFC55A54A4F4EA67D7BC6D090110B8A6347FF7DFBF3FF5258F044F3B15FC45B4BE24193857863A95608545B425AE84D0EF175E17098F40FD630063CA8665F1E48FFB265991FFED7F9E32D07BFB72E2FA4348542A13739C2F917D31FCFF19C23283B882B0E93BE14DD0CA303E030992CD0E91ED2A3A55AD1983B6836AA01B5D1CC1823B798B7CC8A7E4B7569677937D3AC038099F94FF4F18C020A0771C57ECDAACD15DE58A6361A13E319C644C733E244203459882BBA2DE5D6DACA8004D461D2879A3E88ACF2ADB2542B4A3B61ADCDE7D7FB64BC5E2B4F4B4BB5426F32095315B79D686570BF966A85BEBA5A1FA8D06DA637DD08ADD952ADD09B2C1E4B9F7E1DF05FF62C841A91D0AD823741B011C6476F72F83717EBC21E5A64E801412243E120BEE89A99C192DE7CBFA334BFB76490611886E94663C0DE1CB8CA61D27BAA98669DAE99E92E87B6619011B2616FC3DABC6E86611866B061A8D4730C586BAF6D611886E92EB7D6B6B88F82E04A5149D6A1DC76FF6EBCBDB4A3B733A46600D6DA46B4330C33D880A0602882A5C5ADDE7FB34222BA5DFC680BE363F6CBC40286D1ED841719E824C28044A36FDE42E120EEA88D66FE2855545B00C78D21FEF4AE50284A3BADD77CDE1D1CBCCAD1DF6B2DDF17718EE1B83184F22DC2EB988DFBCA3D5EB50D7B7400A0DB528EA11B8E1095E292B425C5EAC05EDC4DD5C67DE5A134F35DB41BD5816242A3C9D57696CEE4229EE87685467C18DD22839D44392009088583F981DAD8DEA0ED3CCF9F84CA8553A1C8D930CCAA59E561FA0DD3D67163280A076AA39961DA5119E6D79739275E5FC4EC42E120AE584C9EB96B7FAF559BAB817A551E3A1B45CF84C1ABD4C525DA10C6410D8550E3303576BA338528092329C0CC9D553B4C8D9DE1DA5A7BFB1D80705ADEA203A0C9D5BACFB296F39DA2EE8DE6C106ADFF693A72ABA8887218BDF6D10D480242E120AEE8565DE3734E457E6D5EB7D9A80674CD830D1032D180B361F02AB5D1DC9DE7AEA9B640B838992FD270A894EFA7B76470A6A7B33092FCCDBACB3B4B150A85A21225E5E1DA6AF3AE55BA37BAD933BDE0DB2ACEA33CC0B1FBD68CFCDA3CFF943E6CAB19103C8CE1897240120F7A93B2089E3729B36C6C1E6DE6713FE0FC750C7D26203E774610734B727232E84DCA044144038503822004E8AE44628ED135330BE752FC0283B203822004281C10042140E180200801BA76100E992C96E3A3522A9D4E27FF630F41CC43283B20084280B20371BABABAE22D8120E61ABA2B313277EEDC191D1D1D1E1E1E1D1DBD7BF7EEF4F437FDAFFA1089CEE2C58BB3B2B256AF5E9D9595959696969424CC12283B888C4C2693CBE52A950AC0BD7BF7288012894E6A6AAA4AA592CBE59EDB9379283B88CCD4D4D4C4C4C4EDDBB79D4E27CBB2346244A2939C9C2C97CB972C59929A9A2A93C924EE3F524EE12032FC1F059D9A9A72B95C345CC402402291C86432994C26954A251209858319C00F91EFBF0491D0F0C7BFEFBF423DEDDF0441F0D07D070441085038200842E0FF0182B1DAD149FDDF370000000049454E44AE426082</data>
      </image>
      <text></text>
    </paragraph>
    <paragraph>
      <text></text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">supprimer</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" un "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">syst&#232;me</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" : faire un "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">clic-droit</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" sur le syst&#232;me ou autre mat&#233;riel &#224; supprimer."</text>
      <text fontsize="10" fontface="Tahoma"></text>
    </paragraph>
    <paragraph leftindent="200" leftsubindent="0">
      <image imagetype="15" fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">
        <data>89504E470D0A1A0A0000000D494844520000012400000052080200000072973ED30000000373424954080808DBE14FE00000111A49444154789CED9D7D5014679EC7BFCDCCA00C018619546095E80C2F925237025171BD8D31820B52063DA42E55463C363548A22E12BD042DAFC8E6A2716380D535BC54D61862ED6EF942F40AE1648C5A9E97A490979CDEB131C30CAE6FB839C4090406986EFAFE98179BA1E7056986019E4F754DF53CFD7B7ECF6FBAFBDBBFA79FE9178A6559100884B1C7472847B5391495532B94374F3192A85B4B962F2F691DDB78089319ABD85A4B965316DCDDA386EE7C29E56C0D52C7566EA3DCDD8755AFCD49450D5B9E22682B048203C40080DA9CA893995AF6AB4800B539395A20F2297CA594B329AEADBC08FE8023F3BEFACAF3B110A6002CCBB26C8D1AEA1A968BB638D15654A34662B196D516275AEAB8FAC66A8B1313D5EA440050D7589659BCD959F2147043E02EE03374DCD0136BDEEA3C011717ABAD6E781BB4963B0C9840700A58963D7EFC788D1A1C41B02CCB11A07986A3BE1AB5BA867DB2F30DD1AAB9505B9C68DE136BD4B0CD24166BF92D87BAB56F9ED3D09316AD386C88E5F1E42260CEE1C051A8CE0226105C200690959585AC2CB6DC3C5E900A750D5B9E82947475EAD9DAF2149CAD50A79723120BB13395420D5B9E525E3E2439B6DEBA898A0AAAC2FA5DAD452C1233D32201C42626C65A66782D23D3F9DDF2F874D0B5E56D08406BC9F2A89D5F5B6C625B91F2A43A7FC0C5BBB97D4A5E1B0091310ED70381E094A1A39129E52C5BA3AE385B0B0029E9EA8AB3B5B5672BD4E92996652C9B7E96A27806F0862413FB1107A7968EDDBAEF7338AD25CBA34E669AEB733A942373CE6FE3743D10088EF10180D692E5B6DDA6F5D6CDC4D8280040CAEEE29BA9A937CD47FCD6929C925620A59CD51627DEBC651EADFBFAAF5A0091310BBFDEF9A13BFBDD704B5EB74E7C9A5B74074BC6436BF5C9AFEDAABB13B0231B47011308AEF00180C8B4CC9BA99681FFA893999579961E57645A66A2759F8D8CC1CEA821169179FBD415A914B5BC24AA5C5B6C73E0F4AF83147BCBE16E1D5982DBA2AB7D3C326FDF428BDFCD7F5D98682B1C41C07C01F0AE0702C13D28D6C91524B539D47BB1DAAFC81E4520088033B1D5E65067D3477AB6442010F8719AD90804827008766D248140708E785C5AA5286A5CDA9DB8900EC8244048B17577773F7CF8B0ABABCB6834C6C5C549A55227C6F1E564EF7197C61C726C9A0C08203686619A9A9AEEDEBDFBE0C1039AA6E7CE9DAB52A99C2B8D4098828C566CBDBDBDD7AE5DEBEFEF7FE69967DADBDBA3A3A3D3D3D305898C4098648C566C62B178C18205E1E1E1006EDCB871FFFE7D00269349229108101D81308918ED68A4AFAFAF5969008282827A7A7A008844A2D1C645204C3A841CFA5728143D3D3D0CC3F8F878E81F85B424342479A629012852A348E59EA91C5599983FB6E1103C8D90AA98316386C964EAECEC74B7821C556A34A8D1A046D50B6E57E1EC85D51A14C2ED3DD8930C534B5A12F025F2752ECC0893182187FE6532998F8F4F4747C78C1933DCB12FCAC095D338DC0900454F9BA0AA35A87ECAAA1E853FCE4E6C38E9F95808E38390620B0C0C944824E6CC76EFDE3D86619E7DF659E755F4D62C98AF01801D9998DB6839FC17A971FB34EA5438B1180060C0A693485E8D08194EA871A7191B74A8CA400400A0F2340E0355AB711BF8A50C57BFC4ED786C96E1AA3999C8875A72532F67516105AAE5A85A8D3D27F19D79916DDEFA95D7FFFC17AC415AFDEF7015E795C7D83C0F85A7916D6E426E6F43987C0829B6F0F0F0E9D3A71B0C86BEBEBEF4F4F4A0A0A06DDBB6AD5FBFDE91FDA53614AA51D886048DA5E470231A94800E50E1976DC807AA16A3B002D5405A122281C317B1D22A8022358E55A01A1619D45D0464B87D1AF9C1687819B74F2321180DF198AF833A63A8A54D3F4051066E7F890D66C124A1BAD1E92F74E0FFBBEB48B80E0050A1211E8735AEE39CDB88040D2047B6350C7B1BC2A4C3E7B3CF3E0330D24F5E5A5B5B7FF8E187D0D0D06BD7AE353636EA74BA8B172F36363ADC7FAB3548A840821E0D6AEB38870E57E7210D4853E2AA1EE8C46DA0508DB4E1DD3039E60285E653BE0C44C81009C080BA4EE031EED8661C59DA9C1850A10380EF74B8330F69CED716AF7F704E3E5F0682879E833988B342E7CA8630E910676565C1FC1892917CDAE8EEEE6E696959BA742980AAAAAAC0C040A3D1F8E0C1035F5F5F86610607072F5CB8101F1FEF2C041D127428322B0AB8D486552A601E2E690020BF02008AD4288425C53DC1804D9C1C65CB123CD8590A8B1C55B6934F39AA56BB6A9D2FCE9AB232EED750A0E62F5801AC0000BC5E5A5A36D4803021D8BA752BF7EB68BB91959595656565EBD6AD5BB16285D1688C8E8E3E73E68C442259BA74E9FDFBF76FDCB8F1F8F163BD5EAF542AED6BCA51158F0D1ACBFC5C03CCB7425737223B0368B6F4A98A54C8BF8EFC0AECC884520E00902112F8AE13B76550AB868DEF0DC7892567D17C1522DA500D649BFD03F355969328D798139D5D15F7E3EC0480CD9B37BBD91A61425059596957325AB1E974BAEEEEEE8E8E8EAAAA2AA9542A93C9525252CE9D3B171B1B4B51D437DF7C333030D0DCDCCC23B64E5C094683DA1AD969EBB1BF13570C80CE328F0C342C06803BCDD8D00900C7DA50A8467633369C4655061A5E060018B0C9F1794EBE9D2527CF7017155600C09E669C50A310B8D366ED253AA713C71EE3841AE056E97C9A3809939BD1DE3CFAC9279F141414AC5DBB76D6AC593FFDF4537F7FFFAA55ABC462F1E5CB974D26D3B973E7689A3E72E4C8A64D9B86B44A510EAFFA57A1217E2C7B7D5EC9EB8365E6CC3660A2DB1E8BDABB45FD8C006E198699366D1A4DD302F822B8629A086101CC5C193DCD5702A0B2B252E06E645C5C5C5C5CDCA3478F828383CD97445EBD7A352727E7EEDDBB7ABD3E3C3CDC6834BEF4D24BEE3B4C53E26AE3D4521A97368398F211FF4289E962016EAB191860FCFDC5030383A3774570493F83B6473E6D06CC9FC96F305AB12D5CB870D1A245972E5D32994CBEBEBE8B162D1A1818B87CF9727F7FFF8A152B76EDDA151A1AEAE7E7E7BEC389F227F518F1A05BF40F4A4A440D9A180114D23730E0E7EF6F6284C892045788286A9EC2E73FF5A2F9332DDBAEBBBB5B2C168BC56291484451D468C52691485E7CF1C5EAEAEA969696A0A0A0A54B970607078784842427278786868E3AFE29C700CD4A44A06961EEAC6559CB44F0002CCB4AC430718E6CEDEDED52A9343030D0CFCF4F2C160BF0A7765A5A5A6D6DEDE79F7F1E1F1FBF77EFDEEEEEEE808080D1BB9DCA08A50ED63A11C605AD56AB502866CF9E6D4E6EA3151BCBB21445BDFBEEBB8B162D5AB66C19808080009AA6CD79538880A724446D9382F6F6760072B93C282808A33F67332B2A2424242727C756E84EC224CFD5E0F27A69A96D5E4075F06BAD6E5B70C6310040F6C9AE3F08798B92EE48F2E233E9CD57DEF0C2FB303C82DDAAEEE9E9E9EBEBA369DAFCBE88F179949D306FE099440C5D3B4F4422FCA43B929481935DBD9D5DBD9DCD31DA3A419DABB65FE8BA92AB1ACBF8BD7B023B644B0E0E0E72B7EFF83CCA8EE00416820D69F00C90E86E35BC10A364C102506EDFAA24C32742E27C5D9287B47A1F639AD992D66DBEFEF6D6A33A4E61DDCEA0951FEBEDE6EB7606ADFC5873644D905411245D63B17758B8F3372B1541DB340EAAEFD4407774A562482DB07ACB5245D0368DBD9FF1CF518264363B88D8BC0ECB361BAB29B9C870F3952F16860449F3EB6CFB08777FB1CDD4EF3B888F0DBD1D4D07B1E7D7A53A67852DD17FEC30FC61356FF553D99519D237F0C70E436FC7A9EC863DC5175980ADCB5F7CE695A6DE0E436FC7291C3AAAB3F7333127A75A23629B8AA87235BD1D4D075B364AF3354ECC96BC57BE5D0940B97DD7967AADCE59E12BBF1A3E2462B54C5AB7D96690B46E33FE47AB07F4B75A50BF2F4E1A2293866C3CD6F0BDCE919F050B9635367E3BAA9FEB3510B179239E380A2BB71FDDBFA4F27C1D3BB451DB3CA750A7FD5F370B79AB3B32C8FE8BA1F7FFCC5349B29D1937D1EE7FFFA386C66FC73B69B935398788CDEB60F1646043F8A9EE48A9CE3CAFBBF0457D42948A6555912FD47FDF6A5EFAEF95B6D6517FAE56C7B2607535E7AE67A7AC7652C8F18F6133BCF3F3626271ECD051DD90D8F87E3858FCE9C4D103EF7FD4D8F0ED18AE16A126A75B968C467A1D2EB7D9085C0D3FE226C56883A5960B65B3CEFEFD0D150BE4ECCE9E9529FD1C4056F66BD68AC092D8EF7F3D33B81EC06B277B57392BB455B19FE72D04C022F950E3C1D4F88533F75A2329E13133131E36EB4F278EBEBAE9CD823D6FC5C53F3F9215E0699C0FED92F7B379056565965B6C2E7CEFF372B4A86F40984B878D46637070B0D1681C79D5BADDF2FD918D5772E6B92C1C5B9E5FB8ACFDDE7F0378D0FEF75737BDF9CE9EB7E2E2BC576FD37D4597B4836BA207015456561A8DC63973E6C4C6C6CE9933C7DFDF9F7423091383F0B0597F3E71F483FD1F35354DD4F1122236AF831DD3FFD926DAC4C5A6B7C6266F1D2F61F9B7A91972CEE68D8CE11524EE92FCBB47C9C322E12DF428A1B3669C38FEFB4D59BFF917EFEE4FF242329B77E12BA6061890FB2578191C1C1C1C1C9C3933E4D827877EE77DFD491F1F6A8081C4F14B654866F32EC20398BF3DA622643ED3240208CE07BE121158DF89FC5221EB6A302B8D611886616684C8CB8EBEFFC6F6BD7BF7ED8E8F5FECB4BEE73031B86340D833CC93A08742C4E65DCC93D1BA4E34DC15F5D3023C168161306D1A4D0BE16ABC18A081A14AA3699A6198901079F1A17FDDF2E66F5FCDDD15BDC02BFA93BE22CCF26794721AE07F3921119B77E143214A41472984791ED68F5D5D7366CFFEF1C71E41BC8D0BD3C43C4AA3699AA6698522B8A2F89DB70BF66FADFA74BCC3740B223682B76353DABD7B0F66CC50D0349DF94F39AEAB791F446C046FC7A6B4F8256BCA3E3EB8EAA55F501495A37EED576B46F088446F808C4612BC1D9BD2CE567D7AE08323344D7FB0BFE0BD7F2B1EEFB8460C111BC1DBB1292D21FEE711113F6B6ABA2997CB22227EF61F172E8F77682383888DE0D5C444AB6C4A03F056FED677F6EE6718E6EDDDB9EFEFFFFD7847373288D8A626FAD2649985E452BD232B4D9EB3A5C2606D435F9ACCD7D8D9AA4FEFFDADC9AC340009F13F9F3737E2E1C31F148A608964828D384CB0700902A02F4D8E2B78EE94C19064F95AAA412ECF13ED34791FC634D5E50E7BFFD0D8A0CCAD33E4BA6358FCD1BBE9FFF8CF09F1CF9714FF76AC83121622B6A986BE746BC173A70C2536752973F9F5A457EDA84BF290D2464268E8CC6FFEEBFC7847F134906EE414437FE18BFA2D6B79F3982C392F2F5926CBD3C09CFDE2E26432CB57703B9EE692A1F61C27D6AEA06D5E93274B2E2DCD73D569E5D4E56BCB0D0FDE0E11DBD463498C830716D7B7C494190C2549D0E4C57DB1BEC96030180CA7F061A91E3C255C7B97D417DC5A6B30180CA7B6D4171C76F69021C0515B23F1E0A510B14D3DEA6F3978E5F092F56B9400A06F6D417D419C4C2693C9361EAFBFA5E329E1DABB66C9811D490090B4760B5A5A9D6726076D8DC083B742C436C550AE59BFE4F879D7A961CB2983154BEA1A5E327678B22DCF41C436D550E6EEDE727C23E74C4B5F5A6AA73D65E47338FE21F7D46878093FAA9825D654A4397FFC290374B3AD890711DBD423A9C4D074A065A3F57FB6AD58639F3C924A9A0EC0D293330F520C2FE1C5A264994C263B8F2D4F1D9F5B6D4D3CC8D3B5BC02DBD3B5847DD9BCF5169B1F05F4497089446279813D79BA1681303E10B111081E82888D40F010446C048287206223103C04111B81E021C855FFDE85582CE41651C8E5BDBDBDE69168C2B843321B81E0214866F3162A2B2BC73B04C2D842AE20F146BABBBBDBDBDBB55A6D7B7B7B4F4FCFE0E0047EA4F154262020202C2C2C2A2A2A2C2CCCDFDF9F64366F442C164BA552854201A0AFAF8F1C1027287E7E7E0A85422A958A442290CCE69D984C26A3D1D8D5D5D5DBDB4BD334D9461314894422954A030303FDFCFCC46231119B37627EE0B6C9646218866CA0890B455162B1582C168B44228AA288D8BC11F346E17E1226221445713F89D808040FF1FF125F547223EE9E4F0000000049454E44AE426082</data>
      </image>
      <text></text>
    </paragraph>
  </paragraphlayout>
</richtext>

"""

TxtRacineTache = """<?xml version="1.0" encoding="UTF-8"?>
<richtext version="1.0.0.0" xmlns="http://www.wxwidgets.org">
  <paragraphlayout textcolor="#000000" fontsize="8" fontstyle="90" fontweight="90" fontunderlined="0" fontface="MS Shell Dlg 2" alignment="1" parspacingafter="10" parspacingbefore="0" linespacing="10">
    <paragraph fontweight="92" alignment="1" parspacingafter="20" parspacingbefore="0">
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">"Utilisation de la branche "</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">T&#226;ches</text>
      <symbol fontsize="12" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">34</symbol>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">ajouter</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" une "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">t&#226;che</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" : faire un "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">clic-droit</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" sur la branche "</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">T&#226;ches</text>
      <symbol fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">34</symbol>
      <text></text>
    </paragraph>
    <paragraph leftindent="200" leftsubindent="0">
      <image imagetype="15">
        <data>89504E470D0A1A0A0000000D49484452000000D60000002A080200000040D1321B0000000373424954080808DBE14FE00000092549444154789CED9C7D5014E71DC7BF7BBB80EC55813BC4E07806B82A50875445ACD34C3B54790974C6B718A6E950E89044B10AF81A2DD64CAB91600A560504CD84A1C838560B51E34B3DB4E3A4D34C07EF88AD898DE242A50E679D0BDEC8708777BBB7FDE35EBC5720B877E7C97EE61966F7D9E7F9FE7ECB7DEF79F6F50804039EE7831257E4398402907E34A086D0AC2302194EE4394712EC0444263BA2054582CCA8165442BD161D19DE36C9D0518014FFE42432A9A0801F9617A028DAA5B6FF0BAC66D0918EC263C829403983C383414A50E44587023E3F7C0A8701C8D09185CA53F8DABE6DF52900F8FA54D09213990C50BE36A464A06D816DB9F5CFB651F0C05AFC1800F0D9170090938DB64400F8EC2AB630800C1D6B30DBA9CB53113D0A9DCC2D22E28000D0D2D252F7A4D87314B4A1843A098B3A515E80040DB630006C6EFB8FD5794AA8D3D174B229E0C98B841EA5A5A56E351480BA27C55EDA3A0D69D02345864CA092716AA0C731EBEA23F403008A8A8A04CE57E4C5A2B5B5D5B3D2C7442C43C71A5CB3CEBF327464F9373391C98CCF6341E8A11A04801425660318C43560ADD23E11FBC66466FB1E91DA21F20927407E1CC7454444B02C2B809648C08920113F954B886623C2C37CB5F161C141343F42DB5A00E8EFB3CDB387AFA0630DD4CB00FBE98857FAF41421A15E4DC2144A801B7126132795522693E5D9A54402CF130E7DDF48FAF44889F3D9C6C98283B6AB3056CE77E2BC5BDB41AC3EE6B47ADDA5E3DBF6B58121F24749044958CC9C00BE19319922A5523327C4882A1270488248944BFED64BA6C4D9CC303434445114455124491204411084EF8978A298583E8C04CB0AF3E803CFDB8A4828C2F37C1805B3D300A2D56A699A9E366D5A646424455118ED58F019630BA7C30BA72612747A7A7AE472F9AC59B31C032105819E9E7ABBB1D1655DF4A08837B45A2D00994C16151565AD91F002E11C860F485195D3D1E5AAA7354C5DF6B4CC062640D1052EAA8DD1A325AFAA08DD5D73B5E0F0F0F0C8C808CBB20EDBF8E7612DDEFF3BC6D47DF85549F15755471C1F8CB2ECF2E36BEB95DF4A47B5695AE691207CB46E719923E793358F2BEF1C52F9EA12C8EFB6B0E569F600008BC5E23666F9E5589087602710BE4E47FA2EB563D5C76578ABF41253BA41F94C2184CB76C271732BCA12781CA8607A79248EA37D083166CA213A0A32973EC18A3C6542DEEBF8E422631F5A3647651EE9050FF0BD75B951B43C8A9647D19B3B3DB6DA96559BA356FE115DBF5940CB2B54AEBD3676DA9B6DAEC8B4AFFAD2B12F346CB446CC6D606C8DDD051DBD5CE27656A42D5A40CBA368F92126C1312E66B9E50F9EB1A98DA5EFA5CC9BB744ADB9F13C8C8201B2A02DB0FF0A73F12C5ECF4D0412F357A0FDB2DD83B6D8BC6ACB821DDF3B6DD0E90DBAEEFDB7D6643632CE5B1DCB3907F4678AB0786FB741773007BC6ACB82F615DD069DDEA03B8D1AEB9117BA6ECDFD58A7AFCFE2DDFA7A2CA36BF79DE53ABD4177BA445DF9872BB6343C0479CFB8C83A68D0E90D3AFD99A296AA4606E099C6ACB4B3AB6EEAF4069DDE7020CBAEBF1F47C6A5EFD508A87ABF56A3BE11780F8EE5C0D07C70BFF72FED58959F0400CADC55D87D58E5BAF9F62D94E467030092CAB6FDB2AB67AC9B8AF65E5DBB17D2B1D174EC1BCDEA3BD63E8B57BC36CE597EF1DEF21C00C85E5E842F7B7A7D097AA373636C341D1BBDD2760FBFF7E2D9EB25DB7EE51677F1DEA3654913D307009C686BA8DA57ABD1DC18DFEE048E50BC2EA8AAAFEC52232DB6D25173EECAC19C651EA19D7B8DAFB2E4A4BEDE4947E5D9C5B3EFA8E26E82DE447AEBF2DEC049BD611998A6ECB77CA94D4CDF9999F1334EB435FCBC70C3AF776D4D4F9F3F6ADB80E2AF89D8711A217C519D6BCDD8FF8F478687B672734F46F3051578DE1E37313915F61AA6AEA6A5242F0B3CAFFC6E46D79DBB760547868E85C4E45434D734302EB1BCECC8583AAE69B80B7A2ADFBDADCE484EE0C13317CF5EB776CC5F9E316A26E3D1772D567B5A5DF8C1BE5A8DFA861F3F208F3D0D8605FD793A72F54273FACAFCC4A735CA9C958B8F5F50390D1E39359AFDB70AE8B8183A2EBD7DB9A67E29C043B96E7BC9716BE505FCC2DE32BFB8EBBD743A6E93CADA8BDF95161743C7C5586B1C82CEC5AB8E4B4BE734DC04EDC5296EF6E63DD8B124868E2BBD9D9A61EDA85CA73A936AEFB8B57302FAEEC581D5855555B59A809D9D8CE54142A81F36686A6AB23EB27AF98E64D95C72C424CC830546A3312626C668348EA3AD6ABBEC5CDE60FD524102BF58CC4F5BA2BDFF4FC7EA80F67F6F166ED859B975E142BFCFC853C2C9BFF65872E75A00B4B6B61A8D468542919A9AAA5028A45229499221793AE29D2BE78E2F4A4E0A761621C14B33A6B7B51CAAAEAAEDEE0EFED949E84DC45E4A5FDD4F65F44B055FFEF668D9CB818C1B3AC5198BC562B158E2E2629B3FAAA9AEAAD574FB7946E6BD9BC481DFCE88C70A3C7E1D7ECC87B512CA3EFDA64CD8B82F2A56FF711CC771DCF4585953FDBED20DBBDE0DC88CEC0BE147C1708A307120C49F2E7AFE70F61FCBB21CC7C5C6CA0E1D78EF43BFCDC8120961E210468ED646F85170E654EEDE236276B424224C001B4A101E46820F1F752744C684F0E23F9665599695CB637E5FBD73476575C7991382873573E8D723FE3B9CF57561AF086FC1C468961984FABFE413568007F7390E11112C2B84D464C6C4C2E1BFFBF707A64F97B32C9BBD72BD739B6B7785FF2787939821E592642CF06D5F5F7A96A86154EA0CA442A8B73D08C02490D4E4258282C37F8B7EF05A6343F5D29FBC2AA7B1BEB4383FCF717BC54FDF736214FF2144EF118B4C0087FF3E3DDB5ABDBF9E65D90FF6EDFCDD9EDA60E725E828E8F55D7991E701A3D178FFFEC0FCF4ACB20D85FFBEF52F8984EFEEBE396FDE5C8984DFB67DD72B69C941CC4DB0BB236E0C0D0D69B5DA9E9E1EAD563B3C3C6CB1880773C1E4E847A7EEF50FAC7BA7E0E5D93301DCEB1FF8D3E94BD7AEB63F78F0B0B0A86CCBA6E280653275EAD4F8F8F83973E6C4C7C74BA5528944E2AFEB821445D1342D97CB018C8C8C88BF6F1E5CDEDFB3D57955A150FCFDF31B0F1E3C94CB63A64C8950281401CB243232522E97D3344D92B6AB1CFE1A05CD66B3D1687CFCF8B1C160B0BEABE28F282213E6E143DD3BA5EF7EFF95796FFE6C796ACA9C80C50D0B0B737E8F9820087F59D07A09C06C36731C27FA4FC40141106EBFA6E02F0B5A659DFF8A88002008C2FDAFE80F91E0F27FAB5CA1E4FD96B5780000000049454E44AE426082</data>
      </image>
      <text></text>
    </paragraph>
    <paragraph>
      <text></text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">supprimer</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" une "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">t&#226;che</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">", faire un "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">clic-droit</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" sur la t&#226;che &#224; supprimer."</text>
    </paragraph>
    <paragraph leftindent="200" leftsubindent="0">
      <image imagetype="15">
        <data>89504E470D0A1A0A0000000D494844520000015C00000042080200000094DFF9240000000373424954080808DBE14FE000001B0E49444154789CED9D7B5C1367BAC77F938410402004BCA0A20289183F72AC62F584AAABABA0A8B5D6225DB716AD6D09586B13BB74ABADADA7B65E6A956897C3A55D57389EEE1E6B956E8514A2ADA77B0A2D0256511013F0B2B658974BC0724F32E78FC9FD46D070B3F3753E3879DFE796C9BCCFBCF3CE9B37044992A0A1A1A131C0728B158220DC6287C645E8544ED37FB000C8D23F5E1EBB4020E03F88A1A82CFA341D20CAC5740AA6E9475800962F59B069C79FFD992DDD5A2C7AECDF5ED99C3CD851D1D0D00C1A0C00023E3F7C1463EFCEAD9F7F92FECD7795972F5F1EECA8686868060D06F59F8E444F4F8F56ABEDD632D2FEFECDEB3B775DB87001405353934EA71BD4086968680614821AB252A954D2373FB8F95353F05461D854FEA34B57D75DF8FE97CBDFDEBAD990B17FFBE8D1A37BB14210F498C280512E26E881469AFEC3E2F43AF6C9278D61D12547D33C743D21A2C5E1D1B1776FD55DFFFAEF73F8E3E29F5AEDEFEFEFD0CA439A140E260167B1B519271763FB715C1DEC7828E8A440D3AF30CC5F3CB376ED8DAF4E4D5FBDB1AB559DFF51764B514E6BEDE559CF6C6A9BB6E80F878EBCBB676F7D7D7D2FF6C2519664D862FA316EF070320153CC77DCCD8A18E02CB6D6DA78741E4FAFB83760B998302296F7221A2D53B9CB2FCDC38BF535472EFFF2B2D7C433FF9D33379417C0F57D61E3739F7F71FAD2DDF69079712C0FF6A9B49D3D1DFE4F2F9CF4FCC60D165608222A8B9CF2288ECDC0CE6C9C0640352A857EDFFDF006F0EA3D50BE5ED065F6B3071A1A3B24275B3C70B49EBC1413B3F8C48E7DCB5FDCD4F8E5D1CD9B5E03F0F49AF878AD36BFA0A0E247F58F64D445F6EF8A335EBD7BF7E76DAFFFD14A373614B9274C59E0B40200C0C3C9784C0000ECCCC6691E4E2EC6B966248602C037864BF1C124CC87A1A4D9A4927B028781938B710398CF35A96C598C095C1C4BC2ADEB4000B61FC755D71CE943B232D86C12D6EB5A0660D4DA7E06BB0DBADF9CC58D2824724D16A85A2BA754AE84E5DB3197347A2CC8446262A28B1F240D8D5BC8CDCDB52AB14E0AF5F5F55346713B5A5B6A3BD9D5D5D542A1100093C95CF9F8E32B81C9FF73E28D9CF7478FBBF78FBABB575E90FED747074D73197958C0C591266B9707E371E32C56536D2306A7CB012E269563960208475914A6D4223601388B5986467B300947A8EE060F2717A3E80CC0C58D13D8DA0484A36C1156D4E2F0192C586CC8058B5D7564BAD45B193C61260C1C8CB709C01C4A3700658B70E3046605A02C0A53CE986AAD9D9EC7ACF300F42587CB6D240D1EC7B8F421D2D0F42FAC9C9C9CF5EBD71B5F878484A44A5F7A6BBF6CFE33E20387DEFC3833DD5CFAF74FC7AF4D201B1B1B015CBD6AD39B56C3FA969587496A6CAF0580ABB5B8158F15E5801AD954FB6FC62D003C2C805E46AF02EC4CC24E43011F801A4554BAA9C5378B10C6B3791FAE38B20CD5C2608099B0DD00ECE9DE32EE58D65A3B35EB77406D369A60E331D370F7D0DDA3B9DECCACBFC7ECD2DABCD3BEA3D56A3D3D3D351A8D1B6CD10C7F3C9908F6D54EE26A3CD91E760558E619C1C8DA154B4ED55D43F88CB367CF2E5AB4C8BC8A2088A0A0200073E7CEB5D069C20D2E6279B86AD359E8336AAC33BF81E761E3039B1CB4007838198F732770B849DFEF70E2D17840AFAB590483F55818382C37CC68EEEED6FAF8B0BABBE9F9263400D0A5C5F546C67535A68CB22F60FF0B5142A130AF28FDB1279F3BF8FAC679F3E6B1D96C579C655FC0B178D4590E34DEE022291C5B6B31251C13AEE3346C1A5813CE412F43BD34AAD8211CF3D5C86E027800177C189A6E930B8EEC42196CC602B3789C05701F183A1453C20DFD052B0C1EAB94FA829FEE31E785114C42D7A375434BEEECEEF6F2F1E9D1BAA3D74133FC6112446820E31F75CC29A3F467D7BD7BF7582C168BC5623299044138FC96E4B34F3D71A8F0CBCA76E1DBEFECDDF3EE5BAE38BB7A1EEB8063C68EF775CC024E9FC0C978942D02809DD9806DCF1F387CC624F3CD596C3553811AEBCE005C1C4BD20BEFCCC655004D38721D3B93B0F1BABE7CAB0B8E4C5819B414B613C07DD38423CD7A5FB7AEDBDCC5587A3426856E0DE9C18446E39EC90824A9DF6868009024E9C1428FD935A2BEBEDEDBDBDBCFCFCFCBCB8BC562399B06F3E21F651F376CC685777ECA4F090E0E76E2A67F272FB9FD89E0403ECEEC0B2FE832A9A70F85D7184B85CC1E8D7BAEED1D1D1D0101011D1D1D6EB146F310E0C162165ED52D99AC03909B9B1B1212121818387EFC781E8FC7E1709CADA7B07EE5ECC2770FF88EBC79F1E245E74981A65F70579A250D1B0D8D3DA849893C1E8F9AB5CC70223AF7B1E89CD7E62C8C5B78A5AA6A80A2B34B1356BBF7AAEE7683FD00D9DF5BD166AE9F37D7CF9BEBB7B9C8BD966B3F8CF15B905EDBFF6F81DE1E6033A7ADADADB3B353A3D190244992A4B3A40060E1C205CF8A84972F55F6DFD94F631FB23FCF89DA0F63E271BCB5BDA9B5BDE94284B2C8ADC6C35F2E6C3D97123EF8E73DBD39DA405A9C6B3A9D8E4A07D4CBDE97639B3367CE7725DFD5D4D4444444F4C3B94F631F126E1B1AB433D0585B53F6684418091240D8CBC961F430E4AF0BE79F762F3D058A944D2957AE5C714B3434AED2AF3D85989589E7FF989C5E6B565824F55FF09F7556FB4552FF05FFA9F87089BF77A0BFF712BDBCC342E92B0B02FD372B1CA84B15A84D5F1068A105B24E5F1BE8BF59616D67F0AFA80FEB06D2D9A9E7D2C2AD6C367BF5EAD5CE65E885031F9C1732328CFBBD7E727DC0742E18893DA8AECC88890CDA8EC44FDB0FC6584A5AEC97EED8F754A9BA3DACEEC3A5339FCF587A2E25CC6161D5E4CA067538C8A2025B75C5E6A078EFAADD950DEA70283607AD493BB3E94F8B51B475C6674F54B47F190628362F4DAF5DBCC9DC4E1FDEE2B469FF9E93931915F5C8031DA85F0DCE0FAD4B3D85DE7DD0B803B77C162E139EA2686FA8D857B5C67BABC289D8EC5D592F8701087BF90F1B4A95B5CE0A9F581AEE503D6665A251206665222E2BEB80BA9A2A94EE98E91DC4F50E5A73A4EC5AAD633BBDB3FBBD03E5E53FDC87228D152C00151515A16161DAAEAE5F6A6B03A64D23B53A0200838061ED76EA7C2549920048ADB6FDF3CFD55BB7125D5D5A601AFDF4BBDFE8C78E8291B097D3777F3627BFE8408C49D8360012006A955780E5AE14DA5577B4BFF16FEA3F2D329514D98AB9C827C7D27FBFEEA56D6FBC4AF7171E10068086DBB71B6EDEB87BA6A841D3D3F0AF7FF98CF0E1787B71381C2F2F2F4F4F4F4F4F4F8EA72787EDC9E1703CFDFDDB320FDF7BFE79764B4B4F67A7B2B373B0E37F6821611A2074FF56F461462DB55F5B78AA7496209C24C3F98F965E5351B57FCF357A47E9E7F25A9204595BF0F9F98D718B9D149AD987CD8EDDFDD008218E7C905E6B11DB7DBD7190181B3CFA9363E97BDE3B505EF6433F1EBA8763737AEEB1003437374D17F05B5A5AC63C1AFCB35A3D616410D89E04830150C79BB2423218EC7F569FD3BD7F8005FC0828815F06A479FC3AE9F593EB8329DB9E424C8432C05BFF7598F5793F6F0A270171EAC6D109DEFF0560FDC6670D8AC06CE1B5E74705940278F678FB6F9D151A55ACF71DF714623F28DFB72C2A72D41B86486476C45C87CA0B6BD7BDB46DFBAB33E9FE826348A7C7972049F2FCF9F36C0F8F4921219D3D9A9BB54AD6EDDB931F5FE9C164427FDB40FD23DB5BFFA538BEE39733FFC729B9D3DCD0A10508E015E7E669FA4266A6699AF3A2C9CCCEEE419FE65C94CADBCD2F3F270EEDB570907924F2DFEB6F5FA4F67FAAFF79EDBA975EDFFEEACC99745EB00F87CDFC4A699AE6DCD1D111121222140A4342427C7C7C18003CD9EC91FE7E977FF8A1B5A971AAEF081F6FAF7FDEBE4D1AE63390A44EA7D56A7ABA2F971C575D2AA91DC9A96FD39FAD743EA019828C0D1EFDD763E97B771FA8A8A0C71DEF07FDD3070F8E17BBAD8DAB6EBE73E9D2087F6E8F56DBFDF3CF0040923A9D8E24983F5D2F2F2E3CDAD24E767593DDDE2C12E80174A30775AD20950CD1B2DEC58627FABB6B7A736DB362CCE891C78E1EDABBFB4079C50F831EDB50DC6C0F9919FAA4C01D39D25F286C9F309117BBB46BD468A2A3E352417E5B672708822488B6963B8ABFBED3A0EE6AEBD4B5A8DBAB277BD74E1CE1B3E03733F6EE315952C94010862DDA660DA661829344E36A0E52219A0041580ACBEF237F0DFE701419FB7EE3B9A449AE140EF2668E4EA7D3E974A346051DF9E8837DEF1D282FA7C71D9D1D2E5BF44941ABD14C9C3811ADAD5557AFF6787A0693A4F091E9DF7EFB2D8320745ADDB7CF6F50DEFC67634B67478F47D08419A2F897961D3A12B5EB3DEEF4E916C644697A9FCA0408C47D6D034302BE04C59207B220DF8F042548123BAA41ADA82E8B06B1AC4F36D82CA25B0BFAA7BCEF032A2368B55AAD563B32889799FEDEFBF47D84250C06D1AD8507D3A1000B54EF8B240172CCB8713FE47F31B5B3BDABA181E47044BFF96DC9F7DF073635D5683C83F98F4F0F9DC20B0C6632994C1693C5627568BA35ED0EACF223806AFDBE4A068114002082B2189041500D320B0020079107A51089D03745954CBF6FA565BE4CA2A90A10A5D971C137934CAC06B25102002820219021118894223B096496996212C82CC8C558960D519ABD00544894A20420A4485342C237451B2945B6C17E9C599C35866F91498AB14286BEACD23CD6577BB39998C065787AB8213130C0F66082643B3E0B1E0208C0322368341AAD561B14C43B74F02DE91FDE7963476A54D48CDEACFC2AE8D1E2961AC123B4FAA366030B00018204A0D531BCBC22563D75A3A39D1718D4FEE38FACE6A6B09141ADA46ED1BEBD8D771BDADB7FE9EAEA2408825AB949D3A361B31D0C8FCBF32012527B1054EBFB2B2A19126528962089803C0B71803C0F49AB801A5B7D3B5AA62AA9BEF9516DD2993050520925093E20176399184A214AA4D84122CBD2942C1A6239B2B2F419CAAECDDC3453F232D93758938BB14B863809E252B14B0029204A43B1F59AAF2E12CAD5D436A1EC9FCC2E8D1B9663D36AE1E9A9D1B8C3D490A55B63272368341A8D46131818B06FF7EB49D2BD6FA71F1BEC3087046C2646FB68C3781AC0C1C2AD3939398F3C329D200890A456AB9D387EDC9D3B77FC02037FF1F6696A6CF0BCFBF39DFA3B13E7CEF39B34A1A3A3A3ABABABB3B353A3E9014010044158CE922E91829002D05F6C01A86A806C10D9068924005895843C39E2E2905789D42C3B49C1AE96B14A9466714176220C4094A0EF38C4AD0276412934A99B9B5A9100691EB2E25CB26961DF6041203414F151DCDB4D5B6F30080802358240F7ACBFDCD2DA1A327E7C4B4B9B5BAC0D4D3C59306684DBB77F1A393250A3D124FCCE740F1BC0C16F43BB0631C2610463FDFAF52041EA74D4894C008123469CFFEB5F47809C3275DA186EC0235322CACACAFCFCFC7C7D7DB95CFF51A34605058DF4F7E7FAF9F9FBFAFA5A18A3C614946928A9B62ED46F590010978ACA3C408ECA049BE5D31D6B39A14FC22ED21F3669FA136346889ABDA4407E56A3D11004912C4ECC3BF9176A1BEC00870D0C50630A86412D1D480E97CBE1F33BABAEFC92F759E7F9EF35BFB4CD9F3FFFABAFBEF2F5F5F5F4E4B0582C2F2FAF112346F8F8F8787979D931C997A00020C400C08F408914D63F71C8474225C4794858A12F302691D3C71D6BC150755CFF68A3576173E4791025406065CAA078FA389256D9AF32C73CD9D10C318C1921EFE45FF6ECFD50A3D1ECDDBD6DD7BB69831DD7F0830100E65FD423A1E9EE16CD9F779960F5FC6661C72351F56D6D8D0D0D8F3FBE8224756C36DBCB8BE36980C3E1D8B71A9785B44A10D150C541998665864795C6C7722B12900DFD701D5F82B44ABD407524A56F5F8BAA2A8884C04561EA8E8600416099CD7080B9A234D274EFE0C8265F82A46C1004FAFA2BADB26808A4FA487A4D5E34F78B3123CC8A9A3E61C2B88A8A4A1E8F3B61C2B82F0BBF1EECD08619044992172E5C983C79B2A9082008A2A9A9A959ADF60F08080C0C6C696EBE74E9D2BD7BADA1A16163C78EA5166FA2FE4E9C387110A3EF05E3B30CD7918BB14BF8A04F25EF17E33467F7FE9A93614CA1C58D36871AAB563F57567E91CA0800CACA2F6EDEB23DEFB33FDFB973F7E557DEFAC7FFE60D768043110F0F0FD89BE6CC827EC890004002044092A44EABE50604F873B9F7EEDD53147EE9E33362C68C191A8DA6B0B070CC98312C16CB30FFF9611AD09683580688A0A44710861F564306B3A2A6874E9A70E7CEDDC0C0000F0F975612A231C280E1E92EA9D381D4EF503942D3D3535656161131452412B1D96C1F1F9FE8E8688542C16432994C2683C160B186F6E1EEDB4CA4389024C86287639F0F1119B15C2E97CB8DCDA8EB939A42D26795C123EDC07F24BFB46DDFFE4C59DA3BFDED6B581D98DE31B56AEAA93C01900C06009224592C564444C4F5EBD7838383190C0693C9F4F3F3EBEEEEBE75EB566868A856AB1DF0C58268DC434AD1A735DCFD119929617D505248F6475414F5496530193366D477DFE60F8CAF18993A3C439251271B3647C7290C000C068320088241100441ADB5441A6648878484F4F4F4DCBE7D5BA3D19C3B77AEA6A666CE9C3963C78EA53A0B043D11F7D7435DF896E19311069EB0942D4B063B0677C100D0D1D1D1DCDCDC6046234553D3DDBB77A7FFDBF4FCFCFC2FBEF862D2A4492121217E7E7E6D6D6D252525D7AE5D7BB8C7AE7E1D2824DCD88C0C09D7E27EA24E7F7FC1E54A1486829933679A0A14126EAC4412AB7F692D6E596BEEA8CE6ADFAE773BFECD8D38F05B97116B26ADF760D7A913FB50E86331D62824DCD80C85D5FD96DD3066CE9C49E938B63E4C6001108944CE855E7BED35AB92F0F0FB595A93664852BAAD2655AD964121E1AE39AC4891C5280E6F9BFAA9BAC8B8C6B34232F3D49315EAA230402189CDA88B4901505A1551A15687F556DB77EF760C9ADB71E41745A91BB8F90A594C0C0045FED10DA9EA30D86D94CEECC7C8D46A19008584BB3F630B5553BA6DFF93156A75585D46ECCCE48C2545FAA5AB1DBD7DBED5D11B7EB86735679AE1CCEC3D5B62002066F90654A9EA80F088D947D7985DB7555528DD3693CBE572B96B8E96D6E8D75C7E724958EFB5F7E1DDBE4193BC43BF31CB371CCDA7BA2AF9557AAB76706E5FDF555873D43C426AF0252C25758351DC711856476F18C200204BFF58A91CA6EB1FD0F4036129456A752692CD3AC01B3E551B90D9B636E7B5F7818B06ADC462B6ECA9DA9F515797B1BFAA979CE4C07E5D46EC1A7CAA56ABD5157B66DB6AD5A9ECFFA6AAA5353B476F98C100B07CC9824D6FFD397EDDA6956B371DFA53E66087443324084B29AAD833BB4A558730FE541CDDEFE8D2E7BCD64478C46CC36556917FD49963D70CDA130B5BF2244E1D3E7C6A6AAAFE8EC09E5327F66B6B4A67478403A82B3C556A2C2D3D5558077DE186E55639CA8135D3D11B86300008F8FCF0518CBD3BB77EFE49FA37DF555EBE7C79B0A3A2E95F3262D71C45E9B664072DCF30DA36731BD5BA6264157BA0EF22DB5EFE9CD71A094B49DD70740D97CBE572F3B1C159742E1AB42716B6E4491C3D3AD5D872ED3A756C3F668BBE22B966AAA9A7307B6A4DB2FE707C6ADB6FB1B1667DF4861F0435D72069CB1BD294750281E0C967A5A3228523BB1B9F7E62C58C19339A9A9AB85C2E83410F3D0C04F434E7A18742C21D56D333FA82B369CE005EDBF29CF4CD0F6EFED4143C55C81EE13B79E9FACF2E7C9F7372D7AD9B0D19FBB78F1E3D7A5083A7A1A11938F45D003E9FFFC5DF325F4B5EB56CC373CD55655F7F90AA6B5747AE933EFAECF33B0E7DF4E7237F7968AF332A5974B4F9D71EE5628210BBF85D464AF7412CD0D00C3D2CEE0B9E59BBF6C657A7A6AFDED8D5AACEFF28BBA528A7B5F6F2AC6736B54D5BF4874347DEDDB3B7BEBEBE177B723161A45F5B86B1295AB7C907422E5E860252FF2D6A27961D575958A019F6C4C8D40FE7BD83132CBED1441044EC0CE16536BBC57742FC8A47D84CC6DB1B567FFEC5E99B77DBA356AD6379B05F787B674F87FFD30B273DBF7183AD2D952C5A208D2C2049AA45C8C56239E2FABD75F025C5C56E33169745BA1430E5546567D576572DD0D00C55AC47106362165F2D3CB9FCC54D1A4DE7E64D291C0EE7E935F1EF243F33F6E677B7FFF7EF3F92510AF69BAF645CD8B3779F8D29D5E9E348539AAE91715959710054B268F39E834A161D2D9389AD3A13A60E86586EAE122D53512A62B1959544694989544010D162B1A9CBD0BB2363B0066181B4C4AA84309833BA90A94C95A6906C7A0AD616EC955808BBAF874343E33EAC93427D7DFD9451DC8ED696DA4E7675B57EF5312693B9F2F1C777263FFBDA62CEA4FAF7A78DBBF78FBABBEB5E905A7C4B5275FA78496484F5F78EE562AAF34092CAB4CA6554D32C9156AF224992240B92B277C95450C9A297A140BFF453569C5C2CA8DE41BD50261C4F94A90094540A730D2ACBC472F025B96922519A92248B53852E3BB21315A94C13E94BAC9C9AB990F0F992627D7C0591D2FD766F8B6C2DD87B233434431E564E4ECEFAF5EB8DAF43424252A52FBDB55F36FF19F181436F7E9C996E2EFDFBA7E3D726908D8D8D00AE5EBD6A6D4C24145895A86A2A4569B97100C05F912092E6C9538510A5A51A56401641DFC3C88D33534176B6D94ACA4A08214A586158943909BB6A54B0EEA2BBE2C89EB063A796EB2AA864D1C63E854868A779DB5A50C1994DBEA49874B8D6837B17AA08E4F1DADBDBA9E74F3434BDC230CF0846D6AE58D270E31AC2679C3D7BD6AA8A2088A0A0A0A0A0A0B973E75A7C759A1F115972FCB45BAE86A234A569D5C8811AB373E254258B161C4F509AF72C5CB330286F8486E6C1B07F45120A857945E98F3DF9DCC1D737CE9B378FCD66BB602A2E356D9740208E309CFD72B11859AB224B96ED974BB2E2A03A7DBC2469471C6A7659E9F157244040C900547259667A69853C2F5B94A0E4032AA0A4DA74ED35D372E8C8E43122B264D7699544C287EAF4F1122438746A7461E8AAE8E5EDDBB4B4E0FC8DE8134DB1C4F2862B3737D751D434340383C36EEAB34F3D71A8F0CBCA76E1DBEFECDDF3EE5BAED8E24B8A95881618BB0F490524E2E2946986A2A402320E2ADBDF83E24B728D32482A20B34C2A80284D990B94480584D4502FE103E04B762411CB886C5152122004E2B27A7764242EAB208F10105240949424A24AAC9C164BF8461769CA1D91022A0083BC3D9B3616ECD8747A00939393A91DF39B152CDDF9D153E3DACAFE22C92A0630492442FDE8DF6F991F04347C737877DE0DBDF9170FAE11DAB14943D32BBEBEBE5E5E5E1E1E1EFA6171274BAABDF847D9C70D9B71E19D9FF25382838307324A0B54B2E844E4F6D6A21E3E3A3A3A1A1B1B6FDFBEDDD8D8D8D9D9492F7E47D34F7879790506068E1F3F9EC7E371381C67035AEB57CE2E7CF780EFC89B172F5E1CCCA4F06B85C562F9F9F9511F9546A3A193024D3FE1E1E1E1EDEDEDE7E7A7EF2C383FD5BEFEFADC67176F84EA9A5EDDBA75C042A4A1A07E1CB1A7A7875E2397A65F31FE6A34B5F06A2F8FBE162E5CE0EDFD7D6606BDC8C220407D544C2613D452BA3434FD03F518D1F8B7F7E7E173E6CCF9AEE4BB9A9A9A8888887E8F8EC60CF38F8A8666C07069A184944D2957AE5CE9EF506868688602FF0F97A14CEA38D098CD0000000049454E44AE426082</data>
      </image>
      <text></text>
    </paragraph>
    <paragraph>
      <text></text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">"Pour "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Tahoma">d&#233;placer</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" une "</text>
      <text fontsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Tahoma">t&#226;che</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">", la "</text>
      <text textcolor="#804040" fontsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Tahoma">faire glisser</text>
      <text fontsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Tahoma">" &#224; l'emplacement souhait&#233;."</text>
      <text></text>
    </paragraph>
  </paragraphlayout>
</richtext>

"""



############################################################################
#
#
#
##############################################################################
fichierProgressionProgramme = {'SSI' : r"SSI_Synthese.xlsx"}
dicCellSavoirs = {}
dicCellSavoirs['SSI']  = {"A1.1" : [10,13],
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
#import array
#from ctypes import *
#
#def get_file_info(filename, info):
#    """
#    Extract information from a file.
#    """
#    # Get size needed for buffer (0 if no info)
#    size = windll.version.GetFileVersionInfoSizeA(filename, None)
#    # If no info in file -> empty string
#    if not size:
#        return ''
#    # Create buffer
#    res = create_string_buffer(size)
#    # Load file informations into buffer res
#    windll.version.GetFileVersionInfoA(filename, None, size, res)
#    r = c_uint()
#    l = c_uint()
#    # Look for codepages
#    windll.version.VerQueryValueA(res, '\\VarFileInfo\\Translation',
#                                  byref(r), byref(l))
#    # If no codepage -> empty string
#    if not l.value:
#        return ''
#    # Take the first codepage (what else ?)
#    codepages = array.array('H', string_at(r.value, l.value))
#    codepage = tuple(codepages[:2].tolist())
#    # Extract information
#    windll.version.VerQueryValueA(res, ('\\StringFileInfo\\%04x%04x\\'
#+ info) % codepage, byref(r), byref(l))
#    return string_at(r.value, l.value)
#
#print dllpath
#print get_file_info(dllpath, 'FileVersion')