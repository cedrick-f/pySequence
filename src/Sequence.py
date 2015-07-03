#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                          ##
##                                  sequence                               ##
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
Sequence.py
Aide à la réalisation de fiches  de séquence pédagogiques
et à la validation de projets
*************
*   STIDD   *
*    SSI    *
*************
Copyright (C) 2011-2015
@author: Cedrick FAURY

"""

import version

####################################################################################
#
#   Import des modules nécessaires
#
####################################################################################

# Outils "système"
import os, sys
import webbrowser
import subprocess

# Gestion des messages d'erreur
import error

#from wx_pysequence import *
import wx_pysequence as GUI

# Pour passer des arguments aux callback
import functools
    
# Pour enregistrer en xml
import xml.etree.ElementTree as ET
Element = type(ET.Element(None))

# des widgets wx évolués "faits maison"
from widgets import Variable, VAR_REEL_POS, VAR_ENTIER_POS, \
                    messageErreur, getNomFichier, rallonge, remplaceCode2LF, pourCent2, \
                    remplaceLF2Code, testRel, dansRectangle, messageInfo, messageWarning, messageYesNo#, chronometrer

# Les constantes partagées
from constantes import calculerEffectifs, revCalculerEffectifs, getSingulierPluriel,\
                        COUL_OK, COUL_NON, COUL_BOF, COUL_BIEN, \
                        toList, COUL_COMPETENCES, COUL_PARTIE, \
                        toFileEncoding, toSystemEncoding, SYSTEM_ENCODING, \
                        TOUTES_REVUES_EVAL, TOUTES_REVUES_EVAL_SOUT, TOUTES_REVUES_SOUT, TOUTES_REVUES, \
                        _S, _Rev, _R1, _R2, _R3
import constantes

# Pour les copier/coller
import pyperclip

import textwrap

# Les constantes partagées
from Referentiel import REFERENTIELS
import Referentiel

from wx.lib.embeddedimage import PyEmbeddedImage

if sys.platform == "win32" :
    # Pour lire les classeurs Excel
    import recup_excel
    
import grilles
import images


from xml.dom.minidom import parseString
import xml.dom

from operator import attrgetter

import draw_cairo_prj, draw_cairo_seq, draw_cairo



        
    
######################################################################################  
def forceID(xml):
    for node in xml.childNodes:
        if hasattr(node, 'hasAttribute'):
            if node.hasAttribute("id"):
                node.setIdAttribute('id')
            if node.hasChildNodes():
                forceID(node)

#####################################################################################
#####################################################################################
def SetWholeText(node, Id, text):
    """ 
    """
    nom = node.getElementById(Id)
    if nom != None:
        
        for txtNode in nom.childNodes:
            if txtNode.nodeType==xml.dom.Node.TEXT_NODE:
                txtNode.replaceWholeText(text)
        
#####################################################################################
def XML_AjouterCol(node, idLigne, text, bcoul = None, fcoul = "black", size = None, bold = False):
    """<td id="rc1" style="background-color: #ff6347;"><font id="r1" size="2">1</font></td>"""
    ligne = node.getElementById(idLigne)
    if ligne != None:
        td = node.createElement("td")
        
        ligne.appendChild(td)
        
        if bcoul != None:
            td.setAttribute("style", "background-color: "+bcoul+";")
        
        if size != None:
            tc = node.createElement("font")
            tc.setAttribute("size", str(size))
#            tc.setAttribute("color", fcoul)
            td.appendChild(tc)
            td = tc
        
        if bold:
            tc = node.createElement("b")
            td.appendChild(tc)
            td = tc
            
        txt = node.createTextNode(text)
        td.appendChild(txt)
        

    
    
    
    
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
        dlg = GUI.URLDialog(None, self, pathseq)
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
          u"Equipe pédagogique"]

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
            self.panelPropriete.sendEvent()
    
    
    ######################################################################################  
    def SetLien(self, lien = None):
        if hasattr(self, 'tip_titrelien'):
            self.tip.SetLien(self.lien, self.tip_titrelien, self.tip_ctrllien)

        if hasattr(self, 'panelPropriete'): 
            self.panelPropriete.MiseAJourLien()
        
        if hasattr(self, 'sousSeances'):
            for sce in self.seances:
                sce.SetLien()
          
            
    ######################################################################################  
    def SetPathSeq(self, pathSeq):
        if hasattr(self, 'panelPropriete'): 
            self.panelPropriete.SetPathSeq(pathSeq)
     
        
    ######################################################################################  
    def AfficherLien(self, pathseq): 
        self.lien.Afficher(pathseq)
        
        
    ######################################################################################  
    def OnPathModified(self):
        if hasattr(self, 'tip_titrelien'):
            self.tip.SetLien(self.lien, self.tip_titrelien, self.tip_ctrllien)
        
        

        
class LienSequence():
    def __init__(self, parent, panelParent, path = ""):
        self.path = path
        self.parent = parent
        self.panelPropriete = GUI.PanelPropriete_LienSequence(panelParent, self)
        self.panelParent = panelParent
        
        #
        # Création du Tip (PopupInfo)
        #
        self.tip = GUI.PopupInfo2(self.parent.app, u"Séquence requise")
        self.tip_titre = self.tip.CreerTexte((1,0))
        self.tip_titrelien, self.tip_ctrllien = self.tip.CreerLien((2,0))
        self.tip_image = self.tip.CreerImage((3,0))
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du lien de sequence pour enregistrement
        """
        root = ET.Element("Sequence")
        root.set("dir", self.path)
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        self.path = branche.get("dir", "")
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = GUI.CodeBranche(self.arbre, u"")
        self.branche = arbre.AppendItem(branche, u"Séquence :", wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Seq"])
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", 
                                                     functools.partial(self.parent.SupprimerSequencePre, item = itemArbre), 
                                                     images.Icone_suppr_seq.GetBitmap()]
                                                    ])
            
    ######################################################################################  
    def SetLabel(self):
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.GetNomFichier())
        
    ######################################################################################  
    def SetImage(self, bmp):
        self.tip.SetImage(bmp, self.tip_image)

    ######################################################################################  
    def SetLien(self):
        self.tip.SetLien(Lien(self.path, 's'), self.tip_titrelien, self.tip_ctrllien)
    
    ######################################################################################  
    def SetTitre(self, titre):
        self.tip.SetTexte(titre, self.tip_titre)
        
    ######################################################################################  
    def GetNomFichier(self):
        return os.path.splitext(os.path.basename(self.path))[0]
     
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
            return self.branche



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
#    def __init__(self):
#        self.elem = None
        
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
    def CopyToClipBoard(self, event = None):
        pyperclip.copy(ET.tostring(self.getBranche()))
        
    
    

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
        if hasattr(self, 'panelPropriete'):
            pp = self.panelPropriete
            if hasattr(pp, 'rtc'):
                return pp.rtc.GetValue()
            
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
        if hasattr(self, 'projet'):
            cl = self.projet.classe
        elif hasattr(self, 'sequence'):
            cl = self.sequence.classe
        elif hasattr(self, 'parent'):
            cl = self.parent.classe
        else:
            cl = self.classe
        return cl
            
    ######################################################################################  
    def GetTypeEnseignement(self, simple = False):
        cl = self.GetClasse()
            
        if simple:
            return cl.familleEnseignement
        
        return cl.typeEnseignement
    
#    ######################################################################################  
#    def GetDocument(self):    
#        return self.projet
    
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
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
            return self.branche
        
        
    ######################################################################################  
    def GetProfondeur(self):
        return 0  
        
        
        

class Classe():
    def __init__(self, app, panelParent = None, intitule = u"", 
                 pourProjet = False, ouverture = False, typedoc = ''):
        self.intitule = intitule
        
        self.academie = u""
        self.ville = u""
        self.etablissement = u""
        self.effectifs = {}
        self.nbrGroupes = {}
        self.systemes = []
        
        self.app = app
        self.panelParent = panelParent
        
        self.Initialise(pourProjet)
        
        
        if panelParent:
            self.panelPropriete = GUI.PanelPropriete_Classe(panelParent, self, pourProjet, 
                                                        ouverture = ouverture, typedoc = typedoc)
            self.panelPropriete.MiseAJour()
            
        

        
    ######################################################################################  
    def __repr__(self):
        return "Classe :"#, self.typeEnseignement
    
    ######################################################################################  
    def GetPath(self):
        return r""
    
    ######################################################################################  
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'codeBranche'):
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
        
        if defaut or self.app.options.optClasse["FichierClasse"] == r"":
            self.setDefaut()
            
        else:
            if not self.ouvrir(self.app.options.optClasse["FichierClasse"]):
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
        
        self.MiseAJour()


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
            
#        if not self.referentiel.CI_BO and hasattr(self, 'CI'): 
#            ci = ET.SubElement(classe, "CentreInteret")
#            for i,c in enumerate(self.CI):
#                ci.set("CI"+str(i+1), c)
#                if self.referentiel.CI_cible:
#                    ci.set("pos"+str(i+1), self.posCI[i])
                
                
#        if self.typeEnseignement == 'ET':
#            ci = ET.SubElement(classe, "CentreInteret")
#            for i,c in enumerate(self.ci_ET):
#                ci.set("CI"+str(i+1), c)
#                ci.set("pos"+str(i+1), self.posCI_ET[i])
#        
#        elif self.typeEnseignement == 'SSI':
#            ci = ET.SubElement(classe, "CentreInteret")
#            if hasattr(self, 'ci_SSI'):
#                for i,c in enumerate(self.ci_SSI):
#                    ci.set("CI"+str(i+1), c)
        
        return classe
    
    ######################################################################################  
    def setBranche(self, branche, reparer = False):
        err = []
        print "setBranche classe"
        self.typeEnseignement = branche.get("Type", constantes.TYPE_ENSEIGNEMENT_DEFAUT)
        
        self.version = branche.get("Version", "0")       # A partir de la version 6 !
        
        #
        # Référentiel
        #
        def ChargerRefOriginal():
            print "Réparation = pas référentiel intégré !"
            if self.GetVersionNum() >= 5:
                code = self.referentiel.setBrancheCodeV5(brancheRef)
                print "   Code trouvé dans référentiel :", code
                if code != self.typeEnseignement:
                    self.typeEnseignement = code
                    
            print "   TypeEnseignement :", self.typeEnseignement
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
                if self.GetVersionNum() == 5:
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
                systeme = Systeme(self, self.panelParent)
                systeme.setBranche(sy)
                self.systemes.append(systeme)    
            self.systemes.sort(key=attrgetter('nom'))
            
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()
            
        return err
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = GUI.CodeBranche(self.arbre, rallonge(self.GetReferentiel().Enseignement[0]))
        self.branche = arbre.AppendItem(branche, Titres[5]+" :", wnd = self.codeBranche, data = self)#, image = self.arbre.images["Seq"])
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
    
    

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
    def GetVersionNum(self):
        return int(self.version.split(".")[0].split("beta")[0])
    
    
    ######################################################################################  
    def Verrouiller(self, etat):
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.Verrouiller(etat)
        if etat:
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
    def __init__(self, app, classe = None, panelParent = None, intitule = ""):
        self.intitule = intitule
        self.classe = classe
        self.app = app
        self.centrer = True
        
        self.position = 0
        
        self.commentaires = u""
        
        self.panelParent = panelParent
          
    ######################################################################################  
    def GetApp(self):
        return self.app
    
    ######################################################################################  
    def GetPath(self):
        if hasattr(self.app, 'fichierCourant'):
            return os.path.split(toFileEncoding(self.app.fichierCourant))[0]
        else:
            return r""
    
    ######################################################################################  
    def GetApercu(self, mult = 3):
        imagesurface = self.draw.get_apercu(self, mult)
#        imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  210*mult, 297*mult)#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
#        ctx = cairo.Context(imagesurface)
#        ctx.scale(297*mult, 297*mult) 
#        self.draw.Draw(ctx, self)
        bmp = GUI.getBitmapFromImageSurface(imagesurface)
        return bmp
    
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

        
####################################################################################################          
class Sequence(BaseDoc, Objet_sequence):
    def __init__(self, app, classe = None, panelParent = None, intitule = u"Intitulé de la séquence pédagogique"):
        BaseDoc.__init__(self, app, classe, panelParent, intitule)
        
        if panelParent:
            self.panelPropriete = GUI.PanelPropriete_Sequence(panelParent, self)
            self.panelSeances = GUI.PanelPropriete_Racine(panelParent, constantes.TxtRacineSeance)
            self.panelObjectifs = GUI.PanelPropriete_Racine(panelParent, constantes.TxtRacineObjectif)
            self.panelSystemes = GUI.PanelPropriete_Racine(panelParent, constantes.TxtRacineSysteme)
        
        self.prerequis = Savoirs(self, panelParent, prerequis = True)
        self.prerequisSeance = []
        
        self.pasVerouille = True
        
        self.CI = CentreInteret(self, panelParent)
        
        self.obj = {"C" : Competences(self, panelParent),
                    "S" : Savoirs(self, panelParent)}
        self.systemes = []
        self.seances = [Seance(self, panelParent)]
        
#        self.options = classe.options
        
        # Le module de dessin
        self.draw = draw_cairo_seq
        
        
    ######################################################################################  
    def __repr__(self):
        return self.intitule
#        t = u"Séquence :"+ + "\n"
#        t += "   " + self.CI.__repr__() + "\n"
#        for c in self.obj.values():
#            t += "   " + c.__repr__() + "\n"
#        for s in self.seances:
#            t += "   " + s.__repr__() + "\n"
#        return t

    ######################################################################################  
    def GetType(self):
        return 'seq'
    
    
    ######################################################################################  
    def Initialise(self):
        self.AjouterListeSystemes(self.classe.systemes)
#        self.AjouterListeSystemes(self.options.optSystemes["Systemes"])
            
            
    ######################################################################################  
    def SetPath(self, fichierCourant):
        pathseq = toFileEncoding(os.path.split(fichierCourant)[0])
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

        sequence.set("Position", str(self.position))

        sequence.append(self.CI.getBranche())
        
        prerequis = ET.SubElement(sequence, "Prerequis")
        prerequis.append(self.prerequis.getBranche())
        for ps in self.prerequisSeance:
            prerequis.append(ps.getBranche())
        
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
        self.intitule = branche.get("Intitule", u"")
        
        self.commentaires = branche.get("Commentaires", u"")
        
        self.position = eval(branche.get("Position", "0"))

        brancheCI = branche.find("CentresInteret")
        if brancheCI != None:
            self.CI.setBranche(brancheCI)
        
        # Pour rétro compatibilité
        if self.CI.numCI == []:
            brancheCI = branche.find("CentreInteret")
            if brancheCI != None:
                self.CI.setBranche(brancheCI)
            
        
        branchePre = branche.find("Prerequis")
        if branchePre != None:
            savoirs = branchePre.find("Savoirs")
            self.prerequis.setBranche(savoirs)
            lst = list(branchePre)
            lst.remove(savoirs)
            self.prerequisSeance = []
            if hasattr(self, 'panelPropriete'):
                for bsp in lst:
                    sp = LienSequence(self, self.panelParent)
                    sp.setBranche(bsp)
                    self.prerequisSeance.append(sp)
        
        
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
            systeme = Systeme(self, self.panelParent)
            systeme.setBranche(sy)
            self.systemes.append(systeme)    

        brancheSce = branche.find("Seances")
        self.seances = []
        for sce in list(brancheSce):         
            seance = Seance(self, self.panelParent)
            seance.setBranche(sce)
            self.seances.append(seance)
        self.OrdonnerSeances()
        
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()

        
    
        
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
        print "CollerElem 1ere pos"
        
        if bseance == None:
            bseance = GetObjectFromClipBoard('Seance')
            if bseance == None:
                return
        
        typeSeance = bseance.get("Type", "")
        
        seance = Seance(self, self.panelParent, typeSeance = typeSeance,
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
            
        seance.panelPropriete.MiseAJour()
        seance.panelPropriete.MiseAJourListeSystemes()
        
        self.panelPropriete.sendEvent()
        
        self.arbre.SelectItem(seance.branche)    


    ######################################################################################  
    def AjouterSeance(self, event = None):
        seance = Seance(self, self.panelParent)
        self.seances.append(seance)
        self.OrdonnerSeances()
        seance.ConstruireArbre(self.arbre, self.brancheSce)
        self.panelPropriete.sendEvent()
        
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
            self.panelPropriete.sendEvent()
            return True
        return False
    
    
    ######################################################################################  
    def OrdonnerSeances(self):
#        print "OrdonnerSeances"
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
            self.SupprimerSequencePre(item = item)           
        
    
    ######################################################################################  
    def SupprimerSequencePre(self, event = None, item = None):
        ps = self.arbre.GetItemPyData(item)
        self.prerequisSeance.remove(ps)
        self.arbre.Delete(item)
        self.panelPropriete.sendEvent()
        
    ######################################################################################  
    def AjouterSequencePre(self, event = None):
        ps = LienSequence(self, self.panelParent)
        self.prerequisSeance.append(ps)
        ps.ConstruireArbre(self.arbre, self.branchePre)
        self.panelPropriete.sendEvent()
        self.arbre.SelectItem(ps.branche)
        
        
    ######################################################################################  
    def AjouterSysteme(self, event = None):
        sy = Systeme(self, self.panelParent)
        self.systemes.append(sy)
        sy.ConstruireArbre(self.arbre, self.brancheSys)
        self.arbre.Expand(self.brancheSys)
        self.panelPropriete.sendEvent()
        self.arbre.SelectItem(sy.branche)
        self.AjouterSystemeSeance()
        return
    
    ######################################################################################  
    def AjouterListeSystemes(self, syst = []):
#        print "AjouterListeSystemes séquence"
        nouvListe = []
        for s in syst:
#            print "   ",s
            
            if not isinstance(s, Systeme):
                sy = Systeme(self, self.panelParent)
                sy.setBranche(ET.fromstring(s))
            else:
                sy = s.Copie(self, self.panelParent)
                sy.lienClasse = s
                sy.panelPropriete.Verrouiller(False)
                sy.panelPropriete.cbListSys.SetSelection(sy.panelPropriete.cbListSys.FindString(s.nom))
#            try:
#                sy.setBranche(ET.fromstring(s))
#            except:
#                print "Erreur parsing :", s
#                continue
            
#            nom = unicode(s)
#            sy = Systeme(self, self.panelParent, nom = nom)
            
            self.systemes.append(sy)
            nouvListe.append(sy.nom)
            sy.ConstruireArbre(self.arbre, self.brancheSys)
            sy.SetCode()
#            sy.nbrDispo.v[0] = eval(n)
            sy.panelPropriete.MiseAJour()
        
        self.arbre.Expand(self.brancheSys)
        self.AjouterListeSystemesSeance(nouvListe)
        self.panelPropriete.sendEvent()
        return
    
    ######################################################################################  
    def SupprimerSysteme(self, event = None, item = None):
        sy = self.arbre.GetItemPyData(item)
        i = self.systemes.index(sy)
        self.systemes.remove(sy)
        self.arbre.Delete(item)
        self.SupprimerSystemeSeance(i)
        self.panelPropriete.sendEvent()
    
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
                                         GUI.ICON_INFORMATION | GUI.CANCEL
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
    def AjouterRotation(self, seance):
        seanceR1 = Seance(self.panelParent)
        seance.seances.append(seanceR1)
        return seanceR1
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, Titres[0], data = self, image = self.arbre.images["Seq"])
        self.arbre.SetItemBold(self.branche)
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
        
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
        for ps in self.prerequisSeance:
            ps.ConstruireArbre(arbre, self.branchePre)
        #
        # Les objectifs
        #
        self.brancheObj = arbre.AppendItem(self.branche, Titres[2], image = self.arbre.images["Obj"], data = self.panelObjectifs)
        for obj in self.obj.values():
            obj.ConstruireArbre(arbre, self.brancheObj)
            
        
        self.brancheSce = arbre.AppendItem(self.branche, Titres[3], image = self.arbre.images["Sea"], data = self.panelSeances)
        self.arbre.SetItemBold(self.brancheSce)
        for sce in self.seances:
            sce.ConstruireArbre(arbre, self.brancheSce) 
            
        self.brancheSys = arbre.AppendItem(self.branche, Titres[4], image = self.arbre.images["Sys"], data = self.panelSystemes)
        for sy in self.systemes:
            sy.ConstruireArbre(arbre, self.brancheSys)    
        
        
        
    ######################################################################################  
    def reconstruireBrancheSeances(self, b1, b2):
        self.arbre.DeleteChildren(self.brancheSce)
        for sce in self.seances:
            sce.ConstruireArbre(self.arbre, self.brancheSce) 
        self.arbre.Expand(b1.branche)
        self.arbre.Expand(b2.branche)
#        
    
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):    
        """ Affiche le menu contextuel associé é la séquence
            ... ou bien celui de itemArbre concerné ...
        """
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([[u"Enregistrer", self.app.commandeEnregistrer, 
                                              GUI.getIconeFileSave()],
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
                                                       GUI.getIconePaste()])
            
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
    def HitTest(self, x, y):     
        if self.CI.HitTest(x, y):
            return self.CI.HitTest(x, y)

        elif dansRectangle(x, y, (draw_cairo_seq.posPre + draw_cairo_seq.taillePre,))[0]:
            for ls in self.prerequisSeance:
                h = ls.HitTest(x,y)
                if h != None:
                    return h
            return self.branchePre
        
        else:
            branche = None
            autresZones = self.seances + self.systemes + self.obj.values()
            continuer = True
            i = 0
            while continuer:
                if i >= len(autresZones):
                    continuer = False
                else:
                    branche = autresZones[i].HitTest(x, y)
                    if branche:
                        continuer = False
                i += 1
            
            if branche == None:
                if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
                    return self.branche
                
            return branche
        
    ######################################################################################  
    def HitTestPosition(self, x, y):
        if hasattr(self, 'rectPos'):
            for i, rectPos in enumerate(self.rectPos):
                if dansRectangle(x, y, (rectPos,))[0]:
                    return i
                    
                                    
                                    
    #############################################################################
    def MiseAJourTypeEnseignement(self, ancienRef = False, ancienneFam = False):
        self.app.SetTitre()
        self.classe.MiseAJourTypeEnseignement()
        self.CI.MiseAJourTypeEnseignement()
        self.obj['C'].MiseAJourTypeEnseignement()
        for o in self.obj.values():
            o.MiseAJourTypeEnseignement()
        self.prerequis.MiseAJourTypeEnseignement()
        for s in self.seances:
            s.MiseAJourTypeEnseignement()
        self.panelPropriete.MiseAJour()
        
        
    #############################################################################
    def Verrouiller(self):
        if hasattr(self, 'CI') \
            and (self.CI.numCI != [] or self.prerequis.savoirs != [] \
                 or self.obj['C'].competences != [] or self.obj['S'].savoirs != []):
            self.classe.Verrouiller(False)
        else:
            if self.classe != None:
                self.classe.Verrouiller(True)




####################################################################################################
#
#        Projet
#
####################################################################################################
class Projet(BaseDoc, Objet_sequence):
    def __init__(self, app, classe = None, panelParent = None, intitule = u""):
        BaseDoc.__init__(self, app, classe, panelParent, intitule)
#        Objet_sequence.__init__(self)
        
        self.version = "" # version de pySéquence avec laquelle le fichier a été sauvegardé
        
        # code désignant le type de projet
#        print "init Projet"
#        print "   ", self.GetReferentiel()
        self.code = self.GetReferentiel().getCodeProjetDefaut()
#        print "   ", self.code
        self.position = self.GetProjetRef().getPeriodeEval()
#        print "   ", self.position
        self.nbrParties = 1
        
        # Organisation des revues du projet
        self.initRevues()

        # Année Scolaire
        self.annee = constantes.getAnneeScolaire()
        
        self.pasVerouille = True
        
        # Par défaut, la revue 1 est après la Conception détaillée
#        self.R1apresConception = False
        
        if panelParent:
            self.panelPropriete = GUI.PanelPropriete_Projet(panelParent, self)
            self.panelEleves = GUI.PanelPropriete_Racine(panelParent, constantes.TxtRacineEleve)
            self.panelTaches = GUI.PanelPropriete_Racine(panelParent, constantes.TxtRacineTache)
            self.panelEquipe = GUI.PanelPropriete_Racine(panelParent, constantes.TxtRacineEquipe)
        
        self.eleves = []
        
        self.taches = self.creerTachesRevue()
            
        self.equipe = []
        
        self.support = Support(self, panelParent)
        
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
        
        
        self.SetPosition(self.position, first = True)
        
        # Le module de dessin
        self.draw = draw_cairo_prj
        
#       
        
        
    ######################################################################################  
    def __repr__(self):
        return self.intitule


    ######################################################################################  
    def GetType(self):
        return 'prj'


    ######################################################################################  
    def GetProjetRef(self):
        """ Renvoie le projet (Referentiel.Projet) de référence
        """
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
            lst.append(Tache(self, self.panelParent, 
                             intitule = self.GetProjetRef().phases[p][1], 
                             phaseTache = p, duree = 0))
        return lst
    
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
            for ph, nomph in self.GetProjetRef().parties.items():
                t += nomph + pourCent2(ev_tot[ph][0], True)+"\n"
            
#            t += u"\tconduite : "+pourCent2(ev_tot['R'][0], True)+"\n"
#            t += u"\tsoutenance : "+pourCent2(ev_tot['S'][0], True)+"\n"
            return t.encode(SYSTEM_ENCODING)
            
            
            
    ######################################################################################  
    def GetCode(self, i = None):
        return u"Projet"
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du projet pour enregistrement
        """
        # Création de la racine
        projet = ET.Element("Projet")
        
        projet.set("Version", version.__version__) # à partir de la version 5.7
        
        projet.set("Intitule", self.intitule)
        
        projet.set("Problematique", remplaceLF2Code(self.problematique))
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
#        print "setBranche projet"
#        print self.GetReferentiel()
        
        err = []
        
        self.intitule = branche.get("Intitule", u"")
        
        self.version = branche.get("Version", "")       # A partir de la version 5.7 !

        self.problematique = remplaceCode2LF(branche.get("Problematique", u""))
        
        self.commentaires = branche.get("Commentaires", u"")
        
        self.nbrRevues = eval(branche.get("NbrRevues", str(self.GetProjetRef().getNbrRevuesDefaut())))
        if not self.nbrRevues in self.GetProjetRef().posRevues.keys():
            self.nbrRevues = self.GetProjetRef().getNbrRevuesDefaut()
        self.positionRevues = branche.get("PosRevues", 
                                          '-'.join(list(self.GetProjetRef().posRevues[self.nbrRevues]))).split('-')

        if self.nbrRevues == 3:
            self.MiseAJourNbrRevues()
        
        self.MiseAJourTypeEnseignement()
        
        self.position = eval(branche.get("Position", "0"))
        if self.version == "": # Enregistré avec une version de pySequence > 5.7
            if self.position == 5:
#                print "Correction position"
                self.position = self.GetProjetRef().getPeriodeEval()
            
            
        self.annee = eval(branche.get("Annee", str(constantes.getAnneeScolaire())))

        brancheEqu = branche.find("Equipe")
        self.equipe = []
        for e in list(brancheEqu):
            prof = Prof(self, self.panelParent)
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
            eleve = Eleve(self, self.panelParent)
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
                tache = Tache(self, self.panelParent, branche = e)
                if tache.code < 0 : # ça s'est mal passé lors du setbranche ...
                    err.append(constantes.Erreur(constantes.ERR_PRJ_TACHES, tache.code))
                    return err
                    
#                tache.setBranche(e)
                self.taches.append(tache)
#        self.CorrigerIndicateursEleve()
        
        # Pour récupérer les prj créés avec la version beta1
        if adapterVersion:
            self.taches.extend(tachesRevue)
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()

        return err
        
    ######################################################################################  
    def GetLastPosition(self):
        n = 0
        for p in self.GetReferentiel().periodes:
            n+=p[1]
        n = n - (self.GetProjetRef().periode[-1] - self.GetProjetRef().periode[0])
        return n-1
    
    
    
    ######################################################################################  
    def SetPosition(self, pos, first = False):
#        print "SetPosition", pos
#        print "  position actuelle :", self.position
#        posEpreuve = self.GetProjetRef().getPeriodeEval()
        kproj = self.GetReferentiel().getProjetEval(pos+1)
#        print "   ", kproj
#        print "  posEpreuve", posEpreuve
    

        ###################################################################
        # on efface toutes les revues
        def effacerRevues():
            lst = []
            for t in self.taches:
                if t.phase in TOUTES_REVUES_EVAL_SOUT:
                    lst.append(t.branche)
            for a in reversed(lst):
                self.SupprimerTache(item = a, verrouiller = False)
        
        
        
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
                    if hasattr(tr, 'panelPropriete'):
                        tr.panelPropriete.MiseAJour()
                self.OrdonnerTaches()
                self.arbre.Ordonner(self.brancheTac)
                if hasattr(self, 'panelPropriete'):
                    self.panelPropriete.sendEvent()
    

                
            
            
        # Sinon on se contente de redessiner
        else:
            if hasattr(self, 'panelPropriete') and not first:
                self.panelPropriete.sendEvent()
        
        
        
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
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()


    ######################################################################################  
    def SetProblematique(self, pb):
        self.problematique = pb


    ######################################################################################  
    def SetReferent(self, personne, referent):
        for p in self.equipe:
            if p == personne:
                p.referent = referent
            else:
                if referent:
                    p.referent = False
            p.panelPropriete.MiseAJour()
        self.MiseAJourNomProfs()
        
        
        
    ######################################################################################  
    def SetCodes(self):
        self.support.SetCode()
        
        for sce in self.taches:
            sce.SetCode()    
            
        for sy in self.eleves:
            sy.SetCode()    

            
    ######################################################################################  
    def PubDescription(self):
        self.support.PubDescription()   
        for t in self.taches:
            t.PubDescription()       
         
            
    ######################################################################################  
    def SetLiens(self):
#        for t in self.taches:
#            t.SetLien()    

        self.support.SetLien()  

        
    ######################################################################################  
    def VerifPb(self):
        return

        
    ######################################################################################  
    def MiseAJourNomsEleves(self):
        """ Met à jour les noms des élèves après une modification
            dans les panelPropriété des tâches
        """
        for t in self.taches:
            t.MiseAJourNomsEleves()
        
        
    ######################################################################################  
    def MiseAJourDureeEleves(self):
        for e in self.eleves:
            e.SetCode()
            e.MiseAJourCodeBranche()
    
    
    ######################################################################################  
    def MiseAJourNomProfs(self):
        for e in self.equipe:
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
            tache = Tache(self, self.panelParent, 
                          intitule = self.GetProjetRef().phases[_R3][1], 
                          phaseTache = _R3, duree = 0)
            self.taches.append(tache)
            tache.ConstruireArbre(self.arbre, self.brancheTac)
            tache.SetPhase()
            
            revue2 = self.getTachesRevue()[1]
            revue2.panelPropriete = GUI.PanelPropriete_Tache(self.panelParent, revue2, revue = True)
            
            
        elif self.nbrRevues == 2 and _R3 in lstPhasesTaches:
            t = self.getTachesRevue()[2]
            self.SupprimerTache(item = t.branche)
            revue2 = self.getTachesRevue()[1]
            revue2.panelPropriete = GUI.PanelPropriete_Tache(self.panelParent, revue2, revue = True)
        return


    ######################################################################################  
    def AjouterTache(self, event = None, tacheAct = None):
        """ Ajoute une tâche au projet
            et la place juste après la tâche tacheAct (si précisé)
        """
        if tacheAct == None or tacheAct.phase == "S" or tacheAct.phase == "":
            tache = Tache(self, self.panelParent)
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

            tache = Tache(self, self.panelParent, phaseTache = phase)
            self.taches.append(tache)
            tache.ordre = tacheAct.ordre+0.5 # truc pour le tri ...
            tache.ConstruireArbre(self.arbre, self.brancheTac)
            
            tache.SetPhase()
            if hasattr(tache, 'panelPropriete'):
                tache.panelPropriete.MiseAJour()
        
        self.Verrouiller()

        self.arbre.EnsureVisible(tache.branche)
        for i in self.arbre._itemWithWindow:
            self.arbre.HideWindows()
        self.arbre.SelectItem(tache.branche)

        self.panelPropriete.sendEvent()

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
        tache_avant = self.arbre.GetItemPyData(item)
        if not isinstance(tache_avant, Tache):
            return
        
        if btache == None:
            btache = GetObjectFromClipBoard("Tache")
            if btache == None:
                return
        
        phase = btache.get("Phase", "")
        if tache_avant.phase != phase and tache_avant.GetSuivante().phase != phase : # la phase est la même
            return
#
#         or tache_avant.phase != btache.get("Phase", ""): # la phase est la même
#            return
        
        tache = Tache(self, self.panelParent, phaseTache = "", branche = btache)
        
        tache.ordre = tache_avant.ordre+1
        for t in self.taches[tache_avant.ordre:]:
            t.ordre += 1
        self.taches.insert(tache_avant.ordre, tache)
#        self.taches.sort(key=attrgetter('ordre'))
        for t in self.taches[tache_avant.ordre:]:
            t.SetCode()

            
        tache.ConstruireArbre(self.arbre, self.brancheTac)
        tache.SetCode()
        if hasattr(tache, 'panelPropriete'):
            tache.panelPropriete.MiseAJour()
            tache.panelPropriete.MiseAJourEleves()
        
        self.arbre.Ordonner(self.brancheTac)
        self.panelPropriete.sendEvent()
        self.arbre.SelectItem(tache.branche)
            
        self.Verrouiller()
#        print "Tache", tache, u"collée"
        
    ######################################################################################  
    def InsererRevue(self, event = None, item = None):
        tache_avant = self.arbre.GetItemPyData(item)
        tache = Tache(self, self.panelParent, phaseTache = "Rev")
        tache.ordre = tache_avant.ordre+1
        for t in self.taches[tache_avant.ordre:]:
            t.ordre += 1
        self.taches.append(tache)
        self.taches.sort(key=attrgetter('ordre'))
        
        tache.ConstruireArbre(self.arbre, self.brancheTac)
        tache.SetCode()
        if hasattr(tache, 'panelPropriete'):
            tache.panelPropriete.MiseAJour()
        
        self.arbre.Ordonner(self.brancheTac)
        self.panelPropriete.sendEvent()
        self.arbre.SelectItem(tache.branche)
            
        self.Verrouiller()
        
    ######################################################################################  
    def SupprimerTache(self, event = None, item = None, verrouiller = True):
        tache = self.arbre.GetItemPyData(item)
        self.taches.remove(tache)
        self.arbre.Delete(item)
        self.SetOrdresTaches()
        self.panelPropriete.sendEvent()
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
            
#        print paquet
        
        # On trie les tâches de chaque paquet  
        for c in [k for k in prj.listPhases if not k in prj.listPhasesEval]:#['Ana', 'Con', 'Rea', 'DCo', 'Val', 'XXX']:
            paquet[c].sort(key=attrgetter('ordre'))

        #
        # On assemble les paquets
        #
        lst = []
        for p in self.GetListePhases()+["S"]:
            lst.extend(paquet[p]) 

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
        self.taches = self.OrdonnerListeTaches(self.taches)
        
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
#            self.SupprimerSequencePre(item = item)           
        
    
#    ######################################################################################  
#    def SupprimerSequencePre(self, event = None, item = None):
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
        if len(self.eleves) < 5:
            e = Eleve(self, self.panelParent, self.GetNewIdEleve())
            self.eleves.append(e)
            self.OrdonnerEleves()
            e.ConstruireArbre(self.arbre, self.brancheElv)
            self.arbre.Expand(self.brancheElv)
            self.panelPropriete.sendEvent()
            self.arbre.SelectItem(e.branche)
            self.AjouterEleveDansPanelTache()

        

    
    ######################################################################################  
    def SupprimerEleve(self, event = None, item = None):
#        print "SupprimerEleve",
        e = self.arbre.GetItemPyData(item)
        i = self.eleves.index(e)
        self.eleves.remove(e)
        self.OrdonnerEleves()
        
        self.arbre.Delete(item)
        self.SupprimerEleveDansPanelTache(i)
        
        # On fait ça car supprimer un élève a un impact sur les noms des éleves "sans nom"
        for i, e in enumerate(self.eleves):
            e.SetCode()
            
        self.panelPropriete.sendEvent()
    
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
    def AjouterProf(self, event = None):
        if len(self.equipe) < 5:
            e = Prof(self, self.panelParent, len(self.equipe))
            self.equipe.append(e)
            e.ConstruireArbre(self.arbre, self.branchePrf)
            self.arbre.Expand(self.branchePrf)
            self.panelPropriete.sendEvent()
            self.arbre.SelectItem(e.branche)

    
    ######################################################################################  
    def SupprimerProf(self, event = None, item = None):
        e = self.arbre.GetItemPyData(item)
#        i = self.equipe.index(e)
        self.equipe.remove(e)
        self.arbre.Delete(item)
        self.panelPropriete.sendEvent()
        
    
    ######################################################################################  
    def MiseAJourPoidsCompetences(self, code = None):
        for t in self.taches:
            t.MiseAJourPoidsCompetences(code)
        self.MiseAJourDureeEleves()
    
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.branche = arbre.AppendItem(branche, Titres[9], data = self, image = self.arbre.images["Prj"])
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
            
        #
        # Le support
        #
        
        self.support.ConstruireArbre(arbre, self.branche)
        #
        # Les profs
        #
        self.branchePrf = arbre.AppendItem(self.branche, Titres[10], data = self.panelEquipe)
        for e in self.equipe:
            e.ConstruireArbre(arbre, self.branchePrf) 
        
        #
        # Les élèves
        #
        self.brancheElv = arbre.AppendItem(self.branche, Titres[6], data = self.panelEleves)
        for e in self.eleves:
            e.ConstruireArbre(arbre, self.brancheElv) 
            
        #
        # Les tâches
        #
        self.brancheTac = arbre.AppendItem(self.branche, Titres[8], data = self.panelTaches)
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
                                              GUI.getIconeFileSave()],
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
            self.app.AfficherMenuContextuel([[u"Ajouter une tâche", self.AjouterTache, images.Icone_ajout_tache.GetBitmap()]])
         
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
    def GetNbrPhases(self):
        """ Renvoie le nombre de phases dans le projet
            (les revues intermédiaires coupent parfois une phase en deux !)
            (pour tracé fiche)
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
#        print "  ", self.nbrRevues,
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
        
    ######################################################################################  
    def HitTest(self, x, y):
        branche = None
        autresZones = self.taches + self.eleves+ self.equipe + [self.support]
        continuer = True
        i = 0
        while continuer:
            if i >= len(autresZones):
                continuer = False
            else:
                branche = autresZones[i].HitTest(x, y)
                if branche:
                    continuer = False
            i += 1
        
        if branche == None:
            if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
                return self.branche

        return branche
        
    ######################################################################################  
    def HitTestCompetence(self, x, y):
        if hasattr(self, 'rectComp'):
            for k, ro in self.rectComp.items():
                rect = [r[:-1] for r in ro]
                obj = [o[-1] for o in ro]
                ok, i = dansRectangle(x, y, rect)
                if ok:
                    return k, obj[i]


    ######################################################################################  
    def HitTestPosition(self, x, y):
        if hasattr(self, 'rectPos'):
            for i, rectPos in enumerate(self.rectPos):
                if dansRectangle(x, y, (rectPos,))[0]:
                    return i


    #############################################################################
    def MiseAJourTypeEnseignement(self, ancienRef = None, ancienneFam = None):#, changeFamille = False):
#        print "MiseAJourTypeEnseignement projet", ancienRef, ">>", self.GetReferentiel()
        
        self.app.SetTitre()
        
        self.code = self.GetReferentiel().getCodeProjetDefaut()
#        print "   ", self.code

        if ancienRef != None:
#            print "   anciennePos", self.position
            anciennePos = self.position
            
            kprj = ancienRef.getProjetEval(anciennePos+1)
#            print "   ancien prj", kprj, self.GetReferentiel().projets.keys()
            if kprj in self.GetReferentiel().projets.keys():
                self.code = kprj
                self.position = self.GetProjetRef().getPeriodeEval()
            else:
                posRel = 1.0*anciennePos/ancienRef.getNbrPeriodes()
                self.position = round(self.GetReferentiel().getNbrPeriodes()*posRel)-1
                self.code = self.GetReferentiel().getProjetEval(self.position+1)
            
        else:
            self.position = self.GetProjetRef().getPeriodeEval()
            
        
        for t in self.taches:
            if t.phase in TOUTES_REVUES_EVAL and self.GetReferentiel().compImposees['C']:
                t.panelPropriete.Destroy()
                t.panelPropriete = GUI.PanelPropriete_Tache(t.panelParent, t)
            t.MiseAJourTypeEnseignement(self.classe.referentiel)
        
        for e in self.eleves:
            e.MiseAJourTypeEnseignement()
        
            
#        print "   ", self.position
#            if ancienRef.estPeriodeEval(anciennePos):
#                self.position = self.GetProjetRef().getPeriodeEval()
##                print "   new pos eval =", self.position
#            else:
#                posRel = 1.0*anciennePos/ancienRef.getNbrPeriodes()
#                self.position = round(self.GetProjetRef().getNbrPeriodes()*posRel)-1
##                print "   new pos =", self.position
        
        
        
        if hasattr(self, 'panelPropriete'):
#            if ancienneFam != self.classe.familleEnseignement:
            self.initRevues()
            self.MiseAJourNbrRevues()
            
            self.panelPropriete.MiseAJourTypeEnseignement()
        
#        self.SetPosition(self.position)




    #############################################################################
    def initRevues(self):
#        print "initRevues",
        self.nbrRevues = self.GetReferentiel().getNbrRevuesDefaut(self.code)
        self.positionRevues = list(self.GetReferentiel().getPosRevuesDefaut(self.code))
#        print self.nbrRevues, self.positionRevues
        

    #############################################################################
    def Verrouiller(self):
        self.pasVerouille = len(self.GetCompetencesUtil()) == 0 and len(self.taches) == self.nbrRevues+1
        self.classe.Verrouiller(self.pasVerouille)
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.Verrouiller(self.pasVerouille)
        
#    #############################################################################
#    def CorrigerIndicateursEleve(self):
#        """
#        """
#        return
#        if self.nbrRevues == 2:
#            lstR = [_R1]
#        else:
#            lstR = [_R1, _R2]
#        for t in self.taches:
#            if t.phase in lstR:
#                for i, e in enumerate(self.eleves):
#                    pass
        
    
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
            
            
                                            
            return messageYesNo(self.GetApp(), m, 
                                      u"Fichier existant", GUI.ICON_WARNING)
            
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


    #############################################################################
    def MiseAJourTachesEleves(self):
        """ Mise à jour des phases de revue 
            pour lesquelles il y a des compétences à cocher
        """
        for t in self.taches:
            if t.phase in [_R1, "Rev"] or (t.phase == _R2 and self.nbrRevues == 3):
                if hasattr(t.panelPropriete, 'arbre'):
                    t.panelPropriete.arbre.MiseAJourTypeEnseignement(t.GetReferentiel())
                    t.panelPropriete.MiseAJour()

    
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
                                        
                                        if self.GetReferentiel().compImposees['C']:
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
    
                    if neleve == 0:
                        if t.phase in [_R1, "Rev"] or (t.phase == _R2 and self.nbrRevues == 3):
                            ti = []
                            for i in t.indicateursEleve[neleve]:
                                if i in t.indicateursMaxiEleve[neleve]:
                                    ti.append(i)
                            t.indicateursEleve[neleve] = ti
                            if miseAJourPanel and hasattr(t.panelPropriete, 'arbre'):
                                t.panelPropriete.arbre.MiseAJourTypeEnseignement(t.GetReferentiel())
                                t.panelPropriete.MiseAJour()
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

            t.ActualiserDicIndicateurs()


#                        
                
####################################################################################
#
#   Classe définissant les propriétés d'une séquence
#
####################################################################################
class CentreInteret(Objet_sequence):
    def __init__(self, parent, panelParent, numCI = []):
#        Objet_sequence.__init__(self)
        self.parent = parent
        self.numCI = []
        self.poids = []
        self.SetNum(self.numCI)
        self.max2CI = True
        
        
        if panelParent:
            self.panelPropriete = GUI.PanelPropriete_CI(panelParent, self)
        
       
        
        
    ######################################################################################  
    def __repr__(self):
        print self.numCI
        return ""
    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du centre d'intérét pour enregistrement
        """
        root = ET.Element("CentresInteret")
        for i, num in enumerate(self.numCI):
            root.set("C"+str(i), str(num))
            root.set("P"+str(i), str(self.poids[i]))
        return root
    
        if hasattr(self, 'code'):
            if self.code == "":
                self.code = "_"
            root = ET.Element(self.code)
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
                    num = eval(code[2:])-1
                    self.AddNum(num)
        
        
#        print self.numCI
#        print self.poids
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()
        return
            
#        code = list(branche)[0].tag
#        if code == "_":
#            num = []
#            self.SetNum(num)
#        else:
#            num = eval(code[2:])-1
#            self.SetNum(num)
#            if hasattr(self, 'panelPropriete'):
#                self.panelPropriete.MiseAJour()

    
    
    
    
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
    def SetNum(self, numCI = None, poids = 1):
#        print "SetNum", numCI
        if numCI != None:
            self.numCI = numCI
#            self.poids = poids
            
        if hasattr(self, 'arbre'):
            self.MaJArbre()
        
#        if len(self.numCI) > 0 :
        self.parent.Verrouiller()
        
    ######################################################################################  
    def GetIntit(self, num):
        if self.GetReferentiel().CI_cible:
            lstCI = self.parent.classe.referentiel.CentresInterets
        else:
            lstCI = self.GetReferentiel().CentresInterets
        if self.numCI[num] < len(lstCI):
            return lstCI[self.numCI[num]]
            
    
    
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
        self.codeBranche = GUI.CodeBranche(self.arbre)
        self.branche = arbre.AppendItem(branche, getSingulierPluriel(self.GetReferentiel().nomCI, True)+u" :", 
                                        wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Ci"])
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)

        
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
        self.arbre.SetItemText(self.branche, getSingulierPluriel(self.GetReferentiel().nomCI, True)+u" :")
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.construire()
            
            
####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Competences(Objet_sequence):
    def __init__(self, parent, panelParent, numComp = None):
#        Objet_sequence.__init__(self)
#        self.clefs = Competences.keys()
#        self.clefs.sort()
        self.parent = parent
        self.num = numComp
        self.competences = []
#        self.SetNum(numComp)
        if panelParent:
            self.panelParent = panelParent
            self.panelPropriete = GUI.PanelPropriete_Competences(panelParent, self)
        
    ######################################################################################  
    def __repr__(self):
        t = ''
        for n in self.competences:
            t += n
        
        return t
        
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
            self.competences.append(branche.get("C"+str(i), ""))
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJour()
    
    
    ######################################################################################  
    def GetCode(self, num):
        return self.competences[num]
    
    ######################################################################################  
    def GetIntit(self, num):
        return REFERENTIELS[self.parent.typeEnseignement].getCompetence(self.competences[num])[0]
    
    
         
#    ######################################################################################  
#    def SetNum(self, num):
#        self.num = num
#        if num != None:
#            self.code = self.clefs[self.num]
#            self.competence = Competences[self.code]
#            
#            if hasattr(self, 'arbre'):
#                self.SetCode()
#        
#    ######################################################################################  
#    def SetCode(self):
#        self.codeBranche.SetLabel(self.code)
    
#    #############################################################################
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
#            return self.branche

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = GUI.CodeBranche(self.arbre, u"")
#        self.codeBranche.SetBackgroundColour(wx.Colour(COUL_COMPETENCES[0]*255, COUL_COMPETENCES[1]*255, COUL_COMPETENCES[2]*255))
        t = self.GetReferentiel().nomCompetences
        self.branche = arbre.AppendItem(branche, t, wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Com"])
        self.arbre.SetItemTextColour(self.branche, constantes.GetCouleurWx(COUL_COMPETENCES))
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        self.arbre.SetItemText(self.branche, self.GetReferentiel().nomCompetences)
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.Destroy()
            self.panelPropriete = GUI.PanelPropriete_Competences(self.panelParent, self)
#            self.panelPropriete.construire()
        
#    ######################################################################################  
#    def AfficherMenuContextuel(self, itemArbre):
#        if itemArbre == self.branche:
#            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerObjectif, item = itemArbre)]])
            
            
####################################################################################
#
#   Classe définissant les propriétés de savoirs
#
####################################################################################
class Savoirs(Objet_sequence):
    def __init__(self, parent, panelParent, num = None, prerequis = False):
#        Objet_sequence.__init__(self)
        self.parent = parent # la séquence
#        self.num = num
        self.savoirs = []
        if panelParent:
            self.panelPropriete = GUI.PanelPropriete_Savoirs(panelParent, self, prerequis)
        
    ######################################################################################  
    def __repr__(self):
        t = ''
        for n in self.savoirs:
            t += n
        return t
        
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
                        code = "B"+code[1:]
                    else:
                        if self.GetReferentiel().tr_com == []:
                            code = "B"+code
                        else:
                            code = "S"+code

                self.savoirs.append(code)
        if hasattr(self, 'panelPropriete'):
#            self.panelPropriete.construire()
            self.panelPropriete.MiseAJour()
        
    ######################################################################################  
    def GetCode(self, num):
        return self.savoirs[num]
    
    
    ######################################################################################  
    def GetTypCode(self, num):
        return self.savoirs[num][0], self.savoirs[num][1:]
    
    
    ######################################################################################  
    def GetIntit(self, num):
        return self.GetReferentiel().getSavoir(self.GetCode(num))  
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        
        self.arbre = arbre
        self.codeBranche = GUI.CodeBranche(self.arbre, u"")
        t = self.GetReferentiel().nomSavoirs
        self.branche = arbre.AppendItem(branche, t, wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Sav"])
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
    
#    #############################################################################
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
#            return self.branche
        
        
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, self.GetReferentiel().nomSavoirs)
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJourTypeEnseignement()
#            self.panelPropriete.construire()
    
#    ######################################################################################  
#    def SetNum(self, num):
#        self.num = num
#        if num != None:
#            self.code = self.clefs[self.num]
#            self.savoir = Savoirs[self.code]
#            
#            if hasattr(self, 'arbre'):
#                self.SetCode()
        
#    ######################################################################################  
#    def SetCode(self):
#        self.codeBranche.SetLabel(self.code)
        

#    ######################################################################################  
#    def ConstruireArbre(self, arbre, branche):
#        self.arbre = arbre
#        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
#        self.branche = arbre.AppendItem(branche, u"Savoirs :", wnd = self.codeBranche, data = self,
#                                        image = self.arbre.images["Com"])
#        
#        
#    ######################################################################################  
#    def AfficherMenuContextuel(self, itemArbre):
#        if itemArbre == self.branche:
#            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerObjectif, item = itemArbre)]])
            
                  
            

####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Seance(ElementDeSequence, Objet_sequence):
    
                  
    def __init__(self, parent, panelParent = None, typeSeance = "", typeParent = 0, branche = None):
        """ Séance :
                parent = le parent wx pour contenir "panelPropriete"
                typeSceance = type de séance parmi "TypeSeance"
                typeParent = type du parent de la séance :  0 = séquence
                                                            1 = séance "Rotation"
                                                            2 = séance "parallèle"
        """
    
        ElementDeSequence.__init__(self)
#        Objet_sequence.__init__(self)
        
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
        self.parent = parent
        self.panelParent = panelParent
        
        if branche != None:
            self.setBranche(branche)
        else:
            self.seances = []
            self.SetType(typeSeance)
            self.AjouterListeSystemes(self.GetDocument().systemes)
            
#        self.SetType(typeSeance)
        
        
        #
        # Création du Tip (PopupInfo)
        #
        if self.GetApp() and isinstance(self.GetApp(), GUI.FenetreSequence) :
            self.tip = GUI.PopupInfo2(self.GetApp(), u"Séance")
            self.tip_type = self.tip.CreerTexte((1,0), flag = GUI.ALL)
            self.tip_intitule = self.tip.CreerTexte((2,0))
            self.tip_titrelien, self.tip_ctrllien = self.tip.CreerLien((3,0))
            self.tip_description = self.tip.CreerRichTexte(self, (4,0))
        
        
        
        if panelParent != None:
            self.panelPropriete = GUI.PanelPropriete_Seance(panelParent, self)
            self.panelPropriete.AdapterAuType()
        
        
        
        
    
    ######################################################################################  
    def __repr__(self):
        t = self.code 
#        t += " " +str(self.GetDuree()) + "h"
#        t += " " +str(self.effectif)
#        for s in self.seances:
#            t += "  " + s.__repr__()
        return t
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    
    
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
        
        self.lien.getBranche(root)
        
        if self.typeSeance in ["R", "S"]:
            for sce in self.seances:
                root.append(sce.getBranche())
            root.set("nbrRotations", str(self.nbrRotations.v[0]))
#            root.set("nbrGroupes", str(self.nbrGroupes.v[0]))
            
        elif self.typeSeance in ["AP", "ED", "P"]:
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
        self.ordre = eval(branche.tag[6:])
        
        self.intitule  = branche.get("Intitule", "")
        self.taille.v[0] = eval(branche.get("Taille", "100"))
        self.typeSeance = branche.get("Type", "C")
        self.description = branche.get("Description", None)
        
        self.lien.setBranche(branche, self.GetPath())
        
        if self.typeSeance in ["R", "S"]:
            self.seances = []
            for sce in list(branche):
                seance = Seance(self, self.panelParent)
                self.seances.append(seance)
                seance.setBranche(sce)
            self.duree.v[0] = self.GetDuree()
            if self.typeSeance == "R":
                self.nbrRotations.v[0] = eval(branche.get("nbrRotations", str(len(self.seances))))
#                self.nbrGroupes.v[0] = eval(branche.get("nbrGroupes", str(len(self.Get???))))
                self.reglerNbrRotMaxi()
            
        elif self.typeSeance in ["AP", "ED", "P"]:   
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
        
#        self.MiseAJourListeSystemes()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeSystemes()
            self.panelPropriete.MiseAJour()
        

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
    
    def GetCode(self, num):
        return self.code
    
    def GetIntit(self, num):
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
                message = u"Effectif de la séance supperieur à celui du groupe \"effectif réduit\""
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
#        d = self.GetDuree(graph = True)
#        if d != 0:
#            return 0.001*log(d*2)+0.001
#        return d
           
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
            self.panelPropriete.MiseAJourDuree()

        
        elif self.typeSeance == "R" : # Rotation
#            for s in self.seances:
#                if s.typeSeance in ["R", "S"]:
#                    s.SetDuree(duree, recurs = False)
#                else:
#                    s.duree.v[0] = duree
#                    s.panelPropriete.MiseAJourDuree()
            self.duree.v[0] = self.GetDuree()
            self.panelPropriete.MiseAJourDuree()

        
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
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.vcNombreRot.mofifierValeursSsEvt()
        
    ######################################################################################  
    def SetIntitule(self, text):           
        self.intitule = text
        if self.intitule != "":
            texte = u"Intitulé : "+ "\n".join(textwrap.wrap(self.intitule, 40))
        else:
            texte = u""
        self.tip.SetTexte(texte, self.tip_intitule)
           
    
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
        if type(typ) == str or type(typ) == unicode:
            self.typeSeance = typ
        else:
            self.typeSeance = self.GetReferentiel().listeTypeSeance[typ]
            
        if hasattr(self, 'arbre'):
            self.SetCode()
            
        if self.typeSeance in ["R","S"] and len(self.seances) == 0: # Rotation ou Serie
            self.AjouterSeance()
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.AdapterAuType()
        
        if self.EstSousSeance() and self.parent.typeSeance in ["R","S"]:
            self.parent.SignalerPb(self.parent.IsEffectifOk(), 0)
        
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
        self.tip.SetRichTexte()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.rtc.Ouvrir()
        
        if self.typeSeance in ["R", "S"]:
            for sce in self.seances:
                sce.PubDescription() 
                
    ######################################################################################  
    def SetDescription(self, description):   
        if self.description != description:
            self.description = description
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.sendEvent()
            self.tip.SetRichTexte()

    ######################################################################################  
    def SetCodeBranche(self):
        if hasattr(self, 'codeBranche') and self.typeSeance != "":
            self.codeBranche.SetLabel(self.code)
            self.arbre.SetItemText(self.branche, self.GetReferentiel().seances[self.typeSeance][0])
            
                  
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

        # Tip
        if hasattr(self, "tip"):
            self.tip.SetTitre(u"Séance "+ self.code)
            if self.typeSeance != "":
                t = u"Type : "+ self.GetReferentiel().seances[self.typeSeance][1]
            else:
                t = u""
            self.tip.SetTexte(t, self.tip_type)    
                
            if self.intitule != "":
                t = u"Intitulé : "+ textwrap.fill(self.intitule, 40)
            else:
                t = u""
            self.tip.SetTexte(t, self.tip_intitule)  
        
        
        
    
            
            
            
            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = GUI.CodeBranche(self.arbre, self.code)
        if self.typeSeance != "":
            image = self.arbre.images[self.typeSeance]
        else:
            image = -1
        
        self.branche = arbre.AppendItem(branche, u"Séance :", wnd = self.codeBranche, 
                                            data = self, image = image)
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
            
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
        print "CollerElem"
        seance_avant = self.arbre.GetItemPyData(item)
        print "   ", seance_avant
        
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
            print "     dans :"
            seance = Seance(seance_avant, self.panelParent, typeSeance = typeSeance,
                            branche = bseance)
            seance_avant.seances.insert(0, seance)
            
        else:
            print "     après :"
            seance = Seance(self.parent, self.panelParent, typeSeance = typeSeance,
                            branche = bseance)
            i = seance_avant.parent.seances.index(seance_avant)
            seance_avant.parent.seances.insert(i+1, seance)
        
        seq = self.GetDocument()
        
        seq.OrdonnerSeances()
#        seance.ConstruireArbre(self.arbre, seq.brancheSce)
        seq.reconstruireBrancheSeances(seance_avant, seance)
        
        seance.panelPropriete.MiseAJour()
        seance.panelPropriete.MiseAJourListeSystemes()
        
        self.panelPropriete.sendEvent()
        
        self.arbre.SelectItem(seance.branche)        
            
    ######################################################################################  
    def AjouterSeance(self, event = None):
        """ Ajoute une séance é la séance
            !! Uniquement pour les séances de type "Rotation" ou "Serie" !!
        """
        seance = Seance(self, self.panelParent)
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
        
        self.arbre.SelectItem(seance.branche)


    ######################################################################################  
    def SupprimerSeance(self, event = None, item = None):
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            if len(self.seances) > 1: # On en laisse toujours une !!
                seance = self.arbre.GetItemPyData(item)
                self.seances.remove(seance)
                self.arbre.Delete(item)
                self.OrdonnerSeances()
                self.panelPropriete.sendEvent()
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
        return
    
    #############################################################################
    def MiseAJourTypeEnseignement(self):
        if self.typeSeance in ["R", "S"]:
            for s in self.seances:
                s.MiseAJourTypeEnseignement()
        else:
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.MiseAJourTypeEnseignement()
        
    ######################################################################################  
    def MiseAJourNomsSystemes(self):
        if self.typeSeance in ["AP", "ED", "P"]:
            sequence = self.GetDocument()
            for i, s in enumerate(sequence.systemes):
                self.systemes[i].n = s.nom
#            self.nSystemes = len(sequence.systemes)
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.MiseAJourListeSystemes()
                                 
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.MiseAJourNomsSystemes()
        
    ######################################################################################  
    def SupprimerSysteme(self, i):
        if self.typeSeance in ["AP", "ED", "P"]:
            del self.systemes[i]
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.SupprimerSysteme(i)

        
        
    ######################################################################################  
    def AjouterSysteme(self, nom = "", nombre = 0, construire = True):
        if self.typeSeance in ["AP", "ED", "P"]:
            self.systemes.append(Variable(nom, lstVal = nombre, nomNorm = "", typ = VAR_ENTIER_POS, 
                                          bornes = [0,9], modeLog = False,
                                          expression = None, multiple = False))
            if construire and hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
                
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.AjouterSysteme(nom, nombre)
    
    
    ######################################################################################  
    def AjouterListeSystemes(self, lstSys, lstNSys = None):
#        print "  AjouterListeSystemes", self.typeSeance
        if self.typeSeance in ["AP", "ED", "P"]:
            if lstNSys == None:
                lstNSys = [0]*len(lstSys)
            for i, s in enumerate(lstSys):
#                print "    ", s
                self.AjouterSysteme(s, lstNSys[i], construire = False)
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
            
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.AjouterListeSystemes(lstSys, lstNSys) 
                
                
    ######################################################################################  
    def GetDocument(self):    
        if self.EstSousSeance():
            sequence = self.parent.GetDocument()
        else:
            sequence = self.parent
        return sequence
    
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
                              GUI.getIconeCopy()])
            
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
                                  GUI.getIconePaste()])
                            
            self.GetApp().AfficherMenuContextuel(listItems)           
                            
#            item2 = menu.Append(wx.ID_ANY, u"Créer une rotation")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterRotation, item = i()tem), item2)
#            
#            item3 = menu.Append(wx.ID_ANY, u"Créer une série")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterSerie, item = item), item3)
            

            
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
#            if posDansRot > 0:
#                rotation = self.parent
#                l = rotation.seances
#                for t in range(posDansRot):
#                    l = draw_cairo.permut(l)
#                for i, s in enumerate(l[:rotation.nbrRotations.v[0]]):
#                    dd = s.GetNbrSystemes(complet)
#                    for k, v in dd.items():
#                        up(d, k, v)
    #                    d[s.n] = s.v[0]*self.nombre.v[0]
        
        return d
        
        
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
#            self.arbre.DoSelectItem(self.branche)
            return self.branche
        
        else:
            if self.typeSeance in ["R", "S"]:
                ls = self.seances
            else:
                return
            continuer = True
            i = 0
            branche = None
            while continuer:
                if i >= len(ls):
                    continuer = False
                else:
                    branche = ls[i].HitTest(x, y)
                    if branche:
                        continuer = False
                i += 1
            return branche
        
        
        






####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Tache(Objet_sequence):
    
                  
    def __init__(self, projet, panelParent, intitule = u"", phaseTache = "", duree = 1.0, branche = None):
        """ Séance :
                panelParent = le parent wx pour contenir "panelPropriete"
                phaseTache = phase de la tache parmi 'Ana', 'Con', 'Rea', 'Val'
        """
#        print "__init__ tâche", phaseTache
        
#        Objet_sequence.__init__(self)
        
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

        # Les autres données
        self.projet = projet
        self.panelParent = panelParent
        
        self.phase = phaseTache
        
        
#        
        if branche != None:
            self.setBranche(branche)
##            if not Ok:
##                self.code = -err # Pour renvoyer une éventuelle erreur à l'ouverture d'un fichier
        else:
#        if branche == None:
            self.indicateursEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []} # clef = n°eleve ;  valeur = liste d'indicateurs
            if phaseTache in TOUTES_REVUES_SOUT:
                self.indicateursMaxiEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
            
        if panelParent:
            self.panelPropriete = GUI.PanelPropriete_Tache(panelParent, self)
        else:
            print "pas panelParent", self
            
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeEleves()
            self.panelPropriete.MiseAJourDuree()
            self.panelPropriete.MiseAJour()
            
        #
        # Création du Tip (PopupInfo)
        #
        if self.GetApp():
            if hasattr(self, "branche"):
                b = self.branche
            else:
                b = None
            self.tip = GUI.PopupInfo2(self.GetApp(), u"Tâche", self.GetDocument(), b)
            self.tip.sizer.SetItemSpan(self.tip.titre, (1,2))
            
            
            if self.phase in TOUTES_REVUES_SOUT:
                p = self.tip.CreerTexte((1,0), txt = u"Délai (depuis début du projet) :", 
                                        flag = GUI.ALIGN_RIGHT|GUI.ALL,
                                        font = GUI.getFont_9S())
                
        
                self.tip_delai = self.tip.CreerTexte((1,1), 
                                                     flag = GUI.ALIGN_LEFT|GUI.BOTTOM|GUI.TOP|GUI.LEFT)

            else:
                p = self.tip.CreerTexte((1,0), txt = u"Phase :", 
                                        flag = GUI.ALIGN_RIGHT|GUI.ALL, 
                                        font = GUI.getFont_9S())
                
                self.tip_phase = self.tip.CreerTexte((1,1), 
                                                     flag = GUI.ALIGN_LEFT|GUI.BOTTOM|GUI.TOP|GUI.LEFT)
            
            if not self.phase in TOUTES_REVUES_EVAL_SOUT:
                i = self.tip.CreerTexte((2,0), txt = u"Intitulé :", 
                                        flag = GUI.ALIGN_RIGHT|GUI.ALL, 
                                        font = GUI.getFont_9S())

                self.tip_intitule = self.tip.CreerTexte((2,1), 
                                                        flag = GUI.ALIGN_LEFT|GUI.BOTTOM|GUI.TOP|GUI.LEFT)
                
            self.tip_description = self.tip.CreerRichTexte(self, (3,0), (1,2))
                
                
                
        
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
        return self.code +" ("+str(self.ordre)+")"
    
    
    ######################################################################################  
    def GetApp(self):
        return self.projet.GetApp()

    ######################################################################################  
    def ActualiserDicIndicateurs(self):
        """ Complète le dict des compétences/indicateurs globaux (tous les élèves confondus)
        """
#        print "ActualiserDicIndicateurs", self
        for i in range(len(self.projet.eleves)):
            indicateurs = self.indicateursEleve[i+1]#self.GetDicIndicateursEleve(eleve)
            for c in indicateurs:
                if not c in self.indicateursEleve[0]:
                    self.indicateursEleve[0].append(c)
#                self.indicateursEleve[0] = [x or y for x, y in zip(self.indicateursEleve[0], lc)]

            
            
        
    ######################################################################################  
    def GetDicIndicateurs(self):
        """ Renvoie l'ensemble des indicateurs de compétences à mobiliser pour cette tâche
            Dict :  clef = code compétence
                  valeur = liste [True False ...] des indicateurs à mobiliser
        """
#        print "GetDicIndicateurs", self, ":", self.indicateursEleve
        tousIndicateurs = self.GetProjetRef()._dicIndicateurs_simple
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
#            else:
#                competence, sscomp, indicateur = cci
#                indicateur = int(eval(indicateur)-1)
#                nbrIndic = 0
#                for sc in tousIndicateurs[competence].values():
#                    nbrIndic += len(sc)
#                if not competence in indicateurs.keys():
#                    indicateurs[competence] = [False]*nbrIndic
#                
#                indicateurs[competence][indicateur] = True
                    
        return indicateurs
    
    
    ######################################################################################  
    def GetDicIndicateursEleve(self, eleve):
        """ Renvoie l'ensemble des indicateurs de compétences à mobiliser pour cette REVUE
            Dict :  clef = code compétence
                  valeur = liste [True False ...] des indicateurs à mobiliser
        """
#        print "GetDicIndicateursEleve", self, eleve.id+1
        indicateurs = {}
        numEleve = eleve.id
        for i in self.indicateursEleve[numEleve+1]:
            competence, indicateur = i.split('_')
            indicateur = eval(indicateur)-1
            if not competence in indicateurs.keys():
                indicateurs[competence] = [False]*len(self.GetProjetRef()._dicIndicateurs_simple[competence])
            
            indicateurs[competence][indicateur] = True
#        print "  >>", indicateurs
        return indicateurs
    
    ######################################################################################  
    def DiffereSuivantEleve(self):
        """ Renvoie True si cette REVUE est différente selon l'élève
            Renvoie False si tous les élèves abordent les mêmes compétences/indicateurs
        """
#        print "DiffereSuivantEleve", self, self.phase
        if len(self.projet.eleves) == 0:
            return False
        indicateurs = self.GetDicIndicateursEleve(self.projet.eleves[0])
        for eleve in self.projet.eleves[1:]:
            ie = self.GetDicIndicateursEleve(eleve)
            if set(indicateurs.keys()) != set(ie.keys()):
                return True
            for k, v in ie.items():
                if set(v) != set(indicateurs[k]):
                    return True
            
        return False
    
    ######################################################################################  
    def GetCompetencesUtil(self):
        lst = []
        for i in self.indicateursEleve[0]:
            lst.append(i.split('_')[0])
        return lst
        
        
#    ######################################################################################  
#    def initIndicateurs(self):
#        # Les indicateurs séléctionnés ou bien les poids des indicateurs 
#        #     clef = code compétence
#        #     Pour la SSI :  valeur = poids
#        #     Pour la STI2D : valeur = liste d'index
#        typeEns = self.GetTypeEnseignement()
#        if False:#typeEns == "SSI":
#            indicateurs = REFERENTIELS[typeEns]._dicCompetences_prj_simple
#            self.indicateursEleve[0] = dict(zip(indicateurs.keys(), [x[1] for x in indicateurs.values()]))
#        else:
#            indicateurs = REFERENTIELS[typeEns].dicIndicateurs
#            self.indicateursEleve[0] = {}
#            for k, dic in indicateurs.items():
#                ndict = dict(zip(dic[1].keys(), [[]]*len(dic[1])))
#                for c in ndict.keys():
#                    ndict[c] = [True]*len(indicateurs[k][1][c])
#                self.indicateursEleve[0].update(ndict)
            
            
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la tâche pour enregistrement
        """
        root = ET.Element("Tache"+str(self.ordre))
        root.set("Phase", self.phase)
        root.set("Intitule", self.intitule)

        if self.description != None:
            root.set("Description", self.description)

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
                    
            if self.phase in lstR:
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
            
            
            
#            # Structure des indicateurs :
#            # <Indicateurs Indic0="True False True " Indic1="True False False True " ..... />
#            if self.GetTypeEnseignement() == "SSI":
#                brancheInd = ET.Element("PoidsIndicateurs")
#            else:
#                brancheInd = ET.Element("Indicateurs")
#            root.append(brancheInd)
#            for i, c in enumerate(self.competences):
#                if self.GetTypeEnseignement() == "SSI":
#                    if c in self.indicateurs.keys():
#                        brancheInd.set("Poids"+str(i), str(self.indicateurs[c]))
#                else:
#                    if c in self.indicateurs.keys():
#                        brancheInd.set("Indic"+str(i), toTxt(self.indicateurs[c]))
            
            
        root.set("IntituleDansDeroul", str(self.intituleDansDeroul))
        
        return root    
        
    ######################################################################################  
    def setBranche(self, branche):
#        print "setBranche tâche", 
   
        err = []
        
        self.ordre = eval(branche.tag[5:])
        self.intitule  = branche.get("Intitule", "")
        
        self.phase = branche.get("Phase", "")
#        print self.phase

        # Suite commentée ... à voir si pb
#        if self.GetTypeEnseignement() == "SSI":
#            if self.phase == 'Con':
#                self.phase = 'Ana'
#            elif self.phase in ['DCo', 'Val']:
#                self.phase = 'Rea'

        self.description = branche.get("Description", None)
        
        if not self.phase in TOUTES_REVUES_EVAL_SOUT:
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        else:
            self.duree.v[0] = 0.5
        
        brancheElv = branche.find("Eleves")
        self.eleves = []
        for i, e in enumerate(brancheElv.keys()):
            self.eleves.append(eval(brancheElv.get("Eleve"+str(i))))
        
        self.indicateursEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
        
        if self.GetClasse().GetVersionNum() < 5:
            if not self.phase in [self.projet.getCodeLastRevue(), "S"]:
                self.indicateursMaxiEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
                
                
            pass # Nouveaux indicateurs STI2D !!
        else:
            if not self.phase in [self.projet.getCodeLastRevue(), "S"]:
                self.indicateursMaxiEleve = { 0 : [], 1 : [], 2 : [], 3 : [],4 : [], 5 : [],6 : []}
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
                                lst = [True]*len(self.GetProjetRef()._dicIndicateurs[e])
                            for n,j in enumerate(lst):
                                if j:
                                    self.indicateursEleve[0].append(brancheCmp.get(e)+"_"+str(n+1))
                        else:
                            indic = brancheCmp.get("Comp"+str(i))
                            self.indicateursEleve[0].append(indic.replace(".", "_"))
                    
                
                
                else:
                    brancheInd = branche.find("Indicateurs")
#                    print "  branche Indicateurs"
                    if brancheInd != None:
                        if self.projet.nbrRevues == 2:
                            lstR = [_R1]
                        else:
                            lstR = [_R1, _R2]

                        # 
                        # Indicateurs revue par élève (première(s) revues)
                        #
                        if self.phase in lstR:
                            for i, e in enumerate(self.projet.eleves):
                                
                                self.indicateursEleve[i+1] = []
                                
                                brancheE = brancheInd.find("Eleve"+str(i+1))
                                if brancheE != None:
                                    for c in brancheE.keys():
                                        codeindic = brancheE.get(c)
                                        code, indic = codeindic.split('_')
                                        
                                        # pour compatibilité version < 3.19
                                        if code == "CO8.es":
                                            code = "CO8.0"
                                            codeindic = code+"_"+indic
                                            
                                        # Si c'est la dernière phase et que c'est une compétence "Conduite" ... on passe
                                        indic = eval(indic)-1
                                        if self.phase == 'XXX' and self.GetReferentiel().getTypeIndicateur(codeindic) == 'C':
                                            continue
                                        
                                        try:
#                                            print "***",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                                            # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                                            if not code in self.GetProjetRef()._dicIndicateurs_simple:
                                                print "Erreur 1", code, "<>", self.GetProjetRef()._dicIndicateurs_simple
                                                err.append(constantes.Erreur(constantes.ERR_PRJ_T_TYPENS))
                                                return err
                                            
                                            if not codeindic in self.indicateursEleve[i+1]:
                                                self.indicateursEleve[i+1].append(codeindic)
                                        except:
                                            pass
                                
                                else: # Pour ouverture version <4.8beta1
                                    indicprov = []
                                    for c in brancheInd.keys():
                                        codeindic = brancheInd.get(c)
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
                                        if not code in self.GetProjetRef()._dicIndicateurs:
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
                                code, indic = codeindic.split('_')
#                                print "     ", code, indic
                                # pour compatibilité version < 3.19
                                if code == "CO8.es":
                                    code = "CO8.0"
                                    codeindic = code+"_"+indic
                                    
                                # Si c'est la dernière phase et que c'est une compétence "Conduite" ... on passe
                                indic = eval(indic)-1
                                if self.phase == 'XXX' and self.GetProjetRef().getTypeIndicateur(codeindic) == 'C':
                                    continue
                                
                                    
#                                try:
#                                    print "******",self.GetReferentiel().dicIndicateurs_prj[code][indic]
                                # si le type d'enseignement ne colle pas avec les indicateurs (pb lors de l'enregistrement)
                                if not code in self.GetProjetRef()._dicIndicateurs_simple.keys():
                                    print "Erreur 3", code, "<>", self.GetProjetRef()._dicIndicateurs_simple.keys()
                                    if not constantes.Erreur(constantes.ERR_PRJ_T_TYPENS) in err:
                                        err.append(constantes.Erreur(constantes.ERR_PRJ_T_TYPENS))
                                else:
                                    self.indicateursEleve[0].append(codeindic)
#                                except:
#                                    pass
                        
                    
#        print self.indicateursEleve
        
        self.ActualiserDicIndicateurs()
            
        self.intituleDansDeroul = eval(branche.get("IntituleDansDeroul", "True"))

        return err
    
#        if hasattr(self, 'panelPropriete'):
#            self.panelPropriete.ConstruireListeEleves()
#            self.panelPropriete.MiseAJourDuree()
#            self.panelPropriete.MiseAJour()
#            self.panelPropriete.MiseAJourPoidsCompetences()


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
    
    def GetCode(self, num):
        return self.code
    
    def GetIntit(self, num):
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
        self.panelPropriete.MiseAJourDuree()
        self.projet.MiseAJourDureeEleves()
        
    ######################################################################################  
    def SetIntitule(self, text):           
        self.intitule = text
        if self.intitule != "":
            t = u"Intitulé : "+ "\n".join(textwrap.wrap(self.intitule, 40))
        else:
            t = u""
        self.tip.SetTexte(t, self.tip_intitule)
        
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
        
    
    ######################################################################################  
    def PubDescription(self):
        """ Publie toutes les descriptions de tâche
            (à l'ouverture)
        """
        self.tip.SetRichTexte()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.rtc.Ouvrir()

                
    ######################################################################################  
    def SetDescription(self, description):   
        if self.description != description:
            self.description = description
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.sendEvent()
            self.tip.SetRichTexte()
            
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
                t = u""
            else:
                self.codeBranche.SetLabel(self.code)
                t = u" :"
            self.arbre.SetItemText(self.branche, self.GetProjetRef().phases[self.phase][1]+t)
        
        #
        # Tip (fenêtre popup)
        #
        if self.phase in TOUTES_REVUES_SOUT:
            self.tip.SetTitre(self.GetProjetRef().phases[self.phase][1])
            self.tip.SetTexte(draw_cairo.getHoraireTxt(self.GetDelai()), self.tip_delai)

        else:
            self.tip.SetTitre(u"Tâche "+ self.code)
            if self.phase != "":
                    t = self.GetProjetRef().phases[self.phase][1]
            else:
                t = u""
            if hasattr(self, "tip_phase"):
                self.tip.SetTexte(t, self.tip_phase)


        if not self.phase in TOUTES_REVUES_EVAL_SOUT:
            if self.intitule != "":
                t = textwrap.fill(self.intitule, 50)
            else:
                t = u""
            self.tip.SetTexte(t, self.tip_intitule)
            
            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = GUI.CodeBranche(self.arbre, self.code)
        if self.phase != "":
            image = self.arbre.images[self.phase]
        else:
            image = -1
            
        self.branche = arbre.AppendItem(branche, u"Tâche :", wnd = self.codeBranche, 
                                        data = self, image = image)
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
            
        if self.phase in TOUTES_REVUES_EVAL:
            arbre.SetItemTextColour(self.branche, "red")
        elif self.phase == "Rev":
            arbre.SetItemTextColour(self.branche, "ORANGE")
        elif self.phase == "S":
            arbre.SetItemTextColour(self.branche, "PURPLE")
    
    
    ######################################################################################  
    def MiseAJourNomsEleves(self):
        """ Met à jour la liste des élèves concernés par la tâche
            et la liste des élèves du panelPropriete de la tâche
        """
#        projet = self.GetDocument()
#        for i, s in enumerate(projet.eleves):
#            self.eleves[i].n = s.nom
#            self.nSystemes = len(sequence.systemes)
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJourListeEleves()
                                 
    
    #############################################################################
    def MiseAJourTypeEnseignement(self, ref):
        self.panelPropriete.MiseAJourTypeEnseignement(ref)
        
    ######################################################################################  
    def SupprimerSysteme(self, i):
        if self.typeSeance in ["AP", "ED", "P"]:
            del self.systemes[i]
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.ConstruireListeSystemes()
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.seances:
                s.SupprimerSysteme(i)

        
    ######################################################################################  
    def AjouterEleve(self):
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeEleves()
    
    
    ######################################################################################  
    def SupprimerEleve(self, i):
        if i in self.eleves:
            self.eleves.remove(i)

        for i, ident in enumerate(self.eleves):
            if ident > i:
                self.eleves[i] = ident-1

        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.ConstruireListeEleves()
        

    
    ######################################################################################  
    def MiseAJourPoidsCompetences(self, code = None):
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJourPoidsCompetences(code)
                
    ######################################################################################  
    def GetDocument(self):    
        return self.projet
    
    ######################################################################################  
    def GetClasse(self):
        return self.GetDocument().classe
    
    ######################################################################################  
    def GetSuivante(self):
        i = self.projet.taches.index(self)
        if len(self.projet.taches) > i:
            return self.projet.taches[i+1]
    
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
#            listItems.append([u"Copier", functools.partial(self.projet.CopierTache, item = itemArbre)])
            listItems.append([u"Copier", 
                              self.CopyToClipBoard, 
                              GUI.getIconeCopy()])
 
#            elementCopie = self.GetApp().parent.elementCopie
            elementCopie = GetObjectFromClipBoard('Tache')
            if elementCopie is not None:
                phase = elementCopie.get("Phase", "")
                if self.phase == phase or self.GetSuivante().phase == phase : # la phase est la même
                    listItems.append([u"Coller après", functools.partial(self.projet.CollerElem, 
                                                                         item = itemArbre, 
                                                                         btache = elementCopie),
                                      GUI.getIconePaste()])
                    
            self.GetApp().AfficherMenuContextuel(listItems)
#            item2 = menu.Append(wx.ID_ANY, u"Créer une rotation")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterRotation, item = item), item2)
#            
#            item3 = menu.Append(wx.ID_ANY, u"Créer une série")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterSerie, item = item), item3)
        
        

        
        
        
        
        
        
        
        
        
        
        
        
####################################################################################
#
#   Classe définissant les propriétés d'un système
#
####################################################################################
class Systeme(ElementDeSequence, Objet_sequence):
    def __init__(self, parent, panelParent, nom = u""):
        
        ElementDeSequence.__init__(self)
        
        self.parent = parent
        self.nom = nom
        self.nbrDispo = Variable(u"Nombre dispo", lstVal = 1, nomNorm = "", typ = VAR_ENTIER_POS, 
                              bornes = [0,20], modeLog = False,
                              expression = None, multiple = False)
        self.image = None
        self.lienClasse = None
        
        #
        # Création du Tip (PopupInfo)
        #
        self.tip = GUI.PopupInfo2(self.parent.app, u"Système ou matériel")
        self.tip_nom = self.tip.CreerTexte((1,0))
        self.tip_nombre, self.tip_ctrllien = self.tip.CreerLien((2,0))
        self.tip_image = self.tip.CreerImage((3,0))
        
        
        if panelParent != None:
            self.panelPropriete = GUI.PanelPropriete_Systeme(panelParent, self)
        
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
        
    ######################################################################################  
    def __repr__(self):
        if self.image != None:
            i = GUI.img2str(self.image.ConvertToImage())[:20]
        else:
            i = "None"
        return self.nom+" ("+str(self.nbrDispo.v[0])+") " + i
        
        
#    ######################################################################################  
#    def __eq__(self, s):
#        if s == None:
#            return False
#        elif self.nom != s.nom:
#            return False
#        elif self.nbrDispo.v[0] != s.nbrDispo.v[0]:
#            return False
#        elif self.lien != s.lien:
#            return False
#        elif img2str(self.image.ConvertToImage()) != img2str(s.image.ConvertToImage()):
#            return False
#        
#        return True

    
    
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
                root.set("Image", GUI.img2str(self.image.ConvertToImage()))
        
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
                    if hasattr(self, 'panelPropriete'):
                        self.panelPropriete.MiseAJour()
                        self.panelPropriete.Verrouiller(False)
                        self.panelPropriete.cbListSys.SetSelection(self.panelPropriete.cbListSys.FindString(self.nom))
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
            
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.MiseAJour()


    ######################################################################################  
    def Copie(self, parent, panelParent = None):
        s = Systeme(parent, panelParent)
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
                        if hasattr(s, 'panelPropriete'):
                            s.panelPropriete.MiseAJourListeSys(self.nom)
        
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
    def SetCode(self):
#        if hasattr(self, 'codeBranche'):
#            self.codeBranche.SetLabel(self.nom)
        if self.nom != "":
            t = self.nom
        else:
            t = u"Système ou matériel"
        
        if hasattr(self, 'arbre'):
            self.arbre.SetItemText(self.branche, t)
            
        # Tip
        if hasattr(self, 'tip'):
            self.tip.SetTexte(u"Nom : "+self.nom, self.tip_nom)
            self.tip.SetTexte(u"Nombre disponible : " + str(self.nbrDispo.v[0]), self.tip_nombre)


    ######################################################################################  
    def SetImage(self):
        self.tip.SetImage(self.image, self.tip_image)
        self.propagerChangements()
        

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
#        self.codeBranche = wx.StaticText(self.arbre, -1, self.nom)

#        if self.image == None or self.image == wx.NullBitmap:
        image = self.arbre.images["Sys"]
#        else:
#            image = self.image.ConvertToImage().Scale(20, 20).ConvertToBitmap()
        self.branche = arbre.AppendItem(branche, u"Système ou matériel", data = self,#, wnd = self.codeBranche
                                        image = image)
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
#        self.SetNom(self.nom)
        self.SetNombre()
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", 
                                                     functools.partial(self.parent.SupprimerSysteme, item = itemArbre),
                                                     images.Icone_suppr_systeme.GetBitmap()],
                                                    [u"Créer un lien", self.CreerLien, None]])
            
            
#    ######################################################################################  
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
##            self.arbre.DoSelectItem(self.branche)
#            return self.branche
    
    
    
        
#    ######################################################################################  
#    def OuvrirListeSystemes(self, nomFichier):
#        fichier = open(nomFichier,'r')
##        try:
#        systemes = ET.parse(fichier).getroot()
#        self.setBranche(systemes)
#        
#        fichier.close()

#    ######################################################################################  
#    def EnregistrerListeSystemes(self, nomFichier):
#        wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
#        fichier = file(nomFichier, 'w')
#        
#        systemes = self.getBranche()
#        indent(systemes)
#        
#        ET.ElementTree(systemes).write(fichier)
#        fichier.close()
#        
#        wx.EndBusyCursor()
  










####################################################################################
#
#   Classe définissant les propriétés d'un support de projet
#
####################################################################################
class Support(ElementDeSequence, Objet_sequence):
    def __init__(self, parent, panelParent, nom = u""):
        
        ElementDeSequence.__init__(self)
#        Objet_sequence.__init__(self)
        
        self.parent = parent
        self.nom = nom
        self.description = None
        
        self.image = None
        
        #
        # Création du Tip (PopupInfo)
        #
        self.tip = GUI.PopupInfo2(self.parent.app, u"Support")
        self.tip_nom = self.tip.CreerTexte((1,0))
        self.tip_titrelien, self.tip_ctrllien = self.tip.CreerLien((2,0))
        self.tip_image = self.tip.CreerImage((3,0))
        self.tip_description = self.tip.CreerRichTexte(self, (4,0))
        
        if panelParent:
            self.panelPropriete = GUI.PanelPropriete_Support(panelParent, self)
        
        
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
        
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
            root.set("Image", GUI.img2str(self.image.ConvertToImage()))
        
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
            
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.SetImage()
            self.panelPropriete.MiseAJour()
        
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
    def PubDescription(self):
        """ Publie toutes les descriptions de séance
            (à l'ouverture)
        """
        self.tip.SetRichTexte()
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.rtc.Ouvrir()
        
                
    ######################################################################################  
    def SetDescription(self, description):   
        if self.description != description:
            self.description = description
            if hasattr(self, 'panelPropriete'):
                self.panelPropriete.sendEvent()
            self.tip.SetRichTexte()
            
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
            
        # Tip
        if hasattr(self, 'tip'):
            self.tip.SetTexte(u"Nom : "+self.nom, self.tip_nom)
            

    ######################################################################################  
    def SetImage(self):
        self.tip.SetImage(self.image, self.tip_image)
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        image = self.arbre.images["Sup"]
        self.branche = arbre.AppendItem(branche, u"Support", data = self,#, wnd = self.codeBranche
                                        image = image)
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)

        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Créer un lien", self.CreerLien, None]])
            
            
#    ######################################################################################  
#    def HitTest(self, x, y):
#        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect)[0]:
##            self.arbre.DoSelectItem(self.branche)
#            return self.branche
    
    
    
####################################################################################
#
#   Classe définissant les propriétés d'une personne
#
####################################################################################
class Personne(Objet_sequence):
    def __init__(self, projet, panelParent, Id = 0):
        self.projet = projet
        self.nom = u""
        self.prenom = u""
        self.avatar = None
        self.id = Id # Un identifiant unique = nombre > 0

        #
        # Création du Tip (PopupInfo)
        #
        self.ficheHTML = self.GetFicheHTML()

        self.ficheXML = parseString(self.ficheHTML.encode('utf-8', errors="ignore"))
       
        forceID(self.ficheXML)
        self.tip = GUI.PopupInfo(self.projet.app, self.ficheHTML)
#        self.tip_nom = self.tip.CreerTexte((1,0), flag = wx.ALIGN_LEFT|wx.TOP)
#        self.tip_nom.SetFont(wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
#        self.tip_avatar = self.tip.CreerImage((2,0))
#        
#        if self.code == 'Prf':
#            self.tip.SetTitre(u"Professeur")
#            self.tip_disc = self.tip.CreerTexte((3,0), flag = wx.ALIGN_LEFT|wx.TOP)
#            self.tip_disc.SetFont(wx.Font(10, wx.SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
#        else:
#            self.tip.SetTitre(self.titre.capitalize())
        
        
        if panelParent:
            self.panelPropriete = GUI.PanelPropriete_Personne(panelParent, self)

    ######################################################################################  
    def GetApp(self):
        return self.projet.GetApp()
        
        
    ######################################################################################  
    def GetDocument(self):
        return self.projet
    
    
    ######################################################################################  
    def __repr__(self):
        return self.GetNomPrenom()


    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
#        print "getBranche", supprime_accent(self.titre)
        root = ET.Element(toSystemEncoding(supprime_accent(self.titre).capitalize()))
        
        root.set("Id", str(self.id))
        root.set("Nom", self.nom)
        root.set("Prenom", self.prenom)
        if self.avatar != None:
            root.set("Avatar", GUI.img2str(self.avatar.ConvertToImage()))
        
        if hasattr(self, 'referent'):
            root.set("Referent", str(self.referent))
            
        if hasattr(self, 'discipline'):
            root.set("Discipline", str(self.discipline))
            
        if hasattr(self, 'grille'):
            for k, g in self.grille.items():
                root.set("Grille"+k, toSystemEncoding(g.path))
#            root.set("Grille0", self.grille[0].path)
#            root.set("Grille1", self.grille[1].path)
           
            
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
            
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.SetImage()
            self.panelPropriete.MiseAJourTypeEnseignement()
            self.panelPropriete.MiseAJour(marquerModifier = False)
        
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
    def SetTip(self):
        self.ficheHTML = self.GetFicheHTML()
        self.ficheXML = parseString(self.ficheHTML.encode('utf-8', errors="ignore"))
        forceID(self.ficheXML)
        SetWholeText(self.ficheXML, "nom", self.GetNomPrenom())
        
        self.tip.XML_AjouterImg(self.ficheXML, "av", self.avatar) 
        
        self.SetTip2()
        
        # Tip
#        if hasattr(self, 'tip'):
#            self.tip.SetTexte(self.GetNomPrenom(), self.tip_nom)
#            self.tip.SetImage(self.avatar, self.tip_avatar)

    ######################################################################################  
    def SetImage(self):
        self.SetTip()
        return
#        self.tip.SetImage(self.avatar, self.tip_avatar)
#        self.SetTip()
        
    


######################################################################################  
def supprime_accent(ligne):
    """ supprime les accents du texte source """
    accents = { u'a': [u'à', u'ã', u'á', u'â'],
                u'e': [u'é', u'è', u'ê', u'ë'],
                u'i': [u'î', u'ï'],
                u'u': [u'ù', u'ü', u'û'],
                u'o': [u'ô', u'ö'] }
    for (char, accented_chars) in accents.iteritems():
        for accented_char in accented_chars:
            ligne = ligne.replace(accented_char, char)
    return ligne

####################################################################################
#
#   Classe définissant les propriétés d'un élève
#
####################################################################################
class Eleve(Personne, Objet_sequence):
    def __init__(self, projet, panelParent, ident = 0):
        
        self.titre = u"élève"
        self.code = "Elv"
        
        self.grille = {} #[Lien(typ = 'f'), Lien(typ = 'f')]
        for k in projet.GetProjetRef().parties.keys():
            self.grille[k] = Lien(typ = 'f')
        
        Personne.__init__(self, projet, panelParent, ident)
 
        
        
    
            
    ######################################################################################  
    def GetDuree(self, phase = None, total = False):
        d = 0
        p = 0
        if not total and phase != None:
            for i, t in enumerate(self.projet.taches):
                if t.phase == phase:
                    break
                if t.phase in TOUTES_REVUES_EVAL_SOUT:
                    p = i
        
        for t in self.projet.taches[p:]:
            if t.phase == phase:
                break
            if not t.phase in TOUTES_REVUES_SOUT:
                if self.id in t.eleves:
                    d += t.GetDuree()
        return d
        
    ######################################################################################  
    def GetDureeJusqua(self, tache, depuis = None):
        d = 0
        p = 0
        if depuis != None:
            for i, t in enumerate(self.projet.taches):
                if t == depuis:
                    break
                p = i
        
        for t in self.projet.taches[p:]:
            if t == tache:
                break
            if not t.phase in TOUTES_REVUES_SOUT:
                if self.id in t.eleves:
                    d += t.GetDuree()
        return d
    
    ######################################################################################  
    def OuvrirGrille(self, k):
        try:
            self.grille[k].Afficher(self.projet.GetPath())#os.startfile(self.grille[num])
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
        return getNomFichier(prefixe, self.GetNomPrenom()+"_"+self.projet.intitule[:20])

        
    ######################################################################################  
    def GetNomGrilles(self, path = None):
        """ Renvoie les noms des fichiers grilles à générer
        """
#        print "GetNomGrilles"
        prj = self.projet.GetProjetRef()
#        print prj
#        print prj.grilles
        #
        # Création des noms des fichiers grilles
        #
        # Par défaut = chemin du fichier .prj
        if path == None:
            path = os.path.dirname(self.projet.GetApp().fichierCourant)
            
        nomFichiers = {} 
        for part, g in prj.parties.items():
            prefixe = "Grille_"+g
            gr = prj.grilles[part]
#            print gr
            if grilles.EXT_EXCEL != None:
#                extention = os.path.splitext(ref.grilles_prj[k][0])[1]
                extention = grilles.EXT_EXCEL
                
                if gr[1] == 'C': # fichier "Collectif"
                    nomFichiers[part] = os.path.join(path, self.projet.getNomFichierDefaut(prefixe)) + extention
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
            if not self.projet.TesterExistanceGrilles({0:nomFichiers}):
                return
            
#        print "  Fichiers :", nomFichiers
        
        prj = self.projet.GetProjetRef()
        
        #
        # Ouverture (et pré-sauvegarde) des fichiers grilles "source" (tableaux Excel)
        #
        tableaux = {}
        for k, f in nomFichiers.items():
            if os.path.isfile(f):
                tableaux[k] = grilles.getTableau(self.projet.GetApp(), f)
            else:
                tableaux[k] = grilles.getTableau(self.projet.GetApp(),
                                                 prj.grilles[k][0])
            
            if tableaux[k] != None: # and tableaux[k].filename !=f:
#                print "      créé :", f
                try:
                    tableaux[k].save(f, ConflictResolution = 2)
                except:
                    messageErreur(self.projet.GetApp(), u"Erreur !",
                                  u"Impossible d'enregistrer le fichier\n\n%s\nVérifier :\n" \
                                  u" - qu'aucun fichier portant le même nom n'est déja ouvert\n" \
                                  u" - que le dossier choisi n'est pas protégé en écriture"%f)

        if tableaux == None:
            return
        
        #
        # Remplissage des grilles
        #
        if "beta" in version.__version__:
            grilles.modifierGrille(self.projet, tableaux, self)
        else:
            try:
                grilles.modifierGrille(self.projet, tableaux, self)
            except:
                messageErreur(self.projet.GetApp(), u"Erreur !",
                              u"Impossible de modifier les grilles !") 


        #
        # Enregistrement final des grilles
        #
        for k, t in tableaux.items():
            try:
                t.save()
            except:
                messageErreur(self.projet.GetApp(), u"Erreur !",
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
            if len(tableaux)>1:
                t = u"Génération des grilles réussie !"
            else:
                t = u"Génération de la grille réussie !"
            t += u"\n\n"
            t += u"\n".join(nomFichiers.values())
            
            messageInfo(self.projet.GetApp(), t, u"Génération réussie")
            
        
        self.panelPropriete.MiseAJour()
        
        
    ######################################################################################  
    def GetEvaluabilite(self, complet = False):
        """ Renvoie l'évaluabilité
            % conduite
            % soutenance
        """ 
#        print "GetEvaluabilite", self
        prj = self.GetProjetRef()
#        dicPoids = self.GetReferentiel().dicPoidsIndicateurs_prj
        dicIndicateurs = self.GetDicIndicateurs()
#        print "dicIndicateurs", dicIndicateurs
        tousIndicateurs = prj._dicIndicateurs
#        lstGrpIndicateur = {'R' : prj._dicGrpIndicateur['R'],
#                            'S' : self.GetProjetRef()._dicGrpIndicateur['S']}
#        print lstGrpIndicateur
        
#        r, s = 0, 0
#        ler, les = {}, {}
        
#        rs = [0, 0]
#        lers = [{}, {}]
        
        rs = {}
        lers = {}
        for ph in prj._dicGrpIndicateur.keys():
            lers[ph] = {}
            rs[ph] = 0
    
        def getPoids(listIndic, comp, poidsGrp):
            """ 
            """
#            print "getPoids", listIndic, comp, poidsGrp
            for ph in prj._dicGrpIndicateur.keys():
                if grp in prj._dicGrpIndicateur[ph]:
                    for i, indic in enumerate(listIndic):
                        if comp in dicIndicateurs.keys():
                            if dicIndicateurs[comp][i]:
#                                print "  comp", grp, comp, i, indic.poids, ph
                                poids = indic.poids
                                if ph in poids.keys():
                                    p = 1.0*poids[ph]/100
                                    rs[ph] += p * poidsGrp[ph]/100
                                    if grp in lers[ph].keys():
                                        lers[ph][grp] += p
                                    else:
                                        lers[ph][grp] = p
                        else:
                            if not grp in lers[ph].keys():
                                lers[ph][grp] = 0
                            
            return
        
        
        for grp, grpComp in tousIndicateurs.items():
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
        for t in prj._dicGrpIndicateur.keys():
#            if t in classeurs:
#            print "aColNon", self.GetReferentiel().aColNon
            if t in self.GetReferentiel().aColNon.keys() and self.GetReferentiel().aColNon[t]:
                seuil[t] = 0.5  # s'il y a une colonne "non", le seuil d'évaluabilité est de 50% par groupe de compétence
            else:
                seuil[t] = 1.0     # s'il n'y a pas de colonne "non", le seuil d'évaluabilité est de 100% par groupe de compétence
        
        ev = {}
        ev_tot = {}
#        for txt, le, ph in zip([r, s], [ler, les], prj._dicGrpIndicateur.keys()):
        for part in prj._dicGrpIndicateur.keys():
            txt = rs[part]
            txt = round(txt, 6)
            ev[part] = {}
            ev_tot[part] = [txt, True]
            for grp, tx in lers[part].items():
                tx = round(tx, 6)
                ev[part][grp] = [tx, tx >= seuil[part]]
                ev_tot[part][1] = ev_tot[part][1] and ev[part][grp][1]
        
#        print "   ", ev, ev_tot, seuil
        return ev, ev_tot, seuil
        
        
#        if complet:
#            return r, s, ler, les
#        else:
#            return r, s
    

    ######################################################################################  
    def GetCompetences(self):
        lst = []
        for t in self.projet.taches:
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
        for t in self.projet.taches: # Toutes les tâches du projet
            if not t.phase in TOUTES_REVUES_SOUT:
                if self.id in t.eleves:     # L'élève est concerné par cette tâche
                    indicTache = t.GetDicIndicateurs() # Les indicateurs des compétences à mobiliser pour cette tâche
                    for c, i in indicTache.items():
                        if c in indicateurs.keys():
                            indicateurs[c] = [x or y for x, y in zip(indicateurs[c], i)]
                        else:
                            indicateurs[c] = i
                
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
        for t in self.projet.taches: # Toutes les tâches du projet
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
        for t in self.projet.taches:
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
                          functools.partial(self.projet.SupprimerEleve, item = itemArbre), 
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
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.MiseAJourTypeEnseignement()
    
    
    ######################################################################################  
    def MiseAJourCodeBranche(self):
        """ Met à jour les tags de durée de projet
            et d'évaluabilité
        """
#        print "MiseAJourCodeBranche", self

        #
        # Durée
        #
        duree = int(self.GetDuree())
        lab = " ("+str(duree)+"h) "
        self.codeBranche.SetLabel(lab)
        tol1 = constantes.DELTA_DUREE
        tol2 = constantes.DELTA_DUREE2
        if abs(duree-70) < tol1:
            self.codeBranche.SetBackgroundColour(COUL_OK)
            self.codeBranche.SetToolTipString(u"Durée de travail conforme")
        elif abs(duree-70) < tol2:
            self.codeBranche.SetBackgroundColour(COUL_BOF)
            self.codeBranche.SetToolTipString(u"Durée de travail acceptable")
        else:
            self.codeBranche.SetBackgroundColour(COUL_NON)
            if duree < 70:
                self.codeBranche.SetToolTipString(u"Durée de travail insuffisante")
            else:
                self.codeBranche.SetToolTipString(u"Durée de travail trop importante")
        
        #
        # Evaluabilité
        #
#        er, es , ler, les = self.GetEvaluabilite(complet = True)
        ev, ev_tot, seuil = self.GetEvaluabilite()
        
        for part in self.GetProjetRef()._dicGrpIndicateur.keys():
            self.codeBranche.comp[part].SetLabel(rallonge(pourCent2(ev_tot[part][0])))
        
        keys = sorted(self.GetProjetRef()._dicIndicateurs_simple.keys())
        if "O8s" in keys:
            keys.remove("O8s")
        
        t1 = u"L'élève ne mobilise pas suffisamment de compétences pour être évalué"
        t21 = u"Le "
        t22 = u"Les "
        t3 = u"taux d'indicateurs évalués pour "
        t4 = u" est inférieur à "
        t51 = u"la compétence "
        t52 = u"les compétences "
        
#        for ph, nomph, st in zip(['R', 'S'], [u"conduite", u"soutenance"], [self.evaluR, self.evaluS]):
        for ph, nomph in self.GetProjetRef().parties.items():
            st = self.codeBranche.comp[ph]
            t = u"Evaluabilité de la "+nomph+u" du projet "
            tt = u""
            if ev_tot[ph][1]:
                tt += u"\n" + t1
        
            le = [k for k in ev[ph].keys() if ev[ph][k] == False] # liste des groupes de compétences pas évaluable
            if len(le) == 1:
                tt += u"\n" + t21 + t3 + t51 + le[0] + t4 + pourCent2(seuil[ph])
            else:
                tt += u"\n" + t22 + t3 + t52 + " ".join(le) + t4 + pourCent2(seuil[ph])
        
            if ev_tot[ph][1]:
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
    def GetFicheHTML(self):
#        print "GetFicheHTML"
#        print self.GetProjetRef().listeParties
        dic = {}
        ligne = []
        for ph in self.GetProjetRef().listeParties:
            dic['coul'] = constantes.GetCouleurHTML(COUL_PARTIE[ph])
            dic['nom'] = self.GetProjetRef().parties[ph]
            dic['id'] = ph
            ligne.append("""<tr  id = "le%(id)s" align="right" valign="middle" >
<td><font color = "%(coul)s"><em>%(nom)s :</em></font></td>
</tr>""" %dic)
        
        
        BASE_FICHE_HTML = u"""<?xml version="1.0" encoding="utf-8"?><HTML>
    <p style="text-align: center;"><font size="12"><b>Elève</b></font></p>
<p id="nom">Nom-Prénom</p>
<p id="av"></p>
<table border="0">
<tbody>
<tr id = "ld" align="right" valign="middle">
<td width="110"><span style="text-decoration: underline;">Durée d'activité :</span></td>
</tr>

<tr  id = "le" align="right" valign="middle">
<td><span style="text-decoration: underline;">Evaluabilité :</span></td>
<td></td>
</tr>"""
        for l in ligne:
            BASE_FICHE_HTML += l+"\n"

        BASE_FICHE_HTML +="""
</tbody>
</table>
</HTML>
"""
        return BASE_FICHE_HTML




    ######################################################################################  
    def SetTip2(self):
#        print "SetTip2", self
        # Tip
        if hasattr(self, 'tip'):
            
#            self.tip.SetTexte(self.GetNomPrenom(), self.tip_nom)
            coulOK = constantes.GetCouleurHTML(COUL_OK)
            coulNON = constantes.GetCouleurHTML(COUL_NON)
            
            #
            # Durée
            #
            duree = self.GetDuree()
            lab = draw_cairo.getHoraireTxt(duree)
            if abs(duree-70) < constantes.DELTA_DUREE:
                coul = coulOK
            elif abs(duree-70) < constantes.DELTA_DUREE2:
                coul = constantes.GetCouleurHTML(COUL_BOF)
            else:
                coul = coulNON
            XML_AjouterCol(self.ficheXML, "ld", lab, coul, bold = True)
#            SetWholeText(self.ficheXML, "d", lab)
#            self.tip.SetTexte(rallonge(lab), self.tip_duree)
            
            #
            # Evaluabilité
            #
            ev, ev_tot, seuil = self.GetEvaluabilite()
            
            keys = sorted(self.GetProjetRef()._dicIndicateurs.keys())
#            if "O8s" in keys:
#                keys.remove("O8s")
            lab = {}
            for part in self.GetProjetRef()._dicGrpIndicateur.keys():
                lab[part] = [[pourCent2(ev_tot[part][0], True), True]]
    #            totalOk = True
                for k in keys:
                    if k in self.GetProjetRef()._dicGrpIndicateur[part]:
                        if k in ev[part].keys():
                            
    #                        totalOk = totalOk and (ler[k] >= 0.5)
                            lab[part].append([pourCent2(ev[part][k][0], True), ev[part][k][1]]) 
                        else:
    #                        totalOk = False
                            lab[part].append([pourCent2(0, True), False]) 
                    else:
                        lab[part].append(["", True])
                lab[part][0][1] = ev_tot[part][1]#totalOk and (er >= 0.5)
 
            for part in self.GetProjetRef()._dicGrpIndicateur.keys():
#                print "   ", part
                for i, lo in enumerate(lab[part]):
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
                    XML_AjouterCol(self.ficheXML, "le"+part, l, coul, constantes.GetCouleurHTML(COUL_PARTIE[part]), size, bold)

            for t in keys:
                XML_AjouterCol(self.ficheXML, "le", t, size = 2) 
            #print "   ", self.ficheXML.toxml()
            self.tip.SetPage(self.ficheXML.toxml())
            

            
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = GUI.CodeBranche(self.arbre)
        for part in self.GetProjetRef()._dicGrpIndicateur.keys():
            self.codeBranche.Add(part)
        
#        if self.image == None or self.image == wx.NullBitmap:
        image = self.arbre.images[self.code]
#        else:
#            image = self.image.ConvertToImage().Scale(20, 20).ConvertToBitmap()
        self.branche = arbre.AppendItem(branche, "", data = self, wnd = self.codeBranche,
                                        image = image)
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
        
        self.SetCode()
        
        
        
####################################################################################
#
#   Classe définissant les propriétés d'un professeur
#
####################################################################################
class Prof(Personne):
    def __init__(self, projet, panelParent, ident = 0):
        self.titre = u"prof"
        self.code = "Prf"
        self.discipline = "Tec"
        self.referent = False
        
        Personne.__init__(self, projet, panelParent, ident)
        
        
    ######################################################################################  
    def GetFicheHTML(self):
        return """<HTML>
        <p style="text-align: center;"><font size="12"><b>Professeur</b></font></p>
        <p id="nom">NomPrénom</p>
        <p id="av"></p>
        <table border="0" width="300">
        <tbody>
        <tr id="spe" align="right" valign="top">
        <td width="110"><span style="text-decoration: underline;">Spécialité :</span></td>
        </tr>
        </tbody>
        </table>
        </HTML>
        """
        
        
    ######################################################################################  
    def SetDiscipline(self, discipline):
        self.discipline = discipline
        self.SetTip()
        self.MiseAJourCodeBranche()
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.projet.app.AfficherMenuContextuel([[u"Supprimer", 
                                                     functools.partial(self.projet.SupprimerProf, item = itemArbre), 
                                                     images.Icone_suppr_prof.GetBitmap()]])
        
    ######################################################################################  
    def MiseAJourCodeBranche(self):
        self.arbre.SetItemBold(self.branche, self.referent)
        if self.discipline <> 'Tec':
            self.codeBranche.SetLabel(u" "+constantes.CODE_DISCIPLINES[self.discipline]+u" ")
            self.codeBranche.SetBackgroundColour(constantes.GetCouleurWx(constantes.COUL_DISCIPLINES[self.discipline]))
            self.codeBranche.SetToolTipString(constantes.NOM_DISCIPLINES[self.discipline])
        else:
            self.codeBranche.SetLabel(u"")
            self.codeBranche.SetBackgroundColour(constantes.GetCouleurWx(constantes.COUL_DISCIPLINES[self.discipline]))
            self.codeBranche.SetToolTipString(constantes.NOM_DISCIPLINES[self.discipline])
        
        self.codeBranche.LayoutFit()
    
    ######################################################################################  
    def SetTip2(self):
        if hasattr(self, 'tip'):
            if self.discipline != 'Tec':
                coul = constantes.GetCouleurHTML(constantes.COUL_DISCIPLINES[self.discipline])
            else:
                coul = None
            XML_AjouterCol(self.ficheXML, "spe", constantes.NOM_DISCIPLINES[self.discipline], bcoul = coul)
            self.tip.SetPage(self.ficheXML.toxml())
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = GUI.CodeBranche(arbre)
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
        if hasattr(self, 'tip'):
            self.tip.SetBranche(self.branche)
        self.SetCode()



server = None
if __name__ == '__main__':
    if sys.platform == "win32":
        import serveur
        import socket
        HOST, PORT = socket.gethostname(), 61955
        
        print "HOST :", HOST
        # On teste si pySequence est déja ouvert ...
        #  = demande de connection au client (HOST,PORT) accéptée
        try:
            if len(sys.argv) > 1:
                arg = sys.argv[1]
            else:
                arg = ''
            serveur.client(HOST, PORT, arg)
            sys.exit()
            
        except socket.error: #socket.error: [Errno 10061] Aucune connexion n'a pu être établie car l'ordinateur cible l'a expressément refusée
            # On démarre une nouvelle instance de pySequence
            # = La demande de connection au client (HOST,PORT) a été refusée
            try :
                server = serveur.start_server(HOST, PORT)
            except: # socket.error: [Errno 10013] Une tentative d’accès à un socket de manière interdite par ses autorisations d’accès a été tentée 
                # L'accés a été refusé ... problème de pare-feu ??
                pass 
            app = GUI.SeqApp(False)
            app.MainLoop()

    else:
        app = GUI.SeqApp(False)
        app.MainLoop()
    

