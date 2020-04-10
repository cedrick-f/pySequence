#!/usr/bin/env python
# -*- coding: utf-8 -*-


##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                 proprietes                              ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014 Cédrick FAURY - Jean-Claude FRICOU
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
module proprietes
*****************

Module de gestion des propriétés d'un document

"""

import wx
import  wx.lib.scrolledpanel as scrolled
import wx.lib.agw.labelbook as LB
from wx.lib.agw.fmresources import *
import images
from widgets import img2str, enregistrer_root, safeParse, scaleImage
import xml.etree.ElementTree as ET
from wx.lib.embeddedimage import PyEmbeddedImage

from couleur import CouleurFloat2CSS, CouleurCSS2Float
import constantes
from dpi_aware import *


####################################################################################################
#
# Constantes
#
####################################################################################################
CATEGORIES = ["Généralités",
              "Affichage"]

TYPES = {}



####################################################################################################
#
# Classes définissant les propriétés d'un document
#
####################################################################################################
class Propriete():
    def __init__(self, code, nom = "", value = "", ptype = None, 
                 cat = "", grp = "", sgrp = ""):
        """ Définition d'une propriété de document
            
            :value: valeur : peut prendre différents types
                bool
                int
                int (list)
                int (couleur)
                string
            :ptype: type de valeur
                list (choix)
                "coul" : couleur
                None : type donné par le type de valeur
                
        """
        self._codeXML = "Propriete"
        self.code = code
        self.nom = nom
        self.value = value
        self.ptype = ptype      # Code de type de donnée (définis comme constante)
        self.cat = cat          # Numéro de catégorie (définies comme constante)
        self.grp = grp          # Code de groupe (dépend du type de document)
        self.sgrp = sgrp        # Code de sous-groupe (dépend du type de document)
        
    
    def __repr__(self):
        return self.nom + " = " + str(self.value)

    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML pour enregistrement
        """
#         self.chargerParametresDraw()
        # Création de la racine
        propriete = ET.Element(self.code)
        
        propriete.set("Nom", self.nom)
        propriete.set("Cat", self.cat)
        propriete.set("Grp", self.grp)
        propriete.set("sGrp", self.sgrp)
        propriete.set("Type", self.ptype)
        
        if self.ptype in ["Bcol", "Icol"]:
            propriete.set("Val", CouleurFloat2CSS(self.value))
                        
        elif self.ptype in ["siz", "pos"]:
            propriete.set("Val", " ".join([str(v) for v in self.value]))
            
        else:
            propriete.set("Val", str(self.value))
        
        return propriete
            
    ######################################################################################  
    def setBranche(self, branche):
        """
        """
        self.code  = branche.tag
        self.nom  = branche.get("Nom", "")
        self.cat  = branche.get("Cat", "")
        self.grp  = branche.get("Grp", "")
        self.sgrp  = branche.get("sGrp", "")
        self.ptype  = branche.get("Type", "")
        
        if self.ptype in ["Bcol", "Icol"]:
            self.value = CouleurCSS2Float(branche.get("Val", "#000000"))
    
            
        elif self.ptype in ["siz", "pos"]:
            self.value = [float(v) for v in branche.get("Val","").split()]
            
        else:
            self.value = float(branche.get("Val"))



# ###################################################################################
# class Categorie():
#     def __init__(self, nom, lstgrp = []):
#         self._codeXML = "Categorie"
#         self.nom = nom
#         self.image = wx.Bitmap(100, 100)
#         self.setGrp(lstgrp)
#         
#         
#     def setGrp(self, lstgrp = []):
#         self.groupes = [Groupe(n) for n in lstgrp]        # Codes des Groupes de propriété
#         
#     def setBmp(self, bmp):
#         self.image = bmp
#         
#         
#     ######################################################################################  
#     def getBranche(self):
#         """ Renvoie la branche XML pour enregistrement
#         """
# #         self.chargerParametresDraw()
#         # Création de la racine
#         categorie = ET.Element(self._codeXML)
#         
#         categorie.set("Nom", self.nom)
#         
#         groupes = ET.SubElement(categorie, "Groupes")
#         for g in self.groupes:
#             groupes.append(g.getBranche())
#         
#         categorie.set("Image", str(img2str(self.image.ConvertToImage()), 'utf-8'))
#             
#         return categorie
# 
# 
#     ######################################################################################  
#     def setBranche(self, branche):
#         
#         self.nom  = branche.get("Nom", "")
#         
#         data = branche.get("Image", "")
#         self.image = wx.Bitmap(100, 100)
#         if data != "":
#             try:
#                 self.image = PyEmbeddedImage(data).GetBitmap()
#             except:
#                 Ok = False
#         
#         groupes = branche.find("Groupes")
#         self.groupes = []
#         if groupes != None:
#             for e in list(groupes):
#                 g = Groupe(self)
#                 Ok = g.setBranche(e)
#                 self.groupes.append(g)
#                 
#                 
        


###################################################################################
class Groupe():
    def __init__(self, code, nom = ""):
        self._codeXML = "Groupe"
        self.code = code
        self.nom = nom
        
        
    ######################################################################################  
    def getBranche(self, suff = ""):
        """ Renvoie la branche XML pour enregistrement
        """
        groupe = ET.Element(self.code)
        groupe.set("Nom", self.nom)
        
        return groupe
    
    
    ######################################################################################  
    def setBranche(self, branche):
        self.nom  = branche.get("Nom", "")
        self.code = branche.tag
        

###################################################################################
class ProprietesDoc():
    def __init__(self, doc = None):

        self._codeXML = "ProprietesDoc"
#         self.categories = [Categorie(n) for n in lstcat]    # Catégories de propriété
        self.groupes = {}
        self.sgroupes = {}
        self.proprietes = {}    # les Propriété
        self.doc = doc

    
    ######################################################################################  
    def get(self, code):
        return self.proprietes[code].value
    
    
    ######################################################################################  
    def set(self, code, val):
        self.proprietes[code].value = val
    
    
    ######################################################################################  
    def create(self, code, nom, val, ptype = None, cat = None, grp = None):
        if code in self.proprietes:
            return
        self.proprietes[code] = Propriete(nom, val, ptype, cat, grp)
    
    
    
    ######################################################################################  
    def update(self, dic_prop, dic_grp, dic_sgrp):
        for code, prop in dic_prop.items():
            self.proprietes[code] = prop
            
        for code, nom in dic_grp.items():
            self.groupes[code] = Groupe(code, nom)
    
        for code, nom in dic_sgrp.items():
            self.sgroupes[code] = Groupe(code, nom)
            
            
            
    ######################################################################################  
    def sauv(self, nomFichier):
        b = self.getBranche()
        constantes.indent(b)
        enregistrer_root(b, nomFichier, xml_declaration = True)



    ######################################################################################  
    def ouvr(self, nomFichier):
        root = safeParse(nomFichier, None)
        if root is None:
            return
#         print(ET.tostring(root))
#         docprop = root.find(self._codeXML)
        self.setBranche(root)
        
#     def chargerParametresDraw(self):
#         self.proprietes["ApparenceFiche"] = self.doc.draw.getParametres()
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML pour enregistrement
        """
#         self.chargerParametresDraw()
        # Création de la racine
        docprop = ET.Element(self._codeXML)
        
#         categories = ET.SubElement(docprop, "Categories")
#         for cat in self.categories:
#             print("cat", cat)
#             categories.append(cat.getBranche())
            
        branchegrp = ET.Element("Groupes")
        docprop.append(branchegrp)
        for c, p in self.groupes.items():
#             ET.SubElement(brancheprop, c)
            branchegrp.append(p.getBranche())
            
        branchegrp = ET.Element("sGroupes")
        docprop.append(branchegrp)
        for c, p in self.sgroupes.items():
#             ET.SubElement(brancheprop, c)
            branchegrp.append(p.getBranche())
            
        brancheprop = ET.Element("Proprietes")
        docprop.append(brancheprop)
        for c, p in self.proprietes.items():
#             ET.SubElement(brancheprop, c)
            brancheprop.append(p.getBranche())
            
        return docprop


    ######################################################################################  
    def setBranche(self, branche):
        
        self.categories = []
        
#         categories = branche.find("Categories")
#         self.categories = []
#         if categories != None:
#             for e in list(categories):
#                 cat = Categorie(self)
#                 Ok = cat.setBranche(e)
#                 self.categories.append(cat)
                
        
        branchegrp = branche.find("Groupes")
        self.groupes = {}
        if branchegrp is not None:
            for e in list(branchegrp):
                p = Groupe(e.tag)
                Ok = p.setBranche(e)
                self.groupes[e.tag] = p
                
        branchegrp = branche.find("sGroupes")
        self.sgroupes = {}
        if branchegrp is not None:
            for e in list(branchegrp):
                p = Groupe(e.tag)
                Ok = p.setBranche(e)
                self.sgroupes[e.tag] = p
        
        brancheprop = branche.find("Proprietes")
        self.proprietes = {}
        if brancheprop is not None:
            for e in list(brancheprop):
                p = Propriete(e.tag)
                Ok = p.setBranche(e)
#                 print('  ', e.tag, p.value)
                self.proprietes[e.tag] = p
                
                
        
####################################################################################################
#
# Classes définissant les fenêtres graphiques
#
####################################################################################################

class TBProprietes(LB.LabelBook):
    def __init__(self, parent, proprietes):
        LB.LabelBook.__init__(self, parent, -1, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             ,
                             agwStyle = INB_BORDER
                            )
        
        self.proprietes = proprietes
#         il = wx.ImageList(100, 100)
#         for p in self.proprietes.categories:
#             il.Add(p.image)
#         self.AssignImageList(il)
        

        for i, c in enumerate(self.proprietes.categories):
            win = PanelProprietes(self, c)
            self.AddPage(win, c.nom, i)
        
        self.SetSelection(0)
        
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)

#     def makePanel(self, cat):
#         p = wx.Panel(self, -1)
#         win = PanelProprietes(p, cat)
#         p.win = win
#         def OnCPSize(evt, win=win):
#             win.SetPosition((0,0))
#             win.SetSize(evt.GetSize())
#         p.Bind(wx.EVT_SIZE, OnCPSize)
#         return p
#     
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        event.Skip()



class PanelProprietes(scrolled.ScrolledPanel):
    def __init__(self, parent, categorie,
                 style = wx.VSCROLL | wx.RETAINED):
        scrolled.ScrolledPanel.__init__(self, parent, -1, style = style)#|wx.BORDER_SIMPLE)
        self.categorie = categorie
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        for grp in categorie.groupes:
            box = wx.StaticBox(self, -1, grp.nom)
            bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            self.sizer.Add(bsizer, flag = wx.EXPAND|wx.ALL, border = 2)
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.SetupScrolling(scroll_x = False) 
        
        

class FrameProprietes(wx.Frame):
    def __init__(self, parent, proprietes):
        wx.Frame.__init__(self, parent, title = "Proprietes")
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.proprietes = proprietes
        pnl = TBProprietes(self, proprietes)
        self.sizer.Add(pnl, flag = wx.EXPAND)
        self.SetSizer(self.sizer)
    
    ###############################################################################################
    def ConstruireTb(self):
        """ Construction de la ToolBar
        """
#        print "ConstruireTb"

        #############################################################################################
        # Création de la barre d'outils
        #############################################################################################
        self.tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        
        
        tsize = (constantes.IMG_SIZE_TB[0]*SSCALE, constantes.IMG_SIZE_TB[1]*SSCALE)
        
#         new_bmp =  scaleImage(images.Icone_new.GetBitmap(), *tsize)
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
        
        
    def ourir(self):
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
            self.proprietes.ouvr(nomFichier)



if __name__ == '__main__':
#     import wx.lib.wxcairo
#     import cairocffi as cairo
#     from pysequence import Sequence
    
    app = wx.App(False)
#     doc = Sequence(app)
    p = ProprietesDoc(None, ["Généralités",
                       "Affichage"])
    p.categories[0].setGrp(["grp1", "grp2"])
    p.categories[0].setBmp(images.Icone_sequence.GetBitmap())
    
    p.categories[1].setGrp(["grp3", "grp4"])
    p.categories[1].setBmp(images.Icone_projet.GetBitmap())
    
    #        code,      nom,     val, ptype = None, cat = None, grp = None)
    p.create("code",    "nom1", 1, ptype = None, cat = 0, grp = 0)
    p.create("truc",    "nom2", 2, ptype = None, cat = 1, grp = 1)
    p.create("az",      "nom3", 3, ptype = None, cat = 0, grp = 1)
    p.create("wx",      "nom4", 4, ptype = None, cat = 1, grp = 0)
    p.create("ppapt",   "nom5", 5, ptype = None, cat = 0, grp = 1)
    
    frame = FrameProprietes(None, p)
    
    frame.Show(True)
    app.MainLoop()
    

    
    