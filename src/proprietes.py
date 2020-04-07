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
from widgets import XMLelem


####################################################################################################
#
# Classes définissant les propriétés d'un document
#
####################################################################################################
class PropPropriete(XMLelem):
    def __init__(self, nom, value, ptype = None, cat = None, grp = None):
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
        self.nom = nom
        self.value = value
        self.ptype = ptype
        self.cat = cat
        self.grp = grp
        


###################################################################################
class PropCategorie(XMLelem):
    def __init__(self, nom, lstgrp = []):
        self._codeXML = "Categorie"
        self.nom = nom
        self.image = wx.Bitmap(100, 100)
        self.setGrp(lstgrp)
        
        
    def setGrp(self, lstgrp = []):
        self.groupes = [PropGroupe(n) for n in lstgrp]        # Codes des Groupes de propriété
        
    def setBmp(self, bmp):
        self.image = bmp


###################################################################################
class PropGroupe(XMLelem):
    def __init__(self, nom):
        self._codeXML = "Groupe"
        self.nom = nom


###################################################################################
class ProprietesDoc(XMLelem):
    def __init__(self, doc = None, lstcat = []):
        self._codeXML = "ProprietesDoc"
        self.categories = [PropCategorie(n) for n in lstcat]    # Catégories de propriété
        self.proprietes = {}    # les Propriété
        self.doc = doc
    
    def get(self, code):
        return self.proprietes[code].value
        
    def set(self, code, val):
        self.proprietes[code].value = val
    
    def create(self, code, nom, val, ptype = None, cat = None, grp = None):
        if code in self.proprietes:
            return
        self.proprietes[code] = PropPropriete(nom, val, ptype, cat, grp)
        
    def update(self, lst_prop):
        for code, prop in lst_prop.items():
            self.proprietes[code] = prop
            
        
        
#     def chargerParametresDraw(self):
#         self.proprietes["ApparenceFiche"] = self.doc.draw.getParametres()
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML pour enregistrement
        """
#         self.chargerParametresDraw()
        
        return XMLelem.getBranche(self)


    
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
        pnl = TBProprietes(self, proprietes)
        self.sizer.Add(pnl, flag = wx.EXPAND)
        self.SetSizer(self.sizer)
    


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
    

    
    