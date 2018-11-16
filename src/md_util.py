#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                 md_util                                 ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014-2016 Cédrick FAURY - Jean-Claude FRICOU
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
Module md_util
**************

Gestion des fenêtres d'aide au format Markdown


"""

#from __future__ import absolute_import

#import sys
#print sys.path
#sys.path.insert(4,'C:\Python27\Lib\site-packages\Markdown-2.6.5-py2.7.egg-info')
AS_MD = True



# try:
#     import markdown as md
# except:
#     print "Erreur import markdown"
#     try:
#         import mistune as md
#     except:
#         AS_MD = False
        
import  wx

import  wx.html

import markdown as md
# En cas d'erreur d'import de markdown
# modifier le fichier inlinepatterns.py (inverser lignes 54 et 56) :
## try:  # pragma: no cover
##     import htmlentitydefs as entities
## except ImportError:  # pragma: no cover
##     from html import entities



# texte = u"""
# # Contexte
# La description du contexte doit mettre en évidence les 3 points suivants :
# 
#  * La situation externe ;
#  * L'environnement du projet ;
#  * Les insatisfactions et/ou les pistes d'amélioration.
# # Fonctionnalités
# L'ensemble des fonctionnalités se traduit sous la forme d'une ou plusieurs fonctions de service essentielles. En STI2D, les fonctions de service à satisfaire sont majoritairement des fonctions d'usage. L'expression d'une fonction de service doit laisser la plus grande latitude possible au concepteur du produit dans sa recherche de solutions. C'est pourquoi l'expression d'une fonction de service ne contient pas, sauf nécessité ou choix délibéré et bien pesé, de référence à une solution technique particulière.
# # Caractéristiques fonctionnelles
# Les caractéristiques fonctionnelles expriment, pour chacune des fonctions de service précédentes, le (ou les) critère(s) essentiel(s) d'appréciation qui permettront de juger que le service est bien rendu par le produit.
# # Caractéristiques techniques
# Les caractéristiques techniques précisent, dans l'esprit des niveaux caractérisant les critères d'une fonction de service au sens de la norme NF EN16271, les performances nominales attendues par le produit pour le service en question, et la plage d'acceptabilité autour de la valeur nominale.
# 
# Extrait de la norme NF EN16271 : "_ une fonction de service est une action demandée à un produit ou réalisée par lui, afin de satisfaire une partie du besoin d'un utilisateur.
# Les fonctions de service sont soit des fonctions d'usage soit des fonctions d'estime. _"
# # Domaine d'étude
# Le domaine d'étude doit porter sur :
#  * Compétitivité et développement durable ;
#  * Innovation et développement durable ;
#  * Eco-conception et développement durable.
# #Thème d'étude
# Le théme d'étude peut porter sur les loisirs, la santé, l'habitat, les transports, etc...
# 
# """
# ...

class SimpleHtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, texte = ""):
        wx.html.HtmlWindow.__init__(self, parent, -1, style = wx.NO_FULL_REPAINT_ON_RESIZE)

        if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
            self.SetStandardFonts()

        if AS_MD:
            html = md.markdown(texte)
            self.SetPage(html)

    def OnLinkClicked(self, linkinfo):
#        self.log.WriteText('OnLinkClicked: %s\n' % linkinfo.GetHref())
        super(SimpleHtmlWindow, self).OnLinkClicked(linkinfo)

    def OnSetTitle(self, title):
#        self.log.WriteText('OnSetTitle: %s\n' % title)
        super(SimpleHtmlWindow, self).OnSetTitle(title)

    def OnCellMouseHover(self, cell, x, y):
#        self.log.WriteText('OnCellMouseHover: %s, (%d %d)\n' % (cell, x, y))
        super(SimpleHtmlWindow, self).OnCellMouseHover(cell, x, y)

    def OnCellClicked(self, cell, x, y, evt):
#        self.log.WriteText('OnCellClicked: %s, (%d %d)\n' % (cell, x, y))
        if isinstance(cell, html.HtmlWordCell):
            sel = html.HtmlSelection()
#            self.log.WriteText('     %s\n' % cell.ConvertToText(sel))
        super(SimpleHtmlWindow, self).OnCellClicked(cell, x, y, evt)


class MD_editor(wx.Panel):
    def __init__(self, parent, texte = ""):
        wx.Panel.__init__(self, parent, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.texteMD = wx.TextCtrl(self, -1, texte, style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        sizer.Add(self.texteMD, 1, flag = wx.EXPAND)

        self.texteHTML = SimpleHtmlWindow(self)
        self.titleBase = "aaa"
#        self.texteHTML.SetRelatedFrame(self, self.titleBase + " -- %s")
        self.texteHTML.SetRelatedStatusBar(0)
        sizer.Add(self.texteHTML, 1, flag = wx.EXPAND)

        self.Bind(wx.EVT_TEXT, self.OnText, self.texteMD)

        self.OnText()

        self.SetSizerAndFit(sizer)
        
    def OnText(self, evt = None):
        print("OnText")
        if AS_MD:
            html = md.markdown(self.texteMD.GetValue())
            self.texteHTML.SetPage(html)

# class MDFrameEditor(wx.Frame):
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1)
#         self.html = MD_editor(self, texte)

class MDFrame(wx.Frame):
    def __init__(self, parent, titre, texte, pos = wx.DefaultPosition, size = wx.DefaultSize):
        wx.Frame.__init__(self, parent, -1, titre, pos, size)
        self.html = SimpleHtmlWindow(self, texte)



#if __name__ == '__main__':
#    
#    
#    app = wx.App()
#    app.frame = MDFrame()
#    app.frame.Show()
#    app.MainLoop()
        
