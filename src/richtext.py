#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               richtext                               ##
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
Module richtext
***************

Editeur de text "riche"

"""

import wx
import wx.richtext as rt
from wx.lib.embeddedimage import PyEmbeddedImage
import os
import io

import webbrowser
import images

from widgets import ToolTip
import functools

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


bulletNames = ["standard/circle",
               "standard/square",
               "standard/diamond",
               "standard/triangle"]

# Styles de titre :


# wx.FONTSTYLE_NORMAL     The font is drawn without slant.
# wx.FONTSTYLE_ITALIC     The font is slanted in an italic style.
# wx.FONTSTYLE_SLANT     The font is slanted, but in a roman style.
# wx.FONTSTYLE_MAX      

# wx.FONTWEIGHT_NORMAL     Normal font.
# wx.FONTWEIGHT_LIGHT     Light font.
# wx.FONTWEIGHT_BOLD     Bold font.
# wx.FONTWEIGHT_MAX



# SetFontWeight, SetFontStyle, SetFontSize, SetFontUnderlined, SetTextColour
headerStyles = [(wx.FONTWEIGHT_NORMAL, wx.FONTSTYLE_NORMAL, 8 , False, wx.Colour(0,0,0)),
                (wx.FONTWEIGHT_NORMAL, wx.FONTSTYLE_NORMAL, 9 , True , wx.Colour(0,0,70)),
                (wx.FONTWEIGHT_NORMAL, wx.FONTSTYLE_NORMAL, 10, True , wx.Colour(0,10,60)),
                (wx.FONTWEIGHT_BOLD  , wx.FONTSTYLE_NORMAL, 11, False, wx.Colour(0,20,50)),
                (wx.FONTWEIGHT_BOLD  , wx.FONTSTYLE_ITALIC, 12, False, wx.Colour(0,20,60)),
                (wx.FONTWEIGHT_BOLD  , wx.FONTSTYLE_NORMAL, 14, False, wx.Colour(0,30,70)),
                ]
        
class RichTextCtrl(ToolTip, rt.RichTextCtrl): 
    def __init__(self, *args, **kargs):
        rt.RichTextCtrl.__init__(self, *args, **kargs)
        self.initToolTip()


class RichTextPanel(wx.Panel):
    def __init__(self, parent, objet, draw = False,
                 toolBar = False, size = wx.DefaultSize):
        """
            :draw: action associée à l'évévement envoyé à l'objet
        """
        wx.Panel.__init__(self, parent, -1, style = wx.BORDER_SUNKEN)
        
        self.objet = objet
        self.draw = draw
        
        # Constantes
        self.indent = 50
        self.subindent = 30
        self.bullet = "\u25CF" 
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.rtc = RichTextCtrl(self, size = size, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS)
        if toolBar:
            self.tbar = self.MakeToolBar()
            if self.tbar != None:
                self.sizer.Add(self.tbar, flag = wx.EXPAND)
            
        
#        self.spell = RTCSpellCheck(self.rtc, language="fr_FR")
        self.toutVerifier = False
        
        
        self.sizer.Add(self.rtc, 1, flag = wx.EXPAND)
        self.SetSizer(self.sizer)
    
                    
        self.Ouvrir()
#        self.rtc.Bind(rt.EVT_RICHTEXT_LEFT_CLICK, self.OnModified)
#        self.rtc.Bind(wx.EVT_IDLE, self.OnIdle)
        #self.rtc.Bind(wx.EVT_KILL_FOCUS, self.Sauver)
        self.rtc.Bind(wx.EVT_TEXT , self.Sauver)
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
        
    def Remplacer(self, event = None, mot = "", start = 0, end = 0):
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
        print("OnModified")
                    
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
        
    
    def SetTexteXML(self, text = None):
        from constantes import xmlVide
        out = io.BytesIO()
        handler = rt.RichTextXMLHandler()
        buff = self.rtc.GetBuffer()
        buff.AddHandler(handler) 
        if text == None:
            out.write(bytes(xmlVide, encoding = "utf8"))
        else:
            out.write(bytes(text, encoding = "utf8"))
        
        out.seek(0)
        handler.LoadFile(buff, out)

        self.rtc.Refresh()
        
    def Ouvrir(self):
        """ Rempli la zone de texte avec le contenu de objet.description
        """
        from constantes import xmlVide
        out = io.BytesIO()
        
        handler = rt.RichTextXMLHandler()
        buff = self.rtc.GetBuffer()
        buff.AddHandler(handler)
        if hasattr(self.objet, "description"):
            if self.objet.description == None:
                out.write(bytes(xmlVide, encoding = "utf8"))
            else:
#                 print(self.objet.description)
                out.write(bytes(self.objet.description, encoding = "utf8"))
                
        else:
            if self.objet[0] == "":
                out.write(bytes(xmlVide, encoding = "utf8"))
            else:
                out.write(bytes(self.objet[0], encoding = "utf8"))
        out.seek(0)
        
        handler.LoadFile(buff, out)
        self.rtc.Refresh()


    def Sauver(self, evt = None):
#         print("Sauver", self.objet)
        if self.rtc.GetValue() == "":
            if hasattr(self.objet, "description"):
                self.objet.SetDescription(None, self.draw)
            else:
                self.objet[0]=""
        else:
            texte = self.GetXML()
#             print(">>", texte)
            if texte is None:
                return
            if hasattr(self.objet, "description"):
                self.objet.SetDescription(texte, self.draw)
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

        stream = io.StringIO()
        if not handler.SaveFile(self.rtc.GetBuffer(), stream):
            return

        return stream.getvalue()



    def GetXML(self):
        # Get an instance of the html file handler, use it to save the
        # document to a StringIO stream
        handler = rt.RichTextXMLHandler()
        handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
        
        stream = io.BytesIO()
        if not handler.SaveFile(self.rtc.GetBuffer(), stream):
            return

        stream.seek(0)
        return stream.read().decode("utf-8")



    def InsertImage(self):
        wildcard= "Fichier image (bmp, gif, jpeg, png, tiff, tga, pnm, pcx, ico, xpm)|(*.bmp; *.gif; *.jpg; *.jpeg; *.png; *.tif; *.tiff; *.tga; *.xpm ; *.ico ; *.pcx ; *.pnm)"
        dlg = wx.FileDialog(self, "Choisir un fichier image",
                            wildcard=wildcard,
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path:
                ext = os.path.splitext(path)[1]
                if ext in list(typesImg.keys()):
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

            if self.estListPuce():
                si = self.subindent
            else:
                si = 0
                
            i = (self.GetActualLeftIndent(attr)+1)*self.indent
            attr.SetLeftIndent(i, si)
            attr.SetFlags(attr.GetFlags() |wx.TEXT_ATTR_LEFT_INDENT)
            attr.SetBulletName(self.GetActualBulletName(attr))
            self.rtc.SetStyle(r, attr)
       
        
    def IndentLess(self):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            if self.estListPuce():
                si = self.subindent
                
            else:
                si = 0
            
            i = max(0, (self.GetActualLeftIndent(attr)-1)*self.indent)
            
            attr.SetLeftIndent(i, si)
            attr.SetFlags(attr.GetFlags() |wx.TEXT_ATTR_LEFT_INDENT)
            attr.SetBulletName(self.GetActualBulletName(attr))
            self.rtc.SetStyle(r, attr)
    
    
    def estListPuce(self):
        attr = rt.RichTextAttr()
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            return attr.GetBulletStyle() != wx.TEXT_ATTR_BULLET_STYLE_NONE
        return False
    
    
#     def GetParagraphs(self):
#         if self.rtc.HasSelection():
#             ds = self.rtc.GetSelectionRange()[0]
#         else:
#             ds = self.rtc.GetInsertionPoint()
#         
#         self.rtc.MoveToParagraphEnd()
#         f = self.rtc.GetCaretPosition()
#         
#         self.rtc.MoveCaret(ds-1)
#         self.rtc.MoveToParagraphStart()
#         d = self.rtc.GetCaretPosition()
#         
#         print "GetParagraphs", d, f 
#         return d, f
# #         return rt.RichTextRange(d, f)
#     
#     def GetParagraphsStarts(self):
#         d, f = self.GetParagraphs()
#         l = []
#         n = d
#         while n < f:
#             l.append(n)
#             print "   ", n,
#             self.rtc.MoveToParagraphEnd()
#             n = self.rtc.GetCaretPosition()+1
#             self.rtc.MoveCaret(n)
#             print ">>>", n
#         if l == []:
#             l.append(d)
#         print "GetParagraphsStarts", l
#         return l
#     
#     
#     def GetParagraphsEnds(self):
#         d, f = self.GetParagraphs()
#         l = []
#         n = d
#         while n < f:
#             print "   ", n,
#             self.rtc.MoveToParagraphEnd()
#             n = self.rtc.GetCaretPosition()+1
#             self.rtc.MoveCaret(n)
#             l.append(n)
#             print ">>>", n
#         if l == []:
#             l.append(d)
#         print "GetParagraphsEnds", l
#         return l
#     
#     
#     def CutParagraphsTexts(self):
#         l = self.GetParagraphsStarts()
#         t = []
#         for d in l:
#             self.rtc.MoveCaret(d)
#             self.rtc.MoveToParagraphEnd()
#             f = self.rtc.GetCaretPosition()
#             r = rt.RichTextRange(d+1, f+1)
#             self.rtc.SetSelectionRange(r)
#             t.append(self.rtc.GetStringSelection())
#         print t
#         r = rt.RichTextRange(l[0], f+1)
#         self.rtc.SetSelectionRange(r)
#         self.rtc.Delete(r)
#         
#         return t
#     
#     def ListPuce2(self):
#         ip = self.rtc.GetInsertionPoint()
#         attr = rt.RichTextAttr()
#         if self.rtc.GetStyle(ip, attr) and attr.BulletStyle > 0: #Ignoring the possibility of numbered lists on purpose (I don't use them in my app)!
#             # Takes out the list style
#             self.rtc.MoveToParagraphStart()
#             start = self.rtc.GetInsertionPoint()
#             self.rtc.MoveToParagraphEnd()
#             end = self.rtc.GetInsertionPoint()
#             r = rt.RichTextRange(start, end)
#             attr.SetFlags(wx.TEXT_ATTR_BULLET_STYLE | wx.TEXT_ATTR_BULLET_NUMBER | wx.TEXT_ATTR_BULLET_TEXT | wx.TEXT_ATTR_BULLET_NAME)
#             attr.BulletStyle = 0
#             attr.BulletNumber = 0
#             attr.BulletText = u''
#             attr.BulletName = u''
#             attr.BulletFont = u''
#             
#             attr.SetLeftIndent(attr.GetLeftIndent() - self.indent)
#             attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
#             
#             
#             self.rtc.SetStyle(r, attr)
#         else:
#             # Transforms the current paragraph in a bulleted list item
#             self.rtc.MoveToParagraphStart()
#             self.rtc.MoveLeft()
#             start = self.rtc.GetInsertionPoint()
#             self.rtc.SetSelection(start, start+1)
#             self.rtc.DeleteSelection()
#             self.rtc.BeginSymbolBullet(unichr(9679), 100, 60)
#             self.rtc.Newline()
#             self.rtc.MoveToParagraphEnd()
#             self.rtc.EndSymbolBullet()
#         # Set the insertion point where it was
#         self.rtc.MoveCaret(ip)
#         return


    def GetActualLeftIndent(self, attr):
        return attr.GetLeftIndent() // self.indent
            
    def GetActualBulletName(self, attr):
        i = self.GetActualLeftIndent(attr)
        return bulletNames[i % len(bulletNames)]
    
    
        
    def ListPuce(self):
        attr = rt.RichTextAttr()
#         attr.SetFlags(wx.TEXT_ATTR_BULLET_STYLE_STANDARD)
        ip = self.rtc.GetInsertionPoint()
#         print "ListPuce", ip
        
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()
            
            if attr.GetBulletStyle() == wx.TEXT_ATTR_BULLET_STYLE_NONE:
#                 print " AJOUTER"
                attr.SetFlags(attr.GetFlags() |wx.TEXT_ATTR_BULLET_STYLE |
                              wx.TEXT_ATTR_LEFT_INDENT | wx.TEXT_ATTR_PARAGRAPH)
                attr.SetBulletStyle(wx.TEXT_ATTR_BULLET_STYLE_STANDARD)
#                                 wx.TEXT_ATTR_BULLET_STYLE_ARABIC |wx.TEXT_ATTR_BULLET_STYLE_ALIGN_LEFT | 
#                                 wx.TEXT_ATTR_BULLET_STYLE_PERIOD|
#                                 wx.TEXT_ATTR_BULLET_STYLE_SYMBOL)
                attr.SetLeftIndent((self.GetActualLeftIndent(attr)+1)*self.indent, self.subindent)
#                 attr.SetBulletText(self.bullet)
                attr.SetBulletName(self.GetActualBulletName(attr))
                self.rtc.SetStyle(r, attr)
                
            else:
#                 print " ENLEVER"
                attr.SetFlags(attr.GetFlags() |wx.TEXT_ATTR_LEFT_INDENT |
                              wx.TEXT_ATTR_PARAGRAPH | wx.TEXT_ATTR_BULLET_STYLE)
                attr.SetBulletStyle(wx.TEXT_ATTR_BULLET_STYLE_NONE)
                attr.SetLeftIndent((self.GetActualLeftIndent(attr)-1)*self.indent,0)
                self.rtc.SetStyle(r, attr)




    def GetActualHeader(self, attr):
        try:
            h = eval(attr.GetParagraphStyleName())
            if 0<=h<=5:
                return h
        except:
            return
        
    def SetHeader(self, attr, num):
        attr.SetFontWeight(headerStyles[num][0])
        attr.SetFontStyle(headerStyles[num][1])
        attr.SetFontSize(headerStyles[num][2])
        attr.SetFontUnderlined(headerStyles[num][3])
        attr.SetTextColour(headerStyles[num][4])
        
        
    def HeaderLess(self):

        attr = rt.RichTextAttr()
#         attr.SetFlags(wx.TEXT_ATTR_BULLET_STYLE_STANDARD)
        ip = self.rtc.GetInsertionPoint()
#         print "ListPuce", ip
        
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()
            
            h = self.GetActualHeader(attr)
            
            if h is not None and h > 0:
                h -= 1
                self.rtc.MoveToParagraphStart()
                st = self.rtc.GetInsertionPoint()#+1
                self.rtc.MoveToParagraphEnd()
                nd = self.rtc.GetInsertionPoint()#+1
                r = rt.RichTextRange(st, nd)
                self.SetHeader(attr, h)
                attr.SetParagraphStyleName(str(h))
                self.rtc.SetStyle(r, attr)

            
        
    def HeaderMore(self):
#         print "HeaderMore"
        attr = rt.RichTextAttr()
#         attr.SetFlags(wx.TEXT_ATTR_BULLET_STYLE_STANDARD)
        ip = self.rtc.GetInsertionPoint()
#         print "ListPuce", ip
        
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()
            
            h = self.GetActualHeader(attr)

            if h is None:
                h = 0
            if h < 5:
                h += 1
                self.rtc.MoveToParagraphStart()
                st = self.rtc.GetInsertionPoint()#+1
#                 print "  ",st
                self.rtc.MoveToParagraphEnd()
                nd = self.rtc.GetInsertionPoint()#+1
#                 print "  ",nd
                r = rt.RichTextRange(st, nd)
#                 print "  ",r
                self.SetHeader(attr, h)
                attr.SetParagraphStyleName(str(h))
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
        

        
        dlg = wx.TextEntryDialog(self, "Adresse du lien",
                                 'Insérer un lien')
        
        if is_valid_url(t):
            dlg.SetValue(t)
        else:
            dlg.SetValue("")

        if dlg.ShowModal() == wx.ID_OK:
#            print parse(dlg.GetValue())
#            if is_valid_url(dlg.GetValue()):
#                print dlg.GetValue()
            urlStyle = rt.RichTextAttr()
            urlStyle.SetTextColour(wx.Colour(wx.BLUE))
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
#                     print("Colour", colour, type(colour))
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
        doBind( tbar.AddTool(wx.ID_CUT, "", _rt_cut.GetBitmap(), 
                            shortHelp="Couper"), self.ForwardEvent, self.ForwardEvent)
        doBind( tbar.AddTool(wx.ID_COPY, "", _rt_copy.GetBitmap(), 
                            shortHelp="Copier"), self.ForwardEvent, self.ForwardEvent)
        doBind( tbar.AddTool(wx.ID_PASTE, "", _rt_paste.GetBitmap(), 
                            shortHelp="Coller"), self.ForwardEvent, self.ForwardEvent)
        tbar.AddSeparator()
        doBind( tbar.AddTool(wx.ID_UNDO, "", _rt_undo.GetBitmap(), 
                            shortHelp="Annuler"), self.ForwardEvent, self.ForwardEvent)
        doBind( tbar.AddTool(wx.ID_REDO, "", _rt_redo.GetBitmap(),
                            shortHelp="Rétablir"), self.ForwardEvent, self.ForwardEvent)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, "", _rt_bold.GetBitmap(),  kind = wx.ITEM_CHECK,
                            shortHelp="Gras"), self.OnBold, self.OnUpdateBold)
        doBind( tbar.AddTool(-1, "", _rt_italic.GetBitmap(), kind = wx.ITEM_CHECK,
                            shortHelp="Italique"), self.OnItalic, self.OnUpdateItalic)
        doBind( tbar.AddTool(-1, "", _rt_underline.GetBitmap(), kind = wx.ITEM_CHECK,
                            shortHelp="Souligné"), self.OnUnderline, self.OnUpdateUnderline)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, "", _rt_alignleft.GetBitmap(), kind = wx.ITEM_CHECK,
                            shortHelp="Aligner à gauche"), self.OnAlignLeft, self.OnUpdateAlignLeft)
        doBind( tbar.AddTool(-1, "", _rt_centre.GetBitmap(), kind = wx.ITEM_CHECK,
                            shortHelp="Centrer"), self.OnAlignCenter, self.OnUpdateAlignCenter)
        doBind( tbar.AddTool(-1, "", _rt_alignright.GetBitmap(), kind = wx.ITEM_CHECK,
                            shortHelp="Aligner à droite"), self.OnAlignRight, self.OnUpdateAlignRight)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, "", _rt_list.GetBitmap(), kind = wx.ITEM_CHECK,
                            shortHelp="Liste à puce"), self.OnListPuce, self.OnUpdateListPuce)
#         doBind( tbar.AddTool(-1, _rt_list.GetBitmap(),
#                             shortHelpString=u""), self.OnListPuce)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, "", _rt_indentless.GetBitmap(),
                            shortHelp="Diminuer le retrait"), self.OnIndentLess)
        doBind( tbar.AddTool(-1, "", _rt_indentmore.GetBitmap(), 
                            shortHelp="Augmenter le retrait"), self.OnIndentMore)
        
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, "", _rt_hless.GetBitmap(), 
                            shortHelp="Diminuer le niveau hierarchique"), self.OnHeaderLess)
        doBind( tbar.AddTool(-1, "", _rt_hmore.GetBitmap(), 
                            shortHelp="Augmenter le niveau hierarchique"), self.OnHeaderMore)
        
        
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, "", _rt_font.GetBitmap(), 
                            shortHelp="Police de caractères"), self.OnFont)
        doBind( tbar.AddTool(-1, "", _rt_colour.GetBitmap(), 
                            shortHelp="Couleur de la police"), self.OnColour)
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, "", _rt_images.GetBitmap(), 
                            shortHelp="Insérer une image"), self.OnImage)
        
        tbar.AddSeparator()
        doBind( tbar.AddTool(-1, "", images.Bouton_lien.GetBitmap(), 
                            shortHelp="Insérer un lien"), self.OnURL)
        try:
            tbar.Realize()
        except wx._core.PyAssertionError:
            print("Trop de documents ouverts")
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
        self.Sauver()
        
    def OnItalic(self, evt): 
        self.ApplyItalicToSelection()
        self.Sauver()
        
    def OnUnderline(self, evt):
        self.ApplyUnderlineToSelection()
        self.Sauver()
        
    def OnAlignLeft(self, evt):
        self.ApplyAlignmentLeftToSelection()
        self.Sauver()
        
    def OnAlignRight(self, evt):
        self.ApplyAlignmentRightToSelection()
        self.Sauver()
        
    def OnAlignCenter(self, evt):
        self.ApplyAlignmentCenterToSelection()
        self.Sauver()
        
    def OnIndentMore(self, evt):
        self.IndentMore()
        self.Sauver()
       
    def OnIndentLess(self, evt):
        self.IndentLess()
        self.Sauver()
        
    def OnListPuce(self, evt):
        self.ListPuce()
        self.Sauver()
        
    def OnHeaderLess(self, evt):
        self.HeaderLess()
        self.Sauver()
        
    def OnHeaderMore(self, evt):
        self.HeaderMore()
        self.Sauver()
        
    def OnParagraphSpacingMore(self, evt):
        self.ParagraphSpacingMore()
        self.Sauver()
        
    def OnParagraphSpacingLess(self, evt):
        self.ParagraphSpacingLess()
        self.Sauver()

    def OnLineSpacingSingle(self, evt): 
        self.LineSpacingSingle()
        self.Sauver()
 
    def OnLineSpacingHalf(self, evt):
        self.LineSpacingHalf()
        self.Sauver()
        
    def OnLineSpacingDouble(self, evt):
        self.LineSpacingDouble()
        self.Sauver()

    def OnFont(self, evt):
        self.Font()
        self.Sauver()
        
    def OnColour(self, evt):
        self.Colour()
        self.Sauver()
        
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
        
    def OnUpdateListPuce(self, evt):
        evt.Check(self.estListPuce())   
         
    def OnImage(self, evt):
        self.InsertImage()
        self.Sauver()
        
    def OnURL(self, evt):
        self.InsertURL()
        self.Sauver()




try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


def XMLtoTXT(texteXML):
        """ Converti un texte au format RichText (XML)
            en texte 
        """
        if texteXML is None:
            return
#         print("XMLtoHTML", texteXML)
        out = io.BytesIO()
        handler = rt.RichTextXMLHandler()
        buff = rt.RichTextBuffer()
        out.write(bytes(texteXML, encoding = "utf-8"))
        out.seek(0)
        
        handler.LoadFile(buff, out)  # out >> buff
        return buff.GetText()


def XMLtoHTML(texteXML):
        """ Converti un texte au format RichText (XML)
            en HTML 
        """
        if texteXML is None:
            return
#         print("XMLtoHTML", texteXML)
        out = io.BytesIO()
        handler = rt.RichTextXMLHandler()
        buff = rt.RichTextBuffer()
        out.write(bytes(texteXML, encoding = "utf-8"))
        out.seek(0)
#         print(out.getvalue())
        
        handler.LoadFile(buff, out)  # out >> buff
 
        # Get an instance of the html file handler, use it to save the
        # document to a StringIO stream
        handler2 = rt.RichTextHTMLHandler()
        handler2.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
        handler2.SetFontSizeMapping([7,9,11,12,14,22,100])

        stream = io.BytesIO()
        if not handler2.SaveFile(buff, stream):  # buff >> stream
            return
        
        soup = BeautifulSoup(stream.getvalue().decode('utf-8'), "html5lib")
#         print(soup.html.body.prettify())
#         soup = BeautifulSoup(stream.getvalue().decode('utf-8'), "html5lib")
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
_rt_list = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1B"
    "AACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAAZdEVYdFNvZnR3YXJlAHBhaW50Lm5l"
    "dCA0LjAuMTZEaa/1AAAARklEQVQ4T2MYVMAdiL0hTPLAeyD+BGEyNADxfwIYA4Bs94cwhyrY"
    "B8SHIUwGByAGhQM+jAEOAfEJCJM8AwYejCYksgADAwAT4CKWi4BBuAAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_hless = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1B"
    "AACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAZdEVYdFNvZnR3YXJlAHBhaW50Lm5l"
    "dCA0LjAuMTZEaa/1AAAA5ElEQVQ4T2MYBkBCQsKLm5t7u5CQ0DIXFxc5kJi8vHwESExERGSp"
    "jY2NKFghPsDHx/eUi4urAsoFAzY2tmfs7OxZUC5BcERQULAMyoaBG0CcBGESBkd4eHgoMwDo"
    "hVMCAgJzYZiRkfEDUJx4A4CBWNXb28sJw0ADbgLFwQYAA9NQTExsBTo2MTExBcmDAKEwUADi"
    "fHSsoqKiDKQZGJiYmI4LCwuTFwZaWlpsvLy8n4Dx3gUVYnB1deUGGvqGn5+/ASqEGwA1OgGp"
    "QhC2srKSAokBA9EbxAcaUujr6ysOEhu2gIEBABe4MyMwJO/yAAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
_rt_hmore = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1B"
    "AACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAZdEVYdFNvZnR3YXJlAHBhaW50Lm5l"
    "dCA0LjAuMTZEaa/1AAAA+klEQVQ4T2MYBkBCQsKLm5t7u5CQ0DIXFxc5kJi8vHwESExERGSp"
    "jY2NKFghPsDHx/eUi4urAsoFAzY2tmfs7OxZUC5BcERQULAMyoaBG0CcBGEigIKCQpyMjIwK"
    "lAsHR3h4eIgyAAg2ArELhIkAR4BeOCUgIDAXhhkZGT8AxYk3ABiIVb29vZwwDDTgJlAcZoAa"
    "kP8NhIHsP0D6J5S/GSJNXBgwQjHMBTA+AwMTE9NxYWFh8sJAS0uLjZeX9xMw3rugQgyurq7c"
    "QEPf8PPzN0CFkEEYECtCmEAA1OgEpApB2MrKSgokBgxEbxAfaEihr6+vOEhs2AIGBgAcQzW9"
    "yBeC9QAAAABJRU5ErkJggg==")

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



class MyFrame(wx.Frame):
    demo = """<?xml version="1.0" encoding="UTF-8"?>
<richtext version="1.0.0.0" xmlns="http://www.wxwidgets.org">
  <paragraphlayout textcolor="#000000" fontpointsize="9" fontfamily="70" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Segoe UI" alignment="1" parspacingafter="10" parspacingbefore="0" linespacing="10" margin-left="5,4098" margin-right="5,4098" margin-top="5,4098" margin-bottom="5,4098">
    <paragraph fontweight="92" alignment="2" parspacingafter="20" parspacingbefore="0">
      <text fontpointsize="14" fontweight="92">Welcome to wxRichTextCtrl, a wxWidgets control for editing and presenting styled text and images</text>
    </paragraph>
    <paragraph alignment="2" parspacingafter="20" parspacingbefore="0">
      <text fontstyle="93" fontweight="92">by Julian Smart</text>
    </paragraph>
    
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text></text>
    </paragraph>
    <paragraph leftindent="60" leftsubindent="0" parspacingafter="20" parspacingbefore="0">
      <text>"What can you do with this thing? "</text>
      <image imagetype="15">
        <data>89504E470D0A1A0A0000000D4948445200000020000000200806000000737A7AF40000000473424954080808087C08648800000119494441545885ED974D12C32008859F991E2C47CFCDE822430753909F98B18BB26BD4F73E9512D21AD6C6ABB28800BA3E6B40692F2DBA4A9AD2977D2F94817101D85833F54423204300022863AC897B102A4065D79E8105B2590B6798B30E919EB82AC0E8D8BD840967B405E09913D926DEB8750AE61568E22C7435F1C647101F006BF7525C0A79BFA3D7E19E8014CFE44034894357F064B486FB05A762CA7561F909FC01C275201399F91B702644E42F366D8E7831853BA24308007A7DE0397B54340AC095ED5040A4319B579A97D3C8A9070C6145C4BC7C05405FE325C82EC633E6FCAC370956C56CDDB7DA33B3259B5D9A2D00B30E54BA1BD378D09CFE66577C8500167D17682016CC635F461E4CC5F436C0CC58FE3A7E033CF37891C02ADD2E0000000049454E44AE426082</data>

      </image>
      <text>" Well, you can change text "</text>
      <text textcolor="#FF0000">colour, like this red bit.</text>
      <text textcolor="#0000FF">" And this blue bit."</text>
      <text>" Naturally you can make things "</text>
      <text fontweight="92">"bold "</text>
      <text fontstyle="93">"or italic "</text>
      <text fontunderlined="1">or underlined.</text>
      <text fontpointsize="14">" Different font sizes on the same line is allowed, too."</text>
      <text>" Next we'll show an indented paragraph."</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text>It was in January, the most down-trodden month of an Edinburgh winter. An attractive woman came into the cafe, which is nothing remarkable.</text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="-40" parspacingafter="20" parspacingbefore="0">
      <text>Next, we'll show a first-line indent, achieved using BeginLeftIndent(100, -40).</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text>It was in January, the most down-trodden month of an Edinburgh winter. An attractive woman came into the cafe, which is nothing remarkable.</text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="257" bulletnumber="1">
      <text>Numbered bullets are possible, again using sub-indents:</text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="257" bulletnumber="2">
      <text>This is my first item. Note that wxRichTextCtrl doesn't automatically do numbering, but this will be added later.</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text>This is my second item.</text>
    </paragraph>
    <paragraph rightindent="200" parspacingafter="20" parspacingbefore="0">
      <text>The following paragraph is right-indented:</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text>It was in January, the most down-trodden month of an Edinburgh winter. An attractive woman came into the cafe, which is nothing remarkable.</text>
    </paragraph>
    <paragraph alignment="3" parspacingafter="20" parspacingbefore="0" linespacing="15">
      <text>The following paragraph is right-aligned with 1.5 line spacing:</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text>It was in January, the most down-trodden month of an Edinburgh winter. An attractive woman came into the cafe, which is nothing remarkable.</text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text>Other notable features of wxRichTextCtrl include:</text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text>Compatibility with wxTextCtrl API</text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text>Easy stack-based BeginXXX()...EndXXX() style setting in addition to SetStyle()</text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text>XML loading and saving</text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text>Undo/Redo, with batching option and Undo suppressing</text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text>Clipboard copy and paste</text>
    </paragraph>
    <paragraph leftindent="100" leftsubindent="60" parspacingafter="20" parspacingbefore="0" bulletstyle="32" bulletsymbol="42" bulletfont="">
      <text>wxRichTextStyleSheet with named character and paragraph styles, and control for applying named styles</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text>A design that can easily be extended to other content types, ultimately with text boxes, tables, controls, and so on</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text>Note: this sample content was generated programmatically from within the MyFrame constructor in the demo. The images were loaded from inline XPMs. Enjoy wxRichTextCtrl!</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text></text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text fontpointsize="12" fontweight="92">Additional comments by David Woods:</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text>I find some of the RichTextCtrl method names, as used above, to be misleading.  Some character styles are stacked in the RichTextCtrl, and they are removed in the reverse order from how they are added, regardless of the method called.  Allow me to demonstrate what I mean.</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text>"Start with plain text. "</text>
      <text fontweight="92">"BeginBold() makes it bold. "</text>
      <text fontstyle="93" fontweight="92">"BeginItalic() makes it bold-italic. "</text>
      <text fontweight="92">"EndBold() should make it italic but instead makes it bold. "</text>
      <text>"EndItalic() takes us back to plain text. "</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text>"Start with plain text. "</text>
      <text fontweight="92">"BeginBold() makes it bold. "</text>
      <text fontweight="92" fontunderlined="1">"BeginUnderline() makes it bold-underline. "</text>
      <text fontweight="92">"EndBold() should make it underline but instead makes it bold. "</text>
      <text>"EndUnderline() takes us back to plain text. "</text>
    </paragraph>
    <paragraph parspacingafter="20" parspacingbefore="0">
      <text>"According to Julian, this functions "</text>
      <symbol>34</symbol>
      <text>as expected</text>
      <symbol>34</symbol>
      <text>" because of the way the RichTextCtrl is written.  I wrote the SetFontStyle() method here to demonstrate a way to work with overlapping styles that solves this problem."</text>
    </paragraph>
    <paragraph textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Times New Roman">
      <text textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Times New Roman">"Start with plain text. "</text>
      <text textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Times New Roman">"Bold. "</text>
      <text textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="93" fontweight="92" fontunderlined="0" fontface="Times New Roman">"Bold-italic. "</text>
      <text textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="93" fontweight="90" fontunderlined="0" fontface="Times New Roman">"Italic. "</text>
      <text textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Times New Roman">"Back to plain text. "</text>
    </paragraph>
    <paragraph textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Times New Roman">
      <text textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Times New Roman">"Start with plain text. "</text>
      <text textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="90" fontweight="92" fontunderlined="0" fontface="Times New Roman">"Bold. "</text>
      <text textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="90" fontweight="92" fontunderlined="1" fontface="Times New Roman">"Bold-Underline. "</text>
      <text textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="90" fontweight="90" fontunderlined="1" fontface="Times New Roman">"Underline. "</text>
      <text textcolor="#000000" bgcolor="#FFFFFF" fontpointsize="10" fontstyle="90" fontweight="90" fontunderlined="0" fontface="Times New Roman">"Back to plain text. "</text>
    </paragraph>
    <paragraph>
      <text></text>
    </paragraph>
  </paragraphlayout>
</richtext>
"""

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,100))
        rtp = RichTextPanel(self, [self.demo], toolBar=True, size = (1000, 600))
        self.SetSize((1000, 600))
        rtp.SetTitre("Test")
        rtp.SetToolTipString("")
        self.Show(True)
   

if __name__ == '__main__':
    
    app = wx.App(False)
    frame = MyFrame(None, "Hello World") # A Frame is a top-level window.
    
#     rtp.SetTexteXML(demo)
    frame.Show(True)     # Show the frame.
    app.MainLoop()






