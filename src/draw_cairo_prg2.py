#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               draw_cairo_prg                            ##
##                                                                         ##
##                        Tracé des fiches de progression                  ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2011-2020 Cédrick FAURY

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


# Pour débuggage
#import time
import sys

#import rsvg
# import cairo
import cairo
# import cairocffi as cairo
from draw_cairo2 import *

# import wx.lib.wxcairo
import images

import couleur

from math import log, pi
from couleur import CouleurFloat2CSS


import util_path

#from constantes import Effectifs, NomsEffectifs, listeDemarches, Demarches, getSavoir, getCompetence, \
#                        DemarchesCourt, estCompetenceRevue
import constantes
from widgets import getSingulier, getSingulierPluriel

# Les constantes partagées
from Referentiel import REFERENTIELS
import Referentiel


## Pour dessiner la cible ...
import os
import tempfile
import wx



# paramètres pour la fonction qui calcule la hauteur des tâches 
# en fonction de leur durée

# def calcH_doc(doc, periode):
#     """ Calcul de la hauteur de la Séquence ou du Projet
#     """
#     N = len(doc.getRangePeriode())
# #     print "calcH_doc", N
#     if N == 1:
#         return calcH(doc.GetDuree(), periode)
#     else:
#         return N*hPeriode + (N-1)*ecartY/2
        

# def calcH2(t, periode):
#     if t != 0:
#         return a[periode]*log(t+0.5)*log(2)+b[periode]
#     return 2*ecartTacheY



    
######################################################################################  
def getPts(lst_rect):
    lst = []
    for rect in lst_rect:
        lst.append(rect[:2])
    return lst


######################################################################################  
def regrouperDic(obj, dicIndicateurs):
#    print "regrouperDic", dicIndicateurs
#    print "   _dicCompetences_prj", obj.GetReferentiel()._dicCompetences_prj
    if obj.GetProjetRef()._niveau == 3:
        dic = {}
        typ = {}
        tousIndicateurs = obj.GetProjetRef()._dicCompetences
        for k0, v0 in list(tousIndicateurs.items()):
            for k1, v1 in list(v0[1].items()):
                dic[k1] = []
                typ[k1] = []
                lk2 = list(v1[1].keys())
                lk2.sort()
#                print "  ", lk2
                for k2 in lk2:
                    if k2 in list(dicIndicateurs.keys()):
                        dic[k1].extend(dicIndicateurs[k2])
#                        print "   **", v1[1][k2]
                        typ[k1].extend([p.poids for p in v1[1][k2][1]])
                    else:
                        l = len(v1[1][k2][1])
                        dic[k1].extend([False]*l)
                        typ[k1].extend(['']*l)
                
                if dic[k1] == [] or not (True in dic[k1]):
                    del dic[k1]
                    del typ[k1]
                    
#        print "  >>", dic
#        print "    ", typ
        return dic, typ
    else:
        typ = {}
        for k in list(dicIndicateurs.keys()):
            typ[k] = [p.poids for p in obj.GetProjetRef().getIndicateur(k)]
#        print "  >>>", dicIndicateurs, typ
        return dicIndicateurs, typ



######################################################################################  
def regrouperLst(ref, competences):
    return competences.get2Niveaux()


nom_module = os.path.splitext(os.path.basename(__file__))[0]

######################################################################################  
class Progression(Base_Fiche_Doc):
    def __init__(self, prg, mouchard = False, surRect = None):
        Base_Fiche_Doc.__init__(self)
        
        self.prg = prg
        self.mouchard = mouchard
        self.surRect = surRect
        
        self.nom_fichparam = "param_prg.cfg"
        
        
        #
        # Données pour le tracé
        #
        
        self.CoulAltern = []
        
        
        # Titre de la progression
        self.tailleNom = (0.29 * COEF, 0.04 * COEF)
        self.posNom = (self.margeX, self.margeY)
        self.IcoulNom = (0.85, 0.8, 0.8, 0.85)
        self.BcoulNom = (0.28, 0.2, 0.25, 1)
        self.fontNom = 0.016 * COEF
        
        # Equipe pédagogique
        self.tailleEqu = (0.17 * COEF, 0.07 * COEF)
        self.posEqu = (self.margeX, self.posNom[1] + self.tailleNom[1] + self.ecartY)
        self.IcoulEqu = (0.8, 0.8, 0.9, 0.85)
        self.BcoulEqu = (0.2, 0.25, 0.3, 1)
        self.fontEqu = 0.012 * COEF
        
        # CI/Thèmes
        self.IcoulCI = (0.9, 0.8, 0.8, 0.85)
        self.BcoulCI = (0.3, 0.2, 0.25, 1)
        self.fontCI = 0.013 * COEF
        
        ## Equipe pédagogique
        #tailleEqu = (0.17 * COEF, 0.18 * COEF - tailleSup[1]- tailleNom[1] - 3*ecartY/2)
        #posEqu = (margeX, posSup[1] + tailleSup[1] + ecartY)
        #IcoulEqu = (0.8, 0.8, 0.9, 0.85)
        #BcoulEqu = (0.2, 0.25, 0.3, 1)
        #fontEqu = 0.011 * COEF
        
        # Position dans l'année
        self.posPos = [None, self.margeY - self.ecartY/2]
        self.taillePos = [None, 0.03 * COEF]
        self.BcoulPos = []
        self.IcoulPos = []
        
        # Calendrier
        self.posPro = [self.posNom[0] + self.tailleNom[0] + self.ecartX/2, 
                       self.margeY + self.taillePos[1] + self.ecartY/2]
        self.taillePro = [self.LargeurTotale - self.margeX - self.posPro[0], 
                          0.19 * COEF - self.posPro[1] - self.ecartY/2]
        self.IcoulPro = (0.8, 0.9, 0.8, 0.85)
        self.BcoulPro = (0.25, 0.3, 0.2, 1)
        self.fontPro = 0.012 * COEF
        
        # Image
        self.posImg = [self.posEqu[0] + self.tailleEqu[0] + self.ecartX/4, 
                       self.posNom[1] + self.tailleNom[1] + self.ecartY]
        self.tailleImg = [self.posPro[0] - self.posImg[0] - self.ecartX/4, None]
        self.tailleImg[1] = self.posEqu[1] + self.tailleEqu[1] - self.posEqu[1]
        self.IcoulImg = (0.8, 0.8, 1, 0.85)
        self.BcoulImg = (0.1, 0.1, 0.25, 1)
        self.centreImg = (self.posImg[0] + self.tailleImg[0] / 2 + 0.0006 * COEF, 
                          self.posImg[1] + self.tailleImg[0] / 2 - 0.004 * COEF)
        
        # Zone d'organisation (grand cadre)
        self.posZOrganis = (self.margeX, 0.19 * COEF)
        self.bordureZOrganis = 0.01 * COEF
        self.tailleZOrganis = (self.LargeurTotale-2*self.margeX, 
                               1 * COEF-self.ecartY-self.posZOrganis[1]-self.bordureZOrganis)
        
        # Zone de déroulement du projet
        self.posZDeroul = [self.margeX, None]
        self.tailleZDeroul = [None, None]
        self.IcoulZDeroul = (1, 1, 0.7, 0.85)
        self.BcoulZDeroul = (0.4, 0.4, 0.03, 1)
        self.fontZDeroul = 0.016 * COEF
        self.wPhases = 0.02 * COEF      # Taille du label "phases"
        self.wDuree = 0.012 * COEF       # Taille de la fleche "duree"
        
        
        
        # Zones des tableaux Thématiques
        self.posZThV = [None, self.posZOrganis[1]]
        self.tailleZThV = [None, None]
        self.posZThH = [self.posZDeroul[0], self.posZThV[1]]
        self.tailleZThH = [None, None]
        self.wTh = 0.015 * COEF
        self.hTh = 0.020 * COEF
        self.xTh = []
        self.yTh = []
        
        
        
        # Zones des tableaux des CI/thèmes de séquence
        self.posZCIV = [None, None]
        self.tailleZCIV = [None, None]
        self.posZCIH = [self.posZDeroul[0], None]
        self.tailleZCIH = [None, None]
        self.wCI = 0.010 * COEF
        self.hCI = 0.020 * COEF
        self.xCI = []
        self.yCI = []
        
        
        # Zone du tableau des compétences
        self.posZComp = [None, None]
        self.tailleZComp = [None, None]
        self.wColCompBase = 0.018 * COEF
        self.ICoulComp = []
        
        self.xComp = {}
        self.cComp = {}
        
        
        # Zone des tâches
        self.posZTaches = [self.posZDeroul[0] + self.wPhases + self.ecartX*3/6, None]
        self.tailleZTaches = [None, None]
        self.hTacheMini = self.ecartY
        self.hRevue = self.ecartY/3
        self.hPeriode = None
        # yTaches = []
        # ecartTacheY = None  
        self.ecartTacheY = self.ecartY/3 # Ecartement entre les tâches de phase différente

        self.ecartyCITaches = 0.05 * COEF
        
        
    #####################################################################################
    def getDocument(self):
        return self.prg   
        
        
    ######################################################################################  
    def calcH(self, t, a, b):
        if t != 0:
            return a*log(t+2)+b
        return self.hTacheMini


    ######################################################################################  
    def definirCouleurs(self):
        n2 = len(self.prg.GetReferentiel()._listesCompetences_simple["S"])
        couleur.generate(self.ICoulComp, [0xFFFF6666, 0xFFFFFF66, 0xFF75FF66, 0xFF66FFF9, 0xFFFF66F4], n2)
        
        n1 = self.prg.GetNbrPeriodes()
        couleur.generate(self.BcoulPos, [0xFF82AAE0, 0xFFEF825D], n1)
        couleur.generate(self.IcoulPos, [0xFFC3D0E2, 0xFFF2C5B5], n1)
        
        
        n3 = len(self.prg.GetListeCI())
        del self.CoulAltern[:]
        for n in range(n3//2+1):
            self.CoulAltern += [((0.85, 0.85, 0.95, 0.3),    (0, 0, 0, 1)),
                           ((0.7,  0.7,  0.8,  0.2),    (0, 0, 0, 1))]

    ######################################################################################  
    def DefinirZones(self, ctx):
        """ Calcule les positions et dimensions des différentes zones de tracé
            en fonction du nombre d'éléments (élèves, tâches, compétences)
        """
#         global ecartTacheY, intituleTaches, fontIntTaches, xCI, yCI, hCI, hTh, \
#                wColComp, xTh, yTh, hPeriode
        
        #
        # Zone du tableau des compétences - X
        #
        ref = self.prg.classe.referentiel
        
        if self.prg.mode == "C":
            competences = ref.dicoCompetences["S"].get2Niveaux()
        elif self.prg.mode == "S": # Expérimental !!
            competences = ref.dicoSavoirs["S"].get2Niveaux()
        
        
        #print(ref.dicoCompetences["S"].get2Niveaux())
        N = 0
        for i, g1 in enumerate(competences):
            k1, l1 = g1
            N += len(l1)
            
            
            
            
    #     if ref.dicoCompetences["S"].getProfondeur() == 3:
    #         wColComp = wColCompBase
    #     else:
    #         wColComp = wColCompBase/2
    #     print("Ncomp :", N, wColCompBase, 0.2/N* COEF)
        if N == 0:
            self.wColComp = self.wColCompBase
        else:
            self.wColComp = min(self.wColCompBase, 0.2/N* COEF)
        
        
        self.tailleZComp[0] = 0
        for i, (k1, l1) in enumerate(competences):
            dx = self.wColComp/3
            if len(l1) == 0:
                l1 = [k1]
                dx = 0
                
            for k2 in l1:
                self.xComp[k2] = self.tailleZComp[0] #- 0.5 * wColComp  # position "gauche" de la colonne (relative)
                self.cComp[k2] = i
                self.tailleZComp[0] += self.wColComp
            self.tailleZComp[0] += dx
            
    #     tailleZComp[0] = 0
    #     for i, (k1, h1, l1) in enumerate(competences):
    #         dx = wColComp/3
    #         if len(l1) == 0:
    #             l1 = [[k1, h1]]
    #             dx = 0
    #             
    #         for k2, h2 in l1:
    #             xComp[k2] = tailleZComp[0] #- 0.5 * wColComp  # position "gauche" de la colonne (relative)
    #             cComp[k2] = i
    #             tailleZComp[0] += wColComp
    #         tailleZComp[0] += dx
            
            
        self.tailleZComp[0] -= dx
        self.posZComp[0] = self.posZOrganis[0] + self.tailleZOrganis[0] - self.tailleZComp[0]
        
        for s in self.xComp:
            self.xComp[s] += self.posZComp[0] # positions -> absolues
        
        
        #
        # Zone du tableau des Thématiques
        #
        lstTh = self.prg.GetListeTh()
        self.hTh = (-0.001*len(lstTh)+0.025) * COEF
    #     print "hTh", hTh
        self.tailleZThV[0] = self.wTh * len(lstTh)
        if len(lstTh) == 0:
            self.tailleZThH[1] = 0
            e = 0
        else:
            self.tailleZThH[1] = self.hTh * len(lstTh) + self.ecartY
            e = 1
        self.posZThV[0] = self.posZComp[0] - self.tailleZThV[0] - self.ecartX/2
        self.tailleZThH[0] = self.posZThV[0]-self.posZThH[0]- self.ecartX/2
        self.tailleZThV[1] = self.posZOrganis[1] + self.tailleZOrganis[1] - self.posZThV[1]
        xTh = []
        yTh = []
        for i in range(len(lstTh)):
            xTh.append(self.posZThV[0] + (i+0.5) * self.wTh)
            yTh.append(self.posZThH[1] + (i+0.5) * self.hTh)
            
            
        #
        # Zone du tableau des thèmes/CI
        #
        lstCI = self.prg.GetListeCI()
        self.hCI = (-0.001*len(lstCI)+0.025) * COEF
    #     print "hCI", hCI
        self.tailleZCIV[0] = self.wCI * len(lstCI)
        if len(lstCI) == 0:
            self.tailleZCIH[1] = 0
        else:
            self.tailleZCIH[1] = self.hCI * len(lstCI) + self.ecartY
        self.posZCIV[0] = self.posZComp[0] - self.tailleZCIV[0] - self.tailleZThV[0] - self.ecartX/2
        self.posZCIV[1] = self.posZThH[1] + self.tailleZThH[1] + self.ecartY/2 * e
        self.posZCIH[1] = self.posZCIV[1]
        self.tailleZCIH[0] = self.posZCIV[0] - self.posZCIH[0] - self.ecartX/2
        self.tailleZCIV[1] = self.posZOrganis[1] + self.tailleZOrganis[1] - self.posZCIV[1]
        self.xCI = []
        self.yCI = []
        for i in range(len(lstCI)):
            self.xCI.append(self.posZCIV[0] + (i+0.5) * self.wCI)
            self.yCI.append(self.posZCIV[1] + (i+0.5) * self.hCI)
    
    
        # Zone du tableau des compétences (entête - uniquement selon y)
        self.posZComp[1] = self.posZThV[1] + self.tailleZThH[1] + self.tailleZCIH[1]
        self.tailleZComp[1] = self.ecartyCITaches            
                     
                     
        # Zone de déroulement de la progression (cadre arrondi)
        self.posZDeroul[1] = self.posZThV[1] + self.tailleZThH[1] + self.tailleZCIH[1] + self.tailleZComp[1]
        self.tailleZDeroul[0] = self.posZCIV[0] - self.posZDeroul[0] - self.ecartX/2
        self.tailleZDeroul[1] = self.posZOrganis[1] + self.tailleZOrganis[1] - self.posZDeroul[1]
        
        
        # Zone des séquences et Projets
    #     yTaches = []
        self.posZTaches[1] = self.posZDeroul[1] + self.ecartY/2
        self.tailleZTaches[0] = self.posZDeroul[0] + self.tailleZDeroul[0] - self.posZTaches[0] - self.ecartX/2
        self.tailleZTaches[1] = self.tailleZDeroul[1] - self.ecartY/2 - 0.03 * COEF    # écart fixe pour la durée totale
    
        # Hauteur des périodes
        self.hPeriode = (self.tailleZTaches[1]-self.ecartTacheY)/ref.getNbrPeriodes()-self.ecartTacheY
    
    
    
        
    def Arranger(self):
        """ Calcul les zones de chaque Séquence/Projet
            de la Progression <prg>
        
            Renvoie :
             - une liste (ordre des prg.sequences_projets) de rectangles encadrant les prg.sequences_projets
             - une liste des rectangles encadrant les titres des positions
        
        """
        
    #     doc = lienDoc.GetDoc()
    #     h = calcH_doc(doc, doc.position[0])
        ref = self.prg.classe.referentiel
        
        # Nombre de creneaux utilisés dans la progression
        nc = self.prg.nbrCreneaux
        
        # Nombre de périodes utilisés dans la progression
        np = ref.getNbrPeriodes()
        
        # Largeur de chaque colonne (créneau)
        wc = self.tailleZTaches[0]/nc
        
        # Hauteur de chaque période
        hp = self.tailleZTaches[1]/np
    #     print "hp", hp
    #     print "hPeriode", hPeriode
        
        # Tableau Creneau/Position contenant des lienDoc
        tableau = [[[] for p in range(np)] for c in range(nc)]
        for lienDoc in self.prg.sequences_projets:
            doc = lienDoc.GetDoc()
            tableau[lienDoc.creneaux[0]][doc.position[0]].append(lienDoc)
            if doc.position[0] != doc.position[1]:
                tableau[lienDoc.creneaux[0]][doc.position[1]].append(lienDoc)
    #     print 
        # Tableau Creneau/Position contenant les coef a et b
        ab = [[self.getCoefCalcH(tableau[c][p]) for p in range(np)] for c in range(nc)]
    #     print "a,b", ab[0][0]
        # Tableau Creneau/Position des "piles" de y
        yc = [[self.posZTaches[1] + hp*p for p in range(np)] for c in range(nc)]
    
        rects = []
        for lienDoc in self.prg.sequences_projets:
            doc = lienDoc.GetDoc()
            c = lienDoc.creneaux[0]
            p = doc.position[0]
            x = self.posZTaches[0] + c * wc
            w = (lienDoc.creneaux[1]-c+1) * wc - self.ecartTacheY
            y = yc[c][p]
            
            r = doc.getRangePeriode()
    #         print "r =", r
    #         print tableau[c][p]
            if len(r) == 1:
                a, b = ab[c][p]
                h = self.calcH(doc.GetDuree(), a, b)
    #             print doc.GetDuree(), h
                yc[c][p] += h
            else:
                n = len(tableau[c][p])
                h = self.hPeriode/n
                yc[c][p] += h
                yc[c][r[-1]] += self.hPeriode/len(tableau[c][r[-1]])
                for pp in r[1:-1]:
                    h += hp
                h += hp-self.hPeriode
                h += self.hPeriode/len(tableau[c][r[-1]])
            
            rects.append((x, y, w, h))
        
        
        rec_pos = [(self.posZDeroul[0], self.posZTaches[1] + hp*p,
                    self.wPhases, hp) for p in range(np)]
        
        
        
        return rects, rec_pos
    
    
    def getCoefCalcH(self, case):
        """ Renvoie les coef a et b
            pour une case (creneau/position) donnée
        """
        b = 0.0
        a = 1.0
        
        h = 0.0         # hauteur totale de tous les éléments de hauteur variable
        nt = 0          # nombre d'éléments de hauteur variable ( = calculée par calcH() )
        hFixe = 0.0     # hauteur totale des éléments de hauteur fixe
        
        for lienDoc in case:
            doc = lienDoc.GetDoc()
            c = lienDoc.creneaux[0]
            p = doc.position[0]
            N = len(doc.getRangePeriode())
            
            if N == 1:
                h += self.calcH(doc.GetDuree(), a, b)
                nt += 1
            else:
                hFixe += self.hPeriode/len(case)
    
        b = self.hTacheMini # Hauteur mini
        if h != 0:
            a = (self.hPeriode - hFixe - b*nt) / h
        return a, b


        
    ######################################################################################  
    def draw(self, ctx, surRect = None, surObj = None):
        """ Dessine une fiche de progression <prg>
            dans un contexte cairo <ctx>
        """
        self.surRect = surRect
        self.ctx = ctx
        
    #        print "Draw progression"
    #    InitCurseur()
        
    #    tps = time.time()
        #
        # Options générales
        #
        self.initOptions(ctx)
            
        self.DefinirZones(ctx)
        
        self.definirCouleurs()
        
        # Essai ...
    #     prg.GetOrganisation()
        
    #     gabarit() # à virer (pour générer image gabarit
        
    #    DefinirCouleurs(prg.GetNbrPeriodes())
    #    print "DefinirCouleurs", IcoulPos
    
        #
        #    pour stocker des zones caractéristiques (à cliquer, ...)
        #
        
        # Zones sensibles, depuis pySéquence
        self.prg.zones_sens = []
        # Points caractéristiques des rectangles
        self.prg.pt_caract = []   # Contenu attendu : ((x,y), code)
        # Points caractéristiques des rectangles (sans code)
        self.prg.pts_caract = [] 
        
    #    prg.rect = []
    #    prg.rectComp = {}
        
        
        #
        # variables locales
        #
        ref = self.prg.classe.referentiel
        classe = self.prg.classe
        
        #
        # Type d'enseignement
        #
        tailleTypeEns = self.taillePro[0]/2
        t = self.prg.classe.GetLabel()
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_BOLD)
        ctx.set_source_rgb (0.6, 0.6, 0.9)
        
        h = self.taillePos[1] * 0.8
        show_text_rect(ctx, t, (self.posPro[0] , self.posPos[1], tailleTypeEns, h), 
                       va = 'c', ha = 'c', b = 0, orient = 'h', 
                       fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = False, couper = False,
                       coulBord = (0, 0, 0))
        
        t = self.prg.classe.GetLabelComplet()
        ctx.set_source_rgb (0.3, 0.3, 0.8)
        show_text_rect(ctx, t, (self.posPro[0] , self.posPos[1] + h, tailleTypeEns, self.taillePos[1] - h), 
                       va = 'c', ha = 'c', b = 0, orient = 'h', 
                       fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = False, couper = False)
    
    
    
    
    
        #
        # Positions dans l'année
        #
        self.posPos[0] = self.posNom[0] + self.tailleNom[0] + self.ecartX + tailleTypeEns
    
        self.taillePos[0] = self.taillePro[0]/2
        ctx.set_line_width (0.0015 * COEF)
        r = (self.posPos[0], self.posPos[1], self.taillePos[0], self.taillePos[1])
        rects = Periodes(self, r, self.prg.GetPositions(), ref.periodes).draw()
    #    prg.rect.append(posPos+taillePos)
        
        
        self.prg.zones_sens.append(Zone_sens([r], param = "POS"))
        for i, re in enumerate(rects):
            self.prg.zones_sens.append(Zone_sens([re], param = "POS"+str(i)))
        
    
    
    
    
    
        #
        # Etablissement
        #
        if classe.etablissement != "":
            t = classe.etablissement + " (" + classe.ville + ")"
            ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                              cairo.FONT_WEIGHT_NORMAL)
            show_text_rect(ctx, t, (self.posPos[0] , self.posPos[1]+self.taillePos[1], 
                                    self.taillePos[0], self.posPro[1]-self.posPos[1]-self.taillePos[1]), 
                           va = 'c', ha = 'g', b = 0.02, orient = 'h', 
                           fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                           coulBord = (0, 0, 0))
    
        
        #
        # Image
        #
        bmp = self.prg.image
        
        if bmp is not None:
            Image(self, (*self.posImg, *self.tailleImg), 
                      bmp, marge = 0.05).draw()
        
        # Ancienne méthode
#         if bmp != None:
#             ctx.save()
#             tfname = tempfile.mktemp()
#             try:
#                 bmp.SaveFile(tfname, wx.BITMAP_TYPE_PNG)
#                 image = cairo.ImageSurface.create_from_png(tfname)
#             finally:
#                 if os.path.exists(tfname):
#                     os.remove(tfname)  
#                     
#             w = image.get_width()*1.1
#             h = image.get_height()*1.1
#             
#             s = min(self.tailleImg[0]/w, self.tailleImg[1]/h)
#             dx = (self.tailleImg[0] - s*image.get_width())/2
#             dy = (self.tailleImg[1] - s*image.get_height())/2
#             ctx.translate(self.posImg[0] + dx, self.posImg[1] + dy)
#             ctx.scale(s, s)
#             ctx.set_source_surface(image, 0, 0)
#             ctx.paint ()
#             ctx.restore()
    
        
    
    
        #
        #  Equipe
        #
        rectEqu = self.posEqu + self.tailleEqu
        self.prg.pt_caract.append((Curve_rect_titre(self, rectEqu, "Equipe pédagogique", 
                                              self.BcoulEqu, self.IcoulEqu, self.fontEqu).draw(),
                            'Equ'))
        
        lstTexte = []
        g = None
        c = []
        for i, p in enumerate(self.prg.equipe):
            lstTexte.append(p.GetNomPrenom(disc = constantes.AFFICHER_DISC_FICHE))
            if p.referent:
                g = i
            c.append(constantes.COUL_DISCIPLINES[p.discipline])
        lstCodes = [" \u25CF"] * len(lstTexte)
    
        if len(lstTexte) > 0:
            r = Liste_code_texte(self, 
                                 (self.posEqu[0], self.posEqu[1], self.tailleEqu[0], self.tailleEqu[1]+0.0001 * COEF),
                                 lstCodes, lstTexte, 
                                 0.1*self.tailleEqu[1]+0.0001 * COEF, 0.1,
                                 gras = g, lstCoul = c, va = 'c').draw()
    
        
        self.prg.zones_sens.append(Zone_sens([rectEqu], param = "EQU"))
        for i, p in enumerate(self.prg.equipe):
            self.prg.zones_sens.append(Zone_sens([r[i]], obj = p))
    #        p.rect = [r[i]]
    #        prj.pts_caract.append(getPts(r))
    
    
    
    
    
        #
        #  Calendrier
        #
    #     prg.pt_caract.append((posPro, "Cal"))
        rectPro = self.posPro + self.taillePro
        pt = Curve_rect_titre(self, rectPro, "Calendrier",  
                              self.BcoulPro, self.IcoulPro, self.fontPro).draw()
        self.prg.pt_caract.append((pt, "Cal"))
        ctx.select_font_face(self.font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, constantes.ellipsizer("", constantes.LONG_MAX_PROBLEMATIQUE), 
                       rectPro, ha = 'g', b = 0.05,
                       fontsizeMinMax = (-1, 0.016 * COEF))
        Calendrier(self, rectPro, self.prg.calendrier).draw()
    #    prg.rect.append(rectPro)
        self.prg.zones_sens.append(Zone_sens([rectPro], param = "CAL"))
    
    
    
    
    
    
        #
        #  Années
        #
    #    prg.pts_caract = []
        rectNom = self.posNom+self.tailleNom
        pt = Curve_rect_titre(self, rectNom, "Progression pédagogique",  
                              self.BcoulNom, self.IcoulNom, self.fontNom).draw()
        self.prg.pt_caract.append((pt, 'Ann'))
        ctx.select_font_face(self.font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, "Années scolaires " + self.prg.GetAnnees(), 
                       rectNom, ha = 'c', b = 0.02,
                       fontsizeMinMax = (-1, 0.017 * COEF),
                       wrap = False, couper = False)
        
        self.prg.zones_sens.append(Zone_sens([rectNom], param = "ANN"))
    #    prg.pt_caract.append(posNom)
    
    
    
    
        
        if self.prg.mode == "C":
            #
            #  Tableau des Compétences
            #    
            
            # Titre
            htitre = 0.017 * COEF
            show_text_rect(ctx, ref.dicoCompetences["S"]._nom.Plur_(),
                           (self.posZComp[0], self.posZOrganis[1], # + self.ecartY/2,
                            self.tailleZComp[0], htitre), 
                           va = 'c', ha = 'c', b = 0, orient = 'h', 
                           fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = False, couper = False,
                           coulBord = (0, 0, 0))
            
            
        #     competences = ref._listesCompetences_simple["S"]
            competences = ref.dicoCompetences["S"].get2Niveaux()
        #     competences = regrouperLst(prj.GetProjetRef(), prj.GetCompetencesUtil())
        #     clefs = constantes.trier(list(ref.dicoCompetences["S"].keys()))
        #     print "competences", competences
            e = 0.0006 * COEF
            ctx.set_line_width(e)
            _x = _x0 = self.posZComp[0]
            _y0, _y1 = self.posZComp[1], self.posZDeroul[1] + self.tailleZDeroul[1]
        #     h = 1.5*wColComp
            
            for i, g1 in enumerate(competences):
                k1, l1 = g1
                dx = self.wColComp/3
                if len(l1) == 0:
                    l1 = [k1]
                    dx = 0
                
                coul = list(self.ICoulComp[i][:3])+[0.2]
                n = 0
                for k2 in l1:
                    #
                    # Lignes verticales et rectangles clairs
                    #
                    rect = (_x, _y0, self.wColComp, _y1 -_y0)
                    ligne(ctx, _x, _y0, _x, _y1, (0, 0, 0))
                    ctx.set_source_rgba(*coul)
                    ctx.rectangle(*rect[:4])
                    ctx.fill()
                    self.prg.pt_caract.append((rect[:2], "C_"+k2))
                    n += 1
                    _x += self.wColComp
                    
                
                # Dernière ligne
                ligne(ctx, _x, _y0, _x, _y1, (0, 0, 0))
        
                ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_NORMAL)
                ctx.set_source_rgb(0, 0, 0)
                ctx.set_line_width(e)
                
        #        # Titre famille de compétences
        #        ht = tailleZComp[1] / 4
        #        show_text_rect(ctx, k1, (_x0, posZComp[1], _x-_x0, ht), va = 'c', ha = 'c', b = 0.3, orient = 'h')
        
                rects = TableauV(self, l1, _x0, self.posZComp[1], 
                                 _x-_x0, self.tailleZComp[1], 
                                 0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', 
                                 coul = self.ICoulComp[i], b = 0.03).draw()
                
                for i, r in enumerate(rects):
                    self.prg.zones_sens.append(Zone_sens([r], param = "CMP"+l1[i]))
                    
                _x += dx
                _x0 = _x
            
            #
            # Bilan des compétences abordées
            #
            dicComp, nbrComp = self.prg.GetCompetencesAbordees()
            self.DrawBoutonCompetence(None, dicComp, self.posZOrganis[1] + htitre + self.ecartY/2, 
                                 h = self.posZComp[1] - self.posZOrganis[1] - self.ecartY - htitre, 
                                 nbr = nbrComp)
            
            
            
            
            
        
        elif self.prg.mode == "S": # Expérimental !!
            #
            #  Tableau des Savoirs
            #    
            
            # Titre
            htitre = 0.017 * COEF
            show_text_rect(ctx, ref.dicoSavoirs["S"]._nom.Plur_(),
                           (self.posZComp[0], self.posZOrganis[1],
                            self.tailleZComp[0], htitre), 
                           va = 'c', ha = 'c', b = 0, orient = 'h', 
                           fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = False, couper = False,
                           coulBord = (0, 0, 0))
            
            savoirs = ref.dicoSavoirs["S"].get2Niveaux()
        #     competences = regrouperLst(prj.GetProjetRef(), prj.GetCompetencesUtil())
        #     clefs = constantes.trier(list(ref.dicoCompetences["S"].keys()))
        #     print "competences", competences
            e = 0.0006 * COEF
            ctx.set_line_width(e)
            _x = _x0 = self.posZComp[0]
            _y0, _y1 = self.posZComp[1], self.posZDeroul[1] + self.tailleZDeroul[1]
        #     h = 1.5*wColComp
            
            for i, g1 in enumerate(savoirs):
                k1, l1 = g1
                dx = self.wColComp/3
                if len(l1) == 0:
                    l1 = [k1]
                    dx = 0
                
                coul = list(self.ICoulComp[i][:3])+[0.2]
                n = 0
                for k2 in l1:
                    #
                    # Lignes verticales et rectangles clairs
                    #
                    rect = (_x, _y0, self.wColComp, _y1 -_y0)
                    ligne(ctx, _x, _y0, _x, _y1, (0, 0, 0))
                    ctx.set_source_rgba(*coul)
                    ctx.rectangle(*rect[:4])
                    ctx.fill()
                    self.prg.pt_caract.append((rect[:2], "C_"+k2))
                    n += 1
                    _x += self.wColComp
                    
                
                # Dernière ligne
                ligne(ctx, _x, _y0, _x, _y1, (0, 0, 0))
        
                ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_NORMAL)
                ctx.set_source_rgb(0, 0, 0)
                ctx.set_line_width(e)
                
        #        # Titre famille de compétences
        #        ht = tailleZComp[1] / 4
        #        show_text_rect(ctx, k1, (_x0, posZComp[1], _x-_x0, ht), va = 'c', ha = 'c', b = 0.3, orient = 'h')
        
                rects = TableauV(ctx, l1, _x0, self.posZComp[1], 
                                 _x-_x0, self.tailleZComp[1], 
                                 0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', 
                                 coul = self.ICoulComp[i], b = 0.03).draw()
                
                for i, r in enumerate(rects):
                    self.prg.zones_sens.append(Zone_sens([r], param = "CMP"+l1[i]))
                    
                _x += dx
                _x0 = _x
            
            
            
            #
            # Bilan des Savoirs abordés
            #
            dicSav, nbrSav = self.prg.GetSavoirsAbordes()
            self.DrawBoutonSavoir(ctx, self.prg, None, dicSav, self.posZOrganis[1] + htitre + self.ecartY/2, 
                                 h = self.posZComp[1] - self.posZOrganis[1] - self.ecartY - htitre, 
                                 nbr = nbrSav)
                
          
            
            
    
        
        #
        #  Tableau des Thématiques
        #   
        lstTh = self.prg.GetListeTh()
    
        
        if len(lstTh) > 0:
            rectTh = (self.posZThH[0], self.posZThV[1], 
                      self.tailleZThH[0], self.tailleZThH[1])
    #         print("nomTh", ref._nomTh.Plur_())
            Curve_rect_titre(ctx, rectTh, ref._nomTh.Plur_(),
                             self.BcoulCI, self.IcoulCI, self.fontCI).draw()
            
            ctx.select_font_face(self.font_family, cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(0.0005 * COEF)
            l=[]
            for i,e in enumerate(lstTh) : 
        #        e.pts_caract = []
                l.append(e)
        
            #
            # Croisements divers
            #
            x, y = self.posZThV[0] + self.ecartX /2, self.posZThV[1] + self.ecartY /2
            w, h = self.tailleZThH[0] - self.ecartX, self.tailleZThH[1] - self.ecartY
            
        
            
            if len(l) > 0:
                rec = TableauH(self, l, x, y, 
                             w, 0, h, 
                             va = 'c', ha = 'd', orient = 'h', coul = self.CoulAltern,
                             tailleFixe = True).draw()
                
                
                
                #
                # Lignes horizontales
                #
                for i, e in enumerate(lstTh):
                    self.prg.zones_sens.append(Zone_sens([rec[i]], param = "Th"+str(i)))
                    
                    Ic = self.CoulAltern[i][0]
                    
                    ctx.set_line_width(0.003 * COEF)
                    ligne(ctx, self.posZThV[0]+self.tailleZThH[0]- self.ecartX /2, self.yTh[i]+ self.ecartY /2,
                          self.posZComp[0]+self.tailleZComp[0], self.yTh[i]+ self.ecartY /2, Ic)
                    
                    self.prg.pt_caract.append((rec[i][:2], "Th"+str(i)))
                    
                    
                #
                # Lignes verticales
                #
                for i, e in enumerate(lstTh):
                    Ic = self.CoulAltern[i][0]
                    ctx.set_line_width(0.003 * COEF)
                    
                    ligne(ctx, self.xTh[i], self.yTh[i]+ self.ecartY /2,
                          self.xTh[i], self.posZTaches[1] + self.tailleZTaches[1],
                          Ic)
    
        #            DrawCroisementsElevesCompetences(ctx, prg, e, yCI[i])
                
                #
                # Ombres des lignes verticales
                #
                e = 0.003 * COEF
                ctx.set_line_width(0.003 * COEF)
                for i in range(len(lstTh)) :
                    y = self.posZTaches[1] + self.tailleZTaches[1] + (i % 2)*(self.ecartY/2) + self.ecartY/2
                    ctx.set_source_rgb(1,1,1)
                    ctx.move_to(self.xTh[i]+e, self.yTh[i]+e+ self.ecartY /2)
                    ctx.line_to(self.xTh[i]+e, y)
                    ctx.move_to(self.xTh[i]-e, self.yTh[i]+e+ self.ecartY /2)
                    ctx.line_to(self.xTh[i]-e, y)
                ctx.stroke()
    
    
    
    
        #
        #  Tableau des CI/Thèmes de séquence
        #   
        lstCI = self.prg.GetListeCI()
        
        if len(lstCI) > 0:
            rectCI = (self.posZCIH[0], self.posZCIH[1], 
                      self.tailleZCIH[0], self.tailleZCIH[1])
            pt = Curve_rect_titre(self, rectCI, ref._nomCI.Plur_(),
                             self.BcoulCI, self.IcoulCI, self.fontCI).draw()
            self.prg.pt_caract.append((pt, "CI"))
            
            ctx.select_font_face(self.font_family, cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(0.0005 * COEF)
            l=[]
            for i,e in enumerate(lstCI) : 
        #        e.pts_caract = []
                l.append(e)
        
            #
            # Croisements divers
            #
            x, y = self.posZCIH[0] + self.ecartX /2, self.posZCIH[1] + self.ecartY /2
            w, h = self.tailleZCIH[0] - self.ecartX, self.tailleZCIH[1] - self.ecartY
            
            if w < 0: w = 0
        
            
            if len(l) > 0:
                rec = TableauH(self, l, x, y, 
                             w, 0, h, 
                             va = 'c', ha = 'd', orient = 'h', 
                             coul = self.CoulAltern,
                             tailleFixe = True).draw()
                
                
                
                #
                # Lignes horizontales
                #
                for i, e in enumerate(lstCI):
                    self.prg.zones_sens.append(Zone_sens([rec[i]], param = "CI"+str(i)))
                    
                    ctx.set_line_width(0.003 * COEF)
                    ligne(ctx, self.posZCIH[0]+self.tailleZCIH[0] - self.ecartX/2, self.yCI[i] + self.ecartY/2,
                               self.xCI[i], self.yCI[i] + self.ecartY/2,
                          self.CoulAltern[i][0][:-1])
                    
                    self.prg.pt_caract.append((rec[i][:2], "CI"+str(i)))
                    
                #
                # Lignes verticales
                #
                for i, e in enumerate(lstCI):
                    ctx.set_line_width(0.003 * COEF)
                    ligne(ctx, self.xCI[i], self.yCI[i] + self.ecartY /2, 
                               self.xCI[i], self.posZTaches[1] + self.tailleZTaches[1], 
                          self.CoulAltern[i][0][:-1])
                     
        #            DrawCroisementsElevesCompetences(ctx, prg, e, yCI[i])
                
                #
                # Ombres des lignes verticales
                #
                e = 0.003 * COEF
                ctx.set_line_width(0.003 * COEF)
                for i in range(len(lstCI)) :
                    y = self.posZTaches[1] + self.tailleZTaches[1]
                    ctx.set_source_rgb(1,1,1)
                    ctx.move_to(self.xCI[i]+e, self.yCI[i]+e+ self.ecartY /2)
                    ctx.line_to(self.xCI[i]+e, y)
                    ctx.move_to(self.xCI[i]-e, self.yCI[i]+e+ self.ecartY /2)
                    ctx.line_to(self.xCI[i]-e, y)
                ctx.stroke()
    
        
        
        self.DrawSequencesEtProjets()
    #     DrawSequencesEtProjets2(ctx, prg)
     
     
    
    
        
        #
        # Durée Totale
        #
        ctx.set_source_rgb(0.5,0.8,0.8)
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
        
        show_text_rect(ctx, getHoraireTxt(self.prg.GetDuree()), 
                       (self.posZDeroul[0], self.posZTaches[1]+self.tailleZTaches[1],
                        self.posZTaches[0]-self.posZDeroul[0], 
                        self.posZDeroul[1]+self.tailleZDeroul[1] - self.posZTaches[1]-self.tailleZTaches[1]), 
                       ha = 'c', 
                       orient = 'h', b = 0.03, couper = False)
    
    
        #
        # Informations
        #
        self.info(ctx)
                
        self.surBrillance(ctx, surObj)
        
        self.prg.zones_sens.reverse()
        
        

#     ######################################################################################  
#     def DrawLigneEff(self, x, y):
#         dashes = [ 0.010 * COEF,   # ink
#                    0.002 * COEF,   # skip
#                    0.005 * COEF,   # ink
#                    0.002 * COEF,   # skip
#                    ]
#         self.ctx.set_line_width (0.001 * COEF)
#         self.ctx.set_dash(dashes, 0)
#         ligne(self.ctx, x, self.posZCIV[1] + self.tailleZCIV[1],
#               x, y, (0.6, 0.8, 0.6))
#         self.ctx.set_dash([], 0)
         
            
            
    ######################################################################################  
    def DrawSequencesEtProjets(self):
        ###################################################################################
        #  Séquences et Projets
        #
        
    
        # Nombre de creneaux utilisés dans la progression
        nc = self.prg.nbrCreneaux
   
            
        rect, l_per, y_lig, _ = self.prg.GetRectangles(verif = False)
    
        
        # Mise des rectangles à l'échelle de la fiche
        rects = [[0,0,0,0] for i in self.prg.sequences_projets]  # Rectangles à l'échelle du dessin
        for sp, r in enumerate(rect):
            # suivant X : position, largeur
            rects[sp][0] = self.posZTaches[0] + self.tailleZTaches[0]/nc * r[0]
            rects[sp][2] = r[2] * self.tailleZTaches[0]/nc
            
            # suivant Y : position, hauteur
            rects[sp][1] = y_lig[r[1]]
            rects[sp][3] = y_lig[r[1]+r[3]] - y_lig[r[1]]
        
    #     print "y_lig", y_lig
        
    #     # On compte les écarts à insérer
    #     n_ecarts = 0
    #     for l, y_l in enumerate(y_lig[:-1]):
    #         if y_l == y_lig[l+1]:
    #             n_ecarts += 1
        
    #     print "n_ecarts", n_ecarts
        
        # On rabote les cotés (suivant X)
        for r in rects:
            r[0] += self.ecartX / 2
            r[2] -= self.ecartX / 2
            
           
        # On ajuste en hauteur 
    #     print "bas:", posZTaches[1] + tailleZTaches[1]
    #     ly = [_y+_h for _x, _y, _w, _h in rects]            # Liste des positions basses de chaque rectangle
    #     if len(ly) >0:
    #         Y = max(ly)
    #         print Y,
        Y = y_lig[-1]   # Position de la dernière ligne = bas de la zone
        if Y > 0:
            a = (self.tailleZTaches[1] ) / Y  # Coefficient multiplicateur- n_ecarts*ecartY
            
            # On met à l'échelle les positions des lignes
            for l in range(len(y_lig)):
                y_lig[l] = self.posZTaches[1] + y_lig[l]*a
                
    #         print "y_lig", y_lig
            
    #         # On rajoute les écarts
    #         for l in range(len(y_lig[:-1])):
    #             if y_lig[l] == y_lig[l+1]:
    #                 for i in range(l+1, len(y_lig)):       # On décale les lignes suivantes
    #                     y_lig[i] += ecartY
       
            
    #         print "y_lig", y_lig
            
            # On met à jour les rectangles (selon Y)
            for sp, r in enumerate(rects):
                r[1] = y_lig[rect[sp][1]]
                r[3] = r[3]*a
        
        
        
        
        # Positions des périodes en Y
        y_per = [y_lig[l] for l in l_per]+[y_lig[-1]]
    #     print rects
    #     print "y_per", y_per
        
        
        
        i = 1
        l = []
        while i < len(y_per)-1:
            
            if y_per[i] is None:
                l.append(i)
            else:
                for n, j in enumerate(l):
                    y_per[j] = (n+1)*(y_per[l[-1]+1] - y_per[l[0]-1]) / (len(l)+1) + y_per[l[0]-1]
                l = []
            i +=1
            
            
    #     print "y_per", y_per        
    #     print        
        
        Curve_rect_titre(self, (self.posZDeroul[0], self.posZDeroul[1], 
                          self.tailleZDeroul[0], self.tailleZDeroul[1]),
                         "Séquences et Projets",
                         self.BcoulZDeroul, self.IcoulZDeroul, self.fontZDeroul).draw()
        
        
    
    
        #
        # Lignes séparatrices des périodes
        #
        for rec in y_per[1:]:
            
            self.ctx.set_source_rgba(*self.BcoulZDeroul)
            self.ctx.move_to(self.posZDeroul[0], rec)
            self.ctx.line_to(self.posZDeroul[0] + self.tailleZDeroul[0], rec)
            self.ctx.stroke()
    
        #
        # Les cadres
        #
        yCadres = []
        for i, lienDoc in enumerate(self.prg.sequences_projets):
            y = rects[i][1] + self.ecartX/5
    #         if len(yCadres) > 0 and y-yCadres[-1] < ecartX/6:
    #             y = yCadres[-1] + ecartX/6
            yCadres.append(y)
#             self.DrawSequenceProjet(lienDoc, rects[i], y)
        
        
        #
        # Les lignes de croisement
        #    avec décalage au cas où elles se superposent
        #
        yLignes = list(zip(yCadres, list(range(len(yCadres)))))
        yLignes.sort(key=lambda x:x[0])
        
        dy = self.ecartX/2      # écart
        i = 1
        while i < len(yLignes):
            if yLignes[i][0] - yLignes[i-1][0] < dy:
                yLignes[i] = (yLignes[i-1][0] + dy, yLignes[i][1])
            i += 1

        yLignes.sort(key=lambda x:x[1])
    
        try:  # ???
            yLignes, i = list(zip(*yLignes))
        except:
            pass
        
        #
        # On dessinne les cadres
        #
        for i, lienDoc in enumerate(self.prg.sequences_projets):
            self.DrawSequenceProjet(lienDoc, rects[i], yCadres[i], yLignes[i])
        
        #
        # Les lignes horizontales en face des sequences
        # et les croisements Séquences/Competences
        #
        for i, y in enumerate(yLignes): 
            x = rects[i][0] + rects[i][2]
            doc = self.prg.sequences_projets[i].GetDoc()
            if doc is None:
                continue
            self.DrawLigne(x, y)
            if self.prg.mode == "C":
                self.DrawCroisementsCompetencesTaches(doc, y)
            elif self.prg.mode == "S":
                self.DrawCroisementsSavoirsTaches(doc, y)
            if hasattr(doc, 'CI'):
                self.DrawCroisementsCISeq(doc, y)
        
        # Nom des périodes
    #    print "yh_phase", yh_phase
         
        fontsize = self.wPhases
        for i, y_p in enumerate(y_per[:-1]):
            if y_p is None or y_per[i+1]-y_p <= 0:
                continue
            h = y_per[i+1]-y_p
            r = (self.posZDeroul[0], y_p,
                 self.wPhases, h)
            c = self.BcoulPos[i]
            self.ctx.set_source_rgb(c[0],c[1],c[2])
            self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_ITALIC,
                                  cairo.FONT_WEIGHT_NORMAL)
            if self.ctx.font_extents()[2] < h:
                show_text_rect(self.ctx, str(i+1), 
                               r, fontsizeMinMax = (fontsize, fontsize),
                               ha = 'c', orient = "h", b = 0.02, le = 0.7,
                               wrap = False, couper = False
                               ) 
    
    



#     ######################################################################################  
#     def DrawSequencesEtProjets2(self):
#         ###################################################################################
#         #  Séquences et Projets
#         #
#         
#         Curve_rect_titre(self,
#                          (self.posZDeroul[0], self.posZDeroul[1], 
#                           self.tailleZDeroul[0], self.tailleZDeroul[1]),
#                          "Séquences et Projets", 
#                          self.BcoulZDeroul, self.IcoulZDeroul, self.fontZDeroul).draw()
#         
#         y = self.posZTaches[1] - self.ecartTacheY
#     
#     
#         
#         rects, rec_pos = self.Arranger(self.prg)
#     
#         #
#         # Ligne séparatrices
#         #
#         for rec in rec_pos[1:]:
#             self.ctx.set_source_rgba(*self.BcoulZDeroul)
#             self.ctx.move_to(self.posZDeroul[0], rec[1] - self.ecartTacheY/2)
#             self.ctx.line_to(self.posZDeroul[0] + self.tailleZDeroul[0], rec[1]-self.ecartTacheY/2)
#             self.ctx.stroke()
#     
#         #
#         # Les cadres
#         #
#         yTaches = []
#         for i, lienDoc in enumerate(self.prg.sequences_projets):
#             y = rects[i][1] + self.ecartX/5
#     #         if len(yTaches) > 0 and y-yTaches[-1] < ecartX/6:
#     #             y = yTaches[-1] + ecartX/6
#             yTaches.append(y)
#             yb = self.DrawSequenceProjet(lienDoc, rects[i], y)
#         
#         # Ajustement des yTaches
#         yt = list(zip(yTaches, list(range(len(yTaches)))))
#     
#         yt.sort(key=lambda x:x[0])
#     
#         
#         i = 1
#         while i < len(yt):
#             if yt[i][0] - yt[i-1][0] < (self.ecartX/5):
#                 yt[i] = (yt[i-1][0] + self.ecartX/5, yt[i][1])
#             i += 1
#         
#         
#     #     for j, (y, i) in enumerate(yt[1:]):
#     #         y_1 = yt[j-1][0]
#     #         if y - y_1 < (ecartX/5):
#     #             print " !! ", y , y_1
#     #             yt[j] = (y_1 + ecartX/5, yt[j][1])
#         yt.sort(key=lambda x:x[1])
#     
#         try:
#             yTaches, i = list(zip(*yt))
#         except:
#             pass
#         
#         #
#         # Les lignes horizontales en face des sequences
#         # et les croisements Séquences/Competences
#         #
#         for i, y in enumerate(yTaches): 
#             x = rects[i][0] + rects[i][2]
#             doc = self.prg.sequences_projets[i].GetDoc()
#             self.DrawLigne(x, y)
#             self.DrawCroisementsCompetencesTaches(doc, y)
#             if hasattr(doc, 'CI'):
#                 self.DrawCroisementsCISeq(doc, y)
#         
#         # Nom des périodes
#     #    print "yh_phase", yh_phase
#         
#         fontsize = self.wPhases
#          
#         for i, rec in enumerate(rec_pos):
#               
#             c = self.BcoulPos[i]
#             self.ctx.set_source_rgb(c[0],c[1],c[2])
#             self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_ITALIC,
#                                   cairo.FONT_WEIGHT_NORMAL)
#             
#             show_text_rect(self.ctx, str(i+1), 
#                            rec, fontsizeMinMax = (fontsize, fontsize),
#                            ha = 'c', orient = "h", b = 0.02, le = 0.7,
#                            wrap = False, couper = False
#                            ) 
#     
#     
    
    
    ######################################################################################  
    def DrawSequenceProjet(self, lienDoc, rect, yd, yl):
        """ Dessine le cadre d'une séquence ou d'un projet
            Avec une petite flèche pour démarrer le croisement avec les compétences
            
            yd = position y du cadre
            yl = position y de la ligne de croisement
        """
    #     print("DrawSequenceProjet", rect)

        doc = lienDoc.GetDoc()
        if doc is None:
            return
#         lienDoc.rect = []
        
        e = 0.0015 * COEF   # épaisseur du cadre
        x, y, w, h = rect
        
        y += e/4
        h -= e/2
        
        #
        # Flèche verticale indiquant la durée de la séquence/Projet
        #
        self.ctx.set_source_rgba (0.9,0.8,0.8,0.9)
           
        self.ctx.rectangle(x, y, self.wDuree, h)
        self.ctx.fill_preserve ()    
        self.ctx.set_source_rgba(0.4, 0.4, 0.4, 1)
        self.ctx.set_line_width(0.0006 * COEF)
        self.ctx.stroke ()
        
        self.ctx.set_source_rgb(0.5, 0.8, 0.8)
        self.ctx.select_font_face(self.font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
        
        if h > self.wDuree:
            orient = 'v'
        else:
            orient = 'h'
            
        show_text_rect(self.ctx, getHoraireTxt(doc.GetDuree()), 
                   (x, y, self.wDuree, h), 
                   orient = orient, b = 0.01)
        
        
        #
        # Tracé du cadre de la tâche
        #
        x += self.wDuree + self.ecartX/6
        w -= self.wDuree + self.ecartX/6
        
    
        
        lienDoc.pts_caract = [(x, y)]
            
        self.ctx.set_line_width(e)
        wd = self.ecartX/5  # Largeur du doigt
    #    print "BcoulPos", BcoulPos
        Rectangle_plein_doigt(self, (x, y, w, h), wd, yl-y, 
                              self.BcoulPos[doc.position[0]], 
                              self.IcoulPos[doc.position[0]], 
                              0.9).draw()
        
        #
        # Icone du type de document
        #
        if h > self.hTacheMini:
            bmp = doc.getIconeDraw()
            
            Image(self, (x, y, self.hTacheMini, self.hTacheMini), 
                  bmp, marge = 0.05).draw()
            
            # Ancienne méthode
#             self.ctx.save()
#         #     if doc.nom_obj == u"Séquence":
#         #         bmp = images.Icone_sequence.GetBitmap()
#         #     else:
#         #         bmp = images.Icone_projet.GetBitmap()
#              
#              
#             image = wx.lib.wxcairo.ImageSurfaceFromBitmap(bmp) 
#             self.ctx.translate(x+self.ecartX/5, y+self.ecartY/5)
#             self.ctx.scale(self.hTacheMini/120, self.hTacheMini/120)
#             self.ctx.set_source_surface(image, 0, 0)
#             self.ctx.paint ()
#             self.ctx.restore()
            
        
        #
        # Affichage de l'intitulé de la Séquence ou du Projet
        #
        self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_ITALIC,
                              cairo.FONT_WEIGHT_NORMAL)
        self.ctx.set_source_rgb (0,0,0)
        
        # Si on ne peut pas afficher l'intitulé dessous, on le met à coté
        rect = (x + self.hTacheMini, y, w - self.hTacheMini - wd, h)
        if rect[2] > 0:
    #         print("intit", doc, len(doc.intitule.strip()) > 0)
            if len(doc.intitule.strip()) > 0:
                intit = doc.intitule
            else:
                intit = lienDoc.GetNomFichier()
            show_text_rect(self.ctx, intit, rect, 
                           ha = 'g', b = 0.02,
                           fontsizeMinMax = (minFont, 0.015 * COEF))
        
        
#         lienDoc.rect.append([x, y, self.tailleZTaches[0], h])
        rect = (x, y, w - wd, h)
        self.prg.zones_sens.append(Zone_sens([rect], obj = lienDoc))
    #     lienDoc.pt_caract = [(rect[:2], "Seq")]
        
        #
        # Tracé des croisements "Tâches" et "Eleves"
        #
    #     yTaches.append([doc, y+h/2])
        
    #    DrawCroisementsCompetencesTaches(ctx, tache, y + h/2)
        
    #     y += h
    #     return y
            
            
            
    ######################################################################################  
    def DrawLigne(self, x, y, gras = False):
        dashes = [ 0.002 * COEF,   # ink
                   0.002 * COEF,   # skip
                   0.002 * COEF,   # ink
                   0.002 * COEF,   # skip
                   ]
        
        if gras:
            self.ctx.set_line_width (0.002 * COEF)
        else:
            self.ctx.set_line_width (0.001 * COEF)
        self.ctx.set_dash(dashes, 0)
        ligne(self.ctx, self.posZOrganis[0]+self.tailleZOrganis[0], y,
              x, y, (0, 0.0, 0.2, 0.6))
        self.ctx.set_dash([], 0)       
    


     

    
    
    ######################################################################################  
    def DrawCroisementsCompetencesTaches(self, seq, y):
        self.DrawBoutonCompetence(seq, seq.GetCompetencesVisees(), y)
        
    ######################################################################################  
    def DrawCroisementsSavoirsTaches(self, seq, y):
        self.DrawBoutonSavoir(seq, seq.GetSavoirsVises(), y)
        
    #####################################################################################  
    def DrawCroisementsCISeq(self, seq, y):
        """ Dessine les "ronds" à cliquer
        """ 
        #
        # Croisements Sequence/CI
        #
        ref = self.prg.GetReferentiel()
        lstCI = self.prg.GetListeCI()
    #    print "DrawCroisementsCISeq", lstCI
        dy = 0
        r = 0.004 * COEF
            
        for num, CI in enumerate(lstCI):
            color0 = self.CoulAltern[num][0]
            color1 = self.CoulAltern[num][1]
    
            _x = self.xCI[num]
            
            if num in seq.CI.numCI or CI in seq.CI.CI_perso:
                Boule(self, _x, y, r, 
                      color0 = color0, color1 = color1,
                      transparent = False).draw()
            elif num < len(ref.CentresInterets):
                self.ctx.set_source_rgba (0,0,0,1)
                self.ctx.arc (_x, y, r, 0, 2*pi)
                self.ctx.stroke()
                Boule(self, _x, y, r, 
                      color0 = color0, color1 = (1,1,1),
                      transparent = False).draw()
            
            self.prg.zones_sens.append(Zone_sens([(_x -r , y - r, 2*r, 2*r)], obj = seq, param = "CI"+str(num)))
    #        tache.projet.eleves[i].rect.append((_x -r , y - r, 2*r, 2*r))
    #        tache.projet.eleves[i].pts_caract.append((_x,y))
            y += dy
            
    
     
    
    
    
    
    
    ######################################################################################  
    def DrawBoutonCompetence(self, seq, listComp, y, h = None, nbr = None):
        """ Dessine les petits rectangles des compétences abordées dans la Séquence
        
        : nbr : nombre de fois que chaque compétence est abordée (pour bilan seulement)
        
        """
    #     print "DrawBoutonCompetence", seq, listComp, nbr
        
        if seq == None and len(listComp) == 0:
            return
        
        if h == None: # Toujours sauf pour les revues
    #         h = 0.6*wColComp
            h = 0.004 * COEF  # ne pas le faire dépendre de wColComp, qui va beaucoup varier !
            
        if nbr == None:
            nbr = [1] * (len(listComp)+1)
            lig = True
        else:
            lig = False
            
        dh = h / max(nbr)    
        
        self.ctx.set_line_width(0.0004 * COEF)
        listComp = [k[1:] for k in listComp]
        
        ref = self.prg.GetReferentiel()
        structComp = ref.dicoCompetences["S"].get2Niveaux()
        dicoComp = ref.dicoCompetences["S"]
    #     print structComp
    #     print dicoComp.dicCompetences
        for i, (k1, l1) in enumerate(structComp):
    #         print "   ",k1, l1 
    #         print "   ", dicoComp.dicCompetences[k1].sousComp
            
            # Lignes commentées pour 7.1.16
            if len(l1) == 0:
                l1 = [k1]
            
            for k2 in l1:
                x = self.xComp[k2]
    #             print "      ", k2
                if len(dicoComp.dicCompetences[k1].sousComp) > 0:
                    comp = dicoComp.dicCompetences[k1].sousComp[k2] 
                    if len(comp.sousComp) > 0:
                        lc = sorted(comp.sousComp.keys())
                    else:
                        lc = [k2]
                else:
                    comp = dicoComp.dicCompetences[k1]
                    lc = [k1]
                    
                dx = self.wColComp/len(lc)
                for a, i in enumerate(lc):
                    if i in listComp:
                        H = nbr[listComp.index(i)] * dh
                        rect = (x+a*dx, y+h-H, dx, H)
                        self.ctx.set_source_rgba(*self.ICoulComp[self.cComp[k2]])
                        self.ctx.rectangle(*rect)
                        self.ctx.fill_preserve ()
                        self.ctx.set_source_rgba (0, 0 , 0, 1)
                        self.ctx.stroke()
                    else:
                        if lig:
                            rect = (x+a*dx, y, dx, h)
                            self.ctx.set_source_rgba (1, 1, 1, 0)
                            self.ctx.move_to(rect[0], rect[1])
                            self.ctx.rel_line_to(0, rect[3])
                            self.ctx.move_to(rect[0]+rect[2], rect[1])
                            self.ctx.rel_line_to(0, rect[3])
                            self.ctx.set_source_rgba (0, 0 , 0, 1)
                            self.ctx.stroke()
                        else:
                            rect = None
                            
                    if rect is not None:
                        self.prg.zones_sens.append(Zone_sens([rect], obj = seq, param = "CMP"+i))
                    
        
        
        return
        
        
    ######################################################################################  
    def DrawBoutonSavoir(self, seq, listSav, y, h = None, nbr = None):
        """ Dessine les petits rectangles des Savoirs abordés dans la Séquence
        
        : nbr : nombre de fois que chaque Savoir est abordé (pour bilan seulement)
        
        """
    #     print "DrawBoutonSavoir", seq, listComp, nbr
        
        if seq == None and len(listSav) == 0:
            return
        
        if h == None: # Toujours sauf pour les revues
    #         h = 0.6*wColComp
            h = 0.004 * COEF  # ne pas le faire dépendre de wColComp, qui va beaucoup varier !
            
        if nbr == None:
            nbr = [1] * (len(listSav)+1)
            lig = True
        else:
            lig = False
            
        dh = h / max(nbr)    
        
        self.ctx.set_line_width(0.0004 * COEF)
        listSav = [k[1:] for k in listSav]
        
        ref = self.prg.GetReferentiel()
        structSav = ref.dicoSavoirs["S"].get2Niveaux()
        dicoSav = ref.dicoSavoirs["S"]
    #     print structComp
    #     print dicoComp.dicCompetences
        for i, (k1, l1) in enumerate(structSav):
    #         print "   ",k1, l1 
    #         print "   ", dicoComp.dicCompetences[k1].sousComp
            
            # Lignes commentées pour 7.1.16
            if len(l1) == 0:
                l1 = [k1]
            
            for k2 in l1:
                x = self.xComp[k2]
    #             print "      ", k2
                if len(dicoSav.dicSavoirs[k1].sousSav) > 0:
                    sav = dicoSav.dicSavoirs[k1].sousSav[k2] 
                    if len(sav.sousSav) > 0:
                        lc = sorted(sav.sousSav.keys())
                    else:
                        lc = [k2]
                else:
                    sav = dicoSav.dicSavoirs[k1]
                    lc = [k1]
                    
                dx = self.wColComp/len(lc)
                for a, i in enumerate(lc):
                    if i in listSav:
                        H = nbr[listSav.index(i)] * dh
                        rect = (x+a*dx, y+h-H, dx, H)
                        self.ctx.set_source_rgba(*self.ICoulComp[self.cComp[k2]])
                        self.ctx.rectangle(*rect)
                        self.ctx.fill_preserve ()
                        self.ctx.set_source_rgba (0, 0 , 0, 1)
                        self.ctx.stroke()
                    else:
                        if lig:
                            rect = (x+a*dx, y, dx, h)
                            self.ctx.set_source_rgba (1, 1, 1, 0)
                            self.ctx.move_to(rect[0], rect[1])
                            self.ctx.rel_line_to(0, rect[3])
                            self.ctx.move_to(rect[0]+rect[2], rect[1])
                            self.ctx.rel_line_to(0, rect[3])
                            self.ctx.set_source_rgba (0, 0 , 0, 1)
                            self.ctx.stroke()
                        else:
                            rect = None
                            
                    if rect is not None:
                        self.prg.zones_sens.append(Zone_sens([rect], obj = seq, param = "SAV"+i))
                    
        
        
        return
        
        







def gabarit():
    
    print("Génération du gabarit ...", end=' ') 
    import draw_cairo_prg
    imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  2100, 2970)#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
    ctx = cairo.Context(imagesurface)
    
    e = 29.7
    ctx.scale(e, e) 
    
    
#     print dir(draw_cairo_prj)
    pos = {}
    taille = {}
    for attr in dir(draw_cairo_prg):
        if attr[:3] == 'pos':
            pos[attr[3:]] = attr
        if attr[:6] == 'taille':
            taille[attr[6:]] = attr
    
    print(pos, taille)
    
    ctx.set_line_width(5.0/e)
    
    for k, p in list(pos.items()):
        if k in list(taille.keys()):
            x, y = getattr(draw_cairo_prg, p)
            w, h = getattr(draw_cairo_prg, taille[k])
            
            txt = k+"\n"+",".join([str(t) for t in [x, y, w, h]])
            try:
                ctx.rectangle(x, y, w, h)
                ctx.stroke()
                show_text_rect(ctx, txt, 
                               (x, y, w, h), fontsizeMinMax = (-1, 30.0/e),
                               wrap = False, couper = False,
                               va = 'h', ha = 'g' )
            except:
                print("   ", k, " : ", x, y, w, h)
    
    
    imagesurface.write_to_png('gabarit_prg.png')
    



# if __name__ == '__main__':
#     sauverParametres(getParametres().keys(), 
#                      nom_module, 
#                      nom_fichparam)
#     
#     
    