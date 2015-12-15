#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

##This file is part of pyXorga
#############################################################################
#############################################################################
##                                                                         ##
##                                  pyXorga                                ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014 Cédrick FAURY

#    pyXorga is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
    
#    pyXorga is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyXorga; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
pyXorga.py
Organiser ses fichiers à l'aide de Xmind
*************
Copyright (C) 2014 - 2015
@author: Cedrick FAURY

"""



import version
####################################################################################
#
#   Import des modules nécessaires
#
####################################################################################
# GUI wxpython
import wx

# sdk
import xmind
from xmind.core import workbook,saver, loader
from xmind.core.markerref import MarkerId, MarkerRefElement
from xmind.core.topic import TopicElement
from xmind import utils

import Images
import subprocess
# mekk
#from mekk.xmind import XMindDocument

import sys
import os
import os.path 
import glob
import ConfigParser
import shutil
import codecs

print "defaultencoding", sys.getdefaultencoding()
print "stdin, stdout", sys.stdin.encoding,sys.stdout.encoding

if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf8')
else:
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('utf-8')

FILE_ENCODING = sys.getfilesystemencoding() #'cp1252'#

SYSTEM_ENCODING = sys.getdefaultencoding()#sys.stdout.encoding#
print "FILE_ENCODING", FILE_ENCODING
print "SYSTEM_ENCODING", SYSTEM_ENCODING
   
######################################################################################  
def toSystemEncoding(path): 
#        try:
    path = path.decode(FILE_ENCODING)
    path = path.encode(SYSTEM_ENCODING)
    return path  
#        except:
#            return self.path    
    
######################################################################################  
def toFileEncoding(path):
#    try:
    path = path.decode(SYSTEM_ENCODING)
    return path.encode(FILE_ENCODING)
#    except:
#        return path

from util_path import *


# Fichiers CFG "originaux"
FICHIER_TYPES_ORG = os.path.join(PATH, toFileEncoding("Types.cfg"))

# Fichiers CFG("commun" ou bien "utilisateur" selon le choix fait à l'installation)
FICHIER_TYPES = os.path.join(APP_DATA_PATH, toFileEncoding("Types.cfg"))

## Fichiers CFG "utilisateurs"
FICHIER_CFG_USER = os.path.join(APP_DATA_PATH_USER, toFileEncoding("pyXorga.cfg"))
#FICHIER_TYPES_USER = os.path.join(APP_DATA_PATH_USER, toFileEncoding("Types.cfg"))


#######################################################################################################
#   Paramètres par défaut
#######################################################################################################
EXCLURE_DIR = [u""]
INCLURE_DIR = [u"*"]

INCLURE_FIC = [u"*"]
EXCLURE_FIC = [u""]

INCLURE_TYP = [u"C"]
EXCLURE_TYP = [u"*"]

FILTRER_TYP = True

DOSSIER = u""
FICHIER = u""

EXCLURE_DOSSIERS_VIDE = True
STRUCTURE  = 'structure-class="org.xmind.ui.logic.right"'

MARQUEUR_DOSSIER = "Dossier"
#MarqueurIDDossier = MarkerId(MARQUEUR_DOSSIER)

MarqueurDossier = MarkerRefElement()
MarqueurDossier.setMarkerId(MARQUEUR_DOSSIER)



def utf8decode(s):
    s = s.encode("iso-8859-1")
    return s.decode("utf-8")


def listdirectory2(path):  
    fichier=[]  
    for root, dirs, files in os.walk(path):  
        for i in files:  
            fichier.append(os.path.join(root, i))  
    return fichier




#
def GetTypeNom(nFich):
    """    Renvoie le type et le nom du document
        nFich  : String encodé en SYSTEM_ENCODING
    """
    parties = nFich.split(SEPARATEUR)
    if len(parties) > 1:
        for t in TYPES.keys():
            if parties[0] == t:
                return t, parties[1]
    return None, nFich


def GetType(nFich):
    """    Renvoie le type du document
        nFich  : String encodé en SYSTEM_ENCODING
    """
    parties = nFich.split(SEPARATEUR)
    if len(parties) > 1:
        for t in TYPES.keys():
            if parties[0] == t:
                return t
    return None


def GetNomSimple(file, typ):
    return os.path.splitext(file[len(TYPES[typ][0]):])[0]
    



#################################################################################################
#
#   Gestion du fichier de configuration
#
#################################################################################################
SECTION_FICH = u"FichierDossiers"
SECTION_FILTRE = u"Filtres"


    
    
#listdirectory(INPUT_DIR, root_topic)

#
#root_topic.add_subtopic(u"First item")
#root_topic.add_subtopic(u"Second item")
#t = root_topic.add_subtopic(u"Third item")
#t.add_subtopic(u"Second level - 1")
#t.add_subtopic(u"Second level - 2")
#root_topic.add_subtopic(u"Detached topic", detached = True)
#t.add_subtopic(u"Another detached", detached = True)
#t.add_marker("flag-red")
#root_topic.add_subtopic(u"Link example").set_link("http://mekk.waw.pl")
##root_topic.add_subtopic(u"Attachment example").set_attachment(
##    file("map_creator.py").read(), ".txt")
#root_topic.add_subtopic(u"With note").set_note(u"""This is just some dummy note.""")

#MARKER_CODE = "40g6170ftul9bo17p1r31nqk2a"
#XMP = "../../py_mekk_nozbe2xmind/src/mekk/nozbe2xmind/NozbeIconsMarkerPackage.xmp"
#root_topic.add_subtopic(u"With non-standard marker").add_marker(MARKER_CODE)
#
#xmind.embed_markers(XMP)

#

#xmind.pretty_print()



####################################################################################
#
#   Classe définissant l'application
#    --> récupération des paramétres passés en ligne de commande
#
####################################################################################
#from asyncore import dispatcher, loop
#import sys, time, socket, threading

#class SeqApp(wx.App):
#    def OnInit(self):
#        wx.Log.SetLogLevel(0) # ?? Pour éviter le plantage de wxpython 3.0 avec Win XP pro ???
#        
##########################################################################################
def fcount(path):
    count1 = 0
    for root, dirs, files in os.walk(path):
        count1 += len(dirs)

    return count1


##########################################################################################
def getListNomGlob(path, liste):
    """ Renvoie la liste des fichiers
        
    """
    os.chdir(path)
    
    l = []
    for f in liste:
        l.extend(glob.glob(f))
#        l = [f.encode(FILE_ENCODING) for f in l]
    return l


##########################################################################################
def estInclus(dossier1, dossier2):
    """ Vérifie si dossier1 est un sous-dossier de dossier2
    """
#    print "estInclus : "
#    print "  ", dossier1
#    print "  ", dossier2
#    print "  ", dossier1[:len(dossier2)]
    if len(dossier1) < len(dossier2):
        return False
    return dossier1[:len(dossier2)] == dossier2



class FilterNB(wx.Notebook):
    def __init__(self, parent, app, exclure_Dir , inclure_Dir,
                     exclure_Fic, inclure_Fic, 
                     exclure_Typ, inclure_Typ,
                     filtrerTypes):
        
        wx.Notebook.__init__(self, parent, -1, size=(21,21), style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )

        self.winDossiers = PanelInclureExclure(self, app, "D", inclure_Dir, exclure_Dir)
        self.AddPage(self.winDossiers, "Dossiers")
#        self.exclure_D = winDossiers.exclure
#        self.inclure_D = winDossiers.inclure

        # Show how to put an image on one of the notebook tabs,
        # first make the image list:
#        il = wx.ImageList(16, 16)
#        idx1 = il.Add(images.Smiles.GetBitmap())
#        self.AssignImageList(il)

        # now put an image on the first tab we just created:
#        self.SetPageImage(0, idx1)


        self.winExtensions = PanelInclureExclure(self, app, "F", inclure_Fic, exclure_Fic)
        self.AddPage(self.winExtensions, u"Fichiers")
#        self.exclure_F = winExtensions.exclure
#        self.inclure_F = winExtensions.inclure
        
        
        self.winTypes = PanelInclureExclureTypes(self, app, inclure_Typ, exclure_Typ, filtrerTypes)
        self.AddPage(self.winTypes, u"Types")
#        self.exclure_T = winTypes.exclure
#        self.inclure_T = winTypes.inclure

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
            
            
    def OnPageChanged(self, event):
#        old = event.GetOldSelection()
#        new = event.GetSelection()
#        sel = self.GetSelection()
#        self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def OnPageChanging(self, event):
#        old = event.GetOldSelection()
#        new = event.GetSelection()
#        sel = self.GetSelection()
#        self.log.write('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()
        
        
        
        
class pyXorgFrame(wx.Frame):
    def __init__(self, nomFichier = None):
        wx.Frame.__init__(self, None, -1, "pyXorga" + version.__version__, size = (400,600))
        p = wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
                     | wx.CLIP_CHILDREN
                     | wx.FULL_REPAINT_ON_RESIZE
                     )

        self.SetIcon(wx.Icon(os.path.join(PATH, r"pyXorga_icone.ico"), wx.BITMAP_TYPE_ICO))
        
        self.exclure_Dir = EXCLURE_DIR
        self.inclure_Dir = INCLURE_DIR
        self.exclure_Fic = EXCLURE_FIC
        self.inclure_Fic = INCLURE_FIC
        self.exclure_Typ = EXCLURE_TYP
        self.inclure_Typ = INCLURE_TYP
        self.filtrerTypes = FILTRER_TYP
        self.ouvrirCFG()
        
        
        #
        # Variables
        #
        self.nomFichier = FICHIER
        self.dossier =  DOSSIER
        self.dossierSortie = u""
        self.titreCarte = u""
        if nomFichier != None:
            # Un dossier est passé en argument
            self.dossier =  nomFichier
            self.nomFichier = os.path.join(self.dossier, os.path.split(self.dossier)[1] + toFileEncoding(".xmind"))
            if len(os.path.split(self.dossier)[1]) > 0:
                self.dossierSortie = os.path.split(self.dossier)[0]
            self.titreCarte = os.path.splitext(os.path.split(self.dossier)[1])[0]
        
        self.ajouterCarteMentale = True
        
        self.ouvrirTypes()

        
        #
        # Dossier à traiter
        #
        box = wx.StaticBox(p, -1, u"Dossier à traiter")
        bsizerd = wx.StaticBoxSizer(box, wx.VERTICAL)

        c = URLSelectorCombo(p, self, self.dossier, "D")
        self.selecteur_D = c
        bsizerd.Add(c, 0, wx.ALL|wx.EXPAND, 5)


        #
        # Sorties
        #
        box = wx.StaticBox(p, -1, u"Structure de sortie")
        bsizerxs = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        st = wx.StaticText(p, -1, u"Nom de la racine")
        ct = self.ctrlTitre = wx.TextCtrl(p, -1, self.titreCarte)
        self.Bind(wx.EVT_TEXT, self.EvtText, ct)
        
        #
        # Fichier Xmind de sortie
        #
        box = wx.StaticBox(p, -1, u"Carte mentale XMind du Dossier à traiter")
        bsizerx = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        c = URLSelectorCombo(p, self,  self.nomFichier, "F")
        bsizerx.Add(c, 1, wx.ALL|wx.EXPAND, 5)
        self.selecteur_F = c
        
        b = self.boutonGenererXMind = wx.Button(p, -1, u"Générer\nla carte", (20, 80)) 
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        self.boutonGenererXMind.Enable(self.nomFichier != u"")
        b.SetToolTipString(u"Générer une carte mentale XMind de la structure")
        bsizerx.Add(b, 0, wx.ALL|wx.EXPAND, 5)
        
        b = self.boutonOuvrirXMind = wx.BitmapButton(p, -1, Images.LogoXMind.GetBitmap())
        self.boutonOuvrirXMind.Enable(os.path.exists(self.nomFichier))
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        b.SetToolTipString(u"Ouvrir la carte mentale générée (XMind nécessaire)")
        bsizerx.Add(b, 0, wx.ALL|wx.EXPAND, 5)
        
        #
        # Dossier de sortie
        #
        box = wx.StaticBox(p, -1, u"Copie filtrée du Dossier à traiter")
        bsizers = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        vs = wx.BoxSizer(wx.VERTICAL)
        
        t = wx.StaticText(p, -1, u"Emplacement du dossier :")
        vs.Add(t, 0, wx.ALL|wx.EXPAND, 2)
        c = URLSelectorCombo(p, self,  self.dossierSortie, "D")
        self.selecteur_DS = c
        vs.Add(c, 1, wx.ALL|wx.EXPAND, 2)
        
        cb = wx.CheckBox(p, -1, u"Ajouter une Carte mentale")
        cb.SetValue(self.ajouterCarteMentale)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
        cb.SetToolTipString(u"Générer une carte mentale à la racine du dossier")
        vs.Add(cb, 1, wx.ALL|wx.EXPAND, 2)
        bsizers.Add(vs, 1, wx.ALL|wx.EXPAND, 5)
        
        b = self.boutonGenererClone = wx.Button(p, -1, u"Générer\ndossier", (20, 80)) 
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        self.boutonGenererClone.Enable(self.testerValiditeClone())
        b.SetToolTipString(u"Générer une arborescence de fichiers de la structure")
        bsizers.Add(b, 0, wx.ALL|wx.EXPAND, 5)
        
        
        b = self.boutonOuvrirDossier = wx.BitmapButton(p, -1, wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (42, 42)))
        self.boutonOuvrirDossier.Enable(os.path.exists(self.dossierSortie))
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        b.SetToolTipString(u"Ouvrir le dossier généré")
        bsizers.Add(b, 0, wx.ALL|wx.EXPAND, 5)
        
        
        #
        # Filtres
        #
        box =  wx.StaticBox(p, -1, u"Filtres")
        bsizerf = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.FilterNB = FilterNB(p, self, self.exclure_Dir , self.inclure_Dir,
                     self.exclure_Fic, self.inclure_Fic, 
                     self.exclure_Typ, self.inclure_Typ,
                     self.filtrerTypes)
        bsizerf.Add(self.FilterNB, 1, wx.ALL|wx.EXPAND, 5)
        
        
        #
        # Mise en place
        #
        bsizerxs.Add(st, 0, wx.ALL|wx.EXPAND, 5)
        bsizerxs.Add(self.ctrlTitre, 0, wx.ALL|wx.EXPAND, 5)
        bsizerxs.Add(bsizerx, 0, wx.ALL|wx.EXPAND, 5)
        bsizerxs.Add(bsizers, 0, wx.ALL|wx.EXPAND, 5)
        bsizerxs.Add(bsizerf, 1, wx.ALL|wx.EXPAND, 5)
        
        gbs = self.gbs = wx.GridBagSizer(5, 5)
        gbs.Add( bsizerd, (0,0), (1,1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        gbs.Add( bsizerxs, (1,0), (1,1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
#        gbs.Add( bsizers, (2,0), (1,1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
#        gbs.Add( bsizerf, (3,0), (1,1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)

        gbs.AddGrowableRow(1)
        gbs.AddGrowableCol(0)

        box = wx.BoxSizer()
        box.Add(gbs, 1, wx.ALL|wx.EXPAND, 5)
        p.SetSizerAndFit(box)
        
        self.SetMinSize((400, 600))
        self.SetClientSize(p.GetBestSize())
        
        # Interception de la demande de fermeture
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.selecteur_D.SetPath(self.dossier)
        self.selecteur_F.SetPath(self.nomFichier)
        self.selecteur_DS.SetPath(self.dossierSortie)
        
        
    ##########################################################################################
    def EvtText(self, event):
        self.titreCarte = event.GetString()
        self.OnPathModified()
        
        
    ##########################################################################################
    def EvtCheckBox(self, event):
        self.ajouterCarteMentale = event.IsChecked()
        
        
    
    ##########################################################################################
    def testerDossierExistant(self):
        print "testerDossierExistant"
        
        os.chdir(self.dossierSortie)
        d = os.path.join(self.dossierSortie, self.titreCarte)
        while os.path.exists(d) and len(os.listdir(d)) > 0:
            os.chdir(d)
            dlg = wx.MessageDialog(self, u"Le dossier suivant existe déja, et n'est pas vide !\n\n\n" \
                                         u"%s\n\n"\
                                         u"Voulez-vous effacer son contenu ?\n" %os.path.join(self.dossierSortie, self.titreCarte),
                                         u'Dossier existant et non vide',
                                         wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                         )
            retCode = dlg.ShowModal()
            dlg.Destroy() 
            if retCode == wx.ID_YES:
                os.chdir(d)
                for f in os.listdir(d):
                    if os.path.isdir(f):
                        shutil.rmtree(f, ignore_errors = False, onerror=onerror)
                    else:
                        os.remove(f)
                os.chdir(d)
            elif retCode == wx.ID_NO:
                return False
            else:
                return False
        
        return True
    
    
    ##########################################################################################
    def OnClick(self, event):
        if event.GetEventObject() == self.boutonOuvrirXMind:
            try:
                os.startfile(self.nomFichier)
#            subprocess.Popen(["xmind", self.nomFichier])
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'accéder au fichier\n\n%s\n" %toSystemEncoding(self.nomFichier))
    
    
    
    

        #####################################################################################################################
        elif event.GetEventObject() == self.boutonOuvrirDossier:
            try:
                os.startfile(os.path.join(self.dossierSortie, self.titreCarte))
#            subprocess.Popen(["xmind", self.nomFichier])
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'accéder au dossier\n\n%s\n" %toSystemEncoding(self.dossierSortie))
    
    
    
    
        #####################################################################################################################
        elif event.GetEventObject() == self.boutonGenererXMind:
            
            if os.path.splitext(self.nomFichier)[1].lower() != ".xmind":
                self.nomFichier = os.path.splitext(self.nomFichier)[0] + ".xmind"
                
            if os.path.exists(self.nomFichier):
                dlg = wx.MessageDialog(self, u"La carte mentale %s existe déja !\n\n" \
                                             u"Voulez-vous l'écraser ?\n" %self.nomFichier,
                                             u'Carte existante',
                                             wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                             )
                retCode = dlg.ShowModal()
                dlg.Destroy() 
                if retCode == wx.ID_YES:
                    os.remove(self.nomFichier)
                elif retCode == wx.ID_NO:
                    return
                else:
                    return
            
#            
#            try:
#                self.dossier = unicode(self.dossier, DEFAUT_ENCODING)
#            except:
#                pass
            
            th = ThreadDossier(self, mode = 0)
            
            self.dlg =    ProgressFrame(None, -1, u"Génération de la carte", th)
            self.dlg.Show()
            th.SetDlg(self.dlg)
            th.start()


            


            
        #####################################################################################################################
        elif event.GetEventObject() == self.boutonGenererClone:

#            try:
#                self.dossierSortie = unicode(self.dossierSortie, DEFAUT_ENCODING)
#            except:
#                pass
#            
#            try:
#                self.dossier = unicode(self.dossier, DEFAUT_ENCODING)
#            except:
#                pass
            
            if self.testerDossierExistant():
                
                os.chdir(self.dossierSortie)
                if not os.path.exists(self.titreCarte):
                    os.mkdir(self.titreCarte)
                os.chdir(self.titreCarte)
                
                th = ThreadDossier(self, mode = 1)
                
                self.dlg = ProgressFrame(None, -1, u"Génération du dossier clone", th)
                self.dlg.Show()
                th.SetDlg(self.dlg)
                th.start()
                
            
            else:
                dlg = wx.MessageDialog(self, u"Le dossier cible n'existe pas !\n\n" + self.dossierSortie, 
                                       u"Dossier inexistant",
                               wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()   

            
    

    
    
    ##########################################################################################
    def getListeIE(self, IE, typ):
        return self.FilterNB.getListeIE(IE, typ)
            
            
            
#    ##########################################################################################
#    def creerCarte(self, nomFichier, titreCarte, dossier):
#        # Version sdk
#        if os.path.splitext(nomFichier)[1] != ".xmind":
#            nomFichier = os.path.splitext(nomFichier)[0] + ".xmind"
#        xm = xmind.load(nomFichier)
#        first_sheet = xm.getPrimarySheet() # get the first sheet
#        first_sheet.setTitle(titreCarte) # set its title
#        root_topic = first_sheet.getRootTopic() # get the root topic of this sheet
#        root_topic.setTitle(titreCarte) # set its title
#        root_topic.setAttribute("structure-class", "org.xmind.ui.logic.right")
#        # Version mekk
##        xmind = XMindDocument.create(titreCarte, titreCarte)
##        first_sheet = xmind.get_first_sheet()
##        root_topic = first_sheet.get_root_topic()
#
#        self.genererCarte(dossier, root_topic)
#        
#        # mekk
##        xmind.save(nomFichier)
#        
#        # sdk
#        xmind.save(xm, nomFichier) # and we save
#        
#        
#        
#    ##########################################################################################
#    def genererCarte(self, path, topic):
#        vide = True
#
#        if not os.path.exists(path) or len(path) > 255:
#            return
#
#        dirs = os.listdir(path)
##        print dirs
#        
#        for file in dirs:
#            
#            path_file = os.path.join(path, file)
#            
#            if os.path.isdir(path_file):
#                inclureD = getListNomGlob(path, self.inclure_Dir)
#                exclureD = getListNomGlob(path, self.exclure_Dir)
#                if not file in exclureD and file in inclureD:
#                    if len(os.listdir(path))>0:
#                        # mekk
##                        t = topic.add_subtopic(file)
#                        
#                        # sdk
#                        t = TopicElement()
#                        t.setTitle(file)
#                        t.addMarker("Folder.png")
#
#                        dv = self.genererCarte(path_file, t)
#                        
#                        if EXCLURE_DOSSIERS_VIDE and not dv:
#                            topic.addSubTopic(t)
#                            vide = False
##                    self.count += 1
#                    self.dlg.Augmenter()
#                else:
#                    self.dlg.Augmenter(fcount(path_file))
##                    self.count += fcount(path_file)
##                self.dlg.Augmenter()
#                
#                
#            else:
#                ext = os.path.splitext(file)[1]
#                typ, nom = GetTypeNom(file)
#                inclureF = getListNomGlob(path, self.inclure_Fic)
#                exclureF = getListNomGlob(path, self.exclure_Fic)
#                if not file in exclureF and file in inclureF and (typ in self.inclure_Typ or typ == None):
#                    # mekk
##                    t = topic.add_subtopic(GetNomSimple(file, typ))
##                    t.set_link(os.path.join(path, file))
##                    t.add_marker(TYPES[typ][1])
#                    
#                    # sdk
#                    t = TopicElement()
#                    if ext != "":
#                        tx = nom.split(ext)[0]
#                    else:
#                        tx = nom
#                    t.setTitle(tx)
##                    t.setFileHyperlink(os.path.join(path, file)) # set a file hyperlink
#                    
#                    t.setFileHyperlink("file://" + utils.get_abs_path(os.path.join(path, file)))
#                    if typ != None:
#                        t.addMarker(TYPES[typ][1])
#                    
#                    topic.addSubTopic(t)
#
#                    vide = False
#        return vide


#    ##########################################################################################
#    def genererDossier(self, path, sortie):
#        vide = True
#        try:
#            sortie = unicode(sortie, DEFAUT_ENCODING)
#        except:
#            pass
#        
#        if not os.path.exists(path) or len(path) > 255:
#            return
#        
#        dirs = os.listdir(path)
#
#        for file in dirs:  
#            path_file = os.path.join(path, file)
#
#            if os.path.isdir(path_file):
#                inclureD = getListNomGlob(path, self.inclure_Dir)
#                exclureD = getListNomGlob(path, self.exclure_Dir)
#                if not file in exclureD and file in inclureD:
#                    if len(os.listdir(path))>0:
#                        os.chdir(sortie)
#                        os.mkdir(file)
#                        dv = self.genererDossier(path_file, os.path.join(sortie, file))
#                        
#                        if EXCLURE_DOSSIERS_VIDE and not dv:
#                            vide = False
#                        else:
#                            os.chdir(sortie)
#                            os.rmdir(file)
#                    
#                    self.dlg.Augmenter()
#                    self.dlg.SetInfo(file)
#                else:
#                    self.dlg.Augmenter(fcount(path_file))
#                    self.dlg.SetInfo(file)
#                        
#            else:
#                ext = os.path.splitext(file)[1]
#                typ, nom = GetTypeNom(file)
#                inclureF = getListNomGlob(path, self.inclure_Fic)
#                exclureF = getListNomGlob(path, self.exclure_Fic)
#                if not file in exclureF and file in inclureF and (typ in self.inclure_Typ or typ == None):
#                    shutil.copy2(os.path.join(path, file), sortie)
#
#                    vide = False
#        return vide
    
    
    #############################################################################
    def OnPathModified(self, selecteur = None, lien = None):

        if hasattr(self, "selecteur_F") and selecteur == self.selecteur_F:
            self.nomFichier = lien
#            self.boutonOuvrirXMind.Enable(os.path.exists(self.nomFichier))
#            self.boutonGenererXMind.Enable(self.nomFichier != u"")

        elif hasattr(self, "selecteur_D") and selecteur == self.selecteur_D:
            self.dossier = lien
            self.ctrlTitre.SetValue(os.path.basename(self.dossier))
#            self.boutonGenererXMind.Enable(self.nomFichier != u"")
        
        elif hasattr(self, "selecteur_DS") and selecteur == self.selecteur_DS:
            self.dossierSortie = lien
#            if not estInclus(lien, self.dossier) or lien == u"":
#                
##                self.boutonGenererClone.Enable(self.dossierSortie != u"")
#            else:
#                self.selecteur_DS.marquerErreur(u"Le dossier de destination ne DOIT PAS être un sous dossier du dossier source !")
                
                
        #
        # Etat des boutons et des selecteurs
        #
        self.boutonOuvrirXMind.Enable(os.path.exists(self.nomFichier))
        self.boutonGenererXMind.Enable(self.nomFichier != u"")
        
        Ok = self.testerValiditeClone()
        
        self.boutonGenererClone.Enable(Ok)
        
        self.Refresh()


    #############################################################################
    def testerValiditeClone(self):
        """ Vérifie que le dossier de clonage est valide
        """
        if samefile(os.path.join(self.dossierSortie, self.titreCarte), self.dossier):
            self.marquerConflit(True)
            return False
        else:
            self.marquerConflit(False)
            
        if not estInclus(self.dossierSortie, self.dossier):
            if self.dossierSortie == u"":
                self.selecteur_DS.marquerErreur(u"Nom de dossier non valide")
                return False
            else:
                self.selecteur_DS.marquerErreur()
        else:
            self.selecteur_DS.marquerErreur(u"Le dossier de destination ne DOIT PAS être un sous dossier du dossier source !")
            return False
        
        return True


    #############################################################################
    def marquerConflit(self, conflit):
        if conflit:
            txt = u"Le nom du dossier copié est identique au dossier source !\n" \
                  u"Modifier l'emplacement du dossier ou le nom de la racine"
            self.selecteur_DS.marquerErreur(txt)
            self.ctrlTitre.SetBackgroundColour(("pink"))
            self.ctrlTitre.SetToolTipString(txt)
        else:
            self.selecteur_DS.marquerErreur()
            self.ctrlTitre.SetBackgroundColour(("white"))
            self.ctrlTitre.SetToolTipString(u"")
        
        
    #############################################################################
    def MiseAJourFiltres(self, inc, exc = None, typ = "D"):
        if typ == "D":
            self.exclure_Dir = exc
            self.inclure_Dir = inc
        elif typ == "F":
            self.exclure_Fic = exc
            self.inclure_Fic = inc
        elif typ == "T":
            self.exclure_Typ = exc
            self.inclure_Typ = inc
        elif typ == None:
            self.filtrerTypes = inc
    
    #############################################################################
    def OnClose(self, evt):
        self.enregistrerCFG()
        evt.Skip()
        sys.exit()
    
    
    
    #############################################################################
    def ouvrirCFG(self):    
        if not os.path.isfile(FICHIER_CFG_USER):
            return
        config = ConfigParser.ConfigParser()
        
        config.readfp(codecs.open(FICHIER_CFG_USER, "r", "utf8"))
        
        try:
            self.dossier = config.get(SECTION_FICH, "Dossier", u"")
        except:
            pass
        
        try:
            self.dossierSortie = config.get(SECTION_FICH, "DossierSortie", u"")
        except:
            pass
        
        try:
            self.nomFichier = config.get(SECTION_FICH, "Fichier", u"")
        except:
            pass
        
        try:
            self.titreCarte = config.get(SECTION_FICH, "Titre", u"")
        except:
            pass
        
        try:
            self.exclure_Dir = config.get(SECTION_FILTRE, "Exclure_Dir").split("\t")
        except:
            pass
        try:
            self.inclure_Dir = config.get(SECTION_FILTRE, "Inclure_Dir").split("\t")
        except:
            pass
        try:    
            self.exclure_Fic = config.get(SECTION_FILTRE, "Exclure_Fic").split("\t")
        except:
            pass
        try:
            self.inclure_Fic = config.get(SECTION_FILTRE, "Inclure_Fic").split("\t")
        except:
            pass
        try:
            self.exclure_Typ = config.get(SECTION_FILTRE, "Exclure_Typ").split("\t")
        except:
            pass
        try:
            self.inclure_Typ = config.get(SECTION_FILTRE, "Inclure_Typ").split("\t")
        except:
            pass
       
        try:
            self.filtrerTypes = config.getboolean(SECTION_FILTRE, "Filtrer_Typ")
        except:
            pass
        

    #############################################################################
    def ouvrirTypes(self):
        global SEPARATEUR, TYPES
        
        if not os.path.isfile(FICHIER_TYPES):
            if os.path.isfile(FICHIER_TYPES_ORG):
                import shutil
                shutil.copy(FICHIER_TYPES_ORG, FICHIER_TYPES)
            else:
                print "Fichier original", FICHIER_TYPES_ORG, "non trouvé"
                TYPES = {}
                SEPARATEUR = "_"
                return
                
        if not os.path.isfile(FICHIER_TYPES):
            print "Fichier", FICHIER_TYPES, "non trouvé"
            TYPES = {}
            SEPARATEUR = "_"
            return
        
        
            
        
        config = ConfigParser.ConfigParser()
        config.readfp(codecs.open(FICHIER_TYPES, "r", SYSTEM_ENCODING))
        
#        config.read(FICHIER_TYPES)
        SEPARATEUR = config.get("Format", "Separateur", u"")[1:-1]
        TYPES = {}
        
        i = 1
        continuer = True
        while continuer:
            try :
                t = config.get("Types", "T"+str(i))
                p, n, f = t.split("#")
                TYPES[p] = [n, f]
                i += 1
            except:
                continuer = False

        
    #############################################################################
    def enregistrerCFG(self):
        config = ConfigParser.ConfigParser()
        
    
        config.add_section(SECTION_FICH)
        config.set(SECTION_FICH, "Dossier", self.dossier)
        config.set(SECTION_FICH, "Fichier", self.nomFichier)
        config.set(SECTION_FICH, "DossierSortie", self.dossierSortie)
        config.set(SECTION_FICH, "Titre", self.titreCarte)
    
        config.add_section(SECTION_FILTRE)
        config.set(SECTION_FILTRE, "Exclure_Dir", "\t".join(self.exclure_Dir))
        config.set(SECTION_FILTRE, "Inclure_Dir", "\t".join(self.inclure_Dir))
        config.set(SECTION_FILTRE, "Exclure_Fic", "\t".join(self.exclure_Fic))
        config.set(SECTION_FILTRE, "Inclure_Fic", "\t".join(self.inclure_Fic))
        config.set(SECTION_FILTRE, "Exclure_Typ", "\t".join(self.exclure_Typ))
        config.set(SECTION_FILTRE, "Inclure_Typ", "\t".join(self.inclure_Typ))
        config.set(SECTION_FILTRE, "Filtrer_Typ", self.filtrerTypes)
        
        config.write(open(FICHIER_CFG_USER,'w'))
    
    

class URLSelectorCombo(wx.Panel):
    def __init__(self, parent, app, lien = "", typ = "D", ext = ""):
        wx.Panel.__init__(self, parent, -1)
        
        self.app = app
        
        self.SetMaxSize((-1,22))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.texte = wx.TextCtrl(self, -1, lien, size = (-1, 16))
        
        if typ == "D":
            bt1 =wx.BitmapButton(self, 100, wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
            bt1.SetToolTipString(u"Sélectionner un dossier")
            self.Bind(wx.EVT_BUTTON, self.OnClick, bt1)
            self.Bind(wx.EVT_TEXT, self.EvtText, self.texte)
            sizer.Add(bt1)
        elif typ == "F":
            bt2 =wx.BitmapButton(self, 101, wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))
            bt2.SetToolTipString(u"Sélectionner un fichier")
            self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
            self.Bind(wx.EVT_TEXT, self.EvtText, self.texte)
            sizer.Add(bt2)
            
        self.ext = u"Xmind (.xmind)|*.xmind|" \
                       u"Tous les fichiers|*.*'"
        self.typ = typ
        
        sizer.Add(self.texte,1,flag = wx.EXPAND)
        self.SetSizerAndFit(sizer)
#        self.SetPath(lien)
#        self.lien = lien
     

    # Overridden from ComboCtrl, called when the combo button is clicked
    def OnClick(self, event):
#        print "OnClick"
        if event.GetId() == 100:
            dlg = wx.DirDialog(self, u"Sélectionner un dossier",
                          style=wx.DD_DEFAULT_STYLE,
                          defaultPath = self.lien
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
            if dlg.ShowModal() == wx.ID_OK:
#                print "   ", dlg.GetPath()
                self.SetPath(dlg.GetPath())
            dlg.Destroy()
            
        else:
            dlg = wx.FileDialog(self, u"Sélectionner un fichier",
                                wildcard = self.ext,
    #                           defaultPath = globdef.DOSSIER_EXEMPLES,
                               style = wx.DD_DEFAULT_STYLE
                               #| wx.DD_DIR_MUST_EXIST
                               #| wx.DD_CHANGE_DIR
                               )
            if dlg.ShowModal() == wx.ID_OK:
                self.SetPath(dlg.GetPath())
            dlg.Destroy()
        
        self.SetFocus()


    ##########################################################################################
    def EvtText(self, event):
        self.SetPath(event.GetString())


    ##########################################################################################
    def GetPath(self):
        return self.lien
    
    
    ##########################################################################################
    def SetPath(self, lien):
        """ lien doit être de type 'String'  encodé en SYSTEM_ENCODING
        """
#        print "SetPath",self.typ, lien
        if self.typ == "D":
            if os.path.exists(lien) and os.path.isdir(lien):
                self.texte.ChangeValue(lien) # On le met en DEFAUT_ENCODING
                self.lien = lien
                self.marquerErreur()
                
            else:
                self.marquerErreur(lien + u" n'est pas un dossier valide !")
                self.lien = u""
        else:
            self.texte.ChangeValue(lien)
            self.lien = lien
            
        self.app.OnPathModified(self, self.lien)
        self.Refresh()
    
    
    ##########################################################################################
    def marquerErreur(self, message = None):
        if message != None:
            self.texte.SetBackgroundColour(("pink"))
            self.texte.SetToolTipString(message)
        else:
            self.texte.SetBackgroundColour(("white"))
            self.texte.SetToolTipString(u"")
            
            
    ##########################################################################################
    def SetToolTipString(self, s):
        self.texte.SetToolTipString(s)
        
        
        
        
        
import  wx.lib.scrolledpanel as scrolled
class PanelInclureExclureTypes(scrolled.ScrolledPanel):
    def __init__(self, parent, app, inclure = [], exclure = [],
                 filtrerTypes = False):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        self.SetupScrolling()
        
        self.app = app
        
        self.cbI = {}
        self.cbE = {}
        sizer = wx.GridBagSizer(5,2)
        
        cbF = wx.CheckBox(self, -1, u"Activer le filtrage par type")
        cbF.SetToolTipString(u"Permet de filter les fichiers selon des critères de type.\n" \
                             u"Si ce filtre est activé, seuls les fichiers \"typés\" seront sélectionnés.\n" \
                             u" => fichiers de la forme : 'préfixe' + 'séparateur' + 'suffixe'")
        self.cbF = cbF
        self.cbF.SetValue(filtrerTypes)
        
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxF, self.cbF)
        sizer.Add(self.cbF, (0, 0), (1,4), flag = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, border = 5)
        sizer.Add(wx.StaticLine(self, -1), (1, 0), (1,4), flag = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, border = 0)
        
        t = wx.StaticText(self, -1, u"Inclure")
        t.SetFont(FONT_IE)
        sizer.Add(t, (3, 0), flag = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, border = 5)
        t = wx.StaticText(self, -1, u"Exclure")
        t.SetFont(FONT_IE)
        sizer.Add(t, (3, 1), flag = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, border = 5)
        t = wx.StaticText(self, -1, u"Préfixe")
        t.SetFont(FONT_IE)
        sizer.Add(t, (3, 2), flag = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, border = 5)
        t = wx.StaticText(self, -1, u"Type de document")
        t.SetFont(FONT_IE)
        sizer.Add(t, (3, 3), flag = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, border = 5)
        
        tte = u"Selectionner tous les types de document"
        self.cbIt = wx.CheckBox(self, -1, u"")
        self.cbIt.SetToolTipString(tte)
        self.cbIt.SetValue(False)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.cbIt)
        
        self.cbEt = wx.CheckBox(self, -1, u"")
        self.cbEt.SetToolTipString(tte)
        self.cbEt.SetValue(False)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.cbEt)
        
        sizer.Add(self.cbIt, (2, 0), flag = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT|wx.TOP, border = 5)
        sizer.Add(self.cbEt, (2, 1), flag = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT|wx.TOP, border = 5)
        t = wx.StaticText(self, -1, u"Tous")
        t.SetToolTipString(tte)
        t.SetFont(FONT_ITALIC)
        sizer.Add(t, (2, 2), (1, 2), flag = wx.EXPAND|wx.LEFT|wx.TOP, border = 5)
        
        i = 4
        for p, nm in TYPES.items():
            self.cbI[p] = wx.CheckBox(self, -1, u"")
            self.cbI[p].SetValue(p in inclure)
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.cbI[p])
            
            self.cbE[p] = wx.CheckBox(self, -1, u"")
            self.cbE[p].SetValue(p in exclure)
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.cbE[p])
            
            sizer.Add(self.cbI[p], (i, 0), flag = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, border = 5)
            sizer.Add(self.cbE[p], (i, 1), flag = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, border = 5)
            sizer.Add(wx.StaticText(self, -1, p), (i, 2), flag = wx.EXPAND|wx.LEFT, border = 5)
            sizer.Add(wx.StaticText(self, -1, nm[0]), (i, 3), flag = wx.EXPAND|wx.LEFT, border = 5)
            
            i += 1
      
        self.EvtCheckBoxF()
        
        sizer.AddGrowableCol(3)
        self.SetSizer(sizer)
        
        
    ##########################################################################################
    def EvtCheckBox(self, event):
        if event.GetEventObject() == self.cbIt:
            for k in self.cbI.values():
                k.SetValue(event.IsChecked())
        elif event.GetEventObject() == self.cbEt:
            for k in self.cbE.values():
                k.SetValue(event.IsChecked())
        
        inclure = [k for k in self.cbI.keys() if self.cbI[k].IsChecked()]
        exclure = [k for k in self.cbE.keys() if self.cbE[k].IsChecked()]
       
        self.cbIt.SetValue(len(inclure) == len(self.cbI))
        self.cbEt.SetValue(len(exclure) == len(self.cbE))
        
        self.app.MiseAJourFiltres(inclure, exclure, typ = "T")
        
    ##########################################################################################
    def EvtCheckBoxF(self, event = None):
        filtrerTypes = self.cbF.GetValue()
        for k in self.cbI.values() + self.cbE.values():
            k.Enable(filtrerTypes)
        self.cbIt.Enable(filtrerTypes)
        self.cbEt.Enable(filtrerTypes)
        
        for c in self.GetChildren():
            if isinstance(c, wx.StaticText):
                c.Enable(filtrerTypes)
                
        self.app.MiseAJourFiltres(filtrerTypes, typ = None)
            
        
class PanelInclureExclure(wx.Panel):
    def __init__(self, parent, app, typ = "D", inclure = [], exclure = []):
        wx.Panel.__init__(self, parent, -1)
        
        self.inclure = inclure
        self.exclure = exclure
        self.typ = typ
        self.app = app
        
        ti = wx.StaticText(self, -1, u"Inclure")
        ti.SetFont(FONT_IE)
        te = wx.StaticText(self, -1, u"Exclure")
        te.SetFont(FONT_IE)
        
        if typ == "D": n = u"dossiers"
        elif typ == "F": n = u"fichiers"
        
        
        si = self.si = wx.TextCtrl(self, -1, u"\n".join(inclure), style=wx.TE_MULTILINE)
        self.Bind(wx.EVT_TEXT, self.EvtText, si)
 
        t_i = u"Spécifier les %s à inclure (les seuls qui figureront dans la structure)\n" \
             u"exemples :\n" \
             u"\t* \ttous les %s\n" \
             u"\tC* \tseulement ceux qui commencent par un \"C\"" %(n, n)
        if typ == "F":
            t_i += u"\n\t*.pdf \tseulement les PDF\n"    
    
        si.SetToolTipString(t_i)
        se = self.se = wx.TextCtrl(self, -1, u"\n".join(exclure), style=wx.TE_MULTILINE)
        self.Bind(wx.EVT_TEXT, self.EvtText, se)
        t_e = u"Spécifier les %s à exclure (ceux qui ne figureront pas dans la structure)\n" \
             u"exemples :\n" \
             u"\t* \ttous les %s\n" \
             u"\tC* \tseulement ceux qui commencent par un \"C\"" %(n ,n)
        if typ == "F":
            t_e += u"\n\t*.pdf \tseulement les PDF\n"
        se.SetToolTipString(t_e)

        gbs = wx.GridBagSizer()
        gbs.Add(ti, (0,0), flag = wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border = 4)
        gbs.Add(te, (0,1), flag = wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border = 4)
        gbs.Add(si, (1,0), flag = wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, border = 4)
        gbs.Add(se, (1,1), flag = wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, border = 4)
        gbs.AddGrowableRow(1)
        
        self.SetSizer(gbs)
        
    ##########################################################################################
    def EvtText(self, event):
        s = event.GetString()
        if event.GetEventObject() == self.si:
            self.inclure = s.split("\n")
        elif event.GetEventObject() == self.se:
            self.exclure = s.split("\n")
        self.app.MiseAJourFiltres(self.inclure, self.exclure, typ = self.typ)


import threading
import  wx.lib.newevent
(UpdateProgressEvent, EVT_UPDATE_PROGRESS) = wx.lib.newevent.NewEvent()

class ThreadDossier(threading.Thread): 
    def __init__(self, frm, mode): 
        threading.Thread.__init__(self)
        
        self.frm = frm
        self.mode = mode
        
        self._stopevent = threading.Event( )
        
    ##########################################################################################
    def SetDlg(self, dlg):
        self.dlg = dlg
        
    ##########################################################################################
    def creerCarte(self, nomFichier, titreCarte, dossier):
        # Version sdk
        if os.path.splitext(nomFichier)[1] != ".xmind":
            nomFichier = os.path.splitext(nomFichier)[0] + toSystemEncoding(".xmind")
        xm = xmind.load(nomFichier)
        first_sheet = xm.getPrimarySheet() # get the first sheet
        first_sheet.setTitle(titreCarte) # set its title
        root_topic = first_sheet.getRootTopic() # get the root topic of this sheet
        root_topic.setTitle(titreCarte) # set its title
        root_topic.setAttribute("structure-class", "org.xmind.ui.logic.right")
        # Version mekk
#        xmind = XMindDocument.create(titreCarte, titreCarte)
#        first_sheet = xmind.get_first_sheet()
#        root_topic = first_sheet.get_root_topic()

        self.genererCarte(dossier, root_topic)
        
        # mekk
#        xmind.save(nomFichier)
        
        # sdk
        xmind.save(xm, nomFichier) # and we save
        
    ##########################################################################################
    def fileOk(self, path, file):
        """ Vérifie si le couple (path, file) passe le filtre
                path et file doivent être encodés en FILE_ENCODING
        """
        inclureF = getListNomGlob(path, self.frm.inclure_Fic)
        exclureF = getListNomGlob(path, self.frm.exclure_Fic)
        fil = toSystemEncoding(file)
        typ = GetType(fil)
        
        return not fil in exclureF and fil in inclureF \
                    and (not self.frm.filtrerTypes \
                         or (not typ in self.frm.exclure_Typ and (typ in self.frm.inclure_Typ or len(self.frm.inclure_Typ) == 0)))
    
    ##########################################################################################
    def dirOk(self, path, file):
        """ Vérifie si le couple (path, file) passe le filtre
                path et file doivent être encodés en FILE_ENCODING
        """
        inclureD = getListNomGlob(path, self.frm.inclure_Dir)
        exclureD = getListNomGlob(path, self.frm.exclure_Dir)
        fil = toSystemEncoding(file)
        return not fil in exclureD and fil in inclureD

    
    ##########################################################################################
    def genererCarte(self, path, topic):
        if self._stopevent.isSet():
            return
        
        vide = True

        if not os.path.exists(path) or len(path) > 255:
            return

        dirs = os.listdir(path)
        
        for file in dirs:
            
            path_file = os.path.join(path, file)
            info_file = toSystemEncoding(path_file[len(self.frm.dossier):])
            
            if os.path.isdir(path_file):
                evt = UpdateProgressEvent(augmenter = 0, info = u"Dossier en cours de traitement :\n\n" + info_file, 
                                          message = None, 
                                          modeStop = False)
                wx.PostEvent(self.dlg, evt)
#                inclureD = getListNomGlob(path, self.frm.inclure_Dir)
#                exclureD = getListNomGlob(path, self.frm.exclure_Dir)
#                fil = toSystemEncoding(file)
#                if not fil in exclureD and fil in inclureD:
                if self.dirOk(path, file):
                    if len(os.listdir(path))>0:
                        # mekk
#                        t = topic.add_subtopic(file)
                        
                        # sdk
                        t = TopicElement()
                        t.setTitle(toSystemEncoding(file))
                        #t.addMarker("Folder.png")
                        
                        t.setFileHyperlink("file://" + toSystemEncoding(utils.get_abs_path(os.path.join(path, file))))
                        
                        dv = self.genererCarte(path_file, t)
                        
                        if EXCLURE_DOSSIERS_VIDE and not dv:
                            topic.addSubTopic(t)
                            vide = False
#                    self.count += 1
                    evt = UpdateProgressEvent(augmenter = fcount(path_file), info = None, message = None, modeStop = False)
                    wx.PostEvent(self.dlg, evt)
#                    self.dlg.Augmenter()
                else:
                    evt = UpdateProgressEvent(augmenter = fcount(path_file), info = None, message = None, modeStop = False)
                    wx.PostEvent(self.dlg, evt)
#                    self.dlg.Augmenter(fcount(path_file))
#                    self.count += fcount(path_file)
#                self.dlg.Augmenter()
                
                
            else:
                if self.fileOk(path, file):
                    ext = os.path.splitext(file)[1]
                    typ, nom = GetTypeNom(toSystemEncoding(file))
#                inclureF = getListNomGlob(path, self.frm.inclure_Fic)
#                exclureF = getListNomGlob(path, self.frm.exclure_Fic)
#                if not file in exclureF and file in inclureF and (typ in self.frm.inclure_Typ or typ == None):
                    # mekk
#                    t = topic.add_subtopic(GetNomSimple(file, typ))
#                    t.set_link(os.path.join(path, file))
#                    t.add_marker(TYPES[typ][1])
                    
                    # sdk
                    t = TopicElement()
                    if ext != "":
                        tx = nom.split(ext)[0]
                    else:
                        tx = nom
                    t.setTitle(tx)
                    
                    t.setFileHyperlink("file://" + toSystemEncoding(utils.get_abs_path(os.path.join(path, file))))
                    if typ != None:
                        t.addMarker(TYPES[typ][1])
                    
                    topic.addSubTopic(t)

                    vide = False
        return vide
    
    
    ##########################################################################################
    def genererDossier(self, path, sortie):
        if self._stopevent.isSet():
            return
        
        vide = True
#        try:
#            sortie = unicode(sortie, DEFAUT_ENCODING)
#        except:
#            pass
        
        if not os.path.exists(path) or len(path) > 255:
            return
        
        dirs = os.listdir(path)

        for file in dirs:
            path_file = os.path.join(path, file)
            info_file = ".." + toSystemEncoding(path_file[len(self.frm.dossier):])
            if os.path.isdir(path_file):
                evt = UpdateProgressEvent(augmenter = 0, info = u"Dossier en cours de traitement :\n\n" + info_file,
                                          message = None, modeStop = False)
                wx.PostEvent(self.dlg, evt)
                
                if self.dirOk(path, file):
#                inclureD = getListNomGlob(path, self.frm.inclure_Dir)
#                exclureD = getListNomGlob(path, self.frm.exclure_Dir)
#                fil = toSystemEncoding(file)
#                if not fil in exclureD and fil in inclureD:
                    if len(os.listdir(path))>0:
                        os.chdir(sortie)
                        try:
                            os.mkdir(file)
                        except WindowsError as e:
                            print "WindowsError({0}): {1}".format(e.errno, e.strerror), e.filename
                        except:
                            print "Unexpected error:", sys.exc_info()[0]
                            raise
                        dv = self.genererDossier(path_file, os.path.join(sortie, file))
                        
                        if EXCLURE_DOSSIERS_VIDE and not dv:
                            vide = False
                        else:
                            os.chdir(sortie)
                            try:
                                os.rmdir(file)
                            except:
                                pass
                    
                    evt = UpdateProgressEvent(augmenter = 1, info = None, message = None, modeStop = False)
                    wx.PostEvent(self.dlg, evt)
                else:
                    evt = UpdateProgressEvent(augmenter = fcount(path_file), info = None, message = None, modeStop = False)
                    wx.PostEvent(self.dlg, evt)
                        
            else:
                if self.fileOk(path, file):
                    shutil.copy2(os.path.join(path, file), sortie)
                    vide = False
                    
#                ext = os.path.splitext(file)[1]
#                typ, nom = GetTypeNom(file)
#                inclureF = getListNomGlob(path, self.frm.inclure_Fic)
#                exclureF = getListNomGlob(path, self.frm.exclure_Fic)
#                if not file in exclureF and file in inclureF \
#                    and (not typ in self.frm.exclure_Typ and (typ in self.frm.inclure_Typ or len(self.frm.inclure_Typ) == 0)):
#                    shutil.copy2(os.path.join(path, file), sortie)
#                    vide = False
        return vide
    
    
     
        
    def run(self):
        
        #
        # Carte mentale
        #
        if self.mode == 0:
            wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
            
            nDossiers = fcount(self.frm.dossier)
            self.dlg.SetMaxi(nDossiers)

            evt = UpdateProgressEvent(augmenter = 0, info = None,
                                      message = u"Génération de la carte mentale ...\n\n",
                                      modeStop = False)
            wx.PostEvent(self.dlg, evt)
            
            self.creerCarte(toFileEncoding(self.frm.nomFichier),
                            self.frm.titreCarte, 
                            self.frm.dossier)
            
            wx.EndBusyCursor()
            evt = UpdateProgressEvent(augmenter = 0, info = u"Fichier :\n" + toSystemEncoding(self.frm.nomFichier),
                                      message = u"La carte mentale à été correctement générée\n\n",
                                      modeStop = True)
            wx.PostEvent(self.dlg, evt)
            
            self.frm.boutonOuvrirXMind.Enable(True)
            
        #
        # Dossier clone
        # 
        else:
        
            wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
            
            nDossiers = fcount(self.frm.dossier)
            self.dlg.SetMaxi(nDossiers) 
                 
            evt = UpdateProgressEvent(augmenter = 0, info = None,
                                      message = u"Génération du dossier clone ...\n\n",
                                      modeStop = False)
            wx.PostEvent(self.dlg, evt)
                    
            self.genererDossier(toFileEncoding(self.frm.dossier), os.getcwd())
            
            if not self._stopevent.isSet():
                if self.frm.ajouterCarteMentale:
                    evt = UpdateProgressEvent(augmenter = 0, info = u"",
                                              message = u"Génération de la carte mentale ...\n\n",
                                              modeStop = False)
                    wx.PostEvent(self.dlg, evt)
                    f = toFileEncoding(self.frm.titreCarte)
                    fichierXmind = os.path.join(toFileEncoding(self.frm.dossierSortie),
                                                f, f)
                    self.creerCarte(fichierXmind, self.frm.titreCarte, 
                                    os.path.join(toFileEncoding(self.frm.dossierSortie), f))
                
            wx.EndBusyCursor()
            
            evt = UpdateProgressEvent(augmenter = 0, info = u"Fichier :\n" + toSystemEncoding(self.frm.dossier),
                                      message = u"Le dossier clone à été correctement générée\n\n",
                                      modeStop = True)
            wx.PostEvent(self.dlg, evt)
            self.frm.boutonOuvrirDossier.Enable(os.path.exists(self.frm.dossierSortie))
    
    
    def stop(self): 
        self._stopevent.set()
        
        
        
class ProgressFrame(wx.Frame):
    def __init__(
            self, parent, ID, title, thread, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE,
            ):
        wx.Frame.__init__(self, None, ID, title, pos, size)
        panel = wx.Panel(self, -1)
        self.thread = thread
        
        self.Bind(EVT_UPDATE_PROGRESS, self.OnUpdate)
        
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(panel, -1, u"\n")
        
        self.label.SetFont(FONT_ACTION)
        sizer.Add(self.label, 0, wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, 5)
        
        self.info = wx.StaticText(panel, -1, u"\n\n", style = wx.ST_ELLIPSIZE_START)
        sizer.Add(self.info, 0, wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, 5)

        self.gauge = wx.Gauge(panel, -1, 1)
        sizer.Add(self.gauge, 0, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5)
        self.count = 0
        
        line = wx.StaticLine(panel, -1, size=(-1,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        self.btn = wx.Button(panel, -1, u"Annuler")
        self.btn.SetHelpText(u"Annuler le traitement")
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btn)
        self.btn.SetDefault()
#        btn.SetSize(btn.GetBestSize())

        sizer.Add(self.btn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetMinSize((250,120))
        self.Layout()
        panel.SetSizerAndFit(sizer)
#        sizer.Fit(self)


    ##########################################################################################
    def SetMaxi(self, maxi):
        self.gauge.SetRange(maxi)
        
        
    ##########################################################################################
    def OnUpdate(self, evt):
        self.Augmenter(evt.augmenter)
        if evt.info != None:
            self.SetInfo(evt.info)
        if evt.message != None:
            self.SetMessage(evt.message)
        if evt.modeStop:
            self.btn.SetLabel(u"Terminé")
        
    ##########################################################################################
    def OnClick(self, event):
        if self.btn.GetLabel()[0] == "T":
            self.Destroy()
        else:
            self.thread.stop()
        
    ##########################################################################################
    def Augmenter(self, n = 1):
        self.count += n
#        print self.count
        self.gauge.SetValue(self.count)
        self.Update()
        self.Refresh()

    ##########################################################################################
    def SetMessage(self, t):
#        print t
        self.label.SetLabelText(t)
        self.Update()
        self.Layout()
        self.Refresh()
        
    ##########################################################################################
    def SetInfo(self, t):
#        print t
        if t != u"":
            self.info.SetLabel(t)
        else:
            self.info.SetLabel(u"")
#        self.Fit()
#        self.Update()
#        self.Layout()
#        self.Refresh()




def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise
    
    
    
    
#############################################################################################################
def messageErreur(parent, titre, message):
    dlg = wx.MessageDialog(parent, message, titre,
                           wx.OK | wx.ICON_WARNING)
    dlg.ShowModal()
    dlg.Destroy()
    

if __name__ == '__main__':

#    if len(sys.argv) > 1:
#        arg = sys.argv[1]
#    else:
#        arg = ''
#    sys.exit()
    
    

    app = wx.App()
    
    FONT_IE = wx.Font(10, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD)
    FONT_ACTION = wx.Font(11, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD)
    FONT_ITALIC = wx.Font(10, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)

    NomFichier = None
    if len(sys.argv)>1: #un paramètre a été passé
        parametre=sys.argv[1]
        # on verifie que le fichier passé en paramètre existe
        if os.path.isdir(parametre):
            NomFichier = parametre
            
    app.frame = pyXorgFrame(NomFichier)
    app.frame.Show()
    app.MainLoop()
    

