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

u"""
module objects_wx
*****************

Les principaux éléments du GUI de **pySéquence**.


"""


DEBUG = False

####################################################################################
#
#   Imports minimum et SplashScreen
#
####################################################################################
# Outils système
import os, sys
import util_path

print sys.version_info

# à décommenter pour forcer l'utilisation de wxpython 2.8 (ubuntu 14)
# if sys.platform != "win32":
#     import wxversion
#    wxversion.select('2.8')

import wx
import  wx.gizmos   as  gizmos
# try:
#     
# except:
#     import wx.adv as gizmos     # à partir de wx 4
    
import version

# Module de gestion des dossiers, de l'installation et de l'enregistrement
from util_path import toFileEncoding, toSystemEncoding, FILE_ENCODING, SYSTEM_ENCODING, \
                        testRel, nomCourt

import richtext

import time

# Chargement des images
import images


#####################################################################################
#   Tout ce qui concerne le GUI
#####################################################################################
     
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

from wx.lib.wordwrap import wordwrap
import wx.lib.hyperlink as hl
import  wx.lib.scrolledpanel as scrolled
import wx.combo
import wx.lib.platebtn as platebtn
import wx.lib.colourdb
import  wx.lib.colourselect as  csel
# Pour les descriptions

import orthographe
import wx.stc  as  stc
import wx.richtext as rt

########################################################################
try:
    from agw import genericmessagedialog as GMD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.genericmessagedialog as GMD


# Les constantes partagées
from constantes import calculerEffectifs, \
                        strEffectifComplet, getElementFiltre, \
                        CHAR_POINT, COUL_PARTIE, getCoulPartie, COUL_ABS, \
                        TOUTES_REVUES_EVAL, TOUTES_REVUES_EVAL_SOUT, TOUTES_REVUES_SOUT, TOUTES_REVUES, \
                        _S, _Rev, _R1, _R2, _R3, \
                        getSingulier, getPluriel, getSingulierPluriel, \
                        COUL_OK, COUL_NON, COUL_BOF, COUL_BIEN, \
                        toList, COUL_COMPETENCES, WMIN_PROP, HMIN_PROP, \
                        WMIN_STRUC, HMIN_STRUC#, bmp
import constantes

import couleur

from xml.dom.minidom import parse

# Graphiques vectoriels
import draw_cairo_seq, draw_cairo_prj, draw_cairo_prg, draw_cairo
try:
    import wx.lib.wxcairo
    import cairo
    haveCairo = True
except ImportError:
    haveCairo = False


# Widgets partagés
# des widgets wx évolués "faits maison"
# import widgets
from widgets import Variable, VariableCtrl, EVT_VAR_CTRL, VAR_ENTIER_POS, \
                    messageErreur, getNomFichier, pourCent2, RangeSlider, \
                    isstring, \
                    TextCtrl_Help, CloseFenHelp, \
                    messageInfo, rognerImage, \
                    tronquerDC, EllipticStaticText, scaleImage, scaleIcone
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

# Gestion des messages d'erreur
if DEBUG:
    import error



import cStringIO
import  wx.html as  html
import wx.html2 as webview

try: 
    from BeautifulSoup import BeautifulSoup, NavigableString
except ImportError:
    from bs4 import BeautifulSoup, NavigableString
    
import copy
import webbrowser

import threading 

# from pysequence import *
# import pysequence   # déplacé à la fin


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
        self.modif = u""
        self.draw = True
        
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
    def GetDraw(self):
        return self.draw


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
    
    
def Get():
    return
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

def getBitmapFromImageSurface(imagesurface):
    u""" Renvoi une wx.Bitmap en fonction d'une cairo.ImageSurface
    """
    # On fait une copie sinon ça s'efface ...
    return wx.lib.wxcairo.BitmapFromImageSurface(imagesurface).ConvertToImage().ConvertToBitmap()


def getDisplayPosSize():
    u""" Renvoie la position et la taille de l'écran : x, y, w, h
    """
    displays = (wx.Display(i) for i in range(wx.Display.GetCount()))
    sizes = [display.ClientArea for display in displays]
    return sizes[0]



####################################################################################
#
#   Classes pour gérer les boutons de la Toolbar principale
#
####################################################################################
class BoutonToolBar():
    def __init__(self, label, image, shortHelp = u"", longHelp = u""):
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
    def __init__(self, parent, fichier):
        aui.AuiMDIParentFrame.__init__(self, parent, -1, 
                                       version.GetAppnameVersion(), 
                                       style=wx.DEFAULT_FRAME_STYLE)
        
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
            try :
                options.ouvrir(SYSTEM_ENCODING)
            except:
                print u"Fichier d'options corrompus ou inexistant !! Initialisation ..."
                options.defaut()
        else:
            options.defaut()
        self.options = options
#        print options
        
        # On applique les options ...
        self.DefinirOptions(options)
        
        
        
        
        
        
        ##############################################################################################
        # Taille et position de la fenétre
        ##############################################################################################
        x, y, w, h = getDisplayPosSize()
        #print wx.GetDisplaySize()
        
        pos, siz = self.options.optFenetre["Position"], self.options.optFenetre["Taille"]
        
#         print pos, siz
#         print len(pos), len(siz)
#         print x, y, w, h
        
        if len(pos) == 2 \
            and len(siz) == 2 \
            and pos[0] < w \
            and pos[1] < h:
            self.SetPosition(pos)
            self.SetSize(siz)
        else:
            self.SetPosition((w/2, y))
            self.SetSize((w/2,h))
        
        self.SetMinSize((800,570)) # Taille mini d'écran : 800x600
        #self.SetSize((1024,738)) # Taille pour écran 1024x768
        # On centre la fenétre dans l'écran ...
        #self.CentreOnScreen(wx.BOTH)
        
        self.SetIcon(images.getlogoIcon())
        
        
        
        
        nb = self.GetNotebook()
#         self.tabmgr = self.GetClientWindow().GetAuiManager()
        
        nb.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnDocChanged)
        nb.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.OnDocClosed)
        
#         self.tabmgr.GetManagedWindow().Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnDocChanged)
#         self.tabmgr.GetManagedWindow().Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnDocChanged)
        
        file_drop_target = MyFileDropTarget(self)
        nb.SetDropTarget(file_drop_target)
#         self.tabmgr.GetManagedWindow().SetDropTarget(file_drop_target)
        
        
        
        #############################################################################################
        # Quelques variables ...
        #############################################################################################
        self.fichierClasse = u""
        self.pleinEcran = False
        # Element placé dans le "presse papier"
        self.elementCopie = None
        
        
        
        
        # !!! cette ligne pose problème à la fermeture : mystère
        self.renommerWindow()
        
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
        
        self.Bind(EVT_APPEL_OUVRIR, self.OnAppelOuvrir)
        
        
        
        # Interception des frappes clavier
#         self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        
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

        self.Thaw()
        
#     ###############################################################################################
#     def GetNotebook(self):
#         if int(wx.version()[0]) > 2:
#             return self.GetClientWindow().GetAuiManager().GetManagedWindow()
#         else:
#             return self.GetClientWindow().GetAuiManager().GetManagedWindow()
            
             
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
    def GetTools(self, typ):
        if typ == 'prj':
            return [(50 , BoutonToolBar(u"Ajouter un élève",
                                   scaleImage(images.Icone_ajout_eleve.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                   shortHelp = u"Ajout d'un élève au projet", 
                                   longHelp = u"Ajout d'un élève au projet")),
                    
                    (54 , BoutonToolBar(u"Ajouter un groupe d'élèves",
                                   scaleImage(images.Icone_ajout_groupe.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                   shortHelp = u"Ajout d'un groupe d'élèves au projet", 
                                   longHelp = u"Ajout d'un groupe d'élèves au projet")),
                
                    (51 , BoutonToolBar(u"Ajouter un professeur", 
                                       scaleImage(images.Icone_ajout_prof.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                       shortHelp = u"Ajout d'un professeur à l'équipe pédagogique", 
                                       longHelp = u"Ajout d'un professeur à l'équipe pédagogique")),
                    
                    (0, None),
                    
                    (52 , BoutonToolBar(u"Ajouter une tâche", 
                                       scaleImage(images.Icone_ajout_tache.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                       shortHelp=u"Ajout d'une tâche au projet", 
                                       longHelp=u"Ajout d'une tâche au projet")),
                    
                    (53 , BoutonToolBar(u"Ajouter une revue", 
                                       scaleImage(images.Icone_ajout_revue.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                       shortHelp = u"Ajout d'une revue au projet", 
                                       longHelp = u"Ajout d'une revue au projet")),
                    
                    (0, None),
                    
                    (55 , BoutonToolBar(u"Ajouter un modèle", 
                                       scaleImage(images.Icone_ajout_modele.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                       shortHelp = u"Ajout d'un modèle numérique du support", 
                                       longHelp = u"Ajout d'un modèle numérique du support")),
                    
                ]
        
        elif typ == 'seq':
            return [(60 , BoutonToolBar(u"Ajouter une séance", 
                                    scaleImage(images.Icone_ajout_seance.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                    shortHelp=u"Ajout d'une séance dans la séquence", 
                                    longHelp=u"Ajout d'une séance dans la séquence")),
                    
                    (62 , BoutonToolBar(u"Ajouter un professeur", 
                                       scaleImage(images.Icone_ajout_prof.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                       shortHelp = u"Ajout d'un professeur à l'équipe pédagogique", 
                                       longHelp = u"Ajout d'un professeur à l'équipe pédagogique")),
                    
                    (61 , BoutonToolBar(u"Ajouter un système", 
                                       scaleImage(images.Icone_ajout_systeme.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                       shortHelp=u"Ajout d'un système", 
                                       longHelp=u"Ajout d'un système"))
                      ]
            
        elif typ == 'prg':
            return [(70 , BoutonToolBar(u"Actualiser la Progression", 
                                       scaleImage(images.Bouton_Actualiser.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                       shortHelp = u"Actualiser la Progression", 
                                       longHelp = u"Actualiser la Progression")),
                    
                    (0, None),
                    
                    (71 , BoutonToolBar(u"Ajouter un professeur", 
                                       scaleImage(images.Icone_ajout_prof.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                       shortHelp = u"Ajout d'un professeur à l'équipe pédagogique", 
                                       longHelp = u"Ajout d'un professeur à l'équipe pédagogique")),
                    
                    (72 , BoutonToolBar(u"Ajouter une Séquence",
                                   scaleImage(images.Icone_ajout_seq.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                   shortHelp = u"Ajout d'une Séquence à la Progression", 
                                   longHelp = u"Ajout d'une Séquence à la Progression")),
                    
                    (73 , BoutonToolBar(u"Ajouter un Projet",
                                   scaleImage(images.Icone_ajout_prj.GetBitmap(),
                                                  *constantes.IMG_SIZE_TB), 
                                   shortHelp = u"Ajout d'un Projet à la Progression", 
                                   longHelp = u"Ajout d'un Projet à la Progression")),
                    
                  ]
            
            
            
    ###############################################################################################
    def ConstruireTb(self):
        """ Construction de la ToolBar
        """
#        print "ConstruireTb"

        #############################################################################################
        # Création de la barre d'outils
        #############################################################################################
        self.tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        
        
        tsize = constantes.IMG_SIZE_TB
        
        new_bmp =  scaleImage(images.Icone_new.GetBitmap(), *tsize)
        open_bmp = scaleImage(images.Icone_open.GetBitmap(), *tsize)
        save_bmp =  scaleImage(images.Icone_save.GetBitmap(), *tsize)
        saveall_bmp =  scaleImage(images.Icone_saveall.GetBitmap(), *tsize)
        saveas_bmp = scaleImage(images.Icone_saveas.GetBitmap(), *tsize)
        undo_bmp = scaleImage(images.Icone_undo.GetBitmap(), *tsize)
        redo_bmp = scaleImage(images.Icone_redo.GetBitmap(), *tsize)
        full_bmp = scaleImage(images.Icone_fullscreen.GetBitmap(), *tsize)
        
        
#         
#         new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
#         open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
#         save_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
#         saveall_bmp =  images.Icone_saveall.GetBitmap()
#         saveas_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, tsize)
#         undo_bmp = wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, tsize)
#         redo_bmp = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, tsize)
        
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
        
        self.tb.AddLabelTool(14, u"Enregistrer tout", saveall_bmp, 
                             shortHelp=u"Enregistrement de tous les documents sous leurs noms actuels", 
                             longHelp=u"Enregistrement de tous les documents sous leurs noms actuels")
        

        self.tb.AddLabelTool(13, u"Enregistrer sous...", saveas_bmp, 
                             shortHelp=u"Enregistrement du document courant sous un nom différent", 
                             longHelp=u"Enregistrement du document courant sous un nom différent")
        
        self.Bind(wx.EVT_TOOL, self.commandeNouveau, id=10)
        self.Bind(wx.EVT_TOOL, self.commandeOuvrir, id=11)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrer, id=12)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrerSous, id=13)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrerTout, id=14)
        
        
        self.tb.AddSeparator()
        
        self.tb.AddLabelTool(200, u"Annuler", undo_bmp, 
                             shortHelp=u"Annuler", 
                             longHelp=u"Annuler")
        

        self.tb.AddLabelTool(201, u"Rétablir", redo_bmp, 
                             shortHelp=u"Rétablir", 
                             longHelp=u"Rétablir")
        
        
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
            for i, tool in self.GetTools(typ):
                if i > 0:
                    self.tools[typ].append(self.tb.AddLabelTool(i, tool.label, tool.image, 
                                                               shortHelp = tool.shortHelp, 
                                                               longHelp = tool.longHelp))
                else:
                    self.tb.AddSeparator()

        

        self.tb.AddSeparator()
        #################################################################################################################
        #
        # Outils de Visualisation
        #
        #################################################################################################################
        
        self.tb.AddLabelTool(100, u"Plein écran", full_bmp, 
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
        
        self.tb.RemoveTool(70)
        self.tb.RemoveTool(71)
        self.tb.RemoveTool(72)
        self.tb.RemoveTool(73)


    ###############################################################################################
    def ajouterOutils(self, typ):
        self.supprimerOutils()

        d = 8 # Position à changer selon le nombre d'outils "communs"
        for tool in self.tools[typ]:
            self.tb.InsertToolItem(d,tool)
            d += 1
        
        
        self.tb.Realize()


    ###############################################################################################
    def miseAJourUndo(self):
        """ Mise à jour des boutons (et menus)
            après une opération undo ou redo
        """
#        print "miseAJourUndo"
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
            t = u""
        else:
            self.tb.EnableTool(200, True)
            t = u"\n"+undoAction
        self.tb.SetToolShortHelp(200, u"Annuler"+t)

        redoAction = doc.undoStack.getRedoAction()
        if redoAction == None:
            self.tb.EnableTool(201, False)
            t = u""
        else:
            self.tb.EnableTool(201, True)
            t = u"\n"+redoAction
        self.tb.SetToolShortHelp(201, u"Rétablir"+t)
        
        
    ###############################################################################################
    def commandePleinEcran(self, event):
        nb = self.GetNotebook()
        if int(wx.version()[0]) > 2:
            fenDoc = nb.GetCurrentPage()
        else:
            fenDoc = nb.GetPage(nb.GetSelection())
        
        if fenDoc is None:
            return
        
#        if self.GetNotebook().GetCurrentPage() == None:
#            return
        
        self.pleinEcran = not self.pleinEcran
        
        if self.pleinEcran:
            win = fenDoc.nb.GetCurrentPage()
            self.fsframe = wx.Frame(self, -1)
            win.Reparent(self.fsframe)
            win.Bind(wx.EVT_KEY_DOWN, self.OnKey)
            self.fsframe.ShowFullScreen(True, style=wx.FULLSCREEN_ALL)
            
        else:
            win = self.fsframe.GetChildren()[0]
            win.Reparent(fenDoc.nb)
            self.fsframe.Destroy()
            win.SendSizeEventToParent()


    ###############################################################################################
    def CreateMenuBar(self):
        # create menu
        
        window_menu = self.GetWindowMenu()
        window_menu.SetLabel(4001, u"Fermer")
        window_menu.SetLabel(4002, u"Fermer tout")
        window_menu.SetLabel(4003, u"Suivante")
        window_menu.SetLabel(4004, u"Précédente")
        
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
        
        
        
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, u"&Quitter\tCtrl+Q")

        self.file_menu = file_menu
        
        tool_menu = wx.Menu()
        
#        if sys.platform == "win32":
#            tool_menu.Append(18, u"&Générer une Synthése pédagogique\tCtrl+B")
#            tool_menu.AppendSeparator()
        
        if sys.platform == "win32" and util_path.INSTALL_PATH != None:
    #        tool_menu.Append(31, u"Options")
            self.menuReg = tool_menu.Append(32, u"a")
            self.MiseAJourMenu()
        self.menuRep = tool_menu.Append(33, u"Ouvrir et réparer un fichier")
        tool_menu.Append(34, u"Récupérer les noms d'établissement")
        tool_menu.Append(35, u"Récupérer les jours fériés")

        self.tool_menu = tool_menu
        
        help_menu = wx.Menu()
        help_menu.Append(21, u"&Aide en ligne\tF1")
        help_menu.Append(23, u"Envoyer un rapport de &bug")
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
    def OnRecupEtab(self, event):
        dlg = wx.MessageDialog(self, u"Récupérer les noms d'établissement\n\n" \
                               u"L'opération qui va suivre permet de récupérer sur Internet\n" \
                               u"la liste officielle des collèges et lycées Français.\n\n" \
                               u"Cette opération ne se justifie que s'il manque\n" \
                               u"un(des) établissement(s) dans le fichier fourni avec pySéquence.\n\n" \
                               u"Il est conseillé de faire une sauvegarde du fichier\n" \
                               u"\t    etablissements.xml\n"\
                               u"qui sera remplacé par un nouveau.\n\n"\
                               u"L'opération peut durer plusieurs minutes\n" \
                               u"et nécessite une connexion à Internet !!\n\n"\
                               u"Voulez-vous continuer ?",
                                 u"Récupérer les noms d'établissement",
                                 wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                 )
        res = dlg.ShowModal()
        dlg.Destroy() 
        if res == wx.ID_YES:
            import getEtab
            fileName = getEtab.SauvEtablissements(self, util_path.APP_DATA_PATH)
            if fileName is not None:
                dlg = wx.MessageDialog(self, u"Le fichier a bien été enregistré\n\n%s\n\n"\
                                       u"Voulez-vous l'ouvrir ?" %fileName, 
                                       u"Fichier enregistré",
                                       wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL)
                res = dlg.ShowModal()
                if res == wx.ID_YES:
                    try:
                        os.startfile(fileName)
                    except:
                        messageErreur(None, u"Ouverture impossible",
                                      u"Impossible d'ouvrir le fichier\n\n%s\n" %toSystemEncoding(fileName))
            else:
                dlg = wx.MessageDialog(self, u"Opération annulée\n\n", 
                                       u"Opération annulée",
                                       wx.ICON_ERROR | wx.OK)
                res = dlg.ShowModal()
            
            dlg.Destroy()
        
    #############################################################################
    def OnRecupFeries(self, event):
        dlg = wx.MessageDialog(self, u"Récupérer les jours fériés\n\n" \
                               u"L'opération qui va suivre permet de récupérer sur Internet\n" \
                               u"la liste officielle des jours fériés.\n\n" \
                               u"Cette opération ne se justifie qu'une seule fois par an.\n\n" \
                               u"Il est conseillé de faire une sauvegarde du fichier\n" \
                               u"\t    JoursFeries.xml\n"\
                               u"qui sera remplacé par un nouveau.\n\n"\
                               u"L'opération nécessite une connexion à Internet !!\n\n"\
                               u"Voulez-vous continuer ?",
                                 u"Récupérer les jours fériés",
                                 wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                 )
        res = dlg.ShowModal()
        dlg.Destroy() 
        if res == wx.ID_YES:
            import getEtab
            fileName = getEtab.SauvFeries(self, util_path.APP_DATA_PATH)
            if fileName is not None:
                dlg = wx.MessageDialog(self, u"Le fichier a bien été enregistré\n\n%s\n\n"\
                                       u"Voulez-vous l'ouvrir ?" %fileName, 
                                       u"Fichier enregistré",
                                       wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL)
                res = dlg.ShowModal()
                if res == wx.ID_YES:
                    try:
                        os.startfile(fileName)
                    except:
                        messageErreur(None, u"Ouverture impossible",
                                      u"Impossible d'ouvrir le fichier\n\n%s\n" %toSystemEncoding(fileName))
            else:
                dlg = wx.MessageDialog(self, u"Opération annulée\n\n", 
                                       u"Opération annulée",
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
    def OnBug(self, event):
        print
        
        
    #############################################################################
    def OnAide(self, event):
        try:
            webbrowser.open(version.__url__+'/wiki',new=2)
        except:
            messageErreur(None, u"Ouverture impossible",
                          u"Impossible d'ouvrir l'url\n\n%s\n" %toSystemEncoding(self.path))

        
        
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
            elif val == 3:
                ext = 'prg'
            else:
                return
                
        if ext == 'seq':
            child = FenetreSequence(self, ouverture)
            child.SetIcon(scaleIcone(constantes.dicimages["Seq"].GetBitmap()))
        elif ext == 'prj':
            child = FenetreProjet(self)
            child.SetIcon(scaleIcone(constantes.imagesProjet["Prj"].GetBitmap()))
        elif ext == 'prg':
            child = FenetreProgression(self, ouverture)
            child.SetIcon(scaleIcone(constantes.imagesProgression["Prg"].GetBitmap()))
        else:
            child = None
        
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
            
            note : pour l'instant, que pour des Séquences
        """
#         print "ouvrirDoc", nomFichier
        if doc.GetType() == 'seq':
            child = FenetreSequence(self, sequence = doc)
            child.SetIcon(scaleIcone(constantes.dicimages["Seq"].GetBitmap()))
            doc
        elif doc.GetType() == 'prj':
            child = FenetreProjet(self, projet = doc)
            child.SetIcon(scaleIcone(constantes.dicimages["Prj"].GetBitmap()))
        child.finaliserOuverture()
        
        child.definirNomFichierCourant(nomFichier)
        wx.CallAfter(child.Activate)
        self.OnDocChanged()
        return child
    
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
        print "ouvrir", nomFichier, reparer
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
                if ext == "seq":
                    #
                    # On vérifie si la Séquence fait partie d'une Progression ouverte
                    #
                    path2 = os.path.normpath(os.path.abspath(nomFichier))
                    for prog in self.GetDocumentsOuverts('prg'):
                        for lienSeq in prog[0].sequences_projets:
                            path1 = os.path.normpath(os.path.abspath(lienSeq.path))
                            if path1 == path2:  # La séquence fait partie d'une progression ouverte
#                                 print "Dans prog :", path2
                                self.ouvrirDoc(lienSeq.sequence, nomFichier)
                                wx.EndBusyCursor()
                                self.Thaw()
                                return lienSeq.sequence
                
                child = self.commandeNouveau(ext = ext, ouverture = True)
                
                if child != None:
                    doc = child.ouvrir(nomFichier, reparer = reparer)
                
                    
            # Le Fichier est déja ouvert
            else:
                child = self.GetChild(nomFichier)
                texte = constantes.MESSAGE_DEJA[ext] % child.fichierCourant
#                if child.fichierCourant != '':
#                    texte += "\n\n\t"+child.fichierCourant+"\n"
                    
                dialog = wx.MessageDialog(self, texte, 
                                          u"Confirmation", wx.YES_NO | wx.ICON_WARNING)
                retCode = dialog.ShowModal()
                if retCode == wx.ID_YES:
                    doc = child.ouvrir(nomFichier, reparer = reparer)
            

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
                                self, message=u"Ouvrir un fichier pySéquence",
#                                defaultDir = self.DossierSauvegarde, 
                                defaultFile = "",
                                wildcard = mesFormats,
                                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                                )

            if dlg.ShowModal() == wx.ID_OK:
                paths = dlg.GetPaths()
                nomFichier = paths[0]

            else:
                nomFichier = r''
            
            dlg.Destroy()
        
        self.ouvrir(nomFichier, reparer = reparer)
        
        
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
#        print "OnAppelOuvrir"
        wx.CallAfter(self.ouvrir, evt.GetFile())
        
        
    ###############################################################################################
    def AppelOuvrir(self, nomFichier):
        evt = AppelEvent(myEVT_APPEL_OUVRIR, self.GetId())
        evt.SetFile(nomFichier)
        self.GetEventHandler().ProcessEvent(evt)
    
    
    #############################################################################
    def commandeDelete(self, event = None):    
        print "Suppr"
    
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
    
    
    ###############################################################################################
    def OnDocClosed(self, evt = None):   
#         print "OnDocClosed"

        if self.GetNotebook().GetPageCount() <= 1:
            self.supprimerOutils()
            self.tb.Realize()
            
            
    ###############################################################################################
    def OnDocChanged(self, evt = None):
        """ Opérations de modification du menu et des barres d'outils 
            en fonction du type de document en cours
            Et rafraichissement des séquences de la fenêtre de Progression
        """
#         print "OnDocChanged"
        
        fenDoc = self.GetCurrentPage()
        
        if hasattr(fenDoc, 'typ'):
            self.ajouterOutils(fenDoc.typ )
            if fenDoc.typ == "prj":
                self.Bind(wx.EVT_TOOL, fenDoc.projet.AjouterEleve,      id=50)
                self.Bind(wx.EVT_TOOL, fenDoc.projet.AjouterProf,       id=51)
                self.Bind(wx.EVT_TOOL, fenDoc.AjouterTache,             id=52)
                self.Bind(wx.EVT_TOOL, fenDoc.projet.InsererRevue,      id=53)
                self.Bind(wx.EVT_TOOL, fenDoc.projet.AjouterGroupe,      id=54)
                self.Bind(wx.EVT_TOOL, fenDoc.projet.support.AjouterModele,      id=55)
                
            elif fenDoc.typ == "seq":
                self.Bind(wx.EVT_TOOL, fenDoc.sequence.AjouterSeance,   id=60)
                self.Bind(wx.EVT_TOOL, fenDoc.sequence.AjouterSysteme,  id=61)
                self.Bind(wx.EVT_TOOL, fenDoc.sequence.AjouterProf,     id=62)
                
            elif fenDoc.typ == "prg":
                self.Bind(wx.EVT_TOOL, fenDoc.progression.Rafraichir,     id=70)
                self.Bind(wx.EVT_TOOL, fenDoc.progression.AjouterProf,    id=71)
                self.Bind(wx.EVT_TOOL, fenDoc.progression.AjouterNouvelleSequence,     id=72)
                self.Bind(wx.EVT_TOOL, fenDoc.progression.AjouterNouveauProjet,     id=73)
    
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
                
            fenDoc.Rafraichir()
        
        else:
            self.supprimerOutils()
            self.tb.Realize()
            
        self.miseAJourUndo()


    ###############################################################################################
    def OnKey(self, evt):
        keycode = evt.GetKeyCode()
#         print "!!", keycode
        if keycode == wx.WXK_ESCAPE and self.pleinEcran:
            self.commandePleinEcran(evt)
              
        elif evt.ControlDown() and keycode == 90: # Ctrl-Z
            self.commandeUndo(evt)
  
        elif evt.ControlDown() and keycode == 89: # Ctrl-Y
            self.commandeRedo(evt)
              
        elif keycode == 46: # Suppr
            self.commandeDelete(evt)
              
        evt.Skip()
    
                
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
        if self.GetNotebook() != None and self.GetNotebook().GetCurrentPage() != None:
            return self.GetNotebook().GetCurrentPage().GetDocument()
    
    
    #############################################################################
    def HideTip(self, event = None):
        print "HideTip principal"
        self.GetDocActif().HideTip()
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
    
    
    #############################################################################
    def OnClose(self, evt):
#        print "OnClose"
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
#        
        
        
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
            sys.exit()
#            self.Destroy()



########################################################################################
#
#
#  Gestion des drag & drop de fichiers
#     pour ouverture ...
#
#
########################################################################################
class MyFileDropTarget(wx.FileDropTarget):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, window):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.window = window
 
    #----------------------------------------------------------------------
    def OnDropFiles(self, x, y, filenames):
        """
        When files are dropped, update the display
        """
        self.window.dropFiles(filenames)


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
        self.fichierCourant = u""
        self.DossierSauvegarde = u""
        self.fichierCourantModifie = False
            
        #
        # Un NoteBook comme conteneur de la fiche
        #
        self.nb = wx.Notebook(self.pnl, -1)


    ###############################################################################################
    def GetDocument(self):
        return


    #########################################################################################################
    def HideTip(self, event = None):
        print "HideTip document"
        self.GetDocument().HideTip()
        
        
    #########################################################################################################
    def GetPanelProp(self):
        return self.panelProp.panel

    #########################################################################################################
    def sendEvent(self, doc = None, modif = u"", draw = True, obj = None):
#        print "sendEvent", modif
        self.eventAttente = False
        evt = SeqEvent(myEVT_DOC_MODIFIED, self.GetId())
        if doc != None:
            evt.SetDocument(doc)
        else:
            evt.SetDocument(self.GetDocument())
        
        if modif != u"":
            evt.SetModif(modif)
            
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
#                         Floatable(False).
                         BestSize((WMIN_STRUC, HMIN_STRUC)).
                         MinSize((WMIN_STRUC, -1)).
                         Dockable(True).
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
                         BestSize((WMIN_PROP, HMIN_PROP)).
                         MinSize((WMIN_PROP, HMIN_PROP)).
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

        self.definirNomFichierCourant(r'')
    
        sizer = wx.BoxSizer()
        sizer.Add(self.pnl, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Layout()
        
        self.Bind(EVT_DOC_MODIFIED, self.OnDocModified)
        self.Bind(wx.EVT_CLOSE, self.quitter)
        for c in self.GetChildren():
            c.Bind(wx.EVT_LEAVE_WINDOW, self.HideTip)
        

    #############################################################################
    def fermer(self):
        # Pour mettre à jour la barre d'outils
        self.parent.OnDocClosed()
        
        self.mgr.UnInit()
        del self.mgr
        try:
            self.Destroy()
        except:
            pass
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
                            defaultDir=toSystemEncoding(self.DossierSauvegarde) , # encodage?
                            defaultFile="", wildcard=mesFormats, 
                            style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR
                            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
            self.enregistrer(path)
            self.DossierSauvegarde = os.path.split(path)[0]
            return path
        else:
            dlg.Destroy()
    
    
    #############################################################################
    def commandeRedo(self, event = None):
        wx.BeginBusyCursor()
        self.GetDocument().undoStack.setOnUndoRedo()
        self.GetDocument().classe.undoStack.setOnUndoRedo()
        
        self.GetDocument().undoStack.redo()
        self.GetDocument().classe.undoStack.redo()
        
        
        self.restaurer()
        
        self.GetDocument().undoStack.resetOnUndoRedo()
        self.GetDocument().classe.undoStack.resetOnUndoRedo()
        
        wx.EndBusyCursor()
        
    #############################################################################
    def commandeUndo(self, event = None):
        wx.BeginBusyCursor()
        self.GetDocument().undoStack.setOnUndoRedo()
        self.GetDocument().classe.undoStack.setOnUndoRedo()
#        t0 = time.time()
        self.GetDocument().undoStack.undo()
#        t1 = time.time()
#        print "  ", t1-t0
        
        self.GetDocument().classe.undoStack.undo()
#        t2 = time.time()
#        print "  ", t2-t1
        
        self.restaurer()
        self.GetDocument().undoStack.resetOnUndoRedo()
        self.GetDocument().classe.undoStack.resetOnUndoRedo()
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
        try:
            t = REFERENTIELS[self.classe.typeEnseignement].Enseignement[0]
        except:
            t = u"???"

        if self.fichierCourant == '':
            t += u" - "+constantes.TITRE_DEFAUT[self.typ]
        else:
            t += u" - "+os.path.splitext(os.path.basename(toSystemEncoding(self.fichierCourant)))[0]
        
        if modif is None:
            modif = self.fichierCourantModifie
            
        if modif :
            t += " **"
        self.SetTitle(t)


    #############################################################################
    def exporterFichePDF(self, nomFichier, pourDossierValidation = False):
        # Le décodage/réencodage est obligatoire sous peine de crash !!
        try:
            PDFsurface = cairo.PDFSurface(nomFichier.decode(SYSTEM_ENCODING).encode(FILE_ENCODING), 595, 842)
        except IOError:
            Dialog_ErreurAccesFichier(nomFichier)
            wx.EndBusyCursor()
            return

        ctx = cairo.Context(PDFsurface)
        ctx.scale(820 / draw_cairo.COEF, 820/ draw_cairo.COEF) 
        if self.typ == 'seq':
            draw_cairo_seq.Draw(ctx, self.sequence)
        elif self.typ == 'prj':
            draw_cairo_prj.Draw(ctx, self.projet, pourDossierValidation = pourDossierValidation)
        elif self.typ == 'prg':
            draw_cairo_prg.Draw(ctx, self.progression)
        
        PDFsurface.finish()
        
    
    #############################################################################
    def exporterFiche(self, event = None):
        mesFormats = "pdf (.pdf)|*.pdf|" \
                     "svg (.svg)|*.svg"
#                     "swf (.swf)|*.swf"
        dlg = wx.FileDialog(
            self, message=u"Enregistrer la fiche sous ...", 
            defaultDir=toSystemEncoding(self.DossierSauvegarde) , 
            defaultFile = os.path.splitext(self.fichierCourant)[0]+".pdf", 
            wildcard=mesFormats, style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR
            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()#.encode(FILE_ENCODING)
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
                ctx.scale(820/ draw_cairo.COEF, 820/ draw_cairo.COEF) 
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
            for e in self.projet.eleves:
                win = FrameRapport(self, self.fichierCourant, self.projet, 'prj', e)
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
                if event is not None: event.Skip()
                return self.fermer()
    
            elif retCode == wx.ID_NO:
                if event is not None: event.Skip()
                return self.fermer()
                 
            else:
                return False
        
        else:            
            if event is not None: event.Skip()
            return self.fermer()


    #############################################################################
    def enrichirSVG(self, path):
        """Enrichissement de l'image SVG <path> avec :
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
        
        # Récupération des points caractéristiques sur la fiche
        pts_caract = self.GetDocument().GetPtCaract()
#        if self.typ == 'seq':
#            pts_caract = self.sequence.GetPtCaract()
#        else:
#            pts_caract = self.projet.GetPtCaract()
        
        # Identification des items correspondants sur le doc SVG
        for p in doc.getElementsByTagName("path"):
            a = p.getAttribute("d")
            a = str(a).translate(None, 'MCLZ')  # Supprime les  lettres
            l = a.split()
            if len(l) > 1:      # On récupére le premier point du <path>
                x, y = l[0], l[1]
                x, y = float(x), float(y)
                
                for pt, obj, flag in pts_caract:
                    if match((x, y), pt) :
                        obj.cadre.append((p, flag))
                        if type(flag) != str:
                            break 
        
        # On lance la procédure d'enrichissement ...
        self.GetDocument().EnrichiSVGdoc(doc)
#        if self.typ == 'seq':
#            self.sequence.EnrichiSVG(doc)
#        elif self.typ == 'prj':
#            self.projet.EnrichiObjetsSVG(doc)
            
        doc.writexml(f, '   ', encoding = "utf-8")
        f.close

    #############################################################################
    def definirNomFichierCourant(self, nomFichier = r''):
        u"""Modification du nom du fichier courant
            :param nomFichier: encodé en FileEncoding
        """
        self.fichierCourant = nomFichier
        self.GetDocument().SetPath(nomFichier)
        self.SetTitre()



 
def Dialog_ErreurAccesFichier(nomFichier):
    messageErreur(None, u'Erreur !',
                  u"Impossible d'accéder en écriture au fichier\n\n%s" %toSystemEncoding(nomFichier))


########################################################################################
#
#
#  Classe définissant la fenétre "Séquence"
#
#
########################################################################################
class FenetreSequence(FenetreDocument):
    u"""Classe définissant la fenêtre d'une Séquence

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
        self.arbre.ExpandAll()
        
        #
        # Permet d'ajouter automatiquement les systèmes des préférences (dans la Classe)
        #
        self.sequence.Initialise()
       
        #
        # Zone graphique de la fiche de séquence (au centre)
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
        self.fiche.Redessiner()


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
#         print "OnDocModified", event.GetModif()
        if event.GetModif() != u"":
            
            self.classe.undoStack.do(event.GetModif())
            self.sequence.undoStack.do(event.GetModif())
        
        if event.GetDocument() == self.sequence:
            self.sequence.VerifPb()
            if event.GetDraw():
                wx.CallAfter(self.fiche.Redessiner)
            self.MarquerFichierCourantModifie()
            
        elif event.GetDocument() == self.classe:
            self.sequence.VerifPb()
            if event.GetDraw():
                wx.CallAfter(self.fiche.Redessiner)
            self.MarquerFichierCourantModifie()
        
        self.parent.miseAJourUndo()
        
        
    ###############################################################################################
    def enregistrer(self, nomFichier):
        u"""Enregistrement
            :param nomFichier: encodé en FileEncoding
        """
        wx.BeginBusyCursor()
        
        self.sequence.enregistrer(nomFichier)

        self.definirNomFichierCourant(nomFichier)
        self.MarquerFichierCourantModifie(False)
        
        wx.EndBusyCursor()
        
        
    ###############################################################################################
    def VerifierReparation(self):
        """Vérification (et correction) de la compatibilité de la séquence avec la classe
            aprés une ouverture avec réparation
        """
#        print "VerifierReparation", self.sequence.CI.numCI, self.sequence.GetReferentiel().CentresInterets
        for ci in self.sequence.CI.numCI:
            if ci >= len(self.sequence.GetReferentiel().CentresInterets):
                self.sequence.CI.numCI.remove(ci)
                messageErreur(self,u"CI inexistant",
                              u"Pas de CI numéro " + str(ci) + " !\n\n" \
                              u"La séquence ouverte fait référence à un Centre d'Intérét\n" \
                              u"qui n'existe pas dans le référentiel par défaut.\n\n" \
                              u"Il a été supprimé !")
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

        
        self.arbre.SelectItem(self.classe.branche)

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        
        self.fiche.Redessiner()

        self.parent.miseAJourUndo()
        
        
    ###############################################################################################
    def finaliserOuverture(self):
        self.arbre.DeleteAllItems()
        root = self.arbre.AddRoot("")
        self.classe.ConstruireArbre(self.arbre, root)
        self.sequence.ConstruireArbre(self.arbre, root)
        self.sequence.CI.SetNum()
        self.sequence.SetCodes()
        self.sequence.PubDescription()
        self.sequence.SetLiens()
        self.sequence.VerifPb()
        self.sequence.MiseAJourTypeEnseignement()
        self.sequence.Verrouiller()
        self.arbre.ExpandAll()
        self.arbre.SelectItem(self.classe.branche)
        
        
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True, reparer = False):
        u"""Ouverture
            :param nomFichier: encodé en FileEncoding
        """
        print "ouvrir sequence", nomFichier
        if not os.path.isfile(nomFichier):
            return
        
        fichier = open(nomFichier,'r')
        self.definirNomFichierCourant(nomFichier)
    
        ###############################################################################################################
        def ouvre():
            root = ET.parse(fichier).getroot()
            
            # La séquence
            sequence = root.find("Sequence")
            if sequence == None: # Ancienne version , forcément STI2D-ETT !!
#                self.classe.GetPanelPropriete().EvtRadioBox(CodeFam = ('ET', 'STI'))
                self.sequence.setBranche(root)
            else:
                # La classe
                classe = root.find("Classe")
                self.classe.setBranche(classe, reparer = reparer)
                self.sequence.MiseAJourTypeEnseignement()
                self.sequence.setBranche(sequence)  

            if reparer:
                self.VerifierReparation()
            
            self.finaliserOuverture()
           


        ###############################################################################################################
        ###############################################################################################################
        
        
        if "beta" in version.__version__:
            ouvre()
        else:
            try:
                ouvre()
            except:
                messageErreur(self, u"Erreur d'ouverture",
                              u"La séquence pédagogique\n    %s\n n'a pas pu étre ouverte !" %nomCourt(nomFichier))
                fichier.close()
                self.Close()
                return

#        self.arbre.Layout()
#        self.arbre.ExpandAll()
#        self.arbre.CalculatePositions()
#        self.arbre.SelectItem(self.arbre.classe.branche)
        
        fichier.close()
        
        
        
        if redessiner:
            wx.CallAfter(self.fiche.Redessiner)

        self.classe.undoStack.do(u"Ouverture de la Classe")
        self.sequence.undoStack.do(u"Ouverture de la Séquence")
        self.parent.miseAJourUndo()
        
       
        
        return self.sequence
        

    #############################################################################
    def definirNomFichierCourant(self, nomFichier = r''):
        u"""Modification du nom du fichier courant
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
    u"""
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
            self.projet.MiseAJourTypeEnseignement()
        
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
        self.nb.AddPage(self.fiche, u"Fiche Projet")
        
        #
        # Détails
        #
#         self.pageDetails = RapportRTF(self.nb, rt.RE_READONLY)
        self.pageDetails = Panel_Details(self.nb)
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
        self.fiche.Redessiner()
        
        wx.CallAfter(self.Thaw)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
        
    


    ###############################################################################################
    def ajouterOutils(self):
        u"""Ajoute à la toolbar les outils spécifiques aux Projets
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
    def OnPageChanged(self, event):
        new = event.GetSelection()
        event.Skip()
        if new == 1: # On vient de cliquer sur la page "détails"
            self.pageDetails.Construire(self.fichierCourant, self.projet, self.typ)
#             self.pageDetails.Remplir(self.fichierCourant, self.projet, self.typ)
        
        elif new == 2: # On vient de cliquer sur la page "dossier de validation"
            self.pageValid.MiseAJour(self.projet, self)
            
        elif new == 3: # On vient de cliquer sur la page "Bulletins Officiels"
            self.pageBO.Construire(REFERENTIELS[self.projet.classe.typeEnseignement])

        elif new == 0: # On vient de cliquer sur la fiche
            self.fiche.Redessiner()
            
            
    ###############################################################################################
    def OnDocModified(self, event):
        if event.GetModif() != u"":
#             print "OnDocModified", event.GetModif()
            self.classe.undoStack.do(event.GetModif())
            self.projet.undoStack.do(event.GetModif())
            
        if event.GetDocument() == self.projet:
            self.projet.VerifPb()
            self.projet.SetCompetencesRevuesSoutenance(miseAJourPanel = False)
            if event.GetDraw():
                wx.CallAfter(self.fiche.Redessiner)

            self.MarquerFichierCourantModifie()
        
        elif event.GetDocument() == self.classe:
            self.MarquerFichierCourantModifie()
            
        self.parent.miseAJourUndo()
        
        
    ###############################################################################################
    def enregistrer(self, nomFichier):
        u"""Enregistrement
            :param nomFichier: encodé en FileEncoding
        """
        wx.BeginBusyCursor()
        
        self.projet.enregistrer(nomFichier)
        
        self.definirNomFichierCourant(nomFichier)
        self.MarquerFichierCourantModifie(False)
        wx.EndBusyCursor()
        
        
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

        self.projet.PubDescription()
  
        self.projet.MiseAJourDureeEleves()

        self.projet.MiseAJourNomProfs()

        self.projet.Verrouiller()
        
        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        
#        self.fiche.Redessiner()

        self.parent.miseAJourUndo()

    
    ###############################################################################################
    def finaliserOuverture(self, dlg = None, message = "", count = 0):
        self.arbre.DeleteAllItems()
        root = self.arbre.AddRoot("")
        
        
        liste_actions = [[self.classe.ConstruireArbre, [self.arbre, root], {},
                         u"Construction de l'arborescence de la classe...\t"],
                         [self.projet.ConstruireArbre, [self.arbre, root], {},
                          u"Construction de l'arborescence du projet...\t"],
                         [self.projet.OrdonnerTaches, [], {},
                          u"Ordonnancement des tâches...\t"],
                         [self.projet.MiseAJour, [], {},
                          u"Mise à jour diverses...\t"],
#                         [self.projet.PubDescription, [], {},
#                          u"Traitement des descriptions...\t"],
                         [self.projet.SetLiens, [], {},
                          u"Construction des liens...\t"],
                         [self.projet.MiseAJourDureeEleves, [], {},
                          u"Ajout des durées/évaluabilités dans l'arbre...\t"],
                         [self.projet.MiseAJourNomProfs, [], {},
                          u"Ajout des disciplines dans l'arbre...\t"],
                         ]
        
        for fct, arg, karg, msg in liste_actions:
            message += msg
            if dlg is not None:
                dlg.Update(count, message)
            count += 1
            if "beta" in version.__version__:
                fct(*arg, **karg)
                message += u"Ok\n"
            
            else:
                try :
                    fct(*arg, **karg)
                    message += u"Ok\n"
                except:
#                     Ok = False
                    message += constantes.Erreur(constantes.ERR_INCONNUE).getMessage() + u"\n"
                    
        self.projet.Verrouiller()
        self.projet.VerifierVersionGrilles()

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        self.arbre.SelectItem(self.arbre.classe.branche)
        
        return message, count
    
    
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True, reparer = False):
        u"""Ouverture
            :param nomFichier: encodé en FileEncoding
        """
        print "Ouverture projet", nomFichier
        tps1 = time.clock()
        Ok = True
        Annuler = False
        nbr_etapes = 10
        
        # Pour le suivi de l'ouverture
        nomCourt = toSystemEncoding(os.path.splitext(os.path.split(nomFichier)[1])[0])
        
        message = nomCourt+"\n\n"
        dlg = myProgressDialog(u"Ouverture d'un projet",
                                   message,
                                   nbr_etapes,
                                   wx.GetTopLevelParent(self))
        
#         self.fiche.Hide()
        
        fichier = open(nomFichier,'r')
        self.definirNomFichierCourant(nomFichier)
    
        #################################################################################################
        def get_err_message(err):
            return (u"\n  "+CHAR_POINT).join([e.getMessage() for e in err])
        
        
        #################################################################################################
        def ouvre(fichier, message):
            try:
                root = ET.parse(fichier).getroot()
            except ET.ParseError:
                messageErreur(wx.GetTopLevelParent(self), u"Fichier corrompu", 
                                  u"Le fichier suivant est corrompu !!\n\n"\
                                  u"%s\n\n" \
                                  u"Il est probablement tronqué suite à un echec d'enregistrement." %toSystemEncoding(nomFichier))
                Annuler = True
                return None, u"", 0, False, Annuler
             
            count = 1
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
#                dlg.top()
                count += 1
                classe = root.find("Classe")
                err = self.classe.setBranche(classe, reparer = reparer)
                if len(err) > 0 :
                    Ok = False
                    message += get_err_message(err) 
                message += u"\n"
                
#                print "V",self.classe.GetVersionNum()
                if self.classe.GetVersionNum() < 5:
                    messageInfo(None, u"Ancien programme", 
                                  u"Projet enregistré avec les indicateurs de compétence antérieurs à la session 2014\n\n"\
                                  u"Les indicateurs de compétence ne seront pas chargés.")
                
                # Le projet
                message += u"Construction de la structure du projet...\t"
#                dlg.top()
                dlg.Update(count, message)
                
                count += 1
                
                self.projet.code = self.projet.GetReferentiel().getCodeProjetDefaut()
                
                # Derniére vérification
                if self.projet.GetProjetRef() == None:
                    print u"Pas bon référentiel"
                    self.classe.setBranche(classe, reparer = True)
                
                err = self.projet.setBranche(projet)
                
                if len(err) > 0 :
                    Ok = False
                    message += get_err_message(err)
                message += u"\n"
                
            
                        
            return root, message, count, Ok, Annuler
        
        
        #################################################################################################
        def annuleTout(message):
            message += u"\n\nLe projet n'a pas pu être ouvert !\n\n"
            if len(err) > 0:
                message += u"\n   L'erreur concerne :"
                message += get_err_message(err)
            fichier.close()
            self.Close()
            count = nbr_etapes
#            dlg.UpdateWindowUI()
##            wx.GetTopLevelParent(self).SetFocus()
#            dlg.top()
            dlg.Update(count, message)
            
#            dlg.Raise()
            wx.CallAfter(dlg.Destroy)
#            wx.CallAfter(self.fiche.Show)
#            wx.CallAfter(self.fiche.Redessiner)
            return
        
        
        
        ################################################################################################
        if "beta" in version.__version__:
            print "beta"
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
            annuleTout(message)
            return
        
        fichier.close()
        
        if "beta" in version.__version__:
            message, count = self.finaliserOuverture(dlg= dlg, message = message, count = count)
        else:
            try:
                message, count = self.finaliserOuverture(dlg= dlg, message = message, count = count)
            except:
                annuleTout(message)
                return
            

#        self.projet.Verrouiller()

        message += u"Tracé de la fiche...\t"
        dlg.Update(count, message)
#        dlg.top()
        count += 1

#        self.arbre.SelectItem(self.classe.branche)

#        self.arbre.Layout()
#        self.arbre.ExpandAll()
#        self.arbre.CalculatePositions()
#        self.arbre.SelectItem(self.arbre.classe.branche)
        
        
    
        #
        # Vérification de la version des grilles
        #
#        self.projet.VerifierVersionGrilles()
        
        tps2 = time.clock() 
        print "Ouverture :", tps2 - tps1

        self.fiche.Redessiner()

        if Ok:
            
            dlg.Destroy()
        else:
            dlg.Update(nbr_etapes, message)
#            dlg.top()
            dlg.Close() 
    
#        self.SetTitre()
#         wx.CallAfter(self.fiche.Show)
#         wx.CallAfter(self.fiche.Redessiner)
        

        #
        # Mise en liste undo/redo
        #
        self.classe.undoStack.do(u"Ouverture de la Classe")
        self.projet.undoStack.do(u"Ouverture du Projet")
        self.parent.miseAJourUndo()
        
        return self.projet


    #############################################################################
    def genererGrilles(self, event = None):
        u""" Génération de toutes les grilles d'évaluation
             - demande d'un dossier -

            :return: la liste des codes d'erreur
            :rtype: list
        """
        log = []
        
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
                log.extend(e.GenererGrille(nomFichiers = nomFichiers[e.id], messageFin = False))
                dlgb.Update(count, u"Traitement de la grille de \n\n"+e.GetNomPrenom())
                dlgb.Refresh()
                count += 1
                dlgb.Refresh()
           
            t = u"Génération des grilles terminée "
            if len(log) == 0:
                t += u"avec succès !\n\n"
            else:
                t += u"avec des erreurs :\n\n"
                t += u"\n".join(log)
            
            t += "\n\nDossier des grilles :\n" + path
            dlgb.Update(count, t)
            dlgb.Destroy() 
                
                
        else:
            dlg.Destroy()
        
        return list(set(log))
    
    
            
    #############################################################################
    def genererGrillesPdf(self, event = None):
        u""" Génération de TOUTES les grilles d'évaluation au format pdf
            demande d'un nom de fichier -
        """
        mesFormats = u"PDF (.pdf)|*.pdf"
        nomFichier = getNomFichier("Grilles", self.projet.intitule[:20], u".pdf")
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
            dlgb = myProgressDialog(u"Génération des grilles",
                                        u"",
                                        maximum = len(self.projet.eleves)+1,
                                        parent=self
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
            
            
            count = 1
            
            pathprj = self.projet.GetPath()
#            print "pathprj", pathprj
            
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
#            print "nomFichiers grille", nomFichiers
            
            # Si des fichiers existent avec le méme nom, on demande si on peut les écraser
            if not self.projet.TesterExistanceGrilles(nomFichiers):
                dlgb.Destroy()
                return
            
#            dlgb.top()
            
            
#            dicInfo = self.projet.GetProjetRef().cellulesInfo
#            classNON = dicInfo["NON"][0][0]
#            feuilNON = dicInfo["NON"][0][1]
#            collectif = self.projet.GetProjetRef().grilles[classNON][1] == 'C'
            
            # Elaboration de la liste des fichiers/feuilles à exporter en PDF
            lst_grilles = []
            for e in self.projet.eleves:
                dlgb.Update(count, u"Traitement de la grille de \n\n"+e.GetNomPrenom())
#                dlgb.top()
#                 dlgb.Refresh()
                    
                if e.id in nomFichiers.keys():
                    e.GenererGrille(nomFichiers = nomFichiers[e.id], messageFin = False)

                for k, g in e.grille.items():
#                    grille = os.path.join(toFileEncoding(pathprj), toFileEncoding(g.path))
                    grille = os.path.join(pathprj, g.path)
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
#                 dlgb.Refresh()
            
            dlgb.Update(count, u"Compilation des grilles ...\n\n")
#            dlgb.top()
#             count += 1
#             dlgb.Refresh()
                
            genpdf.genererGrillePDF(nomFichier, lst_grilles)
            
            dlgb.Update(count, u"Les grilles ont été créées avec succés dans le fichier :\n\n"+nomFichier)
#            dlgb.top()
            try:
                os.startfile(nomFichier)
            except:
                pass
            
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
        
        mesFormats = u"PDF (.pdf)|*.pdf"
        nomFichier = getNomFichier("FicheValidation", self.projet.intitule[:20], u".pdf")
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
                                  u" - qu'aucun fichier portant le méme nom n'est déja ouvert\n" \
                                  u" - que le dossier choisi n'est pas protégé en écriture\n\n" \
                                  + nomFichier)
                wx.EndBusyCursor()
            
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

########################################################################################
#
#
#  Classe définissant la fenétre "Séquence"
#
#
########################################################################################
class FenetreProgression(FenetreDocument):
    u"""
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
        self.arbre.SelectItem(self.classe.branche)
        self.arbre.ExpandAll()
        
        #
        # Zone graphique de la fiche de projet
        #
        self.fiche = FicheProgression(self.nb, self.progression)       
#        self.thread = ThreadRedess(self.fichePrj)
        self.nb.AddPage(self.fiche, u"Fiche Progression")
        
        #
        # Xmind
        #
        self.pageXmind = wx.Panel(self.nb, -1)
        self.nb.AddPage(self.pageXmind, u"Carte mentale")
        
        #
        # Bulletins Officiels
        #
        self.pageBO = Panel_BO(self.nb)
        self.nb.AddPage(self.pageBO, u"Bulletins Officiels")
        
        
        #
        # html
        #
        
#        self.pageHTML = html.HtmlWindow(self.nb, -1, size = (100,100),style=wx.NO_FULL_REPAINT_ON_RESIZE|html.HW_SCROLLBAR_NEVER)
#        self.pageHTML.SetPage("""<!DOCTYPE html>
#<html>
#<body>
#
#<canvas id="myCanvas" width="200" height="100" style="border:1px solid #000000;">
#Your browser does not support the HTML5 canvas tag.
#</canvas>
#
#</body>
#</html>""")
#        self.nb.AddPage(self.pageHTML, u"HTML")
        
        self.miseEnPlace()
        
        self.fiche.Redessiner()
        
        wx.CallAfter(self.Thaw)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)


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
            self.pageBO.Construire(REFERENTIELS[self.progression.classe.typeEnseignement])

        elif new == 0: # On vient de cliquer sur la fiche
            self.fiche.Redessiner()
            
    ###############################################################################################
    def OnDocModified(self, event):
        if event.GetModif() != u"":
#            print "OnDocModified", event.GetModif()
            self.classe.undoStack.do(event.GetModif())
            self.progression.undoStack.do(event.GetModif())
        
        if event.GetDocument() == self.progression:
            self.progression.VerifPb()
            if event.GetDraw():
                wx.CallAfter(self.fiche.Redessiner)
            self.MarquerFichierCourantModifie()
            
        elif event.GetDocument() == self.classe:
            self.progression.VerifPb()
            if event.GetDraw():
                wx.CallAfter(self.fiche.Redessiner)
            self.MarquerFichierCourantModifie()
        
        self.parent.miseAJourUndo()

   
    


    ###############################################################################################
    def ProposerEnregistrer(self, doc, pathProg):
        wx.BeginBusyCursor()
        if doc.GetType() == 'seq':
            t = u"La %s sera engegistrée" %doc.nom_obj
            n = u"nouvelle"
            e = '.seq'
        elif doc.GetType() == 'prj':
            t = u"Le %s sera engegistré" %doc.nom_obj
            n = u"nouveau"
            e = '.prj'
        dlg = wx.TextEntryDialog(self, u"Nom du fichier %s\n\n"\
                                 u"%s dans le dossier de la Progression :\n" %(doc.nom_obj, t) + toSystemEncoding(pathProg),
                                 u"Enregistrement %s %s" %(doc.article_c_obj,doc.nom_obj) , u"")

        if dlg.ShowModal() == wx.ID_OK:
            nomFichier = dlg.GetValue()
            dlg.Destroy()
            nomFichier = os.path.splitext(os.path.basename(nomFichier))[0]+e
            nomFichier = os.path.join(pathProg, nomFichier)
            
            if os.path.isfile(nomFichier):
                dlg = wx.MessageDialog(self, u"Un fichier %s portant ce nom existe déja.\n\n"\
                                             u"Voulez-vous :\n"\
                                             u" - l'ouvrir comme %s %s de la Progression : OUI\n"\
                                             u" - écraser le fichier existant (toutes les données seront perdues) : NON\n"\
                                             u" - choisir un autre nom pour la %s : ANNULER" %(doc.nom_obj, n, doc.nom_obj, doc.nom_obj),
                                       u"%s existante" %doc.nom_obj,
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
            pysequence.enregistrer_root(root, nomFichier)
            
            wx.EndBusyCursor()
            return 0, path
        
        else:
            dlg.Destroy()
        
        wx.EndBusyCursor()
        return 3, ""
        
        
    ###############################################################################################
    def enregistrer(self, nomFichier):
        u""" Enregistrement
            :param nomFichier: encodé en FileEncoding
        """
        wx.BeginBusyCursor()
        
        self.progression.enregistrer(nomFichier)
        
        self.definirNomFichierCourant(nomFichier)
        self.MarquerFichierCourantModifie(False)
        wx.EndBusyCursor()
        
        
    ###############################################################################################
    def ouvrir(self, nomFichier, redessiner = True, reparer = False):
        """ <nomFichier> encodé en FileEncoding
        """
        print "Ouverture progression", nomFichier
        tps1 = time.clock()
        Ok = True
        Annuler = False
        nbr_etapes = 8
        
        # Pour le suivi de l'ouverture
        message = nomCourt(nomFichier)+"\n\n"
        dlg = myProgressDialog(u"Ouverture d'une progression",
                                   message,
                                   nbr_etapes,
                                   wx.GetTopLevelParent(self))
        
        self.fiche.Hide()
        
        fichier = open(nomFichier,'r')
        self.definirNomFichierCourant(nomFichier)
        
    
        #################################################################################################
        def get_err_message(err):
            return (u"\n  "+CHAR_POINT).join([e.getMessage() for e in err])
        
        
        #################################################################################################
        def ouvre(fichier, message):
            try:
                root = ET.parse(fichier).getroot()
            except ET.ParseError:
                messageErreur(wx.GetTopLevelParent(self), u"Fichier corrompu", 
                                  u"Le fichier suivant est corrompu !!\n\n"\
                                  u"%s\n\n" \
                                  u"Il est probablement tronqué suite à un echec d'enregistrement." %toSystemEncoding(nomFichier))
                Annuler = True
                return None, u"", 0, False, Annuler
             
            count = 0
            Ok = True
            Annuler = False
                   
            # La progression
            progression = root.find("Progression")
            if progression == None:
                self.progression.setBranche(root)
            else:
                # La classe
                message += u"Construction de la structure de la classe...\t"
                dlg.Update(count, message)
#                dlg.top()
                count += 1
                classe = root.find("Classe")
                err = self.classe.setBranche(classe, reparer = reparer)
                if len(err) > 0 :
                    Ok = False
                    message += get_err_message(err) 
                message += u"\n"
                
                
                # La progression
                message += u"Construction de la structure de la progression...\t"
#                dlg.top()
                dlg.Update(count, message)
                count += 1
                
                err = self.progression.setBranche(progression)
                self.progression.MiseAJourTypeEnseignement()
                
                if len(err) > 0 :
                    Ok = False
                    message += get_err_message(err)
                message += u"\n"
                
            self.arbre.DeleteAllItems()
            root = self.arbre.AddRoot("")
            
            return root, message, count, Ok, Annuler


        ################################################################################################
        if "beta" in version.__version__:
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
            message += u"\n\nLa progression n'a pas pu être ouverte !\n\n"
            if len(err) > 0:
                message += u"\n   L'erreur concerne :"
                message += get_err_message(err)
            fichier.close()
            self.Close()
            count = nbr_etapes
#            dlg.UpdateWindowUI()
##            wx.GetTopLevelParent(self).SetFocus()
#            dlg.top()
            dlg.Update(count, message)
            
#            dlg.Raise()
            wx.CallAfter(dlg.Destroy)
#            wx.CallAfter(self.fiche.Show)
#            wx.CallAfter(self.fiche.Redessiner)
            return
        
        
        liste_actions = [[self.classe.ConstruireArbre, [self.arbre, root], {},
                         u"Construction de l'arborescence de la classe...\t"],
                         [self.progression.ConstruireArbre, [self.arbre, root], {},
                          u"Construction de l'arborescence de la progression...\t"],
                         [self.progression.ChargerSequences, [], {},
                          u"Chargement des Séquences...\t"],
                         [self.progression.ChargerProjets, [], {},
                          u"Chargement des Projets...\t"],
                         [self.progression.Ordonner, [], {},
                          u"Classement...\t"],
#                         [self.projet.OrdonnerTaches, [], {},
#                          u"Ordonnancement des tâches...\t"],
#                         [self.projet.PubDescription, [], {},
#                          u"Traitement des descriptions...\t"],
#                         [self.projet.SetLiens, [], {},
#                          u"Construction des liens...\t"],
#                         [self.projet.MiseAJourDureeEleves, [], {},
#                          u"Ajout des durées/évaluabilités dans l'arbre...\t"],
#                         [self.projet.MiseAJourNomProfs, [], {},
#                          u"Ajout des disciplines dans l'arbre...\t"],
                         ]
        
        for fct, arg, karg, msg in liste_actions:
#            print "+++", msg
            message += msg
            dlg.Update(count, message)
#            dlg.top()
            count += 1
            if "beta" in version.__version__:
                fct(*arg, **karg)
                message += u"Ok\n"
            else:
                try :
                    fct(*arg, **karg)
                    message += u"Ok\n"
                except:
                    Ok = False
                    message += constantes.Erreur(constantes.ERR_INCONNUE).getMessage() + u"\n"
            

        self.progression.Verrouiller()

        message += u"Tracé de la fiche...\t"
        dlg.Update(count, message)
#        dlg.top()
        count += 1

#        self.arbre.SelectItem(self.classe.branche)

        self.arbre.Layout()
        self.arbre.ExpandAll()
        self.arbre.CalculatePositions()
        self.arbre.SelectItem(self.arbre.classe.branche)
        
        fichier.close()
        
        tps2 = time.clock() 
        print "Ouverture :", tps2 - tps1

        if Ok:
            dlg.Destroy()
        else:
            dlg.Update(nbr_etapes, message)
#            dlg.top()
            dlg.Close() 
    
        self.SetTitre()
#        self.progression.MiseAJourTypeEnseignement()
        
        wx.CallAfter(self.fiche.Show)
        wx.CallAfter(self.fiche.Redessiner)
        
        # Mise en liste undo/redo
        self.classe.undoStack.do(u"Ouverture de la Classe")
        self.progression.undoStack.do(u"Ouverture de la Progression")
        self.parent.miseAJourUndo()
    
        return self.progression
    
    
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

        self.InitBuffer()
        
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
#        self.Bind(wx.EVT_SCROLLWIN, self.OnScroll)

#        self.Redessiner()

     
    ######################################################################################################
    def OnLeave(self, evt = None):
        x, y = evt.GetPosition()
        x, y = self.ClientToScreen((x, y))
        self.GetDoc().HideTip((x, y))


    ######################################################################################################
    def OnEnter(self, event):
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

    
    ######################################################################################################
    def OnMove(self, evt):
        self.GetDoc().HideTip()
        x, y = evt.GetPosition()
        _x, _y = self.CalcUnscrolledPosition(x, y)
        xx, yy = self.ctx.device_to_user(_x, _y)
        
        #
        # Cas général
        #
        zone = self.GetDoc().HitTest(xx, yy)
#         print zone
        if zone is not None:
            x, y = self.ClientToScreen((x, y))
            self.GetDoc().Move(zone, x, y)
        else:
            self.GetDoc().HideTip()
#            elem = branche.GetData()
#            if hasattr(elem, 'tip'):
#                x, y = self.ClientToScreen((x, y))
#                elem.tip.Position((x+1,y+1), (0,0))
#                self.call = wx.CallLater(500, elem.tip.Show, True)
#                self.tip = elem.tip
#                evt.Skip()
#                return    
        
        #
        # Cas particulier des compétences
        #
#        kCompObj = self.GetDoc().HitTestCompetence(xx, yy)
#        if kCompObj != None:
#            kComp, obj = kCompObj
#            if hasattr(self, 'popup'):
##                for tip in self.tip_indic:
##                    tip.Destroy()
##                self.tip_indic = []
#                x, y = self.ClientToScreen((x, y))
##                type_ens = self.projet.classe.typeEnseignement
#         
#                competence = self.GetDoc().GetReferentiel().getCompetence(kComp)
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
#         
#                
#                self.popup.Fit()
#
#                self.popup.Position((x,y), (0,0))
#                self.call = wx.CallLater(500, self.popup.Show, True)
#                self.tip = self.popup
            
        evt.Skip()

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
            self.Scroll(0, y/20/draw_cairo.COEF)
            self.Refresh()
    
    
    #############################################################################            
    def OnClick(self, evt):
        self.GetDoc().HideTip()
        x, y = evt.GetPosition()
        _x, _y = self.CalcUnscrolledPosition(x, y)
        xx, yy = self.ctx.device_to_user(_x, _y)
        
        #
        # Cas général
        #
        zone = self.GetDoc().HitTest(xx, yy)
        if zone is not None:
            x, y = self.ClientToScreen((x, y))
            self.GetDoc().Click(zone, x, y)
        else:
            self.GetDoc().HideTip()
            
        
        
#        if branche != None:
#            self.GetDoc().SelectItem(branche, depuisFiche = True)
#            
#            
#        if not self.GetDoc().classe.verrouillee:
#            #
#            # Autres actions
#            #
#            position = self.GetDoc().HitTestPosition(xx, yy)
#            if position != None:
#                self.GetDoc().SetPosition(position)
            
        
        evt.Skip()
    
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
#        print "Redessiner"
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
#            ctx.show_page()
    #        b = Thread(None, self.Draw, None, (ctx,))
    #        b.start()
            
            dc.EndDrawing()
            self.ctx = ctx
            self.Refresh()
    
    #        tps2 = time.clock() 
    #        print "Tracé :"#, tps2 - tps1
            
            wx.EndBusyCursor()
            
        redess()


    
    #############################################################################            
    def normalize(self, cr):
        h = float(self.GetVirtualSize()[1]) / draw_cairo.COEF
        if h <= 0:
            h = 1.0
        cr.scale(h, h) 
        
#         h = float(self.GetVirtualSize()[1])
#         if h <= 0:
#             h = float(100)
# #        print h
#         cr.scale(h / draw_cairo.COEF, h / draw_cairo.COEF) 
        
        
    
    #############################################################################            
    def Draw(self, ctx):
        self.GetDoc().DefinirCouleurs()
        self.GetDoc().draw.Draw(ctx, self.GetDoc())
        
        
        
        
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
       



    
####################################################################################
#
#   Classe définissant la fenétre de la fiche de séquence
#
####################################################################################
class FicheProjet(BaseFiche):
    def __init__(self, parent, projet):
        BaseFiche.__init__(self, parent)
        self.projet = projet
        
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
class FicheProgression(BaseFiche):
    def __init__(self, parent, progression):
        BaseFiche.__init__(self, parent)
        self.progression = progression
        
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
#            print "Destroy", self.panel
#            try:
#            self.bsizer.Remove(self.panel)
            self.panel.Destroy()
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
    def __init__(self, parent, titre = u"", objet = None,
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
        self.EnableScrolling(False, True)
#        self.SetupScrolling(scroll_x = False) # Cause des problèmes (wx._core.PyDeadObjectError)
        

        self.eventAttente = False
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        
        self.Bind(wx.EVT_SIZE, self.OnResize)
        
#        wx.CallAfter(self.Show)


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
        return self.GetDocument().undoStack.onUndoRedo or self.GetDocument().classe.undoStack.onUndoRedo
    
    
    #########################################################################################################
    def sendEvent(self, doc = None, modif = u"", draw = True, obj = None):
        self.GetDocument().GetApp().sendEvent(doc, modif, draw, obj)
        self.eventAttente = False
        
    
    #########################################################################################################
    def GetFenetreDoc(self):
        return self.GetDocument().app

    #########################################################################################################
    def CreateImageSelect(self, parent, titre = u"Image", defaut = wx.NullBitmap):
        box = myStaticBox(parent, -1, titre)
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        image = wx.StaticBitmap(parent, -1, defaut)
        self.image = image
        self.SetImage()
        bsizer.Add(image, 1)#, flag = wx.EXPAND)
        
        bt = wx.Button(parent, -1, u"Changer l'image")
        bt.SetToolTipString(u"Cliquer ici pour sélectionner un fichier image")
        bsizer.Add(bt, flag = wx.ALIGN_BOTTOM|wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.OnClickImage, bt)
        self.btImg = bt
        
        return bsizer
        
    #############################################################################            
    def OnClickImage(self, event):
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
            self.objet.image = rognerImage(wx.Image(nomFichier).ConvertToBitmap())
            self.SetImage(True)
        
        dlg.Destroy()


    #############################################################################            
    def SetImage(self, sendEvt = False):
        if self.objet.image != None:
            self.image.SetBitmap(rognerImage(self.objet.image, 200, HMIN_PROP-80))
        else:
            self.image.SetBitmap(wx.NullBitmap)
        self.sizer.Layout()
        
        if sendEvt:
            self.sendEvent(modif = u"Modification de l'illustration "+self.objet.article_c_obj+u" "+self.objet.nom_obj,
                           obj = self)
            
            
    #############################################################################            
    def CreateLienSelect(self, parent):
        box = myStaticBox(parent, -1, u"Lien externe")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.selec = URLSelectorCombo(parent, self.objet.lien, self.objet.GetPath())
        bsizer.Add(self.selec, flag = wx.EXPAND)
        
        
        return bsizer
    
    
    


    #############################################################################            
    def CreateIconeSelect(self, parent):
        ib = myStaticBox(parent, -1, u"Icônes")
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
            ico = img.ConvertToImage().Scale(20, 20).ConvertToBitmap()
            btn = wx.BitmapButton(pnl, 100+i, ico)
            btn.SetToolTipString(nom)
            self.icones.append(nom)
            ims.Add(btn, 0, flag = wx.ALL, border = 2)
            btn.Refresh()
            self.Bind(wx.EVT_BUTTON, self.OnIconeClick, btn)
        
        ibsizer.Add(pnl, 1, flag = wx.EXPAND)
        
        self.btn_no_icon = wx.Button(parent, -1, u"Aucune")
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
        self.sendEvent(modif = u"Modification de l'icône "+self.objet.article_c_obj+u" "+self.objet.nom_obj)   






####################################################################################
#
#   Classe définissant le panel "racine" (ne contenant que des infos HTML)
#
####################################################################################

class PanelPropriete_Racine(wx.Panel):
    def __init__(self, parent, texte):
        wx.Panel.__init__(self, parent, -1)
        
        self.Hide() # Sans ça cela provoque des problèmes d'affichage
        
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
        self.Layout()
        
#        wx.CallAfter(self.Show)
        
#    def GetNiveau(self):
#        return 0
     

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
        titre = myStaticBox(self, -1, ref.labels["SEQINT"][0])
        sb = wx.StaticBoxSizer(titre)
        textctrl = TextCtrl_Help(self, u"")
        textctrl.SetTitre(ref.labels["SEQINT"][1], sequence.getIcone())
        textctrl.SetToolTipString(u"")
                    
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        self.sizer.Add(sb, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
#        self.sizer.Add(textctrl, (0,1), flag = wx.EXPAND)
#        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
#         self.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.textctrl)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.textctrl)

        #
        # Commentaires
        #
        titre = myStaticBox(self, -1, u"Commentaires")
        sb = wx.StaticBoxSizer(titre)
        commctrl = TextCtrl_Help(self, u"")
        commctrl.SetTitre(u"Commentaires sur la Séquence", sequence.getIcone())
        commctrl.SetToolTipString(u"")
                    
        sb.Add(commctrl, 1, flag = wx.EXPAND)
        self.commctrl = commctrl
        self.sizer.Add(sb, (0,2), (1,1),  flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
#        self.sizer.Add(commctrl, (1,1), flag = wx.EXPAND)
#        self.Bind(wx.EVT_TEXT, self.EvtText, commctrl)
#         self.Bind(stc.EVT_STC_CHANGE, self.EvtText, commctrl)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, commctrl)
        
        #
        # Position
        #
        titre = myStaticBox(self, -1, u"Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        self.bmp = wx.StaticBitmap(self, -1, self.getBitmapPeriode())
        self.position = PositionCtrl(self, self.sequence.position, 
                                     self.sequence.GetReferentiel().periodes)
#         self.Bind(wx.EVT_RADIOBUTTON, self.onChanged)
        self.Bind(wx.EVT_SLIDER, self.onChanged)
        sb.Add(self.bmp, flag = wx.ALIGN_CENTER|wx.EXPAND)
        sb.Add(self.position, flag = wx.ALIGN_CENTER|wx.EXPAND)
        
        self.sizer.Add(sb, (1,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
        
        #
        # Lien externe
        #
        lsizer = self.CreateLienSelect(self)
        self.sizer.Add(lsizer, (1,2), (1,1),  flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)

        
        self.sizer.SetEmptyCellSize((0, 0))
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(2)
        
        self.cbD = {}
        self.CreerCBDomaine() # Permet de créer les Checkbox "Domaine"
        
        self.MiseAJour()
        
        self.sizer.Layout()
#        wx.CallAfter(self.Layout)
        self.Layout()
        
#        self.Fit()
        
    
    #############################################################################            
    def getBitmapPeriode(self, larg = 250):
        return self.sequence.getBitmapPeriode(larg)
         
    
    #############################################################################            
    def onChanged(self, evt):
        self.sequence.SetPosition(self.position.GetRange())
        self.SetBitmapPosition()
        self.sendEvent(modif = u"Changement de position de la Séquence",
                       obj = self.sequence)
        
        
    #############################################################################            
    def SetBitmapPosition(self, bougerSlider = None):
        self.bmp.SetBitmap(self.getBitmapPeriode())
        self.position.SetValue(self.sequence.position)


    #############################################################################            
    def EvtCheckBox(self, event):
        
#         cb = event.GetEventObject()
        self.sequence.domaine = "".join([t for t, cb in self.cbD.items() if cb.IsChecked()])
        self.sequence.classe.Verrouiller(len(self.sequence.domaine) > 0)
        
        self.sendEvent(modif = u"Modification du domaine de la Séquence")
        
            
    #############################################################################            
    def EvtText(self, event):
        if event.GetEventObject() == self.textctrl:
            self.sequence.SetText(self.textctrl.GetText())
            t = u"Modification de l'intitulé de la Séquence"
        else:
            self.sequence.SetCommentaire(self.commctrl.GetText())
            t = u"Modification du commentaire de la Séquence"
        
        if self.onUndoRedo():
            self.sendEvent(modif = t)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = t)
                self.eventAttente = True


    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "Miseàjour"
        
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
            self.sizer.RemovePos(self.sb)
            
        self.cbD = {}
        if len(self.sequence.domaine) > 1:
            if self.sizer.FindItemAtPosition((0,1)) is None:
                ref = self.sequence.GetReferentiel()
                titre = myStaticBox(self, -1, getSingulierPluriel(ref.nomDom, len(self.sequence.domaine)>1))
                self.sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
                
                for dom in ref.listeDomaines:
                    cb = wx.CheckBox(self, -1, ref.domaines[dom][0])
                    cb.SetToolTipString(ref.domaines[dom][1])
                    self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
                    self.sb.Add(cb)
                    self.cbD[dom] = cb
                
                self.sizer.Add(self.sb, (0,1), (2, 1), flag = wx.ALIGN_TOP | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)

        
            
        
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
        wx.CallAfter(self.PostSizeEvent)
        
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
    def creerPageSimple(self, fct, titre = u"", helpText = u""):
        bg_color = self.Parent.GetBackgroundColour()
        page = PanelPropriete(self.nb, objet = self.GetDocument())
        page.SetBackgroundColour(bg_color)
        self.nb.AddPage(page, u"")
#        ctrl = orthographe.STC_ortho(page, -1)#, u"", style=wx.TE_MULTILINE)
        ctrl = TextCtrl_Help(page, titre, helpText)
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
        self.pages = {}


        #
        # La page "Généralités"
        #
        pageGen = PanelPropriete(self.nb, objet = self.GetDocument())
        bg_color = self.Parent.GetBackgroundColour()
        pageGen.SetBackgroundColour(bg_color)
        self.pageGen = pageGen
        self.nb.AddPage(pageGen, u"Propriétés générales")


        #
        # Intitulé du projet (TIT)
        #
        self.titre = myStaticBox(pageGen, -1, u"")
        sb = wx.StaticBoxSizer(self.titre)
        textctrl = TextCtrl_Help(pageGen, u"")
        
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        pageGen.sizer.Add(sb, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
#        pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText)
#        pageGen.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
#         pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.textctrl)
        pageGen.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.textctrl)
        

        
        #
        # Problématique (PB)
        #
        self.tit_pb = myStaticBox(pageGen, -1, u"")
        sb = wx.StaticBoxSizer(self.tit_pb)
#        self.commctrl = wx.TextCtrl(pageGen, -1, u"", style=wx.TE_MULTILINE)
        self.commctrl = TextCtrl_Help(pageGen, u"")
                                              
                                              
        sb.Add(self.commctrl, 1, flag = wx.EXPAND)
        pageGen.sizer.Add(sb, (0,1), (2,1),
                          flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.EXPAND, border = 2)
#        pageGen.Bind(wx.EVT_TEXT, self.EvtText, self.commctrl)
#        pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.commctrl)
#         pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.commctrl)
        pageGen.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.commctrl)
        

        #
        # Année scolaire et Position dans l'année
        #
        titre = myStaticBox(pageGen, -1, u"Années et Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        
        self.annee = Variable(u"Année scolaire", lstVal = self.projet.annee, 
                                   typ = VAR_ENTIER_POS, bornes = [2012,2100])
        self.ctrlAnnee = VariableCtrl(pageGen, self.annee, coef = 1, signeEgal = False,
                                      help = u"Années scolaires", sizeh = 40, 
                                      unite = str(self.projet.annee+1),
                                      sliderAGauche = True)
        self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlAnnee)
        sb.Add(self.ctrlAnnee)
        
        self.bmp = wx.StaticBitmap(pageGen, -1, self.getBitmapPeriode(250))
        
        ref = self.projet.GetReferentiel()
        self.position = PositionCtrl(pageGen, self.projet.position, ref.periodes, ref.projets)#wx.SL_AUTOTICKS |
        sb.Add(self.bmp)
        sb.Add(self.position, flag = wx.EXPAND)
        
        pageGen.sizer.Add(sb, (1,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.EXPAND|wx.LEFT, border = 2)
#         self.Bind(wx.EVT_RADIOBUTTON, self.onChanged)
        self.Bind(wx.EVT_SLIDER, self.onChanged)
#        self.position.Bind(wx.EVT_RADIOBUTTON, self.onChanged)


        #
        # Organisation (nombre et positions des revues)
        #
        self.panelOrga = PanelOrganisation(pageGen, self, self.projet)
        pageGen.sizer.Add(self.panelOrga, (0,2), (2,1), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.EXPAND|wx.LEFT, border = 2)
        
        
        pageGen.sizer.AddGrowableRow(0)
        pageGen.sizer.AddGrowableCol(1)
    


        
    #############################################################################            
    def getBitmapPeriode(self, larg):
        return self.projet.getBitmapPeriode(larg)
#        print "getBitmapPeriode"       
        
         
    
    #############################################################################            
    def onChanged(self, event):
#        print "onChanged", event.GetSelection(), event.GetEventObject()
        self.projet.SetPosition(self.position.GetRange())
        self.SetBitmapPosition()
        self.sendEvent(modif = u"Changement de position du projet",
                       obj = self.projet)
        
        
    #############################################################################            
    def SetBitmapPosition(self, bougerSlider = None):
        self.bmp.SetBitmap(self.getBitmapPeriode(250))
#        if bougerSlider != None:
        self.position.SetValue(self.projet.position)

        
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
#            nt = event.GetString()
            nt = self.textctrl.GetText()
#             print nt
#            if nt == u"":
#                nt = self.projet.support.nom
            self.projet.SetText(nt)
            #self.textctrl.ChangeValue(nt)
            maj = True
            obj = 'intit'
            
        elif 'ORI' in self.pages.keys() and event.GetEventObject() == self.pages['ORI'][1]:
            self.projet.origine = self.pages['ORI'][1].GetText()
            maj = False
#             obj = 'ORI'
            
        elif 'CCF' in self.pages.keys() and event.GetEventObject() == self.pages['CCF'][1]:
            self.projet.contraintes = self.pages['CCF'][1].GetText()
            maj = False
#             obj = 'CCF'
            
        elif 'OBJ' in self.pages.keys() and event.GetEventObject() == self.pages['OBJ'][1]:
            self.projet.production = self.pages['OBJ'][1].GetText()
            maj = False
#             obj = 'OBJ'
            
        elif 'SYN' in self.pages.keys() and event.GetEventObject() == self.pages['SYN'][1]:
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
            
        elif 'PAR' in self.parctrl.keys() and event.GetEventObject() == self.parctrl['PAR']:
            self.projet.partenariat = self.parctrl['PAR'].GetText()
            maj = False
#             obj = 'PAR'
            
        elif 'PRX' in self.parctrl.keys() and event.GetEventObject() == self.parctrl['PRX']:
            self.projet.montant = self.parctrl['PRX'].GetText()
            maj = False
#             obj = 'PRX'
            
        elif 'SRC' in self.parctrl.keys() and event.GetEventObject() == self.parctrl['SRC']:
            self.projet.src_finance = self.parctrl['SRC'].GetText()
            maj = False
#             obj = 'SRC'
        
#        else:
#            maj = False
            
#         print obj
        modif = u"Modification des propriétés du Projet"
        if self.onUndoRedo():
            self.sendEvent(modif = modif)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, 
                             modif = modif,
                             draw = maj)
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
    def MiseAJourTypeEnseignement(self, sendEvt = False):
        
        ref = self.projet.GetProjetRef()
#        print "MiseAJourTypeEnseignement projet", ref.code
        
        CloseFenHelp()
        
        #
        # Page "Généralités"
        #
        self.titre.SetLabel(ref.attributs['TIT'][0])
        self.textctrl.MiseAJour(ref.attributs['TIT'][0], ref.attributs['TIT'][3])
        self.textctrl.SetToolTipString(u"Titre, résumé, intitulé, description synthétique du projet")
        self.textctrl.SetTitre(ref.attributs['TIT'][0])
        
        self.tit_pb.SetLabel(ref.attributs['PB'][0])
        self.commctrl.MiseAJour(ref.attributs['PB'][0], ref.attributs['PB'][3])
        self.commctrl.SetToolTipString(ref.attributs['PB'][1] + constantes.TIP_PB_LIMITE)
        self.commctrl.SetTitre(ref.attributs['PB'][0])
        
        self.MiseAJourPosition()
        self.panelOrga.MiseAJourListe()
        
        
        #
        # Pages simples
        #
        for k in ['ORI', 'CCF', 'OBJ', 'SYN']:
            if ref.attributs[k][0] != u"":
                if not k in self.pages.keys():
                    self.pages[k] = self.creerPageSimple(self.EvtText,ref.attributs[k][0],  ref.attributs[k][3])
                else:
                    self.pages[k][1].MiseAJour(ref.attributs[k][0], ref.attributs[k][3])
                self.nb.SetPageText(self.GetPageNum(self.pages[k][0]), ref.attributs[k][0])
                self.pages[k][1].SetToolTipString(ref.attributs[k][1])
                self.pages[k][1].SetTitre(ref.attributs[k][0])
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
                self.pages['DEC'] = PanelPropriete(self.nb, objet = self.GetDocument())
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
                
                titreInt = myStaticBox(self.pages['DEC'], -1, u"Intitulés des différentes parties")
                sb = wx.StaticBoxSizer(titreInt)
                
                self.intctrl = TextCtrl_Help(self.pages['DEC'], u"", ref.attributs['DEC'][1])#, u"", style=wx.TE_MULTILINE)
                self.intctrl.SetTitre(u"Intitulés des différentes parties")
                self.intctrl.SetToolTipString(u"Intitulés des parties du projet confiées à chaque groupe.\n" \
                                              u"Les groupes d'élèves sont désignés par des lettres (A, B, C, ...)\n" \
                                              u"et leur effectif est indiqué.")
#                self.pages['DEC'].Bind(wx.EVT_TEXT, self.EvtText, self.intctrl)
#                 self.pages['DEC'].Bind(stc.EVT_STC_CHANGE, self.EvtText, self.intctrl)
                self.pages['DEC'].Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.intctrl)
                sb.Add(self.intctrl, 1, flag = wx.EXPAND)
                self.pages['DEC'].sizer.Add(sb, (1,0), flag = wx.EXPAND|wx.ALL, border = 2)
                
                titreInt = myStaticBox(self.pages['DEC'], -1, u"Enoncés du besoin des différentes parties du projet")
                sb = wx.StaticBoxSizer(titreInt)
                self.enonctrl = TextCtrl_Help(self.pages['DEC'], u"", ref.attributs['DEC'][3])#, u"", style=wx.TE_MULTILINE)       
                self.enonctrl.SetToolTipString(u"Enoncés du besoin des parties du projet confiées à chaque groupe")
                self.enonctrl.SetTitre(u"Enoncés du besoin des différentes parties du projet")
        
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
                self.intctrl.MiseAJour(u"", ref.attributs['DEC'][1])
                self.enonctrl.MiseAJour(u"", ref.attributs['DEC'][3])
        else:
            if 'DEC' in self.pages.keys():
                self.nb.DeletePage(self.GetPageNum(self.pages['DEC']))
                del self.pages['DEC']
        
        
        # La page "typologie" ('TYP')
        
        if ref.attributs['TYP'][0] != "":
            if not 'TYP' in self.pages.keys():
                self.pages['TYP'] = PanelPropriete(self.nb, objet = self.GetDocument())
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
#        print "xxx ", ref.attributs
        if ref.attributs['PAR'][0] != "":
            if not 'PAR' in self.pages.keys():
                self.parctrl = {}
                self.pages['PAR'] = PanelPropriete(self.nb, objet = self.GetDocument())
                bg_color = self.Parent.GetBackgroundColour()
                self.pages['PAR'].SetBackgroundColour(bg_color)
                
                self.nb.AddPage(self.pages['PAR'], ref.attributs['PAR'][0])
                
                for i, k in enumerate(['PAR', 'PRX', 'SRC']):
                    titreInt = myStaticBox(self.pages['PAR'], -1, ref.attributs[k][0])
                    sb = wx.StaticBoxSizer(titreInt)
                
                    self.parctrl[k] = orthographe.STC_ortho(self.pages['PAR'], -1)#, u"", style=wx.TE_MULTILINE)
                    
                    self.parctrl[k].SetTitre(ref.attributs['PAR'][0])

                    self.parctrl[k].SetToolTipString(ref.attributs[k][1])
#                    self.pages['PAR'].Bind(wx.EVT_TEXT, self.EvtText, self.parctrl[k])
#                     self.pages['PAR'].Bind(stc.EVT_STC_CHANGE, self.EvtText, self.parctrl[k])
                    self.pages['PAR'].Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.parctrl[k])
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
##        self.position.SetRange(0, self.projet.GetLastPosition())
        self.position.SetValue(self.projet.position)
    

    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "MiseAJour Projet", sendEvt

        ref = self.projet.GetProjetRef()
        
        # La page "Généralités"
        self.textctrl.SetValue(self.projet.intitule, False)
        self.commctrl.SetValue(self.projet.problematique, False)

        # Les pages simples
        if 'ORI' in self.pages.keys():
            self.pages['ORI'][1].SetValue(self.projet.origine, False)
        if 'CCF' in self.pages.keys():
            self.pages['CCF'][1].SetValue(self.projet.contraintes, False)
        if 'OBJ' in self.pages.keys():
            self.pages['OBJ'][1].SetValue(self.projet.production, False)
        if 'SYN' in self.pages.keys():
            self.pages['SYN'][1].SetValue(self.projet.synoptique, False)
        
        # La page "typologie" ('TYP')
        if ref.attributs['TYP'][0] != "":
            for t in self.projet.typologie:
                self.lb.Check(t)
                
        # La page "sous parties" ('DEC')
        if ref.attributs['DEC'][0] != "":
            self.intctrl.SetValue(self.projet.intituleParties, False)
            self.enonctrl.SetValue(self.projet.besoinParties, False)
            self.nbrParties.v[0] = self.projet.nbrParties
            self.ctrlNbrParties.mofifierValeursSsEvt()
        
        # La page "Partenariat" ('PAR')
        if ref.attributs['PAR'][0] != "":
            self.parctrl['PAR'].SetValue(self.projet.partenariat, False)
            self.parctrl['PRX'].SetValue(self.projet.montant, False)
            self.parctrl['SRC'].SetValue(self.projet.src_finance, False)
                    
        self.MiseAJourPosition()
     
        self.panelOrga.MiseAJourListe()
        self.Layout()
        
        if sendEvt:
            self.sendEvent()


    ######################################################################################  
    def Verrouiller(self, etat):
        self.position.Enable(etat)
        

# class PositionCtrl(wx.Panel):
#     def __init__(self, parent, position, periodes, projets = {}):
#         wx.Panel.__init__(self, parent, -1)
#         self.sizer = wx.BoxSizer(wx.HORIZONTAL)
#         radio = []
#         periodes_prj = [p.periode for p in projets.values()]
#         self.position = position
#         
# #        print "periodes_prj", periodes_prj
#         num = 1
#         for an, np in periodes:
#             p = 1
#             while p <= np:
#                 if num == 0:
#                     s = wx.RB_GROUP
#                 else:
#                     s = 0
#                 
#                 l = 1
#                 for pr in periodes_prj:
#                     if len(pr) > 0 and num == pr[0]:
#                         l = pr[-1] - pr[0] +1
#                         break
#                     
#                 radio.append(wx.RadioButton(self, num, "", style = s))
#                 sizer = wx.BoxSizer(wx.VERTICAL)
#                 sizer.Add(radio[-1], flag = wx.ALIGN_CENTER_HORIZONTAL)
#                 radio[-1].SetToolTipString(an+' '+str(p))
#                 self.sizer.Add(sizer, l, flag = wx.ALIGN_RIGHT|wx.EXPAND)
#                 self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, radio[-1] )
#                 num += l
#                 p += l
#         self.radio = radio
#         self.SetSizer(self.sizer)
#         
#         
#     def OnRadio(self, event):
#         wx.PostEvent(self.Parent, event)
#         
# 
#     def SetValue(self, pos):
#         self.radio[pos].SetValue(True)
#         
#         
#     def MiseAJour(self):
#         self.SetValue(self.position)

class PositionCtrl(wx.Panel):
    def __init__(self, parent, position, periodes, projets = {}):
        wx.Panel.__init__(self, parent, -1)
        self.position = position
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        projets = [[x-1 for x in p.periode] for p in projets.values()]
        self.sel = RangeSlider(self, position, 0, sum(p[1] for p in periodes)-1, projets)
        self.sizer.Add(self.sel, 1, flag = wx.ALIGN_RIGHT|wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Bind(wx.EVT_SLIDER, self.OnSlide)
        
        return
        
        
    def OnSlide(self, event):
        wx.PostEvent(self.Parent, event)
        

    def SetValue(self, pos):
        self.sel.SetValue(pos)
        
    
    def GetRange(self):
        return self.sel.GetRange()
        
        
    def MiseAJour(self):
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
            self.sizer.Add(cb, 1, flag = wx.ALIGN_RIGHT|wx.EXPAND)
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
        wx.CallAfter(self.PostSizeEvent)
        
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
        self.nb.AddPage(pageGen, u"Propriétés générales")


        #
        # Intitulé de la progression (TIT)
        #
        self.titre = myStaticBox(pageGen, -1, u"Intitulé de la Progression")
        sb = wx.StaticBoxSizer(self.titre)
        textctrl = TextCtrl_Help(pageGen, u"")
        textctrl.SetTitre(u"Intitulé de la Progression", self.progression.getIcone())
        textctrl.SetToolTipString(u"")
        sb.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
        pageGen.sizer.Add(sb, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, border = 2)
#        pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText)
#        pageGen.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
#         pageGen.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.textctrl)
        pageGen.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.textctrl)
       
        
        
        
        #
        # Année scolaire et Position dans l'année
        #
        titre = myStaticBox(pageGen, -1, u"Année et Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        
        self.annee = Variable(u"Année scolaire", lstVal = self.GetDocument().calendrier.annee, 
                                   typ = VAR_ENTIER_POS, bornes = [2012,2100])
        self.ctrlAnnee = VariableCtrl(pageGen, self.annee, coef = 1, signeEgal = False,
                                      help = u"Année scolaire", sizeh = 40, 
                                      unite = str(self.GetDocument().calendrier.GetAnneeFin()),
                                      sliderAGauche = True)
        self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlAnnee)
        sb.Add(self.ctrlAnnee)
        pageGen.sizer.Add(sb, (1,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, border = 2)
        
        
        #
        # Nombre de créneaux horaires
        #
        titre = myStaticBox(pageGen, -1, u"Créneaux horaire")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        
        self.nbrCreneaux = Variable(u"Nombre de créneaux", lstVal = self.GetDocument().nbrCreneaux, 
                                   typ = VAR_ENTIER_POS, bornes = [1,5])
        self.ctrlCreneaux = VariableCtrl(pageGen, self.nbrCreneaux, coef = 1, signeEgal = False,
                                      help = u"Nombre de créneaux horaire", sizeh = 40, 
                                      sliderAGauche = True)
        self.Bind(EVT_VAR_CTRL, self.EvtVariable, self.ctrlCreneaux)
        sb.Add(self.ctrlCreneaux)
        pageGen.sizer.Add(sb, (1,1), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, border = 2)
        
        
        
        #
        # Lien
        #
        lsizer = self.CreateLienSelect(pageGen)
        pageGen.sizer.Add(lsizer, (2,0), (1, 2), flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        #
        # Image
        #
        isizer = self.CreateImageSelect(pageGen, titre = u"Image")
        pageGen.sizer.Add(isizer, (0,2), (3,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.ALL, border = 2)#wx.ALIGN_CENTER_VERTICAL |



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
#        print "MiseAJour Progression", sendEvt

        
        # La page "Généralités"
        self.textctrl.SetValue(self.GetDocument().intitule, False)
        
        self.Layout()
        
        if sendEvt:
            self.sendEvent()

    
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
        

        modif = u"Modification des propriétés de la progression"
        if self.onUndoRedo():
            self.sendEvent(modif = modif)
        else:
            if not self.eventAttente:
#                print "   modif", obj
                wx.CallLater(DELAY, self.sendEvent, 
                             modif = modif,
                             draw = maj)
                self.eventAttente = True
    
    
    
    #############################################################################            
    def EvtVariable(self, event):
        var = event.GetVar()
        if var == self.annee:
            cal = self.GetDocument().calendrier
            cal.annee = var.v[0]
            self.ctrlAnnee.unite.SetLabel(str(cal.annee + cal.GetNbrAnnees())) 
            
            modif = u"Modification de l'année scolaire de la Progression"
            self.sendEvent(modif = modif)
            
        elif var == self.nbrCreneaux:
            self.GetDocument().nbrCreneaux = var.v[0]
            
            modif = u"Modification du nombre de creneaux de la Progression"
            self.sendEvent(modif = modif)
            
        self.Refresh()
        
    
    
    
        
    
    
###################################################################################################
class PanelOrganisation(wx.Panel):    
    def __init__(self, parent, panel, objet):
        wx.Panel.__init__(self, parent, -1)
        self.objet = objet
        self.parent = panel
        
        sizer = wx.BoxSizer()
        gbsizer = wx.GridBagSizer()
        titre = myStaticBox(self, -1, u"Organisation")
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
        u""" Déplacement de la revue sélectionnée
            vers le haut ou vers le bas
        """
     
        revue = self.liste.GetStringSelection()
        
        if revue[:5] == "Revue":
            i = event.GetId()
            ref = self.objet.GetProjetRef()
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
#            print posRevue, ">>", nouvPosRevue, self.liste.GetString(nouvPosRevue), toSystemEncoding(self.liste.GetString(nouvPosRevue))
            itemPrecedent = ref.getClefDic('phases', self.liste.GetString(nouvPosRevue).lstrip(), 0)
            
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
            self.parent.sendEvent(modif = u"Déplacement de la revue",
                                  obj = self.objet)
        
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
                self.parent.sendEvent(modif = u"Modification du nombre de revues",
                                      obj = self.objet)



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
        
        #
        # La page "Généralités"
        #
        nb = wx.Notebook(self, -1,  style= wx.BK_DEFAULT)
        pageGen = PanelPropriete(nb, objet = classe)
        bg_color = self.Parent.GetBackgroundColour()
        pageGen.SetBackgroundColour(bg_color)
        self.pageGen = pageGen
        
        nb.AddPage(pageGen, u"Propriétés générales")


        #
        # la page "Systèmes"
        #
        pageSys = PanelPropriete(nb, objet = classe)
        pageSys.SetBackgroundColour(bg_color)
        nb.AddPage(pageSys, u"Systèmes techniques et Matériel")
        self.pageSys = pageSys
        
        self.sizer.Add(nb, (0,1), (2,1), flag = wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND, border = 1)
        self.nb = nb
        self.sizer.AddGrowableCol(1)

        

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
    
        tsize = constantes.IMG_SIZE_TB
        open_bmp = scaleImage(images.Icone_open.GetBitmap(), *tsize)
        save_bmp =  scaleImage(images.Icone_save.GetBitmap(), *tsize)
        pref_bmp = scaleImage(images.Icone_defaut_pref.GetBitmap(), *tsize)
#         open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
#         save_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        
        tb.AddSimpleTool(30, open_bmp, u"Ouvrir un fichier classe")
        self.Bind(wx.EVT_TOOL, self.commandeOuvrir, id=30)
        
        tb.AddSimpleTool(32, save_bmp, t)
        self.Bind(wx.EVT_TOOL, self.commandeSauve, id=32)
        
        tb.AddSimpleTool(31, pref_bmp, 
                         u"Rétablir les paramétres de classe par défaut")
        self.Bind(wx.EVT_TOOL, self.OnDefautPref, id=31)

        tb.Realize()


        #
        # Type d'enseignement
        #
        self.pourProjet = self.GetDocument().estProjet()
        titre = myStaticBox(pageGen, -1, u"Type d'enseignement")
        titre.SetMinSize((180, 100))
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
        titre = myStaticBox(pageGen, -1, u"Etablissement")
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
     
        self.cbv = SlimSelector(pageGen, -1, u"sélectionner une ville ...", (-1,-1), 
                         (-1, -1), [],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboVille, self.cbv)
        pageGen.Bind(wx.EVT_TEXT, self.EvtComboVille, self.cbv)
        sh.Add(self.cbv, 1,flag = wx.ALIGN_CENTER_VERTICAL|wx.LEFT, border = 5)
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
        # Accés au BO
        #
        titre = myStaticBox(pageGen, -1, u"Documents Officiels en ligne")
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
                                 choices = [""], style = wx.LB_SINGLE)# | wx.LB_SORT)
        self.Bind(wx.EVT_LISTBOX, self.EvtListBoxSyst, self.lstSys)
        
        self.btnSupprimerSys = wx.Button(pageSys, -1, u"Supprimer")
        self.btnSupprimerSys.SetToolTipString(u"Supprimer le système de la liste")
        self.Bind(wx.EVT_BUTTON, self.EvtButtonSupprSyst, self.btnSupprimerSys)
        
        s = pysequence.Systeme(self.classe)
        self.panelSys = s.GetPanelPropriete(pageSys)
        self.panelSys.Show()
    
        pageSys.sizer.Add(self.btnAjouterSys, (0,0), flag = wx.ALL|wx.EXPAND, border = 2)
        pageSys.sizer.Add(self.lstSys, (1,0), flag = wx.ALL|wx.EXPAND, border = 2)
        pageSys.sizer.Add(self.btnSupprimerSys, (2,0), flag = wx.ALL|wx.EXPAND, border = 2)
        pageSys.sizer.Add(self.panelSys, (0,1), (3,1),  flag = wx.ALL|wx.EXPAND, border = 2)
        pageSys.sizer.AddGrowableRow(1)
        pageSys.sizer.AddGrowableCol(1)
    
        self.MiseAJour()
        self.Verrouiller()
        self.MiseAJourBoutonsSystem()
        
        self.Bind(wx.EVT_SIZE, self.OnResize)
        
        self.Layout()
        
#        wx.CallAfter(self.cb_type.CollapseAll)
#        wx.CallAfter(self.Thaw)
        
        
    ######################################################################################              
    def OnResize(self, evt = None):
        self.nb.SetMinSize((-1,self.GetClientSize()[1]))
        self.Layout()
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
        
        self.sendEvent(modif = u"Ouverture d'une Classe",
                       obj = self.classe)
    
    ###############################################################################################
    def enregistrer(self, nomFichier):

        wx.BeginBusyCursor()
        fichier = file(nomFichier, 'w')
        
        # La classe
        classe = self.classe.getBranche()
        
        # La racine
        constantes.indent(classe)
        
        try:
#            ET.ElementTree(classe).write(fichier, encoding = SYSTEM_ENCODING)
            ET.ElementTree(classe).write(fichier, xml_declaration=False, encoding = SYSTEM_ENCODING)
        except IOError:
            messageErreur(None, u"Accés refusé", 
                                  u"L'accés au fichier %s a été refusé !\n\n"\
                                  u"Essayer de faire \"Enregistrer sous...\"" %nomFichier)
        except UnicodeDecodeError:
            messageErreur(None, u"Erreur d'encodage", 
                                  u"Un caractére spécial empéche l'enregistrement du fichier !\n\n"\
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
        self.classe.Initialise(isinstance(self.classe.doc, pysequence.Projet), defaut = True)
#        self.classe.doc.AjouterListeSystemes(self.classe.systemes)
        self.MiseAJour()
        self.sendEvent(modif = u"Réinitialisation des paramètres de Classe",
                       obj = self.classe)
        
        
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
    def EvtComboAcad(self, evt = None, modif = True):
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
        self.cbv.SlimResize()
#        self.cbv.SetSize((self.cbv.GetSizeFromTextSize(),-1))
        self.cbv.Refresh()
        
        if modif:
            self.sendEvent(modif = u"Modification de l'académie",
                           obj = self.classe)
            
    
    ######################################################################################  
    def EvtComboVille(self, evt = None, modif = True):
#        print "EvtComboVille"
        if evt != None:
            self.classe.ville = evt.GetString()
#        print "   ", self.classe.ville
        lst = []
        for val in constantes.ETABLISSEMENTS.values():
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
            self.sendEvent(modif = u"Modification de la ville",
                           obj = self.classe)
        
            
        
    ######################################################################################  
    def EvtComboEtab(self, evt):       
#        if evt.GetSelection() == len(constantes.ETABLISSEMENTS_PDD):
#            self.classe.etablissement = self.textctrl.GetStringSelection()
#            self.AfficherAutre(True)
#        else:
        self.classe.etablissement = evt.GetString()
#        self.AfficherAutre(False)
        
        self.sendEvent(modif = u"Modification de l'établissement",
                       obj = self.classe)
     

    ######################################################################################  
    def EvtListBoxSyst(self, event = None, num = 0):
        u""" Actions réalisées après avoir cliqué dans la liste de systèmes
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
        u""" Ajoute un nouveau système à la liste des système de la classe
        """
        #
        # Définition du nouveau nom
        #
        
        nom = u"Nouveau système"
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
        u""" Supprime un  système de la liste des système de la classe
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
        self.btnSupprimerSys.Enable(self.lstSys.GetCount() > 1)
        
    
    ######################################################################################  
    def MiseAJourListeSys(self, nom = u""):
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


    ######################################################################################  
    def EvtRadioBox(self, event = None, CodeFam = None):
        u""" Sélection d'un type d'enseignement
        """
        if event != None:
            radio_selected = event.GetEventObject()
            CodeFam = Referentiel.getEnseignementLabel(radio_selected.GetLabel())
        
        
#        fam = self.classe.familleEnseignement
#         ancienRef = self.classe.referentiel
#         ancienneFam = self.classe.familleEnseignement
        self.classe.typeEnseignement, self.classe.familleEnseignement = CodeFam
        self.classe.referentiel = REFERENTIELS[self.classe.typeEnseignement]
        
#        for c, e in [r.Enseignement[1:] for r in REFERENTIELS]constantes.Enseignement.items():
#            if e[0] == :
#                self.classe.typeEnseignement = c
#                self.classe.familleEnseignement = constantes.FamilleEnseignement[self.classe.typeEnseignement]
#                break
        
        self.classe.MiseAJourTypeEnseignement()
        self.classe.doc.MiseAJourTypeEnseignement()
        self.classe.doc.SetPosition(self.classe.doc.position)
#        self.classe.doc.MiseAJourTypeEnseignement(fam != self.classe.familleEnseignement)
#        self.MiseAJourType()
#        if hasattr(self, 'list'):
#            self.list.Peupler()

        self.st_type.SetLabel(self.classe.referentiel.Enseignement[0])
        self.SetLienBO()
        
        self.Refresh()
        
        self.sendEvent(modif = u"Modification du type d'enseignement",
                       obj = self.classe)
        
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
#         print "MiseAJour panelPropriete Classe"
#        self.MiseAJourType()
        
        
        self.cb_type.SetStringSelection(self.classe.referentiel.Enseignement[0])
        self.st_type.SetLabel(self.classe.referentiel.Enseignement[0])
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
        etat = not self.classe.verrouillee
        self.cb_type.Show(etat)
        self.st_type.Show(not etat)
        self.tb.EnableTool(30, etat)
        self.tb.EnableTool(31, etat)
        self.pasVerrouille = etat

        
    
          

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
    u"""Classe définissant le panel de réglage des effectifs
        Rappel :
        
        :Example:
        
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
        boxClasse = myStaticBox(self, -1, u"Découpage de la classe")

        coulClasse = couleur.GetCouleurWx(constantes.CouleursGroupes['C'])
#        boxClasse.SetOwnForegroundColour(coulClasse)
        
        self.coulEffRed = couleur.GetCouleurWx(constantes.CouleursGroupes['G'])

        self.coulEP = couleur.GetCouleurWx(constantes.CouleursGroupes['E'])
    
        self.coulAP = couleur.GetCouleurWx(constantes.CouleursGroupes['P'])
        
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
                                help = u"Nombre d'élèves dans la classe entiére", sizeh = 30, color = coulClasse)
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
        boxEffRed = myStaticBox(self, -1, u"")
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
        
#        self.BoxEP = myStaticBox(self, -1, u"", size = (30, -1))
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
        
#        self.BoxAP = myStaticBox(self, -1, u"", size = (30, -1))
#        self.BoxAP.SetOwnForegroundColour(self.coulAP)
#        self.BoxAP.SetMinSize((30, -1))     
#        bsizer = wx.StaticBoxSizer(self.BoxAP, wx.VERTICAL)
#        self.sizerEffRed_d.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
        
        
        # Illistration de la répartition
        self.bmp = StaticBitmapZoom(self, -1, size = (320, 46))
        bsizerClasse.Add(self.bmp, flag = wx.EXPAND)
        
        self.lstBoxEffRed = []
        self.lstBoxEP = []
        self.lstBoxAP = []
        
#        self.AjouterGroupesVides()
        
        self.MiseAJourNbrEleve()

        border = wx.BoxSizer()
        border.Add(bsizerClasse, 1, wx.EXPAND)
        self.SetSizer(border)

    
    #############################################################################            
    def getBitmapClasse(self, larg):
        imagesurface = draw_cairo.getBitmapClasse(larg, self.classe)

        return getBitmapFromImageSurface(imagesurface)
    
    
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
            
        self.classe.GetApp().sendEvent(self.classe, modif = u"Modification du découpage de la Classe",
                              obj = self.classe)
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
#            box = myStaticBox(self, -1, u"Eff Red", size = (30, -1))
#            box.SetOwnForegroundColour(self.coulEffRed)
#            box.SetMinSize((30, -1))
#            self.lstBoxEffRed.append(box)
#            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
#            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
#            self.sizerClasse_b.Add(bsizer, flag = wx.EXPAND)
#        
#        for g in range(self.classe.nbrGroupes['E']):
#            box = myStaticBox(self, -1, u"E/P", size = (30, -1))
#            box.SetOwnForegroundColour(self.coulEP)
#            box.SetMinSize((30, -1))
#            self.lstBoxEP.append(box)
#            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
##            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
#            self.sizerEffRed_g.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
#            
#        
#        for g in range(self.classe.nbrGroupes['P']):
#            box = myStaticBox(self, -1, u"AP", size = (30, -1))
#            box.SetOwnForegroundColour(self.coulAP)
#            box.SetMinSize((30, -1))
#            self.lstBoxAP.append(box)
#            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
##            bsizer.Add(wx.Panel(self, -1, size = (20, -1)))
#            self.sizerEffRed_d.Add(bsizer, flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 5)
#        
#        self.Layout()
        
    
    def MiseAJourNbrEleve(self):
        if int(wx.version()[0]) > 2:
            self.boxEffRed.SetLabelText(strEffectifComplet(self.classe, 'G', -1))
        else:
            self.boxEffRed.SetLabel(strEffectifComplet(self.classe, 'G', -1))
            
        self.bmp.SetLargeBitmap(self.getBitmapClasse(640))
        
        
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
            
        if ref.CI_cible:
            self.grid1 = wx.FlexGridSizer( 0, 3, 0, 0 )
        else:
            self.grid1 = wx.FlexGridSizer( 0, 2, 0, 0 )
        

        for i, ci in enumerate(ref.CentresInterets):
#             hs = wx.BoxSizer(wx.HORIZONTAL)
#             if self.CI.maxCI == 1:
#                 if i == 0:
#                     r = wx.RadioButton(panelCI, 200+i, abrevCI+str(i+1), style = wx.RB_GROUP)
#                     r.SetValue(False)
#                 else:
#                     r = wx.RadioButton(panelCI, 200+i, abrevCI+str(i+1))
#                 
#             else:
            r = wx.CheckBox(panelCI, 200+i, abrevCI+str(i+1))
            t = EllipticStaticText(panelCI, -1, "")#ci)#tronquerDC(ci, 50, self))
            r.SetToolTipString(ci)
            t.SetToolTipString(ci)
#             hs.Add(r, flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, border = 1)
#             hs.Add(t, flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border = 4 )
            self.grid1.Add( r, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
            self.grid1.Add( t, 1, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.LEFT, 4 )#|wx.EXPAND
            
            if ref.CI_cible:
                p = wx.TextCtrl(panelCI, -1, u"1")
                p.SetToolTipString(u"Poids horaire relatif du "+ getSingulier(ref.nomCI))
                p.Show(False)
                p.SetMinSize((30, -1))
#                 hs.Add( p, flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT, border = 2)
                self.grid1.Add( p, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT, 2 )
                self.group_ctrls.append((r, t, p))
            else:
                self.group_ctrls.append((r, t))
                
#             self.grid1.Add(hs, flag = wx.EXPAND)
        
        for rtp in self.group_ctrls:
#             if self.CI.maxCI == 1:
#                 self.Bind(wx.EVT_RADIOBUTTON, self.OnCheck, rtp[0] )
#             else:
            self.Bind(wx.EVT_CHECKBOX, self.OnCheck, rtp[0] )
        
        if ref.CI_cible:
            for rtp in self.group_ctrls:
                self.Bind(wx.EVT_TEXT, self.OnPoids, rtp[2] )
        
        
        
        #
        # Séléction du nombre maxi de CI
        #
        self.nCI = wx.SpinCtrl(panelCI, -1, u"Nombre maximum de %s" %ref.nomCI, size = (35, -1))
        self.nCI.SetToolTipString(u"Fixe un nombre maximum de %s sélectionnables.\n" \
                                  u"0 = pas de limite" %ref.nomCI)
        self.nCI.SetRange(0,9)
        self.nCI.SetValue(0)
        self.Bind(wx.EVT_SPINCTRL, self.OnOption, self.nCI)
        self.grid1.Add(self.nCI, flag = wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, border = 5)
#             self.sizer.Add(self.nCI, (0,1), flag = wx.ALL, border = 2)
        self.nCI.Show(ref.maxCI == 0) # maximum pas imposé par le référentiel
            


        #
        # Cas des CI personnalisés
        #
        self.elb = gizmos.EditableListBox(panelCI, -1, 
                                          getSingulierPluriel(ref.nomCI + u" personnalisé(s)", self.CI.maxCI != 1),
                                          size = wx.DefaultSize,
                                          style = gizmos.EL_ALLOW_NEW | gizmos.EL_ALLOW_EDIT | gizmos.EL_ALLOW_DELETE)
        self.elb.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnChangeCI_perso)
        self.elb.SetMinSize((-1, 60))
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnChangeCI_perso)
        self.grid1.Add(self.elb, flag = wx.EXPAND)    
        
        self.grid1.AddGrowableCol(1)
        self.grid1.AddGrowableRow(self.grid1.GetEffectiveRowsCount()-1)
        
        panelCI.SetSizer(self.grid1)
        self.panelCI = panelCI
        self.sizer.Add(panelCI, 1, flag = wx.EXPAND)
#         self.sizer.Add(panelCI, (0,2), (2,1), flag = wx.EXPAND)
        
        
        
        
        #
        # Les Problématiques
        #
        sbpb = myStaticBox(self, -1, getPluriel(ref.nomPb), size = (200,-1))
        sbspb = wx.StaticBoxSizer(sbpb,wx.HORIZONTAL)

        self.panelPb = PanelProblematiques(self, self.CI)
        sbspb.Add(self.panelPb,1, flag = wx.EXPAND)
        self.sizer.Add(sbspb, 0.5, flag = wx.EXPAND)
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
            t.SetLabel(u"")
#         
        self.grid1.Layout()
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
        wx.CallAfter(self.Thaw)
     
        
    


    #############################################################################            
    def OnOption(self, event):
        """ Modification du nombre maxi de CI selectionnables
            (ne peut se produire que si ce nombre n'est pas fixé par le référentiel)
        """
        self.CI.maxCI = self.nCI.GetValue()
#         self.CI.max2CI = not self.CI.max2CI
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
        
        
        
        self.sendEvent(modif = u"Modification des %s abordés" %getPluriel(ref.nomCI))


    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        if self.CI.GetTypeEnseignement() == 'ET':
        self.elb.SetStrings(self.CI.CI_perso)
        
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
            self.sendEvent()



    #############################################################################            
    def GetListeCIActifs(self):
        u""" Renvoie :
            - la liste des indices des boutons "CI" actifs
            - un booléen indiquant si la liste des CI selectionnables est active
        """
#         print "GetListeCIActifs", self.CI.numCI , self.CI.CI_perso
        # Liste des boutons CI à afficher
        ref = self.CI.GetReferentiel()
        if len(self.CI.numCI) + len(self.CI.CI_perso) == 0 or self.CI.maxCI == 0:       # Tous les CI
            l = range(len(ref.CentresInterets))
            p = True    
            
        elif len(self.CI.numCI) + len(self.CI.CI_perso) >= self.CI.maxCI:
            l = self.CI.numCI
            p = False
        
        else:
            l = range(len(ref.CentresInterets))
            p = True
            
#         print "  >>" , l, p
        return l, p
    
    
    
    #############################################################################            
    def GererCases(self, liste, perso, appuyer = False):
        u""" Permet de cacher les cases des CI au fur et à mesure que l'on selectionne des CI
            :param liste: liste des CI à activer
        """ 
#         print "GererCases", perso
        for i, b in enumerate(self.group_ctrls):
            if i in liste:
                b[0].Enable(True)
            else:
                b[0].Enable(False)
                
        self.elb.GetNewButton().Enable(perso)
        
        if appuyer:
            for i, b in enumerate(self.group_ctrls):
                b[0].SetValue(i in self.CI.numCI)
                
    
    #############################################################################            
    def MAJ_CI_perso(self, event = None):
        self.CI.CI_perso = self.elb.GetStrings()
        
        l, p = self.GetListeCIActifs()
        self.GererCases(l, p)
#         print "MAJ_CI_perso", self.CI.CI_perso
        ref = self.CI.GetReferentiel()
        self.sendEvent(modif = u"Modification des %s personnalisés" %getPluriel(ref.nomCI))
        
        
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
        for i, j in enumerate([u"Lundi", u"Mardi", u"Mercredi", u"Jeudi", u"Vendredi", u"Samedi"]):
            nj = wx.StaticText(self, -1, j)
            self.sizer.Add(nj, (0,i), flag = wx.EXPAND)
        
        for seance in self.EDT:
            pass
        
    
    
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
        
        ref = self.CI.GetReferentiel()
        
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
                                     constantes.imagesCI[i].GetBitmap(), 
                                     pos = (centre[0] + ray * sin(ang*pi/180) ,
                                            centre[1] - ray * cos(ang*pi/180)), 
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
        aide.SetToolTipString(u"Informations à propos de la cible des " + getPluriel(ref.nomCI))
        self.Bind(wx.EVT_BUTTON, self.OnAide, aide)
            
            
        bmp = images.Cible.GetBitmap()
        size = (bmp.GetWidth(), bmp.GetHeight())    
        self.SetSize(size)
        self.SetMinSize(size)
    
    
    
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
        dc.DrawBitmap(images.Cible.GetBitmap(), 0, 0)
        evt.Skip()
        
        
    ######################################################################################################
    def OnEraseBackground(self, evt):
        u"""
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
        dc.DrawBitmap(images.Cible.GetBitmap(), 0, 0)    
    
    
    #############################################################################            
    def OnButton(self, event):
        button_selected = event.GetEventObject().GetId()-100
        t = u""
        if event.GetEventObject().IsPressed():
            self.CI.AddNum(button_selected)
            t = u"Ajout d'un CI"
        else:
            try: # sinon probléme avec les doubles clics
                self.CI.DelNum(button_selected)
                t = u"Suppression d'un CI"
            except:
                pass

        self.GererBoutons()
        
        self.Layout()
        self.Parent.group_ctrls[button_selected][0].SetValue(event.GetEventObject().IsPressed())
        self.Parent.sendEvent(modif = t)    
        
        
    #############################################################################            
    def GererBoutons(self, appuyer = False):
        u""" Permet de cacher les boutons des CI au fur et à mesure que l'on selectionne des CI
            Régles :
            - Maximum 2 CI
            - CI voisins sur la cible
            :param appuyer: pour initialisation : si vrai = appuie sur les boutons
            :type appuyer: boolean
        """
#        print "GererBoutons"
        ref = self.CI.GetReferentiel()
        
        # Liste des boutons CI à afficher :
        if len(self.CI.numCI) + len(self.CI.CI_perso) == 0 or self.getMaxCI() == 0:       # Tous les CI
            l = range(len(ref.CentresInterets))   
            p = True          
            
        elif len(self.CI.numCI) + len(self.CI.CI_perso) == self.getMaxCI()-1:
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
            l = self.CI.numCI
            p = self.getMaxCI() > len(l)
            
                
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
        self.lien = lien
        PanelPropriete.__init__(self, parent, objet = self.lien)
        
        self.maxX = 800 # Largeur de l'image "aperçu" zoomée
        self.sequence = self.lien.sequence
        self.classe = None
        self.construire()
        self.parent = parent
        self.MiseAJour()
        
        
    #############################################################################            
    def GetDocument(self):
        return self.lien.parent

    #############################################################################            
    def construire(self):
        
        ref = self.sequence.GetReferentiel()
        
        
        #
        # Intitulé de la séquence
        #
        sbi = myStaticBox(self, -1, u"Intitulé de la Séquence", size = (200,-1))
        sbsi = wx.StaticBoxSizer(sbi,wx.HORIZONTAL)
        self.intit = TextCtrl_Help(self, u"")
        self.intit.SetTitre(u"Intitulé de la Séquence", self.sequence.getIcone())
        self.intit.SetToolTipString(u"")
        sbsi.Add(self.intit,1, flag = wx.EXPAND)
#        self.Bind(wx.EVT_TEXT, self.EvtText, self.intit)
#         self.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.intit)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.intit)
        
        #
        # Sélection du fichier de séquence
        #
        sb0 = myStaticBox(self, -1, u"Fichier de la Séquence", size = (200,-1))
        sbs0 = wx.StaticBoxSizer(sb0,wx.HORIZONTAL)
        self.texte = wx.TextCtrl(self, -1, toSystemEncoding(self.lien.path), size = (250, -1),
                                 style = wx.TE_PROCESS_ENTER)
        bt2 = wx.BitmapButton(self, 101, wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE))
        bt2.SetToolTipString(u"Sélectionner un fichier")
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnText, self.texte)
        self.texte.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocus)
        sbs0.Add(self.texte, flag = wx.ALIGN_CENTER)
        sbs0.Add(bt2)


        #
        # Position de la séquence
        #
        titre = myStaticBox(self, -1, u"Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        self.bmp = wx.StaticBitmap(self, -1, self.sequence.getBitmapPeriode(300))
        self.position = PositionCtrl(self, self.sequence.position, 
                                     ref.periodes)
#         self.Bind(wx.EVT_RADIOBUTTON, self.onChanged)
        self.Bind(wx.EVT_SLIDER, self.onChanged)
        sb.Add(self.bmp, flag = wx.ALIGN_CENTER|wx.EXPAND)
        sb.Add(self.position, flag = wx.ALIGN_CENTER|wx.EXPAND)
        
        
        
        
        #
        # Aperçu de la séquence
        #
        size = (141,200) # Rapport A4
        sb1 = myStaticBox(self, -1, u"Aperçu de la Séquence", size = size)
        sbs1 = wx.StaticBoxSizer(sb1,wx.HORIZONTAL)
        sbs1.SetMinSize(size)
        self.apercu = StaticBitmapZoom(self, -1, size = size)
        self.apercu.SetLargeBitmap(self.sequence.GetApercu(self.maxX))
        sbs1.Add(self.apercu, 1)
        self.size = size
        
        
        #
        # Créneau
        #
        sb2 = myStaticBox(self, -1, u"Créneau horaire")
        sbs2 = wx.StaticBoxSizer(sb2,wx.HORIZONTAL)
        
        self.creneauCtrl = CreneauCtrl(self, self.lien.creneaux)
        sbs2.Add(self.creneauCtrl, 1)
        self.creneauCtrl.SetToolTip(wx.ToolTip(u"Choisir les créneaux horaire de la Séquence"))

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
        sbp = myStaticBox(self, -1, getSingulier(ref.nomPb), size = (200,-1))
        sbsp = wx.StaticBoxSizer(sbp,wx.VERTICAL)
        
        self.panelPb = PanelProblematiques(self, self.sequence.CI)
        
        sbsp.Add(self.panelPb,1, flag = wx.EXPAND)

        #
        # Mise en place
        #
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
        self.sequence.SetPosition(self.position.GetRange())
        self.SetBitmapPosition()
        self.GetDocument().Ordonner()
        t = u"Changement de position de la séquence"
        self.GetDocument().GererDependants(self.sequence, t)
        
        
        
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
        self.sendEvent(modif = u"Modification des créneaux horaire %s %s" % (self.lien.article_c_obj, self.lien.nom_obj))



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
        self.sendEvent(modif = u"Modification des %s abordés" %getPluriel(ref.nomCI))



    #############################################################################            
    def EvtText(self, event):
        print "EvtText"
        if event.GetEventObject() == self.intit:
            self.sequence.SetText(self.intit.GetText())
            self.lien.MiseAJourArbre()
            t = u"Modification de l'intitulé de la séquence"
            self.GetDocument().GererDependants(self.sequence, t)
            
        if self.onUndoRedo():
            self.sendEvent(modif = t)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = t)
                self.eventAttente = True
                             
    #############################################################################            
    def OnLoseFocus(self, event):
        return  
#        self.lien.path = toFileEncoding(self.texte.GetValue())
#        self.MiseAJour()
#        event.Skip()   

    #############################################################################            
    def SetBitmapPosition(self, bougerSlider = None):
        self.bmp.SetBitmap(self.sequence.getBitmapPeriode(300))
        self.position.SetValue(self.sequence.position)
        
    
    
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "MiseAJour PanelPropriete_LienSequence", self.lien

#        self.intit.SetLabel(self.sequence.intitule)
        
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
                self.texte.SetToolTipString(u"Le fichier Séquence est introuvable !")
                return False

        self.texte.SetBackgroundColour("white")
        self.texte.SetToolTipString(u"Lien vers un fichier Séquence")
        
        self.creneauCtrl.MiseAJour()
        
        self.position.MiseAJour()
        self.panelPb.MiseAJour()
        
        self.MiseAJourApercu()
        
       
        if sendEvt:
            print "sendEvent !"
            self.sendEvent()
            
        return True
    
    
    #############################################################################            
    def MiseAJourApercu(self, sendEvt = False):
        #
        # Aperçu
        #
        self.apercu.SetLargeBitmap(self.sequence.GetApercu(self.maxX))
        self.lien.SetLabel()

        self.Layout()
        
        if sendEvt:
            self.sendEvent()
            
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
        
        self.maxX = 800 # Largeur de l'image "aperçu" zoomée
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
        sbi = myStaticBox(self, -1, u"Intitulé du Projet", size = (200,-1))
        sbsi = wx.StaticBoxSizer(sbi,wx.HORIZONTAL)
        self.intit = TextCtrl_Help(self, u"")
        self.intit.SetTitre(u"Intitulé du Projet", self.projet.getIcone())
        self.intit.SetToolTipString(u"")
        
        sbsi.Add(self.intit,1, flag = wx.EXPAND)
#        self.Bind(wx.EVT_TEXT, self.EvtText, self.intit)
#         self.Bind(stc.EVT_STC_CHANGE, self.EvtText, self.intit)
        self.Bind(stc.EVT_STC_MODIFIED, self.EvtText, self.intit)
        
        #
        # Sélection du fichier de Projet
        #
        sb0 = myStaticBox(self, -1, u"Fichier du Projet", size = (200,-1))
        sbs0 = wx.StaticBoxSizer(sb0,wx.HORIZONTAL)
        self.texte = wx.TextCtrl(self, -1, toSystemEncoding(self.lien.path), size = (250, -1),
                                 style = wx.TE_PROCESS_ENTER)
        bt2 = wx.BitmapButton(self, 101, wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE))
        bt2.SetToolTipString(u"Sélectionner un fichier")
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnText, self.texte)
        self.texte.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocus)
        sbs0.Add(self.texte, flag = wx.ALIGN_CENTER)
        sbs0.Add(bt2)


        #
        # Position du Projet
        #
        titre = myStaticBox(self, -1, u"Position")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        self.bmp = wx.StaticBitmap(self, -1, self.projet.getBitmapPeriode(300))
        self.position = PositionCtrl(self, self.projet.position, 
                                     self.projet.GetReferentiel().periodes)
#         self.Bind(wx.EVT_RADIOBUTTON, self.onChanged)
        self.Bind(wx.EVT_SLIDER, self.onChanged)
        sb.Add(self.bmp, flag = wx.ALIGN_CENTER|wx.EXPAND)
        sb.Add(self.position, flag = wx.ALIGN_CENTER|wx.EXPAND)
        
        
        
        
        #
        # Aperçu du Projet
        #
        size = (141,200) # Rapport A4
        sb1 = myStaticBox(self, -1, u"Aperçu du Projet", size = size)
        sbs1 = wx.StaticBoxSizer(sb1,wx.HORIZONTAL)
        sbs1.SetMinSize(size)
        self.apercu = StaticBitmapZoom(self, -1, size = size)
        self.apercu.SetLargeBitmap(self.projet.GetApercu(self.maxX))
        sbs1.Add(self.apercu, 1)
        self.size = size
        
        #
        # Créneau horaire
        #
        sb2 = myStaticBox(self, -1, u"Créneau horaire")
        sbs2 = wx.StaticBoxSizer(sb2,wx.HORIZONTAL)
        
        self.creneauCtrl = CreneauCtrl(self, self.lien.creneaux)
        sbs2.Add(self.creneauCtrl, 1)
        self.creneauCtrl.SetToolTip(wx.ToolTip(u"Choisir les créneaux horaire du projet"))



        #
        # Problématiques associées à(aux) CI/Thème(s)
        #
        sbp = myStaticBox(self, -1, getSingulier(ref.nomPb), size = (200,-1))
        sbsp = wx.StaticBoxSizer(sbp,wx.VERTICAL)
        self.panelPb = TextCtrl_Help(self, u"")
        self.panelPb.SetTitre(ref.nomPb)
        self.panelPb.SetToolTipString(u"")
        
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
        t = u"Changement de position du Projet"
        self.GetDocument().GererDependants(self.projet, t)
        
        
        
    #############################################################################            
    def OnClick(self, event):
        mesFormats = constantes.FORMAT_FICHIER['prj'] + constantes.TOUS_FICHIER
        dlg = wx.FileDialog(self, u"Sélectionner un fichier Projet",
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
        """ Modification du nom du fichier du LienProjet
        """
        self.lien.path = event.GetString()
        self.MiseAJour()
        event.Skip()     

    #############################################################################            
    def OnChangeCreneau(self):
    
        self.sendEvent(modif = u"Modification des créneaux horaire %s %s" % (self.lien.article_c_obj, self.lien.nom_obj))
        
     

    #############################################################################            
    def EvtText(self, event):
        if event.GetEventObject() == self.intit:
            self.projet.SetText(self.intit.GetText())
            self.lien.MiseAJourArbre()
            t = u"Modification de l'intitulé du projet"
            self.GetDocument().GererDependants(self.projet, t)
        
        elif event.GetEventObject() == self.panelPb:
            self.projet.SetProblematique(self.panelPb.GetText())
            self.lien.MiseAJourArbre()
            t = u"Modification de la promblématique du projet"
            self.GetDocument().GererDependants(self.projet, t)
            
        if self.onUndoRedo():
            self.sendEvent(modif = t)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = t)
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
                self.texte.SetToolTipString(u"Le fichier Projet est introuvable !")
                return False
        
        self.texte.SetBackgroundColour("white")
        self.texte.SetToolTipString(u"Lien vers un fichier Projet")
        
        self.creneauCtrl.MiseAJour()
        
        self.position.MiseAJour()
        
        self.MiseAJourApercu()
        
        if sendEvt:
            self.sendEvent()
            
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
            self.sendEvent()
            
        return True
    
    
      
    
    
    
####################################################################################
#
#   Classe définissant le panel de propriété de la compétence
#
####################################################################################
class PanelPropriete_Competences(PanelPropriete):
    def __init__(self, parent, competence, code, compRef, filtre = None):
        """ <competence> : type pysequence.Competences
            <code> : 
            <compRef> : type Referentiel.Competences
           
        """
        self.competence = competence
        self.code = code
        self.compRef = compRef # du type Referentiel.Competences
        
        PanelPropriete.__init__(self, parent, objet = self.competence)
        
#         self.nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
        
#         self.sizer.Add(self.nb, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        
        self.construire(filtre)
        
        self.Layout()
        
        
    ######################################################################################  
    def construire(self, filtre):
        # On efface tout ...
#         self.nb.DeleteAllPages()
        
        # On reconstruit ...
#         ref = self.competence.GetReferentiel()
#         bg_color = self.Parent.GetBackgroundColour()
#         
# #         def getPage():
# #             page = wx.Panel(self.nb, -1)
# #             page.SetBackgroundColour(bg_color) 
# #             pageSizer = wx.BoxSizer(wx.HORIZONTAL)
# #             page.SetSizer(pageSizer)
# #             return page
#             
#         def getNomComp(r):
#             return r.nomCompetences + " " + r.Code
        if self.code == "Fct":
            self.arbre = ArbreFonctionsPrj(self, self.code, None, self.compRef,
                                           self, agwStyle = HTL.TR_NO_HEADER)
            self.sizer.Add(self.arbre, (0,0), flag = wx.EXPAND)
#             self.nb.AddPage(self, self.compRef.nomDiscipline) 
            
        else:
            self.arbre = ArbreCompetences(self, self.code, None, self.compRef,
                                            self, filtre, agwStyle = HTL.TR_NO_HEADER)
            self.sizer.Add(self.arbre, (0,0), flag = wx.EXPAND)
#             self.nb.AddPage(self, self.compRef.nomDiscipline) 
        
#         for code, comp in ref.dicoCompetences.items():
#             self.pagesComp.append(getPage())
#             self.arbres[code] = ArbreCompetences(self.pagesComp[-1], code, None, comp, self, agwStyle = HTL.TR_NO_HEADER)
#             self.pagesComp[-1].GetSizer().Add(self.arbres[code], 1, flag = wx.EXPAND)
#             self.nb.AddPage(self.pagesComp[-1], comp.nomDiscipline) 
#         
        
        
#         if (len(ref.dicFonctions) > 0):
#             #
#             # La page "Fonctions"
#             #
#             pageFct = wx.Panel(self.nb, -1)
#             self.pageFct = pageFct
#             pageFctsizer = wx.BoxSizer(wx.HORIZONTAL)
# 
#             self.arbreFct = ArbreFonctionsPrj(pageFct, ref, self)
#             pageFctsizer.Add(self.arbreFct, 1, flag = wx.EXPAND)
# 
#             pageFct.SetSizer(pageFctsizer)
#             self.nb.AddPage(pageFct, ref.nomFonctions) 
# 
#             self.pageFctsizer = pageFctsizer
        
        self.MiseAJour()
        
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
#         print "AjouterCompetence", code
        self.competence.competences.append(code)
        self.competence.GererElementsDependants(code)
        
    ######################################################################################  
    def EnleverCompetence(self, code, propag = None):
        self.competence.competences.remove(code)
        self.competence.GererElementsDependants(code)
        
    ######################################################################################  
    def SetCompetences(self): 
        
        self.competence.parent.Verrouiller()
        self.sendEvent(modif = u"Ajout/suppression d'une compétence")
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        """ On coche tout ce qui doit l'être dans les différents arbres
        """
#         print u"MiseAJour compétences"
#        print "  ", self.arbre.items.keys()
#        print "   ", self.competence.competences


#         def checkArbre(arbre):
#             print arbre.items.keys()
        self.arbre.UnselectAll()
        for s in self.competence.competences:
            if self.code == s[0]:
#                 print "  ", s
                if s[1:] in self.arbre.items.keys():
                    self.arbre.CheckItem2(self.arbre.items[s[1:]])
        
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
    def __init__(self, parent, savoirs, code, savoirRef):
        
        self.savoirs = savoirs
        self.savoirRef = savoirRef
        self.code = code
        self.prerequis = savoirs.prerequis
        
        PanelPropriete.__init__(self, parent, objet = self.savoirs)
        
#         self.nb = wx.Notebook(self, -1, size = (21,21), style= wx.BK_DEFAULT)
        
#         self.sizer.Add(self.nb, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(0)
            
        self.construire()
        
        self.Layout()


    #############################################################################            
    def GetDocument(self):
        return self.savoirs.parent


#     ######################################################################################  
#     def CreerPage(self, nom):
#         bg_color = self.Parent.GetBackgroundColour()
#         page = PanelPropriete(self.nb, objet = self.savoirs)
#         page.SetBackgroundColour(bg_color)
#         self.nb.AddPage(page, nom)
#         return page


    ######################################################################################  
    def construire(self):
#         print "Construire Savoirs", self.prerequis
#        print self.GetDocument().GetReferentiel()
        
#         # On efface tout ...
#         self.nb.DeleteAllPages()
#         
#         self.pagesSavoir = []
#         self.arbres = {}
        
#         ref = self.GetDocument().GetReferentiel()
#        print "   ", ref.listSavoirs
        # On reconstruit ...
#         dicSavoirs = [(c, ref.dicoSavoirs[c]) for c in ref.listSavoirs]
#         if ref.tr_com != []:
#             # Il y a un tronc comun (ETT pour Spécialité STI2D par exemple)
#             r = REFERENTIELS[ref.tr_com[0]]
#             dicSavoirs.insert(1, ("B", r.dicoSavoirs["S"]))
#             dicSavoirs.extend([(c, r.dicoSavoirs[c]) for c in r.dicoSavoirs.keys() if c != "S"])
        
#         savoir = ref.getTousSavoirs()[self.code]
        
#         for code, savoir in dicSavoirs:
        if (self.prerequis and self.savoirRef.pre) or (not self.prerequis and self.savoirRef.obj):
#                 self.pagesSavoir.append(self.CreerPage(savoir.nomDiscipline))
            self.arbre = ArbreSavoirs(self, self.code, self.savoirRef, self.savoirs, self.prerequis)
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
        
        self.Layout()
    

    ######################################################################################  
    def SetSavoirs(self): 
        self.savoirs.parent.Verrouiller()
        self.sendEvent(modif = u"Ajout/suppression d'un Savoir")
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        """ Coche tous les savoirs a True de self.savoirs.savoirs 
            dans les différents arbres
        """
#         print "MiseAJour Savoirs", self.arbre
#         print self.code

        if hasattr(self, 'arbre'):
            for s in self.savoirs.savoirs:
                if self.code == s[0]:
                    i = self.arbre.get_item_by_label(s[1:], self.arbre.GetRootItem())
                    if i.IsOk():
                        self.arbre.CheckItem2(i)
                
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
            self.sendEvent()
            
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
        
        
        ref = self.seance.GetReferentiel()
        
        #
        # Un notebook pour les différentes catégories de propriété
        #
        self.nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
        pageGen = PanelPropriete(self.nb, panelRacine = self, objet = self.seance)
        self.pageGen = pageGen
        bg_color = self.Parent.GetBackgroundColour()
        pageGen.SetBackgroundColour(bg_color)
#         self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.nb.AddPage(pageGen, u"Propriétés générales")
        self.sizer.Add(self.nb, (0,0), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        
        
         
        
        #
        # Intitulé de la séance
        #
        box = myStaticBox(pageGen, -1, u"Intitulé "+self.seance.article_c_obj+u" "+self.seance.nom_obj)
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
#         textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        textctrl = orthographe.STC_ortho(pageGen, -1)
        textctrl.SetTitre(u"Intitulé "+self.seance.article_c_obj+u" "+self.seance.nom_obj)
        textctrl.SetToolTipString(u"")
        
        
        bsizer.Add(textctrl, 1, flag = wx.EXPAND)
        self.textctrl = textctrl
#        self.Bind(wx.EVT_TEXT, self.EvtTextIntitule, textctrl)
#         self.textctrl.Bind(wx.EVT_LEAVE_WINDOW, self.EvtTextIntitule)
        self.textctrl.Bind(wx.EVT_KILL_FOCUS, self.EvtTextIntitule)
        pageGen.sizer.Add(bsizer, (0,0), (3,1), flag = wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, border = 2)    
        
        
        
        
        #
        # Type de séance
        #
        titre = wx.StaticText(pageGen, -1, u"Type de %s :" %self.seance.nom_obj)
        listType = self.seance.GetListeTypes()
        listTypeS = [(ref.seances[t][1], scaleImage(constantes.imagesSeance[t].GetBitmap())) for t in listType] 
        tsizer = wx.BoxSizer(wx.VERTICAL)
        cbType = wx.combo.BitmapComboBox(pageGen, -1, u"Choisir un type de %s" %self.seance.nom_obj,
                             choices = [], size = (-1,25),
                             style = wx.CB_DROPDOWN
                             | wx.TE_PROCESS_ENTER
                             | wx.CB_READONLY
                             #| wx.CB_SORT
                             )
        
        self.cbType = cbType
        for s in listTypeS:
            self.cbType.Append(s[0], s[1])
            
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbType)
        
        
        tsizer.Add(titre, flag = wx.ALIGN_BOTTOM | wx.ALIGN_LEFT|wx.LEFT, border = 2)
        tsizer.Add(cbType, flag = wx.EXPAND|wx.LEFT, border = 2)
        pageGen.sizer.Add(tsizer, (3,0), flag = wx.EXPAND|wx.ALL, border = 2)
       
        
       
       
        #
        # Organisation
        #
        box2 = myStaticBox(pageGen, -1, u"Organisation")
        self.bsizer2 = wx.StaticBoxSizer(box2, wx.VERTICAL)
        pageGen.sizer.Add(self.bsizer2, (0,1), (2,1), flag =wx.ALL|wx.EXPAND, border = 2)
        
        # reste déplacé dans AdapterAuType()

        


        #
        # Démarche
        #
        self.demSizer = wx.BoxSizer(wx.VERTICAL)
        pageGen.sizer.Add(self.demSizer, (3,1), (1,1), flag = wx.EXPAND|wx.ALL, border = 2)
        
        # reste déplacé dans AdapterAuType()
        
        
        #
        # Systèmes
        #
        self.box = myStaticBox(pageGen, -1, u"Systèmes ou matériels nécessaires", size = (200,200))
        self.box.SetMinSize((200,200))
        self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        self.systemeCtrl = []
        self.ConstruireListeSystemes()
        pageGen.sizer.Add(self.bsizer, (0,2), (4, 1), flag = wx.EXPAND|wx.ALL, border = 2)
    

        #
        # Lien
        #
        lsizer = self.CreateLienSelect(pageGen)
        pageGen.sizer.Add(lsizer, (2,3), (2, 1), flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        
        #
        # Description de la séance
        #
        dbox = myStaticBox(pageGen, -1, u"Description")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
#        bd = wx.Button(self, -1, u"Editer")
        tc = richtext.RichTextPanel(pageGen, self.seance, toolBar = True)
        tc.SetTitre(u"Description détaillée de la Séance")
        tc.SetToolTipString(u"")
#        tc.SetMaxSize((-1, 150))
#        dbsizer.Add(bd, flag = wx.EXPAND)
        dbsizer.Add(tc, 1, flag = wx.EXPAND)
#        self.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        pageGen.sizer.Add(dbsizer, (0,3), (2, 1), flag = wx.EXPAND|wx.ALL, border = 2)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        pageGen.sizer.SetEmptyCellSize((0,0))
        
        
        
        
        #
        # Proprietés d'affichage
        #
        pageAff = PanelPropriete(self.nb, panelRacine = self, objet = self.seance)
        pageAff.SetBackgroundColour(bg_color)
        self.nb.AddPage(pageAff, u"Apparence")
        
        #
        # Apparence
        #
        
        box2 = myStaticBox(pageAff, -1, u"Affichage de l'intitulé")
        bsizer3 = wx.StaticBoxSizer(box2, wx.VERTICAL)
        
        b = csel.ColourSelect(pageAff, -1, u"Couleur du texte", couleur.GetCouleurWx(self.seance.couleur), size = (200,-1))
        
        bsizer3.Add(b, flag = wx.ALL, border = 2)
        
        b.Bind(csel.EVT_COLOURSELECT, self.OnSelectColour)
        self.coulCtrl = b
        
        cb = wx.CheckBox(pageAff, -1, u"Afficher l'intitulé dans la zone de déroulement")
#         print "+++", cb.Value
        cb.SetToolTipString(u"Décocher pour afficher l'intitulé\nen dessous de la zone de déroulement de la séquence")
        cb.SetValue(self.seance.intituleDansDeroul)
        bsizer3.Add(cb, flag = wx.EXPAND|wx.ALL, border = 2)
        
        vcTaille = VariableCtrl(pageAff, seance.taille, signeEgal = True, slider = False, sizeh = 40,
                                help = u"Taille des caractères", unite = u"%")
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
                                        titre = u"Illustration "+self.seance.article_c_obj+u" "+self.seance.nom_obj)
        pageAff.sizer.Add(isizer, (0,2), (1,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.ALL, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        
        
        
        
#        self.sizer.Layout()
#        self.Layout()
    
        self.AdapterAuType()
        self.MiseAJour()
        
        #
        # Mise en place
        #
        pageGen.sizer.AddGrowableCol(3)
        pageGen.sizer.AddGrowableRow(0)

        pageAff.sizer.AddGrowableCol(1)
        pageAff.sizer.AddGrowableRow(0, 1)
        
    
        #############################################################################            
    def AdapterAuType(self):
        """ Adapte le panel au type de séance
        """
#         print "AdapterAuType", self.seance

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
        
        if not self.seance.typeSeance in ["R", "S"]:
            vcDuree = VariableCtrl(self.pageGen, self.seance.duree, coef = 0.25, 
                                   signeEgal = True, slider = False, sizeh = 30,
                                   help = u"Durée de la séance en heures", unite = u"h")
            self.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
            self.vcDuree = vcDuree
            self.bsizer2.Add(vcDuree, flag = wx.EXPAND|wx.LEFT|wx.BOTTOM, border = 2)

        
        
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
        
        if self.seance.typeSeance in ref.effectifsSeance.keys():
            titre = wx.StaticText(self.pageGen, -1, u"Effectif : ")
            
            cbEff = wx.ComboBox(self.pageGen, -1, u"",
                             choices = [],
                             style = wx.CB_DROPDOWN
                             | wx.TE_PROCESS_ENTER
                             | wx.CB_READONLY
                             #| wx.CB_SORT
                             )
            self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxEff, cbEff)
            self.cbEff = cbEff
            self.cbEff.Clear()
            listEff = ref.effectifsSeance[self.seance.typeSeance]
            for s in listEff:
                self.cbEff.Append(strEffectifComplet(self.seance.GetDocument().classe, s, -1))
            self.cbEff.SetSelection(0)
            
            self.titreEff = titre
            
            self.bsizer2.Add(self.titreEff, flag = wx.ALIGN_BOTTOM|wx.LEFT, border = 2)
            self.bsizer2.Add(cbEff, flag = wx.EXPAND|wx.LEFT, border = 2)
            
    
        
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
                                    help = u"Nombre de groupes réalisant simultanément la même séance")
            self.Bind(EVT_VAR_CTRL, self.EvtText, vcNombre)
            self.vcNombre = vcNombre
            self.bsizer2.Add(vcNombre, flag = wx.EXPAND|wx.ALL, border = 2)
            
                
            
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
                                    help = u"Nombre de rotations successives")
            self.Bind(EVT_VAR_CTRL, self.EvtText, vcNombreRot)
            self.vcNombreRot = vcNombreRot
            self.bsizer2.Add(vcNombreRot, flag = wx.EXPAND|wx.ALL, border = 2)

            

        
        #
        # Démarche      
        #
        if hasattr(self, 'cbDem'):
#             try:
            self.demSizer.Detach(self.cbDem)
            self.demSizer.Detach(self.titreDem)
#             except:
#                 pass
            self.cbDem.Destroy()
            self.titreDem.Destroy()
            del self.cbDem
            del self.titreDem
        
        if self.seance.typeSeance in ref.activites.keys():
            if len(ref.demarches) > 0:
                
                listDem = ref.demarcheSeance[self.seance.typeSeance]
                titre = wx.StaticText(self.pageGen, -1, u"Démarche :")
                cbDem = wx.ComboBox(self.pageGen, -1, u"",
                                 choices = [],
                                 style = wx.CB_DROPDOWN
                                 | wx.TE_PROCESS_ENTER
                                 | wx.CB_READONLY
                                 #| wx.CB_SORT
                                 )
                self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxDem, cbDem)
                self.cbDem = cbDem
                
                for s in listDem:
                    self.cbDem.Append(ref.demarches[s][1])

                self.titreDem = titre
                
                
                self.demSizer.Add(titre, flag = wx.ALIGN_BOTTOM|wx.ALIGN_LEFT|wx.LEFT, border = 2)
                self.demSizer.Add(cbDem, flag = wx.EXPAND|wx.LEFT, border = 2)
                self.demSizer.Layout()
                
        
#                 
#                 
#         self.bsizer2.Layout()
        self.pageGen.sizer.Layout()
        


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
        if self.seance.typeSeance in ACTIVITES:
            for ss in self.systemeCtrl:
                self.bsizer.Detach(ss)
                ss.Destroy()
                
            self.systemeCtrl = []
            for s in self.seance.systemes:
#                print "   ", type(s), "---", s
                v = VariableCtrl(self.pageGen, s, signeEgal = False, 
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
        self.seance.couleur = couleur.Wx2Couleur(event.GetValue())
        self.sendEvent(modif = u"Mofification de la couleur de la séance")
        
    #############################################################################            
    def EvtVarSysteme(self, event):
        self.sendEvent(modif = u"Modification du nombre de systèmes nécessaires")
        
    #############################################################################            
    def EvtCheckBox(self, event):
        self.seance.intituleDansDeroul = event.IsChecked()
        self.sendEvent(modif = u"Ajout/Suppression d'un système nécessaire")
    
    #############################################################################            
    def EvtTextIntitule(self, event):
        
        txt = self.textctrl.GetValue()
        
        if self.seance.intitule != txt:
            self.seance.SetIntitule(txt)
            event.Skip()
    #         print "EvtTextIntitule", self.textctrl.GetValue()
            modif = u"Modification de l'intitulé de la Séance"
            if self.onUndoRedo():
                self.sendEvent(modif = modif)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif)
                    self.eventAttente = True
            
    
    #############################################################################            
    def EvtText(self, event):
        t = u""
        if event.GetId() == self.vcDuree.GetId():
            self.seance.SetDuree(event.GetVar().v[0])
            t = u"Modification de la durée de la Séance"
        
        elif event.GetId() == self.vcNombre.GetId():
            self.seance.SetNombre(event.GetVar().v[0])
            t = u"Modification du nombre de groupes réalisant simultanément la méme séance"
        
        elif event.GetId() == self.vcNombreRot.GetId():
            self.seance.SetNombreRot(event.GetVar().v[0])
            t = u"Modification du nombre de rotations successives"
            
        elif event.GetId() == self.vcTaille.GetId():
            self.seance.SetTaille(event.GetVar().v[0])
            t = u"Modification de la taille des caractères"
        
        if self.onUndoRedo():
            self.sendEvent(modif = t)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = t)
                self.eventAttente = True

    #############################################################################            
    def EvtComboBox(self, event):
#        print "EvtComboBox"

        # On s'apprète à changer une séance Rotation ou Série en séance "Normale"
        if self.seance.typeSeance in ["R", "S"] \
          and self.GetReferentiel().listeTypeSeance[event.GetSelection()] not in ["R", "S"]:
            dlg = wx.MessageDialog(self, u"Cette Séance contient des sous-séances !\n\n" \
                                   u"Modifier le type de cette séance entrainera la suppression de toutes les sous séances !\n" \
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
        
        deja = self.seance.typeSeance in ACTIVITES
#        print self.GetReferentiel().seances
#        print self.cbType.GetStringSelection()

        self.seance.SetType(get_key(self.GetReferentiel().seances, 
                                    self.cbType.GetStringSelection(), 1))
        self.seance.GetDocument().OrdonnerSeances()
        self.AdapterAuType()
        
        if self.seance.typeSeance in ACTIVITES:
            if not deja:
                for sy in self.seance.GetDocument().systemes:
                    self.seance.AjouterSysteme(nom = sy.nom, construire = False)
        else:
            self.seance.systemes = []
            
#        if self.cbEff.IsEnabled() and self.cbEff.IsShown():
        self.seance.SetEffectif(self.cbEff.GetStringSelection())
        

        
        self.ConstruireListeSystemes()
        self.Layout()
#        print "ok"
        self.sendEvent(modif = u"Modification du type de Séance")
       
        
        
    #############################################################################            
    def EvtComboBoxEff(self, event):
        self.seance.SetEffectif(event.GetString())  
        self.sendEvent(modif = u"Modification de l'effectif de la Séance")



    #############################################################################            
    def EvtComboBoxDem(self, event):
        self.seance.SetDemarche(event.GetString())  
        self.sendEvent(modif = u"Modification de la démarche de la Séance")
       
       
        
#     #############################################################################            
#     def OnClick(self, event):
#         self.seance.AfficherLien(self.GetDocument().GetPath())
        
    
    
            
            
    
        
        
    #############################################################################            
    def MarquerProblemeDuree(self, etat):
        return
#        self.vcDuree.marquerValid(etat)
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "MiseAJour PP séance"
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
            self.cbEff.SetSelection(ref.findEffectif(self.cbEff.GetStrings(), self.seance.effectif))
        
#         if self.cbDem.IsShown():#self.cbDem.IsEnabled() and :
#            print ref.demarches[self.seance.demarche][1]
#            print self.cbDem.GetStrings()
#            print self.seance
        if hasattr(self, 'cbDem'):
            self.cbDem.SetSelection(self.cbDem.GetStrings().index(ref.demarches[self.seance.demarche][1]))
            
        if self.seance.typeSeance in ACTIVITES:
            if hasattr(self, 'vcNombre'):
                self.vcNombre.mofifierValeursSsEvt()
        elif self.seance.typeSeance == "R":
            if hasattr(self, 'vcNombreRot'):
                self.vcNombreRot.mofifierValeursSsEvt()
        
        self.vcTaille.mofifierValeursSsEvt()
        
        self.cbInt.SetValue(self.seance.intituleDansDeroul)
        if sendEvt:
            self.sendEvent()
        
        self.MiseAJourLien()
        
        self.ConstruireListeSystemes()
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(toSystemEncoding(self.seance.lien.path), 
                           marquerModifier = False)
#         self.btnlien.Show(self.seance.lien.path != "")
        self.sizer.Layout()
        

    
    
    
    
    
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
           and not (tache.phase in TOUTES_REVUES_EVAL and (True in ref.compImposees.values())): #tache.GetReferentiel().compImposees['C']):
            #
            # La page "Généralités"
            #
            self.nb = wx.Notebook(self, -1,  size = (21,21), style= wx.BK_DEFAULT)
            pageGen = PanelPropriete(self.nb, objet = self.tache)
            bg_color = self.Parent.GetBackgroundColour()
            pageGen.SetBackgroundColour(bg_color)
            self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
            self.nb.AddPage(pageGen, u"Propriétés générales")
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
        prj = self.tache.GetProjetRef()
#        lstPhases = [p[1] for k, p in ref.phases_prj.items() if not k in ref.listPhasesEval_prj]
        lstPhases = [prj.phases[k][1] for k in prj.listPhases if not k in prj.listPhasesEval]
        
        titre = wx.StaticText(pageGen, -1, u"Phase :")
        pageGen.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 5)
        
        if tache.phase in TOUTES_REVUES_SOUT:
            txtPhas = wx.StaticText(pageGen, -1, prj.phases[tache.phase][1])
            pageGen.sizer.Add(txtPhas, (0,1), (1,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, border = 5)
            
        elif tache.estPredeterminee():
            txtPhas = wx.StaticText(pageGen, -1, u"")
            pageGen.sizer.Add(txtPhas, (0,1), (1,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, border = 5)
            self.txtPhas = txtPhas
            
        else:
            cbPhas = wx.combo.BitmapComboBox(pageGen, -1, u"Sélectionner la phase",
                                 choices = lstPhases,
                                 style = wx.CB_DROPDOWN
                                 | wx.TE_PROCESS_ENTER
                                 | wx.CB_READONLY
                                 #| wx.CB_SORT
                                 )

            for i, k in enumerate(sorted([k for k in prj.phases.keys() if not k in prj.listPhasesEval])):#ref.listPhases_prj):
                cbPhas.SetItemBitmap(i, scaleImage(constantes.imagesTaches[k].GetBitmap()))
            pageGen.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbPhas)
            self.cbPhas = cbPhas
            
            pageGen.sizer.Add(cbPhas, (0,1), flag = wx.EXPAND|wx.ALL, border = 2)
        

        
        #
        # Intitulé de la tache
        #
        if not tache.phase in TOUTES_REVUES_EVAL_SOUT:
            box = myStaticBox(pageGen, -1, u"Intitulé de la tâche")
            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            self.boxInt = box
            if not tache.estPredeterminee():
                textctrl = orthographe.STC_ortho(pageGen, -1)#, u"", style=wx.TE_MULTILINE)
                
                textctrl.SetTitre(u"Intitulé de la tâche", tache.getIcone())
                textctrl.SetToolTipString(u"Donner l'intitulé de la tâche\n"\
                                          u" = un simple résumé !\n\n" \
                                          u"les détails doivent figurer dans la zone\n" \
                                          u"\"Description détaillée de la tâche\"")
                bsizer.Add(textctrl,1, flag = wx.EXPAND)
                self.textctrl = textctrl
#                 self.textctrl.Bind(wx.EVT_LEAVE_WINDOW, self.EvtTextIntitule)
                self.textctrl.Bind(wx.EVT_KILL_FOCUS, self.EvtTextIntitule)
                
                
            else:
                cc = TreeCtrlComboBook(pageGen, self.tache, self.EvtComboBoxTache)
                bsizer.Add(cc, 1, flag = wx.EXPAND)
                self.cbTache = cc

            pageGen.sizer.Add(bsizer, (1,0), (1,2), 
                               flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT, border = 2)    


        #
        # Durée de la tache
        #
        if not tache.phase in TOUTES_REVUES_EVAL_SOUT:
            vcDuree = VariableCtrl(pageGen, tache.duree, coef = 0.5, signeEgal = True, slider = False,
                                   help = u"Volume horaire de la tâche, en heures")#, sizeh = 60)
            pageGen.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
            self.vcDuree = vcDuree
            pageGen.sizer.Add(vcDuree, (2,0), (1, 2), flag = wx.EXPAND|wx.ALL, border = 2)


        #
        # Icones
        #
        if not tache.phase in TOUTES_REVUES_EVAL_SOUT:
            isizer = self.CreateIconeSelect(pageGen)
            pageGen.sizer.Add(isizer, (0,2), (3, 1), 
                              flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 4)
            pageGen.sizer.AddGrowableCol(2)

            
#             ib = myStaticBox(pageGen, -1, u"Icônes")
#             ibsizer = wx.StaticBoxSizer(ib, wx.VERTICAL)
#             ims = wx.WrapSizer()
#             
# #             ims.SetSize((100,-1))
#             self.icones = []
#             for i, (nom, img) in enumerate(constantes.ICONES_TACHES.items()):
#                 ico = img.ConvertToImage().Scale(20, 20).ConvertToBitmap()
#                 btn = wx.BitmapButton(pageGen, 100+i, ico)
#                 btn.SetToolTipString(nom)
#                 self.icones.append(nom)
#                 ims.Add(btn, flag = wx.ALL, border = 2)
#                 btn.Refresh()
#                 self.Bind(wx.EVT_BUTTON, self.OnIconeClick, btn)
#             
#             ibsizer.Add(ims)
#             
#             self.btn_no_icon = wx.Button(pageGen, -1, u"Aucune")
#             ibsizer.Add(self.btn_no_icon)
#             self.Bind(wx.EVT_BUTTON, self.OnIconeClick, self.btn_no_icon)
#             
#             pageGen.sizer.Add(ibsizer, (0,2), (3, 1), 
#                               flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 4)
#             pageGen.sizer.AddGrowableCol(2)

        #
        # Elèves impliqués
        #
        if not tache.phase in TOUTES_REVUES_EVAL_SOUT:
            self.box = myStaticBox(pageGen, -1, u"Elèves impliqués")
#            self.box.SetMinSize((150,-1))
            self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
            self.elevesCtrl = []
            self.ConstruireListeEleves()
            pageGen.sizer.Add(self.bsizer, (0,3), (3, 1), flag = wx.EXPAND|wx.LEFT|wx.RIGHT, border = 4)
#             pageGen.sizer.AddGrowableCol(3)
        
        
        
        #
        # Description de la tâche
        #
        dbox = myStaticBox(pageGen, -1, u"Description détaillée de la tâche")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
#        bd = wx.Button(pageGen, -1, u"Editer")
        tc = richtext.RichTextPanel(pageGen, self.tache, toolBar = True)
        tc.SetToolTipString(u"Donner une description détaillée de la tâche :\n" \
                            u" - les conditions nécessaires\n" \
                            u" - ce qui est fourni\n" \
                            u" - les résultats attendus\n" \
                            u" - les différentes étapes\n" \
                            u" - la répartition du travail entre les élèves\n"\
                            u" - ...")
        tc.SetTitre(u"Description détaillée de la tâche")
     

#        tc.SetMaxSize((-1, 150))
#        tc.SetMinSize((150, 60))
        dbsizer.Add(tc,1, flag = wx.EXPAND)
#        dbsizer.Add(bd, flag = wx.EXPAND)
#        pageGen.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        if tache.phase in TOUTES_REVUES_EVAL_SOUT:
            pageGen.sizer.Add(dbsizer, (1,0), (2, 2), flag = wx.EXPAND)
            pageGen.sizer.AddGrowableCol(0)
        else:
            pageGen.sizer.Add(dbsizer, (0,4), (3, 1), flag = wx.EXPAND)
            pageGen.sizer.AddGrowableCol(4)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        pageGen.sizer.AddGrowableRow(1)
        
        
        self.ConstruireCompetences()
        self.ConstruireCasesEleve()
        self.MiseAJour()
        
            
##        print ">>>", tache.phase, tache.projet.getCodeLastRevue()
#        if not tache.phase in [tache.projet.getCodeLastRevue(), _S] \
#           and not (tache.phase in TOUTES_REVUES_EVAL and (True in ref.compImposees.values())): #tache.GetReferentiel().compImposees['C']):
#            nb.AddPage(pageGen, u"Propriétés générales")
#
#            #
#            # Les pages "Compétences"
#            #
#            self.arbres = {}
#            self.pagesComp = []
#            
#            for code, dicComp in prj._dicoCompetences.items():
#                self.pagesComp.append(wx.Panel(nb, -1))
#                comp = ref.dicoCompetences[code]
#                pageComsizer = wx.BoxSizer(wx.HORIZONTAL)
#                
#                self.arbres[code] = ArbreCompetencesPrj(self.pagesComp[-1], code, dicComp, comp, self,
#                                                 revue = self.tache.phase in TOUTES_REVUES_SOUT, 
#                                                 eleves = (self.tache.phase in TOUTES_REVUES_EVAL_SOUT \
#                                                           or self.tache.estPredeterminee()))
#                
#                pageComsizer.Add(self.arbres[code], 1, flag = wx.EXPAND)
#                self.pagesComp[-1].SetSizer(pageComsizer)
#                nb.AddPage(self.pagesComp[-1], comp.nomGenerique + u" à mobiliser :" + comp.abrDiscipline) 
#                
#                self.pageComsizer = pageComsizer
#            

        
        #
        # Mise en place
        #
#         self.Layout()
#         self.FitInside()
#        wx.CallAfter(self.PostSizeEvent)
#         self.Show()
        self.Refresh()
#        wx.CallAfter(self.Layout)
        
#    ####################################################################################
#    def getListTaches(self): 
#        """ Renvoie la liste des tâches encore disponibles = pas déja sélectionnées
#        """
#        prj = self.tache.GetProjetRef()
#        l = [t+" "+prj.taches[t][1] for t in prj.listTaches if not t in [tt.intitule for tt in self.tache.projet.taches]]
#        return l
     
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
                for arbre in self.arbres.values():
                    arbre.MiseAJour(competence, self.tache.indicateursEleve[0][competence])
            else:
                prj = self.tache.GetProjetRef()
                for arbre in self.arbres.values():
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
#        print "SetCompetences"
        
        self.GetDocument().MiseAJourDureeEleves()
        
        modif = u"Ajout/Suppression d'une compétence à la Tâche"
        if self.onUndoRedo():
            self.sendEvent(modif = modif)
        else:
            wx.CallAfter(self.sendEvent, modif = modif)
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
           and not (self.tache.phase in TOUTES_REVUES_EVAL and (True in ref.compImposees.values())): #tache.GetReferentiel().compImposees['C']):
            
#            print "ConstruireCompetences", self.tache, ref, prj

            #
            # Les pages "Compétences"
            #
            self.arbres = {}
            self.pagesComp = []
            
            for code, dicComp in prj._dicoCompetences.items():
                self.pagesComp.append(wx.Panel(self.nb, -1))
                comp = ref.dicoCompetences[code]
                pageComsizer = wx.BoxSizer(wx.HORIZONTAL)
                
                self.arbres[code] = ArbreCompetencesPrj(self.pagesComp[-1], code, dicComp, comp, self,
                                                 revue = self.tache.phase in TOUTES_REVUES_SOUT, 
                                                 eleves = (self.tache.phase in TOUTES_REVUES_EVAL_SOUT \
                                                           or self.tache.estPredeterminee()))
                
                pageComsizer.Add(self.arbres[code], 1, flag = wx.EXPAND)
                self.pagesComp[-1].SetSizer(pageComsizer)
                self.nb.AddPage(self.pagesComp[-1], getPluriel(comp.nomGenerique) + u" à mobiliser : " + comp.abrDiscipline) 
                
                self.pageComsizer = pageComsizer
            
            


    ############################################################################            
    def ConstruireListeEleves(self):
        """ Ajout des cases "élève" :
             - sur la page "Proprietes générale"
             - sur les pages "Compétences" : cas des revues (sauf dernière(s)) et des compétences prédéterminées
        """
#         print "ConstruireListeEleves", self.tache
        if hasattr(self, 'elevesCtrl'):
            
            self.pageGen.Freeze()
            
            for ss in self.elevesCtrl:
                self.bsizer.Detach(ss)
                ss.Destroy()
                
            self.elevesCtrl = []

            for i, e in enumerate(self.GetDocument().eleves + self.GetDocument().groupes):
                v = wx.CheckBox(self.pageGen, 100+i, e.GetNomPrenom())
#                 v.SetMinSize((200,-1))
                v.SetValue(i in self.tache.eleves)
                self.pageGen.Bind(wx.EVT_CHECKBOX, self.EvtCheckEleve, v)
                self.bsizer.Add(v, flag = wx.ALIGN_LEFT|wx.ALL, border = 3)#|wx.EXPAND) 
                self.elevesCtrl.append(v)
            
            line = wx.StaticLine(self.pageGen)
            self.bsizer.Add(line, 0, flag = wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, border = 3)#)  size = (100,3))
            
            self.tousElevesCtrl = wx.CheckBox(self.pageGen, -1, u"tous")
            self.tousElevesCtrl.SetValue(all([b.IsChecked() for b in self.elevesCtrl]))
            self.bsizer.Add(self.tousElevesCtrl, flag = wx.ALIGN_LEFT|wx.ALL, border = 3)#|wx.EXPAND) 
            self.pageGen.Bind(wx.EVT_CHECKBOX, self.EvtCheckEleve, self.tousElevesCtrl)
            
            self.bsizer.Layout()
            
            if len(self.GetDocument().eleves + self.GetDocument().groupes) > 0:
                self.box.Show(True)
            else:
                self.box.Hide()
    
#            self.box.SetMinSize((200,200))
            self.bsizer.Layout()
            self.pageGen.Thaw()
#             print [cb.GetSize()[0] for cb in self.elevesCtrl]
#             line.SetSize((max([cb.GetSize()[0] for cb in self.elevesCtrl]), 3))
            
        self.ConstruireCasesEleve()
        
        
        
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
        for i in range(len(self.GetDocument().eleves) + len(self.GetDocument().groupes)):
            if self.elevesCtrl[i].IsChecked():
                lst.append(i)
        
        self.tache.eleves = lst
#         print "    ", lst
        
        self.GetDocument().MiseAJourDureeEleves()
#        self.GetDocument().MiseAJourTachesEleves()
        
        self.ConstruireCasesEleve()
        self.sendEvent(modif = u"Changement d'élève concerné par la tâche")    


    #############################################################################            
    def EvtTextIntitule(self, event):
#         print "EvtTextIntitule"
        txt = self.textctrl.GetValue()
        
        if self.tache.intitule != txt:
            self.tache.SetIntitule(txt)
            modif = u"Modification de l'intitulé de la Tâche"
            if self.onUndoRedo():
                self.sendEvent(modif = modif)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif)
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
        for arbre in self.arbres.values():
            arbre.ReConstruire()
        
        #
        # Marquer UNDO
        #
        modif = u"Modification de l'intitulé de la Tâche"
        if self.onUndoRedo():
            self.sendEvent(modif = modif)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = modif)
                self.eventAttente = True
                
#        self.ccTache.SetTextCtrlStyle(wx.TE_READONLY|wx.TE_WORDWRAP|wx.TE_MULTILINE)
#        event.Skip()
                    
    #############################################################################            
    def EvtText(self, event):
        """ Modification de la durée de la Tâche
        """
        t = u""
        if event.GetId() == self.vcDuree.GetId():
            self.tache.SetDuree(event.GetVar().v[0])
            t = u"Modification de la durée de la Tâche"
#        elif event.GetId() == self.vcNombre.GetId():
#            self.tache.SetNombre(event.GetVar().v[0])
#            t = u"Modification de la durée de la Tâche"
    
        if self.onUndoRedo():
            self.sendEvent(modif = t)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = t)
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
            for arbre in self.arbres.values():
                arbre.MiseAJourPhase(newPhase)
            self.pageGen.Layout()
            self.sendEvent(modif = u"Changement de phase de la Tâche")
        
    
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
    def MiseAJour(self, sendEvt = False):
#        print "MiseAJour panelPropriete Tache"
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
        if hasattr(self, 'cbTache'):
            if self.tache.intitule in prj.taches.keys():
                self.cbTache.SetLabel(self.tache.intitule+"\n"+prj.taches[self.tache.intitule][1])
        
        #
        # Phase de la tâche
        #
        if hasattr(self, 'txtPhas'):
            if self.tache.intitule in prj.taches.keys():
                self.txtPhas.SetLabel(prj.phases[prj.taches[self.tache.intitule][0]][1])
            else:
                self.txtPhas.SetLabel(u"")
        
        if hasattr(self, 'cbPhas') and self.tache.phase != '':
#            print self.tache.phase
#            print self.tache.GetProjetRef().phases[self.tache.phase][1]
            try:
                self.cbPhas.SetStringSelection(self.tache.GetProjetRef().phases[self.tache.phase][1])
            except:
                print "Erreur : conflit de type d'enseignement !"
                pass
            
        if sendEvt:
            self.sendEvent()
        
        
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
#         print "init PanelPropriete_Systeme", systeme
        self.systeme = systeme
        self.parent = parent
        
        PanelPropriete.__init__(self, parent, objet = self.systeme)
        
        #
        # Nom
        #
        titre = wx.StaticText(self, -1, u"Nom du système :")
        textctrl = wx.TextCtrl(self, -1, u"")
        self.textctrl = textctrl
        
        self.sizer.Add(titre, (0,0), (1,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 3)
        
        if isinstance(systeme.parent, pysequence.Sequence):
            self.cbListSys = wx.ComboBox(self, -1, u"",
                                         choices = [u"défini localement"],
                                         style = wx.CB_DROPDOWN
                                         | wx.TE_PROCESS_ENTER
                                         | wx.CB_READONLY
                                         #| wx.CB_SORT
                                         )
            self.MiseAJourListeSys()
            self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.cbListSys)
            self.sizer.Add(self.cbListSys, (0,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT|wx.EXPAND, border = 3)
            
        
        self.sizer.Add(textctrl, (1,0), (1,2),  flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        
        #
        # Nombre de systèmes disponibles en paralléle
        #
        vcNombre = VariableCtrl(self, systeme.nbrDispo, signeEgal = True, slider = False, 
                                help = u"Nombre de d'exemplaires de ce système disponibles simultanément.")
        self.Bind(EVT_VAR_CTRL, self.EvtVar, vcNombre)
        self.vcNombre = vcNombre
        self.sizer.Add(vcNombre, (2,0), (1, 2), flag = wx.TOP|wx.BOTTOM, border = 3)
        
        #
        # Image
        #
        isizer = self.CreateImageSelect(self, titre = u"Image du système")
        self.sizer.Add(isizer, (0,2), (3,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        
        #
        # Lien
        #
        lsizer = self.CreateLienSelect(self)
        self.sizer.Add(lsizer, (0,3), (3, 1), flag = wx.EXPAND|wx.TOP|wx.LEFT, border = 2)
        
         
        self.MiseAJour()
        self.Verrouiller()
        
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
        sel = evt.GetSelection()
        if sel > 0: # Système
            s = self.systeme.parent.classe.systemes[sel-1]
            self.systeme.setBranche(s.getBranche())
            self.systeme.lienClasse = s

        else:
            p = self.systeme.GetDocument()
            s = pysequence.Systeme(p)
            self.systeme.setBranche(s.getBranche())
            self.systeme.lienClasse = None
            

        self.Verrouiller()
        self.MiseAJour()
        self.systeme.SetNom(self.systeme.nom)
        self.GetDocument().MiseAJourNomsSystemes()
        
        if isinstance(self.systeme.parent, pysequence.Sequence):
            self.systeme.parent.MiseAJourNomsSystemes()
            modif = u"Modification des systèmes nécessaires"
            if self.onUndoRedo():
                self.sendEvent(modif = modif)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif)
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
    def GetPanelPropriete(self):
        return self.parent.Parent.Parent


    #############################################################################            
    def MarquerNomValide(self, etat = True):
        if etat:
            self.textctrl.SetBackgroundColour("white")
            self.textctrl.SetToolTipString(u"Saisir le nom du Système")
        else:
            self.textctrl.SetBackgroundColour("pink")
            self.textctrl.SetToolTipString(u"Un autre Système porte déja ce nom !")
        self.textctrl.Refresh()
        
        

    #############################################################################            
    def EvtText(self, event):
        """ Modification du nom du système
        """
        
#         print "EvtText", event.GetString()
        if isinstance(self.systeme.parent, pysequence.Sequence):
            self.systeme.SetNom(event.GetString())
            self.systeme.parent.MiseAJourNomsSystemes()         # mise à jour dans l'arbre de la Séquence
            modif = u"Modification du nom du Système"
            if self.onUndoRedo():
                self.sendEvent(modif = modif)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif)
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
            modif = u"Modification du nombre de Systèmes disponibles"
            if self.onUndoRedo():
                self.sendEvent(modif = modif)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif)
                    self.eventAttente = True

    ######################################################################################  
    def estVerrouille(self):
#         print "estVerrouille", self.systeme
#        print "   ", self.parent
#        print "   ", self.systeme.parent
#        classe = self.systeme.GetClasse()
        if isinstance(self.systeme.parent, pysequence.Classe): # Cas du système édité depuis le panel propriété de la Classe
            return False
        
        if self.systeme.lienClasse is not None:
            return True                             # C'est un système qui appartient à la classe
        
        return False
   
    #############################################################################            
    def Verrouiller(self, nom = u""):
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
#         print "MiseAJour panelPropriete Systeme", self.systeme
        
        self.textctrl.ChangeValue(self.systeme.nom)
        self.vcNombre.mofifierValeursSsEvt()
        
        self.SetImage()
        
        if isinstance(self.systeme.parent, pysequence.Sequence):
            if sendEvt:
                self.sendEvent()
            
        self.MiseAJourListeSys(self.systeme.nom)
        self.MiseAJourLien()
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(toSystemEncoding(self.systeme.lien.path),
                           marquerModifier = False)
#         self.btnlien.Show(len(self.systeme.lien.path) > 0)
        self.Layout()


    #############################################################################            
    def MiseAJourListeSys(self, nom = None):
        if hasattr(self, 'cbListSys'):
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
        
        PanelPropriete.__init__(self, parent, objet = self.personne)
        
        #
        # Nom
        #
        box = myStaticBox(self, -1, u"Identité")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        bsizer.SetMinSize((300,-1))
        titre = wx.StaticText(self, -1, u"Nom : ")
        textctrl = wx.TextCtrl(self, 1)
        self.textctrln = textctrl
        
        nsizer = wx.BoxSizer(wx.HORIZONTAL)
        nsizer.Add(titre, flag = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)
        nsizer.Add(textctrl, 1, flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        #
        # Prénom
        #
        titre = wx.StaticText(self, -1, u"Prénom : ")
        textctrl = wx.TextCtrl(self, 2)
        self.textctrlp = textctrl
        
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        psizer.Add(titre, flag = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, border = 3)
        psizer.Add(textctrl, 1, flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        bsizer.Add(nsizer, flag = wx.EXPAND)
        bsizer.Add(psizer, flag = wx.EXPAND)
        self.sizer.Add(bsizer, (0,0), flag = wx.EXPAND|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
        
        
        #
        # Référent
        #
        if hasattr(self.personne, 'referent'):
            box = myStaticBox(self, -1, u"Fonction")
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

        
        
        #
        # Grilles d'évaluation
        #
        if hasattr(self.personne, 'grille'):
            self.boxGrille = myStaticBox(self, -1, u"Grilles d'évaluation")
            self.bsizer = wx.StaticBoxSizer(self.boxGrille, wx.VERTICAL)
            self.sizer.Add(self.bsizer, (1,0), (1,2), flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)
            self.ConstruireSelectGrille()
            
            
        #
        # Portrait
        #
        isizer = self.CreateImageSelect(self, titre = u"Portrait", defaut = constantes.AVATAR_DEFAUT)
        self.sizer.Add(isizer, (0,2), (2,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        
#         
#         box = myStaticBox(self, -1, u"Portrait")
#         bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
#         image = wx.StaticBitmap(self, -1, constantes.AVATAR_DEFAUT)
#         self.image = image
#         self.SetImage()
#         bsizer.Add(image, flag = wx.EXPAND)
#         
#         bt = wx.Button(self, -1, u"Changer le portrait")
#         bt.SetToolTipString(u"Cliquer ici pour sélectionner un fichier image")
#         bsizer.Add(bt, flag = wx.EXPAND|wx.ALIGN_BOTTOM)
#         self.Bind(wx.EVT_BUTTON, self.OnClick, bt)
#         self.sizer.Add(bsizer, (0,2), (2,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        #
        # Boutons Charger/Sauvegarder
        #
        if self.personne.titre == u"prof":
            bt_sizer = wx.BoxSizer(wx.HORIZONTAL)
            bt_c = wx.Button(self, -1, u"Charger")
            self.Bind(wx.EVT_BUTTON, self.OnCharge, bt_c)
            bt_s = wx.Button(self, -1, u"Sauvegarder")
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
        return self.personne.GetDocument()


    #############################################################################            
    def GetListProfs(self):
        nomFichier = os.path.join(util_path.APP_DATA_PATH, constantes.FICHIER_PROFS)
        
        if not os.path.exists(nomFichier):
            return [], ET.Element("Professeurs")
        
        fichier = open(nomFichier,'r')
        try:
            root = ET.parse(fichier).getroot()
        except ET.ParseError:
            messageErreur(wx.GetTopLevelParent(self), u"Fichier corrompu", 
                              u"Le fichier %s est corrompu !!\n\n"\
                              u"Réparez-le ou supprimez-le pour continuer à utiliser cette fonctionnalité" %nomFichier)
            fichier.close()
            return
        
        list_p = []

        for b in root:
            p = pysequence.Prof(self.personne.GetDocument())
            p.setBranche(b)
            list_p.append((p, b))
        
        
        list_p.sort(key = lambda prof : prof[0].nom)
        
        fichier.close()
        
        list_p, root = zip(*list_p)
        return list_p, list(root)


    #############################################################################            
    def OnCharge(self, event):
        
        list_p, root = self.GetListProfs()
      
        if len(list_p)>0:
            dlg = wx.SingleChoiceDialog(
                    self, u'Sélectionner un Professeur\ndans la liste ci-dessous :',
                    u'Liste des Professeurs enregistrés',
                    [p.GetNomPrenom() for p in list_p], 
                    style = wx.CHOICEDLG_STYLE
                    )
    
            if dlg.ShowModal() == wx.ID_OK:
                referent = self.personne.referent
                self.personne.setBranche(root[dlg.GetSelection()])
                self.personne.referent = referent # Ca évite des conflits ...
                modif = u"Chargement d'un Professeur"
                self.MiseAJour()
                self.sendEvent(modif = modif)
                self.personne.SetCode()
            dlg.Destroy()
            
        else:
            messageInfo(self, u"Aucun Professeur", 
                    u"La liste des Professeurs enregistrés est vide.")

        
       
        
        
    #############################################################################            
    def OnSauv(self, event):
        """ 
        """
#         print "OnSauv", self.GetListProfs()
        
        list_p, root = self.GetListProfs()
        
        if self.personne in list_p:
            dlg = wx.MessageDialog(self, u"Le professeur %s existe déja dans la liste\n\n" \
                                           u"Voulez-vous le remplacer ?" %(self.personne.GetNomPrenom()),
                                             u"Professeur existant",
                                             wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                             )
            res = dlg.ShowModal()
            dlg.Destroy()
            if res == wx.ID_YES:
                for child in root:
                    p = pysequence.Prof(self.personne.GetDocument())
                    p.setBranche(child)
                    if p == self.personne:
                        root.remove(child)
            else:
                return
            
        root.append(self.personne.getBranche())
        constantes.indent(root)
        pysequence.enregistrer_root(root, os.path.join(util_path.APP_DATA_PATH, constantes.FICHIER_PROFS))
        messageInfo(self, u"Enregistrement réussi", 
                    u"Le professeur %s a bien été ajouté." %self.personne.GetNomPrenom())


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
        
        modif = u"Modification du nom de la personne"
        if self.onUndoRedo():
            self.sendEvent(modif = modif)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = modif)
                self.eventAttente = True
        

    #############################################################################            
    def EvtComboBox(self, event):
        self.personne.SetDiscipline(get_key(constantes.NOM_DISCIPLINES, self.cbPhas.GetStringSelection()))
        self.Layout()
        self.sendEvent(modif = u"Modification de la discipline du professeur")


    #############################################################################            
    def EvtCheckBox(self, event):
        self.personne.GetDocument().SetReferent(self.personne, event.IsChecked())
        self.sendEvent(modif = u"Changement de status (référent) du professeur")


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
#        print "MiseAJour panelPropriete Personne"
        self.textctrln.ChangeValue(self.personne.nom)
        self.textctrlp.ChangeValue(self.personne.prenom)
        if hasattr(self, 'cbPhas'):
            self.cbPhas.SetStringSelection(constantes.NOM_DISCIPLINES[self.personne.discipline])
        if hasattr(self, 'cbInt'):
            self.cbInt.SetValue(self.personne.referent)
            self.personne.GetDocument().SetReferent(self.personne, self.cbInt.IsChecked())
        if hasattr(self, 'SelectGrille'):
            for k, select in self.SelectGrille.items():
                select.SetPath(toSystemEncoding(self.personne.grille[k].path), marquerModifier = marquerModifier)
#            self.OnPathModified()
        if sendEvt:
            self.sendEvent()

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
        titre = myStaticBox(self, -1, u"Type d'enseignement")
        titre.SetMinSize((180, 100))
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        te = ArbreTypeEnseignement(self, self)
        self.st_type = wx.StaticText(self, -1, "")
        self.st_type.Show(False)
        sb.Add(te, 1, flag = wx.EXPAND)
        sb.Add(self.st_type, 1, flag = wx.EXPAND)

        self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, te)
 
        te.SetStringSelection(REFERENTIELS[constantes.TYPE_ENSEIGNEMENT_DEFAUT].Enseignement[0])

        self.sizer.Add(sb, (0,0), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)#
        self.cb_type = te
        
        

        #
        # Nom
        #
        box = myStaticBox(self, -1, u"Nom du groupe")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        textctrl = wx.TextCtrl(self, 1)
        self.textctrln = textctrl
    
        bsizer.Add(textctrl, 1, flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, border = 3)
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        self.sizer.Add(bsizer, (0,1), (1,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        
        
        #
        # Etablissement
        #
        titre = myStaticBox(self, -1, u"Etablissement")
        sb = wx.StaticBoxSizer(titre, wx.VERTICAL)
        sh = wx.BoxSizer(wx.HORIZONTAL)
        t = wx.StaticText(self, -1, u"Académie :")
        sh.Add(t, flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        lstAcad = sorted([a[0] for a in constantes.ETABLISSEMENTS.values()])
        self.cba = wx.ComboBox(self, -1, u"sélectionner une académie ...", (-1,-1), 
                         (-1, -1), lstAcad+[u""],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboAcad, self.cba)
        self.Bind(wx.EVT_TEXT, self.EvtComboAcad, self.cba)
        sh.Add(self.cba, flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.LEFT, border = 5)
        sb.Add(sh, flag = wx.EXPAND)
        
        sh = wx.BoxSizer(wx.HORIZONTAL)
        t = wx.StaticText(self, -1, u"Ville :")
        sh.Add(t, flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
     
        self.cbv = SlimSelector(self, -1, u"sélectionner une ville ...", (-1,-1), 
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
        
        t = wx.StaticText(self, -1, u"Etablissement :")
        sb.Add(t, flag = wx.EXPAND)
        
        self.cbe = wx.ComboBox(self, -1, u"sélectionner un établissement ...", (-1,-1), 
                         (-1, -1), [u"autre ..."],
                         wx.CB_DROPDOWN
                         |wx.CB_READONLY
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboEtab, self.cbe)
        sb.Add(self.cbe, flag = wx.EXPAND)
        
        self.sizer.Add(sb, (1,1), (1,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
        
        
        #
        # Portrait
        #
        isizer = self.CreateImageSelect(self, titre = u"Portrait", defaut = constantes.AVATAR_DEFAUT)
        self.sizer.Add(isizer, (0,2), (2,1), flag =  wx.EXPAND|wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border = 2)#wx.ALIGN_CENTER_VERTICAL |
                      
        self.MiseAJour()
        
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(1)
        
        self.sizer.Layout()
        
        self.Layout()
        
        
    
            
            
    #############################################################################            
    def GetDocument(self):
        return self.groupe.GetDocument()


    
    
        ######################################################################################  
    def EvtComboAcad(self, evt = None, modif = True):
#        print "EvtComboAcad"
        if evt != None:
            self.groupe.academie = evt.GetString()

        lst = []
        for val in constantes.ETABLISSEMENTS.values():
            if self.groupe.academie == val[0]:
                if self.groupe.GetReferentiel().getTypeEtab() == 'L':
                    lst = val[2]
                else:
                    lst = val[1]
                break
#        print "   ", lst
        if len(lst) > 0:
            lst = sorted(list(set([v for e, v in lst])))
#        print "Villes", lst

        self.cbv.Set(lst)
        self.cbv.SlimResize()
#        self.cbv.SetSize((self.cbv.GetSizeFromTextSize(),-1))
        self.cbv.Refresh()
        
        if modif:
            self.sendEvent(modif = u"Modification de l'académie",
                           obj = self.groupe)
            
    
    ######################################################################################  
    def EvtComboVille(self, evt = None, modif = True):
#        print "EvtComboVille"
        if evt != None:
            self.groupe.ville = evt.GetString()
#        print "   ", self.classe.ville
        lst = []
        for val in constantes.ETABLISSEMENTS.values():
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
            self.sendEvent(modif = u"Modification de la ville",
                           obj = self.groupe)
        
            
        
    ######################################################################################  
    def EvtComboEtab(self, evt):       
#        if evt.GetSelection() == len(constantes.ETABLISSEMENTS_PDD):
#            self.classe.etablissement = self.textctrl.GetStringSelection()
#            self.AfficherAutre(True)
#        else:
        self.classe.etablissement = evt.GetString()
#        self.AfficherAutre(False)

        self.sendEvent(modif = u"Modification de l'établissement",
                       obj = self.groupe)



    
    #############################################################################            
    def EvtText(self, event):
        self.groupe.SetNom(event.GetString())
        
        modif = u"Modification du nom du groupe"
        if self.onUndoRedo():
            self.sendEvent(modif = modif)
        else:
            if not self.eventAttente:
                wx.CallLater(DELAY, self.sendEvent, modif = modif)
                self.eventAttente = True             
                    
    ######################################################################################  
    def EvtRadioBox(self, event = None, CodeFam = None):
        """ Sélection d'un type d'enseignement
        """
        if event != None:
            radio_selected = event.GetEventObject()
            CodeFam = Referentiel.getEnseignementLabel(radio_selected.GetLabel())

        self.groupe.typeEnseignement = CodeFam[0]
        
        self.Refresh()
        
        self.groupe.SetCode()
        
        self.sendEvent(modif = u"Modification du type d'enseignement",
                       obj = self.groupe)
        

    
    
    
    #############################################################################            
    def MiseAJour(self, sendEvt = False, marquerModifier = True):
#        print "MiseAJour panelPropriete Personne"

        self.cb_type.SetStringSelection(self.groupe.typeEnseignement)
        
        self.textctrln.ChangeValue(self.groupe.nom)

        self.cba.SetValue(self.groupe.academie)
        self.EvtComboAcad(modif = False)
        self.cbv.SetValue(self.groupe.ville)
        self.EvtComboVille(modif = False)
        self.cbe.SetValue(self.groupe.etablissement)
        
        if sendEvt:
            self.sendEvent()


   

         
###################################################################################
class PanelSelectionGrille(wx.Panel):
    def __init__(self, parent, eleve, codeGrille):
        wx.Panel.__init__(self, parent, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.eleve = eleve
        self.codeGrille = codeGrille
        titre = wx.StaticText(self, -1, eleve.GetProjetRef().parties[codeGrille])
        self.SelectGrille = URLSelectorCombo(self, eleve.grille[codeGrille], 
                                             eleve.GetDocument().GetPath(), 
                                             dossier = False, ext = "Classeur Excel (*.xls*)|*.xls*")
#         self.btnlien = wx.Button(self, -1, u"Ouvrir")
#         self.btnlien.Show(self.eleve.grille[self.codeGrille].path != "")
#         self.Bind(wx.EVT_BUTTON, self.OnClick, self.btnlien)
        sizer.Add(titre, flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 3)
        sizer.Add(self.SelectGrille,1, flag = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 3)
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
    def SetPath(self, path, marquerModifier):  
        self.SelectGrille.SetPath(path, marquerModifier = marquerModifier)          
                
                
    ######################################################################################  
    def OnPathModified(self, lien = "", marquerModifier = True):
#         self.btnlien.Show(self.eleve.grille[self.codeGrille].path != "")
        self.selec.MiseAJour()
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
        
        PanelPropriete.__init__(self, parent, objet = self.support)
        
        #
        # Nom
        #
        box = myStaticBox(self, -1, u"Nom du support")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        textctrl = TextCtrl_Help(self, u"")
        textctrl.SetTitre(u"Nom du support")
        textctrl.SetToolTipString(u"Le support est le matériel ou logiciel\n" \
                                  u"sur lequel les élèves réalisent\n" \
                                  u"les modélisations et expérimentations.")
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
        
#         box = myStaticBox(self, -1, u"Lien externe")
#         bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
#         self.selec = URLSelectorCombo(self, self.support.lien, self.support.GetPath())
#         bsizer.Add(self.selec, flag = wx.EXPAND)
#         self.btnlien = wx.Button(self, -1, u"Ouvrir le lien externe")
#         self.btnlien.Hide()
#         self.Bind(wx.EVT_BUTTON, self.OnClick, self.btnlien)
#         bsizer.Add(self.btnlien)
#         self.sizer.Add(bsizer, (1,0), flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        #
        # Image
        #
        isizer = self.CreateImageSelect(self, titre = u"Image du support")
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
#         bt.SetToolTipString(u"Cliquer ici pour sélectionner un fichier image")
#         bsizer.Add(bt, flag = wx.EXPAND)
#         self.Bind(wx.EVT_BUTTON, self.OnClick, bt)
#         self.sizer.Add(bsizer, (0,1), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)#wx.ALIGN_CENTER_VERTICAL |

        
        #
        # Description du support
        #
        dbox = myStaticBox(self, -1, u"Description du support")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
#        bd = wx.Button(self, -1, u"Editer")
        tc = richtext.RichTextPanel(self, self.support, toolBar = True)
        tc.SetTitre(u"Description du support")
        tc.SetToolTipString(u"Description du support :\n" \
                            u" - modèle\n" \
                            u" - documentation\n" \
                            u" - liens Internet\n" \
                            u" - ..."
                            )
        tc.SetMaxSize((-1, 150))
#        dbsizer.Add(bd, flag = wx.EXPAND)
        dbsizer.Add(tc, 1, flag = wx.EXPAND)
#        self.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        self.sizer.Add(dbsizer, (0,2), (2, 1), flag = wx.EXPAND|wx.ALL, border = 2)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        self.MiseAJour()
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(2)
        
        self.sizer.Layout()
        
        
        
        self.clip = wx.Clipboard()
        self.x = wx.BitmapDataObject()
        
        
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
    def OnRClickImage(self, event):
        self.clip.Open()
        ok = self.clip.GetData(self.x)
        self.clip.Close()
        if ok:
            self.GetFenetreDoc().AfficherMenuContextuel([[u"Coller l'image", self.collerImage, None
                                              ]
                                            ])
            
            
#     #############################################################################            
#     def OnClick(self, event):
#         self.support.AfficherLien(self.GetDocument().GetPath())
        
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
#                 self.support.image = rognerImage(wx.Image(nomFichier).ConvertToBitmap())
#                 self.SetImage(True)
#             
#             dlg.Destroy()
# 
# 
#     #############################################################################            
#     def SetImage(self, sendEvt = False):
#         if self.support.image != None:
#             
# #             img = rognerImage(self.support.image)
#             
# #             w, h = self.support.image.GetSize()
# #             wf, hf = 200.0, 100.0
# #             r = max(w/wf, h/hf)
# #             _w, _h = w/r, h/r
# # #            self.support.image = self.support.image.ConvertToImage().Scale(_w, _h).ConvertToBitmap()
#             self.image.SetBitmap(rognerImage(self.support.image, 200,200))
# #        self.support.SetImage()
#         self.Layout()
#         
#         if sendEvt:
#             self.sendEvent(modif = u"Modification de l'illustration du Support",
#                            obj = self)


    #############################################################################            
    def collerImage(self, sendEvt = False):
        self.support.image = self.x.GetBitmap()
#        self.SetImage(True)
    

    #############################################################################            
    def EvtText(self, event):
#         print "EvtText", self.support.nom
        txt = self.textctrl.GetText()
        
        if self.support.nom != txt:
            event.Skip()
            self.support.SetNom(txt)
    #        self.support.parent.MiseAJourNomsSystemes()
            
            modif = u"Modification de l'intitulé du Support"
            print modif
            if self.onUndoRedo():
                self.sendEvent(modif = modif)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif)
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
#        print "MiseAJour panelPropriete Support"
        self.textctrl.ChangeValue(self.support.nom)
        if sendEvt:
            self.sendEvent()
        self.MiseAJourLien()
        self.SetImage()
        
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(toSystemEncoding(self.support.lien.path), marquerModifier = False)
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
        box = myStaticBox(self, -1, u"Intitulé du modèle")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        textctrl = TextCtrl_Help(self, u"")
        textctrl.SetTitre(u"Intitulé du modele")
        textctrl.SetToolTipString(u"Un modèle numérique peut être\n" \
                                  u"une maquette numérique\n" \
                                  u"un modèle multiphysique\n" \
                                  u"...")
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
        isizer = self.CreateImageSelect(self, titre = u"Image du modèle")
        self.sizer.Add(isizer, (0,1), (2,1), flag = wx.EXPAND|wx.ALL, border = 2)

        
        #
        # Description du modèle
        #
        dbox = myStaticBox(self, -1, u"Description du modèle")
        dbsizer = wx.StaticBoxSizer(dbox, wx.VERTICAL)
#        bd = wx.Button(self, -1, u"Editer")
        tc = richtext.RichTextPanel(self, self.modele, toolBar = True)
        tc.SetTitre(u"Description du modèle")
        tc.SetToolTipString(u"Description du modèle :\n" \
                            u" - type de modèle\n" \
                            u" - logiciel utilisé\n" \
                            u" - paramètres principaux\n" \
                            u" - ..."
                            )
        tc.SetMaxSize((-1, 150))
#        dbsizer.Add(bd, flag = wx.EXPAND)
        dbsizer.Add(tc, 1, flag = wx.EXPAND)
#        self.Bind(wx.EVT_BUTTON, self.EvtClick, bd)
        self.sizer.Add(dbsizer, (0,2), (2, 1), flag = wx.EXPAND|wx.ALL, border = 2)
        self.rtc = tc
        # Pour indiquer qu'une édition est déja en cours ...
        self.edition = False  
        
        self.MiseAJour()
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(2)
        
        self.sizer.Layout()
        
        
        
        self.clip = wx.Clipboard()
        self.x = wx.BitmapDataObject()
        
        
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
        return self.modele.parent
    
    
    #############################################################################            
    def OnRClickImage(self, event):
        self.clip.Open()
        ok = self.clip.GetData(self.x)
        self.clip.Close()
        if ok:
            self.GetFenetreDoc().AfficherMenuContextuel([[u"Coller l'image", self.collerImage, None
                                              ]
                                            ])
            

    #############################################################################            
    def collerImage(self, sendEvt = False):
        self.modele.image = self.x.GetBitmap()
    

    #############################################################################            
    def EvtText(self, event):
#         print "EvtText", self.support.nom
        txt = self.textctrl.GetText()
        
        if self.modele.intitule != txt:
            event.Skip()
            self.modele.SetNom(txt)
    #        self.support.parent.MiseAJourNomsSystemes()
            
            modif = u"Modification de l'intitulé du Modèle"
            print modif
            if self.onUndoRedo():
                self.sendEvent(modif = modif)
            else:
                if not self.eventAttente:
                    wx.CallLater(DELAY, self.sendEvent, modif = modif)
                    self.eventAttente = True
        
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
#        print "MiseAJour panelPropriete modele"
        self.textctrl.ChangeValue(self.modele.intitule)
        if sendEvt:
            self.sendEvent()
        self.MiseAJourLien()
        self.SetImage()
        
        
        
    #############################################################################            
    def MiseAJourLien(self):
        self.selec.SetPath(toSystemEncoding(self.modele.lien.path), marquerModifier = False)
#         self.btnlien.Show(len(self.support.lien.path) > 0)
        self.selec.MiseAJour()
        self.Layout()
        
        
        

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
        il = wx.ImageList(*constantes.IMG_SIZE_TREE)
        for k, i in imglst:
#             print k, i.GetBitmap().GetWidth(), i.GetBitmap().GetHeight()
#             self.images[k] = il.Add(i.GetBitmap())
            self.images[k] = il.Add(scaleImage(i.GetBitmap(), 
                                               *constantes.IMG_SIZE_TREE))
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
        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
#        self.Bind(wx.EVT_CHAR, self.OnChar)
        
        self.ExpandAll()
        
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        
    ######################################################################################################
    def GetApp(self):
        return self.doc.GetApp()
    
    
    ######################################################################################################
    def OnEnter(self, event):
        self.SetFocus()
        event.Skip()
        
    
    ###############################################################################################
    def OnKey(self, evt):
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
#        print "OnRightDown", self.doc
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
    def GetPanelPropriete(self, parent, code):
        if code == "Sea":
            return PanelPropriete_Racine(parent, constantes.TxtRacineSeance)
        elif code == "Obj":
            return PanelPropriete_Racine(parent, constantes.TxtRacineObjectif)
        elif code == "Pre":
            return PanelPropriete_Racine(parent, constantes.TxtRacinePrerequis)
        elif code == "Sys":
            return PanelPropriete_Racine(parent, constantes.TxtRacineSysteme)
        elif code == "Equ":
            return PanelPropriete_Racine(parent, constantes.TxtRacineEquipe)
        elif code == "Tac":
            return PanelPropriete_Racine(parent, constantes.TxtRacineTache)
        elif code == "Ele":
            return PanelPropriete_Racine(parent, constantes.TxtRacineEleve)
        elif code == "Seq":
            return PanelPropriete_Racine(parent, constantes.xmlVide)
        
        return 
    
    
    ####################################################################################
    def OnSelChanged(self, event = None, item = None):
        """ Fonction appelée lorsque la selection a été changée dans l'arbre
            ---> affichage du panel de Propriétés associé
        """
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
        
        if isinstance(data, tuple) and hasattr(data[0], 'GetPanelPropriete'):
            panelPropriete = data[0].GetPanelPropriete(self.panelProp, data[1], data[2])
        elif hasattr(data, 'GetPanelPropriete'):
            panelPropriete = data.GetPanelPropriete(self.panelProp)
        elif isinstance(data, (str, unicode)): # 
            panelPropriete = self.GetPanelPropriete(self.panelProp, data)
        else:
            print "err : ", data
        
        if panelPropriete:
#             print "> panelPropriete", panelPropriete
            self.panelProp.AfficherPanel(panelPropriete)
            self.parent.Refresh()
        else:
            print "rien", panelPropriete
        
        #
        # On centre la fiche sur l'objet
        #
        if hasattr(self.classe.doc.GetApp(), 'fiche') and self.classe.doc.centrer:
            self.classe.doc.GetApp().fiche.CentrerSur(data)
        self.classe.doc.centrer = True
        
        if event is not None:
            event.Skip()


    ####################################################################################
    def OnBeginDrag(self, event):
        self.itemDrag = event.GetItem()
        if self.item:
            event.Allow()

        
    ######################################################################################              
    def OnToolTip(self, event):
#         print "OnToolTip"
        node = event.GetItem()
        data = self.GetPyData(node)
        if (hasattr(data, 'toolTip') and isstring(data.toolTip)):
            event.SetToolTip(wx.ToolTip(data.toolTip))
        elif isstring(data):
            if data == "Seq":
                event.SetToolTip(wx.ToolTip(self.doc.toolTip))
            else:
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
                          imglst = constantes.dicimages.items() + constantes.imagesSeance.items())
        
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
#         il = wx.ImageList(*constantes.IMG_SIZE_TREE)
#         for k, i in constantes.dicimages.items() + constantes.imagesSeance.items():
# #             print k, i.GetBitmap().GetWidth(), i.GetBitmap().GetHeight()
# #             self.images[k] = il.Add(i.GetBitmap())
#             self.images[k] = il.Add(scaleImage(i.GetBitmap(), 
#                                                *constantes.IMG_SIZE_TREE))
#         self.AssignImageList(il)
        
        
        #
        # Construction de l'arbre
        #
        self.sequence.ConstruireArbre(self, self.root)
        
        
#        self.panelProp.AfficherPanel(self.sequence.GetPanelPropriete())

#        self.CurseurInsert = wx.CursorFromImage(constantes.images.CurseurInsert.GetImage())
        self.CurseurInsertApres = wx.CursorFromImage(constantes.images.Curseur_InsererApres.GetImage())
        self.CurseurInsertDans = wx.CursorFromImage(constantes.images.Curseur_InsererDans.GetImage())
        

            
        
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
        if self.itemDrag != None:
            item = self.HitTest(wx.Point(event.GetX(), event.GetY()))[0]
            
            if item != None:
                dataTarget = self.GetItemPyData(item)
                if dataTarget == "Sea":
                    dataTarget = self.sequence
                
#                 print "dataTarget", dataTarget
                
#                 if isinstance(dataTarget, PanelPropriete_Racine):
                
#                     print "       >>", dataTarget
                    
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
               or (isinstance(dataTarget, pysequence.Seance) and dataTarget.typeSeance in ["R","S"]):
                if hasattr(dataSource.parent, 'typeSeance') \
                      and dataSource.parent.typeSeance in ["R","S"] \
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
            else:
                if dataTarget.parent != dataSource.parent:  # parents différents
#                    print dataSource.typeSeance, dataTarget.GetListeTypes()
                    if hasattr(dataSource.parent, 'typeSeance') \
                      and dataSource.parent.typeSeance in ["R","S"] \
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
    def OnEndDrag(self, event):
        """ Gestion des glisser-déposer
        """
        self.item = event.GetItem() 
        if self.item is not None:
            dataTarget = self.GetItemPyData(self.item)
            if dataTarget == "Sea":
                dataTarget = self.sequence
    #         if isinstance(dataTarget, PanelPropriete_Racine):
    #             dataTarget = self.sequence
            
            dataSource = self.GetItemPyData(self.itemDrag)
            tx = u"Changement de position de la Séance"
            a = self.getActionDnD(dataSource, dataTarget)
#             print "OnEndDrag", a
            if a == 1:
                lstS = dataSource.parent.seances
                lstT = dataTarget.seances
                s = lstS.index(dataSource)
                lstT.insert(0, lstS.pop(s))
                dataSource.parent = dataTarget
                
                self.sequence.OrdonnerSeances()
                self.sequence.reconstruireBrancheSeances(dataSource.parent, dataTarget)
                self.GetApp().sendEvent(self.sequence, modif = tx) # Solution pour déclencher un "redessiner"
            
            elif a == 2:
                lst = dataSource.parent.seances
                s = lst.index(dataSource)
                lst.insert(0, lst.pop(s))
                   
                self.sequence.OrdonnerSeances() 
                if dataTarget == self.sequence:
                    self.SortChildren(self.item)
                else:
                    self.SortChildren(self.GetItemParent(self.item))
                self.GetApp().sendEvent(self.sequence, modif = tx) # Solution pour déclencher un "redessiner"
            
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
                self.GetApp().sendEvent(self.sequence, modif = tx) # Solution pour déclencher un "redessiner"
            
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
                self.GetApp().sendEvent(self.sequence, modif = tx) # Solution pour déclencher un "redessiner"
                    
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

        ArbreDoc.__init__(self, parent, classe, panelProp,
                          imglst = constantes.imagesProjet.items() + constantes.imagesTaches.items())
        
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
#         il = wx.ImageList(*constantes.IMG_SIZE_TREE)
#         for k, i in constantes.imagesProjet.items() + constantes.imagesTaches.items():
# #             self.images[k] = il.Add(i.GetBitmap())
#             self.images[k] = il.Add(scaleImage(i.GetBitmap(), 
#                                                *constantes.IMG_SIZE_TREE))
#             
#         self.AssignImageList(il)

        #
        # Construction de l'arbre
        #
        self.projet.ConstruireArbre(self, self.root)
     
#        self.panelProp.AfficherPanel(self.projet.GetPanelPropriete())

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
        if hasattr(i1, 'ordre'):   # cas des tâches
            return int(i1.ordre - i2.ordre)
        else:                   # cas des élèves/groupes
            return int(i1.id - i2.id)
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
                if not isinstance(dataSource, pysequence.Tache):
                    self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
                else:
                    if not isinstance(dataTarget, pysequence.Tache) \
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
                    self.GetApp().sendEvent(self.projet, modif = u"Changement de position de la Tâche") # Solution pour déclencher un "redessiner"
    
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
                          imglst = constantes.imagesProgression.items())
        
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
#         il = wx.ImageList(*constantes.IMG_SIZE_TREE)
#         for k, i in constantes.imagesProgression.items():
# #             self.images[k] = il.Add(i.GetBitmap())
#             self.images[k] = il.Add(scaleImage(i.GetBitmap(), 
#                                                *constantes.IMG_SIZE_TREE))
#         self.AssignImageList(il)
#         
        #
        # Construction de l'arbre
        #
        self.progression.ConstruireArbre(self, self.root)
        
#        self.panelProp.AfficherPanel(self.progression.panelPropriete)

#        self.CurseurInsert = wx.CursorFromImage(constantes.images.CurseurInsert.GetImage())
        self.CurseurInsertApres = wx.CursorFromImage(constantes.images.Curseur_InsererApres.GetImage())
        self.CurseurInsertDans = wx.CursorFromImage(constantes.images.Curseur_InsererDans.GetImage())
 


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
        
    ####################################################################################
    def EstMovable(self, obj):
        return isinstance(obj, pysequence.LienSequence) \
            or isinstance(obj, pysequence.LienProjet) \
            or isinstance(obj, pysequence.Prof)


    ####################################################################################
    def EstMemeCategorie(self, obj1, obj2):
        return (isinstance(obj1, pysequence.Prof) and isinstance(obj2, pysequence.Prof)) \
            or (isinstance(obj1, pysequence.LienSequence) and isinstance(obj2, pysequence.LienProjet)) \
            or (isinstance(obj2, pysequence.LienSequence) and isinstance(obj1, pysequence.LienProjet))


    ####################################################################################
    def OnMove(self, event):
        event.Skip()
        
        if self.itemDrag != None:
            item = self.HitTest(wx.Point(event.GetX(), event.GetY()))[0]
            if item != None:
                dataTarget = self.GetItemPyData(item)
                dataSource = self.GetItemPyData(self.itemDrag)
                
                if dataTarget == dataSource:
                    self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
                
                elif not self.EstMovable(dataSource) or not self.EstMemeCategorie(dataSource, dataTarget):
                    self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
                
                else:
                    if isinstance(dataTarget, pysequence.Prof) and dataTarget != dataSource:
                        self.SetCursor(self.CurseurInsertApres)
                            
                    elif dataTarget.GetPosition() <= dataSource.GetPosition():
                        self.SetCursor(self.CurseurInsertApres)
                        
                    else:
                        self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))

        event.Skip()


    ####################################################################################
    def OnEndDrag(self, event):
        self.item = event.GetItem()
        dataTarget = self.GetItemPyData(self.item)
        dataSource = self.GetItemPyData(self.itemDrag)
        
        if dataTarget == dataSource:
            pass
        
        elif self.EstMemeCategorie(dataSource, dataTarget):
            if isinstance(dataTarget, pysequence.Prof) and dataTarget != dataSource:
                lst = self.progression.equipe
                s = lst.index(dataSource)
                t = lst.index(dataTarget)
                if t > s:
                    lst.insert(t, lst.pop(s))
                else:
                    lst.insert(t+1, lst.pop(s))
                
                self.GetApp().sendEvent(self.progression, modif = u"Changement de position d'un professeur") # Solution pour déclencher un "redessiner"

            elif dataTarget.GetPosition() <= dataSource.GetPosition():
                lst = self.progression.sequences_projets
                s = lst.index(dataSource)
                t = lst.index(dataTarget)
                if t > s:
                    lst.insert(t, lst.pop(s))
                else:
                    lst.insert(t+1, lst.pop(s))
                
                if isinstance(dataSource, pysequence.LienSequence):
                    self.GetApp().sendEvent(self.progression, modif = u"Changement de position d'une Séquence") # Solution pour déclencher un "redessiner"
                else:
                    self.GetApp().sendEvent(self.progression, modif = u"Changement de position d'un Projet") # Solution pour déclencher un "redessiner"
        
        
            self.SortChildren(self.GetItemParent(self.item))
        
        self.itemDrag = None
        event.Skip()            

    




            



class ArbreSavoirs(CT.CustomTreeCtrl):
    def __init__(self, parent, typ, savoir, savoirs, prerequis, et = False):

        CT.CustomTreeCtrl.__init__(self, parent, -1, 
                                   agwStyle = wx.TR_DEFAULT_STYLE|wx.TR_MULTIPLE|wx.TR_HIDE_ROOT|CT.TR_AUTO_CHECK_CHILD|\
                                   CT.TR_AUTO_CHECK_PARENT|CT.TR_HAS_VARIABLE_ROW_HEIGHT) # << le dernier pour accepter les texte multiligne (ça marche mais pas débuggé)
        
        self.parent = parent
        self.savoirs = savoirs # Les savoirs sélectrionnés
        self.savoir = savoir   # L'objet Referentiel.Savoir
        self.typ = typ
#        ref = savoirs.GetReferentiel()
        
        self.root = self.AddRoot(u"")
        
#        if typeEns == "SSI":
#            t = u"Capacités "
#        else:
#            t = u"Savoirs "
#        self.root = self.AppendItem(root, t+typeEns)
        self.SetItemBold(self.root, True)
#        et = False
#        if typ == "B":
#            if ref.tr_com != []:
#                dic = REFERENTIELS[ref.tr_com[0]].dicSavoirs
#                et = True
#            else:
#                dic = ref.dicSavoirs
#        elif typ == "S":
#            dic = ref.dicSavoirs
#        elif typ == "M":
#            if ref.tr_com != []:
#                dic = REFERENTIELS[ref.tr_com[0]].dicSavoirs_Math
#            else:
#                dic = ref.dicSavoirs_Math
#        elif typ == "P":
#            if ref.tr_com != []:
#                dic = REFERENTIELS[ref.tr_com[0]].dicSavoirs_Phys
#            else:
#                dic = ref.dicSavoirs_Phys
        self.Construire(self.root, savoir.dicSavoirs, et = et)
            
            
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
            
#        self.typ = typ
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
                        
                        
        self.parent.SetSavoirs()
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
    def __init__(self, parent, typ, dicCompetences, competences, 
                 pptache = None, filtre = None, agwStyle = 0):#|CT.TR_AUTO_CHECK_CHILD):#|HTL.TR_NO_HEADER):
        
        HTL.HyperTreeList.__init__(self, parent, -1, style = wx.WANTS_CHARS,
                                   agwStyle = CT.TR_HIDE_ROOT|CT.TR_HAS_VARIABLE_ROW_HEIGHT|agwStyle)#wx.TR_DEFAULT_STYLE|
        
        self.parent = parent
#         print "ArbreCompetences", pptache
        if pptache == None:
            self.pptache = parent
        else:
            self.pptache = pptache
        
        self.typ = typ
        self.competences = competences # Objet Referentiel.Competences
        self.filtre = filtre
        
        if dicCompetences is None:
            dicCompetences = competences.dicCompetences
            
        self.dicCompetences = dicCompetences
        
        self.items = {}
      
        self.AddColumn(competences.nomDiscipline)
        self.SetMainColumn(0) # the one with the tree in it...
        
        self.CreerColonnes()
        
        self.root = self.AddRoot(competences.nomDiscipline)
        self.MiseAJourTypeEnseignement(dicCompetences)
        
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
    def CreerColonnes(self):
        pass
    
    
    ######################################################################################################
    def ToolTip(self, event):
        return
#        print self.HitTest((event.x, event.y))
        
    ######################################################################################################
    def OnEnter(self, event):
#        print "OnEnter PanelPropriete"
        self.SetFocus()
        event.Skip()
        
    #############################################################################
    def MiseAJourTypeEnseignement(self, dicCompetences):
#        print "MiseAJourTypeEnseignement"
       
 
        self.DeleteChildren(self.root)
        for i in self.items.values():
            for wnd in i._wnd:
                if wnd:
                    wnd.Hide()
                    wnd.Destroy()

        self.items = {}
        self.Construire(self.root, dic = dicCompetences)

        self.ExpandAll()


    
        
    
    ####################################################################################
    def OnSize2(self, evt = None):
#        print "OnSize2"
        ww = 0
        for c in range(1, self.GetColumnCount()):
            ww += self.GetColumnWidth(c)
        w = self.GetClientSize()[0]-20-ww
        if w != self.GetColumnWidth(0):
            self.SetColumnWidth(0, w)
            if self.IsShown():
                self.wrap(w)
        
        if evt is not None:
            evt.Skip()


    ####################################################################################
    def wrap(self,w):
        item = self.GetRootItem()
        if item != None:
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
    def Construire(self, branche, dic = None, ct_type = 0):
        if dic == None:
            dic = self.competences.dicCompetences

        clefs = dic.keys()
        clefs.sort()
        for k in clefs:
            b = None
            if dic[k].sousComp != {}:
                b = self.AppendItem(branche, k+" "+dic[k].intitule, ct_type=ct_type, data = k)
                self.Construire(b, dic[k].sousComp, ct_type = 1)
            else:
                if self.filtre is None or k in self.filtre:
                    b = self.AppendItem(branche, k+" "+dic[k].intitule, ct_type = 1, data = k)
            
            if b is not None:
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
    def getCode(self, item):
        return self.typ+self.GetItemPyData(item)


    ####################################################################################
    def AjouterEnleverCompetencesItem(self, item, propag = True):

        code = self.getCode(item)#.split()[0]
#        print "AjouterEnleverCompetencesItem", code
        if code != None: # un seul indicateur séléctionné
            self.AjouterEnleverCompetences([item], propag)

        else:       # une compétence compléte séléctionnée
            self.AjouterEnleverCompetences(item.GetChildren(), propag)


    ####################################################################################
    def AjouterEnleverCompetences(self, lstitem, propag = True):
#        print "AjouterEnleverCompetences"
        for item in lstitem:
            code = self.getCode(item)#.split()[0]
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
            if self.GetItemWindow(item, self.colEleves).EstCocheEleve(eleve):
                self.pptache.AjouterCompetenceEleve(self.typ+code, eleve)
            else:
                self.pptache.EnleverCompetenceEleve(self.typ+code, eleve)
    
    
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
    def __init__(self, parent, typ, dicCompetences, competences,  pptache, revue = False, eleves = False, 
                 agwStyle = CT.TR_HIDE_ROOT|CT.TR_HAS_VARIABLE_ROW_HEIGHT|\
                            CT.TR_ROW_LINES|CT.TR_ALIGN_WINDOWS| \
                            CT.TR_AUTO_CHECK_PARENT|CT.TR_AUTO_TOGGLE_CHILD):
        self.revue = revue#|CT.TR_AUTO_CHECK_CHILD|\
        self.eleves = eleves
        self.typ = typ
        
#         if pptache == None:
#             self.pptache = parent
#         else:
#             self.pptache = pptache
            
#         print "ArbreCompetencesPrj", pptache
        ArbreCompetences.__init__(self, parent, typ, dicCompetences, competences, pptache,
                                  agwStyle = agwStyle)#|CT.TR_ELLIPSIZE_LONG_ITEMS)#|CT.TR_TOOLTIP_ON_LONG_ITEMS)#
#         print self.pptache
        
        
        self.Bind(wx.EVT_SIZE, self.OnSize2)
        self.Bind(CT.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        
        self.SetColumnText(0, getPluriel(competences.nomGenerique) + u" et " + competences.nomGeneriqueIndic)
        
        tache = self.GetTache()
        prj = tache.GetProjetRef()
        
        for i, part in enumerate(prj.parties.keys()):
            self.SetColumnText(i+1, u"Poids "+part)
            self.SetColumnWidth(i+1, 60)
        
        if eleves:
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
        
        for i in range(len(prj.parties.keys())):
            self.AddColumn(u"")
            self.SetColumnWidth(i+1, 0)
        
        self.colEleves = len(prj.parties.keys())+1
        self.AddColumn(u"Eleves")
        self.SetColumnWidth(self.colEleves, 0)
        
        
    ####################################################################################
    def ConstruireCasesEleve(self):
        """ Ajout des cases "ChoixCompetenceEleve"
        """
        
        tache = self.GetTache()
#        print "   ConstruireCasesEleve", tache.phase, self.items
        cases = None
        affcol = None
        for codeIndic, item in self.items.items():
            cases = self.GetItemWindow(item, self.colEleves)
            if isinstance(cases, ChoixCompetenceEleve):
                item.DeleteWindow(self.colEleves)
                cases = ChoixCompetenceEleve(self.GetMainWindow(), self.typ+codeIndic,
                                             tache.projet, tache, self.MiseAJourCaseEleve)
                item.SetWindow(cases, self.colEleves)
                affcol = cases
        
        if affcol is not None:
            self.SetColumnWidth(self.colEleves, max(60, affcol.GetSize()[0]))
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
#         print "Construire compétences prj", self.GetTache().intitule, self.eleves
#        if competences == None:
#            competences = self.competences
        
        if branche == None:
            branche  = self.root
        
        tache = self.GetTache()
        prj = tache.GetProjetRef()
#        print " prj", prj, self.typ
        if dic == None: # Construction de la racine
#            dic = self.competences.dicCompetences
            dic = self.dicCompetences
            
        
#        print "   ProjetRef", prj
#         print "  dicCompetences", dic
#        if tache.estPredeterminee(): print prj.taches[tache.intitule][2]
        
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False)
        
#        size = None
        if self.eleves:
            tousEleve = [True]*len(tache.projet.eleves)
        
        def const(d, br, debug = False):
            ks = d.keys()
            ks.sort()
            for k in ks:
                if debug: print "****", k
#                 v = d[k]
                competence = d[k]
#                print "****", k#, prj.taches[tache.intitule][2]

                #
                # Groupe de compétences
                #
                if competence.sousComp != {}:
#                 if len(v) > 1 and type(v[1]) == dict:
                    
                    if debug: print "   ", competence.intitule
                    
                    if competence.poids == {}: # Compétence 
#                     if len(v) == 2: # Compétence 
                        if not tache.estPredeterminee() or k in prj.taches[tache.intitule][2]:
                            b = self.AppendItem(br, k+" "+competence.intitule)
                        else:
                            b = None
                    
                    else:   # Groupe de compétences - avec poids 
                        if debug: print "   prem's", competence.poids
                        b = self.AppendItem(br, k+" "+competence.intitule)
#                        print " * ",v[2]
                        
                        for i, part in enumerate(prj.parties.keys()):
                            if part in competence.poids.keys():
                                self.SetItemText(b, pourCent2(0.01*competence.poids[part]), i+1)
                        
#                        for i, p in enumerate(v[2][1:]):
#                            if p != 0:
#                                self.SetItemText(b, pourCent2(0.01*p), i+1)
                        self.SetItemBold(b, True)
                    
                    if b is not None:
                        self.items[k] = b
                        const(competence.sousComp, b, debug = debug)
                        
                #
                # Compétence avec indicateur(s)
                #
                else:
                    b = None #
                    tous = True
                    
                    if not tache.estPredeterminee() or (tache.intitule in prj.taches.keys() and k in prj.taches[tache.intitule][2]):
                        cc = [cd+ " " + it for cd, it in zip(k.split(u"\n"), competence.intitule.split(u"\n"))]
                        comp = self.AppendItem(br, u"\n ".join(cc))
                        
                        #
                        # Compétence "racine" - avec poids
                        #
                        if competence.poids != {}: # 
#                         if len(v) == 3: # 
                            if debug: print "   prem's", competence.poids
                            for j, part in enumerate(prj.parties.keys()):
                                if part in competence.poids.keys():
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
                            if debug:
    #                            print not tache.phase in [_R1, "Rev", tache.projet.getCodeLastRevue()]
    #                            print codeIndic , indic.revue,
                                if hasattr(tache, 'indicateursMaxiEleve'):
                                    print "  ", tache.indicateursMaxiEleve[0]
                                print "  ", prj.getTypeIndicateur(self.typ+codeIndic)
                            
                            if tache == None:
                                b = self.AppendItem(comp, indic.intitule, data = codeIndic)
                                for j, part in enumerate(prj.parties.keys()):
                                    if part in competence.poids.keys():
    #                            for j, p in enumerate(indic.poids[1:]):
    #                                if p != 0:
                                        if j == 0:  coul = 'C'
                                        else:       coul = 'S'
                                self.SetItemTextColour(b, COUL_PARTIE[coul])
                                self.SetItemFont(b, font)
                            
                            if tache != None and tache.estACocherIndic(self.typ+codeIndic):
#                             if tache != None and ((not tache.phase in [_R1,_R2, _Rev, tache.projet.getCodeLastRevue()]) \
#                                                   or (self.typ+codeIndic in tache.indicateursMaxiEleve[0])) \
#                                              and (prj.getTypeIndicateur(self.typ+codeIndic) == "S" or tache.phase != 'XXX'):#and (indic.revue[self.typ] == 0 or indic.revue[self.typ] >= tache.GetProchaineRevue()) \ # à revoir !!
                                
                                b = self.AppendItem(comp, indic.intitule, ct_type=1, data = codeIndic) # Avec case à cocher
                                
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
                    
                    if b == None: # Désactivation si branche vide d'indicateurs
                        self.SetItemType(br,0)
                    else:
                        self.CheckItem2(br, tous)
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


    #############################################################################
    def MiseAJourPhase(self, phase):
        self.DeleteChildren(self.root)
        self.Construire(self.root)
        self.ExpandAll()
        
    
    #############################################################################
    def GetCasesEleves(self, codeIndic):
        if codeIndic in self.items.keys():
            return self.GetItemWindow(self.items[codeIndic], self.colEleves)
    
#    #############################################################################
#    def MiseAJourCases(self):
#        """ Mise à jour des cases "élèves" de l'arbre des compétences
#            > on cécoche tout et on recoche
#        """
#        tache = self.GetTache()
#        print "MiseAJourCases", tache.phase, tache.intitule
#        print "  ", tache.indicateursEleve
#        
#        self.UnselectAll()
#            
#        for codeIndic in tache.indicateursEleve[0]:
#            cases = self.GetCasesEleves(codeIndic)
#            if cases:
#                cases.MiseAJour()
#                cases.Actualiser()

    
    
    #############################################################################
    def MiseAJourCasesEleve(self, codeIndic, cases):
        cases.MiseAJour()
        
        
    #############################################################################
    def MiseAJourCaseEleve(self, codeIndic, etat, eleve, propag = True):
        """ Mise à jour
        """
        print "MiseAJourCaseEleve", codeIndic, etat, eleve, propag
        casesEleves = self.GetCasesEleves(codeIndic[1:])
        if casesEleves.EstCocheEleve(eleve) != etat:
            return
        
        estToutCoche = casesEleves.EstToutCoche()
        print "  estToutCoche =", estToutCoche
        
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
            
            self.CheckItem2(item, estToutCoche, torefresh=True)
#            self.Refresh()
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
                for part in prj.parties.keys():
                    if part in indic.poids.keys():
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
            
####################################################################################
#
#   Classe définissant l'arbre de sélection du type d'enseignement
#
####################################################################################*

class ArbreTypeEnseignement(CT.CustomTreeCtrl):
    def __init__(self, parent, panelParent, 
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.WANTS_CHARS):#|wx.BORDER_SIMPLE):

#        wx.Panel.__init__(self, parent, -1, pos, size)
        
        CT.CustomTreeCtrl.__init__(self, parent, -1, pos, (150, -1), style, 
                                   agwStyle = CT.TR_HIDE_ROOT|CT.TR_FULL_ROW_HIGHLIGHT\
                                   |CT.TR_HAS_VARIABLE_ROW_HEIGHT|CT.TR_HAS_BUTTONS\
                                   |CT.TR_TOOLTIP_ON_LONG_ITEMS)#CT.TR_ALIGN_WINDOWS|CCT.TR_NO_HEADER|T.TR_AUTO_TOGGLE_CHILD|\CT.TR_AUTO_CHECK_CHILD|\CT.TR_AUTO_CHECK_PARENT|
        self.Unbind(wx.EVT_KEY_DOWN)
        self.panelParent = panelParent
#        self.SetBackgroundColour(wx.WHITE)
        self.SetToolTip(wx.ToolTip(u"Choisir le type d'enseignement"))
        
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
#        print ARBRE_REF
        self.branche = []
#        self.ExpandAll()
        for t, st in ARBRE_REF:
#            print "   ", t, st, self.panelParent.pourProjet
            
            if t[0] == "_" or (self.panelParent.pourProjet and len(REFERENTIELS[t].projets) == 0):
                branche = self.AppendItem(racine, REFERENTIELS[st[0]].Enseignement[2], 
                                          data = REFERENTIELS[st[0]].Enseignement[3])
            else:
                branche = self.AppendItem(racine, u"")#, ct_type=2)#, image = self.arbre.images["Seq"])
                rb = wx.RadioButton(self, -1, REFERENTIELS[t].Enseignement[0])
                self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, rb)
                self.SetItemWindow(branche, rb)
                rb.SetToolTipString(REFERENTIELS[t].Enseignement[1])
                rb.Enable(len(REFERENTIELS[t].projets) > 0 or not self.panelParent.pourProjet)
                self.branche.append(branche)
            for sst in st:
                sbranche = self.AppendItem(branche, u"")#, ct_type=2)
                rb = wx.RadioButton(self, -1, REFERENTIELS[sst].Enseignement[0])
                self.Bind(wx.EVT_RADIOBUTTON, self.EvtRadioBox, rb)
                self.SetItemWindow(sbranche, rb)
                rb.SetToolTipString(REFERENTIELS[sst].Enseignement[1])
                rb.Enable(len(REFERENTIELS[sst].projets) > 0 or not self.panelParent.pourProjet)
                self.branche.append(sbranche)
        
        self.ExpandAll()
        self.CollapseAll()
        
    ######################################################################################              
    def EvtRadioBox(self, event):
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
        t = getPluriel(ref.nomPb)
        if hasPb:
            t += u" personnalisées"
        
        self.PbPerso = gizmos.EditableListBox(self, -1, t,
                                              size = wx.DefaultSize,
                                              style = gizmos.EL_ALLOW_NEW | gizmos.EL_ALLOW_EDIT | gizmos.EL_ALLOW_DELETE)
        self.PbPerso.SetMinSize((-1, 60))
        self.PbPerso.SetToolTipString(u"Exprimer ici la(les) %s abordée(s)\n" \
                                      u"ou choisir une parmi les %s envisageables." %(getSingulier(ref.nomPb), getPluriel(ref.nomPb)))

        self.PbPerso.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.EvtText)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.EvtText)
        
        self.sizer.Add(self.PbPerso, 1, flag = wx.EXPAND)
        
        
#        self.SetBackgroundColour(wx.WHITE)
        self.SetToolTip(wx.ToolTip(u"Ppppb"))
        
        
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
    def MiseAJour(self):
#         print "MiseAJour Pb"
#         print self.CI.Pb
#         self.PbPerso.SetStrings(u"")
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
        
        t = u"Modification de la %s" %getSingulier(ref.nomPb)
        self.Parent.GetDocument().GererDependants(self.CI.parent, t)
            
        if self.Parent.onUndoRedo():
            self.Parent.sendEvent(modif = t)
        else:
            if not self.Parent.eventAttente:
                wx.CallLater(DELAY, self.Parent.sendEvent, modif = t)
                self.Parent.eventAttente = True
                
        
        
    
    ######################################################################################              
    def OnToolTip(self, event = None, item = None):
        return
#         print "OnToolTip"


    ######################################################################################              
    def OnClick(self, event = None, item = None):
        print "OnClick"


    ######################################################################################              
    def EvtCheckBox(self, event):
        ref = self.CI.GetReferentiel()
        item = event.GetItem()
        pb = self.arbre.GetItemText(item)
        if pb in self.CI.Pb:
            self.CI.Pb.remove(pb)
        else:
            self.CI.Pb.append(pb)
        self.Parent.sendEvent(modif = u"Modification de la %s" %getSingulier(ref.nomPb))

    

    
        

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
        self.Bouton.SetToolTipString(u"Selectionner une tâche")
        parent.Bind(wx.EVT_BUTTON, self.OnClick, self.Bouton)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.texte = wx.StaticText(self, -1, u"", style = wx.ST_NO_AUTORESIZE|wx.ST_ELLIPSIZE_END)#|wx.BORDER_SIMPLE)
#        self.texte.FitInside()
#        sizer.Add(self.Bouton, flag = wx.EXPAND)
        sizer.Add(self.texte, 1, flag = wx.EXPAND|wx.RIGHT, border = 10)
        
        self.SetSizerAndFit(sizer)

    
    def SetLabel(self, texte):
        self.texte.SetLabel(wordwrap(texte, self.texte.GetSize()[0], wx.ClientDC(self)))
    
    
    def OnSize(self, evt):
        self.texte.SetSize(self.GetSize())
        w = self.GetSize()[0]
        x, y = self.GetPositionTuple()
        self.Bouton.Move((x+w-10, y-20))
        self.Refresh()
        
    def OnClick(self, evt):
        win = TreeCtrlComboPopup(self,
                                 wx.SIMPLE_BORDER,
                                 self.tache,
                                 self.EvtComboBox)
#        w, h = wx.GetDisplaySize()

        btn = evt.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        win.Position(pos, (600,400))
        win.Popup()
    
    
    def ExpandAll(self):
        self.tcp.tree.ExpandAll()

    def AddItem(self, labelItem, parent = None):
        return self.tcp.AddItem(labelItem, parent)
        
    def SetItemBold(self, item, etat = True):
        self.tcp.tree.SetItemBold(item, etat)
        
    def EvtComboBox(self, texte):
        texte = u"\n".join(texte.split(" ", 1))

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
class TreeCtrlComboPopup(wx.PopupTransientWindow):
    def __init__(self, parent, style, tache, fct):
        self.fct = fct
        wx.PopupTransientWindow.__init__(self, parent, style)
        
        self.pnl = wx.Panel(self)
        
        prj = tache.GetProjetRef()

        self.tree = CT.CustomTreeCtrl(self.pnl, style=wx.TR_HIDE_ROOT
                                |wx.TR_HAS_BUTTONS
                                |wx.TR_SINGLE
                                |wx.TR_ROW_LINES
                                |wx.TR_LINES_AT_ROOT,
#                                |wx.SIMPLE_BORDER,
                                agwStyle = CT.TR_HAS_VARIABLE_ROW_HEIGHT | CT.TR_HIDE_ROOT)
        self.tree.SetMinSize((600,400))
        ph = None
        for ct in prj.listTaches:
            if ph != prj.taches[ct][0]:
                pph = self.AddItem(prj.phases[prj.taches[ct][0]][1])
                self.tree.SetItemBold(pph, True)
                ph = prj.taches[ct][0]
            item = self.AddItem(ct+" "+prj.taches[ct][1], parent=pph)
            if prj.tachesOnce:
                self.tree.EnableItem(item, ct not in [t.intitule for t in tache.projet.taches])
            
                
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
        return wx.Size(minWidth, min(200, maxHeight))
                       

    # helpers
    
    def FindItem(self, parentItem, text):        
        item, cookie = self.tree.GetFirstChild(parentItem)
        while item:
            if self.tree.GetItemText(item) == text:
                return item
            if self.tree.ItemHasChildren(item):
                item = self.FindItem(item, text)
            item, cookie = self.tree.GetNextChild(parentItem, cookie)
        return wx.TreeItemId();


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
            margin = 15
        else:
            margin = 30
            
        w = self.tree.GetSize()[0]
        item, cookie = self.tree.GetFirstChild(parentItem)
        while item:
            text = self.tree.GetItemText(item).replace(u"\n", u"")
            self.tree.SetItemText(item, wordwrap(text, w-margin-4, wx.ClientDC(self.tree), breakLongWords=False))
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
        item, flags = self.tree.HitTest(evt.GetPosition())
#        print self.tree.GetItemParent(item)
        if item and self.tree.GetItemParent(item) != self.tree.GetRootItem():
            self.fct(self.tree.GetItemText(self.tree.GetSelection()).replace(u"\n", u""))
            self.Dismiss()
        
#    def OnLeftDown(self, evt):
#        # do the combobox selection
#        item, flags = self.tree.HitTest(evt.GetPosition())
#        if item and flags & wx.TREE_HITTEST_ONITEMLABEL:
#            self.curitem = item
#            self.value = item
#            self.Dismiss()
#        evt.Skip()

    
    
    
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
#         print "MiseAJour ChoixCompetenceEleve", self.tache, self.indic
        for i, e in enumerate(self.projet.eleves): 
            dicIndic = e.GetDicIndicateursRevue(self.tache.phase)
#            print "    ", dicIndic
            comp = self.indic.split("_")[0]
            if comp in dicIndic.keys():
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

        label = wx.StaticText(self, -1, u"Lien :")
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
        
        self.ext = ext
        self.dossier = dossier
        self.lien = lien
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        lsizer = self.CreateSelector()
        sizer.Add(lsizer, 1, flag = wx.EXPAND)
        self.SetSizerAndFit(sizer)
        
        self.SetPathSeq(pathseq)

    
    
    ###############################################################################################
    def CreateSelector(self):
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.texte = wx.TextCtrl(self, -1, toSystemEncoding(self.lien.path), size = (-1, 16))
        self.texte.SetToolTipString(u"Saisir un nom de fichier/dossier\nou faire glisser un fichier")
        if self.dossier:
            bt1 =wx.BitmapButton(self, 100, wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
            bt1.SetToolTipString(u"Sélectionner un dossier")
            self.Bind(wx.EVT_BUTTON, self.OnClick, bt1)
            sizer.Add(bt1)
        bt2 =wx.BitmapButton(self, 101, wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))
        bt2.SetToolTipString(u"Sélectionner un fichier")
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.texte)
        
        sizer.Add(bt2)
        sizer.Add(self.texte,1,flag = wx.EXPAND)
        
        self.btnlien = wx.BitmapButton(self, -1, wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16, 16)))
        self.btnlien.SetToolTipString(u"Ouvrir le lien externe")
        self.btnlien.Show(self.lien.path != "")
        self.Bind(wx.EVT_BUTTON, self.OnClickLien, self.btnlien)
        sizer.Add(self.btnlien)
         
        
        # Pour drag&drop direct de fichiers !! (expérimental)
        file_drop_target = MyFileDropTarget(self)
        self.SetDropTarget(file_drop_target)
        
        return sizer
    
    
    #############################################################################            
    def OnClickLien(self, event):
        self.lien.Afficher(self.pathseq)


    ###############################################################################################
    # Overridden from ComboCtrl, called when the combo button is clicked
    def OnClick(self, event):
        
        if event.GetId() == 100:
            dlg = wx.DirDialog(self, u"Sélectionner un dossier",
                          style=wx.DD_DEFAULT_STYLE,
                          defaultPath = toSystemEncoding(self.pathseq)
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
            if dlg.ShowModal() == wx.ID_OK:
                self.SetPath(dlg.GetPath())
    
            dlg.Destroy()
            
        else:
            dlg = wx.FileDialog(self, u"Sélectionner un fichier",
                                wildcard = self.ext,
                                defaultDir = toSystemEncoding(self.pathseq),
    #                           defaultPath = globdef.DOSSIER_EXEMPLES,
                               style = wx.DD_DEFAULT_STYLE
                               #| wx.DD_DIR_MUST_EXIST
                               #| wx.DD_CHANGE_DIR
                               )
    
            if dlg.ShowModal() == wx.ID_OK:
                self.SetPath(dlg.GetPath())
    
            dlg.Destroy()
        
        self.MiseAJour()
        
        self.SetFocus()


    ###############################################################################################
    def MiseAJour(self):
        self.btnlien.Show(self.lien.path != "")


    ###############################################################################################
    def dropFiles(self, file_list):
        for path in file_list:
            self.SetPath(path)
            return
            
    ##########################################################################################
    def EvtText(self, event):
        self.SetPath(event.GetString())


    ##########################################################################################
    def GetPath(self):
        return self.lien
    
    
    ##########################################################################################
    def SetPath(self, lien, marquerModifier = True):
        """ lien doit étre de type 'String' encodé en SYSTEM_ENCODING
            
        """
#         print t
        self.lien.EvalLien(lien, self.pathseq)
        
        try:
            self.texte.ChangeValue(self.lien.path)
        except:
            self.texte.ChangeValue(toSystemEncoding(self.lien.path)) # On le met en SYSTEM_ENCODING

        self.MiseAJour()
        
        self.Parent.GetPanelRacine().OnPathModified(self.lien, marquerModifier = marquerModifier)
        
        
    ##########################################################################################
    def SetPathSeq(self, pathseq):
        self.pathseq = pathseq


#############################################################################################################
#
# A propos ...
# 
#############################################################################################################
class A_propos(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, u"A propos de "+ version.__appname__)
        
        self.app = parent
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        titre = wx.StaticText(self, -1, " "+version.__appname__)
        titre.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, False))
        titre.SetForegroundColour(wx.NamedColour("BROWN"))
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
        
        lstActeurs = ((u"Développement : ", (u"Cédrick FAURY", u"Jean-Claude FRICOU")), \
                      (u"Référentiels : ",  (u"Thierry VALETTE (STS EE)", \
                                             u"Jean-Claude FRICOU (STS SN)", \
                                             u"Emmanuel VIGNAUD (Ede SI-CIT-DIT 2nde)", \
                                             u"Arnaud BULCKE (Techno Collège)", \
                                             u"Laurent Moutoussamy (MPSI)")), \
                      
                      (u"Remerciements : ", (u"un grand merci aux très nombreux", \
                                             u"utilisateurs qui ont pris le temps", \
                                             u"de nous signaler les dysfonctionnements,", \
                                             u"et de nous faire part de leurs remarques.",)),
                      
                      (u"Crédits : ",       (u"Icones :\n - https://fr.icons8.com\nwww.iconfinder.com",)))

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
            lictext = u"Le fichier de licence (LICENSE.txt) est introuvable !\n\n" \
                      u"Veuillez réinstaller pySequence !"
            messageErreur(self, u'Licence introuvable',
                          lictext)
            
            
        tl = wx.TextCtrl(licence, -1, lictext, size = (400, -1), 
                    style = wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_NONE )
        s = wx.BoxSizer()
        s.Add(tl, flag = wx.EXPAND)
        licence.SetSizer(s)
        
        # Description
        #-------------
        descrip = wx.Panel(nb, -1)
        t = wx.StaticText(descrip, -1,u"",
                          size = (400, -1))#,
#                        style = wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_NONE) 
        txt = wordwrap(u"<b>pySequence</b> est un logiciel d'aide à l'élaboration de séquences et progressions pédagogiques et à la validation de projets,\n"
                                          u"sous forme de fiches exportables au format PDF ou SVG.\n"
                                          u"Il est élaboré en relation avec les programmes et les documents d'accompagnement\n"
                                          u"des enseignements des filières :\n"
                                          u" STI2D, \n SSI\n Technologie Collège\n STS EE et SN\n EdE SI-CIT-DIT 2nde.", 500, wx.ClientDC(self))
        if hasattr(t, 'SetLabelMarkup'): # wxpython 3.0
            t.SetLabelMarkup(txt )
        else:
            t.SetLabe(txt.replace('<b>', '').replace('</b>', '') )
        nb.AddPage(descrip, u"Description")
        nb.AddPage(auteurs, u"Auteurs")
        nb.AddPage(licence, u"Licence")
        
        sizer.Add(hl.HyperLinkCtrl(self, wx.ID_ANY, u"Informations et téléchargement : %s" %version.__url__,
                                   URL = version.__url__),  
                  flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
        sizer.Add(nb)
        
        self.SetSizerAndFit(sizer)

class StaticBitmapZoom(wx.StaticBitmap):
    def __init__(self, *args, **kargs):
        wx.StaticBitmap.__init__(self, *args, **kargs)
        
        self.Bind(wx.EVT_MOTION, self.OnMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)

    def SetLargeBitmap(self, largeBitmap):
        self.largeBitmap = largeBitmap
        self.W, self.H = largeBitmap.GetWidth(), largeBitmap.GetHeight()
        self.OnLeave()
    
    def OnLeave(self, event = None):
        self.SetBitmap(self.largeBitmap.ConvertToImage().Scale(*self.GetSize()).ConvertToBitmap())
        
    def OnMove(self, event):
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
        self.SetForegroundColour(wx.NamedColour("DIM GREY"))
        
        
#############################################################################################################
#
# ProgressDialog personnalisé
# 
#############################################################################################################
# if sys.platform == "win32":
#     import win32gui
# #    import win32con
# class myProgressDialog2(wx.ProgressDialog):
#     def __init__(self, titre, message, maximum, parent, style = 0):
#         wx.ProgressDialog.__init__(self, titre,
#                                    message,
#                                    maximum = maximum,
#                                    parent = parent,
#                                    style = style
#                                     | wx.PD_APP_MODAL
#                                     | wx.STAY_ON_TOP
#                                     | wx.FRAME_FLOAT_ON_PARENT
#                                     #| wx.PD_CAN_ABORT
#                                     #| wx.PD_CAN_SKIP
#                                     #| wx.PD_ELAPSED_TIME
#                                     | wx.PD_ESTIMATED_TIME
#                                     | wx.PD_REMAINING_TIME
#                                     #| wx.PD_AUTO_HIDE
#                                     )
# 
# #        hwnd = self.GetHandle()
# #        exstyle = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
# #        theStyle = win32con.HWND_TOPMOST
# #        win32gui.SetWindowPos(hwnd, theStyle, 0, 0, 0, 0, win32con.SWP_NOSIZE|win32con.SWP_NOMOVE)
#         
#         self.Bind(wx.EVT_UPDATE_UI, self.OnUpdate)
#         self.Bind(wx.EVT_CLOSE, self.OnClose)
#         
#         wx.CallAfter(self.top)
#         
#     def OnUpdate(self,evt):
#         self.top()
#         evt.Skip()
#         
#         
#     def top(self):
#         if sys.platform == "win32":
#             try:
#                 win32gui.SetForegroundWindow(self.GetHandle())
#             except:
#                 pass
#         else:
#             self.RequestUserAttention()
#             self.Iconize(False)
#             self.Raise()
#         return
#         
#         
# #        return
# #        if sys.platform != "win32":
# #            return
# #        hwnd = self.GetHandle()
# #        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
# #                              win32con.SWP_NOSIZE | win32con.SWP_NOMOVE
# #                              ) 
#         
#     def OnClose(self, event):
# #        print "Close dlg"
#         self.Destroy()        





class myProgressDialog(wx.Frame):
    def __init__(self, titre, message, maximum, parent, style = 0, 
                 btnAnnul = True, msgAnnul = u"Annuler l'opération"):

        wx.Frame.__init__(self, parent, -1, titre, size = (400, 200),
                          style = wx.FRAME_FLOAT_ON_PARENT| wx.CAPTION | wx.FRAME_TOOL_WINDOW | wx.STAY_ON_TOP)
#         pre = wx.PreDialog()
#         pre.Create(parent, -1, titre)
#         self.PostCreate(pre)
#         print "myProgressDialog", maximum

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
        sizer.Add(self.titre, 0, wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, 20)

        self.message = wx.TextCtrl(panel, -1, size = (-1, 200), 
                                   style = wx.TE_MULTILINE|wx.TE_READONLY|wx.VSCROLL|wx.TE_NOHIDESEL)
        sizer.Add(self.message, 1, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.EXPAND, 15)
        
        self.SetMessage(message)
        
        
        self.gauge = wx.Gauge(panel, -1, maximum)
        sizer.Add(self.gauge, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5)
#         print dir(self.gauge)
        if maximum < 0:
            self.gauge.Pulse()
            
        line = wx.StaticLine(panel, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5)

        self.btn = wx.Button(panel, -1, u"Annuler")
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

        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        
        self.CenterOnParent()
        self.SetMinSize((400, -1))
        self.GetParent().Enable(False)
        wx.Frame.Show(self)
        
        
#         self.Show()#WindowModal()
#         print "fini"

#     def Show(self):
#         self.CenterOnParent()
#         self.GetParent().Enable(False)
#         wx.Frame.Show(self)
#         self.Raise()
        
        



    def OnDestroy(self, event):
        self.GetParent().Enable(True)
        event.Skip()
    
    def Update(self, count, message):
#         print "Update", count
        self.SetMessage(message)
        self.count = count
        
        if self.maximum >= 0 and (self.count >= self.maximum or self.count < 0):
            self.GetParent().Enable(True)
            self.btn.SetLabel(u"Ok")
        self.panel.Layout()
        self.Fit()

        wx.Frame.Update(self)
        
        if self.maximum >= 0:
            wx.CallAfter(self.gauge.SetValue, self.count)
    #         self.gauge.SetValue(self.count)
            self.gauge.Update()
            self.gauge.Refresh()
            
            wx.Yield()
            try:
                self.gauge.UpdateWindowUI()
            except:
                pass
            
        self.gauge.Refresh()
#         time.sleep(.1)
#         self.Refresh()
        
        

    def SetMessage(self, message):
        m = message.split(u"\n\n")
        if len(m) > 1:
            t, m = m[0], u"\n\n".join(m[1:])
        else:
            t, m = m[0], u""
            
        self.titre.SetLabel(t)
        self.message.ChangeValue(m)
#         self.message.ScrollLines(-1)
#         self.message.ScrollPages(1) 
        self.message.ShowPosition(self.message.GetLastPosition ())
        
    
    def OnClick(self, event):
        self.GetParent().Enable(True)
        if event.GetEventObject().GetLabel()[0] == u"A":
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
        print 'OnCellClicked: %s, (%d %d)\n' % (cell, x, y)
        if isinstance(cell, html.HtmlWordCell):
            sel = html.HtmlSelection()
            print '     %s\n' % cell.ConvertToText(sel)
        super(myHtmlWindow, self).OnCellClicked(cell, x, y, evt)




class PopupInfo(wx.PopupWindow):
    def __init__(self, parent, page, mode = "H", size=(400, 300)):
        wx.PopupWindow.__init__(self, parent, wx.BORDER_SIMPLE)
        self.parent = parent
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #
        self.mode = mode
        if mode == "H":
            self.html = myHtmlWindow(self, -1, size = size,
                                        style=wx.NO_FULL_REPAINT_ON_RESIZE|html.HW_SCROLLBAR_NEVER)
        else:
            self.html = webview.WebView.New(self, size = size)
            self.SetClientSize(size)
        
        self.SetHTML(page)
        self.SetPage()
        self.SetAutoLayout(True)
        
        # Un fichier temporaire pour mettre une image ...
        self.tfname = []
        
        
        #'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'+
        sizer.Add(self.html)
        
        self.SetSizer(sizer)
        
        self.html.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
#         self.Bind(wx.EVT_MOTION, self.OnLeave)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)
        self.Bind(wx.EVT_BUTTON, self.OnClick)


#    ##########################################################################################
#    def SetBranche(self, branche):
#        self.branche = branche

    #####################################################################################
    def SetHTML(self, ficheHTML):
        self.soup = BeautifulSoup(ficheHTML, "html5lib")#.decode('utf-8')
#.encode('utf-8', errors="ignore"), from_encoding="utf-8"


    #####################################################################################
    def Supprime(self, Id):
        tag = self.soup.find(id=Id)
        tag.extract()


    #####################################################################################
    def AjouterHTML(self, Id, text):
        """ Ajoute un texte au format HTML
        """
#         print "AjouterHTML", text
        if text is None:
            return
        tag = self.soup.find(id=Id)
        t = BeautifulSoup(text, "html5lib")
        for c in t.contents:
            tag.append(c)
        
        
        
    #####################################################################################
    def SetWholeText(self, Id, text, bcoul = None, fcoul = "black", 
                     bold = False, italic = False, size = 0):
        """ 
        """
#        print "SetWholeText", text
        if text is None:
            return
        
#         text = text.replace("\n", "<br/>")
        tag = self.soup.find(id=Id)
        
        li = text.split("\n")
        for i, t in enumerate(li):
            f = self.soup.new_tag("font")
            f.string = t
            
            if fcoul != "black":
                f["color"] = fcoul
                
            if size != 0:
                f["size"] = size
                
            if bold:   
                f.string.wrap(self.soup.new_tag("b"))
    
            if italic:     
                f.string.wrap(self.soup.new_tag("i"))
            
            tag.append(f)
            if i < len(li) -1:
                br = self.soup.new_tag('br')
                tag.append(br)


    ##########################################################################################
    def AjouterLien(self, Id, lien, elem):

        tag = self.soup.find(id = Id)
        
        if lien.type == 'u':
            a = self.soup.new_tag("a")
            a.string = lien.path
            a["href"] = lien.path
            tag.append(a)
            
        elif lien.type in ["f", "d"]:
            self.elem = elem
            b = self.soup.new_tag("wxp")
            b["module"] = "wx"
            b["class"] = "Button"
            
            param  = self.soup.new_tag("param")
            param["name"] = "id"
            param["value"] = "-1"
            b.append(param)
            
            param  = self.soup.new_tag("param")
            param["name"] = "label"
            param["value"] = os.path.split(lien.path)[1]
            b.append(param)
            
#             param  = self.soup.new_tag("param")
#             param["name"] = "name"
#             param["value"] = "Bouton"
#             b.append(param)
            
            tag.append(b)
            
        
    
    ##########################################################################################
    def AjouterTxt(self, Id, texte, bcoul = None, fcoul = "black", 
                     bold = False, italic = False, size = 0):
#        print "AjouterTxt", texte
        tag = self.soup.find(id = Id)
        
        if fcoul != None or size != 0:     
            f = self.soup.new_tag("font")
            if fcoul != None:
                f["color"] = fcoul
            if size != 0:
                f["size"] = size

            tag.append(f)
            tag = f
            
        if bold:   
            b = self.soup.new_tag("b")
            tag.append(b)
            tag = b

        if italic:     
            i = self.soup.new_tag("i")
            tag.append(i)
            tag = i
            
        lignes = texte.split("\n")
        for i, l in enumerate(lignes):
            if i > 0:
                br = self.soup.new_tag('br')
                tag.append(br)
            tag.append(NavigableString(l))
#        print tag


    ##########################################################################################
    def AjouterImg(self, item, bmp, width = None):
        try:
            self.tfname.append(tempfile.mktemp()+".png")
            bmp.SaveFile(self.tfname[-1], wx.BITMAP_TYPE_PNG)
        except:
            return
        img = self.soup.find(id = item)
#        print "img", img
        img['src'] = self.tfname[-1]
        
        if width is not None:
            img['width'] = str(width)
            img['height'] = str(int(width*bmp.GetHeight()/bmp.GetWidth()))

#        img = node.getElementById(item)
#        if img != None:
#            td = node.createElement("img")
#            img.appendChild(td)
#            td.setAttribute("src", self.tfname)


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


    ####################################################################################
    def Construire(self, dic , tache, prj, code = None, check = False):
        """ Construit l'arborescence des Compétences et Indicateurs.
            Deux formats possibles pour <dicIndicateurs> :
            
        """
#        print "Construire", dicIndicateurs
#        print dic
        self.tache = tache
        self.dic = dic
        self.prj = prj
        self.code = code
        dicIndicateurs = tache.GetDicIndicateurs()
        def const(d, ul):
            ks = d.keys()
            ks.sort()
            for k in ks:
#                print "  k:", k
                competence = d[k]
                li = self.soup.new_tag("li")
                ul.append(li)
                
                if competence.sousComp != {}: #len(v) > 1 and type(v[1]) == dict:
#                    font = self.soup.new_tag("font")
                    nul = self.soup.new_tag("ul")
                    li.append(textwrap.fill(k+" "+competence.intitule, 50))
                    const(competence.sousComp, nul)
                    li.append(nul)
                    
                else:   # Indicateur
                    nul = self.soup.new_tag("ul")
                    cc = [cd+ " " + it for cd, it in zip(k.split(u"\n"), competence.intitule.split(u"\n"))] 
                    nul['type']="1"
                    li.append(textwrap.fill(u"\n ".join(cc), 50))

                    ajouteIndic(nul, competence.indicateurs, "S"+k, )
                
                    li.append(nul)
                
            return

        
                
                
        def ajouteIndic(fm, listIndic, code):
            if code in dicIndicateurs.keys():
                listIndicUtil = dicIndicateurs[code]
            else:
                listIndicUtil = None

            for i, indic in enumerate(listIndic):
                
                if i > 0:
                    br = self.soup.new_tag("br")   
                    fm.append(br)
                
                codeIndic = code+"_"+str(i+1)
                
                coche = check and tache.estACocherIndic(codeIndic)
                if coche:
                    li = self.soup.new_tag("wxp")
                    li["module"] = "widgets"
                    li["class"] = "CheckBoxValue"
                    param  = self.soup.new_tag("param")
                    param["name"] = "id"
                    param["value"] = str(100+i)
                    li.append(param)
                    
                    param  = self.soup.new_tag("param")
                    param["name"] = "name"
                    param["value"] = codeIndic
                    li.append(param)
                    
                    param  = self.soup.new_tag("param")
                    param["name"] = "value"
                    li.append(param)
                    
                    fm.append(li)
                    
                font = self.soup.new_tag("font")    
#                 li.append(font)
                font.append(textwrap.fill(indic.intitule, 50))
                
                
                
                fm.append(font)
#                 li['type']="1"
                
                for part in prj.parties.keys():
                    if part in indic.poids.keys():
                        if listIndicUtil == None or not listIndicUtil[i]:
                            c = COUL_ABS
                            if coche:
                                param["value"] = "False"
                        else:
                            c = getCoulPartie(part)
                            if coche:
                                param["value"] = "True"

                font['color'] = couleur.GetCouleurHTML(c, wx.C2S_HTML_SYNTAX)
        
        if type(dic) == dict:
            ul = self.soup.find(id = "comp")
            const(dic, ul)
        else:
            fm = self.soup.find(id = "comp")
            ajouteIndic(fm, dic, code)
    
    
    #########################################################################################################
    def GetDocument(self):
        return self.tache.GetDocument()
    
    
    
    #########################################################################################################
    def onUndoRedo(self):
        """ Renvoie True si on est en phase de Undo/Redo
        """
        return self.GetDocument().undoStack.onUndoRedo or self.GetDocument().classe.undoStack.onUndoRedo

     
    #########################################################################################################
    def sendEvent(self, doc = None, modif = u"", draw = True, obj = None):
        self.GetDocument().GetApp().sendEvent(doc, modif, draw, obj)
        self.eventAttente = False
        
        
    ############################################################################            
    def SetCompetences(self):
#        print "SetCompetences"
        
        self.GetDocument().MiseAJourDureeEleves()
        
        modif = u"Ajout/Suppression d'une compétence à la Tâche"
        if self.onUndoRedo():
            self.sendEvent(modif = modif)
        else:
            wx.CallAfter(self.sendEvent, modif = modif)
        self.tache.projet.Verrouiller()
        
        ul = self.soup.find(id = "comp")
        ul.clear()
        self.Construire(self.dic , self.tache, self.prj, self.code, check = True)
        self.SetPage()
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
      
        wx.CallAfter(self.SetCompetences)
    
    ##########################################################################################
    def OnClick(self, evt):
        b = evt.GetEventObject()
        n = b.GetName()
#         print "OnCheck", cb.GetValue(), cb.GetName()
        self.elem.lien.Afficher(self.elem.GetDocument().GetPath())

        
    ##########################################################################################
    def OnDestroy(self, evt): 
#         print "OnDestroy", evt.GetWindow()
        if isinstance(evt.GetWindow(), wx.PopupWindow):
            for f in self.tfname:
                if os.path.exists(f):
                    os.remove(f)


    ##########################################################################################
    def SetPage(self):
#        self.SetSize((10,1000))
#        self.SetClientSize((100,1000))
#        self.html.SetSize( (100, 100) )
#        self.SetClientSize(self.html.GetSize())
        
        
#        print self.GetClientSize()
#        print self.html.GetSize()
#        print self.html.GetClientSize()
        
#        self.SetClientSize(self.html.GetClientSize())
#        self.Fit()

        if self.mode == "H":
#             print self.soup.prettify()
            self.html.SetPage(self.soup.prettify())
            ir = self.html.GetInternalRepresentation()
    
            self.SetClientSize((ir.GetWidth(), ir.GetHeight()))
    
            self.html.SetSize((ir.GetWidth(), ir.GetHeight()))
        else:
            self.html.SetPage(self.soup.prettify(), "")

 
    ##########################################################################################
    def OnLeave(self, event):
#         print "Leave Tip",
        x, y = event.GetPosition()
        w, h = self.GetSize()
#         print y, h
        if not ( x > 0 and y > 0 and x < w-2 and y < h-2):
            self.Show(False)
        event.Skip()
        

    


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
        if int(wx.version()[0]) > 2:
            button.SetBitmap(images.Icone_sequence.Bitmap,wx.LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnSeq, button)
        sizer.Add(button,0, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5)
        
        button = wx.Button(self, -1, u"Nouveau Projet")
        button.SetToolTipString(u"Créer un nouveau projet")
        if int(wx.version()[0]) > 2:
            button.SetBitmap(images.Icone_projet.Bitmap,wx.LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnPrj, button)
        sizer.Add(button,0,  wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5)
    
        button = wx.Button(self, -1, u"Nouvelle Progression")
        button.SetToolTipString(u"Créer une nouvelle progression pédagogique")
        if int(wx.version()[0]) > 2:
            button.SetBitmap(images.Icone_progression.Bitmap,wx.LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnPrg, button)
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
        
    def OnPrg(self, event):
        self.SetReturnCode(3)
        self.EndModal(3)

#import pywintypes



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
            path = os.path.join(util_path.BO_PATH, toFileEncoding(d))
            for root, dirs, files in os.walk(path):
                for f in files:
                    if os.path.splitext(f)[1] == u".pdf":
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
        
        
        
##########################################################################################################
#
#  Panel pour l'affichage des tâches détailles par élève
#
##########################################################################################################
class Panel_Details(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.ConstruireTb()
        
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
    def Construire(self, fichierCourant, projet, typ):
        wx.BeginBusyCursor()
        
        self.fichierCourant = fichierCourant
        self.projet = projet
        
        # Suppression des pages
        for index in reversed(range(self.nb.GetPageCount())):
            try:
                self.nb.DeletePage(index)
            except:
                print "raté :", index
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
        
        tsize = constantes.IMG_SIZE_TB
        
        edit_bmp = scaleImage(images.document_edit.GetBitmap(),*tsize)
        save_bmp =  scaleImage(images.Icone_save.GetBitmap(),*tsize)
        saveas_bmp = scaleImage(images.Icone_saveas.GetBitmap(),*tsize)
        saveall_bmp =  scaleImage(images.Icone_saveall.GetBitmap(),*tsize)
        
        
#         edit_bmp = images.document_edit.GetBitmap()
#         save_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
#         saveas_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, tsize)
#         saveall_bmp =  images.Icone_saveall.GetBitmap()
        
        self.tb.SetToolBitmapSize(tsize)
        
        self.tb.AddLabelTool(10, u"Enregistrer", save_bmp, 
                             shortHelp=u"Enregistrement de la fiche courante sous son nom actuel", 
                             longHelp=u"Enregistrement de la fiche courante sous son nom actuel")
        
        self.tb.AddLabelTool(12, u"Enregistrer tout", saveall_bmp, 
                             shortHelp=u"Enregistrement de tous les documents sous leurs noms actuels", 
                             longHelp=u"Enregistrement de tous les documents sous leurs noms actuels")
        

        self.tb.AddLabelTool(11, u"Enregistrer sous...", saveas_bmp, 
                             shortHelp=u"Enregistrement de la fiche courante sous un nom différent", 
                             longHelp=u"Enregistrement de la fiche courante sous un nom différent")
        
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrer, id=10)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrerSous, id=11)
        self.Bind(wx.EVT_TOOL, self.commandeEnregistrerTout, id=12)
        
        
        self.tb.AddSeparator()
        
        self.tb.AddLabelTool(13, u"Editer", edit_bmp, 
                             shortHelp=u"Editer la fiche", 
                             longHelp=u"Editer la fiche")
        
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
            page.Enregistrer(u"Enregistrer les détails", page.getNomFichierDefaut())


    ######################################################################################################
    def commandeEnregistrerTout(self, evt):
        for page in [self.nb.GetPage(i) for i in range(self.nb.GetPageCount())]:
            page.Enregistrer(u"Enregistrer les détails", page.getNomFichierDefaut())


    ######################################################################################################
    def commandeEnregistrerSous(self, evt):
        page = self.nb.GetCurrentPage()
        if page != None:
            page.EnregistrerSous(u"Enregistrer les détails", page.getNomFichierDefaut())
            
            
        



##########################################################################################################
#
#  CodeBranche : conteneur du code d'un élément à faire figurer dans un arbre
#
##########################################################################################################
class CodeBranche(wx.Panel):
    def __init__(self, arbre, code = u""):
        wx.Panel.__init__(self, arbre, -1)
        sz = wx.BoxSizer(wx.HORIZONTAL)
        self.code = wx.StaticText(self, -1, code)
        sz.Add(self.code)
        self.SetSizerAndFit(sz)
        self.comp = {}
        self.code.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        
    def OnClick(self, event):
#        print "OnClick"
        if hasattr(self, 'branche'):
            self.Parent.SelectItem(self.branche)
#        self.Parent.OnSelChanged(item = self.branche)
#        return
#        evt = wx.Event(-1, CT.EVT_TREE_SEL_CHANGED)
#        evt = wx.PyCommandEvent(CT.EVT_TREE_SEL_CHANGED.typeId, self.GetId())
#        print dir(evt)
#        evt.SetItem(self.branche)
#        self.Parent.GetEventHandler().ProcessEvent(evt)
        
    def SetBranche(self, branche): 
        self.branche = branche
        
    def SetItalic(self, italic = True):
        font = self.code.GetFont().Italic()
        self.code.SetFont(font)
         
    def Add(self, clef, text = u""):
        self.comp[clef] = wx.StaticText(self, -1, "")
        self.GetSizer().Add(self.comp[clef])
        
    def SetLabel(self, text):
        self.code.SetLabel(text)
        self.LayoutFit()
        
    def SetBackgroundColour(self, color):
        self.code.SetBackgroundColour(color)
        
    def SetForegroundColour(self, color):
        self.code.SetForegroundColour(color)
    
    def SetToolTipString(self, text):
        self.code.SetToolTipString(text)
        
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
            self.SetMinSize ( (tsize+25, height) )     
        
    
        
        
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
#     global app
#     if not wx.GetApp():
#         app = wx.PySimpleApp()
        
    # convert the image file to a temporary file
    tfname = tempfile.mktemp()
    try:
        img.SaveFile(tfname, wx.BITMAP_TYPE_PNG)
        data = b64encode(open(tfname, "rb").read())
    finally:
        if os.path.exists(tfname):
            try:
                os.remove(tfname)
            except:
                pass
    return data



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
                                  u"Les CI ne pouvant pas étre placés sur la cible\n"\
                                  u"apparaitront en orbite autour de la cible (2 maxi).\n\n"\
                                  u"Si le nombre de CI sélectionnés est limité à 2,\n"\
                                  u"le deuxiéme CI sélectionnable est forcément\n"\
                                  u"du méme domaine (MEI) que le premier\n"\
                                  u"ou bien un des CI en orbite.")
#        self.SetHelpBitmap(help)
        
        
        
        
        
import pysequence








# if __name__ == '__main__':
#     
# #    if appli.splash != None:
#     appli.AfterFlash() # Ouverture de la fenêtre principale
#     appli.MainLoop()
# #    else:
# #        sys.exit()

