#!/usr/bin/env python
# -*- coding: utf-8 -*-


##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                 pysequence                              ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014 C�drick FAURY - Jean-Claude FRICOU
##
## pyS�quence : aide � la construction
## de S�quences et Progressions p�dagogiques
## et � la validation de Projets

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
module lien
***********
"""
import os, sys, subprocess
import wx
import re
from util_path import toFileEncoding, toSystemEncoding, SYSTEM_ENCODING, testRel
from widgets import messageErreur, scaleImage
import images
from drag_file import *
from util_path import *
from dpi_aware import *

if sys.platform == 'darwin':
    def openFolder(path):
        subprocess.check_call(['open', '--', path])
elif sys.platform == 'linux2':
    def openFolder(path):
        subprocess.check_call(['xdg-open', '--', path])
elif sys.platform == 'win32':
    def openFolder(path):
#         subprocess.Popen(["explorer", path], shell=True)
        subprocess.call(['explorer', path.encode(sys.getfilesystemencoding())], shell=True)


####################################################################################
#
#   Objet lien vers un fichier, un dossier ou bien un site web
#
####################################################################################
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class Lien():
    def __init__(self, path = "", typ = ""):
        self.path = path # Imp�rativement toujours encod� en FILE_ENCODING !!
        self.type = typ
        self.ok = False  # Etat du lien (False = lien rompu)
        
    ######################################################################################  
    def __repr__(self):
        return self.type + " : " + toSystemEncoding(self.path)
    
    ######################################################################################  
    def reset(self):
        self.path = ""
        self.type = ""
        self.ok = False
    
    
    ######################################################################################  
    def setPath(self, path):
        self.path = path
    
    ######################################################################################  
    def __neq__(self, l):
        if self.typ != l.typ:
            return True
        elif self.path != l.path:
            return True
        return False
    
    
    ######################################################################################  
    def DialogCreer(self, pathref):
        dlg = URLDialog(None, self, pathref)
        dlg.ShowModal()
        dlg.Destroy() 
            

    ######################################################################################  
    def Afficher(self, pathref, fenSeq = None):
        """ Lance l'affichage du contenu du lien
            <pathref> = chemin de l'application pour d�terminer le chemin absolu
        """
#         print "Afficher", self.type, self.path
        path = self.GetAbsPath(pathref)
#         print "   ", path
#         print "   ", path.decode("unicode-escape")
#         print "   ", path.encode(sys.getfilesystemencoding())
        
        if self.type == "f":
            if os.path.exists(path):
                try:
                    os.startfile(path)
                except:
                    messageErreur(None, "Ouverture impossible",
                                  "Impossible d'ouvrir le fichier\n\n%s\n" %toSystemEncoding(path))
            else:
                messageErreur(None, "Chemin non trouv�",
                                  "Le fichiern'a pas �t� trouv�\n\n%s" %toSystemEncoding(path))        
            
                
        elif self.type == 'd':
            if os.path.isdir(path):
                openFolder(path)
#                 try:
# #                     subprocess.Popen(["explorer", path])
#                     
#                 except:
#                     messageErreur(None, u"Ouverture impossible",
#                                   u"Impossible d'acc�der au dossier\n\n%s\n" %toSystemEncoding(path))
            else:
                messageErreur(None, "Chemin non trouv�",
                                  "Le dossiern'a pas �t� trouv�\n\n%s" %toSystemEncoding(path))


        elif self.type == 'u':
            try:
                webbrowser.open(self.path)
            except:
                messageErreur(None, "Ouverture impossible",
                              "Impossible d'ouvrir l'url\n\n%s\n" %toSystemEncoding(self.path))
            
                
                
        elif self.type == 's':
            if os.path.isfile(path):
#                self.Show(False)
                child = fenSeq.commandeNouveau()
                child.ouvrir(path)

  
    ######################################################################################  
    def EvalTypeLien(self, pathref):
        """ Evaluation du de self.lien.path
            par rapport à pathref
            et attribue un type
        """
        print("EvalTypeLien\n  ", self.path, "\n  ", pathref)
#         print("   ", os.path.commonpath([pathref, self.path]))
                           
                           
        abspath = self.GetAbsPath(pathref)
        
        if os.path.exists(abspath):
            relpath = testRel(abspath, pathref)
            if os.path.isfile(abspath):
                self.type = 'f'

            elif os.path.isdir(abspath):
                self.type = 'd'
            
            self.path = relpath
            self.ok = True
                
        elif re.match(regex, self.path):
            self.type = 'u'
            self.ok = True
        
        else:
            self.type = ''
            self.ok = False
        
        
        
    ######################################################################################  
    def EvalLien(self, path, pathref):
        """ Teste la validité du chemin <path> (SYSTEM_ENCODING)
             par rapport au dossier de référence <pathref> (FILE_ENCODING)
             
             et change self.path (FILE_ENCODING)
             
        """
#         print("EvalLien", path, pathref, os.path.exists(pathref))
#         print " >", chardet.detect(bytes(path))
#         print " >", chardet.detect(bytes(pathref))
        
        if path == "" or path.split() == []:
            self.path = r""
            self.type = ""
            return
        
        self.EvalTypeLien(pathref)

              
    ######################################################################################  
    def GetAbsPath(self, pathdoc, path = None):
        """ Renvoie le chemin absolu du lien
            grace au chemin du document <pathdoc>
        """
#         print("GetAbsPath", path, pathref)
        if path == None:
            path = self.path
            
        if path == ".":
            return pathdoc
        
        cwd = os.getcwd()
        if pathdoc != "":
            try:
                os.chdir(pathdoc)
            except:
                pass
        
#         print os.path.exists(path)
#         print os.path.exists(os.path.abspath(path))
#         print os.path.exists(os.path.abspath(path).decode(util_path.FILE_ENCODING))
        
        # Immonde bricolage !!
#         if os.path.exists(os.path.abspath(path)) and os.path.exists(os.path.abspath(path)):#.decode(util_path.FILE_ENCODING)):
#             path = path.decode(util_path.FILE_ENCODING)
        
        path = os.path.abspath(path)#.decode(util_path.FILE_ENCODING)
        
#         print("  abs >", path)
        if os.path.exists(path):
            path = path
        else:
#             print(path, "n'existe pas !")
            try:
                path = os.path.join(pathdoc, path)
            except UnicodeDecodeError:
                pathdoc = toFileEncoding(pathdoc)
                path = os.path.join(pathdoc, path)
        
        
        os.chdir(cwd)
        return path
    
    
    ######################################################################################  
    def GetRelPath(self, pathdoc, path = None):
        """ Renvoie le chemin relatif du lien
            grace au chemin du document <pathdoc>
        """
        if path == None:
            path = self.path
            
        if self.type != 'f' and self.type != 'd':
            return path
        
#        path = self.GetEncode(path)
        if os.path.exists(path):
            path = path
        else:
            try:
                path = os.path.join(pathdoc, path)
            except UnicodeDecodeError:
                pathdoc = toFileEncoding(pathdoc)
                path = os.path.join(pathdoc, path)
        return path
    
    
    ######################################################################################  
    def getBranche(self, branche):
        branche.set("Lien", toSystemEncoding(os.path.normpath(self.path)))
        branche.set("TypeLien", self.type)
        
        
    ######################################################################################  
    def setBranche(self, branche, pathdoc):
        self.path = toFileEncoding(branche.get("Lien", r""))
        self.path = os.path.normpath(self.path)
        self.type = branche.get("TypeLien", "")
        if self.type == "" and self.path != r"":
            self.EvalTypeLien(pathdoc)
        return True




##########################################################################################################
#
#  Dialogue de s�lection d'URL
#
##########################################################################################################
class URLDialog(wx.Dialog):
    def __init__(self, parent, lien, pathref):
        wx.Dialog.__init__(self, parent, -1, "S�lection de lien")
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
#         self.Create(parent, -1,  "S�lection de lien")

        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "S�lectionner un fichier, un dossier ou une URL")
        label.SetHelpText("S�lectionner un fichier, un dossier ou une URL")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Lien :")
#        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        url = URLSelectorCombo(self, lien, pathref)
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



####################################################################################
#
#   Evenement perso pour détecter une modification du chemin
#
####################################################################################
myEVT_PATH_MODIFIED = wx.NewEventType()
EVT_PATH_MODIFIED = wx.PyEventBinder(myEVT_PATH_MODIFIED, 1)

#----------------------------------------------------------------------
class PathEvent(wx.PyCommandEvent):
    def __init__(self, evtType, idd):
        wx.PyCommandEvent.__init__(self, evtType, idd)
        self.lien = None

    ######################################################################################  
    def SetPath(self, lien):
        self.lien = lien
        
    ######################################################################################  
    def GetPath(self):
        return self.lien
    
    



####################################################################################
#
#   Widget pour sélectionner un lien
#
####################################################################################
class URLSelectorCombo(wx.Panel):
    def __init__(self, parent, lien, pathref, dossier = True, ext = ""):
        """
            lien : type Lien
            pathref : chemin du dossier de référence (pour chemins relatifs)
            dossier : bool pour spécifier que le lien est un dossier
            ext : 
        """
#         print "init URLSelectorCombo", pathref
        
        wx.Panel.__init__(self, parent, -1)
        self.SetMaxSize((-1,22*SSCALE))
        
        self.ext = ext
        self.dossier = dossier
        self.lien = lien
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        lsizer = self.CreateSelector()
        self.SetToolTipTexte()
        sizer.Add(lsizer, 1, flag = wx.EXPAND)
        self.SetSizerAndFit(sizer)
        
        self.SetPathSeq(pathref)

    
    #########################################################################################################
    def sendEvent(self):
#         print("sendEvent", modif, draw, verif)
        evt = PathEvent(myEVT_PATH_MODIFIED, self.GetId())
        evt.SetPath(self.lien)
        self.GetEventHandler().ProcessEvent(evt)
        
        
    ###############################################################################################
    def SetToolTipTexte(self):
        if self.lien.ok and self.lien.path != "":
            self.texte.SetToolTip(self.lien.path)
        else:
            self.texte.SetToolTip("Saisir un nom de fichier/dossier ou un URL\nou faire glisser un fichier")
    
    
    ###############################################################################################
    def CreateSelector(self):
        # Passage momentan� en Anglais (bug de wxpython)
#         locale2EN()
#         loc = wx.GetApp().locale.GetSystemLanguage()
#         wx.GetApp().locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        bsize = (16*SSCALE, 16*SSCALE)
        
        self.texte = wx.TextCtrl(self, -1, toSystemEncoding(self.lien.path), size = (-1, bsize[1]))
        self.SetToolTipTexte()
        
        if self.dossier:
#             bt1 =wx.BitmapButton(self, 100, wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, bsize))
            bt1 =wx.BitmapButton(self, 100, scaleImage(images.Icone_folder.GetBitmap(), *bsize))
            bt1.SetToolTip("Sélectionner un dossier")
            self.Bind(wx.EVT_BUTTON, self.OnClick, bt1)
            self.bt1 = bt1
            sizer.Add(bt1)
#         bt2 =wx.BitmapButton(self, 101, images.wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, bsize))
        
        bt2 =wx.BitmapButton(self, 101, scaleImage(images.Icone_fichier.GetBitmap(), *bsize))
        bt2.SetToolTip("Sélectionner un fichier")
        self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.texte)
        self.bt2 = bt2
        
        sizer.Add(bt2)
        sizer.Add(self.texte,1,flag = wx.EXPAND)
        
#         self.btnlien = wx.BitmapButton(self, -1, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, bsize))
        self.btnlien = wx.BitmapButton(self, -1, scaleImage(images.Icone_open.GetBitmap(), *bsize))
        self.btnlien.SetToolTip("Ouvrir le lien externe")
        self.btnlien.Show(self.lien.path != "")
        self.Bind(wx.EVT_BUTTON, self.OnClickLien, self.btnlien)
        sizer.Add(self.btnlien)
         
        
        # Pour drag&drop direct de fichiers !! (exp�rimental)
        file_drop_target = MyFileDropTarget(self)
        self.SetDropTarget(file_drop_target)
        
#         locale2def()
#         wx.GetApp().locale = wx.Locale(loc)
        
        return sizer
    
    
    #############################################################################            
    def OnClickLien(self, event):
        self.lien.Afficher(self.pathref)


    ###############################################################################################
    # Overridden from ComboCtrl, called when the combo button is clicked
    def OnClick(self, event):
        
        if event.GetId() == 100:
            dlg = wx.DirDialog(self, "Sélectionner un dossier",
                          style=wx.DD_DEFAULT_STYLE,
                          defaultPath = toSystemEncoding(self.pathref)
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
            if dlg.ShowModal() == wx.ID_OK:
                self.SetPath(dlg.GetPath(), 'd', marquerModifier = True)
    
            dlg.Destroy()
            
        else:
            dlg = wx.FileDialog(self, "Sélectionner un fichier",
                                wildcard = self.ext,
                                defaultDir = toSystemEncoding(self.pathref),
    #                           defaultPath = globdef.DOSSIER_EXEMPLES,
                               style = wx.DD_DEFAULT_STYLE
                               #| wx.DD_DIR_MUST_EXIST
                               #| wx.DD_CHANGE_DIR
                               )
    
            if dlg.ShowModal() == wx.ID_OK:
                self.SetPath(dlg.GetPath(), 'f', marquerModifier = True)
    
            dlg.Destroy()
        
        self.MiseAJour()
        
        self.SetFocus()


    ###############################################################################################
    def Enable(self, etat):
        self.texte.Enable(etat)
        self.bt2.Enable(etat)
        if hasattr(self, "bt1"):
            self.bt1.Enable(etat)
        
        
    ###############################################################################################
    def MiseAJour(self):
#         self.btnlien.Show(self.lien.path != "")
        self.marquerValid()
        self.SetToolTipTexte()


    ###############################################################################################
    def dropFiles(self, file_list):
        for path in file_list:
            self.SetPath(path, 'f', marquerModifier = True)
            return
            
    ##########################################################################################
    def EvtText(self, event):
#         self.lien.EvalLien(event.GetString(), self.pathref)
#         if not self.lien.ok:
#             self.lien.EvalTypeLien(self.pathref)
        self.SetPath(event.GetString(), marquerModifier = True)


    ##########################################################################################
    def GetPath(self):
        return self.lien
    
    
    ##########################################################################################
    def SetPath(self, lien = None, typ = None, marquerModifier = False):
        """ lien doit être de type 'String' encodé en SYSTEM_ENCODING
            
        """
        print("SetPath", lien)
#         print "   ", lien, typ
        if lien is not None:
            self.lien.path = lien
            self.lien.EvalLien(lien, self.pathref)
        
        try:
            self.texte.ChangeValue(self.lien.path)
        except: # Ca ne devrait pas arriver ... et pourtant �a arrive !
            self.lien.path = self.lien.path.decode(FILE_ENCODING)
#             self.lien.path = self.lien.path.encode(SYSTEM_ENCODING)
            self.texte.ChangeValue(toSystemEncoding(self.lien.path)) # On le met en SYSTEM_ENCODING
        
        
        self.MiseAJour()
        
        if marquerModifier:
            self.sendEvent()
        
        
#         if hasattr(self.Parent, 'GetPanelRacine'):
#             self.Parent.GetPanelRacine().OnPathModified(self.lien, marquerModifier = marquerModifier)
        
        
    ##########################################################################################
    def SetPathSeq(self, pathref):
        self.pathref = pathref

    
    ##########################################################################################
    def marquerValid(self):
        if self.lien.ok:
            self.texte.SetBackgroundColour(
                 wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            self.btnlien.SetToolTip("Ouvrir le lien externe")
            
        else:
            self.texte.SetBackgroundColour("pink")
            self.texte.SetFocus()
            self.btnlien.SetToolTip("Le lien est invalide")
        
        self.btnlien.Enable(self.lien.ok)
        self.Refresh()
        
        
