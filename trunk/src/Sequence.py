#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
"""
Sequence.py
Aide � la r�alisation de fiches p�dagogiques de s�quence
*************
*   STIDD   *
*************
Copyright (C) 2011  
@author: Cedrick FAURY

"""
####################################################################################
#
#   Import des modules n�cessaires
#
####################################################################################
# Outils "syst�me"
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


####################################################################################
#
#   D�finition des constantes
#
####################################################################################
CentresInterets = [u"D�veloppement durable et comp�titivit� des produits",
                   u"Design, cr�ativit� et innovation",
                   u"Caract�ristiques des mat�riaux et structures",
                   u"Solutions constructives des mat�riaux et des structures",
                   u"Dimensionnement des structures et choix des mat�riaux",
                   u"Efficacit� �nerg�tique li�e au comportement des mat�riaux et des structures",
                   u"Formes et caract�ristiques de l'�nergie",
                   u"Organisation fonctionnelle et solutions constructives des cha�nes d'�nergie",
                   u"Am�lioration de l'efficacit� �nerg�tique dans les cha�nes d'�nergie",
                   u"Am�lioration de la gestion de l'�nergie",
                   u"Formes et caract�ristiques de l'information",
                   u"Organisation fonctionnelle et solutions constructives des cha�nes d'information",
                   u"Commande temporelle des syst�mes",
                   u"Informations li�e au comportement des mat�riaux et des structures",
                   u"Optimisation des param�tres par simulation globale"
                   ]
    
    
Competences = {"CO1.1" : u"Justifier les choix des mat�riaux, des structures d'un syst�me et les �nergies mises en oeuvre dans une approche de d�veloppement durable",
               "CO1.2" : u"Justifier le choix d'une solution selon des contraintes d'ergonomie et d'effets sur la sant� de l'homme et du vivant",
               "CO2.1" : u"Identifier les flux et la forme de l'�nergie, caract�riser ses transformations et/ou modulations et estimer l'efficacit� �nerg�tique globale d'un syst�me",
               "CO2.2" : u"Justifier les solutions constructives d'un syst�me au regard des impacts environnementaux et �conomiques engendr�s tout au long de son cycle de vie",
               "CO3.1" : u"D�coder le cahier des charges fonctionnel d'un syst�me",
               "CO3.2" : u"�valuer la comp�titivit� d'un syst�me d'un point de vue technique et �conomique",
               "CO4.1" : u"Identifier et caract�riser les fonctions et les constituants d'un syst�me ainsi que ses entr�es/sorties",
               "CO4.2" : u"Identifier et caract�riser l'agencement  mat�riel et/ou logiciel d'un syst�me", 
               "CO4.3" : u"Identifier et caract�riser le fonctionnement temporel d'un syst�me",
               "CO4.4" : u"Identifier et caract�riser des solutions techniques relatives aux mat�riaux, � la structure, � l'�nergie et aux informations (acquisition, traitement, transmission) d'un syst�me",
               "CO5.1" : u"Expliquer des �l�ments d'une mod�lisation propos�e relative au comportement de tout ou partie d'un syst�me",
               "CO5.2" : u"Identifier des variables internes et externes utiles � une mod�lisation, simuler et valider le comportement du mod�le",
               "CO5.3" : u"�valuer un �cart entre le comportement du r�el et le comportement du mod�le en fonction des param�tres propos�s",
               "CO6.1" : u"D�crire une id�e, un principe, une solution, un projet en utilisant des outils de repr�sentation adapt�s",
               "CO6.2" : u"D�crire le fonctionnement et/ou l'exploitation d'un syst�me en utilisant l'outil de description le plus pertinent",
               "CO6.3" : u"Pr�senter et argumenter des d�marches, des r�sultats, y compris dans une langue �trang�re",
               }


TypesActivite = {"ED" : u"Activit� d'�tude de dossier",
                 "AP" : u"Activit� pratique",
                 "P" : u"Activit� de projet",
                }

TypesSeance = {"C" : u"Cours",
               "SA" : u"Synth�se d'activit�",
               "SS" : u"Synth�se de s�quence",
               "E" : u"Evaluation",
               }
TypesSeance.update(TypesActivite)
TypesSeance.update({"R" : u"Rotation d'activit�s",
                    "S" : u"S�rie d'activit�s"})

listeTypeSeance = ["ED", "AP", "P", "C", "SA", "SS", "E", "R", "S"]

####################################################################################
#
#   Classe d�finissant les propri�t�s d'une s�quence
#
####################################################################################
Titres = [u"S�quence p�dagogique",
          u"Objectifs p�dagogiques",
          u"S�ances"]

class Sequence():
    def __init__(self, app, panelParent, intitule = u""):
        self.intitule = intitule
        self.panelPropriete = PanelPropriete_Sequence(panelParent, self)
        
        self.CI = CentreInteret(self, panelParent)
        
        self.obj = [Competence(self, panelParent)]
        
        self.seance = [Seance(self, panelParent)]
        
        self.panelParent = panelParent
        self.app = app
        
    
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
        """ Affiche le menu contextuel associ� � la s�quence
            ... ou bien celui de itemArbre concern� ...
        """
        if itemArbre == self.branche:
            self.app.AfficherMenuContextuel([[u"Enregistrer", self.app.commandeEnregistrer]])
            
        
        elif isinstance(self.arbre.GetItemPyData(itemArbre), Competence):
            self.arbre.GetItemPyData(itemArbre).AfficherMenuContextuel(itemArbre)
            
            
        elif self.arbre.GetItemText(itemArbre) == Titres[1]: # Objectifs p�dagogiques
            self.app.AfficherMenuContextuel([[u"Ajouter une comp�tence", self.AjouterObjectif]])
            
            
        elif self.arbre.GetItemText(itemArbre) == Titres[2]: # S�ances
            self.app.AfficherMenuContextuel([[u"Ajouter une s�ance", self.AjouterSeance]])
            
            
            
            
        
        
        
####################################################################################
#
#   Classe d�finissant les propri�t�s d'une s�quence
#
####################################################################################
class CentreInteret():
    def __init__(self, parent, panelParent, numCI = 0):
        
        self.SetNum(numCI)
        
        self.panelPropriete = PanelPropriete_CI(panelParent, self)
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML du centre d'int�r�t pour enregistrement
        """
        root = ET.Element(self.code)
        return root
    
    ######################################################################################  
    def SetNum(self, num):
        self.num = num
        self.code = "CI"+str(self.num)
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
        self.branche = arbre.AppendItem(branche, u"Centre d'int�r�t :", wnd = self.codeBranche, data = self)
        
    
        
        
####################################################################################
#
#   Classe d�finissant les propri�t�s d'une comp�tence
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
        """ Renvoie la branche XML de la comp�tence pour enregistrement
        """
        root = ET.Element(self.code)
        return root
    
    
    ######################################################################################  
    def ConstruireArbre(self, arbre, branche):
        self.arbre = arbre
        self.codeBranche = wx.StaticText(self.arbre, -1, u"")
        self.branche = arbre.AppendItem(branche, u"Comp�tence :", wnd = self.codeBranche, data = self)
        
        
    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerObjectif, item = itemArbre)]])
            
            
            
            

####################################################################################
#
#   Classe d�finissant les propri�t�s d'une comp�tence
#
####################################################################################
class Seance():
    def __init__(self, parent, panelParent, typeSeance = "C", typeParent = 0):
        """ S�ance :
                parent = le parent wx pour contenir "panelPropriete"
                typeSceance = type de s�ance parmi "TypeSeance"
                typeParent = type du parent de la s�ance :  0 = s�quence
                                                            1 = s�ance "Rotation"
                                                            2 = s�ance "S�rie"
        """
        self.ordre = 1
        self.duree = 1
        self.intitule  = u""
        self.typeParent = typeParent
        self.parent = parent
        
        self.SetType(typeSeance)
        
        self.panelPropriete = PanelPropriete_Seance(panelParent, self)
        
        self.rotation = []
        self.serie = []
        
        
        
    ######################################################################################  
    def SetType(self, typ):
        print typ
        if type(typ) == str:
            self.typeSeance = typ
        else:
            self.typeSeance = listeTypeSeance[typ]
            
        self.code = self.typeSeance + str(self.ordre)
    
        if hasattr(self, 'arbre'):
            self.SetCode()
        
        if self.typeSeance in ["R","S"] : # Rotation ou Serie
            self.AjouterSeance()
        
        
    ######################################################################################  
    def SetCode(self):
        self.codeBranche.SetLabel(self.code)
        
        
    ######################################################################################  
    def getBranche(self):
        """ Renvoie la branche XML de la s�ance pour enregistrement
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
        self.branche = arbre.AppendItem(branche, u"S�ance :", wnd = self.codeBranche, data = self)
        
        
    ######################################################################################  
    def AjouterSeance(self):
        """ Ajoute une s�ance � la s�ance
            !! Uniquement pour les s�ances de type "Rotation" ou "Serie" !!
        """
        seance = Seance(self.panelParent, typeParent = self.typeParent)
        if self.typeSeance == "R" : # Rotation
            self.rotation.append(seance)
            
        elif self.typeSeance == "S" : # Serie
            self.serie.append(seance)
            
        seance.ConstruireArbre(self.arbre, self.branche)



    ######################################################################################  
    def AfficherMenuContextuel(self, itemArbre):
        if itemArbre == self.branche:
            self.parent.app.AfficherMenuContextuel([[u"Supprimer", functools.partial(self.parent.SupprimerSeance, item = itemArbre)]])
            
#            item2 = menu.Append(wx.ID_ANY, u"Cr�er une rotation")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterRotation, item = item), item2)
#            
#            item3 = menu.Append(wx.ID_ANY, u"Cr�er une s�rie")
#            self.Bind(wx.EVT_MENU, functools.partial(self.AjouterSerie, item = item), item3)
            

        


####################################################################################
#
#   Classe d�finissant le panel conteneur des panels de propri�t�s
#
####################################################################################    
class PanelConteneur(wx.Panel):    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        self.bsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.bsizer)
        
        #
        # Le panel affich�
        #
        self.panel = None
    
    
    def AfficherPanel(self, panel):
        if self.panel != None:
            self.bsizer.Remove(self.panel)
            self.panel.Hide()
        self.bsizer.Add(panel, flag = wx.EXPAND)
        self.panel = panel
        self.panel.Show()
        self.bsizer.Layout()
        
    
####################################################################################
#
#   Classe d�finissant la fen�tre de l'application
#
####################################################################################
class FenetreSequence(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "")

        #
        # Taille et position de la fen�tre
        #
        self.SetMinSize((800,570)) # Taille mini d'�cran : 800x600
        self.SetSize((1024,738)) # Taille pour �cran 1024x768
        # On centre la fen�tre dans l'�cran ...
        self.CentreOnScreen(wx.BOTH)
        
        
        
        
        # Use a panel under the AUI panes in order to work around a
        # bug on PPC Macs
        pnl = wx.Panel(self)
        self.pnl = pnl
        
        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(pnl)
        
        # panel de propri�t�s (conteneur)
        panelProp = PanelConteneur(pnl)
        
        
        #
        # La s�quence
        #
        self.sequence = Sequence(self, panelProp)
        
        
        # Arbre de structure de la s�quence
        arbreSeq = ArbreSequence(pnl, self.sequence, panelProp)
        
        # Zone graphique de la fiche de s�quence
        ficheSeq = FicheSequence(pnl, self.sequence)
        
        self.fichierCourant = ""
        self.DossierSauvegarde = ""
        
        
        #############################################################################################
        # Mise en place de la zone graphique
        #############################################################################################
        self.mgr.AddPane(ficheSeq, 
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
#                         DockFixed().
#                         Gripper(False).
#                         Movable(False).
#                         Maximize().
                         Caption(u"Structure").
                         CaptionVisible(True).
#                         PaneBorder(False).
                         CloseButton(False)
#                         Show()
                         )
        
        #############################################################################################
        # Mise en place du panel de propri�t�s
        #############################################################################################
        self.mgr.AddPane(panelProp, 
                         aui.AuiPaneInfo().
#                         Name(u"Structure").
                         Bottom().Layer(1).
                         Floatable(False).
                         BestSize((200, 200)).
#                         DockFixed().
#                         Gripper(False).
#                         Movable(False).
#                         Maximize().
                         Caption(u"Propri�t�s").
                         CaptionVisible(True).
#                         PaneBorder(False).
                         CloseButton(False)
#                         Show()
                         )
        

        
        self.mgr.Update()
#        sizer = wx.BoxSizer(wx.HORIZONTAL)
#        self.SetSizerAndFit(sizer)
    
    ###############################################################################################
    def enregistrer(self, nomFichier):

        wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
        fichier = file(nomFichier, 'w')
        
        # Cr�ation de la racine
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
        mesFormats = "S�quence (.seq)|*.seq|" \
                     "Tous les fichiers|*.*'"
        dlg = wx.FileDialog(
            self, message=u"Enregistrer la s�quence sous ...", defaultDir=self.DossierSauvegarde , 
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
            s = u"'Oui' pour enregistrer la s�quence dans le fichier\n"
            s += self.fichierCourant
            s += ".\n\n"
            s += u"'Non' pour enregistrer la s�quence dans un autre fichier."
            
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
#        if modif : print "Fichier courant modifi� !"
        self.fichierCourant = nomFichier
        self.fichierCourantModifie = modif
        if self.fichierCourant == '':
            t = ''
        else:
            t = ' - ' + self.fichierCourant
        if modif : 
            t += " **"
        self.SetTitle("S�quence" + t )

    #############################################################################
    def MarquerFichierCourantModifie(self):
        self.definirNomFichierCourant(self.fichierCourant, True)
        
        
    #############################################################################
    def AfficherMenuContextuel(self, items):
        """ Affiche un menu contextuel contenant les items sp�cifi�s
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
#   Classe d�finissant la fen�tre de la fiche de s�quence
#
####################################################################################
       
class FicheSequence(wx.Panel):
    def __init__(self, parent, sequence):
        wx.Panel.__init__(self, parent, -1)

        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self, evt):
        #dc = wx.PaintDC(self)
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        
        self.Render(dc)


    def Render(self, dc):
        # Draw some stuff on the plain dc
        sz = self.GetSize()
        dc.SetPen(wx.Pen("navy", 1))
        x = y = 0
        while x < sz.width * 2 or y < sz.height * 2:
            x += 20
            y += 20
            dc.DrawLine(x, 0, 0, y)
        
        # now draw something with cairo
        ctx = wx.lib.wxcairo.ContextFromDC(dc)
        ctx.set_line_width(15)
        ctx.move_to(125, 25)
        ctx.line_to(225, 225)
        ctx.rel_line_to(-200, 0)
        ctx.close_path()
        ctx.set_source_rgba(0, 0, 0.5, 1)
        ctx.stroke()


#        # Draw some text
#        face = wx.lib.wxcairo.FontFaceFromFont(
#            wx.FFont(10, wx.SWISS, wx.FONTFLAG_BOLD))
#        ctx.set_font_face(face)
#        ctx.set_font_size(60)
#        ctx.move_to(360, 180)
#        ctx.set_source_rgb(0, 0, 0)
#        ctx.show_text("Hello")

        # Text as a path, with fill and stroke
        ctx.move_to(400, 220)
        ctx.text_path("World")
        ctx.set_source_rgb(0.39, 0.07, 0.78)
        ctx.fill_preserve()
        ctx.set_source_rgb(0,0,0)
        ctx.set_line_width(2)
        ctx.stroke()

        # Show iterating and modifying a (text) path
        ctx.new_path()
        ctx.move_to(0, 0)
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.set_font_size(30)
        text = "This path was warped..."
        ctx.text_path(text)
        tw, th = ctx.text_extents(text)[2:4]
        self.warpPath(ctx, tw, th, 360,300)
        ctx.fill()

        ctx.paint()
        
        
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
#   Classe d�finissant le panel de propri�t� par d�faut
#
####################################################################################
class PanelPropriete(wx.Panel):
    def __init__(self, parent, titre = u"", objet = None):
        wx.Panel.__init__(self, parent, -1, size = (-1, 200))
        
#        self.boxprop = wx.StaticBox(self, -1, u"")
        self.bsizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self.bsizer)
        self.SetAutoLayout(True)
 
 



####################################################################################
#
#   Classe d�finissant le panel de propri�t� de s�quence
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
        
####################################################################################
#
#   Classe d�finissant le panel de propri�t� du CI
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
                         #| wx.CB_SORT
                         )
        self.bsizer.Add(cb, 0, wx.EXPAND)
        self.bsizer.Layout()
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        
    def EvtComboBox(self, event):
        self.CI.SetNum(event.GetSelection())
        
        

####################################################################################
#
#   Classe d�finissant le panel de propri�t� de la comp�tence
#
####################################################################################
class PanelPropriete_Competence(PanelPropriete):
    def __init__(self, parent, competence):
        PanelPropriete.__init__(self, parent)
        self.competence = competence
        
        listComp = []
        l = Competences.items()
        for c in l:
            listComp.append(c[0] + " " + c[1])
        listComp.sort()    
        
        cb = wx.ComboBox(self, -1, u"Choisir un objectif",
                         choices = listComp,
                         style = wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )
        self.bsizer.Add(cb, 0, wx.EXPAND)
        self.bsizer.Layout()
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        
    def EvtComboBox(self, event):
        self.competence.SetNum(event.GetSelection())
        
        
####################################################################################
#
#   Classe d�finissant le panel de propri�t� de la s�ance
#
####################################################################################
class PanelPropriete_Seance(PanelPropriete):
    def __init__(self, parent, seance):
        PanelPropriete.__init__(self, parent, seance)
        self.seance = seance

        #  s�ance "normale" (parent = s�quence)
        listType = listeTypeSeance
        if seance.typeParent == 1: #  s�ance en rotation (parent = s�ance "Rotation")
            listType = listeTypeSeance[:-1]
        elif seance.typeParent == 1: #  s�ance en s�rie (parent = s�ance "Serie")
            listType = listeTypeSeance[:-2]
        
        listTypeS = []
        for t in listType:
            listTypeS.append(TypesSeance[t])
            
        cb = wx.ComboBox(self, -1, u"Choisir un type de s�ance",
                         choices = listTypeS,
                         style = wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )
        self.bsizer.Add(cb, 0, wx.EXPAND)
        self.bsizer.Layout()
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        
    def EvtComboBox(self, event):
        self.seance.SetType(event.GetSelection())
        

####################################################################################
#
#   Classe d�finissant l'arbre de structure de la s�quence
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
#        # Intitul� de la s�quence
#        #
#        self.AddPage(PanelPropriete_Sequence(self, self.sequence), u"S�quence")
#        
#        
#        #
#        # Centre d'int�r�t
#        #
#        self.AddSubPage(PanelPropriete_CI(self, self.sequence.CI), u"Centre d'int�r�t")
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
        # La s�quence 
        #
        self.sequence = sequence
        
        #
        # Le panel contenant les panel de propri�t�s des �l�ments de s�quence
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
        


        self.panelVide = PanelPropriete(self.panelProp)
        
        #
        # Construction de l'arbre
        #
        self.sequence.ConstruireArbre(self)
        
        #
        # Gestion des �venements
        #
        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(CT.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightDown)
        
        self.ExpandAll()
        
        return




        textctrl = wx.TextCtrl(self, -1, "I Am A Simple\nMultiline wx.TexCtrl", style=wx.TE_MULTILINE)
        self.gauge = wx.Gauge(self, -1, 50, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
        self.gauge.SetValue(0)
        combobox = wx.ComboBox(self, -1, choices=["That", "Was", "A", "Nice", "Holyday!"], style=wx.CB_READONLY|wx.CB_DROPDOWN)

        textctrl.Bind(wx.EVT_CHAR, self.OnTextCtrl)
        combobox.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
        lenArtIds = len(ArtIDs) - 2


        
        for x in range(15):
            if x == 1:
                child = self.AppendItem(self.root, "Item %d" % x + "\nHello World\nHappy wxPython-ing!")
                self.SetItemBold(child, True)
            else:
                child = self.AppendItem(self.root, "Item %d" % x)
            self.SetPyData(child, None)
            self.SetItemImage(child, 24, CT.TreeItemIcon_Normal)
            self.SetItemImage(child, 13, CT.TreeItemIcon_Expanded)

            if random.randint(0, 3) == 0:
                self.SetItemLeftImage(child, random.randint(0, lenArtIds))

            for y in range(5):
                if y == 0 and x == 1:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), ct_type=2, wnd=self.gauge)
                elif y == 1 and x == 2:
                    last = self.AppendItem(child, "Item %d-%s" % (x, chr(ord("a")+y)), ct_type=1, wnd=textctrl)
                    if random.randint(0, 3) == 1:
                        self.SetItem3State(last, True)
                        
                elif 2 < y < 4:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)))
                elif y == 4 and x == 1:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), wnd=combobox)
                else:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), ct_type=2)
                    
                self.SetPyData(last, None)
                self.SetItemImage(last, 24, CT.TreeItemIcon_Normal)
                self.SetItemImage(last, 13, CT.TreeItemIcon_Expanded)

                if random.randint(0, 3) == 0:
                    self.SetItemLeftImage(last, random.randint(0, lenArtIds))
                    
                for z in range(5):
                    if z > 2:
                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=1)
                        if random.randint(0, 3) == 1:
                            self.SetItem3State(item, True)
                    elif 0 < z <= 2:
                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=2)
                    elif z == 0:
                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z))
                        self.SetItemHyperText(item, True)
                    self.SetPyData(item, None)
                    self.SetItemImage(item, 28, CT.TreeItemIcon_Normal)
                    self.SetItemImage(item, numicons-1, CT.TreeItemIcon_Selected)

                    if random.randint(0, 3) == 0:
                        self.SetItemLeftImage(item, random.randint(0, lenArtIds))

        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.eventdict = {'EVT_TREE_BEGIN_DRAG': self.OnBeginDrag, 'EVT_TREE_BEGIN_LABEL_EDIT': self.OnBeginEdit,
                          'EVT_TREE_BEGIN_RDRAG': self.OnBeginRDrag, 'EVT_TREE_DELETE_ITEM': self.OnDeleteItem,
                          'EVT_TREE_END_DRAG': self.OnEndDrag, 'EVT_TREE_END_LABEL_EDIT': self.OnEndEdit,
                          'EVT_TREE_ITEM_ACTIVATED': self.OnActivate, 'EVT_TREE_ITEM_CHECKED': self.OnItemCheck,
                          'EVT_TREE_ITEM_CHECKING': self.OnItemChecking, 'EVT_TREE_ITEM_COLLAPSED': self.OnItemCollapsed,
                          'EVT_TREE_ITEM_COLLAPSING': self.OnItemCollapsing, 'EVT_TREE_ITEM_EXPANDED': self.OnItemExpanded,
                          'EVT_TREE_ITEM_EXPANDING': self.OnItemExpanding, 'EVT_TREE_ITEM_GETTOOLTIP': self.OnToolTip,
                          'EVT_TREE_ITEM_MENU': self.OnItemMenu, 'EVT_TREE_ITEM_RIGHT_CLICK': self.OnRightDown,
                          'EVT_TREE_KEY_DOWN': self.OnKey, 'EVT_TREE_SEL_CHANGED': self.OnSelChanged,
                          'EVT_TREE_SEL_CHANGING': self.OnSelChanging, "EVT_TREE_ITEM_HYPERLINK": self.OnHyperLink}

        mainframe = wx.GetTopLevelParent(self)
        
        if not hasattr(mainframe, "leftpanel"):
            self.Bind(CT.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
            self.Bind(CT.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
            self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
            self.Bind(CT.EVT_TREE_SEL_CHANGING, self.OnSelChanging)
            self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
            self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        else:
            for combos in mainframe.treeevents:
                self.BindEvents(combos)

        if hasattr(mainframe, "leftpanel"):
            self.ChangeStyle(mainframe.treestyles)

        if not(self.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
            self.SelectItem(self.root)
            self.Expand(self.root)

    
        
        
        
    def AjouterObjectif(self, event = None):
        self.sequence.AjouterObjectif()
        
        
    def SupprimerObjectif(self, event = None, item = None):
        self.sequence.SupprimerObjectif(item)

            
    def AjouterSeance(self, event = None):
        seance = self.sequence.AjouterSeance()
        self.lstSeances.append(self.AppendItem(self.seances, u"S�ance :", data = seance))
        
    def AjouterRotation(self, event = None, item = None):
        seance = self.sequence.AjouterRotation(self.GetItemPyData(item))
        self.SetItemText(item, u"Rotation")
        self.lstSeances.append(self.AppendItem(item, u"S�ance :", data = seance))
        
    def AjouterSerie(self, event = None, item = None):
        seance = self.sequence.AjouterRotation(self.GetItemPyData(item))
        self.SetItemText(item, u"Rotation")
        self.lstSeances.append(self.AppendItem(item, u"S�ance :", data = seance))
        
    def SupprimerSeance(self, event = None, item = None):
        if self.sequence.SupprimerSeance(self.GetItemPyData(item)):
            self.lstSeances.remove(item)
            self.Delete(item)
        
        
    def BindEvents(self, choice, recreate=False):

        value = choice.GetValue()
        text = choice.GetLabel()
        
        evt = "CT." + text
        binder = self.eventdict[text]

        if value == 1:
            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
                self.Bind(wx.EVT_RIGHT_DOWN, None)
                self.Bind(wx.EVT_RIGHT_UP, None)
            self.Bind(eval(evt), binder)
        else:
            self.Bind(eval(evt), None)
            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
                self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
                self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)


    def ChangeStyle(self, combos):

        style = 0
        for combo in combos:
            if combo.GetValue() == 1:
                style = style | eval("CT." + combo.GetLabel())

        if self.GetAGWWindowStyleFlag() != style:
            self.SetAGWWindowStyleFlag(style)
            

    def OnCompareItems(self, item1, item2):
        
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        
        self.log.write('compare: ' + t1 + ' <> ' + t2 + "\n")

        if t1 < t2:
            return -1
        if t1 == t2:
            return 0

        return 1

    
    def OnIdle(self, event):

        if self.gauge:
            try:
                if self.gauge.IsEnabled() and self.gauge.IsShown():
                    self.count = self.count + 1

                    if self.count >= 50:
                        self.count = 0

                    self.gauge.SetValue(self.count)

            except:
                self.gauge = None

        event.Skip()


    def OnRightDown(self, event):
        print "OnRightDown"
#        pt = event.GetPosition()
#        item, flags = self.HitTest(pt)
        item = event.GetItem()
#        print dir(item)

        self.sequence.AfficherMenuContextuel(item)
        
        



    def OnRightUp(self, event):

        item = self.item
        
        if not item:
            event.Skip()
            return

        if not self.IsItemEnabled(item):
            event.Skip()
            return

        # Item Text Appearance
        ishtml = self.IsItemHyperText(item)
        back = self.GetItemBackgroundColour(item)
        fore = self.GetItemTextColour(item)
        isbold = self.IsBold(item)
        font = self.GetItemFont(item)

        # Icons On Item
        normal = self.GetItemImage(item, CT.TreeItemIcon_Normal)
        selected = self.GetItemImage(item, CT.TreeItemIcon_Selected)
        expanded = self.GetItemImage(item, CT.TreeItemIcon_Expanded)
        selexp = self.GetItemImage(item, CT.TreeItemIcon_SelectedExpanded)

        # Enabling/Disabling Windows Associated To An Item
        haswin = self.GetItemWindow(item)

        # Enabling/Disabling Items
        enabled = self.IsItemEnabled(item)

        # Generic Item's Info
        children = self.GetChildrenCount(item)
        itemtype = self.GetItemType(item)
        text = self.GetItemText(item)
        pydata = self.GetPyData(item)
        
        self.current = item
        self.itemdict = {"ishtml": ishtml, "back": back, "fore": fore, "isbold": isbold,
                         "font": font, "normal": normal, "selected": selected, "expanded": expanded,
                         "selexp": selexp, "haswin": haswin, "children": children,
                         "itemtype": itemtype, "text": text, "pydata": pydata, "enabled": enabled}
        
        menu = wx.Menu()

        item1 = menu.Append(wx.ID_ANY, "Change Item Background Colour")
        item2 = menu.Append(wx.ID_ANY, "Modify Item Text Colour")
        menu.AppendSeparator()
        if isbold:
            strs = "Make Item Text Not Bold"
        else:
            strs = "Make Item Text Bold"
        item3 = menu.Append(wx.ID_ANY, strs)
        item4 = menu.Append(wx.ID_ANY, "Change Item Font")
        menu.AppendSeparator()
        if ishtml:
            strs = "Set Item As Non-Hyperlink"
        else:
            strs = "Set Item As Hyperlink"
        item5 = menu.Append(wx.ID_ANY, strs)
        menu.AppendSeparator()
        if haswin:
            enabled = self.GetItemWindowEnabled(item)
            if enabled:
                strs = "Disable Associated Widget"
            else:
                strs = "Enable Associated Widget"
        else:
            strs = "Enable Associated Widget"
        item6 = menu.Append(wx.ID_ANY, strs)

        if not haswin:
            item6.Enable(False)

        item7 = menu.Append(wx.ID_ANY, "Disable Item")
        
        menu.AppendSeparator()
        item8 = menu.Append(wx.ID_ANY, "Change Item Icons")
        menu.AppendSeparator()
        item9 = menu.Append(wx.ID_ANY, "Get Other Information For This Item")
        menu.AppendSeparator()

        item10 = menu.Append(wx.ID_ANY, "Delete Item")
        if item == self.GetRootItem():
            item10.Enable(False)
        item11 = menu.Append(wx.ID_ANY, "Prepend An Item")
        item12 = menu.Append(wx.ID_ANY, "Append An Item")

        self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
        self.Bind(wx.EVT_MENU, self.OnItemForeground, item2)
        self.Bind(wx.EVT_MENU, self.OnItemBold, item3)
        self.Bind(wx.EVT_MENU, self.OnItemFont, item4)
        self.Bind(wx.EVT_MENU, self.OnItemHyperText, item5)
        self.Bind(wx.EVT_MENU, self.OnEnableWindow, item6)
        self.Bind(wx.EVT_MENU, self.OnDisableItem, item7)
        self.Bind(wx.EVT_MENU, self.OnItemIcons, item8)
        self.Bind(wx.EVT_MENU, self.OnItemInfo, item9)
        self.Bind(wx.EVT_MENU, self.OnItemDelete, item10)
        self.Bind(wx.EVT_MENU, self.OnItemPrepend, item11)
        self.Bind(wx.EVT_MENU, self.OnItemAppend, item12)
        
        self.PopupMenu(menu)
        menu.Destroy()
        

    def OnItemBackground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["back"])
        dlg = wx.ColourDialog(self, colourdata)
        
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemBackgroundColour(self.current, col1)
        dlg.Destroy()


    def OnItemForeground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["fore"])
        dlg = wx.ColourDialog(self, colourdata)
        
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemTextColour(self.current, col1)
        dlg.Destroy()


    def OnItemBold(self, event):

        self.SetItemBold(self.current, not self.itemdict["isbold"])


    def OnItemFont(self, event):

        data = wx.FontData()
        font = self.itemdict["font"]
        
        if font is None:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            
        data.SetInitialFont(font)

        dlg = wx.FontDialog(self, data)
        
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            self.SetItemFont(self.current, font)

        dlg.Destroy()
        

    def OnItemHyperText(self, event):

        self.SetItemHyperText(self.current, not self.itemdict["ishtml"])


    def OnEnableWindow(self, event):

        enable = self.GetItemWindowEnabled(self.current)
        self.SetItemWindowEnabled(self.current, not enable)


    def OnDisableItem(self, event):

        self.EnableItem(self.current, False)
        

    def OnItemIcons(self, event):

        bitmaps = [self.itemdict["normal"], self.itemdict["selected"],
                   self.itemdict["expanded"], self.itemdict["selexp"]]

        wx.BeginBusyCursor()        
        dlg = TreeIcons(self, -1, bitmaps=bitmaps)
        wx.EndBusyCursor()
        dlg.ShowModal()


    def SetNewIcons(self, bitmaps):

        self.SetItemImage(self.current, bitmaps[0], CT.TreeItemIcon_Normal)
        self.SetItemImage(self.current, bitmaps[1], CT.TreeItemIcon_Selected)
        self.SetItemImage(self.current, bitmaps[2], CT.TreeItemIcon_Expanded)
        self.SetItemImage(self.current, bitmaps[3], CT.TreeItemIcon_SelectedExpanded)


    def OnItemInfo(self, event):

        itemtext = self.itemdict["text"]
        numchildren = str(self.itemdict["children"])
        itemtype = self.itemdict["itemtype"]
        pydata = repr(type(self.itemdict["pydata"]))

        if itemtype == 0:
            itemtype = "Normal"
        elif itemtype == 1:
            itemtype = "CheckBox"
        else:
            itemtype = "RadioButton"

        strs = "Information On Selected Item:\n\n" + "Text: " + itemtext + "\n" \
               "Number Of Children: " + numchildren + "\n" \
               "Item Type: " + itemtype + "\n" \
               "Item Data Type: " + pydata + "\n"

        dlg = wx.MessageDialog(self, strs, "CustomTreeCtrlDemo Info", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
                
        

    def OnItemDelete(self, event):

        strs = "Are You Sure You Want To Delete Item " + self.GetItemText(self.current) + "?"
        dlg = wx.MessageDialog(None, strs, 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)

        if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
            dlg.Destroy()
            return

        dlg.Destroy()

        self.DeleteChildren(self.current)
        self.Delete(self.current)
        self.current = None
        


    def OnItemPrepend(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.PrependItem(self.current, newname)
            self.EnsureVisible(newitem)

        dlg.Destroy()


    def OnItemAppend(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.AppendItem(self.current, newname)
            self.EnsureVisible(newitem)

        dlg.Destroy()
        

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
            

    def OnItemCollapsing(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemCollapsing: %s" % self.GetItemText(item) + "\n")
    
        event.Skip()

        
    def OnSelChanged(self, event):
        print "OnSelChanged"
        self.item = event.GetItem()
        data = self.GetItemPyData(self.item)
        if data == None:
            panelPropriete = self.panelVide
        else:
            panelPropriete = data.panelPropriete
        self.panelProp.AfficherPanel(panelPropriete)
        
                
        event.Skip()


    def OnSelChanging(self, event):

        item = event.GetItem()
        olditem = event.GetOldItem()
        
        if item:
            if not olditem:
                olditemtext = "None"
            else:
                olditemtext = self.GetItemText(olditem)
            self.log.write("OnSelChanging: From %s" % olditemtext + " To %s" % self.GetItemText(item) + "\n")
                
        event.Skip()


    def OnBeginDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Beginning Drag..." + "\n")

            event.Allow()


    def OnBeginRDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Beginning Right Drag..." + "\n")

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
        

    def OnItemCheck(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Has Been Checked!\n")
        event.Skip()


    def OnItemChecking(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Is Being Checked...\n")
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
# Fonction pour indenter les XML g�n�r�s par ElementTree
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
#   Classe d�finissant l'application
#    --> r�cup�ration des param�tres pass�s en ligne de commande
#
####################################################################################
class SeqApp(wx.App):
    def OnInit(self):
        if len(sys.argv)>1: #un param�tre a �t� pass�
            for param in sys.argv:
                parametre = param.upper()
                # on verifie que le fichier pass� en param�tre existe
                
            
        frame = FenetreSequence()
        frame.Show()
        return True
    
    
if __name__ == '__main__':
    app = SeqApp(False)
    app.MainLoop()
    
    
