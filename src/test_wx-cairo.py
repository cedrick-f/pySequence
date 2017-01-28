#!/usr/bin/env python
# -*- coding: utf-8 -*-
from draw_cairo import reduire_rect

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               wx_pysequence                             ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2011-2016 Cédrick FAURY - Jean-Claude FRICOU

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
test_wx-cairo.py

Copyright (C) 2011-2016
@author: Cedrick FAURY

"""


####################################################################################
#
#   Imports minimum et SplashScreen
#
####################################################################################
# Outils système
import os, sys

import wx

# Graphiques vectoriels
import draw_cairo
try:
    import wx.lib.wxcairo
    import cairo
    haveCairo = True
except ImportError:
    haveCairo = False




####################################################################################
#
#   Classes définissant la fenétre principale de l'application
#
####################################################################################
class FenetrePrincipale(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        
        self.SetMinSize((800,570)) # Taille mini d'écran : 800x600
        self.SetSize((800,570))
        #self.SetSize((1024,738)) # Taille pour écran 1024x768
        # On centre la fenétre dans l'écran ...
        #self.CentreOnScreen(wx.BOTH)
        
        self.texte = u"""Certains gérants de centre équestre sont seuls ou ont des employés saisonniers et/ou à temps partiel. Ainsi, ils ne peuvent pas tout gérer et être partout à la fois. Comment peut-on les soulager de certaines tâches en leur proposant un dispositif qui les informe sur les chevaux montés ou restés au box, sur l'état général de l'écurie et les alerter en cas de souci majeur ? 
Il vous est demandé de réaliser une maquette du dispositif et de la tester en conformité au CDC. """
        self.sizer = wx.BoxSizer()
        
        self.sizer_g = wx.BoxSizer(wx.VERTICAL)
        
        
        self.text_ctrl = wx.TextCtrl(self, -1, self.texte,
                                     style = wx.TE_MULTILINE)
        self.dess_ctrl = BaseFiche(self)
        
        self.sizer_g.Add(self.text_ctrl, 1, flag = wx.EXPAND)
        
        #31.999999999999996, 8.0, 38.414, 15.0
        self.rect = {"x" : 320.0, "y" : 80.0, "w" : 384.14, "h" : 150.0, 
                     'le' : 0.8, 'pe' : 1.0, 'b' : 0.5}
        for n in ["x", "y", "w", "h", 'le', 'pe', 'b']:
            v = self.rect[n]
            if n in ["x", "y", "w", "h"]:
                mn, mx, inc = 0.1, 1000.0, 0.5
            elif n in ['b']:
                mn, mx, inc = 0.0, 1.0, 0.1
            elif n in ['le', 'pe']:
                mn, mx, inc = 0.1, 2.0, 0.1
            self.createSpin(v, n, mn, mx, inc)
        
        
        
        
        
        
        self.pos = {"va" : 'c', "ha" : 'g'}
        
        self.rbh = wx.RadioBox(self, -1, "ha",wx.DefaultPosition, wx.DefaultSize,
                          ['g', 'c', 'd'], 1, wx.RA_SPECIFY_COLS,
                          name = "ha")
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.rbh)
        
        
        self.rbv = wx.RadioBox(self, -1, "va",wx.DefaultPosition, wx.DefaultSize,
                          ['h', 'c', 'b'], 1, wx.RA_SPECIFY_COLS,
                          name = "va")
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.rbv)
        
        self.sizer_g.Add(self.rbv, flag = wx.EXPAND)
        self.sizer_g.Add(self.rbh, flag = wx.EXPAND)
        
        
        self.x = wx.StaticText(self, -1, u"")
        self.y = wx.StaticText(self, -1, u"")
        self.sizer_g.Add(self.x, flag = wx.EXPAND)
        self.sizer_g.Add(self.y, flag = wx.EXPAND)
        
        
        
        
        
        
        
        self.sizer.Add(self.sizer_g, flag = wx.EXPAND)
        self.sizer.Add(self.dess_ctrl, 1, flag = wx.EXPAND)
        
        
        self.Bind(wx.EVT_TEXT, self.OnText)
        

        self.SetSizer(self.sizer)
        self.Layout()
        
#         self.Bind(wx.EVT_MENU, self.commandeNouveau, id=10)
#         self.Bind(wx.EVT_MENU, self.commandeOuvrir, id=11)
#         self.Bind(wx.EVT_MENU, self.commandeEnregistrer, id=12)
#         self.Bind(wx.EVT_MENU, self.commandeEnregistrerSous, id=13)
#         self.Bind(wx.EVT_MENU, self.exporterFiche, id=15)
#         self.Bind(wx.EVT_MENU, self.exporterDetails, id=16)
#         self.Bind(wx.EVT_MENU_RANGE, self.OnFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9)
    
    
    
    
    ###############################################################################################
    def createSpin(self, v, n, mn, mx, inc):
        s = wx.BoxSizer()
        
        tx = wx.StaticText(self, -1, n)
        s.Add(tx, flag = wx.EXPAND|wx.ALL, border = 2)
        
        sc = wx.SpinCtrlDouble(self, -1, value = str(v), min = mn, max = mx, inc = inc, name = n)
        sc.SetDigits(2)
        s.Add(sc, 1, flag = wx.EXPAND|wx.ALL, border = 2)
        
        self.sizer_g.Add(s, flag = wx.EXPAND)
        
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnSpin, sc)
        self.Bind(wx.EVT_TEXT, self.OnVal, sc)
        return
    
    
    ###############################################################################################
    def EvtRadioBox(self, evt):
        rb = evt.GetEventObject()
        p = rb.GetString(rb.GetSelection())
        if rb == self.rbh:
            self.pos["ha"] = p
        else:
            self.pos["va"] = p
        self.dess_ctrl.Redessiner()
        
        
    ###############################################################################################
    def OnText(self, evt):
        self.texte = self.text_ctrl.GetValue()
        self.dess_ctrl.Redessiner()

    ###############################################################################################
    def OnSpin(self, evt):
        sc = evt.GetEventObject()
        n = sc.GetValue()
        self.rect[sc.GetName()] = n
#         evt.Skip() 
        self.dess_ctrl.Redessiner()

    ###############################################################################################
    def OnVal(self, evt):
        sc = evt.GetEventObject()
        n = sc.GetValue()
        self.rect[sc.GetName()] = n
#         evt.Skip() 
        self.dess_ctrl.Redessiner()
    
    ###############################################################################################
    def GetVal(self, n):
        return float(self.rect[n])
    
    ###############################################################################################
    def GetRect(self):
        return self.rect["x"], self.rect["y"], self.rect["w"], self.rect["h"]
        
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
        new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        save_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        saveall_bmp =  images.Icone_saveall.GetBitmap()
        saveas_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, tsize)
        undo_bmp = wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, tsize)
        redo_bmp = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, tsize)
        
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
        self.tools = {'prj' : {}, 'seq' : {}, 'prg' : {}}
        for typ in ['prj', 'seq', 'prg']:
            for i, tool in self.GetTools(typ).items():
                self.tools[typ][i] = self.tb.AddLabelTool(i, tool.label, tool.image, 
                                                           shortHelp = tool.shortHelp, 
                                                           longHelp = tool.longHelp)

        

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
        self.supprimerOutils()
        self.miseAJourUndo()
        
        




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

        self.tool_menu = tool_menu
        
        help_menu = wx.Menu()
        help_menu.Append(21, u"&Aide en ligne\tF1")
        help_menu.AppendSeparator()
        help_menu.Append(22, u"A propos")

        mb.Append(file_menu, u"&Fichier")
        mb.Append(tool_menu, u"&Outils")
        mb.Append(help_menu, u"&Aide")
        
        self.SetMenuBar(mb)
    
   

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
        self.Bind(wx.EVT_MOTION, self.OnMove)

        self.InitBuffer()
        
        self.Bind(wx.EVT_SIZE, self.OnResize)

        
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
        if hasattr(self, 'ctx'):
            x, y = evt.GetPosition()
            _x, _y = self.CalcUnscrolledPosition(x, y)
            xx, yy = self.ctx.device_to_user(_x, _y)
            self.Parent.x.SetLabel(str(xx))
            self.Parent.y.SetLabel(str(yy))
        evt.Skip()
        
    #############################################################################            
    def OnPaint(self, evt):
#        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.DrawBitmap(self.buffer, 0,0) 

            
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
#             ctx.set_font_options(cairo.FontOptions(cairo.HINT_METRICS_OFF))
#             print ctx.get_font_options().get_hint_metrics(), cairo.HINT_METRICS_OFF
#             print ctx.get_font_options().get_hint_style(), cairo.HINT_STYLE_NONE
#             print ctx.get_font_options().get_antialias(), cairo.ANTIALIAS_NONE
#             fo = cairo.FontOptions()
#             fo.set_hint_metrics(cairo.HINT_METRICS_OFF)
#             fo.set_hint_style(cairo.HINT_STYLE_NONE)
#             fo.set_antialias(cairo.ANTIALIAS_NONE)
#             ctx.set_font_options(fo)
#             print ctx.get_font_options().get_hint_metrics(), cairo.HINT_METRICS_OFF
#             print ctx.get_font_options().get_hint_style(), cairo.HINT_STYLE_NONE
#             print ctx.get_font_options().get_antialias(), cairo.ANTIALIAS_NONE
            
            
            
            
            
#             print dir(ctx)
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
        
        
        
    #############################################################################            
    def Draw(self, ctx):
        #
        # Options générales
        #
        options = ctx.get_font_options()
        options.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        options.set_hint_style(cairo.HINT_STYLE_NONE)#cairo.HINT_STYLE_FULL)#
        options.set_hint_metrics(cairo.HINT_METRICS_OFF)#cairo.HINT_METRICS_ON)#
        ctx.set_font_options(options)
        
#         ff = Context.get_font_face()
        
        
        ctx.select_font_face (draw_cairo.font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb (0.6, 0.6, 0.9)
        
        rect = self.Parent.GetRect()
        
        ctx.set_source_rgb (0.0, 0.0, 0.0)
        ctx.set_line_width (0.0006 * draw_cairo.COEF)
        ctx.rectangle(*rect)
        ctx.stroke()
        
        
        
        le = self.Parent.rect['le']
        b = self.Parent.rect['b']
        ha = self.Parent.pos["ha"]
        va = self.Parent.pos["va"]
        
        fontSize, rect_eff = draw_cairo.show_text_rect(ctx, self.Parent.texte, rect, \
                   va = va, ha = ha, 
                   le = le, 
                   pe = self.Parent.rect['pe'], \
                   b = b, 
                   orient = 'h', \
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = True, 
                   coulBord = None, tracer = True, ext = "...", debug = True)
        
        fheight = ctx.font_extents()[2]
        x, y, w, h = rect
        rect = reduire_rect(x, y, w, h, fheight, b)
#         hl = fheight * le
#         ecart = fheight * b
#         rect = (rect[0]+ecart/2, rect[1]+ecart/2, rect[2]-ecart, rect[3]-ecart)
        ctx.set_source_rgb (0.6, 0.6, 0.9)
        ctx.set_line_width (0.0006 * draw_cairo.COEF)
        ctx.rectangle(*rect)
        ctx.stroke()
        
    
        ctx.set_source_rgb (0.9, 0.6, 0.6)
        ctx.set_line_width (0.0006 * draw_cairo.COEF)
        ctx.rectangle(*rect_eff)
        ctx.stroke()

#         print "***", fontSize, "!!!"





if __name__ == '__main__':
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = FenetrePrincipale(None)
    frame.Show(True)     # Show the frame.
    app.MainLoop()

