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
module pysequence
*****************

Module de base de **pySéquence**.

"""

import wx
from wx.lib.embeddedimage import PyEmbeddedImage
import time

import glob

import os, sys
if sys.platform == "win32" :
    # Pour lire les classeurs Excel
    import recup_excel
    # Pour compléter les grilles Excel
    import grilles
    th_xls = grilles.get_th_xls()

from jinja2 import Template
from bs4 import BeautifulSoup

import version
import textwrap
import base64

from couleur import Str2Couleur, Couleur2Str
import couleur

import images
# Graphiques vectoriels
import draw_cairo_seq, draw_cairo_prj, draw_cairo_prg, draw_cairo



# Pour passer des arguments aux callback
import functools

# Pour les copier/coller
import pyperclip

# Outils "système"
import subprocess

from operator import attrgetter



from undo import UndoStack

# Les constantes partagées
from constantes import calculerEffectifs, \
                        getCoulPartie, \
                        TOUTES_REVUES_EVAL, TOUTES_REVUES_EVAL_SOUT, TOUTES_REVUES_SOUT, TOUTES_REVUES, \
                        _S, _Rev, _R1, _R2, _R3, \
                        revCalculerEffectifs, \
                        COUL_OK, COUL_NON, COUL_BOF, COUL_BIEN, \
                        toList, COUL_COMPETENCES, COUL_DISCIPLINES, NBR_SYSTEMES_MAXI
import constantes

import proprietes

from util_path import toFileEncoding, toSystemEncoding, SYSTEM_ENCODING, testRel

# Widgets partagés
# des widgets wx évolués "faits maison"
from widgets import Variable, VAR_REEL_POS, VAR_ENTIER_POS, sublist, \
                    messageErreur, getNomFichier, pourCent2, pstdev, mean, \
                    rallonge, remplaceCode2LF, dansRectangle, XMLelem, \
                    Grammaire, et2ou, \
                    remplaceLF2Code, messageInfo, messageYesNo, enregistrer_root, \
                    getAncreFenetre, tronquer, getHoraireTxt, scaleImage, locale2def, locale2EN#, chronometrer
                    
from Referentiel import REFERENTIELS, ACTIVITES
import Referentiel

import webbrowser

from richtext import XMLtoHTML, XMLtoTXT

# Pour enregistrer en xml
import xml.etree.ElementTree as ET
Element = type(ET.Element(None))

from xml.dom.minidom import parseString

from objects_wx import CodeBranche, PopupInfo, getIconeFileSave, getIconeCopy, \
                            getBitmapFromImageSurface, img2str, getIconePaste, \
                            PanelPropriete_Progression, \
                            PanelPropriete_CI, PanelPropriete_LienSequence,\
                            PanelPropriete_Classe, PanelPropriete_Sequence, \
                            PanelPropriete_Projet, PanelPropriete_Competences, \
                            PanelPropriete_Savoirs, PanelPropriete_Seance, \
                            PanelPropriete_Tache, PanelPropriete_Systeme, \
                            PanelPropriete_Support, PanelPropriete_LienProjet,\
                            PanelPropriete_Personne, getDisplayPosSize, URLDialog, \
                            PanelPropriete_Groupe, PanelPropriete_Modele, \
                            PanelPropriete_FS, SSCALE


DEBUG = "beta" in version.__version__


def b64(img):
    return str(b"data:image/png;base64,"+base64.b64encode(img), 'utf-8')
        
        

def safeParse(nomFichier, toplevelwnd):
    if not os.path.isfile(nomFichier):
        return
    
    fichier = open(nomFichier,'r', encoding='utf-8')
    parser = ET.XMLParser(encoding="utf-8")
    
    root = ET.parse(fichier, parser = parser).getroot()
    fichier.close()
    return root
    
    
#     try:
#         root = ET.parse(fichier, parser = parser).getroot()
#         fichier.close()
#         return root
#     
#     except:# ET.ParseError:
#         messageErreur(toplevelwnd, "Fichier corrompu", 
#                           "Le fichier suivant est corrompu !!\n\n"\
#                           "%s\n\n" \
#                           "Il est probablement tronqué suite à un echec d'enregistrement." %toSystemEncoding(nomFichier))
#         fichier.close()
#         
    

#######################################################################################  
#def forceID(xml):
#    for node in xml.childNodes:
#        if hasattr(node, 'hasAttribute'):
#            if node.hasAttribute("id"):
#                node.setIdAttribute('id')
#            if node.hasChildNodes():
#                forceID(node)
#
######################################################################################
######################################################################################
#def SetWholeText(node, Id, text):
#    """ 
#    """
#    print "SetWholeText", Id
#    tag = node.find(id=Id)
#    print tag
#    tag.string.replace_with(text)
#    
    
#    nom = node.getElementById(Id)
#    if nom != None:
#        for txtNode in nom.childNodes:
#            if txtNode.nodeType==xml.dom.Node.TEXT_NODE:
#                txtNode.replaceWholeText(text)


######################################################################################
#def XML_AjouterElemListe(node, idListe, dt, dd):
#    liste = node.find(id = idListe)
#    print "liste", liste
#    if len(liste.find_all('dt')) == 1:
#        liste.dt.string = dt
#        liste.dd.string = dd
#    else:
#        tag_dt = copy.copy(liste.dt)
#        tag_dd = copy.copy(liste.dd)
#        liste.append(tag_dt)
#        liste.append(tag_dd)
        
#    liste = node.getElementById(idListe)
#    if liste != None:
#        _dt = node.createElement("dt")
#        txt = node.createTextNode(dt)
#        _dt.appendChild(txt)
#        liste.appendChild(_dt)
#        
#        _dd = node.createElement("dd")
#        txt = node.createTextNode(dd)
#        _dd.appendChild(txt)
#        liste.appendChild(_dd)


######################################################################################
#def XML_AjouterElemListeUL(node, idListe, li):
#    liste = node.find(id = idListe)
#    print "liste", liste
#    if len(liste.find_all('li')) == 1:
#        liste.li.string = li
#    else:
#        tag_li = copy.copy(liste.li)
#        liste.append(tag_li)
    
    

    
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
    

# import chardet
import util_path
import shutil

import re




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
        self.path = path # Impérativement toujours encodé en FILE_ENCODING !!
        self.type = typ
        self.ok = False  # Etat du lien (False = lien rompu)
        
    ######################################################################################  
    def __repr__(self):
        return self.type + " : " + toSystemEncoding(self.path)
    
    
    ######################################################################################  
    def __neq__(self, l):
        if self.typ != l.typ:
            return True
        elif self.path != l.path:
            return True
        return False
    
    
    ######################################################################################  
    def DialogCreer(self, pathseq):
        dlg = URLDialog(None, self, pathseq)
        dlg.ShowModal()
        dlg.Destroy() 
            

    ######################################################################################  
    def Afficher(self, pathseq, fenSeq = None):
        """ Lance l'affichage du contenu du lien
            <pathseq> = chemin de l'application pour déterminer le chemin absolu
        """
#         print "Afficher", self.type, self.path
        path = self.GetAbsPath(pathseq)
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
                messageErreur(None, "Chemin non trouvé",
                                  "Le fichiern'a pas été trouvé\n\n%s" %toSystemEncoding(path))        
            
                
        elif self.type == 'd':
            if os.path.isdir(path):
                openFolder(path)
#                 try:
# #                     subprocess.Popen(["explorer", path])
#                     
#                 except:
#                     messageErreur(None, u"Ouverture impossible",
#                                   u"Impossible d'accéder au dossier\n\n%s\n" %toSystemEncoding(path))
            else:
                messageErreur(None, "Chemin non trouvé",
                                  "Le dossiern'a pas été trouvé\n\n%s" %toSystemEncoding(path))


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
    def EvalTypeLien(self, pathseq):
        """ Evaluation du de self.lien.path
            par rapport à pathseq
            et attribue un type
        """
#         print("EvalTypeLien", self, pathseq)
        abspath = self.GetAbsPath(pathseq)
        
        if os.path.exists(abspath):
            relpath = testRel(abspath, pathseq)
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
    def EvalLien(self, path, pathseq):
        """ Teste la validité du chemin <path> (SYSTEM_ENCODING)
             par rapport au dossier de référence <pathseq> (FILE_ENCODING)
             
             et change self.path (FILE_ENCODING)
             
        """
#         print("EvalLien", path, pathseq, os.path.exists(pathseq))
#         print " >", chardet.detect(bytes(path))
#         print " >", chardet.detect(bytes(pathseq))
        
        
        if path == "" or path.split() == []:
            self.path = r""
            self.type = ""
            return
        
        self.EvalTypeLien(pathseq)
#         path = toFileEncoding(path)
#        pathseq = toFileEncoding(pathseq)
#         abspath = self.GetAbsPath(pathseq, path)
#         print("   abs :", abspath)
#         
#         EvalTypeLien
#         relpath = testRel(abspath, pathseq)
# 
# #         relpath = testRel(abspath, pathseq)
# #         print "   rel :", relpath
# #         
# #         print "   ", os.getcwd()
# #         print "   ", os.curdir
#         
#         if os.path.exists(abspath):
#             if os.path.isfile(abspath):
#                 self.type = 'f'
#                 self.path = relpath
#                 self.ok = True
#             elif os.path.isdir(abspath):
#                 self.type = 'd'
#                 self.path = relpath
#                 self.ok = True
        
            
#         else:
#             self.type = 'u'
#             self.path = path
        
#         print " >>>", self
              
    ######################################################################################  
    def GetAbsPath(self, pathseq, path = None):
        """ Renvoie le chemin absolu du lien
            grace au chemin du document <pathseq>
        """
#         print("GetAbsPath", path, pathseq)
        if path == None:
            path = self.path
            
        if path == ".":
            return pathseq
        
        cwd = os.getcwd()
        if pathseq != "":
            try:
                os.chdir(pathseq)
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
                path = os.path.join(pathseq, path)
            except UnicodeDecodeError:
                pathseq = toFileEncoding(pathseq)
                path = os.path.join(pathseq, path)
        
        
        os.chdir(cwd)
        return path
    
    
    ######################################################################################  
    def GetRelPath(self, pathseq, path = None):
        """ Renvoie le chemin relatif du lien
            grace au chemin du document <pathseq>
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
                path = os.path.join(pathseq, path)
            except UnicodeDecodeError:
                pathseq = toFileEncoding(pathseq)
                path = os.path.join(pathseq, path)
        return path
    
    
    ######################################################################################  
    def getBranche(self, branche):
        branche.set("Lien", toSystemEncoding(os.path.normpath(self.path)))
        branche.set("TypeLien", self.type)
        
        
    ######################################################################################  
    def setBranche(self, branche, pathseq):
        self.path = toFileEncoding(branche.get("Lien", r""))
        self.path = os.path.normpath(self.path)
        self.type = branche.get("TypeLien", "")
        if self.type == "" and self.path != r"":
            self.EvalTypeLien(pathseq)
        return True






    
Titres = ["Séquence pédagogique",
          "Prérequis",
          "Objectifs pédagogiques",
          "Séances",
          "Systèmes et matériels",
          "Classe",
          "Élèves",
          "Support",
          "Tâches",
          "Projet", 
          "Équipe pédagogique",
          "Séquences et Projets", 
          "Progression"]






####################################################################################
#
#   Classe définissant les propriétés d'un élément avec lien externe : Lien()
#
####################################################################################
class ElementAvecLien():
    def __init__(self):
        self.lien = Lien()
        
    ######################################################################################  
    def GetPath(self):
        return self.GetDocument().GetPath()
    
    ######################################################################################  
    def GetLien(self):
        return self.lien.path
        
    ######################################################################################  
    def GetLienHTML(self):
        if self.lien.type in ['f', 'd', 's']:
            if self.lien.path != '':
                return str('file:///' + os.path.abspath(self.lien.path))
            else:
                return ''
        else:
            return str(self.lien.path)
    
    ######################################################################################  
    def CreerLien(self, event):
        self.lien.DialogCreer(self.GetPath())
        self.SetLien()
        if hasattr(self, 'panelPropriete'): 
            self.GetApp().sendEvent(modif = "Création d'un lien")
    
    
    ######################################################################################  
    def SetLien(self, lien = None):
        if hasattr(self, 'tip_titrelien'):
            self.tip.SetLien(self.lien, self.tip_titrelien, self.tip_ctrllien)
        
        if hasattr(self, 'sousSeances'):
            for sce in self.seances:
                sce.SetLien()
          
            
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        pass
     
        
    ######################################################################################  
    def AfficherLien(self, pathseq): 
        self.lien.Afficher(pathseq)
        
        
    ######################################################################################  
    def OnPathModified(self):
        if hasattr(self, 'tip_titrelien'):
            self.tip.SetLien(self.lien, self.tip_titrelien, self.tip_ctrllien)
        
        



#########################################################################################
def GetObjectFromClipBoard(instance):
    """ Récupération d'un objet pySéquence depuis le presse-papier
        uniquement <instance>
    """
    try:
        b = ET.fromstring(pyperclip.paste())
    except:
        b = None

    if isinstance(b, Element): # Le presse contient un Element XML
        if b.tag[:len(instance)] == instance: # Le presse contient une instance attendue
            return b
    return None




######################################################################################  
#
#   Element de base pySequence
#        - TIP
#        - Enrichissement SVG
#        - Gestion Presse-papier
#        - Description détaillée (richText)
#        - ...
#
######################################################################################  
class ElementBase(Grammaire):
    def __init__(self, tipWidth = 400*SSCALE):
        
                
        
        #
        # Création du Tip (PopupInfo)
        #
        self.tip = PopupInfo(self.GetApp().parent, "", width = tipWidth)
        
        self.toolTip = None


#    def SetSVGTitre(self, p, titre):
#        print "SetSVGTitre", titre
#        titre = titre.decode(DEFAUT_ENCODING)
#        titre = titre.encode('utf-8') 
#        titre = titre.replace(u"\n", u"<br>")
#        self.elem.setAttribute("xlink:title", titre)
    
        
        
    def SetSVGLien(self, p, lien):
#        print "SetSVGLien", lien
        
        p.setAttribute("xlink:href", lien) #
        p.setAttribute("target", "_top")
#        self.elem.setAttribute("xlink:href", lien)
#        self.elem.setAttribute("target", "_top")
        
#    def EncapsuleSVG(self, doc, p):
#        self.elem = doc.createElement("a")
#        parent=p.parentNode
#        parent.insertBefore(self.elem, p)
#        self.elem.appendChild(p)
#        return self.elem

#     ######################################################################################  
#     def getBranche_TOTAL(self, listElem):
#         root = ET.Element(self.nom_obj)
#         for e in listElem:
#             self.getBranche_AUTO(root, e, getattr(self, e))
#         return root

    ####################################################################################
    def EstMovable(self):
        return False
    
    ####################################################################################
    def EstMemeCategorie(self, obj):
        return type(self) is type(obj)
        
    ######################################################################################  
    def getBrancheImage(self, root, nom = "Image"):
        if self.image != None:
            root.set(nom, str(img2str(self.image.ConvertToImage()), 'utf-8'))
    
    
    ######################################################################################  
    def getBrancheIcone(self, root, nom = "Icone"):
        if self.icone != None:
#             str(b"data:image/png;base64,"+base64.b64encode(img), 'utf-8')
            
            root.set(nom, str(img2str(self.icone.ConvertToImage()), 'utf-8'))
            
                    
    ######################################################################################  
    def setBrancheImage(self, branche, nom = "Image"):
        Ok = True
        data = branche.get(nom, "")
        self.image = None
        if data != "":
            try:
                locale2EN()
                self.image = PyEmbeddedImage(data).GetBitmap()
                locale2def()
            except:
                Ok = False
                self.image = None
        return Ok
                
    
    ######################################################################################  
    def setBrancheIcone(self, branche, nom = "Icone"):
        data = branche.get(nom, "")
        if data != "":
            try:
                self.icone = PyEmbeddedImage(data).GetBitmap()
            except:
                self.icone = None
    
    
    ######################################################################################  
    def getIcone(self):
        return wx.NullBitmap
    
    ######################################################################################  
    def getIconeDraw(self):
        return wx.NullBitmap
    
    ######################################################################################  
    def GetOrdre(self):
        """ Pour la fonction OnCompareItems() des arbres
        """
        return 0
    
#     ######################################################################################  
#     def getBranche_AUTO(self, branche, nom, v):
#         if hasattr(v, 'getBranche'):
#             branche.append(v.getBranche())
#         elif isinstance(v, list):
#             self.getBrancheList(branche, nom, v)
#         else:
#             branche.set(nom, v)
        
#     ######################################################################################  
#     def getBrancheList(self, branche, nom, dic):
#         b = ET.SubElement( branche, nom)
#         for obj in dic.values():
#             b.append(obj.getBranche())
#     
    
#     ######################################################################################  
#     def setBranche_TOTAL(self, branche):   
#         return

    
    ######################################################################################  
    def CopyToClipBoard(self, event = None):
        pyperclip.copy(ET.tostring(self.getBranche(), encoding="utf-8").decode('utf-8'))
        
    ######################################################################################  
    def SetToolTip(self, toolTip):
#         print("SetToolTip", toolTip)
        self.toolTip = toolTip
        
    ######################################################################################  
    def SetDescription(self, description, draw = False):
        if self.description != description:
#             ref = self.GetReferentiel()
#             print("SetDescription", self)
            self.description = description
#             self.GetApp().sendEvent(modif = "Modification de la description %s" %ref._nomActivites.du_())
            self.GetApp().sendEvent(modif = "Modification de la description %s" %self.du_(),
                                    draw = draw)
            
#            self.tip.SetRichTexte()


    
    ######################################################################################  
    def EnrichiHTML(self, doc, seance = False):
        """ Enrichissement de l'image SVG <doc> (format XML) avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens 
             - ...
        """
#         print("EnrichiHTML", self, seance, self.cadre)
        
        for i, (p, f, c) in enumerate(self.cadre):
            div = doc.new_tag('div')
            div['class'] = "mouse tooltip"
            div['id'] = self.GetCode(i).replace('.', '_').replace(' ', '_')
            bulle = BeautifulSoup(self.GetBulleHTML(f, css = True), "html5lib").body
            div.extend(bulle.findChildren())
#             div.append(bulle)
            
#             c = bulle.body
#             print(c)
#             for t in bulle.findChildren():
#                 print(t, type(t))
#                 div.append(t)
            
            
            doc.body.insert(0, div)
            
            p['class'] = "sensible"
            p['id'] = self.GetCode(i).replace('.', '_').replace(' ', '_')
            p['x'] = c[0]
            p['y'] = c[1]
        
#             if hasattr(self, 'GetLien'):
#                 lien = self.GetLienHTML()
# #                lien = lien.decode(FILE_ENCODING)
# #                 lien = lien.encode('utf-8')
#                 t = doc.createElement("a")
#                 txt = doc.createTextNode(lien)
#                 t.appendChild(txt)
#                 np = p.cloneNode(True)
#                 t.appendChild(np)
#                 if p.parentNode is not None:
#                     p.parentNode.insertBefore(t, p)
#                     p.parentNode.removeChild(p)
# #                p.appendChild(t)
#                 
#                 if lien != '':
#                     self.SetSVGLien(t, lien)
                    
                    
                    
        if hasattr(self, 'GetLien'):
            lien = self.GetLienHTML()
            if len(lien) > 0:
#                 print(self, ">>> lien:", lien)
                for i, (p, f, c) in enumerate(self.cadre):
                    tag_a = doc.new_tag('a')
                    tag_a['href'] = lien
                    tag_a['target'] = "_blank"
                    p.wrap(tag_a)
                
    
    ######################################################################################  
    def EnrichiSVG(self, doc, seance = False):
        """ Enrichissement de l'image SVG <doc> (format XML) avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens 
             - ...
        """
#         print("EnrichiSVG", self, doc, seance, self.cadre)
        # 
        # Le titre de la page
        #
        pid = '' # id du path
        for p, f in self.cadre:
            if type(f) == str:
                pid = f
                p.setAttribute('filter', 'none')
                p.setAttribute("id",  pid)
                p.setAttribute("onmouseout",  "setAttribute('filter', 'none')")
                p.setAttribute("onmouseover", "setAttribute('filter', 'url(#f1)')")
                break
        
        for i, (p, f) in enumerate(self.cadre):
            if type(f) != str:
#                self.EncapsuleSVG(doc, p)
                titre = self.GetBulleSVG(f)
                t = doc.createElement("title")
                txt = doc.createTextNode(titre)
                t.appendChild(txt)
                p.appendChild(t)
                
                
#                self.SetSVGTitre(p, titre)
                p.setAttribute("id",  self.GetCode(f)+str(f))
                p.setAttribute("pointer-events",  'all')
                
                if pid == '':
                    p.setAttribute("onmouseout",  "setAttribute('filter', 'none')")
                    p.setAttribute("onmouseover", "setAttribute('filter', 'url(#f1)')")
                    
                else:
                    p.setAttribute("onmouseout",  "evt.target.parentNode.parentNode.parentNode.getElementById('%s').setAttribute('filter', 'none');" %pid)
                    p.setAttribute("onmouseover", "evt.target.parentNode.parentNode.parentNode.getElementById('%s').setAttribute('filter', 'url(#f1)');" %pid)

        
            if seance:
                att0 = p.getAttribute("onmouseout")
                att1 = p.getAttribute("onmouseover")
                
                n = list(range(len(self.cadre)))
                n.remove(i)
                for j in n:
                    Id = self.GetCode(f)+str(j)
                    att0 += "; evt.target.parentNode.parentNode.parentNode.getElementById('%s').setAttribute('filter', 'none')" %Id
                    att1 += "; evt.target.parentNode.parentNode.parentNode.getElementById('%s').setAttribute('filter', 'url(#f1)')" %Id

                p.setAttribute("onmouseout", att0)
                p.setAttribute("onmouseover", att1)
                
                
            if hasattr(self, 'GetLien'):
                lien = self.GetLienHTML()
#                lien = lien.decode(FILE_ENCODING)
#                 lien = lien.encode('utf-8')
                t = doc.createElement("a")
                txt = doc.createTextNode(lien)
                t.appendChild(txt)
                np = p.cloneNode(True)
                t.appendChild(np)
                if p.parentNode is not None:
                    p.parentNode.insertBefore(t, p)
                    p.parentNode.removeChild(p)
#                p.appendChild(t)
                
                if lien != '':
                    self.SetSVGLien(t, lien)
        
        
    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
            Chaque point caractéristique est de la forme :
            ((x, y), element, code ou indice)
        """
#         print("GetPtCaract base :", self)
        lst = []
        
        # Points caractéristiques des rectangles (sans code)
        if hasattr(self, 'pts_caract' ):
            for i, pt in enumerate(self.pts_caract):
                lst.append((pt, self, i))
        
        # Points caractéristiques des rectangles (avec code)
        # Contenu de chaque "point" : ((x,y), code)
        if hasattr(self, 'pt_caract' ):
            for pt in self.pt_caract:
#                 print("   ", pt)
                lst.append((pt[0], self, pt[1]))
            
        self.cadre = [] # ???
        return lst
    
    
    ######################################################################################  
    def GetDescription(self):
        if hasattr(self, "description"):
            return XMLtoTXT(self.description)

            
    ######################################################################################  
    def GetBulleSVG(self, i):
#         print("GetBulleSVG", self, i)
#        if hasattr(self, 'description'):
#            des = "\n\n" + self.GetDescription()

        t = self.GetCode(i) + " :\n" + self.GetIntit(i)  
        if self.GetDescription() != None:
            t += "\n\n" + self.GetDescription()
        
#         print("ttt", type(t))
        return t#.encode(SYSTEM_ENCODING)#.replace("\n", "&#10;")#"&#xD;")#
    
    
    ######################################################################################  
    def GetBulleHTML(self, i = None, css = False):
#         print("GetBulleHTML", self, i)
        return  ""
    
    
    
    
    ######################################################################################     
    def GetClasse(self):
        if hasattr(self, 'projet') and self.projet is not None:
            cl = self.projet.classe
        elif hasattr(self, 'sequence') and self.sequence is not None:
            cl = self.sequence.classe
        elif hasattr(self, 'progression'):
            cl = self.progression.classe
        elif hasattr(self, 'parent'):
            if isinstance(self.parent, Classe):
                cl = self.parent
            else:
                cl = self.parent.classe
        elif hasattr(self, 'GetDocument'):
            cl = self.GetDocument().classe
        else:
            cl = self.classe
        return cl
    
    
    ######################################################################################  
    def GetTypeEnseignement(self, simple = False):
        cl = self.GetClasse()
            
        if simple:
            return cl.familleEnseignement
        
        return cl.typeEnseignement
    

    ######################################################################################  
    def GetReferentiel(self):
        try:
            return self.GetClasse().referentiel
        except:
            return REFERENTIELS[self.GetTypeEnseignement()]

#     ######################################################################################  
#     def GetLabelEleve(self):
#         return self.GetReferentiel().labels["ELEVES"][0]

    ######################################################################################  
    def GetProjetRef(self):
        return self.GetDocument().GetProjetRef()

    ######################################################################################  
    def GetTip(self):
        if hasattr(self, 'tip'):
            return self.tip
        
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        if param is None:
            return constantes.encap_HTML(constantes.BASE_FICHE_HTML)
        else:
            if param == "CAL":
                return constantes.encap_HTML(constantes.BASE_FICHE_HTML_CALENDRIER)
            
            elif param == "PB":
                return constantes.encap_HTML(constantes.BASE_FICHE_HTML_PROB)
                
            elif param == "ANN":
                pass
            
            elif param == "DOM":
                return constantes.encap_HTML(constantes.BASE_FICHE_HTML_DOM)
                
            elif param[:3] == "POS":
                return constantes.encap_HTML(constantes.BASE_FICHE_HTML_PERIODES)
                
            elif param[:3] == "EQU":
                pass
            
            elif param[:2] == "CI":
                return constantes.encap_HTML(constantes.BASE_FICHE_HTML_CI)
                
            else:
                pass
            
        return constantes.encap_HTML(constantes.BASE_FICHE_HTML)

    
#     ######################################################################################  
#     def GetBulleHTML(self, i , css = False):
#         print("GetBulleHTML", self, i)
#         return self.GetFicheHTML()
        
    ######################################################################################  
    def GetProfondeur(self):
        return 0  
        
        
        

class Classe(ElementBase):
    def __init__(self, app, intitule = "", 
                 pourProjet = False, typedoc = ''):
        self.app = app
        ElementBase.__init__(self)
        
        self.intitule = intitule
        
        self.undoStack = UndoStack(self)
        
        self.verrouillee = False
        self.specialite = []
        
        self.academie = ""
        self.ville = ""
        self.etablissement = ""
        self.effectifs = {}
        self.nbrGroupes = {'C' : 1} # un seul groupe "classe entière"
        self.systemes = []
        
        
#        self.panelParent = panelParent
        
        self.Initialise(pourProjet)
        
        self.undoStack.do("Création de la Classe")
            
        

        
    ######################################################################################  
    def __repr__(self):
        return "Classe "+ self.typeEnseignement
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Classe(parent, self)
    
    ######################################################################################  
    def GetApp(self):
        return self.app
    
    ######################################################################################  
    def GetPath(self):
        return r""
    
    ######################################################################################  
    def MiseAJourTypeEnseignement(self):
        
        
        if hasattr(self, 'codeBranche'):
#            print "MiseAJourTypeEnseignement classe", self.GetReferentiel().Enseignement[0]
            self.codeBranche.SetLabel(rallonge(self.GetLabel()))
        
#        self.CI = self.options.optClasse["CentresInteret"]
#        self.posCI = self.options.optClasse["PositionsCI"]
        
#        self.ci_SSI = self.options.optClasse["CentresInteretSSI"]
#        self.ci_ET = self.options.optClasse["CentresInteretET"]
#        self.posCI_ET = self.options.optClasse["PositionsCI_ET"]
        

#    ######################################################################################  
#    def SetCI(self, num, ci):
#        self.CI[num] = ci
        
    ######################################################################################  
    def setDefaut(self, typ = 'SSI'):
#        print "setDefaut Classe"
        self.typeEnseignement = typ
        self.specialite = []
        
        self.effectifs['C'] = constantes.Effectifs["C"]
        self.nbrGroupes = { "C" : 1,
                            "G" : constantes.NbrGroupes["G"],
                            "S" : constantes.NbrGroupes["S"],
                            "T" : constantes.NbrGroupes["T"],
                            "U" : constantes.NbrGroupes["U"],
                            "E" : constantes.NbrGroupes["E"],
                            "P" : constantes.NbrGroupes["P"],
                            "D" : 2}
        
        self.academie = ""
        self.ville = ""
        self.etablissement = ""
        
        self.systemes = []


    ######################################################################################  
    def Initialise(self, pourProjet, defaut = False):
        
        options = self.GetApp().parent.options
        typ = options.optClasse["Enseignement"]
#         print("Initialise", typ)
#         print(REFERENTIELS.keys())
        if not (typ in REFERENTIELS.keys()):
            typ = 'SSI'
#         print("  >>", typ)
        # Force à "défaut" ou pas de fichier Classe dans les options
        if defaut or options.optClasse["FichierClasse"] == r"":
            self.setDefaut(typ)
            
        else:
            # Impossible de charger le fichier Classe
            if not self.ouvrir(options.optClasse["FichierClasse"]):
                self.setDefaut(typ)
            
            
        self.referentiel = REFERENTIELS[self.typeEnseignement]
        
        # On vérifie que c'est bien un type d'enseignement avec projet
        if pourProjet:
            if not self.typeEnseignement in [ref.Code for ref in REFERENTIELS.values() if len(ref.projets) > 0]:
                self.typeEnseignement = constantes.TYPE_ENSEIGNEMENT_DEFAUT
                self.referentiel = REFERENTIELS[self.typeEnseignement]
        else:    
            self.MiseAJourTypeEnseignement()
        
        self.familleEnseignement = self.GetReferentiel().Famille  
        
        self.positions = self.referentiel.getPeriodeSpe(self.specialite)

            
#         print("Positions classe :", self.positions)
        calculerEffectifs(self)


    ######################################################################################  
    def SetDocument(self, doc):   
        self.doc = doc 

    ######################################################################################  
    def GetDocument(self):   
        return self.doc 

    ###############################################################################################
    def ouvrir(self, nomFichier):
        print("Ouverture classe", nomFichier)
        
        root = safeParse(nomFichier, None)
        if root is None:
            return False
        
        self.setBranche(root)
        if int(self.version.split(".")[0]) < 8:
            self.setBranche(root, reparer = True)
            
        self.app.fichierClasse = nomFichier
        
        return True
#         try:
#             fichier = open(nomFichier,'r')
#     
#             root = ET.parse(fichier).getroot()
#             self.setBranche(root)
#             
#             fichier.close()
#             self.app.fichierClasse = nomFichier
#             
#             return True
# 
#         except:
#             print("Erreur Ouverture classe", nomFichier)
#             return False
        
#        self.MiseAJour()


    ######################################################################################  
    def getBranche(self):
#        print "getBranche classe"
        # La classe
        classe = ET.Element("Classe")
        classe.set("Type", self.typeEnseignement)
        classe.set("Spe", " ".join(self.specialite))
        
        classe.set("Version", version.__version__) # à partir de la version 6
        
        classe.append(self.referentiel.getBranche())
        
        classe.set("Etab", self.etablissement)
        classe.set("Ville", self.ville)
        classe.set("Acad", self.academie)
        
        eff = ET.SubElement(classe, "Effectifs")
        eff.set('eC', str(self.effectifs['C']))
        eff.set('nG', str(self.nbrGroupes['G']))
        eff.set('nS', str(self.nbrGroupes['S']))
        eff.set('nT', str(self.nbrGroupes['T']))
        eff.set('nU', str(self.nbrGroupes['U']))
        eff.set('nE', str(self.nbrGroupes['E']))
        eff.set('nP', str(self.nbrGroupes['P']))
                     
#        print "   ", self.systemes
        systeme = ET.SubElement(classe, "Systemes")
        for sy in self.systemes:
            if sy.nom != "":
                systeme.append(sy.getBranche())
        
        return classe
    
    ######################################################################################  
    def setBranche(self, branche, reparer = False):
        err = []
#         print("setBranche classe")
        self.typeEnseignement = branche.get("Type", constantes.TYPE_ENSEIGNEMENT_DEFAUT)
        
        self.version = branche.get("Version", "0")       # A partir de la version 6 !
        
        #
        # Référentiel
        #
        def ChargerRefOriginal():
#             print("Réparation = pas référentiel intégré !")
            if self.GetVersionNum() >= 5:
                code = self.referentiel.setBrancheCodeV5(brancheRef)
#                 print("   Code trouvé dans référentiel :", code)
                if code is not None and code != self.typeEnseignement:
                    self.typeEnseignement = code
                
            if self.typeEnseignement in REFERENTIELS:
#                 print("   TypeEnseignement :", self.typeEnseignement)
                self.referentiel = REFERENTIELS[self.typeEnseignement]
                self.referentiel.postTraiter()
                self.referentiel.completer(forcer = True)
            else:
                err.append(constantes.Erreur(constantes.ERR_PRJ_C_TYPENS, self.typeEnseignement))
            
            
                
                
        def RecupCI():
            if self.GetVersionNum() < 5:
                brancheCI = branche.find("CentreInteret")
                if brancheCI != None: # Uniquement pour rétrocompatibilité : normalement cet élément existe !
                    continuer = True
                    i = 1
                    if self.typeEnseignement == 'ET':
                        CI = []
                        posCI = []
                        while continuer:
                            c = brancheCI.get("CI"+str(i))
                            p = brancheCI.get("pos"+str(i))
                            if c == None or p == None:
                                continuer = False
                            else:
                                CI.append(c)
                                posCI.append(p) 
                                i += 1
                            
                        if i > 1:
    #                        self.CI = CI
                            if self.referentiel.CI_cible:
                                self.referentiel.positions_CI = posCI
                                
            elif self.GetVersionNum() == 5:
                brancheCI = branche.find("l_CentresInterets")
                if brancheCI != None: 
                    continuer = True
                    i = 1
                    if self.typeEnseignement == 'ET':
                        CI = []
                        posCI = []
                        while continuer:
                            c = brancheCI.get("S_CentresInterets"+format(i, "02d"))
                            p = brancheCI.get("S_positions_CI"+format(i, "02d"))
                            if c == None or p == None:
                                continuer = False
                            else:
                                CI.append(c)
                                posCI.append(p) 
                                i += 1
                            
                        if i > 1:
                            if self.referentiel.CI_cible:
                                self.referentiel.positions_CI = posCI
    
    
   
        #
        # A partir de la version 5 !
        #
        brancheRef = branche.find("Referentiel")
        if brancheRef != None:   
            self.referentiel = Referentiel.Referentiel()
            if self.GetVersionNum() == 0:       # la version n'était pas encore intégrée dans la version 5 !
                self.version = "5" 
                
            #
            # Ouverture du référentiel original (fourni avec pySéquence)
            #
            if reparer:
                ChargerRefOriginal()
            
            #
            # Ouverture du référentiel intrégré
            #
            else:
#                 print("VersionNum", self.GetVersionNum())
#                versionNum = self.GetVersionNum()
                if self.GetVersionNum() <= 6:
                    ChargerRefOriginal()
                    RecupCI()
                else:
#                     try:
                    self.referentiel.initParam()
#                     print("***", self.referentiel.nomSeances)
                    errr = self.referentiel.setBranche(brancheRef)[1]
#                     print("***", self.referentiel.nomSeances)
#                     print("errr", errr)
                    self.referentiel.corrigerVersion(errr)
#                     print("***", self.referentiel.nomSeances)
                    self.referentiel.postTraiter()
                    self.referentiel.completer(forcer = True)
#                     print("***", self.referentiel.nomSeances)
#                     except:
#                         self.referentiel.initParam()
#                         self.referentiel.setBrancheV5(brancheRef)
#                         ChargerRefOriginal()
#                         RecupCI()



        #
        # Version < 5 !
        #
        else:
            ChargerRefOriginal()
            RecupCI()
        
        # Correction contradiction 
        if self.typeEnseignement != self.referentiel.Code:
            print("Correction type enseignement", self.typeEnseignement, ">>", self.referentiel.Code)
            self.typeEnseignement = self.referentiel.Code

        #
        # Spécialité
        #
        self.specialite = branche.get("Spe", "").split()
#         print("self.specialite", self.specialite)
        #
        # Etablissement
        #
        self.etablissement = branche.get("Etab", "")
        self.ville = branche.get("Ville", "")
        self.academie = branche.get("Acad", "")
        
        self.familleEnseignement = self.referentiel.Famille

        #
        # Effectifs
        #
        # Ancien format : <Effectifs C="9" D="3" E="2" G="9" P="3" />
        # Nouveau format : <Effectifs eC="9" nE="2" nG="9" nP="3" />
        brancheEff = branche.find("Effectifs")
        
        if brancheEff.get('eC') == None: # Ancienne version
            self.effectifs['C'] = eval(brancheEff.get('C', "1"))
            revCalculerEffectifs(self, eval(brancheEff.get('G', "1")), eval(brancheEff.get('E', "1")), eval(brancheEff.get('P', "1")))

        else:
            self.effectifs['C'] = eval(brancheEff.get('eC', "1"))
            self.nbrGroupes['G'] = eval(brancheEff.get('nG', "1"))
            self.nbrGroupes['S'] = eval(brancheEff.get('nS', "1"))
            self.nbrGroupes['T'] = eval(brancheEff.get('nT', "0"))
            self.nbrGroupes['U'] = eval(brancheEff.get('nU', "0"))
            self.nbrGroupes['E'] = eval(brancheEff.get('nE', "1"))
            self.nbrGroupes['P'] = eval(brancheEff.get('nP', "1"))
            calculerEffectifs(self)
        
        #
        # Systèmes
        #
        self.systemes = []
        brancheSys = branche.find("Systemes")
        if brancheSys != None:
            for sy in list(brancheSys):
                systeme = Systeme(self)
                systeme.setBranche(sy)
                self.systemes.append(systeme)    
            self.systemes.sort(key=attrgetter('nom'))
#         print "systèmes Classe :", self.systemes
#        self.GetPanelPropriete().MiseAJour()
        
        return err
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
#         print("ConstruireArbre", self.GetReferentiel().Enseignement[0], self.specialite)
#         print err
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre, 
                                       rallonge(self.GetLabel()))
        self.branche = arbre.AppendItem(branche, Titres[5]+" :", wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Cla"])
        self.codeBranche.SetBranche(self.branche)
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)
    
    
    ######################################################################################  
    def GetLabel(self):
        if len(self.specialite) > 0:
            return self.GetReferentiel().Enseignement[0]+" - "+"+".join(self.specialite)
        else:
            return self.GetReferentiel().Enseignement[0]
    
    ######################################################################################  
    def GetLabelComplet(self):
#         print("GetLabelComplet", self.specialite)
        if len(self.specialite) > 0:
            return self.GetReferentiel().Enseignement[1] \
                +"\n" \
                +" + ".join([self.GetReferentiel().specialite[s][1] for s in self.specialite])
        else:
            return self.GetReferentiel().Enseignement[1]
        
    
#     ######################################################################################  
#     def GetEffectifNorm2(self, eff):
#         """ Renvoie les effectifs des groupes sous forme normalisée (de 0.0 à 1.0)
#             (portion de classe entière)
#         """
#         if eff == 'C':
#             return 1.0
#         
#         elif eff == 'G':
#             return 1.0 / self.nbrGroupes['G']
#         
#         elif eff == 'D':
#             return self.GetEffectifNorm('G') / 2
#         
#         elif eff == 'E':
#             return self.GetEffectifNorm('G') / self.nbrGroupes['E']
#         
#         elif eff == 'P':
#             return self.GetEffectifNorm('G') / self.nbrGroupes['P']
#         
#         elif eff == 'I':
#             return 1 / self.effectifs['C']
#         
#         else:
#             print("ERREUR", eff)
    
    ######################################################################################  
    def GetNbrCouches(self, k):
        """ Renvoie le nombre de fois que l'activité de code-effectif 'k' est faite
            
        """
#         print("GetNbrCouches", k)
        ref = self.GetReferentiel()
        
        if len(ref.effectifs[k]) >= 6 and ref.effectifs[k][5] == "O":
            # Les éventuelles couches supplémentaires
            # pour séances à effectif dont tous les sous-groupes font les mêmes activités
            n = self.nbrGroupes[k]
        else:
            n = 1
            
        if len(ref.effectifs[k]) >= 5 and ref.effectifs[k][4] != '':
            n *= self.GetNbrCouches(ref.effectifs[k][4])
        
#         print("  >>>> :", n)
        return n
    
    
    ######################################################################################  
    def GetStrEffectif(self, e, n = 0, eleve = True):
        if e == "C":
            return str(self.effectifs[e])
        else:
            ref = self.GetReferentiel()
            if e in self.effectifs:
                lsteff = self.effectifs[e]
                if type(lsteff[0]) == list:
                    lsteff = lsteff[0]
                if n == -1:
                    mini, maxi = min(lsteff), max(lsteff)
                    if mini != maxi:
                        eff_str = str(mini) + "-" + str(maxi)
                    else:
                        eff_str = str(mini)
                    eleves = ref.labels["ELEVES"][2].plur_()
                else:
                    eff_str = str(lsteff[n])
                    if lsteff[n] == 1:
                        eleves = ref.labels["ELEVES"][2].sing_()
                    else:
                        eleves = ref.labels["ELEVES"][2].plur_()
                if eleve:
                    return eff_str+" "+eleves
                else:
                    return eff_str
            else:
                return ""
    
    
    ######################################################################################  
    def GetStrEffectifComplet(self, e, n = 0):
        tit_eff = self.GetReferentiel().effectifs[e][0]
        num_eff = self.GetStrEffectif(e, n)
        if num_eff != "":
            return tit_eff+" ("+num_eff+")"
        else:
            return tit_eff

    
    ######################################################################################  
    def GetEffectifNorm(self, eff):
        """ Renvoie les effectifs des groupes sous forme normalisée (de 0.0 à 1.0)
            (portion de classe entière)
        """
        ref = self.GetReferentiel()
        
        if eff == 'C':  # classe entière
            return 1.0
        
        elif eff == 'I':    # individuel
            return 1.0 / self.effectifs['C']
        
        else:
            if eff in self.nbrGroupes and self.nbrGroupes[eff] > 0:
                if ref.effectifs[eff][5] == "N":
                    return self.GetEffectifNorm(ref.effectifs[eff][4]) / self.nbrGroupes[eff]
                else:
                    return self.GetEffectifNorm(ref.effectifs[eff][4])
            else:
                return 0
        
    
    ######################################################################################  
    def GetReferentiel(self):
        return self.referentiel
       
    ######################################################################################  
    def GetVersion(self):
        if hasattr(self, 'version'):
            v = self.version
        elif hasattr(self, 'doc'):
            v = self.doc.version
        if v == '':
            return version.__version__
        else:
            return v
        
    ######################################################################################  
    def GetVersionNum(self):
#         print "GetVersionNum", self.GetVersion()
        return int(self.GetVersion().split(".")[0].split("beta")[0])
    
    
    ######################################################################################  
    def GetPeriodes(self):
        """ Liste des périodes "libres" 
            parmi les périodes du Référentiel
        """
#         print("GetPeriodes", self.specialite)
        if len(self.specialite) > 0:
            ep = self.GetReferentiel().getPeriodeSpe(self.specialite)
#             print("   ", ep)
            return list(range(ep[0], ep[1]+1))
        else:
            return list(range(sum([p for a, p in self.GetReferentiel().periodes])))
        
        
        
    #############################################################################            
    def getBitmapPeriode(self, larg):
#         print("getBitmapPeriode", self.GetPeriodes())
        imagesurface = draw_cairo.getBitmapPeriode(larg, self.GetPeriodes(),
                                                       self.GetReferentiel().periodes, 
                                                       prop = 7)
        return getBitmapFromImageSurface(imagesurface)
    
    
    #############################################################################            
    def getBitmapEffectifs(self, W, H):
#         return wx.Bitmap(larg, larg)
        imagesurface = draw_cairo.getBitmapClasse(W, H, self)

        return getBitmapFromImageSurface(imagesurface)
    
    
    
    ######################################################################################  
    def Verrouiller(self, etat):
#        print "verrouiller classe", etat
        self.verrouillee = etat
#        self.GetPanelPropriete().Verrouiller(etat)
        if not etat:
            couleur = 'white'
            message = ""
        else:
            couleur = COUL_OK
            ref = self.GetReferentiel()
            message = "Les paramètres de la classe sont verrouillés !\n" \
                      "Pour pouvoir les modifier, supprimer %s\n"\
                      "ainsi que les prérequis et les objectifs." %ref._nomCI.les_()
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetBackgroundColour(couleur)
            self.codeBranche.SetToolTip(message)
            self.codeBranche.Refresh()

    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.encap_HTML(constantes.BASE_FICHE_HTML_CLASSE)
    
    
    
    ######################################################################################  
    def SetTip(self, param = None, obj = None):
        """ Mise à jour du TIP (popup)
        """
        bmp = self.getBitmapEffectifs(800, 400)
        self.tip.SetHTML(self.GetFicheHTML())

        self.tip.AjouterImg("eff", bmp)
            
        self.tip.SetPage()


####################################################################################################
#
# Classe définissant les documents principaux
#        base : BaseDoc
#        héritiers : Sequence et Projet
#
####################################################################################################
class BaseDoc(ElementBase, ElementAvecLien):
    """Classe de base pour les documents (Séquence, Projet ou Progression)
    
        :param app: Fenêtre où s'affiche le document
        :type app: wx_pysequence.FenetreDocument
        :param classe: Classe associée au document
        :type classe: pysequence.Classe
        :param intitule: Intitulé du document
        :type intitule: str
    """
    
    def __init__(self, app, classe = None, intitule = ""):
        self.app = app  # de type FenentreDocument
        ElementBase.__init__(self)
        ElementAvecLien.__init__(self)
        
        self.intitule = intitule
        self.classe = classe
        
        self.version = "" # version de pySéquence avec laquelle le fichier a été sauvegardé
        
        self.centrer = True
        self.surbrillance = None # Objet à afficher en surbrillance
        
        # Année Scolaire
        self.annee = constantes.getAnneeScolaire()
        self.position = [0, 0]   # Position de la séquence/projet dans la période d'enseignement
        
        self.commentaires = ""
        
        self.dependants = [] # Liste de documents dépendants (à enregistrer aussi)

        # Gestion des Undo/Redo
        self.undoStack = UndoStack(self)
        wx.CallAfter(self.undoStack.do, "Création "+self.du_())
        
        self.path = ""
        
        self.proprietes = proprietes.ProprietesDoc(self)
        
        #
        # Création du Tip (PopupInfo)
        #
        self.tip = PopupInfo(self.GetApp().parent, width = 1000*SSCALE)
        self.zoneMove = None
        self.curTip = None
        
        
    ######################################################################################  
    def __lt__(self, doc):
        if self.GetPosition()[0] == doc.GetPosition()[0]:
            dp0 = self.GetPosition()[-1]-self.GetPosition()[0]
            dp1 = doc.GetPosition()[-1]-doc.GetPosition()[0]
            return dp0 < dp1
        else:
            return self.GetPosition()[0] < doc.GetPosition()[0]
        
    
    ######################################################################################  
    def GetCode(self, num = None):
        """ Renvoie le code du Document à partir de son num'
        """
        return self.GetType()+str(num)
        
        
    ######################################################################################  
    def GetApp(self):
        return self.app
    
    ######################################################################################  
    def SetPath(self, path):
        self.path = path
        
    
    ######################################################################################  
    def GetPath(self):
        if hasattr(self.app, 'fichierCourant'):
            return os.path.split(self.app.fichierCourant)[0]
        else:
            return self.path
    
    
#     ######################################################################################  
#     def getBranche(self):
#         """ Renvoie la branche XML pour enregistrement
#         """
#         # Création de la racine
#         prop = ET.Element("Proprietes")
#         
# 
#         
#         return prop
# 
# 
#     ######################################################################################  
#     def setBranche(self, branche, reparer = False):
#         """ Lecture d'une branche XML
#         """
#         err = []
#         
# 
#         
#         return err
        



    ######################################################################################  
    def GetAnnees(self):
        return "%s - %s" %(self.annee, self.annee+1)

    ######################################################################################  
    def GetPositions(self):
        return list(range(self.position[0], self.position[1]+1))
    

    ######################################################################################  
    def GetNbrPeriodes(self):
        return sum([p for a, p in self.GetReferentiel().periodes])
    
    
    #############################################################################            
    def getRangePeriode(self):
        return list(range(self.position[0], self.position[1]+1))
    
#     #############################################################################            
#     def getNomEleves(self):
#         return self.GetReferentiel().labels['ELEVES'][0]
    
    ######################################################################################  
    def estProjet(self):
        return isinstance(self, Projet)
    

    ######################################################################################  
    def GetApercu(self, w = 210, h = -1, entete = False):
        imagesurface = draw_cairo.get_apercu(self, w, entete = entete)
        img = getBitmapFromImageSurface(imagesurface).ConvertToImage().Scale(w, w*1.414)
        if h == -1:
            return img.ConvertToBitmap()
        else:
            return img.Resize((w, h), (0,0)).ConvertToBitmap()


    ######################################################################################  
    def restaurer(self, root):
        if self.panelParent != None:
            self.panelParent.restaurer(root)
            
    ######################################################################################  
    def SetText(self, text):
        self.intitule = text
    
    ######################################################################################  
    def SetPosition(self, pos):
        self.position = pos
        
    ######################################################################################  
    def SetCommentaire(self, text):
        self.commentaires = text  
        
    ######################################################################################  
    def AfficherLien(self, item):
        data = self.arbre.GetItemPyData(item)
        if data and data != self and hasattr(data, 'AfficherLien'):
            data.AfficherLien(self.GetPath())

    ######################################################################################  
    def SelectItem(self, branche, depuisFiche = False):
        self.centrer = not depuisFiche
        self.arbre.EnsureVisible(branche)
        for i in self.arbre._itemWithWindow:
            self.arbre.HideWindows()
        self.arbre.SelectItem(branche) 

    
    ######################################################################################  
    def HideTip(self, pos = None):
        if hasattr(self, 'call'):
            self.call.Stop()
            
        if self.curTip is not None:#hasattr(self, 'curTip'):
            if pos is not None:
                x, y = pos
#                 print x, y
                X, Y, W, H = self.curTip.GetRect()
#                 print X, Y, W, H
                if x > X and x < X+W and y > Y and y < Y+H:
                    return
            self.curTip.Show(False)
        
        
            
            
    ######################################################################################  
    def HitTest(self, x, y):
        """ >> Renvoie la Zone sensible sous le point x, y
        """
#        print "HitTest"
        if hasattr(self, 'zones_sens'):
            for z in self.zones_sens:
                if z.dansRectangle(x, y):
    #                print "   xxx", z
                    return z
            return


    ######################################################################################  
    def GererDependants(self, obj, t):
        """ Gestion des documents qui dépendent du présent document
        """
#         print("GererDependants", obj, t)
#         print(self.GetApp(), obj.GetApp())
        self.GetApp().sendEvent(modif = t, obj = self)
        if self.GetApp() == obj.GetApp(): # le document n'est pas ouvert dans une autre fenêtre
            self.dependants.append(obj)
        else:
            obj.GetApp().sendEvent(modif = t, obj = self)
        
        
    ######################################################################################  
    def Click(self, zone, x, y):
#         print("Click", zone)
        self.HideTip()
        
        if zone.obj is not None:
            if zone.param is None:
#                 print("   ", zone.obj)
                if hasattr(zone.obj, "branche"):
                    if hasattr(zone.obj, "branches") and len(zone.obj.branches.values()) > 0:
                        self.SelectItem(list(zone.obj.branches.values())[0], depuisFiche = True)
                    else:
                        self.SelectItem(zone.obj.branche, depuisFiche = True)
                elif hasattr(zone.obj, "branchePre"):
                    self.SelectItem(zone.obj.branchePre, depuisFiche = True)
            
            else:
                ref = self.GetReferentiel()
                if isinstance(zone.obj, Sequence) and len(zone.param) > 2 and zone.param[:2] == "CI":
                    zone.obj.CI.ToogleNum(int(zone.param[2:]))
                    t = "Modification "+ ref._nomCI.des_() + " de la Séquence"
                    pp = self.GetApp().GetPanelProp()
                    if hasattr(pp, "MiseAJourApercu"):
                        pp.MiseAJourApercu()
                    self.GererDependants(zone.obj, t)
                
                elif isinstance(zone.obj, Sequence) and len(zone.param) > 3 and zone.param[:3] == "CMP":
#                     print("Click : S"+zone.param[3:])
#                     print(zone.obj.obj['C'])
                    zone.obj.obj['C'].ToogleCode("S"+zone.param[3:])
                    t = "Modification "+ ref.dicoCompetences["S"]._nom.des_() + " visées par la Séquence"
                    pp = self.GetApp().GetPanelProp()
                    if hasattr(pp, "MiseAJourApercu"):
                        pp.MiseAJourApercu()
                    self.GererDependants(zone.obj, t)
                        
        
        elif zone.param is not None:
            if len(zone.param) > 3 and zone.param[:3] == "POS" :
                if not self.classe.verrouillee:
                    p = int(zone.param[3])
                    if p-self.position[0] > self.position[1]-p+1:
#                     if p > self.position[0]:
                        self.SetPosition([self.position[0], p])
                    else:
                        self.SetPosition([p, self.position[1]])
#                    self.GetPanelPropriete().SetBitmapPosition()
                    pp = self.GetApp().GetPanelProp()
                    if hasattr(pp, "SetBitmapPosition"):
                        pp.SetBitmapPosition()
#                    self.GetApp().arbre.OnSelChanged()
                    self.GetApp().sendEvent(modif = "Changement de position "+ self.du_(),
                                            obj = self)
            
            elif zone.param == "PB":
                self.SelectItem(self.branche, depuisFiche = True)
            
            elif zone.param == "EQU":
                self.SelectItem(self.branchePrf, depuisFiche = True)
                

#     ######################################################################################  
#     def GetTip(self):
#         return self.tip
        
    
#     ######################################################################################  
#     def ShowTip(self, x, y, obj, zone): 
#         tip = obj.GetTip()
#         if self.tip != tip:
#             if obj != self:
#                 obj.SetTip()
#             else:
#                 obj.SetTip(zone.param, zone.obj)
#             tip = obj.GetTip()
#         if tip != None:
#             w, h = tip.GetSize()
#             X, Y, W, H = getDisplayPosSize()
#             tip.Position(getAncreFenetre(x, y, w, h, W, H, 10), (0,0))
#             tip.Show()
#             self.tip = tip
        
    
    ######################################################################################  
    def Move(self, zone, x, y):
#         print "Move", x, y, zone
            
        self.HideTip()
        
        if self.zoneMove != zone:
            self.call = wx.CallLater(500, self.SetAndShowTip, zone, x, y)
            
        else:
            self.call = wx.CallLater(500, self.ShowTip, x, y)


    ######################################################################################  
    def ShowTip(self, x, y):
        if self.curTip is None: return
        
        X, Y, W, H = getDisplayPosSize()
        w, h = self.curTip.GetSize()
        self.curTip.Position(getAncreFenetre(x, y, w, h, W, H, 10), (0,0))
        self.curTip.Show()
    
        
    ######################################################################################  
    def SetAndShowTip(self, zone, x, y):
#         print "SetAndShowTip", x, y
             
#         self.HideTip()
        self.zoneMove = zone
        
        self.curTip = None 
        if zone.obj is not None and zone.param is None:
#             print "    elem :", zone.obj
            if type(zone.obj) != list:
             
                if hasattr(zone.obj, 'tip'):
                    zone.obj.SetTip()
                    self.curTip = zone.obj.tip
            else:
                if hasattr(zone.obj[0], 'tip'):
                    zone.obj[0].SetTip()
                    self.curTip = zone.obj[0].tip
         
        else:
#             print "    zone", zone.param
            self.SetTip(zone.param, zone.obj)
            self.curTip = self.tip
             
        if self.curTip != None:
            self.ShowTip(x, y)
#             X, Y, W, H = getDisplayPosSize()
#  
# #             print "  tip", x, y, tip.GetSize()
#  
#             w, h = tip.GetSize()
#             tip.Position(getAncreFenetre(x, y, w, h, W, H, 10), (0,0))
# #             self.call = wx.CallLater(500, tip.Show, True)
#             tip.Show()
            
#             
            
            
    ######################################################################################  
    def MiseAJourListeSystemesClasse(self):
        return


    ######################################################################################  
    def AjouterProf(self, event = None):
        if len(self.equipe) < 8:
            e = Prof(self, len(self.equipe))
            self.equipe.append(e)
            if not hasattr(self, 'branchePrf'):
                self.branchePrf = self.arbre.InsertItem(self.branche, 3, Titres[10], 
                                                   data = "Equ")
            
            e.ConstruireArbre(self.arbre, self.branchePrf)
            self.arbre.Expand(self.branchePrf)
            self.GetApp().sendEvent(modif = "Ajout d'un professeur")
            self.arbre.SelectItem(e.branche)

    
    ######################################################################################  
    def SupprimerProf(self, event = None, item = None):
        e = self.arbre.GetItemPyData(item)
#        i = self.equipe.index(e)
        self.equipe.remove(e)
        self.arbre.Delete(item)
        if len(self.equipe) == 0:
            self.arbre.Delete(self.branchePrf)
            del self.branchePrf
        self.GetApp().sendEvent(modif = "Suppression d'un professeur")


    ######################################################################################  
    def MiseAJourNomProfs(self):
        for e in self.equipe:
            e.SetCode()
            e.MiseAJourCodeBranche()
            
            
    ######################################################################################  
    def MiseAJourNomsEleves(self):
        pass
            
    
    ######################################################################################  
    def SetReferent(self, personne, referent):
        for p in self.equipe:
            if p == personne:
                p.referent = referent
            else:
                if referent:
                    p.referent = False
#            p.panelPropriete.MiseAJour()
        self.MiseAJourNomProfs()
            
            
    
        


    ##################################################################################################    
    def Tip_POS(self, p = None):
        if p == None:
            self.tip.SetWholeText("titre", "Découpage de la formation en périodes")
            self.tip.SetWholeText("txt", "Périodes occupées pendant la Progression")
            self.tip.AjouterImg("img", self.getBitmapPeriode(300))
        else:
            ref = self.GetReferentiel()
            self.tip.SetWholeText("titre", "Période de formation")
            self.tip.SetWholeText("txt", ref.getPeriodesListe()[p] + " - " + str(p+1))
            self.tip.Supprime('img')


    ##################################################################################################    
    def Tip_EQU(self, typeDoc):
        self.tip.SetWholeText("titre", "Équipe pédagogique impliquée dans " + typeDoc)
        self.tip.Supprime('img')
    
    

    
####################################################################################################          
class Sequence(BaseDoc):
    """Document de type Séquence pédagogique
    
        :param app: Fenêtre où s'affiche la Séquence
        :type app: wx.pysequence.FenetreDocument
        :param ouverture: Indique s'il faut ouvrir la Séquence dans une fenêtre
        :type ouverture: bool
        :param classe: Classe associée au document
        :type classe: pysequence.Classe
        :param intitule: Intitulé du document
        :type intitule: str
    """
    def __init__(self, app, classe = None, intitule = "",
                 ouverture = False):
        

        Grammaire.__init__(self, "Séquence(s)$f")
        BaseDoc.__init__(self, app, classe, intitule)
        
        self.prerequisSeance = []
        
        self.equipe = []
        
        self.domaine = ""   # M E I
        
        self.CI = CentreInteret(self)
        
        self.prerequis = {"C" : Competences(self, prerequis = True),
                          "S" : Savoirs(self, prerequis = True)}
        
        self.obj = {"C" : Competences(self),
                    "S" : Savoirs(self)}
        
        self.systemes = []
        self.seances = [Seance(self)]

        if not ouverture:
            self.MiseAJourTypeEnseignement()
            
        # Le module de dessin
        self.draw = draw_cairo_seq
        


#     ######################################################################################  
#     def __repr__(self):
#         return "Séquence" + self.intitule


    ######################################################################################  
    def GetType(self):
        return 'seq'


    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Sequence(parent, self)

    
    ######################################################################################  
    def Initialise(self):
#         self.AjouterListeSystemes(self.classe.systemes)
        self.MiseAJourTypeEnseignement()
#        self.AjouterListeSystemes(self.options.optSystemes["Systemes"])
            
            
    ######################################################################################  
    def SetPath(self, fichierCourant):
        """  <fichierCourant> encodé en FileEncoding
        """
        pathseq = os.path.split(fichierCourant)[0]
        for sce in self.seances:
            sce.SetPathSeq(pathseq)    
        for sy in self.systemes:
            sy.SetPathSeq(pathseq) 


    ######################################################################################  
    def GetDuree(self):
        duree = 0
        for s in self.seances:
            duree += s.GetDuree()
        return duree
    
    
    ######################################################################################  
    def GetProfondeur(self):
        return max([s.GetProfondeur() for s in self.seances])


    ######################################################################################  
    def GetNiveau(self):
        return 0


    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
#         print("GetPtCaract Seq")
        lst = BaseDoc.GetPtCaract(self)
        
        lst.extend(self.obj["C"].GetPtCaract())
        lst.extend(self.obj["S"].GetPtCaract())
        lst.extend(self.prerequis["S"].GetPtCaract())
        lst.extend(self.prerequis["C"].GetPtCaract())
        lst.extend(self.CI.GetPtCaract())
        for s in self.seances:
            lst.extend(s.GetPtCaract())
            
#         print(">>>", lst)
        return lst    
    
    ######################################################################################  
    def EnrichiHTMLdoc(self, doc):
        """ Enrichissement de l'image SVG <doc> (format XML) avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens
             - ...
             :doc: beautifulsoup
        """
#        print "EnrichiHTML sequence"
        ElementBase.EnrichiHTML(self, doc)
        
        self.obj["C"].EnrichiHTML(doc)
        self.obj["S"].EnrichiHTML(doc)
        self.prerequis["C"].EnrichiHTML(doc)
        self.prerequis["S"].EnrichiHTML(doc)
        self.CI.EnrichiHTML(doc)
        for s in self.seances:
            s.EnrichiHTMLse(doc)
            
            
            
    ######################################################################################  
    def EnrichiSVGdoc(self, doc):
        """ Enrichissement de l'image SVG <doc> (format XML) avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens
             - ...
             :doc: xml.doc.minidom
        """
#        print "EnrichiSVG sequence"
        if hasattr(self, 'app'):
            t = doc.createElement("title")
            path = os.path.split(self.app.fichierCourant)[1]
            path = str(path) # Conversion en unicode !!!
            txt = doc.createTextNode(path)
            
            t.appendChild(txt)
            svg = doc.getElementsByTagName("svg")[0]
            svg.insertBefore(t, svg.childNodes[0])
        
        
        ElementBase.EnrichiSVG(self, doc)
        
        
        self.obj["C"].EnrichiSVG(doc)
        self.obj["S"].EnrichiSVG(doc)
        self.prerequis["C"].EnrichiSVG(doc)
        self.prerequis["S"].EnrichiSVG(doc)
        self.CI.EnrichiSVG(doc)
        for s in self.seances:
            s.EnrichiSVGse(doc)
        
        
    ######################################################################################  
    def GetDureeGraph(self):
        duree = 0
        for s in self.seances:
            duree += s.GetDureeGraph()
        return duree
            
    ######################################################################################  
    def GetDureeGraphMini(self):
        duree = 10000
        for s in self.seances:
            duree = min(duree, s.GetDureeGraphMini())
        return duree
    
    
    ######################################################################################  
    def getIcone(self):
        return scaleImage(images.Icone_sequence.GetBitmap())

    ######################################################################################  
    def getIconeDraw(self):
        return scaleImage(images.Icone_sequence.GetBitmap(), 100,100)

    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la séquence pour enregistrement
        """
#         tps = time.clock()
        
        
        # Création de la racine
        sequence = ET.Element("Sequence")
        
        sequence.set("Intitule", self.intitule)
        
        self.lien.getBranche(sequence)

        if self.commentaires != "":
            sequence.set("Commentaires", self.commentaires)
        
        
        sequence.set("Domaine", self.domaine)

        sequence.set("Position", "_".join([str(p) for p in self.position]))

        equipe = ET.SubElement(sequence, "Equipe")
        for p in self.equipe:
            equipe.append(p.getBranche())
            
        sequence.append(self.CI.getBranche())
        
        
        prerequis = ET.SubElement(sequence, "Prerequis")
        prerequis.append(self.prerequis["S"].getBranche())
        prerequis.append(self.prerequis["C"].getBranche())
        for ps in self.prerequisSeance:
            prerequis.append(ps.getBranche())
        
#        self.getBrancheList(sequence,  "Objectifs", self.obj)
        
        
        objectifs = ET.SubElement(sequence, "Objectifs")
        for obj in self.obj.values():
            objectifs.append(obj.getBranche())
            
        seances = ET.SubElement(sequence, "Seances")
        for sce in self.seances:
            seances.append(sce.getBranche())
        
        
        
        systeme = ET.SubElement(sequence, "Systemes")
        for sy in self.systemes:
#            c = hasattr(sy, 'panelPropriete') and sy.panelPropriete.cbListSys.GetStringSelection() != u""
            if isinstance(sy.parent, Classe):
                systeme.append(sy.getBrancheClasse())
            else:
                systeme.append(sy.getBranche())
        
#         print("1 :", time.clock() - tps)
        
        return sequence


    ######################################################################################  
    def setBranche(self, branche, reparer = False):
        """ Lecture d'une branche XML de séquence
        """
        
#         print "setBranche séquence"
#        t0 = time.time()
        err = []
        
        self.intitule = branche.get("Intitule", "")
#         print self.intitule
        self.lien.setBranche(branche, self.GetPath())
        
        self.commentaires = branche.get("Commentaires", "")
        
        self.domaine = branche.get("Domaine", "")
        
#         self.position = eval(branche.get("Position", "0"))
        sp = branche.get("Position", "0_0")
        sp = sp.split("_")
        if len(sp) == 1:
            sp = [sp[0], sp[0]]
        self.position = [int(sp[0]), int(sp[1])]

        brancheEqu = branche.find("Equipe")
        self.equipe = []
        if brancheEqu != None:
            for e in list(brancheEqu):
                prof = Prof(self)
                Ok = prof.setBranche(e)
                self.equipe.append(prof)
            
        brancheCI = branche.find("CentresInteret")
        if brancheCI != None:
            self.CI.setBranche(brancheCI)
        
        # Pour rétro compatibilité
        if self.CI.numCI == []:
            brancheCI = branche.find("CentreInteret")
            if brancheCI != None:
                self.CI.setBranche(brancheCI)
            
#        t1 = time.time()
#        print "  t1", t1-t0
        branchePre = branche.find("Prerequis")
        if branchePre != None:
            savoirs = branchePre.find("Savoirs")
            self.prerequis["S"].setBranche(savoirs)
            
            comp = branchePre.find("Competences")
            if comp != None:
                self.prerequis["C"].setBranche(comp)
                
            lst = list(branchePre)
            lst.remove(savoirs)
            if comp in lst:
                lst.remove(comp)
                
            self.prerequisSeance = []
            for bsp in lst:
                sp = LienSequence(self)
                sp.setBranche(bsp)
                self.prerequisSeance.append(sp)
                sp.ChargerSequence(reparer = reparer)
        
#        t2 = time.time()
#        print "  t2", t2-t1
        
        brancheObj = branche.find("Objectifs")
#        self.obj = []
#        for obj in list(brancheObj):
#            comp = Competence(self, self.panelParent)
#            comp.setBranche(obj)
#            self.obj.append(comp)
        self.obj["C"].setBranche(list(brancheObj)[0])
        self.obj["S"].setBranche(list(brancheObj)[1])
        
        
        
        brancheSys = branche.find("Systemes")
        self.systemes = []
        for sy in list(brancheSys):
            systeme = Systeme(self)
            systeme.setBranche(sy)
            # On évite les systèmes redondants (correction d'un bug)
            if systeme.lienClasse == None:# or  not systeme.lienClasse in [s.lienClasse for s in self.systemes]:
                self.systemes.append(systeme)
            else:
                if not systeme.lienClasse in [s.lienClasse for s in self.systemes]:
                    self.systemes.append(systeme.lienClasse)
#             print("sy", self.systemes[-1].parent)

#        t3 = time.time()
#        print "  t3", t3-t2
        
        brancheSce = branche.find("Seances")
        self.seances = []
        for sce in list(brancheSce):         
            seance = Seance(self)
            seance.setBranche(sce)
            self.seances.append(seance)
            
#        t4 = time.time()
#        print "  t4", t4-t3
        
        self.OrdonnerSeances()
        
        return err
        
#        self.GetPanelPropriete().MiseAJour()

        
#        t5 = time.time()
#        print "  t5", t5-t4
        
    ######################################################################################  
    def SetCodes(self):
#        self.CI.SetNum()
#        for comp in self.obj:
#            comp.SetCode()
#         self.obj["C"].SetCode()
#         self.obj["S"].SetCode()
        
        for sce in self.seances:
            sce.SetCode()    
            
        for sy in self.systemes:
            sy.SetCode()    
        
        for ps in self.prerequisSeance:
            ps.SetLabel()
            
    ######################################################################################  
    def PubDescription(self):
        for sce in self.seances:
            sce.PubDescription()    
#            
#        for sy in self.systemes:
#            sy.SetDescription()    
        

            
            
    ######################################################################################  
    def SetLiens(self):
        for sce in self.seances:
            sce.SetLien()    

        for sy in self.systemes:
            sy.SetLien()  


    ######################################################################################  
    def Tip_DOM(self, p = None):
#         print "Tip_DOM", self.domaine
        ref = self.GetReferentiel()
        if len(self.domaine)>1:
            t = ref._nomDom.Plur_()
        else:
            t = ref._nomDom.Sing_()
        self.tip.SetWholeText("titre", t)
        ld = [ref.domaines[d][1] for d in self.domaine]

        for d in ld:
            self.tip.AjouterElemListeUL("dom", d)
        
    
    
    ######################################################################################  
    def SetTip(self, param = None, obj = None):
        """ Mise à jour du TIP (popup)
        """
        
        if param is None:   # la Séquence elle-même
            self.tip.SetHTML(constantes.encap_HTML(constantes.BASE_FICHE_HTML_SEQ))
            self.tip.SetWholeText("int", self.intitule)
        
        else:               # Un autre élément de la Séquence
            self.tip.SetHTML(self.GetFicheHTML(param = param))
            if param == "POS":
                self.Tip_POS()
                
            elif param[:3] == "POS":
                self.Tip_POS(int(param[3])) 
                
            elif param[:3] == "EQU":
                self.Tip_EQU("la Séquence")
                
            elif param[:3] == "DOM":
                self.Tip_DOM()
                
            elif type(obj) == list:
                pass
                
            else:
                pass
                
        self.tip.SetPage()
        return self.tip

    ######################################################################################  
    def VerifPb(self):
#         print("\nVerifPb Seq")
        ref = self.GetReferentiel()
#         tps = time.clock()
        
        #
        # On récupère les objectifs abordés dans les séances
        #
        sv = [] # Ensemble des savoirs visées par les Séances
        cv = [] # Ensemble des compétences visées par les Séances
        for s in self.seances:
            cv.extend(s.compVisees)
            sv.extend(s.savVises)
            s.VerifPb()
            if hasattr(s, 'seances'):
                for ss in s.seances:
#                     print("   ", ss.compVisees)
                    cv.extend(ss.compVisees)
                    sv.extend(ss.savVises)
                    ss.VerifPb()
        cv = set(cv)
        sv = set(sv)
         
#         print("1 :", time.clock() - tps)
        tps = time.clock()
        
        
        # Tri par type
        def tri(v):
            dv = {}
            for d in v:
                dv.setdefault(d[0], []).append(d[1:])
            return dv
        
        dcv = tri(cv)
        dsv = tri(sv)
        
#         print("2 :", time.clock() - tps)
        tps = time.clock()
#         print("Séances :")
#         print("  ", dcv, dsv)
                
        #
        # On ne garde que les extréminés des branches
        #
        
        # Branche de départ (et les sous branches
        def getDicElem(code, dic_f):
            if isinstance(dic_f, dict):
                if code in dic_f.keys():
                    return dic_f[code][1]
                for sc in dic_f.keys():
                    d = getDicElem(code, dic_f[sc][1])
                    if d is not None:
                        return d
        
        # Extremités des branches
        def recup_bout(k, c, s, dic_f):
            if isinstance(dic_f, dict):
                for c, d in dic_f.items():
                    if isinstance(d[1], dict):
                        recup_bout(k, c, s, d[1])
                    else:
                        s.add(k+c)
            else:
                s.add(k+c)
                    
                
        ttcmp = ref.getToutesCompetencesDict()
        dic_f_c = {}
        setc = set()
        for k, l in dcv.items():
            # Compétences possibles comme objectif (à l'image de l'arbre)
            filtre = self.GetFiltre(ttcmp[k], "O")
            dic_f_c[k] = ttcmp[k].GetDicFiltre(filtre)
#             print("  c", dic_f)
            for c in l:
                recup_bout(k, c, setc, getDicElem(c, ttcmp[k].GetDicFiltre(filtre)))
            
        
        
        ttsav = ref.getTousSavoirsDict()
        dic_f_s = {}
        sets = set()
        for k, l in dsv.items():
            # Savoirs possibles comme objectif (à l'image de l'arbre)
            filtre = self.GetFiltre(ttsav[k], "O")
            dic_f_s[k] = ttsav[k].GetDicFiltre(filtre)
#             print("  c", dic_f)
            for c in l:
                recup_bout(k, c, sets, getDicElem(c, ttsav[k].GetDicFiltre(filtre)))
        
        
#         print("  ", setc, sets)
#         print("3 :", time.clock() - tps)
#         tps = time.clock()
        
        #
        # Objectifs de la séquence
        #
        cvseq = set()
        for c in self.obj["C"].competences:
            filtre = self.GetFiltre(ttcmp[c[0]], "O")
            recup_bout(c[0], c[1:], cvseq, getDicElem(c[1:], ttcmp[c[0]].GetDicFiltre(filtre)))
            
        
        svseq = set()
        for c in self.obj["S"].savoirs:
            filtre = self.GetFiltre(ttsav[c[0]], "O")
            
            recup_bout(c[0], c[1:], svseq, getDicElem(c[1:], ttsav[c[0]].GetDicFiltre(filtre)))
            
#         print("Séquence :")
#         print("   ", cvseq, svseq)
#         print("4 :", time.clock() - tps)
#         tps = time.clock()
        
        # On compare
        difc = set(cvseq).difference(setc)
        difs = set(svseq).difference(sets)
        
#         print("Différence :")
#         print("   ", difc, difs)
        self.SignalerPb(difc, difs)
        
#         print("5 :", time.clock() - tps)
        
        
    ######################################################################################  
    def SignalerPb(self, difc, difs):
        self.obj["C"].SignalerPb(difc)
        self.obj["S"].SignalerPb(difs)
    

    ######################################################################################  
    def MiseAJourNomsSystemes(self):
        for s in self.seances:
            s.MiseAJourNomsSystemes()
    
    ######################################################################################  
    def AjouterSystemeSeance(self, sy):
        for s in self.seances:
            s.AjouterSysteme(sy)
            
    ######################################################################################  
    def AjouterListeSystemesSeance(self, lstSys):
        for s in self.seances:
            s.AjouterListeSystemes(lstSys)
            
    ######################################################################################  
    def SupprimerSystemeSeance(self, i):
        for s in self.seances:
            s.SupprimerSysteme(i) 
            
    ######################################################################################  
    def CollerElem(self, event = None, item = None, bseance = None):
        """ Colle la séance présente dans le presse-papier (branche <bseance>)
            en première position
        """
#         print("CollerElem", item, self.brancheSce)
        if hasattr(self, "brancheSce") and item == self.brancheSce:
            sea_avant = 0
        else:
            if item != None:
                sea_avant = self.arbre.GetItemPyData(item)
                if not isinstance(sea_avant, Seance):
                    return
            else:
                return
                
        if bseance == None:
            bseance = GetObjectFromClipBoard('Seance')
            if bseance == None:
                return
        
        typeSeance = bseance.get("Type", "")
        
        seance = Seance(self, typeSeance = typeSeance,
                        branche = bseance)
        self.seances.insert(0, seance)
        
        self.OrdonnerSeances()
        #seance.ConstruireArbre(self.arbre, self.brancheSce)
        
        self.arbre.DeleteChildren(self.brancheSce)
        for sce in self.seances:
            sce.ConstruireArbre(self.arbre, self.brancheSce) 
        self.arbre.Expand(self.brancheSce)
        for b in self.brancheSce.GetChildren():
            self.arbre.Expand(b)
            
#        seance.panelPropriete.MiseAJour()
#        seance.panelPropriete.MiseAJourListeSystemes()
        
        self.GetApp().sendEvent(modif = "Collé d'un élément")
        
        self.arbre.SelectItem(seance.branche)    


    ######################################################################################  
    def AjouterSeance(self, event = None):
        ref = self.GetReferentiel()
        seance = Seance(self)
        self.seances.append(seance)
        self.OrdonnerSeances()
        
        seance.ConstruireArbre(self.arbre, self.brancheSce)
        self.VerifPb()
        self.GetApp().sendEvent(modif = "Ajout d'%s" %ref._nomActivites.un_())
        
        self.arbre.SelectItem(seance.branche)
        
        return seance
    
    
    
    ######################################################################################  
    def SupprimerSeance(self, event = None, item = None):
#         print("SupprimerSeance depuis :", self)
#         print("   ", [id(s) for s in self.seances])
#         print("   ", item, id(self.arbre.GetItemPyData(item)))
        if len(self.seances) > 1: # On en laisse toujours une !!
            ref = self.GetReferentiel()
            seance = self.arbre.GetItemPyData(item)
#             print(" ---",  seance)
#             print("iiii",self.seances[1])
            self.seances.remove(seance)
#             print("  >", [id(s) for s in self.seances])
            self.arbre.Delete(item)
            self.OrdonnerSeances()
            self.VerifPb()
            self.GetApp().sendEvent(modif = "Suppression d'%s" %ref._nomActivites.un_())
            return True
        return False
    
    
    ######################################################################################  
    def OrdonnerSeances(self):
        """ Redefinir completement les codes des séances et sous séances
            de manière à avoir des codes ordonnés (chronologiquement)
            et uniques.
        """
#         print "OrdonnerSeances"
#         print "   ", self.seances
        listeTypeSeance = self.GetReferentiel().listeTypeSeance
        dicType = {k:0 for k in listeTypeSeance}
        dicType[''] = 0
        RS = 0
        if hasattr(self, 'seances'): # c'est une sous séance
            for i, sce in enumerate(self.seances):
                sce.ordre = i
                if sce.typeSeance in ['R', 'S']:
    #                print sce
                    sce.ordreType = RS
                    RS += 1
                else:
                    sce.ordreType = dicType[sce.typeSeance]
                    dicType[sce.typeSeance] += 1
                sce.OrdonnerSeances()
        
        self.SetCodes()
#         print "   ", self.seances
    
#    ######################################################################################  
#    def AjouterObjectif(self, event = None):
#        obj = Competence(self, self.panelParent)
#        self.obj.append(obj)
#        obj.ConstruireArbre(self.arbre, self.brancheObj)
#        self.panelPropriete.sendEvent()
#        return
    
    ######################################################################################  
    def SupprimerItem(self, item):
        data = self.arbre.GetItemPyData(item)
        if isinstance(data, Seance):
            if data.EstSousSeance():
                data.parent.SupprimerSeance(item = item)
            else:
                self.SupprimerSeance(item = item)
            
        elif isinstance(data, Systeme):
            self.SupprimerSysteme(item = item)
            
        elif isinstance(data, LienSequence):
            self.SupprimerLienSequence(item = item)           
        
    
    ###################################################################################### 
    def SupprimerLienSequence(self, event = None, item = None):
        ps = self.arbre.GetItemPyData(item)
        self.prerequisSeance.remove(ps)
        self.arbre.Delete(item)
        self.GetApp().sendEvent(modif = "Suppression d'une Séquence prérequise")
    
    
    ########################################################################################################
    def OuvrirFichierSeq(self, nomFichier, reparer = False):

        root = safeParse(nomFichier, None)
        if root is None:
            return None, None
        
        classe = Classe(self.GetApp())
        sequence = Sequence(self.GetApp(), classe, ouverture = True)
        classe.SetDocument(sequence)

        rsequence = root.find("Sequence")
        rclasse = root.find("Classe")
        if rclasse is not None:
            classe.setBranche(rclasse, reparer = reparer)
        if rsequence is not None:
            sequence.setBranche(rsequence, reparer = reparer)
        else:   # Ancienne version , forcément STI2D-ETT !!
            classe.typeEnseignement, self.classe.familleEnseignement = ('ET', 'STI')
            classe.referentiel = REFERENTIELS[classe.typeEnseignement]
            sequence.setBranche(root)
        return classe, sequence
    
    ######################################################################################  
    def AjouterSequencePre(self, event = None):
        """ Ajoute une Séquence prérequise
            parmi une liste de Séquences compatibles recherchées dans le dossier de la progression
        """
        mesFormats = constantes.FORMAT_FICHIER['seq'][:-1]
        dlg = wx.FileDialog(self.GetApp(), message="Ouvrir un fichier Séquence",
#                             defaultDir = self.DossierSauvegarde, 
                            defaultFile = "",
                            wildcard = mesFormats,
                            style=wx.FD_OPEN | wx.FD_CHANGE_DIR
                            )

        if dlg.ShowModal() == wx.ID_OK:
            nomFichier = dlg.GetPath()#.decode(FILE_ENCODING)

            dlg.Destroy()
            classe, sequence = self.OuvrirFichierSeq(nomFichier)
            if classe is None:
                messageErreur(self.GetApp(), "Erreur d'ouverture de Séquence", 
                              "La séquence \n\n   %s\n\nn'a pas pu être ouverte !\n" %nomFichier)
            else:
                if classe.typeEnseignement == self.GetReferentiel().Code:
                    ps = LienSequence(self)
                    self.prerequisSeance.append(ps)
                    ps.path = nomFichier    
                    ps.sequence = sequence
                    ps.ConstruireArbre(self.arbre, self.brancheSeq)
                    self.GetApp().sendEvent(modif = "Ajout d'une Séquence prérequise")
                    self.arbre.SelectItem(ps.branche)
                else:
                    messageErreur(self.GetApp(), "Séquence incompatible", 
                                  "La séquence choisie n'est pas compatible\n" \
                                  "avec la séquence en cours d'édition.\n" \
                                  " - Classe différente : %s ≠ %s" %(classe.typeEnseignement,self.GetReferentiel().Code))

        
        
        
    ######################################################################################  
    def RemplacerSysteme(self, sy1, sy2):
        for i, s in enumerate(self.systemes):
            if s == sy1:
                self.systemes[i] = sy2
                sy1.branche.SetData(sy2)
                sy2.branche = sy1.branche
                sy2.arbre = sy1.arbre
                if not isinstance(sy1.parent, Classe):
                    del sy1
                return
        
        
    ######################################################################################  
    def AjouterSysteme(self, event = None):
        ref = self.GetReferentiel()
        sy = Systeme(self)
#         print("AjouterSysteme", sy)
        self.systemes.append(sy)
        sy.ConstruireArbre(self.arbre, self.brancheSys)
        self.arbre.Expand(self.brancheSys)
        self.GetApp().sendEvent(modif = "Ajout d'%s" %ref._nomSystemes.un_())
        self.arbre.SelectItem(sy.branche)
        self.AjouterSystemeSeance(sy)
        return
    
    ######################################################################################  
    def AjouterListeSystemes(self, syst = []):
#         print("AjouterListeSystemes séquence", syst)
        nouvListe = []
        for s in syst:
#             print("   ",s)
            
            if isinstance(s, Systeme):
                sy = s.Copie(self)
                sy.lienClasse = s
            elif isinstance(s, str):
                sy = Systeme(self)
                sy.setBranche(ET.fromstring(s))
            elif isinstance(s, (list, tuple)) and len(s) > 0:
                sy = Systeme(self, s[0])
                if len(s) > 1:
                    try:
                        sy.nbrDispo.v[0] = int(s[1])
                    except:
                        pass
#                 print 2
                
#                sy.GetPanelPropriete().Verrouiller(False)
#                sy.GetPanelPropriete().cbListSys.SetSelection(sy.GetPanelPropriete().cbListSys.FindString(s.nom))
#            try:
#                sy.setBranche(ET.fromstring(s))
#            except:
#                print "Erreur parsing :", s
#                continue
            
#            nom = unicode(s)
#            sy = Systeme(self, self.panelParent, nom = nom)
            # On évite les systèmes redondants (correction d'un bug)
            if sy.lienClasse == None or  not sy.lienClasse in [s.lienClasse for s in self.systemes]:  
#                 print "   ", sy
                self.systemes.append(sy)
                nouvListe.append(sy.nom)
                sy.ConstruireArbre(self.arbre, self.brancheSys)
                sy.SetCode()
#            sy.nbrDispo.v[0] = eval(n)
#            sy.panelPropriete.MiseAJour()
#         print("  nouvListe :", nouvListe)
        self.arbre.Expand(self.brancheSys)
        self.AjouterListeSystemesSeance(nouvListe)
        self.GetApp().sendEvent(modif = "Ajout d'une liste de Systèmes")
        return


    ######################################################################################  
    def SupprimerSysteme(self, event = None, item = None):
        sy = self.arbre.GetItemPyData(item)
        i = self.systemes.index(sy)
        self.systemes.remove(sy)
        self.arbre.Delete(item)
        self.SupprimerSystemeSeance(i)
        self.GetApp().sendEvent(modif = "Suppression d'un Système")


    ######################################################################################  
    def SelectSystemes(self, event = None):
        if recup_excel.ouvrirFichierExcel():
            res = messageYesNo(self.app, 'Sélection de systèmes',
                                 "Sélection de systèmes depuis Excel\n\n" \
                                 "Excel doit à présent être lancé.\n" \
                                 "\t- selectionner les cellules contenant les informations,\n" \
                                 "\t- puis appuyer sur Ok.\n\n" \
                                 "Format attendu de la selection :\n" \
                                 "|    colonne 1    |    colonne 2      |    colonne 3    |\n" \
                                 "|                         | (optionnelle)    | (optionnelle) |\n" \
                                 "|    systèmes     |   nombre dispo | fichiers image|\n" \
                                 "|   ...                   |   ...                      |   ...                    |\n",
                                 
                                 wx.ICON_INFORMATION | wx.CANCEL
                                 )
            
            if res:
                ls = recup_excel.getSelectionExcel()
                if ls != None:
                    self.AjouterListeSystemes(ls)

        
    ######################################################################################  
    def SauvSystemes(self, event = None):
        self.classe.options.validerSystemes(self)
        self.classe.options.enregistrer()
        try:
            pass
            
        except IOError:
            messageErreur(self.GetApp(), "Permission refusée",
                          "Permission d'enregistrer les préférences refusée.\n\n" \
                          "Le dossier est protégé en écriture")
        except:
            messageErreur(self.GetApp(), "Enregistrement impossible",
                          "Imposible d'enregistrer les préférences\n\n")
        return
    
    ######################################################################################  
    def MiseAJourListeSystemesClasse(self):
        for s in self.systemes:
            s.MiseAJourListeSystemesClasse()
        
    ######################################################################################  
    def AjouterRotation(self, seance):
        seanceR1 = Seance(self.panelParent)
        seance.seances.append(seanceR1)
        return seanceR1
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche, simple = False):
#         print("ConstruireArbre Seq")
#         print err
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, self.Sing_(),#Titres[0] 
                                        image = self.arbre.images["Seq"],
                                        data = self,)
        self.arbre.SetItemBold(self.branche)
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)
        ref = self.GetReferentiel()
        
        #
        # Les centres d'intérêt
        #
        self.CI.ConstruireArbre(arbre, self.branche)
        
        
        #
        # Les objectifs
        #
        self.brancheObj = arbre.AppendItem(self.branche, ref.labels["OBJEC"][2].Plur_(), #Titres[2], 
                                           image = self.arbre.images["Obj"], 
                                           data = "Obj")
        for obj in self.obj.values():
            obj.ConstruireArbre(arbre, self.brancheObj)
            
        
        #
        # Les prérequis
        #
        self.branchePre = arbre.AppendItem(self.branche, Titres[1], 
                                           image = self.arbre.images["Sav"], 
                                           data = "Pre")
        for pre in self.prerequis.values():
            pre.ConstruireArbre(arbre, self.branchePre, prerequis = True)


        self.brancheSeq = arbre.AppendItem(self.branchePre, "Séquences", 
                                           image = self.arbre.images["Seq"], 
                                           data = "Seq")
        for ps in self.prerequisSeance:
            ps.ConstruireArbre(arbre, self.brancheSeq)
    
        
    
    
        #
        # L'équipe pédagogique
        #
        if len(self.equipe) > 0:
            self.branchePrf = arbre.AppendItem(self.branche, Titres[10], 
                                               data = "Equ")
            for e in self.equipe:
                e.ConstruireArbre(arbre, self.branchePrf) 
        


        if not simple: ## !!!
            #
            # Les Séances
            #
            self.brancheSce = arbre.AppendItem(self.branche, ref._nomSeances.Plur_(), 
                                               image = self.arbre.images["Sea"], 
                                               data = "Sea")
            self.arbre.SetItemBold(self.brancheSce)
            for sce in self.seances:
                sce.ConstruireArbre(arbre, self.brancheSce) 
            
            #
            # Les systèmes
            #
            self.brancheSys = arbre.AppendItem(self.branche, ref._nomSystemes.Plur_(), 
                                               image = self.arbre.images["Sys"], 
                                               data = "Sys")
            
            for sy in self.systemes:
                sy.ConstruireArbre(arbre, self.brancheSys)    
        
#         self.VerifPb()
        

    ####################################################################################
    def SetDefautExpansion(self):
        self.arbre.ExpandAll()
        self.arbre.Collapse(self.branchePre)
    
    
    ######################################################################################  
    def DefinirCouleurs(self):
        draw_cairo.DefinirCouleurs(self.GetNbrPeriodes(),
                                   len(self.GetReferentiel()._listesCompetences_simple["S"]),
                                   len(self.GetReferentiel().CentresInterets))


    #########################################################################
    def GetObjAffiches(self):
        """ Renvoie la liste de codes d'objectifs à afficher sur la fiche
            Sélection parmi les objectifs visés selon un critère de quantité
            d'information affichée :
            Trop d'objectifs >> on affiche les parents/grand parents ...
            
            En tenant compte du niveau maximum imposé par le Référentiel.
        """
        lst = []
        ref = self.GetReferentiel()
        
#         if ref.tr_com != []:  # Tronc commun
#             ref_tc = REFERENTIELS[ref.tr_com[0]]
#         
#         print("GetObjAffiches", self.obj["C"].competences)
        for cmp in self.obj["C"].competences: # liste de codes depuis pysequence.Competences
            typ, cod = cmp[0], cmp[1:]
            comp = ref.getToutesCompetencesDict()[typ]
            # Chemin de la compétence, jusqu'à la racine.
            path = ref.getPathCompetence(cmp)

            
#             if typ == "B" and ref.tr_com != []: # B = tronc commun --> référentiel
#                 # Chemin de la compétence, jusqu'à la racine.
#                 path = ref_tc.getPathCompetence("S"+cod)
#             else:
#                 if typ in list(ref.dicoCompetences.keys()):
#                     # Chemin de la compétence, jusqu'à la racine.
#                     path = ref.getPathCompetence(cmp)
#                 elif ref_tc and typ in list(ref_tc.dicoCompetences.keys()):
#                     # Chemin de la compétence, jusqu'à la racine.
#                     path = ref_tc.getPathCompetence(cmp)
                
            i = -comp.nivObj
            
#             print(cmp, i, path)
            lst.append(cmp[0]+path[i])
#         print("GetObjAffiches", list(set(lst)))
        return constantes.trier(list(set(lst)))
    
    
    #########################################################################
    def GetFiltre(self, elem, contexte, seance = None, niveau = 2):
        """ Renvoi le "filtre" = liste de codes "valides"
            pour l'élément <elem> (Reférentiel.Competences ou Savoirs)
            dans le contexte "O" ou "P"
            
            :elem: Referentiel.Competences ou Referentiel.Savoirs
            :preresuis: contexte
        """
#         print("GetFiltre", elem, contexte)
        ref = self.GetReferentiel()
        
        if contexte == "P":
            d = self.prerequis
        else:
            d = self.obj
            
        
        # 1er niveau : Spe, Th et Dom
        
        elem_asso = ref.getElemAsso(elem, contexte)
        if len(elem_asso) == 0: # Pas de filtrage
            return
        
#         print("  ", elem_asso[:niveau])
        filtres = []

        for code in elem_asso[:niveau]:
            filtre = []
            
            # Détermination de la liste de codes constituant le masque du filtre
            if code == "Spe":
                ce = self.classe.specialite
                ef = None
            elif code == "EnsSpe":
                if seance is not None:
                    ce = seance.ensSpecif
                else:
                    continue
                ef = None
            elif code[:4] == "Comp":
                ce = [e[1:] for e in d["C"].competences]
                ef = d["C"]
                ef.filtre = self.GetFiltre(ref.getToutesCompetencesDict()[code[-1]], contexte)
            elif code[:3] == "Sav":
                ce = d["S"].savoirs
                ef = d["S"]
                ef.filtre = self.GetFiltre(ref.getTousSavoirsDict()[code[-1]], contexte)
                
#             print("   :", code, ef.filtre)
            
            filtres.append(filtre)

            # On ajoute les sous éléments ...
            ce2 = ce[:]
#             if ef is not None and hasattr(ef, 'filtre') and ef.filtre is not None:
#                 for e in ce:
# #                     print("   ..", e)
#                     ce2.extend([c for c in ref.getSousElem(e, code) if c in ef.filtre])
                    
            if ef is not None and hasattr(ef, 'filtre'):
                for e in ce:
#                     print("   ..", e)
                    ce2.extend([c for c in ref.getSousElem(e, code) if (ef.filtre is None or c in ef.filtre)])
                    
                    
#             print("   ce =", ce, "-->", ce2)
            
#             if isinstance(elem, Referentiel.Competences):
#                 dic = ref.getDicToutesCompetences()
#             elif isinstance(elem, Referentiel.Savoirs):
#                 dic = ref.getDicTousSavoirs()
            
#             print("   :", elem.getElemAssocies(code, contexte))
            #
            # Filtrage
            #
            for cd, val in elem.getElemAssocies(code, contexte).items():
                v = []
                for c in val:
                    v.extend(ref.getSousElem(c, code))
#                 print("   v =", v)
                if val == []:  # Liste vide = pas de filtrage
                    filtre.append(cd)
                else:
                    for e in ce2:
                        if e in v: 
                            filtre.append(cd)
#                     else:
#                         ssval = 
        
#         print("   filtres :", filtres)
        
        #
        # Intersection des différens filtres
        #
        if len(filtres) > 1:
            filtre = set(filtres[0])
            for l in filtres[1:]:
                filtre.intersection_update(l)
            filtre = list(filtre)
        elif len(filtres) > 0:
            filtre = filtres[0]
        else:
            filtre = []
#         print(">>>", filtre)

        return filtre # Une seule liste de codes
        
#         if code[:4] == "Comp":
#                 e = ref.dicoCompetences[code[5:]]
#             elif code[:3] == "Sav":
#                 e = ref.dicoSavoirs[code[4:]]
#             
#         
#         

    

        
    ########################################################################
    def GererElementsDependants(self, contexte):
        """ Gestion (filtrage) des items des Competences et des Savoirs de la séquence
            en fonction des items "cochés" de <elem> (type pysequence.Competence ou Savoir)
        """
#         print("SEQ: GererElementsDependants de contexte :", contexte)
        
        ref = self.GetReferentiel()
        
        if contexte == "P":
            d = self.prerequis
        else:
            d = self.obj
            
#         print(" ", d["C"].competences, ref.getToutesCompetencesDict())
        maj = False
        toremove=[]
        for cc in d["C"].competences:
#             print("  ", cc)
            filtre = self.GetFiltre(ref.getToutesCompetencesDict()[cc[0]], contexte)
            if filtre is not None and not (cc[1:] in filtre):
                toremove.append(cc)
                maj = True
        for s in toremove:
            d["C"].competences.remove(s)
        if maj:
            d["C"].SetCodeBranche()
        
        
#         print("  sav : ", d["S"].savoirs)
        maj = False
        toremove=[]
        for cs in d["S"].savoirs:
#             print("   ", cs)
            filtre = self.GetFiltre(ref.getTousSavoirsDict()[cs[0]], contexte)
            if filtre is not None and not (cs[1:] in filtre):
                toremove.append(cs)
                maj = True
        
        for s in toremove:
            d["S"].savoirs.remove(s)
        if maj:
            d["S"].SetCodeBranche()
    
    
    ######################################################################################  
    def Rafraichir(self):
        self.arbre.Delete(self.branche)
        self.ConstruireArbre(self.arbre, self.arbre.GetRootItem())
        self.SetDefautExpansion()
#         self.arbre.ExpandAll()
        
        self.DefinirCouleurs()
        
        if self.arbre.GetSelection() is None:
            self.arbre.SelectItem(self.branche)
        
        
    ######################################################################################  
    def reconstruireBrancheSeances(self, b1, b2):
        self.arbre.DeleteChildren(self.brancheSce)
        for sce in self.seances:
            sce.ConstruireArbre(self.arbre, self.brancheSce) 
        self.arbre.Expand(b1.branche)
        self.arbre.Expand(b2.branche)

        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):    
        """ Affiche le menu contextuel associé à la séquence
            ... ou bien celui de itemArbre concerné ...
        """
#         print("AfficherMenuContextuel", itemArbre)
        ref = self.GetReferentiel()
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([["Enregistrer", self.app.commandeEnregistrer, 
                                              getIconeFileSave()],
#                                             [u"Ouvrir", self.app.commandeOuvrir],
                                             ["Exporter la fiche (PDF ou SVG)", self.app.exporterFiche,
                                              None],
                                            ])
                
                
#        [u"Séquence pédagogique",
#          u"Prérequis",
#          u"Objectifs pédagogiques",
#          u"Séances",
#          u"Systèmes"]
        
#        elif isinstance(self.arbre.GetItemPyData(itemArbre), Competences):
#            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)

        elif isinstance(self.arbre.GetItemPyData(itemArbre), Prof):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Seance):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Systeme):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), LienSequence):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
#        elif self.arbre.GetItemText(itemArbre) == Titres[1]: # Objectifs pédagogiques
#            self.app.AfficherMenuContextuel([[u"Ajouter une compétence", self.AjouterObjectif]])
            
            
        elif self.arbre.GetItemData(itemArbre) == "Sea": # Séances
            listItems = [["Ajouter %s" %ref._nomActivites.un_(), 
                          self.AjouterSeance,
                          scaleImage(images.Icone_ajout_seance.GetBitmap())]]
            
            ################
            elementCopie = GetObjectFromClipBoard('Seance')
            if elementCopie is not None:
                listItems.append(["Coller", functools.partial(self.CollerElem, 
                                                              item = itemArbre,
                                                              bseance = elementCopie),
                                                              getIconePaste()])
            
            self.app.AfficherMenuContextuel(listItems)
                
                
        elif self.arbre.GetItemData(itemArbre) == "Sys": # Système
            self.app.AfficherMenuContextuel([["Ajouter %s" %et2ou(ref._nomSystemes.un_()), 
                                              self.AjouterSysteme,
                                              scaleImage(images.Icone_ajout_systeme.GetBitmap())], 
                                             ["Sélectionner depuis un fichier", 
                                              self.SelectSystemes, 
                                              scaleImage(images.Icone_import_systeme.GetBitmap())],
#                                             [u"Sauvegarder la liste dans les préférences", self.SauvSystemes]
                                             ])
         
        elif self.arbre.GetItemData(itemArbre) == "Pre" or self.arbre.GetItemText(itemArbre) == "Séquences": # Prérequis
            self.app.AfficherMenuContextuel([["Ajouter %s" %self.un_(), self.AjouterSequencePre, 
                                              scaleImage(images.Icone_ajout_seq.GetBitmap())], 
                                             ])
        
        elif self.arbre.GetItemText(itemArbre) == Titres[10]: # Eleve
            self.app.AfficherMenuContextuel([["Ajouter un professeur", self.AjouterProf, 
                                              scaleImage(images.Icone_ajout_prof.GetBitmap())]])



    ######################################################################################       
    def GetCompetencesVisees(self):
        """ Renvoie la liste des compétences visées (objectifs) 
        """
        ref = self.GetReferentiel()
        
        def ajouter(k, l, comp):
            if len(comp.sousComp) > 0:
                for k2, c2 in comp.sousComp.items():
                    ajouter("S"+k2, l, c2)
            else:
                l.append(k)
            
        lstCompS = [c for c in self.obj["C"].competences if c[0] == "S"]
        l = []
        for k in lstCompS:
            ajouter(k, l, ref.getCompetence(k))
            
        return l

    
    ######################################################################################       
    def GetTypesCompetencesVisees(self):
        """ Renvoie la liste des types de compétences visées (objectifs)
            "S", ...
        """
        lstTypComp = [c[0] for c in self.obj["C"].competences]
        return list(set(lstTypComp))
    
    
    ######################################################################################       
    def GetSavoirsVises(self):
        """ Renvoie la liste des Savoirs visés (objectifs) 
        """
#         print "GetSavoirsVises", self
        ref = self.GetReferentiel()
        
        def ajouter(k, l):
            ss = ref.getSousSavoirs(k)
            if len(ss) > 0:
                for k2 in ss:
                    ajouter("S"+k2, l)
            else:
                l.append(k)
            
        lstCompS = [c for c in self.obj["S"].savoirs if c[0] == "S"]
#         print "   ", lstCompS
        
        l = []
        for k in lstCompS:
            ajouter(k, l)
            
#         print "   ", l
        return l+lstCompS


    ######################################################################################       
    def GetSystemesUtilises(self, niveau = None):
        """ Renvoie la liste des systèmes utilisés pendant la séquence
        """
#         print("GetSystemesUtilises", self, niveau)
        lst = []
        for s in self.systemes:
#             print "   ", s
            n = 0
            for se in self.seances:
                ns = se.GetNbrSystemes(complet = True, niveau = niveau)
#                 print("   ", se, ns)
                if s.nom in ns.keys():
                    n += ns[s.nom]
            if n > 0:
                lst.append(s)
#         print(">>>", lst)
        return lst



    ######################################################################################  
    def GetNbreSeances(self):
        n = 0
        for s in self.seances:
            if s.EstSeance_RS():
                n += len(s.seances)
            n += 1
        return n



    ######################################################################################  
    def GetToutesSeances(self):
        l = []
        for s in self.seances:
            l.append(s)
            if s.EstSeance_RS():
                l.extend(s.GetToutesSeances())
            
        return l 



    ######################################################################################  
    def GetNbrSystemes(self, niveau = None):
        """
        """
        dic = {}
        for s in self.GetToutesSeances():
            d = s.GetNbrSystemes(niveau = niveau)
            for k, v in d.items():
                if k in dic.keys():
                    dic[k] += v
                else:
                    dic[k] = v
        return dic



    ######################################################################################  
    def GetIntituleSeances(self):
        nomsSeances = []
        intSeances = []
        for s in self.GetToutesSeances():
            if hasattr(s, 'code') and s.intitule != "" and not s.intituleDansDeroul:
                nomsSeances.append(s.code)
                intSeances.append(s.intitule)
        return nomsSeances, intSeances


    ######################################################################################  
    def HitTestPosition(self, x, y):
        if hasattr(self, 'rectPos'):
            for i, rectPos in enumerate(self.rectPos):
                if dansRectangle(x, y, (rectPos,))[0]:
                    return i


    #############################################################################            
    def drawPeriode(self, ctx, larg):
        prop = 7
        w, h = 0.04*prop * draw_cairo.COEF, 0.04 * draw_cairo.COEF
        ctx.scale(larg/w, larg/w) 
    #     ctx.set_source_rgba(1,1,1,1)
    #     ctx.paint()
        draw_cairo.DrawPeriodes(ctx, (0,0,w,h), 
                                    self.getRangePeriode(), 
                                    self.GetReferentiel().periodes)
    
    
    #############################################################################            
    def getBitmapPeriode(self, larg):
        imagesurface = draw_cairo.getBitmapPeriode(larg, self.getRangePeriode(),
                                                       self.GetReferentiel().periodes, 
                                                       prop = 7)
        return getBitmapFromImageSurface(imagesurface)


    #############################################################################
    def MiseAJourTypeEnseignement(self):
#         print("MiseAJourTypeEnseignement Sequence", self.GetPositions(), self.classe.GetPeriodes())
        self.app.SetTitre()
        
        self.classe.MiseAJourTypeEnseignement()
        
#         print(self.position) 
        p = self.classe.GetPeriodes()
        if not sublist(self.GetPositions(), p):
            self.position = [p[0], p[0]]
#         print(">>>", self.position) 
        
        self.CI.MiseAJourTypeEnseignement()
#         self.obj['C'].MiseAJourTypeEnseignement()
        for o in self.obj.values():
            o.MiseAJourTypeEnseignement()
            
        for p in self.prerequis.values():
            p.MiseAJourTypeEnseignement()
            
        for s in self.seances:
            s.MiseAJourTypeEnseignement()
        
        for s in self.systemes:
            s.MiseAJourTypeEnseignement()
        
        if hasattr(self, 'arbre'):
            self.Rafraichir()
        
        draw_cairo.DefinirCouleurs(self.GetNbrPeriodes(),
                                   len(self.GetReferentiel()._listesCompetences_simple["S"]),
                                   len(self.GetReferentiel().CentresInterets))

        

    #############################################################################
    def Verrouiller(self):
        if hasattr(self, 'CI') \
            and (self.CI.numCI != [] or self.prerequis["S"].savoirs != [] \
                 or self.obj['C'].competences != [] or self.obj['S'].savoirs != []):
            self.classe.Verrouiller(True)
        else:
            if self.classe != None:
                self.classe.Verrouiller(False)


    #############################################################################
    def enregistrer(self, nomFichier, dialog = True):
#         print "enregistrer", nomFichier, self.GetPath()
                # La séquence
        sequence = self.getBranche()
        classe = self.classe.getBranche()
        proprietes = self.proprietes.getBranche()
        
        # La racine
        root = ET.Element('Sequence_Classe')
        root.append(sequence)
        root.append(classe)
        root.append(proprietes)
        constantes.indent(root)
        
        return enregistrer_root(root, nomFichier, dialog = dialog)



    ######################################################################################  
    def GetBulleHTML(self, i = None, css = False):
        """ Renvoie le tootTip sous la forme HTML
            pour affichage sur la fiche HTML (template "_CSS")
            ou sur la fiche pySéquence (template par défaut)
            
            :i:  code pour différentier ...
        """
#         print("GetBulleHTML Seq", self, i)
#         ref = self.GetReferentiel()
        
        
        if i == "Eff":
            if css:
                t = Template(constantes.TEMPLATE_EFF_CSS)
            else:
                t = Template(constantes.TEMPLATE_EFF)
            
            
            image = draw_cairo.getBase64PNG(draw_cairo.getBitmapClasse(400, 200, self.GetClasse()))
#             self.image = self.getBitmapPeriode(400).ConvertToImage().GetData()
            if css:
                if image is not None:
                    image = b64(image)
                else:
                    image = None
                
            else:
                image = self.tip.GetImgURL(image, width = 200)
            

            html = t.render(titre = "Découpage de la classe",
                            image = image,
                            )
    
            return html
        return  ""
    
    
####################################################################################################
#
#        Projet
#
####################################################################################################
class Projet(BaseDoc, Grammaire):
    """Document de type Projet
        :param classe: Classe associée au document
        :type classe: pysequence.Classe
        :param intitule: Intitulé du document
        :type intitule: str
    """
    def __init__(self, app, classe = None, intitule = "", ouverture = False):
        
        Grammaire.__init__(self, "Projet(s)$m")
        
#         self.nom_obj = "Projet"
#         self.article_c_obj = "du"   # article partitif
#         self.article_obj = "le"     # article défini
#         self.article_i_obj = "un"   # article indéfini
#         
        BaseDoc.__init__(self, app, classe, intitule)
        
        
        # code désignant le type de projet
#        print "init Projet"
#        print "   ", self.GetReferentiel()
        self.code = self.GetReferentiel().getCodeProjetDefaut()
  
        self.position = self.GetPeriodeDefaut()
#        print "position0", self.position
        self.nbrParties = 1
        
        # Organisation des revues du projet
        self.initRevues()
                
        self.eleves = []
        self.groupes = []
        
        self.fct_serv = []   # Fonctions de service (développement en cours ...)
        
        self.problematique = ""
        
        self.equipe = []
        
        self.support = Support(self)
        
        
        self.taches = self.creerTachesRevue()

        
        
        #
        # Spécifiquement pour la fiche de validation
        #
        self.origine = ""
        self.contraintes = ""
        self.besoinParties = ""
        self.intituleParties = ""

        self.production = ""
        
        self.synoptique = ""
        self.typologie = []
        
        # Prtie "Partenariat ('PAR')
        self.partenariat = ""
        self.montant = ""
        self.src_finance = ""
        
        if not ouverture:
            self.MiseAJourTypeEnseignement()
#        self.SetPosition(self.position, first = True)
        
        # Le module de dessin
        self.draw = draw_cairo_prj
        
        
        
        
    ######################################################################################  
    def __repr__(self):
        return "Projet "+ self.intitule

    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Projet(parent, self)
    
    ######################################################################################  
    def GetType(self):
        return 'prj'


    ######################################################################################  
    def GetProjetRef(self):
        """ Renvoie le projet (Referentiel.Projet) de référence
        """
#         print("GetProjetRef", self.code, list(self.GetReferentiel().projets.keys()))
        if self.code == None:
            return self.GetReferentiel().getProjetDefaut()
        else:
            if self.code in self.GetReferentiel().projets.keys():
                return self.GetReferentiel().projets[self.code]
            else:
                return None #Referentiel.Projet(self.GetReferentiel()) # None : pose des pb

    ######################################################################################  
    def GetPeriodeDefaut(self):
        projet = self.GetProjetRef()
#         return projet.getPeriodeDefaut()
    
    
        if projet is not None:
            return projet.getPeriodeDefaut()
        else:
            return [0,0]
        
    ######################################################################################  
    def GetDuree(self):
        ld = [e.GetDuree() for e in self.eleves + self.groupes]
        if len(ld) > 0:
            duree = max(ld)
            return duree   
        duree = 0
        for t in self.taches:
            duree += t.GetDuree()
        if duree == 0:
            return 1
        return duree
                  
    ######################################################################################  
    def GetDureeGraph(self):
        duree = 0
        for t in self.taches:
            duree += t.GetDureeGraph()
        return duree
    
    
    ######################################################################################  
    def getIcone(self):
        return scaleImage(images.Icone_projet.GetBitmap())
    
    ######################################################################################  
    def getIconeDraw(self):
        return scaleImage(images.Icone_projet.GetBitmap(), 100, 100)
    
    
    ######################################################################################  
    def creerTachesRevue(self):
        projet = self.GetProjetRef()
        if projet is None:
            return []
        
        lst = []
        if self.nbrRevues == 2:
            lr = [_R1, _R2, "S"]
        else:
            lr = TOUTES_REVUES_EVAL_SOUT
            
        for p in lr:
            lst.append(Tache(self, intitule = projet.phases[p][1], 
                             phaseTache = p, duree = 0))
        return lst
    
    
    
    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG et HTML)
        """
#         print("GetPtCaract prj")
        lst = BaseDoc.GetPtCaract(self)  
            
        lst.extend(self.support.GetPtCaract())
        
        for s in self.taches + self.eleves:
            lst.extend(s.GetPtCaract())
            
        self.cadre = []
        return lst    
    
    
    ######################################################################################  
    def EnrichiHTMLdoc(self, doc):
        """ Enrichissement de l'image HTML <doc> (format XML) avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens 
             - ...
        """
        for s in self.taches:
            s.EnrichiHTML(doc)
        self.support.EnrichiHTML(doc)
        self.EnrichiHTML(doc)
        return
    
    
    ######################################################################################  
    def EnrichiSVGdoc(self, doc):
        """ Enrichissement de l'image SVG <doc> (format XML) avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens 
             - ...
        """
        
        if hasattr(self, 'app'):
            t = doc.createElement("title")
            path = os.path.split(self.app.fichierCourant)[1]
            path = str(path) # Conversion en unicode !!!
            txt = doc.createTextNode(path)
            
            t.appendChild(txt)
            svg = doc.getElementsByTagName("svg")[0]
            svg.insertBefore(t, svg.childNodes[0])
        
        
        ElementBase.EnrichiSVG(self, doc)
        
        for s in self.taches:
            s.EnrichiSVG(doc)
        self.support.EnrichiSVG(doc)

        return
    
    ######################################################################################  
    def areTachesPredeterminees(self):
        return len(self.GetProjetRef().taches) > 0
    
    
    ######################################################################################  
    def getTachesRevue(self):
        return [t for t in self.taches if t.phase in TOUTES_REVUES_EVAL_SOUT]
#        lst = []
#        for t in self.taches:
#            if t.phase in TOUTES_REVUES_EVAL_SOUT:
#                lst.append(t)
#        return lst
        
        
#    ######################################################################################  
#    def getTachesRevue(self):    
    
    ######################################################################################  
    def getCodeLastRevue(self):
        return "R"+str(int(self.nbrRevues))
#        if self.nbrRevues == 2:
#            return _R2
#        else:
#            return _R3
        
    ######################################################################################  
    def getLastRevue(self):
        lr = self.getCodeLastRevue()
        for t in self.taches:
            if t.phase == lr:
                return t
        return None
        
    
            
    
    ######################################################################################  
    def GetBulleSVG(self, i):
        prj = self.GetProjetRef()
        if i >= 0:
            c = self.GetCompetencesUtil()
#             print(c)
#             print(prj._dicoIndicateurs_simple)
            lstIndic = prj._dicoIndicateurs_simple[c[i][0]][c[i][1:]]
#             lstIndic = prj.getListeIndic(c[i])
#            lstIndic = REFERENTIELS[self.classe.typeEnseignement]._dicIndicateurs_prj_simple[c[i]]
            t = c[i][1:] + " :\n" + "\n".join([indic.intitule for indic in lstIndic])
            return t#.encode(SYSTEM_ENCODING)
        
        else:
            e = self.eleves[-1-i]
            t = e.GetNomPrenom()+"\n"
            t += "Durée d'activité : "+draw_cairo.getHoraireTxt(e.GetDuree())+"\n"
            t += "Évaluabilité :\n"
            ev_tot = e.GetEvaluabilite()[1]
#             print ev_tot
            for disc, dic in prj._dicoGrpIndicateur.items():
                for ph, nomph in prj.parties.items():
#                     print "  ", ph
                    t += nomph + pourCent2(ev_tot[disc][ph][0], True)+"\n"
            
#            t += u"\tconduite : "+pourCent2(ev_tot['R'][0], True)+"\n"
#            t += u"\tsoutenance : "+pourCent2(ev_tot['S'][0], True)+"\n"
            return t#.encode(SYSTEM_ENCODING)
            
            
    
    ######################################################################################  
    def GetCode(self, i = None):
        return "Projet"
    

    ######################################################################################  
    def GetNom(self):
        return self.intitule
#        if self.intitule != self.support.nom:
#            return self.intitule + u"\n-\n" + self.support.nom
#        else:
#            if self.intitule != u"":
#                return self.intitule
#            else:
#                return self.support.nom
    
    
    ######################################################################################  
    def getBranche(self):
#        print "getBranche Projet"
        """ Renvoie la branche XML du projet pour enregistrement
        """
        # Création de la racine
        projet = ET.Element("Projet")
        
        projet.set("Version", version.__version__) # à partir de la version 5.7
        
        projet.set("Intitule", self.intitule)
        
        self.lien.getBranche(projet)
        
        projet.set("Problematique", remplaceLF2Code(self.problematique))
#        print "   ", self.problematique
#
        if self.commentaires != "":
            projet.set("Commentaires", self.commentaires)

        projet.set("Position", "_".join([str(p) for p in self.position]))
        projet.set("Annee", str(self.annee))
        
        # Organisation
        projet.set("NbrRevues", str(self.nbrRevues))
        projet.set("PosRevues", '-'.join(self.positionRevues))
#        projet.set("R1avC", str(self.R1apresConception))
        
        equipe = ET.SubElement(projet, "Equipe")
        for p in self.equipe:
            equipe.append(p.getBranche())
        
        projet.append(self.support.getBranche())
        
        taches = ET.SubElement(projet, "Taches")
        for t in self.taches:
            taches.append(t.getBranche())
        
        fs = ET.SubElement(projet, "FonctionsService")
        for f in self.fct_serv:
            fs.append(f.getBranche())
            
        eleves = ET.SubElement(projet, "Eleves")
        for e in self.eleves:
            eleves.append(e.getBranche())
            
        
            
        groupes = ET.SubElement(projet, "Groupes")
        for e in self.groupes:
            groupes.append(e.getBranche())
            
        #
        # pour la fiche de validation
        #
        projet.set("Origine", remplaceLF2Code(self.origine))
        projet.set("Contraintes", remplaceLF2Code(self.contraintes))
        projet.set("Production", remplaceLF2Code(self.production))
        projet.set("BesoinParties", remplaceLF2Code(self.besoinParties))
        projet.set("IntitParties", remplaceLF2Code(self.intituleParties))
        projet.set("NbrParties", str(self.nbrParties))

        projet.set("Synoptique", remplaceLF2Code(self.synoptique))
        
        typologie = ET.SubElement(projet, "Typologie")
        for i, t in enumerate(self.typologie):
            typologie.set("T_"+str(i), str(t))
        
        projet.set("Partenaires", remplaceLF2Code(self.partenariat))
        projet.set("Montant", remplaceLF2Code(self.montant))
        projet.set("SrcFinance", remplaceLF2Code(self.src_finance))
        
#        comp = ET.SubElement(projet, "Competences")
#        for k, lc in constantes._dicCompetences_prj_simple[self.classe.typeEnseignement].items():
#            comp.set(k, str(lc[1]))
        
        return projet
        
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche projet", 
#        print self.GetReferentiel()
        
        err = []
        
        self.intitule = branche.get("Intitule", "")
        
        self.lien.setBranche(branche, self.GetPath())
        
        self.version = branche.get("Version", "")       # A partir de la version 5.7 !

#        print "   ", self.problematique
        self.problematique = remplaceCode2LF(branche.get("Problematique", ""))
        
        self.commentaires = branche.get("Commentaires", "")
        
        
        
        sp = branche.get("Position", "0_0")
        sp = sp.split("_")
        if len(sp) == 1:
            sp = [sp[0], sp[0]]
        self.position = [int(sp[0]), int(sp[1])]
        
        
        prj = self.GetProjetRef()
        if prj is not None:
            if self.version == "": # Enregistré avec une version de pySequence > 5.7
                if self.position[0] == 5:
                    print("Correction position")
                    self.position = prj.getPeriodeEval()
    #        print "position", self.position
            self.code = self.GetReferentiel().getProjetEval(self.position[0]+1)
            
            self.nbrRevues = int(branche.get("NbrRevues"))
            #self.MiseAJourNbrRevues()
#             if not self.nbrRevues in prj.posRevues.keys():
#                 self.nbrRevues = prj.getNbrRevuesDefaut()
            self.positionRevues = branche.get('PosRevues')
            
            
            # Correction en cas de problème pour éviter les incohérences
            if self.nbrRevues is None or self.positionRevues is None:
                self.initRevues()
            else:
                self.positionRevues = self.positionRevues.split("-")
            
            
            
            if len(self.positionRevues) > self.nbrRevues:
                self.positionRevues = self.positionRevues[:self.nbrRevues]
            elif len(self.positionRevues) < self.nbrRevues:
                # On réduit le nombre de revues aux nombre de positions !!
                self.nbrRevues = len(self.positionRevues)
                
            
            
            
#                                               '-'.join(list(ref.posRevues[self.nbrRevues]))).split('-')
    
#             if self.nbrRevues == 3: # Car par défaut c'est 2
            
        self.annee = eval(branche.get("Annee", str(constantes.getAnneeScolaire())))

        brancheEqu = branche.find("Equipe")
        self.equipe = []
        for e in list(brancheEqu):
            prof = Prof(self)
            Ok = prof.setBranche(e)
            if not Ok : 
                err.append(constantes.Erreur(constantes.ERR_PRJ_EQUIPE))
            self.equipe.append(prof)

        brancheSup = branche.find("Support")
        if brancheSup != None:
            Ok = self.support.setBranche(brancheSup)
            if not Ok : 
                err.append(constantes.Erreur(constantes.ERR_PRJ_SUPPORT))
        
        
        brancheFS = branche.find("FonctionsService")
        self.fct_serv = []
        if brancheFS is not None:
            for f in list(brancheFS):
                fs = FonctionService(self)
                Ok = fs.setBranche(f)
              
                if not Ok : 
                    err.append(constantes.Erreur(constantes.ERR_PRJ_FS))
                
                self.fct_serv.append(fs)

            
        brancheEle = branche.find("Eleves")
        self.eleves = []
        for e in list(brancheEle):
            eleve = Eleve(self)
            Ok = eleve.setBranche(e)
            if not Ok : 
                err.append(constantes.Erreur(constantes.ERR_PRJ_ELEVES))
            
            self.eleves.append(eleve)
            
            
        
        brancheGrp = branche.find("Groupes")
        self.groupes = []
        if brancheGrp != None:
            for e in list(brancheGrp):
                groupe = Groupe(self)
                Ok = groupe.setBranche(e)
                if not Ok : 
                    err.append(constantes.Erreur(constantes.ERR_PRJ_GROUPES))
                
                self.groupes.append(groupe)
        
        #
        # pour la fiche de validation
        #
        self.origine = remplaceCode2LF(branche.get("Origine", ""))
        self.contraintes = remplaceCode2LF(branche.get("Contraintes", ""))
        self.production = remplaceCode2LF(branche.get("Production", ""))
        self.besoinParties = remplaceCode2LF(branche.get("BesoinParties", ""))
        self.intituleParties = remplaceCode2LF(branche.get("IntitParties", ""))
        self.nbrParties = eval(branche.get("NbrParties", "1"))
      
        self.synoptique = remplaceCode2LF(branche.get("Synoptique", ""))
        
        self.typologie = []
        typologie = branche.find("Typologie")
        if typologie != None:
            i = 0
            continuer = True
            while continuer:
                t = typologie.get("T_"+str(i), "")
                if t == "":
                    continuer = False
                else:
                    self.typologie.append(eval(t))
                    i += 1
            
        self.partenariat = remplaceCode2LF(branche.get("Partenaires", ""))
        self.montant = remplaceCode2LF(branche.get("Montant", ""))
        self.src_finance = remplaceCode2LF(branche.get("SrcFinance", ""))
        
        
      
        #
        # Les poids des compétences (Fixés depuis BO 2014)
        #
#        brancheCmp = branche.find("Competences")
#        if brancheCmp != None:
#            for k, lc in constantes._dicCompetences_prj_simple[self.classe.typeEnseignement].items():
#                lc[1] = eval(brancheCmp.get(k))
        
        
        #
        # Les tâches
        #
        brancheTac = branche.find("Taches")
        tachesRevue = self.getTachesRevue()
        
        self.taches = []
        adapterVersion = True
        
        for e in list(brancheTac):
            phase = e.get("Phase")
            if phase in TOUTES_REVUES_EVAL_SOUT:
                if phase == "S":
                    num = len(tachesRevue)-1
                else:
                    num = eval(phase[1])-1
#                 print("tachesRevue", tachesRevue, num)
                if 0 <= num < len(tachesRevue):
                    e = tachesRevue[num].setBranche(e)
                    err.extend(e)
                    if len(e) > 0:
                        err.append(constantes.Erreur(constantes.ERR_PRJ_TACHES, phase))
                
                    self.taches.append(tachesRevue[num])
                adapterVersion = False
            else:
                tache = Tache(self, branche = e)
#                 if int(tache.code) < 0 : # ça s'est mal passé lors du setbranche ...
#                     err.append(constantes.Erreur(constantes.ERR_PRJ_TACHES, tache.code))
#                     return err
                    
#                tache.setBranche(e)
                self.taches.append(tache)
#        self.CorrigerIndicateursEleve()
        
        # On corrige si le nombre de revues n'est pas compatible avec les limites fixées par le référentiel#
        # Il faut le faire après avoir chargé les tâches
        if prj is not None:
            if not (min(prj.posRevues.keys()) <= self.nbrRevues <= max(prj.posRevues.keys())) :
    #             print("> initRevues")
                self.initRevues()
                self.MiseAJourNbrRevues()
                
                
        # Pour récupérer les prj créés avec la version beta1
        if adapterVersion:
            self.taches.extend(tachesRevue)
        
        if prj is not None:
            self.SetCompetencesRevuesSoutenance()

        if hasattr(self, 'panelPropriete'):
#            if ancienneFam != self.classe.familleEnseignement:
            #self.initRevues()
            
            self.MiseAJourNbrRevues()
           
#            self.GetPanelPropriete().MiseAJourTypeEnseignement()
#            
#            self.GetPanelPropriete().MiseAJour()
 
        return err
        
#    ######################################################################################  
#    def GetLastPosition(self):
#        n = 0
#        for p in self.GetReferentiel().periodes:
#            n+=p[1]
#        n = n - (self.GetProjetRef().getNbrPeriodes())
#        return n-1
    
    
    
    ######################################################################################  
    def SetPosition(self, pos, first = False):
#        print "SetPosition", pos
#        print "  position actuelle :", self.position
#        posEpreuve = self.GetProjetRef().getPeriodeEval()
        kproj = self.GetReferentiel().getProjetEval(pos[0]+1)
#        print "  >", kproj
#        print "  posEpreuve", posEpreuve
    

        ###################################################################
        # on efface toutes les revues
        def effacerRevues():
            lst = []
            for t in self.taches:
                if t.phase in TOUTES_REVUES_EVAL_SOUT:
                    if hasattr(t, 'branche'):
                        lst.append(t.branche)
            for a in reversed(lst):
                self.SupprimerTache(item = a, verrouiller = False, doUndo = False)
        
        
        
        # On change de projet
        if self.code != kproj:
            self.code = kproj
            effacerRevues()
            
            # On passe à une position "épreuve"
            if hasattr(self, 'arbre') and self.code is not None:
                for tr in self.creerTachesRevue():
                    self.taches.append(tr)
                    tr.ConstruireArbre(self.arbre, self.brancheTac)
                    tr.SetCode()
#                    if hasattr(tr, 'panelPropriete'):
#                        tr.panelPropriete.MiseAJour()
                self.OrdonnerTaches()
                self.arbre.Ordonner(self.brancheTac)
                self.GetApp().sendEvent(modif = "Changement de Projet")
    

                
            
            
        # Sinon on se contente de redessiner
        else:
            self.GetApp().sendEvent()
        
        
        
#        # On passe à la position "épreuve"
#        if pos == posEpreuve and self.position != posEpreuve:
#            for tr in self.creerTachesRevue():
#                self.taches.append(tr)
#                tr.ConstruireArbre(self.arbre, self.brancheTac)
#                tr.SetCode()
#                if hasattr(tr, 'panelPropriete'):
#                    tr.panelPropriete.MiseAJour()
#            self.OrdonnerTaches()
#            self.arbre.Ordonner(self.brancheTac)
#            if hasattr(self, 'panelPropriete'):
#                self.panelPropriete.sendEvent()
#
#                
#        # On passe de la position "épreuve" à une autre
#        elif pos !=posEpreuve and self.position == posEpreuve:
#            lst = []
#            for t in self.taches:
#                if t.phase in TOUTES_REVUES_EVAL_SOUT:
#                    lst.append(t.branche)
#            for a in reversed(lst):
#                self.SupprimerTache(item = a, verrouiller = False)
#        
#        
#        # Sinon on se contente de redessiner
#        else:
#            if hasattr(self, 'panelPropriete'):
#                self.panelPropriete.sendEvent()
            
            
        self.position = pos
        
#        self.GetPanelPropriete().MiseAJour()


    ######################################################################################  
    def SetProblematique(self, pb):
        self.problematique = pb

        
    ######################################################################################  
    def SetCodes(self):
        self.support.SetCode()
        
        for sce in self.taches:
            sce.SetCode()    
            
        for sy in self.eleves:
            sy.SetCode()    
        
        for sy in self.groupes:
            sy.SetCode()
            
    ######################################################################################  
    def SetLiens(self):
#        for t in self.taches:
#            t.SetLien()    

        self.support.SetLien()  

#    ######################################################################################  
#    def GetFicheHTML(self, param = None):
#        if param is None:
#            return constantes.BASE_FICHE_HTML_PROJET
#        else:
#            if param == "CAL":
#                return constantes.BASE_FICHE_HTML_CALENDRIER
#                
#            elif param == "ANN":
#                pass
#                
#            elif param[:3] == "POS":
#                return constantes.BASE_FICHE_HTML_PERIODES
#                
#            elif param[:3] == "EQU":
#                pass
#            
#            elif param[:2] == "CI":
#                return constantes.BASE_FICHE_HTML_CI
#                
#            else:
#                pass
#    
#        return constantes.BASE_FICHE_HTML_PROJET


    ######################################################################################  
    def SetTip(self, param = None, obj = None):
        """ Mise à jour du TIP (popup)
        """
        
        if param is None:   
            if obj is None:
                # le Projet lui-même
                self.tip.SetHTML(constantes.encap_HTML(constantes.BASE_FICHE_HTML_PROJET))
                self.tip.SetWholeText("int", self.intitule, size = 4)
                self.tip.SetWholeText("ori", self.origine)
                self.tip.SetWholeText("con", self.contraintes)
                self.tip.SetWholeText("pro", self.production)
                self.tip.SetWholeText("dec", self.besoinParties)
                self.tip.SetWholeText("par", self.intituleParties)
            else:
                pass
            
        
        else:               # Un autre élément du Projet
#            print "  *** ", param
            prj = self.GetProjetRef()
            self.tip.SetHTML(self.GetFicheHTML(param = param))
            if param == "PB":
#                self.tip.SetHTML(constantes.BASE_FICHE_HTML_PROB)
                self.tip.SetWholeText( "titre", prj.attributs['PB'][0])
                self.tip.SetWholeText("txt", self.problematique)
            
            elif param == "POS":
                self.Tip_POS()
                
            elif param[:3] == "POS":
                self.Tip_POS(int(param[3])) 
                
            elif param[:3] == "EQU":
                self.Tip_EQU("le Projet")
                
            elif type(obj) == list:
                pass
                
            else:
                
                competence = prj.getCompetence(param[0], param[1:])
                if competence is not None:
#                     print "TIP", param, competence.indicateurs, competence.sousComp
                    self.tip.SetHTML(constantes.encap_HTML(constantes.BASE_FICHE_HTML_COMP_PRJ))
                    
                    k = param[1:].split("\n")
                    titre = self.GetReferentiel().dicoCompetences["S"]._nom
                    if len(competence.sousComp) > 1:
                        titre = titre.Plur_()
                    else:
                        titre = titre.Sing_()
                    
                    if len(k) > 1:
                        titre += " - ".join(k)
                    else:
                        titre += " " + k[0]
                    self.tip.SetWholeText("titre", titre)
                    
#                     intituleComp = "\n".join([textwrap.fill(ind, 50) for ind in competence.intitule.split(u"\n")]) 
                    self.tip.SetWholeText( "int", competence.intitule)
                    
                    if competence.sousComp != {}: #type(competence[1]) == dict:  
                        code = None
                        self.tip.Construire(competence.sousComp, obj, prj, code = code, 
                                        check = isinstance(obj, Tache))
#                         indicEleve = obj.GetDicIndicateurs()
                    else:
                        code = param
                        self.tip.Construire(competence.indicateurs, obj, prj, code = code, 
                                        check = isinstance(obj, Tache))
#                         indicEleve = obj.GetDicIndicateurs()#[param]
#                     print "indicEleve", indicEleve
#                     print "competence.indicateurs", competence.indicateurs
                    
                
        self.tip.SetPage()
        return
        
        
        
    ######################################################################################  
    def VerifPb(self):
        return

        
#    ######################################################################################  
#    def MiseAJourNomsEleves(self):
#        """ Met à jour les noms des élèves après une modification
#            dans les panelPropriété des tâches
#        """
#        for t in self.taches:
#            t.MiseAJourNomsEleves()
        
        
    ######################################################################################  
    def MiseAJourDureeEleves(self):
        for e in self.eleves + self.groupes:
            e.SetCode()
            e.MiseAJourCodeBranche()
    
    
    #############################################################################
    def initRevues(self):
#         print("initRevues",self.code)
        self.nbrRevues = self.GetReferentiel().getNbrRevuesDefaut(self.code)
        self.positionRevues = list(self.GetReferentiel().getPosRevuesDefaut(self.code, self.nbrRevues))
#         print("   ", self.nbrRevues, self.positionRevues)
    
            
    ######################################################################################  
    def MiseAJourNbrRevues(self):
        """ Opère les changements lorsque le nombre de revues a changé...
        """
#         print("MiseAJourNbrRevues", self.nbrRevues, self.positionRevues)
        lstPhasesTaches = [k.phase for k in self.taches if k.phase in TOUTES_REVUES_EVAL]
#         print("   ", lstPhasesTaches)
        if self.nbrRevues == 3 and not _R3 in lstPhasesTaches: # on ajoute une revue
            self.positionRevues.append(self.positionRevues[-1])
            tache = Tache(self, intitule = self.GetProjetRef().phases[_R3][1], 
                          phaseTache = _R3, duree = 0)
            self.taches.append(tache)
            tache.ConstruireArbre(self.arbre, self.brancheTac)
            tache.SetPhase()
            
#            revue2 = self.getTachesRevue()[1]
#            revue2.panelPropriete = PanelPropriete_Tache(self.panelParent, revue2, revue = True)
            
            
        elif self.nbrRevues == 2 and _R3 in lstPhasesTaches:
            t = self.getTachesRevue()[2]
            self.SupprimerTache(item = t.branche)
#            revue2 = self.getTachesRevue()[1]
#            revue2.panelPropriete = PanelPropriete_Tache(self.panelParent, revue2, revue = True)
#         print("   ", self.nbrRevues, self.positionRevues)
        return


    ######################################################################################  
    def AjouterTache(self, event = None, tacheAct = None):
        """ Ajoute une tâche au projet
            et la place juste après la tâche tacheAct (si précisé)
        """
        if tacheAct == None or tacheAct.phase == "S" or tacheAct.phase == "" or self.areTachesPredeterminees():
            tache = Tache(self)
            self.taches.append(tache)
            tache.ordre = len(self.taches)
            tache.ConstruireArbre(self.arbre, self.brancheTac)
            
        else:
            # La phase de la nouvelle tâche
            if not tacheAct.phase in TOUTES_REVUES:
                phase = tacheAct.phase
            elif tacheAct.phase == "Rev":
                i = self.taches.index(tacheAct)
                if i > 0 and self.taches[i-1].phase not in TOUTES_REVUES_SOUT:
                    phase = self.taches[i-1].phase 
                elif i+1<len(self.taches) and self.taches[i+1].phase not in TOUTES_REVUES_SOUT:
                    phase = self.taches[i+1].phase 
                else:
                    phase = ""
            else:
                l = self.GetListePhases()
                i = l.index(tacheAct.phase)
                if i+1<len(l):
                    phase = l[i+1]
                else:
                    phase = ""

            tache = Tache(self, phaseTache = phase)
            self.taches.append(tache)
            tache.ordre = tacheAct.ordre+0.5 # truc pour le tri ...
            tache.ConstruireArbre(self.arbre, self.brancheTac)
            
            tache.SetPhase()
#            if hasattr(tache, 'panelPropriete'):
#                tache.panelPropriete.MiseAJour()
        
        self.Verrouiller()

        self.arbre.EnsureVisible(tache.branche)
        for i in self.arbre._itemWithWindow:
            self.arbre.HideWindows()
        self.arbre.SelectItem(tache.branche)

        self.GetApp().sendEvent(modif = "Ajout d'une Tâche")

        return tache
    
#    ######################################################################################  
#    def CopierTache(self, event = None, item = None):
#        tache = self.arbre.GetItemPyData(item)
#        if isinstance(tache, Tache):
#            self.GetApp().parent.SetData(tache.getBranche())
#            print "Tache", tache, u"copiée"

    ######################################################################################  
    def CollerElem(self, event = None, item = None, btache = None):
        """ Colle la tâche présente dans le presse-papier (branche <btache>)
            après la tâche désignée par l'item d'arbre <item>
        """
#         print "CollerElem"
        if self.arbre.GetItemText(item) == Titres[8]: # racine des Taches
            tache_avant = 0
        else:
            tache_avant = self.arbre.GetItemPyData(item)
            if not isinstance(tache_avant, Tache):
                return
        
        if btache == None:
            btache = GetObjectFromClipBoard("Tache")
            if btache == None:
                return
        
        phase = btache.get("Phase", "")
        if tache_avant != 0 and tache_avant.phase != phase and tache_avant.GetPhaseSuivante() != phase : # la phase est la même
            return
        
        tache = Tache(self, phaseTache = "", branche = btache)
        
        if tache_avant != 0: 
            t = tache_avant.GetTachePrecedente()
            if t is not None:
                ordre = t.ordre
            else:
                ordre = 0
        else:
            ordre = 0
        tache.ordre = ordre+1
        
        # On enlève les élèves en trop
        i = 0
        while i < len(tache.eleves):
            e = tache.eleves[i]
            if e >= len(self.eleves):
                del tache.eleves[i]
            else:
                i += 1
        
#         for t in self.taches[ordre:]:
#             t.ordre += 1
        self.taches.insert(ordre, tache)
        
        self.OrdonnerTaches()
        
#        self.taches.sort(key=attrgetter('ordre'))
#         for t in self.taches[ordre:]:
#             t.SetCode()

            
        tache.ConstruireArbre(self.arbre, self.brancheTac)
        tache.SetCode()
#        tache.GetPanelPropriete().MiseAJourEleves()
        
        self.arbre.Ordonner(self.brancheTac)
        self.GetApp().sendEvent(modif = "Collé d'un élément")
        self.arbre.SelectItem(tache.branche)
            
#         print "   >", self.taches
        self.Verrouiller()
#        print "Tache", tache, u"collée"


    ######################################################################################  
    def InsererRevue(self, event = None, item = None):
        if item == None:
            return
        tache_avant = self.arbre.GetItemPyData(item)
        tache = Tache(self, phaseTache = "Rev")
        tache.ordre = tache_avant.ordre+1
        for t in self.taches[tache_avant.ordre:]:
            t.ordre += 1
        self.taches.append(tache)
        self.taches.sort(key=attrgetter('ordre'))
        
        tache.ConstruireArbre(self.arbre, self.brancheTac)
        tache.SetCode()
#        if hasattr(tache, 'panelPropriete'):
#            tache.panelPropriete.MiseAJour()
        
        self.arbre.Ordonner(self.brancheTac)
        self.GetApp().sendEvent(modif = "Insertion d'une revue")
        self.arbre.SelectItem(tache.branche)
            
        self.Verrouiller()


    ######################################################################################  
    def SupprimerTache(self, event = None, item = None, verrouiller = True, doUndo = True):
        tache = self.arbre.GetItemPyData(item)
        self.taches.remove(tache)
        self.arbre.Delete(item)
        self.SetOrdresTaches()
        if doUndo:
            modif = "Suppression d'une Tâche"
        else:
            modif = ""
        self.GetApp().sendEvent(modif = modif)
        self.MiseAJourDureeEleves()
        if verrouiller:
            self.Verrouiller()
        
        
    ######################################################################################  
    def SetOrdresTaches(self):
        for i, tt in enumerate(self.taches):
            tt.ordre = i+1
            tt.SetCode()


    
    ######################################################################################  
    def OrdonnerListeTaches(self, lstTaches):
#        print "OrdonnerListeTaches", lstTaches
        
        #
        # On enregistre les positions des revues intermédiaires (après qui ?)
        #
        prj = self.GetProjetRef()
        if prj is None:
            return lstTaches
        
        Rev = []
        for i, t in enumerate(lstTaches):
            if t.phase == _Rev:
                if i > 0:
                    Rev.append((t, lstTaches[i-1]))
                else:
                    Rev.append((t, None))   # Après la première tâche

#        print Rev
        
        
        #
        # On fait des paquets par catégorie
        #
        paquet = {'': []}
        for k in prj.listPhases:#['STI']+constantes.NOM_PHASE_TACHE_E.keys(): 
            paquet[k]=[]

        for t in lstTaches:
            paquet[t.phase].append(t)
            
       
        
        # On trie les tâches de chaque paquet  
        for c in [k for k in prj.listPhases if not k in prj.listPhasesEval]:#['Ana', 'Con', 'Rea', 'DCo', 'Val', 'XXX']:
            paquet[c].sort(key=attrgetter('ordre'))

        #
        # On assemble les paquets
        #
#        print "GetListePhases", self.GetListePhases()
        lst = []
        for p in self.GetListePhases()+["S"]:
            lst.extend(paquet[p]) 

#        print lst
        
        #
        # On ajoute les revues intermédiaires
        #
        for r, q in Rev:
#            print "   ", r, q
            if q == None:
                lst.insert(0, r)
            else:
                i = lst.index(q)
#                print "     >>", i
                lst.insert(i+1, r)
    
        #
        # On ajoute les tâches sans phase
        #
        if '' in paquet.keys():
            lst.extend(paquet[''])
            
#        print lst
        return lst
        
    ######################################################################################  
    def OrdonnerTaches(self):
#        print "OrdonnerTaches"
#        print "  ", self.taches,
        self.taches = self.OrdonnerListeTaches(self.taches)
#        print self.taches
        
        self.SetOrdresTaches()
        self.SetCodes()
        self.arbre.Ordonner(self.brancheTac)
        return

    
    ######################################################################################  
    def SupprimerItem(self, item):
#         print "SupprimerItem", item
        data = self.arbre.GetItemPyData(item)
        
        if isinstance(data, Tache) and data.phase not in TOUTES_REVUES_EVAL_SOUT:
            self.SupprimerTache(item = item)
            
        elif isinstance(data, Groupe):
            self.SupprimerGroupe(item = item)
            
        elif isinstance(data, Eleve):
            self.SupprimerEleve(item = item)    
        
        elif isinstance(data, Prof):
            self.SupprimerProf(item = item)
            
        elif isinstance(data, Modele):
            self.support.SupprimerModele(item = item)
            
        elif isinstance(data, FonctionService):
            self.SupprimerFS(item = item)
            
#        elif isinstance(data, LienSequence):
#            self.SupprimerLienSequence(item = item)           
        
    
#    ######################################################################################  
#    def SupprimerLienSequence(self, event = None, item = None):
#        ps = self.arbre.GetItemPyData(item)
#        self.prerequisSeance.remove(ps)
#        self.arbre.Delete(item)
#        self.panelPropriete.sendEvent()
#        
#    ######################################################################################  
#    def AjouterSequencePre(self, event = None):
#        ps = LienSequence(self, self.panelParent)
#        self.prerequisSeance.append(ps)
#        ps.ConstruireArbre(self.arbre, self.branchePre)
#        self.panelPropriete.sendEvent()
#        self.arbre.SelectItem(ps.branche)
        
#     ######################################################################################  
#     def AjouterEleveDansPanelTache(self):
#         for t in self.taches:
#             t.AjouterEleve()
            
    ######################################################################################  
    def SupprimerEleveDansPanelTache(self, i):
        for t in self.taches:
            t.SupprimerEleve(i)  
                  
    ######################################################################################  
    def AjouterEleve(self, event = None):
#        print "AjouterEleve", self.GetProjetRef().maxEleves
        if len(self.eleves) < self.GetProjetRef().maxEleves:
            e = Eleve(self, self.GetNewIdEleve())
            self.eleves.append(e)
            
            e.ConstruireArbre(self.arbre, self.brancheElv)
            self.arbre.Expand(self.brancheElv)
            self.GetApp().sendEvent(modif = "Ajout d'"+ self.GetReferentiel().labels["ELEVES"][2].un_())
            self.OrdonnerEleves()
            self.arbre.SelectItem(e.branche)
            
#             self.AjouterEleveDansPanelTache()
            e.MiseAJourCodeBranche()

    ######################################################################################  
    def AjouterGroupe(self, event = None):
#         print("AjouterGroupe", self.GetProjetRef().maxGroupes)
        if len(self.groupes) < self.GetProjetRef().maxGroupes:
            e = Groupe(self, self.GetNewIdGroupe())
            self.groupes.append(e)
            
            e.ConstruireArbre(self.arbre, self.brancheElv)
            self.arbre.Expand(self.brancheElv)
            self.GetApp().sendEvent(modif = "Ajout d'un Groupe "+ self.GetReferentiel().labels["ELEVES"][2].de_plur_())
            self.OrdonnerEleves()
            self.arbre.SelectItem(e.branche)
#             self.AjouterEleveDansPanelTache()
            e.MiseAJourCodeBranche()
        

    
    ######################################################################################  
    def SupprimerEleve(self, event = None, item = None):
#         print "SupprimerEleve",
        e = self.arbre.GetItemPyData(item)

#         i = self.eleves.index(e)
        i = e.id

#         self.eleves.remove(e)
        del self.eleves[i]

        self.OrdonnerEleves()

        self.arbre.Delete(item)
        self.SupprimerEleveDansPanelTache(i)

        # On fait ça car supprimer un élève a un impact sur les noms des éleves "sans nom"
        for i, e in enumerate(self.eleves):
            e.SetCode()

        self.GetApp().sendEvent(modif = "Suppression d'"+ self.GetReferentiel().labels["ELEVES"][2].un_())
        
        
    ######################################################################################  
    def SupprimerGroupe(self, event = None, item = None):
#         print "SupprimerGroupe",
        e = self.arbre.GetItemPyData(item)

#         i = self.eleves.index(e)
        i = e.id - len(self.eleves)

#         self.eleves.remove(e)
        del self.groupes[i]

        self.OrdonnerEleves()

        self.arbre.Delete(item)

        # On fait ça car supprimer un élève a un impact sur les noms des éleves "sans nom"
        for i, e in enumerate(self.groupes):
            e.SetCode()

        self.GetApp().sendEvent(modif = "Suppression d'un groupe "+ self.GetReferentiel().labels["ELEVES"][2].de_plur_())
    
    ######################################################################################  
    def OrdonnerEleves(self):
#         print "OrdonnerEleves"
        i = -1
        for i,e in enumerate(self.eleves):
            e.id = i
#             print "   e", i
            
        for j,e in enumerate(self.groupes):
            e.id = i+j+1
#             print "   g", i+j+1
        
        # On fait ça car supprimer un élève a un impact sur les noms des éleves "sans nom"
        for i, e in enumerate(self.eleves):
            e.SetCode()
        for i, e in enumerate(self.groupes):
            e.SetCode()
            
            
        self.arbre.Ordonner(self.brancheElv)
        
    ######################################################################################  
    def GetNewIdEleve(self):
        """ Renvoie le 1er numéro d'identification élève disponible
        """
#        print "GetNewIdEleve", 

        for i in range(self.GetProjetRef().maxEleves):
            ok = False
            for e in self.eleves:
                ok = ok or i != e.id
            if ok:
                break
        return i
    

    ######################################################################################  
    def GetNewIdGroupe(self):
        """ Renvoie le 1er numéro d'identification élève disponible
        """
#        print "GetNewIdGroupe", 
        for i in range(self.GetProjetRef().maxGroupes):
            ok = False
            for e in self.groupes:
                ok = ok or i != e.id
            if ok:
                break
        return i + len(self.eleves)
    
    
    ######################################################################################  
    def AjouterFS(self, event):
        ref = self.GetReferentiel()
        if len(self.fct_serv) > 0:
            t = 1
        else:
            t = 0
        fs = FonctionService(self, "", t)
        self.fct_serv.append(fs)
        
        fs.ConstruireArbre(self.arbre, self.brancheFS)
        self.arbre.Expand(self.brancheFS)
        self.GetApp().sendEvent(modif = "Ajout "+ref._nomFS.de_())
        self.OrdonnerFS()
        self.arbre.SelectItem(fs.branche)

        
    ######################################################################################  
    def SupprimerFS(self, item):
        ref = self.GetReferentiel()
        fs = self.arbre.GetItemPyData(item)
        self.fct_serv.remove(fs)
        self.arbre.Delete(item)
        
        self.GetApp().sendEvent(modif = "Suppression "+ref._nomFS.de_())
        self.OrdonnerFS()
#         self.arbre.SelectItem(fs.branche)
        
    ######################################################################################  
    def OrdonnerFS(self):
        """
        """
        FP = [fs for fs in self.fct_serv if fs.type == 0]
        FC = [fs for fs in self.fct_serv if fs.type == 1]
        self.fct_serv = FP+FC
#         print "OrdonnerFS"
#         i = -1
#         for i,fs in enumerate(self.fct_serv):
#             fs.id = i
#             
        for fs in self.fct_serv:
            fs.SetCode()
    
        self.arbre.Ordonner(self.brancheFS)
        
        
    ######################################################################################  
    def GetNewIdFS(self):
        """ Renvoie le 1er numéro d'identification FS disponible
        """
#        print "GetNewIdFS", 
        return len(self.fct_serv)
    
    
    ######################################################################################  
    def OnModifModeles(self):
        n = [m.id for m in self.support.modeles]
        for e in self.eleves:
            for m in e.modeles:
                if not m in n:
                    e.modeles.remove(m)
            e.MiseAJourCodeBranche()
    
    ######################################################################################  
    def MiseAJourPoidsCompetences(self, code = None):
        for t in self.taches:
            t.MiseAJourPoidsCompetences(code)
        self.MiseAJourDureeEleves()
    
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, self.Sing_(), #Titres[9], 
                                        data = self,
                                        image = self.arbre.images["Prj"])
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)
            
        #
        # Le support
        #
        self.support.ConstruireArbre(arbre, self.branche)
        
        #
        # Les profs
        #
        self.branchePrf = arbre.AppendItem(self.branche, Titres[10], data = "Equ")
        for e in self.equipe:
            e.ConstruireArbre(arbre, self.branchePrf) 
        
        #
        # Les élèves
        #
#         print(self.GetReferentiel().labels["ELEVES"][2])
        self.brancheElv = arbre.AppendItem(self.branche, self.GetReferentiel().labels["ELEVES"][2].Plur_(), 
                                           data = "Ele",
                                           image = self.arbre.images["Grp"])
        for e in self.eleves:
            e.ConstruireArbre(arbre, self.brancheElv) 
            
        #
        # Les fonctions de service
        #
        self.brancheFS = arbre.AppendItem(self.branche, self.GetReferentiel()._nomFS.Plur_(), 
                                           data = "FS",
                                           image = self.arbre.images["FS"])
        for e in self.fct_serv:
            e.ConstruireArbre(arbre, self.brancheFS) 
        
        
        
        #
        # Les groupes
        #
        for e in self.groupes:
            e.ConstruireArbre(arbre, self.brancheElv) 
            
        #
        # Les tâches
        #
        self.brancheTac = arbre.AppendItem(self.branche, self.GetReferentiel()._nomTaches.Plur_(), #Titres[8], 
                                           data = "Tac",
                                           image = self.arbre.images["Tac"])
        for t in self.taches:
            t.ConstruireArbre(arbre, self.brancheTac)
        

    ######################################################################################  
    def reconstruireBrancheSeances(self, b1, b2):
        self.arbre.DeleteChildren(self.brancheSce)
        for sce in self.seances:
            sce.ConstruireArbre(self.arbre, self.brancheSce) 
        self.arbre.Expand(b1.branche)
        self.arbre.Expand(b2.branche)
        
    
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):    
        """ Affiche le menu contextuel associé é la séquence
            ... ou bien celui de itemArbre concerné ...
        """
#         print "AfficherMenuContextuel"
        ref = self.GetReferentiel()
        
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([["Enregistrer", self.app.commandeEnregistrer,
                                              getIconeFileSave()],
#                                             [u"Ouvrir", self.app.commandeOuvrir],
                                             ["Exporter la fiche (PDF ou SVG)", self.app.exporterFiche, 
                                              None],
                                            ])
            
#        [u"Séquence pédagogique",
#          u"Prérequis",
#          u"Objectifs pédagogiques",
#          u"Séances",
#          u"Systèmes"]
        
#        elif isinstance(self.arbre.GetItemPyData(itemArbre), Competences):
#            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Eleve):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Prof):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Tache):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), LienSequence):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Modele):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)           
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Support):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)           
            
        elif self.arbre.GetItemText(itemArbre) == ref.labels["ELEVES"][2].plur_(): # Eleve
            self.app.AfficherMenuContextuel([["Ajouter "+ ref.labels["ELEVES"][2].un_(), self.AjouterEleve, 
                                              scaleImage(images.Icone_ajout_eleve.GetBitmap())],
                                             ["Ajouter un groupe "+ ref.labels["ELEVES"][2].de_plur_(), self.AjouterGroupe, 
                                              scaleImage(images.Icone_ajout_groupe.GetBitmap())]])
            
        elif self.arbre.GetItemText(itemArbre) == Titres[8]: # Tache
            listItems = [["Ajouter %s" %ref._nomTaches.un_(), self.AjouterTache, 
                          scaleImage(images.Icone_ajout_tache.GetBitmap())]]
            elementCopie = GetObjectFromClipBoard('Tache')
            if elementCopie is not None:
                phase = elementCopie.get("Phase", "")
                if phase == self.GetListePhases()[0]: # C'est bien une tâche de la première phase
#                 if self.phase == phase or self.GetPhaseSuivante() == phase : # la phase est la même
                    listItems.append(["Coller après", functools.partial(self.CollerElem, 
                                                                         item = itemArbre, 
                                                                         btache = elementCopie),
                                      getIconePaste()])
            self.app.AfficherMenuContextuel(listItems)
            
        elif self.arbre.GetItemText(itemArbre) == Titres[10]: # Eleve
            self.app.AfficherMenuContextuel([["Ajouter un Professeur", self.AjouterProf, 
                                              scaleImage(images.Icone_ajout_prof.GetBitmap())]])
                                             
        
            
    ######################################################################################       
    def GetCompetencesUtil(self):
        """ Renvoie les listes des codes 
            des compétences utiles au projet
            (pour tracé fiche)
        """
        lst = []
        for t in self.taches:
            lst.extend(t.GetCompetencesUtil())
        lst = list(set(lst))
        lst.sort()
        return lst
    
    ######################################################################################       
    def GetSavoirsUtil(self):
        """ Renvoie les listes des codes 
            des Savoirs utiles au projet
            (pour tracé fiche)
        """
        lst = []
        for t in self.taches:
            lst.extend(t.GetSavoirsUtil())
        lst = list(set(lst))
        lst.sort()
        return lst

    
    ######################################################################################       
    def GetCompetencesVisees(self):
        """ Renvoie la liste des compétences visées (objectifs) 
        """
        return self.GetCompetencesUtil()
    
    
    ######################################################################################       
    def GetSavoirsVises(self):
        """ Renvoie la liste des Savoirs visés (objectifs) 
        """
        return self.GetSavoirsUtil()
    
    
    ######################################################################################  
    def GetNbrPhases(self):
        """Renvoie le nombre de phases dans le projet, y compris les revues
            !! les revues intermédiaires coupent parfois une phase en deux !
            (pour tracé de la fiche)
        """
        n = 0
        for i, t in enumerate(self.taches):
            if (i == 0 or t.phase != self.taches[i-1].phase):
                n += 1
        return n

    ######################################################################################  
    def GetListeNomsPhases(self, avecRevuesInter = False):
#        print "GetListeNomsPhases"
        lst = []
        prj = self.GetProjetRef()
        for p in self.GetListePhases():
            if p in prj.listPhases:#[:-1]:
                n = prj.phases[p][0]
                if not p in TOUTES_REVUES_EVAL_SOUT:
                    n = "     "+n
                lst.append(n)
            elif p in prj.listPhasesEval:
                n = prj.phases[p][0]
                if not p in TOUTES_REVUES_EVAL_SOUT:
                    n = "     "+n
                lst.append(n)
                
#        for p in self.GetListePhases():
#            if p in constantes.NOM_PHASE_TACHE_COURT[self.GetTypeEnseignement(simple = True)].keys():
#                lst.append(constantes.NOM_PHASE_TACHE_COURT[self.GetTypeEnseignement(simple = True)][p])
#            elif p in constantes.NOM_PHASE_TACHE_E_COURT.keys():
#                lst.append(constantes.NOM_PHASE_TACHE_E_COURT[p])

        return lst
        
    ######################################################################################  
    def GetListePhases(self, avecRevuesInter = False):
        """ Renvoie la liste ordonnée des phases dans le projet
        """
#         print("GetListePhases")
        prj = self.GetProjetRef()
        if prj is None:
            return []
#        lst = list(constantes.PHASE_TACHE[self.GetTypeEnseignement(simple = True)][:-1])
        lst = [k for k in prj.listPhases if not k in prj.listPhasesEval]
#        lst = list(self.GetReferentiel().listPhases_prj)
#        print "  ", self.classe.GetReferentiel()
#         print("  ", lst)
#        print "  ", self.nbrRevues
#         lr = list(range(1, self.nbrRevues+1))
#         lr.reverse()
#         print("     ", lr,  self.positionRevues)
        for r in range(self.nbrRevues, 0, -1):
#            print "     ", lr,  self.positionRevues[r-1]
            if self.positionRevues[r-1] in  lst:
                lst.insert(lst.index(self.positionRevues[r-1])+1, "R"+str(r))
#        print "  ", lst
        return lst
        
#        # Ancienne version (marche pas avec les Rev)
#        p = []
#        for t in self.taches:
#            if ((not t.phase in p) or t.phase == "Rev") and t.phase != "":
#                p.append(t.phase)
#        return len(p)
        
    ######################################################################################  
    def GetIntituleTaches(self):
        """ Renvoie les listes des codes et des intitulés 
            de toutes les tâches
            (pour tracé fiche)
        """
        codTaches = []
        intTaches = []
        for s in self.taches:
            if hasattr(s, 'code') and s.intitule != "" and not s.intituleDansDeroul:
                codTaches.append(s.code)
                intTaches.append(s.intitule)
        return codTaches, intTaches
        
        
    ######################################################################################  
    def getNomFichierDefaut(self, prefixe):
        return getNomFichier(prefixe, self.intitule[:20])
#        nomFichier = prefixe+"_"+self.intitule[:20]
#        for c in ["\"", "/", "\", ", "?", "<", ">", "|", ":", "."]:
#            nomFichier = nomFichier.replace(c, "_")
#        return nomFichier


#    ######################################################################################  
#    def HitTest(self, x, y):
#        branche = None
#        autresZones = self.taches + self.eleves+ self.equipe + [self.support]
#        continuer = True
#        i = 0
#        while continuer:
#            if i >= len(autresZones):
#                continuer = False
#            else:
#                branche = autresZones[i].HitTest(x, y)
#                if branche:
#                    continuer = False
#            i += 1
#        
#        if branche == None:
#            if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
#                return self.branche
#
#        return branche


#    ######################################################################################  
#    def HitTestCompetence(self, x, y):
#        if hasattr(self, 'rectComp'):
#            for k, ro in self.rectComp.items():
#                rect = [r[:-1] for r in ro]
#                obj = [o[-1] for o in ro]
#                ok, i = dansRectangle(x, y, rect)
#                if ok:
#                    return k, obj[i]
#
#
#    ######################################################################################  
#    def HitTestPosition(self, x, y):
#        if hasattr(self, 'rectPos'):
#            for i, rectPos in enumerate(self.rectPos):
#                if dansRectangle(x, y, (rectPos,))[0]:
#                    return i

    ######################################################################################  
    def DefinirCouleurs(self):
        if hasattr(self.GetReferentiel(), '_listesCompetences_simple'):
            draw_cairo.DefinirCouleurs(self.GetNbrPeriodes(),
                                       len(self.GetReferentiel()._listesCompetences_simple["S"]),
                                       len(self.eleves + self.groupes))
        
     
    ######################################################################################  
    def Rafraichir(self):
        self.DefinirCouleurs()
        
    #############################################################################            
    def drawPeriode(self, ctx, larg):
        prop = 7
        w, h = 0.04*prop * draw_cairo.COEF, 0.04 * draw_cairo.COEF
        ctx.scale(larg/w, larg/w) 
    #     ctx.set_source_rgba(1,1,1,1)
    #     ctx.paint()
        draw_cairo.DrawPeriodes(ctx, (0,0,w,h), 
                                    self.getRangePeriode(), 
                                    self.GetReferentiel().periodes,
                                    self.GetReferentiel().projets)
        
    #############################################################################            
    def getBitmapPeriode(self, larg):
        imagesurface = draw_cairo.getBitmapPeriode(larg, self.getRangePeriode(), 
                                                       self.GetReferentiel().periodes ,
                                                       self.GetReferentiel().projets, 
                                                       prop = 7)
        return getBitmapFromImageSurface(imagesurface)
    
    #############################################################################
    def MiseAJour(self):
        self.app.SetTitre()
        self.DefinirCouleurs()
        self.SetCompetencesRevuesSoutenance()
        
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):#, changeFamille = False):
#        print "MiseAJourTypeEnseignement projet"

        self.code = self.GetReferentiel().getCodeProjetDefaut()
        self.classe.MiseAJourTypeEnseignement()
        
        self.position = self.GetPeriodeDefaut()
#        print "position", self.position
        
        if hasattr(self, 'brancheElv'):
            self.brancheElv.SetText(self.GetReferentiel().labels["ELEVES"][2].plur_())
            self.arbre.Layout()
            self.arbre.Refresh()
        
        for e in self.eleves:
            e.MiseAJourTypeEnseignement()
        
        self.MiseAJour()

                
    
        

    #############################################################################
    def Verrouiller(self):
        self.classe.Verrouiller(len(self.GetCompetencesUtil()) != 0 or len(self.taches) != self.nbrRevues+1)
#        self.GetPanelPropriete().Verrouiller(self.pasVerouille)

    
    ######################################################################################  
    def TesterExistanceGrilles(self, nomFichiers, dirpath, win = None):
#        print "TesterExistanceGrilles", nomFichiers
        
        if win is None:
            win = self.GetApp()
        existe = []
        for fe in nomFichiers.values():
            for f in fe.values():
                if os.path.isfile(f[1]):
                    existe.append(f[1])
        
        if len(existe) > 0:
            
            nf = [testRel(path, dirpath) for path in existe]
            if len(existe) == 1:
                m = "La grille d'évaluation existe déja !\n\n" \
                    "\t%s\n\n" \
                    "Voulez-vous la remplacer ?" %existe[0]
            else:
                m = "Les grilles d'évaluation existent déja !\n\n" \
                    "\t%s\n\n" \
                    "dans le dossier :\n" \
                    "\t%s\n\n" \
                    "Voulez-vous les remplacer ?" %("\n".join(nf), dirpath)
        
            res = messageYesNo(win, "Fichier existant", 
                                      m, wx.ICON_WARNING)
            
            if res:
                for nf in existe:
                    try:
                        os.remove(nf)
                    except:
                        pass
            return res
            
        return True
    
    
    ######################################################################################  
    def TesterExistanceDetails(self, nomFichiers, dirpath, win = None):
        
        if win is None:
            win = self.GetApp()
        existe = []
        for fe in nomFichiers.values():
            if os.path.isfile(fe):
                existe.append(fe)
        
        if len(existe) > 0:
            
            nf = [testRel(path, dirpath) for path in existe]
            if len(existe) == 1:
                m = "Le fichier de description détaillée des tâches existe déja !\n\n" \
                    "\t%s\n\n" \
                    "Voulez-vous le remplacer ?" %existe[0]
            else:
                m = "Les fichiers de description détaillée des tâches existent déja !\n\n" \
                    "\t%s\n\n" \
                    "dans le dossier :\n" \
                    "\t%s\n\n" \
                    "Voulez-vous les remplacer ?" %("\n".join(nf), dirpath)
        
            res = messageYesNo(win, "Fichier existant", 
                                      m, wx.ICON_WARNING)
            
            if res:
                for nf in existe:
                    try:
                        os.remove(nf)
                    except:
                        pass
            return res
            
        return True
    
    
    ######################################################################################  
    def VerifierIndicRevue(self, numRevue):
        r = self.getTachesRevue()[numRevue-1]
        self.SetCompetencesRevuesSoutenance()
#        print r.phase
#        print r.indicateursMaxiEleve[0]
#        print r.GetDicIndicateursEleve(self.eleves[1])
#        print r.indicateursEleve
        
        for codes in r.indicateursEleve.values():
            for code in codes:
                if not code in r.indicateursMaxiEleve[0]:
                    codes.remove(code)
                   
#        print r.indicateursEleve
        return


    ######################################################################################  
    def VerifierVersionGrilles(self):
        """ Vérification que les grilles d'évaluation enregistrées dans le fichier du projet
            sont toujours valides et à jour.
            (Exécuté à l'ouverture d'un projet)
        """
        pb = []
        prj = self.GetProjetRef()
        if prj is None:
            return
        
        for k in prj.parties.keys():
            if not os.path.isfile(grilles.getFullNameGrille(prj.grilles[k][0])):
                prjdef = REFERENTIELS[self.GetTypeEnseignement()].getProjetDefaut()
                if os.path.isfile(grilles.getFullNameGrille(prjdef.grilles[k][0])):
                    prj.grilles[k] = prjdef.grilles[k]
                    prj.cellulesInfo[k] = prjdef.cellulesInfo[k]
                else:
#                     print(k, grilles.getFullNameGrille(prjdef.grilles[k][0]))
                    pb.append(k)
        
        if len(pb) > 0:
            messageErreur(self.GetApp(), "Fichier non trouvé !",
                                  "Le(s) fichier(s) grille :\n    " + ";".join(pb) + "\n" \
                                  "n'a(ont) pas été trouvé(s) ! \n")
    
    
    #############################################################################
    def GetRevuesAvecCompetences(self):
        return [t for t in self.taches if t.phase in [_R1, "Rev"] or (t.phase == _R2 and self.nbrRevues == 3)]
    
    #############################################################################
    def GetTachesPredeterminees(self):
        return [t for t in self.taches if t.estPredeterminee()]
    
#    #############################################################################
#    def MiseAJourTachesEleves(self):
#        """ Mise à jour des phases de revue 
#            pour lesquelles il y a des compétences à cocher
#        """
#        print "MiseAJourTachesEleves"
#        for t in self.GetRevuesAvecCompetences() + self.GetTachesPredeterminees():
#            t.GetPanelPropriete().ReconstruireArbres()


    
    #############################################################################
    def SetCompetencesRevuesSoutenance(self, miseAJourPanel = True):
        """ Attribue à la soutenance et à la revue n°2 (ou n°3 si 3 revues)
            les compétences et indicateurs 
            mobilisés par les tâches précédentes
        """
#        print "SetCompetencesRevuesSoutenance", len(self.eleves)
#        tousIndicateurs = self.GetReferentiel()._dicIndicateurs_prj
#        print tousIndicateurs
#        REFERENTIELS[self.classe.typeEnseignement].dicIndicateurs_prj
        if self.GetProjetRef() is None or self.GetProjetRef()._pasdIndic:
            return
        
        tR1 = None
        tR2 = None
        
        indicateurs = [{} for e in range(len(self.eleves)+1)]   # 0 : tous les élèves

        for t in self.taches:   # toutes les tâches, dans l'ordre
            
            if t.phase in TOUTES_REVUES_SOUT:
#                print "  ", t.phase
                for neleve in range(len(self.eleves)+1):

                    if t.phase in [_R1, "Rev"] or (t.phase == _R2 and self.nbrRevues == 3):
                        t.indicateursMaxiEleve[neleve] = []
                    else:
                        t.indicateursEleve[neleve] = []

                    for c, l in indicateurs[neleve].items():
                        for i, ok in enumerate(l):
                            if ok:
                                codeIndic = c+"_"+str(i+1)
                                
                                # Phase de Conduite
                                if self.GetProjetRef().getTypeIndicateur(codeIndic) == 'C': # tousIndicateurs[c][i][1]: # Indicateur "revue"
                                    if t.phase in TOUTES_REVUES:
                                        
                                        if (True in self.GetReferentiel().compImposees.values()): #self.GetReferentiel().compImposees['C']:
                                            if self.GetProjetRef().getIndicateur(codeIndic).getRevue() == t.phase:
#                                                print "  compImposees", t.phase, ":", codeIndic
                                                t.indicateursEleve[neleve].append(codeIndic)
#                                                print "  >>", t.indicateursEleve
                                                
                                        elif t.phase in [_R1, _Rev] or (t.phase == _R2 and self.nbrRevues == 3):
                                            t.indicateursMaxiEleve[neleve].append(codeIndic)
                                  
                                        else:
                                            if t.phase == _R2: # 2 revues
                                                if tR1 != None and not codeIndic in tR1.indicateursEleve[neleve]: # R1 est passée
                                                    t.indicateursEleve[neleve].append(codeIndic)
                                                   
                                                            
                                            else: # t.phase == _R3
                                                if tR2 != None and not codeIndic in tR2.indicateursEleve[neleve] and not codeIndic in tR1.indicateursEleve[neleve]: # R2 est passée
                                                    t.indicateursEleve[neleve].append(codeIndic)
                                        
                                # Phase de Soutenance    
                                else:
                                    if t.phase == _S:
                                        t.indicateursEleve[neleve].append(codeIndic)

                    if neleve == 0: # Une seule fois 
                        if t.phase in [_R1, "Rev"] or (t.phase == _R2 and self.nbrRevues == 3):
                            ti = []
                            for i in t.indicateursEleve[neleve]:
                                if i in t.indicateursMaxiEleve[neleve]:
                                    ti.append(i)

                            t.indicateursEleve[neleve] = ti
#                            if miseAJourPanel and hasattr(t.GetPanelPropriete(), 'arbre'):
#                                t.GetPanelPropriete().arbre.MiseAJourTypeEnseignement(t.GetReferentiel())
                            

#                                t.panelPropriete.MiseAJour()
                            if t.phase == _R1:
                                tR1 = t # la revue 1 est passée !
                            elif t.phase == _R2:
                                tR2 = t # la revue 2 est passée ! (3 revues)
#                print "  >>", t.indicateursMaxiEleve
                
                
            else:   # On stock les indicateurs dans un dictionnaire CodeCompétence : ListeTrueFalse
                indicTache = t.GetDicIndicateurs()
                for c, i in indicTache.items():
                    for neleve in range(len(self.eleves)+1):
                        if (neleve == 0) or ((neleve-1) in t.eleves):
                            if c in indicateurs[neleve].keys():
                                indicateurs[neleve][c] = [x or y for x,y in zip(i, indicateurs[neleve][c])]
                            else:
                                indicateurs[neleve][c] = i 

#                if t.estPredeterminee() and miseAJourPanel and hasattr(t.GetPanelPropriete(), 'arbre'):
#                    t.GetPanelPropriete().arbre.MiseAJourTypeEnseignement(t.GetReferentiel())
                
            if not t.estPredeterminee():
                t.ActualiserDicIndicateurs()


    #############################################################################
    def enregistrer(self, nomFichier, dialog = True):
        # Le projet
        projet = self.getBranche()
        classe = self.classe.getBranche()
        
        # La racine
        root = ET.Element("Projet_Classe")
        root.append(projet)
        root.append(classe)
        constantes.indent(root)
        
        return enregistrer_root(root, nomFichier, dialog = dialog)
#                        





####################################################################################################
#
#        Projet
#
####################################################################################################
class Progression(BaseDoc, Grammaire):
    """Document de type Progression pédagogique
        :param classe: Classe associée au document
        :type classe: pysequence.Classe
        :param intitule: Intitulé du document
        :type intitule: str
    """
    def __init__(self, app, classe = None, intitule = "", ouverture = False):
        
        Grammaire.__init__(self, "Progression(s)$f")
#         self.nom_obj = "Progression"
#         self.article_c_obj = "de la"
#         self.article_obj = "la"
        
        self.image = None
        
        BaseDoc.__init__(self, app, classe, intitule)
        

        self.nbrCreneaux = constantes.NBR_CRENEAUX_DEFAUT
        
        self.sequences_projets = []     # liste de LienSequence et de LienProjet et de Referentiel.Projet
        
#         self.calendriers = []
        self.calendrier = Calendrier(self, constantes.getAnneeScolaire())
        self.eleves = []
        self.equipe = []
        self.themes = []
        self.code = self.GetReferentiel().getCodeProjetDefaut()
        
        self.version = ""
        
        self.mode = "C"     # Mde d'affichage de la fiche : C = compétences - S = Savoirs
        
        if not ouverture:
            self.MiseAJourTypeEnseignement()
            
        # Le module de dessin
        self.draw = draw_cairo_prg



    ######################################################################################  
    def __repr__(self):
        return "Progression "+ self.intitule


    ######################################################################################  
    def GetType(self):
        return 'prg'
    
    ######################################################################################  
    def GetAnnees(self):
        return "%s - %s" %(self.calendrier.annee, self.calendrier.GetAnneeFin())


    ######################################################################################  
    def GetProjetRef(self):
        """ Renvoie le projet (Referentiel.Projet) de référence
        """
#        print "GetProjetRef", self.code
        if self.code == None:
            return self.GetReferentiel().getProjetDefaut()
        else:
            if self.code in self.GetReferentiel().projets.keys():
                return self.GetReferentiel().projets[self.code]
            else:
                return None


    ######################################################################################  
    def GetPositions(self):
        """ Renvoie la liste de toutes les positions occupées par les Séquences et les Projets
        """
        l = []
#         for doc in [s.GetDoc() for s in self.sequences_projets]:
        for s in self.sequences_projets:
            doc = s.GetDoc()
#             print "  ", s.path
            if doc is not None:
                l.extend(doc.GetPositions())
        return list(set(l))


    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
#         print("GetPtCaract prg")
        lst = BaseDoc.GetPtCaract(self)
        ##################################### 
            
        for s in self.sequences_projets + self.eleves:
            lst.extend(s.GetPtCaract())
            
#         print(">>>", lst)
        return lst    
    
    ######################################################################################  
    def EnrichiHTMLdoc(self, doc):
        """ Enrichissement de l'image SVG <doc> (format XML) avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens
             - ...
             :doc: beautifulsoup
        """
#         print("EnrichiHTML Progression")
        ElementBase.EnrichiHTML(self, doc)
        
        for s in self.sequences_projets:# + self.eleves:
            ElementBase.EnrichiHTML(s, doc)
        
    
    ######################################################################################  
    def EnrichiSVGdoc(self, doc):
        """ Enrichissement de l'image SVG <doc> (format XML) avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens
             - ...
             :doc: xml.doc.minidom
        """
#        print "EnrichiSVG sequence"
        if hasattr(self, 'app'):
            t = doc.createElement("title")
            path = os.path.split(self.app.fichierCourant)[1]
            path = str(path) # Conversion en unicode !!!
            txt = doc.createTextNode(path)
            
            t.appendChild(txt)
            svg = doc.getElementsByTagName("svg")[0]
            svg.insertBefore(t, svg.childNodes[0])
        
        
        ElementBase.EnrichiSVG(self, doc)

        
        for s in self.sequences_projets:# + self.eleves:
            ElementBase.EnrichiSVG(s, doc)
            
            
    ######################################################################################  
    def GetNbrPeriodesEffectif(self):
        """ Renvoie le nombre de périodes occupées par les Séquences et le Projets
        """
        return len(self.GetPositions())

    ######################################################################################  
    def GetNbrCreneauxMini(self):
        """ Renvoie le nombre de créneau minimum autorisé
             --> nombre de créneaux utilisés dans les Sequences ou Projets
        """
        return max([s.creneaux[-1]+1 for s in self.sequences_projets]+[1])

    ######################################################################################  
    def SetNbrCreneaux(self, nc):
        """ Modifie le nombre de créneaux horaire utilisés dans la progression
             Vérifie avant qu'on ne passe pas en dessous du nombre de créneaux utilisés dans les Sequences ou Projets
        """
        nc_sp = self.GetNbrCreneauxMini()
        if nc >= nc_sp:
            self.nbrCreneaux = nc
            return True
        
        return False
    
    
    ######################################################################################  
    def SetMode(self, m):
        """ Modifie le mode d'affichage
        """
        if m in ("C","S"):
            self.mode = m
        elif m == 0:
            self.mode = "C"
        elif m == 1:
            self.mode = "S"
    
    
    ######################################################################################  
    def GetModeInt(self):
        if self.mode == "S": return 1
        return 0
        
    
    ######################################################################################  
    def GetRectangles(self):
        """Calcule l'arrangement des rectangles représentant les Séquences et les Projets
            Renvoie la liste des rectangles x, y, w, h
            Dans une grille : Période-Lignes-Colonnes
            [
            [(None, None, None)],      Période 0, Ligne 0
                
            [(0, 0, 0),                Période 1, Ligne 1
            (1, 1, 2)],                Période 1, Ligne 2
                
            [(1, 1, 2),                Période 2, Ligne 3
            (3, 3, 2)],                Période 2, Ligne 4
                
            [(None, None, 2)],         Période 3, Ligne 5
            ]
                
                
            Renvoie :
            les rectangles
            la liste des lignes correspondant au début d'une période
            les positions "horaire" des lignes
            un code d'erreur (anomalie détectée)
        """
        err = 0
#         print "GetRectangles", 
        
        ref = self.classe.referentiel
        
        # Nombre de creneaux utilisés dans la progression
        nc = self.nbrCreneaux
        
        # Nombre de périodes utilisés dans la progression
        np = ref.getNbrPeriodes()  
    
#         print np, nc
        
        # Grille niveau 1
        grille = [[[] for c in range(nc)] for l in range(np)]
        for i, lienDoc in enumerate(self.sequences_projets):
#             print "  ", i, lienDoc
            p = lienDoc.GetPosition()   # Première et dernière période
            
            if p[0] == p[-1]:
                p = [p[0]]
            c = lienDoc.GetCrenaux()    # Liste des créneaux
#             print "    ",p, c
            for lig in p:
                for col in c:
                    grille[lig][col].append(i)
        
        
        # Grille  Périodes-Lignes-Colonnes (brute)
        N = list(range(len(self.sequences_projets)))
        grilles_p = []
        for lig in grille:
            lig2 = []
            for c, cre in enumerate(lig):
                lig2.append([n if n in cre else None for n in N ])
#                 cre2 = []
#                 for n in N:
#                     if n in cre:
#                         cre2.append(n)
#                     else: 
#                         cre2.append(None)
#                 lig2.append(cre2)
            lig2 = list(zip(*lig2))
            grilles_p.append([l for l in lig2]) 

#         print "grilles_p", grilles_p
        
        # Compactage de la grille
        for g in grilles_p:
            l = 1
            while l < len(g):
                z = list(zip(g[l-1], g[l]))
                if  all(x is None or y is None for x, y in z):
                    g[l-1] = tuple(y or x for x, y in z) # Ne pas inverser x et y car 0 or None renvoie None
                    del g[l]
                else:
                    l+=1

#         print "grilles_p", grilles_p
        
        
        # Détection d'anomalie
        for p in grilles_p:
            for lig in p:
                if None in lig:
                    err |= 1
                    break
            else:
                continue
            break
        
        
        # Rectangles des sequences_projets
        rect = [[None,None,0,0] for i in self.sequences_projets] # Rectangles en mode "lignes/colonnes"
        l_per = []                                               # Lignes marquant les débuts des périodes
        l = 0
        for p in grilles_p:
            l_per.append(l) 
            for lig in p:
               
                for c, sp in enumerate(lig):
                    if sp is not None:
                        if rect[sp][0] is None:      # X
                            rect[sp][0] = c
                        if rect[sp][1] is None:      # Y
                            rect[sp][1] = l
                        rect[sp][2] = c - rect[sp][0] + 1
                        rect[sp][3] = l - rect[sp][1] + 1
                l += 1
            
#         print "rect", rect
        
        
        # Détection d'anomalie : croisement
        gr = [[0 for cc in range(nc)] for ll in range(l)]
        for r in rect:
            for lg in range(r[1], r[1]+r[3]):
                for cl in range(r[0], r[0]+r[2]):
                    gr[lg][cl] += 1
                    if gr[lg][cl] > 1:
                        err |= 2
                        break
                else:
                    continue
                break
            else:
                continue
            break
                
            
            
            
        
        # Calcul des positions "horaire" des lignes
        h_lig = [0]*(l+1)                                   # Positions en "y" des lignes
        for sp, r in enumerate(rect):
            h = self.sequences_projets[sp].GetDuree() / r[2] * nc
            suiv = r[1] + r[3]
            m = max(h_lig[r[1]]+h, h_lig[suiv])     # Position suivante
            for i in range(suiv, len(h_lig)-1):     # On "repousse" les lignes suivantes
                h_lig[i] = m
            h_lig[-1] = max(m, h_lig[-1])

#         print "h_lig", h_lig
            
        # Détection d'anomalie
        l = 0
        h_per = [h_lig[l] for l in l_per]+[h_lig[-1]]
        d_per = [h-h_per[i] for i, h in enumerate(h_per[1:])]
        m = mean(d_per)
        if m > 0:
#             print d_per, " >> ", pstdev(d_per) / m
            if pstdev(d_per) / m > 0.5:
                err |= 4
            
        
        
        return rect, l_per, h_lig, err
        
        
    ######################################################################################  
    def Analyser(self):
        """ Analyse la cohérence de la répartition des Séquences et des Projets
            Renvoie une liste de messages d'erreur
        """
        messages = {0 : "Aucune anomalie détectée.",
                    1 : "Certains créneaux horaire ne sont pas utilisés.",
                    2 : "Certains Séquences ou Projets se chevauchent.",
                    4 : "Important déséquilibre dans la répartition des durées par période."}
        
        
        err = self.GetRectangles()[-1]
        
        return [m for e, m in messages.items() if e & err]
    
    
    
    ######################################################################################  
    def GetDuree(self):
        """ Renvoie la durée totale des Séquence et des Projets de la Progression
        """
        return sum([sp.GetDoc().GetDuree() for sp in self.sequences_projets if sp.GetDoc() is not None])

#     ######################################################################################  
#     def GetCompetencesAbordees(self):
#         """ Renvoie un bilan des compétences abordées dans les Séquence et les Projets de la Progression
#             sous la forme {CodeGroupe : [Liste de True/False], ...}
#             sur la base de ref._listesCompetences_simple["S"]
#         """
# #         print "GetCompetencesAbordees"
#         ref = self.GetReferentiel()
#         competences = ref._listesCompetences_simple["S"]
#         dicComp = {}
#         
# #         print [sp.GetDoc().GetCompetencesVisees() for sp in self.sequences_projets]
#         for i, g1 in enumerate(competences):
#             k1, h1, l1 = g1
#             l = []
#             
#             for k2, h2 in l1:
#                 
#                 l.append(any(["S" + k2 in sp.GetDoc().GetCompetencesVisees() for sp in self.sequences_projets]))
#             dicComp[k1] = l
#             
# #         print dicComp
#         return dicComp

    ######################################################################################  
    def GetCompetencesAbordees(self):
        """ Renvoie un bilan des compétences abordées dans les Séquence et les Projets de la Progression
            sous la forme d'une liste de tuples (code, nombre d'occurences)
            
        """
#         print "GetCompetencesAbordees"
        lstComp = []
        for sp in self.sequences_projets:
            doc = sp.GetDoc()
            if doc is not None:
                lstComp.extend(doc.GetCompetencesVisees())
 
        l = [(k, lstComp.count(k)) for k in lstComp]
        if l != []:
            l, c = list(zip(*list(set(l))))
            return l, c
        else:
            return [], []
        
    ######################################################################################  
    def GetSavoirsAbordes(self):
        """ Renvoie un bilan des Savoirs abordés dans les Séquence et les Projets de la Progression
            sous la forme d'une liste de tuples (code, nombre d'occurences)
            
        """
#         print "GetSavoirsAbordes"
        lstSav = []
        for sp in self.sequences_projets:
            doc = sp.GetDoc()
            if doc is not None:
                lstSav.extend(doc.GetSavoirsVises())
 
        l = [(k, lstSav.count(k)) for k in lstSav]
        if l != []:
            l, c = list(zip(*list(set(l))))
            return l, c
        else:
            return [], []
                

    ######################################################################################  
    def GetOrganisation(self):
        """ Renvoie une structure organisé des Séquences et Projets
            une liste de colones, avec des Séquences/Projets
            Minimisation du nombre de colonnes ?
        """
#         print "GetOrganisation"
        orga = []
        liste = self.GetAllSequencesProjets()
#         print "   ", liste
        
        liste.sort(key = lambda s:s.GetPosition()[-1]-s.GetPosition()[0], reverse = True)
        liste.sort(key = lambda s:s.GetPosition()[0])
#         print " >>", liste
        
#         for d in liste()
        
        
        return orga



    ######################################################################################  
    def GetAllSequencesProjets(self):
        return self.sequences_projets[:] + list(self.GetReferentiel().projets.values())
    
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Progression(parent, self)


    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, Titres[12], data = self, image = self.arbre.images["Prg"])
        
        #
        # Les profs
        #
        self.branchePrf = arbre.AppendItem(self.branche, Titres[10], data = "Equ")
        for e in self.equipe:
            e.ConstruireArbre(arbre, self.branchePrf) 
        
        #
        # Les séquences
        #
        self.brancheSeq = arbre.AppendItem(self.branche, Titres[11], data = "Seq")
        for e in self.sequences_projets:
            e.ConstruireArbre(arbre, self.brancheSeq) 

            
        
    ######################################################################################  
    def DefinirCouleurs(self):
        draw_cairo.DefinirCouleurs(self.GetNbrPeriodes(),
                                   len(self.GetReferentiel()._listesCompetences_simple["S"]),
                                   len(self.GetListeCI()))
        

    ######################################################################################  
    def Rafraichir(self, event = None):
#         print "Rafraichir progression"
        self.Ordonner()
        self.arbre.DeleteChildren(self.brancheSeq)
        
        for e in self.sequences_projets:
            e.ConstruireArbre(self.arbre, self.brancheSeq)
            
        self.arbre.ExpandAll()
        
        self.DefinirCouleurs()
        
        self.VerifPb()
        
        if self.arbre.GetSelection() is None:
            self.arbre.SelectItem(self.branche)


    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la séquence pour enregistrement
        """
#        print "getBranche progression"
        # Création de la racine
        progression = ET.Element("Progression")
        
        progression.set("Intitule", self.intitule)
        
        progression.set("NbrCreneaux", str(self.nbrCreneaux))
        
        self.lien.getBranche(progression)
        
        self.getBrancheImage(progression)

        if self.commentaires != "":
            progression.set("Commentaires", self.commentaires)
        
        progression.set("Mode", self.mode)
        
        equipe = ET.SubElement(progression, "Equipe")
        for p in self.equipe:
            equipe.append(p.getBranche())
            
        eleves = ET.SubElement(progression, "Eleves")
        for e in self.eleves:
            eleves.append(e.getBranche())
#        
        sequences_projets = ET.SubElement(progression, "Sequences_Projets")
        for lienseq in self.sequences_projets:
            sequences_projets.append(lienseq.getBranche())
            
            
        calendrier = ET.SubElement(progression, "Calendrier")
        calendrier.append(self.calendrier.getBranche())
        
        return progression


    ######################################################################################  
    def setBranche(self, branche):
        """ Lecture d'une branche XML de progression
        """
#        print "setBranche progression"
#        t0 = time.time()
        err = []
        
        self.intitule = branche.get("Intitule", "")
        
        self.nbrCreneaux = int(branche.get("NbrCreneaux", str(constantes.NBR_CRENEAUX_DEFAUT)))
        
        self.lien.setBranche(branche, self.GetPath())
        
        self.commentaires = branche.get("Commentaires", "")
        
        self.mode = branche.get("Mode", "C")
        
        Ok = self.setBrancheImage(branche)
                
        brancheEqu = branche.find("Equipe")
        self.equipe = []
        if brancheEqu is not None:
            for e in list(brancheEqu):
                prof = Prof(self)
                Ok = prof.setBranche(e)
                if not Ok : 
                    err.append(constantes.Erreur(constantes.ERR_PRJ_EQUIPE))
                self.equipe.append(prof)
        
        brancheEle = branche.find("Eleves")
        self.eleves = []
        if brancheEle is not None:
            for e in list(brancheEle):
                eleve = Eleve(self)
                Ok = eleve.setBranche(e)
                if not Ok : 
                    err.append(constantes.Erreur(constantes.ERR_PRJ_ELEVES))
                
                self.eleves.append(eleve)
            
#        brancheDossier = branche.find("Dossier")
#        self.dossier.setBranche(brancheDossier)
        
        
        self.sequences_projets = []
        # Provisoire ... pendant développement
        brancheSeq = branche.find("Sequences")
        if brancheSeq is not None:
            for f in list(brancheSeq):
                sp = LienSequence(self)
                sp.setBranche(f)
                self.sequences_projets.append(sp)
            
        # Provisoire ... pendant développement
        branchePrj = branche.find("Projets")
        if branchePrj is not None:
            for f in list(branchePrj):
                sp = LienProjet(self)
                sp.setBranche(f)
                self.sequences_projets.append(sp)
                
        # Solution définitive
        branchePrj = branche.find("Sequences_Projets")
        if branchePrj is not None:
            for f in list(branchePrj):
                if f.tag == "Projet":
                    sp = LienProjet(self)
                else: # Sequence !
                    sp = LienSequence(self)
                sp.setBranche(f)
                self.sequences_projets.append(sp)
                
                
                
        brancheCal = branche.find("Calendrier")
        if brancheCal is not None:
            for c in list(brancheCal):
                self.calendrier.setBranche(c)


        return err
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):    
        """ Affiche le menu contextuel associé à la progression
            ... ou bien celui de itemArbre concerné ...
        """
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([["Enregistrer", self.app.commandeEnregistrer,
                                              getIconeFileSave()],
#                                             [u"Ouvrir", self.app.commandeOuvrir],
                                             ["Exporter la fiche (PDF ou SVG)", self.app.exporterFiche, None],
                                            ])
            
#        [u"Séquence pédagogique",
#          u"Prérequis",
#          u"Objectifs pédagogiques",
#          u"Séances",
#          u"Systèmes"]
        
#        elif isinstance(self.arbre.GetItemPyData(itemArbre), Competences):
#            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Prof):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), LienSequence):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), LienProjet):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)           
                             
        elif self.arbre.GetItemText(itemArbre) == Titres[10]: # Prof
            self.app.AfficherMenuContextuel([["Ajouter un professeur", self.AjouterProf, 
                                              scaleImage(images.Icone_ajout_prof.GetBitmap())]])
            
        elif self.arbre.GetItemText(itemArbre) == Titres[11]: # Séquence
            lst = [["Créer une nouvelle Séquence", 
                    self.AjouterNouvelleSequence, 
                    scaleImage(images.Icone_ajout_seq.GetBitmap())],
                   ["Importer une Séquence existante", 
                     self.AjouterSequence, 
                     scaleImage(images.Icone_import_seq.GetBitmap())],
                   ["Importer toutes les Séquences compatibles du dossier", 
                     self.ImporterSequences, 
                     scaleImage(images.Icone_cherch_seq.GetBitmap())],]
            
            coderef = self.GetReferentiel().Code
            if len(REFERENTIELS[coderef].projets) > 0:
                lst.extend([["Créer un nouveau Projet", 
                             self.AjouterNouveauProjet, 
                             scaleImage(images.Icone_ajout_prj.GetBitmap())],
                            ["Importer un Projet existant", 
                              self.AjouterProjet, 
                              scaleImage(images.Icone_import_prj.GetBitmap())],
                            ["Importer tous les Projets compatibles du dossier", 
                              self.ImporterProjets, 
                              scaleImage(images.Icone_cherch_prj.GetBitmap())]])

                                            
            self.app.AfficherMenuContextuel(lst)


    ######################################################################################  
    def SupprimerItem(self, item):
        self.SupprimerLien(item = item)
    
    ######################################################################################  
    def SupprimerLien(self, event = None, item = None, lien = None, sendEvent = True):
        if lien is None:
            l = self.arbre.GetItemPyData(item)
        else:
            l = lien

        self.sequences_projets.remove(l)
        
        if item is not None:
            self.arbre.Delete(item)
        
        if sendEvent:
            if isinstance(item, LienSequence):
                self.GetApp().sendEvent(modif = "Suppression d'une Séquence")
            else:
                self.GetApp().sendEvent(modif = "Suppression d'un Projet")
        

    ######################################################################################  
    def OuvrirSequence(self, event = None, item = None):
        l = self.arbre.GetItemPyData(item)
        nomFichier = os.path.join(self.GetPath(), l.path)
#        self.GetApp().parent.ouvrir(toSystemEncoding(l.path))
        l.sequence = self.GetApp().parent.ouvrirDoc(l.sequence, nomFichier)
        
    
    ######################################################################################  
    def OuvrirProjet(self, event = None, item = None):
        l = self.arbre.GetItemPyData(item) # lienProjet de la Progression
        nomFichier = os.path.join(self.GetPath(), l.path)
#        self.GetApp().parent.ouvrir(toSystemEncoding(l.path))
        l.projet = self.GetApp().parent.ouvrirDoc(l.projet, nomFichier)
#         l.projet.app = app.GetApp()

    ######################################################################################  
    def ChargerSequences(self, parent, reparer = False):
#         print("ChargerSequences", self.sequences_projets)
        aSupprimer = []
        for lienSeq in [s for s in self.sequences_projets if isinstance(s, LienSequence)]:
            if lienSeq.sequence is None:
#                print "   ", lienSeq.path
                path = os.path.join(self.GetPath(), lienSeq.path)
#                 print("   ", path)
                if not os.path.isfile(path):
                    dlg = wx.MessageDialog(parent, "Le fichier Séquence suivant n'a pas été trouvé.\n\n"\
                                                 "\t%s\n\n"
                                                 "Voulez-vous le chercher manuellement ?\n" %toSystemEncoding(lienSeq.path),
                                           "Fichier non trouvé",
                                           wx.YES_NO | wx.ICON_QUESTION |wx.YES_DEFAULT
                                           )
                    res = dlg.ShowModal()
                    dlg.Destroy()
                    if res == wx.ID_YES:
                        
                        fichiers_sequences = self.GetFichiersSequencesDossier(exclureExistant = True)
                        if len(fichiers_sequences) > 0:
                            fichiers, sequences = list(zip(*fichiers_sequences))
                            fichiers = [testRel(f, self.GetPath()) for f in fichiers]
                            dlg = wx.SingleChoiceDialog(parent, "Choisir parmi les fichiers ci-dessous\n"\
                                                                       "celui qui doit remplacer %s." %toSystemEncoding(lienSeq.path), 
                                                        "Fichiers Séquences disponibles",
                                                        [toSystemEncoding(f) for f in fichiers], 
                                                        wx.CHOICEDLG_STYLE
                                                        )
                            
                            if dlg.ShowModal() == wx.ID_OK:
                                i = dlg.GetSelection() 
                                lienSeq.path = fichiers[i]
                                lienSeq.sequence = sequences[i]
                                self.GetApp().MarquerFichierCourantModifie()
    
                            else:
                                aSupprimer.append(lienSeq)
                                
                            dlg.Destroy()
                        
                        else:
                            aSupprimer.append(lienSeq)
                        
                    elif res == wx.ID_NO:
                        aSupprimer.append(lienSeq)
                        continue
                else: 
                    lienSeq.ChargerSequence(reparer = reparer)
        
        #
        # On supprime les lienSequences à supprimer
        #
        for s in aSupprimer:
            self.SupprimerLien(lien = s, sendEvent = False)
            
        

    
    ######################################################################################  
    def ChargerProjets(self, parent, reparer = False):
#        print "ChargerProjets", self.sequences_projets
        aSupprimer = []
        for lienPrj in [s for s in self.sequences_projets if isinstance(s, LienProjet)]:
            if lienPrj.projet is None:
#                print "   ", lienSeq.path
                path = os.path.join(self.GetPath(), lienPrj.path)
#                print "   ", path
                if not os.path.isfile(path):
                    dlg = wx.MessageDialog(parent, "Le fichier Projet suivant n'a pas été trouvé.\n\n"\
                                                 "\t%s\n\n"
                                                 "Voulez-vous le chercher manuellement ?\n" %toSystemEncoding(lienPrj.path),
                                           "Fichier non trouvé",
                                           wx.YES_NO | wx.ICON_QUESTION |wx.YES_DEFAULT
                                           )
                    res = dlg.ShowModal()
                    dlg.Destroy()
                    if res == wx.ID_YES:
                        fichiers_projets = self.GetFichiersProjetsDossier(exclureExistant = True)
                        fichiers, projets = list(zip(*fichiers_projets))
                        fichiers = [testRel(f, self.GetPath()) for f in fichiers]
                        
                        dlg = wx.SingleChoiceDialog(parent, "Choisir parmi les fichiers ci-dessous\n"\
                                                                   "celui qui doit remplacer %s." %toSystemEncoding(lienPrj.path), 
                                                    "Fichiers Projet disponibles",
                                                    [toSystemEncoding(f) for f in fichiers], 
                                                    wx.CHOICEDLG_STYLE
                                                    )
                        
                        if dlg.ShowModal() == wx.ID_OK:
                            i = dlg.GetSelection() 
                            lienPrj.path = fichiers[i]
                            lienPrj.projet = projets[i]
                            self.GetApp().MarquerFichierCourantModifie()

                        else:
                            aSupprimer.append(lienPrj)
                            
                        dlg.Destroy()
                    
                    elif res == wx.ID_NO:
                        aSupprimer.append(lienPrj)
                        continue
                else: 
                    lienPrj.ChargerProjet(reparer = reparer)
        
        #
        # On supprime les lienProjet à supprimer
        #
        for s in aSupprimer:
            self.SupprimerLien(lien = s, sendEvent = False)
            
        
        
        
    ######################################################################################  
    def Ordonner(self):
#         print "Ordonner"
    

                
#         print "  ", listeSeqPrj
        self.sequences_projets.sort()#key= lambda s : s.GetDoc().position)
        
        self.brancheSeq.DeleteChildren(self.arbre)
        for r, e in enumerate(self.sequences_projets):
            e.rang = 2*r
            e.ConstruireArbre(self.arbre, self.brancheSeq) 
            
        self.VerifPb()

    

    ######################################################################################  
    def DossierDefini(self):
        dossier = self.GetPath()
        if dossier == r"":
            messageInfo(None, "Progression non enregistrée", 
                                  "La progression %s n'a pas encore été enregistrée.\n\n"\
                                  "L'importation est prévue pour rechercher des fichiers \"Séquence\" (.seq)\n" \
                                  "dans le même dossier que le fichier \"Progression\" (.prg)." %self.intitule)
            return False
        return True


    ######################################################################################  
    def AjouterNouvelleSequence(self, event = None):
        if not self.DossierDefini():
            return
        
        sequence, path = self.CreerSequence(self.classe, self.GetPath())
        if path is not None:
            ps = LienSequence(self)
            ps.path = toFileEncoding(path)
            if sequence is not None:
                ps.sequence = sequence
                sequence.SetText(os.path.splitext(os.path.basename(path))[0])
            else:
                ps.ChargerSequence()
            self.sequences_projets.append(ps)
            self.Ordonner()
            self.GetApp().sendEvent(modif = "Ajout d'une nouvelle Séquence à la Progression")
            self.arbre.SelectItem(ps.branche)


    ######################################################################################  
    def AjouterNouveauProjet(self, event = None):
        if not self.DossierDefini():
            return
        
        projet, path = self.CreerProjet(self.classe, self.GetPath())
        if path is not None:
            ps = LienProjet(self)
            ps.path = toFileEncoding(path)
            if projet is not None:
                ps.projet = projet
                projet.SetText(os.path.splitext(os.path.basename(path))[0])
            else:
                ps.ChargerProjet()
            self.sequences_projets.append(ps)
            self.Ordonner()
            self.GetApp().sendEvent(modif = "Ajout d'un nouveau Projet à la Progression")
            self.arbre.SelectItem(ps.branche)
            
    ######################################################################################  
    def AjouterSequence(self, event = None):
        """ Ajoute une Séquence
            parmi une liste de Séquences compatibles recherchées dans le dossier de la progression
        """
        if not self.DossierDefini():
            return
        
        fichiers_sequences = self.GetFichiersSequencesDossier(exclureExistant = True)
        if len(fichiers_sequences) == 0:
            messageInfo(None, "Aucune Séquence trouvée", 
                        "Aucune Séquence compatible à la progression n'a été trouvée.\n\n")
            return
        
        fichiers, sequences = list(zip(*fichiers_sequences))
        fichiers = [testRel(f, self.GetPath()) for f in fichiers]
        
        dlg = wx.SingleChoiceDialog(self.GetApp(), "Choisir parmi les fichiers ci-dessous\n", 
                                    "Fichiers Séquences disponibles",
                                    [toSystemEncoding(f) for f in fichiers], 
                                    wx.CHOICEDLG_STYLE
                                    )
        
        if dlg.ShowModal() == wx.ID_OK:
            i = dlg.GetSelection() 
            lienSeq = LienSequence(self)
            lienSeq.path = fichiers[i]
            lienSeq.sequence = sequences[i]
            self.sequences_projets.append(lienSeq)
            self.Ordonner()
            self.GetApp().sendEvent(modif = "Ajout d'une Séquence à la Progression")
            self.arbre.SelectItem(lienSeq.branche)
        
        dlg.Destroy()
        
    ######################################################################################  
    def AjouterProjet(self, event = None):
        if not self.DossierDefini():
            return
        
        fichiers_projets = self.GetFichiersProjetsDossier(exclureExistant = True)
        if len(fichiers_projets) == 0:
            messageInfo(None, "Aucun Projet trouvé", 
                        "Aucun Projet compatible à la progression n'a été trouvé.\n\n")
            return
        
        fichiers, projets = list(zip(*fichiers_projets))
        fichiers = [testRel(f, self.GetPath()) for f in fichiers]
        
        dlg = wx.SingleChoiceDialog(self.GetApp(), "Choisir parmi les fichiers ci-dessous\n", 
                                    "Fichiers Projets disponibles",
                                    [toSystemEncoding(f) for f in fichiers], 
                                    wx.CHOICEDLG_STYLE
                                    )
        
        if dlg.ShowModal() == wx.ID_OK:
            i = dlg.GetSelection() 
            lienPrj = LienProjet(self)
            lienPrj.path = fichiers[i]
            lienPrj.projet = projets[i]
            self.sequences_projets.append(lienPrj)
            self.Ordonner()
            self.GetApp().sendEvent(modif = "Ajout d'un Projet à la Progression")
            self.arbre.SelectItem(lienPrj.branche)
        
        dlg.Destroy()

 
    ######################################################################################  
    def CreerSequence(self, classe, pathProg):
        """ Créé une (nouvelle) Séquence pour la progression
            renvoie : un tuple Sequence, chemin du fichier de Séquence
        """
        sequence = Sequence(self.GetApp(), classe)
        res = self.GetApp().ProposerEnregistrer(sequence, pathProg)
        
        if res[0] == 2:     # Fichier existant --> on redemande
            return self.CreerSequence(classe, pathProg)
        elif res[0] == 1:   # Fichier existant --> fichier Séquence à ouvrir
            return None, res[1]
        elif res[0] == 0:   # Nouveau fichier --> nouvelle Séquence à enregistrer
            return sequence, res[1]
        else:
            return None, None
        
        
    ######################################################################################  
    def CreerProjet(self, classe, pathProg):
        projet = Projet(self.GetApp(), classe)
        res = self.GetApp().ProposerEnregistrer(projet, pathProg)
        
        if res[0] == 2:
            return self.CreerProjet(classe, pathProg)
        elif res[0] == 1:
            return None, res[1]
        elif res[0] == 0:
            return projet, res[1]
        else:
            return None, None
    
        
    ######################################################################################  
    def ImporterSequences(self, event = None):
        """ Importe automatiquement toutes les Séquences compatibles du dossier
        """
        if not self.DossierDefini():
            return
        
        sequences = self.GetSequencesDossier()
#         print "sequences trouvées", sequences
        for s in sequences:
            if not s in self.sequences_projets:
                self.sequences_projets.append(s)
#                s.ConstruireArbre(self.arbre, self.brancheSeq)
#         print "sequences importées", self.sequences_projets
        self.Ordonner()
        self.GetApp().sendEvent(modif = "Import des Séquences compatibles") 
        

    ######################################################################################  
    def ImporterProjets(self, event = None):
        """ Importe automatiquement touts les Projets compatibles du dossier
        """
        if not self.DossierDefini():
            return
        
        projets = self.GetProjetsDossier()
        for s in projets:
            if not s in self.sequences_projets:
                self.sequences_projets.append(s)
#                s.ConstruireArbre(self.arbre, self.brancheSeq)
        self.Ordonner()
        
        self.GetApp().sendEvent(modif = "Import des Projets compatibles") 


    ######################################################################################  
    def VerifPb(self):
        """ Vérification d'éventuelles problèmes et anomalies dans la Progression :
             - conflits de Prérequis de séquence (en termes de Savoirs)
             - anomalies de répartition des Séquences et Projets
        """
        obj = []
        for lienseq in [s for s in self.sequences_projets if isinstance(s, LienSequence)]:
            pb = []
            seq = lienseq.sequence
            prerequis = seq.prerequis["S"].savoirs
            
#             objectifs = seq.obj['S'].savoirs
            objectifs = seq.GetSavoirsVises()
            
            for p in prerequis:
                if not p in obj:
                    pb.append(p)
            lienseq.SignalerPb(pb)
            obj.extend(objectifs)


        self.SignalerPb(self.Analyser())
        
        
    ######################################################################################  
    def SignalerPb(self, pb):
        """
        """
        if hasattr(self, 'brancheSeq'):
            bg_color = self.arbre.GetBackgroundColour()
            if len(pb) == 0:
                self.arbre.SetItemBackgroundColour(self.brancheSeq, bg_color)
                self.SetToolTip(self.intitule)
            else:
                self.arbre.SetItemBackgroundColour(self.brancheSeq, wx.Colour("LIGHT PINK"))
                message = "La répartition des Séquences et des Projets pendant l'année\n" \
                          "présente des anomalies :\n"
                self.SetToolTip(message + "\n".join([" - "+p for p in pb]))
  
  
  
    ########################################################################################################
    def OuvrirFichierSeq(self, nomFichier, reparer = False):
#        print "///", nomFichier
        nomFichier = os.path.join(self.GetPath(), nomFichier)
#        path2 = os.path.normpath(os.path.abspath(toSystemEncoding(nomFichier)))
        for seq in self.GetApp().parent.GetDocumentsOuverts('seq'):
#            print "   :", seq[1]
#            path1 = os.path.normpath(os.path.abspath(seq[1]))
            path1 = os.path.join(self.GetPath(), seq[1])
            if path1 == nomFichier:  # La séquence est déja ouverte
                sequence = seq[0]
                classe = sequence.classe
                return classe, sequence
        
#        print "///", nomFichier
        root = safeParse(nomFichier, None)
        if root is None:
            return None,  None
        
        classe = Classe(self.GetApp())
        sequence = Sequence(self.GetApp(), classe, ouverture = True)
        classe.SetDocument(sequence)

        try:
        
            rsequence = root.find("Sequence")
            rclasse = root.find("Classe")
            if rclasse is not None:
                classe.setBranche(rclasse, reparer = reparer)
            if rsequence is not None:
                sequence.setBranche(rsequence)
            else:   # Ancienne version , forcément STI2D-ETT !!
                classe.typeEnseignement, self.classe.familleEnseignement = ('ET', 'STI')
                classe.referentiel = REFERENTIELS[classe.typeEnseignement]
                sequence.setBranche(root)
            return classe, sequence
        except:
#             print("Le fichier n'a pas pu être ouvert :", nomFichier)
            if DEBUG:
                raise
            return None, None
    
    
    ########################################################################################################
    def OuvrirFichierPrj(self, nomFichier, reparer = False):
#        print "///", nomFichier
        nomFichier = os.path.join(self.GetPath(), nomFichier)
        for prj in self.GetApp().parent.GetDocumentsOuverts('prj'):
#            print "   :", seq[1]
#            path1 = os.path.normpath(os.path.abspath(seq[1]))
            path1 = os.path.join(self.GetPath(), prj[1])
            if path1 == nomFichier:  # La séquence est déja ouverte
                projet = prj[0]
                classe = projet.classe
                return classe, projet

        root = safeParse(nomFichier, None)
        if root is None:
            return None,  None
        
        classe = Classe(self.GetApp())
        projet = Projet(self.GetApp(), classe, ouverture = True)
        classe.SetDocument(projet)

        try:
            rprojet = root.find("Projet")
            rclasse = root.find("Classe")
            if rclasse is not None:
                classe.setBranche(rclasse, reparer = reparer)
            if rprojet is not None:
                projet.setBranche(rprojet)
            else:   # Ancienne version (?), forcément STI2D-ETT !!
                classe.typeEnseignement, self.classe.familleEnseignement = ('ET', 'STI')
                classe.referentiel = REFERENTIELS[classe.typeEnseignement]
                projet.setBranche(root)
            return classe, projet
        except:
            print("Le fichier n'a pas pu être ouvert :",nomFichier)
            if DEBUG:
                raise
            return None, None



    #############################################################################
    def MiseAJourTypeEnseignement(self, ancienRef = None, ancienneFam = None):#, changeFamille = False):
#        print "MiseAJourTypeEnseignement Progression"
#        print self.GetReferentiel()._listesCompetences_simple["S"]
        self.app.SetTitre()
        self.classe.MiseAJourTypeEnseignement()
#         self.calendrier.MiseAJourTypeEnseignement()
        draw_cairo.DefinirCouleurs(self.GetNbrPeriodes(),
                                   len(self.GetReferentiel()._listesCompetences_simple["S"]),
                                   len(self.GetReferentiel().CentresInterets))
        
#        self.code = self.GetReferentiel().getCodeProjetDefaut()

        
    #############################################################################
    def Verrouiller(self):
        self.classe.Verrouiller(len(self.sequences_projets) != 0)
        
    
    
    ########################################################################################################
    def GetCreneaux(self):
        """ Renvoie la liste des tous les créneaux utilisés
        """
        c = []
        for e in self.sequences_projets:
            c.extend(e.GetCrenaux())
            
        return sorted(list(set(c)))
    
    
    ########################################################################################################
    def GetListeCI(self):
        """ Renvoie la liste des CI du référentiel
            + ceux définis dans les Séquences de la Progresion
        """
        lst = []
        for e in self.sequences_projets:
            if isinstance(e, LienSequence) and e.sequence is not None:
                lst.extend(e.sequence.CI.CI_perso)
#         print(lst)
        lst = list(set(lst))
        return self.GetReferentiel().CentresInterets + lst
    
    
    ########################################################################################################
    def GetListeTh(self):
        """ Renvoie la liste des thématiques du référentiel
            + ceux définis dans les Séquences de la Progresion
        """
        return []#self.GetReferentiel().listeThematiques
    
    
    ########################################################################################################
    def GetListeFichiersSequences(self):
        """
        """
        return [l.path for l in self.sequences_projets]


    ########################################################################################################
    def GetSequencesDossier(self, event = None):
        sequences = []
        listeFichiersSequences = self.GetFichiersSequencesDossier()
        for fichier, sequence in listeFichiersSequences:
#             print 
#             print fichier
            path = testRel(fichier, self.GetPath())
#             print path
#             path = os.path.join(path, os.path.split(fichier)[1])
#             print path
            lienSequence = LienSequence(self,  path)
#             print "seq", self.GetPath(), fichier
#             print "   ", testRel(self.GetPath(), fichier)
            lienSequence.sequence = sequence
            sequences.append(lienSequence)
        
        
        
        return sequences


    ########################################################################################################
    def GetProjetsDossier(self, event = None):
        projets = []
        listeFichiersProjets = self.GetFichiersProjetsDossier()
        for fichier, projet in listeFichiersProjets:
#             print 
#             print fichier
            path = testRel(fichier, self.GetPath())
#             print path
#             path = os.path.join(path, os.path.split(fichier)[1])
#             print path
            lienSequence = LienSequence(self,  path)
#             print "seq", self.GetPath(), fichier
#             print "   ", testRel(self.GetPath(), fichier)
            lienSequence.sequence = projet
            projets.append(lienSequence)
        
        
        
        return projets

    ########################################################################################################
    def GetFichiersSequencesDossier(self, event = None, exclureExistant = False):    
        """ Recherche tous les fichiers Séquence compatibles avec la progression
        
        >> Renvoie une liste [(nomFichier, Sequence)]
        """   
#         print("GetSequencesDossier", self.GetPath())
        wx.BeginBusyCursor()
        
        #
        # On cherche tous les fichiers .seq
        #
        l = []
        if True:
            for root, dirs, files in os.walk(self.GetPath()):
                l.extend([os.path.join(root, f) for f in files if os.path.splitext(f)[1] == '.seq'])
        else:
            l.extend(glob.glob(os.path.join(self.GetPath(), "*.seq")))
#         print("   ", l)
        #
        # Un ProgressDialog pour patienter ...
        #
        dlg =    wx.ProgressDialog("Recherche des séquences",
                                   "",
                                   maximum = len(l),
                                   parent=self.GetApp(),
                                   style = 0
                                    | wx.PD_APP_MODAL
                                    | wx.PD_ESTIMATED_TIME
                                    | wx.PD_REMAINING_TIME
                                    | wx.PD_AUTO_HIDE
                                    )
        #
        # On enlève les fichiers qui sont déja dans la liste des fichiers Sequence de la progression
        #
        if exclureExistant:
            lf = [os.path.abspath(ls.path) for ls in self.sequences_projets] # Existant
            l = [ls for ls in l if not ls in lf]
        
#         print("   ", l)
        #
        # On ouvre tous les fichiers .seq pour vérifier leur compatibilité
        #
        fichiers_sequences = []
        count = 0
        for f in l:
            dlg.Update(count, toSystemEncoding(f))
      
            classe, sequence = self.OuvrirFichierSeq(f)
#                print classe.typeEnseignement ,  self.referentiel.Code
            if classe != None and classe.typeEnseignement == self.GetReferentiel().Code:
#                lienSequence = LienSequence(self,  testRel(f, self.GetPath()))
#                lienSequence.sequence = sequence
                fichiers_sequences.append((f, sequence))
            count += 1

        dlg.Update(count, "Terminé")
        dlg.Destroy()
        wx.EndBusyCursor()
        
        return fichiers_sequences



    ########################################################################################################
    def GetFichiersProjetsDossier(self, event = None, exclureExistant = False):    
        """ Recherche tous les fichiers Projet compatibles avec la progression
        
            :return: Une liste [(nomFichier, Projet)]
            :rtype: list
        """   
#        print "GetSequencesDossier"
        wx.BeginBusyCursor()
        
        #
        # On cherche tous les fichiers .seq
        #
        l = []
        if True:
            for root, dirs, files in os.walk(self.GetPath()):
                l.extend([os.path.join(root, f) for f in files if os.path.splitext(f)[1] == '.prj'])
        else:
            l.extend(glob.glob(os.path.join(self.GetPath(), "*.prj")))
            
        #
        # Un ProgressDialog pour patienter ...
        #
        dlg =    wx.ProgressDialog("Recherche des Projets",
                                   "",
                                   maximum = len(l),
                                   parent=self.GetApp(),
                                   style = 0
                                    | wx.PD_APP_MODAL
                                    | wx.PD_ESTIMATED_TIME
                                    | wx.PD_REMAINING_TIME
                                    | wx.PD_AUTO_HIDE
                                    )
        #
        # On enlève les fichiers qui sont déja dans la liste des fichiers Projet de la progression
        #
        if exclureExistant:
            lf = [os.path.abspath(ls.path) for ls in self.sequences_projets] # Existant
            l = [ls for ls in l if not ls in lf]
            
        #
        # On ouvre tous les fichiers .prj pour vérifier leur compatibilité
        #
        fichiers_projets = []
        count = 0
        for f in l:
            dlg.Update(count, toSystemEncoding(f))
      
            classe, projet = self.OuvrirFichierPrj(f)

            if classe != None and classe.typeEnseignement == self.GetReferentiel().Code:
                fichiers_projets.append((f, projet))
            count += 1

        dlg.Update(count, "Terminé")
        dlg.Destroy()
        wx.EndBusyCursor()
        
        return fichiers_projets



#    ######################################################################################  
#    def GetFicheHTML(self, param = None):
#        if param is None:
#            return constantes.BASE_FICHE_HTML
#        else:
#            if param == "CAL":
#                return constantes.BASE_FICHE_HTML_CALENDRIER
#                
#            elif param == "ANN":
#                pass
#                
#            elif param[:3] == "POS":
#                return constantes.BASE_FICHE_HTML_PERIODES
#                
#            elif param[:3] == "EQU":
#                pass
#            
#            elif param[:2] == "CI":
#                return constantes.BASE_FICHE_HTML_CI
#                
#            else:
#                pass
#            
#        return constantes.BASE_FICHE_HTML

    ######################################################################################  
    def SetTip(self, param = None, obj = None):
        """ Mise à jour du TIP (popup)
        """
        
        if param is None:   # la Progression elle-même
            self.tip.SetHTML(constantes.encap_HTML(constantes.BASE_FICHE_HTML))
            
        
        else:               # Un autre élément de la Progression
            self.tip.SetHTML(self.GetFicheHTML(param = param))
            if param == "CAL":
                self.tip.SetWholeText("titre", "Calendrier de la Progression")
                self.tip.AjouterImg("img", self.getBitmapCalendrier(1000))
                
            elif param == "ANN":
                self.tip.SetWholeText("titre", "Années scolaires de la Progression")
                self.tip.SetWholeText("txt", self.GetAnnees())
                self.tip.Supprime('img')
                
            elif param == "POS":
                self.Tip_POS() 
                
            elif param[:3] == "POS":
                self.Tip_POS(int(param[3])) 
                            
            elif param[:3] == "EQU":
                self.Tip_EQU("la Progression")
                
            
            elif param[:2] == "CI":
                ref = self.GetReferentiel()
                self.tip.SetWholeText("titre", ref._nomCI.Sing_())  
                numCI = int(param[2:])
                code = ref.abrevCI+str(numCI+1)
#                 intit = ref.CentresInterets[numCI]
             
                self.tip.AjouterElemListeDL("ci", code, 
                                            self.GetListeCI()[numCI])
                if len(ref.listProblematiques) > numCI and len(ref.listProblematiques[numCI]) > 0:
                    self.tip.SetWholeText("nomPb", ref._nomPb.Plur_() + " envisageables")  
                    for pb in ref.listProblematiques[numCI]:
                        self.tip.AjouterElemListeUL("pb", pb)
                else:
                    self.tip.Supprime('pb')
                              
            elif param[:3] == "CMP":
#                 print param
                ref = self.GetReferentiel()
                competences = ref.getCompetenceEtGroupe("S"+param[3:])
                groupe, competence = competences[0], competences[-1]
                
                if len(competences) > 0:
                    self.tip.SetHTML(constantes.encap_HTML(constantes.BASE_FICHE_HTML_COMP_PRJ))
                    k = param[3:]
                    code, groupe = competences[0]
                    nc = ref.dicoCompetences["S"]._nom.Sing_()
                    self.tip.SetWholeText("titre", nc + " " + k)
                    self.tip.SetWholeText("grp", code + "  " + groupe.intitule)
#                     print "***", competences
                    if len(competences) >= 2:
                        codec, competence = competences[1]
                        self.tip.SetWholeText("int", codec + " " + competence.intitule)
                        if len(competence.sousComp) > 0:
#                             print competence.sousComp.items()
                            lc = sorted(competence.sousComp.items(), key = lambda c:c[0])
                            for k, v in lc:
                                self.tip.AjouterElemListeDL('list', k, v.intitule)                 

            
            elif type(obj) == list:
                pass
                
            else:
                pass
            
        self.tip.SetPage()
        return self.tip

    
    
    #############################################################################            
    def getBitmapPeriode(self, larg):
        imagesurface = draw_cairo.getBitmapPeriode(larg, self.GetPositions(),
                                                       self.GetReferentiel().periodes, 
                                                       prop = 7)
        return getBitmapFromImageSurface(imagesurface)


    #############################################################################            
    def getBitmapCalendrier(self, larg):
        imagesurface = draw_cairo.getBitmapCalendrier(larg, self.calendrier)
        return getBitmapFromImageSurface(imagesurface)
    
    
    ##################################################################################################    
    def enregistrer(self, nomFichier, dialog = True):
        
#         print("enregistrer", nomFichier, end=' ') 
#         print("   ", self.dependants)
        # La progression
        progression = self.getBranche()
        classe = self.classe.getBranche()
        
        # La racine
        root = ET.Element("Progression_Classe")
        root.append(progression)
        root.append(classe)
        constantes.indent(root)
        
        ok = enregistrer_root(root, nomFichier, dialog = dialog)

        for lienSeq in [s for s in self.sequences_projets if isinstance(s, LienSequence)]:
            if lienSeq.sequence in self.dependants:
                nomFichier = os.path.join(self.GetPath(), lienSeq.path)
#                 print("++", self.GetPath(), lienSeq.path)
                ok = ok and lienSeq.sequence.enregistrer(nomFichier, dialog = dialog)
        
        for lienPrj in [s for s in self.sequences_projets if isinstance(s, LienProjet)]:
            if lienPrj.projet in self.dependants:
                nomFichier = os.path.join(self.GetPath(), lienPrj.path)
                ok = ok and lienPrj.projet.enregistrer(nomFichier, dialog = dialog)

        del self.dependants[:]

        return ok


    ######################################################################################  
    def GetBulleHTML(self, i = None, css = False):
        """ Renvoie le tootTip sous la forme HTML
            pour affichage sur la fiche HTML (template "_CSS")
            ou sur la fiche pySéquence (template par défaut)
            
            :i:  code pour différentier ...
        """
#         print("GetBulleHTML Prg", self, i)
        ref = self.GetReferentiel()
        
        if i == "Equ":
            if css:
                t = Template(constantes.TEMPLATE_PROF_CSS)
            else:
                t = Template(constantes.TEMPLATE_PROF)
            
            lst_prf = [p.GetNomPrenom() for p in self.equipe]
            
            html = t.render(titre = "Équipe pédagogique",
                            lst_prf = lst_prf,
                            )
    
            return html
        
        
        elif i == "Elv":
            if css:
                t = Template(constantes.TEMPLATE_ELEVE_CSS)
            else:
                t = Template(constantes.TEMPLATE_ELEVE)
            
            lst_elv = [p.GetNomPrenom() for p in self.eleves]
            
            html = t.render(titre = ref.labels["ELEVES"][2].Plur_(),
                            lst_elv = lst_elv,
                            )
    
            return html
        
        
        
        elif i == "CI":
        
            if css:
                t = Template(constantes.TEMPLATE_CI_CSS)
            else:
                t = Template(constantes.TEMPLATE_CI_CSS)
                
                
            html = t.render(titre = ref._nomCI.Plur_(),
                            lst_pb = [],
                            nomPb = "",
                            lst_CI = [("CI"+str(i+1), ci) for i, ci in enumerate(self.GetListeCI())],
                            )
            return html
        
        
        
        
        
        elif i[:2] == "CI":  
        
            c = int(i[2:])
#             ref._dicoCompetences
            
            if css:
                t = Template(constantes.TEMPLATE_CMP_SAV_CSS)
            else:
                t = Template(constantes.TEMPLATE_CMP_SAV)
            
            
            dic = {}
            dic[ref._nomCI.Sing_()] = [(i, self.GetListeCI()[c])]
           
            
            html = t.render(dic = dic)
            return html
        
        
        
        
        
        elif i[:2] == "C_":
            c = i[2:]
#             ref._dicoCompetences
            
            if css:
                t = Template(constantes.TEMPLATE_CMP_SAV_CSS)
            else:
                t = Template(constantes.TEMPLATE_CMP_SAV)
            
            
#             for i, c in enumerate(sorted(self.competences)):
            dic = ref.getDicToutesCompetences()
            titre = dic['S']._nom.sing_()  + " ("+ dic['S'].abrDiscipline+ ")"
            
            dic = {}
            dic[titre] = [(c, ref.getCompetence('S'+c).intitule)]
           
            
            html = t.render(dic = dic)
            return html
        
        
        
        elif i == "Cal":
            if css:
                t = Template(constantes.TEMPLATE_EFF_CSS)
            else:
                t = Template(constantes.TEMPLATE_EFF)
            
            
            image = draw_cairo.getBase64PNG(draw_cairo.getBitmapCalendrier(400, self.calendrier))

            if css:
                if image is not None:
                    image = b64(image)
                else:
                    image = None
                
            else:
                image = self.tip.GetImgURL(image, width = 200)
            
            
            html = t.render(titre = "Calendrier de la formation",
                            image = image,
                            )
    
            return html
        
        return  ""


#########################################################################################################
#########################################################################################################
class ElementProgression():
    def __init__(self, path = r""):
        self.path = path
        
        doc = self.GetDocument()
        if hasattr(doc, 'nbrCreneaux'):
            self.creneaux = [0,doc.nbrCreneaux-1]  # Créneau horaire [début, fin]
        else:
            self.creneaux = [0,0]
        
        self.rang = 0 # pour l'ordonnancement
    
    ######################################################################################  
    def __eq__(self, lien):
        return isinstance(lien, ElementProgression) \
            and os.path.normpath(self.path) == os.path.normpath(lien.path)
    
    
    ######################################################################################  
    def __lt__(self, doc):
        """ utilisé pour la fonction .sort() dans Progression.Ordonner()
        """
        doc0 = self.GetDoc()
        doc1 = doc.GetDoc()
        #print(doc0, "<", doc1, "?")
        if doc0.position[0] == doc1.position[0]:
            dp0 = doc0.position[1]-doc0.position[0]
            dp1 = doc1.position[1]-doc1.position[0]
            if dp0 == dp1:
#                 c0, c1 = self.GetNbCrenaux() , doc.GetNbCrenaux()
#                 if c0 == c1:
                return self.rang < doc.rang
#                 else:
#                     return c0 < c1
            else:
                return dp0 < dp1
        else:
            return doc0.position[0] < doc1.position[0]
        
    
    ######################################################################################  
    def MemeRang(self, doc):
        """ Renvoie True si les éléments peuvent être placés au même rang
            (utilisé pour Drag and Drop ou menu contextuel Monter/Descendre (à faire !)
        """
        doc0 = self.GetDoc()
        doc1 = doc.GetDoc()
        if doc0.position[0] == doc1.position[0]:        # même début
            dp0 = doc0.position[1]-doc0.position[0]
            dp1 = doc1.position[1]-doc1.position[0]
            if dp0 == dp1:
                return True                            # même durée
#                 c0, c1 = self.GetNbCrenaux() , doc.GetNbCrenaux()
#                 if c0 == c1:                            # même nbr de 
#                     return True
#                 else:
#                     return False
            else:
                return False
        else:
            return False
        
    
    
    ####################################################################################
    def EstMovable(self):
        return True
    
        
#     ######################################################################################  
#     def comp(self, lienSeq):
#         """
#         """
#         return self.GetDoc().position[0] > lienSeq.GetDoc().position[0]

    ######################################################################################  
    def GetCode(self, num = None):
        parent = self.GetDocument()
        if isinstance(parent, Progression):
            num = str(parent.sequences_projets.index(self))
        elif isinstance(parent, Sequence):
            num = str(parent.prerequisSeance.index(self))
        return self.codeXML+num
    
    
    ######################################################################################  
    def GetIntit(self, i = 0):
        return self.GetDoc().intitule
    
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    ######################################################################################  
    def GetDocument(self):    
        return self.parent

    ######################################################################################  
    def GetCrenaux(self):
        return list(range(self.creneaux[0], self.creneaux[1]+1))
    
    ######################################################################################  
    def GetNbCrenaux(self):
        return len(self.GetCrenaux())
    
    ######################################################################################  
    def GetNbrPeriodes(self):
        doc = self.GetDoc()
        if doc is not None:
            return doc.GetNbrPeriodes()
        return 0
        
    ######################################################################################  
    def GetDuree(self):
        doc = self.GetDoc()
        if doc is not None:
            return doc.GetDuree()
        return 1
    
    
    ######################################################################################  
    def GetPeriodes(self):
        doc = self.GetDoc()
        if doc is not None:
            return doc.GetPositions()
        return [0]
    
    ######################################################################################  
    def GetPosition(self):
        doc = self.GetDoc()
        if doc is not None:
            return doc.position
        return [0, 0]
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du lien de sequence pour enregistrement
        """
        root = ET.Element(self.codeXML)
        root.set("dir", toSystemEncoding(self.path))
        root.set("creneaux", "_".join([str(p) for p in self.creneaux]))
        root.set("rang", str(self.rang))
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche LienSequence", self
        self.path = toFileEncoding(branche.get("dir", ""))
        
        if isinstance(self.GetDocument(), Progression):
            nc = self.GetDocument().nbrCreneaux
        else:
            nc = 1
        sp = branche.get("creneaux", "0_"+str(nc-1))
        sp = sp.split("_")
        if len(sp) == 1:
            sp = [sp[0], sp[0]]
        self.creneaux = [int(sp[0]), int(sp[1])]
        
        self.rang = int(branche.get("rang", "0"))
        
#        if hasattr(self, 'panelPropriete'):
#            self.panelPropriete.MiseAJour()

    
    
    ######################################################################################  
    def GetBulleHTML(self, i = None, css = False):
        """ Renvoie le tootTip sous la forme HTML
            pour affichage sur la fiche HTML (template "_CSS")
            ou sur la fiche pySéquence (template par défaut)
            
            :i:  code pour différentier ...
        """
#         print("GetBulleHTML liendoc", self, i)
        ref = self.GetReferentiel()
        
        

        doc = self.GetDoc()
        
        if doc is None:
            html = ""
        
        
        elif isinstance(doc, Sequence) or isinstance(doc, Projet):
            if css:
                t = Template(constantes.TEMPLATE_LIENDOC_CSS)
            else:
                t = Template(constantes.TEMPLATE_LIENDOC)
            
            image = draw_cairo.getBase64PNG(draw_cairo.get_apercu(doc, 600,
                                                                  entete = True))
           
            if css:
                if image is not None:
                    image = b64(image)
                else:
                    image = None
                
            else:
                image = self.tip.GetImgURL(image, width = 200)
            
            
            html = t.render(titre = self.Sing_(),
                            intitule = doc.intitule,
                            creneaux = " - ".join([str(i+1) for i in range(*self.creneaux)]),
                            image = image,
                            path = self.path
                            )
        
        
        return html
        

        
        
#########################################################################################################
#########################################################################################################
class LienSequence(ElementBase, ElementProgression, Grammaire):
    def __init__(self, parent, path = r""):
        Grammaire.__init__(self, "Séquence(s)$f")
        
        self.codeXML = "Sequence"
        self.parent = parent
        ElementBase.__init__(self)
        ElementProgression.__init__(self, path)
        
        self.sequence = None
        

    ######################################################################################  
    def __repr__(self):
        return "LienSeq : "+self.path#str(self.GetPosition()[0])+" > "+str(self.GetPosition()[-1]-self.GetPosition()[0])

    ####################################################################################
    def EstMovable(self):
        return True
    
    ####################################################################################
    def EstMemeCategorie(self, obj):
        return isinstance(obj, LienSequence)   \
                or isinstance(obj, LienProjet)
                
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        if self.sequence is not None:
            return PanelPropriete_LienSequence(parent, self)
    
    ######################################################################################  
    def GetDoc(self):
        return self.sequence
    
    
    ######################################################################################  
    def GetPosition(self):
        if self.sequence is not None:
            return self.sequence.position
        return [0,0]
    
    
    ######################################################################################  
    def MiseAJourArbre(self):
        self.arbre.SetItemText(self.branche, self.GetNomFichier())
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
#         if self.sequence is None:
#             return
#         print("ConstruireArbre")
        self.arbre = arbre
        
        
#         self.codeBranche = CodeBranche(self.arbre)
#        self.codeBranche.SetForegroundColour(coul)
        self.branche = arbre.AppendItem(branche, self.GetNomFichier(), #wnd = self.codeBranche, 
                                        data = self,
                                        image = self.arbre.images["Seq"])
#         self.codeBranche.SetBranche(self.branche)
        if self.sequence is not None:
            self.sequence.DefinirCouleurs()
#             print(draw_cairo.BcoulPos)
#             print(self.sequence.position[0])
            coul = draw_cairo.BcoulPos[self.sequence.position[0]]
            coul = [int(200*c) for c in coul]
            self.arbre.SetItemTextColour(self.branche, wx.Colour(*coul))
        else:
            self.arbre.SetItemBackgroundColour(self.branche, wx.Colour("TOMATO1"))
            if self.path is not None:
                t = "Le fichier\n %s\nn'a pas été trouvé !" %self.path
            self.SetToolTip(self.GetNomFichier() + "\n" + t)
    
    
    ######################################################################################  
    def ChargerSequence(self, reparer = False):
#         print("ChargerSequence", self.path)
        classe, sequence = self.GetDocument().OuvrirFichierSeq(self.path, reparer = reparer)
        if classe != None and classe.typeEnseignement == self.GetReferentiel().Code:
            self.sequence = sequence
        
    
    ######################################################################################  
    def SignalerPb(self, pb):
        if hasattr(self, 'branche'):
            bg_color = self.arbre.GetBackgroundColour()
            if len(pb) == 0:
                self.arbre.SetItemBackgroundColour(self.branche, bg_color)
                self.SetToolTip(self.sequence.intitule)
            else:
                self.arbre.SetItemBackgroundColour(self.branche, wx.Colour("LIGHT PINK"))
                message = "Les prérequis suivants n'ont pas été abordés dans les séquences précédentes :\n"
                self.SetToolTip(message + " - ".join(pb))
                
            
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            doc = self.parent
            if isinstance(doc, Progression):
                doc.app.AfficherMenuContextuel([["Supprimer", 
                                                 functools.partial(doc.SupprimerLien, item = itemArbre), 
                                                 scaleImage(images.Icone_suppr_seq.GetBitmap())],
                                                ["Ouvrir", 
                                                 functools.partial(doc.OuvrirSequence, item = itemArbre), 
                                                 scaleImage(images.Icone_open.GetBitmap())]
                                                ])
            else:
                doc.app.AfficherMenuContextuel([["Supprimer", 
                                                 functools.partial(doc.SupprimerLienSequence, item = itemArbre), 
                                                 scaleImage(images.Icone_suppr_seq.GetBitmap())],
                                                ])


    ######################################################################################  
    def SetLabel(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.sequence.intitule)
        

    ######################################################################################  
    def GetNomFichier(self):
        """ Renvoie le nom affiché sur la fiche de Sequence
            quand la Séquence est un prérequis à une autre
        """
        if self.sequence is not None and len(self.sequence.intitule) > 0:
            return self.sequence.intitule
        return os.path.splitext(os.path.basename(self.path))[0]


    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.encap_HTML(constantes.BASE_FICHE_HTML_SEQ)


    ######################################################################################  
    def SetTip(self):
        # Tip
        seq = self.sequence
        
        self.tip.SetHTML(self.GetFicheHTML())
        if seq is None:
            self.tip.SetWholeText("nom", "Séquence non trouvée")
        else:
            self.tip.SetWholeText("nom", seq.intitule)
            self.tip.AjouterImg("ap", seq.GetApercu(600, 265, entete = True)) 
        
        self.tip.SetPage()







#########################################################################################################
#########################################################################################################
class LienProjet(ElementBase, ElementProgression, Grammaire):
    def __init__(self, parent, path = r""):
        Grammaire.__init__(self, "Projet(s)$m")
        
#         self.nom_obj = "Projet"
#         self.article_c_obj = "du"
#         self.article_obj = "le"
        
        self.codeXML = "Projet"
        
        self.parent = parent
        ElementBase.__init__(self)
        ElementProgression.__init__(self, path)
        
        self.projet = None
        
        #
        # Création du Tip (PopupInfo)
        #
#         self.tip = PopupInfo(self.GetApp().parent, "")
#        self.ficheHTML = self.GetFicheHTML()
#        self.tip = PopupInfo(self.parent.app, self.ficheHTML)

        
    ######################################################################################  
    def __repr__(self):
        return "LienPrj :"+str(self.GetPosition()[0])+" > "+str(self.GetPosition()[-1]-self.GetPosition()[0])

    ####################################################################################
    def EstMovable(self):
        return True
    
    ####################################################################################
    def EstMemeCategorie(self, obj):
        return isinstance(obj, LienSequence)   \
                or isinstance(obj, LienProjet)
                
    ######################################################################################  
    def GetDoc(self):
        return self.projet
    
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_LienProjet(parent, self)
    
    
    ######################################################################################  
    def GetPosition(self):
        return self.projet.position
    

    ######################################################################################  
    def MiseAJourArbre(self):
        self.arbre.SetItemText(self.branche, self.projet.intitule)
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        if self.projet is None:
            return
#         print("ConstruireArbre", self.projet.position)
        self.arbre = arbre
            
        coul = draw_cairo.BcoulPos[self.projet.position[0]]
        coul = [int(200*c) for c in coul]
#         self.codeBranche = CodeBranche(self.arbre)
#        self.codeBranche.SetForegroundColour(coul)
        self.branche = arbre.AppendItem(branche, self.projet.intitule, # wnd = self.codeBranche, 
                                        data = self,
                                        image = self.arbre.images["Prj"])
#         self.codeBranche.SetBranche(self.branche)
        self.arbre.SetItemTextColour(self.branche, wx.Colour(*coul))

#        self.codeBranche.SetBranche(self.branche)
        
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)

    
    ######################################################################################  
    def ChargerProjet(self, reparer = False):
        print("ChargerProjet", self.path)
        classe, projet = self.GetDocument().OuvrirFichierPrj(self.path, reparer = reparer)
        print("   ", classe.typeEnseignement , self.GetReferentiel().Code)
        if classe != None and classe.typeEnseignement == self.GetReferentiel().Code:
            self.projet = projet


    ######################################################################################  
    def SignalerPb(self, pb):
        if hasattr(self, 'branche'):
            bg_color = self.arbre.GetBackgroundColour()
            if len(pb) == 0:
                self.arbre.SetItemBackgroundColour(self.branche, bg_color)
                self.SetToolTip(self.projet.intitule)
            else:
                self.arbre.SetItemBackgroundColour(self.branche, wx.Colour("LIGHT PINK"))
                message = ""
                self.SetToolTip(message + " - ".join(pb))
                
            
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
#        print "AfficherMenuContextuel"
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([["Supprimer", 
                                                     functools.partial(self.parent.SupprimerLien, item = itemArbre), 
                                                     scaleImage(images.Icone_suppr_prj.GetBitmap())],
                                                    ["Ouvrir", 
                                                     functools.partial(self.parent.OuvrirProjet, item = itemArbre), 
                                                     scaleImage(images.Icone_open.GetBitmap())]
                                                    ])


    ######################################################################################  
    def SetLabel(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.projet.intitule)
        

    ######################################################################################  
    def GetNomFichier(self):
        return os.path.splitext(os.path.basename(self.path))[0]


    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.encap_HTML(constantes.BASE_FICHE_HTML_PRJ)


    ######################################################################################  
    def SetTip(self):
        # Tip
        seq = self.projet
        self.tip.SetHTML(self.GetFicheHTML())
        self.tip.SetWholeText("nom", seq.intitule)
        self.tip.AjouterImg("ap", seq.GetApercu(600, 200 , entete = True)) 
        
        self.tip.SetPage()






 
####################################################################################
#
#   Classe définissant les propriétés d'une séquence
#
####################################################################################
class CentreInteret(ElementBase):
    def __init__(self, parent):
        self.parent = parent
        ElementBase.__init__(self)
        
        self.numCI = []       # Numéros des CI du Référentiel
        self.CI_perso = []    # Intitulés des Centres d'Intérêt personnalisés
        self.PosCI_perso = [] # Position Cible des CI perso (format "MEI_FSC")
        
        self.poids = []
        
        self.Pb = []        # Problématiques proposées
        self.Pb_perso = []  # Problématiques personnalisées
        
        
        ref = self.GetReferentiel()
        Grammaire.__init__(self, ref.nomCI)
        
        
        self.MiseAJourTypeEnseignement()
            
        self.SetNum(self.numCI)

        
        
    ######################################################################################  
    def __repr__(self):
        return "CI %s" %self.numCI
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_CI(parent, self)
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    ######################################################################################  
    def GetDocument(self):    
        return self.parent
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du centre d'intérét pour enregistrement
        """
        root = ET.Element("CentresInteret")
        for i, num in enumerate(self.numCI):
            root.set("C"+str(i), str(num))
            root.set("P"+str(i), str(self.poids[i]))
        
        # Centres d'Intérêt personnalisés
        CI_perso = ET.SubElement(root, "CI_perso")
        for i, ci in enumerate(self.CI_perso):
            CI_perso.set("CI_"+str(i), ci)
            
        # Positions des Centres d'Intérêt personnalisés
        PosCI_perso = ET.SubElement(root, "PosCI_perso")
        for i, ci in enumerate(self.PosCI_perso):
            PosCI_perso.set("CI_"+str(i), ci)
 
        # Problématiques proposées
        Pb = ET.SubElement(root, "Problematiques")
        for i, pb in enumerate(self.Pb):
            Pb.set("Pb_"+str(i), pb)
            
        # Problématiques personnalisées
        Pb = ET.SubElement(root, "Pb_Perso")
        for i, pb in enumerate(self.Pb_perso):
            Pb.set("PbP_"+str(i), pb)
            
#         root.set("Pb", self.Pb)
            
            
        return root
        
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche CI"
        self.numCI = []
        self.poids = []
        for i in range(len(branche.keys())):
            n = branche.get("C"+str(i), "")
            if n != "":
                self.numCI.append(eval(n))
                self.poids.append(eval(branche.get("P"+str(i), "1")))
        
        # Pour rétro compatibilité
        if self.numCI == []:
            if len(list(branche)) > 0:
                code = list(branche)[0].tag
                if code == "_":
                    num = []
                    self.AddNum(num)
                else:
                    try:
                        num = eval(code[2:])-1
                        self.AddNum(num)
                    except:
                        pass
        
        # Centres d'Intérêt personnalisés
        self.CI_perso = []
        CI_perso = branche.find("CI_perso")
        if CI_perso != None:
            i = 0
            continuer = True
            while continuer:
                t = CI_perso.get("CI_"+str(i), "")
                if t == "":
                    continuer = False
                else:
                    self.CI_perso.append(t)
                    i += 1

        # Positions des Centres d'Intérêt personnalisés
        self.PosCI_perso = []
        CI_perso = branche.find("PosCI_perso")
        if CI_perso != None:
            i = 0
            continuer = True
            while continuer:
                t = CI_perso.get("CI_"+str(i), "")
                if t == "":
                    continuer = False
                else:
                    self.PosCI_perso.append(t)
                    i += 1
        # Correction bug :
        if len(self.PosCI_perso) > len(self.CI_perso):
            self.PosCI_perso = self.PosCI_perso[:len(self.CI_perso)]
        elif len(self.PosCI_perso) < len(self.CI_perso):
            self.PosCI_perso.extend([""]*(len(self.CI_perso)-len(self.PosCI_perso)))
        
        
        # Problématiques proposées
        self.Pb = []
        Pb = branche.find("Problematiques")
        if Pb != None:
            i = 0
            continuer = True
            while continuer:
                t = Pb.get("Pb_"+str(i), "")
                if t == "":
                    continuer = False
                else:
                    self.Pb.append(t)
                    i += 1
                    
        # Problématiques personnalisées
        self.Pb_perso = []
        Pb = branche.find("Pb_Perso")
        if Pb != None:
            i = 0
            continuer = True
            while continuer:
                t = Pb.get("PbP_"+str(i), "")
                if t == "":
                    continuer = False
                else:
                    self.Pb_perso.append(t)
                    i += 1
#         self.Pb = branche.get("Pb", "")
    
    
    ######################################################################################  
    def AddNum(self, num, poids = 1): 
        self.numCI.append(num)
        self.poids.append(poids)
        self.SetNum()
        
    ######################################################################################  
    def Set1Num(self, num, poids = 1): 
        self.numCI = [num]
        self.poids = [poids]
        self.SetNum()
    
        
    ######################################################################################  
    def DelNum(self, num):
        i = self.numCI.index(num)
        self.numCI.remove(num)
        del self.poids[i]
        self.SetNum()
        
        
    ######################################################################################  
    def ToogleNum(self, num):
        if num in self.numCI:
            self.DelNum(num)
        else:
            self.AddNum(num)
            
            
    ######################################################################################  
    def SetNum(self, numCI = None, poids = 1):
#        print "SetNum", numCI
        if numCI != None:
            self.numCI = numCI
#            self.poids = poids
        self.numCI.sort()
        
        if hasattr(self, 'arbre'):
            self.MaJArbre()
        
#        if len(self.numCI) > 0 :
        self.parent.Verrouiller()
        

    ######################################################################################  
    def GetListCIref(self):
        """ Renvoie la liste des CI du Référentiel
        """
        if self.GetReferentiel().CI_cible:
            return self.parent.classe.referentiel.CentresInterets
        else:
            return self.GetReferentiel().CentresInterets
        
        
    ######################################################################################  
    def GetIntit(self, num):
        return self.GetNomCIs()[num]
#         lstCI = self.GetListCIref()
#         if self.numCI[num] < len(lstCI):
#             return lstCI[self.numCI[num]]
    
    
    ######################################################################################  
    def GetCodesCIs(self):
        """ Renvois la liste de tous les codes de CI
             Référentiel et Perso
        """
#         ref = self.GetReferentiel()
#         nci = len(ref.CentresInterets)
#         cip = [ref.abrevCI+str(n) for n in list(range(nci, nci+len(self.CI_perso)))]
#         print("GetCodesCI", cip)
        return [self.GetCode(n) for n in range(len(self.numCI)+len(self.CI_perso))]
    
    
    ######################################################################################  
    def GetNomCIs(self):
        """ Renvois la liste de tous les intitulés de CI
             Référentiel et Perso
        """
        lstCI = self.GetListCIref()
        l = [lstCI[n] for n in self.numCI]
        return l + self.CI_perso


    ######################################################################################  
    def GetCode(self, num = None, sep = " - "):
        """ Renvoie le code du CI à partir de son num'
            Si num est None : renvoie une chaîne avec tous les codes
        """
#         print("GetCode", num, self.numCI)
        if num == None:
            return sep.join([self.GetCode(n) for n in range(len(self.numCI)+len(self.CI_perso))])
        
        else :
            if num < len(self.numCI):
                return self.GetReferentiel().abrevCI+str(self.numCI[num]+1)
            else:
                ref = self.GetReferentiel()
                nci = len(ref.CentresInterets)
                return self.GetReferentiel().abrevCI+str(nci+num-len(self.numCI)+1)


    ######################################################################################  
    def GetPosCible(self, num):
        cod = self.GetCodesCIs()
#         print("GetPosCible", num, cod)
        ref = self.GetReferentiel()
        if ref.CI_cible:
            if num < len(self.numCI):
                return ref.positions_CI[self.numCI[num]]
            elif 0 <= num-len(self.numCI) < len(self.PosCI_perso):
                return self.PosCI_perso[num-len(self.numCI)]
                
        
    
    ######################################################################################  
    def MaJArbre(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.GetCode())
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre)
        if self.maxCI == 1:
            t = self.GetReferentiel()._nomCI.Sing_()
        else:
            t = self.GetReferentiel()._nomCI.Plur_()
        self.branche = arbre.AppendItem(branche, 
                                        t + " :", 
                                        wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Ci"])
        self.codeBranche.SetBranche(self.branche)
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)

        
#    #############################################################################
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
#            return self.branche
#        rect = draw_cairo.posCI + draw_cairo.tailleCI
#        if dansRectangle(x, y, (rect,)):
##            self.arbre.DoSelectItem(self.branche)
#            return self.branche
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        maxCIref = self.GetReferentiel().maxCI
#         if maxCIref == 0:
#             self.maxCI = 2
#         else:
#             self.maxCI = maxCIref
        self.maxCI = maxCIref    
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, self.GetReferentiel()._nomCI.Plur_()+" :")
#        self.GetPanelPropriete().construire()

    
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.encap_HTML(constantes.BASE_FICHE_HTML_CI)
    
    
    ######################################################################################  
    def GetBulleHTML(self, i = None, css = False):
#         print("GetBulleHTML", self, i)
        ref = self.GetReferentiel()
        
        if len(self.numCI)+len(self.CI_perso) > 1:
            titre = ref._nomCI.Plur_()
        else:
            titre = ref._nomCI.Sing_()
        
        lst_CI = []
        for i, c in enumerate(self.numCI):
            lst_CI.append((self.GetCode(i), self.GetIntit(i)))
        for i, c in enumerate(self.CI_perso):
            lst_CI.append((ref.abrevCI+str(len(ref.CentresInterets)+i+1), c))
        
        lst_pb = []
        nomPb = ""
        if len(self.Pb + self.Pb_perso) > 0:
            if len(self.Pb + self.Pb_perso) > 1:
                nomPb = ref._nomPb.Plur_()
            else:
                nomPb = ref._nomPb.Sing_()
            for pb in self.Pb + self.Pb_perso:
                lst_pb.append(pb)
        
        if css:
            t = Template(constantes.TEMPLATE_CI_CSS)
        else:
            t = Template(constantes.TEMPLATE_CI)
        html = t.render(titre = titre,
                        lst_CI = lst_CI,
                        lst_pb = lst_pb,
                        nomPb = nomPb)
        return html
    
    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        
        ref = self.GetReferentiel()
        if len(self.numCI)+len(self.CI_perso) > 1:
            t = ref._nomCI.Plur_()
        else:
            t = ref._nomCI.Sing_()
        self.tip.SetWholeText("titre", t)
        
        for i, c in enumerate(self.numCI):
            self.tip.AjouterElemListeDL("ci", self.GetCode(i), self.GetIntit(i))
        
        for i, c in enumerate(self.CI_perso):
            self.tip.AjouterElemListeDL("ci", ref.abrevCI+str(len(ref.CentresInterets)+i+1), c)
        
        if len(self.Pb + self.Pb_perso) > 0:
            self.tip.SetWholeText("nomPb", ref._nomPb.Sing_())
            for pb in self.Pb + self.Pb_perso:
                self.tip.AjouterElemListeUL("pb", pb)
        else:
            self.tip.SupprimerTag("pb")             
                        
        self.tip.SetPage()
        


####################################################################################
# #
# #   Classe définissant les propriétés des Objectifs de la Séquence
# #
# ####################################################################################
# class Objectifs(ElementBase):
#     def __init__(self, parent, numComp = None, prerequis = False):
#         self.parent = parent
#         ElementBase.__init__(self)
#         
#         self.objectifs = {"Comp"}       # Liste des Objectifs (Compétences ou Savoirs) de la Séquence
#         
#         
# 
#     ######################################################################################  
#     def __repr__(self):
#         return u"Compétences : "+" ".join(self.competences)
#         
#     ######################################################################################  
#     def GetApp(self):
#         return self.parent.GetApp()
#     
#     ######################################################################################  
#     def GetPanelPropriete(self, parent, code, comp):
#         """ Renvoie le PanelPropriete approprié
#             <comp> est du type Referentiel.Competences
#         """
#         ref = self.GetReferentiel()
#         if self.prerequis:
#             contexte = "P"
#         else:
#             contexte = "O"
#         dep = ref.getDependant(comp, contexte)
#         
#         return PanelPropriete_Competences(parent, self, code, comp, dep = dep)
#     
#     ######################################################################################  
#     def getBranche(self):
#         """ Renvoie la branche XML de la compétence pour enregistrement
#         """
#         root = ET.Element("Competences")
#         for i, s in enumerate(self.competences):
#             root.set("C"+str(i), s)
#         return root
#     
#     
#     ######################################################################################  
#     def setBranche(self, branche):
#         self.competences = []
#         for i in range(len(branche.keys())):
#             
#             codeindic = branche.get("C"+str(i), "")
#             
#             # Avant la version 7, il n'y a pas de préfixe "type" devant le code competence
#             if self.GetClasse().GetVersionNum() < 7:
# #                 print "setBranche", codeindic
#                 ref = self.GetReferentiel()
#                 ref_tc = None
#                 lstComp = [] # liste des "type" Referentiel.Competences compatibles avec "codeindic"
#                 if ref.tr_com != []: # B = tronc commun --> référentiel
#                     ref_tc = REFERENTIELS[ref.tr_com[0]]
#                 
#                     comp = ref_tc.dicoCompetences["S"]
#                     c = comp.getCompetence(codeindic)
#                     if c is not None:
#                         lstComp.append("B")
#                     
#                 for typ in ref.dicoCompetences.keys():
#                     comp = ref.dicoCompetences[typ]
#                     c = comp.getCompetence(codeindic)
#                     if c is not None:
#                         lstComp.append(typ)
#                 
#                 if ref_tc is not None:
#                     for typ in [k for k in ref_tc.dicoCompetences.keys() if k != "S"]:
#                         comp = ref.dicoCompetences[typ]
#                         c = comp.getCompetence(codeindic)
#                         if c is not None:
#                             lstComp.append(typ)    
#                 
# #                 print "lstComp", lstComp
#                 if lstComp != []:
#                     codeindic = lstComp[0]+codeindic
#                 else:
#                     codeindic = "S"+codeindic
#                     
#             self.competences.append(codeindic)
#         
# #        self.GetPanelPropriete().MiseAJour()
#     
#     
#     
#     ######################################################################################  
#     def ToogleCode(self, code):
#         self.Etendre()
#         if code in self.competences:
#             self.competences.remove(code)
#         else:
#             self.competences.append(code)
#         self.Condenser()
#             
#     ######################################################################################       
#     def Etendre(self):
#         """ Etend la liste des compétences :
#             A1
#                 >>>
#                     A1
#                     A1.1
#                     A1.2
#                     A1.3
#         """
# #         print "Etendre"
# #         print "   ", self.competences
#         ref = self.GetReferentiel()
#         
#         def ajouter(k, l, comp):
#             if len(comp.sousComp) > 0:
#                 for k2, c2 in comp.sousComp.items():
#                     ajouter("S"+k2, l, c2)
#             else:
#                 l.append(k)
#             
#         lstCompS = [c for c in self.competences if c[0] == "S"]
#         l = []
#         for k in lstCompS:
#             ajouter(k, l, ref.getCompetence(k))
#             
#         self.competences = l
# #         print "   ", self.competences
# 
# 
# 
#     ######################################################################################       
#     def Condenser(self):
#         """ Condense la liste des compétences :
#             A1.1
#             A1.2
#             A1.3
#                 >>>
#                     A1
#         """
# #         print "Condenser"
# #         print "   ", self.competences
#         ref = self.GetReferentiel()
#         s = set(self.competences)
#         
#         def condense(d, k, comp):
#             if len(comp.sousComp) > 0:
# #                 print " +++ ", comp.sousComp.keys()
#                 lk = [d+kk for kk in comp.sousComp.keys()]
#                 if set(lk).issubset(s):
#                     for sk in lk:
#                         s.remove(sk)
#                     s.add(d+k)
#                     
#                 for k1, v1 in comp.sousComp.items():
#                     condense(d, k1, v1)
#                 
#         for d, competences in ref.dicoCompetences.items():
#             dicCompetences = competences.dicCompetences
#             for k, v in dicCompetences.items():
#                 condense(d, k, v)
#             
#         self.competences = list(s)
# #         print "   ", self.competences
#         
#         
#         
#     ######################################################################################  
#     def GetCode(self, num):
#         return self.competences[num]
#     
#     ######################################################################################  
#     def GetTypCode(self, num):
#         return self.competences[num][0], self.competences[num][1:]
#     

#     
#     ######################################################################################  
#     def GetCodeDiscipline(self, code = "S"):
#         dic = self.GetReferentiel().getDicToutesCompetences()
#         return dic[code].codeDiscipline
#         
#     ######################################################################################  
#     def GetDiscipline(self, code):
#         dic = self.GetReferentiel().getDicToutesCompetences()
#         return dic[code].abrDiscipline
#             
#     ######################################################################################  
#     def GetDisciplineNum(self, num):
#         ref = self.GetReferentiel()
#         dicComp = ref.getToutesCompetences()
#         for code, comp in dicComp:
#             if code == self.GetCode(num)[0]:
#                 return comp.abrDiscipline
#     
# #         return self.GetReferentiel().dicoCompetences[self.competences[num][0]].abrDiscipline
#     
#     ######################################################################################  
#     def GetIntit(self, num):
#         return self.GetReferentiel().getCompetence(self.GetCode(num)).intitule  
# #         return self.GetReferentiel().getCompetence(self.competences[num]).intitule
# 
#     ######################################################################################  
#     def ConstruireArbre(self, arbre, branche, prerequis = False):
#         ref = self.GetReferentiel()
#         self.branche = branche
#         lst = ref.getToutesCompetences()
#         if prerequis:
#             aff = any([d.pre for k, d in lst])
#         else:
#             aff = any([d.obj for k, d in lst])
#         
#         if aff:
#             self.arbre = arbre
#             self.codeBranche = {}
#             self.branches = {}
#             for k, d in lst:
#                 if (prerequis and d.pre) or (not prerequis and d.obj):
#                     self.codeBranche[k] = CodeBranche(self.arbre, u"")
#                     self.branches[k] = arbre.AppendItem(branche, self.GetNomGenerique(k), 
#                                                         wnd = self.codeBranche[k], 
#                                                         data = (self, k, d),
#                                                         image = self.arbre.images["Com"])
#                     self.codeBranche[k].SetBranche(self.branches[k])
#                     self.arbre.SetItemTextColour(self.branches[k], 
#                                                  couleur.GetCouleurWx(COUL_DISCIPLINES[self.GetCodeDiscipline(k)]))
#                     self.arbre.SetItemBold(self.branches[k])
# 
#         else:
#             if hasattr(self, 'arbre'):
#                 del self.arbre
#     
#         
#         #
#         # Les "Fonctions" (à faire !)
#         #
#         if (len(ref.dicFonctions) > 0):
#             self.codeBranche["Fct"] = CodeBranche(self.arbre, u"")
#             self.branches["Fct"] = arbre.AppendItem(branche, ref.nomFonctions, 
#                                                    wnd = self.codeBranche[k], 
#                                                    data = (self, "Fct", ref.dicFonctions),
#                                                    image = self.arbre.images["Fct"])
#             self.codeBranche[k].SetBranche(self.branches["Fct"])
#             self.arbre.SetItemTextColour(self.branches["Fct"], couleur.GetCouleurWx(COUL_COMPETENCES))
# 
# 
#     
#     
#     #############################################################################
#     def MiseAJourTypeEnseignement(self):
#         if hasattr(self, 'arbre'):
#             del self.branches
#             self.ConstruireArbre(self.arbre, self.branche, self.prerequis)
# #         if hasattr(self, 'arbre'):
# #             for k, b in self.branche.items():
# #                 self.arbre.SetItemText(b, self.GetNomGenerique(k))
# #        if hasattr(self, 'panelPropriete'):
# #            self.GetPanelPropriete().Destroy()
# #            self.panelPropriete = PanelPropriete_Competences(self.panelParent, self)
# #            self.panelPropriete.construire()
#     
#     
#     ######################################################################################  
#     def GetFicheHTML(self, param = None):
#         return constantes.BASE_FICHE_HTML_COMP
# 
#     
#     ######################################################################################  
#     def SetTip(self):
# #         print "SetTip Comp"
#         self.tip.SetHTML(self.GetFicheHTML())
#         nc = self.GetNomGenerique()
#         self.tip.SetWholeText("titre", nc)
# #         print self.competences
# #         print sorted(self.competences)
#         for c in sorted(self.competences):
#             self.tip.AjouterElemListeDL("list", 
#                                  self.GetDiscipline(c[0]) +" " + c[1:], 
#                                  self.GetReferentiel().getCompetence(c).intitule  )
# #             self.tip.AjouterElemListeDL("list", 
# #                                  self.GetDisciplineNum(i) +" " + self.GetTypCode(i)[1], 
# #                                  self.GetIntit(i))
#       
#         self.tip.SetPage()



####################################################################################
#
#   Classe définissant les propriétés des compétences de la Séquence
#
####################################################################################
class Competences(ElementBase):
    def __init__(self, parent, numComp = None, prerequis = False):
        self.parent = parent
        ElementBase.__init__(self, tipWidth = 600*SSCALE)
        
        self.num = numComp
        self.competences = []       # Liste des compétences (prérequis ou objectif) de la Séquence
        self.filtre = None #[]
        
        self.prerequis = prerequis  # True si ce sont des competences prérequises
        
        

#     ######################################################################################  
#     def __repr__(self):
#         return "Compétences : "+" ".join(self.competences)
    
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    
    ######################################################################################  
    def GetDocument(self):    
        return self.parent

    
    ######################################################################################  
    def GetContext(self):
        """ Renvoie le contexte (Objectif ou Prérequis) des compétences
            sous forme d'un code : 'P' ou 'O'
        """
        if self.prerequis:
            return "P"
        else:
            return "O"
    
    
                
    ######################################################################################  
    def GetPanelPropriete(self, parent, code, compRef):
        """ Renvoie le PanelPropriete approprié
            <compRef> est du type Referentiel.Competences
        """
#         ref = self.GetReferentiel()
# #         dep = ref.getDependant(comp, contexte)
# #         if dep is not None:
#         seq = self.parent
        self.filtre = self.parent.GetFiltre(compRef, self.GetContext())#, self.filtre)
#         if hasattr(compRef, 'GetDicFiltre'):
        dic_f = compRef.GetDicFiltre(self.filtre)
#         else:
#             dic_f = compRef
#         print("GetPanelPropriete", self.filtre)
        return PanelPropriete_Competences(parent, self, code, dic_f, compRef)
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
        root = ET.Element("Competences")
        for i, s in enumerate(self.competences):
            root.set("C"+str(i), s)
        return root
    
    
    ######################################################################################  
    def setBranche(self, branche):
        self.competences = []
        for i in range(len(branche.keys())):
            
            codeindic = branche.get("C"+str(i), "")
            
            # Avant la version 7, il n'y a pas de préfixe "type" devant le code competence
            if self.GetClasse().GetVersionNum() < 7:
#                 print "setBranche", codeindic
                ref = self.GetReferentiel()
                ref_tc = None
                lstComp = [] # liste des "type" Referentiel.Competences compatibles avec "codeindic"
                if ref.tr_com != []: # B = tronc commun --> référentiel
                    ref_tc = REFERENTIELS[ref.tr_com[0]]
                
                    comp = ref_tc.dicoCompetences["S"]
                    c = comp.getCompetence(codeindic)
                    if c is not None:
                        lstComp.append("B")
                    
                for typ in ref.dicoCompetences:
                    comp = ref.dicoCompetences[typ]
                    c = comp.getCompetence(codeindic)
                    if c is not None:
                        lstComp.append(typ)
                
                if ref_tc is not None:
                    for typ in [k for k in ref_tc.dicoCompetences if k != "S"]:
                        comp = ref.dicoCompetences[typ]
                        c = comp.getCompetence(codeindic)
                        if c is not None:
                            lstComp.append(typ)    
                
#                 print "lstComp", lstComp
                if lstComp != []:
                    codeindic = lstComp[0]+codeindic
                else:
                    codeindic = "S"+codeindic
                    
            self.competences.append(codeindic)
        
#        self.GetPanelPropriete().MiseAJour()
    
    
    ######################################################################################  
    def getCompetencesEtendues(self):
        """ Renvoie la liste des compétences étendues :
            A1
            >>>
            A1
            A1.1
            A1.2
            A1.3
        """
#         print("getCompetencesEtendues", self.competences)
        ref = self.GetReferentiel()
        lr = set(self.competences)
        for code in self.competences:
            lr = lr | set([code[0]+c for c in ref.getSousElem(code[1:], "Comp_"+code[0])])
#         print("  >>>", list(lr))
        return list(lr)
    
    
    ######################################################################################  
    def ToogleCode(self, code):
        self.Etendre()
        if code in self.competences:
            self.competences.remove(code)
        else:
            self.competences.append(code)
        self.Condenser()
            
    ######################################################################################       
    def Etendre(self):
        """Etend la liste des compétences :
            A1
            >>>
            A1
            A1.1
            A1.2
            A1.3
        """
#         print "Etendre"
#         print "   ", self.competences
        ref = self.GetReferentiel()
        
        def ajouter(k, l, comp):
            if len(comp.sousComp) > 0:
                for k2, c2 in comp.sousComp.items():
                    ajouter("S"+k2, l, c2)
            else:
                l.append(k)
            
        lstCompS = [c for c in self.competences if c[0] == "S"]
        l = []
        for k in lstCompS:
            ajouter(k, l, ref.getCompetence(k))
            
        self.competences = l
#         print "   ", self.competences



    ######################################################################################       
    def Condenser(self):
        """Condense la liste des compétences :
            A1.1
            A1.2
            A1.3
            >>>
            A1
        """
#         print "Condenser"
#         print "   ", self.competences
        ref = self.GetReferentiel()
        s = set(self.competences)
        
        def condense(d, k, comp):
            if len(comp.sousComp) > 0:
#                 print " +++ ", comp.sousComp.keys()
                lk = [d+kk for kk in comp.sousComp]
                if set(lk).issubset(s):
                    for sk in lk:
                        s.remove(sk)
                    s.add(d+k)
                    
                for k1, v1 in comp.sousComp.items():
                    condense(d, k1, v1)
                
        for d, competences in ref.dicoCompetences.items():
            dicCompetences = competences.dicCompetences
            for k, v in dicCompetences.items():
                condense(d, k, v)
            
        self.competences = list(s)
#         print "   ", self.competences
        
    ######################################################################################  
    def TrierCodes(self):
        t = {}
        for d in self.competences:
            if d[0] in t.keys():
                t[d[0]].append(d[1:])
            else:
                t[d[0]] = [d[1:]]
        return t
        
    ######################################################################################  
    def GetCode(self, num = None, cod = None, sep = " - "):
        """ Renvoie le code de la Compétence à partir de son num'
            Si num est None : renvoie une chaîne avec tous les codes
        """
        if num is None:
            if cod is None:
                return sep.join(constantes.trier(self.competences))
            else:
                c = self.TrierCodes()
                if cod in c.keys():
                    return sep.join(constantes.trier(c[cod]))
                else:
                    return ""
        
        else :
            return self.competences[num]
    
    ######################################################################################  
    def GetTypCode(self, num):
        return self.competences[num][0], self.competences[num][1:]
    
    ######################################################################################  
    def GetNomGenerique(self, code = "S"):
        dic = self.GetReferentiel().getDicToutesCompetences()
        return dic[code]._nom.Plur_()  + " ("+ dic[code].abrDiscipline+ ")"
    
    ######################################################################################  
    def GetNomGenerique_sing(self, code = "S"):
        dic = self.GetReferentiel().getDicToutesCompetences()
        return dic[code]._nom.sing_()
    
    ######################################################################################  
    def GetCodeDiscipline(self, code = "S"):
        dic = self.GetReferentiel().getDicToutesCompetences()
        return dic[code].codeDiscipline
        
    ######################################################################################  
    def GetDiscipline(self, code):
        dic = self.GetReferentiel().getDicToutesCompetences()
        return dic[code].abrDiscipline
            
    ######################################################################################  
    def GetDisciplineNum(self, num):
        ref = self.GetReferentiel()
        dicComp = ref.getToutesCompetences()
        for code, comp in dicComp:
            if code == self.GetCode(num)[0]:
                return comp.abrDiscipline
    
#         return self.GetReferentiel().dicoCompetences[self.competences[num][0]].abrDiscipline
    
    ######################################################################################  
    def GetIntit(self, num):
        return self.GetReferentiel().getCompetence(self.GetCode(num)).intitule  
#         return self.GetReferentiel().getCompetence(self.competences[num]).intitule

    ######################################################################################  
    def SignalerPb(self, dif):
        if hasattr(self, 'codeBranche'):
            ref = self.GetReferentiel()
            
                
            if len(dif) > 0:
                # Tri par type de Savoir
                ddif = {}
                for d in dif:
                    if d[0] in ddif.keys():
                        ddif[d[0]].append(d[1:])
                    else:
                        ddif[d[0]] = [d[1:]]
                        
                couleur = "TOMATO1"
                message = "Certains objectifs visés\n" \
                          "ne sont pas abordés aux cours des %s" %ref._nomActivites.plur_()

                for k, cb in self.codeBranche.items():
                    if k in ddif.keys():
                        if len(ddif[k]) < 4:
                            if len(ddif[k]) > 1:
                                message += "\n"+self.GetNomGenerique(k)+" :"
                            else:
                                message += "\n"+self.GetNomGenerique_sing(k)+" :"

                            for d in ddif[k]:
                                message += "\n"+d
                        
                        cb.SetBackgroundColour(couleur)
                        cb.SetToolTip(message)
                        cb.Refresh()
                    
                
            else:
                message = "Tous les objectifs visés\n" \
                          "sont abordés aux cours des %s" %ref._nomActivites.plur_()
                couleur = COUL_OK
            
                for cb in self.codeBranche.values():
                    cb.SetBackgroundColour(couleur)
                    cb.SetToolTip(message)
                    cb.Refresh()
    
    
    ######################################################################################  
    def SetCodeBranche(self):
        if hasattr(self, 'codeBranche'):
            for k, cb in self.codeBranche.items():
                cb.SetLabel(self.GetCode(cod = k))
    
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche, prerequis = False):
#         print("ConstruireArbre Compétences", prerequis, self)
        ref = self.GetReferentiel()
        doc = self.GetDocument()
        self.branche = branche
        lst = ref.getToutesCompetences()
        if prerequis:
            aff = any([d.pre for k, d in lst])
        else:
            aff = any([d.obj for k, d in lst])
        
        ctx = self.GetContext()
        self.codeBranche = {}
        if aff:
            self.arbre = arbre
            
            self.branches = {}
            for k, d in lst:
                if (prerequis and d.pre) or (not prerequis and d.obj):
#                     print("   ", k, d, doc)
#                     print("   >>>", doc.GetFiltre(d, ctx))
                    f = doc.GetFiltre(d, ctx,  niveau = 1)
#                     print("   ", f)
                    if f is None or len(f) > 0:
                        self.codeBranche[k] = CodeBranche(self.arbre, "")
                        self.branches[k] = arbre.AppendItem(branche, self.GetNomGenerique(k), 
                                                            wnd = self.codeBranche[k], 
                                                            data = (self, k, d),
                                                            image = self.arbre.images["Com"])
                        self.codeBranche[k].SetBranche(self.branches[k])
                        self.arbre.SetItemTextColour(self.branches[k], 
                                                     couleur.GetCouleurWx(COUL_DISCIPLINES[self.GetCodeDiscipline(k)]))
                        self.arbre.SetItemBold(self.branches[k])

        else:
            if hasattr(self, 'arbre'):
                del self.arbre
    
        
        #
        # Les "Fonctions" (à faire !)
        #
#         if (len(ref.dicFonctions) > 0) and hasattr(self, 'arbre'):
        if (ref.fonctions is not None) and hasattr(self, 'arbre'):
            self.codeBranche["F"] = CodeBranche(self.arbre, "")
            self.branches["F"] = arbre.AppendItem(branche, ref.fonctions._nom.Plur_(), 
                                                   wnd = self.codeBranche["F"], 
                                                   data = (self, "F", ref.fonctions),
                                                   image = self.arbre.images["Fct"])
#             self.branches["Fct"] = arbre.AppendItem(branche, ref.nomFonctions, 
#                                                    wnd = self.codeBranche[k], 
#                                                    data = (self, "Fct", ref.dicFonctions),
#                                                    image = self.arbre.images["Fct"])
            self.codeBranche["F"].SetBranche(self.branches["F"])
            self.arbre.SetItemTextColour(self.branches["F"], 
                                         couleur.GetCouleurWx(COUL_COMPETENCES))

        self.SetCodeBranche()
    
    
    #########################################################################
    def GererElementsDependants(self, codeComp = None):
        """ Gestion des éléments (Competences, Savoirs, Th, Dom, Spe)
            qui dépendent de la compétence <codeComp>
        """
#         print("GererElementsDependants de", codeComp)
        seq = self.GetDocument()
        seq.GererElementsDependants(self.GetContext())
        
        
#         ref = seq.GetReferentiel()
# #         dicComp = ref.getDicToutesCompetences()
# #         compRef = dicComp[codeComp[0]] # type Referentiel.Competences
#         
#         if self.prerequis:
#             contexte = "P"
#         else:
#             contexte = "O"
#             
#             
#         elem_asso = []
#         for cc, comp in ref.dicoCompetences.items():
#             ea = ref.getElemAsso(comp, contexte)
#             if "Comp_"+codeComp[0] in ea:
#                 print("  ++", ea)
#                 elem_asso.append(comp)
#         
#         for cs, sav in ref.dicoSavoirs.items():
#             ea = ref.getElemAsso(sav, contexte)
#             if "Comp_"+codeComp[0] in ea:
#                 print("  ++", ea)
#                 elem_asso.append(sav)
#         print(" >>>", elem_asso)
#         
#         for ea in elem_asso:
#             seq.GererElementsDependants(self, ea, codeComp[0])

    
    
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'arbre'):
            del self.branches
            self.ConstruireArbre(self.arbre, self.branche, self.prerequis)
#         if hasattr(self, 'arbre'):
#             for k, b in self.branche.items():
#                 self.arbre.SetItemText(b, self.GetNomGenerique(k))
#        if hasattr(self, 'panelPropriete'):
#            self.GetPanelPropriete().Destroy()
#            self.panelPropriete = PanelPropriete_Competences(self.panelParent, self)
#            self.panelPropriete.construire()
    
    
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.encap_HTML(constantes.BASE_FICHE_HTML_COMP)

    
    ######################################################################################  
    def GetBulleSVG(self, i):
#         print("GetBulleSVG", self, i)

        c = sorted(self.competences)[i]
        t = self.GetDiscipline(c[0]) +" " + c[1:] + " :\n" + self.GetReferentiel().getCompetence(c).intitule  
        if self.GetDescription() != None:
            t += "\n\n" + self.GetDescription()
        
        return t
    
    ######################################################################################  
    def GetBulleHTML(self, i = None, css = False):
#         print("GetBulleHTML", self, i)
        ref = self.GetReferentiel()
        if css:
            t = Template(constantes.TEMPLATE_CMP_SAV_CSS)
        else:
            t = Template(constantes.TEMPLATE_CMP_SAV)
        
        dic = {}
        for i, c in enumerate(sorted(self.competences)):
            titre = self.GetNomGenerique(c[0])
            if not (titre in dic):
                dic[titre] = []
            dic[titre].append((c[1:], ref.getCompetence(c).intitule))
        
        html = t.render(dic = dic)
        
        return html
    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetBulleHTML())
        self.tip.SetPage()
        
# #         print "SetTip Comp"
#         self.tip.SetHTML(self.GetBHTML())
#         nc = self.GetNomGenerique()
#         self.tip.SetWholeText("titre", nc)
# #         print self.competences
# #         print sorted(self.competences)
#         for c in sorted(self.competences):
#             self.tip.AjouterElemListeDL("list", 
#                                  self.GetDiscipline(c[0]) +" " + c[1:], 
#                                  self.GetReferentiel().getCompetence(c).intitule  )
# #             self.tip.AjouterElemListeDL("list", 
# #                                  self.GetDisciplineNum(i) +" " + self.GetTypCode(i)[1], 
# #                                  self.GetIntit(i))
#       
#         self.tip.SetPage()

            
            
####################################################################################
#
#   Classe définissant les propriétés de savoirs
#
####################################################################################
class Savoirs(ElementBase):
    def __init__(self, parent, num = None, prerequis = False):
        self.parent = parent        # la séquence
        ElementBase.__init__(self, tipWidth = 600*SSCALE)
        
        self.prerequis = prerequis  # Indique que ce sont des savoirs prérequis
        self.savoirs = []       # Liste des savoirs (prérequis ou objectif) de la Séquence
        self.filtre = []
        
        
                
#     ######################################################################################  
#     def __repr__(self):
#         return "Savoirs : "+" ".join(self.savoirs)
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    ######################################################################################  
    def GetDocument(self):    
        return self.parent
    
    ######################################################################################  
    def GetPanelPropriete(self, parent, code, savRef):
        if self.prerequis:
            contexte = "P"
        else:
            contexte = "O"
#         print("savRef", savRef)
        self.filtre = self.parent.GetFiltre(savRef, contexte)#, self.filtre)
#         print("filtre", self.filtre)
        dic_f = savRef.GetDicFiltre(self.filtre)
#         print("dic_f_sav", dic_f)
        return PanelPropriete_Savoirs(parent, self, code, dic_f, savRef, filtre = self.filtre)
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du savoir pour enregistrement
        """
        root = ET.Element("Savoirs")
#         print("getBranche", self.savoirs)
        for i, s in enumerate(self.savoirs):
            root.set("S"+str(i), s)
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        """Interprétation de la branche (lecture fichier .seq)
            préfixes :
            - B = enseignement de base (tronc commun)
            - S = spécialité
            - M = math
            - P = physique
        """
#         print("setBranche Savoirs")
        
        # Détection d'un ancienne version (pas infaillible !)
        ancien = False
        for i in range(len(branche.keys())):
            code = branche.get("S"+str(i), "")
            if code != "":
                if not code[0] in ["B", "S", "M", "P"]: # version < 4.6
                    ancien = True
                    break
        
        self.savoirs = []
        for i in range(len(branche.keys())):
            code = branche.get("S"+str(i), "")
            if code != "":
                if ancien: # version < 4.6
                    if code[0] == "_":
                        code = "S"+code[1:]
                    else:
                        if self.GetReferentiel().tr_com == []:
                            code = "S"+code
                        else:
                            code = "S"+code
                                        
                if self.GetClasse().GetVersionNum() < 7 and self.GetReferentiel().tr_com == [] and code[0] == "B" :
                    code = "S"+code[1:]
                    
                self.savoirs.append(code)
                
#        self.GetPanelPropriete().construire()
#        self.GetPanelPropriete().MiseAJour()
        
    ######################################################################################  
    def TrierCodes(self):
        t = {}
        for d in self.savoirs:
            if d[0] in t.keys():
                t[d[0]].append(d[1:])
            else:
                t[d[0]] = [d[1:]]
                        
        return t
    
    
    
    ######################################################################################  
    def GetCode(self, num = None, cod = None, sep = " - "):
        """ Renvoie le code du Savoir à partir de son num'
            Si num est None : renvoie une chaîne avec tous les codes
        """
        if num is None:
            if cod is None:
                return sep.join(constantes.trier(self.savoirs))
            else:
                c = self.TrierCodes()
                if cod in c.keys():
                    return sep.join(constantes.trier(c[cod]))
                else:
                    return ""
        
        else :
            return self.savoirs[num]
            

    
    ######################################################################################  
    def GetTypCode(self, num):
        return self.savoirs[num][0], self.savoirs[num][1:]
    
    ######################################################################################  
    def GetNomGenerique(self, code = "S"):
        dic = self.GetReferentiel().getDicTousSavoirs()
        return dic[code]._nom.Plur_() + " ("+ dic[code].abrDiscipline+ ")"
    
    ######################################################################################  
    def GetNomGenerique_sing(self, code = "S"):
        dic = self.GetReferentiel().getDicTousSavoirs()
        return dic[code]._nom.sing_()
    
    ######################################################################################  
    def GetDiscipline(self, code):
        dic = self.GetReferentiel().getDicTousSavoirs()
        return dic[code].codeDiscipline
    
#     
# #         print "dicoSavoirs", self.GetReferentiel().dicoSavoirs
#         ref = self.GetReferentiel()
#         dicSavoirs = ref.getTousSavoirs()
#         for code, savoirs in dicSavoirs:
#             if code == self.GetCode(num)[0]:
#                 return savoirs.abrDiscipline
            
            
    ######################################################################################  
    def GetDisciplineNum(self, num):
#         print "dicoSavoirs", self.GetReferentiel().dicoSavoirs
        ref = self.GetReferentiel()
        dicSavoirs = ref.getTousSavoirs()
        for code, savoirs in dicSavoirs:
            if code == self.GetCode(num)[0]:
                return savoirs.abrDiscipline
#         return ref.dicoSavoirs[self.savoirs[num][0]].abrDiscipline
    
    
    ######################################################################################  
    def GetIntit(self, num):
        return self.GetReferentiel().getSavoir(self.GetCode(num)).intitule

    
        ######################################################################################  
    def SignalerPb(self, dif):
        if hasattr(self, 'codeBranche'):
#             print("SignalerPb", dif)
            ref = self.GetReferentiel()
            
                
            if len(dif) > 0:
                # Tri par type de Savoir
                ddif = {}
                for d in dif:
                    if d[0] in ddif.keys():
                        ddif[d[0]].append(d[1:])
                    else:
                        ddif[d[0]] = [d[1:]]
                        
                couleur = "TOMATO1"
                
#                 print("  ", ddif)
                for k, cb in self.codeBranche.items():
#                     print("   ", k)
                    message = "Certains objectifs visés " \
                              "ne sont pas abordés aux cours des %s" %ref._nomActivites.plur_()
                    if k in ddif.keys():
                        if len(ddif[k]) < 4:
                            if len(ddif[k]) > 1:
                                message += "\n"+self.GetNomGenerique(k)+" :"
                            else:
                                message += "\n"+self.GetNomGenerique_sing(k)+" :"
                            for d in ddif[k]:
                                message += "\n"+d
             
                        cb.SetBackgroundColour(couleur)
                        cb.SetToolTip(message)
                        cb.Refresh()
                    
                
            else:
                message = "Tous les objectifs visés" \
                          "sont abordés aux cours des %s" %ref._nomActivites.plur_()
                couleur = COUL_OK
#                 print('   ', self.codeBranche)
                for cb in self.codeBranche.values():
                    cb.SetBackgroundColour(couleur)
                    cb.SetToolTip(message)
                    cb.Refresh()
    
    
    ######################################################################################  
    def SetCodeBranche(self):
        if hasattr(self, 'codeBranche'):
            for k, cb in self.codeBranche.items():
                cb.SetLabel(self.GetCode(cod = k))

            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche, prerequis = False):
#         print("ConstruireArbre Savoirs", prerequis, self)
        self.branche = branche
        ref = self.GetReferentiel()
        doc = self.GetDocument()
        lst = ref.getTousSavoirs()
        if prerequis:
            aff = any([d.pre for k, d in lst])
            ctx = "P"
        else:
            aff = any([d.obj for k, d in lst])
            ctx = "O"
        
#         print "  pre:", [d.pre for k, d in lst], "   obj:", [d.obj for k, d in lst]
        self.codeBranche = {}
        self.branches = {}
        if aff:
            self.arbre = arbre
            
            for k, d in lst:
                if (prerequis and d.pre) or (not prerequis and d.obj):
                    f = doc.GetFiltre(d, ctx,  niveau = 1)
                    if f is None or len(f) > 0:
                        self.codeBranche[k] = CodeBranche(self.arbre, "")
                        self.branches[k] = arbre.AppendItem(branche, self.GetNomGenerique(k), 
                                                           wnd = self.codeBranche[k], 
                                                           data = (self, k, d),
                                                           image = self.arbre.images["Sav"])
                        self.codeBranche[k].SetBranche(self.branches[k])
                        self.arbre.SetItemTextColour(self.branches[k], 
                                                     couleur.GetCouleurWx(COUL_DISCIPLINES[self.GetDiscipline(k)]))
            
            self.SetCodeBranche()
        
    
    #########################################################################
    def GererElementsDependants(self):
        """ Gestion des éléments (Competences, Savoirs, Th, Dom, Spe)
            qui dépendent des savoirs
        """
#         print("GererElementsDependants de", codeComp)
        seq = self.GetDocument()
        seq.GererElementsDependants(self.GetContext())
   
   
   
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'arbre'):
#             del self.branches
            self.ConstruireArbre(self.arbre, self.branche, self.prerequis)
#         if hasattr(self, 'arbre'):
#             for k, b in self.branche.items():
#                 self.arbre.SetItemText(b, self.GetNomGenerique(k))
            
#        self.GetPanelPropriete().MiseAJourTypeEnseignement()
#            self.panelPropriete.construire()
    

    
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.encap_HTML(constantes.BASE_FICHE_HTML_SAV)

    
    ######################################################################################  
    def GetBulleSVG(self, i):
#         print("GetBulleSVG", self, i)

        c = sorted(self.savoirs)[i]
        t = self.GetDisciplineNum(i) + " " + self.GetTypCode(i)[1] + " :\n" + self.GetIntit(i)
        if self.GetDescription() != None:
            t += "\n\n" + self.GetDescription()
        
        return t
    
    
    ######################################################################################  
    def GetBulleHTML(self, i = None, css = False):
#         print("GetBulleHTML", self, i)
        ref = self.GetReferentiel()
        if css:
            t = Template(constantes.TEMPLATE_CMP_SAV_CSS)
        else:
            t = Template(constantes.TEMPLATE_CMP_SAV)
        
        dic = {}
        for i, c in enumerate(sorted(self.savoirs)):
            titre = self.GetNomGenerique(c[0])
            if not (titre in dic):
                dic[titre] = []
            dic[titre].append((self.GetTypCode(i)[1], self.GetIntit(i)))
        
        html = t.render(dic = dic)
        
        return html
    
    
#         ref = self.GetReferentiel()
#         if css:
#             t = Template(constantes.TEMPLATE_CMP_SAV_CSS)
#         else:
#             t = Template(constantes.TEMPLATE_CMP_SAV)
#         lst_sav = []
#         for i, c in enumerate(sorted(self.savoirs)):
#             lst_sav.append((self.GetDisciplineNum(i) + " " + self.GetTypCode(i)[1], 
#                                  self.GetIntit(i)))
#          
#         html = t.render(titre = self.GetNomGenerique(),
#                         lst_sav = lst_sav)
#         return html
    
    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetBulleHTML())
        self.tip.SetPage()
        
#         self.tip.SetHTML(self.GetFicheHTML())
#         nc = self.GetNomGenerique()
#         self.tip.SetWholeText("titre", nc)
#         
#         for i, c in enumerate(sorted(self.savoirs)):
#             self.tip.AjouterElemListeDL("list", 
#                                  self.GetDisciplineNum(i) + " " + self.GetTypCode(i)[1], 
#                                  self.GetIntit(i))
#       
#         self.tip.SetPage()
#         
         
            

####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Seance(ElementAvecLien, ElementBase):
    
                  
    def __init__(self, parent, typeSeance = "", typeParent = 0, branche = None):
        """ Séance :
                parent = le parent wx pour contenir "panelPropriete"
                typeSceance = type de séance parmi "TypeSeance"
                typeParent = type du parent de la séance :  0 = séquence
                                                            1 = séance "Rotation"
                                                            2 = séance "parallèle"
        """
#         self.nom_obj = "Séance"
#         self.article_c_obj = "de la"
#         self.article_obj = "la"
        
        self.parent = parent
        ElementAvecLien.__init__(self)
        ElementBase.__init__(self, tipWidth = 800*SSCALE)
        
        
        ref = self.GetReferentiel()
        Grammaire.__init__(self, ref.nomActivites)
        
        
        
        # Les données sauvegardées
        self.ordre = 0
        self.ordreType = 0
        self.duree = Variable("Durée", lstVal = 1.0, nomNorm = "", typ = VAR_REEL_POS, 
                              bornes = [0.25,30], modeLog = False,
                              expression = None, multiple = False)
        self.intitule  = ""
        self.intituleDansDeroul = True
        self.effectif = 'C'
  
        if self.GetReferentiel().multiDemarches:
            self.demarche = ""
        else:
            self.demarche = 'I'  # Zéro, un ou plusieurs codes de démarche (séparés par espaces)
        
        self.systemes = []  # liste d'objets Variable() dont l'attribut data est un Systeme
        self.ensSpecif = self.GetReferentiel().listeEnsSpecif[:] # liste des enseignements spécifiques concernés par la Seance
        
        self.compVisees = [] # Liste de codes de compétences (code famille + code) visées par la séances
        self.savVises = []  # Liste de codes de savoirs (code famille + code) visés par la séances
        
        self.indicateurs = {} # dictionnaire {code_comp : indicateur de performance
        
        self.code = ""
        self.couleur = (0,0,0,1)
        
        # Une icône et une imagepour illustrer la séance
        self.icone = None
        self.image = None
        
        self.description = None
        self.taille = Variable("Taille des caractères", lstVal = 100, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [10,100], modeLog = False,
                              expression = None, multiple = False)
        
        self.nombre = Variable("Nombre", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [1,50], modeLog = False,
                              expression = None, multiple = False)
        
        self.nbrRotations = Variable("Nombre de rotations", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [1,None], modeLog = False,
                              expression = None, multiple = False)
        
#        self.nbrGroupes = Variable(u"Nombre de groupes", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
#                              bornes = [1,None], modeLog = False,
#                              expression = None, multiple = False)
        
        # Les autres données
        self.typeParent = typeParent
        
#        self.panelParent = panelParent
        
        if branche != None:
            self.setBranche(branche)
        else:
            self.seances = []
            self.SetType(typeSeance)
            self.AjouterListeSystemes(self.GetDocument().systemes)


#     ######################################################################################  
#     def __repr__(self):
#         t = self.code 
# #        t += " " +str(self.GetDuree()) + "h"
# #        t += " " +str(self.effectif)
# #        for s in self.seances:
# #            t += "  " + s.__repr__()
#         return t
    
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Seance(parent, self)
    
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    
    ######################################################################################  
    def GetDocument(self):    
        if self.EstSousSeance():
            return self.parent.GetDocument()
        else:
            return self.parent
    
    ######################################################################################  
    def EstSousSeance(self):
        return not isinstance(self.parent, Sequence)
    
    ######################################################################################  
    def EstSeance_RS(self):
        return hasattr(self, 'typeSeance') \
            and len(self.typeSeance) == 1 \
            and self.typeSeance in "RS"
            
            
    ######################################################################################  
    def GetTypeActivite(self):
        """ Renvoie le type de la première activité parmis les sous séances
        """
        if self.EstSeance_RS() and len(self.seances) > 0:
            return self.seances[0].GetTypeActivite()
        else:
            return self.typeSeance
    
    ######################################################################################  
    def GetCodeEffectifParent(self):
        """ Renvoie le code de l'effectif groupe "parent" de la séance
            (pour R et S : estimation à partie de la 1ère sous séance)
            (TODO : rajouter sélection effectif pour R et S)
        """
        ref = self.GetReferentiel()
#         print("GetCodeEffectifParent", ref.effectifs)
        c = ref.effectifs[self.GetCodeEffectif()][4]
        if c =='':
            return 'C'
        else:
            return c
        
        
        
    ######################################################################################  
    def GetCodeEffectif(self):
        """ Renvoie le code de l'effectif de la séance
            (pour R et S : estimation à partie de la 1ère sous séance)
            (TODO : rajouter sélection effectif pour R et S)
        """
#         print("GetCodeEffectif", self, self.typeSeance)
        
        if self.EstSeance_RS() and len(self.seances) > 0:
            ref = self.GetReferentiel()
            e = ref.effectifs[self.seances[0].effectif][4]
            if e == '':
                return 'C'
            return e
#             return self.seances[0].GetCodeEffectif()
#             return ref.effectifs[self.seances[0].GetCodeEffectif()][4]
        else:
            if self.effectif == '':
                return 'C'
            return self.effectif
    
    
    ######################################################################################  
    def GetListeTypes(self, spe = ""):
        """ Renvoie la liste des types de séance compatibles
            :spe: code de l'enseignement spécifique de la séance
        """
        ref = self.GetReferentiel()
#         print("listeTypeActivite", ref.listeTypeActivite)
        if self.EstSousSeance():
            listType = ref.listeTypeActivite[:]
            if not self.parent.EstSousSeance():
                listType +=  ["S", "R"]
        else:
            listType = ref.listeTypeSeance[:]
#         print("listType", listType)
        return listType
    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la séance pour enregistrement
        """
        ref = self.GetReferentiel()
        root = ET.Element("Seance"+str(self.ordre))
        root.set("Type", self.typeSeance)
        root.set("Intitule", self.intitule)
        root.set("Taille", str(self.taille.v[0]))
        
        self.getBrancheImage(root)
        
        self.getBrancheIcone(root)
        
        if self.description != None:
            root.set("Description", self.description)
        
        root.set("Couleur", Couleur2Str(self.couleur))
        
        self.lien.getBranche(root)
        
        if self.EstSeance_RS():
            for sce in self.seances:
                root.append(sce.getBranche())
            root.set("nbrRotations", str(self.nbrRotations.v[0]))
#            root.set("nbrGroupes", str(self.nbrGroupes.v[0]))
            
        elif self.typeSeance in ref.activites.keys():
            root.set("Demarche", self.demarche)
            root.set("Duree", str(self.duree.v[0]))
            root.set("Effectif", self.effectif)
            root.set("Nombre", str(self.nombre.v[0]))
            
            self.branchesSys = []
            for i, s in enumerate(self.systemes):
                bs = ET.SubElement(root, "Systemes"+str(i))
                self.branchesSys.append(bs)
#                 bs.set("Nom", s.n) # Spprimé depuis v7.1 (liée à la liste des systèmes de la Séquence)
                bs.set("Nombre", str(s.v[0]))
        else:
            root.set("Duree", str(self.duree.v[0]))
            root.set("Effectif", self.effectif)
        
        # Enseignements Spécifiques 
        if len(self.ensSpecif) > 0:
            root.set("EnsSpecif", " ".join(self.ensSpecif))
            
        # Compétences visées
        if len(self.compVisees) > 0:
            root.set("CompVisees", " ".join(self.compVisees))    
            
        # Indicateurs de performance
        brancheIndic = ET.Element("Indicateurs")
        root.append(brancheIndic)
        for c, i in self.indicateurs.items():
            brancheIndic.set(c, i)
            
            
        # Savoirs visés
        if len(self.savVises) > 0:
            root.set("SavVises", " ".join(self.savVises))    
        
        root.set("IntituleDansDeroul", str(self.intituleDansDeroul))
        
        return root    
        
    ######################################################################################  
    def setBranche(self, branche):
#         print("setBranche séance", self)
#        t0 = time.time()
        ref = self.GetReferentiel()
        
        self.ordre = eval(branche.tag[6:])
        
        self.intitule  = branche.get("Intitule", "")
        self.taille.v[0] = eval(branche.get("Taille", "100"))
        self.typeSeance = branche.get("Type", "C")
        self.description = branche.get("Description", None)
        
        self.couleur = Str2Couleur(branche.get("Couleur", "0;0;0;1"))
        
        self.lien.setBranche(branche, self.GetPath())
        
        self.setBrancheIcone(branche)
        
        self.setBrancheImage(branche)
        
#        t1 = time.time()
#        print "    t1", t1-t0
        
        if self.EstSeance_RS():
            self.seances = []
            for sce in list(branche):
                if sce.tag[:6] == "Seance":
                    seance = Seance(self)
                    self.seances.append(seance)
                    seance.setBranche(sce)
            self.duree.v[0] = self.GetDuree()
            if self.typeSeance == "R":
                self.nbrRotations.v[0] = eval(branche.get("nbrRotations", str(len(self.seances))))
#                self.nbrGroupes.v[0] = eval(branche.get("nbrGroupes", str(len(self.Get???))))
                self.reglerNbrRotMaxi()
            
        elif self.typeSeance in ref.activites.keys():   
            self.effectif = branche.get("Effectif", "C")
            self.demarche = branche.get("Demarche", "I")
            self.nombre.v[0] = int(branche.get("Nombre", "1"))
#             print("   ", self.demarche)
#            self.lien.setBranche(branche)
            
            # Les systèmes nécessaires
            lstNSys = []    # Liste des quantité de systèmes nécessaires à la séance
                            # liée à la liste des systèmes de la Séquence
                            # Nouveau depuis v7.1
            for s in list(branche):
                lstNSys.append(int(s.get("Nombre", "0")))  
                    
                
            self.AjouterListeSystemes(lstNSys)#lstSys, 
#             print "   >", lstSys
            # Durée
            self.duree.v[0] = float(branche.get("Duree", "1"))
        else:
            self.effectif = branche.get("Effectif", "C")
            self.duree.v[0] = float(branche.get("Duree", "1"))
        
        if self.effectif == '':
            self.effectif = 'C'
            
        # Enseignements Spécifiques
        self.ensSpecif = branche.get("EnsSpecif", "").split()
#         print("   ensSpecif:", self.ensSpecif)
        
        # Compétences visées
        self.compVisees = branche.get("CompVisees", "").split()
        # On vérifie qu'il n'y en a pas de trop : (BUGFIX)
#         print(self.typeSeance, self.ensSpecif, ":")
        for typ in self.GetDocument().GetTypesCompetencesVisees():
            l = self.GetCompetencesVisables(typ)
#             print("  ", typ, l)
            for c in self.compVisees:
                if c[0] == typ and (l is not None and not c[1:] in l):
                    self.compVisees.remove(c)
        
        # Indicateurs de performance
        brancheIndic = branche.find("Indicateurs")
        self.indicateurs = {}
        if brancheIndic is not None:
            for c, i in brancheIndic.items():
                self.indicateurs[c] = i
        
        
        # Savoirs visés
        self.savVises = branche.get("SavVises", "").split()
                    
        self.intituleDansDeroul = eval(branche.get("IntituleDansDeroul", "True"))
        
        
    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        if hasattr(self, 'pts_caract' ):
            for i, pt in enumerate(self.pts_caract):
                lst.append((pt, self, i))
                
        if self.EstSeance_RS():
            for sce in self.seances:
                lst.extend(sce.GetPtCaract())
                
        self.cadre = []
        
        return lst
    
    ######################################################################################  
    def GetCode(self, num):
        return self.code
    
    ######################################################################################  
    def GetIntit(self, num = None):
        return self.intitule
    
    
    ######################################################################################  
    def EnrichiSVGse(self, doc):
        if self.EstSeance_RS():
            for se in self.seances:
                se.EnrichiSVG(doc, seance = True)
        else:
            self.EnrichiSVG(doc, seance = True)
        
    
    ######################################################################################  
    def EnrichiHTMLse(self, doc):
        if self.EstSeance_RS():
            for se in self.seances:
                se.EnrichiHTML(doc, seance = True)
        else:
            self.EnrichiHTML(doc, seance = True)
            
            
    


    
    
    ######################################################################################  
    def GetEffectif(self):
        """ Renvoie l'effectif de la séance
            :return: float = portion de Classe entière
        """
#         print "GetEffectif", self, self.effectif
        eff = 0
        if self.EstSeance_RS():
            for sce in self.seances:
                eff += sce.GetEffectif() #self.seances[0].GetEffectif()
#        elif self.typeSeance == "S":
#            for sce in self.seances:
#                eff += sce.GetEffectif()
        else:
            eff = self.GetClasse().GetEffectifNorm(self.effectif) * self.nombre.v[0]
        
        return eff
    
    
    
    ######################################################################################  
    def GetNbrSystemesUtil(self):
        return 
    
    
    ######################################################################################  
    def SetEffectif(self, val):
        """ Modifie l'effectif des Rotation et séances en Parallèle et de tous leurs enfants
            après une modification de l'effectif d'un des enfants
            1 = P
            2 = E
            4 = D
            8 = G
            16 = C
        """
#         print("SetEffectif", self, val)#, self.GetReferentiel().effectifs.keys())
        codeEff = None
        if type(val) == int:
            if self.typeSeanc == "R":
                for s in self.seances:
                    s.SetEffectif(val)
#            elif self.typeSeance == "S":
#                self.effectif = self.GetEffectif()
#                self.panelPropriete.MiseAJourEffectif()
            else:
                if val == 16:
                    codeEff = "C"
                elif val == 8:
                    codeEff = "G"
                elif val == 4:
                    codeEff = "D"
                elif val == 2:
                    codeEff = "E"
                elif val == 1:
                    codeEff = "P"
                else:
                    codeEff = "C"
        else:
            codeEff = val
#             for k, v in self.GetReferentiel().effectifs.items():
#                 if v is not None and v[0][:2] == val[:2]: # On ne compare que les 2 premières lettres
#                     codeEff = k
        if codeEff == "":
            codeEff = 'C'
        self.effectif = codeEff
        

    ######################################################################################  
    def VerifPb(self):
#         print("VerifPb séance", self)
        self.SignalerPb(self.IsEffectifOk(), self.IsNSystemesOk())
#        if self.typeSeance in ["R", "S"] and len(self.seances) > 0:
#            for s in self.seances:
#                s.VerifPb()
        
    ######################################################################################  
    def IsEffectifOk(self):
        """ Teste s'il y a un problème d'effectif pour les séances en rotation ou en parallèle
            0 : pas de problème
            1 : tout le groupe "effectif réduit" n'est pas occupé
            2 : effectif de la séance supperieur à celui du groupe "effectif réduit"
            4 : séances en rotation/parallèle d'effectifs différents !!
        """
        
        ok = 0 # pas di problèm'
        
        # effectif séance (portion de Classe entière)
        e = self.GetEffectif()
        # effectif "parent" de la séance (portion de Classe entière)
        ep = self.GetClasse().GetEffectifNorm(self.GetCodeEffectifParent())
        
        
        if self.EstSeance_RS() and len(self.seances) > 0:
#             print("IsEffectifOk", self)
#            print self.GetEffectif() ,  self.GetClasse().GetEffectifNorm('G'),
            eff = round(e, 4)
#             effN = round(self.GetClasse().GetEffectifNorm('G'), 4)  # TODO : revoir ce calcul
            effN = round(ep, 4)
            
            if eff < effN:
                ok |= 1 # Tout le groupe "parent" n'est pas occupé
            elif eff > effN:
                ok |= 2 # Effectif de la séance supperieur à celui du groupe "parent" 
                
            ce = self.seances[0].GetCodeEffectifParent()
            for s in self.seances[1:]:
                if ce != s.GetCodeEffectifParent():
                    ok |= 4
                    break
            
        elif self.typeSeance in self.GetReferentiel().listeTypeActivite and not self.EstSousSeance():
            if e < ep:
                ok |= 1 # Tout le groupe "parent" n'est pas occupé
        
#        print "   ", ok
        return ok


    ######################################################################################  
    def IsNSystemesOk(self):
        """ Teste s'il y a un problème de nombre de systèmes disponibles
        """
        ok = 0 # pas de problème
        if self.typeSeance in self.GetReferentiel().listeTypeActivite:#["AP", "ED"]:
            n = self.GetNbrSystemes()
            seq = self.GetApp().sequence
            for s in seq.systemes:
                if s.nom in n and n[s.nom] > s.nbrDispo.v[0]:
                    ok |= 1
                    break
        return ok


    ######################################################################################  
    def SignalerPb(self, etatEff, etatSys):
        if hasattr(self, 'codeBranche'):
#             print("SignalerPb", self, ":", etatEff, etatSys)
            ref = self.GetReferentiel()
#             etat = max(etatEff, etatSys)
            etat = bin(etatEff).count("1") + bin(etatSys).count("1")
            if etat == 0:
                couleur = 'white'
            elif etat == 1 :
                couleur = COUL_BIEN
            elif etat == 2:
                couleur = COUL_BOF
            elif etat >= 3:
                couleur = "TOMATO1"
            
            ep = self.GetCodeEffectifParent()
            
            
            message = ""
            if etatEff & 1 :
                message += "\nTout le groupe \"%s\" n'est pas occupé" %ref.effectifs[ep][1]
            if etatEff & 2:
                message += "\nEffectif %s supérieur à celui du groupe \"%s\"" %(ref._nomActivites.du_(), ref.effectifs[ep][1])
            if etatEff & 4:
                message += "\nLes effectifs sous-%s ne font pas partie du même groupe !!" %ref._nomActivites.plur_()
            
            
            if etatSys & 1 :
                message += "\nNombre de %s nécessaires supérieur au nombre de %s disponibles." %(ref._nomSystemes.plur_(), ref._nomSystemes.plur_())
                
            
            self.codeBranche.SetBackgroundColour(couleur)
            self.codeBranche.SetToolTip(message[1:])
            self.codeBranche.Refresh()


    ######################################################################################  
    def GetListSousSeancesRot(self, tout = False):
        l = []
        for ss in self.seances:
            for n in range(ss.nombre.v[0]):
                l.append(ss)
#            if not tout :
#                i += ss.nombre.v[0]
#                if i >= self.nbrRotations.v[0]:
#                    break
        if not tout:
            l = l[:self.nbrRotations.v[0]]
        return l


    ######################################################################################  
    def GetProfondeur(self):
        if self.EstSeance_RS():
            return 1+max([s.GetProfondeur() for s in self.seances])
        else:
            return 0
    
    
    ######################################################################################  
    def GetNiveau(self):
        if self.EstSousSeance():
            return 1+self.parent.GetNiveau()
        else:
            return 0
        
        
    ######################################################################################  
    def GetDuree(self):
#        print "GetDuree", self.GetListSousSeancesRot()
        duree = 0
        if self.typeSeance == "R":
#            i = 0
#            for ss in self.seances:
#                duree += ss.GetDuree()
#                i += ss.nombre.v[0]
#                if i >= self.nbrRotations.v[0]:
#                    break
                
                
            for ss in self.GetListSousSeancesRot():
#                sce = self.seances[i]
                duree += ss.GetDuree()
#                print "   ", duree
                
#            for sce in self.seances:
#                duree += sce.GetDuree()
        elif self.typeSeance == "S":
            if len(self.seances) > 0:
                duree += self.seances[0].GetDuree()
        elif self.typeSeance in self.GetReferentiel().listeTypeHorsClasse:
            duree = 0
        else:
            duree = self.duree.v[0]
        return duree


    ######################################################################################  
    def GetDureeGraph(self):
        if self.typeSeance in self.GetReferentiel().listeTypeHorsClasse:
            return 1
        else:
            return self.GetDuree()

           
    ######################################################################################  
    def GetDureeGraphMini(self):
        duree = 10000
        if self.typeSeance == "R":
            for ss in self.GetListSousSeancesRot():
                duree = min(duree, ss.GetDuree())
#            i = 0
#            for ss in self.seances:
#                duree = min(duree, ss.GetDuree())
#                i += ss.nombre.v[0]
#                if i >= self.nbrRotations.v[0]:
#                    break
                
#            for i in range(self.nbrRotations.v[0]):
#                sce = self.seances[i]
#                duree = min(duree, sce.GetDuree())
        elif self.typeSeance == "S":
            if len(self.seances) > 0:
                duree = min(duree, self.seances[0].GetDuree())
        else:
            duree = min(duree, self.duree.v[0])

        return duree


    ######################################################################################  
    def SetDuree(self, duree, recurs = True):
        """ Modifie la durée des Rotation et séances en Parallèle et de tous leurs enfants
            après une modification de durée d'un des enfants
        """
        if recurs and self.EstSousSeance() and self.parent.EstSeance_RS(): # séance en rotation (parent = séance "Rotation")
            self.parent.SetDuree(duree, recurs = False)
        
#        return
#        if self.typeSeance in ["R", "S"]:
#            self.duree.v[0] = duree
            
            
        elif self.typeSeance == "S" : # Serie (parallèle)
            self.duree.v[0] = duree
#            for s in self.seances:
#                if s.typeSeance in ["R", "S"]:
#                    s.SetDuree(duree, recurs = False)
#                else:
#                    s.duree.v[0] = duree
#                    s.panelPropriete.MiseAJourDuree()
#            self.GetPanelPropriete().MiseAJourDuree()

        
        elif self.typeSeance == "R" : # Rotation
#            for s in self.seances:
#                if s.typeSeance in ["R", "S"]:
#                    s.SetDuree(duree, recurs = False)
#                else:
#                    s.duree.v[0] = duree
#                    s.panelPropriete.MiseAJourDuree()
            self.duree.v[0] = self.GetDuree()
#            self.GetPanelPropriete().MiseAJourDuree()

        
    ######################################################################################  
    def SetNombre(self, nombre):
        self.nombre.v[0] = nombre
        if self.EstSousSeance() and self.parent.typeSeance == "R":
            self.parent.reglerNbrRotMaxi()
    
    ######################################################################################  
    def SetTaille(self, nombre):
        self.taille.v[0] = nombre
        
    ######################################################################################  
    def SetNombreRot(self, nombre):
        self.nbrRotations.v[0] = nombre
        self.SetDuree(self.GetDuree())
#        self.GetPanelPropriete().vcNombreRot.mofifierValeursSsEvt()
        
    ######################################################################################  
    def SetIntitule(self, text):           
        self.intitule = text
#        if self.intitule != "":
#            texte = u"Intitulé : "+ "\n".join(textwrap.wrap(self.intitule, 40))
#        else:
#            texte = u""
#        self.tip.SetTexte(texte, self.tip_intitule)
           
    
    ######################################################################################  
    def SetDemarche(self, text):
        """ Applique la(les) démarche(s) à la séance
        """
#         print("SetDemarche", text)
#         ref = self.GetReferentiel()
#         for c, n in list(ref.demarches.items()):
#             if n[1] == text:
#                 codeDem = c
#                 break
        self.demarche = text
        
    
    ######################################################################################  
    def SetEnsSpecif(self, lstCode):   
        self.ensSpecif = lstCode
        # On supprime les compétences visées qui ne sont pas visables
        for typ in self.GetDocument().GetTypesCompetencesVisees():
            l = self.GetCompetencesVisables(typ)
            for c in self.compVisees:
                if c[0] == typ and not c[1:] in l:
                    self.compVisees.remove(c)
                    
                    
        if hasattr(self, 'arbre'):
            self.SetCode()
        
        
    ######################################################################################  
    def SetType(self, typ):
#         print "SetType", typ, self.seances
        if type(typ) == str or type(typ) == str:
            self.typeSeance = typ
        else:
            self.typeSeance = self.GetReferentiel().listeTypeSeance[typ]
        
        if self.EstSeance_RS() and not hasattr(self, 'seances'):
            self.seances = []
        
        if hasattr(self, 'arbre'):
            self.SetCode()
            
        if self.EstSeance_RS() and len(self.seances) == 0: # Rotation ou Serie
            self.AjouterSeance()
        
        
#        try:
#            self.GetPanelPropriete().AdapterAuType()
#        except AttributeError:
#            pass
            
        
        if self.EstSousSeance() and self.parent.EstSeance_RS():
            try: # Pas terrible mais pas trouvé mieux
                self.parent.SignalerPb(self.parent.IsEffectifOk(), 0)
            except:
                pass
        
        if self.typeSeance in self.GetReferentiel().listeTypeActivite:#["AP","ED"]:
            self.SignalerPb(0, self.IsNSystemesOk())
            
        if hasattr(self, 'arbre'):
            self.arbre.SetItemImage(self.branche, self.arbre.images[self.typeSeance])
            self.arbre.Refresh()


    ######################################################################################  
    def GetToutesSeances(self):
        l = []
        if self.EstSeance_RS() : # Séances en Rotation ou  Parallèle
            l.extend(self.seances)
            for s in self.seances:
                l.extend(s.GetToutesSeances())
        return l


    ######################################################################################  
    def PubDescription(self):
        """ Publie toutes les descriptions de séance
            (à l'ouverture)
        """
#        self.tip.SetRichTexte()
#        self.GetPanelPropriete().rtc.Ouvrir()
        
        if self.EstSeance_RS():
            for sce in self.seances:
                sce.PubDescription() 
                

    ######################################################################################  
    def SetCodeBranche(self):
        
        if hasattr(self, 'codeBranche') and self.typeSeance != "":
            self.codeBranche.SetLabel(self.code)
            self.arbre.SetItemText(self.branche, self.GetReferentiel().seances[self.typeSeance][0])
            self.codeBranche.SetToolTip(self.intitule)
            
            
    ######################################################################################  
    def aEnsSpe(self):
        ref = self.GetReferentiel()
        if self.typeSeance in ref.ensSpecifSeance.keys(): # La Seance est concernée par les Enseignements Spécifiques
            for s in self.GetDocument().classe.specialite:
                if s in ref.ensSpecifSeance[self.typeSeance]:
                    return True
        return  False
                 
                  
    ######################################################################################  
    def SetCode(self):
        self.code = self.typeSeance
        num = str(self.ordreType+1)
        
        if isinstance(self.parent, Seance):
            num = str(self.parent.ordreType+1)+"."+num
            if isinstance(self.parent.parent, Seance):
                num = str(self.parent.parent.ordreType+1)+"."+num

        self.code += num
        
        ref = self.GetReferentiel()
        if self.aEnsSpe(): # La Seance est concernée par les Enseignements Spécifiques
            if len(self.ensSpecif) > 0:
                self.code += " - " + " ".join(self.ensSpecif)

        self.SetCodeBranche()
        
        if self.EstSeance_RS() and hasattr(self, 'seances'): # Séances en Rotation ou  Parallèle
            for sce in self.seances:
                sce.SetCode()
            
            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre, self.code)
        if self.typeSeance != "":
            image = self.arbre.images[self.typeSeance]
        else:
            image = -1
        
        self.branche = arbre.AppendItem(branche, self.GetReferentiel()._nomActivites.Sing_()+" :", 
                                        wnd = self.codeBranche, 
                                        data = self, image = image)
        self.codeBranche.SetBranche(self.branche)
        
        if hasattr(self, 'branche'):
            self.SetCodeBranche()
            
        if self.EstSeance_RS() : # Séances en Rotation ou  Parallèle
            for sce in self.seances:
                sce.ConstruireArbre(arbre, self.branche)
            
        
    ######################################################################################  
    def OrdonnerSeances(self):
#         print("OrdonnerSeances", self, self.typeSeance)
        listeTypeSeance = self.GetReferentiel().listeTypeSeance
        dicType = {k:0 for k in listeTypeSeance}
        dicType[''] = 0
        RS = 0
        if self.EstSeance_RS() : # Séances en Rotation ou  Parallèle
            for i, sce in enumerate(self.seances):
                sce.ordre = i
                if sce.typeSeance in ['R', 'S']:
                    sce.ordreType = RS
                    RS += 1
                else:
                    sce.ordreType = dicType[sce.typeSeance]
                    dicType[sce.typeSeance] += 1
                sce.OrdonnerSeances()
        
        self.SetCode()


    ######################################################################################  
    def CollerElem(self, event = None, item = None, bseance = None):
        """ Colle la séance présente dans le presse-papier (branche <bseance>)
            après la séance désignée par l'item d'arbre <item>
        """
#        print "CollerElem"
        seance_avant = self.arbre.GetItemPyData(item)
#        print "   ", seance_avant
        
        if not isinstance(seance_avant, Seance):
            return
        
        if bseance == None:
            bseance = GetObjectFromClipBoard('Seance')
            if bseance == None:
                return
        
#        print "CollerElem", ET.tostring(bseance)
#        print u"   après :", seance_avant
        
        typeSeance = bseance.get("Type", "")
        
        
        if seance_avant.typeSeance in ['R', 'S']:
#            print "     dans :"
            seance = Seance(seance_avant, typeSeance = typeSeance,
                            branche = bseance)
            seance_avant.seances.insert(0, seance)
            
        else:
#            print "     après :"
            seance = Seance(self.parent, typeSeance = typeSeance,
                            branche = bseance)
            i = seance_avant.parent.seances.index(seance_avant)
            seance_avant.parent.seances.insert(i+1, seance)
        
        seq = self.GetDocument()
        
        seq.OrdonnerSeances()
#        seance.ConstruireArbre(self.arbre, seq.brancheSce)
        seq.reconstruireBrancheSeances(seance_avant, seance)
        
#        seance.panelPropriete.MiseAJour()
#        seance.panelPropriete.MiseAJourListeSystemes()
        
        self.GetApp().sendEvent(modif = "Collé d'un élément")
        
        wx.CallAfter(self.arbre.SelectItem, seance.branche)        


    ######################################################################################  
    def AjouterSeance(self, event = None):
        """ Ajoute une séance à la séance
            !! Uniquement pour les séances de type "Rotation" ou "Serie" !!
        """
        seance = Seance(self)
        if self.EstSeance_RS() : # Séances en Rotation ou  Parallèle
            self.seances.append(seance)
            
        self.OrdonnerSeances()
        seance.ConstruireArbre(self.arbre, self.branche)
        self.arbre.Expand(self.branche)
        
        if self.typeSeance == "R":
            seance.SetDuree(self.seances[0].GetDuree())
            self.SetNombreRot(self.GetNbrSSeancesRotation())
            self.reglerNbrRotMaxi()
        else:
            seance.SetDuree(self.GetDuree())
        
        self.GetDocument().VerifPb()
        
        wx.CallAfter(self.arbre.SelectItem, seance.branche)


    ######################################################################################  
    def SupprimerSeance(self, event = None, item = None):
        if self.EstSeance_RS() : # Séances en Rotation ou  Parallèle
            if len(self.seances) > 1: # On en laisse toujours une !!
                seance = self.arbre.GetItemPyData(item)
                self.seances.remove(seance)
                self.arbre.Delete(item)
                self.OrdonnerSeances()
                self.GetDocument().VerifPb()
                self.GetApp().sendEvent(modif = "Suppression d'une Séance")
            
            if self.typeSeance == "R":  # Séances en Rotation
                self.reglerNbrRotMaxi()
        return
    
    
    ######################################################################################  
    def SupprimerSousSeances(self):
        self.arbre.DeleteChildren(self.branche)
        self.seances = []
#         self.GetDocument().VerifPb()
        
    
    ######################################################################################  
    def reglerNbrRotMaxi(self):
        n = self.GetNbrSSeancesRotation()
#        print "reglerNbrRotMaxi", self, ":", n
        self.nbrRotations.bornes[1] = n
        if self.nbrRotations.v[0] > n:
            self.SetNombreRot(n)
    
    
    ######################################################################################  
    def GetNbrSSeancesRotation(self):
        n = 0
        for s in self.seances:
            n += s.nombre.v[0]
        return n

    
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if self.EstSeance_RS():
            for s in self.seances:
                s.MiseAJourTypeEnseignement()
        else:
            if not self.GetReferentiel().multiDemarches:
                if len(self.demarche) == 0:
                    self.demarche = "I"
                elif len(self.demarche.split()) > 0:
                    self.demarche = self.demarche.split()[0]
                
                
#             if self.GetReferentiel().multiDemarches:
#                 self.demarche = ""
#             else:
                  # Zéro, un ou plusieurs codes de démarche (séparés par espaces)
#         print("MiseAJourTypeEnseignement", self.demarche)
#         self.ensSpecif = self.GetReferentiel().listeEnsSpecif[:] # liste des enseignements spécifiques concernés par la Seance
        
#        else:
#            self.GetPanelPropriete().MiseAJourTypeEnseignement()
        
    ######################################################################################  
    def MiseAJourNomsSystemes(self):
        if self.typeSeance in ACTIVITES:
            sequence = self.GetDocument()
            for i, s in enumerate(sequence.systemes):
                self.systemes[i].n = tronquer(s.nom, 20)
#            self.nSystemes = len(sequence.systemes)
#            self.GetPanelPropriete().MiseAJourListeSystemes()
                                 
        elif self.EstSeance_RS() : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.MiseAJourNomsSystemes()
        
    ######################################################################################  
    def SupprimerSysteme(self, i):
        if self.typeSeance in ACTIVITES:
            del self.systemes[i]
#            self.GetPanelPropriete().ConstruireListeSystemes()
        elif self.EstSeance_RS() : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.SupprimerSysteme(i)

        
        
    ######################################################################################  
    def AjouterSysteme(self, systeme, nombre = 0, construire = True):
        """ Ajoute une Variable de gestion du nombre de systèmes nécessaires à la Séance
            
            Se propage aux sous Séances ...
            
        """
        #nom = u"Nouveau système"
        nom = tronquer(systeme.nom, 20)
        if self.typeSeance in ACTIVITES:
            self.systemes.append(Variable(nom, lstVal = nombre, nomNorm = "", typ = VAR_ENTIER_POS, 
                                          bornes = [0,9], modeLog = False,
                                          expression = None, multiple = False,
                                          data = systeme))
#            if construire:
#                self.GetPanelPropriete().ConstruireListeSystemes()
                
        elif self.EstSeance_RS() : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.AjouterSysteme(systeme, nombre)
    
    
    ######################################################################################  
    def AjouterListeSystemes(self, lstNSys = None):
        """
        """
#         print("  AjouterListeSystemes", self.typeSeance, lstNSys)
        lstSys = self.GetDocument().systemes
#         print("    ", lstSys)
        if self.typeSeance in ACTIVITES:
            if lstNSys == [] or lstNSys == None:
                lstNSys = [0]*len(lstSys)
            for i, s in enumerate(lstSys):
#                 print("    ", s.nom)
                self.AjouterSysteme(s, lstNSys[i], construire = False)
#            self.GetPanelPropriete().ConstruireListeSystemes()
            
        elif self.EstSeance_RS() : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.AjouterListeSystemes(lstNSys) 
                
                
    
    ######################################################################################  
    def GetCompetencesVisables(self, typ):
        """ Renvoie l'ensemble des compétences qui sont "visables" par la séance
            sous forme de liste de codes de compétences
            (liste complète, avec tous les enfants "visables" des parents)
            :typ: la famille de compétences : "S", ...
        """
        ref = self.GetReferentiel()
        return  self.GetDocument().GetFiltre(ref.getToutesCompetencesDict()[typ], "O", self)
   
    
    
    ######################################################################################  
    def GetReferentiel(self):
        return  self.GetDocument().GetReferentiel()
        
    ######################################################################################  
    def GetClasse(self):
        return self.GetDocument().classe
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
#         print("AfficherMenuContextuel", itemArbre)
        ref = self.GetReferentiel()
        if itemArbre == self.branche:
#             print("supp", itemArbre, id(self.arbre.GetItemPyData(itemArbre)))
            listItems = [["Supprimer "+self.code, 
                          functools.partial(self.parent.SupprimerSeance, item = itemArbre), 
                          scaleImage(images.Icone_suppr_seance.GetBitmap())],
                         ["Créer un lien", 
                          self.CreerLien, 
                          scaleImage(images.Icone_lien.GetBitmap())]]
            
            if self.EstSeance_RS():
                listItems.append(["Ajouter %s" %ref._nomActivites.un_(), 
                                  self.AjouterSeance, 
                                  scaleImage(images.Icone_ajout_seance.GetBitmap())])
            
            listItems.append(["Copier", 
                              self.CopyToClipBoard, 
                              getIconeCopy()])
            
            ################
            elementCopie = GetObjectFromClipBoard('Seance')
            if elementCopie is not None:
                dataSource = Seance(self.parent)
                dataSource.setBranche(elementCopie)
                
                if not hasattr(self, 'GetNiveau') or self.GetNiveau() + dataSource.GetProfondeur() > 2:
                    return
                
                t = "Coller "
                if self.EstSeance_RS() : # la phase est la même
                    t += "dans"
                else:
                    t += "après"
                listItems.append([t, functools.partial(self.CollerElem, 
                                                        item = itemArbre, 
                                                        bseance = elementCopie),
                                  getIconePaste()])
                            
            self.GetApp().AfficherMenuContextuel(listItems)                      

            
    ######################################################################################  
    def GetNbrSystemes(self, complet = False, simple = False, niveau = None):
        """ Renvoie un dictionnaire :
                clef : nom du système
                valeur : nombre d'exemplaires de ce système utilisés dans la séance
        """
        def up(d, k, v):
            if k in d:
                d[k] += v
            else:
                d[k] = v
                
        d = {}
        if self.typeSeance in ["S", "R"]:
            if self.typeSeance == "S" or complet:
                
                for seance in self.seances:
                    dd = seance.GetNbrSystemes(complet, niveau = niveau)
                    for k, v in dd.items():
                        up(d, k, v)

            else:
                for s in self.systemes:
                    if s.data.nom !="" and (niveau is None or niveau == s.data.GetNiveau()):
                        up(d, s.data.nom, s.v[0]*self.nombre.v[0])
#                        d[s.n] = s.v[0]*self.nombre.v[0]
        else:
            for s in self.systemes:
#                 print "      ", s.data.nom
                if s.data.nom !="" and (niveau is None or niveau == s.data.GetNiveau()):
                    if simple:
                        up(d, s.data.nom, s.v[0])
                    else:
                        up(d, s.data.nom, s.v[0]*self.nombre.v[0])        
        return d



    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.BASE_FICHE_HTML_SEANCE
#         return constantes.encap_HTML(constantes.BASE_FICHE_HTML_SEANCE)


    ######################################################################################  
    def GetBulleHTML(self, i = None, css = False):
        """ Renvoie le tootTip sous la forme HTML
            pour affichage sur la fiche HTML (template "_CSS")
            ou sur la fiche pySéquence (template par défaut)
            
        """
#         print("GetBulleHTML séance", self, i)
        ref = self.GetReferentiel()

        
        if css:
            t = Template(constantes.TEMPLATE_SEANCE_CSS)
        else:
            t = Template(constantes.TEMPLATE_SEANCE)
        
        lst_dem = []
        if self.typeSeance in ref.activites.keys():
            for d in self.demarche.split():
                if css:
                    icon_dem = b64(constantes.imagesDemarches[d].GetData())
                else:
                    icon_dem = self.tip.GetImgURL(constantes.imagesDemarches[d].GetBitmap(), width = 60*SSCALE)
                lst_dem.append((icon_dem,
                                ref.demarches[d][1])
                              )
        
        lst_ensSpe = []
        
        if self.aEnsSpe(): # La Seance est concernée par les Enseignements Spécifiques
            for d in self.ensSpecif:
#                     print(ref.ensSpecif[d][3], couleur.GetCouleurHTML(ref.ensSpecif[d][3]))
                lst_ensSpe.append((d, wx.Colour(*ref.ensSpecif[d][3]).GetAsString(wx.C2S_CSS_SYNTAX)))
    
        
        
        
        if css:
            icon_type = b64(constantes.imagesSeance[self.typeSeance].GetData())
            if self.image is not None:
                image = b64(self.image.GetData())
            else:
                image = None
            
        else:
            icon_type = self.tip.GetImgURL(constantes.imagesSeance[self.typeSeance].GetBitmap())
            image = self.tip.GetImgURL(self.image, width = 200)
            
#         print(lst_ensSpe)    
#         print("   self.compVisees", self.compVisees)
        lstCompVisees = []
        comp = self.GetDocument().obj["C"]
        for i, c in enumerate(sorted(comp.competences)):
#             print("   ", c)
            if c in self.compVisees:
#                 lstCompVisees.append((c[1:], 
#                                       ref.getCompetence(c).intitule,
#                                       self.indicateurs[c]))
                
                for sc in ref.getSousElem(c, "Comp_"+c[0]):
                    if sc in self.indicateurs:
                        indic = self.indicateurs[sc]
                    else:
                        indic = ""
                    lstCompVisees.append((sc[1:], 
                                          ref.getCompetence(sc).intitule,
                                          indic))
        
#         print("lstCompVisees", lstCompVisees)
        
        lstSavVises = []
        sav = self.GetDocument().obj["S"]
        for i, c in enumerate(sorted(sav.savoirs)):
            if c in self.savVises:
                lstSavVises.append((c[1:], ref.getSavoir(c).intitule))
        
        
        html = t.render(titre = ref._nomActivites.Sing_()+" "+ self.code,
                        nom_type = ref.seances[self.typeSeance][1],
                        coul_type = couleur.GetCouleurHTML(draw_cairo_seq.BCoulSeance[self.typeSeance]),
                        icon_type = icon_type,
                        lst_dem = lst_dem,
                        lst_ensSpe = lst_ensSpe,
                        image = image,
                        intitule = self.intitule,
                        duree = getHoraireTxt(self.GetDuree()),
                        effectif = self.GetDocument().classe.GetStrEffectifComplet(self.effectif),
                        coul_eff = couleur.GetCouleurHTML(ref.effectifs[self.effectif][3]),
                        decription = XMLtoHTML(self.description),
                        lien = self.lien,
                        nom_du_activite = ref._nomActivites.du_(),
                        compVisees = lstCompVisees,
                        nomCompVisees = comp.GetNomGenerique(),
                        savVises = lstSavVises,
                        nomSavVises = sav.GetNomGenerique(),
                        #savVises = savVises
                        
                        )
    
        return html


    ######################################################################################  
    def GetBulleSVG(self, i):
        """ Renvoie le tootTip sous la forme d'un texte brut
            pour affichage sur la fiche SVG
        """
        
#        if hasattr(self, 'description'):
#            des = "\n\n" + self.GetDescription()
        
        ref = self.GetReferentiel()
        t = self.GetCode(i) + " :\n" + self.GetIntit(i)  
        if self.GetDescription() != None:
            t += "\n\nDescription :\n" + self.GetDescription()
        
        if self.typeSeance in ref.activites.keys():
            if len(self.demarche) > 0:
                if len(self.demarche) > 1:
                    t += "\n\n" + ref._nomDemarches.Plur_()
                else:
                    t += "\n\n" + ref._nomDemarches.Sing_()
                t += " " + ref._nomActivites.du_() + " :"
                for d in self.demarche.split():
                    t += "\n  " + ref.demarches[d][1]
                
        if self.aEnsSpe(): # La Seance est concernée par les Enseignements Spécifiques
            t += "\n\n" + ref._nomEnsSpecif.Plur_()
            for d in self.ensSpecif:
                t += "  " + d
                    
        t += "\n\n" + "Durée : " + getHoraireTxt(self.GetDuree())
        
        t += "\n" + "Effectif : " + self.GetDocument().classe.GetStrEffectifComplet(self.effectif)
                    
#         print("ttt", type(t))
        return t#.encode(SYSTEM_ENCODING)#.replace("\n", "&#10;")#"&#xD;")#
    
    
    ######################################################################################  
    def SetTip(self):
        """ Construction du toolTip (format HTMLwindow)
            qui apparait dans pySéquence
        """
        self.tip.SetHTML(self.GetBulleHTML())
        self.tip.SetPage()
        
    
    
    
    
    
        
#         self.tip.SetHTML(self.GetFicheHTML())
#         ref = self.GetReferentiel()
# #         titre = "Séance "+ self.code
#         titre = ref._nomActivites.sing_()+" "+ self.code
#         self.tip.SetWholeText("titre", titre)
#         
#         # Type de séance
#         if self.typeSeance != "":
#             self.tip.AjouterImg("icon", constantes.imagesSeance[self.typeSeance].GetBitmap())
#             self.tip.SetWholeText("txt", ref.seances[self.typeSeance][1], 
#                                   bold = True, size = 3,
#                                   fcoul = couleur.GetCouleurHTML(draw_cairo_seq.BCoulSeance[self.typeSeance]))
#         
#         else:
#             self.tip.Supprime('icon')
#         
#         
#         
#         # Démarche
#         ld = self.demarche.split()
#         if self.typeSeance in ref.activites.keys() and len(ref.listeDemarches) > 0 \
#             and len(ld) > 0:
# #             if self.demarche in constantes.imagesDemarches.keys():
#             for i, d in enumerate(ld):
#                 bmp = constantes.imagesDemarches[d].GetBitmap()
#             
#             
#                 self.tip.AjouterImg("icon2", constantes.imagesDemarches[self.demarche].GetBitmap(), width = 64)
#                 self.tip.SetWholeText("dem", ref.demarches[self.demarche][1], italic = True, size = 3)
#         else:
#             self.tip.Supprime('icon2')
#         
#         # Intitulé
#         self.tip.SetWholeText("int", self.intitule, size = 5)
#         
#         
#         # Image
#         if self.image is not None:
#             self.tip.AjouterImg("img", self.image, width = 200)
#         else:
#             self.tip.Supprime('img')
#         
#         # Durée
#         self.tip.SetWholeText("dur", getHoraireTxt(self.GetDuree()), size = 3)
#         
#         # Effectif
#         self.tip.SetWholeText("eff", strEffectifComplet(self.GetDocument().classe, self.effectif), size = 3)
#         
#         # Description
#         if hasattr(self, 'description'):
#             self.tip.AjouterHTML("des", XMLtoHTML(self.description))    
#         else:
#             self.tip.Supprime('ldes')
#         
#         self.tip.AjouterLien('lien', self.lien, self)
#         
#         self.tip.SetPage()
#         
#         


####################################################################################
#
#   Classe définissant les propriétés d'une Fonction de Service
#
####################################################################################
class FonctionService(ElementAvecLien, ElementBase):
                  
    def __init__(self, projet, intitule = "", typ = 0,
                 branche = None):
        """ Fonction de Service :
                
        """
        self.projet = projet
        ElementAvecLien.__init__(self)
        ElementBase.__init__(self, 500*SSCALE)
        
        ref = self.GetReferentiel()
        Grammaire.__init__(self, ref.nomFS)
        
        self.intitule  = intitule
        
        # Les élèves concernés (liste d'élèves)
        self.eleves = []        
    
        # Le code de la fonction
        self.code = "FS"
        
        # La description de la fonction
        self.description = None
        
        # Type de FS : 0 = FP ; 1 = FC
        self.type = typ

        # Une icône pour illustrer la fonction
        self.icone = None
        self.image = None
        
#        
        if branche != None:
            self.setBranche(branche)
        

    ######################################################################################  
    def GetApp(self):
        return self.projet.GetApp()
    
    ######################################################################################  
    def GetDocument(self):    
        return self.projet
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_FS(parent, self)
    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la fonction pour enregistrement
        """
        root = ET.Element("FS"+str(self.GetOrdre()))
        root.set("Intitule", self.intitule)
        
        root.set("Type", str(self.type))

        self.lien.getBranche(root)
        
        if self.description != None:
            root.set("Description", self.description)
        
        self.getBrancheIcone(root)
        
        self.getBrancheImage(root)
        
        return root    
    
    
    ######################################################################################  
    def setBranche(self, branche):
        """
        """
        Ok = True

        self.intitule  = branche.get("Intitule", "")

        self.type = int(branche.get("Type", "0"))
                        
        self.description = branche.get("Description", None)
        
        self.lien.setBranche(branche, self.GetPath())
        
        Ok = Ok and self.setBrancheImage(branche)
        
        self.setBrancheIcone(branche)
        
        return Ok
    

    ######################################################################################  
    def SetIntitule(self, text):           
        self.intitule = text
        self.SetCode()


    ######################################################################################  
    def SetType(self, t):
        self.type = t
        self.GetDocument().OrdonnerFS()
        
        
        
    ######################################################################################  
    def SetCode(self):
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, self.GetCode())
            self.arbre.SetItemBold(self.branche, self.type == 0)
            self.codeBranche.SetLabel(self.intitule)
    
    
    ######################################################################################  
    def GetOrdre(self):
        try:
            return self.GetDocument().fct_serv.index(self)
        except:
            return len(self.projet.fct_serv) # En dernier !!
        
         
    ######################################################################################  
    def GetCode(self):
        if self.type == 0:
            code = "FP"
        else:
            code = "FC"
        num = str(1+self.GetOrdre())
        
        return code + num + " :"
        
        
        
    ######################################################################################  
    def GetIcone(self):
        image = self.arbre.images[self.code]
        return image
    
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre, self.code)
        image = self.GetIcone()
            
        self.branche = arbre.AppendItem(branche, "", wnd = self.codeBranche, 
                                        data = self, image = image)
        self.SetCode()
        self.codeBranche.SetBranche(self.branche)
        

    
    
    
    
####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Tache(ElementAvecLien, ElementBase):
                  
    def __init__(self, projet, intitule = "", phaseTache = "", duree = 1.0, branche = None):
        """ Séance :
                panelParent = le parent wx pour contenir "panelPropriete"
                phaseTache = phase de la tache parmi 'Ana', 'Con', 'Rea', 'Val'
        """
#        print "__init__ tâche", phaseTache
#         self.nom_obj = "Tâche"
#         self.article_c_obj = "de la"
#         self.article_obj = "la"
        
        self.projet = projet
        ElementAvecLien.__init__(self)
        ElementBase.__init__(self, 500*SSCALE)
#         self.tip.SetSize((, -1))
        
        ref = self.GetReferentiel()
        Grammaire.__init__(self, ref.nomTaches)
        
        
        # Les données sauvegardées
        self.ordre = 100
        self.duree = Variable("Volume horaire (h)", lstVal = duree, nomNorm = "", typ = VAR_REEL_POS, 
                              bornes = [0.5,40], modeLog = False,
                              expression = None, multiple = False)
        self.intitule  = intitule
        self.intituleDansDeroul = True
        
        # Les élèves concernés (liste d'élèves)
        self.eleves = []        
        self.impEleves = []   # taux d'implication des élèves dans la tâche

        # Le code de la tâche (affiché dans l'arbre et sur la fiche
        self.code = ""
        
        # La description de la tâche
        self.description = None

        # Une icône pour illustrer la tâche
        self.icone = None
        self.image = None
        
        # Les autres données
#        self.panelParent = panelParent
        
        self.phase = phaseTache
        
        self.compVisees = [] # codes des compétences visées (uniquement pour projest non évalués)
        self.savVises = []
        
        if branche != None:
            self.setBranche(branche)
##            if not Ok:
##                self.code = -err # Pour renvoyer une éventuelle erreur à l'ouverture d'un fichier
        else:
#        if branche == None:
            self.indicateursEleve = self.IndicateursEleveDefaut()
            if phaseTache in TOUTES_REVUES_SOUT:
                self.indicateursMaxiEleve = self.IndicateursEleveDefaut()
                
    
    ######################################################################################  
    def __eq__(self, tache):
        return isinstance(tache, Tache) \
            and tache is not None \
            and self.code == tache.code and self.ordre == tache.ordre
  
    
    ######################################################################################  
    def __repr__(self):
#        t = self.phase + str(self.ordre+1) 
#        t += " " +str(self.GetDuree()) + "h"
#        t += " " +str(self.effectif)
#        for s in self.seances:
#            t += "  " + s.__repr__()
        return self.code +" ("+str(self.ordre)+") "+ self.phase
    
    
    ######################################################################################  
    def GetApp(self):
        return self.projet.GetApp()

    ####################################################################################
    def EstMovable(self):
        return True
    
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Tache(parent, self)
    
    ######################################################################################  
    def ActualiserDicIndicateurs(self):
        """ Complète le dict des compétences/indicateurs globaux (tous les élèves confondus)
        """
#        print "ActualiserDicIndicateurs", self
        prj = self.GetProjetRef()
        if prj is not None and not prj._pasdIndic:
            for i in range(len(self.projet.eleves)):
                for c in self.indicateursEleve[i+1]:
                    if not c in self.indicateursEleve[0]:
                        self.indicateursEleve[0].append(c)


    ######################################################################################  
    def estPredeterminee(self):
        prj = self.GetProjetRef()
        if prj is None:
            return False
        return len(prj.taches) > 0 
            
    
    ######################################################################################  
    def estACocherIndic(self, codeIndic):
        """ Renvoie True si l'indicateur <codeIndic> doit être "à cocher"
        """
        prj = self.GetProjetRef()
        return ((not self.phase in [_R1,_R2, _Rev, self.projet.getCodeLastRevue()]) \
                 or (codeIndic in self.indicateursMaxiEleve[0])) \
               and prj.phaseDansPartie(self.phase,
                                       prj.getTypeIndicateur(codeIndic)) #prj.getTypeIndicateur(codeIndic) == "S" or self.phase != 'XXX')


    ######################################################################################  
    def GetDicIndicateurs(self):
        """Renvoie l'ensemble des indicateurs de compétences à mobiliser pour cette tâche
            Dict :  clef = code compétence
            valeur = liste [True False ...] des indicateurs à mobiliser
        """
#         print("GetDicIndicateurs", self, ":", self.indicateursEleve)
#        print self.GetProjetRef()._dicoIndicateurs_simple
        if self.GetProjetRef() is None:
            return {}
        
        tousIndicateurs = {}
        for disc, dic in self.GetProjetRef()._dicoIndicateurs_simple.items():
            for k, i in dic.items():
                tousIndicateurs[disc+k] = i
#        print "  >", tousIndicateurs
        
        indicateurs = {}
        for i in self.indicateursEleve[0]:
#            print "   ", i
            cci = i.split('_')
            if len(cci) == 2:
                competence, indicateur = cci
                indicateur = int(eval(indicateur)-1)
                nbrIndic = len(tousIndicateurs[competence])
                if not competence in indicateurs.keys():
                    indicateurs[competence] = [False]*nbrIndic
                indicateurs[competence][indicateur] = True
                    
        if self.GetProjetRef()._pasdIndic:            
            for e in self.compVisees:
                competence = e
                if not competence in indicateurs.keys():
                    indicateurs[competence] = [True]
                
        return indicateurs
    
    
    ######################################################################################  
    def GetDicIndicateursEleve(self, eleve):
        """Renvoie l'ensemble des indicateurs de compétences à mobiliser pour cette REVUE
            Dict :  clef = code type+compétence
            valeur = liste [True False ...] des indicateurs à mobiliser
        """
#        print "GetDicIndicateursEleve", self, eleve.id+1
        indicateurs = {}
        if self.GetProjetRef() is None:
            return {}
        
        numEleve = eleve.id
        for dic in self.GetProjetRef()._dicoIndicateurs_simple.values():
            for i in self.indicateursEleve[numEleve+1]:
                competence, indicateur = i.split('_')
                indicateur = eval(indicateur)-1
                if not competence in indicateurs.keys():
                    indicateurs[competence] = [False]*len(dic[competence[1:]])
                
                indicateurs[competence][indicateur] = True
#        print "  >>", indicateurs
        return indicateurs
    
    ######################################################################################  
    def DiffereSuivantEleve(self):
        """Renvoie True si cette REVUE est différente selon l'élève
            --> épaisseur variable selon le nombre d'élèves
            Renvoie False si tous les élèves abordent les mêmes compétences/indicateurs
            --> épaisseur fixe
            (utilisé pour tracer la fiche uniquement)
        """
#        print "DiffereSuivantEleve", self, self.phase
        if len(self.projet.eleves) == 0:
            return False
        indicateurs = self.GetDicIndicateursEleve(self.projet.eleves[0])
#        print "   ", indicateurs
        for eleve in self.projet.eleves[1:]:
            
            ie = self.GetDicIndicateursEleve(eleve)
#            print "     ", eleve, " >>> ", ie
            if set(indicateurs.keys()) != set(ie.keys()):
#                print "       >1"
                return True
            for k, v in ie.items():
                for a, b in zip(v, indicateurs[k]):
                    if a != b:
#                        print "       >2"
                        return True
#                print set(v) , "------", set(indicateurs[k])
#                if set(v) != set(indicateurs[k]):
#                    print "       >2"
#                    return True
            
        return False
    
    ######################################################################################  
    def GetCompetencesUtil(self):
#        print "GetCompetencesUtil", self.indicateursEleve
        lst = []
        for e in self.indicateursEleve.values():
            for i in e:
                ci = i.split('_')[0]
                if not ci in lst:
                    lst.append(ci)
        
        for e in self.compVisees:
            if not e in lst:
                lst.append(e)
                    
                    
#        for i in self.indicateursEleve[0]:
#            lst.append(i.split('_')[0])
        return lst


    ######################################################################################  
    def GetSavoirsUtil(self):
#        print "GetSavoirsUtil", self.indicateursEleve
        lst = []
        for e in self.indicateursEleve.values():
            for i in e:
                ci = i.split('_')[0]
                if not ci in lst:
                    lst.append(ci)
        
        for e in self.savVises:
            if not e in lst:
                lst.append(e)
                    
                    
#        for i in self.indicateursEleve[0]:
#            lst.append(i.split('_')[0])
        return lst
    
    
    
    ######################################################################################  
    def IndicateursEleveDefaut(self):
        """ Format pour les indicateurs de performance mobilisés par élève
            0 = tous les elèves
            1 = elève 1
            ...
            Chaque liste contient les codes des indicateurs : CodeCompétence_Numéro_Indicateur
        """
        return { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la tâche pour enregistrement
        """
        root = ET.Element("Tache"+str(self.ordre))
        root.set("Phase", self.phase)
        root.set("Intitule", self.intitule)

        self.lien.getBranche(root)
        
        if self.description != None:
            root.set("Description", self.description)
        
        self.getBrancheIcone(root)
        
        self.getBrancheImage(root)
        
        root.set("Duree", str(self.duree.v[0]))
        
        brancheElv = ET.Element("Eleves")
        root.append(brancheElv)
        for i, e in enumerate(self.eleves):
            brancheElv.set("Eleve"+str(i), str(e))
        
        brancheElv = ET.Element("ImplicationEleves")
        root.append(brancheElv)
        for i, e in enumerate(self.impEleves):
            brancheElv.set("Eleve"+str(i), str(e))
        
        if not self.phase in [self.projet.getCodeLastRevue(), "S"]:
            # Structure des indicateurs :
            # <Indicateurs Indic0="CO6.1_1" Indic1="CO6.2_4" ..... />
            #   (compétence_indicateur)
            brancheCmp = ET.Element("Indicateurs")
            root.append(brancheCmp)
            
            if self.projet.nbrRevues == 2:
                lstR = [_R1]
            else:
                lstR = [_R1, _R2]
                    
            if self.phase in lstR or self.estPredeterminee():
                for e, indicateurs in list(self.indicateursEleve.items())[1:]:
                    if e > len(self.projet.eleves):
                        break
                    brancheE = ET.Element("Eleve"+str(e))
                    brancheCmp.append(brancheE)
                    for i, c in enumerate(indicateurs):
                        brancheE.set("Indic"+str(i), c)
                        
            elif not self.phase in TOUTES_REVUES_EVAL:
                for i, c in enumerate(self.indicateursEleve[0]):
                    brancheCmp.set("Indic"+str(i), c)
            
        # Compétences visées
        if len(self.compVisees) > 0:
            root.set("CompVisees", " ".join(self.compVisees))    
            
            
        root.set("IntituleDansDeroul", str(self.intituleDansDeroul))
        return root    
        
    ######################################################################################  
    def setBranche(self, branche):
        """
        """
        err = []
        ref = self.GetProjetRef()
        prjref = self.GetProjetRef()
        self.ordre = eval(branche.tag[5:])
        self.intitule  = branche.get("Intitule", "")
        
        self.phase = branche.get("Phase", "") 

        debug = False#self.phase == "R1"
        if debug: print("setBranche tâche", self.phase)
        
        # Suite commentée ... à voir si pb
#        if self.GetTypeEnseignement() == "SSI":
#            if self.phase == 'Con':
#                self.phase = 'Ana'
#            elif self.phase in ['DCo', 'Val']:
#                self.phase = 'Rea'

        self.description = branche.get("Description", None)
        
        self.lien.setBranche(branche, self.GetPath())
        
        self.setBrancheImage(branche)
        
        self.setBrancheIcone(branche)
                
                
        if not self.phase in TOUTES_REVUES_EVAL_SOUT:
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        else:
            self.duree.v[0] = constantes.DUREE_REVUES
        
        brancheElv = branche.find("Eleves")
        self.eleves = []
        prj = self.GetDocument()
        for i, e in enumerate(brancheElv.keys()):
            if i < len(prj.eleves) + len(prj.groupes):
                self.eleves.append(eval(brancheElv.get("Eleve"+str(i))))
        
        
        brancheElv = branche.find("ImplicationEleves")
        impEleves = []
        if brancheElv != None: ## cas pour Version <= 7.1.12
            prj = self.GetDocument()
            for i, e in enumerate(brancheElv.keys()):
                if i < len(prj.eleves) + len(prj.groupes):
                    impEleves.append(eval(brancheElv.get("Eleve"+str(i), "100")))
        
        # On corrige un éventuel conflit de taille
        self.impEleves = []
        for i in range(len(self.eleves)):
            if len(impEleves) > i:
                self.impEleves.append(impEleves[i])
            else:
                self.impEleves.append(100)
                
                
        # Initialisation des Indicateurs par elève
        self.indicateursEleve = self.IndicateursEleveDefaut() 
        if not self.phase in [self.projet.getCodeLastRevue(), "S"]:
            self.indicateursMaxiEleve = self.IndicateursEleveDefaut()
        
        if self.GetClasse().GetVersionNum() < 5:
            pass # Nouveaux indicateurs STI2D !!
        
        else:
            #
            # pour compatibilité acsendante
            #
            brancheCmp = branche.find("Competences")
            
            if brancheCmp != None: ## ANCIENNE VERSION (<beta6)
                err.append(constantes.Erreur(constantes.ERR_PRJ_T_VERSION))
                
                if self.GetTypeEnseignement() == "SSI":
                    brancheInd = None
                else:
                    brancheInd = branche.find("Indicateurs")
                
                for i, e in enumerate(brancheCmp.keys()):
                    if brancheInd != None: #STI2D
                        i = eval(e[4:])
                        indic = brancheInd.get("Indic"+str(i))
                        if indic != None:
                            lst = toList(indic)
                        elif prjref is not None:
                            lst = [True]*len(prjref._dicIndicateurs[e])
                        else:
                            lst = []
                        for n,j in enumerate(lst):
                            if j:
                                self.indicateursEleve[0].append(brancheCmp.get(e)+"_"+str(n+1))
                    else:
                        indic = brancheCmp.get("Comp"+str(i))
                        self.indicateursEleve[0].append(indic.replace(".", "_"))
                
            
            #
            # A partir de la version 6
            #
            else:
                brancheInd = branche.find("Indicateurs")
                if brancheInd != None:
                    if self.projet.nbrRevues == 2:
                        lstR = [_R1]
                    else:
                        lstR = [_R1, _R2]
                    if debug: print("   1")
                    # 
                    # Indicateurs revue par élève (première(s) revues)
                    #
                    if self.phase in lstR or self.estPredeterminee():
                        for i, e in enumerate(self.projet.eleves):
                            
                            self.indicateursEleve[i+1] = []
                            
                            brancheE = brancheInd.find("Eleve"+str(i+1))
                            if brancheE != None:
                                for c in brancheE.keys():
                                    codeindic = brancheE.get(c)
                                    if self.GetClasse().GetVersionNum() < 7:
                                        codeindic = "S"+codeindic
                                    code, indic = codeindic.split('_')
                                    
                                    # pour compatibilité version < 3.19
                                    if code == "CO8.es":
                                        code = "CO8.0"
                                        codeindic = code+"_"+indic
                                        
                                    disc, code = code[0], code[1:]
                                    
                                    # Si c'est la dernière phase et que c'est une compétence "Conduite" ... on passe
                                    indic = eval(indic)-1
                                    if not prjref.phaseDansPartie(self.phase, prjref.getTypeIndicateur(codeindic)):
#                                     if self.phase == 'XXX' and self.GetReferentiel().getTypeIndicateur(codeindic) == 'C':
                                        continue
                                    
#                                    try:
#                                            print "***",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                                        # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                                        
                                    if prjref is not None and not code in prjref._dicoIndicateurs_simple[disc]:
                                        print("Erreur 1", code, "<>", prjref._dicoIndicateurs_simple[disc])
                                        err.append(constantes.Erreur(constantes.ERR_PRJ_T_TYPENS))
                                        return err
                                    
                                    if debug: print("   ", codeindic)
                                    if not codeindic in self.indicateursEleve[i+1]:
                                        self.indicateursEleve[i+1].append(codeindic)
                                        
#                                    except:
#                                        print "errrrrr"
                            
                            else: # Pour ouverture version <4.8beta1
                                indicprov = []
                                for c in brancheInd.keys():
                                    codeindic = brancheInd.get(c)
                                    if self.GetClasse().GetVersionNum() < 7:
                                        codeindic = "S"+codeindic
                                    code, indic = codeindic.split('_')
                                    
                                    # pour compatibilité version < 3.19
                                    if code == "CO8.es":
                                        code = "CO8.0"
                                        codeindic = code+"_"+indic
                                        
                                    # Si c'est la dernière phase et que c'est une compétence "Conduite" ... on passe
                                    indic = eval(indic)-1
                                    if not prjref.phaseDansPartie(self.phase, prjref.getTypeIndicateur(codeindic)):
#                                     if self.phase == 'XXX' and self.GetReferentiel().getTypeIndicateur(codeindic) == 'C':
                                        continue
                                    
#                                        print "******",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                                        
                                    # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                                    if prjref is not None and not code in prjref._dicIndicateurs:
                                        print("Erreur 2")
                                        err.append(constantes.Erreur(constantes.ERR_PRJ_T_TYPENS))
                                        return err

                                    indicprov.append(codeindic)
                                    dic = e.GetDicIndicateursRevue(self.phase)
                                    
                                    if code in dic.keys():
                                        if dic[code][indic]:
                                            self.indicateursEleve[i+1].append(codeindic)
                                
                    #
                    # Indicateurs tâche
                    #
                    else:
                        for i, e in enumerate(brancheInd.keys()):
                            codeindic = brancheInd.get(e)
                            if self.GetClasse().GetVersionNum() < 7:
                                codeindic = "S"+codeindic
                            code, indic = codeindic.split('_')
#                                print "     ", code, indic
                            # pour compatibilité version < 3.19
                            if code == "CO8.es":
                                code = "CO8.0"
                                codeindic = code+"_"+indic
                                
                            # Si c'est la dernière phase et que c'est une compétence "Conduite" ... on passe
                            indic = eval(indic)-1
                            if not prjref.phaseDansPartie(self.phase, prjref.getTypeIndicateur(codeindic)):
#                             if prjref is not None and self.phase == 'XXX' and prjref.getTypeIndicateur(codeindic) == 'C':
                                continue
                            
                                
#                                try:
#                                    print "******",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                            # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                            if prjref is not None: 
                                for disc, dic in prjref._dicoIndicateurs_simple.items():
                                    if code[0] == disc:
                                        if not code[1:] in dic.keys():
                                            print("Erreur 3", code, "<>", prjref._dicoIndicateurs_simple[disc])
                                            if not constantes.Erreur(constantes.ERR_PRJ_T_TYPENS) in err:
                                                err.append(constantes.Erreur(constantes.ERR_PRJ_T_TYPENS))
                                        else:
                                            self.indicateursEleve[0].append(codeindic)
        
        
#         if debug: 
#         
        
        if not self.estPredeterminee():
            self.ActualiserDicIndicateurs()
#         print("   indicateursEleve", self.indicateursEleve)
        # Compétences visées
        self.compVisees = branche.get("CompVisees", "").split()
#         print("compVisees", self.phase, ":", self.compVisees)
        
        self.intituleDansDeroul = eval(branche.get("IntituleDansDeroul", "True"))
    

        ####################################################################################
#        pp = self.GetPanelPropriete()
#        if pp and not self.phase in TOUTES_REVUES_EVAL_SOUT:
#            pp.ConstruireListeEleves()
#            pp.MiseAJourDuree()
#            pp.MiseAJour()
#            self.panelPropriete.MiseAJourPoidsCompetences()
        
        return err

    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        if hasattr(self, 'pts_caract' ):
            for i, pt in enumerate(self.pts_caract):
                lst.append((pt, self, i))
                
        self.cadre = []
        
        return lst
    
    ######################################################################################  
    def GetCode(self, num):
        return self.code
    
    ######################################################################################  
    def GetIntit(self, num = None):
        if self.GetProjetRef() is not None and self.estPredeterminee() > 0:
            return self.intitule+"\n"+self.GetProjetRef().taches[self.intitule][1]
        else:
            return self.intitule
        

    ######################################################################################  
    def VerifPb(self):
        return

    ######################################################################################  
    def GetDelai(self):
        if self.phase != "":
            if self.phase in TOUTES_REVUES_EVAL:
                de = []
                for e in self.projet.eleves:
                    de.append(e.GetDuree(phase = self.phase, total = True))
                if not de:
                    d = 0
                else:
                    d = max(de)
                return d
            
            elif self.phase in ["Rev"]:
                de = []
                for e in self.projet.eleves:
                    de.append(e.GetDureeJusqua(self))
                if not de:
                    d = 0
                else:
                    d = max(de)
                return d
        return 0
    
    ######################################################################################  
    def GetDuree(self):
        if self.phase != "":
            return self.duree.v[0]
        return 0
                
    ######################################################################################  
    def GetDureeGraph(self):
        return min(self.GetDuree(), 8)       
    
    ######################################################################################  
    def SetDuree(self, duree):
        """ Modifie la durée de la tâche
        """
        self.duree.v[0] = duree
#        self.GetPanelPropriete().MiseAJourDuree()
        self.projet.MiseAJourDureeEleves()
        
    ######################################################################################  
    def SetIntitule(self, text):           
        self.intitule = text
        self.SetCode()
#        if self.intitule != "":
#            t = u"Intitulé : "+ "\n".join(textwrap.wrap(self.intitule, 40))
#        else:
#            t = u""
            
            
        
            
#        self.tip.SetTexte(t, self.tip_intitule)
        
    ######################################################################################  
    def GetProchaineRevue(self):
#        print "GetProchaineRevue"
        if self.GetProjetRef() is None:
            return 0
        
        posRevues = self.GetProjetRef().posRevues[self.projet.nbrRevues]
#        print "   posRevues:", posRevues
        for i, pr in enumerate(posRevues):#.reverse():
#            print "   ", i, pr, self.phase
            if self.phase <= pr:
#                print '    >> R'+str(i+1)
                return i+1
        return 0
            
            
    ######################################################################################  
    def SetPhase(self, phase = None):
#        print "SetPhase", self.phase, ">>", phase
        if phase != None:
            self.phase = phase
        self.projet.OrdonnerTaches()
        
        if hasattr(self, 'arbre'):
            self.SetCode()
            
        if hasattr(self, 'arbre'):
            self.arbre.SetItemImage(self.branche, self.arbre.images[self.phase])
            self.arbre.Refresh()
        
    
#    ######################################################################################  
#    def PubDescription(self):
#        """ Publie toutes les descriptions de tâche
#            (à l'ouverture)
#        """
#        self.tip.SetRichTexte()
#        self.GetPanelPropriete().rtc.Ouvrir()

                
            
    ######################################################################################  
    def SetCode(self):
        i = 0
        for t in self.projet.taches:
            if t.phase == self.phase:
                if t == self:
                    break
                i += 1
        num = str(i+1)
        
        prj = self.GetProjetRef()
        
        if self.phase != "":
            if self.phase in TOUTES_REVUES_EVAL_SOUT:
                self.code = self.phase
            elif prj is not None:
                self.code = prj.phases[self.phase][2]+num     #constantes.CODE_PHASE_TACHE[typeEns][self.phase]+num
            else:
                self.code = num # à vérifier ...
        else:
            self.code = num

        
        #
        # Branche de l'arbre
        #
        if hasattr(self, 'codeBranche') and self.phase != "":
            if self.phase in TOUTES_REVUES_EVAL_SOUT and prj is not None:
                self.codeBranche.SetLabel("")
                code = prj.phases[self.phase][1]
            else:
                if self.estPredeterminee():
                    code = self.intitule
                    intitule = prj.taches[self.intitule][1]
                    
                else:
                    code = self.code
                    intitule = self.intitule
                    
                i = intitule.replace("\n", " - ")
                i = i[:constantes.LONGUEUR_INTITULE_ARBRE]
                if len(intitule) != len(i):
                    i += "..."
                self.codeBranche.SetLabel(i)
                self.codeBranche.SetToolTip(intitule)
                code += " :"
            self.arbre.SetItemText(self.branche, code)#self.GetProjetRef().phases[self.phase][1]+
            self.codeBranche.LayoutFit()
            
        
            
        
            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre, self.code)
        if self.phase != "":
            image = self.arbre.images[self.phase]
        else:
            image = -1
            
        self.branche = arbre.AppendItem(branche, "Tâche :", wnd = self.codeBranche, 
                                        data = self, image = image)
        self.codeBranche.SetBranche(self.branche)
        
        if self.phase in TOUTES_REVUES_EVAL:
            arbre.SetItemTextColour(self.branche, wx.Colour("red"))
        elif self.phase == "Rev":
            arbre.SetItemTextColour(self.branche, wx.Colour("ORANGE"))
        elif self.phase == "S":
            arbre.SetItemTextColour(self.branche, wx.Colour("PURPLE"))
    
    
#    ######################################################################################  
#    def MiseAJourNomsEleves(self):
#        """ Met à jour la liste des élèves concernés par la tâche
#            et la liste des élèves du panelPropriete de la tâche
#        """
#        projet = self.GetDocument()
#        for i, s in enumerate(projet.eleves):
#            self.eleves[i].n = s.nom
#            self.nSystemes = len(sequence.systemes)
#        self.GetPanelPropriete().MiseAJourListeEleves()
                                 
    
    #############################################################################
    def MiseAJourTypeEnseignement(self, ref):
        return
#        self.GetPanelPropriete().MiseAJourTypeEnseignement(ref)
        
    ######################################################################################  
    def SupprimerSysteme(self, i):
        if self.typeSeance in ACTIVITES:
            del self.systemes[i]
#            self.GetPanelPropriete().ConstruireListeSystemes()
        elif self.EstSeance_RS() : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.SupprimerSysteme(i)

        
#     ######################################################################################  
#     def AjouterEleve(self):
#         return
# #        self.GetPanelPropriete().ConstruireListeEleves()
    
    
    ######################################################################################  
    def SupprimerEleve(self, i):
        if i in self.eleves:
            self.eleves.remove(i)

        for i, ident in enumerate(self.eleves):
            if ident > i:
                self.eleves[i] = ident-1

#        self.GetPanelPropriete().ConstruireListeEleves()
        

    ######################################################################################  
    def AjouterCompetence(self, code, propag = True):
#         print "AjouterCompetence !!", self, code
        if not code in self.indicateursEleve[0] and not self.estPredeterminee():
            self.indicateursEleve[0].append(code)

        if propag:
            for i in range(len(self.projet.eleves)):
                if not self.estPredeterminee() or i in self.eleves:
                    self.AjouterCompetenceEleve(code, i+1)
       
#        if not self.estPredeterminee():
        self.projet.SetCompetencesRevuesSoutenance()
        
        
    ######################################################################################  
    def EnleverCompetence(self, code, propag = True):
#         print "EnleverCompetence", self, code
        if code in self.indicateursEleve[0]:
            self.indicateursEleve[0].remove(code)
        # on recommence : pour corriger un bug
        if code in self.indicateursEleve[0]:
            self.indicateursEleve[0].remove(code)
        
        if propag:
            for i in range(len(self.projet.eleves)):
                self.EnleverCompetenceEleve(code, i+1)
    
        self.projet.SetCompetencesRevuesSoutenance()
    
    
    ######################################################################################  
    def AjouterCompetenceEleve(self, code, eleve):
#         print "AjouterCompetenceEleve", code, self.phase
        if hasattr(self, 'indicateursEleve'):
            
            if self.estPredeterminee():
                self.indicateursEleve[eleve].append(code)
                
            else:
                dicIndic = self.projet.eleves[eleve-1].GetDicIndicateursRevue(self.phase)
                comp = code.split("_")[0]
                if comp in dicIndic.keys():
                    if comp != code: # Indicateur seul
                        indic = eval(code.split("_")[1])
                        ok = dicIndic[comp][indic-1]
                else:
                    ok = False
                    
                if ok and not code in self.indicateursEleve[eleve]:
                    self.indicateursEleve[eleve].append(code)
            
#            print "  ", self.tache.indicateursEleve
#                self.tache.ActualiserDicIndicateurs()
            
        
    ######################################################################################  
    def EnleverCompetenceEleve(self, code, eleve):
#        print "EnleverCompetenceEleve", self, code
        
        if hasattr(self, 'indicateursEleve'):
#            print "  ", self.tache.indicateursEleve
            if code in self.indicateursEleve[eleve]:
                self.indicateursEleve[eleve].remove(code)
            # on recommence : pour corriger un bug
            if code in self.indicateursEleve[eleve]:
                self.indicateursEleve[eleve].remove(code)
#            self.tache.ActualiserDicIndicateurs()
#            print "  ", self.tache.indicateursEleve



    ######################################################################################  
    def MiseAJourPoidsCompetences(self, code = None):
        return
#        self.GetPanelPropriete().MiseAJourPoidsCompetences(code)
                
    ######################################################################################  
    def GetDocument(self):    
        return self.projet
    
    ######################################################################################  
    def GetClasse(self):
        return self.GetDocument().classe
    
    ######################################################################################  
    def GetPhaseSuivante(self):
        """ Renvoie la phase de la tâche juste suivante
        """
#         print "GetPhaseSuivante", self.projet.taches
        
        if self.phase in TOUTES_REVUES:   # On est sur une revue
            lstPhases = self.projet.GetListePhases()
            i = lstPhases.index(self.phase)
            return lstPhases[i+1]
        
        else:
            i = self.projet.taches.index(self)
            if len(self.projet.taches) > i+1:   # On est sur une tâche
                return self.projet.taches[i+1].phase


    ######################################################################################  
    def GetTachePrecedente(self):
        """ Renvoie la tâche (pas revue) juste précédente
            "self" si self est déja une tâche
        """
        t = self
        while t.phase in TOUTES_REVUES:
            i = self.projet.taches.index(t)
            if i > 0:
                t = self.projet.taches[i-1]
            else:
                return
        return t
            
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            if not self.phase in TOUTES_REVUES_EVAL_SOUT:
                listItems = [["Supprimer", 
                              functools.partial(self.projet.SupprimerTache, item = itemArbre), 
                              scaleImage(images.Icone_suppr_tache.GetBitmap())]]
            else:
                listItems = []
            listItems.append(["Insérer une revue après", 
                              functools.partial(self.projet.InsererRevue, item = itemArbre), 
                              scaleImage(images.Icone_ajout_revue.GetBitmap())])

            if self.phase not in TOUTES_REVUES_EVAL_SOUT:
                listItems.append(["Copier", 
                                  self.CopyToClipBoard, 
                                  getIconeCopy()])
 
            elementCopie = GetObjectFromClipBoard('Tache')
            if elementCopie is not None:
                phase = elementCopie.get("Phase", "")
                if self.phase == phase or self.GetPhaseSuivante() == phase : # la phase est la même
                    listItems.append(["Coller après", functools.partial(self.projet.CollerElem, 
                                                                         item = itemArbre, 
                                                                         btache = elementCopie),
                                      getIconePaste()])
                    
            self.GetApp().AfficherMenuContextuel(listItems)
       
        

    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.encap_HTML(constantes.BASE_FICHE_HTML_TACHE)
    
    
    ######################################################################################  
    def GetBulleSVG(self, i):
        """ Renvoie le tootTip sous la forme d'un texte brut
            pour affichage sur la fiche SVG
        """
        # A FAIRE !!
        return ""
    
    ######################################################################################  
    def GetBulleHTML(self, i = None, css = False):
        """ Renvoie le tootTip sous la forme HTML
            pour affichage sur la fiche HTML (template "_CSS")
            ou sur la fiche pySéquence (template par défaut)
            
        """
        # A FAIRE !!
        return ""
    
    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        
        prj = self.GetProjetRef()
        
        if self.phase in TOUTES_REVUES_SOUT and prj is not None:
            titre = prj.phases[self.phase][1]
            texte = draw_cairo.getHoraireTxt(self.GetDelai())

        else:
            if self.estPredeterminee():
                p = self.intitule
            else:
                p = self.code
                    
            titre = "Tâche "+ p
            if self.phase != "" and prj is not None:
                t = prj.phases[self.phase][1]
            else:
                t = ""
            texte = t

        self.tip.SetWholeText("titre", titre)
        
        # Phase
        if self.phase != "":
            self.tip.AjouterImg("icon", constantes.imagesTaches[self.phase].GetBitmap())
            
        else:
            self.tip.Supprime('icon')
        self.tip.SetWholeText("txt", texte, italic = True, size = 3)
        
        # Icône
        if self.icone is not None:
            self.tip.AjouterImg("icon2", self.icone, width = 64)
        else:
            self.tip.Supprime('icon2')
            
        if not self.phase in TOUTES_REVUES_EVAL_SOUT:
            if self.intitule != "":
                if self.estPredeterminee():
                    t = textwrap.fill(self.GetProjetRef().taches[self.intitule][1], 50)
                    t = self.GetProjetRef().taches[self.intitule][1]
                else:
                    t = self.intitule
            else:
                t = ""
            self.tip.AjouterTxt("int", t, size = 4)
        
        if hasattr(self, 'description'):
            self.tip.AjouterHTML("des", XMLtoHTML(self.description))    
        else:
            self.tip.Supprime('ldes')
        
        self.tip.AjouterLien('lien', self.lien, self)
        
        self.tip.SetPage()
        
        
        
        
####################################################################################
#
#   Classe définissant les propriétés d'un système
#
####################################################################################
class Systeme(ElementAvecLien, ElementBase):
    def __init__(self, parent, nom = "", typ = "PE"):
        
        self.parent = parent
        ElementAvecLien.__init__(self)
        ElementBase.__init__(self)
        
        self.nom = nom
        self.typ = typ
        self.nbrDispo = Variable("Nombre dispo", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [0,NBR_SYSTEMES_MAXI], modeLog = False,
                              expression = None, multiple = False)
        self.image = None
        self.lienClasse = None
        
        ref = self.GetReferentiel()
        Grammaire.__init__(self, ref.nomSystemes)
        
        
        # La description du système
        self.description = None
        
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
        
    ######################################################################################  
    def GetDocument(self):
        if isinstance(self.parent, Classe):
            return self.parent.GetDocument()
        else:
            return self.parent
    
#     ######################################################################################  
#     def __repr__(self):
#         if self.image != None:
#             i = img2str(self.image.ConvertToImage())[:20]
#         else:
#             i = "None"
#         return self.nom#+" ("+str(self.nbrDispo.v[0])+") " + i
#         
        

    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Systeme(parent, self)
    
    
    ######################################################################################  
    def getBrancheClasse(self):
        """ Renvoie la branche XML du Système pour enregistrement
            cas d'un système associé à une Classe
        """
        root = ET.Element("Systeme")
        root.set("NomClasse", self.nom)
        return root
    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du Système pour enregistrement
        """
#         print("getBranche", self, self.GetDocument())
        
        root = ET.Element("Systeme")
        
        root.set("Nom", self.nom)
        root.set("Type", self.typ)
        self.lien.getBranche(root)
        root.set("Nbr", str(self.nbrDispo.v[0]))
        self.getBrancheImage(root)
        
        if self.description != None:
            root.set("Description", self.description)
        
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#         print "setBranche systeme",
        nomClasse  = branche.get("NomClasse", "")
#         print nomClasse
        if nomClasse != "" and isinstance(self.parent, Sequence):
            classe = self.parent.classe
#            print "   >>", classe
            for s in classe.systemes:
                if s.nom == nomClasse:
                    self.lienClasse = s
#                     self.setBranche(s.getBranche())
#                    self.GetPanelPropriete().Verrouiller(False)
#                        self.panelPropriete.cbListSys.SetSelection(self.panelPropriete.cbListSys.FindString(self.nom))
                    break
            
                
        else:
            self.nom  = branche.get("Nom", "")
            self.typ  = branche.get("Type", "PE")
            self.lien.setBranche(branche, self.GetPath())
    
            self.nbrDispo.v[0] = eval(branche.get("Nbr", "1"))
            
            self.setBrancheImage(branche)
            
            self.description = branche.get("Description", None)
            
            
#        self.GetPanelPropriete().MiseAJour()

    ######################################################################################  
    def MiseAJourListeSystemesClasse(self):
        return
#        self.GetPanelPropriete().MiseAJourListeSys()

    ######################################################################################  
    def Copie(self, parent, panelParent = None):
        s = Systeme(parent)
        s.setBranche(self.getBranche())
        return s
    
    ######################################################################################  
    def propagerChangements(self):
#        print "propagerChangements", self
        if isinstance(self.parent, Classe) and hasattr(self.parent, 'doc'):
            
            if isinstance(self.parent.doc, Sequence):
#                print "   ",self.parent, self.parent.doc
                seq = self.parent.doc
                for s in seq.systemes:
                    if s.lienClasse == self:
                        s.setBranche(self.getBranche())
                        if hasattr(s, 'arbre'):
                            s.SetCode()
#                        s.GetPanelPropriete().MiseAJourListeSys(self.nom)
        
    ######################################################################################  
    def SetNombre(self):
        if isinstance(self.parent, Sequence):
            self.parent.VerifPb()
            
        else:
            self.propagerChangements()
                
            
    ######################################################################################  
    def SetNom(self, nom):
#         print("SetNom", nom)
        self.nom = nom
        
        self.propagerChangements()
        
#        if nom != u"":
        if hasattr(self, 'arbre'):
            self.SetCode()

    ######################################################################################  
    def GetNom(self):
        if self.nom != "":
            return self.nom
        else:
            return "Système ou matériel"


    ######################################################################################  
    def GetNiveau(self):
        ref = self.GetDocument().GetReferentiel()
        if self.typ in ref.systemes.keys():
            return ref.systemes[self.typ][4]
        else:
            return 0
        
    ######################################################################################  
    def GetIconeType(self):
        ref = self.GetDocument().GetReferentiel()
        return ref.getIconeSysteme(self.typ, 24*SSCALE)
         
    ######################################################################################  
    def SetCode(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetToolTip(self.GetNom() + "\nNombre disponible : " + str(self.nbrDispo.v[0]))
        
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, self.GetNom())
            
#        # Tip
#        if hasattr(self, 'tip'):
#            self.tip.SetTexte(u"Nom : "+self.nom, self.tip_nom)
#            self.tip.SetTexte(u"Nombre disponible : " + str(self.nbrDispo.v[0]), self.tip_nombre)


    ######################################################################################  
    def SetImage(self):
#        self.tip.SetImage(self.image, self.tip_image)
        self.propagerChangements()
        

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
#        self.codeBranche = wx.StaticText(self.arbre, -1, self.nom)

#        if self.image == None or self.image == wx.NullBitmap:
        image = self.arbre.images["Sys"]
#        else:
#            image = self.image.ConvertToImage().Scale(20, 20).ConvertToBitmap()
        self.branche = arbre.AppendItem(branche, self.GetNom(), data = self,#, wnd = self.codeBranche
                                        image = image)
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)
#        self.SetNom(self.nom)
#         self.SetNombre()
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([["Supprimer", 
                                                     functools.partial(self.GetDocument().SupprimerSysteme, item = itemArbre),
                                                     scaleImage(images.Icone_suppr_systeme.GetBitmap())],
                                                    ["Créer un lien", self.CreerLien, 
                                                     scaleImage(images.Icone_lien.GetBitmap())]])
            
    
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        ref = self.GetReferentiel()
        self.SetNomCode(ref.nomSystemes)
        
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.encap_HTML(constantes.BASE_FICHE_HTML_SYSTEME)
    
    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        
        self.tip.SetWholeText("nom", self.nom)
        self.tip.SetWholeText("nbr", "Nombre disponible : " + str(self.nbrDispo.v[0]))
        
        self.tip.AjouterImg("img", self.image) 
        
        self.tip.SetPage()
        
               
               
               
  

# ####################################################################################
# #
# #   Classe définissant les propriétés d'une seance d'emploi du temps
# #
# ####################################################################################
# class Seance_EDT(ElementAvecLien, ElementBase):
#     def __init__(self, parent, nom = u""):
#         
#         self.nom_obj = u"Séance"
#         self.article_c_obj = u"de la"
#         self.article_obj = u"la"
#         
#         self.parent = parent
#         ElementAvecLien.__init__(self)
#         ElementBase.__init__(self)
#         
#         
#         self.jour = 0       # jour de la semaine (lundi = 0)
#         self.groupe = 0     # 0 = classe entière
#         self.debut = 0      # 0 = 8h00 ; 1 = 8h15 ...
#         self.duree = 1      # 1 par 1/4 d'heure
#         
#     
#     ######################################################################################  
#     def getBranche(self):
#         """ Renvoie la branche XML pour enregistrement
#         """
#         root = self.getBranche_TOTAL('intitule','jour','groupe','debut', 'duree')
#         return root
#     
#     ######################################################################################  
#     def setBranche(self, branche):
#         return self.setBranche_TOTAL(branche)
# 
#     ######################################################################################  
#     def GetPanelPropriete(self, parent):
#         return PanelPropriete_Seance_EDT(parent, self)




####################################################################################
#
#   Classe définissant les propriétés d'un emploi du temps
#
####################################################################################
class EDT(ElementAvecLien, ElementBase):
    def __init__(self, parent, nom = ""):
        
#         self.nom_obj = "Emploi du temps"
#         self.article_c_obj = "d'"
#         self.article_obj = "l'"
        
        self.parent = parent
        ElementAvecLien.__init__(self)
        ElementBase.__init__(self)

        self.seances = []




####################################################################################
#
#   Classe définissant les propriétés d'un calendrier de progression
#
####################################################################################
class Calendrier(ElementAvecLien, ElementBase):
    def __init__(self, parent, annee, nom = ""):
        
#         self.nom_obj = "Calendrier"
#         self.article_c_obj = "du"
#         self.article_obj = "le"
        
        self.parent = parent
        ElementAvecLien.__init__(self)
        ElementBase.__init__(self)
        
        self.nom = nom
        self.description = None
        
        self.image = None
        
#         self.MiseAJourTypeEnseignement()
        
        #self.EDT = EDT()
        self.annee = annee
        
        self.seances = []
        
        self.J_feries = []
        
        self.J_absent = []
        
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
        
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la séquence pour enregistrement
        """
        # Création de la racine
        calendrier = ET.Element("Calendrier")
#         calendrier.set("Intitule", self.intitule)
        calendrier.set("Annee", str(self.annee))
        
        return calendrier
    
    
    ######################################################################################  
    def setBranche(self, branche):
        self.intitule = branche.get("Intitule", "")
        self.annee = eval(branche.get("Annee", str(constantes.getAnneeScolaire())))

    
    ######################################################################################  
    def GetAnneeFin(self):
        return self.annee + len(self.GetReferentiel().periodes)


    ######################################################################################  
    def GetNbrAnnees(self):
        return self.GetAnneeFin() - self.annee

    ######################################################################################  
    def GetMois(self):
        lmois = {}
        nmois = 0
        lannees = self.GetListeAnnees()
        for ia, annee in enumerate(lannees):
            if ia == 0:
                lmois[annee] = [list(range(9, 13))]
                nmois += 4
            elif ia == self.GetNbrAnnees():
                lmois[annee] = [list(range(1,7))]
                nmois += 6
            else:
                lmois[annee] = [list(range(1,7)), list(range(9, 13))]
                nmois += 10
            
        return lmois, nmois
    
    
    ######################################################################################  
    def GetListeAnnees(self):
        return [self.annee + i for i in range(self.GetNbrAnnees()+1)]


    ######################################################################################  
    def GetCreneauxFeries(self):
        creneaux = []
        jours_feries = constantes.JOURS_FERIES
        lstAcad = sorted([a[0] for a in constantes.ETABLISSEMENTS.values()])
        acad = self.GetClasse().academie
        
        try:
            num_acad = lstAcad.index(acad)
        except:
            num_acad = None      
                        
        for annee in self.GetListeAnnees():
            if annee in jours_feries.keys():
                list_zones, list_crenaux = jours_feries[annee]
                
                zone = None
                if num_acad is not None:
                    for z, l in list_zones.items():
                        if num_acad in l:
                            zone = z
                            break
                
                if zone in list_crenaux.keys():
                    creneaux.extend(list_crenaux[zone])
            
        return creneaux
        
        
        
        
        
#     #############################################################################
#     def MiseAJourTypeEnseignement(self):
# #         self.annee = self.parent.annee
# #         self.anneefin = self.parent.GetAnneeFin()
#         self.nbr_annees = self.anneefin - self.annee
    


####################################################################################
#
#   Classe définissant les propriétés d'un support de projet
#
####################################################################################
class Support(ElementAvecLien, ElementBase):
    def __init__(self, parent, nom = ""):
        
#         self.nom_obj = "Support"
#         self.article_c_obj = "du"
#         self.article_obj = "le"
        
        self.parent = parent
        ElementAvecLien.__init__(self)
        ElementBase.__init__(self)
        Grammaire.__init__(self, "Support(s)$m")
        
        self.modeles = []
        
        self.nom = nom
        self.description = None
        
        self.image = None
        
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    ######################################################################################  
    def GetDocument(self):    
        return self.parent
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Support(parent, self)
    
    ######################################################################################  
    def __repr__(self):
        return self.nom
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
        root = ET.Element("Support")
        root.set("Nom", self.nom)
        self.lien.getBranche(root)
        if self.description != None:
            root.set("Description", self.description)
        
        self.getBrancheImage(root)
        
        mo = ET.SubElement(root, "Modeles")
        for m in self.modeles:
            mo.append(m.getBranche())

        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        Ok = True
        self.nom  = branche.get("Nom", "")
        self.description = branche.get("Description", None)
        
        Ok = Ok and self.lien.setBranche(branche, self.GetPath())

        Ok = Ok and self.setBrancheImage(branche)
        
        
        brancheMod = branche.find("Modeles")
        self.modeles = []
#         print list(brancheMod)
        if brancheMod is not None:
            for e in list(brancheMod):
                m = Modele(self)
                Ok = Ok and m.setBranche(e)
                self.modeles.append(m)
            
        return Ok
    
    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        if hasattr(self, 'pts_caract' ):
            for i, pt in enumerate(self.pts_caract):
                lst.append((pt, self, i))
                
        self.cadre = []
        
        return lst
    
    
    ######################################################################################  
    def SetNom(self, nom):
        self.nom = nom
#        if nom != u"":
        if hasattr(self, 'arbre'):
            self.SetCode()

    ######################################################################################  
    def GetNom(self):
        if self.nom != "":
            return self.nom
        else:
            return "Support"
    
            
    ######################################################################################  
    def GetCode(self, i = None):
        return "Support"


    ######################################################################################  
    def GetIntit(self, i = None):
        return self.nom


    ######################################################################################  
    def GetNewModeleId(self):
        i = 1
        l = [m.id for m in self.modeles]
        while i in l:
            i += 1
        return i

    ######################################################################################  
    def GetIntitModeles(self):
        return [m.GetNom() for m in self.modeles]
        
        
    ######################################################################################  
    def SetCode(self):
#        if hasattr(self, 'codeBranche'):
#            self.codeBranche.SetLabel(self.nom)

        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, self.GetNom())
            
#        # Tip
#        if hasattr(self, 'tip'):
#            self.tip.SetTexte(u"Nom : "+self.nom, self.tip_nom)
    
    
    ######################################################################################  
    def AjouterModele(self, event = None): 
        m =   Modele(self)
        self.modeles.append(m)
        
        m.ConstruireArbre(self.arbre, self.branche)
        
        self.OrdonnerModeles()
        self.arbre.SelectItem(m.branche)
#             self.AjouterEleveDansPanelTache()
#         m.MiseAJourCodeBranche()
        
        self.GetApp().sendEvent(modif = "Ajout d'un Modèle")
        
        
    ######################################################################################  
    def SupprimerModele(self, event = None, item = None):
#         print "SupprimerModele", item
        if item is not None:
            m = self.arbre.GetItemPyData(item)
#             i = m.id
#             print "   ", i
#             del self.modeles[i-1]
            self.modeles.remove(m)
            self.arbre.Delete(item)
            
            self.GetDocument().OnModifModeles()
            
            self.GetApp().sendEvent(modif = "Suppression d'un Modèle")
        

    ######################################################################################  
    def OrdonnerModeles(self):
#         print "OrdonnerModeles"
#         i = -1
#         for i,m in enumerate(self.modeles):
#             m.id = i
        
        for i, m in enumerate(self.modeles):
            m.SetCode()

        self.arbre.Ordonner(self.branche)

        
#    ######################################################################################  
#    def SetImage(self):
#        self.tip.SetImage(self.image, self.tip_image)
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, "Support", data = self,#, wnd = self.codeBranche
                                        image = self.arbre.images["Spp"])
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)
        #
        # Les modèles
        #
        for m in self.modeles:
            m.ConstruireArbre(arbre, self.branche) 
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([["Créer un lien", self.CreerLien, 
                                                     scaleImage(images.Icone_lien.GetBitmap())],
                                                    ["Ajouter un Modèle", self.AjouterModele, 
                                                     scaleImage(images.Icone_ajout_modele.GetBitmap())],
                                                    ])
            
            
#             elif self.arbre.GetItemText(itemArbre) == Titres[7]: # Support
#             self.app.AfficherMenuContextuel([[u"Ajouter un Modèle", self.support.AjouterModele, 
#                                               scaleImage(images.Icone_ajout_modele.GetBitmap())],
#                                              ]) 
#             
            
            
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.encap_HTML(constantes.BASE_FICHE_HTML_SUPPORT)

    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        
        self.tip.SetWholeText("nom", self.nom, size=5)
        self.tip.AjouterHTML("des", XMLtoHTML(self.description))      
        if self.image is not None:
            self.tip.AjouterImg("img", self.image, width = 300)
        else:
            self.tip.Supprime('img')
            
        for m in self.modeles:
            m.SetTip()
            self.tip.InsererSoup("mod", m.tip.soup)
        
        self.tip.SetPage()
    




####################################################################################
#
#   Classe définissant les propriétés d'un modèle numérique
#
####################################################################################
class Modele(ElementAvecLien, ElementBase, Grammaire):
    def __init__(self, support, Id = None):
        Grammaire.__init__(self, "Modèle(s) numérique(s)$m")
#         self.nom_obj = "Modèle numérique"
#         self.article_c_obj = "du"
#         self.article_obj = "le"
        
        self.code = "Mod"
        self.support = support
        
        self.logiciels = []
    
        ElementAvecLien.__init__(self)
        ElementBase.__init__(self)
        
        self.intitule  = ""
        self.description = None
        self.image = None
        
        if Id is None:
            Id = support.GetNewModeleId()
        self.id = Id
    
    ######################################################################################  
    def __repr__(self):
        return self.intitule
    
    ######################################################################################  
    def GetApp(self):
        return self.support.GetApp()
    
    ######################################################################################  
    def GetDocument(self):    
        return self.support.GetDocument()
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Modele(parent, self)
    
    ######################################################################################  
    def GetArbreLogiciels(self):
        arbre = []
        
        def branche(br, lst):
            for log in lst:
                if type(log) == tuple:
                    if log[0][1:] in self.logiciels:
                        sbr = []
                        br.append((log[0], branche(sbr, log[1])))
                    
                else:
                    if log[1:] in self.logiciels:
                        br.append(log)
            return br
         
        branche(arbre, constantes.LOGICIELS)
        return arbre
    
    
    ######################################################################################  
    def GetLogosLogiciels(self):
        return {l : constantes.IMG_LOGICIELS[l].GetBitmap() for l in self.logiciels if l in constantes.IMG_LOGICIELS.keys()}
    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML pour enregistrement
        """
        root = ET.Element("Modele")
        
        root.set("Id", str(self.id))
        root.set("Intitule", self.intitule)
        self.lien.getBranche(root)
        
        if self.description != None:
            root.set("Description", self.description)
            
        brancheLog = ET.Element("Logiciels")
        root.append(brancheLog)
        for i, m in enumerate(self.logiciels):
            brancheLog.set("Log"+str(i), m)
        
        self.getBrancheImage(root)

        return root
    
    ######################################################################################  
    def SetNom(self, nom):
        self.intitule = nom
        if hasattr(self, 'arbre'):
            self.SetCode()


    ######################################################################################  
    def GetNom(self):
        if self.intitule != "":
            t = self.intitule
        else:
            t = self.Sing_() + " " + str(self.id)
        return t
    
    
    ######################################################################################  
    def GetIcone(self):
        if len(self.logiciels) > 0 and self.logiciels[0] in self.arbre.images.keys():
            image = self.arbre.images[self.logiciels[0]]
        else:
            image = self.arbre.images[self.code]
        return image
    
    
    ######################################################################################  
    def SetCode(self):
#        if hasattr(self, 'codeBranche'):
#            self.codeBranche.SetLabel(self.nom)
        t = self.GetNom()
       
            
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
            self.arbre.SetItemImage(self.branche, self.GetIcone())
            
            
    ######################################################################################  
    def setBranche(self, branche):
        Ok = True
        self.id  = eval(branche.get("Id", "0"))
        self.intitule  = branche.get("Intitule", "")
        self.description = branche.get("Description", None)

        brancheLog = branche.find("Logiciels")
        self.logiciels = []
        if brancheLog is not None:
            for i, m in enumerate(brancheLog.keys()):
                self.logiciels.append(brancheLog.get("Log"+str(i)))
#         print self.id, self.logiciels
        
        Ok = Ok and self.lien.setBranche(branche, self.GetPath())

        Ok = Ok and self.setBrancheImage(branche)
        return Ok
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            listItems = [["Supprimer", 
                          functools.partial(self.support.SupprimerModele, item = itemArbre), 
                          scaleImage(images.Icone_suppr_modele.GetBitmap())]]
            self.GetApp().AfficherMenuContextuel(listItems)
            
            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre)
        
#         image = self.arbre.images[self.code]
#         print image
#         
#         print constantes.IMG_LOGICIELS
#         print self.logiciels
#         image = scaleImage(constantes.IMG_LOGICIELS[self.logiciels[0]].GetBitmap())
#         print image
        
#         try:
#             image = constantes.IMG_LOGICIELS[self.logiciel[0]].GetBitmap()
#         except:
#             image = self.arbre.images[self.code]
#        else:
#            image = self.image.ConvertToImage().Scale(20, 20).ConvertToBitmap()
        self.branche = arbre.AppendItem(branche, "", data = self, 
                                        wnd = self.codeBranche,
                                        image = self.GetIcone())
        self.codeBranche.SetBranche(self.branche)

        
        self.SetCode()
        
    
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.BASE_FICHE_HTML_MODELE

    
    ######################################################################################  
    def SetTip(self):
#         print "SetTip", self
        self.tip.SetHTML(self.GetFicheHTML(), "html.parser")
        
        
        
        self.tip.SetWholeText("int", self.intitule, size=4)
        self.tip.AjouterHTML("des", XMLtoHTML(self.description))      
        if self.image is not None:
            self.tip.AjouterImg("img", self.image, width = 200)
        else:
            self.tip.Supprime('img')
            
        self.tip.AjouterListe("log", self.GetArbreLogiciels())
        
        self.tip.SetPage()
        
        
        
####################################################################################
#
#   Classe définissant les propriétés d'une personne
#
####################################################################################
class Personne(ElementBase):
    def __init__(self, doc, Id = 0, nom = "", prenom = "", width = 400*SSCALE):
        self.doc = doc
        ElementBase.__init__(self, width)

        self.nom = nom
        self.prenom = prenom
        self.image = None
        self.id = Id # Un identifiant unique = nombre > 0


    ######################################################################################  
    def __eq__(self, personne):
        return isinstance(personne, Personne) \
            and self.GetNom() == personne.GetNom() \
            and self.GetPrenom() == personne.GetPrenom()
    
    
    ######################################################################################  
    def GetApp(self):
        return self.doc.GetApp()

    ####################################################################################
    def EstMovable(self):
        return True
    
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Personne(parent, self)


    ######################################################################################  
    def GetDocument(self):
        return self.doc
    
    
    ######################################################################################  
    def __repr__(self):
        return self.GetNomPrenom()+" ("+str(self.id)+")"


    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
#         print("getBranche", constantes.supprime_accent(self.titre).capitalize())
        root = ET.Element(toSystemEncoding(constantes.supprime_accent(self.titre).capitalize()))
        
        root.set("Id", str(self.id))
        root.set("Nom", self.nom)
        root.set("Prenom", self.prenom)
        
        self.getBrancheImage(root, "Avatar")
        
        if hasattr(self, 'referent'):
            root.set("Referent", str(self.referent))
            
        if hasattr(self, 'discipline'):
            root.set("Discipline", str(self.discipline))
            
        if hasattr(self, 'grille'): # Cas des élèves (et pas des profs)
            for k, g in self.grille.items():
                root.set("Grille"+k, toSystemEncoding(g.path))       
#                 brancheGri = ET.Element("Grille"+k)
#                 root.append(brancheGri)
#                 g.getBranche(brancheGri)
        
        if hasattr(self, 'modeles'):
            brancheMod = ET.Element("Modeles")
            root.append(brancheMod)
            for i, m in enumerate(self.modeles):
                brancheMod.set("Mod"+str(i), str(m))
            
            
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche personne"
        Ok = True
        self.id  = eval(branche.get("Id", "0"))
        self.nom  = branche.get("Nom", "")
        self.prenom  = branche.get("Prenom", "")
        
        Ok = Ok and self.setBrancheImage(branche, "Avatar")
        
        if hasattr(self, 'referent'):   # prof
            self.referent = eval(branche.get("Referent", "False"))
            
        if hasattr(self, 'discipline'): # prof
            self.discipline = branche.get("Discipline", 'Tec')
            
        if hasattr(self, 'grille'):     # élève
#            print self.grille
            for k in self.GetProjetRef().parties.keys():
                self.grille[k] = Lien(typ = "f")
                self.grille[k].path = toFileEncoding(branche.get("Grille"+k, r""))
#             print "grilles", self.grille
#            self.grille[0].path = branche.get("Grille0", u"")
#            self.grille[1].path = branche.get("Grille1", u"")
            
#        self.GetPanelPropriete().SetImage()
#        self.GetPanelPropriete().MiseAJourTypeEnseignement()
#        self.GetPanelPropriete().MiseAJour(marquerModifier = False)
            
        if hasattr(self, 'modeles'):    
            brancheMod = branche.find("Modeles")
            self.modeles = []
            if brancheMod is not None:
                for i, m in enumerate(brancheMod.keys()):
                    self.modeles.append(eval(brancheMod.get("Mod"+str(i))))

                
                
        return Ok

    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        if hasattr(self, 'pts_caract' ):
            for i, pt in enumerate(self.pts_caract):
                lst.append((pt, self, i))
                
        self.cadre = []
        
        return lst
    
    ######################################################################################  
    def GetNom(self):
        return self.nom.upper()
    
    ######################################################################################  
    def GetPrenom(self):
        return self.prenom.capitalize()
        
    ######################################################################################  
    def GetNomPrenom(self, disc = False):
        if disc and hasattr(self, 'discipline') and constantes.CODE_DISCIPLINES[self.discipline] != "":
            d = ' ('+constantes.CODE_DISCIPLINES[self.discipline]+')'
        else:
            d = ""
        if self.nom == "" and self.prenom == "":
            return self.titre.capitalize()+' '+str(self.id+1)+d
        else:
            return self.GetPrenom() + ' ' + self.GetNom()+d
         
    
    ######################################################################################  
    def SetNom(self, nom):
        self.nom = nom
        if hasattr(self, 'arbre'):
            self.SetCode()
        
    ######################################################################################  
    def SetPrenom(self, prenom):
        self.prenom = prenom
#        if nom != u"":
        if hasattr(self, 'arbre'):
            self.SetCode()

    ######################################################################################  
    def SetCode(self):
#        if hasattr(self, 'codeBranche'):
#            self.codeBranche.SetLabel(self.nom)
        
        t = self.GetNomPrenom()
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
         
#         self.SetTip()
        
    
    ######################################################################################  
    def GetAvatar(self):
        if self.image is None:
            return constantes.AVATAR_DEFAUT
        else:
            return self.image


    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        self.tip.SetWholeText("tit", self.GetReferentiel().labels["ELEVES"][2].sing_(), bold = True, size=6)
        
        if hasattr(self, 'referent'):
            bold = self.referent
        else:
            bold = True
        self.tip.SetWholeText("nom", self.GetNomPrenom(), bold = bold, size=5)
        self.tip.AjouterImg("av", self.GetAvatar()) 
        
        self.SetTip2()
        
        # Tip
#        if hasattr(self, 'tip'):
#            self.tip.SetTexte(self.GetNomPrenom(), self.tip_nom)
#            self.tip.SetImage(self.image, self.tip_avatar)

    ######################################################################################  
    def SetImage(self):
        self.SetTip()
#        return
#        self.tip.SetImage(self.image, self.tip_avatar)
#        self.SetTip()
        
    




####################################################################################
#
#   Classe définissant les propriétés d'un élève
#
####################################################################################
class Eleve(Personne):
    def __init__(self, doc, ident = 0, nom = "", prenom = ""):
        
#         self.titre = u"élève"
        
        self.code = "Elv"
        
        self.grille = {} #[Lien(typ = 'f'), Lien(typ = 'f')]
        for k in doc.GetProjetRef().parties.keys():
            self.grille[k] = Lien(typ = 'f')
        
        Personne.__init__(self, doc, ident, nom = nom, prenom = prenom, width = 550*SSCALE)
        Grammaire.__init__(self, self.GetReferentiel().labels["ELEVES"][0])
        
        self.titre = self.GetReferentiel().labels["ELEVES"][2].sing_()
 
        self.modeles = []
        
            
    ######################################################################################  
    def GetDuree(self, phase = None, total = False):
        """ Calcul de la durée que doit passer l'élève sur les Tâches du Projet
            à partir de la phase 
        """
#        print "GetDuree", phase
        d = 0.0
        p = 0
        if not total and phase != None:
            for i, t in enumerate(self.GetDocument().taches):
                if t.phase == phase:
                    break
                if t.phase in TOUTES_REVUES_EVAL_SOUT:
                    p = i
        
        for t in self.GetDocument().taches[p:]:
            if t.phase == phase:
                break
            if not t.phase in TOUTES_REVUES_SOUT:
                if self.id in t.eleves:
                    d += t.GetDuree() * t.impEleves[t.eleves.index(self.id)]*0.01
#        print "   >>>", d
        return d

    ######################################################################################  
    def GetAvatar(self):
        if self.image is None:
            return images.Icone_eleve.GetBitmap()
        else:
            return self.image
        
    ######################################################################################  
    def GetDureeJusqua(self, tache, depuis = None):
        d = 0
        p = 0
        if depuis != None:
            for i, t in enumerate(self.GetDocument().taches):
                if t == depuis:
                    break
                p = i
        
        for t in self.GetDocument().taches[p:]:
            if t == tache:
                break
            if not t.phase in TOUTES_REVUES_SOUT:
                if self.id in t.eleves:
                    d += t.GetDuree()
        return d
    
    ######################################################################################  
    def OuvrirGrille(self, k):
#         print("OuvrirGrille", k)
        self.grille[k].Afficher(self.GetDocument().GetPath())
#         try:
#             self.grille[k].Afficher(self.GetDocument().GetPath())#os.startfile(self.grille[num])
#         except:
#             messageErreur(None, u"Ouverture impossible",
#                           u"Impossible d'ouvrir le fichier\n\n%s!\n" %toSystemEncoding(self.grille[k].path))
             
             
    ######################################################################################  
    def OuvrirGrilles(self, event):
        for k in self.grille.keys():
            self.OuvrirGrille(k)
#        if self.GetTypeEnseignement(simple = True) == "STI2D":
#            self.OuvrirGrille(1)
        
        
    ######################################################################################  
    def getNomFichierDefaut(self, prefixe):
        return getNomFichier(prefixe, self.GetNomPrenom()+"_"+self.GetDocument().intitule[:20])

        
#     ######################################################################################  
#     def GetNomGrilles2(self, dirpath = None, ):
#         u""" Renvoie les noms des fichiers grilles à générer
#         
#         
#             :param dirpath: chemin du dossier où doivent se trouver les grilles
#             :type dirpath: string
#             
#             :return: Les noms des grilles sous la forme :
#                         {partie_du_projet : chemin_absolu_du_fichier_grille}
#             :rtype: dict
#         """
# #        print "GetNomGrilles"
#         prj = self.GetDocument().GetProjetRef()
# #        print prj
# #        print prj.grilles
#         #
#         # Création des noms des fichiers grilles
#         #
#         # Par défaut = chemin du fichier .prj
#         if dirpath == None:
#             dirpath = os.path.dirname(self.GetDocument().GetApp().fichierCourant)
#             
#         nomFichiers = {} 
#         for part, g in prj.parties.items():
#             prefixe = "Grille_"+g
#             gr = prj.grilles[part]
# #            print gr
#             if grilles.EXT_EXCEL != None: 
#                 if gr[1] == 'C': # fichier "Collectif"
#                     nomFichiers[part] = os.path.join(dirpath, self.GetDocument().getNomFichierDefaut(prefixe))
#                 else:
#                     nomFichiers[part] = os.path.join(dirpath, self.getNomFichierDefaut(prefixe))
#                 nomFichiers[part] += grilles.EXT_EXCEL
#                 
# #        print "   >", nomFichiers
#         return nomFichiers

    
    ######################################################################################  
    def GetNomGrilles(self, dirpath = None, ):
        """ Renvoie les noms des fichiers grilles à générer
        
        
            :param dirpath: chemin du dossier où doivent se trouver les grilles
            :type dirpath: string
            
            :return: Les noms des grilles sous la forme :
                        {chemin_absolu_du_fichier_grille_original : ([partie(s)_du_projet] , chemin_absolu_du_fichier_grille)}
            :rtype: dict
        """
#         print "GetNomGrilles"
        prj = self.GetDocument().GetProjetRef()
#        print prj
#        print prj.grilles
        #
        # Création des noms des fichiers grilles
        #
        # Par défaut = chemin du fichier .prj
        if dirpath == None:
            dirpath = os.path.dirname(self.GetDocument().GetApp().fichierCourant)
        
        prefixes = {}
        for part, g in prj.parties.items():
            fo = prj.grilles[part][0]
            if not fo in prefixes.keys():
                prefixes[fo] = [part]
            else:
                prefixes[fo].append(part)
            
        nomFichiers = {} 
        for fo, parts in prefixes.items():
            prefixe = "_".join(["Grille"]+[prj.parties[part] for part in parts])
            gr = prj.grilles[parts[0]]
            if grilles.EXT_EXCEL != None: 
                if gr[1] == 'C': # fichier "Collectif"
                    nomFichiers[fo] = os.path.join(dirpath, self.GetDocument().getNomFichierDefaut(prefixe))
                else:
                    nomFichiers[fo] = os.path.join(dirpath, self.getNomFichierDefaut(prefixe))
                nomFichiers[fo] += grilles.EXT_EXCEL
                nomFichiers[fo] = (parts, nomFichiers[fo])
                
#         print "   >", nomFichiers
        return nomFichiers
    
    
    
    ######################################################################################################
    def GetNomDetails(self, dirpath = None):
        """ Renvoie les noms des fichiers de description détaillée des tâches
        
            :param dirpath: chemin du dossier où doivent se trouver les grilles
            :type dirpath: string
            
            :return: Les noms des fichiers sous la forme :
                        {chemin_absolu_du_fichier_grille_original : ([partie(s)_du_projet] , chemin_absolu_du_fichier_grille)}
            :rtype: dict
        """
        # Par défaut = chemin du fichier .prj
        if dirpath == None:
            dirpath = os.path.dirname(self.GetDocument().GetApp().fichierCourant)
        
        f = "Tâches détaillées _ " + self.GetNomPrenom() + ".rtf"
        return os.path.join(dirpath, f)
    
    

    ######################################################################################  
    def GenererGrille(self, event = None, dirpath = None, nomFichiers = None, 
                      messageFin = True, win = None):
        """ Génération des grilles d'évaluation de l'élève
        
            Génère un dictionnaire "tableaux" :
                {chemin_du_fichier_Excel_de_la_grille : (liste_des_parties_concernées, objet_tableau_Excel_ouvert)}
        
            :param nomFichiers: noms des fichiers des grilles (voir méthode .GetNomGrilles())
            :type nomFichiers: dict
            
            :param dirpath: chemin du dossier où doivent se trouver les grilles
            :type dirpath: string
            
            :param messageFin: True pour afficher un message à la fin de la génération
            :type messageFin: bool
            
            :param win: Fenêtre parente des éventuels wx.Dialog à afficher pendant la génération
            :type win: wx.Window
            
            :return: Un log des erreurs rencontrées
            :rtype: list
        
        """
#         print "GenererGrille élève", self
#         print "  ", nomFichiers
        
        if nomFichiers == None:
            nomFichiers = self.GetNomGrilles(dirpath)
            if not self.GetDocument().TesterExistanceGrilles({0:nomFichiers}, dirpath):
                return []
#             print "  >>> Fichiers :", nomFichiers
        
        
        prj = self.GetDocument().GetProjetRef()
        app = self.GetDocument().GetApp()
        if win is None:
            win = app
        
        
        wx.BeginBusyCursor()
        #
        # Ouverture (et pré-sauvegarde) des fichiers grilles "source" (tableaux Excel)
        #
        tableaux = {}
        for fo, v in nomFichiers.items():
            parts, f = v
            if os.path.isfile(f):  # Fichier grille élève déja existant
#                 print "   exist :", f
                tableaux[f] = (parts, grilles.getTableau(win, f))
                
            else:  # fichier original vierge de la grille
#                 print "   new :",
                fo = grilles.getFullNameGrille(fo)
                if os.path.isfile(fo):
                    # Copie du fichier original
#                     print "copy", fo, f
                    try:
                        shutil.copy(fo, f)
                    except IOError :
                        messageErreur(win, "Erreur !",
                                      "Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
                                      " - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
                                      " - que le dossier choisi n'est pas protégé en écriture" %f)
                    else:
                        tableaux[f] = (parts, grilles.getTableau(win, f))
                
                else: # fichier original de grille non trouvé ==> nouvelle tentative avec les noms du référentiel par défaut
#                     prjdef = REFERENTIELS[self.GetDocument().GetTypeEnseignement()].getProjetDefaut()
#                     tableaux[part] = None
                    messageErreur(win, "Fichier non trouvé !",
                                  "Le fichier original de la grille,\n    " + fo + "\n" \
                                  "n'a pas été trouvé ! \n")
                        
    
                    

        if tableaux == {}:
            wx.EndBusyCursor()
            return []
        
        #
        # Remplissage des grilles
        #
        log = []
        if "beta" in version.__version__:
            log = grilles.modifierGrille(self.GetDocument(), tableaux, self)
        else:
            try:
                log = grilles.modifierGrille(self.GetDocument(), tableaux, self)
            except:
                messageErreur(win, "Erreur !",
                              "Impossible de modifier les grilles !") 


        #
        # Enregistrement final des grilles
        #
        for f, v in tableaux.items():
            parts, t = v
            try:
                t.save()
            except:
                messageErreur(win, "Erreur !",
                              "Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
                              " - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
                              " - que le dossier choisi n'est pas protégé en écriture" %f)
            try:
                t.close()
            except:
                pass
            for part in parts:
                self.grille[part] = Lien(typ = 'f')
                self.grille[part].path = toFileEncoding(f)
        
#         self.GetDocument().GetApp().MarquerFichierCourantModifie()
        # Mise à our du panel de Propriétés courant
        panelProp = app.GetPanelProp()
        if hasattr(panelProp, 'MiseAJour'):
            panelProp.MiseAJour(sendEvt = False, marquerModifier = True)
        
        #
        # Message de fin
        #
        if messageFin:
            t = "Génération "
            if len(tableaux)>1:
                t += "des grilles"
            else:
                t += "de la grille"
            t += "\n\n"
            t += "\n".join(list(nomFichiers.values()))
            t += "\n\nterminée avec "
            if len(log) == 0:
                t += "succès !"
            else:
                t += "des erreurs :\n"
                t += "\n".join(log)
            messageInfo(win, "Génération terminée", t)
            
        wx.EndBusyCursor()
#         self.GetPanelPropriete().MiseAJour()
        return log
     
    
#     ######################################################################################  
#     def GenererGrille(self, event = None, dirpath = None, nomFichiers = None, messageFin = True, win = None):
#         u""" Génération des grilles d'évaluation de l'élève
#         
#             :param nomFichiers: noms des fichiers des grilles (voir méthode .GetNomGrilles())
#             :type nomFichiers: dict
#             
#             :param dirpath: chemin du dossier où doivent se trouver les grilles
#             :type dirpath: string
#             
#             :param messageFin: True pour afficher un message à la fin de la génération
#             :type messageFin: bool
#             
#             :param win: Fenêtre parente des éventuels wx.Dialog à afficher pendant la génération
#             :type win: wx.Window
#             
#             :return: Un log des erreurs rencontrées
#             :rtype: list
#         
#         """
# #         print "GenererGrille élève", self
# #         print "  ", nomFichiers
#         
#         if nomFichiers == None:
#             nomFichiers = self.GetNomGrilles(dirpath)
#             if not self.GetDocument().TesterExistanceGrilles({0:nomFichiers}, dirpath):
#                 return []
# #             print "  >>> Fichiers :", nomFichiers
#         
#         
#         prj = self.GetDocument().GetProjetRef()
#         app = self.GetDocument().GetApp()
#         if win is None:
#             win = app
#         
#         
#         wx.BeginBusyCursor()
#         #
#         # Ouverture (et pré-sauvegarde) des fichiers grilles "source" (tableaux Excel)
#         #
#         tableaux = {}
#         for part, f in nomFichiers.items():
#             if os.path.isfile(f):  # Fichier grille élève déja existant
# #                 print "   exist :", f
#                 tableaux[part] = grilles.getTableau(win, f)
#                 
#             else:  # fichier original vierge de la grille
# #                 print "   new :",
#                 fo = grilles.getFullNameGrille(prj.grilles[part][0])
#                 if os.path.isfile(fo):
#                     # Copie du fichier original
# #                     print "copy", fo, f
#                     try:
#                         shutil.copy(fo, f)
#                     except IOError :
#                         messageErreur(win, u"Erreur !",
#                                       u"Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
#                                       u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
#                                       u" - que le dossier choisi n'est pas protégé en écriture" %f)
#                     else:
#                         tableaux[part] = grilles.getTableau(win, f)
#                 
#                 else: # fichier original de grille non trouvé ==> nouvelle tentative avec les noms du référentiel par défaut
#                     prjdef = REFERENTIELS[self.GetDocument().GetTypeEnseignement()].getProjetDefaut()
# #                     tableaux[part] = None
#                     messageErreur(win, u"Fichier non trouvé !",
#                                   u"Le fichier original de la grille,\n    " + prjdef.grilles[part][0] + u"\n" \
#                                   u"n'a pas été trouvé ! \n")
#                         
#     
#                     
# 
#         if tableaux == {}:
#             wx.EndBusyCursor()
#             return []
#         
#         #
#         # Remplissage des grilles
#         #
#         log = []
#         if "beta" in version.__version__:
#             log = grilles.modifierGrille(self.GetDocument(), tableaux, self)
#         else:
#             try:
#                 log = grilles.modifierGrille(self.GetDocument(), tableaux, self)
#             except:
#                 messageErreur(win, u"Erreur !",
#                               u"Impossible de modifier les grilles !") 
# 
# 
#         #
#         # Enregistrement final des grilles
#         #
#         for part, t in tableaux.items():
#             try:
#                 t.save()
#             except:
#                 messageErreur(win, u"Erreur !",
#                               u"Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
#                               u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
#                               u" - que le dossier choisi n'est pas protégé en écriture" %f)
#             try:
#                 t.close()
#             except:
#                 pass
#             self.grille[part] = Lien(typ = 'f')
#             self.grille[part].path = toFileEncoding(nomFichiers[part])
#         
# #         self.GetDocument().GetApp().MarquerFichierCourantModifie()
#         # Mise à our du panel de Propriétés courant
#         panelProp = app.GetPanelProp()
#         if hasattr(panelProp, 'MiseAJour'):
#             panelProp.MiseAJour(sendEvt = False, marquerModifier = True)
#         
#         #
#         # Message de fin
#         #
#         if messageFin:
#             t = u"Génération "
#             if len(tableaux)>1:
#                 t += u"des grilles"
#             else:
#                 t += u"de la grille"
#             t += u"\n\n"
#             t += u"\n".join(nomFichiers.values())
#             t += u"\n\nterminée avec "
#             if len(log) == 0:
#                 t += u"succès !"
#             else:
#                 t += u"des erreurs :\n"
#                 t += u"\n".join(log)
#             messageInfo(win, u"Génération terminée", t)
#             
#         wx.EndBusyCursor()
# #         self.GetPanelPropriete().MiseAJour()
#         return log
#     
    
    ######################################################################################  
    def GrillesGenerees(self):
        b = True
        for g in self.grille.values():
            b = b and len(g.path) > 0
        return b
    
    
    ######################################################################################  
    def HasModele(self):
        return len(self.modeles) > 0
    
    
    ######################################################################################  
    def GetModele(self, num):
#         print "GetModele", num
#         print "   ",self.GetDocument().support.modeles[num-1]
        return self.GetDocument().support.modeles[num]
    
    ######################################################################################  
    def GetModeles(self):
#         print "GetModeles", self.modeles
        return [self.GetModele(num-1) for num in self.modeles]
    
    ######################################################################################  
    def AjouterEnleverModele(self, num):
        idmodel = self.GetModele(num).id
        if idmodel in self.modeles:
            self.modeles.remove(idmodel)
        else:
            self.modeles.append(idmodel)
        self.MiseAJourCodeBranche()
    
    
    ######################################################################################  
    def GetEvaluabilite(self, complet = False, compil = False):
        """ Renvoie l'évaluabilité de l'élève
            % conduite
            % soutenance
            ev, ev_tot, seuil
            
            compil = renvoie des dictionnaire plus simples
        """ 
#         print("GetEvaluabilite", self)
        prj = self.GetProjetRef()
#        dicPoids = self.GetReferentiel().dicoPoidsIndicateurs_prj
        dicIndicateurs = self.GetDicIndicateurs()
#         print("   ", dicIndicateurs)
        
        rs = {}
        lers = {}
        for disc, dic in prj._dicoGrpIndicateur.items():
            rs[disc] = {}
            lers[disc] = {}
            for ph in dic.keys():
                lers[disc][ph] = {}
                rs[disc][ph] = 0
#         print("   xx init :", rs, lers)
        
        
        def getPoids(competence, code, poidsGrp):
#             print "  getPoids", code
            if competence.sousComp != {}:
                for k, c in competence.sousComp.items():
                    getPoids(c, k, poidsGrp)
            
#             if competence.poids != {}:
            for disc, dic in prj._dicoGrpIndicateur.items():
                for ph in dic.keys():
#                     print "      ", ph
                    if grp in dic[ph]:
#                         print "_", dic[ph]
                        for i, indic in enumerate(competence.indicateurs):
                            
                            if disc+code in dicIndicateurs.keys():
                                if dicIndicateurs[disc+code][i]:
#                                     print "  comp", code, i, indic.poids, ph
                                    poids = indic.poids
                                    if ph in poids.keys():
                                        if not ph in poidsGrp.keys():
                                            print("ERREUR poids", code, "Faire \"Ouvrir et réparer\"")
                                        else:
                                            p = 1.0*poids[ph]/100
                                        
                                            rs[disc][ph] += p * poidsGrp[ph]/100
                                            if grp in lers[disc][ph].keys():
                                                lers[disc][ph][grp] += p
                                            else:
                                                lers[disc][ph][grp] = p
                            else:
                                if not grp in lers[disc][ph].keys():
                                    lers[disc][ph][grp] = 0
                            
            return
        
        for typi, dico in prj._dicoIndicateurs.items():
            for grp, grpComp in dico.items():
#                 print "  >>> poids :", grpComp.poids
                getPoids(grpComp, grp, grpComp.poids)
                
        
        #
        # Seuils d'évaluabilité
        #
        # liste des classeurs avec des grilles comprenant des colonne "non"
#        classeurs = [i[0] for i in self.GetReferentiel().cellulesInfo_prj["NON"] if i[0] != '']
        seuil = {}
        for disc, dic in prj._dicoGrpIndicateur.items():
            seuil[disc] = {}
            for t in dic.keys():
    #            if t in classeurs:
    #            print "aColNon", self.GetReferentiel().aColNon
                if t in self.GetReferentiel().aColNon.keys() and self.GetReferentiel().aColNon[t]:
                    seuil[disc][t] = 0.5  # s'il y a une colonne "non", le seuil d'évaluabilité est de 50% par groupe de compétence
                else:
                    seuil[disc][t] = 1.0     # s'il n'y a pas de colonne "non", le seuil d'évaluabilité est de 100% par groupe de compétence
#        print "seuil", seuil
        ev = {}
        ev_tot = {}
#        for txt, le, ph in zip([r, s], [ler, les], prj._dicGrpIndicateur.keys()):

        for disc, dic in prj._dicoGrpIndicateur.items():
            ev[disc] = {}
            ev_tot[disc] = {}
            for part in dic.keys():
                txt = rs[disc][part]
                txt = round(txt, 6)
                ev[disc][part] = {}
                ev_tot[disc][part] = [txt, True]
                for grp, tx in lers[disc][part].items():
                    tx = round(tx, 6)
                    ev[disc][part][grp] = [tx, tx >= seuil[disc][part]]
                    ev_tot[disc][part][1] = ev_tot[disc][part][1] and ev[disc][part][grp][1]
        
#         print("   ", ev, ev_tot, seuil)
        
        
        
        if compil:
            ev = ev["S"]
            ev_tot = ev_tot["S"]
            seuil = seuil["S"]
            
            
        return ev, ev_tot, seuil
        
        
#        if complet:
#            return r, s, ler, les
#        else:
#            return r, s
    

    ######################################################################################  
    def GetCompetences(self):
#         print "GetCompetences", self.code, self.id
        lst = []
        for t in self.GetDocument().taches:
#             print "   ", t, t.eleves
            if self.id in t.eleves:
                lst.extend(t.competences)
        lst = list(set(lst))
        return lst
    
    
    ######################################################################################  
    def GetDicIndicateurs(self, limite = None):
        """Renvoie un dictionnaire des indicateurs que l'élève doit mobiliser
            (pour tracé)
            clef = code compétence
            valeur = liste [True False ...] des indicateurs à mobiliser
        """
        indicateurs = {}
#         print " GetDicIndicateurs", self.id, self.nom
        for t in self.GetDocument().taches: # Toutes les tâches du projet
            if not t.phase in TOUTES_REVUES_SOUT:
                if self.id in t.eleves:     # L'élève est concerné par cette tâche
                    if t.estPredeterminee():
                        indicTache = t.GetDicIndicateursEleve(self) # Les indicateurs des compétences à mobiliser pour cette tâche
                    else:
                        indicTache = t.GetDicIndicateurs() # Les indicateurs des compétences à mobiliser pour cette tâche
                    for c, i in indicTache.items():
                        if c in indicateurs.keys():
                            indicateurs[c] = [x or y for x, y in zip(indicateurs[c], i)]
                        else:
                            indicateurs[c] = i
#         print "  ", indicateurs
        return indicateurs
        
        
        
        
    ######################################################################################  
    def GetDicIndicateursRevue(self, revue):
        """Renvoie un dictionnaire des indicateurs que l'élève doit mobiliser AVANT une revue
            (pour tracé)
            clef = code compétence
            valeur = liste [True False ...] des indicateurs à mobiliser
        """
        indicateurs = {}
#        print " GetDicIndicateurs", self.id
        for t in self.GetDocument().taches: # Toutes les tâches du projet
            if t.code == revue:
                break
            if self.id in t.eleves:     # L'élève est concerné par cette tâche
                indicTache = t.GetDicIndicateurs() # Les indicateurs des compétences à mobiliser pour cette tâche
                for c, i in indicTache.items():
                    if c in indicateurs.keys():
                        indicateurs[c] = [x or y for x, y in zip(indicateurs[c], i)]
                    else:
                        indicateurs[c] = i
                
        return indicateurs
    
    
    
    
    ######################################################################################  
    def GetTaches(self, revues = False):
        lst = []
        for t in self.GetDocument().taches:
            if revues and t.phase in TOUTES_REVUES_EVAL:
                lst.append(t)
            else:
                if self.id in t.eleves:
                    if revues and t.phase == "Rev":
                        lst.append(t)
                    elif t.phase != "Rev":
                        lst.append(t)
            
                    
#        lst = list(set(lst))
            
        return lst
        
    
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            listItems = [["Supprimer", 
                          functools.partial(self.GetDocument().SupprimerEleve, item = itemArbre), 
                          scaleImage(images.Icone_suppr_eleve.GetBitmap())]]
            if len(self.GetProjetRef().parties) > 0:
                tg = "Générer grille"
                to = "Ouvrir grille"
                if len(self.GetProjetRef().parties) > 1:
                    tg += "s"
                    to += "s"
                
                if self.GrillesGenerees():
                    listItems.append([to, functools.partial(self.OuvrirGrilles), None])
            listItems.append([tg, functools.partial(self.GenererGrille), None])    
            
#            if self.projet.GetTypeEnseignement(simple = True) == "SSI":
#                
#                if self.grille[0].path != u"":
#                    
#            else:
#                listItems.append([u"Générer grilles", functools.partial(self.GenererGrille)])
#                if self.grille[0].path != u"":
#                    listItems.append([u"Ouvrir grilles", functools.partial(self.OuvrirGrilles)])
    
            self.GetApp().AfficherMenuContextuel(listItems)
            

    ######################################################################################  
    def MiseAJourTypeEnseignement(self):
#        print "MiseAJourTypeEnseignement", self
        self.grille = {} #[Lien(typ = 'f'), Lien(typ = 'f')]
#        print self.GetReferentiel().nomParties_prj
        for k in self.GetProjetRef().parties.keys():
            self.grille[k] = Lien(typ = 'f')
#        self.GetPanelPropriete().MiseAJourTypeEnseignement()
    
    
    ######################################################################################  
    def MiseAJourCodeBranche(self):
        """ Met à jour les tags de durée de projet
            et d'évaluabilité
            et icône de modèle éventuellement
        """
#        print "MiseAJourCodeBranche", self

        #
        # Durée
        #
        duree = self.GetDuree()
        dureeRef = self.GetProjetRef().duree
#        print "   duree", duree, "/", dureeRef
        lab = " ("+str(int(duree))+"h) "
        self.codeBranche.SetLabel(lab)
        tol1 = constantes.DELTA_DUREE
        tol2 = constantes.DELTA_DUREE2
        taux = abs((duree-dureeRef)/dureeRef)*100
#        print "   taux", taux, "(", tol1, tol2, ")"
        t = "Durée de travail "
        if taux < tol1:
            self.codeBranche.SetBackgroundColour(COUL_OK)
            self.codeBranche.SetToolTip(t + "conforme")
        elif taux < tol2:
            self.codeBranche.SetBackgroundColour(COUL_BOF)
            self.codeBranche.SetToolTip(t + "acceptable")
        else:
            self.codeBranche.SetBackgroundColour(COUL_NON)
            if duree < dureeRef:
                self.codeBranche.SetToolTip(t + "insuffisante")
            else:
                self.codeBranche.SetToolTip(t + "trop importante")
        
        #
        # Evaluabilité
        #
#        er, es , ler, les = self.GetEvaluabilite(complet = True)
        ev, ev_tot, seuil = self.GetEvaluabilite()
        
        for disc, dic in self.GetProjetRef()._dicoGrpIndicateur.items():
            for part in dic.keys():
                self.codeBranche.comp[disc+part].SetLabel(rallonge(pourCent2(ev_tot[disc][part][0])))
        
        keys = {}
        for disc, dic in self.GetProjetRef()._dicoIndicateurs_simple.items():
            keys[disc] = sorted(dic.keys())
            if "O8s" in keys[disc]:
                keys[disc].remove("O8s")
        
        t1 = "L'élève ne mobilise pas suffisamment de compétences pour être évalué"
        t21 = "Le "
        t22 = "Les "
        t3 = "taux d'indicateurs évalués pour "
        t4 = " est inférieur à "
        t51 = "la compétence "
        t52 = "les compétences "
        
#        for ph, nomph, st in zip(['R', 'S'], [u"conduite", u"soutenance"], [self.evaluR, self.evaluS]):
        for disc in self.GetProjetRef()._dicoGrpIndicateur.keys():
            for ph, nomph in self.GetProjetRef().parties.items():
                st = self.codeBranche.comp[disc+ph]
                t = "Évaluabilité de la "+nomph+" du projet "
                tt = ""
                if ev_tot[disc][ph][1]:
                    tt += "\n" + t1
            
                le = [k for k in ev[disc][ph].keys() if ev[disc][ph][k] == False] # liste des groupes de compétences pas évaluable
                if len(le) == 1:
                    tt += "\n" + t21 + t3 + t51 + le[0] + t4 + pourCent2(seuil[disc][ph])
                else:
                    tt += "\n" + t22 + t3 + t52 + " ".join(le) + t4 + pourCent2(seuil[disc][ph])
            
                if ev_tot[disc][ph][1]:
                    coul = COUL_OK
                    t += "POSSIBLE."
                else:
                    coul = COUL_NON
                    t += "IMPOSSIBLE :"
                    t += tt
                
                st.SetBackgroundColour(coul)
                st.SetToolTip(t)

        #
        # Icône
        #
        if self.HasModele():
            self.codeBranche.SetImg(constantes.imagesProjet['Mod'].GetBitmap())
        else:
            self.codeBranche.DelImg()
            
        self.codeBranche.LayoutFit()



    ######################################################################################  
    def SetCode(self):

        t = self.GetNomPrenom()

        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
            
#         self.SetTip()


    ######################################################################################  
    def GetFicheHTML(self, param = None):
#        print "GetFicheHTML"
#        print self.GetProjetRef().listeParties
        dic = {}
        ligne = []
        for ph in self.GetProjetRef().listeParties:
            dic['coul'] = couleur.GetCouleurHTML(getCoulPartie(ph))
            dic['nom'] = self.GetProjetRef().parties[ph]
            dic['id'] = ph
            ligne.append("""<tr  id = "le%(id)s" align="right" valign="middle" >
<td><font color = "%(coul)s"><em>%(nom)s</em></font></td>
</tr>""" %dic)

        ficheHTML = constantes.encap_HTML(constantes.BASE_FICHE_HTML_ELEVE)
        
        
        t = ""
        for l in ligne:
            t += l+"\n"

        ficheHTML = ficheHTML.replace('{{tab_eval}}', t)
        
        return ficheHTML




    ######################################################################################  
    def SetTip2(self):
#        print "SetTip2", self
        # Tip
        if hasattr(self, 'tip'):
            
#            self.tip.SetTexte(self.GetNomPrenom(), self.tip_nom)
            coulOK = couleur.GetCouleurHTML(COUL_OK)
            coulNON = couleur.GetCouleurHTML(COUL_NON)
            
            #
            # Durée
            #
            duree = self.GetDuree()
            lab = draw_cairo.getHoraireTxt(duree)
            if abs(duree-70) < constantes.DELTA_DUREE:
                coul = coulOK
            elif abs(duree-70) < constantes.DELTA_DUREE2:
                coul = couleur.GetCouleurHTML(COUL_BOF)
            else:
                coul = coulNON
            self.tip.AjouterCol("ld", lab, coul, bold = True)

            
            #
            # Evaluabilité
            #
            ev, ev_tot, seuil = self.GetEvaluabilite()
            prj = self.GetProjetRef()
            keys = {}
            for disc, dic in prj._dicoIndicateurs.items():
                keys[disc] = sorted(dic.keys())
#            if "O8s" in keys:
#                keys.remove("O8s")
            lab = {}
            for disc, dic in prj._dicoGrpIndicateur.items():
                lab[disc] = {}
                for part in dic.keys():
                    lab[disc][part] = [[pourCent2(ev_tot[disc][part][0], True), True]]
        #            totalOk = True
                    for k in keys[disc]:
                        if k in prj._dicoGrpIndicateur[disc][part]:
                            if k in ev[disc][part].keys():
                                
        #                        totalOk = totalOk and (ler[k] >= 0.5)
                                lab[disc][part].append([pourCent2(ev[disc][part][k][0], True), ev[disc][part][k][1]]) 
                            else:
        #                        totalOk = False
                                lab[disc][part].append([pourCent2(0, True), False]) 
                        else:
                            lab[disc][part].append(["", True])
                    lab[disc][part][0][1] = ev_tot[disc][part][1]#totalOk and (er >= 0.5)
 
            for disc, dic in prj._dicoGrpIndicateur.items():
                for part in dic.keys():
    #                print "   ", part
                    for i, lo in enumerate(lab[disc][part]):
    #                    print "      ", i, lo
                        l, o = lo
                        if i == 0:
                            size = None
                            bold = True
                            if o:
                                coul = coulOK
                            else:
                                coul = coulNON
                        else:
                            size = 2
                            bold = False
                            if not o:
                                coul = coulNON
                            else:
                                coul = None
                        self.tip.AjouterCol("le"+part, l, coul,
                                       couleur.GetCouleurHTML(getCoulPartie(part)), size, bold)

            for disc in prj._dicoIndicateurs.keys():
                for t in keys[disc]:
                    self.tip.AjouterCol("le", t, size = 2) 
            
            for m in self.GetModeles():
                m.SetTip()
                self.tip.InsererSoup("mod", m.tip.soup)
                
#             for i, m in enumerate(self.GetModeles()):
# #                 print "mod", m
#                 for j, (l,bmp) in enumerate(m.GetLogosLogiciels().items()):
#                     h = u"<p>" + l + u"</p>"
#                     idx = "log"+str(i)+"."+str(j)
#                     h +=u'<img id="%s" src="" alt="">' %idx
# #                     print "   ", h
#                     self.tip.AjouterHTML('mod', h)
#                     self.tip.AjouterImg(idx, bmp)
            
            self.tip.SetPage()
            

            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre)
        for disc, dic in self.GetProjetRef()._dicoGrpIndicateur.items():
            for part in dic.keys():
                self.codeBranche.Add(disc+part)
        
        self.codeBranche.AddImg()
        if self.HasModele():
            self.codeBranche.SetImg(constantes.imagesProjet['Mod'].GetBitmap())
        else:
            self.codeBranche.DelImg()
            
#        if self.image == None or self.image == wx.NullBitmap:
        image = self.arbre.images[self.code]
#        else:
#            image = self.image.ConvertToImage().Scale(20, 20).ConvertToBitmap()
        self.branche = arbre.AppendItem(branche, "", data = self, wnd = self.codeBranche,
                                        image = image)
        self.codeBranche.SetBranche(self.branche)
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)
        
        self.SetCode()
        
        



####################################################################################
#
#   Classe définissant les propriétés d'un groupe d'élève
#
####################################################################################
class Groupe(Eleve):
    def __init__(self, doc, ident = 0):
        
        Eleve.__init__(self, doc, ident)
        
        self.doc = doc
        self.nom = ""
        self.titre = "groupe"
        self.code = "Grp"
        
        self.eleves = []
        
        self.image = None
        
        self.typeEnseignement = self.GetReferentiel().Code
        self.specialite = []

        self.academie = self.GetDocument().classe.academie
        self.ville = self.GetDocument().classe.ville
        self.etablissement = self.GetDocument().classe.etablissement
        
#         print self.academie, self.ville, self.etablissement
        
    ######################################################################################  
    def GetAvatar(self):
        if self.image is None:
            return images.Icone_groupe.GetBitmap()
        else:
            return self.image
        
    ######################################################################################  
    def GetNom(self):
        return self.nom
    
    ######################################################################################  
    def SetNom(self, nom):
        self.nom = nom
        if hasattr(self, 'arbre'):
            self.SetCode()
    
     
    ######################################################################################  
    def GetListEleves(self):
        l = []
        for e in self.eleves:
            l.append((e.GetNom(), e.GetPrenom()))
        return l
    
    
    ######################################################################################  
    def SetListEleves(self, lst):
        self.eleves = []
        for n, p in lst:
            eleve = Eleve(self.GetDocument(), nom = n, prenom = p)
            self.eleves.append(eleve)
    
    
    
    ######################################################################################  
    def GetDuree(self, phase = None, total = False):
#        print "GetDuree", phase
        d = 0.0
        p = 0
        if not total and phase != None:
            for i, t in enumerate(self.GetDocument().taches):
                if t.phase == phase:
                    break
                if t.phase in TOUTES_REVUES_EVAL_SOUT:
                    p = i
        
        for t in self.GetDocument().taches[p:]:
            if t.phase == phase:
                break
            if not t.phase in TOUTES_REVUES_SOUT:
                if self.id in t.eleves:
                    d += t.GetDuree()
#        print "   >>>", d
        return d

    ######################################################################################  
    def GetDocument(self):
        return self.doc
    
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Groupe(parent, self)
    
    
#     ######################################################################################  
#     def GetDureeJusqua(self, tache, depuis = None):
#         d = 0
#         p = 0
#         if depuis != None:
#             for i, t in enumerate(self.GetDocument().taches):
#                 if t == depuis:
#                     break
#                 p = i
#         
#         for t in self.GetDocument().taches[p:]:
#             if t == tache:
#                 break
#             if not t.phase in TOUTES_REVUES_SOUT:
#                 if self.id in t.eleves:
#                     d += t.GetDuree()
#         return d
    
#     ######################################################################################  
#     def OuvrirGrille(self, k):
#         print "OuvrirGrille", k
#         self.grille[k].Afficher(self.GetDocument().GetPath())
# #         try:
# #             self.grille[k].Afficher(self.GetDocument().GetPath())#os.startfile(self.grille[num])
# #         except:
# #             messageErreur(None, u"Ouverture impossible",
# #                           u"Impossible d'ouvrir le fichier\n\n%s!\n" %toSystemEncoding(self.grille[k].path))
#             
#             
#     ######################################################################################  
#     def OuvrirGrilles(self, event):
#         for k in self.grille.keys():
#             self.OuvrirGrille(k)
# #        if self.GetTypeEnseignement(simple = True) == "STI2D":
# #            self.OuvrirGrille(1)
        
        
#     ######################################################################################  
#     def getNomFichierDefaut(self, prefixe):
#         return getNomFichier(prefixe, self.GetNomPrenom()+"_"+self.GetDocument().intitule[:20])

        
#     ######################################################################################  
#     def GetNomGrilles(self, path = None):
#         """ Renvoie les noms des fichiers grilles à générer
#         """
# #        print "GetNomGrilles"
#         prj = self.GetDocument().GetProjetRef()
# #        print prj
# #        print prj.grilles
#         #
#         # Création des noms des fichiers grilles
#         #
#         # Par défaut = chemin du fichier .prj
#         if path == None:
#             path = os.path.dirname(self.GetDocument().GetApp().fichierCourant)
#             
#         nomFichiers = {} 
#         for part, g in prj.parties.items():
#             prefixe = "Grille_"+g
#             gr = prj.grilles[part]
# #            print gr
#             if grilles.EXT_EXCEL != None:
# #                extention = os.path.splitext(ref.grilles_prj[k][0])[1]
#                 extention = grilles.EXT_EXCEL
#                 
#                 if gr[1] == 'C': # fichier "Collectif"
#                     nomFichiers[part] = os.path.join(path, self.GetDocument().getNomFichierDefaut(prefixe)) + extention
#                 else:
#                     nomFichiers[part] = os.path.join(path, self.getNomFichierDefaut(prefixe)) + extention
# #        print "   >", nomFichiers
#         return nomFichiers


#     ######################################################################################  
#     def GenererGrille(self, event = None, path = None, nomFichiers = None, messageFin = True):
# #        print "GenererGrille élève", self
# #        print "  ", nomFichiers
#         if nomFichiers == None:
#             nomFichiers = self.GetNomGrilles(path)
#             if not self.GetDocument().TesterExistanceGrilles({0:nomFichiers}):
#                 return []
#             
# #        print "  Fichiers :", nomFichiers
#         
#         prj = self.GetDocument().GetProjetRef()
#         
#         #
#         # Ouverture (et pré-sauvegarde) des fichiers grilles "source" (tableaux Excel)
#         #
#         tableaux = {}
#         for k, f in nomFichiers.items():
#             if os.path.isfile(f):
#                 tableaux[k] = grilles.getTableau(self.GetDocument().GetApp(), f)
#             else:
#                 if os.path.isfile(grilles.getFullNameGrille(prj.grilles[k][0])):
#                     tableaux[k] = grilles.getTableau(self.GetDocument().GetApp(),
#                                                      prj.grilles[k][0])
#                 else: # fichier original de grille non trouvé ==> nouvelle tentative avec les noms du référentiel par défaut
#                     prjdef = REFERENTIELS[self.GetDocument().GetTypeEnseignement()].getProjetDefaut()
#                     tableaux[k] = None
#                     messageErreur(self.GetDocument().GetApp(), u"Fichier non trouvé !",
#                                   u"Le fichier original de la grille,\n    " + prjdef.grilles[k][0] + u"\n" \
#                                   u"n'a pas été trouvé ! \n")
#                         
#             
#             if tableaux[k] != None: # and tableaux[k].filename !=f:
# #                print "      créé :", f
#                 try:
#                     tableaux[k].save(f, ConflictResolution = 2)
#                 except:
#                     messageErreur(self.GetDocument().GetApp(), u"Erreur !",
#                                   u"Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
#                                   u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
#                                   u" - que le dossier choisi n'est pas protégé en écriture"%f)
# 
#         if tableaux == None:
#             return []
#         
#         #
#         # Remplissage des grilles
#         #
#         log = []
#         if "beta" in version.__version__:
#             log = grilles.modifierGrille(self.GetDocument(), tableaux, self)
#         else:
#             try:
#                 log = grilles.modifierGrille(self.GetDocument(), tableaux, self)
#             except:
#                 messageErreur(self.GetDocument().GetApp(), u"Erreur !",
#                               u"Impossible de modifier les grilles !") 
# 
# 
#         #
#         # Enregistrement final des grilles
#         #
#         for k, t in tableaux.items():
#             try:
#                 t.save()
#             except:
#                 messageErreur(self.GetDocument().GetApp(), u"Erreur !",
#                               u"Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
#                               u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
#                               u" - que le dossier choisi n'est pas protégé en écriture" %f)
#             try:
#                 t.close()
#             except:
#                 pass
#             self.grille[k] = Lien(typ = 'f')
#             self.grille[k].path = toFileEncoding(nomFichiers[k])
#         
#         
#         #
#         # Message de fin
#         #
#         if messageFin:
#             t = u"Génération "
#             if len(tableaux)>1:
#                 t += u"des grilles"
#             else:
#                 t += u"de la grille"
#             t += u"\n\n"
#             t += u"\n".join(nomFichiers.values())
#             t += u"terminée avec "
#             if len(log) == 0:
#                 t += u"succès !"
#             else:
#                 t += u"des erreurs :\n"
#                 t += u"\n".join(log)
#             messageInfo(self.GetDocument().GetApp(), u"Génération terminée", t)
#             
#         
# #         self.GetPanelPropriete().MiseAJour()
#         return log
#         
#         
#     ######################################################################################  
#     def GetEvaluabilite(self, complet = False, compil = False):
#         """ Renvoie l'évaluabilité de l'élève
#             % conduite
#             % soutenance
#             ev, ev_tot, seuil
#             
#             compil = renvoie des dictionnaire plus simples
#         """ 
# #         print "GetEvaluabilite", self
#         prj = self.GetProjetRef()
# #        dicPoids = self.GetReferentiel().dicoPoidsIndicateurs_prj
#         dicIndicateurs = self.GetDicIndicateurs()
# #         print "   dicIndicateurs", dicIndicateurs
# #         print "   _dicoGrpIndicateur", prj._dicoGrpIndicateur
# #        tousIndicateurs = prj._dicIndicateurs
# #        lstGrpIndicateur = {'R' : prj._dicGrpIndicateur['R'],
# #                            'S' : self.GetProjetRef()._dicGrpIndicateur['S']}
# #        print lstGrpIndicateur
#         
# #        r, s = 0, 0
# #        ler, les = {}, {}
#         
# #        rs = [0, 0]
# #        lers = [{}, {}]
# #         print prj._dicoGrpIndicateur
# #         print "   _dicoIndicateurs", prj._dicoIndicateurs
#         rs = {}
#         lers = {}
#         for disc, dic in prj._dicoGrpIndicateur.items():
#             rs[disc] = {}
#             lers[disc] = {}
#             for ph in dic.keys():
#                 lers[disc][ph] = {}
#                 rs[disc][ph] = 0
# #         print "   xx init :", rs, lers
#         
#         
#         def getPoids(competence, code, poidsGrp):
# #             print "  getPoids", code
#             if competence.sousComp != {}:
#                 for k, c in competence.sousComp.items():
#                     getPoids(c, k, poidsGrp)
#             
# #             if competence.poids != {}:
#             for disc, dic in prj._dicoGrpIndicateur.items():
#                 for ph in dic.keys():
# #                     print "      ", ph
#                     if grp in dic[ph]:
# #                         print "_", dic[ph]
#                         for i, indic in enumerate(competence.indicateurs):
#                             
#                             if disc+code in dicIndicateurs.keys():
#                                 if dicIndicateurs[disc+code][i]:
# #                                     print "  comp", code, i, indic.poids, ph
#                                     poids = indic.poids
#                                     if ph in poids.keys():
#                                         if not ph in poidsGrp.keys():
#                                             print u"ERREUR poids", code, u"Faire \"Ouvrir et réparer\""
#                                         else:
#                                             p = 1.0*poids[ph]/100
#                                         
#                                             rs[disc][ph] += p * poidsGrp[ph]/100
#                                             if grp in lers[disc][ph].keys():
#                                                 lers[disc][ph][grp] += p
#                                             else:
#                                                 lers[disc][ph][grp] = p
#                             else:
#                                 if not grp in lers[disc][ph].keys():
#                                     lers[disc][ph][grp] = 0
#                             
#             return
#             
#             
#         
# #         def getPoids(listIndic, comp, poidsGrp):
# #             """ 
# #             """
# # #            print "getPoids", listIndic, comp, poidsGrp
# #             if type(listIndic)
# # 
# #             for disc, dic in prj._dicoGrpIndicateur.items():
# #                 for ph in dic.keys():
# #                     if grp in dic[ph]:
# #                         for i, indic in enumerate(listIndic):
# #                             if disc+comp in dicIndicateurs.keys():
# #                                 if dicIndicateurs[disc+comp][i]:
# #     #                                print "  comp", grp, comp, i, indic.poids, ph
# #                                     poids = indic.poids
# #                                     if ph in poids.keys():
# #                                         p = 1.0*poids[ph]/100
# #                                         rs[disc][ph] += p * poidsGrp[ph]/100
# #                                         if grp in lers[disc][ph].keys():
# #                                             lers[disc][ph][grp] += p
# #                                         else:
# #                                             lers[disc][ph][grp] = p
# #                             else:
# #                                 if not grp in lers[disc][ph].keys():
# #                                     lers[disc][ph][grp] = 0
# #                             
# #             return
#         
#         for typi, dico in prj._dicoIndicateurs.items():
#             for grp, grpComp in dico.items():
# #                 print "  >>> poids :", grpComp.poids
#                 getPoids(grpComp, grp, grpComp.poids)
#                 
#                 
#                 
#                 
#                 
# #                 titre = grpComp.intitule
# #                 dicComp = grpComp.sousComp
# #                 poidsGrp = grpComp.poids
# #                 
# #                 if type(dicComp) == list:                       # 1 niveau
# #                     getPoids(dicComp, grp, poidsGrp)
# #                 else:
# #                     for comp, lstIndic in dicComp.items():
# #     #                    print "      ", comp
# #                         if type(lstIndic[1]) == list:           # 2 niveaux
# #                             getPoids(lstIndic[1], comp, poidsGrp)    
# #                         else:                                   # 3 niveaux
# #                             for scomp, lstIndic2 in lstIndic.items():
# #                                 getPoids(lstIndic2[1], scomp, poidsGrp)
#                                 
#                                                                
# #        r, s = rs
# #        ler, les = lers
# #         print "   eval :", rs, lers
#          
#         # On corrige s'il n'y a qu'une seule grille (cas SSI jusqu'à 2014)
# #        if len(self.GetReferentiel().grilles_prj) == 1: 
# ##        if self.GetTypeEnseignement() == "SSI":
# #            r, s = r*2, s*2
# #            for l in ler.keys():
# #                ler[l] = ler[l]*2
# #            for l in les.keys():
# #                les[l] = les[l]*2
#             
# #        if "O8s" in les.keys():
# #            les["O8"] = les["O8s"]
# #            del les["O8s"]
#             
# #        print r, s, ler, les
#         
#         #
#         # Seuils d'évaluabilité
#         #
#         # liste des classeurs avec des grilles comprenant des colonne "non"
# #        classeurs = [i[0] for i in self.GetReferentiel().cellulesInfo_prj["NON"] if i[0] != '']
#         seuil = {}
#         for disc, dic in prj._dicoGrpIndicateur.items():
#             seuil[disc] = {}
#             for t in dic.keys():
#     #            if t in classeurs:
#     #            print "aColNon", self.GetReferentiel().aColNon
#                 if t in self.GetReferentiel().aColNon.keys() and self.GetReferentiel().aColNon[t]:
#                     seuil[disc][t] = 0.5  # s'il y a une colonne "non", le seuil d'évaluabilité est de 50% par groupe de compétence
#                 else:
#                     seuil[disc][t] = 1.0     # s'il n'y a pas de colonne "non", le seuil d'évaluabilité est de 100% par groupe de compétence
# #        print "seuil", seuil
#         ev = {}
#         ev_tot = {}
# #        for txt, le, ph in zip([r, s], [ler, les], prj._dicGrpIndicateur.keys()):
# 
#         for disc, dic in prj._dicoGrpIndicateur.items():
#             ev[disc] = {}
#             ev_tot[disc] = {}
#             for part in dic.keys():
#                 txt = rs[disc][part]
#                 txt = round(txt, 6)
#                 ev[disc][part] = {}
#                 ev_tot[disc][part] = [txt, True]
#                 for grp, tx in lers[disc][part].items():
#                     tx = round(tx, 6)
#                     ev[disc][part][grp] = [tx, tx >= seuil[disc][part]]
#                     ev_tot[disc][part][1] = ev_tot[disc][part][1] and ev[disc][part][grp][1]
#         
# #        print "   ", ev, ev_tot, seuil
#         if compil:
#             ev = ev["S"]
#             ev_tot = ev_tot["S"]
#             seuil = seuil["S"]
#         return ev, ev_tot, seuil
#         
#         
# #        if complet:
# #            return r, s, ler, les
# #        else:
# #            return r, s
#     

#     ######################################################################################  
#     def GetCompetences(self):
#         lst = []
#         for t in self.GetDocument().taches:
#             if self.id in t.eleves:
#                 lst.extend(t.competences)
#         lst = list(set(lst))
#         return lst
    
    
#     ######################################################################################  
#     def GetDicIndicateurs(self, limite = None):
#         """ Renvoie un dictionnaire des indicateurs que l'élève doit mobiliser
#              (pour tracé)
#                   clef = code compétence
#                 valeur = liste [True False ...] des indicateurs à mobiliser
#         """
#         indicateurs = {}
# #         print " GetDicIndicateurs", self.id
#         for t in self.GetDocument().taches: # Toutes les tâches du projet
#             if not t.phase in TOUTES_REVUES_SOUT:
#                 if self.id in t.eleves:     # L'élève est concerné par cette tâche
#                     if t.estPredeterminee():
#                         indicTache = t.GetDicIndicateursEleve(self) # Les indicateurs des compétences à mobiliser pour cette tâche
#                     else:
#                         indicTache = t.GetDicIndicateurs() # Les indicateurs des compétences à mobiliser pour cette tâche
#                     for c, i in indicTache.items():
#                         if c in indicateurs.keys():
#                             indicateurs[c] = [x or y for x, y in zip(indicateurs[c], i)]
#                         else:
#                             indicateurs[c] = i
# #         print "  ", indicateurs
#         return indicateurs
#         
#         
        
        
#     ######################################################################################  
#     def GetDicIndicateursRevue(self, revue):
#         """ Renvoie un dictionnaire des indicateurs que l'élève doit mobiliser AVANT une revue
#              (pour tracé)
#                   clef = code compétence
#                 valeur = liste [True False ...] des indicateurs à mobiliser
#         """
#         indicateurs = {}
# #        print " GetDicIndicateurs", self.id
#         for t in self.GetDocument().taches: # Toutes les tâches du projet
#             if t.code == revue:
#                 break
#             if self.id in t.eleves:     # L'élève est concerné par cette tâche
#                 indicTache = t.GetDicIndicateurs() # Les indicateurs des compétences à mobiliser pour cette tâche
#                 for c, i in indicTache.items():
#                     if c in indicateurs.keys():
#                         indicateurs[c] = [x or y for x, y in zip(indicateurs[c], i)]
#                     else:
#                         indicateurs[c] = i
#                 
#         return indicateurs
    
    
    
    
#     ######################################################################################  
#     def GetTaches(self, revues = False):
#         lst = []
#         for t in self.GetDocument().taches:
#             if revues and t.phase in TOUTES_REVUES_EVAL:
#                 lst.append(t)
#             elif self.id in t.eleves:
#                 if revues and t.phase == "Rev":
#                     lst.append(t)
#                 elif t.phase != "Rev":
#                     lst.append(t)
#             
#                     
# #        lst = list(set(lst))
#             
#         return lst
        
#     ######################################################################################  
#     def GrillesGenerees(self):
#         b = True
#         for g in self.grille.values():
#             b = b and len(g.path) > 0
#         return b
#     
    
    
    
    ######################################################################################  
    def getBranche(self):
#        print "getBranche groupe"
        # La classe
        groupe = ET.Element("Groupe")
        groupe.set("Type", self.typeEnseignement)
        groupe.set("Spe", " ".join(self.specialite))
        
        groupe.set("Id", str(self.id))
        groupe.set("Nom", self.nom)
        
        self.getBrancheImage(groupe, "Avatar")
        
        eleves = ET.SubElement(groupe, "Eleves")
        for e in self.eleves:
            eleves.append(e.getBranche())
            
        groupe.set("Etab", self.etablissement)
        groupe.set("Ville", self.ville)
        groupe.set("Acad", self.academie)
        
        return groupe
    
    ######################################################################################  
    def setBranche(self, branche, reparer = False):
#         print "setBranche groupe"
        self.typeEnseignement = branche.get("Type", self.GetReferentiel().Code)
        # Bug probable !!! à vérifier
        
        self.id  = eval(branche.get("Id", "0"))
        self.nom  = branche.get("Nom", "")
        
        self.setBrancheImage(branche, "Avatar")
        
        brancheEle = branche.find("Eleves")
        self.eleves = []
        for e in list(brancheEle):
            eleve = Eleve(self.GetDocument())
            eleve.setBranche(e)
            self.eleves.append(eleve)
            
        self.specialite = branche.get("Spe", "").split()
        
        
        #
        # Etablissement
        #
        self.etablissement = branche.get("Etab", self.GetDocument().classe.etablissement)
        self.ville = branche.get("Ville", self.GetDocument().classe.ville)
        self.academie = branche.get("Acad", self.GetDocument().classe.academie)
        
        return
    
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            listItems = [["Supprimer", 
                          functools.partial(self.GetDocument().SupprimerGroupe, item = itemArbre), 
                          scaleImage(images.Icone_suppr_groupe.GetBitmap())]]
    
            self.GetApp().AfficherMenuContextuel(listItems)
            

    ######################################################################################  
    def MiseAJourTypeEnseignement(self):
        return

    
    
    ######################################################################################  
    def MiseAJourCodeBranche(self):
        """ Met à jour les tags de durée de projet
            et d'évaluabilité
        """
#        print "MiseAJourCodeBranche", self
        #
        # Durée
        #
        duree = self.GetDuree()
        dureeRef = self.GetProjetRef().duree
#        print "   duree", duree, "/", dureeRef
        lab = " ("+str(int(duree))+"h) "
        self.codeBranche.SetLabel(lab)
        tol1 = constantes.DELTA_DUREE
        tol2 = constantes.DELTA_DUREE2
        taux = abs((duree-dureeRef)/dureeRef)*100
#        print "   taux", taux, "(", tol1, tol2, ")"
        t = "Durée de travail "
        if taux < tol1:
            self.codeBranche.SetBackgroundColour(COUL_OK)
            self.codeBranche.SetToolTip(t + "conforme")
        elif taux < tol2:
            self.codeBranche.SetBackgroundColour(COUL_BOF)
            self.codeBranche.SetToolTip(t + "acceptable")
        else:
            self.codeBranche.SetBackgroundColour(COUL_NON)
            if duree < dureeRef:
                self.codeBranche.SetToolTip(t + "insuffisante")
            else:
                self.codeBranche.SetToolTip(t + "trop importante")
                
        self.codeBranche.LayoutFit()


    ######################################################################################  
    def GetNomPrenom(self, disc = False):
        if self.GetDocument().classe.typeEnseignement != self.typeEnseignement:
            d = ' (' + REFERENTIELS[self.typeEnseignement].Enseignement[0] + ')'
        else:
            d = ""
            
        if self.nom == "":
            return self.titre.capitalize()+' '+str(self.id+1)+d
        else:
            return self.GetNom()+d
        
        
    ######################################################################################  
    def SetCode(self):
        t = self.GetNomPrenom()

        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
        
        
    ######################################################################################  
    def GetFicheHTML(self, param = None):
#        print "GetFicheHTML"
#        print self.GetProjetRef().listeParties
        dic = {}
        ligne = []
        for ph in self.GetProjetRef().listeParties:
            dic['coul'] = couleur.GetCouleurHTML(getCoulPartie(ph))
            dic['nom'] = self.GetProjetRef().parties[ph]
            dic['id'] = ph
            ligne.append("""<tr  id = "le%(id)s" align="right" valign="middle" >
<td><font color = "%(coul)s"><em>%(nom)s :</em></font></td>
</tr>""" %dic)

        ficheHTML = constantes.encap_HTML(constantes.BASE_FICHE_HTML_GROUPE)
        
        
        t = ""
        for l in ligne:
            t += l+"\n"

        ficheHTML = ficheHTML.replace('{{tab_eval}}', t)
        
        return ficheHTML




    ######################################################################################  
    def SetTip2(self):
#        print "SetTip2", self
        # Tip
        if hasattr(self, 'tip'):
            
#            self.tip.SetTexte(self.GetNomPrenom(), self.tip_nom)
            coulOK = couleur.GetCouleurHTML(COUL_OK)
            coulNON = couleur.GetCouleurHTML(COUL_NON)
            
            #
            # Durée
            #
            duree = self.GetDuree()
            lab = draw_cairo.getHoraireTxt(duree)
            if abs(duree-70) < constantes.DELTA_DUREE:
                coul = coulOK
            elif abs(duree-70) < constantes.DELTA_DUREE2:
                coul = couleur.GetCouleurHTML(COUL_BOF)
            else:
                coul = coulNON
            self.tip.AjouterCol("ld", lab, coul, bold = True)

            
            

            self.tip.SetPage()
            

            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre)
        for disc, dic in self.GetProjetRef()._dicoGrpIndicateur.items():
            for part in dic.keys():
                self.codeBranche.Add(disc+part)
        
#        if self.image == None or self.image == wx.NullBitmap:
        image = self.arbre.images[self.code]
#        else:
#            image = self.image.ConvertToImage().Scale(20, 20).ConvertToBitmap()
        self.branche = arbre.AppendItem(branche, "", data = self, wnd = self.codeBranche,
                                        image = image)
        self.codeBranche.SetBranche(self.branche)
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)
        
        self.SetCode()




    
####################################################################################
#
#   Classe définissant les propriétés d'un professeur
#
####################################################################################
class Prof(Personne):
    def __init__(self, doc, ident = 0):
        self.titre = "prof"
        self.code = "Prf"
        self.discipline = "Tec"
        self.referent = False
        
        Personne.__init__(self, doc, ident)
        Grammaire.__init__(self, "Professeur(s)$m")
        
    ######################################################################################  
    def GetAvatar(self):
        if self.image is None:
            return images.Icone_prof.GetBitmap()
        else:
            return self.image
        
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.encap_HTML(constantes.BASE_FICHE_HTML_PROF)
        
        
    ######################################################################################  
    def SetDiscipline(self, discipline):
        self.discipline = discipline
        self.SetTip()
        self.MiseAJourCodeBranche()
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.GetDocument().app.AfficherMenuContextuel([["Supprimer", 
                                                     functools.partial(self.GetDocument().SupprimerProf, item = itemArbre), 
                                                     scaleImage(images.Icone_suppr_prof.GetBitmap())]])
        
    ######################################################################################  
    def MiseAJourCodeBranche(self):
        self.arbre.SetItemBold(self.branche, self.referent)
        self.codeBranche.SetItalic()
#         if self.discipline <> 'Tec':
        self.codeBranche.SetLabel(" "+constantes.CODE_DISCIPLINES[self.discipline]+" ")
        self.codeBranche.SetToolTip(constantes.NOM_DISCIPLINES[self.discipline])
        
        # Réglage de du mode d'affichage de la couleur de la discipline
        if sum(constantes.COUL_DISCIPLINES[self.discipline]) > 1.5:
            self.codeBranche.SetBackgroundColour(couleur.GetCouleurWx(constantes.COUL_DISCIPLINES[self.discipline]))
            self.codeBranche.SetForeroundColour(wx.BLACK)
        else:
            self.codeBranche.SetBackgroundColour(wx.WHITE)
            self.codeBranche.SetForegroundColour(couleur.GetCouleurWx(constantes.COUL_DISCIPLINES[self.discipline]))
            
        
        self.codeBranche.LayoutFit()
    
    ######################################################################################  
    def SetTip2(self):
        if hasattr(self, 'tip'):
            if self.discipline != 'Tec':
                coul = couleur.GetCouleurHTML(constantes.COUL_DISCIPLINES[self.discipline])
            else:
                coul = None
            self.tip.SetWholeText("spe", constantes.NOM_DISCIPLINES[self.discipline], fcoul = coul)
            
#            self.tip.AjouterCol("spe", constantes.NOM_DISCIPLINES[self.discipline], bcoul = coul)
            self.tip.SetPage()
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = CodeBranche(arbre)
#        self.codeBranche = wx.Panel(self.arbre, -1)
#        sz = wx.BoxSizer(wx.HORIZONTAL)
#        self.codeDisc = wx.StaticText(self.codeBranche, -1, "")
#        sz.Add(self.codeDisc)
#        self.codeBranche.SetSizerAndFit(sz)
        
#        if self.image == None or self.image == wx.NullBitmap:
        image = self.arbre.images[self.code]
#        else:
#            image = self.image.ConvertToImage().Scale(20, 20).ConvertToBitmap()
        self.branche = arbre.AppendItem(branche, "", data = self, wnd = self.codeBranche,
                                        image = image)
        self.codeBranche.SetBranche(self.branche)
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)
        self.SetCode()
        self.MiseAJourCodeBranche()

