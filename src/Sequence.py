#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sequence.py
Aide à la réalisation de fiches pédagogiques de séquence
*************
*   STIDD   *
*************
Copyright (C) 2011-2012  
@author: Cedrick FAURY

"""
__appname__= "pySequence"
__author__ = u"Cédrick FAURY"
__version__ = "2.2"


####################################################################################
#
#   Import des modules nécessaires
#
####################################################################################
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

# Graphiques vectoriels
import draw_cairo, draw_cairo_prj
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

# Gestionnaire de "pane"
import wx.aui as aui

# Pour passer des arguments aux callback
import functools
    
# Pour enregistrer en xml
import xml.etree.ElementTree as ET

# des widgets wx évolués "faits maison"
from CedWidgets import Variable, VariableCtrl, VAR_REEL_POS, EVT_VAR_CTRL, VAR_ENTIER_POS
#from CustomCheckBox import CustomCheckBox
# Les constantes et les fonctions de dessin


# Les constantes partagées
from constantes import calculerEffectifs, revCalculerEffectifs, APP_DATA_PATH, PATH, findEffectif, getTextCI, strEffectifComplet, strEffectif, getListCI, getElementFiltre
import constantes

# Pour lire les classeurs Excel
import recup_excel

import Options
from wx.lib.embeddedimage import PyEmbeddedImage

import register

import textwrap

import serveur

# Pour l'export en swf
#import tempfile
#import svg_export

# Pour les descriptions
import richtext

from math import sin,cos,pi
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
#   Evenement perso pour détecter une modification de la séquence
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
#        print "1"
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
        res = dlg.ShowModal()
        dlg.Destroy() 
#        url = dlg.GetURL().path
#            
#        if res == wx.ID_OK and url != "":
#            self.EvalLien(url, pathseq)
#            
#        elif res == wx.ID_CANCEL:
#            print "Rien" 
            

    ######################################################################################  
    def Afficher(self, pathseq, fenSeq = None):
#        print "Afficher :", self.path
        
        
        path = self.GetAbsPath(pathseq)
        
        if self.type == "f":
            try:
                os.startfile(path)
            except:
                dlg = wx.MessageDialog(None, u"Impossible d'ouvrir le fichier\n%s!\n" %toDefautEncoding(path) ,
                               u"Ouverture impossible",
                               wx.OK | wx.ICON_WARNING
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
                dlg.ShowModal()
                dlg.Destroy()
                
        elif self.type == 'd':
            try:
                subprocess.Popen(["explorer", path])
            except:
                dlg = wx.MessageDialog(None, u"Impossible d'accéder au dossier\n%s!\n" %toDefautEncoding(path) ,
                               u"Ouverture impossible",
                               wx.OK | wx.ICON_WARNING
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
                dlg.ShowModal()
                dlg.Destroy()
            
        elif self.type == 'u':
            try:
#                lien_safe = urllib.quote_plus(self.path)
    #            urllib.urlopen(lien_safe)
                webbrowser.open(self.path)
            except:
                dlg = wx.MessageDialog(None, u"Impossible d'ouvrir l'url\n%s!\n" %toDefautEncoding(self.path) ,
                               u"Ouverture impossible",
                               wx.OK | wx.ICON_WARNING
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
                dlg.ShowModal()
                dlg.Destroy()
        
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
#        print "EvalLien", self

        if path == "" or path.split() == []:
            self.path = ""
            self.type = ""
            return
        
        path = toFileEncoding(path)
        pathseq = toFileEncoding(pathseq)
        abspath = self.GetAbsPath(pathseq, path)
#        print "   ", abspath
        if os.path.exists(abspath):
#            print "   exist"
            if os.path.isfile(abspath):
                self.type = 'f'
                self.path = testRel(abspath, pathseq)
            elif os.path.isdir(abspath):
                self.type = 'd'
                self.path = testRel(abspath, pathseq)
        else:
            self.type = 'u'
            self.path = path

#        print "Fin EvalLien", self.type, self
              
    ######################################################################################  
    def GetAbsPath(self, pathseq, path = None):
        if path == None:
            path = self.path
        
#        path = self.GetEncode(path)
        if os.path.exists(path):
            path = path
        else:
#            pathseq = self.GetEncode(pathseq)
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
            


    
####################################################################################
#
#   Classe définissant les propriétés d'une séquence
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
#        lien = os.path.join(os.path.abspath(os.path.dirname(self.lien.path) ), os.readlink(self.lien.path))
        
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
#        print "SetLien", self.lien
        self.tip.SetLien(self.lien)
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
        self.tip.SetLien(self.lien)
        
        
#    ######################################################################################  
#    def AfficherLien(self):
##        print "AfficherLien", self.lien
#        
#        t = self.GetTypeLien()
#        if t == "f":
#            os.startfile(self.lien)
#        elif t == 'd':
#            subprocess.Popen(["explorer", self.lien])
#        elif t == 'u':
#            lien_safe = urllib.quote_plus(self.lien)
#            urllib.urlopen(self.lien)
#
#  
#    ######################################################################################  
#    def GetTypeLien(self):
#        if self.lien == "":
#            return ""
#        if os.path.exists(self.lien):
#            if os.path.isfile(self.lien):
#                return 'f'
#            elif os.path.isdir(self.lien):
#                return 'd'
#        else:
#            return 'u'
#        
        
        
class LienSequence():
    def __init__(self, parent, panelParent, path = ""):
        self.path = path
        self.parent = parent
        self.panelPropriete = PanelPropriete_LienSequence(panelParent, self)
        self.panelParent = panelParent
        # Tip
        self.tip = PopupInfoSysteme(self.parent.app, u"Séquence requise")
    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du lien de sequence pour enregistrement
        """
        root = ET.Element("Sequence")
        root.set("dir", self.path)
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche lien seq"
        self.path = branche.get("dir", "")
        if hasattr(self, 'panelPropriete'):
            ok = self.panelPropriete.MiseAJour()
#        print "..."

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Sequence :", wnd = self.codeBranche, data = self,
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
        self.tip.SetImage(bmp)

    ######################################################################################  
    def SetLien(self):
        self.tip.SetLien(Lien(self.path, 's'))
#        self.panelPropriete.MiseAJour()
    
    ######################################################################################  
    def SetTitre(self, titre):
        self.tip.SetMessage(titre)
        
    ######################################################################################  
    def GetNomFichier(self):
        return os.path.splitext(os.path.basename(self.path))[0]
     
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
            return self.branche


class Objet_sequence():
    def __init__(self):
        self.elem = None
        
    def SetSVGTitre(self, p, titre):
        self.elem.setAttribute("xlink:title", titre)
     
    def SetSVGLien(self, p, lien):
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
#            print self
#            print p, f
            if type(f) == str:
                pid = f
                p.setAttribute('filter', 'none')
                p.setAttribute("id",  pid)
                p.setAttribute("onmouseout",  "setAttribute('filter', 'none')")
                p.setAttribute("onmouseover", "setAttribute('filter', 'url(#f1)')")
                break
        
        for i, (p, f) in enumerate(self.cadre):
            if type(f) != str:
                a = self.EncapsuleSVG(doc, p)
                titre = self.GetCode(f) + " : " + self.GetIntit(f)
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
                    lien = toDefautEncoding(self.GetLienHTML())
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
    
    
            
class Classe():
    def __init__(self, app, panelParent = None, intitule = u"", pourProjet = False):
        self.intitule = intitule
        
        if pourProjet:
            self.typeEnseignement = 'ITEC'
        else:
            self.typeEnseignement = 'ET'
        
        if not pourProjet:
            self.ci_ET = constantes.CentresInteretsET
            self.posCI_ET = constantes.PositionCibleCIET
        
        self.effectifs = constantes.Effectifs
        self.nbrGroupes = constantes.NbrGroupes
        calculerEffectifs(self)
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Classe(panelParent, self, pourProjet)
            
        self.panelParent = panelParent
        self.app = app
        
    ######################################################################################  
    def __repr__(self):
        return self.posCI_ET[0] + " " + self.ci_ET[0]
    
    
    ######################################################################################  
    def SetDocument(self, doc):   
        self.doc = doc 
        
    
    ######################################################################################  
    def getBranche(self):
        # La classe
        classe = ET.Element("Classe")
        classe.set("Type", self.typeEnseignement)
        
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
#        print "setBranche classe"
        self.typeEnseignement = branche.get("Type", "ET")
        
#        self.ci_ET = getListCI(branche.get("CentreInteret", ""))
        
        
        brancheCI = branche.find("CentreInteret")
        if brancheCI != None:
            listCI = list(brancheCI)
            listCI.sort()
            ci_ET = []
            posCI_ET = []
            for i,c in list(listCI):
                ci_ET.append(brancheCI.get("CI"+str(i+1), ""))
                posCI_ET.append(brancheCI.get("pos"+str(i+1), "O"))    
            if len(ci_ET) > 0:
                self.ci_ET = ci_ET
                self.posCI_ET = posCI_ET
                
        # Ancien format : <Effectifs C="9" D="3" E="2" G="9" P="3" />
        # Nouveau format : <Effectifs eC="9" nE="2" nG="9" nP="3" />
        brancheEff = branche.find("Effectifs")
        
        if brancheEff.get('eC') == None: # Ancienne version
            print "Ancienne version"
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
        
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
#        print "ConstruireArbre classe"
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, self.typeEnseignement)
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
            couleur = 'green'
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
        
        self.position = 0
        
        self.commentaires = u""
        
        self.panelParent = panelParent
          
    ######################################################################################  
    def GetApp(self):
        return self.app
    
    ######################################################################################  
    def GetPath(self):
        return os.path.split(self.app.fichierCourant)[0]
    
    ######################################################################################  
    def GetApercu(self, mult = 3):
        imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  210*mult, 297*mult)#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        ctx = cairo.Context(imagesurface)
        ctx.scale(297*mult, 297*mult) 
        self.draw.Draw(ctx, self)
        bmp = wx.lib.wxcairo.BitmapFromImageSurface(imagesurface)
#        print bmp.GetWidth(), bmp.GetHeight()
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
#        print data
        if data and data != self and hasattr(data, 'AfficherLien'):
            data.AfficherLien(self.GetPath())
#        else:
#            self.arbre.ExpandAllChildren(self.branche)
#            self.arbre.Expand(self.branche)
        
        
        
####################################################################################################          
class Sequence(BaseDoc):
    def __init__(self, app, classe = None, panelParent = None, intitule = u"Intitulé de la séquence pédagogique"):
        BaseDoc.__init__(self, app, classe, panelParent, intitule)
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Sequence(panelParent, self)
        
        self.prerequis = Savoirs(self, panelParent)
        self.prerequisSeance = []
        
        self.CI = CentreInteret(self, panelParent)
        
        self.obj = {"C" : Competences(self, panelParent),
                    "S" : Savoirs(self, panelParent)}
        self.systemes = []
        self.seance = [Seance(self, panelParent)]
        
        self.draw = draw_cairo
        
        
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
#        print ET.tostring(sequence)
        
#        print self.commentaires
        if self.commentaires != u"":
            sequence.set("Commentaires", self.commentaires)
#        print ET.tostring(sequence)
        sequence.set("Position", str(self.position))
#        print ET.tostring(sequence)
        
        sequence.append(self.CI.getBranche())
#        print "brancheCI", brancheCI
#        if brancheCI != None:
#            ci = ET.SubElement(sequence, "CentreInteret")
#            ci.append(brancheCI)
        
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
#        print "setBranche séquence"
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
    def AjouterRotation(self, seance):
        seanceR1 = Seance(self.panelParent)
        seance.sousSeances.append(seanceR1)
        return seanceR1
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
#        print "ConstruireArbre séquence"
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, Titres[0], data = self, image = self.arbre.images["Seq"])

        #
        # LE centre d'intérêt
        #
        self.CI.ConstruireArbre(arbre, self.branche)
        
        #
        # Les prérequis
        #
        self.branchePre = arbre.AppendItem(self.branche, Titres[1], data = self.prerequis, image = self.arbre.images["Sav"])
        for ps in self.prerequisSeance:
            ps.ConstruireArbre(arbre, self.branchePre)
        #
        # Les objectifs
        #
        self.brancheObj = arbre.AppendItem(self.branche, Titres[2], image = self.arbre.images["Obj"])
        for obj in self.obj.values():
            obj.ConstruireArbre(arbre, self.brancheObj)
            
        
        self.brancheSce = arbre.AppendItem(self.branche, Titres[3])
        for sce in self.seance:
            sce.ConstruireArbre(arbre, self.brancheSce) 
            
        self.brancheSys = arbre.AppendItem(self.branche, Titres[4])
        for sy in self.systemes:
            sy.ConstruireArbre(arbre, self.brancheSys)    
        
        
        
#    ######################################################################################  
#    def reconstruireBrancheSeances(self, b1, b2):
#        self.arbre.DeleteChildren(self.brancheSce)
#        for sce in self.seance:
#            sce.ConstruireArbre(self.arbre, self.brancheSce) 
#        self.arbre.Expand(b1.branche)
#        self.arbre.Expand(b2.branche)
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
#            print u"Menu Séances"
            self.app.AfficherMenuContextuel([[u"Ajouter une séance", self.AjouterSeance]])
            
        elif self.arbre.GetItemText(itemArbre) == Titres[4]: # Système
            self.app.AfficherMenuContextuel([[u"Ajouter un système", self.AjouterSysteme], 
                                             [u"Selectionner depuis un fichier", self.SelectSystemes]])
         
        elif self.arbre.GetItemText(itemArbre) == Titres[1]: # Prérequis
            self.app.AfficherMenuContextuel([[u"Ajouter une séquence", self.AjouterSequencePre], 
                                             ])
         
            
    ######################################################################################       
    def GetSystemesUtilises(self):
#        print "GetSystemesUtilises"
        lst = []
#        print "  ", self.systemes
        for s in self.systemes:
            n = 0
#            print "    ", self.seance
            for se in self.seance:
                ns = se.GetNbrSystemes(complet = True)
#                print "      ", ns
                if s.nom in ns.keys():
                    n += ns[s.nom]
            if n > 0:
                lst.append(s)
#        print lst
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
    def GetIntituleSeances(self):
        nomsSeances = []
        intSeances = []
        for s in self.GetToutesSeances():
#            print s
#            print s.intituleDansDeroul
            if hasattr(s, 'code') and s.intitule != "" and not s.intituleDansDeroul:
                nomsSeances.append(s.code)
                intSeances.append(s.intitule)
        return nomsSeances, intSeances
        
        

        
    ######################################################################################  
    def HitTest(self, x, y):
#        rect = draw_cairo.posIntitule + draw_cairo.tailleIntitule
#        posi = draw_cairo.posPos + draw_cairo.taillePos
#        print self.rect

        
        
        if self.CI.HitTest(x, y):
            return self.CI.HitTest(x, y)
#        elif dansRectangle(x, y, (draw_cairo.posObj + draw_cairo.tailleObj,)):
##            self.arbre.DoSelectItem(self.brancheObj)
#            return self.brancheObj
        elif dansRectangle(x, y, (draw_cairo.posPre + draw_cairo.taillePre,)):
            for ls in self.prerequisSeance:
                h = ls.HitTest(x,y)
                if h != None:
                    return h
#            self.arbre.DoSelectItem(self.branchePre)
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
                if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
                    return self.branche
                
            return branche
        
    ######################################################################################  
    def HitTestPosition(self, x, y):
        if hasattr(self, 'rectPos'):
            for i, rectPos in enumerate(self.rectPos):
                if dansRectangle(x, y, (rectPos,)):
                    return i
                    
                                    
                                    
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        self.app.SetTitre()
        self.CI.MiseAJourTypeEnseignement()
        for o in self.obj.values():
            o.MiseAJourTypeEnseignement()
        self.prerequis.MiseAJourTypeEnseignement()
        
        
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
class Projet(BaseDoc):
    def __init__(self, app, classe = None, panelParent = None, intitule = u"Intitulé du projet"):
        BaseDoc.__init__(self, app, classe, panelParent, intitule)
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Projet(panelParent, self)
        
        self.eleves = []
        self.taches = []
        self.equipe = []
        
        self.support = Support(self, panelParent)
        
        self.problematique = u""
        
        
    ######################################################################################  
    def __repr__(self):
        return self.intitule

    
    ######################################################################################  
    def SetPath(self, fichierCourant):
        pathseq = os.path.split(fichierCourant)[0]
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
#        lst.extend(self.obj["C"].GetPtCaract())
#        lst.extend(self.obj["S"].GetPtCaract())
#        lst.extend(self.prerequis.GetPtCaract())
#        lst.extend(self.CI.GetPtCaract())
#        for s in self.seance:
#            lst.extend(s.GetPtCaract())
        return lst    
    
    
    ######################################################################################  
    def EnrichiSVG(self, doc):
#        self.obj["C"].EnrichiSVG(doc)
#        self.obj["S"].EnrichiSVG(doc)
#        self.prerequis.EnrichiSVG(doc)
#        self.CI.EnrichiSVG(doc)
#        for s in self.seance:
#            s.EnrichiSVGse(doc)
        return
            
    
    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la séquence pour enregistrement
        """
        # Création de la racine
        projet = ET.Element("Projet")
        
        projet.set("Intitule", self.intitule)
        
        projet.set("Problematique", self.problematique)
#
        if self.commentaires != u"":
            projet.set("Commentaires", self.commentaires)

        projet.set("Position", str(self.position))
        
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
            
        return projet
        
    ######################################################################################  
    def setBranche(self, branche):
        print "setBranche projet"
        self.intitule = branche.get("Intitule", u"")
        
        self.problematique = branche.get("Problematique", u"")
        
        self.commentaires = branche.get("Commentaires", u"")
        
        self.position = eval(branche.get("Position", "0"))

        brancheEqu = branche.find("Equipe")
        self.equipe = []
        for i,e in enumerate(list(brancheEqu)):
            prof = Prof(self, self.panelParent)
            prof.setBranche(e)
            self.equipe.append(prof)

        brancheSup = branche.find("Support")
        if brancheSup != None:
            self.support.setBranche(brancheSup)
        
        brancheEle = branche.find("Eleves")
        self.eleves = []
        for i,e in enumerate(list(brancheEle)):
            eleve = Eleve(self, self.panelParent)
            eleve.setBranche(e)
            self.eleves.append(eleve)
        
        brancheTac = branche.find("Taches")
        self.taches = []
        for i,e in enumerate(list(brancheTac)):
            tache = Tache(self, self.panelParent)
            tache.setBranche(e)
            self.taches.append(tache)
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()

        
    ######################################################################################  
    def SetProblematique(self, pb):
        self.problematique = pb
        
        
    ######################################################################################  
    def SetCodes(self):
        self.support.SetCode()
        
        for sce in self.taches:
            sce.SetCode()    
            
        for sy in self.eleves:
            sy.SetCode()    

            
    ######################################################################################  
    def PubDescription(self):
        for t in self.taches:
            t.PubDescription()       
         
            
    ######################################################################################  
    def SetLiens(self):
#        for t in self.taches:
#            t.SetLien()    

        self.support.SetLien()  

        
    ######################################################################################  
    def VerifPb(self):
        print "Sert à rien"
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
            e.MiseAJourCodeBranche()
    
    
    ######################################################################################  
    def MiseAJourNomProfs(self):
        for e in self.equipe:
            e.SetCode()
            
            
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
    def AjouterTache(self, event = None):
        tache = Tache(self, self.panelParent)
        self.taches.append(tache)
        tache.ConstruireArbre(self.arbre, self.brancheTac)
#        self.OrdonnerTaches()
        self.panelPropriete.sendEvent()
        self.arbre.SelectItem(tache.branche)
        
        return tache
    
    
    ######################################################################################  
    def SupprimerTache(self, event = None, item = None):
        if len(self.taches) > 1: # On en laisse toujours une !!
            tache = self.arbre.GetItemPyData(item)
            self.taches.remove(tache)
            self.arbre.Delete(item)
            self.OrdonnerTaches()
            self.panelPropriete.sendEvent()
            return True
        return False
    
    
    ######################################################################################  
    def OrdonnerTaches(self):
        ia = ic = ir = iv = 0
        for t in self.taches:
            if t.phase == 'Ana':
                t.ordre = ia
                ia += 1
            elif t.phase == 'Con':
                t.ordre = ic
                ic += 1
            elif t.phase == 'Rea':
                t.ordre = ir
                ir += 1
            elif t.phase == 'Val':
                t.ordre = iv
                iv += 1
        
#        print self.taches
        self.taches.sort(key=attrgetter('phase', 'ordre'))
#        print "-->", self.taches
        
        self.SetCodes()
        self.arbre.Ordonner(self.brancheTac)
    
    
    ######################################################################################  
    def SupprimerItem(self, item):
        data = self.arbre.GetItemPyData(item)
        if isinstance(data, Tache):
            self.SupprimerTache(item = item)
            
        elif isinstance(data, Eleve):
            self.SupprimerEleve(item = item)
            
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
            e = Eleve(self, self.panelParent, len(self.eleves))
            self.eleves.append(e)
            e.ConstruireArbre(self.arbre, self.brancheElv)
            self.arbre.Expand(self.brancheElv)
            self.panelPropriete.sendEvent()
            self.arbre.SelectItem(e.branche)
            self.AjouterEleveDansPanelTache()
        
    
#    ######################################################################################  
#    def AjouterListeEleves(self, propr = []):
#        nouvListe = []
#        for p in propr:
#            sy = Systeme(self, self.panelParent)
#            self.systemes.append(sy)
#            nouvListe.append(sy.nom)
#            sy.ConstruireArbre(self.arbre, self.brancheEle)
#            self.arbre.Expand(self.brancheEle)
#            sy.SetNom(unicode(p[0]))
#            sy.panelPropriete.MiseAJour()
#        self.panelPropriete.sendEvent()
#        self.AjouterListeSystemesSeance(nouvListe)
#        return
    
    ######################################################################################  
    def SupprimerEleve(self, event = None, item = None):
        e = self.arbre.GetItemPyData(item)
        i = self.eleves.index(e)
        self.eleves.remove(e)
        self.arbre.Delete(item)
        self.SupprimerEleveDansPanelTache(i)
        self.panelPropriete.sendEvent()
    
    
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
        i = self.equipe.index(e)
        self.equipe.remove(e)
        self.arbre.Delete(item)
        self.panelPropriete.sendEvent()
        
#    ######################################################################################  
#    def SelectSystemes(self, event = None):
#        if recup_excel.ouvrirFichierExcel():
#            dlg = wx.MessageDialog(self.app, u"Sélectionner une liste de systèmes\n" \
#                                             u"dans le classeur Excel qui vient de s'ouvrir,\n" \
#                                             u"puis appuyer sur Ok.\n\n" \
#                                             u"Format attendu de la selection :\n" \
#                                             u"|    colonne 1\t|    colonne 2 \t|    colonne 3  \t|\n" \
#                                             u"|                  \t|    (optionnelle)  \t|    (optionnelle)   \t|\n" \
#                                             u"|  systèmes  \t|  nombre dispo\t| fichiers image\t|\n" \
#                                             u"|  ...               \t|  ...                \t|  ...               \t|\n",
#                                             u'Sélection de systèmes',
#                                             wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
#                                             )
#            res = dlg.ShowModal()
#            dlg.Destroy() 
#            if res == wx.ID_YES:
#                ls = recup_excel.getSelectionExcel()
#                self.AjouterListeSystemes(ls)
#            elif res == wx.ID_NO:
#                print "Rien" 
        
    
    
    
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        print "ConstruireArbre projet"
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, Titres[9], data = self, image = self.arbre.images["Prj"])

        #
        # Le support
        #
        
        self.support.ConstruireArbre(arbre, self.branche)
        #
        # Les profs
        #
        self.branchePrf = arbre.AppendItem(self.branche, Titres[10])
        for e in self.equipe:
            e.ConstruireArbre(arbre, self.branchePrf) 
        
        #
        # Les élèves
        #
        self.brancheElv = arbre.AppendItem(self.branche, Titres[6])
        for e in self.eleves:
            e.ConstruireArbre(arbre, self.brancheElv) 
            
        #
        # Les tâches
        #
        self.brancheTac = arbre.AppendItem(self.branche, Titres[8])
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
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Tache):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), LienSequence):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)           
            
        elif self.arbre.GetItemText(itemArbre) == Titres[6]: # Eleve
#            print u"Menu Séances"
            self.app.AfficherMenuContextuel([[u"Ajouter un élève", self.AjouterEleve]])
            
        elif self.arbre.GetItemText(itemArbre) == Titres[8]: # Tache
            self.app.AfficherMenuContextuel([[u"Ajouter une tâche", self.AjouterTache]])
         
        elif self.arbre.GetItemText(itemArbre) == Titres[10]: # Eleve
#            print u"Menu Séances"
            self.app.AfficherMenuContextuel([[u"Ajouter un professeur", self.AjouterProf]])
                                             
         
            
    ######################################################################################       
    def GetCompetencesUtil(self):
        """ Renvoie les listes des codes 
            des compétences utiles
            (pour tracé fiche)
        """
        lst = []
        for c in constantes.getAllCodes(constantes.dicCompetences_prj[self.classe.typeEnseignement]):
            for t in self.taches:
                if c in t.competences and not c in lst:
                    lst.append(c)
        lst.sort()
        return lst
    
    
    
    
    ######################################################################################  
    def GetNbrPhases(self):
        p = []
        for t in self.taches:
            if not t.phase in p:
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
#        rect = draw_cairo.posIntitule + draw_cairo.tailleIntitule
#        posi = draw_cairo.posPos + draw_cairo.taillePos
#        print self.rect


        
        branche = None
        autresZones = self.taches + self.eleves + [self.support]
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
            if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
                return self.branche
#        print branche
        return branche
        
    ######################################################################################  
    def HitTestPosition(self, x, y):
        if hasattr(self, 'rectPos'):
            for i, rectPos in enumerate(self.rectPos):
                if dansRectangle(x, y, (rectPos,)):
                    return i
                    
                                    
                                    
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        self.app.SetTitre()
        return
#        self.CI.MiseAJourTypeEnseignement()
#        for o in self.obj.values():
#            o.MiseAJourTypeEnseignement()
#        self.prerequis.MiseAJourTypeEnseignement()
        
        
    #############################################################################
    def VerrouillerClasse(self):
        self.classe.Verrouiller(len(self.GetCompetencesUtil()) == 0)
        
                
                
                
                
####################################################################################
#
#   Classe définissant les propriétés d'une séquence
#
####################################################################################
class CentreInteret(Objet_sequence):
    def __init__(self, parent, panelParent, numCI = []):
        Objet_sequence.__init__(self)
        self.parent = parent
        self.numCI = numCI
        self.SetNum(numCI)
        
        
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
        print "getBranche CI"
        root = ET.Element("CentresInteret")
        for i, num in enumerate(self.numCI):
            root.set("C"+str(i), str(num))
#        print ET.tostring(root)
        return root
    
    
#        print "getBranche CI",
        if hasattr(self, 'code'):
#            print "code CI", self.code
            if self.code == "":
                self.code = "_"
            root = ET.Element(self.code)
            return root
        
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche CI"
        self.numCI = []
#        print branche.keys()
        for i, s in enumerate(branche.keys()):
            self.numCI.append(eval(branche.get("C"+str(i), "")))
#        print self.numCI
        
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
            
#        print "setBranche CI"
        code = list(branche)[0].tag
#        print code
        if code == "_":
            num = []
            self.SetNum(num)
        else:
            num = eval(code[2:])-1
            self.SetNum(num)
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.MiseAJour()

    
    
    
    
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
        return constantes.CentresInterets[self.parent.classe.typeEnseignement][self.numCI[num]]
    
    
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
        if constantes.PositionCibleCIET != None:
            return constantes.PositionCibleCIET[self.numCI[num]]
    
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
        

        
    #############################################################################
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
            return self.branche
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
#        print "getBranche competences",
        root = ET.Element("Competences")
        for i, s in enumerate(self.competences):
            root.set("C"+str(i), s)
        return root
    
    
#        print "getBranche Comp",
#        if hasattr(self, 'code'):
#            print self.code
#            root = ET.Element(self.code)
#        else:
#            print
#            root = ET.Element("")
#        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche competences"
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
    
    #############################################################################
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
            return self.branche

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Compétences", wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Com"])
        
        
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
    def __init__(self, parent, panelParent, num = None):
        Objet_sequence.__init__(self)
        self.parent = parent
        self.num = num
        self.savoirs = []
        if panelParent:
            self.panelPropriete = PanelPropriete_Savoirs(panelParent, self)
        
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
#        print "getBranche Savoir",
        root = ET.Element("Savoirs")
        for i, s in enumerate(self.savoirs):
            root.set("S"+str(i), s)
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche Savoir"
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
        return constantes.getSavoir(self.parent, self.GetCode(num))  
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Savoirs", wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Sav"])
         
    
    #############################################################################
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
            return self.branche
        
        
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
        self.ordre = 1
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
#        self.description = ['<?xml version="1.0" encoding="UTF-8"?>\n<richtext version="1.0.0.0" xmlns="http://www.wxwidgets.org">\n']
        
#        for i in range(8):
#            self.systemes.append(Variable(u"", lstVal = 0, nomNorm = "", typ = VAR_ENTIER_POS, 
#                                 bornes = [0,8], modeLog = False,
#                                 expression = None, multiple = False))
        self.nombre = Variable(u"Nombre", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [1,10], modeLog = False,
                              expression = None, multiple = False)
        
        # Les autres données
        self.typeParent = typeParent
        self.parent = parent
        self.panelParent = panelParent
        
        self.SetType(typeSeance)
        self.sousSeances = []
        
        # Tip
        if self.GetApp():
            self.tip = PopupInfoSeance(self.GetApp(), u"Séance", self)
        
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
#        print "getBranche Séance", self.code
        root = ET.Element("Seance"+str(self.ordre))
        root.set("Type", self.typeSeance)
        root.set("Intitule", self.intitule)
#        print self.description
        if self.description != None:
            root.set("Description", self.description)
        
        self.lien.getBranche(root)
        
        if self.typeSeance in ["R", "S"]:
            for sce in self.sousSeances:
                root.append(sce.getBranche())
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
#        print "setBranche séance"
        self.ordre = eval(branche.tag[6:])
        
        self.intitule  = branche.get("Intitule", "")
        self.typeSeance = branche.get("Type", "C")
        self.description = branche.get("Description", None)
        
        self.lien.setBranche(branche, self.GetPath())
#        print "Lien séance", self.typeSeance, self.ordre,":", self.lien
#        self.SetLien()
        
        if self.typeSeance in ["R", "S"]:
            self.sousSeances = []
            for sce in list(branche):
                seance = Seance(self, self.panelParent)
                self.sousSeances.append(seance)
                seance.setBranche(sce)
            self.duree.v[0] = self.GetDuree()
            
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
#        print "effectif", self, eff
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
#        print "VerifPb", self
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
#        print "IsEffectifOk",
        ok = 0 # pas de problème
        if self.typeSeance in ["R", "S"] and len(self.sousSeances) > 0:
            if self.GetEffectif() < self.GetClasse().GetEffectifNorm('G'):
                ok = 1 # Tout le groupe "effectif réduit" n'est pas occupé
            elif self.GetEffectif() > self.GetClasse().GetEffectifNorm('G'):
                ok = 2 # Effectif de la séance supperieur à celui du groupe "effectif réduit"    
            if self.typeSeance == "R":
                continuer = True
                eff = self.sousSeances[0].GetEffectif()
                i = 1
                while continuer:
                    if i >= len(self.sousSeances):
                        continuer = False
                    else:
                        if self.sousSeances[i].GetEffectif() != eff:
                            ok = 3 # séance en rotation d'effectifs différents !!
                            continuer = False
                        i += 1
            
        elif self.typeSeance in ["AP", "ED"] and not self.EstSousSeance():
            if self.GetEffectif() < self.GetClasse().GetEffectifNorm('G'):
                ok = 1 # Tout le groupe "effectif réduit" n'est pas occupé
#        print ok
        return ok
            
    ######################################################################################  
    def IsNSystemesOk(self):
        """ Teste s'il y a un problème de nombre de systèmes disponibles
        """
        ok = 0 # pas de problème
        if self.typeSeance in ["AP", "ED"]:
#            print "IsNSystemeOk", self
            n = self.GetNbrSystemes()
#            print n
            seq = self.GetApp().sequence
#            print seq.systemes
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
                couleur = 'gold'
            elif etat == 2:
                couleur = 'orange'
            elif etat == 3:
                couleur = 'red'
            
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
            for sce in self.sousSeances:
                duree += sce.GetDuree()
        elif self.typeSeance == "S":
            duree += self.sousSeances[0].GetDuree()
        else:
            duree = self.duree.v[0]
        return duree
                
    ######################################################################################  
    def GetDureeGraph(self):
        return min(self.GetDuree(), 8)           
                
    ######################################################################################  
    def SetDuree(self, duree, recurs = True):
        """ Modifie la durée des Rotation et séances en Parallèle et de tous leurs enfants
            après une modification de durée d'un des enfants
        """
#        print "SetDuree", self.EstSousSeance()
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
    def SetIntitule(self, text):           
        self.intitule = text
        if self.intitule != "":
            self.tip.SetMessage(u"Intitulé : "+ "\n".join(textwrap.wrap(self.intitule, 40)))
        else:
            self.tip.SetMessage(u"")
        
#    ######################################################################################  
#    def SetEffectif(self, text):   
#        for k, v in Effectifs.items():
#            if v[0] == text:
#                codeEff = k
#        self.effectif = codeEff
           
    
    ######################################################################################  
    def SetDemarche(self, text):   
        for k, v in constantes.Demarches.items():
            if v[0] == text[0]:
                codeDem = k
        self.demarche = codeDem
        
        
    ######################################################################################  
    def SetType(self, typ):
#        print "SetType", typ
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
        self.tip.SetDescription()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.rtc.Ouvrir()
        if self.typeSeance in ["R", "S"]:
            for sce in self.sousSeances:
                sce.PubDescription() 
                
    ######################################################################################  
    def SetDescription(self, description):   
#        print "SetDescription", description
#        if description == None:
#            self.description
        if self.description != description:
            self.description = description
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.sendEvent()
            self.tip.SetDescription()
        
#        print "Fini"
            
    ######################################################################################  
    def SetCode(self):
#        print "SetCode",
        self.code = self.typeSeance
        num = str(self.ordre+1)
        if isinstance(self.parent, Seance):
            num = str(self.parent.ordre+1)+"."+num
            if isinstance(self.parent.parent, Seance):
                num = str(self.parent.parent.ordre+1)+"."+num

        self.code += num
#        print self.code
        if hasattr(self, 'codeBranche') and self.typeSeance != "":
            self.codeBranche.SetLabel(self.code)
            self.arbre.SetItemText(self.branche, constantes.TypesSeanceCourt[self.typeSeance])
#        else:
#            self.codeBranche.SetLabel("??")
#            self.arbre.SetItemText(self.branche, u"Séance :")
        
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for sce in self.sousSeances:
                sce.SetCode()

        # Tip
        self.tip.SetTitre(u"Séance "+ self.code)
        if self.typeSeance != "":
            self.tip.SetCode(u"Type : "+ constantes.TypesSeance[self.typeSeance])
        else:
            self.tip.SetCode(u"")
        if self.intitule != "":
            self.tip.SetMessage(u"Intitulé : "+ "\n".join(textwrap.wrap(self.intitule, 40)))
        else:
            self.tip.SetMessage(u"")
        
        
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
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for sce in self.sousSeances:
                sce.ConstruireArbre(arbre, self.branche)
            
        
    ######################################################################################  
    def OrdonnerSeances(self):
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for i, sce in enumerate(self.sousSeances):
                sce.ordre = i
        
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
        return
    
    ######################################################################################  
    def SupprimerSousSeances(self):
        self.arbre.DeleteChildren(self.branche)
        return
    
    ######################################################################################  
    def MiseAJourNomsSystemes(self):
#        print "MiseAJourNomsSystemes", self
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
#        print "SupprimerSysteme", self,id
#        print self.systemes
        if self.typeSeance in ["AP", "ED", "P"]:
            del self.systemes[id]
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.sousSeances:
                s.SupprimerSysteme(id)
        print self.systemes
        
        
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
    def GetNbrSystemes(self, complet = False):
        d = {}
        if self.typeSeance in ["S", "R"]:
            if self.typeSeance == "S" or complet:
                for seance in self.sousSeances:
                    for s in seance.systemes:
                        if s.n <>"":
                            if d.has_key(s.n):
                                d[s.n] += s.v[0]*self.nombre.v[0]
                            else:
                                d[s.n] = s.v[0]*self.nombre.v[0]
            else:
                for s in self.systemes:
                    if s.n <>"":
                        d[s.n] = s.v[0]*self.nombre.v[0]
        else:
            for s in self.systemes:
                if s.n <>"":
                    d[s.n] = s.v[0]*self.nombre.v[0]
        
     
        return d
        
        
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
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
    
                  
    def __init__(self, parent, panelParent, phaseTache = ""):
        """ Séance :
                parent = le parent wx pour contenir "panelPropriete"
                phaseTache = phase de la tache parmi 'Ana', 'Con', 'Rea', 'Val'
        """
    
        Objet_sequence.__init__(self)
        
        # Les données sauvegardées
        self.ordre = 1
        self.duree = Variable(u"Durée", lstVal = 1.0, nomNorm = "", typ = VAR_REEL_POS, 
                              bornes = [0.25,30], modeLog = False,
                              expression = None, multiple = False)
        self.intitule  = u""
        self.intituleDansDeroul = True
        
        # Les élèves concernés (liste de
        self.eleves = []
        
        # Les compétences abordées
        self.competences = []
        
        self.code = u""
        self.description = None

        # Les autres données
        self.parent = parent
        self.panelParent = panelParent
        
        self.phase = phaseTache
        
        # Tip
        if self.GetApp():
            self.tip = PopupInfoSeance(self.GetApp(), u"Tâche", self)
        
        
        if panelParent:
            self.panelPropriete = PanelPropriete_Tache(panelParent, self)
            
        
    
    ######################################################################################  
    def __repr__(self):
        t = self.phase + str(self.ordre+1) 
#        t += " " +str(self.GetDuree()) + "h"
#        t += " " +str(self.effectif)
#        for s in self.sousSeances:
#            t += "  " + s.__repr__()
        return t
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()

    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la tâche pour enregistrement
        """
#        print "getBranche Séance", self.code
        root = ET.Element("Tache"+str(self.ordre))
        root.set("Phase", self.phase)
        root.set("Intitule", self.intitule)
#        print self.description
        if self.description != None:
            root.set("Description", self.description)

        root.set("Duree", str(self.duree.v[0]))
        
        brancheElv = ET.Element("Eleves")
        root.append(brancheElv)
        for i, e in enumerate(self.eleves):
            brancheElv.set("Eleve"+str(i), str(e))
            
        brancheCmp = ET.Element("Competences")
        root.append(brancheCmp)
        for i, c in enumerate(self.competences):
            brancheCmp.set("Comp"+str(i), c)
        
        root.set("IntituleDansDeroul", str(self.intituleDansDeroul))
        
        return root    
        
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche séance"
        self.ordre = eval(branche.tag[5:])
        
        self.intitule  = branche.get("Intitule", "")
        self.phase = branche.get("Phase", "C")
        self.description = branche.get("Description", None)
        
        self.duree.v[0] = eval(branche.get("Duree", "1"))
        
        brancheElv = branche.find("Eleves")
        self.eleves = []
        for i, e in enumerate(brancheElv.keys()):
            self.eleves.append(eval(brancheElv.get("Eleve"+str(i))))
            
        brancheCmp = branche.find("Competences")
#        print brancheCmp.keys()
        self.competences = []
        for i, e in enumerate(brancheCmp.keys()):
            self.competences.append(brancheCmp.get("Comp"+str(i)))
        
        self.intituleDansDeroul = eval(branche.get("IntituleDansDeroul", "True"))
        
#        self.MiseAJourListeSystemes()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeEleves()
            self.panelPropriete.MiseAJourDuree()
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
        return self.duree.v[0]
                
    ######################################################################################  
    def GetDureeGraph(self):
        return min(self.GetDuree(), 8)       
    
    ######################################################################################  
    def SetDuree(self, duree):
        """ Modifie la durée de la tâche
        """
#        print "SetDuree", self.EstSousSeance()
        self.duree.v[0] = duree
        self.panelPropriete.MiseAJourDuree()
        self.parent.MiseAJourDureeEleves()
        
    ######################################################################################  
    def SetIntitule(self, text):           
        self.intitule = text
        if self.intitule != "":
            self.tip.SetMessage(u"Intitulé : "+ "\n".join(textwrap.wrap(self.intitule, 40)))
        else:
            self.tip.SetMessage(u"")
        
        
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
        self.tip.SetDescription()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.rtc.Ouvrir()

                
    ######################################################################################  
    def SetDescription(self, description):   
        if self.description != description:
            self.description = description
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.sendEvent()
            self.tip.SetDescription()
            
    ######################################################################################  
    def SetCode(self):
        num = str(self.ordre+1)

        if self.phase != "":
            self.code = self.phase[0]+num
        else:
            self.code = num

        if hasattr(self, 'codeBranche') and self.phase != "":
            self.codeBranche.SetLabel(self.code)
            self.arbre.SetItemText(self.branche, constantes.NOM_PHASE_TACHE[self.phase])
        
        
        # Tip
        self.tip.SetTitre(u"Tâche "+ self.code)
        if self.phase != "":
            self.tip.SetCode(u"Phase : "+ constantes.NOM_PHASE_TACHE[self.phase])
        else:
            self.tip.SetCode(u"")
        if self.intitule != "":
            self.tip.SetMessage(u"Intitulé : "+ "\n".join(textwrap.wrap(self.intitule, 40)))
        else:
            self.tip.SetMessage(u"")
        
        
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
                                 
        
        
    ######################################################################################  
    def SupprimerSysteme(self, id):
#        print "SupprimerSysteme", self,id
#        print self.systemes
        if self.typeSeance in ["AP", "ED", "P"]:
            del self.systemes[id]
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.sousSeances:
                s.SupprimerSysteme(id)
        print self.systemes
        
    ######################################################################################  
    def AjouterEleve(self):
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeEleves()
    
    ######################################################################################  
    def SupprimerEleve(self, i):
        if i in self.eleves:
            self.eleves.remove(i)
        for id in self.eleves:
            if id > i:
                self.eleves.remove(id)
                self.eleves.append(id-1)
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeEleves()
        
#    ######################################################################################  
#    def AjouterSysteme(self, nom = "", nombre = 0, construire = True):
#        if self.typeSeance in ["AP", "ED", "P"]:
#            self.systemes.append(Variable(nom, lstVal = nombre, nomNorm = "", typ = VAR_ENTIER_POS, 
#                                          bornes = [0,8], modeLog = False,
#                                          expression = None, multiple = False))
#            if construire and hasattr(self, 'panelPropriete'):
#                self.panelPropriete.ConstruireListeSystemes()
#        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
#            for s in self.sousSeances:
#                s.AjouterSysteme(nom, nombre)
#    
#    
#    ######################################################################################  
#    def AjouterListeSystemes(self, lstSys, lstNSys = None):
#        if self.typeSeance in ["AP", "ED", "P"]:
#            if lstNSys == None:
#                lstNSys = [0]*len(lstSys)
#            for i, s in enumerate(lstSys):
#                self.AjouterSysteme(s, lstNSys[i], construire = False)
#            if hasattr(self, 'panelPropriete'):
#                self.panelPropriete.ConstruireListeSystemes()
#            
#        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
#            for s in self.sousSeances:
#                s.AjouterListeSystemes(lstSys, lstNSys) 
                
                
    ######################################################################################  
    def GetDocument(self):    
        return self.parent
    
    ######################################################################################  
    def GetClasse(self):
        return self.GetDocument().classe
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            listItems = [[u"Supprimer", functools.partial(self.parent.SupprimerTache, item = itemArbre)]]
            self.GetApp().AfficherMenuContextuel(listItems)
#            item2 = menu.Append(wx.ID_ANY, u"Créer une rotation")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterRotation, item = item), item2)
#            
#            item3 = menu.Append(wx.ID_ANY, u"Créer une série")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterSerie, item = item), item3)
        
        
        
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
#            self.arbre.DoSelectItem(self.branche)
            return self.branche
        
        
        
        
        
        
        
        
        
        
        
        
        
        
####################################################################################
#
#   Classe définissant les propriétés d'un système
#
####################################################################################
class Systeme(ElementDeSequence):
    def __init__(self, parent, panelParent, nom = u""):
        
        ElementDeSequence.__init__(self)
        
        self.parent = parent
        self.nom = nom
        self.nbrDispo = Variable(u"Nombre dispo", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [0,20], modeLog = False,
                              expression = None, multiple = False)
        self.image = None
        
        # Tip
        self.tip = PopupInfoSysteme(parent.app, u"Système ou matériel")
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
#        print "getBranche systeme", self.nom
        root = ET.Element("Systeme")
        root.set("Nom", self.nom)
        self.lien.getBranche(root)
        root.set("Nbr", str(self.nbrDispo.v[0]))
        if self.image != None:
            root.set("Image", img2str(self.image.ConvertToImage()))
        
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche systeme"
        self.nom  = branche.get("Nom", "")
        self.lien.setBranche(branche, self.GetPath())
#        self.SetLien()
        self.nbrDispo.v[0] = branche.get("Nbr", 1)
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
            self.tip.SetCode(u"Nom : "+self.nom)
            self.tip.SetMessage(u"Nombre disponible : " + str(self.nbrDispo.v[0]))

    ######################################################################################  
    def SetImage(self):
        self.tip.SetImage(self.image)
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
#        self.codeBranche = wx.StaticText(self.arbre, -1, self.nom)
#        print "image",self.arbre.images["Sys"], self.image.GetWidth()
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
            
            
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
#            self.arbre.DoSelectItem(self.branche)
            return self.branche
    
    
    
        
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
class Support(ElementDeSequence):
    def __init__(self, parent, panelParent, nom = u""):
        
        ElementDeSequence.__init__(self)
        
        self.parent = parent
        self.nom = nom
        self.description = None
        
        self.image = None
        
        # Tip
        self.tip = PopupInfoSysteme(parent.app, u"Support")
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
#        print "getBranche systeme", self.nom
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
        print "setBranche support"
        self.nom  = branche.get("Nom", "")
        self.description = branche.get("Description", None)
        self.lien.setBranche(branche, self.GetPath())

        data = branche.get("Image", "")
        if data != "":
            self.image = PyEmbeddedImage(data).GetBitmap()
            
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.SetImage()
            self.panelPropriete.MiseAJour()

    
         
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
        self.tip.SetDescription()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.rtc.Ouvrir()
        
                
    ######################################################################################  
    def SetDescription(self, description):   
        if self.description != description:
            self.description = description
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.sendEvent()
            self.tip.SetDescription()
            
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
            self.tip.SetCode(u"Nom : "+self.nom)
            

    ######################################################################################  
    def SetImage(self):
        self.tip.SetImage(self.image)
        
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
            
            
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
#            self.arbre.DoSelectItem(self.branche)
            return self.branche
    
    
    
####################################################################################
#
#   Classe définissant les propriétés d'une personne
#
####################################################################################
class Personne():
    def __init__(self, parent, panelParent, id = 0):
        self.parent = parent
        self.nom = u""
        self.prenom = u""
        self.avatar = None
        self.id = id # Un identifiant unique = nombre > 0

        # Tip
        self.tip = PopupInfoSysteme(parent.app, self.titre.capitalize())
        if panelParent:
            self.panelPropriete = PanelPropriete_Personne(panelParent, self)

    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
        
    ######################################################################################  
    def __repr__(self):
        return self.nom+" "+self.prenom

    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
#        print "getBranche eleve", self.nom
        root = ET.Element(supprime_accent(self.titre).capitalize())
        root.set("Id", str(self.id))
        root.set("Nom", self.nom)
        root.set("Prenom", self.prenom)
        if self.avatar != None:
            root.set("Avatar", img2str(self.avatar.ConvertToImage()))
        
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche systeme"
        self.id  = eval(branche.get("Id", "0"))
        self.nom  = branche.get("Nom", "")
        self.prenom  = branche.get("Prenom", "")
        data = branche.get("Avatar", "")
        if data != "":
            self.avatar = PyEmbeddedImage(data).GetBitmap()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.SetImage()
            self.panelPropriete.MiseAJour()


    ######################################################################################  
    def GetNomPrenom(self):
        if self.nom == "" and self.prenom == "":
            return self.titre.capitalize()+' '+str(self.id)
        else:
            return self.prenom.capitalize() + ' ' + self.nom.upper()
         
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
            
        # Tip
        if hasattr(self, 'tip'):
            self.tip.SetCode(u"Nom : "+self.GetNomPrenom())

    ######################################################################################  
    def SetImage(self):
        self.tip.SetImage(self.avatar)
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, "")
#        print "image",self.arbre.images["Sys"], self.image.GetWidth()
#        if self.image == None or self.image == wx.NullBitmap:
        image = self.arbre.images[self.code]
#        else:
#            image = self.image.ConvertToImage().Scale(20, 20).ConvertToBitmap()
        self.branche = arbre.AppendItem(branche, self.titre.capitalize() + str(self.id), data = self, wnd = self.codeBranche,
                                        image = image)


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
class Eleve(Personne):
    def __init__(self, parent, panelParent, id = 0):
        
        self.titre = u"élève"
        self.code = "Elv"
        Personne.__init__(self, parent, panelParent, id)
            
    ######################################################################################  
    def GetDuree(self):
        d = 0
        for t in self.parent.taches:
            if self.id in t.eleves:
                d += t.GetDuree()
        return d
        
    ######################################################################################  
    def GetEvaluabilite(self):
        """ Renvoie l'évaluabilité
            % revue
            % soutenance
        """
        print "GetEvaluabilite", self, ":", 
        r = s = 0
        for c in self.GetCompetences():
            comp = constantes.dicCompetences_prj_simple[self.parent.classe.typeEnseignement][c]
            if len(comp) > 2:
                r += comp[1]
            else:
                s += comp[1]
                
        r = 1.0*r/constantes.NRB_COEF_COMP_R
        s = 1.0*s/constantes.NRB_COEF_COMP_S[self.parent.classe.typeEnseignement]   
        print r,s
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
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerEleve, item = itemArbre)]]
                                                    )
            
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect'):
#            print self.rect
            if dansRectangle(x, y, self.rect):
                return self.branche
#            for r in self.rect:
#                if dansRectangle(x, y, r):
#                    return self.branche
    
    
    ######################################################################################  
    def MiseAJourCodeBranche(self):
        duree = int(self.GetDuree())
        self.codeBranche.SetLabel("("+str(duree)+"h)")
        tol = 5
        if abs(duree-70) < tol:
            self.codeBranche.SetBackgroundColour(wx.GREEN)
        else:
            self.codeBranche.SetBackgroundColour(wx.NamedColor('PINK'))
            if duree < 70:
                self.codeBranche.SetToolTipString(u"Durée de travail insuffisante")
            else:
                self.codeBranche.SetToolTipString(u"Durée de travail trop importante")
    
        
    

####################################################################################
#
#   Classe définissant les propriétés d'un professeur
#
####################################################################################
class Prof(Personne):
    def __init__(self, parent, panelParent, id = 0):
        self.titre = u"prof"
        self.code = "Prf"
        Personne.__init__(self, parent, panelParent, id)
        
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerProf, item = itemArbre)]])
        
        
        
        
        
              
        
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
#        print "AfficherPanel"
        if self.panel != None:
            self.bsizer.Remove(self.panel)
            self.panel.Hide()
        self.panel = panel
        self.bsizer.Add(self.panel, 1, flag = wx.EXPAND|wx.GROW)
        
#        if isinstance(self.panel, PanelPropriete_Seance):
#            self.panel.AdapterAuxSystemes()
            
        self.panel.Show()
        self.bsizer.Layout()
        self.Refresh()
    
####################################################################################
#
#   Classes définissant la fenétre de l'application
#
####################################################################################
class FenetrePrincipale(aui.AuiMDIParentFrame):
    def __init__(self, parent, fichier):
        aui.AuiMDIParentFrame.__init__(self, parent, -1, __appname__,style=wx.DEFAULT_FRAME_STYLE)
        
        #
        # Taille et position de la fenétre
        #
        self.SetMinSize((800,570)) # Taille mini d'écran : 800x600
        self.SetSize((1024,738)) # Taille pour écran 1024x768
        # On centre la fenétre dans l'écran ...
        self.CentreOnScreen(wx.BOTH)
        
        #
        # le fichier de configuration de la fiche
        #
        self.nomFichierConfig = os.path.join(APP_DATA_PATH,"configFiche.cfg")
        # on essaye de l'ouvrir
        try:
            draw_cairo.ouvrirConfigFiche(self.nomFichierConfig)
        except:
            print "Erreur à l'ouverture de configFiche.cfg" 
            
            
        #############################################################################################
        # Instanciation et chargement des options
        #############################################################################################
        options = Options.Options()
        if options.fichierExiste():
#            try :
            options.ouvrir(DEFAUT_ENCODING)
#            except:
#                print "Fichier d'options corrompus ou inexistant !! Initialisation ..."
#                options.defaut()

#        print options
        
        # On applique les options ...
        self.DefinirOptions(options)
        
        #############################################################################################
        # Création du menu
        #############################################################################################
        self.CreateMenuBar()
        self.Bind(wx.EVT_MENU, self.commandeNouveau, id=10)
        self.Bind(wx.EVT_MENU, self.commandeOuvrir, id=11)
        self.Bind(wx.EVT_MENU, self.commandeEnregistrer, id=12)
        self.Bind(wx.EVT_MENU, self.commandeEnregistrerSous, id=13)
        self.Bind(wx.EVT_MENU, self.exporterFiche, id=15)
        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)
        
        self.Bind(wx.EVT_MENU, self.OnAide, id=21)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=22)
        
        self.Bind(wx.EVT_MENU, self.OnOptions, id=31)
        self.Bind(wx.EVT_MENU, self.OnRegister, id=32)
        
        
        self.Bind(EVT_APPEL_OUVRIR, self.OnAppelOuvrir)
        
        # Interception de la demande de fermeture
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
#        child = FenetreSequence(self)
        if fichier != "":
            self.ouvrir(fichier)
#        child.Show()
        
        
        
    ###############################################################################################
    def CreateMenuBar(self):
        # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(10, u"Nouveau")
        file_menu.Append(11, u"Ouvrir")
        file_menu.Append(12, u"Enregistrer")
        file_menu.Append(13, u"Enregistrer sous ...")
        file_menu.AppendSeparator()
        file_menu.Append(15, u"Exporter (PDF ou SVG)")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, u"Quitter")

        tool_menu = wx.Menu()
#        tool_menu.Append(31, u"Options")
        self.menuReg = tool_menu.Append(32, u"a")
        self.MiseAJourMenu()
        

        help_menu = wx.Menu()
        help_menu.Append(21, u"Aide en ligne")
        help_menu.AppendSeparator()
        help_menu.Append(22, u"A propos")

        mb.Append(file_menu, "&Fichier")
        mb.Append(tool_menu, "&Outils")
        mb.Append(help_menu, "&Aide")
        
        
        self.SetMenuBar(mb)
        
    def MiseAJourMenu(self):
        if register.IsRegistered():
            self.menuReg.SetText(u"Désinscrire de la base de registre")
        else:
            self.menuReg.SetText(u"Inscrire dans la base de registre")
            
            
            
    #############################################################################
    def DefinirOptions(self, options):
        
        self.options = options.copie()
        #
        # Options de Classe
        #
        
#        te = self.options.optClasse["TypeEnseignement"]
        lstCI = self.options.optClasse["CentresInteretET"]
        if False:
            pass
#        if self.fichierCourantModifie and (te != TYPE_ENSEIGNEMENT \
#           or (te == 'ET' and getTextCI(CentresInterets[TYPE_ENSEIGNEMENT]) != lstCI)):
#            dlg = wx.MessageDialog(self, u"Type de classe incompatible !\n\n" \
#                                         u"Fermer la séquence en cours d'élaboration\n" \
#                                         u"avant de modifier des options de la classe.",
#                               'Type de classe incompatible',
#                               wx.OK | wx.ICON_INFORMATION
#                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
#                               )
#            dlg.ShowModal()
#            dlg.Destroy()
        else:
#            TYPE_ENSEIGNEMENT = te
#            print self.options
            constantes.Effectifs["C"] = self.options.optClasse["Effectifs"]["C"]
            constantes.NbrGroupes["G"] = self.options.optClasse["Effectifs"]["G"]
            constantes.NbrGroupes["E"] = self.options.optClasse["Effectifs"]["E"]
            constantes.NbrGroupes["P"] = self.options.optClasse["Effectifs"]["P"]
                          
            constantes.CentresInteretsET = lstCI
                
            constantes.PositionCibleCIET = self.options.optClasse["PositionsCI_ET"]
                
                
    #############################################################################
    def OnRegister(self, event): 
        if register.IsRegistered():
            ok = register.UnRegister()
        else:
            ok = register.Register(PATH)
        if not ok:
            dlg = wx.MessageDialog(self, u"Accès à la base de registre refusé !\n" \
                                         u"Redémarrer pySequence en tant qu'administrateur.",
                               u"Accès refusé",
                               wx.OK | wx.ICON_WARNING
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.MiseAJourMenu()
         
    #############################################################################
    def OnAbout(self, event):
        win = A_propos(self)
        win.ShowModal()
        
    #############################################################################
    def OnAide(self, event):
        webbrowser.open('http://code.google.com/p/pysequence/wiki/Aide')
        
    #############################################################################
    def OnOptions(self, event, page = 0):
        options = self.options.copie()
#        print options
        dlg = Options.FenOptions(self, options)
        dlg.CenterOnScreen()
        dlg.nb.SetSelection(page)

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
    
        if val == wx.ID_OK:
#            print options
            self.DefinirOptions(options)
            self.AppliquerOptions()
            
        else:
            pass
#            print "You pressed Cancel"

        dlg.Destroy()
        
    
    ###############################################################################################
    def OnAppelOuvrir(self, evt):
        wx.CallAfter(self.ouvrir, evt.GetFile())
        
        
    ###############################################################################################
    def AppelOuvrir(self, nomFichier):
        evt = AppelEvent(myEVT_APPEL_OUVRIR, self.GetId())
        evt.SetFile(nomFichier)
        self.GetEventHandler().ProcessEvent(evt)
        
        
        
    ###############################################################################################
    def commandeNouveau(self, event = None, ext = None):
        if ext == 'seq':
            child = FenetreSequence(self)
        elif ext == 'prj':
            child = FenetreProjet(self)  # A faire : FenetreProjet
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
#        child.Show()
        if child != None:
            wx.CallAfter(child.Show)
        return child
        
    ###############################################################################################
    def ouvrir(self, nomFichier):
        if nomFichier != '':
            ext = os.path.splitext(nomFichier)[1].lstrip('.')
            if not nomFichier in self.GetNomsFichiers():
                wx.BeginBusyCursor()
                child = self.commandeNouveau(ext = ext)
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
        mesFormats = constantes.FORMAT_FICHIER['seq'] + constantes.FORMAT_FICHIER['prj'] + constantes.TOUS_FICHIER
  
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
        return self.GetActiveChild().sequence
    
    
    #############################################################################
    def GetNomsFichiers(self):
        lst = []
        for m in self.GetChildren():
            if isinstance(m, aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    if isinstance(k, FenetreSequence):
#                        print k.IsEnabled()
                        lst.append(k.fichierCourant)
#        print lst
        return lst
    
    
    #############################################################################
    def commandeEnregistrer(self, event = None):
        self.GetActiveChild().commandeEnregistrer(event)
        
    #############################################################################
    def commandeEnregistrerSous(self, event = None):
        self.GetActiveChild().commandeEnregistrerSous(event)
    
    #############################################################################
    def exporterFiche(self, event = None):
        self.GetActiveChild().exporterFiche(event)
    
    #############################################################################
    def OnClose(self, evt):
        try:
            draw_cairo.enregistrerConfigFiche(self.nomFichierConfig)
        except IOError:
            print "   Permission d'enregistrer les options refusée...",
        except:
            print "   Erreur enregistrement options...",
            
#        try:
        self.options.definir()
        self.options.enregistrer()
#        except IOError:
#            print "   Permission d'enregistrer les options refusée...",
#        except:
#            print "   Erreur enregistrement options...",
        
        # Close all ChildFrames first else Python crashes
        toutferme = True
        for m in self.GetChildren():
            if isinstance(m, aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    if isinstance(k, FenetreSequence):
                        toutferme = toutferme and k.quitter()  
        
        print "OnClose fini"
        if toutferme:
            evt.Skip()
            sys.exit()
#        print self.Destroy()
        
        
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
                         Bottom().Layer(1).
                         Floatable(False).
                         BestSize((-1, 200)).
                         MinSize((-1, 200)).
#                         DockFixed().
#                         Gripper(False).
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
   
#        self.Layout()
#        print "Fin instanciation Seq"
        wx.CallAfter(self.Layout)
        self.Layout()
#        wx.CallAfter(self.ficheSeq.Redessiner)
        
        

    #############################################################################
    def fermer(self):
#        self.Reparent(None)
        self.Destroy()
        return True
        
    #############################################################################
    def getNomFichierCourantCourt(self):
        return os.path.splitext(os.path.split(self.fichierCourant)[-1])[0]
    
    #############################################################################
    def MarquerFichierCourantModifie(self, modif = True):
        self.fichierCourantModifie = modif
        self.SetTitre(modif)
        print "modif !"
        
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
#            print "Nouveau dossier de sauvegarde", self.DossierSauvegarde
        else:
            dlg.Destroy()
    
    #############################################################################
    def commandeEnregistrer(self, event = None):
#        print "fichier courant :",self.fichierCourant
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
    def exporterFiche(self, event = None):
        mesFormats = "pdf (.pdf)|*.pdf|" \
                     "svg (.svg)|*.svg|" \
                     "swf (.swf)|*.swf"
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
#            print ext
            wx.BeginBusyCursor()
            if ext == ".pdf":
                try:
                    PDFsurface = cairo.PDFSurface(path, 595, 842)
                except IOError:
                    Dialog_ErreurAccesFichier(path)
                    wx.EndBusyCursor()
                    return
                
                ctx = cairo.Context (PDFsurface)
                ctx.scale(820, 820) 
                if self.typ == 'seq':
                    draw_cairo.Draw(ctx, self.sequence)
                elif self.typ == 'prj':
                    draw_cairo_prj.Draw(ctx, self.projet)
                self.DossierSauvegarde = os.path.split(path)[0]
                PDFsurface.finish()
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
                    draw_cairo.Draw(ctx, self.sequence, mouchard = True)
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
        
        for p in doc.getElementsByTagName("path"):
            a = p.getAttribute("d")
            a = str(a).translate(None, 'MCLZ')
            l = a.split()
            if len(l) > 1:
                x, y = l[0], l[1]
                x, y = eval(x), eval(y)
                
                for pt, obj, flag in pts_caract:
                    if match((x, y), pt) :
#                        print "Trouvé", pt, flag, obj
                        obj.cadre.append((p, flag))
                        if type(flag) != str:
                            break 
        
        if self.typ == 'seq':
            self.sequence.EnrichiSVG(doc)
            
        doc.writexml(f, '   ')
        f.close

 
 
def Dialog_ErreurAccesFichier(nomFichier):
    dlg = wx.MessageDialog(None, u"Impossible d'accéder au fichier\n%s\nen écriture !" %nomFichier,
                               'Erreur !',
                               wx.OK | wx.ICON_ERROR
                               )
    dlg.ShowModal()
    dlg.Destroy()

########################################################################################
#
#
#  Classe définissant la fenêtre "Séquence"
#
#
########################################################################################
class FenetreSequence(FenetreDocument):
    def __init__(self, parent):
        FenetreDocument.__init__(self, parent)
        
        self.typ = 'seq'
        
        #
        # La classe
        #
        self.classe = Classe(self, self.panelProp)
        
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
        # Zone graphique de la fiche de séquence
        #
        self.ficheSeq = FicheSequence(self.nb, self.sequence)
        
        self.nb.AddPage(self.ficheSeq, u"Fiche Séquence")
        
        self.miseEnPlace()
     
            
    ###############################################################################################
    def OnDocModified(self, event):
#        print "OnDocModified",event.GetSequence(), self.sequence
        if event.GetDocument() == self.sequence:
            self.sequence.VerifPb()
            self.ficheSeq.Redessiner()
            self.MarquerFichierCourantModifie()
              
        
    ###############################################################################################
    def enregistrer(self, nomFichier):

        wx.BeginBusyCursor()
        fichier = file(nomFichier, 'w')
        
        # La séquence
        sequence = self.sequence.getBranche()
#        print ET.tostring(sequence)
        classe = self.classe.getBranche()
        
        # La racine
        root = ET.Element("Sequence_Classe")
        root.append(sequence)
        root.append(classe)
        indent(root)
        
        ET.ElementTree(root).write(fichier)
        
        fichier.close()
        self.definirNomFichierCourant(nomFichier)
        self.MarquerFichierCourantModifie(False)
        wx.EndBusyCursor()
        
        
        
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True):
#        print "ouvrir", nomFichier
        
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
                
        except Exception as inst:
            dlg = wx.MessageDialog(self, u"La séquence pédagogique\n%s\n n'a pas pu être ouverte !" %nomFichier,
                               u"Erreur d'ouverture",
                               wx.OK | wx.ICON_WARNING
                               )
            dlg.ShowModal()
            dlg.Destroy()
            fichier.close()
            wx.EndBusyCursor()
            return

        self.arbre.DeleteAllItems()
        root = self.arbre.AddRoot("")
        self.classe.ConstruireArbre(self.arbre, root)
        self.sequence.ConstruireArbre(self.arbre, root)
        
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

        if redessiner:
            wx.CallAfter(self.ficheSeq.Redessiner)
        
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
        FenetreDocument.__init__(self, parent)
        
        self.typ = 'prj'
        
        #
        # La classe
        #
        self.classe = Classe(self, self.panelProp, pourProjet = True)
        
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
        
        #
        # Zone graphique de la fiche de projet
        #
        self.fichePrj = FicheProjet(self.nb, self.projet)
        
        self.nb.AddPage(self.fichePrj, u"Fiche Projet")
        
        self.miseEnPlace()
     
            
    ###############################################################################################
    def OnDocModified(self, event):
#        print "OnDocModified",event.GetSequence(), self.sequence
        if event.GetDocument() == self.projet:
            self.projet.VerifPb()
            self.fichePrj.Redessiner()
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
        
        ET.ElementTree(root).write(fichier)
        
        fichier.close()
        self.definirNomFichierCourant(nomFichier)
        self.MarquerFichierCourantModifie(False)
        wx.EndBusyCursor()
        
        
        
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True):
#        print "ouvrir", nomFichier
        
        fichier = open(nomFichier,'r')
        self.definirNomFichierCourant(nomFichier)
#        try:
        root = ET.parse(fichier).getroot()
        
        # Le projet
        projet = root.find("Projet")
        if projet == None:
            self.projet.setBranche(root)
            
        else:
            # La classe
            classe = root.find("Classe")
            self.classe.setBranche(classe)
            self.projet.setBranche(projet)  
                
#        except Exception as inst:
#            dlg = wx.MessageDialog(self, u"Le projet\n%s\n n'a pas pu être ouvert !" %nomFichier,
#                               u"Erreur d'ouverture",
#                               wx.OK | wx.ICON_WARNING
#                               )
#            dlg.ShowModal()
#            dlg.Destroy()
#            fichier.close()
#            wx.EndBusyCursor()
#            return

        self.arbre.DeleteAllItems()
        root = self.arbre.AddRoot("")
        print "1"
        self.classe.ConstruireArbre(self.arbre, root)
        self.projet.ConstruireArbre(self.arbre, root)
        print "2"
        self.projet.OrdonnerTaches()
        self.projet.PubDescription()
        self.projet.SetLiens()
        self.projet.MiseAJourDureeEleves()
        self.projet.MiseAJourNomProfs()
#        self.projet.MiseAJourNomProfs()
        self.projet.VerrouillerClasse()
        self.arbre.SelectItem(self.classe.branche)

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        
        fichier.close()

        if redessiner:
            wx.CallAfter(self.fichePrj.Redessiner)
        
    #############################################################################
    def definirNomFichierCourant(self, nomFichier = ''):
        self.fichierCourant = nomFichier
        self.projet.SetPath(nomFichier)
        self.SetTitre()

    
    #############################################################################
    def AppliquerOptions(self):
        self.projet.AppliquerOptions() 
    
    
#        print "fichier courant :",self.fichierCourant
#        if self.fichierCourant != '':
#            s = u"'Oui' pour enregistrer la séquence dans le fichier\n"
#            s += self.fichierCourant
#            s += ".\n\n"
#            s += u"'Non' pour enregistrer la séquence dans un autre fichier."
#            
#            dlg = wx.MessageDialog(self, s,
#                                   u'Enregistrement',
#                                     wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
#                                     )
#            res = dlg.ShowModal()
#            dlg.Destroy() 
#            if res == wx.ID_YES:
#                self.enregistrer(self.fichierCourant)
#            elif res == wx.ID_NO:
#                self.dialogEnregistrer('seq')
#            
#            
#        else:
#            self.dialogEnregistrer('seq')
            

        
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
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDClick)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRClick)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_MOTION, self.OnMove)


    ######################################################################################################
    def OnLeave(self, evt = None):
        if hasattr(self, 'call') and self.call.IsRunning():
            self.call.Stop()
#        if hasattr(self, 'tip') 
#            self.tip.Show(False)

    ######################################################################################################
    def OnEnter(self, event):
#        print "OnEnter"
#        self.OnLeave()
        self.SetFocus()
        event.Skip()
        
    #############################################################################            
    def OnResize(self, evt):
#        print "OnSize fiche",
        w, h = self.GetClientSize()
#        print self.GetScrollThumb(wx.VERTICAL)
        self.SetVirtualSize((w,w*29/21)) # Mise au format A4
#        print w
#        self.ficheSeq.FitInside()

        self.InitBuffer()
        if w > 0 and self.IsShown():
            self.Redessiner()


    #############################################################################            
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

        
    #############################################################################            
    def InitBuffer(self):
        w,h = self.GetVirtualSize()
#        print "InitBuffer", w, h
        self.buffer = wx.EmptyBitmap(w,h)

    #############################################################################            
    def Redessiner(self, event = None):  
#        print "REDESSINER"

        cdc = wx.ClientDC(self)
        dc = wx.BufferedDC(cdc, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        ctx = wx.lib.wxcairo.ContextFromDC(dc)
#        face = wx.lib.wxcairo.FontFaceFromFont(wx.FFont(10, wx.SWISS, wx.FONTFLAG_BOLD))
#        ctx.set_font_face(face)
        dc.BeginDrawing()
        self.normalize(ctx)
        self.Draw(ctx)
        dc.EndDrawing()
        self.ctx = ctx
        self.Refresh()
    
    
    #############################################################################            
    def normalize(self, cr):
        w,h = self.GetVirtualSize()
#        print "normalize", h
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
    def OnMove(self, evt):
#        print "OnMove"
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
                self.call = wx.CallLater(800, elem.tip.Show, True)
                self.tip = elem.tip
        evt.Skip()


    #############################################################################            
    def Draw(self, ctx):
        draw_cairo.Draw(ctx, self.sequence)
        
        
    #############################################################################            
    def OnClick(self, evt):
#        print "OnClick"
        x, y = evt.GetX(), evt.GetY()
        _x, _y = self.CalcUnscrolledPosition(x, y)
        xx, yy = self.ctx.device_to_user(_x, _y)
        
        #
        # Changement de branche sur l'arbre
        #
        branche = self.sequence.HitTest(xx, yy)
        if branche != None:
            self.sequence.arbre.SelectItem(branche)


        #
        # Autres actions
        #
        position = self.sequence.HitTestPosition(xx, yy)
        if position != None:
            self.sequence.SetPosition(position)
            if hasattr(self.sequence, 'panelPropriete'):
                self.sequence.panelPropriete.SetBitmapPosition(bougerSlider = position)
            
        return branche
    
    #############################################################################            
    def OnDClick(self, evt):
#        print "DClick"
        item = self.OnClick(evt)
        if item != None:
            self.sequence.AfficherLien(item)
        
    #############################################################################            
    def OnRClick(self, evt):
        item = self.OnClick(evt)
#        print "RClick", item
        if item != None:
            self.sequence.AfficherMenuContextuel(item)
        
    





    
####################################################################################
#
#   Classe définissant la fenétre de la fiche de séquence
#
####################################################################################
class FicheProjet(BaseFiche):
    def __init__(self, parent, projet):
        BaseFiche.__init__(self, parent)
        self.projet = projet

            
    ######################################################################################################
    def OnMove(self, evt):
#        print "OnMove"
        if hasattr(self, 'tip'):
            self.tip.Show(False)
            self.call.Stop()
        x, y = evt.GetPosition()
        _x, _y = self.CalcUnscrolledPosition(x, y)
        xx, yy = self.ctx.device_to_user(_x, _y)
        branche = self.projet.HitTest(xx, yy)
        if branche != None:
            elem = branche.GetData()
            if hasattr(elem, 'tip'):
                x, y = self.ClientToScreen((x, y))
                elem.tip.Position((x,y), (0,0))
                self.call = wx.CallLater(800, elem.tip.Show, True)
                self.tip = elem.tip
        evt.Skip()


    #############################################################################            
    def Draw(self, ctx):
        draw_cairo_prj.Draw(ctx, self.projet)
        
        
    #############################################################################            
    def OnClick(self, evt):
#        print "OnClick"
        x, y = evt.GetX(), evt.GetY()
        _x, _y = self.CalcUnscrolledPosition(x, y)
        xx, yy = self.ctx.device_to_user(_x, _y)
        
        #
        # Changement de branche sur l'arbre
        #
        branche = self.projet.HitTest(xx, yy)
        if branche != None:
            self.projet.arbre.SelectItem(branche)


        #
        # Autres actions
        #
        position = self.projet.HitTestPosition(xx, yy)
        if position != None:
            self.projet.SetPosition(position)
            if hasattr(self.projet, 'panelPropriete'):
                self.projet.panelPropriete.SetBitmapPosition(bougerSlider = position)
            
        return branche
    
    #############################################################################            
    def OnDClick(self, evt):
#        print "DClick"
        item = self.OnClick(evt)
        if item != None:
            self.projet.AfficherLien(item)
        
    #############################################################################            
    def OnRClick(self, evt):
        item = self.OnClick(evt)
#        print "RClick", item
        if item != None:
            self.projet.AfficherMenuContextuel(item)
            
            
            
            
                         
                
####################################################################################
#
#   Classe définissant le panel de propriété par défaut
#
####################################################################################
DELAY = 100 # Delai en millisecondes avant de rafraichir l'affichage suite à un saisie au clavier
class PanelPropriete(scrolled.ScrolledPanel):
    def __init__(self, parent, titre = u"", objet = None):
        scrolled.ScrolledPanel.__init__(self, parent, -1, style = wx.VSCROLL | wx.RETAINED)#|wx.BORDER_SIMPLE)
        
        self.sizer = wx.GridBagSizer()
        self.Hide()
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
#        self.SetScrollRate(20,20)
        self.SetupScrolling()
#        self.EnableScrolling(True, True)
        self.eventAttente = False
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)

    ######################################################################################################
    def OnEnter(self, event):
#        print "OnEnter"
        self.SetFocus()
#        self.sizer.RecalcSizes()
#        self.Layout()
       
    #########################################################################################################
    def sendEvent(self, doc = None):
        print "sendEvent", doc
        evt = SeqEvent(myEVT_DOC_MODIFIED, self.GetId())
        if doc != None:
            evt.SetDocument(doc)
        else:
            evt.SetDocument(self.GetDocument())
        
        self.GetEventHandler().ProcessEvent(evt)
        self.eventAttente = False


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
#        w = 0.5 - draw_cairo.ecartX
        imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  larg, int(h/w*larg))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        ctx = cairo.Context(imagesurface)
        ctx.scale(larg/w, larg/w) 
        draw_cairo.DrawPeriodes(ctx, self.sequence.position, origine = True)

        bmp = wx.lib.wxcairo.BitmapFromImageSurface(imagesurface)
#        print bmp.GetWidth(), bmp.GetHeight()
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
        
        titre = wx.StaticBox(self, -1, u"Intitulé du projet")
        sb = wx.StaticBoxSizer(titre)
        textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        self.sizer.Add(sb, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
#        self.sizer.Add(textctrl, (0,1), flag = wx.EXPAND)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        titre = wx.StaticBox(self, -1, u"Problématique")
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
        position = wx.Slider(self, -1, self.projet.position, 0, 5, (30, 60), (190, -1), 
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
#        w = 0.5 - draw_cairo.ecartX
        imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  larg, int(h/w*larg))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        ctx = cairo.Context(imagesurface)
        ctx.scale(larg/w, larg/w) 
        draw_cairo_prj.DrawPeriodes(ctx, self.projet.position, origine = True)

        bmp = wx.lib.wxcairo.BitmapFromImageSurface(imagesurface)
#        print bmp.GetWidth(), bmp.GetHeight()
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
    def EvtText(self, event):
        if event.GetEventObject() == self.textctrl:
            self.projet.SetText(event.GetString())
        else:
            self.projet.SetProblematique(event.GetString())
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.textctrl.ChangeValue(self.projet.intitule)
        self.commctrl.ChangeValue(self.projet.problematique)
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
        self.classe = classe
        self.pasVerrouille = True
        

        #
        # Type d'enseignement
        #
        rb = wx.RadioBox(
                self, -1, u"Type d'enseignement", wx.DefaultPosition, (120,-1),
                constantes.listEnseigmenent, 1, wx.RA_SPECIFY_COLS
                )
        rb.SetToolTip(wx.ToolTip(u"Choisir le type d'enseignement" ))
        for i, e in enumerate(constantes.listEnseigmenent):
            rb.SetItemToolTip(i, constantes.Enseigmenent[e])
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
        if pourProjet:
            rb.EnableItem(0, False) 
            rb.SetStringSelection(self.classe.typeEnseignement)
            
        self.sizer.Add(rb, (0,0), flag = wx.EXPAND|wx.ALL)
        self.cb_type = rb
        
        #
        # Centres d'intérêt
        #
        if not pourProjet:
            sb1 = wx.StaticBox(self, -1, u"Centres d'intérêt ET", size = (200,-1))
            sbs1 = wx.StaticBoxSizer(sb1,wx.VERTICAL)
            list = ULC.UltimateListCtrl(self, -1, 
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
             
            list.InsertColumnInfo(0, info)
    
            info = ULC.UltimateListItem()
            info._format = wx.LIST_FORMAT_LEFT
            info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_FONT
            info._text = u"Intitulé"
            
            list.InsertColumnInfo(1, info)
            
            list.SetColumnWidth(0, 35)
            list.SetColumnWidth(1, -3)
            
            
            for i,p in enumerate(['M', 'E', 'I', 'F', 'S', 'C']):
                info = ULC.UltimateListItem()
                info._mask = wx.LIST_MASK_TEXT
                info._format = wx.LIST_FORMAT_CENTER
                info._text = p
                
                list.InsertColumnInfo(i+2, info)
                list.SetColumnWidth(i+2, 20)
            
                
            
            self.list = list
            self.PeuplerListe()
            
            self.list.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
            self.list.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            self.leftDown = False
            
    #        txt = wx.TextCtrl(self, -1, getTextCI(self.classe.ci_ET),
    #                          style = wx.TE_MULTILINE)
            sbs1.Add(list, flag = wx.EXPAND|wx.ALL, border = 5)
    #        txt.Bind(wx.EVT_TEXT, self.EvtTxtCI)
    #        self.txtCi = txt
            if self.classe.typeEnseignement != 'ET' :
                self.list.Enable(False)
            
            btn = wx.Button(self, -1, u"Sélectionner depuis un fichier Excel (.xls)")
            aide = u"Sélectionner depuis un fichier Excel (.xls)"
            btn.SetToolTip(wx.ToolTip(aide))
            btn.SetHelpText(aide)
            self.btn = btn
            sbs1.Add(btn, flag = wx.EXPAND|wx.ALL, border = 5)
            self.Bind(wx.EVT_BUTTON, self.SelectCI, btn)
            self.sizer.Add(sbs1, (0,2), flag = wx.EXPAND|wx.ALL)    
            
            self.sizer.AddGrowableCol(2)
        
        
        
        #
        # Effectifs
        #
        self.ec = PanelEffectifsClasse(self, classe)
        self.sizer.Add(self.ec, (0,1), flag = wx.EXPAND|wx.ALL|wx.ALIGN_RIGHT)
    
    
    #############################################################################            
    def GetDocument(self):
        return self.classe.doc
    
    
        
    ######################################################################################  
    def EvtRadioBox(self, event):
#        print event.GetEventObject().GetValue()
        self.classe.typeEnseignement = self.cb_type.GetItemLabel(event.GetInt())
            
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
#        print i, ":", 
        s = self.classe.posCI_ET[numCI] 
        if not event.IsChecked():
            t = " "
        else:
            t = posCI
        s = s[:i]+t+s[i+1:]    
#        print self.classe.posCI_ET[numCI], "-->",
        self.classe.posCI_ET[numCI] = s
#        print self.classe.posCI_ET[numCI]
#        print self.classe
        self.classe.doc.CI.panelPropriete.construire()
        self.sendEvent()
        
        
    ######################################################################################  
    def MiseAJourType(self):
        if hasattr(self, 'list'):
            self.list.Enable(self.pasVerrouille and self.classe.typeEnseignement == 'ET')
            self.btn.Enable(self.pasVerrouille and self.classe.typeEnseignement == 'ET')
            
    ######################################################################################  
    def MiseAJour(self):
        self.MiseAJourType()
        self.cb_type.SetStringSelection(self.classe.typeEnseignement)
        
        if hasattr(self, 'list'):
            self.PeuplerListe()
                
        self.ec.MiseAJour()

    ######################################################################################  
    def PeuplerListe(self):
        # Peuplement de la liste
        self.list.DeleteAllItems()
        for i,ci in enumerate(self.classe.ci_ET):
#            item = ULC.UltimateListItem()
#            item.SetText("CI"+str(i))
            index = self.list.InsertStringItem(sys.maxint, "CI"+str(i+1))
#            item = self.list.GetItem(i, 1)
#            tx = wx.TextCtrl(self.list, 200+i, ci)
#            item.SetWindow(tx)
#            self.list.SetItem(item)
            self.list.SetStringItem(index, 1, ci)
            
#            w = self.list.GetColumnWidth(1)
           
            for j,p in enumerate(['M', 'E', 'I', 'F', 'S', 'C']):
                item = self.list.GetItem(i, j+2)
                
                cb = wx.CheckBox(self.list, 100+i,"", name = p)
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
        
#    ######################################################################################  
#    def EvtTxtCI(self, event):
#        self.classe.ci_ET =  event.GetString()
#        if not self.eventAttente:
#            wx.CallLater(DELAY, self.sendEvent)
#            self.eventAttente = True
        
#    ######################################################################################  
#    def EvtVariableEff(self, event):
#        le, leff = zip(*self.varEff.items())
#        var = event.GetVar()
#        i = leff.index(var)
#        self.classe.effectifs[le[i]][1] = var.v[0]
#        self.sendEvent()

    ######################################################################################  
    def SelectCI(self, event = None):
        if recup_excel.ouvrirFichierExcel():
            dlg = wx.MessageDialog(self.Parent, u"Sélectionner une liste de CI\n" \
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
                self.classe.ci_ET = ls
                self.MiseAJour()
                self.sendEvent()
            elif res == wx.ID_NO:
                print "Rien" 
        
    ######################################################################################  
    def Verrouiller(self, etat):
        self.cb_type.Enable(etat)
        if hasattr(self, 'list'):
            self.list.Enable(etat and (self.classe.typeEnseignement == 'ET'))
            self.btn.Enable(etat and (self.classe.typeEnseignement == 'ET'))
        self.pasVerrouille = etat
#        for c in self.GetChildren():
#            self.Enable(etat)





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
#        print "OnKillFocus"
        txtctrl = evt.GetEventObject()
#        print txtctrl.GetValue()
        self.liste.SetStringItem(self.index, 1, txtctrl.GetValue())
        self.classe.ci_ET[self.index] = txtctrl.GetValue()
        self.classe.sequence.CI.panelPropriete.construire()
#        self.item.SetText(txtctrl.GetValue())
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
#        boxClasse = wx.StaticBox(self, -1, u"Effectifs "+constantes.NomsEffectifs['C'][0], style = wx.BORDER_RAISED)
        boxClasse = wx.StaticBox(self, -1, u"Découpage de la classe", style = wx.BORDER_RAISED)
#        print boxClasse.GetClassDefaultAttributes()
#        print dir(boxClasse)
#        boxClasse.GetClassDefaultAttributes().colFg = wx.RED
        
        r,v,b = constantes.CouleursGroupes['C']
        coulClasse = wx.Colour(r*255,v*255,b*255)
        boxClasse.SetOwnForegroundColour(coulClasse)
        
        r,v,b = constantes.CouleursGroupes['G']
        self.coulEffRed = wx.Colour(r*255,v*255,b*255)
        
        r,v,b = constantes.CouleursGroupes['E']
        self.coulEP = wx.Colour(r*255,v*255,b*255)
        
        r,v,b = constantes.CouleursGroupes['P']
        self.coulAP = wx.Colour(r*255,v*255,b*255)
        
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
        self.cEffClas = VariableCtrl(self, self.vEffClas, coef = 1, labelMPL = False, signeEgal = False,
                                help = u"Nombre d'élèves dans la classe entière", sizeh = 30, color = coulClasse)
        self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cEffClas)
        sizerClasse_h.Add(self.cEffClas, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 5)
        
        # Nombre de groupes à effectif réduits
        self.vNbERed = Variable(u"Nbr de groupes\nà effectif réduit",  
                                lstVal = classe.nbrGroupes['G'], 
                                typ = VAR_ENTIER_POS, bornes = [1,3])
        self.cNbERed = VariableCtrl(self, self.vNbERed, coef = 1, labelMPL = False, signeEgal = False,
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
                            typ = VAR_ENTIER_POS, bornes = [1,5])
        self.cNbEtPr = VariableCtrl(self, self.vNbEtPr, coef = 1, labelMPL = False, signeEgal = False,
                                help = u"Nombre de groupes d'étude/projet par groupe à effectif réduit", sizeh = 20, color = self.coulEP)
        self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cNbEtPr)
        self.sizerEffRed_g.Add(self.cNbEtPr, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 3)
        
        self.BoxEP = wx.StaticBox(self, -1, u"", size = (30, -1))
        self.BoxEP.SetOwnForegroundColour(self.coulEP)
        self.BoxEP.SetMinSize((30, -1))     
        bsizer = wx.StaticBoxSizer(self.BoxEP, wx.VERTICAL)
        self.sizerEffRed_g.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
            
        # Nombre de groupes d'activité pratique
        self.vNbActP = Variable(u"Nbr de groupes\n\"Activités pratiques\"",  
                            lstVal = classe.nbrGroupes['P'], 
                            typ = VAR_ENTIER_POS, bornes = [2,10])
        self.cNbActP = VariableCtrl(self, self.vNbActP, coef = 1, labelMPL = False, signeEgal = False,
                                help = u"Nombre de groupes d'activité pratique par groupe à effectif réduit", sizeh = 20, color = self.coulAP)
        self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cNbActP)
        self.sizerEffRed_d.Add(self.cNbActP, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 3)
        
        self.BoxAP = wx.StaticBox(self, -1, u"", size = (30, -1))
        self.BoxAP.SetOwnForegroundColour(self.coulAP)
        self.BoxAP.SetMinSize((30, -1))     
        bsizer = wx.StaticBoxSizer(self.BoxAP, wx.VERTICAL)
        self.sizerEffRed_d.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
        
        
        self.lstBoxEffRed = []
        self.lstBoxEP = []
        self.lstBoxAP = []
        
        self.AjouterGroupesVides()
        
        self.MiseAJourNbrEleve()

        border = wx.BoxSizer()
        border.Add(bsizerClasse, 1, wx.EXPAND)
        self.SetSizer(border)
        
#        self.SetSizerAndFit(bsizerClasse)
    
    
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
        self.AjouterGroupesVides()
        self.MiseAJourNbrEleve()
        
    def AjouterGroupesVides(self):
        return
        for g in self.lstBoxEP:
            self.sizerEffRed_g.Remove(g)
        for g in self.lstBoxAP:
            self.sizerEffRed_d.Remove(g)    
        for g in self.lstBoxEffRed:
            self.sizerClasse_b.Remove(g)
        
        self.lstBoxEffRed = []
        self.lstBoxEP = []
        self.lstBoxAP = []    
        
        for g in range(self.classe.nbrGroupes['G'] - 1):
            box = wx.StaticBox(self, -1, u"Eff Red", size = (30, -1))
            box.SetOwnForegroundColour(self.coulEffRed)
            box.SetMinSize((30, -1))
            self.lstBoxEffRed.append(box)
            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
            self.sizerClasse_b.Add(bsizer, flag = wx.EXPAND)
        
        for g in range(self.classe.nbrGroupes['E']):
            box = wx.StaticBox(self, -1, u"E/P", size = (30, -1))
            box.SetOwnForegroundColour(self.coulEP)
            box.SetMinSize((30, -1))
            self.lstBoxEP.append(box)
            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
#            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
            self.sizerEffRed_g.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
            
        
        for g in range(self.classe.nbrGroupes['P']):
            box = wx.StaticBox(self, -1, u"AP", size = (30, -1))
            box.SetOwnForegroundColour(self.coulAP)
            box.SetMinSize((30, -1))
            self.lstBoxAP.append(box)
            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
#            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
            self.sizerEffRed_d.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
        
        self.Layout()
        
    
    def MiseAJourNbrEleve(self):
        self.boxEffRed.SetLabel(strEffectifComplet(self.classe, 'G', -1))
        t = u"groupes de "
        self.BoxEP.SetLabel(t+strEffectif(self.classe, 'E', -1))
        self.BoxAP.SetLabel(t+strEffectif(self.classe, 'P', -1))
        
        self.Refresh()
        
        
    def MiseAJour(self):
#        print "MiseAJour PanelEffClasse"
        self.vEffClas.v[0] = self.classe.effectifs['C']
        self.vNbERed.v[0] = self.classe.nbrGroupes['G']
        self.vNbEtPr.v[0] = self.classe.nbrGroupes['E']
        self.vNbActP.v[0] = self.classe.nbrGroupes['P']
#        print self.classe.effectifs
#        print self.classe.nbrGroupes
        
        self.cEffClas.mofifierValeursSsEvt()
        self.cNbERed.mofifierValeursSsEvt()
        self.cNbEtPr.mofifierValeursSsEvt()
        self.cNbActP.mofifierValeursSsEvt()
        
        self.AjouterGroupesVides()
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
            
        if self.CI.parent.classe.typeEnseignement == 'ET': # Rajouter la condition "Clermont" !!!
            
            self.panel_cible = Panel_Cible(self, self.CI)
            self.sizer.Add(self.panel_cible, (0,0), flag = wx.EXPAND)
            
            self.grid1 = wx.FlexGridSizer( 0, 2, 0, 0 )
            
            for i, ci in enumerate(constantes.CentresInterets[self.CI.parent.classe.typeEnseignement]):
                r = wx.CheckBox(self, 200+i, "")
                t = wx.StaticText(self, -1, "CI"+str(i+1)+" : "+ci)
                self.group_ctrls.append((r, t))
                self.grid1.Add( r, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
                self.grid1.Add( t, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5 )
            for radio, text in self.group_ctrls:
                self.Bind(wx.EVT_CHECKBOX, self.OnCheck, radio )
            self.sizer.Add(self.grid1, (0,1), flag = wx.EXPAND)
            self.sizer.Layout()
            
        else:
            
            self.grid1 = wx.FlexGridSizer( 0, 2, 0, 0 )
            
            for i, ci in enumerate(constantes.CentresInterets[self.CI.parent.classe.typeEnseignement]):
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
        
#    #############################################################################            
#    def EvtRadio(self, event):
#        print "EvtRadio CI"
#        radio_selected = eval(event.GetEventObject().GetLabel()[2:])
#        self.CI.SetNum(radio_selected-1)
#
#        self.Layout()
#        self.sendEvent()
#        
#    #############################################################################            
#    def EvtCheck(self, event):
#        print "EvtCheck CI",
#        check_selected = event.GetEventObject().GetId()-100
#        print check_selected 
#        self.CI.AddNum(check_selected)
#
#        self.Layout()
#        self.sendEvent()
#        
    #############################################################################            
    def OnCheck(self, event):
        print "OnCheck CI",
        button_selected = event.GetEventObject().GetId()-200
        print button_selected 
        
        if event.GetEventObject().IsChecked():
            self.CI.AddNum(button_selected)
        else:
            self.CI.DelNum(button_selected)
        
#        self.panel_cible.bouton[button_selected].SetState(event.GetEventObject().IsChecked())
        self.panel_cible.GererBoutons(True)
        
        self.Layout()
        self.sendEvent()
    
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        if self.CI.parent.classe.typeEnseignement == 'ET':
            self.panel_cible.GererBoutons(True)
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
        
        rayons = [90,90,60,40,20,30,60,40,20,30,60,40,20,30,0]
        angles = [-100,100,0,0,0,60,120,120,120,180,-120,-120,-120,-60,0]
        centre = [96, 88]
        
        rayons = {"F" : 60, 
                  "S" : 40, 
                  "C" : 20,
                  "_" : 90}
        angles = {"M" : 0,
                  "E" : 120,
                  "I" : -120,
                  "_" : -100}
        
#            dc = wx.ClientDC(self)
#            dc.DrawBitmap(images.Cible.GetBitmap(), 100, 100)
#            img = wx.StaticBitmap(self, -1, images.Cible.GetBitmap())
        for i, ci in enumerate(constantes.CentresInterets[self.CI.parent.classe.typeEnseignement]):
            mei, fsc = constantes.PositionCibleCIET[i].split("_")
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
        bmp = constantes.images.Cible.GetBitmap()
        self.SetSize((bmp.GetWidth(), bmp.GetHeight()))
        self.SetMinSize((bmp.GetWidth(), bmp.GetHeight()))
        
    ######################################################################################################
    def OnPaint(self, evt):
#        print "On paint"
        
        dc = wx.PaintDC(self)
#        gc = wx.GraphicsContext.Create(dc)
        dc.SetBackground(wx.Brush(self.backGround))
        dc.Clear()
        bmp = constantes.images.Cible.GetBitmap()
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
        color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND)
        dc.SetBackground(wx.Brush(self.backGround))
        dc.Clear()
        bmp = constantes.images.Cible.GetBitmap()
        dc.DrawBitmap(bmp, 0, 0)    
    
    
    #############################################################################            
    def OnButton(self, event):
        print "OnButton CI",
        button_selected = event.GetEventObject().GetId()-100
        print button_selected 
        
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
        if len(self.CI.numCI) == 0:
            l = range(16)
            
        elif len(self.CI.numCI) == 1:
            l = []
            for i,p in enumerate(constantes.PositionCibleCIET):
                p = p[:3].strip()
                c = self.CI.GetPosCible(0)[:3].strip()
#                print c
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
                    b.SetState(platebtn.PLATE_PRESSED)
                else:
                    b.SetState(platebtn.PLATE_NORMAL)
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
#        print "OnText", event.GetString()
        self.lien.path = event.GetString()
        self.MiseAJour()
        event.Skip()     
                            
    def OnLoseFocus(self, event):  
#        print "OnLooseFocus"
        self.lien.path = self.texte.GetValue()
        self.MiseAJour()
        event.Skip()   
                   
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.texte.SetValue(self.lien.path)
#        print "MiseAJour", self.lien.path
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
        
        classe = Classe(self.lien.parent.app)
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
        self.arbre = ArbreCompetences(self, self.competence.parent.classe.typeEnseignement)
        self.sizer.Add(self.arbre, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.Layout()

    ######################################################################################  
    def OnSize(self, event):
#        print self.GetClientSize()
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
#        print "MiseAJour"
        self.arbre.UnselectAll()
        for s in self.competence.competences:
            i = self.arbre.get_item_by_label(s, self.arbre.GetRootItem())
#            print i
            if i.IsOk():
#                print i
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
    def __init__(self, parent, savoirs):
        
        self.savoirs = savoirs

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
        self.arbre = ArbreSavoirs(self, self.savoirs)
        self.sizer.Add(self.arbre, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.Layout()
        
        
#    ######################################################################################  
#    def OnSize(self, event):
##        print self.GetClientSize()
#        self.win.SetMinSize(self.GetClientSize())
#        self.Layout()
#        event.Skip()

    ######################################################################################  
    def SetSavoirs(self): 
#        self.savoirs.savoirs = lst
#        print self.savoirs.savoirs
        self.savoirs.parent.VerrouillerClasse()
        self.sendEvent()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "MiseAJour"
        self.arbre.UnselectAll()
        for s in self.savoirs.savoirs:
            i = self.arbre.get_item_by_label(s, self.arbre.GetRootItem())
#            print i
            if i.IsOk():
#                print i
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
        titre = wx.StaticText(self, -1, u"Type :")
        cbType = wx.combo.BitmapComboBox(self, -1, u"Choisir un type de séance",
                             choices = [],
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
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
        self.cbInt = cb
        self.sizer.Add(bsizer, (1,0), (1,2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
#        self.sizer.Add(textctrl, (1,1), flag = wx.EXPAND)
        
        
        
        #
        # Durée de la séance
        #
        vcDuree = VariableCtrl(self, seance.duree, coef = 0.5, labelMPL = False, signeEgal = True, slider = False,
                               help = u"Durée de la séance en heures")
#        textctrl = wx.TextCtrl(self, -1, u"1")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
        self.vcDuree = vcDuree
        self.sizer.Add(vcDuree, (2,0), (1, 2))
        
        #
        # Effectif
        #
        titre = wx.StaticText(self, -1, u"Effectif :")
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
        
#        nombre = wx.StaticText(self, -1, u"")
#        self.nombre = nombre
        
        self.sizer.Add(titre, (3,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        self.sizer.Add(cbEff, (3,1), flag = wx.EXPAND)
#        self.sizer.Add(self.nombre, (3,2))
        
        #
        # Démarche
        #
        titre = wx.StaticText(self, -1, u"Démarche :")
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
#        self.sizer.Add(self.nombre, (4,2))
        
        #
        # Nombre de séances en parallèle
        #
        vcNombre = VariableCtrl(self, seance.nombre, labelMPL = False, signeEgal = True, slider = False, 
                                help = u"Nombre de groupes réalisant simultanément la même séance")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcNombre)
        self.vcNombre = vcNombre
        self.sizer.Add(vcNombre, (5,0), (1, 2))
        
        
        #
        # Systèmes
        #
        self.box = wx.StaticBox(self, -1, u"Systèmes ou matériels nécessaires", size = (200,200))
        self.box.SetMinSize((200,200))
        self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        self.systemeCtrl = []
        self.ConstruireListeSystemes()
        self.sizer.Add(self.bsizer, (0,4), (6, 1), flag = wx.EXPAND)
        
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
        self.sizer.Add(bsizer, (4,5), (2, 1), flag = wx.EXPAND)
        
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
        self.sizer.Add(dbsizer, (0,5), (4, 1), flag = wx.EXPAND)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        
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
                v = VariableCtrl(self, s, labelMPL = False, signeEgal = False, 
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
        self.Freeze()
#        print "MiseAJourListeSystemes", self.seance
        if self.seance.typeSeance in ["AP", "ED", "P"]:
            self.Freeze()
            for i, s in enumerate(self.seance.systemes):
                self.systemeCtrl[i].Renommer(s.n)
            self.bsizer.Layout()
            self.Layout()
            self.Thaw()

    ############################################################################            
    def GetDocument(self):
        return self.seance.GetDocument()
    
    #############################################################################            
    def EvtClick(self, event):
#        print "EvtClick"
#        print self.seance.description
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
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def EvtText(self, event):
#        print "EvtText", self.seance, event.GetId(), self.vcDuree.GetId()
        if event.GetId() == self.vcDuree.GetId():
            self.seance.SetDuree(event.GetVar().v[0])
        elif event.GetId() == self.vcNombre.GetId():
            self.seance.SetNombre(event.GetVar().v[0])
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def EvtComboBox(self, event):
#        print "EvtComboBox type"
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

        self.ConstruireListeSystemes()
#        self.AdapterAuxSystemes()
        self.Layout()
        
#        self.Fit()
        self.sendEvent()
       
        
        
    #############################################################################            
    def EvtComboBoxEff(self, event):
#        print "EvtComboBoxEff", self,
        self.seance.SetEffectif(event.GetString())  
#        print self.seance.effectif
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
#        print "EvtComboBoxDem", event.GetString()
         
        self.seance.SetDemarche(event.GetString())  
        
        self.sendEvent()
       
       
        
    #############################################################################            
    def OnClick(self, event):
        self.seance.AfficherLien(self.GetDocument().GetPath())
        
        
        
        
#    #############################################################################            
#    def AdapterAuxSystemes(self):
#        self.Freeze()
#        print "AdapterAuxSystemes", self.seance
#        if self.seance.typeSeance in ["AP", "ED", "P"]:
#            self.box.Show()
#            for i in range(self.seance.nSystemes):
#                s = self.seance.systemes[i]
#                self.systemeCtrl[i].Renommer(s.n)
##                self.systemeCtrl[i].mofifierValeursSsEvt()
#                self.systemeCtrl[i].Show()
#            for sc in self.systemeCtrl[self.seance.nSystemes:]:
#                sc.Hide()
#        else:
#            self.box.Hide()
#            for sc in self.systemeCtrl:
#                sc.Hide()
#        
#        self.bsizer.Layout()
#        self.Layout()
#        self.Fit()
#        self.Thaw()
    
      
    #############################################################################            
    def AdapterAuType(self):
        """ Adapte le panel au type de séance
        """
#        print "AdapterAuType"
        
        #
        # Type de parent
        #
        if self.seance.EstSousSeance():
            listType = constantes.listeTypeActivite
            if not self.seance.parent.EstSousSeance():
                listType = constantes.listeTypeActivite + ["S"]
        else:
            listType = constantes.listeTypeSeance
        
        listTypeS = []
        for t in listType:
            listTypeS.append((constantes.TypesSeance[t], constantes.imagesSeance[t].GetBitmap()))
        
        n = self.cbType.GetSelection()   
        self.cbType.Clear()
        for s in listTypeS:
            self.cbType.Append(s[0], s[1])
        self.cbType.SetSelection(n)
        
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
        elif self.seance.typeSeance in ["ED", "P"]:
            listEff = ["G", "D", "E", "P"]
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
#        print listEff
#        n = self.cbEff.GetSelection()   
        self.cbEff.Clear()
        for s in listEff:
            self.cbEff.Append(strEffectifComplet(self.seance.GetDocument().classe, s, -1))
        self.cbEff.SetSelection(0)
        
        
        # Démarche
        if self.seance.typeSeance in ["AP", "ED"]:
            listDem = ["I", "R"]
            self.cbDem.Show(True)
            self.titreDem.Show(True)
        elif self.seance.typeSeance == "P":
            listDem = ["I", "R", "P"]
            self.cbDem.Show(True)
            self.titreDem.Show(True)
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
        
#        self.AdapterAuxSystemes()
        
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
class PanelPropriete_Tache(PanelPropriete):
    def __init__(self, parent, tache):
        PanelPropriete.__init__(self, parent)
        self.tache = tache

        #
        # Phase
        #
        titre = wx.StaticText(self, -1, u"Phase :")
        cbPhas = wx.combo.BitmapComboBox(self, -1, u"Selectionner la phase",
                             choices = constantes.getLstPhase(),
                             style = wx.CB_DROPDOWN
                             | wx.TE_PROCESS_ENTER
                             | wx.CB_READONLY
                             #| wx.CB_SORT
                             )
        for i, k in enumerate(constantes.PHASE_TACHE):
            cbPhas.SetItemBitmap(i, constantes.imagesTaches[k].GetBitmap())
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbPhas)
        self.cbPhas = cbPhas
        self.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        self.sizer.Add(cbPhas, (0,1), flag = wx.EXPAND)
        
        #
        # Intitulé de la tache
        #
        box = wx.StaticBox(self, -1, u"Intitulé")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        bsizer.Add(textctrl, flag = wx.EXPAND)
        self.textctrl = textctrl
#        self.Bind(wx.EVT_TEXT, self.EvtTextIntitule, textctrl)
        self.textctrl.Bind(wx.EVT_KILL_FOCUS, self.EvtTextIntitule)
        
        cb = wx.CheckBox(self, -1, u"Montrer dans la zone de déroulement du projet")
        cb.SetValue(self.tache.intituleDansDeroul)
        bsizer.Add(cb, flag = wx.EXPAND)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
        self.cbInt = cb
        self.sizer.Add(bsizer, (1,0), (1,2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
#        self.sizer.Add(textctrl, (1,1), flag = wx.EXPAND)
        
        
        
        #
        # Durée de la tache
        #
        vcDuree = VariableCtrl(self, tache.duree, coef = 0.5, labelMPL = False, signeEgal = True, slider = False,
                               help = u"Durée de la tâche en heures")
#        textctrl = wx.TextCtrl(self, -1, u"1")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
        self.vcDuree = vcDuree
        self.sizer.Add(vcDuree, (2,0), (1, 2))
        
        
        #
        # Elèves impliqués
        #
        self.box = wx.StaticBox(self, -1, u"Elèves impliqués", size = (200,200))
        self.box.SetMinSize((150,200))
        self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        self.elevesCtrl = []
        self.ConstruireListeEleves()
        self.sizer.Add(self.bsizer, (0,2), (5, 1), flag = wx.EXPAND)
        
        
        #
        # Description de la tâche
        #
        dbox = wx.StaticBox(self, -1, u"Description")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
        bd = wx.Button(self, -1, u"Editer")
        tc = richtext.RichTextPanel(self, self.tache)
        tc.SetMaxSize((-1, 150))
        tc.SetMinSize((150, -1))
        dbsizer.Add(tc, 1, flag = wx.EXPAND)
        dbsizer.Add(bd, flag = wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        self.sizer.Add(dbsizer, (3,0), (1, 2), flag = wx.EXPAND)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        #
        # Compétences employées
        #
        cbox = wx.StaticBox(self, -1, u"Compétences employées")
        cbsizer = wx.StaticBoxSizer(cbox, wx.HORIZONTAL)
        self.arbre = ArbreCompetencesPrj(self, tache.parent.classe.typeEnseignement, cacheRacine = True)
        cbsizer.Add(self.arbre,1, flag = wx.EXPAND|wx.GROW)
        self.sizer.Add(cbsizer, (0,3), (4,1), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(3)
        self.sizer.AddGrowableRow(3)
        
        #
        # Mise en place
        #
        self.sizer.Layout()

        
    ######################################################################################  
    def AjouterCompetence(self, code):
        self.tache.competences.append(code)
        
    ######################################################################################  
    def EnleverCompetence(self, code):
        self.tache.competences.remove(code)
        
    ############################################################################            
    def SetCompetences(self):
        self.sendEvent()
        self.tache.parent.VerrouillerClasse()
        
#        self.tache.SetCompetences()
        
    ############################################################################            
    def ConstruireListeEleves(self):
        
#        print "ConstruireListeEleves"
        self.Freeze()
        
        for ss in self.elevesCtrl:
            self.bsizer.Detach(ss)
            ss.Destroy()
            
        self.elevesCtrl = []
        for i, e in enumerate(self.GetDocument().eleves):
            v = wx.CheckBox(self, 100+i, e.GetNomPrenom())
            v.SetMinSize((200,-1))
            v.SetValue(i in self.tache.eleves)
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckEleve, v)
            self.bsizer.Add(v, flag = wx.ALIGN_LEFT|wx.ALL, border = 3)#|wx.EXPAND) 
            self.elevesCtrl.append(v)
        self.bsizer.Layout()
        
        if len(self.GetDocument().eleves) > 0:
            self.box.Show(True)
        else:
            self.box.Hide()

        self.box.SetMinSize((200,200))
        self.Layout()
        self.Thaw()
        
        
    #############################################################################            
    def MiseAJourListeEleves(self):
        """ Met à jour la liste des élèves
        """
        self.Freeze()
        for i, e in enumerate(self.GetDocument().eleves):
            self.elevesCtrl[i].SetLabel(e.GetNomPrenom())
        self.bsizer.Layout()
        self.Layout()
        self.Thaw()

    ############################################################################            
    def GetDocument(self):
        return self.tache.GetDocument()
    
    #############################################################################            
    def EvtClick(self, event):
#        print "EvtClick"
#        print self.seance.description
        if not self.edition:
            self.win = richtext.RichTextFrame(u"Description de la tâche "+ self.tache.code, self.tache)
            self.edition = True
            self.win.Show(True)
        else:
            self.win.SetFocus()
        
        
    #############################################################################            
    def EvtVarSysteme(self, event):
        self.sendEvent()
        
    #############################################################################            
    def EvtCheckBox(self, event):
        self.tache.intituleDansDeroul = event.IsChecked()
        self.sendEvent()
        
        
    #############################################################################            
    def EvtCheckEleve(self, event):
        lst = []
        for i,s in enumerate(self.GetDocument().eleves):
            if self.elevesCtrl[i].IsChecked():
                lst.append(i)
        self.tache.eleves = lst
        self.sendEvent()    
    
    #############################################################################            
    def EvtTextIntitule(self, event):
        self.tache.SetIntitule(self.textctrl.GetValue())
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def EvtText(self, event):
#        print "EvtText", self.seance, event.GetId(), self.vcDuree.GetId()
        if event.GetId() == self.vcDuree.GetId():
            self.tache.SetDuree(event.GetVar().v[0])
        elif event.GetId() == self.vcNombre.GetId():
            self.tache.SetNombre(event.GetVar().v[0])
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def EvtComboBox(self, event):

        self.tache.SetPhase(get_key(constantes.NOM_PHASE_TACHE, self.cbPhas.GetStringSelection()))
        self.Layout()
        self.sendEvent()
        
    
    #############################################################################            
    def MiseAJourDuree(self):
        print "MiseAJourDuree"
        self.vcDuree.mofifierValeursSsEvt()
        
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        print "MiseAJour PanelPropriete_Tache"
        self.arbre.UnselectAll()
        root = self.arbre.GetRootItem()
        for s in self.tache.competences:
            i = self.arbre.FindItem(root, s)
#            print s, i
            if i.IsOk():
#                print i
                self.arbre.CheckItem2(i)
        
        self.textctrl.SetValue(self.tache.intitule)
        
        if self.tache.phase != '':
            self.cbPhas.SetStringSelection(constantes.NOM_PHASE_TACHE[self.tache.phase])
        
        if sendEvt:
            self.sendEvent()
        
        
        
        
        
        
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
        vcNombre = VariableCtrl(self, systeme.nbrDispo, labelMPL = False, signeEgal = True, slider = False, 
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
    #        print event.GetId()
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
#        print "EvtVar"
#        if event.GetId() == self.vcNombre:
        self.systeme.SetNombre()
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.textctrl.ChangeValue(self.systeme.nom)
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
        self.sizer.Add(bsizer, (0,3), (3,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.LEFT, border = 3)#wx.ALIGN_CENTER_VERTICAL |
        
        self.sizer.AddGrowableRow(2)
        
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
    def MiseAJour(self, sendEvt = False):
        self.textctrln.ChangeValue(self.personne.nom)
        self.textctrlp.ChangeValue(self.personne.prenom)
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
    #        print event.GetId()
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
        self.support.SetNom(event.GetString())
#        self.support.parent.MiseAJourNomsSystemes()
        if not self.eventAttente:
            wx.CallLater(DELAY, self.sendEvent)
            self.eventAttente = True
        
    #############################################################################            
    def EvtClick(self, event):
#        print "EvtClick"
#        print self.seance.description
        if not self.edition:
            self.win = richtext.RichTextFrame(u"Description du support "+ self.support.nom, self.support)
            self.edition = True
            self.win.Show(True)
        else:
            self.win.SetFocus()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        print "MiseAJour support", self.support.nom
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
                 agwStyle = CT.TR_HAS_BUTTONS|CT.TR_HAS_VARIABLE_ROW_HEIGHT | CT.TR_HIDE_ROOT,
                 ):

        CT.CustomTreeCtrl.__init__(self, parent, -1, pos, size, style, agwStyle)

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
        
    ####################################################################################
    def OnSelChanged(self, event):
#        print "OnSelChanged"
        self.item = event.GetItem()
        data = self.GetItemPyData(self.item)
        if data == None:
            panelPropriete = self.panelVide
        else:
            panelPropriete = data.panelPropriete
        self.panelProp.AfficherPanel(panelPropriete)
#        wx.CallAfter(panelPropriete.Refresh)
        event.Skip()
        
    ####################################################################################
    def OnBeginDrag(self, event):
#        print "OnBeginDrag", 
        self.itemDrag = event.GetItem()
#        print self.itemDrag
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
#        print keycode
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
#        print "OnRightDown"
#        pt = event.GetPosition()
#        item, flags = self.HitTest(pt)
        item = event.GetItem()
#        print dir(item)

        self.sequence.AfficherMenuContextuel(item)

    
    ####################################################################################
    def OnLeftDClick(self, event):
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
#        print item
        if item:
#            print "DClick (arbre)"
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
                        self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
                    else:
                        if dataTarget != dataSource:# and dataTarget.parent == dataSource.parent:
                            self.SetCursor(self.CurseurInsert)
                        else:
                            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
                        
        event.Skip()
        
        
    ####################################################################################
    def OnEndDrag(self, event):
#        print "OnEndDrag",
        self.item = event.GetItem()
#        print self.itemDrag, self.item 
        dataTarget = self.GetItemPyData(self.item)
        dataSource = self.GetItemPyData(self.itemDrag)
        if not isinstance(dataSource, Seance):
            pass
        else:
            if not isinstance(dataTarget, Seance):
                pass
            else:
                if dataTarget != dataSource and dataTarget.parent == dataSource.parent:
                    if isinstance(dataTarget.parent, Sequence):
                        lst = dataTarget.parent.seance
                    else:
                        lst = dataTarget.parent.sousSeances
                    s = lst.index(dataSource)
                    t = lst.index(dataTarget)
                    
                    if t > s:
                        lst.insert(t, lst.pop(s))
                    else:
                        lst.insert(t+1, lst.pop(s))
                    dataTarget.parent.OrdonnerSeances()
                    self.SortChildren(self.GetItemParent(self.item))
                    self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
                
                elif dataTarget != dataSource and dataTarget.parent != dataSource.parent:
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
                    t = lstT.index(dataTarget)
                    lstT[t+1:t+1] = [dataSource]
                    del lstS[s]
                    p = dataSource.parent
                    dataSource.parent = dataTarget.parent
#                    dataTarget.parent = p
                    p.OrdonnerSeances()
                    dataTarget.parent.OrdonnerSeances()
                    
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
#        print keycode
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
#        print item
        if item:
#            print "DClick (arbre)"
            self.projet.AfficherLien(item)
        event.Skip()                
        

    ####################################################################################
    def OnCompareItems(self, item1, item2):
        i1 = self.GetItemPyData(item1)
        i2 = self.GetItemPyData(item2)
        if i1.phase == i2.phase:
            return i1.ordre - i2.ordre
        else:
            if i1.phase == "":
                return -1
            elif i2.phase == "":
                return 1
            else:
                if i1.phase[0] > i2.phase[0]:
                    return 1
                else:
                    return -1
        

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
                        self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
                    else:
                        if dataTarget != dataSource:# and dataTarget.parent == dataSource.parent:
                            self.SetCursor(self.CurseurInsert)
                        else:
                            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
                        
        event.Skip()
        
        
    ####################################################################################
    def OnEndDrag(self, event):
#        print "OnEndDrag",
        self.item = event.GetItem()
#        print self.itemDrag, self.item 
        dataTarget = self.GetItemPyData(self.item)
        dataSource = self.GetItemPyData(self.itemDrag)
        if not isinstance(dataSource, Seance):
            pass
        else:
            if not isinstance(dataTarget, Seance):
                pass
            else:
                if dataTarget != dataSource and dataTarget.parent == dataSource.parent:
                    if isinstance(dataTarget.parent, Sequence):
                        lst = dataTarget.parent.seance
                    else:
                        lst = dataTarget.parent.sousSeances
                    s = lst.index(dataSource)
                    t = lst.index(dataTarget)
                    
                    if t > s:
                        lst.insert(t, lst.pop(s))
                    else:
                        lst.insert(t+1, lst.pop(s))
                    dataTarget.parent.OrdonnerSeances()
                    self.SortChildren(self.GetItemParent(self.item))
                    self.panelVide.sendEvent(self.sequence) # Solution pour déclencher un "redessiner"
                
                elif dataTarget != dataSource and dataTarget.parent != dataSource.parent:
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
                    t = lstT.index(dataTarget)
                    lstT[t+1:t+1] = [dataSource]
                    del lstS[s]
                    p = dataSource.parent
                    dataSource.parent = dataTarget.parent
#                    dataTarget.parent = p
                    p.OrdonnerSeances()
                    dataTarget.parent.OrdonnerSeances()
                    
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






            



class ArbreSavoirs(CT.CustomTreeCtrl):
    def __init__(self, parent, savoirs):

        CT.CustomTreeCtrl.__init__(self, parent, -1, style = wx.TR_DEFAULT_STYLE|wx.TR_MULTIPLE|wx.TR_HIDE_ROOT)
        
        self.parent = parent
        self.savoirs = savoirs
        
        self.root = self.AddRoot(u"Savoirs")
        self.Construire(self.root, constantes.dicSavoirs[savoirs.parent.classe.typeEnseignement])
        
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
        il = wx.ImageList(20, 20)
#        for k, i in dicimages.items():
#            self.images[k] = il.Add(i.GetBitmap())
        self.AssignImageList(il)
        
        
        #
        # Gestion des évenements
        #
#        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnItemCheck)
        
    def Construire(self, branche, dic):
#        print "Construire", dic
        clefs = dic.keys()
        clefs.sort()
        for k in clefs:
            b = self.AppendItem(branche, k+" "+dic[k][0], ct_type=1)
            if type(dic[k][1]) == dict:
                self.Construire(b, dic[k][1])

        
    def OnItemCheck(self, event):
        item = event.GetItem()
        code = self.GetItemText(item).split()[0]
        if item.GetValue():
            self.parent.savoirs.savoirs.append(code)
        else:
            self.parent.savoirs.savoirs.remove(code)
        self.parent.SetSavoirs()
        event.Skip()
        
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
#        print "get_item_by_label", search_text, root_item
        item, cookie = self.GetFirstChild(root_item)
    
        while item != None and item.IsOk():
            text = self.GetItemText(item)
#            print "   ", text
            if text.split()[0] == search_text:
                return item
            if self.ItemHasChildren(item):
                match = self.get_item_by_label(search_text, item)
                if match.IsOk():
                    return match
            item, cookie = self.GetNextChild(root_item, cookie)
    
        return wx.TreeItemId()


class ArbreCompetences(CT.CustomTreeCtrl):
    def __init__(self, parent, type_ens, cacheRacine = False):

        
        if cacheRacine :
            agwStyle = CT.TR_MULTIPLE|CT.TR_HIDE_ROOT
        else:
            agwStyle = CT.TR_MULTIPLE
        CT.CustomTreeCtrl.__init__(self, parent, -1, agwStyle = agwStyle)#wx.TR_DEFAULT_STYLE|
        
        self.parent = parent
        
        self.root = self.AddRoot(u"Compétences")
        self.Construire(self.root, type_ens = type_ens)
        
        self.ExpandAll()
        
#        il = wx.ImageList(20, 20)
#        self.AssignImageList(il)
        
        #
        # Gestion des évenements
        #
#        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnItemCheck)
        
    ####################################################################################
    def Construire(self, branche, dic = None, type_ens = None, ct_type = 0):
#        print "Construire", dic
        if dic == None:
            dic = constantes.dicCompetences[type_ens]
        clefs = dic.keys()
        clefs.sort()
        for k in clefs:
            b = self.AppendItem(branche, k+" "+dic[k][0], ct_type=ct_type)
            if len(dic[k])>1 and type(dic[k][1]) == dict:
                self.Construire(b, dic[k][1], ct_type=1)
        
    ####################################################################################
    def OnItemCheck(self, event):
        item = event.GetItem()
        code = self.GetItemText(item).split()[0]
        if item.GetValue():
            self.parent.AjouterCompetence(code)
        else:
            self.parent.EnleverCompetence(code)
        self.parent.SetCompetences()
        event.Skip()

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
#        print "get_item_by_label", search_text, root_item
        item, cookie = self.GetFirstChild(root_item)
    
        while item != None and item.IsOk():
            text = self.GetItemText(item)
#            print "   ", text
            if text.split()[0] == search_text:
                return item
            if self.ItemHasChildren(item):
                match = self.get_item_by_label(search_text, item)
                if match.IsOk():
                    return match
            item, cookie = self.GetNextChild(root_item, cookie)
    
        return wx.TreeItemId()



class ArbreCompetencesPrj(ArbreCompetences):
    def __init__(self, parent, type_ens, cacheRacine = False):
        ArbreCompetences.__init__(self, parent, type_ens, cacheRacine)
        

    ####################################################################################
    def Construire(self, branche, dic = None, type_ens = None, ct_type = 0):
#        print "Construire", dic
        if dic == None:
            dic = constantes.dicCompetences_prj[type_ens]
        clefs = dic.keys()
        clefs.sort()
        for k in clefs:
            b = self.AppendItem(branche, k+" "+dic[k][0], ct_type=ct_type)
            if len(dic[k])>1 and type(dic[k][1]) == dict:
                self.Construire(b, dic[k][1], ct_type=1)



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

def listesEgales(l1, l2):
    if len(l1) != len(l2):
        return False
    else:
        
        for e1, e2 in zip(l1,l2):
            if e1 != e2:
                return False
    return True

def dansRectangle(x, y, rect):
    for r in rect:
        if x > r[0] and y > r[1] and x < r[0] + r[2] and y < r[1] + r[3]:
            return True
    return False

#def dansRectangles(x, y, rect):
#    for r in rect:
#        print r
#        if dansRectangle(x, y, r):
#            return True
#    return False

def get_key(dict, value):
    i = 0
    continuer = True
    while continuer:
        if i > len(dict.keys()):
            continuer = False
        else:
            if dict.values()[i] == value:
                continuer = False
                key = dict.keys()[i]
            i += 1
    return key


#def permut(liste):
#    l = []
#    for a in liste[1:]:
#        l.append(a)
#    l.append(liste[0])
#    return l
#    
#    
#def getHoraireTxt(v): 
#    h, m = divmod(v*60, 60)
#    h = str(int(h))
#    if m == 0:
#        m = ""
#    else:
#        m = str(int(m))
#    return h+"h"+m


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
        if len(sys.argv)>1: #un paramétre a été passé
            parametre = sys.argv[1]
#            for param in sys.argv:
#                parametre = param.upper()
#                # on verifie que le fichier passé en paramétre existe
            if os.path.isfile(parametre):
                fichier = unicode(parametre, FILE_ENCODING)
        
#        self.serveur = Server(fichier)
#        loop()
#        self.a = threading.Thread(None, loop)
#        self.a.start()

        
        frame = FenetrePrincipale(None, fichier)
        frame.Show()
        
        server.app = frame
        
        self.SetTopWindow(frame)
        return True

#    def OnExit(self):
#        self.a.stop()
        
#    def OuvrirSequence(self, nomFichier):
#        print "ordre ouverture", nomFichier
#        self.frame.ouvrir(nomFichier)
#        
#def lanceServeur(fichier):
#    serveur = Server(fichier)
#    loop()
#    return serveur



#class lanceServeur(threading.Thread):
#    def __init__(self, fichier = ''):
#        threading.Thread.__init__(self)
#        self.fichier = fichier
#        self.Terminated = False
#    
#    def run(self):
#        i = 0
#        while not self.Terminated:
#            print self.nom, i
#            i += 1
#            time.sleep(2.0)
#        print "le thread "+self.nom +" s'est termine proprement"
#    def stop(self):
#        self.Terminated = True    
        
        
        
#class Server( dispatcher ):
#    def __init__(self, nomfichier):
#        dispatcher.__init__(self)
#        self.create_socket( socket.AF_INET, socket.SOCK_STREAM )
#        self.buffer = ""
#        self.fichier = nomfichier
#        try:
#            self.bind( ( '', 50000 ) )
#        except:
#            self.connect(( '', 50000 ))
#            self.send(nomfichier)
#            sys.exit()
#        self.listen(1)
#    
#    def handle_write(self):
#        sent = self.send(self.buffer)
#        self.buffer = self.buffer[sent:]
#
#    def writable(self):
#        return (len(self.buffer) > 0)
#
#    def handle_read(self):
#        s = self.recv(len(self.buffer))
#        print "Recv", s
#        
#    def handle_close(self):
#        print 'close'
#        self.close()
#        
#    def handle_accept(self):
#        return True

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
class PopupInfo(wx.PopupWindow):
    def __init__(self, parent, titre = ""):
        wx.PopupWindow.__init__(self, parent, wx.BORDER_SIMPLE)
        self.parent = parent
        self.sizer = wx.GridBagSizer()
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
        

class PopupInfoSysteme(PopupInfo):
    def __init__(self, parent, titre):
        PopupInfo.__init__(self, parent, titre)
        
        
        self.code = wx.StaticText(self, -1, "")
        self.sizer.Add(self.code, (1,0), flag = wx.ALL, border = 5)
#        
        
        self.message = wx.StaticText(self, -1, "")
        self.sizer.Add(self.message, (2,0), flag = wx.ALL, border = 5)
        
        
        self.titreLien = wx.StaticText(self, -1, "")
        self.ctrlLien = wx.BitmapButton(self, -1, wx.NullBitmap)
        self.ctrlLien.Show(False)
        self.typeLien = ""
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.ctrlLien)
        sizerLien = wx.BoxSizer(wx.HORIZONTAL)
        sizerLien.Add(self.titreLien, flag = wx.ALIGN_CENTER_VERTICAL)
        sizerLien.Add(self.ctrlLien)
        self.sizer.Add(sizerLien, (3,0), flag = wx.ALL, border = 5)
        

        self.image = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.image.Show(False)
        self.sizer.Add(self.image, (4,0), flag = wx.ALL, border = 5)
       
    
    
    ##########################################################################################
    def SetCode(self, message):
        if message == "":
            self.code.Show(False)
        else:
            self.code.SetLabel(message)
            self.code.Show(True)
        self.Layout()
        self.Fit()
        
    ##########################################################################################
    def SetMessage(self, message):
        if message == "":
            self.message.Show(False)
        else:
            self.message.SetLabel(message)
            self.message.Show(True)
        self.Layout()
        self.Fit()
        
    ##########################################################################################
    def SetLien(self, lien):
        self.lien = lien
        if lien.type == "":
            self.ctrlLien.Show(False)
            self.titreLien.Show(False)
            self.ctrlLien.SetToolTipString(toDefautEncoding(self.lien.path))
        else:
            self.ctrlLien.SetToolTipString(toDefautEncoding(self.lien.path))
            if lien.type == "f":
                self.titreLien.SetLabel(u"Fichier :")
                self.ctrlLien.SetBitmapLabel(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE))
                self.ctrlLien.Show(True)
            elif lien.type == 'd':
                self.titreLien.SetLabel(u"Dossier :")
                self.ctrlLien.SetBitmapLabel(wx.ArtProvider_GetBitmap(wx.ART_FOLDER))
                self.ctrlLien.Show(True)
            elif lien.type == 'u':
                self.titreLien.SetLabel(u"Lien web :")
                self.ctrlLien.SetBitmapLabel(constantes.images.Icone_web.GetBitmap())
                self.ctrlLien.Show(True)
            elif lien.type == 's':
                self.titreLien.SetLabel(u"Fichier séquence :")
                self.ctrlLien.SetBitmapLabel(constantes.images.Icone_sequence.GetBitmap())
                self.ctrlLien.Show(True)

        self.Layout()
        self.Fit()
        
    ##########################################################################################
    def SetImage(self, image):
        if image == None:
            self.image.Show(False)
        else:
            self.image.SetBitmap(image)
            self.image.Show(True)
        self.Layout()
        self.Fit()
        
    ##########################################################################################
    def OnClick(self, evt):
        self.lien.Afficher(self.parent.sequence.GetPath(), self.parent.parent)
        


#############################################################################################################
#
# Le tip d'information pour les descriptions de séance
# 
#############################################################################################################
import cStringIO
import wx.richtext as rt

class PopupInfoSeance(PopupInfoSysteme):
    def __init__(self, parent, titre, objet):
        PopupInfoSysteme.__init__(self, parent, titre)
        self.objet = objet
        self.titreDescr = wx.StaticText(self, -1, u"Description :")
        self.rtp = richtext.RichTextPanel(self, objet, size = (300, 200))
        self.sizer.Add(self.titreDescr, (5,0), flag = wx.ALL, border = 5)
        self.sizer.Add(self.rtp, (6,0), flag = wx.ALL|wx.EXPAND, border = 5)
        self.SetDescription()
        
    def SetDescription(self):
#        print "SetDescription TIP", self.objet.description != None
        self.rtp.Show(self.objet.description != None)
        self.titreDescr.Show(self.objet.description != None)
        self.rtp.Ouvrir()
        self.Layout()
        self.Fit()


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
        self.Bind(wx.EVT_BUTTON, self.OnSeq, button)
        sizer.Add(button,0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        button = wx.Button(self, -1, u"Nouveau Projet")
        button.SetToolTipString(u"Créer un nouveau projet")
        self.Bind(wx.EVT_BUTTON, self.OnPrj, button)
        sizer.Add(button,0,  wx.ALIGN_CENTRE|wx.ALL, 5)
    
        self.SetSizer(sizer)
        sizer.Fit(self)
        
        self.SetReturnCode(0)
        

    def OnSeq(self, event):
        print "seq"
        self.SetReturnCode(1)
        self.EndModal(1)

    def OnPrj(self, event):
        print "prj"
        self.SetReturnCode(2)
        self.EndModal(2)




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
        titre = wx.StaticText(self, -1, __appname__)
        titre.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, False))
        titre.SetForegroundColour(wx.NamedColour("BROWN"))
        sizer.Add(titre, border = 10)
        sizer.Add(wx.StaticText(self, -1, "Version : "+__version__), 
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
            lictext = u"Le fichier de licence (gpl.txt) est introuvable !\n" \
                      u"Veuillez réinstaller pySequence !"
            dlg = wx.MessageDialog(self, lictext,
                               'Licence introuvable',
                               wx.OK | wx.ICON_ERROR
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            
            
        wx.TextCtrl(licence, -1, lictext, size = (400, -1), 
                    style = wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_NONE )
        

        
        # Description
        #-------------
        descrip = wx.Panel(nb, -1)
        wx.TextCtrl(descrip, -1, wordwrap(u"pySequence est un logiciel d'aide à l'élaboration de séquences pédagogiques,\n"
                                          u"sous forme de fiches exportables au format PDF.\n"
                                          u"Il est élaboré en relation avec le programme et le document d'accompagnement\n"
                                          u"des enseignements technologiques transversaux de la filière STI2D.",
                                            500, wx.ClientDC(self)),
                        size = (400, -1),
                        style = wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_NONE) 
        
        nb.AddPage(descrip, u"Description")
        nb.AddPage(auteurs, u"Auteurs")
        nb.AddPage(licence, u"Licence")
        
        sizer.Add(hl.HyperLinkCtrl(self, wx.ID_ANY, u"Informations et téléchargement : http://code.google.com/p/pysequence/",
                                   URL="http://code.google.com/p/pysequence/"),  
                  flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
        sizer.Add(nb)
        
        self.SetSizerAndFit(sizer)



        
import socket

if __name__ == '__main__':

    HOST, PORT = socket.gethostname(), 61955

    server = None
    try:
        if len(sys.argv) > 1:
            arg = sys.argv[1]
        else:
            arg = ''
        serveur.client(HOST, PORT, arg)
        sys.exit()
    except socket.error:
        server = serveur.start_server(HOST, PORT)
        app = SeqApp(False)
        app.MainLoop()
    
    
