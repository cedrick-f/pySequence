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
Copyright (C) 2011-2015
@author: Cedrick FAURY

"""
__appname__= "pySequence"
__author__ = u"Cédrick FAURY"
__version__ = "6.0-beta.12"
print __version__

#from threading import Thread

#import psyco
#psyco.full()

####################################################################################
#
#   TODO
#
####################################################################################
# MEI

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
    mes = u"pySéquence %s a rencontré une erreur et doit fermer !\n\n"\
         u"Merci de copier le message ci-dessous\n" \
         u"et de l'envoyer à l'équipe de développement :\n"\
         u"cedrick point faury arobase ac-clermont point fr\n\n" %__version__
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


sys.excepthook = MyExceptionHook



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
#    import locale
#    loc = locale.getdefaultlocale()
#    print loc
#    if loc[1]:
#        encoding = loc[1]
#        sys.setdefaultencoding(encoding)
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
from widgets import Variable, VariableCtrl, VAR_REEL_POS, EVT_VAR_CTRL, VAR_ENTIER_POS, getHoraireTxt#, chronometrer
#from CustomCheckBox import CustomCheckBox
# Les constantes et les fonctions de dessin


# Les constantes partagées
from constantes import calculerEffectifs, revCalculerEffectifs, PATH, getSingulierPluriel,\
                        strEffectifComplet, getElementFiltre, COUL_OK, COUL_NON, COUL_BOF, COUL_BIEN, \
                        toList, COUL_COMPETENCES, CHAR_POINT, COUL_PARTIE, COUL_ABS
import constantes

# Pour les copier/coller
import pyperclip

import threading 


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
#   Quelques constantes
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
def getNomFichier(prefixe, intitule, extension = r""):
    nomFichier = prefixe+"_"+intitule
    for c in [u"\t", u"\n", "\"", "/", "\\", "?", "<", ">", "|", ":", "."]:
        nomFichier = nomFichier.replace(c, r"_")
    return nomFichier+extension
        
    
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
        
    ######################################################################################  
    def __repr__(self):
        return self.type + " : " + self.path
    
    
    ######################################################################################  
    def __neq__(self, l):
        if self.typ != l.typ:
            return True
        elif self.path != l.path:
            return True
        return False
    
    
    ######################################################################################  
    def DialogCreer(self, pathseq):
        dlg = URLDialog(None, self, pathseq)
        dlg.ShowModal()
        dlg.Destroy() 
            

    ######################################################################################  
    def Afficher(self, pathseq, fenSeq = None):
        path = self.GetAbsPath(pathseq)
#        print "Afficher", path
        
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
            for sce in self.seances:
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
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", 
                                                     functools.partial(self.parent.SupprimerSequencePre, item = itemArbre), 
                                                     images.Icone_suppr_seq.GetBitmap()]
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
        
#    def SetSVGTitre(self, p, titre):
#        print "SetSVGTitre", titre
#        titre = titre.decode(DEFAUT_ENCODING)
#        titre = titre.encode('utf-8') 
#        titre = titre.replace(u"\n", u"<br>")
#        self.elem.setAttribute("xlink:title", titre)
     
    def SetSVGLien(self, p, lien):
#        print "SetSVGLien", lien
        lien = lien.decode(FILE_ENCODING)
        lien = lien.encode('utf-8')
        p.setAttribute("xlink:href", lien) #
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
    def CopyToClipBoard(self, event = None):
        pyperclip.copy(ET.tostring(self.getBranche()))
        
    ######################################################################################  
    def EnrichiSVG(self, doc, seance = False):
#        print "EnrichiSVG", doc, seance
        # 
        # Le titre de la page
        #
        

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
                
                
            if hasattr(self, 'GetLien'):
                lien = self.GetLienHTML()
                t = doc.createElement("a")
                txt = doc.createTextNode(lien)
                t.appendChild(txt)
                np = p.cloneNode(True)
                t.appendChild(np)
                p.parentNode.insertBefore(t, p)
                p.parentNode.removeChild(p)
#                p.appendChild(t)
                
                if lien != '':
                    self.SetSVGLien(t, lien)
        
        
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
    def GetDescription(self):
        if hasattr(self, 'panelPropriete'):
            pp = self.panelPropriete
            if hasattr(pp, 'rtc'):
                return pp.rtc.GetValue()
            
    ######################################################################################  
    def GetBulleSVG(self, i):
        des = ""
#        if hasattr(self, 'description'):
#            des = "\n\n" + self.GetDescription()
            
        if self.GetDescription() != None:
            des = "\n\n" + self.GetDescription()
        t = self.GetCode(i) + " :\n" + self.GetIntit(i) + des
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
    def GetProjetRef(self):
        return self.GetDocument().GetProjetRef()
    
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
            return self.branche
        
        
    ######################################################################################  
    def GetProfondeur(self):
        return 0  
        
        
        

class Classe():
    def __init__(self, app, panelParent = None, intitule = u"", 
                 pourProjet = False, ouverture = False, typedoc = ''):
        self.intitule = intitule
        
        self.academie = u""
        self.ville = u""
        self.etablissement = u""
        self.effectifs = {}
        self.nbrGroupes = {}
        self.systemes = []
        
        self.app = app
        self.panelParent = panelParent
        
        self.Initialise(pourProjet)
        
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Classe(panelParent, self, pourProjet, 
                                                        ouverture = ouverture, typedoc = typedoc)
            self.panelPropriete.MiseAJour()
            
        

        
    ######################################################################################  
    def __repr__(self):
        return "Classe :"#, self.typeEnseignement
    
    ######################################################################################  
    def GetPath(self):
        return r""
    
    ######################################################################################  
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.GetReferentiel().Enseignement[0])
        
#        self.CI = self.options.optClasse["CentresInteret"]
#        self.posCI = self.options.optClasse["PositionsCI"]
        
#        self.ci_SSI = self.options.optClasse["CentresInteretSSI"]
#        self.ci_ET = self.options.optClasse["CentresInteretET"]
#        self.posCI_ET = self.options.optClasse["PositionsCI_ET"]
        

#    ######################################################################################  
#    def SetCI(self, num, ci):
#        self.CI[num] = ci
        
    ######################################################################################  
    def setDefaut(self):
        self.typeEnseignement = 'SSI'
            
        self.effectifs['C'] = constantes.Effectifs["C"]
        self.nbrGroupes = {"G" : constantes.NbrGroupes["G"],
                           "E" : constantes.NbrGroupes["E"],
                           "P" : constantes.NbrGroupes["P"]}
        
        self.academie = u""
        self.ville = u""
        self.etablissement = u""
        
        self.systemes = []


    ######################################################################################  
    def Initialise(self, pourProjet, defaut = False):
        
        if defaut or self.app.options.optClasse["FichierClasse"] == r"":
            self.setDefaut()
            
        else:
            if not self.ouvrir(self.app.options.optClasse["FichierClasse"]):
                self.setDefaut()
            
            
        self.referentiel = REFERENTIELS[self.typeEnseignement]    
        
        # On vérifie que c'est bien un type d'enseignement avec projet
        if pourProjet:
            if not self.typeEnseignement in [ref.Code for ref in REFERENTIELS.values() if len(ref.projets) > 0]:
                self.typeEnseignement = constantes.TYPE_ENSEIGNEMENT_DEFAUT
                self.referentiel = REFERENTIELS[self.typeEnseignement]
        else:    
            self.MiseAJourTypeEnseignement()
        
        self.familleEnseignement = self.GetReferentiel().Famille  
        
        
        
        calculerEffectifs(self)


    ######################################################################################  
    def SetDocument(self, doc):   
        self.doc = doc 


    ###############################################################################################
    def ouvrir(self, nomFichier):
        print "Ouverture classe", nomFichier
        
        try:
            fichier = open(nomFichier,'r')
    
            root = ET.parse(fichier).getroot()
            self.setBranche(root)
            
            fichier.close()
            self.app.fichierClasse = nomFichier
            
            return True

        except:
            print "Erreur Ouverture classe", nomFichier
            return False
        
        self.MiseAJour()


    ######################################################################################  
    def getBranche(self):
#        print "getBranche classe"
        # La classe
        classe = ET.Element("Classe")
        classe.set("Type", self.typeEnseignement)
        
        classe.set("Version", __version__) # à partir de la version 6
        
        classe.append(self.referentiel.getBranche())
        
        classe.set("Etab", self.etablissement)
        classe.set("Ville", self.ville)
        classe.set("Acad", self.academie)
        
        eff = ET.SubElement(classe, "Effectifs")
        eff.set('eC', str(self.effectifs['C']))
        eff.set('nG', str(self.nbrGroupes['G']))
        eff.set('nE', str(self.nbrGroupes['E']))
        eff.set('nP', str(self.nbrGroupes['P']))
                     
#        print "   ", self.systemes
        systeme = ET.SubElement(classe, "Systemes")
        for sy in self.systemes:
            if sy.nom != u"":
                systeme.append(sy.getBranche())
            
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
    def setBranche(self, branche, reparer = False):
        err = []
#        print "setBranche classe"
        self.typeEnseignement = branche.get("Type", constantes.TYPE_ENSEIGNEMENT_DEFAUT)
        
        self.version = branche.get("Version", "0")       # A partir de la version 6 !
        
        #
        # Référentiel
        #
        def ChargerRefOriginal():
            print "Réparation = pas référentiel intégré !"
            if self.GetVersionNum() >= 5:
                code = self.referentiel.setBrancheCodeV5(brancheRef)
                print "   Code trouvé dans référentiel :", code
                if code != self.typeEnseignement:
                    self.typeEnseignement = code
                    
            print "   TypeEnseignement :", self.typeEnseignement
            if self.typeEnseignement in REFERENTIELS:
                self.referentiel = REFERENTIELS[self.typeEnseignement]
            else:
                err.append(constantes.Erreur(constantes.ERR_PRJ_C_TYPENS, self.typeEnseignement))
        
        def RecupCI():
            if self.GetVersionNum() < 5:
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
    #                        self.CI = CI
                            if self.referentiel.CI_cible:
                                self.referentiel.positions_CI = posCI
                                
            elif self.GetVersionNum() == 5:
                brancheCI = branche.find("l_CentresInterets")
                if brancheCI != None: 
                    continuer = True
                    i = 1
                    if self.typeEnseignement == 'ET':
                        CI = []
                        posCI = []
                        while continuer:
                            c = brancheCI.get("S_CentresInterets"+format(i, "02d"))
                            p = brancheCI.get("S_positions_CI"+format(i, "02d"))
                            if c == None or p == None:
                                continuer = False
                            else:
                                CI.append(c)
                                posCI.append(p) 
                                i += 1
                            
                        if i > 1:
                            if self.referentiel.CI_cible:
                                self.referentiel.positions_CI = posCI
    
    
   
        #
        # A partir de la version 5 !
        #
        brancheRef = branche.find("Referentiel")
        if brancheRef != None:   
            self.referentiel = Referentiel.Referentiel()
            if self.GetVersionNum() == 0:       # la version n'était pas encore intégrée dans la version 5 !
                self.version = "5" 
                
            #
            # Ouverture du référentiel original (fourni avec pySéquence)
            #
            if reparer:
                ChargerRefOriginal()
            
            #
            # Ouverture du référentiel intrégré
            #
            else:
#                versionNum = self.GetVersionNum()
                if self.GetVersionNum() == 5:
                    ChargerRefOriginal()
                    RecupCI()
                else:
                    try:
                        self.referentiel.initParam()
                        errr = self.referentiel.setBranche(brancheRef)[1]
                        self.referentiel.corrigerVersion(errr)
                        self.referentiel.postTraiter()
                        self.referentiel.completer()
        
    #                    print self.referentiel.CentresInterets
                    except:
    #                    try:
                        self.referentiel.initParam()
                        self.referentiel.setBrancheV5(brancheRef)
                        ChargerRefOriginal()
                        RecupCI()
    #                    except:
    #                        print "Erreur ouverture référentiel intégré !"
    #                        self.referentiel = REFERENTIELS[self.typeEnseignement]


        #
        # Version < 5 !
        #
        else:
            ChargerRefOriginal()
            RecupCI()
        
        # Correction contradiction 
        if self.typeEnseignement != self.referentiel.Code:
            print "Correction type enseignement", self.typeEnseignement, ">>", self.referentiel.Code
            self.typeEnseignement = self.referentiel.Code

        
            

        #
        # Etablissement
        #
        self.etablissement = branche.get("Etab", u"")
        self.ville = branche.get("Ville", u"")
        self.academie = branche.get("Acad", u"")
        
        self.familleEnseignement = self.referentiel.Famille

        #
        # Effectifs
        #
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
        
        #
        # Systèmes
        #
        self.systemes = []
        brancheSys = branche.find("Systemes")
        if brancheSys != None:
            for sy in list(brancheSys):
                systeme = Systeme(self, self.panelParent)
                systeme.setBranche(sy)
                self.systemes.append(systeme)    
            self.systemes.sort(key=attrgetter('nom'))
            
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()
            
        return err
        
        
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
    def GetVersionNum(self):
        return int(self.version.split(".")[0].split("beta")[0])
    
    
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
        
        self.pasVerouille = True
        
        self.CI = CentreInteret(self, panelParent)
        
        self.obj = {"C" : Competences(self, panelParent),
                    "S" : Savoirs(self, panelParent)}
        self.systemes = []
        self.seances = [Seance(self, panelParent)]
        
#        self.options = classe.options
        
        self.draw = draw_cairo_seq
        
        
    ######################################################################################  
    def __repr__(self):
        return self.intitule
#        t = u"Séquence :"+ + "\n"
#        t += "   " + self.CI.__repr__() + "\n"
#        for c in self.obj.values():
#            t += "   " + c.__repr__() + "\n"
#        for s in self.seances:
#            t += "   " + s.__repr__() + "\n"
#        return t

    ######################################################################################  
    def GetType(self):
        return 'seq'
    
    
    ######################################################################################  
    def Initialise(self):
        self.AjouterListeSystemes(self.classe.systemes)
#        self.AjouterListeSystemes(self.options.optSystemes["Systemes"])
            
            
    ######################################################################################  
    def SetPath(self, fichierCourant):
        pathseq = os.path.split(fichierCourant)[0]
        for sce in self.seances:
            sce.SetPathSeq(pathseq)    
        for sy in self.systemes:
            sy.SetPathSeq(pathseq) 
        
    ######################################################################################  
    def GetDuree(self):
        duree = 0
        for s in self.seances:
            duree += s.GetDuree()
        return duree
    
    
    ######################################################################################  
    def GetProfondeur(self):
        return max([s.GetProfondeur() for s in self.seances])
         
    ######################################################################################  
    def GetNiveau(self):
        return 0
                  
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
        for s in self.seances:
            lst.extend(s.GetPtCaract())
        return lst    
    
    
    ######################################################################################  
    def EnrichiSVG(self, doc):
        if hasattr(self, 'app'):
#            print "   ajout titre"
            t = doc.createElement("title")
            txt = doc.createTextNode(os.path.split(self.app.fichierCourant)[1])
            t.appendChild(txt)
            svg = doc.getElementsByTagName("svg")[0]
#            print svg
            svg.insertBefore(t, svg.childNodes[0])
            
        self.obj["C"].EnrichiSVG(doc)
        self.obj["S"].EnrichiSVG(doc)
        self.prerequis.EnrichiSVG(doc)
        self.CI.EnrichiSVG(doc)
        for s in self.seances:
            s.EnrichiSVGse(doc)
        
        
    ######################################################################################  
    def GetDureeGraph(self):
        duree = 0
        for s in self.seances:
            duree += s.GetDureeGraph()
        return duree
            
    ######################################################################################  
    def GetDureeGraphMini(self):
        duree = 10000
        for s in self.seances:
            duree = min(duree, s.GetDureeGraphMini())
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
        for sce in self.seances:
            seances.append(sce.getBranche())
            
        systeme = ET.SubElement(sequence, "Systemes")
        for sy in self.systemes:
#            c = hasattr(sy, 'panelPropriete') and sy.panelPropriete.cbListSys.GetStringSelection() != u""
            systeme.append(sy.getBranche())
        
        return sequence


    ######################################################################################  
    def setBranche(self, branche):
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
        self.seances = []
        for sce in list(brancheSce):         
            seance = Seance(self, self.panelParent)
            seance.setBranche(sce)
            self.seances.append(seance)
        self.OrdonnerSeances()
        
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()

        
    
        
    ######################################################################################  
    def SetCodes(self):
#        self.CI.SetNum()
#        for comp in self.obj:
#            comp.SetCode()
#        self.obj["C"].SetCode()
#        self.obj["S"].SetCode()
        
        for sce in self.seances:
            sce.SetCode()    
            
        for sy in self.systemes:
            sy.SetCode()    
        
        for ps in self.prerequisSeance:
            ps.SetLabel()
            
    ######################################################################################  
    def PubDescription(self):
        for sce in self.seances:
            sce.PubDescription()    
#            
#        for sy in self.systemes:
#            sy.SetDescription()    
        

            
            
    ######################################################################################  
    def SetLiens(self):
        for sce in self.seances:
            sce.SetLien()    

        for sy in self.systemes:
            sy.SetLien()  

        
    ######################################################################################  
    def VerifPb(self):
#        print "VerifPb"
        for s in self.seances:
            s.VerifPb()
        
    ######################################################################################  
    def MiseAJourNomsSystemes(self):
        for s in self.seances:
            s.MiseAJourNomsSystemes()
    
    ######################################################################################  
    def AjouterSystemeSeance(self):
        for s in self.seances:
            s.AjouterSysteme()
            
    ######################################################################################  
    def AjouterListeSystemesSeance(self, lstSys):
        for s in self.seances:
            s.AjouterListeSystemes(lstSys)
            
    ######################################################################################  
    def SupprimerSystemeSeance(self, i):
        for s in self.seances:
            s.SupprimerSysteme(i) 
            
            
                   
    ######################################################################################  
    def AjouterSeance(self, event = None):
        seance = Seance(self, self.panelParent)
        self.seances.append(seance)
        self.OrdonnerSeances()
        seance.ConstruireArbre(self.arbre, self.brancheSce)
        self.panelPropriete.sendEvent()
        
        self.arbre.SelectItem(seance.branche)
        
        return seance
    
    ######################################################################################  
    def CollerElem(self, event = None, item = None, bseance = None):
        """ Colle la séance présente dans le presse-papier (branche <bseance>)
            après la séance désignée par l'item d'arbre <item>
        """
        
        seance_avant = self.arbre.GetItemPyData(item)
        
        
        if not isinstance(seance_avant, Seance):
            return
        
        if bseance == None:
            try:
                b = ET.fromstring(pyperclip.paste())
            except:
                b = None
            if isinstance(b, Element): # Le presse contient un Element
                if b.tag[:6] == 'Seance': # Le presse contient une tache
                    bseance = b
            if bseance == None:
                return
        
#        print "CollerElem", ET.tostring(bseance)
#        print u"   après :", seance_avant
        
        typeSeance = bseance.get("Type", "")
        
        
        if seance_avant.typeSeance in ['R', 'S']:
            seance = Seance(seance_avant, self.panelParent, typeSeance = typeSeance,
                            branche = bseance)
            seance_avant.seances.insert(0, seance)
        else:
            seance = Seance(self, self.panelParent, typeSeance = typeSeance,
                            branche = bseance)
            i = seance_avant.parent.seances.index(seance_avant)
            seance_avant.parent.seances.insert(i+1, seance)
        
        
        self.OrdonnerSeances()
        seance.ConstruireArbre(self.arbre, self.brancheSce)
        self.reconstruireBrancheSeances(seance_avant, seance)
        
        
        self.panelPropriete.sendEvent()
        
        self.arbre.SelectItem(seance.branche)
    
    ######################################################################################  
    def SupprimerSeance(self, event = None, item = None):
#        print "SupprimerSeance depuis :", self.code
#        print "   ", self.seances
        if len(self.seances) > 1: # On en laisse toujours une !!
            seance = self.arbre.GetItemPyData(item)
#            print " ---",  seance
            self.seances.remove(seance)
            self.arbre.Delete(item)
            self.OrdonnerSeances()
            self.panelPropriete.sendEvent()
            return True
        return False
    
    
    ######################################################################################  
    def OrdonnerSeances(self):
#        print "OrdonnerSeances"
        listeTypeSeance = self.GetReferentiel().listeTypeSeance
        dicType = {k:0 for k in listeTypeSeance}
        dicType[''] = 0
        RS = 0
        if hasattr(self, 'seances'): # c'est une sous séance
            for i, sce in enumerate(self.seances):
                sce.ordre = i
                if sce.typeSeance in ['R', 'S']:
    #                print sce
                    sce.ordreType = RS
                    RS += 1
                else:
                    sce.ordreType = dicType[sce.typeSeance]
                    dicType[sce.typeSeance] += 1
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
    def AjouterListeSystemes(self, syst = []):
#        print "AjouterListeSystemes séquence"
        nouvListe = []
        for s in syst:
#            print "   ",s
            
            if not isinstance(s, Systeme):
                erreur
                sy = Systeme(self, self.panelParent)
                sy.setBranche(ET.fromstring(s))
            else:
                sy = s.Copie(self, self.panelParent)
                sy.lienClasse = s
                sy.panelPropriete.Verrouiller(False)
                sy.panelPropriete.cbListSys.SetSelection(sy.panelPropriete.cbListSys.FindString(s.nom))
#            try:
#                sy.setBranche(ET.fromstring(s))
#            except:
#                print "Erreur parsing :", s
#                continue
            
#            nom = unicode(s)
#            sy = Systeme(self, self.panelParent, nom = nom)
            
            self.systemes.append(sy)
            nouvListe.append(sy.nom)
            sy.ConstruireArbre(self.arbre, self.brancheSys)
            sy.SetCode()
#            sy.nbrDispo.v[0] = eval(n)
            sy.panelPropriete.MiseAJour()
        
        self.arbre.Expand(self.brancheSys)
        self.AjouterListeSystemesSeance(nouvListe)
        self.panelPropriete.sendEvent()
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
            dlg = wx.MessageDialog(self.app, u"Sélection de systèmes depuis Excel\n\n" \
                                             u"Excel doit à présent être lancé.\n" \
                                             u"\t- selectionner les cellules contenant les informations,\n" \
                                             u"\t- puis appuyer sur Ok.\n\n" \
                                             u"Format attendu de la selection :\n" \
                                             u"|    colonne 1    |    colonne 2      |    colonne 3    |\n" \
                                             u"|                         | (optionnelle)    | (optionnelle) |\n" \
                                             u"|    systèmes     |   nombre dispo | fichiers image|\n" \
                                             u"|   ...                   |   ...                      |   ...                    |\n",
                                             u'Sélection de systèmes',
                                             wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                             )
            res = dlg.ShowModal()
            dlg.Destroy() 
            if res == wx.ID_YES:
                ls = recup_excel.getSelectionExcel()
                if ls != None:
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
        seance.seances.append(seanceR1)
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
        for sce in self.seances:
            sce.ConstruireArbre(arbre, self.brancheSce) 
            
        self.brancheSys = arbre.AppendItem(self.branche, Titres[4], image = self.arbre.images["Sys"], data = self.panelSystemes)
        for sy in self.systemes:
            sy.ConstruireArbre(arbre, self.brancheSys)    
        
        
        
    ######################################################################################  
    def reconstruireBrancheSeances(self, b1, b2):
        self.arbre.DeleteChildren(self.brancheSce)
        for sce in self.seances:
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
            self.app.AfficherMenuContextuel([[u"Enregistrer", self.app.commandeEnregistrer, 
                                              wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, (20,20))],
#                                             [u"Ouvrir", self.app.commandeOuvrir],
                                             [u"Exporter la fiche (PDF ou SVG)", self.app.exporterFiche, None],
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
            self.app.AfficherMenuContextuel([[u"Ajouter une séance", 
                                              self.AjouterSeance,
                                             images.Icone_ajout_seance.GetBitmap()]])
            
        elif self.arbre.GetItemText(itemArbre) == Titres[4]: # Système
            self.app.AfficherMenuContextuel([[u"Ajouter un système", 
                                              self.AjouterSysteme,
                                              images.Icone_ajout_systeme.GetBitmap()], 
                                             [u"Selectionner depuis un fichier", 
                                              self.SelectSystemes, 
                                              None],
#                                             [u"Sauvegarder la liste dans les préférences", self.SauvSystemes]
                                             ])
         
        elif self.arbre.GetItemText(itemArbre) == Titres[1]: # Prérequis
            self.app.AfficherMenuContextuel([[u"Ajouter une séquence", self.AjouterSequencePre, 
                                              images.Icone_ajout_seq.GetBitmap()], 
                                             ])
         
            
    ######################################################################################       
    def GetSystemesUtilises(self):
        """ Renvoie la liste des systèmes utilisés pendant la séquence
        """
        lst = []
        for s in self.systemes:
            n = 0
            for se in self.seances:
                ns = se.GetNbrSystemes(complet = True)
                if s.nom in ns.keys():
                    n += ns[s.nom]
            if n > 0:
                lst.append(s)
        return lst
    
            
    ######################################################################################  
    def GetNbreSeances(self):
        n = 0
        for s in self.seances:
            if s.typeSeance in ["R", "S"]:
                n += len(s.seances)
            n += 1
        return n
    
    
    ######################################################################################  
    def GetToutesSeances(self):
        l = []
        for s in self.seances:
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
        try:
            return self.classe.GetReferentiel()
        except:
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
            autresZones = self.seances + self.systemes + self.obj.values()
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
    def MiseAJourTypeEnseignement(self, ancienRef = False, ancienneFam = False):
        self.app.SetTitre()
        self.classe.MiseAJourTypeEnseignement()
        self.CI.MiseAJourTypeEnseignement()
        self.obj['C'].MiseAJourTypeEnseignement()
        for o in self.obj.values():
            o.MiseAJourTypeEnseignement()
        self.prerequis.MiseAJourTypeEnseignement()
        for s in self.seances:
            s.MiseAJourTypeEnseignement()
        self.panelPropriete.MiseAJour()
        
        
    #############################################################################
    def Verrouiller(self):
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
        
        self.version = "" # version de pySéquence avec laquelle le fichier a été sauvegardé
        
        # code désignant le type de projet
#        print "init Projet"
#        print "   ", self.GetReferentiel()
        self.code = self.GetReferentiel().getCodeProjetDefaut()
#        print "   ", self.code
        self.position = self.GetProjetRef().getPeriodeEval()
#        print "   ", self.position
        self.nbrParties = 1
        
        # Organisation des revues du projet
        self.initRevues()

        # Année Scolaire
        self.annee = constantes.getAnneeScolaire()
        
        self.pasVerouille = True
        
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
        
        #
        # Spécifiquement pour la fiche de validation
        #
        self.origine = u""
        self.contraintes = u""
        self.besoinParties = u""
        self.intituleParties = u""

        self.production = u""
        
        self.synoptique = u""
        self.typologie = []
        
        # Prtie "Partenariat ('PAR')
        self.partenariat = u""
        self.montant = u""
        self.src_finance = u""
        
        
        self.SetPosition(self.position)
        
        
#       
        
        
    ######################################################################################  
    def __repr__(self):
        return self.intitule

    ######################################################################################  
    def GetType(self):
        return 'prj'
        
    ######################################################################################  
    def GetProjetRef(self):
        if self.code == None:
            return self.GetReferentiel().getProjetDefaut()
        else:
            if self.code in self.GetReferentiel().projets.keys():
                return self.GetReferentiel().projets[self.code]
            else:
                return None
    
    
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
            lr = [_R1, _R2, "S"]
        else:
            lr = TOUTES_REVUES_EVAL_SOUT
        for p in lr:
            lst.append(Tache(self, self.panelParent, 
                             intitule = self.GetProjetRef().phases[p][1], 
                             phaseTache = p, duree = 0))
        return lst
    
    ######################################################################################  
    def getTachesRevue(self):
        return [t for t in self.taches if t.phase in TOUTES_REVUES_EVAL_SOUT]
#        lst = []
#        for t in self.taches:
#            if t.phase in TOUTES_REVUES_EVAL_SOUT:
#                lst.append(t)
#        return lst
        
        
#    ######################################################################################  
#    def getTachesRevue(self):    
    
    ######################################################################################  
    def getCodeLastRevue(self):
        return "R"+str(int(self.nbrRevues))
#        if self.nbrRevues == 2:
#            return _R2
#        else:
#            return _R3
        
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
#        for s in self.seances:
#            s.EnrichiSVGse(doc)
        return
            
    
    ######################################################################################  
    def GetBulleSVG(self, i):
        if i >= 0:
            c = self.GetCompetencesUtil()
            prj = self.classe.GetProjetRef()
            lstIndic = prj._dicIndicateurs_simple[c[i]]
#            lstIndic = REFERENTIELS[self.classe.typeEnseignement]._dicIndicateurs_prj_simple[c[i]]
            t = c[i] + " :\n" + u"\n".join([indic.intitule for indic in lstIndic])
            return t.encode(DEFAUT_ENCODING)
        else:
            e = self.eleves[-1-i]
            t = e.GetNomPrenom()+"\n"
            t += u"Durée d'activité : "+draw_cairo.getHoraireTxt(e.GetDuree())+"\n"
            t += u"Evaluabilité :\n"
            ev_tot = e.GetEvaluabilite()[1]
            t += u"\tconduite : "+pourCent2(ev_tot['R'][0], True)+"\n"
            t += u"\tsoutenance : "+pourCent2(ev_tot['S'][0], True)+"\n"
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
        
        projet.set("Version", __version__) # à partir de la version 5.7
        
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

        projet.set("Synoptique", remplaceLF2Code(self.synoptique))
        
        typologie = ET.SubElement(projet, "Typologie")
        for i, t in enumerate(self.typologie):
            typologie.set("T_"+str(i), str(t))
        
        projet.set("Partenaires", remplaceLF2Code(self.partenariat))
        projet.set("Montant", remplaceLF2Code(self.montant))
        projet.set("SrcFinance", remplaceLF2Code(self.src_finance))
        
#        comp = ET.SubElement(projet, "Competences")
#        for k, lc in constantes._dicCompetences_prj_simple[self.classe.typeEnseignement].items():
#            comp.set(k, str(lc[1]))
        
        return projet
        
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche projet"
#        print self.GetReferentiel()
        
        err = []
        
        self.intitule = branche.get("Intitule", u"")
        
        self.version = branche.get("Version", "")       # A partir de la version 5.7 !

        self.problematique = remplaceCode2LF(branche.get("Problematique", u""))
        
        self.commentaires = branche.get("Commentaires", u"")
        
        self.nbrRevues = eval(branche.get("NbrRevues", str(self.GetProjetRef().getNbrRevuesDefaut())))
        if not self.nbrRevues in self.GetProjetRef().posRevues.keys():
            self.nbrRevues = self.GetProjetRef().getNbrRevuesDefaut()
        self.positionRevues = branche.get("PosRevues", 
                                          '-'.join(list(self.GetProjetRef().posRevues[self.nbrRevues]))).split('-')

        if self.nbrRevues == 3:
            self.MiseAJourNbrRevues()
        
        self.MiseAJourTypeEnseignement()
        
        self.position = eval(branche.get("Position", "0"))
        if self.version == "": # Enregistré avec une version de pySequence > 5.7
            if self.position == 5:
#                print "Correction position"
                self.position = self.GetProjetRef().getPeriodeEval()
            
            
        self.annee = eval(branche.get("Annee", str(constantes.getAnneeScolaire())))

        brancheEqu = branche.find("Equipe")
        self.equipe = []
        for e in list(brancheEqu):
            prof = Prof(self, self.panelParent)
            Ok = prof.setBranche(e)
            if not Ok : 
                err.append(constantes.Erreur(constantes.ERR_PRJ_EQUIPE))
            self.equipe.append(prof)

        brancheSup = branche.find("Support")
        if brancheSup != None:
            Ok = self.support.setBranche(brancheSup)
            if not Ok : 
                err.append(constantes.Erreur(constantes.ERR_PRJ_SUPPORT))
        
        brancheEle = branche.find("Eleves")
        self.eleves = []
        for e in list(brancheEle):
            eleve = Eleve(self, self.panelParent)
            Ok = eleve.setBranche(e)
            if not Ok : 
                err.append(constantes.Erreur(constantes.ERR_PRJ_ELEVES))
            
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
      
        self.synoptique = remplaceCode2LF(branche.get("Synoptique", u""))
        
        self.typologie = []
        typologie = branche.find("Typologie")
        if typologie != None:
            i = 0
            continuer = True
            while continuer:
                t = typologie.get("T_"+str(i), u"")
                if t == u"":
                    continuer = False
                else:
                    self.typologie.append(eval(t))
                    i += 1
            
        self.partenariat = remplaceCode2LF(branche.get("Partenaires", u""))
        self.montant = remplaceCode2LF(branche.get("Montant", u""))
        self.src_finance = remplaceCode2LF(branche.get("SrcFinance", u""))
        
        
      
        #
        # Les poids des compétences (Fixés depuis BO 2014)
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
            if phase in TOUTES_REVUES_EVAL_SOUT:
                if phase == "S":
                    num = len(tachesRevue)-1
                else:
                    num = eval(phase[1])-1
                
                e = tachesRevue[num].setBranche(e)
                err.extend(e)
                if len(e) > 0:
                    err.append(constantes.Erreur(constantes.ERR_PRJ_TACHES, phase))
            
                self.taches.append(tachesRevue[num])
                adapterVersion = False
            else:
                tache = Tache(self, self.panelParent, branche = e)
                if tache.code < 0 : # ça s'est mal passé lors du setbranche ...
                    err.append(constantes.Erreur(constantes.ERR_PRJ_TACHES, tache.code))
                    return err
                    
#                tache.setBranche(e)
                self.taches.append(tache)
#        self.CorrigerIndicateursEleve()
        
        # Pour récupérer les prj créés avec la version beta1
        if adapterVersion:
            self.taches.extend(tachesRevue)
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()

        return err
        
    ######################################################################################  
    def GetLastPosition(self):
        n = 0
        for p in self.GetReferentiel().periodes:
            n+=p[1]
        n = n - (self.GetProjetRef().periode[-1] - self.GetProjetRef().periode[0])
        return n-1
    
    
    
    ######################################################################################  
    def SetPosition(self, pos):
#        print "SetPosition", pos
#        print "  position actuelle :", self.position
#        posEpreuve = self.GetProjetRef().getPeriodeEval()
        kproj = self.GetReferentiel().getProjetEval(pos+1)
#        print "   ", kproj
#        print "  posEpreuve", posEpreuve
    

        ###################################################################
        # on efface toutes les revues
        def effacerRevues():
            lst = []
            for t in self.taches:
                if t.phase in TOUTES_REVUES_EVAL_SOUT:
                    lst.append(t.branche)
            for a in reversed(lst):
                self.SupprimerTache(item = a, verrouiller = False)
        
        
        
        # On change de projet
        if self.code != kproj:
            self.code = kproj
            effacerRevues()
            
            # On passe à une position "épreuve"
            if self.code != None:
                for tr in self.creerTachesRevue():
                    self.taches.append(tr)
                    tr.ConstruireArbre(self.arbre, self.brancheTac)
                    tr.SetCode()
                    if hasattr(tr, 'panelPropriete'):
                        tr.panelPropriete.MiseAJour()
                self.OrdonnerTaches()
                self.arbre.Ordonner(self.brancheTac)
                if hasattr(self, 'panelPropriete'):
                    self.panelPropriete.sendEvent()
    

                
            
            
        # Sinon on se contente de redessiner
        else:
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.sendEvent()
        
        
        
#        # On passe à la position "épreuve"
#        if pos == posEpreuve and self.position != posEpreuve:
#            for tr in self.creerTachesRevue():
#                self.taches.append(tr)
#                tr.ConstruireArbre(self.arbre, self.brancheTac)
#                tr.SetCode()
#                if hasattr(tr, 'panelPropriete'):
#                    tr.panelPropriete.MiseAJour()
#            self.OrdonnerTaches()
#            self.arbre.Ordonner(self.brancheTac)
#            if hasattr(self, 'panelPropriete'):
#                self.panelPropriete.sendEvent()
#
#                
#        # On passe de la position "épreuve" à une autre
#        elif pos !=posEpreuve and self.position == posEpreuve:
#            lst = []
#            for t in self.taches:
#                if t.phase in TOUTES_REVUES_EVAL_SOUT:
#                    lst.append(t.branche)
#            for a in reversed(lst):
#                self.SupprimerTache(item = a, verrouiller = False)
#        
#        
#        # Sinon on se contente de redessiner
#        else:
#            if hasattr(self, 'panelPropriete'):
#                self.panelPropriete.sendEvent()
            
            
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
        lstPhasesTaches = [k.phase for k in self.taches if k.phase in TOUTES_REVUES_EVAL]
#        print "   ", lstPhasesTaches
        if self.nbrRevues == 3 and not _R3 in lstPhasesTaches: # on ajoute une revue
            self.positionRevues.append(self.positionRevues[-1])
            tache = Tache(self, self.panelParent, 
                          intitule = self.GetProjetRef().phases[_R3][1], 
                          phaseTache = _R3, duree = 0)
            self.taches.append(tache)
            tache.ConstruireArbre(self.arbre, self.brancheTac)
            tache.SetPhase()
            
            revue2 = self.getTachesRevue()[1]
            revue2.panelPropriete = PanelPropriete_Tache(self.panelParent, revue2, revue = True)
            
            
        elif self.nbrRevues == 2 and _R3 in lstPhasesTaches:
            t = self.getTachesRevue()[2]
            self.SupprimerTache(item = t.branche)
            revue2 = self.getTachesRevue()[1]
            revue2.panelPropriete = PanelPropriete_Tache(self.panelParent, revue2, revue = True)
        return


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
            if not tacheAct.phase in TOUTES_REVUES:
                phase = tacheAct.phase
            elif tacheAct.phase == "Rev":
                i = self.taches.index(tacheAct)
                if i > 0 and self.taches[i-1].phase not in TOUTES_REVUES_SOUT:
                    phase = self.taches[i-1].phase 
                elif i+1<len(self.taches) and self.taches[i+1].phase not in TOUTES_REVUES_SOUT:
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

            tache = Tache(self, self.panelParent, phaseTache = phase)
            self.taches.append(tache)
            tache.ordre = tacheAct.ordre+0.5 # truc pour le tri ...
            tache.ConstruireArbre(self.arbre, self.brancheTac)
            
            tache.SetPhase()
            if hasattr(tache, 'panelPropriete'):
                tache.panelPropriete.MiseAJour()
        
        self.Verrouiller()

        self.arbre.EnsureVisible(tache.branche)
        for i in self.arbre._itemWithWindow:
            self.arbre.HideWindows()
        self.arbre.SelectItem(tache.branche)

        self.panelPropriete.sendEvent()

        return tache
    
#    ######################################################################################  
#    def CopierTache(self, event = None, item = None):
#        tache = self.arbre.GetItemPyData(item)
#        if isinstance(tache, Tache):
#            self.GetApp().parent.SetData(tache.getBranche())
#            print "Tache", tache, u"copiée"

    ######################################################################################  
    def CollerElem(self, event = None, item = None, btache = None):
        """ Colle la tâche présente dans le presse-papier (branche <btache>)
            après la tâche désignée par l'item d'arbre <item>
        """
        tache_avant = self.arbre.GetItemPyData(item)
        if not isinstance(tache_avant, Tache):
            return
        
        if btache == None:
            try:
                b = ET.fromstring(pyperclip.paste())
            except:
                b = None
            if isinstance(b, Element): # Le presse contient un Element
                if b.tag[:5] == 'Tache': # Le presse contient une tache
                    phase = b.get("Phase", "")
                    if tache_avant.phase == phase or tache_avant.GetSuivante().phase == phase : # la phase est la même
                        btache = b
            if btache == None:
                return
        
        phase = btache.get("Phase", "")
        if tache_avant.phase != phase and tache_avant.GetSuivante().phase != phase : # la phase est la même
            return
#
#         or tache_avant.phase != btache.get("Phase", ""): # la phase est la même
#            return
        
        tache = Tache(self, self.panelParent, phaseTache = "", branche = btache)
        
        tache.ordre = tache_avant.ordre+1
        for t in self.taches[tache_avant.ordre:]:
            t.ordre += 1
        self.taches.insert(tache_avant.ordre, tache)
#        self.taches.sort(key=attrgetter('ordre'))
        for t in self.taches[tache_avant.ordre:]:
            t.SetCode()

            
        tache.ConstruireArbre(self.arbre, self.brancheTac)
        tache.SetCode()
        if hasattr(tache, 'panelPropriete'):
            tache.panelPropriete.MiseAJour()
            tache.panelPropriete.MiseAJourEleves()
        
        self.arbre.Ordonner(self.brancheTac)
        self.panelPropriete.sendEvent()
        self.arbre.SelectItem(tache.branche)
            
        self.Verrouiller()
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
            
        self.Verrouiller()
        
    ######################################################################################  
    def SupprimerTache(self, event = None, item = None, verrouiller = True):
        tache = self.arbre.GetItemPyData(item)
        self.taches.remove(tache)
        self.arbre.Delete(item)
        self.SetOrdresTaches()
        self.panelPropriete.sendEvent()
        if verrouiller:
            self.Verrouiller()
        
        
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
        prj = self.GetProjetRef()
        Rev = []
        for i, t in enumerate(lstTaches):
            if t.phase == _Rev:
                if i > 0:
                    Rev.append((t, lstTaches[i-1]))
                else:
                    Rev.append((t, None))   # Après la première tâche

#        print Rev
        
        
        #
        # On fait des paquets par catégorie
        #
        paquet = {'': []}
        for k in prj.listPhases:#['STI']+constantes.NOM_PHASE_TACHE_E.keys(): 
            paquet[k]=[]

        for t in lstTaches:
            paquet[t.phase].append(t)
            
#        print paquet
        
        # On trie les tâches de chaque paquet  
        for c in [k for k in prj.listPhases if not k in prj.listPhasesEval]:#['Ana', 'Con', 'Rea', 'DCo', 'Val', 'XXX']:
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
#            print "   ", r, q
            if q == None:
                lst.insert(0, r)
            else:
                i = lst.index(q)
#                print "     >>", i
                lst.insert(i+1, r)
    
        #
        # On ajoute les tâches sans phase
        #
        if '' in paquet.keys():
            lst.extend(paquet[''])
            
#        print lst
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
        if isinstance(data, Tache) and data.phase not in TOUTES_REVUES_EVAL_SOUT:
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
        for sce in self.seances:
            sce.ConstruireArbre(self.arbre, self.brancheSce) 
        self.arbre.Expand(b1.branche)
        self.arbre.Expand(b2.branche)
        
    
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):    
        """ Affiche le menu contextuel associé é la séquence
            ... ou bien celui de itemArbre concerné ...
        """
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([[u"Enregistrer", self.app.commandeEnregistrer,
                                              wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, (20,20))],
#                                             [u"Ouvrir", self.app.commandeOuvrir],
                                             [u"Exporter la fiche (PDF ou SVG)", self.app.exporterFiche, None],
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
            self.app.AfficherMenuContextuel([[u"Ajouter un élève", self.AjouterEleve, images.Icone_ajout_eleve.GetBitmap()]])
            
        elif self.arbre.GetItemText(itemArbre) == Titres[8]: # Tache
            self.app.AfficherMenuContextuel([[u"Ajouter une tâche", self.AjouterTache, images.Icone_ajout_tache.GetBitmap()]])
         
        elif self.arbre.GetItemText(itemArbre) == Titres[10]: # Eleve
            self.app.AfficherMenuContextuel([[u"Ajouter un professeur", self.AjouterProf, images.Icone_ajout_prof.GetBitmap()]])
                                             
         
            
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
        prj = self.GetProjetRef()
        for p in self.GetListePhases():
            if p in prj.listPhases:#[:-1]:
                n = prj.phases[p][0]
                if not p in TOUTES_REVUES_EVAL_SOUT:
                    n = u"     "+n
                lst.append(n)
            elif p in prj.listPhasesEval:
                n = prj.phases[p][0]
                if not p in TOUTES_REVUES_EVAL_SOUT:
                    n = u"     "+n
                lst.append(n)
                
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
#        print "GetListePhases",
#        lst = list(constantes.PHASE_TACHE[self.GetTypeEnseignement(simple = True)][:-1])
        lst = [k for k in self.GetProjetRef().listPhases if not k in self.GetProjetRef().listPhasesEval]
#        lst = list(self.GetReferentiel().listPhases_prj)
#        print "  ", self.classe.GetReferentiel()
#        print "  ", lst
#        print "  ", self.nbrRevues,
        lr = range(1, self.nbrRevues+1)
        lr.reverse()

        for r in lr:
#            print "     ", lr,  self.positionRevues[r-1]
            if self.positionRevues[r-1] in  lst:
                lst.insert(lst.index(self.positionRevues[r-1])+1, "R"+str(r))
#        print "  ", lst
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
        return getNomFichier(prefixe, self.intitule[:20])
#        nomFichier = prefixe+"_"+self.intitule[:20]
#        for c in ["\"", "/", "\", ", "?", "<", ">", "|", ":", "."]:
#            nomFichier = nomFichier.replace(c, "_")
#        return nomFichier
        
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
    def MiseAJourTypeEnseignement(self, ancienRef = None, ancienneFam = None):#, changeFamille = False):
#        print "MiseAJourTypeEnseignement projet", ancienRef, ">>", self.GetReferentiel()
        
        self.app.SetTitre()
        
        self.code = self.GetReferentiel().getCodeProjetDefaut()
#        print "   ", self.code

        if ancienRef != None:
#            print "   anciennePos", self.position
            anciennePos = self.position
            
            kprj = ancienRef.getProjetEval(anciennePos+1)
#            print "   ancien prj", kprj, self.GetReferentiel().projets.keys()
            if kprj in self.GetReferentiel().projets.keys():
                self.code = kprj
                self.position = self.GetProjetRef().getPeriodeEval()
            else:
                posRel = 1.0*anciennePos/ancienRef.getNbrPeriodes()
                self.position = round(self.GetReferentiel().getNbrPeriodes()*posRel)-1
                self.code = self.GetReferentiel().getProjetEval(self.position+1)
            
        else:
            self.position = self.GetProjetRef().getPeriodeEval()
            
        
        for t in self.taches:
            if t.phase in TOUTES_REVUES_EVAL and self.GetReferentiel().compImposees['C']:
                t.panelPropriete.Destroy()
                t.panelPropriete = PanelPropriete_Tache(t.panelParent, t)
            t.MiseAJourTypeEnseignement(self.classe.referentiel)
        
        for e in self.eleves:
            e.MiseAJourTypeEnseignement()
        
            
#        print "   ", self.position
#            if ancienRef.estPeriodeEval(anciennePos):
#                self.position = self.GetProjetRef().getPeriodeEval()
##                print "   new pos eval =", self.position
#            else:
#                posRel = 1.0*anciennePos/ancienRef.getNbrPeriodes()
#                self.position = round(self.GetProjetRef().getNbrPeriodes()*posRel)-1
##                print "   new pos =", self.position
        
        
        
        if hasattr(self, 'panelPropriete'):
#            if ancienneFam != self.classe.familleEnseignement:
            self.initRevues()
            self.MiseAJourNbrRevues()
            
            self.panelPropriete.MiseAJourTypeEnseignement()
        
        self.SetPosition(self.position)




    #############################################################################
    def initRevues(self):
#        print "initRevues",
        self.nbrRevues = self.GetReferentiel().getNbrRevuesDefaut(self.code)
        self.positionRevues = list(self.GetReferentiel().getPosRevuesDefaut(self.code))
#        print self.nbrRevues, self.positionRevues
        

    #############################################################################
    def Verrouiller(self):
        self.pasVerouille = len(self.GetCompetencesUtil()) == 0 and len(self.taches) == self.nbrRevues+1
        self.classe.Verrouiller(self.pasVerouille)
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.Verrouiller(self.pasVerouille)
        
#    #############################################################################
#    def CorrigerIndicateursEleve(self):
#        """
#        """
#        return
#        if self.nbrRevues == 2:
#            lstR = [_R1]
#        else:
#            lstR = [_R1, _R2]
#        for t in self.taches:
#            if t.phase in lstR:
#                for i, e in enumerate(self.eleves):
#                    pass
        
    
    ######################################################################################  
    def TesterExistanceGrilles(self, nomFichiers):
#        print "TesterExistanceGrilles", nomFichiers

        existe = []
        for fe in nomFichiers.values():
            for f in fe.values():
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
    
    
    ######################################################################################  
    def VerifierIndicRevue(self, numRevue):
        r = self.getTachesRevue()[numRevue-1]
        self.SetCompetencesRevuesSoutenance()
#        print r.phase
#        print r.indicateursMaxiEleve[0]
#        print r.GetDicIndicateursEleve(self.eleves[1])
#        print r.indicateursEleve
        
        for codes in r.indicateursEleve.values():
            for code in codes:
                if not code in r.indicateursMaxiEleve[0]:
                    codes.remove(code)
                   
#        print r.indicateursEleve
        return


    #############################################################################
    def MiseAJourTachesEleves(self):
        """ Mise à jour des phases de revue 
            pour lesquelles il y a des compétences à cocher
        """
        for t in self.taches:
            if t.phase in [_R1, "Rev"] or (t.phase == _R2 and self.nbrRevues == 3):
                if hasattr(t.panelPropriete, 'arbre'):
                    t.panelPropriete.arbre.MiseAJourTypeEnseignement(t.GetReferentiel())
                    t.panelPropriete.MiseAJour()

    
    #############################################################################
    def SetCompetencesRevuesSoutenance(self, miseAJourPanel = True):
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
            
            if t.phase in TOUTES_REVUES_SOUT:
#                print "  ", t.phase
                for neleve in range(len(self.eleves)+1):

                    if t.phase in [_R1, "Rev"] or (t.phase == _R2 and self.nbrRevues == 3):
                        t.indicateursMaxiEleve[neleve] = []
                    else:
                        t.indicateursEleve[neleve] = []

                    for c, l in indicateurs[neleve].items():
                        for i, ok in enumerate(l):
                            if ok:
                                codeIndic = c+"_"+str(i+1)
                                
                                # Phase de Conduite
                                if self.GetProjetRef().getTypeIndicateur(codeIndic) == 'C': # tousIndicateurs[c][i][1]: # Indicateur "revue"
                                    if t.phase in TOUTES_REVUES:
                                        
                                        if self.GetReferentiel().compImposees['C']:
                                            if self.GetProjetRef().getIndicateur(codeIndic).getRevue() == t.phase:
#                                                print "  compImposees", t.phase, ":", codeIndic
                                                t.indicateursEleve[neleve].append(codeIndic)
#                                                print "  >>", t.indicateursEleve
                                                
                                        elif t.phase in [_R1, _Rev] or (t.phase == _R2 and self.nbrRevues == 3):
                                            t.indicateursMaxiEleve[neleve].append(codeIndic)
                                  
                                        else:
                                            if t.phase == _R2: # 2 revues
                                                if tR1 != None and not codeIndic in tR1.indicateursEleve[neleve]: # R1 est passée
                                                    t.indicateursEleve[neleve].append(codeIndic)
                                                   
                                                            
                                            else: # t.phase == _R3
                                                if tR2 != None and not codeIndic in tR2.indicateursEleve[neleve] and not codeIndic in tR1.indicateursEleve[neleve]: # R2 est passée
                                                    t.indicateursEleve[neleve].append(codeIndic)
                                        
                                # Phase de Soutenance    
                                else:
                                    if t.phase == _S:
                                        t.indicateursEleve[neleve].append(codeIndic)
    
                    if neleve == 0:
                        if t.phase in [_R1, "Rev"] or (t.phase == _R2 and self.nbrRevues == 3):
                            ti = []
                            for i in t.indicateursEleve[neleve]:
                                if i in t.indicateursMaxiEleve[neleve]:
                                    ti.append(i)
                            t.indicateursEleve[neleve] = ti
                            if miseAJourPanel and hasattr(t.panelPropriete, 'arbre'):
                                t.panelPropriete.arbre.MiseAJourTypeEnseignement(t.GetReferentiel())
                                t.panelPropriete.MiseAJour()
                            if t.phase == _R1:
                                tR1 = t # la revue 1 est passée !
                            elif t.phase == _R2:
                                tR2 = t # la revue 2 est passée ! (3 revues)
#                print "  >>", t.indicateursMaxiEleve
                
                
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
        self.poids = []
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
            root.set("P"+str(i), str(self.poids[i]))
        return root
    
        if hasattr(self, 'code'):
            if self.code == "":
                self.code = "_"
            root = ET.Element(self.code)
            return root
        
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche CI"
        self.numCI = []
        self.poids = []
        for i in range(len(branche.keys())):
            n = branche.get("C"+str(i), "")
            if n != "":
                self.numCI.append(eval(n))
                self.poids.append(eval(branche.get("P"+str(i), "1")))
        
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
        
        
#        print self.numCI
#        print self.poids
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
    def AddNum(self, num, poids = 1): 
        self.numCI.append(num)
        self.poids.append(poids)
        self.SetNum()
    
        
    ######################################################################################  
    def DelNum(self, num):
        i = self.numCI.index(num)
        self.numCI.remove(num)
        del self.poids[i]
        self.SetNum()
        
    ######################################################################################  
    def SetNum(self, numCI = None, poids = 1):
#        print "SetNum", numCI
        if numCI != None:
            self.numCI = numCI
#            self.poids = poids
            
        if hasattr(self, 'arbre'):
            self.MaJArbre()
        
#        if len(self.numCI) > 0 :
        self.parent.Verrouiller()
        
    ######################################################################################  
    def GetIntit(self, num):
        if self.GetReferentiel().CI_cible:
            lstCI = self.parent.classe.referentiel.CentresInterets
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
            return self.GetReferentiel().abrevCI+str(self.numCI[num]+1)
    
    ######################################################################################  
    def GetPosCible(self, num):
        if self.GetReferentiel().CI_cible:
            return self.parent.classe.referentiel.positions_CI[self.numCI[num]]
        
    
    ######################################################################################  
    def MaJArbre(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.GetCode())
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, getSingulierPluriel(self.GetReferentiel().nomCI, True)+u" :", 
                                        wnd = self.codeBranche, data = self,
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
        self.arbre.SetItemText(self.branche, getSingulierPluriel(self.GetReferentiel().nomCI, True)+u" :")
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
            self.panelParent = panelParent
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
            self.panelPropriete.Destroy()
            self.panelPropriete = PanelPropriete_Competences(self.panelParent, self)
#            self.panelPropriete.construire()
        
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
#        self.num = num
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
        
        # Détection d'un ancienne version (pas infaillible !)
        ancien = False
        for i in range(len(branche.keys())):
            code = branche.get("S"+str(i), "")
            if code != "":
                if not code[0] in ["B", "S", "M", "P"]: # version < 4.6
                    ancien = True
                    break
        
        self.savoirs = []
        for i in range(len(branche.keys())):
            code = branche.get("S"+str(i), "")
            if code != "":
                if ancien: # version < 4.6
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
    def GetTypCode(self, num):
        return self.savoirs[num][0], self.savoirs[num][1:]
    
    
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
    
                  
    def __init__(self, parent, panelParent = None, typeSeance = "", typeParent = 0, branche = None):
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
        self.ordreType = 0
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
        
#        self.nbrGroupes = Variable(u"Nombre de groupes", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
#                              bornes = [1,None], modeLog = False,
#                              expression = None, multiple = False)
        
        # Les autres données
        self.typeParent = typeParent
        self.parent = parent
        self.panelParent = panelParent
        
        if branche != None:
            self.setBranche(branche)
        else:
            self.seances = []
            self.SetType(typeSeance)
            self.AjouterListeSystemes(self.GetDocument().systemes)
            
#        self.SetType(typeSeance)
        
        
        #
        # Création du Tip (PopupInfo)
        #
        if self.GetApp() and isinstance(self.GetApp(), FenetreSequence) :
            self.tip = PopupInfo2(self.GetApp(), u"Séance")
            self.tip_type = self.tip.CreerTexte((1,0), flag = wx.ALL)
            self.tip_intitule = self.tip.CreerTexte((2,0))
            self.tip_titrelien, self.tip_ctrllien = self.tip.CreerLien((3,0))
            self.tip_description = self.tip.CreerRichTexte(self, (4,0))
        
        
        
        if panelParent != None:
            self.panelPropriete = PanelPropriete_Seance(panelParent, self)
            self.panelPropriete.AdapterAuType()
        
        
        
        
    
    ######################################################################################  
    def __repr__(self):
        t = self.code 
#        t += " " +str(self.GetDuree()) + "h"
#        t += " " +str(self.effectif)
#        for s in self.seances:
#            t += "  " + s.__repr__()
        return t
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    
    
    ######################################################################################  
    def EstSousSeance(self):
        return not isinstance(self.parent, Sequence)
    
    
    ######################################################################################  
    def GetListeTypes(self):
        """ Renvoie la liste des types de séance compatibles
        """
        ref = self.GetReferentiel()
        if self.EstSousSeance():
            listType = ref.listeTypeActivite
            if not self.parent.EstSousSeance():
                listType = ref.listeTypeActivite +  ["S", "R"]
        else:
            listType = ref.listeTypeSeance
        
        return listType
    
    
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
            for sce in self.seances:
                root.append(sce.getBranche())
            root.set("nbrRotations", str(self.nbrRotations.v[0]))
#            root.set("nbrGroupes", str(self.nbrGroupes.v[0]))
            
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
            self.seances = []
            for sce in list(branche):
                seance = Seance(self, self.panelParent)
                self.seances.append(seance)
                seance.setBranche(sce)
            self.duree.v[0] = self.GetDuree()
            if self.typeSeance == "R":
                self.nbrRotations.v[0] = eval(branche.get("nbrRotations", str(len(self.seances))))
#                self.nbrGroupes.v[0] = eval(branche.get("nbrGroupes", str(len(self.Get???))))
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
                    
#            print "lstSys", lstSys
            # Correction d'un bug versions <5.5
            # "manque des systèmes dans les séances lors de l'enregistrement"
            for s in self.GetDocument().systemes:
#                print "nom syst :", s.nom
                if not s.nom in lstSys:
                    lstSys.append(s.nom)
                    lstNSys.append(0)
                    
                
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
            for sce in self.seances:
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
            for se in self.seances:
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
            for sce in self.seances:
                eff += sce.GetEffectif() #self.seances[0].GetEffectif()
#        elif self.typeSeance == "S":
#            for sce in self.seances:
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
                for s in self.seances:
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
#        if self.typeSeance in ["R", "S"] and len(self.seances) > 0:
#            for s in self.seances:
#                s.VerifPb()
        
    ######################################################################################  
    def IsEffectifOk(self):
        """ Teste s'il y a un problème d'effectif pour les séances en rotation ou en parallèle
            0 : pas de problème
            1 : tout le groupe "effectif réduit" n'est pas occupé
            2 : effectif de la séance supperieur à celui du groupe "effectif réduit"
            3 : séances en rotation d'effectifs différents !!
        """
#        print "IsEffectifOk", self, 
        ok = 0 # pas de problème
        if self.typeSeance in ["R", "S"] and len(self.seances) > 0:
#            print self.GetEffectif() ,  self.GetClasse().GetEffectifNorm('G'),
            eff = round(self.GetEffectif(), 4)
            effN = round(self.GetClasse().GetEffectifNorm('G'), 4)
            if eff < effN:
                ok = 1 # Tout le groupe "effectif réduit" n'est pas occupé
            elif eff > effN:
                ok = 2 # Effectif de la séance supperieur à celui du groupe "effectif réduit"    
#            if self.typeSeance == "R":
#                continuer = True
#                eff = self.seances[0].GetEffectif()
#                i = 1
#                while continuer:
#                    if i >= len(self.seances):
#                        continuer = False
#                    else:
#                        if self.seances[i].GetEffectif() != eff:
#                            ok = 3 # séance en rotation d'effectifs différents !!
#                            continuer = False
#                        i += 1
            
        elif self.typeSeance in ["AP", "ED"] and not self.EstSousSeance():
            if self.GetEffectif() < self.GetClasse().GetEffectifNorm('G'):
                ok = 1 # Tout le groupe "effectif réduit" n'est pas occupé
        
#        print "   ", ok
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
    def GetListSousSeancesRot(self, tout = False):
        l = []
        i = 0
        for ss in self.seances:
            for n in range(ss.nombre.v[0]):
                l.append(ss)
#            if not tout :
#                i += ss.nombre.v[0]
#                if i >= self.nbrRotations.v[0]:
#                    break
        if not tout:
            l = l[:self.nbrRotations.v[0]]
        return l
    
    ######################################################################################  
    def GetProfondeur(self):
        if self.typeSeance in ["R", "S"]:
            return 1+max([s.GetProfondeur() for s in self.seances])
        else:
            return 0
    
    
    ######################################################################################  
    def GetNiveau(self):
        if self.EstSousSeance():
            return 1+self.parent.GetNiveau()
        else:
            return 0
        
        
    ######################################################################################  
    def GetDuree(self):
#        print "GetDuree", self.GetListSousSeancesRot()
        duree = 0
        if self.typeSeance == "R":
#            i = 0
#            for ss in self.seances:
#                duree += ss.GetDuree()
#                i += ss.nombre.v[0]
#                if i >= self.nbrRotations.v[0]:
#                    break
                
                
            for ss in self.GetListSousSeancesRot():
#                sce = self.seances[i]
                duree += ss.GetDuree()
#                print "   ", duree
                
#            for sce in self.seances:
#                duree += sce.GetDuree()
        elif self.typeSeance == "S":
            if len(self.seances) > 0:
                duree += self.seances[0].GetDuree()
        elif self.typeSeance in self.GetReferentiel().listeTypeHorsClasse:
            duree = 0
        else:
            duree = self.duree.v[0]
        return duree
                
    ######################################################################################  
    def GetDureeGraph(self):
        if self.typeSeance in self.GetReferentiel().listeTypeHorsClasse:
            return 1
        else:
            return self.GetDuree()
#        d = self.GetDuree(graph = True)
#        if d != 0:
#            return 0.001*log(d*2)+0.001
#        return d
           
    ######################################################################################  
    def GetDureeGraphMini(self):
        duree = 10000
        if self.typeSeance == "R":
            for ss in self.GetListSousSeancesRot():
                duree = min(duree, ss.GetDuree())
#            i = 0
#            for ss in self.seances:
#                duree = min(duree, ss.GetDuree())
#                i += ss.nombre.v[0]
#                if i >= self.nbrRotations.v[0]:
#                    break
                
#            for i in range(self.nbrRotations.v[0]):
#                sce = self.seances[i]
#                duree = min(duree, sce.GetDuree())
        elif self.typeSeance == "S":
            if len(self.seances) > 0:
                duree = min(duree, self.seances[0].GetDuree())
        else:
            duree = min(duree, self.duree.v[0])

        return duree
                
    ######################################################################################  
    def SetDuree(self, duree, recurs = True):
        """ Modifie la durée des Rotation et séances en Parallèle et de tous leurs enfants
            après une modification de durée d'un des enfants
        """
        if recurs and self.EstSousSeance() and self.parent.typeSeance in ["R", "S"]: # séance en rotation (parent = séance "Rotation")
            self.parent.SetDuree(duree, recurs = False)
        
#        return
#        if self.typeSeance in ["R", "S"]:
#            self.duree.v[0] = duree
            
            
        elif self.typeSeance == "S" : # Serie (parallèle)
            self.duree.v[0] = duree
#            for s in self.seances:
#                if s.typeSeance in ["R", "S"]:
#                    s.SetDuree(duree, recurs = False)
#                else:
#                    s.duree.v[0] = duree
#                    s.panelPropriete.MiseAJourDuree()
            self.panelPropriete.MiseAJourDuree()

        
        elif self.typeSeance == "R" : # Rotation
#            for s in self.seances:
#                if s.typeSeance in ["R", "S"]:
#                    s.SetDuree(duree, recurs = False)
#                else:
#                    s.duree.v[0] = duree
#                    s.panelPropriete.MiseAJourDuree()
            self.duree.v[0] = self.GetDuree()
            self.panelPropriete.MiseAJourDuree()

        
    ######################################################################################  
    def SetNombre(self, nombre):
        self.nombre.v[0] = nombre
        if self.EstSousSeance() and self.parent.typeSeance == "R":
            self.parent.reglerNbrRotMaxi()
    
    ######################################################################################  
    def SetTaille(self, nombre):
        self.taille.v[0] = nombre
        
    ######################################################################################  
    def SetNombreRot(self, nombre):
        self.nbrRotations.v[0] = nombre
        self.SetDuree(self.GetDuree())
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.vcNombreRot.mofifierValeursSsEvt()
        
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
            
        if self.typeSeance in ["R","S"] and len(self.seances) == 0: # Rotation ou Serie
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
            l.extend(self.seances)
            for s in self.seances:
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
            for sce in self.seances:
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
        num = str(self.ordreType+1)
        
        if isinstance(self.parent, Seance):
            num = str(self.parent.ordreType+1)+"."+num
            if isinstance(self.parent.parent, Seance):
                num = str(self.parent.parent.ordreType+1)+"."+num

        self.code += num

    
        self.SetCodeBranche()
        
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for sce in self.seances:
                sce.SetCode()

        # Tip
        if hasattr(self, "tip"):
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
            for sce in self.seances:
                sce.ConstruireArbre(arbre, self.branche)
            
        
    ######################################################################################  
    def OrdonnerSeances(self):
        listeTypeSeance = self.GetReferentiel().listeTypeSeance
        dicType = {k:0 for k in listeTypeSeance}
        dicType[''] = 0
        RS = 0
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for i, sce in enumerate(self.seances):
                sce.ordre = i
                if sce.typeSeance in ['R', 'S']:
                    sce.ordreType = RS
                    RS += 1
                else:
                    sce.ordreType = dicType[sce.typeSeance]
                    dicType[sce.typeSeance] += 1
                sce.OrdonnerSeances()
        
        self.SetCode()
    
            
    ######################################################################################  
    def AjouterSeance(self, event = None):
        """ Ajoute une séance é la séance
            !! Uniquement pour les séances de type "Rotation" ou "Serie" !!
        """
        seance = Seance(self, self.panelParent)
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            self.seances.append(seance)
            
        self.OrdonnerSeances()
        seance.ConstruireArbre(self.arbre, self.branche)
        self.arbre.Expand(self.branche)
        
        if self.typeSeance == "R":
            seance.SetDuree(self.seances[0].GetDuree())
            self.SetNombreRot(self.GetNbrSSeancesRotation())
            self.reglerNbrRotMaxi()
        else:
            seance.SetDuree(self.GetDuree())
        
        self.arbre.SelectItem(seance.branche)


    ######################################################################################  
    def SupprimerSeance(self, event = None, item = None):
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            if len(self.seances) > 1: # On en laisse toujours une !!
                seance = self.arbre.GetItemPyData(item)
                self.seances.remove(seance)
                self.arbre.Delete(item)
                self.OrdonnerSeances()
                self.panelPropriete.sendEvent()
            if self.typeSeance == "R":  # Séances en Rotation
                self.reglerNbrRotMaxi()
        return
    
    
    ######################################################################################  
    def reglerNbrRotMaxi(self):
        n = self.GetNbrSSeancesRotation()
#        print "reglerNbrRotMaxi", self, ":", n
        self.nbrRotations.bornes[1] = n
        if self.nbrRotations.v[0] > n:
            self.SetNombreRot(n)
    
    
    ######################################################################################  
    def GetNbrSSeancesRotation(self):
        n = 0
        for s in self.seances:
            n += s.nombre.v[0]
        return n
    
    
    ######################################################################################  
    def SupprimerSousSeances(self):
        self.arbre.DeleteChildren(self.branche)
        return
    
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if self.typeSeance in ["R", "S"]:
            for s in self.seances:
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
            for s in self.seances:
                s.MiseAJourNomsSystemes()
        
    ######################################################################################  
    def SupprimerSysteme(self, i):
        if self.typeSeance in ["AP", "ED", "P"]:
            del self.systemes[i]
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.SupprimerSysteme(i)

        
        
    ######################################################################################  
    def AjouterSysteme(self, nom = "", nombre = 0, construire = True):
        if self.typeSeance in ["AP", "ED", "P"]:
            self.systemes.append(Variable(nom, lstVal = nombre, nomNorm = "", typ = VAR_ENTIER_POS, 
                                          bornes = [0,9], modeLog = False,
                                          expression = None, multiple = False))
            if construire and hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
                
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.AjouterSysteme(nom, nombre)
    
    
    ######################################################################################  
    def AjouterListeSystemes(self, lstSys, lstNSys = None):
#        print "  AjouterListeSystemes", self.typeSeance
        if self.typeSeance in ["AP", "ED", "P"]:
            if lstNSys == None:
                lstNSys = [0]*len(lstSys)
            for i, s in enumerate(lstSys):
#                print "    ", s
                self.AjouterSysteme(s, lstNSys[i], construire = False)
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
            
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.AjouterListeSystemes(lstSys, lstNSys) 
                
                
    ######################################################################################  
    def GetDocument(self):    
        if self.EstSousSeance():
            sequence = self.parent.GetDocument()
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
            listItems = [[u"Supprimer", 
                          functools.partial(self.parent.SupprimerSeance, item = itemArbre), 
                          images.Icone_suppr_seance.GetBitmap()],
                         [u"Créer un lien", 
                          self.CreerLien, 
                          None]]
            
            if self.typeSeance in ["R", "S"]:
                listItems.append([u"Ajouter une séance", 
                                  self.AjouterSeance, 
                                  images.Icone_ajout_seance.GetBitmap()])
            
            listItems.append([u"Copier", 
                              self.CopyToClipBoard, 
                              wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, (20,20))])
            
            ################
            try:
                elementCopie = ET.fromstring(pyperclip.paste())
            except:
                elementCopie = None
                
            if elementCopie != None: # Le presse papier n'est pas vide
                if isinstance(elementCopie, Element): # Le presse contient un Element
                    if elementCopie.tag[:6] == 'Seance': # Le presse contient une tache
                        dataSource = Seance(self.parent)
                        dataSource.setBranche(elementCopie)
                        
                        if not hasattr(self, 'GetNiveau') or self.GetNiveau() + dataSource.GetProfondeur() > 2:
                            return
                        
                        if self.typeSeance in ["R", "S"] : # la phase est la même
                            t = u"Coller dans"
                        else:
                            t = u"Coller après"
                        listItems.append([t, functools.partial(self.parent.CollerElem, 
                                                                                 item = itemArbre, 
                                                                                 bseance = elementCopie),
                                          wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, (20,20))])
                            
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
                
                for seance in self.seances:
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
#                l = rotation.seances
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
                ls = self.seances
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
#        print "__init__ tâche", phaseTache
        
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

        # Le code de la tâche (affiché dans l'arbre et sur la fiche
        self.code = u""
        
        # La description de la tâche
        self.description = None

        # Les autres données
        self.projet = projet
        self.panelParent = panelParent
        
        self.phase = phaseTache
        
        
#        
        if branche != None:
            self.setBranche(branche)
##            if not Ok:
##                self.code = -err # Pour renvoyer une éventuelle erreur à l'ouverture d'un fichier
        else:
#        if branche == None:
            self.indicateursEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []} # clef = n°eleve ;  valeur = liste d'indicateurs
            if phaseTache in TOUTES_REVUES_SOUT:
                self.indicateursMaxiEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
            
        if panelParent:
            self.panelPropriete = PanelPropriete_Tache(panelParent, self)
        else:
            print "pas panelParent", self
            
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeEleves()
            self.panelPropriete.MiseAJourDuree()
            self.panelPropriete.MiseAJour()
            
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
            
            
            if self.phase in TOUTES_REVUES_SOUT:
                p = self.tip.CreerTexte((1,0), txt = u"Délai (depuis début du projet) :", flag = wx.ALIGN_RIGHT|wx.ALL)
                p.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline = True))
        
                self.tip_delai = self.tip.CreerTexte((1,1), flag = wx.ALIGN_LEFT|wx.BOTTOM|wx.TOP|wx.LEFT)
                self.tip_delai.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
            else:
                p = self.tip.CreerTexte((1,0), txt = u"Phase :", flag = wx.ALIGN_RIGHT|wx.ALL)
                p.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline = True))
                
                self.tip_phase = self.tip.CreerTexte((1,1), flag = wx.ALIGN_LEFT|wx.BOTTOM|wx.TOP|wx.LEFT)
                self.tip_phase.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
            
            if not self.phase in TOUTES_REVUES_EVAL_SOUT:
                i = self.tip.CreerTexte((2,0), txt = u"Intitulé :", flag = wx.ALIGN_RIGHT|wx.ALL)
                i.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline = True))

                self.tip_intitule = self.tip.CreerTexte((2,1), flag = wx.ALIGN_LEFT|wx.BOTTOM|wx.TOP|wx.LEFT)
                self.tip_intitule.SetFont(wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
                
            self.tip_description = self.tip.CreerRichTexte(self, (3,0), (1,2))
                
                
                
        
    def __eq__(self, tache):
        if tache == None:
            return False
        return self.code == tache.code and self.ordre == tache.ordre
  
    
    ######################################################################################  
    def __repr__(self):
#        t = self.phase + str(self.ordre+1) 
#        t += " " +str(self.GetDuree()) + "h"
#        t += " " +str(self.effectif)
#        for s in self.seances:
#            t += "  " + s.__repr__()
        return self.code +" ("+str(self.ordre)+")"
    
    
    ######################################################################################  
    def GetApp(self):
        return self.projet.GetApp()

    ######################################################################################  
    def ActualiserDicIndicateurs(self):
        """ Complète le dict des compétences/indicateurs globaux (tous les élèves confondus)
        """
#        print "ActualiserDicIndicateurs", self
        for i in range(len(self.projet.eleves)):
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
        tousIndicateurs = self.GetProjetRef()._dicIndicateurs_simple
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
                indicateurs[competence] = [False]*len(self.GetProjetRef()._dicIndicateurs_simple[competence])
            
            indicateurs[competence][indicateur] = True
#        print "  >>", indicateurs
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
        
        
#    ######################################################################################  
#    def initIndicateurs(self):
#        # Les indicateurs séléctionnés ou bien les poids des indicateurs 
#        #     clef = code compétence
#        #     Pour la SSI :  valeur = poids
#        #     Pour la STI2D : valeur = liste d'index
#        typeEns = self.GetTypeEnseignement()
#        if False:#typeEns == "SSI":
#            indicateurs = REFERENTIELS[typeEns]._dicCompetences_prj_simple
#            self.indicateursEleve[0] = dict(zip(indicateurs.keys(), [x[1] for x in indicateurs.values()]))
#        else:
#            indicateurs = REFERENTIELS[typeEns].dicIndicateurs
#            self.indicateursEleve[0] = {}
#            for k, dic in indicateurs.items():
#                ndict = dict(zip(dic[1].keys(), [[]]*len(dic[1])))
#                for c in ndict.keys():
#                    ndict[c] = [True]*len(indicateurs[k][1][c])
#                self.indicateursEleve[0].update(ndict)
            
            
        
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
                lstR = [_R1]
            else:
                lstR = [_R1, _R2]
                    
            if self.phase in lstR:
                for e, indicateurs in self.indicateursEleve.items()[1:]:
                    if e > len(self.projet.eleves):
                        break
                    brancheE = ET.Element("Eleve"+str(e))
                    brancheCmp.append(brancheE)
                    for i, c in enumerate(indicateurs):
                        brancheE.set("Indic"+str(i), c)        
            elif not self.phase in TOUTES_REVUES_EVAL:
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
   
        err = []
        
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
        
        if not self.phase in TOUTES_REVUES_EVAL_SOUT:
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        else:
            self.duree.v[0] = 0.5
        
        brancheElv = branche.find("Eleves")
        self.eleves = []
        for i, e in enumerate(brancheElv.keys()):
            self.eleves.append(eval(brancheElv.get("Eleve"+str(i))))
        
        self.indicateursEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
        
        if self.GetClasse().GetVersionNum() < 5:
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
                    err.append(constantes.Erreur(constantes.ERR_PRJ_T_VERSION))
                    
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
                                lst = [True]*len(self.GetProjetRef()._dicIndicateurs[e])
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
                            lstR = [_R1]
                        else:
                            lstR = [_R1, _R2]

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
                                            if not code in self.GetProjetRef()._dicIndicateurs_simple:
                                                print "Erreur 1", code, "<>", self.GetProjetRef()._dicIndicateurs_simple
                                                err.append(constantes.Erreur(constantes.ERR_PRJ_T_TYPENS))
                                                return err
                                            
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
                                        if not code in self.GetProjetRef()._dicIndicateurs:
                                            print "Erreur 2"
                                            err.append(constantes.Erreur(constantes.ERR_PRJ_T_TYPENS))
                                            return err
    
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
                                if self.phase == 'XXX' and self.GetProjetRef().getTypeIndicateur(codeindic) == 'C':
                                    continue
                                
                                    
#                                try:
#                                    print "******",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                                # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                                if not code in self.GetProjetRef()._dicIndicateurs_simple.keys():
                                    print "Erreur 3", code, "<>", self.GetProjetRef()._dicIndicateurs_simple.keys()
                                    if not constantes.Erreur(constantes.ERR_PRJ_T_TYPENS) in err:
                                        err.append(constantes.Erreur(constantes.ERR_PRJ_T_TYPENS))
                                else:
                                    self.indicateursEleve[0].append(codeindic)
#                                except:
#                                    pass
                        
                    
#        print self.indicateursEleve
        
        self.ActualiserDicIndicateurs()
            
        self.intituleDansDeroul = eval(branche.get("IntituleDansDeroul", "True"))

        return err
    
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
            if self.phase in TOUTES_REVUES_EVAL:
                de = []
                for e in self.projet.eleves:
                    de.append(e.GetDuree(phase = self.phase, total = True))
                if not de:
                    d = 0
                else:
                    d = max(de)
                return d
            
            elif self.phase in ["Rev"]:
                de = []
                for e in self.projet.eleves:
                    de.append(e.GetDureeJusqua(self))
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
    def GetProchaineRevue(self):
#        print "GetProchaineRevue"
        posRevues = self.GetProjetRef().posRevues[self.projet.nbrRevues]
#        print "   posRevues:", posRevues
        for i, pr in enumerate(posRevues):#.reverse():
#            print "   ", i, pr, self.phase
            if self.phase <= pr:
#                print '    >> R'+str(i+1)
                return i+1
        return 0
            
            
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
        
        if self.phase != "":
            if self.phase in TOUTES_REVUES_EVAL_SOUT:
                self.code = self.phase
            else:
                self.code = self.GetProjetRef().phases[self.phase][2]+num     #constantes.CODE_PHASE_TACHE[typeEns][self.phase]+num
        else:
            self.code = num

        
        #
        # Branche de l'arbre
        #
        if hasattr(self, 'codeBranche') and self.phase != "":
            if self.phase in TOUTES_REVUES_EVAL_SOUT:
                self.codeBranche.SetLabel(u"")
                t = u""
            else:
                self.codeBranche.SetLabel(self.code)
                t = u" :"
            self.arbre.SetItemText(self.branche, self.GetProjetRef().phases[self.phase][1]+t)
        
        #
        # Tip (fenêtre popup)
        #
        if self.phase in TOUTES_REVUES_SOUT:
            self.tip.SetTitre(self.GetProjetRef().phases[self.phase][1])
            self.tip.SetTexte(draw_cairo.getHoraireTxt(self.GetDelai()), self.tip_delai)

        else:
            self.tip.SetTitre(u"Tâche "+ self.code)
            if self.phase != "":
                    t = self.GetProjetRef().phases[self.phase][1]
            else:
                t = u""
            if hasattr(self, "tip_phase"):
                self.tip.SetTexte(t, self.tip_phase)


        if not self.phase in TOUTES_REVUES_EVAL_SOUT:
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
            
        if self.phase in TOUTES_REVUES_EVAL:
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
            for s in self.seances:
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
    def GetSuivante(self):
        i = self.projet.taches.index(self)
        if len(self.projet.taches) > i:
            return self.projet.taches[i+1]
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            if not self.phase in TOUTES_REVUES_EVAL_SOUT:
                listItems = [[u"Supprimer", 
                              functools.partial(self.projet.SupprimerTache, item = itemArbre), 
                              images.Icone_suppr_tache.GetBitmap()]]
            else:
                listItems = []
            listItems.append([u"Insérer une revue après", 
                              functools.partial(self.projet.InsererRevue, item = itemArbre), 
                              images.Icone_ajout_revue.GetBitmap()])
#            listItems.append([u"Copier", functools.partial(self.projet.CopierTache, item = itemArbre)])
            listItems.append([u"Copier", 
                              self.CopyToClipBoard, 
                              wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, (20,20))])
 
#            elementCopie = self.GetApp().parent.elementCopie
            try:
                elementCopie = ET.fromstring(pyperclip.paste())
            except:
                elementCopie = None
            
            if elementCopie != None: # Le presse papier n'est pas vide
                if isinstance(elementCopie, Element): # Le presse contient un Element
                    if elementCopie.tag[:5] == 'Tache': # Le presse contient une tache
                        phase = elementCopie.get("Phase", "")
                        if self.phase == phase or self.GetSuivante().phase == phase : # la phase est la même
                            listItems.append([u"Coller après", functools.partial(self.projet.CollerElem, 
                                                                                 item = itemArbre, 
                                                                                 btache = elementCopie),
                                              wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, (20,20))])
                    
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
        self.lienClasse = None
        
        #
        # Création du Tip (PopupInfo)
        #
        self.tip = PopupInfo2(self.parent.app, u"Système ou matériel")
        self.tip_nom = self.tip.CreerTexte((1,0))
        self.tip_nombre, self.tip_ctrllien = self.tip.CreerLien((2,0))
        self.tip_image = self.tip.CreerImage((3,0))
        
        
        if panelParent != None:
            self.panelPropriete = PanelPropriete_Systeme(panelParent, self)
        
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
        
    ######################################################################################  
    def __repr__(self):
        if self.image != None:
            i = img2str(self.image.ConvertToImage())[:20]
        else:
            i = "None"
        return self.nom+" ("+str(self.nbrDispo.v[0])+") " + i
        
        
#    ######################################################################################  
#    def __eq__(self, s):
#        if s == None:
#            return False
#        elif self.nom != s.nom:
#            return False
#        elif self.nbrDispo.v[0] != s.nbrDispo.v[0]:
#            return False
#        elif self.lien != s.lien:
#            return False
#        elif img2str(self.image.ConvertToImage()) != img2str(s.image.ConvertToImage()):
#            return False
#        
#        return True

    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
        root = ET.Element("Systeme")
        if self.lienClasse != None:
            root.set("NomClasse", self.lienClasse.nom)
            
        else:
            root.set("Nom", self.nom)
            self.lien.getBranche(root)
            root.set("Nbr", str(self.nbrDispo.v[0]))
            if self.image != None:
                root.set("Image", img2str(self.image.ConvertToImage()))
        
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche systeme"
        nomClasse  = branche.get("NomClasse", "")
        if nomClasse != u"" and isinstance(self.parent, Sequence):
            classe = self.parent.classe
#            print "   >>", classe
            for s in classe.systemes:
                if s.nom == nomClasse:
                    self.lienClasse = s
                    self.setBranche(s.getBranche())
                    if hasattr(self, 'panelPropriete'):
                        self.panelPropriete.MiseAJour()
                        self.panelPropriete.Verrouiller(False)
                        self.panelPropriete.cbListSys.SetSelection(self.panelPropriete.cbListSys.FindString(self.nom))
                    break
            
                
        else:
            self.nom  = branche.get("Nom", "")
            self.lien.setBranche(branche, self.GetPath())
    
            self.nbrDispo.v[0] = eval(branche.get("Nbr", "1"))
            
            data = branche.get("Image", "")
            if data != "":
                self.image = PyEmbeddedImage(data).GetBitmap()
            else:
                self.image = None
            
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.MiseAJour()


    ######################################################################################  
    def Copie(self, parent, panelParent = None):
        s = Systeme(parent, panelParent)
        s.setBranche(self.getBranche())
        return s
    
    ######################################################################################  
    def propagerChangements(self):
#        print "propagerChangements", self
        if isinstance(self.parent, Classe) and hasattr(self.parent, 'doc'):
            
            if isinstance(self.parent.doc, Sequence):
#                print "   ",self.parent, self.parent.doc
                seq = self.parent.doc
                for s in seq.systemes:
                    if s.lienClasse == self:
                        s.setBranche(self.getBranche())
                        if hasattr(s, 'arbre'):
                            s.SetCode()
                        if hasattr(s, 'panelPropriete'):
                            s.panelPropriete.MiseAJourListeSys(self.nom)
        
    ######################################################################################  
    def SetNombre(self):
        if isinstance(self.parent, Sequence):
            self.parent.VerifPb()
            
        else:
            self.propagerChangements()
                
            
    ######################################################################################  
    def SetNom(self, nom):
        self.nom = nom
        
        self.propagerChangements()
        
                        
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
        self.propagerChangements()
        

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
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", 
                                                     functools.partial(self.parent.SupprimerSysteme, item = itemArbre),
                                                     images.Icone_suppr_systeme.GetBitmap()],
                                                    [u"Créer un lien", self.CreerLien, None]])
            
            
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
            try :
                self.image = PyEmbeddedImage(data).GetBitmap()
            except:
                self.image = None
                Ok = False
            
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
            self.parent.app.AfficherMenuContextuel([[u"Créer un lien", self.CreerLien, None]])
            
            
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
            try:
                self.avatar = PyEmbeddedImage(data).GetBitmap()
            except:
                Ok = False
                self.avatar = None
            
        if hasattr(self, 'referent'):   # prof
            self.referent = eval(branche.get("Referent", "False"))
            
        if hasattr(self, 'discipline'): # prof
            self.discipline = branche.get("Discipline", 'Tec')
            
        if hasattr(self, 'grille'):     # élève
#            print self.grille
            for k in self.GetProjetRef().parties.keys():
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
        for k in projet.GetProjetRef().parties.keys():
            self.grille[k] = Lien(typ = 'f')
        
        Personne.__init__(self, projet, panelParent, ident)
 
        
        
    def GetFicheHTML(self):
        cr = constantes.GetCouleurHTML(COUL_PARTIE['C'])
        cs = constantes.GetCouleurHTML(COUL_PARTIE['S'])
        return BASE_FICHE_HTML %(cr,cs)

            
    ######################################################################################  
    def GetDuree(self, phase = None, total = False):
        d = 0
        p = 0
        if not total and phase != None:
            for i, t in enumerate(self.projet.taches):
                if t.phase == phase:
                    break
                if t.phase in TOUTES_REVUES_EVAL_SOUT:
                    p = i
        
        for t in self.projet.taches[p:]:
            if t.phase == phase:
                break
            if not t.phase in TOUTES_REVUES_SOUT:
                if self.id in t.eleves:
                    d += t.GetDuree()
        return d
        
    ######################################################################################  
    def GetDureeJusqua(self, tache, depuis = None):
        d = 0
        p = 0
        if depuis != None:
            for i, t in enumerate(self.projet.taches):
                if t == depuis:
                    break
                p = i
        
        for t in self.projet.taches[p:]:
            if t == tache:
                break
            if not t.phase in TOUTES_REVUES_SOUT:
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
        return getNomFichier(prefixe, self.GetNomPrenom()+"_"+self.projet.intitule[:20])
#
#        for c in [u"\t", u"\n", "\"", "/", "\\", "?", "<", ">", "|", ":", "."]:
#            nomFichier = nomFichier.replace(c, "_")
#        return nomFichier


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
#        print "GetNomGrilles"
        prj = self.projet.GetProjetRef()
#        print prj
#        print prj.grilles
        #
        # Création des noms des fichiers grilles
        #
        # Par défaut = chemin du fichier .prj
        if path == None:
            path = os.path.dirname(self.projet.GetApp().fichierCourant)
            
        nomFichiers = {} 
        for part, g in prj.parties.items():
            prefixe = "Grille_"+g
            gr = prj.grilles[part]
#            print gr
            if grilles.EXT_EXCEL != None:
#                extention = os.path.splitext(ref.grilles_prj[k][0])[1]
                extention = grilles.EXT_EXCEL
                
                if gr[1] == 'C': # fichier "Collectif"
                    nomFichiers[part] = os.path.join(path, self.projet.getNomFichierDefaut(prefixe)) + extention
                else:
                    nomFichiers[part] = os.path.join(path, self.getNomFichierDefaut(prefixe)) + extention
#        print "   >", nomFichiers
        return nomFichiers


    ######################################################################################  
    def GenererGrille(self, event = None, path = None, nomFichiers = None, messageFin = True):
        print "GenererGrille élève", self
#        print "  ", nomFichiers
        if nomFichiers == None:
            nomFichiers = self.GetNomGrilles(path)
            if not self.projet.TesterExistanceGrilles({0:nomFichiers}):
                return
        print "  Fichiers :", nomFichiers
        
        prj = self.projet.GetProjetRef()
        
        #
        # Ouverture (et pré-sauvegarde) des fichiers grilles "source" (tableaux Excel)
        #
        tableaux = {}
        for k, f in nomFichiers.items():
#            if os.path.isfile(f):
#                tableaux[k] = grilles.getTableau(self.projet.GetApp(), f)
#            else:
            tableaux[k] = grilles.getTableau(self.projet.GetApp(),
                                             prj.grilles[k][0])
            if tableaux[k] != None: # and tableaux[k].filename !=f:
#                print "      créé :", f
#                tableaux[k].save(f)
                try:
                    tableaux[k].save(f)
                except:
                    messageErreur(self.projet.GetApp(), u"Erreur !",
                                  u"Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
                                  u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
                                  u" - que le dossier choisi n'est pas protégé en écriture"%f)

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
        prj = self.GetProjetRef()
#        dicPoids = self.GetReferentiel().dicPoidsIndicateurs_prj
        dicIndicateurs = self.GetDicIndicateurs()
#        print "dicIndicateurs", dicIndicateurs
        tousIndicateurs = prj._dicIndicateurs
#        lstGrpIndicateur = {'R' : prj._lstGrpIndicateur['R'],
#                            'S' : self.GetProjetRef()._lstGrpIndicateur['S']}
#        print lstGrpIndicateur
        
#        r, s = 0, 0
#        ler, les = {}, {}
        
#        rs = [0, 0]
#        lers = [{}, {}]
        
        rs = {}
        lers = {}
        for ph in prj._lstGrpIndicateur.keys():
            lers[ph] = {}
            rs[ph] = 0
    
        def getPoids(listIndic, comp, poidsGrp):
            """ 
            """
#            print "getPoids", listIndic, comp, poidsGrp
            for ph in prj._lstGrpIndicateur.keys():
                if grp in prj._lstGrpIndicateur[ph]:
                    for i, indic in enumerate(listIndic):
                        if comp in dicIndicateurs.keys():
                            if dicIndicateurs[comp][i]:
#                                print "  comp", grp, comp, i, indic.poids, ph
                                poids = indic.poids
                                if ph in poids.keys():
                                    p = 1.0*poids[ph]/100
                                    rs[ph] += p * poidsGrp[ph]/100
                                    if grp in lers[ph].keys():
                                        lers[ph][grp] += p
                                    else:
                                        lers[ph][grp] = p
                        else:
                            if not grp in lers[ph].keys():
                                lers[ph][grp] = 0
                            
            return
        
        
        for grp, grpComp in tousIndicateurs.items():
            if len(grpComp) > 2 :
                titre, dicComp, poidsGrp = grpComp
            else:
                titre, dicComp = grpComp
                poidsGrp = 1
#            print "    ", grp, poidsGrp
            
            if type(dicComp) == list:                       # 1 niveau
                getPoids(dicComp, grp, poidsGrp)
            else:
                for comp, lstIndic in dicComp.items():
#                    print "      ", comp
                    if type(lstIndic[1]) == list:           # 2 niveaux
                        getPoids(lstIndic[1], comp, poidsGrp)    
                    else:                                   # 3 niveaux
                        for scomp, lstIndic2 in lstIndic.items():
                            getPoids(lstIndic2[1], scomp, poidsGrp)
                                
                                                               
#        r, s = rs
#        ler, les = lers
#        print "   eval :", rs, lers
         
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
        for t in prj._lstGrpIndicateur.keys():
#            if t in classeurs:
#            print "aColNon", self.GetReferentiel().aColNon
            if t in self.GetReferentiel().aColNon.keys() and self.GetReferentiel().aColNon[t]:
                seuil[t] = 0.5  # s'il y a une colonne "non", le seuil d'évaluabilité est de 50% par groupe de compétence
            else:
                seuil[t] = 1.0     # s'il n'y a pas de colonne "non", le seuil d'évaluabilité est de 100% par groupe de compétence
        
        ev = {}
        ev_tot = {}
#        for txt, le, ph in zip([r, s], [ler, les], prj._lstGrpIndicateur.keys()):
        for part in prj._lstGrpIndicateur.keys():
            txt = rs[part]
            txt = round(txt, 6)
            ev[part] = {}
            ev_tot[part] = [txt, True]
            for grp, tx in lers[part].items():
                tx = round(tx, 6)
                ev[part][grp] = [tx, tx >= seuil[part]]
                ev_tot[part][1] = ev_tot[part][1] and ev[part][grp][1]
        
#        print "   ", ev, ev_tot, seuil
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
            if not t.phase in TOUTES_REVUES_SOUT:
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
            if revues and t.phase in TOUTES_REVUES_EVAL:
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
            b = b and len(g.path) > 0
        return b
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            listItems = [[u"Supprimer", 
                          functools.partial(self.projet.SupprimerEleve, item = itemArbre), 
                          images.Icone_suppr_eleve.GetBitmap()]]
            if len(self.GetProjetRef().parties) > 0:
                tg = u"Générer grille"
                to = u"Ouvrir grille"
                if len(self.GetProjetRef().parties) > 1:
                    tg += u"s"
                    to += u"s"
                
                if self.GrillesGenerees():
                    listItems.append([to, functools.partial(self.OuvrirGrilles), None])
            listItems.append([tg, functools.partial(self.GenererGrille), None])    
            
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
        for k in self.GetProjetRef().parties.keys():
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
        
        for part in self.GetProjetRef()._lstGrpIndicateur.keys():
            self.evalu[part].SetLabel(rallonge(pourCent2(ev_tot[part][0])))
            
#        labr = rallonge(pourCent2(ev_tot['R'][0]))
#        labs = rallonge(pourCent2(ev_tot['S'][0]))
#        self.evaluR.SetLabel(labr)
#        self.evaluS.SetLabel(labs)
        
        keys = sorted(self.GetProjetRef()._dicIndicateurs_simple.keys())
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
        
#        for ph, nomph, st in zip(['R', 'S'], [u"conduite", u"soutenance"], [self.evaluR, self.evaluS]):
        for ph, nomph in self.GetProjetRef().parties.items():
            st = self.evalu[ph]
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
            
            keys = sorted(self.GetProjetRef()._dicIndicateurs.keys())
#            if "O8s" in keys:
#                keys.remove("O8s")
            lab = {}
            for part in self.GetProjetRef()._lstGrpIndicateur.keys():
                lab[part] = [[pourCent2(ev_tot[part][0], True), True]]
    #            totalOk = True
                for k in keys:
                    if k in self.GetProjetRef()._lstGrpIndicateur[part]:
                        if k in ev[part].keys():
                            
    #                        totalOk = totalOk and (ler[k] >= 0.5)
                            lab[part].append([pourCent2(ev[part][k][0], True), ev[part][k][1]]) 
                        else:
    #                        totalOk = False
                            lab[part].append([pourCent2(0, True), False]) 
                    else:
                        lab[part].append(["", True])
                lab[part][0][1] = ev_tot[part][1]#totalOk and (er >= 0.5)
            
            
#            labr = [[pourCent2(ev_tot['R'][0], True), True]]
##            totalOk = True
#            for k in keys:
#                if k in self.GetProjetRef()._lstGrpIndicateur['R']:
#                    if k in ev['R'].keys():
#                        
##                        totalOk = totalOk and (ler[k] >= 0.5)
#                        labr.append([pourCent2(ev['R'][k][0], True), ev['R'][k][1]]) 
#                    else:
##                        totalOk = False
#                        labr.append([pourCent2(0, True), False]) 
#                else:
#                    labr.append(["", True])
#            labr[0][1] = ev_tot['R'][1]#totalOk and (er >= 0.5)
#                    
#                    
#                    
#            labs = [[pourCent2(ev_tot['S'][0], True), True]]
##            totalOk = True
#            for k in keys:
#                if k in self.GetProjetRef()._lstGrpIndicateur['S']:
#                    if k in ev['S'].keys():
##                        totalOk = totalOk and (ev['S'][k] >= 1)
#                        labs.append([pourCent2(ev['S'][k][0], True), ev['S'][k][1]]) 
#                    else:
##                        totalOk = False
#                        labs.append([pourCent2(0, True), False]) 
#                else:
#                    labs.append(["", True])
#            labs[0][1] = ev_tot['S'][1]#totalOk and (es >= 1)
 
            for part in self.GetProjetRef()._lstGrpIndicateur.keys():
                for i, lo in enumerate(lab[part]):
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
                    XML_AjouterCol(self.ficheXML, "le"+part, l, coul, constantes.GetCouleurHTML(COUL_PARTIE[part]), size, bold)
                
#            for i, lo in enumerate(labr):
#                l, o = lo
#                if i == 0:
#                    size = None
#                    bold = True
#                    if o:
#                        coul = coulOK
#                    else:
#                        coul = coulNON
#                else:
#                    size = 2
#                    bold = False
#                    if not o:
#                        coul = coulNON
#                    else:
#                        coul = None
#                XML_AjouterCol(self.ficheXML, "ler", l, coul, constantes.GetCouleurHTML(COUL_PARTIE['C']), size, bold)
#                
##                SetWholeText(self.ficheXML, "r"+str(i), l)
#                
#                
#            for i, lo in enumerate(labs):
#                l, o = lo
#                if i ==0:
#                    size = None
#                    bold = True
#                    if o:
#                        coul = coulOK
#                    else:
#                        coul = coulNON
#                else:
#                    size = 2
#                    bold = False
#                    if not o:
#                        coul = coulNON
#                    else:
#                        coul = None
#                XML_AjouterCol(self.ficheXML, "les", l, coul, constantes.GetCouleurHTML(COUL_PARTIE['S']), size, bold)
##                SetWholeText(self.ficheXML, "s"+str(i), l)
                
                
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
        sz.Add(self.codeDuree)
        
        self.evalu = {}
        for part in self.GetProjetRef()._lstGrpIndicateur.keys():
            self.evalu[part] = wx.StaticText(self.codeBranche, -1, "")
            sz.Add(self.evalu[part])
            
#        self.evaluR = wx.StaticText(self.codeBranche, -1, "")
#        self.evaluS = wx.StaticText(self.codeBranche, -1, "")
#        
#        sz.Add(self.evaluR)
#        sz.Add(self.evaluS)
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
            self.projet.app.AfficherMenuContextuel([[u"Supprimer", 
                                                     functools.partial(self.projet.SupprimerProf, item = itemArbre), 
                                                     images.Icone_suppr_prof.GetBitmap()]])
        
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
#        print "afficher", panel
        if self.panel != None:
            self.bsizer.Detach(self.panel)
            self.panel.Hide()
        
        self.panel = panel
        self.bsizer.Add(self.panel, 1, flag = wx.EXPAND|wx.GROW)
        self.panel.Show()
        self.bsizer.Layout()
#        self.panel.Refresh()
#        self.Refresh()


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
        
        
        
        
        
        #############################################################################################
        # Quelques variables ...
        #############################################################################################
        self.fichierClasse = r""
        self.pleinEcran = False
        # Element placé dans le "presse papier"
        self.elementCopie = None
        
        
        
        
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
        self.Bind(wx.EVT_MENU_RANGE, self.OnFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9)
        
        if sys.platform == "win32":
            self.Bind(wx.EVT_MENU, self.genererGrilles, id=17)
            self.Bind(wx.EVT_MENU, self.genererGrillesPdf, id=20)
            
        self.Bind(wx.EVT_MENU, self.genererFicheValidation, id=19)
        
        if sys.platform == "win32":
            self.Bind(wx.EVT_MENU, self.etablirBilan, id=18)
            
        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)
        
        self.Bind(wx.EVT_MENU, self.OnAide, id=21)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=22)
        
#        self.Bind(wx.EVT_MENU, self.OnOptions, id=31)
        
        if sys.platform == "win32" :
            self.Bind(wx.EVT_MENU, self.OnRegister, id=32)
        
        self.Bind(wx.EVT_MENU, self.OnReparer, id=33)
        
        self.Bind(EVT_APPEL_OUVRIR, self.OnAppelOuvrir)
        
        
        
        # Interception des frappes clavier
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        
        # Interception de la demande de fermeture
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
        #############################################################################################
        # Création de la barre d'outils
        #############################################################################################
        self.ConstruireTb()
        
        
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
        print options
        
        # On applique les options ...
        self.DefinirOptions(options)
        
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
    
        
        
        
        
        # Récupération de la dernière version
        a = threading.Thread(None, self.GetNewVersion, None) 
        a.start()


#        wx.CallAfter(self.GetNewVersion)
        
        
        self.Thaw()
        
    ###############################################################################################
    def GetNewVersion(self):  
        # url = 'https://code.google.com/p/pysequence/downloads/list'
        print "Recherche nouvelle version ..."
        url = 'https://github.com/cedrick-f/pySequence/releases'
        try:
            self.downloadPage = BeautifulSoup(urllib2.urlopen(url, timeout = 5))
        except IOError:
            print "pas d'accès Internet"
            return
        
        # Dernière version
        div_latest = self.downloadPage.find_all('div', attrs={'class':"release label-latest"})
        try:
            latest = div_latest[0].contents[1].find_all('span', attrs={'class':"css-truncate-target"})[0].contents[0]
        except:
            print "aucune"
            return
        latest = latest.lstrip('v')
        
        # Version actuelle
        a = __version__.split('.')
        
        # Comparaison
        new = True
        for i, l in enumerate(latest.split('.')):
            nl = int(l.rstrip("-beta"))
            na = int(a[i].rstrip("-beta"))
            if nl < na:
                new = False
                break
        if new:
            print latest
        else:
            print

        if new:
            dialog = wx.MessageDialog(self, u"Une nouvelle version de pySéquence est disponible\n\n" \
                                            u"\t%s\n\n" \
                                            u"Voulez-vous visiter la page de téléchargement ?" % latest, 
                                          u"Nouvelle version", wx.YES_NO | wx.ICON_INFORMATION)
            retCode = dialog.ShowModal()
            if retCode == wx.ID_YES:
                try:
                    webbrowser.open(url,new=2)
                except:
                    messageErreur(None, u"Ouverture impossible",
                                  u"Impossible d'ouvrir l'url\n\n%s\n" %toDefautEncoding(self.path))


        return
        
                    
                    
#    ###############################################################################################
#    def GetNewVersionOld(self):  
#        # url = 'https://code.google.com/p/pysequence/downloads/list'
#        print "Recherche nouvelle version ...",
#        url = 'https://drive.google.com/folderview?id=0B2jxnxsuUscPX0tFLVN0cF91TGc#list'
#        try:
#            self.downloadPage = BeautifulSoup(urllib2.urlopen(url, timeout = 5))
#        except IOError:
#            print "pas d'accès Internet"
#            return   
#
##        ligne = self.downloadPage.find('div', attrs={'class':"flip-entry-title"})
#        ligne = self.downloadPage.find_all('div', attrs={'class':"flip-entry-title"})
##        fichier = ligne.text.strip()
#        
#        # Version actuelle
#        vba = __version__.split("beta")
#        va = vba[0]
#        if len(vba) > 1:
#            ba = eval(vba[1])
#        else:
#            ba = 100
#        
##        print vba, va, ba
#        # version en ligne plus récente
#        versionPlusRecente = False    
#                    
#        for l in ligne:
#            if len(l.text.split('_')) > 1:
#                v = l.text.split('_')[1].split('.zip')[0]
#                vb = v.split("beta")
#                vn = vb[0]
#                if len(vb) >1:
#                    bn = eval(vb[1])
#                else:
#                    bn = 100
##                print vb, vn, bn
#                if vn > va or (vn == va and bn > ba): # Nouvelle version disponible
#                    versionPlusRecente = True
#                    break
##        print v
#        
#        if versionPlusRecente:
#            dialog = wx.MessageDialog(self, u"Une nouvelle version de pySéquence est disponible\n\n" \
#                                            u"\t%s\n\n" \
#                                            u"Voulez-vous visiter la page de téléchargement ?" % v, 
#                                          u"Nouvelle version", wx.YES_NO | wx.ICON_INFORMATION)
#            retCode = dialog.ShowModal()
#            if retCode == wx.ID_YES:
#                try:
#                    webbrowser.open(url,new=2)
#                except:
#                    messageErreur(None, u"Ouverture impossible",
#                                  u"Impossible d'ouvrir l'url\n\n%s\n" %toDefautEncoding(self.path))

                    
                
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
        if self.GetNotebook().GetCurrentPage() == None:
            return
        
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
        
        submenu = wx.Menu()
        file_menu.AppendMenu(14, u"&Ouvrir un fichier récent", submenu)
        self.filehistory = wx.FileHistory()
        self.filehistory.UseMenu(submenu)
        
        file_menu.Append(12, u"&Enregistrer\tCtrl+S")
        file_menu.Append(13, u"&Enregistrer sous ...")
        file_menu.AppendSeparator()
        
#        file_menu.AppendSeparator()
        file_menu.Append(15, u"&Exporter la fiche (PDF ou SVG)\tCtrl+E")
        file_menu.Append(16, u"&Exporter les détails\tCtrl+D")
        
        if sys.platform == "win32":
            file_menu.Append(17, u"&Générer les grilles d'évaluation projet\tCtrl+G")
            file_menu.Append(20, u"&Générer les grilles d'évaluation projet en PDF\tCtrl+P")
        
        file_menu.Append(19, u"&Générer le dossier de validation projet\tAlt+V")
        
        if sys.platform == "win32":
            file_menu.Append(18, u"&Générer une Synthèse pédagogique\tCtrl+B")
        
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, u"&Quitter\tCtrl+Q")

        self.file_menu = file_menu
        
        tool_menu = wx.Menu()
        
        if sys.platform == "win32" :
    #        tool_menu.Append(31, u"Options")
            self.menuReg = tool_menu.Append(32, u"a")
            self.MiseAJourMenu()
        self.menuRep = tool_menu.Append(33, u"Ouvrir et réparer un fichier")

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
        if hasattr(self, 'menuReg'):
            if register.IsRegistered():
                self.menuReg.SetText(u"Désinscrire de la base de registre")
            else:
                self.menuReg.SetText(u"Inscrire dans la base de registre")
            
            
            
    #############################################################################
    def DefinirOptions(self, options):
        for f in reversed(options.optFichiers["FichiersRecents"]):
            self.filehistory.AddFileToHistory(f)
            
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
    def OnReparer(self, event):
        dlg = wx.MessageDialog(self, u"Ouvrir et réparer un fichier de projet\n\n" \
                               u"L'opération qui va suivre permet d'ouvrir un fichier de projet (.prj)\n" \
                               u"en restaurant les valeurs par défaut du programme d'enseignement.\n" \
                               u"Si le projet utilise un programme d'enseignement personnalisé,\n" \
                               u"les spécificités de ce dernier seront perdues.\n\n"\
                               u"Voulez-vous continuer ?",
                                 u"Ouvrir et réparer",
                                 wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                 )
        res = dlg.ShowModal()
        dlg.Destroy() 
        if res == wx.ID_YES:
            self.commandeOuvrir(reparer = True)
            

         
                
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
            webbrowser.open('https://github.com/cedrick-f/pySequence/wiki',new=2)
        except:
            messageErreur(None, u"Ouverture impossible",
                          u"Impossible d'ouvrir l'url\n\n%s\n" %toDefautEncoding(self.path))

        
        
    ###############################################################################################
    def commandeNouveau(self, event = None, ext = None, ouverture = False):
#        print "commandeNouveau"
        if ext == None:
            dlg = DialogChoixDoc(self)
            val = dlg.ShowModal()
            dlg.Destroy()
            if val == 1:
                ext = 'seq' 
            elif val == 2:
                ext = 'prj'
            else:
                return
                
        if ext == 'seq':
            child = FenetreSequence(self, ouverture)
        elif ext == 'prj':
            child = FenetreProjet(self)
        
        self.OnDocChanged(None)
        if child != None:
            wx.CallAfter(child.Activate)
        return child


    ###############################################################################################
    def ouvrir(self, nomFichier, reparer = False):
        self.Freeze()
        wx.BeginBusyCursor()
        
        if nomFichier != '':
            ext = os.path.splitext(nomFichier)[1].lstrip('.')
            
            # Fichier pas déja ouvert
            if not nomFichier in self.GetNomsFichiers():
                
                child = self.commandeNouveau(ext = ext, ouverture = True)
                if child != None:
                    child.ouvrir(nomFichier, reparer = reparer)
                
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
                    child.ouvrir(nomFichier, reparer = reparer)
            
            if not reparer:
                self.filehistory.AddFileToHistory(nomFichier)
            
        wx.EndBusyCursor()
        self.Thaw()


    ###############################################################################################
    def commandeOuvrir(self, event = None, nomFichier = None, reparer = False):
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
        
        
            
        self.ouvrir(nomFichier, reparer = reparer)
        
        
    ###############################################################################################
    def OnFileHistory(self, evt):
        # get the file based on the menu ID
        fileNum = evt.GetId() - wx.ID_FILE1
        path = self.filehistory.GetHistoryFile(fileNum)
#        print "You selected %s\n" % path

        # add it back to the history so it will be moved up the list
        self.filehistory.AddFileToHistory(path)
        self.commandeOuvrir(nomFichier = path)


    ###############################################################################################
    def GetFichiersRecents(self):
        lst = []
        for n in range(self.filehistory.GetCount()):
            lst.append(self.filehistory.GetHistoryFile(n))
        return lst


    ###############################################################################################
    def OnAppelOuvrir(self, evt):
#        print "OnAppelOuvrir"
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
    def genererGrillesPdf(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.genererGrillesPdf(event)
            
    #############################################################################
    def genererFicheValidation(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.genererFicheValidation(event)
    
    #############################################################################
    def etablirBilan(self, event = None):
        for w in self.GetChildren():
            if isinstance(w, FenetreBilan):
                w.SetFocus()
                return
#        if self.GetFenetreActive() != None:
        if self.GetFenetreActive():
            dossier = self.GetFenetreActive().DossierSauvegarde
        else:
            dossier = constantes.INSTALL_PATH
        win = FenetreBilan(self, dossier)
        win.Show()
#        win.Destroy()
        
        
        
#    #############################################################################
#    def OnOptions(self, event, page = 0):
#        options = self.options.copie()
#        dlg = Options.FenOptions(self, options)
#        dlg.CenterOnScreen()
#        dlg.nb.SetSelection(page)
#
#        # this does not return until the dialog is closed.
#        val = dlg.ShowModal()
#    
#        if val == wx.ID_OK:
#            self.DefinirOptions(options)
#            self.AppliquerOptions()
#            
#        else:
#            pass
#
#        dlg.Destroy()
            
            
            

        
        
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
                self.file_menu.Enable(18, True)
                self.file_menu.Enable(17, True)
                self.file_menu.Enable(19, True)
                self.file_menu.Enable(20, True)
            elif doc.typ == "seq":
                self.file_menu.Enable(18, True)
                self.file_menu.Enable(17, False)
                self.file_menu.Enable(19, False)
                self.file_menu.Enable(20, False)
                
           
        
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
    def GetDocActif(self):
        if self.GetNotebook().GetCurrentPage() != None:
            return self.GetNotebook().GetCurrentPage().GetDocument()
    
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
            
        try:
            self.options.definir()
            self.options.valider(self)
            self.options.enregistrer()
        except IOError:
            print "   Permission d'enregistrer les options refusée...",
        except:
            print "   Erreur enregistrement options...",
        
        
        
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

        self.definirNomFichierCourant('')
    
        sizer = wx.BoxSizer()
        sizer.Add(self.pnl, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Layout()
        
        self.Bind(EVT_DOC_MODIFIED, self.OnDocModified)
        self.Bind(wx.EVT_CLOSE, self.quitter)
        

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
        
        for nom, fct, img in items:
            item = wx.MenuItem(menu, wx.ID_ANY, nom)
            if img != None:
                item.SetBitmap(img)
            item1 = menu.AppendItem(item)    
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
    def exporterFichePDF(self, nomFichier, pourDossierValidation = False):
        try:
            PDFsurface = cairo.PDFSurface(nomFichier, 595, 842)
        except IOError:
            Dialog_ErreurAccesFichier(nomFichier)
            wx.EndBusyCursor()
            return
        
        ctx = cairo.Context(PDFsurface)
        ctx.scale(820, 820) 
        if self.typ == 'seq':
            draw_cairo_seq.Draw(ctx, self.sequence)
        elif self.typ == 'prj':
            draw_cairo_prj.Draw(ctx, self.projet, pourDossierValidation = pourDossierValidation)
        
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
        self.classe = Classe(parent, self.panelProp, ouverture = ouverture, typedoc = self.typ)
        
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
        
        #
        # Bulletins Officiels
        #
        self.pageBO = Panel_BO(self.nb)
        self.nb.AddPage(self.pageBO, u"Bulletins Officiels")
        
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
        self.miseEnPlace()
        
    ###############################################################################################
    def GetDocument(self):
        return self.sequence
        
        
    ###############################################################################################
    def OnPageChanged(self, event):
        new = event.GetSelection()
        event.Skip()
        if new == 1: # On vient de cliquer sur la page "détails"
            self.pageDetails.Remplir(self.fichierCourant, self.sequence, self.typ)
        
        elif new == 2: # On vient de cliquer sur la page "Bulletins Officiels"
            self.pageBO.Construire(REFERENTIELS[self.sequence.classe.typeEnseignement])
            
        elif new == 0: # On vient de cliquer sur la fiche
            self.fiche.Redessiner()
            
    ###############################################################################################
    def OnDocModified(self, event):
#        print "OnDocModified"
        if event.GetDocument() == self.sequence:
            self.sequence.VerifPb()
            wx.CallAfter(self.fiche.Redessiner)
            self.MarquerFichierCourantModifie()
            
        elif event.GetDocument() == self.classe:
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
    def VerifierReparation(self):
        """ Vérification (et correction) de la compatibilité de la séquence avec la classe
            après une ouverture avec réparation
        """
#        print "VerifierReparation", self.sequence.CI.numCI, self.sequence.GetReferentiel().CentresInterets
        for ci in self.sequence.CI.numCI:
            if ci >= len(self.sequence.GetReferentiel().CentresInterets):
                self.sequence.CI.numCI.remove(ci)
                messageErreur(self,u"CI inexistant",
                              u"Pas de CI numéro " + str(ci) + " !\n\n" \
                              u"La séquence ouverte fait référence à un Centre d'Intérêt\n" \
                              u"qui n'existe pas dans le référentiel par défaut.\n\n" \
                              u"Il a été supprimé !")
        return
    
    
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True, reparer = False):
#        print "ouvrir sequence"
        if not os.path.isfile(nomFichier):
            return
        
        fichier = open(nomFichier,'r')
        self.definirNomFichierCourant(nomFichier)
    
        def ouvre():
            root = ET.parse(fichier).getroot()
            
            # La séquence
            sequence = root.find("Sequence")
            if sequence == None: # Ancienne version , forcément STI2D-ETT !!
                if hasattr(self.classe, 'panelPropriete'):
                    self.classe.panelPropriete.EvtRadioBox(CodeFam = ('ET', 'STI'))
                self.sequence.setBranche(root)
            else:
                # La classe
                classe = root.find("Classe")
                self.classe.setBranche(classe, reparer = reparer)
                self.sequence.MiseAJourTypeEnseignement()
                self.sequence.setBranche(sequence)  

            if reparer:
                self.VerifierReparation()
                
            self.arbre.DeleteAllItems()
            root = self.arbre.AddRoot("")
            self.classe.ConstruireArbre(self.arbre, root)
            self.sequence.ConstruireArbre(self.arbre, root)
            self.sequence.CI.SetNum()
            self.sequence.SetCodes()
            self.sequence.PubDescription()
            self.sequence.SetLiens()
            self.sequence.VerifPb()
    
            self.sequence.Verrouiller()
            self.arbre.SelectItem(self.classe.branche)


        if "beta" in __version__:
            ouvre()
        else:
            try:
                ouvre()
            except:
                nomCourt = os.path.splitext(os.path.split(nomFichier)[1])[0]
                messageErreur(self,u"Erreur d'ouverture",
                              u"La séquence pédagogique\n    %s\n n'a pas pu être ouverte !" %nomCourt)
                fichier.close()
                self.Close()
                return

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        
        fichier.close()
        
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
        print "FenetreProjet"
        FenetreDocument.__init__(self, parent)
        
        self.Freeze()
        
        #
        # La classe
        #
        self.classe = Classe(parent, self.panelProp, pourProjet = True, typedoc = self.typ)
        
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
        
        #
        # Bulletins Officiels
        #
        self.pageBO = Panel_BO(self.nb)
        self.nb.AddPage(self.pageBO, u"Bulletins Officiels")
        
        self.miseEnPlace()
        
        wx.CallAfter(self.Thaw)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
    ###############################################################################################
    def GetDocument(self):
        return self.projet
    
    ###############################################################################################
    def AjouterTache(self, event = None):
        self.arbre.AjouterTache()
        
        
    ###############################################################################################
    def OnPageChanged(self, event):
        new = event.GetSelection()
        event.Skip()
        if new == 1: # On vient de cliquer sur la page "détails"
            self.pageDetails.Remplir(self.fichierCourant, self.projet, self.typ)
        
        elif new == 2: # On vient de cliquer sur la page "dossier de validation"
            self.pageValid.MiseAJour(self.projet, self)
            
        elif new == 3: # On vient de cliquer sur la page "Bulletins Officiels"
            self.pageBO.Construire(REFERENTIELS[self.projet.classe.typeEnseignement])

        elif new == 0: # On vient de cliquer sur la fiche
            self.fiche.Redessiner()
            
            
    ###############################################################################################
    def OnDocModified(self, event):
#        print "OnDocModified"
        if event.GetDocument() == self.projet:
            self.projet.VerifPb()
            self.projet.SetCompetencesRevuesSoutenance(miseAJourPanel = False)
            
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
    def ouvrir(self, nomFichier, redessiner = True, reparer = False):
        print "Ouverture projet", nomFichier
        tps1 = time.clock()
        Ok = True
        Annuler = False
        nbr_etapes = 11
        
        # Pour le suivi de l'ouverture
        nomCourt = os.path.splitext(os.path.split(nomFichier)[1])[0]
        
        message = nomCourt+"\n"
        dlg = myProgressDialog(u"Ouverture d'un projet",
                                   message,
                                   nbr_etapes,
                                   self.parent)
        
#        dlg =    wx.ProgressDialog(u"Ouverture d'un projet",
#                                   message,
#                                   maximum = nbr_etapes,
#                                   parent=self.parent,
#                                   style = 0
#                                    | wx.PD_APP_MODAL
#                                    #| wx.PD_CAN_ABORT
#                                    #| wx.PD_CAN_SKIP
#                                    #| wx.PD_ELAPSED_TIME
#                                    | wx.PD_ESTIMATED_TIME
#                                    | wx.PD_REMAINING_TIME
#                                    #| wx.PD_AUTO_HIDE
#                                    )

#        print dir(dlg)
        
        self.fiche.Hide()
        
        fichier = open(nomFichier,'r')
        self.definirNomFichierCourant(nomFichier)
    
        
        def ouvre(fichier, message):
            root = ET.parse(fichier).getroot()
            count = 0
            Ok = True
            Annuler = False
                   
            # Le projet
            projet = root.find("Projet")
            if projet == None:
                self.projet.setBranche(root)
                
            else:
                # La classe
                message += u"Construction de la structure de la classe...\t"
                dlg.Update(count, message)
                count += 1
                classe = root.find("Classe")
                err = self.classe.setBranche(classe, reparer = reparer)
                if len(err) > 0 :
                    Ok = False
                    message += (u"\n  "+CHAR_POINT).join([e.getMessage() for e in err]) 
                message += u"\n"
                
#                print "V",self.classe.GetVersionNum()
                if self.classe.GetVersionNum() < 5:
                    messageErreur(None, u"Ancien programme", 
                                  u"Projet enregistré avec les indicateurs de compétence antérieurs à la session 2014\n\n"\
                                  u"Les indicateurs de compétence ne seront pas chargés.")
                
                # Le projet
                message += u"Construction de la structure du projet...\t"
                dlg.Update(count, message)
                count += 1
#                print "ref :", 
#                self.projet.classe = self.classe
                # Dernière vérification
                if self.projet.GetProjetRef() == None:
                    print "Pas bon référentiel"
                    self.classe.setBranche(classe, reparer = True)
                err = self.projet.setBranche(projet)
    
            
                if len(err) > 0 :
                    Ok = False
                    message += (u"\n  "+CHAR_POINT).join([e.getMessage() for e in err])
                message += u"\n"
                
            self.arbre.DeleteAllItems()
            root = self.arbre.AddRoot("")
            
            message += u"Traitement des revues...\t"
            dlg.Update(count, message)
            count += 1
            try:
                self.projet.SetCompetencesRevuesSoutenance()
                message += u"Ok\n"
            except:
                Ok = False
                Annuler = True
                message += u"Erreur !\n"
                print "Erreur 4"
                        
            return root, message, count, Ok, Annuler
        
        
        if "beta" in __version__:
#            print "beta"
            root, message, count, Ok, Annuler = ouvre(fichier, message)
            err = []
        else:
            try:
                err = []
                root, message, count, Ok, Annuler = ouvre(fichier, message)
            except:
                count = 0
                err = [constantes.Erreur(constantes.ERR_INCONNUE)]
                message += err[0].getMessage() + u"\n"
                Annuler = True
        
        #
        # Erreur fatale d'ouverture
        #
        if Annuler:
            message += u"\n\nLe projet n'a pas pu être ouvert !\n\n"
            if len(err) > 0:
                message += u"\n   L'erreur concerne :"
                message += (u"\n"+CHAR_POINT).join([e.getMessage() for e in err])
            fichier.close()
            self.Close()
            count = nbr_etapes
            dlg.Update(count, message)
            dlg.Destroy()
#            wx.CallAfter(self.fiche.Show)
#            wx.CallAfter(self.fiche.Redessiner)
            return
        
        liste_actions = [[self.classe.ConstruireArbre, [self.arbre, root], {},
                         u"Construction de l'arborescence de la classe...\t"],
                         [self.projet.ConstruireArbre, [self.arbre, root], {},
                          u"Construction de l'arborescence du projet...\t"],
                         [self.projet.OrdonnerTaches, [], {},
                          u"Ordonnancement des tâches...\t"],
                         [self.projet.PubDescription, [], {},
                          u"Traitement des descriptions...\t"],
                         [self.projet.SetLiens, [], {},
                          u"Construction des liens...\t"],
                         [self.projet.MiseAJourDureeEleves, [], {},
                          u"Ajout des durées/évaluabilités dans l'arbre...\t"],
                         [self.projet.MiseAJourNomProfs, [], {},
                          u"Ajout des disciplines dans l'arbre...\t"],
                         ]
        
        for fct, arg, karg, msg in liste_actions:
            message += msg
            dlg.Update(count, message)
            count += 1
            try :
                fct(*arg, **karg)
                message += u"Ok\n"
            except:
                Ok = False
                message += constantes.Erreur(constantes.ERR_INCONNUE).getMessage() + u"\n"
            

        self.projet.Verrouiller()

        message += u"Tracé de la fiche...\t"
        dlg.Update(count, message)
        count += 1

#        self.arbre.SelectItem(self.classe.branche)

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        
        fichier.close()
        
        

#        if redessiner:
#
#        self.fiche.Show()
#        time.sleep(1)
#        self.fiche.Redessiner()
#        message += u"Ok\n"
#            
#        try :
#            self.fiche.Show()
##            self.fiche.Redessiner()
#            message += u"Ok\n"
#        except:
#            Ok = False
#            message += constantes.Erreur(constantes.ERR_INCONNUE).getMessage() + u"\n"
#            
#        dlg.Update(count, message)
        
        tps2 = time.clock() 
        print "Ouverture :", tps2 - tps1

        if Ok:
            dlg.Destroy()
        else:
            dlg.Update(nbr_etapes, message)
            dlg.Raise()
            dlg.Close() 
    
        wx.CallAfter(self.fiche.Show)
        wx.CallAfter(self.fiche.Redessiner)
        wx.CallAfter(dlg.Raise)

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
#            print "nomFichiers", nomFichiers
            
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
    def genererGrillesPdf(self, event = None):
        """ Génération de TOUTES les grilles d'évaluation au format pdf
             - demande d'un nom de fichier -
        """
        mesFormats = u"PDF (.pdf)|*.pdf"
        nomFichier = getNomFichier("Grilles", self.projet.intitule[:20], r".pdf")
        dlg = wx.FileDialog(self, u"Enregistrer les grilles d'évaluation",
                            defaultFile = nomFichier,
                            wildcard = mesFormats,
#                           defaultPath = globdef.DOSSIER_EXEMPLES,
                            style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR
                            #| wx.DD_DIR_MUST_EXIST
                            #| wx.DD_CHANGE_DIR
                            )

        if dlg.ShowModal() == wx.ID_OK:
            nomFichier = dlg.GetPath()
            dlg.Destroy()
            dlgb = wx.ProgressDialog   (u"Génération des grilles",
                                        u"",
                                        maximum = len(self.projet.eleves)+1,
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
            
            
            pathprj = self.projet.GetPath()
            print "pathprj", pathprj
            
            #
            # Détermination des fichiers grille à créer
            #
            nomFichiers = {}
            for e in self.projet.eleves:
                if len(e.grille) == 0: # Pas de fichier grille connu pour cet élève
                    nomFichiers[e.id] = e.GetNomGrilles(path = os.path.split(nomFichier)[0])
                else:
                    for g in e.grille.values():
                        if not os.path.exists(g.path): # Le fichier grille pour cet élève n'a pas été trouvé
                            nomFichiers[e.id] = e.GetNomGrilles(path = os.path.split(nomFichier)[0])
            print "nomFichiers grille", nomFichiers
            
            # Si des fichiers existent avec le même nom, on demande si on peut les écraser
            if not self.projet.TesterExistanceGrilles(nomFichiers):
                dlgb.Destroy()
                return
            
            
#            dicInfo = self.projet.GetProjetRef().cellulesInfo
#            classNON = dicInfo["NON"][0][0]
#            feuilNON = dicInfo["NON"][0][1]
#            collectif = self.projet.GetProjetRef().grilles[classNON][1] == 'C'
            
            # Elaboration de la liste des fichiers/feuilles à exporter en PDF
            lst_grilles = []
            for e in self.projet.eleves:
                dlgb.Update(count, u"Traitement de la grille de \n\n"+e.GetNomPrenom())
                dlgb.Refresh()
                    
                if e.id in nomFichiers.keys():
                    e.GenererGrille(nomFichiers = nomFichiers[e.id], messageFin = False)

                for k, g in e.grille.items():
                    grille = os.path.join(toFileEncoding(pathprj), g.path)
                    if k in self.projet.GetReferentiel().aColNon.keys():
#                    if k == classNON:
                        collectif = self.projet.GetProjetRef().grilles[k][1] == 'C'
                        feuilNON = self.projet.GetProjetRef().cellulesInfo[k]["NON"][0][0]
                        if feuilNON != '' and collectif: # fichier "Collectif"
                            feuille = feuilNON+str(e.id+1)
                        else:
                            feuille = None
                    else:
                        feuille = None
                
                    lst_grilles.append((grille, feuille))
                
                count += 1
                dlgb.Refresh()
            
            dlgb.Update(count, u"Compilation des grilles ...\n\n")
            count += 1
            dlgb.Refresh()
                
            genpdf.genererGrillePDF(nomFichier, lst_grilles)
            
            dlgb.Update(count, u"Les grilles ont été créées avec succès dans le fichier :\n\n"+nomFichier)
            dlgb.Destroy() 
                
                
        else:
            dlg.Destroy()
            
            
            
    #############################################################################
    def genererFicheValidation(self, event = None):
#        mesFormats = "Tableur Excel (.xls)|*.xls"
        
#        def getNomFichier(prefixe, projet):
#            nomFichier = prefixe+"_"+projet.intitule[:20]
#            for c in ["\"", "/", "\", ", "?", "<", ">", "|", ":", "."]:
#                nomFichier = nomFichier.replace(c, "_")
#            return nomFichier+".pdf"
        
        mesFormats = u"PDF (.pdf)|*.pdf"
        nomFichier = getNomFichier("FicheValidation", self.projet.intitule[:20], r".pdf")
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
#        self.Bind(wx.EVT_SCROLLWIN, self.OnScroll)
        
        self.InitBuffer()

    ######################################################################################################
    def OnLeave(self, evt = None):
        if hasattr(self, 'call') and self.call.IsRunning():
            self.call.Stop()
#        if hasattr(self, 'tip') 
#            self.tip.Show(False)

    ######################################################################################################
    def OnEnter(self, event):
#        print "OnEnter Fiche"
        self.SetFocus()
        event.Skip()
        
        
    #############################################################################            
    def OnResize(self, evt):
        w = self.GetClientSize()[0]
        self.SetVirtualSize((w,w*29/21)) # Mise au format A4

        self.InitBuffer()
        if w > 0 and self.IsShown():
            self.Redessiner()


    #############################################################################            
    def OnScroll(self, evt):
        self.Refresh()



    #############################################################################            
    def OnPaint(self, evt):
#        print "OnPaint"
#        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.DrawBitmap(self.buffer, 0,0) 
        
        
    #############################################################################            
    def CentrerSur(self, obj):
        if hasattr(obj, 'rect'):
            y = (obj.rect[0][1])*self.GetVirtualSizeTuple()[1]
            self.Scroll(0, y/20)
            self.Refresh()
    
    
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
            
            
        if self.GetDoc().pasVerouille:
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
        
        def redess():
            wx.BeginBusyCursor()
                
    #        tps1 = time.clock() 
                
            
    #        face = wx.lib.wxcairo.FontFaceFromFont(wx.FFont(10, wx.SWISS, wx.FONTFLAG_BOLD))
    #        ctx.set_font_face(face)
            
            cdc = wx.ClientDC(self)
            self.PrepareDC(cdc) 
            dc = wx.BufferedDC(cdc, self.buffer, wx.BUFFER_VIRTUAL_AREA)
            dc.SetBackground(wx.Brush('white'))
            dc.Clear()
            ctx = wx.lib.wxcairo.ContextFromDC(dc)
            dc.BeginDrawing()
            self.normalize(ctx)
            
            self.Draw(ctx)
            
    #        b = Thread(None, self.Draw, None, (ctx,))
    #        b.start()
            
            dc.EndDrawing()
            self.ctx = ctx
            self.Refresh()
    
    #        tps2 = time.clock() 
    #        print "Tracé :"#, tps2 - tps1
            
            wx.EndBusyCursor()
            
        redess()
#        wx.CallAfter(redess)
#        a = threading.Thread(None, redess, None) 
#        a.start()
    
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
        
        self.lab_legend = {}
        for i, (part , tit) in enumerate(self.projet.GetProjetRef().parties.items()):
            self.lab_legend[part] = popup.CreerTexte((l,i), txt = tit, flag = wx.ALIGN_RIGHT|wx.RIGHT)
            self.lab_legend[part].SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
            self.lab_legend[part].SetForegroundColour(constantes.COUL_PARTIE[part])
            
            
#        self.lab_legend1 = popup.CreerTexte((l,0), txt = u"Conduite", flag = wx.ALIGN_RIGHT|wx.RIGHT)
#        self.lab_legend1.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
#        self.lab_legend1.SetForegroundColour(constantes.COUL_PARTIE['C'])
#        
#        self.lab_legend2 = popup.CreerTexte((l,1), txt = u"Soutenance", flag = wx.ALIGN_LEFT|wx.LEFT)
#        self.lab_legend2.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
#        self.lab_legend2.SetForegroundColour(constantes.COUL_PARTIE['S'])
        
        self.popup = popup
#        self.MiseAJourTypeEnseignement(self.projet.classe.typeEnseignement)
        
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
        
        #
        # Cas général
        #
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
        
        #
        # Cas particulier des compétences
        #
        kCompObj = self.projet.HitTestCompetence(xx, yy)
        if kCompObj != None:
            kComp, obj = kCompObj
            if hasattr(self, 'popup'):
#                for tip in self.tip_indic:
#                    tip.Destroy()
#                self.tip_indic = []
                x, y = self.ClientToScreen((x, y))
#                type_ens = self.projet.classe.typeEnseignement
                prj = self.projet.GetProjetRef()
                competence = prj.getCompetence(kComp)
                        
                intituleComp = competence[0]
                
                k = kComp.split(u"\n")
                if len(k) > 1:
                    titre = u"Compétences\n"+u"\n".join(k)
                else:
                    titre = u"Compétence\n"+k[0]
                self.popup.SetTitre(titre)
             
                intituleComp = "\n".join([textwrap.fill(ind, 50) for ind in intituleComp.split(u"\n")]) 
             
                self.popup.SetTexte(intituleComp, self.tip_comp)
                
                self.tip_arbre.DeleteChildren(self.tip_arbre.root)
                if type(competence[1]) == dict:  
                    indicEleve = obj.GetDicIndicateurs()
                else:
                    indicEleve = obj.GetDicIndicateurs()[kComp]
                self.tip_arbre.Construire(competence[1], indicEleve, prj)
                
                self.popup.Fit()

                self.popup.Position((x,y), (0,0))
                self.call = wx.CallLater(500, self.popup.Show, True)
                self.tip = self.popup
            
        evt.Skip()


    #############################################################################
#    def MiseAJourTypeEnseignement(self, type_ens):
#        print u"Sert à rien", a
#        texte = u"Indicateur"
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
#        self.SetupScrolling() # Cause des problèmes 
#        self.EnableScrolling(True, True)
        self.eventAttente = False
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)


    ######################################################################################################
    def OnEnter(self, event):
#        print "OnEnter PanelPropriete"
        self.SetFocus()
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
#   Classe définissant le panel "racine" (ne contenant que des infos HTML)
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

#    def GetNiveau(self):
#        return 0
     

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
        position = wx.Slider(self, -1, self.sequence.position, 0, self.sequence.GetReferentiel().getNbrPeriodes()-1, (30, 60), (250, -1), 
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
        draw_cairo_seq.DrawPeriodes(ctx, (0,0,w,h), self.sequence.position,
                                    self.sequence.GetReferentiel().periodes)

        bmp = wx.lib.wxcairo.BitmapFromImageSurface(imagesurface)
        
        # On fait une copie sinon ça s'efface ...
        img = bmp.ConvertToImage()
        bmp = img.ConvertToBitmap()
        
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
#        print "Miseàjour"
        self.textctrl.ChangeValue(self.sequence.intitule)
        
        self.position.SetMax(self.sequence.GetReferentiel().getNbrPeriodes()-1)
        self.sequence.position = min(self.sequence.position, self.sequence.GetReferentiel().getNbrPeriodes()-1)
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
        
        self.nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
        
        self.construire()
        
        self.sizer.Add(self.nb, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
#        self.sizer.Layout()
        
        self.Layout()
        self.FitInside()
        wx.CallAfter(self.PostSizeEvent)
        
        self.MiseAJourTypeEnseignement()
        
        self.Show()
        
#        self.Fit()
        
    #############################################################################            
    def GetPageNum(self, win):
        for np in range(self.nb.GetPageCount()):
            if self.nb.GetPage(np) == win:
                return np
        
    #############################################################################            
    def creerPageSimple(self, fct):
        bg_color = self.Parent.GetBackgroundColour()
        page = PanelPropriete(self.nb)
        page.SetBackgroundColour(bg_color)
        self.nb.AddPage(page, u"")
        ctrl = wx.TextCtrl(page, -1, u"", style=wx.TE_MULTILINE)
        page.Bind(wx.EVT_TEXT, fct, ctrl)
        page.sizer.Add(ctrl, (0,0), flag = wx.EXPAND)
        page.sizer.AddGrowableCol(0)
        page.sizer.AddGrowableRow(0)  
        page.sizer.Layout()
        return page, ctrl, self.nb.GetPageCount()-1
    
    
    #############################################################################            
    def construire(self):
#        ref = self.projet.GetReferentiel()
        self.pages = {}
        
        
        #
        # La page "Généralités"
        #
        pageGen = PanelPropriete(self.nb)
        bg_color = self.Parent.GetBackgroundColour()
        pageGen.SetBackgroundColour(bg_color)
        self.pageGen = pageGen
        self.nb.AddPage(pageGen, u"Propriétés générales")
        
            
        #
        # Intitulé du projet (TIT)
        #
        self.titre = wx.StaticBox(pageGen, -1, u"")
        sb = wx.StaticBoxSizer(self.titre)
        textctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        pageGen.sizer.Add(sb, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
        pageGen.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        
        #
        # Problématique (PB)
        #
        self.tit_pb = wx.StaticBox(pageGen, -1, u"")
        sb = wx.StaticBoxSizer(self.tit_pb)
        self.commctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
        sb.Add(self.commctrl, 1, flag = wx.EXPAND)
        pageGen.sizer.Add(sb, (0,1), (2,1),  flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
        pageGen.Bind(wx.EVT_TEXT, self.EvtText, self.commctrl)
        pageGen.sizer.AddGrowableCol(1)
        
        
        #
        # Année scolaire et Position dans l'année
        #
        titre = wx.StaticBox(pageGen, -1, u"Année et Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        
        self.annee = Variable(u"Année scolaire", lstVal = self.projet.annee, 
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

        
        
        #
        # La page "Enoncé général du besoin" ('ORI')
        #
#        self.pages['ORI'] = self.creerPageSimple(self.EvtText)
#        self.pageBG = PanelPropriete(self.nb)
#        self.pageBG.SetBackgroundColour(bg_color)
#        self.nb.AddPage(self.pageBG, u"")
#        self.bgctrl = wx.TextCtrl(self.pageBG, -1, u"", style=wx.TE_MULTILINE)
#        self.pageBG.Bind(wx.EVT_TEXT, self.EvtText, self.bgctrl)
#        self.pageBG.sizer.Add(self.bgctrl, (0,0), flag = wx.EXPAND)
#        self.pageBG.sizer.AddGrowableCol(0)
#        self.pageBG.sizer.AddGrowableRow(0)  
#        self.pageBG.sizer.Layout()
        
        
        #
        # La page "Contraintes Imposées" (CCF)
        #
#        self.pages['CCF'] = self.creerPageSimple(self.EvtText)
#        self.pageCont = PanelPropriete(self.nb)
#        self.pageCont.SetBackgroundColour(bg_color)
#        self.nb.AddPage(self.pageCont, u"")  
#        self.contctrl = wx.TextCtrl(self.pageCont, -1, u"", style=wx.TE_MULTILINE)
#        self.pageCont.Bind(wx.EVT_TEXT, self.EvtText, self.contctrl)
#        self.pageCont.sizer.Add(self.contctrl, (0,0), flag = wx.EXPAND)
#        self.pageCont.sizer.AddGrowableCol(0)
#        self.pageCont.sizer.AddGrowableRow(0)  
#        self.pageCont.sizer.Layout()
        
        
        
        
        
        #
        # La page "Production attendue" ('OBJ')
        #
#        self.pages['OBJ'] = self.creerPageSimple(self.EvtText)
#        self.pageProd = PanelPropriete(self.nb)
#        self.pageProd.SetBackgroundColour(bg_color)
#        self.nb.AddPage(self.pageProd, u"")
#        self.prodctrl = wx.TextCtrl(self.pageProd, -1, u"", style=wx.TE_MULTILINE)
#        self.pageProd.Bind(wx.EVT_TEXT, self.EvtText, self.prodctrl)
#        self.pageProd.sizer.Add(self.prodctrl, (0,0), flag = wx.EXPAND)
#        self.pageProd.sizer.AddGrowableCol(0)
#        self.pageProd.sizer.AddGrowableRow(0)  
#        self.pageProd.sizer.Layout()
    
    
    #############################################################################            
    def getBitmapPeriode(self, larg):
#        print "getBitmapPeriode"
#        print "  ", self.projet.position
#        print "  ", self.projet.GetReferentiel().periodes
#        print "  ", self.projet.GetReferentiel().periode_prj
        w, h = 0.04*7, 0.04
        imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  larg, int(h/w*larg))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        ctx = cairo.Context(imagesurface)
        ctx.scale(larg/w, larg/w) 
        draw_cairo_prj.DrawPeriodes(ctx, (0,0,w,h), self.projet.position, 
                                    self.projet.GetReferentiel().periodes ,
                                    self.projet.GetReferentiel().projets)

        bmp = wx.lib.wxcairo.BitmapFromImageSurface(imagesurface)
        
        # On fait une copie sinon ça s'efface ...
        img = bmp.ConvertToImage()
        bmp = img.ConvertToBitmap()

        return bmp
         
    
    #############################################################################            
    def onChanged(self, evt):
        self.projet.SetPosition(evt.EventObject.GetValue())
#        self.SetBitmapPosition()
        
        
        
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
        self.Refresh()
            
              
    #############################################################################            
    def EvtText(self, event):
        if event.GetEventObject() == self.textctrl:
            nt = event.GetString()
            if nt == u"":
                nt = self.projet.support.nom
            self.projet.SetText(nt)
            self.textctrl.ChangeValue(nt)
            maj = True
            
        elif 'ORI' in self.pages.keys() and event.GetEventObject() == self.pages['ORI'][1]:
            self.projet.origine = event.GetString()
            maj = False
            
        elif 'CCF' in self.pages.keys() and event.GetEventObject() == self.pages['CCF'][1]:
            self.projet.contraintes = event.GetString()
            maj = False
            
        elif 'OBJ' in self.pages.keys() and event.GetEventObject() == self.pages['OBJ'][1]:
            self.projet.production = event.GetString()
            maj = False
            
        elif 'SYN' in self.pages.keys() and event.GetEventObject() == self.pages['SYN'][1]:
            self.projet.synoptique = event.GetString()
            maj = False
        
        elif hasattr(self, 'intctrl') and event.GetEventObject() == self.intctrl:
            self.projet.intituleParties = event.GetString()
            maj = False
        
        elif hasattr(self, 'enonctrl') and event.GetEventObject() == self.enonctrl:
            self.projet.besoinParties = event.GetString()
            maj = False
            
        elif event.GetEventObject() == self.commctrl:
            self.projet.SetProblematique(event.GetString())
            maj = True
            
        elif 'PAR' in self.parctrl.keys() and event.GetEventObject() == self.parctrl['PAR']:
            self.projet.partenariat = event.GetString()
            maj = False
            
        elif 'PRX' in self.parctrl.keys() and event.GetEventObject() == self.parctrl['PRX']:
            self.projet.montant = event.GetString()
            maj = False
            
        elif 'SRC' in self.parctrl.keys() and event.GetEventObject() == self.parctrl['SRC']:
            self.projet.src_finance = event.GetString()
            maj = False
        
#        else:
#            maj = False
            
            
        if maj and not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True

  
    #############################################################################            
    def EvtCheckListBox(self, event):
        index = event.GetSelection()
#        label = self.lb.GetString(index)
        if self.lb.IsChecked(index):
            if not index in self.projet.typologie:
                self.projet.typologie.append(index)
        else:
            if index in self.projet.typologie:
                self.projet.typologie.remove(index)
#        self.lb.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
        print "typologie", self.projet.typologie
        
            
    #############################################################################            
    def MiseAJourTypeEnseignement(self, sendEvt = False):
        
        ref = self.projet.GetProjetRef()
#        print "MiseAJourTypeEnseignement", ref.code
        
        
        #
        # Page "Généralités"
        #
        self.titre.SetLabel(ref.attributs['TIT'][0])
        
        self.tit_pb.SetLabel(ref.attributs['PB'][0])
        self.commctrl.SetToolTipString(ref.attributs['PB'][1] + constantes.TIP_PB_LIMITE)
        
        self.MiseAJourPosition()
        self.panelOrga.MiseAJourListe()
        
        
        #
        # Pages simples
        #
        for k in ['ORI', 'CCF', 'OBJ', 'SYN']:
            if ref.attributs[k][0] != u"":
                if not k in self.pages.keys():
                    self.pages[k] = self.creerPageSimple(self.EvtText)
                self.nb.SetPageText(self.GetPageNum(self.pages[k][0]), ref.attributs[k][0])
                self.pages[k][1].SetToolTipString(ref.attributs[k][1])
            else:
                if k in self.pages.keys():
                    self.nb.DeletePage(self.GetPageNum(self.pages[k][0]))
                    del self.pages[k]
                
                    
        #
        # Pages spéciales
        #       
        
        # La page "sous parties" ('DEC')
        
        if ref.attributs['DEC'][0] != "":
            if not 'DEC' in self.pages.keys():
                self.pages['DEC'] = PanelPropriete(self.nb)
                bg_color = self.Parent.GetBackgroundColour()
                self.pages['DEC'].SetBackgroundColour(bg_color)
                
                self.nb.AddPage(self.pages['DEC'], ref.attributs['DEC'][0])
                
                self.nbrParties = Variable(u"Nombre de sous parties",  
                                           lstVal = self.projet.nbrParties, 
                                           typ = VAR_ENTIER_POS, bornes = [1,5])
                self.ctrlNbrParties = VariableCtrl(self.pages['DEC'], self.nbrParties, coef = 1, signeEgal = False,
                                        help = u"Nombre de sous parties", sizeh = 30)
                self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlNbrParties)
                self.pages['DEC'].sizer.Add(self.ctrlNbrParties, (0,0), flag = wx.EXPAND|wx.ALL, border = 2)
                
                titreInt = wx.StaticBox(self.pages['DEC'], -1, u"Intitulés des différentes parties")
                sb = wx.StaticBoxSizer(titreInt)
                
                self.intctrl = wx.TextCtrl(self.pages['DEC'], -1, u"", style=wx.TE_MULTILINE)
                self.intctrl.SetToolTipString(u"Intitulés des parties du projet confiées à chaque groupe.\n" \
                                              u"Les groupes d'élèves sont désignés par des lettres (A, B, C, ...)\n" \
                                              u"et leur effectif est indiqué.")
                self.pages['DEC'].Bind(wx.EVT_TEXT, self.EvtText, self.intctrl)
                sb.Add(self.intctrl, 1, flag = wx.EXPAND)
                self.pages['DEC'].sizer.Add(sb, (1,0), flag = wx.EXPAND|wx.ALL, border = 2)
                
                titreInt = wx.StaticBox(self.pages['DEC'], -1, u"Enoncés du besoin des différentes parties du projet")
                sb = wx.StaticBoxSizer(titreInt)
                self.enonctrl = wx.TextCtrl(self.pages['DEC'], -1, u"", style=wx.TE_MULTILINE)
                self.enonctrl.SetToolTipString(u"Enoncés du besoin des parties du projet confiées à chaque groupe")
                self.pages['DEC'].Bind(wx.EVT_TEXT, self.EvtText, self.enonctrl)
                sb.Add(self.enonctrl, 1, flag = wx.EXPAND)
                self.pages['DEC'].sizer.Add(sb, (0,1), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)
                
                self.pages['DEC'].sizer.AddGrowableCol(1)
                self.pages['DEC'].sizer.AddGrowableRow(1)  
                self.pages['DEC'].sizer.Layout()
                
        else:
            if 'DEC' in self.pages.keys():
                self.nb.DeletePage(self.GetPageNum(self.pages['DEC']))
                del self.pages['DEC']
        
        
        # La page "typologie" ('TYP')
        
        if ref.attributs['TYP'][0] != "":
            if not 'TYP' in self.pages.keys():
                self.pages['TYP'] = PanelPropriete(self.nb)
                bg_color = self.Parent.GetBackgroundColour()
                self.pages['TYP'].SetBackgroundColour(bg_color)
                
                self.nb.AddPage(self.pages['TYP'], ref.attributs['TYP'][0])
                
                liste = ref.attributs['TYP'][2].split(u"\n")
                self.lb = wx.CheckListBox(self.pages['TYP'], -1, (80, 50), wx.DefaultSize, liste)
                self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.lb)
                
                self.pages['TYP'].sizer.Add(self.lb, (0,0), flag = wx.EXPAND|wx.ALL, border = 2)
                
                self.pages['TYP'].sizer.AddGrowableCol(0)
                self.pages['TYP'].sizer.AddGrowableRow(0)  
                self.pages['TYP'].sizer.Layout()
                
        else:
            if 'TYP' in self.pages.keys():
                self.nb.DeletePage(self.GetPageNum(self.pages['TYP']))
                del self.pages['TYP']
        
        # La page "Partenariat" ('PAR')
        
        if ref.attributs['PAR'][0] != "":
            if not 'PAR' in self.pages.keys():
                self.parctrl = {}
                self.pages['PAR'] = PanelPropriete(self.nb)
                bg_color = self.Parent.GetBackgroundColour()
                self.pages['PAR'].SetBackgroundColour(bg_color)
                
                self.nb.AddPage(self.pages['PAR'], ref.attributs['PAR'][0])
                
                for i, k in enumerate(['PAR', 'PRX', 'SRC']):
                    titreInt = wx.StaticBox(self.pages['PAR'], -1, ref.attributs[k][0])
                    sb = wx.StaticBoxSizer(titreInt)
                
                    self.parctrl[k] = wx.TextCtrl(self.pages['PAR'], -1, u"", style=wx.TE_MULTILINE)
                    self.parctrl[k].SetToolTipString(ref.attributs[k][1])
                    self.pages['PAR'].Bind(wx.EVT_TEXT, self.EvtText, self.parctrl[k])
                    sb.Add(self.parctrl[k], 1, flag = wx.EXPAND)
                    self.pages['PAR'].sizer.Add(sb, (0,i), flag = wx.EXPAND|wx.ALL, border = 2)
                
                self.pages['PAR'].sizer.AddGrowableCol(0)
                self.pages['PAR'].sizer.AddGrowableRow(0)  
                self.pages['PAR'].sizer.Layout()
                
        else:
            if 'PAR' in self.pages.keys():
                self.nb.DeletePage(self.GetPageNum(self.pages['PAR']))
                del self.pages['PAR']
                self.parctrl = {}
        
    #############################################################################            
    def MiseAJourPosition(self, sendEvt = False):
        self.bmp.SetBitmap(self.getBitmapPeriode(250))
        self.position.SetRange(0, self.projet.GetLastPosition())
        self.position.SetValue(self.projet.position)
    

    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "mise à jour panel table"
        ref = self.projet.GetProjetRef()
        
        # La page "Généralités"
        self.textctrl.ChangeValue(self.projet.intitule)
        self.commctrl.ChangeValue(self.projet.problematique)
        
        # Les pages simples
        if 'ORI' in self.pages.keys():
            self.pages['ORI'][1].ChangeValue(self.projet.origine)
        if 'CCF' in self.pages.keys():
            self.pages['CCF'][1].ChangeValue(self.projet.contraintes)
        if 'OBJ' in self.pages.keys():
            self.pages['OBJ'][1].ChangeValue(self.projet.production)
        if 'SYN' in self.pages.keys():
            self.pages['SYN'][1].ChangeValue(self.projet.synoptique)
        
        # La page "typologie" ('TYP')
        if ref.attributs['TYP'][0] != "":
            for t in self.projet.typologie:
                self.lb.Check(t)
                
        # La page "sous parties" ('DEC')
        if ref.attributs['DEC'][0] != "":
            self.intctrl.ChangeValue(self.projet.intituleParties)
            self.enonctrl.ChangeValue(self.projet.besoinParties)
            self.nbrParties.v[0] = self.projet.nbrParties
            self.ctrlNbrParties.mofifierValeursSsEvt()
        
        # La page "Partenariat" ('PAR')
        if ref.attributs['PAR'][0] != "":
            self.parctrl['PAR'].ChangeValue(self.projet.partenariat)
            self.parctrl['PRX'].ChangeValue(self.projet.montant)
            self.parctrl['SRC'].ChangeValue(self.projet.src_finance)
                    
        self.MiseAJourPosition()
     
        self.panelOrga.MiseAJourListe()
        self.Layout()
        
        if sendEvt:
            self.sendEvent()


    #############################################################################            
    def GetDocument(self):
        return self.projet


    ######################################################################################  
    def Verrouiller(self, etat):
        self.position.Enable(etat)
        
        
    
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
        ref = self.objet.GetProjetRef()
        if ref.getClefDic('phases', self.liste.GetString(event.GetSelection()), 0) in TOUTES_REVUES_EVAL:
            self.buttonUp.Enable(True)
            self.buttonDown.Enable(True)
        else:
            self.buttonUp.Enable(False)
            self.buttonDown.Enable(False)
            
            
        
    #############################################################################            
    def OnClick(self, event):
        i = event.GetId()
        revue = self.liste.GetStringSelection()
        ref = self.objet.GetProjetRef()
        
        if revue[:5] == "Revue":
            posRevue = self.liste.GetSelection()
            numRevue = eval(revue[-1])
            if i == 11 and posRevue-2 >= 0:
                nouvPosRevue = posRevue-2   # Montée
                monte = True
            elif i == 12 and posRevue < self.liste.GetCount() - 1:
                nouvPosRevue = posRevue+1   # Descente
                monte = False
            else:
                return
            itemPrecedent = ref.getClefDic('phases', self.liste.GetString(nouvPosRevue), 0)
#            itemPrecedent = constantes.getCodeNomCourt(self.liste.'(nouvPosRevue), 
#                                                       self.objet.GetTypeEnseignement(simple = True))
            j=1
            while itemPrecedent in TOUTES_REVUES_EVAL:
                itemPrecedent = ref.getClefDic('phases', self.liste.GetString(nouvPosRevue-j), 0)
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
            if monte:
                self.objet.VerifierIndicRevue(numRevue)
            self.parent.sendEvent()
        
    #############################################################################            
    def MiseAJourListe(self):
#        print "MiseAJourListe"
#        print self.objet.GetListeNomsPhases()
        prj = self.objet.GetProjetRef()
        self.ctrlNbrRevues.redefBornes([min(prj.posRevues.keys()), max(prj.posRevues.keys())])
        self.ctrlNbrRevues.setValeur(prj.getNbrRevuesDefaut())
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
    def __init__(self, parent, classe, pourProjet, ouverture = False, typedoc = ''):
#        print "__init__ PanelPropriete_Classe"
        PanelPropriete.__init__(self, parent)
#        self.BeginRepositioningChildren()
        
        #
        # La page "Généralités"
        #
        nb = wx.Notebook(self, -1,  style= wx.BK_DEFAULT)
        pageGen = PanelPropriete(nb)
        bg_color = self.Parent.GetBackgroundColour()
        pageGen.SetBackgroundColour(bg_color)
        self.pageGen = pageGen
        
        nb.AddPage(pageGen, u"Propriétés générales")


        #
        # la page "Systèmes"
        #
        pageSys = PanelPropriete(nb)
        pageSys.SetBackgroundColour(bg_color)
        nb.AddPage(pageSys, u"Systèmes techniques et Matériel")
        self.pageSys = pageSys
        
        self.sizer.Add(nb, (0,1), (2,1), flag = wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND, border = 1)
        self.nb = nb
        self.sizer.AddGrowableCol(1)

        self.classe = classe
        self.pasVerrouille = True


        #
        # La barre d'outils
        #
        self.tb = tb = wx.ToolBar(self, style = wx.TB_VERTICAL|wx.TB_FLAT|wx.TB_NODIVIDER)
        self.sizer.Add(tb, (0,0), (2,1), flag = wx.ALL|wx.ALIGN_RIGHT, border = 1)
        t = u"Sauvegarder ces paramètres de classe dans un fichier :\n" \
            u" - type d'enseignement\n" \
            u" - effectifs\n" \
            u" - établissement\n"
        if typedoc == 'seq':
            t += u" - systèmes\n"
        elif typedoc == 'prj':
            t += u" - nombre de revues et positions\n"
    
        tsize = (24,24)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        save_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        
        tb.AddSimpleTool(30, open_bmp, u"Ouvrir un fichier classe")
        self.Bind(wx.EVT_TOOL, self.commandeOuvrir, id=30)
        
        tb.AddSimpleTool(32, save_bmp, t)
        self.Bind(wx.EVT_TOOL, self.commandeSauve, id=32)
        
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
        self.st_type = wx.StaticText(pageGen, -1, "")
        self.st_type.Show(False)
        sb.Add(te, 1, flag = wx.EXPAND)
        sb.Add(self.st_type, 1, flag = wx.EXPAND)
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

        pageGen.sizer.Add(sb, (0,1), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)#
        self.cb_type = te

        #
        # Etablissement
        #
        titre = wx.StaticBox(pageGen, -1, u"Etablissement")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        sh = wx.BoxSizer(wx.HORIZONTAL)
        t = wx.StaticText(pageGen, -1, u"Académie :")
        sh.Add(t, flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        lstAcad = sorted([a[0] for a in constantes.ETABLISSEMENTS.values()])
        self.cba = wx.ComboBox(pageGen, -1, u"sélectionner une académie ...", (-1,-1), 
                         (-1, -1), lstAcad+[u""],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboAcad, self.cba)
        pageGen.Bind(wx.EVT_TEXT, self.EvtComboAcad, self.cba)
        sh.Add(self.cba, flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.LEFT, border = 5)
        sb.Add(sh, flag = wx.EXPAND)
        
        sh = wx.BoxSizer(wx.HORIZONTAL)
        t = wx.StaticText(pageGen, -1, u"Ville :")
        sh.Add(t, flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
     
        self.cbv = wx.ComboBox(pageGen, -1, u"sélectionner une ville ...", (-1,-1), 
                         (-1, -1), [],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboVille, self.cbv)
        pageGen.Bind(wx.EVT_TEXT, self.EvtComboVille, self.cbv)
        sh.Add(self.cbv, flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.LEFT, border = 5)
        sb.Add(sh, flag = wx.EXPAND)
        
        t = wx.StaticText(pageGen, -1, u"Etablissement :")
        sb.Add(t, flag = wx.EXPAND)
        
        self.cbe = wx.ComboBox(pageGen, -1, u"sélectionner un établissement ...", (-1,-1), 
                         (-1, -1), [u"autre ..."],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboEtab, self.cbe)
        sb.Add(self.cbe, flag = wx.EXPAND)

#        textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
#        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
##        textctrl.SetMinSize((-1, 150))
#        sb.Add(textctrl, 1, flag = wx.EXPAND)
#        self.textctrl = textctrl
        
#        self.info = wx.StaticText(self, -1, u"""Inscrire le nom de l'établissement dans le champ ci-dessus...
#        ou bien modifier le fichier "etablissements.txt"\n        pour le faire apparaitre dans la liste.""")
#        self.info.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
#        sb.Add(self.info, 0, flag = wx.EXPAND|wx.ALL, border = 5)

        pageGen.sizer.Add(sb, (0,2), (1,1), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, border = 2)
        
        #
        # Accès au BO
        #
        titre = wx.StaticBox(pageGen, -1, u"Documents Officiels en ligne")
        self.bo = []
        sbBO = wx.StaticBoxSizer(titre, wx.VERTICAL)
        pageGen.sizer.Add(sbBO, (1,2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, border = 2)
        self.sbBO = sbBO
#        self.SetLienBO()
        
        
        #
        # Effectifs
        #
        self.ec = PanelEffectifsClasse(pageGen, classe)
        pageGen.sizer.Add(self.ec, (0,3), (2,1), flag = wx.ALL|wx.EXPAND, border = 2)#|wx.ALIGN_RIGHT

        pageGen.sizer.AddGrowableRow(0)
        pageGen.sizer.AddGrowableCol(2)
#        pageGen.sizer.Layout()

        #
        # Systèmes
        #
        self.btnAjouterSys = wx.Button(pageSys, -1, u"Ajouter un système")
        self.btnAjouterSys.SetToolTipString(u"Ajouter un nouveau système à la liste")
        self.Bind(wx.EVT_BUTTON, self.EvtButtonSyst, self.btnAjouterSys)
        
        self.lstSys = wx.ListBox(pageSys, -1,
                                 choices = [""], style = wx.LB_SINGLE | wx.LB_SORT)
        self.Bind(wx.EVT_LISTBOX, self.EvtListBoxSyst, self.lstSys)
        
        s = Systeme(self.classe, pageSys, "")
        self.panelSys = s.panelPropriete
        self.panelSys.Show()
    
        pageSys.sizer.Add(self.btnAjouterSys, (0,0), flag = wx.ALL|wx.EXPAND, border = 2)
        pageSys.sizer.Add(self.lstSys, (1,0), flag = wx.ALL|wx.EXPAND, border = 2)
        pageSys.sizer.Add(self.panelSys, (0,1), (2,1),  flag = wx.ALL|wx.EXPAND, border = 2)
        pageSys.sizer.AddGrowableRow(1)
        pageSys.sizer.AddGrowableCol(1)
    
        self.Bind(wx.EVT_SIZE, self.OnResize)
        
        
#        wx.CallAfter(self.cb_type.CollapseAll)
#        wx.CallAfter(self.Thaw)
        
        
    ######################################################################################              
    def OnResize(self, evt = None):
#        print "Resize ArbreTypeEnseignement", self.GetClientSize()
        self.cb_type.SetMinSize((-1, self.GetClientSize()[1]-30))
        self.cb_type.Layout()
        self.pageGen.sizer.Layout()
        if evt:
            evt.Skip()


    
        
        
    ###############################################################################################
    def commandeOuvrir(self, event = None, nomFichier = None):
        mesFormats = constantes.FORMAT_FICHIER_CLASSE['cla'] + constantes.TOUS_FICHIER
  
        if nomFichier == None:
            dlg = wx.FileDialog(
                                self, message=u"Ouvrir une classe",
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
        if nomFichier != '':
            self.classe.ouvrir(nomFichier)
        
        self.sendEvent()
    
    ###############################################################################################
    def enregistrer(self, nomFichier):

        wx.BeginBusyCursor()
        fichier = file(nomFichier, 'w')
        
        # La classe
        classe = self.classe.getBranche()
        
        # La racine
        constantes.indent(classe)
        
        try:
            ET.ElementTree(classe).write(fichier, encoding = DEFAUT_ENCODING)
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

        wx.EndBusyCursor()
        
    #############################################################################
    def commandeSauve(self, event):
        mesFormats = constantes.FORMAT_FICHIER_CLASSE['cla'] + constantes.TOUS_FICHIER
        dlg = wx.FileDialog(self, 
                            message = constantes.MESSAGE_ENR['cla'], 
                            defaultDir="" , 
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
    def OnDefautPref(self, evt):
#        self.classe.options.defaut()
        self.classe.Initialise(isinstance(self.classe.doc, Projet), defaut = True)
#        self.classe.doc.AjouterListeSystemes(self.classe.systemes)
        self.MiseAJour()
        self.sendEvent()
        
        
#    #############################################################################            
#    def OnValidPref(self, evt):
#        try:
#            self.classe.options.valider(self.classe, self.classe.doc)
#            self.classe.options.enregistrer()
#        except IOError:
#            messageErreur(self, u"Permission refusée",
#                          u"Permission d'enregistrer les préférences refusée.\n\n" \
#                          u"Le dossier est protégé en écriture")
#        except:
#            messageErreur(self, u"Enregistrement impossible",
#                          u"Imposible d'enregistrer les préférences\n\n")
#        return   
        
        
    #############################################################################            
    def GetDocument(self):
        return self.classe.doc
    
    
    #############################################################################            
    def EvtText(self, event):
        if event.GetEventObject() == self.textctrl:
            self.classe.etablissement = event.GetString()
            self.sendEvent()
            
            
    ######################################################################################  
    def EvtComboAcad(self, evt = None):
#        print "EvtComboAcad"
        if evt != None:
            self.classe.academie = evt.GetString()

        lst = []
        for val in constantes.ETABLISSEMENTS.values():
            if self.classe.academie == val[0]:
                if self.classe.GetReferentiel().getTypeEtab() == 'L':
                    lst = val[2]
                else:
                    lst = val[1]
                break
#        print "   ", lst
        if len(lst) > 0:
            lst = sorted(list(set([v for e, v in lst])))
#        print "Villes", lst

        self.cbv.Set(lst)
        self.cbv.Refresh()
            
    
    ######################################################################################  
    def EvtComboVille(self, evt = None):
#        print "EvtComboVille"
        if evt != None:
            self.classe.ville = evt.GetString()
#        print "   ", self.classe.ville
        lst = []
        for val in constantes.ETABLISSEMENTS.values():
            if self.classe.academie == val[0]:
                if self.classe.GetReferentiel().getTypeEtab() == 'L':
                    lst = val[2]
                else:
                    lst = val[1]
                break
#        print "   ", lst
        lst = sorted([e for e, v in lst if v == self.cbv.GetStringSelection()])
#        print "   ", self.cbv.GetStringSelection()
#        print "   Etab", lst
        
        self.cbe.Set(lst)
        self.cbe.Refresh()
            
        
    ######################################################################################  
    def EvtComboEtab(self, evt):       
#        if evt.GetSelection() == len(constantes.ETABLISSEMENTS_PDD):
#            self.classe.etablissement = self.textctrl.GetStringSelection()
#            self.AfficherAutre(True)
#        else:
        self.classe.etablissement = evt.GetString()
#        self.AfficherAutre(False)
        
        self.sendEvent()
     

    ######################################################################################  
    def EvtListBoxSyst(self, event = None):
        if event != None:
            n = event.GetSelection()
        else:
            n = 0
        if len(self.classe.systemes) > n:
#            s = self.classe.systemes[n]
            self.panelSys.SetSysteme(self.classe.systemes[n])
            
#            self.panelSys.systeme.setBranche(s.getBranche())


    ######################################################################################  
    def EvtButtonSyst(self, event = None):
#        print "EvtButtonSyst"
#        print self.classe.systemes
#        print self.panelSys.systeme
#        for n, s in enumerate(self.classe.systemes):
#            if s.nom == self.panelSys.systeme.nom:
##                print "  ---", n, s
#                self.classe.systemes.remove(s)
#                self.lstSys.Delete(n)
#                break

#        s = self.panelSys.systeme.Copie()
        s = Systeme(self.classe, None)
#        print "   +++", s
        self.lstSys.Append(s.nom)
        self.classe.systemes.append(s)
        self.classe.systemes.sort(key=attrgetter('nom'))
        self.lstSys.SetSelection(0)
        self.EvtListBoxSyst()
#        print "   >>>",self.classe.systemes


    ######################################################################################  
    def MiseAJourListeSys(self, nom = u""):
#        print "MiseAJourListeSys", nom, self.lstSys.GetSelection()
        if nom == u"":
            nom = u"Système sans nom"
            
        n = self.lstSys.GetSelection()
        if n != wx.NOT_FOUND:
            self.lstSys.SetString(n, nom)
            self.lstSys.SetSelection(self.lstSys.FindString(nom))


    ######################################################################################  
    def EvtRadioBox(self, event = None, CodeFam = None):
        """ Sélection d'un type d'enseignement
        """
        if event != None:
            radio_selected = event.GetEventObject()
            CodeFam = Referentiel.getEnseignementLabel(radio_selected.GetLabel())
        
        
#        fam = self.classe.familleEnseignement
        ancienRef = self.classe.referentiel
        ancienneFam = self.classe.familleEnseignement
        self.classe.typeEnseignement, self.classe.familleEnseignement = CodeFam
        self.classe.referentiel = REFERENTIELS[self.classe.typeEnseignement]
        
#        for c, e in [r.Enseignement[1:] for r in REFERENTIELS]constantes.Enseignement.items():
#            if e[0] == :
#                self.classe.typeEnseignement = c
#                self.classe.familleEnseignement = constantes.FamilleEnseignement[self.classe.typeEnseignement]
#                break
        
        self.classe.MiseAJourTypeEnseignement()
        self.classe.doc.MiseAJourTypeEnseignement(ancienRef, ancienneFam)
#        self.classe.doc.MiseAJourTypeEnseignement(fam != self.classe.familleEnseignement)
#        self.MiseAJourType()
#        if hasattr(self, 'list'):
#            self.list.Peupler()

        self.st_type.SetLabel(self.classe.referentiel.Enseignement[0])
        self.SetLienBO()
        
        self.Refresh()
        
        self.sendEvent()
        
    ######################################################################################  
    def SetLienBO(self):
        for b in self.bo:
            b.Destroy()
            
        self.bo = []
        for tit, url in REFERENTIELS[self.classe.typeEnseignement].BO_URL:
            self.bo.append(hl.HyperLinkCtrl(self.pageGen, wx.ID_ANY, tit, URL = url))
            self.sbBO.Add(self.bo[-1], flag = wx.EXPAND)
            self.bo[-1].Show(tit != u"")
            self.bo[-1].ToolTip.SetTip(url)
            
        self.pageGen.sizer.Layout()
        

        
    ######################################################################################  
    def MiseAJour(self):
#        print "MiseAJour panelPropriete classe"
#        self.MiseAJourType()
        
        self.cb_type.SetStringSelection(self.classe.referentiel.Enseignement[0])
        self.st_type.SetLabel(self.classe.referentiel.Enseignement[0])
#        self.cb_type.SetStringSelection(REFERENTIELS[self.classe.typeEnseignement].Enseignement[0])
        
        
        self.cba.SetValue(self.classe.academie)
        self.EvtComboAcad()
        self.cbv.SetValue(self.classe.ville)
        self.EvtComboVille()
        self.cbe.SetValue(self.classe.etablissement)
        
#        print "   ", self.classe.systemes
        
        self.lstSys.Set([])
        
        if len(self.classe.systemes) == 0:
            # On crée un système vide
            self.EvtButtonSyst()
#            print "   +++", self.classe.systemes
            self.EvtListBoxSyst()
            self.MiseAJourListeSys()
        else:
            self.lstSys.Set([s.nom for s in self.classe.systemes])
            self.lstSys.SetSelection(0)
            self.EvtListBoxSyst()
#        self.MiseAJourListeSys()
#        if self.cbe.GetStringSelection () and self.cbe.GetStringSelection() == self.classe.etablissement:
#            self.textctrl.ChangeValue(u"")
#            self.AfficherAutre(False)
            
#        else:
#            self.textctrl.ChangeValue(self.classe.etablissement)
#            self.AfficherAutre(True)
#            self.cbe.SetSelection(len(constantes.ETABLISSEMENTS))
        
        self.SetLienBO()
        
#        if hasattr(self, 'list'):
#            self.list.Peupler()
                
        self.ec.MiseAJour()

            
    #############################################################################            
    def OnAide(self, event):
        dlg = MessageAideCI(self)
        dlg.ShowModal()
        dlg.Destroy()

        
    ######################################################################################  
    def Verrouiller(self, etat):
        self.cb_type.Show(etat)
        self.st_type.Show(not etat)
        self.pasVerrouille = etat

        
    
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
                                  CT.TR_AUTO_CHECK_PARENT|CT.TR_AUTO_TOGGLE_CHILD|\
                                  CT.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.Unbind(wx.EVT_KEY_DOWN)
        self.panelParent = panelParent
#        self.SetBackgroundColour(wx.WHITE)
        self.SetToolTip(wx.ToolTip(u"Choisir le type d'enseignement"))
        
        self.AddColumn(u"")
        self.SetMainColumn(0)
        self.root = self.AddRoot("r")
        self.Construire(self.root)
        self.ExpandAll()
        
#        wx.CallAfter(self.ExpandAll)
        
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
#        print "Construire ArbreTypeEnseignement"
        self.branche = []
        self.ExpandAll()
        for t, st in ARBRE_REF.items():
            if t[0] == "_":
                branche = self.AppendItem(racine, REFERENTIELS[st[0]].Enseignement[2])
            else:
                branche = self.AppendItem(racine, u"")#, ct_type=2)#, image = self.arbre.images["Seq"])
                rb = wx.RadioButton(self, -1, REFERENTIELS[t].Enseignement[0])
                self.Bind(wx.EVT_RADIOBUTTON, self.panelParent.EvtRadioBox, rb)
                self.SetItemWindow(branche, rb)
                rb.SetToolTipString(REFERENTIELS[t].Enseignement[1])
                rb.Enable(len(REFERENTIELS[t].projets) > 0 or not self.panelParent.pourProjet)
                self.branche.append(branche)
            for sst in st:
                sbranche = self.AppendItem(branche, u"")#, ct_type=2)
                rb = wx.RadioButton(self, -1, REFERENTIELS[sst].Enseignement[0])
                self.Bind(wx.EVT_RADIOBUTTON, self.panelParent.EvtRadioBox, rb)
                self.SetItemWindow(sbranche, rb)
                rb.SetToolTipString(REFERENTIELS[sst].Enseignement[1])
                rb.Enable(len(REFERENTIELS[sst].projets) > 0 or not self.panelParent.pourProjet)
                self.branche.append(sbranche)
#        self.Layout()
    
    ######################################################################################              
    def SetStringSelection(self, label):
        for rb in self.branche:
            if isinstance(rb.GetWindow(), wx.RadioButton) and label == rb.GetWindow().GetLabel():
                rb.GetWindow().SetValue(True)
          
                

#class ListeCI(ULC.UltimateListCtrl):
#    def __init__(self, parent, classe):
#        
#        self.typeEnseignement = classe.typeEnseignement
#        self.classe = classe
#        self.parent = parent
#        
#        style = wx.LC_REPORT| wx.BORDER_NONE| wx.LC_VRULES| wx.LC_HRULES| ULC.ULC_HAS_VARIABLE_ROW_HEIGHT
#        if not REFERENTIELS[self.typeEnseignement].CI_cible:
#            style = style |wx.LC_NO_HEADER
#            
#        ULC.UltimateListCtrl.__init__(self,parent, -1, 
#                                        agwStyle=style)
#                
#        info = ULC.UltimateListItem()
#        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT
#        info._format = wx.LIST_FORMAT_LEFT
#        info._text = u"CI"
#         
#        self.InsertColumnInfo(0, info)
#
#        info = ULC.UltimateListItem()
#        info._format = wx.LIST_FORMAT_LEFT
#        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_FONT
#        info._text = u"Intitulé"
#        
#        self.InsertColumnInfo(1, info)
#        
#        self.SetColumnWidth(0, 35)
#        self.SetColumnWidth(1, -3)
#        
#        if REFERENTIELS[self.typeEnseignement].CI_cible:
#            for i,p in enumerate(['M', 'E', 'I', 'F', 'S', 'C']):
#                info = ULC.UltimateListItem()
#                info._mask = wx.LIST_MASK_TEXT
#                info._format = wx.LIST_FORMAT_CENTER
#                info._text = p
#                
#                self.InsertColumnInfo(i+2, info)
#                self.SetColumnWidth(i+2, 20)
#        
#        self.Peupler()
#                
#    ######################################################################################  
#    def Peupler(self):
##        print "PeuplerListe"
#        # Peuplement de la liste
#        self.DeleteAllItems()
#        l = self.classe.CI
#        
##        if self.typeEnseignement != "SSI":
##            l = self.classe.ci_ET
##        else:
##            l = self.classe.ci_SSI
#            
#        for i,ci in enumerate(l):
#            index = self.InsertStringItem(sys.maxint, "CI"+str(i+1))
#            self.SetStringItem(index, 1, ci)
#           
#            if REFERENTIELS[self.typeEnseignement].CI_cible:
#                for j,p in enumerate(['M', 'E', 'I', 'F', 'S', 'C']):
#                    item = self.GetItem(i, j+2)
#                    cb = wx.CheckBox(self, 100+i, u"", name = p)
#                    cb.SetValue(p in self.classe.posCI[i])
#                    self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
#                    item.SetWindow(cb)
#                    self.SetItem(item)
#        self.Update()
#        
#    ######################################################################################  
#    def EvtCheckBox(self, event):
#        self.parent.EvtCheckBox(event)
    
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
            
        #
        # Cas où les CI sont sur une cible MEI
        #
        abrevCI = self.CI.parent.classe.referentiel.abrevCI
        if self.CI.GetReferentiel().CI_cible:
            self.panel_cible = Panel_Cible(self, self.CI)
            self.sizer.Add(self.panel_cible, (0,0), (2,1), flag = wx.EXPAND)
            
            self.grid1 = wx.FlexGridSizer( 0, 3, 0, 0 )
            self.grid1.AddGrowableCol(1)
            
            
#            for i, ci in enumerate(constantes.CentresInterets[self.CI.GetTypeEnseignement()]):
            for i, ci in enumerate(self.CI.parent.classe.referentiel.CentresInterets):
                r = wx.CheckBox(self, 200+i, "")
                t = wx.StaticText(self, -1, abrevCI+str(i+1)+" : "+ci)
                p = wx.TextCtrl(self, -1, u"1")
                p.SetToolTipString(u"Poids horaire relatif du "+abrevCI)
                p.Show(False)
                p.SetMinSize((30, -1))
                self.group_ctrls.append((r, t, p))
                self.grid1.Add( r, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
                self.grid1.Add( t, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.EXPAND, 5 )
                self.grid1.Add( p, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT, 5 )
            for radio, text, poids in self.group_ctrls:
                self.Bind(wx.EVT_CHECKBOX, self.OnCheck, radio )
                self.Bind(wx.EVT_TEXT, self.OnPoids, poids )
            self.sizer.Add(self.grid1, (0,1), (2,1), flag = wx.EXPAND)
            
            aide = wx.BitmapButton(self, -1, images.Bouton_Aide.GetBitmap())
            aide.SetToolTipString(u"Informations à propos de la cible "+abrevCI)
            self.sizer.Add(aide, (0,2), flag = wx.ALL, border = 2)
            self.Bind(wx.EVT_BUTTON, self.OnAide, aide )
            
            b = wx.ToggleButton(self, -1, "")
            b.SetValue(self.CI.max2CI)
            b.SetBitmap(images.Bouton_2CI.GetBitmap())
            b.SetToolTipString(u"Limite à 2 le nombre de "+abrevCI+" sélectionnables")
            self.sizer.Add(b, (1,2), flag = wx.ALL, border = 2)
#            b.SetSize((30,30)) # adjust default size for the bitmap
            b.SetInitialSize((32,32))
            self.b2CI = b
            self.Bind(wx.EVT_TOGGLEBUTTON, self.OnOption, b)
            if not self.sizer.IsColGrowable(1):
                self.sizer.AddGrowableCol(1)
            self.sizer.Layout()
        
        #
        # Cas où les CI ne sont pas sur une cible
        #  
        else:
            
            self.grid1 = wx.FlexGridSizer( 0, 2, 0, 0 )
            
            for i, ci in enumerate(self.CI.parent.classe.referentiel.CentresInterets):
    #            if i == 0 : s = wx.RB_GROUP
    #            else: s = 0
                r = wx.CheckBox(self, 200+i, abrevCI+str(i+1), style = wx.RB_GROUP )
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
    def OnPoids(self, event):
        pass
    
    #############################################################################            
    def OnCheck(self, event):
        button_selected = event.GetEventObject().GetId()-200 
        
        if event.GetEventObject().IsChecked():
            self.CI.AddNum(button_selected)
        else:
            self.CI.DelNum(button_selected)
        
        if len(self.group_ctrls[button_selected]) > 2:
            self.group_ctrls[button_selected][2].Show(event.GetEventObject().IsChecked())
        
#        self.panel_cible.bouton[button_selected].SetState(event.GetEventObject().IsChecked())
#        if self.CI.GetTypeEnseignement() == 'ET':
        if self.CI.GetReferentiel().CI_cible:
            self.panel_cible.GererBoutons(True)
        
            if hasattr(self, 'b2CI'):
                self.b2CI.Enable(len(self.CI.numCI) <= 2)
            
        self.Layout()
        self.sendEvent()
    
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        if self.CI.GetTypeEnseignement() == 'ET':
        if self.CI.GetReferentiel().CI_cible:
            self.panel_cible.GererBoutons(True)
            if hasattr(self, 'b2CI'):
                self.b2CI.Enable(len(self.CI.numCI) <= 2)
        
        else:
            for i, num in enumerate(self.CI.numCI):
                self.group_ctrls[num][0].SetValue(True)
                if len(self.group_ctrls[num]) > 2:
                    self.group_ctrls[num][2].SetValue(self.CI.poids[i])
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
        
        self.nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
        pageComp = wx.Panel(self.nb, -1)
        bg_color = self.Parent.GetBackgroundColour()
        pageComp.SetBackgroundColour(bg_color)
        self.pageComp = pageComp   
        pageCompsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        

        pageComp.SetSizer(pageCompsizer)
            
        ref = self.competence.GetReferentiel()
        
#        self.DestroyChildren()
#        if hasattr(self, 'arbre'):
#            self.sizer.Remove(self.arbre)
        self.arbre = ArbreCompetences(self.pageComp, ref, self)
        pageCompsizer.Add(self.arbre, 1, flag = wx.EXPAND)
#        self.pageComp.sizer.Add(self.arbre, (0,0), flag = wx.EXPAND)
#        if not self.pageComp.sizer.IsColGrowable(0):
#            self.pageComp.sizer.AddGrowableCol(0)
#        if not self.pageComp.sizer.IsRowGrowable(0):
#            self.pageComp.sizer.AddGrowableRow(0)
#        self.pageComp.Layout()
        
        self.nb.AddPage(pageComp, ref.nomCompetences) 
        
        if (len(ref.dicFonctions) > 0):
            #
            # La page "Fonctions"
            #
            pageFct = wx.Panel(self.nb, -1)
            self.pageFct = pageFct
            pageFctsizer = wx.BoxSizer(wx.HORIZONTAL)

            self.arbreFct = ArbreFonctionsPrj(pageFct, ref, self)
            pageFctsizer.Add(self.arbreFct, 1, flag = wx.EXPAND)

            pageFct.SetSizer(pageFctsizer)
            self.nb.AddPage(pageFct, ref.nomFonctions) 

            self.pageFctsizer = pageFctsizer
        
        self.sizer.Add(self.nb, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        
        self.Layout()
        
    #############################################################################            
    def GetDocument(self):
        return self.competence.parent
    
#    ######################################################################################  
#    def construire(self):
#        ref = self.competence.GetReferentiel()
#        
#        self.DestroyChildren()
##        if hasattr(self, 'arbre'):
##            self.sizer.Remove(self.arbre)
#        self.arbre = ArbreCompetences(self.pageComp, ref)
#        self.pageComp.sizer.Add(self.arbre, (0,0), flag = wx.EXPAND)
#        if not self.pageComp.sizer.IsColGrowable(0):
#            self.pageComp.sizer.AddGrowableCol(0)
#        if not self.pageComp.sizer.IsRowGrowable(0):
#            self.pageComp.sizer.AddGrowableRow(0)
#        self.pageComp.Layout()
#        
#        self.nb.AddPage(pageComp, ref.nomFonctions) 
#        
#        if (len(ref.dicFonctions) > 0):
#            #
#            # La page "Fonctions"
#            #
#            pageFct = wx.Panel(self.nb, -1)
#            self.pageFct = pageFct
#            pageFctsizer = wx.BoxSizer(wx.HORIZONTAL)
#
#            self.arbreFct = ArbreFonctionsPrj(pageFct, ref, self)
#            pageFctsizer.Add(self.arbreFct, 1, flag = wx.EXPAND)
#
#            pageFct.SetSizer(pageFctsizer)
#            self.nb.AddPage(pageFct, ref.nomFonctions) 
#
#            self.pageFctsizer = pageFctsizer
                
                
        

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
        self.competence.parent.Verrouiller()
        self.sendEvent()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "MiseAJour compétences"
#        print "  ", self.arbre.items.keys()
#        print "   ", self.competence.competences
        self.arbre.UnselectAll()
        for s in self.competence.competences:
            if s in self.arbre.items.keys():
                self.arbre.CheckItem2(self.arbre.items[s])
                    
                    
        
        
        
#        for s in self.competence.competences:
#            
#            i = self.arbre.get_item_by_label(s, self.arbre.GetRootItem())
#            print s, 
#            print i, i.IsOk()
#            if i.IsOk():
#                self.arbre.CheckItem2(i)
        
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
        
        self.nb = wx.Notebook(self, -1,  style= wx.BK_DEFAULT)
        
        # Liste des numéros de pages attribués à
        # 0 : savoirs spécifiques de l'enseignement
        # 1 : savoirs d'un éventuel tronc commun
        # 2 : Math
        # 3 : Phys
        self.lstPages = [0,1,2,3]
        
        
        self.pageSavoir     = self.CreerPage()
        self.pageSavoirSpe  = self.CreerPage()
        self.pageSavoirM    = self.CreerPage()
        self.pageSavoirP    = self.CreerPage()
        
#        # Savoirs
#        pageSavoir = PanelPropriete(nb)
#        pageSavoir.SetBackgroundColour(bg_color)
#        self.pageSavoir = pageSavoir
#        nb.AddPage(pageSavoir, u"")
#        
#        
#        # Savoirs autres
#        ref = self.GetDocument().GetReferentiel()
#        if (prerequis and ref.preSavoirs_Math) or (not prerequis and ref.objSavoirs_Math):
#            # Savoirs Maths
#            pageSavoirM = PanelPropriete(nb)
#            pageSavoirM.SetBackgroundColour(bg_color)
#            self.pageSavoirM = pageSavoirM
#            nb.AddPage(pageSavoirM, self.GetDocument().GetReferentiel().nomSavoirs_Math)
#            self.lstPages[2] = nb.GetPageCount()-1
#            print "page Math" , self.lstPages[2]
#            
#        if (prerequis and ref.preSavoirs_Phys) or (not prerequis and ref.objSavoirs_Phys):
#            # Savoirs Physique
#            pageSavoirP = PanelPropriete(nb)
#            pageSavoirP.SetBackgroundColour(bg_color)
#            self.pageSavoirP = pageSavoirP
#            nb.AddPage(pageSavoirP, self.GetDocument().GetReferentiel().nomSavoirs_Phys)
#            self.lstPages[3] = nb.GetPageCount()-1
#            print "page Phys" , self.lstPages[3]
            
        self.sizer.Add(self.nb, (0,1), (2,1), flag = wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND, border = 1)
        
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(1)
            
        self.MiseAJourTypeEnseignement()

        
    #############################################################################            
    def GetDocument(self):
        return self.savoirs.parent
        
        
    ######################################################################################  
    def CreerPage(self):
        bg_color = self.Parent.GetBackgroundColour()
        page = PanelPropriete(self.nb)
        page.SetBackgroundColour(bg_color)
        self.nb.AddPage(page, u"")
        return page
        
        
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
            
        ref = self.GetDocument().GetReferentiel()
        if ref.tr_com != []:
            # Il y a un tronc comun (Spécialité STI2D par exemple)
            self.pageSavoirSpe.DestroyChildren()
            self.arbreSpe = ArbreSavoirs(self.pageSavoirSpe, "S", self.savoirs, self.prerequis)
            self.pageSavoirSpe.sizer.Add(self.arbreSpe, (0,0), flag = wx.EXPAND)
            if not self.pageSavoirSpe.sizer.IsColGrowable(0):
                self.pageSavoirSpe.sizer.AddGrowableCol(0)
            if not self.pageSavoirSpe.sizer.IsRowGrowable(0):
                self.pageSavoirSpe.sizer.AddGrowableRow(0)
            self.pageSavoirSpe.Layout()
            
        if (self.prerequis and ref.preSavoirs_Math) or (not self.prerequis and ref.objSavoirs_Math):
            # Savoirs Math
            self.pageSavoirM.DestroyChildren()
            self.arbreM = ArbreSavoirs(self.pageSavoirM, "M", self.savoirs, self.prerequis)
            self.pageSavoirM.sizer.Add(self.arbreM, (0,0), flag = wx.EXPAND)
            if not self.pageSavoirM.sizer.IsColGrowable(0):
                self.pageSavoirM.sizer.AddGrowableCol(0)
            if not self.pageSavoirM.sizer.IsRowGrowable(0):
                self.pageSavoirM.sizer.AddGrowableRow(0)
            self.pageSavoirM.Layout()
            
        if (self.prerequis and ref.preSavoirs_Phys) or (not self.prerequis and ref.objSavoirs_Phys):
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
#        print " page Math" , self.lstPages[2]
#        print " page Phys" , self.lstPages[3]
    

    ######################################################################################  
    def SetSavoirs(self): 
        self.savoirs.parent.Verrouiller()
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
#            typ, cod = s[0], s[1:]
            typ = s[0]
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
        ref = self.GetDocument().GetReferentiel()
        
        # Il y a un tronc commun : 0 = TC - 1 = Spé
        if ref.tr_com != []:
            ref_tc = REFERENTIELS[ref.tr_com[0]]
            self.nb.SetPageText(0, ref_tc.nomSavoirs + " " + ref_tc.Code)
            if self.lstPages[1] == None:
                self.lstPages[1] = 1
                self.nb.InsertPage(self.lstPages[1], self.pageSavoirSpe, ref.nomSavoirs + " " + ref.Code)
                for i in range(2,4):
                    if self.lstPages[i] != None:
                        self.lstPages[i] += 1
            else:
                self.nb.SetPageText(self.lstPages[1], ref.nomSavoirs + " " + ref.Code)
        
        # Il n'y a pas de tronc commun : 0 = TC - 1 = rien
        else:
            if ref.surnomSavoirs != u"":
                t = ref.surnomSavoirs
            else:
                t = ref.nomSavoirs + " " + ref.Code
            self.nb.SetPageText(0, t)
            if self.lstPages[1] != None:
                self.nb.RemovePage(self.lstPages[1])
                self.lstPages[1] = None
                for i in range(2,4):
                    if self.lstPages[i] != None:
                        self.lstPages[i] -= 1
        
        # Il y a des maths
        if (self.prerequis and ref.preSavoirs_Math) or (not self.prerequis and ref.objSavoirs_Math):
            if self.lstPages[2] == None:
                if self.lstPages[1] != None:
                    self.lstPages[2] = self.lstPages[1] +1
                else:
                    self.lstPages[2] = self.lstPages[0] +1
                self.nb.InsertPage(self.lstPages[2], self.pageSavoirM, ref.nomSavoirs_Math)
                if self.lstPages[3] != None:
                    self.lstPages[3] += 1
            else:
                self.nb.SetPageText(self.lstPages[2], ref.nomSavoirs_Math)
        else:
            if self.lstPages[2] != None:
                self.nb.RemovePage(self.lstPages[2])
                self.lstPages[2]= None
                if self.lstPages[3] != None:
                    self.lstPages[3] -= 1
                    
        # Il y a de la physique
        if (self.prerequis and ref.preSavoirs_Phys) or (not self.prerequis and ref.objSavoirs_Phys):
            if self.lstPages[3] == None:
                if self.lstPages[2] != None:
                    self.lstPages[3] = self.lstPages[2] +1
                elif self.lstPages[1] != None:
                    self.lstPages[3] = self.lstPages[1] +1
                else:
                    self.lstPages[3] = self.lstPages[0] +1
                self.nb.InsertPage(self.lstPages[3], self.pageSavoirP, ref.nomSavoirs_Phys)
            else:
                self.nb.SetPageText(self.lstPages[3], ref.nomSavoirs_Phys)
        else:
            if self.lstPages[3] != None:
                self.nb.RemovePage(self.lstPages[3])
                self.lstPages[3]= None
        
        self.construire()
            
#############################################################################            
    def MiseAJourTypeEnseignement2(self):
#        print "MiseAJourTypeEnseignement Savoirs"
#        ref = REFERENTIELS[self.savoirs.GetTypeEnseignement()]
        ref = self.GetDocument().GetReferentiel()
        
        if ref.tr_com != []:
            ref_tc = REFERENTIELS[ref.tr_com[0]]
            self.nb.SetPageText(0, ref_tc.nomSavoirs + " " + ref_tc.Code)
            if not hasattr(self, 'pageSavoirSpe') or not isinstance(self.pageSavoirSpe, PanelPropriete):
                bg_color = self.Parent.GetBackgroundColour()
                pageSavoirSpe = PanelPropriete(self.nb)
                pageSavoirSpe.SetBackgroundColour(bg_color)
                self.pageSavoirSpe = pageSavoirSpe
                self.nb.InsertPage(self.lstPages[1], pageSavoirSpe, ref.nomSavoirs + ref.Code)
                for i in range(2,4):
                    self.lstPages[i] += 1
                    
        else:
            self.nb.SetPageText(0, ref.nomSavoirs + " " + ref.Code)
            if hasattr(self, 'pageSavoirSpe') and isinstance(self.pageSavoirSpe, PanelPropriete):
                self.nb.DeletePage(self.lstPages[1])
                for i in range(2,4):
                    self.lstPages[i] -= 1
        
        if (self.prerequis and ref.preSavoirs_Math) or (not self.prerequis and ref.objSavoirs_Math):
            if not hasattr(self, 'pageSavoirM') or not isinstance(self.pageSavoirM, PanelPropriete):
                bg_color = self.Parent.GetBackgroundColour()
                pageSavoirM = PanelPropriete(self.nb)
                pageSavoirM.SetBackgroundColour(bg_color)
                self.pageSavoirM = pageSavoirM
#                self.lstPages[2] = self.lstPages[1]+1
                self.nb.InsertPage(self.lstPages[2], pageSavoirM, ref.nomSavoirs_Math)
                self.lstPages[3] += 1
            else:
                self.nb.SetPageText(self.lstPages[2], ref.nomSavoirs_Math)
        else:
            if hasattr(self, 'pageSavoirM') and isinstance(self.pageSavoirM, PanelPropriete):
                self.nb.DeletePage(self.lstPages[2])
                self.lstPages[3] -= 1
                    
                    
        if (self.prerequis and ref.preSavoirs_Phys) or (not self.prerequis and ref.objSavoirs_Phys):
            if not hasattr(self, 'pageSavoirP') or not isinstance(self.pageSavoirP, PanelPropriete):
                bg_color = self.Parent.GetBackgroundColour()
                pageSavoirP = PanelPropriete(self.nb)
                pageSavoirP.SetBackgroundColour(bg_color)
                self.pageSavoirP = pageSavoirP
#                self.lstPages[3] = self.lstPages[2]+1
                print self.lstPages[3]
                self.nb.InsertPage(self.lstPages[3], pageSavoirP, ref.nomSavoirs_Phys)
            else:
                self.nb.SetPageText(self.lstPages[3], ref.nomSavoirs_Phys)
        else:
            if hasattr(self, 'pageSavoirP') and isinstance(self.pageSavoirP, PanelPropriete):
                self.nb.DeletePage(self.lstPages[3])
            

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
                                help = u"Nombre de rotations successives")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcNombreRot)
        self.vcNombreRot = vcNombreRot
        bsizer2.Add(vcNombreRot, flag = wx.EXPAND|wx.ALL, border = 2)
        
        self.sizer.Add(bsizer2, (0,2), (4,1), flag =wx.ALL|wx.EXPAND, border = 2)
        
        # Nombre de groupes
#        vcNombreGrp = VariableCtrl(self, seance.nbrGroupes, signeEgal = True, slider = False, sizeh = 30,
#                                help = u"Nombre de groupes occupés simultanément")
#        self.Bind(EVT_VAR_CTRL, self.EvtText, vcNombreRot)
#        self.vcNombreGrp = vcNombreGrp
#        bsizer2.Add(vcNombreGrp, flag = wx.EXPAND|wx.ALL, border = 2)
#        
#        self.sizer.Add(bsizer2, (0,2), (4,1), flag =wx.ALL|wx.EXPAND, border = 2)
        
        
        
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
#                print "   ", type(s), "---", s
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
        self.seance.parent.OrdonnerSeances()
        
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
#        print "AdapterAuType", self.seance
        #
        # Type de parent
        #
        ref = self.GetReferentiel()

        listType = self.seance.GetListeTypes()
        listTypeS = [(ref.seances[t][1], constantes.imagesSeance[t].GetBitmap()) for t in listType] 
        
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
        
        #
        # Effectif
        #
        if self.seance.typeSeance == "":
            listEff = []
        else:
            listEff = ref.effectifsSeance[self.seance.typeSeance]
#        print "  ", listEff
        
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
#        self.vcDuree.marquerValid(etat)
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.AdapterAuType()
        ref = self.GetReferentiel()
        if self.seance.typeSeance != "" and ref.seances[self.seance.typeSeance][1] in self.cbType.GetStrings():
            self.cbType.SetSelection(self.cbType.GetStrings().index(ref.seances[self.seance.typeSeance][1]))
        self.textctrl.ChangeValue(self.seance.intitule)
        self.vcDuree.mofifierValeursSsEvt()
        
        if self.cbEff.IsShown():#self.cbEff.IsEnabled() and 
            self.cbEff.SetSelection(ref.findEffectif(self.cbEff.GetStrings(), self.seance.effectif))
        
        if self.cbDem.IsShown():#self.cbDem.IsEnabled() and :
            self.cbDem.SetSelection(self.cbDem.GetStrings().index(ref.demarches[self.seance.demarche][1]))
            
        if self.seance.typeSeance in ["AP", "ED", "P"]:
            self.vcNombre.mofifierValeursSsEvt()
        elif self.seance.typeSeance == "R":
            self.vcNombreRot.mofifierValeursSsEvt()
        
        self.vcTaille.mofifierValeursSsEvt()
        
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
#        print "init pptache", tache
        if not tache.phase in [tache.projet.getCodeLastRevue(), _S]  \
           and not (tache.phase in TOUTES_REVUES_EVAL and tache.GetReferentiel().compImposees['C']):
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
        prj = self.tache.GetProjetRef()
#        lstPhases = [p[1] for k, p in ref.phases_prj.items() if not k in ref.listPhasesEval_prj]
        lstPhases = [prj.phases[k][1] for k in prj.listPhases if not k in prj.listPhasesEval]
        
        if tache.phase in TOUTES_REVUES_SOUT:
            titre = wx.StaticText(pageGen, -1, u"Phase : "+prj.phases[tache.phase][1])
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

            for i, k in enumerate(sorted([k for k in prj.phases.keys() if not k in prj.listPhasesEval])):#ref.listPhases_prj):
                cbPhas.SetItemBitmap(i, constantes.imagesTaches[k].GetBitmap())
            pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbPhas)
            self.cbPhas = cbPhas
            pageGen.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 5)
            pageGen.sizer.Add(cbPhas, (0,1), flag = wx.EXPAND|wx.ALL, border = 2)
        

        
        #
        # Intitulé de la tache
        #
        if not tache.phase in TOUTES_REVUES_EVAL_SOUT:
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
        if not tache.phase in TOUTES_REVUES_EVAL_SOUT:
            vcDuree = VariableCtrl(pageGen, tache.duree, coef = 0.5, signeEgal = True, slider = False,
                                   help = u"Volume horaire de la tâche en heures", sizeh = 60)
            pageGen.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
            self.vcDuree = vcDuree
            pageGen.sizer.Add(vcDuree, (2,0), (1, 2), flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        #
        # Elèves impliqués
        #
        if not tache.phase in TOUTES_REVUES_EVAL_SOUT:
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
        if tache.phase in TOUTES_REVUES_EVAL_SOUT:
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
        if not tache.phase in [tache.projet.getCodeLastRevue(), _S] \
           and not (tache.phase in TOUTES_REVUES_EVAL and tache.GetReferentiel().compImposees['C']):
            nb.AddPage(pageGen, u"Propriétés générales")

            #
            # La page "Compétences"
            #
            pageCom = wx.Panel(nb, -1)
            
            self.pageCom = pageCom
            pageComsizer = wx.BoxSizer(wx.HORIZONTAL)
            
            self.arbre = ArbreCompetencesPrj(pageCom, tache.GetReferentiel(), self,
                                             revue = self.tache.phase in TOUTES_REVUES_SOUT, 
                                             eleves = self.tache.phase in TOUTES_REVUES_EVAL_SOUT)
            pageComsizer.Add(self.arbre, 1, flag = wx.EXPAND)
        
            pageCom.SetSizer(pageComsizer)
            nb.AddPage(pageCom, tache.GetReferentiel().nomCompetences + u" à mobiliser") 
            
            self.pageComsizer = pageComsizer
            
#            if (len(tache.GetReferentiel().dicFonctions) > 0) and (not tache.phase in TOUTES_REVUES_EVAL_SOUT):
#                #
#                # La page "Fonctions"
#                #
#                pageFct = wx.Panel(nb, -1)
#                self.pageFct = pageFct
#                pageFctsizer = wx.BoxSizer(wx.HORIZONTAL)
#
#                self.arbreFct = ArbreFonctionsPrj(pageFct, tache.GetReferentiel(), self)
#                pageFctsizer.Add(self.arbreFct, 1, flag = wx.EXPAND)
#
#                pageFct.SetSizer(pageFctsizer)
#                nb.AddPage(pageFct, tache.GetReferentiel().nomFonctions) 
#
#                self.pageFctsizer = pageFctsizer
        
        
            self.sizer.Add(nb, (0,0), flag = wx.EXPAND)
            self.sizer.AddGrowableCol(0)
            self.sizer.AddGrowableRow(0)
        
        #
        # Mise en place
        #
        
        
        self.Layout()
        self.FitInside()
#        wx.CallAfter(self.PostSizeEvent)
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
                prj = self.tache.GetProjetRef()
                self.arbre.MiseAJour(competence, prj._dicCompetences_simple[competence][1])
#                self.arbre.MiseAJour(competence, REFERENTIELS[self.tache.GetTypeEnseignement()]._dicCompetences_prj_simple[competence][1])
            
            
        self.Thaw()
        
        
    ######################################################################################  
    def EvtCheckListBox(self, event):
        index = event.GetSelection()
        
        if self.competence in self.tache.indicateursEleve[0].keys():
            lst = self.tache.indicateursEleve[0][self.competence]
        else:
            prj = self.tache.GetProjetRef()
            lst = [self.competence in self.tache.competences]*len(prj.dicIndicateurs[self.competence])
#            lst = [self.competence in self.tache.competences]*len(REFERENTIELS[self.tache.GetTypeEnseignement()].dicIndicateurs_prj[self.competence])
            
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
#        print "AjouterCompetence !!", self, code
        if not code in self.tache.indicateursEleve[0]:
            self.tache.indicateursEleve[0].append(code)
        
        if propag:
            for i in range(len(self.tache.projet.eleves)):
                self.AjouterCompetenceEleve(code, i+1)
        
        self.tache.projet.SetCompetencesRevuesSoutenance()
        
        
    ######################################################################################  
    def EnleverCompetence(self, code, propag = True):
#        print "EnleverCompetence", self, code
        if code in self.tache.indicateursEleve[0]:
            self.tache.indicateursEleve[0].remove(code)
        # on recommence : pour corriger un bug
        if code in self.tache.indicateursEleve[0]:
            self.tache.indicateursEleve[0].remove(code)
        
        if propag:
            for i in range(len(self.tache.projet.eleves)):
                self.EnleverCompetenceEleve(code, i+1)
    
        self.tache.projet.SetCompetencesRevuesSoutenance()
    
    
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
        wx.CallAfter(self.sendEvent)
        self.tache.projet.Verrouiller()
        
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
            
        # On reconstruit l'arbre pour ajouter/enlever des cases "élève"
        if hasattr(self, 'arbre') and self.arbre.eleves:
            self.arbre.ConstruireCasesEleve()
        
        
    #############################################################################            
    def MiseAJourListeEleves(self):
        """ Met à jour la liste des élèves
        """
        if not self.tache.phase in TOUTES_REVUES_EVAL_SOUT:
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
        if not self.tache.phase in TOUTES_REVUES_EVAL_SOUT:
            for i in range(len(self.GetDocument().eleves)):
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
        self.GetDocument().MiseAJourTachesEleves()
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
        ref = self.tache.GetProjetRef()
        newPhase = ref.getClefDic('phases', self.cbPhas.GetStringSelection(), 1)
#        print "   ", newPhase
#        newPhase = get_key(self.GetReferentiel().NOM_PHASE_TACHE[self.tache.GetTypeEnseignement(True)], 
#                                        self.cbPhas.GetStringSelection())
        if self.tache.phase != newPhase:
            if newPhase == "Rev":
                self.tache.SetDuree(0)
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
    def MiseAJourCases(self):
#        print "MiseAJourCases", self.tache.phase, self.tache.intitule
        if hasattr(self, 'arbre'):
            self.arbre.UnselectAll()
            
            for codeIndic in self.tache.indicateursEleve[0]:
                if codeIndic in self.arbre.items.keys():
                    item = self.arbre.items[codeIndic]
                    cases = self.arbre.GetItemWindow(item, 3)
                    cases.MiseAJour()
                    cases.Actualiser()
                  
            
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "MiseAJour", self.tache.phase, self.tache.intitule
        if hasattr(self, 'arbre'):
            self.arbre.UnselectAll()
            
            for codeIndic in self.tache.indicateursEleve[0]:
                if codeIndic in self.arbre.items.keys():
                    item = self.arbre.items[codeIndic]
                    self.arbre.CheckItem2(item)

            
        if hasattr(self, 'textctrl'):
            self.textctrl.SetValue(self.tache.intitule)
        
        if hasattr(self, 'cbPhas') and self.tache.phase != '':
            self.cbPhas.SetStringSelection(self.tache.GetProjetRef().phases[self.tache.phase][1])
            
        if sendEvt:
            self.sendEvent()
        
        
    #############################################################################
    def MiseAJourTypeEnseignement(self, ref):
        if self.tache.phase in TOUTES_REVUES_EVAL and self.tache.GetReferentiel().compImposees['C']:
            pass
        else:
            if hasattr(self, 'arbre'):
                self.arbre.MiseAJourTypeEnseignement(ref)
            if hasattr(self, 'arbreFct'):
                self.arbreFct.MiseAJourTypeEnseignement(ref)
        
        
####################################################################################
#
#   Classe définissant le panel de propriété d'un système
#
####################################################################################
class PanelPropriete_Systeme(PanelPropriete):
    def __init__(self, parent, systeme):
#        print "init", parent
        self.systeme = systeme
        self.parent = parent
        
        PanelPropriete.__init__(self, parent)
        
        if isinstance(systeme.parent, Sequence):
            self.cbListSys = wx.ComboBox(self, -1, u"",
                                         choices = [u""],
                                         style = wx.CB_DROPDOWN
                                         | wx.TE_PROCESS_ENTER
                                         | wx.CB_READONLY
                                         #| wx.CB_SORT
                                         )
            self.MiseAJourListeSys()
            self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.cbListSys)
            self.sizer.Add(self.cbListSys, (0,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT|wx.EXPAND, border = 3)
            
        #
        # Nom
        #
        titre = wx.StaticText(self, -1, u"Nom du système :")
        textctrl = wx.TextCtrl(self, -1, u"")
        self.textctrl = textctrl
        
        self.sizer.Add(titre, (0,0), (1,1), flag = wx.ALIGN_TOP|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)
        self.sizer.Add(textctrl, (1,0), (1,2),  flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        
        #
        # Nombre de systèmes disponibles en parallèle
        #
        vcNombre = VariableCtrl(self, systeme.nbrDispo, signeEgal = True, slider = False, 
                                help = u"Nombre de d'exemplaires de ce système disponibles simultanément.")
        self.Bind(EVT_VAR_CTRL, self.EvtVar, vcNombre)
        self.vcNombre = vcNombre
        self.sizer.Add(vcNombre, (2,0), (1, 2), flag = wx.TOP|wx.BOTTOM, border = 3)
        
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
        self.sizer.Add(bsizer, (0,2), (3,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        self.btImg = bt
        
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
        self.sizer.Add(bsizer, (0,3), (3, 1), flag = wx.EXPAND|wx.TOP|wx.LEFT, border = 2)
        
        self.sizer.AddGrowableCol(3)
#        self.sizer.AddGrowableRow(1)
        self.sizer.Layout()
        
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        self.selec.SetPathSeq(pathSeq)
        
        
    ######################################################################################  
    def OnPathModified(self, lien, marquerModifier = True):
#        print "OnPathModified", self.systeme.lien.path, lien.path
        self.systeme.OnPathModified()
        self.systeme.propagerChangements()
        self.btnlien.Show(self.systeme.lien.path != "")
        self.Layout()
        self.Refresh()


    #############################################################################            
    def GetDocument(self):
        if isinstance(self.systeme.parent, Sequence):
            return self.systeme.parent
        elif isinstance(self.systeme.parent, Classe):
            return self.systeme.parent.GetDocument()
    
    
    #############################################################################            
    def EvtComboBox(self, evt):
        sel = evt.GetSelection()
        if sel > 0:
            s = self.systeme.parent.classe.systemes[sel-1]
            self.systeme.setBranche(s.getBranche())
            self.systeme.lienClasse = s
            self.Verrouiller(False)
        else:
            self.systeme.lienClasse = None
            self.Verrouiller(True)
        
        self.systeme.SetNom(evt.GetString())
        if isinstance(self.systeme.parent, Sequence):
            self.systeme.parent.MiseAJourNomsSystemes()
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent)
                self.eventAttente = True


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
#        print "SetImage", self.systeme
        if self.systeme.image != None:
            w, h = self.systeme.image.GetSize()
            wf, hf = 200.0, 100.0
            r = max(w/wf, h/hf)
            _w, _h = w/r, h/r
            self.systeme.image = self.systeme.image.ConvertToImage().Scale(_w, _h).ConvertToBitmap()
            self.image.SetBitmap(self.systeme.image)
        else:
#            print "NullBitmap"
            self.image.SetBitmap(wx.NullBitmap)
            
        self.systeme.SetImage()
        self.Layout()
        
        
    #############################################################################            
    def EvtText(self, event):
        self.systeme.SetNom(event.GetString())
        
        if isinstance(self.systeme.parent, Sequence):
            self.systeme.parent.MiseAJourNomsSystemes()
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent)
                self.eventAttente = True
        elif isinstance(self.systeme.parent, Classe):
#            print "  ***", self.systeme.parent
            self.systeme.parent.panelPropriete.MiseAJourListeSys(self.systeme.nom)


    #############################################################################            
    def EvtVar(self, event):
        self.systeme.SetNombre()
        
        if isinstance(self.systeme.parent, Sequence):
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent)
                self.eventAttente = True


    #############################################################################            
    def Verrouiller(self, etat = True):
        self.textctrl.Show(etat)
        self.vcNombre.Enable(etat)
        self.selec.Enable(etat)
#        self.btnlien.Enable(etat)
        self.btImg.Enable(etat)
        self.sizer.Layout()
    
    
    #############################################################################            
    def SetSysteme(self, s):
        self.systeme = s
        self.vcNombre.SetVariable(s.nbrDispo)
        self.selec.lien = s.lien
        self.MiseAJour()
    
    
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        """
        """
#        print "MiseAJour", self.systeme
            
        self.textctrl.ChangeValue(self.systeme.nom)
        self.vcNombre.mofifierValeursSsEvt()
        
        self.SetImage()
        
        if isinstance(self.systeme.parent, Sequence):
            if sendEvt:
                self.sendEvent()
        
        self.MiseAJourLien()
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(self.systeme.lien.path)
        self.btnlien.Show(self.systeme.lien.path != "")
        self.Layout()


    #############################################################################            
    def MiseAJourListeSys(self, nom = None):
        self.cbListSys.Set([u""]+[s.nom for s in self.systeme.parent.classe.systemes])
        if nom != None:
            self.cbListSys.SetSelection(self.cbListSys.FindString(nom))




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
            for k in self.personne.grille.keys():
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
                for sg in self.SelectGrille.values():
                    self.bsizer.Detach(sg)
                    sg.Destroy()
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
        titre = wx.StaticText(self, -1, eleve.GetProjetRef().parties[codeGrille])
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
        
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        
    ######################################################################################################
    def OnEnter(self, event):
        self.SetFocus()
        event.Skip()
        
    
    ###############################################################################################
    def OnKey(self, evt):
        keycode = evt.GetKeyCode()
        item = self.GetSelection()
        
        if keycode == wx.WXK_DELETE:
            self.doc.SupprimerItem(item)
            
        elif evt.ControlDown() and keycode == 67: # Crtl-C
            self.GetItemPyData(item).CopyToClipBoard()


        elif evt.ControlDown() and keycode == 86: # Crtl-V
            self.doc.CollerElem(item = item)
            
        evt.Skip()


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

        self.panelProp.AfficherPanel(panelPropriete)
#        panelPropriete.Refresh()
        self.parent.Refresh()
        
        if hasattr(self.classe.doc.GetApp(), 'fiche') and self.classe.doc.centrer:
            self.classe.doc.GetApp().fiche.CentrerSur(data)
        self.classe.doc.centrer = True
        
        event.Skip()
        
    ####################################################################################
    def OnBeginDrag(self, event):
        self.itemDrag = event.GetItem()
#        print self.GetItemPyData(self.itemDrag).GetNiveau(), 
#        print self.GetItemPyData(self.itemDrag).GetProfondeur()
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
        self.doc = sequence
        
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

#        self.CurseurInsert = wx.CursorFromImage(constantes.images.CurseurInsert.GetImage())
        self.CurseurInsertApres = wx.CursorFromImage(constantes.images.Curseur_InsererApres.GetImage())
        self.CurseurInsertDans = wx.CursorFromImage(constantes.images.Curseur_InsererDans.GetImage())
        

            
        
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
                if isinstance(dataTarget, PanelPropriete_Racine):
                    dataTarget = self.sequence
                dataSource = self.GetItemPyData(self.itemDrag)
                a = self.getActionDnD(dataSource, dataTarget)
                if a == 0:
                    self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
                elif a == 1:
                    self.SetCursor(self.CurseurInsertDans)
                elif a == 2 or a == 3 or a == 4:
                    self.SetCursor(self.CurseurInsertApres)

                    
#                if not isinstance(dataSource, Seance):
#                    self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
#                else:
#                    # Première place !
#                    if not isinstance(dataTarget, Seance):
#                        if dataTarget == self.sequence.panelSeances:
#                            self.SetCursor(self.CurseurInsertApres)
#                        else:
#                            self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
#                            
#                    # Autres séances
#                    else:
#                        if dataTarget != dataSource:# and dataTarget.parent == dataSource.parent:
#                            if dataTarget.parent == dataSource.parent or not dataTarget.typeSeance in ["R","S"]:
#                                self.SetCursor(self.CurseurInsertApres)
#                            else:
#                                self.SetCursor(self.CurseurInsertDans)
#                        else:
#                            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
                        
        event.Skip()
        
    ####################################################################################
    def getActionDnD(self, dataSource, dataTarget):
        """ Renvoie un code indiquant l'action à réaliser en cas de EnDrag :
                0 : rien
                1 : 
                2 : 
                3 : 
        """
        if isinstance(dataSource, Seance) and dataTarget != dataSource:
            if not hasattr(dataTarget, 'GetNiveau') or dataTarget.GetNiveau() + dataSource.GetProfondeur() > 2:
#                print "0.1"
                return 0


            # Insérer "dans"  (racine ou "R" ou "S")  .panelSeances
            if dataTarget == self.sequence \
               or (isinstance(dataTarget, Seance) and dataTarget.typeSeance in ["R","S"]):
                if not dataSource in dataTarget.seances:    # parents différents
#                    print dataSource.typeSeance, dataTarget.seances[0].GetListeTypes()
                    if dataTarget.GetNiveau() + dataSource.GetProfondeur() > 1:
#                        print "0-2"
                        return 0
                    elif not dataSource.typeSeance in dataTarget.seances[0].GetListeTypes():
#                        print "0-3"
                        return 0
                    else:
#                        print "1"
                        return 1
                else:
#                    print "2"
                    return 2
            
            # Insérer "après"
            else:
                if dataTarget.parent != dataSource.parent:  # parents différents
#                    print dataSource.typeSeance, dataTarget.GetListeTypes()
                    if not dataSource.typeSeance in dataTarget.GetListeTypes():
#                        print "0-4"
                        return 0
                    else:
#                        print "3"
                        return 3
                else:
#                    print "4"
                    return 4
            
            




#            if isinstance(dataTarget, Seance):
#                # source et target ont le même parent (même niveau dans l'arbre)
#                if dataTarget.parent == dataSource.parent:
#                    if dataTarget.typeSeance in ["R","S"]:# rotation ou parallele
#                        if not dataSource in dataTarget.seances:
#                            return 1
#                    else:
#                        return 2
#                
#                # source et target ont des parents différents
#                elif dataTarget.parent != dataSource.parent:
#                    return 3
#            elif dataTarget == self.sequence.panelSeances:
#                return 4
        
        return 0

    ####################################################################################
    def OnEndDrag(self, event):
        """ Gestion des glisser-déposer
        """
        self.item = event.GetItem() 
        dataTarget = self.GetItemPyData(self.item)
        if isinstance(dataTarget, PanelPropriete_Racine):
            dataTarget = self.sequence
        dataSource = self.GetItemPyData(self.itemDrag)
        
        a = self.getActionDnD(dataSource, dataTarget)
        if a == 1:
            lstS = dataSource.parent.seances
            lstT = dataTarget.seances
            s = lstS.index(dataSource)
            lstT.insert(0, lstS.pop(s))
            dataSource.parent = dataTarget
            
            self.sequence.OrdonnerSeances()
            self.sequence.reconstruireBrancheSeances(dataSource.parent, dataTarget)
            self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
        elif a == 2:
            lst = dataSource.parent.seances
            s = lst.index(dataSource)
            lst.insert(0, lst.pop(s))
               
            self.sequence.OrdonnerSeances() 
            self.SortChildren(self.GetItemParent(self.item))
            self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
        elif a == 3:
            lstT = dataTarget.parent.seances
            lstS = dataSource.parent.seances
            s = lstS.index(dataSource)
            t = lstT.index(dataTarget)
            lstT[t+1:t+1] = [dataSource]
            del lstS[s]
            p = dataSource.parent
            dataSource.parent = dataTarget.parent
            
            self.sequence.OrdonnerSeances()
            self.sequence.reconstruireBrancheSeances(dataTarget.parent, p)
            self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
        elif a == 4:
            lst = dataTarget.parent.seances
            s = lst.index(dataSource)
            t = lst.index(dataTarget)
            
            if t > s:
                lst.insert(t, lst.pop(s))
            else:
                lst.insert(t+1, lst.pop(s))
               
            self.sequence.OrdonnerSeances() 
            self.SortChildren(self.GetItemParent(self.item))
            self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
        
        
#        if isinstance(dataSource, Seance) and dataTarget != dataSource:
#            
#            # Insérer "dans"  (racine ou "R" ou "S")
#            if dataTarget == self.sequence.panelSeances \
#               or (isinstance(dataTarget, Seance) and dataTarget.typeSeance in ["R","S"]):
#                if not dataSource in dataTarget.seances:    # changement de parent
#                    
#                else:
#                    
#            
#            # Insérer "après"
#            else:
#                print "Insérer après"
#                if dataTarget.parent != dataSource.parent:
#                    
#                else:
#                    print "  même parent"
                    
            
        self.itemDrag = None
        event.Skip()
        
        
        
#    ####################################################################################
#    def OnEndDrag2(self, event):
#        """ Gestion des glisser-déposer
#        """
#        self.item = event.GetItem() 
#        dataTarget = self.GetItemPyData(self.item)
#        dataSource = self.GetItemPyData(self.itemDrag)
#        if dataTarget == self.sequence.panelSeances: # racine des séances
#            dataTarget = self.sequence.seances[0]
#            self.item = self.GetFirstChild(self.item)[0]
#            root = True
#        else:
#            root = False
#            
#        if isinstance(dataSource, Seance) and isinstance(dataTarget, Seance)  and dataTarget != dataSource:
#            
#            # source et target ont le même parent (même niveau dans l'arbre)
#            if dataTarget.parent == dataSource.parent:
#                
#                if dataTarget.typeSeance in ["R","S"]:          # rotation ou parallele
#                    if not dataSource in dataTarget.seances:    # changement de parent
#                        lstS = dataSource.parent.seances
#                        lstT = dataTarget.seances
#                        s = lstS.index(dataSource)
#                        lstT.insert(0, lstS.pop(s))
#                        dataSource.parent = dataTarget
#                        
#                        self.sequence.OrdonnerSeances()
#                        self.sequence.reconstruireBrancheSeances(dataSource.parent, dataTarget)
#                        self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
#                    
#                else:
#                    lst = dataTarget.parent.seances
#
#                    s = lst.index(dataSource)
#                    if root:
#                        t = -1
#                    else:
#                        t = lst.index(dataTarget)
#                    
#                    if t > s:
#                        lst.insert(t, lst.pop(s))
#                    else:
#                        lst.insert(t+1, lst.pop(s))
#                       
#                    self.sequence.OrdonnerSeances() 
#                    self.SortChildren(self.GetItemParent(self.item))
#                    self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
#            
#            # source et target ont des parents différents
#            elif dataTarget.parent != dataSource.parent:
#                lstT = dataTarget.parent.seances
#                lstS = dataSource.parent.seances
#
#                s = lstS.index(dataSource)
#                if root:
#                    t = -1
#                else:
#                    t = lstT.index(dataTarget)
#                lstT[t+1:t+1] = [dataSource]
#                del lstS[s]
#                p = dataSource.parent
#                dataSource.parent = dataTarget.parent
#                
#                self.sequence.OrdonnerSeances()
#                self.sequence.reconstruireBrancheSeances(dataTarget.parent, p)
#                self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
#            else:
#                pass
#            
#        self.itemDrag = None
#        event.Skip()            

    
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
        self.doc = projet
        
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

#        self.CurseurInsert = wx.CursorFromImage(constantes.images.CurseurInsert.GetImage())
        self.CurseurInsertApres = wx.CursorFromImage(constantes.images.Curseur_InsererApres.GetImage())
        self.CurseurInsertDans = wx.CursorFromImage(constantes.images.Curseur_InsererDans.GetImage())
                
        
            
    
            
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
                            self.SetCursor(self.CurseurInsertApres)
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
        
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)


    ######################################################################################################
    def OnEnter(self, event):
#        print "OnEnter PanelPropriete"
        self.SetFocus()
        event.Skip()
        
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
#        item = event.GetItem()
#        code = self.GetItemText(item).split()[0]

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
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.GetMainWindow().Bind(wx.EVT_MOTION, self.ToolTip)

    ######################################################################################################
    def ToolTip(self, event):
        return
        print self.HitTest((event.x, event.y))
        
    ######################################################################################################
    def OnEnter(self, event):
#        print "OnEnter PanelPropriete"
        self.SetFocus()
        event.Skip()
        
    #############################################################################
    def MiseAJourTypeEnseignement(self, ref):
#        print "MiseAJourTypeEnseignement"
        self.ref = ref
        
        for i in self.items.values():
            for wnd in i._wnd:
                if wnd:
                    wnd.Hide()
                    wnd.Destroy()
                    
        self.DeleteChildren(self.root)
        self.items = {}
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
        ww = 0
        for c in range(1, self.GetColumnCount()):
            ww += self.GetColumnWidth(c)
        w = self.GetClientSize()[0]-20-ww
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
            self.items[k] = b
            
            if ct_type == 0:
                self.SetItemBold(b, True)
        
    ####################################################################################
    def OnItemCheck(self, event, item = None):
#        print "OnItemCheck"
        if event != None:
            item = event.GetItem()
        
        self.AjouterEnleverCompetencesItem(item)
        
        if event != None:
            event.Skip()
        wx.CallAfter(self.pptache.SetCompetences)
        
    
    ####################################################################################
    def AjouterEnleverCompetencesItem(self, item, propag = True):
#        print "AjouterEnleverCompetencesItem"
        code = self.GetItemPyData(item)#.split()[0]
#        print "AjouterEnleverCompetencesItem", code
        if code != None: # un seul indicateur séléctionné
            self.AjouterEnleverCompetences([item], propag)

        else:       # une compétence complète séléctionnée
            self.AjouterEnleverCompetences(item.GetChildren(), propag)

    ####################################################################################
    def AjouterEnleverCompetences(self, lstitem, propag = True):
#        print "AjouterEnleverCompetences"
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
                            CT.TR_ROW_LINES|CT.TR_ALIGN_WINDOWS| \
                            CT.TR_AUTO_CHECK_PARENT|CT.TR_AUTO_TOGGLE_CHILD):
        self.revue = revue#|CT.TR_AUTO_CHECK_CHILD|\
        self.eleves = eleves
 
        ArbreCompetences.__init__(self, parent, ref, pptache,
                                  agwStyle = agwStyle)#|CT.TR_ELLIPSIZE_LONG_ITEMS)#|CT.TR_TOOLTIP_ON_LONG_ITEMS)#
        self.Bind(wx.EVT_SIZE, self.OnSize2)
        self.Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        
        self.SetColumnText(0, ref.nomCompetences + u" et " + ref.nomIndicateurs)
        
        tache = self.pptache.tache
        prj = tache.GetProjetRef()
        
        for i, part in enumerate(prj.parties.keys()):
            self.SetColumnText(i+1, u"Poids "+part)
            self.SetColumnWidth(i+1, 60)
        if eleves:
            self.SetColumnWidth(i+2, 0)
            
          
        
#        self.Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        
    ####################################################################################
    def ConstruireCasesEleve(self):
        """ 
        """
#        print "ConstruireCasesEleve"
        tache = self.pptache.tache
        prj = tache.GetProjetRef()
        for codeIndic, item in self.items.items():
            cases = self.GetItemWindow(item, 3)
            if isinstance(cases, ChoixCompetenceEleve):
                item.DeleteWindow(3)
                cases = ChoixCompetenceEleve(self.GetMainWindow(), codeIndic,
                                             tache.projet, tache)
                item.SetWindow(cases, 3)
            
    

    ####################################################################################
    def Construire(self, branche = None, dic = None, ref = None):
#        print "Construire compétences prj", self.pptache.tache
        if ref == None:
            ref = self.ref
        
        if branche == None:
            branche  = self.root
#        print dic
        
        tache = self.pptache.tache
        prj = tache.GetProjetRef()
        if dic == None: # Construction de la racine
            dic = prj._dicCompetences
        
#        print "   ProjetRef", prj
#        print "   dicCompetences", dic
#        print tache
        
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False)
        
#        size = None
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
                    
                    else:   # Groupe de compétences - avec poids
                        if debug: print "   prem's", v[2]
                        b = self.AppendItem(br, k+" "+v[0])
#                        print " * ",v[2]
                        
                        for i, part in enumerate(prj.parties.keys()):
                            if part in v[2].keys():
                                self.SetItemText(b, pourCent2(0.01*v[2][part]), i+1)
                        
#                        for i, p in enumerate(v[2][1:]):
#                            if p != 0:
#                                self.SetItemText(b, pourCent2(0.01*p), i+1)
                        self.SetItemBold(b, True)
                    self.items[k] = b
                    const(v[1], b, debug = debug)
                        
                else:   # Indicateur
                    
                    cc = [cd+ " " + it for cd, it in zip(k.split(u"\n"), v[0].split(u"\n"))]
#                    c = self.AppendItem(b, u"\n".join(cc), ct_type=1)
              
                    comp = self.AppendItem(br, u"\n ".join(cc))
                    
                    if len(v) == 3: # Groupe de compétences - avec poids
                        if debug: print "   prem's", v[2]
                        for j, part in enumerate(prj.parties.keys()):
                            if part in v[2].keys():
#                        for i, p in enumerate(v[2][1:]):
#                            if p != 0:
                                self.SetItemText(comp, pourCent2(0.01*v[2][part]), j+1)
                        self.SetItemBold(comp, True)
                                
#                    comp = self.AppendItem(br, k+" "+v[0])
                    
                    self.items[k] = comp
                    b = None #
                    tous = True
                    for i, indic in enumerate(v[1]):
                        codeIndic = str(k+'_'+str(i+1))
                        if debug:
#                            print not tache.phase in [_R1, "Rev", tache.projet.getCodeLastRevue()]
                            print codeIndic , indic.revue,
                            if hasattr(tache, 'indicateursMaxiEleve'):
                                print tache.indicateursMaxiEleve[0]
                            print prj.getTypeIndicateur(codeIndic)
                        
                        if tache == None:
                            b = self.AppendItem(comp, indic.intitule, data = codeIndic)
                            for j, part in enumerate(prj.parties.keys()):
                                if part in v[2].keys():
#                            for j, p in enumerate(indic.poids[1:]):
#                                if p != 0:
                                    if j == 0:
                                        self.SetItemTextColour(b, COUL_PARTIE['C'])
                                    else:
                                        self.SetItemTextColour(b, COUL_PARTIE['S'])
                            self.SetItemFont(b, font)
                            
                            
                        if tache != None and ((not tache.phase in [_R1,_R2, _Rev, tache.projet.getCodeLastRevue()]) \
                                              or (codeIndic in tache.indicateursMaxiEleve[0])) \
                                         and (indic.revue == 0 or indic.revue >= tache.GetProchaineRevue()) \
                                         and (prj.getTypeIndicateur(codeIndic) == "S" or tache.phase != 'XXX'):
                            
                            b = self.AppendItem(comp, indic.intitule, ct_type=1, data = codeIndic)
                            if codeIndic in tache.indicateursEleve[0]:
                                self.CheckItem2(b)
                            else:
                                tous = False
                            
                            if indic.getRevue() == tache.phase:
                                self.CheckItem2(b)
                                
                            if debug: print "   indic", indic
                            
                            for j, part in enumerate(prj.parties.keys()):
                                if part in indic.poids.keys():
#                            for j, p in enumerate(indic.poids[1:]):
#                                if p != 0:
                                    self.SetItemText(b, pourCent2(0.01*indic.poids[part]), j+1)
                                    if part in COUL_PARTIE.keys():
                                        self.SetItemTextColour(b, COUL_PARTIE[part])
                                    else:
                                        self.SetItemTextColour(b, COUL_PARTIE[''])
                            self.SetItemFont(b, font)        
                            
                            self.items[codeIndic] = b
                            
                            if self.eleves:
#                                print "   ", tache.projet.eleves,
                                cases = ChoixCompetenceEleve(self.GetMainWindow(), codeIndic, 
                                                                           tache.projet, 
                                                                           tache)

#                                cases.SetSize(cases.GetBestSize())
                                self.SetItemWindow(b, cases, 3)
                                
                                for e in range(len(tache.projet.eleves)):
                                    tousEleve[e] = tousEleve[e] and self.GetItemWindow(b, 3).EstCocheEleve(e+1)
#                                size = self.GetItemWindow(b, 3).GetSize()[0]
#                                print cases.GetSize()
                                b.SetWindowEnabled(True, 3)
#                                self.Collapse(comp)
#                                self.Refresh()
#                                self.Layout()
                    
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
        
        
#        self.ExpandAll()
#        self.CalculatePositions()
        self.Refresh()
            
        return
    

    #############################################################################
    def MiseAJourCaseEleve(self, codeIndic, etat, eleve, propag = True):
#        print "MiseAJourCaseEleve", codeIndic, etat, eleve, propag
        casesEleves = self.GetItemWindow(self.items[codeIndic], 3)
        if casesEleves.EstCocheEleve(eleve) != etat:
            return
        
        estToutCoche = casesEleves.EstToutCoche()
#        print "  estToutCoche =", estToutCoche
        
        comp = codeIndic.split("_")[0]
        
        if comp != codeIndic: # Indicateur seul
            item = self.items[codeIndic]
            itemComp = self.items[comp]
#            print "  itemComp =", itemComp
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
            
            self.CheckItem2(item, estToutCoche, torefresh=True)
#            self.Refresh()
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
        
        if propag:
            self.pptache.SetCompetences()
#        wx.CallAfter(self.Refresh)
#        if propag:
#            wx.CallAfter(self.pptache.SetCompetences)
        
        
    #############################################################################
    def OnToolTip(self, event):
        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))
            




class ArbreFonctionsPrj(ArbreCompetences):
    """ Arbre des fonctions abordées en projet lors d'une tâche <pptache>
        <revue> : vrai si la tâche est une revue
        <eleves> : vrai s'il faut afficher une colonne supplémentaire pour distinguer les compétences pour chaque éleve
    """
    def __init__(self, parent, ref, pptache, 
                 agwStyle = CT.TR_HIDE_ROOT|CT.TR_HAS_VARIABLE_ROW_HEIGHT|\
                            CT.TR_ROW_LINES|CT.TR_ALIGN_WINDOWS|CT.TR_AUTO_CHECK_CHILD|\
                            CT.TR_AUTO_CHECK_PARENT|CT.TR_AUTO_TOGGLE_CHILD):

          
        ArbreCompetences.__init__(self, parent, ref, pptache,
                                  agwStyle = agwStyle)#|CT.TR_ELLIPSIZE_LONG_ITEMS)#|CT.TR_TOOLTIP_ON_LONG_ITEMS)#
        self.Bind(wx.EVT_SIZE, self.OnSize2)
        self.Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        
        self.SetColumnText(0, ref.nomFonctions + u" et " + ref.nomTaches)
        
      


    ####################################################################################
    def Construire(self, branche = None, dic = None, ref = None):
#        print "Construire fonctions",
        if ref == None:
            ref = self.ref
#        prj = self.pptache.tache.GetProjetRef()
        
        if dic == None: # Construction de la racine
            dic = ref.dicFonctions
        if branche == None:
            branche  = self.root
#        print dic
#        
#        print "   ", self.GetColumnCount()
        for c in range(1, self.GetColumnCount()):
            self.RemoveColumn(1)
#        print "  ", dic
        for i, c in enumerate(sorted(ref.dicCompetences.keys())):
            self.AddColumn(u"")
            self.SetColumnText(i+1, c)
            self.SetColumnAlignment(i+1, wx.ALIGN_CENTER)
            self.SetColumnWidth(i+1, 30)
            
#        tache = self.pptache.tache
            
#        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False)
#        
#        size = None
        
        def const(d, br, debug = False):
            ks = d.keys()
            ks.sort()
            for k in ks:
                if debug: print "****", k
                v = d[k]
                if len(v) > 1 and type(v[1]) == dict:
                    if debug: print "   ", v[0]
                    b = self.AppendItem(br, k+" "+v[0])
                    self.items[k] = b
                    const(v[1], b, debug = debug)
                        
                else:   # Extremité de branche
                    cc = [cd+ " " + it for cd, it in zip(k.split(u"\n"), v[0].split(u"\n"))]
                    comp = self.AppendItem(br, u"\n ".join(cc), ct_type=1, data = k)
               
                    if debug: print "   prem's 2", v[1]
                    
                    
                    for c, p in enumerate(sorted(ref.dicCompetences.keys())):
                        if p in v[1]:
#                    for i, p in enumerate(v[1]):
#                        if p == self.GetColumnText(i+1):
                            self.SetItemText(comp, "X", c+1)
                                
                    self.items[k] = comp

#                    if b == None: # Désactivation si branche vide d'indicateurs
#                        self.SetItemType(br,0)
#                    else:
#                        self.CheckItem2(br, tous)

            return
            
        const(dic, branche, debug = False)
            
#        if tache == None: # Cas des arbres dans popup
#            self.SetColumnWidth(1, 0)
#            self.SetColumnWidth(2, 0)
#        self.Refresh()
            
        return
    
        
    #############################################################################
    def OnToolTip(self, event):
        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))
            
    ####################################################################################
    def OnItemCheck(self, event, item = None):
        pass



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
    def Construire(self, dic , dicIndicateurs, prj):
#        print "Construire", dic
#        print dicIndicateurs
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
                    if k in dicIndicateurs.keys():
                        ajouteIndic(comp, v[1], dicIndicateurs[k])
                    else:
                        ajouteIndic(comp, v[1], None)
            return
        
        def ajouteIndic(branche, listIndic, listIndicUtil):
            for i, indic in enumerate(listIndic):
                b = self.AppendItem(branche, textwrap.fill(indic.intitule, 50))
                for j, part in enumerate(prj.parties.keys()):
                    if part in indic.poids.keys():
#                for j, p in enumerate(indic.poids[1:]):
#                    if p != 0:
#                        print listIndic
#                        print comp, dicIndicateurs[comp]
                        if listIndicUtil == None or not listIndicUtil[i]:
                            self.SetItemTextColour(b, COUL_ABS)
                        else:
                            self.SetItemTextColour(b, COUL_PARTIE[part])
                self.SetItemFont(b, font)
        
        if type(dic) == dict:  
            const(dic, branche, debug = debug)
        else:
            ajouteIndic(branche, dic, dicIndicateurs)
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
            sizer.Add(cb[-1], 1, flag = wx.EXPAND)
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb[-1])
        self.cb = cb
        self.projet = projet
        self.tache = tache
        
        self.MiseAJour()
        self.Actualiser()
        self.Layout()
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
        
        for i in range(len(self.projet.eleves)):
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
        self.SetCursor(wx.CursorFromImage(constantes.images.Curseur_InsererApres.GetImage()))

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
        
    def GetHeight2(self):
        height = int(2*16)
        for indx in xrange(self.GetItemCount()):
            height += self.GetItemRect(indx).height
        return height
    
    def GetWidth2(self):
        return self.GetViewRect()[2]
    
    
    
        
class PanelListe(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent, fen):
        wx.Panel.__init__(self, parent, -1, style = wx.BORDER_RAISED)
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
        
#        self.listeSeq.Bind(wx.EVT_SIZE, self.OnResize)
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
            try:
                pos = self.listeSeq.InsertStringItem(i, f)
                self.listeSeq.SetStringItem(pos, 1, d)
                self.itemDataMap[i] = (f, d, seq)
                self.listeSeq.SetItemData(i, i)
            except:
                print "Erreur", f
            
#        self.listeSeq.SetColumnWidth(0, wx.LIST_AUTOSIZE)
#        self.listeSeq.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.listeSeq.Layout()
#        self.OnResize()
#        self.Fit()
        
        listmix.ColumnSorterMixin.__init__(self, 2)
        
##########################################################################################################
#
#  Panel pour l'affichage des BO
#
##########################################################################################################
class Panel_BO(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.nb = wx.Notebook(self, -1)
        self.sizer.Add(self.nb, proportion=1, flag = wx.EXPAND)
        
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
        self.SetSizer(self.sizer)
        
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)


    ######################################################################################################
    def OnEnter(self, event):
        self.SetFocus()
        event.Skip()
        
        
    ######################################################################################################
    def OnPageChanged(self, event):
        pass
    
    ######################################################################################################
    def Construire(self, ref):
        if ref.BO_dossier == u"":
            return
        
        wx.BeginBusyCursor()
        
        lst_pdf = []
        for d in ref.BO_dossier:
            path = os.path.join(constantes.BO_PATH, d)
            for root, dirs, files in os.walk(path):
                for f in files:
                    if os.path.splitext(f)[1] == r".pdf":
                        lst_pdf.append(os.path.join(root, f))
            
      
#        print self.nb.GetPageCount()
        for index in reversed(range(self.nb.GetPageCount())):
            try:
                self.nb.DeletePage(index)
            except:
                print "raté :", index
#        self.dataNoteBook.SendSizeEvent()
        
        
        for f in lst_pdf:
            page = genpdf.PdfPanel(self.nb)
            page.chargerFichierPDF(f)
            self.nb.AddPage(page, os.path.split(os.path.splitext(f)[0])[1])

        wx.EndBusyCursor()

#################################################################################################################
#
# Synthèse pédagogique (sur pluieures séquences)
#
#################################################################################################################
import xlwt
from xlwt import Workbook, Font, XFStyle, Borders, Alignment, Formula, Pattern


class FenetreBilan(wx.Frame):
    def __init__(self, parent, dossierCourant = constantes.PATH, 
                 referentiel = REFERENTIELS[constantes.TYPE_ENSEIGNEMENT_DEFAUT]):
        wx.Frame.__init__(self, parent, -1, u"Synthèse pédagogique", style = wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP)
        
        self.pourProjet = False
        self.lastPath = None
        
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
        titre = wx.StaticBox(panel, -1, u"Type d'enseignement")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        te = ArbreTypeEnseignement(panel, self)
        self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, te)
        sb.Add(te, flag = wx.EXPAND)
        self.referentiel = referentiel
#        l = []
#        for i, e in enumerate(REFERENTIELS.keys()):
#            l.append(REFERENTIELS[e].Enseignement[0])
#        rb = wx.RadioBox(
#                panel, -1, u"Type d'enseignement", wx.DefaultPosition, (130,-1),
#                l,
#                1, wx.RA_SPECIFY_COLS
#                )
#        rb.SetToolTip(wx.ToolTip(u"Choisir le type d'enseignement"))
#        for i, e in enumerate(REFERENTIELS.keys()):
#            rb.SetItemToolTip(i, REFERENTIELS[e].Enseignement[1])
#        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
#            
#        # Provosoirement uniquement pour SSI
#        for i in [1,2,3,4]:
#            rb.EnableItem(i, False)    
        
        self.sizer.Add(sb, (0,0), (2,1), flag = wx.EXPAND|wx.ALL)
        self.cb_type = te
        te.SetStringSelection(referentiel.Enseignement[0])

        #
        # Dossiers de recherche
        #
        sb = wx.StaticBox(panel, -1, u"Dossiers où chercher les fichiers de séquence")
        sbs = wx.StaticBoxSizer(sb, wx.VERTICAL)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        self.dossiers = [os.path.abspath(dossierCourant)]
        self.dossiersOk = True
        self.txtDoss = wx.TextCtrl(panel, -1, os.path.abspath(dossierCourant))
        self.txtDoss.SetToolTipString(u"Saisir les dossiers de recherche, séparés par \";\"")
#        self.txtDoss.Bind(wx.EVT_KILL_FOCUS, self.EvtTextDoss)
        self.Bind(wx.EVT_TEXT, self.EvtTextDoss, self.txtDoss)
        hs.Add(self.txtDoss, 1, flag = wx.EXPAND|wx.ALL)
        
        self.boutonDoss = wx.Button(panel, -1, "+", size = (30, -1))
        self.boutonDoss.SetToolTipString(u"Ajouter un dossier de recherche")
        self.Bind(wx.EVT_BUTTON, self.OnDossier, self.boutonDoss)
        hs.Add(self.boutonDoss, flag = wx.EXPAND|wx.ALL)
        
        sbs.Add(hs, flag = wx.EXPAND|wx.ALL)
        self.cbr = wx.CheckBox(panel, -1, u"Inclure les sous-dossiers")
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.cbr)
        self.recurs = True
        self.cbr.SetValue(self.recurs)
        sbs.Add(self.cbr, flag = wx.EXPAND|wx.ALL)
        
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
        
        self.Bind(wx.EVT_SIZE, self.OnResize)
#        wx.CallAfter(self.cb_type.CollapseAll)
#        wx.CallAfter(self.Thaw)
        
        
    ######################################################################################              
    def EvtCheckBox(self, event):
        self.recurs = event.IsChecked()
        self.MiseAJourListe()
        
    ######################################################################################              
    def OnResize(self, evt = None):
#        print "Resize ArbreTypeEnseignement", self.GetClientSize()
        self.cb_type.SetMinSize((-1, self.GetClientSize()[1]-30))
        self.cb_type.Layout()
        self.sizer.Layout()
        if evt:
            evt.Skip()
        
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
        
        self.tb.AddLabelTool(30, u"Actualiser", images.Bouton_Actualiser.GetBitmap(), 
                             shortHelp=u"Actualiser la liste des séquences", 
                             longHelp=u"Actualiser la liste des séquences")
        self.Bind(wx.EVT_TOOL, self.MiseAJourListe, id=30)
        
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        self.tool_open = self.tb.AddLabelTool(20, u"Ouvrir", open_bmp, 
                             shortHelp=u"Ouvrir la synthèse", 
                             longHelp=u"Ouvrir la synthèse")
        self.Bind(wx.EVT_TOOL, self.OuvrirSynthese, id=20)     
        
#        print "fini"

        
        #################################################################################################################
        #
        # Mise en place
        #
        #################################################################################################################
        self.tb.Realize()
        
        self.tb.RemoveTool(20)
#        print "fini 2"
    
    
    ######################################################################################  
    def commandeExporter(self, event = None):
        mesFormats = r"Fichier Excel|*.xls"
        dlg = wx.FileDialog(self, 
                            message = u"Enregistrement de la synthèse", 
                            defaultFile="", wildcard=mesFormats, 
                            style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR
                            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
#            ok = self.enregistrer(path)
            ok = self.genererBilan(path)
            if ok:
                dlg = wx.MessageDialog(self, u"Export de la synthèse réussi !", u"Export de la synthèse réussi",
                           wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
                self.lastPath = path
                self.tb.InsertToolItem(2,self.tool_open)
                self.tb.Realize()
                
            else:
                dlg = wx.MessageDialog(self, u"L'export de la synthèse a échoué !", u"Echec de l'export de la synthèse",
                           wx.OK | wx.ICON_WARNING)
                dlg.ShowModal()
                dlg.Destroy()
        else:
            dlg.Destroy()

    ######################################################################################  
    def OuvrirSynthese(self, event = None):
        if self.lastPath != None and os.path.isfile(self.lastPath):
            try:
                os.startfile(self.lastPath)
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'ouvrir la synthèse\n\n%s\n" %toDefautEncoding(self.lastPath))

    ######################################################################################  
    def definirStyles(self, book):
        #
        # Couleurs
        #
        xlwt.add_palette_colour("vert1", 8)
        book.set_colour_RGB(8, 120, 200, 120)
        xlwt.add_palette_colour("vert2", 9)
        book.set_colour_RGB(9, 160, 220, 160)
        xlwt.add_palette_colour("vert3", 10)
        book.set_colour_RGB(10, 200, 255, 200)
        
        xlwt.add_palette_colour("rouge1", 18)
        book.set_colour_RGB(18, 200, 120, 120)
        xlwt.add_palette_colour("rouge2", 19)
        book.set_colour_RGB(19, 220, 160, 160)
        xlwt.add_palette_colour("rouge3", 20)
        book.set_colour_RGB(20, 255, 200, 200)
        
        #
        # Styles
        #    
        
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 37
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.height = 36*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER

        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 42
        
        styleT = XFStyle()
        styleT.font = fnt
        styleT.borders = borders
        styleT.alignment = al
        styleT.pattern = pattern
        self.styleT = styleT
        
        ######################################################
        
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.height = 16*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER

        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 1

        styleE = XFStyle()
        styleE.font = fnt
        styleE.borders = borders
        styleE.alignment = al
        styleE.pattern = pattern
        self.styleE = styleE
        
        ######################################################

        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.height = 14*20

        borders = Borders()
        borders.left = 1
        borders.right = 0
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        al.wrap = False
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 43

        style0 = XFStyle()
        style0.font = fnt
        style0.borders = borders
        style0.alignment = al
        style0.pattern = pattern
        self.style0 = style0
        
        ######################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.height = 14*20

        borders = Borders()
        borders.left = 0
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        al.wrap = True
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 43
        
        style01 = XFStyle()
        style01.font = fnt
        style01.borders = borders
        style01.alignment = al
        style01.pattern = pattern
        self.style01 = style01
        
        ######################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.height = 14*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        al.wrap = True
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 43
        
        style02 = XFStyle()
        style02.font = fnt
        style02.borders = borders
        style02.alignment = al
        style02.pattern = pattern
        self.style02 = style02
    
        ######################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.height = 12*20

        borders = Borders()
        borders.left = 1
        borders.right = 0
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        al.wrap = False
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 41

        style1 = XFStyle()
        style1.font = fnt
        style1.borders = borders
        style1.alignment = al
        style1.pattern = pattern
        self.style1 = style1
        
        ######################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = False
        fnt.height = 12*20

        borders = Borders()
        borders.left = 0
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 41
        al.wrap = True

        style11 = XFStyle()
        style11.font = fnt
        style11.borders = borders
        style11.alignment = al
        style11.pattern = pattern
        self.style11 = style11
        
        ######################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = False
        fnt.height = 12*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 41
        al.wrap = True

        style12 = XFStyle()
        style12.font = fnt
        style12.borders = borders
        style12.alignment = al
        style12.pattern = pattern
        self.style12 = style12
        
        ######################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.height = 10*20

        borders = Borders()
        borders.left = 1
        borders.right = 0
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        al.wrap = False
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 1

        style2 = XFStyle()
        style2.font = fnt
        style2.borders = borders
        style2.alignment = al
        style2.pattern = pattern
        self.style2 = style2
        
        ######################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = False
        fnt.height = 10*20
        

        borders = Borders()
        borders.left = 0
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        al.wrap = True
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 1

        style21 = XFStyle()
        style21.font = fnt
        style21.borders = borders
        style21.alignment = al
        style21.pattern = pattern
        self.style21 = style21
        
        ######################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = False
        fnt.height = 10*20
        

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_LEFT
        al.vert = Alignment.VERT_CENTER
        al.wrap = True
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 1

        style22 = XFStyle()
        style22.font = fnt
        style22.borders = borders
        style22.alignment = al
        style22.pattern = pattern
        self.style22 = style22
        
        # Croix #####################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.height = 12*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 47

        styleX = XFStyle()
        styleX.font = fnt
        styleX.borders = borders
        styleX.alignment = al
        styleX.pattern = pattern
        self.styleX = styleX
        
        # rien #####################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.height = 12*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 1

        stylenX = XFStyle()
        stylenX.font = fnt
        stylenX.borders = borders
        stylenX.alignment = al
        stylenX.pattern = pattern
        self.stylenX = stylenX
        
        # Durée de séquence #####################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.italic = True
        fnt.height = 9*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        al.wrap = False
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 29

        styleD = XFStyle()
        styleD.num_format_str='hh:mm'
        styleD.font = fnt
        styleD.borders = borders
        styleD.alignment = al
        styleD.pattern = pattern
        self.styleD = styleD
        
        
        # Période de séquence #####################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.italic = False
        fnt.height = 18*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        al.wrap = False
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 29

        stylePer = XFStyle()
        stylePer.font = fnt
        stylePer.borders = borders
        stylePer.alignment = al
        stylePer.pattern = pattern
        self.stylePer = stylePer
        
        
        # Numéro de séquence #####################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.italic = False
        fnt.height = 16*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        al.wrap = False
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 19

        styleN = XFStyle()
        styleN.font = fnt
        styleN.borders = borders
        styleN.alignment = al
        styleN.pattern = pattern
        self.styleN = styleN
        
        # Intitulé de séquence #####################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.italic = False
        fnt.height = 9*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        al.rotation = Alignment.ORIENTATION_90_CC
        
        al.wrap = True
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 20

        styleS = XFStyle()
        styleS.num_format_str='hh:mm'
        styleS.font = fnt
        styleS.borders = borders
        styleS.alignment = al
        styleS.pattern = pattern
        self.styleS = styleS
        
        ######################################################
        
        f = Font()
        f.height = 20*6
        f.name = 'Verdana'
        f.bold = False
        f.underline = Font.UNDERLINE_SINGLE
        f.colour_index = 4
        
        al = Alignment()
        al.horz = Alignment.HORZ_RIGHT
        
        h_style = XFStyle()
        h_style.font = f
        h_style.alignment = al
        self.h_style = h_style
        
        # Position cible CI #####################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.italic = True
        fnt.height = 12*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        al.wrap = False
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 8

        stylePosCI = XFStyle()
        stylePosCI.num_format_str='hh:mm'
        stylePosCI.font = fnt
        stylePosCI.borders = borders
        stylePosCI.alignment = al
        stylePosCI.pattern = pattern
        self.stylePosCI = stylePosCI
        
        # Numéro de CI #####################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = True
        fnt.italic = False
        fnt.height = 14*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        al.wrap = False
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 9

        styleNumCI = XFStyle()
        styleNumCI.font = fnt
        styleNumCI.borders = borders
        styleNumCI.alignment = al
        styleNumCI.pattern = pattern
        self.styleNumCI = styleNumCI
        
        # Intitulé de CI #####################################################
        fnt = Font()
        fnt.name = 'Arial'
        fnt.colour_index = 0
        fnt.outline = True
        fnt.struck_out = False
        fnt.bold = False
        fnt.italic = False
        fnt.height = 9*20

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        al.rotation = Alignment.ORIENTATION_90_CC
        
        al.wrap = True
        
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 10

        styleCI = XFStyle()
        styleCI.num_format_str='hh:mm'
        styleCI.font = fnt
        styleCI.borders = borders
        styleCI.alignment = al
        styleCI.pattern = pattern
        self.styleCI = styleCI
    
    #######################################################################################  
    def getCIcommuns(self, listeSeq):
        """ Dresse un bilan des CI intégrés dans les séquences
            >> renvoie : 
            [[[liste de séquences], [liste des CI de ces séquences]], [[autre liste de séquences], [liste des CI de ces séquences]], ...]
        """
        
        def memeCI(lst1, lst2):
            if len(lst1) <> len(lst2):
                return False
            for i, ci in enumerate(lst2):
                if ci != lst1[i]:
                    return False
            return True
        
        
        
        new = True
        listeCI = []
        for seq in listeSeq:
#            print "***", seq
            ref = seq.GetReferentiel()
#            print "   ", ref.CentresInterets
            if len(listeCI) == 0: # Initialisation de la listeCI
                listeCI.append([[seq], list(ref.CentresInterets)])
            else:
                for s, l in listeCI:
                    if memeCI(l, ref.CentresInterets):
                        s.append(seq)
                        new = False
                        break
                if new:
#                    print "   Nouveau >>", seq, "<>", s[-1]
                    listeCI.append([[seq], list(ref.CentresInterets)])
                new = True
                    
        
#        print "listeCI", listeCI
                            
        return listeCI
    
    #######################################################################################  
    def traiterDic(self, dic, ws0, l = 6, c = 0):
        """ Fonction de traitement des dictionnaires (compétences, savoir)
            >>> positionnement sur la partie gauche
        """
        dicLigne = {}
        for c0, v0 in sorted(dic):
            ws0.write(l, c, c0, self.style0)                                     # Code
            ws0.write_merge(l, l, c+1, c+3, v0[0], self.style01)                   # Intitulé
            dicLigne[c0] = [l, [], 0]
            l += 1
            if type(v0[1]) == dict:
                for c1, v1 in sorted(v0[1].items()):
                    ws0.write(l, c+1, c1, self.style1)                           # Code
                    dicLigne[c1] = [l, [], 1]
                    dicLigne[c0][1].append(c1)
                    ws0.write_merge(l, l, c+2, c+3, v1[0], self.style11)           # Intitulé
                    if type(v1[1]) == dict:
                        for c2, v2 in sorted(v1[1].items()):
                            l += 1
                            ws0.write(l, c+2, c2, self.style2)                   # Code
                            dicLigne[c2] = [l, [], 2]
                            dicLigne[c1][1].append(c2)
                            ws0.write_merge(l, l, c+3, c+3, v2[0], self.style21)   # Intitulé
#                                l += 1
                    l += 1
        return dicLigne, l
        
    
    ######################################################################################  
    def reglerLargeursGauche(self, ws0, c, c0 = 0):
        """ Règle la largeur des colonnes de la partie gauche
        """
        #
        # Largeur des colonnes
        #
        ws0.col(c0+0).width = 100*20
        ws0.col(c0+1).width = 100*20
        ws0.col(c0+2).width = 100*20
        ws0.col(c0+3).width = 900*20
        ws0.col(c0+4).width = 15*20
#        for cc in range(c0+5, c0+c):
#            ws0.col(cc).width = 80*20
    
    ######################################################################################  
    def getStyleComp(self, niv):
        if niv == 0:
            return self.style02
        elif niv == 1:
            return self.style12
        elif niv == 2:
            return self.style22
        
                               
    ######################################################################################  
    def genererBilanComplexe(self, wb, comp_sav = 'C'):
        """ Génère une feuille affichant un croisement
                CI/Compétence (comp_sav = 'C')
                CI/Savoirs (comp_sav = 'S')
        """
        
        def traiterSeq(nom, dic):
            ws0 = wb.add_sheet(nom)
            ws0.write_merge(1, 3, 1, 3, self.referentiel.Enseignement[0], self.styleT)
            ws0.write_merge(5, 5, 0, 3, nom, self.styleE)
            dicLigne, last = self.traiterDic(dic.items(), ws0)
          
            #
            # On met les croix
            #
            c = 5
            l = 6
            n = "HYPERLINK"
            for p, lst in enumerate(self.seqTriees):
                for i, seq in enumerate(lst):
                    ws0.write(l-4, c, (i*(p+1))+1, self.styleN)                  # Numéro de séquence
                    ws0.write(l-3, c, seq.intitule, self.styleS)                 # Intitulé
                    ws0.write(l-2, c, str(seq.GetDuree()), self.styleD)          # Durée
                    ws0.write(l-1, c, Formula(n + '("%s";"%s")' %(seq.nomFichier, os.path.split(seq.nomFichier)[1])), self.h_style)           # Fichier
                    c += 1
                if len(lst) > 0:
                    ws0.write_merge(l-5, l-5, c-i-1, c-1, seq.position+1, self.styleN)
                ws0.col(c).width = 10*20
                c += 1
            return  ws0, dicLigne, last 
        
        col_deb = 6
        
        
        
        if comp_sav == 'C':
            nom = self.referentiel.nomCompetences + u" - CI"
        else:
            nom = self.referentiel.nomSavoirs + u" - CI"
        ws0 = wb.add_sheet(nom)
        ws0.write_merge(1, 3, 1, col_deb-2, self.referentiel.Enseignement[0], self.styleT)
        ws0.write_merge(5, 5, 0, col_deb-2, nom, self.styleE)
        if comp_sav == 'C':
            dicLigne, lastComp = self.traiterDic(self.referentiel.dicCompetences.items(), ws0, c = 1)
        else:
            dicLigne, lastComp = self.traiterDic(self.referentiel.dicSavoirs.items(), ws0, c = 1)
        
        #
        # Séquences en colonne
        #  
        c = col_deb
        l = lastComp+1
        
        ws0.write_merge(l, l, 0, col_deb-2, u"Séquences", self.styleE)
        
        l += 1
        ws0.write(l, c-6, u"Année", self.styleS)             # Année
        ws0.write(l, c-5, u"Période", self.styleS)           # Période
        ws0.write(l, c-4, u"Numéro", self.styleS)            # Numéro de séquence
        ws0.write(l, c-3, u"Fichier", self.styleS)           # Fichier
        ws0.write(l, c-2, u"Intitulé", self.styleS)          # Intitulé
        
        ws0.write(l, c, u"Durée", self.styleS)               # Durée
        
        l += 2
        pt = 0
        n = "HYPERLINK"
        for p, lst in enumerate(self.seqTriees):
            for i, seq in enumerate(lst):
                ws0.write(l, c-4, (i*(p+1))+1, self.styleN)                  # Numéro de séquence
                ws0.write(l, c-2, seq.intitule, self.styleS)                 # Intitulé
                ws0.write(l, c, getHoraireTxt(seq.GetDuree()), self.styleD)            # Durée
                ws0.write(l, c-3, Formula(n + '("%s";"%s")' %(seq.nomFichier, os.path.split(seq.nomFichier)[1])), self.h_style)           # Fichier
                l += 1
            if len(lst) > 0:
                ws0.write_merge(l-i-1, l-1, c-5, c-5, seq.position+1, self.stylePer)  # Période
                if pt == 0 and seq.position == 4:
                    pt = l
            ws0.row(c).height = 10*20
            l += 1
        lastSeq = l-1
        if pt != 0:
            ws0.write_merge(lastComp+4, pt-1, c-6, c-6, u"1ère", self.styleN)  # Période
            if pt < lastSeq:
                ws0.write_merge(pt+1, lastSeq, c-6, c-6, u"Tale", self.styleN)  # Période
                
                
        #
        # CI en ligne
        #        
        c = col_deb+2
        l = 4
        ws0.write_merge(l-3, l-3, c, c+len(self.referentiel.CentresInterets)-1, 
                        getSingulierPluriel(self.referentiel.nomCI, True), self.styleT)
        
        for i, ci in enumerate(self.referentiel.CentresInterets):
            if len(self.referentiel.positions_CI) > i:
                pos = self.referentiel.positions_CI[i]
                ws0.write(l-2, c, pos, self.stylePosCI)                 # position cible
            ws0.write(l-1, c, self.referentiel.abrevCI+str(i+1), self.styleNumCI)          # numéro CI
            ws0.write(l, c, ci, self.styleCI)                           # ci
            ws0.col(c).width = 120*20
            c += 1
        lastCI = c
        
        #
        # On additionne les poids horaires par séquence
        #
        lstSomPoidsSeq = []
        for p, lst in enumerate(self.seqTriees):
            for i, seq in enumerate(lst):
#                if seq.CI.poids != []:
                lstSomPoidsSeq.append(0)
                for poids in seq.CI.poids:
                    lstSomPoidsSeq[-1] += poids
#        print  lstSomPoidsSeq

        #
        # On met les durées au croisement seq/CI
        #
        c = col_deb+2
        l = lastComp+4
        j = 0
        sumCI = [0]*len(self.referentiel.CentresInterets)
        for p, lst in enumerate(self.seqTriees):
            for i, seq in enumerate(lst):
                # Poids horaires
                for ci, poids in zip(seq.CI.numCI, seq.CI.poids):
                    p = poids*seq.GetDuree()/lstSomPoidsSeq[j]
                    sumCI[ci] += p
                    ws0.write(l, c+ci, getHoraireTxt(p), self.styleX)
                # Case vides
                for co in range(c, lastCI):
                    try:
                        ws0.write(l, co, "", self.stylenX)
                    except:
                        pass
                l += 1
                j += 1
            l += 1
        
        
        def CodeDansListe(code, dic):
#            print code
#            print dic
            if comp_sav == 'C':
                if code in dic.keys():
                    return True, dic[code][0]
                else:
                    return False, None
            else:
                if code[1:] in dic.keys() and (code[0] == 'S' or code[0] == 'B'):
                    return True , dic[code[1:]][0]
                else:
                    return False, None
        
        
        #
        # On met les croix Compétences/CI ou Savoirs/CO
        #
        c = col_deb+2
        l = 6
        for p, lst in enumerate(self.seqTriees):
            for i, seq in enumerate(lst):
                if comp_sav == 'C':
                    lstc = seq.obj["C"].competences
                else:
                    lstc = seq.obj["S"].savoirs
                for cod in lstc:
                    x, li = CodeDansListe(cod, dicLigne)
                    if x:
                        for ci in seq.CI.numCI:
                            try:
                                ws0.write(li, c+ci, "X", self.styleX)
                            except:
                                pass
                                
        for co in range(c, lastCI):
#            for li in range(l, lastComp):
            for li, ch, niv  in dicLigne.values():
                try:
                    ws0.write(li, co, "", self.getStyleComp(niv))
                except:
                    pass
                
        #
        # On met les formules de somme
        #
        l = lastComp+2
        c = col_deb+2
        for ci in range(c, lastCI):
#            cc = constantes.lettreCol(ci)
#            ws0.write(l, ci, Formula("SUM("+cc+str(l+3)+":"+cc+str(lastSeq+1)+")"), self.styleN)
            ws0.write(l, ci, getHoraireTxt(sumCI[ci-c]), self.styleN)
        
        ws0.col(0).width = 80*20
        ws0.col(1).width = 70*20
        self.reglerLargeursGauche(ws0, c, c0 = 1)
        ws0.col(col_deb).width = 80*20
        ws0.col(col_deb+1).width = 15*20
        
        
        return
        
    
    ######################################################################################  
    def genererBilan(self, nomFichier):
#        print "genererBilan"
        wb = Workbook()
        self.definirStyles(wb)
        
        #
        # On trie les séquences par période
        #
        self.seqTriees = [[], [], [], [], [], [], [], [], [], []]
        for i in range(self.listeSeq.listeSeq.GetItemCount()):
            seq = self.listeSeq.GetSequence(i)
            self.seqTriees[seq.position].append(seq)
        
        
        def traiterSeq(nom, dic):
            ws0 = wb.add_sheet(nom)
            ws0.write_merge(1, 3, 1, 3, self.referentiel.Enseignement[0], self.styleT)
            ws0.write_merge(5, 5, 0, 3, nom, self.styleE)
            dicLigne, last = self.traiterDic(dic.items(), ws0)
          
            #
            # Séquences en ligne
            #
            c = 5
            l = 6
            pt = 0
            n = "HYPERLINK"
            for p, lst in enumerate(self.seqTriees):
                for i, seq in enumerate(lst):
                    ws0.write(l-4, c, (i*(p+1))+1, self.styleN)                  # Numéro de séquence
                    ws0.write(l-3, c, seq.intitule, self.styleS)                 # Intitulé
                    ws0.write(l-2, c, getHoraireTxt(seq.GetDuree()), self.styleD)          # Durée
                    ws0.write(l-1, c, Formula(n + '("%s";"%s")' %(seq.nomFichier, os.path.split(seq.nomFichier)[1])), self.h_style)           # Fichier
                    ws0.col(c).width = 100*20
                    c += 1
                if len(lst) > 0:
                    ws0.write_merge(l-5, l-5, c-i-1, c-1, seq.position+1, self.styleN) # Période
                    if pt == 0 and seq.position == 4:
                        pt = c
                ws0.col(c).width = 15*20
                c += 1
            
            if pt != 0:
                ws0.write_merge(l-6, l-6, 5, pt-1, u"1ère", self.styleN)  # Année
                if pt < c:
                    ws0.write_merge(l-6, l-6, pt+1, c, u"Tale", self.styleN)  # Année
                
                
            return  ws0, dicLigne, last 
        
        
        #
        # Feuille Compétences
        #
        ws0, dicLigne, last = traiterSeq(self.referentiel.nomCompetences, 
                                         self.referentiel.dicCompetences)
        c = 5
        l = 6
        for p, lst in enumerate(self.seqTriees):
            for i, seq in enumerate(lst):         
                for sav in seq.obj["C"].competences:
                    if sav in dicLigne.keys():
                        li = dicLigne[sav][0]
#                        for li in dicLigne[sav]:
                        ws0.write(li, c, "X", self.styleX)
#                for li in range(l+1, last):
                for li, ch, niv in dicLigne.values():
                    try:
                        ws0.write(li, c, "", self.getStyleComp(niv))
                    except:
                        pass
                c += 1
            c += 1
                
        self.reglerLargeursGauche(ws0, c)
        
        
        
        #
        # Feuille Savoirs
        #
        if self.referentiel.tr_com != []: # C'est un enseignement de spécialité avec un tronc commun
            ws0, dicLigne, last = traiterSeq(self.referentiel.nomSavoirs + " " + REFERENTIELS[self.referentiel.tr_com[0]].Enseignement[0], 
                                              REFERENTIELS[self.referentiel.tr_com[0]].dicSavoirs)
            c = 5
            l = 6
            for p, lst in enumerate(self.seqTriees):
                for i, seq in enumerate(lst):
                    for sav in seq.obj["S"].savoirs:
                        if sav[1:] in dicLigne.keys() and sav[0] == 'B':
                            li = dicLigne[sav[1:]][0]
                            ws0.write(li, c, "X", self.styleX)       # X
                    
#                    for li in range(l+1, last):
                    for li, ch, niv in dicLigne.values():
                        try:
                            ws0.write(li, c, "", self.getStyleComp(niv))
                        except:
                            pass
                    c += 1
                c += 1
            self.reglerLargeursGauche(ws0, c)
            
            
        
        
        #
        # Feuille Savoirs
        # 
        ws0, dicLigne, last = traiterSeq(self.referentiel.nomSavoirs + " " + self.referentiel.Enseignement[0], 
                                         self.referentiel.dicSavoirs)
        c = 5
        l = 6
#        print dicLigne.keys()
        for p, lst in enumerate(self.seqTriees):
            for i, seq in enumerate(lst):
                for sav in seq.obj["S"].savoirs:
#                    print sav
                    if sav[1:] in dicLigne.keys() and (sav[0] == 'S' or sav[0] == 'B'):
                        li = dicLigne[sav[1:]][0]
#                        for li in dicLigne[sav[1:]]:
                        ws0.write(li, c, "X", self.styleX)       # X
                
#                for li in range(l+1, last):
                for li, ch, niv in dicLigne.values():
                    try:
                        ws0.write(li, c, "", self.getStyleComp(niv))
                    except:
                        pass
                c += 1
            c += 1
        self.reglerLargeursGauche(ws0, c)
            
        self.genererBilanComplexe(wb, 'C')
        self.genererBilanComplexe(wb, 'S')
        
#        ws0 = wb.add_sheet(self.referentiel.nomSavoirs)
#        
#        ws0.write_merge(1, 3, 1, 3, self.referentiel.Enseignement[0], styleT)
#        ws0.write_merge(5, 5, 0, 3, self.referentiel.nomSavoirs, styleE)
#        dicLigne, last = traiter(self.referentiel.dicSavoirs.items())
#      
#        #
#        # On met les croix
#        #
#        c = 5
#        l = 5
#        n = "HYPERLINK"
#        for i, seq in enumerate(listePrem + listeTerm):
#            ws0.write(l-4, c, i+1, styleN)                          # Numéro de séquence
#            ws0.write(l-3, c, seq.intitule, styleS)                 # Intitulé
#            ws0.write(l-2, c, str(seq.GetDuree()), styleD)          # Durée
#            ws0.write(l-1, c, Formula(n + '("%s";"%s")' %(seq.nomFichier,seq.nomFichier)), h_style)           # Fichier
#            
#            for sav in seq.obj["S"].savoirs:
#                if sav[1:] in dicLigne.keys() and sav[0] == 'B':
#                    for li in dicLigne[sav[1:]]:
#                        ws0.write(li, c, "X", styleX)       # X
#            
#            for li in range(l+1, last):
#                try:
#                    ws0.write(li, c, "", stylenX)
#                except:
#                    pass
#            c += 1
#            
#        #
#        # Largeur des colonnes
#        #
#        ws0.col(0).width = 100*20
#        ws0.col(1).width = 100*20
#        ws0.col(2).width = 100*20
#        ws0.col(3).width = 1000*20
#        ws0.col(4).width = 50*20
#        for cc in range(5, c):
#            ws0.col(cc).width = 80*20
#        
#        #
#        # Feuille Compétences
#        #        
#        ws0 = wb.add_sheet(self.referentiel.nomCompetences)
#        
#        ws0.write_merge(1, 3, 1, 3, self.referentiel.Enseignement[0], styleT)
#        ws0.write_merge(5, 5, 0, 3, self.referentiel.nomCompetences, styleE)
#        dicLigne, last = traiter(self.referentiel.dicCompetences.items())
#      
#        #
#        # On met les croix
#        #
#        c = 5
#        l = 5
#        for i, seq in enumerate(listePrem + listeTerm):
#            ws0.write(l-4, c, i+1, styleN)                          # Numéro de séquence
#            ws0.write(l-3, c, seq.intitule, styleS)                 # Intitulé
#            ws0.write(l-2, c, str(seq.GetDuree()), styleD)          # Durée
#            ws0.write(l-1, c, Formula(n + '("%s";"%s")' %(seq.nomFichier,seq.nomFichier)), h_style)           # Fichier
#            
#            for sav in seq.obj["C"].competences:
#                if sav in dicLigne.keys():
#                    for li in dicLigne[sav]:
#                        ws0.write(li, c, "X", styleX)
#            for li in range(l+1, last):
#                try:
#                    ws0.write(li, c, "", stylenX)
#                except:
#                    pass
#            c += 1
#            
#        #
#        # Largeur des colonnes
#        #
#        ws0.col(0).width = 100*20
#        ws0.col(1).width = 100*20
#        ws0.col(2).width = 100*20
#        ws0.col(3).width = 1000*20
#        ws0.col(4).width = 50*20
#        for cc in range(5, c):
#            ws0.col(cc).width = 80*20
        
        #
        # Sauvegarde
        #
        try:
            wb.save(nomFichier)
        except IOError:
            messageErreur(self, u'Accès refusé',
                          u"Le fichier n'a pas pu être enregistré !\n\n" \
                          u"Il est peut-être déja ouvert ...")
            return False
        
        return True
        
#    ######################################################################################  
#    def enregistrer(self, nomFichier):
#        fichierPP = constantes.fichierProgressionProgramme[self.typeEnseignement]
#        try:
#            tableau = grilles.PyExcel(os.path.join(TABLE_PATH, fichierPP))
#        except:
#            print fichierPP, "est déja ouvert !"
#            return False
#
##        def ecrire(feuille, l, c):
##            v = tableau.getCell(feuille, l, c)
##            if v == "A":
##                v = "B"
##            elif v == "B":
##                v = "C"
##            elif v == "C":
##                v = "C"
##            else:
##                v = "A"
##            tableau.setCell(feuille, l, cc+i, v)
#            
#        feuilleP = u"Progression - Programme"
#        feuilleS = u"Progression - Systèmes"
#        
#        # Première cellule "séquence"
#        lcp, ccp = (4, 11) # K4
#        lct, cct = (4, 15) # O4
#        
#        # Première cellule "durée"
#        ldp, cdp = (5, 11) # K5
#        
#        # Première cellule "systèmes"
#        lsp, csp = (8, 4) # D8
#        lst, cst = (8, 8) # H8
#        
#        listePrem = []
#        listeTerm = []
#
#        
#        for i in range(self.listeSeq.listeSeq.GetItemCount()):
#            seq = self.listeSeq.GetSequence(i)
#            if seq.position >= 4:
#                listeTerm.append(seq)
#            else:
#                listePrem.append(seq)
#        
##        listePrem = sorted(listePrem, key=lambda s: s.intitule)
##        listeTerm = sorted(listeTerm, key=lambda s: s.intitule)
#        
#        listeSystemes = []
#        for i, seq in enumerate(listePrem + listeTerm):
#            
#            if seq in listePrem:
#                c = ccp + i
#                cs = csp + i
#            else:
#                c = cct + i - len(listePrem)
#                cs = cst + i - len(listePrem)
#                
#            tableau.setCell(feuilleP, lcp, c, seq.intitule)
#            tableau.setCell(feuilleP, ldp, c, str(seq.GetDuree()))
#            tableau.setLink(feuilleP, lcp, c, seq.nomFichier)
#            tableau.setCell(feuilleP, lcp-1, c, i+1)
#            
#            dicCel = constantes.dicCellSavoirs[self.typeEnseignement]
#            for sav in seq.obj["S"].savoirs:
#                if sav in dicCel.keys():
#                    lig0, lig1 = dicCel[sav]
#                    for l in range(lig0, lig1+1):
#                        tableau.setCell(feuilleP, l, c, "X")
#                else:
#                    continuer = True
#                    s=1
#                    while continuer:
#                        sav1 = sav+'.'+str(s)
#                        if sav1 in dicCel.keys():
#                            lig0, lig1 = dicCel[sav1]
#                            for l in range(lig0, lig1+1):
#                                tableau.setCell(feuilleP, l, c, "X")
#                            s += 1
#                        else:
#                            continuer = False
#            
#            #
#            # Tableau "Systèmes"
#            #
#            nbrSystemes = seq.GetNbrSystemes()
#            for syst in seq.systemes:
#                # ligne du tableau correspondant au système
#                if not syst.nom in listeSystemes:
#                    listeSystemes.append(syst.nom)
#                    l = lsp+len(listeSystemes)-1
#                    tableau.setCell(feuilleS, l, 1, syst.nom)
#                else:
#                    l = lsp+listeSystemes.index(syst.nom)-1
#                
#                # nombre d'exemplaires du système utilisés dans la séquence
#                if syst.nom in nbrSystemes.keys():
#                    tableau.setCell(feuilleS, l, cs, nbrSystemes[syst.nom])
#                
#            #
#            # Ajout éventuel de colonnes
#            #
#            if seq in listePrem:
#                if len(listePrem) > 3 and i < len(listePrem) - 3:
#                    tableau.insertPasteCol(feuilleP, c+1)
#                    tableau.insertPasteCol(feuilleS, cs+1)
#                    cct += 1
#            else:
#                if len(listeTerm) > 3 and i - len(listePrem) < len(listeTerm) - 3:
#                    tableau.insertPasteCol(feuilleP, c+1)
#                    tableau.insertPasteCol(feuilleS, c+1)
#                
#        try:                   
#            tableau.save(nomFichier)
#        except :
#            print nomFichier, "est déja ouvert !"
#            return False
#            
#        tableau.close()
#        return True
        
    ######################################################################################  
    def EvtRadioBox(self, event):
#        print "EvtRadioBox"
        radio_selected = event.GetEventObject()
        typeEnseignement = Referentiel.getEnseignementLabel(radio_selected.GetLabel())[0]
        self.referentiel = REFERENTIELS[typeEnseignement]
        
#        self.referentiel = REFERENTIELS[Referentiel.getEnseignementLabel(self.cb_type.GetItemLabel(event.GetInt()))[0]]
        
#        self.typeEnseignement = Referentiel.getEnseignementLabel(self.cb_type.GetItemLabel(event.GetInt()))[0]
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
        self.txtDoss.Refresh()
    

    

        
    ########################################################################################################
    def MiseAJourListe(self, event = None):       
        if self.dossiersOk:
            wx.BeginBusyCursor()
            
            l = []
            if self.recurs:
                for dossier in self.dossiers:
                    for root, dirs, files in os.walk(dossier):
#                        print files
                        l.extend([os.path.join(root, f) for f in files if os.path.splitext(f)[1] == '.seq'])
            else:
                for dossier in self.dossiers:
                    l.extend(glob.glob(os.path.join(dossier, "*.seq")))
                

            dlg =    wx.ProgressDialog(u"Recherche des séquences",
                                       u"",
                                       maximum = len(l),
                                       parent=self.Parent,
                                       style = 0
                                        | wx.PD_APP_MODAL
                                        #| wx.PD_CAN_ABORT
                                        #| wx.PD_CAN_SKIP
                                        #| wx.PD_ELAPSED_TIME
                                        | wx.PD_ESTIMATED_TIME
                                        | wx.PD_REMAINING_TIME
                                        | wx.PD_AUTO_HIDE
                                        )
#            print "l =", l
            listSequences = []
            count = 0
            for f in l:
                try:
                    dlg.Update(count, f)
                except:
                    print "Erreur", f
                
                classe, sequence = self.OuvrirFichierSeq(f)
#                print classe.typeEnseignement ,  self.referentiel.Code
                if classe != None and classe.typeEnseignement == self.referentiel.Code:
                    sequence.nomFichier = f
                    listSequences.append(sequence)
                count += 1
            
#            print "listSequences AVANT", listSequences
            listeCI = self.getCIcommuns(listSequences)
            if len(listeCI) > 1:
                dlgc = DialogChoixCI(self, listeCI, self.referentiel)
                dlgc.ShowModal()
                choix = dlgc.choix
                listSequences = listeCI[choix][0]
        
                dlgc.Destroy()
            
#            print "listSequences APRES", listSequences
            self.listeSeq.MiseAJourListe(listSequences)
            self.tb.RemoveTool(20)
#            self.tb.Realize()
            
            dlg.Update(count, u"Terminé")
            dlg.Destroy()
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
            if rclasse is not None:
                classe.setBranche(rclasse)
            if rsequence is not None:
                sequence.setBranche(rsequence)
            else:   # Ancienne version , forcément STI2D-ETT !!
                classe.typeEnseignement, self.classe.familleEnseignement = ('ET', 'STI')
                classe.referentiel = REFERENTIELS[classe.typeEnseignement]
                sequence.setBranche(root)
            return classe, sequence
        except:
            print u"Le fichier n'a pas pu être ouvert :",nomFichier
#            messageErreur(self,u"Erreur d'ouverture",
#                          u"La séquence pédagogique\n    %s\n n'a pas pu être ouverte !" %nomFichier)
#            fichier.close()
#            self.Close()
            return None, None
                
                
class DialogChoixCI(wx.Dialog):
    def __init__(self, parent, listeCI, referentiel, style=wx.DEFAULT_DIALOG_STYLE):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, -1, getSingulierPluriel(referentiel.nomCI, True) + u" différents")

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, u"Les séquences identifiées n'utilisent pas toutes les mêmes centres d'intérêt.\n" \
                              u"Merci de choisir la liste de centres d'intérêt à utiliser pour la synthèse.\n")
        label.SetHelpText("Choisir la liste de centres d'intérêt à utiliser pour la synthèse    ²")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        
        maxs = 600/len(listeCI)
        self.radio = []
        for i, (l, s) in enumerate(listeCI):
            lstsz = wx.BoxSizer(wx.VERTICAL)
            if i == 0:
                radio = wx.RadioButton(self, -1, getSingulierPluriel(referentiel.nomCI, True) + u" #"+str(i+1), style = wx.RB_GROUP )
            else:
                radio = wx.RadioButton(self, -1, getSingulierPluriel(referentiel.nomCI, True) +u" #"+str(i+1))
            radio.SetHelpText(u"Liste de "+referentiel.abrevCI+" #"+str(i))
            self.Bind(wx.EVT_RADIOBUTTON, self.OnSelect, radio )
            self.radio.append(radio)
            lstsz.Add(radio, 0, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5)
            
            label = wx.StaticText(self, -1, str(len(l))+u" séquence"+(len(l)>1)*"s")
            lstsz.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5)                      
                                  
            text = wx.TextCtrl(self, -1, u"\n".join(s), size=(maxs,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
            text.SetHelpText(u"Liste de "+referentiel.abrevCI+" #"+str(i))
            lstsz.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5)
            box.Add(lstsz, 0, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5 )
            
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.choix = 0
        
        self.SetSizer(sizer)
        sizer.Fit(self)              
    
    
    def OnSelect( self, event ):
        self.choix = self.radio.index(event.GetEventObject())

                
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
# ProgressDialog personnalisé
# 
#############################################################################################################
class myProgressDialog(wx.ProgressDialog):
    def __init__(self, titre, message, nbr_etapes, parent):
        wx.ProgressDialog.__init__(self, u"Ouverture d'un projet",
                                   message,
                                   maximum = nbr_etapes,
                                   parent = parent,
                                   style = 0
                                    | wx.PD_APP_MODAL
                                    #| wx.PD_CAN_ABORT
                                    #| wx.PD_CAN_SKIP
                                    #| wx.PD_ELAPSED_TIME
                                    | wx.PD_ESTIMATED_TIME
                                    | wx.PD_REMAINING_TIME
                                    #| wx.PD_AUTO_HIDE
                                    )

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    
    def OnClose(self, event):
        print "Close dlg"
        self.Destroy()        
        
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
        t.SetLabelMarkup( wordwrap(u"<b>pySequence</b> est un logiciel d'aide à l'élaboration de séquences pédagogiques et à la validation de projets,\n"
                                          u"sous forme de fiches exportables au format PDF ou SVG.\n"
                                          u"Il est élaboré en relation avec les programmes et les documents d'accompagnement\n"
                                          u"des enseignements des filières STI2D, SSI et Technologie Collège",500, wx.ClientDC(self)))
        nb.AddPage(descrip, u"Description")
        nb.AddPage(auteurs, u"Auteurs")
        nb.AddPage(licence, u"Licence")
        
        sizer.Add(hl.HyperLinkCtrl(self, wx.ID_ANY, u"Informations et téléchargement : https://github.com/cedrick-f/pySequence",
                                   URL="https://github.com/cedrick-f/pySequence"),  
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
    

