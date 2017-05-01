#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""

Copyright (C) 2011  
@author: Cedrick FAURY

"""

import wx
import wx.richtext as rt
from wx.lib.embeddedimage import PyEmbeddedImage
import os
import cStringIO
from constantes import xmlVide
print 10
import webbrowser
import images
print 11
from widgets import ToolTip
print 12
#from urlparse import urlparse
#from rfc3987 import parse


def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

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


#from stcspellcheck import RTCSpellCheck
        
        
class RichTextCtrl(ToolTip, rt.RichTextCtrl): 
    def __init__(self, *args, **kargs):
        rt.RichTextCtrl.__init__(self, *args, **kargs)
        self.initToolTip()
        
class RichTextPanel(wx.Panel):
    def __init__(self, parent, objet, toolBar = False, size = wx.DefaultSize):
        wx.Panel.__init__(self, parent, -1, style = wx.BORDER_SUNKEN)
        
        self.objet = objet
        
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        if toolBar:
            self.tbar = self.MakeToolBar()
            if self.tbar != None:
                self.sizer.Add(self.tbar, flag = wx.EXPAND)
            
        self.rtc = RichTextCtrl(self, size = size, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS);
#        self.spell = RTCSpellCheck(self.rtc, language="fr_FR")
        self.toutVerifier = False
        
        
        self.sizer.Add(self.rtc, 1, flag = wx.EXPAND)
        self.SetSizer(self.sizer)
    
                    
        self.Ouvrir()
#        self.rtc.Bind(rt.EVT_RICHTEXT_LEFT_CLICK, self.OnModified)
#        self.rtc.Bind(wx.EVT_IDLE, self.OnIdle)
        self.rtc.Bind(wx.EVT_KILL_FOCUS, self.Sauver)
        self.rtc.Bind(wx.EVT_TEXT_URL, self.OnURLClick)

        
    
    def OnIdle(self, evt):
        self.spell.processIdleBlock()

    def OnContextMenu(self,evt):
        pos = evt.GetPosition()
        bpos = self.PositionFromPoint(self.ScreenToClient(pos))
        words = self.GetWordFromPosition(bpos)

#        print dir(evt)
#        print evt.GetClientObject()
        
        spell = self.spell._spelling_dict
        if not spell.check(words[0]):
            sugg = self.spell.getSuggestions(words[0])
            menu = wx.Menu()
        
            for w in sugg:
                item = wx.MenuItem(menu, wx.ID_ANY, w)
                item1 = menu.AppendItem(item)    
                self.Bind(wx.EVT_MENU, 
                          functools.partial(self.Remplacer, mot = w, start = words[1], end = words[2]), 
                          item1)
            
            self.PopupMenu(menu)
            menu.Destroy()
            
        else:
            evt.Skip()
        
    def Remplacer(self, event = None, mot = u"", start = 0, end = 0):
        self.Replace(start, end, mot)
        
    def GetWordFromPosition(self, pos):
        """Get the word at the given position
        @param pos: int
        @return: (string, int_start, int_end)

        """
        end = self.WordEndPosition(pos, True)
        start = self.WordStartPosition(pos, True)
        word = self.GetTextRange(start, end)
        return (word, start, end)
        
        
    def SetValue(self, text):
#        print "SetValue", text
        self.toutVerifier = True
        self.SetText(text)

 
    def OnModified(self, evt):
        # NOTE: on really big insertions, evt.GetText can cause a
        # MemoryError on MSW, so I've commented this dprint out.
        print "OnModified"
                    
        if self.toutVerifier:
            pos = 1
            last = self.rtc.GetLastPosition()
        else:
            pos = self.rtc.GetInsertionPoint()
            last = pos + evt.GetPosition()
        
        self.toutVerifier = False
            
        self.spell.addDirtyRange(pos, last)
        
        #self.modified_count += 1
        #if self.modified_count > 10:
        #    wx.CallAfter(self.spell.processDirtyRanges)
        #    self.modified_count = 0
        evt.Skip()
        
    def GetValue(self):
        return self.rtc.GetValue()
    
    
    def SetToolTipString(self, txt):
        self.rtc.SetToolTipString(txt)
        
    def SetTitre(self, txt):
        self.rtc.SetTitre(txt)
        
    def setObjet(self, objet):
        self.objet = objet
        
    def Ouvrir(self):
        u""" Rempli la zone de texte avec le contenu de objet.description
        """
        out = cStringIO.StringIO()
        handler = rt.RichTextXMLHandler()
        buff = self.rtc.GetBuffer()
#        buff.AddHandler(handler)
        if hasattr(self.objet, "description"):
            if self.objet.description == None:
                out.write(xmlVide)
            else:
                out.write(self.objet.description)
        else:
            if self.objet[0] == u"":
                out.write(xmlVide)
            else:
                out.write(self.objet[0])
        out.seek(0)
        handler.LoadStream(buff, out)
        self.rtc.Refresh()


    def Sauver(self, evt = None):
        if self.rtc.GetValue() == "":
            if hasattr(self.objet, "description"):
                self.objet.SetDescription(None)
            else:
                self.objet[0]=u""
        else:
            texte = self.GetXML()
            if texte is None:
                return
            if hasattr(self.objet, "description"):
                self.objet.SetDescription(texte)
            else:
                self.objet[0]=texte
            
        if evt != None:
            evt.Skip()


    def GetHTML(self):
        # Get an instance of the html file handler, use it to save the
        # document to a StringIO stream
        handler = rt.RichTextHTMLHandler()
        handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
        handler.SetFontSizeMapping([7,9,11,12,14,22,100])

        stream = cStringIO.StringIO()
        if not handler.SaveStream(self.rtc.GetBuffer(), stream):
            return

        return stream.getvalue()



    def GetXML(self):
        # Get an instance of the html file handler, use it to save the
        # document to a StringIO stream
        handler = rt.RichTextXMLHandler()
        handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
        
        stream = cStringIO.StringIO()
        if not handler.SaveStream(self.rtc.GetBuffer(), stream):
            return

        return stream.getvalue()



    def InsertImage(self):
        wildcard= u"Fichier image (bmp, gif, jpeg, png, tiff, tga, pnm, pcx, ico, xpm)|(*.bmp; *.gif; *.jpg; *.jpeg; *.png; *.tif; *.tiff; *.tga; *.xpm ; *.ico ; *.pcx ; *.pnm)"
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
       
        
    def IndentLess(self):
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
            
    def ParagraphSpacingMore(self):
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

        
    def ParagraphSpacingLess(self):
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
        
    def LineSpacingSingle(self): 
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
 
                
    def LineSpacingHalf(self):
        attr = rt.RichTextAttr()
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
            
    def Font(self):
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

    def InsertURL(self):
        if not self.rtc.HasSelection():
            return

        r = self.rtc.GetSelectionRange()
        s = r.GetStart()
        e = r.GetEnd()
        
        t = self.rtc.GetRange(s, e)
#        parse = urlparse(t)
        

        
        dlg = wx.TextEntryDialog(self, u"Adresse du lien",
                                 u'Insérer un lien')
        
        if is_valid_url(t):
            dlg.SetValue(t)
        else:
            dlg.SetValue(u"")

        if dlg.ShowModal() == wx.ID_OK:
#            print parse(dlg.GetValue())
#            if is_valid_url(dlg.GetValue()):
#                print dlg.GetValue()
            urlStyle = rt.RichTextAttr()
            urlStyle.SetTextColour(wx.BLUE)
            urlStyle.SetFontUnderlined(True)
            urlStyle.SetFontSize(8)
            
            self.rtc.Delete(r)
            
            self.rtc.SetInsertionPoint(s)
            self.rtc.BeginStyle(urlStyle)
            self.rtc.BeginURL(dlg.GetValue())
            self.rtc.WriteText(t)
            self.rtc.EndURL();
            self.rtc.EndStyle();
        dlg.Destroy()
        
        

    def Colour(self):
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
            
            
    def MakeToolBar(self):
        def doBind(item, handler, updateUI=None):
            self.Bind(wx.EVT_TOOL, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)
        
#        tbar = self.CreateToolBar()
        
        tbar = wx.ToolBar(self)
        
#        doBind( tbar.AddTool(-1, _rt_open.GetBitmap(),
#                            shortHelpString=u"Ouvrir"), self.OnFileOpen)
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
        
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, images.Bouton_lien.GetBitmap(),
                            shortHelpString=u"Insérer un lien"), self.OnURL)
        try:
            tbar.Realize()
        except wx._core.PyAssertionError:
            print u"Trop de documents ouverts"
            return None
        
        return tbar
            
    def ForwardEvent(self, evt):
        # The RichTextCtrl can handle menu and update events for undo,
        # redo, cut, copy, paste, delete, and select all, so just
        # forward the event to it.
        self.rtc.ProcessEvent(evt)
       
    def OnURLClick(self, evt):
        webbrowser.open_new((evt.GetString())) 
        
    def OnBold(self, evt):
        self.ApplyBoldToSelection()
        
    def OnItalic(self, evt): 
        self.ApplyItalicToSelection()
        
    def OnUnderline(self, evt):
        self.ApplyUnderlineToSelection()
        
    def OnAlignLeft(self, evt):
        self.ApplyAlignmentLeftToSelection()
        
    def OnAlignRight(self, evt):
        self.ApplyAlignmentRightToSelection()
        
    def OnAlignCenter(self, evt):
        self.ApplyAlignmentCenterToSelection()
        
    def OnIndentMore(self, evt):
        self.IndentMore()
       
    def OnIndentLess(self, evt):
        self.IndentLess()
        
    def OnParagraphSpacingMore(self, evt):
        self.ParagraphSpacingMore()
        
    def OnParagraphSpacingLess(self, evt):
        self.ParagraphSpacingLess()

    def OnLineSpacingSingle(self, evt): 
        self.LineSpacingSingle()
 
    def OnLineSpacingHalf(self, evt):
        self.LineSpacingHalf()
        
    def OnLineSpacingDouble(self, evt):
        self.LineSpacingDouble()

    def OnFont(self, evt):
        self.Font()
        
    def OnColour(self, evt):
        self.Colour()
        
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
        
    def OnImage(self, evt):
        self.InsertImage()
        
    def OnURL(self, evt):
        self.InsertURL()




try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def XMLtoHTML(texteXML):
        u""" Converti un texte au format RichText (XML)
            en HTML 
        """
        if texteXML is None:
            return
        
        out = cStringIO.StringIO()
        handler = rt.RichTextXMLHandler()
        buff = rt.RichTextBuffer()
        out.write(texteXML)
        out.seek(0)
        handler.LoadStream(buff, out)
    
        # Get an instance of the html file handler, use it to save the
        # document to a StringIO stream
        handler2 = rt.RichTextHTMLHandler()
        handler2.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
        handler2.SetFontSizeMapping([7,9,11,12,14,22,100])

        stream = cStringIO.StringIO()
        if not handler2.SaveStream(buff, stream):
            return
        
        soup = BeautifulSoup(stream.getvalue().decode('utf-8'), "html5lib")

        return soup.html.body.prettify()

















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
