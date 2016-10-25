#!/usr/bin/env python
# -*- coding: utf-8 -*-
from draw_cairo_seq import BCoulSeance


##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               wx_pysequence                             ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014 Cédrick FAURY - Jean-Claude FRICOU

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
wx_pysequence.py

pySéquence : aide à la réalisation de fiches de séquence pédagogiques
et à la validation de projets

Copyright (C) 2011-2015
@author: Cedrick FAURY

"""

import wx
from wx.lib.embeddedimage import PyEmbeddedImage

import glob

import os, sys
if sys.platform == "win32" :
    # Pour lire les classeurs Excel
    import recup_excel
    
import version
import textwrap
import grilles

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
                        strEffectifComplet, getElementFiltre, \
                        CHAR_POINT, COUL_PARTIE, getCoulPartie, COUL_ABS, \
                        TOUTES_REVUES_EVAL, TOUTES_REVUES_EVAL_SOUT, TOUTES_REVUES_SOUT, TOUTES_REVUES, \
                        _S, _Rev, _R1, _R2, _R3, \
                        revCalculerEffectifs, getSingulierPluriel,\
                        COUL_OK, COUL_NON, COUL_BOF, COUL_BIEN, \
                        toList, COUL_COMPETENCES
import constantes

from util_path import toFileEncoding, toSystemEncoding, FILE_ENCODING, SYSTEM_ENCODING

# Widgets partagés
# des widgets wx évolués "faits maison"
from widgets import Variable, VariableCtrl, VAR_REEL_POS, EVT_VAR_CTRL, VAR_ENTIER_POS, \
                    messageErreur, getNomFichier, pourCent2, testRel, \
                    rallonge, remplaceCode2LF, dansRectangle, \
                    StaticBoxButton, TextCtrl_Help, CloseFenHelp, \
                    remplaceLF2Code, messageInfo, messageYesNo, enregistrer_root, \
                    getAncreFenetre#, chronometrer
                    
from Referentiel import REFERENTIELS, ARBRE_REF, ACTIVITES
import Referentiel


from richtext import XMLtoHTML

# Pour enregistrer en xml
import xml.etree.ElementTree as ET
Element = type(ET.Element(None))

from wx_pysequence import CodeBranche, PopupInfo, getIconeFileSave, getIconeCopy, \
                            getBitmapFromImageSurface, img2str, getIconePaste, \
                            PanelPropriete_Progression, \
                            PanelPropriete_CI, PanelPropriete_LienSequence,\
                            PanelPropriete_Classe, PanelPropriete_Sequence, \
                            PanelPropriete_Projet, PanelPropriete_Competences, \
                            PanelPropriete_Savoirs, PanelPropriete_Seance, \
                            PanelPropriete_Tache, PanelPropriete_Systeme, \
                            PanelPropriete_Support, PanelPropriete_LienProjet,\
                            PanelPropriete_Personne, getDisplayPosSize, URLDialog




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
    
    
    
    
#    liste = node.getElementById(idListe)
#    if liste != None:
#        _dt = node.createElement("li")
#        txt = node.createTextNode(li)
#        _dt.appendChild(txt)
#        liste.appendChild(_dt)
        

#def AjouterImg(node, item, bmp):
##        print "AjouterImg"
#
#    img = node.find(id = item)
#    try:
#        bmp.SaveFile(self.tfname, wx.BITMAP_TYPE_PNG)
#    except:
#        return
#    
#    img = node.getElementById(item)
#    if img != None:
#        td = node.createElement("img")
#        img.appendChild(td)
#        td.setAttribute("src", self.tfname)
            

        

    
    
    
    
####################################################################################
#
#   Objet lien vers un fichier, un dossier ou bien un site web
#
####################################################################################
class Lien():
    def __init__(self, path = u"", typ = ""):
        self.path = path # Impérativement toujours encodé en FILE_ENCODING !!
        self.type = typ
        
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
        path = self.GetAbsPath(pathseq)
#        print "Afficher", path
        
        if self.type == "f":
            try:
                os.startfile(path)
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'ouvrir le fichier\n\n%s\n" %toSystemEncoding(path))
                
        elif self.type == 'd':
            try:
                subprocess.Popen(["explorer", path])
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'accéder au dossier\n\n%s\n" %toSystemEncoding(path))
            
        elif self.type == 'u':
            try:
                webbrowser.open(self.path)
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'ouvrir l'url\n\n%s\n" %toSystemEncoding(self.path))
        
        elif self.type == 's':
            if os.path.isfile(path):
#                self.Show(False)
                child = fenSeq.commandeNouveau()
                child.ouvrir(path)

  
    ######################################################################################  
    def EvalTypeLien(self, pathseq):
        path = self.GetAbsPath(pathseq)
        
        if os.path.exists(path):
            if os.path.isfile(path):
                self.type = 'f'
                
            elif os.path.isdir(path):
                self.type = 'd'

        else:
            self.type = 'u'
        
                
    ######################################################################################  
    def EvalLien(self, path, pathseq):
        """ Teste la validité du chemin <path> (SYSTEM_ENCODING)
            et change self.path (FILE_ENCODING)
            <pathseq> doit être en FILE_ENCODING
        """
        if path == "" or path.split() == []:
            self.path = r""
            self.type = ""
            return
        
        path = toFileEncoding(path)
#        pathseq = toFileEncoding(pathseq)
        abspath = self.GetAbsPath(pathseq, path)
        
        relpath = testRel(abspath, pathseq)
        if os.path.exists(relpath):
            if os.path.isfile(relpath):
                self.type = 'f'
                self.path = relpath
            elif os.path.isdir(relpath):
                self.type = 'd'
                self.path = relpath
        else:
            self.type = 'u'
            self.path = path
        
              
    ######################################################################################  
    def GetAbsPath(self, pathseq, path = None):
        """ Renvoie le chemin absolu du lien
            grace au chemin de l'application <pathseq>
        """
        if path == None:
            path = self.path
        
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
        branche.set("Lien", toSystemEncoding(self.path))
        branche.set("TypeLien", self.type)
        
        
    ######################################################################################  
    def setBranche(self, branche, pathseq):
        self.path = toFileEncoding(branche.get("Lien", r""))
        self.type = branche.get("TypeLien", "")
        if self.type == "" and self.path != r"":
            self.EvalTypeLien(pathseq)
        return True

    
####################################################################################
#
#   Classe définissant les propriétés d'une séquence ou d'un projet
#
####################################################################################
Titres = [u"Séquence pédagogique",
          u"Prérequis",
          u"Objectifs pédagogiques",
          u"Séances",
          u"Systèmes et matériels",
          u"Classe",
          u"Elèves",
          u"Support",
          u"Tâches",
          u"Projet", 
          u"Equipe pédagogique",
          u"Séquences et Projets", 
          u"Progression"]

class ElementDeSequence():
    def __init__(self):
        self.lien = Lien()
        
    
    ######################################################################################  
    def GetPath(self):
        return self.parent.GetPath()
    
    ######################################################################################  
    def GetLien(self):
        return self.lien.path
    
    ######################################################################################  
    def GetLienHTML(self):
        if self.lien.type in ['f', 'd', 's']:
            if self.lien.path != '':
                return toSystemEncoding('file:///' + os.path.abspath(self.lien.path))
            else:
                return ''
        else:
            return toSystemEncoding(self.lien.path)
    
    ######################################################################################  
    def CreerLien(self, event):
        self.lien.DialogCreer(self.GetPath())
        self.SetLien()
        if hasattr(self, 'panelPropriete'): 
            self.GetApp().sendEvent(modif = u"Création d'un lien")
    
    
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
        
        



######################################################################################  
def GetObjectFromClipBoard(instance):
    try:
        b = ET.fromstring(pyperclip.paste())
    except:
        b = None

    if isinstance(b, Element): # Le presse contient un Element
        if b.tag[:len(instance)] == instance: # Le presse contient une instance attendue
            return b
    return None


######################################################################################  
#
#   Objet_sequence
#
######################################################################################  
class Objet_sequence():
    def __init__(self):
        
        #
        # Création du Tip (PopupInfo)
        #
        self.tip = PopupInfo(self.GetApp().parent, "")
        
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

    ######################################################################################  
    def getBranche_TOTAL(self, listElem):
        root = ET.Element(self.nom_obj)
        for e in listElem:
            self.getBranche_AUTO(root, e, getattr(self, e))
        return root

    ######################################################################################  
    def getIcone(self):
        return wx.NullBitmap
    
    ######################################################################################  
    def getBranche_AUTO(self, branche, nom, v):
        if hasattr(v, 'getBranche'):
            branche.append(v.getBranche())
        elif isinstance(v, list):
            self.getBrancheList(branche, nom, v)
        else:
            branche.set(nom, v)
        
    ######################################################################################  
    def getBrancheList(self, branche, nom, dic):
        b = ET.SubElement( branche, nom)
        for obj in dic.values():
            b.append(obj.getBranche())
    
    
    ######################################################################################  
    def setBranche_TOTAL(self, branche):   
        return

    
    ######################################################################################  
    def CopyToClipBoard(self, event = None):
        pyperclip.copy(ET.tostring(self.getBranche()))
        
    ######################################################################################  
    def SetToolTip(self, toolTip):
        self.toolTip = toolTip
        
    ######################################################################################  
    def SetDescription(self, description):
        if self.description != description:
#            print "SetDescription", self.nom_obj, self
            self.description = description
            self.GetApp().sendEvent(modif = u" ".join([u"Modification de la description", 
                                                                 self.article_c_obj, self.nom_obj]))
#            self.tip.SetRichTexte()

    ######################################################################################  
    def EnrichiSVG(self, doc, seance = False):
        """ Enrichissement de l'image SVG <doc> (format XML) avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens 
             - ...
        """
#        print "EnrichiSVG", self, doc, seance
        # 
        # Le titre de la page
        #
        pid = ''
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
                
                n = range(len(self.cadre))
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
                lien = lien.encode('utf-8')
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
        """
        lst = []
        if hasattr(self, 'pts_caract' ):
            for i, pt in enumerate(self.pts_caract):
                lst.append((pt, self, i))
        
        if hasattr(self, 'pt_caract' ):
            lst.append((self.pt_caract[0], self, self.pt_caract[1]))
            
        self.cadre = []
        return lst
    
    
    ######################################################################################  
    def GetDescription(self):
        return
#        if hasattr(self, 'panelPropriete'):
#            pp = self.GetPanelPropriete()
#            if hasattr(pp, 'rtc'):
#                return pp.rtc.GetValue()
            
    ######################################################################################  
    def GetBulleSVG(self, i):
        des = ""
#        if hasattr(self, 'description'):
#            des = "\n\n" + self.GetDescription()
            
        if self.GetDescription() != None:
            des = "\n\n" + self.GetDescription()
        t = self.GetCode(i) + " :\n" + self.GetIntit(i) + des
        return t.encode(SYSTEM_ENCODING)#.replace("\n", "&#10;")#"&#xD;")#
    
           
           
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


    ######################################################################################  
    def GetProjetRef(self):
        return self.GetDocument().GetProjetRef()


    ######################################################################################  
    def GetFicheHTML(self, param = None):
        if param is None:
            return constantes.BASE_FICHE_HTML
        else:
            if param == "CAL":
                return constantes.BASE_FICHE_HTML_CALENDRIER
            
            elif param == "PB":
                return constantes.BASE_FICHE_HTML_PROB
                
            elif param == "ANN":
                pass
                
            elif param[:3] == "POS":
                return constantes.BASE_FICHE_HTML_PERIODES
                
            elif param[:3] == "EQU":
                pass
            
            elif param[:2] == "CI":
                return constantes.BASE_FICHE_HTML_CI
                
            else:
                pass
            
        return constantes.BASE_FICHE_HTML

        
        
    ######################################################################################  
    def GetProfondeur(self):
        return 0  
        
        
        

class Classe(Objet_sequence):
    def __init__(self, app, intitule = u"", 
                 pourProjet = False, typedoc = ''):
        self.app = app
        Objet_sequence.__init__(self)
        
        self.intitule = intitule
        
        self.undoStack = UndoStack(self)
        
        self.verrouillee = False
        
        
        self.academie = u""
        self.ville = u""
        self.etablissement = u""
        self.effectifs = {}
        self.nbrGroupes = {}
        self.systemes = []
        
        
#        self.panelParent = panelParent
        
        self.Initialise(pourProjet)
        
        self.undoStack.do(u"Création de la Classe")
            
        

        
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
            self.codeBranche.SetLabel(self.GetReferentiel().Enseignement[0])
        
#        self.CI = self.options.optClasse["CentresInteret"]
#        self.posCI = self.options.optClasse["PositionsCI"]
        
#        self.ci_SSI = self.options.optClasse["CentresInteretSSI"]
#        self.ci_ET = self.options.optClasse["CentresInteretET"]
#        self.posCI_ET = self.options.optClasse["PositionsCI_ET"]
        

#    ######################################################################################  
#    def SetCI(self, num, ci):
#        self.CI[num] = ci
        
    ######################################################################################  
    def setDefaut(self):
#        print "setDefaut Classe"
        self.typeEnseignement = 'SSI'
            
        self.effectifs['C'] = constantes.Effectifs["C"]
        self.nbrGroupes = {"G" : constantes.NbrGroupes["G"],
                           "E" : constantes.NbrGroupes["E"],
                           "P" : constantes.NbrGroupes["P"]}
        
        self.academie = u""
        self.ville = u""
        self.etablissement = u""
        
        self.systemes = []


    ######################################################################################  
    def Initialise(self, pourProjet, defaut = False):
        
        # Força "défaut" ou pas de fichier Classe dans les options
        if defaut or self.GetApp().parent.options.optClasse["FichierClasse"] == r"":
            self.setDefaut()
            
        else:
            # Impossible de charger le fichier Classe
            if not self.ouvrir(self.GetApp().parent.options.optClasse["FichierClasse"]):
                self.setDefaut()
            
            
        self.referentiel = REFERENTIELS[self.typeEnseignement]    
        
        # On vérifie que c'est bien un type d'enseignement avec projet
        if pourProjet:
            if not self.typeEnseignement in [ref.Code for ref in REFERENTIELS.values() if len(ref.projets) > 0]:
                self.typeEnseignement = constantes.TYPE_ENSEIGNEMENT_DEFAUT
                self.referentiel = REFERENTIELS[self.typeEnseignement]
        else:    
            self.MiseAJourTypeEnseignement()
        
        self.familleEnseignement = self.GetReferentiel().Famille  
        
        
        
        calculerEffectifs(self)


    ######################################################################################  
    def SetDocument(self, doc):   
        self.doc = doc 


    ###############################################################################################
    def ouvrir(self, nomFichier):
        print "Ouverture classe", nomFichier
        
        try:
            fichier = open(nomFichier,'r')
    
            root = ET.parse(fichier).getroot()
            self.setBranche(root)
            
            fichier.close()
            self.app.fichierClasse = nomFichier
            
            return True

        except:
            print "Erreur Ouverture classe", nomFichier
            return False
        
#        self.MiseAJour()


    ######################################################################################  
    def getBranche(self):
#        print "getBranche classe"
        # La classe
        classe = ET.Element("Classe")
        classe.set("Type", self.typeEnseignement)
        
        classe.set("Version", version.__version__) # à partir de la version 6
        
        classe.append(self.referentiel.getBranche())
        
        classe.set("Etab", self.etablissement)
        classe.set("Ville", self.ville)
        classe.set("Acad", self.academie)
        
        eff = ET.SubElement(classe, "Effectifs")
        eff.set('eC', str(self.effectifs['C']))
        eff.set('nG', str(self.nbrGroupes['G']))
        eff.set('nE', str(self.nbrGroupes['E']))
        eff.set('nP', str(self.nbrGroupes['P']))
                     
#        print "   ", self.systemes
        systeme = ET.SubElement(classe, "Systemes")
        for sy in self.systemes:
            if sy.nom != u"":
                systeme.append(sy.getBranche())
        
        return classe
    
    ######################################################################################  
    def setBranche(self, branche, reparer = False):
        err = []
#        print "setBranche classe"
        self.typeEnseignement = branche.get("Type", constantes.TYPE_ENSEIGNEMENT_DEFAUT)
        
        self.version = branche.get("Version", "0")       # A partir de la version 6 !
        
        #
        # Référentiel
        #
        def ChargerRefOriginal():
            print u"Réparation = pas référentiel intégré !"
            if self.GetVersionNum() >= 5:
                code = self.referentiel.setBrancheCodeV5(brancheRef)
                print u"   Code trouvé dans référentiel :", code
                if code != self.typeEnseignement:
                    self.typeEnseignement = code
                    
            print u"   TypeEnseignement :", self.typeEnseignement
            if self.typeEnseignement in REFERENTIELS:
                self.referentiel = REFERENTIELS[self.typeEnseignement]
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
#                print "VersionNum", self.GetVersionNum()
#                versionNum = self.GetVersionNum()
                if self.GetVersionNum() <= 6:
                    ChargerRefOriginal()
                    RecupCI()
                else:
                    try:
                        self.referentiel.initParam()
                        errr = self.referentiel.setBranche(brancheRef)[1]
    #                        print "errr", errr
                        self.referentiel.corrigerVersion(errr)
                        self.referentiel.postTraiter()
                        self.referentiel.completer(forcer = True)

                    except:
                        self.referentiel.initParam()
                        self.referentiel.setBrancheV5(brancheRef)
                        ChargerRefOriginal()
                        RecupCI()



        #
        # Version < 5 !
        #
        else:
            ChargerRefOriginal()
            RecupCI()
        
        # Correction contradiction 
        if self.typeEnseignement != self.referentiel.Code:
            print "Correction type enseignement", self.typeEnseignement, ">>", self.referentiel.Code
            self.typeEnseignement = self.referentiel.Code

        
            

        #
        # Etablissement
        #
        self.etablissement = branche.get("Etab", u"")
        self.ville = branche.get("Ville", u"")
        self.academie = branche.get("Acad", u"")
        
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
            
#        self.GetPanelPropriete().MiseAJour()
            
        return err
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
#        print "ConstruireArbre", self.GetReferentiel().Enseignement[0]
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre, rallonge(self.GetReferentiel().Enseignement[0]))
        self.branche = arbre.AppendItem(branche, Titres[5]+" :", wnd = self.codeBranche, data = self)#, image = self.arbre.images["Seq"])
        self.codeBranche.SetBranche(self.branche)
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)
    
    

    ######################################################################################  
    def GetEffectifNorm(self, eff):
        """ Renvoie les effectifs des groupes sous forme normalisée
            (portion de classe entière)
        """
        if eff == 'C':
            return 1.0
        elif eff == 'G':
            return 1.0 / self.nbrGroupes['G']
        elif eff == 'D':
            return self.GetEffectifNorm('G') / 2
        elif eff == 'E':
            return self.GetEffectifNorm('G') / self.nbrGroupes['E']
        elif eff == 'P':
            return self.GetEffectifNorm('G') / self.nbrGroupes['P']
        
        
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
    def Verrouiller(self, etat):
#        print "verrouiller classe", etat
        self.verrouillee = etat
#        self.GetPanelPropriete().Verrouiller(etat)
        if not etat:
            couleur = 'white'
            message = u""
        else:
            couleur = COUL_OK
            message = u"Les paramètres de la classe sont verrouillés !\n" \
                      u"Pour pouvoir les modifier, supprimer le centre d'intérêt\n"\
                      u"ainsi que les prérequis et les objectifs."
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetBackgroundColour(couleur)
            self.codeBranche.SetToolTipString(message)
            self.codeBranche.Refresh()

####################################################################################################
#
# Classe définissant les documents principaux
#        base : BaseDoc
#        héritiers : Sequence et Projet
#
####################################################################################################
class BaseDoc():   
    def __init__(self, app, classe = None, intitule = ""):
        self.intitule = intitule
        self.classe = classe
        self.app = app  # de type FenentreDocument
        self.centrer = True
        
        self.position = 0   # Position de la séquence/projet dans la période d'enseignement
        
        self.commentaires = u""
        
        self.dependants = [] # Liste de documents dépendants (à enregistrer aussi)

        self.undoStack = UndoStack(self)
        
        #
        # Création du Tip (PopupInfo)
        #
        self.tip = PopupInfo(self.GetApp().parent, "")
        
        
          
    ######################################################################################  
    def GetApp(self):
        return self.app
    
    ######################################################################################  
    def GetPath(self):
        if hasattr(self.app, 'fichierCourant'):
            return os.path.split(self.app.fichierCourant)[0]
        else:
            return r""
    
    ######################################################################################  
    def GetNbrPeriodes(self):
        return sum([p for a, p in self.GetReferentiel().periodes])


    ######################################################################################  
    def estProjet(self):
        return isinstance(self, Projet)
    

    ######################################################################################  
    def GetApercu(self, w = 210, h = -1, entete = False):
        imagesurface = self.draw.get_apercu(self, w, entete = entete)
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
        if hasattr(self, 'tip'):
            if pos is not None:
                x, y = pos
#                 print x, y
                X, Y, W, H = self.tip.GetRect()
#                 print X, Y, W, H
                if x > X and x < X+W and y > Y and y < Y+H:
                    return
            self.tip.Show(False)
        
        if hasattr(self, 'call'):
            self.call.Stop()
            
            
    ######################################################################################  
    def HitTest(self, x, y):
        """ >> Renvoie la Zone sensible sous le point x, y
        """
#        print "HitTest"
        for z in self.zones_sens:
            if z.dansRectangle(x, y):
#                print "   xxx", z
                return z
        return


    ######################################################################################  
    def GererDependants(self, obj, t):
        """ Gestion des documents qui dépendent du présent document
        """
        print "GererDependants", t
        obj.GetApp().sendEvent(modif = t, obj = self)
        if self.GetApp() == obj.GetApp(): # la séquence n'est pas ouverte dans une autre fenêtre
            self.dependants.append(obj)
        else:
            self.GetApp().sendEvent(modif = t, obj = self)
        
        
    ######################################################################################  
    def Click(self, zone, x, y):
#         print "Click", zone
        self.HideTip()
        
        if zone.obj is not None:
            if zone.param is None:
                if hasattr(zone.obj, "branche"):
                    self.SelectItem(zone.obj.branche, depuisFiche = True)
                elif hasattr(zone.obj, "branchePre"):
                    self.SelectItem(zone.obj.branchePre, depuisFiche = True)
            
            else:
                if isinstance(zone.obj, Sequence) and len(zone.param) > 2 and zone.param[:2] == "CI":
                    ref = self.GetReferentiel()
                    zone.obj.CI.ToogleNum(int(zone.param[2:]))
                    t = u"Modification des "+ ref.nomCI + " de la Séquence"
                    pp = self.GetApp().GetPanelProp()
                    if hasattr(pp, "MiseAJourApercu"):
                        pp.MiseAJourApercu()
                    self.GererDependants(zone.obj, t)
                
                elif isinstance(zone.obj, Sequence) and len(zone.param) > 3 and zone.param[:3] == "CMP":
                    ref = self.GetReferentiel()
                    zone.obj.obj['C'].ToogleCode("S"+zone.param[3:])
                    t = u"Modification des "+ getSingulierPluriel(ref.dicoCompetences["S"].nomGenerique, True) + " visées par la Séquence"
                    pp = self.GetApp().GetPanelProp()
                    if hasattr(pp, "MiseAJourApercu"):
                        pp.MiseAJourApercu()
                    self.GererDependants(zone.obj, t)
                        
        
        elif zone.param is not None:
            if len(zone.param) > 3 and zone.param[:3] == "POS" :
                if not self.classe.verrouillee:
                    self.SetPosition(int(zone.param[3]))
#                    self.GetPanelPropriete().SetBitmapPosition()
                    pp = self.GetApp().GetPanelProp()
                    if hasattr(pp, "SetBitmapPosition"):
                        pp.SetBitmapPosition()
#                    self.GetApp().arbre.OnSelChanged()
                    self.GetApp().sendEvent(modif = u"Changement de position "+ self.article_c_obj + " " + self.nom_obj,
                                            obj = self)
            
            elif zone.param == "PB":
                self.SelectItem(self.branche, depuisFiche = True)
            
            elif zone.param == "EQU":
                self.SelectItem(self.branchePrf, depuisFiche = True)
            


    ######################################################################################  
    def Move(self, zone, x, y):
#         print "Move", x, y
        self.HideTip()
            
        tip = None 
        if zone.obj is not None and zone.param is None and type(zone.obj) != list:
#             print "    elem :", zone.obj
            if hasattr(zone.obj, 'tip'):
                zone.obj.SetTip()
                tip = zone.obj.tip
            
#            if hasattr(zone.obj, "branche"):
#                elem = zone.obj.branche.GetData()
#                
#                if hasattr(elem, 'tip'):
#                    elem.SetTip()
#                    tip = elem.tip
        
        else:
#             print "    zone", zone.param
            tip = self.SetTip(zone.param, zone.obj)
            
        if tip != None:
            X, Y, W, H = getDisplayPosSize()

#             print "  tip", x, y, tip.GetSize()

            w, h = tip.GetSize()
            tip.Position(getAncreFenetre(x, y, w, h, W, H, 10), (0,0))
            self.call = wx.CallLater(500, tip.Show, True)
            self.tip = tip


    ######################################################################################  
    def MiseAJourListeSystemesClasse(self):
        return


    ######################################################################################  
    def AjouterProf(self, event = None):
        if len(self.equipe) < 5:
            e = Prof(self, len(self.equipe))
            self.equipe.append(e)
            e.ConstruireArbre(self.arbre, self.branchePrf)
            self.arbre.Expand(self.branchePrf)
            self.GetApp().sendEvent(modif = u"Ajout d'un professeur")
            self.arbre.SelectItem(e.branche)

    
    ######################################################################################  
    def SupprimerProf(self, event = None, item = None):
        e = self.arbre.GetItemPyData(item)
#        i = self.equipe.index(e)
        self.equipe.remove(e)
        self.arbre.Delete(item)
        self.GetApp().sendEvent(modif = u"Suppression d'un professeur")


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
            self.tip.SetWholeText("titre", u"Découpage de la formation en périodes")
            self.tip.SetWholeText("txt", u"Périodes occupées pendant la Progression")
            self.tip.AjouterImg("img", self.getBitmapPeriode(300))
        else:
            ref = self.GetReferentiel()
            self.tip.SetWholeText("titre", u"Période de formation")
            self.tip.SetWholeText("txt", ref.getPeriodesListe()[p] + " - " + str(p+1))
            self.tip.Supprime('img')


    ##################################################################################################    
    def Tip_EQU(self, typeDoc):
        self.tip.SetWholeText("titre", u"Equipe pédagogique impliquée dans " + typeDoc)



    
####################################################################################################          
class Sequence(BaseDoc, Objet_sequence):
    def __init__(self, app, classe = None, intitule = u"Intitulé de la séquence pédagogique",
                 ouverture = False):
        BaseDoc.__init__(self, app, classe, intitule)
        Objet_sequence.__init__(self)
        
        self.nom_obj = u"Séquence"
        self.article_c_obj = u"de la"
        self.article_obj = u"la"
        
        self.prerequis = Savoirs(self, prerequis = True)
        self.prerequisSeance = []
        
        self.equipe = []
        
        self.domaine = ""   # M E I
        
        self.CI = CentreInteret(self)
        
        self.obj = {"C" : Competences(self),
                    "S" : Savoirs(self)}
        self.systemes = []
        self.seances = [Seance(self)]

        if not ouverture:
            self.MiseAJourTypeEnseignement()
            
        # Le module de dessin
        self.draw = draw_cairo_seq
        
        self.undoStack.do(u"Création de la Séquence")


    ######################################################################################  
    def __repr__(self):
        return u"Séquence" + self.intitule


    ######################################################################################  
    def GetType(self):
        return 'seq'


    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Sequence(parent, self)


    ######################################################################################  
    def Initialise(self):
        self.AjouterListeSystemes(self.classe.systemes)
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
        lst = []
        lst.extend(self.obj["C"].GetPtCaract())
        lst.extend(self.obj["S"].GetPtCaract())
        lst.extend(self.prerequis.GetPtCaract())
        lst.extend(self.CI.GetPtCaract())
        for s in self.seances:
            lst.extend(s.GetPtCaract())
        return lst    
    
    
    ######################################################################################  
    def EnrichiSVGdoc(self, doc):
        """ Enrichissement de l'image SVG <doc> (format XML) avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens 
             - ...
        """
#        print "EnrichiSVG sequence"
        if hasattr(self, 'app'):
            t = doc.createElement("title")
            txt = doc.createTextNode(os.path.split(self.app.fichierCourant)[1])
            t.appendChild(txt)
            svg = doc.getElementsByTagName("svg")[0]
            svg.insertBefore(t, svg.childNodes[0])
            
        self.obj["C"].EnrichiSVG(doc)
        self.obj["S"].EnrichiSVG(doc)
        self.prerequis.EnrichiSVG(doc)
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
    def getBranche(self):
        """ Renvoie la branche XML de la séquence pour enregistrement
        """
        # Création de la racine
        sequence = ET.Element("Sequence")
        
        sequence.set("Intitule", self.intitule)

        if self.commentaires != u"":
            sequence.set("Commentaires", self.commentaires)
        
        sequence.set("Domaine", self.domaine)

        sequence.set("Position", str(self.position))

        equipe = ET.SubElement(sequence, "Equipe")
        for p in self.equipe:
            equipe.append(p.getBranche())
            
        sequence.append(self.CI.getBranche())
        
        prerequis = ET.SubElement(sequence, "Prerequis")
        prerequis.append(self.prerequis.getBranche())
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
            systeme.append(sy.getBranche())
        
        return sequence


    ######################################################################################  
    def setBranche(self, branche):
        """ Lecture d'une branche XML de séquence
        """
#        print "setBranche séquence"
#        t0 = time.time()
        self.intitule = branche.get("Intitule", u"")
        
        self.commentaires = branche.get("Commentaires", u"")
        
        self.domaine = branche.get("Domaine", "")
        
        self.position = eval(branche.get("Position", "0"))

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
            self.prerequis.setBranche(savoirs)
            lst = list(branchePre)
            lst.remove(savoirs)
            self.prerequisSeance = []
            for bsp in lst:
                sp = LienSequence(self)
                sp.setBranche(bsp)
                self.prerequisSeance.append(sp)
        
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
            if systeme.lienClasse == None or  not systeme.lienClasse in [s.lienClasse for s in self.systemes]:
                self.systemes.append(systeme)    

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
        
        
        
#        self.GetPanelPropriete().MiseAJour()

        
#        t5 = time.time()
#        print "  t5", t5-t4
        
    ######################################################################################  
    def SetCodes(self):
#        self.CI.SetNum()
#        for comp in self.obj:
#            comp.SetCode()
#        self.obj["C"].SetCode()
#        self.obj["S"].SetCode()
        
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
    def SetTip(self, param = None, obj = None):
        """ Mise à jour du TIP (popup)
        """
        
        if param is None:   # la Séquence elle-même
            self.tip.SetHTML(constantes.BASE_FICHE_HTML_SEQ)
            self.tip.SetWholeText("int", self.intitule)
        
        else:               # Un autre élément de la Séquence
            self.tip.SetHTML(self.GetFicheHTML(param = param))
            if param == "POS":
                self.Tip_POS()
                
            elif param[:3] == "POS":
                self.Tip_POS(int(param[3])) 
                
            elif param[:3] == "EQU":
                self.Tip_EQU("la Séquence")
                
            elif type(obj) == list:
                pass
                
            else:
                pass
                
        self.tip.SetPage()
        return self.tip


    ######################################################################################  
    def VerifPb(self):
#        print "VerifPb"
        for s in self.seances:
            s.VerifPb()


    ######################################################################################  
    def MiseAJourNomsSystemes(self):
        for s in self.seances:
            s.MiseAJourNomsSystemes()
    
    ######################################################################################  
    def AjouterSystemeSeance(self):
        for s in self.seances:
            s.AjouterSysteme()
            
    ######################################################################################  
    def AjouterListeSystemesSeance(self, lstSys):
        for s in self.seances:
            s.AjouterListeSystemes(lstSys)
            
    ######################################################################################  
    def SupprimerSystemeSeance(self, i):
        for s in self.seances:
            s.SupprimerSysteme(i) 
            
    ######################################################################################  
    def CollerElem(self, event = None, bseance = None):
        """ Colle la séance présente dans le presse-papier (branche <bseance>)
            en première position
        """
#        print "CollerElem 1ere pos"
        
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
        
        self.GetApp().sendEvent(modif = u"Collé d'un élément")
        
        self.arbre.SelectItem(seance.branche)    


    ######################################################################################  
    def AjouterSeance(self, event = None):
        seance = Seance(self)
        self.seances.append(seance)
        self.OrdonnerSeances()
        seance.ConstruireArbre(self.arbre, self.brancheSce)
        self.GetApp().sendEvent(modif = u"Ajout d'une Séance")
        
        self.arbre.SelectItem(seance.branche)
        
        return seance
    
    
    
    ######################################################################################  
    def SupprimerSeance(self, event = None, item = None):
#        print "SupprimerSeance depuis :", self.code
#        print "   ", self.seances
        if len(self.seances) > 1: # On en laisse toujours une !!
            seance = self.arbre.GetItemPyData(item)
#            print " ---",  seance
            self.seances.remove(seance)
            self.arbre.Delete(item)
            self.OrdonnerSeances()
            self.GetApp().sendEvent(modif = u"Suppression d'une Séance")
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
        self.GetApp().sendEvent(modif = u"Suppression d'une Séquence prérequise")
        
    ######################################################################################  
    def AjouterSequencePre(self, event = None):
        ps = LienSequence(self)
        self.prerequisSeance.append(ps)
        ps.ConstruireArbre(self.arbre, self.branchePre)
        self.GetApp().sendEvent(modif = u"Ajout d'une Séquence prérequise")
        self.arbre.SelectItem(ps.branche)
        
        
    ######################################################################################  
    def AjouterSysteme(self, event = None):
        sy = Systeme(self)
        self.systemes.append(sy)
        sy.ConstruireArbre(self.arbre, self.brancheSys)
        self.arbre.Expand(self.brancheSys)
        self.GetApp().sendEvent(modif = u"Ajout d'un Système")
        self.arbre.SelectItem(sy.branche)
        self.AjouterSystemeSeance()
        return
    
    ######################################################################################  
    def AjouterListeSystemes(self, syst = []):
#         print "AjouterListeSystemes séquence"
        nouvListe = []
        for s in syst:
#             print "   ",s
            
            if not isinstance(s, Systeme):
#                 print 1
                sy = Systeme(self)
                sy.setBranche(ET.fromstring(s))
            else:
#                 print 2
                sy = s.Copie(self)
                sy.lienClasse = s
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
        
        self.arbre.Expand(self.brancheSys)
        self.AjouterListeSystemesSeance(nouvListe)
        self.GetApp().sendEvent(modif = u"Ajout d'une liste de Systèmes")
        return


    ######################################################################################  
    def SupprimerSysteme(self, event = None, item = None):
        sy = self.arbre.GetItemPyData(item)
        i = self.systemes.index(sy)
        self.systemes.remove(sy)
        self.arbre.Delete(item)
        self.SupprimerSystemeSeance(i)
        self.GetApp().sendEvent(modif = u"Suppression d'un Système")


    ######################################################################################  
    def SelectSystemes(self, event = None):
        if recup_excel.ouvrirFichierExcel():
            res = messageYesNo(self.app, u"Sélection de systèmes depuis Excel\n\n" \
                                         u"Excel doit à présent être lancé.\n" \
                                         u"\t- selectionner les cellules contenant les informations,\n" \
                                         u"\t- puis appuyer sur Ok.\n\n" \
                                         u"Format attendu de la selection :\n" \
                                         u"|    colonne 1    |    colonne 2      |    colonne 3    |\n" \
                                         u"|                         | (optionnelle)    | (optionnelle) |\n" \
                                         u"|    systèmes     |   nombre dispo | fichiers image|\n" \
                                         u"|   ...                   |   ...                      |   ...                    |\n",
                                         u'Sélection de systèmes',
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
            messageErreur(self.GetApp(), u"Permission refusée",
                          u"Permission d'enregistrer les préférences refusée.\n\n" \
                          u"Le dossier est protégé en écriture")
        except:
            messageErreur(self.GetApp(), u"Enregistrement impossible",
                          u"Imposible d'enregistrer les préférences\n\n")
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
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, Titres[0], data = self, image = self.arbre.images["Seq"])
        self.arbre.SetItemBold(self.branche)
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)
        
        #
        # LE centre d'intérêt
        #
        self.CI.ConstruireArbre(arbre, self.branche)
        
        #
        # Les prérequis
        #
        self.branchePre = arbre.AppendItem(self.branche, Titres[1], 
                                           data = self.prerequis, 
                                           image = self.arbre.images["Sav"])
        self.prerequis.branche = self.branchePre
        for ps in self.prerequisSeance:
            ps.ConstruireArbre(arbre, self.branchePre)
        
        #
        # L'équipe pédagogique
        #
        self.branchePrf = arbre.AppendItem(self.branche, Titres[10], 
                                           data = "Equ")
        for e in self.equipe:
            e.ConstruireArbre(arbre, self.branchePrf) 
        
        #
        # Les objectifs
        #
        self.brancheObj = arbre.AppendItem(self.branche, Titres[2], image = self.arbre.images["Obj"], 
                                           data = "Obj")
        for obj in self.obj.values():
            obj.ConstruireArbre(arbre, self.brancheObj)
            
        if not simple: ## !!!
            self.brancheSce = arbre.AppendItem(self.branche, Titres[3], image = self.arbre.images["Sea"], data = "Sea")
            self.arbre.SetItemBold(self.brancheSce)
            for sce in self.seances:
                sce.ConstruireArbre(arbre, self.brancheSce) 
                
            self.brancheSys = arbre.AppendItem(self.branche, Titres[4], image = self.arbre.images["Sys"], data = "Sys")
            
            for sy in self.systemes:
                sy.ConstruireArbre(arbre, self.brancheSys)    
        

    ######################################################################################  
    def DefinirCouleurs(self):
        draw_cairo.DefinirCouleurs(self.GetNbrPeriodes(),
                                   len(self.GetReferentiel()._listesCompetences_simple["S"]),
                                   len(self.GetReferentiel().CentresInterets))


    ######################################################################################  
    def Rafraichir(self):
        self.arbre.Delete(self.branche)
        self.ConstruireArbre(self.arbre, self.arbre.GetRootItem())
        self.arbre.ExpandAll()
        
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
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([[u"Enregistrer", self.app.commandeEnregistrer, 
                                              getIconeFileSave()],
#                                             [u"Ouvrir", self.app.commandeOuvrir],
                                             [u"Exporter la fiche (PDF ou SVG)", self.app.exporterFiche, None],
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
            
            
        elif self.arbre.GetItemText(itemArbre) == Titres[3]: # Séances
            listItems = [[u"Ajouter une séance", 
                          self.AjouterSeance,
                          images.Icone_ajout_seance.GetBitmap()]]
            
            ################
            elementCopie = GetObjectFromClipBoard('Seance')
            if elementCopie is not None:
                listItems.append([u"Coller", functools.partial(self.CollerElem, 
                                                       bseance = elementCopie),
                                                       getIconePaste()])
            
            self.app.AfficherMenuContextuel(listItems)
                
                
        elif self.arbre.GetItemText(itemArbre) == Titres[4]: # Système
            self.app.AfficherMenuContextuel([[u"Ajouter un système", 
                                              self.AjouterSysteme,
                                              images.Icone_ajout_systeme.GetBitmap()], 
                                             [u"Selectionner depuis un fichier", 
                                              self.SelectSystemes, 
                                              None],
#                                             [u"Sauvegarder la liste dans les préférences", self.SauvSystemes]
                                             ])
         
        elif self.arbre.GetItemText(itemArbre) == Titres[1]: # Prérequis
            self.app.AfficherMenuContextuel([[u"Ajouter une séquence", self.AjouterSequencePre, 
                                              images.Icone_ajout_seq.GetBitmap()], 
                                             ])
        
        elif self.arbre.GetItemText(itemArbre) == Titres[10]: # Eleve
            self.app.AfficherMenuContextuel([[u"Ajouter un professeur", self.AjouterProf, images.Icone_ajout_prof.GetBitmap()]])



    ######################################################################################       
    def GetCompetencesVisees(self):
        """ Renvoie la liste des compétences visées (objectifs) 
        """
        return self.obj["C"].competences



    ######################################################################################       
    def GetSystemesUtilises(self):
        """ Renvoie la liste des systèmes utilisés pendant la séquence
        """
        lst = []
        for s in self.systemes:
            n = 0
            for se in self.seances:
                ns = se.GetNbrSystemes(complet = True)
                if s.nom in ns.keys():
                    n += ns[s.nom]
            if n > 0:
                lst.append(s)
        return lst



    ######################################################################################  
    def GetNbreSeances(self):
        n = 0
        for s in self.seances:
            if s.typeSeance in ["R", "S"]:
                n += len(s.seances)
            n += 1
        return n



    ######################################################################################  
    def GetToutesSeances(self):
        l = []
        for s in self.seances:
            l.append(s)
            if s.typeSeance in ["R", "S"]:
                l.extend(s.GetToutesSeances())
            
        return l 



    ######################################################################################  
    def GetNbrSystemes(self):
        """
        """
        dic = {}
        for s in self.GetToutesSeances():
            d = s.GetNbrSystemes()
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
    def getBitmapPeriode(self, larg):
        imagesurface = draw_cairo_seq.getBitmapPeriode(larg, self.position,
                                                       self.GetReferentiel().periodes, 
                                                       prop = 7)
        return getBitmapFromImageSurface(imagesurface)


    #############################################################################
    def MiseAJourTypeEnseignement(self):
#        print "MiseAJourTypeEnseignement Sequence", self.GetNbrPeriodes()
        self.app.SetTitre()
        self.classe.MiseAJourTypeEnseignement()
        self.CI.MiseAJourTypeEnseignement()
        self.obj['C'].MiseAJourTypeEnseignement()
        for o in self.obj.values():
            o.MiseAJourTypeEnseignement()
        self.prerequis.MiseAJourTypeEnseignement()
        for s in self.seances:
            s.MiseAJourTypeEnseignement()
        
        draw_cairo.DefinirCouleurs(self.GetNbrPeriodes(),
                                   len(self.GetReferentiel()._listesCompetences_simple["S"]),
                                   len(self.GetReferentiel().CentresInterets))



    #############################################################################
    def Verrouiller(self):
        if hasattr(self, 'CI') \
            and (self.CI.numCI != [] or self.prerequis.savoirs != [] \
                 or self.obj['C'].competences != [] or self.obj['S'].savoirs != []):
            self.classe.Verrouiller(True)
        else:
            if self.classe != None:
                self.classe.Verrouiller(False)


    #############################################################################
    def enregistrer(self, nomFichier):
                # La séquence
        sequence = self.getBranche()
        classe = self.classe.getBranche()
        
        # La racine
        root = ET.Element("Sequence_Classe")
        root.append(sequence)
        root.append(classe)
        constantes.indent(root)
        
        enregistrer_root(root, nomFichier)


####################################################################################################
#
#        Projet
#
####################################################################################################
class Projet(BaseDoc, Objet_sequence):
    def __init__(self, app, classe = None, intitule = u"", ouverture = False):
        BaseDoc.__init__(self, app, classe, intitule)
        Objet_sequence.__init__(self)
        
        self.nom_obj = u"Projet"
        self.article_c_obj = u"du"
        self.article_obj = u"le"
        
        self.version = "" # version de pySéquence avec laquelle le fichier a été sauvegardé
        
        # code désignant le type de projet
#        print "init Projet"
#        print "   ", self.GetReferentiel()
        self.code = self.GetReferentiel().getCodeProjetDefaut()
  
        self.position = self.GetProjetRef().getPeriodeDefaut()
#        print "position0", self.position
        self.nbrParties = 1
        
        # Organisation des revues du projet
        self.initRevues()

        # Année Scolaire
        self.annee = constantes.getAnneeScolaire()
                
        self.eleves = []
        
        self.taches = self.creerTachesRevue()
            
        self.equipe = []
        
        self.support = Support(self)
        
        self.problematique = u""
        
        #
        # Spécifiquement pour la fiche de validation
        #
        self.origine = u""
        self.contraintes = u""
        self.besoinParties = u""
        self.intituleParties = u""

        self.production = u""
        
        self.synoptique = u""
        self.typologie = []
        
        # Prtie "Partenariat ('PAR')
        self.partenariat = u""
        self.montant = u""
        self.src_finance = u""
        
        if not ouverture:
            self.MiseAJourTypeEnseignement()
#        self.SetPosition(self.position, first = True)
        
        # Le module de dessin
        self.draw = draw_cairo_prj
        
        self.undoStack.do(u"Création du Projet")
        
        
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
#        print "GetProjetRef", self.code
        if self.code == None:
            return self.GetReferentiel().getProjetDefaut()
        else:
            if self.code in self.GetReferentiel().projets.keys():
                return self.GetReferentiel().projets[self.code]
            else:
                return None

        
    ######################################################################################  
    def GetDuree(self):
        duree = 0
        for t in self.taches:
            duree += t.GetDuree()
        return duree
                  
    ######################################################################################  
    def GetDureeGraph(self):
        duree = 0
        for t in self.taches:
            duree += t.GetDureeGraph()
        return duree
    
    ######################################################################################  
    def GetPtCaract(self): 
        """ Renvoie la liste des points caractéristiques des zones actives de la fiche
            (pour l'animation SVG)
        """
        lst = []
        
        for i, pt in enumerate(self.pt_caract_comp):
            lst.append((pt, self, i))
            
        for i, pt in enumerate(self.pt_caract_eleve):
            lst.append((pt, self, -1-i))    
            
        lst.extend(self.support.GetPtCaract())
        
        for s in self.taches + self.eleves:
            lst.extend(s.GetPtCaract())
            
        self.cadre = []
        return lst    
    
    
    ######################################################################################  
    def creerTachesRevue(self):
        lst = []
        if self.nbrRevues == 2:
            lr = [_R1, _R2, "S"]
        else:
            lr = TOUTES_REVUES_EVAL_SOUT
        for p in lr:
            lst.append(Tache(self, intitule = self.GetProjetRef().phases[p][1], 
                             phaseTache = p, duree = 0))
        return lst
    
    
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
    def EnrichiSVGdoc(self, doc):
        """ Enrichissement de l'image SVG <doc> (format XML) avec :
             - mise en surbrillance des éléments actifs
             - infobulles sur les éléments actifs
             - liens 
             - ...
        """
        for s in self.taches:
            s.EnrichiSVG(doc)
        self.support.EnrichiSVG(doc)
        self.EnrichiSVG(doc)
        return
            
    
    ######################################################################################  
    def GetBulleSVG(self, i):
        if i >= 0:
            c = self.GetCompetencesUtil()
            prj = self.GetProjetRef()
            lstIndic = prj._dicIndicateurs_simple[c[i]]
#            lstIndic = REFERENTIELS[self.classe.typeEnseignement]._dicIndicateurs_prj_simple[c[i]]
            t = c[i] + " :\n" + u"\n".join([indic.intitule for indic in lstIndic])
            return t.encode(SYSTEM_ENCODING)
        else:
            e = self.eleves[-1-i]
            t = e.GetNomPrenom()+"\n"
            t += u"Durée d'activité : "+draw_cairo.getHoraireTxt(e.GetDuree())+"\n"
            t += u"Evaluabilité :\n"
            ev_tot = e.GetEvaluabilite()[1]
#             print ev_tot
            for disc, dic in self.GetProjetRef()._dicoGrpIndicateur.items():
                for ph, nomph in self.GetProjetRef().parties.items():
#                     print "  ", ph
                    t += nomph + pourCent2(ev_tot[disc][ph][0], True)+"\n"
            
#            t += u"\tconduite : "+pourCent2(ev_tot['R'][0], True)+"\n"
#            t += u"\tsoutenance : "+pourCent2(ev_tot['S'][0], True)+"\n"
            return t.encode(SYSTEM_ENCODING)
            
            
            
    ######################################################################################  
    def GetCode(self, i = None):
        return u"Projet"
    

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
        
        projet.set("Problematique", remplaceLF2Code(self.problematique))
#        print "   ", self.problematique
#
        if self.commentaires != u"":
            projet.set("Commentaires", self.commentaires)

        projet.set("Position", str(self.position))
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
#        
        eleves = ET.SubElement(projet, "Eleves")
        for e in self.eleves:
            eleves.append(e.getBranche())
            
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
        
        self.intitule = branche.get("Intitule", u"")
        
        self.version = branche.get("Version", "")       # A partir de la version 5.7 !

#        print "   ", self.problematique
        self.problematique = remplaceCode2LF(branche.get("Problematique", u""))
        
        self.commentaires = branche.get("Commentaires", u"")
        
        ref = self.GetProjetRef()
        self.position = eval(branche.get("Position", "0"))
        if self.version == "": # Enregistré avec une version de pySequence > 5.7
            if self.position == 5:
                print "Correction position"
                self.position = ref.getPeriodeEval()
#        print "position", self.position
        self.code = self.GetReferentiel().getProjetEval(self.position+1)
        
        self.nbrRevues = eval(branche.get("NbrRevues", str(ref.getNbrRevuesDefaut())))
        if not self.nbrRevues in ref.posRevues.keys():
            self.nbrRevues = ref.getNbrRevuesDefaut()
        self.positionRevues = branche.get("PosRevues", 
                                          '-'.join(list(ref.posRevues[self.nbrRevues]))).split('-')

        if self.nbrRevues == 3: # Car par défaut c'est 2
            self.MiseAJourNbrRevues()
        
            
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
        
        brancheEle = branche.find("Eleves")
        self.eleves = []
        for e in list(brancheEle):
            eleve = Eleve(self)
            Ok = eleve.setBranche(e)
            if not Ok : 
                err.append(constantes.Erreur(constantes.ERR_PRJ_ELEVES))
            
            self.eleves.append(eleve)
        
        #
        # pour la fiche de validation
        #
        self.origine = remplaceCode2LF(branche.get("Origine", u""))
        self.contraintes = remplaceCode2LF(branche.get("Contraintes", u""))
        self.production = remplaceCode2LF(branche.get("Production", u""))
        self.besoinParties = remplaceCode2LF(branche.get("BesoinParties", u""))
        self.intituleParties = remplaceCode2LF(branche.get("IntitParties", u""))
        self.nbrParties = eval(branche.get("NbrParties", "1"))
      
        self.synoptique = remplaceCode2LF(branche.get("Synoptique", u""))
        
        self.typologie = []
        typologie = branche.find("Typologie")
        if typologie != None:
            i = 0
            continuer = True
            while continuer:
                t = typologie.get("T_"+str(i), u"")
                if t == u"":
                    continuer = False
                else:
                    self.typologie.append(eval(t))
                    i += 1
            
        self.partenariat = remplaceCode2LF(branche.get("Partenaires", u""))
        self.montant = remplaceCode2LF(branche.get("Montant", u""))
        self.src_finance = remplaceCode2LF(branche.get("SrcFinance", u""))
        
        
      
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
                
                e = tachesRevue[num].setBranche(e)
                err.extend(e)
                if len(e) > 0:
                    err.append(constantes.Erreur(constantes.ERR_PRJ_TACHES, phase))
            
                self.taches.append(tachesRevue[num])
                adapterVersion = False
            else:
                tache = Tache(self, branche = e)
                if tache.code < 0 : # ça s'est mal passé lors du setbranche ...
                    err.append(constantes.Erreur(constantes.ERR_PRJ_TACHES, tache.code))
                    return err
                    
#                tache.setBranche(e)
                self.taches.append(tache)
#        self.CorrigerIndicateursEleve()
        
        # Pour récupérer les prj créés avec la version beta1
        if adapterVersion:
            self.taches.extend(tachesRevue)
        
        self.SetCompetencesRevuesSoutenance()

        if hasattr(self, 'panelPropriete'):
#            if ancienneFam != self.classe.familleEnseignement:
            self.initRevues()
            
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
        kproj = self.GetReferentiel().getProjetEval(pos+1)
#        print "  >", kproj
#        print "  posEpreuve", posEpreuve
    

        ###################################################################
        # on efface toutes les revues
        def effacerRevues():
            lst = []
            for t in self.taches:
                if t.phase in TOUTES_REVUES_EVAL_SOUT:
                    lst.append(t.branche)
            for a in reversed(lst):
                self.SupprimerTache(item = a, verrouiller = False, doUndo = False)
        
        
        
        # On change de projet
        if self.code != kproj:
            self.code = kproj
            effacerRevues()
            
            # On passe à une position "épreuve"
            if self.code != None:
                for tr in self.creerTachesRevue():
                    self.taches.append(tr)
                    tr.ConstruireArbre(self.arbre, self.brancheTac)
                    tr.SetCode()
#                    if hasattr(tr, 'panelPropriete'):
#                        tr.panelPropriete.MiseAJour()
                self.OrdonnerTaches()
                self.arbre.Ordonner(self.brancheTac)
                self.GetApp().sendEvent(modif = u"Changement de projet")
    

                
            
            
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
        
        if param is None:   # le Projet lui-même
            self.tip.SetHTML(constantes.BASE_FICHE_HTML_PROJET)
            self.tip.SetWholeText("int", self.intitule)
        
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
                    self.tip.SetHTML(constantes.BASE_FICHE_HTML_COMP_PRJ)
                    
                    k = param[1:].split(u"\n")
                    nc = getSingulierPluriel(self.GetReferentiel().dicoCompetences["S"].nomGenerique, 
                                             len(competence[1]) > 1)
                    if len(k) > 1:
                        titre = nc + u" - ".join(k)
                    else:
                        titre = nc + " " + k[0]
                    self.tip.SetWholeText("titre", titre)
                    
                    intituleComp = "\n".join([textwrap.fill(ind, 50) for ind in competence[0].split(u"\n")]) 
                    self.tip.SetWholeText( "int", intituleComp)
                    
                    if type(competence[1]) == dict:  
                        indicEleve = obj.GetDicIndicateurs()
                    else:
                        indicEleve = obj.GetDicIndicateurs()[param]
                    self.tip.Construire(competence[1], indicEleve, prj)
                
        self.tip.SetPage()
        return self.tip
        
        
        
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
        for e in self.eleves:
            e.SetCode()
            e.MiseAJourCodeBranche()
    
    
    
            
    ######################################################################################  
    def MiseAJourNbrRevues(self):
        """ Opère les changements lorsque le nombre de revues a changé...
        """
#        print "MiseAJourNbrRevues", self.nbrRevues
        lstPhasesTaches = [k.phase for k in self.taches if k.phase in TOUTES_REVUES_EVAL]
#        print "   ", lstPhasesTaches
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

        self.GetApp().sendEvent(modif = u"Ajout d'une Tâche")

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
        self.GetApp().sendEvent(modif = u"Collé d'un élément")
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
        self.GetApp().sendEvent(modif = u"Insertion d'une revue")
        self.arbre.SelectItem(tache.branche)
            
        self.Verrouiller()


    ######################################################################################  
    def SupprimerTache(self, event = None, item = None, verrouiller = True, doUndo = True):
        tache = self.arbre.GetItemPyData(item)
        self.taches.remove(tache)
        self.arbre.Delete(item)
        self.SetOrdresTaches()
        if doUndo:
            modif = u"Suppression d'une Tâche"
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
        data = self.arbre.GetItemPyData(item)
        if isinstance(data, Tache) and data.phase not in TOUTES_REVUES_EVAL_SOUT:
            self.SupprimerTache(item = item)
            
        elif isinstance(data, Eleve):
            self.SupprimerEleve(item = item)
        
        elif isinstance(data, Prof):
            self.SupprimerProf(item = item)
            
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
        
    ######################################################################################  
    def AjouterEleveDansPanelTache(self):
        for t in self.taches:
            t.AjouterEleve()
            
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
            self.OrdonnerEleves()
            e.ConstruireArbre(self.arbre, self.brancheElv)
            self.arbre.Expand(self.brancheElv)
            self.GetApp().sendEvent(modif = u"Ajout d'un Elève")
            self.arbre.SelectItem(e.branche)
            self.AjouterEleveDansPanelTache()
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

        self.GetApp().sendEvent(modif = u"Suppression d'un Elève")
    
    ######################################################################################  
    def OrdonnerEleves(self):
        for i,e in enumerate(self.eleves):
            e.id = i
            
        
    ######################################################################################  
    def GetNewIdEleve(self):
        """ Renvoie le 1er numéro d'identification élève disponible
        """
#        print "GetNewIdEleve", 
        for i in range(6):
            ok = False
            for e in self.eleves:
                ok = ok or i != e.id
            if ok:
                break
        return i
    

    
        
    
    ######################################################################################  
    def MiseAJourPoidsCompetences(self, code = None):
        for t in self.taches:
            t.MiseAJourPoidsCompetences(code)
        self.MiseAJourDureeEleves()
    
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, Titres[9], data = self, image = self.arbre.images["Prj"])
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
        self.brancheElv = arbre.AppendItem(self.branche, Titres[6], data = "Ele")
        for e in self.eleves:
            e.ConstruireArbre(arbre, self.brancheElv) 
            
        #
        # Les tâches
        #
        self.brancheTac = arbre.AppendItem(self.branche, Titres[8], data = "Tac")
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
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([[u"Enregistrer", self.app.commandeEnregistrer,
                                              getIconeFileSave()],
#                                             [u"Ouvrir", self.app.commandeOuvrir],
                                             [u"Exporter la fiche (PDF ou SVG)", self.app.exporterFiche, None],
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
            
        elif self.arbre.GetItemText(itemArbre) == Titres[6]: # Eleve
            self.app.AfficherMenuContextuel([[u"Ajouter un élève", self.AjouterEleve, images.Icone_ajout_eleve.GetBitmap()]])
            
        elif self.arbre.GetItemText(itemArbre) == Titres[8]: # Tache
            listItems = [[u"Ajouter une tâche", self.AjouterTache, images.Icone_ajout_tache.GetBitmap()]]
            elementCopie = GetObjectFromClipBoard('Tache')
            if elementCopie is not None:
                phase = elementCopie.get("Phase", "")
                if phase == self.GetListePhases()[0]: # C'est bien une tâche de la première phase
#                 if self.phase == phase or self.GetPhaseSuivante() == phase : # la phase est la même
                    listItems.append([u"Coller après", functools.partial(self.CollerElem, 
                                                                         item = itemArbre, 
                                                                         btache = elementCopie),
                                      getIconePaste()])
            self.app.AfficherMenuContextuel(listItems)
            
        elif self.arbre.GetItemText(itemArbre) == Titres[10]: # Eleve
            self.app.AfficherMenuContextuel([[u"Ajouter un professeur", self.AjouterProf, images.Icone_ajout_prof.GetBitmap()]])
                                             
         
            
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
    def GetCompetencesVisees(self):
        """ Renvoie la liste des compétences visées (objectifs) 
        """
        return self.GetCompetencesUtil()
    
    ######################################################################################  
    def GetNbrPhases(self):
        """ Renvoie le nombre de phases dans le projet, y compris les revues
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
                    n = u"     "+n
                lst.append(n)
            elif p in prj.listPhasesEval:
                n = prj.phases[p][0]
                if not p in TOUTES_REVUES_EVAL_SOUT:
                    n = u"     "+n
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
#        print "GetListePhases",
#        lst = list(constantes.PHASE_TACHE[self.GetTypeEnseignement(simple = True)][:-1])
        lst = [k for k in self.GetProjetRef().listPhases if not k in self.GetProjetRef().listPhasesEval]
#        lst = list(self.GetReferentiel().listPhases_prj)
#        print "  ", self.classe.GetReferentiel()
#        print "  ", lst
#        print "  ", self.nbrRevues
        lr = range(1, self.nbrRevues+1)
        lr.reverse()

        for r in lr:
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
        draw_cairo.DefinirCouleurs(self.GetNbrPeriodes(),
                                   len(self.GetReferentiel()._listesCompetences_simple["S"]),
                                   len(self.eleves))
        
     
    ######################################################################################  
    def Rafraichir(self):
        self.DefinirCouleurs()
        
        
    #############################################################################            
    def getBitmapPeriode(self, larg):
        imagesurface = draw_cairo_prj.getBitmapPeriode(larg, self.position,
                                                       self.GetReferentiel().periodes, 
                                                       prop = 7)
        return getBitmapFromImageSurface(imagesurface)
    
    
    #############################################################################
    def MiseAJour(self):
        self.app.SetTitre()
        draw_cairo.DefinirCouleurs(self.GetNbrPeriodes(),
                                   len(self.GetReferentiel()._listesCompetences_simple["S"]),
                                   len(self.eleves))
        self.SetCompetencesRevuesSoutenance()
        
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):#, changeFamille = False):
#        print "MiseAJourTypeEnseignement projet"

        self.code = self.GetReferentiel().getCodeProjetDefaut()

        self.position = self.GetProjetRef().getPeriodeDefaut()
#        print "position", self.position
        
        
        for e in self.eleves:
            e.MiseAJourTypeEnseignement()
        
        self.MiseAJour()

                
    #############################################################################
    def initRevues(self):
#        print "initRevues",self.code
        self.nbrRevues = self.GetReferentiel().getNbrRevuesDefaut(self.code)
        self.positionRevues = list(self.GetReferentiel().getPosRevuesDefaut(self.code))
#        print self.nbrRevues, self.positionRevues
        

    #############################################################################
    def Verrouiller(self):
        self.classe.Verrouiller(len(self.GetCompetencesUtil()) != 0 or len(self.taches) != self.nbrRevues+1)
#        self.GetPanelPropriete().Verrouiller(self.pasVerouille)

    
    ######################################################################################  
    def TesterExistanceGrilles(self, nomFichiers):
#        print "TesterExistanceGrilles", nomFichiers

        existe = []
        for fe in nomFichiers.values():
            for f in fe.values():
                if os.path.isfile(f):
                    existe.append(f)
        
        if len(existe) > 0:
            if len(existe) == 1:
                m = u"La grille d'évaluation existe déja !\n\n" \
                    u"\t%s\n\n" \
                    u"Voulez-vous la remplacer ?" %existe[0]
            else:
                m = u"Les grilles d'évaluation existent déja !\n\n" \
                    u"\t%s\n\n" \
                    u"Voulez-vous les remplacer ?" %u"\n".join(existe)
            
            
                                            
            return messageYesNo(self.GetApp(),
                                      u"Fichier existant", 
                                      m, wx.ICON_WARNING)
            
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
        for k, g in prj.parties.items():
            if not os.path.isfile(grilles.getFullNameGrille(prj.grilles[k][0])):
                prjdef = REFERENTIELS[self.GetTypeEnseignement()].getProjetDefaut()
                if os.path.isfile(grilles.getFullNameGrille(prjdef.grilles[k][0])):
                    prj.grilles[k] = prjdef.grilles[k]
                    prj.cellulesInfo[k] = prjdef.cellulesInfo[k]
                else:
                    print k, grilles.getFullNameGrille(prjdef.grilles[k][0])
                    pb.append(k)
        
        if len(pb) > 0:
            messageErreur(self.GetApp(), u"Fichier non trouvé !",
                                  u"Le(s) fichier(s) grille :\n    " + ";".join(pb) + u"\n" \
                                  u"n'a(ont) pas été trouvé(s) ! \n")
    
    
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
    def enregistrer(self, nomFichier):
        # Le projet
        projet = self.getBranche()
        classe = self.classe.getBranche()
        
        # La racine
        root = ET.Element("Projet_Classe")
        root.append(projet)
        root.append(classe)
        constantes.indent(root)
        
        enregistrer_root(root, nomFichier)
#                        





####################################################################################################
#
#        Projet
#
####################################################################################################
class Progression(BaseDoc, Objet_sequence):
    def __init__(self, app, classe = None, intitule = u"", ouverture = False):
        BaseDoc.__init__(self, app, classe, intitule)
        Objet_sequence.__init__(self)
        
        self.nom_obj = u"Progression"
        self.article_c_obj = u"de la"
        self.article_obj = u"la"

        self.image = None
        
        self.sequences_projets = []     # liste de LienSequence et de LienProjet
        
#         self.calendriers = []
        self.calendrier = Calendrier(self, constantes.getAnneeScolaire())
        self.eleves = []
        self.equipe = []
        self.themes = []
        self.code = self.GetReferentiel().getCodeProjetDefaut()
        
        self.version = ""
        
        if not ouverture:
            self.MiseAJourTypeEnseignement()
            
        # Le module de dessin
        self.draw = draw_cairo_prg

        self.undoStack.do(u"Création de la progression")


    ######################################################################################  
    def __repr__(self):
        return "Projet "+ self.intitule


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
        l = []
        for doc in [s.GetDoc() for s in self.sequences_projets]:
            l.append(doc.position)
        return list(set(l))



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
                                   len(self.GetReferentiel().CentresInterets))
        

    ######################################################################################  
    def Rafraichir(self, event = None):
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
        
        if self.image != None:
            progression.set("Image", img2str(self.image.ConvertToImage()))

        if self.commentaires != u"":
            progression.set("Commentaires", self.commentaires)
        
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
        
        self.intitule = branche.get("Intitule", u"")
        
        self.commentaires = branche.get("Commentaires", u"")
        
        data = branche.get("Image", "")
        if data != "":
            try:
                self.image = PyEmbeddedImage(data).GetBitmap()
            except:
                Ok = False
                self.image = None
                
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
                else:
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
            self.app.AfficherMenuContextuel([[u"Enregistrer", self.app.commandeEnregistrer,
                                              getIconeFileSave()],
#                                             [u"Ouvrir", self.app.commandeOuvrir],
                                             [u"Exporter la fiche (PDF ou SVG)", self.app.exporterFiche, None],
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
            self.app.AfficherMenuContextuel([[u"Ajouter un professeur", self.AjouterProf, images.Icone_ajout_prof.GetBitmap()]])
            
        elif self.arbre.GetItemText(itemArbre) == Titres[11]: # Séquence
            self.app.AfficherMenuContextuel([[u"Créer une nouvelle Séquence", 
                                              self.AjouterNouvelleSequence, 
                                              images.Icone_ajout_seq.GetBitmap()],
                                             [u"Importer une Séquence existante", 
                                              self.AjouterSequence, 
                                              images.Icone_import_seq.GetBitmap()],
                                             [u"Importer toutes les Séquences compatibles du dossier", 
                                              self.ImporterSequences, 
                                              images.Icone_cherch_seq.GetBitmap()],
                                             
                                             [u"Créer un nouveau Projet", 
                                              self.AjouterNouveauProjet, 
                                              images.Icone_ajout_prj.GetBitmap()],
                                             [u"Importer un Projet existant", 
                                              self.AjouterProjet, 
                                              images.Icone_import_prj.GetBitmap()],
                                             [u"Importer tous les Projets compatibles du dossier", 
                                              self.ImporterProjets, 
                                              images.Icone_cherch_prj.GetBitmap()]])


    ######################################################################################  
    def SupprimerItem(self, item):
        self.SupprimerLien(item = item)
    
    ######################################################################################  
    def SupprimerLien(self, event = None, item = None, lien = None):
        if lien is None:
            l = self.arbre.GetItemPyData(item)
        else:
            l = lien

        self.sequences_projets.remove(l)
        
        if item is not None:
            self.arbre.Delete(item)

        if isinstance(item, LienSequence):
            self.GetApp().sendEvent(modif = u"Suppression d'une Séquence")
        else:
            self.GetApp().sendEvent(modif = u"Suppression d'un Projet")
        

    ######################################################################################  
    def OuvrirSequence(self, event = None, item = None):
        l = self.arbre.GetItemPyData(item)
#        self.GetApp().parent.ouvrir(toSystemEncoding(l.path))
        app = self.GetApp().parent.ouvrirDoc(l.sequence, l.path)
#        l.sequence.app = app
    
    ######################################################################################  
    def OuvrirProjet(self, event = None, item = None):
        l = self.arbre.GetItemPyData(item)
#        self.GetApp().parent.ouvrir(toSystemEncoding(l.path))
        app = self.GetApp().parent.ouvrirDoc(l.projet, l.path)
#        l.sequence.app = app

    ######################################################################################  
    def ChargerSequences(self):
#        print "ChargerSequences", self.sequences_projets
        aSupprimer = []
        for lienSeq in [s for s in self.sequences_projets if isinstance(s, LienSequence)]:
            if lienSeq.sequence is None:
#                print "   ", lienSeq.path
                path = os.path.join(self.GetPath(), lienSeq.path)
#                print "   ", path
                if not os.path.isfile(path):
                    dlg = wx.MessageDialog(self.GetApp(), u"Le fichier Séquence suivant n'a pas été trouvé.\n\n"\
                                                 u"\t%s\n\n"
                                                 u"Voulez-vous le chercher manuellement ?\n" %toSystemEncoding(lienSeq.path),
                                           u"Fichier non trouvé",
                                           wx.YES_NO | wx.ICON_QUESTION |wx.YES_DEFAULT
                                           )
                    res = dlg.ShowModal()
                    dlg.Destroy()
                    if res == wx.ID_YES:
                        fichiers_sequences = self.GetFichiersSequencesDossier(exclureExistant = True)
                        fichiers, sequences = zip(*fichiers_sequences)
                        fichiers = [os.path.relpath(f, self.GetPath()) for f in fichiers]
                        
                        dlg = wx.SingleChoiceDialog(self.GetApp(), u"Choisir parmi les fichiers ci-dessous\n"\
                                                                   u"celui qui doit remplacer %s." %toSystemEncoding(lienSeq.path), 
                                                    u"Fichiers Séquences disponibles",
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
                    
                    elif res == wx.ID_NO:
                        aSupprimer.append(lienSeq)
                        continue
                else: 
                    lienSeq.ChargerSequence()
        
        #
        # On supprime les lienSequences à supprimer
        #
        for s in aSupprimer:
            self.SupprimerLien(lien = s)
            
        

    
    ######################################################################################  
    def ChargerProjets(self):
#        print "ChargerProjets", self.sequences_projets
        aSupprimer = []
        for lienPrj in [s for s in self.sequences_projets if isinstance(s, LienProjet)]:
            if lienPrj.projet is None:
#                print "   ", lienSeq.path
                path = os.path.join(self.GetPath(), lienPrj.path)
#                print "   ", path
                if not os.path.isfile(path):
                    dlg = wx.MessageDialog(self.GetApp(), u"Le fichier Projet suivant n'a pas été trouvé.\n\n"\
                                                 u"\t%s\n\n"
                                                 u"Voulez-vous le chercher manuellement ?\n" %toSystemEncoding(lienPrj.path),
                                           u"Fichier non trouvé",
                                           wx.YES_NO | wx.ICON_QUESTION |wx.YES_DEFAULT
                                           )
                    res = dlg.ShowModal()
                    dlg.Destroy()
                    if res == wx.ID_YES:
                        fichiers_projets = self.GetFichiersProjetsDossier(exclureExistant = True)
                        fichiers, projets = zip(*fichiers_projets)
                        fichiers = [os.path.relpath(f, self.GetPath()) for f in fichiers]
                        
                        dlg = wx.SingleChoiceDialog(self.GetApp(), u"Choisir parmi les fichiers ci-dessous\n"\
                                                                   u"celui qui doit remplacer %s." %toSystemEncoding(lienPrj.path), 
                                                    u"Fichiers Projet disponibles",
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
                    lienPrj.ChargerProjet()
        
        #
        # On supprime les lienProjet à supprimer
        #
        for s in aSupprimer:
            self.SupprimerLien(lien = s)
            
        
        
        
    ######################################################################################  
    def Ordonner(self):
#        print "Ordonner"
    
        listeSeqPrj = self.sequences_projets
                
        listeSeqPrj.sort(key= lambda s : s.GetDoc().position)
        
        self.brancheSeq.DeleteChildren(self.arbre)
        for e in listeSeqPrj:
            e.ConstruireArbre(self.arbre, self.brancheSeq) 
            
        self.VerifPb()

    

    ######################################################################################  
    def DossierDefini(self):
        dossier = self.GetPath()
        if dossier == r"":
            messageInfo(None, u"Progression non enregistrée", 
                                  u"La progression %s n'a pas encore été enregistrée.\n\n"\
                                  u"L'importation est prévue pour rechercher des fichier \"Séquence\" (.seq)" \
                                  u"dans le même dossier que le fichier \"Progression\" (.prg)." %self.intitule)
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
            else:
                ps.ChargerSequence()
            self.sequences_projets.append(ps)
            self.Ordonner()
            self.GetApp().sendEvent(modif = u"Ajout d'une nouvelle Séquence à la Progression")
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
            else:
                ps.ChargerProjet()
            self.sequences_projets.append(ps)
            self.Ordonner()
            self.GetApp().sendEvent(modif = u"Ajout d'un nouveau Projet à la Progression")
            self.arbre.SelectItem(ps.branche)
            
    ######################################################################################  
    def AjouterSequence(self, event = None):
        if not self.DossierDefini():
            return
        
        fichiers_sequences = self.GetFichiersSequencesDossier(exclureExistant = True)
        if len(fichiers_sequences) == 0:
            messageInfo(None, u"Aucune Séquence trouvée", 
                        u"Aucune Séquence compatible à la progression n'a été trouvée.\n\n")
            return
        
        fichiers, sequences = zip(*fichiers_sequences)
        fichiers = [os.path.relpath(f, self.GetPath()) for f in fichiers]
        
        dlg = wx.SingleChoiceDialog(self.GetApp(), u"Choisir parmi les fichiers ci-dessous\n", 
                                    u"Fichiers Séquences disponibles",
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
            self.GetApp().sendEvent(modif = u"Ajout d'une Séquence à la Progression")
            self.arbre.SelectItem(lienSeq.branche)
        
        dlg.Destroy()
        
    ######################################################################################  
    def AjouterProjet(self, event = None):
        if not self.DossierDefini():
            return
        
        fichiers_projets = self.GetFichiersProjetsDossier(exclureExistant = True)
        if len(fichiers_projets) == 0:
            messageInfo(None, u"Aucun Projet trouvé", 
                        u"Aucun Projet compatible à la progression n'a été trouvé.\n\n")
            return
        
        fichiers, projets = zip(*fichiers_projets)
        fichiers = [os.path.relpath(f, self.GetPath()) for f in fichiers]
        
        dlg = wx.SingleChoiceDialog(self.GetApp(), u"Choisir parmi les fichiers ci-dessous\n", 
                                    u"Fichiers Projets disponibles",
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
            self.GetApp().sendEvent(modif = u"Ajout d'un Projet à la Progression")
            self.arbre.SelectItem(lienPrj.branche)
        
        dlg.Destroy()

 
    ######################################################################################  
    def CreerSequence(self, classe, pathProg):
        sequence = Sequence(self.GetApp(), classe)
        res = self.GetApp().ProposerEnregistrer(sequence, pathProg)
        
        if res[0] == 2:
            return self.CreerSequence(classe, pathProg)
        elif res[0] == 1:
            return None, res[1]
        elif res[0] == 0:
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
#        print "sequences", sequences
        for s in sequences:
            if not s in self.sequences_projets:
                self.sequences_projets.append(s)
#                s.ConstruireArbre(self.arbre, self.brancheSeq)
        self.Ordonner()

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


    ######################################################################################  
    def VerifPb(self):
        obj = []
        for lienseq in [s for s in self.sequences_projets if isinstance(s, LienSequence)]:
            pb = []
            seq = lienseq.sequence
            prerequis = seq.prerequis.savoirs
            objectifs = seq.obj['S'].savoirs
            for p in prerequis:
                if not p in obj:
                    pb.append(p)
            lienseq.SignalerPb(pb)
            obj.extend(objectifs)

            
    ########################################################################################################
    def OuvrirFichierSeq(self, nomFichier):
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
        fichier = open(nomFichier,'r')
        classe = Classe(self.GetApp())
        sequence = Sequence(self.GetApp(), classe, ouverture = True)
        classe.SetDocument(sequence)

        try:
            root = ET.parse(fichier).getroot()
            rsequence = root.find("Sequence")
            rclasse = root.find("Classe")
            if rclasse is not None:
                classe.setBranche(rclasse)
            if rsequence is not None:
                sequence.setBranche(rsequence)
            else:   # Ancienne version , forcément STI2D-ETT !!
                classe.typeEnseignement, self.classe.familleEnseignement = ('ET', 'STI')
                classe.referentiel = REFERENTIELS[classe.typeEnseignement]
                sequence.setBranche(root)
            return classe, sequence
        except:
            print u"Le fichier n'a pas pu être ouvert :",nomFichier
            return None, None
        finally:
            fichier.close()

    
    ########################################################################################################
    def OuvrirFichierPrj(self, nomFichier):
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
        
#        print "///", nomFichier
        fichier = open(nomFichier,'r')
        classe = Classe(self.GetApp())
        projet = Projet(self.GetApp(), classe, ouverture = True)
        classe.SetDocument(projet)

        try:
            root = ET.parse(fichier).getroot()
            rprojet = root.find("Projet")
            rclasse = root.find("Classe")
            if rclasse is not None:
                classe.setBranche(rclasse)
            if rprojet is not None:
                projet.setBranche(rprojet)
            else:   # Ancienne version , forcément STI2D-ETT !!
                classe.typeEnseignement, self.classe.familleEnseignement = ('ET', 'STI')
                classe.referentiel = REFERENTIELS[classe.typeEnseignement]
                projet.setBranche(root)
            return classe, projet
        except:
            print u"Le fichier n'a pas pu être ouvert :",nomFichier
            return None, None
        finally:
            fichier.close()


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
    def GetListeFichiersSequences(self):
        """
        """
        return [l.path for l in self.sequences_projets]


    ########################################################################################################
    def GetSequencesDossier(self, event = None):
        sequences = []
        listeFichiersSequences = self.GetFichiersSequencesDossier()
        for fichier, sequence in listeFichiersSequences:
            lienSequence = LienSequence(self,  os.path.relpath(fichier, self.GetPath()))
            lienSequence.sequence = sequence
            sequences.append(lienSequence)
        
        self.GetApp().sendEvent(modif = u"Import de Séquences compatibles") 
        
        return sequences




    ########################################################################################################
    def GetFichiersSequencesDossier(self, event = None, exclureExistant = False):    
        """ Recherche tous les fichiers Séquence compatibles avec la progression
        
        >> Renvoie une liste [(nomFichier, Sequence)]
        """   
#        print "GetSequencesDossier"
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
            
        #
        # Un ProgressDialog pour patienter ...
        #
        dlg =    wx.ProgressDialog(u"Recherche des séquences",
                                   u"",
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
#                lienSequence = LienSequence(self,  os.path.relpath(f, self.GetPath()))
#                lienSequence.sequence = sequence
                fichiers_sequences.append((f, sequence))
            count += 1

        dlg.Update(count, u"Terminé")
        dlg.Destroy()
        wx.EndBusyCursor()
        
        return fichiers_sequences



    ########################################################################################################
    def GetFichiersProjetsDossier(self, event = None, exclureExistant = False):    
        """ Recherche tous les fichiers Projet compatibles avec la progression
        
        >> Renvoie une liste [(nomFichier, Projet)]
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
        dlg =    wx.ProgressDialog(u"Recherche des Projets",
                                   u"",
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

        dlg.Update(count, u"Terminé")
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
            self.tip.SetHTML(constantes.BASE_FICHE_HTML)
            
        
        else:               # Un autre élément de la Progression
            self.tip.SetHTML(self.GetFicheHTML(param = param))
            if param == "CAL":
                self.tip.SetWholeText("titre", u"Calendrier de la Progression")
                self.tip.AjouterImg("img", self.getBitmapCalendrier(1000))
                
            elif param == "ANN":
                self.tip.SetWholeText("titre", u"Années scolaires de la Progression")
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
                self.tip.SetWholeText("titre", getSingulierPluriel(ref.nomCI, False))  
                numCI = int(param[2:])
                code = ref.abrevCI+str(numCI+1)
                intit = ref.CentresInterets[numCI]
                self.tip.AjouterElemListeDL("ci", code, intit)
                if len(ref.listProblematiques) > numCI and len(ref.listProblematiques[numCI]) > 0:
                    self.tip.SetWholeText("nomPb", getSingulierPluriel(ref.nomPb, True) + " envisageables")  
                    for pb in ref.listProblematiques[numCI]:
                        self.tip.AjouterElemListeUL("pb", pb)
                else:
                    self.tip.Supprime('pb')
                              
            elif param[:3] == "CMP":
                ref = self.GetReferentiel()
                competence = ref.getCompetence("S"+param[3:])
                if competence is not None:
                    self.tip.SetHTML(constantes.BASE_FICHE_HTML_COMP_PRJ)
                    k = param[3:]
                    nc = getSingulierPluriel(ref.dicoCompetences["S"].nomGenerique, False)
                    self.tip.SetWholeText("titre", nc + " " + k)
                    
                    intituleComp = competence[0]
                    intituleComp = "\n".join([textwrap.fill(ind, 50) for ind in intituleComp.split(u"\n")]) 
                    self.tip.SetWholeText("int", intituleComp)
            
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
    def enregistrer(self, nomFichier):
        # La progression
        progression = self.getBranche()
        classe = self.classe.getBranche()
        
        # La racine
        root = ET.Element("Progression_Classe")
        root.append(progression)
        root.append(classe)
        constantes.indent(root)
        
        enregistrer_root(root, nomFichier)

        for lienSeq in [s for s in self.sequences_projets if isinstance(s, LienSequence)]:
            if lienSeq.sequence in self.dependants:
                lienSeq.sequence.enregistrer(lienSeq.path)
        
        for lienPrj in [s for s in self.sequences_projets if isinstance(s, LienProjet)]:
            if lienPrj.projet in self.dependants:
                lienPrj.projet.enregistrer(lienPrj.path)

        del self.dependants[:]




#########################################################################################################
#########################################################################################################
class LienSequence(Objet_sequence):
    def __init__(self, parent, path = r""):
        self.path = path
        self.parent = parent
        Objet_sequence.__init__(self)
        
        self.sequence = None
        
        #
        # Création du Tip (PopupInfo)
        #
#         self.tip = PopupInfo(self.GetApp().parent, "")
#        self.ficheHTML = self.GetFicheHTML()
#        self.tip = PopupInfo(self.parent.app, self.ficheHTML)

        
    
    ######################################################################################  
    def __eq__(self, lien):
        return os.path.normpath(self.path) == os.path.normpath(lien.path)
    
    ######################################################################################  
    def comp(self, lienSeq):
        """
        """
        return self.sequence.position > lienSeq.sequence.position
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    ######################################################################################  
    def GetDocument(self):    
        return self.parent
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_LienSequence(parent, self)
    
    ######################################################################################  
    def GetDoc(self):
        return self.sequence
    
    ######################################################################################  
    def GetPosition(self):
        return self.sequence.position
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du lien de sequence pour enregistrement
        """
        root = ET.Element("Sequence")
        root.set("dir", toSystemEncoding(self.path))
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche LienSequence", self
        self.path = toFileEncoding(branche.get("dir", ""))
#        if hasattr(self, 'panelPropriete'):
#            self.panelPropriete.MiseAJour()

    ######################################################################################  
    def MiseAJourArbre(self):
        self.arbre.SetItemText(self.branche, self.sequence.intitule)
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        if self.sequence is None:
            return
#        print "ConstruireArbre"
        self.arbre = arbre
            
        coul = draw_cairo.BcoulPos[self.sequence.position]
        coul = [int(200*c) for c in coul]
        self.codeBranche = CodeBranche(self.arbre)
#        self.codeBranche.SetForegroundColour(coul)
        self.branche = arbre.AppendItem(branche, self.sequence.intitule, #wnd = self.codeBranche, 
                                        data = self,
                                        image = self.arbre.images["Seq"])
        self.codeBranche.SetBranche(self.branche)
        self.arbre.SetItemTextColour(self.branche, coul)

#        self.codeBranche.SetBranche(self.branche)
        
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)

    
    ######################################################################################  
    def ChargerSequence(self):
        classe, sequence = self.GetDocument().OuvrirFichierSeq(self.path)
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
                self.arbre.SetItemBackgroundColour(self.branche, wx.NamedColour("LIGHT PINK"))
                message = u"Les prérequis suivants n'ont pas été abordés dans les séquences précédentes :\n"
                self.SetToolTip(message + u" - ".join(pb))
                
            
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", 
                                                     functools.partial(self.parent.SupprimerLien, item = itemArbre), 
                                                     images.Icone_suppr_seq.GetBitmap()],
                                                    [u"Ouvrir", 
                                                     functools.partial(self.parent.OuvrirSequence, item = itemArbre), 
                                                     wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (20,20))]
                                                    ])


    ######################################################################################  
    def SetLabel(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.sequence.intitule)
        

    ######################################################################################  
    def GetNomFichier(self):
        return os.path.splitext(os.path.basename(self.path))[0]


    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.BASE_FICHE_HTML_SEQ


    ######################################################################################  
    def SetTip(self):
        # Tip
        seq = self.sequence
        self.tip.SetHTML(self.GetFicheHTML())
        self.tip.SetWholeText("nom", seq.intitule)
        self.tip.AjouterImg("ap", seq.GetApercu(600, 265, entete = True)) 
        
        self.tip.SetPage()







#########################################################################################################
#########################################################################################################
class LienProjet(Objet_sequence):
    def __init__(self, parent, path = r""):
        self.path = path
        self.parent = parent
        Objet_sequence.__init__(self)
        
        self.projet = None
        
        #
        # Création du Tip (PopupInfo)
        #
#         self.tip = PopupInfo(self.GetApp().parent, "")
#        self.ficheHTML = self.GetFicheHTML()
#        self.tip = PopupInfo(self.parent.app, self.ficheHTML)

        
    
    ######################################################################################  
    def __eq__(self, lien):
        return os.path.normpath(self.path) == os.path.normpath(lien.path)
    
    ######################################################################################  
    def comp(self, lienSeq):
        """
        """
        return self.projet.position > lienSeq.projet.position
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    ######################################################################################  
    def GetDocument(self):    
        return self.parent
    
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
    def getBranche(self):
        """ Renvoie la branche XML du lien de projet pour enregistrement
        """
        root = ET.Element("Projet")
        root.set("dir", toSystemEncoding(self.path))
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche LienSequence", self
        self.path = toFileEncoding(branche.get("dir", ""))
#        if hasattr(self, 'panelPropriete'):
#            self.panelPropriete.MiseAJour()

    ######################################################################################  
    def MiseAJourArbre(self):
        self.arbre.SetItemText(self.branche, self.projet.intitule)
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        if self.projet is None:
            return
#        print "ConstruireArbre"
        self.arbre = arbre
            
        coul = draw_cairo.BcoulPos[self.projet.position]
        coul = [int(200*c) for c in coul]
        self.codeBranche = CodeBranche(self.arbre)
#        self.codeBranche.SetForegroundColour(coul)
        self.branche = arbre.AppendItem(branche, self.projet.intitule, #wnd = self.codeBranche, 
                                        data = self,
                                        image = self.arbre.images["Prj"])
        self.codeBranche.SetBranche(self.branche)
        self.arbre.SetItemTextColour(self.branche, coul)

#        self.codeBranche.SetBranche(self.branche)
        
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)

    
    ######################################################################################  
    def ChargerProjet(self):
        classe, projet = self.GetDocument().OuvrirFichierPrj(self.path)
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
                self.arbre.SetItemBackgroundColour(self.branche, wx.NamedColour("LIGHT PINK"))
                message = u""
                self.SetToolTip(message + u" - ".join(pb))
                
            
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
#        print "AfficherMenuContextuel"
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", 
                                                     functools.partial(self.parent.SupprimerLien, item = itemArbre), 
                                                     images.Icone_suppr_prj.GetBitmap()],
                                                    [u"Ouvrir", 
                                                     functools.partial(self.parent.OuvrirProjet, item = itemArbre), 
                                                     wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (20,20))]
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
        return constantes.BASE_FICHE_HTML_PRJ


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
class CentreInteret(Objet_sequence):
    def __init__(self, parent, numCI = []):
        self.parent = parent
        Objet_sequence.__init__(self)
        
        self.numCI = []     # Numéros des CI du Référentiel
        self.poids = []
        
        self.CI_perso = []  # Centres d'Intérêt personnalisés
        self.Pb = u""  # Problématique
        
        self.SetNum(self.numCI)
        self.max2CI = True
        
        
    ######################################################################################  
    def __repr__(self):
        return "CI%s" %self.numCI
    
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
 
        # Problématiques personnalisées
        root.set("Pb", self.Pb)
            
            
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
                t = CI_perso.get("CI_"+str(i), u"")
                if t == u"":
                    continuer = False
                else:
                    self.CI_perso.append(t)
                    i += 1

        # Problématique
        self.Pb = branche.get("Pb", "")
    
    
    ######################################################################################  
    def AddNum(self, num, poids = 1): 
        self.numCI.append(num)
        self.poids.append(poids)
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
        lstCI = self.GetListCIref()
        if self.numCI[num] < len(lstCI):
            return lstCI[self.numCI[num]]
            
    
    ######################################################################################  
    def GetNomCIs(self):
        lstCI = self.GetListCIref()
        l = []
        for n in self.numCI:
            l.append(lstCI[n])
        return l + self.CI_perso


    ######################################################################################  
    def GetCode(self, num = None):
        if num == None:
            s = ""
            for i in range(len(self.numCI)):
                s += self.GetCode(i)
                if i < len(self.numCI)-1:
                    s += " - "
            return s
        
        else :
            return self.GetReferentiel().abrevCI+str(self.numCI[num]+1)


    ######################################################################################  
    def GetPosCible(self, num):
        if self.GetReferentiel().CI_cible:
            return self.parent.classe.referentiel.positions_CI[self.numCI[num]]
        
    
    ######################################################################################  
    def MaJArbre(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.GetCode())
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre)
        self.branche = arbre.AppendItem(branche, getSingulierPluriel(self.GetReferentiel().nomCI, True)+u" :", 
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
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, getSingulierPluriel(self.GetReferentiel().nomCI, True)+u" :")
#        self.GetPanelPropriete().construire()

    
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.BASE_FICHE_HTML_CI
    
    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        
        ref = self.GetReferentiel()
        plusieurs = len(self.numCI)+len(self.CI_perso) > 0
        self.tip.SetWholeText("titre", getSingulierPluriel(ref.nomCI, plusieurs))
        
        for i, c in enumerate(self.numCI):
            self.tip.AjouterElemListeDL("ci", self.GetCode(i), self.GetIntit(i))
        
        if len(self.Pb) > 0:
            self.tip.SetWholeText("nomPb", getSingulierPluriel(ref.nomPb, False))  
            self.tip.AjouterElemListeUL("pb", self.Pb)
        else:
            self.tip.SupprimerTag("pb")             
                        
        self.tip.SetPage()
        



####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Competences(Objet_sequence):
    def __init__(self, parent, numComp = None):
        self.parent = parent
        Objet_sequence.__init__(self)
        
        self.num = numComp
        self.competences = []
        

    ######################################################################################  
    def __repr__(self):
        return u"Compétences : "+" ".join(self.competences)
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Competences(parent, self)
    
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
            if self.GetClasse().GetVersionNum() < 7:
                codeindic = "S"+codeindic
                    
            self.competences.append(codeindic)
        
#        self.GetPanelPropriete().MiseAJour()
    
    ######################################################################################  
    def ToogleCode(self, code):
        if code in self.competences:
            self.competences.remove(code)
        else:
            self.competences.append(code)
            
    ######################################################################################  
    def GetCode(self, num):
        return self.competences[num]
    
    ######################################################################################  
    def GetTypCode(self, num):
        return self.competences[num][0], self.competences[num][1:]
    
    ######################################################################################  
    def GetNomGenerique(self):
        return getSingulierPluriel(self.GetReferentiel().dicoCompetences["S"].nomGenerique, True)
    
    ######################################################################################  
    def GetDiscipline(self, num):
        return self.GetReferentiel().dicoCompetences[self.competences[num][0]].abrDiscipline
    
    ######################################################################################  
    def GetIntit(self, num):
        return self.GetReferentiel().getCompetence(self.competences[num])[0]

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre, u"")
#        self.codeBranche.SetBackgroundColour(wx.Colour(COUL_COMPETENCES[0]*255, COUL_COMPETENCES[1]*255, COUL_COMPETENCES[2]*255))
        t = self.GetNomGenerique()
        self.branche = arbre.AppendItem(branche, t, wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Com"])
        self.codeBranche.SetBranche(self.branche)
        self.arbre.SetItemTextColour(self.branche, couleur.GetCouleurWx(COUL_COMPETENCES))
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, self.GetNomGenerique())
#        if hasattr(self, 'panelPropriete'):
#            self.GetPanelPropriete().Destroy()
#            self.panelPropriete = PanelPropriete_Competences(self.panelParent, self)
#            self.panelPropriete.construire()
    
    
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.BASE_FICHE_HTML_COMP

    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        nc = self.GetNomGenerique()
        self.tip.SetWholeText("titre", nc)
        
        for i, c in enumerate(self.competences):
            self.tip.AjouterElemListeDL("list", 
                                 self.GetDiscipline(i) +" " + self.GetTypCode(i)[0], 
                                 self.GetIntit(i))
      
        self.tip.SetPage()

            
            
####################################################################################
#
#   Classe définissant les propriétés de savoirs
#
####################################################################################
class Savoirs(Objet_sequence):
    def __init__(self, parent, num = None, prerequis = False):
        self.parent = parent        # la séquence
        Objet_sequence.__init__(self)
        
        self.prerequis = prerequis  # Indique que ce sont des savoirs prérequis
        self.savoirs = []
        
                
    ######################################################################################  
    def __repr__(self):
        return "Savoirs : "+" ".join(self.savoirs)
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Savoirs(parent, self)
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du savoir pour enregistrement
        """
        root = ET.Element("Savoirs")
        for i, s in enumerate(self.savoirs):
            root.set("S"+str(i), s)
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        """ Interprétation de la branche (lecture fichier .seq)
             préfixes :
              - B = enseignement de base (tronc commun)
              - S = spécialité
              - M = math
              - P = physique
        """
#        print "setBranche Savoirs"
        
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
    def GetCode(self, num):
        return self.savoirs[num]
    
    ######################################################################################  
    def GetTypCode(self, num):
        return self.savoirs[num][0], self.savoirs[num][1:]
    
    ######################################################################################  
    def GetNomGenerique(self):
        return getSingulierPluriel(self.GetReferentiel().dicoSavoirs["S"].nomGenerique, True)
    
    ######################################################################################  
    def GetDiscipline(self, num):
#         print "dicoSavoirs", self.GetReferentiel().dicoSavoirs
        ref = self.GetReferentiel()
        dicSavoirs = ref.getTousSavoirs()
        for code, savoirs in dicSavoirs:
            if code == self.GetCode(num)[0]:
                return savoirs.abrDiscipline
#         return ref.dicoSavoirs[self.savoirs[num][0]].abrDiscipline
    
    ######################################################################################  
    def GetIntit(self, num):
        return self.GetReferentiel().getSavoir(self.GetCode(num))  
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        
        self.arbre = arbre
        self.codeBranche = CodeBranche(self.arbre, u"")
        t = self.GetNomGenerique()
        self.branche = arbre.AppendItem(branche, t, wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Sav"])
        self.codeBranche.SetBranche(self.branche)
        
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, self.GetNomGenerique())
#        self.GetPanelPropriete().MiseAJourTypeEnseignement()
#            self.panelPropriete.construire()
    

    
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.BASE_FICHE_HTML_SAV

    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        nc = self.GetNomGenerique()
        self.tip.SetWholeText("titre", nc)
        
        for i, c in enumerate(self.savoirs):
            self.tip.AjouterElemListeDL("list", 
                                 self.GetDiscipline(i) + " " + self.GetTypCode(i)[1], 
                                 self.GetIntit(i))
      
        self.tip.SetPage()
        
         
            

####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Seance(ElementDeSequence, Objet_sequence):
    
                  
    def __init__(self, parent, typeSeance = "", typeParent = 0, branche = None):
        """ Séance :
                parent = le parent wx pour contenir "panelPropriete"
                typeSceance = type de séance parmi "TypeSeance"
                typeParent = type du parent de la séance :  0 = séquence
                                                            1 = séance "Rotation"
                                                            2 = séance "parallèle"
        """
        self.nom_obj = "Séance"
        self.article_c_obj = "de la"
        self.article_obj = "la"
        
        self.parent = parent
        ElementDeSequence.__init__(self)
        Objet_sequence.__init__(self)
        
        # Les données sauvegardées
        self.ordre = 0
        self.ordreType = 0
        self.duree = Variable(u"Durée", lstVal = 1.0, nomNorm = "", typ = VAR_REEL_POS, 
                              bornes = [0.25,30], modeLog = False,
                              expression = None, multiple = False)
        self.intitule  = u""
        self.intituleDansDeroul = True
        self.effectif = "C"
        self.demarche = "I"
        self.systemes = []
        self.code = u""
        self.couleur = (0,0,0,1)
        self.description = None
        self.taille = Variable(u"Taille des caractères", lstVal = 100, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [10,100], modeLog = False,
                              expression = None, multiple = False)
        self.nombre = Variable(u"Nombre", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [1,10], modeLog = False,
                              expression = None, multiple = False)
        
        self.nbrRotations = Variable(u"Nombre de rotations", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
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


    ######################################################################################  
    def __repr__(self):
        t = self.code 
#        t += " " +str(self.GetDuree()) + "h"
#        t += " " +str(self.effectif)
#        for s in self.seances:
#            t += "  " + s.__repr__()
        return t
    
    
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
    def GetListeTypes(self):
        """ Renvoie la liste des types de séance compatibles
        """
        ref = self.GetReferentiel()
        if self.EstSousSeance():
            listType = ref.listeTypeActivite
            if not self.parent.EstSousSeance():
                listType = ref.listeTypeActivite +  ["S", "R"]
        else:
            listType = ref.listeTypeSeance
        
        return listType
    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la séance pour enregistrement
        """
        root = ET.Element("Seance"+str(self.ordre))
        root.set("Type", self.typeSeance)
        root.set("Intitule", self.intitule)
        root.set("Taille", str(self.taille.v[0]))
        
        if self.description != None:
            root.set("Description", self.description)
        
        root.set("Couleur", Couleur2Str(self.couleur))
        
        self.lien.getBranche(root)
        
        if self.typeSeance in ["R", "S"]:
            for sce in self.seances:
                root.append(sce.getBranche())
            root.set("nbrRotations", str(self.nbrRotations.v[0]))
#            root.set("nbrGroupes", str(self.nbrGroupes.v[0]))
            
        elif self.typeSeance in ACTIVITES:
            root.set("Demarche", self.demarche)
            root.set("Duree", str(self.duree.v[0]))
            root.set("Effectif", self.effectif)
            root.set("Nombre", str(self.nombre.v[0]))
            
            self.branchesSys = []
            for i, s in enumerate(self.systemes):
                bs = ET.SubElement(root, "Systemes"+str(i))
                self.branchesSys.append(bs)
                bs.set("Nom", s.n)
                bs.set("Nombre", str(s.v[0]))
        else:
            root.set("Duree", str(self.duree.v[0]))
            root.set("Effectif", self.effectif)
        
        root.set("IntituleDansDeroul", str(self.intituleDansDeroul))
        
        return root    
        
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche séance"
#        t0 = time.time()
        
        self.ordre = eval(branche.tag[6:])
        
        self.intitule  = branche.get("Intitule", "")
        self.taille.v[0] = eval(branche.get("Taille", "100"))
        self.typeSeance = branche.get("Type", "C")
        self.description = branche.get("Description", None)
        
        self.couleur = Str2Couleur(branche.get("Couleur", "0;0;0;1"))
        
        self.lien.setBranche(branche, self.GetPath())
        
#        t1 = time.time()
#        print "    t1", t1-t0
        
        if self.typeSeance in ["R", "S"]:
            self.seances = []
            for sce in list(branche):
                seance = Seance(self)
                self.seances.append(seance)
                seance.setBranche(sce)
            self.duree.v[0] = self.GetDuree()
            if self.typeSeance == "R":
                self.nbrRotations.v[0] = eval(branche.get("nbrRotations", str(len(self.seances))))
#                self.nbrGroupes.v[0] = eval(branche.get("nbrGroupes", str(len(self.Get???))))
                self.reglerNbrRotMaxi()
            
        elif self.typeSeance in ACTIVITES:   
            self.effectif = branche.get("Effectif", "C")
            self.demarche = branche.get("Demarche", "I")
            self.nombre.v[0] = eval(branche.get("Nombre", "1"))
#            self.lien.setBranche(branche)
            
            # Les systèmes nécessaires
            lstSys = []
            lstNSys = []
            for s in list(branche):
                nom = s.get("Nom", "")
                if nom != "":
                    lstSys.append(nom)
                    lstNSys.append(eval(s.get("Nombre", "")))
                    
#            print "lstSys", lstSys
            # Correction d'un bug versions <5.5
            # "manque des systèmes dans les séances lors de l'enregistrement"
            for s in self.GetDocument().systemes:
#                print "nom syst :", s.nom
                if not s.nom in lstSys:
                    lstSys.append(s.nom)
                    lstNSys.append(0)
                    
                
            self.AjouterListeSystemes(lstSys, lstNSys)
            
            # Durée
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        else:
            self.effectif = branche.get("Effectif", "C")
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        
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
                
        if self.typeSeance in ["R", "S"]:
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
        if self.typeSeance in ["R", "S"]:
            for se in self.seances:
                se.EnrichiSVG(doc, seance = True)
        else:
            self.EnrichiSVG(doc, seance = True)
        
        
    ######################################################################################  
    def GetEffectif(self):
        """ Renvoie l'effectif de la séance
            n : portion de classe
        """
#         print "GetEffectif", self, self.effectif
        eff = 0
        if self.typeSeance in ["R", "S"]:
            for sce in self.seances:
                eff += sce.GetEffectif() #self.seances[0].GetEffectif()
#        elif self.typeSeance == "S":
#            for sce in self.seances:
#                eff += sce.GetEffectif()
        else:
            eff = self.GetClasse().GetEffectifNorm(self.effectif)
            eff = eff * self.nombre.v[0]

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
#         print "SetEffectif", val, self.GetReferentiel().effectifs.keys()
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
                    codeEff = ""
        else:
            for k, v in self.GetReferentiel().effectifs.items():
                if v[0][:2] == val[:2]: # On ne compare que les 2 premières lettres
                    codeEff = k
        self.effectif = codeEff
        

    ######################################################################################  
    def VerifPb(self):
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
            3 : séances en rotation d'effectifs différents !!
        """
#        print "IsEffectifOk", self, 
        ok = 0 # pas de problème
        if self.typeSeance in ["R", "S"] and len(self.seances) > 0:
#            print self.GetEffectif() ,  self.GetClasse().GetEffectifNorm('G'),
            eff = round(self.GetEffectif(), 4)
            effN = round(self.GetClasse().GetEffectifNorm('G'), 4)
            if eff < effN:
                ok = 1 # Tout le groupe "effectif réduit" n'est pas occupé
            elif eff > effN:
                ok = 2 # Effectif de la séance supperieur à celui du groupe "effectif réduit"    
#            if self.typeSeance == "R":
#                continuer = True
#                eff = self.seances[0].GetEffectif()
#                i = 1
#                while continuer:
#                    if i >= len(self.seances):
#                        continuer = False
#                    else:
#                        if self.seances[i].GetEffectif() != eff:
#                            ok = 3 # séance en rotation d'effectifs différents !!
#                            continuer = False
#                        i += 1
            
        elif self.typeSeance in ["AP", "ED"] and not self.EstSousSeance():
            if self.GetEffectif() < self.GetClasse().GetEffectifNorm('G'):
                ok = 1 # Tout le groupe "effectif réduit" n'est pas occupé
        
#        print "   ", ok
        return ok


    ######################################################################################  
    def IsNSystemesOk(self):
        """ Teste s'il y a un problème de nombre de systèmes disponibles
        """
        ok = 0 # pas de problème
        if self.typeSeance in ["AP", "ED"]:
            n = self.GetNbrSystemes()
            seq = self.GetApp().sequence
            for s in seq.systemes:
                if n.has_key(s.nom) and n[s.nom] > s.nbrDispo.v[0]:
                    ok = 1
        return ok


    ######################################################################################  
    def SignalerPb(self, etatEff, etatSys):
        if hasattr(self, 'codeBranche'):
            etat = max(etatEff, etatSys)
            if etat == 0:
                couleur = 'white'
            elif etat == 1 :
                couleur = COUL_BIEN
            elif etat == 2:
                couleur = COUL_BOF
            elif etat == 3:
                couleur = "TOMATO1"
            
            if etatEff == 0:
                message = u""
            elif etatEff == 1 :
                message = u"Tout le groupe \"effectif réduit\" n'est pas occupé"
            elif etatEff == 2:
                message = u"Effectif de la Séance supérieur à celui du groupe \"effectif réduit\""
            elif etatEff == 3:
                message = u"Séances en rotation d'effectifs différents !!"
                
            if etatSys == 0:
                message += u""
            elif etatSys == 1 :
                message += u"Nombre de systèmes nécessaires supérieur au nombre de systèmes disponibles."
                
            self.codeBranche.SetBackgroundColour(couleur)
            self.codeBranche.SetToolTipString(message)
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
        if self.typeSeance in ["R", "S"]:
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
        if recurs and self.EstSousSeance() and self.parent.typeSeance in ["R", "S"]: # séance en rotation (parent = séance "Rotation")
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
        for c, n in self.GetReferentiel().demarches.items():
#        for k, v in constantes.Demarches.items():
            if n[1] == text:
                codeDem = c
                break
        self.demarche = codeDem
        
        
    ######################################################################################  
    def SetType(self, typ):
#         print "SetType", typ
        if type(typ) == str or type(typ) == unicode:
            self.typeSeance = typ
        else:
            self.typeSeance = self.GetReferentiel().listeTypeSeance[typ]
        
        if hasattr(self, 'arbre'):
            self.SetCode()
            
        if self.typeSeance in ["R","S"] and len(self.seances) == 0: # Rotation ou Serie
            self.AjouterSeance()
        
#        try:
#            self.GetPanelPropriete().AdapterAuType()
#        except AttributeError:
#            pass
            
        
        if self.EstSousSeance() and self.parent.typeSeance in ["R","S"]:
            try: # Pas terrible mais pas trouvé mieux
                self.parent.SignalerPb(self.parent.IsEffectifOk(), 0)
            except:
                pass
        
        if self.typeSeance in ["AP","ED"]:
            self.SignalerPb(0, self.IsNSystemesOk())
            
        if hasattr(self, 'arbre'):
            self.arbre.SetItemImage(self.branche, self.arbre.images[self.typeSeance])
            self.arbre.Refresh()


    ######################################################################################  
    def GetToutesSeances(self):
        l = []
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
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
        
        if self.typeSeance in ["R", "S"]:
            for sce in self.seances:
                sce.PubDescription() 
                

    ######################################################################################  
    def SetCodeBranche(self):
        if hasattr(self, 'codeBranche') and self.typeSeance != "":
            self.codeBranche.SetLabel(self.code)
            self.arbre.SetItemText(self.branche, self.GetReferentiel().seances[self.typeSeance][0])
            self.codeBranche.SetToolTipString(self.intitule)
            
                  
    ######################################################################################  
    def SetCode(self):
        self.code = self.typeSeance
        num = str(self.ordreType+1)
        
        if isinstance(self.parent, Seance):
            num = str(self.parent.ordreType+1)+"."+num
            if isinstance(self.parent.parent, Seance):
                num = str(self.parent.parent.ordreType+1)+"."+num

        self.code += num

        self.SetCodeBranche()
        
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
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
        
        self.branche = arbre.AppendItem(branche, u"Séance :", wnd = self.codeBranche, 
                                            data = self, image = image)
        self.codeBranche.SetBranche(self.branche)
        
        if hasattr(self, 'branche'):
            self.SetCodeBranche()
            
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for sce in self.seances:
                sce.ConstruireArbre(arbre, self.branche)
            
        
    ######################################################################################  
    def OrdonnerSeances(self):
        listeTypeSeance = self.GetReferentiel().listeTypeSeance
        dicType = {k:0 for k in listeTypeSeance}
        dicType[''] = 0
        RS = 0
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
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
        
        self.GetApp().sendEvent(modif = u"Collé d'un élément")
        
        wx.CallAfter(self.arbre.SelectItem, seance.branche)        


    ######################################################################################  
    def AjouterSeance(self, event = None):
        """ Ajoute une séance é la séance
            !! Uniquement pour les séances de type "Rotation" ou "Serie" !!
        """
        seance = Seance(self)
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
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
        
        wx.CallAfter(self.arbre.SelectItem, seance.branche)


    ######################################################################################  
    def SupprimerSeance(self, event = None, item = None):
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            if len(self.seances) > 1: # On en laisse toujours une !!
                seance = self.arbre.GetItemPyData(item)
                self.seances.remove(seance)
                self.arbre.Delete(item)
                self.OrdonnerSeances()
                self.GetApp().sendEvent(modif = u"Suppression d'une Séance")
            if self.typeSeance == "R":  # Séances en Rotation
                self.reglerNbrRotMaxi()
        return
    
    
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
    
    
    ######################################################################################  
    def SupprimerSousSeances(self):
        self.arbre.DeleteChildren(self.branche)

    
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if self.typeSeance in ["R", "S"]:
            for s in self.seances:
                s.MiseAJourTypeEnseignement()
#        else:
#            self.GetPanelPropriete().MiseAJourTypeEnseignement()
        
    ######################################################################################  
    def MiseAJourNomsSystemes(self):
        if self.typeSeance in ACTIVITES:
            sequence = self.GetDocument()
            for i, s in enumerate(sequence.systemes):
                self.systemes[i].n = s.nom
#            self.nSystemes = len(sequence.systemes)
#            self.GetPanelPropriete().MiseAJourListeSystemes()
                                 
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.MiseAJourNomsSystemes()
        
    ######################################################################################  
    def SupprimerSysteme(self, i):
        if self.typeSeance in ACTIVITES:
            del self.systemes[i]
#            self.GetPanelPropriete().ConstruireListeSystemes()
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.SupprimerSysteme(i)

        
        
    ######################################################################################  
    def AjouterSysteme(self, nom = "", nombre = 0, construire = True):
        if self.typeSeance in ACTIVITES:
            self.systemes.append(Variable(nom, lstVal = nombre, nomNorm = "", typ = VAR_ENTIER_POS, 
                                          bornes = [0,9], modeLog = False,
                                          expression = None, multiple = False))
#            if construire:
#                self.GetPanelPropriete().ConstruireListeSystemes()
                
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.AjouterSysteme(nom, nombre)
    
    
    ######################################################################################  
    def AjouterListeSystemes(self, lstSys, lstNSys = None):
#        print "  AjouterListeSystemes", self.typeSeance
        if self.typeSeance in ACTIVITES:
            if lstNSys == None:
                lstNSys = [0]*len(lstSys)
            for i, s in enumerate(lstSys):
#                print "    ", s
                self.AjouterSysteme(s, lstNSys[i], construire = False)
#            self.GetPanelPropriete().ConstruireListeSystemes()
            
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.AjouterListeSystemes(lstSys, lstNSys) 
                
                
    
    
    ######################################################################################  
    def GetReferentiel(self):
        return  self.GetDocument().GetReferentiel()
        
    ######################################################################################  
    def GetClasse(self):
        return self.GetDocument().classe
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            listItems = [[u"Supprimer", 
                          functools.partial(self.parent.SupprimerSeance, item = itemArbre), 
                          images.Icone_suppr_seance.GetBitmap()],
                         [u"Créer un lien", 
                          self.CreerLien, 
                          None]]
            
            if self.typeSeance in ["R", "S"]:
                listItems.append([u"Ajouter une séance", 
                                  self.AjouterSeance, 
                                  images.Icone_ajout_seance.GetBitmap()])
            
            listItems.append([u"Copier", 
                              self.CopyToClipBoard, 
                              getIconeCopy()])
            
            ################
            elementCopie = GetObjectFromClipBoard('Seance')
            if elementCopie is not None:
                dataSource = Seance(self.parent)
                dataSource.setBranche(elementCopie)
                
                if not hasattr(self, 'GetNiveau') or self.GetNiveau() + dataSource.GetProfondeur() > 2:
                    return
                
                if self.typeSeance in ["R", "S"] : # la phase est la même
                    t = u"Coller dans"
                else:
                    t = u"Coller après"
                listItems.append([t, functools.partial(self.CollerElem, 
                                                                         item = itemArbre, 
                                                                         bseance = elementCopie),
                                  getIconePaste()])
                            
            self.GetApp().AfficherMenuContextuel(listItems)                      

            
    ######################################################################################  
    def GetNbrSystemes(self, complet = False, simple = False):
        """ Renvoie un dictionnaire :
                clef : nom du système
                valeur : nombre d'exemplaires de ce système utilisés dans la séance
        """
        def up(d, k, v):
            if d.has_key(k):
                d[k] += v
            else:
                d[k] = v
                
        d = {}
        if self.typeSeance in ["S", "R"]:
            if self.typeSeance == "S" or complet:
                
                for seance in self.seances:
                    dd = seance.GetNbrSystemes(complet)
                    for k, v in dd.items():
                        up(d, k, v)

            else:
                for s in self.systemes:
                    if s.n <>"":
                        up(d, s.n, s.v[0]*self.nombre.v[0])
#                        d[s.n] = s.v[0]*self.nombre.v[0]
        else:
            for s in self.systemes:
                if s.n <>"":
                    if simple:
                        up(d, s.n, s.v[0])
                    else:
                        up(d, s.n, s.v[0]*self.nombre.v[0])        
        return d



    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.BASE_FICHE_HTML_SEANCE

    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        ref = self.GetReferentiel()
        titre = u"Séance "+ self.code
        self.tip.SetWholeText("titre", titre)
        
        # Type de séance
        if self.typeSeance != "":
            self.tip.AjouterImg("icon", constantes.imagesSeance[self.typeSeance].GetBitmap())
            self.tip.SetWholeText("txt", ref.seances[self.typeSeance][1], 
                                  bold = True, size = 3,
                                  fcoul = couleur.GetCouleurHTML(BCoulSeance[self.typeSeance]))
        
        else:
            self.tip.Supprime('icon')
        
        
        
        # Démarche
        if len(ref.listeDemarches) > 0:
            self.tip.AjouterImg("icon2", constantes.imagesDemarches[self.demarche].GetBitmap(), width = 64)
            self.tip.SetWholeText("txt2", ref.demarches[self.demarche][1], italic = True, size = 3)
        else:
            self.tip.Supprime('icon2')
        
        # Intitulé
        self.tip.SetWholeText("int", self.intitule, size = 5)
        
        if hasattr(self, 'description'):
            self.tip.AjouterHTML("des", XMLtoHTML(self.description))    
        else:
            self.tip.Supprime('ldes')
        
        self.tip.SetPage()
        
        





####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Tache(Objet_sequence):
    
                  
    def __init__(self, projet, intitule = u"", phaseTache = "", duree = 1.0, branche = None):
        """ Séance :
                panelParent = le parent wx pour contenir "panelPropriete"
                phaseTache = phase de la tache parmi 'Ana', 'Con', 'Rea', 'Val'
        """
#        print "__init__ tâche", phaseTache
        self.nom_obj = "Tâche"
        self.article_c_obj = "de la"
        self.article_obj = "la"
        
        self.projet = projet
        Objet_sequence.__init__(self)
        
        # Les données sauvegardées
        self.ordre = 100
        self.duree = Variable(u"Volume horaire (h)", lstVal = duree, nomNorm = "", typ = VAR_REEL_POS, 
                              bornes = [0.5,40], modeLog = False,
                              expression = None, multiple = False)
        self.intitule  = intitule
        self.intituleDansDeroul = True
        
        # Les élèves concernés (liste d'élèves)
        self.eleves = []

        # Le code de la tâche (affiché dans l'arbre et sur la fiche
        self.code = u""
        
        # La description de la tâche
        self.description = None

        # Une icône pour illustrer la tâche
        self.icone = None
        
        # Les autres données
        
#        self.panelParent = panelParent
        
        self.phase = phaseTache
        
        
#        
        if branche != None:
            self.setBranche(branche)
##            if not Ok:
##                self.code = -err # Pour renvoyer une éventuelle erreur à l'ouverture d'un fichier
        else:
#        if branche == None:
            self.indicateursEleve = self.IndicateursEleveDefaut()
            if phaseTache in TOUTES_REVUES_SOUT:
                self.indicateursMaxiEleve = self.IndicateursEleveDefaut()
                
                
        
    def __eq__(self, tache):
        if tache == None:
            return False
        return self.code == tache.code and self.ordre == tache.ordre
  
    
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

    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Tache(parent, self)
    
    ######################################################################################  
    def ActualiserDicIndicateurs(self):
        """ Complète le dict des compétences/indicateurs globaux (tous les élèves confondus)
        """
#        print "ActualiserDicIndicateurs", self
        for i in range(len(self.projet.eleves)):
            for c in self.indicateursEleve[i+1]:
                if not c in self.indicateursEleve[0]:
                    self.indicateursEleve[0].append(c)


    ######################################################################################  
    def estPredeterminee(self):
        return len(self.GetProjetRef().taches) > 0 
            
        
    ######################################################################################  
    def GetDicIndicateurs(self):
        """ Renvoie l'ensemble des indicateurs de compétences à mobiliser pour cette tâche
            Dict :  clef = code compétence
                  valeur = liste [True False ...] des indicateurs à mobiliser
        """
#        print "GetDicIndicateurs", self, ":", self.indicateursEleve
#        print self.GetProjetRef()._dicoIndicateurs_simple
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
                    
        return indicateurs
    
    
    ######################################################################################  
    def GetDicIndicateursEleve(self, eleve):
        """ Renvoie l'ensemble des indicateurs de compétences à mobiliser pour cette REVUE
            Dict :  clef = code type+compétence
                  valeur = liste [True False ...] des indicateurs à mobiliser
        """
#        print "GetDicIndicateursEleve", self, eleve.id+1
        indicateurs = {}
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
        """ Renvoie True si cette REVUE est différente selon l'élève
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

        if self.description != None:
            root.set("Description", self.description)
        
        if self.icone != None:
            root.set("Icone", img2str(self.icone.ConvertToImage()))
            
        root.set("Duree", str(self.duree.v[0]))
        
        brancheElv = ET.Element("Eleves")
        root.append(brancheElv)
        for i, e in enumerate(self.eleves):
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
                for e, indicateurs in self.indicateursEleve.items()[1:]:
                    if e > len(self.projet.eleves):
                        break
                    brancheE = ET.Element("Eleve"+str(e))
                    brancheCmp.append(brancheE)
                    for i, c in enumerate(indicateurs):
                        brancheE.set("Indic"+str(i), c)
                        
            elif not self.phase in TOUTES_REVUES_EVAL:
                for i, c in enumerate(self.indicateursEleve[0]):
                    brancheCmp.set("Indic"+str(i), c)
            
        root.set("IntituleDansDeroul", str(self.intituleDansDeroul))
        return root    
        
    ######################################################################################  
    def setBranche(self, branche):
        """
        """
        err = []
        ref = self.GetProjetRef()
        self.ordre = eval(branche.tag[5:])
        self.intitule  = branche.get("Intitule", "")
        
        self.phase = branche.get("Phase", "") 

        debug = False#self.phase == "R1"
        if debug: print "setBranche tâche", self.phase
        
        # Suite commentée ... à voir si pb
#        if self.GetTypeEnseignement() == "SSI":
#            if self.phase == 'Con':
#                self.phase = 'Ana'
#            elif self.phase in ['DCo', 'Val']:
#                self.phase = 'Rea'

        self.description = branche.get("Description", None)
        
        data = branche.get("Icone", "")
        if data != "":
            try:
                self.icone = PyEmbeddedImage(data).GetBitmap()
            except:
                self.icone = None
                
                
        if not self.phase in TOUTES_REVUES_EVAL_SOUT:
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        else:
            self.duree.v[0] = constantes.DUREE_REVUES
        
        brancheElv = branche.find("Eleves")
        self.eleves = []
        for i, e in enumerate(brancheElv.keys()):
            self.eleves.append(eval(brancheElv.get("Eleve"+str(i))))
        
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
                        else:
                            lst = [True]*len(ref._dicIndicateurs[e])
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
                    if debug: print "   1"
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
                                    if self.phase == 'XXX' and self.GetReferentiel().getTypeIndicateur(codeindic) == 'C':
                                        continue
                                    
#                                    try:
#                                            print "***",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                                        # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                                        
                                    if not code in ref._dicoIndicateurs_simple[disc]:
                                        print "Erreur 1", code, "<>", ref._dicoIndicateurs_simple[disc]
                                        err.append(constantes.Erreur(constantes.ERR_PRJ_T_TYPENS))
                                        return err
                                    
                                    if debug: print "   ", codeindic
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
                                    if self.phase == 'XXX' and self.GetReferentiel().getTypeIndicateur(codeindic) == 'C':
                                        continue
                                    
#                                        print "******",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                                        
                                    # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                                    if not code in ref._dicIndicateurs:
                                        print "Erreur 2"
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
                            if self.phase == 'XXX' and ref.getTypeIndicateur(codeindic) == 'C':
                                continue
                            
                                
#                                try:
#                                    print "******",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                            # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                            for disc, dic in ref._dicoIndicateurs_simple.items():
                                if code[0] == disc:
                                    if not code[1:] in dic.keys():
                                        print "Erreur 3", code, "<>", ref._dicoIndicateurs_simple[disc]
                                        if not constantes.Erreur(constantes.ERR_PRJ_T_TYPENS) in err:
                                            err.append(constantes.Erreur(constantes.ERR_PRJ_T_TYPENS))
                                    else:
                                        self.indicateursEleve[0].append(codeindic)
        
        
        if debug: print "   indicateursEleve", self.indicateursEleve
        
        if not self.estPredeterminee():
            self.ActualiserDicIndicateurs()
            
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
        if self.estPredeterminee() > 0:
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
        
        if self.phase != "":
            if self.phase in TOUTES_REVUES_EVAL_SOUT:
                self.code = self.phase
            else:
                self.code = self.GetProjetRef().phases[self.phase][2]+num     #constantes.CODE_PHASE_TACHE[typeEns][self.phase]+num
        else:
            self.code = num

        
        #
        # Branche de l'arbre
        #
        if hasattr(self, 'codeBranche') and self.phase != "":
            if self.phase in TOUTES_REVUES_EVAL_SOUT:
                self.codeBranche.SetLabel(u"")
                code = self.GetProjetRef().phases[self.phase][1]
            else:
                if self.estPredeterminee():
                    code = self.intitule
                    intitule = self.GetProjetRef().taches[self.intitule][1]
                    
                else:
                    code = self.code
                    intitule = self.intitule
                    
                i = intitule.replace("\n", " - ")
                i = i[:constantes.LONGUEUR_INTITULE_ARBRE]
                if len(intitule) != len(i):
                    i += "..."
                self.codeBranche.SetLabel(i)
                self.codeBranche.SetToolTipString(intitule)
                code += u" :"
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
            
        self.branche = arbre.AppendItem(branche, u"Tâche :", wnd = self.codeBranche, 
                                        data = self, image = image)
        self.codeBranche.SetBranche(self.branche)
        
        if self.phase in TOUTES_REVUES_EVAL:
            arbre.SetItemTextColour(self.branche, "red")
        elif self.phase == "Rev":
            arbre.SetItemTextColour(self.branche, "ORANGE")
        elif self.phase == "S":
            arbre.SetItemTextColour(self.branche, "PURPLE")
    
    
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
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.SupprimerSysteme(i)

        
    ######################################################################################  
    def AjouterEleve(self):
        return
#        self.GetPanelPropriete().ConstruireListeEleves()
    
    
    ######################################################################################  
    def SupprimerEleve(self, i):
        if i in self.eleves:
            self.eleves.remove(i)

        for i, ident in enumerate(self.eleves):
            if ident > i:
                self.eleves[i] = ident-1

#        self.GetPanelPropriete().ConstruireListeEleves()
        

    
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
                listItems = [[u"Supprimer", 
                              functools.partial(self.projet.SupprimerTache, item = itemArbre), 
                              images.Icone_suppr_tache.GetBitmap()]]
            else:
                listItems = []
            listItems.append([u"Insérer une revue après", 
                              functools.partial(self.projet.InsererRevue, item = itemArbre), 
                              images.Icone_ajout_revue.GetBitmap()])

            if self.phase not in TOUTES_REVUES_EVAL_SOUT:
                listItems.append([u"Copier", 
                                  self.CopyToClipBoard, 
                                  getIconeCopy()])
 
            elementCopie = GetObjectFromClipBoard('Tache')
            if elementCopie is not None:
                phase = elementCopie.get("Phase", "")
                if self.phase == phase or self.GetPhaseSuivante() == phase : # la phase est la même
                    listItems.append([u"Coller après", functools.partial(self.projet.CollerElem, 
                                                                         item = itemArbre, 
                                                                         btache = elementCopie),
                                      getIconePaste()])
                    
            self.GetApp().AfficherMenuContextuel(listItems)
       
        

    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.BASE_FICHE_HTML_TACHE
    

    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        
        if self.phase in TOUTES_REVUES_SOUT:
            titre = self.GetProjetRef().phases[self.phase][1]
            texte = draw_cairo.getHoraireTxt(self.GetDelai())

        else:
            if self.estPredeterminee():
                p = self.intitule
            else:
                p = self.code
                    
            titre = u"Tâche "+ p
            if self.phase != "":
                    t = self.GetProjetRef().phases[self.phase][1]
            else:
                t = u""
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
                t = u""
            self.tip.AjouterTxt("int", t, size = 4)
        
        if hasattr(self, 'description'):
            self.tip.AjouterHTML("des", XMLtoHTML(self.description))    
        else:
            self.tip.Supprime('ldes')
        self.tip.SetPage()
        
        
        
        
####################################################################################
#
#   Classe définissant les propriétés d'un système
#
####################################################################################
class Systeme(ElementDeSequence, Objet_sequence):
    def __init__(self, parent, nom = u""):
        
        self.parent = parent
        ElementDeSequence.__init__(self)
        Objet_sequence.__init__(self)
        
        self.nom = nom
        self.nbrDispo = Variable(u"Nombre dispo", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [0,20], modeLog = False,
                              expression = None, multiple = False)
        self.image = None
        self.lienClasse = None
        
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
        
    ######################################################################################  
    def __repr__(self):
        if self.image != None:
            i = img2str(self.image.ConvertToImage())[:20]
        else:
            i = "None"
        return self.nom+" ("+str(self.nbrDispo.v[0])+") " + i
        
        

    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Systeme(parent, self)
    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
        root = ET.Element("Systeme")
        if self.lienClasse != None:
            root.set("NomClasse", self.lienClasse.nom)
            
        else:
            root.set("Nom", self.nom)
            self.lien.getBranche(root)
            root.set("Nbr", str(self.nbrDispo.v[0]))
            if self.image != None:
                root.set("Image", img2str(self.image.ConvertToImage()))
        
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche systeme"
        nomClasse  = branche.get("NomClasse", "")
        if nomClasse != u"" and isinstance(self.parent, Sequence):
            classe = self.parent.classe
#            print "   >>", classe
            for s in classe.systemes:
                if s.nom == nomClasse:
                    self.lienClasse = s
                    self.setBranche(s.getBranche())
#                    self.GetPanelPropriete().Verrouiller(False)
#                        self.panelPropriete.cbListSys.SetSelection(self.panelPropriete.cbListSys.FindString(self.nom))
                    break
            
                
        else:
            self.nom  = branche.get("Nom", "")
            self.lien.setBranche(branche, self.GetPath())
    
            self.nbrDispo.v[0] = eval(branche.get("Nbr", "1"))
            
            data = branche.get("Image", "")
            if data != "":
                self.image = PyEmbeddedImage(data).GetBitmap()
            else:
                self.image = None
            
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
            return u"Système ou matériel"

    ######################################################################################  
    def SetCode(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetToolTipString(self.GetNom() + u"\nNombre disponible : " + str(self.nbrDispo.v[0]))
        
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
        self.SetNombre()
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", 
                                                     functools.partial(self.parent.SupprimerSysteme, item = itemArbre),
                                                     images.Icone_suppr_systeme.GetBitmap()],
                                                    [u"Créer un lien", self.CreerLien, None]])
            
    
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.BASE_FICHE_HTML_SYSTEME
    
    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        
        self.tip.SetWholeText("nom", self.nom)
        self.tip.SetWholeText("nbr", u"Nombre disponible : " + str(self.nbrDispo.v[0]))
        
        self.tip.AjouterImg("img", self.image) 
        
        self.tip.SetPage()
        
               
               
               
  

####################################################################################
#
#   Classe définissant les propriétés d'une seance d'emploi du temps
#
####################################################################################
class Seance_EDT(ElementDeSequence, Objet_sequence):
    def __init__(self, parent, nom = u""):
        
        self.nom_obj = "Séance"
        self.article_c_obj = "de la"
        self.article_obj = "la"
        
        self.parent = parent
        ElementDeSequence.__init__(self)
        Objet_sequence.__init__(self)
        
        
        self.jour = 0       # jour de la semaine (lundi = 0)
        self.groupe = 0     # 0 = classe entière
        self.debut = 0      # 0 = 8h00 ; 1 = 8h15 ...
        self.duree = 1      # 1 par 1/4 d'heure
        
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML pour enregistrement
        """
        root = self.getBranche_TOTAL('intitule','jour','groupe','debut', 'duree')
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        return self.setBranche_TOTAL(branche)

    ######################################################################################  
    def GetPanelPropriete(self, parent):
        return PanelPropriete_Seance_EDT(parent, self)




####################################################################################
#
#   Classe définissant les propriétés d'un emploi du temps
#
####################################################################################
class EDT(ElementDeSequence, Objet_sequence):
    def __init__(self, parent, nom = u""):
        
        self.nom_obj = "Emploi du temps"
        self.article_c_obj = "d'"
        self.article_obj = "l'"
        
        self.parent = parent
        ElementDeSequence.__init__(self)
        Objet_sequence.__init__(self)

        self.seances = []

####################################################################################
#
#   Classe définissant les propriétés d'un calendrier de progression
#
####################################################################################
class Calendrier(ElementDeSequence, Objet_sequence):
    def __init__(self, parent, annee, nom = u""):
        
        self.nom_obj = "Calendrier"
        self.article_c_obj = "du"
        self.article_obj = "le"
        
        self.parent = parent
        ElementDeSequence.__init__(self)
        Objet_sequence.__init__(self)
        
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
        self.intitule = branche.get("Intitule", u"")
        self.annee = eval(branche.get("Annee", str(constantes.getAnneeScolaire())))

    
    ######################################################################################  
    def GetAnneeFin(self):
        return self.annee + len(self.GetReferentiel().periodes)


    ######################################################################################  
    def GetNbrAnnees(self):
        return self.GetAnneeFin() - self.annee


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
class Support(ElementDeSequence, Objet_sequence):
    def __init__(self, parent, nom = u""):
        
        self.nom_obj = "Support"
        self.article_c_obj = "du"
        self.article_obj = "le"
        
        self.parent = parent
        ElementDeSequence.__init__(self)
        Objet_sequence.__init__(self)
        
        self.nom = nom
        self.description = None
        
        self.image = None
        
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
        
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
        if self.image != None:
            root.set("Image", img2str(self.image.ConvertToImage()))
        
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        Ok = True
        self.nom  = branche.get("Nom", "")
        self.description = branche.get("Description", None)
        Ok = Ok and self.lien.setBranche(branche, self.GetPath())

        data = branche.get("Image", "")
        if data != "":
            try :
                self.image = PyEmbeddedImage(data).GetBitmap()
            except:
                self.image = None
                Ok = False
        
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
        return self.nom
    
            
    ######################################################################################  
    def GetCode(self, i = None):
        return u"Support"


    ######################################################################################  
    def GetIntit(self, i = None):
        return self.nom


    ######################################################################################  
    def SetCode(self):
#        if hasattr(self, 'codeBranche'):
#            self.codeBranche.SetLabel(self.nom)
        if self.nom != "":
            t = self.nom
        else:
            t = u"Support"
        
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
            
#        # Tip
#        if hasattr(self, 'tip'):
#            self.tip.SetTexte(u"Nom : "+self.nom, self.tip_nom)
            

#    ######################################################################################  
#    def SetImage(self):
#        self.tip.SetImage(self.image, self.tip_image)
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        image = self.arbre.images["Sup"]
        self.branche = arbre.AppendItem(branche, u"Support", data = self,#, wnd = self.codeBranche
                                        image = image)
#        if hasattr(self, 'tip'):
#            self.tip.SetBranche(self.branche)

        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Créer un lien", self.CreerLien, None]])
            
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.BASE_FICHE_HTML_SUPPORT

    
    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
        
        self.tip.SetWholeText("nom", self.nom, size=5)
        self.tip.AjouterHTML("des", XMLtoHTML(self.description))       
        self.tip.AjouterImg("img", self.image, width = 300) 
        #self.tip.Supprime('img')
        self.tip.SetPage()
    





    
####################################################################################
#
#   Classe définissant les propriétés d'une personne
#
####################################################################################
class Personne(Objet_sequence):
    def __init__(self, doc, Id = 0):
        self.doc = doc
        Objet_sequence.__init__(self)

        self.nom = u""
        self.prenom = u""
        self.avatar = None
        self.id = Id # Un identifiant unique = nombre > 0


    ######################################################################################  
    def __eq__(self, personne):
        return self.GetNom() == personne.GetNom() and self.GetPrenom() == personne.GetPrenom()
    
    
    ######################################################################################  
    def GetApp(self):
        return self.doc.GetApp()


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
#        print "getBranche", supprime_accent(self.titre)
        root = ET.Element(toSystemEncoding(constantes.supprime_accent(self.titre).capitalize()))
        
        root.set("Id", str(self.id))
        root.set("Nom", self.nom)
        root.set("Prenom", self.prenom)
        if self.avatar != None:
            root.set("Avatar", img2str(self.avatar.ConvertToImage()))
        
        if hasattr(self, 'referent'):
            root.set("Referent", str(self.referent))
            
        if hasattr(self, 'discipline'):
            root.set("Discipline", str(self.discipline))
            
        if hasattr(self, 'grille'):
            for k, g in self.grille.items():
                root.set("Grille"+k, toSystemEncoding(g.path))       
            
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche personne"
        Ok = True
        self.id  = eval(branche.get("Id", "0"))
        self.nom  = branche.get("Nom", "")
        self.prenom  = branche.get("Prenom", "")
        data = branche.get("Avatar", "")
        if data != "":
            try:
                self.avatar = PyEmbeddedImage(data).GetBitmap()
            except:
                Ok = False
                self.avatar = None
            
        if hasattr(self, 'referent'):   # prof
            self.referent = eval(branche.get("Referent", "False"))
            
        if hasattr(self, 'discipline'): # prof
            self.discipline = branche.get("Discipline", 'Tec')
            
        if hasattr(self, 'grille'):     # élève
#            print self.grille
            for k in self.GetProjetRef().parties.keys():
                self.grille[k] = Lien(typ = "f")
                self.grille[k].path = toFileEncoding(branche.get("Grille"+k, r""))
#                print self.grille
#            self.grille[0].path = branche.get("Grille0", u"")
#            self.grille[1].path = branche.get("Grille1", u"")
            
#        self.GetPanelPropriete().SetImage()
#        self.GetPanelPropriete().MiseAJourTypeEnseignement()
#        self.GetPanelPropriete().MiseAJour(marquerModifier = False)
        
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
        if disc and hasattr(self, 'discipline') and constantes.CODE_DISCIPLINES[self.discipline] != u"":
            d = u' ('+constantes.CODE_DISCIPLINES[self.discipline]+')'
        else:
            d = u""
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
         
        self.SetTip()
        
    
    ######################################################################################  
    def GetAvatar(self):
        if self.avatar is None:
            return constantes.AVATAR_DEFAUT
        else:
            return self.avatar


    ######################################################################################  
    def SetTip(self):
        self.tip.SetHTML(self.GetFicheHTML())
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
#            self.tip.SetImage(self.avatar, self.tip_avatar)

    ######################################################################################  
    def SetImage(self):
        self.SetTip()
#        return
#        self.tip.SetImage(self.avatar, self.tip_avatar)
#        self.SetTip()
        
    




####################################################################################
#
#   Classe définissant les propriétés d'un élève
#
####################################################################################
class Eleve(Personne, Objet_sequence):
    def __init__(self, doc, ident = 0):
        
        self.titre = u"élève"
        self.code = "Elv"
        
        self.grille = {} #[Lien(typ = 'f'), Lien(typ = 'f')]
        for k in doc.GetProjetRef().parties.keys():
            self.grille[k] = Lien(typ = 'f')
        
        Personne.__init__(self, doc, ident)
 
    
            
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
        try:
            self.grille[k].Afficher(self.GetDocument().GetPath())#os.startfile(self.grille[num])
        except:
            messageErreur(None, u"Ouverture impossible",
                          u"Impossible d'ouvrir le fichier\n\n%s!\n" %toSystemEncoding(self.grille[k].path))
            
            
    ######################################################################################  
    def OuvrirGrilles(self, event):
        for k in self.grille.keys():
            self.OuvrirGrille(k)
#        if self.GetTypeEnseignement(simple = True) == "STI2D":
#            self.OuvrirGrille(1)
        
        
    ######################################################################################  
    def getNomFichierDefaut(self, prefixe):
        return getNomFichier(prefixe, self.GetNomPrenom()+"_"+self.GetDocument().intitule[:20])

        
    ######################################################################################  
    def GetNomGrilles(self, path = None):
        """ Renvoie les noms des fichiers grilles à générer
        """
#        print "GetNomGrilles"
        prj = self.GetDocument().GetProjetRef()
#        print prj
#        print prj.grilles
        #
        # Création des noms des fichiers grilles
        #
        # Par défaut = chemin du fichier .prj
        if path == None:
            path = os.path.dirname(self.GetDocument().GetApp().fichierCourant)
            
        nomFichiers = {} 
        for part, g in prj.parties.items():
            prefixe = "Grille_"+g
            gr = prj.grilles[part]
#            print gr
            if grilles.EXT_EXCEL != None:
#                extention = os.path.splitext(ref.grilles_prj[k][0])[1]
                extention = grilles.EXT_EXCEL
                
                if gr[1] == 'C': # fichier "Collectif"
                    nomFichiers[part] = os.path.join(path, self.GetDocument().getNomFichierDefaut(prefixe)) + extention
                else:
                    nomFichiers[part] = os.path.join(path, self.getNomFichierDefaut(prefixe)) + extention
#        print "   >", nomFichiers
        return nomFichiers


    ######################################################################################  
    def GenererGrille(self, event = None, path = None, nomFichiers = None, messageFin = True):
#        print "GenererGrille élève", self
#        print "  ", nomFichiers
        if nomFichiers == None:
            nomFichiers = self.GetNomGrilles(path)
            if not self.GetDocument().TesterExistanceGrilles({0:nomFichiers}):
                return []
            
#        print "  Fichiers :", nomFichiers
        
        prj = self.GetDocument().GetProjetRef()
        
        #
        # Ouverture (et pré-sauvegarde) des fichiers grilles "source" (tableaux Excel)
        #
        tableaux = {}
        for k, f in nomFichiers.items():
            if os.path.isfile(f):
                tableaux[k] = grilles.getTableau(self.GetDocument().GetApp(), f)
            else:
                if os.path.isfile(grilles.getFullNameGrille(prj.grilles[k][0])):
                    tableaux[k] = grilles.getTableau(self.GetDocument().GetApp(),
                                                     prj.grilles[k][0])
                else: # fichier original de grille non trouvé ==> nouvelle tentative avec les noms du référentiel par défaut
                    prjdef = REFERENTIELS[self.GetDocument().GetTypeEnseignement()].getProjetDefaut()
                    tableaux[k] = None
                    messageErreur(self.GetDocument().GetApp(), u"Fichier non trouvé !",
                                  u"Le fichier original de la grille,\n    " + prjdef.grilles[k][0] + u"\n" \
                                  u"n'a pas été trouvé ! \n")
                        
            
            if tableaux[k] != None: # and tableaux[k].filename !=f:
#                print "      créé :", f
                try:
                    tableaux[k].save(f, ConflictResolution = 2)
                except:
                    messageErreur(self.GetDocument().GetApp(), u"Erreur !",
                                  u"Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
                                  u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
                                  u" - que le dossier choisi n'est pas protégé en écriture"%f)

        if tableaux == None:
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
                messageErreur(self.GetDocument().GetApp(), u"Erreur !",
                              u"Impossible de modifier les grilles !") 


        #
        # Enregistrement final des grilles
        #
        for k, t in tableaux.items():
            try:
                t.save()
            except:
                messageErreur(self.GetDocument().GetApp(), u"Erreur !",
                              u"Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
                              u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
                              u" - que le dossier choisi n'est pas protégé en écriture" %f)
            try:
                t.close()
            except:
                pass
            self.grille[k] = Lien(typ = 'f')
            self.grille[k].path = toFileEncoding(nomFichiers[k])
        
        
        #
        # Message de fin
        #
        if messageFin:
            t = u"Génération "
            if len(tableaux)>1:
                t += u"des grilles"
            else:
                t += u"de la grille"
            t += u"\n\n"
            t += u"\n".join(nomFichiers.values())
            t += u"terminée avec "
            if len(log) == 0:
                t += u"succès !"
            else:
                t += u"des erreurs :\n"
                t += u"\n".join(log)
            messageInfo(self.GetDocument().GetApp(), t, u"Génération terminée")
            
        
#        self.GetPanelPropriete().MiseAJour()
        return log
        
        
    ######################################################################################  
    def GetEvaluabilite(self, complet = False, compil = False):
        """ Renvoie l'évaluabilité
            % conduite
            % soutenance
            ev, ev_tot, seuil
            
            compil = renvoie des dictionnaire plus simples
        """ 
#        print "GetEvaluabilite", self
        prj = self.GetProjetRef()
#        dicPoids = self.GetReferentiel().dicoPoidsIndicateurs_prj
        dicIndicateurs = self.GetDicIndicateurs()
#        print "dicIndicateurs", dicIndicateurs
#        print "_dicoGrpIndicateur", prj._dicoGrpIndicateur
#        tousIndicateurs = prj._dicIndicateurs
#        lstGrpIndicateur = {'R' : prj._dicGrpIndicateur['R'],
#                            'S' : self.GetProjetRef()._dicGrpIndicateur['S']}
#        print lstGrpIndicateur
        
#        r, s = 0, 0
#        ler, les = {}, {}
        
#        rs = [0, 0]
#        lers = [{}, {}]
        
        rs = {}
        lers = {}
        for disc, dic in prj._dicoGrpIndicateur.items():
            rs[disc] = {}
            lers[disc] = {}
            for ph in dic.keys():
                lers[disc][ph] = {}
                rs[disc][ph] = 0
#        print "   init :", rs, lers
        
        def getPoids(listIndic, comp, poidsGrp):
            """ 
            """
#            print "getPoids", listIndic, comp, poidsGrp
            for disc, dic in prj._dicoGrpIndicateur.items():
                for ph in dic.keys():
                    if grp in dic[ph]:
                        for i, indic in enumerate(listIndic):
                            if disc+comp in dicIndicateurs.keys():
                                if dicIndicateurs[disc+comp][i]:
    #                                print "  comp", grp, comp, i, indic.poids, ph
                                    poids = indic.poids
                                    if ph in poids.keys():
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
                if len(grpComp) > 2 :
                    titre, dicComp, poidsGrp = grpComp
                else:
                    titre, dicComp = grpComp
                    poidsGrp = 1
    #            print "    ", grp, poidsGrp
                
                if type(dicComp) == list:                       # 1 niveau
                    getPoids(dicComp, grp, poidsGrp)
                else:
                    for comp, lstIndic in dicComp.items():
    #                    print "      ", comp
                        if type(lstIndic[1]) == list:           # 2 niveaux
                            getPoids(lstIndic[1], comp, poidsGrp)    
                        else:                                   # 3 niveaux
                            for scomp, lstIndic2 in lstIndic.items():
                                getPoids(lstIndic2[1], scomp, poidsGrp)
                                
                                                               
#        r, s = rs
#        ler, les = lers
#        print "   eval :", rs, lers
         
        # On corrige s'il n'y a qu'une seule grille (cas SSI jusqu'à 2014)
#        if len(self.GetReferentiel().grilles_prj) == 1: 
##        if self.GetTypeEnseignement() == "SSI":
#            r, s = r*2, s*2
#            for l in ler.keys():
#                ler[l] = ler[l]*2
#            for l in les.keys():
#                les[l] = les[l]*2
            
#        if "O8s" in les.keys():
#            les["O8"] = les["O8s"]
#            del les["O8s"]
            
#        print r, s, ler, les
        
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
        
#        print "   ", ev, ev_tot, seuil
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
        lst = []
        for t in self.GetDocument().taches:
            if self.id in t.eleves:
                lst.extend(t.competences)
        lst = list(set(lst))
        return lst
    
    
    ######################################################################################  
    def GetDicIndicateurs(self, limite = None):
        """ Renvoie un dictionnaire des indicateurs que l'élève doit mobiliser
             (pour tracé)
                  clef = code compétence
                valeur = liste [True False ...] des indicateurs à mobiliser
        """
        indicateurs = {}
#        print " GetDicIndicateurs", self.id
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
#        print "  ", indicateurs
        return indicateurs
        
        
        
        
    ######################################################################################  
    def GetDicIndicateursRevue(self, revue):
        """ Renvoie un dictionnaire des indicateurs que l'élève doit mobiliser AVANT une revue
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
            elif self.id in t.eleves:
                if revues and t.phase == "Rev":
                    lst.append(t)
                elif t.phase != "Rev":
                    lst.append(t)
            
                    
#        lst = list(set(lst))
            
        return lst
        
    ######################################################################################  
    def GrillesGenerees(self):
        b = True
        for g in self.grille.values():
            b = b and len(g.path) > 0
        return b
    
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            listItems = [[u"Supprimer", 
                          functools.partial(self.GetDocument().SupprimerEleve, item = itemArbre), 
                          images.Icone_suppr_eleve.GetBitmap()]]
            if len(self.GetProjetRef().parties) > 0:
                tg = u"Générer grille"
                to = u"Ouvrir grille"
                if len(self.GetProjetRef().parties) > 1:
                    tg += u"s"
                    to += u"s"
                
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
        t = u"Durée de travail "
        if taux < tol1:
            self.codeBranche.SetBackgroundColour(COUL_OK)
            self.codeBranche.SetToolTipString(t + u"conforme")
        elif taux < tol2:
            self.codeBranche.SetBackgroundColour(COUL_BOF)
            self.codeBranche.SetToolTipString(t + u"acceptable")
        else:
            self.codeBranche.SetBackgroundColour(COUL_NON)
            if duree < dureeRef:
                self.codeBranche.SetToolTipString(t + u"insuffisante")
            else:
                self.codeBranche.SetToolTipString(t + u"trop importante")
        
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
        
        t1 = u"L'élève ne mobilise pas suffisamment de compétences pour être évalué"
        t21 = u"Le "
        t22 = u"Les "
        t3 = u"taux d'indicateurs évalués pour "
        t4 = u" est inférieur à "
        t51 = u"la compétence "
        t52 = u"les compétences "
        
#        for ph, nomph, st in zip(['R', 'S'], [u"conduite", u"soutenance"], [self.evaluR, self.evaluS]):
        for disc in self.GetProjetRef()._dicoGrpIndicateur.keys():
            for ph, nomph in self.GetProjetRef().parties.items():
                st = self.codeBranche.comp[disc+ph]
                t = u"Evaluabilité de la "+nomph+u" du projet "
                tt = u""
                if ev_tot[disc][ph][1]:
                    tt += u"\n" + t1
            
                le = [k for k in ev[disc][ph].keys() if ev[disc][ph][k] == False] # liste des groupes de compétences pas évaluable
                if len(le) == 1:
                    tt += u"\n" + t21 + t3 + t51 + le[0] + t4 + pourCent2(seuil[disc][ph])
                else:
                    tt += u"\n" + t22 + t3 + t52 + " ".join(le) + t4 + pourCent2(seuil[disc][ph])
            
                if ev_tot[disc][ph][1]:
                    coul = COUL_OK
                    t += u"POSSIBLE."
                else:
                    coul = COUL_NON
                    t += u"IMPOSSIBLE :"
                    t += tt
                
                st.SetBackgroundColour(coul)
                st.SetToolTipString(t)

        self.codeBranche.LayoutFit()



    ######################################################################################  
    def SetCode(self):

        t = self.GetNomPrenom()

        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
            
        self.SetTip()


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

        ficheHTML = constantes.BASE_FICHE_HTML_ELEVE
        
        
        t = u""
        for l in ligne:
            t += l+"\n"

        ficheHTML = ficheHTML.replace('{{tableau}}', t)
        
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
        self.titre = u"prof"
        self.code = "Prf"
        self.discipline = "Tec"
        self.referent = False
        
        Personne.__init__(self, doc, ident)
        
        
    ######################################################################################  
    def GetFicheHTML(self, param = None):
        return constantes.BASE_FICHE_HTML_PROF
        
        
    ######################################################################################  
    def SetDiscipline(self, discipline):
        self.discipline = discipline
        self.SetTip()
        self.MiseAJourCodeBranche()
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.GetDocument().app.AfficherMenuContextuel([[u"Supprimer", 
                                                     functools.partial(self.GetDocument().SupprimerProf, item = itemArbre), 
                                                     images.Icone_suppr_prof.GetBitmap()]])
        
    ######################################################################################  
    def MiseAJourCodeBranche(self):
        self.arbre.SetItemBold(self.branche, self.referent)
        self.codeBranche.SetItalic()
#         if self.discipline <> 'Tec':
        self.codeBranche.SetLabel(u" "+constantes.CODE_DISCIPLINES[self.discipline]+u" ")
        self.codeBranche.SetToolTipString(constantes.NOM_DISCIPLINES[self.discipline])
        
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

