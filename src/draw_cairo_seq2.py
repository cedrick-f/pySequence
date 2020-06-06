#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               draw_cairo_seq                            ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2011-2020 Cédrick FAURY

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import cairo
# import cairocffi as cairo
from draw_cairo2 import *

from math import pi, cos, sin
from couleur import CouleurFloat2CSS, CouleurInt2Float

#import textwrap
#from math import sqrt, pi, cos, sin
#import cairo

import util_path
#import ConfigParser

from constantes import Effectifs,COUL_COMPETENCES, mergeDict
                        #getSavoir, getCompetence, \ NomsEffectifs, listeDemarches, Demarches, \
                        #DemarchesCourt, 
import constantes

# Les constantes partagées
from Referentiel import REFERENTIELS, ACTIVITES
import Referentiel


## Pour afficher des images
import os
import tempfile
import wx

from proprietes import *


_torad = pi/180


######################################################################################  
class Sequence(Base_Fiche_Doc):
    def __init__(self, seq, mouchard = False, entete = False, surRect = None):
        Base_Fiche_Doc.__init__(self)
        self.seq = seq
        self.mouchard = mouchard
        self.entete = entete
        self.surRect = surRect
        
        # Ecart pour les couches
        self.ecartC = self.ecartX/8
        
        ######################################################################################
        self.curseur = None
        
    
        # paramètres pour la fonction qui calcule la hauteur des tâches 
        # en fonction de leur durée
        self.a = self.b = None
        
        
        
        # CI
        self.p_siz_CI = (0.17 * COEF, 0.085 * COEF)
        #posCI = (posPre[0] + taillePre[0]+ecartX, 0.1)
        self.pos_CI = (self.margeX, self.margeY)
        self.p_Icol_CI = (0.9, 0.8, 0.8, 0.85)
        self.p_Bcol_CI = (0.3, 0.2, 0.25, 1)
        self.p_font_CI = 0.014 * COEF
        
        # Rectangle des prerequis
        self.p_w_Pre = 0.28 * COEF
        self.p_h_Tet =  0.18 * COEF
        self.h_Pre = None
#         self.siz_Pre = (0.28 * COEF, 0.18 * COEF - self.p_siz_CI[1] - self.ecartY)
        self.pos_Pre = (None, None)
        self.p_Icol_Pre = (0.8, 0.8, 0.9, 0.85)
        self.p_Bcol_Pre = (0.2, 0.25, 0.3, 1)
        self.p_font_Pre = 0.014 * COEF
        
        # Position dans l'année
        self.pos_Pos = [None, self.margeY - self.ecartY/2]
        self.p_h_Pos = 0.04 * COEF
        self.w_Pos = None

        
        # Rectangle des objectifs
        self.pos_Obj = (None, None)
        self.siz_Obj = [None, None]
        self.p_Icol_Obj = (0.8, 0.9, 0.8, 0.85)
        self.p_Bcol_Obj = (0.25, 0.3, 0.2, 1)
        self.p_font_Obj = 0.014 * COEF
        
        # Cible
        self.pos_Cib = [None, None]
        self.siz_Cib = [None, None]
        self.p_Icol_Cib = (0.8, 0.8, 1, 0.85)
        self.p_Bcol_Cib = (0.1, 0.1, 0.25, 1)
        self.ctr_Cib = (None, None)
        
        # Zone de commentaire
        self.p_font_Com = 0.01* COEF
        self.pos_Com = [self.margeX, None]
        self.siz_Com = [self.LargeurTotale-2*self.margeX, None]
        self.intComm = []
        
        # Zone d'organisation de la séquence (intérieur du grand cadre vert - bordure)
        self.p_mrg_Org = 0.01 * COEF
        self.x_Org = None
        self.p_y_Org = 0.24 * COEF
#         self.pos_Org = (self.margeX+self.p_mrg_Org, 0.24 * COEF)
        self.siz_Org = [None, None]
        
        
        # # Rectangle de l'intitulé
        # tailleIntitule = [0.4 * COEF, 0.04 * COEF]
        # posIntitule = [(LargeurTotale-tailleIntitule[0])/2, posZOrganis[1]-tailleIntitule[1]]
        self.p_Icol_Int = (0.98, 0.99, 0.98, 0.8)
        self.p_Bcol_Int = (0.2, 0.8, 0.2, 1)
        self.p_font_Int = 0.02 * COEF
        
        # Zone de découpage de la classe
        self.p_h_Cls = 0.06 * COEF
        
        # Zone de déroulement de la séquence
        self.pos_Der = (None, None)
        self.siz_Der = [None, None]
        
        
        # Zone du tableau des Systèmes
        self.pos_Sys = [None, None]
        self.siz_Sys = [None, None]
        self.p_wCol_Sys = 0.025 * COEF
        self.xSystemes = {}
        
        # Zone du tableau des démarches
        self.pos_Dem = [None, None]
        self.p_w_Dem = 0.02 * COEF
        self.h_Dem = None
#         self.siz_Dem = [0.02 * COEF, None]
        # xDemarche = {"I" : None,
        #              "R" : None,
        #              "P" : None}
        
        # Zone des intitulés des séances
        self.p_font_ISea = 0.01 * COEF
        self.p_mrg_ISea = 0.06 * COEF
        self.pos_ISea = [None, None]
        self.siz_ISea = [None, None]
#         self.p_h_ISea = 0.02 * COEF
        self.intituleSeances = []
        
        # Zone des séances
        self.p_w_Dur = 0.02 * COEF
        self.pos_Sea = (None, None)
        self.siz_Sea = [None, None]
        # wEff =  {"C" : None,
        #          "G" : None,
        #          "D" : None,
        #          "E" : None,
        #          "P" : None,
        #          "I" : None
        #          }
        #hHoraire = None
        self.ey_Sea = None
        self.p_Bcol_Sea_ = {"ED" : (0.3,0.5,0.5), 
                           "AP" : (0.5,0.3,0.5), 
                           "P"  : (0.5,0.5,0.3), 
                           "EPI" : (0.5,0.5,0.3), 
                           "C"  : (0.3,0.3,0.7), 
                           "TD" : (0.3,0.5,0.7),
                           "SA" : (0.3,0.7,0.3), 
                           "SS" : (0.4,0.5,0.4), 
                           "E"  : (0.7,0.3,0.3), 
                           "R"  : (0.45,0.35,0.45), 
                           "S"  : (0.45,0.45,0.35),
                           "HC": (0.51,0.29,0.24),
                           "DM": (0.51,0.29,0.24),
                           "ST" : (0.12,0.29,0.53)}
        
        self.p_Icol_Sea_ = {"ED" : (0.6, 0.8, 0.8), 
                           "AP" : (0.8, 0.6, 0.8), 
                           "P"  : (0.8, 0.8, 0.6), 
                           "EPI"  : (0.8, 0.8, 0.6), 
                           "C"  : (0.6, 0.6, 1.0),
                           "TD" : (0.6,0.8,1.0),
                           "SA" : (0.6, 1.0, 0.6), 
                           "SS" : (0.7, 0.8, 0.7), 
                           "E"  : (1.0, 0.6, 0.6), 
                           "R"  : (0.75, 0.65, 0.75), 
                           "S"  : (0.75, 0.75, 0.65),
                           ""   : (1.0, 1.0, 1.0),
                           "HC": (0.86,0.49,0.41),
                           "DM": (0.86,0.49,0.41),
                           "ST" : (0.21,0.49,0.54)}
        
        self.Bstyl_Sea = {"ED" : [], 
                           "AP" : [], 
                           "P"  : [], 
                           "EPI"  : [], 
                           "C"  : [],
                           "TD" : [],
                           "SA" : [], 
                           "SS" : [], 
                           "E"  : [], 
                           "R"  : [], 
                           "S"  : [],
                           ""   : [],
                           "HC": [0.01 * COEF, 0.005 * COEF],
                           "DM": [0.01 * COEF, 0.005 * COEF],
                           "ST" : [0.01 * COEF, 0.005 * COEF]}



        
    #####################################################################################
    def getDocument(self):
        return self.seq
        
        
    ######################################################################################  
    def getGroupes(self):
        doc = self.getDocument()
        if doc is None:
            return {}
        ref = doc.GetReferentiel()
        
        return {"CI" : ref._nomCI.Plur_(),
                "Pre" : "Prérequis",
                "Obj" : "Objectifs",
                "Cib" : "Cible MEI",
                "ISea" : f"Intitulés des {ref._nomSeances.plur_()}",
                "Sys" : ref._nomSystemes.Plur_(),
                "Sea" : ref._nomSeances.Plur_(),
                "Com" : "Commentaires",
                "Int" : "Intitulé de la séquence",
                "Dur" : "Durée de la séquence",
                "Org" : "Zone d'organisation de la séquence",
                }
    
    
    ######################################################################################  
    def getSSGroupes(self):
        doc = self.getDocument()
        if doc is None:
            return {}
        
        ref = doc.GetReferentiel()
        
        sg = {}
        for c, s in ref.seances.items():
            sg[c] = s[0]
        
        return sg
    
    
    ######################################################################################  
    def calcH(self, t):
        return self.a*t+self.b
    
    
    ######################################################################################  
    def repartir(self, lst, mini):
        """ Réparti n valeurs proportionnellement 
            en assurant une valeur mini
            mais en gardant les zé&ros
        """
        lst_base = []
        for v in lst:
            if v > 0:
                lst_base.append(True)
            else:
                lst_base.append(False)
        
        # On enlève les 0
        lst_calc = [v for v in lst if v > 0]
        n = len(lst_calc)
        s = sum(lst_calc)
        assert s>0 and 1 > n*mini
        a = (1-n*mini)/s
        lst_calc = [a*v+mini for v in lst_calc]
        
        # on les remet
        L = []
        i = 0
        for ok in lst_base:
            if ok:
                L.append(lst_calc[i])
                i += 1
            else:
                L.append(0)
        
        return L


    ######################################################################################  
    def DefinirZones(self, ctx):
        """ Calcule les positions et dimensions des différentes zones de tracé
            en fonction du nombre d'éléments (séances, systèmes)
        """
#         global a, b , ecartSeanceY, intituleSeances, fontIntSeances, fontIntComm, intComm
#         ref = self.seq.GetReferentiel()
        
        
        
        self.h_Pre = self.p_h_Tet - self.p_siz_CI[1] - self.ecartY
        self.pos_Pre = (self.margeX, self.pos_CI[1] + self.p_siz_CI[1] + self.ecartY)
        self.pos_Obj = (self.pos_Pre[0] + self.p_w_Pre + self.ecartX/2, self.margeY + self.p_h_Pos + self.ecartY/2)
        self.siz_Obj = [self.LargeurTotale - self.margeX - self.pos_Obj[0], self.pos_Pre[1] + self.h_Pre - self.pos_Obj[1]]
        
        self.pos_Cib = [self.pos_CI[0] + self.p_siz_CI[0] + self.ecartX/4, self.margeY - self.ecartY/2]
        self.siz_Cib = [self.pos_Obj[0] - self.pos_CI[0] - self.p_siz_CI[0] - self.ecartX/2, None]
        self.siz_Cib[1] = self.siz_Cib[0]
        self.ctr_Cib = (self.pos_Cib[0] + self.siz_Cib[0] / 2 + 0.0006 * COEF, 
                     self.pos_Cib[1] + self.siz_Cib[1] / 2 - 0.0015 * COEF)
        
        self.x_Org = self.margeX+self.p_mrg_Org
        self.siz_Org = [self.LargeurTotale-2*(self.margeX+self.p_mrg_Org), None]
        
        self.pos_Der = (self.margeX+self.ecartX/2, self.p_y_Org+self.p_h_Cls)
        
        self.pos_Sys = [None, self.p_y_Org + self.p_mrg_Org]
        
        self.pos_Dem = [None, self.pos_Sys[1]]
        
        self.pos_ISea = [self.p_mrg_ISea, None]
        self.siz_ISea = [self.LargeurTotale-self.p_mrg_ISea*2, None]
        
        self.pos_Sea = (self.pos_Der[0] + self.p_w_Dur, self.p_y_Org+0.08 * COEF)
        
        
        #hHoraire
        # Zone de commentaire
        if self.seq.commentaires == "":
            self.siz_Com[1] = 0
        else:
            self.siz_Com[1], self.intComm = calc_h_texte(ctx, "Commentaires : " + self.seq.commentaires, 
                                                            self.siz_Com[0], self.p_font_Com)
    
        self.pos_Com[1] = 1 * COEF - self.siz_Com[1] - self.margeY
        
        # Zone d'organisation de la séquence (grand cadre)
        self.siz_Org[1] = self.pos_Com[1]-self.p_y_Org-self.p_mrg_Org
    
    #     # Rectangle de l'intitulé
    #     posIntitule[1] = posZOrganis[1]-tailleIntitule[1]
    
        # Zone des intitulés des séances
    #    print "Zone des intitulés des séances"
        #                  titres    contenus    hauteurs de ligne
        self.intituleSeances = [[],      [],         []]
        self.siz_ISea[1] = 0
        
        self.intituleSeances[0], lstInt = self.seq.GetIntituleSeances()
        for intS in lstInt:
            h, t = calc_h_texte(ctx, intS, self.siz_ISea[0], self.p_font_ISea)
            self.intituleSeances[2].append(h)
            self.intituleSeances[1].append(t)
    #        intituleSeances.append([intS[0],h,t])
            self.siz_ISea[1] += h
        
    
    #    tailleZIntSeances[1] = len(seq.GetIntituleSeances()[0])* hIntSeance
        self.pos_ISea[1] = self.p_y_Org + self.siz_Org[1] - self.siz_ISea[1]
        
        # Zone du tableau des Systèmes
        systemes = self.seq.GetSystemesUtilises(niveau = 0)
        self.siz_Sys[0] = self.p_wCol_Sys * len(systemes)
        self.siz_Sys[1] = self.siz_Org[1] - self.ecartY - self.siz_ISea[1]
        self.pos_Sys[0] = self.x_Org + self.siz_Org[0] - self.siz_Sys[0]
        for i, s in enumerate(systemes):
            self.xSystemes[s.nom] = self.pos_Sys[0] + (i+0.5) * self.p_wCol_Sys
        
        
        # Zone du tableau des démarches
        if len(self.seq.classe.GetReferentiel().listeDemarches) > 0 and self.seq.HasDemarches():
            self.p_w_Dem = 0.02 * COEF
            self.pos_Dem[0] = self.pos_Sys[0] - self.p_w_Dem - self.ecartX/2
            self.h_Dem = self.siz_Sys[1]
    #         xDemarche["I"] = posZDemarche[0] + tailleZDemarche[0]/6
    #         xDemarche["R"] = posZDemarche[0] + tailleZDemarche[0]*3/6
    #         xDemarche["P"] = posZDemarche[0] + tailleZDemarche[0]*5/6
        else:
            self.p_w_Dem = 0
            self.h_Dem = self.siz_Sys[1]
            self.pos_Dem[0] = self.pos_Sys[0] - self.p_w_Dem - self.ecartX/2
                     
        # Zone de déroulement de la séquence
        self.siz_Der[0] = self.pos_Dem[0] - self.pos_Der[0] - self.ecartX/2
        self.siz_Der[1] = self.siz_Org[1] - self.pos_Der[1] + self.p_y_Org - self.ecartY/2
        
        
        # Zone des séances
        self.siz_Sea[0] = self.siz_Der[0] - self.ecartX# - largeFlecheDuree - ecartX - bordureZOrganis#0.05 # écart pour les durées
        self.siz_Sea[1] = self.siz_Sys[1] - self.pos_Sea[1] + self.pos_Der[1] - 0.05 * COEF
    #     wEff = {"C" : tailleZSeances[0],
    #              "G" : tailleZSeances[0]*6/7,
    #              "D" : tailleZSeances[0]*3/7,
    #              "S" : tailleZSeances[0]/seq.classe.nbrGroupes['E']*6/7,
    #              "E" : tailleZSeances[0]/seq.classe.nbrGroupes['E']*6/7,
    #              "P" : tailleZSeances[0]/seq.classe.nbrGroupes['P']*6/7,
    #              "I" : tailleZSeances[0]
    # #             "E" : tailleZSeances[0]*Effectifs["E"][1]/Effectifs["G"][1]*6/7,
    # #             "P" : tailleZSeances[0]*Effectifs["P"][1]/Effectifs["G"][1]*6/7,
    #              }
        
    #     wEff = {"C" : tailleZSeances[0],
    #             "I" : tailleZSeances[0]}
    #     for k in 'GDSEP':
    #         if len(ref.effectifs[k]) >= 6 and ref.effectifs[k][5] == "O":
    #             wEff[k] = tailleZSeances[0] * seq.classe.GetEffectifNorm(k) * seq.classe.nbrGroupes[ref.effectifs[k][4]]
    #         else:
    #             wEff[k] = tailleZSeances[0] * seq.classe.GetEffectifNorm(k)# * seq.classe.nbrGroupes[ref.effectifs[k][4]]
                
        
    #     for k in 'GDSEP':
    #         if len(ref.effectifs[k]) >= 6 and ref.effectifs[k][5] == "O":
    #             wEff[k] = tailleZSeances[0] * seq.classe.GetEffectifNorm(ref.effectifs[k][4]) * 0.9
    #         else:
    #             wEff[k] = tailleZSeances[0] * seq.classe.GetEffectifNorm(k) * seq.classe.nbrGroupes[ref.effectifs[k][4]]
                
    #    print "durées :"
        self.ey_Sea = 0.006 * COEF    # écart mini entre deux séances
        hmin = 0.016   * COEF           # hauteur minimum d'une séance
        tmin = self.seq.GetDureeGraphMini() # durée minimale de séance
        n = len(self.seq.seances)
        d = self.seq.GetDureeGraph()- n*tmin
    #    print "   ", seq.GetDureeGraphMini()
        
        if d == 0:
            self.a = 0
            self.b = (self.siz_Sea[1] - self.ey_Sea*(n-1)) / n
        else:
            self.a = (self.siz_Sea[1] - self.ey_Sea*(n-1) - n*hmin) / d
            if self.a < 0:
                self.a = 0
                self.b = (self.siz_Sea[1] - self.ey_Sea*(n-1)) / n
            else:
                self.b = hmin - self.a * tmin
                if self.b < 0:
                    self.a = (self.siz_Sea[1] - (n-1)*self.ey_Sea) / self.seq.GetDureeGraph()
                    self.b = 0
    
    
    ######################################################################################  
    def InitCurseur(self):
    #    curseur = [posZSeances[0], posZSeances[1]]
#         print("InitCurseur", self.pos_Sea)
        self.cursY = self.pos_Sea[1]


    ######################################################################################  
    def draw(self, ctx, surRect = None, surObj = None):
        """ Dessine une fiche de séquence de la séquence <seq>
            dans un contexte cairo <ctx>
            
            surRect : élément en surbrilance (rectangle ou objet)
            
        """
        self.surRect = surRect
        self.ctx = ctx
    #    print "Draw séquence"
        
        

        #
        # Options générales
        #
        self.initOptions(ctx)
        
        self.DefinirZones(ctx)
        self.InitCurseur()
#         self.definirCouleurs()

        
    #     gabarit() # génération du gabarit de test
    
        #
        #    pour stocker des zones caractéristiques (à cliquer, ...)
        #
        
        # Zones sensibles, depuis pySéquence
        self.seq.zones_sens = [] 
        # Points caractéristiques des rectangles (avec code)
        self.seq.pt_caract = [] 
        # Points caractéristiques des rectangles (sans code)
        self.seq.pts_caract = [] 
        
        
        #
        # Flèche
        #
        rayon = 0.30 * COEF
        alpha0 = 55
        alpha1 = 155
        y = self.pos_Obj[1]+self.siz_Obj[1] - rayon*sin(alpha0*_torad)
        Fleche_ronde(self, self.LargeurTotale/2, y, rayon, alpha0, alpha1, 
                     0.035 * COEF, 0.06 * COEF, (0.8, 0.9, 0.8, 1)).draw()
        
        
        #
        # Cadre et Intitulé de la séquence
        #
        if not self.entete:
            rect = (self.x_Org-self.p_mrg_Org, self.p_y_Org, 
                    self.siz_Org[0]+self.p_mrg_Org*2, self.siz_Org[1]+self.p_mrg_Org)
            self.seq.zones_sens.append(Zone_sens([rect], obj = self.seq))
            if len(self.seq.intitule) == 0:
                t = "Séquence sans nom"
            else:
                t = self.seq.intitule
            pt = Curve_rect_titre(self, rect, t,  
                                  self.p_Bcol_Int, 
                                  self.p_Icol_Int, 
                                  self.p_font_Int).draw()
            self.seq.pt_caract.append((pt, "Seq"))
    
    
        #####################################################################################
        # Domaines
        #
        self.DrawDomaines((self.pos_Sea[0] + self.x_Org-self.p_mrg_Org)/2,
                           self.p_y_Org + self.ecartY/2)
    
    
    
        #####################################################################################
        # Type d'enseignement
        #
        tailleTypeEns = self.siz_Obj[0]/2
        t = self.seq.classe.GetLabel()
        self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_BOLD)
        self.ctx.set_source_rgb (0.6, 0.6, 0.9)
        
        
        t2 = self.seq.classe.GetLabelComplet()
        coef = max(min(-0.003*len(t2)+0.9, 0.8), 0.45)
        h = self.p_h_Pos * coef #0.8
        show_text_rect(self.ctx, t, (self.pos_Obj[0] , self.pos_Pos[1], tailleTypeEns, h), 
                       va = 'c', ha = 'g', b = 0, orient = 'h', 
                       fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                       coulBord = (0, 0, 0))
    
        
    #     print("len=", len(t2))
        self.ctx.set_source_rgb (0.3, 0.3, 0.8)
        show_text_rect(self.ctx, t2, (self.pos_Obj[0] , self.pos_Pos[1] + h, tailleTypeEns, self.p_h_Pos - h), 
                       va = 'c', ha = 'g', b = 0, orient = 'h', 
                       fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False)
        
    
    
        #####################################################################################
        # Position dans l'année
        #
        self.pos_Pos[0] = self.pos_Pre[0] + self.p_w_Pre + self.ecartX + tailleTypeEns
        self.w_Pos =  self.LargeurTotale - self.pos_Pos[0] - self.margeX
        self.ctx.set_line_width (0.0015 * COEF)
        r = (*self.pos_Pos, self.w_Pos, self.p_h_Pos)
        
        rects = Periodes(self, r, self.seq.getRangePeriode(), 
                         self.seq.classe.referentiel.periodes).draw()
        
        
        self.seq.zones_sens.append(Zone_sens([r], param = "POS"))
        for i, re in enumerate(rects):
            self.seq.zones_sens.append(Zone_sens([re], param = "POS"+str(i)))
    
    
        #####################################################################################
        # Etablissement
        #
        if self.seq.classe.etablissement != "":
            t = self.seq.classe.etablissement + " (" + self.seq.classe.ville + ")"
            self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                              cairo.FONT_WEIGHT_NORMAL)
            show_text_rect(self.ctx, t, (self.pos_Pos[0] , self.pos_Pos[1]+self.p_h_Pos, 
                                         self.p_h_Pos, self.pos_Obj[1]-self.pos_Pos[1]-self.p_h_Pos), 
                           va = 'c', ha = 'g', b = 0.015, orient = 'h', 
                           fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                           coulBord = (0, 0, 0))
        
        
        #####################################################################################
        # Cible ou Logo
        #
        
        # Affichage du Logo
    #     print(seq.classe.referentiel.getLogo())
        rect = (*self.pos_Cib, *self.siz_Cib)
        Image(self, rect,
              self.seq.classe.referentiel.getLogo()).draw()
        self.seq.zones_sens.append(Zone_sens([rect], obj = self.seq))
        self.seq.pt_caract.append((self.pos_Cib, "Seq"))
              
        # Affichage des CI sur la cible
        if self.seq.classe.referentiel.CI_cible:
            self.seq.zones_sens.append(Zone_sens([self.pos_Cib+self.siz_Cib], obj = self.seq.CI))
#             self.seq.CI.rect = [self.pos_Cib+self.siz_Cib]
    
            rayons = {"F" : self.siz_Cib[0] * 0.28, 
                      "S" : self.siz_Cib[0] * 0.19, 
                      "C" : self.siz_Cib[0] * 0.1,
                      "_" : self.siz_Cib[0] * 0.45}
            angles = {"M" : 0,
                      "E" : 120,
                      "I" : -120,
                      "_" : -98}
    
            for i, _ in enumerate(self.seq.CI.GetCodesCIs()):
                mei, fsc = self.seq.CI.GetPosCible(i).split("_")
                mei = mei.replace(" ", "")
                fsc = fsc.replace(" ", "")
    
                # Rayon et angle
                if self.seq.classe.referentiel.champsInter: # un seul point
                    if len(fsc) == 0:
                        ray = 0
                    else:
                        ray = 0
                        for j in fsc:
                            ray += rayons[j]
                        ray = ray/len(fsc)
                    
                    if len(mei) == 0:
                        ray = rayons["_"]
                        ang = angles["_"]
                        angles["_"] = -angles["_"] # on inverse le coté pour pouvoir mettre 2 CI en orbite
                    elif len(mei) == 3:
                        ray = 0
                        ang = 0
                    elif len(mei) == 2:
                        ang = (angles[mei[1]] + angles[mei[0]])/2
                        if ang == 0:
                            ang = 180
                        
                    else:
                        ang = angles[mei[0]]
                            
                    pos = (self.ctr_Cib[0] + ray * sin(ang*_torad) ,
                           self.ctr_Cib[1] - ray * cos(ang*_torad))
        #             boule(ctx, pos[0], pos[1], 0.005 * COEF, 
        #                   color0 = (0.95, 1, 0.9, 1), color1 = (0.1, 0.3, 0.05, 1))
                    r = 0.01 * COEF
                    Image(self, (pos[0]-r/2, pos[1]-r/2, r, r),
                          constantes.images.impact.GetBitmap()).draw()
                    
                else:   # plusieurs points
                    ray = [rayons[j] for j in fsc]
                    ang = [angles[j] for j in mei]
                    for a in ang:
                        for r in ray:
                            pos = (self.ctr_Cib[0] + r * sin(a*_torad) ,
                                   self.ctr_Cib[1] - r * cos(a*_torad))
                #             boule(ctx, pos[0], pos[1], 0.005 * COEF, 
                #                   color0 = (0.95, 1, 0.9, 1), color1 = (0.1, 0.3, 0.05, 1))
                            r_ = 0.01 * COEF
                            Image(self, (pos[0]-r_/2, pos[1]-r_/2, r_, r_),
                                  constantes.images.impact.GetBitmap()).draw()




        #####################################################################################
        # Durée de la séquence
        #
        if not self.entete:
            self.ctx.set_source_rgb(0.5,0.8,0.8)
            self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                               cairo.FONT_WEIGHT_BOLD)
            
            
            re = (self.x_Org-self.p_mrg_Org,
                  self.pos_Dem[1] + self.h_Dem,
                  self.pos_Sea[0] - self.x_Org + self.p_mrg_Org,
                  0.015 * COEF)
            
            show_text_rect(self.ctx, getHoraireTxt(self.seq.GetDuree()),
                           re,
    #                        (posZDeroul[0]-0.01 * COEF, posZDemarche[1] + tailleZDemarche[1] , #- 0.015
    #                         0.1 * COEF, 0.015 * COEF),
                           ha = 'c', b = 0.01)
    
    
    
    
        #####################################################################################
        # Commentaires
        #
        if not self.entete:
            if self.siz_Com[1] > 0:
                self.ctx.set_source_rgb(0.1,0.1,0.1)
                self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_ITALIC,
                                                  cairo.FONT_WEIGHT_NORMAL)
                self.ctx.set_font_size(self.p_font_Com)
                _x, _y = self.pos_Com
                fascent, fdescent, fheight, *_ = self.ctx.font_extents()
                #
                # On dessine toutes les lignes de texte
                #
                for i, t in enumerate(self.intComm):
                    yt = _y + (fascent+fdescent)*i  + fheight #- fdescent
                    self.ctx.move_to(_x, yt)
                    self.ctx.show_text(t)
    
    
        ref = self.seq.GetReferentiel()
        
        
        
        ##################################################################################### 
        # Effectifs
        #
        if not self.entete:
            self.rEff, rects = Classe(self, (self.pos_Sea[0], self.pos_Dem[1],
                                      self.siz_Sea[0], self.pos_Sea[1]-self.pos_Dem[1]-0.01 * COEF),
                                      self.seq.classe).draw(complet = False)
    #         print("rEff", rEff)
            r = []
            for v in rects.values():
                r.extend(v)
            for v in r:
                self.seq.pt_caract.append((v[:2], "Eff"))
            self.seq.zones_sens.append(Zone_sens(r, param = "EFF", obj = self.seq.classe))
    #         seq.pt_caract.append((r[0][:2], "Eff"))
            
            # Lignes verticales
#             x = self.pos_Sea[0]
            h = (self.pos_Sea[1]-self.pos_Dem[1]-0.01 * COEF) / 5
            y = self.pos_Dem[1] + 4 * h
            for e in "CGDSTUEP":
                if e in self.rEff:
                    r0 = self.rEff[e][0] # le premier rectangle
                    w = r0[2]
                    self.DrawLigneEff(self.ctx, r0[0], r0[1]+r0[3], CouleurInt2Float(ref.effectifs[e][3]))
                    self.DrawLigneEff(self.ctx, w+r0[0], r0[1]+r0[3], CouleurInt2Float(ref.effectifs[e][3]))
    
    
        def taille(lstTxt):
            return sum([len(t) for t in lstTxt])
    
    
        #####################################################################################
        #  Prerequis
        #
        
        # Rectangle arrondi
        x0, y0 = self.pos_Pre
        rect_width, rect_height  = self.p_w_Pre, self.h_Pre 
        Curve_rect_titre(self,  
                         (x0, y0, rect_width, rect_height),
                         "Prérequis", 
                         self.p_Bcol_Pre, self.p_Icol_Pre, self.p_font_Pre).draw()
        
        #
        # Codes prerequis
        #
        lstTexteC = []
        lstCodesC = []
        lstCoulC = []
        
        
#         if ref.tr_com != []:
#             ref_tc = REFERENTIELS[ref.tr_com[0]]
#         else:
#             ref_tc = None
            
        lstComp = []
        lstTyp = []
        ttcomp = ref.getToutesCompetencesDict()
    #     for c in sorted(seq.prerequis["C"].competences):
        for c in constantes.trier(self.seq.prerequis["C"].competences):
            typ, cod = c[0], c[1:]
            
            comp = ttcomp[typ]
            
    #         if typ == "B" and ref.tr_com != []: # B = tronc commun --> référentiel
    #             comp = ref_tc.dicoCompetences["S"]
    #         else:
    #             if typ in list(ref.dicoCompetences.keys()):
    #                 comp = ref.dicoCompetences[typ]
    #             elif ref_tc and typ in list(ref_tc.dicoCompetences.keys()):
    #                 comp = ref_tc.dicoCompetences[typ]
            lstComp.append([cod,comp])
            if not typ in lstTyp:
                lstTyp.append(typ)
        
        multi = len(lstTyp) > 1
        
        for cod, comp in lstComp:   
            disc = comp.codeDiscipline
            intit = comp.getCompetence(cod).intitule
            if len(intit) == 0:
                intit = " "
            lstTexteC.append(intit)
            if multi:
                lstCodesC.append(comp.abrDiscipline + " " + cod)
            else:
                lstCodesC.append(cod)
            lstCoulC.append(constantes.COUL_DISCIPLINES[disc])
            
                
                
        lstTexteS = []
        lstCodesS = []
        lstCoulS = []
        
        ref = self.seq.GetReferentiel()
#         if ref.tr_com != []:
#             ref_tc = REFERENTIELS[ref.tr_com[0]]
#         else:
#             ref_tc = None
            
        lstSav = []
        lstTyp = []
        ttsav = ref.getTousSavoirsDict()
    #     for c in sorted(seq.prerequis["S"].savoirs):
        for c in constantes.trier(self.seq.prerequis["S"].savoirs):
            typ, cod = c[0], c[1:]
            savoir = ttsav[typ]
    #         if typ == "B" and ref.tr_com != []: # B = tronc commun --> référentiel
    #             savoir = ref_tc.dicoSavoirs["S"]
    #         else:
    #             if typ in list(ref.dicoSavoirs.keys()):
    #                 savoir = ref.dicoSavoirs[typ]
    #             elif ref_tc and typ in list(ref_tc.dicoSavoirs.keys()):
    #                 savoir = ref_tc.dicoSavoirs[typ]
            lstSav.append([cod, savoir])
            if not typ in lstTyp:
                lstTyp.append(typ)
        
        lstSav.sort(key = lambda x:x[0])
        
        multi = len(lstTyp) > 1
        
        for cod, savoir in lstSav:
            disc = savoir.codeDiscipline
            intit = savoir.getSavoir(cod).intitule
            if len(intit) == 0:
                intit = " "
            lstTexteS.append(intit)
            if multi:
                lstCodesS.append(savoir.abrDiscipline+" "+cod)
            else:
                lstCodesS.append(savoir.abrDiscipline+" "+cod)
            lstCoulS.append(constantes.COUL_DISCIPLINES[disc])
            
            
        lstTexteSe = []   
        for c in self.seq.prerequisSeance:
            lstTexteSe.append(c.GetNomFichier())    
            
        hl = rect_height+0.0001 * COEF
        
        ltot = taille(lstTexteC) + taille(lstTexteS) + taille(lstTexteSe)
        if ltot > 0:  # il y a qq chose à afficher
            
            wC, wS, wSe = self.repartir([taille(lstTexteC), taille(lstTexteS), taille(lstTexteSe)], 0.1)

#             print("sw:", wC+wS+wSe)

            # Mise à l'échelle
            wC  *= rect_width
            wS  *= rect_width
            wSe *= rect_width
            
#             print("W:", wC, wS, wSe)
            
            # Création des deux zones
            maxFontSize = 0.011 * COEF
            self.ctx.set_font_size(maxFontSize)
            f = self.ctx.font_extents()[2]
            rectC  = reduire_rect(x0, y0, wC, hl, f, 0.02)
            rectS  = reduire_rect(x0+wC, y0, wS, hl, f, 0.02)
            rectSe = reduire_rect(x0+wC+wS, y0, wSe, hl, f, 0.02)
            
            # lignes de séparation
            self.ctx.set_source_rgba (*self.p_Bcol_Pre)
            if wS > 0:
                self.ctx.move_to(x0+wC, y0)
                self.ctx.line_to(x0+wC, y0+hl)
                self.ctx.stroke()
            
            if wSe > 0:
                self.ctx.move_to(x0+wC+wS, y0)
                self.ctx.line_to(x0+wC+wS, y0+hl)
                self.ctx.stroke()
            
            r = Liste_code_texte2(self, rectC, lstCodesC, lstTexteC, 
                                 0.05*rect_width, 0.1,
                                 lstCoul = lstCoulC, va = 'c',
                                 coulFond = self.p_Icol_Pre).draw()
            self.ctx.set_source_rgba (0.0, 0.0, 0.5, 1.0)
            self.seq.prerequis["C"].pts_caract = getPts(r)
    #         print("prerequis C", getPts(r))
            for i, c in enumerate(sorted(self.seq.prerequis["C"].competences)): 
                self.seq.zones_sens.append(Zone_sens([r[i]], obj = self.seq.prerequis["C"]))
    #             seq.prerequis["C"].pt_caract = (r[i][:2], i)
    
            
            r = Liste_code_texte2(self, rectS, 
                                  lstCodesS, lstTexteS, 
                                 0.05*rect_width, 0.1,
                                 lstCoul = lstCoulS, va = 'c',
                                 coulFond = self.p_Icol_Pre).draw()
            self.ctx.set_source_rgba (0.0, 0.0, 0.5, 1.0)
            self.seq.prerequis["S"].pts_caract = getPts(r)
    #         print("prerequis S", getPts(r))
            for i, c in enumerate(sorted(self.seq.prerequis["S"].savoirs)): 
                self.seq.zones_sens.append(Zone_sens([r[i]], obj = self.seq.prerequis["S"]))
    #             seq.prerequis["S"].pt_caract = (r[i][:2], i)
            
    #         print("lstTexteSe", lstTexteSe, rectSe)
            lstRect = Liste_code_texte(self, rectSe, ["Seq."]*len(lstTexteSe), lstTexteSe, 
                                       0.05*rect_width, 0.1, va = 'c').draw()
            for i, c in enumerate(self.seq.prerequisSeance):
                self.seq.zones_sens.append(Zone_sens([lstRect[i]], obj = c))
                
        else:
            show_text_rect(self.ctx, "Aucun", (x0, y0, rect_width, hl), 
                           fontsizeMinMax = (-1, 0.015 * COEF))
            self.seq.zones_sens.append(Zone_sens([(x0, y0, rect_width, hl)], obj = self.seq.prerequis["S"]))
    
    
    
    
    
    
        ##################################################################################
        #  Objectifs
        #
        x0, y0 = self.pos_Obj
    #    tailleObj[0] =  taillePos[0]
        rect_width, rect_height  = self.siz_Obj
        Curve_rect_titre(self, (x0, y0, rect_width, rect_height),
                         ref.labels["OBJEC"][2].Plur_(),#"Objectifs", 
                         self.p_Bcol_Obj, self.p_Icol_Obj, self.p_font_Obj).draw()

        
        
        #
        # Codes objectifs
        #
        lstTexteC = []
        lstCodesC = []
        lstCoulC = []
        ref = self.seq.GetReferentiel()
    #     print(seq.GetObjAffiches())
    #     ref_tc = None
    #     if ref.tr_com != []:
    #         ref_tc = REFERENTIELS[ref.tr_com[0]]
            
        lstComp = []
        lstTyp = []
        for c in self.seq.GetObjAffiches():#obj["C"].competences:
            typ, cod = c[0], c[1:]
            comp = ttcomp[typ]
            
    #         comp = None
    # #         print "typ, cod =", typ, cod
    #         if typ == "B" and ref.tr_com != []: # B = tronc commun --> référentiel
    #             comp = ref_tc.dicoCompetences["S"]
    #         else:
    #             if typ in list(ref.dicoCompetences.keys()):
    #                 comp = ref.dicoCompetences[typ]
    #             elif ref_tc and typ in list(ref_tc.dicoCompetences.keys()):
    #                 comp = ref_tc.dicoCompetences[typ]
            lstComp.append([cod,comp])
            if not typ in lstTyp:
                lstTyp.append(typ)
        
        multi = len(lstTyp) > 1
        
    #     lstComp.sort(key = lambda x:x[0])
        
        for cod, comp in lstComp:    
            disc = comp.codeDiscipline
            if isinstance(comp, Referentiel.Fonctions):
                intit = comp.getFonction(cod)[0]
            else:
                intit = comp.getCompetence(cod).intitule
            if len(intit) == 0: # Précaution nécessaire car bug : parfois == ""
                intit = " "
            lstTexteC.append(intit)
            if multi:
                lstCodesC.append(comp.abrDiscipline + " " + cod)
            else:
                lstCodesC.append(cod)
            lstCoulC.append(constantes.COUL_DISCIPLINES[disc])
            
    
        lstTexteS = []
        lstCodesS = []
        lstCoulS = []
        
        lstSav = []
        lstTyp = []
        
    #     for c in sorted(seq.obj["S"].savoirs):
        for c in constantes.trier(self.seq.obj["S"].savoirs):
            typ, cod = c[0], c[1:]
            savoir = ttsav[typ]
            
    #         if typ == "B" and ref.tr_com != []: # B = tronc commun --> référentiel
    #             savoir = ref_tc.dicoSavoirs["S"]
    #         else:
    #             if typ in list(ref.dicoSavoirs.keys()):
    #                 savoir = ref.dicoSavoirs[typ]
    #             elif ref_tc and typ in list(ref_tc.dicoSavoirs.keys()):
    #                 savoir = ref_tc.dicoSavoirs[typ]
            lstSav.append([cod,savoir])
            if not typ in lstTyp:
                lstTyp.append(typ)
        
        multi = len(lstTyp) > 1
        
        for cod, savoir in lstSav:
            disc = savoir.codeDiscipline
            intit = savoir.getSavoir(cod).intitule
            if len(intit) == 0: # Précaution nécessaire car bug : parfois == ""
                intit = " "
            lstTexteS.append(intit)
            if multi:
                lstCodesS.append(savoir.abrDiscipline + " " + cod)
            else:
                lstCodesS.append(cod)
            lstCoulS.append(constantes.COUL_DISCIPLINES[disc])
    #     print("lstTexteS", lstTexteS)
        
        h = rect_height+0.0001 * COEF
        
        ltot = taille(lstTexteC) + taille(lstTexteS)
        
        # Nombre de colonnes
    #     nc = 1*(len(lstTexteC) > 0) + 1*(len(lstTexteS) > 0)
        
        if ltot > 0:
            # Répartition gauche/droite
            c = [taille(lstTexteC)/ltot, taille(lstTexteS)/ltot]
            if c[0] > 0 and c[1] > 0:
                if c[1] < 0.25:
                    c[1] = 0.25
                    c[0] = 0.75
                elif c[0] < 0.25:
                    c[0] = 0.25
                    c[1] = 0.75
            wC = rect_width*c[0]
            wS = rect_width*c[1]
            
            # Création des deux zones
            maxFontSize = 0.011 * COEF
            self.ctx.set_font_size(maxFontSize)
            f = self.ctx.font_extents()[2]
            rectC = reduire_rect(x0, y0, wC, h, f, 0.02)
            rectS = reduire_rect(x0+wC, y0, wS, h, f, 0.02)
            
            self.ctx.set_source_rgba (*self.p_Bcol_Obj)
            self.ctx.move_to(x0+wC, y0)
            self.ctx.line_to(x0+wC, y0+h)
            self.ctx.stroke()
            
            self.ctx.set_source_rgba (*COUL_COMPETENCES)
            r = Liste_code_texte2(self,rectC,  
                                 lstCodesC, lstTexteC, 
                                 0.03*rect_width, 0.1, 
                                 lstCoul = lstCoulC, va = 'c',
                                 coulFond = self.p_Icol_Obj).draw()
            self.seq.obj["C"].pts_caract = getPts(r)
            
            self.ctx.set_source_rgba (0.0, 0.0, 0.0, 1.0)
    #        r = liste_code_texte(ctx, [s[1:] for s in seq.obj["S"].savoirs], 
    #                             lstTexteS, x0, y0+hC, rect_width, hS, 0.008)
            
            r = Liste_code_texte2(self, rectS, 
                                 lstCodesS, lstTexteS, 
                                 0.03*rect_width, 0.1, 
                                 lstCoul = lstCoulS, va = 'c',
                                 coulFond = self.p_Icol_Obj).draw()
            self.seq.obj["S"].pts_caract = getPts(r)
        
            self.seq.zones_sens.append(Zone_sens([rectC], obj = self.seq.obj["C"]))
            self.seq.zones_sens.append(Zone_sens([rectS], obj = self.seq.obj["S"]))
    #    seq.obj["C"].rect = 
#             self.seq.obj["S"].rect = [rectS]
#             self.seq.obj["C"].rect = [rectC]
        
    
    
    
    
    
        #################################################################################
        #  CI
        #
        self.Draw_CI(self.ctx, self.seq.CI, self.seq)
    
    
    
    
        
        #################################################################################
        #  Séances
        #
        if not self.entete:
            for s in self.seq.seances:
        #        Draw_seance(ctx, s, curseur)
                self.DrawSeanceRacine(s)
            
        #
        #  Tableau des systèmes
        #    
        if not self.entete:
            nomsSystemes = []
            systemes = self.seq.GetSystemesUtilises(niveau = 0)
            for s in systemes:
                nomsSystemes.append(s.nom)
            
            if nomsSystemes != []:
                self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_NORMAL)
                self.ctx.set_source_rgb(0, 0, 0)
                self.ctx.set_line_width(0.001 * COEF)
                TableauV(self, nomsSystemes, self.pos_Sys[0], self.pos_Sys[1], 
                        self.siz_Sys[0], self.pos_Sea[1] - self.pos_Sys[1], 
                        0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', coul = (0.8,0.8,0.8)).draw()
                
                wc = self.siz_Sys[0]/len(nomsSystemes)
                _x = self.pos_Sys[0]
                _y = self.pos_Sys[1]
                for s in systemes:
        #            s.rect=((_x, _y, wc, posZSeances[1] - posZSysteme[1]),)
                    self.seq.zones_sens.append(Zone_sens([(_x, _y, wc, self.pos_Sea[1] - self.pos_Sys[1])],
                                               obj = s))
                    self.ctx.set_source_rgb(0, 0, 0)
                    self.ctx.move_to(_x, _y + self.pos_Sea[1] - self.pos_Sys[1])
                    self.ctx.line_to(_x, _y + self.h_Dem)
                    self.ctx.stroke()
                    
                    self.ctx.set_source_rgba(0.8,0.8,0.8, 0.2)
                    self.ctx.rectangle(_x, _y+ self.pos_Sea[1] - self.pos_Sys[1], 
                                  wc, self.h_Dem-self.pos_Sea[1] + self.pos_Sys[1])
                    self.ctx.fill()
                    _x += wc
                self.ctx.set_source_rgb(0, 0, 0)
                self.ctx.move_to(_x, _y + self.pos_Sea[1] - self.pos_Sys[1])
                self.ctx.line_to(_x, _y + self.h_Dem)   
                self.ctx.stroke()
    
    
        #
        #  Tableau des démarches
        #
        if not self.entete and self.seq.HasDemarches():
            if len(ref.listeDemarches) > 0:
                self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_NORMAL)
                self.ctx.set_source_rgb(0, 0, 0)
                show_text_rect(self.ctx, ref._nomDemarches.Sing_(),
                               (self.pos_Dem[0], self.pos_Dem[1],
                                self.p_w_Dem, self.pos_Sea[1] - self.pos_Sys[1]), \
                       va = 'h', ha = 'g', le = 0.8, pe = 1.0, \
                       b = 0.03, orient = 'v', \
                       fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False, 
                       coulBord = None, tracer = True, ext = "...")
                
                
    
    
    
        #
        #  Tableau des séances (en bas)
        #
        if not self.entete:
            if self.intituleSeances[0] != []:
                self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_NORMAL)
                self.ctx.set_source_rgb(0, 0, 0)
                self.ctx.set_line_width(0.001 * COEF)
                TableauH_var(self, self.intituleSeances[0], self.pos_ISea[0], self.pos_ISea[1], 
                        0.05* COEF, self.siz_ISea[0]-0.05 * COEF, self.intituleSeances[2], self.p_font_ISea, 
                        nCol = 1, va = 'c', ha = 'g', orient = 'h', coul = self.p_Icol_Sea_, 
                        contenu = [self.intituleSeances[1]]).draw()
            
        #
        # Informations
        #
        if not self.entete:
            self.info(self.ctx)
        
        self.surBrillance(ctx, surObj)
                    
        self.seq.zones_sens.reverse()
                

    ######################################################################################  
    def DrawLigneEff(self, ctx, x, y, coul):
    #     dashes = [ 0.010 * COEF,   # ink
    #                0.002 * COEF,   # skip
    #                0.005 * COEF,   # ink
    #                0.002 * COEF,   # skip
    #                ]
        dashes = [ 0.002 * COEF,   # ink
                   0.002 * COEF,   # skip
                   ]
        ctx.set_source_rgba (*coul)
        ctx.set_line_width (0.0005 * COEF)
        ctx.set_dash(dashes, 0)
        ctx.move_to(x, self.pos_Dem[1] + self.h_Dem)
        ctx.line_to(x, y)
        ctx.stroke()
        ctx.set_dash([], 0)
    
    
        
    ######################################################################################  
    def H_code(self):
        """ Renvoie la hauteur des codes de séance
        """  
        return max(self.ecartY/4, 0.01 * COEF)
                
                  
    ######################################################################################  
    def Draw_CI(self, ctx, CI, seq):
        # Rectangle arrondi
        x0, y0 = self.pos_CI
        rect_width, rect_height  = self.p_siz_CI
        
        ref = CI.GetReferentiel()
        
        if len(CI.numCI)+len(CI.CI_perso) > 1:
            t = ref._nomCI.Plur_()
        else:
            t = ref._nomCI.Sing_()
        
        rect = (x0, y0, rect_width, rect_height)
        CI.pt_caract = [(Curve_rect_titre(self, rect, t, 
                                          self.p_Bcol_CI, self.p_Icol_CI, self.p_font_CI).draw(), 
                        'CI')]
        seq.zones_sens.append(Zone_sens([rect], obj = CI))
    #     CI.rect.append(rect)
        
        
        
        #
        # code et intitulé des CI
        #
    #     lstCodes = []
    #     lstIntit = []
    #     for i, c in enumerate(CI.numCI):
    #         lstCodes.append(CI.GetCode(i))
    #         lstIntit.append(CI.GetIntit(i))
    #     
    #     for j, c in enumerate(CI.CI_perso):
    #         lstCodes.append(ref.abrevCI+str(len(ref.CentresInterets)+j+1))
    #         lstIntit.append(c)
    # 
    #     print("CI:", lstCodes, lstIntit)
        lstCodes = CI.GetCodesCIs()
        lstIntit = CI.GetNomCIs()
        #
        # Problématiques
        #
        lstPb = []
        for c in CI.Pb:
            lstPb.append(c)
            
        for c in CI.Pb_perso:
            lstPb.append(c)
        
    
        #
        # Affichage
        #
        t = len(lstCodes) + len(lstPb)
        if t > 0:
            hCI = rect_height * len(lstCodes) / t
            hPb = rect_height * len(lstPb) / t
            if len(lstCodes) > 0:
                r = Liste_code_texte(self, (x0, y0+0.0001 * COEF, rect_width, hCI),
                                     lstCodes, lstIntit, 
                                     0.05*rect_width, 0.1, va = 'c').draw()
                CI.pts_caract = getPts(r)
            
            ctx.select_font_face (self.font_family, cairo.FONT_SLANT_ITALIC,
                                               cairo.FONT_WEIGHT_NORMAL)
            show_text_rect(ctx, "\n".join(lstPb), 
                           (x0, y0+0.0001 * COEF + hCI, rect_width, hPb)
                           )

    
    
    ######################################################################################  
    def DrawSeanceRacine(self, seance):
    #    if seance.GetDureeGraph() == 0:
    #        return
            
        #
        # Flèche indiquant la durée
        #
        h = self.calcH(seance.GetDureeGraph())
        if seance.GetDureeGraph() > 0:
            
            e = self.p_w_Dur
            Fleche_verticale(self, self.pos_Der[0]+e/4, self.cursY, 
                             h, e, (0.9,0.8,0.8,0.5)).draw()
            self.ctx.set_source_rgb(0.5,0.8,0.8)
            self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_BOLD)
            he = min(e/2, h/3)
            
            if h-he < e:
                o = 'h'
            else:
                o = 'v'
            show_text_rect(self.ctx, getHoraireTxt(seance.GetDuree()), 
                           (self.pos_Der[0]-e/4, self.cursY, e, h-he), 
                           orient = o, b = 0.02)
    
        
    
        #
        # Remplissage du tableau de blocs : [[], [], ...]
        #
        def getBloc(seance, h, filigrane = False, decal = 0, nbr = 0, rotation = False):
            """ Construction récursive du bloc (et des sous blocs) de la Séance
            
            :h: hauteur du bloc
            :filigrane: True si  il faut afficher le bloc en mode filigrane (transparent)
            :decal: proportion (0-1) du décalage pour les Séances en parallèles
            :nbr:   nombre de Séances en parallèles
            :rotation: True si la Séance fait partie d'une Rotation
            
            """
#             seance.rect = []
            
            ###########################################################################################
            # Séance "simple" --> un seul bloc d'une ligne de un ou plusieurs cadres 
            if not seance.typeSeance in ["R", "S", ""]:
                bloc = Bloc(self, seance)
                seance.pts_caract = []
    
                l = []
                if rotation:
                    n = 1
                else:
                    n = int(seance.nombre.v[0])
                
                for i in range(n):
                    l.append(Cadre(self, seance, h, signEgal = (i>0), filigrane = filigrane))
                bloc.contenu.append(l)
                
                hc = self.H_code()
                if not filigrane:
                    if decal == 0 :
                        l[-1].dy = l[-1].h/2
                        l[-1].nf = 0
                    else:
                        l[-1].dy = hc + decal * (l[-1].h - hc)
                        l[-1].nf = nbr
                else:
                    l[-1].dy = hc + decal * (l[-1].h - hc)
                    l[-1].nf = nbr
            
                return bloc
                
                
            ###########################################################################################
            # Séance "complexe"   (Rotation ou Parallèle) 
            else:
                # Rotation : plusieurs lignes/plusieurs colonnes
                if seance.typeSeance == "R":           
                    bloc = Bloc(self, seance)
                    l0 = seance.GetListSousSeancesRot() # Liste des sous séances de la première colonne (têtes de ligne - foncé)
    #                print "l0 =", l0
                    for ss in l0[:seance.nbrRotations.v[0]]:
                        hl = h * ss.GetDuree()/seance.GetDuree() * len(l0)/  seance.nbrRotations.v[0] 
                        bloc.contenu.append([getBloc(ss, hl, rotation = True)])
                        
                    #
                    # Aperçu en filigrane du reste de la rotation
                    #
                    if True:#seance.IsEffectifOk() <= 3:
                        l = seance.GetListSousSeancesRot(True)
    #                    print "  l =", l
                        for _ in range(len(l)-1): # Colonnes
                            l = permut(l)
    #                        print "   ", l
                            for i, ss in enumerate(l[:seance.nbrRotations.v[0]]):   # Lignes
                                hl = h * ss.GetDuree()/seance.GetDuree() * len(l0)/  seance.nbrRotations.v[0] 
                                bloc.contenu[i].extend([getBloc(ss, hl, filigrane = True, rotation = True)])
    #                blocs.extend(bloc)
    #                print "   >>", bloc.contenu
                    return bloc
                
                # Parallèle : plusieurs colonnes
                elif seance.typeSeance == "S":
                    n = len(seance.seances)
                    bloc = Bloc(self, seance)
                    bloc.contenu.append([])
    #                bloc.contenu.append(getLigne(seance, h))
                    for j, ss in enumerate(seance.seances):
                        bloc.contenu[0].append(getBloc(ss, h*ss.GetDuree()/seance.GetDuree(), 
                                                       decal = 1.0*(j+1)/(n+1),
                                                       nbr = n))
                    
                    return bloc
                
                return Bloc(self, seance)
            return Bloc(self, seance)
    
        bloc = getBloc(seance, h)
        
    #    print "bloc :", bloc
    #    print "  ", cursY,
    #    y = cursY
    #     x, cursY , w, h = bloc.Draw(posZSeances[0], cursY)
    #     if seance.typeSeance in "RS":
             
        if seance.EstSeance_RS() and len(seance.seances) > 0:
            ce = seance.seances[0].effectif
        else:
            ce = seance.GetCodeEffectif()
        x0 = self.rEff[ce][0][0]
        
        # Gestion des séances à effectif dont tous les sous-groupes font les mêmes activités
        classe = seance.GetDocument().classe
        ncouches = classe.GetNbrCouches(seance.GetCodeEffectif()) - 1
    #     print("Bloc", seance, ":", ncouches, "couches")
        
    
        for c in range(ncouches):
            x = x0 + self.ecartC*c/ncouches
            y = self.cursY + self.ecartC*c/ncouches
            bloc.draw(x = x, y = y, vide = True)
    
            
        if ncouches > 0:
            x0 += self.ecartC
            self.cursY += self.ecartC
            
        x, self.cursY , w, h = bloc.draw(x = x0, y = self.cursY)
        seance.GetDocument().zones_sens.append(Zone_sens([(bloc.x, bloc.y, w, h)], obj = seance))
#         seance.rect.append((bloc.x, bloc.y, w, h))
        
        bloc.DrawCroisement(seance.typeSeance == "R") 
    #    for lbloc in blocs:
    #        
    #        x = posZSeances[0]
    #        yf = y
    #        for bloc in lbloc:
    #            # Tracé des blocs
    #            xf, yf = bloc.Draw(x, y)
    #            x += xf
    #            
    #            # Tracé des croisements "Démarche" et "Systèmes"
    #            bloc.DrawCroisement(seance.typeSeance == "R")
    #        print "..", yf, 
    #        y = yf
    #    print 
        self.cursY += self.ey_Sea


    #####################################################################################  
    def DrawDomaines(self, x, y, r = 0.008 * COEF):
        """ Tracé des logos des Domaines
            x : centre de la zone
            y : haut de la zone
        """
        p = 0.8
        self.ctx.set_line_width (0.0006 * COEF)
        y += r
        
        def draw(x, y, t, c):
            self.ctx.set_source_rgba (c[0]/3, c[1]/3, c[2]/3, 0.4)
            self.ctx.arc(x, y, r, 0, 2*pi)
            self.ctx.fill_preserve ()
            self.ctx.set_source_rgba (c[0], c[1], c[2], 1)
            show_text_rect(self.ctx, t, (x-r, y-r, 2*r, 2*r),
                                   wrap = False, couper = False)
            self.ctx.stroke ()
        
        dx = p*r
        dy = p*r*1.732
        
        ref = self.seq.GetReferentiel()
        for i, d in enumerate(self.seq.domaine):
            X = x + [0, -1, 1][i%3]*dx
            c = 2 * (i//3) + (i%3 + 1)//2
            Y = y + c*dy
            draw(X, Y, d, ref.domaines[d][3])
        
        if len(self.seq.domaine) > 0:
            rect = x-r-dx, y-r, 2*(r+dx), Y-y+2*r
            self.seq.zones_sens.append(Zone_sens([rect], param = "DOM"))
        



    

######################################################################################  
class Cadre(Elem_Dessin):  
    """ Plus petit élément de séance :
         - 1 cadre
         - 1 code
         - 1 intitulé
    """
    def __init__(self, parent, seance, h, filigrane = False, signEgal = False): 
        Elem_Dessin.__init__(self, parent)
        
        self.seance = seance

        
        if not seance.effectif in self.parent.rEff:
            print("CONFLIT Effectif !", seance.effectif, self.parent.rEff.keys())
            return
        r = self.parent.rEff[seance.effectif]
#         self.w = r[0][2]
        self.w = (r[-1][0]+r[-1][2] - r[0][0])/len(r)
        self.h = h
        
#         self.d = 0
#         ref = seance.GetReferentiel()
#         if len(ref.effectifs[seance.effectif]) >= 6 and ref.effectifs[seance.effectif][5] == "O":
#             self.d = ecartX * seance.GetDocument().classe.nbrGroupes[seance.effectif]
#             self.d = min(self.d, self.h/6)
#             self.w -= self.d
#             self.h -= self.d                      
        
        self.filigrane = filigrane
        self.xd = None
        self.y = None   # Position en Y du cadre
        self.dy = None  # Position en Y relative de la ligne
        self.nf = 0     # Nombre de "frères" (pour calcul rayon boule
#         self.seance.rect = []
        self.signEgal = signEgal
        
        
        # Gestion des séances à effectif dont tous les sous-groupes font les mêmes activités
#         ref = seance.GetReferentiel()
        
        # Réduction taille
#         self.ncouches = seance.GetDocument().classe.GetNbrCouches(seance.GetCodeEffectif()) - 1
#         print("Cadre", self.seance, ":", self.ncouches, "couches")
#         if self.ncouches >= 1 :
#             self.h -= ecartC
#         if len(ref.effectifs[seance.GetCodeEffectif()]) >= 6 and ref.effectifs[seance.GetCodeEffectif()][5] == "O":
# #             self.w -= ecartC
#             self.h -= ecartC
#             # Les éventuelles couches supplémentaires
#             # pour séances à effectif dont tous les sous-groupes font les mêmes activités
#             self.ncouches = seance.GetDocument().classe.nbrGroupes[seance.GetCodeEffectif()]-1
#         else:
#             self.ncouches = 0
            
            
        
    def __repr__(self):
        return self.seance.code
    
    
    
    def _draw(self, ctx = None, x = 0, y = 0, vide = False):
        """ Dessine le cadre à la position (x,y)
        """
        if self.filigrane:
            alpha = 1.4#0.2
        else:
            alpha = 1
            self.seance.pts_caract.append((x, y))
#         print(self.seance, (x, y))
        
        #
        # Le(s) cadre(s)
        #
        epaisseurTrait = 0.0015 * COEF
        self.ctx.set_line_width(epaisseurTrait)
        self.ctx.set_dash(self.parent.Bstyl_Sea[self.seance.typeSeance], 0)
        
        # Rectangle(s) des couches à afficher derrière
#         for c in range(self.ncouches):
#             _x = x + ecartC*c/self.ncouches
#             _y = y + ecartC*c/self.ncouches
#             rectangle_plein(self.ctx, _x, _y, self.w, self.h, 
#                             BCoulSeance[self.seance.typeSeance], 
#                             ICoulSeance[self.seance.typeSeance], alpha)
#         
#         if self.ncouches > 0:
#             x += ecartC
#             y += ecartC
        
        # Rectangle(s) du dessus
        Rectangle_plein(self, (x, y, self.w, self.h), 
                            self.parent.p_Bcol_Sea_[self.seance.typeSeance], 
                            self.parent.p_Icol_Sea_[self.seance.typeSeance], alpha).draw()

        self.ctx.set_dash([], 0)
        
        
        if not vide:
            wc = 0 # la largeur effective du code (calculé dans show_text_rect)
            #
            # Le code (en haut à gauche)
            #
            if hasattr(self.seance, 'code'):
                self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_BOLD)
                c = self.seance.couleur
                self.ctx.set_source_rgba (*c[:3], alpha)

                hc = self.parent.H_code()
                _, r, _ = show_text_rect(self.ctx, self.seance.code, 
                                         (x, y, self.w, hc), 
                                         ha = 'g', 
                                         wrap = False, fontsizeMinMax = (minFont, -1), b = 0.02)
                
                wc = r[2] + self.parent.ecartX/2
            
            #
            # L'intitulé (si intituleDansDeroul)
            #
            if self.seance.intituleDansDeroul and self.seance.intitule != "" and self.h-hc > 0:  #not self.filigrane and 
                self.ctx.select_font_face (self.font_family, cairo.FONT_SLANT_ITALIC,
                                           cairo.FONT_WEIGHT_NORMAL)
                self.ctx.set_source_rgba (0,0,0, alpha)
    #            print (x, y + hc, self.w, self.h-hc)
    #            print (wc, y, self.w - (wc-x), self.h)
    #            print 
                if self.h < 0.02 * COEF: # h petit -> on écrit à coté du code !
                    rct = (x+wc, y, self.w - (wc-x), self.h)
                else:
                    rct = (x, y + hc, self.w, self.h-hc)
    
                show_text_rect(self.ctx, self.seance.intitule, rct, 
                               ha = 'g', b = 0.02, fontsizeMinMax = (minFont, 0.015 * COEF), 
                               fontsizePref = self.seance.taille.v[0])
            
            #
            # Le signe "égal"
            #
            if  self.signEgal:# not self.filigrane and
                dx = self.parent.rEff["P"][0][2]/16
    #            dy = hHoraire/32
                dy = self.parent.ecartY/4
                self.ctx.set_source_rgba (0, 0.0, 0.2, alpha)
                self.ctx.set_line_width (0.002 * COEF)
                self.ctx.move_to(x-dx, y+self.h/2 - dy)
                self.ctx.line_to(x+dx, y+self.h/2 - dy)
                self.ctx.move_to(x-dx, y+self.h/2 + dy)
                self.ctx.line_to(x+dx, y+self.h/2 + dy)
                self.ctx.stroke()
        
        
        
        # Sauvegarde de la position du bord droit pour les lignes de croisement
        self.xd = x+self.w
        self.y = y
        
        self.seance.GetDocument().zones_sens.append(Zone_sens([(x, y, self.w, self.h)], obj = self.seance))
#         self.seance.rect.append([x, y, self.w, self.h])
        
        return x + self.w, y + self.h




######################################################################################  
class Bloc(Elem_Dessin):
    """ Ensemble de cadres.
        contenu = [[], [], ...]
        lignes
    """
    def __init__(self, parent, seance):
        Elem_Dessin.__init__(self, parent)
        
        self.contenu = []
     
        self.seq = seance.GetDocument()
        self.seance = seance
        
        self.x = None
        self.y = None
        
#         # Gestion des séances à effectif dont tous les sous-groupes font les mêmes activités
#         self.ncouches = self.seq.classe.GetNbrCouches(seance.GetCodeEffectif()) - 1
#         print("Bloc", self.seance, ":", self.ncouches, "couches")
#         ref = seance.GetReferentiel()
#         if len(ref.effectifs[seance.GetCodeEffectif()]) >= 6 and ref.effectifs[seance.GetCodeEffectif()][5] == "O":
#             # Les éventuelles couches supplémentaires
#             # pour séances à effectif dont tous les sous-groupes font les mêmes activités
#             self.ncouches = self.seq.classe.nbrGroupes[seance.GetCodeEffectif()]-1
#         else:
#             self.ncouches = 0
    
#     def GetRect(self):
#         return (self.x, self.y, )
    
    
    
    def _draw(self, ctx = None, x = 0, y = 0, vide = False):
#         print("Draw", self.seance, self.seance.GetCodeEffectif())
        self.x = x
        self.y = y
        xf = self.x # position droite du rectangle (à incrémenter)
        yf = self.y # position basse du rectangle (à incrémenter)
            
        # La couche du dessus
        y = self.y
        for ligne in self.contenu:
#            print 
            x = self.x
#            x = posZSeances[0]
            for elem in ligne:
#                print "  > ", elem
                if isinstance(elem, Cadre):
                    xf, yf = elem.draw(x = x, y = y, vide = vide)
                    
                elif isinstance(elem, Bloc):
                    xf, yf, w, h = elem.draw(x = x, y = y, vide = vide)
                    
                x = xf
                    
            if len(ligne) > 0:
                y = yf
        
        w = xf - self.x
        h = yf - self.y
        
        self.seance.GetDocument().zones_sens.append(Zone_sens([(self.x, self.y, w, h)], obj = self.seance))
#         self.seance.rect.append((self.x, self.y, w, h))
            
        return x, y, w, h
    
    
    def DrawCroisement(self, estRotation):
        """ Dessine les différents croisement :
            - séance/système  : rond avec nbr syst
            - séance/démarche : boule
            et un trait en pointillé ._._.
        """
        
#        print "DrawCroisement", estRotation
        for ligne in self.contenu:
            for cadre in ligne:
                
                if isinstance(cadre, Cadre):
                    if not cadre.filigrane and cadre.dy != None:
                        #
                        # Les lignes horizontales
                        #
                        if cadre.seance.typeSeance in ACTIVITES:
                            self.DrawLigne(cadre.ctx, 
                                      cadre.xd, cadre.y + cadre.dy, 
                                      cadre.seance.couleur)
    
                        #
                        # L'icone "démarche"
                        #
                        r = min(self.parent.p_w_Dem, cadre.h/(cadre.nf+1))
                        if len(cadre.seance.GetReferentiel().listeDemarches) > 0:
                            self.DrawCroisementsDemarche(cadre.ctx, cadre.seance, cadre.y + cadre.dy, r)
                        
                        
                        #
                        # Le rond "nombre de systèmes nécessaires"
                        #
                        r = min(self.parent.p_wCol_Sys, cadre.h/(cadre.nf+1))
                        if not estRotation: # Cas des rotations traité plus bas ...
                            self.DrawCroisementSystemes(cadre.ctx, cadre.seance, cadre.xd, cadre.y + cadre.dy, 
                                                   cadre.seance.GetNbrSystemes(niveau = 0), r)
                
                else:
                    cadre.DrawCroisement(estRotation)
            
            #
            # Cas des rotations :
            #
            if estRotation:
                NS = {}
                cadreOk = False
                for cadre in ligne:
                    if isinstance(cadre, Cadre):
                        ns = cadre.seance.GetNbrSystemes(simple = True, niveau = 0)
                        mergeDict(NS, ns)
                        
#                        if cadre.dy:# != None:
                        if not cadre.filigrane:
#                            print cadre.dy
                            cadreOk = cadre
                    else:
                        cadre.DrawCroisement(estRotation)
                if cadreOk:
#                    print "!!!"
                    r = min(self.parent.p_wCol_Sys, cadreOk.h/(cadreOk.nf+1)/3)
                    self.DrawCroisementSystemes(cadreOk.ctx, cadreOk.seance, cadre.xd, cadreOk.y + cadreOk.dy,
                                           NS, r)
            




    ######################################################################################  
    def DrawLigne(self, ctx, x, y, c = (0, 0.0, 0.2, 0.6)):
        dashes = [ 0.010 * COEF,   # ink
                   0.002 * COEF,   # skip
                   0.005 * COEF,   # ink
                   0.002 * COEF,   # skip
                   ]
        
        ctx.set_source_rgba (c[0], c[1], c[2], 0.5)
        ctx.set_line_width (0.0006 * COEF)
        ctx.set_dash(dashes, 0)
        ctx.move_to(self.parent.x_Org+self.parent.siz_Org[0], y)
        ctx.line_to(x, y)
        ctx.stroke()
        ctx.set_dash([], 0)




    ######################################################################################  
    def DrawCroisementSystemes(self, ctx, seance, x, y, ns, w):
        """ Remplissage du tableau des systèmes mobilisés pour la séance
            :ns: nombre de systèmes
        """
    #        if self.typeSeance in ["AP", "ED", "P"]:
    #            and not (self.EstSousSeance() and self.parent.typeSeance == "S"):
    #    #
    #    # Les lignes horizontales
    #    #
    #    if seance.typeSeance in ACTIVITES:
    #        DrawLigne(ctx, x, y, seance.couleur)
        
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
    
        for s, n in list(ns.items()):
            if n > 0 and s in list(self.parent.xSystemes.keys()):
                x = self.parent.xSystemes[s]
                rect = (x-w/2, y-w/2, w, w)
                ctx.rectangle(*rect)
                ctx.set_source_rgba(1,1,1, 0.5)
                ctx.fill()
                ctx.set_source_rgba(*seance.couleur)
                show_text_rect(ctx, str(n), rect,
                               wrap = False, couper = False)
                
                seance.GetDocument().zones_sens.append(Zone_sens([rect],
                                                                 obj = seance))
                    
        return
        
        
        
    #     #
    #     # Cercle avec nombre de systèmes dedans
    #     #
    #     if r >= wColSysteme/4:
    #     #    ns = seance.GetNbrSystemes(posDansRot = posDansRot)
    #         for s, n in ns.items():
    #             if n > 0:
    #                 x = xSystemes[s]
    #                 ctx.arc(x, y, r, 0, 2*pi)
    #                 ctx.set_source_rgba (1,0.2,0.2,1.0)
    #                 ctx.fill_preserve ()
    #                 ctx.set_source_rgba (0,0,0,1)
    #                 ctx.stroke ()
    #                 ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
    #                                       cairo.FONT_WEIGHT_BOLD)
    #                 show_text_rect(ctx, str(n), (x-r, y-r, 2*r, 2*r),
    #                                wrap = False, couper = False)
    #                 
    #                 seance.GetDocument().zones_sens.append(Zone_sens([(x-r, y-r, 2*r, 2*r)],
    #                                                                  obj = seance))
    # #                seance.rect.append((x-r, y-r, 2*r, 2*r))
    #     else:
    #         for s, n in ns.items():
    #             if n > 0:
    #                 x = xSystemes[s] - wColSysteme/2
    #                 p = wColSysteme/n
    #                 for i in range(n):
    #                     ctx.arc(x+p*i+p/2, y, r, 0, 2*pi)
    #                     ctx.set_source_rgba (1,0.2,0.2,1.0)
    #                     ctx.fill_preserve ()
    #                     ctx.set_source_rgba (0,0,0,1)
    #                 ctx.stroke ()
    #                 
    #                 seance.GetDocument().zones_sens.append(Zone_sens([(x-wColSysteme/2, y-r, wColSysteme, 2*r)],
    #                                                                  obj = seance))
    #                 
    # #                seance.rect.append((x-wColSysteme/2, y-r, wColSysteme, 2*r))
            
            
    



          

    #####################################################################################  
    def DrawCroisementsDemarche(self, ctx, seance, y, w):
            
        #
        # Croisements Séance/Démarche
        #
        ref = seance.GetReferentiel()
        if seance.typeSeance in ref.activites.keys():
            ld = seance.demarche.split()
            if len(ld) > 0:
                n = len(ld)
                for i, d in enumerate(ld):
                    bmp = constantes.imagesDemarches[d].GetBitmap()
                    dx = w*(i-(n-1)/2)/2
                    rect =    (self.parent.pos_Dem[0] + dx, y - w/2 + dx, w, w)
                    Image(self, (self.parent.pos_Dem[0] + dx, y - w/2 + dx, w, w), 
                          bmp, marge = 0.1).draw()
    #     _x = xDemarche[seance.demarche]
    # #        if self.typeSeance in ["AP", "ED", "P"]:
    # #    r = 0.008 * COEF
    #     boule(ctx, _x, y, r)
        
                seance.GetDocument().zones_sens.append(Zone_sens([rect], obj = seance))
    
#                 seance.rect.append(rect)



        
        

def gabarit():
    print("Génération du gabarit ...", end=' ') 
    import draw_cairo_seq
    imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  2100, 2970)#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
    ctx = cairo.Context(imagesurface)
    
    e = 28
    ctx.scale(e, e) 
    
#     print dir(draw_cairo_prj)
    pos = {}
    taille = {}
    for attr in dir(draw_cairo_seq):
        if attr[:3] == 'pos':
            pos[attr[3:]] = attr
        if attr[:6] == 'taille':
            taille[attr[6:]] = attr
    
    print(pos, taille)
    
    ctx.set_line_width(5.0/e)
    
    for k, p in list(pos.items()):
        if k in list(taille.keys()):
            x, y = getattr(draw_cairo_seq, p)
            w, h = getattr(draw_cairo_seq, taille[k])
            
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
    
    
    imagesurface.write_to_png('gabarit_seq.png')



#     return {n : CouleurFloat2CSS(v) for n, v in globals().items() if "coul_" in n}


# nom_module = os.path.splitext(os.path.basename(__file__))[0]
# nom_fichparam = "param_seq.cfg"
# 
# if __name__ == '__main__':
#     sauverParametres(getParametres().keys(), 
#                      nom_module, 
#                      nom_fichparam)
#     
# def setParametres(doc):
#     pass

##########################################################################################
# chargerParametres(getParametres().keys(), 
#                   os.path.splitext(os.path.basename(__file__))[0], 
#                   os.path.join(util_path.PATH, nom_fichparam))
    

