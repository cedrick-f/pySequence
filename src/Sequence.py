#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                          ##
##                                  sequence                               ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2013 Cédrick FAURY - Jean-Claude FRICOU

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

"""
Sequence.py
Aide à la réalisation de fiches  de séquence pédagogiques
et à la validation de projets
*************
*   STIDD   *
*    SSI    *
*************
Copyright (C) 2011-2013
@author: Cedrick FAURY

"""
__appname__= "pySequence"
__author__ = u"Cédrick FAURY"
__version__ = "3.20"

#from threading import Thread

#import psyco
#psyco.full()

####################################################################################
#
#   Import des modules nécessaires
#
####################################################################################
import time
import glob

# Outils "système"
import sys, os

if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf8')
    import locale
    loc = locale.getdefaultlocale()
    print loc
    if loc[1]:
        encoding = loc[1]
        sys.setdefaultencoding(encoding)

DEFAUT_ENCODING = sys.getdefaultencoding()

import webbrowser
import subprocess
#import urllib

# GUI wxpython
import wx
from wx.lib.wordwrap import wordwrap
import wx.lib.hyperlink as hl
import  wx.lib.scrolledpanel as scrolled
import wx.combo
import wx.lib.platebtn as platebtn
#import  wx.lib.buttons  as  buttons
from wx.lib.agw import ultimatelistctrl as ULC
import wx.lib.colourdb
#import  wx.lib.fancytext as fancytext
import  wx.lib.mixins.listctrl  as  listmix

import images

# Graphiques vectoriels
import draw_cairo_seq, draw_cairo_prj, draw_cairo
try:
    import wx.lib.wxcairo
    import cairo
    haveCairo = True
except ImportError:
    haveCairo = False


# Arbre
try:
    from agw import customtreectrl as CT
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.customtreectrl as CT

try:
    from agw import hypertreelist as HTL
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.hypertreelist as HTL
    
    
# Gestionnaire de "pane"
import wx.aui as aui

# Pour passer des arguments aux callback
import functools
    
# Pour enregistrer en xml
import xml.etree.ElementTree as ET

# des widgets wx évolués "faits maison"
from widgets import Variable, VariableCtrl, VAR_REEL_POS, EVT_VAR_CTRL, VAR_ENTIER_POS, messageErreur#, chronometrer
#from CustomCheckBox import CustomCheckBox
# Les constantes et les fonctions de dessin


# Les constantes partagées
from constantes import calculerEffectifs, revCalculerEffectifs, PATH, findEffectif, \
                        strEffectifComplet, getElementFiltre, COUL_OK, COUL_NON, COUL_BOF, COUL_BIEN, \
                        toList, COUL_COMPETENCES, TABLE_PATH
import constantes
import constantes_ETT

# Pour lire les classeurs Excel
import recup_excel

import Options
from wx.lib.embeddedimage import PyEmbeddedImage

import register

import textwrap

import grilles, genpdf

from rapport import FrameRapport, RapportRTF

# Pour l'export en swf
#import tempfile
#import svg_export

# Pour les descriptions
import richtext

from math import sin,cos,pi, log
from operator import attrgetter

FILE_ENCODING = sys.getfilesystemencoding() #'cp1252'#
#DEFAUT_ENCODING = sys.getdefaultencoding()

print "FILE_ENCODING", FILE_ENCODING
print "DEFAUT_ENCODING", DEFAUT_ENCODING

####################################################################################
#
#   Evenement perso pour détecter une modification de la séquence
#
####################################################################################
myEVT_DOC_MODIFIED = wx.NewEventType()
EVT_DOC_MODIFIED = wx.PyEventBinder(myEVT_DOC_MODIFIED, 1)

#----------------------------------------------------------------------
class SeqEvent(wx.PyCommandEvent):
    def __init__(self, evtType, idd):
        wx.PyCommandEvent.__init__(self, evtType, idd)
        self.doc = None
        
        
        
    ######################################################################################  
    def SetDocument(self, doc):
        self.doc = doc
        
    ######################################################################################  
    def GetDocument(self):
        return self.doc
    
    
    
####################################################################################
#
#   Evenement perso pour signaler qu'il faut ouvrir un fichier .prj ou .seq
#   suite à un appel extérieur (explorateur Windows)
#
####################################################################################
myEVT_APPEL_OUVRIR = wx.NewEventType()
EVT_APPEL_OUVRIR = wx.PyEventBinder(myEVT_APPEL_OUVRIR, 1)

#----------------------------------------------------------------------
class AppelEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.file = None
        
        
    ######################################################################################  
    def SetFile(self, file):
        self.file = file
        
    ######################################################################################  
    def GetFile(self):
        return self.file
    
    
def testRel(lien, path):
    try:
        return os.path.relpath(lien,path)
    except:
        return lien
    
######################################################################################  
def toDefautEncoding(path): 
#        try:
    path = path.decode(FILE_ENCODING)
    path = path.encode(DEFAUT_ENCODING)
    return path  
#        except:
#            return self.path    
    
######################################################################################  
def toFileEncoding(path):
    try:
        path = path.decode(DEFAUT_ENCODING)
        return path.encode(FILE_ENCODING)
    except:
        return path
    
######################################################################################  
def rallonge(txt):
    return u" "+txt+" "

######################################################################################  
def remplaceLF2Code(txt):
    return txt.replace("\n", "##13##")#.replace("\n", "##13##")#&#13")
    
######################################################################################  
def remplaceCode2LF(txt):
    return txt.replace("##13##", "\n")#&#13")
    
####################################################################################
#
#   Objet lien vers un fichier, un dossier ou bien un site web
#
####################################################################################
class Lien():
    def __init__(self, path = "", typ = ""):
        self.path = path
        self.type = typ
        
    def __repr__(self):
        return self.type + " : " + self.path
        
    ######################################################################################  
    def DialogCreer(self, pathseq):
        dlg = URLDialog(None, self, pathseq)
        dlg.ShowModal()
        dlg.Destroy() 
            

    ######################################################################################  
    def Afficher(self, pathseq, fenSeq = None):
        path = self.GetAbsPath(pathseq)
        
        if self.type == "f":
            try:
                os.startfile(path)
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'ouvrir le fichier\n\n%s!\n" %toDefautEncoding(path))
                
        elif self.type == 'd':
            try:
                subprocess.Popen(["explorer", path])
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'accéder au dossier\n\n%s!\n" %toDefautEncoding(path))
            
        elif self.type == 'u':
            try:
#                lien_safe = urllib.quote_plus(self.path)
    #            urllib.urlopen(lien_safe)
                webbrowser.open(self.path)
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'ouvrir l'url\n\n%s!\n" %toDefautEncoding(self.path))
        
        elif self.type == 's':
            if os.path.isfile(path):
#                self.Show(False)
                child = fenSeq.commandeNouveau()
                child.ouvrir(path)

  
    ######################################################################################  
    def EvalTypeLien(self, pathseq):
        path = self.GetAbsPath(pathseq)
        
        if os.path.exists(path):
            if os.path.isfile(path):
                self.type = 'f'
                
            elif os.path.isdir(path):
                self.type = 'd'

        else:
            self.type = 'u'
        
                
    ######################################################################################  
    def EvalLien(self, path, pathseq):
        if path == "" or path.split() == []:
            self.path = ""
            self.type = ""
            return
        
        path = toFileEncoding(path)
        pathseq = toFileEncoding(pathseq)
        abspath = self.GetAbsPath(pathseq, path)
        
        relpath = testRel(abspath, pathseq)
        if os.path.exists(relpath):
            if os.path.isfile(relpath):
                self.type = 'f'
                self.path = relpath
            elif os.path.isdir(relpath):
                self.type = 'd'
                self.path = relpath
        else:
            self.type = 'u'
            self.path = path
        
              
    ######################################################################################  
    def GetAbsPath(self, pathseq, path = None):
        if path == None:
            path = self.path
        
#        path = self.GetEncode(path)
        if os.path.exists(path):
            path = path
        else:
#            pathseq = self.GetEncode(pathseq)
            print pathseq
            path = os.path.join(pathseq, path)
        return path
    
    
   
    
    ######################################################################################  
    def getBranche(self, branche):
        branche.set("Lien", self.path)
        branche.set("TypeLien", self.type)
        
        
    ######################################################################################  
    def setBranche(self, branche, pathseq):
        self.path = branche.get("Lien", "")
        self.type = branche.get("TypeLien", "")
        if self.type == "" and self.path != "":
            self.EvalTypeLien(pathseq)
        return True

    
####################################################################################
#
#   Classe définissant les propriétés d'une séquence ou d'un projet
#
####################################################################################
Titres = [u"Séquence pédagogique",
          u"Prérequis",
          u"Objectifs pédagogiques",
          u"Séances",
          u"Systèmes et matériels",
          u"Classe",
          u"Elèves",
          u"Support",
          u"Tâches",
          u"Projet", 
          u"Equipe pédagogique"]

class ElementDeSequence():
    def __init__(self):
        self.lien = Lien()
        
    
    ######################################################################################  
    def GetPath(self):
        return self.parent.GetPath()
    
    ######################################################################################  
    def GetLien(self):
        return self.lien.path
    
    ######################################################################################  
    def GetLienHTML(self):
        if self.lien.type in ['f', 'd', 's']:
            if self.lien.path != '':
                return 'file:///' + os.path.abspath(self.lien.path)
            else:
                return ''
        else:
            return self.lien.path
    
    ######################################################################################  
    def CreerLien(self, event):
        self.lien.DialogCreer(self.GetPath())
        self.SetLien()
        if hasattr(self, 'panelPropriete'): 
            self.panelPropriete.sendEvent()
    
    
    ######################################################################################  
    def SetLien(self, lien = None):
        if hasattr(self, 'tip_titrelien'):
            self.tip.SetLien(self.lien, self.tip_titrelien, self.tip_ctrllien)

        if hasattr(self, 'panelPropriete'): 
            self.panelPropriete.MiseAJourLien()
        
        if hasattr(self, 'sousSeances'):
            for sce in self.sousSeances:
                sce.SetLien()
          
            
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        if hasattr(self, 'panelPropriete'): 
            self.panelPropriete.SetPathSeq(pathSeq)
     
        
    ######################################################################################  
    def AfficherLien(self, pathseq): 
        self.lien.Afficher(pathseq)
        
        
    ######################################################################################  
    def OnPathModified(self):
        if hasattr(self, 'tip_titrelien'):
            self.tip.SetLien(self.lien, self.tip_titrelien, self.tip_ctrllien)
        
        

        
class LienSequence():
    def __init__(self, parent, panelParent, path = ""):
        self.path = path
        self.parent = parent
        self.panelPropriete = PanelPropriete_LienSequence(panelParent, self)
        self.panelParent = panelParent
        
        #
        # Création du Tip (PopupInfo)
        #
        self.tip = PopupInfo(self.parent.app, u"Séquence requise")
        self.tip_titre = self.tip.CreerTexte((1,0))
        self.tip_titrelien, self.tip_ctrllien = self.tip.CreerLien((2,0))
        self.tip_image = self.tip.CreerImage((3,0))
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du lien de sequence pour enregistrement
        """
        root = ET.Element("Sequence")
        root.set("dir", self.path)
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        self.path = branche.get("dir", "")
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Séquence :", wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Seq"])
        
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerSequencePre, item = itemArbre)],
                                                    ])
            
    ######################################################################################  
    def SetLabel(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.GetNomFichier())
        
    ######################################################################################  
    def SetImage(self, bmp):
        self.tip.SetImage(bmp, self.tip_image)

    ######################################################################################  
    def SetLien(self):
        self.tip.SetLien(Lien(self.path, 's'), self.tip_titrelien, self.tip_ctrllien)
    
    ######################################################################################  
    def SetTitre(self, titre):
        self.tip.SetTexte(titre, self.tip_titre)
        
    ######################################################################################  
    def GetNomFichier(self):
        return os.path.splitext(os.path.basename(self.path))[0]
     
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
            return self.branche


class Objet_sequence():
    def __init__(self):
        self.elem = None
        
    def SetSVGTitre(self, p, titre):
        titre = titre.decode(DEFAUT_ENCODING)
        titre = titre.encode('utf-8')
        self.elem.setAttribute("xlink:title", titre)
     
    def SetSVGLien(self, p, lien):
        lien = lien.decode(FILE_ENCODING)
        lien = lien.encode('utf-8')
        self.elem.setAttribute("xlink:href", lien)
        self.elem.setAttribute("target", "_top")
        
    def EncapsuleSVG(self, doc, p):
        self.elem = doc.createElement("a")
        parent=p.parentNode
        parent.insertBefore(self.elem, p)
        self.elem.appendChild(p)
        return self.elem


        
    ######################################################################################  
    def EnrichiSVG(self, doc, seance = False):

        pid = ''
        for p, f in self.cadre:
            if type(f) == str:
                pid = f
                p.setAttribute('filter', 'none')
                p.setAttribute("id",  pid)
                p.setAttribute("onmouseout",  "setAttribute('filter', 'none')")
                p.setAttribute("onmouseover", "setAttribute('filter', 'url(#f1)')")
                break
        
        for i, (p, f) in enumerate(self.cadre):
            if type(f) != str:
                self.EncapsuleSVG(doc, p)
                titre = self.GetBulleSVG(f)
                self.SetSVGTitre(p, titre)
                p.setAttribute("id",  self.GetCode(f)+str(f))
                p.setAttribute("pointer-events",  'all')
                
                if pid == '':
                    p.setAttribute("onmouseout",  "setAttribute('filter', 'none')")
                    p.setAttribute("onmouseover", "setAttribute('filter', 'url(#f1)')")
                    
                else:
                    p.setAttribute("onmouseout",  "evt.target.parentNode.parentNode.parentNode.getElementById('%s').setAttribute('filter', 'none');" %pid)
                    p.setAttribute("onmouseover", "evt.target.parentNode.parentNode.parentNode.getElementById('%s').setAttribute('filter', 'url(#f1)');" %pid)
        
                if hasattr(self, 'GetLien'):
#                    lien = toDefautEncoding(self.GetLienHTML())
                    lien = self.GetLienHTML()
    
                    if lien != '':
                        self.SetSVGLien(p, lien)
        
            if seance:
                att0 = p.getAttribute("onmouseout")
                att1 = p.getAttribute("onmouseover")
                
                n = range(len(self.cadre))
                n.remove(i)
                for j in n:
                    Id = self.GetCode(f)+str(j)
                    att0 += "; evt.target.parentNode.parentNode.parentNode.getElementById('%s').setAttribute('filter', 'none')" %Id
                    att1 += "; evt.target.parentNode.parentNode.parentNode.getElementById('%s').setAttribute('filter', 'url(#f1)')" %Id

                p.setAttribute("onmouseout", att0)
                p.setAttribute("onmouseover", att1)
        
    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        if hasattr(self, 'pts_caract' ):
            for i, pt in enumerate(self.pts_caract):
                lst.append((pt, self, i))
        
        if hasattr(self, 'pt_caract' ):
            lst.append((self.pt_caract[0], self, self.pt_caract[1]))
            
        self.cadre = []
        return lst
    
    ######################################################################################  
    def GetBulleSVG(self, i):
        return self.GetCode(i) + " : " + self.GetIntit(i)
    
            
    ######################################################################################  
    def GetTypeEnseignement(self, simple = False):
        if hasattr(self, 'parent'):
            cl = self.parent.classe
        else:
            cl = self.classe
            
        if simple:
            return cl.familleEnseignement
        
        return cl.typeEnseignement
        
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
            return self.branche
        
        
        
        
        
        
        
class Classe():
    def __init__(self, app, panelParent = None, intitule = u"", pourProjet = False):
        self.intitule = intitule
        
        self.etablissement = u""
        
        self.options = app.options
        self.Initialise(pourProjet)
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Classe(panelParent, self, pourProjet)
            
        self.panelParent = panelParent
#        self.app = app
        
    ######################################################################################  
    def __repr__(self):
        return self.typeEnseignement
        return self.posCI_ET[0] + " " + self.ci_ET[0]
    
    ######################################################################################  
    def Initialise(self, pourProjet):
        self.typeEnseignement = self.options.optClasse["TypeEnseignement"]
        
        if not pourProjet:
            self.ci_ET = self.options.optClasse["CentresInteretET"]
            self.posCI_ET = self.options.optClasse["PositionsCI_ET"]
        else:
            if not self.typeEnseignement in constantes.EnseignementsProjet:
                self.typeEnseignement = 'ITEC'

        self.familleEnseignement = constantes.FamilleEnseignement[self.typeEnseignement]  
         
        self.effectifs =  {"C" : constantes.Effectifs["C"],
                           "G" : constantes.NbrGroupes["G"],
                           "E" : constantes.NbrGroupes["E"],
                           "P" : constantes.NbrGroupes["P"]}
        
        
#        self.effectifs = constantes.Effectifs
        self.effectifs['C'] = self.options.optClasse["Effectifs"]['C']

        self.nbrGroupes = {"P" : self.options.optClasse["Effectifs"]["P"],
                           "E" : self.options.optClasse["Effectifs"]["E"],
                           "G" : self.options.optClasse["Effectifs"]["G"]
                           }

        calculerEffectifs(self)
        
    ######################################################################################  
    def SetDocument(self, doc):   
        self.doc = doc 
        
    
    ######################################################################################  
    def getBranche(self):
        # La classe
        classe = ET.Element("Classe")
        classe.set("Type", self.typeEnseignement)
        
        classe.set("Etab", self.etablissement)
        
        eff = ET.SubElement(classe, "Effectifs")
        eff.set('eC', str(self.effectifs['C']))
        eff.set('nG', str(self.nbrGroupes['G']))
        eff.set('nE', str(self.nbrGroupes['E']))
        eff.set('nP', str(self.nbrGroupes['P']))
                      
        if self.typeEnseignement == 'ET':
            ci = ET.SubElement(classe, "CentreInteret")
            for i,c in enumerate(self.ci_ET):
                ci.set("CI"+str(i+1), c)
                ci.set("pos"+str(i+1), self.posCI_ET[i])
        return classe
    
    ######################################################################################  
    def setBranche(self, branche):
        Ok = True
#        print "setBranche classe",
        self.typeEnseignement = branche.get("Type", "ET")
        
        self.etablissement = branche.get("Etab", u"")
        
        self.familleEnseignement = constantes.FamilleEnseignement[self.typeEnseignement]
#        print self.typeEnseignement
        
        brancheCI = branche.find("CentreInteret")
        if brancheCI != None: # Uniquement pour rétrocompatibilité : normalement cet élément existe !
            continuer = True
            i = 1
            ci_ET = []
            posCI_ET = []
            while continuer:
                c = brancheCI.get("CI"+str(i))
                p = brancheCI.get("pos"+str(i))
                if c == None or p == None:
                    continuer = False
                else:
                    ci_ET.append(c)
                    posCI_ET.append(p) 
                    i += 1
                
            if i > 1:
                self.ci_ET = ci_ET
                self.posCI_ET = posCI_ET
            
                
        # Ancien format : <Effectifs C="9" D="3" E="2" G="9" P="3" />
        # Nouveau format : <Effectifs eC="9" nE="2" nG="9" nP="3" />
        brancheEff = branche.find("Effectifs")
        
        if brancheEff.get('eC') == None: # Ancienne version
            self.effectifs['C'] = eval(brancheEff.get('C', "1"))
            revCalculerEffectifs(self, eval(brancheEff.get('G', "1")), eval(brancheEff.get('E', "1")), eval(brancheEff.get('P', "1")))

        else:
            self.effectifs['C'] = eval(brancheEff.get('eC', "1"))
            self.nbrGroupes['G'] = eval(brancheEff.get('nG', "1"))
            self.nbrGroupes['E'] = eval(brancheEff.get('nE', "1"))
            self.nbrGroupes['P'] = eval(brancheEff.get('nP', "1"))
            calculerEffectifs(self)
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()
        
            self.doc.MiseAJourTypeEnseignement()
        
        return Ok
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, rallonge(self.typeEnseignement))
        self.branche = arbre.AppendItem(branche, Titres[5]+" :", wnd = self.codeBranche, data = self)#, image = self.arbre.images["Seq"])



    ######################################################################################  
    def GetEffectifNorm(self, eff):
        """ Renvoie les effectifs des groupes sous forme normalisée
            (portion de classe entière)
        """
        if eff == 'C':
            return 1.0
        elif eff == 'G':
            return 1.0 / self.nbrGroupes['G']
        elif eff == 'D':
            return self.GetEffectifNorm('G') / 2
        elif eff == 'E':
            return self.GetEffectifNorm('G') / self.nbrGroupes['E']
        elif eff == 'P':
            return self.GetEffectifNorm('G') / self.nbrGroupes['P']
        
        
        
    ######################################################################################  
    def Verrouiller(self, etat):
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.Verrouiller(etat)
        if etat:
            couleur = 'white'
            message = u""
        else:
            couleur = COUL_OK
            message = u"Les paramètres de la classe sont verrouillés !\n" \
                      u"Pour pouvoir les modifier, supprimer le centre d'intérêt\n"\
                      u"ainsi que les prérequis et les objectifs."
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetBackgroundColour(couleur)
            self.codeBranche.SetToolTipString(message)
            self.codeBranche.Refresh()

####################################################################################################
#
# Classe définissant les documents principaux
#        base : BaseDoc
#        héritiers : Sequence et Projet
#
####################################################################################################
class BaseDoc():   
    def __init__(self, app, classe = None, panelParent = None, intitule = ""):
        self.intitule = intitule
        self.classe = classe
        self.app = app
        self.centrer = True
        
        self.position = 0
        
        self.commentaires = u""
        
        self.panelParent = panelParent
          
    ######################################################################################  
    def GetApp(self):
        return self.app
    
    ######################################################################################  
    def GetPath(self):
        if hasattr(self.app, 'fichierCourant'):
            return os.path.split(self.app.fichierCourant)[0]
        else:
            return ''
    
    ######################################################################################  
    def GetApercu(self, mult = 3):
        imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  210*mult, 297*mult)#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        ctx = cairo.Context(imagesurface)
        ctx.scale(297*mult, 297*mult) 
        self.draw.Draw(ctx, self)
        bmp = wx.lib.wxcairo.BitmapFromImageSurface(imagesurface)
        return bmp
    
    ######################################################################################  
    def SetText(self, text):
        self.intitule = text
    
    ######################################################################################  
    def SetPosition(self, pos):
        self.position = pos  
        
    ######################################################################################  
    def SetCommentaire(self, text):
        self.commentaires = text  
        
    ######################################################################################  
    def AfficherLien(self, item):
        data = self.arbre.GetItemPyData(item)
        if data and data != self and hasattr(data, 'AfficherLien'):
            data.AfficherLien(self.GetPath())

    ######################################################################################  
    def SelectItem(self, branche, depuisFiche = False):
        self.centrer = not depuisFiche
        self.arbre.SelectItem(branche)  
        
        
####################################################################################################          
class Sequence(BaseDoc):
    def __init__(self, app, classe = None, panelParent = None, intitule = u"Intitulé de la séquence pédagogique"):
        BaseDoc.__init__(self, app, classe, panelParent, intitule)
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Sequence(panelParent, self)
            self.panelSeances = PanelPropriete_Racine(panelParent, constantes.TxtRacineSeance)
            self.panelObjectifs = PanelPropriete_Racine(panelParent, constantes.TxtRacineObjectif)
            self.panelSystemes = PanelPropriete_Racine(panelParent, constantes.TxtRacineSysteme)
        
        self.prerequis = Savoirs(self, panelParent, prerequis = True)
        self.prerequisSeance = []
        
        self.CI = CentreInteret(self, panelParent)
        
        self.obj = {"C" : Competences(self, panelParent),
                    "S" : Savoirs(self, panelParent)}
        self.systemes = []
        self.seance = [Seance(self, panelParent)]
        
        self.options = classe.options
        
        self.draw = draw_cairo_seq
        
        
    ######################################################################################  
    def __repr__(self):
        return self.intitule
        t = u"Séquence :"+ + "\n"
        t += "   " + self.CI.__repr__() + "\n"
        for c in self.obj.values():
            t += "   " + c.__repr__() + "\n"
        for s in self.seance:
            t += "   " + s.__repr__() + "\n"
        return t

    ######################################################################################  
    def Initialise(self):
        self.AjouterListeSystemes(zip(self.options.optSystemes["Systemes"], 
                                      self.options.optSystemes["Nombre"]))
            
            
            
    ######################################################################################  
    def SetPath(self, fichierCourant):
        pathseq = os.path.split(fichierCourant)[0]
        for sce in self.seance:
            sce.SetPathSeq(pathseq)    
        for sy in self.systemes:
            sy.SetPathSeq(pathseq) 
        
    ######################################################################################  
    def GetDuree(self):
        duree = 0
        for s in self.seance:
            duree += s.GetDuree()
        return duree
                  
    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        lst.extend(self.obj["C"].GetPtCaract())
        lst.extend(self.obj["S"].GetPtCaract())
        lst.extend(self.prerequis.GetPtCaract())
        lst.extend(self.CI.GetPtCaract())
        for s in self.seance:
            lst.extend(s.GetPtCaract())
        return lst    
    
    
    ######################################################################################  
    def EnrichiSVG(self, doc):
        self.obj["C"].EnrichiSVG(doc)
        self.obj["S"].EnrichiSVG(doc)
        self.prerequis.EnrichiSVG(doc)
        self.CI.EnrichiSVG(doc)
        for s in self.seance:
            s.EnrichiSVGse(doc)
        
        
    ######################################################################################  
    def GetDureeGraph(self):
        duree = 0
        for s in self.seance:
            duree += s.GetDureeGraph()
        return duree
            
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la séquence pour enregistrement
        """
        # Création de la racine
        sequence = ET.Element("Sequence")
        
        sequence.set("Intitule", self.intitule)

        if self.commentaires != u"":
            sequence.set("Commentaires", self.commentaires)

        sequence.set("Position", str(self.position))

        sequence.append(self.CI.getBranche())
        
        prerequis = ET.SubElement(sequence, "Prerequis")
        prerequis.append(self.prerequis.getBranche())
        for ps in self.prerequisSeance:
            prerequis.append(ps.getBranche())
        
        objectifs = ET.SubElement(sequence, "Objectifs")
        for obj in self.obj.values():
            objectifs.append(obj.getBranche())
            
        seances = ET.SubElement(sequence, "Seances")
        for sce in self.seance:
            seances.append(sce.getBranche())
            
        systeme = ET.SubElement(sequence, "Systemes")
        for sy in self.systemes:
            systeme.append(sy.getBranche())
        
        return sequence
        
    ######################################################################################  
    def setBranche(self, branche, ):
        self.intitule = branche.get("Intitule", u"")
        
        self.commentaires = branche.get("Commentaires", u"")
        
        self.position = eval(branche.get("Position", "0"))

        brancheCI = branche.find("CentresInteret")
        if brancheCI != None:
            self.CI.setBranche(brancheCI)
        
        # Pour rétro compatibilité
        if self.CI.numCI == []:
            brancheCI = branche.find("CentreInteret")
            if brancheCI != None:
                self.CI.setBranche(brancheCI)
        
        branchePre = branche.find("Prerequis")
        if branchePre != None:
            savoirs = branchePre.find("Savoirs")
            self.prerequis.setBranche(savoirs)
            lst = list(branchePre)
            lst.remove(savoirs)
            self.prerequisSeance = []
            if hasattr(self, 'panelPropriete'):
                for bsp in lst:
                    sp = LienSequence(self, self.panelParent)
                    sp.setBranche(bsp)
                    self.prerequisSeance.append(sp)
        
        
        brancheObj = branche.find("Objectifs")
#        self.obj = []
#        for obj in list(brancheObj):
#            comp = Competence(self, self.panelParent)
#            comp.setBranche(obj)
#            self.obj.append(comp)
        self.obj["C"].setBranche(list(brancheObj)[0])
        self.obj["S"].setBranche(list(brancheObj)[1])
        brancheSys = branche.find("Systemes")
        self.systemes = []
        for sy in list(brancheSys):
            systeme = Systeme(self, self.panelParent)
            systeme.setBranche(sy)
            self.systemes.append(systeme)    

        brancheSce = branche.find("Seances")
        self.seance = []
        for sce in list(brancheSce):         
            seance = Seance(self, self.panelParent)
            seance.setBranche(sce)
            self.seance.append(seance)
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()

        
    
        
    ######################################################################################  
    def SetCodes(self):
#        self.CI.SetNum()
#        for comp in self.obj:
#            comp.SetCode()
#        self.obj["C"].SetCode()
#        self.obj["S"].SetCode()
        
        for sce in self.seance:
            sce.SetCode()    
            
        for sy in self.systemes:
            sy.SetCode()    
        
        for ps in self.prerequisSeance:
            ps.SetLabel()
            
    ######################################################################################  
    def PubDescription(self):
        for sce in self.seance:
            sce.PubDescription()    
#            
#        for sy in self.systemes:
#            sy.SetDescription()    
        

            
            
    ######################################################################################  
    def SetLiens(self):
        for sce in self.seance:
            sce.SetLien()    

        for sy in self.systemes:
            sy.SetLien()  

        
    ######################################################################################  
    def VerifPb(self):
        for s in self.seance:
            s.VerifPb()
        
    ######################################################################################  
    def MiseAJourNomsSystemes(self):
        for s in self.seance:
            s.MiseAJourNomsSystemes()
    
    ######################################################################################  
    def AjouterSystemeSeance(self):
        for s in self.seance:
            s.AjouterSysteme()
            
    ######################################################################################  
    def AjouterListeSystemesSeance(self, lstSys):
        for s in self.seance:
            s.AjouterListeSystemes(lstSys)
            
    ######################################################################################  
    def SupprimerSystemeSeance(self, i):
        for s in self.seance:
            s.SupprimerSysteme(i) 
            
            
                   
    ######################################################################################  
    def AjouterSeance(self, event = None):
        seance = Seance(self, self.panelParent)
        self.seance.append(seance)
        self.OrdonnerSeances()
        seance.ConstruireArbre(self.arbre, self.brancheSce)
        self.panelPropriete.sendEvent()
        
        self.arbre.SelectItem(seance.branche)
        
        return seance
    
    
    ######################################################################################  
    def SupprimerSeance(self, event = None, item = None):
        if len(self.seance) > 1: # On en laisse toujours une !!
            seance = self.arbre.GetItemPyData(item)
            self.seance.remove(seance)
            self.arbre.Delete(item)
            self.OrdonnerSeances()
            self.panelPropriete.sendEvent()
            return True
        return False
    
    
    ######################################################################################  
    def OrdonnerSeances(self):
        for i, sce in enumerate(self.seance):
            sce.ordre = i
            sce.OrdonnerSeances()
        
        self.SetCodes()
    
#    ######################################################################################  
#    def AjouterObjectif(self, event = None):
#        obj = Competence(self, self.panelParent)
#        self.obj.append(obj)
#        obj.ConstruireArbre(self.arbre, self.brancheObj)
#        self.panelPropriete.sendEvent()
#        return
    
    ######################################################################################  
    def SupprimerItem(self, item):
        data = self.arbre.GetItemPyData(item)
        if isinstance(data, Seance):
            if data.EstSousSeance():
                data.parent.SupprimerSeance(item = item)
            else:
                self.SupprimerSeance(item = item)
            
        elif isinstance(data, Systeme):
            self.SupprimerSysteme(item = item)
            
        elif isinstance(data, LienSequence):
            self.SupprimerSequencePre(item = item)           
        
    
    ######################################################################################  
    def SupprimerSequencePre(self, event = None, item = None):
        ps = self.arbre.GetItemPyData(item)
        self.prerequisSeance.remove(ps)
        self.arbre.Delete(item)
        self.panelPropriete.sendEvent()
        
    ######################################################################################  
    def AjouterSequencePre(self, event = None):
        ps = LienSequence(self, self.panelParent)
        self.prerequisSeance.append(ps)
        ps.ConstruireArbre(self.arbre, self.branchePre)
        self.panelPropriete.sendEvent()
        self.arbre.SelectItem(ps.branche)
        
        
    ######################################################################################  
    def AjouterSysteme(self, event = None):
        sy = Systeme(self, self.panelParent)
        self.systemes.append(sy)
        sy.ConstruireArbre(self.arbre, self.brancheSys)
        self.arbre.Expand(self.brancheSys)
        self.panelPropriete.sendEvent()
        self.arbre.SelectItem(sy.branche)
        self.AjouterSystemeSeance()
        return
    
    ######################################################################################  
    def AjouterListeSystemes(self, propr = []):
        nouvListe = []
        for p in propr:
            sy = Systeme(self, self.panelParent)
            self.systemes.append(sy)
            nouvListe.append(sy.nom)
            sy.ConstruireArbre(self.arbre, self.brancheSys)
            self.arbre.Expand(self.brancheSys)
            sy.SetNom(unicode(p[0]))
            if len(p) > 1:
                sy.nbrDispo.v[0] = eval(p[1])
            sy.panelPropriete.MiseAJour()
        self.panelPropriete.sendEvent()
        self.AjouterListeSystemesSeance(nouvListe)
        return
    
    ######################################################################################  
    def SupprimerSysteme(self, event = None, item = None):
        sy = self.arbre.GetItemPyData(item)
        i = self.systemes.index(sy)
        self.systemes.remove(sy)
        self.arbre.Delete(item)
        self.SupprimerSystemeSeance(i)
        self.panelPropriete.sendEvent()
    
    ######################################################################################  
    def SelectSystemes(self, event = None):
        if recup_excel.ouvrirFichierExcel():
            dlg = wx.MessageDialog(self.app, u"Sélectionner une liste de systèmes\n" \
                                             u"dans le classeur Excel qui vient de s'ouvrir,\n" \
                                             u"puis appuyer sur Ok.\n\n" \
                                             u"Format attendu de la selection :\n" \
                                             u"|    colonne 1\t|    colonne 2 \t|    colonne 3  \t|\n" \
                                             u"|                  \t|    (optionnelle)  \t|    (optionnelle)   \t|\n" \
                                             u"|  systèmes  \t|  nombre dispo\t| fichiers image\t|\n" \
                                             u"|  ...               \t|  ...                \t|  ...               \t|\n",
                                             u'Sélection de systèmes',
                                             wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                             )
            res = dlg.ShowModal()
            dlg.Destroy() 
            if res == wx.ID_YES:
                ls = recup_excel.getSelectionExcel()
                self.AjouterListeSystemes(ls)
            elif res == wx.ID_NO:
                print "Rien" 
        
    ######################################################################################  
    def SauvSystemes(self, event = None):
        self.classe.options.validerSystemes(self)
        self.classe.options.enregistrer()
        try:
            pass
            
        except IOError:
            messageErreur(self.GetApp(), u"Permission refusée",
                          u"Permission d'enregistrer les préférences refusée.\n\n" \
                          u"Le dossier est protégé en écriture")
        except:
            messageErreur(self.GetApp(), u"Enregistrement impossible",
                          u"Imposible d'enregistrer les préférences\n\n")
        return
    
    ######################################################################################  
    def AjouterRotation(self, seance):
        seanceR1 = Seance(self.panelParent)
        seance.sousSeances.append(seanceR1)
        return seanceR1
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, Titres[0], data = self, image = self.arbre.images["Seq"])
        self.arbre.SetItemBold(self.branche)
        #
        # LE centre d'intérêt
        #
        self.CI.ConstruireArbre(arbre, self.branche)
        
        #
        # Les prérequis
        #
        self.branchePre = arbre.AppendItem(self.branche, Titres[1], 
                                           data = self.prerequis, 
                                           image = self.arbre.images["Sav"])
        for ps in self.prerequisSeance:
            ps.ConstruireArbre(arbre, self.branchePre)
        #
        # Les objectifs
        #
        self.brancheObj = arbre.AppendItem(self.branche, Titres[2], image = self.arbre.images["Obj"], data = self.panelObjectifs)
        for obj in self.obj.values():
            obj.ConstruireArbre(arbre, self.brancheObj)
            
        
        self.brancheSce = arbre.AppendItem(self.branche, Titres[3], image = self.arbre.images["Sea"], data = self.panelSeances)
        self.arbre.SetItemBold(self.brancheSce)
        for sce in self.seance:
            sce.ConstruireArbre(arbre, self.brancheSce) 
            
        self.brancheSys = arbre.AppendItem(self.branche, Titres[4], image = self.arbre.images["Sys"], data = self.panelSystemes)
        for sy in self.systemes:
            sy.ConstruireArbre(arbre, self.brancheSys)    
        
        
        
    ######################################################################################  
    def reconstruireBrancheSeances(self, b1, b2):
        self.arbre.DeleteChildren(self.brancheSce)
        for sce in self.seance:
            sce.ConstruireArbre(self.arbre, self.brancheSce) 
        self.arbre.Expand(b1.branche)
        self.arbre.Expand(b2.branche)
#        
    
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):    
        """ Affiche le menu contextuel associé é la séquence
            ... ou bien celui de itemArbre concerné ...
        """
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([[u"Enregistrer", self.app.commandeEnregistrer],
#                                             [u"Ouvrir", self.app.commandeOuvrir],
                                             [u"Exporter la fiche (PDF ou SVG)", self.app.exporterFiche],
                                            ])
            
#        [u"Séquence pédagogique",
#          u"Prérequis",
#          u"Objectifs pédagogiques",
#          u"Séances",
#          u"Systèmes"]
        
#        elif isinstance(self.arbre.GetItemPyData(itemArbre), Competences):
#            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Seance):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Systeme):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), LienSequence):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
#        elif self.arbre.GetItemText(itemArbre) == Titres[1]: # Objectifs pédagogiques
#            self.app.AfficherMenuContextuel([[u"Ajouter une compétence", self.AjouterObjectif]])
            
            
        elif self.arbre.GetItemText(itemArbre) == Titres[3]: # Séances
            self.app.AfficherMenuContextuel([[u"Ajouter une séance", self.AjouterSeance]])
            
        elif self.arbre.GetItemText(itemArbre) == Titres[4]: # Système
            self.app.AfficherMenuContextuel([[u"Ajouter un système", self.AjouterSysteme], 
                                             [u"Selectionner depuis un fichier", self.SelectSystemes],
                                             [u"Sauvegarder la liste dans les préférences", self.SauvSystemes]])
         
        elif self.arbre.GetItemText(itemArbre) == Titres[1]: # Prérequis
            self.app.AfficherMenuContextuel([[u"Ajouter une séquence", self.AjouterSequencePre], 
                                             ])
         
            
    ######################################################################################       
    def GetSystemesUtilises(self):
        """ Renvoie la liste des systèmes utilisés pendant la séquence
        """
        lst = []
        for s in self.systemes:
            n = 0
            for se in self.seance:
                ns = se.GetNbrSystemes(complet = True)
                if s.nom in ns.keys():
                    n += ns[s.nom]
            if n > 0:
                lst.append(s)
        return lst
    
            
    ######################################################################################  
    def GetNbreSeances(self):
        n = 0
        for s in self.seance:
            if s.typeSeance in ["R", "S"]:
                n += len(s.sousSeances)
            n += 1
        return n
    
    
    ######################################################################################  
    def GetToutesSeances(self):
        l = []
        for s in self.seance:
            l.append(s)
            if s.typeSeance in ["R", "S"]:
                l.extend(s.GetToutesSeances())
            
        return l 

    ######################################################################################  
    def GetNbrSystemes(self):
        dic = {}
        for s in self.GetToutesSeances():
            d = s.GetNbrSystemes()
            for k, v in d.items():
                if k in dic.keys():
                    dic[k] += v
                else:
                    dic[k] = v
        return dic
                    
        
    ######################################################################################  
    def GetIntituleSeances(self):
        nomsSeances = []
        intSeances = []
        for s in self.GetToutesSeances():
            if hasattr(s, 'code') and s.intitule != "" and not s.intituleDansDeroul:
                nomsSeances.append(s.code)
                intSeances.append(s.intitule)
        return nomsSeances, intSeances
        
        

        
    ######################################################################################  
    def HitTest(self, x, y):     
        if self.CI.HitTest(x, y):
            return self.CI.HitTest(x, y)

        elif dansRectangle(x, y, (draw_cairo_seq.posPre + draw_cairo_seq.taillePre,))[0]:
            for ls in self.prerequisSeance:
                h = ls.HitTest(x,y)
                if h != None:
                    return h
            return self.branchePre
        
        else:
            branche = None
            autresZones = self.seance + self.systemes + self.obj.values()
            continuer = True
            i = 0
            while continuer:
                if i >= len(autresZones):
                    continuer = False
                else:
                    branche = autresZones[i].HitTest(x, y)
                    if branche:
                        continuer = False
                i += 1
            
            if branche == None:
                if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
                    return self.branche
                
            return branche
        
    ######################################################################################  
    def HitTestPosition(self, x, y):
        if hasattr(self, 'rectPos'):
            for i, rectPos in enumerate(self.rectPos):
                if dansRectangle(x, y, (rectPos,))[0]:
                    return i
                    
                                    
                                    
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        self.app.SetTitre()
        self.CI.MiseAJourTypeEnseignement()
        for o in self.obj.values():
            o.MiseAJourTypeEnseignement()
        self.prerequis.MiseAJourTypeEnseignement()
        for s in self.seance:
            s.MiseAJourTypeEnseignement()
        
        
    #############################################################################
    def VerrouillerClasse(self):
        if hasattr(self, 'CI') \
            and (self.CI.numCI != [] or self.prerequis.savoirs != [] \
                 or self.obj['C'].competences != [] or self.obj['S'].savoirs != []):
            self.classe.Verrouiller(False)
        else:
            if self.classe != None:
                self.classe.Verrouiller(True)
        
        
        
        
####################################################################################################
class Projet(BaseDoc, Objet_sequence):
    def __init__(self, app, classe = None, panelParent = None, intitule = u""):
        BaseDoc.__init__(self, app, classe, panelParent, intitule)
        Objet_sequence.__init__(self)
        self.position = 5
        self.nbrParties = 1
        
        # Par défaut, la revue 1 est après la Conception détaillée
        self.R1avantConception = False
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Projet(panelParent, self)
            self.panelEleves = PanelPropriete_Racine(panelParent, constantes.TxtRacineEleve)
            self.panelTaches = PanelPropriete_Racine(panelParent, constantes.TxtRacineTache)
            self.panelEquipe = PanelPropriete_Racine(panelParent, constantes.TxtRacineEquipe)
        
        self.eleves = []
        
        self.taches = self.creerTachesRevue()
            
        self.equipe = []
        
        self.support = Support(self, panelParent)
        
        self.problematique = u""
        
        # Spécifiquement pour la fiche de validation
        self.origine = u""
        self.contraintes = u""
        self.besoinParties = u""
        self.intituleParties = u""

        self.production = u""
        
        
        self.SetPosition(5)
        
        
#       
        
        
    ######################################################################################  
    def __repr__(self):
        return self.intitule

    
#    ######################################################################################  
#    def SetPath(self, fichierCourant):
#        pathseq = os.path.split(fichierCourant)[0]
#        for t in self.taches:
#            t.SetPathSeq(pathseq)    
#        for sy in self.systemes:
#            sy.SetPathSeq(pathseq) 
        
    ######################################################################################  
    def GetDuree(self):
        duree = 0
        for t in self.taches:
            duree += t.GetDuree()
        return duree
                  
    ######################################################################################  
    def GetDureeGraph(self):
        duree = 0
        for t in self.taches:
            duree += t.GetDureeGraph()
        return duree
    
    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        
        for i, pt in enumerate(self.pt_caract_comp):
            lst.append((pt, self, i))
            
        for i, pt in enumerate(self.pt_caract_eleve):
            lst.append((pt, self, -1-i))    
            
        lst.extend(self.support.GetPtCaract())
        
        for s in self.taches + self.eleves:
            lst.extend(s.GetPtCaract())
            
        self.cadre = []
        return lst    
    
    
    ######################################################################################  
    def creerTachesRevue(self):
        lst = []
        for p in ["R1", "R2", "S"]:
            lst.append(Tache(self, self.panelParent, 
                             intitule = constantes.NOM_PHASE_TACHE_E[p], 
                             phaseTache = p, duree = 0.5))
        return lst
    
    ######################################################################################  
    def getTachesRevue(self):
        lst = []
        for t in self.taches:
            if t.phase in ["R1", "R2", "S"]:
                lst.append(t)
        return lst
        
        
    ######################################################################################  
    def EnrichiObjetsSVG(self, doc):
        for s in self.taches:
            s.EnrichiSVG(doc)
        self.support.EnrichiSVG(doc)
        self.EnrichiSVG(doc)
#        self.obj["C"].EnrichiSVG(doc)
#        self.obj["S"].EnrichiSVG(doc)
#        self.prerequis.EnrichiSVG(doc)
#        self.CI.EnrichiSVG(doc)
#        for s in self.seance:
#            s.EnrichiSVGse(doc)
        return
            
    
    ######################################################################################  
    def GetBulleSVG(self, i):
        if i >= 0:
            c = self.GetCompetencesUtil()
            return c[i] + " : " + constantes.dicCompetences_prj_simple[self.classe.typeEnseignement][c[i]]
        else:
            e = self.eleves[-1-i]
            t = e.GetNomPrenom()+"\n"
            t += u"Durée d'activité : "+draw_cairo.getHoraireTxt(e.GetDuree())+"\n"
            t += u"Evaluabilité :\n"
            r, s = e.GetEvaluabilite()
            t += u"\trevues : "+str(int(r*100))+"%\n"
            t += u"\tsoutenance : "+str(int(s*100))+"%\n"
            return t
            
            
            
    ######################################################################################  
    def GetCode(self, i = None):
        return u"Projet"
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du projet pour enregistrement
        """
        # Création de la racine
        projet = ET.Element("Projet")
        
        projet.set("Intitule", self.intitule)
        
        projet.set("Problematique", remplaceLF2Code(self.problematique))
#
        if self.commentaires != u"":
            projet.set("Commentaires", self.commentaires)

        projet.set("Position", str(self.position))
        
        projet.set("R1avC", str(self.R1avantConception))
        
        equipe = ET.SubElement(projet, "Equipe")
        for p in self.equipe:
            equipe.append(p.getBranche())
        
        projet.append(self.support.getBranche())
        
        taches = ET.SubElement(projet, "Taches")
        for t in self.taches:
            taches.append(t.getBranche())
        
        eleves = ET.SubElement(projet, "Eleves")
        for e in self.eleves:
            eleves.append(e.getBranche())
            
        #
        # pour la fiche de validation
        #
        projet.set("Origine", remplaceLF2Code(self.origine))
        projet.set("Contraintes", remplaceLF2Code(self.contraintes))
        projet.set("Production", remplaceLF2Code(self.production))
        projet.set("BesoinParties", remplaceLF2Code(self.besoinParties))
        projet.set("IntitParties", remplaceLF2Code(self.intituleParties))
        projet.set("NbrParties", str(self.nbrParties))
#        comp = ET.SubElement(projet, "Competences")
#        for k, lc in constantes.dicCompetences_prj_simple[self.classe.typeEnseignement].items():
#            comp.set(k, str(lc[1]))
        
        return projet
        
    ######################################################################################  
    def setBranche(self, branche):
        Ok = True
       
        self.intitule = branche.get("Intitule", u"")

        self.problematique = remplaceCode2LF(branche.get("Problematique", u""))
        
        self.commentaires = branche.get("Commentaires", u"")
        
        self.R1avantConception = eval(branche.get("R1avC", "False"))
        
        self.position = eval(branche.get("Position", "0"))

        brancheEqu = branche.find("Equipe")
        self.equipe = []
        for i,e in enumerate(list(brancheEqu)):
            prof = Prof(self, self.panelParent)
            Ok = Ok and prof.setBranche(e)
            self.equipe.append(prof)

        brancheSup = branche.find("Support")
        if brancheSup != None:
            Ok = Ok and self.support.setBranche(brancheSup)
        
        brancheEle = branche.find("Eleves")
        self.eleves = []
        for i,e in enumerate(list(brancheEle)):
            eleve = Eleve(self, self.panelParent)
            Ok = Ok and eleve.setBranche(e)
            self.eleves.append(eleve)
        
        #
        # pour la fiche de validation
        #
        self.origine = remplaceCode2LF(branche.get("Origine", u""))
        self.contraintes = remplaceCode2LF(branche.get("Contraintes", u""))
        self.production = remplaceCode2LF(branche.get("Production", u""))
        self.besoinParties = remplaceCode2LF(branche.get("BesoinParties", u""))
        self.intituleParties = remplaceCode2LF(branche.get("IntitParties", u""))
        self.nbrParties = eval(branche.get("NbrParties", "1"))
      
        #
        # Les poids des compétences
        #
#        brancheCmp = branche.find("Competences")
#        if brancheCmp != None:
#            for k, lc in constantes.dicCompetences_prj_simple[self.classe.typeEnseignement].items():
#                lc[1] = eval(brancheCmp.get(k))
        
        
        #
        # Les tâches
        #
        brancheTac = branche.find("Taches")
        tachesRevue = self.getTachesRevue()
        
        self.taches = []
        adapterVersion = True
        for e in list(brancheTac):
            phase = e.get("Phase")
            if phase in ["R1", "R2", "S"]:
                if phase == "S":
                    num = 2
                else:
                    num = eval(phase[1])-1
                Ok = Ok and tachesRevue[num].setBranche(e)
                self.taches.append(tachesRevue[num])
                adapterVersion = False
            else:
                tache = Tache(self, self.panelParent, branche = e)
#                tache.setBranche(e)
                self.taches.append(tache)
        
        
        # Pour récupérer les prj créés avec la version beta1
        if adapterVersion:
            self.taches.extend(tachesRevue)
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()

        return Ok
        
    ######################################################################################  
    def SetPosition(self, pos):
        # On passe à la position 5
        if pos == 5 and self.position != 5:
            for tr in self.creerTachesRevue():
                self.taches.append(tr)
                tr.ConstruireArbre(self.arbre, self.brancheTac)
                tr.SetCode()
                if hasattr(rt, 'panelPropriete'):
                    rt.panelPropriete.MiseAJour()
            self.OrdonnerTaches()
            self.arbre.Ordonner(self.brancheTac)
#            self.panelPropriete.sendEvent()
#            self.taches.extend(self.creerTachesRevue())
#            self.OrdonnerTaches()

                
        # On passe de la position5 à une autre
        elif pos !=5 and self.position == 5:
            lst = []
            for t in self.taches:
                if t.phase in ["R1", "R2", "S"]:
                    lst.append(t.branche)
            for a in lst:
                self.SupprimerTache(item = a)
        
        self.position = pos
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()
        
    ######################################################################################  
    def SetProblematique(self, pb):
        self.problematique = pb
        
    ######################################################################################  
    def SetReferent(self, personne, referent):
        for p in self.equipe:
            if p == personne:
                p.referent = referent
            else:
                if referent:
                    p.referent = False
            p.panelPropriete.MiseAJour()
        self.MiseAJourNomProfs()
        
        
        
    ######################################################################################  
    def SetCodes(self):
        self.support.SetCode()
        
        for sce in self.taches:
            sce.SetCode()    
            
        for sy in self.eleves:
            sy.SetCode()    

            
    ######################################################################################  
    def PubDescription(self):
        self.support.PubDescription()   
        for t in self.taches:
            t.PubDescription()       
         
            
    ######################################################################################  
    def SetLiens(self):
#        for t in self.taches:
#            t.SetLien()    

        self.support.SetLien()  

        
    ######################################################################################  
    def VerifPb(self):
        return

        
    ######################################################################################  
    def MiseAJourNomsEleves(self):
        """ Met à jour les noms des élèves après une modification
            dans les panelPropriété des tâches
        """
        for t in self.taches:
            t.MiseAJourNomsEleves()
        
        
    ######################################################################################  
    def MiseAJourDureeEleves(self):
        for e in self.eleves:
            e.SetCode()
            e.MiseAJourCodeBranche()
    
    
    ######################################################################################  
    def MiseAJourNomProfs(self):
        for e in self.equipe:
            e.SetCode()
            e.MiseAJourCodeBranche()
            
            
#    ######################################################################################  
#    def AjouterSystemeSeance(self):
#        for s in self.seance:
#            s.AjouterSysteme()
#            
#    ######################################################################################  
#    def AjouterListeSystemesSeance(self, lstSys):
#        for s in self.seance:
#            s.AjouterListeSystemes(lstSys)
#            
#    ######################################################################################  
#    def SupprimerSystemeSeance(self, i):
#        for s in self.seance:
#            s.SupprimerSysteme(i) 
            
            
                   
    ######################################################################################  
    def AjouterTache(self, event = None, tache = None):
        if tache == None:
            tache = Tache(self, self.panelParent)
        self.taches.append(tache)
        
#        self.arbre.Freeze()
        tache.ConstruireArbre(self.arbre, self.brancheTac)
        
#        self.arbre.ExpandAll()
#        self.arbre.CalculatePositions()
#        self.arbre.Layout()
#        self.arbre.Update()
#        self.arbre.SelectItem(self.arbre.GetRootItem())
        
        
        self.brancheTac.Collapse()
#        self.arbre.SelectItem(tache.branche)
#        self.brancheTac.Expand()
        self.arbre.CalculatePositions()
        self.arbre.Expand(self.brancheTac)
        self.arbre.SelectItem(tache.branche)
#        self.arbre.AdjustMyScrollbars()
#        wx.CallAfter(self.arbre.CalculatePositions)

        self.panelPropriete.sendEvent()
#        self.arbre.Thaw()
        return tache
    
    
    ######################################################################################  
    def InsererRevue(self, event = None, item = None):
        tache_avant = self.arbre.GetItemPyData(item)
        tache = Tache(self, self.panelParent, phaseTache = "Rev")
        tache.ordre = tache_avant.ordre+1
        for t in self.taches[tache_avant.ordre:]:
            t.ordre += 1
        self.taches.append(tache)
        self.taches.sort(key=attrgetter('ordre'))
        
        tache.ConstruireArbre(self.arbre, self.brancheTac)
        tache.SetCode()
        if hasattr(tache, 'panelPropriete'):
            tache.panelPropriete.MiseAJour()
        
        self.arbre.Ordonner(self.brancheTac)
        self.panelPropriete.sendEvent()
        self.arbre.SelectItem(tache.branche)
            
        
    ######################################################################################  
    def SupprimerTache(self, event = None, item = None):
        tache = self.arbre.GetItemPyData(item)
        self.taches.remove(tache)
        self.arbre.Delete(item)
        self.SetOrdresTaches()
        self.panelPropriete.sendEvent()
        
        
    ######################################################################################  
    def SetOrdresTaches(self):
        for i, tt in enumerate(self.taches):
            tt.ordre = i+1
            tt.SetCode()
        
    ######################################################################################  
    def OrdonnerListeTaches(self, lstTaches):
        #
        # On enregistre les positions des revues intermédiaires (après qui ?)
        #
        Rev = []
        for i, t in enumerate(lstTaches):
            if t.phase == 'Rev':
                if i > 0:
                    Rev.append((t, lstTaches[i-1]))
                else:
                    Rev.append((t, None))
             
        #
        # On fait des paquets par catégorie
        #
        Ana = []
        Con = []
        Rea = []
        DCo = []
        Val = []
        R1 = []
        R2 = []
        S = []
        X = []
        Rien = []
        for t in lstTaches:
            if t.phase == 'Ana':
                Ana.append(t)
            elif t.phase == 'Con':
                Con.append(t)
            elif t.phase == 'DCo':
                DCo.append(t)
            elif t.phase == 'Rea':
                Rea.append(t)
            elif t.phase == 'Val':
                Val.append(t)
            elif t.phase == 'R1':
                R1.append(t)
            elif t.phase == 'R2':
                R2.append(t)
            elif t.phase == 'S':
                S.append(t)
            elif t.phase == 'XXX':
                X.append(t)
            elif t.phase == '':
                Rien.append(t)
        
        # On trie les paquets       
        for c in [Ana, Con, Rea, DCo, Val, X]:
            c.sort(key=attrgetter('ordre'))
        
        #
        # On assemble les paquets
        #
        if self.R1avantConception:
            lst = Ana + Con + DCo + R1 + Rea  + Val + R2+ X + Rien + S
        else:
            lst = Ana + Con + R1 + DCo + Rea  + Val + R2+ X + Rien + S
           
        #
        # On ajoute les revues intermédiaires
        #
        for r, q in Rev:
            if q == None:
                lst.insert(0, r)
            else:
                i = lst.index(q)
                lst.insert(i+1, r)
                
        return lst
        
    ######################################################################################  
    def OrdonnerTaches(self):
        self.taches = self.OrdonnerListeTaches(self.taches)
        
        self.SetOrdresTaches()
        self.SetCodes()
        self.arbre.Ordonner(self.brancheTac)
        return

    
    ######################################################################################  
    def SupprimerItem(self, item):
        data = self.arbre.GetItemPyData(item)
        if isinstance(data, Tache) and data.phase not in ["R1", "R2", "S"]:
            self.SupprimerTache(item = item)
            
        elif isinstance(data, Eleve):
            self.SupprimerEleve(item = item)
        
        elif isinstance(data, Prof):
            self.SupprimerProf(item = item)
            
#        elif isinstance(data, LienSequence):
#            self.SupprimerSequencePre(item = item)           
        
    
#    ######################################################################################  
#    def SupprimerSequencePre(self, event = None, item = None):
#        ps = self.arbre.GetItemPyData(item)
#        self.prerequisSeance.remove(ps)
#        self.arbre.Delete(item)
#        self.panelPropriete.sendEvent()
#        
#    ######################################################################################  
#    def AjouterSequencePre(self, event = None):
#        ps = LienSequence(self, self.panelParent)
#        self.prerequisSeance.append(ps)
#        ps.ConstruireArbre(self.arbre, self.branchePre)
#        self.panelPropriete.sendEvent()
#        self.arbre.SelectItem(ps.branche)
        
    ######################################################################################  
    def AjouterEleveDansPanelTache(self):
        for t in self.taches:
            t.AjouterEleve()
            
    ######################################################################################  
    def SupprimerEleveDansPanelTache(self, i):
        for t in self.taches:
            t.SupprimerEleve(i)  
                  
    ######################################################################################  
    def AjouterEleve(self, event = None):
        if len(self.eleves) < 6:
            e = Eleve(self, self.panelParent, self.GetNewIdEleve())
            self.eleves.append(e)
            self.OrdonnerEleves()
            e.ConstruireArbre(self.arbre, self.brancheElv)
            self.arbre.Expand(self.brancheElv)
            self.panelPropriete.sendEvent()
            self.arbre.SelectItem(e.branche)
            self.AjouterEleveDansPanelTache()
        

    
    ######################################################################################  
    def SupprimerEleve(self, event = None, item = None):
#        print "SupprimerEleve",
        e = self.arbre.GetItemPyData(item)
#        print e,
        i = self.eleves.index(e)
#        print "(", i,")"
        self.eleves.remove(e)
        self.OrdonnerEleves()
        
        self.arbre.Delete(item)
        self.SupprimerEleveDansPanelTache(i)
        
        # On fait ça car supprimer un élève a un impact sur les noms des éleves "sans nom"
        for i, e in enumerate(self.eleves):
            e.SetCode()
            
        self.panelPropriete.sendEvent()
    
    ######################################################################################  
    def OrdonnerEleves(self):
        for i,e in enumerate(self.eleves):
            e.id = i
            
        
        
    ######################################################################################  
    def GetNewIdEleve(self):
        """ Renvoie le 1er numéro d'identification élève disponible
        """
        print "GetNewIdEleve", 
        for i in range(6):
            ok = False
            for e in self.eleves:
                ok = ok or i != e.id
            if ok:
                break
        print i
        return i
    

    
    ######################################################################################  
    def AjouterProf(self, event = None):
        e = Prof(self, self.panelParent, len(self.equipe))
        self.equipe.append(e)
        e.ConstruireArbre(self.arbre, self.branchePrf)
        self.arbre.Expand(self.branchePrf)
        self.panelPropriete.sendEvent()
        self.arbre.SelectItem(e.branche)
        return
    
    ######################################################################################  
    def SupprimerProf(self, event = None, item = None):
        e = self.arbre.GetItemPyData(item)
#        i = self.equipe.index(e)
        self.equipe.remove(e)
        self.arbre.Delete(item)
        self.panelPropriete.sendEvent()
        
    
    ######################################################################################  
    def MiseAJourPoidsCompetences(self, code = None):
        for t in self.taches:
            t.MiseAJourPoidsCompetences(code)
        self.MiseAJourDureeEleves()
    
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, Titres[9], data = self, image = self.arbre.images["Prj"])

        #
        # Le support
        #
        
        self.support.ConstruireArbre(arbre, self.branche)
        #
        # Les profs
        #
        self.branchePrf = arbre.AppendItem(self.branche, Titres[10], data = self.panelEquipe)
        for e in self.equipe:
            e.ConstruireArbre(arbre, self.branchePrf) 
        
        #
        # Les élèves
        #
        self.brancheElv = arbre.AppendItem(self.branche, Titres[6], data = self.panelEleves)
        for e in self.eleves:
            e.ConstruireArbre(arbre, self.brancheElv) 
            
        #
        # Les tâches
        #
        self.brancheTac = arbre.AppendItem(self.branche, Titres[8], data = self.panelTaches)
        for t in self.taches:
            t.ConstruireArbre(arbre, self.brancheTac)
        

    ######################################################################################  
    def reconstruireBrancheSeances(self, b1, b2):
        self.arbre.DeleteChildren(self.brancheSce)
        for sce in self.seance:
            sce.ConstruireArbre(self.arbre, self.brancheSce) 
        self.arbre.Expand(b1.branche)
        self.arbre.Expand(b2.branche)
        
    
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):    
        """ Affiche le menu contextuel associé é la séquence
            ... ou bien celui de itemArbre concerné ...
        """
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([[u"Enregistrer", self.app.commandeEnregistrer],
#                                             [u"Ouvrir", self.app.commandeOuvrir],
                                             [u"Exporter la fiche (PDF ou SVG)", self.app.exporterFiche],
                                            ])
            
#        [u"Séquence pédagogique",
#          u"Prérequis",
#          u"Objectifs pédagogiques",
#          u"Séances",
#          u"Systèmes"]
        
#        elif isinstance(self.arbre.GetItemPyData(itemArbre), Competences):
#            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Eleve):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Prof):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Tache):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), LienSequence):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)           
            
        elif self.arbre.GetItemText(itemArbre) == Titres[6]: # Eleve
            self.app.AfficherMenuContextuel([[u"Ajouter un élève", self.AjouterEleve]])
            
        elif self.arbre.GetItemText(itemArbre) == Titres[8]: # Tache
            self.app.AfficherMenuContextuel([[u"Ajouter une tâche", self.AjouterTache]])
         
        elif self.arbre.GetItemText(itemArbre) == Titres[10]: # Eleve
            self.app.AfficherMenuContextuel([[u"Ajouter un professeur", self.AjouterProf]])
                                             
         
            
    ######################################################################################       
    def GetCompetencesUtil(self):
        """ Renvoie les listes des codes 
            des compétences utiles
            (pour tracé fiche)
        """
        
        lst = []
        for t in self.taches:
            lst.extend(t.GetCompetencesUtil())
        lst = list(set(lst))
        lst.sort()
        return lst

    
    ######################################################################################  
    def GetNbrPhases(self):
        p = []
        for t in self.taches:
            if (not t.phase in p or t.phase == "Rev") and t.phase != "":
                p.append(t.phase)
        return len(p)
        
    ######################################################################################  
    def GetIntituleTaches(self):
        """ Renvoie les listes des codes et des intitulés 
            de toutes les tâches
            (pour tracé fiche)
        """
        codTaches = []
        intTaches = []
        for s in self.taches:
            if hasattr(s, 'code') and s.intitule != "" and not s.intituleDansDeroul:
                codTaches.append(s.code)
                intTaches.append(s.intitule)
        return codTaches, intTaches
        
        

        
    ######################################################################################  
    def HitTest(self, x, y):
        branche = None
        autresZones = self.taches + self.eleves+ self.equipe + [self.support]
        continuer = True
        i = 0
        while continuer:
            if i >= len(autresZones):
                continuer = False
            else:
                branche = autresZones[i].HitTest(x, y)
                if branche:
                    continuer = False
            i += 1
        
        if branche == None:
            if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
                return self.branche

        return branche
        
    ######################################################################################  
    def HitTestCompetence(self, x, y):
        if hasattr(self, 'rectComp'):
            for k, ro in self.rectComp.items():
                rect = [r[:-1] for r in ro]
                obj = [o[-1] for o in ro]
                ok, i = dansRectangle(x, y, rect)
                if ok:
                    return k, obj[i]
    
    ######################################################################################  
    def HitTestPosition(self, x, y):
        if hasattr(self, 'rectPos'):
            for i, rectPos in enumerate(self.rectPos):
                if dansRectangle(x, y, (rectPos,))[0]:
                    return i
                    
                 
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        self.app.SetTitre()
        for t in self.taches:
#            if t.phase in ["R1", "R2", "S"]:
            t.MiseAJourTypeEnseignement(self.classe.typeEnseignement)
        
        
    #############################################################################
    def VerrouillerClasse(self):
        self.classe.Verrouiller(len(self.GetCompetencesUtil()) == 0)
        
    #############################################################################
    def SetCompetencesRevuesSoutenance(self):
        """ Attribue à la soutenance et à la revue n°2
            les compétences et indicateurs 
            mobilisés par les tâches précédentes
        """
        tousIndicateurs = constantes.dicIndicateurs[self.classe.typeEnseignement]
        tR1 = None
        indicateurs = {}
        for t in self.taches:   # toutes les tâches, dans l'ordre
            if t.phase in ["R1", "R2", "S"]:
                if t.phase != "R1":
                    t.indicateurs = []
                else:
                    t.indicateursMaxi = []
                for c, l in indicateurs.items():
                    for i, ok in enumerate(l):
                        if ok:
                            codeIndic = c+"_"+str(i+1)
                            if tousIndicateurs[c][i][1]: # Indicateur "revue"
                                if t.phase in ["R1", "R2"]:
                                    if t.phase == "R2" and (tR1 != None and not codeIndic in tR1.indicateurs):
                                        t.indicateurs.append(codeIndic)
                                    if t.phase == "R1":
                                        t.indicateursMaxi.append(codeIndic)
                            else:
                                if t.phase == "S":
                                    t.indicateurs.append(codeIndic)
#                if t.phase == "R2":
#                    indicateurs = {}
                
                if t.phase == "R1":
                    ti = []
                    for i in t.indicateurs:
                        if i in t.indicateursMaxi:
                            ti.append(i)
                    t.indicateurs = ti
                    t.panelPropriete.arbre.MiseAJourTypeEnseignement(t.GetTypeEnseignement())
                    t.panelPropriete.MiseAJour()
                    tR1 = t
                            
                        
            else:   # On stock les indicateurs dans un dictionnaire CodeCompétence : ListeTrueFalse
                indicTache = t.GetDicIndicateurs()
                for c, i in indicTache.items():
                    if c in indicateurs.keys():
                        indicateurs[c] = [x or y for x,y in zip(i, indicateurs[c])]
                    else:
                        indicateurs[c] = i   
            
                
                
####################################################################################
#
#   Classe définissant les propriétés d'une séquence
#
####################################################################################
class CentreInteret(Objet_sequence):
    def __init__(self, parent, panelParent, numCI = []):
        Objet_sequence.__init__(self)
        self.parent = parent
        self.numCI = []
        self.SetNum(self.numCI)
        self.max2CI = True
        
        
        if panelParent:
            self.panelPropriete = PanelPropriete_CI(panelParent, self)
        
       
        
        
    ######################################################################################  
    def __repr__(self):
        print self.numCI
        return ""
    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du centre d'intérét pour enregistrement
        """
        root = ET.Element("CentresInteret")
        for i, num in enumerate(self.numCI):
            root.set("C"+str(i), str(num))
        return root
    
        if hasattr(self, 'code'):
            if self.code == "":
                self.code = "_"
            root = ET.Element(self.code)
            return root
        
    
    ######################################################################################  
    def setBranche(self, branche):
        self.numCI = []
        for i, s in enumerate(branche.keys()):
            self.numCI.append(eval(branche.get("C"+str(i), "")))
        
        # Pour rétro compatibilité
        if self.numCI == []:
            if len(list(branche)) > 0:
                code = list(branche)[0].tag
                if code == "_":
                    num = []
                    self.AddNum(num)
                else:
                    num = eval(code[2:])-1
                    self.AddNum(num)
        
        
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()
        return
            
#        code = list(branche)[0].tag
#        if code == "_":
#            num = []
#            self.SetNum(num)
#        else:
#            num = eval(code[2:])-1
#            self.SetNum(num)
#            if hasattr(self, 'panelPropriete'):
#                self.panelPropriete.MiseAJour()

    
    
    
    
    ######################################################################################  
    def AddNum(self, num): 
        self.numCI.append(num)
        self.SetNum()
    
        
    ######################################################################################  
    def DelNum(self, num): 
        self.numCI.remove(num)
        self.SetNum()
        
    ######################################################################################  
    def SetNum(self, numCI = None):
        if numCI != None:
            self.numCI = numCI
            
        if hasattr(self, 'arbre'):
            self.MaJArbre()
        
#        if len(self.numCI) > 0 :
        self.parent.VerrouillerClasse()
        
    ######################################################################################  
    def GetIntit(self, num):
        if self.GetTypeEnseignement() == 'ET':
            lstCI = self.parent.classe.ci_ET
        else:
            lstCI = constantes.CentresInterets[self.GetTypeEnseignement()]
        if self.numCI[num] < len(lstCI):
            return lstCI[self.numCI[num]]
            
    
    
    ######################################################################################  
    def GetCode(self, num = None):
        if num == None:
            s = ""
            for i, n in enumerate(self.numCI):
                s = s + self.GetCode(i)
                if i < len(self.numCI)-1:
                    s += " - "
            return s
        
        else :
            return "CI"+str(self.numCI[num]+1)
    
    ######################################################################################  
    def GetPosCible(self, num):
        if self.GetTypeEnseignement() == 'ET':
            return self.parent.classe.posCI_ET[self.numCI[num]]
        
#        if constantes_ETT.PositionCibleCI != None:
#            return constantes_ETT.PositionCibleCI[self.numCI[num]]
    
    ######################################################################################  
    def MaJArbre(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.GetCode())
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Centre d'intérét :", wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Ci"])
        

        
#    #############################################################################
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
#            return self.branche
#        rect = draw_cairo.posCI + draw_cairo.tailleCI
#        if dansRectangle(x, y, (rect,)):
##            self.arbre.DoSelectItem(self.branche)
#            return self.branche
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.construire()
            
            
####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Competences(Objet_sequence):
    def __init__(self, parent, panelParent, numComp = None):
        Objet_sequence.__init__(self)
#        self.clefs = Competences.keys()
#        self.clefs.sort()
        self.parent = parent
        self.num = numComp
        self.competences = []
#        self.SetNum(numComp)
        if panelParent:
            self.panelPropriete = PanelPropriete_Competences(panelParent, self)
        
    ######################################################################################  
    def __repr__(self):
        t = ''
        for n in self.competences:
            t += n
        
        return t
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
        root = ET.Element("Competences")
        for i, s in enumerate(self.competences):
            root.set("C"+str(i), s)
        return root
    
    
    ######################################################################################  
    def setBranche(self, branche):
        self.competences = []
        for i, s in enumerate(branche.keys()):
            self.competences.append(branche.get("C"+str(i), ""))
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()
    
    
    ######################################################################################  
    def GetCode(self, num):
        return self.competences[num]
    
    ######################################################################################  
    def GetIntit(self, num):
        return constantes.getCompetence(self.parent, self.competences[num])
    
    
         
#    ######################################################################################  
#    def SetNum(self, num):
#        self.num = num
#        if num != None:
#            self.code = self.clefs[self.num]
#            self.competence = Competences[self.code]
#            
#            if hasattr(self, 'arbre'):
#                self.SetCode()
#        
#    ######################################################################################  
#    def SetCode(self):
#        self.codeBranche.SetLabel(self.code)
    
#    #############################################################################
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
#            return self.branche

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
#        self.codeBranche.SetBackgroundColour(wx.Colour(COUL_COMPETENCES[0]*255, COUL_COMPETENCES[1]*255, COUL_COMPETENCES[2]*255))
        self.branche = arbre.AppendItem(branche, u"Compétences", wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Com"])
        self.arbre.SetItemTextColour(self.branche, constantes.GetCouleurWx(COUL_COMPETENCES))
        
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.construire()
        
#    ######################################################################################  
#    def AfficherMenuContextuel(self, itemArbre):
#        if itemArbre == self.branche:
#            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerObjectif, item = itemArbre)]])
            
            
####################################################################################
#
#   Classe définissant les propriétés de savoirs
#
####################################################################################
class Savoirs(Objet_sequence):
    def __init__(self, parent, panelParent, num = None, prerequis = False):
        Objet_sequence.__init__(self)
        self.parent = parent # la séquence
        self.num = num
        self.savoirs = []
        if panelParent:
            self.panelPropriete = PanelPropriete_Savoirs(panelParent, self, prerequis)
        
    ######################################################################################  
    def __repr__(self):
        t = ''
        for n in self.savoirs:
            t += n
        return t
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du savoir pour enregistrement
        """
        root = ET.Element("Savoirs")
        for i, s in enumerate(self.savoirs):
            root.set("S"+str(i), s)
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        self.savoirs = []
        for i, s in enumerate(branche.keys()):
            self.savoirs.append(branche.get("S"+str(i), ""))
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()
        
    ######################################################################################  
    def GetCode(self, num):
        return self.savoirs[num]
    
    ######################################################################################  
    def GetIntit(self, num):
        return constantes.getSavoir(self.parent.classe.typeEnseignement, self.GetCode(num))  
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        if self.parent.classe.typeEnseignement == "SSI":
            t = u"Capacités"
        else:
            t = u"Savoirs"
        self.branche = arbre.AppendItem(branche, t, wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Sav"])
         
    
#    #############################################################################
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
#            return self.branche
        
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.construire()
    
#    ######################################################################################  
#    def SetNum(self, num):
#        self.num = num
#        if num != None:
#            self.code = self.clefs[self.num]
#            self.savoir = Savoirs[self.code]
#            
#            if hasattr(self, 'arbre'):
#                self.SetCode()
        
#    ######################################################################################  
#    def SetCode(self):
#        self.codeBranche.SetLabel(self.code)
        

#    ######################################################################################  
#    def ConstruireArbre(self, arbre, branche):
#        self.arbre = arbre
#        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
#        self.branche = arbre.AppendItem(branche, u"Savoirs :", wnd = self.codeBranche, data = self,
#                                        image = self.arbre.images["Com"])
#        
#        
#    ######################################################################################  
#    def AfficherMenuContextuel(self, itemArbre):
#        if itemArbre == self.branche:
#            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerObjectif, item = itemArbre)]])
            
                  
            

####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Seance(ElementDeSequence, Objet_sequence):
    
                  
    def __init__(self, parent, panelParent, typeSeance = "", typeParent = 0):
        """ Séance :
                parent = le parent wx pour contenir "panelPropriete"
                typeSceance = type de séance parmi "TypeSeance"
                typeParent = type du parent de la séance :  0 = séquence
                                                            1 = séance "Rotation"
                                                            2 = séance "parallèle"
        """
    
        ElementDeSequence.__init__(self)
        Objet_sequence.__init__(self)
        
        # Les données sauvegardées
        self.ordre = 0
        self.duree = Variable(u"Durée", lstVal = 1.0, nomNorm = "", typ = VAR_REEL_POS, 
                              bornes = [0.25,30], modeLog = False,
                              expression = None, multiple = False)
        self.intitule  = u""
        self.intituleDansDeroul = True
        self.effectif = "C"
        self.demarche = "I"
        self.systemes = []
        self.code = u""
        self.description = None
        self.taille = Variable(u"Taille des caractères", lstVal = 100, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [10,100], modeLog = False,
                              expression = None, multiple = False)
        self.nombre = Variable(u"Nombre", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [1,10], modeLog = False,
                              expression = None, multiple = False)
        
        self.nbrRotations = Variable(u"Nombre de rotations", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [1,None], modeLog = False,
                              expression = None, multiple = False)
        
        # Les autres données
        self.typeParent = typeParent
        self.parent = parent
        self.panelParent = panelParent
        
        self.SetType(typeSeance)
        self.sousSeances = []
        
        #
        # Création du Tip (PopupInfo)
        #
        if self.GetApp():
            self.tip = PopupInfo(self.GetApp(), u"Séance")
            self.tip_type = self.tip.CreerTexte((1,0), flag = wx.ALL)
            self.tip_intitule = self.tip.CreerTexte((2,0))
            self.tip_titrelien, self.tip_ctrllien = self.tip.CreerLien((3,0))
            self.tip_description = self.tip.CreerRichTexte(self, (4,0))
        
        self.AjouterListeSystemes(self.GetDocument().systemes)
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Seance(panelParent, self)
            self.panelPropriete.AdapterAuType()
        
        
        
        
    
    ######################################################################################  
    def __repr__(self):
        t = self.code 
#        t += " " +str(self.GetDuree()) + "h"
#        t += " " +str(self.effectif)
#        for s in self.sousSeances:
#            t += "  " + s.__repr__()
        return t
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    
    
    ######################################################################################  
    def EstSousSeance(self):
        return not isinstance(self.parent, Sequence)
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la séance pour enregistrement
        """
        root = ET.Element("Seance"+str(self.ordre))
        root.set("Type", self.typeSeance)
        root.set("Intitule", self.intitule)
        root.set("Taille", str(self.taille.v[0]))
        
        if self.description != None:
            root.set("Description", self.description)
        
        self.lien.getBranche(root)
        
        if self.typeSeance in ["R", "S"]:
            for sce in self.sousSeances:
                root.append(sce.getBranche())
            root.set("nbrRotations", str(self.nbrRotations.v[0]))
            
        elif self.typeSeance in ["AP", "ED", "P"]:
            root.set("Demarche", self.demarche)
            root.set("Duree", str(self.duree.v[0]))
            root.set("Effectif", self.effectif)
            root.set("Nombre", str(self.nombre.v[0]))
            
            self.branchesSys = []
            for i, s in enumerate(self.systemes):
                bs = ET.SubElement(root, "Systemes"+str(i))
                self.branchesSys.append(bs)
                bs.set("Nom", s.n)
                bs.set("Nombre", str(s.v[0]))
        else:
            root.set("Duree", str(self.duree.v[0]))
            root.set("Effectif", self.effectif)
        
        root.set("IntituleDansDeroul", str(self.intituleDansDeroul))
        
        return root    
        
    ######################################################################################  
    def setBranche(self, branche):
        self.ordre = eval(branche.tag[6:])
        
        self.intitule  = branche.get("Intitule", "")
        self.taille.v[0] = eval(branche.get("Taille", "100"))
        self.typeSeance = branche.get("Type", "C")
        self.description = branche.get("Description", None)
        
        self.lien.setBranche(branche, self.GetPath())
        
        if self.typeSeance in ["R", "S"]:
            self.sousSeances = []
            for sce in list(branche):
                seance = Seance(self, self.panelParent)
                self.sousSeances.append(seance)
                seance.setBranche(sce)
            self.duree.v[0] = self.GetDuree()
            if self.typeSeance == "R":
                self.nbrRotations.v[0] = eval(branche.get("nbrRotations", str(len(self.sousSeances))))
                self.reglerNbrRotMaxi()
            
        elif self.typeSeance in ["AP", "ED", "P"]:   
            self.effectif = branche.get("Effectif", "C")
            self.demarche = branche.get("Demarche", "I")
            self.nombre.v[0] = eval(branche.get("Nombre", "1"))
#            self.lien.setBranche(branche)
            
            # Les systèmes nécessaires
            lstSys = []
            lstNSys = []
            for i, s in enumerate(list(branche)):
                nom = s.get("Nom", "")
                if nom != "":
                    lstSys.append(nom)
                    lstNSys.append(eval(s.get("Nombre", "")))
            self.AjouterListeSystemes(lstSys, lstNSys)
            
            # Durée
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        else:
            self.effectif = branche.get("Effectif", "C")
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        
        self.intituleDansDeroul = eval(branche.get("IntituleDansDeroul", "True"))
        
#        self.MiseAJourListeSystemes()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeSystemes()
            self.panelPropriete.MiseAJour()
        

    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        if hasattr(self, 'pts_caract' ):
            for i, pt in enumerate(self.pts_caract):
                lst.append((pt, self, i))
                
        if self.typeSeance in ["R", "S"]:
            for sce in self.sousSeances:
                lst.extend(sce.GetPtCaract())
                
        self.cadre = []
        
        return lst
    
    def GetCode(self, num):
        return self.code
    
    def GetIntit(self, num):
        return self.intitule
    
    
    
    ######################################################################################  
    def EnrichiSVGse(self, doc):
        if self.typeSeance in ["R", "S"]:
            for se in self.sousSeances:
                se.EnrichiSVG(doc, seance = True)
        else:
            self.EnrichiSVG(doc, seance = True)
        
        
        
    ######################################################################################  
    def GetEffectif(self):
        """ Renvoie l'effectif de la séance
            n : portion de classe
        """
        eff = 0
        if self.typeSeance in ["R", "S"]:
            for sce in self.sousSeances:
                eff += sce.GetEffectif() #self.sousSeances[0].GetEffectif()
#        elif self.typeSeance == "S":
#            for sce in self.sousSeances:
#                eff += sce.GetEffectif()
        else:
            eff = self.GetClasse().GetEffectifNorm(self.effectif)
            eff = eff * self.nombre.v[0]

        return eff
    
    
    
    def GetNbrSystemesUtil(self):
        return 
    
    
    ######################################################################################  
    def SetEffectif(self, val):
        """ Modifie l'effectif des Rotation et séances en Parallèle et de tous leurs enfants
            après une modification de l'effectif d'un des enfants
            1 = P
            2 = E
            4 = D
            8 = G
            16 = C
        """
        if type(val) == int:
            if self.typeSeanc == "R":
                for s in self.sousSeances:
                    s.SetEffectif(val)
#            elif self.typeSeance == "S":
#                self.effectif = self.GetEffectif()
#                self.panelPropriete.MiseAJourEffectif()
            else:
                if val == 16:
                    codeEff = "C"
                elif val == 8:
                    codeEff = "G"
                elif val == 4:
                    codeEff = "D"
                elif val == 2:
                    codeEff = "E"
                elif val == 1:
                    codeEff = "P"
                else:
                    codeEff = ""
        else:
            for k, v in constantes.NomsEffectifs.items():
                if v[0][:2] == val[:2]: # On ne compare que les 2 premières lettres
                    codeEff = k
        self.effectif = codeEff
        

    ######################################################################################  
    def VerifPb(self):
        self.SignalerPb(self.IsEffectifOk(), self.IsNSystemesOk())
        if self.typeSeance in ["R", "S"] and len(self.sousSeances) > 0:
            for s in self.sousSeances:
                s.VerifPb()
        
    ######################################################################################  
    def IsEffectifOk(self):
        """ Teste s'il y a un problème d'effectif pour les séances en rotation ou en parallèle
            0 : pas de problème
            1 : tout le groupe "effectif réduit" n'est pas occupé
            2 : effectif de la séance supperieur à celui du groupe "effectif réduit"
            3 : séances en rotation d'effectifs différents !!
        """
        ok = 0 # pas de problème
        if self.typeSeance in ["R", "S"] and len(self.sousSeances) > 0:
            if self.GetEffectif() < self.GetClasse().GetEffectifNorm('G'):
                ok = 1 # Tout le groupe "effectif réduit" n'est pas occupé
            elif self.GetEffectif() > self.GetClasse().GetEffectifNorm('G'):
                ok = 2 # Effectif de la séance supperieur à celui du groupe "effectif réduit"    
#            if self.typeSeance == "R":
#                continuer = True
#                eff = self.sousSeances[0].GetEffectif()
#                i = 1
#                while continuer:
#                    if i >= len(self.sousSeances):
#                        continuer = False
#                    else:
#                        if self.sousSeances[i].GetEffectif() != eff:
#                            ok = 3 # séance en rotation d'effectifs différents !!
#                            continuer = False
#                        i += 1
            
        elif self.typeSeance in ["AP", "ED"] and not self.EstSousSeance():
            if self.GetEffectif() < self.GetClasse().GetEffectifNorm('G'):
                ok = 1 # Tout le groupe "effectif réduit" n'est pas occupé

        return ok
            
    ######################################################################################  
    def IsNSystemesOk(self):
        """ Teste s'il y a un problème de nombre de systèmes disponibles
        """
        ok = 0 # pas de problème
        if self.typeSeance in ["AP", "ED"]:
            n = self.GetNbrSystemes()
            seq = self.GetApp().sequence
            for i, s in enumerate(seq.systemes):
                if n.has_key(s.nom) and n[s.nom] > s.nbrDispo.v[0]:
                    ok = 1
        return ok
    
    ######################################################################################  
    def SignalerPb(self, etatEff, etatSys):
        if hasattr(self, 'codeBranche'):
            etat = max(etatEff, etatSys)
            if etat == 0:
                couleur = 'white'
            elif etat == 1 :
                couleur = COUL_BIEN
            elif etat == 2:
                couleur = COUL_BOF
            elif etat == 3:
                couleur = "TOMATO1"
            
            if etatEff == 0:
                message = u""
            elif etatEff == 1 :
                message = u"Tout le groupe \"effectif réduit\" n'est pas occupé"
            elif etatEff == 2:
                message = u"Effectif de la séance supperieur à celui du groupe \"effectif réduit\""
            elif etatEff == 3:
                message = u"Séances en rotation d'effectifs différents !!"
                
            if etatSys == 0:
                message += u""
            elif etatSys == 1 :
                message += u"Nombre de systèmes nécessaires supérieur au nombre de systèmes disponibles."
                
            self.codeBranche.SetBackgroundColour(couleur)
            self.codeBranche.SetToolTipString(message)
            self.codeBranche.Refresh()
    
    
    ######################################################################################  
    def GetDuree(self):
        duree = 0
        if self.typeSeance == "R":
            for i in range(self.nbrRotations.v[0]):
                sce = self.sousSeances[i]
                duree += sce.GetDuree()
#            for sce in self.sousSeances:
#                duree += sce.GetDuree()
        elif self.typeSeance == "S":
            if len(self.sousSeances) > 0:
                duree += self.sousSeances[0].GetDuree()
        else:
            duree = self.duree.v[0]
        return duree
                
    ######################################################################################  
    def GetDureeGraph(self):
        return self.GetDuree()
        d = self.GetDuree(graph = True)
        if d != 0:
            return 0.001*log(d*2)+0.001
        return d
           
                
    ######################################################################################  
    def SetDuree(self, duree, recurs = True):
        """ Modifie la durée des Rotation et séances en Parallèle et de tous leurs enfants
            après une modification de durée d'un des enfants
        """
        if recurs and self.EstSousSeance() and self.parent.typeSeance in ["R", "S"]: # séance en rotation (parent = séance "Rotation")
            self.parent.SetDuree(duree)
        
        elif self.typeSeance == "S" : # Serie
            self.duree.v[0] = duree
            for s in self.sousSeances:
                if s.typeSeance in ["R", "S"]:
                    s.SetDuree(duree, recurs = False)
                else:
                    s.duree.v[0] = duree
                    s.panelPropriete.MiseAJourDuree()
            self.panelPropriete.MiseAJourDuree()

        
        elif self.typeSeance == "R" : # Serie
            for s in self.sousSeances:
                if s.typeSeance in ["R", "S"]:
                    s.SetDuree(duree, recurs = False)
                else:
                    s.duree.v[0] = duree
                    s.panelPropriete.MiseAJourDuree()
            self.duree.v[0] = self.GetDuree()
            self.panelPropriete.MiseAJourDuree()

        
    ######################################################################################  
    def SetNombre(self, nombre):
        self.nombre.v[0] = nombre
    
    ######################################################################################  
    def SetTaille(self, nombre):
        self.taille.v[0] = nombre
        
    ######################################################################################  
    def SetNombreRot(self, nombre):
        self.nbrRotations.v[0] = nombre
        
    ######################################################################################  
    def SetIntitule(self, text):           
        self.intitule = text
        if self.intitule != "":
            texte = u"Intitulé : "+ "\n".join(textwrap.wrap(self.intitule, 40))
        else:
            texte = u""
        self.tip.SetTexte(texte, self.tip_intitule)
           
    
    ######################################################################################  
    def SetDemarche(self, text):   
        for k, v in constantes.Demarches.items():
            if v[0] == text[0]:
                codeDem = k
        self.demarche = codeDem
        
        
    ######################################################################################  
    def SetType(self, typ):
        if type(typ) == str:
            self.typeSeance = typ
        else:
            self.typeSeance = constantes.listeTypeSeance[typ]
            
        if hasattr(self, 'arbre'):
            self.SetCode()
            
        if self.typeSeance in ["R","S"] and len(self.sousSeances) == 0: # Rotation ou Serie
            self.AjouterSeance()
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.AdapterAuType()
        
        if self.EstSousSeance() and self.parent.typeSeance in ["R","S"]:
            self.parent.SignalerPb(self.parent.IsEffectifOk(), 0)
        
        if self.typeSeance in ["AP","ED"]:
            self.SignalerPb(0, self.IsNSystemesOk())
            
        if hasattr(self, 'arbre'):
            self.arbre.SetItemImage(self.branche, self.arbre.images[self.typeSeance])
            self.arbre.Refresh()
        
    ######################################################################################  
    def GetToutesSeances(self):
        l = []
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            l.extend(self.sousSeances)
            for s in self.sousSeances:
                l.extend(s.GetToutesSeances())
        return l
        
    ######################################################################################  
    def PubDescription(self):
        """ Publie toutes les descriptions de séance
            (à l'ouverture)
        """
        self.tip.SetRichTexte()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.rtc.Ouvrir()
        
        if self.typeSeance in ["R", "S"]:
            for sce in self.sousSeances:
                sce.PubDescription() 
                
    ######################################################################################  
    def SetDescription(self, description):   
        if self.description != description:
            self.description = description
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.sendEvent()
            self.tip.SetRichTexte()

    ######################################################################################  
    def SetCodeBranche(self):
        if hasattr(self, 'codeBranche') and self.typeSeance != "":
            self.codeBranche.SetLabel(self.code)
            self.arbre.SetItemText(self.branche, constantes.TypesSeanceCourt[self.typeSeance])
            
                  
    ######################################################################################  
    def SetCode(self):
        self.code = self.typeSeance
        num = str(self.ordre+1)
        
        if isinstance(self.parent, Seance):
            num = str(self.parent.ordre+1)+"."+num
            if isinstance(self.parent.parent, Seance):
                num = str(self.parent.parent.ordre+1)+"."+num

        self.code += num

    
        self.SetCodeBranche()
        
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for sce in self.sousSeances:
                sce.SetCode()

        # Tip
        self.tip.SetTitre(u"Séance "+ self.code)
        if self.typeSeance != "":
            t = u"Type : "+ constantes.TypesSeance[self.typeSeance]
        else:
            t = u""
        self.tip.SetTexte(t, self.tip_type)    
            
        if self.intitule != "":
            t = u"Intitulé : "+ textwrap.fill(self.intitule, 40)
        else:
            t = u""
        self.tip.SetTexte(t, self.tip_intitule)  
        
        
        
    
            
            
            
            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, self.code)
        if self.typeSeance != "":
            image = self.arbre.images[self.typeSeance]
        else:
            image = -1
        
        self.branche = arbre.AppendItem(branche, u"Séance :", wnd = self.codeBranche, 
                                            data = self, image = image)
        if hasattr(self, 'branche'):
            self.SetCodeBranche()
            
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for sce in self.sousSeances:
                sce.ConstruireArbre(arbre, self.branche)
            
        
    ######################################################################################  
    def OrdonnerSeances(self):
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for i, sce in enumerate(self.sousSeances):
                sce.ordre = i
                sce.OrdonnerSeances()
        
        self.SetCode()
        
            
    ######################################################################################  
    def AjouterSeance(self, event = None):
        """ Ajoute une séance é la séance
            !! Uniquement pour les séances de type "Rotation" ou "Serie" !!
        """
        seance = Seance(self, self.panelParent)
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            self.sousSeances.append(seance)
            
        self.OrdonnerSeances()
        seance.ConstruireArbre(self.arbre, self.branche)
        self.arbre.Expand(self.branche)
        
        if self.typeSeance == "R":
            seance.SetDuree(self.sousSeances[0].GetDuree())
            self.reglerNbrRotMaxi()
        else:
            seance.SetDuree(self.GetDuree())
        
        self.arbre.SelectItem(seance.branche)


    ######################################################################################  
    def SupprimerSeance(self, event = None, item = None):
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            if len(self.sousSeances) > 1: # On en laisse toujours une !!
                seance = self.arbre.GetItemPyData(item)
                self.sousSeances.remove(seance)
                self.arbre.Delete(item)
                self.OrdonnerSeances()
                self.panelPropriete.sendEvent()
            if self.typeSeance == "R":  # Séances en Rotation
                self.reglerNbrRotMaxi()
        return
    
    
    ######################################################################################  
    def reglerNbrRotMaxi(self):
        self.nbrRotations.bornes[1] = len(self.sousSeances)
        if self.nbrRotations.v[0] > len(self.sousSeances):
            self.SetNombreRot(len(self.sousSeances))
    
    
    ######################################################################################  
    def SupprimerSousSeances(self):
        self.arbre.DeleteChildren(self.branche)
        return
    
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if self.typeSeance in ["R", "S"]:
            for s in self.sousSeances:
                s.MiseAJourTypeEnseignement()
        else:
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.MiseAJourTypeEnseignement()
        
    ######################################################################################  
    def MiseAJourNomsSystemes(self):
        if self.typeSeance in ["AP", "ED", "P"]:
            sequence = self.GetDocument()
            for i, s in enumerate(sequence.systemes):
                self.systemes[i].n = s.nom
#            self.nSystemes = len(sequence.systemes)
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.MiseAJourListeSystemes()
                                 
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.sousSeances:
                s.MiseAJourNomsSystemes()
        
    ######################################################################################  
    def SupprimerSysteme(self, id):
        if self.typeSeance in ["AP", "ED", "P"]:
            del self.systemes[id]
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.sousSeances:
                s.SupprimerSysteme(id)

        
        
    ######################################################################################  
    def AjouterSysteme(self, nom = "", nombre = 0, construire = True):
        if self.typeSeance in ["AP", "ED", "P"]:
            self.systemes.append(Variable(nom, lstVal = nombre, nomNorm = "", typ = VAR_ENTIER_POS, 
                                          bornes = [0,8], modeLog = False,
                                          expression = None, multiple = False))
            if construire and hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.sousSeances:
                s.AjouterSysteme(nom, nombre)
    
    
    ######################################################################################  
    def AjouterListeSystemes(self, lstSys, lstNSys = None):
        if self.typeSeance in ["AP", "ED", "P"]:
            if lstNSys == None:
                lstNSys = [0]*len(lstSys)
            for i, s in enumerate(lstSys):
                self.AjouterSysteme(s, lstNSys[i], construire = False)
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
            
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.sousSeances:
                s.AjouterListeSystemes(lstSys, lstNSys) 
                
                
    ######################################################################################  
    def GetDocument(self):    
        if self.EstSousSeance():
            if self.parent.EstSousSeance():
                sequence = self.parent.parent.parent
            else:
                sequence = self.parent.parent
        else:
            sequence = self.parent
        return sequence
    
    
    ######################################################################################  
    def GetClasse(self):
        return self.GetDocument().classe
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            listItems = [[u"Supprimer", functools.partial(self.parent.SupprimerSeance, item = itemArbre)],
                         [u"Créer un lien", self.CreerLien]]
            if self.typeSeance in ["R", "S"]:
                listItems.append([u"Ajouter une séance", self.AjouterSeance])
            self.GetApp().AfficherMenuContextuel(listItems)
#            item2 = menu.Append(wx.ID_ANY, u"Créer une rotation")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterRotation, item = item), item2)
#            
#            item3 = menu.Append(wx.ID_ANY, u"Créer une série")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterSerie, item = item), item3)
            

            
    ######################################################################################  
    def GetNbrSystemes(self, complet = False, simple = False):
        """ Renvoie un dictionnaire :
                clef : nom du système
                valeur : nombre d'exemplaires de ce système utilisés dans la séance
        """
        def up(d, k, v):
            if d.has_key(k):
                d[k] += v
            else:
                d[k] = v
                
        d = {}
        if self.typeSeance in ["S", "R"]:
            if self.typeSeance == "S" or complet:
                
                for seance in self.sousSeances:
                    dd = seance.GetNbrSystemes(complet)
                    for k, v in dd.items():
                        up(d, k, v)

            else:
                for s in self.systemes:
                    if s.n <>"":
                        up(d, s.n, s.v[0]*self.nombre.v[0])
#                        d[s.n] = s.v[0]*self.nombre.v[0]
        else:
            for s in self.systemes:
                if s.n <>"":
                    if simple:
                        up(d, s.n, s.v[0])
                    else:
                        up(d, s.n, s.v[0]*self.nombre.v[0])
#            if posDansRot > 0:
#                rotation = self.parent
#                l = rotation.sousSeances
#                for t in range(posDansRot):
#                    l = draw_cairo.permut(l)
#                for i, s in enumerate(l[:rotation.nbrRotations.v[0]]):
#                    dd = s.GetNbrSystemes(complet)
#                    for k, v in dd.items():
#                        up(d, k, v)
    #                    d[s.n] = s.v[0]*self.nombre.v[0]
        
        return d
        
        
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
#            self.arbre.DoSelectItem(self.branche)
            return self.branche
        
        else:
            if self.typeSeance in ["R", "S"]:
                ls = self.sousSeances
            else:
                return
            continuer = True
            i = 0
            branche = None
            while continuer:
                if i >= len(ls):
                    continuer = False
                else:
                    branche = ls[i].HitTest(x, y)
                    if branche:
                        continuer = False
                i += 1
            return branche
        
        
        






####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Tache(Objet_sequence):
    
                  
    def __init__(self, parent, panelParent, intitule = u"", phaseTache = "", duree = 1.0, branche = None):
        """ Séance :
                parent = le parent wx pour contenir "panelPropriete"
                phaseTache = phase de la tache parmi 'Ana', 'Con', 'Rea', 'Val'
        """
       
        Objet_sequence.__init__(self)
        
        # Les données sauvegardées
        self.ordre = 100
        self.duree = Variable(u"Volume horaire (h)", lstVal = duree, nomNorm = "", typ = VAR_REEL_POS, 
                              bornes = [0.5,40], modeLog = False,
                              expression = None, multiple = False)
        self.intitule  = intitule
        self.intituleDansDeroul = True
        
        
        # Les élèves concernés (liste de
        self.eleves = []
        
        # Les indicateurs de compétences abordés
        self.indicateurs = []
        self.indicateursMaxi = [] # Code à revoir : ça ne sert que pour R1 !

        self.code = u""
        self.description = None

        # Les autres données
        self.parent = parent
        self.panelParent = panelParent
        
        self.phase = phaseTache
        
#        self.initIndicateurs()
        
        
        #
        # Création du Tip (PopupInfo)
        #
        if self.GetApp():
            self.tip = PopupInfo(self.GetApp(), u"Tâche")
            self.tip.sizer.SetItemSpan(self.tip.titre, (1,2))
            
            if not self.phase in ["R1", "R2", "S", "Rev"]:
                p = self.tip.CreerTexte((1,0), txt = u"Phase :", flag = wx.ALIGN_RIGHT|wx.ALL)
                p.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline = True))
                
                i = self.tip.CreerTexte((2,0), txt = u"Intitulé :", flag = wx.ALIGN_RIGHT|wx.ALL)
                i.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline = True))
            
            self.tip_phase = self.tip.CreerTexte((1,1), flag = wx.ALIGN_LEFT|wx.BOTTOM|wx.TOP|wx.LEFT)
            self.tip_phase.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
            
            self.tip_intitule = self.tip.CreerTexte((2,1), flag = wx.ALIGN_LEFT|wx.BOTTOM|wx.TOP|wx.LEFT)
            self.tip_intitule.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
            
            self.tip_description = self.tip.CreerRichTexte(self, (3,0), (1,2))
        
        if branche != None:
            self.setBranche(branche)
            
        if panelParent:
            self.panelPropriete = PanelPropriete_Tache(panelParent, self)
            
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeEleves()
            self.panelPropriete.MiseAJourDuree()
            self.panelPropriete.MiseAJour()
            
        
            
        
    
    ######################################################################################  
    def __repr__(self):
#        t = self.phase + str(self.ordre+1) 
#        t += " " +str(self.GetDuree()) + "h"
#        t += " " +str(self.effectif)
#        for s in self.sousSeances:
#            t += "  " + s.__repr__()
        return self.code
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()


    ######################################################################################  
    def GetDicIndicateurs(self):
        indicateurs = {}
        for i in self.indicateurs:
            competence, indicateur = i.split('_')
            indicateur = eval(indicateur)-1
            if not competence in indicateurs.keys():
                indicateurs[competence] = [False]*len(constantes.dicIndicateurs[self.GetTypeEnseignement()][competence])
            indicateurs[competence][indicateur] = True
        return indicateurs
    
    
    ######################################################################################  
    def GetCompetencesUtil(self):
        lst = []
        for i in self.indicateurs:
            lst.append(i.split('_')[0])
        return lst
        
    ######################################################################################  
    def initIndicateurs(self):
        # Les indicateurs séléctionnés ou bien les poids des indicateurs 
        #     clef = code compétence
        #     Pour la SSI :  valeur = poids
        #     Pour la STI2D : valeur = liste d'index
        typeEns = self.GetTypeEnseignement()
        if False:#typeEns == "SSI":
            indicateurs = constantes.dicCompetences_prj_simple[typeEns]
            self.indicateurs = dict(zip(indicateurs.keys(), [x[1] for x in indicateurs.values()]))
        else:
            indicateurs = constantes.dicIndicateurs[typeEns]
            self.indicateurs = {}
            for k, dic in indicateurs.items():
                ndict = dict(zip(dic[1].keys(), [[]]*len(dic[1])))
                for c in ndict.keys():
                    ndict[c] = [True]*len(indicateurs[k][1][c])
                self.indicateurs.update(ndict)
            
            


#            self.indicateurs = dict(zip(indicateurs.keys(), [[]]*len(indicateurs)))
#            for c in self.indicateurs.keys():
#                self.indicateurs[c] = [True]*len(constantes.dicIndicateurs[self.GetTypeEnseignement()][c])
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la tâche pour enregistrement
        """
        root = ET.Element("Tache"+str(self.ordre))
        root.set("Phase", self.phase)
        root.set("Intitule", self.intitule)

        if self.description != None:
            root.set("Description", self.description)

        root.set("Duree", str(self.duree.v[0]))
        
        brancheElv = ET.Element("Eleves")
        root.append(brancheElv)
        for i, e in enumerate(self.eleves):
            brancheElv.set("Eleve"+str(i), str(e))
        
        
        if not self.phase in ["R2", "S"]:
            # Structure des indicateurs :
            # <Indicateurs Indic0="CO6.1_1" Indic1="CO6.2_4" ..... />
            #   (compétence_indicateur)
            brancheCmp = ET.Element("Indicateurs")
            root.append(brancheCmp)
            
            for i, c in enumerate(self.indicateurs):
                brancheCmp.set("Indic"+str(i), c)
        
#            # Structure des indicateurs :
#            # <Indicateurs Indic0="True False True " Indic1="True False False True " ..... />
#            if self.GetTypeEnseignement() == "SSI":
#                brancheInd = ET.Element("PoidsIndicateurs")
#            else:
#                brancheInd = ET.Element("Indicateurs")
#            root.append(brancheInd)
#            for i, c in enumerate(self.competences):
#                if self.GetTypeEnseignement() == "SSI":
#                    if c in self.indicateurs.keys():
#                        brancheInd.set("Poids"+str(i), str(self.indicateurs[c]))
#                else:
#                    if c in self.indicateurs.keys():
#                        brancheInd.set("Indic"+str(i), toTxt(self.indicateurs[c]))
            
            
        root.set("IntituleDansDeroul", str(self.intituleDansDeroul))
        
        return root    
        
    ######################################################################################  
    def setBranche(self, branche):
        Ok = True
        self.ordre = eval(branche.tag[5:])
#        print "setBranche tache", self.ordre
        self.intitule  = branche.get("Intitule", "")
        
        self.phase = branche.get("Phase", "")
        if self.GetTypeEnseignement() == "SSI":
            if self.phase == 'Con':
                self.phase = 'Ana'
            elif self.phase in ['DCo', 'Val']:
                self.phase = 'Rea'
        self.description = branche.get("Description", None)
        
        if not self.phase in ["R1", "R2", "S", "Rev"]:
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        else:
            self.duree.v[0] = 0.5
        
        brancheElv = branche.find("Eleves")
        self.eleves = []
        for i, e in enumerate(brancheElv.keys()):
            self.eleves.append(eval(brancheElv.get("Eleve"+str(i))))
            
        if not self.phase in ["R2", "S"]:
            self.indicateurs = []
            #
            # pour compatibilité acsendante
            #
            brancheCmp = branche.find("Competences")
            if brancheCmp != None: ## ANCIENNE VERSION (<beta6)
                Ok = False
#                print "ancien"
                if self.GetTypeEnseignement() == "SSI":
                    brancheInd = None
                else:
                    brancheInd = branche.find("Indicateurs")
                for i, e in enumerate(brancheCmp.keys()):
                    print i,e
                    if brancheInd != None: #STI2D
                        i = eval(e[4:])
                        indic = brancheInd.get("Indic"+str(i))
                        if indic != None:
                            lst = toList(indic)
                        else:
                            lst = [True]*len(constantes.dicIndicateurs[self.GetTypeEnseignement()][e])
                        for n,j in enumerate(lst):
                            if j:
                                self.indicateurs.append(brancheCmp.get(e)+"_"+str(n+1))
                    else:
                        indic = brancheCmp.get("Comp"+str(i))
                        self.indicateurs.append(indic.replace(".", "_"))
                
            else:
                brancheInd = branche.find("Indicateurs")
                if brancheInd != None:
                    for i, e in enumerate(brancheInd.keys()):
                        codeindic = brancheInd.get(e)
                        code, indic = codeindic.split('_')
                        
                        # pour compatibilité version < 3.19
                        if code == "CO8.es":
                            code = "CO8.0"
                            codeindic = code+"_"+indic
                            
                        indic = eval(indic)-1
                        if self.phase != 'XXX' or not constantes.dicIndicateurs[self.GetTypeEnseignement()][code][indic][1]:
                            self.indicateurs.append(codeindic)
                        else:
                            print "Enlève :", self, constantes.dicIndicateurs[self.GetTypeEnseignement()][code][indic]
            
        self.intituleDansDeroul = eval(branche.get("IntituleDansDeroul", "True"))
        
        return Ok
    
#        if hasattr(self, 'panelPropriete'):
#            self.panelPropriete.ConstruireListeEleves()
#            self.panelPropriete.MiseAJourDuree()
#            self.panelPropriete.MiseAJour()
#            self.panelPropriete.MiseAJourPoidsCompetences()


    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        if hasattr(self, 'pts_caract' ):
            for i, pt in enumerate(self.pts_caract):
                lst.append((pt, self, i))
                
        self.cadre = []
        
        return lst
    
    def GetCode(self, num):
        return self.code
    
    def GetIntit(self, num):
        return self.intitule
        

    ######################################################################################  
    def VerifPb(self):
        print "Sert à rien"
        return

    ######################################################################################  
    def GetDuree(self):
        if self.phase != "":
            return self.duree.v[0]
        return 0
                
    ######################################################################################  
    def GetDureeGraph(self):
        return min(self.GetDuree(), 8)       
    
    ######################################################################################  
    def SetDuree(self, duree):
        """ Modifie la durée de la tâche
        """
        self.duree.v[0] = duree
        self.panelPropriete.MiseAJourDuree()
        self.parent.MiseAJourDureeEleves()
        
    ######################################################################################  
    def SetIntitule(self, text):           
        self.intitule = text
        if self.intitule != "":
            t = u"Intitulé : "+ "\n".join(textwrap.wrap(self.intitule, 40))
        else:
            t = u""
        self.tip.SetTexte(t, self.tip_intitule)
        
        
            
            
    ######################################################################################  
    def SetPhase(self, phase):
        self.phase = phase
        self.parent.OrdonnerTaches()
        
        if hasattr(self, 'arbre'):
            self.SetCode()
            
        if hasattr(self, 'arbre'):
            self.arbre.SetItemImage(self.branche, self.arbre.images[self.phase])
            self.arbre.Refresh()
        
        
    ######################################################################################  
    def PubDescription(self):
        """ Publie toutes les descriptions de tâche
            (à l'ouverture)
        """
        self.tip.SetRichTexte()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.rtc.Ouvrir()

                
    ######################################################################################  
    def SetDescription(self, description):   
        if self.description != description:
            self.description = description
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.sendEvent()
            self.tip.SetRichTexte()
            
    ######################################################################################  
    def SetCode(self):
        i = 0
        for t in self.parent.taches:
            if t.phase == self.phase:
                if t == self:
                    break
                i += 1
        num = str(i+1)

        typeEns = self.GetTypeEnseignement(True)
        
        if self.phase != "":
            if self.phase in ["R1", "R2", "S"]:
                self.code = self.phase
            else:
                self.code = constantes.CODE_PHASE_TACHE[typeEns][self.phase]+num
        else:
            self.code = num

        
        
        if hasattr(self, 'codeBranche') and self.phase != "":
            if self.phase in ["R1", "R2", "S"]:
                self.codeBranche.SetLabel(u"")
                t = u""
            else:
                self.codeBranche.SetLabel(self.code)
                t = u" :"
            self.arbre.SetItemText(self.branche, constantes.NOM_PHASE_TACHE[typeEns][self.phase]+t)
        
        
        # Tip
        if self.phase in ["R1", "R2", "S"]:
            self.tip.SetTitre(constantes.NOM_PHASE_TACHE_E[self.phase])
        elif self.phase == "Rev":
            self.tip.SetTitre(constantes.NOM_PHASE_TACHE_E[self.phase])
        else:
            self.tip.SetTitre(u"Tâche "+ self.code)
            if self.phase != "":
                t = constantes.NOM_PHASE_TACHE[typeEns][self.phase]
            else:
                t = u""
            self.tip.SetTexte(t, self.tip_phase)
            
            if self.intitule != "":
                t = textwrap.fill(self.intitule, 50)
            else:
                t = u""
            self.tip.SetTexte(t, self.tip_intitule)
        
            
        
        
            
            
            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, self.code)
        if self.phase != "":
            image = self.arbre.images[self.phase]
        else:
            image = -1
            
        self.branche = arbre.AppendItem(branche, u"Tâche :", wnd = self.codeBranche, 
                                        data = self, image = image)
        if self.phase in ["R1", "R2"]:
            arbre.SetItemTextColour(self.branche, "red")
        elif self.phase == "Rev":
            arbre.SetItemTextColour(self.branche, "ORANGE")
        elif self.phase == "S":
            arbre.SetItemTextColour(self.branche, "PURPLE")
    
    
    ######################################################################################  
    def MiseAJourNomsEleves(self):
        """ Met à jour la liste des élèves concernés par la tâche
            et la liste des élèves du panelPropriete de la tâche
        """
#        projet = self.GetDocument()
#        for i, s in enumerate(projet.eleves):
#            self.eleves[i].n = s.nom
#            self.nSystemes = len(sequence.systemes)
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJourListeEleves()
                                 
    
    #############################################################################
    def MiseAJourTypeEnseignement(self, type_ens):
        self.panelPropriete.MiseAJourTypeEnseignement(type_ens)
        
    ######################################################################################  
    def SupprimerSysteme(self, i):
        if self.typeSeance in ["AP", "ED", "P"]:
            del self.systemes[i]
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.sousSeances:
                s.SupprimerSysteme(i)

        
    ######################################################################################  
    def AjouterEleve(self):
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeEleves()
    
    
    ######################################################################################  
    def SupprimerEleve(self, i):
        if i in self.eleves:
            self.eleves.remove(i)

        for i, id in enumerate(self.eleves):
            if id > i:
                self.eleves[i] = id-1

        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeEleves()
        

    
    ######################################################################################  
    def MiseAJourPoidsCompetences(self, code = None):
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJourPoidsCompetences(code)
                
    ######################################################################################  
    def GetDocument(self):    
        return self.parent
    
    ######################################################################################  
    def GetClasse(self):
        return self.GetDocument().classe
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            if not self.phase in ["R1", "R2", "S"]:
                listItems = [[u"Supprimer", functools.partial(self.parent.SupprimerTache, item = itemArbre)]]
            else:
                listItems = []
            listItems.append([u"Insérer une revue après", functools.partial(self.parent.InsererRevue, item = itemArbre)])
            self.GetApp().AfficherMenuContextuel(listItems)
#            item2 = menu.Append(wx.ID_ANY, u"Créer une rotation")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterRotation, item = item), item2)
#            
#            item3 = menu.Append(wx.ID_ANY, u"Créer une série")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterSerie, item = item), item3)
        
        
        
#    ######################################################################################  
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
##            self.arbre.DoSelectItem(self.branche)
#            return self.branche
        
        
        
        
        
        
        
        
        
        
        
        
        
        
####################################################################################
#
#   Classe définissant les propriétés d'un système
#
####################################################################################
class Systeme(ElementDeSequence, Objet_sequence):
    def __init__(self, parent, panelParent, nom = u""):
        
        ElementDeSequence.__init__(self)
        
        self.parent = parent
        self.nom = nom
        self.nbrDispo = Variable(u"Nombre dispo", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [0,20], modeLog = False,
                              expression = None, multiple = False)
        self.image = None
        
        #
        # Création du Tip (PopupInfo)
        #
        self.tip = PopupInfo(self.parent.app, u"Système ou matériel")
        self.tip_nom = self.tip.CreerTexte((1,0))
        self.tip_nombre, self.tip_ctrllien = self.tip.CreerLien((2,0))
        self.tip_image = self.tip.CreerImage((3,0))
        
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Systeme(panelParent, self)
        
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
        
    ######################################################################################  
    def __repr__(self):
        return self.nom+" ("+str(self.nbrDispo.v[0])+")"
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
        root = ET.Element("Systeme")
        root.set("Nom", self.nom)
        self.lien.getBranche(root)
        root.set("Nbr", str(self.nbrDispo.v[0]))
        if self.image != None:
            root.set("Image", img2str(self.image.ConvertToImage()))
        
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        self.nom  = branche.get("Nom", "")
        self.lien.setBranche(branche, self.GetPath())

        self.nbrDispo.v[0] = eval(branche.get("Nbr", 1))
        data = branche.get("Image", "")
        if data != "":
            self.image = PyEmbeddedImage(data).GetBitmap()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.SetImage()
            self.panelPropriete.MiseAJour()

    ######################################################################################  
    def SetNombre(self):
        self.parent.VerifPb()
         
    ######################################################################################  
    def SetNom(self, nom):
        self.nom = nom
#        if nom != u"":
        if hasattr(self, 'arbre'):
            self.SetCode()
        
    ######################################################################################  
    def SetCode(self):
#        if hasattr(self, 'codeBranche'):
#            self.codeBranche.SetLabel(self.nom)
        if self.nom != "":
            t = self.nom
        else:
            t = u"Système ou matériel"
        
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
            
        # Tip
        if hasattr(self, 'tip'):
            self.tip.SetTexte(u"Nom : "+self.nom, self.tip_nom)
            self.tip.SetTexte(u"Nombre disponible : " + str(self.nbrDispo.v[0]), self.tip_nombre)

    ######################################################################################  
    def SetImage(self):
        self.tip.SetImage(self.image, self.tip_image)
        

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
#        self.codeBranche = wx.StaticText(self.arbre, -1, self.nom)

#        if self.image == None or self.image == wx.NullBitmap:
        image = self.arbre.images["Sys"]
#        else:
#            image = self.image.ConvertToImage().Scale(20, 20).ConvertToBitmap()
        self.branche = arbre.AppendItem(branche, u"Système ou matériel", data = self,#, wnd = self.codeBranche
                                        image = image)
#        self.SetNom(self.nom)
        self.SetNombre()
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerSysteme, item = itemArbre)],
                                                    [u"Créer un lien", self.CreerLien]])
            
            
#    ######################################################################################  
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
##            self.arbre.DoSelectItem(self.branche)
#            return self.branche
    
    
    
        
#    ######################################################################################  
#    def OuvrirListeSystemes(self, nomFichier):
#        fichier = open(nomFichier,'r')
##        try:
#        systemes = ET.parse(fichier).getroot()
#        self.setBranche(systemes)
#        
#        fichier.close()

#    ######################################################################################  
#    def EnregistrerListeSystemes(self, nomFichier):
#        wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
#        fichier = file(nomFichier, 'w')
#        
#        systemes = self.getBranche()
#        indent(systemes)
#        
#        ET.ElementTree(systemes).write(fichier)
#        fichier.close()
#        
#        wx.EndBusyCursor()
  










####################################################################################
#
#   Classe définissant les propriétés d'un support de projet
#
####################################################################################
class Support(ElementDeSequence, Objet_sequence):
    def __init__(self, parent, panelParent, nom = u""):
        
        ElementDeSequence.__init__(self)
        Objet_sequence.__init__(self)
        
        self.parent = parent
        self.nom = nom
        self.description = None
        
        self.image = None
        
        #
        # Création du Tip (PopupInfo)
        #
        self.tip = PopupInfo(self.parent.app, u"Support")
        self.tip_nom = self.tip.CreerTexte((1,0))
        self.tip_titrelien, self.tip_ctrllien = self.tip.CreerLien((2,0))
        self.tip_image = self.tip.CreerImage((3,0))
        self.tip_description = self.tip.CreerRichTexte(self, (4,0))
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Support(panelParent, self)
        
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
        
    ######################################################################################  
    def __repr__(self):
        return self.nom
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
        root = ET.Element("Support")
        root.set("Nom", self.nom)
        self.lien.getBranche(root)
        if self.description != None:
            root.set("Description", self.description)
        if self.image != None:
            root.set("Image", img2str(self.image.ConvertToImage()))
        
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        Ok = True
        self.nom  = branche.get("Nom", "")
        self.description = branche.get("Description", None)
        Ok = Ok and self.lien.setBranche(branche, self.GetPath())

        data = branche.get("Image", "")
        if data != "":
            self.image = PyEmbeddedImage(data).GetBitmap()
            
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.SetImage()
            self.panelPropriete.MiseAJour()
        
        return Ok
    
    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        if hasattr(self, 'pts_caract' ):
            for i, pt in enumerate(self.pts_caract):
                lst.append((pt, self, i))
                
        self.cadre = []
        
        return lst
    
    
    ######################################################################################  
    def SetNom(self, nom):
        self.nom = nom
#        if nom != u"":
        if hasattr(self, 'arbre'):
            self.SetCode()
        
    ######################################################################################  
    def PubDescription(self):
        """ Publie toutes les descriptions de séance
            (à l'ouverture)
        """
        self.tip.SetRichTexte()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.rtc.Ouvrir()
        
                
    ######################################################################################  
    def SetDescription(self, description):   
        if self.description != description:
            self.description = description
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.sendEvent()
            self.tip.SetRichTexte()
            
    ######################################################################################  
    def GetCode(self, i = None):
        return u"Support"

    ######################################################################################  
    def GetIntit(self, i = None):
        return self.nom
    
    ######################################################################################  
    def SetCode(self):
#        if hasattr(self, 'codeBranche'):
#            self.codeBranche.SetLabel(self.nom)
        if self.nom != "":
            t = self.nom
        else:
            t = u"Support"
        
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
            
        # Tip
        if hasattr(self, 'tip'):
            self.tip.SetTexte(u"Nom : "+self.nom, self.tip_nom)
            

    ######################################################################################  
    def SetImage(self):
        self.tip.SetImage(self.image, self.tip_image)
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        image = self.arbre.images["Sup"]
        self.branche = arbre.AppendItem(branche, u"Support", data = self,#, wnd = self.codeBranche
                                        image = image)


        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Créer un lien", self.CreerLien]])
            
            
#    ######################################################################################  
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
##            self.arbre.DoSelectItem(self.branche)
#            return self.branche
    
    
    
####################################################################################
#
#   Classe définissant les propriétés d'une personne
#
####################################################################################
class Personne(Objet_sequence):
    def __init__(self, parent, panelParent, id = 0):
        self.parent = parent
        self.nom = u""
        self.prenom = u""
        self.avatar = None
        self.id = id # Un identifiant unique = nombre > 0

        #
        # Création du Tip (PopupInfo)
        #
        self.tip = PopupInfo(self.parent.app, u"")
        self.tip_nom = self.tip.CreerTexte((1,0), flag = wx.ALIGN_LEFT|wx.TOP)
#        self.tip_nom.SetFont(wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        self.tip_avatar = self.tip.CreerImage((2,0))
        
        if self.code == 'Prf':
            self.tip.SetTitre(u"Professeur")
            self.tip_disc = self.tip.CreerTexte((3,0), flag = wx.ALIGN_LEFT|wx.TOP)
            self.tip_disc.SetFont(wx.Font(10, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        else:
            self.tip.SetTitre(self.titre.capitalize())
        
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Personne(panelParent, self)

    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
        
    ######################################################################################  
    def __repr__(self):
        return self.GetNomPrenom()

    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
        root = ET.Element(toDefautEncoding(supprime_accent(self.titre).capitalize()))
        
        root.set("Id", str(self.id))
        root.set("Nom", self.nom)
        root.set("Prenom", self.prenom)
        if self.avatar != None:
            root.set("Avatar", img2str(self.avatar.ConvertToImage()))
        
        if hasattr(self, 'referent'):
            root.set("Referent", str(self.referent))
            
        if hasattr(self, 'discipline'):
            root.set("Discipline", str(self.discipline))
            
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        Ok = True
        self.id  = eval(branche.get("Id", "0"))
        self.nom  = branche.get("Nom", "")
        self.prenom  = branche.get("Prenom", "")
        data = branche.get("Avatar", "")
        if data != "":
            self.avatar = PyEmbeddedImage(data).GetBitmap()
            
        if hasattr(self, 'referent'):
            self.referent = eval(branche.get("Referent", "False"))
            
        if hasattr(self, 'discipline'):
            self.discipline = branche.get("Discipline", 'Tec')
            
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.SetImage()
            self.panelPropriete.MiseAJour()
        
        return Ok

    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        if hasattr(self, 'pts_caract' ):
            for i, pt in enumerate(self.pts_caract):
                lst.append((pt, self, i))
                
        self.cadre = []
        
        return lst
    
    ######################################################################################  
    def GetNom(self):
        return self.nom.upper()
    
    ######################################################################################  
    def GetPrenom(self):
        return self.prenom.capitalize()
        
    ######################################################################################  
    def GetNomPrenom(self, disc = False):
        if disc and hasattr(self, 'discipline') and constantes.CODE_DISCIPLINES[self.discipline] != u"":
            d = u' ('+constantes.CODE_DISCIPLINES[self.discipline]+')'
        else:
            d = u""
        if self.nom == "" and self.prenom == "":
            return self.titre.capitalize()+' '+str(self.id+1)+d
        else:
            return self.GetPrenom() + ' ' + self.GetNom()+d
         
    
    ######################################################################################  
    def SetNom(self, nom):
        self.nom = nom
        if hasattr(self, 'arbre'):
            self.SetCode()
        
    ######################################################################################  
    def SetPrenom(self, prenom):
        self.prenom = prenom
#        if nom != u"":
        if hasattr(self, 'arbre'):
            self.SetCode()

    ######################################################################################  
    def SetCode(self):
#        if hasattr(self, 'codeBranche'):
#            self.codeBranche.SetLabel(self.nom)

        t = self.GetNomPrenom()
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
         
        self.SetTip()
        
        
    ######################################################################################  
    def SetTip(self):   
        # Tip
        if hasattr(self, 'tip'):
            self.tip.SetTexte(self.GetNomPrenom(), self.tip_nom)
            self.tip.SetImage(self.avatar, self.tip_avatar)

    ######################################################################################  
    def SetImage(self):
        self.tip.SetImage(self.avatar, self.tip_avatar)
        self.SetTip()
        
    


######################################################################################  
def supprime_accent(ligne):
    """ supprime les accents du texte source """
    accents = { 'a': ['à', 'ã', 'á', 'â'],
                'e': ['é', 'è', 'ê', 'ë'],
                'i': ['î', 'ï'],
                'u': ['ù', 'ü', 'û'],
                'o': ['ô', 'ö'] }
    for (char, accented_chars) in accents.iteritems():
        for accented_char in accented_chars:
            ligne = ligne.replace(accented_char, char)
    return ligne

####################################################################################
#
#   Classe définissant les propriétés d'un élève
#
####################################################################################
class Eleve(Personne, Objet_sequence):
    def __init__(self, parent, panelParent, id = 0):
        
        self.titre = u"élève"
        self.code = "Elv"
        Personne.__init__(self, parent, panelParent, id)
        
        #
        # Création du Tip (PopupInfo) - plus complexe pour pour une personne "standard"
        #
        dc = self.tip.CreerTexte((3,0), (1,2), txt = u"Durée d'activité :", flag = wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT)
        ec = self.tip.CreerTexte((4,0), (1,2), txt = u"Evaluabilité :", flag = wx.ALIGN_RIGHT|wx.TOP|wx.LEFT)
        rc = self.tip.CreerTexte((5,1), (1,1), txt = u"Revue :", flag = wx.ALIGN_RIGHT|wx.RIGHT)
        sc = self.tip.CreerTexte((6,1), (1,1), txt = u"Soutenance :", flag = wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM)
        
        self.tip_duree = self.tip.CreerTexte((3,2), flag = wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT|wx.LEFT)
        self.tip_evalR = self.tip.CreerTexte((5,2), flag = wx.ALIGN_LEFT|wx.RIGHT)
        self.tip_evalS = self.tip.CreerTexte((6,2), flag = wx.ALIGN_LEFT|wx.RIGHT|wx.BOTTOM)
        
        dc.SetFont(wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline = True))
        ec.SetFont(wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline = True))
        rc.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
        sc.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
        self.tip_duree.SetFont(wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.tip_evalR.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
        self.tip_evalS.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
               
        self.tip.DeplacerItem(self.tip_avatar, span = (1,3)) 
        self.tip.DeplacerItem(self.tip_nom, span = (1,3))      
        self.tip.DeplacerItem(None, span = (1,3))                        
        
        
        
            
    ######################################################################################  
    def GetDuree(self, partie = None):
        d = 0
        for t in self.parent.taches:
            if t.phase == partie:
                break
            if not t.phase in ["R1", "R2", "S"]:
                if self.id in t.eleves:
                    d += t.GetDuree()
        return d
        
    ######################################################################################  
    def GetEvaluabilite(self):
        """ Renvoie l'évaluabilité
            % revue
            % soutenance
        """ 
#        print "GetEvaluabilite", self
        r = s = 0
        
        dicPoids = constantes.dicPoidsIndicateurs[self.GetTypeEnseignement()]
#        print dicPoids
        dicIndicateurs = self.GetDicIndicateurs()
        tousIndicateurs = constantes.dicIndicateurs[self.GetTypeEnseignement()]
#        print "   ", dicIndicateurs
        for grp, poids in dicPoids.items():
            poidsGrp, dicIndicGrp = poids
            for comp, poidsIndic in dicIndicGrp.items():
                if comp in dicIndicateurs.keys():
                    for i, indic in enumerate(dicIndicateurs[comp]):
                        if indic:
                            p = 1.0*poidsIndic[i]/100 * poidsGrp/100
                            if tousIndicateurs[comp][i][1]:     # revue
                                r += p
                            else:
                                s += p
        
        if self.GetTypeEnseignement() == "SSI":
            r, s = r*2, s*2
            
#        print r,s
        return r, s
    

    ######################################################################################  
    def GetCompetences(self):
        lst = []
        for t in self.parent.taches:
            if self.id in t.eleves:
                lst.extend(t.competences)
        lst = list(set(lst))
        return lst
    
    ######################################################################################  
    def GetDicIndicateurs(self):
        """ Renvoie un dictionnaire des indicateurs que l'élève doit mobiliser
             (pour tracé)
                  clef = code compétence
                valeur = liste [True False ...] des indicateurs à mobiliser
        """
        indicateurs = {}
#        print " GetDicIndicateurs", self.id
        for t in self.parent.taches:
#            print "  ", t.eleves
            if self.id in t.eleves:     # L'élève est concerné par cette tâche
                indicTache = t.GetDicIndicateurs()
                for c, i in indicTache.items():
#                    print "    ",c,  i
                    if c in indicateurs.keys():
                        indicateurs[c] = [x or y for x, y in zip(indicateurs[c], i)]
                    else:
                        indicateurs[c] = i
        return indicateurs
        
        
    ######################################################################################  
    def GetTaches(self, revues = False):
        lst = []
        for t in self.parent.taches:
            if self.id in t.eleves:
                lst.append(t)
            if revues and t.phase in ["R1", "R2", "Rev"]:
                lst.append(t)
        lst = list(set(lst))
            
        return lst
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerEleve, item = itemArbre)]]
                                                    )
    
    
    ######################################################################################  
    def MiseAJourCodeBranche(self):
        duree = int(self.GetDuree())
        lab = " ("+str(duree)+"h) "
        self.codeDuree.SetLabel(lab)
        tol1 = constantes.DELTA_DUREE
        tol2 = constantes.DELTA_DUREE2
        if abs(duree-70) < tol1:
            self.codeDuree.SetBackgroundColour(COUL_OK)
            self.codeDuree.SetToolTipString(u"Durée de travail conforme")
        elif abs(duree-70) < tol2:
            self.codeDuree.SetBackgroundColour(COUL_BOF)
            self.codeDuree.SetToolTipString(u"Durée de travail conforme")
        else:
            self.codeDuree.SetBackgroundColour(COUL_NON)
            if duree < 70:
                self.codeDuree.SetToolTipString(u"Durée de travail insuffisante")
            else:
                self.codeDuree.SetToolTipString(u"Durée de travail trop importante")
        
        
        er, es = self.GetEvaluabilite()
        labr = rallonge(str(int(er*100))+"%")
        labs = rallonge(str(int(es*100))+"%")
        self.evaluR.SetLabel(labr)
        self.evaluS.SetLabel(labs)
        t = u"L'élève ne mobilise pas suffisamment de compétences pour être évalué lors "
        if er >= 0.5:
            self.evaluR.SetBackgroundColour(COUL_OK)
            self.evaluR.SetToolTipString(u"Evaluabilité des revues")
        else:
            self.evaluR.SetBackgroundColour(COUL_NON)
            self.evaluR.SetToolTipString(t+u"des revues")
        
        if es >= 0.5:
            self.evaluS.SetBackgroundColour(COUL_OK)
            self.evaluS.SetToolTipString(u"Evaluabilité de la soutenance")
        else:
            self.evaluS.SetBackgroundColour(COUL_NON)
            self.evaluS.SetToolTipString(t+u"de la soutenance")

        self.codeBranche.Layout()
        self.codeBranche.Fit()
    
    ######################################################################################  
    def SetCode(self):

        t = self.GetNomPrenom()

        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
            
        # Tip
        if hasattr(self, 'tip'):
            self.tip.SetTexte(self.GetNomPrenom(), self.tip_nom)
            er, es = self.GetEvaluabilite()
            duree = self.GetDuree()
            labr = str(int(er*100))+"% "
            labs = str(int(es*100))+"%"
            lab = draw_cairo.getHoraireTxt(duree)
            self.tip.SetTexte(rallonge(lab), self.tip_duree)
            self.tip.SetTexte(rallonge(labr), self.tip_evalR)
            self.tip.SetTexte(rallonge(labs), self.tip_evalS)
            self.tip.SetImage(self.avatar, self.tip_avatar)
            
            tol = 5
            if abs(duree-70) < tol:
                self.tip_duree.SetBackgroundColour(COUL_OK)
            else:
                self.tip_duree.SetBackgroundColour(COUL_NON)
            
            if er >= 0.5:
                self.tip_evalR.SetBackgroundColour(COUL_OK)
            else:
                self.tip_evalR.SetBackgroundColour(COUL_NON)
            
            if es >= 0.5:
                self.tip_evalS.SetBackgroundColour(COUL_OK)
            else:
                self.tip_evalS.SetBackgroundColour(COUL_NON)
            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.Panel(self.arbre, -1)
        sz = wx.BoxSizer(wx.HORIZONTAL)
        self.codeDuree = wx.StaticText(self.codeBranche, -1, "")
        self.evaluR = wx.StaticText(self.codeBranche, -1, "")
        self.evaluS = wx.StaticText(self.codeBranche, -1, "")
        sz.Add(self.codeDuree)
        sz.Add(self.evaluR)
        sz.Add(self.evaluS)
        self.codeBranche.SetSizerAndFit(sz)
        
#        if self.image == None or self.image == wx.NullBitmap:
        image = self.arbre.images[self.code]
#        else:
#            image = self.image.ConvertToImage().Scale(20, 20).ConvertToBitmap()
        self.branche = arbre.AppendItem(branche, "", data = self, wnd = self.codeBranche,
                                        image = image)
        self.SetCode()
        
        
        
####################################################################################
#
#   Classe définissant les propriétés d'un professeur
#
####################################################################################
class Prof(Personne):
    def __init__(self, parent, panelParent, id = 0):
        self.titre = u"prof"
        self.code = "Prf"
        self.discipline = "Tec"
        self.referent = False
        
        Personne.__init__(self, parent, panelParent, id)
        
        
    ######################################################################################  
    def SetDiscipline(self, discipline):
        self.discipline = discipline
        self.SetTip()
        self.MiseAJourCodeBranche()
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerProf, item = itemArbre)]])
        
    ######################################################################################  
    def MiseAJourCodeBranche(self):
        self.arbre.SetItemBold(self.branche, self.referent)
        self.codeDisc.SetLabel(u" "+constantes.CODE_DISCIPLINES[self.discipline]+u" ")
        self.codeDisc.SetBackgroundColour(constantes.GetCouleurWx(constantes.COUL_DISCIPLINES[self.discipline]))
        self.codeDisc.SetToolTipString(constantes.NOM_DISCIPLINES[self.discipline])
        
        self.codeBranche.Layout()
        self.codeBranche.Fit()
    
    ######################################################################################  
    def SetTip(self):   
        
        # Tip
        if hasattr(self, 'tip'):
#            print "SetTip", self.GetNomPrenom(), self.referent
            if self.referent:
                self.tip.SetTexte(u"<b>"+self.GetNomPrenom()+"</b>", self.tip_nom)
            else:
                self.tip.SetTexte(self.GetNomPrenom(), self.tip_nom)
#            if self.referent:
#                font = wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
#            else:
#                font = wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
#            self.tip_nom.SetFont(font)
#            self.tip_nom.Refresh()

            self.tip.SetImage(self.avatar, self.tip_avatar)
        
            self.tip.SetTexte(constantes.NOM_DISCIPLINES[self.discipline], self.tip_disc)
            self.tip_disc.SetForegroundColour(constantes.GetCouleurWx(constantes.COUL_DISCIPLINES[self.discipline]))     
        
            self.tip.Layout()
            self.tip.Fit()
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.Panel(self.arbre, -1)
        sz = wx.BoxSizer(wx.HORIZONTAL)
        self.codeDisc = wx.StaticText(self.codeBranche, -1, "")
        sz.Add(self.codeDisc)
        self.codeBranche.SetSizerAndFit(sz)
        
#        if self.image == None or self.image == wx.NullBitmap:
        image = self.arbre.images[self.code]
#        else:
#            image = self.image.ConvertToImage().Scale(20, 20).ConvertToBitmap()
        self.branche = arbre.AppendItem(branche, "", data = self, wnd = self.codeBranche,
                                        image = image)
        self.SetCode()
        
        
        
####################################################################################
#
#   Classe définissant le panel conteneur des panels de propriétés
#
####################################################################################    
class PanelConteneur(wx.Panel):    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)#, style = wx.BORDER_SIMPLE)
        
        self.bsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.bsizer)
        
        #
        # Le panel affiché
        #
        self.panel = None
    
    
    def AfficherPanel(self, panel):
        if self.panel != None:
            self.bsizer.Detach(self.panel)
            self.panel.Hide()
        self.panel = panel
        self.bsizer.Add(self.panel, 1, flag = wx.EXPAND|wx.GROW)
        self.panel.Show()
        self.bsizer.Layout()
        self.Refresh()


####################################################################################
#
#   Classes définissant la fenêtre principale de l'application
#
####################################################################################
class FenetrePrincipale(aui.AuiMDIParentFrame):
    def __init__(self, parent, fichier):
        aui.AuiMDIParentFrame.__init__(self, parent, -1, __appname__, style=wx.DEFAULT_FRAME_STYLE)
        
        wx.lib.colourdb.updateColourDB()
        
        #
        # le fichier de configuration de la fiche
        #
#        self.nomFichierConfig = os.path.join(APP_DATA_PATH,"configFiche.cfg")
#        # on essaye de l'ouvrir
#        try:
#            draw_cairo_seq.ouvrirConfigFiche(self.nomFichierConfig)
#        except:
#            print "Erreur à l'ouverture de configFiche.cfg" 

        #
        # Taille et position de la fenétre
        #
        self.SetMinSize((800,570)) # Taille mini d'écran : 800x600
        self.SetSize((1024,738)) # Taille pour écran 1024x768
        # On centre la fenétre dans l'écran ...
        self.CentreOnScreen(wx.BOTH)
        
        self.SetIcon(images.getlogoIcon())
        
        self.tabmgr = self.GetClientWindow().GetAuiManager()
        self.tabmgr.GetManagedWindow().Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnDocChanged)
        
        
        self.pleinEcran = False
        
        #############################################################################################
        # Instanciation et chargement des options
        #############################################################################################
        options = Options.Options()
        if options.fichierExiste():
            try :
                options.ouvrir(DEFAUT_ENCODING)
            except:
                print "Fichier d'options corrompus ou inexistant !! Initialisation ..."
                options.defaut()
        else:
            options.defaut()
        self.options = options
#        else:
#            options.defaut()
#        print options
        
        # On applique les options ...
#        self.DefinirOptions(options)
        
        #############################################################################################
        # Création du menu
        #############################################################################################
        self.CreateMenuBar()
        self.Bind(wx.EVT_MENU, self.commandeNouveau, id=10)
        self.Bind(wx.EVT_MENU, self.commandeOuvrir, id=11)
        self.Bind(wx.EVT_MENU, self.commandeEnregistrer, id=12)
        self.Bind(wx.EVT_MENU, self.commandeEnregistrerSous, id=13)
        self.Bind(wx.EVT_MENU, self.exporterFiche, id=15)
        self.Bind(wx.EVT_MENU, self.exporterDetails, id=16)
        self.Bind(wx.EVT_MENU, self.genererGrilles, id=17)
        self.Bind(wx.EVT_MENU, self.genererFicheValidation, id=19)
        self.Bind(wx.EVT_MENU, self.etablirBilan, id=18)
        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)
        
        self.Bind(wx.EVT_MENU, self.OnAide, id=21)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=22)
        
        self.Bind(wx.EVT_MENU, self.OnOptions, id=31)
        self.Bind(wx.EVT_MENU, self.OnRegister, id=32)
        
        self.Bind(EVT_APPEL_OUVRIR, self.OnAppelOuvrir)
        
        
        
        # Interception des frappes clavier
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        
        # Interception de la demande de fermeture
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
        #############################################################################################
        # Création de la barre d'outils
        #############################################################################################
        self.ConstruireTb()
        
#        #################################################################################################################
#        #
#        # Mise en place
#        #
#        #################################################################################################################
#        sizer = wx.BoxSizer(wx.VERTICAL)
#        sizer.Add(sizerTb, 0, wx.EXPAND)
#        sizer.Add(self.fenDoc, 0, wx.EXPAND)
#        self.SetSizer(sizer)
        
        if fichier != "":
            self.ouvrir(fichier)
    
            
    ###############################################################################################
    def ConstruireTb(self):
        """ Construction de la ToolBar
        """
#        print "ConstruireTb"

        #############################################################################################
        # Création de la barre d'outils
        #############################################################################################
        self.tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        
        
        tsize = (24,24)
        new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        save_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        saveas_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, tsize)
        
        self.tb.SetToolBitmapSize(tsize)
        
        self.tb.AddLabelTool(10, u"Nouveau", new_bmp, 
                             shortHelp=u"Création d'une nouvelle séquence ou d'un nouveau projet", 
                             longHelp=u"Création d'une nouvelle séquence ou d'un nouveau projet")
        

        self.tb.AddLabelTool(11, u"Ouvrir", open_bmp, 
                             shortHelp=u"Ouverture d'un fichier séquence ou projet", 
                             longHelp=u"Ouverture d'un fichier séquence ou projet")
        
        self.tb.AddLabelTool(12, u"Enregistrer", save_bmp, 
                             shortHelp=u"Enregistrement du document courant sous son nom actuel", 
                             longHelp=u"Enregistrement du document courant sous son nom actuel")
        

        self.tb.AddLabelTool(13, u"Enregistrer sous...", saveas_bmp, 
                             shortHelp=u"Enregistrement du document courant sous un nom différent", 
                             longHelp=u"Enregistrement du document courant sous un nom différent")
        
        self.Bind(wx.EVT_TOOL, self.commandeNouveau, id=10)
        self.Bind(wx.EVT_TOOL, self.commandeOuvrir, id=11)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrer, id=12)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrerSous, id=13)
        
        
        self.tb.AddSeparator()
        

        #################################################################################################################
        #
        # Outils "Projet"
        #
        #################################################################################################################
        self.tool_pe = self.tb.AddLabelTool(50, u"Ajouter un élève", images.Icone_ajout_eleve.GetBitmap(), 
                             shortHelp=u"Ajout d'un élève au projet", 
                             longHelp=u"Ajout d'un élève au projet")

        
        
        self.tool_pp = self.tb.AddLabelTool(51, u"Ajouter un professeur", images.Icone_ajout_prof.GetBitmap(), 
                             shortHelp=u"Ajout d'un professeur à l'équipe pédagogique", 
                             longHelp=u"Ajout d'un professeur à l'équipe pédagogique")

        
        
        self.tool_pt = self.tb.AddLabelTool(52, u"Ajouter une tâche", images.Icone_ajout_tache.GetBitmap(), 
                             shortHelp=u"Ajout d'une tâche au projet", 
                             longHelp=u"Ajout d'une tâche au projet")
        

        
        
        
        #################################################################################################################
        #
        # Outils "Séquence"
        #
        #################################################################################################################
        self.tool_ss = self.tb.AddLabelTool(60, u"Ajouter une séance", images.Icone_ajout_seance.GetBitmap(), 
                             shortHelp=u"Ajout d'une séance dans la séquence", 
                             longHelp=u"Ajout d'une séance dans la séquence")

        
        
        self.tool_sy = self.tb.AddLabelTool(61, u"Ajouter un système", images.Icone_ajout_systeme.GetBitmap(), 
                             shortHelp=u"Ajout d'un système", 
                             longHelp=u"Ajout d'un système")
#
#        
#        
#        self.tool_pt = self.tb_p.AddLabelTool(62, u"Ajouter ", images.Icone_ajout_tache.GetBitmap(), 
#                             shortHelp=u"Ajout d'une tâche au projet", 
#                             longHelp=u"Ajout d'une tâche au projet")
        

        self.tb.AddSeparator()
        #################################################################################################################
        #
        # Outils de Visualisation
        #
        #################################################################################################################
        saveas_bmp = images.Icone_fullscreen.GetBitmap()
        self.tb.AddLabelTool(100, u"Plein écran", saveas_bmp, 
                             shortHelp=u"Affichage de la fiche en plein écran (Echap pour quitter le mode plein écran)", 
                             longHelp=u"Affichage de la fiche en plein écran (Echap pour quitter le mode plein écran)")

        self.Bind(wx.EVT_TOOL, self.commandePleinEcran, id=100)
        
        
#        self.Bind(wx.EVT_TOOL, self.OnClose, id=wx.ID_EXIT)
#        
#        self.Bind(wx.EVT_TOOL, self.OnAide, id=21)
#        self.Bind(wx.EVT_TOOL, self.OnAbout, id=22)
#        
#        self.Bind(wx.EVT_TOOL, self.OnOptions, id=31)
#        self.Bind(wx.EVT_TOOL, self.OnRegister, id=32)
        
        self.tb.AddSeparator()
        
        
        
        #################################################################################################################
        #
        # Mise en place
        #
        #################################################################################################################
        self.tb.Realize()
        
        
        self.tb.RemoveTool(60)
        self.tb.RemoveTool(61)
        self.tb.RemoveTool(50)
        self.tb.RemoveTool(51)
        self.tb.RemoveTool(52)


    ###############################################################################################
    def ajouterOutilsProjet(self):
        self.tb.RemoveTool(50)
        self.tb.RemoveTool(51)
        self.tb.RemoveTool(52)
        self.tb.RemoveTool(60)
        self.tb.RemoveTool(61)

        self.tb.InsertToolItem(5,self.tool_pe)
        self.tb.InsertToolItem(6, self.tool_pp)
        self.tb.InsertToolItem(7, self.tool_pt)
        self.tb.Realize()
    
    ###############################################################################################
    def ajouterOutilsSequence(self):
        self.tb.RemoveTool(50)
        self.tb.RemoveTool(51)
        self.tb.RemoveTool(52)
        self.tb.RemoveTool(60)
        self.tb.RemoveTool(61)
        
        self.tb.InsertToolItem(5, self.tool_ss)
        self.tb.InsertToolItem(6, self.tool_sy)

        self.tb.Realize()
        
        
    
    ###############################################################################################
    def commandePleinEcran(self, event):
        self.pleinEcran = not self.pleinEcran
        

        if self.pleinEcran:
            win = self.GetNotebook().GetCurrentPage().nb.GetCurrentPage()
            self.fsframe = wx.Frame(self, -1)
            win.Reparent(self.fsframe)
            win.Bind(wx.EVT_KEY_DOWN, self.OnKey)
            self.fsframe.ShowFullScreen(True, style=wx.FULLSCREEN_ALL)
        else:
            win = self.fsframe.GetChildren()[0]
            win.Reparent(self.GetNotebook().GetCurrentPage().nb)
            self.fsframe.Destroy()
            win.SendSizeEventToParent()
            
    ###############################################################################################
    def CreateMenuBar(self):
        # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(10, u"&Nouveau\tCtrl+N")
        file_menu.Append(11, u"&Ouvrir\tCtrl+O")
        file_menu.Append(12, u"&Enregistrer\tCtrl+S")
        file_menu.Append(13, u"&Enregistrer sous ...")
        file_menu.AppendSeparator()
        file_menu.Append(15, u"&Exporter la fiche (PDF ou SVG)\tCtrl+E")
        file_menu.Append(16, u"&Exporter les détails\tCtrl+D")
        file_menu.Append(17, u"&Générer les grilles d'évaluation projet\tCtrl+G")
        file_menu.Append(19, u"&Générer le dossier de validation projet\tCtrl+V")
        file_menu.Append(18, u"&Générer une Synthèse pédagogique (SSI et ETT uniquement)\tCtrl+B")
        
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, u"&Quitter\tCtrl+Q")

        self.file_menu = file_menu
        
        
        tool_menu = wx.Menu()
#        tool_menu.Append(31, u"Options")
        self.menuReg = tool_menu.Append(32, u"a")
        self.MiseAJourMenu()
        

        help_menu = wx.Menu()
        help_menu.Append(21, u"&Aide en ligne\tF1")
        help_menu.AppendSeparator()
        help_menu.Append(22, u"A propos")

        mb.Append(file_menu, u"&Fichier")
        mb.Append(tool_menu, u"&Outils")
        mb.Append(help_menu, u"&Aide")
        
        self.SetMenuBar(mb)
    
    
    #############################################################################
    def MiseAJourMenu(self):
        if register.IsRegistered():
            self.menuReg.SetText(u"Désinscrire de la base de registre")
        else:
            self.menuReg.SetText(u"Inscrire dans la base de registre")
            
            
            
#    #############################################################################
#    def DefinirOptions(self, options):
#        return
#        self.options = options.copie()
#        #
#        # Options de Classe
#        #
#        
##        te = self.options.optClasse["TypeEnseignement"]
#        lstCI = self.options.optClasse["CentresInteretET"]
#        if False:
#            pass
##        if self.fichierCourantModifie and (te != TYPE_ENSEIGNEMENT \
##           or (te == 'ET' and getTextCI(CentresInterets[TYPE_ENSEIGNEMENT]) != lstCI)):
##            dlg = wx.MessageDialog(self, u"Type de classe incompatible !\n\n" \
##                                         u"Fermer la séquence en cours d'élaboration\n" \
##                                         u"avant de modifier des options de la classe.",
##                               'Type de classe incompatible',
##                               wx.OK | wx.ICON_INFORMATION
##                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
##                               )
##            dlg.ShowModal()
##            dlg.Destroy()
#        else:
##            TYPE_ENSEIGNEMENT = te
#
#            constantes.Effectifs["C"] = self.options.optClasse["Effectifs"]["C"]
#            constantes.NbrGroupes["G"] = self.options.optClasse["Effectifs"]["G"]
#            constantes.NbrGroupes["E"] = self.options.optClasse["Effectifs"]["E"]
#            constantes.NbrGroupes["P"] = self.options.optClasse["Effectifs"]["P"]
#                          
#            constantes.CentresInteretsET = lstCI
#                
#            constantes.PositionCibleCIET = self.options.optClasse["PositionsCI_ET"]
                
                
    #############################################################################
    def OnRegister(self, event): 
        if register.IsRegistered():
            ok = register.UnRegister()
        else:
            ok = register.Register(PATH)
        if not ok:
            messageErreur(self, u"Accès refusé",
                          u"Accès à la base de registre refusé !\n\n" \
                          u"Redémarrer pySequence en tant qu'administrateur.")
        else:
            self.MiseAJourMenu()
         
    #############################################################################
    def OnAbout(self, event):
        win = A_propos(self)
        win.ShowModal()
        
    #############################################################################
    def OnAide(self, event):
        webbrowser.open('http://code.google.com/p/pysequence/wiki/Aide')
        
        
    ###############################################################################################
    def commandeNouveau(self, event = None, ext = None):
        if ext == 'seq':
            child = FenetreSequence(self)
        elif ext == 'prj':
            child = FenetreProjet(self)
        else:
            dlg = DialogChoixDoc(self)
            val = dlg.ShowModal()
            if val == 1:
                child = FenetreSequence(self)  
            elif val == 2:
                child = FenetreProjet(self)
            else:
                child = None
            dlg.Destroy()
        
        self.OnDocChanged(None)
        
        if child != None:
            wx.CallAfter(child.Activate)

        return child
        
    ###############################################################################################
    def ouvrir(self, nomFichier):
        if nomFichier != '':
            ext = os.path.splitext(nomFichier)[1].lstrip('.')
            if not nomFichier in self.GetNomsFichiers():
                wx.BeginBusyCursor()
                child = self.commandeNouveau(ext = ext)
                if child != None:
                    child.ouvrir(nomFichier)
                wx.CallAfter(wx.EndBusyCursor)
            else:
                child = self.GetChild(nomFichier)
                texte = constantes.MESSAGE_DEJA[ext]
                if child.fichierCourant != '':
                    texte += "\n\n\t"+child.fichierCourant+"\n"
                    
                dialog = wx.MessageDialog(self, texte, 
                                          u"Confirmation", wx.YES_NO | wx.ICON_WARNING)
                retCode = dialog.ShowModal()
                if retCode == wx.ID_YES:
                    child.ouvrir(nomFichier)
        
        
        
    ###############################################################################################
    def commandeOuvrir(self, event = None, nomFichier=None):
        mesFormats = constantes.FORMAT_FICHIER['seqprj'] + constantes.FORMAT_FICHIER['seq'] + constantes.FORMAT_FICHIER['prj'] + constantes.TOUS_FICHIER
  
        if nomFichier == None:
            dlg = wx.FileDialog(
                                self, message=u"Ouvrir une séquence",# ou un projet",
#                                defaultDir = self.DossierSauvegarde, 
                                defaultFile = "",
                                wildcard = mesFormats,
                                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                                )

            if dlg.ShowModal() == wx.ID_OK:
                paths = dlg.GetPaths()
                nomFichier = paths[0]
            else:
                nomFichier = ''
            
            dlg.Destroy()
        
        self.ouvrir(nomFichier)
        
    ###############################################################################################
    def OnAppelOuvrir(self, evt):
        wx.CallAfter(self.ouvrir, evt.GetFile())
        
        
    ###############################################################################################
    def AppelOuvrir(self, nomFichier):
        evt = AppelEvent(myEVT_APPEL_OUVRIR, self.GetId())
        evt.SetFile(nomFichier)
        self.GetEventHandler().ProcessEvent(evt)
        
    #############################################################################
    def commandeEnregistrer(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.commandeEnregistrer(event)
        
    #############################################################################
    def commandeEnregistrerSous(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.commandeEnregistrerSous(event)
    
    #############################################################################
    def exporterFiche(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.exporterFiche(event)
              
    #############################################################################
    def exporterDetails(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.exporterDetails(event)
        
    #############################################################################
    def genererGrilles(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.genererGrilles(event)
            
    #############################################################################
    def genererFicheValidation(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.genererFicheValidation(event)
    
    #############################################################################
    def etablirBilan(self, event = None):
        win = FenetreBilan(self, self.GetFenetreActive().DossierSauvegarde)
        win.Show()
#        win.Destroy()
        
        
        
    #############################################################################
    def OnOptions(self, event, page = 0):
        options = self.options.copie()
        dlg = Options.FenOptions(self, options)
        dlg.CenterOnScreen()
        dlg.nb.SetSelection(page)

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
    
        if val == wx.ID_OK:
            self.DefinirOptions(options)
            self.AppliquerOptions()
            
        else:
            pass

        dlg.Destroy()
            
            
            

        
        
    ###############################################################################################
    def OnDocChanged(self, evt):
        """ Opérations de modification du menu et des barre d'outil 
            en fonction du type de document en cours
        """
        doc = self.GetClientWindow().GetAuiManager().GetManagedWindow().GetCurrentPage()
        if hasattr(doc, 'typ'):
            
            if doc.typ == "prj":
                self.ajouterOutilsProjet()
                self.Bind(wx.EVT_TOOL, doc.projet.AjouterEleve, id=50)
                self.Bind(wx.EVT_TOOL, doc.projet.AjouterProf, id=51)
                self.Bind(wx.EVT_TOOL, doc.projet.AjouterTache, id=52)
            elif doc.typ == "seq":
                self.ajouterOutilsSequence()
                self.Bind(wx.EVT_TOOL, doc.sequence.AjouterSeance, id=60)
                self.Bind(wx.EVT_TOOL, doc.sequence.AjouterSysteme, id=61)
    #                self.Bind(wx.EVT_TOOL, self.GetActiveChild().projet.AjouterEleve, id=50)
    #                self.Bind(wx.EVT_TOOL, self.GetActiveChild().projet.AjouterProf, id=51)
    #                self.Bind(wx.EVT_TOOL, self.GetActiveChild().projet.AjouterTache, id=52)
    
            if doc.typ == "prj":
                self.file_menu.Enable(18, False)
                self.file_menu.Enable(17, True)
                self.file_menu.Enable(19, True)
            elif doc.typ == "seq":
                self.file_menu.Enable(18, True)
                self.file_menu.Enable(17, False)
                self.file_menu.Enable(19, False)
                
           
        
    ###############################################################################################
    def OnKey(self, evt):
        keycode = evt.GetKeyCode()
        if keycode == wx.WXK_ESCAPE and self.pleinEcran:
            self.commandePleinEcran(evt)
        evt.Skip()
        
        
#    ###############################################################################################
#    def OnToolClick(self, event):
#        self.log.WriteText("tool %s clicked\n" % event.GetId())
#        #tb = self.GetToolBar()
#        tb = event.GetEventObject()
#        tb.EnableTool(10, not tb.GetToolEnabled(10))
 
        
    
    
                
    #############################################################################
    def GetChild(self, nomFichier):
        for m in self.GetChildren():
            if isinstance(m, aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    if isinstance(k, FenetreSequence):
                        if k.fichierCourant == nomFichier:
                            return k
        return
    
    
    #############################################################################
    def GetSequenceActive(self):
        return self.GetNotebook().GetCurrentPage().sequence
    
    #############################################################################
    def GetFenetreActive(self):
        return self.GetNotebook().GetCurrentPage()
    
    #############################################################################
    def GetNomsFichiers(self):
        lst = []
        for m in self.GetChildren():
            if isinstance(m, aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    if isinstance(k, FenetreSequence):
                        lst.append(k.fichierCourant)

        return lst
    
    
    
    
    #############################################################################
    def OnClose(self, evt):
#        try:
#            draw_cairo.enregistrerConfigFiche(self.nomFichierConfig)
#        except IOError:
#            print "   Permission d'enregistrer les options refusée...",
#        except:
#            print "   Erreur enregistrement options...",
            
#        try:
#            self.options.definir()
#            self.options.enregistrer()
#        except IOError:
#            print "   Permission d'enregistrer les options refusée...",
#        except:
#            print "   Erreur enregistrement options...",
        
        # Close all ChildFrames first else Python crashes
        toutferme = True
        for m in self.GetChildren():
            if isinstance(m, aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    if isinstance(k, FenetreDocument):
                        toutferme = toutferme and k.quitter()  
        
        if toutferme:
            evt.Skip()
            sys.exit()

        
        
########################################################################################
#
#
#  Classe définissant la fenêtre "Document" (séquence, projet, ...)
#     qui apparait en onglet
#
#
########################################################################################
class FenetreDocument(aui.AuiMDIChildFrame):
    def __init__(self, parent):
        
        aui.AuiMDIChildFrame.__init__(self, parent, -1, "")#, style = wx.DEFAULT_FRAME_STYLE | wx.SYSTEM_MENU)
#        self.SetExtraStyle(wx.FRAME_EX_CONTEXTHELP)
#        
        self.parent = parent
        
        # Use a panel under the AUI panes in order to work around a
        # bug on PPC Macs
        pnl = wx.Panel(self)
        self.pnl = pnl
        
        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(pnl)
        
        # panel de propriétés (conteneur)
        self.panelProp = PanelConteneur(pnl)
        
        #
        # Pour la sauvegarde
        #
        self.fichierCourant = u""
        self.DossierSauvegarde = u""
        self.fichierCourantModifie = False
            
        #
        # Un NoteBook comme conteneur de la fiche
        #
        self.nb = wx.Notebook(self.pnl, -1)
        
    
    def miseEnPlace(self):
        
        #############################################################################################
        # Mise en place de la zone graphique
        #############################################################################################
        self.mgr.AddPane(self.nb, 
                         aui.AuiPaneInfo().
                         CenterPane()
#                         Caption(u"Bode").
#                         PaneBorder(False).
#                         Floatable(False).
#                         CloseButton(False)
#                         Name("Bode")
#                         Layer(2).BestSize(self.zoneGraph.GetMaxSize()).
#                         MaxSize(self.zoneGraph.GetMaxSize())
                        )
        
        #############################################################################################
        # Mise en place de l'arbre
        #############################################################################################
        self.mgr.AddPane(self.arbre, 
                         aui.AuiPaneInfo().
#                         Name(u"Structure").
                         Left().Layer(1).
                         Floatable(False).
                         BestSize((250, -1)).
                         MinSize((250, -1)).
#                         DockFixed().
#                         Gripper(False).
#                         Movable(False).
                         Maximize().
                         Caption(u"Structure").
                         CaptionVisible(True).
#                         PaneBorder(False).
                         CloseButton(False)
#                         Show()
                         )
        
        #############################################################################################
        # Mise en place du panel de propriétés
        #############################################################################################
        self.mgr.AddPane(self.panelProp, 
                         aui.AuiPaneInfo().
#                         Name(u"Structure").
                         Bottom().
                         Layer(1).
#                         Floatable(False).
                         BestSize((600, 200)).
                         MinSize((600, 200)).
                         MinimizeButton(True).
                         Resizable(True).

#                         DockFixed().
#                         Gripper(True).
#                         Movable(False).
#                         Maximize().
                         Caption(u"Propriétés").
                         CaptionVisible(True).
#                         PaneBorder(False).
                         CloseButton(False)
#                         Show()
                         )
        

        self.mgr.Update()

        self.Bind(EVT_DOC_MODIFIED, self.OnDocModified)
        self.Bind(wx.EVT_CLOSE, self.quitter)
        
        self.definirNomFichierCourant('')
    
        sizer = wx.BoxSizer()
        sizer.Add(self.pnl, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        wx.CallAfter(self.Layout)
#        self.Layout()

         

    #############################################################################
    def fermer(self):
        self.mgr.UnInit()
        del self.mgr
        self.Destroy()
        return True
        
    #############################################################################
    def getNomFichierCourantCourt(self):
        return os.path.splitext(os.path.split(self.fichierCourant)[-1])[0]
    
    #############################################################################
    def MarquerFichierCourantModifie(self, modif = True):
        self.fichierCourantModifie = modif
        self.SetTitre(modif)

        
    #############################################################################
    def AfficherMenuContextuel(self, items):
        """ Affiche un menu contextuel contenant les items spécifiés
                items = [ [nom1, fct1], [nom2, fct2], ...]
        """
        menu = wx.Menu()
        
        for nom, fct in items:
            item1 = menu.Append(wx.ID_ANY, nom)
            self.Bind(wx.EVT_MENU, fct, item1)
        
        self.PopupMenu(menu)
        menu.Destroy()
    
    #############################################################################
    def dialogEnregistrer(self):
        mesFormats = constantes.FORMAT_FICHIER[self.typ] + constantes.TOUS_FICHIER
        dlg = wx.FileDialog(self, 
                            message = constantes.MESSAGE_ENR[self.typ], 
                            defaultDir=toDefautEncoding(self.DossierSauvegarde) , 
                            defaultFile="", wildcard=mesFormats, 
                            style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR
                            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
            self.enregistrer(path)
            self.DossierSauvegarde = os.path.split(path)[0]
        else:
            dlg.Destroy()
    
    #############################################################################
    def commandeEnregistrer(self, event = None):
        if self.fichierCourant != '':
            self.enregistrer(self.fichierCourant)
        else:
            self.dialogEnregistrer()        
            
    #############################################################################
    def commandeEnregistrerSous(self, event = None):
        self.dialogEnregistrer()
    
    #############################################################################
    def SetTitre(self, modif = False):
        t = self.classe.typeEnseignement
        if self.fichierCourant == '':
            t += u" - "+constantes.TITRE_DEFAUT[self.typ]
        else:
            t += u" - "+os.path.splitext(os.path.basename(self.fichierCourant))[0]
        if modif :
            t += " **"
        self.SetTitle(t)#toDefautEncoding(t))
        
    #############################################################################
    def exporterFichePDF(self, nomFichier):
        try:
            PDFsurface = cairo.PDFSurface(nomFichier, 595, 842)
        except IOError:
            Dialog_ErreurAccesFichier(nomFichier)
            wx.EndBusyCursor()
            return
        
        ctx = cairo.Context (PDFsurface)
        ctx.scale(820, 820) 
        if self.typ == 'seq':
            draw_cairo_seq.Draw(ctx, self.sequence)
        elif self.typ == 'prj':
            draw_cairo_prj.Draw(ctx, self.projet, pourDossierValidation = True)
        
        PDFsurface.finish()
        
    
    #############################################################################
    def exporterFiche(self, event = None):
        mesFormats = "pdf (.pdf)|*.pdf|" \
                     "svg (.svg)|*.svg"
#                     "swf (.swf)|*.swf"
        dlg = wx.FileDialog(
            self, message=u"Enregistrer la fiche sous ...", defaultDir=toDefautEncoding(self.DossierSauvegarde) , 
            defaultFile = os.path.splitext(self.fichierCourant)[0]+".pdf", 
            wildcard=mesFormats, style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR
            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath().encode(FILE_ENCODING)
            ext = os.path.splitext(path)[1]
            dlg.Destroy()
            wx.BeginBusyCursor()
            if ext == ".pdf":
                self.exporterFichePDF(path)
                self.DossierSauvegarde = os.path.split(path)[0]
                os.startfile(path)
            elif ext == ".svg":
                try:
                    SVGsurface = cairo.SVGSurface(path, 595, 842)
                except IOError:
                    Dialog_ErreurAccesFichier(path)
                    wx.EndBusyCursor()
                    return
                
                ctx = cairo.Context (SVGsurface)
                ctx.scale(820, 820) 
                if self.typ == 'seq':
                    draw_cairo_seq.Draw(ctx, self.sequence, mouchard = True)
                elif self.typ == 'prj':
                    draw_cairo_prj.Draw(ctx, self.projet)
                self.DossierSauvegarde = os.path.split(path)[0]
                SVGsurface.finish()
                self.enrichirSVG(path)
            wx.EndBusyCursor()

#                os.startfile(path)
#            elif ext == ".swf":
#                fichierTempo = tempfile.NamedTemporaryFile(delete=False)
#                SVGsurface = cairo.SVGSurface(fichierTempo, 595, 842)
#                ctx = cairo.Context (SVGsurface)
#                ctx.scale(820, 820) 
#                draw_cairo.Draw(ctx, self.sequence)
#                self.DossierSauvegarde = os.path.split(path)[0]
#                SVGsurface.finish()
#                svg_export.saveSWF(fichierTempo, path)
        else:
            dlg.Destroy()
        return
    
    
    #############################################################################
    def exporterDetails(self, event = None):
        if hasattr(self, 'projet'):
            win = FrameRapport(self, self.fichierCourant, self.projet, 'prj')
            win.Show()
        elif hasattr(self, 'sequence'):
            win = FrameRapport(self, self.fichierCourant, self.sequence, 'seq')
            win.Show()
#            win.Destroy()

    #############################################################################
    def genererGrilles(self, event = None):
        return
    
    #############################################################################
    def genererFicheValidation(self, event = None):
        return
    
    #############################################################################
    def quitter(self, event = None):
        if self.fichierCourantModifie:
            texte = constantes.MESSAGE_FERMER[self.typ]
            if self.fichierCourant != '':
                texte += "\n\n\t"+self.fichierCourant+"\n"
                
            dialog = wx.MessageDialog(self, texte, 
                                      u"Confirmation", wx.YES_NO | wx.CANCEL | wx.ICON_WARNING)
            retCode = dialog.ShowModal()
            if retCode == wx.ID_YES:
                self.commandeEnregistrer()
                return self.fermer()
    
            elif retCode == wx.ID_NO:
                
                return self.fermer()
                 
            else:
                return False
        
        else:            
            
            return self.fermer()


    #############################################################################
    def enrichirSVG(self, path):
        """ Enrichissement de l'image SVG avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens 
             - ...
        """
        epsilon = 0.001

        from xml.dom.minidom import parse
        doc = parse(path)
        
        f = open(path, 'w')

        defs = doc.getElementsByTagName("defs")[0]
        defs.appendChild(getElementFiltre(constantes.FILTRE1))
        
        def match(p0, p1):
            return abs(p0[0]-p1[0])<epsilon and abs(p0[1]-p1[1])<epsilon
        
        if self.typ == 'seq':
            pts_caract = self.sequence.GetPtCaract()
        else:
            pts_caract = self.projet.GetPtCaract()
        
        
        for p in doc.getElementsByTagName("path"):
            a = p.getAttribute("d")
            a = str(a).translate(None, 'MCLZ')
            l = a.split()
            if len(l) > 1:
                x, y = l[0], l[1]
                x, y = eval(x), eval(y)
                
                for pt, obj, flag in pts_caract:
                    if match((x, y), pt) :
                        obj.cadre.append((p, flag))
                        if type(flag) != str:
                            break 
        
        if self.typ == 'seq':
            self.sequence.EnrichiSVG(doc)
        elif self.typ == 'prj':
            self.projet.EnrichiObjetsSVG(doc)
            
        doc.writexml(f, '   ')
        f.close

 
 
def Dialog_ErreurAccesFichier(nomFichier):
    messageErreur(None, u'Erreur !',
                  u"Impossible d'accéder en écriture au fichier\n\n%s" %toDefautEncoding(nomFichier))


########################################################################################
#
#
#  Classe définissant la fenêtre "Séquence"
#
#
########################################################################################
class FenetreSequence(FenetreDocument):
    def __init__(self, parent):
        self.typ = 'seq'
        FenetreDocument.__init__(self, parent)
        
        #
        # La classe
        #
        self.classe = Classe(parent, self.panelProp)
        
        #
        # La séquence
        #
        self.sequence = Sequence(self, self.classe, self.panelProp)
        self.classe.SetDocument(self.sequence)
      
        #
        # Arbre de structure de la séquence
        #
        arbre = ArbreSequence(self.pnl, self.sequence, self.classe,  self.panelProp)
        self.arbre = arbre
        self.arbre.SelectItem(self.classe.branche)
        self.arbre.ExpandAll()
        
        #
        # Permet d'ajouter automatiquement les systèmes des préférences
        #
        self.sequence.Initialise()
        
        #
        # Zone graphique de la fiche de séquence
        #
        self.fiche = FicheSequence(self.nb, self.sequence)
        self.nb.AddPage(self.fiche, u"Fiche Séquence")
        
        #
        # Détails
        #
        self.pageDetails = RapportRTF(self.nb, rt.RE_READONLY)
        self.nb.AddPage(self.pageDetails, u"Détails des séances")
        
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
        self.miseEnPlace()
        
    ###############################################################################################
    def OnPageChanged(self, event):
        new = event.GetSelection()
        event.Skip()
        if new == 1: # On vient de cliquer sur la page "détails"
            self.pageDetails.Remplir(self.fichierCourant, self.sequence, self.typ)
     
            
    ###############################################################################################
    def OnDocModified(self, event):
        if event.GetDocument() == self.sequence:
            self.sequence.VerifPb()
            wx.CallAfter(self.fiche.Redessiner)
            self.MarquerFichierCourantModifie()
              
        
    ###############################################################################################
    def enregistrer(self, nomFichier):

        wx.BeginBusyCursor()
        fichier = file(nomFichier, 'w')
        
        # La séquence
        sequence = self.sequence.getBranche()
        classe = self.classe.getBranche()
        
        # La racine
        root = ET.Element("Sequence_Classe")
        root.append(sequence)
        root.append(classe)
        indent(root)
        
        ET.ElementTree(root).write(fichier, encoding = DEFAUT_ENCODING)
        
        fichier.close()
        self.definirNomFichierCourant(nomFichier)
        self.MarquerFichierCourantModifie(False)
        wx.EndBusyCursor()
        
        
        
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True):
        if not os.path.isfile(nomFichier):
            return
        
        self.Freeze()
        fichier = open(nomFichier,'r')
        self.definirNomFichierCourant(nomFichier)
        
        try:
            root = ET.parse(fichier).getroot()
            
            # La séquence
            sequence = root.find("Sequence")
            if sequence == None:
                self.sequence.setBranche(root)
                
            else:
                # La classe
                classe = root.find("Classe")
                self.classe.setBranche(classe)
                self.sequence.setBranche(sequence)  
                
        except:
            messageErreur(self,u"Erreur d'ouverture",
                          u"La séquence pédagogique\n    %s\n n'a pas pu être ouverte !" %nomFichier)
            fichier.close()
            self.Close()
#            wx.EndBusyCursor()
            return

        self.arbre.DeleteAllItems()
        root = self.arbre.AddRoot("")
        self.classe.ConstruireArbre(self.arbre, root)
        self.sequence.ConstruireArbre(self.arbre, root)
        
        self.sequence.CI.SetNum()
        self.sequence.SetCodes()
        self.sequence.PubDescription()
        self.sequence.SetLiens()
        self.sequence.VerifPb()
        self.sequence.VerrouillerClasse()
        self.arbre.SelectItem(self.classe.branche)

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        
        fichier.close()
        self.Thaw()
        
        if redessiner:
            wx.CallAfter(self.fiche.Redessiner)
        
    #############################################################################
    def definirNomFichierCourant(self, nomFichier = ''):
        self.fichierCourant = nomFichier
        self.sequence.SetPath(nomFichier)
        self.SetTitre()

    
    #############################################################################
    def AppliquerOptions(self):
        self.sequence.AppliquerOptions()   
    

########################################################################################
#
#
#  Classe définissant la fenêtre "Séquence"
#
#
########################################################################################
class FenetreProjet(FenetreDocument):
    def __init__(self, parent):
        self.typ = 'prj'
        FenetreDocument.__init__(self, parent)
        
        #
        # La classe
        #
        self.classe = Classe(parent, self.panelProp, pourProjet = True)
        
        #
        # Le projet
        #
        self.projet = Projet(self, self.classe, self.panelProp)
        self.classe.SetDocument(self.projet)
        
        #
        # Arbre de structure du projet
        #
        arbre = ArbreProjet(self.pnl, self.projet, self.classe,  self.panelProp)
        self.arbre = arbre
        self.arbre.SelectItem(self.classe.branche)
        self.arbre.ExpandAll()
        
        for t in self.projet.taches:
            t.SetCode()
        
        #
        # Zone graphique de la fiche de projet
        #
        self.fiche = FicheProjet(self.nb, self.projet)       
#        self.thread = ThreadRedess(self.fichePrj)
        self.nb.AddPage(self.fiche, u"Fiche Projet")
        
        #
        # Détails
        #
        self.pageDetails = RapportRTF(self.nb, rt.RE_READONLY)
        self.nb.AddPage(self.pageDetails, u"Tâches élèves détaillées")
        
        #
        # Dossier de validation
        #
        self.pageValid = genpdf.PdfPanel(self.nb)
        self.nb.AddPage(self.pageValid, u"Dossier de validation")
        
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
        
        self.miseEnPlace()
   
        
    ###############################################################################################
    def OnPageChanged(self, event):
        new = event.GetSelection()
        event.Skip()
        if new == 1: # On vient de cliquer sur la page "détails"
            self.pageDetails.Remplir(self.fichierCourant, self.projet, self.typ)
        elif new == 2: # On vient de cliquer sur la page "dossie de validation"
            self.pageValid.MiseAJour(self.projet, self)

        
    ###############################################################################################
    def OnDocModified(self, event):
        if event.GetDocument() == self.projet:
            self.projet.VerifPb()
            self.projet.SetCompetencesRevuesSoutenance()
            
            wx.CallAfter(self.fiche.Redessiner)

            self.MarquerFichierCourantModifie()
            
        
    ###############################################################################################
    def enregistrer(self, nomFichier):

        wx.BeginBusyCursor()
        fichier = file(nomFichier, 'w')
        
        # Le projet
        projet = self.projet.getBranche()
        classe = self.classe.getBranche()
        
        # La racine
        root = ET.Element("Projet_Classe")
        root.append(projet)
        root.append(classe)
        indent(root)
        
        ET.ElementTree(root).write(fichier, encoding = DEFAUT_ENCODING)
        
        fichier.close()
        self.definirNomFichierCourant(nomFichier)
        self.MarquerFichierCourantModifie(False)
        wx.EndBusyCursor()
        
        
        
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True):
        tps1 = time.clock()
        self.Freeze()
        fichier = open(nomFichier,'r')
        self.definirNomFichierCourant(nomFichier)
        
        Ok = True
        try:
            root = ET.parse(fichier).getroot()
            
            # Le projet
            projet = root.find("Projet")
            if projet == None:
                self.projet.setBranche(root)
                
            else:
                # La classe
                classe = root.find("Classe")
                Ok = Ok and self.classe.setBranche(classe)
                Ok = Ok and self.projet.setBranche(projet)  
                
            self.arbre.DeleteAllItems()
            root = self.arbre.AddRoot("")
            self.projet.SetCompetencesRevuesSoutenance()
            
        except:
            Ok = False
        
        if not Ok:
            messageErreur(self, u"Erreur d'ouverture",
                          u"Le projet\n    %s\nn'a pas pu être ouvert !" \
                          u"\n\nIl s'agit peut-être d'un fichier d'une ancienne version de pySequence." %nomFichier,
                               )
            fichier.close()
            self.Close()
            return
        
        self.classe.ConstruireArbre(self.arbre, root)
        self.projet.ConstruireArbre(self.arbre, root)
        self.projet.OrdonnerTaches()
        
        self.projet.PubDescription()
        self.projet.SetLiens()
        self.projet.MiseAJourDureeEleves()
        self.projet.MiseAJourNomProfs()
#        print "1", self.projet.taches[0].indicateurs
        self.projet.VerrouillerClasse()

#        self.arbre.SelectItem(self.classe.branche)

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        
        fichier.close()
        
        self.Thaw()
        
        if redessiner:
            wx.CallAfter(self.fiche.Redessiner)
        
#    
        tps2 = time.clock() 
        print tps2 - tps1
        
        
    #############################################################################
    def genererGrilles(self, event = None):
#        mesFormats = "Tableur Excel (.xls)|*.xls"
        
        def getNomFichier(prefixe, eleve, projet):
            nomFichier = prefixe+"_"+eleve.GetNomPrenom()+"_"+projet.intitule[:20]
            for c in ["\"", "/", "\", ", "?", "<", ">", "|", ":", "."]:
                nomFichier = nomFichier.replace(c, "_")
            return nomFichier


        def getTableurEtModif(projet, eleve):
            tableur = grilles.getTableau(self, projet)
            grilles.modifierGrille(projet, tableur, eleve)
#            try:
#                grilles.modifierGrille(projet, tableur, eleve)
#            except:
#                messageErreur(self, u"Accès refusé !",
#                              u"Impossible d'accéder au fichier.\n\nVérifier :\n" \
#                              u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
#                              u" - qu'Excel n'est pas déja ouvert (gestionnaire des tâches)")
            return tableur
        
        
        
        dlg = wx.DirDialog(self, message = u"Emplacement des grilles", 
                            style=wx.DD_DEFAULT_STYLE|wx.CHANGE_DIR
                            )
#        dlg.SetFilterIndex(0)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
            dlgb = wx.ProgressDialog   (u"Génération des grilles",
                                        u"",
                                        maximum = len(self.projet.eleves),
                                        parent=self,
                                        style = 0
                                        | wx.PD_APP_MODAL
                                        | wx.PD_CAN_ABORT
                                        #| wx.PD_CAN_SKIP
                                        #| wx.PD_ELAPSED_TIME
    #                                    | wx.PD_ESTIMATED_TIME
    #                                    | wx.PD_REMAINING_TIME
                                        #| wx.PD_AUTO_HIDE
                                        )

            
            count = 0
            for e in self.projet.eleves:
                if self.projet.GetTypeEnseignement() == 'SSI':
                    nomFichier = getNomFichier("Grille", e, self.projet)
                    dlgb.Update(count, u"Traitement du fichier\n\n"+nomFichier)
                    dlgb.Refresh()
                    count += 1
                    tableur = getTableurEtModif(self.projet, e)
                    tf = [[tableur, nomFichier]]
                else:
                    nomFichierR = getNomFichier("Grille_revue", e, self.projet)
                    nomFichierS = getNomFichier("Grille_soutenance", e, self.projet)
                    dlgb.Update(count, u"Traitement des fichiers\n\n"+nomFichierR+u"\n"+nomFichierS)
                    dlgb.Refresh()
                    count += 1
                    tableur = getTableurEtModif(self.projet, e)
                    tf = [[tableur[0], nomFichierR], [tableur[1], nomFichierS]]
                
                for t, f in tf:
                    try:
                        t.save(os.path.join(path, f))
                    except:
                        messageErreur(self, u"Erreur !",
                                      u"Impossible d'enregistrer le fichier.\n\nVérifier :\n" \
                                      u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
                                      u" - que le dossier choisi n'est pas protégé en écriture")
                    t.close()
            
            dlgb.Update(count, u"Toutes les grilles ont été créées avec succès dans le dossier :\n\n"+path)
            dlgb.Destroy() 
                
                
        else:
            dlg.Destroy()
            
            
    #############################################################################
    def genererFicheValidation(self, event = None):
#        mesFormats = "Tableur Excel (.xls)|*.xls"
        
        def getNomFichier(prefixe, projet):
            nomFichier = prefixe+"_"+projet.intitule[:20]
            for c in ["\"", "/", "\", ", "?", "<", ">", "|", ":", "."]:
                nomFichier = nomFichier.replace(c, "_")
            return nomFichier+".pdf"
        
        mesFormats = u"PDF (.pdf)|*.pdf"
        nomFichier = getNomFichier("FicheValidation", self.projet)
        dlg = wx.FileDialog(self, u"Enregistrer le dossier de validation",
                            defaultFile = nomFichier,
                            wildcard = mesFormats,
#                           defaultPath = globdef.DOSSIER_EXEMPLES,
                            style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR
                            #| wx.DD_DIR_MUST_EXIST
                            #| wx.DD_CHANGE_DIR
                            )
        
        
        
#        dlg = wx.DirDialog(self, message = u"Emplacement de la fiche", 
#                            style=wx.DD_DEFAULT_STYLE|wx.CHANGE_DIR
#                            )
#        dlg.SetFilterIndex(0)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
            nomFichier = path
#            nomFichier = getNomFichier("FicheValidation", self.projet)
#            nomFichier = os.path.join(path, nomFichier)
#            print nomFichier
            try:
                genpdf.genererDossierValidation(nomFichier, self.projet, self)
                os.startfile(nomFichier)
            except IOError:
                messageErreur(self, u"Erreur !",
                                  u"Impossible d'enregistrer le fichier.\n\nVérifier :\n" \
                                  u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
                                  u" - que le dossier choisi n'est pas protégé en écriture\n\n" \
                                  + nomFichier)
                
            
#            for t, f in tf:
#                try:
#                    t.save(os.path.join(path, f))
#                except:
#                    messageErreur(self, u"Erreur !",
#                                  u"Impossible d'enregistrer le fichier.\n\nVérifier :\n" \
#                                  u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
#                                  u" - que le dossier choisi n'est pas protégé en écriture")
#                t.close()
#            
#            dlgb.Update(count, u"Toutes les grilles ont été créées avec succès dans le dossier :\n\n"+path)
#            dlgb.Destroy() 
#                
                
        else:
            dlg.Destroy()
            
            
    #############################################################################
    def definirNomFichierCourant(self, nomFichier = ''):
        self.fichierCourant = nomFichier
#        self.projet.SetPath(nomFichier)
        self.SetTitre()

    
    #############################################################################
    def AppliquerOptions(self):
        self.projet.AppliquerOptions() 
    
    
#class ThreadRedess(Thread):
#    def __init__(self, fiche):
#        Thread.__init__(self)
#        self.fiche = fiche
#        
#    def run(self):
#        self.fiche.enCours = True
#        self.fiche.Redessiner()
#        Thread.__init__(self)
#        self.fiche.enCours = False

        
####################################################################################
#
#   Classe définissant la base de la fenétre de fiche
#
####################################################################################
class BaseFiche(wx.ScrolledWindow):
    def __init__(self, parent):
#        wx.Panel.__init__(self, parent, -1)
        wx.ScrolledWindow.__init__(self, parent, -1, style = wx.VSCROLL | wx.RETAINED)
        
        self.EnableScrolling(False, True)
        self.SetScrollbars(20, 20, 50, 50);
        
        self.enCours = False
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDClick)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRClick)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_MOTION, self.OnMove)

        self.InitBuffer()

    ######################################################################################################
    def OnLeave(self, evt = None):
        if hasattr(self, 'call') and self.call.IsRunning():
            self.call.Stop()
#        if hasattr(self, 'tip') 
#            self.tip.Show(False)

    ######################################################################################################
    def OnEnter(self, event):
#        self.SetFocus()
        event.Skip()
        
    #############################################################################            
    def OnResize(self, evt):
        
        w, h = self.GetClientSize()
        self.SetVirtualSize((w,w*29/21)) # Mise au format A4

        self.InitBuffer()
        if w > 0 and self.IsShown():
            self.Redessiner()


    #############################################################################            
    def OnPaint(self, evt):
#        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.DrawBitmap(self.buffer, 0,0) 
        
        
    #############################################################################            
    def CentrerSur(self, obj):
        if hasattr(obj, 'rect'):
            y = (obj.rect[0][1])*self.GetVirtualSizeTuple()[1]
            self.Scroll(0, y/20)
        return
    
    
    #############################################################################            
    def OnClick(self, evt):
        _x, _y = self.CalcUnscrolledPosition(evt.GetX(), evt.GetY())
        xx, yy = self.ctx.device_to_user(_x, _y)
        
        #
        # Changement de branche sur l'arbre
        #
        branche = self.GetDoc().HitTest(xx, yy)
        if branche != None:
#            print "Selectitem"
#            self.GetDoc().arbre.EnsureVisible(branche)
#            self.GetDoc().arbre.CalculatePositions()
#            self.GetDoc().arbre.ScrollTo(branche)
#            self.GetDoc().arbre.RefreshSubtree(self.GetDoc().arbre.root) 
#            
#            self.GetDoc().arbre.AdjustMyScrollbars()
#            self.GetDoc().arbre.Collapse(self.GetDoc().arbre.root)
#            self.GetDoc().arbre.Update()
            self.GetDoc().SelectItem(branche, depuisFiche = True)
#            self.GetDoc().arbre.SelectItem(branche)
#            self.GetDoc().arbre.DoSelectItem(branche, extended_select=True)
#            self.GetDoc().arbre.CalculatePositions()
#            self.GetDoc().arbre.AdjustMyScrollbars()
#            self.GetDoc().arbre.ExpandAll()
#            
#            self.GetDoc().arbre.Layout()
            

        #
        # Autres actions
        #
        position = self.GetDoc().HitTestPosition(xx, yy)
        if position != None:
            self.projet.SetPosition(position)
            if hasattr(self.GetDoc(), 'panelPropriete'):
                self.GetDoc().panelPropriete.SetBitmapPosition(bougerSlider = position)
            
        return branche
    
    
    #############################################################################            
    def OnDClick(self, evt):
        item = self.OnClick(evt)
        if item != None:
            self.GetDoc().AfficherLien(item)
            
            
    #############################################################################            
    def OnRClick(self, evt):
        item = self.OnClick(evt)
        if item != None:
            self.GetDoc().AfficherMenuContextuel(item)
            
            
    #############################################################################            
    def InitBuffer(self):
#        print "InitBuffer", 
        w,h = self.GetVirtualSize()
#        print w,h
        self.buffer = wx.EmptyBitmap(w,h)


    #############################################################################            
    def Redessiner(self, event = None):  
        wx.BeginBusyCursor()
        tps = time.time()
            
        cdc = wx.ClientDC(self)
        self.PrepareDC(cdc) 
        dc = wx.BufferedDC(cdc, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        ctx = wx.lib.wxcairo.ContextFromDC(dc)
#        face = wx.lib.wxcairo.FontFaceFromFont(wx.FFont(10, wx.SWISS, wx.FONTFLAG_BOLD))
#        ctx.set_font_face(face)
        dc.BeginDrawing()
        self.normalize(ctx)
        
        
        self.Draw(ctx)
        
#        b = Thread(None, self.Draw, None, (ctx,))
#        b.start()
        
        dc.EndDrawing()
        self.ctx = ctx
        self.Refresh()

#        print "   ", time.time() - tps
        wx.EndBusyCursor()
    
    #############################################################################            
    def normalize(self, cr):
        w,h = self.GetVirtualSize()
        cr.scale(h, h) 
        
        
        
        
        
        
        
        
####################################################################################
#
#   Classe définissant la fenétre de la fiche de séquence
#
####################################################################################
class FicheSequence(BaseFiche):
    def __init__(self, parent, sequence):
        BaseFiche.__init__(self, parent)
        self.sequence = sequence


    ######################################################################################################
    def GetDoc(self):
        return self.sequence
       
    ######################################################################################################
    def OnMove(self, evt):
        if hasattr(self, 'tip'):
            self.tip.Show(False)
            self.call.Stop()
        x, y = evt.GetPosition()
        _x, _y = self.CalcUnscrolledPosition(x, y)
        xx, yy = self.ctx.device_to_user(_x, _y)
        branche = self.sequence.HitTest(xx, yy)
        if branche != None:
            elem = branche.GetData()
            if hasattr(elem, 'tip'):
                x, y = self.ClientToScreen((x, y))
                elem.tip.Position((x,y), (0,0))
                self.call = wx.CallLater(500, elem.tip.Show, True)
                self.tip = elem.tip
        evt.Skip()


    #############################################################################            
    def Draw(self, ctx):
        draw_cairo_seq.Draw(ctx, self.sequence)
        
        
#    #############################################################################            
#    def OnClick(self, evt):
#        x, y = evt.GetX(), evt.GetY()
#        _x, _y = self.CalcUnscrolledPosition(x, y)
#        xx, yy = self.ctx.device_to_user(_x, _y)
#        
#        #
#        # Changement de branche sur l'arbre
#        #
#        branche = self.sequence.HitTest(xx, yy)
#        if branche != None:
#            self.sequence.arbre.SelectItem(branche)
#
#
#        #
#        # Autres actions
#        #
#        position = self.sequence.HitTestPosition(xx, yy)
#        if position != None:
#            self.sequence.SetPosition(position)
#            if hasattr(self.sequence, 'panelPropriete'):
#                self.sequence.panelPropriete.SetBitmapPosition(bougerSlider = position)
#            
#        return branche
    
    



    
####################################################################################
#
#   Classe définissant la fenétre de la fiche de séquence
#
####################################################################################
class FicheProjet(BaseFiche):
    def __init__(self, parent, projet):
        BaseFiche.__init__(self, parent)
        self.projet = projet
        
        #
        # Création du Tip (PopupInfo) pour les compétences
        #
        l = 0
        popup = PopupInfo(self.projet.GetApp(), u"Compétence")
        popup.sizer.SetItemSpan(popup.titre, (1,2)) 
        l += 1
        
        self.tip_comp = popup.CreerTexte((l,0), (1,2), flag = wx.ALL)
        self.tip_comp.SetForegroundColour("CHARTREUSE4")
        self.tip_comp.SetFont(wx.Font(11, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        l += 1
        
        self.tip_compp = popup.CreerTexte((l,0), (1,2), flag = wx.ALL)
        self.tip_compp.SetForegroundColour("CHARTREUSE3")
        self.tip_compp.SetFont(wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        l += 1
            
        self.lab_indic = popup.CreerTexte((l,0), txt = u"Indicateur :", flag = wx.ALIGN_RIGHT|wx.RIGHT)
        self.lab_indic.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline = True))
        self.tip_indic = []
        l += 1
        
        self.lab_legend1 = popup.CreerTexte((l,0), txt = u"Revues", flag = wx.ALIGN_RIGHT|wx.RIGHT)
        self.lab_legend1.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
        self.lab_legend1.SetForegroundColour(constantes.COUL_REVUE)
        
        self.lab_legend2 = popup.CreerTexte((l,1), txt = u"Soutenance", flag = wx.ALIGN_LEFT|wx.LEFT)
        self.lab_legend2.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
        self.lab_legend2.SetForegroundColour(constantes.COUL_SOUT)
        
        self.popup = popup
        self.MiseAJourTypeEnseignement(self.projet.classe.typeEnseignement)
        
    ######################################################################################################
    def GetDoc(self):
        return self.projet
            
    ######################################################################################################
    def OnMove(self, evt):
        
        if hasattr(self, 'tip'):
            self.tip.Show(False)
            self.call.Stop()
        
        x, y = evt.GetPosition()
        _x, _y = self.CalcUnscrolledPosition(x, y)
        xx, yy = self.ctx.device_to_user(_x, _y)
        evt.Skip()
        branche = self.projet.HitTest(xx, yy)
        if branche != None:
            elem = branche.GetData()
            if hasattr(elem, 'tip'):
                x, y = self.ClientToScreen((x, y))
                elem.tip.Position((x,y), (0,0))
                self.call = wx.CallLater(500, elem.tip.Show, True)
                self.tip = elem.tip
                evt.Skip()
                return    
        
        kCompObj = self.projet.HitTestCompetence(xx, yy)
        if kCompObj != None:
            kComp, obj = kCompObj
            if hasattr(self, 'popup'):
                for tip in self.tip_indic:
                    tip.Destroy()
                self.tip_indic = []
                x, y = self.ClientToScreen((x, y))
                type_ens = self.projet.classe.typeEnseignement
                competence = constantes.dicCompetences_prj_simple[type_ens][kComp]
                if type_ens == "SSI":
                    competencePlus = constantes.dicCompetences[type_ens][kComp[0]][1][kComp][1].values()
                indicTache = obj.GetDicIndicateurs()[kComp]
                
                self.MiseAJourTypeEnseignement(type_ens)
                
                indicateurs = constantes.dicIndicateurs[type_ens][kComp]
          
                self.popup.SetTitre(u"Compétence "+kComp)
                self.popup.SetTexte(textwrap.fill(competence, 50), self.tip_comp)
                
                if type_ens == "SSI":
                    t = ''
                    for cp in competencePlus:
                        t += textwrap.fill(u"\u25CF " + cp, 50)+"\n"
                    self.popup.SetTexte(t, self.tip_compp)
                
                self.popup.DeplacerItem(self.lab_legend1, (4+len(indicateurs), 0))
                self.popup.DeplacerItem(self.lab_legend2, (4+len(indicateurs), 1))
                    
                for i, indic in enumerate(indicateurs):
                    indic, revue = indic
                    if indicTache[i]:
                        if revue:
                            coul = constantes.COUL_REVUE
                        else:
                            coul = constantes.COUL_SOUT
                    else:
                        coul = "GREY"
                    self.tip_indic.append(self.popup.CreerTexte((3+i,1), flag = wx.ALIGN_LEFT|wx.LEFT))
                    self.tip_indic[i].SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
                    self.tip_indic[i].SetForegroundColour(coul)

                    self.popup.SetTexte(textwrap.fill(indic, 50), self.tip_indic[i])
                    
                self.popup.Position((x,y), (0,0))
                self.call = wx.CallLater(500, self.popup.Show, True)
                self.tip = self.popup
            
        evt.Skip()


    #############################################################################
    def MiseAJourTypeEnseignement(self, type_ens):
        texte = u"Indicateur"
        if type_ens != "SSI":
            texte += u"s"
        self.popup.SetTexte(texte, self.lab_indic)
        self.tip_compp.Show(type_ens == "SSI")
#        self.tip_poids.Show(type_ens == "SSI")
            
        
    #############################################################################            
    def Draw(self, ctx):
        draw_cairo_prj.Draw(ctx, self.projet)
        
        
    
    
        
            
                         
                
####################################################################################
#
#   Classe définissant le panel de propriété par défaut
#
####################################################################################
DELAY = 100 # Delai en millisecondes avant de rafraichir l'affichage suite à un saisie au clavier
class PanelPropriete(scrolled.ScrolledPanel):
    def __init__(self, parent, titre = u"", objet = None, style = wx.VSCROLL | wx.RETAINED):
        scrolled.ScrolledPanel.__init__(self, parent, -1, style = style)#|wx.BORDER_SIMPLE)
        
        self.sizer = wx.GridBagSizer()
        self.Hide()
#        self.SetMinSize((400, 200))
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
#        self.SetScrollRate(20,20)
        self.SetupScrolling()
#        self.EnableScrolling(True, True)
        self.eventAttente = False
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)


    ######################################################################################################
    def OnEnter(self, event):
#        self.SetFocus()
        event.Skip()

       
    #########################################################################################################
    def sendEvent(self, doc = None):
        self.eventAttente = False
        evt = SeqEvent(myEVT_DOC_MODIFIED, self.GetId())
        if doc != None:
            evt.SetDocument(doc)
        else:
            evt.SetDocument(self.GetDocument())

        self.GetEventHandler().ProcessEvent(evt)
        

####################################################################################
#
#   Classe définissant le panel de propriété de type Book
#
####################################################################################
class PanelProprieteBook(wx.Notebook, PanelPropriete):
    def __init__(self, parent, titre = u"", objet = None):
        wx.Notebook.__init__(self, parent, -1,  style= wx.BK_DEFAULT)#| wx.BORDER_SIMPLE)
        self.eventAttente = False
#        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)


    def OnPageChanged(self, event):
#        old = event.GetOldSelection()
#        new = event.GetSelection()
#        sel = self.GetSelection()
        
        event.Skip()

#    #########################################################################################################
#    def sendEvent(self, doc = None):
#        evt = SeqEvent(myEVT_DOC_MODIFIED, self.GetId())
#        if doc != None:
#            evt.SetDocument(doc)
#        else:
#            evt.SetDocument(self.GetDocument())
#        
#        self.GetEventHandler().ProcessEvent(evt)
#        self.eventAttente = False
        
        
####################################################################################
#
#   Classe définissant le panel "racine" 
#
####################################################################################
import wx.richtext as rt
class PanelPropriete_Racine(wx.Panel):
    def __init__(self, parent, texte):
        wx.Panel.__init__(self, parent, -1)
        self.Hide()

        self.rtc = rt.RichTextCtrl(self, style=rt.RE_READONLY|wx.NO_BORDER)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.rtc, 1,flag = wx.EXPAND)
        self.SetSizer(sizer)

        out = cStringIO.StringIO()
        handler = rt.RichTextXMLHandler()
        buff = self.rtc.GetBuffer()
        buff.AddHandler(handler)
        out.write(texte)
        out.seek(0)
        handler.LoadStream(buff, out)
        self.rtc.Refresh()
        
        sizer.Layout()
        wx.CallAfter(self.Layout)


     

####################################################################################
#
#   Classe définissant le panel de propriété de séquence
#
####################################################################################
class PanelPropriete_Sequence(PanelPropriete):
    def __init__(self, parent, sequence):
        PanelPropriete.__init__(self, parent)
        self.sequence = sequence
        
        titre = wx.StaticBox(self, -1, u"Intitulé de la séquence")
        sb = wx.StaticBoxSizer(titre)
        textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        self.sizer.Add(sb, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
#        self.sizer.Add(textctrl, (0,1), flag = wx.EXPAND)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        titre = wx.StaticBox(self, -1, u"Commentaires")
        sb = wx.StaticBoxSizer(titre)
        commctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        sb.Add(commctrl, 1, flag = wx.EXPAND)
        self.commctrl = commctrl
        self.sizer.Add(sb, (0,1), (2,1),  flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
#        self.sizer.Add(commctrl, (1,1), flag = wx.EXPAND)
        self.Bind(wx.EVT_TEXT, self.EvtText, commctrl)
        self.sizer.AddGrowableCol(1)
        
        titre = wx.StaticBox(self, -1, u"Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        self.bmp = wx.StaticBitmap(self, -1, self.getBitmapPeriode(250))
        position = wx.Slider(self, -1, self.sequence.position, 0, 7, (30, 60), (250, -1), 
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS |wx.SL_TOP 
            )
        sb.Add(self.bmp)
        sb.Add(position)
        self.position = position
        self.sizer.Add(sb, (1,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        position.Bind(wx.EVT_SCROLL_CHANGED, self.onChanged)
        
        self.sizer.Layout()
        wx.CallAfter(self.Layout)
        
#        self.Fit()
        
    
    #############################################################################            
    def getBitmapPeriode(self, larg):
        w, h = 0.04*5, 0.04
        imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  larg, int(h/w*larg))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        ctx = cairo.Context(imagesurface)
        ctx.scale(larg/w, larg/w) 
        draw_cairo_seq.DrawPeriodes(ctx, self.sequence.position, origine = True)

        bmp = wx.lib.wxcairo.BitmapFromImageSurface(imagesurface)
        return bmp
         
    
    #############################################################################            
    def onChanged(self, evt):
        self.sequence.SetPosition(evt.EventObject.GetValue())
        self.SetBitmapPosition()
        
        
    #############################################################################            
    def SetBitmapPosition(self, bougerSlider = None):
        self.sendEvent()
        self.bmp.SetBitmap(self.getBitmapPeriode(250))
        if bougerSlider != None:
            self.position.SetValue(bougerSlider)
        
    #############################################################################            
    def EvtText(self, event):
        if event.GetEventObject() == self.textctrl:
            self.sequence.SetText(event.GetString())
        else:
            self.sequence.SetCommentaire(event.GetString())
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.textctrl.ChangeValue(self.sequence.intitule)
        self.Layout()
        if sendEvt:
            self.sendEvent()

    #############################################################################            
    def GetDocument(self):
        return self.sequence
    
    
####################################################################################
#
#   Classe définissant le panel de propriété du projet
#
####################################################################################
class PanelPropriete_Projet(PanelPropriete):
    def __init__(self, parent, projet):
        PanelPropriete.__init__(self, parent)
        
        self.projet = projet
        
        nb = wx.Notebook(self, -1,  style= wx.BK_DEFAULT)
        
        #
        # La page "Généralités"
        #
        pageGen = PanelPropriete(nb)
        bg_color = self.Parent.GetBackgroundColour()
        pageGen.SetBackgroundColour(bg_color)
        self.pageGen = pageGen
        
        nb.AddPage(pageGen, u"Propriétés générales")
        
#        pageGen.sizer.Add(nb, (0,1), (2,1), flag = wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND, border = 1)
            
        
        titre = wx.StaticBox(pageGen, -1, u"Intitulé du projet")
        sb = wx.StaticBoxSizer(titre)
        textctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        pageGen.sizer.Add(sb, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
#        self.sizer.Add(textctrl, (0,1), flag = wx.EXPAND)
        pageGen.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        titre = wx.StaticBox(pageGen, -1, u"Problématique - Énoncé général du besoin")
        sb = wx.StaticBoxSizer(titre)
        commctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
        commctrl.SetToolTipString(constantes.TIP_PROBLEMATIQUE)
        sb.Add(commctrl, 1, flag = wx.EXPAND)
        self.commctrl = commctrl
        pageGen.sizer.Add(sb, (0,1), (2,1),  flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
#        self.sizer.Add(commctrl, (1,1), flag = wx.EXPAND)
        pageGen.Bind(wx.EVT_TEXT, self.EvtText, commctrl)
        pageGen.sizer.AddGrowableCol(1)
        
        titre = wx.StaticBox(pageGen, -1, u"Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        self.bmp = wx.StaticBitmap(pageGen, -1, self.getBitmapPeriode(250))
        position = wx.Slider(pageGen, -1, self.projet.position, 0, 5, (30, 60), (190, -1), 
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS |wx.SL_TOP 
            )
        sb.Add(self.bmp)
        sb.Add(position)
        self.position = position
        pageGen.sizer.Add(sb, (1,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        position.Bind(wx.EVT_SCROLL_CHANGED, self.onChanged)
        
        pageGen.sizer.Layout()
        wx.CallAfter(self.Layout)
        
        
        #
        # La page "Enoncé général du besoin"
        #
        pageBG = PanelPropriete(nb)
        bg_color = self.Parent.GetBackgroundColour()
        pageBG.SetBackgroundColour(bg_color)
        self.pageBG = pageBG
        
        nb.AddPage(pageBG, u"Origine")
        
        self.bgctrl = wx.TextCtrl(pageBG, -1, u"", style=wx.TE_MULTILINE)
        self.bgctrl.SetToolTipString(u"Partenariat, thématique, concours…")
        
        pageBG.Bind(wx.EVT_TEXT, self.EvtText, self.bgctrl)
        
        pageBG.sizer.Add(self.bgctrl, (0,0), flag = wx.EXPAND)
        pageBG.sizer.AddGrowableCol(0)
        pageBG.sizer.AddGrowableRow(0)  
        pageBG.sizer.Layout()
        
        
        #
        # La page "Contraintes Imposées"
        #
        pageCont = PanelPropriete(nb)
        bg_color = self.Parent.GetBackgroundColour()
        pageCont.SetBackgroundColour(bg_color)
        self.pageCont = pageCont
        
        nb.AddPage(pageCont, u"Contraintes imposées")
        
        self.contctrl = wx.TextCtrl(pageCont, -1, u"", style=wx.TE_MULTILINE)
        self.contctrl.SetToolTipString(constantes.TIP_CONTRAINTES)
        pageCont.Bind(wx.EVT_TEXT, self.EvtText, self.contctrl)
        
        pageCont.sizer.Add(self.contctrl, (0,0), flag = wx.EXPAND)
        pageCont.sizer.AddGrowableCol(0)
        pageCont.sizer.AddGrowableRow(0)  
        pageCont.sizer.Layout()
        
        #
        # La page "sous parties"
        #
        pagePart = PanelPropriete(nb)
        bg_color = self.Parent.GetBackgroundColour()
        pagePart.SetBackgroundColour(bg_color)
        self.pagePart = pagePart
        
        nb.AddPage(pagePart, u"Découpage du projet")
        
        self.nbrParties = Variable(u"Nombre de sous parties",  
                                   lstVal = self.projet.nbrParties, 
                                   typ = VAR_ENTIER_POS, bornes = [1,5])
        self.ctrlNbrParties = VariableCtrl(pagePart, self.nbrParties, coef = 1, signeEgal = False,
                                help = u"Nombre de sous parties", sizeh = 30)
        self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlNbrParties)
        pagePart.sizer.Add(self.ctrlNbrParties, (0,0), flag = wx.EXPAND|wx.ALL, border = 2)
        
        titreInt = wx.StaticBox(pagePart, -1, u"Intitulés des différentes parties")
        sb = wx.StaticBoxSizer(titreInt)
        
        self.intctrl = wx.TextCtrl(pagePart, -1, u"", style=wx.TE_MULTILINE)
        self.intctrl.SetToolTipString(u"Intitulés des parties du projet confiées à chaque groupe.\n" \
                                      u"Les groupes d'élèves sont désignés par des lettres (A, B, C, ...)\n" \
                                      u"et leur effectif est indiqué.")
        pagePart.Bind(wx.EVT_TEXT, self.EvtText, self.intctrl)
        sb.Add(self.intctrl, 1, flag = wx.EXPAND)
        pagePart.sizer.Add(sb, (1,0), flag = wx.EXPAND|wx.ALL, border = 2)
        
        titreInt = wx.StaticBox(pagePart, -1, u"Enoncés du besoin des différentes parties du projet")
        sb = wx.StaticBoxSizer(titreInt)
        self.enonctrl = wx.TextCtrl(pagePart, -1, u"", style=wx.TE_MULTILINE)
        self.enonctrl.SetToolTipString(u"Enoncés du besoin des parties du projet confiées à chaque groupe")
        pagePart.Bind(wx.EVT_TEXT, self.EvtText, self.enonctrl)
        sb.Add(self.enonctrl, 1, flag = wx.EXPAND)
        pagePart.sizer.Add(sb, (0,1), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)
        
        pagePart.sizer.AddGrowableCol(1)
        pagePart.sizer.AddGrowableRow(1)  
        pagePart.sizer.Layout()
        
        #
        # La page "Production attendue"
        #
        pageProd = PanelPropriete(nb)
        bg_color = self.Parent.GetBackgroundColour()
        pageProd.SetBackgroundColour(bg_color)
        self.pageProd = pageProd
        
        nb.AddPage(pageProd, u"Production finale attendue")
        
        self.prodctrl = wx.TextCtrl(pageProd, -1, u"", style=wx.TE_MULTILINE)
        self.prodctrl.SetToolTipString(constantes.TIP_PRODUCTION)
        pageProd.Bind(wx.EVT_TEXT, self.EvtText, self.prodctrl)
        
        pageProd.sizer.Add(self.prodctrl, (0,0), flag = wx.EXPAND)
        pageProd.sizer.AddGrowableCol(0)
        pageProd.sizer.AddGrowableRow(0)  
        pageProd.sizer.Layout()
        
        
        self.sizer.Add(nb, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.sizer.Layout()
        
#        self.Fit()
        
    
    #############################################################################            
    def getBitmapPeriode(self, larg):
        w, h = 0.04*5, 0.04
        imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  larg, int(h/w*larg))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        ctx = cairo.Context(imagesurface)
        ctx.scale(larg/w, larg/w) 
        draw_cairo_prj.DrawPeriodes(ctx, self.projet.position, origine = True)

        bmp = wx.lib.wxcairo.BitmapFromImageSurface(imagesurface)
        return bmp
         
    
    #############################################################################            
    def onChanged(self, evt):
        self.projet.SetPosition(evt.EventObject.GetValue())
        self.SetBitmapPosition()
        
        
        
    #############################################################################            
    def SetBitmapPosition(self, bougerSlider = None):
        self.sendEvent()
        self.bmp.SetBitmap(self.getBitmapPeriode(250))
        if bougerSlider != None:
            self.position.SetValue(bougerSlider)
        
        
    #############################################################################            
    def EvtVariable(self, event):
        var = event.GetVar()
        if var == self.nbrParties:
            self.projet.nbrParties = var.v[0]
        
        
    #############################################################################            
    def EvtText(self, event):
        if event.GetEventObject() == self.textctrl:
            nt = event.GetString()
            if nt == u"":
                nt = self.projet.support.nom
            self.projet.SetText(nt)
            self.textctrl.ChangeValue(nt)
            maj = True
            
        elif event.GetEventObject() == self.bgctrl:
            self.projet.origine = event.GetString()
            maj = False
            
        elif event.GetEventObject() == self.contctrl:
            self.projet.contraintes = event.GetString()
            maj = False
            
        elif event.GetEventObject() == self.prodctrl:
            self.projet.production = event.GetString()
            maj = False
        
        elif event.GetEventObject() == self.intctrl:
            self.projet.intituleParties = event.GetString()
            maj = False
        
        elif event.GetEventObject() == self.enonctrl:
            self.projet.besoinParties = event.GetString()
            maj = False
            
        else:
            self.projet.SetProblematique(event.GetString())
            maj = True
            
            
        if maj and not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.textctrl.ChangeValue(self.projet.intitule)
        self.commctrl.ChangeValue(self.projet.problematique)
        
        self.bgctrl.ChangeValue(self.projet.origine)
        self.contctrl.ChangeValue(self.projet.contraintes)
        self.prodctrl.ChangeValue(self.projet.production)
        self.intctrl.ChangeValue(self.projet.intituleParties)
        self.enonctrl.ChangeValue(self.projet.besoinParties)
        
        self.nbrParties.v[0] = self.projet.nbrParties
        self.ctrlNbrParties.mofifierValeursSsEvt()
        
        self.bmp.SetBitmap(self.getBitmapPeriode(250))
        self.position.SetValue(self.projet.position)
        self.Layout()
        if sendEvt:
            self.sendEvent()

    #############################################################################            
    def GetDocument(self):
        return self.projet
    
    
    
    
####################################################################################
#
#   Classe définissant le panel de propriété de la classe
#
####################################################################################
class PanelPropriete_Classe(PanelPropriete):
    def __init__(self, parent, classe, pourProjet):
        PanelPropriete.__init__(self, parent)
        
        if not pourProjet:
            #
            # La page "Généralités"
            #
            nb = wx.Notebook(self, -1,  style= wx.BK_DEFAULT)
            pageGen = PanelPropriete(nb)
            bg_color = self.Parent.GetBackgroundColour()
            pageGen.SetBackgroundColour(bg_color)
            self.pageGen = pageGen
            
            nb.AddPage(pageGen, u"Propriétés générales")
            
            self.sizer.Add(nb, (0,1), (2,1), flag = wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND, border = 1)
            
        else:
            #
            # 
            #
            pageGen = self
            self.pageGen = pageGen
        

        self.classe = classe
        self.pasVerrouille = True
#        print "PanelPropriete_Classe", classe.typeEnseignement
        

        #
        # La barre d'outils
        #
        tb = wx.ToolBar(self, style = wx.TB_VERTICAL|wx.TB_FLAT|wx.TB_NODIVIDER)
        self.sizer.Add(tb, (0,0), (2,1), flag = wx.ALL|wx.ALIGN_RIGHT, border = 1)
        tb.AddSimpleTool(30, images.Icone_valid_pref.GetBitmap(),
                         u"Choisir ces paramètres de classe pour les futurs documents")
        self.Bind(wx.EVT_TOOL, self.OnValidPref, id=30)
        tb.AddSimpleTool(31, images.Icone_defaut_pref.GetBitmap(), 
                         u"Rétablir les paramètres de classe par défaut")
        self.Bind(wx.EVT_TOOL, self.OnDefautPref, id=31)
        if not pourProjet:
            tb.AddSimpleTool(32, images.Icone_excel.GetBitmap(), 
                             u"Sélectionner les CI depuis un fichier Excel",
                             u"Sélectionner les CI ETT depuis un fichier Excel (.xls)")
            self.Bind(wx.EVT_TOOL, self.SelectCI, id=32)
            
            tb.AddSimpleTool(33, images.Bouton_Aide.GetBitmap(), 
                             u"Informations à propos de la cible CI",
                             u"Informations à propos de la cible CI")
            self.Bind(wx.EVT_TOOL, self.OnAide, id=33)
        
        
        self.tb = tb
        tb.Realize()
        
        
        
        #
        # Type d'enseignement
        #
        l = []
        for i, e in enumerate(constantes.listEnseigmenent):
            l.append(constantes.Enseigmenent[e][0])
        rb = wx.RadioBox(
                pageGen, -1, u"Type d'enseignement", wx.DefaultPosition, (130,-1),
                l,
                1, wx.RA_SPECIFY_COLS
                )
        rb.SetToolTip(wx.ToolTip(u"Choisir le type d'enseignement"))
        for i, e in enumerate(constantes.listEnseigmenent):
            rb.SetItemToolTip(i, constantes.Enseigmenent[e][1])
        pageGen.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
        if pourProjet:
            rb.ShowItem(0, False) 
        rb.SetStringSelection(constantes.Enseigmenent[self.classe.typeEnseignement][0])
            
        pageGen.sizer.Add(rb, (0,1), flag = wx.EXPAND|wx.ALL, border = 2)#
        self.cb_type = rb
        
        
        
        #
        # Etablissement
        #
        titre = wx.StaticBox(pageGen, -1, u"Etablissement")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        
        self.cb = wx.ComboBox(pageGen, -1, "sélectionner un établissement ...", (-1,-1), 
                         (-1, -1), constantes.ETABLISSEMENTS_PDD + [u"autre ..."],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.cb)
        sb.Add(self.cb, flag = wx.EXPAND)
        
        textctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
        pageGen.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
#        textctrl.SetMinSize((-1, 150))
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        
        pageGen.sizer.Add(sb, (0,2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, border = 2)
        
        
        
        #
        # Effectifs
        #
        self.ec = PanelEffectifsClasse(pageGen, classe)
        pageGen.sizer.Add(self.ec, (0,3), flag = wx.ALL|wx.EXPAND, border = 2)#|wx.ALIGN_RIGHT
        

        pageGen.sizer.AddGrowableRow(0)
        pageGen.sizer.AddGrowableCol(2)
        pageGen.sizer.Layout()
        
        #
        # Centres d'intérêt
        #
        if not pourProjet:
            pageCI= wx.Panel(nb, -1)
            sizer = wx.BoxSizer()
#            bg_color = self.Parent.GetBackgroundColour()
#            pageCI.SetBackgroundColour(bg_color)
            self.pageCI = pageCI
            nb.AddPage(pageCI, u"Centres d'intérêt")
            
            sb1 = wx.StaticBox(pageCI, -1, u"Centres d'intérêt ETT", size = (200,-1))
            sbs1 = wx.StaticBoxSizer(sb1, wx.VERTICAL)
            self.sb1 = sb1
            listCI = ULC.UltimateListCtrl(pageCI, -1, 
                                        agwStyle=wx.LC_REPORT
                                             #| wx.BORDER_SUNKEN
                                             | wx.BORDER_NONE
                                             #| wx.ULC_EDIT_LABELS
                                             #| wx.LC_SORT_ASCENDING
                                             #| wx.LC_NO_HEADER
                                             | wx.LC_VRULES
                                             | wx.LC_HRULES
                                             #| wx.LC_SINGLE_SEL
                                             | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
            
            info = ULC.UltimateListItem()
            info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT
            info._format = wx.LIST_FORMAT_LEFT
            info._text = u"CI"
             
            listCI.InsertColumnInfo(0, info)
    
            info = ULC.UltimateListItem()
            info._format = wx.LIST_FORMAT_LEFT
            info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_FONT
            info._text = u"Intitulé"
            
            listCI.InsertColumnInfo(1, info)
            
            listCI.SetColumnWidth(0, 35)
            listCI.SetColumnWidth(1, -3)
            
            for i,p in enumerate(['M', 'E', 'I', 'F', 'S', 'C']):
                info = ULC.UltimateListItem()
                info._mask = wx.LIST_MASK_TEXT
                info._format = wx.LIST_FORMAT_CENTER
                info._text = p
                
                listCI.InsertColumnInfo(i+2, info)
                listCI.SetColumnWidth(i+2, 20)
            
            self.list = listCI
            self.PeuplerListe()
            
            self.list.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
            self.list.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            self.leftDown = False
            sbs1.Add(listCI, 1, flag = wx.EXPAND)

            if self.classe.typeEnseignement != 'ET' :
                self.list.Enable(False)
                
            sizer.Add(sbs1, 1, flag = wx.EXPAND|wx.ALL, border = 2)
            
            self.sizer.AddGrowableRow(0)
            self.sizer.AddGrowableCol(1)
            
            pageCI.SetSizer(sizer)
            sizer.Layout()
            self.Layout()
        
        self.MiseAJourType()
    
    #############################################################################            
    def OnDefautPref(self, evt):
        self.classe.options.defaut()
        self.classe.Initialise(isinstance(self.classe.doc, Projet))
        self.MiseAJour()
        
        
    #############################################################################            
    def OnValidPref(self, evt):
        try:
            self.classe.options.valider(self.classe)
            self.classe.options.enregistrer()
        except IOError:
            messageErreur(self, u"Permission refusée",
                          u"Permission d'enregistrer les préférences refusée.\n\n" \
                          u"Le dossier est protégé en écriture")
        except:
            messageErreur(self, u"Enregistrement impossible",
                          u"Imposible d'enregistrer les préférences\n\n")
        return   
        
        
    #############################################################################            
    def GetDocument(self):
        return self.classe.doc
    
    
    #############################################################################            
    def EvtText(self, event):
        if event.GetEventObject() == self.textctrl:
            self.classe.etablissement = event.GetString()
            self.sendEvent()
            
    ######################################################################################  
    def EvtComboBox(self, evt):
        cb = evt.GetEventObject()
#        data = cb.GetClientData(evt.GetSelection())
#        s = evt.GetString()
        
        if evt.GetSelection() == len(constantes.ETABLISSEMENTS_PDD):
            self.classe.etablissement = self.textctrl.GetStringSelection()
            self.textctrl.Show(True)
        else:
            self.classe.etablissement = evt.GetString()
            self.textctrl.Show(False)
        
        self.sendEvent()
#        self.log.WriteText('EvtComboBox: %s\nClientData: %s\n' % (evt.GetString(), data))
#
#        if evt.GetString() == 'one':
#            self.log.WriteText("You follow directions well!\n\n")        
             
    ######################################################################################  
    def EvtRadioBox(self, event):
#        print self.cb_type.GetItemLabel(event.GetInt())
        for c, e in constantes.Enseigmenent.items():
#            print "   ", c, e
            if e[0] == self.cb_type.GetItemLabel(event.GetInt()):
                self.classe.typeEnseignement = c
                self.classe.familleEnseignement = constantes.FamilleEnseignement[self.classe.typeEnseignement]
                break
#        self.classe.typeEnseignement = self.cb_type.GetItemLabel(event.GetInt())
            
        self.MiseAJourType()
        
        self.classe.codeBranche.SetLabel(self.classe.typeEnseignement)
        self.classe.doc.MiseAJourTypeEnseignement()
        self.sendEvent()
        
        
    ######################################################################################  
    def EvtCheckBox(self, event):
        cb = event.GetEventObject()
        numCI = cb.GetId()-100
        posCI = cb.GetName()
        
        i = 'MEI_FSC'.index(posCI)

        s = self.classe.posCI_ET[numCI] 
        if not event.IsChecked():
            t = " "
        else:
            t = posCI
        s = s[:i]+t+s[i+1:]    

        self.classe.posCI_ET[numCI] = s

        self.classe.doc.CI.panelPropriete.construire()
        self.sendEvent()
        
    
    
    ######################################################################################  
    def MiseAJourType(self):
        """ Modification de la barre d'outil
            en fonction du type d'enseignement
        """
        if hasattr(self, 'list'):
            if self.classe.familleEnseignement == 'STI':
                self.list.Show(True)
#                self.tb.Show(True)
                self.sb1.Show(True)
                enable = self.pasVerrouille and (self.classe.typeEnseignement == 'ET')
                self.list.Enable(enable)
                self.tb.EnableTool(31, enable)
                self.tb.EnableTool(32, enable)
                self.tb.EnableTool(33, enable)
            else:
                self.list.Show(False)
#                self.tb.Show(False)
                self.sb1.Show(False)
                self.tb.EnableTool(32, False)   
                self.tb.EnableTool(33, False)  
#            self.btn.Enable(self.pasVerrouille and self.classe.typeEnseignement == 'ET')
        
            self.pageCI.Layout()
            
        self.Layout()
        self.sizer.Layout()
        self.Refresh()
         
        
    ######################################################################################  
    def MiseAJour(self):
        self.MiseAJourType()
        self.cb_type.SetStringSelection(constantes.Enseigmenent[self.classe.typeEnseignement][0])
        
        self.cb.SetValue(self.classe.etablissement)
        print self.cb.GetStringSelection ()
        if self.cb.GetStringSelection () and self.cb.GetStringSelection() == self.classe.etablissement:
            self.textctrl.ChangeValue(u"")
            self.textctrl.Show(False)
            
        else:
            self.textctrl.ChangeValue(self.classe.etablissement)
            self.textctrl.Show(True)
            self.cb.SetSelection(len(constantes.ETABLISSEMENTS_PDD))
        
        if hasattr(self, 'list'):
            self.PeuplerListe()
                
        self.ec.MiseAJour()

    ######################################################################################  
    def PeuplerListe(self):
#        print "PeuplerListe"
        # Peuplement de la liste
        self.list.DeleteAllItems()
        for i,ci in enumerate(self.classe.ci_ET):
            index = self.list.InsertStringItem(sys.maxint, "CI"+str(i+1))
            self.list.SetStringItem(index, 1, ci)
           
            for j,p in enumerate(['M', 'E', 'I', 'F', 'S', 'C']):
                item = self.list.GetItem(i, j+2)
                
                cb = wx.CheckBox(self.list, 100+i, u"", name = p)
                cb.SetValue(p in self.classe.posCI_ET[i])
                self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
                item.SetWindow(cb)
#                item.Enable(False)
                self.list.SetItem(item)
        self.list.Update()
        
    ######################################################################################  
    def OnLeftDown(self, event):
        x = event.GetX()
        y = event.GetY()

        item, flags = self.list.HitTest((x, y))

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            if not self.list.IsSelected(item):
                self.leftDown = True
            else:
                self.leftDown = False
                
        event.Skip()
            
    #############################################################################            
    def OnAide(self, event):
        dlg = MessageAideCI(self)
        dlg.ShowModal()
        dlg.Destroy()
            
    ######################################################################################  
    def OnLeftUp(self, event):
        x = event.GetX()
        y = event.GetY()

        item, flags = self.list.HitTest((x, y))

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            if self.list.IsSelected(item) and not self.leftDown:
                x0, y0 = self.list.GetScreenPosition()
                x, y, w, h = self.list.GetItemRect(item, ULC.ULC_RECT_BOUNDS)#ULC.ULC_RECT_LABEL)#
                
                ed = Editeur(self.classe, self.list, item, self.list.GetItem(item, 1).GetText(),
                             pos = (x0+x+self.list.GetColumnWidth(0), y0+y), 
                             size = (self.list.GetColumnWidth(1), -1))
                ed.Show()

        event.Skip()
        

    ######################################################################################  
    def SelectCI(self, event = None):
        if recup_excel.ouvrirFichierExcel():
            dlg = wx.MessageDialog(self.Parent,  u"Sélectionner une liste de CI\n" \
                                                 u"dans le classeur Excel qui vient de s'ouvrir,\n" \
                                                 u'puis appuyer sur "Oui".\n\n' \
                                                 u"Format attendu de la selection :\n" \
                                                 u"Liste des CI sur une colonne.",
                                                 u'Sélection de CI',
                                                 wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                                 )
            res = dlg.ShowModal()
            dlg.Destroy() 
            if res == wx.ID_YES:
                ls = recup_excel.getColonne(c = 0)
#                ci = getTextCI(ls)
#                self.txtCi.ChangeValue(ci)
                if ls != None:
                    self.classe.ci_ET = list(ls)
                    self.classe.posCI_ET = ['   _   ']*len(ls)
                    self.MiseAJour()
                    self.GetDocument().CI.MiseAJourTypeEnseignement()
                    self.sendEvent()
            elif res == wx.ID_NO:
                print "Rien" 
        
    ######################################################################################  
    def Verrouiller(self, etat):
        self.cb_type.Enable(etat)
        if hasattr(self, 'list'):
            enable = etat and (self.classe.typeEnseignement == 'ET')
            self.list.Enable(enable)
            self.tb.EnableTool(31, enable)
            self.tb.EnableTool(32, enable)
        self.pasVerrouille = etat





class Editeur(wx.Frame):  
    def __init__(self, classe, liste, index, texte, pos, size):
        wx.Frame.__init__(self, None, -1, pos = pos, 
                          size = size, style = wx.BORDER_NONE)
        self.index = index
        self.liste = liste
        self.classe = classe
        txt = wx.TextCtrl(self, -1, texte, size = size)
        txt.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
#        self.Bind(wx.EVT_TEXT_ENTER, self.OnKillFocus, txt)
        self.Fit()
        
    def OnKillFocus(self, evt):
        txtctrl = evt.GetEventObject()
        self.liste.SetStringItem(self.index, 1, txtctrl.GetValue())
        self.classe.ci_ET[self.index] = txtctrl.GetValue()
#        self.classe.doc.CI.
        self.classe.doc.CI.panelPropriete.construire()
        self.Destroy() 
        evt.Skip()
        return
    
        
        
####################################################################################
#
#   Classe définissant le panel de réglage des effectifs
#
####################################################################################     
class PanelEffectifsClasse(wx.Panel):
    """ Classe définissant le panel de réglage des effectifs
    
        Rappel :
        listeEffectifs = ["C", "G", "D" ,"E" ,"P"]
        NbrGroupes = {"G" : 2, # Par classe
                      "E" : 2, # Par grp Eff réduit
                      "P" : 4, # Par grp Eff réduit
                      }
                      
    """
    def __init__(self, parent, classe):
        wx.Panel.__init__(self, parent, -1)
        self.classe = classe
        
        #
        # Box "Classe"
        #
        boxClasse = wx.StaticBox(self, -1, u"Découpage de la classe", style = wx.BORDER_RAISED)

        coulClasse = constantes.GetCouleurWx(constantes.CouleursGroupes['C'])
        boxClasse.SetOwnForegroundColour(coulClasse)
        
        self.coulEffRed = constantes.GetCouleurWx(constantes.CouleursGroupes['G'])

        self.coulEP = constantes.GetCouleurWx(constantes.CouleursGroupes['E'])
    
        self.coulAP = constantes.GetCouleurWx(constantes.CouleursGroupes['P'])
        
#        self.boxClasse = boxClasse
        bsizerClasse = wx.StaticBoxSizer(boxClasse, wx.VERTICAL)
        sizerClasse_h = wx.BoxSizer(wx.HORIZONTAL)
        sizerClasse_b = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerClasse_b = sizerClasse_b
        bsizerClasse.Add(sizerClasse_h)
        bsizerClasse.Add(sizerClasse_b)
        
        # Effectif de la classe
        self.vEffClas = Variable(u"Nombre d'élèves",  
                            lstVal = classe.effectifs['C'], 
                            typ = VAR_ENTIER_POS, bornes = [4,40])
        self.cEffClas = VariableCtrl(self, self.vEffClas, coef = 1, signeEgal = False,
                                help = u"Nombre d'élèves dans la classe entière", sizeh = 30, color = coulClasse)
        self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cEffClas)
        sizerClasse_h.Add(self.cEffClas, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 5)
        
        # Nombre de groupes à effectif réduits
        self.vNbERed = Variable(u"Nbr de groupes\nà effectif réduit",  
                                lstVal = classe.nbrGroupes['G'], 
                                typ = VAR_ENTIER_POS, bornes = [1,4])
        self.cNbERed = VariableCtrl(self, self.vNbERed, coef = 1, signeEgal = False,
                                    help = u"Nombre de groupes à effectif réduit dans la classe", sizeh = 20, color = self.coulEffRed)
        self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cNbERed)
        sizerClasse_h.Add(self.cNbERed, 0, wx.TOP|wx.LEFT, 5)
        
        
        #
        # Boxes Effectif Réduit
        #
        boxEffRed = wx.StaticBox(self, -1, u"")
        boxEffRed.SetOwnForegroundColour(self.coulEffRed)
        self.boxEffRed = boxEffRed
        bsizerEffRed = wx.StaticBoxSizer(boxEffRed, wx.HORIZONTAL)
        self.sizerEffRed_g = wx.BoxSizer(wx.VERTICAL)
        self.sizerEffRed_d = wx.BoxSizer(wx.VERTICAL)
        bsizerEffRed.Add(self.sizerEffRed_g, flag = wx.EXPAND)
        bsizerEffRed.Add(wx.StaticLine(self, -1, style = wx.VERTICAL), flag = wx.EXPAND)
        bsizerEffRed.Add(self.sizerEffRed_d, flag = wx.EXPAND)
        sizerClasse_b.Add(bsizerEffRed)
        
        # Nombre de groupes d'étude/projet
        self.vNbEtPr = Variable(u"Nbr de groupes\n\"Etudes et Projets\"",  
                            lstVal = classe.nbrGroupes['E'], 
                            typ = VAR_ENTIER_POS, bornes = [1,10])
        self.cNbEtPr = VariableCtrl(self, self.vNbEtPr, coef = 1, signeEgal = False,
                                help = u"Nombre de groupes d'étude/projet par groupe à effectif réduit", sizeh = 20, color = self.coulEP)
        self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cNbEtPr)
        self.sizerEffRed_g.Add(self.cNbEtPr, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 3)
        
#        self.BoxEP = wx.StaticBox(self, -1, u"", size = (30, -1))
#        self.BoxEP.SetOwnForegroundColour(self.coulEP)
#        self.BoxEP.SetMinSize((30, -1))     
#        bsizer = wx.StaticBoxSizer(self.BoxEP, wx.VERTICAL)
#        self.sizerEffRed_g.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
            
        # Nombre de groupes d'activité pratique
        self.vNbActP = Variable(u"Nbr de groupes\n\"Activités pratiques\"",  
                            lstVal = classe.nbrGroupes['P'], 
                            typ = VAR_ENTIER_POS, bornes = [2,20])
        self.cNbActP = VariableCtrl(self, self.vNbActP, coef = 1, signeEgal = False,
                                help = u"Nombre de groupes d'activité pratique par groupe à effectif réduit", sizeh = 20, color = self.coulAP)
        self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cNbActP)
        self.sizerEffRed_d.Add(self.cNbActP, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 3)
        
#        self.BoxAP = wx.StaticBox(self, -1, u"", size = (30, -1))
#        self.BoxAP.SetOwnForegroundColour(self.coulAP)
#        self.BoxAP.SetMinSize((30, -1))     
#        bsizer = wx.StaticBoxSizer(self.BoxAP, wx.VERTICAL)
#        self.sizerEffRed_d.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
        
        
        self.lstBoxEffRed = []
        self.lstBoxEP = []
        self.lstBoxAP = []
        
#        self.AjouterGroupesVides()
        
        self.MiseAJourNbrEleve()

        border = wx.BoxSizer()
        border.Add(bsizerClasse, 1, wx.EXPAND)
        self.SetSizer(border)

    
    
    def EvtVariableEff(self, event):
        var = event.GetVar()
        if var == self.vEffClas:
            self.classe.effectifs['C'] = var.v[0]
        elif var == self.vNbERed:
            self.classe.nbrGroupes['G'] = var.v[0]
        elif var == self.vNbEtPr:
            self.classe.nbrGroupes['E'] = var.v[0]
        elif var == self.vNbActP:
            self.classe.nbrGroupes['P'] = var.v[0]
        calculerEffectifs(self.classe)
            
        self.Parent.sendEvent()
#        self.AjouterGroupesVides()
        self.MiseAJourNbrEleve()
        
#    def AjouterGroupesVides(self):
#        return
#        for g in self.lstBoxEP:
#            self.sizerEffRed_g.Remove(g)
#        for g in self.lstBoxAP:
#            self.sizerEffRed_d.Remove(g)    
#        for g in self.lstBoxEffRed:
#            self.sizerClasse_b.Remove(g)
#        
#        self.lstBoxEffRed = []
#        self.lstBoxEP = []
#        self.lstBoxAP = []    
#        
#        for g in range(self.classe.nbrGroupes['G'] - 1):
#            box = wx.StaticBox(self, -1, u"Eff Red", size = (30, -1))
#            box.SetOwnForegroundColour(self.coulEffRed)
#            box.SetMinSize((30, -1))
#            self.lstBoxEffRed.append(box)
#            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
#            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
#            self.sizerClasse_b.Add(bsizer, flag = wx.EXPAND)
#        
#        for g in range(self.classe.nbrGroupes['E']):
#            box = wx.StaticBox(self, -1, u"E/P", size = (30, -1))
#            box.SetOwnForegroundColour(self.coulEP)
#            box.SetMinSize((30, -1))
#            self.lstBoxEP.append(box)
#            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
##            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
#            self.sizerEffRed_g.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
#            
#        
#        for g in range(self.classe.nbrGroupes['P']):
#            box = wx.StaticBox(self, -1, u"AP", size = (30, -1))
#            box.SetOwnForegroundColour(self.coulAP)
#            box.SetMinSize((30, -1))
#            self.lstBoxAP.append(box)
#            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
##            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
#            self.sizerEffRed_d.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
#        
#        self.Layout()
        
    
    def MiseAJourNbrEleve(self):
        self.boxEffRed.SetLabelText(strEffectifComplet(self.classe, 'G', -1))
#        t = u"groupes de "
#        self.BoxEP.SetLabelText(t+strEffectif(self.classe, 'E', -1))
#        self.BoxAP.SetLabelText(t+strEffectif(self.classe, 'P', -1))

#        self.Refresh()
        
        
    def MiseAJour(self):
        self.vEffClas.v[0] = self.classe.effectifs['C']
        self.vNbERed.v[0] = self.classe.nbrGroupes['G']
        self.vNbEtPr.v[0] = self.classe.nbrGroupes['E']
        self.vNbActP.v[0] = self.classe.nbrGroupes['P']
        
        self.cEffClas.mofifierValeursSsEvt()
        self.cNbERed.mofifierValeursSsEvt()
        self.cNbEtPr.mofifierValeursSsEvt()
        self.cNbActP.mofifierValeursSsEvt()
        
#        self.AjouterGroupesVides()
        self.MiseAJourNbrEleve()
        

        
        
####################################################################################
#
#   Classe définissant le panel de propriété du CI
#
####################################################################################
class PanelPropriete_CI(PanelPropriete):
    def __init__(self, parent, CI):
        PanelPropriete.__init__(self, parent)
        self.CI = CI       
        self.construire()
        

    #############################################################################            
    def GetDocument(self):
        return self.CI.parent
    
    ######################################################################################################
    def OnEnter(self, event):
        return
        
    #############################################################################            
    def construire(self):
        self.group_ctrls = []
        self.DestroyChildren()
        if hasattr(self, 'grid1'):
            self.sizer.Remove(self.grid1)
            
        if self.CI.GetTypeEnseignement() == 'ET': # Rajouter la condition "Clermont" !!!
            
            self.panel_cible = Panel_Cible(self, self.CI)
            self.sizer.Add(self.panel_cible, (0,0), (2,1), flag = wx.EXPAND)
            
            self.grid1 = wx.FlexGridSizer( 0, 2, 0, 0 )
            
#            for i, ci in enumerate(constantes.CentresInterets[self.CI.GetTypeEnseignement()]):
            for i, ci in enumerate(self.CI.parent.classe.ci_ET):
                r = wx.CheckBox(self, 200+i, "")
                t = wx.StaticText(self, -1, "CI"+str(i+1)+" : "+ci)
                self.group_ctrls.append((r, t))
                self.grid1.Add( r, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
                self.grid1.Add( t, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5 )
            for radio, text in self.group_ctrls:
                self.Bind(wx.EVT_CHECKBOX, self.OnCheck, radio )
            self.sizer.Add(self.grid1, (0,1), (2,1), flag = wx.EXPAND)
            
            aide = wx.BitmapButton(self, -1, images.Bouton_Aide.GetBitmap())
            aide.SetToolTipString(u"Informations à propos de la cible CI")
            self.sizer.Add(aide, (0,2), flag = wx.ALL, border = 2)
            self.Bind(wx.EVT_BUTTON, self.OnAide, aide )
            
            b = wx.ToggleButton(self, -1, "")
            b.SetValue(self.CI.max2CI)
            b.SetBitmap(images.Bouton_2CI.GetBitmap())
            b.SetToolTipString(u"Limite à 2 le nombre de CI sélectionnables")
            self.sizer.Add(b, (1,2), flag = wx.ALL, border = 2)
#            b.SetSize((30,30)) # adjust default size for the bitmap
            b.SetInitialSize((32,32))
            self.b2CI = b
            self.Bind(wx.EVT_TOGGLEBUTTON, self.OnOption, b)
            if not self.sizer.IsColGrowable(1):
                self.sizer.AddGrowableCol(1)
            self.sizer.Layout()
            
        else:
            
            self.grid1 = wx.FlexGridSizer( 0, 2, 0, 0 )
            
            for i, ci in enumerate(constantes.CentresInterets[self.CI.GetTypeEnseignement()]):
    #            if i == 0 : s = wx.RB_GROUP
    #            else: s = 0
                r = wx.CheckBox(self, 200+i, "CI"+str(i+1), style = wx.RB_GROUP )
                t = wx.StaticText(self, -1, ci)
                self.grid1.Add( r, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
                self.grid1.Add( t, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5 )
                self.group_ctrls.append((r, t))
            self.sizer.Add(self.grid1, (0,0), flag = wx.EXPAND)
            for radio, text in self.group_ctrls:
                self.Bind(wx.EVT_CHECKBOX, self.OnCheck, radio )
#            btn = wx.Button(self, -1, u"Effacer")
#            self.Bind(wx.EVT_BUTTON, self.OnClick, btn)
#            self.sizer.Add(btn, (0,1))
            
            self.sizer.Layout()
        
    #############################################################################            
    def OnAide(self, event):
        dlg = MessageAideCI(self)
        dlg.ShowModal()
        dlg.Destroy()

    #############################################################################            
    def OnOption(self, event):
        self.CI.max2CI = not self.CI.max2CI
        self.MiseAJour()
        
    #############################################################################            
    def OnCheck(self, event):
        button_selected = event.GetEventObject().GetId()-200 
        
        if event.GetEventObject().IsChecked():
            self.CI.AddNum(button_selected)
        else:
            self.CI.DelNum(button_selected)
        
#        self.panel_cible.bouton[button_selected].SetState(event.GetEventObject().IsChecked())
        if self.CI.GetTypeEnseignement() == 'ET':
            self.panel_cible.GererBoutons(True)
        
        if hasattr(self, 'b2CI'):
            if len(self.CI.numCI) > 2:
                self.b2CI.Enable(False)
            else:
                self.b2CI.Enable(True)
            
        self.Layout()
        self.sendEvent()
    
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        if self.CI.GetTypeEnseignement() == 'ET':
            self.panel_cible.GererBoutons(True)
        else:
            for num in self.CI.numCI:
                self.group_ctrls[num][0].SetValue(True)
            self.Layout()
        
        if hasattr(self, 'b2CI'):
            if len(self.CI.numCI) > 2:
                self.b2CI.Enable(False)
            else:
                self.b2CI.Enable(True)
            
        if sendEvt:
            self.sendEvent()
            
    #############################################################################            
    def OnClick(self, event):
        if self.CI.num != None:
            self.group_ctrls[self.CI.num][0].SetValue(False)
            self.CI.SetNum(None)
            self.sendEvent()

    #############################################################################            
    def GererCases(self, liste, appuyer = False):
        """ Permet de cacher les cases des CI au fur et à mesure que l'on selectionne des CI
            <liste> : liste des CI à activer
        """ 
        for i, b in enumerate(self.group_ctrls):
            if i in liste:
                b[0].Enable(True)
            else:
                b[0].Enable(False)
                
        if appuyer:
            for i, b in enumerate(self.group_ctrls):
                b[0].SetValue(i in self.CI.numCI)
                
                    

####################################################################################
#
#   Classe définissant le panel conteneur de la Cible MEI
#
#################################################################################### 
class Panel_Cible(wx.Panel):
    def __init__(self, parent, CI):
        wx.Panel.__init__(self, parent, -1)
        self.CI = CI
        self.bouton = []
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.backGround = self.GetBackgroundColour()
        
#        rayons = [90,90,60,40,20,30,60,40,20,30,60,40,20,30,0]
#        angles = [-100,100,0,0,0,60,120,120,120,180,-120,-120,-120,-60,0]
        centre = [96, 88]
        
        rayons = {"F" : 60, 
                  "S" : 40, 
                  "C" : 20,
                  "_" : 90}
        angles = {"M" : 0,
                  "E" : 120,
                  "I" : -120,
                  "_" : -100}
        

        for i, ci in enumerate(self.CI.parent.classe.ci_ET):
            #print self.CI.parent.classe.posCI_ET[i]
            mei, fsc = self.CI.parent.classe.posCI_ET[i].split("_")
#            constantes.PositionCibleCIET[i].split("_")
            mei = mei.replace(" ", "")
            fsc = fsc.replace(" ", "")
            
            if len(fsc) == 0:
                ray = 0
            else:
                ray = 0
                for j in fsc:
                    ray += rayons[j]
                ray = ray/len(fsc)
            
            if len(mei) == 0:
                ray = rayons["_"]
                ang = angles["_"]
                angles["_"] = -angles["_"] # on inverse le coté pour pouvoir mettre 2 CI en orbite
            elif len(mei) == 3:
                ray = 0
                ang = 0
            elif len(mei) == 2:
                ang = (angles[mei[1]] + angles[mei[0]])/2
                if ang == 0:
                    ang = 180
                
            else:
                ang = angles[mei[0]]
                    
            pos = (centre[0] + ray * sin(ang*pi/180) ,
                   centre[1] - ray * cos(ang*pi/180))
            bmp = constantes.imagesCI[i].GetBitmap()
#                bmp.SetMaskColour(self.backGround)
#                mask = wx.Mask(bmp, self.backGround)
#                bmp.SetMask(mask)
#                bmp.SetMaskColour(wx.NullColour)
#                r = CustomCheckBox(self, 100+i, pos = pos, style = wx.NO_BORDER)
            r = platebtn.PlateButton(self, 100+i, "", bmp, pos = pos, 
                                     style=platebtn.PB_STYLE_GRADIENT|platebtn.PB_STYLE_TOGGLE|platebtn.PB_STYLE_NOBG)#platebtn.PB_STYLE_DEFAULT|
            r.SetPressColor(wx.Colour(245, 55, 245))
            self.bouton.append(r)
#                r = buttons.GenBitmapToggleButton(self, 100+i, bmp, pos = pos, style=wx.BORDER_NONE)
#                r.SetBackgroundColour(wx.NullColour)
#                self.group_ctrls.append((r, 0))
#                self.Bind(wx.EVT_CHECKBOX, self.EvtCheck, r )
        
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButton)
        bmp = images.Cible.GetBitmap()
        self.SetSize((bmp.GetWidth(), bmp.GetHeight()))
        self.SetMinSize((bmp.GetWidth(), bmp.GetHeight()))
        
    ######################################################################################################
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush(self.backGround))
        dc.Clear()
        bmp = images.Cible.GetBitmap()
        dc.DrawBitmap(bmp, 0, 0)
        
        evt.Skip()
        
        
    ######################################################################################################
    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()
 
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.SetBackgroundMode(wx.TRANSPARENT)
#        color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND)
        dc.SetBackground(wx.Brush(self.backGround))
        dc.Clear()
        bmp = constantes.images.Cible.GetBitmap()
        dc.DrawBitmap(bmp, 0, 0)    
    
    
    #############################################################################            
    def OnButton(self, event):
        button_selected = event.GetEventObject().GetId()-100
        
        if event.GetEventObject().IsPressed():
            self.CI.AddNum(button_selected)
        else:
            try: # sinon problème avec les doubles clics
                self.CI.DelNum(button_selected)
            except:
                pass

        self.GererBoutons()
        
        self.Layout()
        self.Parent.group_ctrls[button_selected][0].SetValue(event.GetEventObject().IsPressed())
        self.Parent.sendEvent()    
        
        
    #############################################################################            
    def GererBoutons(self, appuyer = False):
        """ Permet de cacher les boutons des CI au fur et à mesure que l'on selectionne des CI
            Règles :
             - Maximum 2 CI
             - CI voisins sur la cible
            <appuyer> : pour initialisation : si vrai = appuie sur les boutons
        """
#        print "GererBoutons"
        if len(self.CI.numCI) == 0 or not self.CI.max2CI:
            l = range(len(self.CI.parent.classe.ci_ET))
            
        elif len(self.CI.numCI) == 1:
            l = []
            for i,p in enumerate(self.CI.parent.classe.posCI_ET):
                p = p[:3].strip()
                c = self.CI.GetPosCible(0)[:3].strip()

                if len(p) == 0 or len(c) == 0: # Cas des CI "en orbite"
                    l.append(i)
                else:       # Autres cas
                    for d in c:
                        if d in p:  
                            l.append(i)
                            break

        else:
            l = self.CI.numCI
            
#        print l
                
        for i, b in enumerate(self.bouton):
            if i in l:
                b.Show(True)
            else:
                b.Show(False)
                
        if appuyer:
            for i, b in enumerate(self.bouton):
                if i in self.CI.numCI:
                    b._SetState(platebtn.PLATE_PRESSED)
                else:
                    b._SetState(platebtn.PLATE_NORMAL)
                b._pressed = i in self.CI.numCI
                
        self.Parent.GererCases(l, True)    
                    
                    
####################################################################################
#
#   Classe définissant le panel de propriété d'un lien vers une séquence
#
####################################################################################
class PanelPropriete_LienSequence(PanelPropriete):
    def __init__(self, parent, lien):
        PanelPropriete.__init__(self, parent)
        self.lien = lien
        self.sequence = None
        self.classe = None
        self.construire()
        self.parent = parent
        
    #############################################################################            
    def GetDocument(self):
        return self.lien.parent
        
    #############################################################################            
    def construire(self):
        #
        # Sélection du ficier de séquence
        #
        sb0 = wx.StaticBox(self, -1, u"Fichier de la séquence", size = (200,-1))
        sbs0 = wx.StaticBoxSizer(sb0,wx.HORIZONTAL)
        self.texte = wx.TextCtrl(self, -1, self.lien.path, size = (300, -1),
                                 style = wx.TE_PROCESS_ENTER)
        bt2 =wx.BitmapButton(self, 101, wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE))
        bt2.SetToolTipString(u"Sélectionner un fichier")
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnText, self.texte)
        self.texte.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocus)
        sbs0.Add(self.texte)#, flag = wx.EXPAND)
        sbs0.Add(bt2)
        
        #
        # Aperçu de la séquence
        #
        sb1 = wx.StaticBox(self, -1, u"Aperçu de la séquence", size = (210,297))
        sbs1 = wx.StaticBoxSizer(sb1,wx.HORIZONTAL)
        sbs1.SetMinSize((210,297))
        self.apercu = wx.StaticBitmap(self, -1, wx.NullBitmap)
        sbs1.Add(self.apercu, 1)
        
        self.sizer.Add(sbs0, (0,0), flag = wx.EXPAND)
        self.sizer.Add(sbs1, (0,1), (2,1))#, flag = wx.EXPAND)
        
        self.sizer.Layout()
        
    #############################################################################            
    def OnClick(self, event):
        mesFormats = u"Séquence (.seq)|*.seq|" \
                       u"Tous les fichiers|*.*'"
                       
        dlg = wx.FileDialog(self, u"Sélectionner un fichier séquence",
                            defaultFile = "",
                            wildcard = mesFormats,
#                           defaultPath = globdef.DOSSIER_EXEMPLES,
                            style = wx.DD_DEFAULT_STYLE
                            #| wx.DD_DIR_MUST_EXIST
                            #| wx.DD_CHANGE_DIR
                            )

        if dlg.ShowModal() == wx.ID_OK:
            self.lien.path = testRel(dlg.GetPath(), 
                                     self.GetDocument().GetPath())
            self.MiseAJour(sendEvt = True)
        dlg.Destroy()
        
        self.SetFocus()
        
        
    #############################################################################            
    def OnText(self, event):
        self.lien.path = event.GetString()
        self.MiseAJour()
        event.Skip()     
                            
    def OnLoseFocus(self, event):  
        self.lien.path = self.texte.GetValue()
        self.MiseAJour()
        event.Skip()   
                   
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.texte.SetValue(self.lien.path)

#        try:
        if os.path.isfile(self.lien.path):
            fichier = open(self.lien.path,'r')
        else:
            abspath = os.path.join(self.GetDocument().GetPath(), self.lien.path)
            if os.path.isfile(abspath):
                fichier = open(abspath,'r')
            else:
                self.texte.SetBackgroundColour("pink")
                self.texte.SetToolTipString(u"Le fichier Séquence est introuvable !")
                return False
        self.texte.SetBackgroundColour("white")
        self.texte.SetToolTipString(u"Lien vers un fichier Séquence")
#        except:
#            dlg = wx.MessageDialog(self, u"Le fichier %s\nn'a pas pu être trouvé !" %self.lien.path,
#                               u"Erreur d'ouverture du fichier",
#                               wx.OK | wx.ICON_WARNING
#                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
#                               )
#            dlg.ShowModal()
#            dlg.Destroy()
#            self.texte.SetBackgroundColour("pink")
#            self.texte.SetToolTipString(u"Le lien vers le fichier Séquence est rompu !")
#            return False
        
        classe = Classe(self.lien.parent.app.parent)
        self.sequence = Sequence(self.lien.parent.app, classe)
        classe.SetDocument(self.sequence)
        
#        try:
        root = ET.parse(fichier).getroot()
        
        # La séquence
        sequence = root.find("Sequence")
        if sequence == None:
            self.sequence.setBranche(root)
        else:
            self.sequence.setBranche(sequence)
        
            # La classe
            classe = root.find("Classe")
            self.sequence.classe.setBranche(classe)
            self.sequence.SetCodes()
            self.sequence.SetLiens()
            self.sequence.VerifPb()
            
        fichier.close()
        
#        except:
#            self.sequence = None
##            dlg = wx.MessageDialog(self, u"Le fichier %s\nn'a pas pu être ouvert !" %self.lien.path,
##                               u"Erreur d'ouverture du fichier",
##                               wx.OK | wx.ICON_WARNING
##                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
##                               )
##            dlg.ShowModal()
##            dlg.Destroy()
#            self.texte.SetBackgroundColour("pink")
#            self.texte.SetToolTipString(u"Fichier Séquence corrompu !")

    
        if self.sequence:
            bmp = self.sequence.GetApercu().ConvertToImage().Scale(210, 297).ConvertToBitmap()
            self.apercu.SetBitmap(bmp)
            self.lien.SetLabel()
            self.lien.SetImage(bmp)
            self.lien.SetLien()
            self.lien.SetTitre(self.sequence.intitule)

        self.Layout()
        
        if sendEvt:
            self.sendEvent()
            
        return True
            
####################################################################################
#
#   Classe définissant le panel de propriété de la compétence
#
####################################################################################
class PanelPropriete_Competences(PanelPropriete):
    def __init__(self, parent, competence):
        
        self.competence = competence
        
        
        PanelPropriete.__init__(self, parent)
        
        self.construire()
        
        self.Layout()
        
    #############################################################################            
    def GetDocument(self):
        return self.competence.parent
    
    ######################################################################################  
    def construire(self):
        self.DestroyChildren()
#        if hasattr(self, 'arbre'):
#            self.sizer.Remove(self.arbre)
        self.arbre = ArbreCompetences(self, self.competence.GetTypeEnseignement())
        self.sizer.Add(self.arbre, (0,0), flag = wx.EXPAND)
        if not self.sizer.IsColGrowable(0):
            self.sizer.AddGrowableCol(0)
        if not self.sizer.IsRowGrowable(0):
            self.sizer.AddGrowableRow(0)
        self.Layout()

    ######################################################################################  
    def OnSize(self, event):
        self.win.SetMinSize(self.GetClientSize())
        self.Layout()
        event.Skip()
        
    ######################################################################################  
    def AjouterCompetence(self, code):
        self.competence.competences.append(code)
        
    ######################################################################################  
    def EnleverCompetence(self, code):
        self.competence.competences.remove(code)
        
    ######################################################################################  
    def SetCompetences(self): 
        self.competence.parent.VerrouillerClasse()
        self.sendEvent()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):

        self.arbre.UnselectAll()
        for s in self.competence.competences:
            i = self.arbre.get_item_by_label(s, self.arbre.GetRootItem())

            if i.IsOk():

                self.arbre.CheckItem2(i)
        
        if sendEvt:
            self.sendEvent()
#        titre = wx.StaticText(self, -1, u"Compétence :")
#        
#        # Prévoir un truc pour que la liste des compétences tienne compte de celles déja choisies
#        # idée : utiliser cb.CLear, Clear.Append ou cb.Delete
#        listComp = []
#        l = Competences.items()
#        for c in l:
#            listComp.append(c[0] + " " + c[1])
#        listComp.sort()    
#        
#        cb = wx.ComboBox(self, -1, u"Choisir une compétence",
#                         choices = listComp,
#                         style = wx.CB_DROPDOWN
#                         | wx.TE_PROCESS_ENTER
#                         | wx.CB_READONLY
#                         #| wx.CB_SORT
#                         )
#        self.cb = cb
#        
#        self.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
#        self.sizer.Add(cb, (0,1), flag = wx.EXPAND)
#        self.sizer.Layout()
#        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        
#    #############################################################################            
#    def EvtComboBox(self, event):
#        self.competence.SetNum(event.GetSelection())
#        self.sendEvent()
#        
#    #############################################################################            
#    def MiseAJour(self, sendEvt = False):
#        self.cb.SetSelection(self.competence.num)
#        if sendEvt:
#            self.sendEvent()
        


####################################################################################
#
#   Classe définissant le panel de propriété de savoirs
#
####################################################################################
class PanelPropriete_Savoirs(PanelPropriete):
    def __init__(self, parent, savoirs, prerequis):
        
        self.savoirs = savoirs
        self.prerequis = prerequis
        PanelPropriete.__init__(self, parent)
        
        self.construire()

        
    #############################################################################            
    def GetDocument(self):
        return self.savoirs.parent
        
    ######################################################################################  
    def construire(self):
        self.DestroyChildren()
#        if hasattr(self, 'arbre'):
#            self.sizer.Remove(self.arbre)
        self.arbre = ArbreSavoirs(self, self.savoirs, self.prerequis)
        self.sizer.Add(self.arbre, (0,0), flag = wx.EXPAND)
        if not self.sizer.IsColGrowable(0):
            self.sizer.AddGrowableCol(0)
        if not self.sizer.IsRowGrowable(0):
            self.sizer.AddGrowableRow(0)
        self.Layout()
        
    

    ######################################################################################  
    def SetSavoirs(self): 
        self.savoirs.parent.VerrouillerClasse()
        self.sendEvent()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.arbre.UnselectAll()
        for s in self.savoirs.savoirs:
            i = self.arbre.get_item_by_label(s, self.arbre.GetRootItem())

            if i.IsOk():
                self.arbre.CheckItem2(i)
        
        if sendEvt:
            self.sendEvent()
            
            
            
####################################################################################
#
#   Classe définissant le panel de propriété de la séance
#
####################################################################################
class PanelPropriete_Seance(PanelPropriete):
    def __init__(self, parent, seance):
        PanelPropriete.__init__(self, parent)
        self.seance = seance

        #
        # Type de séance
        #
        titre = wx.StaticText(self, -1, u"Type : ")
        cbType = wx.combo.BitmapComboBox(self, -1, u"Choisir un type de séance",
                             choices = [], size = (-1,25),
                             style = wx.CB_DROPDOWN
                             | wx.TE_PROCESS_ENTER
                             | wx.CB_READONLY
                             #| wx.CB_SORT
                             )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbType)
        self.cbType = cbType
        self.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        self.sizer.Add(cbType, (0,1), flag = wx.EXPAND)
        
        #
        # Intitulé de la séance
        #
        box = wx.StaticBox(self, -1, u"Intitulé")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        bsizer.Add(textctrl, flag = wx.EXPAND)
        self.textctrl = textctrl
#        self.Bind(wx.EVT_TEXT, self.EvtTextIntitule, textctrl)
        self.textctrl.Bind(wx.EVT_KILL_FOCUS, self.EvtTextIntitule)
        
        cb = wx.CheckBox(self, -1, u"Montrer dans la zone de déroulement de la séquence")
        cb.SetValue(self.seance.intituleDansDeroul)
        bsizer.Add(cb, flag = wx.EXPAND)
        
        vcTaille = VariableCtrl(self, seance.taille, signeEgal = True, slider = False, sizeh = 40,
                                help = u"Taille des caractères", unite = u"%")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcTaille)
        bsizer.Add(vcTaille, flag = wx.EXPAND)
        self.vcTaille = vcTaille
        
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
        self.cbInt = cb
        self.sizer.Add(bsizer, (1,0), (1,2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
#        self.sizer.Add(textctrl, (1,1), flag = wx.EXPAND)
        
        
        
        #
        # Durée de la séance
        #
        vcDuree = VariableCtrl(self, seance.duree, coef = 0.25, signeEgal = True, slider = False, sizeh = 30,
                               help = u"Durée de la séance en heures", unite = u"h")
#        textctrl = wx.TextCtrl(self, -1, u"1")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
        self.vcDuree = vcDuree
        self.sizer.Add(vcDuree, (2,0), (1, 2))
        
        #
        # Effectif
        #
        titre = wx.StaticText(self, -1, u"Effectif : ")
        cbEff = wx.ComboBox(self, -1, u"",
                         choices = [],
                         style = wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         | wx.CB_READONLY
                         #| wx.CB_SORT
                         )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxEff, cbEff)
        self.cbEff = cbEff
        self.titreEff = titre
        
        self.sizer.Add(titre, (3,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        self.sizer.Add(cbEff, (3,1), flag = wx.EXPAND)
#        self.sizer.AddGrowableRow(3)
#        self.sizer.Add(self.nombre, (3,2))
        
        #
        # Démarche
        #
        titre = wx.StaticText(self, -1, u"Démarche : ")
        cbDem = wx.ComboBox(self, -1, u"",
                         choices = [],
                         style = wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         | wx.CB_READONLY
                         #| wx.CB_SORT
                         )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxDem, cbDem)
        self.cbDem = cbDem
        self.titreDem = titre
        
#        nombre = wx.StaticText(self, -1, u"")
#        self.nombre = nombre
        
        self.sizer.Add(titre, (4,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        self.sizer.Add(cbDem, (4,1), flag = wx.EXPAND)
#        self.sizer.AddGrowableRow(4)
#        self.sizer.Add(self.nombre, (4,2))
        
        #
        # Nombre de séances en parallèle
        #
        vcNombre = VariableCtrl(self, seance.nombre, signeEgal = True, slider = False, sizeh = 30,
                                help = u"Nombre de groupes réalisant simultanément la même séance")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcNombre)
        self.vcNombre = vcNombre
        self.sizer.Add(vcNombre, (5,0), (1, 2))
#        self.sizer.AddGrowableRow(5)
        
        #
        # Nombre de rotations
        #
        vcNombreRot = VariableCtrl(self, seance.nbrRotations, signeEgal = True, slider = False, sizeh = 30,
                                help = u"Nombre de rotations")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcNombreRot)
        self.vcNombreRot = vcNombreRot
        self.sizer.Add(vcNombreRot, (6,0), (1, 2))
        
        
        #
        # Systèmes
        #
        self.box = wx.StaticBox(self, -1, u"Systèmes ou matériels nécessaires", size = (200,200))
        self.box.SetMinSize((200,200))
        self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        self.systemeCtrl = []
        self.ConstruireListeSystemes()
        self.sizer.Add(self.bsizer, (0,4), (7, 1), flag = wx.EXPAND)
        
#        self.sizer.AddGrowableCol(4, proportion = 1)


        #
        # Lien
        #
        box = wx.StaticBox(self, -1, u"Lien externe")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.selec = URLSelectorCombo(self, self.seance.lien, self.seance.GetPath())
        bsizer.Add(self.selec, flag = wx.EXPAND)
        self.btnlien = wx.Button(self, -1, u"Ouvrir le lien externe")
        self.btnlien.Hide()
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btnlien)
        bsizer.Add(self.btnlien)
        self.sizer.Add(bsizer, (5,5), (2, 1), flag = wx.EXPAND)
        
        #
        # Description de la séance
        #
        dbox = wx.StaticBox(self, -1, u"Description")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
        bd = wx.Button(self, -1, u"Editer")
        tc = richtext.RichTextPanel(self, self.seance)
        tc.SetMaxSize((-1, 150))
        dbsizer.Add(bd, flag = wx.EXPAND)
        dbsizer.Add(tc, 1, flag = wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        self.sizer.Add(dbsizer, (0,5), (5, 1), flag = wx.EXPAND)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        self.sizer.SetEmptyCellSize((0,0))
        
        #
        # Mise en place
        #
        self.sizer.Layout()
    
    
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        self.selec.SetPathSeq(pathSeq)
        
        
    ######################################################################################  
    def OnPathModified(self, lien):
        self.seance.OnPathModified()
        self.btnlien.Show(self.seance.lien.path != "")
        self.Layout()
        self.Refresh()
        
    
    ############################################################################            
    def ConstruireListeSystemes(self):
        self.Freeze()
        if self.seance.typeSeance in ["AP", "ED", "P"]:
            for ss in self.systemeCtrl:
                self.bsizer.Detach(ss)
                ss.Destroy()
                
            self.systemeCtrl = []
            for s in self.seance.systemes:
                v = VariableCtrl(self, s, signeEgal = False, 
                                 slider = False, fct = None, help = "", sizeh = 30)
                self.Bind(EVT_VAR_CTRL, self.EvtVarSysteme, v)
                self.bsizer.Add(v, flag = wx.ALIGN_RIGHT)#|wx.EXPAND) 
                self.systemeCtrl.append(v)
            self.bsizer.Layout()
            
            if len(self.seance.systemes) > 0:
                self.box.Show(True)
            else:
                self.box.Hide()
        else:
            for ss in self.systemeCtrl:
                self.bsizer.Detach(ss)
                ss.Destroy()
            self.systemeCtrl = []
            self.box.Hide()
            
        self.box.SetMinSize((200,200))
        self.Layout()
        self.Thaw()
    
    
    #############################################################################            
    def MiseAJourListeSystemes(self):
        if self.seance.typeSeance in ["AP", "ED", "P"]:
            self.Freeze()
            for i, s in enumerate(self.seance.systemes):
                self.systemeCtrl[i].Renommer(s.n)
            self.bsizer.Layout()
            self.Layout()
            self.Thaw()

    #############################################################################
    def MiseAJourTypeEnseignement(self):
        self.cbDem.Show(self.seance.GetClasse().typeEnseignement != "SSI")
        self.titreDem.Show(self.seance.GetClasse().typeEnseignement != "SSI")
        
    ############################################################################            
    def GetDocument(self):
        return self.seance.GetDocument()
    
    #############################################################################            
    def EvtClick(self, event):
        if not self.edition:
            self.win = richtext.RichTextFrame(u"Description de la séance "+ self.seance.code, self.seance)
            self.edition = True
            self.win.Show(True)
        else:
            self.win.SetFocus()
        
        
    #############################################################################            
    def EvtVarSysteme(self, event):
        self.sendEvent()
        
    #############################################################################            
    def EvtCheckBox(self, event):
        self.seance.intituleDansDeroul = event.IsChecked()
        self.sendEvent()
    
    #############################################################################            
    def EvtTextIntitule(self, event):
        self.seance.SetIntitule(self.textctrl.GetValue())
        event.Skip()
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
            
    
    #############################################################################            
    def EvtText(self, event):
        if event.GetId() == self.vcDuree.GetId():
            self.seance.SetDuree(event.GetVar().v[0])
        elif event.GetId() == self.vcNombre.GetId():
            self.seance.SetNombre(event.GetVar().v[0])
        elif event.GetId() == self.vcNombreRot.GetId():
            self.seance.SetNombreRot(event.GetVar().v[0])
            
        elif event.GetId() == self.vcTaille.GetId():
            self.seance.SetTaille(event.GetVar().v[0])
            
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
            
   
        
    #############################################################################            
    def EvtComboBox(self, event):
        if self.seance.typeSeance in ["R", "S"] and constantes.listeTypeSeance[event.GetSelection()] not in ["R", "S"]:
            dlg = wx.MessageDialog(self, u"Modifier le type de cette séance entrainera la suppression de toutes les sous séances !\n" \
                                         u"Voulez-vous continuer ?",
                                    u"Modification du type de séance",
                                    wx.YES_NO | wx.ICON_EXCLAMATION
                                    #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                    )
            res = dlg.ShowModal()
            dlg.Destroy() 
            if res == wx.ID_NO:
                return
            else:
                self.seance.SupprimerSousSeances()
        
        deja = self.seance.typeSeance in ["AP", "ED", "P"]
        
        self.seance.SetType(get_key(constantes.TypesSeance, self.cbType.GetStringSelection()))
        
        if self.seance.typeSeance in ["AP", "ED", "P"]:
            if not deja:
                for sy in self.seance.GetDocument().systemes:
                    self.seance.AjouterSysteme(nom = sy.nom, construire = False)
        else:
            self.seance.systemes = []
            
        if self.cbEff.IsEnabled() and self.cbEff.IsShown():
            self.seance.SetEffectif(self.cbEff.GetStringSelection())

        self.AdapterAuType()
        self.ConstruireListeSystemes()
        self.Layout()
        self.sendEvent()
       
        
        
    #############################################################################            
    def EvtComboBoxEff(self, event):

        self.seance.SetEffectif(event.GetString())  

#        l = Effectifs.values()
#        continuer = True
#        i = 0
#        while continuer:
#            if i>=len(l):
#                continuer = False
#            else:
#                if l[i][0] == event.GetString():
#                    n = l[i][1]
#                    continuer = False
#            i += 1
#        self.nombre.SetLabel(u" (" + str(n) + u" élèves)")
        self.sendEvent()



    #############################################################################            
    def EvtComboBoxDem(self, event):
        self.seance.SetDemarche(event.GetString())  
        self.sendEvent()
       
       
        
    #############################################################################            
    def OnClick(self, event):
        self.seance.AfficherLien(self.GetDocument().GetPath())
        
        
    #############################################################################            
    def AdapterAuType(self):
        """ Adapte le panel au type de séance
        """
        
        #
        # Type de parent
        #
        if self.seance.EstSousSeance():
            listType = constantes.listeTypeActivite
            if not self.seance.parent.EstSousSeance():
                listType = constantes.listeTypeActivite + ["S"]
        else:
            listType = constantes.listeTypeSeance
        
#        listTypeS = []
#        for t in listType:
#            listTypeS.append((constantes.TypesSeance[t], constantes.imagesSeance[t].GetBitmap()))
        
        listTypeS = [(constantes.TypesSeance[t], constantes.imagesSeance[t].GetBitmap()) for t in listType]
        
        n = self.cbType.GetSelection()   
        self.cbType.Clear()
        for s in listTypeS:
            self.cbType.Append(s[0], s[1])
        self.cbType.SetSelection(n)
        self.cbType.Layout()
        
        #
        # Durée
        #
        if self.seance.typeSeance in ["R", "S"]:
            self.vcDuree.Activer(False)
        
        # Effectif
        if self.seance.typeSeance in ["C", "E", "SS"]:
            listEff = ["C"]
            self.cbEff.Show(True)
            self.titreEff.Show(True)

        elif self.seance.typeSeance in ["R", "S"] or self.seance.typeSeance == "":
            self.cbEff.Show(False)
            self.titreEff.Show(False)
            listEff = []
            
        elif self.seance.typeSeance in ["ED", "P", "TD"]:
            listEff = ["C", "G", "D", "E", "P"]
            self.cbEff.Show(True)
            self.titreEff.Show(True)

        elif self.seance.typeSeance in ["AP"]:
            listEff = ["P", "E"]
            self.cbEff.Show(True)
            self.titreEff.Show(True)

        elif self.seance.typeSeance in ["SA"]:
            listEff = ["C", "G"]
            self.cbEff.Show(True)
            self.titreEff.Show(True)

        self.vcNombreRot.Show(self.seance.typeSeance == "R")
        
        self.cbEff.Clear()
        for s in listEff:
            self.cbEff.Append(strEffectifComplet(self.seance.GetDocument().classe, s, -1))
        self.cbEff.SetSelection(0)
        
        
        # Démarche
        if self.seance.typeSeance in ["AP", "ED"]:
            listDem = ["I", "R"]
            self.cbDem.Show(True and self.seance.GetClasse().typeEnseignement != "SSI")
            self.titreDem.Show(True and self.seance.GetClasse().typeEnseignement != "SSI")
        elif self.seance.typeSeance == "P":
            listDem = ["I", "R", "P"]
            self.cbDem.Show(True and self.seance.GetClasse().typeEnseignement != "SSI")
            self.titreDem.Show(True and self.seance.GetClasse().typeEnseignement != "SSI")
        else:
            self.cbDem.Show(False)
            self.titreDem.Show(False)
            listDem = []
        
        # Nombre
        if self.seance.typeSeance in ["AP", "ED"]:
            self.vcNombre.Show(True)
        else:
            self.vcNombre.Show(False) 
            
        self.cbDem.Clear()
        for s in listDem:
            self.cbDem.Append(constantes.Demarches[s])
        self.cbDem.SetSelection(0)
        
    #############################################################################            
    def MarquerProblemeDuree(self, etat):
        return
        self.vcDuree.marquerValid(etat)
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.AdapterAuType()
        
        if self.seance.typeSeance != "":
            self.cbType.SetSelection(self.cbType.GetStrings().index(constantes.TypesSeance[self.seance.typeSeance]))
        self.textctrl.ChangeValue(self.seance.intitule)
        self.vcDuree.mofifierValeursSsEvt()
        
        if self.cbEff.IsShown():#self.cbEff.IsEnabled() and 
            self.cbEff.SetSelection(findEffectif(self.cbEff.GetStrings(), self.seance.effectif))
        
        if self.cbDem.IsShown():#self.cbDem.IsEnabled() and :
            self.cbDem.SetSelection(self.cbDem.GetStrings().index(constantes.Demarches[self.seance.demarche]))
            

        if self.seance.typeSeance in ["AP", "ED", "P"]:
            self.vcNombre.mofifierValeursSsEvt()
        elif self.seance.typeSeance == "R":
            self.vcNombreRot.mofifierValeursSsEvt()
        
        self.vcTaille.mofifierValeursSsEvt()
        
#        if self.seance.typeSeance in ["AP", "ED", "P"]:
#            for i in range(self.seance.nSystemes):
#                s = self.seance.systemes[i]
#                self.systemeCtrl[i].mofifierValeursSsEvt()
#            self.vcNombre.mofifierValeursSsEvt()
        
        self.cbInt.SetValue(self.seance.intituleDansDeroul)
        if sendEvt:
            self.sendEvent()
        
        self.MiseAJourLien()
        
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(self.seance.lien.path)
        self.btnlien.Show(self.seance.lien.path != "")
        self.Layout()
        
        
    
    def MiseAJourDuree(self):
        self.vcDuree.mofifierValeursSsEvt()
    
    
    
    
    
    
    
    
    
####################################################################################
#
#   Classe définissant le panel de propriété de la tache
#
####################################################################################
class PanelPropriete_Tache(PanelProprieteBook, PanelPropriete):
    def __init__(self, parent, tache, revue = 0):
        self.tache = tache
        self.revue = revue
        
        if not tache.phase in ["R2", "S"]:
            #
            # La page "Généralités"
            #
            PanelProprieteBook.__init__(self, parent)
            pageGen = PanelPropriete(self)
            bg_color = self.Parent.GetBackgroundColour()
            pageGen.SetBackgroundColour(bg_color)
            self.pageGen = pageGen
            self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        else:
            #
            # Pas de book pour la revue 2 et la soutenance
            #
            PanelPropriete.__init__(self, parent)
            pageGen = self
            self.pageGen = pageGen
            
        
        #
        # Phase
        #
        if tache.phase in ["R1", "R2", "S", "Rev"]:
            titre = wx.StaticText(pageGen, -1, u"Phase : "+constantes.NOM_PHASE_TACHE_E[tache.phase])
            pageGen.sizer.Add(titre, (0,0), (1,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, border = 5)
        else:
            titre = wx.StaticText(pageGen, -1, u"Phase :")
            cbPhas = wx.combo.BitmapComboBox(pageGen, -1, u"Selectionner la phase",
                                 choices = constantes.getLstPhase(tache.GetTypeEnseignement(True)),
                                 style = wx.CB_DROPDOWN
                                 | wx.TE_PROCESS_ENTER
                                 | wx.CB_READONLY
                                 #| wx.CB_SORT
                                 )
            for i, k in enumerate(constantes.PHASE_TACHE[tache.GetTypeEnseignement(True)]):
                cbPhas.SetItemBitmap(i, constantes.imagesTaches[k].GetBitmap())
            pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbPhas)
            self.cbPhas = cbPhas
            pageGen.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 5)
            pageGen.sizer.Add(cbPhas, (0,1), flag = wx.EXPAND)
        
        #
        # Position de la revue 1
        #
        if tache.phase == "R1":
            self.cbR1 = wx.CheckBox(pageGen, -1, u"Placer avant la conception détaillée")
            self.cbR1.SetValue(self.tache.GetDocument().R1avantConception)
            pageGen.sizer.Add(self.cbR1, (0,1), flag = wx.EXPAND)
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxR1, self.cbR1)
        
        #
        # Intitulé de la tache
        #
        if not tache.phase in ["R1", "R2", "S", "Rev"]:
            box = wx.StaticBox(pageGen, -1, u"Intitulé")
            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            textctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
            bsizer.Add(textctrl, flag = wx.EXPAND)
            self.textctrl = textctrl
            self.boxInt = box
            self.textctrl.Bind(wx.EVT_KILL_FOCUS, self.EvtTextIntitule)
            pageGen.sizer.Add(bsizer, (1,0), (1,2), 
                           flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)

        
        #
        # Durée de la tache
        #
        if not tache.phase in ["R1", "R2", "S", "Rev"]:
            vcDuree = VariableCtrl(pageGen, tache.duree, coef = 0.5, signeEgal = True, slider = False,
                                   help = u"Volume horaire de la tâche en heures", sizeh = 60)
            pageGen.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
            self.vcDuree = vcDuree
            pageGen.sizer.Add(vcDuree, (2,0), (1, 2))
        
        
        #
        # Elèves impliqués
        #
        if not tache.phase in ["R1", "R2", "S"]:
            self.box = wx.StaticBox(pageGen, -1, u"Elèves impliqués", size = (200,200))
            self.box.SetMinSize((150,200))
            self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
            self.elevesCtrl = []
            self.ConstruireListeEleves()
            pageGen.sizer.Add(self.bsizer, (0,2), (4, 1), flag = wx.EXPAND)
        
        
        
        
        #
        # Description de la tâche
        #
        dbox = wx.StaticBox(pageGen, -1, u"Description")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
        bd = wx.Button(pageGen, -1, u"Editer")
        tc = richtext.RichTextPanel(pageGen, self.tache)
#        tc.SetMaxSize((-1, 150))
        tc.SetMinSize((150, 60))
        dbsizer.Add(tc,1, flag = wx.EXPAND)
        dbsizer.Add(bd, flag = wx.EXPAND)
        pageGen.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        if tache.phase in ["R1", "R2", "S", "Rev"]:
            pageGen.sizer.Add(dbsizer, (1,0), (3, 2), flag = wx.EXPAND)
            pageGen.sizer.AddGrowableCol(0)
        else:
            pageGen.sizer.Add(dbsizer, (0,3), (4, 1), flag = wx.EXPAND)
            pageGen.sizer.AddGrowableCol(3)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        
        
        if not tache.phase in ["R2", "S"]:
            self.AddPage(pageGen, u"Propriétés générales")
#        pageGen.sizer.Layout()
        
        
        if not tache.phase in ["R2", "S"]:
            #
            # La page "Compétences"
            #
    #        pageCom = PanelPropriete(self, style = wx.RETAINED)
            pageCom = wx.Panel(self, -1)
            
        
    #        pageCom.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            self.pageCom = pageCom
            pageComsizer = wx.BoxSizer(wx.HORIZONTAL)
            #
            # Compétences employées
            #
            if tache.phase != "S":
                self.arbre = ArbreCompetencesPrj(pageCom, tache.GetTypeEnseignement(), self,
                                                 revue = self.tache.phase in ["R1", "R2", "S", "Rev"])
                pageComsizer.Add(self.arbre, 1, flag = wx.EXPAND)
        
            
        
            pageCom.SetSizer(pageComsizer)
            self.AddPage(pageCom, u"Compétences à mobiliser") 
            
#            pageComsizer.Layout() 
            self.pageComsizer = pageComsizer
        
        
        #
        # Mise en place
        #
        self.Layout()
        self.FitInside()
        wx.CallAfter(self.PostSizeEvent)
        self.Show()
#        wx.CallAfter(self.Layout)
        
        
    ####################################################################################
    def OnPageChanged(self, event):
        sel = self.GetSelection()
#        self.MiseAJourPoids()
        event.Skip()
        
    ####################################################################################
    def MiseAJourPoids(self):
        for c in self.tache.indicateurs:
            self.MiseAJourIndicateurs(c)
            
    ####################################################################################
    def OnSelChanged(self, event):
        item = event.GetItem() 
        self.competence = self.arbre.GetItemText(item).split()[0]
        self.MiseAJourIndicateurs(self.competence)
        
    #############################################################################            
    def MiseAJourIndicateurs(self, competence):
#        print "MiseAJourIndicateurs", competence
        self.Freeze()
        if False:#self.tache.GetTypeEnseignement() != "SSI":
            indicateurs = constantes.dicIndicateurs[self.tache.GetTypeEnseignement()]
            lab = u"Indicateurs"
            
            # On supprime l'ancienne CheckListBox
            if self.liste != None:
                self.ibsizer.Detach(self.liste)
                self.liste.Destroy()
            
            if competence in indicateurs.keys():
                self.liste = wx.CheckListBox(self.pageCom, -1, choices = indicateurs[competence], style = wx.BORDER_NONE)
    
                lst = self.tache.indicateurs[competence]
                for i, c in enumerate(lst):
                    self.liste.Check(i, c)
                
                self.ibox.SetLabel(lab+u" "+competence)
                self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.liste)
                
            else:
                self.liste = wx.StaticText(self.pageCom, -1, u"Selectionner une compétence pour afficher les indicateurs associés.")
                self.ibox.SetLabel(lab)
                
            self.ibsizer.Add(self.liste,1 , flag = wx.EXPAND)
                
            self.arbre.Layout()
            self.ibsizer.Layout()
            self.pageComsizer.Layout()
        
        else:
            if competence in self.tache.indicateurs.keys():
                self.arbre.MiseAJour(competence, self.tache.indicateurs[competence])
            else:
                self.arbre.MiseAJour(competence, constantes.dicCompetences_prj_simple[self.tache.GetTypeEnseignement()][competence][1])
            
            
        self.Thaw()
        
        
    ######################################################################################  
    def EvtCheckListBox(self, event):
        index = event.GetSelection()
        
        if self.competence in self.tache.indicateurs.keys():
            lst = self.tache.indicateurs[self.competence]
        else:
            lst = [self.competence in self.tache.competences]*len(constantes.dicIndicateurs[self.tache.GetTypeEnseignement()][self.competence])
            
        lst[index] = self.liste.IsChecked(index)
        
        if True in lst and not self.competence in self.tache.competences:
            self.tache.competences.append(self.competence)
            self.arbre.CheckItem2(self.arbre.FindItem(self.arbre.GetRootItem(), self.competence), True)
            self.arbre.SelectItem(self.arbre.FindItem(self.arbre.GetRootItem(), self.competence))
        if not True in lst and self.competence in self.tache.competences:
            self.tache.competences.remove(self.competence)
#            self.MiseAJour(sendEvt = False)
            self.arbre.CheckItem2(self.arbre.FindItem(self.arbre.GetRootItem(), self.competence), False)
            self.arbre.SelectItem(self.arbre.FindItem(self.arbre.GetRootItem(), self.competence))
            
        self.Refresh()    
        self.sendEvent()
        
#        self.liste.Check()
#        self.tache.indicateurs[]
#        label = self.liste.GetString(index)
#        status = 'un'
#        if self.liste.IsChecked(index):
#            status = ''
#        
#        self.lb.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
        

    ######################################################################################  
    def AjouterCompetence(self, code):
        if not code in self.tache.indicateurs:
            self.tache.indicateurs.append(code)
#        print "AjouterCompetence", code
#        if True:#self.tache.GetTypeEnseignement() != "SSI":
#            if not True in self.tache.indicateurs[code]:
#                self.tache.indicateurs[code] = [True]*len(constantes.dicIndicateurs[self.tache.GetTypeEnseignement()][code])
#                
#        else:
#            self.tache.indicateurs[code] = constantes.dicCompetences_prj_simple[self.tache.GetTypeEnseignement()][code][1]
#        self.MiseAJourIndicateurs(code)
        
    ######################################################################################  
    def EnleverCompetence(self, code):
        
        self.tache.indicateurs.remove(code)
        # on recommence : pour corriger un bug
        if code in self.tache.indicateurs:
            self.tache.indicateurs.remove(code)
#        if code in self.tache.indicateurs.keys():
#            del self.tache.indicateurs[code]
        
#        self.MiseAJourIndicateurs(code)
        
    ############################################################################            
    def SetCompetences(self):
        self.GetDocument().MiseAJourDureeEleves()
        self.sendEvent()
        self.tache.parent.VerrouillerClasse()
        
    ############################################################################            
    def ConstruireListeEleves(self):
        if hasattr(self, 'elevesCtrl'):
            self.pageGen.Freeze()
            
            for ss in self.elevesCtrl:
                self.bsizer.Detach(ss)
                ss.Destroy()
                
            self.elevesCtrl = []
            for i, e in enumerate(self.GetDocument().eleves):
                v = wx.CheckBox(self.pageGen, 100+i, e.GetNomPrenom())
                v.SetMinSize((200,-1))
                v.SetValue(i in self.tache.eleves)
                self.pageGen.Bind(wx.EVT_CHECKBOX, self.EvtCheckEleve, v)
                self.bsizer.Add(v, flag = wx.ALIGN_LEFT|wx.ALL, border = 3)#|wx.EXPAND) 
                self.elevesCtrl.append(v)
            self.bsizer.Layout()
            
            if len(self.GetDocument().eleves) > 0:
                self.box.Show(True)
            else:
                self.box.Hide()
    
            self.box.SetMinSize((200,200))
            self.pageGen.Layout()
            self.pageGen.Thaw()
        
        
    #############################################################################            
    def MiseAJourListeEleves(self):
        """ Met à jour la liste des élèves
        """
        if not self.tache.phase in ["S", "R1", "R2"]:
            self.pageGen.Freeze()
            for i, e in enumerate(self.GetDocument().eleves):
                self.elevesCtrl[i].SetLabel(e.GetNomPrenom())
            self.bsizer.Layout()
            self.pageGen.Layout()
            self.pageGen.Thaw()

    
        
    ############################################################################            
    def GetDocument(self):
        return self.tache.GetDocument()
    
    #############################################################################            
    def EvtClick(self, event):
        if not self.edition:
            self.win = richtext.RichTextFrame(u"Description de la tâche "+ self.tache.code, self.tache)
            self.edition = True
            self.win.Show(True)
        else:
            self.win.SetFocus()
        
        
    #############################################################################            
    def EvtVarSysteme(self, event):
        self.sendEvent()
        
#    #############################################################################            
#    def EvtCheckBox(self, event):
#        self.tache.intituleDansDeroul = event.IsChecked()
#        self.sendEvent()
        
    #############################################################################            
    def EvtCheckBoxR1(self, event):
        self.tache.GetDocument().R1avantConception = event.IsChecked()
        self.tache.SetPhase("R1")
        self.sendEvent()
        
    #############################################################################            
    def EvtCheckEleve(self, event):
        lst = []
        for i,s in enumerate(self.GetDocument().eleves):
            if self.elevesCtrl[i].IsChecked():
                lst.append(i)
        self.tache.eleves = lst
        self.GetDocument().MiseAJourDureeEleves()
        self.sendEvent()    
    
    #############################################################################            
    def EvtTextIntitule(self, event):
#        print "EvtTextIntitule"
        self.tache.SetIntitule(self.textctrl.GetValue())
#        self.sendEvent()
        event.Skip()
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def EvtText(self, event):
        if event.GetId() == self.vcDuree.GetId():
            self.tache.SetDuree(event.GetVar().v[0])
        elif event.GetId() == self.vcNombre.GetId():
            self.tache.SetNombre(event.GetVar().v[0])
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def EvtComboBox(self, event):
        newPhase = get_key(constantes.NOM_PHASE_TACHE[self.tache.GetTypeEnseignement(True)], 
                                        self.cbPhas.GetStringSelection())
        if self.tache.phase != newPhase:
            self.tache.SetPhase(newPhase)
            self.arbre.MiseAJourPhase(newPhase)
            self.pageGen.Layout()
            self.sendEvent()
        
    
    #############################################################################            
    def MiseAJourDuree(self):
        """ Mise à jour du champ de texte de la durée
            (conformément à la valeur de la variable associée)
        """
        if hasattr(self, 'vcDuree'):
            self.vcDuree.mofifierValeursSsEvt()
        
    
#    #############################################################################            
#    def TransformerEnRevue(self):
#        if self.tache.phase in ["R1", "R2"]:
#            print "R", constantes.NOM_PHASE_TACHE[self.tache.phase]
#            self.cbPhas.Destroy()
#            self.cbPhas = wx.StaticText(self, -1, constantes.NOM_PHASE_TACHE[self.tache.phase])
#            self.sizer.Add(self.cbPhas, (0,1), flag = wx.EXPAND|wx.ALL, border = 5)
#            self.vcDuree.Destroy()
#            self.textctrl.Destroy()
#            self.boxInt.Destroy()
#            self.sizer.Layout()

            
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "MiseAJour", self.tache.phase, self.tache.intitule
        if hasattr(self, 'arbre'):
            self.arbre.UnselectAll()
            
#            root = self.arbre.GetRootItem()
            for s in self.tache.indicateurs:
                if s in self.arbre.items.keys():
                    self.arbre.CheckItem2(self.arbre.items[s])
                
                
#                print "   ", s
#                i = self.arbre.FindItem(root, s)
#                print "      ", i#.GetText()
#                if i.IsOk():
#                    self.arbre.CheckItem2(i)
            
        if hasattr(self, 'textctrl'):
            self.textctrl.SetValue(self.tache.intitule)
        
        if hasattr(self, 'cbPhas') and self.tache.phase != '':
            self.cbPhas.SetStringSelection(constantes.NOM_PHASE_TACHE[self.tache.GetTypeEnseignement(True)][self.tache.phase])
            
        if sendEvt:
            self.sendEvent()
        
#    ######################################################################################  
#    def MiseAJourPoidsCompetences(self, code = None):
#        if hasattr(self, 'arbre'):
#            if self.tache.GetTypeEnseignement() == "SSI":
#                self.arbre.MiseAJour(code)
        
    #############################################################################
    def MiseAJourTypeEnseignement(self, type_ens):
        if hasattr(self, 'arbre'):
            self.arbre.MiseAJourTypeEnseignement(type_ens)
        if hasattr(self, 'cbR1'):
            self.cbR1.Show(type_ens != "SSI")
        
        
####################################################################################
#
#   Classe définissant le panel de propriété d'un système
#
####################################################################################
class PanelPropriete_Systeme(PanelPropriete):
    def __init__(self, parent, systeme):
        
        self.systeme = systeme
        self.parent = parent
        
        PanelPropriete.__init__(self, parent)
        
        #
        # Nom
        #
        titre = wx.StaticText(self, -1, u"Nom du système :")
        textctrl = wx.TextCtrl(self, -1, u"")
        self.textctrl = textctrl
        
        self.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)
        self.sizer.Add(textctrl, (0,1), flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        
        #
        # Nombre de systèmes disponibles en parallèle
        #
        vcNombre = VariableCtrl(self, systeme.nbrDispo, signeEgal = True, slider = False, 
                                help = u"Nombre de d'exemplaires de ce système disponibles simultanément.")
        self.Bind(EVT_VAR_CTRL, self.EvtVar, vcNombre)
        self.vcNombre = vcNombre
        self.sizer.Add(vcNombre, (1,0), (1, 2), flag = wx.TOP|wx.BOTTOM, border = 3)
        
        #
        # Image
        #
        box = wx.StaticBox(self, -1, u"Image du système")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        image = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.image = image
        self.SetImage()
        bsizer.Add(image, flag = wx.EXPAND)
        
        
        bt = wx.Button(self, -1, u"Changer l'image")
        bt.SetToolTipString(u"Cliquer ici pour sélectionner un fichier image")
        bsizer.Add(bt, flag = wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt)
        self.sizer.Add(bsizer, (0,3), (2,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |

        #
        # Lien
        #
        box = wx.StaticBox(self, -1, u"Lien externe")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.selec = URLSelectorCombo(self, self.systeme.lien, self.systeme.GetPath())
        bsizer.Add(self.selec, flag = wx.EXPAND)
        self.btnlien = wx.Button(self, -1, u"Ouvrir le lien externe")
        self.btnlien.Hide()
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btnlien)
        bsizer.Add(self.btnlien)
        self.sizer.Add(bsizer, (0,4), (2, 1), flag = wx.EXPAND)
        
        
        self.sizer.Layout()
        
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        self.selec.SetPathSeq(pathSeq)
        
        
    ######################################################################################  
    def OnPathModified(self, lien):
        self.systeme.OnPathModified()
        self.btnlien.Show(self.systeme.lien.path != "")
        self.Layout()
        self.Refresh()
        
    #############################################################################            
    def GetDocument(self):
        return self.systeme.parent
    
    
    #############################################################################            
    def OnClick(self, event):
        if event.GetId() == self.btnlien.GetId():
            self.systeme.AfficherLien(self.GetDocument().GetPath())
        else:
            mesFormats = u"Fichier Image|*.bmp;*.png;*.jpg;*.jpeg;*.gif;*.pcx;*.pnm;*.tif;*.tiff;*.tga;*.iff;*.xpm;*.ico;*.ico;*.cur;*.ani|" \
                           u"Tous les fichiers|*.*'"
            
            dlg = wx.FileDialog(
                                self, message=u"Ouvrir une image",
    #                            defaultDir = self.DossierSauvegarde, 
                                defaultFile = "",
                                wildcard = mesFormats,
                                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                                )
                
            # Show the dialog and retrieve the user response. If it is the OK response, 
            # process the data.
            if dlg.ShowModal() == wx.ID_OK:
                # This returns a Python list of files that were selected.
                paths = dlg.GetPaths()
                nomFichier = paths[0]
                self.systeme.image = wx.Image(nomFichier).ConvertToBitmap()
                self.SetImage()
            
            
            
            dlg.Destroy()
        
    #############################################################################            
    def SetImage(self):
        if self.systeme.image != None:
            w, h = self.systeme.image.GetSize()
            wf, hf = 200.0, 100.0
            r = max(w/wf, h/hf)
            _w, _h = w/r, h/r
            self.systeme.image = self.systeme.image.ConvertToImage().Scale(_w, _h).ConvertToBitmap()
            self.image.SetBitmap(self.systeme.image)
        self.systeme.SetImage()
        self.Layout()
        
        
        
    #############################################################################            
    def EvtText(self, event):
        self.systeme.SetNom(event.GetString())
        self.systeme.parent.MiseAJourNomsSystemes()
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def EvtVar(self, event):
        self.systeme.SetNombre()
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.textctrl.ChangeValue(self.systeme.nom)
        self.vcNombre.mofifierValeursSsEvt()
        
        if sendEvt:
            self.sendEvent()
        self.MiseAJourLien()
        
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(self.systeme.lien.path)
        self.btnlien.Show(self.systeme.lien.path != "")
        self.Layout()








####################################################################################
#
#   Classe définissant le panel de propriété d'une personne
#
####################################################################################
class PanelPropriete_Personne(PanelPropriete):
    def __init__(self, parent, personne):
        
        self.personne = personne
        self.parent = parent
        
        PanelPropriete.__init__(self, parent)
        
        #
        # Nom
        #
        titre = wx.StaticText(self, -1, u"Nom :")
        textctrl = wx.TextCtrl(self, 1, u"")
        self.textctrln = textctrl
        
        self.sizer.Add(titre, (0,0), flag = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)
        self.sizer.Add(textctrl, (0,1), flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        #
        # Prénom
        #
        titre = wx.StaticText(self, -1, u"Prénom :")
        textctrl = wx.TextCtrl(self, 2, u"")
        self.textctrlp = textctrl
        
        self.sizer.Add(titre, (1,0), flag = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)
        self.sizer.Add(textctrl, (1,1), flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        #
        # Référent
        #
        if hasattr(self.personne, 'referent'):
            cb = wx.CheckBox(self, -1, u"Référent", style=wx.ALIGN_RIGHT)
            cb.SetValue(self.personne.referent)
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
            self.cbInt = cb
            self.sizer.Add(cb, (2,0), (1,2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        
        
        #
        # Discipline
        #
        if hasattr(self.personne, 'discipline'):
            titre = wx.StaticText(self, -1, u"Discipline :")
            cbPhas = wx.combo.BitmapComboBox(self, -1, constantes.NOM_DISCIPLINES[self.personne.discipline],
                                 choices = constantes.getLstDisciplines(),
                                 style = wx.CB_DROPDOWN
                                 | wx.TE_PROCESS_ENTER
                                 | wx.CB_READONLY
                                 #| wx.CB_SORT
                                 )
#            for i, k in enumerate(constantes.DISCIPLINES):
#                cbPhas.SetItemBitmap(i, constantes.imagesTaches[k].GetBitmap())
            self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbPhas)
            self.cbPhas = cbPhas
            self.sizer.Add(titre, (3,0), (1,2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT|wx.LEFT, border = 2)
            self.sizer.Add(cbPhas, (4,0), (1,2), flag = wx.EXPAND)
        
        #
        # Avatar
        #
        box = wx.StaticBox(self, -1, u"Avatar")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        image = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.image = image
        self.SetImage()
        bsizer.Add(image, flag = wx.EXPAND)
        
        bt = wx.Button(self, -1, u"Changer l'avatar")
        bt.SetToolTipString(u"Cliquer ici pour sélectionner un fichier image")
        bsizer.Add(bt, flag = wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt)
        self.sizer.Add(bsizer, (0,3), (6,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.LEFT, border = 3)#wx.ALIGN_CENTER_VERTICAL |
        
        self.sizer.AddGrowableRow(5)
        
        self.sizer.Layout()
        
        
        
        
    
        
    #############################################################################            
    def GetDocument(self):
        return self.personne.parent
    
    
    #############################################################################            
    def OnClick(self, event):
        mesFormats = u"Fichier Image|*.bmp;*.png;*.jpg;*.jpeg;*.gif;*.pcx;*.pnm;*.tif;*.tiff;*.tga;*.iff;*.xpm;*.ico;*.ico;*.cur;*.ani|" \
                       u"Tous les fichiers|*.*'"
        
        dlg = wx.FileDialog(
                            self, message=u"Ouvrir une image",
#                            defaultDir = self.DossierSauvegarde, 
                            defaultFile = "",
                            wildcard = mesFormats,
                            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                            )
            
        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            nomFichier = paths[0]
            self.personne.avatar = wx.Image(nomFichier).ConvertToBitmap()
            self.SetImage()
        
        dlg.Destroy()
        
    #############################################################################            
    def SetImage(self):
        if self.personne.avatar != None:
            w, h = self.personne.avatar.GetSize()
            wf, hf = 200.0, 100.0
            r = max(w/wf, h/hf)
            _w, _h = w/r, h/r
            self.personne.avatar = self.personne.avatar.ConvertToImage().Scale(_w, _h).ConvertToBitmap()
            self.image.SetBitmap(self.personne.avatar)
        self.personne.SetImage()
        self.Layout()
        
        
        
    #############################################################################            
    def EvtText(self, event):
        if event.GetId() == 1:
            self.personne.SetNom(event.GetString())
        else:
            self.personne.SetPrenom(event.GetString())
        self.personne.parent.MiseAJourNomsEleves()
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        

    #############################################################################            
    def EvtComboBox(self, event):
        self.personne.SetDiscipline(get_key(constantes.NOM_DISCIPLINES, self.cbPhas.GetStringSelection()))
        self.Layout()
        self.sendEvent()
        
    #############################################################################            
    def EvtCheckBox(self, event):
        self.personne.parent.SetReferent(self.personne, event.IsChecked())
        self.sendEvent()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.textctrln.ChangeValue(self.personne.nom)
        self.textctrlp.ChangeValue(self.personne.prenom)
        if hasattr(self, 'cbPhas'):
            self.cbPhas.SetStringSelection(constantes.NOM_DISCIPLINES[self.personne.discipline])
        if hasattr(self, 'cbInt'):
            self.cbInt.SetValue(self.personne.referent)
        
        if sendEvt:
            self.sendEvent()

   
        
        

####################################################################################
#
#   Classe définissant le panel de propriété d'un support de projet
#
####################################################################################
class PanelPropriete_Support(PanelPropriete):
    def __init__(self, parent, support):
        
        self.support = support
        self.parent = parent
        
        PanelPropriete.__init__(self, parent)
        
        #
        # Nom
        #
        box = wx.StaticBox(self, -1, u"Nom du support :")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        textctrl = wx.TextCtrl(self, -1, u"")
        self.textctrl = textctrl
        bsizer.Add(textctrl, flag = wx.EXPAND)
        self.sizer.Add(bsizer, (0,0), flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)

        
        #
        # Lien
        #
        box = wx.StaticBox(self, -1, u"Lien externe")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.selec = URLSelectorCombo(self, self.support.lien, self.support.GetPath())
        bsizer.Add(self.selec, flag = wx.EXPAND)
        self.btnlien = wx.Button(self, -1, u"Ouvrir le lien externe")
        self.btnlien.Hide()
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btnlien)
        bsizer.Add(self.btnlien)
        self.sizer.Add(bsizer, (1,0), flag = wx.LEFT, border = 3)
        
        
        #
        # Image
        #
        box = wx.StaticBox(self, -1, u"Image du support")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        image = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.image = image
        self.SetImage()
        bsizer.Add(image, flag = wx.EXPAND)
        bt = wx.Button(self, -1, u"Changer l'image")
        bt.SetToolTipString(u"Cliquer ici pour sélectionner un fichier image")
        bsizer.Add(bt, flag = wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt)
        self.sizer.Add(bsizer, (0,1), (2,1), flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)#wx.ALIGN_CENTER_VERTICAL |

        
        #
        # Description du support
        #
        dbox = wx.StaticBox(self, -1, u"Description")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
        bd = wx.Button(self, -1, u"Editer")
        tc = richtext.RichTextPanel(self, self.support)
        tc.SetMaxSize((-1, 150))
        dbsizer.Add(bd, flag = wx.EXPAND)
        dbsizer.Add(tc, 1, flag = wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        self.sizer.Add(dbsizer, (0,2), (2, 1), flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        self.sizer.AddGrowableRow(1)
        self.sizer.AddGrowableCol(2)
        
        self.sizer.Layout()
        
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        self.selec.SetPathSeq(pathSeq)
        
        
    ######################################################################################  
    def OnPathModified(self, lien):
        self.support.OnPathModified()
        self.btnlien.Show(self.support.lien.path != "")
        self.Layout()
        self.Refresh()
        
    #############################################################################            
    def GetDocument(self):
        return self.support.parent
    
    
    #############################################################################            
    def OnClick(self, event):
        if event.GetId() == self.btnlien.GetId():
            self.support.AfficherLien(self.GetDocument().GetPath())
        else:
            mesFormats = u"Fichier Image|*.bmp;*.png;*.jpg;*.jpeg;*.gif;*.pcx;*.pnm;*.tif;*.tiff;*.tga;*.iff;*.xpm;*.ico;*.ico;*.cur;*.ani|" \
                           u"Tous les fichiers|*.*'"
            
            dlg = wx.FileDialog(
                                self, message=u"Ouvrir une image",
    #                            defaultDir = self.DossierSauvegarde, 
                                defaultFile = "",
                                wildcard = mesFormats,
                                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                                )
                
            # Show the dialog and retrieve the user response. If it is the OK response, 
            # process the data.
            if dlg.ShowModal() == wx.ID_OK:
                # This returns a Python list of files that were selected.
                paths = dlg.GetPaths()
                nomFichier = paths[0]
                self.support.image = wx.Image(nomFichier).ConvertToBitmap()
                self.SetImage(True)
            
            
            
            dlg.Destroy()
        
    #############################################################################            
    def SetImage(self, sendEvt = False):
        if self.support.image != None:
            w, h = self.support.image.GetSize()
            wf, hf = 200.0, 100.0
            r = max(w/wf, h/hf)
            _w, _h = w/r, h/r
            self.support.image = self.support.image.ConvertToImage().Scale(_w, _h).ConvertToBitmap()
            self.image.SetBitmap(self.support.image)
        self.support.SetImage()
        self.Layout()
        if sendEvt:
            self.sendEvent()
        
        
        
    #############################################################################            
    def EvtText(self, event):
        nt = event.GetString()
        if nt == u"":
            nt = self.support.parent.intitule
            self.textctrl.ChangeValue(nt)
        elif self.support.parent.intitule == self.support.nom:
            self.support.parent.SetText(nt)
            self.support.parent.panelPropriete.textctrl.ChangeValue(nt)
        self.support.SetNom(nt)
#        self.support.parent.MiseAJourNomsSystemes()
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def EvtClick(self, event):
        if not self.edition:
            self.win = richtext.RichTextFrame(u"Description du support "+ self.support.nom, self.support)
            self.edition = True
            self.win.Show(True)
        else:
            self.win.SetFocus()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.textctrl.ChangeValue(self.support.nom)
        if sendEvt:
            self.sendEvent()
        self.MiseAJourLien()
        
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(self.support.lien.path)
        self.btnlien.Show(self.support.lien.path != "")
        self.Layout()
        
        
        
        
        
        
        
        
        

####################################################################################
#
#   Classe définissant l'arbre de structure de base d'un document
#
####################################################################################*
class ArbreDoc(CT.CustomTreeCtrl):
    def __init__(self, parent, classe, panelProp,
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.SUNKEN_BORDER|wx.WANTS_CHARS,
                 agwStyle = CT.TR_HAS_BUTTONS|CT.TR_HAS_VARIABLE_ROW_HEIGHT | CT.TR_HIDE_ROOT|CT.TR_TOOLTIP_ON_LONG_ITEMS, 
                 ):

        CT.CustomTreeCtrl.__init__(self, parent, -1, pos, size, style, agwStyle)
        self.SetBackgroundColour(wx.WHITE)
        
        #
        # Le panel contenant les panel de propriétés des éléments de séquence
        #
        self.panelProp = panelProp

        #
        # La classe 
        #
        self.classe = classe
        
        #
        # On instancie un panel de propriétés vide pour les éléments qui n'ont pas de propriétés
        #
        self.panelVide = PanelPropriete(self.panelProp)
        self.panelVide.Hide()
        
        #
        # Construction de l'arbre
        #
        root = self.AddRoot("")
        self.classe.ConstruireArbre(self, root)
        self.root = root
        
        self.itemDrag = None
        
        #
        # Gestion des évenements
        #
        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(CT.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightDown)
        self.Bind(CT.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
        self.Bind(CT.EVT_TREE_END_DRAG, self.OnEndDrag)
        self.Bind(wx.EVT_MOTION, self.OnMove)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        
        self.ExpandAll()
        
        
#    ####################################################################################
#    def SelectItem(self, item, select=True):
#        if select:
#            CT.CustomTreeCtrl.SelectItem(self, item, False)
#        CT.CustomTreeCtrl.SelectItem(self, item, select)


    ####################################################################################
    def OnSelChanged(self, event):
        self.item = event.GetItem()
        data = self.GetItemPyData(self.item)
        if data == None:
            panelPropriete = self.panelVide
        else:
            if isinstance(data, wx.Panel):
                panelPropriete = data
            else:
                panelPropriete = data.panelPropriete

        if hasattr(self.classe.doc.GetApp(), 'fiche') and self.classe.doc.centrer:
            self.classe.doc.GetApp().fiche.CentrerSur(data)
        self.classe.doc.centrer = True
        
        self.panelProp.AfficherPanel(panelPropriete)
        
#        wx.CallAfter(panelPropriete.Refresh)
        event.Skip()
        
    ####################################################################################
    def OnBeginDrag(self, event):
        self.itemDrag = event.GetItem()
        if self.item:
            event.Allow()

        
        
        
        

####################################################################################
#
#   Classe définissant l'arbre de structure de la séquence
#
####################################################################################
class ArbreSequence(ArbreDoc):
    def __init__(self, parent, sequence, classe, panelProp):

        ArbreDoc.__init__(self, parent, classe, panelProp)
        
        self.parent = parent
        
        #
        # La séquence 
        #
        self.sequence = sequence
        
        #
        # Les icones des branches
        #
        self.images = {}
        il = wx.ImageList(20, 20)
        for k, i in constantes.dicimages.items() + constantes.imagesSeance.items():
            self.images[k] = il.Add(i.GetBitmap())
        self.AssignImageList(il)
        
        
        #
        # Construction de l'arbre
        #
        self.sequence.ConstruireArbre(self, self.root)
        
        
        self.panelProp.AfficherPanel(self.sequence.panelPropriete)

        self.CurseurInsert = wx.CursorFromImage(constantes.images.CurseurInsert.GetImage())
        
    ###############################################################################################
    def OnKey(self, evt):
        keycode = evt.GetKeyCode()
        if keycode == wx.WXK_DELETE:
            item = self.GetSelection()
            self.sequence.SupprimerItem(item)
            
        
    ####################################################################################
    def AjouterObjectif(self, event = None):
        self.sequence.AjouterObjectif()
        
        
    ####################################################################################
    def SupprimerObjectif(self, event = None, item = None):
        self.sequence.SupprimerObjectif(item)

            
    ####################################################################################
    def AjouterSeance(self, event = None):
        seance = self.sequence.AjouterSeance()
        self.lstSeances.append(self.AppendItem(self.seances, u"Séance :", data = seance))
        
    ####################################################################################
    def AjouterRotation(self, event = None, item = None):
        seance = self.sequence.AjouterRotation(self.GetItemPyData(item))
        self.SetItemText(item, u"Rotation")
        self.lstSeances.append(self.AppendItem(item, u"Séance :", data = seance))
        
    ####################################################################################
    def AjouterSerie(self, event = None, item = None):
        seance = self.sequence.AjouterRotation(self.GetItemPyData(item))
        self.SetItemText(item, u"Rotation")
        self.lstSeances.append(self.AppendItem(item, u"Séance :", data = seance))
        
    ####################################################################################
    def SupprimerSeance(self, event = None, item = None):
        if self.sequence.SupprimerSeance(self.GetItemPyData(item)):
            self.lstSeances.remove(item)
            self.Delete(item)


    ####################################################################################
    def OnRightDown(self, event):
        item = event.GetItem()
        self.sequence.AfficherMenuContextuel(item)

    
    ####################################################################################
    def OnLeftDClick(self, event):
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        if item:
            self.sequence.AfficherLien(item)
        event.Skip()                
        

    ####################################################################################
    def OnCompareItems(self, item1, item2):
        i1 = self.GetItemPyData(item1)
        i2 = self.GetItemPyData(item2)
        return i1.ordre - i2.ordre

    ####################################################################################
    def OnMove(self, event):
        if self.itemDrag != None:
            (id, flag) = self.HitTest(wx.Point(event.GetX(), event.GetY()))
            if id != None:
                dataTarget = self.GetItemPyData(id)
                dataSource = self.GetItemPyData(self.itemDrag)
                if not isinstance(dataSource, Seance):
                    self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
                else:
                    if not isinstance(dataTarget, Seance):
                        if dataTarget == self.sequence.panelSeances:
                            self.SetCursor(self.CurseurInsert)
                        else:
                            self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
                    else:
                        if dataTarget != dataSource:# and dataTarget.parent == dataSource.parent:
                            self.SetCursor(self.CurseurInsert)
                        else:
                            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
                        
        event.Skip()
        
        
    ####################################################################################
    def OnEndDrag(self, event):
        """ Gestion des glisser-déposer
        """
        self.item = event.GetItem() 
        dataTarget = self.GetItemPyData(self.item)
        dataSource = self.GetItemPyData(self.itemDrag)
        if dataTarget == self.sequence.panelSeances:
            dataTarget = self.sequence.seance[0]
            self.item = self.GetFirstChild(self.item)[0]
            root = True
        else:
            root = False
            
        if isinstance(dataSource, Seance) and isinstance(dataTarget, Seance)  and dataTarget != dataSource:
            
            # source et target ont le même parent (même niveau dans l'arbre)
            if dataTarget.parent == dataSource.parent:
                
                if dataTarget.typeSeance in ["R","S"]:# rotation ou parallele
                    if not dataSource in dataTarget.sousSeances:
                        if isinstance(dataSource.parent, Sequence):# Niveau 0
                            lstS = dataSource.parent.seance
                        else:
                            lstS = dataSource.parent.sousSeances
                        lstT = dataTarget.sousSeances
                        s = lstS.index(dataSource)
                        lstT.insert(0, lstS.pop(s))
                        dataSource.parent = dataTarget
                        self.sequence.OrdonnerSeances()
                        self.sequence.reconstruireBrancheSeances(dataSource.parent, dataTarget)
                        self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
                    
                else:
                    if isinstance(dataTarget.parent, Sequence):# Niveau 0
                        lst = dataTarget.parent.seance
                    else:
                        lst = dataTarget.parent.sousSeances

                    s = lst.index(dataSource)
                    if root:
                        t = -1
                    else:
                        t = lst.index(dataTarget)
                    
                    if t > s:
                        lst.insert(t, lst.pop(s))
                    else:
                        lst.insert(t+1, lst.pop(s))
                       
                    self.sequence.OrdonnerSeances() 
                    self.SortChildren(self.GetItemParent(self.item))
                    self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
            
            # source et target ont des parents différents
            elif dataTarget.parent != dataSource.parent:
                if isinstance(dataTarget.parent, Sequence):
                    lstT = dataTarget.parent.seance
                else:
                    lstT = dataTarget.parent.sousSeances
                    if len(lstT) > 0:
                        dataSource.duree.v[0] = lstT[0].GetDuree()
                
                if isinstance(dataSource.parent, Sequence):
                    lstS = dataSource.parent.seance
                else:
                    lstS = dataSource.parent.sousSeances

                s = lstS.index(dataSource)
                if root:
                    t = -1
                else:
                    t = lstT.index(dataTarget)
                lstT[t+1:t+1] = [dataSource]
                del lstS[s]
                p = dataSource.parent
                dataSource.parent = dataTarget.parent
                self.sequence.OrdonnerSeances()
                self.sequence.reconstruireBrancheSeances(dataTarget.parent, p)
                self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
            else:
                pass
            
        self.itemDrag = None
        event.Skip()            

    
    ####################################################################################
    def OnToolTip(self, event):

        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))

        
    
####################################################################################
#
#   Classe définissant l'arbre de structure d'un projet
#
####################################################################################
class ArbreProjet(ArbreDoc):
    def __init__(self, parent, projet, classe, panelProp):

        ArbreDoc.__init__(self, parent, classe, panelProp)
        
        self.parent = parent
        
        #
        # La séquence 
        #
        self.projet = projet
        
        #
        # Les icones des branches
        #
        self.images = {}
        il = wx.ImageList(20, 20)
        for k, i in constantes.imagesProjet.items() + constantes.imagesTaches.items():
            self.images[k] = il.Add(i.GetBitmap())
        self.AssignImageList(il)
        
        #
        # Construction de l'arbre
        #
        self.projet.ConstruireArbre(self, self.root)
        
        self.panelProp.AfficherPanel(self.projet.panelPropriete)

        self.CurseurInsert = wx.CursorFromImage(constantes.images.CurseurInsert.GetImage())
        
    ###############################################################################################
    def OnKey(self, evt):
        keycode = evt.GetKeyCode()
        if keycode == wx.WXK_DELETE:
            item = self.GetSelection()
            self.projet.SupprimerItem(item)
            
        
    ####################################################################################
    def AjouterEleve(self, event = None):
        self.projet.AjouterEleve()
        
        
    ####################################################################################
    def SupprimerEleve(self, event = None, item = None):
        self.projet.SupprimerEleve(item)

            
    ####################################################################################
    def AjouterTache(self, event = None):
        tache = self.projet.AjouterTache()
        self.lstTaches.append(self.AppendItem(self.taches, u"Tâche :", data = tache))
        
    ####################################################################################
    def SupprimerTache(self, event = None, item = None):
        if self.projet.SupprimerTache(self.GetItemPyData(item)):
            self.lstTaches.remove(item)
            self.Delete(item)

    ####################################################################################
    def Ordonner(self, item):
        self.SortChildren(item)

    ####################################################################################
    def OnRightDown(self, event):
        item = event.GetItem()
        self.projet.AfficherMenuContextuel(item)

    
    ####################################################################################
    def OnLeftDClick(self, event):
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        if item:
            self.projet.AfficherLien(item)
        event.Skip()                
        

    ####################################################################################
    def OnCompareItems(self, item1, item2):
        i1 = self.GetItemPyData(item1)
        i2 = self.GetItemPyData(item2)
        return i1.ordre - i2.ordre
#        if i1.phase == i2.phase:
#            
#        else:
#            if i1.phase == "":
#                return -1
#            elif i2.phase == "":
#                return 1
#            else:
#                if i1.phase[0] > i2.phase[0]:
#                    return 1
#                else:
#                    return -1
        

    ####################################################################################
    def OnMove(self, event):
        if self.itemDrag != None:
            (id, flag) = self.HitTest(wx.Point(event.GetX(), event.GetY()))
            if id != None:
                dataTarget = self.GetItemPyData(id)
                dataSource = self.GetItemPyData(self.itemDrag)
                if not isinstance(dataSource, Tache):
                    self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
                else:
                    if not isinstance(dataTarget, Tache) \
                        or (dataTarget.phase != dataSource.phase and dataSource.phase !="Rev"):
                        self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
                    else:
                        if dataTarget != dataSource:# and dataTarget.parent == dataSource.parent:
                            self.SetCursor(self.CurseurInsert)
                        else:
                            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
                        
        event.Skip()
        
        
    ####################################################################################
    def OnEndDrag(self, event):
        self.item = event.GetItem()
        dataTarget = self.GetItemPyData(self.item)
        dataSource = self.GetItemPyData(self.itemDrag)
        if not isinstance(dataSource, Tache):
            pass
        else:
            if not isinstance(dataTarget, Tache):
                pass
            else:
                if dataTarget != dataSource \
                    and (dataTarget.phase == dataSource.phase or dataSource.phase =="Rev"):
                    lst = dataTarget.parent.taches

                    s = lst.index(dataSource)
                    t = lst.index(dataTarget)
                    
                    if t > s:
                        lst.insert(t, lst.pop(s))
                    else:
                        lst.insert(t+1, lst.pop(s))
                    dataTarget.parent.SetOrdresTaches()
                    self.SortChildren(self.GetItemParent(self.item))
                    self.panelVide.sendEvent(self.projet) # Solution pour déclencher un "redessiner"
    
                else:
                    pass
        self.itemDrag = None
        event.Skip()            

    
    ####################################################################################
    def OnToolTip(self, event):

        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))






            



class ArbreSavoirs(CT.CustomTreeCtrl):
    def __init__(self, parent, savoirs, prerequis):

        CT.CustomTreeCtrl.__init__(self, parent, -1, 
                                   agwStyle = wx.TR_DEFAULT_STYLE|wx.TR_MULTIPLE|wx.TR_HIDE_ROOT|CT.TR_AUTO_CHECK_CHILD|CT.TR_AUTO_CHECK_PARENT)
        
        self.parent = parent
        self.savoirs = savoirs
        
        typeEns = savoirs.GetTypeEnseignement()
        
        root = self.AddRoot(u"")
        
        if typeEns == "SSI":
            t = u"Capacités "
        else:
            t = u"Savoirs "
        self.root = self.AppendItem(root, t+typeEns)
        self.SetItemBold(self.root, True)
        self.Construire(self.root, constantes.dicSavoirs[typeEns])
        
        if prerequis and typeEns!="ET" and typeEns!="SSI":
            self.rootET = self.AppendItem(root, u"Savoirs ETT")
            self.SetItemBold(self.rootET, True)
            self.SetItemItalic(self.rootET, True)
            self.Construire(self.rootET, constantes.dicSavoirs['ET'], et = True)
        
        
        self.ExpandAll()
        
        #
        # Les icones des branches
        #
#        dicimages = {"Seq" : images.Icone_sequence,
#                       "Rot" : images.Icone_rotation,
#                       "Cou" : images.Icone_cours,
#                       "Com" : images.Icone_competence,
#                       "Obj" : images.Icone_objectif,
#                       "Ci" : images.Icone_centreinteret,
#                       "Eva" : images.Icone_evaluation,
#                       "Par" : images.Icone_parallele
#                       }
#        self.images = {}
#        il = wx.ImageList(20, 20)
##        for k, i in dicimages.items():
##            self.images[k] = il.Add(i.GetBitmap())
#        self.AssignImageList(il)
        
        
        #
        # Gestion des évenements
        #
#        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnItemCheck)
    
        
    def Construire(self, branche, dic, et = False, grosseBranche = True):
        """ Construction d'une branche de "savoirs"
            <et> = prérequis ETT pour spécialité STI2D
        """
        clefs = constantes.trier(dic.keys())
        for k in clefs:
            if type(dic[k][1]) == list:
                toolTip = u" \u25CF ".join(dic[k][1])
            else:
                toolTip = None
            b = self.AppendItem(branche, k+" "+dic[k][0], ct_type=1, data = toolTip)
            
            if et:
                self.SetItemItalic(b, True)
            if grosseBranche:
                self.SetItemBold(b, True)
            
            if type(dic[k][1]) == dict:
                self.Construire(b, dic[k][1], et, grosseBranche = False)

        
    def OnItemCheck(self, event):
        item = event.GetItem()
        code = self.GetItemText(item).split()[0]
        if self.IsItalic(item):
            code = '_'+code
        if item.GetValue():
            self.parent.savoirs.savoirs.append(code)
        else:
            self.parent.savoirs.savoirs.remove(code)
        self.parent.SetSavoirs()
        event.Skip()
        
        
    def OnGetToolTip(self, event):
        toolTip = event.GetItem().GetData()
        if toolTip != None:
            event.SetToolTip(wx.ToolTip(toolTip))

        
    def traverse(self, parent=None):
        if parent is None:
            parent = self.GetRootItem()
        nc = self.GetChildrenCount(parent, True)

        def GetFirstChild(parent, cookie):
            return self.GetFirstChild(parent)
        
        GetChild = GetFirstChild
        cookie = 1
        for i in range(nc):
            child, cookie = GetChild(parent, cookie)
            GetChild = self.GetNextChild
            yield child
            

    def get_item_by_label(self, search_text, root_item):
        item, cookie = self.GetFirstChild(root_item)
    
        while item != None and item.IsOk():
            text = self.GetItemText(item)
            if text.split()[0] == search_text:
                return item
            if self.ItemHasChildren(item):
                match = self.get_item_by_label(search_text, item)
                if match.IsOk():
                    return match
            item, cookie = self.GetNextChild(root_item, cookie)
    
        return wx.TreeItemId()


class ArbreCompetences(HTL.HyperTreeList):
    def __init__(self, parent, type_ens, pptache = None, agwStyle = CT.TR_HIDE_ROOT|CT.TR_HAS_VARIABLE_ROW_HEIGHT):#|CT.TR_AUTO_CHECK_CHILD):#|HTL.TR_NO_HEADER):
        
        HTL.HyperTreeList.__init__(self, parent, -1, style = wx.WANTS_CHARS, agwStyle = agwStyle)#wx.TR_DEFAULT_STYLE|
        
        self.parent = parent
        if pptache == None:
            self.pptache = parent
        else:
            self.pptache = pptache
        self.type_ens = type_ens
        
        self.items = {}
        
        self.AddColumn(u"Compétences")
        self.SetMainColumn(0) # the one with the tree in it...
        self.AddColumn(u"")
        self.SetColumnWidth(1, 0)
        self.root = self.AddRoot(u"Compétences")
        self.MiseAJourTypeEnseignement(type_ens)
        
        self.ExpandAll()
        
#        il = wx.ImageList(20, 20)
#        self.AssignImageList(il)
        
        #
        # Gestion des évenements
        #
#        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnItemCheck)
        self.Bind(wx.EVT_SIZE, self.OnSize2)
        
    #############################################################################
    def MiseAJourTypeEnseignement(self, type_ens):
#        print "MiseAJourTypeEnseignement"
        self.type_ens = type_ens
        self.DeleteChildren(self.root)
        self.Construire(self.root, type_ens = type_ens)
        self.ExpandAll()
#        self.Layout()
        
    
    
    #############################################################################
    def MiseAJourPhase(self, phase):
        self.DeleteChildren(self.root)
        self.Construire(self.root)
        self.ExpandAll()
        
    
    ####################################################################################
    def OnSize2(self, evt):
        w = self.GetClientSize()[0]-17-self.GetColumnWidth(1)
        if w != self.GetColumnWidth(0):
            self.SetColumnWidth(0, w)
            if self.IsShown():
                self.wrap(w)
        evt.Skip()
        
    ####################################################################################
    def wrap(self,w):
        item = self.GetRootItem()
        while 1:
            item = self.GetNext(item)
            if item == None:
                break
             
            # Coefficient pour le texte en gras (plus large)
            # Et position en X du texte
            if item._type == 0:
                W = w*0.93 - 5
            else:
                W = w - 35
                
            text = self.GetItemText(item, 0).replace("\n", "")
            text = wordwrap(text, W, wx.ClientDC(self))

            self.SetItemText(item, text, 0)
        
    ####################################################################################
    def Construire(self, branche, dic = None, type_ens = None, ct_type = 0):
        if dic == None:
            dic = constantes.dicCompetences[type_ens]
        clefs = dic.keys()
        clefs.sort()
        for k in clefs:
            if type(dic[k]) == list and type(dic[k][1]) == dict:#len(dic[k])>1
                b = self.AppendItem(branche, k+" "+dic[k][0], ct_type=ct_type, data = k)
                self.Construire(b, dic[k][1], ct_type = 1)
            else:
                b = self.AppendItem(branche, k+" "+dic[k], ct_type = 1, data = k)
            
            if ct_type == 0:
                self.SetItemBold(b, True)
        
    ####################################################################################
    def OnItemCheck(self, event, item = None):
        if event != None:
            item = event.GetItem()
        
        code = self.GetItemPyData(item)#.split()[0]

        if code != None: # un seul indicateur séléctionné
            self.AjouterEnleverCompetences([item])

        else:       # une compérence séléctionnée
            self.AjouterEnleverCompetences(item.GetChildren())
        
        event.Skip()
        wx.CallAfter(self.pptache.SetCompetences)
        
        

    ####################################################################################
    def AjouterEnleverCompetences(self,lstitem):
        for item in lstitem:
            code = self.GetItemPyData(item)#.split()[0]
#            print code, item.GetValue()
            if item.GetValue():
                self.pptache.AjouterCompetence(code)
            else:
                self.pptache.EnleverCompetence(code)
    
    ####################################################################################
    def traverse(self, parent=None):
        if parent is None:
            parent = self.GetRootItem()
        nc = self.GetChildrenCount(parent, True)

        def GetFirstChild(parent, cookie):
            return self.GetFirstChild(parent)
        
        GetChild = GetFirstChild
        cookie = 1
        for i in range(nc):
            child, cookie = GetChild(parent, cookie)
            GetChild = self.GetNextChild
            yield child
            
    ####################################################################################
    def get_item_by_label(self, search_text, root_item):
        item, cookie = self.GetFirstChild(root_item)
    
        while item != None and item.IsOk():
            text = self.GetItemText(item)
            if text.split()[0] == search_text:
                return item
            if self.ItemHasChildren(item):
                match = self.get_item_by_label(search_text, item)
                if match.IsOk():
                    return match
            item, cookie = self.GetNextChild(root_item, cookie)
    
        return wx.TreeItemId()



class ArbreCompetencesPrj(ArbreCompetences):
    def __init__(self, parent, type_ens, pptache, revue = False):
        self.revue = revue
        ArbreCompetences.__init__(self, parent, type_ens, pptache,
                                  agwStyle = CT.TR_HIDE_ROOT|CT.TR_HAS_VARIABLE_ROW_HEIGHT|CT.TR_ROW_LINES|CT.TR_ALIGN_WINDOWS|CT.TR_AUTO_CHECK_CHILD|CT.TR_AUTO_CHECK_PARENT|CT.TR_AUTO_TOGGLE_CHILD)#|CT.TR_ELLIPSIZE_LONG_ITEMS)#|CT.TR_TOOLTIP_ON_LONG_ITEMS)#
        self.Bind(wx.EVT_SIZE, self.OnSize2)
        self.Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        
        self.SetColumnText(0,u"Compétences et indicateurs")
        self.SetColumnText(1, u"Poids")
        self.SetColumnWidth(1, 60)
        
#        self.Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        
       
    

    ####################################################################################
    def Construire(self, branche, dic = None, type_ens = None):
#        print "Construire", self.pptache.tache.phase, type_ens
        if type_ens == None:
            type_ens = self.type_ens
        if dic == None: # Construction de la racine
            dic = constantes.dicCompetences_prj[type_ens]
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False)
#        self.poids_ctrl = {}
        clefs = dic.keys()
        clefs.sort()
        for codeGrp in clefs:
#            self.poids_ctrl[codeGrp] = wx.TextCtrl(self, -1, 
#                                                   str(constantes.dicPoidsIndicateurs[type_ens][codeGrp][0])+"%", 
#                                                   size = (32,20), name = codeGrp)
            b = self.AppendItem(branche, codeGrp+" "+dic[codeGrp][0])
            self.SetItemText(b, str(constantes.dicPoidsIndicateurs[type_ens][codeGrp][0])+"%", 1)
            self.SetItemBold(b, True)
#            self.poids_ctrl[codeGrp].Bind(wx.EVT_TEXT, self.OnTextCtrl)
#            self.SetItemWindow(b, self.poids_ctrl[codeGrp], 1)
            
            codes = dic[codeGrp][1].keys()
            codes.sort()
            for code in codes:
                intitule = dic[codeGrp][1][code]
                
                if type(intitule) == list: # C'est le cas des compétences SSI
                    intitule = intitule[0] + " : " + u" \u25CF ".join(intitule[1].values())
                
                c = self.AppendItem(b, code+" "+intitule, ct_type=1)
                i = None
                for j, Indic in enumerate(constantes.dicIndicateurs[type_ens][code]):
                    codeIndic = code+'_'+str(j+1)
                    if self.pptache.tache.phase != "R1" or codeIndic in self.pptache.tache.indicateursMaxi:
#                        self.poids_ctrl[codeIndic] = wx.TextCtrl(self, -1, 
#                                                                 str(constantes.dicPoidsIndicateurs[type_ens][codeGrp][1][code][j])+"%", 
#                                                                 size = (32,18), name = codeIndic)
#                        self.poids_ctrl[codeIndic] = wx.StaticText(self, -1, 
#                                                                 str(constantes.dicPoidsIndicateurs[type_ens][codeGrp][1][code][j])+"%", 
#                                                                 size = (32,18), name = codeIndic)
#                        self.AppendItem(c, str(constantes.dicPoidsIndicateurs[type_ens][codeGrp][1][code][j])+"%", 1)
#                        self.poids_ctrl[codeIndic].Bind(wx.EVT_TEXT, self.OnTextCtrl)

                        if not Indic[1] or self.pptache.tache.phase != 'XXX':
                            i = self.AppendItem(c, Indic[0], ct_type=1, data = codeIndic)
                            if codeIndic in self.pptache.tache.indicateurs:
                                self.CheckItem2(i)
                            self.SetItemText(i, str(constantes.dicPoidsIndicateurs[type_ens][codeGrp][1][code][j])+"%", 1)
                            self.SetItemFont(i, font)
                            if Indic[1]:
                                self.SetItemTextColour(i, constantes.COUL_REVUE)
                            else:
                                self.SetItemTextColour(i, constantes.COUL_SOUT)
    #                        self.SetItemWindow(i, self.poids_ctrl[codeIndic], 1)
                            self.items[codeIndic] = i
                
                if i == None:
                    self.SetItemType(c,0)

        

#    #############################################################################
#    def OnTextCtrl(self, evt):
#        return
#        c = evt.GetEventObject()
#        k = c.GetName()
#        try:
#            s = eval(evt.GetString())
#            c.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
#            c.Refresh()
#        except:
#            c.SetBackgroundColour("pink")
#            c.Refresh()
#            return
#        self.pptache.tache.indicateurs[k] = s
##        constantes.dicCompetences_prj_simple[self.type_ens][k][1] = s
##        self.parent.GetDocument().MiseAJourPoidsCompetences(k)
#        self.pptache.sendEvent()

        
    #############################################################################
    def OnToolTip(self, event):
        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))
            
            
#    #############################################################################
#    def MiseAJour(self, code = None, value = None):
#        return
#        if code == None:
#            for k, v in constantes.dicCompetences_prj_simple[self.type_ens].items():
#                if k in self.poids_ctrl.keys():
#                    self.poids_ctrl[k].ChangeValue(str(v[1]))
#        else:
#            self.poids_ctrl[code].ChangeValue(str(value))
            
#    #############################################################################
#    def MiseAJourTypeEnseignement(self, type_ens):
#        self.type_ens = type_ens
#        self.DeleteChildren(self.root)
#        self.Construire(self.root, type_ens = type_ens)
#        self.ExpandAll()
            
            
#class ArbreIndicateursPrj(wx.CheckListBox):
#    def __init__(self, parent):
#        
#        wx.CheckListBox.__init__(self, parent, -1)
#        
#        self.parent = parent
#        
#        
#    
#        
##    ####################################################################################
##    def Construire(self, type_ens, competence = None):
##        dic = constantes.dicIndicateurs[competence]
##        clefs = dic.keys()
##        clefs.sort()
##        for k in clefs:
##            b = self.AppendItem(branche, k+" "+dic[k][0], ct_type=ct_type)
##            if len(dic[k])>1 and type(dic[k][1]) == dict:
##                self.Construire(b, dic[k][1], ct_type=1)
##            
##            if ct_type == 0:
##                self.SetItemBold(b, True)
#        
#    ####################################################################################
#    def OnItemCheck(self, event):
#        item = event.GetItem()
#        code = self.GetItemText(item).split()[0]
#        if item.GetValue():
#            self.parent.AjouterCompetence(code)
#        else:
#            self.parent.EnleverCompetence(code)
#        self.parent.SetCompetences()
#        event.Skip()
#
#    ####################################################################################
#    def traverse(self, parent=None):
#        if parent is None:
#            parent = self.GetRootItem()
#        nc = self.GetChildrenCount(parent, True)
#
#        def GetFirstChild(parent, cookie):
#            return self.GetFirstChild(parent)
#        
#        GetChild = GetFirstChild
#        cookie = 1
#        for i in range(nc):
#            child, cookie = GetChild(parent, cookie)
#            GetChild = self.GetNextChild
#            yield child
#            
#    ####################################################################################
#    def get_item_by_label(self, search_text, root_item):
#        item, cookie = self.GetFirstChild(root_item)
#    
#        while item != None and item.IsOk():
#            text = self.GetItemText(item)
#            if text.split()[0] == search_text:
#                return item
#            if self.ItemHasChildren(item):
#                match = self.get_item_by_label(search_text, item)
#                if match.IsOk():
#                    return match
#            item, cookie = self.GetNextChild(root_item, cookie)
#    
#        return wx.TreeItemId()      
            
            
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

##
## Fonction pour vérifier si deux listes sont égales ou pas
##
#def listesEgales(l1, l2):
#    if len(l1) != len(l2):
#        return False
#    else:
#        for e1, e2 in zip(l1,l2):
#            if e1 != e2:
#                return False
#    return True

#
# Fonction pour vérifier si un point x, y est dans un rectangle (x0, y0, x1, y1)
#
def dansRectangle(x, y, rect):
    """ Renvoie True si le point x, y est dans un des rectangles de la liste de rectangles r(xr, yr, wr, hr)
    """
    for i, r in enumerate(rect):
        if x > r[0] and y > r[1] and x < r[0] + r[2] and y < r[1] + r[3]:
            return True, i
    return False, 0



def get_key(dic, value):
    """ Renvoie la clef du dictionnaire <dic> correspondant à la valeur <value>
    """
    i = 0
    continuer = True
    while continuer:
        if i > len(dic.keys()):
            continuer = False
        else:
            if dic.values()[i] == value:
                continuer = False
                key = dic.keys()[i]
            i += 1
    return key





####################################################################################
#
#   Classe définissant l'application
#    --> récupération des paramétres passés en ligne de commande
#
####################################################################################
#from asyncore import dispatcher, loop
#import sys, time, socket, threading

class SeqApp(wx.App):
    def OnInit(self):
        fichier = ""
        if len(sys.argv)>1: # un paramètre a été passé
            parametre = sys.argv[1]

#           # on verifie que le fichier passé en paramètre existe
            if os.path.isfile(parametre):
                fichier = unicode(parametre, FILE_ENCODING)

        
        frame = FenetrePrincipale(None, fichier)
        frame.Show()
        
        if server != None:
            server.app = frame
        
        self.SetTopWindow(frame)
        return True



##########################################################################################################
#
#  Dialogue de sélection d'URL
#
##########################################################################################################
class URLDialog(wx.Dialog):
    def __init__(self, parent, lien, pathseq):
        wx.Dialog.__init__(self, parent, -1)
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, -1, u"Sélection de lien")

        self.PostCreate(pre)

        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, u"Sélectionner un fichier, un dossier ou une URL")
        label.SetHelpText(u"Sélectionner un fichier, un dossier ou une URL")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Lien :")
#        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        url = URLSelectorCombo(self, lien, pathseq)
#        text.SetHelpText("Here's some help text for field #1")
        box.Add(url, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.url = url
        
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


    ######################################################################################  
    def GetURL(self):
        return self.url.GetPath()


    ######################################################################################  
    def OnPathModified(self, lien):
        return



    
class URLSelectorCombo(wx.Panel):
    def __init__(self, parent, lien, pathseq):
        wx.Panel.__init__(self, parent, -1)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.texte = wx.TextCtrl(self, -1, lien.path, size = (300, -1))
        bt1 =wx.BitmapButton(self, 100, wx.ArtProvider_GetBitmap(wx.ART_FOLDER))
        bt1.SetToolTipString(u"Sélectionner un dossier")
        bt2 =wx.BitmapButton(self, 101, wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE))
        bt2.SetToolTipString(u"Sélectionner un fichier")
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt1)
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.texte)
        
        sizer.Add(self.texte,flag = wx.EXPAND)
        sizer.Add(bt1)
        sizer.Add(bt2)
        
        self.SetSizerAndFit(sizer)
        self.lien = lien
        self.SetPathSeq(pathseq)

    # Overridden from ComboCtrl, called when the combo button is clicked
    def OnClick(self, event):
        
        if event.GetId() == 100:
            dlg = wx.DirDialog(self, u"Sélectionner un dossier",
                          style=wx.DD_DEFAULT_STYLE,
                          defaultPath = self.pathseq
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
            if dlg.ShowModal() == wx.ID_OK:
                self.SetPath(dlg.GetPath())
    
            dlg.Destroy()
        else:
            dlg = wx.FileDialog(self, u"Sélectionner un fichier",
    #                           defaultPath = globdef.DOSSIER_EXEMPLES,
                               style = wx.DD_DEFAULT_STYLE
                               #| wx.DD_DIR_MUST_EXIST
                               #| wx.DD_CHANGE_DIR
                               )
    
            if dlg.ShowModal() == wx.ID_OK:
                self.SetPath(dlg.GetPath())
    
            dlg.Destroy()
        
        self.SetFocus()


    ##########################################################################################
    def EvtText(self, event):
        path = event.GetString()
        self.SetPath(path)


    ##########################################################################################
    def GetPath(self):
        return self.lien
    
    
    ##########################################################################################
    def SetPath(self, lien):
        """ lien doit être de type 'String'
        """
        
        self.lien.EvalLien(lien, self.pathseq)
        
        self.texte.ChangeValue(toDefautEncoding(self.lien.path)) # On le met en DEFAUT_ENCODING
#            self.texte.SetBackgroundColour(("white"))
#        else:
#            self.texte.SetBackgroundColour(("pink"))
        self.Parent.OnPathModified(self.lien)
        
        
    ##########################################################################################
    def SetPathSeq(self, pathseq):
        self.pathseq = pathseq



#############################################################################################################
#
# Pour convertir les images en texte
# 
#############################################################################################################
import base64
try:
    b64encode = base64.b64encode
except AttributeError:
    b64encode = base64.encodestring
    
import tempfile

def img2str(img):
    """
    """
    
    global app
    if not wx.GetApp():
        app = wx.PySimpleApp()
        
    # convert the image file to a temporary file
    tfname = tempfile.mktemp()
    try:
        img.SaveFile(tfname, wx.BITMAP_TYPE_PNG)
        data = b64encode(open(tfname, "rb").read())
    finally:
        if os.path.exists(tfname):
            os.remove(tfname)
            
    return data

#############################################################################################################
#
# Information PopUp
# 
#############################################################################################################
import cStringIO

class PopupInfo(wx.PopupWindow):
    def __init__(self, parent, titre = ""):
        wx.PopupWindow.__init__(self, parent, wx.BORDER_SIMPLE)
        self.parent = parent
        
        #
        # Un sizer "tableau", comme ça, on y met ce q'on veut où on veut ...
        #
        self.sizer = wx.GridBagSizer()
        
        #
        # Un titre
        #
        self.titre = wx.StaticText(self, -1, titre)
        font = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.titre.SetFont(font)
        self.sizer.Add(self.titre, (0,0), flag = wx.ALL|wx.ALIGN_CENTER, border = 5)
        
        self.SetSizerAndFit(self.sizer)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        
        
    
    ##########################################################################################
    def OnLeave(self, event):
        x, y = event.GetPosition()
        w, h = self.GetSize()
        if not ( x > 0 and y > 0 and x < w and y < h):
            self.Show(False)
        event.Skip()


    ##########################################################################################
    def SetTitre(self, titre):
        self.titre.SetLabel(titre)
        
        
    ##########################################################################################
    def CreerLien(self, position = (3,0), span = (1,1)):
        titreLien = wx.StaticText(self, -1, "")
        ctrlLien = wx.BitmapButton(self, -1, wx.NullBitmap)
        ctrlLien.Show(False)
        self.Bind(wx.EVT_BUTTON, self.OnClickLien, ctrlLien)
        sizerLien = wx.BoxSizer(wx.HORIZONTAL)
        sizerLien.Add(titreLien, flag = wx.ALIGN_CENTER_VERTICAL)
        sizerLien.Add(ctrlLien)
        self.sizer.Add(sizerLien, position, span, flag = wx.ALL, border = 5)
        return titreLien, ctrlLien

    ##########################################################################################
    def SetLien(self, lien, titreLien, ctrlLien):
        self.lien = lien # ATTENTION ! Cette façon de faire n'autorise qu'un seul lien par PopupInfo !
        if lien.type == "":
            ctrlLien.Show(False)
            titreLien.Show(False)
            ctrlLien.SetToolTipString(toDefautEncoding(lien.path))
        else:
            ctrlLien.SetToolTipString(toDefautEncoding(lien.path))
            if lien.type == "f":
                titreLien.SetLabel(u"Fichier :")
                ctrlLien.SetBitmapLabel(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE))
                ctrlLien.Show(True)
            elif lien.type == 'd':
                titreLien.SetLabel(u"Dossier :")
                ctrlLien.SetBitmapLabel(wx.ArtProvider_GetBitmap(wx.ART_FOLDER))
                ctrlLien.Show(True)
            elif lien.type == 'u':
                titreLien.SetLabel(u"Lien web :")
                ctrlLien.SetBitmapLabel(images.Icone_web.GetBitmap())
                ctrlLien.Show(True)
            elif lien.type == 's':
                titreLien.SetLabel(u"Fichier séquence :")
                ctrlLien.SetBitmapLabel(images.Icone_sequence.GetBitmap())
                ctrlLien.Show(True)
            self.Layout()
            self.Fit()
        
    ##########################################################################################
    def OnClickLien(self, evt):
        if self.parent.typ == 'seq':
            path = self.parent.sequence.GetPath()
        else:
            path = self.parent.projet.GetPath()
        self.lien.Afficher(path, self.parent.parent)
        
    ##########################################################################################
    def CreerImage(self, position = (4,0), span = (1,1), flag = wx.ALIGN_CENTER):
        image = wx.StaticBitmap(self, -1, wx.NullBitmap)
        image.Show(False)
        self.sizer.Add(image, position, span, flag = flag|wx.ALL, border = 5)
        return image
    
    ##########################################################################################
    def SetImage(self, image, ctrlImage):
        if image == None:
            ctrlImage.Show(False)
        else:
            ctrlImage.SetBitmap(image)
            ctrlImage.Show(True)
        self.Layout()
        self.Fit()
        
    
    ##########################################################################################
    def CreerTexte(self, position = (1,0), span = (1,1), txt = u"", flag = wx.ALIGN_CENTER):
        ctrlTxt = wx.StaticText(self, -1, txt)
        self.sizer.Add(ctrlTxt, position, span, flag = flag|wx.ALL, border = 5)
        self.Layout()
        self.Fit()
        return ctrlTxt
    
    ##########################################################################################
    def SetTexte(self, texte, ctrlTxt):
        if texte == "":
            ctrlTxt.Show(False)
        else:
            ctrlTxt.SetLabelMarkup(texte)
            ctrlTxt.Show(True)
            self.Layout()
            self.Fit()
    
    ##########################################################################################
    def CreerRichTexte(self, objet, position = (6,0), span = (1,1)):
        self.objet = objet # ATTENTION ! Cette façon de faire n'autorise qu'un seul objet par PopupInfo !
        self.rtp = richtext.RichTextPanel(self, objet, size = (300, 200))
        self.sizer.Add(self.rtp, position, span, flag = wx.ALL|wx.EXPAND, border = 5)
        self.SetRichTexte()
        return self.rtp
    
    ##########################################################################################
    def SetRichTexte(self):
        self.rtp.Show(self.objet.description != None)
        self.rtp.Ouvrir()
        self.Layout()
        self.Fit()
        
    ##########################################################################################
    def DeplacerItem(self, item, pos = None, span = None):
        if item == None:
            item = self.titre
        if pos != None:
            self.sizer.SetItemPosition(item, pos) 
        if span != None:
            self.sizer.SetItemSpan(item, span) 
        
        







#############################################################################################################
#
# Dialog pour choisir le type de document à créer
# 
#############################################################################################################
class DialogChoixDoc(wx.Dialog):
    def __init__(self, parent,
                 style=wx.DEFAULT_DIALOG_STYLE 
                 ):

        wx.Dialog.__init__(self, parent, -1, u"Créer ...", style = style, size = wx.DefaultSize)
        self.SetMinSize((200,100))
        sizer = wx.BoxSizer(wx.VERTICAL)
        button = wx.Button(self, -1, u"Nouvelle Séquence")
        button.SetToolTipString(u"Créer une nouvelle séquence pédagogique")
        button.SetBitmap(images.Icone_sequence.Bitmap,wx.LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnSeq, button)
        sizer.Add(button,0, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5)
        
        button = wx.Button(self, -1, u"Nouveau Projet")
        button.SetToolTipString(u"Créer un nouveau projet")
        button.SetBitmap(images.Icone_projet.Bitmap,wx.LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnPrj, button)
        sizer.Add(button,0,  wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5)
    
        self.SetSizer(sizer)
        sizer.Fit(self)
        
        self.SetReturnCode(0)
        

    def OnSeq(self, event):
        self.SetReturnCode(1)
        self.EndModal(1)

    def OnPrj(self, event):
        self.SetReturnCode(2)
        self.EndModal(2)

#import pywintypes
#############################################################################################################
#
# Fenetre de bilan d'objectifs
# 
#############################################################################################################
class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)
        self.Bind(wx.EVT_LEFT_UP, self.endDrag)
        self.Bind(wx.EVT_MOTION, self.onMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeave)

        self.idx = None

    def startDrag(self, e):

        self.idx = e.GetIndex()
        self.SetCursor(wx.CursorFromImage(constantes.images.CurseurInsert.GetImage()))

    def onLeave(self, event):
        if self.idx != None:
            self.Select(self.idx)
            self.idx = None
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()
        
    def onMove(self, event):    
        if self.idx != None:
            x = event.GetX()
            y = event.GetY()
            index, flags = self.HitTest((x, y))
            if index != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
                rect = self.GetItemRect(index)
                if y > rect.y + rect.height/2:
                    index += 1
                
                self.Select(index)
            

    def endDrag(self, event):    
        if self.idx != None:
            x = event.GetX()
            y = event.GetY()
            
            
            index, flags = self.HitTest((x, y))
            if index != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
                rect = self.GetItemRect(index)
                if y > rect.y + rect.height/2:
                    index += 1
                index += 1

                
                f = self.GetItemText(self.idx, 0)
                d = self.GetItemText(self.idx, 1)
                i = self.GetItemData(self.idx)

                pos = self.InsertStringItem(index, f)

                self.SetStringItem(pos, 1, d)
                self.SetItemData(index, i)
    #            self.itemDataMap[index] = self.itemDataMap[self.idx]
                
                if index > self.idx:
                    self.DeleteItem(self.idx)
    #                del self.itemDataMap[self.idx]
                else:
                    self.DeleteItem(self.idx+1)
    #                del self.itemDataMap[self.idx+1]
            
            self.idx = None
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        
        
        
class PanelListe(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent, fen):
        wx.Panel.__init__(self, parent, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.fen = fen
        
        self.il = wx.ImageList(16, 16)
        self.idx1 = self.il.Add(images.Icone_sequence.GetImage().Rescale(16,16).ConvertToBitmap())
        self.sm_up = self.il.Add(images.SmallUpArrow.GetBitmap())
        self.sm_dn = self.il.Add(images.SmallDnArrow.GetBitmap())
        
        
        self.listeSeq = TestListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL)
        self.currentItem = None
        self.listeSeq.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        sizer.Add(self.listeSeq, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        
        self.listeSeq.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.listeSeq)
        self.listeSeq.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
#        self.listeSeq.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        
        # for wxMSW
        self.listeSeq.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.listeSeq.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        
    def GetListCtrl(self):
        return self.listeSeq

    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)
    
    ########################################################################################################
    def OnResize(self, event=None):
        height = 30
        for indx in xrange(self.listeSeq.GetItemCount()):
            height += self.listeSeq.GetItemRect(indx).height
        self.listeSeq.SetMinSize((-1, height))
        
    ########################################################################################################
    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        event.Skip()
    
    ########################################################################################################
    def OnDoubleClick(self, event=None):
        nomFichier = self.GetSequence(self.currentItem).nomFichier
        self.fen.Parent.ouvrir(nomFichier)
        event.Skip()
        
    ########################################################################################################
    def OnRightDown(self, event):
        x = event.GetX()
        y = event.GetY()
        item, flags = self.listeSeq.HitTest((x, y))

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.listeSeq.Select(item)

        event.Skip()
        
    ########################################################################################################
    def OnRightClick(self, event):
        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID4"):
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID4, u"Supprimer")
        menu.Append(self.popupID5, u"Ouvrir")


        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def OnPopupFour(self, event):
        item = self.listeSeq.GetItem(self.currentItem)
        self.listeSeq.DeleteItem(self.currentItem)

    def OnPopupFive(self, event):
        self.OnDoubleClick(event)
        
        
    def GetSequence(self, num):
        return self.itemDataMap[self.listeSeq.GetItemData(num)][2]
    
    ########################################################################################################
    def MiseAJourListe(self, listSequences):
        self.listeSeq.ClearAll()
        self.listeSeq.InsertColumn(0, u"Fichier séquence")
        self.listeSeq.InsertColumn(1, u"Dossier")
    
        self.itemDataMap = {}
        for i, seq in enumerate(listSequences):
            f = seq.nomFichier
            d, f = os.path.split(f)
            f = os.path.splitext(f)[0]
            pos = self.listeSeq.InsertStringItem(i, f)
            self.listeSeq.SetStringItem(pos, 1, d)
            self.itemDataMap[i] = (f, d, seq)
            self.listeSeq.SetItemData(i, i)
            
        self.listeSeq.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.listeSeq.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.listeSeq.Layout()
        self.OnResize()
        self.Fit()
        
        listmix.ColumnSorterMixin.__init__(self, 2)
        
        
        
class FenetreBilan(wx.Frame):
    def __init__(self, parent, dossierCourant = '', typeEnseignement = "SSI"):
        wx.Frame.__init__(self, parent, -1, u"Synthèse pédagogique")
        
        self.sizer = wx.GridBagSizer()
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer()
        self.SetIcon(images.getlogoIcon())
        
        #############################################################################################
        # Création de la barre d'outils
        #############################################################################################
        self.ConstruireTb()
        
        self.lstClasse = []
        self.lstSeq = []
            
        #
        # Type d'enseignement
        #
        self.typeEnseignement = typeEnseignement
        l = []
        for i, e in enumerate(constantes.listEnseigmenent):
            l.append(constantes.Enseigmenent[e][0])
        rb = wx.RadioBox(
                panel, -1, u"Type d'enseignement", wx.DefaultPosition, (130,-1),
                l,
                1, wx.RA_SPECIFY_COLS
                )
        rb.SetToolTip(wx.ToolTip(u"Choisir le type d'enseignement"))
        for i, e in enumerate(constantes.listEnseigmenent):
            rb.SetItemToolTip(i, constantes.Enseigmenent[e][1])
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
            
        # Provosoirement uniquement pour SSI
        for i in [1,2,3,4]:
            rb.EnableItem(i, False)    
        
        self.sizer.Add(rb, (0,0), (2,1), flag = wx.EXPAND|wx.ALL)
        self.cb_type = rb
        self.cb_type.SetStringSelection(constantes.Enseigmenent[self.typeEnseignement][0])
        
        #
        # Dossiers de recherche
        #
        
        sb = wx.StaticBox(panel, -1, u"Dossiers où chercher les fichiers de séquence")
        sbs = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        self.dossiers = [os.path.abspath(dossierCourant)]
        self.dossiersOk = True
        self.txtDoss = wx.TextCtrl(panel, -1, os.path.abspath(dossierCourant))
        self.txtDoss.SetToolTipString(u"Saisir les dossiers de recherche, séparés par \";\"")
        self.txtDoss.Bind(wx.EVT_KILL_FOCUS, self.EvtTextDoss)
        sbs.Add(self.txtDoss, 1, flag = wx.EXPAND|wx.ALL)
        
        self.boutonDoss = wx.Button(panel, -1, "+", size = (30, -1))
        self.boutonDoss.SetToolTipString(u"Ajouter un dossier de recherche")
        self.Bind(wx.EVT_BUTTON, self.OnDossier, self.boutonDoss)
        sbs.Add(self.boutonDoss, flag = wx.EXPAND|wx.ALL)
        
        self.sizer.Add(sbs, (0,1), (1,1) , flag = wx.EXPAND|wx.ALL)
        self.sizer.AddGrowableCol(1)
        
        #
        #    Liste des fichiers trouvés
        #
        self.listeSeq = PanelListe(panel, self)

        self.sizer.Add(self.listeSeq, (1,1), (1,1) , flag = wx.EXPAND|wx.ALL)
        self.MiseAJourListe()
        
        panel.SetSizer(self.sizer)
        sizer.Add(panel, 1, flag = wx.EXPAND)
        
        self.SetSizerAndFit(sizer)
        
    ###############################################################################################
    def ConstruireTb(self):
        """ Construction de la ToolBar
        """
#        print "ConstruireTb"

        #############################################################################################
        # Création de la barre d'outils
        #############################################################################################
        self.tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        
        tsize = (24,24)
        new_bmp = images.Icone_excel.GetBitmap()
        
        self.tb.SetToolBitmapSize(tsize)
        
        self.tb.AddLabelTool(10, u"Exporter", new_bmp, 
                             shortHelp=u"Exporter la synthèse dans un fichier Excel", 
                             longHelp=u"Exporter la synthèse dans un fichier Excel")
        
        self.Bind(wx.EVT_TOOL, self.commandeExporter, id=10)    
        
        
        #################################################################################################################
        #
        # Mise en place
        #
        #################################################################################################################
        self.tb.Realize()
        

    ######################################################################################  
    def commandeExporter(self, event = None):
        mesFormats = "Fichier Excel|*.xlsx"
        dlg = wx.FileDialog(self, 
                            message = u"Enregistrement de la synthèse", 
                            defaultFile="", wildcard=mesFormats, 
                            style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR
                            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
            ok = self.enregistrer(path)
            if ok:
                dlg = wx.MessageDialog(self, u"Export de la synthèse réussi !", u"Export de la synthèse réussi",
                           wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                dlg = wx.MessageDialog(self, u"L'export de la synthèse a échoué !", u"Echec de l'export de la synthèse",
                           wx.OK | wx.ICON_WARNING)
                dlg.ShowModal()
                dlg.Destroy()
        else:
            dlg.Destroy()

    ######################################################################################  
    def enregistrer(self, nomFichier):
        fichierPP = constantes.fichierProgressionProgramme[self.typeEnseignement]
        try:
            tableau = grilles.PyExcel(os.path.join(TABLE_PATH, fichierPP))
        except:
            print fichierPP, "est déja ouvert !"
            return False

#        def ecrire(feuille, l, c):
#            v = tableau.getCell(feuille, l, c)
#            if v == "A":
#                v = "B"
#            elif v == "B":
#                v = "C"
#            elif v == "C":
#                v = "C"
#            else:
#                v = "A"
#            tableau.setCell(feuille, l, cc+i, v)
            
        feuilleP = u"Progression - Programme"
        feuilleS = u"Progression - Systèmes"
        
        # Première cellule "séquence"
        lcp, ccp = (4, 11) # K4
        lct, cct = (4, 15) # O4
        
        # Première cellule "durée"
        ldp, cdp = (5, 11) # K5
        
        # Première cellule "systèmes"
        lsp, csp = (8, 4) # D8
        lst, cst = (8, 8) # H8
        
        listePrem = []
        listeTerm = []

        
        for i in range(self.listeSeq.listeSeq.GetItemCount()):
            seq = self.listeSeq.GetSequence(i)
            if seq.position >= 4:
                listeTerm.append(seq)
            else:
                listePrem.append(seq)
        
#        listePrem = sorted(listePrem, key=lambda s: s.intitule)
#        listeTerm = sorted(listeTerm, key=lambda s: s.intitule)
        
        listeSystemes = []
        for i, seq in enumerate(listePrem + listeTerm):
            
            if seq in listePrem:
                c = ccp + i
                cs = csp + i
            else:
                c = cct + i - len(listePrem)
                cs = cst + i - len(listePrem)
                
            print seq.intitule, str(seq.GetDuree()), seq.nomFichier, i
            tableau.setCell(feuilleP, lcp, c, seq.intitule)
            tableau.setCell(feuilleP, ldp, c, str(seq.GetDuree()))
            tableau.setLink(feuilleP, lcp, c, seq.nomFichier)
            tableau.setCell(feuilleP, lcp-1, c, i+1)
            
            for sav in seq.obj["S"].savoirs:
                if sav in constantes.dicCellSavoirs[self.typeEnseignement].keys():
                    lig0, lig1 = constantes.dicCellSavoirs[self.typeEnseignement][sav]
                    for l in range(lig0, lig1+1):
                        tableau.setCell(feuilleP, l, c, "X")
                else:
                    continuer = True
                    s=1
                    while continuer:
                        sav1 = sav+'.'+str(s)
                        if sav1 in constantes.dicCellSavoirs[self.typeEnseignement].keys():
                            lig0, lig1 = constantes.dicCellSavoirs[self.typeEnseignement][sav1]
                            for l in range(lig0, lig1+1):
                                tableau.setCell(feuilleP, l, c, "X")
                            s += 1
                        else:
                            continuer = False
            
            #
            # Tableau "Systèmes"
            #
            nbrSystemes = seq.GetNbrSystemes()
            for syst in seq.systemes:
                # ligne du tableau correspondant au système
                if not syst.nom in listeSystemes:
                    listeSystemes.append(syst.nom)
                    l = lsp+len(listeSystemes)-1
                    tableau.setCell(feuilleS, l, 1, syst.nom)
                else:
                    l = lsp+listeSystemes.index(syst.nom)-1
                
                # nombre d'exemplaires du système utilisés dans la séquence
                if syst.nom in nbrSystemes.keys():
                    tableau.setCell(feuilleS, l, cs, nbrSystemes[syst.nom])
                
            #
            # Ajout éventuel de colonnes
            #
            if seq in listePrem:
                if len(listePrem) > 3 and i < len(listePrem) - 3:
                    tableau.insertPasteCol(feuilleP, c+1)
                    tableau.insertPasteCol(feuilleS, cs+1)
                    cct += 1
            else:
                if len(listeTerm) > 3 and i - len(listePrem) < len(listeTerm) - 3:
                    tableau.insertPasteCol(feuilleP, c+1)
                    tableau.insertPasteCol(feuilleS, c+1)
                
        try:                   
            tableau.save(nomFichier)
        except :
            print nomFichier, "est déja ouvert !"
            return False
            
        tableau.close()
        return True
        
    ######################################################################################  
    def EvtRadioBox(self, event):
        for c, e in constantes.Enseigmenent.items():
            if e[0] == self.cb_type.GetItemLabel(event.GetInt()):
                self.typeEnseignement = c
                self.MiseAJourListe()
                break
        
        
    #############################################################################            
    def EvtTextDoss(self, event):
        self.dossiers = self.txtDoss.GetValue().split(";")
        self.VerifierDossiers()
        self.MiseAJourListe()
        
        
    ########################################################################################################
    def OnDossier(self, event):
        dlg = wx.DirDialog(self, "Choisir un dossier",
                           style = wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )

        if dlg.ShowModal() == wx.ID_OK:
            if len(self.dossiers) == 0:
                self.txtDoss.ChangeValue(dlg.GetPath())
            else:
                self.txtDoss.ChangeValue(self.txtDoss.GetValue()+";"+dlg.GetPath())
            self.dossiers.append(dlg.GetPath())
            self.MiseAJourListe()
            
        dlg.Destroy()
        
        
    ########################################################################################################
    def VerifierDossiers(self):
        col = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        self.txtDoss.SetBackgroundColour(col)
        self.dossiersOk = True
        for dossier in self.dossiers:
            if not os.path.isdir(dossier):
                self.txtDoss.SetBackgroundColour("pink")
                self.dossiersOk = False
                break
    
    



        
    ########################################################################################################
    def MiseAJourListe(self):       
        if self.dossiersOk:
            wx.BeginBusyCursor()
            l = []
            for dossier in self.dossiers:
                l.extend(glob.glob(os.path.join(dossier, "*.seq")))
                
            listSequences = []
         
            for i, f in enumerate(l):
                classe, sequence = self.OuvrirFichierSeq(f)
                if classe != None and classe.typeEnseignement == self.typeEnseignement:
                    sequence.nomFichier = f
                    listSequences.append(sequence)
                  
            self.listeSeq.MiseAJourListe(listSequences)
            wx.EndBusyCursor()
        
        
        
    ########################################################################################################
    def OuvrirFichierSeq(self, nomFichier):
        fichier = open(nomFichier,'r')
#        print nomFichier
        classe = Classe(self.Parent)
        sequence = Sequence(self, classe)
        classe.SetDocument(sequence)
        
#        print fichier
        try:
            root = ET.parse(fichier).getroot()
            rsequence = root.find("Sequence")
            rclasse = root.find("Classe")
            classe.setBranche(rclasse)
            sequence.setBranche(rsequence)
            return classe, sequence
        except:
            print u"Le fichier n'a pas pu être ouvert :",nomFichier
#            messageErreur(self,u"Erreur d'ouverture",
#                          u"La séquence pédagogique\n    %s\n n'a pas pu être ouverte !" %nomFichier)
#            fichier.close()
#            self.Close()
            return None, None
                
                
                
                
##########################################################################################################
#
#  DirSelectorCombo
#
##########################################################################################################
class DirSelectorCombo(wx.combo.ComboCtrl):
    def __init__(self, *args, **kw):
        wx.combo.ComboCtrl.__init__(self, *args, **kw)

        # make a custom bitmap showing "..."
        bw, bh = 14, 16
        bmp = wx.EmptyBitmap(bw,bh)
        dc = wx.MemoryDC(bmp)

        # clear to a specific background colour
        bgcolor = wx.Colour(255,254,255)
        dc.SetBackground(wx.Brush(bgcolor))
        dc.Clear()

        # draw the label onto the bitmap
        label = "..."
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        tw,th = dc.GetTextExtent(label)
        dc.DrawText(label, (bw-tw)/2, (bw-tw)/2)
        del dc

        # now apply a mask using the bgcolor
        bmp.SetMaskColour(bgcolor)

        # and tell the ComboCtrl to use it
        self.SetButtonBitmaps(bmp, True)
        

    # Overridden from ComboCtrl, called when the combo button is clicked
    def OnButtonClick(self):
        # In this case we include a "New directory" button. 
#        dlg = wx.FileDialog(self, "Choisir un fichier modèle", path, name,
#                            "Rich Text Format (*.rtf)|*.rtf", wx.FD_OPEN)
        dlg = wx.DirDialog(self, _("Choisir un dossier"),
                           style = wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )

        # If the user selects OK, then we process the dialog's data.
        # This is done by getting the path data from the dialog - BEFORE
        # we destroy it. 
        if dlg.ShowModal() == wx.ID_OK:
            self.SetValue(dlg.GetPath())

        # Only destroy a dialog after you're done with it.
        dlg.Destroy()
        
        self.SetFocus()

    # Overridden from ComboCtrl to avoid assert since there is no ComboPopup
    def DoSetPopupControl(self, popup):
        pass


#############################################################################################################
#
# Message d'aide CI
# 
#############################################################################################################
try:
    from agw import genericmessagedialog as GMD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.genericmessagedialog as GMD

class MessageAideCI(GMD.GenericMessageDialog):
    def __init__(self, parent):
        GMD.GenericMessageDialog.__init__(self,  parent, 
                                  u"Informations à propos de la cible CI",
                                  u"Informations à propos de la cible CI",
                                   wx.OK | wx.ICON_QUESTION
                                   #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
        self.SetExtendedMessage(u"Afin que tous les CI apparaissent sur la cible,\n"\
                                  u"ils doivent cibler des domaines (MEI)\n"\
                                  u"et des niveaux (FSC) différents.\n\n"\
                                  u"Les CI ne pouvant pas être placés sur la cible\n"\
                                  u"apparaitront en orbite autour de la cible (2 maxi).\n\n"\
                                  u"Si le nombre de CI sélectionnés est limité à 2,\n"\
                                  u"le deuxième CI sélectionnable est forcément\n"\
                                  u"du même domaine (MEI) que le premier\n"\
                                  u"ou bien un des CI en orbite.")
#        self.SetHelpBitmap(help)
        
        
#############################################################################################################
#
# A propos ...
# 
#############################################################################################################
class A_propos(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, u"A propos de "+ __appname__)
        
        self.app = parent
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        titre = wx.StaticText(self, -1, " "+__appname__)
        titre.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, False))
        titre.SetForegroundColour(wx.NamedColour("BROWN"))
        sizer.Add(titre, border = 10)
        sizer.Add(wx.StaticText(self, -1, "Version : "+__version__+ " "), 
                  flag=wx.ALIGN_RIGHT)
#        sizer.Add(wx.StaticBitmap(self, -1, Images.Logo.GetBitmap()),
#                  flag=wx.ALIGN_CENTER)
        
#        sizer.Add(20)
        nb = wx.Notebook(self, -1, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        
        
        # Auteurs
        #---------
        auteurs = wx.Panel(nb, -1)
        fgs1 = wx.FlexGridSizer(cols=2, vgap=4, hgap=4)
        
        lstActeurs = ((u"Développement : ",(u"Cédrick FAURY", u"Jean-Claude FRICOU")),)#,
#                      (_(u"Remerciements : "),()) 


        
        for ac in lstActeurs:
            t = wx.StaticText(auteurs, -1, ac[0])
            fgs1.Add(t, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=4)
            for l in ac[1]:
                t = wx.StaticText(auteurs, -1, l)
                fgs1.Add(t , flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL| wx.ALL, border=4)
                t = wx.StaticText(auteurs, -1, "")
                fgs1.Add(t, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=0)
            t = wx.StaticText(auteurs, -1, "")
            fgs1.Add(t, flag=wx.ALL, border=0)
            
        auteurs.SetSizer(fgs1)
        
        # licence
        #---------
        licence = wx.Panel(nb, -1)
        try:
            txt = open(os.path.join(PATH, "gpl.txt"))
            lictext = txt.read()
            txt.close()
        except:
            lictext = u"Le fichier de licence (gpl.txt) est introuvable !\n\n" \
                      u"Veuillez réinstaller pySequence !"
            messageErreur(self, u'Licence introuvable',
                          lictext)
            
            
        wx.TextCtrl(licence, -1, lictext, size = (400, -1), 
                    style = wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_NONE )
        

        
        # Description
        #-------------
        descrip = wx.Panel(nb, -1)
        t = wx.StaticText(descrip, -1,u"",
                          size = (400, -1))#,
#                        style = wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_NONE) 
        t.SetLabelMarkup( wordwrap(u"<b>pySequence</b> est un logiciel d'aide à l'élaboration de séquences pédagogiques,\n"
                                          u"sous forme de fiches exportables au format PDF.\n"
                                          u"Il est élaboré en relation avec le programme et le document d'accompagnement\n"
                                          u"des enseignements technologiques transversaux de la filière STI2D.",500, wx.ClientDC(self)))
        nb.AddPage(descrip, u"Description")
        nb.AddPage(auteurs, u"Auteurs")
        nb.AddPage(licence, u"Licence")
        
        sizer.Add(hl.HyperLinkCtrl(self, wx.ID_ANY, u"Informations et téléchargement : http://code.google.com/p/pysequence/",
                                   URL="http://code.google.com/p/pysequence/"),  
                  flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
        sizer.Add(nb)
        
        self.SetSizerAndFit(sizer)



        


if __name__ == '__main__':
    import serveur
    import socket
    HOST, PORT = socket.gethostname(), 61955
    
    print "HOST :", HOST
    
    server = None
    # On teste si pySequence est déja ouvert ...
    #  = demande de connection au client (HOST,PORT) accéptée
    try:
        if len(sys.argv) > 1:
            arg = sys.argv[1]
        else:
            arg = ''
        serveur.client(HOST, PORT, arg)
        sys.exit()
        
    except socket.error: #socket.error: [Errno 10061] Aucune connexion n'a pu être établie car l'ordinateur cible l'a expressément refusée
        # On démarre une nouvelle instance de pySequence
        # = La demande de connection au client (HOST,PORT) a été refusée
        try :
            server = serveur.start_server(HOST, PORT)
        except: # socket.error: [Errno 10013] Une tentative d’accès à un socket de manière interdite par ses autorisations d’accès a été tentée 
            # L'accés a été refusé ... problème de pare-feu ??
            pass 
        app = SeqApp(False)
        app.MainLoop()
    

