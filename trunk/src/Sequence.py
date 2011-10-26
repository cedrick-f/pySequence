#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sequence.py
Aide à la réalisation de fiches pédagogiques de séquence
*************
*   STIDD   *
*************
Copyright (C) 2011  
@author: Cedrick FAURY

"""
__appname__= "pySequence"
__author__ = u"Cédrick FAURY"
__version__ = "1 beta"

##
## Les deuxlignes suivantes permettent de lancer le script sequence.py depuis n'importe
## quel répertoire sans que l'utilisation de chemins
## relatifs ne soit perturbée
##
#import sys, os
#PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
##PATH = os.path.split(PATH)[0]
#os.chdir(PATH)
#sys.path.append(PATH)
#print "Dossier de l'application :",PATH

####################################################################################
#
#   Import des modules nécessaires
#
####################################################################################
# Outils "système"
import sys, os
import webbrowser

# GUI
import wx
from wx.lib.wordwrap import wordwrap
import wx.lib.hyperlink as hl

# Graphiques vectoriels
try:
    import wx.lib.wxcairo
    import cairo
    haveCairo = True
except ImportError:
    haveCairo = False
from assistCairo import *


# Arbre
try:
    from agw import customtreectrl as CT
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.customtreectrl as CT
import images

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
from CedWidgets import Variable, VariableCtrl, VAR_REEL_POS, EVT_VAR_CTRL, VAR_ENTIER_POS

## les paramèters de configuration graphique de la fiche de séquence
#import configFiche as cf
#import ConfigParser

#from draw_cairo import Draw
import draw_cairo
from constantes import *

#####################################################################################
##
##   Définition des constantes
##
#####################################################################################
#
#CentresInterets = [u"Développement durable et compétitivité des produits",
#                   u"Design, créativité et innovation",
#                   u"Caractéristiques des matériaux et structures",
#                   u"Solutions constructives des matériaux et des structures",
#                   u"Dimensionnement des structures et choix des matériaux",
#                   u"Efficacité énergétique liée au comportement des matériaux et des structures",
#                   u"Formes et caractéristiques de l'énergie",
#                   u"Organisation structurelle et solutions constructives des chaînes d'énergie",
#                   u"Amélioration de l'efficacité énergétique dans les chaînes d'énergie",
#                   u"Amélioration de la gestion de l'énergie",
#                   u"Formes et caractéristiques de l'information",
#                   u"Organisation structurelle et solutions constructives des chaînes d'information",
#                   u"Commande temporelle des systémes",
#                   u"Informations liées au comportement des matériaux et des structures",
#                   u"Optimisation des paramètres par simulation globale"
#                   ]
#
#Effectifs = {"C" : [u"Classe entière",      32],
#             "G" : [u"Effectif réduit",     16],
#             "D" : [u"Demi-groupe",         8],
#             "E" : [u"Etude et Projet",     4],
#             "P" : [u"Activité Pratique",   2],
#             }
#
#
#def ouvrirConfig():
#    print "ouvrirConfig"
#    global CentresInterets
#    
#    config = ConfigParser.ConfigParser()
#    config.read(os.path.join(PATH,'configuration.cfg'))
#    
#    section = "Centres d'interet"
#    l = [""] * len(config.options(section))
#    for o in config.options(section):
#        l[eval(o)-1] = unicode(config.get(section,o), 'cp1252')
#    CentresInterets = l
#        
#    section = "Effectifs classe"
#    for k in Effectifs.keys():
#        Effectifs[k][1] = config.getint(section,k)
#
#ouvrirConfig()
#
#    
#Competences = {"CO1.1" : u"Justifier les choix des matériaux, des structures d'un système et les énergies mises en oeuvre dans une approche de développement durable",
#               "CO1.2" : u"Justifier le choix d'une solution selon des contraintes d'ergonomie et d'effets sur la santé de l'homme et du vivant",
#               "CO2.1" : u"Identifier les flux et la forme de l'énergie, caractériser ses transformations et/ou modulations et estimer l'efficacité énergétique globale d'un système",
#               "CO2.2" : u"Justifier les solutions constructives d'un systéme au regard des impacts environnementaux et économiques engendrés tout au long de son cycle de vie",
#               "CO3.1" : u"Décoder le cahier des charges fonctionnel d'un système",
#               "CO3.2" : u"Evaluer la compétitivité d'un système d'un point de vue technique et économique",
#               "CO4.1" : u"Identifier et caractériser les fonctions et les constituants d'un système ainsi que ses entrées/sorties",
#               "CO4.2" : u"Identifier et caractériser l'agencement  matériel et/ou logiciel d'un système", 
#               "CO4.3" : u"Identifier et caractériser le fonctionnement temporel d'un système",
#               "CO4.4" : u"Identifier et caractériser des solutions techniques relatives aux matériaux, à la structure, à l'énergie et aux informations (acquisition, traitement, transmission) d'un système",
#               "CO5.1" : u"Expliquer des éléments d'une modélisation proposée relative au comportement de tout ou partie d'un système",
#               "CO5.2" : u"Identifier des variables internes et externes utiles à une modélisation, simuler et valider le comportement du modèle",
#               "CO5.3" : u"Evaluer un écart entre le comportement du réel et le comportement du modèle en fonction des paramètres proposés",
#               "CO6.1" : u"Décrire une idée, un principe, une solution, un projet en utilisant des outils de représentation adaptés",
#               "CO6.2" : u"Décrire le fonctionnement et/ou l'exploitation d'un système en utilisant l'outil de description le plus pertinent",
#               "CO6.3" : u"Présenter et argumenter des démarches, des résultats, y compris dans une langue étrangère",
#               }
#
#
#TypesActivite = {"ED" : u"Activité d'étude de dossier",
#                 "AP" : u"Activité pratique",
#                 "P" : u"Activité de projet",
#                }
#
#TypesSeance = {"C" : u"Cours",
#               "SA" : u"Synthèse d'activité",
#               "SS" : u"Synthèse de séquence",
#               "E" : u"Evaluation",
#               }
#TypesSeance.update(TypesActivite)
#TypesSeance.update({"R" : u"Rotation d'activités",
#                    "S" : u"Activités en parallèle"})
#
#TypesSeanceCourt = {"ED" : u"Etude de dossier",
#                    "AP" : u"Activité pratique",
#                    "P" : u"Projet",
#                    "C" : u"Cours",
#                    "SA" : u"Synt. d'activité",
#                    "SS" : u"Synt. de séquence",
#                    "E" : u"Evaluation",
#                    "R" : u"Rotation",
#                    "S" : u"Parallèle"}
#
#listeTypeSeance = ["ED", "AP", "P", "C", "SA", "SS", "E", "R", "S"]
#listeTypeActivite = ["ED", "AP", "P"]
#
#
#
#Demarches = {"I" : u"Investigation",
#             "R" : u"Résolution de problème",
#             "P" : u"Projet"}
#listeDemarches = ["I", "R", "P"]

####################################################################################
#
#   Evenement perso pour détecter une modification de la séquence
#
####################################################################################
myEVT_SEQ_MODIFIED = wx.NewEventType()
EVT_SEQ_MODIFIED = wx.PyEventBinder(myEVT_SEQ_MODIFIED, 1)

#----------------------------------------------------------------------
class SeqEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
       

    
####################################################################################
#
#   Classe définissant les propriétés d'une séquence
#
####################################################################################
Titres = [u"Séquence pédagogique",
          u"Objectifs pédagogiques",
          u"Séances",
          u"Systèmes"]

class Sequence():
    def __init__(self, app, panelParent, intitule = u""):
        self.intitule = intitule
        self.panelPropriete = PanelPropriete_Sequence(panelParent, self)
        
        self.CI = CentreInteret(self, panelParent)
        
        self.obj = [Competence(self, panelParent)]
        self.systemes = []
        self.seance = [Seance(self, panelParent)]
        
        
        
        self.panelParent = panelParent
        self.app = app
        
        
        # Un curseur pour placer les séances
#        self.InitCurseur()
        
        
    ######################################################################################  
    def __repr__(self):
        t = u"Séquence :"+self.intitule + "\n"
        t += "   " + self.CI.__repr__() + "\n"
        for c in self.obj:
            t += "   " + c.__repr__() + "\n"
        for s in self.seance:
            t += "   " + s.__repr__() + "\n"
        return t
    
    ######################################################################################  
    def GetApp(self):
        return self.app
    
    ######################################################################################  
    def getBranche(self):
        # Création de la racine
        sequence = ET.Element("Sequence")
        sequence.set("Intitule", self.intitule)
        
        ci = ET.SubElement(sequence, "CentreInteret")
        ci.append(self.CI.getBranche())
        
        objectifs = ET.SubElement(sequence, "Objectifs")
        for obj in self.obj:
            objectifs.append(obj.getBranche())
            
        seances = ET.SubElement(sequence, "Seances")
        for sce in self.seance:
            seances.append(sce.getBranche())
            
        systeme = ET.SubElement(sequence, "Systemes")
        for sy in self.systemes:
            systeme.append(sy.getBranche())
        
        return sequence
        
    ######################################################################################  
    def setBranche(self, branche):
        print "setBranche séquence"
        self.intitule = branche.get("Intitule", u"")
        
        brancheCI = branche.find("CentreInteret")
        self.CI.setBranche(brancheCI)
        
        brancheObj = branche.find("Objectifs")
        self.obj = []
        for obj in list(brancheObj):
            comp = Competence(self, self.panelParent)
            comp.setBranche(obj)
            self.obj.append(comp)
        
        brancheSys = branche.find("Systemes")
        self.systemes = []
        for sy in list(brancheSys):
            systeme = Systeme(self, self.panelParent)
            systeme.setBranche(sy)
            self.systemes.append(systeme)    
        
        brancheSce = branche.find("Seances")
        self.seance = []
        for sce in list(brancheSce):
            seance = Seance(self, self.panelParent)
            seance.setBranche(sce)
            self.seance.append(seance)
        
#        self.MiseAJourListeSystemes()
        self.panelPropriete.MiseAJour()
        
        
    ######################################################################################  
    def SetText(self, text):
        self.intitule = text
        
    ######################################################################################  
    def SetCodes(self):
        self.CI.SetCode()
        for comp in self.obj:
            comp.SetCode()
        
        for sce in self.seance:
            sce.SetCode()    
            
        for sy in self.systemes:
            sy.SetCode()    
        
    ######################################################################################  
    def VerifPb(self):
        for s in self.seance:
            s.VerifPb()
        
    ######################################################################################  
    def MiseAJourListeSystemes(self):
        for s in self.seance:
            s.MiseAJourListeSystemes()
    
    
    ######################################################################################  
    def AjouterSeance(self, event = None):
        seance = Seance(self, self.panelParent)
        self.seance.append(seance)
        self.OrdonnerSeances()
        seance.ConstruireArbre(self.arbre, self.brancheSce)
        self.panelPropriete.sendEvent()
        return seance
    
    
    ######################################################################################  
    def SupprimerSeance(self, event = None, item = None):
        if len(self.seance) > 1: # On en laisse toujours une !!
            seance = self.arbre.GetItemPyData(item)
            self.seance.remove(seance)
            self.arbre.Delete(item)
            self.OrdonnerSeances()
            self.panelPropriete.sendEvent()
            return True
        return False
    
    
    ######################################################################################  
    def OrdonnerSeances(self):
        for i, sce in enumerate(self.seance):
            sce.ordre = i
        
        self.SetCodes()
    
    ######################################################################################  
    def AjouterObjectif(self, event = None):
        obj = Competence(self, self.panelParent)
        self.obj.append(obj)
        obj.ConstruireArbre(self.arbre, self.brancheObj)
        self.panelPropriete.sendEvent()
        return
    
    
    ######################################################################################  
    def SupprimerObjectif(self, event = None, item = None):
        if len(self.obj) > 1:
            comp = self.arbre.GetItemPyData(item)
            self.obj.remove(comp)
            self.arbre.Delete(item)
            self.panelPropriete.sendEvent()
        
    
    ######################################################################################  
    def AjouterSysteme(self, event = None):
        sy = Systeme(self, self.panelParent)
        self.systemes.append(sy)
        sy.ConstruireArbre(self.arbre, self.brancheSys)
        self.arbre.Expand(self.brancheSys)
        self.panelPropriete.sendEvent()
        return
    
    
    ######################################################################################  
    def SupprimerSysteme(self, event = None, item = None):
        sy = self.arbre.GetItemPyData(item)
        self.systemes.remove(sy)
        self.arbre.Delete(item)
        self.panelPropriete.sendEvent()
    
    
    
    ######################################################################################  
    def AjouterRotation(self, seance):
        seanceR1 = Seance(self.panelParent)
        seance.sousSeances.append(seanceR1)
        return seanceR1
        
        
    ######################################################################################  
    def ConstruireArbre(self, arbre):
        print "ConstruireArbre séquence"
        self.arbre = arbre
        self.branche = arbre.AddRoot(Titres[0], data = self, image = self.arbre.images["Seq"])

        self.CI.ConstruireArbre(arbre, self.branche)
        
        self.brancheObj = arbre.AppendItem(self.branche, Titres[1], image = self.arbre.images["Obj"])
        for obj in self.obj:
            obj.ConstruireArbre(arbre, self.brancheObj)
            
        
        self.brancheSce = arbre.AppendItem(self.branche, Titres[2])
        for sce in self.seance:
            sce.ConstruireArbre(arbre, self.brancheSce) 
            
        self.brancheSys = arbre.AppendItem(self.branche, Titres[3])
        for sy in self.systemes:
            sy.ConstruireArbre(arbre, self.brancheSys)    
            
            
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):    
        """ Affiche le menu contextuel associé é la séquence
            ... ou bien celui de itemArbre concerné ...
        """
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([[u"Enregistrer", self.app.commandeEnregistrer],
                                             [u"Ouvrir", self.app.commandeOuvrir],
                                             [u"Exporter la fiche en PDF", self.app.exporterFiche]])
            
        
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Competence):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Seance):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Systeme):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
        elif self.arbre.GetItemText(itemArbre) == Titres[1]: # Objectifs pédagogiques
            self.app.AfficherMenuContextuel([[u"Ajouter une compétence", self.AjouterObjectif]])
            
            
        elif self.arbre.GetItemText(itemArbre) == Titres[2]: # Séances
            self.app.AfficherMenuContextuel([[u"Ajouter une séance", self.AjouterSeance]])
            
        elif self.arbre.GetItemText(itemArbre) == Titres[3]: # Système
            self.app.AfficherMenuContextuel([[u"Ajouter un système", self.AjouterSysteme]])
         
         
            
#    ######################################################################################  
#    def InitCurseur(self):
#        self.curseur = [cf.posZSeances[0], cf.posZSeances[1]]
        
        
    ######################################################################################  
    def GetHoraireTotal(self):
        h = 0
        for s in self.seance:
            h += s.GetDuree()
        return h
            
    ######################################################################################  
    def GetNbreSeances(self):
        n = 0
        for s in self.seance:
            if s.typeSeance in ["R", "S"]:
                n += len(s.sousSeances)
            n += 1
        return n
    
    
    ######################################################################################  
    def GetToutesSeances(self):
        l = []
        for s in self.seance:
            l.append(s)
            if s.typeSeance in ["R", "S"]:
                l.extend(s.GetToutesSeances())
            
        return l
    
    
#    ######################################################################################  
#    def DefinirZones(self):
#        """ Calcule les positions et dimensions des différentes zones de tracé
#            en fonction du nombre d'éléments (séances, systèmes)
#        """
#        # Zone des intitulés des séances
#        cf.tailleZIntSeances[1] = len(self.GetIntituleSeances()[0])* cf.hIntSeance
#        cf.posZIntSeances[1] = 1 - cf.tailleZIntSeances[1]-cf.margeY
#        
#        # Zone du tableau des Systèmes
#        cf.tailleZSysteme[0] = cf.wColSysteme * len(self.systemes)
#        cf.tailleZSysteme[1] = cf.posZIntSeances[1] - cf.posZSysteme[1] - cf.ecartY
#        cf.posZSysteme[0] = cf.posZOrganis[0] + cf.tailleZOrganis[0] - cf.tailleZSysteme[0]
#        for i, s in enumerate(self.systemes):
#            cf.xSystemes[s.nom] = cf.posZSysteme[0] + (i+0.5) * cf.wColSysteme
#        
#        
#        # Zone du tableau des démarches
#        cf.posZDemarche[0] = cf.posZSysteme[0] - cf.tailleZDemarche[0] - cf.ecartX
#        cf.tailleZDemarche[1] = cf.tailleZSysteme[1]
#        cf.xDemarche["I"] = cf.posZDemarche[0] + cf.tailleZDemarche[0]/6
#        cf.xDemarche["R"] = cf.posZDemarche[0] + cf.tailleZDemarche[0]*3/6
#        cf.xDemarche["P"] = cf.posZDemarche[0] + cf.tailleZDemarche[0]*5/6
#                     
#        # Zone de déroulement de la séquence
#        cf.tailleZDeroul[0] = cf.posZDemarche[0] - cf.posZDeroul[0] - cf.ecartX
#        cf.tailleZDeroul[1] = cf.tailleZSysteme[1]
#        
#        
#        # Zone des séances
#        cf.tailleZSeances[0] = cf.tailleZDeroul[0] - 0.05 # écart pour les durées
#        cf.tailleZSeances[1] = cf.tailleZSysteme[1] - cf.posZSeances[1] + cf.posZDeroul[1] - 0.05
#        cf.wEff = {"C" : cf.tailleZSeances[0],
#                 "G" : cf.tailleZSeances[0]*6/7,
#                 "D" : cf.tailleZSeances[0]*3/7,
#                 "E" : cf.tailleZSeances[0]*Effectifs["E"][1]/Effectifs["G"][1]*6/7,
#                 "P" : cf.tailleZSeances[0]*Effectifs["P"][1]/Effectifs["G"][1]*6/7,
#                 }
#        cf.ecartSeanceY = 0.02
#        cf.hHoraire = (cf.tailleZSeances[1] - (len(self.seance)-1)*cf.ecartSeanceY) / self.GetHoraireTotal()
        
        
        
#    ######################################################################################  
#    def Draw(self, ctx):
##        print "Draw séquence"
#        self.InitCurseur()
#        
#        self.DefinirZones()
#        
#        options = ctx.get_font_options()
#        options.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
#        ctx.set_font_options(options)
#        
#        # 
#        # Effectifs
#        #
#        for i, e in enumerate(["C", "G", "D", "E", "P"]):
#            x = cf.posZSeances[0]
#            h = (cf.posZSeances[1]-cf.posZDemarche[1]-0.01) / 5
#            y = cf.posZDemarche[1] + i * h
#            w = cf.wEff[e]
#            ctx.set_line_width(0.001)
#            ctx.set_source_rgb(0.8, 0.9, 0.8)
#            ctx.rectangle(x, y, w, h)
#            ctx.stroke()
#            ctx.set_source_rgb(0.6, 0.8, 0.6)
#            show_text_rect(ctx, Effectifs[e][0], x, y, w, h)
#            ctx.stroke()
#            self.DrawLigneEff(ctx, x+w, y+h)
#            
#        
##        #
##        #  Bordure
##        #
##        ctx.set_line_width(0.005)
##        ctx.set_source_rgb(0, 0, 0)
##        ctx.rectangle(0, 0, 0.724, 1)
##        ctx.stroke()
#        
#        #
#        #  Intitulé de la séquence
#        #
#        x, y = cf.posIntitule
#        w, h = cf.tailleIntitule
#        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                              cairo.FONT_WEIGHT_BOLD)
#        ctx.set_source_rgb(0, 0, 0)
#        if len(self.intitule) > 0:
#            show_text_rect(ctx, self.intitule, x, y, w, h)
#        ctx.set_line_width(0.005)
#        ctx.set_source_rgb(cf.BcoulIntitule[0], cf.BcoulIntitule[1], cf.BcoulIntitule[2])
#        ctx.rectangle(x, y, w, h)
#        ctx.stroke()
#
#        #
#        #  Objectifs
#        #
#        
#        # Rectangle arrondi
#        x0, y0 = cf.posObj
#        rect_width, rect_height  = cf.tailleObj
#        curve_rect(ctx, x0, y0, rect_width, rect_height, 0.3)
#        ctx.set_source_rgb (cf.IcoulObj[0], cf.IcoulObj[1], cf.IcoulObj[2])
#        ctx.fill_preserve ()
#        ctx.set_source_rgba (cf.BcoulObj[0], cf.BcoulObj[1], cf.BcoulObj[2])
#        ctx.stroke ()
#        
#        # Titre
#        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                              cairo.FONT_WEIGHT_BOLD)
#        ctx.set_font_size(0.016)
#        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents("Objectifs")
#        xc=x0+rect_width/2-width/2
#        yc=y0+height+0.008
#        ctx.move_to(xc, yc)
#        ctx.set_source_rgb(0, 0, 0)
#        ctx.show_text("Objectifs")
#        
#        #
#        # Codes objectifs
#        #
#        if self.obj[0].num != None:
#            no = len(self.obj)
#            txtObj = ''
#            for i, t in enumerate(self.obj):
#                if hasattr(t, 'code'):
#                    txtObj += " " + t.code
#                    ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                          cairo.FONT_WEIGHT_BOLD)
#                    show_text_rect(ctx, t.code, x0+i*rect_width/no, yc, 
#                                   rect_width/no, rect_height/4)
#                    ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                          cairo.FONT_WEIGHT_NORMAL)
#                    show_text_rect(ctx, Competences[t.code], x0+i*rect_width/no, y0+rect_height*2/5, 
#                                   rect_width/no, rect_height/2)
#            
##            x, y = cf.posObj
##            w, h = cf.tailleObj
#                    ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                          cairo.FONT_WEIGHT_BOLD)
##        
# 
#        #
#        #  CI
#        #
#        self.CI.Draw(ctx)
#        
#        
#        #
#        #  Séances
#        #
#        for s in self.seance:
#            s.Draw(ctx, self.curseur)
#            
#        #
#        #  Tableau des systèmes
#        #    
#        nomsSystemes = []
#        for s in self.systemes:
#            nomsSystemes.append(s.nom)
#        if nomsSystemes != []:
#            ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                  cairo.FONT_WEIGHT_NORMAL)
#            ctx.set_source_rgb(0, 0, 0)
#            ctx.set_line_width(0.001)
#            tableauV(ctx, nomsSystemes, cf.posZSysteme[0], cf.posZSysteme[1], 
#                    cf.tailleZSysteme[0], cf.posZSeances[1] - cf.posZSysteme[1], 
#                    0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', coul = (0.8,0.8,0.8))
#            
#            wc = cf.tailleZSysteme[0]/len(nomsSystemes)
#            _x = cf.posZSysteme[0]
#            _y = cf.posZSysteme[1]
#            for s in self.systemes:
#                s.rect=((_x, _y, wc, cf.posZSeances[1] - cf.posZSysteme[1]),)
#                ctx.move_to(_x, _y + cf.posZSeances[1] - cf.posZSysteme[1])
#                ctx.line_to(_x, _y + cf.tailleZDemarche[1])
#                _x += wc
#            ctx.move_to(_x, _y + cf.posZSeances[1] - cf.posZSysteme[1])
#            ctx.line_to(_x, _y + cf.tailleZDemarche[1])   
#            ctx.stroke()
#    
#        #
#        #  Tableau des démarches
#        #    
#        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                              cairo.FONT_WEIGHT_NORMAL)
#        ctx.set_source_rgb(0, 0, 0)
#        ctx.set_line_width(0.001)
#        l=[]
#        for d in listeDemarches : 
#            l.append(Demarches[d])
#        tableauV(ctx, l, cf.posZDemarche[0], cf.posZDemarche[1], 
#                cf.tailleZDemarche[0], cf.posZSeances[1] - cf.posZSysteme[1], 
#                0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', coul = (0.8,0.75,0.9))
#        ctx.move_to(cf.posZDemarche[0], cf.posZDemarche[1] + cf.posZSeances[1] - cf.posZSysteme[1])
#        ctx.line_to(cf.posZDemarche[0], cf.posZDemarche[1] + cf.tailleZDemarche[1])
#        ctx.move_to(cf.posZDemarche[0]+cf.tailleZDemarche[0]/3, cf.posZDemarche[1] + cf.posZSeances[1] - cf.posZSysteme[1])
#        ctx.line_to(cf.posZDemarche[0]+cf.tailleZDemarche[0]/3, cf.posZDemarche[1] + cf.tailleZDemarche[1])
#        ctx.move_to(cf.posZDemarche[0]+cf.tailleZDemarche[0]*2/3, cf.posZDemarche[1] + cf.posZSeances[1] - cf.posZSysteme[1])
#        ctx.line_to(cf.posZDemarche[0]+cf.tailleZDemarche[0]*2/3, cf.posZDemarche[1] + cf.tailleZDemarche[1])
#        ctx.move_to(cf.posZDemarche[0]+cf.tailleZDemarche[0], cf.posZDemarche[1] + cf.posZSeances[1] - cf.posZSysteme[1])
#        ctx.line_to(cf.posZDemarche[0]+cf.tailleZDemarche[0], cf.posZDemarche[1] + cf.tailleZDemarche[1])
#        ctx.stroke()
#        
#        #
#        #  Tableau des séances (en bas)
#        #
#        nomsSeances, intSeances = self.GetIntituleSeances()
##        print nomsSeances
#        if nomsSeances != []:
#            ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                  cairo.FONT_WEIGHT_NORMAL)
#            ctx.set_source_rgb(0, 0, 0)
#            ctx.set_line_width(0.002)
#            tableauH(ctx, nomsSeances, cf.posZIntSeances[0], cf.posZIntSeances[1], 
#                    0.05, cf.tailleZIntSeances[0]-0.05, cf.tailleZIntSeances[1], 
#                    nCol = 1, va = 'c', ha = 'g', orient = 'h', coul = cf.ICoulSeance, 
#                    contenu = [intSeances])
    
        
    ######################################################################################  
    def GetIntituleSeances(self):
        nomsSeances = []
        intSeances = []
        for s in self.GetToutesSeances():
#            print s
#            print s.intituleDansDeroul
            if hasattr(s, 'code') and s.intitule != "" and not s.intituleDansDeroul:
                nomsSeances.append(s.code)
                intSeances.append(s.intitule)
        return nomsSeances, intSeances
        
        
#    ######################################################################################  
#    def DrawLigneEff(self, ctx, x, y):
#        dashes = [ 0.010,   # ink
#                   0.002,   # skip
#                   0.005,   # ink
#                   0.002,   # skip
#                   ]
#        ctx.set_source_rgba (0.6, 0.8, 0.6)
#        ctx.set_line_width (0.001)
#        ctx.set_dash(dashes, 0)
#        ctx.move_to(x, cf.posZDemarche[1] + cf.tailleZDemarche[1])
#        ctx.line_to(x, y)
#        ctx.stroke()
#        ctx.set_dash([], 0)
        
    ######################################################################################  
    def HitTest(self, x, y):
#        print "HitTest", x, y
        rect = draw_cairo.posIntitule + draw_cairo.tailleIntitule
        if dansRectangle(x, y, (rect,)):
            self.arbre.DoSelectItem(self.branche)
        elif self.CI.HitTest(x, y):
            return
        elif dansRectangle(x, y, (draw_cairo.posObj + draw_cairo.tailleObj,)):
            self.arbre.DoSelectItem(self.brancheObj)
        else:
            autresZones = self.seance + self.systemes
            continuer = True
            i = 0
            while continuer:
                if i >= len(autresZones):
                    continuer = False
                else:
                    if autresZones[i].HitTest(x, y):
                        continuer = False
                i += 1
        
        
####################################################################################
#
#   Classe définissant les propriétés d'une séquence
#
####################################################################################
class CentreInteret():
    def __init__(self, parent, panelParent, numCI = None):
        
        self.SetNum(numCI)
        self.parent = parent
        
        self.panelPropriete = PanelPropriete_CI(panelParent, self)
        
       
        
        
    ######################################################################################  
    def __repr__(self):
        return self.code
    
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du centre d'intérét pour enregistrement
        """
        print "getBranche CI",
        if hasattr(self, 'code'):
            print self.code
            root = ET.Element(self.code)
        else:
            print
            root = ET.Element("")
        return root
    
    
    
    ######################################################################################  
    def setBranche(self, branche):
        code = list(branche)[0].tag
        num = eval(code[2:])-1
        self.SetNum(num)
        self.panelPropriete.MiseAJour()
#        self.SetCode()
        
    ######################################################################################  
    def SetNum(self, num):
        self.num = num
        if num != None:
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
        self.branche = arbre.AppendItem(branche, u"Centre d'intérét :", wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Ci"])
        
#    ######################################################################################  
#    def Draw(self, ctx):
#        # Rectangle arrondi
#        x0, y0 = cf.posCI
#        rect_width, rect_height  = cf.tailleCI
#        
#        curve_rect(ctx, x0, y0, rect_width, rect_height, 0.05)
#        ctx.set_source_rgb (cf.IcoulCI[0], cf.IcoulCI[1], cf.IcoulCI[2])
#        ctx.fill_preserve ()
#        ctx.set_source_rgba (cf.BcoulCI[0], cf.BcoulCI[1], cf.BcoulCI[2])
#        ctx.stroke ()
#        
#        #
#        # code
#        #
#        if self.num != None:
#            ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                  cairo.FONT_WEIGHT_BOLD)
#            ctx.set_font_size(0.02)
#            xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(self.code)
#            xc=x0+rect_width/2-width/2
#            yc=y0+height+0.01
#            ctx.move_to(xc, yc)
#            ctx.set_source_rgb(0, 0, 0)
#            ctx.show_text(self.code)
#        
#            #
#            # intitulé
#            #
#            ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                  cairo.FONT_WEIGHT_NORMAL)
#            show_text_rect(ctx, self.CI, x0, yc, rect_width, rect_height - height-0.01)

        
    def HitTest(self, x, y):
        rect = draw_cairo.posCI + draw_cairo.tailleCI
        if dansRectangle(x, y, (rect,)):
            self.arbre.DoSelectItem(self.branche)
        
            
            
####################################################################################
#
#   Classe définissant les propriétés d'une compétence
#
####################################################################################
class Competence():
    def __init__(self, parent, panelParent, numComp = None):
        self.clefs = Competences.keys()
        self.clefs.sort()
        self.parent = parent
        self.num = numComp
        
        self.SetNum(numComp)
        
        self.panelPropriete = PanelPropriete_Competence(panelParent, self)
        
    ######################################################################################  
    def __repr__(self):
        return self.code
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
        print "getBranche Comp",
        if hasattr(self, 'code'):
            print self.code
            root = ET.Element(self.code)
        else:
            print
            root = ET.Element("")
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        code = branche.tag
        num = Competences.keys().index(code)
        self.SetNum(num)
        self.panelPropriete.MiseAJour()
#        self.SetCode()
        
         
    ######################################################################################  
    def SetNum(self, num):
        self.num = num
        if num != None:
            self.code = self.clefs[self.num]
            self.competence = Competences[self.code]
            
            if hasattr(self, 'arbre'):
                self.SetCode()
        
    ######################################################################################  
    def SetCode(self):
        self.codeBranche.SetLabel(self.code)
        

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Compétence :", wnd = self.codeBranche, data = self,
                                        image = self.arbre.images["Com"])
        
        
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
    def __init__(self, parent, panelParent, typeSeance = "", typeParent = 0):
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
        self.intituleDansDeroul = True
        self.effectif = "C"
        self.demarche = "I"
        self.systemes = []
        for i in range(8):
            self.systemes.append(Variable(u"", lstVal = 0, nomNorm = "", typ = VAR_ENTIER_POS, 
                                 bornes = [0,8], modeLog = False,
                                 expression = None, multiple = False))
        
        # Les autres données
        self.typeParent = typeParent
        self.parent = parent
        self.panelParent = panelParent
        
        self.SetType(typeSeance)
        self.sousSeances = []
        
        
        self.MiseAJourListeSystemes()
        
        self.panelPropriete = PanelPropriete_Seance(panelParent, self)
        self.panelPropriete.AdapterAuType()
        
        
        
        
    
    ######################################################################################  
    def __repr__(self):
        t = self.typeSeance + self.code 
#        t += " " +str(self.GetDuree()) + "h"
#        t += " " +str(self.effectif)
#        for s in self.sousSeances:
#            t += "  " + s.__repr__()
        return t
    
    ######################################################################################  
    def GetApp(self):
        return self.parent.GetApp()
    
    ######################################################################################  
    def EstSousSeance(self):
        return not isinstance(self.parent, Sequence)
    
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la séance pour enregistrement
        """
#        print "getBranche Séance", self.code
        root = ET.Element("Seance"+str(self.ordre))
        root.set("Type", self.typeSeance)
        root.set("Intitule", self.intitule)
        
        
        if self.typeSeance in ["R", "S"]:
            for sce in self.sousSeances:
                root.append(sce.getBranche())
        elif self.typeSeance in ["AP", "ED", "P"]:
            root.set("Demarche", self.demarche)
            root.set("Duree", str(self.duree.v[0]))
            root.set("Effectif", self.effectif)
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
#        print "setBranche séance", 
        self.ordre = eval(branche.tag[6:])
        
        self.intitule  = branche.get("Intitule", "")
        self.typeSeance = branche.get("Type", "C")
        
        if self.typeSeance in ["R", "S"]:
            self.sousSeances = []
            for sce in list(branche):
                seance = Seance(self, self.panelParent)
                self.sousSeances.append(seance)
                seance.setBranche(sce)
            self.duree.v[0] = self.GetDuree()
        elif self.typeSeance in ["AP", "ED", "P"]:   
            self.effectif = branche.get("Effectif", "C")
            self.demarche = branche.get("Demarche", "I")
            for i, s in enumerate(list(branche)):
                nom = s.get("Nom", "")
                nombre = eval(s.get("Nombre", ""))
                self.systemes[i].n = nom
                self.systemes[i].v = [nombre]
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        else:
            self.effectif = branche.get("Effectif", "C")
            self.duree.v[0] = eval(branche.get("Duree", "1"))
        
        self.intituleDansDeroul = eval(branche.get("IntituleDansDeroul", "True"))
        
        self.MiseAJourListeSystemes()
        self.panelPropriete.MiseAJour()
#        print self
        
    ######################################################################################  
    def GetEffectif(self):
        """ Renvoie l'effectif de la séance
            1 = P
            2 = E
            4 = D
            8 = G
            16 = C
        """
        eff = 0
        if self.typeSeance == "R":
            eff += self.sousSeances[0].GetEffectif()
        elif self.typeSeance == "S":
            for sce in self.sousSeances:
                eff += sce.GetEffectif()
        else:
            if self.effectif == "C":
                eff = 16
            elif self.effectif == "G":
                eff = 8
            elif self.effectif == "D":
                eff = 4
            elif self.effectif == "E":
                eff = 2
            elif self.effectif == "P":
                eff = 1
            else:
                eff = 0
#        print "effectif", self, eff
        return eff
    
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
            if self.typeSeance == "R":
                for s in self.sousSeances:
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
            for k, v in Effectifs.items():
                if v[0] == val:
                    codeEff = k
        self.effectif = codeEff
        

    ######################################################################################  
    def VerifPb(self):
        self.SignalerPbEffectif(self.IsEffectifOk())
        if self.EstSousSeance():
            for s in self.sousSeances:
                self.VerifPb()
        
    ######################################################################################  
    def IsEffectifOk(self):
        """ Teste s'il y a un problème d'effectif pour les séances en rotation ou en parallèle
            0 : pas de problème
            1 : tout le groupe "effectif réduit" n'est pas occupé
            2 : effectif de la séance supperieur à celui du groupe "effectif réduit"
            3 : séances en rotation d'effectifs différents !!
        """
#        print "IsEffectifOk",
        ok = 0 # pas de problème
        if self.typeSeance in ["R", "S"] and len(self.sousSeances) > 0:
            if self.GetEffectif() < 8:
                ok = 1 # Tout le groupe "effectif réduit" n'est pas occupé
            if self.typeSeance == "R":
                continuer = True
                eff = self.sousSeances[0].GetEffectif()
                i = 1
                while continuer:
                    if i >= len(self.sousSeances):
                        continuer = False
                    else:
                        if self.sousSeances[i].GetEffectif() != eff:
                            ok = 3 # séance en rotation d'effectifs différents !!
                            continuer = False
                        i += 1
            elif self.typeSeance == "S":
                if self.GetEffectif() > 16:
                    ok = 2 # Effectif de la séance supperieur à celui du groupe "effectif réduit"
         
#        print ok
        return ok
            
    
    
    ######################################################################################  
    def SignalerPbEffectif(self, etat):
        if hasattr(self, 'codeBranche'):
            if etat == 0:
                self.codeBranche.SetBackgroundColour('white')
                self.codeBranche.SetToolTipString(u"")
            elif etat == 1 :
                self.codeBranche.SetBackgroundColour('gold')
                self.codeBranche.SetToolTipString(u"Tout le groupe \"effectif réduit\" n'est pas occupé")
            elif etat == 2:
                self.codeBranche.SetBackgroundColour('orange')
                self.codeBranche.SetToolTipString(u"Effectif de la séance supperieur à celui du groupe \"effectif réduit\"")
            elif etat == 3:
                self.codeBranche.SetBackgroundColour('red')
                self.codeBranche.SetToolTipString(u"Séances en rotation d'effectifs différents !!")
            self.codeBranche.Refresh()
    
    ######################################################################################  
    def GetDuree(self):
        duree = 0
        if self.typeSeance == "R":
            for sce in self.sousSeances:
                duree += sce.GetDuree()
        elif self.typeSeance == "S":
            duree += self.sousSeances[0].GetDuree()
        else:
            duree = self.duree.v[0]
        return duree
                
                
                
    ######################################################################################  
    def SetDuree(self, duree, recurs = True):
        """ Modifie la durée des Rotation et séances en Parallèle et de tous leurs enfants
            après une modification de durée d'un des enfants
        """
#        print "SetDuree"
        if recurs and self.EstSousSeance() and self.parent.typeSeance in ["R", "S"]: # séance en rotation (parent = séance "Rotation")
            self.parent.SetDuree(duree)

        
        elif self.typeSeance == "S" : # Serie
            self.duree.v[0] = duree
            for s in self.sousSeances:
                if s.typeSeance in ["R", "S"]:
                    s.SetDuree(duree, recurs = False)
                else:
                    s.duree.v[0] = duree
                    s.panelPropriete.MiseAJourDuree()
            self.panelPropriete.MiseAJourDuree()

        
        elif self.typeSeance == "R" : # Serie
            for s in self.sousSeances:
                if s.typeSeance in ["R", "S"]:
                    s.SetDuree(duree, recurs = False)
                else:
                    s.duree.v[0] = duree
                    s.panelPropriete.MiseAJourDuree()
            self.duree.v[0] = self.GetDuree()
            self.panelPropriete.MiseAJourDuree()

        
            
        
    ######################################################################################  
    def SetIntitule(self, text):           
        self.intitule = text
        
#    ######################################################################################  
#    def SetEffectif(self, text):   
#        for k, v in Effectifs.items():
#            if v[0] == text:
#                codeEff = k
#        self.effectif = codeEff
           
    
    ######################################################################################  
    def SetDemarche(self, text):   
        for k, v in Demarches.items():
            if v[0] == text[0]:
                codeDem = k
        self.demarche = codeDem
        
        
    ######################################################################################  
    def SetType(self, typ):
#        print "SetType", typ
        if type(typ) == str:
            self.typeSeance = typ
        else:
            self.typeSeance = listeTypeSeance[typ]
            
        if hasattr(self, 'arbre'):
            self.SetCode()
        
        if self.typeSeance in ["R","S"] and len(self.sousSeances) == 0: # Rotation ou Serie
            self.AjouterSeance()
        
        if hasattr(self, 'panelPropriete'):
            self.panelPropriete.AdapterAuType()
        
        if self.EstSousSeance() and self.parent.typeSeance in ["R","S"]:
            self.parent.SignalerPbEffectif(self.parent.IsEffectifOk())
        
    ######################################################################################  
    def GetToutesSeances(self):
        l = []
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            l.extend(self.sousSeances)
            for s in self.sousSeances:
                l.extend(s.GetToutesSeances())
        return l
        
        
    ######################################################################################  
    def SetCode(self):
#        print "SetCode",
        self.code = self.typeSeance
        num = str(self.ordre+1)
        if isinstance(self.parent, Seance):
            num = str(self.parent.ordre+1)+"."+num
            if isinstance(self.parent.parent, Seance):
                num = str(self.parent.parent.ordre+1)+"."+num

        self.code += num
#        print self.code
        if hasattr(self, 'codeBranche'):
            self.codeBranche.SetLabel(self.code)
            self.arbre.SetItemText(self.branche, TypesSeanceCourt[self.typeSeance])
#        else:
#            self.codeBranche.SetLabel("??")
#            self.arbre.SetItemText(self.branche, u"Séance :")
        
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for sce in self.sousSeances:
                sce.SetCode()

        
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Séance :", wnd = self.codeBranche, data = self)
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for sce in self.sousSeances:
                sce.ConstruireArbre(arbre, self.branche)
            
        
    ######################################################################################  
    def OrdonnerSeances(self):
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for i, sce in enumerate(self.sousSeances):
                sce.ordre = i
        
        self.SetCode()
        
            
    ######################################################################################  
    def AjouterSeance(self, event = None):
        """ Ajoute une séance é la séance
            !! Uniquement pour les séances de type "Rotation" ou "Serie" !!
        """
        seance = Seance(self, self.panelParent)
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            self.sousSeances.append(seance)
            
        self.OrdonnerSeances()
        seance.ConstruireArbre(self.arbre, self.branche)
        self.arbre.Expand(self.branche)



    ######################################################################################  
    def SupprimerSeance(self, event = None, item = None):
        if self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            if len(self.sousSeances) > 1: # On en laisse toujours une !!
                seance = self.arbre.GetItemPyData(item)
                self.sousSeances.remove(seance)
                self.arbre.Delete(item)
                self.OrdonnerSeances()
        return
    
    ######################################################################################  
    def SupprimerSousSeances(self):
        self.arbre.DeleteChildren(self.branche)
        return
    
    ######################################################################################  
    def MiseAJourListeSystemes(self):
#        print "MiseAJourListeSystemes", self
        if self.typeSeance in ["AP", "ED", "P", "C", "SS", "SA", "E"]:
            sequence = self.GetSequence()
            for i, s in enumerate(sequence.systemes):
                self.systemes[i].n = s.nom
            self.nSystemes = len(sequence.systemes)
            
        elif self.typeSeance in ["R", "S"] : # Séances en Rotation ou  Parallèle
            for s in self.sousSeances:
                s.MiseAJourListeSystemes()
        
    
    def GetSequence(self):    
        if self.EstSousSeance():
            if self.parent.EstSousSeance():
                sequence = self.parent.parent.parent
            else:
                sequence = self.parent.parent
        else:
            sequence = self.parent
        return sequence
    
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            listItems = [[u"Supprimer", functools.partial(self.parent.SupprimerSeance, item = itemArbre)]]
            if self.typeSeance in ["R", "S"]:
                listItems.append([u"Ajouter une séance", self.AjouterSeance])
            self.GetApp().AfficherMenuContextuel(listItems)
#            item2 = menu.Append(wx.ID_ANY, u"Créer une rotation")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterRotation, item = item), item2)
#            
#            item3 = menu.Append(wx.ID_ANY, u"Créer une série")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterSerie, item = item), item3)
            
#    ######################################################################################  
#    def Draw(self, ctx, curseur, typParent = "", rotation = False):
#        if not self.EstSousSeance():
#            h = cf.hHoraire * self.GetDuree()
#            fleche_verticale(ctx, cf.posZDeroul[0], curseur[1], 
#                             h, 0.02, (0.9,0.8,0.8,0.5))
#            ctx.set_source_rgb(0.5,0.8,0.8)
#            show_text_rect(ctx, getHoraireTxt(self.GetDuree()), cf.posZDeroul[0]-0.01, curseur[1], 
#                           0.02, h, orient = 'v')
#            
#            
#        if not self.typeSeance in ["R", "S", ""]:
##            print "Draw", self
#            x, y = curseur
#            w = cf.wEff[self.effectif]
#            h = cf.hHoraire * self.GetDuree()
#            if rotation:
#                self.rect.append((x, y, w, h))
#            else:
#                self.rect=[(x, y, w, h),] # Rectangles pour clic
#            ctx.set_line_width(0.002)
#            if rotation:
#                alpha = 0.2
#            else:
#                alpha = 1
#            rectangle_plein(ctx, x, y, w, h, 
#                            cf.BCoulSeance[self.typeSeance], cf.ICoulSeance[self.typeSeance], alpha)
#            if not rotation and self.typeSeance in ["AP", "ED", "P"]:
#                if self.EstSousSeance() and self.parent.typeSeance == "S":
#                    ns = len(self.parent.sousSeances)
#                    ys = y+(self.ordre+1) * h/(ns+1)
##                    print ns, ys, self.ordre
#                else:
#                    ys = y+h/2
#                self.DrawCroisements(ctx, x+w, ys)
#                self.DrawCroisementSystemes(ctx, ys)
#                
#            
#            if not rotation and hasattr(self, 'code'):
#                ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                      cairo.FONT_WEIGHT_BOLD)
#                ctx.set_source_rgb (0,0,0)
#                show_text_rect(ctx, self.code, x, y, cf.wEff["P"], cf.hHoraire/4, ha = 'g')
#            
#            if not rotation and self.intituleDansDeroul and self.intitule != "":
#                ctx.select_font_face ("Sans", cairo.FONT_SLANT_ITALIC,
#                                      cairo.FONT_WEIGHT_NORMAL)
#                ctx.set_source_rgb (0,0,0)
#                show_text_rect(ctx, self.intitule, x, y + cf.hHoraire/4, 
#                               w, h-cf.hHoraire/4, ha = 'g')
#                
#            if typParent == "R":
#                curseur[1] += h
#            elif typParent == "S":
#                curseur[0] += w
#            else:
#                curseur[1] += h + cf.ecartSeanceY
#        else:
#            if self.typeSeance in ["R", "S"]:
#                for s in self.sousSeances:
#                    s.Draw(ctx, curseur, typParent = self.typeSeance, rotation = rotation)
##                    if self.typeSeance == "S":
#                
#                #
#                # Aperçu en filigrane de la rotation
#                #
#                if self.typeSeance == "R" and self.IsEffectifOk() < 2:
#                    l = self.sousSeances
#                    eff = self.GetEffectif()
#                    if eff == 16:
#                        codeEff = "C"
#                    elif eff == 8:
#                        codeEff = "G"
#                    elif eff == 4:
#                        codeEff = "D"
#                    elif eff == 2:
#                        codeEff = "E"
#                    elif eff == 1:
#                        codeEff = "P"
#                    curs = [curseur[0]+cf.wEff[codeEff], curseur[1]-cf.hHoraire * self.GetDuree()]
#                    for t in range(len(self.sousSeances)-1):
#                        l = permut(l)
#                        for s in l:
#                            s.Draw(ctx, curs, typParent = "R", rotation = True)
#                        curs[0] += cf.wEff[s.effectif]
#                
#                
#                curseur[0] = cf.posZSeances[0]
#                if typParent == "":
#                    curseur[1] += cf.ecartSeanceY
#                if self.typeSeance == "S":
#                    curseur[1] += cf.hHoraire * self.GetDuree()
#
#                
#        
##        # 
##        # Croisement Seance/Systèmes
##        #
##        
##        if self.typeSeance in ["AP", "ED", "P"]:
###            and not (self.EstSousSeance() and self.parent.typeSeance == "S"):
##            ns = self.GetNbrSystemes()
##            for s, n in ns.items():
##                if n > 0:
##                    _x, _y = cf.xSystemes[s], curseur[1]+cf.hHoraire * self.GetDuree()/2
##                    self.DrawCroisementSystemes(ctx, _x, _y, n)
##        elif self.typeSeance == "S":
##            self.DrawCroisements(ctx, x+w, y+h/2)
##            ns = self.GetNbrSystemes()
##            for s, n in ns.items():
##                if n > 0:
##                    _x, _y = cf.xSystemes[s], curseur[1]-cf.hHoraire * self.GetDuree()/2- cf.ecartY
##                    self.DrawCroisementSystemes(ctx, _x, _y, n)
#            
#            
#            
#    ######################################################################################  
#    def DrawCroisementSystemes(self, ctx, y):
##        if self.typeSeance in ["AP", "ED", "P"]:
##            and not (self.EstSousSeance() and self.parent.typeSeance == "S"):
#        r = 0.01
#        ns = self.GetNbrSystemes()
#        for s, n in ns.items():
#            if n > 0:
#                x = cf.xSystemes[s]
#                ctx.arc(x, y, r, 0, 2*pi)
#                ctx.set_source_rgba (1,0.2,0.2,0.6)
#                ctx.fill_preserve ()
#                ctx.set_source_rgba (0,0,0,1)
#                ctx.stroke ()
#                ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                      cairo.FONT_WEIGHT_BOLD)
#                show_text_rect(ctx, str(n), x-r, y-r, 2*r, 2*r)
#                self.rect.append((x-r, y-r, 2*r, 2*r))
#            
            
    ######################################################################################  
    def GetNbrSystemes(self):
        d = {}
        if not self.typeSeance == "S":
            for s in self.systemes:
                if s.n <>"":
                    d[s.n] = s.v[0]
        else:
            for seance in self.sousSeances:
                for s in seance.systemes:
                    if s.n <>"":
                        if d.has_key(s.n):
                            d[s.n] += s.v[0]
                        else:
                            d[s.n] = s.v[0]
        return d
    
#    ######################################################################################  
#    def DrawCroisements(self, ctx, x, y):
#    
#        #
#        # Les lignes horizontales
#        #
#        if self.typeSeance in ["AP", "ED", "P"]:
#            self.DrawLigne(ctx, x, y)
#            
#        #
#        # Croisements Séance/Démarche
#        #
#        _x = cf.xDemarche[self.demarche]
##        if self.typeSeance in ["AP", "ED", "P"]:
#        r = 0.008
#        boule(ctx, _x, y, r)
#        self.rect.append((_x -r , y - r, 2*r, 2*r))
##        ctx.arc (_x, y, 0.006, 0, 2*pi)
##        ctx.stroke ()


                
#    ######################################################################################  
#    def DrawLigne(self, ctx, x, y):
#        dashes = [ 0.010,   # ink
#                   0.002,   # skip
#                   0.005,   # ink
#                   0.002,   # skip
#                   ]
#        ctx.set_source_rgba (0, 0.0, 0.2, 0.6)
#        ctx.set_line_width (0.001)
#        ctx.set_dash(dashes, 0)
#        ctx.move_to(draw_cairo.posZOrganis[0]+draw_cairo.tailleZOrganis[0], y)
#        ctx.line_to(x, y)
#        ctx.stroke()
#        ctx.set_dash([], 0)
        
        
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
            self.arbre.DoSelectItem(self.branche)
        else:
            if self.typeSeance in ["R", "S"]:
                ls = self.sousSeances
            else:
                return
            continuer = True
            i = 0
            while continuer:
                if i >= len(ls):
                    continuer = False
                else:
                    if ls[i].HitTest(x, y):
                        continuer = False
                i += 1

####################################################################################
#
#   Classe définissant les propriétés d'un système
#
####################################################################################
class Systeme():
    def __init__(self, parent, panelParent, nom = u""):
        
        self.parent = parent
        self.nom = nom
        
        self.panelPropriete = PanelPropriete_Systeme(panelParent, self)
        
    ######################################################################################  
    def __repr__(self):
        return self.nom
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la compétence pour enregistrement
        """
        root = ET.Element("Systeme")
        root.set("Nom", self.nom)
        return root
    
    ######################################################################################  
    def setBranche(self, branche):
        nom  = branche.get("Nom", "")
        self.SetNom(nom)
        self.panelPropriete.MiseAJour()

        
         
    ######################################################################################  
    def SetNom(self, nom):
        self.nom = nom
        if nom != u"":
            if hasattr(self, 'arbre'):
                self.SetCode()
        
    ######################################################################################  
    def SetCode(self):
        self.codeBranche.SetLabel(self.nom)
        

    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Système :", wnd = self.codeBranche, data = self)
        
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerSysteme, item = itemArbre)]])
            
    ######################################################################################  
    def HitTest(self, x, y):
        if hasattr(self, 'rect') and dansRectangle(x, y, self.rect):
            self.arbre.DoSelectItem(self.branche)

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
#        print "AfficherPanel"
        if self.panel != None:
            self.bsizer.Remove(self.panel)
            self.panel.Hide()
        self.bsizer.Add(panel, flag = wx.EXPAND)
        self.panel = panel
        if isinstance(self.panel, PanelPropriete_Seance):
            self.panel.AdapterAuxSystemes()
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
        
        wx.Frame.__init__(self, None, -1, "")#, style = wx.DEFAULT_FRAME_STYLE | wx.SYSTEM_MENU)
#        self.SetExtraStyle(wx.FRAME_EX_CONTEXTHELP)
        #
        # Taille et position de la fenétre
        #
        self.SetMinSize((800,570)) # Taille mini d'écran : 800x600
        self.SetSize((1024,738)) # Taille pour écran 1024x768
        # On centre la fenétre dans l'écran ...
        self.CentreOnScreen(wx.BOTH)
        
#        
        # Use a panel under the AUI panes in order to work around a
        # bug on PPC Macs
        pnl = wx.Panel(self)
        self.pnl = pnl
        
        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(pnl)
        
        # panel de propriétés (conteneur)
        panelProp = PanelConteneur(pnl)
        
        #
        # le fichier de configuration de la fiche
        #
        self.nomFichierConfig = os.path.join(PATH,"configFiche.cfg")
        # on essaye de l'ouvrir
        try:
            draw_cairo.ouvrirConfigFiche(self.nomFichierConfig)
            print draw_cairo.posObj
        except:
            pass 
        
        #
        # La séquence
        #
        self.sequence = Sequence(self, panelProp)
        
        #
        # Arbre de structure de la séquence
        #
        arbreSeq = ArbreSequence(pnl, self.sequence, panelProp)
        self.arbreSeq = arbreSeq
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
        
        self.CreateMenuBar()
        
        wx.CallAfter(self.ficheSeq.Redessiner)
        self.Bind(EVT_SEQ_MODIFIED, self.OnSeqModified)
        
        self.Bind(wx.EVT_MENU, self.commandeOuvrir, id=11)
        self.Bind(wx.EVT_MENU, self.commandeEnregistrer, id=12)
        self.Bind(wx.EVT_MENU, self.exporterFiche, id=15)
        self.Bind(wx.EVT_MENU, self.quitter, id=wx.ID_EXIT)
        
        self.Bind(wx.EVT_MENU, self.OnAide, id=21)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=22)
        
        # Interception de la demande de fermeture
        self.Bind(wx.EVT_CLOSE, self.quitter)
        
        self.definirNomFichierCourant('')
#        sizer = wx.BoxSizer(wx.HORIZONTAL)
#        self.SetSizerAndFit(sizer)
    
    
    def CreateMenuBar(self):
        # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(11, u"Ouvrir")
        file_menu.Append(12, u"Enregistrer")
        file_menu.AppendSeparator()
        file_menu.Append(15, u"Exporter en PDF")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, u"Quitter")

        help_menu = wx.Menu()
        help_menu.Append(21, u"Aide en ligne")
        help_menu.AppendSeparator()
        help_menu.Append(22, u"A propos")

        mb.Append(file_menu, "&Fichier")
        mb.Append(help_menu, "&Aide")
        
        self.SetMenuBar(mb)
        
    ###############################################################################################
    def OnSeqModified(self, event):
        self.sequence.VerifPb()
        self.ficheSeq.Redessiner()
        self.MarquerFichierCourantModifie()
        
        
    ###############################################################################################
#    def OnSize(self, event):
#        print "OnSize fenetre",
#        w = self.panelCentral.GetClientSize()[0]
#        print w
#        self.panelCentral.SetVirtualSize((w,w*29/21)) # Mise au format A4
##        self.ficheSeq.FitInside()
#        
        
    ###############################################################################################
    def enregistrer(self, nomFichier):

        wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
        fichier = file(nomFichier, 'w')
        
        sequence = self.sequence.getBranche()
        
        indent(sequence)
        print sequence.text
        ET.ElementTree(sequence).write(fichier)
        fichier.close()
        self.definirNomFichierCourant(nomFichier)
        wx.EndBusyCursor()
        
    ###############################################################################################
    def ouvrir(self, nomFichier):
        print "ouvrir", nomFichier
        fichier = open(nomFichier,'r')
#        try:
        sequence = ET.parse(fichier).getroot()
        self.sequence.setBranche(sequence)
        
        self.arbreSeq.DeleteAllItems()
        self.sequence.ConstruireArbre(self.arbreSeq)
        self.sequence.SetCodes()
        self.arbreSeq.ExpandAll()
        
#        print self.sequence
#        except:
#            pass
        fichier.close()
        self.definirNomFichierCourant(nomFichier)
        self.ficheSeq.Redessiner()
        self.sequence.VerifPb()
        
        
    ###############################################################################################
    def commandeOuvrir(self, event = None, nomFichier=None):
        mesFormats = u"Séquence (.seq)|*.seq|" \
                       u"Tous les fichiers|*.*'"
  
        if nomFichier == None:
            dlg = wx.FileDialog(
                                self, message=u"Ouvrir une séquence",
                                defaultDir = self.DossierSauvegarde, 
                                defaultFile = "",
                                wildcard = mesFormats,
                                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                                )
                
            # Show the dialog and retrieve the user response. If it is the OK response, 
            # process the data.
            if dlg.ShowModal() == wx.ID_OK:
                # This returns a Python list of files that were selected.
                paths = dlg.GetPaths()
                nomFichier = paths[0]
            else:
                nomFichier = ''
            
            dlg.Destroy()
            
        self.Refresh()
        
        print ""
        if nomFichier != '':
            raz = True
                
            if raz:
                wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
                self.ouvrir(nomFichier)
                wx.EndBusyCursor()
        
    #############################################################################
    def dialogEnregistrer(self):
        mesFormats = u"Séquence (.seq)|*.seq|" \
                     u"Tous les fichiers|*.*'"
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
        self.SetTitle(__appname__ + t )

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
       
       
       
    #############################################################################
    def exporterFiche(self, event = None):
        mesFormats = "pdf (.pdf)|*.pdf|"
        dlg = wx.FileDialog(
            self, message=u"Enregistrer la fiche sous ...", defaultDir=self.DossierSauvegarde , 
            defaultFile="", wildcard=mesFormats, style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR
            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
            PDFsurface = cairo.PDFSurface(path, 595, 842)
            ctx = cairo.Context (PDFsurface)
            ctx.scale(820, 820) 
            self.sequence.Draw(ctx)
            self.DossierSauvegarde = os.path.split(path)[0]
        else:
            dlg.Destroy()
        return
    
    #############################################################################
    def quitter(self, event = None):
        try:
            draw_cairo.enregistrerConfigFiche(self.nomFichierConfig)
        except IOError:
            print "   Permission d'enregistrer les options refusée...",
        except:
            print "   Erreur enregistrement options...",
            
#        event.Skip()
        if not self.fichierCourantModifie:
            self.fermer()
            return
        
        texte = u"La séquence a été modifiée.\nVoulez vous enregistrer les changements ?"
        if self.fichierCourant != '':
            texte += "\n\n\t"+self.fichierCourant+"\n"
            
        dialog = wx.MessageDialog(self, texte, 
                                  u"Confirmation", wx.YES_NO | wx.CANCEL | wx.ICON_WARNING)
        retCode = dialog.ShowModal()
        if retCode == wx.ID_YES:
            self.commandeEnregistrer()
            self.fermer()
        elif retCode == wx.ID_NO:
            self.fermer()


    #############################################################################
    def fermer(self):
        self.Destroy()
        sys.exit()
        
    #############################################################################
    def OnAbout(self, event):
        win = A_propos(self)
        win.ShowModal()
        
    #############################################################################
    def OnAide(self, event):
        webbrowser.open('http://code.google.com/p/pysequence/wiki/Aide')
        
        
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
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)

    
    #############################################################################            
    def OnClick(self, evt):
#        print "OnClick"
        x, y = evt.GetX(), evt.GetY()
        _x, _y = self.CalcUnscrolledPosition(x, y)
        xx, yy = self.ctx.device_to_user(_x, _y)
#        print "  ", xx, yy
        self.sequence.HitTest(xx, yy)

    #############################################################################            
    def OnResize(self, evt):
#        print "OnSize fiche",
        w = self.GetClientSize()[0]
#        print w
        self.SetVirtualSize((w,w*29/21)) # Mise au format A4
#        self.ficheSeq.FitInside()

        self.InitBuffer()
        if w > 0:
            self.Redessiner()


    #############################################################################            
    def OnPaint(self, evt):
#        print "PAINT"
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

#        self.Redessiner()
        
        
    #############################################################################            
    def InitBuffer(self):
        w,h = self.GetVirtualSize()
#        print "InitBuffer", w, h
        self.buffer = wx.EmptyBitmap(w,h)

        
    #############################################################################            
    def Redessiner(self, event = None):  
#        print "REDESSINER"
        cdc = wx.ClientDC(self)
        dc = wx.BufferedDC(cdc, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        ctx = wx.lib.wxcairo.ContextFromDC(dc)
        dc.BeginDrawing()
        self.normalize(ctx)
        draw_cairo.Draw(ctx, self.sequence)
        dc.EndDrawing()
        self.ctx = ctx
        self.Refresh()

    #############################################################################            
    def normalize(self, cr):
        w,h = self.GetVirtualSize()
#        print "normalize", h
        cr.scale(h, h) 
        
        
        
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
        
        
    #############################################################################            
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
        wx.Panel.__init__(self, parent, -1, size = (-1, 200))#, style = wx.BORDER_SIMPLE)
        
#        self.boxprop = wx.StaticBox(self, -1, u"")
        self.sizer = wx.GridBagSizer(5, 5)
        self.Hide()
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
       
    #########################################################################################################
    def sendEvent(self):
        evt = SeqEvent(myEVT_SEQ_MODIFIED, self.GetId())
        self.GetEventHandler().ProcessEvent(evt)



####################################################################################
#
#   Classe définissant le panel de propriété de séquence
#
####################################################################################
class PanelPropriete_Sequence(PanelPropriete):
    def __init__(self, parent, sequence):
        PanelPropriete.__init__(self, parent)
        self.sequence = sequence
        
        titre = wx.StaticText(self, -1, u"Intitulé de la séquence:")
        textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        self.textctrl = textctrl
        
        self.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        self.sizer.Add(textctrl, (0,1), flag = wx.EXPAND)
        self.sizer.AddGrowableCol(1)
        self.sizer.Layout()
        
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
    
    #############################################################################            
    def EvtText(self, event):
        self.sequence.SetText(event.GetString())
        self.sendEvent()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.textctrl.ChangeValue(self.sequence.intitule)
        if sendEvt:
            self.sendEvent()
        
####################################################################################
#
#   Classe définissant le panel de propriété du CI
#
####################################################################################
class PanelPropriete_CI(PanelPropriete):
    def __init__(self, parent, CI):
        PanelPropriete.__init__(self, parent)
        self.CI = CI
        
        titre = wx.StaticText(self, -1, u"CI :")
        cb = wx.ComboBox(self, -1, u"Choisir un CI",
                         choices = CentresInterets,
                         style = wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         | wx.CB_READONLY
                         #| wx.CB_SORT
                         )
        self.cb = cb
        self.titre = titre
        
        self.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        self.sizer.Add(cb, (0,1), flag = wx.EXPAND)
        self.sizer.Layout()
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        
    #############################################################################            
    def EvtComboBox(self, event):
        self.CI.SetNum(event.GetSelection())
        self.titre.SetLabel(u"CI "+str(self.CI.num+1)+":")
        self.Layout()
        self.sendEvent()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.titre.SetLabel(u"CI "+str(self.CI.num+1)+":")
        self.cb.SetSelection(self.CI.num)
        self.Layout()
        if sendEvt:
            self.sendEvent()
        
####################################################################################
#
#   Classe définissant le panel de propriété de la compétence
#
####################################################################################
class PanelPropriete_Competence(PanelPropriete):
    def __init__(self, parent, competence):
        
        self.competence = competence
        
        
        PanelPropriete.__init__(self, parent)
        
        titre = wx.StaticText(self, -1, u"Compétence :")
        
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
        self.cb = cb
        
        self.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        self.sizer.Add(cb, (0,1), flag = wx.EXPAND)
        self.sizer.Layout()
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        
    #############################################################################            
    def EvtComboBox(self, event):
        self.competence.SetNum(event.GetSelection())
        self.sendEvent()
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.cb.SetSelection(self.competence.num)
        if sendEvt:
            self.sendEvent()
        
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
        titre = wx.StaticText(self, -1, u"Type :")
        cbType = wx.ComboBox(self, -1, u"Choisir un type de séance",
                             choices = [],
                             style = wx.CB_DROPDOWN
                             | wx.TE_PROCESS_ENTER
                             | wx.CB_READONLY
                             #| wx.CB_SORT
                             )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cbType)
        self.cbType = cbType
        self.sizer.Add(titre, (0,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        self.sizer.Add(cbType, (0,1), flag = wx.EXPAND)
        
        #
        # Intitulé de la séance
        #
        box = wx.StaticBox(self, -1, u"Intitulé")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        textctrl = wx.TextCtrl(self, -1, u"", style=wx.TE_MULTILINE)
        bsizer.Add(textctrl, flag = wx.EXPAND)
        self.textctrl = textctrl
        self.Bind(wx.EVT_TEXT, self.EvtTextIntitule, textctrl)
        
        cb = wx.CheckBox(self, -1, u"Montrer dans la zone de déroulement de la séquence")
        cb.SetValue(self.seance.intituleDansDeroul)
        bsizer.Add(cb, flag = wx.EXPAND)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
        self.cbInt = cb
        self.sizer.Add(bsizer, (1,0), (1,2), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
#        self.sizer.Add(textctrl, (1,1), flag = wx.EXPAND)
        
        #
        # Durée de la séance
        #
        vcDuree = VariableCtrl(self, seance.duree, coef = 0.5, labelMPL = False, signeEgal = True, slider = False, fct = None, help = "")
#        textctrl = wx.TextCtrl(self, -1, u"1")
        self.Bind(EVT_VAR_CTRL, self.EvtText, vcDuree)
        self.vcDuree = vcDuree
        self.sizer.Add(vcDuree, (2,0), (1, 2))
        
        #
        # Effectif
        #
        titre = wx.StaticText(self, -1, u"Effectif :")
        cbEff = wx.ComboBox(self, -1, u"",
                         choices = [],
                         style = wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         | wx.CB_READONLY
                         #| wx.CB_SORT
                         )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxEff, cbEff)
        self.cbEff = cbEff
        self.titreEff = titre
        
        nombre = wx.StaticText(self, -1, u"")
        self.nombre = nombre
        
        self.sizer.Add(titre, (3,0), flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        self.sizer.Add(cbEff, (3,1), flag = wx.EXPAND)
        self.sizer.Add(self.nombre, (3,2))
        
        #
        # Démarche
        #
        titre = wx.StaticText(self, -1, u"Démarche :")
        cbDem = wx.ComboBox(self, -1, u"",
                         choices = [],
                         style = wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         | wx.CB_READONLY
                         #| wx.CB_SORT
                         )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBoxDem, cbDem)
        self.cbDem = cbDem
        self.titreDem = titre
        
        nombre = wx.StaticText(self, -1, u"")
        self.nombre = nombre
        
        self.sizer.Add(titre, (4,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT, border = 2)
        self.sizer.Add(cbDem, (4,1), flag = wx.EXPAND)
        self.sizer.Add(self.nombre, (4,2))
        
        #
        #Systèmes
        #
        self.box = wx.StaticBox(self, -1, u"Systèmes nécessaires")
        self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        self.systemeCtrl = []
        for s in range(8):
            v = VariableCtrl(self, seance.systemes[s], labelMPL = False, signeEgal = False, slider = False, fct = None, help = "")
            self.Bind(EVT_VAR_CTRL, self.EvtVarSysteme, v)
            self.bsizer.Add(v, flag = wx.ALIGN_RIGHT) 
            self.systemeCtrl.append(v)
        self.sizer.Add(self.bsizer, (0,4), (5, 1), flag = wx.EXPAND)
#        self.sizer.AddGrowableCol(4, proportion = 1)

        #
        # Mise en place
        #
        self.sizer.Layout()
    
    
    #############################################################################            
    def EvtVarSysteme(self, event):
        self.sendEvent()
        
    #############################################################################            
    def EvtCheckBox(self, event):
        self.seance.intituleDansDeroul = event.IsChecked()
        self.sendEvent()
    
    #############################################################################            
    def EvtTextIntitule(self, event):
        self.seance.SetIntitule(event.GetString())
        self.sendEvent()
        
    #############################################################################            
    def EvtText(self, event):
        self.seance.SetDuree(event.GetVar().v[0])
        self.sendEvent()
        
    #############################################################################            
    def EvtComboBox(self, event):
        print "EvtComboBox type"
        if self.seance.typeSeance in ["R", "S"] and listeTypeSeance[event.GetSelection()] not in ["R", "S"]:
            dlg = wx.MessageDialog(self, u"Modifier le type de cette séance entrainera la suppression de toutes les sous séances !\n" \
                                         u"Voulez-vous continuer ?",
                                    u"Modification du type de séance",
                                    wx.YES_NO | wx.ICON_EXCLAMATION
                                    #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                    )
            res = dlg.ShowModal()
            dlg.Destroy() 
            if res == wx.ID_NO:
                return
            else:
                self.seance.SupprimerSousSeances()
        self.seance.SetType(get_key(TypesSeance, self.cbType.GetStringSelection()))
        if self.cbEff.IsEnabled():
            self.seance.SetEffectif(self.cbEff.GetStringSelection())

        self.seance.MiseAJourListeSystemes()
        self.AdapterAuxSystemes()
        self.Fit()
        self.sendEvent()
       
        
        
    #############################################################################            
    def EvtComboBoxEff(self, event):
        print "EvtComboBoxEff", self,
        self.seance.SetEffectif(event.GetString())  
        print self.seance.effectif
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
        self.nombre.SetLabel(u" (" + str(n) + u" élèves)")
        self.sendEvent()


    #############################################################################            
    def EvtComboBoxDem(self, event):
        print "EvtComboBoxDem", event.GetString()
         
        self.seance.SetDemarche(event.GetString())  
        
        self.sendEvent()
        
        
    #############################################################################            
    def AdapterAuxSystemes(self):
        self.Freeze()
        print "AdapterAuxSystemes"
        if self.seance.typeSeance in ["AP", "ED", "P"]:
            self.box.Show()
            for i in range(self.seance.nSystemes):
                s = self.seance.systemes[i]
                self.systemeCtrl[i].Renommer(s.n)
#                self.systemeCtrl[i].mofifierValeursSsEvt()
                self.systemeCtrl[i].Show()
            for sc in self.systemeCtrl[self.seance.nSystemes:]:
                sc.Hide()
        else:
            self.box.Hide()
            for sc in self.systemeCtrl:
                sc.Hide()
        self.Layout()
#        self.Fit()
        self.Thaw()
    
      
    #############################################################################            
    def AdapterAuType(self):
        """ Adapte le panel au type de séance
        """
        print "AdapterAuType"
        
        # Type de parent
        if self.seance.EstSousSeance():
            listType = listeTypeActivite
            if not self.seance.parent.EstSousSeance():
                listType += ["S"]
        else:
            listType = listeTypeSeance
        
#        if self.seance.typeSeance == "R":       #  séance en rotation
#            listType = listeTypeSeance
#        elif self.seance.typeSeance == "S":     #  séance en série
#            listType = listeTypeSeance
#        else:                                   #  séance "normale" (parent = séquence)
#            listType = listeTypeActivite          
        
        listTypeS = []
        for t in listType:
            listTypeS.append(TypesSeance[t])
        
        n = self.cbType.GetSelection()   
        self.cbType.Clear()
        for s in listTypeS:
            self.cbType.Append(s)
        self.cbType.SetSelection(n)
        
        # Durée
        if self.seance.typeSeance in ["R", "S"]:
            self.vcDuree.Activer(False)
        
        # Effectif
        if self.seance.typeSeance in ["C", "E", "SS"]:
            listEff = ["C"]
            self.cbEff.Show(True)
            self.titreEff.Show(True)
        elif self.seance.typeSeance in ["R", "S"] or self.seance.typeSeance == "":
            self.cbEff.Show(False)
            self.titreEff.Show(False)
            listEff = []
        elif self.seance.typeSeance in ["ED", "P"]:
            listEff = ["G", "D", "E", "P"]
            self.cbEff.Show(True)
            self.titreEff.Show(True)
        elif self.seance.typeSeance in ["AP"]:
            listEff = ["P", "E"]
            self.cbEff.Show(True)
            self.titreEff.Show(True)
        elif self.seance.typeSeance in ["SA"]:
            listEff = ["C", "G"]
            self.cbEff.Show(True)
            self.titreEff.Show(True)
        print listEff
#        n = self.cbEff.GetSelection()   
        self.cbEff.Clear()
        for s in listEff:
            self.cbEff.Append(Effectifs[s][0])
        self.cbEff.SetSelection(0)
        
        
        # Démarche
        if self.seance.typeSeance in ["AP", "ED"]:
            listDem = ["I", "R"]
            self.cbDem.Show(True)
            self.titreDem.Show(True)
        elif self.seance.typeSeance == "P":
            listDem = ["I", "R", "P"]
            self.cbDem.Show(True)
            self.titreDem.Show(True)
        else:
            self.cbDem.Show(False)
            self.titreDem.Show(False)
            listDem = []
        
        self.cbDem.Clear()
        for s in listDem:
            self.cbDem.Append(Demarches[s])
        self.cbDem.SetSelection(0)
        
    #############################################################################            
    def MarquerProblemeDuree(self, etat):
        return
        self.vcDuree.marquerValid(etat)
        
    #############################################################################            
    def MiseAJour(self, sendEvt = False):
        self.AdapterAuType()
        self.cbType.SetSelection(self.cbType.GetStrings().index(TypesSeance[self.seance.typeSeance]))
        self.textctrl.ChangeValue(self.seance.intitule)
        self.vcDuree.mofifierValeursSsEvt()
        if self.cbEff.IsEnabled() and self.cbEff.IsShown():
            self.cbEff.SetSelection(self.cbEff.GetStrings().index(Effectifs[self.seance.effectif][0]))
        
        if self.cbDem.IsEnabled() and self.cbDem.IsShown():
            self.cbDem.SetSelection(self.cbDem.GetStrings().index(Demarches[self.seance.demarche]))
            
        
        self.AdapterAuxSystemes()
        
        if self.seance.typeSeance in ["AP", "ED", "P"]:
            for i in range(self.seance.nSystemes):
                s = self.seance.systemes[i]
                self.systemeCtrl[i].mofifierValeursSsEvt()
        
        self.cbInt.SetValue(self.seance.intituleDansDeroul)
        
        if sendEvt:
            self.sendEvent()
    
    def MiseAJourDuree(self):
        self.vcDuree.mofifierValeursSsEvt()
    
####################################################################################
#
#   Classe définissant le panel de propriété d'un système
#
####################################################################################
class PanelPropriete_Systeme(PanelPropriete):
    def __init__(self, parent, systeme):
        
        self.systeme = systeme
        self.parent = parent
        
        PanelPropriete.__init__(self, parent)
        
        titre = wx.StaticText(self, -1, u"Nom du système :")
        
        # Prévoir un truc pour que la liste des compétences tienne compte de celles déja choisies
        # idée : utiliser cb.CLear, Clear.Append ou cb.Delete
        
        textctrl = wx.TextCtrl(self, -1, u"")
        self.textctrl = textctrl
        
        self.sizer.Add(titre, (0,0))
        self.sizer.Add(textctrl, (0,1), flag = wx.EXPAND)
        
        self.sizer.Layout()
        
        self.Bind(wx.EVT_TEXT, self.EvtText, textctrl)
        
        
        
    def EvtText(self, event):
        self.systeme.SetNom(event.GetString())
        self.systeme.parent.MiseAJourListeSystemes()
        self.sendEvent()
        
    def MiseAJour(self, sendEvt = False):
        self.textctrl.ChangeValue(self.systeme.nom)
        if sendEvt:
            self.sendEvent()
            
            
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
        dicimages = {"Seq" : images.Icone_sequence,
                       "Rot" : images.Icone_rotation,
                       "Cou" : images.Icone_cours,
                       "Com" : images.Icone_competence,
                       "Obj" : images.Icone_objectif,
                       "Ci" : images.Icone_centreinteret,
                       "Eva" : images.Icone_evaluation,
                       "Par" : images.Icone_parallele
                       }
        self.images = {}
        il = wx.ImageList(20, 20)
        for k, i in dicimages.items():
            self.images[k] = il.Add(i.GetBitmap())
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
        self.itemDrag = None
        
        #
        # Gestion des évenements
        #
        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(CT.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightDown)
        self.Bind(CT.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
        self.Bind(CT.EVT_TREE_END_DRAG, self.OnEndDrag)
        self.Bind(wx.EVT_MOTION, self.OnMove)
        
        self.ExpandAll()
        
        self.panelProp.AfficherPanel(self.sequence.panelPropriete)
        
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

    
#        self.CurseurInsert = wx.Cursor(wx.Image('CurseurInsert.png', wx.BITMAP_TYPE_PNG ))
#        self.CurseurInsert = wx.Cursor('CurseurInsert.ico', wx.BITMAP_TYPE_ICO )
        self.CurseurInsert = wx.CursorFromImage(images.CurseurInsert.GetImage())
        
        
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

    def OnCompareItems(self, item1, item2):
        i1 = self.GetItemPyData(item1)
        i2 = self.GetItemPyData(item2)
        return i1.ordre - i2.ordre

    def OnMove(self, event):
        if self.itemDrag != None:
            (id, flag) = self.HitTest(wx.Point(event.GetX(), event.GetY()))
            if id != None:
                dataTarget = self.GetItemPyData(id)
                dataSource = self.GetItemPyData(self.itemDrag)
                if not isinstance(dataSource, Seance):
                    self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
                else:
                    if not isinstance(dataTarget, Seance):
                        self.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
                    else:
                        if dataTarget != dataSource and dataTarget.parent == dataSource.parent:
                            self.SetCursor(self.CurseurInsert)
                        else:
                            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
                    
                        
        event.Skip()
        
    def OnBeginDrag(self, event):
        print "OnBeginDrag", 
        self.itemDrag = event.GetItem()
        print self.itemDrag
        if self.item:
            event.Allow()



    def OnEndDrag(self, event):
        print "OnEndDrag",
        self.item = event.GetItem()
        print self.itemDrag, self.item 
        dataTarget = self.GetItemPyData(self.item)
        dataSource = self.GetItemPyData(self.itemDrag)
        if not isinstance(dataSource, Seance):
            pass
        else:
            if not isinstance(dataTarget, Seance):
                pass
            else:
                if dataTarget != dataSource and dataTarget.parent == dataSource.parent:
                    if isinstance(dataTarget.parent, Sequence):
                        lst = dataTarget.parent.seance
                    else:
                        lst = dataTarget.parent.sousSeances
                    s = lst.index(dataSource)
                    t = lst.index(dataTarget)
                    lst[s] = dataTarget
                    lst[t] = dataSource
                    dataTarget.parent.OrdonnerSeances()
                    self.SortChildren(self.GetItemParent(self.item))
                    self.panelVide.sendEvent() # Solution pour déclencher un "redessiner"
                else:
                    pass
        self.itemDrag = None
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



def dansRectangle(x, y, rect):
    for r in rect:
        if x > r[0] and y > r[1] and x < r[0] + r[2] and y < r[1] + r[3]:
            return True
    return False

       

def get_key(dict, value):
    i = 0
    continuer = True
    while continuer:
        if i > len(dict.keys()):
            continuer = False
        else:
            if dict.values()[i] == value:
                continuer = False
                key = dict.keys()[i]
            i += 1
    return key


#def permut(liste):
#    l = []
#    for a in liste[1:]:
#        l.append(a)
#    l.append(liste[0])
#    return l
#    
#    
#def getHoraireTxt(v): 
#    h, m = divmod(v*60, 60)
#    h = str(int(h))
#    if m == 0:
#        m = ""
#    else:
#        m = str(int(m))
#    return h+"h"+m


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
    
#############################################################################################################
#
# A propos ...
# 
#############################################################################################################
class A_propos(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, u"A propos de "+ __appname__)
        
        self.app = parent
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        titre = wx.StaticText(self, -1, __appname__)
        titre.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, False))
        titre.SetForegroundColour(wx.NamedColour("BROWN"))
        sizer.Add(titre, border = 10)
        sizer.Add(wx.StaticText(self, -1, "Version : "+__version__), 
                  flag=wx.ALIGN_RIGHT)
#        sizer.Add(wx.StaticBitmap(self, -1, Images.Logo.GetBitmap()),
#                  flag=wx.ALIGN_CENTER)
        
#        sizer.Add(20)
        nb = wx.Notebook(self, -1, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        
        
        # Auteurs
        #---------
        auteurs = wx.Panel(nb, -1)
        fgs1 = wx.FlexGridSizer(cols=2, vgap=4, hgap=4)
        
        lstActeurs = ((u"Développement : ",(u"Cédrick FAURY", u"Jean-Claude FRICOU")),)#,
#                      (_(u"Remerciements : "),()) 


        
        for ac in lstActeurs:
            t = wx.StaticText(auteurs, -1, ac[0])
            fgs1.Add(t, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=4)
            for l in ac[1]:
                t = wx.StaticText(auteurs, -1, l)
                fgs1.Add(t , flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL| wx.ALL, border=4)
                t = wx.StaticText(auteurs, -1, "")
                fgs1.Add(t, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=0)
            t = wx.StaticText(auteurs, -1, "")
            fgs1.Add(t, flag=wx.ALL, border=0)
            
        auteurs.SetSizer(fgs1)
        
        # licence
        #---------
        licence = wx.Panel(nb, -1)
        try:
            txt = open(os.path.join(PATH, "gpl.txt"))
            lictext = txt.read()
            txt.close()
        except:
            lictext = u"Le fichier de licence (gpl.txt) est introuvable !\n" \
                      u"Veuillez réinstaller pySequence !"
            dlg = wx.MessageDialog(self, lictext,
                               'Licence introuvable',
                               wx.OK | wx.ICON_ERROR
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            
            
        wx.TextCtrl(licence, -1, lictext, size = (400, -1), 
                    style = wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_NONE )
        

        
        # Description
        #-------------
        descrip = wx.Panel(nb, -1)
        wx.TextCtrl(descrip, -1, wordwrap(u"pySequence est un logiciel d'aide à l'élaboration de séquences pédagogiques,\n"
                                          u"sous forme de fiches exportables au format PDF.\n"
                                          u"Il est élaboré en relation avec le programme et le document d'accompagnement\n"
                                          u"des enseignements technologiques transversaux de la filière STI2D.",
                                            500, wx.ClientDC(self)),
                        size = (400, -1),
                        style = wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_NONE) 
        
        nb.AddPage(descrip, u"Description")
        nb.AddPage(auteurs, u"Auteurs")
        nb.AddPage(licence, u"Licence")
        
        sizer.Add(hl.HyperLinkCtrl(self, wx.ID_ANY, u"Informations et téléchargement : http://code.google.com/p/pysequence/",
                                   URL="http://code.google.com/p/pysequence/"),  
                  flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
        sizer.Add(nb)
        
        self.SetSizerAndFit(sizer)

#        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

#    def OnCloseWindow(self, event):
##        evt = wx.CommandEvent(wx.EVT_TOOL.typeId, 16)
#        self.app.tb.ToggleTool(13, False)
##        self.app.tb.GetEventHandler().ProcessEvent(evt)
#        event.Skip()
    
if __name__ == '__main__':
    app = SeqApp(False)
    app.MainLoop()
    
    