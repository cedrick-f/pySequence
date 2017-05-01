#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                  rapport                                ##
##               génération d'un rapport détaillé                          ##
##               des tâches à effectuer par les élèves lors d'un projet    ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2012 Cédrick FAURY

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
import os, sys
if sys.platform != "win32":
    import wxversion
#    wxversion.select('2.8')
import wx
import wx.richtext as rt
import richtext

from widgets import messageErreur
from util_path import toSystemEncoding

import images
import cStringIO

from draw_cairo import getHoraireTxt
from draw_cairo_prj import ICoulTache, BCoulTache
from draw_cairo_seq import ICoulSeance#, BCoulSeance

from xml.dom.minidom import parse, parseString

#from wx import ImageFromStream, BitmapFromImage, EmptyIcon

from wx.lib.embeddedimage import PyEmbeddedImage 

#from constantes import NOM_PHASE_TACHE#, TypesSeanceCourt

# Module utilisé pour tester la disponibilité du presse-papier
# (Windows seulement)
#if sys.platform == "win32":
#    import win32clipboard
    
import random
import time


Styles = {"Titre"     :     rt.RichTextAttr(),
          "Titre 1"   :     rt.RichTextAttr(),
          "Titre 2"   :     rt.RichTextAttr(),
          "Message"   :     rt.RichTextAttr(),
          "MessSens"  :     rt.RichTextAttr(),
          "Sous titre":     rt.RichTextAttr(),
          "Tableau"   :     rt.RichTextAttr()}

Styles["Titre"].SetParagraphStyleName("Titre")
Styles["Titre"].SetFontSize(18)
Styles["Titre"].SetTextColour((0,0,0))
Styles["Titre"].SetParagraphSpacingBefore(40)
Styles["Titre"].SetAlignment(wx.TEXT_ALIGNMENT_CENTRE)
Styles["Titre"].SetPageBreak(pageBreak=True)

Styles["Titre 1"].SetParagraphStyleName("Titre 1")
Styles["Titre 1"].SetFontSize(12)
Styles["Titre 1"].SetFontWeight(wx.FONTWEIGHT_BOLD)
Styles["Titre 1"].SetTextColour((0,0,180))
Styles["Titre 1"].SetParagraphSpacingBefore(10)
Styles["Titre 1"].SetAlignment(wx.TEXT_ALIGNMENT_LEFT)
Styles["Titre 1"].SetParagraphSpacingAfter(10)
if int(wx.version()[0]) > 2:
    Styles["Titre 1"].SetBulletStyle(wx.TEXT_ATTR_BULLET_STYLE_RIGHT_PARENTHESIS)
#Styles["Titre 1"].SetFontUnderlined(True)

Styles["Titre 2"].SetParagraphStyleName("Titre 2")
Styles["Titre 2"].SetFontSize(11)
Styles["Titre 2"].SetTextColour((0,0,120))
Styles["Titre 2"].SetParagraphSpacingAfter(0)
Styles["Titre 2"].SetParagraphSpacingBefore(10)
Styles["Titre 2"].SetAlignment(wx.TEXT_ALIGNMENT_LEFT)
Styles["Titre 2"].SetFontUnderlined(True)

Styles["Message"].SetParagraphStyleName("Message")
Styles["Message"].SetFontSize(10)
Styles["Message"].SetLeftIndent(80)
#Styles["Message"].SetFontStyle(wx.BOLD)
Styles["Message"].SetParagraphSpacingAfter(10)
Styles["Message"].SetParagraphSpacingBefore(10)
Styles["Message"].SetAlignment(wx.TEXT_ALIGNMENT_LEFT)

Styles["MessSens"].SetParagraphStyleName("MessSens")
Styles["MessSens"].SetFontSize(10)
Styles["MessSens"].SetTextColour((0,0,0))
#Styles["Message"].SetFontStyle(wx.BOLD)
Styles["MessSens"].SetParagraphSpacingAfter(10)
Styles["MessSens"].SetParagraphSpacingBefore(10)
Styles["MessSens"].SetAlignment(wx.TEXT_ALIGNMENT_LEFT)
Styles["MessSens"].SetTabs((800, 2000))

Styles["Tableau"].SetParagraphStyleName("Tableau")
Styles["Tableau"].SetFontSize(10)
#Styles["Tableau"].SetTextColour((0,0,0))
#Styles["Message"].SetFontStyle(wx.BOLD)
#Styles["Tableau"].SetParagraphSpacingAfter(10)
#Styles["Tableau"].SetParagraphSpacingBefore(10)



Styles["Sous titre"].SetFontSize(8)
Styles["Sous titre"].SetFontStyle(wx.ITALIC)#wx.TEXT_ATTR_FONT_ITALIC)
Styles["Sous titre"].SetAlignment(wx.TEXT_ALIGNMENT_CENTRE)

#########################################################################################
class StyleDeTexte:
    def __init__(self, font, color):
        self.font = font
        self.color = color
        
    def applique(self, win, color = None):
        if color != None:
            self.color = color
        win.SetFont(self.font)
        win.SetForegroundColour(self.color)


##########################################################################################
#class PanelRapport(wx.Panel):
#    def __init__(self, parent, fichierCourant, doc, typ):
#        wx.Panel.__init__(self, parent, -1)#,
##                            style = wx.DEFAULT_FRAME_STYLE)
#        
#        #
#        # Instanciation du rapport RichTextCtrl
#        #
#        self.rtc = RapportRTF(self, rt.RE_READONLY)#rt.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER)
#        
#        #
#        # On rempli le rapport
#        #
#        self.rtc.Remplir(fichierCourant, doc, typ)
#        
#        sizer = wx.BoxSizer(wx.VERTICAL)
#        sizer.Add(self.rtc, flag = wx.EXPAND)
#        self.SetSizer(sizer)
        
        

#########################################################################################
class FrameRapport(wx.Frame):
    def __init__(self, parent, fichierCourant, doc, typ, eleve = None):
        wx.Frame.__init__(self, parent, -1, u"Tâches élèves détaillées",
                            size=(700, 500))#,
#                            style = wx.DEFAULT_FRAME_STYLE)
        
        self.SetMinSize((700, -1))

        self.parent = parent
        
        self.SetIcon(images.getlogoIcon())
        
        self.MakeMenuBar()
        self.MakeToolBar()
        self.CreateStatusBar()

        
        #
        # Instanciation du rapport en RTF
        #
        self.rtc = RapportRTF(self)#rt.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER)
        wx.CallAfter(self.rtc.SetFocus)
        
        self.rtp = RTPrinting(self)
        
        #
        # On rempli le rapport
        #
        self.rtc.Remplir(fichierCourant, doc, typ, eleve)
    

        
#    def AddRTCHandlers(self):
#        # make sure we haven't already added them.
#        if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is not None:
#            return
#        
#        rt.RichTextBuffer.GetHandlers()[0].SetEncoding("iso-8859-1")
##        f = rt.RichTextFileHandler()#.SetEncoding("iso-8859-1")
#        # This would normally go in your app's OnInit method.  I'm
#        # not sure why these file handlers are not loaded by
#        # default by the C++ richtext code, I guess it's so you
#        # can change the name or extension if you wanted...
#        HTML = rt.RichTextHTMLHandler()
#        HTML.SetEncoding("latin_1")#"iso-8859-1")
#        rt.RichTextBuffer.AddHandler(HTML)
#        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())
##        rt.RichTextBuffer.AddHandler(rt.RICHTEXT_TYPE_RTF)
#        # This is needed for the view as HTML option since we tell it
#        # to store the images in the memory file system.
#        wx.FileSystem.AddHandler(wx.MemoryFSHandler())

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)


    ######################################################################################################
    def OnEnter(self, event):
        self.SetFocus()
        event.Skip()
        
    ######################################################################################################
    def OnFileSave(self, evt):
        self.rtc.Enregistrer(u"Enregistrer les détails")
#         if not self.rtc.GetFilename():
#             self.OnFileSaveAs(evt)
#             return
#         self.rtc.SaveFile()

    ######################################################################################################
    def OnFileSaveAs(self, evt):
        self.rtc.EnregistrerSous(u"Enregistrer les détails")
        
        
#         wildcard =  u"Rich Text Format (.rtf)|*.rtf|" \
#                     u"Format HTML (.html)|*.html|" \
#                     u"Fichier texte (.txt)|*.txt"
#         types = [0, 3, 2]
#         dlg = wx.FileDialog(self, u"Enregistrer les détails",
#                             wildcard=wildcard,
#                             style=wx.SAVE)
#         
#         if dlg.ShowModal() == wx.ID_OK:
#             path = dlg.GetPath()
#             ext = os.path.splitext(path)[1].lstrip('.')
#             
#             if os.path.exists(path):
#                 dlg = wx.MessageDialog(self, u"Le fichier existe déja !\n\n"\
#                                        u"Voulez-vous l'écraser ?", 
#                                        u"Fichier existant",
#                                        wx.ICON_WARNING | wx.YES_NO | wx.CANCEL)
#                 res = dlg.ShowModal()
#                 dlg.Destroy() 
#                 if res != wx.ID_YES:
#                     return
#                     
#             if path:
#                 if ext == 'txt':
#                     wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=True)
#                     fileType = 1
#                     ext = rt.RichTextBuffer.FindHandlerByType(fileType).GetExtension()
#                     if not path.endswith(ext):
#                         path += '.' + ext
#                     self.rtc.SaveFile(path, 1)
#                 elif ext == 'html':
#                     handler = rt.RichTextHTMLHandler()
#                     handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
#                     handler.SetFontSizeMapping([7,9,11,12,14,22,100])
#                     stream = cStringIO.StringIO()
#                     if handler.SaveStream(self.rtc.GetBuffer(), stream):
#                         f = open(path, 'w')
#                         f.write(prefixeHTML+stream.getvalue())#.encode(sys.getdefaultencoding()))
#                         f.close()
#                 elif ext == 'rtf':
#                     import PyRTFParser
#                     # Use the custom RTF Handler
#                     handler = PyRTFParser.PyRichTextRTFHandler()
#                     # Save the file with the custom RTF Handler.
#                     # The custom RTF Handler can take either a wxRichTextCtrl or a wxRichTextBuffer argument.
#                     handler.SaveFile(self.rtc.GetBuffer(), path)
#         dlg.Destroy()
              
    def OnApplyStyle(self, evt):
#        self.rtc.ApplyStyle(Styles[evt.GetString()])
        self.rtc.SetStyle(self.rtc.GetSelectionRange(), Styles[evt.GetString()])
    
    def OnFileExit(self, evt):
        self.Close(True)

    def OnBold(self, evt):
        self.rtc.ApplyBoldToSelection()
        
    def OnItalic(self, evt): 
        self.rtc.ApplyItalicToSelection()
        
    def OnUnderline(self, evt):
        self.rtc.ApplyUnderlineToSelection()
        
    def OnAlignLeft(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)
        
    def OnAlignRight(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)
        
    def OnAlignCenter(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_CENTRE)
        
    def OnIndentMore(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetLeftIndent(attr.GetLeftIndent() + 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)
       
    def OnIndentLess(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

        if attr.GetLeftIndent() >= 100:
            attr.SetLeftIndent(attr.GetLeftIndent() - 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)

    def OnParagraphSpacingMore(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() + 20);
            attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
            self.rtc.SetStyle(r, attr)
  
    def OnParagraphSpacingLess(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            if attr.GetParagraphSpacingAfter() >= 20:
                attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() - 20);
                attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
                self.rtc.SetStyle(r, attr)

    def OnLineSpacingSingle(self, evt): 
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(10)
            self.rtc.SetStyle(r, attr)
      
    def OnLineSpacingHalf(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(15)
            self.rtc.SetStyle(r, attr)

    def OnLineSpacingDouble(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(20)
            self.rtc.SetStyle(r, attr)
            
    def OnFont(self, evt):
        if not self.rtc.HasSelection():
            return

        r = self.rtc.GetSelectionRange()
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_FONT)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            fontData.SetInitialFont(attr.GetFont())

        dlg = wx.FontDialog(self, fontData)
        if dlg.ShowModal() == wx.ID_OK:
            fontData = dlg.GetFontData()
            font = fontData.GetChosenFont()
            if font:
                attr.SetFlags(wx.TEXT_ATTR_FONT)
                attr.SetFont(font)
                self.rtc.SetStyle(r, attr)
        dlg.Destroy()

    def OnColour(self, evt):
        colourData = wx.ColourData()
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            colourData.SetColour(attr.GetTextColour())

        dlg = wx.ColourDialog(self, colourData)
        if dlg.ShowModal() == wx.ID_OK:
            colourData = dlg.GetColourData()
            colour = colourData.GetColour()
            if colour:
                if not self.rtc.HasSelection():
                    self.rtc.BeginTextColour(colour)
                else:
                    r = self.rtc.GetSelectionRange()
                    attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
                    attr.SetTextColour(colour)
                    self.rtc.SetStyle(r, attr)
        dlg.Destroy()
        
    def OnUpdateBold(self, evt):
        evt.Check(self.rtc.IsSelectionBold())
    
    def OnUpdateItalic(self, evt): 
        evt.Check(self.rtc.IsSelectionItalics())
    
    def OnUpdateUnderline(self, evt): 
        evt.Check(self.rtc.IsSelectionUnderlined())
    
    def OnUpdateAlignLeft(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_LEFT))
        
    def OnUpdateAlignCenter(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_CENTRE))
        
    def OnUpdateAlignRight(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_RIGHT))

    def ForwardEvent(self, evt):
        # The RichTextCtrl can handle menu and update events for undo,
        # redo, cut, copy, paste, delete, and select all, so just
        # forward the event to it.
        self.rtc.ProcessEvent(evt)

    def MakeMenuBar(self):
        def doBind(item, handler, updateUI=None):
            self.Bind(wx.EVT_MENU, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)
            
        fileMenu = wx.Menu()
        doBind( fileMenu.Append(-1, u"&Enregistrer\tCtrl+S", u"Enregistrer le rapport"),
                self.OnFileSave )
        doBind( fileMenu.Append(-1, u"&Enregistrer sous...\tF12", u"Enregistrer le rapport"),
                self.OnFileSaveAs )
        fileMenu.AppendSeparator()
        doBind( fileMenu.Append(-1, u"&Mise en Page...\tCtrl+M", u"Règle la mise en page de l'impression"),
                self.OnPageSetup )
        doBind( fileMenu.Append(-1, u"Aperç&u avant impression...\tCtrl+U", u"Affiche un aperçu de ce qui sera imprimé"),
                self.OnPrintPreview )
        doBind( fileMenu.Append(-1, u"&Imprimer\tCtrl+P", u"Imprime le document"),
                self.OnDoPrint )
#        doBind( fileMenu.Append(-1, u"&Aperçu HTML", u"Affiche un aperçu HTML"),
#                self.OnFileViewHTML )
        fileMenu.AppendSeparator()
        doBind( fileMenu.Append(-1, u"&Quitter\tCtrl+Q", u"Quitter le visualisateur de rapport"),
                self.OnFileExit )
    
        
        fileMenu.AppendSeparator()

        
        editMenu = wx.Menu()
        doBind( editMenu.Append(wx.ID_UNDO, u"&Annuler\tCtrl+Z"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_REDO, u"&R�tablir\tCtrl+Y"),
                self.ForwardEvent, self.ForwardEvent )
        editMenu.AppendSeparator()
        doBind( editMenu.Append(wx.ID_CUT, u"Co&uper\tCtrl+X"),
                self.ForwardEvent, self.ForwardEvent )
        doBind( editMenu.Append(wx.ID_COPY, u"&Copier\tCtrl+C"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_PASTE, u"Co&ller\tCtrl+V"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_CLEAR, u"&E&ffacer\tDel"),
                self.ForwardEvent, self.ForwardEvent)
        editMenu.AppendSeparator()
        doBind( editMenu.Append(wx.ID_SELECTALL, "Selectionner tout\tCtrl+A"),
                self.ForwardEvent, self.ForwardEvent )
        
        #doBind( editMenu.AppendSeparator(),  )
        #doBind( editMenu.Append(-1, "&Find...\tCtrl+F"),  )
        #doBind( editMenu.Append(-1, "&Replace...\tCtrl+R"),  )

        formatMenu = wx.Menu()
        doBind( formatMenu.AppendCheckItem(-1, u"&Gras\tCtrl+B"),
                self.OnBold, self.OnUpdateBold)
        doBind( formatMenu.AppendCheckItem(-1, u"&Italic\tCtrl+I"),
                self.OnItalic, self.OnUpdateItalic)
        doBind( formatMenu.AppendCheckItem(-1, u"&Soulign�\tCtrl+U"),
                self.OnUnderline, self.OnUpdateUnderline)
        formatMenu.AppendSeparator()
        doBind( formatMenu.AppendCheckItem(-1, u"Aligner � &gauche"),
                self.OnAlignLeft, self.OnUpdateAlignLeft)
        doBind( formatMenu.AppendCheckItem(-1, u"&Centrer"),
                self.OnAlignCenter, self.OnUpdateAlignCenter)
        doBind( formatMenu.AppendCheckItem(-1, u"Aligner � &droite"),
                self.OnAlignRight, self.OnUpdateAlignRight)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, u"&Indenter"), self.OnIndentMore)
        doBind( formatMenu.Append(-1, u"&Desindenter"), self.OnIndentLess)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, u"&Augmenter l'espace entre paragraphe"), self.OnParagraphSpacingMore)
        doBind( formatMenu.Append(-1, u"&Diminuer l'espace entre paragraphe"), self.OnParagraphSpacingLess)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, u"Interligne &simple"), self.OnLineSpacingSingle)
        doBind( formatMenu.Append(-1, u"Interligne &x1.5"), self.OnLineSpacingHalf)
        doBind( formatMenu.Append(-1, u"Interligne &double"), self.OnLineSpacingDouble)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, u"&Police..."), self.OnFont)
        


        mb = wx.MenuBar()
        mb.Append(fileMenu, "&Fichier")
        mb.Append(editMenu, "&Edition")
        self.SetMenuBar(mb)

    def MakeToolBar(self):
        def doBind(item, handler, updateUI=None):
            self.Bind(wx.EVT_TOOL, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)
        
        tbar = self.CreateToolBar()
        doBind( tbar.AddTool(-1, _rt_save.GetBitmap(),
                            shortHelpString=u"Enregistrer"), self.OnFileSave)
        bmp = wx.ArtProvider_GetBitmap(wx.ART_PRINT).ConvertToImage().Rescale(17,17,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        doBind( tbar.AddTool(-1, bmp,
                            shortHelpString=u"Imprimer le rapport"), self.OnDoPrint)
        
        tbar.AddSeparator()
        doBind( tbar.AddTool(wx.ID_UNDO, _rt_undo.GetBitmap(),
                            shortHelpString=u"Annuler"), self.ForwardEvent, self.ForwardEvent)
        doBind( tbar.AddTool(wx.ID_REDO, _rt_redo.GetBitmap(),
                            shortHelpString=u"R�tablir"), self.ForwardEvent, self.ForwardEvent)
        
        tbar.AddSeparator()
        doBind( tbar.AddTool(wx.ID_CUT, _rt_cut.GetBitmap(),
                            shortHelpString=u"Couper dans le presse-papier"), self.ForwardEvent, self.ForwardEvent)
        doBind( tbar.AddTool(wx.ID_COPY, _rt_copy.GetBitmap(),
                            shortHelpString=u"Copier dans le presse-papier"), self.ForwardEvent, self.ForwardEvent)
        doBind( tbar.AddTool(wx.ID_PASTE, _rt_paste.GetBitmap(),
                            shortHelpString=u"Coller depuis le presse-papier"), self.ForwardEvent, self.ForwardEvent)
        
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, _rt_bold.GetBitmap(), isToggle=True,
                            shortHelpString=u"Gras"), self.OnBold, self.OnUpdateBold)
        doBind( tbar.AddTool(-1, _rt_italic.GetBitmap(), isToggle=True,
                            shortHelpString=u"Italic"), self.OnItalic, self.OnUpdateItalic)
        doBind( tbar.AddTool(-1, _rt_underline.GetBitmap(), isToggle=True,
                            shortHelpString=u"Soulign�"), self.OnUnderline, self.OnUpdateUnderline)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, _rt_alignleft.GetBitmap(), isToggle=True,
                            shortHelpString=u"Aligner � gauche"), self.OnAlignLeft, self.OnUpdateAlignLeft)
        doBind( tbar.AddTool(-1, _rt_centre.GetBitmap(), isToggle=True,
                            shortHelpString=u"Centrer"), self.OnAlignCenter, self.OnUpdateAlignCenter)
        doBind( tbar.AddTool(-1, _rt_alignright.GetBitmap(), isToggle=True,
                            shortHelpString=u"Aligner � droite"), self.OnAlignRight, self.OnUpdateAlignRight)
        
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, _rt_indentless.GetBitmap(),
                            shortHelpString="Indenter"), self.OnIndentLess)
        doBind( tbar.AddTool(-1, _rt_indentmore.GetBitmap(),
                            shortHelpString="Desindenter"), self.OnIndentMore)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, _rt_font.GetBitmap(),
                            shortHelpString="Police"), self.OnFont)
        doBind( tbar.AddTool(-1, _rt_colour.GetBitmap(),
                            shortHelpString="Couleur de police"), self.OnColour)

        tbar.AddSeparator()
        tbar.AddControl(
            wx.ComboBox(
                tbar, -1, "Styles", choices = Styles.keys(),
                size=(150,-1), style=wx.CB_DROPDOWN
                ))
        self.Bind(wx.EVT_COMBOBOX, self.OnApplyStyle)
        
        
        tbar.Realize()

    def OnPageSetup(self, evt):
        self.rtp.PageSetup() 
#        psdd = wx.PageSetupDialogData(self.printData)
#        psdd.CalculatePaperSizeFromId()
#        dlg = wx.PageSetupDialog(self, psdd)
#        dlg.ShowModal()
#
#        # this makes a copy of the wx.PrintData instead of just saving
#        # a reference to the one inside the PrintDialogData that will
#        # be destroyed when the dialog is destroyed
#        self.printData = wx.PrintData( dlg.GetPageSetupData().GetPrintData() )
#
#        dlg.Destroy()

    def OnPrintPreview(self, event = None):
        self.rtp.PreviewBuffer(self.rtc.GetBuffer()) 
#        data = wx.PrintDialogData(self.printData)
#        printout = MyPrintout(self.rtc)
#        printout2 = MyPrintout(self.rtc)
#        self.preview = wx.PrintPreview(printout, printout2, data)
##        rtp = rt.RichTextPrinting()
##        rt.RichTextPrinting(self, "test").PreviewBuffer(self.rtc.GetBuffer())
#        if not self.preview.Ok():
#            print "Erreur Preview"
#            return
#
#        pfrm = wx.PreviewFrame(self.preview, self, "This is a print preview")
#
#        pfrm.Initialize()
#        pfrm.SetPosition(self.rtc.GetPosition())
#        pfrm.SetSize(self.rtc.GetSize())
#        pfrm.Show(True)

    def OnDoPrint(self, event = None):
        self.rtp.PrintBuffer(self.rtc.GetBuffer()) 
        
#        pdd = wx.PrintDialogData(self.printData)
#        pdd.SetToPage(2)
#        printer = wx.Printer(pdd)
#        printout = MyPrintout(self.rtc)
#
#        if not printer.Print(self.rtc, printout, True):
#            wx.MessageBox("There was a problem printing.\nPerhaps your current printer is not set correctly?", "Printing", wx.OK)
#        else:
#            self.printData = wx.PrintData( printer.GetPrintDialogData().GetPrintData() )
#        printout.Destroy()
    
        
    def OnFileViewHTML(self, evt):
        # Get an instance of the html file handler, use it to save the
        # document to a StringIO stream, and then display the
        # resulting html text in a dialog with a HtmlWindow.
        handler = rt.RichTextHTMLHandler()
        handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
        handler.SetFontSizeMapping([7,9,11,12,14,22,100])

        import cStringIO
        stream = cStringIO.StringIO()
        if not handler.SaveStream(self.rtc.GetBuffer(), stream):
            return
        print stream.getvalue()
        import wx.html
        dlg = wx.Dialog(self, title="HTML", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        html = wx.html.HtmlWindow(dlg, size=(500,400), style=wx.BORDER_SUNKEN)
        html.SetPage(stream.getvalue())
        btn = wx.Button(dlg, wx.ID_CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 10)
        dlg.SetSizer(sizer)
        sizer.Fit(dlg)

        dlg.ShowModal()

        handler.DeleteTemporaryImages()





class RapportRTF(rt.RichTextCtrl): 
    def __init__(self, parent, style = 0):
#        print "RapportRTF"
        rt.RichTextCtrl.__init__(self, parent, style = rt.RE_MULTILINE | wx.WANTS_CHARS |style)

        self.style = style
        self.parent = parent   
         
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)


    ######################################################################################################
    def OnEnter(self, event):
        self.SetFocus()
        event.Skip()
        
        
    ######################################################################################################
    def Remplir(self, fichierCourant, doc, typ, eleve = None):
        isEditable = self.IsEditable()
        self.SetEditable(True)
        
        self.MoveEnd()
        self.Clear()
            
        #
        # On rempli le rapport
        #
        phase = ''
        if typ == 'prj':
#             for e in doc.eleves:
            self.AddTitreProjet(eleve, doc.GetProjetRef().attributs["FIC"][0])
            for t in doc.OrdonnerListeTaches(eleve.GetTaches(revues = True)):
                if t.phase != phase and t.phase != '':
                    phase = t.phase
                    self.AddPhase(t, doc.GetTypeEnseignement(simple = True))
                self.AddTache(t, revue = t.phase in ["R1", "R2", "R3", "Rev"])
            
            self.eleve = eleve
            self.projet = doc

        else:
            self.AddTitreSeance(doc)
    
            for s in doc.seances:
                self.AddSeance(s)
            
        self.AddPieds(fichierCourant)
        
        self.SetEditable(isEditable)
        self.ScrollIntoView(0, wx.WXK_HOME)
        
    
    ######################################################################################################
    def AddPieds(self, fichierCourant):
        self.Newline()
        self.BeginFontSize(8)
        self.BeginItalic()
        self.WriteText(os.path.basename(os.path.splitext(fichierCourant)[0]))
        self.EndItalic()
        self.EndFontSize()
       
        self.Newline()
        self.EndAlignment()
        
        
    ######################################################################################################
    def AddTitreProjet(self, eleve, titre):
#        print self.GetCaretPosition()
        if self.GetCaretPosition() == -1:
            Styles["Titre"].SetPageBreak(pageBreak=False)
        else:
            Styles["Titre"].SetPageBreak(pageBreak=True)
#        
        parag = self.AddParagraph(titre + u"\n")
        self.MoveEnd()
        self.Newline()
        
        self.BeginBold()
        self.BeginFontSize(14)
        self.WriteText(eleve.GetNomPrenom())
        self.EndFontSize()
        self.EndBold()
        self.BeginAlignment(wx.TEXT_ALIGNMENT_CENTRE)
        
        self.Newline()
        self.SetStyle(parag, Styles["Titre"])
        self.EndAlignment()
    
    
    ######################################################################################################
    def AddTitreSeance(self, doc):
        
        parag = self.AddParagraph(u"Détail des séances\n")
        self.MoveEnd()
        self.Newline()
        
        self.BeginBold()
        self.BeginFontSize(14)
        self.BeginItalic()
        self.WriteText(doc.intitule)
        self.EndItalic()
        self.EndFontSize()
        self.EndBold()
        self.BeginAlignment(wx.TEXT_ALIGNMENT_CENTRE)
        
        self.Newline()
        self.SetStyle(parag, Styles["Titre"])
        self.EndAlignment()

        
    ######################################################################################################
    def AddPhase(self, tache, typ):
        if tache.phase != '':
            r,v,b,a = ICoulTache[tache.phase]
        else:
            r,v,b, a = 1,1,1,1
        bgCoul = wx.Colour(r*255,v*255,b*255)
        
        if tache.phase != '':
            r,v,b = BCoulTache[tache.phase]
        else:
            r,v,b, a = 0,0,0,1
        fgCoul = wx.Colour(r*255,v*255,b*255)

        Styles["Titre 1"].SetBackgroundColour(bgCoul)
        Styles["Titre 1"].SetTextColour(fgCoul)  
        self.BeginStyle(Styles["Titre 1"])
        
        phase = tache.GetProjetRef().phases[tache.phase][1]
        self.WriteText(phase)
        self.EndStyle()
#        self.EndAlignment()
        
        self.Newline()
#        self.EndLeftIndent()
#        self.EndStyle()
         
    ######################################################################################################
    def AddTache(self, tache, revue = False):
        if tache.phase != '':
            r,v,b, a = ICoulTache[tache.phase]
        else:
            r,v,b, a = 1,1,1,1
        bgCoul = wx.Colour(r*255,v*255,b*255)
        
        if tache.phase != '':
            r,v,b = BCoulTache[tache.phase]
        else:
            r,v,b, a = 0,0,0,1
        fgCoul = wx.Colour(r*255,v*255,b*255)
            
        if not revue:
            Styles["Titre 2"].SetBackgroundColour(bgCoul)  
            self.BeginStyle(Styles["Titre 2"])
            self.WriteText(u"Tache : " + tache.code+"\t\t\t"+getHoraireTxt(tache.GetDuree()))
            self.EndStyle()
            self.Newline()
            self.EndAlignment()
            
            self.BeginStyle(Styles["Message"])
#            self.BeginLeftIndent(60)
            self.BeginUnderline()
            self.WriteText(u"Intitulé :")
            self.EndUnderline()
            self.WriteText(u" " + tache.intitule)
            self.EndStyle()
#            self.Newline()
        
        if tache.description != None:
#            self.BeginUnderline()
#            self.WriteText(u"Description :")
#            self.BeginLeftIndent(60)
#            self.EndUnderline()
            self.Newline()
            rtc = richtext.RichTextPanel(self.parent, tache, toolBar = False)
            rtc.Show(False)
            self.AddDescription(rtc.rtc)
            rtc.Destroy()
            self.EndStyle()

##            self.BeginLeftIndent(60)
#            self.Newline()
#            self.EndStyle()
#            self.MoveEnd()
            
#            tache.panelPropriete.rtc.rtc.SelectAll()
#            
#            if sys.platform == "win32":
#                #
#                # Procédure pour vérifier que le clipboard est disponible
#                # (source http://teachthe.net/?cat=56&paged=2)
#                #
#                cbOpened = False
#                n = 0
#                while not cbOpened and n < 10:
#                    n += 1
#                    try:
#                        win32clipboard.OpenClipboard(0)
#                        cbOpened = True
#                        win32clipboard.CloseClipboard()
#                    except Exception, err:
##                        print "error", err
#                        # If access is denied, that means that the clipboard is in use.
#                        # Keep trying until it's available.
#                        if err[0] == 5:  #Access Denied
#                            pass
#                            print 'waiting on clipboard...'
#                            # wait on clipboard because something else has it. we're waiting a
#                            # random amount of time before we try again so we don't collide again
#                            time.sleep( random.random()/50 )
#                        elif err[0] == 1418:  #doesn't have board open
#                            pass
#                        elif err[0] == 0:  #open failure
#                            pass
#                        else:
#                            print 'ERROR in Clipboard section of readcomments: %s' %err
#                            pass
#
#            tache.panelPropriete.rtc.rtc.Copy()
#            self.Paste()
            
        self.Newline()
#        self.EndLeftIndent()
        self.EndAlignment()
#        self.BeginUnderline()
#        self.WriteText(u"Volume horaire :")
#        self.EndUnderline()
#        self.WriteText(u" " + getHoraireTxt(tache.GetDuree()))
        
        self.EndStyle()
        
        
        
    def AddDescription(self, rtc):
        """ Ajoute une description contenue dans un RichTextCtrl
        """
#         print "AddDescription"
#        par = rtc.GetFocusObject()
#        par = rtc.GetSelectionAnchorObject()
        par = rtc.GetBuffer()
        pos = self.GetInsertionPoint()
#         print "   ", rtc.GetBuffer()
#         print "   ", pos
        
        self.GetBuffer().InsertParagraphsWithUndo(pos, par, self)
        
        self.MoveEnd()
#        self.Newline()
#        return
#        pos = self.GetLastPosition()
#        
#        self.
        
#        
#        
#        
#        
#        
#        
#        bufS = cStringIO.StringIO()
#        handlerS = rt.RichTextXMLHandler()
#        handlerS.SetFlags(rt.RICHTEXT_HANDLER_INCLUDE_STYLESHEET)
#        handlerS.SaveStream(rtc.GetBuffer(), bufS)
##        print "   ", bufS.getvalue()
#        domS = parseString(bufS.getvalue())
#        
#        
#        bufT  = cStringIO.StringIO()
#        handlerT = rt.RichTextXMLHandler()
#        handlerT.SetFlags(rt.RICHTEXT_HANDLER_INCLUDE_STYLESHEET)
#        handlerT.SaveStream(self.GetBuffer(), bufT)
##        print "   ", bufT.getvalue()
#        domT = parseString(bufT.getvalue())
#        
#        parS = domS.getElementsByTagName("paragraphlayout")[0]
#        parT = domT.getElementsByTagName("paragraphlayout")[0]
#        
#        for c in parS.childNodes:
##            print ">>>>   ", c.toxml()
#            parT.appendChild(domT.importNode(c, True))
##        print "    T : ", parT.toxml()
#        
#        print "resultat :"
##        print domT.toxml()
        
#        bufT  = cStringIO.StringIO()
#        bufT.write(domT.toxml())
#        bufT.seek(0)
#        
#        try:
#            for line in bufT:
#                print line,
#        finally:
#            pass
#        
#        bufT.seek(0)
##        print " >>", bufT.getvalue()
#        
##        rt_buffer = self.GetBuffer()
##        rt_buffer.AddHandler(handlerT)
#
##        handlerT.LoadStream(self.GetBuffer(),  bufT)  
#    
#        # add the handler (where you create the control)
#        self.GetBuffer().AddHandler(rt.RichTextXMLHandler())
#        
#        # you have to specify the type of data to load and the control
#        # must already have an instance of the handler to parse it
#        self.GetBuffer().LoadStream(bufT, rt.RICHTEXT_TYPE_XML)
#        bufT.close()
#        
##        self.MoveToParagraphEnd()
#        self.MoveEnd()
#        self.Newline()
#        self.MoveEnd()
#        
#        self.EndStyle()
#        self.EndLeftIndent()
#        self.EndAlignment()
#        self.Newline()
        
        
#        self.Refresh()
    
    
    ######################################################################################################
    def AddSeance(self, seance, indent = 1):
#        print "Add", seance
        if seance.typeSeance == '':
            return
        
        r,v,b = ICoulSeance[seance.typeSeance]
        bgCoul = wx.Colour(r*255,v*255,b*255)
        
#        self.Newline()
        
#        if not isinstance(fgCoul, wx.Colour):
#            fgCoul = wx.NamedColour(fgCoul)
#        self.BeginTextColour(fgCoul)
            
        if not isinstance(bgCoul, wx.Colour):
            bgCoul = wx.NamedColour(bgCoul)
        Styles["Titre 1"].SetBackgroundColour(bgCoul)
        
        self.BeginStyle(Styles["Titre 1"])
        self.WriteText(seance.GetReferentiel().seances[seance.typeSeance][0] + u" : " + seance.code+"\t\t\t"+getHoraireTxt(seance.GetDuree()))
        self.EndStyle()
#        self.BeginLeftIndent(60*(indent-1))
        self.Newline()
        self.EndLeftIndent()
        
        self.BeginStyle(Styles["Message"])
        self.BeginUnderline()
        self.WriteText(u"Intitulé :")
        self.EndUnderline()
        self.WriteText(u" " + seance.intitule)
#        self.EndStyle()
#        self.BeginLeftIndent(60*indent)
        self.Newline()
        self.EndLeftIndent()
        
        if seance.description != None and hasattr(seance, 'panelPropriete'):
#            self.BeginUnderline()
#            self.WriteText(u"Description :")
#            self.EndUnderline()
#            self.Newline()
#            self.BeginLeftIndent(60*indent)
            seance.panelPropriete.rtc.rtc.SelectAll()
            seance.panelPropriete.rtc.rtc.Copy()
            self.Paste()
            
            self.Newline()
            self.EndLeftIndent()
        
        self.EndStyle()
        
        if seance.typeSeance in ["R", "S"]:
            for sseance in seance.seances:
                self.AddSeance(sseance, indent + 1)
            self.Newline()
        
        
    
        
#    ######################################################################################################
#    # Analyse   
#    ######################################################################################################
#    def AddTitreAnImmob(self):
#        self.AddParagraphStyled(u"Structure du Montage :", "Titre 1")
#        
#    def AddAnImmob(self, analyse, zoneMtg):
#        self.AddParagraphStyled(u"Mise en position axiale :", "Titre 2")
#        
#        # Message principal
#        self.AddParagraphStyled(analyse.messageImmobilisation.mess, "Message", analyse.messageImmobilisation.coul)
#        self.AppendText("\n")
#        
#        # Message par sens
#        for s in [1,0]: # diff�rents sens ...
#            self.BeginStyle(Styles["MessSens"])
#            self.BeginTextColour(Couleur[analyse.resultatImmobilisation[s][0].coul])
#            mess = self.AppendText(analyse.resultatImmobilisation[s][0].mess)
#            if s == 1: self.WriteText("\t")
#        self.AppendText("\n")
#        
#        # Image par sens
#        for s in [1,0]: # diff�rents sens ...
#            if analyse.resultatImmobilisation[s][0].clef == 'ArretArbreSens':
#                img = self.GetImageArret(s, analyse, zoneMtg)
#            elif analyse.resultatImmobilisation[s][0].clef == 'ImmobCorrect':
#                img = self.GetImageChaine(s, analyse, zoneMtg)
#            self.WriteImage(img)
#            self.WriteText("\t")
#        self.AppendText("\n")
#            
#    def AddAnStruc(self, analyse, zoneMtg):
#        titre = self.AddParagraph(u"Sch�ma de Structure :")
#        self.SetStyle(titre, Styles["Titre 2"])
#        img = analyse.schemaStructure.bitmap().ConvertToImage()
#        self.AddImage(img)
#        self.AppendText("\n")
#        
#    ######################################################################################################
#    def AddTitreAnCharg(self):
#        self.AddParagraphStyled(u"R�sistance aux charges :", "Titre 1")
#    
#    def AddAnResistMtg(self, analyse, zoneMtg):
#        self.AddParagraphStyled(u"R�sistance axiale du montage :", "Titre 2")
#              
#        # Message principal
#        self.AddParagraphStyled(analyse.messageResistanceAxiale.mess, "Message", analyse.messageResistanceAxiale.coul)
#        self.AppendText("\n")
#        
#        # Message par sens
#        for s in [1,0]: # diff�rents sens ...
#            self.BeginStyle(Styles["MessSens"])
#            self.BeginTextColour(Couleur[analyse.resultatEffortAxialMtg[s][0].coul])
#            mess = self.AppendText(analyse.resultatEffortAxialMtg[s][0].mess)
#            if s == 1: self.WriteText("\t")
#        self.AppendText("\n")
#
#        # Image par sens
#        for s in [1,0]: # diff�rents sens ...
#            if analyse.resultatEffortAxialMtg[s][0].clef == 'ElemResistPas':
#                img = self.GetImageChaineSurbrill(s, analyse, zoneMtg)
#            elif analyse.resultatEffortAxialMtg[s][0].clef == 'ChargeAxOk':
#                img = self.GetImageChaine(s, analyse, zoneMtg)
#            elif analyse.resultatEffortAxialMtg[s][0].clef == 'ArretArbreSens':
#                img = self.GetImageArret(s, analyse, zoneMtg)
#            self.WriteImage(img)
#            if s == 1: self.WriteText("\t")
#        self.AppendText("\n")
#    
#    
#    def AddAnResistRlt(self, analyse, zoneMtg, panelResist):
#        self.AddParagraphStyled(u"R�sistance des roulements :", "Titre 2")
#        
#        # Message principal
#        self.AddParagraphStyled(analyse.messageResistanceAxiale.mess, "Message", analyse.messageResistanceAxiale.coul)
#        self.AppendText("\n")
#        
#        # Sch�ma de structure
#        img = analyse.imageSchemaCharges.ConvertToImage()
#        self.AddImage(img)
#        
#        # Tableau
#        self.AddGrid(panelResist.tableResist)
#        
#        self.AppendText("\n")
#        
#        
#    ######################################################################################################
#    def AddTitreAnMontab(self, analyse):
#        self.AddParagraphStyled(u"Montabilit� :", "Titre 1")
#        
#        self.AddParagraphStyled(analyse.resultatMontabilite.mess, "Message", analyse.resultatMontabilite.coul)
#        
#    def AddAnMontabEns(self, analyse, zoneMtg):
#        if analyse.cdcf.bagueTournante == "I": ens = u"""arbre"""
#        else: ens = u"""al�sage"""
#        self.AddParagraphStyled(u"Montabilit� de l'ensemble "+ens+" :", "Titre 2")
#        self.AppendText("")
#        
#        # Images pour "Montabilit�"
#        imagMontabiliteEns = self.GetImagesDemontageEns(analyse, zoneMtg)
#        for img in imagMontabiliteEns:
#            self.WriteImage(img)
#            self.WriteText("\t")
#        
#    def AddAnMontabRlt(self, analyse, zoneMtg):
#        self.AddParagraphStyled(u"Montabilit� des Roulements :", "Titre 2")
#        self.AppendText("")
#        
#        # Images pour "Montabilit�"
#        imagMontabiliteRlt = self.GetImagesDemontageRlt(analyse, zoneMtg)
#        for img in imagMontabiliteRlt:
#            self.WriteImage(img)
#            self.WriteText("\t")
#            
#            
#    ######################################################################################################
#    def AddAnEtanch(self, analyse, panelEtanch, CdCF):
#        self.AddParagraphStyled(u"Etanch�it� :", "Titre 1")
#        
#        #
#        # Etanch�it� statique
#        #
#        self.AddParagraphStyled(u"Etanch�it� Statique :", "Titre 2")
#        
#        # CdCF
#        self.AddCdCFEtanchStat(CdCF)
#        
#        # Resultat principal
#        message = analyse.resultatEtancheite["SB"]
#        self.AddParagraphStyled(message.mess, "Message", message.coul)
#        
#        # D�tails 
#        if "SB+" in analyse.resultatEtancheite.keys():
#            for mess in analyse.resultatEtancheite["SB+"]:
#                self.AddParagraphStyled(mess.mess, "MessSens", mess.coul)
#
#        self.AppendText("\n")
#        self.AddGrid(panelEtanch.tableStat)
#        
#        #
#        # Etanch�it� Dynamique
#        #
#        if "DB" in analyse.resultatEtancheite:
#            self.AddParagraphStyled(u"Etanch�it� Dynamique :", "Titre 2")
#            
#            # CdCF
#            self.AddCdCFEtanchDyn(CdCF)
#            
#            mess = analyse.resultatEtancheite["DB"]
#            self.AddParagraphStyled(mess.mess, "Message", mess.coul)
#            
#            if "DB+" in analyse.resultatEtancheite.keys():
#                for mess in analyse.resultatEtancheite["DB+"]:
#                    self.AddParagraphStyled(mess.mess, "MessSens", mess.coul)
#
#            self.AppendText("\n")
#            self.AddGrid(panelEtanch.tableDyn)
#        
#        #
#        # Compatibilit� lubrifiant
#        #
#        self.AddParagraphStyled(u"Compatibilit� lubrifiant :", "Titre 2")
#        
#        # CdCF
#        self.AddCdCFEtanchLub(CdCF)
#        
#        mess = analyse.resultatEtancheite["C"]
#        self.AddParagraphStyled(mess.mess, "Message", mess.coul)
#        
#        self.AppendText("\n")
#                    
#                    
#                    
#    ######################################################################################################
#    def AddAnCout(self, analyse, panelDevis, CdCF):
#        self.AddParagraphStyled(u"Devis (co�t indicatif) :", "Titre 1")
#        
#        # CdCF
#        self.AddCdCFCoutMax(CdCF)
#        
#        # Devis
#        self.AppendText("\n")
#        self.AddGrid(panelDevis.devis)
#
#
#    def AddGrid(self, grid):
#        
#        debut = self.GetInsertionPoint()
#    
#        def SsRc(s):
#            return s.replace("\n", " ")
#
#        # Définition des tabs
#        coef = 5
#        tabs = [max(coef*grid.GetRowLabelSize(), 30)]
#        for c in range(grid.GetNumberCols()):
#            tabs.append(tabs[-1:][0]+coef*grid.GetColSize(c))
#        Styles["Tableau"].SetTabs(tabs)
#        
#        # Affichage du contenu
#        for l in range(1+grid.GetNumberRows()):
#            ll = l-1
#            for c in range(1+grid.GetNumberCols()):
#                # Titres colonnes
#                cc = c-1
#                if l == 0 and c > 0:
#                     self.BeginTextColour(wx.BLACK)
#                     self.AppendText(SsRc(grid.GetColLabelValue(cc)))
#                     
#                # Titres lignes
#                elif c == 0 and l > 0:
#                    self.BeginTextColour(wx.BLACK)
#                    self.AppendText(SsRc(grid.GetRowLabelValue(ll)))
#                
#                elif c == 0 and l == 0:
#                    pass
#                
#                # Valeurs
#                else:
#                    self.BeginTextColour(grid.GetCellTextColour(ll,cc))
#                    self.AppendText(SsRc(grid.GetCellValue(ll,cc)))
#                
#                self.AppendText("\t")
#            self.AppendText("\n")
#            
#        fin = self.GetInsertionPoint()
#        tout = self.GetRange(debut, fin)
#        
#        self.SetStyle((debut, fin), Styles["Tableau"])
#        
#        self.EndTextColour()
        
    def AddParagraphStyled(self, texte, style, couleur = None, bgCoul = "WHITE", souligne = False):
        
#        if style == "MessSens":
#            print  Styles[style].GetTextColour(), texte.encode('cp437','replace')
        
        if couleur is not None:
            if isinstance(couleur, wx.Colour):
                c = couleur
            else:
                c = wx.Colour(0,0,0)#Couleur[couleur]
#            cs = Styles[style].GetTextColour()
#            Styles[style].SetTextColour(c)
            self.BeginTextColour(c)
            
        if not isinstance(bgCoul, wx.Colour):
            bgCoul = wx.NamedColour(bgCoul)
                
        if souligne:
            self.BeginUnderline()
#        Styles[style].SetFlags(wx.TEXT_ATTR_BACKGROUND_COLOUR)
        Styles[style].SetBackgroundColour(bgCoul)
        parag = self.AddParagraph(texte)
        self.SetStyle(parag, Styles[style])
        
        self.EndTextColour()
        self.EndUnderline()
        self.EndParagraphStyle()
        
    def AddTextStyled(self, texte, style, 
                      fgCoul = "BLACK", bgCoul = "WHITE", souligne = False):
        
#        if style == "MessSens":
#            print  Styles[style].GetTextColour(), texte.encode('cp437','replace')
        
        if not isinstance(fgCoul, wx.Colour):
            fgCoul = wx.NamedColour(fgCoul)
        self.BeginTextColour(fgCoul)
            
        if not isinstance(bgCoul, wx.Colour):
            bgCoul = wx.NamedColour(bgCoul)
        Styles[style].SetBackgroundColour(bgCoul)     
                
        if souligne:
            self.BeginUnderline()
        
        self.BeginStyle(Styles[style])
        
        self.AppendText(texte)
        
        self.EndStyle()
        self.EndUnderline()
        self.EndTextColour()
        
        
#        if couleur is not None:
#            Styles[style].SetTextColour(cs)
    
    ######################################################################################################
    def getNomFichierDefaut(self):
        f = u"Tâches détaillées _ " + self.eleve.GetNomPrenom() + u".rtf"
        return os.path.join(self.projet.GetPath(), f)
    
    ######################################################################################################
    def Enregistrer(self, titre, nomFichierDefaut = u""): 
        if not self.GetFilename():
            if self.Ecraser(nomFichierDefaut):
                self.SetFilename(nomFichierDefaut)
                self.SaveFile()
            else:
                return
        else:
            self.SaveFile()
           
        if nomFichierDefaut:
            ext = os.path.splitext(nomFichierDefaut)[1].lstrip('.')
            if ext == 'txt':
                wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=True)
                fileType = 1
                ext = rt.RichTextBuffer.FindHandlerByType(fileType).GetExtension()
                if not nomFichierDefaut.endswith(ext):
                    nomFichierDefaut += '.' + ext
                self.SaveFile(nomFichierDefaut, 1)
                
            elif ext == 'html':
                handler = rt.RichTextHTMLHandler()
                handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
                handler.SetFontSizeMapping([7,9,11,12,14,22,100])
                stream = cStringIO.StringIO()
                if handler.SaveStream(self.GetBuffer(), stream):
                    f = open(nomFichierDefaut, 'w')
                    f.write(prefixeHTML+stream.getvalue())#.encode(sys.getdefaultencoding()))
                    f.close()
                    
            elif ext == 'rtf':
                import PyRTFParser
                # Use the custom RTF Handler
                handler = PyRTFParser.PyRichTextRTFHandler()
                # Save the file with the custom RTF Handler.
                # The custom RTF Handler can take either a wxRichTextCtrl or a wxRichTextBuffer argument.
                handler.SaveFile(self.GetBuffer(), nomFichierDefaut)
        

        dlg = wx.MessageDialog(self, u"Le fichier a bien été enregistré\n\n%s\n\n"\
                                   u"Voulez-vous l'ouvrir ?" %self.GetFilename(), 
                                   u"Fichier enregistré",
                                   wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL)
        res = dlg.ShowModal()
        if res == wx.ID_YES:
            try:
                os.startfile(self.GetFilename())
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'ouvrir le fichier\n\n%s\n" %toSystemEncoding(self.GetFilename()))
        dlg.Destroy()



    ######################################################################################################
    def Ecraser(self, nomFichier):
        if os.path.exists(nomFichier):
            dlg = wx.MessageDialog(self, u"Le fichier existe déja !\n\n%s\n\n"\
                                   u"Voulez-vous l'écraser ?" %nomFichier, 
                                   u"Fichier existant",
                                   wx.ICON_WARNING | wx.YES_NO | wx.CANCEL)
            res = dlg.ShowModal()
            dlg.Destroy()
            return res == wx.ID_YES
        return True
        
        
        
        
    ######################################################################################################
    def EnregistrerSous(self, titre, nomFichierDefaut = u""):
        wildcard =  u"Rich Text Format (.rtf)|*.rtf|" \
                    u"Format HTML (.html)|*.html|" \
                    u"Fichier texte (.txt)|*.txt"
        types = [0, 3, 2]
        dlg = wx.FileDialog(self, titre,
                            wildcard=wildcard,
                            defaultFile = nomFichierDefaut,
                            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

            self.Enregistrer(titre, path)

        dlg.Destroy()
        
        
        
        
        
        
        
        
class RTPrinting(rt.RichTextPrinting):
    def __init__(self, parent):
        rt.RichTextPrinting.__init__(self, "", parent)
        
        self.SetTitle(u"Tâches")

        printData = wx.PrintData()
        printData.SetPaperId(wx.PAPER_A4)
        printData.SetPrintMode(wx.PRINT_MODE_PRINTER)
        printData.SetQuality(wx.PRINT_QUALITY_HIGH)
        self.SetPrintData(printData)
        
        pageSetupData = self.GetPageSetupData()
        pageSetupData.SetMarginBottomRight(wx.Point(10,10))
        pageSetupData.SetMarginTopLeft(wx.Point(10,10))


prefixeHTML = u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
"""


        
        
#----------------------------------------------------------------------
_rt_save = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAQ1J"
    "REFUKJFjjE/L/c9AJlg0ZxojCwMDA8Oee78YvOzNGGbVJBHUFFc7hWHfiSsMLkpsDAwMDAws"
    "DAwMDPE+rgyvP39kYGBgYNi7bz9Ozc5Ojgww9U+vHUQYgE0RsQDDAGJcgNcAsl0gysvPEFc7"
    "haAGWRFJ3C5AlyTJBTCw7fxVvBq8DLVxG7Dt/FWG0kBLOF+In5eBn5eHgYeXl4Gfl49BTlKQ"
    "wTChCcUQDBcwMDAwlE1Zy6CppsrAwMDA0JTkjtdFTHhlGRgYfv3+x8D89wfD7z9/yDOA+d93"
    "hq9/WBh+/f2LVR7DC3KifAwrGhMZhKXkGTQVJAiZz8DIyMTMEJeSRXKOXDRnGiMDAwMDALeo"
    "P7cp9rvcAAAAAElFTkSuQmCC")


#----------------------------------------------------------------------
_rt_undo = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAhVJ"
    "REFUKJGNkstrE1EYxX8zmcSZZDJp2rSNfSg22CANYhYijWjAjcviwkVxW2hBVyZ/gZu6aOtK"
    "aLC7dicqwcdGiIrUoCIhpUVDsPZhq4GENqE2aUu5LuqkLxv94Fvce885995zPkmSLRxVffce"
    "ikQ6W123N7i41XOR65fPSeaeFH3wTAz390h7ib2D4+J9ZhGXajskWqxscq27C5MjP0nOEInF"
    "hQkIDgyJpeUCvjoVjyrjtCoAOK0KHlXGV6eSSGUZefxaACgu1cbH6W/0Do6LL/M5WjQNpyqz"
    "tb3NbKnClaCPwMlmpudzJFJZ/G4Hhm2b+OQMAApAp8fOykoRv9uBrlpYq+yQU6NRKbXn+ZFY"
    "XCzNLeN22Jj9UdoV0FU7umoHYK2yTmblF6nR6D5fAFobXRR/5tBVO07r+o6A06pgGM59QMOx"
    "9ddU4pMzhDu8ICtAHgAZwDhmrXZbYz3hDi/BgSFxUMBjkzA0jbXNMucDp3YEJJsVQ9cwdI1S"
    "uczCaoFsLl+N0ySHI/fF1eAZDF3j00KhGqOyWCgy8TZNa0sDXSeauNTuqw6KaWD37Zi4caGT"
    "ekPnXeYrp9uaePPnTKo1iSb5ZjjA8WY333N5JpKfeXm3f9dgSbYc2aHomHj6Ki2mMnPiUWJK"
    "hKJj4iBGrnV7yO/lrL+dfHGD4RcfSI70H4q25hdME0vlDZ7f6TtE/i8P/lW/AfYJsF99ZciZ"
    "AAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
_rt_redo = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAg5J"
    "REFUKJGdkr9rU1EcxT/3vbz2vfS924qRpmopVmIsFCWDiFkCAXHs5CDoJqSrJIP+BS5tXCw0"
    "EHDo4FBUguDgULVQImJJLe0Qu2hqWyKNMT9q0p/XofRHmtrBA9/l3HPPPffcK4Sms4fxyRn1"
    "NDXFYqG0z4Wv+kg+uC34B8SeQTSRUq/S87SbLU2iUn2D6/5unj+612AUTaSUEJpO/OV7Nfb2"
    "Mx5TA2B9W6OyuYVjuGjVdxq4zGhMHD5QCE0nFB1RHl1h6DrZ4hrhgI/+nk7mvueZyCzQK00M"
    "XadS32G5VuNyTydLywUqm1u4AMprNXxdkmp9m3DAx3BkoPHOg0PKf6qNrg4Dx9TYKJa45HEz"
    "vVJGA3AMF7bpxjZ1zp1pb+ogMxoT2eIaAN4Oh+7THdimG2A3AYCUDtK2SE3NH9u2bLOwTTdS"
    "OvucY6zuGlzrv0C1XuOsI/G0NL9YYHBIhXq9SMtqWtMAhiMDYjpXQNoWtwJ9hKIjak9w5/GY"
    "AljIr5L7XaBcqyFtC2lbiBbj4B/cfzKupLZN0H+RX+Uqzz5+JR2PNMQZn5xR2cU887mfLC0X"
    "+FH5c2AAcPNhQt290cf5Tg8r+SIjH+aaTJogNL1hgrGkejExq2az39Trd19UMJZURzWHRztq"
    "mI5HxPCbT6yW1rni7ybo954YwHUcmY5HRNxOKmm1nrgZaOzgf/AXUUy2DjrCDG0AAAAASUVO"
    "RK5CYII=")

#----------------------------------------------------------------------
_rt_copy = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAATlJ"
    "REFUKJGFk71OwzAURo/tpE2AdihiAAmQWNiKWICpDIhnQEi8A0+ASsXAzDsgIcTEA3QANsZu"
    "XTMQBiqkUkFF04aB2sRJSO90bV+f+33+EUIqzq7bMam471UA6JzuiPRaMqROltc2KS9tMFhY"
    "JVArAJw31qlfPWfguYCqp6j5Lou+S81XpmAWRGgLe1t13r8i+sMxYdAtasrFyYGx5eik4v11"
    "DYHW8T6dl0/6w4i3wYjXjxFh0KV51ADasYYYQNUzKXlQDQYsiNnluzLJA6CsBKQgrdtHa2x2"
    "zJdkeoq5koLvsYEc7m5bdqxqRwk8V5C4GFwlDCRKKdR2Egq01IkpUhJgCsmKtkdKJiHTOSFA"
    "xoWQ7NFbgF8F+ZAU4PLuKbMopYBJXAhxwH5ZgPW5ZkH+tdC8eShyZ+IHUNNZHhrzal0AAAAA"
    "SUVORK5CYII=")

#----------------------------------------------------------------------
_rt_alignleft = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEJJ"
    "REFUOI1jZGRiZqAEMFGkm4GBgYWBgYHBx9vrPzmat2zdxshIqRdIcsGWrdsY0cXo6wJsLhoN"
    "g2ERBhRnJooNAACQdhhQZbXeGAAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_alignright = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAADxJ"
    "REFUOI1jZGRiZqAEMFGkm4GBgYWBgYHBx9vrPzmat2zdxshIqRdYsAkS6yLquWA0DEZ8GFCc"
    "mSg2AADQZxhQFG0xxgAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_bold = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEtJ"
    "REFUOI3NUkEKACAMyq3//7jWNQwWY0HzKNOJCIi2DCSlfmHQmbA5zBNAFG4CPoAodo4fFOyA"
    "wZGvHTDqdwCecnQHh0EU/ztIGyy1dBRJuH/9MwAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_centre = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEJJ"
    "REFUOI1jZGRiZqAEMFGkm4GBgYWBgYHBx9vrPzmat2zdxshIqRdYkDnEumTL1m2MMDZ1XDAa"
    "BiM+DCjOTBQbAAAwdhhQDziCqAAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_colour = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAPZJ"
    "REFUOI1jZGRiZqAEsOCS+Mcu9h+bONPPV4wofEKa37Lz4zWYEd0LuGzG5RKsLiAFDEIDllTz"
    "MWxtyGJ4yiWKofgfCyTSkGMCJRDd/hr/Z2BgYGCZ5cAg8v0jg++C9wy6zx8ysP37zfCYXYFh"
    "g1gww+VfUSiGwg2AaRZ/JcPw6v0fhv/qLxg4vv1jCOv5zPBvZgrDSukghp8/ZRkY/rFiGgDT"
    "jBV84mX4572WgekzL8O/v5hBxoRXMwMDw/+3QgwM/3CHNeFY+MvMwMDyE6vtRBnAKPqWgUH2"
    "OQUu4P/IwGh8HrcFBAORgYFhF/NZRhetP1jVAACsCFJPHjA77wAAAABJRU5ErkJggg==")


#----------------------------------------------------------------------
_rt_cut = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAbBJ"
    "REFUKJGdk0FLG1EQx3/vpRdv7sG49CKYxvSmVDwkpd78ALbSShQkbU81guAH8BN4EE0KGlCQ"
    "5iAIoiaIwWAP3bi0WXZLW1q2WfGmJ8mhV19Pu+xqWsSBx/Bm/vObmQcPIWP4Jz83r96vb6pw"
    "LJxzXfdWThKyuJR8/2rjOI4Kxz8ZDQUwkHosuGERwOLKsohLydpaKSIqfyjfrOsM8C2VSlKr"
    "1RRAtVJRAK8mJ+8GWFxZFldui93dPTzvTFWqhwCMPnt6a3yAB52CWjLBSCLBwcH+P0f/7wpX"
    "bouLywvys+/uB9CSCfRendVCkezMm/tN8PnwiKHBQX59axKXHWUACCFjAHyp15VX2gIgbdg0"
    "MkO8LG+I7WxO+XeARwt5ngwPBw8q/eLe1wtI75y25QTCsG9bDtI7p+fFW6xmU0UAXmkLU9eY"
    "OK0LNf0cIOji+4ezOSZO68LUNX4vrUbfIG3YXPf3AdD9o4Wpa5E9TV3jT8MC4Lq/j7RhRwGm"
    "rtG2HPx9u6bGI4CuqXHShs12NqfalhNtIGSMn8cnaiczpnYyY6paKHb8jdVCMdA0Tz4Gmr9P"
    "zKg0oZ3GfwAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_font = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAIpJ"
    "REFUOI21k8ENgCAMRSmMpwzAgenUsgDMhweCgUpRJDYhJG362v8DAFKJmZBT3W8A67LFz4Bj"
    "T835HgY4V99DADqV24IF5Kk+WOht0QTkabm5twW03kHPeQoVIFV1EDFqjZHmtU55xLp2k8Bp"
    "NaZdrwCcdhqlF5cHVHcJ4TzxwULTxJH4/zM9xQmi7UCACkKFWgAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_idea = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAVtJ"
    "REFUWIXtl2FOwkAQhd8u3gAJp1EXuQEBrmOU24DxBtoWjmA8BAlXsOsPXNjadjtvRImJ708T"
    "pnS+fTudnRpjezinLjR/Wq5K//W3+cwazbMM40BIPJ3c1GKPT4UKRASQShxruyuwWYMC6QRY"
    "rkpfTZwBGCUhAGCzlkFYCeUxcTW5Ma521/Ay7RIFcFx9VouF5E0QAHB13VysFEBd7dbHYlxo"
    "BUitXgohcYFwQLZ6VoJGpE+834oieQ9ZA5zCK3kWAEnyJMB8Zk1or1pJmpHaAe/zylUrRSvu"
    "VjgTJK1YdRwD1Q4YuyDd+6DOLWBqgT2IAGIekGwFY30QVYQpJ+JZgJEYILUqzSASRBXh2+sd"
    "Bn3XGBv0gTzPASyYR/JvwT7J6UQDOOdaYxq4fwcogPuHhQHQOuF8xilRHyaxspfnA8jodqz6"
    "KvoWgC/fDwDG9n4f4FT60ZHsTwB8AA6FjDfFEDh8AAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
_rt_indentless = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAHRJ"
    "REFUOI3Nkm8KgCAMxfe2TlftCJ0u6ATa9eyTIqZiKdEDYfj25+eQwEKlo6qu5oOFABbq0eSD"
    "dZldbBh7Ir3LaSTB7ozdEJstBOyL3xJA9bgVpyTVBmAJBK1PMPYMefx0YpagR7/6B2WCeGnD"
    "CbhmfrKDC/GuLg9MR0atAAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
_rt_indentmore = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAHlJ"
    "REFUOI3NkmEKgCAMhbfZ6aododMJncB5PftlTE2TkuiBID7f9jkEJAO1xcyh5SMZQCQDbzTF"
    "zbrMQRtOPOZnVxpJYIOTDbXZQ0BpwN4GciHzXoRykmaBOIPYXYdrT3DizzuUGv2dC4Kn+tU/"
    "qBPooQ0noJb5yQwOwa4uD/KzgEcAAAAASUVORK5CYII=")

#----------------------------------------------------------------------
_rt_italic = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAGdJ"
    "REFUOI3Vk1EOgDAIQwt4/2P0lopfS6YOgsEfl+xntK8kMBE1dI623F8Atqzox+73N1GTcgez"
    "mOTDPEThJekAHIBHmhQwzCTfAyrpKaCSHgKq6SGgmi5qkHmVV3Nfzf5S+/9faANOrocplI0e"
    "xSoAAAAASUVORK5CYII=")


#----------------------------------------------------------------------
_rt_paste = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAXNJ"
    "REFUKJGFkzsvREEYhp/vzDnWWHuxdnsJjd+wRKPYgkIUKqHVKtYlQoi4FX6BiGQTolEpFBIU"
    "/gUJtbXWdSMuo1jGHueceJvJN5nvmff9JiPiKH6UL5YMITrfGJWwfQARR5EvlsxY8pqr6gvL"
    "60u+A3NT8wCcOd2hICdfLJmT/k+AQPPPXke6hcP241CHbmOxtboW5TRS0jO9a06HM5j7MgAf"
    "lRsAzE2N15cLBm77A02NURxLSmUBUJlcvc5pYi1dAGxODDI7WgDgaHHEF8UBkERbJAQgrV2y"
    "rZ510AixM5BEG+bxDkllMfdlVCZn46T071MXFvZ9cVwAiScxzw+hEIAm5ZDSsD05RLX2Tvnp"
    "jZXS0S8AnUAgFALQ7AlQh/yVHSI6gcSTNo5vJiI0e/LtRJHWrh8gno6EAHhKLCTepHwzqaNi"
    "McRVmNpTIA5U6J3ZC3r3AZz6IroV3j8wYCFn4532cN/OZeA/uAC98weRN/ynL78NdulpYuMM"
    "AAAAAElFTkSuQmCC")



#----------------------------------------------------------------------
_rt_sample = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAMNJ"
    "REFUWIXtl0sawiAMhGcoN2mvqIeoV6RHUVwoC5VqiOkXFsyahJ+8ADJM8FRw3X0A9AAQfy3I"
    "t2vWOGaYaAIAAPN8atp82y7ite4pEAOktCKl1Q/gKLkDiIpQovfCk3aPGQAA5MaGJYGo7XMr"
    "RQD4RiCaJi8q3mSWHRVhSSDr5MtyPgTAPQJEOftOBFpq4OlIbElKbsOaIT5vO203uafAHcB0"
    "Ej7UNjk6isBO/7dI48IsBdI3YBXg/7PrxfE1GwDeAHen2yjnZJXsxQAAAABJRU5ErkJggg==")


#----------------------------------------------------------------------
_rt_underline = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAFdJ"
    "REFUOI1jZGRiZqAEMFGkmxoGsKAL/P/39z8yn5GJmRGbGE4XIEvC2NjEcBpAKhg1gIABS5cs"
    "/o9MYwOMuJIyetwzMGBGIV4DiAUEUyI2gJKwBjw3AgDOdhYrghF5ggAAAABJRU5ErkJggg==")



