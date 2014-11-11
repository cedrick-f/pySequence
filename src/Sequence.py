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

## Copyright (C) 2014 Cédrick FAURY - Jean-Claude FRICOU

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
Copyright (C) 2011-2014
@author: Cedrick FAURY

"""
__appname__= "pySequence"
__author__ = u"Cédrick FAURY"
__version__ = "5.0beta9"
print __version__

#from threading import Thread

#import psyco
#psyco.full()



####################################################################################
#
#   Gestion des erreurs
#
####################################################################################
import traceback
import time
import sys
from widgets import messageErreur

def MyExceptionHook(etype, value, trace):
    """
    Handler for all unhandled exceptions.
 
    :param `etype`: the exception type (`SyntaxError`, `ZeroDivisionError`, etc...);
    :type `etype`: `Exception`
    :param string `value`: the exception error message;
    :param string `trace`: the traceback header, if any (otherwise, it prints the
     standard Python header: ``Traceback (most recent call last)``.
    """
    tmp = traceback.format_exception(etype, value, trace)
    mes = u"pySéquence a renconté une erreur et doit fermer !\n\n"\
         u"Merci de copier le message ci-dessous\n" \
         u"et de l'envoyer à l'équipe de développement :\n"\
         u"http://code.google.com/p/pysequence/\n\n"
    exception = mes + "".join(tmp)
    
    try:
        frame = wx.GetApp().GetTopWindow()
        dlg = messageErreur(None, "Erreur !", exception, wx.ICON_ERROR)
    except:
        print exception
        time.sleep(6)
    sys.exit()

    
########################################################################
try:
    from agw import genericmessagedialog as GMD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.genericmessagedialog as GMD

 


#sys.excepthook = MyExceptionHook



####################################################################################
#
#   Import des modules nécessaires
#
####################################################################################

# Outils "système"
import os
import glob

if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf8')
    import locale
    loc = locale.getdefaultlocale()
    print loc
    if loc[1]:
        encoding = loc[1]
        sys.setdefaultencoding(encoding)
else:
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('utf-8')

FILE_ENCODING = sys.getfilesystemencoding() #'cp1252'#
DEFAUT_ENCODING = "utf-8"
SYSTEM_ENCODING = sys.getdefaultencoding()#sys.stdout.encoding#
print "FILE_ENCODING", FILE_ENCODING
print "SYSTEM_ENCODING", SYSTEM_ENCODING


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
Element = type(ET.Element(None))


# des widgets wx évolués "faits maison"
from widgets import Variable, VariableCtrl, VAR_REEL_POS, EVT_VAR_CTRL, VAR_ENTIER_POS#, chronometrer
#from CustomCheckBox import CustomCheckBox
# Les constantes et les fonctions de dessin


# Les constantes partagées
from constantes import calculerEffectifs, revCalculerEffectifs, PATH, \
                        strEffectifComplet, getElementFiltre, COUL_OK, COUL_NON, COUL_BOF, COUL_BIEN, \
                        toList, COUL_COMPETENCES, TABLE_PATH, CHAR_POINT, COUL_SOUT, COUL_REVUE
import constantes

# Les constantes partagées
from Referentiel import REFERENTIELS, ARBRE_REF
import Referentiel
#import constantes_ETT



import Options
from wx.lib.embeddedimage import PyEmbeddedImage

if sys.platform == "win32" :
    # Pour l'enregistement dans la base de donnée Windows
    import register
    # Pour lire les classeurs Excel
    import recup_excel
print "OS :", sys.platform

import textwrap

import grilles, genpdf

from rapport import FrameRapport, RapportRTF

import urllib2
from bs4 import BeautifulSoup
from xml.dom.minidom import parse, parseString
import xml.dom
        
        
# Pour l'export en swf
#import tempfile
#import svg_export

# Pour les descriptions
#import wx.richtext as rt
import richtext

from math import sin,cos,pi, log
from operator import attrgetter



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
    def SetFile(self, fil):
        self.file = fil
        
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
def toSystemEncoding(path): 
#        try:
    path = path.decode(FILE_ENCODING)
    path = path.encode(SYSTEM_ENCODING)
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
def pourCent(v, ajuster = False):
    if ajuster:
        return str(int(round(v*100))).rjust(3)+"%"
    else:
        return str(int(round(v*100)))+"%"

######################################################################################  
def pourCent2(v, ajuster = False):
    if ajuster:
        return str(int(v*100)).rjust(3)+"%"
    else:
        return str(int(v*100))+"%"

######################################################################################  
def remplaceLF2Code(txt):
    return txt.replace("\n", "##13##")#.replace("\n", "##13##")#&#13")
    
    
######################################################################################  
def remplaceCode2LF(txt):
    return txt.replace("##13##", "\n")#&#13")
    
    
######################################################################################  
def forceID(xml):
    for node in xml.childNodes:
        if hasattr(node, 'hasAttribute'):
            if node.hasAttribute("id"):
                node.setIdAttribute('id')
            if node.hasChildNodes():
                forceID(node)

#####################################################################################
#####################################################################################
def SetWholeText(node, Id, text):
    """ 
    """
    nom = node.getElementById(Id)
    if nom != None:
        
        for txtNode in nom.childNodes:
            if txtNode.nodeType==xml.dom.Node.TEXT_NODE:
                txtNode.replaceWholeText(text)
        
#####################################################################################
def XML_AjouterCol(node, idLigne, text, bcoul = None, fcoul = "black", size = None, bold = False):
    """<td id="rc1" style="background-color: #ff6347;"><font id="r1" size="2">1</font></td>"""
    ligne = node.getElementById(idLigne)
    if ligne != None:
        td = node.createElement("td")
        
        ligne.appendChild(td)
        
        if bcoul != None:
            td.setAttribute("style", "background-color: "+bcoul+";")
        
        if size != None:
            tc = node.createElement("font")
            tc.setAttribute("size", str(size))
#            tc.setAttribute("color", fcoul)
            td.appendChild(tc)
            td = tc
        
        if bold:
            tc = node.createElement("b")
            td.appendChild(tc)
            td = tc
            
        txt = node.createTextNode(text)
        td.appendChild(txt)
        

    
    
    
    
####################################################################################
#
#   Objet lien vers un fichier, un dossier ou bien un site web
#
####################################################################################
class Lien():
    def __init__(self, path = u"", typ = ""):
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
                              u"Impossible d'ouvrir le fichier\n\n%s\n" %toDefautEncoding(path))
                
        elif self.type == 'd':
            try:
                subprocess.Popen(["explorer", path])
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'accéder au dossier\n\n%s\n" %toDefautEncoding(path))
            
        elif self.type == 'u':
            try:
                webbrowser.open(self.path)
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'ouvrir l'url\n\n%s\n" %toDefautEncoding(self.path))
        
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
            try:
                path = os.path.join(pathseq, path)
            except UnicodeDecodeError:
                pathseq = toFileEncoding(pathseq)
                path = os.path.join(pathseq, path)
        return path
    
    
   
    
    ######################################################################################  
    def getBranche(self, branche):
        branche.set("Lien", toDefautEncoding(self.path))
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
        self.tip = PopupInfo2(self.parent.app, u"Séquence requise")
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
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
        
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
        p.setAttribute("xlink:href", lien)
        p.setAttribute("target", "_top")
#        self.elem.setAttribute("xlink:href", lien)
#        self.elem.setAttribute("target", "_top")
        
#    def EncapsuleSVG(self, doc, p):
#        self.elem = doc.createElement("a")
#        parent=p.parentNode
#        parent.insertBefore(self.elem, p)
#        self.elem.appendChild(p)
#        return self.elem


        
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
#                self.EncapsuleSVG(doc, p)
                titre = self.GetBulleSVG(f)
                
                t = doc.createElement("title")
                txt = doc.createTextNode(titre)
                t.appendChild(txt)

                p.appendChild(t)
                
                
#                self.SetSVGTitre(p, titre)
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
        t = self.GetCode(i) + " :\n" + self.GetIntit(i)
        return t.encode(DEFAUT_ENCODING)#.replace("\n", "&#10;")#"&#xD;")#
    
           
           
    ######################################################################################     
    def GetClasse(self):
        if hasattr(self, 'projet'):
            cl = self.projet.classe
        elif hasattr(self, 'sequence'):
            cl = self.sequence.classe
        elif hasattr(self, 'parent'):
            cl = self.parent.classe
        else:
            cl = self.classe
            
        return cl
            
    ######################################################################################  
    def GetTypeEnseignement(self, simple = False):
        cl = self.GetClasse()
            
        if simple:
            return cl.familleEnseignement
        
        return cl.typeEnseignement
        
        
    ######################################################################################  
    def GetReferentiel(self):
        return self.GetClasse().referentiel
    
    
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
            return self.branche
        
        
        
        
        
        
        
class Classe():
    def __init__(self, app, panelParent = None, intitule = u"", pourProjet = False, ouverture = False):
        self.intitule = intitule
        
        self.etablissement = u""
        
        self.options = app.options
        self.Initialise(pourProjet)
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Classe(panelParent, self, pourProjet, ouverture = ouverture)
            
        self.panelParent = panelParent

        
    ######################################################################################  
    def __repr__(self):
        return "Classe :", self.typeEnseignement
    
    
    ######################################################################################  
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.GetReferentiel().Enseignement[0])
        
#        self.CI = self.options.optClasse["CentresInteret"]
#        self.posCI = self.options.optClasse["PositionsCI"]
        
#        self.ci_SSI = self.options.optClasse["CentresInteretSSI"]
#        self.ci_ET = self.options.optClasse["CentresInteretET"]
#        self.posCI_ET = self.options.optClasse["PositionsCI_ET"]
        

    ######################################################################################  
    def SetCI(self, num, ci):
        self.CI[num] = ci
#        if self.typeEnseignement == "SSI":
#            self.ci_SSI[num] = ci
#        else:
#            self.ci_ET[num] = ci
            
    ######################################################################################  
    def Initialise(self, pourProjet):
        self.typeEnseignement = self.options.optClasse["TypeEnseignement"]
        self.referentiel = REFERENTIELS[self.typeEnseignement]
        
        if not pourProjet:
            self.MiseAJourTypeEnseignement()
        else:
            if not self.typeEnseignement in [ref.Code for ref in REFERENTIELS.values() if ref.projet]:
                self.typeEnseignement = constantes.TYPE_ENSEIGNEMENT_DEFAUT

        self.familleEnseignement = self.GetReferentiel().Famille  
         
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
        
        classe.append(self.referentiel.getBranche())
        
        classe.set("Etab", self.etablissement)
        
        eff = ET.SubElement(classe, "Effectifs")
        eff.set('eC', str(self.effectifs['C']))
        eff.set('nG', str(self.nbrGroupes['G']))
        eff.set('nE', str(self.nbrGroupes['E']))
        eff.set('nP', str(self.nbrGroupes['P']))
                      
#        if not self.referentiel.CI_BO and hasattr(self, 'CI'): 
#            ci = ET.SubElement(classe, "CentreInteret")
#            for i,c in enumerate(self.CI):
#                ci.set("CI"+str(i+1), c)
#                if self.referentiel.CI_cible:
#                    ci.set("pos"+str(i+1), self.posCI[i])
                
                
#        if self.typeEnseignement == 'ET':
#            ci = ET.SubElement(classe, "CentreInteret")
#            for i,c in enumerate(self.ci_ET):
#                ci.set("CI"+str(i+1), c)
#                ci.set("pos"+str(i+1), self.posCI_ET[i])
#        
#        elif self.typeEnseignement == 'SSI':
#            ci = ET.SubElement(classe, "CentreInteret")
#            if hasattr(self, 'ci_SSI'):
#                for i,c in enumerate(self.ci_SSI):
#                    ci.set("CI"+str(i+1), c)
        
        return classe
    
    ######################################################################################  
    def setBranche(self, branche):
        Ok = True
#        print "setBranche classe"
        self.typeEnseignement = branche.get("Type", constantes.TYPE_ENSEIGNEMENT_DEFAUT)
        
        brancheRef = branche.find("Referentiel")        # A partir de la version 5 !
        if brancheRef != None:   
            self.referentiel = Referentiel.Referentiel()
            self.version5 = True
            try:
                self.referentiel.setBranche(brancheRef)
#                print self.referentiel
            except:
                print "Erreur ouverture référentiel intégré !"
                self.referentiel = REFERENTIELS[self.typeEnseignement]
#            print self.referentiel
        else:
            self.version5 = False
            self.referentiel = REFERENTIELS[self.typeEnseignement]
            
            brancheCI = branche.find("CentreInteret")
            if brancheCI != None: # Uniquement pour rétrocompatibilité : normalement cet élément existe !
                continuer = True
                i = 1
                if self.typeEnseignement == 'ET':
                    CI = []
                    posCI = []
                    while continuer:
                        c = brancheCI.get("CI"+str(i))
                        p = brancheCI.get("pos"+str(i))
                        if c == None or p == None:
                            continuer = False
                        else:
                            CI.append(c)
                            posCI.append(p) 
                            i += 1
                        
                    if i > 1:
                        self.CI = CI
                        if self.referentiel.CI_cible:
                            self.posCI = posCI
        
        print "version 5", self.version5
        
        self.etablissement = branche.get("Etab", u"")
        
        self.familleEnseignement = self.referentiel.Famille
             
                
#                continuer = True
#                i = 1
#                if self.typeEnseignement == 'ET':
#                    ci_ET = []
#                    posCI_ET = []
#                    while continuer:
#                        c = brancheCI.get("CI"+str(i))
#                        p = brancheCI.get("pos"+str(i))
#                        if c == None or p == None:
#                            continuer = False
#                        else:
#                            ci_ET.append(c)
#                            posCI_ET.append(p) 
#                            i += 1
#                        
#                    if i > 1:
#                        self.ci_ET = ci_ET
#                        self.posCI_ET = posCI_ET
#                
#                elif self.typeEnseignement == 'SSI':
#                    ci_SSI = []
#                    while continuer:
#                        c = brancheCI.get("CI"+str(i))
#                        if c == None:
#                            continuer = False
#                        else:
#                            ci_SSI.append(c)
#                            i += 1
#                        
#                    if i > 1:
#                        self.ci_SSI = ci_SSI

                
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
#            self.doc.MiseAJourTypeEnseignement()
            self.panelPropriete.MiseAJour()
            
        return Ok
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, rallonge(self.GetReferentiel().Enseignement[0]))
        self.branche = arbre.AppendItem(branche, Titres[5]+" :", wnd = self.codeBranche, data = self)#, image = self.arbre.images["Seq"])
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)


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
    def GetReferentiel(self):
        return self.referentiel
        
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
        self.arbre.EnsureVisible(branche)
        for i in self.arbre._itemWithWindow:
            self.arbre.HideWindows()
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
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
        
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
    def GetTypeEnseignement(self, simple = False):
        cl = self.classe
            
        if simple:
            return cl.familleEnseignement
        
        return cl.typeEnseignement
        
    ######################################################################################  
    def GetReferentiel(self):
        return REFERENTIELS[self.GetTypeEnseignement()]
        
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
    def MiseAJourTypeEnseignement(self, changeFamille = False):
        self.app.SetTitre()
        self.classe.MiseAJourTypeEnseignement()
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
        
        # Organisation des phases du projet
        self.nbrRevues = 2
        self.positionRevues = list(self.GetReferentiel().posRevues[self.nbrRevues])

        # Année Scolaire
        self.annee = constantes.getAnneeScolaire()
        
        
        # Par défaut, la revue 1 est après la Conception détaillée
#        self.R1apresConception = False
        
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
#        self.panelPropriete.bgctrl.setObjet(self.origine)
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
        if self.nbrRevues == 2:
            lr = ["R1", "R2", "S"]
        else:
            lr = ["R1", "R2", "R3", "S"]
        for p in lr:
            lst.append(Tache(self, self.panelParent, 
                             intitule = self.GetReferentiel().phases_prj[p][1], 
                             phaseTache = p, duree = 0.5))
        return lst
    
    ######################################################################################  
    def getTachesRevue(self):
        return [t for t in self.taches if t.phase in ["R1", "R2", "R3", "S"]]
#        lst = []
#        for t in self.taches:
#            if t.phase in ["R1", "R2", "R3", "S"]:
#                lst.append(t)
#        return lst
        
        
#    ######################################################################################  
#    def getTachesRevue(self):    
    
    ######################################################################################  
    def getCodeLastRevue(self):
        if self.nbrRevues == 2:
            return "R2"
        else:
            return "R3"
        
    ######################################################################################  
    def getLastRevue(self):
        lr = self.getCodeLastRevue()
        for t in self.taches:
            if t.phase == lr:
                return t
        return None
        
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
            t = c[i] + " : " + REFERENTIELS[self.classe.typeEnseignement]._dicCompetences_prj_simple[c[i]]
            return t.encode(DEFAUT_ENCODING)
        else:
            e = self.eleves[-1-i]
            t = e.GetNomPrenom()+"\n"
            t += u"Durée d'activité : "+draw_cairo.getHoraireTxt(e.GetDuree())+"\n"
            t += u"Evaluabilité :\n"
            r, s = e.GetEvaluabilite()
            t += u"\tconduite : "+str(int(r*100))+"%\n"
            t += u"\tsoutenance : "+str(int(s*100))+"%\n"
            return t.encode(DEFAUT_ENCODING)
            
            
            
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
        projet.set("Annee", str(self.annee))
        
        # Organisation
        projet.set("NbrRevues", str(self.nbrRevues))
        projet.set("PosRevues", '-'.join(self.positionRevues))
#        projet.set("R1avC", str(self.R1apresConception))
        
        equipe = ET.SubElement(projet, "Equipe")
        for p in self.equipe:
            equipe.append(p.getBranche())
        
        projet.append(self.support.getBranche())
        
        taches = ET.SubElement(projet, "Taches")
        for t in self.taches:
            taches.append(t.getBranche())
#        
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
#        for k, lc in constantes._dicCompetences_prj_simple[self.classe.typeEnseignement].items():
#            comp.set(k, str(lc[1]))
        
        return projet
        
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche projet"
#        print self.GetReferentiel()
        Ok = True
        err = 0
        
        self.intitule = branche.get("Intitule", u"")

        self.problematique = remplaceCode2LF(branche.get("Problematique", u""))
        
        self.commentaires = branche.get("Commentaires", u"")
        
        self.nbrRevues = eval(branche.get("NbrRevues", "2"))
        self.positionRevues = branche.get("PosRevues", 
                                          '-'.join(list(self.GetReferentiel().posRevues[self.nbrRevues]))).split('-')

        if self.nbrRevues == 3:
            self.MiseAJourNbrRevues()
        
        self.MiseAJourTypeEnseignement()
        
        self.position = eval(branche.get("Position", "0"))
        self.annee = eval(branche.get("Annee", str(constantes.getAnneeScolaire())))

        brancheEqu = branche.find("Equipe")
        self.equipe = []
        for e in list(brancheEqu):
            prof = Prof(self, self.panelParent)
            Ok = Ok and prof.setBranche(e)
            if not Ok: err = err | constantes.ERR_PRJ_EQUIPE
            self.equipe.append(prof)

        brancheSup = branche.find("Support")
        if brancheSup != None:
            Ok = Ok and self.support.setBranche(brancheSup)
            if not Ok: err = err | constantes.ERR_PRJ_SUPPORT
        
        brancheEle = branche.find("Eleves")
        self.eleves = []
        for e in list(brancheEle):
            eleve = Eleve(self, self.panelParent)
            Ok = Ok and eleve.setBranche(e)
            if not Ok: err = err | constantes.ERR_PRJ_ELEVES
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
#            for k, lc in constantes._dicCompetences_prj_simple[self.classe.typeEnseignement].items():
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
            if phase in ["R1", "R2", "R3", "S"]:
                if phase == "S":
                    num = len(tachesRevue)-1
                else:
                    num = eval(phase[1])-1
                o,er =  tachesRevue[num].setBranche(e)
                Ok = Ok and o
                if not Ok: err = err | constantes.ERR_PRJ_TACHES | er
                self.taches.append(tachesRevue[num])
                adapterVersion = False
            else:
                tache = Tache(self, self.panelParent, branche = e)
                if tache.code < 0 : # ça s'est mal passé lors du setbranche ...
                    return False, err | constantes.ERR_PRJ_TACHES | -tache.code
#                tache.setBranche(e)
                self.taches.append(tache)
        self.CorrigerIndicateursEleve()
        
        # Pour récupérer les prj créés avec la version beta1
        if adapterVersion:
            self.taches.extend(tachesRevue)
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()

        return Ok, err
        
    ######################################################################################  
    def SetPosition(self, pos):
        # On passe à la position 5
        if pos == 5 and self.position != 5:
            for tr in self.creerTachesRevue():
                self.taches.append(tr)
                tr.ConstruireArbre(self.arbre, self.brancheTac)
                tr.SetCode()
                if hasattr(tr, 'panelPropriete'):
                    tr.panelPropriete.MiseAJour()
            self.OrdonnerTaches()
            self.arbre.Ordonner(self.brancheTac)
#            self.panelPropriete.sendEvent()
#            self.taches.extend(self.creerTachesRevue())
#            self.OrdonnerTaches()

                
        # On passe de la position5 à une autre
        elif pos !=5 and self.position == 5:
            lst = []
            for t in self.taches:
                if t.phase in ["R1", "R2", "R3", "S"]:
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
            
    ######################################################################################  
    def MiseAJourNbrRevues(self):
        """ Opère les changements lorsque le nombre de revues a changé...
        """
#        print "MiseAJourNbrRevues", self.nbrRevues
        if self.nbrRevues == 3: # on ajoute une revue
            self.positionRevues.append(self.positionRevues[-1])
            tache = Tache(self, self.panelParent, 
                          intitule = self.GetReferentiel().phases_prj["R3"][1], 
                          phaseTache = "R3", duree = 0.5)
            self.taches.append(tache)
            tache.ConstruireArbre(self.arbre, self.brancheTac)
            tache.SetPhase()
            
            revue2 = self.getTachesRevue()[1]
            revue2.panelPropriete = PanelPropriete_Tache(self.panelParent, revue2, revue = True)
            
            
        elif self.nbrRevues == 2:
            t = self.getTachesRevue()[2]
            self.SupprimerTache(item = t.branche)
            revue2 = self.getTachesRevue()[1]
            revue2.panelPropriete = PanelPropriete_Tache(self.panelParent, revue2, revue = True)
        return
           
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
    def AjouterTache(self, event = None, tacheAct = None):
        """ Ajoute une tâche au projet
            et la place juste après la tâche tacheAct (si précisé)
        """
        if tacheAct == None or tacheAct.phase == "S" or tacheAct.phase == "":
            tache = Tache(self, self.panelParent)
            self.taches.append(tache)
            tache.ordre = len(self.taches)
            tache.ConstruireArbre(self.arbre, self.brancheTac)
            
        else:
            # La phase de la nouvelle tâche
            if not tacheAct.phase in ["R1", "R2", "R3", "Rev"]:
                phase = tacheAct.phase
            elif tacheAct.phase == "Rev":
                i = self.taches.index(tacheAct)
                if i > 0 and self.taches[i-1].phase not in ["R1", "R2", "R3", "Rev", "S"]:
                    phase = self.taches[i-1].phase 
                elif i+1<len(self.taches) and self.taches[i+1].phase not in ["R1", "R2", "R3", "Rev", "S"]:
                    phase = self.taches[i+1].phase 
                else:
                    phase = ""
            else:
                l = self.GetListePhases()
                i = l.index(tacheAct.phase)
                if i+1<len(l):
                    phase = l[i+1]
                else:
                    phase = ""
#            elif tacheAct.phase == "R1":
#                if self.GetTypeEnseignement() == "SSI":
#                    phase = 'Rea'
#                else:
#                    phase = 'DCo'
#            elif tacheAct.phase == "R2":
#                phase = 'XXX'
#            else:
#                phase = ""
            tache = Tache(self, self.panelParent, phaseTache = phase)
            self.taches.append(tache)
            tache.ordre = tacheAct.ordre+0.5 # truc pour le tri ...
            tache.ConstruireArbre(self.arbre, self.brancheTac)
            
            tache.SetPhase()
            if hasattr(tache, 'panelPropriete'):
                tache.panelPropriete.MiseAJour()
        
        self.VerrouillerClasse()
        
#        self.brancheTac.Collapse()
#        self.arbre.CalculatePositions()
#        self.arbre.Expand(self.brancheTac)
        
        
        
        self.arbre.EnsureVisible(tache.branche)
        for i in self.arbre._itemWithWindow:
            self.arbre.HideWindows()
        self.arbre.SelectItem(tache.branche)

        self.panelPropriete.sendEvent()

        return tache
    
    ######################################################################################  
    def CopierTache(self, event = None, item = None):
        tache = self.arbre.GetItemPyData(item)
        if isinstance(tache, Tache):
            self.GetApp().parent.SetData(tache.getBranche())
#            print "Tache", tache, u"copiée"

    ######################################################################################  
    def CollerTache(self, event = None, item = None):
        tache_avant = self.arbre.GetItemPyData(item)
        if not isinstance(tache_avant, Tache):
            return
        
        elementCopie = self.GetApp().parent.elementCopie
        if elementCopie == None or tache_avant.phase != elementCopie.get("Phase", ""): # la phase est la même
            return
        
        tache = Tache(self, self.panelParent, phaseTache = "Rev")
        tache.setBranche(elementCopie)
        
        tache.ordre = tache_avant.ordre+1
        for t in self.taches[tache_avant.ordre:]:
            t.ordre += 1
        self.taches.append(tache)
        self.taches.sort(key=attrgetter('ordre'))
        
        tache.ConstruireArbre(self.arbre, self.brancheTac)
        tache.SetCode()
        if hasattr(tache, 'panelPropriete'):
            tache.panelPropriete.MiseAJour()
            tache.panelPropriete.MiseAJourEleves()
        
        self.arbre.Ordonner(self.brancheTac)
        self.panelPropriete.sendEvent()
        self.arbre.SelectItem(tache.branche)
            
        self.VerrouillerClasse()
#        print "Tache", tache, u"collée"
        
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
            
        self.VerrouillerClasse()
        
    ######################################################################################  
    def SupprimerTache(self, event = None, item = None):
        tache = self.arbre.GetItemPyData(item)
        self.taches.remove(tache)
        self.arbre.Delete(item)
        self.SetOrdresTaches()
        self.panelPropriete.sendEvent()
        
        self.VerrouillerClasse()
        
        
    ######################################################################################  
    def SetOrdresTaches(self):
        for i, tt in enumerate(self.taches):
            tt.ordre = i+1
            tt.SetCode()
        
    ######################################################################################  
    def OrdonnerListeTaches(self, lstTaches):
#        print "OrdonnerListeTaches", lstTaches
        
        #
        # On enregistre les positions des revues intermédiaires (après qui ?)
        #
        ref = self.GetReferentiel()
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
        paquet = {'': []}
        for k in ref.listPhases_prj:#['STI']+constantes.NOM_PHASE_TACHE_E.keys(): 
            paquet[k]=[]

        Rien = []
        for t in lstTaches:
            paquet[t.phase].append(t)
            
#        print paquet
        
        # On trie les tâches de chaque paquet  
        for c in [k for k in ref.listPhases_prj if not k in ref.listPhasesEval_prj]:#['Ana', 'Con', 'Rea', 'DCo', 'Val', 'XXX']:
            paquet[c].sort(key=attrgetter('ordre'))

        #
        # On assemble les paquets
        #
        lst = []
        for p in self.GetListePhases()+["S"]:
            lst.extend(paquet[p]) 

        #
        # On ajoute les revues intermédiaires
        #
        for r, q in Rev:
            if q == None:
                lst.insert(0, r)
            else:
                i = lst.index(q)
                lst.insert(i+1, r)
    
        #
        # On ajoute les tâches sans phase
        #
        if '' in paquet.keys():
            lst.extend(paquet[''])
            
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
        if isinstance(data, Tache) and data.phase not in ["R1", "R2", "R3", "S"]:
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
        if len(self.eleves) < 5:
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
        i = self.eleves.index(e)
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
#        print "GetNewIdEleve", 
        for i in range(6):
            ok = False
            for e in self.eleves:
                ok = ok or i != e.id
            if ok:
                break
        return i
    

    ######################################################################################  
    def AjouterProf(self, event = None):
        if len(self.equipe) < 5:
            e = Prof(self, self.panelParent, len(self.equipe))
            self.equipe.append(e)
            e.ConstruireArbre(self.arbre, self.branchePrf)
            self.arbre.Expand(self.branchePrf)
            self.panelPropriete.sendEvent()
            self.arbre.SelectItem(e.branche)

    
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
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
            
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
            des compétences utiles au projet
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
        """ Renvoie le nombre de phases dans le projet
            (les revues intermédiaires coupent parfois une phase en deux !)
            (pour tracé fiche)
        """
        n = 0
        for i, t in enumerate(self.taches):
            if (i == 0 or t.phase != self.taches[i-1].phase):
                n += 1
        return n

    ######################################################################################  
    def GetListeNomsPhases(self, avecRevuesInter = False):
#        print "GetListeNomsPhases"
        lst = []
        ref = self.GetReferentiel()
        for p in self.GetListePhases():
            if p in ref.listPhases_prj:#[:-1]:
                lst.append(ref.phases_prj[p][0])
            elif p in ref.listPhasesEval_prj:
                lst.append(ref.phases_prj[p][0])
                
#        for p in self.GetListePhases():
#            if p in constantes.NOM_PHASE_TACHE_COURT[self.GetTypeEnseignement(simple = True)].keys():
#                lst.append(constantes.NOM_PHASE_TACHE_COURT[self.GetTypeEnseignement(simple = True)][p])
#            elif p in constantes.NOM_PHASE_TACHE_E_COURT.keys():
#                lst.append(constantes.NOM_PHASE_TACHE_E_COURT[p])

        return lst
        
    ######################################################################################  
    def GetListePhases(self, avecRevuesInter = False):
        """ Renvoie la liste ordonnée des phases dans le projet
        """
#        print "GetListePhases"
#        lst = list(constantes.PHASE_TACHE[self.GetTypeEnseignement(simple = True)][:-1])
        lst = [k for k in self.GetReferentiel().listPhases_prj if not k in self.GetReferentiel().listPhasesEval_prj]
#        lst = list(self.GetReferentiel().listPhases_prj)
#        print "  ", lst
#        print "  ", self.nbrRevues
        if self.nbrRevues == 2:
            lr = [2,1]
        else:
            lr = [3,2,1]
        for r in lr:
#            print "     ", self.positionRevues[r-1]
            lst.insert(lst.index(self.positionRevues[r-1])+1, "R"+str(r))
        
        
        return lst
        
#        # Ancienne version (marche pas avec les Rev)
#        p = []
#        for t in self.taches:
#            if ((not t.phase in p) or t.phase == "Rev") and t.phase != "":
#                p.append(t.phase)
#        return len(p)
        
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
    def getNomFichierDefaut(self, prefixe):
        nomFichier = prefixe+"_"+self.intitule[:20]
        for c in ["\"", "/", "\", ", "?", "<", ">", "|", ":", "."]:
            nomFichier = nomFichier.replace(c, "_")
        return nomFichier
        
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
    def MiseAJourTypeEnseignement(self, changeFamille = False):
        self.app.SetTitre()
        for t in self.taches:
            t.MiseAJourTypeEnseignement(self.classe.referentiel)
        
        for e in self.eleves:
            e.MiseAJourTypeEnseignement()
            
        if hasattr(self, 'panelPropriete'):
            if changeFamille:
                self.nbrRevues = 2
                self.positionRevues = list(self.GetReferentiel().posRevues[self.nbrRevues])
            self.panelPropriete.panelOrga.MiseAJourListe()
        
    #############################################################################
    def VerrouillerClasse(self):
#        print "VerrouillerClasse", len(self.taches)
        self.classe.Verrouiller(len(self.GetCompetencesUtil()) == 0 and len(self.taches) == 3)
        
    #############################################################################
    def CorrigerIndicateursEleve(self):
        """
        """
        return
        if self.nbrRevues == 2:
            lstR = ["R1"]
        else:
            lstR = ["R1", "R2"]
        for t in self.taches:
            if t.phase in lstR:
                for i, e in enumerate(self.eleves):
                    pass
        
    
    ######################################################################################  
    def TesterExistanceGrilles(self, nomFichiers):
#        print "TesterExistanceGrilles", nomFichiers
        existe = []
        for fe in nomFichiers.values():
            for k, f in fe.items():
                if os.path.isfile(f):
                    existe.append(f)
        
        if len(existe) > 0:
            if len(existe) == 1:
                m = u"La grille d'évaluation existe déja !\n\n" \
                    u"\t%s\n\n" \
                    u"Voulez-vous la remplacer ?" %existe[0]
            else:
                m = u"Les grilles d'évaluation existent déja !\n\n" \
                    u"\t%s\n\n" \
                    u"Voulez-vous les remplacer ?" %u"\n".join(existe)
                                            
            dialog = wx.MessageDialog(self.GetApp(), m, 
                                      u"Fichier existant", wx.YES_NO | wx.ICON_WARNING)
            retCode = dialog.ShowModal()
            if retCode == wx.ID_YES:
                return True
            else:
                return False
        return True
    
    
    #############################################################################
    def SetCompetencesRevuesSoutenance(self):
        """ Attribue à la soutenance et à la revue n°2 (ou n°3 si 3 revues)
            les compétences et indicateurs 
            mobilisés par les tâches précédentes
        """
#        print "SetCompetencesRevuesSoutenance", len(self.eleves)
#        tousIndicateurs = self.GetReferentiel()._dicIndicateurs_prj
#        print tousIndicateurs
#        REFERENTIELS[self.classe.typeEnseignement].dicIndicateurs_prj
        tR1 = None
        tR2 = None
        indicateurs = [{} for e in range(len(self.eleves)+1)]   # 0 : tous les élèves
        
        for t in self.taches:   # toutes les tâches, dans l'ordre
            
            if t.phase in ["R1", "R2", "R3", "S", "Rev"]:
                
                for neleve in range(len(self.eleves)+1):

                    if t.phase in ["R1", "Rev"] or (t.phase == "R2" and self.nbrRevues == 3):
                        t.indicateursMaxiEleve[neleve] = []
                    else:
                        t.indicateursEleve[neleve] = []

                    for c, l in indicateurs[neleve].items():
                        for i, ok in enumerate(l):
                            if ok:
                                codeIndic = c+"_"+str(i+1)
                                if self.GetReferentiel().getTypeIndicateur(codeIndic) == "C": # tousIndicateurs[c][i][1]: # Indicateur "revue"
                                    if t.phase in ["R1", "R2", "R3", "Rev"]:

                                        if t.phase in ["R1", "Rev"] or (t.phase == "R2" and self.nbrRevues == 3):
                                            t.indicateursMaxiEleve[neleve].append(codeIndic)
                                  
                                        else:
                                            if t.phase == "R2": # 2 revues
                                                if tR1 != None and not codeIndic in tR1.indicateursEleve[neleve]: # R1 est passée
                                                    t.indicateursEleve[neleve].append(codeIndic)
                                                   
                                                            
                                            else: # t.phase == "R3"
                                                if tR2 != None and not codeIndic in tR2.indicateursEleve[neleve] and not codeIndic in tR1.indicateursEleve[neleve]: # R2 est passée
                                                    t.indicateursEleve[neleve].append(codeIndic)
                                        
                                        
                                else:
                                    if t.phase == "S":
                                        t.indicateursEleve[neleve].append(codeIndic)
    
                    if neleve == 0:

                        if t.phase in ["R1", "Rev"] or (t.phase == "R2" and self.nbrRevues == 3):
                            ti = []
                            for i in t.indicateursEleve[neleve]:
                                if i in t.indicateursMaxiEleve[neleve]:
                                    ti.append(i)
                            t.indicateursEleve[neleve] = ti
                            t.panelPropriete.arbre.MiseAJourTypeEnseignement(t.GetReferentiel())
                            t.panelPropriete.MiseAJour()
                            if t.phase == "R1":
                                tR1 = t # la revue 1 est passée !
                            elif t.phase == "R2":
                                tR2 = t # la revue 2 est passée ! (3 revues)
                        
            else:   # On stock les indicateurs dans un dictionnaire CodeCompétence : ListeTrueFalse
                indicTache = t.GetDicIndicateurs()
                for c, i in indicTache.items():
                    for neleve in range(len(self.eleves)+1):
                        if (neleve == 0) or ((neleve-1) in t.eleves):
                            if c in indicateurs[neleve].keys():
                                indicateurs[neleve][c] = [x or y for x,y in zip(i, indicateurs[neleve][c])]
                            else:
                                indicateurs[neleve][c] = i 

            t.ActualiserDicIndicateurs()

#    #############################################################################
#    def SetCompetencesRevuesSoutenance2(self):
#        """ Attribue à la soutenance et à la revue n°2
#            les compétences et indicateurs 
#            mobilisés par les tâches précédentes
#        """
#        print "SetCompetencesRevuesSoutenance"
#        tousIndicateurs = constantes.dicIndicateurs[self.classe.typeEnseignement]
#        tR1 = None
#        tR2 = None
#        indicateurs = {}
#        
#        for t in self.taches:   # toutes les tâches, dans l'ordre
#            
#            if t.phase in ["R1", "R2", "R3", "S"]:
#                
#                if t.phase == "R1" or (t.phase == "R2" and self.nbrRevues == 3):
#                    t.indicateursMaxi = []
#                else:
#                    t.indicateurs = []
#                
#                for c, l in indicateurs.items():
#                    for i, ok in enumerate(l):
#                        if ok:
#                            codeIndic = c+"_"+str(i+1)
#                            if tousIndicateurs[c][i][1]: # Indicateur "revue"
#                                if t.phase in ["R1", "R2", "R3"]:
##                                    if t.phase == self.getCodeLastRevue() and (tR1 != None and not codeIndic in tR1.indicateurs):
##                                        t.indicateurs.append(codeIndic)
#                                    if t.phase == "R1" or (t.phase == "R2" and self.nbrRevues == 3):
#                                        t.indicateursMaxi.append(codeIndic)
#                                    else:
#                                        if t.phase == "R2": # 2 revues
#                                            if tR1 != None and not codeIndic in tR1.indicateurs: # R1 est passée
#                                                t.indicateurs.append(codeIndic)
#                                        else: # t.phase == "R3"
#                                            if tR2 != None and not codeIndic in tR2.indicateurs and not codeIndic in tR1.indicateurs: # R2 est passée
#                                                t.indicateurs.append(codeIndic)
#                                    
#                                    
#                            else:
#                                if t.phase == "S":
#                                    t.indicateurs.append(codeIndic)
#
#                
#                if t.phase == "R1" or (t.phase == "R2" and self.nbrRevues == 3):
#                    ti = []
#                    for i in t.indicateurs:
#                        if i in t.indicateursMaxi:
#                            ti.append(i)
#                    t.indicateurs = ti
#                    t.panelPropriete.arbre.MiseAJourTypeEnseignement(t.GetTypeEnseignement())
#                    t.panelPropriete.MiseAJour()
#                    if t.phase == "R1":
#                        tR1 = t # la revue 1 est passée !
#                    else:
#                        tR2 = t # la revue 2 est passée ! (3 revues)
#                        
#            else:   # On stock les indicateurs dans un dictionnaire CodeCompétence : ListeTrueFalse
#                indicTache = t.GetDicIndicateurs()
#                for c, i in indicTache.items():
#                    if c in indicateurs.keys():
#                        indicateurs[c] = [x or y for x,y in zip(i, indicateurs[c])]
#                    else:
#                        indicateurs[c] = i         

#    #############################################################################
#    def SetCompetencesRevuesSoutenance2(self):
#        """ Attribue à la soutenance et à la revue n°2
#            les compétences et indicateurs 
#            mobilisés par les tâches précédentes
#        """
#        print "SetCompetencesRevuesSoutenance"
#        tousIndicateurs = constantes.dicIndicateurs[self.classe.typeEnseignement]
#        tR1 = None
#        indicateurs = {}
#        for t in self.taches:   # toutes les tâches, dans l'ordre
#            if t.phase in ["R1", "R2", "R3", "S"]:
#                if t.phase == "R1" or (t.phase == "R2" and self.nbrRevues == 3):
#                    t.indicateursMaxi = []
#                else:
#                    t.indicateurs = []
#                
#                for c, l in indicateurs.items():
#                    for i, ok in enumerate(l):
#                        if ok:
#                            codeIndic = c+"_"+str(i+1)
#                            if tousIndicateurs[c][i][1]: # Indicateur "revue"
#                                if t.phase in ["R1", "R2", "R3"]:
#                                    if t.phase == self.getCodeLastRevue() and (tR1 != None and not codeIndic in tR1.indicateurs):
#                                        t.indicateurs.append(codeIndic)
#                                    if t.phase == "R1" or (t.phase == "R2" and self.nbrRevues == 3):
#                                        t.indicateursMaxi.append(codeIndic)
#                            else:
#                                if t.phase == "S":
#                                    t.indicateurs.append(codeIndic)
#
#                
#                if t.phase == "R1" or (t.phase == "R2" and self.nbrRevues == 3):
#                    ti = []
#                    for i in t.indicateurs:
#                        if i in t.indicateursMaxi:
#                            ti.append(i)
#                    t.indicateurs = ti
#                    t.panelPropriete.arbre.MiseAJourTypeEnseignement(t.GetTypeEnseignement())
#                    t.panelPropriete.MiseAJour()
#                    tR1 = t
#                            
#                        
#            else:   # On stock les indicateurs dans un dictionnaire CodeCompétence : ListeTrueFalse
#                indicTache = t.GetDicIndicateurs()
#                for c, i in indicTache.items():
#                    if c in indicateurs.keys():
#                        indicateurs[c] = [x or y for x,y in zip(i, indicateurs[c])]
#                    else:
#                        indicateurs[c] = i   
#                        
                
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
        for i in range(len(branche.keys())):
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
        if self.GetReferentiel().CI_cible:
            lstCI = self.parent.classe.CI
        else:
            lstCI = self.GetReferentiel().CentresInterets
        if self.numCI[num] < len(lstCI):
            return lstCI[self.numCI[num]]
            
    
    
    ######################################################################################  
    def GetCode(self, num = None):
        if num == None:
            s = ""
            for i in range(len(self.numCI)):
                s += self.GetCode(i)
                if i < len(self.numCI)-1:
                    s += " - "
            return s
        
        else :
            return "CI"+str(self.numCI[num]+1)
    
    ######################################################################################  
    def GetPosCible(self, num):
        if self.GetReferentiel().CI_cible:
            return self.parent.classe.posCI[self.numCI[num]]
        
    
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
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)

        
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
        for i in range(len(branche.keys())):
            self.competences.append(branche.get("C"+str(i), ""))
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()
    
    
    ######################################################################################  
    def GetCode(self, num):
        return self.competences[num]
    
    ######################################################################################  
    def GetIntit(self, num):
        return REFERENTIELS[self.parent.typeEnseignement].getCompetence(self.competences[num])[0]
    
    
         
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
        t = self.GetReferentiel().nomCompetences
        self.branche = arbre.AppendItem(branche, t, wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Com"])
        self.arbre.SetItemTextColour(self.branche, constantes.GetCouleurWx(COUL_COMPETENCES))
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        self.arbre.SetItemText(self.branche, self.GetReferentiel().nomCompetences)
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
        """ Interprétation de la branche (lecture fichier .seq)
             préfixes :
              - B = enseignement de base (tronc commun)
              - S = spécialité
              - M = math
              - P = physique
        """
#        print "setBranche Savoirs"
        self.savoirs = []
        for i in range(len(branche.keys())):
            code = branche.get("S"+str(i), "")
            if code != "":
                if not code[0] in ["B", "S", "M", "P"]: # version < 4.6
                    if code[0] == "_":
                        code = "B"+code[1:]
                    else:
                        if self.GetReferentiel().tr_com == []:
                            code = "B"+code
                        else:
                            code = "S"+code

                self.savoirs.append(code)
        if hasattr(self, 'panelPropriete'):
#            self.panelPropriete.construire()
            self.panelPropriete.MiseAJour()
        
    ######################################################################################  
    def GetCode(self, num):
        return self.savoirs[num]
    
    ######################################################################################  
    def GetIntit(self, num):
        return self.GetReferentiel().getSavoir(self.GetCode(num))  
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        t = self.GetReferentiel().nomSavoirs
        self.branche = arbre.AppendItem(branche, t, wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Sav"])
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
    
#    #############################################################################
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
#            return self.branche
        
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, self.GetReferentiel().nomSavoirs)
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJourTypeEnseignement()
#            self.panelPropriete.construire()
    
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
            self.tip = PopupInfo2(self.GetApp(), u"Séance")
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
            for s in list(branche):
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
            for k, v in self.GetReferentiel().effectifs.items():
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
            for s in seq.systemes:
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
        for c, n in self.GetReferentiel().demarches.items():
#        for k, v in constantes.Demarches.items():
            if n[1] == text:
                codeDem = c
                break
        self.demarche = codeDem
        
        
    ######################################################################################  
    def SetType(self, typ):
        if type(typ) == str or type(typ) == unicode:
            self.typeSeance = typ
        else:
            self.typeSeance = self.GetReferentiel().listeTypeSeance[typ]
            
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
            self.arbre.SetItemText(self.branche, self.GetReferentiel().seances[self.typeSeance][0])
            
                  
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
            t = u"Type : "+ self.GetReferentiel().seances[self.typeSeance][1]
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
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
            
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
    def SupprimerSysteme(self, i):
        if self.typeSeance in ["AP", "ED", "P"]:
            del self.systemes[i]
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.sousSeances:
                s.SupprimerSysteme(i)

        
        
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
    def GetReferentiel(self):
        return  self.GetDocument().GetReferentiel()
        
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
    
                  
    def __init__(self, projet, panelParent, intitule = u"", phaseTache = "", duree = 1.0, branche = None):
        """ Séance :
                panelParent = le parent wx pour contenir "panelPropriete"
                phaseTache = phase de la tache parmi 'Ana', 'Con', 'Rea', 'Val'
        """
#        print "__init__ tâche"
        Objet_sequence.__init__(self)
        
        # Les données sauvegardées
        self.ordre = 100
        self.duree = Variable(u"Volume horaire (h)", lstVal = duree, nomNorm = "", typ = VAR_REEL_POS, 
                              bornes = [0.5,40], modeLog = False,
                              expression = None, multiple = False)
        self.intitule  = intitule
        self.intituleDansDeroul = True
        
        
        # Les élèves concernés (liste d'élèves)
        self.eleves = []
        
        # Les indicateurs de compétences abordés
#        self.indicateurs = []
#        self.indicateursMaxi = [] # Code à revoir : ça ne sert que pour R1 !
        
#        if phaseTache in ["R1", "R2", "R3", "S"]:

#        self.indicateursEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []} # clef = n°eleve ;  valeur = liste d'indicateurs
#        if phaseTache in ["R1", "R2", "R3", "S", "Rev"]:
#            self.indicateursMaxiEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
            
        
        self.code = u""
        self.description = None

        # Les autres données
        self.projet = projet
        self.panelParent = panelParent
        
        self.phase = phaseTache
        
#        self.initIndicateurs()
        
        
            
        #
        # Création du Tip (PopupInfo)
        #
        if self.GetApp():
            if hasattr(self, "branche"):
                b = self.branche
            else:
                b = None
            self.tip = PopupInfo2(self.GetApp(), u"Tâche", self.GetDocument(), b)
            self.tip.sizer.SetItemSpan(self.tip.titre, (1,2))
            
            if not self.phase in ["R1", "R2", "R3", "S", "Rev"]:
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
            Ok, err = self.setBranche(branche)
            if not Ok:
                self.code = -err # Pour renvoyer une éventuelle erreur à l'ouverture d'un fichier
        else:
            self.indicateursEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []} # clef = n°eleve ;  valeur = liste d'indicateurs
            if phaseTache in ["R1", "R2", "R3", "S", "Rev"]:
                self.indicateursMaxiEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
            
        if panelParent:
            self.panelPropriete = PanelPropriete_Tache(panelParent, self)
        else:
            print "pas panelParent", self
            
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
        return self.code +"("+str(self.ordre)+")"
    
    
    ######################################################################################  
    def GetApp(self):
        return self.projet.GetApp()

    ######################################################################################  
    def ActualiserDicIndicateurs(self):
        """ Complète le dict des compétences/indicateurs globaux (tous les élèves confondus)
        """
#        print "ActualiserDicIndicateurs", self
        for i, eleve in enumerate(self.projet.eleves):
            indicateurs = self.indicateursEleve[i+1]#self.GetDicIndicateursEleve(eleve)
            for c in indicateurs:
                if not c in self.indicateursEleve[0]:
                    self.indicateursEleve[0].append(c)
#                self.indicateursEleve[0] = [x or y for x, y in zip(self.indicateursEleve[0], lc)]

            
            
        
    ######################################################################################  
    def GetDicIndicateurs(self):
        """ Renvoie l'ensemble des indicateurs de compétences à mobiliser pour cette tâche
            Dict :  clef = code compétence
                  valeur = liste [True False ...] des indicateurs à mobiliser
        """
#        print "GetDicIndicateurs", self, ":", self.indicateursEleve
        tousIndicateurs = self.GetReferentiel()._dicIndicateurs_prj_simple
        indicateurs = {}
        
        for i in self.indicateursEleve[0]:
#            print "   ", i
            cci = i.split('_')
            if len(cci) == 2:
                competence, indicateur = cci
                indicateur = int(eval(indicateur)-1)
                nbrIndic = len(tousIndicateurs[competence])
                if not competence in indicateurs.keys():
                    indicateurs[competence] = [False]*nbrIndic
                indicateurs[competence][indicateur] = True
#            else:
#                competence, sscomp, indicateur = cci
#                indicateur = int(eval(indicateur)-1)
#                nbrIndic = 0
#                for sc in tousIndicateurs[competence].values():
#                    nbrIndic += len(sc)
#                if not competence in indicateurs.keys():
#                    indicateurs[competence] = [False]*nbrIndic
#                
#                indicateurs[competence][indicateur] = True
                    
        return indicateurs
    
    
    ######################################################################################  
    def GetDicIndicateursEleve(self, eleve):
        """ Renvoie l'ensemble des indicateurs de compétences à mobiliser pour cette REVUE
            Dict :  clef = code compétence
                  valeur = liste [True False ...] des indicateurs à mobiliser
        """
#        print "GetDicIndicateursEleve", self, eleve.id+1
        indicateurs = {}
        numEleve = eleve.id
        for i in self.indicateursEleve[numEleve+1]:
            competence, indicateur = i.split('_')
            indicateur = eval(indicateur)-1
            if not competence in indicateurs.keys():
                indicateurs[competence] = [False]*len(self.GetReferentiel()._dicIndicateurs_prj_simple[competence])
            
            indicateurs[competence][indicateur] = True
        return indicateurs
    
    ######################################################################################  
    def DiffereSuivantEleve(self):
        """ Renvoie True si cette REVUE est différente selon l'élève
            Renvoie False si tous les élèves abordent les mêmes compétences/indicateurs
        """
#        print "DiffereSuivantEleve", self, self.phase
        if len(self.projet.eleves) == 0:
            return False
        indicateurs = self.GetDicIndicateursEleve(self.projet.eleves[0])
        for eleve in self.projet.eleves[1:]:
            ie = self.GetDicIndicateursEleve(eleve)
            if set(indicateurs.keys()) != set(ie.keys()):
                return True
            for k, v in ie.items():
                if set(v) != set(indicateurs[k]):
                    return True
            
        return False
    
    ######################################################################################  
    def GetCompetencesUtil(self):
        lst = []
        for i in self.indicateursEleve[0]:
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
            indicateurs = REFERENTIELS[typeEns]._dicCompetences_prj_simple
            self.indicateursEleve[0] = dict(zip(indicateurs.keys(), [x[1] for x in indicateurs.values()]))
        else:
            indicateurs = REFERENTIELS[typeEns].dicIndicateurs
            self.indicateursEleve[0] = {}
            for k, dic in indicateurs.items():
                ndict = dict(zip(dic[1].keys(), [[]]*len(dic[1])))
                for c in ndict.keys():
                    ndict[c] = [True]*len(indicateurs[k][1][c])
                self.indicateursEleve[0].update(ndict)
            
            
        
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
        
        
        if not self.phase in [self.projet.getCodeLastRevue(), "S"]:
            # Structure des indicateurs :
            # <Indicateurs Indic0="CO6.1_1" Indic1="CO6.2_4" ..... />
            #   (compétence_indicateur)
            brancheCmp = ET.Element("Indicateurs")
            root.append(brancheCmp)
            
            if self.projet.nbrRevues == 2:
                lstR = ["R1"]
            else:
                lstR = ["R1", "R2"]
                    
            if self.phase in lstR:
                for e, indicateurs in self.indicateursEleve.items()[1:]:
                    if e > len(self.projet.eleves):
                        break
                    brancheE = ET.Element("Eleve"+str(e))
                    brancheCmp.append(brancheE)
                    for i, c in enumerate(indicateurs):
                        brancheE.set("Indic"+str(i), c)        
            elif not self.phase in ["R1", "R2", "R3"]:
                for i, c in enumerate(self.indicateursEleve[0]):
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
#        print "setBranche tâche", 
        Ok = True
        err = 0
        
        self.ordre = eval(branche.tag[5:])
        self.intitule  = branche.get("Intitule", "")
        
        self.phase = branche.get("Phase", "")
#        print self.phase

        # Suite commentée ... à voir si pb
#        if self.GetTypeEnseignement() == "SSI":
#            if self.phase == 'Con':
#                self.phase = 'Ana'
#            elif self.phase in ['DCo', 'Val']:
#                self.phase = 'Rea'

        self.description = branche.get("Description", None)
        
        if not self.phase in ["R1", "R2", "R3", "S"]:
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        else:
            self.duree.v[0] = 0.5
        
        brancheElv = branche.find("Eleves")
        self.eleves = []
        for i, e in enumerate(brancheElv.keys()):
            self.eleves.append(eval(brancheElv.get("Eleve"+str(i))))
        
        self.indicateursEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
        
        if not self.GetClasse().version5:
            if not self.phase in [self.projet.getCodeLastRevue(), "S"]:
                self.indicateursMaxiEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
                
                
            pass # Nouveaux indicateurs STI2D !!
        else:
            if not self.phase in [self.projet.getCodeLastRevue(), "S"]:
                self.indicateursMaxiEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
                #
                # pour compatibilité acsendante
                #
                brancheCmp = branche.find("Competences")
                
                if brancheCmp != None: ## ANCIENNE VERSION (<beta6)
                    Ok = False
                    err = err | constantes.ERR_PRJ_T_VERSION
                    if self.GetTypeEnseignement() == "SSI":
                        brancheInd = None
                    else:
                        brancheInd = branche.find("Indicateurs")
                    
                    for i, e in enumerate(brancheCmp.keys()):
                        if brancheInd != None: #STI2D
                            i = eval(e[4:])
                            indic = brancheInd.get("Indic"+str(i))
                            if indic != None:
                                lst = toList(indic)
                            else:
                                lst = [True]*len(self.GetReferentiel()._dicIndicateurs_prj[e])
                            for n,j in enumerate(lst):
                                if j:
                                    self.indicateursEleve[0].append(brancheCmp.get(e)+"_"+str(n+1))
                        else:
                            indic = brancheCmp.get("Comp"+str(i))
                            self.indicateursEleve[0].append(indic.replace(".", "_"))
                    
                
                
                else:
                    brancheInd = branche.find("Indicateurs")
#                    print "  branche Indicateurs"
                    if brancheInd != None:
                        if self.projet.nbrRevues == 2:
                            lstR = ["R1"]
                        else:
                            lstR = ["R1", "R2"]

                        # 
                        # Indicateurs revue par élève (première(s) revues)
                        #
                        if self.phase in lstR:
                            for i, e in enumerate(self.projet.eleves):
                                
                                self.indicateursEleve[i+1] = []
                                
                                brancheE = brancheInd.find("Eleve"+str(i+1))
                                if brancheE != None:
                                    for c in brancheE.keys():
                                        codeindic = brancheE.get(c)
                                        code, indic = codeindic.split('_')
                                        
                                        # pour compatibilité version < 3.19
                                        if code == "CO8.es":
                                            code = "CO8.0"
                                            codeindic = code+"_"+indic
                                            
                                        # Si c'est la dernière phase et que c'est une compétence "Conduite" ... on passe
                                        indic = eval(indic)-1
                                        if self.phase == 'XXX' and self.GetReferentiel().getTypeIndicateur(codeindic) == 'C':
                                            continue
                                        
                                        try:
#                                            print "***",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                                            # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                                            if not code in self.GetReferentiel()._dicIndicateurs_prj_simple:
                                                print "Erreur 1", code, "<>", self.GetReferentiel()._dicIndicateurs_prj_simple
                                                return False, err | constantes.ERR_PRJ_T_TYPENS
                                            
                                            if not codeindic in self.indicateursEleve[i+1]:
                                                self.indicateursEleve[i+1].append(codeindic)
                                        except:
                                            pass
                                
                                else: # Pour ouverture version <4.8beta1
                                    indicprov = []
                                    for c in brancheInd.keys():
                                        codeindic = brancheInd.get(c)
                                        code, indic = codeindic.split('_')
                                        
                                        # pour compatibilité version < 3.19
                                        if code == "CO8.es":
                                            code = "CO8.0"
                                            codeindic = code+"_"+indic
                                            
                                        # Si c'est la dernière phase et que c'est une compétence "Conduite" ... on passe
                                        indic = eval(indic)-1
                                        if self.phase == 'XXX' and self.GetReferentiel().getTypeIndicateur(codeindic) == 'C':
                                            continue
                                        
#                                        print "******",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                                            
                                        # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                                        if not code in self.GetReferentiel()._dicIndicateurs_prj:
                                            print "Erreur 2"
                                            return False, err | constantes.ERR_PRJ_T_TYPENS
    
                                        indicprov.append(codeindic)
                                        dic = e.GetDicIndicateursRevue(self.phase)
                                        if code in dic.keys():
                                            if dic[code][indic]:
                                                self.indicateursEleve[i+1].append(codeindic)
                                    
                        #
                        # Indicateurs tâche
                        #
                        else:
                            for i, e in enumerate(brancheInd.keys()):
                                codeindic = brancheInd.get(e)
                                code, indic = codeindic.split('_')
#                                print "     ", code, indic
                                # pour compatibilité version < 3.19
                                if code == "CO8.es":
                                    code = "CO8.0"
                                    codeindic = code+"_"+indic
                                    
                                # Si c'est la dernière phase et que c'est une compétence "Conduite" ... on passe
                                indic = eval(indic)-1
                                if self.phase == 'XXX' and self.GetReferentiel().getTypeIndicateur(codeindic) == 'C':
                                    continue
                                
                                    
#                                try:
#                                    print "******",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                                # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                                if not code in self.GetReferentiel()._dicIndicateurs_prj_simple.keys():
                                    print "Erreur 3", code, "<>", self.GetReferentiel()._dicIndicateurs_prj_simple.keys()
                                    err =  err | constantes.ERR_PRJ_T_TYPENS
                                else:
                                    self.indicateursEleve[0].append(codeindic)
#                                except:
#                                    pass
                        
                    
#        print self.indicateursEleve
        
        self.ActualiserDicIndicateurs()
            
        self.intituleDansDeroul = eval(branche.get("IntituleDansDeroul", "True"))

        return Ok, err
    
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
        return

    ######################################################################################  
    def GetDelai(self):
        if self.phase != "":
            if self.phase in ["R1", "R2", "R3", "Rev"]:
                de = []
                for e in self.projet.eleves:
                    de.append(e.GetDuree(self.phase))
                if not de:
                    d = 0
                else:
                    d = max(de)
                return d
        return 0
    
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
        self.projet.MiseAJourDureeEleves()
        
    ######################################################################################  
    def SetIntitule(self, text):           
        self.intitule = text
        if self.intitule != "":
            t = u"Intitulé : "+ "\n".join(textwrap.wrap(self.intitule, 40))
        else:
            t = u""
        self.tip.SetTexte(t, self.tip_intitule)
        
        
            
            
    ######################################################################################  
    def SetPhase(self, phase = None):
#        print "SetPhase", self.phase, ">>", phase
        if phase != None:
            self.phase = phase
        self.projet.OrdonnerTaches()
        
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
        for t in self.projet.taches:
            if t.phase == self.phase:
                if t == self:
                    break
                i += 1
        num = str(i+1)

        typeEns = self.GetTypeEnseignement(True)
        
        if self.phase != "":
            if self.phase in ["R1", "R2", "R3", "S"]:
                self.code = self.phase
            else:
                self.code = self.GetReferentiel().phases_prj[self.phase][2]+num     #constantes.CODE_PHASE_TACHE[typeEns][self.phase]+num
        else:
            self.code = num

        
        
        if hasattr(self, 'codeBranche') and self.phase != "":
            if self.phase in ["R1", "R2", "R3", "S"]:
                self.codeBranche.SetLabel(u"")
                t = u""
            else:
                self.codeBranche.SetLabel(self.code)
                t = u" :"
            self.arbre.SetItemText(self.branche, self.GetReferentiel().phases_prj[self.phase][1]+t)
        
        
        # Tip
        if self.phase in ["R1", "R2", "R3", "S"]:
            self.tip.SetTitre(self.GetReferentiel().phases_prj[self.phase][1])
        elif self.phase == "Rev":
            self.tip.SetTitre(self.GetReferentiel().phases_prj[self.phase][1])
        else:
            self.tip.SetTitre(u"Tâche "+ self.code)
            if self.phase != "":
                t = self.GetReferentiel().phases_prj[self.phase][1]
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
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
            
        if self.phase in ["R1", "R2", "R3"]:
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
    def MiseAJourTypeEnseignement(self, ref):
        self.panelPropriete.MiseAJourTypeEnseignement(ref)
        
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

        for i, ident in enumerate(self.eleves):
            if ident > i:
                self.eleves[i] = ident-1

        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeEleves()
        

    
    ######################################################################################  
    def MiseAJourPoidsCompetences(self, code = None):
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJourPoidsCompetences(code)
                
    ######################################################################################  
    def GetDocument(self):    
        return self.projet
    
    ######################################################################################  
    def GetClasse(self):
        return self.GetDocument().classe
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            if not self.phase in ["R1", "R2", "R3", "S"]:
                listItems = [[u"Supprimer", functools.partial(self.projet.SupprimerTache, item = itemArbre)]]
            else:
                listItems = []
            listItems.append([u"Insérer une revue après", functools.partial(self.projet.InsererRevue, item = itemArbre)])
            listItems.append([u"Copier", functools.partial(self.projet.CopierTache, item = itemArbre)])
            
 
            elementCopie = self.GetApp().parent.elementCopie
            if elementCopie != None: # Le presse papier n'est pas vide
                if isinstance(elementCopie, Element): # Le presse contient un Element
                    if elementCopie.tag[:5] == 'Tache': # Le presse contient une tache
                        if self.phase == elementCopie.get("Phase", ""): # la phase est la même
                            listItems.append([u"Coller après", functools.partial(self.projet.CollerTache, item = itemArbre)])
                    
            self.GetApp().AfficherMenuContextuel(listItems)
#            item2 = menu.Append(wx.ID_ANY, u"Créer une rotation")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterRotation, item = item), item2)
#            
#            item3 = menu.Append(wx.ID_ANY, u"Créer une série")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterSerie, item = item), item3)
        
        

        
        
        
        
        
        
        
        
        
        
        
        
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
        self.tip = PopupInfo2(self.parent.app, u"Système ou matériel")
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

        self.nbrDispo.v[0] = eval(branche.get("Nbr", "1"))
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
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
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
        self.tip = PopupInfo2(self.parent.app, u"Support")
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
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)

        
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
    def __init__(self, projet, panelParent, Id = 0):
        self.projet = projet
        self.nom = u""
        self.prenom = u""
        self.avatar = None
        self.id = Id # Un identifiant unique = nombre > 0

        #
        # Création du Tip (PopupInfo)
        #
        self.ficheHTML = self.GetFicheHTML()

        self.ficheXML = parseString(self.ficheHTML.encode('utf-8', errors="ignore"))
       
        forceID(self.ficheXML)
        self.tip = PopupInfo(self.projet.app, self.ficheHTML)
#        self.tip_nom = self.tip.CreerTexte((1,0), flag = wx.ALIGN_LEFT|wx.TOP)
#        self.tip_nom.SetFont(wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
#        self.tip_avatar = self.tip.CreerImage((2,0))
#        
#        if self.code == 'Prf':
#            self.tip.SetTitre(u"Professeur")
#            self.tip_disc = self.tip.CreerTexte((3,0), flag = wx.ALIGN_LEFT|wx.TOP)
#            self.tip_disc.SetFont(wx.Font(10, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
#        else:
#            self.tip.SetTitre(self.titre.capitalize())
        
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Personne(panelParent, self)

    ######################################################################################  
    def GetApp(self):
        return self.projet.GetApp()
        
        
    ######################################################################################  
    def GetDocument(self):
        return self.projet
    
    
    ######################################################################################  
    def __repr__(self):
        return self.GetNomPrenom()


    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
#        print "getBranche", supprime_accent(self.titre)
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
            
        if hasattr(self, 'grille'):
            for k, g in self.grille.items():
                root.set("Grille"+k, toDefautEncoding(g.path))
#            root.set("Grille0", self.grille[0].path)
#            root.set("Grille1", self.grille[1].path)
           
            
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche personne"
        Ok = True
        self.id  = eval(branche.get("Id", "0"))
        self.nom  = branche.get("Nom", "")
        self.prenom  = branche.get("Prenom", "")
        data = branche.get("Avatar", "")
        if data != "":
            self.avatar = PyEmbeddedImage(data).GetBitmap()
            
        if hasattr(self, 'referent'):   # prof
            self.referent = eval(branche.get("Referent", "False"))
            
        if hasattr(self, 'discipline'): # prof
            self.discipline = branche.get("Discipline", 'Tec')
            
        if hasattr(self, 'grille'):     # élève
#            print self.grille
            for k in self.GetReferentiel().nomParties_prj.keys():
                self.grille[k] = Lien(typ = "f")
                self.grille[k].path = toFileEncoding(branche.get("Grille"+k, u""))
#                print self.grille
#            self.grille[0].path = branche.get("Grille0", u"")
#            self.grille[1].path = branche.get("Grille1", u"")
            
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.SetImage()
            self.panelPropriete.MiseAJourTypeEnseignement()
            self.panelPropriete.MiseAJour(marquerModifier = False)
        
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
        self.ficheHTML = self.GetFicheHTML()
        self.ficheXML = parseString(self.ficheHTML.encode('utf-8', errors="ignore"))
        forceID(self.ficheXML)
        SetWholeText(self.ficheXML, "nom", self.GetNomPrenom())
        
        self.tip.XML_AjouterImg(self.ficheXML, "av", self.avatar) 
        
        self.SetTip2()
        
        # Tip
#        if hasattr(self, 'tip'):
#            self.tip.SetTexte(self.GetNomPrenom(), self.tip_nom)
#            self.tip.SetImage(self.avatar, self.tip_avatar)

    ######################################################################################  
    def SetImage(self):
        self.SetTip()
        return
#        self.tip.SetImage(self.avatar, self.tip_avatar)
#        self.SetTip()
        
    


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
#   Classe définissant les propriétés d'un élève
#
####################################################################################
BASE_FICHE_HTML = u"""<?xml version="1.0" encoding="utf-8"?><HTML>
    <p style="text-align: center;"><font size="12"><b>Elève</b></font></p>
<p id="nom">Nom-Prénom</p>
<p id="av"></p>
<table border="0">
<tbody>
<tr id = "ld" align="right" valign="middle">
<td width="110"><span style="text-decoration: underline;">Durée d'activité :</span></td>
</tr>

<tr  id = "le" align="right" valign="middle">
<td><span style="text-decoration: underline;">Evaluabilité :</span></td>
<td></td>
</tr>

<tr  id = "ler" align="right" valign="middle" >
<td><font color = "%s"><em>conduite :</em></font></td>
</tr>

<tr  id = "les" align="right" valign="middle" >
<td><font color = "%s"><em>soutenance :</em></font></td>
</tr>

</tbody>
</table>
</HTML>
"""

class Eleve(Personne, Objet_sequence):
    def __init__(self, projet, panelParent, ident = 0):
        
        self.titre = u"élève"
        self.code = "Elv"
        
        self.grille = {} #[Lien(typ = 'f'), Lien(typ = 'f')]
        for k in projet.GetReferentiel().nomParties_prj.keys():
            self.grille[k] = Lien(typ = 'f')
        
        Personne.__init__(self, projet, panelParent, ident)
 
        
        
    def GetFicheHTML(self):
        cr = constantes.GetCouleurHTML(COUL_REVUE)
        cs = constantes.GetCouleurHTML(COUL_SOUT)
        return BASE_FICHE_HTML %(cr,cs)

            
    ######################################################################################  
    def GetDuree(self, partie = None):
        d = 0
        p = 0
        if partie != None:
            for i, t in enumerate(self.projet.taches):
                if t.phase == partie:
                    break
                if t.phase in ["R1", "R2", "R3", "S"]:
                    p = i
        
        for t in self.projet.taches[p:]:
            if t.phase == partie:
                break
            if not t.phase in ["R1", "R2", "R3", "S", "Rev"]:
                if self.id in t.eleves:
                    d += t.GetDuree()
        return d
        
        
    ######################################################################################  
    def OuvrirGrille(self, k):
        try:
            self.grille[k].Afficher(self.projet.GetPath())#os.startfile(self.grille[num])
        except:
            messageErreur(None, u"Ouverture impossible",
                          u"Impossible d'ouvrir le fichier\n\n%s!\n" %toDefautEncoding(self.grille[k].path))
            
            
    ######################################################################################  
    def OuvrirGrilles(self, event):
        for k in self.grille.keys():
            self.OuvrirGrille(k)
#        if self.GetTypeEnseignement(simple = True) == "STI2D":
#            self.OuvrirGrille(1)
        
        
    ######################################################################################  
    def getNomFichierDefaut(self, prefixe):
        nomFichier = prefixe+"_"+self.GetNomPrenom()+"_"+self.projet.intitule[:20]
        for c in ["\"", "/", "\", ", "?", "<", ">", "|", ":", "."]:
            nomFichier = nomFichier.replace(c, "_")
        return nomFichier


#    ######################################################################################  
#    def getTableurEtModif(self):
#        try :
#            tableaux = grilles.getTableau(self.projet.GetApp(), self.projet)
#        except:
#            pass
#        if tableaux != None:
#            if "beta" in __version__:
#                grilles.modifierGrille(self.projet, tableaux, self)
#            else:
#                try:
#                    grilles.modifierGrille(self.projet, tableaux, self)
#                except:
#                    pass 
#            return tableaux
    
#    ######################################################################################  
#    def GenererGrille2(self, event = None, path = None, messageFin = True):
#        
#        if path == None:
#            path = os.path.dirname(self.projet.GetApp().fichierCourant)
#        
#        nomFichiers = {} 
#        for k, g in self.projet.GetReferentiel().nomParties_prj.items():
#            nomFichiers[k] = os.path.join(path, self.getNomFichierDefaut("Grille"+g))
#        
#        grilles.copierClasseurs(self.projet, nomFichiers)
#        
#        grilles.modifierGrille2(self.projet, nomFichiers, self)
#        
#        tableaux = self.getTableurEtModif()
#        
#
##        if self.projet.GetTypeEnseignement() == 'SSI':
##            nomFichier = self.getNomFichierDefaut("Grille")
##            
##            tableur = self.getTableurEtModif()
##            tf = [[tableur, nomFichier]]
##        else:
##            nomFichierR = self.getNomFichierDefaut("Grille_revue")
##            nomFichierS = self.getNomFichierDefaut("Grille_soutenance")
##            tableur = self.getTableurEtModif()
##            tf = [[tableur[0], nomFichierR], [tableur[1], nomFichierS]]
#        
##        for k, t in tableaux.items():
##            try:
##                cheminComplet = os.path.join(path, nomFichiers[k])+".xls"
##                t.save(cheminComplet)
##            except:
##                messageErreur(self.projet.GetApp(), u"Erreur !",
##                              u"Impossible d'enregistrer le fichier.\n\nVérifier :\n" \
##                              u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
##                              u" - que le dossier choisi n'est pas protégé en écriture")
##            try:
##                t.close()
##            except:
##                pass
##            self.grille[k] = Lien(typ = 'f')
##            self.grille[k].path = cheminComplet
#        
#        if messageFin:
#            if len(tableaux)>1:
#                t = u"Génération des grilles réussie !"
#            else:
#                t = u"Génération de la grille réussie !"
#            t += u"\n\n"
#            t += u"\n".join(nomFichiers.values())
#            
#            
#            dlg = wx.MessageDialog(self.projet.GetApp(), t, u"Génération réussie",
#                           wx.OK | wx.ICON_INFORMATION)
#            dlg.ShowModal()
#            dlg.Destroy()
#        
#        self.panelPropriete.MiseAJour()
        
    ######################################################################################  
    def GetNomGrilles(self, path = None):
        """ Renvoie les noms des fichiers grilles à générer
        """
        ref = self.projet.GetReferentiel()
        #
        # Création des noms des fichiers grilles
        #
        # Par défaut = chemin du fichier .prj
        if path == None:
            path = os.path.dirname(self.projet.GetApp().fichierCourant)
            
        nomFichiers = {} 
        for k, g in ref.nomParties_prj.items():
            prefixe = "Grille_"+g
            if grilles.EXT_EXCEL != None:
#                extention = os.path.splitext(ref.grilles_prj[k][0])[1]
                extention = grilles.EXT_EXCEL
                if ref.grilles_prj[k][1] == 'C': # fichier "Collectif"
                    nomFichiers[k] = os.path.join(path, self.projet.getNomFichierDefaut(prefixe)) + extention
                else:
                    nomFichiers[k] = os.path.join(path, self.getNomFichierDefaut(prefixe)) + extention
        return nomFichiers


    ######################################################################################  
    def GenererGrille(self, event = None, path = None, nomFichiers = None, messageFin = True):
#        print "GenererGrille", self
#        print "  ", nomFichiers
        if nomFichiers == None:
            nomFichiers = self.GetNomGrilles(path)
            if not self.projet.TesterExistanceGrilles(nomFichiers):
                return
            
        ref = self.projet.GetReferentiel()
        
        #
        # Ouverture (et pré-sauvegarde) des fichiers grilles "source" (tableaux Excel)
        #
#        existe = []
#        for k, f in nomFichiers.items():
#            if os.path.isfile(f):
#                existe.append(f)
#        if len(existe) > 0:
#            if len(existe) == 1:
#                m = u"La grille d'évaluation existe déja !\n\n" \
#                    u"\t%s\n\n" \
#                    u"Voulez-vous la remplacer ?" %existe[0]
#            else:
#                m = u"Les grilles d'évaluation existent déja !\n\n" \
#                    u"\t%s\n\n" \
#                    u"Voulez-vous les remplacer ?" %u"\n".join(existe)
#                                            
#            dialog = wx.MessageDialog(self.projet.GetApp(), m, 
#                                      u"Fichier existant", wx.YES_NO | wx.ICON_WARNING)
#            retCode = dialog.ShowModal()
#            if retCode != wx.ID_YES:
#                return
        
        
        tableaux = {}
        for k, f in nomFichiers.items():
            if os.path.isfile(f):
                tableaux[k] = grilles.getTableau(self.projet.GetApp(), f)
            else:
                tableaux[k] = grilles.getTableau(self.projet.GetApp(),
                                                 ref.grilles_prj[k][0])
                if tableaux[k] != None: # and tableaux[k].filename !=f:
                    tableaux[k].save(f)
#                    try:
#                        tableaux[k].save(f)
#                    except:
#                        messageErreur(self.projet.GetApp(), u"Erreur !",
#                                      u"Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
#                                      u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
#                                      u" - que le dossier choisi n'est pas protégé en écriture"%f)

        if tableaux == None:
            return
        
        #
        # Remplissage des grilles
        #
        if "beta" in __version__:
            grilles.modifierGrille(self.projet, tableaux, self)
        else:
            try:
                grilles.modifierGrille(self.projet, tableaux, self)
            except:
                messageErreur(self.projet.GetApp(), u"Erreur !",
                              u"Impossible de modifier les grilles !") 


        #
        # Enregistrement final des grilles
        #
        for k, t in tableaux.items():
            try:
                t.save()
            except:
                messageErreur(self.projet.GetApp(), u"Erreur !",
                              u"Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
                              u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
                              u" - que le dossier choisi n'est pas protégé en écriture" %f)
            try:
                t.close()
            except:
                pass
            self.grille[k] = Lien(typ = 'f')
            self.grille[k].path = nomFichiers[k]
        
        
        #
        # Message de fin
        #
        if messageFin:
            if len(tableaux)>1:
                t = u"Génération des grilles réussie !"
            else:
                t = u"Génération de la grille réussie !"
            t += u"\n\n"
            t += u"\n".join(nomFichiers.values())
            
            dlg = wx.MessageDialog(self.projet.GetApp(), t, u"Génération réussie",
                           wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        
        self.panelPropriete.MiseAJour()
        
        
    ######################################################################################  
    def GetEvaluabilite(self, complet = False):
        """ Renvoie l'évaluabilité
            % conduite
            % soutenance
        """ 
#        print "GetEvaluabilite", self
            
#        dicPoids = self.GetReferentiel().dicPoidsIndicateurs_prj
        dicIndicateurs = self.GetDicIndicateurs()
#        print "dicIndicateurs", dicIndicateurs
        tousIndicateurs = self.GetReferentiel()._dicIndicateurs_prj
        lstGrpIndicateur = {'R' : self.GetReferentiel()._lstGrpIndicateurRevues,
                            'S' : self.GetReferentiel()._lstGrpIndicateurSoutenance}
#        print lstGrpIndicateur
            
#        r, s = 0, 0
#        ler, les = {}, {}
        
        rs = [0, 0]
        lers = [{}, {}]
            
        def getPoids(listIndic, comp, poidsGrp):
            """ 
            """
            for k, ph in enumerate(["R", "S"]):
                if grp in lstGrpIndicateur[ph]:
                    for i, indic in enumerate(listIndic):
#                        print "comp", grp, comp, i, indic[1]
                        if comp in dicIndicateurs.keys():
                            if dicIndicateurs[comp][i]:
                                poids = indic[1]
                                p = 1.0*poids[k+1]/100
                                rs[k] += p * poidsGrp[k+1]/100
                                if grp in lers[k].keys():
                                    lers[k][grp] += p
                                else:
                                    lers[k][grp] = p
                        else:
                            if not grp in lers[k].keys():
                                lers[k][grp] = 0
                            
            return rs[0], rs[1], lers[0], lers[1]
        
        
        for grp, grpComp in tousIndicateurs.items():
            titre, dicComp, poidsGrp = grpComp
#            print "    ", grp, poidsGrp
            for comp, lstIndic in dicComp.items():
#                print "      ", comp
                if type(lstIndic[1]) == list:           # 2 niveaux
                    getPoids(lstIndic[1], comp, poidsGrp)    
                else:                                   # 3 niveaux
                    for scomp, lstIndic2 in lstIndic.items():
                        getPoids(lstIndic2[1], scomp, poidsGrp)
                                
                                                               
        r, s = rs
        ler, les = lers
#        print "les", les, s
         
        # On corrige s'il n'y a qu'une seule grille (cas SSI jusqu'à 2014)
#        if len(self.GetReferentiel().grilles_prj) == 1: 
##        if self.GetTypeEnseignement() == "SSI":
#            r, s = r*2, s*2
#            for l in ler.keys():
#                ler[l] = ler[l]*2
#            for l in les.keys():
#                les[l] = les[l]*2
            
#        if "O8s" in les.keys():
#            les["O8"] = les["O8s"]
#            del les["O8s"]
            
#        print r, s, ler, les
        
        #
        # Seuils d'évaluabilité
        #
        # liste des classeurs avec des grilles comprenant des colonne "non"
#        classeurs = [i[0] for i in self.GetReferentiel().cellulesInfo_prj["NON"] if i[0] != '']
        seuil = {}
        for t in ["R", "S"]:
#            if t in classeurs:
#            print "aColNon", self.GetReferentiel().aColNon
            if self.GetReferentiel().aColNon[t]:
                seuil[t] = 0.5  # s'il y a une colonne "non", le seuil d'évaluabilité est de 50% par groupe de compétence
            else:
                seuil[t] = 1.0     # s'il n'y a pas de colonne "non", le seuil d'évaluabilité est de 100% par groupe de compétence
        
        ev = {}
        ev_tot = {}
        for txt, le, ph in zip([r, s], [ler, les], ["R", "S"]):
            txt = round(txt, 6)
            ev[ph] = {}
            ev_tot[ph] = [txt, True]
            for grp, tx in le.items():
                tx = round(tx, 6)
                ev[ph][grp] = [tx, tx >= seuil[ph]]
                ev_tot[ph][1] = ev_tot[ph][1] and ev[ph][grp][1]
        
#        print ev, ev_tot, seuil
        return ev, ev_tot, seuil
        
        
#        if complet:
#            return r, s, ler, les
#        else:
#            return r, s
    

    ######################################################################################  
    def GetCompetences(self):
        lst = []
        for t in self.projet.taches:
            if self.id in t.eleves:
                lst.extend(t.competences)
        lst = list(set(lst))
        return lst
    
    
    ######################################################################################  
    def GetDicIndicateurs(self, limite = None):
        """ Renvoie un dictionnaire des indicateurs que l'élève doit mobiliser
             (pour tracé)
                  clef = code compétence
                valeur = liste [True False ...] des indicateurs à mobiliser
        """
        indicateurs = {}
#        print " GetDicIndicateurs", self.id
        for t in self.projet.taches: # Toutes les tâches du projet
            if not t.phase in ["R1", "R2", "R3", "S", "Rev"]:
                if self.id in t.eleves:     # L'élève est concerné par cette tâche
                    indicTache = t.GetDicIndicateurs() # Les indicateurs des compétences à mobiliser pour cette tâche
                    for c, i in indicTache.items():
                        if c in indicateurs.keys():
                            indicateurs[c] = [x or y for x, y in zip(indicateurs[c], i)]
                        else:
                            indicateurs[c] = i
                
        return indicateurs
        
        
        
        
    ######################################################################################  
    def GetDicIndicateursRevue(self, revue):
        """ Renvoie un dictionnaire des indicateurs que l'élève doit mobiliser AVANT une revue
             (pour tracé)
                  clef = code compétence
                valeur = liste [True False ...] des indicateurs à mobiliser
        """
        indicateurs = {}
#        print " GetDicIndicateurs", self.id
        for t in self.projet.taches: # Toutes les tâches du projet
            if t.code == revue:
                break
            if self.id in t.eleves:     # L'élève est concerné par cette tâche
                indicTache = t.GetDicIndicateurs() # Les indicateurs des compétences à mobiliser pour cette tâche
                for c, i in indicTache.items():
                    if c in indicateurs.keys():
                        indicateurs[c] = [x or y for x, y in zip(indicateurs[c], i)]
                    else:
                        indicateurs[c] = i
                
        return indicateurs
    
    
    
    
    ######################################################################################  
    def GetTaches(self, revues = False):
        lst = []
        for t in self.projet.taches:
            if revues and t.phase in ["R1", "R2", "R3"]:
                lst.append(t)
            elif self.id in t.eleves:
                if revues and t.phase == "Rev":
                    lst.append(t)
                elif t.phase != "Rev":
                    lst.append(t)
            
                    
#        lst = list(set(lst))
            
        return lst
        
    ######################################################################################  
    def GrillesGenerees(self):
        b = True
        for g in self.grille.values():
            b = b and g.path != u""
        return b
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            listItems = [[u"Supprimer", functools.partial(self.projet.SupprimerEleve, item = itemArbre)]]
            if len(self.GetReferentiel().nomParties_prj) > 0:
                tg = u"Générer grille"
                to = u"Ouvrir grille"
                if len(self.GetReferentiel().nomParties_prj) > 1:
                    tg += u"s"
                    to += u"s"
                
                if self.GrillesGenerees():
                    listItems.append([to, functools.partial(self.OuvrirGrilles)])
            listItems.append([tg, functools.partial(self.GenererGrille)])    
            
#            if self.projet.GetTypeEnseignement(simple = True) == "SSI":
#                
#                if self.grille[0].path != u"":
#                    
#            else:
#                listItems.append([u"Générer grilles", functools.partial(self.GenererGrille)])
#                if self.grille[0].path != u"":
#                    listItems.append([u"Ouvrir grilles", functools.partial(self.OuvrirGrilles)])
    
            self.GetApp().AfficherMenuContextuel(listItems)
            

    ######################################################################################  
    def MiseAJourTypeEnseignement(self):
#        print "MiseAJourTypeEnseignement", self
        self.grille = {} #[Lien(typ = 'f'), Lien(typ = 'f')]
#        print self.GetReferentiel().nomParties_prj
        for k in self.GetReferentiel().nomParties_prj.keys():
            self.grille[k] = Lien(typ = 'f')
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJourTypeEnseignement()
    
    
    ######################################################################################  
    def MiseAJourCodeBranche(self):
        """ Met à jour les tags de durée de projet
            et d'évaluabilité
        """
#        print "MiseAJourCodeBranche", self
        
        
        
        #
        # Durée
        #
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
            self.codeDuree.SetToolTipString(u"Durée de travail acceptable")
        else:
            self.codeDuree.SetBackgroundColour(COUL_NON)
            if duree < 70:
                self.codeDuree.SetToolTipString(u"Durée de travail insuffisante")
            else:
                self.codeDuree.SetToolTipString(u"Durée de travail trop importante")
        
        #
        # Evaluabilité
        #
#        er, es , ler, les = self.GetEvaluabilite(complet = True)
        ev, ev_tot, seuil = self.GetEvaluabilite()

        labr = rallonge(pourCent2(ev_tot['R'][0]))
        labs = rallonge(pourCent2(ev_tot['S'][0]))
        self.evaluR.SetLabel(labr)
        self.evaluS.SetLabel(labs)
        
        keys = sorted(self.GetReferentiel()._dicIndicateurs_prj_simple.keys())
        if "O8s" in keys:
            keys.remove("O8s")
        
#        labr = {}
#        for k in keys:
#            if k in self.GetReferentiel()._lstGrpIndicateurRevues:
#                if k in ev_tot['R'].keys():
#                    labr[k] = ev_tot['R'][k][0]
#                else:
#                    labr[k] = 0
        
#        pas50r = [k for k in labr.keys() if labr[k] < 0.5]
#        pas50s = [] # Pas de case "NON" pour la grille de soutenance
        
        t1 = u"L'élève ne mobilise pas suffisamment de compétences pour être évalué"
        t21 = u"Le "
        t22 = u"Les "
        t3 = u"taux d'indicateurs évalués pour "
        t4 = u" est inférieur à "
        t51 = u"la compétence "
        t52 = u"les compétences "
        
        for ph, nomph, st in zip(['R', 'S'], [u"conduite", u"soutenance"], [self.evaluR, self.evaluS]):
            t = u"Evaluabilité de la "+nomph+u" du projet "
            tt = u""
            if ev_tot[ph][1]:
                tt += u"\n" + t1
        
            le = [k for k in ev[ph].keys() if ev[ph][k] == False] # liste des groupes de compétences pas évaluable
            if len(le) == 1:
                tt += u"\n" + t21 + t3 + t51 + le[0] + t4 + pourCent2(seuil[ph])
            else:
                tt += u"\n" + t22 + t3 + t52 + " ".join(le) + t4 + pourCent2(seuil[ph])
        
            if ev_tot[ph][1]:
                coul = COUL_OK
                t += u"POSSIBLE."
            else:
                coul = COUL_NON
                t += u"IMPOSSIBLE :"
                t += tt
            
            st.SetBackgroundColour(coul)
            st.SetToolTipString(t)
            
#        for ph, e, le, st, limT in zip([u"conduite", u"soutenance"],
#                                             [ev_tot['R'][0], ev_tot['S'][0]], 
#                                             [pas50r, pas50s],
#                                             [self.evaluR, self.evaluS], 
#                                             [0.5, 1.0]):
#            
#            t = u"Evaluabilité de la "+ph+u" du projet "
#            tt = u""
#            Ok = True
#            if e < limT:
#                Ok = Ok and False
#                tt += u"\n" + t1
#                
#            if len(le) == 1:
#                tt += u"\n" + t21 + t3 + t51 + le[0] + t4
#                Ok = Ok and False
#            elif len(le) > 1:
#                tt += u"\n" + t22 + t3 + t52 + " ".join(le) + t4
#                Ok = Ok and False
#            
#            if Ok:
#                coul = COUL_OK
#                t += u"POSSIBLE."
#            else:
#                coul = COUL_NON
#                t += u"IMPOSSIBLE :"
#                t += tt
#            
#            st.SetBackgroundColour(coul)
#            st.SetToolTipString(t)

        self.codeBranche.Layout()
        self.codeBranche.Fit()
    
    ######################################################################################  
    def SetCode(self):

        t = self.GetNomPrenom()

        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
            
        self.SetTip()
        
    ######################################################################################  
    def SetTip2(self):
        # Tip
        if hasattr(self, 'tip'):
            
#            self.tip.SetTexte(self.GetNomPrenom(), self.tip_nom)
            coulOK = constantes.GetCouleurHTML(COUL_OK)
            coulNON = constantes.GetCouleurHTML(COUL_NON)
            
            #
            # Durée
            #
            duree = self.GetDuree()
            lab = draw_cairo.getHoraireTxt(duree)
            if abs(duree-70) < constantes.DELTA_DUREE:
                coul = coulOK
            elif abs(duree-70) < constantes.DELTA_DUREE2:
                coul = constantes.GetCouleurHTML(COUL_BOF)
            else:
                coul = coulNON
            XML_AjouterCol(self.ficheXML, "ld", lab, coul, bold = True)
#            SetWholeText(self.ficheXML, "d", lab)
#            self.tip.SetTexte(rallonge(lab), self.tip_duree)
            
            #
            # Evaluabilité
            #
            ev, ev_tot, seuil = self.GetEvaluabilite()
            
            keys = sorted(self.GetReferentiel()._dicIndicateurs_prj.keys())
#            if "O8s" in keys:
#                keys.remove("O8s")
            
            
            labr = [[pourCent2(ev_tot['R'][0], True), True]]
#            totalOk = True
            for k in keys:
                if k in self.GetReferentiel()._lstGrpIndicateurRevues:
                    if k in ev['R'].keys():
                        
#                        totalOk = totalOk and (ler[k] >= 0.5)
                        labr.append([pourCent2(ev['R'][k][0], True), ev['R'][k][1]]) 
                    else:
#                        totalOk = False
                        labr.append([pourCent2(0, True), False]) 
                else:
                    labr.append(["", True])
            labr[0][1] = ev_tot['R'][1]#totalOk and (er >= 0.5)
                    
            labs = [[pourCent2(ev_tot['S'][0], True), True]]
#            totalOk = True
            for k in keys:
                if k in self.GetReferentiel()._lstGrpIndicateurSoutenance:
                    if k in ev['S'].keys():
#                        totalOk = totalOk and (ev['S'][k] >= 1)
                        labs.append([pourCent2(ev['S'][k][0], True), ev['S'][k][1]]) 
                    else:
#                        totalOk = False
                        labs.append([pourCent2(0, True), False]) 
                else:
                    labs.append(["", True])
            labs[0][1] = ev_tot['S'][1]#totalOk and (es >= 1)
 
            for i, lo in enumerate(labr):
                l, o = lo
                if i == 0:
                    size = None
                    bold = True
                    if o:
                        coul = coulOK
                    else:
                        coul = coulNON
                else:
                    size = 2
                    bold = False
                    if not o:
                        coul = coulNON
                    else:
                        coul = None
                XML_AjouterCol(self.ficheXML, "ler", l, coul, constantes.GetCouleurHTML(COUL_REVUE), size, bold)
                
#                SetWholeText(self.ficheXML, "r"+str(i), l)
                
                
            for i, lo in enumerate(labs):
                l, o = lo
                if i ==0:
                    size = None
                    bold = True
                    if o:
                        coul = coulOK
                    else:
                        coul = coulNON
                else:
                    size = 2
                    bold = False
                    if not o:
                        coul = coulNON
                    else:
                        coul = None
                XML_AjouterCol(self.ficheXML, "les", l, coul, constantes.GetCouleurHTML(COUL_SOUT), size, bold)
#                SetWholeText(self.ficheXML, "s"+str(i), l)
                
                
            for t in keys:
                XML_AjouterCol(self.ficheXML, "le", t, size = 2)
#                SetWholeText(self.ficheXML, str(i+1), t)
                
            
            self.tip.SetPage(self.ficheXML.toxml())
            

            
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
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
        
        self.SetCode()
        
        
        
####################################################################################
#
#   Classe définissant les propriétés d'un professeur
#
####################################################################################
class Prof(Personne):
    def __init__(self, projet, panelParent, ident = 0):
        self.titre = u"prof"
        self.code = "Prf"
        self.discipline = "Tec"
        self.referent = False
        
        Personne.__init__(self, projet, panelParent, ident)
        
        
    ######################################################################################  
    def GetFicheHTML(self):
        return """<HTML>
        <p style="text-align: center;"><font size="12"><b>Professeur</b></font></p>
        <p id="nom">NomPrénom</p>
        <p id="av"></p>
        <table border="0" width="300">
        <tbody>
        <tr id="spe" align="right" valign="top">
        <td width="110"><span style="text-decoration: underline;">Spécialité :</span></td>
        </tr>
        </tbody>
        </table>
        </HTML>
        """
        
        
    ######################################################################################  
    def SetDiscipline(self, discipline):
        self.discipline = discipline
        self.SetTip()
        self.MiseAJourCodeBranche()
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.projet.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.projet.SupprimerProf, item = itemArbre)]])
        
    ######################################################################################  
    def MiseAJourCodeBranche(self):
        self.arbre.SetItemBold(self.branche, self.referent)
        if self.discipline <> 'Tec':
            self.codeDisc.SetLabel(u" "+constantes.CODE_DISCIPLINES[self.discipline]+u" ")
            self.codeDisc.SetBackgroundColour(constantes.GetCouleurWx(constantes.COUL_DISCIPLINES[self.discipline]))
            self.codeDisc.SetToolTipString(constantes.NOM_DISCIPLINES[self.discipline])
        else:
            self.codeDisc.SetLabel(u"")
            self.codeDisc.SetBackgroundColour(constantes.GetCouleurWx(constantes.COUL_DISCIPLINES[self.discipline]))
            self.codeDisc.SetToolTipString(constantes.NOM_DISCIPLINES[self.discipline])
        
        self.codeBranche.Layout()
        self.codeBranche.Fit()
    
    ######################################################################################  
    def SetTip2(self):
        if hasattr(self, 'tip'):
            if self.discipline != 'Tec':
                coul = constantes.GetCouleurHTML(constantes.COUL_DISCIPLINES[self.discipline])
            else:
                coul = None
            XML_AjouterCol(self.ficheXML, "spe", constantes.NOM_DISCIPLINES[self.discipline], bcoul = coul)
            self.tip.SetPage(self.ficheXML.toxml())
        
        
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
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
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
        
        self.Freeze()
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
#            options.ouvrir(DEFAUT_ENCODING)
            try :
                options.ouvrir(DEFAUT_ENCODING)
            except:
                print "Fichier d'options corrompus ou inexistant !! Initialisation ..."
                options.defaut()
        else:
            options.defaut()
        self.options = options

        
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
        
        if sys.platform == "win32":
            self.Bind(wx.EVT_MENU, self.genererGrilles, id=17)
            
        self.Bind(wx.EVT_MENU, self.genererFicheValidation, id=19)
        
        if sys.platform == "win32":
            self.Bind(wx.EVT_MENU, self.etablirBilan, id=18)
            
        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)
        
        self.Bind(wx.EVT_MENU, self.OnAide, id=21)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=22)
        
        self.Bind(wx.EVT_MENU, self.OnOptions, id=31)
        
        if sys.platform == "win32" :
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
    
        # Element placé dans le "presse papier"
        self.elementCopie = None
        
        # Récupération de la dernière version
        wx.CallAfter(self.GetNewVersion)
        
        self.Thaw()
        
        
    ###############################################################################################
    def GetNewVersion(self):  
        # url = 'https://code.google.com/p/pysequence/downloads/list'
        print "Recherche nouvelle version ...",
        url = 'https://drive.google.com/folderview?id=0B2jxnxsuUscPX0tFLVN0cF91TGc#list'
        try:
            self.downloadPage = BeautifulSoup(urllib2.urlopen(url, timeout = 5))
        except IOError:
            print "pas d'accès Internet"
            return   

#        ligne = self.downloadPage.find('div', attrs={'class':"flip-entry-title"})
        ligne = self.downloadPage.find_all('div', attrs={'class':"flip-entry-title"})
#        fichier = ligne.text.strip()
        
        # Version actuelle
        vba = __version__.split("beta")
        va = vba[0]
        if len(va) >1:
            ba = vba[1]
        else:
            ba = 0
                    
        # version en ligne plus récente
        versionPlusRecente = False    
                    
        for l in ligne:
            if len(l.text.split('_')) > 1:
                v = l.text.split('_')[1].split('.zip')[0]
                vb = v.split("beta")
                vn = vb[0]
                if len(vn) >1:
                    bn = vb[1]
                else:
                    bn = 100
                
                if vn > va or (vn == va and bn > ba): # Nouvelle version disponible
                    versionPlusRecente = True
                    break
        print v
        
        if versionPlusRecente:
            dialog = wx.MessageDialog(self, u"Une nouvelle version de pySéquence est disponible\n\n" \
                                            u"\t%s\n\n" \
                                            u"Voulez-vous visiter la page de téléchargement ?" % v, 
                                          u"Nouvelle version", wx.YES_NO | wx.ICON_INFORMATION)
            retCode = dialog.ShowModal()
            if retCode == wx.ID_YES:
                try:
                    webbrowser.open(url,new=2)
                except:
                    messageErreur(None, u"Ouverture impossible",
                                  u"Impossible d'ouvrir l'url\n\n%s\n" %toDefautEncoding(self.path))

                    
                
#                dlg = wx.DirDialog(self, message = u"Emplacement du téléchargement", 
#                                style=wx.DD_DEFAULT_STYLE|wx.CHANGE_DIR
#                                )
#        
#                if dlg.ShowModal() == wx.ID_OK:
#                    path = dlg.GetPath()
#                    url = 'https://code.google.com/p/pysequence/downloads/'+ligne.a['href']
#                    filename, headers = urllib.urlretrieve(url, os.path.join(path, fichier))
#                    print filename
#                    dlg.Destroy()
#                else:
#                    dlg.Destroy()
                
       
    ###############################################################################################
    def SetData(self, data):  
        self.elementCopie = data      
        
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
        
        if sys.platform == "win32":
            file_menu.Append(17, u"&Générer les grilles d'évaluation projet\tCtrl+G")
        
        file_menu.Append(19, u"&Générer le dossier de validation projet\tAlt+V")
        
        if sys.platform == "win32":
            file_menu.Append(18, u"&Générer une Synthèse pédagogique (SSI et ETT uniquement)\tCtrl+B")
        
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, u"&Quitter\tCtrl+Q")

        self.file_menu = file_menu
        
        if sys.platform == "win32" :
            tool_menu = wx.Menu()
    #        tool_menu.Append(31, u"Options")
            
            self.menuReg = tool_menu.Append(32, u"a")
            self.MiseAJourMenu()
        

        help_menu = wx.Menu()
        help_menu.Append(21, u"&Aide en ligne\tF1")
        help_menu.AppendSeparator()
        help_menu.Append(22, u"A propos")

        mb.Append(file_menu, u"&Fichier")
        if sys.platform == "win32" :
            mb.Append(tool_menu, u"&Outils")
        mb.Append(help_menu, u"&Aide")
        
        self.SetMenuBar(mb)
    
    
    #############################################################################
    def MiseAJourMenu(self):
        if hasattr(self, 'menuReg'):
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
        try:
            webbrowser.open('http://code.google.com/p/pysequence/wiki/Aide',new=2)
        except:
            messageErreur(None, u"Ouverture impossible",
                          u"Impossible d'ouvrir l'url\n\n%s\n" %toDefautEncoding(self.path))

        
        
    ###############################################################################################
    def commandeNouveau(self, event = None, ext = None, ouverture = False):
        if ext == 'seq':
            child = FenetreSequence(self, ouverture)
        elif ext == 'prj':
            child = FenetreProjet(self)
        else:
            dlg = DialogChoixDoc(self)
            val = dlg.ShowModal()
            if val == 1:
                child = FenetreSequence(self, ouverture)  
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
            
            # Fichier pas déja ouvert
            if not nomFichier in self.GetNomsFichiers():
                wx.BeginBusyCursor()
                child = self.commandeNouveau(ext = ext, ouverture = True)
                if child != None:
                    child.ouvrir(nomFichier)
                wx.EndBusyCursor()
#                wx.CallAfter(wx.EndBusyCursor)
                
            # Fichier déja ouvert
            else:
                child = self.GetChild(nomFichier)
                texte = constantes.MESSAGE_DEJA[ext] % child.fichierCourant
#                if child.fichierCourant != '':
#                    texte += "\n\n\t"+child.fichierCourant+"\n"
                    
                dialog = wx.MessageDialog(self, texte, 
                                          u"Confirmation", wx.YES_NO | wx.ICON_WARNING)
                retCode = dialog.ShowModal()
                if retCode == wx.ID_YES:
                    wx.BeginBusyCursor()
                    child.ouvrir(nomFichier)
                    wx.EndBusyCursor()
        
        
        
    ###############################################################################################
    def commandeOuvrir(self, event = None, nomFichier=None):
        mesFormats = constantes.FORMAT_FICHIER['seqprj'] + constantes.FORMAT_FICHIER['seq'] + constantes.FORMAT_FICHIER['prj'] + constantes.TOUS_FICHIER
  
        if nomFichier == None:
            dlg = wx.FileDialog(
                                self, message=u"Ouvrir une séquence ou un projet",
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
        """ Opérations de modification du menu et des barres d'outil 
            en fonction du type de document en cours
        """
        doc = self.GetClientWindow().GetAuiManager().GetManagedWindow().GetCurrentPage()
        if hasattr(doc, 'typ'):
            
            if doc.typ == "prj":
                self.ajouterOutilsProjet()
                self.Bind(wx.EVT_TOOL, doc.projet.AjouterEleve, id=50)
                self.Bind(wx.EVT_TOOL, doc.projet.AjouterProf, id=51)
                self.Bind(wx.EVT_TOOL, doc.AjouterTache, id=52)
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
        
#        wx.CallAfter(self.Layout)
        self.Layout()

         

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
        t = REFERENTIELS[t].Enseignement[0]
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
            texte = constantes.MESSAGE_FERMER[self.typ] % self.fichierCourant
#            if self.fichierCourant != '':
#                texte += "\n\n\t"+self.fichierCourant+"\n"
                
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
            
        doc.writexml(f, '   ', encoding = "utf-8")
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
    def __init__(self, parent, ouverture = False):
        self.typ = 'seq'
        FenetreDocument.__init__(self, parent)
        
        #
        # La classe
        #
        self.classe = Classe(parent, self.panelProp, ouverture = ouverture)
        
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
        constantes.indent(root)
        
        ET.ElementTree(root).write(fichier, encoding = DEFAUT_ENCODING)
        
        fichier.close()
        self.definirNomFichierCourant(nomFichier)
        self.MarquerFichierCourantModifie(False)
        wx.EndBusyCursor()
        
        
        
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True):
        print "ouvrir sequence"
        if not os.path.isfile(nomFichier):
            return
        
        self.Freeze()
        fichier = open(nomFichier,'r')
        self.definirNomFichierCourant(nomFichier)
        nomCourt = os.path.splitext(os.path.split(nomFichier)[1])[0]
        
#        try:
        root = ET.parse(fichier).getroot()
        
        # La séquence
        sequence = root.find("Sequence")
        if sequence == None:
            self.sequence.setBranche(root)
        else:
            # La classe
            classe = root.find("Classe")
            self.classe.setBranche(classe)
            self.sequence.MiseAJourTypeEnseignement()
            self.sequence.setBranche(sequence)  
                
          
#        except:
#            messageErreur(self,u"Erreur d'ouverture",
#                          u"La séquence pédagogique\n    %s\n n'a pas pu être ouverte !" %nomCourt)
#            fichier.close()
#            self.Close()
#            return



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
        
        self.Freeze()
        
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
        
        self.Thaw()
   
    
    ###############################################################################################
    def AjouterTache(self, event = None):
        self.arbre.AjouterTache()
        
        
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
        constantes.indent(root)
        
#        print ET.tostring(projet)#, encoding="utf8",  method="xml")
        try:
            ET.ElementTree(root).write(fichier, encoding = DEFAUT_ENCODING)
        except IOError:
            messageErreur(None, u"Accès refusé", 
                                  u"L'accès au fichier %s a été refusé !\n\n"\
                                  u"Essayer de faire \"Enregistrer sous...\"" %nomFichier)
        except UnicodeDecodeError:
            messageErreur(None, u"Erreur d'encodage", 
                                  u"Un caractère spécial empêche l'enregistrement du fichier !\n\n"\
                                  u"Essayer de le localiser et de le supprimer.\n"\
                                  u"Merci de reporter cette erreur au développeur.")
            
        fichier.close()
        self.definirNomFichierCourant(nomFichier)
        self.MarquerFichierCourantModifie(False)
        wx.EndBusyCursor()
        
        
        
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True):
        print "Ouverture projet", nomFichier
        tps1 = time.clock()
        
        # Pour le suivi de l'ouverture
        nomCourt = os.path.splitext(os.path.split(nomFichier)[1])[0]
        
        message = nomCourt+"\n"
        dlg =    wx.ProgressDialog(u"Ouverture d'un projet",
                                   message,
                                   maximum = 11,
                                   parent=self.parent,
                                   style = 0
                                    | wx.PD_APP_MODAL
                                    #| wx.PD_CAN_ABORT
                                    #| wx.PD_CAN_SKIP
                                    #| wx.PD_ELAPSED_TIME
                                    | wx.PD_ESTIMATED_TIME
                                    | wx.PD_REMAINING_TIME
                                    #| wx.PD_AUTO_HIDE
                                    )

        self.Freeze()
        
        self.fiche.Hide()
        
        fichier = open(nomFichier,'r')
        self.definirNomFichierCourant(nomFichier)
        
        
        
        
        def ouvre(fichier, message):
            root = ET.parse(fichier).getroot()
            count = 0
            Ok = True
            err = 0
            
            # Le projet
            projet = root.find("Projet")
            if projet == None:
                self.projet.setBranche(root)
                
            else:
                # La classe
                message += u"Construction de la structure de la classe..."
                dlg.Update(count, message)
                count += 1
                classe = root.find("Classe")
                Ok = Ok and self.classe.setBranche(classe)
                message += constantes.getOkErr(Ok) + u"\n"
                
                if not self.classe.version5:
                    messageErreur(None, u"Ancien programme", 
                                  u"Projet enregistré avec les indicateurs de compétence antérieurs à la session 2014\n\n"\
                                  u"Les indicateurs de compétence ne seront pas chargés.")
                
                # Le projet
                message += u"Construction de la structure du projet..."
                dlg.Update(count, message)
                count += 1
                o,err = self.projet.setBranche(projet)
                Ok = Ok and o
                message += constantes.getOkErr(Ok) + u"\n"
                
            self.arbre.DeleteAllItems()
            root = self.arbre.AddRoot("")
            
            message += u"Traitement des revues\n"
            dlg.Update(count, message)
            count += 1
            if err == 0:
                try:
                    self.projet.SetCompetencesRevuesSoutenance()
                except:
                    print "Erreur 4"
                        
            return root, message, count, Ok, err
        
        
        if "beta" in __version__:
#            print "beta"
            root, message, count, Ok, err = ouvre(fichier, message)
        else:
            try:
                root, message, count, Ok, err = ouvre(fichier, message)
            except:
                Ok = False
        
#        if not Ok:
#            m = u"Le projet\n    %s\nn'a pas pu être ouvert !" \
#                u"\n\nIl s'agit peut-être d'un fichier d'une ancienne version de pySequence.\n" %nomCourt
#            
#            if err != 0:
#                m += u"\n   L'erreur concerne :"
#                for c,e in constantes.ERREURS.items():
#                    if err & c:
#                        m += u"\n   "+e
#              
#            messageErreur(self, u"Erreur d'ouverture", m)
#            fichier.close()
#            self.Close()
#            dlg.Destroy()
#            return
        
        message += u"Construction de l'arborescence de la classe\n"
        dlg.Update(count, message)
        count += 1
        self.classe.ConstruireArbre(self.arbre, root)
        
        message += u"Construction de l'arborescence du projet\n"
        dlg.Update(count, message)
        count += 1
        self.projet.ConstruireArbre(self.arbre, root)
        
        message += u"Ordonnancement des tâches\n"
        dlg.Update(count, message)
        count += 1
        self.projet.OrdonnerTaches()
        
        message += u"Traitement des descriptions\n"
        dlg.Update(count, message)
        count += 1
        self.projet.PubDescription()
        
        message += u"Construction des liens\n"
        dlg.Update(count, message)
        count += 1
        self.projet.SetLiens()
        
        message += u"Ajout des durées/évaluabilités dans l'arbre\n"
        dlg.Update(count, message)
        count += 1
        self.projet.MiseAJourDureeEleves()
        
        message += u"Ajout des disciplines dans l'arbre\n"
        dlg.Update(count, message)
        count += 1
        self.projet.MiseAJourNomProfs()

        self.projet.VerrouillerClasse()

        message += u"Tracé de la fiche..."
        dlg.Update(count, message)
        count += 1

#        self.arbre.SelectItem(self.classe.branche)

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        
        fichier.close()
        dlg.Destroy()
        
        self.Thaw()
   
        
        wx.CallAfter(self.fiche.Show)
        wx.CallAfter(self.fiche.Redessiner)
#        if redessiner:
#            

        tps2 = time.clock() 
        print "Ouverture :", tps2 - tps1


    


    #############################################################################
    def genererGrilles(self, event = None):
        """ Génération de toutes les grilles d'évaluation
             - demande d'un dossier -
        """
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
            
            nomFichiers = {}
            for e in self.projet.eleves:
                nomFichiers[e.id] = e.GetNomGrilles(path = path)
            
            if not self.projet.TesterExistanceGrilles(nomFichiers):
                dlgb.Destroy()
                return
            
            for e in self.projet.eleves:
                e.GenererGrille(nomFichiers = nomFichiers[e.id], messageFin = False)
                dlgb.Update(count, u"Traitement de la grille de \n\n"+e.GetNomPrenom())
                dlgb.Refresh()
                count += 1
                dlgb.Refresh()
           
            
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

            try:
                genpdf.genererDossierValidation(nomFichier, self.projet, self)
                os.startfile(nomFichier)
            except IOError:
                messageErreur(self, u"Erreur !",
                                  u"Impossible d'enregistrer le fichier.\n\nVérifier :\n" \
                                  u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
                                  u" - que le dossier choisi n'est pas protégé en écriture\n\n" \
                                  + nomFichier)
                wx.EndBusyCursor()
            
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
        w = self.GetClientSize()[0]
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
            self.GetDoc().SelectItem(branche, depuisFiche = True)
            

        #
        # Autres actions
        #
        position = self.GetDoc().HitTestPosition(xx, yy)
        if position != None:
            if hasattr(self, 'projet'):
                self.projet.SetPosition(position)
            else:
                self.sequence.SetPosition(position)
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
        w,h = self.GetVirtualSize()
        self.buffer = wx.EmptyBitmap(w,h)


    #############################################################################            
    def Redessiner(self, event = None):  
        wx.BeginBusyCursor()
        tps1 = time.clock() 
            
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

        tps2 = time.clock() 
        print "Tracé :", tps2 - tps1
        
        wx.EndBusyCursor()
    
    #############################################################################            
    def normalize(self, cr):
        h = self.GetVirtualSize()[1]
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
        popup = PopupInfo2(self.projet.GetApp(), u"Compétence")
        popup.sizer.SetItemSpan(popup.titre, (1,2)) 
        l += 1
        
        self.tip_comp = popup.CreerTexte((l,0), (1,2), flag = wx.ALL)
        self.tip_comp.SetForegroundColour("CHARTREUSE4")
        self.tip_comp.SetFont(wx.Font(11, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        l += 1
        
        self.tip_arbre = popup.CreerArbre((l,0), (1,2), projet.GetReferentiel(), flag = wx.ALL)
        l += 1
        
#        self.tip_compp = popup.CreerTexte((l,0), (1,2), flag = wx.ALL)
#        self.tip_compp.SetForegroundColour("CHARTREUSE3")
#        self.tip_compp.SetFont(wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
#        l += 1
#            
#        self.lab_indic = popup.CreerTexte((l,0), txt = u"Indicateur :", flag = wx.ALIGN_RIGHT|wx.RIGHT)
#        self.lab_indic.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline = True))
#        self.tip_indic = []
#        l += 1
        
        self.lab_legend1 = popup.CreerTexte((l,0), txt = u"Conduite", flag = wx.ALIGN_RIGHT|wx.RIGHT)
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
#                for tip in self.tip_indic:
#                    tip.Destroy()
#                self.tip_indic = []
                x, y = self.ClientToScreen((x, y))
#                type_ens = self.projet.classe.typeEnseignement
                ref = self.projet.GetReferentiel()
                competence = ref.getCompetence_prj(kComp)
#                print "competence", kComp, competence
#                indicTache = obj.GetDicIndicateurs()
                
#                ###################################################################
#                def afficherIndic(listIndic, codeComp, ligne):
#                    print "   afficherIndic", codeComp, ligne, len(listIndic)
#                    
#                    for i, indic in enumerate(listIndic):
#                        intit = indic[0]
#                        poids = indic[1]
#                        if codeComp in indicTache and indicTache[codeComp][i]:
#                            if poids[1] != 0:
#                                coul = constantes.COUL_REVUE
#                            else:
#                                coul = constantes.COUL_SOUT
#                        else:
#                            coul = "GREY"
#                        self.tip_indic.append(self.popup.CreerTexte((3+i+ligne[0],1), flag = wx.ALIGN_LEFT|wx.LEFT))
#                        self.tip_indic[-1].SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
#                        self.tip_indic[-1].SetForegroundColour(coul)
#    
#                        self.popup.SetTexte(textwrap.fill(intit, 50), self.tip_indic[-1])
#                        ligne[0] += 1
                        
                intituleComp = competence[0]
                
                k = kComp.split(u"\n")
                if len(k) > 1:
                    titre = u"Compétences\n"+u"\n".join(k)
                else:
                    titre = u"Compétence\n"+k[0]
                self.popup.SetTitre(titre)
                
                
#                cc = [cd+ " " + it for cd, it in zip(k.split(u"\n"), v[0].split(u"\n"))] 
#                comp = self.AppendItem(br, textwrap.fill(u"\n ".join(cc), 50))
#                    
                intituleComp = "\n".join([textwrap.fill(ind, 50) for ind in intituleComp.split(u"\n")]) 
             
                self.popup.SetTexte(intituleComp, self.tip_comp)
                
                self.tip_arbre.DeleteChildren(self.tip_arbre.root)
                self.tip_arbre.Construire(dic = competence[1])
                
                self.popup.Fit()
#                self.tip_arbre.AdapterSize()
                
#                if type(competence[1]) == list:
#                    indicateurs = competence[1]
#                    
#                    self.popup.DeplacerItem(self.lab_legend1, (4+len(indicateurs), 0))
#                    self.popup.DeplacerItem(self.lab_legend2, (4+len(indicateurs), 1))
#                
#                    afficherIndic(indicateurs, kComp, [0])
#                    
#                else:
#                    l = 0
#                    for v in competence[1].values():
#                        l += len(v[1])
#                    print "   ", l
#                    self.popup.DeplacerItem(self.lab_legend1, (4+l, 0))
#                    self.popup.DeplacerItem(self.lab_legend2, (4+l, 1))
#                    ligne = [0]
#                    for k, v in competence[1].items():
#                        afficherIndic(v[1], k, ligne)
                
##                competence = ref._dicIndicateurs_prj_simple[kComp][0]
#                competence = ref.getIntituleCompetence(kComp, sousComp = True)
##                if ref.prof_Comp > 1:
##                    competencePlus = competence[1:]
#                
#                
#                self.MiseAJourTypeEnseignement(type_ens)
#                
##                indicateurs = ref._dicIndicateurs_prj_simple[kComp]
#                indicateurs = ref.getIndicateur(kComp)
#          
#                self.popup.SetTitre(u"Compétence "+kComp)
#                self.popup.SetTexte(textwrap.fill(competence, 50), self.tip_comp)
#                
##                if ref.prof_Comp > 1:
##                    t = ''
##                    for cp in competencePlus:
##                        t += textwrap.fill(CHAR_POINT + " " + cp, 50)+"\n"
##                    self.popup.SetTexte(t, self.tip_compp)
#                
#                self.popup.DeplacerItem(self.lab_legend1, (4+len(indicateurs), 0))
#                self.popup.DeplacerItem(self.lab_legend2, (4+len(indicateurs), 1))
#                    
#                
#                
#                    
#                if type(indicateurs) == list:
#                    afficherIndic(indicateurs, kComp, 0)
#                else:
#                    for k, v in indicateurs.items():
#                        afficherIndic(v[1], k, ligne)
                    
                    
                    
                self.popup.Position((x,y), (0,0))
                self.call = wx.CallLater(500, self.popup.Show, True)
                self.tip = self.popup
            
        evt.Skip()


    #############################################################################
    def MiseAJourTypeEnseignement(self, type_ens):
        texte = u"Indicateur"
#        ref = self.projet.GetReferentiel()
#        if ref.prof_Comp <= 1:
#            texte += u"s"
#        self.popup.SetTexte(texte, self.lab_indic)
#        self.tip_compp.Show(ref.prof_Comp > 1)
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
#class PanelProprieteBook(wx.Notebook, PanelPropriete):
#    def __init__(self, parent, titre = u"", objet = None):
#        wx.Notebook.__init__(self, parent, -1,  style= wx.BK_DEFAULT)#| wx.BORDER_SIMPLE)
#        self.eventAttente = False
##        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
#
#
#    def OnPageChanged(self, event):
##        old = event.GetOldSelection()
##        new = event.GetSelection()
##        sel = self.GetSelection()
#        
#        event.Skip()

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
        
        self.rtc = rt.RichTextCtrl(self, style=rt.RE_READONLY|wx.NO_BORDER)#
        wx.CallAfter(self.rtc.SetFocus)
        
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.rtc, 1,flag = wx.EXPAND)
        self.SetSizer(sizer)

        out = cStringIO.StringIO()
        handler = rt.RichTextXMLHandler()
        buff = self.rtc.GetBuffer()
#        buff.AddHandler(handler)
        out.write(texte)
        out.seek(0)
        handler.LoadStream(buff, out)
        self.rtc.Refresh()
        
        sizer.Layout()
#        wx.CallAfter(self.Layout)
        self.Layout()


     

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
#        wx.CallAfter(self.Layout)
        self.Layout()
        
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
        self.position.SetValue(self.sequence.position)
        self.bmp.SetBitmap(self.getBitmapPeriode(250))
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
        
        nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
        
        #
        # La page "Généralités"
        #
        pageGen = PanelPropriete(nb)
        bg_color = self.Parent.GetBackgroundColour()
        pageGen.SetBackgroundColour(bg_color)
        self.pageGen = pageGen
        
        nb.AddPage(pageGen, u"Propriétés générales")
        
#        pageGen.sizer.Add(nb, (0,1), (2,1), flag = wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND, border = 1)
            
        #
        # Intitulé du projet
        #
        titre = wx.StaticBox(pageGen, -1, u"Intitulé du projet")
        sb = wx.StaticBoxSizer(titre)
        textctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        pageGen.sizer.Add(sb, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
#        self.sizer.Add(textctrl, (0,1), flag = wx.EXPAND)
        pageGen.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        #
        # Problématique
        #
        titre = wx.StaticBox(pageGen, -1, u"Problématique - Énoncé général du besoin")
        sb = wx.StaticBoxSizer(titre)
        commctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
        commctrl.SetToolTipString(constantes.TIP_PROBLEMATIQUE + constantes.TIP_PB_LIMITE)
        sb.Add(commctrl, 1, flag = wx.EXPAND)
        self.commctrl = commctrl
        pageGen.sizer.Add(sb, (0,1), (2,1),  flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
#        self.sizer.Add(commctrl, (1,1), flag = wx.EXPAND)
        pageGen.Bind(wx.EVT_TEXT, self.EvtText, commctrl)
        pageGen.sizer.AddGrowableCol(1)
        
        
        #
        # Année scolaire et Position dans l'année
        #
        titre = wx.StaticBox(pageGen, -1, u"Année et Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        
        self.annee = Variable(u"", lstVal = self.projet.annee, 
                                   typ = VAR_ENTIER_POS, bornes = [2012,2100])
        self.ctrlAnnee = VariableCtrl(pageGen, self.annee, coef = 1, signeEgal = False,
                                      help = u"Année scolaire", sizeh = 40, 
                                      unite = str(self.projet.annee+1),
                                      sliderAGauche = True)
        self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlAnnee)
        sb.Add(self.ctrlAnnee)
        
        self.bmp = wx.StaticBitmap(pageGen, -1, self.getBitmapPeriode(250))
        position = wx.Slider(pageGen, -1, self.projet.position, 0, 5, (30, 60), (190, -1), 
            wx.SL_HORIZONTAL | wx.SL_TOP)#wx.SL_AUTOTICKS |
        sb.Add(self.bmp)
        sb.Add(position)
        self.position = position
        pageGen.sizer.Add(sb, (1,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.EXPAND|wx.LEFT, border = 2)
        position.Bind(wx.EVT_SCROLL_CHANGED, self.onChanged)
        
        #
        # Organisation (nombre et positions des revues)
        #
        self.panelOrga = PanelOrganisation(pageGen, self, self.projet)
        pageGen.sizer.Add(self.panelOrga, (0,2), (2,1), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.EXPAND|wx.LEFT, border = 2)
        
        
        pageGen.sizer.AddGrowableRow(0)
#        pageGen.FitInside()
#        pageGen.sizer.Layout()
#        wx.CallAfter(pageGen.Layout)
#        
#        wx.CallAfter(pageGen.PostSizeEvent)
        
        #
        # La page "Enoncé général du besoin"
        #
        pageBG = PanelPropriete(nb)
        bg_color = self.Parent.GetBackgroundColour()
        pageBG.SetBackgroundColour(bg_color)
        self.pageBG = pageBG
        
        nb.AddPage(pageBG, u"Origine")
        
        self.bgctrl = wx.TextCtrl(pageBG, -1, u"", style=wx.TE_MULTILINE)
#        self.bgctrl = richtext.RichTextPanel(pageBG, [u""], toolBar = True)
        
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
#        self.sizer.Layout()
        
        self.Layout()
        self.FitInside()
        wx.CallAfter(self.PostSizeEvent)
        self.Show()
        
#        self.Fit()
        
    
    #############################################################################            
    def getBitmapPeriode(self, larg):
        w, h = 0.04*7, 0.04
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
        elif var == self.annee:
            self.projet.annee = var.v[0]
            self.ctrlAnnee.unite.SetLabel(str(self.projet.annee+1)) 
        
            
              
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
            nt = event.GetString()[:constantes.LONG_MAX_PROBLEMATIQUE]
            self.projet.SetProblematique(nt)
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
        
        self.panelOrga.MiseAJourListe()
        self.Layout()
        
        if sendEvt:
            self.sendEvent()

    #############################################################################            
    def GetDocument(self):
        return self.projet
    
    
class PanelOrganisation(wx.Panel):    
    def __init__(self, parent, panel, objet):
        wx.Panel.__init__(self, parent, -1)
        self.objet = objet
        self.parent = panel
        
        sizer = wx.BoxSizer()
        gbsizer = wx.GridBagSizer()
        titre = wx.StaticBox(self, -1, u"Organisation")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)

        self.nbrRevues = Variable(u"Nombre de revues",  
                                   lstVal = self.objet.nbrRevues, 
                                   typ = VAR_ENTIER_POS, bornes = [2,3])
        self.ctrlNbrRevues = VariableCtrl(self, self.nbrRevues, coef = 1, signeEgal = False,
                                help = u"Nombre de revues de projet (avec évaluation)", sizeh = 30)
        self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlNbrRevues)
        gbsizer.Add(self.ctrlNbrRevues, (0,0), (1,2), flag = wx.EXPAND)
        
        liste = wx.ListBox(self, -1, choices = self.objet.GetListeNomsPhases(), style = wx.LB_SINGLE)
        liste.SetToolTipString(u"Séléctionner la revue à déplacer")
        gbsizer.Add(liste, (1,0), (2,1), flag = wx.EXPAND)
        self.liste = liste
        self.Bind(wx.EVT_LISTBOX, self.EvtListBox, self.liste)
        
        buttonUp = wx.BitmapButton(self, 11, wx.ArtProvider.GetBitmap(wx.ART_GO_UP), size = (20,20))
        gbsizer.Add(buttonUp, (1,1), (1,1))
        self.Bind(wx.EVT_BUTTON, self.OnClick, buttonUp)
        buttonUp.SetToolTipString(u"Monter la revue")
        self.buttonUp = buttonUp
        
        buttonDown = wx.BitmapButton(self, 12, wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN), size = (20,20))
        gbsizer.Add(buttonDown, (2,1), (1,1))
        self.Bind(wx.EVT_BUTTON, self.OnClick, buttonDown)
        buttonDown.SetToolTipString(u"Descendre la revue")
        self.buttonDown = buttonDown
        
        gbsizer.AddGrowableRow(1)
        sb.Add(gbsizer, flag = wx.EXPAND)
        
        sizer.Add(sb, flag = wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
        
    #############################################################################            
    def EvtListBox(self, event):
        ref = self.objet.GetReferentiel()
        if ref.getClefDic('phases_prj', self.liste.GetString(event.GetSelection()), 0) in ["R1", "R2", "R3"]:
            self.buttonUp.Enable(True)
            self.buttonDown.Enable(True)
        else:
            self.buttonUp.Enable(False)
            self.buttonDown.Enable(False)
            
            
        
    #############################################################################            
    def OnClick(self, event):
        i = event.GetId()
        revue = self.liste.GetStringSelection()
        ref = self.objet.GetReferentiel()
        
        if revue[:5] == "Revue":
            posRevue = self.liste.GetSelection()
            numRevue = eval(revue[-1])
            if i == 11 and posRevue-2 >= 0:
                nouvPosRevue = posRevue-2
            elif i == 12 and posRevue < self.liste.GetCount() - 1:
                nouvPosRevue = posRevue+1
            else:
                return
            itemPrecedent = ref.getClefDic('phases_prj', self.liste.GetString(nouvPosRevue), 0)
#            itemPrecedent = constantes.getCodeNomCourt(self.liste.'(nouvPosRevue), 
#                                                       self.objet.GetTypeEnseignement(simple = True))
            j=1
            while itemPrecedent in ["R1", "R2", "R3"]:
                itemPrecedent = ref.getClefDic('phases_prj', self.liste.GetString(nouvPosRevue-j), 0)
#                itemPrecedent = constantes.getCodeNomCourt(self.liste.GetString(nouvPosRevue-j),
#                                                           self.objet.GetTypeEnseignement(simple = True))
                j += 1
            self.objet.positionRevues[numRevue-1] = itemPrecedent
        else:
            return
          
        self.MiseAJourListe()
        self.liste.SetStringSelection(revue)
        if hasattr(self.objet, 'OrdonnerTaches'):
            self.objet.OrdonnerTaches()
            self.parent.sendEvent()
        
    #############################################################################            
    def MiseAJourListe(self):
#        print "MiseAJourListe"
#        print self.objet.GetListeNomsPhases()
        self.liste.Set(self.objet.GetListeNomsPhases())
        self.Layout()
        
    #############################################################################            
    def EvtVariable(self, event):
        var = event.GetVar()
        if var == self.nbrRevues:
            if var.v[0] != self.objet.nbrRevues:
                self.objet.nbrRevues = var.v[0]
                self.objet.MiseAJourNbrRevues()
                self.MiseAJourListe()
                self.parent.sendEvent()
        
####################################################################################
#
#   Classe définissant le panel de propriété de la classe
#
####################################################################################
class PanelPropriete_Classe(PanelPropriete):
    def __init__(self, parent, classe, pourProjet, ouverture = False):
#        print "__init__ PanelPropriete_Classe"
        PanelPropriete.__init__(self, parent)
#        self.BeginRepositioningChildren()
        
        if not pourProjet:  # Séquence
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
            self.nb = nb
            
        else:               # Projet
            #
            # Pas de NoteBook
            #
            pageGen = self
            self.pageGen = pageGen
        
        self.classe = classe
        self.pasVerrouille = True
        
        #
        # La barre d'outils
        #
        self.tb = tb = wx.ToolBar(self, style = wx.TB_VERTICAL|wx.TB_FLAT|wx.TB_NODIVIDER)
        self.sizer.Add(tb, (0,0), (2,1), flag = wx.ALL|wx.ALIGN_RIGHT, border = 1)
        tb.AddSimpleTool(30, images.Icone_valid_pref.GetBitmap(),
                         u"Choisir ces paramètres de classe pour les futurs documents")
        self.Bind(wx.EVT_TOOL, self.OnValidPref, id=30)
        tb.AddSimpleTool(31, images.Icone_defaut_pref.GetBitmap(), 
                         u"Rétablir les paramètres de classe par défaut")
        self.Bind(wx.EVT_TOOL, self.OnDefautPref, id=31)

        tb.Realize()
        
        #
        # Type d'enseignement
        #
        self.pourProjet = pourProjet
        titre = wx.StaticBox(pageGen, -1, u"Type d'enseignement")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        te = ArbreTypeEnseignement(pageGen, self)

        sb.Add(te, 1, flag = wx.EXPAND)
#        l = []
#        for i, e in enumerate(REFERENTIELS.keys()):
#            l.append(REFERENTIELS[e].Enseignement[0])
#        rb = wx.RadioBox(
#                pageGen, -1, u"Type d'enseignement", wx.DefaultPosition, (130,-1),
#                l,
#                1, wx.RA_SPECIFY_COLS
#                )
#        rb.SetToolTip(wx.ToolTip(u"Choisir le type d'enseignement"))
#        for i, e in enumerate(REFERENTIELS.keys()):
#            rb.SetItemToolTip(i, REFERENTIELS[e].Enseignement[1])
        pageGen.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, te)
 
        te.SetStringSelection(REFERENTIELS[constantes.TYPE_ENSEIGNEMENT_DEFAUT].Enseignement[0])

        pageGen.sizer.Add(sb, (0,1), flag = wx.EXPAND|wx.ALL, border = 2)#
        self.cb_type = te

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

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboEtab, self.cb)
        sb.Add(self.cb, flag = wx.EXPAND)

        textctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
        pageGen.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
#        textctrl.SetMinSize((-1, 150))
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        
        self.info = wx.StaticText(pageGen, -1, u"""Inscrire le nom de l'établissement dans le champ ci-dessus...
        ou bien modifier le fichier "etablissements.txt" pour le faire apparaitre dans la liste.""")
        self.info.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
        sb.Add(self.info, 0, flag = wx.EXPAND|wx.ALL, border = 5)

        pageGen.sizer.Add(sb, (0,2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, border = 2)
        
        #
        # Effectifs
        #
        self.ec = PanelEffectifsClasse(pageGen, classe)
        pageGen.sizer.Add(self.ec, (0,3), flag = wx.ALL|wx.EXPAND, border = 2)#|wx.ALIGN_RIGHT

        pageGen.sizer.AddGrowableRow(0)
        pageGen.sizer.AddGrowableCol(2)
#        pageGen.sizer.Layout()

        #
        # Centres d'intérêt
        #
        if not pourProjet:
            pageCI= wx.Panel(nb, -1)
            sizer = wx.BoxSizer()
            pageCI.SetSizer(sizer)

            self.pageCI = pageCI
            self.nb.AddPage(pageCI, u"")

#            wx.CallAfter(self.InitListe)
#            wx.CallAfter(self.MiseAJourToolbar)
            
#            if not ouverture:
#                self.InitListe()
#                self.MiseAJourToolbar()
            
            self.leftDown = False
            
            self.sizer.AddGrowableRow(0)
            self.sizer.AddGrowableCol(1)
        
#        self.EndRepositioningChildren()
    
        pageGen.Bind(wx.EVT_SIZE, self.OnResize)
#        wx.CallAfter(self.OnResize)
        
        
    ######################################################################################              
    def OnResize(self, evt = None):
#        print "Resize ArbreTypeEnseignement", self.cb_type.GetVirtualSize()
        self.cb_type.SetMinSize(self.cb_type.GetVirtualSize())
        self.pageGen.sizer.Layout()
        if evt:
            evt.Skip()
    
    
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
    def EvtComboEtab(self, evt):       
        if evt.GetSelection() == len(constantes.ETABLISSEMENTS_PDD):
            self.classe.etablissement = self.textctrl.GetStringSelection()
            self.AfficherAutre(True)
        else:
            self.classe.etablissement = evt.GetString()
            self.AfficherAutre(False)
        
        self.sendEvent()
     
    ######################################################################################  
    def AfficherAutre(self, montrer):
        self.textctrl.Show(montrer)
        self.info.Show(montrer)
             
    ######################################################################################  
    def EvtRadioBox(self, event):
        """ Sélection d'un type d'enseignement
        """
        radio_selected = event.GetEventObject()

        fam = self.classe.familleEnseignement
        
        self.classe.typeEnseignement, self.classe.familleEnseignement = Referentiel.getEnseignementLabel(radio_selected.GetLabel())
        self.classe.referentiel = REFERENTIELS[self.classe.typeEnseignement]
        
#        for c, e in [r.Enseignement[1:] for r in REFERENTIELS]constantes.Enseignement.items():
#            if e[0] == :
#                self.classe.typeEnseignement = c
#                self.classe.familleEnseignement = constantes.FamilleEnseignement[self.classe.typeEnseignement]
#                break
        
        self.classe.MiseAJourTypeEnseignement()
        self.classe.doc.MiseAJourTypeEnseignement(fam != self.classe.familleEnseignement)
#        self.MiseAJourType()
#        if hasattr(self, 'list'):
#            self.list.Peupler()
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
        
    
#    ######################################################################################  
#    def InitListe(self):
#        if hasattr(self, 'list'):
#            self.pageCI.GetSizer().Detach(self.list)
#            self.list.Destroy()
#            
#        ref = REFERENTIELS[self.classe.typeEnseignement]
#        if ref.CI_BO and (ref.tr_com == None or REFERENTIELS[ref.tr_com[0]].CI_BO):
#            self.pageCI.Show(False)
#        else:
#            self.list = ListeCI(self.pageCI, self.classe)
#            if not ref.CI_BO:
#                self.nb.SetPageText(1, u"Centres d'intérêt ")
#            else:
#                self.nb.SetPageText(1, u"Centres d'intérêt " + ref.tr_com[0])
#    #        if self.classe.typeEnseignement == "SSI":
#    #            self.nb.SetPageText(1, u"Centres d'intérêt")
#    #        else:
#    #            self.nb.SetPageText(1, u"Centres d'intérêt ETT" + REFERENTIELS[self.classe.typeEnseignement].self.tr_com[0])
#                
#            self.list.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
#            self.list.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
#            
#            self.pageCI.GetSizer().Add(self.list, 1, flag = wx.EXPAND|wx.ALL, border = 2)
    
    
#    ######################################################################################  
#    def MiseAJourType(self):
#        """ Modification de la barre d'outil et de la liste des CI
#            en fonction du type d'enseignement
#        """
##        print "MiseAJourType"
##        if hasattr(self, 'list'):
##            self.InitListe()
##            self.MiseAJourToolbar()
#            
#        self.Layout()
#        self.sizer.Layout()
#        self.Refresh()
#         
#        
#    ######################################################################################  
#    def MiseAJourToolbar(self):
##        print "MiseAJourToolbar", self.pasVerrouille, self.classe.familleEnseignement
#        if self.classe.familleEnseignement == 'STI':
#            self.list.Show(True)
#            enable = self.pasVerrouille and (self.classe.typeEnseignement == 'ET')
#            self.list.Enable(enable)
#            self.tb.EnableTool(31, enable) # Paramètres dar défaut
##            self.tb.EnableTool(32, enable) # CI depuis Excel
##            self.tb.EnableTool(33, enable) # Info cible CI ETT
#        else:
#            self.list.Show(True)
#            enable = self.pasVerrouille
#            self.list.Enable(enable)
##            self.tb.EnableTool(32, enable)  # CI depuis Excel
##            self.tb.EnableTool(33, False)  # Info cible CI ETT
#    
#        self.pageCI.Layout()
        
    ######################################################################################  
    def MiseAJour(self):
#        self.MiseAJourType()
        
        self.cb_type.SetStringSelection(self.classe.referentiel.Enseignement[0])
#        self.cb_type.SetStringSelection(REFERENTIELS[self.classe.typeEnseignement].Enseignement[0])
        
        self.cb.SetValue(self.classe.etablissement)
        if self.cb.GetStringSelection () and self.cb.GetStringSelection() == self.classe.etablissement:
            self.textctrl.ChangeValue(u"")
            self.AfficherAutre(False)
            
        else:
            self.textctrl.ChangeValue(self.classe.etablissement)
            self.AfficherAutre(True)
            self.cb.SetSelection(len(constantes.ETABLISSEMENTS_PDD))
        
#        if hasattr(self, 'list'):
#            self.list.Peupler()
                
        self.ec.MiseAJour()

    
        
#    ######################################################################################  
#    def OnLeftDown(self, event):
#        x = event.GetX()
#        y = event.GetY()
#
#        item, flags = self.list.HitTest((x, y))
#
#        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
#            if not self.list.IsSelected(item):
#                self.leftDown = True
#            else:
#                self.leftDown = False
#                
#        event.Skip()
            
    #############################################################################            
    def OnAide(self, event):
        dlg = MessageAideCI(self)
        dlg.ShowModal()
        dlg.Destroy()
            
#    ######################################################################################  
#    def OnLeftUp(self, event):
#        x = event.GetX()
#        y = event.GetY()
#
#        item, flags = self.list.HitTest((x, y))
#
#        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
#            if self.list.IsSelected(item) and not self.leftDown:
#                x0, y0 = self.list.GetScreenPosition()
#                x, y, w, h = self.list.GetItemRect(item, ULC.ULC_RECT_BOUNDS)#ULC.ULC_RECT_LABEL)#
#                
#                ed = Editeur(self.classe, self.list, item, self.list.GetItem(item, 1).GetText(),
#                             pos = (x0+x+self.list.GetColumnWidth(0), y0+y), 
#                             size = (self.list.GetColumnWidth(1), -1))
#                ed.Show()
#
#        event.Skip()
        

#    ######################################################################################  
#    def SelectCI(self, event = None):
#        if recup_excel.ouvrirFichierExcel():
#            dlg = wx.MessageDialog(self.Parent,  u"Sélectionner une liste de CI\n" \
#                                                 u"dans le classeur Excel qui vient de s'ouvrir,\n" \
#                                                 u'puis appuyer sur "Oui".\n\n' \
#                                                 u"Format attendu de la selection :\n" \
#                                                 u"Liste des CI sur une colonne.",
#                                                 u'Sélection de CI',
#                                                 wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
#                                                 )
#            res = dlg.ShowModal()
#            dlg.Destroy() 
#            if res == wx.ID_YES:
#                ls = recup_excel.getColonne(c = 0)
##                ci = getTextCI(ls)
##                self.txtCi.ChangeValue(ci)
#                if ls != None:
#                    self.classe.CI = list(ls)
#                    self.classe.posCI = ['   _   ']*len(ls)
#                    self.MiseAJour()
#                    self.GetDocument().CI.MiseAJourTypeEnseignement()
#                    self.sendEvent()

        
    ######################################################################################  
    def Verrouiller(self, etat):
        self.cb_type.Enable(etat)
        self.pasVerrouille = etat
#        if hasattr(self, 'list'):
#            self.MiseAJourToolbar()
#            enable = etat and (self.classe.typeEnseignement == 'ET')
#            self.list.Enable(enable)
#            self.tb.EnableTool(31, enable)
#            self.tb.EnableTool(32, enable)
        
    
####################################################################################
#
#   Classe définissant l'arbre de sélection du type d'enseignement
#
####################################################################################*
class ArbreTypeEnseignement(HTL.HyperTreeList):
    def __init__(self, parent, panelParent, 
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.WANTS_CHARS|wx.NO_BORDER):

#        wx.Panel.__init__(self, parent, -1, pos, size)
        
        HTL.HyperTreeList.__init__(self, parent, -1, pos, size, style, 
                                   agwStyle = CT.TR_HIDE_ROOT|HTL.TR_NO_HEADER|\
                                  CT.TR_ALIGN_WINDOWS|CT.TR_AUTO_CHECK_CHILD|\
                                  CT.TR_AUTO_CHECK_PARENT|CT.TR_AUTO_TOGGLE_CHILD)
        self.Unbind(wx.EVT_KEY_DOWN)
        self.panelParent = panelParent
#        self.SetBackgroundColour(wx.WHITE)
        self.SetToolTip(wx.ToolTip(u"Choisir le type d'enseignement"))
        
        self.AddColumn(u"")
        self.SetMainColumn(0)
        self.root = self.AddRoot("r")
        self.Construire(self.root)
        self.ExpandAll()
        
#        sizer = wx.BoxSizer()
#        sizer.Add(self.ctc, flag = wx.EXPAND)
#        self.SetSizer(sizer)
#        self.Bind(wx.EVT_SIZE, self.OnResize)
#        
#    ######################################################################################              
#    def OnResize(self, evt):
#        print "Resize ArbreTypeEnseignement", self.GetVirtualSize()
#        self.SetMinSize(self.GetVirtualSize())
#        self.Update()
#        evt.Skip()
#        
        
    ######################################################################################  
    def Construire(self, racine):
        """ Construction de l'arbre
        """
        self.branche = []
        for t, st in ARBRE_REF.items():
            if t[0] == "_":
                branche = self.AppendItem(racine, REFERENTIELS[st[0]].Enseignement[2])
            else:
                branche = self.AppendItem(racine, u"")#, ct_type=2)#, image = self.arbre.images["Seq"])
                rb = wx.RadioButton(self, -1, REFERENTIELS[t].Enseignement[0])
                self.Bind(wx.EVT_RADIOBUTTON, self.panelParent.EvtRadioBox, rb)
                self.SetItemWindow(branche, rb)
                rb.SetToolTipString(REFERENTIELS[t].Enseignement[1])
                rb.Enable(REFERENTIELS[t].projet or not self.panelParent.pourProjet)
                self.branche.append(branche)
            for sst in st:
                sbranche = self.AppendItem(branche, u"")#, ct_type=2)
                rb = wx.RadioButton(self, -1, REFERENTIELS[sst].Enseignement[0])
                self.Bind(wx.EVT_RADIOBUTTON, self.panelParent.EvtRadioBox, rb)
                self.SetItemWindow(sbranche, rb)
                rb.SetToolTipString(REFERENTIELS[sst].Enseignement[1])
                rb.Enable(REFERENTIELS[sst].projet or not self.panelParent.pourProjet)
                self.branche.append(sbranche)
    
    ######################################################################################              
    def SetStringSelection(self, label):
        for rb in self.branche:
            if isinstance(rb.GetWindow(), wx.RadioButton) and label == rb.GetWindow().GetLabel():
                rb.GetWindow().SetValue(True)
          
                

class ListeCI(ULC.UltimateListCtrl):
    def __init__(self, parent, classe):
        
        self.typeEnseignement = classe.typeEnseignement
        self.classe = classe
        self.parent = parent
        
        style = wx.LC_REPORT| wx.BORDER_NONE| wx.LC_VRULES| wx.LC_HRULES| ULC.ULC_HAS_VARIABLE_ROW_HEIGHT
        if not REFERENTIELS[self.typeEnseignement].CI_cible:
            style = style |wx.LC_NO_HEADER
            
        ULC.UltimateListCtrl.__init__(self,parent, -1, 
                                        agwStyle=style)
                
        info = ULC.UltimateListItem()
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT
        info._format = wx.LIST_FORMAT_LEFT
        info._text = u"CI"
         
        self.InsertColumnInfo(0, info)

        info = ULC.UltimateListItem()
        info._format = wx.LIST_FORMAT_LEFT
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_FONT
        info._text = u"Intitulé"
        
        self.InsertColumnInfo(1, info)
        
        self.SetColumnWidth(0, 35)
        self.SetColumnWidth(1, -3)
        
        if REFERENTIELS[self.typeEnseignement].CI_cible:
            for i,p in enumerate(['M', 'E', 'I', 'F', 'S', 'C']):
                info = ULC.UltimateListItem()
                info._mask = wx.LIST_MASK_TEXT
                info._format = wx.LIST_FORMAT_CENTER
                info._text = p
                
                self.InsertColumnInfo(i+2, info)
                self.SetColumnWidth(i+2, 20)
        
        self.Peupler()
                
    ######################################################################################  
    def Peupler(self):
#        print "PeuplerListe"
        # Peuplement de la liste
        self.DeleteAllItems()
        l = self.classe.CI
        
#        if self.typeEnseignement != "SSI":
#            l = self.classe.ci_ET
#        else:
#            l = self.classe.ci_SSI
            
        for i,ci in enumerate(l):
            index = self.InsertStringItem(sys.maxint, "CI"+str(i+1))
            self.SetStringItem(index, 1, ci)
           
            if REFERENTIELS[self.typeEnseignement].CI_cible:
                for j,p in enumerate(['M', 'E', 'I', 'F', 'S', 'C']):
                    item = self.GetItem(i, j+2)
                    cb = wx.CheckBox(self, 100+i, u"", name = p)
                    cb.SetValue(p in self.classe.posCI[i])
                    self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
                    item.SetWindow(cb)
                    self.SetItem(item)
        self.Update()
        
    ######################################################################################  
    def EvtCheckBox(self, event):
        self.parent.EvtCheckBox(event)
    
####################################################################################
#
#   Editeur pour les listes de CI
#
####################################################################################   
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
        
        self.classe.SetCI(self.index, txtctrl.GetValue())
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
        boxClasse = wx.StaticBox(self, -1, u"Découpage de la classe")

        coulClasse = constantes.GetCouleurWx(constantes.CouleursGroupes['C'])
#        boxClasse.SetOwnForegroundColour(coulClasse)
        
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
            
        self.Parent.sendEvent(self.classe)
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
            
#        if self.CI.GetTypeEnseignement() == 'ET': # Rajouter la condition "Clermont" !!!
        if self.CI.GetReferentiel().CI_cible:
            self.panel_cible = Panel_Cible(self, self.CI)
            self.sizer.Add(self.panel_cible, (0,0), (2,1), flag = wx.EXPAND)
            
            self.grid1 = wx.FlexGridSizer( 0, 2, 0, 0 )
            
#            for i, ci in enumerate(constantes.CentresInterets[self.CI.GetTypeEnseignement()]):
            for i, ci in enumerate(self.CI.parent.classe.referentiel.CentresInterets):
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
            
            for i, ci in enumerate(self.CI.parent.classe.referentiel.CentresInterets):
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
#        if self.CI.GetTypeEnseignement() == 'ET':
        if self.CI.GetReferentiel().CI_cible:
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
#        if self.CI.GetTypeEnseignement() == 'ET':
        if self.CI.GetReferentiel().CI_cible:
            self.panel_cible.GererBoutons(True)
            if hasattr(self, 'b2CI'):
                if len(self.CI.numCI) > 2:
                    self.b2CI.Enable(False)
                else:
                    self.b2CI.Enable(True)
        else:
            for num in self.CI.numCI:
                self.group_ctrls[num][0].SetValue(True)
            self.Layout()
        
        
            
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
        

        for i in range(len(self.CI.parent.classe.referentiel.CentresInterets)):
            mei, fsc = self.CI.parent.classe.referentiel.positions_CI[i].split("_")
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
            l = range(len(self.CI.parent.classe.referentiel.CentresInterets))
            
        elif len(self.CI.numCI) == 1:
            l = []
            for i,p in enumerate(self.CI.parent.classe.referentiel.positions_CI):
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
        self.arbre = ArbreCompetences(self, self.competence.GetReferentiel())
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
    def AjouterCompetence(self, code, propag = None):
        self.competence.competences.append(code)
        
    ######################################################################################  
    def EnleverCompetence(self, code, propag = None):
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
        
        nb = wx.Notebook(self, -1,  style= wx.BK_DEFAULT)
        bg_color = self.Parent.GetBackgroundColour()
        
        # Savoirs SSI ou ETT
        pageSavoir = PanelPropriete(nb)
        pageSavoir.SetBackgroundColour(bg_color)
        self.pageSavoir = pageSavoir
        nb.AddPage(pageSavoir, u"")
        
        # Savoirs Spécialité STI2D
        
        
        if prerequis:
            # Savoirs Maths
            pageSavoirM = PanelPropriete(nb)
            pageSavoirM.SetBackgroundColour(bg_color)
            self.pageSavoirM = pageSavoirM
            nb.AddPage(pageSavoirM, u"Mathématiques")
            
            # Savoirs Physique
            pageSavoirP = PanelPropriete(nb)
            pageSavoirP.SetBackgroundColour(bg_color)
            self.pageSavoirP = pageSavoirP
            nb.AddPage(pageSavoirP, u"Sciences Physiques")
            
        self.sizer.Add(nb, (0,1), (2,1), flag = wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND, border = 1)
        self.nb = nb
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(1)
            
        self.MiseAJourTypeEnseignement()

        
    #############################################################################            
    def GetDocument(self):
        return self.savoirs.parent
        
    ######################################################################################  
    def construire(self):
#        print "Construire Savoirs"
#        print self.GetDocument().GetReferentiel()
        
        # Savoirs de base (SSI ou ETT par exemple)
        self.pageSavoir.DestroyChildren()
        self.arbre = ArbreSavoirs(self.pageSavoir, "B", self.savoirs, self.prerequis)
        self.pageSavoir.sizer.Add(self.arbre, (0,0), flag = wx.EXPAND)
        if not self.pageSavoir.sizer.IsColGrowable(0):
            self.pageSavoir.sizer.AddGrowableCol(0)
        if not self.pageSavoir.sizer.IsRowGrowable(0):
            self.pageSavoir.sizer.AddGrowableRow(0)
        self.pageSavoir.Layout()
            
        if self.GetDocument().GetReferentiel().tr_com != []:
#        if REFERENTIELS[self.savoirs.GetTypeEnseignement()].tr_com:
            # Il y a un tronc comun (Spécialité STI2D par exemple)
            self.pageSavoirSpe.DestroyChildren()
            self.arbreSpe = ArbreSavoirs(self.pageSavoirSpe, "S", self.savoirs, self.prerequis)
            self.pageSavoirSpe.sizer.Add(self.arbreSpe, (0,0), flag = wx.EXPAND)
            if not self.pageSavoirSpe.sizer.IsColGrowable(0):
                self.pageSavoirSpe.sizer.AddGrowableCol(0)
            if not self.pageSavoirSpe.sizer.IsRowGrowable(0):
                self.pageSavoirSpe.sizer.AddGrowableRow(0)
            self.pageSavoirSpe.Layout()
            
        if self.prerequis:
            # Savoirs Math
            self.pageSavoirM.DestroyChildren()
            self.arbreM = ArbreSavoirs(self.pageSavoirM, "M", self.savoirs, self.prerequis)
            self.pageSavoirM.sizer.Add(self.arbreM, (0,0), flag = wx.EXPAND)
            if not self.pageSavoirM.sizer.IsColGrowable(0):
                self.pageSavoirM.sizer.AddGrowableCol(0)
            if not self.pageSavoirM.sizer.IsRowGrowable(0):
                self.pageSavoirM.sizer.AddGrowableRow(0)
            self.pageSavoirM.Layout()
            
            # Savoirs Physique
            self.pageSavoirP.DestroyChildren()
            self.arbreP = ArbreSavoirs(self.pageSavoirP, "P", self.savoirs, self.prerequis)
            self.pageSavoirP.sizer.Add(self.arbreP, (0,0), flag = wx.EXPAND)
            if not self.pageSavoirP.sizer.IsColGrowable(0):
                self.pageSavoirP.sizer.AddGrowableCol(0)
            if not self.pageSavoirP.sizer.IsRowGrowable(0):
                self.pageSavoirP.sizer.AddGrowableRow(0)
            self.pageSavoirP.Layout()
        self.Layout()
        
    

    ######################################################################################  
    def SetSavoirs(self): 
        self.savoirs.parent.VerrouillerClasse()
        self.sendEvent()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        """ Coche tous les savoirs a True de self.savoirs.savoirs 
            dans les différents arbres
        """
#        print "MiseAJour Savoirs"
        self.arbre.UnselectAll()
        for s in self.savoirs.savoirs:
#            print "  ",s
            typ, cod = s[0], s[1:]
            if typ == "S": # Savoir spécialité STI2D
                i = self.arbreSpe.get_item_by_label(s[1:], self.arbreSpe.GetRootItem())
                if i.IsOk():
                    self.arbreSpe.CheckItem2(i)
            elif typ == "M": # Savoir Math
                i = self.arbreM.get_item_by_label(s[1:], self.arbreM.GetRootItem())
                if i.IsOk():
                    self.arbreM.CheckItem2(i)
            elif typ == "P": # Savoir Physique
                i = self.arbreP.get_item_by_label(s[1:], self.arbreP.GetRootItem())
                if i.IsOk():
                    self.arbreP.CheckItem2(i)
            else:
                i = self.arbre.get_item_by_label(s[1:], self.arbre.GetRootItem())
                if i.IsOk():
                    self.arbre.CheckItem2(i)
        
        if sendEvt:
            self.sendEvent()
            
    #############################################################################            
    def MiseAJourTypeEnseignement(self):
#        print "MiseAJourTypeEnseignement Savoirs"
        ref = REFERENTIELS[self.savoirs.GetTypeEnseignement()]
        
        if ref.tr_com != []:
            ref_tc = REFERENTIELS[ref.tr_com[0]]
            self.nb.SetPageText(0, ref_tc.nomSavoirs + " " + ref_tc.Code)
            if not hasattr(self, 'pageSavoirSpe') or not isinstance(self.pageSavoirSpe, PanelPropriete):
                bg_color = self.Parent.GetBackgroundColour()
                pageSavoirSpe = PanelPropriete(self.nb)
                pageSavoirSpe.SetBackgroundColour(bg_color)
                self.pageSavoirSpe = pageSavoirSpe
                self.nb.InsertPage(1, pageSavoirSpe, ref.nomSavoirs + ref.Code)
        else:
            self.nb.SetPageText(0, ref.nomSavoirs + " " + ref.Code)
            if hasattr(self, 'pageSavoirSpe') and isinstance(self.pageSavoirSpe, PanelPropriete):
                self.nb.DeletePage(1)
            
            
#        if self.savoirs.GetTypeEnseignement() == "SSI":
#            self.nb.SetPageText(0, u"Capacités SSI")
#        else:
#            self.nb.SetPageText(0, u"Savoirs ETT")
#        
#        if self.savoirs.GetTypeEnseignement() not in ["SSI", "ET"]:
#            if not hasattr(self, 'pageSavoirSpe') or not isinstance(self.pageSavoirSpe, PanelPropriete):
#                bg_color = self.Parent.GetBackgroundColour()
#                pageSavoirSpe = PanelPropriete(self.nb)
#                pageSavoirSpe.SetBackgroundColour(bg_color)
#                self.pageSavoirSpe = pageSavoirSpe
#                self.nb.InsertPage(1, pageSavoirSpe, u"Savoirs " + self.savoirs.GetTypeEnseignement())
#        else:
#            if hasattr(self, 'pageSavoirSpe') and isinstance(self.pageSavoirSpe, PanelPropriete):
#                self.nb.DeletePage(1)
        
        self.construire()
            
            
            
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
        self.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.ALL, border = 2)
        self.sizer.Add(cbType, (0,1), flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        
        
        #
        # Intitulé de la séance
        #
        box = wx.StaticBox(self, -1, u"Intitulé")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        bsizer.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
#        self.Bind(wx.EVT_TEXT, self.EvtTextIntitule, textctrl)
        self.textctrl.Bind(wx.EVT_KILL_FOCUS, self.EvtTextIntitule)
        
        cb = wx.CheckBox(self, -1, u"Afficher dans la zone de déroulement")
        cb.SetToolTipString(u"Décocher pour afficher l'intitulé\nen dessous de la zone de déroulement de la séquence")
        cb.SetValue(self.seance.intituleDansDeroul)
        bsizer.Add(cb, flag = wx.EXPAND)
        
        vcTaille = VariableCtrl(self, seance.taille, signeEgal = True, slider = False, sizeh = 40,
                                help = u"Taille des caractères", unite = u"%")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcTaille)
        bsizer.Add(vcTaille, flag = wx.EXPAND)
        self.vcTaille = vcTaille
        
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
        self.cbInt = cb
        self.sizer.Add(bsizer, (2,0), (2,2), flag = wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, border = 2)
#        self.sizer.Add(textctrl, (1,1), flag = wx.EXPAND)
        
        
        
        
        
        #
        # Organisation
        #
        box2 = wx.StaticBox(self, -1, u"Organisation")
        bsizer2 = wx.StaticBoxSizer(box2, wx.VERTICAL)
        
        # Durée de la séance
        vcDuree = VariableCtrl(self, seance.duree, coef = 0.25, signeEgal = True, slider = False, sizeh = 30,
                               help = u"Durée de la séance en heures", unite = u"h")
#        textctrl = wx.TextCtrl(self, -1, u"1")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
        self.vcDuree = vcDuree
        bsizer2.Add(vcDuree, flag = wx.EXPAND|wx.ALL, border = 2)
        
        # Effectif
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
        
        bsizer2.Add(titre, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 2)
        bsizer2.Add(cbEff, flag = wx.EXPAND|wx.LEFT, border = 2)
#        self.sizer.AddGrowableRow(3)
#        self.sizer.Add(self.nombre, (3,2))
        
        # Nombre de séances en parallèle
        vcNombre = VariableCtrl(self, seance.nombre, signeEgal = True, slider = False, sizeh = 30,
                                help = u"Nombre de groupes réalisant simultanément la même séance")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcNombre)
        self.vcNombre = vcNombre
        bsizer2.Add(vcNombre, flag = wx.EXPAND|wx.ALL, border = 2)
#        self.sizer.AddGrowableRow(5)
        
        # Nombre de rotations
        vcNombreRot = VariableCtrl(self, seance.nbrRotations, signeEgal = True, slider = False, sizeh = 30,
                                help = u"Nombre de rotations")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcNombreRot)
        self.vcNombreRot = vcNombreRot
        bsizer2.Add(vcNombreRot, flag = wx.EXPAND|wx.ALL, border = 2)
        
        self.sizer.Add(bsizer2, (0,2), (4,1), flag =wx.ALL|wx.EXPAND, border = 2)
        
        
        
        
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
        
        self.sizer.Add(titre, (1,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, border = 2)
        self.sizer.Add(cbDem, (1,1), flag = wx.EXPAND|wx.ALL, border = 2)
#        self.sizer.AddGrowableRow(4)
#        self.sizer.Add(self.nombre, (4,2))
        
        
        
        
        #
        # Systèmes
        #
        self.box = wx.StaticBox(self, -1, u"Systèmes ou matériels nécessaires", size = (200,200))
        self.box.SetMinSize((200,200))
        self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        self.systemeCtrl = []
        self.ConstruireListeSystemes()
        self.sizer.Add(self.bsizer, (0,3), (4, 1), flag = wx.EXPAND|wx.ALL, border = 2)
        
#        self.sizer.AddGrowableCol(4, proportion = 1)



        #
        # Lien
        #
        box = wx.StaticBox(self, -1, u"Lien externe")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.selec = URLSelectorCombo(self, self.seance.lien, self.seance.GetPath())
        bsizer.Add(self.selec, flag = wx.EXPAND)
        self.btnlien = wx.Button(self, -1, u"Ouvrir le lien externe")
#        self.btnlien.SetMaxSize((-1,30))
        self.btnlien.Hide()
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btnlien)
        bsizer.Add(self.btnlien, 1,  flag = wx.EXPAND)
        self.sizer.Add(bsizer, (3,4), (1, 1), flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        
        
        #
        # Description de la séance
        #
        dbox = wx.StaticBox(self, -1, u"Description")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
#        bd = wx.Button(self, -1, u"Editer")
        tc = richtext.RichTextPanel(self, self.seance, toolBar = True)
#        tc.SetMaxSize((-1, 150))
#        dbsizer.Add(bd, flag = wx.EXPAND)
        dbsizer.Add(tc, 1, flag = wx.EXPAND)
#        self.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        self.sizer.Add(dbsizer, (0,4), (3, 1), flag = wx.EXPAND|wx.ALL, border = 2)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        self.sizer.SetEmptyCellSize((0,0))
        
        #
        # Mise en place
        #
        self.sizer.AddGrowableCol(4)
        self.sizer.AddGrowableRow(2)
        self.sizer.Layout()
        self.Layout()
    
    
    ######################################################################################  
    def GetReferentiel(self):
        return self.seance.GetReferentiel()
    
    
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        self.selec.SetPathSeq(pathSeq)
        
        
    ######################################################################################  
    def OnPathModified(self, lien, marquerModifier = True):
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
        dem = len(REFERENTIELS[self.seance.GetClasse().typeEnseignement].demarches) > 0
        self.cbDem.Show(dem)
        self.titreDem.Show(dem)
        
    ############################################################################            
    def GetDocument(self):
        return self.seance.GetDocument()
    
#    #############################################################################            
#    def EvtClick(self, event):
#        if not self.edition:
#            self.win = richtext.RichTextFrame(u"Description de la séance "+ self.seance.code, self.seance)
#            self.edition = True
#            self.win.Show(True)
#        else:
#            self.win.SetFocus()
        
        
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
        if self.seance.typeSeance in ["R", "S"] and self.GetReferentiel().listeTypeSeance[event.GetSelection()] not in ["R", "S"]:
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
        
        self.seance.SetType(get_key(self.GetReferentiel().seances, self.cbType.GetStringSelection(), 1))
        
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
            listType = self.GetReferentiel().listeTypeActivite
            if not self.seance.parent.EstSousSeance():
                listType = self.GetReferentiel().listeTypeActivite + ["S"]
        else:
            listType = self.seance.GetReferentiel().listeTypeSeance
        
        ref = REFERENTIELS[self.seance.GetClasse().typeEnseignement]
        
#        listTypeS = []
#        for t in listType:
#            listTypeS.append((constantes.TypesSeance[t], constantes.imagesSeance[t].GetBitmap()))
        
        listTypeS = [(self.GetReferentiel().seances[t][1], constantes.imagesSeance[t].GetBitmap()) for t in listType]
        
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
        if self.seance.typeSeance == "":
            listEff = []
        else:
            listEff = ref.effectifsSeance[self.seance.typeSeance]
        self.cbEff.Show(len(listEff) > 0)
        self.titreEff.Show(len(listEff) > 0)
            
            
        self.vcNombreRot.Show(self.seance.typeSeance == "R")
        
        self.cbEff.Clear()
        for s in listEff:
            self.cbEff.Append(strEffectifComplet(self.seance.GetDocument().classe, s, -1))
        self.cbEff.SetSelection(0)
        
        
        # Démarche       
        if self.seance.typeSeance in ref.activites.keys():
            listDem = ref.demarcheSeance[self.seance.typeSeance]
            dem = len(ref.demarches) > 0
            self.cbDem.Show(dem)
            self.titreDem.Show(dem)
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
            self.cbDem.Append(ref.demarches[s][1])
        self.cbDem.SetSelection(0)
        
    #############################################################################            
    def MarquerProblemeDuree(self, etat):
        return
        self.vcDuree.marquerValid(etat)
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.AdapterAuType()
        
        if self.seance.typeSeance != "":
            self.cbType.SetSelection(self.cbType.GetStrings().index(self.GetReferentiel().seances[self.seance.typeSeance][1]))
        self.textctrl.ChangeValue(self.seance.intitule)
        self.vcDuree.mofifierValeursSsEvt()
        
        if self.cbEff.IsShown():#self.cbEff.IsEnabled() and 
            self.cbEff.SetSelection(self.GetReferentiel().findEffectif(self.cbEff.GetStrings(), self.seance.effectif))
        
        if self.cbDem.IsShown():#self.cbDem.IsEnabled() and :
            self.cbDem.SetSelection(self.cbDem.GetStrings().index(self.GetReferentiel().demarches[self.seance.demarche][1]))
            

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
        self.sizer.Layout()
        
        
    
    def MiseAJourDuree(self):
        self.vcDuree.mofifierValeursSsEvt()
    
    
    
    
    
    
    
    
    
####################################################################################
#
#   Classe définissant le panel de propriété de la tache
#
####################################################################################
class PanelPropriete_Tache(PanelPropriete):
    def __init__(self, parent, tache, revue = 0):
        self.tache = tache
        self.revue = revue
        PanelPropriete.__init__(self, parent)
        
        if not tache.phase in [tache.projet.getCodeLastRevue(), "S"]:
            #
            # La page "Généralités"
            #
            nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
            pageGen = PanelPropriete(nb)
            bg_color = self.Parent.GetBackgroundColour()
            pageGen.SetBackgroundColour(bg_color)
            self.pageGen = pageGen
            nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        else:
            #
            # Pas de book pour la revue 2 et la soutenance
            #
            pageGen = self
            self.pageGen = pageGen
            
        
        #
        # Phase
        #
        ref = self.tache.GetReferentiel()
#        lstPhases = [p[1] for k, p in ref.phases_prj.items() if not k in ref.listPhasesEval_prj]
        lstPhases = [ref.phases_prj[k][1] for k in ref.listPhases_prj if not k in ref.listPhasesEval_prj]
        
        if tache.phase in ["R1", "R2", "R3", "S"]:
            titre = wx.StaticText(pageGen, -1, u"Phase : "+ref.phases_prj[tache.phase][1])
            pageGen.sizer.Add(titre, (0,0), (1,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, border = 5)
        else:
            titre = wx.StaticText(pageGen, -1, u"Phase :")
            cbPhas = wx.combo.BitmapComboBox(pageGen, -1, u"Selectionner la phase",
                                 choices = lstPhases,
                                 style = wx.CB_DROPDOWN
                                 | wx.TE_PROCESS_ENTER
                                 | wx.CB_READONLY
                                 #| wx.CB_SORT
                                 )

            for i, k in enumerate(sorted([k for k in ref.phases_prj.keys() if not k in ref.listPhasesEval_prj])):#ref.listPhases_prj):
                cbPhas.SetItemBitmap(i, constantes.imagesTaches[k].GetBitmap())
            pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbPhas)
            self.cbPhas = cbPhas
            pageGen.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 5)
            pageGen.sizer.Add(cbPhas, (0,1), flag = wx.EXPAND|wx.ALL, border = 2)
        

        
        #
        # Intitulé de la tache
        #
        if not tache.phase in ["R1", "R2", "R3", "S"]:
            box = wx.StaticBox(pageGen, -1, u"Intitulé de la tâche")
            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            textctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
            textctrl.SetToolTipString(u"Donner l'intitulé de la tâche\n"\
                                      u" = un simple résumé !\n" \
                                      u"les détails doivent figurer dans la zone\n" \
                                      u"\"Description détaillée de la tâche\"")
            bsizer.Add(textctrl,1, flag = wx.EXPAND)
            self.textctrl = textctrl
            self.boxInt = box
            self.textctrl.Bind(wx.EVT_KILL_FOCUS, self.EvtTextIntitule)
            pageGen.sizer.Add(bsizer, (1,0), (1,2), 
                           flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT, border = 2)
            
        
        #
        # Durée de la tache
        #
        if not tache.phase in ["R1", "R2", "R3", "S"]:
            vcDuree = VariableCtrl(pageGen, tache.duree, coef = 0.5, signeEgal = True, slider = False,
                                   help = u"Volume horaire de la tâche en heures", sizeh = 60)
            pageGen.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
            self.vcDuree = vcDuree
            pageGen.sizer.Add(vcDuree, (2,0), (1, 2), flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        #
        # Elèves impliqués
        #
        if not tache.phase in ["R1", "R2", "R3", "S"]:
            self.box = wx.StaticBox(pageGen, -1, u"Elèves impliqués")
#            self.box.SetMinSize((150,-1))
            self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
            self.elevesCtrl = []
            self.ConstruireListeEleves()
            pageGen.sizer.Add(self.bsizer, (0,2), (4, 1), flag = wx.EXPAND)
        
        
        
        
        #
        # Description de la tâche
        #
        dbox = wx.StaticBox(pageGen, -1, u"Description détaillée de la tâche")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
#        bd = wx.Button(pageGen, -1, u"Editer")
        tc = richtext.RichTextPanel(pageGen, self.tache, toolBar = True)
        tc.SetToolTipString(u"Donner une description détaillée de la tâche :\n" \
                            u" - les conditions nécessaires\n" \
                            u" - ce qui est fourni\n" \
                            u" - les résultats attendus\n" \
                            u" - les différentes étapes\n" \
                            u" - la répartition du travail entre les élèves\n"\
                            u" - ..."
                            )
#        tc.SetMaxSize((-1, 150))
#        tc.SetMinSize((150, 60))
        dbsizer.Add(tc,1, flag = wx.EXPAND)
#        dbsizer.Add(bd, flag = wx.EXPAND)
#        pageGen.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        if tache.phase in ["R1", "R2", "R3", "S"]:
            pageGen.sizer.Add(dbsizer, (1,0), (3, 2), flag = wx.EXPAND)
            pageGen.sizer.AddGrowableCol(0)
        else:
            pageGen.sizer.Add(dbsizer, (0,3), (4, 1), flag = wx.EXPAND)
            pageGen.sizer.AddGrowableCol(3)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        pageGen.sizer.AddGrowableRow(1)
        
#        print ">>>", tache.phase, tache.projet.getCodeLastRevue()
        if not tache.phase in [tache.projet.getCodeLastRevue(), "S"]:
            nb.AddPage(pageGen, u"Propriétés générales")
#        pageGen.sizer.Layout()
        
#            pageGen.SetMinSize((-1, 100))
#        if not tache.phase in ["R2", "S"]:
            #
            # La page "Compétences"
            #
    #        pageCom = PanelPropriete(self, style = wx.RETAINED)
            pageCom = wx.Panel(nb, -1)
            
        
    #        pageCom.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            self.pageCom = pageCom
            pageComsizer = wx.BoxSizer(wx.HORIZONTAL)
            #
            # Compétences employées
            #
            if tache.phase != "S":
                self.arbre = ArbreCompetencesPrj(pageCom, tache.GetReferentiel(), self,
                                                 revue = self.tache.phase in ["R1", "R2", "R3", "S", "Rev"], 
                                                 eleves = self.tache.phase in ["R1", "R2", "R3", "S"])
                pageComsizer.Add(self.arbre, 1, flag = wx.EXPAND)
        
            
        
            pageCom.SetSizer(pageComsizer)
            nb.AddPage(pageCom, u"Compétences à mobiliser") 
            
#            pageComsizer.Layout() 
            self.pageComsizer = pageComsizer
        
            self.sizer.Add(nb, (0,0), flag = wx.EXPAND)
            self.sizer.AddGrowableCol(0)
            self.sizer.AddGrowableRow(0)
        
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
#        sel = self.nb.GetSelection()
#        self.MiseAJourPoids()
        event.Skip()
        
    ####################################################################################
    def MiseAJourPoids(self):
        for c in self.tache.indicateursEleve[0]:
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
            indicateurs = REFERENTIELS[self.tache.GetTypeEnseignement()].dicIndicateurs
            lab = u"Indicateurs"
            
            # On supprime l'ancienne CheckListBox
            if self.liste != None:
                self.ibsizer.Detach(self.liste)
                self.liste.Destroy()
            
            if competence in indicateurs.keys():
                self.liste = wx.CheckListBox(self.pageCom, -1, choices = indicateurs[competence], style = wx.BORDER_NONE)
    
                lst = self.tache.indicateursEleve[0][competence]
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
            if competence in self.tache.indicateursEleve[0].keys():
                self.arbre.MiseAJour(competence, self.tache.indicateursEleve[0][competence])
            else:
                self.arbre.MiseAJour(competence, REFERENTIELS[self.tache.GetTypeEnseignement()]._dicCompetences_prj_simple[competence][1])
            
            
        self.Thaw()
        
        
    ######################################################################################  
    def EvtCheckListBox(self, event):
        index = event.GetSelection()
        
        if self.competence in self.tache.indicateursEleve[0].keys():
            lst = self.tache.indicateursEleve[0][self.competence]
        else:
            lst = [self.competence in self.tache.competences]*len(REFERENTIELS[self.tache.GetTypeEnseignement()].dicIndicateurs_prj[self.competence])
            
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
    def AjouterCompetence(self, code, propag = True):
#        print "AjouterCompetence", self, code
        if not code in self.tache.indicateursEleve[0]:
            self.tache.indicateursEleve[0].append(code)
        
        if propag:
            for i,e in enumerate(self.tache.projet.eleves):
                self.AjouterCompetenceEleve(code, i+1)
        
    ######################################################################################  
    def EnleverCompetence(self, code, propag = True):
#        print "EnleverCompetence", self, code
        if code in self.tache.indicateursEleve[0]:
            self.tache.indicateursEleve[0].remove(code)
        # on recommence : pour corriger un bug
        if code in self.tache.indicateursEleve[0]:
            self.tache.indicateursEleve[0].remove(code)
        
        if propag:
            for i,e in enumerate(self.tache.projet.eleves):
                self.EnleverCompetenceEleve(code, i+1)

    ######################################################################################  
    def AjouterCompetenceEleve(self, code, eleve):
#        print "AjouterCompetenceEleve", self, code
        if hasattr(self.tache, 'indicateursEleve'):
            dicIndic = self.tache.projet.eleves[eleve-1].GetDicIndicateursRevue(self.tache.phase)
            comp = code.split("_")[0]
            if comp in dicIndic.keys():
                if comp != code: # Indicateur seul
                    indic = eval(code.split("_")[1])
                    ok = dicIndic[comp][indic-1]
            else:
                ok = False
                
            if ok and not code in self.tache.indicateursEleve[eleve]:
                self.tache.indicateursEleve[eleve].append(code)
#                self.tache.ActualiserDicIndicateurs()
            
        
    ######################################################################################  
    def EnleverCompetenceEleve(self, code, eleve):
#        print "EnleverCompetenceEleve", self, code
        if hasattr(self.tache, 'indicateursEleve'):
            if code in self.tache.indicateursEleve[eleve]:
                self.tache.indicateursEleve[eleve].remove(code)
            # on recommence : pour corriger un bug
            if code in self.tache.indicateursEleve[eleve]:
                self.tache.indicateursEleve[eleve].remove(code)
#            self.tache.ActualiserDicIndicateurs()
    
    ############################################################################            
    def SetCompetences(self):
        self.GetDocument().MiseAJourDureeEleves()
        self.sendEvent()
        self.tache.projet.VerrouillerClasse()
        
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
    
#            self.box.SetMinSize((200,200))
            self.pageGen.Layout()
            self.pageGen.Thaw()
        
        
    #############################################################################            
    def MiseAJourListeEleves(self):
        """ Met à jour la liste des élèves
        """
        if not self.tache.phase in ["S", "R1", "R2", "R3"]:
            self.pageGen.Freeze()
            for i, e in enumerate(self.GetDocument().eleves):
                self.elevesCtrl[i].SetLabel(e.GetNomPrenom())
            self.bsizer.Layout()
            self.pageGen.Layout()
            self.pageGen.Thaw()

    #############################################################################            
    def MiseAJourEleves(self):
        """ Met à jour le cochage des élèves concernés par la tâche
        """
        if not self.tache.phase in ["S", "R1", "R2", "R3"]:
            for i, e in enumerate(self.GetDocument().eleves):
                self.elevesCtrl[i].SetValue(i in self.tache.eleves)

                
                
        
    ############################################################################            
    def GetDocument(self):
        return self.tache.GetDocument()
    
#    #############################################################################            
#    def EvtClick(self, event):
#        if not self.edition:
#            self.win = richtext.RichTextFrame(u"Description de la tâche "+ self.tache.code, self.tache)
#            self.edition = True
#            self.win.Show(True)
#        else:
#            self.win.SetFocus()
        
        
    #############################################################################            
    def EvtVarSysteme(self, event):
        self.sendEvent()
        
        
    
        
        
    #############################################################################            
    def EvtCheckEleve(self, event):
        lst = []
        for i in range(len(self.GetDocument().eleves)):
            if self.elevesCtrl[i].IsChecked():
                lst.append(i)
        self.tache.eleves = lst
        self.GetDocument().MiseAJourDureeEleves()
        self.sendEvent()    


    #############################################################################            
    def EvtTextIntitule(self, event):
        self.tache.SetIntitule(self.textctrl.GetValue())
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
        """ Changement de phase
        """
#        print "EvtComboBox phase", self.tache, self.tache.phase
        ref = self.tache.GetReferentiel()
        newPhase = ref.getClefDic('phases_prj', self.cbPhas.GetStringSelection(), 1)
#        print "   ", newPhase
#        newPhase = get_key(self.GetReferentiel().NOM_PHASE_TACHE[self.tache.GetTypeEnseignement(True)], 
#                                        self.cbPhas.GetStringSelection())
        if self.tache.phase != newPhase:
            if newPhase == "Rev":
                self.tache.SetDuree(0.5)
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

            
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "MiseAJour", self.tache.phase, self.tache.intitule
        if hasattr(self, 'arbre'):
            self.arbre.UnselectAll()
            
#            root = self.arbre.GetRootItem()
            for s in self.tache.indicateursEleve[0]:
                if s in self.arbre.items.keys():
                    self.arbre.CheckItem2(self.arbre.items[s])
            
        if hasattr(self, 'textctrl'):
            self.textctrl.SetValue(self.tache.intitule)
        
        if hasattr(self, 'cbPhas') and self.tache.phase != '':
            self.cbPhas.SetStringSelection(self.tache.GetReferentiel().phases_prj[self.tache.phase][1])
            
        if sendEvt:
            self.sendEvent()
        
        
    #############################################################################
    def MiseAJourTypeEnseignement(self, ref):
        if hasattr(self, 'arbre'):
            self.arbre.MiseAJourTypeEnseignement(ref)
        
        
        
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
        self.sizer.Add(bsizer, (0,2), (2,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |

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
        self.sizer.Add(bsizer, (0,3), (2, 1), flag = wx.EXPAND|wx.TOP|wx.LEFT, border = 2)
        
        self.sizer.AddGrowableCol(3)
        self.sizer.AddGrowableRow(1)
        self.sizer.Layout()
        
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        self.selec.SetPathSeq(pathSeq)
        
        
    ######################################################################################  
    def OnPathModified(self, lien, marquerModifier = True):
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
#        print "PanelPropriete_Personne", personne
        self.personne = personne
        self.parent = parent
        
        PanelPropriete.__init__(self, parent)
        
        #
        # Nom
        #
        box = wx.StaticBox(self, -1, u"Identité")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        titre = wx.StaticText(self, -1, u"Nom :")
        textctrl = wx.TextCtrl(self, 1, u"")
        self.textctrln = textctrl
        
        nsizer = wx.BoxSizer(wx.HORIZONTAL)
        nsizer.Add(titre, flag = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)
        nsizer.Add(textctrl, flag = wx.ALIGN_RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        #
        # Prénom
        #
        titre = wx.StaticText(self, -1, u"Prénom :")
        textctrl = wx.TextCtrl(self, 2, u"")
        self.textctrlp = textctrl
        
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        psizer.Add(titre, flag = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)
        psizer.Add(textctrl, flag = wx.ALIGN_RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        bsizer.Add(nsizer, flag = wx.ALIGN_RIGHT|wx.EXPAND)
        bsizer.Add(psizer, flag = wx.ALIGN_RIGHT|wx.EXPAND)
        self.sizer.Add(bsizer, (0,0), flag = wx.EXPAND|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
        
        
        #
        # Référent
        #
        if hasattr(self.personne, 'referent'):
            box = wx.StaticBox(self, -1, u"Fonction")
            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            cb = wx.CheckBox(self, -1, u"Référent")#, style=wx.ALIGN_RIGHT)
            cb.SetValue(self.personne.referent)
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
            self.cbInt = cb
            bsizer.Add(cb, flag = wx.EXPAND|wx.ALL, border = 3)
            self.sizer.Add(bsizer, (0,1), flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
        
        
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
            bsizer.Add(titre, flag = wx.EXPAND|wx.TOP|wx.LEFT, border = 3)
            bsizer.Add(cbPhas, flag = wx.EXPAND|wx.BOTTOM|wx.LEFT, border = 3)
#            self.sizer.Add(bsizer, (2,0), flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT|wx.LEFT, border = 2)

        
        
        #|
        # Grilles d'évaluation
        #
        if hasattr(self.personne, 'grille'):
            self.boxGrille = wx.StaticBox(self, -1, u"Grilles d'évaluation")
            self.bsizer = wx.StaticBoxSizer(self.boxGrille, wx.VERTICAL)
            self.sizer.Add(self.bsizer, (1,0), (1,2), flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
            self.ConstruireSelectGrille()
            
            
        #
        # Avatar
        #
        box = wx.StaticBox(self, -1, u"Portrait")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        image = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.image = image
        self.SetImage()
        bsizer.Add(image, flag = wx.EXPAND)
        
        bt = wx.Button(self, -1, u"Changer le portrait")
        bt.SetToolTipString(u"Cliquer ici pour sélectionner un fichier image")
        bsizer.Add(bt, flag = wx.EXPAND|wx.ALIGN_BOTTOM)
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt)
        self.sizer.Add(bsizer, (0,2), (2,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(1)
        
        self.sizer.Layout()
        
        self.Layout()
        
        
    #############################################################################            
    def ConstruireSelectGrille(self):
#        titres = self.personne.GetReferentiel().nomParties_prj
        if len(self.personne.grille) > 0:
#            lstGrilles = self.personne.grille
#            titres = self.personne.GetReferentiel().nomParties_prj
            
    #            if self.personne.projet.GetTypeEnseignement(simple = True) == "SSI":
    #                lstGrilles = [self.personne.grille[0]]
    #                titres = [u""]
    #            else:
    #                lstGrilles = self.personne.grille
    #                titres = [u"Revues :", u"Soutenance :"]
            
            self.SelectGrille = {}
            for k, t in self.personne.grille.items():
                self.SelectGrille[k] = PanelSelectionGrille(self, self.personne, k)
                self.bsizer.Add(self.SelectGrille[k], flag = wx.EXPAND)
            
            self.boxGrille.Show(True)
            
        else:
            self.boxGrille.Show(False)
            
            
            
    #############################################################################            
    def GetDocument(self):
        return self.personne.projet
    
    
    #############################################################################            
    def OnClick(self, event):
#        for k, g in self.personne.grille.items():
#            if event.GetId() == self.btnlien[k].GetId():
#                g.Afficher(self.GetDocument().GetPath())
##        if event.GetId() == self.btnlien[0].GetId():
##            self.personne.grille[0].Afficher(self.GetDocument().GetPath())
##        elif event.GetId() == self.btnlien[1].GetId():
##            self.personne.grille[1].Afficher(self.GetDocument().GetPath())
#            
#        else:
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
            self.sendEvent()
            
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
        self.personne.projet.MiseAJourNomsEleves()
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
        self.personne.projet.SetReferent(self.personne, event.IsChecked())
        self.sendEvent()
        
    #############################################################################            
    def MiseAJourTypeEnseignement(self):
        if hasattr(self.personne, 'grille'):
#            print "MiseAJourTypeEnseignement eleve", self.personne
            if hasattr(self, 'SelectGrille'):
                
#                for c in self.bsizer.GetChildren():
#                    print c
#                    if c.GetWindow():
#                        print "  ",c.GetWindow()
#                        self.bsizer.Detach(c.GetWindow())
#                        c.GetWindow().Destroy()
                for k, sg in self.SelectGrille.items():
                    self.bsizer.Detach(sg)
                    sg.Destroy()
#                    sh.Detach(self.SelectGrille[k])
#                    sh.Detach(self.titreGrille[k])
#                    sh.Detach(self.btnlien[k])
#                    self.SelectGrille[k].Destroy()
#                    self.titreGrille[k].Destroy()
#                    self.btnlien[k].Destroy()
#                
#                sh.Destroy()
#                for sg in self.SelectGrille.values():
#                    self.bsizer.Detach(sg)
#                    sg.Destroy()
#                for tg in self.titreGrille.values():
#                    self.bsizer.Detach(tg)
#                    tg.Destroy()
#                for bl in self.btnlien.values():
#                    self.bsizer.Detach(bl)
#                    bl.Destroy()
#                self.boxGrille.Destroy()
            self.ConstruireSelectGrille()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False, marquerModifier = True):
        self.textctrln.ChangeValue(self.personne.nom)
        self.textctrlp.ChangeValue(self.personne.prenom)
        if hasattr(self, 'cbPhas'):
            self.cbPhas.SetStringSelection(constantes.NOM_DISCIPLINES[self.personne.discipline])
        if hasattr(self, 'cbInt'):
            self.cbInt.SetValue(self.personne.referent)
        if hasattr(self, 'SelectGrille'):
            for k, select in self.SelectGrille.items():
                select.SetPath(self.personne.grille[k].path, marquerModifier = marquerModifier)
#            self.OnPathModified()
        if sendEvt:
            self.sendEvent()

    ######################################################################################  
    def OnPathModified(self, lien = "", marquerModifier = True):
        if marquerModifier:
            self.personne.projet.GetApp().MarquerFichierCourantModifie()
        self.Layout()
        self.Refresh()
   
        
        
        
class PanelSelectionGrille(wx.Panel):
    def __init__(self, parent, eleve, codeGrille):
        wx.Panel.__init__(self, parent, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.eleve = eleve
        self.codeGrille = codeGrille
        titre = wx.StaticText(self, -1, eleve.GetReferentiel().nomParties_prj[codeGrille])
        self.SelectGrille = URLSelectorCombo(self, eleve.grille[codeGrille], 
                                             eleve.projet.GetPath(), 
                                             dossier = False, ext = "Classeur Excel (*.xls*)|*.xls*")
        self.btnlien = wx.Button(self, -1, u"Ouvrir")
        self.btnlien.Show(self.eleve.grille[self.codeGrille].path != "")
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btnlien)
        sizer.Add(titre, flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 3)
        sizer.Add(self.SelectGrille,1, flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 3)
        sizer.Add(self.btnlien, flag = wx.EXPAND|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 3)
        
        self.Layout()
        self.SetSizerAndFit(sizer)


    #############################################################################            
    def OnClick(self, event):
        self.eleve.grille[self.codeGrille].Afficher(self.eleve.GetDocument().GetPath())
                
                
    #############################################################################            
    def SetPath(self, path, marquerModifier):  
        self.SelectGrille.SetPath(path, marquerModifier = marquerModifier)          
                
                
    ######################################################################################  
    def OnPathModified(self, lien = "", marquerModifier = True):
        self.btnlien.Show(self.eleve.grille[self.codeGrille].path != "")
        self.Parent.OnPathModified(lien, marquerModifier)
                
                
                
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
        self.sizer.Add(bsizer, (1,0), flag = wx.EXPAND|wx.LEFT, border = 3)
        
        
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
#        bd = wx.Button(self, -1, u"Editer")
        tc = richtext.RichTextPanel(self, self.support, toolBar = True)
        tc.SetMaxSize((-1, 150))
#        dbsizer.Add(bd, flag = wx.EXPAND)
        dbsizer.Add(tc, 1, flag = wx.EXPAND)
#        self.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
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
    def OnPathModified(self, lien, marquerModifier = True):
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
        
#    #############################################################################            
#    def EvtClick(self, event):
#        if not self.edition:
#            self.win = richtext.RichTextFrame(u"Description du support "+ self.support.nom, self.support)
#            self.edition = True
#            self.win.Show(True)
#        else:
#            self.win.SetFocus()
        
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
#        self.Bind(wx.EVT_CHAR, self.OnChar)
        
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
        item = self.HitTest(pt)[0]
        if item:
            self.sequence.AfficherLien(item)
        event.Skip()                
        

    ####################################################################################
    def OnCompareItems(self, item1, item2):
        i1 = self.GetItemPyData(item1)
        i2 = self.GetItemPyData(item2)
        return int(i1.ordre - i2.ordre)

    ####################################################################################
    def OnMove(self, event):
        if self.itemDrag != None:
            item = self.HitTest(wx.Point(event.GetX(), event.GetY()))[0]
            if item != None:
                dataTarget = self.GetItemPyData(item)
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
        elif evt.ControlDown() and keycode == 67: # Crtl-C
            item = self.GetSelection()
            self.projet.CopierTache(item = item)
        elif evt.ControlDown() and keycode == 86: # Crtl-V
            item = self.GetSelection()
            self.projet.CollerTache(item = item)
        evt.Skip()
            
    ####################################################################################
    def AjouterEleve(self, event = None):
        self.projet.AjouterEleve()
        
        
    ####################################################################################
    def SupprimerEleve(self, event = None, item = None):
        self.projet.SupprimerEleve(item)

            
    ####################################################################################
    def AjouterTache(self, event = None):
        obj = self.GetItemPyData(self.GetSelection())
        if not isinstance(obj, Tache):
            obj = None
        self.projet.AjouterTache(tacheAct = obj)
#        self.lstTaches.append(self.AppendItem(self.taches, u"Tâche :", data = tache))
        
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
        item = self.HitTest(pt)[0]
        if item:
            self.projet.AfficherLien(item)
        event.Skip()                
        

    ####################################################################################
    def OnCompareItems(self, item1, item2):
        i1 = self.GetItemPyData(item1)
        i2 = self.GetItemPyData(item2)
        return int(i1.ordre - i2.ordre)
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
            item = self.HitTest(wx.Point(event.GetX(), event.GetY()))[0]
            if item != None:
                dataTarget = self.GetItemPyData(item)
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
                    lst = dataTarget.projet.taches

                    s = lst.index(dataSource)
                    t = lst.index(dataTarget)
                    
                    if t > s:
                        lst.insert(t, lst.pop(s))
                    else:
                        lst.insert(t+1, lst.pop(s))
                    dataTarget.projet.SetOrdresTaches()
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
    def __init__(self, parent, typ, savoirs, prerequis):

        CT.CustomTreeCtrl.__init__(self, parent, -1, 
                                   agwStyle = wx.TR_DEFAULT_STYLE|wx.TR_MULTIPLE|wx.TR_HIDE_ROOT|CT.TR_AUTO_CHECK_CHILD|CT.TR_AUTO_CHECK_PARENT)
        
        self.parent = parent
        self.savoirs = savoirs
        
        ref = savoirs.GetReferentiel()
        
        self.root = self.AddRoot(u"")
        
#        if typeEns == "SSI":
#            t = u"Capacités "
#        else:
#            t = u"Savoirs "
#        self.root = self.AppendItem(root, t+typeEns)
        self.SetItemBold(self.root, True)
        et = False
        if typ == "B":
            if ref.tr_com != []:
                dic = REFERENTIELS[ref.tr_com[0]].dicSavoirs
                et = True
            else:
                dic = ref.dicSavoirs
        elif typ == "S":
            dic = ref.dicSavoirs
        elif typ == "M":
            if ref.tr_com != []:
                dic = REFERENTIELS[ref.tr_com[0]].dicSavoirs_Math
            else:
                dic = ref.dicSavoirs_Math
        elif typ == "P":
            if ref.tr_com != []:
                dic = REFERENTIELS[ref.tr_com[0]].dicSavoirs_Phys
            else:
                dic = ref.dicSavoirs_Phys
        self.Construire(self.root, dic, et = et)
            
            
#        if typ == "B":
#            if not typeEns in ["SSI", "ET"]:
#                self.Construire(self.root, REFERENTIELS["ET"].dicSavoirs)
#            else:
#                self.Construire(self.root, REFERENTIELS[typeEns].dicSavoirs)
#        elif typ == "S":
#            self.Construire(self.root, REFERENTIELS[typeEns].dicSavoirs)
#        elif typ == "M":
#            self.Construire(self.root, REFERENTIELS[typeEns].dicSavoirs_Math)
#        elif typ == "P":
#            self.Construire(self.root, REFERENTIELS[typeEns].dicSavoirs_Phys)
            
        self.typ = typ
#        if prerequis and typeEns!="ET" and typeEns!="SSI":
#            self.rootET = self.AppendItem(root, u"Savoirs ETT")
#            self.SetItemBold(self.rootET, True)
#            self.SetItemItalic(self.rootET, True)
#            self.Construire(self.rootET, constantes.dicSavoirs['ET'], )
        
        
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
    
        
    ####################################################################################
    def Construire(self, branche, dic, et = False, grosseBranche = True):
        """ Construction d'une branche de "savoirs"
            <et> = prérequis ETT pour spécialité STI2D
        """
        if dic == None:
            return
        clefs = constantes.trier(dic.keys())
        for k in clefs:
            if type(dic[k][1]) == list:
                sep = u"\n " + CHAR_POINT + u" "
                toolTip = CHAR_POINT + u" " + sep.join(dic[k][1])
            else:
                toolTip = None
#            print k+" "+dic[k][0]
            b = self.AppendItem(branche, k+" "+dic[k][0], ct_type=1, data = toolTip)
            
            if et:
                self.SetItemItalic(b, True)
            if grosseBranche:
                self.SetItemBold(b, True)
#                self.SetItem3State(b, True)
            
            if type(dic[k][1]) == dict:
                self.Construire(b, dic[k][1], et, grosseBranche = False)

        
    ####################################################################################
    def OnItemCheck(self, event):
#        print "OnItemCheck"
        item = event.GetItem()
        code = self.GetItemText(item).split()[0]

#        if self.IsItalic(item):
#            code = '_'+code
        

        newSavoirs = []
        for s in self.savoirs.savoirs:
            if s[0] != self.typ:
                newSavoirs.append(s)
                
        newSavoirs.extend(self.getListItemChecked(self.root)[0])    
        
        self.savoirs.savoirs = newSavoirs

#        if item.GetValue():
#            self.savoirs.savoirs.append(code)
#        else:
#            if code in self.savoirs.savoirs:
#                self.savoirs.savoirs.remove(code)
#            else:
#                codeparent = code[:-2]
#                    if codeparent in self.savoirs.savoirs:
                        
                        
        self.parent.Parent.Parent.SetSavoirs()
        event.Skip()
        
        
    ####################################################################################
    def getListItemChecked(self, root):
        liste = []
        complet = True
        for i in root.GetChildren():
            cliste, ccomplet = self.getListItemChecked(i)
            if ccomplet:
                if i.IsChecked():
                    liste.append(self.getCode(i))
                else:
                    complet = False
            else:
                liste.extend(cliste)
                complet = False
             
        return liste, complet
    
    
    ####################################################################################
    def OnGetToolTip(self, event):
        toolTip = event.GetItem().GetData()
        if toolTip != None:
            event.SetToolTip(wx.ToolTip(toolTip))

        
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
    def getCode(self, item):
        return self.typ+self.GetItemText(item).split()[0]
    
    
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




####################################################################################
####################################################################################
####################################################################################
    
class ArbreCompetences(HTL.HyperTreeList):
    def __init__(self, parent, ref, pptache = None, agwStyle = CT.TR_HIDE_ROOT|CT.TR_HAS_VARIABLE_ROW_HEIGHT):#|CT.TR_AUTO_CHECK_CHILD):#|HTL.TR_NO_HEADER):
        
        HTL.HyperTreeList.__init__(self, parent, -1, style = wx.WANTS_CHARS, agwStyle = agwStyle)#wx.TR_DEFAULT_STYLE|
        
        self.parent = parent
        if pptache == None:
            self.pptache = parent
        else:
            self.pptache = pptache
        self.ref = ref
        
        self.items = {}
      
        self.AddColumn(ref.nomCompetences)
        self.SetMainColumn(0) # the one with the tree in it...
        self.AddColumn(u"")
        self.SetColumnWidth(1, 0)
        self.AddColumn(u"")
        self.SetColumnWidth(1, 0)
        self.AddColumn(u"Eleves")
        self.SetColumnWidth(3, 0)
        self.root = self.AddRoot(ref.nomCompetences)
        self.MiseAJourTypeEnseignement(ref)
        
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
    def MiseAJourTypeEnseignement(self, ref):
#        print "MiseAJourTypeEnseignement"
        self.ref = ref
        self.DeleteChildren(self.root)
        self.Construire(self.root, ref = ref)
        self.ExpandAll()
#        self.Layout()
        
    
    
    #############################################################################
    def MiseAJourPhase(self, phase):
        self.DeleteChildren(self.root)
        self.Construire(self.root)
        self.ExpandAll()
        
    
    ####################################################################################
    def OnSize2(self, evt):
        w = self.GetClientSize()[0]-17-self.GetColumnWidth(1)-self.GetColumnWidth(2)
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
    def Construire(self, branche, dic = None, ref = None, ct_type = 0):
        if dic == None:
            dic = ref.dicCompetences
        clefs = dic.keys()
        clefs.sort()
        for k in clefs:
            if type(dic[k]) == list and type(dic[k][1]) == dict:
                b = self.AppendItem(branche, k+" "+dic[k][0], ct_type=ct_type, data = k)
                self.Construire(b, dic[k][1], ct_type = 1)
            else:
                b = self.AppendItem(branche, k+" "+dic[k][0], ct_type = 1, data = k)
            
            if ct_type == 0:
                self.SetItemBold(b, True)
        
    ####################################################################################
    def OnItemCheck(self, event, item = None):
        if event != None:
            item = event.GetItem()
        
        self.AjouterEnleverCompetencesItem(item)
        
        if event != None:
            event.Skip()
        wx.CallAfter(self.pptache.SetCompetences)
        
    
    ####################################################################################
    def AjouterEnleverCompetencesItem(self, item, propag = True):
        code = self.GetItemPyData(item)#.split()[0]
#        print "AjouterEnleverCompetencesItem", code
        if code != None: # un seul indicateur séléctionné
            self.AjouterEnleverCompetences([item], propag)

        else:       # une compétence complète séléctionnée
            self.AjouterEnleverCompetences(item.GetChildren(), propag)

    ####################################################################################
    def AjouterEnleverCompetences(self, lstitem, propag = True):
        for item in lstitem:
            code = self.GetItemPyData(item)#.split()[0]
#            print "  ", code, item.GetValue()
            if item.GetValue():
                self.pptache.AjouterCompetence(code, propag)
            else:
                self.pptache.EnleverCompetence(code, propag)
                
                
    ####################################################################################
    def AjouterEnleverCompetencesEleve(self, lstitem, eleve):
#        print "AjouterEnleverCompetencesEleve", self, lstitem, eleve
        for item in lstitem:
            code = self.GetItemPyData(item)
            if self.GetItemWindow(item, 3).EstCocheEleve(eleve):
                self.pptache.AjouterCompetenceEleve(code, eleve)
            else:
                self.pptache.EnleverCompetenceEleve(code, eleve)
    
    
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
    """ Arbre des compétences abordées en projet lors d'une tâche <pptache>
        <revue> : vrai si la tâche est une revue
        <eleves> : vrai s'il faut afficher une colonne supplémentaire pour distinguer les compétences pour chaque éleve
    """
    def __init__(self, parent, ref, pptache, revue = False, eleves = False, 
                 agwStyle = CT.TR_HIDE_ROOT|CT.TR_HAS_VARIABLE_ROW_HEIGHT|\
                            CT.TR_ROW_LINES|CT.TR_ALIGN_WINDOWS|CT.TR_AUTO_CHECK_CHILD|\
                            CT.TR_AUTO_CHECK_PARENT|CT.TR_AUTO_TOGGLE_CHILD):
        self.revue = revue
        self.eleves = eleves
          
        ArbreCompetences.__init__(self, parent, ref, pptache,
                                  agwStyle = agwStyle)#|CT.TR_ELLIPSIZE_LONG_ITEMS)#|CT.TR_TOOLTIP_ON_LONG_ITEMS)#
        self.Bind(wx.EVT_SIZE, self.OnSize2)
        self.Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        
        self.SetColumnText(0, ref.nomCompetences + u" et indicateurs de performance")
        self.SetColumnText(1, u"Poids C")
        self.SetColumnText(2, u"Poids S")
        self.SetColumnWidth(1, 60)
        self.SetColumnWidth(2, 60)
        if eleves:
            self.SetColumnWidth(3, 0)
            
          
        
#        self.Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        
       
    

    ####################################################################################
    def Construire(self, branche = None, dic = None, ref = None):
#        print "Construire", dic
        if ref == None:
            ref = self.ref
        if dic == None: # Construction de la racine
            dic = ref._dicCompetences_prj
        if branche == None:
            branche  = self.root
        
        tache = self.pptache.tache
            
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False)
        
        size = None
        if self.eleves:
            tousEleve = [True]*len(tache.projet.eleves)
        
        def const(d, br, debug = False):
            ks = d.keys()
            ks.sort()
            for k in ks:
                if debug: print "****", k
                v = d[k]
                if len(v) > 1 and type(v[1]) == dict:
                    if debug: print "   ", v[0]
                    if len(v) == 2:
                        b = self.AppendItem(br, k+" "+v[0])
                    else:
                        if debug: print "   prem's", v[2]
                        b = self.AppendItem(br, k+" "+v[0])
                        for i, p in enumerate(v[2][1:]):
                            if p != 0:
                                self.SetItemText(b, pourCent2(1.0*p/100), i+1)
                        self.SetItemBold(b, True)
                    self.items[k] = b
                    const(v[1], b, debug = debug)
                        
                else:   # Indicateur
                    
                    cc = [cd+ " " + it for cd, it in zip(k.split(u"\n"), v[0].split(u"\n"))]
#                    c = self.AppendItem(b, u"\n".join(cc), ct_type=1)
              
                    comp = self.AppendItem(br, u"\n ".join(cc))
                    
#                    comp = self.AppendItem(br, k+" "+v[0])
                    
                    self.items[k] = comp
                    b = None #
                    tous = True
                    for i, indic in enumerate(v[1]):
                        codeIndic = k+'_'+str(i+1)
                        if debug:
#                            print not tache.phase in ["R1", "Rev", tache.projet.getCodeLastRevue()]
#                            print codeIndic in tache.indicateursMaxiEleve[0]
                            print ref.getTypeIndicateur(codeIndic)
#                            print tache.phase != 'XXX'
                        
                        if tache == None:
                            b = self.AppendItem(comp, indic[0], data = codeIndic)
                            for j, p in enumerate(indic[1][1:]):
                                if p != 0:
                                    if j == 0:
                                        self.SetItemTextColour(b, COUL_REVUE)
                                    else:
                                        self.SetItemTextColour(b, COUL_SOUT)
                            self.SetItemFont(b, font)
                            
                            
                        if tache != None and ((not tache.phase in ["R1", "Rev", tache.projet.getCodeLastRevue()]) \
                            or (codeIndic in tache.indicateursMaxiEleve[0])) \
                            and (ref.getTypeIndicateur(codeIndic) == "S" or tache.phase != 'XXX'):
                            
                            b = self.AppendItem(comp, indic[0], ct_type=1, data = codeIndic)
                            if codeIndic in tache.indicateursEleve[0]:
                                self.CheckItem2(b)
                            else:
                                tous = False
                                
                            if debug: print "   indic", indic
                            for j, p in enumerate(indic[1][1:]):
                                if p != 0:
                                    self.SetItemText(b, pourCent2(1.0*p/100), j+1)
                                    if j == 0:
                                        self.SetItemTextColour(b, COUL_REVUE)
                                    else:
                                        self.SetItemTextColour(b, COUL_SOUT)
                            self.SetItemFont(b, font)        
                            
                            self.items[codeIndic] = b
                            
                            if self.eleves:
                                self.SetItemWindow(b, ChoixCompetenceEleve(self, codeIndic, 
                                                                           tache.projet, 
                                                                           tache), 3)
                                for e in range(len(tache.projet.eleves)):
                                    tousEleve[e] = tousEleve[e] and self.GetItemWindow(b, 3).EstCocheEleve(e+1)
                                size = self.GetItemWindow(b, 3).GetSize()[0]

                    
                    if b == None: # Désactivation si branche vide d'indicateurs
                        self.SetItemType(br,0)
                    else:
                        self.CheckItem2(br, tous)
#                        if self.eleves:
#                            self.SetItemWindow(c, ChoixCompetenceEleve(self, code, self.pptache.tache.projet, self.pptache.tache), 2)
#                            for e in range(len(self.pptache.tache.projet.eleves)):
#                                self.GetItemWindow(c, 2).CocherEleve(e+1, tousEleve[e])
            return
            
        const(dic, branche, debug = False)
            
        if self.eleves:
            self.SetColumnWidth(3, 60)
        if tache == None: # Cas des arbres dans popup
            self.SetColumnWidth(1, 0)
            self.SetColumnWidth(2, 0)
        self.Refresh()
            
        return
    
    
#        size = False
#        
#        
#        for codeGrp in clefs:
##            self.poids_ctrl[codeGrp] = wx.TextCtrl(self, -1, 
##                                                   str(constantes.dicPoidsIndicateurs[type_ens][codeGrp][0])+"%", 
##                                                   size = (32,20), name = codeGrp)
#            b = self.AppendItem(branche, codeGrp+" "+dic[codeGrp][0])
#            self.SetItemText(b, str(ref._dicCompetences_prj[codeGrp][2][1])+"%", 1)
#            self.SetItemText(b, str(ref._dicCompetences_prj[codeGrp][2][2])+"%", 2)
#            self.SetItemBold(b, True)
##            self.poids_ctrl[codeGrp].Bind(wx.EVT_TEXT, self.OnTextCtrl)
##            self.SetItemWindow(b, self.poids_ctrl[codeGrp], 1)
#            
#            codes = dic[codeGrp][1].keys()
#            codes.sort()
#            for code in codes:
#                intitule = dic[codeGrp][1][code]
#                
#                if type(intitule) == list: # C'est le cas des compétences SSI
#                    sep = u" " + CHAR_POINT + u" "
#                    intitule = intitule[0] + " : " + sep.join(intitule[1].values())
#                
#                
#                cc = [cd+ " " + it for cd, it in zip(code.split(u"\n"), intitule.split(u"\n"))]
#                c = self.AppendItem(b, u"\n".join(cc), ct_type=1)
#                self.items[code] = c
#                        
#                i = None
#                tous = True
#                tousEleve = [True]*len(self.pptache.tache.projet.eleves)
#                for j, Indic in enumerate(ref._dicIndicateurs_prj[code]):
#                    codeIndic = code+'_'+str(j+1)
#                    if (not self.pptache.tache.phase in ["R1", "Rev", self.pptache.tache.projet.getCodeLastRevue()]) or (codeIndic in self.pptache.tache.indicateursMaxiEleve[0]):
#                        if not Indic[1] or self.pptache.tache.phase != 'XXX':
#                            i = self.AppendItem(c, Indic[0], ct_type=1, data = codeIndic)
#                            if codeIndic in self.pptache.tache.indicateursEleve[0]:
#                                self.CheckItem2(i)
#                            else:
#                                tous = False
#                            
#                            self.SetItemText(i, str(ref._dicCompetences_prj[codeGrp][1][code][j])+"%", 1)
#                            self.SetItemFont(i, font)
#                            
#                            if Indic[1]:
#                                self.SetItemTextColour(i, COUL_REVUE)
#                            else:
#                                self.SetItemTextColour(i, COUL_SOUT)
#
#                            self.items[codeIndic] = i
#                     
#                            if self.eleves:
#                                self.SetItemWindow(i, ChoixCompetenceEleve(self, codeIndic, self.pptache.tache.projet, self.pptache.tache), 2)
#                                for e in range(len(self.pptache.tache.projet.eleves)):
#                                    tousEleve[e] = tousEleve[e] and self.GetItemWindow(i, 2).EstCocheEleve(e+1)
#                                if not size:
#                                    size = self.GetItemWindow(i, 2).GetSize()[0]
#                
#                if i == None: # Désactivation si branche vide d'indicateurs
#                    self.SetItemType(c,0)
#                else:
#                    self.CheckItem2(c, tous)
#                    if self.eleves:
#                        self.SetItemWindow(c, ChoixCompetenceEleve(self, code, self.pptache.tache.projet, self.pptache.tache), 2)
#                        for e in range(len(self.pptache.tache.projet.eleves)):
#                            self.GetItemWindow(c, 2).CocherEleve(e+1, tousEleve[e])
#        if self.eleves:
#            self.SetColumnWidth(3, size+2)
#        self.Refresh()

    #############################################################################
    def MiseAJourCaseEleve(self, codeIndic, etat, eleve, propag = True):
        casesEleves = self.GetItemWindow(self.items[codeIndic], 3)
        if casesEleves.EstCocheEleve(eleve) != etat:
            return
        
        estToutCoche = casesEleves.EstToutCoche()

        comp = codeIndic.split("_")[0]
        
        if comp != codeIndic: # Indicateur seul
            item = self.items[codeIndic]
            itemComp = self.items[comp]
            
            if propag:
                tout = True
                for i in itemComp.GetChildren():
                    tout = tout and self.GetItemWindow(i, 3).EstCocheEleve(eleve)
    #            self.GetItemWindow(itemComp, 2).CocherEleve(eleve, tout)
#                print "MiseAJourCaseEleve", comp, eleve
                cases = self.GetItemWindow(self.items[comp], 3)
                if cases != None:
                    cases.CocherEleve(eleve, tout, withEvent = True)
            
#            self.MiseAJourCaseEleve(comp, tout, eleve, forcer = True)
            
            self.AjouterEnleverCompetencesEleve([item], eleve)
            
            self.CheckItem2(item, estToutCoche)
#            self.AjouterEnleverCompetencesItem(item, propag = False)
            
        else: #Compétence complete
            if propag:
                itemComp = self.items[comp]
                for i in itemComp.GetChildren():
    #                self.GetItemWindow(i, 2).CocherEleve(eleve, etat)
    #                self.MiseAJourCaseEleve(self.GetItemPyData(i), etat, eleve, forcer = True)
                    cases = self.GetItemWindow(i, 3)
                    cases.CocherEleve(eleve, etat, withEvent = True)
#            self.CheckItem2(itemComp, estToutCoche)
#            self.AjouterEnleverCompetencesEleve(itemComp.GetChildren(), eleve)
#            self.AjouterEnleverCompetencesItem(itemComp, propag = False)
        
        self.Refresh()
        if propag:
            wx.CallAfter(self.pptache.SetCompetences)
        
        
    #############################################################################
    def OnToolTip(self, event):
        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))
            
            
#    #############################################################################
#    def MiseAJour(self, code = None, value = None):
#        return
#        if code == None:
#            for k, v in constantes._dicCompetences_prj_simple[self.type_ens].items():
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
            
class ArbreCompetencesPopup(CT.CustomTreeCtrl):
    """ Arbre des compétences abordées en projet lors d'une tâche <pptache>
        <revue> : vrai si la tâche est une revue
        <eleves> : vrai s'il faut afficher une colonne supplémentaire pour distinguer les compétences pour chaque éleve
    """
    def __init__(self, parent):
          
        CT.CustomTreeCtrl.__init__(self, parent, -1,
                                   agwStyle = CT.TR_HAS_VARIABLE_ROW_HEIGHT|CT.TR_HIDE_ROOT|CT.TR_NO_LINES)
#        self.SetQuickBestSize(False)
        self.root = self.AddRoot(u"")

    ####################################################################################
    def Construire(self, dic):
#        print "Construire", dic
        
        branche  = self.root
        
        debug = False
            
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False)
        
        def const(d, br, debug = False):
            ks = d.keys()
            ks.sort()
            for k in ks:
                if debug: print "****", k
                v = d[k]
                if len(v) > 1 and type(v[1]) == dict:
                    if debug: print "   ", v[0]
                    if len(v) == 2:
                        b = self.AppendItem(br, textwrap.fill(k+" "+v[0], 50))
                    else:
                        if debug: print "   prem's", v[2]
                        b = self.AppendItem(br, textwrap.fill(k+" "+v[0], 50))
                        self.SetItemBold(b, True)

                    const(v[1], b, debug = debug)
                        
                else:   # Indicateur
                    cc = [cd+ " " + it for cd, it in zip(k.split(u"\n"), v[0].split(u"\n"))] 
                    comp = self.AppendItem(br, textwrap.fill(u"\n ".join(cc), 50))
                    ajouteIndic(comp, v[1])
                    
            return
        
        def ajouteIndic(branche, listIndic):
            for i, indic in enumerate(listIndic):
                b = self.AppendItem(branche, textwrap.fill(indic[0], 50))
                for j, p in enumerate(indic[1][1:]):
                    if p != 0:
                        if j == 0:
                            self.SetItemTextColour(b, COUL_REVUE)
                        else:
                            self.SetItemTextColour(b, COUL_SOUT)
                self.SetItemFont(b, font)
        
        if type(dic) == dict:  
            const(dic, branche, debug = debug)
        else:
            ajouteIndic(branche, dic)
#        self.Update()
        self.Layout()
        self.Parent.Layout()
        self.Refresh()
        
#        self.SetVirtualSize(self.GetWindowBorderSize()+self.GetBestSize())
        self.AdapterSize()
    

#        self.SetMaxSize(self.GetWindowBorderSize()+self.GetVirtualSize())
 
            
        return
    
    
    def AdapterSize(self):
        self.ExpandAll()
#        self.CalculateSize(self.root, wx.ScreenDC())
#        self.PaintItem(self.root, wx.ScreenDC(), 1, 0)
#        print "Size =", self.GetBestSize(), self.GetClientSize(), 
#        print self.GetEffectiveMinSize(), self.GetBoundingRect(self.root), 
#        print self.GetMinClientSize(), self.GetMaxSize(), self.GetMinSize(), 
#        print self.GetVirtualSize(), self.GetBestVirtualSize(),
#        print self.GetWindowBorderSize()+self.GetVirtualSize(), self.GetMaxWidth(respect_expansion_state=False),
#        print self.DoGetVirtualSize()
        ms = self.GetMaxSize2(self.root)
#        print "   **", ms
#        print self.RecurseOnChildren(self.root, 1000, False)
        self.SetMinSize((ms[0]+5, ms[1]+16))


    def GetMaxSize2(self, item, level = 2, maxwidth=0, lastheight = 0):
        dc = wx.ScreenDC()
#        dc.SetFont(self.GetItemFont())
        
        child, cookie = self.GetFirstChild(item)
#        print " level",level
#        print " ",child, cookie
        while child != None and child.IsOk():
            dc.SetFont(self.GetItemFont(child))
#            print "  txt =",self.GetItemText(child)
            W, H, lH = dc.GetMultiLineTextExtent(self.GetItemText(child))
#            print "  W,H, lH =",W,H, lH, self.GetIndent()
            width = W + self.GetIndent()*level + 10
            maxwidth = max(maxwidth, width)
            lastheight += H + 6
            
            maxwidth, lastheight = self.GetMaxSize2(child, level+1, 
                                                    maxwidth, lastheight)
            
            child, cookie = self.GetNextChild(item, cookie)

        return maxwidth, lastheight
    
#    def max_width(self):
#        dc = wx.ScreenDC()
#        dc.SetFont(self.GetFont())
#        widths = []
#        print dir(self)
#        for item, depth in self.__walk_items():
#            if item != self.root:
#                width = dc.GetTextExtent(self.GetItemText(item))[0] + self.GetIndent()*depth
#                widths.append(width)
#        return max(widths) + self.GetIndent()
         
#    def OnPaint(self,event):
#        self.AdapterSize()
        
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
            
###########################################################################################################
#
#  Liste de Checkbox
#
###########################################################################################################
        
class ChoixCompetenceEleve(wx.Panel):
    def __init__(self, parent, indic, projet, tache):
        wx.Panel.__init__(self, parent, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.indic = indic
        self.parent = parent
        
        cb = []
        for e in projet.eleves:
            cb.append(wx.CheckBox(self, -1, ""))
            sizer.Add(cb[-1])
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb[-1])
        self.cb = cb
        
        self.projet = projet
        self.tache = tache
        
        self.MiseAJour()
        self.Actualiser()
        self.SetSizerAndFit(sizer)
    


    #############################################################################
    def MiseAJour(self):
        """ Active/désactive les cases à cocher
            selon que les élèves ont à mobiliser cette compétence/indicateur
        """
#        print "MiseAJour", self.tache
        for i, e in enumerate(self.projet.eleves): 
            dicIndic = e.GetDicIndicateursRevue(self.tache.phase)
            comp = self.indic.split("_")[0]
            if comp in dicIndic.keys():
                if comp != self.indic: # Indicateur seul
                    indic = eval(self.indic.split("_")[1])
                    self.cb[i].Enable(dicIndic[comp][indic-1])
            else:
                self.cb[i].Enable(False)
#            self.cb[i].Update()
        
    #############################################################################
    def Actualiser(self):
        """ Coche/décoche les cases à cocher
            
        """
#        print "Actualiser", self.tache
#        self.CocherTout(self.indic in self.tache.indicateurs)
        
        for i, e in enumerate(self.projet.eleves):
            if self.cb[i].IsThisEnabled ():
                if i+1 in self.tache.indicateursEleve.keys():
                    indicateurs = self.tache.indicateursEleve[i+1]
                    self.cb[i].SetValue(self.indic in indicateurs)
      
            
#            comp = self.indic.split("_")[0]
#            if comp in dicIndic.keys():
#                if comp != self.indic: # Indicateur seul
#                    indic = eval(self.indic.split("_")[1])
#                    self.cb[i].SetValue(dicIndic[comp][indic-1])
#            else:
#                self.cb[i].SetValue(False)
#        self.CocherTout(self.indic in self.tache.indicateurs)
        
            
            
    #############################################################################
    def EvtCheckBox(self, event = None, eleve = None, etat = None):
        if event != None:
            cb = event.GetEventObject()
            eleve = self.cb.index(cb)+1
            etat = event.IsChecked()
        self.parent.MiseAJourCaseEleve(self.indic, etat, eleve, event != None)
        
    #############################################################################
    def CocherTout(self, etat):
        for cb in self.cb:
            if cb.IsEnabled():
                cb.SetValue(etat)
            
    #############################################################################
    def CocherEleve(self, eleve, etat, withEvent = False):
        if self.cb[eleve-1].IsEnabled():
            if etat != self.cb[eleve-1].GetValue():
                self.cb[eleve-1].SetValue(etat)
                if withEvent:
                    self.EvtCheckBox(eleve = eleve, etat = etat)
   
       
    #############################################################################
    def EstToutCoche(self):
        t = True
        for cb in self.cb:
            t = t and cb.GetValue() 
        return t
    
    #############################################################################
    def EstCocheEleve(self, eleve):
        return self.cb[eleve-1].GetValue() 
            


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



def get_key(dic, value, pos = None):
    """ Renvoie la clef du dictionnaire <dic> correspondant à la valeur <value>
    """
    i = 0
    continuer = True
    while continuer:
        if i > len(dic.keys()):
            continuer = False
        else:
            if pos:
                v = dic.values()[i][pos]
            else:
                v = dic.values()[i]
            if v == value:
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
        wx.Log.SetLogLevel(0) # ?? Pour éviter le plantage de wxpython 3.0 avec Win XP pro ???
        
        fichier = ""
        if len(sys.argv)>1: # un paramètre a été passé
            parametre = sys.argv[1]

#           # on verifie que le fichier passé en paramètre existe
            if os.path.isfile(parametre):
                fichier = unicode(parametre, FILE_ENCODING)

        self.AddRTCHandlers()
        
        frame = FenetrePrincipale(None, fichier)
        frame.Show()
        
        if server != None:
            server.app = frame
        
        self.SetTopWindow(frame)
        
        
        return True

    def AddRTCHandlers(self):
        # make sure we haven't already added them.
        if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is not None:
            print u"AddRTCHandlers : déja fait"
            return
        
        # This would normally go in your app's OnInit method.  I'm
        # not sure why these file handlers are not loaded by
        # default by the C++ richtext code, I guess it's so you
        # can change the name or extension if you wanted...
        rt.RichTextBuffer.AddHandler(rt.RichTextHTMLHandler())
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())

        # ...like this
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler(name="Autre XML",
                                                           ext="ox",
                                                           type=99))

        # This is needed for the view as HTML option since we tell it
        # to store the images in the memory file system.
        wx.FileSystem.AddHandler(wx.MemoryFSHandler())



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
    def __init__(self, parent, lien, pathseq, dossier = True, ext = ""):
        wx.Panel.__init__(self, parent, -1)
        self.SetMaxSize((-1,22))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.texte = wx.TextCtrl(self, -1, toSystemEncoding(lien.path), size = (-1, 16))
        if dossier:
            bt1 =wx.BitmapButton(self, 100, wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
            bt1.SetToolTipString(u"Sélectionner un dossier")
            self.Bind(wx.EVT_BUTTON, self.OnClick, bt1)
            sizer.Add(bt1)
        bt2 =wx.BitmapButton(self, 101, wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))
        bt2.SetToolTipString(u"Sélectionner un fichier")
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.texte)
        
        self.ext = ext
        
        sizer.Add(bt2)
        sizer.Add(self.texte,1,flag = wx.EXPAND)
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
                                wildcard = self.ext,
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
    def SetPath(self, lien, marquerModifier = True):
        """ lien doit être de type 'String'
        """
        
        self.lien.EvalLien(lien, self.pathseq)
        
        self.texte.ChangeValue(toSystemEncoding(self.lien.path)) # On le met en DEFAUT_ENCODING
#        self.texte.ChangeValue(self.lien.path) 
#            self.texte.SetBackgroundColour(("white"))
#        else:
#            self.texte.SetBackgroundColour(("pink"))
        self.Parent.OnPathModified(self.lien, marquerModifier = marquerModifier)
        
        
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
import  wx.html as  html

class PopupInfo(wx.PopupWindow):
    def __init__(self, parent, page):
        wx.PopupWindow.__init__(self, parent, wx.BORDER_SIMPLE)
        self.parent = parent
      
        self.html = html.HtmlWindow(self, -1, size = (100,100),style=wx.NO_FULL_REPAINT_ON_RESIZE|html.HW_SCROLLBAR_NEVER)
        self.SetPage(page)
        self.SetAutoLayout(False)
        
        # Un fichier temporaire pour mettre une image ...
        self.tfname = tempfile.mktemp()
        #'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'+

        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
    
    ##########################################################################################
    def SetBranche(self, branche):
        self.branche = branche
        
    ##########################################################################################
    def XML_AjouterImg(self, node, item, bmp):
#        print "XML_AjouterImg"
        try:
            bmp.SaveFile(self.tfname, wx.BITMAP_TYPE_PNG)
        except:
            return
        
        img = node.getElementById(item)
        if img != None:
            td = node.createElement("img")
            img.appendChild(td)
            td.setAttribute("src", self.tfname)

        
    ##########################################################################################
    def OnDestroy(self, evt):
        if os.path.exists(self.tfname):
            os.remove(self.tfname)
            
    ##########################################################################################
    def SetPage(self, page):
#        self.SetSize((10,1000))
#        self.SetClientSize((100,1000))
#        self.html.SetSize( (100, 100) )
#        self.SetClientSize(self.html.GetSize())
        
        self.html.SetPage(page)
        ir = self.html.GetInternalRepresentation()

        self.SetClientSize((ir.GetWidth(), ir.GetHeight()))

        self.html.SetSize( (ir.GetWidth(), ir.GetHeight()) )

        
#        self.SetClientSize(self.html.GetSize())
#        self.SetSize(self.html.GetSize())
        
        
    ##########################################################################################
    def OnLeave(self, event):
        x, y = event.GetPosition()
        w, h = self.GetSize()
        if not ( x > 0 and y > 0 and x < w and y < h):
            self.Show(False)
        event.Skip()
        
        
        
        
        
class PopupInfo2(wx.PopupWindow):
    def __init__(self, parent, titre = "", doc = None, branche = None):
        wx.PopupWindow.__init__(self, parent, wx.BORDER_SIMPLE)
        self.parent = parent
        self.doc = doc
        self.branche = branche
        
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
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        
    ##########################################################################################
    def SetBranche(self, branche):
        self.branche = branche
        
    ##########################################################################################
    def OnClick(self, event):
        if self.doc != None and self.branche != None:
            self.doc.SelectItem(self.branche)
            self.Show(False)
            
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
    def CreerArbre(self, position = (1,0), span = (1,1), ref = None, dic = {}, flag = wx.ALIGN_CENTER):
        arbre = ArbreCompetencesPopup(self)
        self.sizer.Add(arbre, position, span, flag = flag|wx.ALL|wx.EXPAND, border = 5)
        self.Layout()
        self.Fit()
        return arbre
    
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
#        item = self.listeSeq.GetItem(self.currentItem)
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
    def __init__(self, parent, dossierCourant = '', 
                 typeEnseignement = constantes.TYPE_ENSEIGNEMENT_DEFAUT):
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
        for i, e in enumerate(REFERENTIELS.keys()):
            l.append(REFERENTIELS[e].Enseignement[0])
        rb = wx.RadioBox(
                panel, -1, u"Type d'enseignement", wx.DefaultPosition, (130,-1),
                l,
                1, wx.RA_SPECIFY_COLS
                )
        rb.SetToolTip(wx.ToolTip(u"Choisir le type d'enseignement"))
        for i, e in enumerate(REFERENTIELS.keys()):
            rb.SetItemToolTip(i, REFERENTIELS[e].Enseignement[1])
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
            
        # Provosoirement uniquement pour SSI
        for i in [1,2,3,4]:
            rb.EnableItem(i, False)    
        
        self.sizer.Add(rb, (0,0), (2,1), flag = wx.EXPAND|wx.ALL)
        self.cb_type = rb
        self.cb_type.SetStringSelection(REFERENTIELS[self.typeEnseignement].Enseignement[0])
        
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
                
            tableau.setCell(feuilleP, lcp, c, seq.intitule)
            tableau.setCell(feuilleP, ldp, c, str(seq.GetDuree()))
            tableau.setLink(feuilleP, lcp, c, seq.nomFichier)
            tableau.setCell(feuilleP, lcp-1, c, i+1)
            
            for sav in seq.obj["S"].savoirs:
                if sav in REFERENTIELS[self.typeEnseignement].dicCellSavoirs.keys():
                    lig0, lig1 = REFERENTIELS[self.typeEnseignement].dicCellSavoirs[sav]
                    for l in range(lig0, lig1+1):
                        tableau.setCell(feuilleP, l, c, "X")
                else:
                    continuer = True
                    s=1
                    while continuer:
                        sav1 = sav+'.'+str(s)
                        if sav1 in constantes.dicCellSavoirs[self.typeEnseignement].keys():
                            lig0, lig1 = REFERENTIELS[self.typeEnseignement].dicCellSavoirs[sav1]
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
        self.typeEnseignement = Referentiel.getEnseignementLabel(self.cb_type.GetItemLabel(event.GetInt()))[0]
        self.MiseAJourListe()
#        for c, e in constantes.Enseignement.items():
#            if e[0] == self.cb_type.GetItemLabel(event.GetInt()):
#                self.typeEnseignement = c
#                self.MiseAJourListe()
#                break
        
        
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
         
            for f in l:
                classe, sequence = self.OuvrirFichierSeq(f)
                if classe != None and classe.typeEnseignement == self.typeEnseignement:
                    sequence.nomFichier = f
                    listSequences.append(sequence)
                  
            self.listeSeq.MiseAJourListe(listSequences)
            wx.EndBusyCursor()
        
        
        
    ########################################################################################################
    def OuvrirFichierSeq(self, nomFichier):
        fichier = open(nomFichier,'r')

        classe = Classe(self.Parent)
        sequence = Sequence(self, classe)
        classe.SetDocument(sequence)

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
        tw = dc.GetTextExtent(label)[0]
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
        t.SetLabelMarkup( wordwrap(u"<b>pySequence</b> est un logiciel d'aide à l'élaboration de séquences pédagogiques et à la validation de projet,\n"
                                          u"sous forme de fiches exportables au format PDF ou SVG.\n"
                                          u"Il est élaboré en relation avec le programme et le document d'accompagnement\n"
                                          u"des enseignements des filières STI2D et SSI.",500, wx.ClientDC(self)))
        nb.AddPage(descrip, u"Description")
        nb.AddPage(auteurs, u"Auteurs")
        nb.AddPage(licence, u"Licence")
        
        sizer.Add(hl.HyperLinkCtrl(self, wx.ID_ANY, u"Informations et téléchargement : http://code.google.com/p/pysequence/",
                                   URL="http://code.google.com/p/pysequence/"),  
                  flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
        sizer.Add(nb)
        
        self.SetSizerAndFit(sizer)

##############################################################################################################
##
## Connexion à la page Google Drive
## 
##############################################################################################################
#import threading
#class Connexion(threading.Thread): 
#    def __init__(self, nom = ''): 
#        threading.Thread.__init__(self) 
#        self.nom = nom 
#        self._stopevent = threading.Event( ) 
#    
#    def run(self): 
#        i = 0 
#        while not self._stopevent.isSet(): 
#            print self.nom, i 
#            i += 1 
#            self._stopevent.wait(2.0) 
#        print "le thread "+self.nom +" s'est termine proprement" 
#    
#    def stop(self): 
#        self._stopevent.set( ) 
  
#a = Affiche('Thread A') 
#b = Affiche('Thread B') 
#c = Affiche2('Thread C') 
#  
#a.start() 
#b.start() 
#c.start() 
#time.sleep(6.5) 
#a._Thread__stop() 
#b.stop() 
#c.stop()
        


if __name__ == '__main__':
    if sys.platform == "win32":
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
    else:
        app = SeqApp(False)
        app.MainLoop()
    

