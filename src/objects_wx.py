#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                objects_wx                               ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2011-2016 Cédrick FAURY - Jean-Claude FRICOU
##
## pySéquence : aide à la construction
## de Séquences et Progressions pédagogiques
## et à la validation de Projets

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
module objects_wx
*****************

Les principaux éléments du GUI de **pySéquence**.


"""


SSCALE = 1.0

####################################################################################
#
#   Imports minimum et SplashScreen
#
####################################################################################
# Outils système
import os, sys
import urllib.request
import util_path
import logiciels
import shutil
import uuid # Pour autosave

# print(sys.version_info)

# à décommenter pour forcer l'utilisation de wxpython 2.8 (ubuntu 14)
# if sys.platform != "win32":
#     import wxversion
#    wxversion.select('2.8')

import wx

try:
    import  wx.gizmos as adv
except:
    pass

try:
    import wx.adv as adv     # à partir de wx 4
except:
    pass
   
from wx.lib.expando import ExpandoTextCtrl

import wx.lib.wxpTag

from wx.lib.ClickableHtmlWindow import PyClickableHtmlWindow


import version

# Module de gestion des dossiers, de l'installation et de l'enregistrement
from util_path import toFileEncoding, toSystemEncoding, FILE_ENCODING, SYSTEM_ENCODING, \
                      nomCourt

import richtext

import time

# Chargement des images
import images


#####################################################################################
#   Tout ce qui concerne le GUI
#####################################################################################
     
# Arbre
# try:
#     from agw import customtreectrl as CT
# except ImportError: # if it's not there locally, try the wxPython lib.
import wx.lib.agw.customtreectrl as CT

import wx.lib.agw.ultimatelistctrl as ULC

import wx.lib.agw.hypertreelist as HTL
    
# Gestionnaire de "pane"
import wx.aui as aui
#import wx.lib.agw.aui as aui # ça marche pas !

from wx.lib.wordwrap import wordwrap

import wx.lib.agw.hyperlink as hl # à partir de wx 4
    
import  wx.lib.scrolledpanel as scrolled
try: # gros basard pour py3
    import wx.combo as combo
    combo_adv = combo
except:
    import wx.adv as combo_adv
    combo = wx
    
import wx.lib.platebtn as platebtn
import wx.lib.colourdb
import wx.lib.colourselect as  csel
import wx.lib.agw.foldpanelbar as fpb

# import wx.lib.mixins.listctrl as listmix


# Pour les descriptions

import orthographe
import wx.stc  as  stc
import wx.richtext as rt

from drag_file import *

import lien
import grilles

########################################################################
try:
    from agw import genericmessagedialog as GMD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.genericmessagedialog as GMD


# Les constantes partagées
from constantes import calculerEffectifs, \
                        getElementFiltre, \
                        CHAR_POINT, COUL_PARTIE, getCoulPartie, COUL_ABS, \
                        TOUTES_REVUES_EVAL, TOUTES_REVUES_EVAL_SOUT, TOUTES_REVUES_SOUT, TOUTES_REVUES, \
                        _S, _Rev, _R1, _R2, _R3, DUREE_AUTOSAVE, \
                        COUL_OK, COUL_NON, COUL_BOF, COUL_BIEN, \
                        toList, COUL_COMPETENCES, WMIN_PROP, HMIN_PROP, \
                        WMIN_STRUC, HMIN_STRUC, LOGICIELS, \
                        IMG_SIZE_TB, IMG_SIZE_TREE, evaluer#, bmp
import constantes
constantes.charger_templates()
constantes.charger_icones()


import couleur

from xml.dom.minidom import parse, parseString

# Graphiques vectoriels

import wx.lib.wxcairo
import cairo
# import cairocffi as cairo

import draw_cairo2 as draw_cairo
import draw_cairo_seq2 as draw_cairo_seq
import draw_cairo_prj2 as draw_cairo_prj
import draw_cairo_prg2 as draw_cairo_prg

# Widgets partagés
# des widgets wx évolués "faits maison"
# import widgets
from widgets import Variable, VariableCtrl, EVT_VAR_CTRL, VAR_ENTIER_POS, \
                    messageErreur, getNomFichier, pourCent2, RangeSlider, \
                    isstring, EditableListCtrl, Grammaire, getAncreFenetre, \
                    et2ou, FullScreenWin, safeParse, dansRectangle, \
                    TextCtrl_Help, CloseFenHelp, DelayedResult, \
                    messageInfo, messageWarning, rognerImage, enregistrer_root, \
                    tronquerDC, EllipticStaticText, scaleImage, scaleIcone, \
                    DisplayChoice, MyEditableListBox, intersection, locale2def, locale2EN
                    #, chronometrer


# Pour enregistrer en xml
import xml.etree.ElementTree as ET

import Options

import textwrap

if sys.platform == "win32" :
    # Pour l'enregistement dans la base de donnée Windows
    import register
    

import genpdf

from rapport import FrameRapport, RapportRTF

from math import sin, cos, pi

from Referentiel import REFERENTIELS, ARBRE_REF, ACTIVITES
import Referentiel


import io
import  wx.html as  html
# import wx.html2 as webview

try: 
    from BeautifulSoup import BeautifulSoup, NavigableString
except ImportError:
    from bs4 import BeautifulSoup, NavigableString
    
import copy
import webbrowser

import threading 

# from pysequence import *
# import pysequence   # déplacé à la fin

from dpi_aware import *
from file2bmp import *

# Pour débugger
DEBUG = version.DEBUG




####################################################################################
#
#   Classe permettant de gérer les anciennes versions des documents lors de l'ouverture
#
####################################################################################

class OldVersion(Exception):
    pass


####################################################################################
#
#   Classe permettant de gérer les écarts de version de référentiel
#
####################################################################################

class DiffReferentiel(Exception):
    pass


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
        self.modif = ""
        self.draw = True
        self.verif = False
        
    ######################################################################################  
    def SetDocument(self, doc):
        self.doc = doc
        
    ######################################################################################  
    def GetDocument(self):
        return self.doc
    
    ######################################################################################  
    def SetModif(self, modif):
        self.modif = modif
        
    ######################################################################################  
    def GetModif(self):
        return self.modif
    
    ######################################################################################  
    def SetDraw(self, draw):
        self.draw = draw
        
    ######################################################################################  
    def SetVerif(self, verif):
        self.verif = verif
        
    ######################################################################################  
    def GetDraw(self):
        return self.draw

    ######################################################################################  
    def GetVerif(self):
        return self.verif

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
    
    
# def Get():
#     return
####################################################################################
#
#   Quelques flags
#
####################################################################################
ALIGN_RIGHT = wx.ALIGN_RIGHT
ALL = wx.ALL
ALIGN_LEFT = wx.ALIGN_LEFT
BOTTOM = wx.BOTTOM
TOP = wx.TOP
LEFT = wx.LEFT
ICON_INFORMATION = wx.ICON_INFORMATION
ICON_WARNING = wx.ICON_WARNING
CANCEL = wx.CANCEL


####################################################################################
#
#   Quelques polices de caractères
#
####################################################################################
def getFont_9S():
    return wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline = True)

def getFont_9():
    return wx.Font(9, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL)



####################################################################################
#
#   Quelques icones "wx"
#
####################################################################################
def getIconeFileSave(size = (20,20)):
    return scaleImage(images.Icone_save.GetBitmap())
#     return wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, size)

def getIconePaste(size = (20,20)):
    return scaleImage(images.Icone_paste.GetBitmap())
#     return wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, size)

def getIconeCopy(size = (20,20)):
    return scaleImage(images.Icone_copy.GetBitmap())
#     return wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, size)

def getIconeUndo(size = (20,20)):
    return scaleImage(images.Icone_undo.GetBitmap())
#     return wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, size)

def getIconeRedo(size = (20,20)):
    return scaleImage(images.Icone_redo.GetBitmap())
#     return wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, size)


#     return wx.Bitmap(wx.lib.wxcairo.BitmapFromImageSurface(imagesurface))


def getDisplaysPosSize():
    """ Renvoie la position et la taille des écrans : x, y, w, h
    """
    displays = (wx.Display(i) for i in range(wx.Display.GetCount()))
    sizes = [display.ClientArea for display in displays]
    return sizes



def getDisplaysPPI():
    """ Renvoie la résolution des écrans : ppi
    """
    displays = (wx.Display(i) for i in range(wx.Display.GetCount()))
    ppi = [display.GetPPI() for display in displays]
    return ppi
    
def getDisplayPPI(win):
    display = wx.Display.GetFromWindow(win)
    return wx.Display(display).GetPPI()


####################################################################################
#
#   Classes pour gérer les boutons de la Toolbar principale
#
####################################################################################
class BoutonToolBar():
    def __init__(self, label, image, shortHelp = "", longHelp = ""):
        self.label = label
        self.image = image
        self.shortHelp = shortHelp
        self.longHelp = longHelp
#        self.fonction = fonction

####################################################################################
#
#   Classes définissant la fenétre principale de l'application
#
####################################################################################
class FenetrePrincipale(aui.AuiMDIParentFrame):
    def __init__(self, parent, fichier, options = []):
        global DEBUG
        aui.AuiMDIParentFrame.__init__(self, parent, -1, 
                                       version.GetAppnameVersion(), 
                                       style=wx.DEFAULT_FRAME_STYLE)
        
        
        DEBUG = DEBUG or "d" in options
        
        
#         print "SSCALE", SSCALE
        self.Freeze()
        wx.lib.colourdb.updateColourDB()


        # Timer pour autosave
        self.timerAutosave = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timerAutosave)
        
        
        
        
#         self.Bind(wx.EVT_UPDATE_UI, self.onDisplayChanged)
        
        #
        # le fichier de configuration de la fiche
        #
#        self.nomFichierConfig = os.path.join(APP_DATA_PATH,"configFiche.cfg")
#        # on essaye de l'ouvrir
#        try:
#            draw_cairo_seq.ouvrirConfigFiche(self.nomFichierConfig)
#        except:
#            print "Erreur à l'ouverture de configFiche.cfg" 


        #############################################################################################
        # Création du menu
        #############################################################################################
        self.CreateMenuBar()
        
        
        #############################################################################################
        # Instanciation et chargement des options
        #############################################################################################
        options = Options.Options()
        if options.fichierExiste():
#            options.ouvrir(DEFAUT_ENCODING)
            options.ouvrir(SYSTEM_ENCODING)
#             try :
#                 options.ouvrir(SYSTEM_ENCODING)
#             except:
#                 print("Fichier d'options corrompus ou inexistant !! Initialisation ...")
#                 options.defaut()
        else:
            options.defaut()
        self.options = options
#        print options
        
        # On applique les options ...
        self.DefinirOptions(options)
        
        
        
        
        
        
        ##############################################################################################
        # Taille et position de la fenétre
        ##############################################################################################
#         set_screen_scale()
        rs = getDisplaysPosSize()
        x, y, w, h = rs[0]
        #print wx.GetDisplaySize()
#         print("DisplayPosSize", rs)
        pos, siz = self.options.optFenetre["Position"], self.options.optFenetre["Taille"]
#         print("Position", pos, siz)
            
#         self.WMIN_STRUC*SSCALE = self.options.optFenetre["Larg_pnl_Arbre"]
#         self.HMIN_PROP*SSCALE = self.options.optFenetre["Haut_pnt_Prop"]
        
#         print(getDisplayPPI(self))
        
#         print pos, siz
#         print len(pos), len(siz)
#         print x, y, w, h
        
        if len(pos) == 2 and dansRectangle(*pos, rs)[0] \
            and len(siz) == 2 \
            and pos[0] < w \
            and pos[1] < h:
            self.SetPosition(pos)
            self.SetSize(siz)
        else:
#             print("Centrage")
            self.SetPosition((w/2, y))
            self.SetSize((w/2,h))
        
        self.SetMinSize((800,570)) # Taille mini d'écran : 800x600
        #self.SetSize((1024,738)) # Taille pour écran 1024x768
        # On centre la fenétre dans l'écran ...
        #self.CentreOnScreen(wx.BOTH)
        
        
        self.Bind(wx.EVT_MOVE, self.onMoveWindow)
        
        
        self.SetIcon(images.getlogoIcon())
        
        wx.CallAfter(self.connect)
        
                
        # Pour drag&drop direct de fichiers
        file_drop_target = MyFileDropTarget(self)
        self.SetDropTarget(file_drop_target)
#         self.tabmgr.GetManagedWindow().SetDropTarget(file_drop_target)
        
        
        
        #############################################################################################
        # Quelques variables ...
        #############################################################################################
        self.fichierClasse = ""
        self.pleinEcran = False
        # Element placé dans le "presse papier"
        self.elementCopie = None
        
        
        
        
        # !!! cette ligne pose problème à la fermeture : mystère
#         self.renommerWindow()
        
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
        
        self.Bind(wx.EVT_MENU, self.genererZip, id=25)
        
#        if sys.platform == "win32":
#            self.Bind(wx.EVT_MENU, self.etablirBilan, id=18)
            
        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)
        
        self.Bind(wx.EVT_MENU, self.OnAide, id=21)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=22)
        self.Bind(wx.EVT_MENU, self.OnBug, id=23)
        
#        self.Bind(wx.EVT_MENU, self.OnOptions, id=31)
        
        if sys.platform == "win32" :
            self.Bind(wx.EVT_MENU, self.OnRegister, id=32)
        
        self.Bind(wx.EVT_MENU, self.OnReparer, id=33)
        self.Bind(wx.EVT_MENU, self.OnRecupEtab, id=34)
        self.Bind(wx.EVT_MENU, self.OnRecupFeries, id=35)
        self.Bind(wx.EVT_MENU, self.telechargerBO, id=36)
        
        self.Bind(EVT_APPEL_OUVRIR, self.OnAppelOuvrir)
        
        
        
        # Interception des frappes clavier
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        
        # Interception de la demande de fermeture
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        # Sortie de la fenêtre
        self.Bind(wx.EVT_LEAVE_WINDOW, self.HideTip)
        
        
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


        # Récupération de la derniére version
        
        a = threading.Thread(None, version.GetNewVersion, None,  (self,) )
        a.start()

        self.timerAutosave.Start(DUREE_AUTOSAVE)
        
        self.Thaw()
        
#     ###############################################################################################
#     def GetNotebook(self):
#         if int(wx.version()[0]) > 2:
#             return self.GetClientWindow().GetAuiManager().GetManagedWindow()
#         else:
#             return self.GetClientWindow().GetAuiManager().GetManagedWindow()
            
    def connect(self):
        nb = self.GetNotebook()
#         self.tabmgr = self.GetClientWindow().GetAuiManager()
        
        
#         nb.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.OnDocClosed)
        nb.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnCloseDoc)
        nb.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnDocChanged)

    ###############################################################################################
    def onMoveWindow(self, event):
        global SSCALE
        pass
#         print("onMoveWindow")
#         print("   display:",wx.Display.GetFromWindow(self))
#         print("   PPI:", getDisplayPPI(self))
#         SSCALE = getDisplayPPI(self)[0]/96
        
        
        
    ###############################################################################################
    def GetCurrentPage(self):
        nb = self.GetNotebook()
        if int(wx.version()[0]) > 2:
            return nb.GetCurrentPage()
        else:
            return nb.GetPage(nb.GetSelection())
        
        
        ###############################################################################################
    def renommerWindow(self):
        menu_bar = self.GetMenuBar()
#        menu_bar.SetMenuLabel(3, u"Fenétre")
#        menu_bar.SetMenuLabel(menu_bar.FindMenu("Window"), u"Fenétre")
        
    
    ###############################################################################################
    def SetData(self, data):  
        self.elementCopie = data      
        
    ###############################################################################################
    def RenameTools(self, typ):
        fenDoc = self.GetCurrentPage()
        if hasattr(fenDoc, 'typ'):
            ref = fenDoc.GetDocument().GetReferentiel()
            for tool in self.tools[fenDoc.typ]:
                # Projets ###############################################################
                if tool.GetId() == 50:
                    tool.SetLabel("Ajouter %s" %ref.getLabel("ELEVES").un_())
                    tool.SetShortHelp("Ajout %s au projet" %ref.getLabel("ELEVES").de_())
                    tool.SetLongHelp("Ajout %s au projet" %ref.getLabel("ELEVES").de_())
                
                elif tool.GetId() == 54:
                    tool.SetLabel("Ajouter un groupe %s" %ref.getLabel("ELEVES").de_plur_())
                    tool.SetShortHelp("Ajout d'un groupe %s au projet" %ref.getLabel("ELEVES").de_plur_())
                    tool.SetLongHelp("Ajout d'un groupe %s au projet" %ref.getLabel("ELEVES").de_plur_())
                
                elif tool.GetId() == 51:
                    tool.SetLabel("Ajouter un professeur")
                    tool.SetShortHelp("Ajout d'un professeur à l'équipe pédagogique")
                    tool.SetLongHelp("Ajout d'un professeur à l'équipe pédagogique")
        
                elif tool.GetId() == 52:
                    tool.SetLabel("Ajouter %s" %ref._nomTaches.un_())
                    tool.SetShortHelp("Ajout %s au projet" %ref._nomTaches.de_())
                    tool.SetLongHelp("Ajout %s au projet" %ref._nomTaches.de_())
    
                elif tool.GetId() == 53:
                    tool.SetLabel("Ajouter une revue")
                    tool.SetShortHelp("Ajout d'une revue au projet")
                    tool.SetLongHelp("Ajout d'une revue au projet")
    
                elif tool.GetId() == 55:
                    tool.SetLabel("Ajouter un modèle")
                    tool.SetShortHelp("Ajout d'un modèle numérique du support")
                    tool.SetLongHelp("Ajout d'un modèle numérique du support")
                    
                elif tool.GetId() == 56:
                    tool.SetLabel("Ajouter %s" %ref.getLabel("EXIG").sing_())
                    tool.SetShortHelp("Ajout %s au Projet" %ref.getLabel("EXIG").de_())
                    tool.SetLongHelp("Ajout %s au Projet" %ref.getLabel("EXIG").de_())
                
                
                # Séquences ##################################################################
                elif tool.GetId() == 60:
                    tool.SetLabel("Ajouter %s" %ref._nomActivites.un_())
                    tool.SetShortHelp("Ajout %s dans la Séquence" %ref._nomActivites.de_())
                    tool.SetLongHelp("Ajout %s dans la Séquence" %ref._nomActivites.de_())
                    
                elif tool.GetId() == 62:
                    tool.SetLabel("Ajouter un professeur")
                    tool.SetShortHelp("Ajout d'un professeur à l'équipe pédagogique")
                    tool.SetLongHelp("Ajout d'un professeur à l'équipe pédagogique")
                    
                elif tool.GetId() == 61:
                    tool.SetLabel("Ajouter %s" %et2ou(ref._nomSystemes.un_()))
                    tool.SetShortHelp("Ajout %s" %et2ou(ref._nomSystemes.de_()))
                    tool.SetLongHelp("Ajout %s" %et2ou(ref._nomSystemes.de_()))
                    
                
                # Progressions ###############################################################
                elif tool.GetId() == 70:
                    tool.SetLabel("Actualiser la Progression")
                    tool.SetShortHelp("Actualiser la Progression")
                    tool.SetLongHelp("Actualiser la Progression")
                
                elif tool.GetId() == 71:
                    tool.SetLabel("Ajouter un professeur")
                    tool.SetShortHelp("Ajout d'un professeur à l'équipe pédagogique")
                    tool.SetLongHelp("Ajout d'un professeur à l'équipe pédagogique")
                       
                elif tool.GetId() == 72:
                    tool.SetLabel("Ajouter une Séquence")
                    tool.SetShortHelp("Ajout d'une Séquence à la Progression")
                    tool.SetLongHelp("Ajout d'une Séquence à la Progression")
                    
                elif tool.GetId() == 73:
                    tool.SetLabel("Ajouter un Projet")
                    tool.SetShortHelp("Ajout d'un Projet à la Progression")
                    tool.SetLongHelp("Ajout d'un Projet à la Progression")
    
    
    
    
    ###############################################################################################
    def GetTools(self, typ):
        """ Renvoie la liste des id et images des boutons de la toolbar
            pour le type <typ>
            Format :
                [(id, wx.Bitmap), (id, wx.Bitmap), ...]
        """
        ts = (IMG_SIZE_TB[0]*SSCALE, IMG_SIZE_TB[1]*SSCALE)
        if typ == 'prj':
            return [(50 , scaleImage(images.Icone_ajout_eleve.GetBitmap(), *ts)),
                    
                    (54 , scaleImage(images.Icone_ajout_groupe.GetBitmap(), *ts)),
                
                    (51 , scaleImage(images.Icone_ajout_prof.GetBitmap(), *ts)),
                    
                    (0, None),
                    
                    (56 , scaleImage(images.Icone_ajout_FS.GetBitmap(), *ts)),
                    
                    (52 , scaleImage(images.Icone_ajout_tache.GetBitmap(), *ts)),
                    
                    (53 , scaleImage(images.Icone_ajout_revue.GetBitmap(), *ts)),
                    
                    (0, None),
                    
                    (55 , scaleImage(images.Icone_ajout_modele.GetBitmap(), *ts)),
                    ]
        
        elif typ == 'seq':
            return [(60 , scaleImage(images.Icone_ajout_seance.GetBitmap(), *ts)),
                    
                    (62 , scaleImage(images.Icone_ajout_prof.GetBitmap(), *ts)),
                    
                    (61 , scaleImage(images.Icone_ajout_systeme.GetBitmap(), *ts))
                      ]
            
        elif typ == 'prg':
            return [(70 , scaleImage(images.Bouton_Actualiser.GetBitmap(), *ts)),
                    
                    (0, None),
                    
                    (71 , scaleImage(images.Icone_ajout_prof.GetBitmap(), *ts)),
                    
                    (72 , scaleImage(images.Icone_ajout_seq.GetBitmap(), *ts)),
                    
                    (73 , scaleImage(images.Icone_ajout_prj.GetBitmap(), *ts)),
                  ]
            
            
    ###############################################################################################
    def GetBoutonToolBar(self, typ, n):
        for btn in self.tools[typ]:
            if btn.GetId() == n:
                return btn
            
    ###############################################################################################
    def ConstruireTb(self):
        """ Construction de la ToolBar
        """
#        print "ConstruireTb"

        #############################################################################################
        # Création de la barre d'outils
        #############################################################################################
        self.tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        
        
        tsize = (IMG_SIZE_TB[0]*SSCALE, IMG_SIZE_TB[1]*SSCALE)
        
        new_bmp =  scaleImage(images.Icone_new.GetBitmap(), *tsize)
        open_bmp = scaleImage(images.Icone_open.GetBitmap(), *tsize)
        save_bmp =  scaleImage(images.Icone_save.GetBitmap(), *tsize)
        saveall_bmp =  scaleImage(images.Icone_saveall.GetBitmap(), *tsize)
        saveas_bmp = scaleImage(images.Icone_saveas.GetBitmap(), *tsize)
        undo_bmp = scaleImage(images.Icone_undo.GetBitmap(), *tsize)
        redo_bmp = scaleImage(images.Icone_redo.GetBitmap(), *tsize)
        full_bmp = scaleImage(images.Icone_fullscreen.GetBitmap(), *tsize)
        
        
        self.tb.SetToolBitmapSize(tsize)
        
        self.tb.AddTool(10, "Nouveau", new_bmp, wx.NullBitmap,
                             shortHelp="Création d'une nouvelle séquence ou d'un nouveau projet", 
                             longHelp="Création d'une nouvelle séquence ou d'un nouveau projet")
        

        self.tb.AddTool(11, "Ouvrir", open_bmp, wx.NullBitmap,
                             shortHelp="Ouverture d'un fichier séquence ou projet", 
                             longHelp="Ouverture d'un fichier séquence ou projet")
        
        self.tb.AddTool(12, "Enregistrer", save_bmp, wx.NullBitmap,
                             shortHelp="Enregistrement du document courant sous son nom actuel", 
                             longHelp="Enregistrement du document courant sous son nom actuel")
        
        self.tb.AddTool(14, "Enregistrer tout", saveall_bmp, wx.NullBitmap,
                             shortHelp="Enregistrement de tous les documents sous leurs noms actuels", 
                             longHelp="Enregistrement de tous les documents sous leurs noms actuels")
        

        self.tb.AddTool(13, "Enregistrer sous...", saveas_bmp, wx.NullBitmap,
                             shortHelp="Enregistrement du document courant sous un nom différent", 
                             longHelp="Enregistrement du document courant sous un nom différent")
        
        self.Bind(wx.EVT_TOOL, self.commandeNouveau, id=10)
        self.Bind(wx.EVT_TOOL, self.commandeOuvrir, id=11)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrer, id=12)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrerSous, id=13)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrerTout, id=14)
        
        
        self.tb.AddSeparator()
        
        self.tb.AddTool(200, "Annuler", undo_bmp, wx.NullBitmap,
                             shortHelp="Annuler", 
                             longHelp="Annuler")
        

        self.tb.AddTool(201, "Rétablir", redo_bmp, wx.NullBitmap,
                             shortHelp="Rétablir", 
                             longHelp="Rétablir")
        
        
        self.tb.AddSeparator()
        
        self.Bind(wx.EVT_TOOL, self.commandeUndo, id=200)
        self.Bind(wx.EVT_TOOL, self.commandeRedo, id=201)
        
        
        #################################################################################################################
        #
        # Outils "Projet" ou  "séquence" ou "progression" ou ...
        #
        #################################################################################################################
        self.tools = {'prj' : [], 'seq' : [], 'prg' : []}
        for typ in ['prj', 'seq', 'prg']:
            for i, bmp in self.GetTools(typ):
                if i > 0:
                    self.tools[typ].append(self.tb.AddTool(i, "", bmp, wx.NullBitmap))
                self.RenameTools(typ)
#                 else:
#                     self.tb.AddSeparator()

        

        self.tb.AddSeparator()
        #################################################################################################################
        #
        # Outils de Visualisation
        #
        #################################################################################################################
        
        self.tb.AddTool(100, "Plein écran", full_bmp, wx.NullBitmap,
                             shortHelp="Affichage de la fiche en plein écran (Echap pour quitter le mode plein écran)", 
                             longHelp="Affichage de la fiche en plein écran (Echap pour quitter le mode plein écran)")

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
        self.supprimerOutils()
        self.miseAJourUndo()
        
        
        
    ###############################################################################################
    def supprimerOutils(self):
        self.tb.RemoveTool(60)
        self.tb.RemoveTool(61)
        self.tb.RemoveTool(62)
        
        self.tb.RemoveTool(50)
        self.tb.RemoveTool(51)
        self.tb.RemoveTool(52)
        self.tb.RemoveTool(53)
        self.tb.RemoveTool(54)
        self.tb.RemoveTool(55)
        self.tb.RemoveTool(56)
        
        self.tb.RemoveTool(70)
        self.tb.RemoveTool(71)
        self.tb.RemoveTool(72)
        self.tb.RemoveTool(73)


    ###############################################################################################
    def ajouterOutils(self, typ):
        self.supprimerOutils()

        d = 8 # Position à changer selon le nombre d'outils "communs"
        for tool in self.tools[typ]:
            self.tb.InsertTool(d,tool)
            d += 1
        
        
        self.tb.Realize()


    ###############################################################################################
    def miseAJourUndo(self):
        """ Mise à jour des boutons (et menus)
            après une opération undo ou redo
        """
#         print("miseAJourUndo")
        try:
            doc = self.GetDocActif()
        except:
            doc = None
        if doc == None:
            self.tb.EnableTool(200, False)
            self.tb.EnableTool(201, False)
            return
        
        undoAction = doc.undoStack.getUndoAction()
    
        if undoAction == None:
            self.tb.EnableTool(200, False)
            t = ""
        else:
            self.tb.EnableTool(200, True)
            t = "\n"+undoAction
        self.tb.SetToolShortHelp(200, "Annuler"+t)

        redoAction = doc.undoStack.getRedoAction()
        if redoAction == None:
            self.tb.EnableTool(201, False)
            t = ""
        else:
            self.tb.EnableTool(201, True)
            t = "\n"+redoAction
        self.tb.SetToolShortHelp(201, "Rétablir"+t)
        
        
    ###############################################################################################
    def commandePleinEcran(self, event):
        """
        """
        
            
        fenDoc = self.GetCurrentPage()
        
        if fenDoc is None:
            return
        
#        if self.GetNotebook().GetCurrentPage() == None:
#            return
        
        self.pleinEcran = not self.pleinEcran
        
        if self.pleinEcran:
            pos = None
            if wx.Display.GetCount() > 1:
                ch = DisplayChoice(self)
                ch.ShowModal()
                pos = ch.GetValue()
                ch.Destroy()
            if pos is None:
                pos = [0,0]
            win = fenDoc.nb.GetCurrentPage()
            self.fsframe = wx.Frame(self, -1)
            self.fsframe.SetPosition(pos)
            win.Reparent(self.fsframe)
            
            win.Bind(wx.EVT_KEY_DOWN, self.OnKey)
            
            self.fsframe.ShowFullScreen(True, style=wx.FULLSCREEN_ALL)
            win.OnResize()
        else:
            win = self.fsframe.GetChildren()[0]
            win.Reparent(fenDoc.nb)
            self.fsframe.Destroy()
            win.SendSizeEventToParent()


    ###############################################################################################
    def CreateMenuBar(self):
        # create menu
        
#         window_menu = self.GetWindowMenu()
#         window_menu.SetLabel(4001, u"Fermer")
#         window_menu.SetLabel(4002, u"Fermer tout")
#         window_menu.SetLabel(4003, u"Suivante")
#         window_menu.SetLabel(4004, u"Précédente")
#         
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(10, "&Nouveau\tCtrl+N")
        file_menu.Append(11, "&Ouvrir\tCtrl+O")
        
        submenu = wx.Menu()
#         file_menu.Append(14, "&Ouvrir un fichier récent", submenu)
        file_menu.AppendSubMenu(submenu, "&Ouvrir un fichier récent")
        self.filehistory = wx.FileHistory()
        self.filehistory.UseMenu(submenu)
        
        file_menu.Append(12, "&Enregistrer\tCtrl+S")
        file_menu.Append(13, "&Enregistrer sous ...")
        file_menu.AppendSeparator()
        
#        file_menu.AppendSeparator()
        file_menu.Append(15, "&Exporter la fiche\tCtrl+E")
        file_menu.Append(16, "&Exporter les détails\tCtrl+D")
        
        if sys.platform == "win32":
            file_menu.Append(17, "&Générer les grilles d'évaluation projet\tCtrl+G")
            file_menu.Append(20, "&Générer les grilles d'évaluation projet en PDF\tCtrl+P")
        
        self.menuDos = file_menu.Append(19, "&Générer le dossier de projet\tAlt+V")
        
        file_menu.Append(25, "Générer le dossier complet (archive &Zip)\tAlt+Z")
        
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, "&Quitter\tCtrl+Q")
        
        self.file_menu = file_menu
        
        tool_menu = wx.Menu()
        
#        if sys.platform == "win32":
#            tool_menu.Append(18, u"&Générer une Synthése pédagogique\tCtrl+B")
#            tool_menu.AppendSeparator()
        
        if sys.platform == "win32":# and util_path.INSTALL_PATH != None:
    #        tool_menu.Append(31, u"Options")
            self.menuReg = tool_menu.Append(32, "a")
            
        self.menuRep = tool_menu.Append(33, "Ouvrir et réparer un fichier")
        tool_menu.Append(34, "Récupérer les noms d'établissement")
        tool_menu.Append(35, "Récupérer les jours fériés")
        tool_menu.Append(36, "Télécharger les documents officiels")

        self.tool_menu = tool_menu
        
        help_menu = wx.Menu()
        help_menu.Append(21, "&Aide en ligne\tF1")
        help_menu.Append(23, "Envoyer un rapport de &bug")
        help_menu.AppendSeparator()
        help_menu.Append(22, "A propos")

        mb.Append(file_menu, "&Fichier")
        mb.Append(tool_menu, "&Outils")
        mb.Append(help_menu, "&Aide")
        
        self.MiseAJourMenu()
        
        self.SetMenuBar(mb)
    
    
    #############################################################################
    def MiseAJourMenu(self):
#         print("MiseAJourMenu")
        if hasattr(self, 'menuReg'):
            if register.IsRegistered():
                self.menuReg.SetItemLabel("Désinscrire de la base de registre")
            else:
                self.menuReg.SetItemLabel("Inscrire dans la base de registre")
        
        fenDoc = self.GetCurrentPage()
        if fenDoc is not None:
            doc = fenDoc.GetDocument()
            ref = doc.GetReferentiel()
#             print("   ", doc)
            self.menuDos.SetItemLabel("&Générer %s\tAlt+V" %ref.getLabel("PRJVAL").le_())
        
            prj = isinstance(doc, pysequence.Projet)
            self.file_menu.Enable(17, prj and grilles.EXT_EXCEL != None)
            self.file_menu.Enable(19, prj and grilles.EXT_EXCEL != None)
            self.file_menu.Enable(20, prj)
            self.file_menu.Enable(25, prj)
                
        
#         if sys.platform == "win32":
#             self.file_menu.Enable(17, prj)
#             self.file_menu.Enable(20, prj)
            
            
    #############################################################################
    def MiseAJourToolBar(self):
        return
#         fenDoc = self.GetCurrentPage()
#         if fenDoc is not None and fenDoc.typ == 'prg': #and hasattr(fenDoc, 'progression') 
#             coderef = fenDoc.progression.GetReferentiel().Code
#     #         print "   ", coderef
#             btnPrj = self.GetBoutonToolBar(fenDoc.typ, 73)
#             if btnPrj is not None:
#     #             print "   ", REFERENTIELS[coderef].projets
#                 btnPrj.Enable(len(REFERENTIELS[coderef].projets) > 0)
#                 self.tb.Realize()
            
    #############################################################################
    def DefinirOptions(self, options):
        for f in reversed(options.optFichiers["FichiersRecents"]):
#            print "Ajout3", f
            try:
                self.filehistory.AddFileToHistory(toFileEncoding(f))
            except:
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
        dlg = wx.MessageDialog(self, "Ouvrir et réparer un fichier\n\n" \
                               "L'opération qui va suivre permet d'ouvrir un fichier\n" \
                               "en restaurant les valeurs par défaut du référentiel d'enseignement.\n" \
                               "Si le document utilise un programme d'enseignement personnalisé,\n" \
                               "les spécificités de ce dernier seront perdues.\n\n"\
                               "Voulez-vous continuer ?",
                                 "Ouvrir et réparer",
                                 wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                 )
        res = dlg.ShowModal()
        dlg.Destroy() 
        if res == wx.ID_YES:
            self.commandeOuvrir(reparer = True)
            


    #############################################################################
    def OnRecupEtab(self, event):
        dlg = wx.MessageDialog(self, "Récupérer les noms d'établissement\n\n" \
                               "L'opération qui va suivre permet de récupérer sur Internet\n" \
                               "la liste officielle des collèges et lycées Français.\n\n" \
                               "Cette opération ne se justifie que s'il manque\n" \
                               "un(des) établissement(s) dans le fichier fourni avec pySéquence.\n\n" \
                               "Il est conseillé de faire une sauvegarde du fichier\n" \
                               "\t    etablissements.xml\n"\
                               "qui sera remplacé par un nouveau.\n\n"\
                               "L'opération peut durer plusieurs minutes\n" \
                               "et nécessite une connexion à Internet !!\n\n"\
                               "Voulez-vous continuer ?",
                                 "Récupérer les noms d'établissement",
                                 wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                 )
        res = dlg.ShowModal()
        dlg.Destroy() 
        if res == wx.ID_YES:
            import getEtab
            fileName = getEtab.SauvEtablissements(self, util_path.APP_DATA_PATH)
            if fileName is not None:
                dlg = wx.MessageDialog(self, "Le fichier a bien été enregistré\n\n%s\n\n"\
                                       "Voulez-vous l'ouvrir ?" %fileName, 
                                       "Fichier enregistré",
                                       wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL)
                res = dlg.ShowModal()
                constantes.ETABLISSEMENTS = getEtab.ouvrir()
                if res == wx.ID_YES:
                    try:
                        os.startfile(fileName)
                    except:
                        messageErreur(None, "Ouverture impossible",
                                      "Impossible d'ouvrir le fichier\n\n%s\n" %toSystemEncoding(fileName))
            else:
                dlg = wx.MessageDialog(self, "Opération annulée\n\n", 
                                       "Opération annulée",
                                       wx.ICON_ERROR | wx.OK)
                res = dlg.ShowModal()
            
            dlg.Destroy()
        
    #############################################################################
    def OnRecupFeries(self, event):
        dlg = wx.MessageDialog(self, "Récupérer les jours fériés\n\n" \
                               "L'opération qui va suivre permet de récupérer sur Internet\n" \
                               "la liste officielle des jours fériés.\n\n" \
                               "Cette opération ne se justifie qu'une seule fois par an.\n\n" \
                               "Il est conseillé de faire une sauvegarde du fichier\n" \
                               "\t    JoursFeries.xml\n"\
                               "qui sera remplacé par un nouveau.\n\n"\
                               "L'opération nécessite une connexion à Internet !!\n\n"\
                               "Voulez-vous continuer ?",
                                 "Récupérer les jours fériés",
                                 wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                 )
        res = dlg.ShowModal()
        dlg.Destroy() 
        if res == wx.ID_YES:
            import getEtab
            fileName = getEtab.SauvFeries(self, util_path.APP_DATA_PATH)
            if fileName is not None:
                dlg = wx.MessageDialog(self, "Le fichier a bien été enregistré\n\n%s\n\n"\
                                       "Voulez-vous l'ouvrir ?" %fileName, 
                                       "Fichier enregistré",
                                       wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL)
                res = dlg.ShowModal()
                if res == wx.ID_YES:
                    try:
                        os.startfile(fileName)
                    except:
                        messageErreur(None, "Ouverture impossible",
                                      "Impossible d'ouvrir le fichier\n\n%s\n" %toSystemEncoding(fileName))
            else:
                dlg = wx.MessageDialog(self, "Opération annulée\n\n", 
                                       "Opération annulée",
                                       wx.ICON_ERROR | wx.OK)
                res = dlg.ShowModal()
            
            dlg.Destroy()    
                
    #############################################################################
    def OnRegister(self, event): 
        if register.IsRegistered():
            ok = register.UnRegister()
        else:
            ok = register.Register(util_path.PATH)
        if not ok:
            messageErreur(self, "Accès refusé",
                          "Accès à la base de registre refusé !\n\n" \
                          "Redémarrer %s en tant qu'administrateur." %version.__appname__)
        else:
            self.MiseAJourMenu()
         
    #############################################################################
    def OnAbout(self, event):
        win = A_propos(self)
        win.ShowModal()
        
    #############################################################################
    def OnBug(self, event):
        import platform
        recipient = version.__mail__.replace("#", "@")
        subject = "Rapport de Bug %s" %version.__appname__
        body = "Bonjour,\n\n J'ai (ou je crois avoir) constaté un bug !\n\n"
        body += "Version %s : %s\n" %(version.__appname__, version.__version__)
        body += "Système : %s\n" %platform.platform()
        body += "Description du bug : \n   ... décrire ici ce qui se produit d'anormal ... ne pas hésiter à joindre des images ...\n\n"
        body += "Moyen de le reproduire : \n   ... décrire ici un moyen de reproduire le problème constaté ... joindre si besoin un fichier .seq, .prj ou .prg ...\n\n"
        body += "Merci d'avance !"
        
        body = body.replace(' ', '%20')
        body = body.replace('\n', '%0D%0A')
        
#         bodyh = u"""<html>
#         <head>
#     
#         <meta http-equiv="content-type" content="text/html; charset=utf-8">
#         <title>Rapport de Bug pySéquence</title>
#       </head>
#       <body>
#         %s
#       </body>
#     </html>""" %body
     
        try:
            webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)
        except:
            messageErreur(None, "Envoi impossible",
                          "Impossible d'envoyer le rapport")
        
        
    #############################################################################
    def OnAide(self, event):
        try:
            webbrowser.open(version.__url__+'/wiki',new=2)
        except:
            messageErreur(None, "Ouverture impossible",
                          "Impossible d'ouvrir l'url\n\n%s\n" %toSystemEncoding(self.path))

        
    #############################################################################
    def OnTimer(self, event = None):
        for page in [self.GetNotebook().GetPage(i) for i in range(self.GetNotebook().GetPageCount())]:
            try:
                page.autoSave(event)
            except:
                if DEBUG:
                    raise
        
        self.timerAutosave.Start(DUREE_AUTOSAVE)
        
        
    ###############################################################################################
    def commandeNouveau(self, event = None, ext = None, ouverture = False):
        """ Création d'un nouveau document dans une fenêtre
        
            :ext: extension de fichier pour déterminer le type de document
                    (si None, ouvre un dialogue)
            :ouverture: True si la création doit être suivie d'une ouverture de fichier
        """
#         print "commandeNouveau"
        if ext == None:
            dlg = DialogChoixDoc(self)
            val = dlg.ShowModal()
            dlg.Destroy()
            if val == 1:
                ext = 'seq' 
            elif val == 2:
                ext = 'prj'
            elif val == 3:
                ext = 'prg'
            else:
                return
                
        if ext == 'seq':
            child = FenetreSequence(self, ouverture)
            child.SetIcon(scaleIcone(constantes.dicimages["Seq"].GetBitmap()))
        elif ext == 'prj':
            child = FenetreProjet(self, ouverture)
            child.SetIcon(scaleIcone(constantes.imagesProjet["Prj"].GetBitmap()))
        elif ext == 'prg':
            child = FenetreProgression(self, ouverture)
            child.SetIcon(scaleIcone(constantes.imagesProgression["Prg"].GetBitmap()))
        else:
            child = None

#         if not ouverture: # Si c'est vraiment pour un document vide
        self.OnDocChanged(None)
         
        if child != None:
            wx.CallAfter(child.Activate)
            
        return child


    ###############################################################################################
    def dropFiles(self, file_list):
        for path in file_list:
            self.ouvrir(path)
            
            
    ###############################################################################################
    def ouvrirDoc(self, doc, nomFichier):
        """ Ouvre un document à partir de sa version "pySequence"
            <nomFichier> encodé en FileEncoding

        """
#         print("ouvrirDoc", doc)
        return self.ouvrir(nomFichier)
        
        
        # Ancienne version : Pourquoi ?
#         if doc.GetType() == 'seq':
#             child = FenetreSequence(self, sequence = doc)
#             child.SetIcon(scaleIcone(constantes.dicimages["Seq"].GetBitmap()))
#              
#         elif doc.GetType() == 'prj':
#              
#             child = FenetreProjet(self, projet = doc)
#             child.SetIcon(scaleIcone(constantes.dicimages["Prj"].GetBitmap()))
#         child.finaliserOuverture()
#          
#         child.definirNomFichierCourant(nomFichier)
#         wx.CallAfter(child.Activate)
#         self.OnDocChanged()
#         return child
    
#     root = ET.parse(fichier).getroot()
#             
#             # La séquence
#             sequence = root.find("Sequence")
#             if sequence == None: # Ancienne version , forcément STI2D-ETT !!
# #                self.classe.GetPanelPropriete().EvtRadioBox(CodeFam = ('ET', 'STI'))
#                 self.sequence.setBranche(root)
#             else:
#                 # La classe
#                 classe = root.find("Classe")
#                 self.classe.setBranche(classe, reparer = reparer)
#                 self.sequence.MiseAJourTypeEnseignement()
#                 self.sequence.setBranche(sequence)  
# 
#             if reparer:
#                 self.VerifierReparation()
#                 
#             self.finaliserOuverture()
            
            
            
    
    ###############################################################################################
    def ouvrir(self, nomFichier, reparer = False):
        print("ouvrir", nomFichier, reparer, os.getcwd())
        
        nomFichier = util_path.verifierPath(nomFichier)
        if len(nomFichier) == 0:
            messageErreur(None, 'Erreur !',
                  "Impossible de trouver le fichier\n\n%s" %toSystemEncoding(nomFichier))
            return
        
        
        self.Freeze()
        wx.BeginBusyCursor()
        
        doc = None

#         nomFichier = os.path.join(self.GetDocument(), nomFichier)
        
        if nomFichier != '':
            ext = os.path.splitext(nomFichier)[1].lstrip('.')
            
            #
            # Le Fichier n'est pas déja ouvert
            #
            if not nomFichier in self.GetNomsFichiers():
#                 if ext == "seq":
#                     #
#                     # On vérifie si la Séquence fait partie d'une Progression ouverte
#                     #
#                     path2 = os.path.normpath(os.path.abspath(nomFichier))
#                     for prog in self.GetDocumentsOuverts('prg'):
#                         for lienSeq in prog[0].sequences_projets:
#                             path1 = os.path.normpath(os.path.abspath(lienSeq.path))
#                             if path1 == path2:  # La séquence fait partie d'une progression ouverte
# #                                 print "Dans prog :", path2
#                                 self.ouvrirDoc(lienSeq.sequence, nomFichier)
#                                 wx.EndBusyCursor()
#                                 self.Thaw()
#                                 return lienSeq.sequence
                
                child = self.commandeNouveau(ext = ext, ouverture = True)
#                 print("doc=",child)
                if child != None:
                    doc = child.ouvrir(nomFichier, reparer = reparer)
                    
#                     print("xxx", doc)
                   
                    
            # Le Fichier est déja ouvert
            else:
                child = self.GetChild(nomFichier)
                texte = constantes.MESSAGE_DEJA[ext] % child.fichierCourant
#                if child.fichierCourant != '':
#                    texte += "\n\n\t"+child.fichierCourant+"\n"
                    
                dialog = wx.MessageDialog(self, texte, 
                                          "Confirmation", wx.YES_NO | wx.ICON_WARNING)
                retCode = dialog.ShowModal()
                if retCode == wx.ID_YES:
                    doc = child.ouvrir(nomFichier, reparer = reparer)
                else:
                    wx.EndBusyCursor()
                    self.Thaw()
                    return
                
            if doc is None:
                child.fermer()
                
            if not reparer and doc is not None:
#                 print "Ajout1", nomFichier
                self.filehistory.AddFileToHistory(nomFichier)
            
        wx.EndBusyCursor()
        self.Thaw()
        
        return doc


    ###############################################################################################
    def commandeOuvrir(self, event = None, nomFichier = None, reparer = False):
        mesFormats =  constantes.FORMAT_FICHIER['seqprj'] \
                    + constantes.FORMAT_FICHIER['seq'] \
                    + constantes.FORMAT_FICHIER['prj'] \
                    + constantes.FORMAT_FICHIER['prg'] \
                    + constantes.TOUS_FICHIER
  
        if nomFichier == None:
            dlg = wx.FileDialog(
                                self, message=f"Ouvrir un fichier {version.__appname__}",
#                                defaultDir = self.DossierSauvegarde, 
                                defaultFile = "",
                                wildcard = mesFormats,
                                style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
                                )

            if dlg.ShowModal() == wx.ID_OK:
#                 paths = dlg.GetPaths()
#                 nomFichier = paths[0]
                nomFichier = dlg.GetPath()#.decode(FILE_ENCODING)

            else:
                nomFichier = r''
            
            dlg.Destroy()
        if nomFichier != r'':
            self.ouvrir(nomFichier, reparer = reparer)
#         print("fin")
        
        
    ###############################################################################################
    def OnFileHistory(self, evt):
        # get the file based on the menu ID
        fileNum = evt.GetId() - wx.ID_FILE1
        path = self.filehistory.GetHistoryFile(fileNum)
#         print "You selected %s\n" % path
        if os.path.isfile(path):
            # add it back to the history so it will be moved up the list
#            print "Ajout2", path
            self.filehistory.AddFileToHistory(path)
            os.chdir(os.path.split(path)[0])
            self.commandeOuvrir(nomFichier = path)
            

    ###############################################################################################
    def GetFichiersRecents(self):
        lst = []
        for n in range(self.filehistory.GetCount()):
#            lst.append(toSystemEncoding(self.filehistory.GetHistoryFile(n)))
            lst.append(self.filehistory.GetHistoryFile(n))
        return lst


    ###############################################################################################
    def OnAppelOuvrir(self, evt):
        #print("OnAppelOuvrir")
        wx.CallAfter(self.ouvrir, evt.GetFile())
        
        
#        
        
        
        
    ###############################################################################################
    def AppelOuvrir(self, nomFichier):
        evt = AppelEvent(myEVT_APPEL_OUVRIR, self.GetId())
        evt.SetFile(nomFichier)
        self.GetEventHandler().ProcessEvent(evt)
        
    
    #############################################################################
    def commandeDelete(self, event = None):    
        print("Suppr")
    
    #############################################################################
    def commandeUndo(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.commandeUndo(event)
    
    #############################################################################
    def commandeRedo(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.commandeRedo(event)     
            
    #############################################################################
    def commandeEnregistrer(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.commandeEnregistrer(event)
        
    #############################################################################
    def commandeEnregistrerTout(self, event = None):
        for page in [self.GetNotebook().GetPage(i) for i in range(self.GetNotebook().GetPageCount())]:
#         for page in self.GetNotebook().GetPages():
            page.commandeEnregistrer(event)
        
    #############################################################################
    def commandeEnregistrerSous(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            nomFichier = page.commandeEnregistrerSous(event)
            if nomFichier is not None:
                self.filehistory.AddFileToHistory(nomFichier)
    
    #############################################################################
    def exporterFiche(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.exporterFiche()
              
    #############################################################################
    def exporterDetails(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.exporterDetails(event)
    
    #############################################################################
    def genererZip(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.genererZip(event)
            
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
    def telechargerBO(self, event = None):
        page = self.GetNotebook().GetCurrentPage()
        if page != None:
            page.TelechargerBO()
    
    ###############################################################################################
    def OnDocClosed(self, evt = None):   
#         print "OnDocClosed", evt

        if self.GetNotebook().GetPageCount() <= 1:
            self.supprimerOutils()
            self.tb.Realize()
        
        if evt is not None:
            evt.Skip()
            
    ###############################################################################################
    def OnDocChanged(self, evt = None):
        """ Opérations de modification du menu et des barres d'outils 
            en fonction du type de document en cours
            Et rafraichissement des séquences de la fenêtre de Progression
        """
#         print("OnDocChanged", evt)
        
        fenDoc = self.GetCurrentPage()
        
        
        if hasattr(fenDoc, 'typ'):
            self.ajouterOutils(fenDoc.typ)
            
            #
            # Connection des outils
            #
            if fenDoc.typ == "prj":
                self.Bind(wx.EVT_TOOL, fenDoc.projet.AjouterEleve,      id=50)
                self.Bind(wx.EVT_TOOL, fenDoc.projet.AjouterProf,       id=51)
                self.Bind(wx.EVT_TOOL, fenDoc.AjouterTache,             id=52)
                self.Bind(wx.EVT_TOOL, fenDoc.projet.InsererRevue,      id=53)
                self.Bind(wx.EVT_TOOL, fenDoc.projet.AjouterGroupe,      id=54)
                self.Bind(wx.EVT_TOOL, fenDoc.projet.support.AjouterModele,      id=55)
                self.Bind(wx.EVT_TOOL, fenDoc.projet.AjouterFS,      id=56)
                
            elif fenDoc.typ == "seq":
                self.Bind(wx.EVT_TOOL, fenDoc.sequence.AjouterSeance,   id=60)
                self.Bind(wx.EVT_TOOL, fenDoc.sequence.AjouterSysteme,  id=61)
                self.Bind(wx.EVT_TOOL, fenDoc.sequence.AjouterProf,     id=62)
                
            elif fenDoc.typ == "prg":
                self.Bind(wx.EVT_TOOL, fenDoc.progression.Rafraichir,     id=70)
                self.Bind(wx.EVT_TOOL, fenDoc.progression.AjouterProf,    id=71)
                self.Bind(wx.EVT_TOOL, fenDoc.progression.AjouterNouvelleSequence,     id=72)
                self.Bind(wx.EVT_TOOL, fenDoc.progression.AjouterNouveauProjet,     id=73)
                    
            #
            # Infosbulle des outils
            #
            self.RenameTools(fenDoc.typ)
            
                        
                        
            #
            # Eléments de Menu
            #
            if fenDoc.typ == "prj":
                for i in [17, 19, 20]:
                    if self.file_menu.FindItemById(i) is not None:
                        self.file_menu.Enable(i, True)
                
            elif fenDoc.typ == "seq":
                for i in [17, 19, 20]:
                    if self.file_menu.FindItemById(i) is not None:
                        self.file_menu.Enable(i, False)
                
            elif fenDoc.typ == "prg":
                for i in [17, 19, 20]:
                    if self.file_menu.FindItemById(i) is not None:
                        self.file_menu.Enable(i, False)
                
            if evt is not None:
                fenDoc.Rafraichir()
        
        else:
            self.supprimerOutils()
            self.tb.Realize()
            
        wx.CallAfter(self.MiseAJourToolBar)
        wx.CallAfter(self.MiseAJourMenu)
        
#         self.miseAJourUndo()


    ###############################################################################################
    def OnKey(self, evt):
#         print("OnKey2")
        keycode = evt.GetKeyCode()
#         print "!!", keycode
        if keycode == wx.WXK_ESCAPE:
            if self.pleinEcran:
                self.commandePleinEcran(evt)
            try:
                wx.EndBusyCursor()
            except:
                pass
               
        elif evt.ControlDown() and keycode == 90: # Ctrl-Z
            self.commandeUndo(evt)
   
        elif evt.ControlDown() and keycode == 89: # Ctrl-Y
            self.commandeRedo(evt)
               
        elif keycode == 46: # Suppr
            self.commandeDelete(evt)
               
        evt.Skip()
#     
                
    #############################################################################
    def GetChild(self, nomFichier):
        for m in self.GetChildren():
            if isinstance(m, aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    if isinstance(k, FenetreSequence):
                        if k.fichierCourant == nomFichier:
                            return k
                    elif isinstance(k, FenetreProjet):
                        if k.fichierCourant == nomFichier:
                            return k
                    elif isinstance(k, FenetreProgression):
                        if k.fichierCourant == nomFichier:
                            return k
        return
    
    
    #############################################################################
    def GetDocActif(self):
        if self.GetNotebook() != None and self.GetNotebook().GetCurrentPage() != None:
            return self.GetNotebook().GetCurrentPage().GetDocument()
    
    
    #############################################################################
    def HideTip(self, event = None):
#         print "HideTip principal"
        
        d = self.GetFenetreActive()
        print("HideTip", d)
        if d is not None:
            d.HideTip()
        event.Skip()
        
        
    #############################################################################
    def GetFenetreActive(self):
        return self.GetNotebook().GetCurrentPage()
    
    #############################################################################
    def GetNomsFichiers(self):
        """ Renvoie la liste des noms de fichier Séquence ouverts
        """
        lst = []
        for m in self.GetChildren():
            if isinstance(m, aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    if isinstance(k, FenetreSequence):
                        lst.append(k.fichierCourant)
                    elif isinstance(k, FenetreProjet):
                        lst.append(k.fichierCourant)

        return lst
    
    
    #############################################################################
    def GetDocumentsOuverts(self, typ):
        prog = []
        if self.GetNotebook() != None:
            for p in range(self.GetNotebook().GetPageCount()):
                page = self.GetNotebook().GetPage(p)
                if page.typ == typ:
                    prog.append((page.GetDocument(), page.fichierCourant))
        return prog
    
    
    
#     #########################################################################################################
#     def GetLargPnlArbre(self):
#         w = []
#         for m in self.GetChildren():
#             if isinstance(m, aui.AuiMDIClientWindow):
#                 for k in m.GetChildren():
#                     if isinstance(k, FenetreDocument):
#                         w.append(k.GetLargPnlArbre())
#         if len(w) > 0:
#             return max(w)
#         else:
#             return WMIN_STRUC*SSCALE
#          
#      
#     #########################################################################################################
#     def GetHautPnlProp(self):
#         h = []
#         for m in self.GetChildren():
#             if isinstance(m, aui.AuiMDIClientWindow):
#                 for k in m.GetChildren():
#                     if isinstance(k, FenetreDocument):
#                         h.append(k.GetHautPnlProp())
#         if len(h) > 0:
#             return max(h)
#         else:
#             return HMIN_PROP*SSCALE
    
    #############################################################################
    def OnCloseDoc(self, evt):
#         print("OnClose doc")
        fenDoc = self.GetNotebook().GetPage(evt.GetSelection())
        if fenDoc:
            if not fenDoc.quitter():
                evt.StopPropagation()
                evt.Veto()
#             print("   fin")

#         evt.Skip() # Crash !
        
    
    #############################################################################
    def OnClose(self, evt):
#         print("OnClose app")
        
#        try:
#            draw_cairo.enregistrerConfigFiche(self.nomFichierConfig)
#        except IOError:
#            print "   Permission d'enregistrer les options refusée...",
#        except:
#            print "   Erreur enregistrement options...",
        #
        # Fremeture du thread de test de version Excel
        #
        try:
            pysequence.th_xls.exit()
        except:
            pass
        
        
        #
        # Récupération des dimensions des fenêtres
        #
#         try:
        #self.options.definir()
        self.options.valider(self)
        self.options.enregistrer()
#         except PermissionError:
#             print("   Permission d'enregistrer les options refusée...", end=' ')
#         except:
#             print("   Erreur enregistrement options...", end=' ')
# #        
        
        # Close all ChildFrames first else Python crashes
        toutferme = True
        for m in self.GetChildren():
            if isinstance(m, aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    if isinstance(k, FenetreDocument):
                        toutferme = toutferme and k.quitter()  
        
#        print ">>", toutferme
        if toutferme:
            evt.Skip()





    

########################################################################################
#
#
#  Classe définissant la fenétre "Document" (séquence, projet, ...)
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
        self.fichierCourant = ""
        self.DossierSauvegarde = ""
        self.fichierCourantModifie = False
        self.fichierSauvegarde = ""
            
        #
        # Un NoteBook comme conteneur de la fiche
        #
        self.nb = wx.Notebook(self.pnl, -1)

        #
        # Création du Tip (PopupInfo)
        #
        self.tip = PopupInfo(self.parent, width = 500*SSCALE)
        self.zoneMove = None
        self.curTip = None
        
        # Les tip pour les différents objets
        self.tips = {}




#     ######################################################################################################
#     def OnClose(self, evt):
#         print "OnClose doc"
#         

    ###############################################################################################
    def GetDocument(self):
        return


#     #########################################################################################################
#     def HideTip(self, event = None):
# #         print("HideTip document")
#         self.GetDocument().HideTip()
    
    ######################################################################################  
    def HideTip(self, pos = None):
        if hasattr(self, 'call'):
            self.call.Stop()
            
        if self.curTip is not None:#hasattr(self, 'curTip'):
            if pos is not None:
                x, y = pos
#                 print x, y
                X, Y, W, H = self.curTip.GetRect()
#                 print X, Y, W, H
                if x > X and x < X+W and y > Y and y < Y+H:
                    return
            self.curTip.Show(False)
            
            
    ######################################################################################  
    def ShowTip(self, x, y):
        if self.curTip is None: 
            return
        
#         self.curTip.SetWidth(width)
#         print("ShowTip", self.curTip.w)
        _, _, W, H = getDisplaysPosSize()[0]
        w, h = self.curTip.GetSize()
        self.curTip.Position(getAncreFenetre(x, y, w, h, W, H, 10), (0,0))
        self.curTip.Show()
    
        
    ######################################################################################  
    def SetAndShowTip(self, zone, x, y):
#         print("SetAndShowTip", (x, y), zone.param, zone.obj)
             
#         self.HideTip()
        self.zoneMove = zone
        
        self.curTip = None 
        if zone.obj is not None and zone.param is None:
            self.tip.SetWidth(zone.getWidth())
#             print("    elem :", zone.obj)
            if type(zone.obj) != list:
                self.curTip = zone.obj.SetTip()
            else:
                self.curTip = zone.obj[0].SetTip()
         
        else:
#             print("    zone", zone.param)
            self.tip.SetWidth(zone.getWidth())
            self.GetDocument().SetTip(zone.param, zone.obj)
            self.curTip = self.tip
        
#         print("   ", self.curTip)
        if self.curTip != None:
            self.ShowTip(x, y)
#             X, Y, W, H = getDisplayPosSize()
#  
# #             print "  tip", x, y, tip.GetSize()
#  
#             w, h = tip.GetSize()
#             tip.Position(getAncreFenetre(x, y, w, h, W, H, 10), (0,0))
# #             self.call = wx.CallLater(500, tip.Show, True)
#             tip.Show()


    
    #########################################################################################################
    def createTip(self, code, page, width):
        """ Création (une seule fois) du Tip de l'objet désigné par un code
        
            :code: str
            :page: str = contenu par défaut du Tip
            :width: int largeur en pixel
        """
        self.tips[code] = PopupInfo(self.parent, page, width = width)
        return self.tips[code]
    
    
    #########################################################################################################
    def delTip(self, code):
        del self.tips[code]
    
    
    ######################################################################################  
    def Move(self, zone, x, y):
#         print("Move", x, y, zone)
            
        self.HideTip()
        
        if self.zoneMove != zone:
            self.call = wx.CallLater(500, self.SetAndShowTip, zone, x, y)
            
        else:
            self.call = wx.CallLater(500, self.ShowTip, x, y)
    
#     #########################################################################################################
#     def GetLargPnlArbre(self):
#         return self.arbre.GetSize()[0]
#         
#     
#     #########################################################################################################
#     def GetHautPnlProp(self):
#         return self.panelProp.GetSize()[1]
        
        
    #########################################################################################################
    def GetPanelProp(self):
        return self.panelProp.panel

    #########################################################################################################
    def sendEvent(self, doc = None, modif = "",
                  draw = True, verif = False):
#         print("sendEvent", modif, draw, verif)
        self.eventAttente = False
        evt = SeqEvent(myEVT_DOC_MODIFIED, self.GetId())
        if doc != None:
            evt.SetDocument(doc)
        else:
            evt.SetDocument(self.GetDocument())
        
        if modif != "":
            evt.SetModif(modif)
            
        evt.SetVerif(verif)
        evt.SetDraw(draw)
        
        self.GetEventHandler().ProcessEvent(evt)
        
        
    
    ###############################################################################################
    def Rafraichir(self):
        self.GetDocument().Rafraichir()
        wx.CallAfter(self.fiche.Redessiner)
        
            
    ###############################################################################################
    def miseEnPlace(self):
        
        #############################################################################################
        # Mise en place de la zone graphique
        #############################################################################################
        self.mgr.AddPane(self.nb, 
                         aui.AuiPaneInfo().
                         CenterPane().
                         DestroyOnClose(True)
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
#                         Floatable(False).
                         BestSize((WMIN_STRUC*SSCALE, HMIN_STRUC*SSCALE)).
                         MinSize((WMIN_STRUC*SSCALE, -1)).
                         Dockable(True).
#                         DockFixed().
#                         Gripper(False).
#                         Movable(False).
#                          Maximize().
                         Caption("Structure").
                         CaptionVisible(True).
#                         PaneBorder(False).
                         CloseButton(False).
                         DestroyOnClose(True)
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
                         BestSize((WMIN_PROP*SSCALE, HMIN_PROP*SSCALE)).
                         MinSize((WMIN_PROP*SSCALE, HMIN_PROP*SSCALE)).
                         MinimizeButton(True).
                         Resizable(True).

#                         DockFixed().
#                         Gripper(True).
#                         Movable(False).
#                         Maximize().
                         Caption("Propriétés").
                         CaptionVisible(True).
#                         PaneBorder(False).
                         CloseButton(False).
                         DestroyOnClose(True)
#                         Show()
                         )
        

        self.mgr.Update()

        self.definirNomFichierCourant(r'')

        sizer = wx.BoxSizer()
        sizer.Add(self.pnl, 1, wx.EXPAND)

        self.SetSizer(sizer)

        self.Layout()
        
        self.Bind(EVT_DOC_MODIFIED, self.OnDocModified)
#         self.Bind(wx.EVT_CLOSE, self.quitter)
#         self.Bind(wx.EVT_WINDOW_DESTROY, self.quitter)
        for c in self.GetChildren():
            c.Bind(wx.EVT_LEAVE_WINDOW, self.HideTip)
        
    #############################################################################
    def CleanClose(self):
        """ Tout ce qu'il faut faire pour que le document se ferme proprement ...
        """
        return
    
    
    #############################################################################
    def fermer(self):
#         print("Fermer", self)
        self.delFichierSauvegarde()
        
        
        # Pour mettre à jour la barre d'outils
        self.CleanClose()
        self.parent.OnDocClosed()
        
        try:
            self.mgr.UnInit()
        except:
            pass
# #         del self.mgr
#         self.mgr.Destroy()
        
        self.Close()
#         try:
#             wx.CallAfter(self.Destroy)
#             print("   ***")
#         except:
#             pass
        
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
        
        for nom, fct, img, ena in items:
            item = wx.MenuItem(menu, wx.ID_ANY, nom)
            if img != None:
                item.SetBitmap(img)
            item1 = menu.Append(item) 
            item.Enable(ena)
            self.Bind(wx.EVT_MENU, fct, item1)
        
        self.PopupMenu(menu)
        menu.Destroy()
    
    #############################################################################
    def dialogEnregistrer(self):
        mesFormats = constantes.FORMAT_FICHIER[self.typ] + constantes.TOUS_FICHIER
        dlg = wx.FileDialog(self, 
                            message = constantes.MESSAGE_ENR[self.typ], 
                            defaultDir=toSystemEncoding(self.DossierSauvegarde) , # encodage?
                            defaultFile="", wildcard=mesFormats, 
                            style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT|wx.FD_CHANGE_DIR
                            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()#.decode(FILE_ENCODING)
            dlg.Destroy()
            self.enregistrer(path)
            self.DossierSauvegarde = os.path.split(path)[0]
            return path
        else:
            dlg.Destroy()
    
    
    #############################################################################
    def ouvreProprietes(self, event = None):
        mesFormats =  "xml (.xml)|*.xml"

        dlg = wx.FileDialog(
                            self, message="Ouvrir un fichier de propriétés",
#                                defaultDir = self.DossierSauvegarde, 
                            defaultFile = "",
                            wildcard = mesFormats,
                            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
                            )

        if dlg.ShowModal() == wx.ID_OK:
            nomFichier = dlg.GetPath()#.decode(FILE_ENCODING)

        else:
            nomFichier = r''
        
        dlg.Destroy()
        if nomFichier != r'':
            self.GetDocument().ouvreProprietes(nomFichier)
            self.sendEvent(modif = "Modification des paramètres", 
                           draw = True, verif = True)
#         print("fin")
    
    
    #############################################################################
    def sauveProprietes(self, event = None):
        mesFormats = "xml (.xml)|*.xml"
        dlg = wx.FileDialog(self, 
                            message = "Enregistrement des propriétés de", 
                            defaultDir=toSystemEncoding(self.DossierSauvegarde) , # encodage?
                            defaultFile="", wildcard=mesFormats, 
                            style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT|wx.FD_CHANGE_DIR
                            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()#.decode(FILE_ENCODING)
            dlg.Destroy()
            self.GetDocument().sauveProprietes(path)
            return path
        else:
            dlg.Destroy()
        
    
    ###############################################################################################
    def enregistrer(self, nomFichier):
        """Enregistrement
            :param nomFichier: encodé en FileEncoding
        """
        wx.BeginBusyCursor()
        
        ok = self.GetDocument().enregistrer(nomFichier)

        if ok:
            self.definirNomFichierCourant(nomFichier)
            self.MarquerFichierCourantModifie(False)
            self.delFichierSauvegarde()
            
        wx.EndBusyCursor()
        return ok
    
    
    #############################################################################
    def delFichierSauvegarde(self):
        if self.fichierSauvegarde != "":
            try:
                os.remove(self.fichierSauvegarde)
                self.fichierSauvegarde = ""
            except:
                pass
    
    
    #############################################################################
    def miseAJourUndo(self):
        self.parent.miseAJourUndo()
        
        
    #############################################################################
    def commandeRedo(self, event = None):
        wx.BeginBusyCursor()
        doc = self.GetDocument()
        doc.undoStack.setOnUndoRedo()
#         doc.classe.undoStack.setOnUndoRedo()
        
        doc.undoStack.redo()
#         doc.classe.undoStack.redo()
        
        self.restaurer()
        
        doc.undoStack.resetOnUndoRedo()
#         doc.classe.undoStack.resetOnUndoRedo()
        
        wx.EndBusyCursor()
        
    #############################################################################
    def commandeUndo(self, event = None):
        wx.BeginBusyCursor()
        doc = self.GetDocument()
        doc.undoStack.setOnUndoRedo()
#         doc.classe.undoStack.setOnUndoRedo()

        doc.undoStack.undo()
#         doc.classe.undoStack.undo()
        
        self.restaurer()
        doc.undoStack.resetOnUndoRedo()
#         doc.classe.undoStack.resetOnUndoRedo()
        
        wx.EndBusyCursor()
    
    
    #############################################################################
    def autoSave(self, event):
#         print("autoSave")
        if self.fichierCourantModifie:
            wx.BeginBusyCursor()
            
            if self.fichierCourant != '':
                nf = self.fichierCourant+".bak"
            else:
                wx.EndBusyCursor()
                return
#                 nf = "tmp_"+str(uuid.uuid4())+".bak"
            
            if self.GetDocument().enregistrer(nf, dialog = False):
                self.fichierSauvegarde = nf
#                 print("   ", nf)
                
            wx.EndBusyCursor()
            
    
    #############################################################################
    def commandeEnregistrer(self, event = None):
        if self.fichierCourant != '':
            self.enregistrer(self.fichierCourant)
        else:
            self.dialogEnregistrer()        
            
            
    #############################################################################
    def commandeEnregistrerSous(self, event = None):
        return self.dialogEnregistrer()


    #############################################################################
    def SetTitre(self, modif = None):
#        print "SetTitre", modif
        if self.classe.typeEnseignement in REFERENTIELS:
            t = REFERENTIELS[self.classe.typeEnseignement].Enseignement[0]
        else:
            t = self.classe.GetReferentiel().Enseignement[0]

        if self.fichierCourant == '':
            t += " - "+constantes.TITRE_DEFAUT[self.typ]
        else:
            t += " - "+os.path.splitext(os.path.basename(toSystemEncoding(self.fichierCourant)))[0]
        
        if modif is None:
            modif = self.fichierCourantModifie
            
        if modif :
            t += " **"
        self.SetTitle(t)


    #############################################################################
    def exporterFichePDF(self, nomFichier, pourDossierValidation = False):
        """ Exporte la fiche au format PDF
            pourDossierValidation : concerne uniquement les Projets = pour anonymiser la fiche
        """
        # On passe par un fichier temporaire en ascii car cairo ne supporte pas (encore) utf-8
        tf = tempfile.mkstemp(suffix = ".pdf")#+".pdf"
        PDFsurface = cairo.PDFSurface(tf[1], 595, 842)#.decode(SYSTEM_ENCODING).encode(FILE_ENCODING)

        ctx = cairo.Context(PDFsurface)
        ctx.scale(820 / draw_cairo.COEF, 820/ draw_cairo.COEF) 
        if self.typ == 'seq':
#             draw_cairo_seq.Draw(ctx, self.sequence)
            draw_cairo_seq.Sequence(self.sequence).draw(ctx)
        elif self.typ == 'prj':
            draw_cairo_prj.Projet(self.projet, pourDossierValidation = pourDossierValidation).draw(ctx)
        elif self.typ == 'prg':
            draw_cairo_prg.Progression(self.progression).draw(ctx)
        
        ctx.stroke()
#         ctx.show_page()
        PDFsurface.finish()
#         PDFsurface.flush()
        
        try:
            shutil.copy(tf[1], nomFichier)
            os.close(tf[0])
            os.remove(tf[1])
        except IOError:
            Dialog_ErreurAccesFichier(nomFichier)
#             wx.EndBusyCursor()
            if DEBUG:
                raise
        
        
        
    #############################################################################
    def exporterFicheSVG(self, nomFichier, pourDossierValidation = False):
        """ Exporte la fiche au format PDF
        
            pourDossierValidation : concerne uniquement les Projet = pour anonymiser la fiche
        """

        # On passe par un fichier temporaire en ascii car cairo ne supporte pas (encore) utf-8
        tf = tempfile.mkstemp()[1]+".svg"
        SVGsurface = cairo.SVGSurface(tf, 707, 1000)
            
        ctx = cairo.Context(SVGsurface)
#         ctx.scale(820/ draw_cairo.COEF, 820/ draw_cairo.COEF) 
        ctx.scale(1.0, 1.0) 
        if self.typ == 'seq':
#             draw_cairo_seq.Draw(ctx, self.sequence, mouchard = True)
            draw_cairo_seq.Sequence(self.sequence, mouchard = True).draw(ctx)
        elif self.typ == 'prj':
            draw_cairo_prj.Projet(self.projet).draw(ctx)
        elif self.typ == 'prg':
            draw_cairo_prg.Progression(self.progression).draw(ctx)
             
        SVGsurface.finish()
   
        # et on reprend le nom de fichier unicode ...
        try:
            shutil.copy(tf, nomFichier)
            os.remove(tf)
        except IOError:
            Dialog_ErreurAccesFichier(nomFichier)
#             wx.EndBusyCursor()
            return
            
        self.enrichirSVG(nomFichier)
        
    
    #############################################################################
    def exporterFicheHTML(self, nomFichier, pourDossierValidation = False):
        """ Exporte la fiche au format PDF
        
            pourDossierValidation : concerne uniquement les Projet = pour anonymiser la fiche
        """
#         print('exporterFicheHTML')
        # On passe par un fichier temporaire en ascii car cairo ne supporte pas (encore) utf-8
        tf = tempfile.mkstemp()[1]+".svg"
        SVGsurface = cairo.SVGSurface(tf, 707, 1000)
            
        ctx = cairo.Context(SVGsurface)
#         ctx.scale(820/ draw_cairo.COEF, 820/ draw_cairo.COEF) 
        ctx.scale(1.0, 1.0) 
        if self.typ == 'seq':
#             draw_cairo_seq.Draw(ctx, self.sequence, mouchard = True)
            draw_cairo_seq.Sequence(self.sequence, mouchard = True).draw(ctx)
        elif self.typ == 'prj':
            draw_cairo_prj.Projet(self.projet).draw(ctx)
        elif self.typ == 'prg':
            draw_cairo_prg.Progression(self.progression).draw(ctx)
             
        SVGsurface.finish()
   
        # et on reprend le nom de fichier unicode ...
        try:
            shutil.copy(tf, nomFichier)
            os.remove(tf)
        except IOError: # normalement, ça ne peut pas arriver
            Dialog_ErreurAccesFichier(nomFichier)
#             wx.EndBusyCursor()
            return
            
        # à virer ou remplacer après ...
        self.enrichirHTML(nomFichier)
        
        
        
        
        
    
    #############################################################################
    def exporterFiche(self, event = None):
        mesFormats = "pdf (.pdf)|*.pdf|" \
                     "svg (.svg)|*.svg|" \
                     "html (.html)|*.html"
#                     "swf (.swf)|*.swf"
        dlg = wx.FileDialog(
            self, message="Enregistrer la fiche sous ...", 
            defaultDir=toSystemEncoding(self.DossierSauvegarde) , 
            defaultFile = os.path.splitext(self.fichierCourant)[0]+".pdf", 
            wildcard=mesFormats, style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT|wx.FD_CHANGE_DIR
            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()#.decode(FILE_ENCODING)
            ext = os.path.splitext(path)[1]
            dlg.Destroy()
            wx.BeginBusyCursor()
            if ext == ".pdf":
                self.exporterFichePDF(path)
                self.DossierSauvegarde = os.path.split(path)[0]
                os.startfile(path)
                
            elif ext == ".svg":
                self.exporterFicheSVG(path)
                self.DossierSauvegarde = os.path.split(path)[0]
                os.startfile(path)
                
            elif ext == ".html":
                self.exporterFicheHTML(path)
                self.DossierSauvegarde = os.path.split(path)[0]
                os.startfile(path)    
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
#         if hasattr(self, 'projet'):
#             for e in self.projet.eleves:
#                 win = FrameRapport(self, self.fichierCourant, self.projet, 'prj', e)
#                 win.Show()
        
        if hasattr(self, 'sequence'):
            win = FrameRapport(self, self.fichierCourant, self.sequence, 'seq')
            win.Show()
#            win.Destroy()


    #############################################################################
    def genererZip(self, event = None):
#         print("exporterZip")
        
        message = ""
        
        def ecrire(fct, *args, **kargs):
            message = dlg.GetMessage()
            message += os.path.split(args[0])[1]
            try:
                fct(*args, **kargs)
                message += "  ... OK\n"
                
            except:
                message += "  ... ERREUR\n"
                if DEBUG:
                    raise
                
            dlg.update(dlg.count+1, message)
            
        
        
        mesFormats = "zip (.zip)|*.zip"

        dlg = wx.FileDialog(
            self, message = "Enregistrer l'archive sous ...", 
            defaultDir=toSystemEncoding(self.DossierSauvegarde) , 
            defaultFile = os.path.splitext(self.fichierCourant)[0]+".zip", 
            wildcard=mesFormats, style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT|wx.FD_CHANGE_DIR
            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()#.decode(FILE_ENCODING)
            dlg.Destroy()
            
            dir, _ = os.path.splitext(path)
            if os.path.exists(dir):
                dlg = wx.MessageDialog(self, "Le dossier suivant existe déjà :\n\n%s\n\n"\
                                             "Si vous continuez, il sera effacé !\n\n"\
                                             "Voulez-vous continuer ?" %dir,
                                             "Dossier existant",
                                             wx.ICON_WARNING | wx.YES_NO
                                             )
                retCode = dlg.ShowModal()
                if retCode == wx.ID_NO:
                    return
            else:
                try:
                    os.mkdir(dir)
                except:
                    Dialog_ErreurAccesDossier(dir, dlg)
                    wx.EndBusyCursor()
                    if DEBUG:
                        raise
                    dlg.Destroy()
                    return
                     
            
            nomGen = os.path.join(dir, os.path.splitext(os.path.split(path)[1])[0])
#             print("  path :", path)
#             print("  dir :", dir)
#             print("  nomGen :", nomGen)
            
            wx.BeginBusyCursor()
            
            if self.typ == 'prj':
                maxCount = 4 + 2 * len(self.projet.eleves)
            else:
                maxCount = 3
            
            dlg = myProgressDialog("Création d'une archive",
                                   "Fichiers enregistrés dans l'archive :\n\n",
                                   maxCount,
                                   wx.GetTopLevelParent(self))
            dlg.Show()
            
            ecrire(self.exporterFichePDF, nomGen+".pdf")
            ecrire(self.exporterFicheSVG, nomGen+".svg")
            ecrire(self.exporterFicheHTML, nomGen+".html")
            
#             self.exporterFicheSVG(nomGen+".svg")
            
    
            ecrire(shutil.copy2,self.fichierCourant, dir)

            if self.typ == 'prj':
                dirGrilles = os.path.join(dir, "Grilles")
                try:
                    os.mkdir(dirGrilles)
                except FileExistsError:
                    pass
                for e in self.projet.eleves:
                    for g in list(e.grille.values()):
                        ng = g.GetAbsPath(dir)
                        if os.path.isfile(ng):
                            ecrire(shutil.copy2,ng, dirGrilles)
                
                ecrire(genpdf.genererDossierValidation,nomGen+"_Dossier_Validation.pdf", self.projet, self)
                
            try:
                shutil.make_archive(dir, 'zip', dir)
            except IOError:
                Dialog_ErreurAccesFichier(dir+'.zip', dlg)
                wx.EndBusyCursor()
                if DEBUG:
                    raise
                dlg.Destroy()
                return
            
            
            
            
            
            dlg.update(maxCount, dlg.GetMessage()+"Terminé !")
#             shutil.rmtree(dir)
                
            wx.EndBusyCursor()

        else:
            dlg.Destroy()
        return
        
        
    #############################################################################
    def genererGrilles(self, event = None):
        return
    
    #############################################################################
    def genererFicheValidation(self, event = None):
        return
    
    #############################################################################
    def quitter(self, event = None):
#         print("quitter")

        if self.fichierCourantModifie:
            texte = constantes.MESSAGE_FERMER[self.typ] % self.fichierCourant
#            if self.fichierCourant != '':
#                texte += "\n\n\t"+self.fichierCourant+"\n"
                
            dialog = wx.MessageDialog(self, texte, 
                                      "Confirmation", wx.YES_NO | wx.CANCEL | wx.ICON_WARNING)
            retCode = dialog.ShowModal()
            if retCode == wx.ID_YES:
#                 print("   YES")
                self.commandeEnregistrer()
                if event is not None: event.Skip()
                return self.fermer()
    
            elif retCode == wx.ID_NO:
#                 print("   NO")
                if event is not None: event.Skip()
                return self.fermer()
                 
            else:
                if event is not None: event.StopPropagation()
                return False
        
        else:            
            self.fermer()
            if event is not None: event.Skip()
            return True
            


    #############################################################################
    def enrichirSVG(self, path):
        """Enrichissement de l'image SVG <path> avec :
        - mise en surbrillance des éléments actifs
        - infobulles sur les éléments actifs
        - liens 
        - ...
        """
#         print("enrichirSVG :")
        epsilon = 1.5
        
        doc = parse(path)
        
        f = open(path, 'w', encoding = "utf-8")

        defs = doc.getElementsByTagName("defs")[0]
        defs.appendChild(getElementFiltre(constantes.FILTRE1))
        
        def match(p0, p1):
            return abs(p0[0]-p1[0])<epsilon and abs(p0[1]-p1[1])<epsilon
        
        # Récupération des points caractéristiques sur la fiche
        pts_caract = self.GetDocument().GetPtCaract()
#         print(pts_caract)
        
        # Identification des items correspondants sur le doc SVG
        for p in doc.getElementsByTagName("path"):
            a = p.getAttribute("d")
            a = str(a).translate(str.maketrans(dict.fromkeys('MCLZ')))  # Supprime les  lettres
            l = a.split()
            if len(l) > 1:      # On récupére le premier point du <path>
                x, y = l[0], l[1]
                x, y = float(x), float(y)
#                 print("   ", l)
                for pt, obj, flag in pts_caract:
                    if match((x, y), pt) :
#                         print("    ", l, pt)
                        obj.cadre.append((p, flag))
                        if type(flag) != str:
                            break
        
        # On lance la procédure d'enrichissement ...
        self.GetDocument().EnrichiSVGdoc(doc)
            
        doc.writexml(f, '   ', encoding = "utf-8")
        f.close()
        
        
    #############################################################################
    def enrichirHTML(self, nomFichierSVG):
        """Enrichissement de l'image SVG <path> avec :
        - mise en surbrillance des éléments actifs
        - infobulles sur les éléments actifs
        - liens 
        - ...
        """
#         print("enrichirHTML")
        epsilon = 1.5
        def match(p0, p1):
            return abs(p0[0]-p1[0])<epsilon and abs(p0[1]-p1[1])<epsilon
        
        
        
        f = open(os.path.join(util_path.TEMPLATE_PATH, "fiche.html"))
        soup = BeautifulSoup(f, "html5lib")
        f.close()
        
        f = open(os.path.join(util_path.PATH, "d3.min.js"))
        d3 = f.read()
        f.close()
        
        
        f = open(nomFichierSVG)
        svg = BeautifulSoup(f, "html5lib")#, 'xml')
        f.close()
        
#         titre = soup.find('title')
        soup.head.title.string = str(os.path.splitext(os.path.split(nomFichierSVG)[1])[0])
        soup.body.insert(0, svg.svg)
        
        script = soup.new_tag('script', type = "text/javascript")
        script.append(d3)
        soup.head.insert(2, script)
        
        
#         print(soup.body.svg)
        # Récupération des points caractéristiques sur la fiche
        pts_caract = self.GetDocument().GetPtCaract()
        # Identification des items correspondants sur le doc SVG
        for p in soup.body.svg.find_all("path"):
#             print("  ", p)
            a = p.get("d")
            a = str(a).translate(str.maketrans(dict.fromkeys('MCLZ')))  # Supprime les  lettres
            l = a.split()
            if len(l) > 1:      # On récupére le premier point du <path>
                x, y = l[0], l[1]
                x, y = float(x), float(y)
#                 print("   ", l[0], l[1])
                for pt, obj, flag in pts_caract:
                    if match((x, y), pt) :
#                         print("    ", l, obj, flag)
                        obj.cadre.append((p, flag, (x,y)))
                        if type(flag) != str:
                            break
        
#         print(">>", obj.cadre)
        
        # On lance la procédure d'enrichissement ...
        self.GetDocument().EnrichiHTMLdoc(soup)
        
        # Enregistrement du fichier HTML
        nomFichierHTML = os.path.splitext(nomFichierSVG)[0]+".html"
        with open(nomFichierHTML, "wb") as f:
            f.write(soup.prettify("utf-8"))
        
        return


    #############################################################################
    def definirNomFichierCourant(self, nomFichier = r''):
        """Modification du nom du fichier courant
            :param nomFichier: encodé en FileEncoding
        """
        self.fichierCourant = nomFichier
        self.GetDocument().SetPath(nomFichier)
        self.SetTitre()


    #############################################################################
    def MiseAJourTypeEnseignement(self):
        self.parent.MiseAJourToolBar()
        return

    #############################################################################
    def VerifierReferentiel(self, parent, nomFichier):
#         print("VerifierReferentiel", self.classe.GetReferentiel(), Referentiel.REFERENTIELS[self.classe.GetReferentiel().Code])
        ref = self.classe.GetReferentiel()
        e = False
        if ref.Code in REFERENTIELS:
            e = ref == REFERENTIELS[ref.Code]
        if not e:
#             print("   Différence !!!! (", self.classe.version ,"-", version.__version__, ")")
            dlg = DiffRefChoix(parent, nomFichier)
            val = dlg.ShowModal()
            dlg.Destroy()
            if val == 1:
                return 1
            elif val == 2:
                return 2
         
#             raise DiffReferentiel
               
               
    #############################################################################
    def TelechargerBO(self):
#         print("TelechargerBO")
        ref = self.GetDocument().GetReferentiel()
#         print(ref.Code)
        
        path = os.path.join(util_path.BO_PATH, ref.Code)
        if not os.path.exists(path):
            os.mkdir(path)
        
        l = []
        for tit, url in ref.BO_URL:
            if os.path.splitext(url)[1] == ".pdf":
                f, _ = urllib.request.urlretrieve(url, os.path.join(path, tit+".pdf"))
                l.append(os.path.basename(f))

        s = "\n"+CHAR_POINT
        lst = s.join(l)
        messageInfo(self, "Téléchargements terminés", 
                    "Les documents suivants ont été téléchargés\n"  + lst \
                    + "\n\nIls sont placés dans le dossier : %s" %path \
                    + "\n\net sont désormais consultables depuis l'onglet \"Bulletins Officiels\"")
  

 
def Dialog_ErreurAccesFichier(nomFichier, win = None):
    messageErreur(win, 'Erreur !',
                  "Impossible d'accéder en écriture au fichier\n\n%s" %toSystemEncoding(nomFichier))

def Dialog_ErreurAccesDossier(nomFichier, win = None):
    messageErreur(win, 'Erreur !',
                  "Impossible d'accéder en écriture au dossier\n\n%s" %toSystemEncoding(nomFichier))
    
    
########################################################################################
#
#
#  Classe définissant la fenétre "Séquence"
#
#
########################################################################################
class FenetreSequence(FenetreDocument):
    """Classe définissant la fenêtre d'une Séquence

    :param parent: Fenêtre parente
    :type parent: wx.Window
    :param ouverture: 
    :type ouverture: bool
    :param sequence: Séquence associée à la fenêtre
    :type sequence: pysequence.Sequence
    """
    
    def __init__(self, parent, ouverture = False, sequence = None):
        self.typ = 'seq'
        FenetreDocument.__init__(self, parent)
        self.Freeze() 
        
        if sequence is None:
            #
            # La classe
            #
            self.classe = pysequence.Classe(self, typedoc = self.typ)
        
            #
            # La séquence
            #
            self.sequence = pysequence.Sequence(self, self.classe, ouverture = ouverture)
            self.classe.SetDocument(self.sequence)
        
        else:
            self.sequence = sequence
            self.classe = self.sequence.classe
            self.sequence.app = self
        
        
        #
        # Arbre de structure de la séquence (à gauche)
        #
        arbre = ArbreSequence(self.pnl, self.sequence, self.classe, self.panelProp)
        self.arbre = arbre
        if sequence is None:
            self.arbre.SelectItem(self.classe.branche)
        self.sequence.SetDefautExpansion()
#         self.arbre.ExpandAll()
        
        #
        # Permet d'ajouter automatiquement les systèmes des préférences (dans la Classe)
        #
        self.sequence.Initialise()

        #
        # Zone graphique de la fiche de séquence (au centre)
        #
        self.fiche = FicheSequence(self.nb, self.sequence)
        self.nb.AddPage(self.fiche, "Fiche Séquence")
        
        #
        # Détails
        #
#         self.pageDetails = RapportRTF(self.nb, rt.RE_READONLY)
        self.pageDetails = RapportRTF(self.nb)
        self.nb.AddPage(self.pageDetails, "Détails des séances")
        
        #
        # Bulletins Officiels
        #
        self.pageBO = Panel_BO(self.nb)
        self.nb.AddPage(self.pageBO, "Bulletins Officiels")
        
        
        self.miseEnPlace()
        
        wx.CallAfter(self.Thaw)
        
#         self.fiche.Redessiner()

        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
        
        
            
            
        #
        # Mise en liste undo/redo
        #    
        self.sequence.undoStack.do("Nouvelle Séquence")
#             self.parent.miseAJourUndo()
            
        
            
#     ###############################################################################################
#     def ajouterOutils(self):
#         self.parent.supprimerOutils()
#         
#         self.parent.tb.InsertToolItem(5, self.parent.tool_ss)
#         self.parent.tb.InsertToolItem(6, self.parent.tool_sy)
# 
#         self.parent.tb.Realize()
    
        
        
    ###############################################################################################
    def GetDocument(self):
        return self.sequence
        
        
    ###############################################################################################
    def OnPageChanged(self, event):
#         print("OnPageChanged")
        new = event.GetSelection()
        event.Skip()
        if new == 1: # On vient de cliquer sur la page "détails"
            self.pageDetails.Remplir(self.fichierCourant, self.sequence, self.typ)
        
        elif new == 2: # On vient de cliquer sur la page "Bulletins Officiels"
            if self.sequence.classe.typeEnseignement in REFERENTIELS:
                self.pageBO.Construire(REFERENTIELS[self.sequence.classe.typeEnseignement])
            else:
                self.pageBO.Construire(self.sequence.GetReferentiel())
            
            
        elif new == 0: # On vient de cliquer sur la fiche
            self.fiche.Redessiner()
            
    ###############################################################################################
    def OnDocModified(self, event):
        """ La Séquence a été modifiée
        """
#         print("OnDocModified :", event.GetModif())
        
        # coupé pour accélération :
#         if event.GetModif() != "":
#             self.classe.undoStack.do(event.GetModif())
#             self.sequence.undoStack.do(event.GetModif())
        
#         if event.GetDocument() == self.sequence:
        if event.GetModif() != "":
            self.sequence.undoStack.do(event.GetModif())
            
        if event.GetVerif():
            self.sequence.VerifPb()
            
        if event.GetDraw():
            wx.CallAfter(self.fiche.Redessiner)
            
        self.MarquerFichierCourantModifie()
            
            
#         elif event.GetDocument() == self.classe:
#             if event.GetModif() != "":
#                 self.classe.undoStack.do(event.GetModif())
#             
#             if event.GetVerif():
#                 self.sequence.VerifPb()
#             if event.GetDraw():
#                 wx.CallAfter(self.fiche.Redessiner)
#             self.MarquerFichierCourantModifie()
        
#         self.parent.miseAJourUndo()
        
        
#     ###############################################################################################
#     def enregistrer(self, nomFichier):
#         """Enregistrement
#             :param nomFichier: encodé en FileEncoding
#         """
#         wx.BeginBusyCursor()
#         
#         ok = self.sequence.enregistrer(nomFichier)
# 
#         if ok:
#             self.definirNomFichierCourant(nomFichier)
#             self.MarquerFichierCourantModifie(False)
#         
#         wx.EndBusyCursor()
#         return ok
        
        
    ###############################################################################################
    def VerifierReparation(self):
        """Vérification (et correction) de la compatibilité de la séquence avec la classe
            aprés une ouverture avec réparation
        """
#        print "VerifierReparation", self.sequence.CI.numCI, self.sequence.GetReferentiel().CentresInterets
        for ci in self.sequence.CI.numCI:
            if ci >= len(self.sequence.GetReferentiel().CentresInterets):
                self.sequence.CI.numCI.remove(ci)
                messageErreur(self,"CI inexistant",
                              "Pas de CI numéro " + str(ci) + " !\n\n" \
                              "La séquence ouverte fait référence à un Centre d'Intérét\n" \
                              "qui n'existe pas dans le référentiel par défaut.\n\n" \
                              "Il a été supprimé !")
        return


    ###############################################################################################
    def restaurer(self):
        """Restaure l'arbre de construction
        et redessine la fiche
        (après undo ou redo)
        """
        
        self.sequence.MiseAJourTypeEnseignement()
#         t0 = time.time()
        
        #
        # Réinitialisation de l'arbre
        #
        self.arbre.DeleteAllItems()
        root = self.arbre.AddRoot("")
        
        self.classe.ConstruireArbre(self.arbre, root)
        
        self.sequence.ConstruireArbre(self.arbre, root)
        
        self.sequence.CI.SetNum()
        
        self.sequence.SetCodes()
        
        self.sequence.PubDescription()
        
        self.sequence.SetLiens()
        
        self.sequence.MiseAJourNomProfs()
        
        self.sequence.VerifPb()

        self.sequence.Verrouiller()

        wx.CallAfter(self.arbre.SelectItem, self.classe.branche)
#         self.arbre.SelectItem(self.classe.branche)

        self.arbre.Layout()
        self.sequence.SetDefautExpansion()
#         self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        
        self.fiche.Redessiner()

#         self.parent.miseAJourUndo()
        
        
    ###############################################################################################
    def finaliserOuverture(self, dlg = None, message = "", count = 0):
        self.arbre.DeleteAllItems()
        root = self.arbre.AddRoot("")
        
        liste_actions = [[self.classe.ConstruireArbre, [self.arbre, root], {},
                         "Construction de l'arborescence de la classe...\t"],
                         [self.sequence.ConstruireArbre, [self.arbre, root], {},
                          "Construction de l'arborescence de la séquence...\t"],
                         [self.sequence.CI.SetNum, [], {},
                          "Mise à jour des CI...\t"],
                         [self.sequence.SetCodes, [], {},
                          "Mise à jour diverses...\t"],
                         [self.sequence.PubDescription, [], {}, # à garder ???
                          "Traitement des descriptions...\t"],
                         [self.sequence.SetLiens, [], {},
                          "Construction des liens...\t"],
                         [self.sequence.VerifPb, [], {},
                          "Vérifications...\t"],
                         
                         ]
        
        for fct, arg, karg, msg in liste_actions:
            message += msg
            if dlg is not None:
                dlg.update(count, message)
            count += 1

            try :
                fct(*arg, **karg)
                message += "Ok\n"
            except:
#                     Ok = False
                message += constantes.Erreur(constantes.ERR_INCONNUE).getMessage() + "\n"
                if DEBUG:
                    raise
        
        self.sequence.Verrouiller()
        self.sequence.SetDefautExpansion()

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        wx.CallAfter(self.arbre.SelectItem, self.classe.branche)
        
        return message, count
    

        
    
        
        
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True, reparer = False):
        """Ouverture
            :param nomFichier: encodé en FileEncoding
        """
        print("ouvrir sequence", nomFichier)
#         tps1 = time.clock()
        Ok = True
        Annuler = False
        nbr_etapes = 10
        
        # Pour le suivi de l'ouverture
        message = nomCourt(nomFichier)+"\n\n"
        dlg = myProgressDialog("Ouverture d'une séquence",
                                   message,
                                   nbr_etapes,
                                   wx.GetTopLevelParent(self))
        dlg.Show()

        root = safeParse(nomFichier, wx.GetTopLevelParent(self))
        if root is None:
            dlg.Close()
            return None#, "", 0, False, True

        
        #################################################################################################
        def get_err_message(err):
            return ("\n  "+CHAR_POINT).join([e.getMessage() for e in err])
        
        ###############################################################################################################
        def ouvre(message):
            nonlocal reparer
            count = 1
            Ok = True
            Annuler = False

            # La séquence
            sequence = root.find("Sequence")
#             print("ouvre", sequence)
            if sequence == None: # Ancienne version , forcément STI2D-ETT !!
#                self.classe.GetPanelPropriete().EvtRadioBox(CodeFam = ('ET', 'STI'))
                self.sequence.setBranche(root)
            else:
                # La classe
                message += "Construction de la structure de la classe...\t"
                dlg.update(count, message)
#                dlg.top()
                count += 1
                classe = root.find("Classe")
                err = self.classe.setBranche(classe, reparer = reparer)
                if not reparer and int(self.classe.version.split(".")[0]) < 8:
                    raise OldVersion
                
                if self.VerifierReferentiel(dlg, "séquence") == 1:
                    reparer = True
                    self.classe.setBranche(classe, reparer = reparer)
                
                if len(err) > 0 :
                    Ok = False
                    message += get_err_message(err) 
                message += "\n"
                
                message += "Construction de la structure de la séquence...\t"
                dlg.update(count, message)
                count += 1
                
                err = self.sequence.setBranche(sequence, reparer = reparer)
                if len(err) > 0 :
                    Ok = False
                    message += get_err_message(err)
                message += "\n"
                
                self.sequence.MiseAJourTypeEnseignement()
            
            # Les propriétés
#             print("   proprietes4", self.sequence.proprietes.proprietes)
            prop = root.find("ProprietesDoc")
            if prop is not None:
                self.sequence.proprietes.setBranche(prop)
                
            
                
#             print("   proprietes5", self.sequence.proprietes.categories)    
            # Chargement des paramètres depuis les propriétes de la séquence
            self.sequence.GetApp().fiche.fiche.chargerParametres()
#             print("   proprietes6", self.sequence.proprietes.categories)
            
            
            
            
            return root, message, count, Ok, Annuler


        #################################################################################################
        def annuleTout(message):
            message += "\n\nLa séquence n'a pas pu être ouverte !\n\n"
            if len(err) > 0:
                message += "\n   L'erreur concerne :"
                message += get_err_message(err)
                
            self.fermer()
            count = nbr_etapes
            dlg.update(count, message)
            dlg.Close()
            return
        
        
        ###############################################################################################################
        ###############################################################################################################
        
        err = []
        try:
            root, message, count, Ok, Annuler = ouvre(message)
        except OldVersion:
            messageWarning(dlg, "Ancienne version",
               "La séquence pédagogique\n    %s\n a été créée avec une version ancienne de pySéquence !\n" \
               "Elle va être automatiquement convertie au format actuel." %nomCourt(nomFichier))
            reparer = True
            root, message, count, Ok, Annuler = ouvre(message)
            
        except:
            messageErreur(dlg, "Erreur d'ouverture",
                          "La séquence pédagogique\n    %s\n n'a pas pu étre ouverte !\n" \
                          "Essayez de faire Outils/Ouvrir et réparer." %nomCourt(nomFichier))
#             self.Close()
            count = 0
            err = [constantes.Erreur(constantes.ERR_INCONNUE)]
            message += err[0].getMessage() + "\n"
            Annuler = True
            
            if DEBUG:
                raise
#             return
        
        if reparer:
            self.MarquerFichierCourantModifie(True)
            self.VerifierReparation()
            
        #
        # Erreur fatale d'ouverture
        #
        if Annuler:
            annuleTout(message)
            return
        
        #
        # Finalisation
        #
        try:
            message, count = self.finaliserOuverture(dlg= dlg, message = message, count = count)
        except:
            annuleTout(message)
            if DEBUG:raise
            return
        
        
        message += "Tracé de la fiche...\t"
        dlg.update(count, message)
#        dlg.top()
        count += 1

#         tps2 = time.clock() 
#         print("Ouverture :", tps2 - tps1)

        if Ok:
            dlg.Destroy()
        else:
            dlg.update(nbr_etapes, message)
            dlg.Close() 
            
            
        #
        # Mise en liste undo/redo
        #    
#         self.classe.undoStack.do("Ouverture de la Classe")
        self.sequence.undoStack.do("Ouverture de la Séquence")
#         self.parent.miseAJourUndo()
        
        self.definirNomFichierCourant(nomFichier)
        
        return self.sequence
        

    #############################################################################
    def definirNomFichierCourant(self, nomFichier = r''):
        """Modification du nom du fichier courant
            :param nomFichier: encodé en FileEncoding
        """
        self.fichierCourant = nomFichier
        self.sequence.SetPath(nomFichier)
        self.SetTitre()

    
    #############################################################################
    def AppliquerOptions(self):
        self.sequence.AppliquerOptions()   
    


########################################################################################
#
#
#  Classe définissant la fenêtre d'un Projet
#
#
########################################################################################
class FenetreProjet(FenetreDocument):
    """
    Classe définissant la fenêtre d'un Projet

    :param parent: Fenêtre parente
    :type parent: wx.Window
    :param projet: Projet associé à la fenêtre
    :type projet: pysequence.Projet
    """
    
    def __init__(self, parent, ouverture = False, projet = None):
        self.typ = 'prj'
#        print "__init__ FenetreProjet"
        FenetreDocument.__init__(self, parent)
        
        self.Freeze() 
        
        if projet is None:
            #
            # La classe
            #
            self.classe = pysequence.Classe(self, pourProjet = True, typedoc = self.typ)
        
            #
            # Le projet
            #
            self.projet = pysequence.Projet(self, self.classe)
            self.classe.SetDocument(self.projet)
#             print("___-111", self.projet.code)   
            self.projet.MiseAJourTypeEnseignement()
#             print("___-11", self.projet.code)   
        
        else:
            self.projet = projet
            self.classe = self.projet.classe
            self.projet.app = self
        
        

#        self.projet.MiseAJourTypeEnseignement()
        
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
        self.nb.AddPage(self.fiche, "Fiche Projet")
        
        #
        # Détails
        #
#         self.pageDetails = RapportRTF(self.nb, rt.RE_READONLY)
        self.pageDetails = Panel_Details(self.nb)
        self.nb.AddPage(self.pageDetails, "Tâches %s détaillées" %self.projet.GetReferentiel().getLabel("ELEVES").plur_())
        
        #
        # Dossier de validation
        #
        self.pageValid = genpdf.PdfPanel(self.nb)
#         self.pageValid.MiseAJour(self.projet, self)
        self.nb.AddPage(self.pageValid, "Dossier de validation")
        
        #
        # Bulletins Officiels
        #
        self.pageBO = Panel_BO(self.nb)
        self.nb.AddPage(self.pageBO, "Bulletins Officiels")
        
        
        self.miseEnPlace()
#         print "__init__ FenetreProjet"
#         self.fiche.Redessiner() #!!!
        
        wx.CallAfter(self.Thaw)
        wx.CallAfter(self.MiseAJourTypeEnseignement)
        
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        
        
        
        if not ouverture:
            #
            # Mise en liste undo/redo
            #    
#             self.classe.undoStack.do("Nouvelle Classe")
            self.projet.undoStack.do("Nouveau Projet")
#             self.parent.miseAJourUndo()
            
    #############################################################################
    def CleanClose(self):
        """ Tout ce qu'il faut faire pour que le document se ferme proprement ...
        """
        print("CleanClose")
        self.pageValid.PreClose()


    ###############################################################################################
    def ajouterOutils(self):
        """Ajoute à la toolbar les outils spécifiques aux Projets
        """
        self.parent.supprimerOutils()

        self.parent.tb.InsertToolItem(5, self.parent.tool_pe)
        self.parent.tb.InsertToolItem(6, self.parent.tool_pp)
        self.parent.tb.InsertToolItem(7, self.parent.tool_pt)
        self.parent.tb.InsertToolItem(7, self.parent.tool_pr)
        self.parent.tb.Realize()
        
        
    ###############################################################################################
    def GetDocument(self):
        
        return self.projet
    
    ###############################################################################################
    def AjouterTache(self, event = None):
        self.arbre.AjouterTache()
        
    ###############################################################################################
    def OnPageChanging(self, event):
        old = event.GetSelection()
        event.Skip()
        
        if old == 2: # On vient de cliquer sur la page "dossier de validation"
            self.pageValid.supprimerDossierTemp()
            
    ###############################################################################################
    def OnPageChanged(self, event):
#         print "OnPageChanged"
        new = event.GetSelection()
        event.Skip()
        if new == 1: # On vient de cliquer sur la page "détails"
            self.pageDetails.Construire(self.fichierCourant, self.projet, self.typ)
        
        elif new == 2: # On vient de cliquer sur la page "dossier de validation"
            self.pageValid.MiseAJour(self.projet, self)
            
        elif new == 3: # On vient de cliquer sur la page "Bulletins Officiels"
            if self.projet.classe.typeEnseignement in REFERENTIELS:
                self.pageBO.Construire(REFERENTIELS[self.projet.classe.typeEnseignement])
            else:
                self.pageBO.Construire(self.projet.GetReferentiel())

        elif new == 0: # On vient de cliquer sur la fiche
            self.fiche.Redessiner()
            
            
    ###############################################################################################
    def OnDocModified(self, event):
        """ Le Projet a été modifié ...
        """
#         print("OnDocModified Projet", event.GetModif(), event.GetVerif())
        
        if event.GetModif() != "":
#             print "OnDocModified", event.GetModif()
#             self.classe.undoStack.do(event.GetModif())
            self.projet.undoStack.do(event.GetModif())
            
        if event.GetDocument() == self.projet:
            if event.GetVerif():
                self.projet.VerifPb()
            
            self.projet.SetCompetencesRevuesSoutenance(miseAJourPanel = False)
            
            if event.GetDraw():
                wx.CallAfter(self.fiche.Redessiner)

            self.MarquerFichierCourantModifie()
        
        elif event.GetDocument() == self.classe:
            self.MarquerFichierCourantModifie()
            
#         self.parent.miseAJourUndo()
        
        
#     ###############################################################################################
#     def enregistrer(self, nomFichier):
#         """Enregistrement
#             :param nomFichier: encodé en FileEncoding
#         """
#         wx.BeginBusyCursor()
#         
#         ok = self.projet.enregistrer(nomFichier)
#         
#         if ok:
#             self.definirNomFichierCourant(nomFichier)
#             self.MarquerFichierCourantModifie(False)
#             
#         wx.EndBusyCursor()
#         return ok
        
        
    ###############################################################################################
    def restaurer(self):
        """ Restaure l'arbre de construction
            et redessine la fiche
            (après undo ou redo)
        """

        #
        # Réinitialisation de l'arbre
        #
        self.arbre.DeleteAllItems()
        root = self.arbre.AddRoot("")

        self.projet.SetCompetencesRevuesSoutenance()

        self.classe.ConstruireArbre(self.arbre, root)

        self.projet.ConstruireArbre(self.arbre, root)

        self.projet.OrdonnerTaches()

#         self.projet.PubDescription()
  
        self.projet.MiseAJourDureeEleves()

        self.projet.MiseAJourNomProfs()

        self.projet.Verrouiller()
        
        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        wx.CallAfter(self.arbre.SelectItem, self.classe.branche)
        
#        self.fiche.Redessiner()

#         self.parent.miseAJourUndo()

    
    ###############################################################################################
    def finaliserOuverture(self, dlg = None, message = "", count = 0):
        self.arbre.DeleteAllItems()
        root = self.arbre.AddRoot("")
        
        
        liste_actions = [[self.classe.ConstruireArbre, [self.arbre, root], {},
                         "Construction de l'arborescence de la classe...\t"],
                         [self.projet.ConstruireArbre, [self.arbre, root], {},
                          "Construction de l'arborescence du projet...\t"],
                         [self.projet.OrdonnerTaches, [], {},
                          "Ordonnancement des tâches...\t"],
                         [self.projet.MiseAJour, [], {},
                          "Mise à jour diverses...\t"],
#                         [self.projet.PubDescription, [], {},
#                          u"Traitement des descriptions...\t"],
                         [self.projet.SetLiens, [], {},
                          "Construction des liens...\t"],
                         [self.projet.MiseAJourDureeEleves, [], {},
                          "Ajout des durées/évaluabilités dans l'arbre...\t"],
                         [self.projet.MiseAJourNomProfs, [], {},
                          "Ajout des disciplines dans l'arbre...\t"],
                         ]
        
        for fct, arg, karg, msg in liste_actions:
            message += msg
            if dlg is not None:
                dlg.update(count, message)
            count += 1

            try :
                fct(*arg, **karg)
                message += "Ok\n"
            except:
#                     Ok = False
                message += constantes.Erreur(constantes.ERR_INCONNUE).getMessage() + "\n"
                if DEBUG:
                    raise
#             print("tachesi", self.projet.taches)
            
            
        self.projet.Verrouiller()
        self.projet.VerifierVersionGrilles()

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        wx.CallAfter(self.arbre.SelectItem, self.classe.branche)
#         self.arbre.SelectItem(self.arbre.classe.branche)
        
        return message, count
    
    
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True, reparer = False):
        """Ouverture
            :param nomFichier: encodé en FileEncoding
        """
        print("Ouverture projet", nomFichier)
#         tps1 = time.clock()
        Ok = True
        Annuler = False
        nbr_etapes = 10
        
        # Pour le suivi de l'ouverture
        message = nomCourt(nomFichier)+"\n\n"
        dlg = myProgressDialog("Ouverture d'un projet",
                                   message,
                                   nbr_etapes,
                                   wx.GetTopLevelParent(self))
        dlg.Show()

#         self.fiche.Hide()
        root = safeParse(nomFichier, dlg)
        if root is None:
            dlg.Close()
            return None#, "", 0, False, True
        

            
        
        #################################################################################################
        def get_err_message(err):
            return ("\n  "+CHAR_POINT).join([e.getMessage() for e in err])
        
        
        #################################################################################################
        def ouvre(message):
            nonlocal reparer
            count = 1
            Ok = True
            Annuler = False
                   
            # Le projet
            projet = root.find("Projet")
            if projet == None:
                self.projet.setBranche(root)
            else:
                # La classe
                message += "Construction de la structure de la classe...\t"
                dlg.update(count, message)
#                dlg.top()
                count += 1
                classe = root.find("Classe")
                err = self.classe.setBranche(classe, reparer = reparer)
                if not reparer and int(self.classe.version.split(".")[0]) < 8:
                    raise OldVersion
                
                if self.VerifierReferentiel(dlg, "projet") == 1:
#                     print("Remplacer ref")
                    reparer = True
                    self.classe.setBranche(classe, reparer = reparer)
                
                if len(err)  > 0 :
                    Ok = False
                    message += get_err_message(err) 
                message += "\n"
                
#                print "V",self.classe.GetVersionNum()
                if self.classe.GetVersionNum() < 5:
                    messageInfo(dlg, "Ancien programme", 
                                  "Projet enregistré avec les indicateurs de compétence antérieurs à la session 2014\n\n"\
                                  "Les indicateurs de compétence ne seront pas chargés.")
                    
                # Le projet
                message += "Construction de la structure du projet...\t"
                dlg.update(count, message)
                count += 1
#                 print("___-2", self.projet.code) 
                self.projet.code = self.projet.GetReferentiel().getCodeProjetDefaut()
#                 print("___-1", self.projet.code) 
                # Derniére vérification
                if self.projet.GetProjetRef() == None:
                    print("Pas bon référentiel")
                    self.classe.setBranche(classe, reparer = True)
                
#                 print("taches1", self.projet.taches)
                
                # Correction du bug des CO7.ee3 et 4 manquante pour les Projets enregistrés avant v7.1.12
                if version.sup("7.1.12", self.classe.GetVersion().split('.')):
                    if self.classe.GetReferentiel().Code == "EE":
                        print("Correction bug des CO7.eex", self.classe.GetVersion(), ">>", version.__version__)
#                         print self.projet.GetProjetRef()._dicoCompetences['S']['O7'].sousComp.items()
                        self.projet.GetProjetRef().normaliserPoidsComp(self.projet.GetProjetRef()._dicoCompetences['S']['O7'], reset = True)
#                         print self.projet.GetProjetRef()._dicoCompetences['S']['O7'].sousComp.items()
#                 print("setBranche ...")
                err = self.projet.setBranche(projet)
#                 print("taches2", self.projet.taches)
                if len(err) > 0 :
                    Ok = False
                    message += get_err_message(err)
                message += "\n"
                          
            # Les propriétés
            prop = root.find("ProprietesDoc")
            if prop is not None:
                self.projet.proprietes.setBranche(prop)
            
            return root, message, count, Ok, Annuler
        
        
        #################################################################################################
        def annuleTout(message):
            message += "\n\nLe projet n'a pas pu être ouvert !\n\n"
            if len(err) > 0:
                message += "\n   L'erreur concerne :"
                message += get_err_message(err)
                
            self.fermer()
            count = nbr_etapes
#            dlg.UpdateWindowUI()
##            wx.GetTopLevelParent(self).SetFocus()
#            dlg.top()
            dlg.update(count, message)
            
        
        
        ################################################################################################
        err = []
        try:
            root, message, count, Ok, Annuler = ouvre(message)
            
        except OldVersion:
            messageWarning(dlg, "Ancienne version",
                               "Le projet\n    %s\n a été créé avec une version ancienne de pySéquence !\n" \
                               "Il va être automatiquement converti au format actuel." %nomCourt(nomFichier))
            reparer = True
            root, message, count, Ok, Annuler = ouvre(message)
            
        except:
            count = 0
            err = [constantes.Erreur(constantes.ERR_INCONNUE)]
            message += err[0].getMessage() + "\n"
            Annuler = True
            if DEBUG:
                raise
        
        if reparer:
            self.MarquerFichierCourantModifie(True)
            
            
        #
        # Erreur fatale d'ouverture
        #
        if Annuler:
            annuleTout(message)
            return
        
        #
        # Finalisation
        #
#         print("finalisation", self.projet.taches)
        try:
            message, count = self.finaliserOuverture(dlg= dlg, message = message, count = count)
        except:
            annuleTout(message)
            if DEBUG:raise
            return
            

#        self.projet.Verrouiller()

        message += "Tracé de la fiche...\t"
        dlg.update(count, message)
#        dlg.top()
        count += 1
    
        #
        # Vérification de la version des grilles
        #
#        self.projet.VerifierVersionGrilles()
        
#         tps2 = time.clock() 
#         print("Ouverture :", tps2 - tps1)

#         self.fiche.Redessiner() #!!!

        if Ok:
            dlg.Destroy()
        else:
            dlg.update(nbr_etapes, message)
            dlg.Close() 
        

        #
        # Mise en liste undo/redo
        #
#         self.classe.undoStack.do("Ouverture de la Classe")
        self.projet.undoStack.do("Ouverture du Projet")
#         self.parent.miseAJourUndo()
        
        self.definirNomFichierCourant(nomFichier)
        
        return self.projet

    #############################################################################
    def exporterDetails(self, event = None):
        """ Génération de toutes les fichier des tâches élève
             - demande d'un dossier -

            :return: la liste des codes d'erreur
            :rtype: list
        """

        log = []
        
        dlg = wx.DirDialog(self, message = "Emplacement des fichiers", 
                           defaultPath = "",
                            style=wx.DD_DEFAULT_STYLE|wx.DD_CHANGE_DIR
                            )
#        dlg.SetFilterIndex(0)

        if dlg.ShowModal() == wx.ID_OK:
            dirpath = dlg.GetPath()
            dlg.Destroy()
            
            message = "Génération des fichiers de détails des tâches\n\n"
            dlgb = myProgressDialog   ("Génération des fichiers de détail des tâches",
                                        message,
                                        maximum = len(self.projet.eleves) + 1,
                                        parent = wx.GetTopLevelParent(self),
                                        style = 0
                                        | wx.PD_APP_MODAL
                                        | wx.PD_CAN_ABORT
                                        #| wx.PD_CAN_SKIP
                                        #| wx.PD_ELAPSED_TIME
    #                                    | wx.PD_ESTIMATED_TIME
    #                                    | wx.PD_REMAINING_TIME
                                        #| wx.PD_AUTO_HIDE
                                        )

            dlgb.Show()
            count = 0
            message += "Vérification des noms de fichier\n"
            dlgb.update(count, message)
                
            nomFichiers = {}
            for e in self.projet.eleves:
                nomFichiers[e.id] = e.GetNomDetails(dirpath)
#            print "nomFichiers", nomFichiers
            
            if not self.projet.TesterExistanceDetails(nomFichiers, dirpath, dlgb):
                dlgb.Destroy()
                return
            
            
            count += 1
            message += "Traitement du fichier de :\n"
            
            for e in self.projet.eleves:
                message += "  "+e.GetNomPrenom()+"\n"
                dlgb.update(count, message)
                win = FrameRapport(self, self.fichierCourant, self.projet, 'prj', e, hide = True)
                win.rtc.Enregistrer("", dialog = False)
                win.Close()
                count += 1

           
            t = "Génération des fichiers de description détaillée des tâches terminée "
            if len(log) == 0:
                t += "avec succès !\n\n"
            else:
                t += "avec des erreurs :\n\n"
                t += "\n".join(log)
            
            t += "Dossier des fichiers :\n  " + dirpath
            message += t
            dlgb.update(count, message)
#             dlgb.Destroy() 
                
                
        else:
            dlg.Destroy()
        
        return list(set(log))
    
    
    
    
                
    #############################################################################
    def genererGrilles(self, event = None):
        """ Génération de toutes les grilles d'évaluation
             - demande d'un dossier -

            :return: la liste des codes d'erreur
            :rtype: list
        """
#         print("genererGrilles")
        log = []
        
        dlg = wx.DirDialog(self, message = "Emplacement des grilles", 
                           defaultPath = "",
                            style=wx.DD_DEFAULT_STYLE|wx.DD_CHANGE_DIR
                            )
#        dlg.SetFilterIndex(0)

        if dlg.ShowModal() == wx.ID_OK:
            dirpath = dlg.GetPath()
            dlg.Destroy()
            
            message = "Génération des grilles d'évaluation\n\n"
            
            dlgb = myProgressDialog   ("Génération des grilles",
                                        message,
                                        maximum = len(self.projet.eleves) + 1,
                                        parent = wx.GetTopLevelParent(self),
                                        style = 0
                                        | wx.PD_APP_MODAL
                                        | wx.PD_CAN_ABORT
                                        #| wx.PD_CAN_SKIP
                                        #| wx.PD_ELAPSED_TIME
    #                                    | wx.PD_ESTIMATED_TIME
    #                                    | wx.PD_REMAINING_TIME
                                        #| wx.PD_AUTO_HIDE
                                        )

            dlgb.Show()
            count = 0
            message += "Vérification des noms de fichier\n"
            dlgb.update(count, message)
            
                
            nomFichiers = {}
            for e in self.projet.eleves:
                nomFichiers[e.id] = e.GetNomGrilles(dirpath, win = dlgb)
                if nomFichiers[e.id] is None:
                    dlgb.Destroy()
                    return ["Opération annulée"]
#             print("nomFichiers", nomFichiers)
            
            
            if not self.projet.TesterExistanceGrilles(nomFichiers, dirpath, dlgb):
                dlgb.Destroy()
                return []
            count += 1
            message += "Traitement de la grille de :\n"
            
            for e in self.projet.eleves:
                message += "  "+e.GetNomPrenom()+"\n"
                dlgb.update(count, message)
                log.extend(e.GenererGrille(nomFichiers = nomFichiers[e.id], 
                                           messageFin = False, win = dlgb))
                
#                 dlgb.Refresh()
                count += 1
#                 dlgb.Refresh()
           
            t = "Génération des grilles terminée "
            if len(log) == 0:
                t += "avec succès !\n\n"
            else:
                t += "avec des erreurs :\n\n"
                t += "\n".join(log)
            
            t += "Dossier des grilles :\n  " + dirpath
            message += t
            dlgb.update(count, message)
#             dlgb.Destroy() 
                
                
        else:
            dlg.Destroy()
        
        return list(set(log))
    
    
            
    #############################################################################
    def genererGrillesPdf(self, event = None):
        """ Génération de TOUTES les grilles d'évaluation au format pdf
            demande d'un nom de fichier -
        """
        mesFormats = "PDF (.pdf)|*.pdf"
        nomFichier = getNomFichier("Grilles", self.projet.intitule[:20], ".pdf")
        dlg = wx.FileDialog(self, "Enregistrer les grilles d'évaluation",
                            defaultFile = nomFichier,
                            wildcard = mesFormats,
#                           defaultPath = globdef.DOSSIER_EXEMPLES,
                            style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT|wx.FD_CHANGE_DIR
                            #| wx.DD_DIR_MUST_EXIST
                            #| wx.DD_CHANGE_DIR
                            )

        if dlg.ShowModal() == wx.ID_OK:
            nomFichier = dlg.GetPath()#.decode(FILE_ENCODING)
            dlg.Destroy()
            
            message = "Génération des grilles d'évaluation en PDF\n\n"
            dlgb = myProgressDialog("Génération des grilles",
                                        message,
                                        maximum = len(self.projet.eleves)+1,
                                        parent = wx.GetTopLevelParent(self)
#                                         style = 0
#                                         | wx.PD_APP_MODAL
#                                         | wx.PD_CAN_ABORT
#                                         | wx.STAY_ON_TOP
                                        #| wx.PD_CAN_SKIP
                                        #| wx.PD_ELAPSED_TIME
    #                                    | wx.PD_ESTIMATED_TIME
    #                                    | wx.PD_REMAINING_TIME
                                        #| wx.PD_AUTO_HIDE
                                        )
            
            dlgb.Show()
            count = 1
            
            pathprj = self.projet.GetPath()
#            print "pathprj", pathprj
            dirpath = os.path.split(nomFichier)[0]
            #
            # Détermination des fichiers grille à créer
            #
            nomFichiers = {}
            for e in self.projet.eleves:
                if len(e.grille) == 0: # Pas de fichier grille connu pour cet élève
                    nomFichiers[e.id] = e.GetNomGrilles(dirpath)
                    if nomFichiers[e.id] is None:
                        dlgb.Destroy()
                        return ["Opération annulée"]
                else:
                    for g in e.grille.values():
                        if not os.path.exists(g.path): # Le fichier grille pour cet élève n'a pas été trouvé
                            nomFichiers[e.id] = e.GetNomGrilles(dirpath)
                            if nomFichiers[e.id] is None:
                                dlgb.Destroy()
                                return ["Opération annulée"]
#            print "nomFichiers grille", nomFichiers
            
            # Si des fichiers existent avec le méme nom, on demande si on peut les écraser
            if not self.projet.TesterExistanceGrilles(nomFichiers, dirpath, dlgb):
                dlgb.Destroy()
                return
            
#            dlgb.top()
            
            
#            dicInfo = self.projet.GetProjetRef().cellulesInfo
#            classNON = dicInfo["NON"][0][0]
#            feuilNON = dicInfo["NON"][0][1]
#            collectif = self.projet.GetProjetRef().grilles[classNON][1] == 'C'
            
            # Elaboration de la liste des fichiers/feuilles à exporter en PDF
            lst_grilles = []
            message += "Traitement de la grille de :\n"
            for e in self.projet.eleves:
                message += "  "+e.GetNomPrenom()+"\n"
                dlgb.update(count, message)
#                dlgb.top()
#                 dlgb.Refresh()
                    
                if e.id in nomFichiers:
                    e.GenererGrille(nomFichiers = nomFichiers[e.id], 
                                    messageFin = False, win = dlgb)

                for k, g in e.grille.items():
#                     print(">>>", g, g.ok)
#                    grille = os.path.join(toFileEncoding(pathprj), toFileEncoding(g.path))
#                     grille = os.path.join(pathprj, g.path)
                    if g.ok:
                        grille = g.GetAbsPath(pathprj)
                        if k in self.projet.GetReferentiel().aColNon:
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
#                 dlgb.Refresh()
            
            if len(lst_grilles) > 0:
                message += "Compilation des grilles ...\n\n"
                dlgb.update(count, message)
    #            dlgb.top()
    #             count += 1
    #             dlgb.Refresh()
                    
                ok = genpdf.genererGrillePDF(nomFichier, lst_grilles)
                
                if ok:
                    message += "Les grilles ont été créées avec succés dans le fichier :\n\n"+nomFichier
                    dlgb.update(count, message)
        #            dlgb.top()
                    try:
                        os.startfile(nomFichier)
                    except:
                        pass
            else:
                message += "Aucune grille n'a pu être générée !\n\n"
                dlgb.update(count, message)
#             dlgb.Destroy()
                
                
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
#         print("genererFicheValidation")
        mesFormats = "PDF (.pdf)|*.pdf"
        ref = self.projet.GetReferentiel()
        t = ref.getLabel("PRJVAL").Sing_()
        nomFichier = getNomFichier(t, self.projet.intitule[:20], ".pdf")
        
        dlg = wx.FileDialog(self, "Enregistrer %s" %ref.getLabel("PRJVAL").le_(),
                            defaultFile = nomFichier,
                            wildcard = mesFormats,
#                           defaultPath = globdef.DOSSIER_EXEMPLES,
                            style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT|wx.FD_CHANGE_DIR
                            #| wx.DD_DIR_MUST_EXIST
                            #| wx.DD_CHANGE_DIR
                            )
        
        
        
#        dlg = wx.DirDialog(self, message = u"Emplacement de la fiche", 
#                            style=wx.DD_DEFAULT_STYLE|wx.CHANGE_DIR
#                            )
#        dlg.SetFilterIndex(0)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()#.decode(FILE_ENCODING)
            dlg.Destroy()
            nomFichier = path
#            nomFichier = getNomFichier("FicheValidation", self.projet)
#            nomFichier = os.path.join(path, nomFichier)
#             print(nomFichier)
            err = genpdf.genererDossierValidation(nomFichier, self.projet, self)
            if len(err) > 0:
                ref = self.projet.GetReferentiel()
                m = "\n - ".join(err)
                messageErreur(self, "Erreur !",
                                  "Impossible de générer %s :\n\n" %ref.getLabel("PRJVAL").le_() +m
                                  )
                return
            
            try:
                os.startfile(nomFichier)
            except (IOError, RuntimeError):
                messageErreur(self, "Erreur !",
                                  "Impossible d'enregistrer le fichier suivant :\n\n%s\n\nVérifier :\n" \
                                  " - qu'aucun fichier portant le méme nom n'est déjà ouvert\n" \
                                  " - que le dossier choisi n'est pas protégé en écriture\n\n" %nomFichier)
                try:
                    wx.EndBusyCursor()
                except:
                    pass
            
#            for t, f in tf:
#                try:
#                    t.save(os.path.join(path, f))
#                except:
#                    messageErreur(self, u"Erreur !",
#                                  u"Impossible d'enregistrer le fichier.\n\nVérifier :\n" \
#                                  u" - qu'aucun fichier portant le méme nom n'est déja ouvert\n" \
#                                  u" - que le dossier choisi n'est pas protégé en écriture")
#                t.close()
#            
#            dlgb.Update(count, u"Toutes les grilles ont été créées avec succés dans le dossier :\n\n"+path)
#            dlgb.Destroy() 
#                
                
        else:
            dlg.Destroy()
            
            
    
    
    #############################################################################
    def AppliquerOptions(self):
        self.projet.AppliquerOptions() 
        
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):
#         print("MiseAJourTypeEnseignement", self.projet.GetReferentiel().getLabel("PRJVAL").Sing_())
        self.nb.SetPageText(1, "Tâches %s détaillées" %self.projet.GetReferentiel().getLabel("ELEVES").plur_())
        self.nb.SetPageText(2, self.projet.GetReferentiel().getLabel("PRJVAL").Sing_())
        
        self.parent.OnDocChanged()



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


# class ThreadDraw(threading.Thread):
#     def __init__(self):
#         super(ThreadDraw, self).__init__()
#         self._stop_event = threading.Event()
#         self.ctx = None
#         self.doc = None
# 
#     def set_param(self,  ctx, doc):
#         self.ctx = ctx
#         self.doc = doc
#         
#     def stop(self):
#         self._stop_event.set()
# 
#     def stopped(self):
#         return self._stop_event.is_set()
#         
#     def run(self):
#         if self.doc is not None:
#             self.doc.DefinirCouleurs()
#             self.doc.draw.Draw(self.ctx, self.doc)
        
# threadDraw = ThreadDraw()

########################################################################################
#
#
#  Classe définissant la fenétre "Séquence"
#
#
########################################################################################
class FenetreProgression(FenetreDocument):
    """
    Classe définissant la fenêtre d'une Progression

    :param parent: Fenêtre parente
    :type parent: wx.Window
    """
    def __init__(self, parent, ouverture = False):
        self.typ = 'prg'
#        print "__init__ FenetreProjet"
        FenetreDocument.__init__(self, parent)
        
        self.Freeze()
        
        #
        # La classe
        #
        self.classe = pysequence.Classe(self, pourProjet = True, typedoc = self.typ)
        
        #
        # La progression
        #
        self.progression = pysequence.Progression(self, self.classe)
        self.classe.SetDocument(self.progression)
        
        #
        # Arbre de structure de la progression
        #
        arbre = ArbreProgression(self.pnl, self.progression, self.classe,  self.panelProp)
        self.arbre = arbre
#         self.arbre.SelectItem(self.classe.branche)
        self.arbre.ExpandAll()
        
        #
        # Zone graphique de la fiche de projet
        #
        self.fiche = FicheProgression(self.nb, self.progression)       
#        self.thread = ThreadRedess(self.fichePrj)
        self.nb.AddPage(self.fiche, "Fiche Progression")
        
        #
        # Xmind
        #
#         self.pageXmind = wx.Panel(self.nb, -1)
#         self.nb.AddPage(self.pageXmind, "Carte mentale")
        
        #
        # Bulletins Officiels
        #
        self.pageBO = Panel_BO(self.nb)
        self.nb.AddPage(self.pageBO, "Bulletins Officiels")
        
        self.miseEnPlace()
        
#         self.fiche.Redessiner()
        
        wx.CallAfter(self.Thaw)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

        if not ouverture:
            #
            # Mise en liste undo/redo
            #    
#             self.classe.undoStack.do("Nouvelle Classe")
            self.progression.undoStack.do("Nouvelle Progression")
#             self.parent.miseAJourUndo()

    ###############################################################################################
    def GetDocument(self):
        return self.progression
    
    
    ###############################################################################################
    def OnPageChanged(self, event):
        new = event.GetSelection()
        event.Skip()
#        if new == 1: # On vient de cliquer sur la page "Xmind"
#            self.pageXmind.Remplir(self.fichierCourant, self.projet, self.typ)
      
            
        if new == 2: # On vient de cliquer sur la page "Bulletins Officiels"
            if self.progression.classe.typeEnseignement in REFERENTIELS:
                self.pageBO.Construire(REFERENTIELS[self.progression.classe.typeEnseignement])
            else:
                self.pageBO.Construire(self.progression.GetReferentiel())
            
            

        elif new == 0: # On vient de cliquer sur la fiche
            self.fiche.Redessiner()
            
    ###############################################################################################
    def OnDocModified(self, event):
        """ La Progression a été modifiée ...
        """
        if event.GetModif() != "":
#            print "OnDocModified", event.GetModif()
#             self.classe.undoStack.do(event.GetModif())
            self.progression.undoStack.do(event.GetModif())
        
        if event.GetDocument() == self.progression:
            if event.GetVerif():
                self.progression.VerifPb()
            if event.GetDraw():
                wx.CallAfter(self.fiche.Redessiner)
            self.MarquerFichierCourantModifie()
            
        elif event.GetDocument() == self.classe:
            if event.GetVerif():
                self.progression.VerifPb()
            if event.GetDraw():
                wx.CallAfter(self.fiche.Redessiner)
            self.MarquerFichierCourantModifie()
        
#         self.parent.miseAJourUndo()

   
    ###############################################################################################
    def restaurer(self):
        """ Restaure l'arbre de construction
            et redessine la fiche
            (après undo ou redo)
        """

        #
        # Réinitialisation de l'arbre
        #
        self.arbre.DeleteAllItems()
        root = self.arbre.AddRoot("")

        self.progression.ChargerSequences(self)
        self.progression.ChargerProjets(self)
        
        self.classe.ConstruireArbre(self.arbre, root)

        self.progression.ConstruireArbre(self.arbre, root)


        self.progression.Ordonner()

        self.progression.VerifPb()
        
        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        wx.CallAfter(self.arbre.SelectItem, self.classe.branche)


    ###############################################################################################
    def ProposerEnregistrer(self, doc, pathProg):
        """ Propose l'enregistrement d'un (nouveau) fichier de Séquence ou de Projet
            Renvoie un tuple : code, chemin du fichier
            code : 
            0 : Nouveau fichier --> à enregistrer
            1 : Fichier existant --> à ouvrir
            2 : Fichier existant --> annuler l'opération
            3 : opération annulée
        """
        wx.BeginBusyCursor()
        if doc.GetType() == 'seq':
            t = "La %s sera engegistrée" %doc.sing_()
            n = "nouvelle"
            e = '.seq'
        elif doc.GetType() == 'prj':
            t = "Le %s sera engegistré" %doc.sing_()
            n = "nouveau"
            e = '.prj'
        dlg = wx.TextEntryDialog(self, "Nom du fichier %s\n\n"\
                                 "%s dans le dossier de la Progression :\n" %(doc.sing_(), t) + toSystemEncoding(pathProg),
                                 "Enregistrement %s" %doc.du_() , "")

        if dlg.ShowModal() == wx.ID_OK:
            nomFichier = dlg.GetValue()
            dlg.Destroy()
            nomFichier = os.path.splitext(os.path.basename(nomFichier))[0]+e
            nomFichier = os.path.join(pathProg, nomFichier)
            
            if os.path.isfile(nomFichier):
                dlg = wx.MessageDialog(self, "Un fichier %s portant ce nom existe déjà.\n\n"\
                                             "Voulez-vous :\n"\
                                             " - l'ouvrir comme %s %s de la Progression : OUI\n"\
                                             " - écraser le fichier existant (toutes les données seront perdues) : NON\n"\
                                             " - choisir un autre nom pour la %s : ANNULER" %(doc.sing_(), n, doc.sing_(), doc.sing_()),
                                       "%s existante" %doc.sing_(),
                                       wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION |wx.YES_DEFAULT
                                       )
                res = dlg.ShowModal()
                dlg.Destroy()
                if res == wx.ID_YES:
                    wx.EndBusyCursor()
                    return 1, os.path.relpath(nomFichier, pathProg)
                elif res == wx.ID_NO:
                    pass
                else:
                    wx.EndBusyCursor()
                    return 2, ""
                             
            path = os.path.relpath(nomFichier, pathProg)
            
            # La séquence
            bdoc = doc.getBranche()
            bclasse = self.classe.getBranche()
            
            # La racine
            if doc.GetType() == 'seq':
                root = ET.Element("Sequence_Classe")
            elif doc.GetType() == 'prj':
                root = ET.Element("Projet_Classe")
            root.append(bdoc)
            root.append(bclasse)
            constantes.indent(root)
            enregistrer_root(root, nomFichier)
            
            wx.EndBusyCursor()
            return 0, path
        
        else:
            dlg.Destroy()
        
        wx.EndBusyCursor()
        return 3, ""
        
        
#     ###############################################################################################
#     def enregistrer(self, nomFichier):
#         """ Enregistrement
#             :param nomFichier: encodé en FileEncoding
#         """
#         wx.BeginBusyCursor()
#         
#         ok = self.progression.enregistrer(nomFichier)
#         
#         self.definirNomFichierCourant(nomFichier)
#         self.MarquerFichierCourantModifie(False)
#         wx.EndBusyCursor()
#         return ok
        
        
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True, reparer = False):
        """ <nomFichier> encodé en FileEncoding
        """
        print("Ouverture progression", nomFichier)
        
        Ok = True
        Annuler = False
        nbr_etapes = 8
        
        # Pour le suivi de l'ouverture
        message = nomCourt(nomFichier)+"\n\n"
        dlg = myProgressDialog("Ouverture d'une progression",
                                   message,
                                   nbr_etapes,
                                   wx.GetTopLevelParent(self))
        dlg.Show()
#         print(wx.GetTopLevelParent(self))
#         self.fiche.Hide()
        
        root = safeParse(nomFichier, dlg)
        if root is None:
            dlg.Close()
            return None#, "", 0, False, True
         
        
        #################################################################################################
        def get_err_message(err):
            return ("\n  "+CHAR_POINT).join([e.getMessage() for e in err])
        
        
        #################################################################################################
        def ouvre(message):
            nonlocal reparer      
            count = 0
            Ok = True
            Annuler = False
                   
            # La progression
            progression = root.find("Progression")
            if progression == None:
                self.progression.setBranche(root)
            else:
                # La classe
                message += "Construction de la structure de la classe...\t"
                dlg.update(count, message)

                count += 1
                classe = root.find("Classe")
                err = self.classe.setBranche(classe, reparer = reparer)
                if not reparer and int(self.classe.version.split(".")[0]) < 8:
                    raise OldVersion
                
                if self.VerifierReferentiel(dlg, "progression") == 1:
                    reparer = True
                    self.classe.setBranche(classe, reparer = reparer)
                
                if len(err) > 0 :
                    Ok = False
                    message += get_err_message(err) 
                message += "\n"
                
                
                # La progression
                message += "Construction de la structure de la progression...\t"
#                dlg.top()
                dlg.update(count, message)
                count += 1
                
                err = self.progression.setBranche(progression)
                self.progression.MiseAJourTypeEnseignement()
                
                if len(err) > 0 :
                    Ok = False
                    message += get_err_message(err)
                message += "\n"
            
            
            # Les propriétés
            prop = root.find("ProprietesDoc")
            if prop is not None:
                self.progression.proprietes.setBranche(prop)
            
            
            return root, message, count, Ok, Annuler


        ################################################################################################
        err = []

        try:
            root, message, count, Ok, Annuler = ouvre(message)
            
        except OldVersion:
            messageWarning(dlg, "Ancienne version",
                               "La progression\n    %s\n a été créée avec une version ancienne de pySéquence !\n" \
                               "Elle va être automatiquement converti au format actuel." %nomCourt(nomFichier))
            reparer = True
            root, message, count, Ok, Annuler = ouvre(message)
            
        except:
            count = 0
            err = [constantes.Erreur(constantes.ERR_INCONNUE)]
            message += err[0].getMessage() + "\n"
            Annuler = True
            if DEBUG:
                raise
            
        if reparer:
            self.MarquerFichierCourantModifie(True)
        #
        # Erreur fatale d'ouverture
        #
        if Annuler:
            message += "\n\nLa progression n'a pas pu être ouverte !\n\n"
            if len(err) > 0:
                message += "\n   L'erreur concerne :"
                message += get_err_message(err)
        
            self.Close()
            count = nbr_etapes
            dlg.update(count, message)
            wx.CallAfter(dlg.Destroy)
            return
        
        self.definirNomFichierCourant(nomFichier)
        
        #
        # Finalisation de l'ouverture
        #
        self.arbre.DeleteAllItems()
        root = self.arbre.AddRoot("")
        liste_actions = [[self.classe.ConstruireArbre, [self.arbre, root], {},
                         "Construction de l'arborescence de la classe...\t"],
                         [self.progression.ConstruireArbre, [self.arbre, root], {},
                          "Construction de l'arborescence de la progression...\t"],
                        [self.progression.ChargerSequences, [dlg], {"reparer" : reparer},
                         "Chargement des Séquences...\t"],
                        [self.progression.ChargerProjets, [dlg], {"reparer" : reparer},
                         "Chargement des Projets...\t"],
                        [self.progression.Ordonner, [], {},
                         "Classement...\t"],
                         ]
        
        for fct, arg, karg, msg in liste_actions:
#            print "+++", msg
            message += msg
            if dlg is not None:
                dlg.update(count, message)
            count += 1
            if DEBUG:
                fct(*arg, **karg)
                message += "Ok\n"
            else:
                try :
                    fct(*arg, **karg)
                    message += "Ok\n"
                except:
                    Ok = False
                    message += constantes.Erreur(constantes.ERR_INCONNUE).getMessage() + "\n"
                    if DEBUG:
                        raise
            

        self.progression.Verrouiller()

        message += "Tracé de la fiche...\t"
        dlg.update(count, message)
# #        dlg.top()
        count += 1

#        self.arbre.SelectItem(self.classe.branche)

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        wx.CallAfter(self.arbre.SelectItem, self.classe.branche)
#         self.arbre.SelectItem(self.arbre.classe.branche)


        if Ok:
            dlg.Destroy()
        else:
            dlg.update(nbr_etapes, message)
            dlg.Close() 
    
        self.SetTitre()
#        self.progression.MiseAJourTypeEnseignement()
        self.parent.MiseAJourToolBar()
         
         
        # Mise en liste undo/redo
#         self.classe.undoStack.do("Ouverture de la Classe")
        self.progression.undoStack.do("Ouverture de la Progression")
#         self.parent.miseAJourUndo()
        
        
        
        return self.progression
    
    
####################################################################################
#
#   Classe définissant la base de la fenétre de fiche
#
####################################################################################
class BaseFiche2(wx.ScrolledWindow): # Ancienne version : NE PAS SUPPRIMER (peut servir pour debuggage)
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent, -1, style = wx.VSCROLL | wx.RETAINED)
         
        self.InitBuffer()
        
        
    #############################################################################            
    def OnResize(self, evt = None):
#         print "OnResize"
        w = self.GetClientSize()[0]
        self.SetVirtualSize((w,w*29/21)) # Mise au format A4

        self.w, self.h = self.GetVirtualSize()
        self.InitBuffer()
        if w > 0 and self.IsShown():
            self.Redessiner()


    #############################################################################            
    def OnPaint(self, evt):
#         print("OnPaint")
#        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.DrawBitmap(self.buffer, 0,0) 

            
    #############################################################################            
    def InitBuffer(self):
        w,h = self.GetVirtualSize()
        if w == 0: w = 1
        if h == 0: h = 1
        self.buffer = wx.Bitmap(w,h)


    #############################################################################            
    def Redessiner(self, event = None):  
#         print("Redessiner :")
#         tps1 = time.clock()
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
            
            self.normalize(ctx)
            self.Draw(ctx)
#             if r is not None:
#                 draw_cairo.surbrillance(ctx, *r)

            self.ctx = ctx
            self.Refresh()
    
    #        tps2 = time.clock() 
    #        print "Tracé :"#, tps2 - tps1
            
            wx.EndBusyCursor()
            
#         self.t = threading.Thread(target=redess)
#         self.t.start()

        redess()        
#         tps2 = time.clock() 
#         print(tps2 - tps1)




        
####################################################################################
# from wx.lib.delayedresult import startWorker
class BaseFiche(wx.ScrolledWindow, DelayedResult):
    def __init__(self, parent):
#        wx.Panel.__init__(self, parent, -1)
        wx.ScrolledWindow.__init__(self, parent, -1, style = wx.VSCROLL | wx.RETAINED)
        DelayedResult.__init__(self, self.Compute)
        
#         self.t = None
        self.w, self.h = self.GetVirtualSize()
        self.buffer = wx.Bitmap(self.w, self.h)

        self.SizeUpdate()
#         self.Thaw()


    #############################################################################            
    def Redessiner(self, event = None):  
        
#         print("Redessiner")
        self.OnResize()    
#         tps2 = time.clock() 
#         print tps2 - tps1


    #############################################################################            
    def OnPaint(self, evt):
#        print "OnPaint"
        wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
#         dc = wx.PaintDC(self)
#         self.PrepareDC(dc)
#         dc.DrawBitmap(self.buffer, 0,0) 



    #-------------------------------------------------------------------------
    def OnResize(self, event = None):
#         print("OnResize")
        if not self.IsShownOnScreen():
            return
        
        w = self.GetClientSize()[0]
#         print "  ", w
        self.SetVirtualSize((w,w*29/21)) # Mise au format A4
        self.w, self.h = self.GetVirtualSize()

        if self.w > 0 and self.h > 0:
            try:
                self.buffer = self.buffer.ConvertToImage().Scale(self.w, self.h,
                                           quality = wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
            except:
                self.buffer = wx.Bitmap(self.w, self.h)

        else:
#             print("wh", self.w, self.h)
            self.buffer = wx.Bitmap()
        self.Refresh()
        self.Update()
        # After drawing empty bitmap start update
#         wx.CallAfter(self.SizeUpdate)
        self.SizeUpdate()


    #-------------------------------------------------------------------------
    def OnEraseBackground(self, event):
        pass # Or None


    #-------------------------------------------------------------------------
    def SizeUpdate(self):
        # The timer is used to wait for last thread to finish
        self.timer.Stop()
        self.timer.Start(100)

    #-------------------------------------------------------------------------
    def Compute(self):
#         print("Compute")
        self.SetCursor(wx.Cursor(wx.HOURGLASS_CURSOR))
#         if hasattr(self, "imagesurface"):
#             self.imagesurface.flush()
#             self.imagesurface.mark_dirty()
        if hasattr(self, "ctx"):
            del self.ctx
        self.imagesurface = cairo.ImageSurface(cairo.FORMAT_RGB24, self.w, self.h)#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        self.ctx = cairo.Context(self.imagesurface)
        self.normalize(self.ctx)
        self.ctx.set_source_rgba(1,1,1,1)
        self.ctx.paint()
#         print("Status", cairo.cairo.cairo_status_to_string(cairo.cairo.cairo_status(self.ctx)))
        try:
            self.Draw(self.ctx)
        except MemoryError:
            print("MemoryError")
            
        self.buffer = wx.lib.wxcairo.BitmapFromImageSurface(self.imagesurface)
        
#         self.imagesurface.flush()
#         temp_buffer = wx.lib.wxcairo.BitmapFromImageSurface(imagesurface)
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        return self.buffer


        
BaseFiche = BaseFiche2 # Décommenter pour mod debug

class FicheDoc(BaseFiche):
    def __init__(self, parent, threaded = False):
        BaseFiche.__init__(self, parent)
        

        self.EnableScrolling(False, True)
        self.SetScrollbars(20, 20, 50, 50);
        
#         self.surRect = None     # Liste des rectangles en surbrillance
        self.surObj = None      # Objet en surbrillance
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        
        wx.CallAfter(self.connect)


    ######################################################################################################
    def connect(self):
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDClick)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRClick)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_MOTION, self.OnMove)
        
        
    ######################################################################################  
    def HideTip(self, pos = None):
        self.GetDoc().GetApp().HideTip(pos)
    
    
    ######################################################################################  
    def Move(self, zone, x, y):
        self.GetDoc().GetApp().Move(zone, x, y)
    
    
    ######################################################################################################
    def OnLeave(self, evt = None):
        x, y = evt.GetPosition()
        x, y = self.ClientToScreen((x, y))
        self.HideTip((x, y))
#         self.GetDoc().HideTip((x, y))
        

    ######################################################################################################
    def OnEnter(self, event):
        self.SetFocus()
        event.Skip()
    
    #############################################################################            
    def OnScroll(self, evt):
        self.Refresh()
        
    
    ######################################################################################################
    def OnMove(self, evt):
        c = self.getCoordZone(evt)
        if c is None: 
            return
        x, y, zone = c
        
        #
        # Cas général
        #
        if zone is not None:
            self.Move(zone, x, y)
            if zone.estClicable(): 
                self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            else:
                self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        else:
            self.HideTip()
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))


            
        evt.Skip()

    


#     #############################################################################            
#     def MiseAJourSur(self, obj):
#         """ Met l'objet <obj> en surbrillance
#         """
#         self.surRect = self.getRects(obj)
# #         self.surRect = None
# #         if hasattr(obj, 'rect') and hasattr(self, "ctx"):
# #             self.surRect = obj.rect
#     
    
    
    
    #############################################################################            
    def Surbrillance(self, obj = None):
        """ Met l'objet <obj> en surbrillance
            et redessine
        """
#         print("Surbrillance", obj)
#         if obj is None:
#             self.surRect = []
#         else:
#             self.surRect = self.getRects(obj)
        self.surObj = obj
#         print("   ", self.surRect)
        self.Redessiner()
        
    
    #############################################################################            
    def CentrerSur(self, obj):
        rect = self.fiche.getRects(obj)
        if len(rect) > 0:
            y0 = min([r[1] for r in rect])
            y1 = max([r[1]+r[3] for r in rect])
            
            y0 = y0*self.GetVirtualSize()[1]/draw_cairo.COEF/20
            y1 = y1*self.GetVirtualSize()[1]/draw_cairo.COEF/20
            Y = self.GetViewStart()[1]
            H = self.GetClientSize()[1]/20
#                 print(y0, y1, Y, H)
            if y0 < Y:
                self.Scroll(0, y0)
            if  y1 > Y+H:
                self.Scroll(0, y1-H+1)
        
        
#         if hasattr(obj, 'rect'):
# #             print("CentrerSur", obj, obj.rect)
# #             self.Redessiner()
#             if len(obj.rect) > 0:
#                 y0 = min([r[1] for r in obj.rect])
#                 y1 = max([r[1]+r[3] for r in obj.rect])
#                 
#                 y0 = y0*self.GetVirtualSize()[1]/draw_cairo.COEF/20
#                 y1 = y1*self.GetVirtualSize()[1]/draw_cairo.COEF/20
#                 Y = self.GetViewStart()[1]
#                 H = self.GetClientSize()[1]/20
# #                 print(y0, y1, Y, H)
#                 if y0 < Y:
#                     self.Scroll(0, y0)
#                 if  y1 > Y+H:
#                     self.Scroll(0, y1-H+1)
    


    ######################################################################################################
    def getCoordZone(self, evt):
        """ Renvoie les coordonnées 
            et la zone (draw_cairo2.Zone_sens)
            associées à l'événement de type mouseevent
        """
        if not hasattr(self, 'ctx'):
            evt.Skip()
            return
        self.HideTip()
        x, y = evt.GetPosition()
        _x, _y = self.CalcUnscrolledPosition(x, y)
        x, y = self.ClientToScreen((x, y))
        try:
            xx, yy = self.ctx.device_to_user(_x, _y)
        except:
            return
        zone = self.GetDoc().HitTest(xx, yy)
        return x, y, zone 
    

    #############################################################################            
    def OnClick(self, evt):
        """ Actions réalisées quand on a cliqué sur la fiche
            Renvoie l'objet cliqué (sinon None)
        """
        
        c = self.getCoordZone(evt)
        if c is None: return
        x, y, zone = c
        
        #
        # Cas général
        #
        if zone is not None:
            
            self.GetDoc().Click(zone, x, y)
            obj = zone.obj
        else:
            self.HideTip()
            obj = None
        evt.Skip()
        return obj
    
    
    #############################################################################            
    def OnDClick(self, evt):
        item = self.OnClick(evt)
        if item != None and hasattr(item, "branche"):
            self.GetDoc().AfficherLien(item.branche)
            
            
    #############################################################################            
    def OnRClick(self, evt):
        item = self.OnClick(evt)
#         print("OnRClick", item)
        if item != None and hasattr(item, "branche"):
            self.GetDoc().AfficherMenuContextuel(item.branche)
            
            
            
            
    #############################################################################            
    def normalize(self, cr):
#         h = float(self.GetVirtualSize()[1]) / draw_cairo.COEF
        h = float(self.h)/ draw_cairo.COEF
        if h <= 0:
            h = 1.0
        cr.scale(h, h) 
        
        
    #############################################################################            
    def Draw(self, ctx):
#         print("Draw", self.fiche)
        self.fiche.draw(ctx, surObj = self.surObj)
#         self.GetDoc().DefinirCouleurs()
#         self.GetDoc().draw.Draw(ctx, self.GetDoc(), surRect = self.surRect)




            
    
####################################################################################
#
#   Classe définissant la fenétre de la fiche de séquence
#
####################################################################################
class FicheSequence(FicheDoc):
    def __init__(self, parent, sequence):
        FicheDoc.__init__(self, parent)
        self.sequence = sequence


        self.fiche = draw_cairo_seq.Sequence(sequence)
#         print("   proprietes3", self.sequence.proprietes.proprietes)
        
        
    ######################################################################################################
    def GetDoc(self):
        return self.sequence
       



    
####################################################################################
#
#   Classe définissant la fenétre de la fiche de séquence
#
####################################################################################
class FicheProjet(FicheDoc):
    def __init__(self, parent, projet):
        FicheDoc.__init__(self, parent)
        self.projet = projet
        
        
        self.fiche = draw_cairo_prj.Projet(projet)
        
        
#        #
#        # Création du Tip (PopupInfo) pour les compétences
#        #
#        l = 0
#        popup = PopupInfo2(self.projet.GetApp(), u"Compétence")
#        popup.sizer.SetItemSpan(popup.titre, (1,2)) 
#        l += 1
#        
#        self.tip_comp = popup.CreerTexte((l,0), (1,2), flag = wx.ALL)
#        self.tip_comp.SetForegroundColour("CHARTREUSE4")
#        self.tip_comp.SetFont(wx.Font(11, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
#        l += 1
#        
#        self.tip_arbre = popup.CreerArbre((l,0), (1,2), projet.GetReferentiel(), flag = wx.ALL)
#        l += 1
#        
#        self.lab_legend = {}
#        for i, (part , tit) in enumerate(self.projet.GetProjetRef().parties.items()):
#            self.lab_legend[part] = popup.CreerTexte((l,i), txt = tit, flag = wx.ALIGN_RIGHT|wx.RIGHT)
#            self.lab_legend[part].SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
#            self.lab_legend[part].SetForegroundColour(constantes.getCoulPartie(part))
#            
#            
##        self.lab_legend1 = popup.CreerTexte((l,0), txt = u"Conduite", flag = wx.ALIGN_RIGHT|wx.RIGHT)
##        self.lab_legend1.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
##        self.lab_legend1.SetForegroundColour(constantes.COUL_PARTIE['C'])
##        
##        self.lab_legend2 = popup.CreerTexte((l,1), txt = u"Soutenance", flag = wx.ALIGN_LEFT|wx.LEFT)
##        self.lab_legend2.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
##        self.lab_legend2.SetForegroundColour(constantes.COUL_PARTIE['S'])
#        
#        self.popup = popup
##        self.MiseAJourTypeEnseignement(self.projet.classe.typeEnseignement)
        
    ######################################################################################################
    def GetDoc(self):
        return self.projet
            
#    ######################################################################################################
#    def OnMove(self, evt):
#        
#        if hasattr(self, 'tip'):
#            self.tip.Show(False)
#            self.call.Stop()
#        
#        x, y = evt.GetPosition()
#        _x, _y = self.CalcUnscrolledPosition(x, y)
#        xx, yy = self.ctx.device_to_user(_x, _y)
#        evt.Skip()
#        
#        #
#        # Cas général
#        #
#        branche = self.projet.HitTest(xx, yy)
#        if branche != None:
#            elem = branche.GetData()
#            if hasattr(elem, 'tip'):
#                x, y = self.ClientToScreen((x, y))
#                elem.tip.Position((x+1,y+1), (0,0))
#                self.call = wx.CallLater(500, elem.tip.Show, True)
#                self.tip = elem.tip
#                evt.Skip()
#                return    
#        
#        #
#        # Cas particulier des compétences
#        #
#        kCompObj = self.projet.HitTestCompetence(xx, yy)
#        if kCompObj != None:
#            kComp, obj = kCompObj
#            if hasattr(self, 'popup'):
##                for tip in self.tip_indic:
##                    tip.Destroy()
##                self.tip_indic = []
#                x, y = self.ClientToScreen((x, y))
##                type_ens = self.projet.classe.typeEnseignement
#                prj = self.projet.GetProjetRef()
#                
#                competence = prj.getCompetence(kComp[0], kComp[1:])
#                        
#                intituleComp = competence[0]
#                
#                k = kComp.split(u"\n")
#                if len(k) > 1:
#                    titre = u"Compétences\n"+u"\n".join(k)
#                else:
#                    titre = u"Compétence\n"+k[0]
#                self.popup.SetTitre(titre)
#             
#                intituleComp = "\n".join([textwrap.fill(ind, 50) for ind in intituleComp.split(u"\n")]) 
#             
#                self.popup.SetTexte(intituleComp, self.tip_comp)
#                
#                self.tip_arbre.DeleteChildren(self.tip_arbre.root)
#                if type(competence[1]) == dict:  
#                    indicEleve = obj.GetDicIndicateurs()
#                else:
#                    indicEleve = obj.GetDicIndicateurs()[kComp]
#                self.tip_arbre.Construire(competence[1], indicEleve, prj)
#                
#                self.popup.Fit()
#
#                self.popup.Position((x,y), (0,0))
#                self.call = wx.CallLater(500, self.popup.Show, True)
#                self.tip = self.popup
#            
#        evt.Skip()


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
            
        
#    #############################################################################            
#    def Draw(self, ctx):
#        draw_cairo_prj.Draw(ctx, self.projet)
        

####################################################################################
#
#   Classe définissant la fenétre de la fiche de séquence
#
####################################################################################
class FicheProgression(FicheDoc):
    def __init__(self, parent, progression):
        FicheDoc.__init__(self, parent)
        self.progression = progression
        
        
        self.fiche = draw_cairo_prg.Progression(progression)
        
        
#        #
#        # Création du Tip (PopupInfo) pour les compétences
#        #
#        l = 0
#        popup = PopupInfo2(self.progression.GetApp(), u"Compétence")
#        popup.sizer.SetItemSpan(popup.titre, (1,2)) 
#        l += 1
#        
#        self.tip_comp = popup.CreerTexte((l,0), (1,2), flag = wx.ALL)
#        self.tip_comp.SetForegroundColour("CHARTREUSE4")
#        self.tip_comp.SetFont(wx.Font(11, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
#        l += 1
#        
#        
#        
#        self.lab_legend = {}
#        for i, (part , tit) in enumerate(self.progression.GetProjetRef().parties.items()):
#            self.lab_legend[part] = popup.CreerTexte((l,i), txt = tit, flag = wx.ALIGN_RIGHT|wx.RIGHT)
#            self.lab_legend[part].SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
#            self.lab_legend[part].SetForegroundColour(constantes.getCoulPartie(part))
#            
#            
##        self.lab_legend1 = popup.CreerTexte((l,0), txt = u"Conduite", flag = wx.ALIGN_RIGHT|wx.RIGHT)
##        self.lab_legend1.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
##        self.lab_legend1.SetForegroundColour(constantes.COUL_PARTIE['C'])
##        
##        self.lab_legend2 = popup.CreerTexte((l,1), txt = u"Soutenance", flag = wx.ALIGN_LEFT|wx.LEFT)
##        self.lab_legend2.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
##        self.lab_legend2.SetForegroundColour(constantes.COUL_PARTIE['S'])
#        
#        self.popup = popup
#        self.MiseAJourTypeEnseignement(self.projet.classe.typeEnseignement)
        
    ######################################################################################################
    def GetDoc(self):
        return self.progression
    
#     ######################################################################################################
#     def OnLeave(self, evt = None):
#         self.GetDoc().HideTip()
            



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
            
        
#    #############################################################################            
#    def Draw(self, ctx):
#        draw_cairo_prg.Draw(ctx, self.progression)
        
    
    
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
        """ On remplace le panel affiché par un nouveau
        """
        #
        # Destruction de l'ancien panel
        #
        if self.panel is not None:
#             print("Destroy", self.panel)
#            try:
#            self.bsizer.Remove(self.panel)
            try:
                self.panel.DestroyLater()
            except:
                pass
#            except:
#                print "erreur AfficherPanel"
        
#        if self.panel != None:
#            self.bsizer.Detach(self.panel)
#            self.panel.Hide()
        
        #
        # Mise en place du nouveau
        #
        self.panel = panel
        self.bsizer.Add(self.panel, 1, flag = wx.EXPAND|wx.GROW)
        self.panel.Show()
        self.bsizer.Layout()
#        self.panel.Refresh()
#        self.Refresh()        
    

                         
                
####################################################################################
#
#   Classe définissant le panel de propriété par défaut
#
####################################################################################
DELAY = 100 # Delai en millisecondes avant de rafraichir l'affichage suite à un saisie au clavier
class PanelPropriete(scrolled.ScrolledPanel):
    def __init__(self, parent, titre = "", objet = None,
                 panelRacine = None,
                 style = wx.VSCROLL | wx.RETAINED):
        scrolled.ScrolledPanel.__init__(self, parent, -1, style = style)#|wx.BORDER_SIMPLE)
        self.objet = objet
        
        if panelRacine is not None:
            self.panelRacine = panelRacine
        else:
            self.panelRacine = self
        
        self.sizer = wx.GridBagSizer()
#        self.Hide()  # utilité ?? à priori cause des erreurs au lancement (linux en autres)
#        self.SetMinSize((400, 200))
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
#        self.SetScrollRate(20,20)
#         self.EnableScrolling(False, True)
        self.SetupScrolling(scroll_x = False) # ? Cause des problèmes (wx._core.PyDeadObjectError)
        

        self.eventAttente = False
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        
#         self.Bind(wx.EVT_SIZE, self.OnResize)
        

        self.clip = wx.Clipboard()
        self.x = wx.BitmapDataObject()
        
        

    ######################################################################################              
    def OnResize(self, evt):
        self.Refresh()
        evt.Skip()
    
    
    ######################################################################################################
    def GetPanelRacine(self):
        return self.panelRacine
    
    
    ######################################################################################################
    def OnEnter(self, event):
#        print "OnEnter PanelPropriete"
        self.SetFocus()
        event.Skip()

    #########################################################################################################
    def onUndoRedo(self):
        """ Renvoie True si on est en phase de Undo/Redo
        """
        return self.GetDocument().undoStack.onUndoRedo# or self.GetDocument().classe.undoStack.onUndoRedo
    
    
    #########################################################################################################
    def sendEvent(self, doc = None, modif = "", draw = False, verif = False):
        self.GetDocument().GetApp().sendEvent(doc, modif, draw = draw, verif = verif)
        self.eventAttente = False
        
    
    #########################################################################################################
    def GetFenetreDoc(self):
        return self.GetDocument().app

    #########################################################################################################
    def CreateImageSelect(self, parent, titre = "image", prefixe = "l'", defaut = wx.NullBitmap):
        self.boxImg = myStaticBox(parent, -1, titre.capitalize())
        bsizer = wx.StaticBoxSizer(self.boxImg, wx.VERTICAL)
        image = wx.StaticBitmap(parent, -1, defaut)
        image.Bind(wx.EVT_RIGHT_UP, self.OnRClickImage)
        self.image = image
        self.SetImage()
        bsizer.Add(image, 1)#, flag = wx.EXPAND)
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        bt = wx.Button(parent, -1, "Changer")
        bt.SetToolTip("Sélectionner un fichier image pour %s" %prefixe+titre)
        hsizer.Add(bt, 1, flag = wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.OnClickImage, bt)
        self.btImg = bt
        
        bt = wx.BitmapButton(parent, -1, scaleImage(images.Icone_supprimer.GetBitmap(), 20*SSCALE, 20*SSCALE))
        bt.SetToolTip("Supprimer %s" %prefixe+titre)
        hsizer.Add(bt, flag = wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.OnSupprImage, bt)
        self.btSupImg = bt
        
        bsizer.Add(hsizer, flag = wx.EXPAND)
        return bsizer
        
        
    #########################################################################################################
    def MiseAJourImageSelect(self, titre = "image", prefixe = "l'"):
        self.boxImg.SetLabel(titre.capitalize())
        self.btImg.SetToolTip("Sélectionner un fichier image pour %s" %prefixe+titre)
        self.btSupImg.SetToolTip("Supprimer %s" %prefixe+titre)

    
    #############################################################################            
    def OnSupprImage(self, event):
        self.objet.image = None
        self.SetImage(True)
        
    #############################################################################            
    def OnRClickImage(self, event):
        print("OnRClickImage")
        self.clip.Open()
        ok = self.clip.GetData(self.x)
        self.clip.Close()
        if ok:
            self.GetFenetreDoc().AfficherMenuContextuel([["Coller l'image", 
                                                          self.collerImage, 
                                                          None,
                                                          True
                                                          ]
                                                        ])
     
 
 
    #############################################################################            
    def collerImage(self, sendEvt = False):
        self.support.image = self.x.GetBitmap()
#        self.SetImage(True)

    #############################################################################            
    def OnClickImage(self, event):
        mesFormats = "Fichier Image|*.bmp;*.png;*.jpg;*.jpeg;*.gif;*.pcx;*.pnm;*.tif;*.tiff;*.tga;*.iff;*.xpm;*.ico;*.ico;*.cur;*.ani|" \
                       "Tous les fichiers|*.*'"
        
        dlg = wx.FileDialog(
                            self, message="Ouvrir une image",
#                            defaultDir = self.DossierSauvegarde, 
                            defaultFile = "",
                            wildcard = mesFormats,
                            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
                            )
            
        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()#.decode(FILE_ENCODING)
            nomFichier = paths[0]
            
            try:
                locale2EN()
                bmp = wx.Image(nomFichier).ConvertToBitmap()
                locale2def()
            except:
                messageErreur(self, "Erreur !",
                                    "Fichier image invalide !\n" \
                                 )
                dlg.Destroy()
                return
            self.objet.image = rognerImage(bmp)
            self.SetImage(True)
        
        dlg.Destroy()


    #############################################################################            
    def SetImage(self, sendEvt = False):
        if self.objet.image != None:
            self.image.SetBitmap(rognerImage(self.objet.image, 200*SSCALE, HMIN_PROP*SSCALE-80*SSCALE))
        else:
            self.image.SetBitmap(wx.NullBitmap)
        self.sizer.Layout()
        
        if sendEvt:
            self.sendEvent(modif = "Modification de l'illustration "+self.objet.du_(),
                           draw = False, verif = False)
            
            
    #############################################################################            
    def CreateLienSelect(self, parent):
        box = myStaticBox(parent, -1, "Lien externe")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.selec = lien.URLSelectorCombo(parent, self.objet.lien, self.objet.GetPath())
        self.Bind(lien.EVT_PATH_MODIFIED, self.OnPathModified)
        bsizer.Add(self.selec, flag = wx.EXPAND)
        
        
        return bsizer
    
    
    


    #############################################################################            
    def CreateIconeSelect(self, parent):
        ib = myStaticBox(parent, -1, "Icônes")
        ibsizer = wx.StaticBoxSizer(ib, wx.VERTICAL)
        pnl = scrolled.ScrolledPanel(parent, -1, style = wx.VSCROLL)
#         pnl = wx.VScrolledWindow(parent, -1, style = wx.VSCROLL | wx.EXPAND)
#         pnl.EnableScrolling(False, True)
        ims = wx.WrapSizer()
        pnl.SetSizer(ims)
        pnl.SetupScrolling()
        
#             ims.SetSize((100,-1))
        self.icones = []
        for i, (nom, img) in enumerate(constantes.ICONES_TACHES.items()):
            ico = img.ConvertToImage().Scale(20*SSCALE, 20*SSCALE).ConvertToBitmap()
            btn = wx.BitmapButton(pnl, 100+i, ico)
            btn.SetToolTip(nom)
            self.icones.append(nom)
            ims.Add(btn, 0, flag = wx.ALL, border = 2)
            btn.Refresh()
            self.Bind(wx.EVT_BUTTON, self.OnIconeClick, btn)
        
        ibsizer.Add(pnl, 1, flag = wx.EXPAND)
        
        self.btn_no_icon = wx.Button(parent, -1, "Aucune")
        ibsizer.Add(self.btn_no_icon)
        self.Bind(wx.EVT_BUTTON, self.OnIconeClick, self.btn_no_icon)
        pnl.FitInside()
        parent.Layout()
        return ibsizer
    
    
    #############################################################################            
    def OnIconeClick(self, event):
        if event.GetId() == self.btn_no_icon.GetId():
            self.objet.icone = None
        else:
            self.objet.icone = constantes.ICONES_TACHES[self.icones[event.GetId()-100]]
        self.sendEvent(modif = "Modification de l'icône "+self.objet.du_(),
                       draw = True, verif = False)   



    ######################################################################################  
    def OnPathModified(self, evt):
        self.GetDocument().OnPathModified()


####################################################################################
#
#   Classe définissant le panel "racine" (ne contenant que des infos HTML)
#
####################################################################################

class PanelPropriete_Racine(wx.Panel):
    def __init__(self, parent, texte = None):
#         print("PanelPropriete_Racine", texte)
        wx.Panel.__init__(self, parent, -1)
        if texte is not None:
            wx.StaticText(self, -1, "" + texte)

     

####################################################################################
#
#   Classe définissant le panel de propriété de séquence
#
####################################################################################
class PanelPropriete_Sequence(PanelPropriete):
    def __init__(self, parent, sequence):
        self.sequence = sequence
        PanelPropriete.__init__(self, parent, objet = self.sequence)
        
        
        ref = self.sequence.GetReferentiel()
        
        #
        # Intitulé
        #
        titre = myStaticBox(self, -1, ref.getLabel("SEQINT").Sing_())
        sb = wx.StaticBoxSizer(titre)
        textctrl = TextCtrl_Help(self, "", scale = SSCALE)
        textctrl.SetTitre(ref.getLabelAide("SEQINT"), sequence.getIcone())
        textctrl.SetToolTip("")
                    
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        self.sizer.Add(sb, (0,0), flag = wx.ALL|wx.EXPAND, border = 2)
#        self.sizer.Add(textctrl, (0,1), flag = wx.EXPAND)
#        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
#         self.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.textctrl)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.textctrl)

        #
        # Commentaires
        #
        titre = myStaticBox(self, -1, "Commentaires")
        sb = wx.StaticBoxSizer(titre)
        commctrl = TextCtrl_Help(self, "", scale = SSCALE)
        commctrl.SetTitre("Commentaires sur la Séquence", sequence.getIcone())
        commctrl.SetToolTip("")
                    
        sb.Add(commctrl, 1, flag = wx.EXPAND)
        self.commctrl = commctrl
        self.sizer.Add(sb, (0,2), (1,1),  flag = wx.ALL|wx.EXPAND, border = 2)
#        self.sizer.Add(commctrl, (1,1), flag = wx.EXPAND)
#        self.Bind(wx.EVT_TEXT, self.EvtText, commctrl)
#         self.Bind(stc.EVT_STC_CHANGE, self.EvtText, commctrl)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, commctrl)
        
        #
        # Position
        #
        titre = myStaticBox(self, -1, "Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        self.bmp = wx.StaticBitmap(self, -1, self.getBitmapPeriode())
        self.position = PositionCtrl(self, self.sequence.position,    
#                                      self.sequence.GetReferentiel().periodes)                      
                                     self.sequence.classe.GetPeriodes(),
                                     totmax = self.sequence.GetReferentiel().getNbrPeriodes()
                                     )
#         self.Bind(wx.EVT_RADIOBUTTON, self.onChanged)
        self.Bind(wx.EVT_SLIDER, self.onChanged)
        sb.Add(self.bmp, flag = wx.EXPAND)
        sb.Add(self.position, flag = wx.EXPAND)
        
        self.sizer.Add(sb, (1,0), flag = wx.ALL|wx.EXPAND, border = 2)
        
        #
        # Lien externe
        #
        lsizer = self.CreateLienSelect(self)
        self.sizer.Add(lsizer, (1,2), (1,1),  wx.ALL|wx.EXPAND, border = 2)

        
        self.sizer.SetEmptyCellSize((0, 0))
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(2)
        
        self.cbD = {}
        self.CreerCBDomaine() # Permet de créer les Checkbox "Domaine"
        
        self.MiseAJour()
        
        self.sizer.Layout()
        self.Layout()
        
#        self.Fit()
        
    
    #############################################################################            
    def getBitmapPeriode(self, larg = 250):
        return self.sequence.getBitmapPeriode(larg)
         
    
    #############################################################################            
    def onChanged(self, evt):
        self.sequence.SetPosition(self.position.GetRange())
        self.SetBitmapPosition()
        self.sendEvent(modif = "Changement de position de la Séquence",
                       draw = True, verif = False)
        
        
    #############################################################################            
    def SetBitmapPosition(self, bougerSlider = None):
        self.bmp.SetBitmap(self.getBitmapPeriode())
        self.position.SetValue(self.sequence.position)


    #############################################################################            
    def EvtCheckBox(self, event):
        
#         cb = event.GetEventObject()
        self.sequence.domaine = "".join([t for t, cb in list(self.cbD.items()) if cb.IsChecked()])
        self.sequence.classe.Verrouiller(len(self.sequence.domaine) > 0)
        
        self.sendEvent(modif = "Modification du domaine de la Séquence", 
                       draw = False, verif = False)
        
            
    #############################################################################            
    def EvtText(self, event):
#         print("EvtText")
        if event.GetEventObject() == self.textctrl:
            self.sequence.SetText(self.textctrl.GetText())
            t = "Modification de l'intitulé de la Séquence"
        else:
            self.sequence.SetCommentaire(self.commctrl.GetText())
            t = "Modification du commentaire de la Séquence"
        
        if self.onUndoRedo():
            self.sendEvent(modif = t, draw = True, verif = False)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = t, draw = True, verif = False)
                self.eventAttente = True


    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#         print("Miseàjour", self, sendEvt)
        
        self.textctrl.SetValue(self.sequence.intitule, False)
        self.commctrl.SetValue(self.sequence.commentaires, False)
#        self.textctrl.ChangeValue(self.sequence.intitule)
        
        ref = self.sequence.GetReferentiel()
#        self.position.SetMax(ref.getNbrPeriodes()-1)
        self.sequence.position[1] = min(self.sequence.position[1], ref.getNbrPeriodes()-1)
        self.position.SetValue(self.sequence.position)
        self.bmp.SetBitmap(self.getBitmapPeriode())
        
        for t, cb in self.cbD.items():
            cb.SetValue(t in self.sequence.domaine)

        self.Layout()
        
        if sendEvt:
            self.sendEvent()


    #############################################################################            
    def CreerCBDomaine(self):
        if self.sizer.FindItemAtPosition((0,1)) is not None:
            for cb in self.cbD.values():
                cb.Destroy()
            self.sizer.Remove(self.sb)
            
        self.cbD = {}
        if len(self.sequence.domaine) > 1:
            if self.sizer.FindItemAtPosition((0,1)) is None:
                ref = self.sequence.GetReferentiel()
                if len(self.sequence.domaine)>1:
                    t = ref._nomDom.Plur_()
                else:
                    t = ref._nomDom.Sing_()
                titre = myStaticBox(self, -1, t)
                self.sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
                
                for dom in ref.listeDomaines:
                    cb = wx.CheckBox(self, -1, ref.domaines[dom][0])
                    cb.SetToolTip(ref.domaines[dom][1])
                    self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
                    self.sb.Add(cb)
                    self.cbD[dom] = cb
                
                self.sizer.Add(self.sb, (0,1), (2, 1), flag = wx.ALL|wx.EXPAND, border = 2)

        
            
        
# #        print "MiseAJourTypeEnseignement"
#         if self.sequence.GetReferentiel().domainesMEI:
# #            print self.sizer.FindItemAtPosition((1,0))
#             if self.sizer.FindItemAtPosition((0,1)) is None:
#                 titre = myStaticBox(self, -1, u"Domaines")
#                 self.sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
#                 self.cbM = wx.CheckBox(self, -1, u"Matériaux et Structures")
#                 self.cbE = wx.CheckBox(self, -1, u"Energie")
#                 self.cbI = wx.CheckBox(self, -1, u"Information")
#                 self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.cbM)
#                 self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.cbE)
#                 self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.cbI)
#                 self.sb.AddMany([self.cbM, self.cbE, self.cbI])
#                 self.sizer.Add(self.sb, (0,1), (2, 1), flag = wx.ALIGN_TOP | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
#         else:
#             if self.sizer.FindItemAtPosition((0,1)) is not None:
#                 self.cbM.Destroy()
#                 self.cbE.Destroy()
#                 self.cbI.Destroy()
#                 self.sizer.RemovePos(self.sb)
            
    
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
        self.projet = projet
        PanelPropriete.__init__(self, parent, objet = self.projet)
        
        self.nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
        
        self.construire()
        
        self.sizer.Add(self.nb, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
#        self.sizer.Layout()
        
        self.Layout()
        self.FitInside()

        self.MiseAJourTypeEnseignement()
        self.MiseAJour()
        
        self.Show()
        
#        self.Fit()
        
    #############################################################################            
    def GetDocument(self):
        return self.projet
    
    #############################################################################            
    def GetPageNum(self, win):
        for np in range(self.nb.GetPageCount()):
            if self.nb.GetPage(np) == win:
                return np
        
    #############################################################################            
    def creerPageSimple(self, fct, titre = "", helpText = ""):
        bg_color = self.Parent.GetBackgroundColour()
        page = PanelPropriete(self.nb, objet = self.GetDocument())
        page.SetBackgroundColour(bg_color)
        self.nb.AddPage(page, "")
#        ctrl = orthographe.STC_ortho(page, -1)#, u"", style=wx.TE_MULTILINE)
        ctrl = TextCtrl_Help(page, titre, helpText, scale = SSCALE)
#         page.Bind(stc.EVT_STC_CHANGE, fct, ctrl)
        page.Bind(stc.EVT_STC_MODIFIED, fct, ctrl)
#        page.Bind(wx.EVT_TEXT, fct, ctrl)
        page.sizer.Add(ctrl, (0,0), flag = wx.EXPAND)
        page.sizer.AddGrowableCol(0)
        page.sizer.AddGrowableRow(0)  
        page.sizer.Layout()
        return page, ctrl, self.nb.GetPageCount()-1
    
    
    #############################################################################            
    def construire(self):
#        ref = self.projet.GetReferentiel()
        
        # Conteneur pour les différentes pages du NoteBook (hormis pageGen)
        self.pages = {}


        #
        # La page "Généralités"
        #
        pageGen = PanelPropriete(self.nb, objet = self.GetDocument())
        bg_color = self.Parent.GetBackgroundColour()
        pageGen.SetBackgroundColour(bg_color)
        self.pageGen = pageGen
        self.nb.AddPage(pageGen, "Propriétés générales")


        #
        # Intitulé du projet (TIT)
        #
        self.titre = myStaticBox(pageGen, -1, "")
        sb = wx.StaticBoxSizer(self.titre)
        textctrl = TextCtrl_Help(pageGen, "", scale = SSCALE)
        
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        pageGen.sizer.Add(sb, (0,0), flag = wx.LEFT|wx.EXPAND, border = 2)
#        pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText)
#        pageGen.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
#         pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.textctrl)
        pageGen.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.textctrl)
        
        
        
        #
        # Problématique (PB)
        #
        self.tit_pb = myStaticBox(pageGen, -1, "")
        sb = wx.StaticBoxSizer(self.tit_pb)
#        self.commctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
        self.commctrl = TextCtrl_Help(pageGen, "", scale = SSCALE)
                                              
                                              
        sb.Add(self.commctrl, 1, flag = wx.EXPAND)
        pageGen.sizer.Add(sb, (0,1), (2,1),
                          flag = wx.LEFT|wx.EXPAND, border = 2)
#        pageGen.Bind(wx.EVT_TEXT, self.EvtText, self.commctrl)
#        pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.commctrl)
#         pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.commctrl)
        pageGen.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.commctrl)
        

        #
        # Année scolaire et Position dans l'année
        #
        titre = myStaticBox(pageGen, -1, "Années et Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        
        self.annee = Variable("Année scolaire", lstVal = self.projet.annee, 
                                   typ = VAR_ENTIER_POS, bornes = [2012,2100])
        self.ctrlAnnee = VariableCtrl(pageGen, self.annee, coef = 1, signeEgal = False,
                                      help = "Années scolaires", sizeh = 40*SSCALE, 
                                      unite = str(self.projet.annee+1),
                                      sliderAGauche = True)
        self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlAnnee)
        sb.Add(self.ctrlAnnee)
        
        self.bmp = wx.StaticBitmap(pageGen, -1, self.getBitmapPeriode(250*SSCALE))
#         self.bmp = CairoStaticBitmap(pageGen, self.projet.drawPeriode, 250*SSCALE)
        
        ref = self.projet.GetReferentiel()
        self.position = PositionCtrl(pageGen, self.projet.position,
                                     ref.getPeriodeSpe(self.projet.classe.specialite),
                                     totmax = ref.getNbrPeriodes(),
                                     projets = ref.projets)#wx.SL_AUTOTICKS |
        sb.Add(self.bmp, flag = wx.EXPAND|wx.TOP, border = 3)
        sb.Add(self.position, 1, flag = wx.EXPAND|wx.TOP, border = 3)
        
        pageGen.sizer.Add(sb, (1,0), flag = wx.EXPAND|wx.LEFT, border = 2)
#         self.Bind(wx.EVT_RADIOBUTTON, self.onChanged)
        self.Bind(wx.EVT_SLIDER, self.onChanged)
#        self.position.Bind(wx.EVT_RADIOBUTTON, self.onChanged)



        #
        # Organisation (nombre et positions des revues)
        #
        #   Dans MiseAJour()
        pageGen.sizer.AddGrowableRow(0)
        pageGen.sizer.AddGrowableCol(1)
        
        

    #############################################################################            
    def getBitmapPeriode(self, larg):
        return self.projet.getBitmapPeriode(larg)
#        print "getBitmapPeriode"       
        
         
    
    #############################################################################            
    def onChanged(self, event):
#         print("onChanged")#, event.GetSelection(), event.GetEventObject())
        self.projet.SetPosition(self.position.GetRange())
#         self.MiseAJourPosition()
#         self.SetBitmapPosition()
        self.MiseAJourTypeEnseignement()
        self.MiseAJour()
        event.Skip()
        self.sendEvent(modif = "Changement de position du Projet",
                       draw = True, verif = True)
        
        
    #############################################################################            
    def SetBitmapPosition(self, bougerSlider = None):
        try: # py3 : pas trouvé mieux pour éviter les MemoryError
            self.bmp.SetBitmap(self.getBitmapPeriode(250*SSCALE))
        except:
            pass

        
    #############################################################################            
    def EvtVariable(self, event):
        var = event.GetVar()
        if hasattr(self, 'nbrParties') and var == self.nbrParties:
            self.projet.nbrParties = var.v[0]
        elif var == self.annee:
            self.projet.annee = var.v[0]
            self.ctrlAnnee.unite.SetLabel(str(self.projet.annee+1)) 
        self.Refresh()
            
              
    #############################################################################            
    def EvtText(self, event):
        if event.GetEventObject() == self.textctrl:
#            nt = event.GetString()
            nt = self.textctrl.GetText()
#             print nt
#            if nt == u"":
#                nt = self.projet.support.nom
            self.projet.SetText(nt)
            #self.textctrl.ChangeValue(nt)
            maj = True
            #obj = 'intit'
            
        elif 'ORI' in self.pages and event.GetEventObject() == self.pages['ORI'][1]:
            self.projet.origine = self.pages['ORI'][1].GetText()
            maj = False
#             obj = 'ORI'
            
        elif 'CCF' in self.pages and event.GetEventObject() == self.pages['CCF'][1]:
            self.projet.contraintes = self.pages['CCF'][1].GetText()
            maj = False
#             obj = 'CCF'
            
        elif 'OBJ' in self.pages and event.GetEventObject() == self.pages['OBJ'][1]:
            self.projet.production = self.pages['OBJ'][1].GetText()
            maj = False
#             obj = 'OBJ'
            
        elif 'SYN' in self.pages and event.GetEventObject() == self.pages['SYN'][1]:
            self.projet.synoptique = self.pages['SYN'][1].GetText()
            maj = False
#             obj = 'SYN'
        
        elif hasattr(self, 'intctrl') and event.GetEventObject() == self.intctrl:
            self.projet.intituleParties = self.intctrl.GetText()
            maj = False
#             obj = 'intctrl'
        
        elif hasattr(self, 'enonctrl') and event.GetEventObject() == self.enonctrl:
            self.projet.besoinParties = self.enonctrl.GetText()
            maj = False
#             obj = 'enonctrl'
            
        elif event.GetEventObject() == self.commctrl:
            self.projet.SetProblematique(self.commctrl.GetText())
            maj = True
#             obj = 'commctrl'
            
        elif 'PAR' in self.parctrl and event.GetEventObject() == self.parctrl['PAR']:
            self.projet.partenariat = self.parctrl['PAR'].GetText()
            maj = False
#             obj = 'PAR'
            
        elif 'PRX' in self.parctrl and event.GetEventObject() == self.parctrl['PRX']:
            self.projet.montant = self.parctrl['PRX'].GetText()
            maj = False
#             obj = 'PRX'
            
        elif 'SRC' in self.parctrl and event.GetEventObject() == self.parctrl['SRC']:
            self.projet.src_finance = self.parctrl['SRC'].GetText()
            maj = False
#             obj = 'SRC'
        
#        else:
#            maj = False
            
#         print obj
        modif = "Modification des propriétés du Projet"
        if self.onUndoRedo():
            self.sendEvent(modif = modif, draw = True, verif = False)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, 
                             modif = modif,
                             draw = maj, verif = False)
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
#        print "typologie", self.projet.typologie
        
            
    #############################################################################            
    def MiseAJourTypeEnseignement(self, sendEvt = False, miseAJourPosition = True):
        """ Modifications structurelles
            après un changement d'enseignement
            ou de type de projet
        """
        prj = self.projet.GetProjetRef()
#        print "MiseAJourTypeEnseignement projet", ref.code
        doc = self.GetDocument()
        
        CloseFenHelp()
        
        if prj is None:
            return
        
        #
        # Page "Généralités"
        #
        self.titre.SetLabel(prj.attributs['TIT'][0])
        self.textctrl.MiseAJour(prj.attributs['TIT'][0], prj.attributs['TIT'][3])
        self.textctrl.SetToolTip("Titre, résumé, intitulé, description synthétique du projet")
        self.textctrl.SetTitre(prj.attributs['TIT'][0])
        
        self.tit_pb.SetLabel(prj.attributs['PB'][0])
        self.commctrl.MiseAJour(prj.attributs['PB'][0], prj.attributs['PB'][3])
        self.commctrl.SetToolTip(prj.attributs['PB'][1] + constantes.TIP_PB_LIMITE)
        self.commctrl.SetTitre(prj.attributs['PB'][0])
        
#         self.MiseAJourPosition()
        if miseAJourPosition:
            wx.CallLater(0, self.MiseAJourPosition) # py3 : pour éviter les MemoryError !!
        if hasattr(self, 'panelOrga'):
            self.panelOrga.MiseAJourListe()
        
        
        
        #
        # La page "sysML"
        #
        if 'SML' in prj.attributs and prj.attributs['SML'][0] != "":
            doc.UpdateSysML()
            if not 'SML' in self.pages:
                self.pages['SML'] = PanelPropriete(self.nb, objet = doc)
                bg_color = self.Parent.GetBackgroundColour()
                self.pages['SML'].SetBackgroundColour(bg_color)
                
                self.nb.AddPage(self.pages['SML'], prj.attributs['SML'][0])
                
             
                self.psysml = []
                for i, n in enumerate(prj.attributs['SML'][2]):
                    code = "SML"+str(i)
                    
                    sb = myStaticBox(self.pages['SML'], -1, n)
                    sbs = wx.StaticBoxSizer(sb, wx.VERTICAL)
                    self.psysml.append(Panel_Select_sysML(self.pages['SML'], doc, code))
                    sbs.Add(self.psysml[-1], flag = wx.EXPAND)
                    self.pages['SML'].sizer.Add(sbs, (0,i), flag = wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, border = 2)
                
                    
                self.pages['SML'].sizer.AddGrowableRow(0)
                
            else:
#                print "MiseAJour :", ref.attributs['SML'][1]
                if hasattr(self, 'intctrl'):
                    self.intctrl.MiseAJour("", prj.attributs['SML'][1])
                if hasattr(self, 'enonctrl'):
                    self.enonctrl.MiseAJour("", prj.attributs['SML'][3])
        else:
            if 'SML' in self.pages:
                self.nb.DeletePage(self.GetPageNum(self.pages['SML']))
                del self.pages['SML']
        
        
        
        


        
        
        
        
        #
        # Pages simples
        #
        for k in ['ORI', 'CCF', 'OBJ', 'SYN']:
            if prj.attributs[k][0] != "":
                if not k in self.pages:
                    self.pages[k] = self.creerPageSimple(self.EvtText,prj.attributs[k][0],  
                                                         prj.attributs[k][3])
                else:
                    self.pages[k][1].MiseAJour(prj.attributs[k][0], prj.attributs[k][3])
                self.nb.SetPageText(self.GetPageNum(self.pages[k][0]), prj.attributs[k][0])
                self.pages[k][1].SetToolTip(prj.attributs[k][1])
                self.pages[k][1].SetTitre(prj.attributs[k][0])
            
            else:
                if k in self.pages:
                    self.nb.DeletePage(self.GetPageNum(self.pages[k][0]))
                    del self.pages[k]
                
                    
        #
        # Pages spéciales
        #       
        
        # La page "sous parties" ('DEC')
        
        if prj.attributs['DEC'][0] != "":
            if not 'DEC' in self.pages:
                self.pages['DEC'] = PanelPropriete(self.nb, objet = self.GetDocument())
                bg_color = self.Parent.GetBackgroundColour()
                self.pages['DEC'].SetBackgroundColour(bg_color)
                
                self.nb.AddPage(self.pages['DEC'], prj.attributs['DEC'][0])
                
                self.nbrParties = Variable("Nombre de sous parties",  
                                           lstVal = self.projet.nbrParties, 
                                           typ = VAR_ENTIER_POS, bornes = [1,5])
                self.ctrlNbrParties = VariableCtrl(self.pages['DEC'], self.nbrParties, coef = 1, signeEgal = False,
                                        help = "Nombre de sous parties", sizeh = 30*SSCALE, scale = SSCALE)
                self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlNbrParties)
                self.pages['DEC'].sizer.Add(self.ctrlNbrParties, (0,0), flag = wx.EXPAND|wx.ALL, border = 2)
                
                titreInt = myStaticBox(self.pages['DEC'], -1, "Intitulés des différentes parties")
                sb = wx.StaticBoxSizer(titreInt)
                
                self.intctrl = TextCtrl_Help(self.pages['DEC'], "", prj.attributs['DEC'][1], scale = SSCALE)#, u"", style=wx.TE_MULTILINE)
                self.intctrl.SetTitre("Intitulés des différentes parties")
                self.intctrl.SetToolTip("Intitulés des parties du projet confiées à chaque groupe.\n" \
                                              "Les groupes %s sont désignés par des lettres (A, B, C, ...)\n" \
                                              "et leur effectif est indiqué." %self.projet.GetReferentiel().getLabel("ELEVES").de_plur_())
#                self.pages['DEC'].Bind(wx.EVT_TEXT, self.EvtText, self.intctrl)
#                 self.pages['DEC'].Bind(stc.EVT_STC_CHANGE, self.EvtText, self.intctrl)
                self.pages['DEC'].Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.intctrl)
                sb.Add(self.intctrl, 1, flag = wx.EXPAND)
                self.pages['DEC'].sizer.Add(sb, (1,0), flag = wx.EXPAND|wx.ALL, border = 2)
                
                titreInt = myStaticBox(self.pages['DEC'], -1, "Énoncés du besoin des différentes parties du projet")
                sb = wx.StaticBoxSizer(titreInt)
                self.enonctrl = TextCtrl_Help(self.pages['DEC'], "", prj.attributs['DEC'][3], scale = SSCALE)#, u"", style=wx.TE_MULTILINE)       
                self.enonctrl.SetToolTip("Énoncés du besoin des parties du projet confiées à chaque groupe")
                self.enonctrl.SetTitre("Énoncés du besoin des différentes parties du projet")
        
#                self.pages['DEC'].Bind(wx.EVT_TEXT, self.EvtText, self.enonctrl)
#                 self.pages['DEC'].Bind(stc.EVT_STC_CHANGE, self.EvtText, self.enonctrl)
                self.pages['DEC'].Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.enonctrl)
                sb.Add(self.enonctrl, 1, flag = wx.EXPAND)
                self.pages['DEC'].sizer.Add(sb, (0,1), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)
                
                self.pages['DEC'].sizer.AddGrowableCol(1)
                self.pages['DEC'].sizer.AddGrowableRow(1)  
                self.pages['DEC'].sizer.Layout()
            else:
#                print "MiseAJour :", ref.attributs['DEC'][1]
                self.intctrl.MiseAJour("", prj.attributs['DEC'][1])
                self.enonctrl.MiseAJour("", prj.attributs['DEC'][3])
        else:
            if 'DEC' in self.pages:
                self.nb.DeletePage(self.GetPageNum(self.pages['DEC']))
                del self.pages['DEC']
        
        
        # La page "typologie" ('TYP') : cases à cocher
        
        if prj.attributs['TYP'][0] != "":
            if not 'TYP' in self.pages:
                self.pages['TYP'] = PanelPropriete(self.nb, objet = self.GetDocument())
                bg_color = self.Parent.GetBackgroundColour()
                self.pages['TYP'].SetBackgroundColour(bg_color)
                
                self.nb.AddPage(self.pages['TYP'], prj.attributs['TYP'][0])
                
                lab = prj.attributs['TYP'][2].replace("\n\n", "\n")
                liste = lab.split("\n")
                self.lb = wx.CheckListBox(self.pages['TYP'], -1, (80*SSCALE, 50*SSCALE), wx.DefaultSize, liste)
                self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.lb)
                
                self.pages['TYP'].sizer.Add(self.lb, (0,0), flag = wx.EXPAND|wx.ALL, border = 2)
                
                self.pages['TYP'].sizer.AddGrowableCol(0)
                self.pages['TYP'].sizer.AddGrowableRow(0)  
                self.pages['TYP'].sizer.Layout()
                
        else:
            if 'TYP' in self.pages:
                self.nb.DeletePage(self.GetPageNum(self.pages['TYP']))
                del self.pages['TYP']
        
        # La page "Partenariat" ('PAR')
#        print "xxx ", ref.attributs
        if prj.attributs['PAR'][0] != "":
            if not 'PAR' in self.pages:
                self.parctrl = {}
                self.pages['PAR'] = PanelPropriete(self.nb, objet = self.GetDocument())
                bg_color = self.Parent.GetBackgroundColour()
                self.pages['PAR'].SetBackgroundColour(bg_color)
                
                self.nb.AddPage(self.pages['PAR'], prj.attributs['PAR'][0])
                
                for i, k in enumerate(['PAR', 'PRX', 'SRC']):
                    titreInt = myStaticBox(self.pages['PAR'], -1, prj.attributs[k][0])
                    sb = wx.StaticBoxSizer(titreInt)
                
                    self.parctrl[k] = orthographe.STC_ortho(self.pages['PAR'], -1)#, u"", style=wx.TE_MULTILINE)
                    
                    self.parctrl[k].SetTitre(prj.attributs['PAR'][0])

                    self.parctrl[k].SetToolTip(prj.attributs[k][1])
#                    self.pages['PAR'].Bind(wx.EVT_TEXT, self.EvtText, self.parctrl[k])
#                     self.pages['PAR'].Bind(stc.EVT_STC_CHANGE, self.EvtText, self.parctrl[k])
                    self.pages['PAR'].Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.parctrl[k])
                    sb.Add(self.parctrl[k], 1, flag = wx.EXPAND)
                    self.pages['PAR'].sizer.Add(sb, (0,i), flag = wx.EXPAND|wx.ALL, border = 2)
                
                self.pages['PAR'].sizer.AddGrowableCol(0)
                self.pages['PAR'].sizer.AddGrowableRow(0)  
                self.pages['PAR'].sizer.Layout()
                
        else:
            if 'PAR' in self.pages:
                self.nb.DeletePage(self.GetPageNum(self.pages['PAR']))
                del self.pages['PAR']
                self.parctrl = {}
    
    
    #############################################################################            
    def MiseAJourPosition(self, sendEvt = False):
        self.SetBitmapPosition()
#         self.bmp.SetBitmap(self.getBitmapPeriode(250*SSCALE))
#         self.bmp.Render()
##        self.position.SetRange(0, self.projet.GetLastPosition())
        self.position.SetValue(self.projet.position)
    

    #############################################################################            
    def MiseAJour(self, sendEvt = False, marquerModifier = True):
#         print("MiseAJour Projet", sendEvt)

        prj = self.projet.GetProjetRef()
        ref = self.projet.GetReferentiel()
        
        # La page "Généralités"
        self.textctrl.SetValue(self.projet.intitule, False)
        self.commctrl.SetValue(self.projet.problematique, False)

        # Les pages simples
        if 'ORI' in self.pages:
            self.pages['ORI'][1].SetValue(self.projet.origine, False)
        if 'CCF' in self.pages:
            self.pages['CCF'][1].SetValue(self.projet.contraintes, False)
        if 'OBJ' in self.pages:
            self.pages['OBJ'][1].SetValue(self.projet.production, False)
        if 'SYN' in self.pages:
            self.pages['SYN'][1].SetValue(self.projet.synoptique, False)
        
        # La page "typologie" ('TYP')
        if prj is not None and prj.attributs['TYP'][0] != "":
            for t in self.projet.typologie:
                self.lb.Check(t)
                
        # La page "sous parties" ('DEC')
        if prj is not None and prj.attributs['DEC'][0] != "":
            self.intctrl.SetValue(self.projet.intituleParties, False)
            self.enonctrl.SetValue(self.projet.besoinParties, False)
            self.nbrParties.v[0] = self.projet.nbrParties
            self.ctrlNbrParties.mofifierValeursSsEvt()
        
        # La page "Partenariat" ('PAR')
        if prj is not None and prj.attributs['PAR'][0] != "" and hasattr(self, 'parctrl'):
            self.parctrl['PAR'].SetValue(self.projet.partenariat, False)
            self.parctrl['PRX'].SetValue(self.projet.montant, False)
            self.parctrl['SRC'].SetValue(self.projet.src_finance, False)
                    
        self.MiseAJourPosition()
        
#         print("code", self.projet.code)
        if not hasattr(self, 'panelOrga') and self.projet.code in ref.projets:
            self.panelOrga = PanelOrganisation(self.pageGen, self, self.projet)
            self.pageGen.sizer.Add(self.panelOrga, (0,2), (2,1), flag = wx.EXPAND|wx.LEFT, border = 2)
        else:
            # Pas d'évaluation = pas de revues
            if hasattr(self, 'panelOrga'):
                try:
                    self.pageGen.sizer.Detach(self.panelOrga)
                except:
                    pass
                self.panelOrga.Destroy()
                del self.panelOrga
                
        if hasattr(self, 'panelOrga'):
            self.panelOrga.MiseAJourListe()
        
        if 'SML' in self.pages:
            for s in self.psysml:
                s.MiseAJour()
                
                
        self.pageGen.Layout()
        self.Layout()
        
        if sendEvt:
            self.sendEvent(draw = True, verif = True)


    ######################################################################################  
    def Verrouiller(self, etat):
        self.position.Enable(etat)
        




class PositionCtrl(wx.Panel):
    def __init__(self, parent, position, periodes, totmax = None, projets = {}):
        wx.Panel.__init__(self, parent, -1)
        self.position = position
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        
#         projets = [[x-1 for x in p.periode] for p in projets.values()]
        projets = [[p.periode[0]-1, p.periode[-1]] for p in projets.values()]
#         print("projets", projets)
        mini, maxi = periodes[0], periodes[-1]#0, sum(p[1] for p in periodes)-1
        if totmax == None:
            totmax = maxi+1
            
        self.sel = RangeSlider(self, -1, lowValue=position[0], highValue=position[1]+1, 
                               minValue=mini, maxValue=maxi+1, minDelta = 1, zones = projets, 
                               size = (-1, 18*SSCALE))
        
#         w1, w2, w3 = 100*mini/totmax, 100*(maxi-mini+1)/totmax, 100*(totmax-maxi-1)/totmax
        self.sizer.AddStretchSpacer(100*mini/totmax)
        self.sizer.Add(self.sel, 100*(maxi-mini+1)/totmax  , flag = wx.EXPAND)
        self.sizer.AddStretchSpacer(100*(totmax-maxi-1)/totmax)
        
        self.SetSizer(self.sizer)
#         self.sel.Bind(wx.EVT_SLIDER, self.OnSlide)
#         
#         
#         
#     def OnSlide(self, event):
# #         print("OnSlide")
#         wx.PostEvent(self.Parent, event)
#         event.Skip()
#         

    def SetValue(self, pos):
        
        self.sel.SetValues(pos[0], pos[1]+1)
        
    
    def GetRange(self):
        p = self.sel.GetValues()
        return [p[0], p[1]-1]
        
        
    def MiseAJour(self, position = None):
        if position is not None:
            self.position = position
        self.SetValue(self.position)
        


class CreneauCtrl(wx.Panel):
    def __init__(self, parent, creneaux):
        wx.Panel.__init__(self, parent, -1)
        self.creneaux = creneaux
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.cb = []
        for creneau in range(self.GetDocument().nbrCreneaux):
            cb = wx.CheckBox(self, 110+creneau, "")
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
            self.sizer.Add(cb, 1, flag = wx.EXPAND)
            self.cb.append(cb)
            
        self.SetSizer(self.sizer)

        return

    def Verif(self):
        lst = [c.IsChecked() for c in self.cb]
        if sum(lst) == 1:
            self.cb[lst.index(1)].Enable(False)
        else:
            for cb in self.cb:
                cb.Enable(True)
            

            
    def GetDocument(self):
        return self.Parent.GetDocument()
    
    
    def SetCreneaux(self):
        lst = [c.IsChecked() for c in self.cb]
        self.creneaux[0] = lst.index(True)
        lst.reverse()
        self.creneaux[1] = self.GetDocument().nbrCreneaux-lst.index(True)-1
        
            
        
    def EvtCheckBox(self, event):
        self.Verif()
        self.SetCreneaux()
        self.MiseAJour()
        self.Parent.OnChangeCreneau()
        

    
    def GetRange(self):
        return self.sel.GetRange()
        
        
    def MiseAJour(self):
        for i, cb in enumerate(self.cb):
            cb.SetValue(self.creneaux[0] <= i <= self.creneaux[1])

####################################################################################
#
#   Classe définissant le panel de propriété de la progression
#
####################################################################################
class PanelPropriete_Progression(PanelPropriete):
    def __init__(self, parent, progression):
        self.progression = progression
        PanelPropriete.__init__(self, parent, objet = self.progression)
        
        
        
        self.nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
        
        self.construire()
        
        self.sizer.Add(self.nb, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
#        self.sizer.Layout()
        
        self.Layout()
        self.FitInside()
        
        self.MiseAJourTypeEnseignement()
        self.MiseAJour()
        
        self.Show()
        
#        self.Fit()
        
    #############################################################################            
    def GetDocument(self):
        return self.progression
    
    
    ######################################################################################  
    def OnPathModified(self, lien, marquerModifier = True):
#         print "OnPathModified", self.progression.lien
        self.progression.OnPathModified()
#         self.btnlien.Show(self.progression.lien.path != "")
        self.selec.MiseAJour()
        if marquerModifier:
            self.progression.GetApp().MarquerFichierCourantModifie()
        self.pageGen.Layout()
        self.pageGen.Refresh()
        
    #############################################################################            
    def construire(self):
        self.pages = {}
        
        #
        # La page "Généralités"
        #
        pageGen = PanelPropriete(self.nb, panelRacine = self, objet = self.GetDocument())
        bg_color = self.Parent.GetBackgroundColour()
        pageGen.SetBackgroundColour(bg_color)
        self.pageGen = pageGen
        self.nb.AddPage(pageGen, "Propriétés générales")


        #
        # Intitulé de la progression (TIT)
        #
        self.titre = myStaticBox(pageGen, -1, "Intitulé de la Progression")
        sb = wx.StaticBoxSizer(self.titre)
        textctrl = TextCtrl_Help(pageGen, "", scale = SSCALE)
        textctrl.SetTitre("Intitulé de la Progression", self.progression.getIcone())
        textctrl.SetToolTip("")
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        pageGen.sizer.Add(sb, (0,0), (1,2),  flag = wx.ALL|wx.EXPAND, border = 2)
#        pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText)
#        pageGen.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
#         pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.textctrl)
        pageGen.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.textctrl)
       
        
        
        
        #
        # Année scolaire et Position dans l'année
        #
        titre = myStaticBox(pageGen, -1, "Année et Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        
        self.annee = Variable("Année scolaire", lstVal = self.GetDocument().calendrier.annee, 
                                   typ = VAR_ENTIER_POS, bornes = [2012,2100])
        self.ctrlAnnee = VariableCtrl(pageGen, self.annee, coef = 1, signeEgal = False,
                                      help = "Année scolaire", sizeh = 40*SSCALE, 
                                      unite = str(self.GetDocument().calendrier.GetAnneeFin()),
                                      sliderAGauche = True, scale = SSCALE)
        self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlAnnee)
        sb.Add(self.ctrlAnnee)
        pageGen.sizer.Add(sb, (1,0), flag = wx.ALIGN_CENTER_VERTICAL |wx.EXPAND|wx.ALL, border = 2)
        
        
        #
        # Nombre de créneaux horaires
        #
        titre = myStaticBox(pageGen, -1, "Créneaux horaire")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        
        self.nbrCreneaux = Variable("Nombre de créneaux", lstVal = self.GetDocument().nbrCreneaux, 
                                   typ = VAR_ENTIER_POS, bornes = [self.GetDocument().GetNbrCreneauxMini(),5])
        self.ctrlCreneaux = VariableCtrl(pageGen, self.nbrCreneaux, coef = 1, signeEgal = False,
                                      help = "Nombre de créneaux horaires\nLa valeur mini est fixée\npar les séquences ou projets déjà définis", sizeh = 40*SSCALE, 
                                      sliderAGauche = True, scale = SSCALE)
        self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlCreneaux)
        sb.Add(self.ctrlCreneaux)
        pageGen.sizer.Add(sb, (1,1), flag = wx.ALIGN_CENTER_VERTICAL |wx.EXPAND|wx.ALL, border = 2)
        
        
        #
        # Mode
        #
        ref = self.GetDocument().GetReferentiel()
        dic = ref.getDicToutesCompetences()
        c = dic["S"]._nom.Plur_()
        dic = ref.getDicTousSavoirs()
        s = dic["S"]._nom.Plur_()
        self.mdbox = wx.RadioBox(pageGen, -1, "Mode d'affichage",
                                 majorDimension = 1, style = wx.RA_SPECIFY_COLS,
                                 choices = [c, s])
        
        self.Bind(wx.EVT_RADIOBOX, self.EvtMode)
        pageGen.sizer.Add(self.mdbox, (0,2), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        
        
        
        #
        # Lien
        #
        lsizer = self.CreateLienSelect(pageGen)
        pageGen.sizer.Add(lsizer, (2,0), (1, 3), flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        #
        # Image
        #
        isizer = self.CreateImageSelect(pageGen)
        pageGen.sizer.Add(isizer, (0,3), (3,1), flag =  wx.EXPAND|wx.ALL, border = 2)#wx.ALIGN_CENTER_VERTICAL |



        pageGen.sizer.AddGrowableCol(0)
        pageGen.sizer.AddGrowableRow(0)
        

        
    #############################################################################            
    def MiseAJourTypeEnseignement(self, sendEvt = False):
        
        CloseFenHelp()
        
        #
        # Page "Généralités"
        #
#        self.titre.SetLabel()
#        self.textctrl.MiseAJour(self.GetDocument().intitule)
   

        
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#         print("MiseAJour Progression", sendEvt)

        
        # La page "Généralités"
        self.textctrl.SetValue(self.GetDocument().intitule, False)
        
        self.mdbox.SetSelection(self.progression.GetModeInt())
        
        self.Layout()
        
        if sendEvt:
            self.sendEvent(draw = True, verif = True)

    
#     #############################################################################            
#     def SetImage(self):
#         if self.progression.image != None:
#             
# #             self.progression.image = rognerImage(self.progression.image)
#             
# #             w, h = self.progression.image.GetSize()
# #             wf, hf = 200.0, 100.0
# #             r = max(w/wf, h/hf)
# #             _w, _h = w/r, h/r
# #             self.progression.image = self.progression.image.ConvertToImage().Scale(_w, _h).ConvertToBitmap()
#             self.image.SetBitmap(rognerImage(self.progression.image, 200,200))
#         self.pageGen.Layout()
        
#     #############################################################################            
#     def OnClickLien(self, event):
#         self.progression.lien.Afficher(self.GetDocument().GetPath())
        
#     #############################################################################            
#     def OnClick(self, event):
#         mesFormats = u"Fichier Image|*.bmp;*.png;*.jpg;*.jpeg;*.gif;*.pcx;*.pnm;*.tif;*.tiff;*.tga;*.iff;*.xpm;*.ico;*.ico;*.cur;*.ani|" \
#                        u"Tous les fichiers|*.*'"
#         
#         dlg = wx.FileDialog(
#                             self, message=u"Ouvrir une image",
# #                            defaultDir = self.DossierSauvegarde, 
#                             defaultFile = "",
#                             wildcard = mesFormats,
#                             style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
#                             )
#             
#         # Show the dialog and retrieve the user response. If it is the OK response, 
#         # process the data.
#         if dlg.ShowModal() == wx.ID_OK:
#             # This returns a Python list of files that were selected.
#             paths = dlg.GetPaths()
#             nomFichier = paths[0]
#             self.progression.image = rognerImage(wx.Image(nomFichier).ConvertToBitmap())
#             self.SetImage()
#             self.sendEvent(modif = u"Modification de l'image de la Progression")
#             
#         dlg.Destroy()
    
    #############################################################################            
    def EvtMode(self, event):
        self.progression.SetMode(self.mdbox.GetSelection())
        self.sendEvent(modif = "Modification du mode d'affichage de la Progresion", 
                       draw = True, verif = False)
    
    
    #############################################################################            
    def EvtText(self, event):
#        print "EvtText",
        if event.GetEventObject() == self.textctrl:
#            nt = event.GetString()
            nt = self.textctrl.GetText()
#            if nt == u"":
#                nt = self.projet.support.nom
            self.GetDocument().SetText(nt)
            self.textctrl.ChangeValue(nt)
            maj = True
#             obj = 'intit'
        

        modif = "Modification des propriétés de la Progression"
        if self.onUndoRedo():
            self.sendEvent(modif = modif, draw = True, verif = False)
        else:
            if not self.eventAttente:
#                print "   modif", obj
                wx.CallLater(DELAY, self.sendEvent, 
                             modif = modif,
                             draw = maj, verif = False)
                self.eventAttente = True
    
    
    
    #############################################################################            
    def EvtVariable(self, event):
        var = event.GetVar()
        if var == self.annee:
            cal = self.GetDocument().calendrier
            cal.annee = var.v[0]
            self.ctrlAnnee.unite.SetLabel(str(cal.annee + cal.GetNbrAnnees())) 
            
            modif = "Modification de l'année scolaire de la Progression"
            self.sendEvent(modif = modif, draw = True, verif = True)
            
        elif var == self.nbrCreneaux:
            
            if self.GetDocument().SetNbrCreneaux(var.v[0]):
                modif = "Modification du nombre de creneaux de la Progression"
                self.sendEvent(modif = modif, draw = True, verif = True)
            else:
                self.nbrCreneaux.setValeur(var.v[0]+1)
            
        self.Refresh()
        
    
    
    
        
    
    
###################################################################################################
class PanelOrganisation(wx.Panel):    
    def __init__(self, parent, panel, objet):
#         print("PanelOrganisation", objet.getNbrRevues())
        wx.Panel.__init__(self, parent, -1)
        self.objet = objet
        self.parent = panel
        
        bsize = (20*SSCALE, 20*SSCALE)
        sizer = wx.BoxSizer()
        gbsizer = wx.GridBagSizer()
        titre = myStaticBox(self, -1, "Organisation")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        
        self.nbrRevues = Variable("Nombre de revues",  
                                   lstVal = self.objet.getNbrRevues(), 
                                   typ = VAR_ENTIER_POS,
                                   bornes = [2,3])
        self.ctrlNbrRevues = VariableCtrl(self, self.nbrRevues, coef = 1, signeEgal = False,
                                help = "Nombre de revues de projet (avec évaluation)", sizeh = 30*SSCALE, scale = SSCALE)
        self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlNbrRevues)
        gbsizer.Add(self.ctrlNbrRevues, (0,0), (1,2), flag = wx.EXPAND)
        
        liste = wx.ListBox(self, -1, choices = self.objet.GetListeNomsPhases(), style = wx.LB_SINGLE)
        liste.SetToolTip("Séléctionner la revue à déplacer")
        gbsizer.Add(liste, (1,0), (2,1), flag = wx.EXPAND)
        self.liste = liste
        self.Bind(wx.EVT_LISTBOX, self.EvtListBox, self.liste)
        
#         buttonUp = wx.BitmapButton(self, 11, wx.ArtProvider.GetBitmap(wx.ART_GO_UP), size = bsize)
        buttonUp = wx.BitmapButton(self, 11, scaleImage(images.go_up.GetBitmap(), *bsize))
        gbsizer.Add(buttonUp, (1,1), (1,1))
        self.Bind(wx.EVT_BUTTON, self.OnClick, buttonUp)
        buttonUp.SetToolTip("Monter la revue")
        self.buttonUp = buttonUp
        
#         buttonDown = wx.BitmapButton(self, 12, wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN), size = bsize)
        buttonDown = wx.BitmapButton(self, 12, scaleImage(images.go_down.GetBitmap(), *bsize))
        gbsizer.Add(buttonDown, (2,1), (1,1))
        self.Bind(wx.EVT_BUTTON, self.OnClick, buttonDown)
        buttonDown.SetToolTip("Descendre la revue")
        self.buttonDown = buttonDown
        
        gbsizer.AddGrowableRow(1)
        sb.Add(gbsizer, flag = wx.EXPAND)
        
        sizer.Add(sb, flag = wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
        
    
        
        
    #############################################################################            
    def EvtListBox(self, event):
        ref = self.objet.GetProjetRef()
        if ref is None:
            return
        if ref.getClefDic('phases', self.liste.GetString(event.GetSelection()), 0) in TOUTES_REVUES_EVAL:
            self.buttonUp.Enable(True)
            self.buttonDown.Enable(True)
        else:
            self.buttonUp.Enable(False)
            self.buttonDown.Enable(False)
            
            
        
    #############################################################################            
    def OnClick(self, event):
        """ Déplacement de la revue sélectionnée
            vers le haut ou vers le bas
        """
     
        revue = self.liste.GetStringSelection()
        prj = self.objet.GetProjetRef()
        if prj is None or revue[:5] != "Revue":
            return
        
        i = event.GetId()
        
        posRevue = self.liste.GetSelection()
        numRevue = eval(revue[-1])

#         print("OnClick", numRevue, posRevue)
        if i == 11 and posRevue-2 >= 0:
            nouvPosRevue = posRevue-2   # Montée
            monte = True
            
        elif i == 12 and posRevue < self.liste.GetCount() - 1:
            nouvPosRevue = posRevue+1   # Descente
            monte = False
            
        else: 
            return
#            print posRevue, ">>", nouvPosRevue, self.liste.GetString(nouvPosRevue), toSystemEncoding(self.liste.GetString(nouvPosRevue))
        itemPrecedent = prj.getClefDic('phases', self.liste.GetString(nouvPosRevue).lstrip(), 0)
        
#            itemPrecedent = constantes.getCodeNomCourt(self.liste.'(nouvPosRevue), 
#                                                       self.objet.GetTypeEnseignement(simple = True))
        j=1
        while itemPrecedent in TOUTES_REVUES_EVAL:
            itemPrecedent = prj.getClefDic('phases', self.liste.GetString(nouvPosRevue-j).lstrip(), 0)
#                itemPrecedent = constantes.getCodeNomCourt(self.liste.GetString(nouvPosRevue-j),
#                                                           self.objet.GetTypeEnseignement(simple = True))
            j += 1
#         print("  itemPrecedent", itemPrecedent)
        if itemPrecedent is None:
            return
        self.objet.positionRevues[numRevue-1] = itemPrecedent
          
        self.MiseAJourListe()
        
        self.liste.SetStringSelection(revue)
        if hasattr(self.objet, 'OrdonnerTaches'):
            self.objet.OrdonnerTaches()
            if monte:
                self.objet.VerifierIndicRevue(numRevue)
            self.parent.sendEvent(modif = "Déplacement de la revue",
                                  draw = True, verif = True)
        
    #############################################################################            
    def MiseAJourListe(self):
#         print("MiseAJourListe", self.objet.getNbrRevues())
#        print self.objet.GetListeNomsPhases()
        prj = self.objet.GetProjetRef()
        if prj is None:
            return
#         print("MiseAJourListe", prj.posRevues)
        
        mini, maxi = min(prj.posRevues.keys()), max(prj.posRevues.keys())
        self.ctrlNbrRevues.redefBornes([mini, maxi])
        self.ctrlNbrRevues.setValeur(self.objet.getNbrRevues())
        self.ctrlNbrRevues.Show(mini != maxi)
#         self.ctrlNbrRevues.setValeur(prj.getNbrRevuesDefaut())
        self.liste.Set(self.objet.GetListeNomsPhases())
        self.Layout()


    #############################################################################            
    def EvtVariable(self, event):
        
        var = event.GetVar()
        print("EvtVariable NbrRevues", var.v[0])
        if var == self.nbrRevues:
            if var.v[0] != self.objet.getNbrRevues():
                self.objet.setNbrRevues(var.v[0])
                self.objet.MiseAJourNbrRevues()
                self.MiseAJourListe()
                self.parent.sendEvent(modif = "Modification du nombre de revues",
                                      draw = True, verif = True)



####################################################################################
#
#   Classe définissant le panel de propriété de la classe
#
####################################################################################
class PanelPropriete_Classe(PanelPropriete):
    def __init__(self, parent, classe, ouverture = False, typedoc = ''):
        self.classe = classe
#        print "__init__ PanelPropriete_Classe"
        PanelPropriete.__init__(self, parent, objet = self.classe)
#        self.BeginRepositioningChildren()
        self.SetupScrolling(scroll_x = False, scroll_y = False)
        
        ref = self.classe.GetReferentiel()
        bg_color = self.Parent.GetBackgroundColour()
        
        nb = wx.Notebook(self, -1,  style= wx.BK_DEFAULT)
        self.nb = nb
        
        #
        # La page "Généralités"
        #
        pageGen = PanelPropriete(nb, objet = classe)
        pageGen.SetBackgroundColour(bg_color)
        self.pageGen = pageGen
        nb.AddPage(pageGen, "Propriétés générales")


        #
        # la page "Découpage de la classe"
        #
        pageDec = PanelPropriete(nb, objet = classe)
        pageDec.SetBackgroundColour(bg_color)
        nb.AddPage(pageDec, "Découpage de la classe")
        self.pageDec = pageDec
        
        
        #
        # la page "Systèmes"
        #
        pageSys = PanelPropriete(nb, objet = classe)
        pageSys.SetBackgroundColour(bg_color)
        self.pageSys = pageSys
        nb.AddPage(pageSys, ref._nomSystemes.Plur_())

        
        


        #
        # La barre d'outils
        #
        self.tb = tb = wx.ToolBar(self, style = wx.TB_VERTICAL|wx.TB_FLAT|wx.TB_NODIVIDER)
        self.sizer.Add(tb, (0,0), flag = wx.ALL, border = 1)
        t = "Sauvegarder ces paramètres de classe dans un fichier :\n" \
            " - type d'enseignement\n" \
            " - effectifs\n" \
            " - établissement\n"
        if typedoc == 'seq':
            t += " - "+ref.nomSystemes+"\n"
        elif typedoc == 'prj':
            t += " - nombre de revues et positions\n"
    
        tsize = (IMG_SIZE_TB[0]*SSCALE, IMG_SIZE_TB[1]*SSCALE)
        open_bmp = scaleImage(images.Icone_open.GetBitmap(), *tsize)
        save_bmp =  scaleImage(images.Icone_save.GetBitmap(), *tsize)
        pref_bmp = scaleImage(images.Icone_defaut_pref.GetBitmap(), *tsize)
#         open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
#         save_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        
        tb.AddTool(30, u"Ouvrir un fichier classe", open_bmp)
        self.Bind(wx.EVT_TOOL, self.commandeOuvrir, id=30)
        
        tb.AddTool(32, t, save_bmp)
        self.Bind(wx.EVT_TOOL, self.commandeSauve, id=32)
        
        tb.AddTool(31, u"Rétablir les paramètres de classe par défaut",
                         pref_bmp)
        
        self.Bind(wx.EVT_TOOL, self.OnDefautPref, id=31)

        tb.Realize()

        self.sizer.Add(nb, (0,1), flag = wx.ALL|wx.EXPAND, border = 1)
        self.sizer.AddGrowableCol(1)
        self.sizer.AddGrowableRow(0)
        
        
        #
        # Type d'enseignement
        #
        self.pourProjet = self.GetDocument().estProjet()
        titre = myStaticBox(pageGen, -1, "Type d'enseignement")
        titre.SetMinSize((180*SSCALE, 100*SSCALE))
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        self.sel_type = Panel_SelectEnseignement(pageGen, self, self.pourProjet, self.classe)
        sb.Add(self.sel_type, 1, flag = wx.EXPAND)

        pageGen.sizer.Add(sb, (0,0), flag = wx.EXPAND|wx.ALL, border = 2)#


        #
        # Etablissement
        #
        titre = myStaticBox(pageGen, -1, "Établissement")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        
        sh = wx.BoxSizer(wx.HORIZONTAL)
        t = wx.StaticText(pageGen, -1, "Académie :")
        sh.Add(t, flag = wx.ALIGN_CENTER_VERTICAL)
        
        lstAcad = sorted([a[0] for a in constantes.ETABLISSEMENTS.values()])
        self.cba = wx.ComboBox(pageGen, -1, "sélectionner une académie ...", (-1,-1), 
                         (-1, -1), lstAcad+[""],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboAcad, self.cba)
#         pageGen.Bind(wx.EVT_TEXT, self.EvtComboAcad, self.cba)
        sh.Add(self.cba, flag = wx.EXPAND|wx.LEFT, border = 5)
        sb.Add(sh, flag = wx.EXPAND|wx.BOTTOM, border = 5)
        
        ##############################################
        sh = wx.BoxSizer(wx.HORIZONTAL)
        t = wx.StaticText(pageGen, -1, "Ville :")
        sh.Add(t, flag = wx.ALIGN_CENTER_VERTICAL)
     
        self.cbv = SlimSelector(pageGen, -1, "sélectionner une ville ...", (-1,-1), 
                         (-1, -1), [],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboVille, self.cbv)
        pageGen.Bind(wx.EVT_TEXT, self.EvtComboVille, self.cbv)
        sh.Add(self.cbv, 1,flag = wx.ALIGN_CENTER_VERTICAL|LEFT, border = 5)
        sb.Add(sh, flag = wx.EXPAND|wx.BOTTOM, border = 5)
        
        t = wx.StaticText(pageGen, -1, "Établissement :")
        sb.Add(t, flag = wx.EXPAND|wx.BOTTOM, border = 5)
        
        self.cbe = wx.ComboBox(pageGen, -1, "sélectionner un établissement ...", (-1,-1), 
                         (-1, -1), ["autre ..."],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboEtab, self.cbe)
        sb.Add(self.cbe, flag = wx.EXPAND|wx.BOTTOM, border = 2)
        
#        textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
#        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
##        textctrl.SetMinSize((-1, 150))
#        sb.Add(textctrl, 1, flag = wx.EXPAND)
#        self.textctrl = textctrl
        
#        self.info = wx.StaticText(self, -1, u"""Inscrire le nom de l'établissement dans le champ ci-dessus...
#        ou bien modifier le fichier "etablissements.txt"\n        pour le faire apparaitre dans la liste.""")
#        self.info.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.NORMAL))
#        sb.Add(self.info, 0, flag = wx.EXPAND|wx.ALL, border = 5)

        pageGen.sizer.Add(sb, (0,1), flag = wx.ALL|wx.EXPAND, border = 2)
        
        #
        # Accés au BO
        #
        titre = myStaticBox(pageGen, -1, "Documents Officiels en ligne")
        self.bo = []
        sbBO = wx.StaticBoxSizer(titre, wx.VERTICAL)
        pageGen.sizer.Add(sbBO, (0,2), flag = wx.ALL|wx.EXPAND, border = 2)
        self.sbBO = sbBO
#        self.SetLienBO()
        
        # Bouton "télécharger"
        btn_bo = wx.Button(pageGen, -1, "Télécharger")
        btn_bo.SetToolTip("Télécharger l'ensemble des documents officiels pour y accéder via l'onglet \"Bulletins Officiels\"")
        pageGen.Bind(wx.EVT_BUTTON, self.EvtBnt_BO, btn_bo)
        self.sbBO.Add(btn_bo, flag = wx.EXPAND)
        
#         pageGen.sizer.Add(10, 1, (0,3))
        pageGen.sizer.AddGrowableRow(0)
        pageGen.sizer.AddGrowableCol(1)
        
        
        #
        # Effectifs
        #
        self.ec = PanelEffectifsClasse(pageDec, classe)
        
        pageDec.sizer.Add(self.ec, (0,0), flag = wx.ALL|wx.EXPAND, border = 2)

        pageDec.sizer.AddGrowableRow(0)
        pageDec.sizer.AddGrowableCol(0)
#        pageGen.sizer.Layout()




        #####################################################################
        # Systèmes
        #
        self.btnAjouterSys = wx.Button(pageSys, -1, "Ajouter")
        self.btnAjouterSys.SetToolTip("Ajouter %s à la liste" %et2ou(ref._nomSystemes.un_("nouveau")))
        self.Bind(wx.EVT_BUTTON, self.EvtButtonSyst, self.btnAjouterSys)
        
        self.lstSys = wx.ListBox(pageSys, -1,
                                 choices = [""], style = wx.LB_SINGLE)# | wx.LB_SORT)
        self.Bind(wx.EVT_LISTBOX, self.EvtListBoxSyst, self.lstSys)
        
        self.btnSupprimerSys = wx.Button(pageSys, -1, "Supprimer")
        self.btnSupprimerSys.SetToolTip("Supprimer %s de la liste" %et2ou(ref._nomSystemes.le_()))
        self.Bind(wx.EVT_BUTTON, self.EvtButtonSupprSyst, self.btnSupprimerSys)
        
        s = pysequence.Systeme(self.classe)
        self.panelSys = s.GetPanelPropriete(pageSys)
        self.panelSys.Show()
    
        vs = wx.BoxSizer(wx.VERTICAL)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        
        vs.Add(self.lstSys, 1, flag = wx.ALL|wx.EXPAND, border = 2)
        vs.Add(hs, flag = wx.ALL|wx.EXPAND, border = 2)
        
        hs.Add(self.btnAjouterSys, flag = wx.ALL|wx.EXPAND, border = 2)
        hs.Add(self.btnSupprimerSys, flag = wx.ALL|wx.EXPAND, border = 2)
        
        pageSys.sizer.Add(vs, (0,0), flag = wx.ALL|wx.EXPAND, border = 2)
        
        pageSys.sizer.Add(self.panelSys, (0,1), flag = wx.ALL|wx.EXPAND, border = 2)
        pageSys.sizer.AddGrowableRow(0)
        pageSys.sizer.AddGrowableCol(1)
    
        self.MiseAJour()
        self.Verrouiller()
        self.MiseAJourBoutonsSystem()
        
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.ec.Onsize)
        
        
        self.Layout()
        
        
        
    ######################################################################################              
    def OnResize(self, evt = None):
#         self.Layout()
#         self.nb.SetMinSize((-1,self.GetClientSize()[1]))
        
        if evt:
            evt.Skip()
    

    
    
    
    ###############################################################################################
    def commandeOuvrir(self, event = None, nomFichier = None):
        mesFormats = constantes.FORMAT_FICHIER_CLASSE['cla'] + constantes.TOUS_FICHIER
  
        if nomFichier == None:
            dlg = wx.FileDialog(
                                self, message="Ouvrir une classe",
                                defaultFile = "",
                                wildcard = mesFormats,
                                style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
                                )

            if dlg.ShowModal() == wx.ID_OK:
                paths = dlg.GetPaths()#.decode(FILE_ENCODING)
                nomFichier = paths[0]
            else:
                nomFichier = ''
            
            dlg.Destroy()
        if nomFichier != '':
            self.classe.ouvrir(nomFichier)
        
        self.classe.doc.MiseAJourTypeEnseignement()
        self.classe.doc.SetPosition(self.classe.doc.position)
        
        self.MiseAJour()
        
        self.sendEvent(modif = "Ouverture d'une Classe",
                       draw = True, verif = True)
    
    ###############################################################################################
    def enregistrer(self, nomFichier):

        wx.BeginBusyCursor()
#         fichier = open(nomFichier, 'w')
        
        # La classe
        classe = self.classe.getBranche()
        
        # La racine
        constantes.indent(classe)
        
        enregistrer_root(classe, nomFichier)
        
        
#         try:
# #            ET.ElementTree(classe).write(fichier, encoding = SYSTEM_ENCODING)
#             ET.ElementTree(classe).write(fichier, xml_declaration=False, encoding = SYSTEM_ENCODING)
#         except IOError:
#             messageErreur(None, "Accés refusé", 
#                                   "L'accés au fichier %s a été refusé !\n\n"\
#                                   "Essayer de faire \"Enregistrer sous...\"" %nomFichier)
#         except UnicodeDecodeError:
#             messageErreur(None, "Erreur d'encodage", 
#                                   "Un caractére spécial empéche l'enregistrement du fichier !\n\n"\
#                                   "Essayer de le localiser et de le supprimer.\n"\
#                                   "Merci de reporter cette erreur au développeur.")
            
#         fichier.close()

        wx.EndBusyCursor()
        
    #############################################################################
    def commandeSauve(self, event):
        mesFormats = constantes.FORMAT_FICHIER_CLASSE['cla'] + constantes.TOUS_FICHIER
        dlg = wx.FileDialog(self, 
                            message = constantes.MESSAGE_ENR['cla'], 
                            defaultDir="" , 
                            defaultFile="", wildcard=mesFormats, 
                            style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT|wx.FD_CHANGE_DIR
                            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()#.decode(FILE_ENCODING)
            dlg.Destroy()
            self.enregistrer(path)
            self.DossierSauvegarde = os.path.split(path)[0]
        else:
            dlg.Destroy()
            
    
        
    #############################################################################            
    def OnDefautPref(self, evt):
#        self.classe.options.defaut()
        self.classe.Initialise(isinstance(self.classe.doc, pysequence.Projet), defaut = True)
#        self.classe.doc.AjouterListeSystemes(self.classe.systemes)
        self.MiseAJour()
        self.sendEvent(modif = "Réinitialisation des paramètres de Classe",
                       draw = True, verif = True)
        
        
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
    
    
#    #############################################################################            
#    def EvtText(self, event):
#        if event.GetEventObject() == self.textctrl:
#            self.classe.etablissement = event.GetString()
#            self.sendEvent()
            
    ######################################################################################  
    def EvtBnt_BO(self, evt):
        self.GetFenetreDoc().TelechargerBO()
    
            
    ######################################################################################  
    def EvtComboAcad(self, evt = None, modif = True):
#        print "EvtComboAcad"
        if evt != None:
            self.classe.academie = evt.GetString()

        lst = []
        for val in list(constantes.ETABLISSEMENTS.values()):
            if self.classe.academie == val[0]:
                if self.classe.GetReferentiel().getTypeEtab() == 'L':
                    lst = val[2]
                else:
                    lst = val[1]
                break
#        print "   ", lst
        if len(lst) > 0:
            lst = sorted(list(set([v for _, v in lst])))
#        print "Villes", lst

        self.cbv.Set(lst)
        self.cbv.SlimResize()
#        self.cbv.SetSize((self.cbv.GetSizeFromTextSize(),-1))
        self.cbv.Refresh()
        
        if modif:
            self.sendEvent(modif = "Modification de l'académie",
                           draw = True, verif = False)
            
    
    ######################################################################################  
    def EvtComboVille(self, evt = None, modif = True):
#        print "EvtComboVille"
        if evt != None:
            self.classe.ville = evt.GetString()
#        print "   ", self.classe.ville
        lst = []
        for val in list(constantes.ETABLISSEMENTS.values()):
            if self.classe.academie == val[0]:
                if self.classe.GetReferentiel().getTypeEtab() == 'L':  # Lycée
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
        
        if modif:
            self.sendEvent(modif = "Modification de la ville",
                           draw = True, verif = False)
        
            
        
    ######################################################################################  
    def EvtComboEtab(self, evt):       
#        if evt.GetSelection() == len(constantes.ETABLISSEMENTS_PDD):
#            self.classe.etablissement = self.textctrl.GetStringSelection()
#            self.AfficherAutre(True)
#        else:
        self.classe.etablissement = evt.GetString()
#        self.AfficherAutre(False)
        
        self.sendEvent(modif = "Modification de l'établissement",
                       draw = True, verif = False)
     

    ######################################################################################  
    def EvtListBoxSyst(self, event = None, num = 0):
        """ Actions réalisées après avoir cliqué dans la liste de systèmes
        """
#        print "EvtListBoxSyst"
        if event != None:
            n = event.GetSelection()
        else:
            n = num
#        print "   ", n
        if len(self.classe.systemes) > n:
#            s = self.classe.systemes[n]
            self.panelSys.SetSysteme(self.classe.systemes[n])
            
#            self.panelSys.systeme.setBranche(s.getBranche())

    

    ######################################################################################  
    def EvtButtonSyst(self, event = None):
        """ Ajoute un nouveau système à la liste des système de la classe
        """
        #
        # Définition du nouveau nom
        #
        ref = self.classe.GetReferentiel()
        nom = "Nouveau %s " %et2ou(ref._nomSystemes.sing_())
        if nom in [s.nom for s in self.classe.systemes]:
            return
        
        self.panelSys.Enable(True)
#         nom0 = self.panelSys.textctrl.GetValue().strip()
#         if len(nom0) > 0:
#         nom = nom0
#         i = 1
#         while nom in [s.nom for s in self.classe.systemes]:
#             nom = nom0 + u" " + str(i)
#             i += 1
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
        s = pysequence.Systeme(self.classe, nom)
#        print "   +++", s.nom
        self.lstSys.Append(s.nom)
        self.classe.systemes.append(s)
#        self.classe.systemes.sort(key=attrgetter('nom'))
        num = self.lstSys.GetCount()-1
        self.lstSys.SetSelection(num)
        self.lstSys.EnsureVisible(num)
        self.EvtListBoxSyst(num = num)
        self.MiseAJourBoutonsSystem()
        
        if hasattr(self.classe, 'doc'):
            self.classe.doc.MiseAJourListeSystemesClasse()
            
#        print "   >>>",self.classe.systemes

    ######################################################################################  
    def EvtButtonSupprSyst(self, event = None):
        """ Supprime un  système de la liste des systèmes de la classe
        """
        num = self.lstSys.GetSelection()
        self.lstSys.Delete(num)
        del self.classe.systemes[num]
        self.EvtListBoxSyst()
        self.MiseAJourBoutonsSystem()
        
        if hasattr(self.classe, 'doc'):
            self.classe.doc.MiseAJourListeSystemesClasse()
        
    ######################################################################################  
    def MiseAJourBoutonsSystem(self):
        self.btnSupprimerSys.Enable(self.lstSys.GetCount() >= 1)
        
    
    ######################################################################################  
    def MiseAJourListeSys(self, nom = ""):
#         print "MiseAJourListeSys", nom, self.lstSys.GetSelection()
#         print "   ", [s.nom for s in self.classe.systemes]
#        if nom == u"":
#            nom = u"Système sans nom"
            
        n = self.lstSys.GetSelection()
        if n != wx.NOT_FOUND:
#             lst = [self.lstSys.GetItem(idx).GetText() for idx in range(self.lstSys.GetCount())]
        
        
            if not nom in self.lstSys.GetStrings():
                self.lstSys.SetString(n, nom)
                self.lstSys.SetSelection(self.lstSys.FindString(nom))


#     ######################################################################################  
#     def EvtRadioBox(self, event = None, CodeFam = None):
#         """ Sélection d'un type d'enseignement
#         """
#         if event != None:
#             radio_selected = event.GetEventObject()
#             CodeFam = Referentiel.getEnseignementLabel(radio_selected.GetLabel())
#         
#         
# #        fam = self.classe.familleEnseignement
# #         ancienRef = self.classe.referentiel
# #         ancienneFam = self.classe.familleEnseignement
#         self.classe.typeEnseignement, self.classe.familleEnseignement = CodeFam
#         self.classe.referentiel = REFERENTIELS[self.classe.typeEnseignement]
#         
# #        for c, e in [r.Enseignement[1:] for r in REFERENTIELS]constantes.Enseignement.items():
# #            if e[0] == :
# #                self.classe.typeEnseignement = c
# #                self.classe.familleEnseignement = constantes.FamilleEnseignement[self.classe.typeEnseignement]
# #                break
#         
#         self.classe.MiseAJourTypeEnseignement()
#         self.classe.doc.MiseAJourTypeEnseignement()
#         self.classe.doc.SetPosition(self.classe.doc.position)
# #        self.classe.doc.MiseAJourTypeEnseignement(fam != self.classe.familleEnseignement)
# #        self.MiseAJourType()
# #        if hasattr(self, 'list'):
# #            self.list.Peupler()
# 
#         self.st_type.SetLabel(self.classe.referentiel.Enseignement[0])
#         
#         # Modification des liens vers le BO
#         self.SetLienBO()
#         
#         # Modification des onglet du classeur
#         self.GetFenetreDoc().MiseAJourTypeEnseignement()
#         
#         self.Refresh()
#         
#         self.sendEvent(modif = "Modification du type d'enseignement",
#                        obj = self.classe)
        
    ######################################################################################  
    def SetLienBO(self):
        for b in self.bo:
            b.Destroy()
            
        self.bo = []
        if self.classe.typeEnseignement in REFERENTIELS:
            tit_url = REFERENTIELS[self.classe.typeEnseignement].BO_URL
        else:
            tit_url = self.classe.GetReferentiel().BO_URL
        for tit, url in tit_url:
            self.bo.append(hl.HyperLinkCtrl(self.pageGen, wx.ID_ANY, tit, URL = url))
            self.sbBO.Add(self.bo[-1], flag = wx.EXPAND)
            self.bo[-1].Show(tit != "")
            self.bo[-1].ToolTip.SetTip(url)
            
        self.pageGen.sizer.Layout()
        

    ######################################################################################  
    def MiseAJourTypeEnseignement(self):    
        
        ref = self.classe.GetReferentiel()
        
        # Mise à jour l'onglet Systèmes
        self.nb.SetPageText(2, ref._nomSystemes.Plur_())
        self.btnAjouterSys.SetLabel("Ajouter")# %s" %et2ou(ref._nomSystemes.un_()))
        self.btnAjouterSys.SetToolTip("Ajouter %s à la liste" %et2ou(ref._nomSystemes.un_("nouveau")))
        
        self.btnSupprimerSys.SetLabel("Supprimer")
        self.btnSupprimerSys.SetToolTip("Supprimer %s de la liste" %et2ou(ref._nomSystemes.le_()))
        
        self.panelSys.MiseAJourTypeEnseignement()
        
#         if hasattr(self, 'panelSys'):
#             try:
#                 self.pageSys.sizer.Detach(self.panelSys)
#             except:
#                 pass
#             self.panelSys.Destroy()
#             del self.panelSys
#         
#         s = pysequence.Systeme(self.classe)
#         self.panelSys = s.GetPanelPropriete(self.pageSys)
#         self.panelSys.Show()
#         self.pageSys.sizer.Add(self.panelSys, (0,1), (3,1),  flag = wx.ALL|wx.EXPAND, border = 2)
        
        # Modification des liens vers le BO
        self.SetLienBO()
        
        # Modification des onglet du classeur
        self.GetFenetreDoc().MiseAJourTypeEnseignement()
        self.ec.MiseAJourTypeEnseignement()
        
        self.Refresh()
        
        self.GetFenetreDoc().parent.options.optClasse["Enseignement"] = ref.Code
        
        self.sendEvent(modif = "Modification du type d'enseignement",
                       draw = True, verif = True)
        
        
    ######################################################################################  
    def MiseAJour(self, sendEvt = False, marquerModifier = True):
#         print "MiseAJour panelPropriete Classe", self.classe.referentiel.Enseignement[0]
#        self.MiseAJourType()
        
        self.sel_type.MiseAJour()
        
#        self.cb_type.SetStringSelection(REFERENTIELS[self.classe.typeEnseignement].Enseignement[0])
        
        
        self.cba.SetValue(self.classe.academie)
        self.EvtComboAcad(modif = False)
        self.cbv.SetValue(self.classe.ville)
        self.EvtComboVille(modif = False)
        self.cbe.SetValue(self.classe.etablissement)
        
#         print "   ", self.classe.systemes
        
        self.lstSys.Set([])
        
        
        if len(self.classe.systemes) == 0:
            self.panelSys.Enable(False)
#             # On crée un système vide
#             self.EvtButtonSyst()
# #            print "   +++", self.classe.systemes
#             self.EvtListBoxSyst()
# #            self.MiseAJourListeSys()
        else:
            self.panelSys.Enable(True)
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
    def Verrouiller(self):
        self.sel_type.Verrouiller()
        self.ec.Verrouiller()
        etat = not self.classe.verrouillee
#         self.cb_type.Show(etat)
#         self.st_type.Show(not etat)
        self.tb.EnableTool(30, etat)
        self.tb.EnableTool(31, etat)
        self.pasVerrouille = etat





class ListeCI(wx.Panel):

    def __init__(self, parent, prems = 1, pref = "CI"):

        wx.Panel.__init__(self, parent, -1, style = wx.BORDER_SIMPLE)
        
        #
        # Liste
        #
        # Passage momentané en Anglais (bug de wxpython)
#         locale2EN()
        
        
        self.list = ULC.UltimateListCtrl(self, wx.ID_ANY, 
                                         agwStyle = ULC.ULC_REPORT|ULC.ULC_EDIT_LABELS|ULC.ULC_SHOW_TOOLTIPS|
                                                    ULC.ULC_SINGLE_SEL|ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        
        self.prems = prems
        self.pref = pref
        self.parent = parent.Parent # Le PanelPropriete_CI
        
        self.imgSz = (30*SSCALE, 18*SSCALE)
        imageList = wx.ImageList(*self.imgSz)
        for n in range(18-prems):
            imageList.Add(self.GetBmpCode(n))
        self.list.SetImageList(imageList, wx.IMAGE_LIST_SMALL)
        
        
        self.list.InsertColumn(0, "")
        self.lstCb = ["M", "E", "I", "F", "S", "C"]
        self.lstCbtt = ["Matière", "Énergie", "Information", "Fonctionnel", "Structurel", "Comportemental"]
        for i, c in enumerate(self.lstCb):
            self.list.InsertColumn(i+1, c, width = 24, format = ULC.ULC_FORMAT_CENTER)
            self.list.SetColumnToolTip(i+1, self.lstCbtt[i])
        
        
            
        #
        # Toolbar
        #
        tsize = (IMG_SIZE_TB[0]*SSCALE, IMG_SIZE_TB[1]*SSCALE)
        self.toolbar = wx.ToolBar(self,-1)
        self.newtool= self.toolbar.AddTool(1, 'Ajouter', scaleImage(images.Icone_new.GetBitmap(), *tsize))
        self.edittool= self.toolbar.AddTool(2, 'Éditer', scaleImage(images.document_edit.GetBitmap(), *tsize))
        self.deltool= self.toolbar.AddTool(3, 'Supprimer', scaleImage(images.document_delete.GetBitmap(), *tsize))
        self.uptool= self.toolbar.AddTool(4, 'Remonter', scaleImage(images.go_up.GetBitmap(), *tsize))
        self.downtool= self.toolbar.AddTool(5, 'Descendre', scaleImage(images.go_down.GetBitmap(), *tsize))
        self.toolbar.Realize()
        
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=1)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=2)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=3)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=4)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=5)
        
        self.list.Bind(wx.EVT_SIZE, self.OnSize)
        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnChangeSelection)
        self.list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnChangeSelection)
        self.list.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnChange)
        self.list.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnLabelEdit)
        self.list.Bind(ULC.EVT_LIST_ITEM_CHECKED, self.OnCheck)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.toolbar, flag = wx.EXPAND)
        self.sizer.Add(self.list,1, flag = wx.EXPAND)
        self.SetSizer(self.sizer)
        self.sizer.Layout()
        
        
#         locale2def()
        
        
        self.OnChangeSelection()



    def OnSize(self, event):
        event.Skip()
        w = self.GetSize()[0]
        self.list.SetColumnWidth(0, w-6*self.list.GetColumnWidth(1)-6)
        
    def OnChangeSelection(self, event = None):
        num = self.list.GetFirstSelected()
#         print("OnChangeSelection", num)
        self.edittool.Enable(num >= 0)
        self.deltool.Enable(num >= 0)
        self.uptool.Enable(num >= 1)
        self.downtool.Enable(num >= 0 and num < self.list.GetItemCount())
        self.toolbar.Realize()
        
    def OnChange(self, event = None):
        event.Skip()
        self.OnChangeSelection()
        wx.CallAfter(self.parent.MAJ_CI_perso)
        
    def OnLabelEdit(self, event = None):
        event.Skip()
        self.edittool.Enable(False)
        self.deltool.Enable(False)
        self.uptool.Enable(False)
        self.downtool.Enable(False)
        self.toolbar.Realize()
        
    def OnCheck(self, event = None):
        event.Skip()
        wx.CallAfter(self.parent.MAJ_CI_perso)
        
    def AppendCI(self, tit = ""):
        num = self.list.GetFirstSelected()+1
        if num == 0:
            num = self.list.GetItemCount()

        cod = self.GetCode(num)
        self.list.InsertImageStringItem(num, cod, [num])
        
        self.SetCode(num, cod)
        
        self.list.SetStringItem(num, 0, tit)
        for i, _ in enumerate(self.lstCb):
            self.list.SetStringItem(num, i+1, "", it_kind=1)
            
        self.list.Select(num)
        
        self.sizer.Layout()
        
        
        
    
    def GetBmpCode(self, num):
        # make a custom bitmap showing "..."
        bw, bh = self.imgSz
        bmp = wx.Bitmap(bw,bh)
        dc = wx.MemoryDC(bmp)

        # clear to a specific background colour
        bgcolor = wx.Colour(255,254,255)
        dc.SetBackground(wx.Brush(bgcolor))
        dc.Clear()

        # draw the label onto the bitmap
        label = self.GetCode(num)
#         print("GetBmpCode", num, label)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        th = dc.GetTextExtent(label)[1]
        dc.DrawText(label,3*SSCALE, (bh-th)/2)
        del dc

        # now apply a mask using the bgcolor
        bmp.SetMaskColour(bgcolor)
        
        return bmp
        
    def GetCode(self, num):
        return self.pref+str(self.prems+num+1)
    
    def SetCode(self, num, cod):
#         print("SetCode", num, cod)
        self.list.SetItemData(num, cod)
        self.list.SetItemImage(num, [num])

        
    def SetStrings(self, lst):
        self.list.DeleteAllItems()
        for l in lst:
            self.AppendCI(tit = l)
    
    def GetStrings(self):
#         print("GetStrings", [self.list.GetItemText(n) for n in range(self.list.GetItemCount())])
        return [self.list.GetItemText(n) for n in range(self.list.GetItemCount())]
    
    def GetNewButton(self):
        return self.toolbar.GetToolByPos(0)
    
    def GetMEIFSC(self, num):
        cod = ""
        for c in range(1,7):
            if self.list.IsItemChecked(num, c):
                cod += self.lstCb[c-1]
            else:
                cod += " "
        cod = cod[:3]+"_"+cod[3:]
        return cod
    
    
    def GetAllMEIFSC(self):
        return [self.GetMEIFSC(n) for n in range(self.list.GetItemCount())]
    
    
    def SetMEIFSC(self, num, meifsc):
#         print("SetMEIFSC", num, meifsc, self.list.GetItemCount())
        for c in range(1,7):
            if self.lstCb[c-1] in meifsc:
                temp = self.list.GetItem(num, c)
                temp.Check(True)
                self.list.SetItem(temp)
            
    
    def SetAllMEIFSC(self, lst):
        for l, meifsc in enumerate(lst):
            self.SetMEIFSC(l, meifsc)

    
    
    def OnCompareItems(self, c1, c2):
        c1 = evaluer(c1)
        c2 = evaluer(c2)
        if c1 > c2: return 1
        elif c1 < c2: return -1
        else: return 0


        
    def OnToolClick(self, event):
        if event.GetId() == 1:
            self.AppendCI(self.pref+str(self.prems+self.list.GetItemCount()+1))
            
        elif event.GetId() == 2:
            num = self.list.GetFirstSelected()
            if num >= 0:
                self.list.EditLabel(num)
                
        elif event.GetId() == 3:
            num = self.list.GetFirstSelected()
            if num >= 0:
                self.list.DeleteItem(num)
        
        elif event.GetId() == 4:
            num = self.list.GetFirstSelected()
            if num > 0:
                cod = self.list.GetItemData(num)
                self.SetCode(num, self.GetCode(num-1))
                self.SetCode(num-1, cod)
                self.list.SortItems(self.OnCompareItems)
                self.list.Select(num-1)
        
        elif event.GetId() == 5:
            num = self.list.GetFirstSelected()
            if num >= 0 and num < self.list.GetItemCount():
                cod = self.list.GetItemData(num)
                self.SetCode(num, self.GetCode(num+1))
                self.SetCode(num+1, cod)
                self.list.SortItems(self.OnCompareItems)
                self.list.Select(num+1)
        
        self.OnChangeSelection()
        wx.CallAfter(self.parent.MAJ_CI_perso)
        
        
        

    def OnGetItemToolTip(self, item, col):
        pass
#         print(item, col)
        
        
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
#        self.classe.doc.CI.GetPanelPropriete().construire()
        self.Destroy() 
        evt.Skip()
        return
    
        
        
####################################################################################
#
#   Classe définissant le panel de réglage des effectifs
#
####################################################################################     
class PanelEffectifsClasse(wx.Panel):
    """Classe définissant le panel de réglage des effectifs
        Rappel :
        
        :Example:
        
        listeEffectifs = ["C", "G", "D" ,"S", "E" ,"P"]
        NbrGroupes =   {"G" : 2, # Par classe
                        "E" : 2, # Par grp Eff réduit
                        "S" : 3, # Par classe
                        "P" : 4, # Par grp Eff réduit
                        }
                        
        Les effectifs sous forme arborescente
        exemple 'STI2D.xls' :
        [{'G': [{'D': []}, 
                {'E': []}, 
                {'P': []}]}, 
         {'S': []}, 
         {'I': []}]
                      
    """
    def __init__(self, parent, classe):
        wx.Panel.__init__(self, parent, -1)
        self.classe = classe
        
        #
        # Box "Classe"
        #
        self.boxClasse = scrolled.ScrolledPanel(self, -1, style = wx.BORDER_SUNKEN)
        self.boxClasse.SetupScrolling(scroll_x = False)
        self.boxClasse.SetAutoLayout(True)
        
        self.bsizerClasse = wx.BoxSizer(wx.VERTICAL)
        
        self.tClasse = wx.StaticText(self.boxClasse, -1, "")
        self.bsizerClasse.Add(self.tClasse, flag = wx.ALL|wx.EXPAND, border = 5)
        
        #
        # Effectif de la classe
        #
        self.vEffClas = Variable("",  
                                 lstVal = self.classe.effectifs['C'], 
                                 typ = VAR_ENTIER_POS, bornes = [4,80],
                                 data = "C")
        self.cEffClas = VariableCtrl(self.boxClasse, self.vEffClas, coef = 1, signeEgal = False, 
                                     sizeh = 30*SSCALE,
                                     scale = SSCALE)
        
        self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cEffClas)
        self.bsizerClasse.Add(self.cEffClas, flag = wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND, border = 5)
        
        self.boxClasse.SetSizer(self.bsizerClasse)
        
        
        # Illustration de la répartition
        self.pnlImg = wx.Panel(self, -1)
        self.bmp = wx.StaticBitmap(self.pnlImg, -1)#, size = (400*SSCALE, 80*SSCALE))
        
        sizer = wx.BoxSizer()
        sizer.Add(self.bmp)
        self.pnlImg.SetSizerAndFit(sizer)
        
        self.MiseAJourTypeEnseignement()
        
        self.MiseAJourNbrEleve()

        border = wx.BoxSizer(wx.HORIZONTAL)
        border.Add(self.boxClasse, flag = wx.EXPAND|wx.ALL, border = 3)
        border.Add(self.pnlImg, 1, flag = wx.EXPAND|wx.ALL, border = 3)
        
        self.SetSizerAndFit(border)
        self.Layout()
        
        self.Bind(wx.EVT_SIZE, self.Onsize)
        

    #############################################################################            
    def Onsize(self, event = None):
        if self.IsShownOnScreen():
            wp, hp = self.pnlImg.GetSize()
            print("Onsize", wp, hp)
            if wp > 0 and hp > 0:
                self.bmp.SetBitmap(self.classe.getBitmapEffectifs(wp, hp))
            
            self.Refresh()
        
        if event is not None:
            event.Skip()
        
        
    ######################################################################################  
    def MiseAJourTypeEnseignement(self):
        ref = self.classe.GetReferentiel()
        
        # couleurs
        coulGrp = {k : couleur.GetCouleurWx(ref.effectifs[k][3], bytes = True) for k in ref.effectifs.keys() if ref.effectifs[k] is not None}
        
        self.tClasse.SetLabel(ref.effectifs["C"][1])
        self.boxClasse.SetBackgroundColour(coulGrp["C"].ChangeLightness(180))
        self.boxClasse.SetForegroundColour(coulGrp["C"])
            
        #
        # Effectif de la classe
        #
        self.vEffClas.n = "Nombre %s" %ref.getLabel("ELEVES").de_plur_()
        self.cEffClas.Renommer(self.vEffClas.n)
        self.cEffClas.SetBackgroundColour(coulGrp['C'].ChangeLightness(180))
        self.cEffClas.SetForegroundColour(coulGrp["C"])
        self.cEffClas.SetHelp("Nombre %s dans la %s" %(ref.getLabel("ELEVES").de_plur_(),ref.effectifs["C"][1]))
        

        # widgets + variables
        if hasattr(self, "_widgets"):
            for w in self._widgets:
                try:
                    w.Destroy()
                except:
                    pass
        self._widgets = []
#         if hasattr(self, "cNbGrp"):
#             for c in self.cNbGrp.values():
#                 c.Destroy()
        self.vNbGrp = {}
        self.cNbGrp = {}
        
        def construire(lst, k0, pnl):
            for dic in lst:
                k, g = list(dic.items())[0]
                sb = wx.Panel(pnl, -1, style = wx.BORDER_RAISED)
#                 st = wx.StaticText(sb, -1, ref.effectifs[k][1])
                sb.SetOwnBackgroundColour(coulGrp[k].ChangeLightness(180))
                sb.SetForegroundColour(coulGrp[k])
                bs = wx.BoxSizer(wx.VERTICAL)
#                 bs.Add(st, flag = wx.ALL|wx.EXPAND, border = 2)
                
                self.vNbGrp[k] = Variable("",  
                                          lstVal = self.classe.nbrGroupes[k], 
                                          typ = VAR_ENTIER_POS, bornes = [0,40],
                                          data = k)
                self.cNbGrp[k] = VariableCtrl(sb, self.vNbGrp[k], coef = 1, signeEgal = False,
                                              help = "Nombre de groupes %s au sein du groupe %s" %(ref.effectifs[k][1], ref.effectifs[k0][1]), 
                                              sizeh = 20*SSCALE, color = coulGrp[k],
                                              unite = "groupes "+"\""+ref.effectifs[k][1]+"\"",
                                              scale = SSCALE, sliderAGauche = True)
                self.cNbGrp[k].SetBackgroundColour(coulGrp[k].ChangeLightness(180))
                self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cNbGrp[k])
                bs.Add(self.cNbGrp[k], flag = wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND, border = 5)
                sb.SetSizer(bs)
                self._widgets.append(sb)
                
                pnl.GetSizer().Add(sb, flag = wx.ALL|wx.EXPAND, border = 5)
                
                construire(g, k, sb)
                    
#         print("_effectifs", ref._effectifs)
        construire(ref._effectifs, "C", self.boxClasse)
        calculerEffectifs(self.classe)
        self.Onsize()
#         self.boxClasse.Layout()

        wx.CallAfter(self.Layout)
        
        
#     #############################################################################            
#     def getBitmapClasse(self, W, H):
# #         return wx.Bitmap(larg, larg)
#         imagesurface = draw_cairo.getBitmapClasse(W, H, self.classe)
# 
#         return getBitmapFromImageSurface(imagesurface)
    
    
    #############################################################################            
    def EvtVariableEff(self, event):
        
        var = event.GetVar()
        
        if var == self.vEffClas:
            if self.classe.effectifs['C'] == var.v[0]:
                return
            self.classe.effectifs['C'] = var.v[0]
        else:
            if self.classe.nbrGroupes[var.GetData()] == var.v[0]:
                return
            self.classe.nbrGroupes[var.GetData()] = var.v[0]
        
        calculerEffectifs(self.classe)
            
        self.classe.GetApp().sendEvent(self.classe, 
                                       modif = "Modification du découpage de la Classe",
                                       draw = True, verif = True)
#        self.AjouterGroupesVides()
        self.MiseAJourNbrEleve()
        

        
    
    def MiseAJourNbrEleve(self):
        self.Onsize()
#         if int(wx.version()[0]) > 2:
#             self.boxEffRed.SetLabelText(strEffectifComplet(self.classe, 'G', -1))
#         else:
#             self.boxEffRed.SetLabel(strEffectifComplet(self.classe, 'G', -1))
        
#         try: # py3 : pas trouvé mieux pour éviter les MemoryError
# #             self.bmp.SetLargeBitmap(self.getBitmapClasse(1200))
#             self.bmp.SetBitmap(self.getBitmapClasse(900))
#         except:
#             pass
        
        
        
    def MiseAJour(self):
        self.vEffClas.v[0] = self.classe.effectifs['C']
        for k, v in self.vNbGrp.items():
            v.v[0] = self.classe.nbrGroupes[k]
        
        self.cEffClas.mofifierValeursSsEvt()
        for c in self.cNbGrp.values():
            c.mofifierValeursSsEvt()
        
#        self.AjouterGroupesVides()
        self.MiseAJourNbrEleve()
    
    
    ########################################################################
    def Verrouiller(self):
        for s in self.cNbGrp.values():
            if not self.classe.verrouillee:
                s.SetMin(0)
            else:
                s.SetMin(1)
# 
# 
# class PanelEffectifsClasse2(wx.Panel):
#     """Classe définissant le panel de réglage des effectifs
#         Rappel :
#         
#         :Example:
#         
#         listeEffectifs = ["C", "G", "D" ,"S", "E" ,"P"]
#         NbrGroupes = {"G" : 2, # Par classe
#         "E" : 2, # Par grp Eff réduit
#         "S" : 3, # Par classe
#         "P" : 4, # Par grp Eff réduit
#         }
#                       
#     """
#     def __init__(self, parent, classe):
#         wx.Panel.__init__(self, parent, -1)
#         self.classe = classe
#         ref = self.classe.GetReferentiel()
#         
#         #
#         # Box "Classe"
#         #
#         boxClasse = myStaticBox(self, -1, ref.effectifs["C"][1])
# 
# #         coulClasse = couleur.GetCouleurWx(constantes.CouleursGroupes['C'])
#         coulClasse = couleur.GetCouleurWx(ref.effectifs["C"][3], bytes = True)
# #        boxClasse.SetOwnForegroundColour(coulClasse)
#         
# #         self.coulEffRed = couleur.GetCouleurWx(constantes.CouleursGroupes['G'])
#         self.coulEffRed = couleur.GetCouleurWx(ref.effectifs["G"][3], bytes = True)
#         
# #         self.coulEP = couleur.GetCouleurWx(constantes.CouleursGroupes['E'])
#         self.coulEP = couleur.GetCouleurWx(ref.effectifs["E"][3], bytes = True)
#     
# #         self.coulAP = couleur.GetCouleurWx(constantes.CouleursGroupes['P'])
#         self.coulAP = couleur.GetCouleurWx(ref.effectifs["P"][3], bytes = True)
#         
# #        self.boxClasse = boxClasse
#         bsizerClasse = wx.StaticBoxSizer(boxClasse, wx.VERTICAL)
#         sizerClasse_h = wx.BoxSizer(wx.HORIZONTAL)
#         sizerClasse_b = wx.BoxSizer(wx.HORIZONTAL)
#         self.sizerClasse_b = sizerClasse_b
#         bsizerClasse.Add(sizerClasse_h)
#         bsizerClasse.Add(sizerClasse_b)
#         
#         # Effectif de la classe
#         self.vEffClas = Variable("Nombre %s" %ref.getLabel("ELEVES").de_plur_(),  
#                             lstVal = classe.effectifs['C'], 
#                             typ = VAR_ENTIER_POS, bornes = [4,80])
#         self.cEffClas = VariableCtrl(self, self.vEffClas, coef = 1, signeEgal = False,
#                                 help = "Nombre %s dans la %s" %(ref.getLabel("ELEVES").de_plur_(),ref.effectifs["C"][1]), 
#                                 sizeh = 30*SSCALE, 
#                                 color = coulClasse, scale = SSCALE)
#         self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cEffClas)
#         sizerClasse_h.Add(self.cEffClas, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 5)
#         
#         # Nombre de groupes à effectif réduits
#         self.vNbERed = Variable("Nbr de groupes\n%s" %ref.effectifs["G"][1],  
#                                 lstVal = classe.nbrGroupes['G'], 
#                                 typ = VAR_ENTIER_POS, bornes = [1,4])
#         self.cNbERed = VariableCtrl(self, self.vNbERed, coef = 1, signeEgal = False,
#                                     help = "Nombre de groupes %s dans la %s" %(ref.effectifs["G"][1],ref.effectifs["C"][1]), sizeh = 20*SSCALE, 
#                                     color = self.coulEffRed, scale = SSCALE)
#         self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cNbERed)
#         sizerClasse_h.Add(self.cNbERed, 0, wx.TOP|wx.LEFT, 5)
#         
#         
#         #
#         # Boxes Effectif Réduit
#         #
#         boxEffRed = myStaticBox(self, -1, "")
#         boxEffRed.SetBackgroundColour('white')
#         boxEffRed.SetOwnBackgroundColour('white')
#         boxEffRed.SetOwnForegroundColour(self.coulEffRed)
#         self.boxEffRed = boxEffRed
#         bsizerEffRed = wx.StaticBoxSizer(boxEffRed, wx.HORIZONTAL)
#         self.sizerEffRed_g = wx.BoxSizer(wx.VERTICAL)
#         self.sizerEffRed_d = wx.BoxSizer(wx.VERTICAL)
#         bsizerEffRed.Add(self.sizerEffRed_g, flag = wx.EXPAND)
#         bsizerEffRed.Add(wx.StaticLine(self, -1, style = wx.VERTICAL), flag = wx.EXPAND)
#         bsizerEffRed.Add(self.sizerEffRed_d, flag = wx.EXPAND)
#         sizerClasse_b.Add(bsizerEffRed)
#         
#         # Nombre de groupes d'étude/projet
#         self.vNbEtPr = Variable("Nbr de groupes\n%s" %ref.effectifs["E"][1],  
#                             lstVal = classe.nbrGroupes['E'], 
#                             typ = VAR_ENTIER_POS, bornes = [1,10])
#         self.cNbEtPr = VariableCtrl(self, self.vNbEtPr, coef = 1, signeEgal = False,
#                                 help = "Nombre de groupes %s par groupe %s" %(ref.effectifs["E"][1], ref.effectifs["G"][1]), 
#                                 sizeh = 20*SSCALE, 
#                                 color = self.coulEP, scale = SSCALE)
#         self.cNbEtPr.SetBackgroundColour('white')
#         self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cNbEtPr)
#         self.sizerEffRed_g.Add(self.cNbEtPr, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 3)
#         
# #        self.BoxEP = myStaticBox(self, -1, u"", size = (30, -1))
# #        self.BoxEP.SetOwnForegroundColour(self.coulEP)
# #        self.BoxEP.SetMinSize((30, -1))     
# #        bsizer = wx.StaticBoxSizer(self.BoxEP, wx.VERTICAL)
# #        self.sizerEffRed_g.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
#             
#         # Nombre de groupes d'activité pratique
#         self.vNbActP = Variable("Nbr de groupes\n%s" %ref.effectifs["P"][1],  
#                             lstVal = classe.nbrGroupes['P'], 
#                             typ = VAR_ENTIER_POS, bornes = [2,20])
#         self.cNbActP = VariableCtrl(self, self.vNbActP, coef = 1, signeEgal = False,
#                                 help = "Nombre de groupes %s par groupe %s" %(ref.effectifs["P"][1], ref.effectifs["G"][1]), 
#                                 sizeh = 20*SSCALE, 
#                                 color = self.coulAP, scale = SSCALE)
#         self.cNbActP.SetBackgroundColour('white')
#         self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, self.cNbActP)
#         self.sizerEffRed_d.Add(self.cNbActP, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 3)
#         
# #        self.BoxAP = myStaticBox(self, -1, u"", size = (30, -1))
# #        self.BoxAP.SetOwnForegroundColour(self.coulAP)
# #        self.BoxAP.SetMinSize((30, -1))     
# #        bsizer = wx.StaticBoxSizer(self.BoxAP, wx.VERTICAL)
# #        self.sizerEffRed_d.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
#         
#         
#         # Illustration de la répartition
# #         self.bmp = StaticBitmapZoom(self, -1, size = (400*SSCALE, 80*SSCALE))
#         self.bmp = wx.StaticBitmap(self, -1, size = (400*SSCALE, 80*SSCALE))
#         
#         self.lstBoxEffRed = []
#         self.lstBoxEP = []
#         self.lstBoxAP = []
#         
# #        self.AjouterGroupesVides()
#         
#         self.MiseAJourNbrEleve()
# 
#         border = wx.BoxSizer(wx.HORIZONTAL)
#         border.Add(bsizerClasse, flag = wx.EXPAND)
#         border.Add(self.bmp, 1, flag = wx.EXPAND|wx.ALL, border = 3)
#         
#         self.SetSizer(border)
# 
#     
#     #############################################################################            
#     def getBitmapClasse(self, larg):
# #         return wx.Bitmap(larg, larg)
#         imagesurface = draw_cairo.getBitmapClasse(larg, self.classe)
# 
#         return getBitmapFromImageSurface(imagesurface)
#     
#     
#     #############################################################################            
#     def EvtVariableEff(self, event):
#         var = event.GetVar()
#         if var == self.vEffClas:
#             self.classe.effectifs['C'] = var.v[0]
#         elif var == self.vNbERed:
#             self.classe.nbrGroupes['G'] = var.v[0]
#         elif var == self.vNbEtPr:
#             self.classe.nbrGroupes['E'] = var.v[0]
#         elif var == self.vNbActP:
#             self.classe.nbrGroupes['P'] = var.v[0]
#         calculerEffectifs(self.classe)
#             
#         self.classe.GetApp().sendEvent(self.classe, modif = "Modification du découpage de la Classe",
#                               obj = self.classe, draw = True, verif = True)
# #        self.AjouterGroupesVides()
#         self.MiseAJourNbrEleve()
#         
# #    def AjouterGroupesVides(self):
# #        return
# #        for g in self.lstBoxEP:
# #            self.sizerEffRed_g.Remove(g)
# #        for g in self.lstBoxAP:
# #            self.sizerEffRed_d.Remove(g)    
# #        for g in self.lstBoxEffRed:
# #            self.sizerClasse_b.Remove(g)
# #        
# #        self.lstBoxEffRed = []
# #        self.lstBoxEP = []
# #        self.lstBoxAP = []    
# #        
# #        for g in range(self.classe.nbrGroupes['G'] - 1):
# #            box = myStaticBox(self, -1, u"Eff Red", size = (30, -1))
# #            box.SetOwnForegroundColour(self.coulEffRed)
# #            box.SetMinSize((30, -1))
# #            self.lstBoxEffRed.append(box)
# #            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
# #            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
# #            self.sizerClasse_b.Add(bsizer, flag = wx.EXPAND)
# #        
# #        for g in range(self.classe.nbrGroupes['E']):
# #            box = myStaticBox(self, -1, u"E/P", size = (30, -1))
# #            box.SetOwnForegroundColour(self.coulEP)
# #            box.SetMinSize((30, -1))
# #            self.lstBoxEP.append(box)
# #            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
# ##            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
# #            self.sizerEffRed_g.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
# #            
# #        
# #        for g in range(self.classe.nbrGroupes['P']):
# #            box = myStaticBox(self, -1, u"AP", size = (30, -1))
# #            box.SetOwnForegroundColour(self.coulAP)
# #            box.SetMinSize((30, -1))
# #            self.lstBoxAP.append(box)
# #            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
# ##            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
# #            self.sizerEffRed_d.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
# #        
# #        self.Layout()
#         
#     
#     def MiseAJourNbrEleve(self):
#         if int(wx.version()[0]) > 2:
#             self.boxEffRed.SetLabelText(self.classe.GetStrEffectifComplet('G', -1))
#         else:
#             self.boxEffRed.SetLabel(self.classe.GetStrEffectifComplet('G', -1))
#         
#         try: # py3 : pas trouvé mieux pour éviter les MemoryError
# #             self.bmp.SetLargeBitmap(self.getBitmapClasse(1200))
#             self.bmp.SetBitmap(self.getBitmapClasse(900))
#         except:
#             pass
#         
#          
# #        t = u"groupes de "
# #        self.BoxEP.SetLabelText(t+strEffectif(self.classe, 'E', -1))
# #        self.BoxAP.SetLabelText(t+strEffectif(self.classe, 'P', -1))
# 
# #        self.Refresh()
#         
#         
#     def MiseAJour(self):
#         self.vEffClas.v[0] = self.classe.effectifs['C']
#         self.vNbERed.v[0] = self.classe.nbrGroupes['G']
#         self.vNbEtPr.v[0] = self.classe.nbrGroupes['E']
#         self.vNbActP.v[0] = self.classe.nbrGroupes['P']
#         
#         self.cEffClas.mofifierValeursSsEvt()
#         self.cNbERed.mofifierValeursSsEvt()
#         self.cNbEtPr.mofifierValeursSsEvt()
#         self.cNbActP.mofifierValeursSsEvt()
#         
# #        self.AjouterGroupesVides()
#         self.MiseAJourNbrEleve()
#         
# 
#         
        
        
####################################################################################
#
#   Classe définissant le panel de propriété du CI
#
####################################################################################
class PanelPropriete_CI(PanelPropriete):
    def __init__(self, parent, CI):
        self.CI = CI       
        PanelPropriete.__init__(self, parent, objet = self.CI)
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        
        self.construire()
        self.MiseAJour()
        


    #############################################################################            
    def GetDocument(self):
        return self.CI.parent
    
    ######################################################################################################
    def OnEnter(self, event):
        return
        
    #############################################################################            
    def construire(self):
#        print "construire CI"
        self.group_ctrls = []
        self.DestroyChildren()
#         if hasattr(self, 'grid1'):
#             self.sizer.Remove(self.grid1)
            
        ref = self.CI.GetReferentiel()
        
        #
        # Cas où les CI sont sur une cible MEI
        #
        abrevCI = ref.abrevCI
        if ref.CI_cible:
            self.panel_cible = Panel_Cible(self, self.CI)
            self.sizer.Add(self.panel_cible, flag = wx.EXPAND|wx.ALIGN_TOP)
#             self.sizer.Add(self.panel_cible, (1,0), (2,2), flag = wx.EXPAND|wx.ALIGN_TOP)
            
            
        #
        # La liste des CI à cocher (plus éventuelle selection de poids)
        #
        panelCI = wx.Panel(self, -1)#, style = wx.BORDER_SIMPLE)
        sci = wx.BoxSizer(wx.VERTICAL)
        panelCI.SetSizer(sci)
        
#         if ref.CI_cible:
#             self.grid1 = wx.FlexGridSizer( 0, 3, 0, 0 )
#         else:
#             self.grid1 = wx.FlexGridSizer( 0, 2, 0, 0 )

        for i, ci in enumerate(ref.CentresInterets):
            hs = wx.BoxSizer(wx.HORIZONTAL)
            r = wx.CheckBox(panelCI, 200+i, abrevCI+str(i+1))
            t = EllipticStaticText(panelCI, -1, "")#ci)#tronquerDC(ci, 50, self))
            r.SetToolTip(ci)
            t.SetToolTip(ci)
#             hs.Add(r, flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, border = 1)
#             hs.Add(t, flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border = 4 )
            hs.Add( r, flag = wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, border = 1 )
            hs.Add( t, flag = wx.ALIGN_CENTRE_VERTICAL|wx.LEFT, border = 4 )#|wx.EXPAND
            
            if ref.CI_cible:
                p = wx.TextCtrl(panelCI, -1, "1")
                p.SetToolTip("Poids horaire relatif "+ ref._nomCI.du_())
                p.Show(False)
                p.SetMinSize((30*SSCALE, -1))
#                 hs.Add( p, flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT, border = 2)
                hs.Add( p, flag = wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT, border = 2)
                self.group_ctrls.append((r, t, p))
            else:
                self.group_ctrls.append((r, t))
            
            sci.Add(hs, flag = wx.EXPAND)

        
        for rtp in self.group_ctrls:
            self.Bind(wx.EVT_CHECKBOX, self.OnCheck, rtp[0] )
        
        
        if ref.CI_cible:
            for rtp in self.group_ctrls:
                self.Bind(wx.EVT_TEXT, self.OnPoids, rtp[2] )
        

        #
        # Cas des CI personnalisés
        #
        
        tit = ref.nomCI
        if len(ref.CentresInterets) > 0:
            tit += " personnalisé(s)"
            
        tit = Grammaire(tit)    
        if self.CI.maxCI != 1:
            tit = tit.Plur_()
        else:
            tit = tit.Sing_()
            
        if ref.CI_cible:
            self.elb = ListeCI(panelCI, prems = len(ref.CentresInterets), pref = abrevCI)
            self.elb.SetMinSize((-1, 60*SSCALE))
        else:
            self.elb = MyEditableListBox(panelCI, -1, tit,
                                         size = wx.DefaultSize,
                                         style = adv.EL_ALLOW_NEW | adv.EL_ALLOW_EDIT | adv.EL_ALLOW_DELETE)
            self.elb.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnChangeCI_perso)
            self.elb.SetMinSize((-1, 60*SSCALE))
            self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnChangeCI_perso)
        sci.Add(self.elb, 1, flag = wx.EXPAND)    
        
        
        

        #
        # Séléction du nombre maxi de CI
        #
#         print("maxCI", ref.maxCI)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(wx.StaticText(panelCI, -1, "Nombre maximum de %s" %ref._nomCI.plur_()), 
               flag = wx.EXPAND|wx.TOP|wx.RIGHT, border = 4)
        
        self.nCI = wx.SpinCtrl(panelCI, -1, "Nombre maximum de %s" %ref._nomCI.plur_(), size = (35*SSCALE, -1))
        self.nCI.SetToolTip("Fixe un nombre maximum de %s sélectionnables.\n" \
                                  "0 = pas de limite" %ref._nomCI.plur_())
        self.nCI.SetRange(0,9)
        self.nCI.SetValue(0)
        self.Bind(wx.EVT_SPINCTRL, self.OnOption, self.nCI)
        self.nCI.Bind(wx.EVT_TEXT , self.OnText)
#         self.grid1.Add(self.nCI, flag = wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, border = 5)
#             self.sizer.Add(self.nCI, (0,1), flag = wx.ALL, border = 2)
        self.nCI.Show(ref.maxCI == 0) # maximum pas imposé par le référentiel
        hs.Add(self.nCI, flag = wx.EXPAND)
        sci.Add(hs, flag = wx.EXPAND) 

        self.panelCI = panelCI
        self.sizer.Add(panelCI, 1, flag = wx.EXPAND)
        
        
        
        
        
        #
        # Les Problématiques
        #
#         sbspb = wx.StaticBoxSizer(sbpb,wx.HORIZONTAL)

        self.panelPb = PanelProblematiques(self, self.CI)
#         sbspb.Add(self.panelPb,1, flag = wx.EXPAND)
        self.sizer.Add(self.panelPb, 0.5, flag = wx.EXPAND)
#         self.sizer.Add(sbspb, (0,3), (3, 1), flag = wx.EXPAND)
        
#         self.sizer.AddGrowableCol(2,1)
#         self.sizer.AddGrowableCol(3,1)
#         self.sizer.AddGrowableRow(2)

        self.Bind(wx.EVT_SIZE, self.OnSize)

        #
        # Mise en place
        #
        self.SetupScrolling(scroll_x = False)
        self.sizer.Layout()

        
    
    #############################################################################            
    def OnSize(self, event):
        event.Skip()
        self.Freeze()
        
#         print "OnSize", 
#         w = self.GetClientSize()[0]
# #         print w
#         if hasattr(self, 'panel_cible'):
#             w -= self.panel_cible.GetSize()[0]
            
#         print ">>", w*2/3
        
        ref = self.CI.GetReferentiel()
#         self.panelCI.SetSize((10,10))
        
#         return
        for i, ci in enumerate(ref.CentresInterets):
            t = self.group_ctrls[i][1]
            t.SetLabel("")
#         

#         self.sizer.RecalcSizes()
#         self.panelCI.Fit()
        self.sizer.Layout()
#         self.elb.FitInside()
        
        
        l = self.elb.GetSize()[0]
#         print "  ", l
        for i, ci in enumerate(ref.CentresInterets):
            t = self.group_ctrls[i][1]
            t.SetLabel(tronquerDC(ci, l, self))
#         self.sizer.Layout()

        self.Thaw()
     
    #############################################################################            
    def OnText(self, event):
#         print(event.GetString(), self.nCI.GetValue())
        if int(event.GetString()) == 0:
            self.Unbind(wx.EVT_SPINCTRL)
            self.nCI.SetRange(0,9)
#             print(" ", event.GetString(), self.nCI.GetValue())
            self.nCI.SetValue(0)
            self.Bind(wx.EVT_SPINCTRL, self.OnOption, self.nCI)
        event.Skip()


    #############################################################################            
    def OnOption(self, event):
        """ Modification du nombre maxi de CI selectionnables
            (ne peut se produire que si ce nombre n'est pas fixé par le référentiel)
        """
        m = len(self.CI.numCI)+len(self.CI.CI_perso)
#         print("OnOption", m, self.CI.maxCI, self.nCI.GetValue())
        if self.CI.maxCI == 0: # pas de limite
            self.nCI.SetValue(m)
            self.CI.maxCI = m
        else:
            self.CI.maxCI = self.nCI.GetValue()
        self.nCI.SetRange(m,9)
        self.MiseAJour()


    #############################################################################            
    def OnPoids(self, event):
        pass


    #############################################################################            
    def OnCheck(self, event):
        """ Selection d'un CI
        """
        ref = self.CI.GetReferentiel()
        button_selected = event.GetEventObject().GetId()-200 
#         if self.CI.maxCI == 1: # Des boutons radio
#             self.CI.Set1Num(button_selected)
#         else:               # Des checkbox
        if event.GetEventObject().GetValue():
            self.CI.AddNum(button_selected)
        else:
            self.CI.DelNum(button_selected)
        
#        self.panel_cible.bouton[button_selected].SetState(event.GetEventObject().IsChecked())
#        if self.CI.GetTypeEnseignement() == 'ET':
        if ref.CI_cible:
            self.panel_cible.GererBoutons(True)
        else:
            if len(self.group_ctrls[button_selected]) > 2: # Il y a un Crtl de poids
                self.group_ctrls[button_selected][2].Show(event.GetEventObject().GetValue ())
            
            l, p = self.GetListeCIActifs()
            self.GererCases(l, p)
#             if hasattr(self, 'b2CI'):
#                 self.b2CI.Enable(len(self.CI.numCI) <= 2)
        
        self.panelPb.ReConstruire()
        self.panelCI.Layout()
        self.Layout()
        
        
        
        self.sendEvent(modif = "Modification des %s abordés" %ref._nomCI.plur_(),
                       draw = True, verif = True)


    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        if self.CI.GetTypeEnseignement() == 'ET':
        self.elb.SetStrings(self.CI.CI_perso)
        if hasattr(self.elb, "GetAllMEIFSC"):
            self.elb.SetAllMEIFSC(self.CI.PosCI_perso)
            
            
        if self.CI.GetReferentiel().CI_cible:
            self.panel_cible.GererBoutons(True)

        else:
            for i, num in enumerate(self.CI.numCI):
                self.group_ctrls[num][0].SetValue(True)
                if len(self.group_ctrls[num]) > 2:
                    self.group_ctrls[num][2].Show()
                    self.group_ctrls[num][2].SetValue(self.CI.poids[i])
            self.Layout()
            
            l, p = self.GetListeCIActifs()
            self.GererCases(l, p)

        if hasattr(self, 'nCI'):
            self.nCI.SetValue(self.CI.maxCI)
        
        self.panelPb.ReConstruire()
        self.panelPb.MiseAJour()
        
        
        
        if sendEvt:
            self.sendEvent(draw = True, verif = True)



    #############################################################################            
    def GetListeCIActifs(self):
        """ Renvoie :
            - la liste des indices des boutons "CI" actifs
            - un booléen indiquant si la liste des CI selectionnables est active
        """
#         print "GetListeCIActifs", self.CI.numCI , self.CI.CI_perso
        # Liste des boutons CI à afficher
        ref = self.CI.GetReferentiel()
        if len(self.CI.numCI) + len(self.CI.CI_perso) == 0 or self.CI.maxCI == 0:       # Tous les CI
            l = list(range(len(ref.CentresInterets)))
            p = True    
            
        elif len(self.CI.numCI) + len(self.CI.CI_perso) >= self.CI.maxCI:
            l = self.CI.numCI
            p = False
        
        else:
            l = list(range(len(ref.CentresInterets)))
            p = True
            
#         print "  >>" , l, p
        return l, p
    
    
    
    #############################################################################            
    def GererCases(self, liste, perso, appuyer = False):
        """ Permet de cacher les cases des CI au fur et à mesure que l'on selectionne des CI
            :param liste: liste des CI à activer
        """ 
#         print "GererCases", perso
        for i, b in enumerate(self.group_ctrls):
            b[0].Enable(i in liste)
                
        self.elb.GetNewButton().Enable(perso)
        
        if appuyer:
            for i, b in enumerate(self.group_ctrls):
                b[0].SetValue(i in self.CI.numCI)
                
    
    #############################################################################            
    def MAJ_CI_perso(self, event = None):
        self.CI.CI_perso = self.elb.GetStrings()
        
        if hasattr(self.elb, "GetAllMEIFSC"):
            self.CI.PosCI_perso = self.elb.GetAllMEIFSC()
        else:
            self.CI.PosCI_perso = [""]*len(self.CI.CI_perso) # pour pas qu'il y ait de différence de taille entre les deux listes
        
        l, p = self.GetListeCIActifs()
        self.GererCases(l, p)
#         print "MAJ_CI_perso", self.CI.CI_perso
        ref = self.CI.GetReferentiel()
        self.sendEvent(modif = "Modification des %s personnalisés" %ref._nomCI.plur_(),
                       draw = True, verif = False)
        
        
    #############################################################################            
    def OnChangeCI_perso(self, event):
        wx.CallAfter(self.MAJ_CI_perso)
        event.Skip()




   
####################################################################################
#
#   Classe définissant le panel conteneur d'un calendrier
#
#################################################################################### 
class Panel_Calendrier(wx.Panel):
    def __init__(self, parent, calendrier):
        wx.Panel.__init__(self, parent, -1)
        self.calendrier = calendrier
        self.sizer = wx.GridBagSizer()
        
    def MiseAJour(self):
        self.sizer.Clear(delete_windows = True)
    
####################################################################################
#
#   Classe définissant le panel conteneur d'un emploi du temps
#
#################################################################################### 
class Panel_EDT(wx.Panel):
    def __init__(self, parent, EDT):
        wx.Panel.__init__(self, parent, -1)
        self.EDT = EDT
        self.sizer = wx.GridBagSizer()
        self.SetSizer(self.sizer)
        
    def MiseAJour(self):
        self.sizer.Clear(delete_windows = True)
        for i, j in enumerate(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]):
            nj = wx.StaticText(self, -1, j)
            self.sizer.Add(nj, (0,i), flag = wx.EXPAND)
        
#         for seance in self.EDT:
#             pass
        
    
    
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
        
        
        bmp = self.GetBmpCible()
        size_c = (bmp.GetWidth(), bmp.GetHeight())
        
        size_b = (0.1*size_c[0], 0.1*size_c[1])
        
        
#        rayons = [90,90,60,40,20,30,60,40,20,30,60,40,20,30,0]
#        angles = [-100,100,0,0,0,60,120,120,120,180,-120,-120,-120,-60,0]
#         centre = [96, 88]
        centre = [0.5*size_c[0], 0.5*size_c[1]]
        
#         rayons = {"F" : 60, 
#                   "S" : 40, 
#                   "C" : 20,
#                   "_" : 90}
        
        rayons = {"F" : 0.3*size_c[0], 
                  "S" : 0.2*size_c[0], 
                  "C" : 0.1*size_c[0],
                  "_" : 0.45*size_c[0]}
        
        angles = {"M" : 0,
                  "E" : 120,
                  "I" : -120,
                  "_" : -100}
        
        ref = self.CI.GetReferentiel()
        
        offset = 6
        for i in range(len(ref.CentresInterets)):
            mei, fsc = ref.positions_CI[i].split("_")
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

            
            r = platebtn.PlateButton(self, 100+i, "", 
                                     scaleImage(constantes.imagesCI[i].GetBitmap(), size_b[0], size_b[1]), 
                                     pos = (centre[0] + ray * sin(ang*pi/180) - size_b[0]/2-offset,
                                            centre[1] - ray * cos(ang*pi/180) - size_b[1]/2-offset/2), 
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
        
        
        #
        # Un bouton d'aide
        #
        aide = wx.BitmapButton(self, -1, scaleImage(images.Bouton_Aide.GetBitmap()),
                               pos = (0,0))
        aide.SetToolTip("Informations à propos de la cible des " + ref._nomCI.plur_())
        self.Bind(wx.EVT_BUTTON, self.OnAide, aide)
            
            
            
        self.SetSize(size_c)
        self.SetMinSize(size_c)
    
    
    #############################################################################            
    def GetBmpCible(self):
        if self.CI.GetReferentiel().champsInter:
            bmp = images.Cible.GetBitmap()
        else:
            bmp = images.Cible_simple.GetBitmap()
        size_c = (220*SSCALE, 200*SSCALE)
        return scaleImage(bmp, *size_c)
    
    #############################################################################            
    def OnAide(self, event):
        dlg = MessageAideCI(self)
        dlg.ShowModal()
        dlg.Destroy()
        
    
    ######################################################################################################
    def getMaxCI(self):
        return self.CI.maxCI
    
    
    ######################################################################################################
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush(self.backGround))
        dc.Clear()
        dc.DrawBitmap(self.GetBmpCible(), 0, 0)
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
        dc.DrawBitmap(self.GetBmpCible(), 0, 0)    
    
    
    #############################################################################            
    def OnButton(self, event):
        button_selected = event.GetEventObject().GetId()-100
        t = ""
        if event.GetEventObject().IsPressed():
            self.CI.AddNum(button_selected)
            t = "Ajout d'un CI"
        else:
            try: # sinon probléme avec les doubles clics
                self.CI.DelNum(button_selected)
                t = "Suppression d'un CI"
            except:
                pass

        self.GererBoutons()
        
        self.Layout()
        self.Parent.group_ctrls[button_selected][0].SetValue(event.GetEventObject().IsPressed())
        self.Parent.sendEvent(modif = t, draw = True, verif = False)    
        
        
    #############################################################################            
    def GererBoutons(self, appuyer = False):
        """ Permet de cacher les boutons des CI au fur et à mesure que l'on selectionne des CI
            Régles :
            - Maximum 2 CI
            - CI voisins sur la cible
            :param appuyer: pour initialisation : si vrai = appuie sur les boutons
            :type appuyer: boolean
        """
#         print("GererBoutons", len(self.CI.numCI), len(self.CI.CI_perso), self.getMaxCI())
        ref = self.CI.GetReferentiel()
        
        seuil_filtr = 4         # Nombre seuil de CI selectionnés au dela duquel on ne filtre plus par branche
        
        # Liste des boutons CI à afficher :
        if len(self.CI.numCI) + len(self.CI.CI_perso) == 0 or self.getMaxCI() == 0 \
           or self.getMaxCI() > seuil_filtr:                                                                         # Tous les CI
            l = list(range(len(ref.CentresInterets)))   
            p = True          
            
        elif self.getMaxCI() <= seuil_filtr and (len(self.CI.numCI) + len(self.CI.CI_perso) < self.getMaxCI()):    # Les CI de la même "branche"
            l = []
            for i,p in enumerate(ref.positions_CI):
                p = p[:3].strip()
                c = self.CI.GetPosCible(0)[:3].strip()

                if len(p) == 0 or len(c) == 0: # Cas des CI "en orbite"
                    l.append(i)
                else:       # Autres cas
                    for d in c:
                        if d in p:  
                            l.append(i)
                            break
            p = True
            
        else:
            l = self.CI.numCI                                                               # Seuls les CI déja sélectionnés
            p = self.getMaxCI() > len(l)
            
#         print("   ", l, p)
        
        for i, b in enumerate(self.bouton):
            if i in l:
                b.Show(True)
            else:
                b.Show(False)
                
        if appuyer:
            for i, b in enumerate(self.bouton):
#                 b.SetValue(i in self.CI.numCI)
                if hasattr(b, '_SetState'):
                    if i in self.CI.numCI:
                        b._SetState(platebtn.PLATE_PRESSED)
                    else:
                        b._SetState(platebtn.PLATE_NORMAL)
                b._pressed = i in self.CI.numCI
                
        self.Parent.GererCases(l, p, True)    
                    
                    
####################################################################################
#
#   Classe définissant le panel de propriété d'un lien vers une séquence
#
####################################################################################
class PanelPropriete_LienSequence(PanelPropriete):
    def __init__(self, parent, lien):
        self.lien = lien # type LienSequence
        PanelPropriete.__init__(self, parent, objet = self.lien)
        
        self.maxX = 800*SSCALE # Largeur de l'image "aperçu" zoomée
        self.sequence = self.lien.sequence
        print("PanelPropriete_LienSequence", self.lien, "---", self.lien.sequence)
        self.classe = None
        self.construire()
        self.parent = parent
        self.MiseAJour()
        
        
    #############################################################################            
    def GetDocument(self):
        return self.lien.parent


    #############################################################################            
    def construire(self):
#         print("construire")
        if self.sequence is not None:
            classe = self.sequence.classe
            ref = self.sequence.GetReferentiel()
        else:
            classe = self.GetDocument().classe
            ref = classe.GetReferentiel()
            
        
        #
        # Intitulé de la séquence
        #
        sbi = myStaticBox(self, -1, "Intitulé de la Séquence", size = (200*SSCALE,-1))
        sbsi = wx.StaticBoxSizer(sbi,wx.HORIZONTAL)
        self.intit = TextCtrl_Help(self, "", scale = SSCALE)
        self.intit.SetMinSize((-1, 20*SSCALE))
        self.intit.SetTitre("Intitulé de la Séquence", 
                            images.Icone_sequence.GetBitmap())
        self.intit.SetToolTip("")
        sbsi.Add(self.intit,1, flag = wx.EXPAND)
#        self.Bind(wx.EVT_TEXT, self.EvtText, self.intit)
        self.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.intit)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.intit)
        
        
        #
        # Sélection du fichier de séquence
        #
        sb0 = myStaticBox(self, -1, "Fichier de la Séquence", size = (200*SSCALE,-1))
        sbs0 = wx.StaticBoxSizer(sb0,wx.HORIZONTAL)
        self.texte = wx.TextCtrl(self, -1, toSystemEncoding(self.lien.path), size = (250*SSCALE, -1),
                                 style = wx.TE_PROCESS_ENTER)
#         bt2 = wx.BitmapButton(self, 101, wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE))
        bt2 = wx.BitmapButton(self, 101, scaleImage(images.Icone_fichier.GetBitmap(), 16*SSCALE, 16*SSCALE))
        bt2.SetToolTip("Sélectionner un fichier")
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnText, self.texte)
        self.texte.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocus)
        sbs0.Add(self.texte, flag = wx.ALIGN_CENTER)
        sbs0.Add(bt2)


        #
        # Position de la séquence
        #
        if self.sequence is not None:
            bmp = self.sequence.getBitmapPeriode(300*SSCALE)
        else:
            bmp = classe.getBitmapPeriode(300*SSCALE)
        titre = myStaticBox(self, -1, "Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        self.bmp = wx.StaticBitmap(self, -1, bmp)
        sb.Add(self.bmp, flag = wx.EXPAND)
        
        if self.sequence is not None:
            position = self.sequence.position
        else:
            position = [0, 0]
        self.position = PositionCtrl(self, position, 
                                     ref.getPeriodeSpe(classe.specialite),
                                     totmax = ref.getNbrPeriodes())
        self.Bind(wx.EVT_SLIDER, self.onChanged)
        sb.Add(self.position, flag = wx.EXPAND)
        
        
        #
        # Aperçu de la séquence
        #
        size = (141*SSCALE, 200*SSCALE) # Rapport A4
        sb1 = myStaticBox(self, -1, "Aperçu de la Séquence", size = size)
        sbs1 = wx.StaticBoxSizer(sb1,wx.HORIZONTAL)
        sbs1.SetMinSize(size)
        self.apercu = StaticBitmapZoom(self, -1, size = size)
        if self.sequence is not None:
            self.apercu.SetLargeBitmap(self.sequence.GetApercu(self.maxX))
        sbs1.Add(self.apercu, 1)
        self.size = size
        
        
        #
        # Créneau
        #
        if isinstance(self.lien.parent, pysequence.Progression):
            sb2 = myStaticBox(self, -1, "Créneau horaire")
            sbs2 = wx.StaticBoxSizer(sb2,wx.HORIZONTAL)
            
            self.creneauCtrl = CreneauCtrl(self, self.lien.creneaux)
            sbs2.Add(self.creneauCtrl, 1)
            self.creneauCtrl.SetToolTip("Choisir les créneaux horaire de la Séquence")
            self.sizer.Add(sbs2, (0,2), (1,1), flag = wx.EXPAND|wx.ALL, border = 2)
    #         self.creneauCtrl = wx.RadioBox(self, -1, u"Créneau horaire", wx.DefaultPosition, wx.DefaultSize,
    #                                        [str(i+1) for i in range(constantes.NBR_CRENEAU)], 
    #                                        constantes.NBR_CRENEAU, wx.RA_SPECIFY_COLS
    #                                        )
    #         
    #         
    #         self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.creneauCtrl)
    #         #rb.SetBackgroundColour(wx.BLUE)
    #         self.creneauCtrl.SetToolTip(wx.ToolTip(u"Choisir le créneau horaire de la Séquence"))
                      
        
        #
        # Problématiques associées à(aux) CI/Thème(s)
        #
        sbp = myStaticBox(self, -1, ref._nomPb.Plur_(), size = (200*SSCALE,-1))
        sbsp = wx.StaticBoxSizer(sbp,wx.VERTICAL)
        if self.sequence is not None:
            self.panelPb = PanelProblematiques(self, self.sequence.CI)
            sbsp.Add(self.panelPb,1, flag = wx.EXPAND)

        #
        # Mise en place
        #
        self.sizer.Add(sbsi, (0,0), flag = wx.EXPAND|wx.ALL, border = 2)
        self.sizer.Add(sbs0, (1,0), flag = wx.EXPAND|wx.ALL, border = 2)
        self.sizer.Add(sb, (2,0), flag = wx.ALIGN_TOP|wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border = 2)
        self.sizer.Add(sbs1, (0,1), (3,1), flag = wx.EXPAND|wx.ALL, border = 2)
        
        self.sizer.Add(sbsp, (1,2), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)
        self.sizer.AddGrowableCol(2)
        self.sizer.AddGrowableRow(0)
        self.sizer.Layout()
    
#         locale2def()
    

    #############################################################################            
    def onChanged(self, evt):
        if self.sequence is not None:
            self.sequence.SetPosition(self.position.GetRange())
            self.SetBitmapPosition()
            self.GetDocument().Ordonner()
            t = "Changement de position de la séquence"
            self.GetDocument().GererDependants(self.sequence, t)
        
        
        
    #############################################################################            
    def OnClick(self, event):
        mesFormats = "Séquence (.seq)|*.seq|" \
                       "Tous les fichiers|*.*'"
                       
        dlg = wx.FileDialog(self, "Sélectionner un fichier séquence",
                            defaultFile = "",
                            wildcard = mesFormats,
#                           defaultPath = globdef.DOSSIER_EXEMPLES,
                            style = wx.DD_DEFAULT_STYLE
                            #| wx.DD_DIR_MUST_EXIST
                            #| wx.DD_CHANGE_DIR
                            )

        if dlg.ShowModal() == wx.ID_OK:
            self.lien.setPath(dlg.GetPath())
            self.lien.ChargerSequence()
            self.lien.GetApp().arbre.ReSelectItem(self.lien.branche)
#             
#             self.__init__(self.parent, self.lien)
#             self.sequence = self.lien.sequence
#             self.construire()
#             self.MiseAJour(sendEvt = True)
        dlg.Destroy()
        
        self.SetFocus()
        
        
    #############################################################################            
    def OnText(self, event):
        """ Modification du nom du fichier du LienSequence
        """
        self.lien.path = event.GetString()
        self.MiseAJour()
        event.Skip()     

#     #############################################################################            
#     def EvtRadioBox(self, event):
#         self.lien.creneau = event.GetInt()
#         self.sendEvent(modif = u"Modification du créneau horaire %s %s" % (self.lien.article_c_obj, self.lien.nom_obj))
        
    #############################################################################            
    def OnChangeCreneau(self):
        self.sendEvent(modif = "Modification des créneaux horaire %s" % self.lien.du_(),
                       draw = True, verif = True)



    #############################################################################            
    def OnCheck(self, event):
        """ Selection d'une problématique
        """
        button_selected = event.GetEventObject().GetId()-200 
        
        if event.GetEventObject().IsChecked():
            self.sequence.CI.AddNum(button_selected)
        else:
            self.sequence.CI.DelNum(button_selected)
        
        if len(self.group_ctrls[button_selected]) > 2:
            self.group_ctrls[button_selected][2].Show(event.GetEventObject().IsChecked())
        
#        self.panel_cible.bouton[button_selected].SetState(event.GetEventObject().IsChecked())
#        if self.CI.GetTypeEnseignement() == 'ET':
        if self.sequenceCI.GetReferentiel().CI_cible:
            self.panel_cible.GererBoutons(True)
        
            if hasattr(self, 'b2CI'):
                self.b2CI.Enable(len(self.sequenceCI.numCI) <= 2)
        
        self.Layout()
        ref = self.sequenceCI.parent.classe.referentiel
        self.sendEvent(modif = "Modification des %s abordés" %ref._nomCI.plur_(),
                       draw = True, verif = True)



    #############################################################################            
    def EvtText(self, event):
#         print "EvtText"
        if event.GetEventObject() == self.intit:
            self.sequence.SetText(self.intit.GetText())
            self.lien.MiseAJourArbre()
            t = "Modification de l'intitulé de la Séquence"
            self.GetDocument().GererDependants(self.sequence, t)
            
        if self.onUndoRedo():
            self.sendEvent(modif = t, draw = True, verif = False)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = t, draw = True, verif = False)
                self.eventAttente = True
                             
    #############################################################################            
    def OnLoseFocus(self, event):
        return  
#        self.lien.path = toFileEncoding(self.texte.GetValue())
#        self.MiseAJour()
#        event.Skip()   

    #############################################################################            
    def SetBitmapPosition(self, bougerSlider = None):
        self.bmp.SetBitmap(self.sequence.getBitmapPeriode(300*SSCALE))
        self.position.SetValue(self.sequence.position)
        
    
    
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#         print("MiseAJour PanelPropriete_LienSequence", self.lien, sendEvt)

#        self.intit.SetLabel(self.sequence.intitule)
        if self.sequence is None:
            return
        
        self.intit.SetValue(self.sequence.intitule, False)
#         SetValue  : voir orthographe.STC_ortho
#         ChangeValue ?

        self.texte.SetValue(toSystemEncoding(self.lien.path))

    
#        try:
        if os.path.isfile(self.lien.path):
#             fichier = open(self.lien.path,'r')
            pass
            
        else:
            abspath = os.path.join(self.GetDocument().GetPath(), self.lien.path)
            if os.path.isfile(abspath):
#                 fichier = open(abspath,'r')
                pass
            else:
                self.texte.SetBackgroundColour("pink")
                self.texte.SetToolTip("Le fichier Séquence est introuvable !")
                return False

        self.texte.SetBackgroundColour("white")
        self.texte.SetToolTip("Lien vers un fichier Séquence")
        
        if hasattr(self, 'creneauCtrl'):
            self.creneauCtrl.MiseAJour()
        
        self.position.MiseAJour()
        self.panelPb.MiseAJour()
        
        self.MiseAJourApercu()
        
       
        if sendEvt:
#             print("sendEvent !")
            self.sendEvent(draw = True, verif = True)
            
        return True
    
    
    #############################################################################            
    def MiseAJourApercu(self, sendEvt = False):
        #
        # Aperçu
        #
        if self.sequence is not None:
            self.apercu.SetLargeBitmap(self.sequence.GetApercu(self.maxX))
        self.lien.SetLabel()

        self.Layout()
        
        if sendEvt:
            self.sendEvent(draw = False, verif = False)
            
        return True
    
    
    


####################################################################################
#
#   Classe définissant le panel de propriété d'un lien vers une séquence
#
####################################################################################
class PanelPropriete_LienProjet(PanelPropriete):
    def __init__(self, parent, lien):
        self.lien = lien
        PanelPropriete.__init__(self, parent, objet = self.lien)
        
        self.maxX = 800*SSCALE # Largeur de l'image "aperçu" zoomée
        self.projet = self.lien.projet
        self.classe = None
        self.construire()
        self.parent = parent
        self.MiseAJour()
        
        
    #############################################################################            
    def GetDocument(self):
        return self.lien.parent

    #############################################################################            
    def construire(self):
        
        ref = self.projet.GetReferentiel()
        
        #
        # Intitulé du Projet
        #
        sbi = myStaticBox(self, -1, "Intitulé du Projet", size = (200*SSCALE,-1))
        sbsi = wx.StaticBoxSizer(sbi,wx.HORIZONTAL)
        self.intit = TextCtrl_Help(self, "", scale = SSCALE)
        self.intit.SetTitre("Intitulé du Projet", self.projet.getIcone())
        self.intit.SetToolTip("")
        
        sbsi.Add(self.intit,1, flag = wx.EXPAND)
#        self.Bind(wx.EVT_TEXT, self.EvtText, self.intit)
#         self.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.intit)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.intit)
        
        #
        # Sélection du fichier de Projet
        #
        sb0 = myStaticBox(self, -1, "Fichier du Projet", size = (200*SSCALE,-1))
        sbs0 = wx.StaticBoxSizer(sb0,wx.HORIZONTAL)
        self.texte = wx.TextCtrl(self, -1, toSystemEncoding(self.lien.path), size = (250*SSCALE, -1),
                                 style = wx.TE_PROCESS_ENTER)
        bt2 = wx.BitmapButton(self, 101, scaleImage(images.Icone_fichier.GetBitmap(), 16*SSCALE, 16*SSCALE))
        bt2.SetToolTip("Sélectionner un fichier")
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnText, self.texte)
        self.texte.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocus)
        sbs0.Add(self.texte, flag = wx.ALIGN_CENTER)
        sbs0.Add(bt2)


        #
        # Position du Projet
        #
        titre = myStaticBox(self, -1, "Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        self.bmp = wx.StaticBitmap(self, -1, self.projet.getBitmapPeriode(300*SSCALE))
        self.position = PositionCtrl(self, self.projet.position, 
                                     ref.getPeriodeSpe(self.projet.classe.specialite),
                                     totmax = ref.getNbrPeriodes()
                                     )
#         self.Bind(wx.EVT_RADIOBUTTON, self.onChanged)
        self.Bind(wx.EVT_SLIDER, self.onChanged)
        sb.Add(self.bmp, flag = wx.EXPAND)
        sb.Add(self.position, flag = wx.EXPAND)
        
        
        
        
        #
        # Aperçu du Projet
        #
        size = (141,200) # Rapport A4
        sb1 = myStaticBox(self, -1, "Aperçu du Projet", size = size)
        sbs1 = wx.StaticBoxSizer(sb1,wx.HORIZONTAL)
        sbs1.SetMinSize(size)
        self.apercu = StaticBitmapZoom(self, -1, size = size)
        self.apercu.SetLargeBitmap(self.projet.GetApercu(self.maxX))
        sbs1.Add(self.apercu, 1)
        self.size = size
        
        #
        # Créneau horaire
        #
        sb2 = myStaticBox(self, -1, "Créneau horaire")
        sbs2 = wx.StaticBoxSizer(sb2,wx.HORIZONTAL)
        
        self.creneauCtrl = CreneauCtrl(self, self.lien.creneaux)
        sbs2.Add(self.creneauCtrl, 1)
        self.creneauCtrl.SetToolTip(wx.ToolTip("Choisir les créneaux horaire du projet"))



        #
        # Problématiques associées à(aux) CI/Thème(s)
        #
        sbp = myStaticBox(self, -1, ref._nomPb.Sing_(), size = (200*SSCALE,-1))
        sbsp = wx.StaticBoxSizer(sbp,wx.VERTICAL)
        self.panelPb = TextCtrl_Help(self, "", scale = SSCALE)
        self.panelPb.SetTitre(ref.nomPb)
        self.panelPb.SetToolTip("")
        
#         self.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.panelPb)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.panelPb)
        sbsp.Add(self.panelPb,1, flag = wx.EXPAND)

        
        self.sizer.Add(sbsi, (0,0), flag = wx.EXPAND|wx.ALL, border = 2)
        self.sizer.Add(sbs0, (1,0), flag = wx.EXPAND|wx.ALL, border = 2)
        self.sizer.Add(sb, (2,0), flag = wx.ALIGN_TOP|wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border = 2)
        self.sizer.Add(sbs1, (0,1), (3,1), flag = wx.EXPAND|wx.ALL, border = 2)
        self.sizer.Add(sbs2, (0,2), (1,1), flag = wx.EXPAND|wx.ALL, border = 2)
        self.sizer.Add(sbsp, (1,2), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)
        self.sizer.AddGrowableCol(2)
        
        self.sizer.Layout()
        

    #############################################################################            
    def onChanged(self, evt):
        self.projet.SetPosition(self.position.GetRange())
        self.SetBitmapPosition()
        self.GetDocument().Ordonner()
        t = "Changement de position du Projet"
        self.GetDocument().GererDependants(self.projet, t)
        
        
        
    #############################################################################            
    def OnClick(self, event):
        mesFormats = constantes.FORMAT_FICHIER['prj'] + constantes.TOUS_FICHIER
        dlg = wx.FileDialog(self, "Sélectionner un fichier Projet",
                            defaultFile = "",
                            wildcard = mesFormats,
#                           defaultPath = globdef.DOSSIER_EXEMPLES,
                            style = wx.DD_DEFAULT_STYLE
                            #| wx.DD_DIR_MUST_EXIST
                            #| wx.DD_CHANGE_DIR
                            )

        if dlg.ShowModal() == wx.ID_OK:
            self.lien.setPath(dlg.GetPath())
            self.MiseAJour(sendEvt = True)
        dlg.Destroy()
        
        self.SetFocus()
        
        
    #############################################################################            
    def OnText(self, event):
        """ Modification du nom du fichier du LienProjet
        """
        self.lien.path = event.GetString()
        self.MiseAJour()
        event.Skip()     

    #############################################################################            
    def OnChangeCreneau(self):
    
        self.sendEvent(modif = "Modification des créneaux horaire %s" %self.lien.du_(),
                       draw = True, verif = True)
        
     

    #############################################################################            
    def EvtText(self, event):
        if event.GetEventObject() == self.intit:
            self.projet.SetText(self.intit.GetText())
            self.lien.MiseAJourArbre()
            t = "Modification de l'intitulé du projet"
            self.GetDocument().GererDependants(self.projet, t)
        
        elif event.GetEventObject() == self.panelPb:
            self.projet.SetProblematique(self.panelPb.GetText())
            self.lien.MiseAJourArbre()
            t = "Modification de la promblématique du projet"
            self.GetDocument().GererDependants(self.projet, t)
            
        if self.onUndoRedo():
            self.sendEvent(modif = t, draw = True, verif = False)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = t, draw = True, verif = False)
                self.eventAttente = True
                             
    #############################################################################            
    def OnLoseFocus(self, event):
        return  
#        self.lien.path = toFileEncoding(self.texte.GetValue())
#        self.MiseAJour()
#        event.Skip()   

    #############################################################################            
    def SetBitmapPosition(self, bougerSlider = None):
        self.bmp.SetBitmap(self.projet.getBitmapPeriode(300))
        self.position.SetValue(self.projet.position)
        
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "MiseAJour PanelPropriete_LienSequence", self.lien

#        self.intit.SetLabel(self.sequence.intitule)
        self.intit.SetValue(self.projet.intitule, False)
        self.panelPb.SetValue(self.projet.problematique, False)
        self.texte.SetValue(toSystemEncoding(self.lien.path))

        if os.path.isfile(self.lien.path):
#             fichier = open(self.lien.path,'r')
            pass
            
        else:
            abspath = os.path.join(self.GetDocument().GetPath(), self.lien.path)
            if os.path.isfile(abspath):
#                 fichier = open(abspath,'r')
                pass
            else:
                self.texte.SetBackgroundColour("pink")
                self.texte.SetToolTip("Le fichier Projet est introuvable !")
                return False
        
        self.texte.SetBackgroundColour("white")
        self.texte.SetToolTip("Lien vers un fichier Projet")
        
        self.creneauCtrl.MiseAJour()
        
        self.position.MiseAJour()
        
        self.MiseAJourApercu()
        
        if sendEvt:
            self.sendEvent(draw = True, verif = True)
            
        return True
    
    
    #############################################################################            
    def MiseAJourApercu(self, sendEvt = False):
        #
        # Aperçu
        #
        self.apercu.SetLargeBitmap(self.projet.GetApercu(self.maxX))
        self.lien.SetLabel()

        self.Layout()
        
        if sendEvt:
            self.sendEvent(draw = False, verif = False)
            
        return True
    
    
      
    
    
    
####################################################################################
#
#   Classe définissant le panel de propriété de la compétence
#
####################################################################################
class PanelPropriete_Competences(PanelPropriete):
    def __init__(self, parent, competences, code, compFiltre, compRef):
        """ <competences> : type pysequence.Competences
            <code> : 
            <compFiltre> : dictionnaire des compétences à afficher dans l'abre (sortie de GetDicFiltre())
            <compRef> : type referentiel.Competences
        """
#         print("PanelPropriete_Competences", code)

        self.competences = competences  # pysequence.Competences
        self.code = code
        self.compFiltre = compFiltre
        
        PanelPropriete.__init__(self, parent, objet = self.competences)
        
#         self.nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
        
#         self.sizer.Add(self.nb, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        
        self.construire(compRef)
        
        self.Layout()
        
        
    ######################################################################################  
    def construire(self, compRef):
        """ Création de l'arbre
        """
        if self.code == "F": # Cas particulier des Fonctions
            self.arbre = ArbreFonctionsPrj(self, self.code, compRef,
                                           self, agwStyle = HTL.TR_NO_HEADER)
            
        else:
            self.arbre = ArbreCompetences(self, self.code, self.compFiltre, compRef, None, 
                                          self, agwStyle = HTL.TR_NO_HEADER)
        
        
        self.sizer.Add(self.arbre, (0,0), flag = wx.EXPAND)
        
        self.MiseAJour()
        
        self.Layout()


    #############################################################################            
    def GetDocument(self):
        return self.competences.parent
    

    ######################################################################################  
    def OnSize(self, event):
        self.win.SetMinSize(self.GetClientSize())
        self.Layout()
        event.Skip()
        
    
    ######################################################################################  
    def AjouterEnleverCompetences(self, app, rem, compRef):
        for s in app:
            if not s in self.competences.competences:
                self.competences.competences.append(s)
        for s in rem:
            if s in self.competences.competences:
                self.competences.competences.remove(s)
#         self.competences.SetCodeBranche()
        
        
    ######################################################################################  
    def AjouterCompetence(self, code, propag = None):
#         print "AjouterCompetence", code
        if not code in self.competences.competences:
            self.competences.competences.append(code)
            self.competences.GererElementsDependants(code)
            self.competences.SetCodeBranche()
        
        
    ######################################################################################  
    def EnleverCompetence(self, code, propag = None):
        if code in self.competences.competences:
            self.competences.competences.remove(code)
            self.competences.GererElementsDependants(code)
            self.competences.SetCodeBranche()
        
        
    ######################################################################################  
    def SetCompetences(self): 
        self.competences.GererElementsDependants()
        self.competences.SetCodeBranche()
        self.competences.parent.Verrouiller()
        self.sendEvent(modif = "Ajout/suppression d'une compétence", 
                       draw = True, verif = True)
        
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        """ On coche tout ce qui doit l'être dans les différents arbres
        """
#         print("MiseAJour compétences")
#        print "  ", self.arbre.items.keys()
#        print "   ", self.competence.competences


#         def checkArbre(arbre):
#             print arbre.items.keys()
        self.arbre.UnselectAll()
        for s in self.competences.competences:
            if self.code == s[0]:
#                 print "  ", s
                if s[1:] in list(self.arbre.items.keys()):
                    self.arbre.CheckItem2(self.arbre.items[s[1:]])
                    self.arbre.AutoCheckChild(self.arbre.items[s[1:]], True)
        
#         for arbre in self.arbres.values():
#             checkArbre(arbre)  
#        self.arbre.UnselectAll()
#        for s in self.competence.competences:
#            if s in self.arbre.items.keys():
#                self.arbre.CheckItem2(self.arbre.items[s])
                    
                    
#        if hasattr(self, 'arbreSpe'):
#            checkArbre(self.arbreSpe)  
#            
#        
#        if hasattr(self, 'arbreFct'):
#            checkArbre(self.arbreFct)  
#            
            
#        for s in self.competence.competences:
#            
#            i = self.arbre.get_item_by_label(s, self.arbre.GetRootItem())
#            print s, 
#            print i, i.IsOk()
#            if i.IsOk():
#                self.arbre.CheckItem2(i)
        
        if sendEvt:
            self.sendEvent(draw = True, verif = True)
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
    def __init__(self, parent, savoirs, code, savFiltre, savRef, filtre = None):
        """ <savoirs> : type pysequence.Savoirs
            <code> : 
            <savFiltre> : dictionnaire des savoirs à afficher dans l'abre (sortie de GetDicFiltre())
            <savRef> : type referentiel.Savoirs
        """
        self.savoirs = savoirs      # pysequence.Savoirs
        self.savRef = savRef    # referentiel.Savoirs
        self.code = code
        self.filtre = filtre
        self.prerequis = savoirs.prerequis
        
        PanelPropriete.__init__(self, parent, objet = self.savoirs)
        
#         self.nb = wx.Notebook(self, -1, size = (21,21), style= wx.BK_DEFAULT)
        
#         self.sizer.Add(self.nb, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(0)
            
        self.construire(savFiltre)
        
        self.Layout()


    #############################################################################            
    def GetDocument(self):
        return self.savoirs.parent

    ######################################################################################  
    def GetReferentiel(self):
        return self.savoirs.GetReferentiel()

#     ######################################################################################  
#     def CreerPage(self, nom):
#         bg_color = self.Parent.GetBackgroundColour()
#         page = PanelPropriete(self.nb, objet = self.savoirs)
#         page.SetBackgroundColour(bg_color)
#         self.nb.AddPage(page, nom)
#         return page


    ######################################################################################  
    def construire(self, savFiltre):
#         for code, savoir in dicSavoirs:
        if (self.prerequis and self.savRef.pre) or (not self.prerequis and self.savRef.obj):
#                 self.pagesSavoir.append(self.CreerPage(savoir.nomDiscipline))
            self.arbre = ArbreSavoirs(self, self.code, savFiltre, self.savRef, filtre = self.filtre)#, self.savoirs)
            self.sizer.Add(self.arbre, (0,0), flag = wx.EXPAND)
            
            if int(wx.version()[0]) > 2:
                if not self.sizer.IsColGrowable(0):
                    self.sizer.AddGrowableCol(0)
                if not self.sizer.IsRowGrowable(0):
                    self.sizer.AddGrowableRow(0)
            else:
                try:
                    self.sizer.AddGrowableCol(0)
                except:
                    pass
                try:
                    self.sizer.AddGrowableRow(0)
                except:
                    pass
            self.Layout()
        
        self.MiseAJour()
        
        self.sizer.Layout()
        
    
    
    ######################################################################################  
    def AjouterEnleverSavoirs(self, app, rem, savRef):
        for s in app:
            if not s in self.savoirs.savoirs:
                self.savoirs.savoirs.append(s)
        for s in rem:
            if s in self.savoirs.savoirs:
                self.savoirs.savoirs.remove(s)
        self.savoirs.SetCodeBranche()
    
    
    ######################################################################################  
    def AjouterSavoir(self, code, propag = None):
#         print "AjouterCompetence", code
        self.savoirs.savoirs.append(code)
        self.savoirs.GererElementsDependants()
        self.savoirs.SetCodeBranche()

        
    ######################################################################################  
    def EnleverSavoir(self, code, propag = None):
        if code in self.savoirs.savoirs:
            self.savoirs.savoirs.remove(code)
            self.savoirs.GererElementsDependants()
            self.savoirs.SetCodeBranche()


    ######################################################################################  
    def SetSavoirs(self): 
        self.savoirs.parent.Verrouiller()
        self.sendEvent(modif = "Ajout/suppression d'un Savoir", 
                       draw = True, verif = True)
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        """ Coche tous les savoirs a True de self.savoirs.savoirs 
            dans les différents arbres
        """
#         print("MiseAJour Savoirs", self.code, self.arbre.items)
#         print self.code

        if hasattr(self, 'arbre'):
#             self.arbre.ExpandAll()
            for s in self.savoirs.savoirs:
                if self.code == s[0]:
                    if not s[1:] in self.arbre.items:
                        print("ERREUR : ")
                        continue
#                     print("   ", s[1:])
                    i = self.arbre.items[s[1:]]
#                     i = self.arbre.get_item_by_label(s[1:], self.arbre.GetRootItem())
#                     print("       ", i)
                    if i is not None and i.IsOk():
                        self.arbre.CheckItem2(i)
                        self.arbre.AutoCheckChild(i, True)
#             self.arbre.OnSelChanged()
#        for code, arbre in self.arbres.items():
#            arbre.UnselectAll()
#            for s in self.savoirs.savoirs:
#                if s[0] == arbre.savoir.code[0]: 
#                    i = arbre.get_item_by_label(s[1:], arbre.GetRootItem())
#                    if i.IsOk():
#                        arbre.CheckItem2(i)
        
        
#        self.arbre.UnselectAll()
#        for s in self.savoirs.savoirs:
##            print "  ",s
##            typ, cod = s[0], s[1:]
#            typ = s[0]
#            if typ == "S": # Savoir spécialité STI2D
#                i = self.arbreSpe.get_item_by_label(s[1:], self.arbreSpe.GetRootItem())
#                if i.IsOk():
#                    self.arbreSpe.CheckItem2(i)
#            elif typ == "M": # Savoir Math
#                i = self.arbreM.get_item_by_label(s[1:], self.arbreM.GetRootItem())
#                if i.IsOk():
#                    self.arbreM.CheckItem2(i)
#            elif typ == "P": # Savoir Physique
#                i = self.arbreP.get_item_by_label(s[1:], self.arbreP.GetRootItem())
#                if i.IsOk():
#                    self.arbreP.CheckItem2(i)
#            else:
#                i = self.arbre.get_item_by_label(s[1:], self.arbre.GetRootItem())
#                if i.IsOk():
#                    self.arbre.CheckItem2(i)
        
        if sendEvt:
            self.sendEvent(draw = True, verif = True)
            
    #############################################################################            
    def MiseAJourTypeEnseignement(self):
        self.construire()

            
####################################################################################
#
#   Classe définissant le panel de propriété de la séance
#
####################################################################################
class PanelPropriete_Seance(PanelPropriete):
    def __init__(self, parent, seance):
        self.seance = seance
        PanelPropriete.__init__(self, parent, objet = self.seance)
        
        ref = self.GetReferentiel()
        
        #
        # Un notebook pour les différentes catégories de propriété
        #
        self.nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
        pageGen = PanelPropriete(self.nb, panelRacine = self, objet = self.seance)
        self.pageGen = pageGen
        bg_color = self.Parent.GetBackgroundColour()
        pageGen.SetBackgroundColour(bg_color)
#         self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.nb.AddPage(pageGen, "Propriétés générales")
        self.sizer.Add(self.nb, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        
        #
        # Organisation sur 3 colonnes
        #
        c0 = wx.BoxSizer(wx.VERTICAL)
        pageGen.sizer.Add(c0, (0,0), (1,1), flag = wx.ALL|wx.EXPAND, border = 2)
        c1 = wx.BoxSizer(wx.VERTICAL)
        pageGen.sizer.Add(c1, (0,1), (1,1), flag = wx.ALL|wx.EXPAND, border = 2)
        c2 = wx.BoxSizer(wx.VERTICAL)
        pageGen.sizer.Add(c2, (0,2), (1,1), flag = wx.ALL|wx.EXPAND, border = 2)
        
        
        #
        # Intitulé de la séance
        #
        box = myStaticBox(pageGen, -1, "Intitulé "+ref._nomActivites.du_())
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
#         textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        textctrl = orthographe.STC_ortho(pageGen, -1)
        textctrl.SetTitre("Intitulé "+ref._nomActivites.du_())
        textctrl.SetToolTip("")
        
        
        bsizer.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
#        self.Bind(wx.EVT_TEXT, self.EvtTextIntitule, textctrl)
        self.textctrl.Bind(wx.EVT_LEAVE_WINDOW, self.EvtTextIntitule)
        self.textctrl.Bind(wx.EVT_KILL_FOCUS, self.EvtTextIntitule)
#         pageGen.sizer.Add(bsizer, (0,0), (3,1), flag = wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, border = 2)
        c0.Add(bsizer, 1, flag = wx.ALL|wx.EXPAND, border = 2)    
        
        
        # 2 élémenents en horizontal :
        sto = wx.BoxSizer(wx.HORIZONTAL)
        c0.Add(sto, flag = wx.ALL|wx.EXPAND, border = 2) 
        
        c00 = wx.BoxSizer(wx.VERTICAL)
        sto.Add(c00, flag = wx.ALL|wx.EXPAND, border = 2)
        
        #
        # Type de séance
        #
        titre = wx.StaticText(pageGen, -1, "Type %s :" %ref._nomActivites.de_())
        listType = self.seance.GetListeTypes()
        listTypeS = [(ref.seances[t][1], scaleImage(constantes.imagesSeance[t].GetBitmap(), 24*SSCALE, 24*SSCALE)) for t in listType] 
        tsizer = wx.BoxSizer(wx.VERTICAL)
        cbType = combo_adv.BitmapComboBox(pageGen, -1, "Choisir un type %s" %ref._nomActivites.du_(),
                             choices = [],# size = (-1,25),
                             style = wx.CB_DROPDOWN
                             | wx.TE_PROCESS_ENTER
                             | wx.CB_READONLY
                             #| wx.CB_SORT
                             )
        
        self.cbType = cbType
        for s in listTypeS:
            self.cbType.Append(s[0], s[1])
        
        cbType.SetInitialSize() 
        
#         self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbType)
        
        
        tsizer.Add(titre, flag = wx.ALIGN_LEFT|wx.LEFT, border = 2)
        tsizer.Add(cbType, flag = wx.EXPAND|wx.LEFT, border = 2)
#         pageGen.sizer.Add(tsizer, (3,0), (2, 1), flag = wx.EXPAND|wx.ALL, border = 2)
        c00.Add(tsizer, flag = wx.EXPAND|wx.ALL, border = 2)


        #
        # Enseignement Spécifique
        #
        self.speSizer = wx.BoxSizer(wx.VERTICAL)
        c00.Add(self.speSizer, flag = wx.EXPAND|wx.ALL, border = 2)
        # reste déplacé dans AdapterAuType()
        
        
        #
        # Démarche
        #
        self.demSizer = wx.BoxSizer(wx.VERTICAL)
        c00.Add(self.demSizer, flag = wx.EXPAND|wx.ALL, border = 2)
        # reste déplacé dans AdapterAuType()
        
        
        #
        # Organisation
        #
        box2 = myStaticBox(pageGen, -1, "Organisation")
        self.bsizer2 = wx.StaticBoxSizer(box2, wx.VERTICAL)
        sto.Add(self.bsizer2, flag = wx.EXPAND)
        # reste déplacé dans AdapterAuType()
        
        
        #
        # Systèmes
        #
        self.box = myStaticBox(pageGen, -1, ref._nomSystemes.Plur_()+" nécessaires", size = (200*SSCALE,200*SSCALE))
        self.box.SetMinSize((200*SSCALE,200*SSCALE))
        self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        self.systemeCtrl = []
        self.ConstruireListeSystemes()
        c1.Add(self.bsizer, 1, flag = wx.EXPAND|wx.ALL, border = 2)

        
        
        #
        # Description de la séance
        #
        dbox = myStaticBox(pageGen, -1, "Description")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
#        bd = wx.Button(self, -1, u"Editer")
        tc = richtext.RichTextPanel(pageGen, self.seance, toolBar = True)
        tc.SetTitre("Description détaillée "+ref._nomActivites.du_())
        tc.SetToolTip("")
#        tc.SetMaxSize((-1, 150))
#        dbsizer.Add(bd, flag = wx.EXPAND)
        dbsizer.Add(tc, 1, flag = wx.EXPAND)
#        self.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        c2.Add(dbsizer, 1, flag = wx.EXPAND|wx.ALL, border = 2)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        #
        # Lien
        #
        lsizer = self.CreateLienSelect(pageGen)
        c2.Add(lsizer, flag = wx.EXPAND|wx.ALL, border = 2)



        
        
        
        
        doc = self.seance.GetDocument()
        
        #
        # Compétences
        #
        pageCmp = PanelPropriete(self.nb, panelRacine = self, objet = self.seance)
        pageCmp.SetBackgroundColour(bg_color)
        self.nb.AddPage(pageCmp, doc.obj["C"].GetNomGenerique())
        self.pageCmp = pageCmp
        
        self.cmpSizer = wx.BoxSizer(wx.VERTICAL)
        pageCmp.sizer.Add(self.cmpSizer, (0,0), flag = wx.EXPAND)
        
        self.dicComp = {}
        for c in doc.obj["C"].competences:
            if c[0] != 'F':
                if c[0] in self.dicComp.keys():
                    self.dicComp[c[0]].append(c[1:])
                else:
                    self.dicComp[c[0]] = [c[1:]]
        # reste déplacé dans AdapterAuType()
        
        
        
        #
        # Savoirs
        #
        pageSav = PanelPropriete(self.nb, panelRacine = self, objet = self.seance)
        pageSav.SetBackgroundColour(bg_color)
        self.nb.AddPage(pageSav, doc.obj["S"].GetNomGenerique())
        self.pageSav = pageSav
        
        self.savSizer = wx.BoxSizer(wx.VERTICAL)
        pageSav.sizer.Add(self.savSizer, (0,0), flag = wx.EXPAND)
        
        self.dicSav = {}
        for c in doc.obj["S"].savoirs:
            if c[0] in self.dicSav.keys():
                self.dicSav[c[0]].append(c[1:])
            else:
                self.dicSav[c[0]] = [c[1:]]
        # reste déplacé dans AdapterAuType()
        
        
        #
        # Proprietés d'affichage
        #
        pageAff = PanelPropriete(self.nb, panelRacine = self, objet = self.seance)
        pageAff.SetBackgroundColour(bg_color)
        self.nb.AddPage(pageAff, "Apparence")
        
        #
        # Apparence
        #
        
        box2 = myStaticBox(pageAff, -1, "Affichage de l'intitulé")
        bsizer3 = wx.StaticBoxSizer(box2, wx.VERTICAL)
        
        b = csel.ColourSelect(pageAff, -1, "Couleur du texte", couleur.GetCouleurWx(self.seance.couleur), size = (200*SSCALE,-1))
        
        bsizer3.Add(b, flag = wx.ALL, border = 2)
        
        b.Bind(csel.EVT_COLOURSELECT, self.OnSelectColour)
        self.coulCtrl = b
        
        cb = wx.CheckBox(pageAff, -1, "Afficher l'intitulé dans la zone de déroulement")
#         print "+++", cb.Value
        cb.SetToolTip("Décocher pour afficher l'intitulé\nen dessous de la zone de déroulement de la séquence")
        cb.SetValue(self.seance.intituleDansDeroul)
        bsizer3.Add(cb, flag = wx.EXPAND|wx.ALL, border = 2)
        
        vcTaille = VariableCtrl(pageAff, seance.taille, signeEgal = True, slider = False, sizeh = 40*SSCALE,
                                help = "Taille des caractères", unite = "%", scale = SSCALE)
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcTaille)
        bsizer3.Add(vcTaille, flag = wx.EXPAND|wx.ALL, border = 2)
        self.vcTaille = vcTaille
        
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
        self.cbInt = cb
        
        pageAff.sizer.Add(bsizer3, (0,0), (1,1), flag =wx.ALL|wx.EXPAND, border = 2)
        
        
        #
        # Icônes
        #
        isizer = self.CreateIconeSelect(pageAff)
        pageAff.sizer.Add(isizer, (0,1), (1, 1), 
                          flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        #
        # Image
        #
        isizer = self.CreateImageSelect(pageAff, 
                                        titre = "Illustration "+ref._nomActivites.du_())
        pageAff.sizer.Add(isizer, (0,2), (1,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.ALL, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        
        
        self.AdapterAuType()
        self.MiseAJour()
        self.pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboBox)
        
        #
        # Mise en place
        #
        pageGen.sizer.AddGrowableCol(2)
        pageGen.sizer.AddGrowableRow(0)

        pageAff.sizer.AddGrowableCol(1)
        pageAff.sizer.AddGrowableRow(0, 1)
        
        pageCmp.sizer.AddGrowableCol(0)
        pageCmp.sizer.AddGrowableRow(0)
        
        pageSav.sizer.AddGrowableCol(0)
        pageSav.sizer.AddGrowableRow(0)
        
#         pageGen.SetupScrolling(scroll_x = False, scroll_y = True)
#         self.SetupScrolling(scroll_x = False, scroll_y = False)
        
    
    
    #############################################################################            
    def AdapterAuType(self):
        """ Adapte le panel au type de séance
        """
#         print("AdapterAuType", self.seance)

        ref = self.GetReferentiel()
        

        #
        # Organisation
        #
        
        # Durée de la séance
        
        if hasattr(self, 'vcDuree'):
            try:
                self.bsizer2.Detach(self.vcDuree)
            except:
                pass
            self.vcDuree.Destroy()
            del self.vcDuree
        
        if not self.seance.EstSeance_RS():
            vcDuree = VariableCtrl(self.pageGen, self.seance.duree, coef = 0.25, 
                                   signeEgal = True, slider = False, sizeh = 30,
                                   help = "Durée %s en heures" %ref._nomActivites.du_(),
                                   unite = "h", scale = SSCALE)
            self.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
            self.vcDuree = vcDuree
            self.bsizer2.Add(vcDuree, flag = wx.EXPAND|wx.BOTTOM, border = 2)

        
        
        # Effectif
        
        if hasattr(self, 'cbEff'):
            try:
                self.bsizer2.Detach(self.cbEff)
                self.bsizer2.Detach(self.titreEff)
            except:
                pass
            self.cbEff.Destroy()
            self.titreEff.Destroy()
            del self.cbEff
            del self.titreEff
#         print("ref.effectifsSeance", ref.effectifsSeance)
        if self.seance.typeSeance in ref.effectifsSeance.keys() \
                and len(ref.effectifsSeance[self.seance.typeSeance]) > 0:
            titre = wx.StaticText(self.pageGen, -1, "Effectif : ")
            
#             cbEff = wx.ComboBox(self.pageGen, -1, "",
#                              choices = [],
#                              style = wx.CB_DROPDOWN
#                              | wx.TE_PROCESS_ENTER
#                              | wx.CB_READONLY
#                              #| wx.CB_SORT
#                              )
            cbEff = myComboTreeBox(self.pageGen, wx.ID_ANY, size=(300,-1))#,
#                              style = wx.CB_DROPDOWN
#                              | wx.TE_PROCESS_ENTER
#                              | wx.CB_READONLY
#                              #| wx.CB_SORT
#                              )
            self.cbEff = cbEff
            try:        # Erreur sous MacOS (?)
                self.cbEff.Clear()
            except:
                pass
            
            classe = self.seance.GetDocument().classe
            def construire(lst, parent = None, m = None):
                for dic in lst:
                    k, g = list(dic.items())[0]
#                     print("N=",classe.nbrGroupes[k])
                    if k == 'I' or classe.nbrGroupes[k] > 0:
                        child = cbEff.Append(classe.GetStrEffectifComplet(k, -1), 
                                             parent, clientData = k)
                        r = self.cbEff.GetTree().GetBoundingRect(child)
                        if r is not None:
                            m[0] = max(m[0], r.GetRight())# + r.GetWidth())
                        construire(g, child, m)
            
#             print("_effectifs", ref._effectifs)
            m = [0]
            treeEffectifs = ref.getTreeEffectifs(self.seance.typeSeance)
#             print("treeEffectifs", treeEffectifs)
            if len(treeEffectifs) > 0:
                construire(treeEffectifs, m = m)
    #             print("m=", m[0])
    #             self.cbEff.SetMinSize((m[0]+10, -1))
                
    #             listEff = ref.effectifsSeance[self.seance.typeSeance]
    #             for s in listEff:
    #                 self.cbEff.Append(self.seance.GetDocument().classe.GetStrEffectifComplet(s, -1))
    #             self.cbEff.SetSelection(0)
                self.cbEff.GetTree().SetWindowStyle(wx.TR_NO_BUTTONS)
                self.cbEff.ExpandAll()
    #             print("sel", list(ref.getTreeEffectifs()[0].keys())[0])
                self.cbEff.SetClientDataSelection(list(treeEffectifs[0].keys())[0])
            
            #, self.cbEff)
#             self.pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.cbEff)
            self.titreEff = titre
            
            self.bsizer2.Add(self.titreEff, flag = wx.LEFT|wx.BOTTOM, border = 2)
            self.bsizer2.Add(cbEff, flag = wx.EXPAND|wx.LEFT, border = 8)
            
    
        
        # Nombre de séances en parallèle
        
        if hasattr(self, 'vcNombre'):
            try:
                self.bsizer2.Detach(self.vcNombre)
            except:
                pass
            self.vcNombre.Destroy()
            del self.vcNombre
            
                
        if self.seance.typeSeance in ref.listeTypeActivite:
            vcNombre = VariableCtrl(self.pageGen, self.seance.nombre, signeEgal = True, slider = False, sizeh = 30,
                                    help = "Nombre de groupes réalisant simultanément %s" %ref._nomActivites.le_("même"),
                                    scale = SSCALE)
            self.Bind(EVT_VAR_CTRL, self.EvtText, vcNombre)
            self.vcNombre = vcNombre
            self.bsizer2.Add(vcNombre, flag = wx.EXPAND|wx.BOTTOM, border = 4)
            
                
            
        # Nombre de rotations
        
        if hasattr(self, 'vcNombreRot'):
            try:
                self.bsizer2.Detach(self.vcNombreRot)
                
            except:
                pass
            self.vcNombreRot.Destroy()
            del self.vcNombreRot
            
            
        if self.seance.typeSeance == "R":
            vcNombreRot = VariableCtrl(self.pageGen, self.seance.nbrRotations, signeEgal = True, slider = False, sizeh = 30,
                                    help = "Nombre de rotations successives", scale = SSCALE)
            self.Bind(EVT_VAR_CTRL, self.EvtText, vcNombreRot)
            self.vcNombreRot = vcNombreRot
            self.bsizer2.Add(vcNombreRot, flag = wx.EXPAND|wx.BOTTOM, border = 4)

            

        
        #
        # Démarche      
        #
        if hasattr(self, 'titreDem'):
#             try:
            self.demSizer.Detach(self.titreDem)
#             except:
#                 pass
            self.titreDem.Destroy()
            del self.titreDem
            
        
        if hasattr(self, 'cbDem'):
            if ref.multiDemarches:
                for cb in self.cbDem:
                    try:
                        self.speSizer.Detach(cb)
                        cb.Destroy()
                    except:
                        pass
                    
                    del cb
            else:
    #             try:
                self.demSizer.Detach(self.cbDem)
    #             except:
    #                 pass
                self.cbDem.Destroy()
                del self.cbDem
            
            
        
        if self.seance.typeSeance in ref.activites.keys():
            if len(ref.demarches) > 0:
                
                listDem = ref.demarcheSeance[self.seance.typeSeance]
                if ref.multiDemarches and len(listDem) > 1:
                    tit = ref._nomDemarches.Plur_()
                else:
                    tit = ref._nomDemarches.Sing_()
                tit += " " + ref._nomActivites.du_()
                titre = wx.StaticText(self.pageGen, -1, tit + " :")
                self.titreDem = titre
                self.demSizer.Add(titre, flag = wx.ALIGN_LEFT|wx.LEFT|wx.BOTTOM, border = 2)
                
                if ref.multiDemarches:
                    cbDem = []
                    for s in listDem:
                        cb = wx.CheckBox(self.pageGen, -1, ref.demarches[s][1],
                                             name = s)
                        cb.SetToolTip(ref.demarches[s][1])
                        cb.SetForegroundColour(ref.demarches[s][3])
                        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxDem, cb)
                        self.demSizer.Add(cb, flag = wx.EXPAND|wx.LEFT, border = 8)
                        cbDem.append(cb) 
                else:
                    cbDem = wx.ComboBox(self.pageGen, -1, "",
                                     choices = [],
                                     style = wx.CB_DROPDOWN
                                     | wx.TE_PROCESS_ENTER
                                     | wx.CB_READONLY
                                     #| wx.CB_SORT
                                     )
#                     self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbDem)
                    self.demSizer.Add(cbDem, flag = wx.EXPAND|wx.LEFT, border = 8)
                    for s in listDem:
                        cbDem.Append(ref.demarches[s][1])
                        
                self.cbDem = cbDem

                self.demSizer.Layout()
                
        #
        # Enseignement Spécifique      
        #
        if hasattr(self, 'titreSpe'):
            self.speSizer.Detach(self.titreSpe)
            self.titreSpe.Destroy()
            del self.titreSpe
        
        if hasattr(self, 'cbSpe'):
            for cb in self.cbSpe:
                self.speSizer.Detach(cb)
                cb.Destroy()
                del cb

        self.cbSpe = []
        if self.seance.aEnsSpe():
            if len(ref.listeEnsSpecif) > 0:
                
                self.titreSpe = wx.StaticText(self.pageGen, -1, "Enseignements Spécifiques :")
                self.speSizer.Add(self.titreSpe, flag = wx.ALIGN_LEFT|wx.LEFT|wx.BOTTOM, border = 2)
                
                for s in ref.listeEnsSpecif:
                    cb = wx.CheckBox(self.pageGen, -1, ref.ensSpecif[s][1],
                                     name = s)
                    cb.SetValue(True)
                    cb.SetToolTip(ref.ensSpecif[s][2])
                    cb.SetForegroundColour(ref.ensSpecif[s][3])
                    self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxSpe, cb)
                    self.speSizer.Add(cb, flag = wx.EXPAND|wx.LEFT, border = 8)
                    self.cbSpe.append(cb)
                self.speSizer.Layout()
#                 
#                 
#         self.bsizer2.Layout()
        self.pageGen.sizer.Layout()
        self.pageGen.SetupScrolling(scroll_x = False, scroll_y = True)

        doc = self.seance.GetDocument()
        
        #
        # Compétences
        #
        if self.seance.EstSeance_RS():
            pass # Là, il faudrait cacher les onglets ...
        else:
            if hasattr(self, 'arbreCmp'):
                for arbre in self.arbreCmp.values():
                    try:
                        self.cmpSizer.Detach(arbre)
                    except:
                        pass
                    arbre.Destroy()
                    del arbre
            
            if hasattr(self, 'infoCmp'):
                try:
                    self.cmpSizer.Detach(self.infoCmp)
                except:
                    pass
                self.infoCmp.Destroy()
                del self.infoCmp    
            
            if len(self.dicComp) == 0:
                self.infoCmp = wx.StaticText(self.pageCmp, -1, 
                                             "Aucune %s n'a été sélectionnée pour la Séquence" %doc.obj["C"].GetNomGenerique_sing())
                self.cmpSizer.Add(self.infoCmp, 1, flag = wx.EXPAND)
            
            self.arbreCmp = {}
            for cod, filtre in self.dicComp.items():
                f1 = []
                for f in filtre:
                    f1.append(f)
                    f1.extend(ref.getSousElem(f, "Comp_"+cod))
                    
#                 fcomp = self.seance.GetDocument().GetFiltre(ref.dicoCompetences[cod], "O", self.seance)
                fcomp = self.seance.GetCompetencesVisables(cod)
                
    #             print("filtres comp", cod, fcomp, f1)
                filtre = intersection(f1, fcomp)
                
                dic_f = ref.getToutesCompetencesDict()[cod].GetDicFiltre(filtre)
#                 print("ArbreCompetences", cod, dic_f, ref.dicoCompetences[cod])
                self.arbreCmp[cod] = ArbreCompetences(self.pageCmp, cod, dic_f, ref.getToutesCompetencesDict()[cod],
                                                      lstCases = doc.obj["C"].getCompetencesEtendues(), 
                                                      pp = self, agwStyle = HTL.TR_NO_HEADER)
                # parent, typ, dicCompetences, competences, pptache = None, filtre = None, agwStyle = 0
                self.cmpSizer.Add(self.arbreCmp[cod], 1, flag = wx.EXPAND)
    
            self.cmpSizer.Layout()
            self.pageCmp.sizer.Layout()

        
        
        
        #
        # Savoirs
        #
        if self.seance.EstSeance_RS():
            pass # Là, il faudrait cacher les onglets ...
        else:
            if hasattr(self, 'arbreSav'):
                for arbre in self.arbreSav.values():
                    try:
                        self.savSizer.Detach(arbre)
                    except:
                        pass
                    arbre.Destroy()
                    del arbre
            
            if hasattr(self, 'infoSav'):
                try:
                    self.savSizer.Detach(self.infoSav)
                except:
                    pass
                self.infoSav.Destroy()
                del self.infoSav    
            
            if len(self.dicSav) == 0:
                self.infoSav = wx.StaticText(self.pageSav, -1, 
                                             "Aucun %s n'a été sélectionné pour la Séquence" %doc.obj["S"].GetNomGenerique_sing())
                self.savSizer.Add(self.infoSav, 1, flag = wx.EXPAND)
                
            self.arbreSav = {}
            for cod, filtre in self.dicSav.items():
                f1 = []
                for f in filtre:
                    f1.append(f)
                    f1.extend(ref.getSousElem(f, "Sav_"+cod))
                    
                fcomp = self.seance.GetDocument().GetFiltre(ref.getTousSavoirsDict()[cod], "O", self.seance)
                filtre = intersection(fcomp, f1)
    #             print("filtres sav", cod, filtre)
                dic_f = ref.getTousSavoirsDict()[cod].GetDicFiltre(filtre)
                
                
                self.arbreSav[cod] = ArbreSavoirs(self.pageSav, cod, dic_f, ref.getTousSavoirsDict()[cod],
                                                  pp = self, filtre = filtre, agwStyle = HTL.TR_NO_HEADER)
                # parent, typ, savoirsRef, savoirs, prerequis, filtre = None, et = False, agwStyle = 0
                self.savSizer.Add(self.arbreSav[cod], 1, flag = wx.EXPAND)
    
            self.savSizer.Layout()
            self.pageSav.sizer.Layout()
        
        
        
#         self.pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboBox)
        
        
        




    ######################################################################################  
    def GetReferentiel(self):
        return self.seance.GetReferentiel()
    
    
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        self.selec.SetPathSeq(pathSeq)
        
        
    ######################################################################################  
    def OnPathModified(self, lien, marquerModifier = True):
        self.seance.OnPathModified()
#         self.btnlien.Show(self.seance.lien.path != "")
        self.selec.MiseAJour()
        if marquerModifier:
            self.seance.GetApp().MarquerFichierCourantModifie()
        self.Layout()
        self.Refresh()
        
    
    ############################################################################            
    def ConstruireListeSystemes(self):
        self.Freeze()
        ref = self.seance.GetReferentiel()
        if self.seance.typeSeance in ACTIVITES:
            for ss in self.systemeCtrl:
                self.bsizer.Detach(ss)
                ss.Destroy()
                
            self.systemeCtrl = []
            for s in self.seance.systemes:
#                print "   ", type(s), "---", s
                v = VariableCtrl(self.pageGen, s, signeEgal = False, 
                                 slider = False, fct = None, help = "", 
                                 sizeh = 30*SSCALE, scale = SSCALE)
                v.SetHelp("Indiquer le nombre de %s\n  \"%s\"\nnécessaires pour %s" %(ref.systemes[s.data.typ][1], s.data.nom, ref._nomActivites.le_()))
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
            
        self.box.SetMinSize((200*SSCALE,200*SSCALE))
        self.Layout()
        self.Thaw()
    
    
    #############################################################################            
    def MiseAJourListeSystemes(self):
        if self.seance.typeSeance in ACTIVITES:
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
        
    #############################################################################            
    def OnSelectColour(self, event):
#        print "OnSelectColour", event.GetValue()
        ref = self.GetReferentiel()
        self.seance.couleur = couleur.Wx2Couleur(event.GetValue())
        self.sendEvent(modif = "Mofification de la couleur %s" %ref._nomActivites.du_(), 
                       draw = False, verif = False)
        
        
    #############################################################################            
    def EvtVarSysteme(self, event):
        ref = self.GetReferentiel()
        self.sendEvent(modif = "Modification du nombre de %s nécessaires" %ref._nomSystemes.plur_(),
                       draw = True, verif = True)
        
        
    #############################################################################            
    def EvtCheckBox(self, event):
        ref = self.GetReferentiel()
        self.seance.intituleDansDeroul = event.IsChecked()
        self.sendEvent(modif = "Ajout/Suppression d'%s nécessaire" %ref._nomSystemes.un_(),
                       draw = True, verif = True)
    
    
    #############################################################################            
    def EvtTextIntitule(self, event):
#         print "EvtTextIntitule Seance"
        txt = self.textctrl.GetValue()
        ref = self.GetReferentiel()
        
        if self.seance.intitule != txt:
            self.seance.SetIntitule(txt)
            
    #         print "EvtTextIntitule", self.textctrl.GetValue()
            modif = "Modification de l'intitulé %s" %ref._nomActivites.du_()
            if self.onUndoRedo():
                self.sendEvent(modif = modif, draw = False, verif = False)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif, draw = False, verif = False)
                    self.eventAttente = True
        event.Skip()    
    
    #############################################################################            
    def EvtText(self, event):
        ref = self.GetReferentiel()
        t = ""
        if hasattr(self, 'vcDuree') and event.GetId() == self.vcDuree.GetId():
            self.seance.SetDuree(event.GetVar().v[0])
#             self.seance.GetFiche().Surbrillance(self.seance)
#             self.seance.GetFiche().MiseAJourSur(self.seance)
            t = "Modification de la durée %s" %ref._nomActivites.du_()
        
        elif hasattr(self, 'vcNombre') and event.GetId() == self.vcNombre.GetId():
            self.seance.SetNombre(event.GetVar().v[0])
            t = "Modification du nombre de groupes réalisant simultanément %s" %ref._nomActivites.le_("même")
            
        elif hasattr(self, 'vcTaille') and event.GetId() == self.vcTaille.GetId():
            self.seance.SetTaille(event.GetVar().v[0])
            t = "Modification de la taille des caractères"
        
        elif hasattr(self, 'vcNombreRot') and event.GetId() == self.vcNombreRot.GetId():
            self.seance.SetNombreRot(event.GetVar().v[0])
            t = "Modification du nombre de rotations successives"
            
        if self.onUndoRedo():
            self.sendEvent(modif = t)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = t, draw = True, verif = True)
                self.eventAttente = True

    #############################################################################            
    def EvtComboBox(self, event):
#         if hasattr(self, 'cbEff'):
#             print("EvtComboBox", event.GetEventObject(), self.cbEff)
        if event.GetEventObject() == self.cbType:
#             print("EvtComboBox type", self)
            ref = self.GetReferentiel()
            event.Skip()
            # On s'apprète à changer une séance Rotation ou Série en séance "Normale"
            if self.seance.typeSeance in ["R", "S"] \
              and ref.listeTypeSeance[event.GetSelection()] not in ["R", "S"]:
                dlg = wx.MessageDialog(self, "Cette %s contient des sous-%s !\n\n" \
                                             "Modifier le type de cette %s entrainera la suppression de toutes les sous %s !\n" \
                                             "Voulez-vous continuer ?" %(ref._nomActivites.sing_(), 
                                                                         ref._nomActivites.plur_(), 
                                                                         ref._nomActivites.sing_(),
                                                                         ref._nomActivites.plur_()),
                                        "Modification du type de %s" %ref._nomActivites.de_(),
                                        wx.YES_NO | wx.ICON_EXCLAMATION
                                        #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                        )
                res = dlg.ShowModal()
                dlg.Destroy() 
                if res == wx.ID_NO:
                    return
                else:
                    self.seance.SupprimerSousSeances()
            
            deja = self.seance.typeSeance in ACTIVITES
    #        print self.GetReferentiel().seances
    #         print(self.cbType.GetStringSelection())
    
            self.seance.SetType(get_key(ref.seances, 
                                        self.cbType.GetStringSelection(), 1))
            self.seance.GetDocument().OrdonnerSeances()
            if not self.seance.EstSeance_RS():
                self.AdapterAuType()
            if self.seance.typeSeance in ACTIVITES:
                if not deja:
                    for sy in self.seance.GetDocument().systemes:
                        self.seance.AjouterSysteme(sy, construire = False)
            else:
                self.seance.systemes = []
            if not self.seance.EstSeance_RS():   
                if self.cbEff.IsEnabled() and self.cbEff.IsShown() and self.cbEff.GetClientData() != "":
                    self.seance.SetEffectif(self.cbEff.GetClientData())
                else:
                    self.seance.SetEffectif("C")

    #         print(self.seance.typeSeance, ref.effectifsSeance)
    #         if self.seance.typeSeance in list(ref.effectifsSeance.keys())\
    #             and len(ref.effectifsSeance[self.seance.typeSeance]) > 0:
    #             print(">>>", ref.effectifsSeance[self.seance.typeSeance][0])
    #             self.seance.SetEffectif(ref.effectifsSeance[self.seance.typeSeance][0])
    
                
            
            self.ConstruireListeSystemes()
            self.Layout()
    #        print "ok"
            self.sendEvent(modif = "Modification du type %s (%s)" %(ref._nomActivites.de_(), self.seance.code), 
                           draw = True, verif = True)



        elif event.GetEventObject() == self.cbEff:
#             print("   effectif")
            self.cbEff.SetClientDataSelection(self.cbEff.GetClientData())
            self.seance.SetEffectif(self.cbEff.GetClientData())
           
    #         self.seance.SetEffectif(event.GetString())  
            self.sendEvent(modif = "Modification de l'effectif %s" %self.GetReferentiel()._nomActivites.du_(), 
                           draw = True, verif = True)


        elif event.GetEventObject() == self.cbDem:
#             print("EvtComboBoxDem")
            ref = self.seance.GetReferentiel()
            listDem = ref.demarcheSeance[self.seance.typeSeance]
            sel = self.cbDem.GetSelection()
            if sel != wx.NOT_FOUND and sel < len(listDem):
                self.seance.SetDemarche(listDem[sel])
                self.sendEvent(modif = "Modification de %s %s" %(ref._nomDemarches.le_(), ref._nomActivites.du_()), 
                               draw = True, verif = True) 


    #############################################################################            
    def EvtCheckBoxSpe(self, event):
#         print("EvtCheckBoxSpe")
        self.seance.SetEnsSpecif([cb.GetName() for cb in self.cbSpe if cb.IsChecked()])
#         event.Skip()
        self.AdapterAuType()
        self.MiseAJour()
        ref = self.seance.GetReferentiel()
        self.sendEvent(modif = "Modification %s %s" %(ref._nomEnsSpecif.du_(), ref._nomActivites.du_()), 
                       draw = True, verif = True)


#     #############################################################################            
#     def EvtComboBoxDem(self, event):
#         print("EvtComboBoxDem")
#         ref = self.seance.GetReferentiel()
#         cb = event.GetEventObject()
#         self.seance.SetDemarche(cb.GetName())  
#         self.sendEvent(modif = "Modification de %s %s" %(ref._nomDemarches.le_(), ref._nomActivites.du_()), 
#                        draw = True, verif = True) 
        
    
    #############################################################################            
    def EvtCheckBoxDem(self, event):
        ref = self.seance.GetReferentiel()
        self.seance.SetDemarche(" ".join([cb.GetName() for cb in self.cbDem if cb.IsChecked()]))
        self.sendEvent(modif = "Modification d'%s %s" %(ref._nomDemarches.un_(), ref._nomActivites.du_()), 
                       draw = True, verif = True) 
    
    
    ######################################################################################  
    def AjouterEnleverCompetences(self, app, rem, compRef):
        for s in app:
            if not s in self.seance.compVisees:
                self.seance.compVisees.append(s)
        for s in rem:
            if s in self.seance.compVisees:
                self.seance.compVisees.remove(s)
        ref = self.seance.GetReferentiel()
        self.sendEvent(modif = "Ajout/Suppression d'%s associée %s" %(compRef._nom.un_(), ref._nomActivites.au_()), 
                       draw = True, verif = True) 
        
        
#     #############################################################################            
#     def AjouterCompetence(self, code, propag = None):
#         self.seance.compVisees.append(code)
#         ref = self.seance.GetReferentiel()
#         self.sendEvent(modif = "Ajout d'une %s associée %s" %(getSingulier(ref.GetNomGeneriqueComp()), ref._nomActivites.au_())) 
#         
#         
#     #############################################################################            
#     def EnleverCompetence(self, code, propag = None):
#         self.seance.compVisees.remove(code)
#         ref = self.seance.GetReferentiel()
#         self.sendEvent(modif = "Suppression d'une %s associée %s" %(getSingulier(ref.GetNomGeneriqueComp()), ref._nomActivites.au_())) 
    
    
    ######################################################################################  
    def AjouterEnleverSavoirs(self, app, rem, savoirsRef):
        for s in app:
            if not s in self.seance.savVises:
                self.seance.savVises.append(s)
        for s in rem:
            if s in self.seance.savVises:
                self.seance.savVises.remove(s)
        ref = self.seance.GetReferentiel()
        self.sendEvent(modif = "Ajout/Suppression d'%s associée %s" %(savoirsRef._nom.un_(), ref._nomActivites.au_()), 
                       draw = True, verif = True) 
        
        
#     #############################################################################            
#     def AjouterSavoir(self, code, propag = None):
#         self.seance.savVises.append(code)
#         ref = self.seance.GetReferentiel()
#         self.sendEvent(modif = "Ajout d'une %s associée %s" %(getSingulier(ref.GetNomGeneriqueSav()), ref._nomActivites.au_())) 
#         
#         
#     #############################################################################            
#     def EnleverSavoir(self, code, propag = None):
#         self.seance.savVises.remove(code)
#         ref = self.seance.GetReferentiel()
#         self.sendEvent(modif = "Suppression d'une %s associée %s" %(getSingulier(ref.GetNomGeneriqueSav()), ref._nomActivites.au_())) 
        
        
    ######################################################################################  
    def SetCompetences(self):
        pass
    
    ######################################################################################  
    def SetIndicateurs(self):
        self.seance.indicateurs = {}
        if len(self.arbreCmp) > 0:
            for arbre in self.arbreCmp.values():
                self.seance.indicateurs.update(arbre.getDictIndicateurs())
                n = arbre.competencesRef._nomIndic.un_()
            ref = self.GetReferentiel()
            self.sendEvent(modif = "Modification d'%s de %s" %(n, ref._nomActivites.au_()), 
                           draw = False, verif = False) 
        
        
    ######################################################################################  
    def SetSavoirs(self):
        pass
        
    #############################################################################            
    def MarquerProblemeDuree(self, etat):
        return
#        self.vcDuree.marquerValid(etat)
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#         print("MiseAJour PP séance")
#         self.AdapterAuType()
        ref = self.GetReferentiel()
        if self.seance.typeSeance != "" and ref.seances[self.seance.typeSeance][1] in self.cbType.GetStrings():
            self.cbType.SetSelection(self.cbType.GetStrings().index(ref.seances[self.seance.typeSeance][1]))
#         self.textctrl.ChangeValue(self.seance.intitule)
        self.textctrl.SetValue(self.seance.intitule)
        if hasattr(self, 'vcDuree'):
            self.vcDuree.mofifierValeursSsEvt()
        
        self.coulCtrl.SetColour(couleur.Couleur2Wx(self.seance.couleur))
        
#         if self.cbEff.IsShown():#self.cbEff.IsEnabled() and 
        if hasattr(self, 'cbEff'):
#             self.cbEff.SetSelection(ref.findEffectif(self.cbEff.GetStrings(), self.seance.effectif))
            self.cbEff.SetClientDataSelection(self.seance.effectif)
        
#         if self.cbDem.IsShown():#self.cbDem.IsEnabled() and :
#            print ref.demarches[self.seance.demarche][1]
#            print self.cbDem.GetStrings()
#            print self.seance
#         print("   ", self.seance.demarche)
        if hasattr(self, 'cbDem'):
            if ref.multiDemarches:
                for cb in self.cbDem:
                    cb.SetValue(cb.GetName() in self.seance.demarche.split())
            else:
                self.cbDem.SetSelection(self.cbDem.GetStrings().index(ref.demarches[self.seance.demarche][1]))
        
        if hasattr(self, 'cbSpe'):
            for cb in self.cbSpe:
                cb.SetValue(cb.GetName() in self.seance.ensSpecif)
            
        if self.seance.typeSeance in ACTIVITES:
            if hasattr(self, 'vcNombre'):
                self.vcNombre.mofifierValeursSsEvt()
        elif self.seance.typeSeance == "R":
            if hasattr(self, 'vcNombreRot'):
                self.vcNombreRot.mofifierValeursSsEvt()
        
        # Arbres de compétences
        if hasattr(self, 'arbreCmp'):
            for typ, arbre in self.arbreCmp.items():
                arbre.UnselectAll()
                for cmp in self.seance.compVisees:
                    if typ == cmp[0]:
                        if cmp[1:] in arbre.items.keys():
                            i = arbre.items[cmp[1:]]
                            arbre.CheckItem2(i)
                            arbre.AutoCheckChild(i, True)
                
                arbre.gererAffichageTxtCtrl()
                arbre.MiseAJour(typ, self.seance)
                            
                            
        # Arbres de savoirs
        if hasattr(self, 'arbreSav'):
            for typ, arbre in self.arbreSav.items():
                arbre.UnselectAll()
                for cmp in self.seance.savVises:
                    if typ == cmp[0]:
                        if cmp[1:] in arbre.items.keys():
                            i = arbre.items[cmp[1:]]
                            arbre.CheckItem2(i)
                            arbre.AutoCheckChild(i, True)
            
        self.vcTaille.mofifierValeursSsEvt()
        
        self.cbInt.SetValue(self.seance.intituleDansDeroul)
        if sendEvt:
            self.sendEvent(draw = True, verif = True)
        
        self.MiseAJourLien()
        
        self.ConstruireListeSystemes()
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(toSystemEncoding(self.seance.lien.path), self.seance.lien.type)
#         self.btnlien.Show(self.seance.lien.path != "")
        self.sizer.Layout()
        

    
####################################################################################
#
#   Classe définissant le panel de propriété d'une fonction de service
#
####################################################################################
class PanelPropriete_FS(PanelPropriete):
    def __init__(self, parent, FS):
        
        self.FS = FS
        self.parent = parent
        
        PanelPropriete.__init__(self, parent, objet = self.FS)
        
        #
        # Intitulé
        #
        box = myStaticBox(self, -1, "Intitulé")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        textctrl = TextCtrl_Help(self, "", scale = SSCALE)
        textctrl.SetTitre("Intitulé")
        textctrl.SetToolTip("Intitulé")
        self.textctrl = textctrl
        bsizer.Add(textctrl, 1, flag = wx.EXPAND)
        self.sizer.Add(bsizer, (0,0), flag = wx.EXPAND|wx.ALL, border = 2)
#         self.Bind(stc.EVT_STC_CHANGE, self.EvtText, textctrl)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, textctrl)
    
        #
        # Principale ou contrainte
        #
        ref = FS.GetReferentiel()
        self.rdtype = wx.RadioBox(self, -1, label="Type %s" %ref.getLabel("EXIG").de_(), 
                                  choices=["Principale", "Contrainte"],
                                  style = wx.RA_SPECIFY_COLS)
        
        
        self.sizer.Add(self.rdtype, (1,0), flag = wx.EXPAND|wx.ALL, border = 2)
        self.sizer.AddGrowableRow(0)
        
        self.Bind(wx.EVT_RADIOBOX, self.OnChangeType, self.rdtype)
    
        self.MiseAJour()
        
        
    
    ############################################################################            
    def GetDocument(self):
        return self.FS.GetDocument()
    
    #############################################################################            
    def OnChangeType(self, event): 
        self.FS.SetType(event.GetSelection())
        
    #############################################################################            
    def EvtText(self, event):
#         print "EvtText", self.FS.intitule
        txt = self.textctrl.GetText()
        ref = self.FS.GetReferentiel()
        
        if self.FS.intitule != txt:
            event.Skip()
            self.FS.SetIntitule(txt)
            
            modif = "Modification de l'intitulé %s" %ref.getLabel("EXIG").du_()
            
            if self.onUndoRedo():
                self.sendEvent(modif = modif, draw = True, verif = False)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif, draw = True, verif = False)
                    self.eventAttente = True
                    
    #############################################################################            
    def MiseAJour(self, sendEvt = False, marquerModifier = True):
#        print "MiseAJour panelPropriete Support"
        self.textctrl.ChangeValue(self.FS.intitule)
        self.rdtype.SetSelection(self.FS.type)
        
        if sendEvt:
            self.sendEvent(draw = True, verif = True)

        
        
        
####################################################################################
#
#   Classe définissant le panel de propriété de la tache
#
####################################################################################
class PanelPropriete_Tache(PanelPropriete):
    def __init__(self, parent, tache, revue = 0):
        self.tache = tache
        self.revue = revue
        ref = tache.GetReferentiel()
        PanelPropriete.__init__(self, parent, objet = self.tache)
#        print "init pptache", tache, ref
        if not tache.phase in [tache.projet.getCodeLastRevue(), _S]  \
           and not (tache.phase in TOUTES_REVUES_EVAL and (True in list(ref.compImposees.values()))): #tache.GetReferentiel().compImposees['C']):
            #
            # La page "Généralités"
            #
            self.nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
            pageGen = PanelPropriete(self.nb, objet = self.tache)
            bg_color = self.Parent.GetBackgroundColour()
            pageGen.SetBackgroundColour(bg_color)
            self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
            self.nb.AddPage(pageGen, "Propriétés générales")
            self.sizer.Add(self.nb, (0,0), flag = wx.EXPAND)
            self.sizer.AddGrowableCol(0)
            self.sizer.AddGrowableRow(0)
        
        else:
            #
            # Pas de book pour la revue 2 et la soutenance
            #
            pageGen = self
            
        self.pageGen = pageGen
            
        
        #
        # Phase
        #
        # Mise en place
        c0 = wx.BoxSizer(wx.VERTICAL)
        pageGen.sizer.Add(c0, (0,0), flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 2)
        c00 = wx.BoxSizer(wx.HORIZONTAL)
        
        prj = self.tache.GetProjetRef()
        if prj is not None:
#        lstPhases = [p[1] for k, p in ref.phases_prj.items() if not k in ref.listPhasesEval_prj]
            lstPhases = [prj.phases[k][1] for k in prj.listPhases if not k in prj.listPhasesEval]
            
            titre = wx.StaticText(pageGen, -1, "Phase : ")
            c00.Add(titre, flag = wx.ALIGN_CENTER_VERTICAL)
    #         pageGen.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 5)
            
            if tache.phase in TOUTES_REVUES_SOUT:
                txtPhas = wx.StaticText(pageGen, -1, prj.phases[tache.phase][1])
                c00.Add(txtPhas, flag = wx.ALIGN_CENTER_VERTICAL)
    #             pageGen.sizer.Add(txtPhas, (0,1), (1,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, border = 5)
                
            elif tache.estPredeterminee():
                txtPhas = wx.StaticText(pageGen, -1, "")
    #             pageGen.sizer.Add(txtPhas, (0,1), (1,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, border = 5)
                self.txtPhas = txtPhas
                c00.Add(txtPhas, flag = wx.ALIGN_CENTER_VERTICAL)
                
            else:
                cbPhas = combo_adv.BitmapComboBox(pageGen, -1, "Sélectionner la phase",
                                     choices = lstPhases, #size = (-1, 24*SSCALE),
                                     style = wx.CB_READONLY
                                            |wx.CB_DROPDOWN
    #                                  | wx.TE_PROCESS_ENTER
    #                                 | 
                                     #| wx.CB_SORT
                                     )
                
                for i, k in enumerate(sorted([k for k in list(prj.phases.keys()) if not k in prj.listPhasesEval])):#ref.listPhases_prj):
                    cbPhas.SetItemBitmap(i, scaleImage(constantes.imagesTaches[k].GetBitmap(), 24*SSCALE, 24*SSCALE))
                pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbPhas)
                self.cbPhas = cbPhas
                c00.Add(cbPhas, flag = wx.ALIGN_CENTER_VERTICAL)
                
    #             pageGen.sizer.Add(cbPhas, (0,1), flag = wx.EXPAND|wx.ALL, border = 2)
            c0.Add(c00, flag = wx.EXPAND)    

        
        #
        # Intitulé de la tache
        #
        if not tache.phase in TOUTES_REVUES_EVAL_SOUT:
            box = myStaticBox(pageGen, -1, "Intitulé de la tâche")
            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            self.boxInt = box
            if not tache.estPredeterminee():
                textctrl = orthographe.STC_ortho(pageGen, -1)#, u"", style=wx.TE_MULTILINE)
                
                textctrl.SetTitre("Intitulé de la tâche", tache.getIcone())
                textctrl.SetToolTip("Donner l'intitulé de la tâche\n"\
                                          " = un simple résumé !\n\n" \
                                          "les détails doivent figurer dans la zone\n" \
                                          "\"Description détaillée de la tâche\"")
                bsizer.Add(textctrl,1, flag = wx.EXPAND)
                self.textctrl = textctrl
                self.textctrl.Bind(wx.EVT_LEAVE_WINDOW, self.EvtTextIntitule)
#                 self.textctrl.Bind(wx.EVT_KILL_FOCUS, self.EvtTextIntitule)
                
                
            else:
                cc = TreeCtrlComboBook(pageGen, self.tache, self.EvtComboBoxTache)
                bsizer.Add(cc, 1, flag = wx.EXPAND)
                self.cbTache = cc

            c0.Add(bsizer, 1, flag = wx.EXPAND)
#             pageGen.sizer.Add(bsizer, (1,0), (1,2), 
#                                flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT, border = 2)    


        #
        # Durée de la tache
        #
        if not tache.phase in TOUTES_REVUES_EVAL_SOUT:
            vcDuree = VariableCtrl(pageGen, tache.duree, coef = 0.5, signeEgal = True, slider = False,
                                   help = "Volume horaire de la tâche, en heures")#, sizeh = 60)
            pageGen.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
            self.vcDuree = vcDuree
            c0.Add(vcDuree, flag = wx.EXPAND)
#             pageGen.sizer.Add(vcDuree, (2,0), (1, 2), flag = wx.EXPAND|wx.ALL, border = 2)


        #
        # Icones
        #
        if not tache.phase in TOUTES_REVUES_EVAL_SOUT:
            isizer = self.CreateIconeSelect(pageGen)
            c1 = wx.BoxSizer(wx.VERTICAL)
            c1.Add(isizer, 1, flag = wx.EXPAND)
            pageGen.sizer.Add(c1, (0,1), flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 2)
#             pageGen.sizer.Add(isizer, (0,2), (3, 1), 
#                               flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 4)
#             pageGen.sizer.AddGrowableCol(2)


        #
        # Elèves impliqués
        #
        if not tache.phase in TOUTES_REVUES_EVAL_SOUT:
            self.box = myStaticBox(pageGen, -1, "%s impliqués" %ref.getLabel("ELEVES").Plur_())
#            self.box.SetMinSize((150,-1))
#             self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
            ebsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
            sp = scrolled.ScrolledPanel(pageGen, -1)
            ebsizer.Add(sp, 1, flag = wx.EXPAND)
            
            self.elevesCtrl = []
            self.ConstruireListeEleves(sp)
            
            c2 = wx.BoxSizer(wx.VERTICAL)
            c2.Add(ebsizer, 1, flag = wx.EXPAND)
            pageGen.sizer.Add(c2, (0,2), flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 2)
#             pageGen.sizer.Add(self.bsizer, (0,3), (3, 1), flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 4)
#             pageGen.sizer.AddGrowableCol(3)
        
        
        
        #
        # Description de la tâche
        #
        dbox = myStaticBox(pageGen, -1, "Description détaillée de la tâche")
        dbsizer = wx.StaticBoxSizer(dbox, wx.HORIZONTAL)
#        bd = wx.Button(pageGen, -1, u"Editer")
        tc = richtext.RichTextPanel(pageGen, self.tache, toolBar = True)
        tc.SetToolTip("Donner une description détaillée de la tâche :\n" \
                            " - les conditions nécessaires\n" \
                            " - ce qui est fourni\n" \
                            " - les résultats attendus\n" \
                            " - les différentes étapes\n" \
                            " - la répartition du travail entre %s\n"\
                            " - ..." %ref.getLabel("ELEVES").les_())
        tc.SetTitre("Description détaillée de la tâche")
     
        dbsizer.Add(tc, flag = wx.EXPAND)

        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
#         c3 = wx.BoxSizer(wx.VERTICAL)
#         c3.Add(dbsizer, 1, flag = wx.EXPAND)
        pageGen.sizer.Add(dbsizer, (0,3), flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 2)
        
#         pageGen.sizer.AddGrowableRow(1)
        
        pageGen.sizer.AddGrowableRow(0)
        pageGen.sizer.AddGrowableCol(3)
        
        self.ConstruireCompetences()
        if prj is not None and not prj._pasdIndic:
            self.ConstruireCasesEleve()
        self.MiseAJour()

        
        #
        # Mise en place
        #
        self.Refresh()
    
     
    ####################################################################################
    def OnPageChanged(self, event):
#        sel = self.nb.GetSelection()
#        self.MiseAJourPoids()
        event.Skip()
        
    ####################################################################################
    def MiseAJourPoids(self):
        for c in self.tache.indicateursEleve[0]:
            self.MiseAJourIndicateurs(c)
            
#    ####################################################################################
#    def OnSelChanged(self, event):
#        item = event.GetItem() 
#        self.competence = self.arbre.GetItemText(item).split()[0]
#        self.MiseAJourIndicateurs(self.competence)
        
    #############################################################################            
    def MiseAJourIndicateurs(self, competence):
#        print "MiseAJourIndicateurs", competence
        self.Freeze()
        if False:#self.tache.GetTypeEnseignement() != "SSI":
            indicateurs = REFERENTIELS[self.tache.GetTypeEnseignement()].dicIndicateurs
            lab = "Indicateurs"
            
            # On supprime l'ancienne CheckListBox
            if self.liste != None:
                self.ibsizer.Detach(self.liste)
                self.liste.Destroy()
            
            if competence in list(indicateurs.keys()):
                self.liste = wx.CheckListBox(self.pageCom, -1, choices = indicateurs[competence], style = wx.BORDER_NONE)
    
                lst = self.tache.indicateursEleve[0][competence]
                for i, c in enumerate(lst):
                    self.liste.Check(i, c)
                
                self.ibox.SetLabel(lab+" "+competence)
                self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.liste)
                
            else:
                self.liste = wx.StaticText(self.pageCom, -1, "Selectionner une compétence pour afficher les indicateurs associés.")
                self.ibox.SetLabel(lab)
                
            self.ibsizer.Add(self.liste,1 , flag = wx.EXPAND)
                
            self.arbre.Layout()
            self.ibsizer.Layout()
            self.pageComsizer.Layout()
        
        else:
            if competence in list(self.tache.indicateursEleve[0].keys()):
                for arbre in list(self.arbres.values()):
                    arbre.MiseAJour(competence, self.tache.indicateursEleve[0][competence])
            else:
                prj = self.tache.GetProjetRef()
                if prj is not None:
                    for arbre in list(self.arbres.values()):
                        arbre.MiseAJour(competence, prj._dicCompetences_simple[competence][1])
#                self.arbre.MiseAJour(competence, REFERENTIELS[self.tache.GetTypeEnseignement()]._dicCompetences_prj_simple[competence][1])
            
            
        self.Thaw()
        
        
#    ######################################################################################  
#    def EvtCheckListBox(self, event):
#        index = event.GetSelection()
#        
#        if self.competence in self.tache.indicateursEleve[0].keys():
#            lst = self.tache.indicateursEleve[0][self.competence]
#        else:
#            prj = self.tache.GetProjetRef()
#            lst = [self.competence in self.tache.competences]*len(prj.dicIndicateurs[self.competence])
##            lst = [self.competence in self.tache.competences]*len(REFERENTIELS[self.tache.GetTypeEnseignement()].dicIndicateurs_prj[self.competence])
#            
#        lst[index] = self.liste.IsChecked(index)
#        
#        if True in lst and not self.competence in self.tache.competences:
#            self.tache.competences.append(self.competence)
#            self.arbre.CheckItem2(self.arbre.FindItem(self.arbre.GetRootItem(), self.competence), True)
#            self.arbre.SelectItem(self.arbre.FindItem(self.arbre.GetRootItem(), self.competence))
#        if not True in lst and self.competence in self.tache.competences:
#            self.tache.competences.remove(self.competence)
##            self.MiseAJour(sendEvt = False)
#            self.arbre.CheckItem2(self.arbre.FindItem(self.arbre.GetRootItem(), self.competence), False)
#            self.arbre.SelectItem(self.arbre.FindItem(self.arbre.GetRootItem(), self.competence))
#            
#        self.Refresh()    
#        self.sendEvent(modif = u"Modification du type de séance")
#        
#        self.liste.Check()
#        self.tache.indicateurs[]
#        label = self.liste.GetString(index)
#        status = 'un'
#        if self.liste.IsChecked(index):
#            status = ''
#        
#        self.lb.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
        

    ######################################################################################  
    def AjouterEnleverCompetences(self, app, rem, compRef):
        for s in app:
            if not s in self.tache.compVisees:
                self.tache.compVisees.append(s)
        for s in rem:
            if s in self.tache.compVisees:
                self.tache.compVisees.remove(s)
        
        self.sendEvent(modif = "Ajout/Suppression d'%s visée par à la Tâche" %compRef._nom.un_(), 
                       draw = True, verif = True) 
        
   
    ######################################################################################  
    def AjouterCompetence(self, code, propag = True):
        self.tache.AjouterCompetence(code, propag)
# #        print "AjouterCompetence !!", self, code
#         if not code in self.tache.indicateursEleve[0] and not self.tache.estPredeterminee():
#             self.tache.indicateursEleve[0].append(code)
# 
#         if propag:
#             for i in range(len(self.tache.projet.eleves)):
#                 if not self.tache.estPredeterminee() or i in self.tache.eleves:
#                     self.AjouterCompetenceEleve(code, i+1)
#        
# #        if not self.tache.estPredeterminee():
#         self.tache.projet.SetCompetencesRevuesSoutenance()
#         
        
    ######################################################################################  
    def EnleverCompetence(self, code, propag = True):
        self.tache.EnleverCompetence(code, propag)
# #        print "EnleverCompetence", self, code
#         if code in self.tache.indicateursEleve[0]:
#             self.tache.indicateursEleve[0].remove(code)
#         # on recommence : pour corriger un bug
#         if code in self.tache.indicateursEleve[0]:
#             self.tache.indicateursEleve[0].remove(code)
#         
#         if propag:
#             for i in range(len(self.tache.projet.eleves)):
#                 self.EnleverCompetenceEleve(code, i+1)
#     
#         self.tache.projet.SetCompetencesRevuesSoutenance()
    
    
    ######################################################################################  
    def AjouterCompetenceEleve(self, code, eleve):
        self.tache.AjouterCompetenceEleve(code, eleve)
# #        print "AjouterCompetenceEleve", code, self.tache.phase
#         if hasattr(self.tache, 'indicateursEleve'):
#             
#             if self.tache.estPredeterminee():
#                 self.tache.indicateursEleve[eleve].append(code)
#                 
#             else:
#                 dicIndic = self.tache.projet.eleves[eleve-1].GetDicIndicateursRevue(self.tache.phase)
#                 comp = code.split("_")[0]
#                 if comp in dicIndic.keys():
#                     if comp != code: # Indicateur seul
#                         indic = eval(code.split("_")[1])
#                         ok = dicIndic[comp][indic-1]
#                 else:
#                     ok = False
#                     
#                 if ok and not code in self.tache.indicateursEleve[eleve]:
#                     self.tache.indicateursEleve[eleve].append(code)
#             
# #            print "  ", self.tache.indicateursEleve
# #                self.tache.ActualiserDicIndicateurs()
            
        
    ######################################################################################  
    def EnleverCompetenceEleve(self, code, eleve):
        self.tache.EnleverCompetenceEleve(code, eleve)
# #        print "EnleverCompetenceEleve", self, code
#         
#         if hasattr(self.tache, 'indicateursEleve'):
# #            print "  ", self.tache.indicateursEleve
#             if code in self.tache.indicateursEleve[eleve]:
#                 self.tache.indicateursEleve[eleve].remove(code)
#             # on recommence : pour corriger un bug
#             if code in self.tache.indicateursEleve[eleve]:
#                 self.tache.indicateursEleve[eleve].remove(code)
# #            self.tache.ActualiserDicIndicateurs()
# #            print "  ", self.tache.indicateursEleve


    ############################################################################            
    def SetCompetences(self):
#         print("SetCompetences")
        
        self.GetDocument().MiseAJourDureeEleves()
        
        modif = "Ajout/Suppression d'une compétence à la Tâche"
        if self.onUndoRedo():
            self.sendEvent(modif = modif, draw = True, verif = True)
        else:
            wx.CallAfter(self.sendEvent, modif = modif, draw = True, verif = True)
        self.tache.projet.Verrouiller()


    ############################################################################            
    def ConstruireCompetences(self):
        """
        """
        ref = self.tache.GetReferentiel()
        prj = self.tache.GetProjetRef()
        
        
        if hasattr(self, "nb"):
            while True:
                try:
                    self.nb.DeletePage(1)
                except:
                    break
            
        if not self.tache.phase in [self.tache.projet.getCodeLastRevue(), _S] \
           and not (self.tache.phase in TOUTES_REVUES_EVAL and (True in list(ref.compImposees.values()))) \
           and prj is not None: #tache.GetReferentiel().compImposees['C']):
            
#            print "ConstruireCompetences", self.tache, ref, prj

            #
            # Les pages "Compétences"
            #
            self.arbres = {}
            self.pagesComp = []
#             print(prj._dicoCompetences)
            for code, dicComp in prj._dicoCompetences.items():
                self.pagesComp.append(wx.Panel(self.nb, -1))
                compRef = ref.getToutesCompetencesDict()[code]
                pageComsizer = wx.BoxSizer(wx.HORIZONTAL)
                
#                 print("dicComp", dicComp)
                if prj._pasdIndic:
                    dic_f = ref.getToutesCompetencesDict()[code].GetDicFiltre()
                    self.arbres[code] = ArbreCompetences(self.pagesComp[-1], code, dic_f, ref.getToutesCompetencesDict()[code], 
                                                         pp = self, agwStyle = HTL.TR_NO_HEADER)
                else:
                    self.arbres[code] = ArbreCompetencesPrj(self.pagesComp[-1], code, 
                                                            dicComp, compRef, self,
                                                            revue = self.tache.phase in TOUTES_REVUES_SOUT, 
                                                            eleves = (self.tache.phase in TOUTES_REVUES_EVAL_SOUT \
                                                               or self.tache.estPredeterminee()))
                
                pageComsizer.Add(self.arbres[code], 1, flag = wx.EXPAND)
                self.pagesComp[-1].SetSizer(pageComsizer)
                self.nb.AddPage(self.pagesComp[-1], "%s à mobiliser : %s" %(compRef._nom.Plur_(),compRef.abrDiscipline))
                
                self.pageComsizer = pageComsizer
            
            


    ############################################################################            
    def ConstruireListeEleves(self, panel):
        """ Ajout des cases "élève" :
             - sur la page "Proprietes générales"
             - sur les pages "Compétences" : cas des revues (sauf dernière(s)) et des compétences prédéterminées
        """
#         print "ConstruireListeEleves", self.tache

        # Sur la page "Proprietes générales"
        if hasattr(self, 'elevesCtrl'):
            
            panel.Freeze()
            bsizer = wx.BoxSizer(wx.VERTICAL)
            panel.SetSizer(bsizer)
            panel.SetupScrolling()
            
            for ss in self.elevesCtrl:
                self.bsizer.Detach(ss)
                ss.Destroy()
                
            self.elevesCtrl = []
            self.impElevesCtrl = []

            for i, e in enumerate(self.GetDocument().eleves + self.GetDocument().groupes):
                v = wx.CheckBox(panel, 100+i, e.GetNomPrenom())
#                 v.SetMinSize((200,-1))
                v.SetValue(i in self.tache.eleves)
                panel.Bind(wx.EVT_CHECKBOX, self.EvtCheckEleve, v)
                bsizer.Add(v, flag = wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, border = 3)#|wx.EXPAND) 
                self.elevesCtrl.append(v)
                
                p = wx.SpinCtrl(panel, 200+i, "%", (50*SSCALE, 18*SSCALE))
                p.SetMaxSize((50*SSCALE, 18*SSCALE))
                p.SetToolTip("Taux d'implication de l'élève dans la tâche")
                p.SetRange(1,100)
                if i in self.tache.eleves:
                    p.SetValue(self.tache.impEleves[self.tache.eleves.index(i)])
                    p.Enable(True)
                else:
                    p.SetValue(100)
                    p.Enable(False)
                panel.Bind(wx.EVT_SPINCTRL, self.OnSpin, p)
                panel.Bind(wx.EVT_TEXT, self.OnSpin, p)
                bsizer.Add(p, flag = wx.ALIGN_RIGHT|wx.BOTTOM|wx.LEFT|wx.RIGHT, border = 3)#|wx.EXPAND) 
                self.impElevesCtrl.append(p)
                 
            
            line = wx.StaticLine(panel)
            bsizer.Add(line, 0, flag = wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, border = 3)#)  size = (100,3))
            
            self.tousElevesCtrl = wx.CheckBox(panel, -1, "tous")
            self.tousElevesCtrl.SetValue(all([b.IsChecked() for b in self.elevesCtrl]))
            bsizer.Add(self.tousElevesCtrl, flag = wx.ALIGN_LEFT|wx.ALL, border = 3)#|wx.EXPAND) 
            panel.Bind(wx.EVT_CHECKBOX, self.EvtCheckEleve, self.tousElevesCtrl)
            
            bsizer.Layout()
            
            if len(self.GetDocument().eleves + self.GetDocument().groupes) > 0:
                self.box.Show(True)
            else:
                self.box.Hide()
    
#            self.box.SetMinSize((200,200))
            bsizer.Layout()
            panel.Thaw()
#             print [cb.GetSize()[0] for cb in self.elevesCtrl]
#             line.SetSize((max([cb.GetSize()[0] for cb in self.elevesCtrl]), 3))
        
        
        # sur les pages "Compétences"
        prj = self.tache.GetProjetRef()
        if prj is not None and not prj._pasdIndic:
            self.ConstruireCasesEleve()
        
        
    #############################################################################            
    def OnSpin(self, event):
#         print event.GetId()
        i = event.GetId()-200
        if i in self.tache.eleves:
            e = self.tache.eleves.index(i)
            self.tache.impEleves[e] = self.impElevesCtrl[i].GetValue()
#         print "    ", lst
        
            self.GetDocument().MiseAJourDureeEleves()
    
            self.sendEvent(modif = "Modification du taux d'implication de l'%s dans la tâche" %self.GetDocument().GetReferentiel().getLabel("ELEVES").le_(), 
                           draw = True, verif = False) 
            

#     #############################################################################            
#     def OnText(self, event):
#         print event.GetEventObject()
#         print event.GetId()
#         self.log.write('OnText: %d\n' % self.sc.GetValue())
        
        
    #############################################################################            
    def ConstruireCasesEleve(self):
        # On reconstruit l'arbre pour ajouter/enlever des cases "élève"
        if hasattr(self, 'arbres'):
            for arbre in self.arbres.values():
                if arbre.eleves:
                    arbre.ConstruireCasesEleve()
        
        
    #############################################################################            
#    def MiseAJourListeEleves(self):
#        """ Met à jour la liste des élèves
#        """
#        if not self.tache.phase in TOUTES_REVUES_EVAL_SOUT:
#            self.pageGen.Freeze()
#            for i, e in enumerate(self.GetDocument().eleves):
#                self.elevesCtrl[i].SetLabel(e.GetNomPrenom())
#            self.bsizer.Layout()
#            self.pageGen.Layout()
#            self.pageGen.Thaw()



#    #############################################################################            
#    def MiseAJourEleves(self):
#        """ Met à jour le cochage des élèves concernés par la tâche
#        """
#        if not self.tache.phase in TOUTES_REVUES_EVAL_SOUT:
#            for i in range(len(self.GetDocument().eleves)):
#                self.elevesCtrl[i].SetValue(i in self.tache.eleves)

                
                
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
        
        
#    #############################################################################            
#    def EvtVarSysteme(self, event):
#        self.sendEvent(modif = u"Modification ")
#        
        
    


    #############################################################################            
    def EvtCheckEleve(self, event):
#         print "EvtCheckEleve"
        if event.GetEventObject() == self.tousElevesCtrl:
            for b in self.elevesCtrl:       # On coche tout
                b.SetValue(self.tousElevesCtrl.IsChecked())
        else:
            self.tousElevesCtrl.SetValue(all([b.IsChecked() for b in self.elevesCtrl]))
        
        lst = []
        lsti = []
        for i in range(len(self.GetDocument().eleves) + len(self.GetDocument().groupes)):
            if self.elevesCtrl[i].IsChecked():
                lst.append(i)
                self.impElevesCtrl[i].Enable(True)
                lsti.append(self.impElevesCtrl[i].GetValue())
            else:
                self.impElevesCtrl[i].Enable(False)
        
        self.tache.eleves = lst
        self.tache.impEleves = lsti
#         print "    ", lst
        
        self.GetDocument().MiseAJourDureeEleves()
#        self.GetDocument().MiseAJourTachesEleves()
        prj = self.tache.GetProjetRef()
        if prj is not None and not prj._pasdIndic:
            self.ConstruireCasesEleve()
        
        self.sendEvent(modif = "Changement d'%s concerné par la tâche" %self.GetDocument().GetReferentiel().getLabel("ELEVES").le_(), 
                       draw = True, verif = True)    


    #############################################################################            
    def EvtTextIntitule(self, event):
#         print "EvtTextIntitule Tache"
        txt = self.textctrl.GetValue()
        
        if self.tache.intitule != txt:
            self.tache.SetIntitule(txt)
            modif = "Modification de l'intitulé de la Tâche"
            if self.onUndoRedo():
                self.sendEvent(modif = modif, draw = True, verif = False)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif, draw = True, verif = False)
                    self.eventAttente = True
        
        event.Skip()
        
        
#    #############################################################################            
#    def    testCloseUp(self, evt):
#        print "testCloseUp"
#        self.ccTache.SetTextCtrlStyle(wx.TE_READONLY|wx.TE_WORDWRAP|wx.TE_MULTILINE)
#        evt.Skip()
        
    #############################################################################            
    def EvtComboBoxTache(self, texte):
        """ Modification de l'intitulé de la tâche
        """
        prj = self.tache.GetProjetRef()
        if prj is None:
            return
        
#        ct = event.GetString().split()[0]
        ct = texte
        if len(ct) == 0 or ct.split()[0] not in prj.listTaches:
#            event.Skip()
            return
#        print "EvtComboBoxTache", ct.split()[0]
        ct = ct.split()[0]
        self.tache.SetIntitule(ct)
        
        ph = prj.taches[ct][0]
        self.txtPhas.SetLabel(prj.phases[ph][1])
        self.tache.SetPhase(ph)
        
        #
        # Reconstruire l'arbre des compétences (uniquement celles associées à la tâche)
        #
        for arbre in list(self.arbres.values()):
            arbre.ReConstruire()
        
        #
        # Marquer UNDO
        #
        modif = "Modification de l'intitulé de la Tâche"
        if self.onUndoRedo():
            self.sendEvent(modif = modif, draw = True, verif = False)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = modif, draw = True, verif = False)
                self.eventAttente = True
                
#        self.ccTache.SetTextCtrlStyle(wx.TE_READONLY|wx.TE_WORDWRAP|wx.TE_MULTILINE)
#        event.Skip()
                    
    #############################################################################            
    def EvtText(self, event):
        """ Modification de la durée de la Tâche
        """
        t = ""
        if event.GetId() == self.vcDuree.GetId():
            self.tache.SetDuree(event.GetVar().v[0])
            t = "Modification de la durée de la Tâche"
#        elif event.GetId() == self.vcNombre.GetId():
#            self.tache.SetNombre(event.GetVar().v[0])
#            t = u"Modification de la durée de la Tâche"
    
        if self.onUndoRedo():
            self.sendEvent(modif = t, draw = True, verif = True)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = t, draw = True, verif = True)
                self.eventAttente = True
                
    
        
    #############################################################################            
    def EvtComboBox(self, event):
        """ Changement de phase
        """
#        print "EvtComboBox phase", self.tache, self.tache.phase
        prj = self.tache.GetProjetRef()
        if prj is None:
            return
        
        newPhase = prj.getClefDic('phases', self.cbPhas.GetStringSelection(), 1)
#        print "   ", newPhase
#        newPhase = get_key(self.GetReferentiel().NOM_PHASE_TACHE[self.tache.GetTypeEnseignement(True)], 
#                                        self.cbPhas.GetStringSelection())
        if self.tache.phase != newPhase:
            if newPhase == "Rev":
                self.tache.SetDuree(0)
            self.tache.SetPhase(newPhase)
            for arbre in self.arbres.values():
                arbre.MiseAJourPhase(newPhase)
            self.pageGen.Layout()
            self.sendEvent(modif = "Changement de phase de la Tâche", draw = True, verif = True)
        
    
#    #############################################################################            
#    def MiseAJourDuree(self):
#        """ Mise à jour du champ de texte de la durée
#            (conformément à la valeur de la variable associée)
#        """
#        if hasattr(self, 'vcDuree'):
#            self.vcDuree.mofifierValeursSsEvt()

    
#    #############################################################################            
#    def MiseAJourCases(self):
#        """ Mise à jour des cases "élèves" de l'arbre des compétences
#            > on cécoche tout et on recoche
#        """
#        print "MiseAJourCases", self.tache.phase, self.tache.intitule
#        print "  ", self.tache.indicateursEleve
#        if hasattr(self, 'arbre'):
#            self.arbre.UnselectAll()
#            
#            for codeIndic in self.tache.indicateursEleve[0]:
#                cases = self.arbre.GetCasesEleves(codeIndic)
#                if cases:
#                    cases.MiseAJour()
#                    cases.Actualiser()
                  
            
    #############################################################################            
    def MiseAJour(self, sendEvt = False, marquerModifier = True):
#         print("MiseAJour panelPropriete Tache", self.tache.compVisees)
#        print "MiseAJour", self.tache.phase, self.tache.intitule
        
        #
        # On coche les indicateurs de compétence
        #
        if hasattr(self, 'arbres'):
            for codeIndic in self.tache.indicateursEleve[0]:
                disc, code = codeIndic[0], codeIndic[1:]
                if code in self.arbres[disc].items.keys():
                    item = self.arbres[disc].items[code]
                    cases = self.arbres[disc].GetItemWindow(item, self.arbres[disc].colEleves)
                    if isinstance(cases, ChoixCompetenceEleve):     # Cas des revues à évaluation
                        self.arbres[disc].MiseAJourCasesEleve(codeIndic, cases)     
                    else:
                        self.arbres[disc].CheckItem2(item)
                        self.arbres[disc].AutoCheckChild(item, True)
            
            for codeComp in self.tache.compVisees:
                disc, code = codeComp[0], codeComp[1:]
#                 print("  ", self.arbres[disc].items.keys())
                if code in self.arbres[disc].items.keys():
                    self.arbres[disc].UnselectAll()
                    for cmp in self.tache.compVisees:
                        if disc == cmp[0]:
                            if cmp[1:] in self.arbres[disc].items.keys():
                                i = self.arbres[disc].items[cmp[1:]]
                                self.arbres[disc].CheckItem2(i)
                                self.arbres[disc].AutoCheckChild(i, True)
                    

                
                        
#        if hasattr(self, 'arbres'):
#            for arbre in self.arbres.values():
#                arbre.UnselectAll()
#                for codeIndic in self.tache.indicateursEleve[0]:
#                    if codeIndic[1:] in arbre.items.keys():
#                        item = arbre.items[codeIndic[1:]]
#                        arbre.CheckItem2(item)

        #
        # Intitulé de la tâche
        #    
        if hasattr(self, 'textctrl'):
            self.textctrl.SetValue(self.tache.intitule)
        
        prj = self.tache.GetProjetRef()
#        if not tache.estPredeterminee():
        if hasattr(self, 'cbTache') and prj is not None:
            if self.tache.intitule in prj.taches.keys():
                self.cbTache.SetLabel(self.tache.intitule+"\n"+prj.taches[self.tache.intitule][1])
        
        #
        # Phase de la tâche
        #
        if hasattr(self, 'txtPhas'):
            if self.tache.intitule in prj.taches.keys() and prj is not None:
                self.txtPhas.SetLabel(prj.phases[prj.taches[self.tache.intitule][0]][1])
            else:
                self.txtPhas.SetLabel("")
        
        if hasattr(self, 'cbPhas') and self.tache.phase != '' and prj is not None:
#            print self.tache.phase
#            print self.tache.GetProjetRef().phases[self.tache.phase][1]
            try:
                self.cbPhas.SetStringSelection(prj.phases[self.tache.phase][1])
            except:
                print("Erreur : conflit de type d'enseignement !")
                pass
            
        if sendEvt:
            self.sendEvent(draw = True, verif = True)
        
        
#    #############################################################################
#    def ReconstruireArbres(self):
#        print "ReconstruireArbres", self.tache.phase
#        if hasattr(self, 'arbres'):
#            for arbre in self.arbres.values():
#                arbre.ReConstruire()
                
#        if self.tache.phase in TOUTES_REVUES_EVAL and (True in self.tache.GetReferentiel().compImposees.values()): #self.tache.GetReferentiel().compImposees['C']:
#            print "pas MiseAJourTypeEnseignement", self.tache.GetReferentiel().compImposees.values()
#        else:
#            if hasattr(self, 'panelProprietes'):
#                self.panelProprietes.MiseAJourTypeEnseignement()
            
#            if hasattr(self, 'arbres'):
#                print "arbres"
#                for arbre in self.arbres.values():
#                    arbre.MiseAJourTypeEnseignement(ref)
#            if hasattr(self, 'arbreFct'):
#                self.arbreFct.MiseAJourTypeEnseignement(ref)
        
        
####################################################################################
#
#   Classe définissant le panel de propriété d'un système
#
####################################################################################
class PanelPropriete_Systeme(PanelPropriete):
    def __init__(self, parent, systeme):
#         print("init PanelPropriete_Systeme", systeme)
        self.systeme = systeme
        self.parent = parent
        ref = self.systeme.GetReferentiel()
        
        PanelPropriete.__init__(self, parent, objet = self.systeme)
        
        vs = wx.BoxSizer(wx.VERTICAL)
        
        #
        # Nom
        #
        hs = wx.BoxSizer(wx.HORIZONTAL)
        self.titre = wx.StaticText(self, -1, "Nom %s :" %et2ou(ref._nomSystemes.du_()))
        textctrl = wx.TextCtrl(self, -1, "")
        self.textctrl = textctrl
        
#         self.sizer.Add(titre, (0,0), (1,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 3)
        hs.Add(self.titre, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 3)
        
        # Combo de sélection des Systèmes de la Classe
#         if isinstance(systeme.parent, pysequence.Sequence):
        if isinstance(self.parent, PanelConteneur):
            self.cbListSys = wx.ComboBox(self, -1, "",
                                         choices = [],
                                         style = wx.CB_DROPDOWN
                                         | wx.TE_PROCESS_ENTER
                                         | wx.CB_READONLY
                                         #| wx.CB_SORT
                                         )

            self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.cbListSys)
            hs.Add(self.cbListSys, flag = wx.TOP|wx.BOTTOM|wx.LEFT|wx.EXPAND, border = 3)
            
               
        vs.Add(hs,1, flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        vs.Add(textctrl, flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        
        #
        # Type de système
        #
#         print(ref.listeSystemes)
#         if len(ref.listeSystemes) > 0:
        self.titreTyp = wx.StaticText(self, -1, "Type %s :" %et2ou(ref._nomSystemes.de_()))
        self.tsizer = wx.BoxSizer(wx.VERTICAL)
        cbType = combo_adv.BitmapComboBox(self, -1, "Choisir un type %s" %et2ou(ref._nomSystemes.de_()),
                             choices = [],# size = (-1,25),
                             style = wx.CB_DROPDOWN
                             | wx.TE_PROCESS_ENTER
                             | wx.CB_READONLY
                             #| wx.CB_SORT
                             )
        
        self.cbType = cbType
        for s in [(ref.systemes[t][1], ref.getIconeSysteme(t, 24*SSCALE)) for t in ref.listeSystemes]:
            self.cbType.Append(s[0], s[1])
            
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxSys, cbType)
        
        
        self.tsizer.Add(self.titreTyp, flag = wx.ALIGN_LEFT|wx.LEFT, border = 2)
        self.tsizer.Add(cbType, flag = wx.EXPAND|wx.LEFT, border = 2)
        vs.Add(self.tsizer, flag = wx.EXPAND|wx.ALL, border = 2)
#         self.sizer.Add(tsizer, (2,0), (1, 2), flag = wx.EXPAND|wx.ALL, border = 2)
        vs.Show(self.tsizer, len(ref.listeSystemes) > 0)
        self.vs = vs
        
        #
        # Nombre de systèmes disponibles en paralléle
        #
        vcNombre = VariableCtrl(self, systeme.nbrDispo, signeEgal = True, slider = False, 
                                help = "Nombre de d'exemplaires de %s disponibles simultanément." %et2ou(ref._nomSystemes.ce_()), 
                                scale = SSCALE)
        self.Bind(EVT_VAR_CTRL, self.EvtVar, vcNombre)
        self.vcNombre = vcNombre
        vs.Add(vcNombre, flag = wx.TOP|wx.BOTTOM, border = 3)
#         self.sizer.Add(vcNombre, (3,0), (1, 2), flag = wx.TOP|wx.BOTTOM, border = 3)
        
        
        self.sizer.Add(vs, (0,0), (1, 1), flag = wx.TOP|wx.BOTTOM, border = 3)
        
        #
        # Image
        #
        isizer = self.CreateImageSelect(self, titre = "image %s" %et2ou(ref._nomSystemes.du_()))
        self.sizer.Add(isizer, (0,2), (1,1), flag =  wx.EXPAND|wx.TOP|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        
        #
        # Description de la séance
        #
        vs = wx.BoxSizer(wx.VERTICAL)
        dbox = myStaticBox(self, -1, "Description")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
        tc = richtext.RichTextPanel(self, self.systeme, toolBar = True)
        tc.SetTitre("Description détaillée "+et2ou(ref._nomSystemes.du_()))
        tc.SetToolTip("")
        dbsizer.Add(tc, 1, flag = wx.EXPAND)
        vs.Add(dbsizer, 1, flag = wx.EXPAND|wx.ALL, border = 2)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        
        #
        # Lien
        #
        lsizer = self.CreateLienSelect(self)
        vs.Add(lsizer, flag = wx.EXPAND|wx.ALL, border = 2)
        self.sizer.Add(vs, (0,3), (1, 1), flag = wx.EXPAND|wx.TOP|wx.LEFT, border = 0)
        
        self.MiseAJour()
        self.Verrouiller()
        
        self.sizer.AddGrowableCol(3)
        self.sizer.AddGrowableRow(0)
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
        if marquerModifier:
            self.systeme.GetApp().MarquerFichierCourantModifie()
#         self.btnlien.Show(self.systeme.lien.path != "")
        self.selec.MiseAJour()
        self.Layout()
        self.Refresh()


    #############################################################################            
    def GetDocument(self):
        if isinstance(self.systeme.parent, pysequence.Sequence):
            return self.systeme.parent
        elif isinstance(self.systeme.parent, pysequence.Classe):
            return self.systeme.parent.GetDocument()
    
    
    #############################################################################            
    def EvtComboBox(self, evt):
        """ Sélection d'un système dans la liste des systèmes de la Classe
        """
        
        sel = evt.GetSelection()
#         print("EvtComboBox", sel)
        if sel > 0: # Système lié à la Classe
            classe = self.systeme.GetDocument().classe
            s = classe.systemes[sel-1]
            
#             setBranche(s.getBranche())
#             self.systeme.lienClasse = s

        else: # Nouveau système, lié au document
            p = self.systeme.GetDocument()
            s = pysequence.Systeme(p)
#             self.systeme.setBranche(s.getBranche())
#             self.systeme.lienClasse = None
#         print("Remplace", self.systeme, s)
        self.GetDocument().RemplacerSysteme(self.systeme, s)
        self.SetSysteme(s)
#         print("   ", self.systeme)
        self.Verrouiller()
        
#         self.MiseAJour()
        self.systeme.SetNom(self.systeme.nom)
        self.GetDocument().MiseAJourNomsSystemes()
        
        if isinstance(self.systeme.parent, pysequence.Sequence):
            ref = self.systeme.GetReferentiel()
            self.systeme.parent.MiseAJourNomsSystemes()
            modif = "Modification %s nécessaires" %et2ou(ref._nomSystemes.des_())
            if self.onUndoRedo():
                self.sendEvent(modif = modif, draw = True, verif = True)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif, draw = True, verif = True)
                    self.eventAttente = True


#     #############################################################################            
#     def OnClick(self, event):
#         self.systeme.AfficherLien(self.GetDocument().GetPath())
#         
#         else:
#             mesFormats = u"Fichier Image|*.bmp;*.png;*.jpg;*.jpeg;*.gif;*.pcx;*.pnm;*.tif;*.tiff;*.tga;*.iff;*.xpm;*.ico;*.ico;*.cur;*.ani|" \
#                            u"Tous les fichiers|*.*'"
#              
#             dlg = wx.FileDialog(
#                                 self, message=u"Ouvrir une image",
#     #                            defaultDir = self.DossierSauvegarde, 
#                                 defaultFile = "",
#                                 wildcard = mesFormats,
#                                 style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
#                                 )
#                  
#             # Show the dialog and retrieve the user response. If it is the OK response, 
#             # process the data.
#             if dlg.ShowModal() == wx.ID_OK:
#                 # This returns a Python list of files that were selected.
#                 paths = dlg.GetPaths()
#                 nomFichier = paths[0]
#                 self.systeme.image = rognerImage(wx.Image(nomFichier).ConvertToBitmap())
#                 self.SetImage()
#              
#              
#              
#             dlg.Destroy()
#         
#     #############################################################################            
#     def SetImage(self):
# #        print "SetImage", self.systeme
#         if self.systeme.image != None:
#             
#             self.systeme.image = rognerImage(self.systeme.image)
#             
# #             w, h = self.systeme.image.GetSize()
# #             wf, hf = 200.0, 100.0
# #             r = max(w/wf, h/hf)
# #             _w, _h = w/r, h/r
# #             self.systeme.image = self.systeme.image.ConvertToImage().Scale(_w, _h).ConvertToBitmap()
#             self.image.SetBitmap(self.systeme.image)
#         else:
# #            print "NullBitmap"
#             self.image.SetBitmap(wx.NullBitmap)
#             
#         self.systeme.SetImage()
#         self.Layout()

    #############################################################################            
    def EvtComboBoxSys(self, event):
#        print "EvtComboBoxSys"
        ref = self.systeme.GetReferentiel()
        self.systeme.typ = ref.listeSystemes[event.GetSelection()]
        
        self.Layout()
#        print "ok"
        self.sendEvent(modif = "Modification du type %s" %et2ou(ref._nomSystemes.de_()),
                       draw = True, verif = False)
        
        
        
    #############################################################################            
    def GetPanelPropriete(self):
        return self.parent.Parent.Parent


    #############################################################################            
    def MarquerNomValide(self, etat = True):
        ref = self.systeme.GetReferentiel()
        if etat:
            self.textctrl.SetBackgroundColour("white")
            self.textctrl.SetToolTip("Saisir le nom %s" %et2ou(ref._nomSystemes.du_()))
        else:
            self.textctrl.SetBackgroundColour("pink")
            self.textctrl.SetToolTip("Un autre %s porte déjà ce nom !" %et2ou(ref._nomSystemes.sing_()))
        self.textctrl.Refresh()
        
        

    #############################################################################            
    def EvtText(self, event):
        """ Modification du nom du système
        """
        ref = self.systeme.GetReferentiel()
#         print "EvtText", event.GetString()
        if isinstance(self.systeme.parent, pysequence.Sequence):
            self.systeme.SetNom(event.GetString())
            self.systeme.parent.MiseAJourNomsSystemes()         # mise à jour dans l'arbre de la Séquence
            modif = "Modification du nom %s" %et2ou(ref._nomSystemes.du_())
            if self.onUndoRedo():
                self.sendEvent(modif = modif, draw = True, verif = False)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif, draw = True, verif = False)
                    self.eventAttente = True
        
        elif isinstance(self.systeme.parent, pysequence.Classe):
            classe = self.systeme.parent
            if event.GetString() in [s.nom for s in classe.systemes]:
                self.MarquerNomValide(False)
                return
            self.MarquerNomValide(True)
            self.systeme.SetNom(event.GetString())
#            print "  ***", self.systeme.parent
            self.GetPanelPropriete().MiseAJourListeSys(self.systeme.nom)
            if isinstance(classe.GetDocument(), pysequence.Sequence):
                classe.GetDocument().MiseAJourNomsSystemes()


    #############################################################################            
    def EvtVar(self, event):
        self.systeme.SetNombre()

        if isinstance(self.systeme.parent, pysequence.Sequence):
            ref = self.systeme.GetReferentiel()
            modif = "Modification du nombre %s disponibles" %et2ou(ref._nomSystemes.de_())
            if self.onUndoRedo():
                self.sendEvent(modif = modif, draw = True, verif = True)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif, draw = True, verif = True)
                    self.eventAttente = True

    ######################################################################################  
    def estVerrouille(self):
#         print("estVerrouille", self.systeme)
#         print("   ", self.parent)
#        print "   ", self.systeme.parent
#        classe = self.systeme.GetClasse()
        if isinstance(self.systeme.parent, pysequence.Classe): 
            if isinstance(self.parent, PanelConteneur): # Cas du système édité depuis le panel propriété de la Classe
                return True
            else:
                return False
        
        if self.systeme.lienClasse is not None:
            return True                             # C'est un système qui appartient à la classe
        
        return False
   
    #############################################################################            
    def Verrouiller(self, nom = ""):
        """ Vérrouiller les propriétés du Système
            (quand le Système est défini dans la Classe)
            False = vérrouillé
        """
#        try:
#            self.cbListSys.SetSelection(self.cbListSys.FindString(nom))
#        except:
#            nom = u""
#        etat = nom != u""
        
        etat = not self.estVerrouille()
        
        self.textctrl.Show(etat)
        self.vcNombre.Enable(etat)
        self.selec.Enable(etat)
        self.btImg.Show(etat)
        self.btSupImg.Show(etat)
        self.rtc.Enable(etat)
        self.cbType.Enable(etat)
        self.sizer.Layout()
    
    
    #############################################################################            
    def SetSysteme(self, s):
#         print("SetSysteme", s)
        self.systeme = s
        self.vcNombre.SetVariable(s.nbrDispo)
        self.selec.lien = s.lien
        self.rtc.setObjet(s)
        self.MiseAJour()
    
    
    #############################################################################            
    def MiseAJourTypeEnseignement(self):
        ref = self.systeme.GetReferentiel()
        self.titre.SetLabel("Nom %s :" %et2ou(ref._nomSystemes.du_()))
        self.titreTyp.SetLabel("Type %s :" %et2ou(ref._nomSystemes.de_()))
        self.vcNombre.SetHelp("Nombre de d'exemplaires de %s disponibles simultanément." %et2ou(ref._nomSystemes.ce_()))
        self.MiseAJourImageSelect(titre = "image %s" %et2ou(ref._nomSystemes.du_()))
        
        self.cbType.Clear()
        for s in [(ref.systemes[t][1], ref.getIconeSysteme(t, 24*SSCALE)) for t in ref.listeSystemes]:
            self.cbType.Append(s[0], s[1])
        self.vs.Show(self.tsizer, len(ref.listeSystemes) > 0)
        
        self.MiseAJour()
        self.sizer.Layout()
        
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        """
        """
#         print("MiseAJour panelPropriete Systeme", self.systeme.typ)
        ref = self.systeme.GetReferentiel()
        self.textctrl.ChangeValue(self.systeme.nom)
        self.vcNombre.mofifierValeursSsEvt()
        
        if len(ref.listeSystemes) > 0:
            self.cbType.SetSelection(ref.listeSystemes.index(self.systeme.typ))
#             self.cbType.SetSelection(self.cbType.GetStrings().index(ref.systemes[self.systeme.typ][1]))
        
        self.SetImage()
        
        self.rtc.Ouvrir()

        if isinstance(self.systeme.parent, pysequence.Sequence):
            if sendEvt:
                self.sendEvent(draw = True, verif = True)
            
        self.MiseAJourListeSys(self.systeme.nom)
        self.MiseAJourLien()
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(toSystemEncoding(self.systeme.lien.path), self.systeme.lien.type)
#         self.btnlien.Show(len(self.systeme.lien.path) > 0)
        self.Layout()


    #############################################################################            
    def MiseAJourListeSys(self, nom = None):
        """ Mise à jour du Combo listant les Systèmes définis dans la Classe
        """
        if hasattr(self, 'cbListSys'):
            ls = ["défini localement"]
            classe = self.systeme.GetDocument().classe
            
            for s in classe.systemes:
                ls.append(s.nom)
            self.cbListSys.Set(ls)
            
            if nom != None:
                n = self.cbListSys.FindString(nom)
                if n == wx.NOT_FOUND:
                    self.cbListSys.SetSelection(0)
                else:
                    self.cbListSys.SetSelection(n)
            else:
                self.cbListSys.SetSelection(0)





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
        
        PanelPropriete.__init__(self, parent, objet = self.personne)
        
        #
        # Nom
        #
        box = myStaticBox(self, -1, "Identité")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        bsizer.SetMinSize((300*SSCALE,-1))
        titre = wx.StaticText(self, -1, "Nom : ")
        textctrl = wx.TextCtrl(self, 1)
        self.textctrln = textctrl
        
        nsizer = wx.BoxSizer(wx.HORIZONTAL)
        nsizer.Add(titre, flag = wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)
        nsizer.Add(textctrl, 1, flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        #
        # Prénom
        #
        titre = wx.StaticText(self, -1, "Prénom : ")
        textctrl = wx.TextCtrl(self, 2)
        self.textctrlp = textctrl
        
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        psizer.Add(titre, flag = wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)
        psizer.Add(textctrl, 1, flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        bsizer.Add(nsizer, flag = wx.EXPAND)
        bsizer.Add(psizer, flag = wx.EXPAND)
        self.sizer.Add(bsizer, (0,0), flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
        
        
        #
        # Référent
        #
        if hasattr(self.personne, 'referent'):
            box = myStaticBox(self, -1, "Fonction")
            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            cb = wx.CheckBox(self, -1, "Référent")#, style=wx.ALIGN_RIGHT)
            cb.SetValue(self.personne.referent)
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
            self.cbInt = cb
            bsizer.Add(cb, flag = wx.EXPAND|wx.ALL, border = 3)
            self.sizer.Add(bsizer, (0,1), flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
        
        
        #
        # Discipline
        #
        if hasattr(self.personne, 'discipline'):
            titre = wx.StaticText(self, -1, "Discipline :")
            cbPhas = wx.ComboBox(self, -1, constantes.NOM_DISCIPLINES[self.personne.discipline],
                                 choices = constantes.getLstDisciplines(), size = (-1, 50*SSCALE),
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

        
        
        #
        # Grilles d'évaluation
        #
        if hasattr(self.personne, 'grille'):
            self.boxGrille = myStaticBox(self, -1, "Grilles d'évaluation")
            self.bsizer = wx.StaticBoxSizer(self.boxGrille, wx.VERTICAL)
            self.sizer.Add(self.bsizer, (1,0), (1,2), flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
            self.ConstruireSelectGrille()
            
        #
        # Modèles
        #
        if hasattr(self.personne, 'modeles'):
            box = myStaticBox(self, -1, "Modèles numériques")
            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            pnl = scrolled.ScrolledPanel(self, -1, style = wx.VSCROLL)
            s = wx.BoxSizer(wx.HORIZONTAL)
            pnl.SetSizer(s)
            pnl.SetupScrolling()
            lb = wx.CheckListBox(pnl, -1)
            s.Add(lb, 1, flag = wx.EXPAND)
#             self.Bind(wx.EVT_LISTBOX, self.EvtListBox, lb)
            self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, lb)
#             lb.SetSelection(0)
            self.lb = lb
            bsizer.Add(pnl,1, flag = wx.EXPAND|wx.ALL, border = 3)
            self.sizer.Add(bsizer, (0,1), flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
            
            pnl.FitInside()
        
            
        #
        # Portrait
        #
        isizer = self.CreateImageSelect(self, titre = "portrait", prefixe = "le ", defaut = constantes.AVATAR_DEFAUT)
        self.sizer.Add(isizer, (0,2), (2,1), flag =  wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        
#         
#         box = myStaticBox(self, -1, u"Portrait")
#         bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
#         image = wx.StaticBitmap(self, -1, constantes.AVATAR_DEFAUT)
#         self.image = image
#         self.SetImage()
#         bsizer.Add(image, flag = wx.EXPAND)
#         
#         bt = wx.Button(self, -1, u"Changer le portrait")
#         bt.SetToolTip(u"Cliquer ici pour sélectionner un fichier image")
#         bsizer.Add(bt, flag = wx.EXPAND|wx.ALIGN_BOTTOM)
#         self.Bind(wx.EVT_BUTTON, self.OnClick, bt)
#         self.sizer.Add(bsizer, (0,2), (2,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        #
        # Boutons Charger/Sauvegarder
        #
        if self.personne.titre == "prof":
            bt_sizer = wx.BoxSizer(wx.HORIZONTAL)
            bt_c = wx.Button(self, -1, "Charger")
            self.Bind(wx.EVT_BUTTON, self.OnCharge, bt_c)
            bt_s = wx.Button(self, -1, "Sauvegarder")
            self.Bind(wx.EVT_BUTTON, self.OnSauv, bt_s)
            bt_sizer.Add(bt_c)
            bt_sizer.Add(bt_s)
            self.sizer.Add(bt_sizer, (1,0), (1,2), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
            
        self.MiseAJour()
        
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(1)
        
        self.sizer.Layout()
        
        self.Layout()
        
        
    #############################################################################            
    def ConstruireSelectGrille(self):
#         print("ConstruireSelectGrille", self)
#         print("   ", self.personne.grille)
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
            
            prjeval = self.personne.GetProjetRef()
#             print("   ", prjeval, prjeval.parties)
            self.SelectGrille = {}
            for k in self.personne.grille:
                if k in prjeval.parties:
                    self.SelectGrille[k] = PanelSelectionGrille(self, self.personne, k)
                    self.bsizer.Add(self.SelectGrille[k], flag = wx.EXPAND)
            
            self.boxGrille.Show(True)
            
        else:
            self.boxGrille.Show(False)
            
            
            
    #############################################################################            
    def GetDocument(self):
        return self.personne.GetDocument()


    #############################################################################            
    def GetListProfs(self):
        """ Lit le fichier profs.xml
            et renvoie la liste des Professeurs
            qui y sont enregistrés
        
        """
        nomFichier = os.path.join(util_path.APP_DATA_PATH_USER, constantes.FICHIER_PROFS)
        
        if not os.path.exists(nomFichier):
            return []
        
        # Lecture du fichier
        root = ET.parse(nomFichier).getroot()
#         fichier = open(nomFichier,'r',encoding='utf-8')
#         root = ET.parse(fichier).getroot()
#         fichier.close()
#         try:
#             root = ET.parse(fichier).getroot()
#         except ET.ParseError:
#             messageErreur(wx.GetTopLevelParent(self), "Fichier corrompu", 
#                               "Le fichier %s est corrompu !!\n\n"\
#                               "Réparez-le ou supprimez-le pour continuer à utiliser cette fonctionnalité" %nomFichier)
#             return None
#         finally:
#             fichier.close()
        
        list_p = []

        # Conversion des ET.Element en Professeur
        for b in root:
            p = pysequence.Prof(self.personne.GetDocument())
            p.setBranche(b)
            list_p.append(p)
        
        # Tri par ordre alphabétique
        list_p.sort(key = lambda prof : prof.nom)
        
#         list_p, root = zip(*list_p)
        return list_p


    #############################################################################            
    def OnCharge(self, event):
        
        list_p = self.GetListProfs()
        if list_p is None:
            return
        
        if len(list_p)>0:
            dlg = wx.SingleChoiceDialog(
                    self, 'Sélectionner un Professeur\ndans la liste ci-dessous :',
                    'Liste des Professeurs enregistrés',
                    [p.GetNomPrenom() for p in list_p], 
                    style = wx.CHOICEDLG_STYLE
                    )
    
            if dlg.ShowModal() == wx.ID_OK:
                referent = self.personne.referent
                self.personne.setBranche(list_p[dlg.GetSelection()].getBranche())
                self.personne.referent = referent # Ca évite des conflits ...
                modif = "Chargement d'un Professeur"
                self.MiseAJour()
                self.sendEvent(modif = modif, draw = True, verif = False)
                self.personne.SetCode()
            dlg.Destroy()
            
        else:
            messageInfo(self, "Aucun Professeur", 
                    "La liste des Professeurs enregistrés est vide.")

        
       
        
        
    #############################################################################            
    def OnSauv(self, event):
        """ 
        """
#         print("OnSauv", self.GetListProfs())
        
        # Construction de la structure XML
        root = ET.Element("Professeurs")
        
        list_p = self.GetListProfs()
        
        if self.personne in list_p:
            dlg = wx.MessageDialog(self, "Le professeur %s existe déjà dans la liste\n\n" \
                                           "Voulez-vous le remplacer ?" %(self.personne.GetNomPrenom()),
                                             "Professeur existant",
                                             wx.ICON_INFORMATION | wx.YES_NO
                                             )
            res = dlg.ShowModal()
            dlg.Destroy()
            if res != wx.ID_YES:
                return
        
        list_p.append(self.personne)
        
        # Tri par ordre alphabétique
        list_p.sort(key = lambda prof : prof.nom)
        
        
        for p in list_p:
            root.append(p.getBranche())
        constantes.indent(root)
        
        
        # Enregistrement en XML
        enregistrer_root(root, os.path.join(util_path.APP_DATA_PATH_USER, 
                                            constantes.FICHIER_PROFS))
        messageInfo(self, "Enregistrement réussi", 
                    "Le professeur %s a bien été ajouté." %self.personne.GetNomPrenom())


#     #############################################################################            
#     def OnClick(self, event):
# #        for k, g in self.personne.grille.items():
# #            if event.GetId() == self.btnlien[k].GetId():
# #                g.Afficher(self.GetDocument().GetPath())
# ##        if event.GetId() == self.btnlien[0].GetId():
# ##            self.personne.grille[0].Afficher(self.GetDocument().GetPath())
# ##        elif event.GetId() == self.btnlien[1].GetId():
# ##            self.personne.grille[1].Afficher(self.GetDocument().GetPath())
# #            
# #        else:
#         mesFormats = u"Fichier Image|*.bmp;*.png;*.jpg;*.jpeg;*.gif;*.pcx;*.pnm;*.tif;*.tiff;*.tga;*.iff;*.xpm;*.ico;*.ico;*.cur;*.ani|" \
#                        u"Tous les fichiers|*.*'"
#         
#         dlg = wx.FileDialog(
#                             self, message=u"Ouvrir une image",
# #                            defaultDir = self.DossierSauvegarde, 
#                             defaultFile = "",
#                             wildcard = mesFormats,
#                             style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
#                             )
#             
#         # Show the dialog and retrieve the user response. If it is the OK response, 
#         # process the data.
#         if dlg.ShowModal() == wx.ID_OK:
#             # This returns a Python list of files that were selected.
#             paths = dlg.GetPaths()
#             nomFichier = paths[0]
#             self.personne.avatar = rognerImage(wx.Image(nomFichier).ConvertToBitmap())
#             self.SetImage()
#             self.sendEvent(modif = u"Modification du portrait de la personne")
#             
#         dlg.Destroy()
#         
#         
#     #############################################################################            
#     def SetImage(self):
#         if self.personne.avatar != None:
#             self.personne.avatar = constantes.ReSize_avatar(self.personne.avatar)
#             self.image.SetBitmap(self.personne.avatar)
#         self.personne.SetImage()
#         self.Layout()
        
        
        
    #############################################################################            
    def EvtText(self, event):
        if event.GetId() == 1:
            self.personne.SetNom(event.GetString())
        else:
            self.personne.SetPrenom(event.GetString())
#        self.personne.GetDocument().MiseAJourNomsEleves()
        
        modif = "Modification du nom de la personne"
        if self.onUndoRedo():
            self.sendEvent(modif = modif, draw = True, verif = False)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = modif, draw = True, verif = False)
                self.eventAttente = True
        

    #############################################################################            
    def EvtComboBox(self, event):
        self.personne.SetDiscipline(get_key(constantes.NOM_DISCIPLINES, self.cbPhas.GetStringSelection()))
        self.Layout()
        self.sendEvent(modif = "Modification de la discipline du professeur", 
                       draw = True, verif = False)


    #############################################################################            
    def EvtCheckBox(self, event):
        self.personne.GetDocument().SetReferent(self.personne, event.IsChecked())
        self.sendEvent(modif = "Changement de status (référent) du professeur", 
                       draw = True, verif = False)

    #############################################################################            
    def EvtCheckListBox(self, event):
        index = event.GetSelection()
#         label = self.lb.GetString(index)
        self.personne.AjouterEnleverModele(index)
        
        self.sendEvent(modif = "Modification des modèles associés à %s" %self.personne.GetReferentiel().getLabel("ELEVES").le_(), 
                       draw = False, verif = False)
        
    #############################################################################            
    def MiseAJourTypeEnseignement(self):
        print("MiseAJourTypeEnseignement panel", self.personne)
        if hasattr(self.personne, 'grille'):
#            print "MiseAJourTypeEnseignement eleve", self.personne
            if hasattr(self, 'SelectGrille'):
                for sg in list(self.SelectGrille.values()):
                    self.bsizer.Detach(sg)
                    sg.Destroy()
            self.ConstruireSelectGrille()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#         print "MiseAJour panelPropriete Personne", self.personne
#         print self.personne.grille
        doc = self.personne.GetDocument()
        self.textctrln.ChangeValue(self.personne.nom)
        self.textctrlp.ChangeValue(self.personne.prenom)
        if hasattr(self, 'cbPhas'):
            self.cbPhas.SetStringSelection(constantes.NOM_DISCIPLINES[self.personne.discipline])
        
        if hasattr(self, 'cbInt'):
            self.cbInt.SetValue(self.personne.referent)
            doc.SetReferent(self.personne, self.cbInt.IsChecked())
        
        if hasattr(self, 'SelectGrille'):
            for k, select in self.SelectGrille.items():
                select.SetPath(toSystemEncoding(self.personne.grille[k].path))
#            self.OnPathModified()

        if hasattr(self, 'lb'):
            self.lb.Set(doc.support.GetIntitModeles())
            for i, m in enumerate(doc.support.modeles):
                if m.id in self.personne.modeles:
                    self.lb.Check(i)
            self.lb.Refresh()

        if sendEvt:
            self.sendEvent(draw = True, verif = True)

    ######################################################################################  
    def OnPathModified(self, lien = "", marquerModifier = True):
        if marquerModifier:
            self.personne.GetApp().MarquerFichierCourantModifie()
        self.Layout()
        self.Refresh()
   
        



####################################################################################
#
#   Classe définissant le panel de propriété d'une personne
#
####################################################################################
class PanelPropriete_Groupe(PanelPropriete):
    def __init__(self, parent, groupe):
#        print "PanelPropriete_Personne", personne
        self.groupe = groupe
        self.parent = parent
        
        PanelPropriete.__init__(self, parent, objet = self.groupe)
        
        #
        # Type d'enseignement
        #
        self.pourProjet = self.GetDocument().estProjet()
        titre = myStaticBox(self, -1, "Type d'enseignement")
        titre.SetMinSize((180*SSCALE, 100*SSCALE))
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
#         te = ArbreTypeEnseignement(self, self)
        te = Panel_SelectEnseignement(self, self, self.pourProjet, self.groupe)
        
        self.st_type = wx.StaticText(self, -1, "")
        self.st_type.Show(False)
        sb.Add(te, 1, flag = wx.EXPAND)
        sb.Add(self.st_type, 1, flag = wx.EXPAND)

        self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, te)
 
        te.MiseAJour()
#         te.SetStringSelection(REFERENTIELS[constantes.TYPE_ENSEIGNEMENT_DEFAUT].Enseignement[0])

        self.sizer.Add(sb, (0,0), (2,1), flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)#
        self.cb_type = te
        
        

        #
        # Nom
        #
        box = myStaticBox(self, -1, "Nom du groupe")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        textctrl = wx.TextCtrl(self, 1)
        self.textctrln = textctrl
    
        bsizer.Add(textctrl, 1, flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        self.sizer.Add(bsizer, (0,1), (1,1), flag =  wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
        
        
        
        #
        # Etablissement
        #
        titre = myStaticBox(self, -1, "Établissement")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        sh = wx.BoxSizer(wx.HORIZONTAL)
        t = wx.StaticText(self, -1, "Académie :")
        sh.Add(t, flag = wx.EXPAND)
        
        lstAcad = sorted([a[0] for a in list(constantes.ETABLISSEMENTS.values())])
        self.cba = wx.ComboBox(self, -1, "sélectionner une académie ...", (-1,-1), 
                         (-1, -1), lstAcad+[""],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboAcad, self.cba)
#         self.Bind(wx.EVT_TEXT, self.EvtComboAcad, self.cba)
        sh.Add(self.cba, flag = wx.EXPAND|wx.LEFT, border = 5)
        sb.Add(sh, flag = wx.EXPAND)
        
        sh = wx.BoxSizer(wx.HORIZONTAL)
        t = wx.StaticText(self, -1, "Ville :")
        sh.Add(t, flag = wx.EXPAND)
     
        self.cbv = SlimSelector(self, -1, "sélectionner une ville ...", (-1,-1), 
                         (-1, -1), [],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboVille, self.cbv)
        self.Bind(wx.EVT_TEXT, self.EvtComboVille, self.cbv)
        sh.Add(self.cbv, 1,flag = wx.ALIGN_CENTER_VERTICAL|wx.LEFT, border = 5)
        sb.Add(sh, flag = wx.EXPAND)
        
        t = wx.StaticText(self, -1, "Établissement :")
        sb.Add(t, flag = wx.EXPAND)
        
        self.cbe = wx.ComboBox(self, -1, "sélectionner un établissement ...", (-1,-1), 
                         (-1, -1), ["autre ..."],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboEtab, self.cbe)
        sb.Add(self.cbe, flag = wx.EXPAND)
        
        self.sizer.Add(sb, (1,1), (1,1), flag =  wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        
        
        #
        # Portrait
        #
        isizer = self.CreateImageSelect(self, titre = "portrait", prefixe = "le ", defaut = constantes.AVATAR_DEFAUT)
        self.sizer.Add(isizer, (0,2), (2,1), flag =  wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
                    
                    
                    
        #
        # Elèves
        #
        ref = groupe.GetReferentiel()
        n = ref.getLabel("ELEVES").Plur_()
        titre = myStaticBox(self, -1, "%s du groupe" %n)
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        

        self.list_ctrl = EditableListCtrl(self, -1,
                                         img = (images.Icone_ajout_eleve.GetBitmap(),
                                                images.Icone_suppr_eleve.GetBitmap()),
                                          hlp = ("Ajouter %s au groupe" %ref.getLabel("ELEVES").un_(), 
                                                 "Supprimer la selection"))
        self.list_ctrl.InsertColumn(0, 'Nom')
        self.list_ctrl.InsertColumn(1, 'Prénom')
#         self.list_ctrl.Bind(wx.EVT_TOOL, self.OnClick)
        
        
        sb.Add(self.list_ctrl, flag = wx.EXPAND)
        
        
        self.sizer.Add(sb, (0,3), (2,1), flag =  wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
        
        self.MiseAJour()
        
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(1)
        
        self.sizer.Layout()
        
        self.Layout()
        
        self.list_ctrl.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnClick)
        self.list_ctrl.Bind(wx.EVT_LIST_INSERT_ITEM, self.OnClick)
        self.list_ctrl.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnClick)
    
    #############################################################################            
    def OnClick(self, event):
        print("OnClick")
        event.Skip()
        wx.CallAfter(self.SetList)
    
    
    #############################################################################            
    def SetList(self):
        l = []
        for n, p in self.list_ctrl.GetListItem():
            l.append((n, p))
        self.groupe.SetListEleves(l)
        ref = self.groupe.GetReferentiel()
        self.sendEvent(modif = "Modification de la liste %s du groupe." %ref.getLabel("ELEVES").des_(),
                       draw = False, verif = False)
    
    #############################################################################            
    def GetDocument(self):
        return self.groupe.GetDocument()


    
    
        ######################################################################################  
    def EvtComboAcad(self, evt = None, modif = True):
#        print "EvtComboAcad"
        if evt != None:
            self.groupe.academie = evt.GetString()

        lst = []
        for val in list(constantes.ETABLISSEMENTS.values()):
            if self.groupe.academie == val[0]:
                if self.groupe.GetReferentiel().getTypeEtab() == 'L':
                    lst = val[2]
                else:
                    lst = val[1]
                break
#        print "   ", lst
        if len(lst) > 0:
            lst = sorted(list(set([v for _, v in lst])))
#        print "Villes", lst

        self.cbv.Set(lst)
        self.cbv.SlimResize()
#        self.cbv.SetSize((self.cbv.GetSizeFromTextSize(),-1))
        self.cbv.Refresh()
        
        if modif:
            self.sendEvent(modif = "Modification de l'académie",
                           draw = True, verif = False)
            
    
    ######################################################################################  
    def EvtComboVille(self, evt = None, modif = True):
#        print "EvtComboVille"
        if evt != None:
            self.groupe.ville = evt.GetString()
#        print "   ", self.classe.ville
        lst = []
        for val in list(constantes.ETABLISSEMENTS.values()):
            if self.groupe.academie == val[0]:
                if self.groupe.GetReferentiel().getTypeEtab() == 'L':  # Lycée
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
        
        if modif:
            self.sendEvent(modif = "Modification de la ville",
                           draw = True, verif = False)
        
            
        
    ######################################################################################  
    def EvtComboEtab(self, evt):       
#        if evt.GetSelection() == len(constantes.ETABLISSEMENTS_PDD):
#            self.classe.etablissement = self.textctrl.GetStringSelection()
#            self.AfficherAutre(True)
#        else:
        self.groupe.etablissement = evt.GetString()
#        self.AfficherAutre(False)

        self.sendEvent(modif = "Modification de l'établissement",
                       draw = True, verif = False)



    
    #############################################################################            
    def EvtText(self, event):
        self.groupe.SetNom(event.GetString())
        
        modif = "Modification du nom du groupe"
        if self.onUndoRedo():
            self.sendEvent(modif = modif, draw = True, verif = False)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = modif, draw = True, verif = False)
                self.eventAttente = True             
                    
    ######################################################################################  
    def EvtRadioBox(self, event = None, CodeFam = None):
        """ Sélection d'un type d'enseignement
        """
        if event != None:
            radio_selected = event.GetEventObject()
            CodeFam = Referentiel.getEnseignementLabel(radio_selected.GetLabel())
#         print "EvtRadioBox", self.groupe.typeEnseignement, ">>>", CodeFam
        self.groupe.typeEnseignement = CodeFam[0]
        
        self.Refresh()
        
        self.groupe.SetCode()
        
        self.sendEvent(modif = "Modification du type d'enseignement",
                       draw = True, verif = True)
        

    
    
    
    #############################################################################            
    def MiseAJour(self, sendEvt = False, marquerModifier = True):
#         print("MiseAJour panelPropriete Groupe", self.groupe.typeEnseignement)
#         print "  ", REFERENTIELS.keys()
#         self.cb_type.SetStringSelection(self.groupe.typeEnseignement)
#         self.cb_type.SetStringSelection(REFERENTIELS[self.groupe.typeEnseignement].Enseignement[0])
        self.cb_type.MiseAJour()
        
        self.textctrln.ChangeValue(self.groupe.nom)

        self.cba.SetValue(self.groupe.academie)
        self.EvtComboAcad(modif = False)
        self.cbv.SetValue(self.groupe.ville)
        self.EvtComboVille(modif = False)
        self.cbe.SetValue(self.groupe.etablissement)
        
        self.list_ctrl.SetListItem(self.groupe.GetListEleves())
        
        if sendEvt:
            self.sendEvent(draw = True, verif = True)


   

         
###################################################################################
class PanelSelectionGrille(wx.Panel):
    def __init__(self, parent, eleve, codeGrille):
        wx.Panel.__init__(self, parent, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.eleve = eleve
        self.codeGrille = codeGrille
        titre = wx.StaticText(self, -1, eleve.GetProjetRef().parties[codeGrille])
        self.SelectGrille = lien.URLSelectorCombo(self, eleve.grille[codeGrille], 
                                             eleve.GetDocument().GetPath(), 
                                             dossier = False, ext = "Classeur Excel (*.xls*)|*.xls*")
        self.Bind(lien.EVT_PATH_MODIFIED, self.OnPathModified)
#         self.btnlien = wx.Button(self, -1, u"Ouvrir")
#         self.btnlien.Show(self.eleve.grille[self.codeGrille].path != "")
#         self.Bind(wx.EVT_BUTTON, self.OnClick, self.btnlien)
        sizer.Add(titre, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 3)
        sizer.Add(self.SelectGrille,1, flag = wx.EXPAND|wx.ALL, border = 3)
#         sizer.Add(self.btnlien, flag = wx.EXPAND|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 3)
        
        self.Layout()
        self.SetSizerAndFit(sizer)

    
    ######################################################################################################
    def GetPanelRacine(self):
        return self.Parent.GetPanelRacine()


    #############################################################################            
    def OnClick(self, event):
        self.eleve.grille[self.codeGrille].Afficher(self.eleve.GetDocument().GetPath())
                
                
    #############################################################################            
    def SetPath(self, path):#, marquerModifier):  
        self.SelectGrille.SetPath(path, 'f')#, marquerModifier = marquerModifier)          
                
                
    ######################################################################################  
    def OnPathModified(self, evt):#lien = "", marquerModifier = True):
#         self.btnlien.Show(self.eleve.grille[self.codeGrille].path != "")
        self.SelectGrille.MiseAJour()
        self.Parent.OnPathModified(evt.lien)#, marquerModifier)
                
                
                
####################################################################################
#
#   Classe définissant le panel de propriété d'un support de projet
#
####################################################################################
class PanelPropriete_Support(PanelPropriete):
    def __init__(self, parent, support):
        
        self.support = support
        self.parent = parent
        
        PanelPropriete.__init__(self, parent, objet = self.support)
        
        #
        # Nom
        #
        box = myStaticBox(self, -1, "Nom du support")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        textctrl = TextCtrl_Help(self, "", scale = SSCALE)
        textctrl.SetTitre("Nom du support")
        textctrl.SetToolTip("Le support est le matériel ou logiciel\n" \
                                  "sur lequel %s réalisent\n" \
                                  "les modélisations et expérimentations." %self.support.GetReferentiel().getLabel("ELEVES").les_())
        self.textctrl = textctrl
        bsizer.Add(textctrl, 1, flag = wx.EXPAND)
        self.sizer.Add(bsizer, (0,0), flag = wx.EXPAND|wx.ALL, border = 2)
#         self.Bind(stc.EVT_STC_CHANGE, self.EvtText, textctrl)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, textctrl)
        
        
        #
        # Lien
        #
        lsizer = self.CreateLienSelect(self)
        self.sizer.Add(lsizer, (1,0), flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        #
        # Image
        #
        isizer = self.CreateImageSelect(self, titre = "image du support")
        self.sizer.Add(isizer, (0,1), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)
#         
#         box = myStaticBox(self, -1, u"Image du support")
#         bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
#         image = wx.StaticBitmap(self, -1, wx.NullBitmap)
#         image.Bind(wx.EVT_RIGHT_UP, self.OnRClickImage)
#         self.image = image
#         self.SetImage()
#         bsizer.Add(image, flag = wx.EXPAND)
#         bt = wx.Button(self, -1, u"Changer l'image")
#         bt.SetToolTip(u"Cliquer ici pour sélectionner un fichier image")
#         bsizer.Add(bt, flag = wx.EXPAND)
#         self.Bind(wx.EVT_BUTTON, self.OnClick, bt)
#         self.sizer.Add(bsizer, (0,1), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)#wx.ALIGN_CENTER_VERTICAL |

        
        #
        # Description du support
        #
        dbox = myStaticBox(self, -1, "Description du support")
        dbsizer = wx.StaticBoxSizer(dbox, wx.HORIZONTAL)
#        bd = wx.Button(self, -1, u"Editer")
        tc = richtext.RichTextPanel(self, self.support, toolBar = True)
        tc.SetTitre("Description du support")
        tc.SetToolTip("Description du support :\n" \
                            " - modèle\n" \
                            " - documentation\n" \
                            " - liens Internet\n" \
                            " - ..."
                            )
#         tc.SetMaxSize((-1, 150))
#        dbsizer.Add(bd, flag = wx.EXPAND)
        dbsizer.Add(tc, flag = wx.EXPAND)
#        self.Bind(wx.EVT_BUTTON, self.EvtClick, bd)

        self.sizer.Add(dbsizer, (0,2), (2, 1), flag = wx.EXPAND|wx.ALL, border = 2)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        self.MiseAJour()
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(2)
        
        self.sizer.Layout()
        
        
        
        
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        self.selec.SetPathSeq(pathSeq)
        
        
    ######################################################################################  
    def OnPathModified(self, lien, marquerModifier = True):
        self.support.OnPathModified()
        if marquerModifier:
            self.support.GetApp().MarquerFichierCourantModifie()
#         self.btnlien.Show(self.support.lien.path != "")
        self.selec.MiseAJour()
        self.Layout()
        self.Refresh()
        
        
    #############################################################################            
    def GetDocument(self):
        return self.support.parent
    

    #############################################################################            
    def EvtText(self, event):
#         print "EvtText", self.support.nom
        txt = self.textctrl.GetText()
        
        if self.support.nom != txt:
            event.Skip()
            self.support.SetNom(txt)
    #        self.support.parent.MiseAJourNomsSystemes()
            
            modif = "Modification de l'intitulé du Support"
            
            if self.onUndoRedo():
                self.sendEvent(modif = modif, draw = True, verif = False)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif, draw = True, verif = False)
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
    def MiseAJour(self, sendEvt = False, marquerModifier = True):
#        print "MiseAJour panelPropriete Support"
        self.textctrl.ChangeValue(self.support.nom)
        if sendEvt:
            self.sendEvent(draw = True, verif = True)
        self.MiseAJourLien()
        self.SetImage()
        
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(toSystemEncoding(self.support.lien.path), self.support.lien.type,
                           marquerModifier = False)
#         self.btnlien.Show(len(self.support.lien.path) > 0)
        self.selec.MiseAJour()
        self.Layout()
        
        
        
        
        
####################################################################################
#
#   Classe définissant le panel de propriété d'un support de projet
#
####################################################################################
class PanelPropriete_Modele(PanelPropriete):
    def __init__(self, parent, modele):
        
        self.modele = modele
        self.parent = parent
        
        PanelPropriete.__init__(self, parent, objet = self.modele)
        
        #
        # Nom
        #
        box = myStaticBox(self, -1, "Intitulé du modèle")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        textctrl = TextCtrl_Help(self, "", scale = SSCALE)
        textctrl.SetTitre("Intitulé du modele")
        textctrl.SetToolTip("Un modèle numérique peut être\n" \
                                  "une maquette numérique\n" \
                                  "un modèle multiphysique\n" \
                                  "...")
        self.textctrl = textctrl
        bsizer.Add(textctrl, 1, flag = wx.EXPAND)
        self.sizer.Add(bsizer, (0,0), flag = wx.EXPAND|wx.ALL, border = 2)
#         self.Bind(stc.EVT_STC_CHANGE, self.EvtText, textctrl)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, textctrl)
        
        
        
        #
        # Logiciel ArbreLogiciels
        #
        titre = myStaticBox(self, -1, "Logiciel utilisé")
        titre.SetMinSize((180*SSCALE, 100*SSCALE))
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        te = ArbreLogiciels(self, self)
        
        sb.Add(te, 1, flag = wx.EXPAND)
        
#         self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, te)
 
#         te.SetStringSelection(self.modele)

        self.sizer.Add(sb, (0,1), flag = wx.EXPAND|wx.ALL, border = 2)#
        self.cb_type = te
        
        self.cb_type.Layout()
        self.cb_type.CalculatePositions()
        
        #
        # Lien
        #
        lsizer = self.CreateLienSelect(self)
        self.sizer.Add(lsizer, (1,0), (1,2), flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        
        
        #
        # Image
        #
        isizer = self.CreateImageSelect(self, titre = "image du modèle")
        self.sizer.Add(isizer, (0,2), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)

        
        #
        # Description du modèle
        #
        dbox = myStaticBox(self, -1, "Description du modèle")
        dbsizer = wx.StaticBoxSizer(dbox, wx.HORIZONTAL)
#        bd = wx.Button(self, -1, u"Editer")
        tc = richtext.RichTextPanel(self, self.modele, toolBar = True)
        tc.SetTitre("Description du modèle")
        tc.SetToolTip("Description du modèle :\n" \
                            " - type de modèle\n" \
                            " - logiciel utilisé\n" \
                            " - paramètres principaux\n" \
                            " - ..."
                            )
#         tc.SetMaxSize((-1, 150*SSCALE))
#        dbsizer.Add(bd, flag = wx.EXPAND)
        dbsizer.Add(tc, flag = wx.EXPAND)
#        self.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        self.sizer.Add(dbsizer, (0,3), (2, 1), flag = wx.EXPAND|wx.ALL, border = 2)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        self.MiseAJour()
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(2)
        
        self.sizer.Layout()
        
        

        
        
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        self.selec.SetPathSeq(pathSeq)
        
        
    ######################################################################################  
    def OnPathModified(self, lien, marquerModifier = True):
        self.modele.OnPathModified()
        if marquerModifier:
            self.modele.GetApp().MarquerFichierCourantModifie()
#         self.btnlien.Show(self.support.lien.path != "")
        self.selec.MiseAJour()
        self.Layout()
        self.Refresh()
        
        
    #############################################################################            
    def GetDocument(self):
        return self.modele.GetDocument()
    

    #############################################################################            
    def EvtText(self, event):
#         print "EvtText", self.support.nom
        txt = self.textctrl.GetText()
        
        if self.modele.intitule != txt:
            event.Skip()
            self.modele.SetNom(txt)
    #        self.support.parent.MiseAJourNomsSystemes()
            
            modif = "Modification de l'intitulé du Modèle"
            
            if self.onUndoRedo():
                self.sendEvent(modif = modif, draw = False, verif = False)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif)
                    self.eventAttente = True
        
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False, marquerModifier = True):
#        print "MiseAJour panelPropriete modele"
        self.textctrl.ChangeValue(self.modele.intitule)
        self.cb_type.CheckItems(self.modele.logiciels)
        
        
        if sendEvt:
            self.sendEvent(draw = False, verif = False)
        self.MiseAJourLien()
        self.SetImage()
        
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(toSystemEncoding(self.modele.lien.path), self.modele.lien.type,
                           marquerModifier = False)
#         self.btnlien.Show(len(self.support.lien.path) > 0)
        self.selec.MiseAJour()
        self.Layout()
    
    
    ######################################################################################  
    def OnCheckModele(self):
#         print "OnCheckModele"
        self.modele.logiciels = self.cb_type.GetAllChecked()
        self.modele.SetLogiciel()
#         print(self.modele.logiciels)
        self.sendEvent(modif = "Modification du logiciel du Modèle",
                       draw = False, verif = False)
        




####################################################################################
#
#   Classe définissant l'arbre de structure de base d'un document
#
####################################################################################*
class ArbreDoc(CT.CustomTreeCtrl):
    def __init__(self, parent, classe, panelProp,
                 imglst = [], 
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.SUNKEN_BORDER|wx.WANTS_CHARS,
                 ):
        if int(wx.version()[0]) > 2:
            agwStyle = CT.TR_HAS_BUTTONS|CT.TR_HAS_VARIABLE_ROW_HEIGHT | CT.TR_HIDE_ROOT|CT.TR_TOOLTIP_ON_LONG_ITEMS
        else:
            agwStyle = CT.TR_HAS_BUTTONS|CT.TR_HAS_VARIABLE_ROW_HEIGHT | CT.TR_HIDE_ROOT
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
        # Les icones des branches
        #
        self.images = {}
        s = (IMG_SIZE_TREE[0]*SSCALE, IMG_SIZE_TREE[1]*SSCALE)
        il = wx.ImageList(*s)
        for k, i in imglst:
#             print k, i.GetBitmap().GetWidth(), i.GetBitmap().GetHeight()
#             self.images[k] = il.Add(i.GetBitmap())
            self.images[k] = il.Add(scaleImage(i.GetBitmap(), 
                                               *s))
        self.AssignImageList(il)
        
        
        
        #
        # On instancie un panel de propriétés vide pour les éléments qui n'ont pas de propriétés
        #
#        self.panelVide = PanelPropriete(self.panelProp)
#        self.panelVide.Hide()
        
        #
        # Construction de l'arbre
        #
        root = self.AddRoot("")
        self.classe.ConstruireArbre(self, root)
        self.root = root
        
        self.itemDrag = None
        self.fctDrop = None
        
        #
        # Gestion des évenements
        #
        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(CT.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightDown)
        
        self.Bind(CT.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
#         self.GetMainWindow().Bind(wx.EVT_MOUSE_CAPTURE_LOST, lambda x: None)
        self.Bind(CT.EVT_TREE_END_DRAG, self.OnEndDrag)
        self.Bind(wx.EVT_MOTION, self.OnMove)
        
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
#         self.Bind(wx.EVT_TREE_KEY_DOWN, self.OnKey)
        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
#        self.Bind(wx.EVT_CHAR, self.OnChar)
        
#         self.ExpandAll()
        
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        
        
#     def OnSetFocus(self, event):
#         print "OnSetFocus"
#         event.Skip()
            
    ######################################################################################################
    def GetApp(self):
        return self.doc.GetApp()
    
    
    ######################################################################################################
    def OnEnter(self, event):
        self.SetFocusIgnoringChildren()
        event.Skip()
    
#     ###############################################################################################
#     def OnKey(self, evt):
#         print "OnKey"
    
    
    ###############################################################################################
    def ReSelectItem(self, item):
        self.SelectItem(item, select=False)
        self.SelectItem(item)
        
        
    ###############################################################################################
    def OnKeyDown(self, evt):
#         print "OnKeyDown"
        keycode = evt.GetKeyCode()
        item = self.GetSelection()
#         print keycode
        if keycode == wx.WXK_DELETE:
            self.doc.SupprimerItem(item)
            
        elif evt.ControlDown() and keycode == 67: # Crtl-C
            self.GetItemPyData(item).CopyToClipBoard()


        elif evt.ControlDown() and keycode == 86: # Crtl-V
            self.doc.CollerElem(item = item)
            
        evt.Skip()


    ####################################################################################
    def OnRightDown(self, event):
#         print "OnRightDown", self.doc
        item = event.GetItem()
        self.doc.AfficherMenuContextuel(item)
        
        
    ####################################################################################
    def OnLeftDClick(self, event):
        pt = event.GetPosition()
        item = self.HitTest(pt)[0]
        if item:
            self.doc.AfficherLien(item)
        event.Skip()    
        
        
    ######################################################################################  
    def GetPanelPropriete(self, parent, code, texte = ""):
#         print(code)
#         if code == "Sea":
#             return PanelPropriete_Racine(parent, constantes.TxtRacineSeance)
#         elif code == "Obj":
#             return PanelPropriete_Racine(parent, constantes.TxtRacineObjectif)
#         elif code == "Pre":
#             return PanelPropriete_Racine(parent, constantes.TxtRacinePrerequis)
#         elif code == "Sys":
#             return PanelPropriete_Racine(parent, constantes.TxtRacineSysteme)
#         elif code == "Equ":
#             return PanelPropriete_Racine(parent, constantes.TxtRacineEquipe)
#         elif code == "Tac":
#             return PanelPropriete_Racine(parent, constantes.TxtRacineTache)
#         elif code == "Ele":
#             return PanelPropriete_Racine(parent, constantes.TxtRacineEleve)
#         elif code == "Seq":
        return PanelPropriete_Racine(parent, texte)
#         
#         return 
    
    
    ####################################################################################
    def OnSelChanged(self, event = None, item = None):
        """ Fonction appelée lorsque la selection a été changée dans l'arbre
            ---> affichage du panel de Propriétés associé
        """
#         tps1 = time.clock()
        
        self.panelProp.Freeze()
        wx.BeginBusyCursor()
        
        #
        # On ferme l'éventuelle fenêtre d'aide ...
        #
        CloseFenHelp()
        
        
        #
        # On récupère les données associées à la branche cliquée ...
        #
        if item is None:
            self.item = event.GetItem()
        else:
            self.item = item
        data = self.GetItemPyData(self.item)
#         print("OnSelChanged", data)
        if isinstance(data, tuple) and hasattr(data[0], 'GetPanelPropriete'):
            panelPropriete = data[0].GetPanelPropriete(self.panelProp, data[1], data[2])
        elif hasattr(data, 'GetPanelPropriete'):
            panelPropriete = data.GetPanelPropriete(self.panelProp)
        elif isinstance(data, str): # 
            panelPropriete = self.GetPanelPropriete(self.panelProp, data)
        else:
            print("err : ", data)
#         print("   >>", panelPropriete)
        if panelPropriete is None:
            panelPropriete = self.GetPanelPropriete(self.panelProp, data.toolTip)
        
        #
        # On centre la fiche sur l'objet
        #
        if hasattr(self.classe.doc.GetApp(), 'fiche'):
            fiche = self.classe.doc.GetApp().fiche
            if self.classe.doc.centrer:
                fiche.CentrerSur(data)
            fiche.Surbrillance(data)
            
        self.classe.doc.centrer = True
        
        
        if panelPropriete:
#             tps2 = time.clock() 
#             print "> panelPropriete", panelPropriete
            self.panelProp.AfficherPanel(panelPropriete)
            self.parent.Refresh()
#         else:
#             print("rien", panelPropriete)
#         tps3 = time.clock() 
        
        
#         wx.CallAfter(self.panelProp.Thaw)
#         wx.CallAfter(wx.EndBusyCursor)
        self.panelProp.Thaw()
        wx.EndBusyCursor()
        
        
        if event is not None:
            event.Skip()
        


    ####################################################################################
    def OnBeginDrag(self, event):
        self.itemDrag = event.GetItem()
        if self.item:
            event.Allow()


        
    ######################################################################################              
    def OnToolTip(self, event):
        node = event.GetItem()
        data = self.GetPyData(node)
#         print("OnToolTip", data)
        if hasattr(data, 'toolTip'):
            if isstring(data.toolTip):
#                 print("   1:", data.toolTip)
                event.SetToolTip(wx.ToolTip(data.toolTip))
            else:
#                 print("   2:", self.GetItemText(node))
                event.SetToolTip(wx.ToolTip(self.GetItemText(node)))
        elif isstring(data):
            if data == "Seq" and self.doc.toolTip is not None:
#                 print("   3:", self.doc.toolTip)
                event.SetToolTip(wx.ToolTip(self.doc.toolTip))
            else:
#                 print("   4:", self.GetItemText(node))
                event.SetToolTip(wx.ToolTip(self.GetItemText(node)))
        else:
            event.Skip()
        




####################################################################################
#
#   Classe définissant l'arbre de structure de la séquence
#
####################################################################################
class ArbreSequence(ArbreDoc):
    def __init__(self, parent, sequence, classe, panelProp):

        ArbreDoc.__init__(self, parent, classe, panelProp,
                          imglst = list(constantes.dicimages.items()) + list(constantes.imagesSeance.items()))
        
        self.parent = parent
        
        #
        # La séquence 
        #
        self.sequence = sequence
        self.doc = sequence
        
#         #
#         # Les icones des branches
#         #
#         self.images = {}
#         il = wx.ImageList(*constantes.IMG_SIZE_TREE*SSCALE)
#         for k, i in constantes.dicimages.items() + constantes.imagesSeance.items():
# #             print k, i.GetBitmap().GetWidth(), i.GetBitmap().GetHeight()
# #             self.images[k] = il.Add(i.GetBitmap())
#             self.images[k] = il.Add(scaleImage(i.GetBitmap(), 
#                                                *constantes.IMG_SIZE_TREE*SSCALE))
#         self.AssignImageList(il)
        
        
        #
        # Construction de l'arbre
        #
        self.sequence.ConstruireArbre(self, self.root)
        
        
#        self.panelProp.AfficherPanel(self.sequence.GetPanelPropriete())

#        self.CurseurInsert = wx.CursorFromImage(constantes.images.CurseurInsert.GetImage())
        self.CurseurInsertApres = wx.Cursor(constantes.images.Curseur_InsererApres.GetImage())
        self.CurseurInsertDans = wx.Cursor(constantes.images.Curseur_InsererDans.GetImage())
        

    
        
        
#    ####################################################################################
#    def AjouterObjectif(self, event = None):
#        self.sequence.AjouterObjectif()
        
        
#    ####################################################################################
#    def SupprimerObjectif(self, event = None, item = None):
#        self.sequence.SupprimerObjectif(item)

            
#    ####################################################################################
#    def AjouterSeance(self, event = None):
#        seance = self.sequence.AjouterSeance()
#        self.lstSeances.append(self.AppendItem(self.seances, u"Séance :", data = seance))
        
#    ####################################################################################
#    def AjouterRotation(self, event = None, item = None):
#        seance = self.sequence.AjouterRotation(self.GetItemPyData(item))
#        self.SetItemText(item, u"Rotation")
#        self.lstSeances.append(self.AppendItem(item, u"Séance :", data = seance))
        
#    ####################################################################################
#    def AjouterSerie(self, event = None, item = None):
#        seance = self.sequence.AjouterRotation(self.GetItemPyData(item))
#        self.SetItemText(item, u"Rotation")
#        self.lstSeances.append(self.AppendItem(item, u"Séance :", data = seance))
        
    ####################################################################################
    def SupprimerSeance(self, event = None, item = None):
        if self.sequence.SupprimerSeance(self.GetItemPyData(item)):
            self.lstSeances.remove(item)
            self.Delete(item)
            
        

    ####################################################################################
    def OnCompareItems(self, item1, item2):
        i1 = self.GetItemPyData(item1)
        i2 = self.GetItemPyData(item2)
        return int(i1.ordre - i2.ordre)

    ####################################################################################
    def OnMove(self, event):
        
            
        if not self.HasFocus():
            self.SetFocusIgnoringChildren()
            
        if self.itemDrag != None:
            self.fctDrop = None
            item = self.HitTest(wx.Point(event.GetX(), event.GetY()))[0]
            
            if item != None:
                dataTarget = self.GetItemPyData(item)
                dataSource = self.GetItemPyData(self.itemDrag)
                
                if dataTarget == "Sea":
                    dataTarget = self.sequence
                
                if isinstance(dataSource, pysequence.Seance) and dataTarget != dataSource:
                    if not hasattr(dataTarget, 'GetNiveau') or dataTarget.GetNiveau() + dataSource.GetProfondeur() > 2:
                        self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
                        return 0
        
        
                    # Insérer "dans"  (racine ou "R" ou "S")  .panelSeances
                    if dataTarget == self.sequence \
                       or (isinstance(dataTarget, pysequence.Seance) and dataTarget.EstSeance_RS()):
                        if dataSource.EstSousSeance() and dataSource.parent.EstSeance_RS() \
                              and len(dataSource.parent.seances) == 1:  # On ne peut pas supprimer la dernière séance d'une rotation ou série
                            self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
                            return
                            
                        elif not dataSource in dataTarget.seances:    # parents différents
        #                    print dataSource.typeSeance, dataTarget.seances[0].GetListeTypes()
                            if dataTarget.GetNiveau() + dataSource.GetProfondeur() > 1:
                                self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
                                return
                            
                            elif not dataSource.typeSeance in dataTarget.seances[0].GetListeTypes():
                                self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
                                return
                            
                            else:
                                self.SetCursor(self.CurseurInsertDans)
                                self.fctDrop = self.InsererDans
                            
                        else:
                            self.SetCursor(self.CurseurInsertApres)
                            self.fctDrop = self.InsererApres
        #                    print "2"
                            return 2
                    
                    # Insérer "aprés"
                    elif isinstance(dataTarget, pysequence.Seance):
                        if dataTarget.parent != dataSource.parent:  # parents différents
        #                    print dataSource.typeSeance, dataTarget.GetListeTypes()
                            if dataSource.EstSousSeance() and dataSource.parent.EstSeance_RS() \
                              and len(dataSource.parent.seances) == 1:  # On ne peut pas supprimer la dernière séance d'une rotation ou série
                                self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
                                return 0
                                
                            elif not dataSource.typeSeance in dataTarget.GetListeTypes():
                                self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
        #                        print "0-4"
                                return 0
                            
                            elif dataTarget.parent == dataSource:
                                self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
                                return 0
                            
                            else:
                                self.fctDrop = self.InsererApresDansDiff
                                self.SetCursor(self.CurseurInsertApres)
        #                        print "3"
                                return 3
                        else:
                            self.fctDrop = self.InsererApresDansMeme
                            self.SetCursor(self.CurseurInsertApres)
        #                    print "4"
                            return 4
                    
                    else:
                        self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
                        return 0
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
#                 a = self.getActionDnD(dataSource, dataTarget)
#                 if a == 0:
#                     self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
#                 elif a == 1:
#                     self.SetCursor(self.CurseurInsertDans)
#                 elif a == 2 or a == 3 or a == 4:
#                     self.SetCursor(self.CurseurInsertApres)

#                 self.lastItem = item
                
#         else:
#             if hasattr(self, "lastItem"):
#                 del self.lastItem
#                 self.RefreshSelectedUnder(self.itemDrag)
#                if not isinstance(dataSource, Seance):
#                    self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
#                else:
#                    # Premiére place !
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
        
    
        if isinstance(dataSource, pysequence.Seance) and dataTarget != dataSource:
            if not hasattr(dataTarget, 'GetNiveau') or dataTarget.GetNiveau() + dataSource.GetProfondeur() > 2:
#                print "0.1"
                return 0


            # Insérer "dans"  (racine ou "R" ou "S")  .panelSeances
            if dataTarget == self.sequence \
               or (isinstance(dataTarget, pysequence.Seance) and dataTarget.EstSeance_RS()):
                if dataSource.parent.EstSeance_RS() \
                      and len(dataSource.parent.seances) == 1:  # On ne peut pas supprimer la dernière séance d'une rotation ou série
                        return 0
                    
                elif not dataSource in dataTarget.seances:    # parents différents
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
            
            # Insérer "aprés"
            elif isinstance(dataTarget, pysequence.Seance):
                if dataTarget.parent != dataSource.parent:  # parents différents
#                    print dataSource.typeSeance, dataTarget.GetListeTypes()
                    if dataSource.parent.EstSeance_RS() \
                      and len(dataSource.parent.seances) == 1:  # On ne peut pas supprimer la dernière séance d'une rotation ou série
                        return 0
                        
                    elif not dataSource.typeSeance in dataTarget.GetListeTypes():
#                        print "0-4"
                        return 0
                    
                    elif dataTarget.parent == dataSource:
                        return 0
                    
                    else:
#                        print "3"
                        return 3
                else:
#                    print "4"
                    return 4
            
            else:
                return 0




#            if isinstance(dataTarget, Seance):
#                # source et target ont le méme parent (méme niveau dans l'arbre)
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
    
    
    
    ####################################################################################
    def OnEndDrag(self, event):
        self.item = event.GetItem()
        if self.item is None:
            self.itemDrag = None
            event.Skip()      
            return
        dataTarget = self.GetItemPyData(self.item)
        dataSource = self.GetItemPyData(self.itemDrag)
        
        if self.fctDrop is not None:
            tx = "Changement de position de la Séance"
            self.fctDrop(dataSource, dataTarget)
            if type(dataTarget) == str : # Déjà item parent de la rubrique à trier
                self.SortChildren(self.item)
            else:
                self.SortChildren(self.GetItemParent(self.item))
            self.GetApp().sendEvent(self.sequence, modif = tx, 
                                    draw = True, verif = True) # Solution pour déclencher un "redessiner"
            
            
            
        self.itemDrag = None
        self.fctDrop = None
        event.Skip()       
    
    
    
    ####################################################################################
    def InsererDans(self, dataSource, dataTarget):
        lstS = dataSource.parent.seances
        lstT = dataTarget.seances
        s = lstS.index(dataSource)
        lstT.insert(0, lstS.pop(s))
        dataSource.parent = dataTarget
        
        self.sequence.OrdonnerSeances()
        self.sequence.reconstruireBrancheSeances(dataSource.parent, dataTarget)
        
    
    
    ####################################################################################
    def InsererApres(self, dataSource, dataTarget):
        lst = dataSource.parent.seances
        s = lst.index(dataSource)
        lst.insert(0, lst.pop(s))
           
        self.sequence.OrdonnerSeances() 
#         if dataTarget == self.sequence:
#             self.SortChildren(self.item)
#         else:
#             self.SortChildren(self.GetItemParent(self.item))
                
        
    ####################################################################################
    def InsererApresDansDiff(self, dataSource, dataTarget):
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
        
    
    ####################################################################################
    def InsererApresDansMeme(self, dataSource, dataTarget):
        lst = dataTarget.parent.seances
        s = lst.index(dataSource)
        t = lst.index(dataTarget)
        
        if t > s:
            lst.insert(t, lst.pop(s))
        else:
            lst.insert(t+1, lst.pop(s))
           
        self.sequence.OrdonnerSeances() 
        self.SortChildren(self.GetItemParent(self.item))
        
        
#     ####################################################################################
#     def OnEndDrag2(self, event):
#         """ Gestion des glisser-déposer
#         """
#         self.item = event.GetItem() 
#         if self.item is not None:
#             dataTarget = self.GetItemPyData(self.item)
#             if dataTarget == "Sea":
#                 dataTarget = self.sequence
#     #         if isinstance(dataTarget, PanelPropriete_Racine):
#     #             dataTarget = self.sequence
#             
#             dataSource = self.GetItemPyData(self.itemDrag)
#             tx = "Changement de position de la Séance"
#             a = self.getActionDnD(dataSource, dataTarget)
# #             print "OnEndDrag", a
#             if a == 1:
#                 lstS = dataSource.parent.seances
#                 lstT = dataTarget.seances
#                 s = lstS.index(dataSource)
#                 lstT.insert(0, lstS.pop(s))
#                 dataSource.parent = dataTarget
#                 
#                 self.sequence.OrdonnerSeances()
#                 self.sequence.reconstruireBrancheSeances(dataSource.parent, dataTarget)
#                 self.GetApp().sendEvent(self.sequence, modif = tx, draw = True, verif = True) # Solution pour déclencher un "redessiner"
#             
#             elif a == 2:
#                 lst = dataSource.parent.seances
#                 s = lst.index(dataSource)
#                 lst.insert(0, lst.pop(s))
#                    
#                 self.sequence.OrdonnerSeances() 
#                 if dataTarget == self.sequence:
#                     self.SortChildren(self.item)
#                 else:
#                     self.SortChildren(self.GetItemParent(self.item))
#                 self.GetApp().sendEvent(self.sequence, modif = tx, draw = True, verif = True) # Solution pour déclencher un "redessiner"
#             
#             elif a == 3:
#                 lstT = dataTarget.parent.seances
#                 lstS = dataSource.parent.seances
#                 s = lstS.index(dataSource)
#                 t = lstT.index(dataTarget)
#                 lstT[t+1:t+1] = [dataSource]
#                 del lstS[s]
#                 p = dataSource.parent
#                 dataSource.parent = dataTarget.parent
#                 
#                 self.sequence.OrdonnerSeances()
#                 self.sequence.reconstruireBrancheSeances(dataTarget.parent, p)
#                 self.GetApp().sendEvent(self.sequence, modif = tx, draw = True, verif = True) # Solution pour déclencher un "redessiner"
#             
#             elif a == 4:
#                 lst = dataTarget.parent.seances
#                 s = lst.index(dataSource)
#                 t = lst.index(dataTarget)
#                 
#                 if t > s:
#                     lst.insert(t, lst.pop(s))
#                 else:
#                     lst.insert(t+1, lst.pop(s))
#                    
#                 self.sequence.OrdonnerSeances() 
#                 self.SortChildren(self.GetItemParent(self.item))
#                 self.GetApp().sendEvent(self.sequence, modif = tx, draw = True, verif = True) # Solution pour déclencher un "redessiner"
#                     
#         self.itemDrag = None
#         event.Skip()
        
    
#     ####################################################################################
#     def OnToolTip(self, event):
# 
#         item = event.GetItem()
#         if item:
#             event.SetToolTip(wx.ToolTip(self.GetItemText(item)))






    
####################################################################################
#
#   Classe définissant l'arbre de structure d'un projet
#
####################################################################################
class ArbreProjet(ArbreDoc):
    def __init__(self, parent, projet, classe, panelProp):

        ArbreDoc.__init__(self, parent, classe, panelProp,
                        imglst =  list(constantes.imagesProjet.items()) \
                                + list(constantes.imagesTaches.items()) \
                                + list(constantes.IMG_LOGICIELS.items()))
        
        self.parent = parent
        
        #
        # La séquence 
        #
        self.projet = projet
        self.doc = projet
        
#         #
#         # Les icones des branches
#         #
#         self.images = {}
#         il = wx.ImageList(*constantes.IMG_SIZE_TREE*SSCALE)
#         for k, i in constantes.imagesProjet.items() + constantes.imagesTaches.items():
# #             self.images[k] = il.Add(i.GetBitmap())
#             self.images[k] = il.Add(scaleImage(i.GetBitmap(), 
#                                                *constantes.IMG_SIZE_TREE*SSCALE))
#             
#         self.AssignImageList(il)

        #
        # Construction de l'arbre
        #
        self.projet.ConstruireArbre(self, self.root)
     
#        self.panelProp.AfficherPanel(self.projet.GetPanelPropriete())

#        self.CurseurInsert = wx.CursorFromImage(constantes.images.CurseurInsert.GetImage())
        self.CurseurInsertApres = wx.Cursor(constantes.images.Curseur_InsererApres.GetImage())
        self.CurseurInsertDans = wx.Cursor(constantes.images.Curseur_InsererDans.GetImage())
                
        
            
    
            
    ####################################################################################
    def AjouterEleve(self, event = None):
        self.projet.AjouterEleve()
        
        
    ####################################################################################
    def SupprimerEleve(self, event = None, item = None):
        self.projet.SupprimerEleve(item)

            
    ####################################################################################
    def AjouterTache(self, event = None):
        obj = self.GetItemPyData(self.GetSelection())
        if not isinstance(obj, pysequence.Tache):
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
    def OnCompareItems(self, item1, item2):
        i1 = self.GetItemPyData(item1)
        i2 = self.GetItemPyData(item2)
        if hasattr(i1, 'ordre'):   # cas des tâches, ...
            return int(i1.ordre - i2.ordre)
        elif hasattr(i1, 'id'):   # cas des élèves/groupes
            return int(i1.id - i2.id)
        else:# ???
            return int(i1.GetOrdre() - i2.GetOrdre())
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
        if not self.HasFocus():
            self.SetFocusIgnoringChildren()

        if self.itemDrag != None:
            item = self.HitTest(wx.Point(event.GetX(), event.GetY()))[0]
            if item != None:
                dataTarget = self.GetItemPyData(item)
                dataSource = self.GetItemPyData(self.itemDrag)
                if not isinstance(dataSource, pysequence.Tache):
                    self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
                else:
                    if not isinstance(dataTarget, pysequence.Tache) \
                        or (dataTarget.phase != dataSource.phase and dataSource.phase !="Rev"):
                        self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
                    else:
                        if dataTarget != dataSource:# and dataTarget.parent == dataSource.parent:
                            self.SetCursor(self.CurseurInsertApres)
                        else:
                            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
                        
        event.Skip()
        
        
    ####################################################################################
    def OnEndDrag(self, event):
        self.item = event.GetItem()
        dataTarget = self.GetItemPyData(self.item)
        dataSource = self.GetItemPyData(self.itemDrag)
        if not isinstance(dataSource, pysequence.Tache):
            pass
        else:
            if not isinstance(dataTarget, pysequence.Tache):
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
                    self.GetApp().sendEvent(self.projet, modif = "Changement de position de la Tâche", 
                                            draw = True, verif = True) # Solution pour déclencher un "redessiner"
    
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
#   Classe définissant l'arbre de structure d'une progression
#
####################################################################################
class ArbreProgression(ArbreDoc):
    def __init__(self, parent, progression, classe, panelProp):

        ArbreDoc.__init__(self, parent, classe, panelProp,
                          imglst = list(constantes.imagesProgression.items()))
        
        self.parent = parent
        
        #
        # La progression 
        #
        self.progression = progression
        self.doc = progression
        
#         #
#         # Les icones des branches
#         #
#         self.images = {}
#         il = wx.ImageList(*constantes.IMG_SIZE_TREE*SSCALE)
#         for k, i in constantes.imagesProgression.items():
# #             self.images[k] = il.Add(i.GetBitmap())
#             self.images[k] = il.Add(scaleImage(i.GetBitmap(), 
#                                                *constantes.IMG_SIZE_TREE*SSCALE))
#         self.AssignImageList(il)
#         
        #
        # Construction de l'arbre
        #
        self.progression.ConstruireArbre(self, self.root)
        
#        self.panelProp.AfficherPanel(self.progression.panelPropriete)

#        self.CurseurInsert = wx.CursorFromImage(constantes.images.CurseurInsert.GetImage())
        self.CurseurInsertApres = wx.Cursor(constantes.images.Curseur_InsererApres.GetImage())
        self.CurseurInsertDans = wx.Cursor(constantes.images.Curseur_InsererDans.GetImage())
 


    ####################################################################################
    def OnCompareItems(self, item1, item2):
        i1 = self.GetItemPyData(item1)
        i2 = self.GetItemPyData(item2)
        prog = self.doc
        if isinstance(i1, pysequence.Prof):
            return int(prog.equipe.index(i1) - prog.equipe.index(i2))
        else:
            return int(prog.sequences_projets.index(i1) - prog.sequences_projets.index(i2))
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
        
#     ####################################################################################
#     def EstMovable(self, obj):
#         return isinstance(obj, pysequence.LienSequence) \
#             or isinstance(obj, pysequence.LienProjet) \
#             or isinstance(obj, pysequence.Prof)


#     ####################################################################################
#     def EstMemeCategorie(self, obj1, obj2):
#         return type(obj1) is type(obj2) \
#             or (isinstance(obj1, pysequence.LienSequence) and isinstance(obj2, pysequence.LienProjet)) \
#             or (isinstance(obj2, pysequence.LienSequence) and isinstance(obj1, pysequence.LienProjet))


    ####################################################################################
    def OnMove(self, event):
        event.Skip()
        
        if not self.HasFocus():
            self.SetFocusIgnoringChildren()
        
        if self.itemDrag != None:
            self.fctDrop = None
            item = self.HitTest(wx.Point(event.GetX(), event.GetY()))[0]
            
            if item != None:
                dataTarget = self.GetItemPyData(item)
                dataSource = self.GetItemPyData(self.itemDrag)
#                 print("dataTarget", dataTarget, type(dataTarget))
                if dataTarget == dataSource:
                    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
                    return
                    
#                 if not dataSource.EstMovable() or not dataSource.EstMemeCategorie(dataTarget):
#                     self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
#                     return
#                     print("Movable :", dataSource.EstMovable(), 
#                           "- EstMemeCategorie :", dataSource.EstMemeCategorie(dataTarget))
                
                if isinstance(dataTarget, pysequence.Prof):
                    self.SetCursor(self.CurseurInsertApres)
                    self.fctDrop = self.InsererApres
                    return
#                     elif dataTarget.GetPosition() <= dataSource.GetPosition():
                if isinstance(dataSource, pysequence.Prof) \
                  and dataTarget == "Equ":
                    self.SetCursor(self.CurseurInsertApres)
                    self.fctDrop = self.InsererApres
                    return
                    
                if isinstance(dataTarget, pysequence.ElementProgression)  \
                  and dataTarget.MemeRang(dataSource):
                    self.SetCursor(self.CurseurInsertApres)
                    self.fctDrop = self.InsererApres
                    return
                    
                if isinstance(dataSource, pysequence.ElementProgression) \
                  and dataTarget == "Seq":
                    self.SetCursor(self.CurseurInsertApres)
                    self.fctDrop = self.InsererApres
                    return
                  
                  
                  
                self.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
#                         print("MemeRang :", dataTarget.MemeRang(dataSource))

        

    ####################################################################################
    def InsererApres(self, dataSource, dataTarget):
        """ Déplace dataSource Après dataTarget
            On suppose que la compatibilité des deux datas a déjà été vérifiée
        """
        if isinstance(dataTarget, pysequence.Prof):
            lst = self.progression.equipe
            s = lst.index(dataSource)
            t = lst.index(dataTarget)
            if t > s:
                lst.insert(t, lst.pop(s))
            else:
                lst.insert(t+1, lst.pop(s))
            
            self.GetApp().sendEvent(self.progression, modif = "Changement de position d'un professeur", 
                                    draw = True, verif = False) # Solution pour déclencher un "redessiner"
        
        elif dataTarget == "Equ":
            lst = self.progression.equipe
            s = lst.index(dataSource)
            lst.insert(0, lst.pop(s))

            self.GetApp().sendEvent(self.progression, modif = "Changement de position d'un professeur", 
                                    draw = True, verif = False) # Solution pour déclencher un "redessiner"
        
        
        elif isinstance(dataTarget, pysequence.ElementProgression):
            dataSource.rang = dataTarget.rang + 1
            self.progression.Ordonner()
            
            if isinstance(dataSource, pysequence.LienSequence):
                self.GetApp().sendEvent(self.progression, modif = "Changement de position d'une Séquence", 
                                        draw = True, verif = True) # Solution pour déclencher un "redessiner"
            else:
                self.GetApp().sendEvent(self.progression, modif = "Changement de position d'un Projet", 
                                        draw = True, verif = True) # Solution pour déclencher un "redessiner"
        
        elif dataTarget == "Seq":
            dataSource.rang = -1
            self.progression.Ordonner()
            
            if isinstance(dataSource, pysequence.LienSequence):
                self.GetApp().sendEvent(self.progression, modif = "Changement de position d'une Séquence", 
                                        draw = True, verif = True) # Solution pour déclencher un "redessiner"
            else:
                self.GetApp().sendEvent(self.progression, modif = "Changement de position d'un Projet", 
                                        draw = True, verif = True) # Solution pour déclencher un "redessiner"
            
    
    ####################################################################################
    def OnEndDrag(self, event):
        self.item = event.GetItem()
        if self.item is None:
            self.itemDrag = None
            event.Skip()      
            return
        dataTarget = self.GetItemPyData(self.item)
        dataSource = self.GetItemPyData(self.itemDrag)
        
        if self.fctDrop is not None:
            self.fctDrop(dataSource, dataTarget)
            if type(dataTarget) == str : # Déjà item parent de la rubrique à trier
                self.SortChildren(self.item)
            else:
                self.SortChildren(self.GetItemParent(self.item))
        
        self.itemDrag = None
        self.fctDrop = None
        event.Skip()            

    



class ArbreCompSav(HTL.HyperTreeList):
    def __init__(self, parent, typ, savoirsRef, savoirs, 
                 pp = None, filtre = None, et = False, agwStyle = 0):
        """ Arbre de sélection de Compétences ou de Savoirs
        
            :parent: conteneur WX
            :pp: PanelPropriété de référence
        """
        HTL.HyperTreeList.__init__(self, parent, -1, 
                                   agwStyle = wx.TR_MULTIPLE|wx.TR_HIDE_ROOT|CT.TR_AUTO_CHECK_CHILD|\
                                   CT.TR_AUTO_CHECK_PARENT|CT.TR_HAS_VARIABLE_ROW_HEIGHT|HTL.TR_NO_HEADER|agwStyle) # wx.TR_DEFAULT_STYLE|<< le dernier pour accepter les texte multiligne (ça marche mais pas débuggé)
#         print("ArbreSavoirs", savoirs)
        self.parent = parent
        
        if pp == None:
            self.pp = parent
        else:
            self.pp = pp
            
        self.typ = typ
        self.filtre = filtre






class ArbreSavoirs(HTL.HyperTreeList):#, listmix.ListRowHighlighter):
    def __init__(self, parent, typ, savFiltre, savoirsRef, filtre = None,
                 pp = None, et = False, agwStyle = 0):
        """    
            :parent: 
            :typ:
            :savFiltre: dictionnaire des compétences à afficher dans l'abre (sortie de GetDicFiltre())
            :savoirsRef: type referentiel.Competences
            :pp: PanelPropriete contenant les méthodes AjouterEnlever...
        """
        HTL.HyperTreeList.__init__(self, parent, -1, 
                                   agwStyle = wx.TR_MULTIPLE|wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|CT.TR_AUTO_CHECK_CHILD|\
                                   CT.TR_AUTO_CHECK_PARENT|CT.TR_HAS_VARIABLE_ROW_HEIGHT|HTL.TR_NO_HEADER|CT.TR_FULL_ROW_HIGHLIGHT| \
                                   agwStyle) # wx.TR_DEFAULT_STYLE|<< le dernier pour accepter les texte multiligne (ça marche mais pas débuggé)
        
#         listmix.ListRowHighlighter.__init__(self, (206, 218, 255))
        
#         print("ArbreSavoirs")
        self.parent = parent
        
        if pp == None:
            self.pp = parent
        else:
            self.pp = pp
            
        self.items = {}
        
#         if savoirs is None:
#             savoirs = savoirsRef.dicSavoirs
            
#         self.savoirs = savoirs          # Les Savoirs sélectrionnés
        self.savoirsRef = savoirsRef    # L'objet Referentiel.Savoirs
        self.typ = typ
        self.filtre = filtre
      
        ref = self.pp.GetReferentiel()
        
        self.AddColumn("")
        self.SetMainColumn(0)
        self.root = self.AddRoot("")
        
        #
        # Colonnes taxonomie
        #
#         print(self.savoirsRef.nivTaxo)
        doc = self.pp.GetDocument()
        for f in self.savoirsRef.nivTaxo:
            if f == "Spe":
                for s in doc.classe.specialite:
                    self.AddColumn(s, flag = wx.ALIGN_CENTER)
                    
            elif f == "EnsSpe":
                for es in ref.listeEnsSpecif:
                    self.AddColumn(es, flag = wx.ALIGN_CENTER)
            
            else:
                self.AddColumn(f, flag = wx.ALIGN_CENTER)
                
        if self.GetColumnCount() > 1:
            self.SetAGWWindowStyleFlag(self.GetAGWWindowStyleFlag()^HTL.TR_NO_HEADER)           


#         self.taxo =  self.savoirsRef.TaxoDefinie()
#         if self.taxo:
#             
#             doc = self.pp.GetDocument()
#             print("taxo")
#             if hasattr(doc.classe, "specialite"): # cas des Séances
#                 self.SetAGWWindowStyleFlag(self.GetAGWWindowStyleFlag()^HTL.TR_NO_HEADER)
#                 self.AddColumn(doc.classe.specialite)
#                 
#             if hasattr(doc, "ensSpecif"): # cas des Séances
#                 print("   ", doc.ensSpecif)
#                 self.SetAGWWindowStyleFlag(self.GetAGWWindowStyleFlag()^HTL.TR_NO_HEADER)
#                 self.AddColumn(doc.ensSpecif)
#                 for es in ref.listeEnsSpecif:
#                     self.AddColumn(es)

        
        self.SetItemBold(self.root, True)
        
        # Dictionnaire filtré :
#         dic_f = self.GetDicFiltre(savoirsRef.dicSavoirs)
#         print("filtre Sav", self.filtre)
        self.Construire(self.root, savFiltre, et = et)
        
#         wx.CallAfter(self.OnSelChanged)
        wx.CallAfter(self.connect)
#         self.ExpandAll()
        
        
        
    
    ######################################################################################################
    def connect(self):
        #
        # Gestion des évenements
        #
        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnItemCheck)
        self.Bind(wx.EVT_SIZE, self.OnSize2)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        
        self.Bind(CT.EVT_TREE_ITEM_EXPANDED, self.OnCollOrExp)
        self.Bind(CT.EVT_TREE_ITEM_COLLAPSED, self.OnCollOrExp)
        
        self.GetMainWindow().Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnGetToolTip)
        
        self.OnSize2()
        
        
    ######################################################################################################
    def OnEnter(self, event):
#        print "OnEnter PanelPropriete"
        self.SetFocus()
        event.Skip()
    
    ######################################################################################################
    def OnSelChanged(self, event=None):
#         print("OnSelChanged")
        if event is None:
            item = None
        else:
            item = event.GetItem()
        self.ExpandAll()
        def unselectAll(branche, niveau = 0):
            for i in branche.GetChildren():
                if not unselectAll(i, niveau+1):
                    return False
                if i.IsChecked():
                    return False
            if niveau >= 3:
                try: # RuntimeError: wrapped C/C++ object of type TreeListMainWindow has been deleted
                    self.Collapse(branche)
                except:
                    pass
            return True
        
        unselectAll(self.root)
            
        if item is not None:
            self.Expand(item)
        
        if event is not None:
            event.Skip()
    
    ####################################################################################
    def OnSize2(self, evt = None):
#         print("OnSize2")
        ww = 0
        for c in range(1, self.GetColumnCount()):
            ww += self.GetColumnWidth(c)
        w = self.GetClientSize()[0] - ww - 20*SSCALE # + un petit peu (20 par expérience) pour la barre de défilement
        if w != self.GetColumnWidth(0):
            self.SetColumnWidth(0, w)
            if self.IsShown():
                self.wrap(w)
        
        if evt is not None:
            evt.Skip()
            
    ####################################################################################
    def wrap(self,w):
        item = self.GetRootItem()
#         font = wx.ClientDC(self).GetFont()
        if item != None:
            dc = wx.ClientDC(self)
            while 1: # On parcoure toutes les lignes de l'arbre
                item = self.GetNext(item)
                if item == None:
                    break
                 
                # Coefficient pour le texte en gras (plus large)
                # Et position en X du texte
                if item._type == 0:
                    W = w*0.93 - 5*SSCALE
                else:
                    W = w - 35*SSCALE # 35 correspond au décallage des "enfants" (cases à cocher)
                
                text = self.GetItemText(item, 0).replace("\n", "")
#                 try:
#                     f = self.GetItemFont(item)#.GetPixelSize()
#                     print dc.GetFullTextExtent("text", f)
#                     print f.GetPixelSize()
#                 except:
#                     pass
#                 wx.ClientDC(self).SetFont(f)
                text = wordwrap(text, W*0.9, dc) # Je ne comprends pas mais il faut ce 0.9 ...
             
                self.SetItemText(item, text, 0)
#         wx.ClientDC(self).SetFont(font)


    ####################################################################################
    def OnCollOrExp(self, event):
        self.AlternColour()
        
    ####################################################################################
    def AlternColour(self, parent = None, pair = False):
#         print("AlternColour")
        if parent is None:
            parent = self.GetRootItem()
        item, cookie = self.GetFirstChild(parent)
    
        while item != None and item.IsOk():
            if not item.IsHidden():#self.IsVisible(item):
                if pair:
                    self.SetItemBackgroundColour(item, wx.Colour(0xDFDFDF))
                else:
                    self.SetItemBackgroundColour(item, self.GetBackgroundColour())
                pair = not pair
                
            if self.ItemHasChildren(item):
                self.AlternColour(item, pair)
            item, cookie = self.GetNextChild(parent, cookie)
    
        return
            
            
    ####################################################################################
    def Construire(self, branche, dic, et = False, niveau = 0):#, pair = None):
        """ Construction d'une branche de "savoirs"
            <et> = prérequis ETT pour spécialité STI2D ?? plus utilisé ??
            
            fonction récursive
        """
        if dic == None:
            return
#         if pair is None:
#             pair = [False]
#         print(" "*niveau, "Construire", dic)

        clefs = constantes.trier(list(dic.keys()))
        sep = "\n" + CHAR_POINT + " "
        
        for k in clefs:
            #
            # Tooltip
            #
            if type(dic[k][0].sousSav) == list:
                if self.filtre is not None:
                    lstPoints = [ss.intitule for i, ss in enumerate(dic[k][0].sousSav) if k+'.'+str(i) in self.filtre]
                else:
                    lstPoints = [ss.intitule for i, ss in enumerate(dic[k][0].sousSav)]
                toolTip = CHAR_POINT + " " + sep.join(lstPoints)
            else:
                toolTip = None
#             print("toolTip", toolTip)

            #
            # L'item avec la case ou pas
            #
            if dic[k][1] is None or len(dic[k][1]) > 1:
                ct_type = 1
            else:
                ct_type = 0
            
            
                
            b = self.AppendItem(branche, k+" "+dic[k][0].intitule, 
                                ct_type = ct_type, 
                                data = toolTip)
            
            
            #
            # Taxonomie
            #
            ref = self.pp.GetReferentiel()
            doc = self.pp.GetDocument()
            col = 1
#             print("nivTaxo", k, " : ", self.savoirsRef.nivTaxo)
            
            # format dans __init__() :
#             for f in self.savoirsRef.nivTaxo:
#                 if f == "Spe":
#                     for s in doc.classe.specialite:
#                         self.AddColumn(s, flag = wx.ALIGN_CENTER)
#                 elif f == "EnsSpe":
#                     
#                     for es in ref.listeEnsSpecif:
#                         self.AddColumn(es, flag = wx.ALIGN_CENTER)
                    
            
            
            for i, f in enumerate(self.savoirsRef.nivTaxo):  # Même structure que dans _init_
                if f == "Spe":
                    for sp in doc.classe.specialite:
                        for sn in dic[k][0].nivTaxo[i]:
                            s, n = sn.split("-")
                            if s == sp:
                                self.SetItemText(b, n, col)
                        col += 1
                elif f == "EnsSpe":
                    d = dict([l.split("-") for l in dic[k][0].nivTaxo[i]])
                    for es in ref.listeEnsSpecif:
                        if es in d.keys():
                            self.SetItemText(b, d[es], col)
                        col += 1
            
                else:
                    if len(dic[k][0].nivTaxo[i]) > 0:
                        self.SetItemText(b, " ".join(dic[k][0].nivTaxo[i]), col)
                    
                    
                    
#             for i, f in enumerate(self.savoirsRef.nivTaxo):  # Même structure que dans _init_
#                 if f == "Spe":
#                     for sn in dic[k][0].nivTaxo[i]:
#                         s, n = sn.split("-")
#                         if s in doc.classe.specialite:
#                             self.SetItemText(b, n, col)
#                         col += 1
#                 elif f == "EnsSpe":
#                     d = dict([l.split("-") for l in dic[k][0].nivTaxo[i]])
#                     for es in ref.listeEnsSpecif:
#                         if es in d.keys():
#                             self.SetItemText(b, d[es], col)
#                         col += 1
                        
                        
            if type(dic[k][0].sousSav) == dict:
                self.Construire(b, dic[k][1], et, niveau = niveau+1)#, pair = pair)       
            
            self.items[k] = b
            
            if et or niveau == 4:
                self.SetItemItalic(b, True)
            
            if niveau == 0:
                self.SetItemBold(b, True)
    
#             if pair[0]:
#                 self.SetItemBackgroundColour(b, wx.Colour(0xDDDDDD))#wx.LIGHT_GREY))
#             pair[0] = not pair[0]
    
    
#     ####################################################################################
#     def Construire2(self, branche, dic, et = False, niveau = 0):
#         """ Construction d'une branche de "savoirs"
#             <et> = prérequis ETT pour spécialité STI2D ?? plus utilisé ??
#             
#             fonction récursive
#         """
#         if dic == None:
#             return
# #         print(" "*niveau, "Construire", dic)
# 
#         
#         clefs = constantes.trier(list(dic.keys()))
#         sep = "\n" + CHAR_POINT + " "
#         
#         for k in clefs:
#             if type(dic[k].sousSav) == list:
#                 if self.filtre is not None:
#                     lstPoints = [ss.intitule for i, ss in enumerate(dic[k].sousSav) if k+'.'+str(i) in self.filtre]
#                 else:
#                     lstPoints = [ss.intitule for i, ss in enumerate(dic[k].sousSav)]
#                 toolTip = CHAR_POINT + " " + sep.join(lstPoints)
#             else:
#                 lstPoints = None
#                 toolTip = None
#                 
# #             if lstPoints is None or len(lstPoints) > 0:
#             b = None
#             if type(dic[k].sousSav) == dict:
#                 b = self.AppendItem(branche, k+" "+dic[k].intitule, ct_type=0, data = toolTip)
#                 self.Construire(b, dic[k].sousSav, et, niveau = niveau+1)       
#         
#             else:
#                 if self.filtre is None or k in self.filtre:
#                     b = self.AppendItem(branche, k+" "+dic[k].intitule, ct_type=1, data = toolTip)
#                 
#             if b is not None:   
#                 if et:
#                     self.SetItemItalic(b, True)
#                 if niveau == 0:
#                     self.SetItemBold(b, True)

    
        
    ####################################################################################
    def OnItemCheck(self, event):
        event.Skip()
        
        self.uncheckParentsPasPleins(self.root)

        lstc, lstu = [], []
        self.getListItemCheckedUnchecked(self.root, lstc, lstu)

        self.pp.AjouterEnleverSavoirs(lstc, lstu, self.savoirsRef)
        
        self.Refresh()                
        wx.CallAfter(self.pp.SetSavoirs)
    
    
    ####################################################################################
    def getCode(self, item):
        return self.typ+self.GetItemText(item).split()[0]
    
    
    
    ####################################################################################
    def AjouterEnleverSavoirsItem(self, item, propag = True):

        code = self.getCode(item)#.split()[0]
#        print "AjouterEnleverCompetencesItem", code
        if code != None: # un seul indicateur séléctionné
            self.AjouterEnleverSavoirs([item], propag)

        else:       # une compétence complète séléctionnée
            self.AjouterEnleverSavoirs(item.GetChildren(), propag)

    ####################################################################################
    def AjouterEnleverSavoirs(self, lstitem, propag = True):
#        print "AjouterEnleverCompetences"
        for item in lstitem:
            code = self.getCode(item)#.split()[0]
            
#            print "  ", code, item.GetValue()
            if item.GetValue():
                self.pp.AjouterSavoir(code, propag)
            else:
                self.pp.EnleverSavoir(code, propag)
                
        
    ###################################################################################
    def getListItemCheckedUnchecked(self, branche, lstc, lstu):
        """ Rempli 2 listes :
             - une avec les codes des items cochés
             - une autre avec les codes des items décochés
             
            fonction récursive
        """
        for i in branche.GetChildren():
            if i.IsChecked() and not branche.IsChecked():
                lstc.append(self.getCode(i))
            else:
                lstu.append(self.getCode(i))
            self.getListItemCheckedUnchecked(i, lstc, lstu)
        
    
    ###################################################################################
    def uncheckParentsPasPleins(self, branche):
        """ Décoche les parents dont tous les enfants ne sont pas cochés
             
            fonction récursive
        """
        for i in branche.GetChildren():
            self.uncheckParentsPasPleins(i)
        if any([not i.IsChecked() for i in branche.GetChildren()]):
            branche.Check(False)
            
            
#     ###################################################################################
#     def getListItemChecked(self, root):
#         liste = []
#         complet = True
#         for i in root.GetChildren():
#             cliste, ccomplet = self.getListItemChecked(i)
#             if ccomplet:
#                 if i.IsChecked():
#                     liste.append(self.getCode(i))
#                 else:
#                     complet = False
#             else:
#                 liste.extend(cliste)
#                 complet = False
#               
#         return liste, complet
    
    
    ####################################################################################
    def OnGetToolTip(self, event):
        toolTip = event.GetItem().GetData()
#         print(event.GetPoint())
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
        for _ in range(nc):
            child, cookie = GetChild(parent, cookie)
            GetChild = self.GetNextChild
            yield child
            
            
    
    
    
    ####################################################################################
    def get_item_by_label(self, search_text, root_item):
        """
                source : https://stackoverflow.com/questions/6954242/wxpython-treectrl-how-can-i-get-a-tree-item-by-name
        """
#         print("get_item_by_label", search_text)
        item, cookie = self.GetFirstChild(root_item)
    
        while item != None and item.IsOk():
            text = self.GetItemText(item).replace("\n", "")
#             print("   ", text)
            if text.split(" ")[0] == search_text:
                return item
            if self.ItemHasChildren(item):
                return self.get_item_by_label(search_text, item)
#                 match = self.get_item_by_label(search_text, item)
#                 if match.IsOk():
#                     return match
            item, cookie = self.GetNextChild(root_item, cookie)
    
        return None




####################################################################################
####################################################################################
# 
# Arbre des compétences
#
####################################################################################
    
class ArbreCompetences(HTL.HyperTreeList):
    def __init__(self, parent, typ, compFiltre, competencesRef, lstCases = None,
                 pp = None, agwStyle = 0):#|CT.TR_AUTO_CHECK_CHILD):#|HTL.TR_NO_HEADER):
        """    
            :parent: 
            :typ:
            :compFiltre: dictionnaire des compétences à afficher dans l'abre (sortie de GetDicFiltre())
            :competencesRef: type referentiel.Competences (ou referentiel.Fonctions)
            :pp: PanelPropriete contenant les méthodes AjouterEnlever...
        """
        HTL.HyperTreeList.__init__(self, parent, -1, style = wx.WANTS_CHARS,
                                   agwStyle = CT.TR_HIDE_ROOT|CT.TR_AUTO_CHECK_CHILD|wx.TR_HAS_BUTTONS|\
                                   CT.TR_AUTO_CHECK_PARENT|CT.TR_HAS_VARIABLE_ROW_HEIGHT|agwStyle)#wx.TR_DEFAULT_STYLE|
        
        self.parent = parent
#         print "ArbreCompetences", pptache
        if pp == None:
            self.pp = parent
        else:
            self.pp = pp
        
        self.typ = typ
        self.competencesRef = competencesRef # Objet Referentiel.Competences
        self.lstCases = lstCases
        
#         if dicCompetences is None:
#             dicCompetences = competencesRef.dicCompetences
        self.compFiltre = compFiltre
        
        self.items = {}
      
        self.AddColumn(competencesRef.nomDiscipline)
        self.SetMainColumn(0) # the one with the tree in it...
        self.CreerColonnes() # Pour projet uniquement
        
        # Séance ==> colonne pour Indicateurs
        if isinstance(self.pp, PanelPropriete_Seance) \
          and isinstance(competencesRef, Referentiel.Competences):
            self.AddColumn(competencesRef._nomIndic.Plur_())
            self.Bind(wx.EVT_TEXT, self.OnTextIndic)
        
        self.root = self.AddRoot(competencesRef.nomDiscipline)
        self.MiseAJourTypeEnseignement(self.compFiltre)
        
#         self.ExpandAll()
        
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
#        print self.HitTest((event.x, event.y))
        
    ######################################################################################################
    def OnEnter(self, event):
#         print "OnEnter ArbreCompetences"
        self.SetFocus()
        event.Skip()
        
    #############################################################################
    def MiseAJourTypeEnseignement(self, dicCompetences):
#        print "MiseAJourTypeEnseignement"
        self.DeleteChildren(self.root)
        for i in list(self.items.values()):
            for wnd in i._wnd:
                if wnd:
                    wnd.Hide()
                    wnd.Destroy()

        self.items = {}
        
        # Dictionnaire filtré :
#         dic_f = self.GetDicFiltre(dicCompetences)
#         print("filtre Cmp", self.filtre)
#         print("  dic_f", dic_f)
        self.Construire(self.root, dic = dicCompetences)

        self.ExpandAll()
    
        
    #############################################################################
    def MiseAJourPhase(self, phase):
        self.DeleteChildren(self.root)
        self.Construire(self.root, self.compFiltre)
        self.ExpandAll()
    
    
    
    ####################################################################################
    def Construire(self, branche, dic, et = False, niveau = 0):
        """ Constuction de la structure de l'arbre
            à partir de la branche <branche>
                ! Fonction récursive !
                
            :branche: wx.TreeItemId
            :dic: 
            :ct_type: 0 = normal, 1 = check, 2 = radio
        """
#         print(" "*niveau,"Construire", self.lstCases)
#         if dic == None:
#             dic = self.competences.dicCompetences

#         # On ajoute les sous éléments des compétences "cochables"
#         lstCases_ss = []
#         for code in self.lstCases:
#             lstCases_ss.extend(ref.getSousElem(code[1:], "Comp_"+code[0]))
        
        
        clefs = constantes.trier(list(dic.keys()))
        for k in clefs:
#             print("  "+" "*niveau, dic[k])
            if dic[k][1] is None or len(dic[k][1]) > 1: # Feuille ou noeud avec plusieurs fils
                if self.lstCases is None or self.typ+k in self.lstCases:
                    ct_type = 1
                else:
                    ct_type = 0
            else:
                ct_type = 0
            b = self.AppendItem(branche, k+" "+dic[k][0].intitule, ct_type = ct_type, data = k)
            
            # Séance ==> Indicateurs
#             if isinstance(self.pp, PanelPropriete_Seance):
#                 wnd = ExpandoTextCtrl(self.GetMainWindow())
#                 wnd.Hide()
#                 self.SetItemWindow(b, wnd, 1)
#                 self.Bind(wx.EVT_TEXT, self.OnTextIndic)
            
            if dic[k][1] is not None:
                self.Construire(b, dic[k][1], niveau = niveau+1)
            
            self.items[k] = b
                
            if niveau == 0: # On est à la racine
                self.SetItemBold(b, True)
    
#     ####################################################################################
#     def Construire2(self, branche, dic = None, niveau = 0):
#         """ Constuction de la structure de l'arbre
#             à partir de la branche <branche>
#                 ! Fonction récursive !
#                 
#             :branche: wx.TreeItemId
#             :dic: 
#             :ct_type: 0 = normal, 1 = check, 2 = radio
#         """
# #         print(" "*niveau,"Construire", self.filtre)
#         if dic == None:
#             dic = self.competences.dicCompetences
# 
#         clefs = constantes.trier(list(dic.keys()))
#         for k in clefs:
#             b = None
# #             print(" "*niveau,k,  dic[k].sousComp)
#             if len(dic[k].sousComp) > 0:
#                 b = self.AppendItem(branche, k+" "+dic[k].intitule, ct_type = 0, data = k)
#                 self.Construire(b, dic[k].sousComp, niveau = niveau+1)
#             else:
#                 if self.filtre is None or k in self.filtre:
# #                     print(" "*niveau,"+++", k)
#                     b = self.AppendItem(branche, k+" "+dic[k].intitule, ct_type = 1, data = k)
#             
#             if b is not None:
#                 self.items[k] = b
#                 
#                 if niveau == 0: # On est à la racine
#                     self.SetItemBold(b, True)
            

                
    ####################################################################################
    def SetItemType(self, item, newType):
        # CustomTreeCtrl doesn't support changing the item type on the fly,
        # so we create a new item and delete the old one. We currently only
        # keep the item text, would be nicer to also retain other attributes.
        text = self.GetItemText(item)
        newItem = self.InsertItem(self.GetItemParent(item), item, text, 
                                  ct_type=newType)
        self.Delete(item)
        return newItem
    
    
    ####################################################################################
    def OnTextIndic(self, event):
#         print("OnTextIndic")
        event.Skip()
        wx.CallAfter(self.pp.SetIndicateurs)
        
    ####################################################################################
    def OnItemCheck(self, event):
#         print("OnItemCheck")
        event.Skip()
        
        self.uncheckParentsPasPleins(self.root)

        lstc, lstu = [], []
        self.getListItemCheckedUnchecked(self.root, lstc, lstu)
        self.pp.AjouterEnleverCompetences(lstc, lstu, self.competencesRef)
        
        self.gererAffichageTxtCtrl()
#         lstc, lstu = [], []
#         self.getListItemCheckedUnchecked2(self.root, lstc, lstu)
#         for i in lstc:
#             self.GetItemWindow(i).Show(True)
#         for i in lstu:
#             self.GetItemWindow(i).Show(False)
            
            
        self.Refresh()                
        wx.CallAfter(self.pp.SetCompetences)


    ####################################################################################
    def getCode(self, item):
        return self.typ + self.GetItemPyData(item)


    ####################################################################################
    def AjouterEnleverCompetencesItem(self, item, propag = True):

        code = self.getCode(item)#.split()[0]
#        print "AjouterEnleverCompetencesItem", code
        if code != None: # un seul indicateur séléctionné
            self.AjouterEnleverCompetences([item], propag)

        else:       # une compétence complète séléctionnée
            self.AjouterEnleverCompetences(item.GetChildren(), propag)


    ####################################################################################
    def AjouterEnleverCompetences(self, lstitem, propag = True):
#        print "AjouterEnleverCompetences"
        for item in lstitem:
            code = self.getCode(item)#.split()[0]
            
#            print "  ", code, item.GetValue()
            if item.GetValue():
                self.pp.AjouterCompetence(code, propag)
            else:
                self.pp.EnleverCompetence(code, propag)
                
                
    ####################################################################################
    def AjouterEnleverCompetencesEleve(self, lstitem, eleve):
#        print "AjouterEnleverCompetencesEleve", self, lstitem, eleve
        for item in lstitem:
            code = self.GetItemPyData(item)
            if self.GetItemWindow(item, self.colEleves).EstCocheEleve(eleve):
                self.pp.AjouterCompetenceEleve(self.typ+code, eleve)
            else:
                self.pp.EnleverCompetenceEleve(self.typ+code, eleve)
    
    
    ###################################################################################
    def getListItemCheckedUnchecked(self, branche, lstc, lstu):
        """ Rempli 2 listes :
             - une avec les codes des items cochés
             - une autre avec les codes des items décochés
             
            fonction récursive
        """
        for i in branche.GetChildren():
            if i.IsChecked() and not branche.IsChecked():
                lstc.append(self.getCode(i))
            else:
                lstu.append(self.getCode(i))
            self.getListItemCheckedUnchecked(i, lstc, lstu)
        
    
    ###################################################################################
    def getListItemCheckedUnchecked2(self, branche, lstc, lstu):
        """ Rempli 2 listes :
             - une avec les  items cochés
             - une autre avec les items décochés
             
            fonction récursive
        """
        for i in branche.GetChildren():
            if i.IsChecked():# and not branche.IsChecked():
                lstc.append(i)
            else:
                lstu.append(i)
            self.getListItemCheckedUnchecked2(i, lstc, lstu)
            
    
    ###################################################################################
    def gererAffichageTxtCtrl(self):
        if isinstance(self.pp, PanelPropriete_Seance):
            lstc, lstu = [], []
            self.getListItemCheckedUnchecked2(self.root, lstc, lstu)
            
            for i in lstc:
                if self.GetItemWindow(i, 1) is None:
                    wnd = ExpandoTextCtrl(self.GetMainWindow())
                    self.SetItemWindow(i, wnd, 1)
            
            
                          
            for i in lstu:
                i.DeleteWindow(1)
#                 wnd = self.GetItemWindow(i, 1)
#                 self.SetItemWindow(i, None, 1)
#                 wnd.Destroy()
#                 self.DeleteItemWindow(i, 1)
        
    ###################################################################################
    def MiseAJour(self, typ, seance):
#         if isinstance(seance, pysequence.Seance):
        for cmp, item in self.items.items():
            wnd = self.GetItemWindow(item, 1)
            if wnd is not None and typ+cmp in seance.indicateurs:
                self.setIndicateur(item, seance.indicateurs[typ+cmp])
        
#         else:
#             for cmp, item in self.items.items():
#                 wnd = self.GetItemWindow(item, 1)
#                 if wnd is not None and typ+cmp in seance.compVisees:
#                     self.setIndicateur(item, True)            
#     
    
    ###################################################################################
    def setIndicateur(self, item, indic):
#         print("setIndicateur", indic)
        wnd = self.GetItemWindow(item, 1)
        if wnd is not None:
            wnd.SetValue(indic)
        
        
    ###################################################################################
    def getDictIndicateurs(self):
        lstc, lstu = [], []
        self.getListItemCheckedUnchecked2(self.root, lstc, lstu)
        d = {}
        for i in lstc:
            d[self.getCode(i)] = self.GetItemWindow(i, 1).GetValue()
        return d
    
    
    ###################################################################################
    def uncheckParentsPasPleins(self, branche):
        """ Décoche les parents dont tous les enfants ne sont pas cochés
             
            fonction récursive
        """
        for i in branche.GetChildren():
            self.uncheckParentsPasPleins(i)
        if any([not i.IsChecked() for i in branche.GetChildren()]):
            branche.Check(False)
            
            
    
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
        for _ in range(nc):
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


    ####################################################################################
    def OnSize2(self, evt = None):
#        print "OnSize2"
        ww = 0
        for c in range(1, self.GetColumnCount()):
            ww += self.GetColumnWidth(c)
        w = self.GetClientSize()[0] - ww - 20*SSCALE # + un petit peu (20 par expérience) pour la barre de défilement
        if w != self.GetColumnWidth(0):
            self.SetColumnWidth(0, w)
            if self.IsShown():
                self.wrap(w)
        
        if evt is not None:
            evt.Skip()


    ####################################################################################
    def wrap(self,w):
        item = self.GetRootItem()
#         font = wx.ClientDC(self).GetFont()
        if item != None:
            dc = wx.ClientDC(self)
            while 1: # On parcoure toutes les lignes de l'arbre
                item = self.GetNext(item)
                if item == None:
                    break
                 
                # Coefficient pour le texte en gras (plus large)
                # Et position en X du texte
                if item._type == 0:
                    W = w*0.93 - 5*SSCALE
                else:
                    W = w - 35*SSCALE # 35 correspond au décallage des "enfants" (cases à cocher)
                
                text = self.GetItemText(item, 0).replace("\n", "")
#                 try:
#                     f = self.GetItemFont(item)#.GetPixelSize()
#                     print dc.GetFullTextExtent("text", f)
#                     print f.GetPixelSize()
#                 except:
#                     pass
#                 wx.ClientDC(self).SetFont(f)
                text = wordwrap(text, W*0.9, dc) # Je ne comprends pas mais il faut ce 0.9 ...
             
                self.SetItemText(item, text, 0)
#         wx.ClientDC(self).SetFont(font)
    
    
    ####################################################################################
    def CreerColonnes(self):
        pass

    

class ArbreCompetencesPrj(ArbreCompetences):
    """ Arbre des compétences abordées en projet lors d'une tâche <pptache>
        <revue> : vrai si la tâche est une revue
        <eleves> : vrai s'il faut afficher une colonne supplémentaire 
                    pour distinguer les compétences pour chaque éleve
    """
    def __init__(self, parent, typ, dicComp, compRef,  pptache, revue = False, eleves = False, 
                 agwStyle = CT.TR_HIDE_ROOT|CT.TR_HAS_VARIABLE_ROW_HEIGHT|\
                            CT.TR_ROW_LINES|CT.TR_ALIGN_WINDOWS| \
                            CT.TR_AUTO_CHECK_PARENT|CT.TR_AUTO_TOGGLE_CHILD):
        self.revue = revue#|CT.TR_AUTO_CHECK_CHILD|\
        self.eleves = eleves
        self.typ = typ
        
        if pptache == None:
            self.pptache = parent
        else:
            self.pptache = pptache
            
#         print "ArbreCompetencesPrj", pptache
        
        ArbreCompetences.__init__(self, parent, typ, dicComp, compRef, 
                                  pp = pptache, agwStyle = agwStyle)#|CT.TR_ELLIPSIZE_LONG_ITEMS)#|CT.TR_TOOLTIP_ON_LONG_ITEMS)#
#         print self.pptache
#         """    
#             :parent: 
#             :typ:
#             :compFiltre: dictionnaire des compétences à afficher dans l'abre (sortie de GetDicFiltre())
#             :compRef: type referentiel.Competences
#             :pp: PanelPropriete contenant les méthodes AjouterEnlever...
#         """
        
        self.Bind(wx.EVT_SIZE, self.OnSize2)
        self.Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        
        self.SetColumnText(0, "%s et %s" %(compRef._nom.Plur_(),compRef._nomIndic.Plur_()))
        
        
        tache = self.GetTache()
        prj = tache.GetProjetRef()
        if prj is not None:
            i=0
            for i, part in enumerate(prj.parties.keys()):
                self.SetColumnText(i+1, "Poids "+part)
                self.SetColumnWidth(i+1, 60*SSCALE)
            
            if eleves and i>0:
                self.SetColumnWidth(i+2, 0)
        
        
    ####################################################################################
    def GetTache(self):
#         print "GetTache", self.pptache
        return self.pptache.tache  
        
#        self.Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
    
    
    ####################################################################################
    def CreerColonnes(self):
        tache = self.GetTache()
        prj = tache.GetProjetRef()
        if prj is not None:
            for i in range(len(prj.parties.keys())):
                self.AddColumn("")
                self.SetColumnWidth(i+1, 0)
            
            self.colEleves = len(prj.parties.keys())+1
            self.AddColumn(tache.GetReferentiel().getLabel("ELEVES").plur_())#(u"Eleves")
            self.SetColumnWidth(self.colEleves, 0)
        
        
    ####################################################################################
    def ConstruireCasesEleve(self):
        """ Ajout des cases "ChoixCompetenceEleve"
        """
        
        tache = self.GetTache()
#        print "   ConstruireCasesEleve", tache.phase, self.items
        cases = None
        affcol = None
        for codeIndic, item in list(self.items.items()):
            cases = self.GetItemWindow(item, self.colEleves)
            if isinstance(cases, ChoixCompetenceEleve):
                item.DeleteWindow(self.colEleves)
                cases = ChoixCompetenceEleve(self.GetMainWindow(), self.typ+codeIndic,
                                             tache.projet, tache, self.MiseAJourCaseEleve)
                item.SetWindow(cases, self.colEleves)
                affcol = cases
        
        if affcol is not None:
            self.SetColumnWidth(self.colEleves, max(60*SSCALE, affcol.GetSize()[0]))
        self.Layout()
        self.OnSize2()
        
            
    ####################################################################################
    def ReConstruire(self):
#        print "ReConstruire"
        self.DeleteChildren(self.root)
        self.Construire()
        self.ConstruireCasesEleve()
        self.ExpandAll()
        self.OnSize2()


    ####################################################################################
    def Construire(self, branche = None, dic = None):
        print("Construire compétences prj", self.GetTache().intitule, self.eleves)
#        if competences == None:
#            competences = self.competences
        
        if branche == None:
            branche  = self.root
        
        tache = self.GetTache()
        prj = tache.GetProjetRef()
        if prj is None:
            return 
        
#        print " prj", prj, self.typ
        if dic is None: # Construction de la racine
#            dic = self.competences.dicCompetences
#             dic = tache.GetReferentiel().dicCompetences
            dic = self.compFiltre
#         print("dic", dic, self.compFiltre)
        
#        print "   ProjetRef", prj
#         print("  dicCompetences", dic)
#        if tache.estPredeterminee(): print prj.taches[tache.intitule][2]
        
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False)
        
#        size = None
        if self.eleves:
            tousEleve = [True]*len(tache.projet.eleves)
        
        def const(d, br, debug = False, niveau = 0):
#             print(" "*niveau, d)
            ks = list(d.keys())
            ks.sort()
            for k in ks:
                
#                 v = d[k]
                competence = d[k] # type Referentiel.Competence
                if debug: print("*"*niveau, k, competence.sousComp)
                
#                print "****", k#, prj.taches[tache.intitule][2]

                #
                # Groupe de compétences
                #
                if competence.sousComp != {}:
#                 if len(v) > 1 and type(v[1]) == dict:
                    
                    if debug: print("   "+" "*niveau, competence.intitule)
                    
                    if competence.poids == {}: # Compétence 
#                     if len(v) == 2: # Compétence 
                        if not tache.estPredeterminee() or k in prj.taches[tache.intitule][2]:
                            b = self.AppendItem(br, k+" "+competence.intitule,
                                                data = k)
                        else:
                            b = None
                    
                    else:   # Groupe de compétences - avec poids 
                        if debug: print("   prem's"+" "*niveau, competence.poids)
                        b = self.AppendItem(br, k+" "+competence.intitule,
                                                data = k)
#                        print " * ",v[2]
                        
                        for i, part in enumerate(prj.parties.keys()):
                            if part in competence.poids:
                                self.SetItemText(b, pourCent2(0.01*competence.poids[part]), i+1)
                        
#                        for i, p in enumerate(v[2][1:]):
#                            if p != 0:
#                                self.SetItemText(b, pourCent2(0.01*p), i+1)
                        self.SetItemBold(b, True)
                    
                    if b is not None:
                        self.items[k] = b
                        const(competence.sousComp, b, debug = debug, niveau = niveau+1)
                        
                #
                # Compétence avec indicateur(s)
                #
                else:
                    b = None #
                    tous = True
                    
                    if not tache.estPredeterminee() \
                       or (tache.intitule in prj.taches and k in prj.taches[tache.intitule][2]):
                        print("  ",competence.intitule[:10])
                        cc = [cd+ " " + it for cd, it in zip(k.split("\n"), competence.intitule.split("\n"))]
                        comp = self.AppendItem(br, "\n ".join(cc),
                                                data = k)
                        
                        #
                        # Compétence "racine" - avec poids
                        #
                        if competence.poids != {}: # 
#                         if len(v) == 3: # 
                            if debug: print("   prem'S", competence.poids)
                            for j, part in enumerate(prj.parties.keys()):
                                if part in competence.poids:
    #                        for i, p in enumerate(v[2][1:]):
    #                            if p != 0:
                                    self.SetItemText(comp, pourCent2(0.01*competence.poids[part]), j+1)
                            self.SetItemBold(comp, True)
                                    
    #                    comp = self.AppendItem(br, k+" "+v[0])
                        
                        self.items[k] = comp
                        
                        #
                        # Ajout des indicateurs
                        #
                        for i, indic in enumerate(competence.indicateurs):
                            codeIndic = str(k+'_'+str(i+1))
                            print("      ", codeIndic)
                            if debug:
    #                            print not tache.phase in [_R1, "Rev", tache.projet.getCodeLastRevue()]
    #                            print codeIndic , indic.revue,
                                if hasattr(tache, 'indicateursMaxiEleve'):
                                    print("  ", tache.indicateursMaxiEleve[0])
                                print("  ", prj.getTypeIndicateur(self.typ+codeIndic))
                            
                            if tache == None:
                                b = self.AppendItem(comp, indic.intitule, 
                                                    data = codeIndic)
                                for j, part in enumerate(prj.parties.keys()):
                                    if part in competence.poids:
    #                            for j, p in enumerate(indic.poids[1:]):
    #                                if p != 0:
                                        if j == 0:  coul = 'C'
                                        else:       coul = 'S'
                                self.SetItemTextColour(b, wx.Colour(COUL_PARTIE[coul]))
                                self.SetItemFont(b, font)
                            
                            if tache != None and tache.estACocherIndic(self.typ+codeIndic):
#                             if tache != None and ((not tache.phase in [_R1,_R2, _Rev, tache.projet.getCodeLastRevue()]) \
#                                                   or (self.typ+codeIndic in tache.indicateursMaxiEleve[0])) \
#                                              and (prj.getTypeIndicateur(self.typ+codeIndic) == "S" or tache.phase != 'XXX'):#and (indic.revue[self.typ] == 0 or indic.revue[self.typ] >= tache.GetProchaineRevue()) \ # à revoir !!
                                
                                b = self.AppendItem(comp, indic.intitule, ct_type=1, 
                                                    data = codeIndic) # Avec case à cocher
                                
#                                 if codeIndic in tache.indicateursEleve[0]:
#                                     self.MiseAJourCheckbox(b)
#                                 else:
                                if not codeIndic in tache.indicateursEleve[0]:
                                    tous = False
                                
                                if indic.getRevue() == tache.phase:
                                    self.MiseAJourCheckbox(b)
                                    
                                if debug: print("   indic", indic)
                                
                                for j, part in enumerate(prj.parties.keys()):
                                    if part in indic.poids:
    #                            for j, p in enumerate(indic.poids[1:]):
    #                                if p != 0:
                                        self.SetItemText(b, pourCent2(0.01*indic.poids[part]), j+1)
                                        self.SetItemTextColour(b, getCoulPartie(part))
                                       
                                self.SetItemFont(b, font)        
                                
                                self.items[codeIndic] = b
                                
                                if self.eleves:
    #                                print "   ", tache.projet.eleves,
                                    cases = ChoixCompetenceEleve(self.GetMainWindow(), self.typ+codeIndic, 
                                                                               tache.projet, 
                                                                               tache, self.MiseAJourCaseEleve)
#                                    cases = ChoixCompetenceEleve(self, codeIndic, 
#                                                                               tache.projet, 
#                                                                               tache)
    
    #                                cases.SetSize(cases.GetBestSize())
                                    self.SetItemWindow(b, cases, self.colEleves)
                                    self.SetItem3State(b, True)
                                    
                                    for e in range(len(tache.projet.eleves)):
                                        tousEleve[e] = tousEleve[e] and self.GetItemWindow(b, self.colEleves).EstCocheEleve(e+1)
    #                                size = self.GetItemWindow(b, 3).GetSize()[0]
    #                                print cases.GetSize()
                                    b.SetWindowEnabled(True, self.colEleves)
#                                    print "  ...", cases.GetSize()[0]
                                    self.SetColumnWidth(self.colEleves, max(60, cases.GetSize()[0]))
    #                                self.Collapse(comp)
    #                                self.Refresh()
                                    self.Layout()
                                    
                        #
                        # Cas où il n'y a pas d'indicateurs dans ce type de projet
                        #
                        if prj._pasdIndic:
                            if debug: print("   pas d'indic !!")
                            for k, d in competence.sousComp.items():
                                b = self.AppendItem(comp, k+" "+competence.intitule, 
                                                    ct_type = 1,
                                                    data = k)
                    
                    if b == None: # Désactivation si branche vide d'indicateurs
                        pass#self.SetItemType(br,0)
                    else:
                        self.MiseAJourCheckbox(br, etat = tous)
#                        if self.eleves:
#                            self.SetItemWindow(c, ChoixCompetenceEleve(self, code, self.pptache.tache.projet, self.pptache.tache), 2)
#                            for e in range(len(self.pptache.tache.projet.eleves)):
#                                self.GetItemWindow(c, 2).CocherEleve(e+1, tousEleve[e])
            return

        # Démarrage de la récursion
        const(dic, branche, debug = False)
        
#        self.ConstruireCasesEleve()
        
#        if self.eleves:
#            print "***"
#            self.SetColumnWidth(3, 10)
        
        if tache == None: # Cas des arbres dans popup (que l'arbre, pas de poids)
            for i in range(self.colEleves):
                self.SetColumnWidth(i+1, 0)
        
        self.Refresh()


    ###################################################################################
    def OnItemCheck(self, event, item = None):
#         print("OnItemCheck")
        if event != None:
            item = event.GetItem()
            event.Skip()
        
#         cases = self.GetItemWindow(item, self.colEleves)
#         print("   ", cases)
        if self.IsItem3State(item):
            etat = self.GetItem3StateValue(item)
            if etat == wx.CHK_UNDETERMINED:
                etat = wx.CHK_UNCHECKED
            self.MiseAJourCheckbox(item, etat = etat)        
        
        self.AjouterEnleverCompetencesItem(item)
        
        cases = self.GetItemWindow(item, self.colEleves)
        if cases is not None:
            cases.Actualiser()
        

        
        wx.CallAfter(self.pp.SetCompetences)
        
    
    #############################################################################
    def GetCasesEleves(self, codeIndic):
        if codeIndic in self.items:
            return self.GetItemWindow(self.items[codeIndic], self.colEleves)
    
    #############################################################################
    def MiseAJourCheckbox(self, item, casesEleves = None, etat = True):
#         print("MiseAJourCheckbox", casesEleves, etat)
        if self.IsItem3State(item):
#             print("   3states")
            if casesEleves:
                if casesEleves.EstToutCoche():
                    self.SetItem3StateValue(item, wx.CHK_CHECKED)
                elif casesEleves.EstToutDecoche():
                    self.SetItem3StateValue(item, wx.CHK_UNCHECKED)
                else:
                    self.SetItem3StateValue(item, wx.CHK_UNDETERMINED)
            elif etat in [wx.CHK_CHECKED, wx.CHK_UNCHECKED, wx.CHK_UNDETERMINED]:
                self.SetItem3StateValue(item, etat)
        else:
            if casesEleves: # Normalement, ça n'arrive pas
                self.CheckItem2(item, casesEleves.EstToutCoche(), torefresh=True)
            else:
                self.CheckItem2(item, etat, torefresh=True)
        
        self.Refresh()
    
    
    #############################################################################
    def MiseAJourCasesEleve(self, codeIndic, cases):
        cases.MiseAJour()
        
        
    #############################################################################
    def MiseAJourCaseEleve(self, codeIndic, etat, eleve, propag = True):
        """ Mise à jour
        """
#         print("MiseAJourCaseEleve", codeIndic, etat, eleve, propag)
        casesEleves = self.GetCasesEleves(codeIndic[1:])
        if casesEleves.EstCocheEleve(eleve) != etat:
            return
        
        comp = codeIndic.split("_")[0]
        
        if comp != codeIndic: # Indicateur seul
            item = self.items[codeIndic[1:]]
            itemComp = self.items[comp[1:]]
#            print "  itemComp =", itemComp
            if propag:
                tout = True
                for i in itemComp.GetChildren():
                    tout = tout and self.GetItemWindow(i, self.colEleves).EstCocheEleve(eleve)
    #            self.GetItemWindow(itemComp, 2).CocherEleve(eleve, tout)
#                print "MiseAJourCaseEleve", comp, eleve
                cases = self.GetCasesEleves(comp[1:])
                if cases != None:
                    cases.CocherEleve(eleve, tout, withEvent = True)
            
#            self.MiseAJourCaseEleve(comp, tout, eleve, forcer = True)
            
            self.AjouterEnleverCompetencesEleve([item], eleve)
            
            self.MiseAJourCheckbox(item, casesEleves)
            
#            self.AjouterEnleverCompetencesItem(item, propag = False)
            
        else: #Compétence complete (avec plusieurs indicateurs)
            if propag:
                itemComp = self.items[comp[1:]]
                for i in itemComp.GetChildren():
    #                self.GetItemWindow(i, 2).CocherEleve(eleve, etat)
    #                self.MiseAJourCaseEleve(self.GetItemPyData(i), etat, eleve, forcer = True)
                    cases = self.GetItemWindow(i, self.colEleves)
                    cases.CocherEleve(eleve, etat, withEvent = True)
#            self.CheckItem2(itemComp, estToutCoche)
#            self.AjouterEnleverCompetencesEleve(itemComp.GetChildren(), eleve)
#            self.AjouterEnleverCompetencesItem(itemComp, propag = False)
        
        if propag:
            self.pptache.SetCompetences()
        
        
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
    def __init__(self, parent, typ, competences, pptache, 
                 agwStyle = CT.TR_HIDE_ROOT|CT.TR_HAS_VARIABLE_ROW_HEIGHT|\
                            CT.TR_ROW_LINES|CT.TR_ALIGN_WINDOWS|CT.TR_AUTO_CHECK_CHILD|\
                            CT.TR_AUTO_CHECK_PARENT|CT.TR_AUTO_TOGGLE_CHILD):

        
        ArbreCompetences.__init__(self, parent, typ, None, competences, pp = pptache,
                                  agwStyle = agwStyle)#|CT.TR_ELLIPSIZE_LONG_ITEMS)#|CT.TR_TOOLTIP_ON_LONG_ITEMS)#
        
        
#         ArbreCompetences.__init__(self, parent, ref, pptache,
#                                   agwStyle = agwStyle)#|CT.TR_ELLIPSIZE_LONG_ITEMS)#|CT.TR_TOOLTIP_ON_LONG_ITEMS)#
        self.Bind(wx.EVT_SIZE, self.OnSize2)
        self.Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        ref = parent.GetDocument().GetReferentiel()
        self.SetColumnText(0, competences._nom.Plur_() + " et " + ref._nomTaches.Plur_())
        
      


    ####################################################################################
    def Construire(self, branche = None, dic = None):
#        print "Construire fonctions",
        
#        prj = self.pptache.tache.GetProjetRef()
        
        if dic == None: # Construction de la racine
            dic = self.competencesRef.dicFonctions
        if branche == None:
            branche  = self.root
#        print dic
#        
#        print "   ", self.GetColumnCount()
#         for c in range(1, self.GetColumnCount()):
#             self.RemoveColumn(1)
#        print "  ", dic
#         for i, c in enumerate(sorted(ref.dicCompetences.keys())):
#             self.AddColumn("")
#             self.SetColumnText(i+1, c)
#             self.SetColumnAlignment(i+1, wx.ALIGN_CENTER)
#             self.SetColumnWidth(i+1, 30*SSCALE)
            
        
            
#        tache = self.pptache.tache
            
#        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False)
#        
#        size = None
        
        def const(d, br, debug = False):
            ks = list(d.keys())
            ks.sort()
            for k in ks:
                if debug: print("****", k)
                v = d[k]
                if len(v) > 1 and type(v[1]) == dict:
                    if debug: print("   ", v[0])
                    b = self.AppendItem(br, k+" "+v[0], data = k)
                    self.items[k] = b
                    const(v[1], b, debug = debug)
                        
                else:   # Extremité de branche
                    cc = [cd+ " " + it for cd, it in zip(k.split("\n"), v[0].split("\n"))]
                    comp = self.AppendItem(br, "\n ".join(cc), ct_type=1, data = k)
               
                    if debug: print("   prem's 2", v[1])
                    
                    
                    for c, p in enumerate(sorted(self.competencesRef.dicFonctions.keys())):
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
#         print("OnItemCheck Fct")
        event.Skip()
        
        self.uncheckParentsPasPleins(self.root)

        lstc, lstu = [], []
        self.getListItemCheckedUnchecked(self.root, lstc, lstu)
        self.pp.AjouterEnleverCompetences(lstc, lstu, self.competencesRef)
        
        self.Refresh()                
        wx.CallAfter(self.pp.SetCompetences)








class ArbreCompetencesPopup(CT.CustomTreeCtrl):
    """ Arbre des compétences abordées en projet lors d'une tâche <pptache>
        <revue> : vrai si la tâche est une revue
        <eleves> : vrai s'il faut afficher une colonne supplémentaire pour distinguer les compétences pour chaque éleve
    """
    def __init__(self, parent):
          
        CT.CustomTreeCtrl.__init__(self, parent, -1,
                                   agwStyle = CT.TR_HAS_VARIABLE_ROW_HEIGHT|CT.TR_HIDE_ROOT|CT.TR_NO_LINES)
#        self.SetQuickBestSize(False)
        self.root = self.AddRoot("")

    ####################################################################################
    def Construire(self, dic , dicIndicateurs, prj):
#        print "Construire", dic
#        print dicIndicateurs
        branche  = self.root
        
        debug = False
            
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False)
        
        def const(d, br, debug = False):
            ks = list(d.keys())
            ks.sort()
            for k in ks:
                if debug: print("****", k)
                v = d[k]
                if len(v) > 1 and type(v[1]) == dict:
                    if debug: print("   ", v[0])
                    if len(v) == 2:
                        b = self.AppendItem(br, textwrap.fill(k+" "+v[0], 50))
                    else:
                        if debug: print("   prem's", v[2])
                        b = self.AppendItem(br, textwrap.fill(k+" "+v[0], 50))
                        self.SetItemBold(b, True)

                    const(v[1], b, debug = debug)
                        
                else:   # Indicateur
                    cc = [cd+ " " + it for cd, it in zip(k.split("\n"), v[0].split("\n"))] 
                    comp = self.AppendItem(br, textwrap.fill("\n ".join(cc), 50))
                    if k in list(dicIndicateurs.keys()):
                        ajouteIndic(comp, v[1], dicIndicateurs[k])
                    else:
                        ajouteIndic(comp, v[1], None)
            return
        
        def ajouteIndic(branche, listIndic, listIndicUtil):
            for i, indic in enumerate(listIndic):
                b = self.AppendItem(branche, textwrap.fill(indic.intitule, 50))
                for part in list(prj.parties.keys()):
                    if part in list(indic.poids.keys()):
#                for j, p in enumerate(indic.poids[1:]):
#                    if p != 0:
#                        print listIndic
#                        print comp, dicIndicateurs[comp]
                        if listIndicUtil == None or not listIndicUtil[i]:
                            self.SetItemTextColour(b, COUL_ABS)
                        else:
                            self.SetItemTextColour(b, getCoulPartie(part))
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
        self.SetMinSize((ms[0]+5*SSCALE, ms[1]+16*SSCALE))


    def GetMaxSize2(self, item, level = 2, maxwidth=0, lastheight = 0):
        dc = wx.ScreenDC()
#        dc.SetFont(self.GetItemFont())
        
        child, cookie = self.GetFirstChild(item)
#        print " level",level
#        print " ",child, cookie
        while child != None and child.IsOk():
            dc.SetFont(self.GetItemFont(child))
#            print "  txt =",self.GetItemText(child)
            W, H, _ = dc.GetMultiLineTextExtent(self.GetItemText(child))
#            print "  W,H, lH =",W,H, lH, self.GetIndent()
            width = W + self.GetIndent()*level + 10*SSCALE
            maxwidth = max(maxwidth, width)
            lastheight += H + 6*SSCALE
            
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
            
####################################################################################
#
#   Classes définissant le panel de sélection du type d'enseignement
#
####################################################################################*
# from wx.lib.combotreebox import ComboTreeBox
class Panel_SelectEnseignement(wx.Panel):
    def __init__(self, parent, panelClasse, pourProjet, objet):
        wx.Panel.__init__(self, parent, -1)
        
        if isinstance(objet, pysequence.Classe):
            self.classe = objet
            self.groupe = None
        elif isinstance(objet, pysequence.Groupe):
            self.groupe = objet
            self.classe = None
            
        self.pourProjet = pourProjet
        
        self.panelClasse = panelClasse
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
#         self.st_type = wx.StaticText(self, -1, "")
        #
        # Type d'enseignement
        #
#         self.ctb_type = ComboTreeBox(self, wx.ID_ANY)
        self.ctb_type = myComboTreeBox(self, wx.ID_ANY)
        self.sizer.Add(self.ctb_type, 0, wx.GROW | wx.EXPAND| wx.ALL, 1)
        self.Construire()
        
        #
        # Spécialité
        # 
        self.rb_spe = wx.CheckListBox(self, -1, choices = [])
        self.rb_spe.SetLabel("Choisir une ou plusieurs spécialité(s)")
        self.sizer.Add(self.rb_spe, 0, wx.GROW | wx.EXPAND| wx.ALL, 1)
        self.rb_spe.Show(False)
        
        #
        # Périodes possibles
        #
        if self.classe is not None:
            self.bmp = wx.StaticBitmap(self, -1, wx.Bitmap())
            self.bmp.SetToolTip("Périodes attribuées à la spécialité")
            self.sizer.Add(self.bmp, wx.EXPAND| wx.ALL, 1)
        
        
        
        
        self.Bind(wx.EVT_COMBOBOX, self.EvtRadioBox)
#         self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, self.cb_type)
        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtRadioBoxSpe, self.rb_spe)
        
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.layout)
#         def_ref = REFERENTIELS[constantes.TYPE_ENSEIGNEMENT_DEFAUT]
        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnTreeTooltip)
#         wx.EVT_TREE_ITEM_GETTOOLTIP(self, -1, self.OnTreeTooltip)
        
        self.MiseAJour()
        self.sizer.Layout()
#         self.sp_type.SetLabel(def_ref.Enseignement[0])
#         self.cb_type.SetStringSelection(def_ref.Enseignement[0])
#         self.sp_type.Show(len(def_ref.listeSpecialites) > 0)


    ######################################################################################  
    def GetReferentiel(self):
        if self.classe is not None:
            return self.classe.referentiel
        if self.groupe is not None:
            return self.groupe.GetReferentiel()
            return REFERENTIELS[self.groupe.typeEnseignement]
    
    
    ######################################################################################  
    def GetDocument(self):
        if self.classe is not None:
            return self.classe.GetDocument()
        if self.groupe is not None:
            return self.groupe.GetDocument()
        
    
    ######################################################################################  
    def layout(self, event):
        self.sizer.Layout()
        event.Skip()
    
    
    ######################################################################################  
    def EvtRadioBoxSpe(self, event):
#         print("EvtRadioBoxSpe")
        if self.classe is not None:
            index = event.GetSelection()  
            spe = self.rb_spe.GetString(index)
            ref = self.classe.doc.GetReferentiel()
            per = ref.getPeriodeSpe([spe])
            exc = ref.getSpeHorsPeriode(per)
#             print("   ", exc, spe)
            for i in self.rb_spe.GetCheckedItems():
#                 print(i, self.rb_spe.GetString(i))
                if self.rb_spe.GetString(i) in exc:
                    self.rb_spe.Check(i, False)
            
            
            
            self.classe.specialite = list(self.rb_spe.GetCheckedStrings())
            self.classe.doc.MiseAJourTypeEnseignement()
#             print("  ", self.classe.doc.position)
            self.classe.doc.SetPosition(self.classe.doc.position)
#             print("  ", self.classe.doc.position)
            self.MiseAJour()
            self.sizer.Layout()
            
            self.panelClasse.sendEvent(modif = "Modification de la spécialité",
                                       draw = True, verif = True)
        
        if self.groupe is not None:
            self.groupe.specialite = list(self.rb_spe.GetCheckedStrings())
            
            
            
    ######################################################################################  
    def EvtRadioBox(self, event = None, CodeFam = None):
        """ Sélection d'un type d'enseignement
        """
#         print("EvtRadioBox")
        if event != None:
#             radio_selected = event.GetEventObject()
            CodeFam = Referentiel.getEnseignementLabel(event.GetString())
#         print("EvtRadioBox", CodeFam)
        if CodeFam is None:
            self.ctb_type.SetStringSelection(self.GetReferentiel().Enseignement[0])
            return
        
        if self.classe is not None:
            self.classe.typeEnseignement, self.classe.familleEnseignement = CodeFam
            self.classe.referentiel = REFERENTIELS[self.classe.typeEnseignement]
            if len(self.classe.referentiel.listeSpecialites) > 0:
                self.classe.specialite = [self.classe.referentiel.listeSpecialites[0]]
            else:
                self.classe.specialite = []
            
    #         self.classe.MiseAJourTypeEnseignement()
            self.classe.doc.MiseAJourTypeEnseignement()
            self.classe.doc.SetPosition(self.classe.doc.position)

            # Mise à jour du panel Classe
            self.panelClasse.MiseAJourTypeEnseignement()
        
        if self.groupe is not None:
            self.groupe.typeEnseignement = CodeFam[0]
            # Mise à jour du panel Groupe
            self.panelClasse.MiseAJour()
    
        # Gestion des affichages ...
        self.rb_spe.Show(len(self.GetReferentiel().listeSpecialites) > 0)
        self.MiseAJour()
        self.sizer.Layout()
        
        
    ######################################################################################  
    def Verrouiller(self):
        etat = not self.classe.verrouillee
        self.ctb_type.Enable(etat)
        self.rb_spe.Enable(etat)
        self.sizer.Layout()
#         self.spe.Show(etat)
#         self.arbre.Show(etat)
        
        
    ######################################################################################  
    def Construire(self):
        """ Construction de l'arbre
        """
#         print("Construire ArbreTypeEnseignement")
#         print ARBRE_REF
        self.branche = []
        self.Tooltips = {}
#        self.ExpandAll()
        for t, st in ARBRE_REF:
#            print "   ", t, st, self.panelParent.pourProjet
            
            if t[0] == "_" or (self.pourProjet and len(REFERENTIELS[t].projets) == 0):
                branche = self.ctb_type.Append(REFERENTIELS[st[0]].Enseignement[2], 
                                               clientData = REFERENTIELS[st[0]].Enseignement[3])
                self.Tooltips[REFERENTIELS[st[0]].Enseignement[2]] = REFERENTIELS[st[0]].Enseignement[2]
            else:
                branche = self.ctb_type.Append(REFERENTIELS[t].Enseignement[0])#, ct_type=2)#, image = self.arbre.images["Seq"])
                self.Tooltips[REFERENTIELS[t].Enseignement[0]] = REFERENTIELS[t].Enseignement[1]
#                 branche.SetTooltip(REFERENTIELS[t].Enseignement[1])
#                 rb = wx.RadioButton(self, -1, REFERENTIELS[t].Enseignement[0])
#                 self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, rb)
#                 self.SetItemWindow(branche, rb)
#                 rb.SetToolTip(REFERENTIELS[t].Enseignement[1])
#                 rb.Enable(len(REFERENTIELS[t].projets) > 0 or not self.pourProjet)
                self.branche.append(branche)
            for sst in st:
                sbranche = self.ctb_type.Append(REFERENTIELS[sst].Enseignement[0], branche)#, ct_type=2)
                self.Tooltips[REFERENTIELS[sst].Enseignement[0]] = REFERENTIELS[sst].Enseignement[1]
#                 print(dir(sbranche))
#                 sbranche.SetTooltip(REFERENTIELS[sst].Enseignement[1])
#                 rb = wx.RadioButton(self, -1, REFERENTIELS[sst].Enseignement[0])
#                 self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, rb)
#                 self.SetItemWindow(sbranche, rb)
#                 rb.SetToolTip(REFERENTIELS[sst].Enseignement[1])
#                 rb.Enable(len(REFERENTIELS[sst].projets) > 0 or not self.pourProjet)
                self.branche.append(sbranche)
#         print(self.Tooltips)
#         self.ExpandAll()
#         self.CollapseAll()

    ######################################################################################  
    def OnTreeTooltip(self, event):

        itemtext = self.ctb_type.GetString(event.GetItem())
#         event.SetToolTip(self.Tooltips[itemtext])
#         tree = event.GetClientObject()
#         print("Tool tip!", event.GetEventObject(), self.Tooltips[itemtext])
        event.GetEventObject().SetToolTip(self.Tooltips[itemtext])
#         event.Skip()
        
        
    ######################################################################################  
    def MiseAJour(self):
#         print("MiseAJour ens", self.classe.referentiel.Enseignement[0])
        ref = self.GetReferentiel()
        self.ctb_type.SetStringSelection(ref.Enseignement[0])
#         self.st_type.SetLabel(self.classe.GetLabel())
        self.rb_spe.Clear()
        for s in ref.listeSpecialites:
            doc = self.GetDocument()
            if (isinstance(doc, pysequence.Sequence) \
                and "S" in ref.specialite[s][5]) \
               or \
               (isinstance(doc, pysequence.Projet) \
                and "P" in ref.specialite[s][5]) \
               or \
               isinstance(doc, pysequence.Progression):
                self.rb_spe.Append(s)
#         print(self.classe.specialite)
#         for s in self.classe.specialite:
        if len(ref.listeSpecialites) > 0:
            if self.classe is not None:
                sp = self.classe.specialite
            if self.groupe is not None:
                sp = self.groupe.specialite
            self.rb_spe.SetCheckedStrings(sp)
            self.rb_spe.Show()
        
        if hasattr(self, 'bmp'):
            self.bmp.SetBitmap(self.classe.getBitmapPeriode(200*SSCALE))




# class Panel_SelectEnseignement2(wx.Panel):
#     def __init__(self, parent, panelClasse, pourProjet, classe):
#         
#         
#         
#         wx.Panel.__init__(self, parent, -1)
#         
#         self.classe = classe
#         self.panelClasse = panelClasse
#         
#         self.sizer = wx.BoxSizer(wx.VERTICAL)
#         self.SetSizer(self.sizer)
#         
# #         self.st_type = wx.StaticText(self, -1, "")
#         #
#         # Type d'enseignement
#         #
#         self.cp_type = wx.CollapsiblePane(self, wx.ID_ANY, "Type d'enseignement",
#                                           style = wx.CP_NO_TLW_RESIZE|wx.BORDER_NONE)
#         
#         self.sizer.Add(self.cp_type, 0, wx.GROW | wx.EXPAND| wx.ALL, 1)
# 
#         win = self.cp_type.GetPane()
#         self.cb_type = ArbreTypeEnseignement(win, self, pourProjet)
#         paneSz = wx.BoxSizer(wx.VERTICAL)
#         paneSz.Add(self.cb_type, 1, wx.GROW | wx.EXPAND | wx.ALL, 2)
#         win.SetSizer(paneSz)
#         paneSz.SetSizeHints(win)
#         
#         #
#         # Spécialité
#         #
#         self.sp_type = wx.CollapsiblePane(self, wx.ID_ANY, "Spécialité",
#                                           style = wx.CP_NO_TLW_RESIZE|wx.BORDER_NONE)
#         
#         self.sizer.Add(self.sp_type, 0, wx.GROW | wx.EXPAND| wx.ALL, 1)
# 
#         win = self.sp_type.GetPane()
#         self.rb_spe = wx.Choice(win, -1, choices = [])
#         self.rb_spe.SetLabel("Choisir une spécialité")
#         paneSz = wx.BoxSizer(wx.VERTICAL)
#         paneSz.Add(self.rb_spe, 1, wx.GROW| wx.EXPAND | wx.ALL, 2)
#         win.SetSizer(paneSz)
#         paneSz.SetSizeHints(win)
#         
#         #
#         # Périodes possibles
#         #
#         self.bmp = wx.StaticBitmap(self, -1, wx.Bitmap())
#         self.bmp.SetToolTip("Périodes attribuées à la spécialité")
#         self.sizer.Add(self.bmp, wx.EXPAND| wx.ALL, 1)
#         
#         
#         self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, self.cb_type)
#         self.Bind(wx.EVT_CHOICE, self.EvtRadioBoxSpe, self.rb_spe)
#         self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.layout)
# #         def_ref = REFERENTIELS[constantes.TYPE_ENSEIGNEMENT_DEFAUT]
#         
#         
#         self.MiseAJour()
#         self.sizer.Layout()
# #         self.sp_type.SetLabel(def_ref.Enseignement[0])
# #         self.cb_type.SetStringSelection(def_ref.Enseignement[0])
# #         self.sp_type.Show(len(def_ref.listeSpecialites) > 0)
# 
#     
#     ######################################################################################  
#     def layout(self, event):
#         self.sizer.Layout()
#         event.Skip()
#     
#     
#     ######################################################################################  
#     def EvtRadioBoxSpe(self, event):
# #         print('EvtRadioBoxSpe')
#         self.classe.specialite = event.GetString()
# #         self.classe.MiseAJourTypeEnseignement()
#         self.classe.doc.MiseAJourTypeEnseignement()
#         self.classe.doc.SetPosition(self.classe.doc.position)
#         self.MiseAJour()
#         self.sp_type.Collapse()
#         self.sizer.Layout()
#         
#         self.panelClasse.sendEvent(modif = "Modification de la spécialité",
#                                    obj = self.classe)
#         
#         
#     ######################################################################################  
#     def EvtRadioBox(self, event = None, CodeFam = None):
#         """ Sélection d'un type d'enseignement
#         """
#         if event != None:
#             radio_selected = event.GetEventObject()
#             CodeFam = Referentiel.getEnseignementLabel(radio_selected.GetLabel())
#         
#         self.classe.typeEnseignement, self.classe.familleEnseignement = CodeFam
#         self.classe.referentiel = REFERENTIELS[self.classe.typeEnseignement]
#         if len(self.classe.referentiel.listeSpecialites) > 0:
#             self.classe.specialite = self.classe.referentiel.listeSpecialites[0]
#         else:
#             self.classe.specialite = ""
#             
#             
# #         self.classe.MiseAJourTypeEnseignement()
#         self.classe.doc.MiseAJourTypeEnseignement()
#         self.classe.doc.SetPosition(self.classe.doc.position)
#         
#         # Gestion des affichages ...
#         self.MiseAJour()
#         self.cp_type.Collapse()
#         self.sp_type.Expand()
#         self.sizer.Layout()
#             
#         # Modification des liens vers le BO
#         self.panelClasse.SetLienBO()
#         
#         # Modification des onglet du classeur
#         self.panelClasse.GetFenetreDoc().MiseAJourTypeEnseignement()
#         
#         self.Refresh()
#         
#         self.panelClasse.sendEvent(modif = "Modification du type d'enseignement",
#                                    obj = self.classe)
#     
#     
#     ######################################################################################  
#     def Verrouiller(self):
#         etat = not self.classe.verrouillee
#         self.cp_type.Enable(etat)
#         self.sp_type.Enable(etat)
#         self.sizer.Layout()
# #         self.spe.Show(etat)
# #         self.arbre.Show(etat)
#         
#         
#         
#     ######################################################################################  
#     def MiseAJour(self):
#         self.cb_type.SetStringSelection(self.classe.referentiel.Enseignement[0])
#         self.cp_type.SetLabel(self.classe.referentiel.Enseignement[0])
# #         self.st_type.SetLabel(self.classe.GetLabel())
#         self.rb_spe.Clear()
#         for s in self.classe.referentiel.listeSpecialites:
#             self.rb_spe.Append(s)
#             
#         self.sp_type.Show(len(self.classe.referentiel.listeSpecialites) > 0)    
#         self.rb_spe.SetStringSelection(self.classe.specialite)
#         if len(self.classe.specialite) > 0:
#             self.sp_type.SetLabel(self.classe.specialite)
#         else:
#             self.sp_type.SetLabel("Choisir la Spécialité")
#         
#         self.bmp.SetBitmap(self.classe.getBitmapPeriode(200*SSCALE))

     
class ArbreTypeEnseignement(CT.CustomTreeCtrl):
    def __init__(self, parent, panelParent, pourProjet, 
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.WANTS_CHARS):#|wx.BORDER_SIMPLE):

#        wx.Panel.__init__(self, parent, -1, pos, size)
        self.panelParent = panelParent
        
        CT.CustomTreeCtrl.__init__(self, parent, -1, pos, (150*SSCALE, -1), style, 
                                   agwStyle = CT.TR_HIDE_ROOT|CT.TR_FULL_ROW_HIGHLIGHT\
                                   |CT.TR_HAS_VARIABLE_ROW_HEIGHT|CT.TR_HAS_BUTTONS\
                                   |CT.TR_TOOLTIP_ON_LONG_ITEMS)#CT.TR_ALIGN_WINDOWS|CCT.TR_NO_HEADER|T.TR_AUTO_TOGGLE_CHILD|\CT.TR_AUTO_CHECK_CHILD|\CT.TR_AUTO_CHECK_PARENT|
        self.Unbind(wx.EVT_KEY_DOWN)
        self.pourProjet = pourProjet
#        self.SetBackgroundColour(wx.WHITE)
        self.SetToolTip(wx.ToolTip("Choisir le type d'enseignement"))
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnClick)
        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
#        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnItemCollapsed)
        
#        self.AddColumn(u"")
#        self.SetMainColumn(0)
        self.root = self.AddRoot("r")
        self.Construire(self.root)
        

        
        
    ######################################################################################  
    def Construire(self, racine):
        """ Construction de l'arbre
        """
#        print "Construire ArbreTypeEnseignement"
#         print ARBRE_REF
        self.branche = []
#        self.ExpandAll()
        for t, st in ARBRE_REF:
#            print "   ", t, st, self.panelParent.pourProjet
            
            if t[0] == "_" or (self.pourProjet and len(REFERENTIELS[t].projets) == 0):
                branche = self.AppendItem(racine, REFERENTIELS[st[0]].Enseignement[2], 
                                          data = REFERENTIELS[st[0]].Enseignement[3])
            else:
                branche = self.AppendItem(racine, "")#, ct_type=2)#, image = self.arbre.images["Seq"])
                rb = wx.RadioButton(self, -1, REFERENTIELS[t].Enseignement[0])
                self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, rb)
                self.SetItemWindow(branche, rb)
                rb.SetToolTip(REFERENTIELS[t].Enseignement[1])
                rb.Enable(len(REFERENTIELS[t].projets) > 0 or not self.pourProjet)
                self.branche.append(branche)
            for sst in st:
                sbranche = self.AppendItem(branche, "")#, ct_type=2)
                rb = wx.RadioButton(self, -1, REFERENTIELS[sst].Enseignement[0])
                self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, rb)
                self.SetItemWindow(sbranche, rb)
                rb.SetToolTip(REFERENTIELS[sst].Enseignement[1])
                rb.Enable(len(REFERENTIELS[sst].projets) > 0 or not self.pourProjet)
                self.branche.append(sbranche)
        
        self.ExpandAll()
        self.CollapseAll()
        
    ######################################################################################              
    def EvtRadioBox(self, event):
#         print("EvtRadioBox")
        wnd = event.GetEventObject()
        for item in self.branche:
            if item.GetWindow() == wnd:# and item.GetParent()== self.root:
                self.OnClick(item = item)
                break
        
#        if event.GetEventObject().GetParent() == self.root:
#            self.OnClick(event)
        self.panelParent.EvtRadioBox(event)
        
        
    ######################################################################################              
    def SetStringSelection(self, label):
        for rb in self.branche:
            if isinstance(rb.GetWindow(), wx.RadioButton) and label == rb.GetWindow().GetLabel():
                rb.GetWindow().SetValue(True)
          
      
    ######################################################################################              
    def OnToolTip(self, event = None, item = None):
        node = event.GetItem()
        data = self.GetPyData(node)
        if isstring(data):
            event.SetToolTip(wx.ToolTip(data))
        else:
            event.Skip()
    
    
    ######################################################################################              
    def OnClick(self, event = None, item = None):
#        print "OnClick"
        if item == None:
            item = event.GetItem()
        else:
            self.SelectItem(item)
            
        if item.GetParent()== self.root:
            self.Freeze()
            self.CollapseAll()
            self.Expand(item)
            self.AdjustMyScrollbars()
            self.ScrollLines(1)
            self.ScrollLines(-1)
            self.Thaw()
#            self.Scroll()


    ######################################################################################              
    def CollapseAll(self):
#        print "CollapseAll"
        child = self.GetFirstChild(self.root)[0]
        while child:
            self.Collapse(child)
#            self.CalculatePositions()
            child = self.GetNextSibling(child)
        self.RefreshSubtree(self.root)
#        self.GetMainWindow().AdjustMyScrollbars()
#        self.GetMainWindow().Layout()



####################################################################################
#
#   Classe définissant l'arbre de sélection du logiciel d'un Modèle
#
####################################################################################*
class ArbreLogiciels(CT.CustomTreeCtrl):
    def __init__(self, parent, panelParent, 
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.WANTS_CHARS):#|wx.BORDER_SIMPLE):

        CT.CustomTreeCtrl.__init__(self, parent, -1, pos, (150*SSCALE, -1), style, 
                                   agwStyle = CT.TR_HIDE_ROOT|CT.TR_FULL_ROW_HIGHLIGHT\
                                   |CT.TR_HAS_VARIABLE_ROW_HEIGHT|CT.TR_HAS_BUTTONS\
                                   |CT.TR_TOOLTIP_ON_LONG_ITEMS)#CT.TR_ALIGN_WINDOWS|CCT.TR_NO_HEADER|T.TR_AUTO_TOGGLE_CHILD|\CT.TR_AUTO_CHECK_CHILD|\CT.TR_AUTO_CHECK_PARENT|
        
        self.dic_img = {}
        s = (16*SSCALE, 16*SSCALE)
        il = wx.ImageList(*s)
        for i, (n, img) in enumerate(constantes.IMG_LOGICIELS.items()):
            il.Add(scaleImage(img.GetBitmap(), 16*SSCALE,16*SSCALE))
            self.dic_img[n] = i
#         i = 0
#         for l in LOGICIELS:
#             if l.image is not None:
#                 il.Add(scaleImage(l.image.GetBitmap(),*s))
#                 self.dic_img[l.nom] = i
#                 i += 1
#                 
#             for m in l.modules:
#                 if m.image is not None:
#                     il.Add(scaleImage(m.image.GetBitmap(), *s))
#                     self.dic_img[m.nom] = i
#                     i += 1
        self.AssignImageList(il)
        
        
        self.Unbind(wx.EVT_KEY_DOWN)
        self.panelParent = panelParent
#        self.SetBackgroundColour(wx.WHITE)
        self.SetToolTip(wx.ToolTip("Choisir le logiciel"))
        
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnCheck)
        
#         self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnClick)
        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
#        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnItemCollapsed)
        
#        self.AddColumn(u"")
#        self.SetMainColumn(0)
        self.root = self.AddRoot("r")
        self.Construire(self.root)
        
    
    ######################################################################################  
    def Construire(self, racine):
        """ Construction de l'arbre
        """
#         print "Construire ArbreLogiciel"
    
        self.lstItems = []
        
        def appendBranche(branche, l):
            if l.type == 0:
                ct = 2
                wnd = None
            elif l.type == 1:
                ct = 1
                wnd = None
            if l.nom == "":
                wnd = wx.TextCtrl(self, -1, "", name = str(len(self.lstItems)))
                wnd.Enable(False)
                self.Bind(wx.EVT_TEXT, self.OnText, wnd)

            b = self.AppendItem(branche, l.nom, ct_type=ct, wnd = wnd)
            self.lstItems.append(b)
         
            if l.nom in self.dic_img:
                self.SetItemImage(b, self.dic_img[l.nom])
                
                
#             self.branche.append(b)
            return b
            
            
        self.branche = []
#        self.ExpandAll()
        for l in LOGICIELS:
            
#             print "   ", t, st
            
#             if t[0] == "_":
#                 branche = self.AppendItem(racine, t)
#             else:
            branche = appendBranche(racine, l)
#                 branche = self.AppendItem(racine, t, ct_type=ct, image = self.arbre.images["Seq"])
# #                 rb = wx.RadioButton(self, -1, t)
# #                 self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, rb)
# #                 self.SetItemWindow(branche, rb)
# #                 rb.SetToolTip(t)
#                 self.branche.append(branche)
                
            for m in l.modules:
                appendBranche(branche, m)
#                 sbranche = self.AppendItem(branche, u"")#, ct_type=2)
#                 rb = wx.RadioButton(self, -1, sst)
#                 self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, rb)
#                 self.SetItemWindow(sbranche, rb)
#                 rb.SetToolTip(sst)
#                 self.branche.append(sbranche)
        
        self.ExpandAll()
        self.CollapseAll()
#         self.Layout()
#         self.CalculatePositions()
    
    
    ######################################################################################  
    def Construire2(self, racine):
        """ Construction de l'arbre
        """
#         print "Construire ArbreLogiciel"
    
        self.lstItems = []
        
        def appendBranche(branche, t):
            if t[0] == ".":
                ct = 2
                wnd = None
            elif t[0] == "x":
                ct = 1
                wnd = None
            elif t[0] == "_":
                ct = 1
                wnd = wx.TextCtrl(self, -1, "", name = str(len(self.lstItems)))
                wnd.Enable(False)
                self.Bind(wx.EVT_TEXT, self.OnText, wnd)
#                 self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, wnd)
            t = t[1:]
            
            
            b = self.AppendItem(branche, t, ct_type=ct, wnd = wnd)
            self.lstItems.append(b)
         
            if t in list(self.dic_img.keys()):
                self.SetItemImage(b, self.dic_img[t])
                
                
#             self.branche.append(b)
            return b
            
            
        self.branche = []
#        self.ExpandAll()
        for t, st in LOGICIELS:
#             print "   ", t, st
            
#             if t[0] == "_":
#                 branche = self.AppendItem(racine, t)
#             else:
            branche = appendBranche(racine, t)
#                 branche = self.AppendItem(racine, t, ct_type=ct, image = self.arbre.images["Seq"])
# #                 rb = wx.RadioButton(self, -1, t)
# #                 self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, rb)
# #                 self.SetItemWindow(branche, rb)
# #                 rb.SetToolTip(t)
#                 self.branche.append(branche)
                
            for sst in st:
                appendBranche(branche, sst)
#                 sbranche = self.AppendItem(branche, u"")#, ct_type=2)
#                 rb = wx.RadioButton(self, -1, sst)
#                 self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, rb)
#                 self.SetItemWindow(sbranche, rb)
#                 rb.SetToolTip(sst)
#                 self.branche.append(sbranche)
        
        self.ExpandAll()
        self.CollapseAll()
#         self.Layout()
#         self.CalculatePositions()


    ######################################################################################              
    def GetLogName(self, item):
        if item.GetWindow() is None:
            return item.GetText()
        else:
            wnd = item.GetWindow()
            return "_".join([wnd.GetName(), wnd.GetValue()])
    
    
    ######################################################################################              
    def Match(self, item, listItem):
        if item.GetWindow() is None:
            if item.GetText() in listItem:
                return item.GetText()
        else:
            wnd = item.GetWindow()
            for i, n in enumerate(listItem):
                n = n.split("_", 1)
                if len(n) == 1:
                    continue
                n = n[0]
                if wnd.GetName() == n:
                    return listItem[i]
        
        
        
    ######################################################################################              
    def SetLogName(self, item, name):
        if item.GetWindow() is not None:
#             print "SetLogName", name
            wnd = item.GetWindow()
            txt = name.split("_", 1)[1]
#             print ">>", txt
            wnd.SetValue(txt)
        
        
    ######################################################################################              
    def GetAllChecked(self, itemParent=None, checkedItems=None):
        """
            source : https://stackoverflow.com/questions/26466551/how-to-get-the-checked-items-of-customtreectrl-in-wxpython
        """ 
        if itemParent is None:
            itemParent = self.GetRootItem()

        if checkedItems is None:
            checkedItems = []

        child, cookie = self.GetFirstChild(itemParent)

        while child:

            if self.IsItemChecked(child):
                checkedItems.append(self.GetLogName(child))

                checkedItems = self.GetAllChecked(child, checkedItems)
            child, cookie = self.GetNextChild(itemParent, cookie)

        return checkedItems
    
    
    ######################################################################################              
    def CheckItems(self, listItems, itemParent=None):
        """ Coche tous les logiciels de listItems
            (fonction récursive)
        """ 
#         print "CheckItems", listItems
        if itemParent is None:
            itemParent = self.GetRootItem()
        else:
            itemParent.Enable()
        
        if len(listItems) == 0:
            return
        
        child, cookie = self.GetFirstChild(itemParent)

        while child:
            name = self.Match(child, listItems)
            if name is not None:
#                 listItems.remove(name)
                child.Check()
                child.Expand()
                if child.GetWindow() is not None:
                    self.SetLogName(child, name)
                    child.GetWindow().Enable()
                
            self.CheckItems(listItems, child)
            child, cookie = self.GetNextChild(itemParent, cookie)


    
    ######################################################################################              
    def EvtRadioBox(self, event):
        wnd = event.GetEventObject()
        self.panelParent.EvtRadioBox(wnd.GetLabel())
        
        
#     ######################################################################################              
#     def SetStringSelection(self, label):
#         for rb in self.branche:
#             if isinstance(rb.GetWindow(), wx.RadioButton) and label == rb.GetWindow().GetLabel():
#                 rb.GetWindow().SetValue(True)
          
    
    ######################################################################################              
    def OnToolTip(self, event = None, item = None):
        node = event.GetItem()
        data = self.GetPyData(node)
        if isstring(data):
            event.SetToolTip(wx.ToolTip(data))
        else:
            event.Skip()
    
    
    ######################################################################################              
    def OnText(self, event = None):
#         wnd = event.GetEventObject()
        event.Skip()
        wx.CallAfter(self.panelParent.OnCheckModele)
#         print wnd
#         print self.GetItemWindow(self.lstItems[int(wnd.GetName())])
        
#     ######################################################################################              
#     def OnUpdateUI(self, event = None):
#         print "OnUpdateUI"
#         wnd = event.GetEventObject()
#         print wnd
#         print self.GetItemWindow(self.lstItems[int(wnd.GetName())])
        
    ######################################################################################              
    def OnCheck(self, event = None):
        
        item = event.GetItem()
        wnd = self.GetItemWindow(item)
        if wnd is not None:
            wnd.Enable(item.IsChecked())
#         self.log.write("Item " + self.GetItemText(item) + " Has Been Checked!\n")
        event.Skip()
        wx.CallAfter(self.panelParent.OnCheckModele)
        
        
    ######################################################################################              
    def OnClick(self, event = None, item = None):
#         print "OnClick"
        if item == None:
            item = event.GetItem()
        else:
            self.SelectItem(item)
            
        if item.GetParent()== self.root:
            self.Freeze()
            self.CollapseAll()
            self.Expand(item)
            self.AdjustMyScrollbars()
            self.ScrollLines(1)
            self.ScrollLines(-1)
            self.Thaw()
#            self.Scroll()


    ######################################################################################              
    def CollapseAll(self):
#        print "CollapseAll"
        child = self.GetFirstChild(self.root)[0]
        while child:
            self.Collapse(child)
#            self.CalculatePositions()
            child = self.GetNextSibling(child)
        self.RefreshSubtree(self.root)
#        self.GetMainWindow().AdjustMyScrollbars()
#        self.GetMainWindow().Layout()


####################################################################################
#
#   Classe définissant l'arbre de sélection d'une problematique
#
####################################################################################*

class PanelProblematiques(wx.Panel):
    def __init__(self, parent, CI, 
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.WANTS_CHARS):#|wx.BORDER_SIMPLE):
        self.CI = CI
        ref = self.CI.GetReferentiel()
        hasPb  = len(ref.listProblematiques) > 0
        
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        if hasPb:
            self.arbre = CT.CustomTreeCtrl(self, -1, pos, size, style, 
                                       agwStyle = CT.TR_HIDE_ROOT|CT.TR_FULL_ROW_HIGHLIGHT\
                                       |CT.TR_HAS_VARIABLE_ROW_HEIGHT|CT.TR_HAS_BUTTONS\
                                       |CT.TR_TOOLTIP_ON_LONG_ITEMS)#CT.TR_ALIGN_WINDOWS|CCT.TR_NO_HEADER|T.TR_AUTO_TOGGLE_CHILD|\CT.TR_AUTO_CHECK_CHILD|\CT.TR_AUTO_CHECK_PARENT|
            self.Unbind(wx.EVT_KEY_DOWN)
            self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnClick)
            self.sizer.Add(self.arbre, flag = wx.EXPAND)
            self.root = self.arbre.AddRoot("r")
            self.Construire()
            
        #
        # Cas des Problématiques personalisées
        #
        t = ref._nomPb.Plur_()
        if hasPb:
            t += " personnalisées"
        
        self.PbPerso = MyEditableListBox(self, -1, t,
                                              size = wx.DefaultSize,
                                              style = adv.EL_ALLOW_NEW | adv.EL_ALLOW_EDIT | adv.EL_ALLOW_DELETE)
        self.PbPerso.SetMinSize((-1, 60*SSCALE))
        self.PbPerso.SetToolTip("Exprimer ici la(les) %s(s) abordée(s)\n" \
                                "ou choisir une parmi les %s envisageables." %(ref._nomPb.sing_(), ref._nomPb.plur_()))

        self.PbPerso.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.EvtText)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.EvtText)
        
        self.sizer.Add(self.PbPerso, 1, flag = wx.EXPAND)
        
        
#        self.SetBackgroundColour(wx.WHITE)
        self.SetToolTip(wx.ToolTip("Ppppb"))
        
        
#        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
#        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnItemCollapsed)
        
#        self.AddColumn(u"")
#        self.SetMainColumn(0)
        
        
        self.SetSizer(self.sizer)
        
        self.MiseAJour()
        
        

    ######################################################################################              
    def Construire(self):
#         print "Construire ArbreProblematiques"
        ref = self.CI.GetReferentiel()
#        print "  ", ref.Code
#        print "  ", ref.listProblematiques
        
        self.branche = []
#        self.ExpandAll()
        for n, ci in enumerate(self.CI.GetNomCIs()):
            branche = self.arbre.AppendItem(self.root, ci)
            self.arbre.SetItemBold(branche, True)
#            print "    ", n
            if n < len(self.CI.numCI):
                if self.CI.numCI[n] < len(ref.listProblematiques):
                    for pb in ref.listProblematiques[self.CI.numCI[n]]:
                        sbranche = self.arbre.AppendItem(branche, pb, ct_type=1)
                        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.EvtCheckBox)
                        self.branche.append(sbranche)
        
        self.arbre.ExpandAll()


    ####################################################################################
    def ReConstruire(self):
#         print "ReConstruire"
        if hasattr(self, 'arbre'):
            self.arbre.DeleteChildren(self.root)
            self.Construire()
            self.arbre.ExpandAll()


    ####################################################################################
    def MiseAJour(self, CI = None):
#         print "MiseAJour Pb"
#         print self.CI.Pb
#         self.PbPerso.SetStrings(u"")
        if CI is not None:
            self.CI = CI
        
        if hasattr(self, 'arbre'):
            for b in self.branche:
                self.arbre.CheckItem2(b, False)
    #             print self.arbre.GetItemText(b)
                if self.arbre.GetItemText(b) in self.CI.Pb:
                    self.arbre.CheckItem2(b)
                
        self.PbPerso.SetStrings(self.CI.Pb_perso)
#         print "  ", self.PbPerso.GetStrings()

        
    #############################################################################            
    def EvtText(self, event):      
        wx.CallAfter(self.MAJ_Pb_perso)
        event.Skip()
        
    #############################################################################            
    def MAJ_Pb_perso(self):
#         print "MAJ_Pb_perso"
#         if hasattr(self, 'arbre'):
#             for b in self.branche:
#                 self.arbre.CheckItem2(b, False)
        
        ref = self.CI.GetReferentiel()
        self.CI.Pb_perso = self.PbPerso.GetStrings()
#         print  "  ", self.CI.Pb_perso
        
        t = "Modification %s" %ref._nomPb.du_()
        self.Parent.GetDocument().GererDependants(self.CI.parent, t)
            
        if self.Parent.onUndoRedo():
            self.Parent.sendEvent(modif = t, draw = True, verif = False)
        else:
            if not self.Parent.eventAttente:
                wx.CallLater(DELAY, self.Parent.sendEvent, modif = t, draw = True, verif = False)
                self.Parent.eventAttente = True
                
        
        
    
    ######################################################################################              
    def OnToolTip(self, event = None, item = None):
        return
#         print "OnToolTip"


    ######################################################################################              
    def OnClick(self, event = None, item = None):
        print("Fonction inutile : OnClick")


    ######################################################################################              
    def EvtCheckBox(self, event):
        ref = self.CI.GetReferentiel()
        item = event.GetItem()
        pb = self.arbre.GetItemText(item)
        if pb in self.CI.Pb:
            self.CI.Pb.remove(pb)
        else:
            self.CI.Pb.append(pb)
        self.Parent.sendEvent(modif = "Modification %s" %ref._nomPb.du_(), 
                              draw = True, verif = False)

    

    
        

###########################################################################################################
#
#  Choice
#
###########################################################################################################
class TreeCtrlComboBook(wx.Panel):
    def __init__(self, parent, tache, fct):
        self.tache = tache
        self.fct = fct
        wx.Panel.__init__(self, parent, -1)#, style = wx.BORDER_SIMPLE)
        sizer = wx.BoxSizer(wx.VERTICAL)
#        self.cc = wx.combo.ComboCtrl(self, style=wx.TE_WORDWRAP|wx.TE_MULTILINE|wx.TE_NO_VSCROLL)#wx.TE_READONLY|
        self.Bouton = wx.BitmapButton(parent, -1, images.Icone_Tache.GetBitmap(), style = wx.NO_BORDER)
        self.Bouton.SetToolTip("Selectionner une tâche")
        parent.Bind(wx.EVT_BUTTON, self.OnClick, self.Bouton)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.texte = wx.StaticText(self, -1, "", style = wx.ST_NO_AUTORESIZE|wx.ST_ELLIPSIZE_END)#|wx.BORDER_SIMPLE)
#        self.texte.FitInside()
#        sizer.Add(self.Bouton, flag = wx.EXPAND)
        sizer.Add(self.texte, 1, flag = wx.EXPAND|wx.RIGHT, border = 10*SSCALE)
        
        self.SetSizerAndFit(sizer)

    
    def SetLabel(self, texte):
        self.texte.SetLabel(wordwrap(texte, self.texte.GetSize()[0], wx.ClientDC(self)))
    
    
    def OnSize(self, evt):
        self.texte.SetSize(self.GetSize())
        w = self.GetSize()[0]
        x, y = self.GetPositionTuple()
        self.Bouton.Move((x+w-10*SSCALE, y-20*SSCALE))
        self.Refresh()
        
    def OnClick(self, evt):
        win = TreeCtrlComboPopupTaches(self,
                                 wx.SIMPLE_BORDER,
                                 self.tache,
                                 self.EvtComboBox)
#        w, h = wx.GetDisplaySize()

        btn = evt.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        win.Position(pos, (600*SSCALE,400*SSCALE))
        win.Popup()
    
    
    def ExpandAll(self):
        self.tcp.tree.ExpandAll()

    def AddItem(self, labelItem, parent = None):
        return self.tcp.AddItem(labelItem, parent)
        
    def SetItemBold(self, item, etat = True):
        self.tcp.tree.SetItemBold(item, etat)
        
    def EvtComboBox(self, texte):
        texte = "\n".join(texte.split(" ", 1))

        self.SetLabel(texte)

        self.fct(texte)
        self.Layout()
        self.Refresh()
        
    def GetStringValue(self):
        return self.tcp.GetStringValue()
        
 
###########################################################################################################
#
#  TreeCtrlComboPopup
#
###########################################################################################################
class TreeCtrlComboPopup2(wx.PopupTransientWindow):
    def __init__(self, parent, style):
        wx.PopupTransientWindow.__init__(self, parent, style)
        
        self.pnl = wx.Panel(self)
        
        self.tree = CT.CustomTreeCtrl(self.pnl, style=wx.TR_HIDE_ROOT
                                |wx.TR_HAS_BUTTONS
                                |wx.TR_SINGLE
                                |wx.TR_ROW_LINES
                                |wx.TR_LINES_AT_ROOT,
#                                |wx.SIMPLE_BORDER,
                                agwStyle = CT.TR_HAS_VARIABLE_ROW_HEIGHT | CT.TR_HIDE_ROOT)
        self.tree.SetMinSize((600*SSCALE,400*SSCALE))
        
                
        self.tree.ExpandAll()
        
        self.tree.Bind(wx.EVT_MOTION, self.OnMotion)
        self.tree.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.tree.Bind(wx.EVT_SIZE, self.OnSize)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree, 1, wx.ALL, 5)
     
        self.pnl.SetSizer(sizer)
        
        sizer.Fit(self.pnl )
        sizer.Fit(self)
        self.Layout()
        
        wx.CallAfter(self.Refresh)



    def GetControl(self):
        return self.tree


    def GetStringValue(self):
        if self.value:
            return self.tree.GetItemText(self.value)
        return ""


    def OnPopup(self):
        if self.value:
            self.tree.EnsureVisible(self.value)
            self.tree.SelectItem(self.value)


    def SetStringValue(self, value):
        # this assumes that item strings are unique...
        root = self.tree.GetRootItem()
        if not root:
            return
        found = self.FindItem(root, value)
        if found:
            self.value = found
            self.tree.SelectItem(found)


    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.Size(minWidth, min(200*SSCALE, maxHeight))
                       

    # helpers
    
    def FindItem(self, parentItem, text):        
        item, cookie = self.tree.GetFirstChild(parentItem)
        while item:
            if self.tree.GetItemText(item) == text:
                return item
            if self.tree.ItemHasChildren(item):
                item = self.FindItem(item, text)
            item, cookie = self.tree.GetNextChild(parentItem, cookie)
        return wx.TreeItemId()


    def AddItem(self, value, parent = None):
        if not parent:
            root = self.tree.GetRootItem()
            if not root:
                root = self.tree.AddRoot("<hidden root>")
            parent = root

        item = self.tree.AppendItem(parent, value)
        return item

    def OnSize(self, evt = None, parentItem = None):
        if parentItem == None:
            parentItem = self.tree.GetRootItem()
            margin = 15*SSCALE
        else:
            margin = 30*SSCALE
            
        w = self.tree.GetSize()[0]
        item, cookie = self.tree.GetFirstChild(parentItem)
        while item:
            text = self.tree.GetItemText(item).replace("\n", "")
            self.tree.SetItemText(item, wordwrap(text, w-margin-4*SSCALE, wx.ClientDC(self.tree), breakLongWords=False))
            if self.tree.ItemHasChildren(item):
                item = self.OnSize(parentItem = item)
            item, cookie = self.tree.GetNextChild(parentItem, cookie)
        return
        
        
    def OnMotion(self, evt):
        # have the selection follow the mouse, like in a real combobox
        item, flags = self.tree.HitTest(evt.GetPosition())
        if item and flags & wx.TREE_HITTEST_ONITEMLABEL:
            self.tree.SelectItem(item)
            self.curitem = item
        evt.Skip()

    def OnClick(self, evt):
        item, _ = self.tree.HitTest(evt.GetPosition())
#        print self.tree.GetItemParent(item)
        if item and self.tree.GetItemParent(item) != self.tree.GetRootItem():
            self.fct(self.tree.GetItemText(self.tree.GetSelection()).replace("\n", ""))
            self.Dismiss()
        
#    def OnLeftDown(self, evt):
#        # do the combobox selection
#        item, flags = self.tree.HitTest(evt.GetPosition())
#        if item and flags & wx.TREE_HITTEST_ONITEMLABEL:
#            self.curitem = item
#            self.value = item
#            self.Dismiss()
#        evt.Skip()

    
class TreeCtrlComboPopupTaches(TreeCtrlComboPopup2):
    def __init__(self, parent, style, tache, fct):
        self.fct = fct
        TreeCtrlComboPopup2.__init__(self, parent, style)
        
        prj = tache.GetProjetRef()
        if prj is None:
            return 
        
        ph = None
        for ct in prj.listTaches:
            if ph != prj.taches[ct][0]:
                pph = self.AddItem(prj.phases[prj.taches[ct][0]][1])
                self.tree.SetItemBold(pph, True)
                ph = prj.taches[ct][0]
            item = self.AddItem(ct+" "+prj.taches[ct][1], parent=pph)
            if prj.tachesOnce:
                self.tree.EnableItem(item, ct not in [t.intitule for t in tache.projet.taches])
            
    
###########################################################################################################
#
#  ComboTreeBox personnalisé
#
###########################################################################################################
class myComboTreeBox(wx.ComboCtrl):
    def __init__(self, *arg, **kargs):
        wx.ComboCtrl.__init__(self, *arg, **kargs)
        self.tcp = TreeCtrlComboPopup()
        self.SetPopupControl(self.tcp)
    
#     def Append(self, itemText, parent = None, clientData=None):
#         if parent is None:
#             parent = self.tcp.GetRootItem()
#         self.tcp.AppendItem(parent, itemText, image=-1, data=clientData)

    def Append(self, value, parent = None, clientData = None):
        return self.tcp.AddItem(value, parent, clientData)
#         
    def ExpandAll(self):
        self.tcp.ExpandAll()
    
    def SetClientDataSelection(self, data):
#         print("SetClientDataSelection", data)
        self.tcp.SetClientDataSelection(data)
#         print("value", self.GetStringSelection())
        self.SetText(self.GetStringSelection())
        
    def GetClientData(self, item = None):
        return self.tcp.GetClientData(item)
         
    
    def SetStringSelection(self, text):
        self.tcp.SetStringValue(text)
        self.SetValue(text)
        
        
    def GetStringSelection(self):
        return self.tcp.GetStringValue()
    
    
    def GetString(self, item):
        return self.tcp.GetString(item)


    def OnLeftDown(self, evt):
        self.SetText(self.GetStringSelection())
#         self.GetEventHandler().ProcessEvent(evt)
#         print("OnLeftDown2")
#         self.Parent.GetEventHandler().ProcessEvent(evt)
        

    def GetTree(self):
        return self.tcp.tree

    def FindClientData(self, clientData, parentItem=None):
        return self.tcp.FindClientData(clientData, parentItem)
        
        
        
class TreeCtrlComboPopup(wx.ComboPopup):
    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.tree = None
    
    def FindClientData(self, clientData, parentItem = None):
        item, cookie = self.tree.GetFirstChild(parentItem)
        while item:
            if self.tree.GetItemData(item) == clientData:
#                 print(" ", clientData, self.tree.GetItemData(item), clientData==self.tree.GetItemData(item))
#                 print(item)
                return item
            if self.tree.ItemHasChildren(item):
                item = self.FindClientData(clientData, item)
                if item:
                    return item
            item, cookie = self.tree.GetNextChild(parentItem, cookie)
    
    
    def FindItem(self, text, parentItem = None):       
#         print(self, parentItem, text) 
        item, cookie = self.tree.GetFirstChild(parentItem)
        while item:
            if self.tree.GetItemText(item) == text:
                return item
            if self.tree.ItemHasChildren(item):
                item = self.FindItem(text, item)
                if item:
                    return item
            item, cookie = self.tree.GetNextChild(parentItem, cookie)
#         return wx.TreeItemId(), 


    def SetClientDataSelection(self, data):
#         print("SetClientDataSelection", data)
        root = self.tree.GetRootItem()

        if not root:
            return
        found = self.FindClientData(data, root)
        if found is not None:
#             print("   >", found)
            self.value = found
            self.tree.SelectItem(found)
        
        
    def AddItem(self, value, parent = None, clientData = None):
        if not parent:
            root = self.tree.GetRootItem()
            if not root:
                root = self.tree.AddRoot("<hidden root>")
            parent = root

        item = self.tree.AppendItem(parent, value, data = clientData)
        return item


    def OnMotion(self, evt):
        # have the selection follow the mouse, like in a real combobox
        item, _ = self.tree.HitTest(evt.GetPosition())
        if item:# and flags & wx.TREE_HITTEST_ONITEMLABEL:
#             self.tree.SelectItem(item)
            self.curitem = item
#     def OnToolTip(self, evt):
#         item, flags = self.tree.HitTest(evt.GetPosition())
            ev = wx.TreeEvent(wx.EVT_TREE_ITEM_GETTOOLTIP.typeId, self.tree, item)
            self.GetComboCtrl().GetEventHandler().ProcessEvent(ev)

#         self.tree.SetToolTip("aaa")
        evt.Skip()
        
        
    def OnLeftDown(self, evt):
#         print("OnLeftDown", self.GetComboCtrl())
        # do the combobox selection
        item, flags = self.tree.HitTest(evt.GetPosition())
        if item and flags & wx.TREE_HITTEST_ONITEMLABEL:
            self.curitem = item
            self.value = item
            self.Dismiss()
        
        ev = wx.CommandEvent(wx.EVT_COMBOBOX.typeId)
        ev.SetString(self.GetStringValue())
        ev.SetClientData(self.GetClientData(item))
        ev.SetEventObject(self.GetComboCtrl())
#         print("   ", self.GetClientData(item))
#         self.GetComboCtrl().GetEventHandler().ProcessEvent(ev)
#         print("OnLeftDown", item)
#         self.GetComboCtrl().OnLeftDown(ev)
        self.GetComboCtrl().GetEventHandler().ProcessEvent(ev)
        evt.Skip()
        
    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.

    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.value = None
        self.curitem = None


    def ExpandAll(self):
        root = self.tree.GetRootItem()
        if root:
            item, cookie = self.tree.GetFirstChild(root)
            while item:
                self.tree.ExpandAllChildren(item)
                item, cookie = self.tree.GetNextChild(root, cookie)
        
        
        
#         root = self.tree.GetRootItem()
#         if root:
#             self.tree.ExpandAllChildren(root)
    
    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        self.tree = wx.TreeCtrl(parent, style=wx.TR_HIDE_ROOT
                                |wx.TR_HAS_BUTTONS#wx.TR_NO_BUTTONS#
                                |wx.TR_SINGLE
                                |wx.TR_LINES_AT_ROOT
                                |wx.SIMPLE_BORDER)

        self.tree.Bind(wx.EVT_MOTION, self.OnMotion)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
#         self.tree.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        return True

    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self.tree

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, value):
#         print("SetStringValue", value)
        root = self.tree.GetRootItem()
        if not root:
            return
        found = self.FindItem(value, root)
        
        if found is not None:
#             print(">>", found)
            self.value = found
            self.tree.SelectItem(found)

    # Return a string representation of the current item.
    def GetStringValue(self):
#         print("GetStringValue", self.value)
        if self.value is not None:
#             print("  ", self.tree.GetItemText(self.value))
            return self.tree.GetItemText(self.value)
        return ""
    
    def GetString(self, item):
        if item:
            return self.tree.GetItemText(item)
        return ""

    def GetClientData(self, item = None):
        if item is not None and item.IsOk():
            return self.tree.GetItemData(item)
        elif self.value is not None:
            return self.tree.GetItemData(self.value)
        return ""
    
    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.ComboPopup.OnPopup(self)
        if self.value:
            self.tree.EnsureVisible(self.value)
            self.tree.SelectItem(self.value)


    # Called when popup is dismissed
    def OnDismiss(self):
        wx.ComboPopup.OnDismiss(self)

    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        wx.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        wx.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        wx.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.ComboPopup.GetAdjustedSize(self, minWidth, prefHeight, maxHeight)

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.
    # Default returns false.
    def LazyCreate(self):
        return wx.ComboPopup.LazyCreate(self)
    
    
###########################################################################################################
#
#  Liste de Checkbox
#
###########################################################################################################
        
class ChoixCompetenceEleve(wx.Panel):
    def __init__(self, parent, indic, projet, tache, fonction):
#        print "init ChoixCompetenceEleve"
        wx.Panel.__init__(self, parent, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.indic = indic
        self.fonction = fonction
        self.parent = parent
        
        cb = []
        for _ in projet.eleves:
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
#         print("MiseAJour ChoixCompetenceEleve", self.tache, self.indic)
        for i, e in enumerate(self.projet.eleves): 
            dicIndic = e.GetDicIndicateursRevue(self.tache.phase)
#            print "    ", dicIndic
            comp = self.indic.split("_")[0]
            if comp in list(dicIndic.keys()):
                if comp != self.indic: # Indicateur seul
                    indic = eval(self.indic.split("_")[1])
                    self.cb[i].Enable(dicIndic[comp][indic-1])
            elif self.tache.estPredeterminee():
#                print "  ", e, self.tache.eleves
                self.cb[i].Enable(i in self.tache.eleves) 
            else:
                self.cb[i].Enable(False)
#            self.cb[i].Update()
        
    #############################################################################
    def Actualiser(self):
        """ Coche/décoche les cases à cocher
            
        """
#         print("Actualiser", self.tache)
#        self.CocherTout(self.indic in self.tache.indicateurs)
        
        for i in range(len(self.projet.eleves)):
            if self.cb[i].IsThisEnabled():
#                 print("  ", i, self.tache.indicateursEleve)
                if i+1 in self.tache.indicateursEleve:
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
        self.fonction(self.indic, etat, eleve, event != None)
        
#    #############################################################################
#    def CocherTout(self, etat):
#        for cb in self.cb:
#            if cb.IsEnabled():
#                cb.SetValue(etat)
            
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
    def EstToutDecoche(self):
        t = True
        for cb in self.cb:
            t = t and not cb.GetValue() 
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





def get_key(dic, value, pos = None):
    """ Renvoie la clef du dictionnaire <dic> correspondant à la valeur <value>
    """
    i = 0
    continuer = True
    while continuer:
        if i > len(list(dic.keys())):
            continuer = False
        else:
            if pos:
                v = list(dic.values())[i][pos]
            else:
                v = list(dic.values())[i]
            if v == value:
                continuer = False
                key = list(dic.keys())[i]
            i += 1
    return key








##########################################################################################################
#
#  Dialogue de sélection d'URL
#
##########################################################################################################
class URLDialog(wx.Dialog):
    def __init__(self, parent, lien, pathseq):
        wx.Dialog.__init__(self, parent, -1, "Sélection de lien")
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
#         self.Create(parent, -1,  "Sélection de lien")

        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Sélectionner un fichier, un dossier ou une URL")
        label.SetHelpText("Sélectionner un fichier, un dossier ou une URL")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Lien :")
#        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        url = lien.URLSelectorCombo(self, lien, pathseq)
        self.Bind(lien.EVT_PATH_MODIFIED, self.OnPathModified)
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






# class URLSelectorCombo(wx.Panel):
#     def __init__(self, parent, lien, pathseq, dossier = True, ext = ""):
# #         print "init URLSelectorCombo", pathseq
#         
#         wx.Panel.__init__(self, parent, -1)
#         self.SetMaxSize((-1,22*SSCALE))
#         
#         self.ext = ext
#         self.dossier = dossier
#         self.lien = lien
#         
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         
#         
#         lsizer = self.CreateSelector()
#         
#         
#         
#         sizer.Add(lsizer, 1, flag = wx.EXPAND)
#         self.SetSizerAndFit(sizer)
#         
#         self.SetPathSeq(pathseq)
# 
#     
#     
#     ###############################################################################################
#     def CreateSelector(self):
#         # Passage momentané en Anglais (bug de wxpython)
# #         locale2EN()
# #         loc = wx.GetApp().locale.GetSystemLanguage()
# #         wx.GetApp().locale = wx.Locale(wx.LANGUAGE_ENGLISH)
#         
#         sizer = wx.BoxSizer(wx.HORIZONTAL)
#         bsize = (16*SSCALE, 16*SSCALE)
#         
#         self.texte = wx.TextCtrl(self, -1, toSystemEncoding(self.lien.path), size = (-1, bsize[1]))
#         self.texte.SetToolTip("Saisir un nom de fichier/dossier ou un URL\nou faire glisser un fichier")
#         if self.dossier:
# #             bt1 =wx.BitmapButton(self, 100, wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, bsize))
#             bt1 =wx.BitmapButton(self, 100, scaleImage(images.Icone_folder.GetBitmap(), *bsize))
#             bt1.SetToolTip("Sélectionner un dossier")
#             self.Bind(wx.EVT_BUTTON, self.OnClick, bt1)
#             self.bt1 = bt1
#             sizer.Add(bt1)
# #         bt2 =wx.BitmapButton(self, 101, images.wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, bsize))
#         bt2 =wx.BitmapButton(self, 101, scaleImage(images.Icone_fichier.GetBitmap(), *bsize))
#         bt2.SetToolTip("Sélectionner un fichier")
#         self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
#         self.Bind(wx.EVT_TEXT, self.EvtText, self.texte)
#         self.bt2 = bt2
#         
#         sizer.Add(bt2)
#         sizer.Add(self.texte,1,flag = wx.EXPAND)
#         
# #         self.btnlien = wx.BitmapButton(self, -1, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, bsize))
#         self.btnlien = wx.BitmapButton(self, -1, scaleImage(images.Icone_open.GetBitmap(), *bsize))
#         self.btnlien.SetToolTip("Ouvrir le lien externe")
#         self.btnlien.Show(self.lien.path != "")
#         self.Bind(wx.EVT_BUTTON, self.OnClickLien, self.btnlien)
#         sizer.Add(self.btnlien)
#          
#         
#         # Pour drag&drop direct de fichiers !! (expérimental)
#         file_drop_target = MyFileDropTarget(self)
#         self.SetDropTarget(file_drop_target)
#         
# #         locale2def()
# #         wx.GetApp().locale = wx.Locale(loc)
#         
#         return sizer
#     
#     
#     #############################################################################            
#     def OnClickLien(self, event):
#         self.lien.Afficher(self.pathseq)
# 
# 
#     ###############################################################################################
#     # Overridden from ComboCtrl, called when the combo button is clicked
#     def OnClick(self, event):
#         
#         if event.GetId() == 100:
#             dlg = wx.DirDialog(self, "Sélectionner un dossier",
#                           style=wx.DD_DEFAULT_STYLE,
#                           defaultPath = toSystemEncoding(self.pathseq)
#                            #| wx.DD_DIR_MUST_EXIST
#                            #| wx.DD_CHANGE_DIR
#                            )
#             if dlg.ShowModal() == wx.ID_OK:
#                 self.SetPath(dlg.GetPath(), 'd')
#     
#             dlg.Destroy()
#             
#         else:
#             dlg = wx.FileDialog(self, "Sélectionner un fichier",
#                                 wildcard = self.ext,
#                                 defaultDir = toSystemEncoding(self.pathseq),
#     #                           defaultPath = globdef.DOSSIER_EXEMPLES,
#                                style = wx.DD_DEFAULT_STYLE
#                                #| wx.DD_DIR_MUST_EXIST
#                                #| wx.DD_CHANGE_DIR
#                                )
#     
#             if dlg.ShowModal() == wx.ID_OK:
#                 self.SetPath(dlg.GetPath(), 'f')
#     
#             dlg.Destroy()
#         
#         self.MiseAJour()
#         
#         self.SetFocus()
# 
# 
#     ###############################################################################################
#     def Enable(self, etat):
#         self.texte.Enable(etat)
#         self.bt2.Enable(etat)
#         if hasattr(self, "bt1"):
#             self.bt1.Enable(etat)
#         
#         
#     ###############################################################################################
#     def MiseAJour(self):
# #         self.btnlien.Show(self.lien.path != "")
#         self.marquerValid()
# 
# 
#     ###############################################################################################
#     def dropFiles(self, file_list):
#         for path in file_list:
#             self.SetPath(path, 'f')
#             return
#             
#     ##########################################################################################
#     def EvtText(self, event):
# #         self.lien.EvalLien(event.GetString(), self.pathseq)
# #         if not self.lien.ok:
# #             self.lien.EvalTypeLien(self.pathseq)
#         self.SetPath(event.GetString())
# 
# 
#     ##########################################################################################
#     def GetPath(self):
#         return self.lien
#     
#     
#     ##########################################################################################
#     def SetPath(self, lien = None, typ = None, marquerModifier = True):
#         """ lien doit être de type 'String' encodé en SYSTEM_ENCODING
#             
#         """
# #         print("SetPath", self.lien)
# #         print "   ", lien, typ
#         if lien is not None:
#             self.lien.path = lien
#             self.lien.EvalLien(lien, self.pathseq)
# 
#         try:
#             self.texte.ChangeValue(self.lien.path)
#         except: # Ca ne devrait pas arriver ... et pourtant ça arrive !
#             self.lien.path = self.lien.path.decode(FILE_ENCODING)
# #             self.lien.path = self.lien.path.encode(SYSTEM_ENCODING)
#             self.texte.ChangeValue(toSystemEncoding(self.lien.path)) # On le met en SYSTEM_ENCODING
# 
#         self.MiseAJour()
#         
#         
#         if hasattr(self.Parent, 'GetPanelRacine'):
#             self.Parent.GetPanelRacine().OnPathModified(self.lien, marquerModifier = marquerModifier)
#         
#         
#     ##########################################################################################
#     def SetPathSeq(self, pathseq):
#         self.pathseq = pathseq
# 
#     
#     ##########################################################################################
#     def marquerValid(self):
#         if self.lien.ok:
#             self.texte.SetBackgroundColour(
#                  wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
#             self.btnlien.SetToolTip("Ouvrir le lien externe")
#             
#         else:
#             self.texte.SetBackgroundColour("pink")
#             self.texte.SetFocus()
#             self.btnlien.SetToolTip("Le lien est invalide")
#         
#         self.btnlien.Enable(self.lien.ok)
#         self.Refresh()
#         
#         
#         
        
        
#############################################################################################################
#
# A propos ...
# 
#############################################################################################################
class A_propos(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "A propos de "+ version.__appname__)
        
        self.app = parent
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        titre = wx.StaticText(self, -1, " "+version.__appname__)
        titre.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, False))
        titre.SetForegroundColour(wx.Colour("BROWN"))
        sizer.Add(titre, border = 10)
        sizer.Add(wx.StaticText(self, -1, "Version : "+version.__version__+ " "), 
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
        
        lstActeurs = (("Développement : ", ("Cédrick FAURY", "Jean-Claude FRICOU")), \
                      ("Référentiels : ",  ("Thierry VALETTE (STS EE)", \
                                             "Jean-Claude FRICOU (STS SN)", \
                                             "Emmanuel VIGNAUD (Ede SI-CIT-DIT 2nde)", \
                                             "Arnaud BULCKE (Techno Collège)", \
                                             "Laurent Moutoussamy (MPSI)", \
                                             "André Forys (NSI)",
                                             "Hubert Faigner (STS MS)",
                                             "Ludovic FROMAGEOT (STS CPI)")), \
                      
                      ("Remerciements : ", ("un grand merci aux très nombreux", \
                                             "utilisateurs qui ont pris le temps", \
                                             "de nous signaler les dysfonctionnements,", \
                                             "et de nous faire part de leurs remarques.",)),
                      
                      ("Crédits : ",       ("Icones :\n - https://fr.icons8.com\nwww.iconfinder.com"\
                                            "\n https://thenounproject.com/term/broken-image/583402/",)))

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
            txt = open(os.path.join(util_path.PATH, "LICENSE.txt"))
            lictext = txt.read()
            txt.close()
        except:
            lictext = "Le fichier de licence (LICENSE.txt) est introuvable !\n\n" \
                      "Veuillez réinstaller %s !" %version.__appname__
            messageErreur(self, 'Licence introuvable',
                          lictext)
            
            
        tl = wx.TextCtrl(licence, -1, lictext, size = (400*SSCALE, -1), 
                    style = wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_NONE )
        s = wx.BoxSizer()
        s.Add(tl, flag = wx.EXPAND)
        licence.SetSizer(s)
        
        # Description
        #-------------
        descrip = wx.Panel(nb, -1)
        t = wx.StaticText(descrip, -1,"",
                          size = (400, -1))#,
#                        style = wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_NONE) 
        txt = wordwrap("<b>%s</b> est un logiciel d'aide à l'élaboration de séquences et progressions pédagogiques et à la validation de projets,\n"
                                          "sous forme de fiches exportables au format PDF ou SVG.\n"
                                          "Il est élaboré en relation avec les programmes et les documents d'accompagnement\n"
                                          "des enseignements des filières :\n"
                                          " STI2D, \n SSI\n Technologie Collège\n STS EE et SN\n EdE SI-CIT-DIT 2nde." %version.__appname__, 500, wx.ClientDC(self))
        if hasattr(t, 'SetLabelMarkup'): # wxpython 3.0
            t.SetLabelMarkup(txt )
        else:
            t.SetLabel(txt.replace('<b>', '').replace('</b>', '') )
        
        s = wx.BoxSizer()
        s.Add(t, flag = wx.EXPAND)
        descrip.SetSizer(s)
        
        # Dossiers
        #-------------
        dossiers = wx.Panel(nb, -1)
        print(util_path.INSTALL_PATH)
        td =  "Dossier d'installation : " + str(util_path.INSTALL_PATH) + "\n" \
            + "Dossier de démarrage : " + str(util_path.PATH) + "\n" \
            + "Dossier COMMUN pour les données : " + util_path.APP_DATA_PATH + "\n" \
            + "Dossier USER pour les données : " + util_path.APP_DATA_PATH_USER

        t = wx.StaticText(dossiers, -1,td,
                          size = (400, -1))
        
        s = wx.BoxSizer()
        s.Add(t, flag = wx.EXPAND)
        dossiers.SetSizer(s)
        
        nb.AddPage(descrip, "Description")
        nb.AddPage(auteurs, "Auteurs")
        nb.AddPage(dossiers, "Dossiers")
        nb.AddPage(licence, "Licence")
        
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Informations et téléchargement :"),  
                  flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
        
        
        sizer.Add(hl.HyperLinkCtrl(self, wx.ID_ANY, version.__url__,
                                   URL = version.__url__),  
                  flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
        sizer.Add(nb)
        
        self.SetSizerAndFit(sizer)

class StaticBitmapZoom(wx.StaticBitmap):
    def __init__(self, *args, **kargs):
        wx.StaticBitmap.__init__(self, *args, **kargs)
        
        self.Bind(wx.EVT_MOTION, self.OnMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.W, self.H = 0, 0

    def SetLargeBitmap(self, largeBitmap):
        self.largeBitmap = largeBitmap
        self.W, self.H = largeBitmap.GetWidth(), largeBitmap.GetHeight()
        self.OnLeave()
    
    def OnLeave(self, event = None):
        if hasattr(self, 'largeBitmap'):
            self.SetBitmap(self.largeBitmap.ConvertToImage().Scale(*self.GetSize()).ConvertToBitmap())
        
    def OnMove(self, event):
        if hasattr(self, 'largeBitmap'):
            x, y = event.GetPosition()
            w, h = self.GetSize()
            x, y = (w-self.W)*x/w, (h-self.H)*y/h
            
            
    #        self.popup = wx.PopupTransientWindow(self)
            img = self.largeBitmap.ConvertToImage().Resize(self.GetSize(), (x, y))
            self.SetBitmap(img.ConvertToBitmap())
            self.Refresh()

class myStaticBox(wx.StaticBox):
    def __init__(self, *args, **kargs):
        wx.StaticBox.__init__(self, *args, **kargs)
        self.SetForegroundColour(wx.Colour("DIM GREY"))
        
        
#############################################################################################################
#
# ProgressDialog personnalisé
# 
#############################################################################################################
# class MyProgressDialog2(wx.Dialog):
#     """"""
#  
#     #----------------------------------------------------------------------
#     def __init__(self):
#         """Constructor"""
#         wx.Dialog.__init__(self, None, title="Progress")
#         self.count = 0
#  
#         self.progress = wx.Gauge(self, range=20)
#  
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(self.progress, 0, wx.EXPAND)
#         self.SetSizer(sizer)
#  
#         # create a pubsub receiver
#         pub.subscribe(self.update, "update")
#  
#     #----------------------------------------------------------------------
#     def update(self, msg):
#         """"""
#         self.count += 1
#  
#         if self.count >= 20:
#             self.Destroy()
#  
#         self.progress.SetValue(self.count)
#  
 
 
 
 
class myProgressDialog(wx.Dialog):
    def __init__(self, titre, message, maximum, parent, style = 0, 
                 btnAnnul = True, msgAnnul = "Annuler l'opération"):

        wx.Dialog.__init__(self, parent, -1, titre, size = (400*SSCALE, 200*SSCALE),
                          style = wx.FRAME_FLOAT_ON_PARENT| wx.CAPTION | wx.FRAME_TOOL_WINDOW | wx.STAY_ON_TOP)

        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour(wx.WHITE)
        
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        
        self.count = 0
        self.maximum = maximum
        self.stop = False # Pour opération "Annuler"
        
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.titre = wx.StaticText(panel, -1)
#         self.titre.SetLabelMarkup(u"<big><span fgcolor='blue'>%s</span></big>" %t)
        self.titre.SetFont(wx.Font(11, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.titre.SetForegroundColour((50,50,200))
        sizer.Add(self.titre, 0, wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, 20*SSCALE)

        self.message = wx.TextCtrl(panel, -1, size = (-1, 200*SSCALE), 
                                   style = wx.TE_MULTILINE|wx.TE_READONLY|wx.VSCROLL|wx.TE_NOHIDESEL)
        sizer.Add(self.message, 1, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.EXPAND, 15)
        
        self.SetMessage(message)
        
        
        self.gauge = wx.Gauge(panel, -1, maximum)
        sizer.Add(self.gauge, 0, wx.GROW|wx.ALL|wx.EXPAND, 5)
#         print dir(self.gauge)
        if maximum < 0:
            self.gauge.Pulse()
            
        line = wx.StaticLine(panel, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALL|wx.EXPAND, 5)

        self.btn = wx.Button(panel, -1, "Annuler")
        self.btn.SetHelpText(msgAnnul)
        self.btn.Enable(btnAnnul)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btn)
        
        sizer.Add(self.btn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        mainsizer.Add(panel, 1, flag = wx.EXPAND)
        
        panel.SetSizer(sizer)
        panel.Layout()
        self.panel = panel
        self.SetSizer(mainsizer)
#         sizer.Fit(self)
        
        self.sizer = sizer

#         self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        
        self.CenterOnParent()
        self.SetMinSize((400*SSCALE, -1))        
        



#     def OnDestroy(self, event):
#         try:
#             self.GetParent().Enable(True)
#         except:
#             pass
#         event.Skip()


    def update(self, count, message):
#         print "Update", count
        self.SetMessage(message)
        self.count = count
        
        if self.maximum >= 0 and (self.count >= self.maximum or self.count < 0):
            self.GetParent().Enable(True)
            self.btn.SetLabel("Ok")
        self.panel.Layout()
        self.Fit()

#         wx.Frame.Update(self)
        
        if self.maximum >= 0:
            wx.CallAfter(self.gauge.SetValue, self.count)
    #         self.gauge.SetValue(self.count)
            self.gauge.Update()
            self.gauge.Refresh()
            
#             wx.Yield()
#             wx.AppConsole.Yield()
            try:
                self.gauge.UpdateWindowUI()
            except:
                pass
            
        self.gauge.Refresh()
#         time.sleep(.1)
#         self.Refresh()
        
        
    def GetMessage(self):
        return self.titre.GetLabel()+"\n\n"+self.message.GetValue()
    
    
    def SetMessage(self, message):
        m = message.split("\n\n")
        if len(m) > 1:
            t, m = m[0], "\n\n".join(m[1:])
        else:
            t, m = m[0], ""
            
        self.titre.SetLabel(t)
        self.message.ChangeValue(m)
#         self.message.ScrollLines(-1)
#         self.message.ScrollPages(1) 
        self.message.ShowPosition(self.message.GetLastPosition ())
        
    
    def OnClick(self, event):
        self.GetParent().Enable(True)
        if event.GetEventObject().GetLabel()[0] == "A":
            self.stop = True
        else:
            self.Destroy()




#############################################################################################################
#
# Information PopUp (format HTML)
# 
#############################################################################################################
class myHtmlWindow(html.HtmlWindow):
    def __init__(self, *arg, **kargs):
        html.HtmlWindow.__init__(self, *arg, **kargs)
        
    def OnLinkClicked(self, evt):
        webbrowser.open_new((evt.GetHref()))
        self.Parent.Show(False)
        
    def OnCellClicked(self, cell, x, y, evt):
#         print('OnCellClicked: %s, (%d %d)\n' % (cell, x, y))
        if isinstance(cell, html.HtmlWordCell):
            sel = html.HtmlSelection()
#             print('     %s\n' % cell.ConvertToText(sel))
        super(myHtmlWindow, self).OnCellClicked(cell, x, y, evt)
        return True


# class myComboTreeBox(ComboTreeBox):
#     def __init__(self, *arg, **karg):
#         ComboTreeBox.__init__(self, *arg, **karg)
#         
#         
#     def SetSizeP(self, s):
#         self.w, self.h = s
#         
#     def GetSizeP(self):
#         return self.w, self.h
#         
#     def Popup(self):
#         """Pops up the frame with the tree."""
#         comboBoxSize = self.GetSizeP()
#         x, y = self.GetParent().ClientToScreen(self.GetPosition())
#         y += comboBoxSize[1]
#         width = comboBoxSize[0]
#         height = comboBoxSize[1]
#         self._popupFrame.SetSize(x, y, width, height)
#         # On wxGTK, when the Combobox width has been increased a call
#         # to SetMinSize is needed to force a resize of the popupFrame:
#         self._popupFrame.SetMinSize((width, height))
#         self._popupFrame.Show()
    
    
    
class PopupInfo(wx.PopupWindow):
    def __init__(self, parent, page = "", mode = "H", width = 400*SSCALE):
        wx.PopupWindow.__init__(self, parent, wx.BORDER_SIMPLE)
        
        self.parent = parent
        sizer = wx.BoxSizer(wx.VERTICAL)
#         print "PopupInfo", size[0], id(self)
        
        self.w = width
        size = (self.w, -1)
        
        #
        self.mode = mode
        if mode == "H":
#             self.html = myHtmlWindow(self, -1, size = size,
#                                      style = wx.NO_FULL_REPAINT_ON_RESIZE|html.HW_SCROLLBAR_AUTO)#html.HW_SCROLLBAR_NEVER)
            self.html = PyClickableHtmlWindow(self, -1, size = size,
                                     style = wx.NO_FULL_REPAINT_ON_RESIZE|html.HW_SCROLLBAR_AUTO)#html.HW_SCROLLBAR_NEVER)
        else:
            self.html = webview.WebView.New(self, size = size)
            self.SetClientSize(size)
        
        self.SetHTML(page)

#         self.SetMinSize(size)
#         self.html.SetSize(size)
        
        self.SetPage()
        
        
        self.SetAutoLayout(True)
        
        # Un fichier temporaire pour mettre une image ...
        self.tfname = []
        
        
        #'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'+
        sizer.Add(self.html, 1, flag = wx.EXPAND)
        
        self.SetSizer(sizer)
        
        self.html.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
#         self.Bind(wx.EVT_MOTION, self.OnLeave)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)
        self.Bind(wx.EVT_BUTTON, self.OnClick)
        
        # Pour gérér le déplacement de la fenêtre
        self._dragPos = None
        self.html.Bind(wx.EVT_MOTION, self.OnMotion)

    
    ##########################################################################################
    def OnMotion(self, event):
        if not event.Dragging():
            self._dragPos = None
            if self.html.HasCapture():
                self.html.ReleaseMouse()
            return
        if not self.html.HasCapture():
            self.html.CaptureMouse()
        if not self._dragPos:
            self._dragPos = event.GetPosition()
#             print "Drag :", self._dragPos
        else:
            pos = event.GetPosition()
            displacement = self._dragPos - pos
#             print "   ...", pos, displacement
            self.SetPosition( self.GetPosition() - displacement )
#             self.Parent.Refresh()
            
            
    ##########################################################################################
    def OnLeave(self, event):
#         print "Leave Tip"
        x, y = event.GetPosition()
        w, h = self.GetSize()
#         print y, h
        if not ( x > 0 and y > 0 and x < w-2 and y < h-2):
            self.Show(False)
            if self.html.HasCapture():
                self.html.ReleaseMouse()
        event.Skip()
        
    #####################################################################################
    def SetWidth(self, w):
        self.w = w
        size = (self.w, -1)
        self.html.SetSize(size)
        self.SetClientSize(size)
        
        
#    ##########################################################################################
#    def SetBranche(self, branche):
#        self.branche = branche

    #####################################################################################
    def SetHTML(self, ficheHTML, parser = "html5lib"):
#         print ficheHTML
        self.soup = BeautifulSoup(ficheHTML, parser)#.decode('utf-8')
#         print " >>>>>>"
#         print self.soup.prettify()
        
#.encode('utf-8', errors="ignore"), from_encoding="utf-8"


#     #####################################################################################
#     def Supprime(self, Id):
#         tag = self.soup.find(id=Id)
#         tag.extract()


#     #####################################################################################
#     def Render_Template(self, template, *args, **kargs):
#         self.AjouterHTML
        
    #####################################################################################
    def AjouterHTML(self, Id, text):
        """ Ajoute un texte au format HTML
        """
#         print("AjouterHTML", text)
        if text is None:
            return
        tag = self.soup.find(id=Id)
        t = BeautifulSoup(text, "html5lib")
        for c in t.contents:
            tag.append(c)
        
    
    #####################################################################################
    def InsererSoup(self, Id, soup):
        """ Insere un texte au format soup
        """
#         print "AjouterHTML", text
        tag = self.soup.find(id=Id)
        tag.append(soup)
    
    
#     #####################################################################################
#     def SetWholeText(self, Id, text, bcoul = None, fcoul = "black", 
#                      bold = False, italic = False, size = 0):
#         """ 
#         """
# #        print "SetWholeText", text
#         if text is None:
#             return
#         
# #         text = text.replace("\n", "<br/>")
#         tag = self.soup.find(id=Id)
#         if tag is None:
#             return
#         
#         li = text.split("\n")
#         for i, t in enumerate(li):
#             f = self.soup.new_tag("font")
#             f.string = t
#             
#             if fcoul != "black":
#                 f["color"] = fcoul
#                 
#             if size != 0:
#                 f["size"] = size
#                 
#             if bold:   
#                 f.string.wrap(self.soup.new_tag("b"))
#     
#             if italic:     
#                 f.string.wrap(self.soup.new_tag("i"))
#             
#             tag.append(f)
#             if i < len(li) -1:
#                 br = self.soup.new_tag('br')
#                 tag.append(br)

#     ##########################################################################################
#     def setLien(self, Id, lien, elem):
        
        
#     ##########################################################################################
#     def AjouterLien(self, Id, lien, elem):
# 
#         tag = self.soup.find(id = Id)
#         if tag is None: return
#         
#         if lien.type == 'u':
#             a = self.soup.new_tag("a")
#             a.string = lien.path
#             a["href"] = lien.path
#             tag.append(a)
#             
#         elif lien.type in ["f", "d"]:
#             self.elem = elem
#             b = self.soup.new_tag("wxp")
#             b["module"] = "wx"
#             b["class"] = "Button"
#             
#             param  = self.soup.new_tag("param")
#             param["name"] = "id"
#             param["value"] = "-1"
#             b.append(param)
#             
#             param  = self.soup.new_tag("param")
#             param["name"] = "label"
#             param["value"] = os.path.split(lien.path)[1]
#             b.append(param)
#             
# #             param  = self.soup.new_tag("param")
# #             param["name"] = "name"
# #             param["value"] = "Bouton"
# #             b.append(param)
#             
#             tag.append(b)
            
        
    
#     ##########################################################################################
#     def AjouterTxt(self, Id, texte, bcoul = None, fcoul = "black", 
#                      bold = False, italic = False, size = 0):
# #        print "AjouterTxt", texte
#         tag = self.soup.find(id = Id)
#         
#         if fcoul != None or size != 0:     
#             f = self.soup.new_tag("font")
#             if fcoul != None:
#                 f["color"] = fcoul
#             if size != 0:
#                 f["size"] = size
# 
#             tag.append(f)
#             tag = f
#             
#         if bold:   
#             b = self.soup.new_tag("b")
#             tag.append(b)
#             tag = b
# 
#         if italic:     
#             i = self.soup.new_tag("i")
#             tag.append(i)
#             tag = i
#             
#         lignes = texte.split("\n")
#         for i, l in enumerate(lignes):
#             if i > 0:
#                 br = self.soup.new_tag('br')
#                 tag.append(br)
#             tag.append(NavigableString(l))
#        print tag


    ##########################################################################################
    def GetImgURL(self, bmp, width = None):
#         try:
        self.tfname.append(tempfile.mktemp()+".png")
        bmp.SaveFile(self.tfname[-1], wx.BITMAP_TYPE_PNG)
#         except:
#             return
        
        return self.tfname[-1]



#     ##########################################################################################
#     def AjouterImg(self, item, bmp, width = None):
#         try:
#             self.tfname.append(tempfile.mktemp()+".png")
#             bmp.SaveFile(self.tfname[-1], wx.BITMAP_TYPE_PNG)
#         except:
#             print("err")
#             return
#         img = self.soup.find(id = item)
# #        print "img", img
#         img['src'] = self.tfname[-1]
#         
#         if width is not None:
#             img['width'] = str(width)
#             img['height'] = str(int(width*bmp.GetHeight()/bmp.GetWidth()))

#        img = node.getElementById(item)
#        if img != None:
#            td = node.createElement("img")
#            img.appendChild(td)
#            td.setAttribute("src", self.tfname)


#     #####################################################################################
#     def AjouterListe(self, idListe, lst_log):
#         t = ['disc', 'square', 'circle']
# 
#         liste = self.soup.find(id = idListe)
#         
#         def Liste(l, l_log, i):
#             ul = self.soup.new_tag("ul")
#             l.append(ul)
#             ul['type'] = t[i]
#             for log in l_log:
#                 li = self.soup.new_tag("li")
#                 
#                 if type(log) == tuple:
#                     li.append(log[0][1:])
#                     Liste(li, log[1], (i+1) % 3)
#                 else:
#                     li.append(log[1:])    
#                 ul.append(li)
# 
#         Liste(liste, lst_log, 0)
#         
        
    #####################################################################################
    def AjouterElemListeUL(self, idListe, li):
        liste = self.soup.find(id = idListe)
#        print "liste", liste,liste.find_all('li')
        if len(liste.find_all('li')) == 1 and liste.li.string == " ":
            liste.li.string = li
        else:
            tag_li = copy.copy(liste.li)
            tag_li.string = li
            liste.append(tag_li)


    #####################################################################################
    def AjouterElemListeDL(self, idListe, dt, dd):
        liste = self.soup.find(id = idListe)
#        print "liste", liste,liste.find_all('dt')
        if len(liste.find_all('dt')) == 1 and liste.dt.string == " ":
            liste.dt.string = dt
            liste.dd.string = dd
        else:
            tag_dt = copy.copy(liste.dt)
            tag_dd = copy.copy(liste.dd)
            tag_dt.string = dt
            tag_dd.string = dd
            liste.append(tag_dt)
            liste.append(tag_dd)


    #####################################################################################
    def AjouterCol(self, idLigne, text, bcoul = None, fcoul = "black", size = None, bold = False):
        """<td id="rc1" style="background-color: #ff6347;"><font id="r1" size="2">1</font></td>"""
        ligne = self.soup.find(id = idLigne)
        if ligne != None:
            td = self.soup.new_tag("td")
            
            ligne.append(td)
            
            if bcoul != None:
                td["style"] = "background-color: "+bcoul
            
            if size != None:
                tc = self.soup.new_tag("font", size = str(size))
                td.append(tc)
                td = tc
            
            if bold:
                tc = self.soup.new_tag("b")
                td.append(tc)
                td = tc

            td.append(text)


    ####################################################################################
    def SupprimerTag(self, idTag):
        tag = self.soup.find(id = idTag)
        tag.decompose()


#     ####################################################################################
#     def Construire(self, dic , tache, prj, code = None, check = False):
#         """ Construit l'arborescence des Compétences et Indicateurs.
#             Deux formats possibles pour <dicIndicateurs> :
#             
#         """
# #        print "Construire", dicIndicateurs
# #        print dic
#         self.tache = tache
#         self.dic = dic
#         self.prj = prj
#         self.code = code
#         dicIndicateurs = tache.GetDicIndicateurs()
#         def const(d, ul):
#             ks = list(d.keys())
#             ks.sort()
#             for k in ks:
# #                print "  k:", k
#                 competence = d[k]
#                 li = self.soup.new_tag("li")
#                 ul.append(li)
#                 
#                 if competence.sousComp != {}: #len(v) > 1 and type(v[1]) == dict:
# #                    font = self.soup.new_tag("font")
#                     nul = self.soup.new_tag("ul")
#                     li.append(textwrap.fill(k+" "+competence.intitule, 50))
#                     const(competence.sousComp, nul)
#                     li.append(nul)
#                     
#                 else:   # Indicateur
#                     nul = self.soup.new_tag("ul")
#                     cc = [cd+ " " + it for cd, it in zip(k.split("\n"), competence.intitule.split("\n"))] 
#                     nul['type']="1"
#                     li.append(textwrap.fill("\n ".join(cc), 50))
# 
#                     ajouteIndic(nul, competence.indicateurs, "S"+k, )
#                 
#                     li.append(nul)
#                 
#             return
# 
#         
#                 
#                 
#         def ajouteIndic(fm, listIndic, code):
#             if code in list(dicIndicateurs.keys()):
#                 listIndicUtil = dicIndicateurs[code]
#             else:
#                 listIndicUtil = None
# 
#             for i, indic in enumerate(listIndic):
#                 
#                 if i > 0:
#                     br = self.soup.new_tag("br")   
#                     fm.append(br)
#                 
#                 codeIndic = code+"_"+str(i+1)
#                 
#                 coche = check and tache.estACocherIndic(codeIndic)
#                 if coche:
#                     li = self.soup.new_tag("wxp")
#                     li["module"] = "widgets"
#                     li["class"] = "CheckBoxValue"
#                     param  = self.soup.new_tag("param")
#                     param["name"] = "id"
#                     param["value"] = str(100+i)
#                     li.append(param)
#                     
#                     param  = self.soup.new_tag("param")
#                     param["name"] = "name"
#                     param["value"] = codeIndic
#                     li.append(param)
#                     
#                     param  = self.soup.new_tag("param")
#                     param["name"] = "value"
#                     li.append(param)
#                     
#                     fm.append(li)
#                     
#                 font = self.soup.new_tag("font")    
# #                 li.append(font)
#                 font.append(textwrap.fill(indic.intitule, 50))
#                 
#                 
#                 
#                 fm.append(font)
# #                 li['type']="1"
#                 
#                 for part in list(prj.parties.keys()):
#                     if part in list(indic.poids.keys()):
#                         if listIndicUtil == None or not listIndicUtil[i]:
#                             c = COUL_ABS
#                             if coche:
#                                 param["value"] = "False"
#                         else:
#                             c = getCoulPartie(part)
#                             if coche:
#                                 param["value"] = "True"
# 
#                 font['color'] = couleur.GetCouleurHTML(c, wx.C2S_HTML_SYNTAX)
#         
#         if type(dic) == dict:
#             ul = self.soup.find(id = "comp")
#             const(dic, ul)
#         else:
#             fm = self.soup.find(id = "comp")
#             ajouteIndic(fm, dic, code)
    
    
    #########################################################################################################
    def GetDocument(self):
        return self.tache.GetDocument()
    
    
    
    #########################################################################################################
    def onUndoRedo(self):
        """ Renvoie True si on est en phase de Undo/Redo
        """
        return self.GetDocument().undoStack.onUndoRedo# or self.GetDocument().classe.undoStack.onUndoRedo

     
    #########################################################################################################
    def sendEvent(self, doc = None, modif = "", draw = False, verif = False):
        self.GetDocument().GetApp().sendEvent(doc, modif, draw = draw, verif = verif)
        self.eventAttente = False
        
        
    ############################################################################            
    def SetCompetences(self):
#        print "SetCompetences"
        
        self.GetDocument().MiseAJourDureeEleves()
        
        modif = "Ajout/Suppression d'une compétence à la Tâche"
        if self.onUndoRedo():
            self.sendEvent(modif = modif, draw = True, verif = True)
        else:
            self.sendEvent(modif = modif, draw = True, verif = True)
#             wx.CallAfter(self.sendEvent, modif = modif, draw = True, verif = True)
        
        self.tache.projet.Verrouiller()
        
#         ul = self.soup.find(id = "comp")
#         ul.clear()
#         self.Construire(self.dic , self.tache, self.prj, self.code, check = True)
#         self.SetPage()
        self.Update()
        
    
    ##########################################################################################
    def OnCheck(self, evt):
        cb = evt.GetEventObject()
        code = cb.GetName()
#         print "OnCheck", cb.GetValue(), cb.GetName()
        if cb.GetValue():
            self.tache.AjouterCompetence(code)
        else:
            self.tache.EnleverCompetence(code)
        evt.Skip()
        self.SetCompetences()
#         wx.CallAfter(self.SetCompetences)
    
    ##########################################################################################
    def OnClick(self, evt):
        btn = evt.GetEventObject()
#         doc = btn.Parent.Parent.parent.GetDocument()
        print("OnClick")
        obj = None
        try:
            obj = ctypes.cast(int(btn.GetName()), ctypes.py_object).value
        except:
            print("Objet inconnu :", btn.GetName())
            return
#         b = evt.GetEventObject()
#         n = b.GetName()
#         print "OnCheck", cb.GetValue(), cb.GetName()
        obj.lien.Afficher(obj.GetDocument().GetPath())

        
    ##########################################################################################
    def OnDestroy(self, evt): 
#         print "OnDestroy", evt.GetWindow()
        if isinstance(evt.GetWindow(), wx.PopupWindow):
            for f in self.tfname:
                if os.path.exists(f):
                    os.remove(f)


    ##########################################################################################
    def SetPage(self):
#         print("SetPage")
#        self.SetSize((10,1000))
#        self.SetClientSize((100,1000))
#        self.html.SetSize( (100, 100) )
#        self.SetClientSize(self.html.GetSize())
#         size = (self.w, -1)
#         self.SetClientSize(size)
#         self.html.SetClientSize(size)

#        print self.html.GetSize()
#        print self.html.GetClientSize()
        
#        self.SetClientSize(self.html.GetClientSize())
#        self.Fit()

        if self.mode == "H":
#             print(self.GetClientSize())
#             self.html.SetPage("")
            
#             print self.soup.prettify()
            
#             self.html.SetPage(self.soup.prettify())
#             self.html.AppendToPage(self.soup.prettify())
            self.html.SetPage(self.soup.prettify())
            ir = self.html.GetInternalRepresentation()
#             print("   ", ir.GetWidth(), ir.GetHeight())
#             ir.Layout(self.w)
            
#             self.html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
#             self.SetClientSize(self.html.GetSize()) 
#             print ir.GetWidth(), ir.GetHeight()
            self.SetClientSize((ir.GetWidth() + 10*SSCALE, 
                                ir.GetHeight()+  5*SSCALE))
            self.html.SetClientSize((ir.GetWidth(), ir.GetHeight()))
        else:
            self.html.SetPage(self.soup.prettify(), "")

            
 
    
        
        
    


#############################################################################################################
#
# Dialog pour choisir le type de document à créer
# 
#############################################################################################################
class DialogChoixDoc(wx.Dialog):
    def __init__(self, parent,
                 style=wx.DEFAULT_DIALOG_STYLE 
                 ):

        wx.Dialog.__init__(self, parent, -1, "Créer ...", style = style, size = wx.DefaultSize)
        self.SetMinSize((200*SSCALE,100*SSCALE))
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        button = wx.Button(self, -1, "Nouvelle Séquence")
        button.SetToolTip("Créer une nouvelle séquence pédagogique")
        if int(wx.version()[0]) > 2:
            button.SetBitmap(images.Icone_sequence.Bitmap,wx.LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnSeq, button)
        sizer.Add(button,0, wx.ALL|wx.EXPAND, 5)
        
        button = wx.Button(self, -1, "Nouveau Projet")
        button.SetToolTip("Créer un nouveau projet")
        if int(wx.version()[0]) > 2:
            button.SetBitmap(images.Icone_projet.Bitmap,wx.LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnPrj, button)
        sizer.Add(button,0,  wx.ALL|wx.EXPAND, 5)
    
        button = wx.Button(self, -1, "Nouvelle Progression")
        button.SetToolTip("Créer une nouvelle progression pédagogique")
        if int(wx.version()[0]) > 2:
            button.SetBitmap(images.Icone_progression.Bitmap,wx.LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnPrg, button)
        sizer.Add(button,0,  wx.ALL|wx.EXPAND, 5)
        
        self.SetSizer(sizer)
        sizer.Fit(self)
        
        self.SetReturnCode(0)
        

    def OnSeq(self, event):
        self.SetReturnCode(1)
        self.EndModal(1)

    def OnPrj(self, event):
        self.SetReturnCode(2)
        self.EndModal(2)
        
    def OnPrg(self, event):
        self.SetReturnCode(3)
        self.EndModal(3)

#import pywintypes



#############################################################################################################
#
# Dialog pour choisir l'action à réaliser en cas de référentiel modifié
# 
#############################################################################################################
class DiffRefChoix(wx.Dialog):
    def __init__(self, parent, nomFichier, 
                 style=wx.DEFAULT_DIALOG_STYLE 
                 ):

        wx.Dialog.__init__(self, parent, -1, "Référentiel différent", style = style, size = wx.DefaultSize)
        self.SetMinSize((200*SSCALE,100*SSCALE))
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        st = wx.StaticText(self, -1, f"Le référentiel intégré au fichier {nomFichier}\n" \
                                     f"est différent du référentiel fourni par pySéquence.\n\n" \
                                     f"Soit vous avez modifié sciemment ce référentiel,\n" \
                                     f"Soit il a été mis à jour depuis la création du fichier {nomFichier}.\n\n" \
                                     f"Que souhaitez-vous faire ?"
                                     
                           )
        
        sizer.Add(st, 0,  wx.ALL|wx.EXPAND, 10)#wx.ALIGN_CENTRE|
        
        button = wx.Button(self, -1, "Remplacer le référentiel")
        button.SetToolTip("Remplacer le référentiel intégré au document\npar celui fourni avec pySéquence")
        self.Bind(wx.EVT_BUTTON, self.OnRepl, button)
        sizer.Add(button,0, wx.ALL|wx.EXPAND, 15)
        
        button = wx.Button(self, -1, "Conserver le référentiel")
        button.SetToolTip("Conserver le référentiel intégré au document")
        self.Bind(wx.EVT_BUTTON, self.OnCons, button)
        sizer.Add(button,0, wx.ALL|wx.EXPAND, 15)
        
        self.SetSizer(sizer)
        sizer.Fit(self)
        
        self.SetReturnCode(0)
        

    def OnRepl(self, event):
        self.SetReturnCode(1)
        self.EndModal(1)

    def OnCons(self, event):
        self.SetReturnCode(2)
        self.EndModal(2)
        


##########################################################################################################
#
#  Panel pour l'affichage des BO
#
##########################################################################################################
class Panel_BO(wx.Panel, FullScreenWin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.nb = wx.Notebook(self, -1)
        self.sizer.Add(self.nb, proportion=1, flag = wx.EXPAND)
        
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
        self.SetSizer(self.sizer)
        
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        FullScreenWin.__init__(self, self)

    ######################################################################################################
    def OnEnter(self, event):
        self.SetFocus()
        event.Skip()
        

    ######################################################################################################
    def OnPageChanged(self, event):
        pass
    
    ######################################################################################################
    def Construire(self, ref):
#         print("Construire Panel_BO")
#         if ref.BO_dossier == "":
#             return
        
        wx.BeginBusyCursor()
        
        lst_pdf = []
#         for d in ref.BO_dossier:
        path = os.path.join(util_path.BO_PATH, ref.Code)
        if not os.path.exists(path):
            wx.EndBusyCursor()
            return
        
        for root, dirs, files in os.walk(path):
            for f in files:
                if os.path.splitext(f)[1] == ".pdf":
                    lst_pdf.append(os.path.join(root, f))
            
      
#        print self.nb.GetPageCount()
        for index in reversed(list(range(self.nb.GetPageCount()))):
            try:
                self.nb.DeletePage(index)
            except:
                print("raté :", index)
#        self.dataNoteBook.SendSizeEvent()
        
        
        for f in lst_pdf:
            page = genpdf.PdfPanel(self.nb)
            page.chargerFichierPDF(f)
            self.nb.AddPage(page, os.path.split(os.path.splitext(f)[0])[1])

        wx.EndBusyCursor()
        
        
##########################################################################################################
#
#  Panel pour l'affichage des diagrammes SysML
#
##########################################################################################################

class Panel_Select_sysML(wx.Panel, FullScreenWin):
    def __init__(self, parent, doc, code):
        self.doc = doc
        
        self.lien = doc.sysML[code] # Type lien.LienImege
        
        wx.Panel.__init__(self, parent, -1)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.selec = lien.URLSelector(self, self.lien, doc.GetPath(), dossier = False)
        self.Bind(lien.EVT_PATH_MODIFIED, self.OnPathModified)
        self.sizer.Add(self.selec, flag = wx.ALIGN_TOP|wx.EXPAND)
        
        self.image = wx.StaticBitmap(self, -1, wx.NullBitmap)
        
        self.sizer.Add(self.image, flag = wx.EXPAND)#, flag = wx.EXPAND)
        
        self.FitInside()
        self.SetSizer(self.sizer)
        self.Layout()
    
    
    #############################################################################            
    def GetDocument(self):
        return self.doc
    
    
    #########################################################################################################
    def sendEvent(self, doc = None, modif = "", draw = False, verif = False):
        self.GetDocument().GetApp().sendEvent(doc, modif, draw = draw, verif = verif)
    
    
    #########################################################################################################
    def OnPathModified(self, evt):
#         print("OnPathModified, sysML", self.lien)
        self.SetImage(sendEvt = True) 
    
    
    #########################################################################################################
    def MiseAJour(self, titre = "image", prefixe = "l'"):
#         print("MiseAJour Panel_Select_sysML")
#         self.boxImg.SetLabel(titre.capitalize())
#         self.btImg.SetToolTip("Sélectionner un fichier image pour %s" %prefixe+titre)
#         self.btSupImg.SetToolTip("Supprimer %s" %prefixe+titre)
        self.selec.SetPath()
        self.SetImage()
    
    
    #############################################################################            
    def SetImage(self, sendEvt = False):
#         print("SetImage", self.lien)
        defaut = images.Icone_noimg.GetBitmap()
#         print(defaut)
        bmp = self.lien.getBitmap(defaut)
            
        if self.lien.ok:
            self.image.Bind(wx.EVT_LEFT_DOWN, self.OnClicImage)
            self.image.SetToolTip("Cliquer pour ouvrir le fichier")
        else:
            self.image.SetToolTip("")
            self.image.Unbind(wx.EVT_LEFT_DOWN)
        
        self.image.SetBitmap(rognerImage(bmp, 200*SSCALE, HMIN_PROP*SSCALE-80*SSCALE))
        
        self.Parent.Layout()
        self.Layout()
        
        if sendEvt:
            self.sendEvent(modif = "Modification du fichier sysML",
                           draw = False, verif = False)
            
            
    #############################################################################            
    def OnSupprImage(self, event):
        self.lien.reset()
        self.SetImage(True)
    
    
    #############################################################################            
    def OnClicImage(self, event):
        self.lien.Afficher(self.doc.GetPath())
        
        
          
#     #############################################################################            
#     def OnClickImage(self, event):
#         doc = self.GetDocument()
#         mesFormats = "Fichier Image|*.bmp;*.png;*.jpg;*.jpeg;*.gif;*.pcx;*.pnm;*.tif;*.tiff;*.tga;*.iff;*.xpm;*.ico;*.ico;*.cur;*.ani|" \
#                        "Tous les fichiers|*.*'"
#         
#         dlg = wx.FileDialog(
#                             self, message="Ouvrir une image",
# #                            defaultDir = self.DossierSauvegarde, 
#                             defaultFile = "",
#                             wildcard = mesFormats,
#                             style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
#                             )
#             
#         # Show the dialog and retrieve the user response. If it is the OK response, 
#         # process the data.
#         if dlg.ShowModal() == wx.ID_OK:
#             # This returns a Python list of files that were selected.
#             paths = dlg.GetPaths()#.decode(FILE_ENCODING)
#             nomFichier = paths[0]
#             
#             try:
#                 locale2EN()
#                 bmp = wx.Image(nomFichier).ConvertToBitmap()
#                 locale2def()
#             except:
#                 messageErreur(self, "Erreur !",
#                                     "Fichier image invalide !\n" \
#                                  )
#                 dlg.Destroy()
#                 return
#             doc.sysML[self.code].setPath(nomFichier)
#             self.SetImage(True)
#         
#         dlg.Destroy()
        
##########################################################################################################
#
#  Panel pour l'affichage des tâches détailles par élève
#
##########################################################################################################
class Panel_Details(wx.Panel, FullScreenWin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.ConstruireTb()
        
        self.nb = wx.Notebook(self, -1)
        self.sizer.Add(self.nb, proportion=1, flag = wx.EXPAND)
        
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
        self.SetSizer(self.sizer)
        
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        FullScreenWin.__init__(self, self.nb)
        

    ######################################################################################################
    def OnEnter(self, event):
        self.SetFocus()
        event.Skip()
        
    
    ######################################################################################################
    def OnPageChanged(self, event):
        pass
    
    ######################################################################################################
    def Construire(self, fichierCourant, projet, typ):
        wx.BeginBusyCursor()
        
        self.fichierCourant = fichierCourant
        self.projet = projet
        
        # Suppression des pages
        for index in reversed(list(range(self.nb.GetPageCount()))):
            try:
                self.nb.DeletePage(index)
            except:
                print("raté :", index)
#        self.dataNoteBook.SendSizeEvent()
        
        # Recréation des pages
        for e in projet.eleves:
            page = RapportRTF(self.nb, rt.RE_READONLY)
            page.Remplir(fichierCourant, projet, typ, e)
            self.nb.AddPage(page, e.GetNomPrenom())

        wx.EndBusyCursor()

    
    ###############################################################################################
    def ConstruireTb(self):
        """ Construction de la ToolBar
        """
#        print "ConstruireTb"

        #############################################################################################
        # Création de la barre d'outils
        #############################################################################################
#         self.tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        self.tb = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        
        tsize = (IMG_SIZE_TB[0]*SSCALE, IMG_SIZE_TB[1]*SSCALE)
        
        edit_bmp = scaleImage(images.document_edit.GetBitmap(),*tsize)
        save_bmp =  scaleImage(images.Icone_save.GetBitmap(),*tsize)
        saveas_bmp = scaleImage(images.Icone_saveas.GetBitmap(),*tsize)
        saveall_bmp =  scaleImage(images.Icone_saveall.GetBitmap(),*tsize)
        
        
#         edit_bmp = images.document_edit.GetBitmap()
#         save_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
#         saveas_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, tsize)
#         saveall_bmp =  images.Icone_saveall.GetBitmap()
        
        self.tb.SetToolBitmapSize(tsize)
        
        self.tb.AddTool(10, "Enregistrer", save_bmp, wx.NullBitmap,
                             shortHelp="Enregistrement de la fiche courante sous son nom actuel", 
                             longHelp="Enregistrement de la fiche courante sous son nom actuel")
        
        self.tb.AddTool(12, "Enregistrer tout", saveall_bmp, wx.NullBitmap,
                             shortHelp="Enregistrement de tous les documents sous leurs noms actuels", 
                             longHelp="Enregistrement de tous les documents sous leurs noms actuels")
        

        self.tb.AddTool(11, "Enregistrer sous...", saveas_bmp, wx.NullBitmap,
                             shortHelp="Enregistrement de la fiche courante sous un nom différent", 
                             longHelp="Enregistrement de la fiche courante sous un nom différent")
        
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrer, id=10)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrerSous, id=11)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrerTout, id=12)
        
        
        self.tb.AddSeparator()
        
        self.tb.AddTool(13, "Editer", edit_bmp, wx.NullBitmap,
                             shortHelp="Editer la fiche", 
                             longHelp="Editer la fiche")
        
        self.Bind(wx.EVT_TOOL, self.commandeEditer, id=13)
        
        #################################################################################################################
        #
        # Mise en place
        #
        #################################################################################################################
        self.tb.Realize()
        self.sizer.Add(self.tb, flag = wx.EXPAND)

    
    ###############################################################################################
    def commandeEditer(self, event):
        page = self.nb.GetCurrentPage()
        if page != None:
            win = FrameRapport(self, self.fichierCourant, self.projet, 'prj', page.eleve)
            win.Show()
        
    
#     ######################################################################################################
#     def getNomFichierDefaut(self):
#         page = self.nb.GetCurrentPage()
#         if page != None:
#             f = u"Tâches détaillées _ " + page.eleve.GetNomPrenom() + u".rtf"
#             return os.path.join(self.projet.GetPath(), f)


    ######################################################################################################
    def commandeEnregistrer(self, evt):
        page = self.nb.GetCurrentPage()
        if page != None:
            page.Enregistrer("Enregistrer les détails", page.getNomFichierDefaut())


    ######################################################################################################
    def commandeEnregistrerTout(self, evt):
        for page in [self.nb.GetPage(i) for i in range(self.nb.GetPageCount())]:
            page.Enregistrer("Enregistrer les détails", page.getNomFichierDefaut())


    ######################################################################################################
    def commandeEnregistrerSous(self, evt):
        page = self.nb.GetCurrentPage()
        if page != None:
            page.EnregistrerSous("Enregistrer les détails", page.getNomFichierDefaut())
            
            
        



##########################################################################################################
#
#  CodeBranche : conteneur du code d'un élément à faire figurer dans un arbre
#
##########################################################################################################
class CodeBranche(wx.Panel):
    def __init__(self, arbre, code = ""):
        wx.Panel.__init__(self, arbre, -1)
        sz = wx.BoxSizer(wx.HORIZONTAL)
        self.code = wx.StaticText(self, -1, code)
        sz.Add(self.code)
        
        self.info = wx.BoxSizer(wx.HORIZONTAL)
        sz.Add(self.info)
        
        self.SetSizerAndFit(sz)
        
        self.reset()
        
        self.code.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
    
    
    def OnClick(self, event):
#        print "OnClick"
        if hasattr(self, 'branche'):
            self.Parent.SelectItem(self.branche)

        
    def reset(self):
        self.info.Clear(delete_windows=True)
        self.comp = {}
#         self.img = wx.StaticBitmap(self, -1, wx.NullBitmap)
    
    
    def SetBranche(self, branche): 
        self.branche = branche
    
    
    def SetItalic(self, italic = True):
        font = self.code.GetFont().Italic()
        self.code.SetFont(font)
    
    
    def Add(self, clef, text = ""):
        self.comp[clef] = wx.StaticText(self, -1, "")
        self.info.Add(self.comp[clef])
    
    
    def AddImg(self):
        self.img = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.info.Add(self.img)


    def SetLabel(self, text):
        self.code.SetLabel(text)
        self.LayoutFit()
    
    
    def SetImg(self, bmp):
        bmp = scaleImage(bmp, IMG_SIZE_TREE[0]*SSCALE, IMG_SIZE_TREE[1]*SSCALE)
        self.img.SetBitmap(bmp)
        self.LayoutFit()
        
        
    def DelImg(self):
        self.img.SetBitmap(wx.NullBitmap)
        self.LayoutFit()
        
        
    def SetBackgroundColour(self, color):
        self.code.SetBackgroundColour(color)
        
        
    def SetForegroundColour(self, color):
        self.code.SetForegroundColour(color)
    
    
    def SetToolTip(self, text):
        self.code.SetToolTip(text)
        
        
    def LayoutFit(self):
        self.Layout()
        self.Fit()
        
        
        
##########################################################################################################
#
#  DirSelectorCombo
#        http://wxpython-users.1045709.n5.nabble.com/Auto-fitting-ComboBox-td4470228.html
#
##########################################################################################################
class SlimSelector(wx.ComboBox):
    """ ComboBox that displays in minimal width.
    """
    def __init__ (self, *args, **kwargs):
        wx.ComboBox.__init__ (self, *args, **kwargs)
        self.SlimResize()
        
    def SlimResize(self):
        choices = self.GetStrings()
        if choices:
            height = self.GetSize()[1]
            dc = wx.ClientDC (self)
            tsize = max ( (dc.GetTextExtent (c)[0] for c in choices) )
            self.SetMinSize ( (tsize+25*SSCALE, height) )     
        
    
        
        
##########################################################################################################
#
#  DirSelectorCombo
#
##########################################################################################################
class DirSelectorCombo(combo.ComboCtrl):
    def __init__(self, *args, **kw):
        combo.ComboCtrl.__init__(self, *args, **kw)

        # make a custom bitmap showing "..."
        bw, bh = 14*SSCALE, 16*SSCALE
        bmp = wx.Bitmap(bw,bh)
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
#        dlg = wx.FileDialog(self, "Choisir un fichier modéle", path, name,
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



        

    
    
#     # Version fichier sur le disque : long !! (mais ça marche
#     data = ""
#     # convert the image file to a temporary file
#     tfname = tempfile.mktemp()
#     try:
#         img.SaveFile(tfname, wx.BITMAP_TYPE_PNG)
#         data = b64encode(open(tfname, "rb").read())
#     finally:
#         if os.path.exists(tfname):
#             try:
#                 os.remove(tfname)
#             except:
#                 pass
#     return data



#############################################################################################################
#
# Message d'aide CI
# 
#############################################################################################################


class MessageAideCI(GMD.GenericMessageDialog):
    def __init__(self, parent):
        GMD.GenericMessageDialog.__init__(self,  parent, 
                                  "Informations à propos de la cible CI",
                                  "Informations à propos de la cible CI",
                                   wx.OK | wx.ICON_QUESTION
                                   #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
        self.SetExtendedMessage("Afin que tous les CI apparaissent sur la cible,\n"\
                                  "ils doivent cibler des domaines (MEI)\n"\
                                  "et des niveaux (FSC) différents.\n\n"\
                                  "Les CI ne pouvant pas étre placés sur la cible\n"\
                                  "apparaitront en orbite autour de la cible (2 maxi).\n\n"\
                                  "Si le nombre de CI sélectionnés est limité à 2,\n"\
                                  "le deuxiéme CI sélectionnable est forcément\n"\
                                  "du méme domaine (MEI) que le premier\n"\
                                  "ou bien un des CI en orbite.")
#        self.SetHelpBitmap(help)
        
        
class CairoStaticBitmap(wx.Panel):
    def __init__(self, parent, drawFcn, larg):
        wx.Panel.__init__(self, parent)
        self.drawFcn = drawFcn
        self.larg = larg        # Largeur en pixels
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.InitBuffer()

    #############################################################################            
    def OnPaint(self, evt = None):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.buffer, 0,0) 
#         self.Render(dc)

    #############################################################################            
    def InitBuffer(self):
        w,h = self.GetSize()
        self.buffer = wx.Bitmap(w,h)

    #############################################################################            
    def Render(self):
        cdc = wx.ClientDC(self)
        dc = wx.BufferedDC(cdc, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        ctx = wx.lib.wxcairo.ContextFromDC(dc)
        
#         self.normalize(ctx)
        self.drawFcn(ctx, self.larg)
        
        self.ctx = ctx
        self.Refresh()
            
            
            

        
import pysequence

# Gestion des messages d'erreur
if not DEBUG:
    import error

