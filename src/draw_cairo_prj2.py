#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               draw_cairo_prj                            ##
##                                                                         ##
##                         Tracé des fiches de projet                      ##
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

# import cairo
# from draw_cairo import *
import cairocffi as cairo
from draw_cairo2 import *

from math import log
# from couleur import CouleurFloat2CSS

import util_path

#from constantes import Effectifs, NomsEffectifs, listeDemarches, Demarches, getSavoir, getCompetence, \
#                        DemarchesCourt, estCompetenceRevue
import constantes

# Les constantes partagées
from Referentiel import REFERENTIELS
import Referentiel


## Pour dessiner la cible ...
import os
import tempfile
import wx


import couleur

    
######################################################################################  
def getPts(lst_rect):
        lst = []
        for rect in lst_rect:
            lst.append(rect[:2])
        return lst



######################################################################################  




######################################################################################  
def regrouperLst(prjRef, lstCompetences):
#    print "regrouperLst", lstCompetences
#    print "   _dicoCompetences", obj.GetProjetRef()._dicoCompetences["S"]
    lstCompetences.sort()
    if prjRef is not None and prjRef._niveau == 3:
        lstGrpCompetences = []
        for disc, tousIndicateurs in prjRef._dicoCompetences.items():
            dic = []
            for k0, competence in tousIndicateurs.items():
                for k1, sousComp in competence.sousComp.items():
                    for k2 in sorted(sousComp.sousComp.keys()):
                        if disc+k2 in lstCompetences:
                            dic.append(disc+k1)
            dic = list(set(dic))
            dic.sort()
        lstGrpCompetences.extend(dic)
#        print "  >>", dic
        return lstGrpCompetences
    else:
        return lstCompetences





######################################################################################  
class Projet(Base_Fiche_Doc):
    def __init__(self, prj, mouchard = False, pourDossierValidation = False, 
                 entete = False, surRect = None):
        Base_Fiche_Doc.__init__(self)
        self.prj = prj
        self.mouchard = mouchard
        self.entete = entete
        self.surRect = surRect
        self.pourDossierValidation = pourDossierValidation
        
        
        self.CoulAltern = []
        self.ICoulComp = []
        
        
        #
        # Données pour le tracé
        #
        
        # Nom du projet
        self.tailleNom = (0.29 * COEF, 0.04 * COEF)
        self.posNom = (self.margeX, self.margeY)
        self.Icoul_Nom = (0.9, 0.8, 0.8, 0.85)
        self.Bcoul_Nom = (0.3, 0.2, 0.25, 1)
        self.fontNom = 0.014 * COEF
        
        # Support du projet
        self.tailleSup = (0.17 * COEF, 0.06 * COEF)
        self.posSup = (self.margeX, self.posNom[1] + self.tailleNom[1] + self.ecartY)
        self.Icoul_Sup = (0.85, 0.8, 0.8, 0.85)
        self.Bcoul_Sup = (0.28, 0.2, 0.25, 1)
        self.fontSup = 0.012 * COEF
        
        # Equipe pédagogique
        self.tailleEqu = (0.17 * COEF, 0.18 * COEF - self.tailleSup[1]- self.tailleNom[1] - 3*self.ecartY/2)
        self.posEqu = (self.margeX, self.posSup[1] + self.tailleSup[1] + self.ecartY)
        self.Icoul_Equ = (0.8, 0.8, 0.9, 0.85)
        self.Bcoul_Equ = (0.2, 0.25, 0.3, 1)
        self.fontEqu = 0.011 * COEF
        
        # Position dans l'année
        self.posPos = [None, self.margeY - self.ecartY/2]
        self.taillePos = [None, 0.03 * COEF]
        
        # Problématique
        self.posPro = [self.posNom[0] + self.tailleNom[0] + self.ecartX/2, self.margeY + self.taillePos[1] + self.ecartY/2]
        self.taillePro = [self.LargeurTotale - self.margeX - self.posPro[0], self.posEqu[1] + self.tailleEqu[1] - self.posPro[1]]
        self.Icoul_Pro = (0.8, 0.9, 0.8, 0.85)
        self.Bcoul_Pro = (0.25, 0.3, 0.2, 1)
        self.fontPro = 0.014 * COEF
        
        # Image du support
        self.posImg = [self.posSup[0] + self.tailleSup[0] + self.ecartX/4, self.posNom[1] + self.tailleNom[1] + self.ecartY]
        self.tailleImg = [self.posPro[0] - self.posImg[0] - self.ecartX/4, None]
        self.tailleImg[1] = self.posEqu[1] + self.tailleEqu[1] - self.posSup[1]
        self.Icoul_Img = (0.8, 0.8, 1, 0.85)
        self.Bcoul_Img = (0.1, 0.1, 0.25, 1)
        self.centreImg = (self.posImg[0] + self.tailleImg[0] / 2 + 0.0006 * COEF, self.posImg[1] + self.tailleImg[0] / 2 - 0.004 * COEF)
        
        # Zone d'organisation du projet (grand cadre)
        self.posZOrganis = (self.margeX, 0.24 * COEF)
        self.bordureZOrganis = 0.01 * COEF
        self.tailleZOrganis = (self.LargeurTotale-2*self.margeX, 1 * COEF-self.ecartY-self.posZOrganis[1]-self.bordureZOrganis)
        
        # Zone de déroulement du projet
        self.posZDeroul = [self.margeX, None]
        self.tailleZDeroul = [None, None]
        self.Icoul_ZDeroul = (1, 1, 0.7, 0.85)
        self.Bcoul_ZDeroul = (0.4, 0.4, 0.03, 1)
        self.fontZDeroul = 0.014 * COEF
        self.wPhases = 0.04 * COEF      # Taille du label "phases"
        self.wDuree = 0.012 * COEF       # Taille de la fleche "duree"
        
        
        # Zones des tableaux des éléves
        self.posZElevesV = [None, 0.24 * COEF]
        self.tailleZElevesV = [None, None]
        self.posZElevesH = [self.posZDeroul[0], self.posZElevesV[1]]
        self.tailleZElevesH = [None, None]
        self.wEleves = 0.015 * COEF
        self.hEleves = 0.020 * COEF
        self.xEleves = []
        self.yEleves = []
        
        # Zone du tableau des compétences
        self.posZComp = [None, None]
        self.tailleZComp = [None, None]
        self.wColCompBase = 0.018 * COEF
        self.wColComp = self.wColCompBase
        self.xComp = {}
        
        
        
        self.ICoulComp = {}
        self.BCoulCompS = (0.7, 0.7, 0.7, 0.2)      # couleur "Soutenance"
        
        
        # Zone des tâches
        self.posZTaches = [self.posZDeroul[0] + self.wPhases + self.wDuree + self.ecartX*3/6, None]
        self.tailleZTaches = [None, None]
        self.hTacheMini = self.ecartY/2
        self.hRevue = self.ecartY/3
        self.yTaches = []
        self.ecartTacheY = None  # Ecartement entre les tâches de phase différente
    
        # paramètres pour la fonction qui calcule la hauteur des tâches 
        # en fonction de leur durée
        self.a = self.b = None
    
        self.BCoulTache = {'Sup' : (0.3,0.4,0.4), 
                          'Ana' : (0.3,0.5,0.5), 
                          'Con' : (0.5,0.3,0.5), 
                          'DCo' : (0.55,0.3,0.45),
                          'Rea' : (0.5,0.5,0.3), 
                          'Val' : (0.3,0.3,0.7),
                          'XXX' : (0.3,0.3,0.7),
                          'Rev' : (0.6,0.3,0.3),
                          'R1'  : (0.8,0.3,0.2),
                          'R2'  : (0.8,0.3,0.2),
                          'R3'  : (0.8,0.3,0.2),
                          'S'   : (0.3,0.1,0.8)}
        
        self.ICoulTache = {'Sup' : (0.6, 0.7, 0.7,1),
                          'Ana' : (0.6, 0.8, 0.8,1), 
                          'Con' : (0.8, 0.6, 0.8,1),
                          'DCo' : (0.9, 0.6, 0.7,1),
                          'Rea' : (0.8, 0.8, 0.6,1), 
                          'Val' : (0.6, 0.6, 1.0,1),
                          'XXX' : (0.6, 0.6, 1.0,1),
                          'Rev' : (0.9,0.6,0.6,0.8),
                          'R1'  : (1,0.6,0.5,0.8),
                          'R2'  : (1,0.6,0.5,0.8),
                          'R3'  : (1,0.6,0.5,0.8),
                          'S'   : (0.6,0.5,1,0.8)}
        
        
        self.ecartYElevesTaches = 0.05 * COEF

        self.p_coul_a1 = (0.85, 0.85, 0.95, 0.3)
        self.p_coul_a2 = (0.7,  0.7,  0.8,  0.2)
        
        self.p_coul_cmpC = (1, 0.6, 0.7, 0.2)      # couleur "Conduite"
        self.p_coul_cmpS = (0.598, 0.7, 1, 0.2)    # couleur "Soutenance"
        
    
    ######################################################################################  
    def DefinirZones(self):
        """ Calcule les positions et dimensions des différentes zones de tracé
            en fonction du nombre d'éléments (élèves, tâches, compétences)
        """
#         global ecartTacheY, intituleTaches, fontIntTaches, xEleves, yEleves, a, b, yTaches, wColComp, xComp
        
        #
        # Zone du tableau des compétences - X
        #
    
    #    wColComp = prj.GetReferentiel().calculerLargeurCompetences(wColCompBase)
        competences = regrouperLst(self.prj.GetProjetRef(), self.prj.GetCompetencesUtil())
        self.tailleZComp[0] = self.wColComp * len(competences)
        self.posZComp[0] = self.posZOrganis[0] + self.tailleZOrganis[0] - self.tailleZComp[0]
        self.xComp = {}
        for i, s in enumerate(competences):
            self.xComp[s] = self.posZComp[0] + (i+0.5) * self.wColComp
        
        #
        # Zone du tableau des élèves
        #
        self.tailleZElevesV[0] = self.wEleves * len(self.prj.eleves + self.prj.groupes)
        self.tailleZElevesH[1] = self.hEleves * len(self.prj.eleves + self.prj.groupes)
        self.posZElevesV[0] = self.posZComp[0] - self.tailleZElevesV[0] - self.ecartX/2
        self.tailleZElevesH[0] = self.posZElevesV[0]-self.posZElevesH[0]- self.ecartX/2
        self.tailleZElevesV[1] = self.posZOrganis[1] + self.tailleZOrganis[1] - self.posZElevesV[1]
        self.xEleves = []
        self.yEleves = []
        for i in range(len(self.prj.eleves + self.prj.groupes)):
            self.xEleves.append(self.posZElevesV[0] + (i+0.5) * self.wEleves)
            self.yEleves.append(self.posZElevesH[1] + (i+0.5) * self.hEleves)
    
    
        # Zone du tableau des compétences - Y
        self.posZComp[1] = self.posZElevesH[1] + self.tailleZElevesH[1]
        self.tailleZComp[1] = self.ecartYElevesTaches            
                     
                     
        # Zone de déroulement du projet
        self.posZDeroul[1] = self.posZElevesH[1] + self.tailleZElevesH[1] + self.tailleZComp[1] - self.ecartY/2
        self.tailleZDeroul[0] = self.posZElevesV[0] - self.posZDeroul[0] - self.ecartX/2
        self.tailleZDeroul[1] = self.posZOrganis[1] + self.tailleZOrganis[1] - self.posZDeroul[1]
        
        
        # Zone des tâches
        self.yTaches = []
        self.posZTaches[1] = self.posZDeroul[1] + self.ecartY/2
        self.tailleZTaches[0] = self.posZDeroul[0] + self.tailleZDeroul[0] - self.posZTaches[0] - self.ecartX/2
        self.tailleZTaches[1] = self.tailleZDeroul[1] - self.ecartY/2 - 0.04 * COEF    # écart pour la durée totale
        
        self.calculCoefCalcH(self.hTacheMini)
        if self.a < 0:   # Trop de tâches -> on réduit !
            self.calculCoefCalcH(self.hTacheMini/2)
    
    
    ######################################################################################  
    def calculCoefCalcH(self, hm):
#         global ecartTacheY, a, b
        self.ecartTacheY = self.ecartY/3
        sommeEcarts = (self.prj.GetNbrPhases()-1)*self.ecartTacheY
        
        # Calcul des paramètres de la fonction hauteur = f(durée)
        # hauteur = a * log(durée) + b
        self.b = 0
        self.a = 1
        h = 0#ecartTacheY
        nt = 0 # nombre de tâches de hauteur variable ( = calculée par calcH() )
        hrv = 0 # Hauteur totale des revues différenciant les élèves
        hrf = 0 # Hauteur totale des revues de taille fixe
        for t in self.prj.taches:
            if t.phase in ["R1", "R2", "R3", "S"]:
                if t.DiffereSuivantEleve():
                    hrv += max(len(t.projet.eleves + t.projet.groupes) * self.hRevue, self.hRevue)
                else:
                    hrf += self.hRevue
            else:
                h += self.calcH(t.GetDuree())
                nt += 1
        
    #    hr = (prj.nbrRevues+1)*len(prj.eleves)*hRevue
        
        
    #    hr = (len(prj.taches)-nt)*len(prj.eleves)*hRevue
    
        self.b = hm # Hauteur mini
        
        hFixe = sommeEcarts + hrv + hrf
    
        if h != 0:
            self.a = (self.tailleZTaches[1] - hFixe - self.b*nt) / h
        
        
    
    ######################################################################################  
    def calcH_tache(self, tache):
        if (tache.phase in ["R1", "R2", "R3", "S"] and tache.DiffereSuivantEleve()):
            return max(len(tache.projet.eleves + tache.projet.groupes) * self.hRevue, self.hRevue)
        else:
            return self.calcH(tache.GetDuree())
    
        
    ######################################################################################  
    def calcH(self, t):
        if t != 0:
            return self.a*log(t/constantes.DUREE_REVUES)+self.b
        return 2*self.ecartTacheY
    
    
    ######################################################################################  
    def getCoulComp(self, partie, alpha = 1.0):
#         print("getCoulComp", partie)
        if partie in self.ICoulComp:
            return (*self.ICoulComp[partie][:3], alpha)  
        return (*self.ICoulComp[''][:3], alpha)

    
    ######################################################################################  
    def definirCouleurs(self):        
        # Les couleurs des parties (Conduite - Soutenance)
        pr = self.prj.GetProjetRef()
        for i, pa in enumerate(pr.listeParties):
            if i%2 == 0:
                self.ICoulComp[pa] = self.p_coul_cmpC
            else:
                self.ICoulComp[pa] = self.p_coul_cmpS
            
        
        # Des couleurs alternées (pour les lignes de croisement)
        n3 = len(self.prj.eleves + self.prj.groupes)
        del self.CoulAltern[:]
        for _ in range(n3//2+1):
            self.CoulAltern += [(self.p_coul_a1,    (0, 0, 0, 1)),
                                (self.p_coul_a2,    (0, 0, 0, 1))]

        
    ######################################################################################  
    def regrouperDic(self, obj, dicIndicateurs):
    #     print("regrouperDic", dicIndicateurs)
    #     print "   _dicoCompetences", obj.GetProjetRef()._dicoCompetences
        if obj.GetProjetRef() is None or obj.GetProjetRef()._pasdIndic:
            return dicIndicateurs, {k:[{'C':0}] for k in dicIndicateurs}
        
        if obj.GetProjetRef()._niveau == 3:
            dic = {}
            typ = {}
            for disc, tousIndicateurs in obj.GetProjetRef()._dicoCompetences.items():
    #             print "   ", disc, tousIndicateurs
                for competence in tousIndicateurs.values():
    #                 print "      ",k0,  competence
                    for k1, sousComp in competence.sousComp.items():
    #                     print "         ", k1, sousComp
                        dic[disc+k1] = []
                        typ[disc+k1] = []
                        lk2 = list(sousComp.sousComp.keys())
                        lk2.sort()
        #                print "  ", lk2
                        for k2 in lk2:
                            if disc+k2 in dicIndicateurs.keys():
                                dic[disc+k1].extend(dicIndicateurs[disc+k2])
        #                        print "   **", v1[1][k2]
                                typ[disc+k1].extend([p.poids for p in sousComp.sousComp[k2].indicateurs])
                            else:
                                l = len(sousComp.sousComp[k2].indicateurs)
                                dic[disc+k1].extend([False]*l)
                                typ[disc+k1].extend(['']*l)
                        
                        if not disc+k1 in self.xComp.keys():
    #                     if dic[disc+k1] == [] or not (True in dic[disc+k1]):
                            del dic[disc+k1]
                            del typ[disc+k1]
                        
    #         print "  >>>", dic
    #         print "     ", typ
            return dic, typ
        else:
            dic = {}
            typ = {}
            for disc, tousIndicateurs in obj.GetProjetRef()._dicoCompetences.items():
    #             print "-----", disc
                for competence in tousIndicateurs.values():
    #                 print "     ", k0, competence
                    for k1, sousComp in competence.sousComp.items():
    #                     print "        ", k1, sousComp
                        dic[disc+k1] = []
                        typ[disc+k1] = []
                        
                        
                        if disc+k1 in dicIndicateurs.keys():
                            dic[disc+k1].extend(dicIndicateurs[disc+k1])
    #                        print "   **", v1[1][k2]
                            typ[disc+k1].extend([p.poids for p in sousComp.indicateurs])
                        else:
                            l = len(sousComp.indicateurs)
                            dic[disc+k1].extend([False]*l)
                            typ[disc+k1].extend(['']*l)
                        
                        
                        if not disc+k1 in self.xComp.keys():
    #                     if dic[disc+k1] == [] or not (True in dic[disc+k1]):
                            del dic[disc+k1]
                            del typ[disc+k1]
                        
    #         print "  >>", dic
    #         print "    ", typ
            return dic, typ
    
    
    
        
    ######################################################################################  
    def draw(self, ctx):
        """ Dessine une fiche de projet du projet <prj>
            dans un contexte cairo <ctx>
        """
        #        print "Draw séquence"
        
        self.ctx = ctx
        
        #
        # Options générales
        #
        self.initOptions(ctx)
        self.DefinirZones()
        self.definirCouleurs()
#         print("ICoulComp", self.ICoulComp)
        #
        # Objects annexes
        #
        prjeval = self.prj.GetProjetRef()
        
        
    #     gabarit()
    
        #
        #    pour stocker des zones caractéristiques (à cliquer, ...)
        #
        # Zones sensibles, depuis pySéquence
        self.prj.zones_sens = []
        # Points caractéristiques des rectangles
        self.prj.pt_caract = []  # Contenu attendu : ((x,y), code)
        # Points caractéristiques des rectangles (sans code)
        self.prj.pts_caract = [] 
        
        
        
        #
        # Type d'enseignement
        #
        tailleTypeEns = self.taillePro[0]/2
        t = self.prj.classe.GetLabel()
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_BOLD)
        ctx.set_source_rgb (0.6, 0.6, 0.9)
        
        h = self.taillePos[1] * 0.8
        show_text_rect(ctx, t, (self.posPro[0] , self.posPos[1], tailleTypeEns, h), 
                       va = 'c', ha = 'g', b = 0, orient = 'h', 
                       fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                       coulBord = (0, 0, 0))
        
        t = self.prj.classe.GetLabelComplet()
        ctx.set_source_rgb (0.3, 0.3, 0.8)
        show_text_rect(ctx, t, (self.posPro[0] , self.posPos[1] + h, tailleTypeEns, self.taillePos[1] - h), 
                       va = 'c', ha = 'g', b = 0, orient = 'h', 
                       fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False)
        
    
        #
        # Position dans l'année
        #
    #    posPos[0] = posEqu[0] + tailleEqu[0] + ecartX + tailleTypeEns
        self.posPos[0] = self.posNom[0] + self.tailleNom[0] + self.ecartX + tailleTypeEns
    #    taillePos[0] =  0.72414 - posPos[0] - margeX
        self.taillePos[0] = self.taillePro[0]/2
        ctx.set_line_width (0.0015 * COEF)
        r = (*self.posPos, *self.taillePos)
        rects = Periodes(self, r, 
                         self.prj.getRangePeriode(), self.prj.classe.referentiel.periodes,
                         self.prj.classe.referentiel.projets).draw()
        
        for i, re in enumerate(rects):
            self.prj.zones_sens.append(Zone_sens([re], param = "POS"+str(i)))
        self.prj.zones_sens.append(Zone_sens([r], param = "POS"))
    
    
    
        #
        # Etablissement
        #
        if self.prj.classe.etablissement != "":
            t = self.prj.classe.etablissement + " (" + self.prj.classe.ville + ")"
            ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                              cairo.FONT_WEIGHT_NORMAL)
            show_text_rect(ctx, t, (self.posPos[0] , self.posPos[1]+self.taillePos[1], self.taillePos[0], self.posPro[1]-self.posPos[1]-self.taillePos[1]), 
                           va = 'c', ha = 'g', b = 0.02, orient = 'h', 
                           fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                           coulBord = (0, 0, 0))
    
        
        #
        # Image
        #
    #    prj.support.rect = []
        self.prj.support.pts_caract = []
        bmp = self.prj.support.image
        if bmp != None:
            Image(self,
                  (*self.posImg, *self.tailleImg),
                  bmp).draw()
            
            self.prj.zones_sens.append(Zone_sens([self.posImg + self.tailleImg], obj = self.prj.support))
            self.prj.support.pts_caract.append(self.posImg)
        
    
    
        #
        #  Equipe
        #
        rectEqu = self.posEqu + self.tailleEqu
        self.prj.pt_caract.append((Curve_rect_titre(self, rectEqu, "Equipe pédagogique",   
                                                    self.Bcoul_Equ, 
                                                    self.Icoul_Equ, 
                                                    self.fontEqu).draw(),
                            "Equ"))
        
        lstTexte = []
        g = None
        c = []
        for i, p in enumerate(self.prj.equipe):
            lstTexte.append(p.GetNomPrenom(disc = constantes.AFFICHER_DISC_FICHE))
            if p.referent:
                g = i
            c.append(constantes.COUL_DISCIPLINES[p.discipline])
        lstCodes = [" \u25CF"] * len(lstTexte)
    
       
        if len(lstTexte) > 0:
            r = Liste_code_texte(self, (self.posEqu[0], self.posEqu[1], self.tailleEqu[0], self.tailleEqu[1]+0.0001 * COEF),
                                 lstCodes, lstTexte, 
                                 0.1*self.tailleEqu[1]+0.0001 * COEF, 0.1,
                                 gras = g, lstCoul = c, va = 'c').draw()
    
        
        for i, p in enumerate(self.prj.equipe):
            self.prj.zones_sens.append(Zone_sens([r[i]], obj = p))
        self.prj.zones_sens.append(Zone_sens([rectEqu], param = "EQU"))
        
    
        #
        #  Problématique
        #
        rectPro = self.posPro + self.taillePro
        pt = Curve_rect_titre(self, rectPro, "Problématique",  
                              self.Bcoul_Pro, self.Icoul_Pro, self.fontPro).draw()
        self.prj.pt_caract.append((pt, "Pb"))
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, constantes.ellipsizer(self.prj.problematique, constantes.LONG_MAX_PROBLEMATIQUE), 
                       rectPro, ha = 'g', b = 0.02,
                       fontsizeMinMax = (-1, 0.016 * COEF))
        self.prj.zones_sens.append(Zone_sens([rectPro], param = "PB"))
        
    #    print "     6 ", time.time() - tps
    
    
        #
        #  Projet
        #
        rectNom = self.posNom+self.tailleNom
        self.prj.pts_caract.append(Curve_rect_titre(self, rectNom, self.prj.GetCode(),  
                                               self.Bcoul_Nom, 
                                               self.Icoul_Nom, 
                                               self.fontNom).draw())
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, self.prj.GetNom(), 
                       rectNom, ha = 'c', b = 0.02,
                       fontsizeMinMax = (-1, 0.016 * COEF))
        
        self.prj.zones_sens.append(Zone_sens([rectNom], obj = self.prj))
        self.prj.pts_caract.append(self.posNom)
    
        
        
        #
        #  Support
        #
        self.prj.support.pt_caract = []
        rectSup = self.posSup+self.tailleSup
#         print("rectSup", rectSup)
        pt = Curve_rect_titre(self, rectSup, self.prj.support.GetCode(),  
                              self.Bcoul_Sup, self.Icoul_Sup, self.fontSup).draw()
        self.prj.support.pt_caract.append((pt, "Sup"))
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, self.prj.support.GetNom(), 
                       rectSup, ha = 'c', b = 0.02,
                       fontsizeMinMax = (-1, 0.016 * COEF))
#         print("rectSup >>", rectSup)
        self.prj.zones_sens.append(Zone_sens([rectSup], obj = self.prj.support))
    #     prj.support.pts_caract.append(posSup)
    
    
    
        #
        #  Tableau des compétenecs
        #
        if not self.entete:
            competences = regrouperLst(prjeval, self.prj.GetCompetencesUtil())
    #         print "competences", competences
    #         prj.pt_caract_comp = []
            
            if competences != []:
                
                ctx.set_line_width(0.001 * COEF)
                wc = self.tailleZComp[0]/len(competences)
                _x = self.posZComp[0]
                _y0, _y1 = self.posZElevesH[1], self.posZDeroul[1] + self.tailleZDeroul[1]
                
                for _ in competences:
        #            s.rect=((_x, _y, wc, posZTaches[1] - posZComp[1]),)
                    ligne(ctx, _x, _y0, _x, _y1, (0, 0, 0))
                    ctx.set_source_rgba(0.5, 0.5, 0.5, 0.2)
                    ctx.rectangle(_x, _y0,  
                                  wc, _y1-_y0)
                    ctx.fill()
                    _x += wc
                
                ligne(ctx, _x, _y0, _x, _y1, (0, 0, 0))
                
                ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_NORMAL)
                ctx.set_source_rgb(0, 0, 0)
                ctx.set_line_width(0.001 * COEF)
                p = TableauV(self, [c[1:] for c in competences], self.posZComp[0], self.posZComp[1], 
                             self.tailleZComp[0], self.tailleZComp[1], 
                             0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', 
                              coul = self.BCoulCompS).draw()
                for pt in getPts(p):
                    self.prj.pt_caract.append((pt, "Cmp"))
    
    #    print "compétences", time.time() - tps
    
    
        #
        #  Tableau des élèves
        #   
    #    tps = time.time()
        if not self.entete:
            ctx.select_font_face(self.font_family, cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(0.001 * COEF)
            l=[]
            for i,e in enumerate(self.prj.eleves) : 
                e.pts_caract = []
                if self.pourDossierValidation:
                    
                    l.append(self.prj.GetReferentiel().labels["ELEVES"][2].Sing_()+" "+str(i+1))
                else:
                    l.append(e.GetNomPrenom())
            
            for i,e in enumerate(self.prj.groupes) : 
                e.pts_caract = []
                l.append(e.GetNomPrenom())
            
            #
            # Graduation
            #
            y = self.posZElevesH[1] + self.tailleZElevesH[1]
            w = self.tailleZElevesH[0]
            h = self.hEleves/2
            for t, ha in [("0%", 'g'), ("50%", 'c'), ("100%", 'd')]:
                show_text_rect(ctx, t, 
                               (self.posZElevesH[0], y, w, h), ha = ha, b = 0.01,
                               fontsizeMinMax = (-1, 0.016 * COEF))
            
    #         prj.pt_caract_eleve = []
            if len(l) > 0:
                
                #
                # Barres d'évaluabilité
                #
                if prjeval is None:
                    parties = []
                else:
                    parties = prjeval.listeParties
                
                for i, e in enumerate(self.prj.eleves + self.prj.groupes):
                    ev = e.GetEvaluabilite(compil = True)[1]
                    y = self.posZElevesH[1] + i*self.hEleves
        #            wr = tailleZElevesH[0]*r
        #            ws = tailleZElevesH[0]*s
                    hb = self.hEleves/(len(parties)+1)
        #            y = posZElevesH[1] + (2*i*hb)+hb/2
                    
        
                    
                    for j, part in enumerate(parties):
                        
                        BarreH(self, self.posZElevesH[0], y+(j+1)*hb, 
                               self.tailleZElevesH[0], 
                               ev[part][0], ev[part][1], hb, 
                               (1, 0, 0, 0.7), (0, 1, 0, 0.7), 
                               self.getCoulComp(part)).draw()
                    
        
                rec = TableauH(self, l, self.posZElevesH[0], self.posZElevesH[1], 
                               self.tailleZElevesH[0], 0, self.tailleZElevesH[1], 
                               va = 'c', ha = 'd', orient = 'h', coul = self.CoulAltern).draw()
                
                for pt in getPts(rec):
                    self.prj.pt_caract.append((pt, "Elv"))
                
                #
                # Lignes horizontales
                #
                for i, e in enumerate(self.prj.eleves + self.prj.groupes):
                    self.prj.zones_sens.append(Zone_sens([rec[i]], obj = e))
                    ctx.set_line_width(0.003 * COEF)
                    
                    ligne(ctx, self.posZElevesH[0]+self.tailleZElevesH[0], self.yEleves[i],
                          self.posZComp[0]+self.tailleZComp[0], self.yEleves[i],
                          self.CoulAltern[i][0][:-1])
                
                #
                # Lignes verticales
                #
                for i, e in enumerate(self.prj.eleves + self.prj.groupes):
                    ctx.set_line_width(0.003 * COEF)
                    ligne(ctx, self.xEleves[i], self.yEleves[i],
                          self.xEleves[i], self.posZTaches[1] + self.tailleZTaches[1] + (i % 2)*(self.ecartY/2) + self.ecartY/2,
                          self.CoulAltern[i][0][:-1])
                    
                    self.drawCroisementsElevesCompetences(e, self.yEleves[i])
                
                #
                # Ombres des lignes verticales
                #
                e = 0.003 * COEF
                ctx.set_line_width(0.003 * COEF)
                for i in range(len(self.prj.eleves + self.prj.groupes)) :
                    y = self.posZTaches[1] + self.tailleZTaches[1] + (i % 2)*(self.ecartY/2) + self.ecartY/2
                    ctx.set_source_rgb(1,1,1)
                    ctx.move_to(self.xEleves[i]+e, self.yEleves[i]+e)
                    ctx.line_to(self.xEleves[i]+e, y)
                    ctx.move_to(self.xEleves[i]-e, self.yEleves[i]+e)
                    ctx.line_to(self.xEleves[i]-e, y)
                ctx.stroke()
        
    #    print "élèves", time.time() - tps
        
        #
        #  Tâches
        #
        if not self.entete:
    #    tps = time.time()
            Curve_rect_titre(self,
                             (self.posZDeroul[0], self.posZDeroul[1], 
                              self.tailleZDeroul[0], self.tailleZDeroul[1]),
                             "Tâches à réaliser",  
                             self.Bcoul_ZDeroul, self.Icoul_ZDeroul, self.fontZDeroul).draw()
            
            y = self.posZTaches[1] - self.ecartTacheY
            
            # Les positions en Y haut et bas des phases
            yh_phase = {'Sup' : [[], []], 
                        'Ana' : [[], []],
                        'Con' : [[], []], 
                        'DCo' : [[], []],
                        'Rea' : [[], []], 
                        'Val' : [[], []],
                        'XXX' : [[], []]}
        
            phase = None
            y1 = y2 = y3 = 0   # juste pour éviter une erreur en cas d'echec d'ouverture.
            for t in self.prj.taches:
                if t.phase == "R1":
                    y1 = y
                elif t.phase == "R2":
                    y2 = y
                elif t.phase == "R3":
                    y3 = y
                    
                if phase != t.phase:
                    y += self.ecartTacheY
        
                if t.phase != '':  
                    yb = self.drawTacheRacine(t, y)
                    if t.phase in ["Ana", "Con", "DCo", "Rea", "Val", 'XXX'] :
                        yh_phase[t.phase][0].append(y)
                        yh_phase[t.phase][1].append(yb)
                    y = yb
                    
                if y3 == 0 and t == self.prj.taches[-1]:
                    y3 = y
    
                phase = t.phase
        #    print "    ", time.time() - tps
            #
            # Les lignes horizontales en face des taches
            # et les croisements Tâche/Competences
            #
            x = self.posZTaches[0] + self.tailleZTaches[0]
            for t, y in self.yTaches: 
                if not t.phase in ["R1", "R2", "R3", "S", "Rev"]:
                    self.drawLigne(x, y)
                if (t.phase in ["R1", "R2", "R3", "S"] and t.DiffereSuivantEleve()) or t.estPredeterminee():
                    dy = self.hRevue
                    y = y - ((len(self.prj.eleves + self.prj.groupes)-1)*dy)/2
        #            print "phase = ", t.phase
                    h = 0.006 * COEF
                    for eleve in self.prj.eleves + self.prj.groupes:
                        self.drawCroisementsCompetencesRevue(t, eleve, y, h)
                        y += dy
                else:
                    self.drawCroisementsCompetencesTaches(t, y)
            
            # Nom des phases
            for phase, yh in yh_phase.items():
        #        print phase, yh
                if len(yh[0]) > 0:
                    yh[0] = min(yh[0])
                    yh[1] = max(yh[1])
                    ctx.set_source_rgb(*self.BCoulTache[phase][:3])
                    ctx.select_font_face (self.font_family, cairo.FONT_SLANT_ITALIC,
                                                        cairo.FONT_WEIGHT_NORMAL)
                    if self.wPhases > yh[1]-yh[0]:
                        orient = "h"
                    else:
                        orient = "v"
                    
                    if prjeval is None:
                        n = ""
                    else:
                        try:
                            n = prjeval.phases[phase][1]
                        except KeyError:
                            n = ""
                    show_text_rect(ctx, n, 
                                   (self.posZDeroul[0] + self.ecartX/6, yh[0], 
                                    self.wPhases, yh[1]-yh[0]), 
                                   ha = 'c', orient = orient, b = 0.01, le = 0.7,
                                   couper = False) 
                    
        #            show_text_rect(ctx, constantes.NOM_PHASE_TACHE[prj.GetTypeEnseignement(True)][phase], 
        #                           (posZDeroul[0] + ecartX/6, yh[0], 
        #                            wPhases, yh[1]-yh[0]), 
        #                           ha = 'c', orient = orient, b = 0,
        #                           couper = False) 
        
        #    print "taches", time.time() - tps
        
        #
        # Durées élève entre revues (uniquement en période "terminale")
        #
        if not self.entete and prjeval is not None:
        #    tps = time.time()
            posEpreuve = prjeval.getPeriodeEval()
            if posEpreuve is not None and self.prj.position == posEpreuve:
                y0 = self.posZTaches[1]
                y4 = y1+len(self.prj.eleves + self.prj.groupes) * self.hRevue + 2*self.ecartTacheY
        #        y4 = y1+2*ecartTacheY + 0.015
        #        y5 = y2+2*ecartTacheY + 0.015
                y5 = y2+len(self.prj.eleves + self.prj.groupes) * self.hRevue + 2*self.ecartTacheY
    #            print y0, y1, y2, y3, y4, y5
                md1 = md2 = md3 = 0
                for i, e in enumerate(self.prj.eleves + self.prj.groupes):
                    md1 = max(e.GetDuree(phase = "R1"), md1)
                    md2 = max(e.GetDuree(phase = "R2"), md2)
                    md3 = max(e.GetDuree(phase = "R3"), md3)
                    
                for i, e in enumerate(self.prj.eleves + self.prj.groupes):
                    d1 = e.GetDuree(phase = "R1")
                    d2 = e.GetDuree(phase = "R2")
                    d3 = e.GetDuree(phase = "R3")
                    ctx.set_source_rgba(*self.CoulAltern[i][0])
                    ctx.set_line_width(0.005 * COEF)
                    if md1 > 0:
                        ctx.move_to(self.xEleves[i], y0)
                        ctx.line_to(self.xEleves[i], y0+(y1-y0)*d1/md1)
                        ctx.stroke()
                    if md2 > 0:
                        ctx.move_to(self.xEleves[i], y4)
                        ctx.line_to(self.xEleves[i], y4+(y2-y4)*d2/md2)
                        ctx.stroke()
                    if md3 > 0:
                        ctx.move_to(self.xEleves[i], y5)
                        ctx.line_to(self.xEleves[i], y5+(y3-y5)*d3/md3)
                        ctx.stroke()
        
    #    print "durées", time.time() - tps
        
        
        
        #
        # Croisements élèves/tâches
        #
        if not self.entete :
    #    tps = time.time()
            for t, y in self.yTaches: 
                self.drawCroisementsElevesTaches(t, y)
                
        #    print "CroisementsElevesTaches", time.time() - tps
            
            #
            # Durées du projet (durées élèves)
            #
        #    tps = time.time()
            for i, e in enumerate(self.prj.eleves + self.prj.groupes):
        #        x = posZElevesV[0]+i*tailleZElevesV[0]/len(prj.eleves)-wEleves/2
                x = self.xEleves[i]-self.wEleves*3/4
                y = self.posZTaches[1] + self.tailleZTaches[1] + (i % 2)*(self.ecartY/2)+self.ecartY/2
                d = e.GetDuree()
                if prjeval is None:
                    taux = 100
                else:
                    dureeRef = prjeval.duree
                    taux = abs((d-dureeRef)/dureeRef)*100
        #        print "   duree", d, "/", dureeRef
        #        print "   taux", taux
                if taux < constantes.DELTA_DUREE:
                    ctx.set_source_rgb(0.1,1,0.1)
                elif taux < constantes.DELTA_DUREE2:
                    ctx.set_source_rgb(1,0.6,0.1)
                else:
                    ctx.set_source_rgb(1,0.1,0.1)
                show_text_rect(ctx, getHoraireTxt(d), 
                               (x, y, self.wEleves*3/2, self.ecartY/2), ha = 'c', b = 0)
            
    #    print "dureeProjet", time.time() - tps
        #
        # Informations
        #
        if not self.entete:
            self.info(ctx)
        
        
        if self.surRect is not None:
    #         print("Surbrillance")
            if type(self.surRect) == list:
                for r in self.surRect:
        #             print("   ", r)
                    self.surbrillance(r)
            elif hasattr(self.surRect, 'rect'):
                for r in self.surRect.rect:
        #             print("   ", r)
                    self.surbrillance(r)
        
# 
#     ######################################################################################  
#     def drawLigneEff(x, y):
#         dashes = [ 0.010 * COEF,   # ink
#                    0.002 * COEF,   # skip
#                    0.005 * COEF,   # ink
#                    0.002 * COEF,   # skip
#                    ]
#         
#         ctx.set_line_width (0.001 * COEF)
#         ctx.set_dash(dashes, 0)
#         ligne(ctx, x, posZElevesV[1] + tailleZElevesV[1],
#               x, y, (0.6, 0.8, 0.6))
#         ctx.set_dash([], 0)

    


    
    ######################################################################################  
    def drawTacheRacine(self, tache, y):
        global yTaches
        
        h = self.calcH_tache(tache)
        
        #
        # Flèche verticale indiquant la durée de la tâche
        #
        if not tache.phase in ["R1", "R2", "R3", "S", "Rev"]:
    #        fleche_verticale(ctx, posZTaches[0] - wDuree/2 - ecartX/4, y, 
    #                         h, wDuree, (0.9,0.8,0.8,0.5))
            
            self.ctx.set_source_rgba (0.9,0.8,0.8,0.5)
            x = self.posZTaches[0] - self.wDuree - self.ecartX/4
            self.ctx.rectangle(x, y, self.wDuree, h)
            self.ctx.fill_preserve ()    
            self.ctx.set_source_rgba(0.4,  0.4,  0.4,  1)
            self.ctx.set_line_width(0.0006 * COEF)
            self.ctx.stroke ()
            
            self.ctx.set_source_rgb(0.5,0.8,0.8)
            self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_BOLD)
            
            if h > self.wDuree:
                show_text_rect(self.ctx, getHoraireTxt(tache.GetDuree()), 
                           (x, y, self.wDuree, h), 
                           orient = 'v', b = 0.01)
            else:
                show_text_rect(self.ctx, getHoraireTxt(tache.GetDuree()), 
                           (x, y, self.wDuree, h), 
                           orient = 'h', b = 0.01)
        
        #
        # Indication du délai pour revue
        #
        elif tache.phase in ["R1", "R2", "R3", "Rev"]:
            self.ctx.set_source_rgba (0.9,0.8,0.8,0.5)
            if tache.phase == "Rev":
                x = self.posZTaches[0] - self.wDuree - self.ecartX/4
                w = self.wDuree*3
            else:
                x = self.posZTaches[0] - self.wDuree*4 - self.ecartX/4
                w = self.wDuree*3
            self.ctx.rectangle(x, y, w, h)
            self.ctx.fill_preserve ()    
            self.ctx.set_source_rgba(0.4,  0.4,  0.4,  1)
            self.ctx.set_line_width(0.0006 * COEF)
            self.ctx.stroke ()
            
            self.ctx.set_source_rgb(0.5,0.8,0.8)
            self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_BOLD)
            show_text_rect(self.ctx, getHoraireTxt(tache.GetDelai(), constantes.CHAR_FLECHE), 
                           (x, y, w, h), 
                           orient = 'h', 
                           fontsizeMinMax = (minFont, 0.015 * COEF), 
                           b = 0.01, couper = False)
        
    
        
        #
        # Rectangles actifs et points caractéristiques : initialisation
        #
        tache.pts_caract = []
        
        
        
        #
        # Tracé du cadre de la tâche
        #
        if tache.phase == "Rev":
            x = self.posZTaches[0] + self.wDuree*2
            w = self.posZComp[0] + self.tailleZComp[0] + self.ecartX/4 - x
        elif not tache.phase in ["R1", "R2", "R3", "S"]:
            x = self.posZTaches[0]
            w = self.tailleZTaches[0]
        else:
            x = self.posZTaches[0] - self.wDuree/2 - self.ecartX/4
            w = self.posZComp[0] + self.tailleZComp[0] + self.ecartX/4 - x
    
        tache.pts_caract.append((x, y))
            
        self.ctx.set_line_width(0.002 * COEF)
        Rectangle_plein(self, (x, y, w, h), 
                        self.BCoulTache[tache.phase], 
                        self.ICoulTache[tache.phase], 
                        self.ICoulTache[tache.phase][3]).draw()
        
        
        #
        # Affichage du code de la tâche
        #
        if hasattr(tache, 'code'):
            self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
            self.ctx.set_source_rgb (0,0,0)
            
            if not tache.phase in ["R1", "R2", "R3", "S"]:
                t = tache.code
                hc = max(self.hTacheMini/2, 0.01 * COEF)
            else:
                t = tache.intitule
                hc = h
            show_text_rect(self.ctx, t, (x, y, self.tailleZTaches[0], hc), ha = 'g', 
                           wrap = False, 
                           fontsizeMinMax = (minFont, 0.02 * COEF), b = 0.02)
        
        
        #
        # Affichage de l'intitulé de la tâche
        #
        if tache.intituleDansDeroul and tache.intitule != "" and not tache.phase in ["R1", "R2", "R3", "S"]:
            self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_ITALIC,
                                  cairo.FONT_WEIGHT_NORMAL)
            self.ctx.set_source_rgb (0,0,0)
            
            # Si on ne peut pas afficher l'intitulé dessous, on le met à coté
            if h-hc < minFont:
                width = self.ctx.text_extents(t)[2]*1.2
                rect = (x + width, y, self.tailleZTaches[0] - width, hc)
            else:
                rect = (x, y + hc, self.tailleZTaches[0], h-hc)
            if rect[2] > 0:
                show_text_rect(self.ctx, tache.GetIntit(), rect, 
                               ha = 'g', 
                               fontsizeMinMax = (minFont, 0.015 * COEF))
            
        tache.GetDocument().zones_sens.append(Zone_sens([(x, y, self.tailleZTaches[0], h)], obj = tache))
    #    tache.rect.append([x, y, tailleZTaches[0], h])
            
            
        #
        # Tracé des croisements "Tâches" et "Eleves"
        #
        self.yTaches.append([tache, y+h/2])
    #    DrawCroisementsCompetencesTaches(ctx, tache, y + h/2)
        
        
        #
        # Icone de la tâche
        #
        bmp = tache.icone
        if bmp != None:
            d = min(self.hTacheMini * 3, h)
            Image(self, (x+w-d, y, d, d), bmp).draw()
            
            
    #         ctx.save()
    #         tfname = tempfile.mktemp()
    #         try:
    #             bmp.SaveFile(tfname, wx.BITMAP_TYPE_PNG)
    #             image = cairo.ImageSurface.create_from_png(tfname)
    #         finally:
    #             if os.path.exists(tfname):
    #                 os.remove(tfname)  
    #                 
    #         wi = image.get_width()*1.1
    #         hi = image.get_height()*1.1
    #         
    #         d = min(hTacheMini * 3, h)
    #         s = min(d/wi, d/hi)
    #         ctx.translate(x+w-d, y)
    #         ctx.scale(s, s)
    #         ctx.set_source_surface(image, 0, 0)
    #         ctx.paint()
    #         ctx.restore()
        
        y += h
        return y
            
            
            
    ######################################################################################  
    def drawLigne(self, x, y, gras = False):
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
    def drawCroisementsCompetencesTaches(self, tache, y):
        self.drawBoutonCompetence(tache, 
                                  self.regrouperDic(tache, tache.GetDicIndicateurs()), y)
        
    
    ######################################################################################  
    def drawCroisementsCompetencesRevue(self, revue, eleve, y, h):
    #    print "DrawCroisementsCompetencesRevue", eleve, revue.phase
    #    print "   ", revue.GetDicIndicateursEleve(eleve)
        self.drawBoutonCompetence(revue, 
                                  self.regrouperDic(revue, revue.GetDicIndicateursEleve(eleve)), y, h)
    
    
    
    ######################################################################################  
    def drawCroisementsElevesCompetences(self, eleve, y):
        #
        # Boutons
        #
        self.drawBoutonCompetence(eleve, 
                                  self.regrouperDic(eleve, eleve.GetDicIndicateurs()), y)
    
    
    
    #####################################################################################  
    def drawCroisementsElevesTaches(self, tache, y):
        """ Dessine les "boules"
        
        """ 
    #     print "DrawCroisementsElevesTaches", tache
    #     print tache.eleves
    #     print 
        
        #
        # Croisements Tâche/Eleves
        #
        if tache.phase in ["R1", "R2", "R3", "S"]:
            differeSuivantEleve = tache.DiffereSuivantEleve()
        else:
            differeSuivantEleve = tache.estPredeterminee()
            
    #    if tache.phase in ["R1", "R2", "R3", "S"] and differeSuivantEleve: 
        if differeSuivantEleve: 
            lstElv = list(range(len(tache.projet.eleves + tache.projet.groupes)))
            lstImp = [100]*len(lstElv)
        else:
            lstElv = tache.eleves
            lstImp = tache.impEleves
        
    #    if tache.phase in ["R1", "R2", "R3", "S"] and differeSuivantEleve:
        if differeSuivantEleve: 
            dy = self.hRevue
            y = y - ((len(tache.projet.eleves + tache.projet.groupes)-1)*dy)/2
            r = 0.005 * COEF
        else:
            dy = 0
            r = 0.006 * COEF
            
        for i, e in enumerate(lstElv):
    #         print "   ",i, e
    #        if tache.phase in ["R1", "R2", "R3", "S"] and differeSuivantEleve:
            if differeSuivantEleve: 
                color1 = self.BCoulTache[tache.phase]
                color0 = (1, 1, 1, 1)
            else:
                color0 = self.CoulAltern[e][0]
                color1 = self.CoulAltern[e][1]
    
            if e > len(self.xEleves)-1:
                break
            
            _x = self.xEleves[e]
    
            Boule(self, _x, y, r, lstImp[i], 
                  color0 = color0, color1 = color1,
                  transparent = False).draw()
    
            eleves_groupes = tache.projet.eleves + tache.projet.groupes
            tache.GetDocument().zones_sens.append(Zone_sens([(_x -r , y - r, 2*r, 2*r)], 
                                                       obj = [eleves_groupes[i], tache]))
            
    #        tache.projet.eleves[i].rect.append((_x -r , y - r, 2*r, 2*r))
            eleves_groupes[i].pts_caract.append((_x,y))
            y += dy
            
    
    
        
    
        
    ######################################################################################  
    def drawBoutonCompetence(self, objet, dicIndic, y, h = None):
        """ Dessine les petits rectangles des indicateurs (en couleurs R et S)
             ... avec un petit décalage vertical pour que ce soit lisible en version N&B
        """
#         print("DrawBoutonCompetence", objet, dicIndic)
        if h == None: # Toujours sauf pour les revues
            r = self.wColComp/3
            h = 2*r
        
        # Un petit décalage pour distinguer R et S en N&B    
        dh = h/10
        self.ctx.set_line_width (0.0004 * COEF)
        dicIndic, dictype = dicIndic
        prjeval = objet.GetProjetRef()
        
        for s in dicIndic.keys():
            
    #         if s in dicIndic.keys():
            x = self.xComp[s]-self.wColComp/2
            
            rect = (x, y-h/2, self.wColComp, h)
            
            objet.GetDocument().zones_sens.append(Zone_sens([rect], obj = objet, param = s))
            
    #        if s in objet.GetDocument().rectComp.keys() and objet.GetDocument().rectComp[s] != None:
    #            objet.GetDocument().rectComp[s].append(rect)
    #        else:
    #            objet.GetDocument().rectComp[s] = [rect]
            
            objet.pts_caract.append((x,y))
            
            indic = dicIndic[s]
    #            dangle = 2*pi/len(indic)
            dx = self.wColComp/len(indic)
            for a, i in enumerate(indic):
                deja = False
                for part in prjeval.listeParties:
                    if part in dictype[s][a]:
                
#                 for part in dictype[s][a]:
#                     if part in prjeval.parties:
                        if i: # Rose ou bleu
                        
                            if part == prjeval.listeParties[0]:  # Conduite
                                d = -1
                            else:               # Soutenance
                                d = 1
                        
                            self.ctx.set_source_rgba (*self.getCoulComp(part))
                
                        else:
                            d = 0
                            self.ctx.set_source_rgba (1, 1, 1, 0)
                
                        if d != 0:      # Un rectangle coloré
                            if deja != 0:   # On a jéja mis un rectangle ici (position deja)
                                if deja:
                                    self.ctx.rectangle(x+a*dx, y, dx, h/2)
#                                 else:
#                                     self.ctx.rectangle(x+a*dx, y-h/2, dx, h/2-dh)
                                
                            else:
                                self.ctx.rectangle(x+a*dx, y-h/2+d*dh, dx, h-dh)
                                deja = True
                                
                            self.ctx.fill_preserve ()
                            
                        else:           # Juste deux traits verticaux
                            self.ctx.move_to(x+a*dx, y-h/2+dh)
                            self.ctx.rel_line_to(0, h-4*dh)
                            self.ctx.move_to(x+a*dx+dx, y-h/2+dh)
                            self.ctx.rel_line_to(0, h-4*dh)
                
                        self.ctx.set_source_rgba (0, 0 , 0, 1)
                        self.ctx.stroke()
                
                
                
                
                
#                 if i: # Rose ou bleu
#     #                 print "   ", s, a
#                     part = list(dictype[s][a].keys())[0]
#                     if part == 'S':
#     #                if dictype[s][a][1] != 0:   #objet.projet.classe.GetReferentiel().getTypeIndicateur(s+'_'+str(a+1)) == "C": # Conduite     #dicIndicateurs_prj[s][a][1]:
#                         d = -1
#                     else:
#                         d = 1
#                     self.ctx.set_source_rgba (*self.getCoulComp(part))
#                 else: # Rien => Transparent
#                     d = 0
#                     self.ctx.set_source_rgba (1, 1, 1, 0)
#                 
#     #                 print "d", d, (x+a*dx, y-h/2+d*dh, dx, h-dh)
#                 
#                 
#                 
#                 if d != 0:      # Un rectangle coloré
#                     self.ctx.rectangle(x+a*dx, y-h/2+d*dh, dx, h-dh)
#                     self.ctx.fill_preserve ()
#                     
#                 else:           # Juste deux trait verticaux
#                     self.ctx.move_to(x+a*dx, y-h/2+dh)
#                     self.ctx.rel_line_to(0, h-4*dh)
#                     self.ctx.move_to(x+a*dx+dx, y-h/2+dh)
#                     self.ctx.rel_line_to(0, h-4*dh)
    
                
#                 self.ctx.set_source_rgba (0, 0 , 0, 1)
#                 self.ctx.stroke()
    
    


###########################################################################################
# 
# 
#
###########################################################################################
def gabarit():
    
    print("Génération du gabarit ...", end=' ') 
    import draw_cairo_prj2
    imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  2100, 2970)#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
    ctx = cairo.Context(imagesurface)
    
    e = 29
    ctx.scale(e, e) 
    
    
#     print dir(draw_cairo_prj)
    pos = {}
    taille = {}
    for attr in dir(draw_cairo_prj2):
        if attr[:3] == 'pos':
            pos[attr[3:]] = attr
        if attr[:6] == 'taille':
            taille[attr[6:]] = attr
    
    print(pos, taille)
    
    ctx.set_line_width(5.0/e)
    
    for k, p in list(pos.items()):
        if k in list(taille.keys()):
            x, y = getattr(draw_cairo_prj2, p)
            w, h = getattr(draw_cairo_prj2, taille[k])
            
            try:
                ctx.rectangle(x, y, w, h)
                ctx.stroke()
                show_text_rect(ctx, k, (x, y, w, h), fontsizeMinMax = (-1, 30.0/e),
                               wrap = False, couper = False)
            except:
                pass
                print("   ", k, " : ", x, y, w, h)
    
    
    imagesurface.write_to_png('gabarit_prj.png')
       

# #######################################################################################
# # Gestion des paramètres sauvegardables
# #####################################################################################
# 
# def getParametres():
#     """ Renvoi un dict {nom: valeur} des paramètres à sauvegarder
#          - couleurs
#          - ...
#     """
#     return {n : CouleurFloat2CSS(v) for n, v in globals().items() if "coul_" in n}
# 
# 
# nom_module = os.path.splitext(os.path.basename(__file__))[0]
# nom_fichparam = "param_prj.cfg"
# 
# if __name__ == '__main__':
#     sauverParametres(getParametres().keys(), 
#                      nom_module, 
#                      nom_fichparam)
#     
#     
# ##########################################################################################
# chargerParametres(getParametres().keys(), 
#                   os.path.splitext(os.path.basename(__file__))[0], 
#                   os.path.join(util_path.PATH, nom_fichparam))


# if __name__ == "__main__":
#     gabarit()


