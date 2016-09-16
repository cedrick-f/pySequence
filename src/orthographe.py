#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# Name: ed_editv.py                                                           #
# Purpose: Editor view notebook tab implementation                            #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
Text editor buffer view control for the main notebook

@summary: Editor view

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: ed_editv.py 67834 2011-06-02 02:39:41Z CJP $"
__revision__ = "$Revision: 67834 $"

#--------------------------------------------------------------------------#
# Imports
import wx
import os
import  wx.stc  as  stc
import functools
from widgets import ToolTip

from stcspellcheck import STCSpellCheck


ID_UNDO = 1
ID_REDO = 2
ID_CUT = 3
ID_COPY = 4
ID_PASTE = 5
ID_TO_UPPER = 6
ID_TO_LOWER = 7
ID_SELECTALL = 8

class STC_ortho(ToolTip, stc.StyledTextCtrl):
    def __init__(self, *args, **kwargs):
        
        stc.StyledTextCtrl.__init__(self, *args, **kwargs)
        ToolTip.__init__(self)
        
        self.spell = STCSpellCheck(self, language="fr_FR")
        self.SetMarginType(0, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 0)
        self.SetMinSize((200, 22))
#        self.SetScrollWidth(0)
#        self.SetUseHorizontalScrollBar(False)
        self.SetWrapMode(stc.STC_WRAP_WORD)
#        self.SetLayoutCache(stc.STC_CACHE_NONE )
        self.toutVerifier = False
        self.skipEvt = True
        self.remplace = False
        
        self.Bind(stc.EVT_STC_MODIFIED, self.OnModified)
#         self.Bind(stc.EVT_STC_CHANGE, self.OnModified)
#        self.Bind(stc.EVT_STC_CHANGE, self.OnChange)
        
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        
#        self.Bind(wx.EVT_MENU, self._OnMenu)

        
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.modified_count = 0



#    def _OnMenu(self,evt):
##        print 'OnMenu'
#        evt.Skip()

    def OnContextMenu(self,evt):
        pos = evt.GetPosition()
        bpos = self.PositionFromPoint(self.ScreenToClient(pos))
        words = self.GetWordFromPosition(bpos)

#        print dir(evt)
#        print evt.GetClientObject()
        
        spell = self.spell._spelling_dict
        
        if spell != None and len(words[0]) > 0 and not spell.check(words[0]):
            sugg = self.spell.getSuggestions(words[0])
            menu = wx.Menu()
            
            if len(sugg) == 0:
                item = wx.MenuItem(menu, wx.ID_ANY, u"Aucune suggestion")
                item.Enable(False)
                item1 = menu.AppendItem(item)    
                
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
#        print "Remplacer"
        self.remplace = True
        self.Replace(start, end, mot)
#        print "fin Remplacer"
        
    def GetWordFromPosition(self, pos):
        """Get the word at the given position
        @param pos: int
        @return: (string, int_start, int_end)

        """
        end = self.WordEndPosition(pos, True)
        start = self.WordStartPosition(pos, True)
        word = self.GetTextRange(start, end)
        return (word, start, end)
        
        
    def SetValue(self, text, event = True):
#         print "SetValue", text[:10], "..."
        self.toutVerifier = True
        self.skipEvt = event
        wx.CallAfter(self.SetText, text)
        
        
 
    def OnModified(self, evt):
#         print "OnModified", self.skipEvt
        # NOTE: on really big insertions, evt.GetText can cause a
        # MemoryError on MSW, so I've commented this dprint out.
        mod = evt.GetModificationType()
#        print "mod", mod & stc.STC_MOD_BEFOREINSERT, mod & stc.STC_MOD_CHANGEFOLD, mod & stc.STC_MOD_CONTAINER, mod & stc.STC_MOD_BEFOREDELETE
        if mod & stc.STC_MOD_INSERTTEXT or mod & stc.STC_MOD_DELETETEXT:# or self.toutVerifier:
#            print "OnModified", self.toutVerifier
            #print("(%s) at %d: text=%s len=%d" % (self.transModType(evt.GetModificationType()),evt.GetPosition(), repr(evt.GetText()), evt.GetLength()))
            
            if self.toutVerifier:
#                print "   toutVerifier"
                pos = 1
                last = self.GetLastPosition()
            else:
                pos = evt.GetPosition()
                last = pos + evt.GetLength()
                
                
            self.toutVerifier = False
                
            self.spell.addDirtyRange(pos, last, evt.GetLinesAdded(), mod & stc.STC_MOD_DELETETEXT)
            
            #self.modified_count += 1
            #if self.modified_count > 10:
            #    wx.CallAfter(self.spell.processDirtyRanges)
            #    self.modified_count = 0
#            print self.skipEvt
            evt.Skip(self.skipEvt)
            self.skipEvt = True
        
        else:
            evt.Skip(False)
#        if self.remplace:
#            evt.Skip()
#            self.remplace = False
#        else:
#            evt.Skip(False)
#            
        
        
    def OnIdle(self, evt):
        self.spell.processIdleBlock()
        
    def transModType(self, modType):
        st = ""
        
        table = [(stc.STC_MOD_INSERTTEXT, "InsertText"),
                 (stc.STC_MOD_DELETETEXT, "DeleteText"),
                 (stc.STC_MOD_CHANGESTYLE, "ChangeStyle"),
                 (stc.STC_MOD_CHANGEFOLD, "ChangeFold"),
                 (stc.STC_PERFORMED_USER, "UserFlag"),
                 (stc.STC_PERFORMED_UNDO, "Undo"),
                 (stc.STC_PERFORMED_REDO, "Redo"),
                 (stc.STC_LASTSTEPINUNDOREDO, "Last-Undo/Redo"),
                 (stc.STC_MOD_CHANGEMARKER, "ChangeMarker"),
                 (stc.STC_MOD_BEFOREINSERT, "B4-Insert"),
                 (stc.STC_MOD_BEFOREDELETE, "B4-Delete")
                 ]

        for flag,text in table:
            if flag & modType:
                st = st + text + " "

        if not st:
            st = 'UNKNOWN'

        return st
    
    
    












if __name__ == "__main__":
    import sys
    
    class Frame(wx.Frame):
        def __init__(self, *args, **kwargs):
            super(self.__class__, self).__init__(*args, **kwargs)

            self.stc = STC_ortho(self, -1)

            self.CreateStatusBar()
            menubar = wx.MenuBar()
            self.SetMenuBar(menubar)  # Adding the MenuBar to the Frame content.
            menu = wx.Menu()
            menubar.Append(menu, "File")
            self.menuAdd(menu, "Open", "Open File", self.OnOpenFile)
            self.menuAdd(menu, "Quit", "Exit the pragram", self.OnQuit)
            menu = wx.Menu()
            menubar.Append(menu, "Edit")
            self.menuAdd(menu, "Check All", "Spell check the entire document", self.OnCheckAll)
            self.menuAdd(menu, "Check Current Page", "Spell check the currently visible page", self.OnCheckPage)
            self.menuAdd(menu, "Check Selection", "Spell check the selected region", self.OnCheckSelection)
            menu.AppendSeparator()
            self.menuAdd(menu, "Clear Spelling", "Remove spelling correction indicators", self.OnClearSpelling)
            menu = wx.Menu()
            menubar.Append(menu, "Language")
            langs = self.stc.spell.getAvailableLanguages()
            self.lang_id = {}
            for lang in langs:
                id = wx.NewId()
                self.lang_id[id] = lang
                self.menuAdd(menu, lang, "Change dictionary to %s" % lang, self.OnChangeLanguage, id=id)


        def loadFile(self, filename):
            fh = open(filename)
            self.stc.SetText(fh.read())
            self.stc.spell.clearDirtyRanges()
            self.stc.spell.checkCurrentPage()
        
        def loadSample(self, paragraphs=10):
            lorem_ipsum = u"""\
Lorem ipsum dolor sit amet, consectetuer adipiscing elit.  Vivamus mattis
commodo sem.  Phasellus scelerisque tellus id lorem.  Nulla facilisi.
Suspendisse potenti.  Fusce velit odio, scelerisque vel, consequat nec,
dapibus sit amet, tortor.  Vivamus eu turpis.  Nam eget dolor.  Integer
at elit.  Praesent mauris.  Nullam non nulla at nulla tincidunt malesuada.
Phasellus id ante.  Sed mauris.  Integer volutpat nisi non diam.  Etiam
elementum.  Pellentesque interdum justo eu risus.  Cum sociis natoque
penatibus et magnis dis parturient montes, nascetur ridiculus mus.  Nunc
semper.  In semper enim ut odio.  Nulla varius leo commodo elit.  Quisque
condimentum, nisl eget elementum laoreet, mauris turpis elementum felis, ut
accumsan nisl velit et mi.

And some Russian: \u041f\u0438\u0442\u043e\u043d - \u043b\u0443\u0447\u0448\u0438\u0439 \u044f\u0437\u044b\u043a \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f!

"""
            self.stc.ClearAll()
            for i in range(paragraphs):
                self.stc.AppendText(lorem_ipsum)
            # Call the spell check after the text has had a chance to be
            # displayed and the window resized to the correct size.
            self.stc.spell.clearDirtyRanges()
            wx.CallAfter(self.stc.spell.checkCurrentPage)

        def menuAdd(self, menu, name, desc, fcn, id=-1, kind=wx.ITEM_NORMAL):
            if id == -1:
                id = wx.NewId()
            a = wx.MenuItem(menu, id, name, desc, kind)
            menu.AppendItem(a)
            wx.EVT_MENU(self, id, fcn)
            menu.SetHelpString(id, desc)
        
        def OnOpenFile(self, evt):
            dlg = wx.FileDialog(self, "Choose a text file",
                               defaultDir = "",
                               defaultFile = "",
                               wildcard = "*")
            if dlg.ShowModal() == wx.ID_OK:
                print("Opening %s" % dlg.GetPath())
                self.loadFile(dlg.GetPath())
            dlg.Destroy()
        
        def OnQuit(self, evt):
            self.Close(True)
        
        def OnCheckAll(self, evt):
            self.stc.spell.checkAll()
        
        def OnCheckPage(self, evt):
            self.stc.spell.checkCurrentPage()
        
        def OnCheckSelection(self, evt):
            self.stc.spell.checkSelection()
        
        def OnClearSpelling(self, evt):
            self.stc.spell.clearAll()
        
        def OnChangeLanguage(self, evt):
            id = evt.GetId()
            normalized = locale.normalize(self.lang_id[id])
            try:
                locale.setlocale(locale.LC_ALL, normalized)
                print("Changing locale %s, dictionary set to %s" % (normalized, self.lang_id[id]))
            except locale.Error:
                print("Can't set python locale to %s; dictionary set to %s" % (normalized, self.lang_id[id]))
            self.stc.spell.setLanguage(self.lang_id[id])
            self.stc.spell.clearAll()
            self.stc.spell.checkCurrentPage()

    app = wx.App(False)
    frame = Frame(None, size=(600, -1))
    need_sample = True
    if len(sys.argv) > 1:
        if not sys.argv[-1].startswith("-"):
            frame.loadFile(sys.argv[-1])
            need_sample = False
    if need_sample:
        frame.loadSample()
    if '-d' in sys.argv:
        frame.stc.spell._spelling_debug = True
    frame.Show()
    app.MainLoop()
    
    
 