#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sequence.py
Aide é la réalisation de fiches pédagogiques de séquence
*************
*   STIDD   *
*************
Copyright (C) 2011  
@author: Cedrick FAURY

"""
####################################################################################
#
#   Import des modules nécessaires
#
####################################################################################
# Outils "systéme"
import sys, os

# GUI
import wx

# Graphiques vectoriels
try:
    import wx.lib.wxcairo
    import cairo
    haveCairo = True
except ImportError:
    haveCairo = False

# Arbre
try:
    from agw import customtreectrl as CT
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.customtreectrl as CT

# Gestionnaire de pane
try:
    from agw import aui
except ImportError:
    import wx.lib.agw.aui as aui

# Pour passer des arguments aux callback
import functools
    
# Pour enregistrer en xml
import xml.etree.ElementTree as ET

# des widgets wx évolués "faits maison"
from CedWidgets import Variable, VariableCtrl, VAR_REEL_POS, EVT_VAR_CTRL




####################################################################################
#
#   Définition des constantes
#
####################################################################################
CentresInterets = [u"Développement durable et compétitivité des produits",
                   u"Design, créativité et innovation",
                   u"Caractéristiques des matériaux et structures",
                   u"Solutions constructives des matériaux et des structures",
                   u"Dimensionnement des structures et choix des matériaux",
                   u"Efficacité énergétique liée au comportement des matériaux et des structures",
                   u"Formes et caractéristiques de l'énergie",
                   u"Organisation structurelle et solutions constructives des chaînes d'énergie",
                   u"Amélioration de l'efficacité énergétique dans les chaînes d'énergie",
                   u"Amélioration de la gestion de l'énergie",
                   u"Formes et caractéristiques de l'information",
                   u"Organisation structurelle et solutions constructives des chaînes d'information",
                   u"Commande temporelle des systémes",
                   u"Informations liées au comportement des matériaux et des structures",
                   u"Optimisation des paramètres par simulation globale"
                   ]
    
    
Competences = {"CO1.1" : u"Justifier les choix des matériaux, des structures d'un système et les énergies mises en oeuvre dans une approche de développement durable",
               "CO1.2" : u"Justifier le choix d'une solution selon des contraintes d'ergonomie et d'effets sur la santé de l'homme et du vivant",
               "CO2.1" : u"Identifier les flux et la forme de l'énergie, caractériser ses transformations et/ou modulations et estimer l'efficacité énergétique globale d'un système",
               "CO2.2" : u"Justifier les solutions constructives d'un systéme au regard des impacts environnementaux et économiques engendrés tout au long de son cycle de vie",
               "CO3.1" : u"Décoder le cahier des charges fonctionnel d'un système",
               "CO3.2" : u"Evaluer la compétitivité d'un système d'un point de vue technique et économique",
               "CO4.1" : u"Identifier et caractériser les fonctions et les constituants d'un système ainsi que ses entrées/sorties",
               "CO4.2" : u"Identifier et caractériser l'agencement  matériel et/ou logiciel d'un système", 
               "CO4.3" : u"Identifier et caractériser le fonctionnement temporel d'un système",
               "CO4.4" : u"Identifier et caractériser des solutions techniques relatives aux matériaux, à la structure, à l'énergie et aux informations (acquisition, traitement, transmission) d'un système",
               "CO5.1" : u"Expliquer des éléments d'une modélisation proposée relative au comportement de tout ou partie d'un système",
               "CO5.2" : u"Identifier des variables internes et externes utiles à une modélisation, simuler et valider le comportement du modèle",
               "CO5.3" : u"Evaluer un écart entre le comportement du réel et le comportement du modèle en fonction des paramètres proposés",
               "CO6.1" : u"Décrire une idée, un principe, une solution, un projet en utilisant des outils de représentation adaptés",
               "CO6.2" : u"Décrire le fonctionnement et/ou l'exploitation d'un système en utilisant l'outil de description le plus pertinent",
               "CO6.3" : u"Présenter et argumenter des démarches, des résultats, y compris dans une langue étrangère",
               }


TypesActivite = {"ED" : u"Activité d'étude de dossier",
                 "AP" : u"Activité pratique",
                 "P" : u"Activité de projet",
                }

TypesSeance = {"C" : u"Cours",
               "SA" : u"Synthèse d'activité",
               "SS" : u"Synthèse de séquence",
               "E" : u"Evaluation",
               }
TypesSeance.update(TypesActivite)
TypesSeance.update({"R" : u"Rotation d'activités",
                    "S" : u"Série d'activités"})

listeTypeSeance = ["ED", "AP", "P", "C", "SA", "SS", "E", "R", "S"]

Effectifs = {"C" : [u"Classe entière",      32],
             "G" : [u"Effectif réduit",     16],
             "D" : [u"Demi-groupe",         8],
             "E" : [u"Etude et Projet",     4],
             "P" : [u"Activité Pratique",   2],
             }

####################################################################################
#
#   Classe définissant les propriétés d'une séquence
#
####################################################################################
Titres = [u"Séquence pédagogique",
          u"Objectifs pédagogiques",
          u"Séances"]

class Sequence():
    def __init__(self, app, panelParent, intitule = u""):
        self.intitule = intitule
        self.panelPropriete = PanelPropriete_Sequence(panelParent, self)
        
        self.CI = CentreInteret(self, panelParent)
        
        self.obj = [Competence(self, panelParent)]
        
        self.seance = [Seance(self, panelParent)]
        
        self.panelParent = panelParent
        self.app = app
        
        #
        # Données pour le tracé
        #
        self.posIntitule = (0.8, 0.1)
        self.posCI = (0.1, 0.1)
        
        
    ######################################################################################  
    def SetText(self, text):
        self.intitule = text
        
    
    ######################################################################################  
    def AjouterSeance(self, event = None):
        seance = Seance(self, self.panelParent)
        self.seance.append(seance)
        seance.ConstruireArbre(self.arbre, self.brancheSce)
        return seance
    
    ######################################################################################  
    def AjouterObjectif(self, event = None):
        obj = Competence(self, self.panelParent)
        self.obj.append(obj)
        obj.ConstruireArbre(self.arbre, self.brancheObj)
        return
    
    
    
    ######################################################################################  
    def SupprimerObjectif(self, event = None, item = None):
        if len(self.obj) > 1:
            comp = self.arbre.GetItemPyData(item)
            self.obj.remove(comp)
            self.arbre.Delete(item)
        
    
    ######################################################################################  
    def SupprimerSeance(self, seance):
        if len(self.seance) > 1:
            self.seance.remove(seance)
            return True
        return False
    
    
    ######################################################################################  
    def AjouterRotation(self, seance):
        seanceR1 = Seance(self.panelParent)
        seance.rotation.append(seanceR1)
        return seanceR1
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre):
        self.arbre = arbre
        self.branche = arbre.AddRoot(Titres[0], data = self)

        self.CI.ConstruireArbre(arbre, self.branche)
        
        self.brancheObj = arbre.AppendItem(self.branche, Titres[1])
        for obj in self.obj:
            obj.ConstruireArbre(arbre, self.brancheObj)
            
        
        self.brancheSce = arbre.AppendItem(self.branche, Titres[2])
        for sce in self.seance:
            sce.ConstruireArbre(arbre, self.brancheSce)    
            
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):    
        """ Affiche le menu contextuel associé é la séquence
            ... ou bien celui de itemArbre concerné ...
        """
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([[u"Enregistrer", self.app.commandeEnregistrer]])
            
        
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Competence):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Seance):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif self.arbre.GetItemText(itemArbre) == Titres[1]: # Objectifs pédagogiques
            self.app.AfficherMenuContextuel([[u"Ajouter une compétence", self.AjouterObjectif]])
            
            
        elif self.arbre.GetItemText(itemArbre) == Titres[2]: # Séances
            self.app.AfficherMenuContextuel([[u"Ajouter une séance", self.AjouterSeance]])
            
            
    def Redessiner(self):
        self.app.ficheSeq.Redessiner()
        
        
    def Draw(self, ctx):
        print "Draw séquence"
        #
        #  Bordure
        #
        ctx.set_line_width(0.1)
        ctx.set_source_rgb(0, 0, 0)
        ctx.rectangle(0, 0, 1, 1)
        
        
        #
        #  Intitulé de la séquence
        #
        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                     cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(0.05)
        ctx.move_to(self.posIntitule[0], self.posIntitule[1])
        ctx.set_source_rgb(0, 0, 0)
        ctx.show_text(self.intitule)


        ctx.set_line_width(0.01)
        ctx.move_to(0.1, 0.1)
        ctx.line_to(0.2, 0.2)
        ctx.rel_line_to(0.5, 0.1)
        ctx.close_path()
        ctx.set_source_rgba(0, 0, 0.5, 1)
        
#        self.CI.Draw(ctx, self.posCI)
        
        ctx.stroke()
        
####################################################################################
#
#   Classe définissant les propriétés d'une séquence
#
####################################################################################
class CentreInteret():
    def __init__(self, parent, panelParent, numCI = 0):
        
        self.SetNum(numCI)
        
        self.panelPropriete = PanelPropriete_CI(panelParent, self)
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du centre d'intérét pour enregistrement
        """
        root = ET.Element(self.code)
        return root
    
    ######################################################################################  
    def SetNum(self, num):
        self.num = num
        self.code = "CI"+str(self.num+1)
        self.CI = CentresInterets[self.num]
        
        if hasattr(self, 'arbre'):
            self.SetCode()
        
    ######################################################################################  
    def SetCode(self):
        self.codeBranche.SetLabel(self.code)
        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Centre d'intérét :", wnd = self.codeBranche, data = self)
        
    ######################################################################################  
    def Draw(self, ctx, pos):
        #/* a custom shape, that could be wrapped in a function */
        x0       = pos[0]   #/*< parameters like cairo_rectangle */
        y0       = pos[0]
        rect_width  = 0.2
        rect_height = 0.2
        radius = 0.05   #/*< and an approximate curvature radius */
        
        x1=x0+rect_width
        y1=y0+rect_height
        #if (!rect_width || !rect_height)
        #    return
        if rect_width/2<radius:
            if rect_height/2<radius:
                ctx.move_to  (x0, (y0 + y1)/2)
                ctx.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
                ctx.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
                ctx.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
                ctx.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
            else:
                ctx.move_to  (x0, y0 + radius)
                ctx.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
                ctx.curve_to (x1, y0, x1, y0, x1, y0 + radius)
                ctx.line_to (x1 , y1 - radius)
                ctx.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
                ctx.curve_to (x0, y1, x0, y1, x0, y1- radius)
        
        else:
            if rect_height/2<radius:
                ctx.move_to  (x0, (y0 + y1)/2)
                ctx.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
                ctx.line_to (x1 - radius, y0)
                ctx.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
                ctx.curve_to (x1, y1, x1, y1, x1 - radius, y1)
                ctx.line_to (x0 + radius, y1)
                ctx.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
            else:
                ctx.move_to  (x0, y0 + radius)
                ctx.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
                ctx.line_to (x1 - radius, y0)
                ctx.curve_to (x1, y0, x1, y0, x1, y0 + radius)
                ctx.line_to (x1 , y1 - radius)
                ctx.curve_to (x1, y1, x1, y1, x1 - radius, y1)
                ctx.line_to (x0 + radius, y1)
                ctx.curve_to (x0, y1, x0, y1, x0, y1- radius)
        
        ctx.close_path ()
        
        ctx.set_source_rgb (0.5,0.5,1)
        ctx.fill_preserve ()
        ctx.set_source_rgba (0.5,0,0,0.5)
        ctx.stroke ()
        
        #
        # code
        #
        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                     cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(0.05)
        ctx.move_to(pos[0], pos[1])
        ctx.set_source_rgb(0, 0, 0)
        ctx.show_text(self.code)
        
        #
        # intitulé
        #
        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                     cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(0.01)
        ctx.move_to(pos[0], pos[1])
        ctx.set_source_rgb(0, 0, 0)
        ctx.show_text(self.code)
        
####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Competence():
    def __init__(self, parent, panelParent, numComp = 0):
        self.clefs = Competences.keys()
        self.clefs.sort()
        self.parent = parent
        
        
        self.SetNum(numComp)
        
        self.panelPropriete = PanelPropriete_Competence(panelParent, self)
        
        
        
    ######################################################################################  
    def SetNum(self, num):
        self.num = num
        self.code = self.clefs[self.num]
        self.competence = Competences[self.code]
        
        if hasattr(self, 'arbre'):
            self.SetCode()
        
    ######################################################################################  
    def SetCode(self):
        self.codeBranche.SetLabel(self.code)
        
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
        root = ET.Element(self.code)
        return root
    
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Compétence :", wnd = self.codeBranche, data = self)
        
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerObjectif, item = itemArbre)]])
            
            
            
            

####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Seance():
    def __init__(self, parent, panelParent, typeSeance = "C", typeParent = 0):
        """ Séance :
                parent = le parent wx pour contenir "panelPropriete"
                typeSceance = type de séance parmi "TypeSeance"
                typeParent = type du parent de la séance :  0 = séquence
                                                            1 = séance "Rotation"
                                                            2 = séance "Série"
        """
        
        # Les données sauvegardées
        self.ordre = 1
        self.duree = Variable(u"Durée", lstVal = 1.0, nomNorm = "", typ = VAR_REEL_POS, 
                 bornes = [0,8], modeLog = False,
                 expression = None, multiple = False)
        self.intitule  = u""
        self.effectif = "C"
        
        # Les autres données
        self.typeParent = typeParent
        self.parent = parent
        self.panelParent = panelParent
        
        self.SetType(typeSeance)
        
        self.panelPropriete = PanelPropriete_Seance(panelParent, self)
        self.panelPropriete.AdapterAuType()
        
        self.rotation = []
        self.serie = []
        
        
        
    ######################################################################################  
    def GetDuree(self):
        duree = 0
        if self.typeSeance == "R":
            for sce in self.rotation:
                duree += sce.GetDuree()
        elif self.typeSeance == "S":
            duree += self.rotation[0].GetDuree()
        else:
            duree = self.duree.v
        return duree
                
    ######################################################################################  
    def SetDuree(self, duree): 
        print "SetDuree"
        if self.typeSeance == "R" : # Rotation
            d = self.rotation[0].GetDuree()
            pb = False
            print "  R:", d
            for s in self.rotation[1:]:
                if s.GetDuree() != d:
                    pb = True
            if pb :
                self.panelPropriete.MarquerProblemeDuree(False)
            else:
                self.duree.v = duree
                self.panelPropriete.MarquerProblemeDuree(True)
        
        elif self.typeSeance == "S" : # Serie
            d = self.serie[0].GetDuree()
            pb = False
            print "  S:", d
            for s in self.serie[1:]:
                if s.GetDuree() != d:
                    pb = True
            if pb : 
                self.panelPropriete.MarquerProblemeDuree(False)
            else:
                self.duree.v = duree
                self.panelPropriete.MarquerProblemeDuree(True)
        
    ######################################################################################  
    def SetIntitule(self, text):           
        self.intitule = text
        
    ######################################################################################  
    def SetEffectif(self, text):           
        self.intitule = text   
           
    ######################################################################################  
    def SetType(self, typ):
        if type(typ) == str:
            self.typeSeance = typ
        else:
            self.typeSeance = listeTypeSeance[typ]
            
        self.code = self.typeSeance + str(self.ordre)
    
        if hasattr(self, 'arbre'):
            self.SetCode()
        
        if self.typeSeance in ["R","S"] : # Rotation ou Serie
            self.AjouterSeance()
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.AdapterAuType()
        
        
    ######################################################################################  
    def SetCode(self):
        self.codeBranche.SetLabel(self.code)
        
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la séance pour enregistrement
        """
        root = ET.Element(str(self.ordre))
        root.set("Type", TypesSeance[self.typeSeance])
        root.set("Duree", TypesSeance[self.duree])
        
        if self.typeSeance == "R":
            for sce in self.rotation:
                root.append(sce.getBranche())
        elif self.typeSeance == "S":
            for sce in self.serie:
                root.append(sce.getBranche())
        return root
    
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Séance :", wnd = self.codeBranche, data = self)
        
        
    ######################################################################################  
    def AjouterSeance(self, event = None):
        """ Ajoute une séance é la séance
            !! Uniquement pour les séances de type "Rotation" ou "Serie" !!
        """
        seance = Seance(self, self.panelParent, typeParent = self.typeParent)
        if self.typeSeance == "R" : # Rotation
            self.rotation.append(seance)
            
        elif self.typeSeance == "S" : # Serie
            self.serie.append(seance)
            
        seance.ConstruireArbre(self.arbre, self.branche)



    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            listItems = [[u"Supprimer", functools.partial(self.parent.SupprimerSeance, item = itemArbre)]]
            if self.typeSeance in ["R", "S"]:
                listItems.append([u"Ajouter une séance", self.AjouterSeance])
            self.parent.app.AfficherMenuContextuel(listItems)
#            item2 = menu.Append(wx.ID_ANY, u"Créer une rotation")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterRotation, item = item), item2)
#            
#            item3 = menu.Append(wx.ID_ANY, u"Créer une série")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterSerie, item = item), item3)
            

        


####################################################################################
#
#   Classe définissant le panel conteneur des panels de propriétés
#
####################################################################################    
class PanelConteneur(wx.Panel):    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        self.bsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.bsizer)
        
        #
        # Le panel affiché
        #
        self.panel = None
    
    
    def AfficherPanel(self, panel):
        print "AfficherPanel"
        if self.panel != None:
            self.bsizer.Remove(self.panel)
            self.panel.Hide()
        self.bsizer.Add(panel, flag = wx.EXPAND)
        self.panel = panel
        self.panel.Show()
        self.bsizer.FitInside(self)
        self.bsizer.Layout()
        self.Refresh()
    
####################################################################################
#
#   Classe définissant la fenétre de l'application
#
####################################################################################
class FenetreSequence(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "")

        #
        # Taille et position de la fenétre
        #
        self.SetMinSize((800,570)) # Taille mini d'écran : 800x600
        self.SetSize((1024,738)) # Taille pour écran 1024x768
        # On centre la fenétre dans l'écran ...
        self.CentreOnScreen(wx.BOTH)
        
        
        
        
        # Use a panel under the AUI panes in order to work around a
        # bug on PPC Macs
        pnl = wx.Panel(self)
        self.pnl = pnl
        
        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(pnl)
        
        # panel de propriétés (conteneur)
        panelProp = PanelConteneur(pnl)
        
        
        #
        # La séquence
        #
        self.sequence = Sequence(self, panelProp)
        
        #
        # Arbre de structure de la séquence
        #
        arbreSeq = ArbreSequence(pnl, self.sequence, panelProp)
        
        #
        # Zone graphique de la fiche de séquence
        #
        
#        panelCentral = wx.ScrolledWindow(pnl, -1, style = wx.HSCROLL | wx.VSCROLL | wx.RETAINED)# | wx.BORDER_SIMPLE)
#        sizerCentral = wx.GridSizer(1,1)
        self.ficheSeq = FicheSequence(pnl, self.sequence)
#        panelCentral.SetScrollRate(5,5)
#        sizerCentral.Add(self.ficheSeq, flag = wx.ALIGN_CENTER|wx.ALL)#|wx.EXPAND)
#        panelCentral.SetSizerAndFit(sizerCentral)
        
#        panelCentral.Bind(wx.EVT_SIZE, self.OnSize)
#        self.panelCentral = panelCentral
        
        #
        # Pour la sauvegarde
        #
        self.fichierCourant = ""
        self.DossierSauvegarde = ""
        
        
        #############################################################################################
        # Mise en place de la zone graphique
        #############################################################################################
        self.mgr.AddPane(self.ficheSeq, 
                         aui.AuiPaneInfo().
                         CenterPane()
#                         Caption(u"Bode").
#                         PaneBorder(False).
#                         Floatable(False).
#                         CloseButton(False)
#                         Name("Bode")
#                         Layer(2).BestSize(self.zoneGraph.GetMaxSize()).
#                         MaxSize(self.zoneGraph.GetMaxSize())
                        )

        #############################################################################################
        # Mise en place de l'arbre
        #############################################################################################
        self.mgr.AddPane(arbreSeq, 
                         aui.AuiPaneInfo().
#                         Name(u"Structure").
                         Left().Layer(1).
                         Floatable(False).
                         BestSize((200, -1)).
                         MinSize((200, -1)).
#                         DockFixed().
#                         Gripper(False).
#                         Movable(False).
                         Maximize().
                         Caption(u"Structure").
                         CaptionVisible(True).
#                         PaneBorder(False).
                         CloseButton(False)
#                         Show()
                         )
        
        #############################################################################################
        # Mise en place du panel de propriétés
        #############################################################################################
        self.mgr.AddPane(panelProp, 
                         aui.AuiPaneInfo().
#                         Name(u"Structure").
                         Bottom().Layer(1).
                         Floatable(False).
                         BestSize((200, 200)).
                         MinSize((-1, 200)).
#                         DockFixed().
#                         Gripper(False).
#                         Movable(False).
#                         Maximize().
                         Caption(u"Propriétés").
                         CaptionVisible(True).
#                         PaneBorder(False).
                         CloseButton(False)
#                         Show()
                         )
        

        
        self.mgr.Update()
        
        wx.CallAfter(self.ficheSeq.Redessiner)
        
#        sizer = wx.BoxSizer(wx.HORIZONTAL)
#        self.SetSizerAndFit(sizer)
    
    
    ###############################################################################################
    def OnSize(self, event):
        print "OnSize fenetre",
        w = self.panelCentral.GetClientSize()[0]
        print w
        self.panelCentral.SetVirtualSize((w,w*29/21)) # Mise au format A4
#        self.ficheSeq.FitInside()
        
        
    ###############################################################################################
    def enregistrer(self, nomFichier):

        wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
        fichier = file(nomFichier, 'w')
        
        # Création de la racine
        sequence = ET.Element("Sequence")
        sequence.set("Intitule", self.sequence.intitule)
        
        
        ci = ET.SubElement(sequence, "Centre d'interet")
        ci.append(self.sequence.CI.getBranche())
        
        objectifs = ET.SubElement(sequence, "Objectifs")
        for obj in self.sequence.obj:
            objectifs.append(obj.getBranche())
            
        seances = ET.SubElement(sequence, "Seances")
        for sce in self.sequence.seance:
            seances.append(sce.getBranche())
        
        indent(sequence)
        ET.ElementTree(sequence).write(fichier)
        fichier.close()
        self.definirNomFichierCourant(nomFichier)
        wx.EndBusyCursor()
        
    
    #############################################################################
    def dialogEnregistrer(self):
        mesFormats = "Séquence (.seq)|*.seq|" \
                     "Tous les fichiers|*.*'"
        dlg = wx.FileDialog(
            self, message=u"Enregistrer la séquence sous ...", defaultDir=self.DossierSauvegarde , 
            defaultFile="", wildcard=mesFormats, style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR
            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
            self.enregistrer(path)
            self.DossierSauvegarde = os.path.split(path)[0]
#            print "Nouveau dossier de sauvegarde", self.DossierSauvegarde
        else:
            dlg.Destroy()
            
    #############################################################################
    def commandeEnregistrer(self, event = None):
#        print "fichier courant :",self.fichierCourant
        if self.fichierCourant != '':
            s = u"'Oui' pour enregistrer la séquence dans le fichier\n"
            s += self.fichierCourant
            s += ".\n\n"
            s += u"'Non' pour enregistrer la séquence dans un autre fichier."
            
            dlg = wx.MessageDialog(self, s,
                                   u'Enregistrement',
                                     wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                     )
            res = dlg.ShowModal()
            dlg.Destroy() 
            if res == wx.ID_YES:
                self.enregistrer(self.fichierCourant)
            elif res == wx.ID_NO:
                self.dialogEnregistrer()
            
            
        else:
            self.dialogEnregistrer()
            
            
    #############################################################################
    def getNomFichierCourantCourt(self):
        return os.path.splitext(os.path.split(self.fichierCourant)[-1])[0]
        
    #############################################################################
    def definirNomFichierCourant(self, nomFichier = '', modif = False):
#        if modif : print "Fichier courant modifié !"
        self.fichierCourant = nomFichier
        self.fichierCourantModifie = modif
        if self.fichierCourant == '':
            t = ''
        else:
            t = ' - ' + self.fichierCourant
        if modif : 
            t += " **"
        self.SetTitle("Séquence" + t )

    #############################################################################
    def MarquerFichierCourantModifie(self):
        self.definirNomFichierCourant(self.fichierCourant, True)
        
        
    #############################################################################
    def AfficherMenuContextuel(self, items):
        """ Affiche un menu contextuel contenant les items spécifiés
                items = [ [nom1, fct1], [nom2, fct2], ...]
        """
        menu = wx.Menu()
        
        for nom, fct in items:
            item1 = menu.Append(wx.ID_ANY, nom)
            self.Bind(wx.EVT_MENU, fct, item1)
        
        self.PopupMenu(menu)
        menu.Destroy()
       
####################################################################################
#
#   Classe définissant la fenétre de la fiche de séquence
#
####################################################################################


class FicheSequence(wx.ScrolledWindow):
    def __init__(self, parent, sequence):
#        wx.Panel.__init__(self, parent, -1)
        wx.ScrolledWindow.__init__(self, parent, -1, style = wx.VSCROLL | wx.RETAINED)
        self.sequence = sequence
        self.EnableScrolling(False, True)
        self.SetScrollbars(20, 20, 50, 50);
#        self.InitBuffer()
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    #############################################################################            
    def OnResize(self, evt):
        print "OnSize fiche",
        w = self.GetClientSize()[0]
        print w
        self.SetVirtualSize((w,w*29/21)) # Mise au format A4
#        self.ficheSeq.FitInside()

        self.InitBuffer()



    #############################################################################            
    def OnPaint(self, evt):
#        print "PAINT"
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

#        self.Redessiner()
        
        
    #############################################################################            
    def InitBuffer(self):
        w,h = self.GetVirtualSize()
        print "InitBuffer", w, h
        self.buffer = wx.EmptyBitmap(w,h)

        
    #############################################################################            
    def Redessiner(self):  
        print "REDESSINER"
        cdc = wx.ClientDC(self)
        dc = wx.BufferedDC(cdc, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        ctx = wx.lib.wxcairo.ContextFromDC(dc)
        dc.BeginDrawing()
        self.normalize(ctx)
        self.sequence.Draw(ctx)
        dc.EndDrawing()

    #############################################################################            
    def normalize(self, cr):
        w,h = self.GetVirtualSize()
        cr.scale(w, h) 
        print "normalize", w,h
        
        
#    def OnPaint(self, evt = None):
#        #dc = wx.PaintDC(self)
#        dc = wx.BufferedPaintDC(self)
#        dc.SetBackground(wx.Brush('white'))
#        dc.Clear()
#        self.dc = dc
        

    
#    def Render(self):
#        print "Render"
#        
#        # now draw something with cairo
#        ctx = wx.lib.wxcairo.ContextFromDC(self.dc)
#        self.normalize(ctx)
#        
#        self.sequence.Draw(ctx)
        
        


#        # Draw some text
#        face = wx.lib.wxcairo.FontFaceFromFont(
#            wx.FFont(10, wx.SWISS, wx.FONTFLAG_BOLD))
#        ctx.set_font_face(face)
#        ctx.set_font_size(60)
#        ctx.move_to(360, 180)
#        ctx.set_source_rgb(0, 0, 0)
#        ctx.show_text("Hello")

#        # Text as a path, with fill and stroke
#        ctx.move_to(400, 220)
#        ctx.text_path("World")
#        ctx.set_source_rgb(0.39, 0.07, 0.78)
#        ctx.fill_preserve()
#        ctx.set_source_rgb(0,0,0)
#        ctx.set_line_width(2)
#        ctx.stroke()

#        # Show iterating and modifying a (text) path
#        ctx.new_path()
#        ctx.move_to(0, 0)
#        ctx.set_source_rgb(0.3, 0.3, 0.3)
#        ctx.set_font_size(30)
#        text = "This path was warped..."
#        ctx.text_path(text)
#        tw, th = ctx.text_extents(text)[2:4]
#        self.warpPath(ctx, tw, th, 360,300)
#        ctx.fill()

#        ctx.paint()
        
        
    def warpPath(self, ctx, tw, th, dx, dy):
        def f(x, y):
            xn = x - tw/2
            yn = y+ xn ** 3 / ((tw/2)**3) * 70
            return xn+dx, yn+dy

        path = ctx.copy_path()
        ctx.new_path()
        for type, points in path:
            if type == cairo.PATH_MOVE_TO:
                x, y = f(*points)
                ctx.move_to(x, y)

            elif type == cairo.PATH_LINE_TO:
                x, y = f(*points)
                ctx.line_to(x, y)

            elif type == cairo.PATH_CURVE_TO:
                x1, y1, x2, y2, x3, y3 = points
                x1, y1 = f(x1, y1)
                x2, y2 = f(x2, y2)
                x3, y3 = f(x3, y3)
                ctx.curve_to(x1, y1, x2, y2, x3, y3)

            elif type == cairo.PATH_CLOSE_PATH:
                ctx.close_path()
                
                
####################################################################################
#
#   Classe définissant le panel de propriété par défaut
#
####################################################################################
class PanelPropriete(wx.Panel):
    def __init__(self, parent, titre = u"", objet = None):
        wx.Panel.__init__(self, parent, -1, size = (-1, 200), style = wx.BORDER_SIMPLE)
        
#        self.boxprop = wx.StaticBox(self, -1, u"")
        self.bsizer = wx.BoxSizer(wx.VERTICAL)
        self.Hide()
        self.SetSizer(self.bsizer)
        self.SetAutoLayout(True)
       
 



####################################################################################
#
#   Classe définissant le panel de propriété de séquence
#
####################################################################################
class PanelPropriete_Sequence(PanelPropriete):
    def __init__(self, parent, sequence):
        PanelPropriete.__init__(self, parent)
        self.sequence = sequence
        
        textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        self.bsizer.Add(textctrl, flag = wx.EXPAND)
        self.bsizer.Layout()
        
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
    
    def EvtText(self, event):
        self.sequence.SetText(event.GetString())
        self.sequence.Redessiner()
        
####################################################################################
#
#   Classe définissant le panel de propriété du CI
#
####################################################################################
class PanelPropriete_CI(PanelPropriete):
    def __init__(self, parent, CI):
        PanelPropriete.__init__(self, parent)
        self.CI = CI
        
        cb = wx.ComboBox(self, -1, u"Choisir un CI",
                         choices = CentresInterets,
                         style = wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         | wx.CB_READONLY
                         #| wx.CB_SORT
                         )
        self.bsizer.Add(cb, 0, wx.EXPAND)
        self.bsizer.Layout()
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        
    def EvtComboBox(self, event):
        self.CI.SetNum(event.GetSelection())
        
        

####################################################################################
#
#   Classe définissant le panel de propriété de la compétence
#
####################################################################################
class PanelPropriete_Competence(PanelPropriete):
    def __init__(self, parent, competence):
        
        self.competence = competence
        
        
        PanelPropriete.__init__(self, parent)
        
        # Prévoir un truc pour que la liste des compétences tienne compte de celles déja choisies
        # idée : utiliser cb.CLear, Clear.Append ou cb.Delete
        listComp = []
        l = Competences.items()
        for c in l:
            listComp.append(c[0] + " " + c[1])
        listComp.sort()    
        
        cb = wx.ComboBox(self, -1, u"Choisir une compétence",
                         choices = listComp,
                         style = wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         | wx.CB_READONLY
                         #| wx.CB_SORT
                         )
        
        print dir(cb)
        self.bsizer.Add(cb, 0, wx.EXPAND)
        self.bsizer.Layout()
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        
    def EvtComboBox(self, event):
        self.competence.SetNum(event.GetSelection())
        
        
####################################################################################
#
#   Classe définissant le panel de propriété de la séance
#
####################################################################################
class PanelPropriete_Seance(PanelPropriete):
    def __init__(self, parent, seance):
        PanelPropriete.__init__(self, parent)
        self.seance = seance

        
        #
        # Type de séance
        #
        titre = wx.StaticText(self, -1, u"Type =")
        cbType = wx.ComboBox(self, -1, u"Choisir un type de séance",
                         choices = [],
                         style = wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbType)
        self.cbType = cbType
        sizerType = wx.BoxSizer(wx.HORIZONTAL)
        sizerType.Add(titre, 0)
        sizerType.Add(cbType, 1, wx.EXPAND)
        
        #
        # Intitulé de la séance
        #
        titre = wx.StaticText(self, -1, u"Intitulé =")
        textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        self.Bind(wx.EVT_TEXT, self.EvtTextIntitule, textctrl)
        sizerIntitule = wx.BoxSizer(wx.HORIZONTAL)
        sizerIntitule.Add(titre, 0)
        sizerIntitule.Add(textctrl, 1, wx.EXPAND)
        
        #
        # Durée de la séance
        #
        vcDuree = VariableCtrl(self, seance.duree, coef = 0.5, labelMPL = False, signeEgal = True, slider = False, fct = None, help = "")
#        textctrl = wx.TextCtrl(self, -1, u"1")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
        self.vcDuree = vcDuree
        
        #
        # Effectif
        #
        titre = wx.StaticText(self, -1, u"Effectif =")
        cbEff = wx.ComboBox(self, -1, u"Effectif",
                         choices = [],
                         style = wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         | wx.CB_READONLY
                         #| wx.CB_SORT
                         )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxEff, cbEff)
        self.cbEff = cbEff
        
        nombre = wx.StaticText(self, -1, u"")
        self.nombre = nombre
        
        sizerEff = wx.BoxSizer(wx.HORIZONTAL)
        sizerEff.Add(titre, 0)
        sizerEff.Add(cbEff, 0, wx.EXPAND)
        sizerEff.Add(self.nombre, 0)
        
        #
        # Mise en place
        #
        self.bsizer.Add(sizerType, 1, wx.EXPAND)
        self.bsizer.Add(sizerIntitule, 1, wx.EXPAND)
        self.bsizer.Add(vcDuree, 1)
        self.bsizer.Add(sizerEff, 1)
        self.bsizer.Layout()
    
    def EvtTextIntitule(self, event):
        self.seance.SetIntitule(event.GetString())
        
    def EvtText(self, event):
        self.seance.SetDuree(event.GetVar().v)
        if self.seance.parent.typeSeance == "R": # séance en rotation (parent = séance "Rotation")
            self.seance.parent.SetDuree(self.seance.GetDuree())
        
    def EvtComboBox(self, event):
        self.seance.SetType(event.GetSelection())
        
    def EvtComboBoxEff(self, event):
#        print "EvtComboBoxEff", event.GetString()
        self.seance.SetEffectif(event.GetSelection())  
        l = Effectifs.values()
        continuer = True
        i = 0
        while continuer:
            if i>=len(l):
                continuer = False
            else:
                if l[i][0] == event.GetString():
                    n = l[i][1]
                    continuer = False
            i += 1
        self.nombre.SetLabel(u" (" + str(n) + u" éléves)")
#        self.Refresh()
        
    def AdapterAuType(self):
        print "AdapterAuType"
        #  séance "normale" (parent = séquence)
        listType = listeTypeSeance
        if self.seance.typeSeance == "R": #  séance en rotation
            listType = listeTypeSeance[:-1]
        elif self.seance.typeSeance == "S": #  séance en série
            listType = listeTypeSeance[:-2]
        
        listTypeS = []
        for t in listType:
            listTypeS.append(TypesSeance[t])
        
        n = self.cbType.GetSelection()   
        self.cbType.Clear()
        for s in listTypeS:
            self.cbType.Append(s)
        self.cbType.SetSelection(n)
        
        # Durée
        if self.seance.typeSeance == "R": #  séance en rotation
            self.vcDuree.Activer(False)
        elif self.seance.typeSeance == "S": #  séance en série
            self.vcDuree.Activer(False)
        
        # Effectif
        if self.seance.typeSeance in ["C", "E", "SS"]:
            listEff = ["C"]
        elif self.seance.typeSeance in ["R", "S"] or self.seance.typeSeance == "":
            self.cbEff.Enable(False)
            listEff = []
        elif self.seance.typeSeance in ["ED", "P"]:
            listEff = ["G", "D", "E", "P"]
        elif self.seance.typeSeance in ["AP"]:
            listEff = ["P"]
        elif self.seance.typeSeance in ["SA"]:
            listEff = ["C", "G"]
        
#        n = self.cbEff.GetSelection()   
        self.cbEff.Clear()
        for s in listEff:
            self.cbEff.Append(Effectifs[s][0])
        self.cbEff.SetSelection(0)
        
#        self.Refresh()
        
#    def MarquerProblemeDuree(self, etat):
#        return
#        self.vcDuree.marquerValid(etat)
        
####################################################################################
#
#   Classe définissant l'arbre de structure de la séquence
#
####################################################################################

#class ArbreSequence(wx.Treebook):
#    def __init__(self, parent):
#        wx.Treebook.__init__(self, parent, -1, size = (),
#                             style=
#                             #wx.BK_DEFAULT
#                             wx.BK_TOP
#                             #wx.BK_BOTTOM
#                             #wx.BK_LEFT
#                             #wx.BK_RIGHT
#                            )
#
#
#        self.sequence = Sequence()
#        
#        
#        # make an image list using the LBXX images
#        il = wx.ImageList(16, 16)
##        for x in range(12):
##            obj = getattr(images, 'LB%02d' % (x+1))
##            bmp = obj.GetBitmap()
##            il.Add(bmp)
#        self.AssignImageList(il)
##        imageIdGenerator = getNextImageID(il.GetImageCount())
#        
#        #
#        # Intitulé de la séquence
#        #
#        self.AddPage(PanelPropriete_Sequence(self, self.sequence), u"Séquence")
#        
#        
#        #
#        # Centre d'intérét
#        #
#        self.AddSubPage(PanelPropriete_CI(self, self.sequence.CI), u"Centre d'intérét")
#        
#        # Now make a bunch of panels for the list book
##        first = True
##        for colour in colourList:
##            win = self.makeColorPanel(colour)
##            self.AddPage(win, colour, imageId=imageIdGenerator.next())
##            if first:
##                st = wx.StaticText(win.win, -1,
##                          "You can put nearly any type of window here,\n"
##                          "and the wx.TreeCtrl can be on either side of the\n"
##                          "Treebook",
##                          wx.Point(10, 10))
##                first = False
##
##            win = self.makeColorPanel(colour)
##            st = wx.StaticText(win.win, -1, "this is a sub-page", (10,10))
##            self.AddSubPage(win, 'a sub-page', imageId=imageIdGenerator.next())
#
##        self.Bind(wx.EVT_TREEBOOK_PAGE_CHANGED, self.OnPageChanged)
##        self.Bind(wx.EVT_TREEBOOK_PAGE_CHANGING, self.OnPageChanging)
#
#        # This is a workaround for a sizing bug on Mac...
##        wx.FutureCall(100, self.AdjustSize)

class ArbreSequence(CT.CustomTreeCtrl):
    def __init__(self, parent, sequence, panelProp,
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.SUNKEN_BORDER|wx.WANTS_CHARS,
                 agwStyle = CT.TR_HAS_BUTTONS|CT.TR_HAS_VARIABLE_ROW_HEIGHT,
                 ):

        CT.CustomTreeCtrl.__init__(self, parent, -1, pos, size, style, agwStyle)
        
        self.parent = parent
        
        #
        # La séquence 
        #
        self.sequence = sequence
        
        #
        # Le panel contenant les panel de propriétés des éléments de séquence
        #
        self.panelProp = panelProp
        
        
        #
        # Les icones des branches
        #
        il = wx.ImageList(16, 16)
#        for items in ArtIDs[1:-1]:
#            bmp = wx.ArtProvider_GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
#            il.Add(bmp)

#        smileidx = il.Add(images.Smiles.GetBitmap())
#        numicons = il.GetImageCount()
        self.AssignImageList(il)
        
        #
        # On instancie un panel de propriétés vide pour les éléments qui n'ont pas de propriétés
        #
        self.panelVide = PanelPropriete(self.panelProp)
        self.panelVide.Hide()
        
        #
        # Construction de l'arbre
        #
        self.sequence.ConstruireArbre(self)
        
        #
        # Gestion des évenements
        #
        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(CT.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightDown)
        
        self.ExpandAll()
        

#        textctrl = wx.TextCtrl(self, -1, "I Am A Simple\nMultiline wx.TexCtrl", style=wx.TE_MULTILINE)
#        self.gauge = wx.Gauge(self, -1, 50, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
#        self.gauge.SetValue(0)
#        combobox = wx.ComboBox(self, -1, choices=["That", "Was", "A", "Nice", "Holyday!"], style=wx.CB_READONLY|wx.CB_DROPDOWN)
#
#        textctrl.Bind(wx.EVT_CHAR, self.OnTextCtrl)
#        combobox.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
#        lenArtIds = len(ArtIDs) - 2
#
#
#        
#        for x in range(15):
#            if x == 1:
#                child = self.AppendItem(self.root, "Item %d" % x + "\nHello World\nHappy wxPython-ing!")
#                self.SetItemBold(child, True)
#            else:
#                child = self.AppendItem(self.root, "Item %d" % x)
#            self.SetPyData(child, None)
#            self.SetItemImage(child, 24, CT.TreeItemIcon_Normal)
#            self.SetItemImage(child, 13, CT.TreeItemIcon_Expanded)
#
#            if random.randint(0, 3) == 0:
#                self.SetItemLeftImage(child, random.randint(0, lenArtIds))
#
#            for y in range(5):
#                if y == 0 and x == 1:
#                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), ct_type=2, wnd=self.gauge)
#                elif y == 1 and x == 2:
#                    last = self.AppendItem(child, "Item %d-%s" % (x, chr(ord("a")+y)), ct_type=1, wnd=textctrl)
#                    if random.randint(0, 3) == 1:
#                        self.SetItem3State(last, True)
#                        
#                elif 2 < y < 4:
#                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)))
#                elif y == 4 and x == 1:
#                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), wnd=combobox)
#                else:
#                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), ct_type=2)
#                    
#                self.SetPyData(last, None)
#                self.SetItemImage(last, 24, CT.TreeItemIcon_Normal)
#                self.SetItemImage(last, 13, CT.TreeItemIcon_Expanded)
#
#                if random.randint(0, 3) == 0:
#                    self.SetItemLeftImage(last, random.randint(0, lenArtIds))
#                    
#                for z in range(5):
#                    if z > 2:
#                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=1)
#                        if random.randint(0, 3) == 1:
#                            self.SetItem3State(item, True)
#                    elif 0 < z <= 2:
#                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=2)
#                    elif z == 0:
#                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z))
#                        self.SetItemHyperText(item, True)
#                    self.SetPyData(item, None)
#                    self.SetItemImage(item, 28, CT.TreeItemIcon_Normal)
#                    self.SetItemImage(item, numicons-1, CT.TreeItemIcon_Selected)
#
#                    if random.randint(0, 3) == 0:
#                        self.SetItemLeftImage(item, random.randint(0, lenArtIds))
#
#        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
#        self.Bind(wx.EVT_IDLE, self.OnIdle)
#
#        self.eventdict = {'EVT_TREE_BEGIN_DRAG': self.OnBeginDrag, 'EVT_TREE_BEGIN_LABEL_EDIT': self.OnBeginEdit,
#                          'EVT_TREE_BEGIN_RDRAG': self.OnBeginRDrag, 'EVT_TREE_DELETE_ITEM': self.OnDeleteItem,
#                          'EVT_TREE_END_DRAG': self.OnEndDrag, 'EVT_TREE_END_LABEL_EDIT': self.OnEndEdit,
#                          'EVT_TREE_ITEM_ACTIVATED': self.OnActivate, 'EVT_TREE_ITEM_CHECKED': self.OnItemCheck,
#                          'EVT_TREE_ITEM_CHECKING': self.OnItemChecking, 'EVT_TREE_ITEM_COLLAPSED': self.OnItemCollapsed,
#                          'EVT_TREE_ITEM_COLLAPSING': self.OnItemCollapsing, 'EVT_TREE_ITEM_EXPANDED': self.OnItemExpanded,
#                          'EVT_TREE_ITEM_EXPANDING': self.OnItemExpanding, 'EVT_TREE_ITEM_GETTOOLTIP': self.OnToolTip,
#                          'EVT_TREE_ITEM_MENU': self.OnItemMenu, 'EVT_TREE_ITEM_RIGHT_CLICK': self.OnRightDown,
#                          'EVT_TREE_KEY_DOWN': self.OnKey, 'EVT_TREE_SEL_CHANGED': self.OnSelChanged,
#                          'EVT_TREE_SEL_CHANGING': self.OnSelChanging, "EVT_TREE_ITEM_HYPERLINK": self.OnHyperLink}
#
#        mainframe = wx.GetTopLevelParent(self)
#        
#        if not hasattr(mainframe, "leftpanel"):
#            self.Bind(CT.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
#            self.Bind(CT.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
#            self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
#            self.Bind(CT.EVT_TREE_SEL_CHANGING, self.OnSelChanging)
#            self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
#            self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
#        else:
#            for combos in mainframe.treeevents:
#                self.BindEvents(combos)
#
#        if hasattr(mainframe, "leftpanel"):
#            self.ChangeStyle(mainframe.treestyles)
#
#        if not(self.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
#            self.SelectItem(self.root)
#            self.Expand(self.root)

    
        
        
        
    def AjouterObjectif(self, event = None):
        self.sequence.AjouterObjectif()
        
        
    def SupprimerObjectif(self, event = None, item = None):
        self.sequence.SupprimerObjectif(item)

            
    def AjouterSeance(self, event = None):
        seance = self.sequence.AjouterSeance()
        self.lstSeances.append(self.AppendItem(self.seances, u"Séance :", data = seance))
        
    def AjouterRotation(self, event = None, item = None):
        seance = self.sequence.AjouterRotation(self.GetItemPyData(item))
        self.SetItemText(item, u"Rotation")
        self.lstSeances.append(self.AppendItem(item, u"Séance :", data = seance))
        
    def AjouterSerie(self, event = None, item = None):
        seance = self.sequence.AjouterRotation(self.GetItemPyData(item))
        self.SetItemText(item, u"Rotation")
        self.lstSeances.append(self.AppendItem(item, u"Séance :", data = seance))
        
    def SupprimerSeance(self, event = None, item = None):
        if self.sequence.SupprimerSeance(self.GetItemPyData(item)):
            self.lstSeances.remove(item)
            self.Delete(item)
        
        
#    def BindEvents(self, choice, recreate=False):
#
#        value = choice.GetValue()
#        text = choice.GetLabel()
#        
#        evt = "CT." + text
#        binder = self.eventdict[text]
#
#        if value == 1:
#            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
#                self.Bind(wx.EVT_RIGHT_DOWN, None)
#                self.Bind(wx.EVT_RIGHT_UP, None)
#            self.Bind(eval(evt), binder)
#        else:
#            self.Bind(eval(evt), None)
#            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
#                self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
#                self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)


#    def ChangeStyle(self, combos):
#
#        style = 0
#        for combo in combos:
#            if combo.GetValue() == 1:
#                style = style | eval("CT." + combo.GetLabel())
#
#        if self.GetAGWWindowStyleFlag() != style:
#            self.SetAGWWindowStyleFlag(style)
#            
#
#    def OnCompareItems(self, item1, item2):
#        
#        t1 = self.GetItemText(item1)
#        t2 = self.GetItemText(item2)
#        
#        self.log.write('compare: ' + t1 + ' <> ' + t2 + "\n")
#
#        if t1 < t2:
#            return -1
#        if t1 == t2:
#            return 0
#
#        return 1

    
#    def OnIdle(self, event):
#
#        if self.gauge:
#            try:
#                if self.gauge.IsEnabled() and self.gauge.IsShown():
#                    self.count = self.count + 1
#
#                    if self.count >= 50:
#                        self.count = 0
#
#                    self.gauge.SetValue(self.count)
#
#            except:
#                self.gauge = None
#
#        event.Skip()


    def OnRightDown(self, event):
        print "OnRightDown"
#        pt = event.GetPosition()
#        item, flags = self.HitTest(pt)
        item = event.GetItem()
#        print dir(item)

        self.sequence.AfficherMenuContextuel(item)
        
        



#    def OnRightUp(self, event):
#
#        item = self.item
#        
#        if not item:
#            event.Skip()
#            return
#
#        if not self.IsItemEnabled(item):
#            event.Skip()
#            return
#
#        # Item Text Appearance
#        ishtml = self.IsItemHyperText(item)
#        back = self.GetItemBackgroundColour(item)
#        fore = self.GetItemTextColour(item)
#        isbold = self.IsBold(item)
#        font = self.GetItemFont(item)
#
#        # Icons On Item
#        normal = self.GetItemImage(item, CT.TreeItemIcon_Normal)
#        selected = self.GetItemImage(item, CT.TreeItemIcon_Selected)
#        expanded = self.GetItemImage(item, CT.TreeItemIcon_Expanded)
#        selexp = self.GetItemImage(item, CT.TreeItemIcon_SelectedExpanded)
#
#        # Enabling/Disabling Windows Associated To An Item
#        haswin = self.GetItemWindow(item)
#
#        # Enabling/Disabling Items
#        enabled = self.IsItemEnabled(item)
#
#        # Generic Item's Info
#        children = self.GetChildrenCount(item)
#        itemtype = self.GetItemType(item)
#        text = self.GetItemText(item)
#        pydata = self.GetPyData(item)
#        
#        self.current = item
#        self.itemdict = {"ishtml": ishtml, "back": back, "fore": fore, "isbold": isbold,
#                         "font": font, "normal": normal, "selected": selected, "expanded": expanded,
#                         "selexp": selexp, "haswin": haswin, "children": children,
#                         "itemtype": itemtype, "text": text, "pydata": pydata, "enabled": enabled}
#        
#        menu = wx.Menu()
#
#        item1 = menu.Append(wx.ID_ANY, "Change Item Background Colour")
#        item2 = menu.Append(wx.ID_ANY, "Modify Item Text Colour")
#        menu.AppendSeparator()
#        if isbold:
#            strs = "Make Item Text Not Bold"
#        else:
#            strs = "Make Item Text Bold"
#        item3 = menu.Append(wx.ID_ANY, strs)
#        item4 = menu.Append(wx.ID_ANY, "Change Item Font")
#        menu.AppendSeparator()
#        if ishtml:
#            strs = "Set Item As Non-Hyperlink"
#        else:
#            strs = "Set Item As Hyperlink"
#        item5 = menu.Append(wx.ID_ANY, strs)
#        menu.AppendSeparator()
#        if haswin:
#            enabled = self.GetItemWindowEnabled(item)
#            if enabled:
#                strs = "Disable Associated Widget"
#            else:
#                strs = "Enable Associated Widget"
#        else:
#            strs = "Enable Associated Widget"
#        item6 = menu.Append(wx.ID_ANY, strs)
#
#        if not haswin:
#            item6.Enable(False)
#
#        item7 = menu.Append(wx.ID_ANY, "Disable Item")
#        
#        menu.AppendSeparator()
#        item8 = menu.Append(wx.ID_ANY, "Change Item Icons")
#        menu.AppendSeparator()
#        item9 = menu.Append(wx.ID_ANY, "Get Other Information For This Item")
#        menu.AppendSeparator()
#
#        item10 = menu.Append(wx.ID_ANY, "Delete Item")
#        if item == self.GetRootItem():
#            item10.Enable(False)
#        item11 = menu.Append(wx.ID_ANY, "Prepend An Item")
#        item12 = menu.Append(wx.ID_ANY, "Append An Item")
#
#        self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
#        self.Bind(wx.EVT_MENU, self.OnItemForeground, item2)
#        self.Bind(wx.EVT_MENU, self.OnItemBold, item3)
#        self.Bind(wx.EVT_MENU, self.OnItemFont, item4)
#        self.Bind(wx.EVT_MENU, self.OnItemHyperText, item5)
#        self.Bind(wx.EVT_MENU, self.OnEnableWindow, item6)
#        self.Bind(wx.EVT_MENU, self.OnDisableItem, item7)
#        self.Bind(wx.EVT_MENU, self.OnItemIcons, item8)
#        self.Bind(wx.EVT_MENU, self.OnItemInfo, item9)
#        self.Bind(wx.EVT_MENU, self.OnItemDelete, item10)
#        self.Bind(wx.EVT_MENU, self.OnItemPrepend, item11)
#        self.Bind(wx.EVT_MENU, self.OnItemAppend, item12)
#        
#        self.PopupMenu(menu)
#        menu.Destroy()
        

#    def OnItemBackground(self, event):
#
#        colourdata = wx.ColourData()
#        colourdata.SetColour(self.itemdict["back"])
#        dlg = wx.ColourDialog(self, colourdata)
#        
#        dlg.GetColourData().SetChooseFull(True)
#
#        if dlg.ShowModal() == wx.ID_OK:
#            data = dlg.GetColourData()
#            col1 = data.GetColour().Get()
#            self.SetItemBackgroundColour(self.current, col1)
#        dlg.Destroy()
#
#
#    def OnItemForeground(self, event):
#
#        colourdata = wx.ColourData()
#        colourdata.SetColour(self.itemdict["fore"])
#        dlg = wx.ColourDialog(self, colourdata)
#        
#        dlg.GetColourData().SetChooseFull(True)
#
#        if dlg.ShowModal() == wx.ID_OK:
#            data = dlg.GetColourData()
#            col1 = data.GetColour().Get()
#            self.SetItemTextColour(self.current, col1)
#        dlg.Destroy()


#    def OnItemBold(self, event):
#
#        self.SetItemBold(self.current, not self.itemdict["isbold"])
#
#
#    def OnItemFont(self, event):
#
#        data = wx.FontData()
#        font = self.itemdict["font"]
#        
#        if font is None:
#            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
#            
#        data.SetInitialFont(font)
#
#        dlg = wx.FontDialog(self, data)
#        
#        if dlg.ShowModal() == wx.ID_OK:
#            data = dlg.GetFontData()
#            font = data.GetChosenFont()
#            self.SetItemFont(self.current, font)
#
#        dlg.Destroy()
        

#    def OnItemHyperText(self, event):
#
#        self.SetItemHyperText(self.current, not self.itemdict["ishtml"])
#
#
#    def OnEnableWindow(self, event):
#
#        enable = self.GetItemWindowEnabled(self.current)
#        self.SetItemWindowEnabled(self.current, not enable)
#
#
#    def OnDisableItem(self, event):
#
#        self.EnableItem(self.current, False)
#        

#    def OnItemIcons(self, event):
#
#        bitmaps = [self.itemdict["normal"], self.itemdict["selected"],
#                   self.itemdict["expanded"], self.itemdict["selexp"]]
#
#        wx.BeginBusyCursor()        
#        dlg = TreeIcons(self, -1, bitmaps=bitmaps)
#        wx.EndBusyCursor()
#        dlg.ShowModal()


#    def SetNewIcons(self, bitmaps):
#
#        self.SetItemImage(self.current, bitmaps[0], CT.TreeItemIcon_Normal)
#        self.SetItemImage(self.current, bitmaps[1], CT.TreeItemIcon_Selected)
#        self.SetItemImage(self.current, bitmaps[2], CT.TreeItemIcon_Expanded)
#        self.SetItemImage(self.current, bitmaps[3], CT.TreeItemIcon_SelectedExpanded)

        

#    def OnItemDelete(self, event):
#
#        strs = "Are You Sure You Want To Delete Item " + self.GetItemText(self.current) + "?"
#        dlg = wx.MessageDialog(None, strs, 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
#
#        if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
#            dlg.Destroy()
#            return
#
#        dlg.Destroy()
#
#        self.DeleteChildren(self.current)
#        self.Delete(self.current)
#        self.current = None
#        


#    def OnItemPrepend(self, event):
#
#        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')
#
#        if dlg.ShowModal() == wx.ID_OK:
#            newname = dlg.GetValue()
#            newitem = self.PrependItem(self.current, newname)
#            self.EnsureVisible(newitem)
#
#        dlg.Destroy()
#
#
#    def OnItemAppend(self, event):
#
#        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')
#
#        if dlg.ShowModal() == wx.ID_OK:
#            newname = dlg.GetValue()
#            newitem = self.AppendItem(self.current, newname)
#            self.EnsureVisible(newitem)
#
#        dlg.Destroy()
        

    def OnBeginEdit(self, event):
        
        self.log.write("OnBeginEdit" + "\n")
        # show how to prevent edit...
        item = event.GetItem()
        if item and self.GetItemText(item) == "The Root Item":
            wx.Bell()
            self.log.write("You can't edit this one..." + "\n")

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.GetFirstChild(root)

            while child:
                self.log.write("Child [%s] visible = %d" % (self.GetItemText(child), self.IsVisible(child)) + "\n")
                (child, cookie) = self.GetNextChild(root, cookie)

            event.Veto()


    def OnEndEdit(self, event):
        pass
#        self.log.write("OnEndEdit: %s %s" %(event.IsEditCancelled(), event.GetLabel()))
#        # show how to reject edit, we'll not allow any digits
#        for x in event.GetLabel():
#            if x in string.digits:
#                self.log.write(", You can't enter digits..." + "\n")
#                event.Veto()
#                return
#            
#        self.log.write("\n")


    def OnLeftDClick(self, event):
        
        pt = event.GetPosition()
#        item, flags = self.HitTest(pt)
#        if item and (flags & CT.TREE_HITTEST_ONITEMLABEL):
#            if self.GetAGWWindowStyleFlag() & CT.TR_EDIT_LABELS:
#                self.log.write("OnLeftDClick: %s (manually starting label edit)"% self.GetItemText(item) + "\n")
#                self.EditLabel(item)
#            else:
#                self.log.write("OnLeftDClick: Cannot Start Manual Editing, Missing Style TR_EDIT_LABELS\n")

        event.Skip()                
        

    def OnItemExpanded(self, event):
        
        item = event.GetItem()
        if item:
            self.log.write("OnItemExpanded: %s" % self.GetItemText(item) + "\n")


    def OnItemExpanding(self, event):
        
        item = event.GetItem()
        if item:
            self.log.write("OnItemExpanding: %s" % self.GetItemText(item) + "\n")
            
        event.Skip()

        
    def OnItemCollapsed(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemCollapsed: %s" % self.GetItemText(item) + "\n")
            

    

        
    def OnSelChanged(self, event):
        print "OnSelChanged"
        self.item = event.GetItem()
        data = self.GetItemPyData(self.item)
        if data == None:
            panelPropriete = self.panelVide
        else:
            panelPropriete = data.panelPropriete
        self.panelProp.AfficherPanel(panelPropriete)
#        wx.CallAfter(panelPropriete.Refresh)
        event.Skip()



    def OnBeginDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Beginning Drag..." + "\n")

            event.Allow()



    def OnEndDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Ending Drag!" + "\n")

        event.Skip()            


    def OnDeleteItem(self, event):

        item = event.GetItem()

        if not item:
            return

        self.log.write("Deleting Item: %s" % self.GetItemText(item) + "\n")
        event.Skip()
        

    
    def OnToolTip(self, event):

        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))


    def OnItemMenu(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemMenu: %s" % self.GetItemText(item) + "\n")
    
        event.Skip()


    def OnKey(self, event):

        keycode = event.GetKeyCode()
#        keyname = keyMap.get(keycode, None)
#                
#        if keycode == wx.WXK_BACK:
#            self.log.write("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
#            return
#
#        if keyname is None:
#            if "unicode" in wx.PlatformInfo:
#                keycode = event.GetUnicodeKey()
#                if keycode <= 127:
#                    keycode = event.GetKeyCode()
#                keyname = "\"" + unichr(event.GetUnicodeKey()) + "\""
#                if keycode < 27:
#                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
#                
#            elif keycode < 256:
#                if keycode == 0:
#                    keyname = "NUL"
#                elif keycode < 27:
#                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
#                else:
#                    keyname = "\"%s\"" % chr(keycode)
#            else:
#                keyname = "unknown (%s)" % keycode
                

        event.Skip()
        
        
    def OnActivate(self, event):
        
        if self.item:
            self.log.write("OnActivate: %s" % self.GetItemText(self.item) + "\n")

        event.Skip()

        
    def OnHyperLink(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnHyperLink: %s" % self.GetItemText(self.item) + "\n")
            

    def OnTextCtrl(self, event):

        char = chr(event.GetKeyCode())
        self.log.write("EDITING THE TEXTCTRL: You Wrote '" + char + \
                       "' (KeyCode = " + str(event.GetKeyCode()) + ")\n")
        event.Skip()


    def OnComboBox(self, event):

        selection = event.GetEventObject().GetValue()
        self.log.write("CHOICE FROM COMBOBOX: You Chose '" + selection + "'\n")
        event.Skip()

#
# Fonction pour indenter les XML générés par ElementTree
#
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

####################################################################################
#
#   Classe définissant l'application
#    --> récupération des paramétres passés en ligne de commande
#
####################################################################################
class SeqApp(wx.App):
    def OnInit(self):
        if len(sys.argv)>1: #un paramétre a été passé
            for param in sys.argv:
                parametre = param.upper()
                # on verifie que le fichier passé en paramétre existe
                
            
        frame = FenetreSequence()
        frame.Show()
        return True
    
    
if __name__ == '__main__':
    app = SeqApp(False)
    app.MainLoop()
    
    
