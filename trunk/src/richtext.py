#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sequence.py
Aide à la réalisation de fiches p�dagogiques de séquence
*************
*   STIDD   *
*************
Copyright (C) 2011  
@author: Cedrick FAURY

"""

import wx
import wx.richtext as rt
from wx.lib.embeddedimage import PyEmbeddedImage
import os
import cStringIO
from constantes import xmlVide

typesImg = {".bmp" : wx.BITMAP_TYPE_BMP, 
            ".gif" : wx.BITMAP_TYPE_GIF,
            ".jpg" : wx.BITMAP_TYPE_JPEG,
            ".jpeg" : wx.BITMAP_TYPE_JPEG,
            ".png" : wx.BITMAP_TYPE_PNG,
            ".pcx" : wx.BITMAP_TYPE_PCX,
            ".pnm" : wx.BITMAP_TYPE_PNM ,
            ".tif" : wx.BITMAP_TYPE_TIF ,  
            ".tiff" : wx.BITMAP_TYPE_TIF , 
            ".tga" : wx.BITMAP_TYPE_TGA , 
            ".xpm" : wx.BITMAP_TYPE_XPM,
            ".ico" : wx.BITMAP_TYPE_ICO}


class RichTextPanel(wx.Panel):
    def __init__(self, parent, objet, size = wx.DefaultSize):
        wx.Panel.__init__(self, parent, -1, style = wx.BORDER_SUNKEN)
        
        self.objet = objet
        
        self.rtc = rt.RichTextCtrl(self, size = size, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.rtc, 1, flag = wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.Ouvrir()
        self.rtc.Bind(wx.EVT_KILL_FOCUS, self.Sauver)
        
    def Ouvrir(self):
        """ Rempli la zone de texte avec le contenu de objet.description
        """
        out = cStringIO.StringIO()
        handler = rt.RichTextXMLHandler()
        buff = self.rtc.GetBuffer()
        buff.AddHandler(handler)
        if self.objet.description == None:
            out.write(xmlVide)
        else:
            out.write(self.objet.description)
        out.seek(0)
        handler.LoadStream(buff, out)
        self.rtc.Refresh()
        
    def Sauver(self, evt = None):
        if self.rtc.GetValue() == "":
            self.objet.SetDescription(None)
        else:
            handler = rt.RichTextXMLHandler()
            handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
            stream = cStringIO.StringIO()
            if not handler.SaveStream(self.rtc.GetBuffer(), stream):
                return
            self.objet.SetDescription(stream.getvalue())
        if evt != None:
            evt.Skip()
        
    def InsertImage(self):
        wildcard= "Fichier image (bmp, gif, jpeg, png, tiff, tga, pnm, pcx, ico, xpm)|(*.bmp; *.gif; *.jpg; *.jpeg; *.png; *.tif; *.tiff; *.tga; *.xpm ; *.ico ; *.pcx ; *.pnm)"
        dlg = wx.FileDialog(self, u"Choisir un fichier image",
                            wildcard=wildcard,
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path:
                ext = os.path.splitext(path)[1]
                if ext in typesImg.keys():
                    img = wx.Image(path) 
                    self.rtc.WriteImage(img)#, typesImg[ext])
        dlg.Destroy()
        
    def ApplyBoldToSelection(self):
        self.rtc.ApplyBoldToSelection()
        
    def ApplyItalicToSelection(self): 
        self.rtc.ApplyItalicToSelection()
        
    def ApplyUnderlineToSelection(self):
        self.rtc.ApplyUnderlineToSelection()
        
    def ApplyAlignmentLeftToSelection(self):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)
        
    def ApplyAlignmentRightToSelection(self,):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)
        
    def ApplyAlignmentCenterToSelection(self):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_CENTRE)
        
        
    def IndentMore(self):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetLeftIndent(attr.GetLeftIndent() + 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)
       
        
    def IndentLess(self):
        attr = wx.TextAttr()
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
            
    def ParagraphSpacingMore(self):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() + 20);
            attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
            self.rtc.SetStyle(r, attr)

        
    def ParagraphSpacingLess(self):
        attr = wx.TextAttr()
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
        
    def LineSpacingSingle(self): 
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(10)
            self.rtc.SetStyle(r, attr)
 
                
    def LineSpacingHalf(self):
        attr = wx.TextAttr()
        attr.SetFlags(wx)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(15)
            self.rtc.SetStyle(r, attr)

        
    def LineSpacingDouble(self):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(20)
            self.rtc.SetStyle(r, attr)
            
    def Font(self):
        if not self.rtc.HasSelection():
            return

        r = self.rtc.GetSelectionRange()
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        attr = wx.TextAttr()
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


    def Colour(self):
        colourData = wx.ColourData()
        attr = wx.TextAttr()
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
            
            
            
############################################################################################################            
class RichTextFrame(wx.Frame):
    def __init__(self, titre, objet):
        wx.Frame.__init__(self, None, -1, titre,
                                     size = (700, 500),
                                     style = wx.DEFAULT_FRAME_STYLE)

        self.objet = objet
        
        self.MakeMenuBar()
        self.MakeToolBar()
        self.CreateStatusBar()
        self.SetStatusText(u"Saisir le texte descriptif")

        self.rtp = RichTextPanel(self, objet)
        wx.CallAfter(self.rtp.rtc.SetFocus)
        
#        self.EcrireHTML()

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
    def OnClose(self, evt):
        self.rtp.Sauver()
        if hasattr(self.objet, 'panelPropriete'):
            self.objet.panelPropriete.rtc.Ouvrir()
            self.objet.panelPropriete.edition = False
        evt.Skip()
        
    def OnURL(self, evt):
        wx.MessageBox(evt.GetString(), "URL Clicked")
        
    def OnImage(self, evt):
        self.rtp.InsertImage()
        

    def OnFileOpen(self, evt):
        # This gives us a string suitable for the file dialog based on
        # the file handlers that are loaded
        wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=False)
        dlg = wx.FileDialog(self, "Choose a filename",
                            wildcard=wildcard,
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path:
                fileType = types[dlg.GetFilterIndex()]
                self.rtp.rtc.LoadFile(path, fileType)
        dlg.Destroy()

        
    def OnFileSave(self, evt):
        if not self.rtp.rtc.GetFilename():
            self.OnFileSaveAs(evt)
            return
        self.rtp.rtc.SaveFile()

        
    def OnFileSaveAs(self, evt):
        wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=True)

        dlg = wx.FileDialog(self, "Choose a filename",
                            wildcard=wildcard,
                            style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path:
                fileType = types[dlg.GetFilterIndex()]
                ext = rt.RichTextBuffer.FindHandlerByType(fileType).GetExtension()
                if not path.endswith(ext):
                    path += '.' + ext
                self.rtp.rtc.SaveFile(path, fileType)
        dlg.Destroy()
        
        
        
    def Ouvrir(self):
        self.rtp.Ouvrir()

                
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
    
    def OnFileExit(self, evt):
        self.Close(True)

    def OnBold(self, evt):
        self.rtp.ApplyBoldToSelection()
        
    def OnItalic(self, evt): 
        self.rtp.ApplyItalicToSelection()
        
    def OnUnderline(self, evt):
        self.rtp.ApplyUnderlineToSelection()
        
    def OnAlignLeft(self, evt):
        self.rtp.ApplyAlignmentLeftToSelection()
        
    def OnAlignRight(self, evt):
        self.rtp.ApplyAlignmentRightToSelection()
        
    def OnAlignCenter(self, evt):
        self.rtp.ApplyAlignmentCenterToSelection()
        
    def OnIndentMore(self, evt):
        self.rtp.IndentMore()
       
    def OnIndentLess(self, evt):
        self.rtp.IndentLess()
        
    def OnParagraphSpacingMore(self, evt):
        self.rtp.ParagraphSpacingMore()
        
    def OnParagraphSpacingLess(self, evt):
        self.rtp.ParagraphSpacingLess()

    def OnLineSpacingSingle(self, evt): 
        self.rtp.LineSpacingSingle()
 
    def OnLineSpacingHalf(self, evt):
        self.rtp.LineSpacingHalf()
        
    def OnLineSpacingDouble(self, evt):
        self.rtp.LineSpacingDouble()

    def OnFont(self, evt):
        self.rtp.Font()
        
    def OnColour(self, evt):
        self.rtp.Colour()
        
    def OnUpdateBold(self, evt):
        evt.Check(self.rtp.rtc.IsSelectionBold())
    
    def OnUpdateItalic(self, evt): 
        evt.Check(self.rtp.rtc.IsSelectionItalics())
    
    def OnUpdateUnderline(self, evt): 
        evt.Check(self.rtp.rtc.IsSelectionUnderlined())
    
    def OnUpdateAlignLeft(self, evt):
        evt.Check(self.rtp.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_LEFT))
        
    def OnUpdateAlignCenter(self, evt):
        evt.Check(self.rtp.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_CENTRE))
        
    def OnUpdateAlignRight(self, evt):
        evt.Check(self.rtp.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_RIGHT))

    
    def ForwardEvent(self, evt):
        # The RichTextCtrl can handle menu and update events for undo,
        # redo, cut, copy, paste, delete, and select all, so just
        # forward the event to it.
        self.rtp.rtc.ProcessEvent(evt)


    def MakeMenuBar(self):
        def doBind(item, handler, updateUI=None):
            self.Bind(wx.EVT_MENU, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)
            
        fileMenu = wx.Menu()
        doBind( fileMenu.Append(-1, u"&Ouvrir\tCtrl+O", u"Ouvrir un fichier"),
                self.OnFileOpen )
#        doBind( fileMenu.Append(-1, u"&Enregistrer\tCtrl+S", u"Enregistrer le fichier"),
#                self.OnFileSave )
#        doBind( fileMenu.Append(-1, u"&Enregistrer sous...\tF12", u"Enregistrer dans un nouveau fichier"),
#                self.OnFileSaveAs )
        fileMenu.AppendSeparator()
        doBind( fileMenu.Append(-1, "&Visualiser en HTML", u"Visualiser en HTML"),
                self.OnFileViewHTML)
        fileMenu.AppendSeparator()
        doBind( fileMenu.Append(-1, "&Quitter\tCtrl+Q", "Fermer la fenêtre"),
                self.OnFileExit )
        
        editMenu = wx.Menu()
        doBind( editMenu.Append(wx.ID_UNDO, u"&Annuler\tCtrl+Z"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_REDO, u"&Rétablir\tCtrl+Y"),
                self.ForwardEvent, self.ForwardEvent )
        editMenu.AppendSeparator()
        doBind( editMenu.Append(wx.ID_CUT, u"Couper\tCtrl+X"),
                self.ForwardEvent, self.ForwardEvent )
        doBind( editMenu.Append(wx.ID_COPY, u"&Copier\tCtrl+C"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_PASTE, u"&Coller\tCtrl+V"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_CLEAR, u"&Effacer\tDel"),
                self.ForwardEvent, self.ForwardEvent)
        editMenu.AppendSeparator()
        doBind( editMenu.Append(wx.ID_SELECTALL, u"Selectionner tout\tCtrl+A"),
                self.ForwardEvent, self.ForwardEvent )
        
        #doBind( editMenu.AppendSeparator(),  )
        #doBind( editMenu.Append(-1, "&Find...\tCtrl+F"),  )
        #doBind( editMenu.Append(-1, "&Replace...\tCtrl+R"),  )

        formatMenu = wx.Menu()
        doBind( formatMenu.AppendCheckItem(-1, u"&Gras\tCtrl+B"),
                self.OnBold, self.OnUpdateBold)
        doBind( formatMenu.AppendCheckItem(-1, u"&Italique\tCtrl+I"),
                self.OnItalic, self.OnUpdateItalic)
        doBind( formatMenu.AppendCheckItem(-1, u"&Souligné\tCtrl+U"),
                self.OnUnderline, self.OnUpdateUnderline)
        formatMenu.AppendSeparator()
        doBind( formatMenu.AppendCheckItem(-1, u"Aligner à gauche"),
                self.OnAlignLeft, self.OnUpdateAlignLeft)
        doBind( formatMenu.AppendCheckItem(-1, u"&Centrer"),
                self.OnAlignCenter, self.OnUpdateAlignCenter)
        doBind( formatMenu.AppendCheckItem(-1, u"Aligner à droite"),
                self.OnAlignRight, self.OnUpdateAlignRight)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, u"Augmenter le retrait"), self.OnIndentMore)
        doBind( formatMenu.Append(-1, u"Diminuer le retrait"), self.OnIndentLess)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, u"Augmenter l'espacement des paragraphes"), self.OnParagraphSpacingMore)
        doBind( formatMenu.Append(-1, u"Diminuer l'espacement des paragraphes"), self.OnParagraphSpacingLess)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, u"Interligne normal"), self.OnLineSpacingSingle)
        doBind( formatMenu.Append(-1, u"Interligne de 1.5"), self.OnLineSpacingHalf)
        doBind( formatMenu.Append(-1, u"Interligne double"), self.OnLineSpacingDouble)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, u"&Police..."), self.OnFont)
        
        mb = wx.MenuBar()
        mb.Append(fileMenu, u"&Fichier")
        mb.Append(editMenu, u"&Edition")
        mb.Append(formatMenu, u"F&ormat")
        self.SetMenuBar(mb)


    def MakeToolBar(self):
        def doBind(item, handler, updateUI=None):
            self.Bind(wx.EVT_TOOL, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)
        
        tbar = self.CreateToolBar()
        doBind( tbar.AddTool(-1, _rt_open.GetBitmap(),
                            shortHelpString=u"Ouvrir"), self.OnFileOpen)
#        doBind( tbar.AddTool(-1, _rt_save.GetBitmap(),
#                            shortHelpString=u"Enregistrer"), self.OnFileSave)
        tbar.AddSeparator()
        doBind( tbar.AddTool(wx.ID_CUT, _rt_cut.GetBitmap(),
                            shortHelpString=u"Couper"), self.ForwardEvent, self.ForwardEvent)
        doBind( tbar.AddTool(wx.ID_COPY, _rt_copy.GetBitmap(),
                            shortHelpString=u"Copier"), self.ForwardEvent, self.ForwardEvent)
        doBind( tbar.AddTool(wx.ID_PASTE, _rt_paste.GetBitmap(),
                            shortHelpString=u"Coller"), self.ForwardEvent, self.ForwardEvent)
        tbar.AddSeparator()
        doBind( tbar.AddTool(wx.ID_UNDO, _rt_undo.GetBitmap(),
                            shortHelpString=u"Annuler"), self.ForwardEvent, self.ForwardEvent)
        doBind( tbar.AddTool(wx.ID_REDO, _rt_redo.GetBitmap(),
                            shortHelpString=u"Rétablir"), self.ForwardEvent, self.ForwardEvent)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, _rt_bold.GetBitmap(), isToggle=True,
                            shortHelpString=u"Gras"), self.OnBold, self.OnUpdateBold)
        doBind( tbar.AddTool(-1, _rt_italic.GetBitmap(), isToggle=True,
                            shortHelpString=u"Italique"), self.OnItalic, self.OnUpdateItalic)
        doBind( tbar.AddTool(-1, _rt_underline.GetBitmap(), isToggle=True,
                            shortHelpString=u"Souligné"), self.OnUnderline, self.OnUpdateUnderline)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, _rt_alignleft.GetBitmap(), isToggle=True,
                            shortHelpString=u"Aligner à gauche"), self.OnAlignLeft, self.OnUpdateAlignLeft)
        doBind( tbar.AddTool(-1, _rt_centre.GetBitmap(), isToggle=True,
                            shortHelpString=u"Centrer"), self.OnAlignCenter, self.OnUpdateAlignCenter)
        doBind( tbar.AddTool(-1, _rt_alignright.GetBitmap(), isToggle=True,
                            shortHelpString=u"Aligner à droite"), self.OnAlignRight, self.OnUpdateAlignRight)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, _rt_indentless.GetBitmap(),
                            shortHelpString=u"Diminuer le retrait"), self.OnIndentLess)
        doBind( tbar.AddTool(-1, _rt_indentmore.GetBitmap(),
                            shortHelpString=u"Augmenter le retrait"), self.OnIndentMore)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, _rt_font.GetBitmap(),
                            shortHelpString=u"Police de caractères"), self.OnFont)
        doBind( tbar.AddTool(-1, _rt_colour.GetBitmap(),
                            shortHelpString=u"Couleur de la police"), self.OnColour)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, _rt_images.GetBitmap(),
                            shortHelpString=u"Insérer une image"), self.OnImage)
        tbar.Realize()
        
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
_rt_open = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAbpJ"
    "REFUKJGlkz1IW1EUx39X3zNRgwFBMaCoQ0sFJwfpICgBccgkQQlOIUWE0lJCVTS0KWhU0KhY"
    "LeigoIMaQXCwgx9YR3XoIC2lpYMu4uLg0/jy8gLPQfLwGePimc79n3t+5+NyhcjJ5TkmPSbW"
    "BwaM++ejhbDICqjy9hoPxaOFsKgPDBirUQ8APjCyQSSAd54mi7hVUWZE/B583TGmwy9YjXqy"
    "QkR1W7/xEKBoOopyxXXihuPTc758dFDjasTdGTPvnKyPCoCcx9oqssmUlxTzqqI8Izb9oSNz"
    "BICZ7/uWQKnTYfqq8QdoBOD91DIAVd5eo7bSZX2Fr2992GUZm02mZ26NN8M/AbgAdpKD9H+D"
    "5rzPuDtj/F0Zwts3czeCoqoAxFWNhK6jaTpjXe3Mh+osXaWTfy2G2T74jbmDpb1DAi0NXN0k"
    "LJCIv9WEpJMPZ0Noeoq5jR9sTgSFOUKBJKFpuqWiXZaJ+Fv5FIKRyxg740GSqSSQZ13i65fV"
    "KKpKEfkZW09DnMWFxNW7Av9Oz6wAhz0XXUuhkB2SiCehEFBhcm2LzYmgAJCcBXZ2j/9nJD1l"
    "tZUu0xfP/Y230rSdugX3RssAAAAASUVORK5CYII=")

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
_rt_sample = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAMNJ"
    "REFUWIXtl0sawiAMhGcoN2mvqIeoV6RHUVwoC5VqiOkXFsyahJ+8ADJM8FRw3X0A9AAQfy3I"
    "t2vWOGaYaAIAAPN8atp82y7ite4pEAOktCKl1Q/gKLkDiIpQovfCk3aPGQAA5MaGJYGo7XMr"
    "RQD4RiCaJi8q3mSWHRVhSSDr5MtyPgTAPQJEOftOBFpq4OlIbElKbsOaIT5vO203uafAHcB0"
    "Ej7UNjk6isBO/7dI48IsBdI3YBXg/7PrxfE1GwDeAHen2yjnZJXsxQAAAABJRU5ErkJggg==")

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
_rt_smiley = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAATpJ"
    "REFUWIXtV9EWwiAIRdeH7dP3Y0UPxiIHXjR31kO8VIPuvQNFTCkvdKXdRv7EjzvXz1Je0qkC"
    "NCkf6IlSevt7xCRUAiG2SH3QuJCMyJn7yIlKPLNdqtrMDIy8tU/w+nSy4WZgBrngtLJxECBp"
    "tyyBiiI/FIDImX0S5Pey0FyENbgA1STI3xKxC/DeXoNrIPQ7Wg6YAQ3eswaiizhUgjMtE7UX"
    "nzYUE8XQ6+A3MvAXgKy3w/XEZ6JyUES22LQYdTCFB5JNARDZ/UFi1ihoVIB0ts0QoomFvG94"
    "UfMA6gciwrMI+XAJiD57vBayKn8PeXlWTUTRrtjb9y1yImMbRnaEkI7Mi1DALmRoyrdxvLcv"
    "/sZYHi1HkxyM5s1OKOUY6YQR8hIbvBvim5H6PvNmhMSMkH4tYKZdfhw/Ad89rp/htXYGAAAA"
    "AElFTkSuQmCC")

#----------------------------------------------------------------------
_rt_underline = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAFdJ"
    "REFUOI1jZGRiZqAEMFGkmxoGsKAL/P/39z8yn5GJmRGbGE4XIEvC2NjEcBpAKhg1gIABS5cs"
    "/o9MYwOMuJIyetwzMGBGIV4DiAUEUyI2gJKwBjw3AgDOdhYrghF5ggAAAABJRU5ErkJggg==")

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

_rt_images = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAylJ"
    "REFUOI1lk11oWwUAhb/7k581XfqXNF1tunbVLVVr7ag4ZVrrNsaQbiJaZKBDmRWLoi8b+jSK"
    "MPVBQV8UXwT1xfmDLXMZVijinNrJOqzdZtquadIuTdI2aXZzf3Jv7vVBmJqdx4/DgQPnCFQo"
    "ej5+PNzkOyYJwk3mAKYlUCgaxGLXxhIz4y+MjIzYAHJlgOz1+TvbGgJCBb9hQCKl0HV35HmP"
    "16XCyCsAYmUASz/rzi0QRBFEUaCxzsPeh3e+/Pno5FsA0n9Np57CLWZmBr1uqzf96xfk539j"
    "I3kV16ZqqmoD6JaLpVQGQ9fRTXZ3Pzjwb9HRAQarG+uHN3f19y4S8SFWs6PFhZ25Qj4Vpyrc"
    "Q/jxEyzlbObnFlE0i3Q2YwoApw9xsnXvwBudh9/morqN937yUJag20zy7D6Vufg0N858jGD7"
    "2HH0U5azKiWjxJXY/IY0OsBQ/faOd5xNNd+rid8zq+Wq8JtnAly6DG1alKmmT5iouobZ2kEk"
    "Nsvs1RkCXQdwy5BdyxvS0L7gV3Wd93gvfnZ2KPHHdHxX35ZDnSGDbmeS1x7NcTL1JRPajwTT"
    "RV7t3c/k6VOE7h/E568nlU4bsi8UaLnrycdkX430tSg40paQyDMtv0BEB1Pg3dUI55d9HLSa"
    "cDfEqHVraNk4weatuEQJeenPhfHgufED7fdtDyCUYGURNAVKGhgaexydPQtNlL0PUfgrCsUN"
    "cGzcbgFREpDzBf3IxAffHvTfVnO0py+ya1tH3T8mQwW9SNkqsh69TmAxQVZMkt5p097YjAgI"
    "goA0Noc6tsBUv9/45vL0cri5Qe6q8QOKArqOYOkoSoHVdI5Mi0Wi9XbufeJ1JFEmnrxu3Fzi"
    "8DlyhsLweDR2yczlwNZAKyIUVEI9Zba+WGY+CO19Q3h9XsAGxP8v8YcUxgN3BNs21tXdm0s5"
    "3JaGpFnkCw7fTcFaaz+PvPQ+luUgCiLx5Ipxy5nufO4js71e58LZD3HSs7iwWTO91O0/zNNH"
    "TiB6PGiqjccl4pIkT+XpiF5IHy/p68dKSgFFUSiXQZJdVNcGKZsGhq5jOw6SKLG8ki38DbMJ"
    "XHT2R43dAAAAAElFTkSuQmCC")
