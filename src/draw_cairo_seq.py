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

## Copyright (C) 2011 Cédrick FAURY

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

'''
Created on 26 oct. 2011

@author: Cedrick
'''

from draw_cairo import *
#import textwrap
#from math import sqrt, pi, cos, sin
#import cairo


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

#
# Données pour le tracé
#

# Marges
margeX = 0.02 * COEF
margeY = 0.03 * COEF

# Ecarts
ecartX = 0.02 * COEF
ecartY = 0.02 * COEF

# CI
tailleCI = (0.17 * COEF, 0.085 * COEF)
#posCI = (posPre[0] + taillePre[0]+ecartX, 0.1)
posCI = (margeX, margeY)
IcoulCI = (0.9, 0.8, 0.8, 0.85)
BcoulCI = (0.3, 0.2, 0.25, 1)
fontCI = 0.014 * COEF

# Rectangle des prerequis
taillePre = (0.28 * COEF, 0.18 * COEF - tailleCI[1] - ecartY)
posPre = (margeX, posCI[1] + tailleCI[1] + ecartY)
IcoulPre = (0.8, 0.8, 0.9, 0.85)
BcoulPre = (0.2, 0.25, 0.3, 1)
fontPre = 0.014 * COEF

# Position dans l'année
posPos = [None, margeY - ecartY/2]
taillePos = [None, 0.04 * COEF]

# Rectangle des objectifs
posObj = (posPre[0] + taillePre[0] + ecartX/2, margeY + taillePos[1] + ecartY/2)
tailleObj = [LargeurTotale - margeX - posObj[0], posPre[1] + taillePre[1] - posObj[1]]
IcoulObj = (0.8, 0.9, 0.8, 0.85)
BcoulObj = (0.25, 0.3, 0.2, 1)
fontObj = 0.014 * COEF

# Cible
posCib = [posCI[0] + tailleCI[0] + ecartX/4, margeY - ecartY/2]
tailleCib = [posObj[0] - posCI[0] - tailleCI[0] - ecartX/2, None]
tailleCib[1] = tailleCib[0] 
IcoulCib = (0.8, 0.8, 1, 0.85)
BcoulCib = (0.1, 0.1, 0.25, 1)
centreCib = (posCib[0] + tailleCib[0] / 2 + 0.0006 * COEF, 
             posCib[1] + tailleCib[1] / 2 - 0.0015 * COEF)

# Zone de commentaire
fontIntComm = 0.01* COEF
posComm = [margeX, None]
tailleComm = [LargeurTotale-2*margeX, None]
intComm = []

# Zone d'organisation de la séquence (intérieur du grand cadre vert - bordure)
bordureZOrganis = 0.01 * COEF
posZOrganis = (margeX+bordureZOrganis, 0.24 * COEF)
tailleZOrganis = [LargeurTotale-2*(margeX+bordureZOrganis), None]


# # Rectangle de l'intitulé
# tailleIntitule = [0.4 * COEF, 0.04 * COEF]
# posIntitule = [(LargeurTotale-tailleIntitule[0])/2, posZOrganis[1]-tailleIntitule[1]]
IcoulIntitule = (0.98, 0.99, 0.98, 0.8)
BcoulIntitule = (0.2, 0.8, 0.2, 1)
FontIntitule = 0.02 * COEF

# Zone de déroulement de la séquence
posZDeroul = (margeX+ecartX/2, posZOrganis[1]+0.06 * COEF)
tailleZDeroul = [None, None]

# Zone du tableau des Systèmes
posZSysteme = [None, posZOrganis[1]+0.01 * COEF]
tailleZSysteme = [None, None]
wColSysteme = 0.025 * COEF
xSystemes = {}

# Zone du tableau des démarches
posZDemarche = [None, posZSysteme[1]]
tailleZDemarche = [0.02 * COEF, None]
# xDemarche = {"I" : None,
#              "R" : None,
#              "P" : None}

# Zone des intitulés des séances
fontIntSeances = 0.01 * COEF
posZIntSeances = [0.06 * COEF, None]
tailleZIntSeances = [LargeurTotale-0.12 * COEF, None]
hIntSeance = 0.02 * COEF
intituleSeances = []

# Zone des séances
largeFlecheDuree = 0.02 * COEF
posZSeances = (posZDeroul[0] + largeFlecheDuree, posZOrganis[1]+0.08 * COEF)
tailleZSeances = [None, None]
# wEff =  {"C" : None,
#          "G" : None,
#          "D" : None,
#          "E" : None,
#          "P" : None,
#          "I" : None
#          }
#hHoraire = None
ecartSeanceY = None
BCoulSeance = {"ED" : (0.3,0.5,0.5), 
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

ICoulSeance = {"ED" : (0.6, 0.8, 0.8), 
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

BStylSeance = {"ED" : [], 
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


# paramètres pour la fonction qui calcule la hauteur des tâches 
# en fonction de leur durée
a = b = None
def calcH(t):
    return a*t+b


######################################################################################  
def DefinirZones(seq, ctx):
    """ Calcule les positions et dimensions des différentes zones de tracé
        en fonction du nombre d'éléments (séances, systèmes)
    """
    global wEff, a, b , ecartSeanceY, intituleSeances, fontIntSeances, fontIntComm, intComm
    #hHoraire
    # Zone de commentaire
    if seq.commentaires == "":
        tailleComm[1] = 0
    else:
        tailleComm[1], intComm = calc_h_texte(ctx, "Commentaires : " + seq.commentaires, tailleComm[0], fontIntComm)

    posComm[1] = 1 * COEF - tailleComm[1] - margeY
    
    # Zone d'organisation de la séquence (grand cadre)
    tailleZOrganis[1] = posComm[1]-posZOrganis[1]-bordureZOrganis

#     # Rectangle de l'intitulé
#     posIntitule[1] = posZOrganis[1]-tailleIntitule[1]

    # Zone des intitulés des séances
#    print "Zone des intitulés des séances"
    #                  titres    contenus    hauteurs de ligne
    intituleSeances = [[],      [],         []]
    tailleZIntSeances[1] = 0
    
    intituleSeances[0], lstInt = seq.GetIntituleSeances()
    for intS in lstInt:
        h, t = calc_h_texte(ctx, intS, tailleZIntSeances[0], fontIntSeances)
        intituleSeances[2].append(h)
        intituleSeances[1].append(t)
#        intituleSeances.append([intS[0],h,t])
        tailleZIntSeances[1] += h
    

#    tailleZIntSeances[1] = len(seq.GetIntituleSeances()[0])* hIntSeance
    posZIntSeances[1] = posZOrganis[1] + tailleZOrganis[1] - tailleZIntSeances[1]
    
    # Zone du tableau des Systèmes
    systemes = seq.GetSystemesUtilises(niveau = 0)
    tailleZSysteme[0] = wColSysteme * len(systemes)
    tailleZSysteme[1] = tailleZOrganis[1] - ecartY - tailleZIntSeances[1]
    posZSysteme[0] = posZOrganis[0] + tailleZOrganis[0] - tailleZSysteme[0]
    for i, s in enumerate(systemes):
        xSystemes[s.nom] = posZSysteme[0] + (i+0.5) * wColSysteme
    
    
    # Zone du tableau des démarches
    if len(seq.classe.GetReferentiel().listeDemarches) > 0:
        tailleZDemarche[0] = 0.02 * COEF
        posZDemarche[0] = posZSysteme[0] - tailleZDemarche[0] - ecartX/2
        tailleZDemarche[1] = tailleZSysteme[1]
#         xDemarche["I"] = posZDemarche[0] + tailleZDemarche[0]/6
#         xDemarche["R"] = posZDemarche[0] + tailleZDemarche[0]*3/6
#         xDemarche["P"] = posZDemarche[0] + tailleZDemarche[0]*5/6
    else:
        tailleZDemarche[0] = 0
        tailleZDemarche[1] = tailleZSysteme[1]
        posZDemarche[0] = posZSysteme[0] - tailleZDemarche[0] - ecartX/2
                 
    # Zone de déroulement de la séquence
    tailleZDeroul[0] = posZDemarche[0] - posZDeroul[0] - ecartX/2
    tailleZDeroul[1] = tailleZOrganis[1] - posZDeroul[1] + posZOrganis[1] - ecartY/2
    
    
    # Zone des séances
    tailleZSeances[0] = tailleZDeroul[0] - ecartX# - largeFlecheDuree - ecartX - bordureZOrganis#0.05 # écart pour les durées
    tailleZSeances[1] = tailleZSysteme[1] - posZSeances[1] + posZDeroul[1] - 0.05 * COEF
    wEff = {"C" : tailleZSeances[0],
             "G" : tailleZSeances[0]*6/7,
             "D" : tailleZSeances[0]*3/7,
             "E" : tailleZSeances[0]/seq.classe.nbrGroupes['E']*6/7,
             "P" : tailleZSeances[0]/seq.classe.nbrGroupes['P']*6/7,
             "I" : tailleZSeances[0]
#             "E" : tailleZSeances[0]*Effectifs["E"][1]/Effectifs["G"][1]*6/7,
#             "P" : tailleZSeances[0]*Effectifs["P"][1]/Effectifs["G"][1]*6/7,
             }
    
#    print "durées :"
    ecartSeanceY = 0.006 * COEF    # écart mini entre deux séances
    hmin = 0.016   * COEF           # hauteur minimum d'une séance
    tmin = seq.GetDureeGraphMini() # durée minimale de séance
    n = len(seq.seances)
    d = seq.GetDureeGraph()- n*tmin
#    print "   ", seq.GetDureeGraphMini()
    
    if d == 0:
        a = 0
        b = (tailleZSeances[1] - ecartSeanceY*(n-1)) / n
    else:
        a = (tailleZSeances[1] - ecartSeanceY*(n-1) - n*hmin) / d
        if a < 0:
            a = 0
            b = (tailleZSeances[1] - ecartSeanceY*(n-1)) / n
        else:
            b = hmin - a * tmin
            if b < 0:
                a = (tailleZSeances[1] - (n-1)*ecartSeanceY) / seq.GetDureeGraph()
                b = 0
#    print "   ", a, b
    
#    hHoraire = tailleZSeances[1] / (seq.GetDureeGraph() + 0.25*(len(seq.seances)-1))
#    print "hHoraire", hHoraire
#    print "d =", d
#    print "a, b =", a, b
#    print tailleZSeances[1]
#    print seq.GetDureeGraph()
#    print n
#    print tmin
#    print "a,b = ", a,b
#    hHoraire = tailleZSeances[1] / (seq.GetDureeGraph() + 0.25*(len(seq.seances)-1))
#    ecartSeanceY = hHoraire/4
#    if ecartSeanceY > 0.02:
#        ecartSeanceY = 0.02
#        hHoraire = (tailleZSeances[1] - (len(seq.seances)-1)*ecartSeanceY) / seq.GetDureeGraph()


######################################################################################
curseur = None 
def InitCurseur():
    global cursY
#    curseur = [posZSeances[0], posZSeances[1]]
    cursY = posZSeances[1]
    
    
######################################################################################  
def Draw(ctx, seq, mouchard = False, entete = False):
    """ Dessine une fiche de séquence de la séquence <seq>
        dans un contexte cairo <ctx>
    """
#    print "Draw séquence"
    InitCurseur()
    
    
    #
    # Options générales
    #
    options = ctx.get_font_options()
    options.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    options.set_hint_style(cairo.HINT_STYLE_NONE)#cairo.HINT_STYLE_FULL)#
    options.set_hint_metrics(cairo.HINT_METRICS_OFF)#cairo.HINT_METRICS_ON)#
    ctx.set_font_options(options)
    
    DefinirZones(seq, ctx)
    
#     gabarit() # génération du gabarit de test

    #
    #    pour stocker des zones caractéristiques (à cliquer, ...)
    #
    seq.zones_sens = [] # zones sensibles pour fiche depuis pySequence
    seq.pt_caract = []  # points caractéristiques pour fiche SVG
    
    
    #
    # Flèche
    #
    rayon = 0.30 * COEF
    alpha0 = 55
    alpha1 = 155
    y = posObj[1]+tailleObj[1] - rayon*sin(alpha0*pi/180)
    fleche_ronde(ctx, LargeurTotale/2, y, rayon, alpha0, alpha1, 0.035 * COEF, 0.06 * COEF, (0.8, 0.9, 0.8, 1))
    
    
    #
    # Cadre et Intitulé de la séquence
    #
    if not entete:
        rect = (posZOrganis[0]-bordureZOrganis, posZOrganis[1], 
                tailleZOrganis[0]+bordureZOrganis*2, tailleZOrganis[1]+bordureZOrganis)
    #    seq.zones_sens.append(Zone([rect], param = "INT"))
        if len(seq.intitule) == 0:
            t = "Séquence sans nom"
        else:
            t = seq.intitule
        seq.pt_caract.append((curve_rect_titre(ctx, t, rect, 
                                               BcoulIntitule, IcoulIntitule, FontIntitule),
                              "Seq"))

    #
    # Domaines
    #
    DrawDomaines(ctx, seq, 
                 (posZSeances[0] + posZOrganis[0]-bordureZOrganis)/2,
                 posZOrganis[1] + ecartY/2)



    #
    # Type d'enseignement
    #
    tailleTypeEns = tailleObj[0]/2
    t = seq.classe.GetLabel()
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_BOLD)
    ctx.set_source_rgb (0.6, 0.6, 0.9)
    
    h = taillePos[1] * 0.8
    show_text_rect(ctx, t, (posObj[0] , posPos[1], tailleTypeEns, h), 
                   va = 'c', ha = 'g', b = 0, orient = 'h', 
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                   coulBord = (0, 0, 0))

    t = seq.classe.GetLabelComplet()
    ctx.set_source_rgb (0.3, 0.3, 0.8)
    show_text_rect(ctx, t, (posObj[0] , posPos[1] + h, tailleTypeEns, taillePos[1] - h), 
                   va = 'c', ha = 'g', b = 0, orient = 'h', 
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False)
    


    #
    # Position dans l'année
    #
    posPos[0] = posPre[0] + taillePre[0] + ecartX + tailleTypeEns
    taillePos[0] =  LargeurTotale - posPos[0] - margeX
    ctx.set_line_width (0.0015 * COEF)
    r = (posPos[0], posPos[1], taillePos[0], taillePos[1])
    
    rects = DrawPeriodes(ctx, r, seq.getRangePeriode(), 
                               seq.classe.referentiel.periodes,
                               tailleTypeEns = tailleTypeEns)
    
    for i, re in enumerate(rects):
        seq.zones_sens.append(Zone([re], param = "POS"+str(i)))
    seq.zones_sens.append(Zone([r], param = "POS"))



    #
    # Etablissement
    #
    if seq.classe.etablissement != "":
        t = seq.classe.etablissement + " (" + seq.classe.ville + ")"
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                          cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, t, (posPos[0] , posPos[1]+taillePos[1], taillePos[0], posObj[1]-posPos[1]-taillePos[1]), 
                       va = 'c', ha = 'g', b = 0.15, orient = 'h', 
                       fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                       coulBord = (0, 0, 0))
    
    
    #
    # Cible ou Logo
    #
    
    # Affichage du Logo
    image(ctx, 
          posCib[0], posCib[1], tailleCib[0], tailleCib[1],
          seq.classe.referentiel.getLogo())

    # Affichage des CI sur la cible
    if seq.classe.referentiel.CI_cible:
        seq.zones_sens.append(Zone([posCib+tailleCib], obj = seq.CI))
#        seq.CI.rect.append(())

        rayons = {"F" : tailleCib[0] * 0.28, 
                  "S" : tailleCib[0] * 0.19, 
                  "C" : tailleCib[0] * 0.1,
                  "_" : tailleCib[0] * 0.45}
        angles = {"M" : 0,
                  "E" : 120,
                  "I" : -120,
                  "_" : -98}

        for i, ci in enumerate(seq.CI.GetCodesCIs()):
            mei, fsc = seq.CI.GetPosCible(i).split("_")
            mei = mei.replace(" ", "")
            fsc = fsc.replace(" ", "")

            # Rayon et angle
            if seq.classe.referentiel.champsInter: # un seul point
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
                        
                pos = (centreCib[0] + ray * sin(ang*pi/180) ,
                       centreCib[1] - ray * cos(ang*pi/180))
    #             boule(ctx, pos[0], pos[1], 0.005 * COEF, 
    #                   color0 = (0.95, 1, 0.9, 1), color1 = (0.1, 0.3, 0.05, 1))
                r = 0.01 * COEF
                image(ctx, pos[0]-r/2, pos[1]-r/2, r, r,
                      constantes.images.impact.GetBitmap())
                
            else:   # plusieurs points
                ray = [rayons[j] for j in fsc]
                ang = [angles[j] for j in mei]
                for a in ang:
                    for r in ray:
                        pos = (centreCib[0] + r * sin(a*pi/180) ,
                               centreCib[1] - r * cos(a*pi/180))
            #             boule(ctx, pos[0], pos[1], 0.005 * COEF, 
            #                   color0 = (0.95, 1, 0.9, 1), color1 = (0.1, 0.3, 0.05, 1))
                        r_ = 0.01 * COEF
                        image(ctx, pos[0]-r_/2, pos[1]-r_/2, r_, r_,
                              constantes.images.impact.GetBitmap())

    #
    # Durée de la séquence
    #
    if not entete:
        ctx.set_source_rgb(0.5,0.8,0.8)
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_BOLD)
        
        
        re = (posZOrganis[0]-bordureZOrganis,
              posZDemarche[1] + tailleZDemarche[1],
              posZSeances[0] - posZOrganis[0] + bordureZOrganis,
              0.015 * COEF)
        
        show_text_rect(ctx, getHoraireTxt(seq.GetDuree()),
                       re,
#                        (posZDeroul[0]-0.01 * COEF, posZDemarche[1] + tailleZDemarche[1] , #- 0.015
#                         0.1 * COEF, 0.015 * COEF),
                       ha = 'c', b = 0.1)




    #
    # Commentaires
    #
    if not entete:
        if tailleComm[1] > 0:
            ctx.set_source_rgb(0.1,0.1,0.1)
            ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                                              cairo.FONT_WEIGHT_NORMAL)
            ctx.set_font_size(fontIntComm)
            _x, _y = posComm
            fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
            #
            # On dessine toutes les lignes de texte
            #
            for i, t in enumerate(intComm):
                yt = _y + (fascent+fdescent)*i  + fheight #- fdescent
                ctx.move_to(_x, yt)
                ctx.show_text(t)


    # 
    # Effectifs
    #
    if not entete:
        wEff, rects = DrawClasse(ctx, (posZSeances[0], posZDemarche[1],
                                       tailleZSeances[0], posZSeances[1]-posZDemarche[1]-0.01 * COEF),
                                 seq.classe)
        
        for i, e in enumerate(["C", "G", "D", "E", "P"]):
            x = posZSeances[0]
            h = (posZSeances[1]-posZDemarche[1]-0.01 * COEF) / 5
            y = posZDemarche[1] + 4 * h
            w = wEff[e]
            DrawLigneEff(ctx, x+w, y+h, constantes.CouleursGroupes[e])




    def taille(lstTxt):
        return 1.0*sum([len(t) for t in lstTxt])


    #
    #  Prerequis
    #
    
    # Rectangle arrondi
    x0, y0 = posPre
    rect_width, rect_height  = taillePre
    curve_rect_titre(ctx, "Prérequis",  
                     (x0, y0, rect_width, rect_height),
                     BcoulPre, IcoulPre, fontPre)
    
    #
    # Codes prerequis
    #
    lstTexteC = []
    lstCodesC = []
    lstCoulC = []
    
    ref = seq.GetReferentiel()
    if ref.tr_com != []:
        ref_tc = REFERENTIELS[ref.tr_com[0]]
    else:
        ref_tc = None
        
    lstComp = []
    lstTyp = []
    for c in seq.prerequis["C"].competences:
        typ, cod = c[0], c[1:]
        
        if typ == "B" and ref.tr_com != []: # B = tronc commun --> référentiel
            comp = ref_tc.dicoCompetences["S"]
        else:
            if typ in list(ref.dicoCompetences.keys()):
                comp = ref.dicoCompetences[typ]
            elif ref_tc and typ in list(ref_tc.dicoCompetences.keys()):
                comp = ref_tc.dicoCompetences[typ]
        lstComp.append([cod,comp])
        if not typ in lstTyp:
            lstTyp.append(typ)
    
    multi = len(lstTyp) > 1
    
    for cod, comp in lstComp:   
        disc = comp.codeDiscipline
        lstTexteC.append(comp.getCompetence(cod).intitule)
        if multi:
            lstCodesC.append(comp.abrDiscipline + " " + cod)
        else:
            lstCodesC.append(cod)
        lstCoulC.append(constantes.COUL_DISCIPLINES[disc])
        
            
            
    lstTexteS = []
    lstCodesS = []
    lstCoulS = []
    
    ref = seq.GetReferentiel()
    if ref.tr_com != []:
        ref_tc = REFERENTIELS[ref.tr_com[0]]
    else:
        ref_tc = None
        
    lstSav = []
    lstTyp = []
    for c in seq.prerequis["S"].savoirs:
        typ, cod = c[0], c[1:]
        if typ == "B" and ref.tr_com != []: # B = tronc commun --> référentiel
            savoir = ref_tc.dicoSavoirs["S"]
        else:
            if typ in list(ref.dicoSavoirs.keys()):
                savoir = ref.dicoSavoirs[typ]
            elif ref_tc and typ in list(ref_tc.dicoSavoirs.keys()):
                savoir = ref_tc.dicoSavoirs[typ]
        lstSav.append([cod,savoir])
        if not typ in lstTyp:
            lstTyp.append(typ)
    
    lstSav.sort(key = lambda x:x[0])
    
    multi = len(lstTyp) > 1
    
    for cod, savoir in lstSav:
        disc = savoir.codeDiscipline
        lstTexteS.append(savoir.getSavoir(cod).intitule)
        if multi:
            lstCodesS.append(savoir.abrDiscipline+" "+cod)
        else:
            lstCodesS.append(savoir.abrDiscipline+" "+cod)
        lstCoulS.append(constantes.COUL_DISCIPLINES[disc])
        
        
    lstTexteSe = []   
    for c in seq.prerequisSeance:
        lstTexteSe.append(c.GetNomFichier())    
        
    hl = rect_height+0.0001 * COEF
    
    ltot = taille(lstTexteC) + taille(lstTexteS) + taille(lstTexteSe)
    if ltot > 0:
#         hC = hl*len(lstTexteC)/(ltot)
#         hS = hl*len(lstTexteS)/(ltot)
#         hSe = hl*len(lstTexteSe)/(ltot)
#         wC = rect_width
#         wS = rect_width
#         wSe = rect_width
        
        wC = rect_width*taille(lstTexteC)/(ltot)
        wS = rect_width*taille(lstTexteS)/(ltot)
        wSe = rect_width*len(lstTexteSe)/(ltot)
        rectC = (x0, y0, wC, hl)
        rectS = (x0+wC, y0, wS, hl)
        rectSe = (x0+wC+wS, y0, wSe, hl)
        
        
        
        r = liste_code_texte(ctx, lstCodesC, lstTexteC, 
                             rectC, 
                             0.05*rect_width, 0.1,
                             lstCoul = lstCoulC, va = 'c')
        ctx.set_source_rgba (0.0, 0.0, 0.5, 1.0)
        seq.prerequis["C"].pts_caract = getPts(r)
#         print("prerequis C", getPts(r))
        for i, c in enumerate(seq.prerequis["C"].competences): 
            seq.zones_sens.append(Zone([r[i]], obj = seq.prerequis["C"]))
#             seq.prerequis["C"].pt_caract = (r[i][:2], i)

        
        
        
        r = liste_code_texte(ctx, lstCodesS, lstTexteS, 
                             rectS, 
                             0.05*rect_width, 0.1,
                             lstCoul = lstCoulS, va = 'c')
        ctx.set_source_rgba (0.0, 0.0, 0.5, 1.0)
        seq.prerequis["S"].pts_caract = getPts(r)
#         print("prerequis S", getPts(r))
        for i, c in enumerate(seq.prerequis["S"].savoirs): 
            seq.zones_sens.append(Zone([r[i]], obj = seq.prerequis["S"]))
#             seq.prerequis["S"].pt_caract = (r[i][:2], i)
        
            
        lstRect = liste_code_texte(ctx, ["Seq."]*len(lstTexteSe), lstTexteSe, 
                                   rectSe, 
                                   0.05*rect_width, 0.1, va = 'c')
        for i, c in enumerate(seq.prerequisSeance):
            seq.zones_sens.append(Zone([lstRect[i]], obj = c))
            
    else:
        show_text_rect(ctx, "Aucun", (x0, y0, rect_width, hl), fontsizeMinMax = (-1, 0.015 * COEF))
        seq.zones_sens.append(Zone([(x0, y0, rect_width, hl)], obj = seq.prerequis["S"]))






    ##################################################################################
    #  Objectifs
    #
    x0, y0 = posObj
#    tailleObj[0] =  taillePos[0]
    rect_width, rect_height  = tailleObj
    curve_rect_titre(ctx, ref.labels["OBJEC"][2].plur_(),#"Objectifs", 
                     (x0, y0, rect_width, rect_height), 
                     BcoulObj, IcoulObj, fontObj)
                          
    
    
    
    #
    # Codes objectifs
    #
    lstTexteC = []
    lstCodesC = []
    lstCoulC = []
    ref = seq.GetReferentiel()
#     print(seq.GetObjAffiches())
    ref_tc = None
    if ref.tr_com != []:
        ref_tc = REFERENTIELS[ref.tr_com[0]]
        
    lstComp = []
    lstTyp = []
    for c in seq.GetObjAffiches():#obj["C"].competences:
        typ, cod = c[0], c[1:]
        comp = None
#         print "typ, cod =", typ, cod
        if typ == "B" and ref.tr_com != []: # B = tronc commun --> référentiel
            comp = ref_tc.dicoCompetences["S"]
        else:
            if typ in list(ref.dicoCompetences.keys()):
                comp = ref.dicoCompetences[typ]
            elif ref_tc and typ in list(ref_tc.dicoCompetences.keys()):
                comp = ref_tc.dicoCompetences[typ]
        lstComp.append([cod,comp])
        if not typ in lstTyp:
            lstTyp.append(typ)
    
    multi = len(lstTyp) > 1
    
    lstComp.sort(key = lambda x:x[0])
    
    for cod, comp in lstComp:    
        disc = comp.codeDiscipline
        
        lstTexteC.append(comp.getCompetence(cod).intitule)
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
    for c in seq.obj["S"].savoirs:
        typ, cod = c[0], c[1:]
        if typ == "B" and ref.tr_com != []: # B = tronc commun --> référentiel
            savoir = ref_tc.dicoSavoirs["S"]
        else:
            if typ in list(ref.dicoSavoirs.keys()):
                savoir = ref.dicoSavoirs[typ]
            elif ref_tc and typ in list(ref_tc.dicoSavoirs.keys()):
                savoir = ref_tc.dicoSavoirs[typ]
        lstSav.append([cod,savoir])
        if not typ in lstTyp:
            lstTyp.append(typ)
    
    multi = len(lstTyp) > 1
    
    for cod, savoir in lstSav:
        disc = savoir.codeDiscipline
        
        lstTexteS.append(savoir.getSavoir(cod).intitule)
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
        ctx.set_font_size(maxFontSize)
        f = ctx.font_extents()[2]
        rectC = reduire_rect(x0, y0, wC, h, f, 0.2)
        rectS = reduire_rect(x0+wC, y0, wS, h, f, 0.2)
        
        ctx.set_source_rgba (*BcoulObj)
        ctx.move_to(x0+wC, y0)
        ctx.line_to(x0+wC, y0+h)
        ctx.stroke()
        
        ctx.set_source_rgba (*COUL_COMPETENCES)
        r = liste_code_texte2(ctx, lstCodesC, lstTexteC, 
                             rectC, 
                             0.03*rect_width, 0.1, 
                             lstCoul = lstCoulC, va = 'c') 
        seq.obj["C"].pts_caract = getPts(r)
        
        ctx.set_source_rgba (0.0, 0.0, 0.0, 1.0)
#        r = liste_code_texte(ctx, [s[1:] for s in seq.obj["S"].savoirs], 
#                             lstTexteS, x0, y0+hC, rect_width, hS, 0.008)
        r = liste_code_texte2(ctx, lstCodesS, lstTexteS, 
                             rectS, 
                             0.03*rect_width, 0.1, 
                             lstCoul = lstCoulS, va = 'c')
        seq.obj["S"].pts_caract = getPts(r)
    
        seq.zones_sens.append(Zone([rectC], obj = seq.obj["C"]))
        
        
        
        seq.zones_sens.append(Zone([rectS], obj = seq.obj["S"]))
#    seq.obj["C"].rect = 
#    seq.obj["S"].rect = [(x0, y0+hC, rect_width, hS)]
    





    #################################################################################
    #  CI
    #
    Draw_CI(ctx, seq.CI, seq)




    
    #################################################################################
    #  Séances
    #
    if not entete:
        for s in seq.seances:
    #        Draw_seance(ctx, s, curseur)
            DrawSeanceRacine(ctx, s)
        
    #
    #  Tableau des systèmes
    #    
    if not entete:
        nomsSystemes = []
        systemes = seq.GetSystemesUtilises()
        for s in systemes:
            nomsSystemes.append(s.nom)
        
        if nomsSystemes != []:
            ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_NORMAL)
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(0.001 * COEF)
            tableauV(ctx, nomsSystemes, posZSysteme[0], posZSysteme[1], 
                    tailleZSysteme[0], posZSeances[1] - posZSysteme[1], 
                    0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', coul = (0.8,0.8,0.8))
            
            wc = tailleZSysteme[0]/len(nomsSystemes)
            _x = posZSysteme[0]
            _y = posZSysteme[1]
            for s in systemes:
    #            s.rect=((_x, _y, wc, posZSeances[1] - posZSysteme[1]),)
                seq.zones_sens.append(Zone([(_x, _y, wc, posZSeances[1] - posZSysteme[1])],
                                           obj = s))
                ctx.set_source_rgb(0, 0, 0)
                ctx.move_to(_x, _y + posZSeances[1] - posZSysteme[1])
                ctx.line_to(_x, _y + tailleZDemarche[1])
                ctx.stroke()
                
                ctx.set_source_rgba(0.8,0.8,0.8, 0.2)
                ctx.rectangle(_x, _y+ posZSeances[1] - posZSysteme[1], 
                              wc, tailleZDemarche[1]-posZSeances[1] + posZSysteme[1])
                ctx.fill()
                _x += wc
            ctx.set_source_rgb(0, 0, 0)
            ctx.move_to(_x, _y + posZSeances[1] - posZSysteme[1])
            ctx.line_to(_x, _y + tailleZDemarche[1])   
            ctx.stroke()


    #
    #  Tableau des démarches
    #
    if not entete:
        if len(seq.GetReferentiel().listeDemarches) > 0:
            ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_NORMAL)
            ctx.set_source_rgb(0, 0, 0)
            show_text_rect(ctx, "Démarche",
                           (posZDemarche[0], posZDemarche[1],
                            tailleZDemarche[0], posZSeances[1] - posZSysteme[1]), \
                   va = 'h', ha = 'g', le = 0.8, pe = 1.0, \
                   b = 0.3, orient = 'v', \
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False, 
                   coulBord = None, tracer = True, ext = "...")
            
            
#             ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
#                                   cairo.FONT_WEIGHT_NORMAL)
#             ctx.set_source_rgb(0, 0, 0)
#             ctx.set_line_width(0.001 * COEF)
#             l=[]
#             for d in seq.GetReferentiel().listeDemarches : 
#                 l.append(seq.GetReferentiel().demarches[d][0])
#             tableauV(ctx, l, posZDemarche[0], posZDemarche[1], 
#                     tailleZDemarche[0], posZSeances[1] - posZSysteme[1], 
#                     0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', coul = (0.8,0.75,0.9))
#             ctx.move_to(posZDemarche[0], posZDemarche[1] + posZSeances[1] - posZSysteme[1])
#             ctx.line_to(posZDemarche[0], posZDemarche[1] + tailleZDemarche[1])
#             ctx.move_to(posZDemarche[0]+tailleZDemarche[0]/3, posZDemarche[1] + posZSeances[1] - posZSysteme[1])
#             ctx.line_to(posZDemarche[0]+tailleZDemarche[0]/3, posZDemarche[1] + tailleZDemarche[1])
#             ctx.move_to(posZDemarche[0]+tailleZDemarche[0]*2/3, posZDemarche[1] + posZSeances[1] - posZSysteme[1])
#             ctx.line_to(posZDemarche[0]+tailleZDemarche[0]*2/3, posZDemarche[1] + tailleZDemarche[1])
#             ctx.move_to(posZDemarche[0]+tailleZDemarche[0], posZDemarche[1] + posZSeances[1] - posZSysteme[1])
#             ctx.line_to(posZDemarche[0]+tailleZDemarche[0], posZDemarche[1] + tailleZDemarche[1])
#             ctx.stroke()



    #
    #  Tableau des séances (en bas)
    #
    if not entete:
        if intituleSeances[0] != []:
            ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_NORMAL)
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(0.001 * COEF)
            tableauH_var(ctx, intituleSeances[0], posZIntSeances[0], posZIntSeances[1], 
                    0.05* COEF, tailleZIntSeances[0]-0.05 * COEF, intituleSeances[2], fontIntSeances, 
                    nCol = 1, va = 'c', ha = 'g', orient = 'h', coul = ICoulSeance, 
                    contenu = [intituleSeances[1]])
        
    #
    # Informations
    #
    if not entete:
        info(ctx, margeX, margeY)
    
    



######################################################################################  
def DrawLigneEff(ctx, x, y, coul):
    dashes = [ 0.010 * COEF,   # ink
               0.002 * COEF,   # skip
               0.005 * COEF,   # ink
               0.002 * COEF,   # skip
               ]
    ctx.set_source_rgba (*coul)
    ctx.set_line_width (0.001 * COEF)
    ctx.set_dash(dashes, 0)
    ctx.move_to(x, posZDemarche[1] + tailleZDemarche[1])
    ctx.line_to(x, y)
    ctx.stroke()
    ctx.set_dash([], 0)


    
######################################################################################  
def H_code():
    """ Renvoie la hauteur des codes de séance
    """  
    return max(ecartY/4, 0.01 * COEF)
            
              
######################################################################################  
def Draw_CI(ctx, CI, seq):
    # Rectangle arrondi
    x0, y0 = posCI
    rect_width, rect_height  = tailleCI
    
    ref = CI.GetReferentiel()
    
    if len(CI.numCI)+len(CI.CI_perso) > 1:
        t = ref._nomCI.Plur_()
    else:
        t = ref._nomCI.Sing_()
    
    rect = (x0, y0, rect_width, rect_height)
    CI.pt_caract = (curve_rect_titre(ctx, t, rect, BcoulCI, IcoulCI, fontCI), 
                    'CI')
    seq.zones_sens.append(Zone([rect], obj = CI))
#    CI.rect.append()
    
    
    
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
            r = liste_code_texte(ctx, lstCodes, lstIntit, 
                                 (x0, y0+0.0001 * COEF, rect_width, hCI), 
                                 0.05*rect_width, 0.1, va = 'c')
            CI.pts_caract = getPts(r)
        
        ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                                           cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, "\n".join(lstPb), 
                       (x0, y0+0.0001 * COEF + hCI, rect_width, hPb)
                       )




######################################################################################  
class Cadre():  
    """ Plus petit élément de séance :
         - 1 cadre
         - 1 code
         - 1 intitulé
    """
    def __init__(self, ctx, seance, h, filigrane = False, signEgal = False): 
        self.seance = seance
        self.ctx = ctx
        self.w = wEff[seance.effectif]
        self.h = h
        self.filigrane = filigrane
        self.xd = None
        self.y = None   # Position en Y du cadre
        self.dy = None  # Position en Y relative de la ligne
        self.nf = 0     # Nombre de "frères" (pour calcul rayon boule
#        self.seance.rect = []
        self.signEgal = signEgal
        
    def __repr__(self):
        return self.seance.code
    
    def Draw(self, x, y):
        """ Dessine le cadre à la position (x,y)
        """
        if self.filigrane:
            alpha = 0.2
        else:
            alpha = 1
            self.seance.pts_caract.append((x, y))
#         print(self.seance, (x, y))
        #
        # Le cadre
        #
        epaisseurTrait = 0.002 * COEF
        self.ctx.set_line_width(epaisseurTrait)
        self.ctx.set_dash(BStylSeance[self.seance.typeSeance], 0)
        rectangle_plein(self.ctx, x, y, self.w, self.h, 
                        BCoulSeance[self.seance.typeSeance], ICoulSeance[self.seance.typeSeance], alpha)
        self.ctx.set_dash([], 0)
        
        wc = 0
        #
        # Le code (en haut à gauche)
        #
        if hasattr(self.seance, 'code'):
            self.ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
            c = self.seance.couleur
            self.ctx.set_source_rgba (c[0], c[1], c[2], alpha)
#            hc = max(hHoraire/4, 0.01)
            hc = H_code()
            f, r = show_text_rect(self.ctx, self.seance.code, (x, y, wEff["P"], hc), ha = 'g', 
                                      wrap = False, fontsizeMinMax = (minFont, -1), b = 0.2)
            
            wc = r[2] + ecartX/2
        
        #
        # L'intitulé (si intituleDansDeroul)
        #
        if self.seance.intituleDansDeroul and self.seance.intitule != "" and self.h-hc > 0:#not self.filigrane and 
            self.ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                                  cairo.FONT_WEIGHT_NORMAL)
            self.ctx.set_source_rgba (0,0,0, alpha)
#            print (x, y + hc, self.w, self.h-hc)
#            print (wc, y, self.w - (wc-x), self.h)
#            print 
            if self.h < 0.02 * COEF: # h petit -> on écrit à coté du code !
                rct = (wc, y, self.w - (wc-x), self.h)
            else:
                rct = (x, y + hc, self.w, self.h-hc)

            show_text_rect(self.ctx, self.seance.intitule, rct, 
                           ha = 'g', b = 0.2, fontsizeMinMax = (minFont, 0.015 * COEF), 
                           fontsizePref = self.seance.taille.v[0])
        
        #
        # L'intitulé (si intituleDansDeroul)
        #
        if  self.signEgal:# not self.filigrane and
            dx = wEff["P"]/16
#            dy = hHoraire/32
            dy = b/4
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
        
        self.seance.GetDocument().zones_sens.append(Zone([(x, y, self.w, self.h)], obj = self.seance))
#        self.seance.rect.append([x, y, self.w, self.h])
        
        return x + self.w, y + self.h




######################################################################################  
class Bloc():
    """ Ensemble de cadres.
        contenu = [[], [], ...]
        lignes
    """
    def __init__(self):
        self.contenu = []
        self.x = None
        self.y = None
        
    
    def Draw(self, x, y):
#        print self.contenu
        self.x = x
        self.y = y
        for ligne in self.contenu:
#            print 
            x = self.x
#            x = posZSeances[0]
            for elem in ligne:
#                print "  > ", elem
                if isinstance(elem, Cadre):
                    xf, yf = elem.Draw(x, y)
                    
                elif isinstance(elem, Bloc):
                    xf, yf = elem.Draw(x, y)
                    
                x = xf
                    
            if len(ligne) > 0:
                y = yf

        return x, y
    
    
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
                            DrawLigne(cadre.ctx, 
                                      cadre.xd, cadre.y + cadre.dy, 
                                      cadre.seance.couleur)
    
                        #
                        # L'icone "démarche"
                        #
                        r = min(tailleZDemarche[0], cadre.h/(cadre.nf+1))
                        if len(cadre.seance.GetReferentiel().listeDemarches) > 0:
                            DrawCroisementsDemarche(cadre.ctx, cadre.seance, cadre.y + cadre.dy, r)
                        
                        
                        #
                        # Le rond "nombre de systèmes nécessaires"
                        #
                        r = min(wColSysteme, cadre.h/(cadre.nf+1))
                        if not estRotation: # Cas des rotations traité plus bas ...
                            DrawCroisementSystemes(cadre.ctx, cadre.seance, cadre.xd, cadre.y + cadre.dy, 
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
                    r = min(wColSysteme, cadreOk.h/(cadreOk.nf+1)/3)
                    DrawCroisementSystemes(cadreOk.ctx, cadreOk.seance, cadre.xd, cadreOk.y + cadreOk.dy,
                                           NS, r)
            



######################################################################################  
def DrawSeanceRacine(ctx, seance):
    global cursY
#    if seance.GetDureeGraph() == 0:
#        return
        
    #
    # Flèche indiquant la durée
    #
    h = calcH(seance.GetDureeGraph())
    if seance.GetDureeGraph() > 0:
        
        e = largeFlecheDuree
        fleche_verticale(ctx, posZDeroul[0]+e/4, cursY, 
                         h, e, (0.9,0.8,0.8,0.5))
        ctx.set_source_rgb(0.5,0.8,0.8)
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
        he = min(e/2, h/3)
        
        if h-he < e:
            o = 'h'
        else:
            o = 'v'
        show_text_rect(ctx, getHoraireTxt(seance.GetDuree()), 
                       (posZDeroul[0]-e/4, cursY, e, h-he), 
                       orient = o, b = 0.2)

    

    #
    # Remplissage du tableau de blocs : [[], [], ...]
    #
    def getBloc(seance, h, filigrane = False, decal = 0, nbr = 0, rotation = False):
        # Séance "simple" --> un seul bloc d'une ligne de un ou plusieurs cadres 
        if not seance.typeSeance in ["R", "S", ""]:
            bloc = Bloc()
            seance.pts_caract = []
#            if seance.typeSeance in ["AP", "ED", "P"]:
            l = []
            if rotation:
                n = 1
            else:
                n = int(seance.nombre.v[0])
            for i in range(n):
                l.append(Cadre(ctx, seance, h, signEgal = (i>0), filigrane = filigrane))
            bloc.contenu.append(l)
            hc = H_code()
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
            
            
        # Séance "complexe"    
        else:
            # Rotation : plusieurs lignes
            if seance.typeSeance == "R":           
                bloc = Bloc()
                l0 = seance.GetListSousSeancesRot() # Liste des sous séances de la première colonne (têtes de ligne - foncé)
#                print "l0 =", l0
                for ss in l0[:seance.nbrRotations.v[0]]:
#                for i in range(seance.nbrRotations.v[0]):
#                    ss = seance.seances[i]
                    hl = h * ss.GetDuree()/seance.GetDuree() * len(l0)/  seance.nbrRotations.v[0] 
                    bloc.contenu.append([getBloc(ss, hl, rotation = True)])
                    
                #
                # Aperçu en filigrane de la rotation
                #
                if True:#seance.IsEffectifOk() <= 3:
                    l = seance.GetListSousSeancesRot(True)
#                    print "  l =", l
                    for t in range(len(l)-1): # Colonnes
                        l = permut(l)
#                        print "   ", l
                        for i, ss in enumerate(l[:seance.nbrRotations.v[0]]):   # Lignes
                            hl = h * ss.GetDuree()/seance.GetDuree() * len(l0)/  seance.nbrRotations.v[0] 
                            bloc.contenu[i].extend([getBloc(ss, hl, filigrane = True, rotation = True)])
#                blocs.extend(bloc)
#                print "   >>", bloc.contenu
                return bloc
                
            elif seance.typeSeance == "S":
                n = len(seance.seances)
                bloc = Bloc()
                bloc.contenu.append([])
#                bloc.contenu.append(getLigne(seance, h))
                for j, ss in enumerate(seance.seances):
                    bloc.contenu[0].append(getBloc(ss, h*ss.GetDuree()/seance.GetDuree(), 
                                                   decal = 1.0*(j+1)/(len(seance.seances)+1),
                                                   nbr = len(seance.seances)))
                
                return bloc
            
            return Bloc()
        return Bloc()

    bloc = getBloc(seance, h)
    
#    print "bloc :", bloc
#    print "  ", cursY,
#    y = cursY
    x, cursY = bloc.Draw(posZSeances[0], cursY)
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
    cursY += ecartSeanceY






######################################################################################  
def DrawCroisementSystemes(ctx, seance, x, y, ns, w):
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
    
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_BOLD)

    for s, n in list(ns.items()):
        if n > 0 and s in list(xSystemes.keys()):
            x = xSystemes[s]
            rect = (x-w/2, y-w/2, w, w)
            ctx.rectangle(*rect)
            ctx.set_source_rgba(1,1,1, 0.5)
            ctx.fill()
            ctx.set_source_rgba(*seance.couleur)
            show_text_rect(ctx, str(n), rect,
                           wrap = False, couper = False)
            
            seance.GetDocument().zones_sens.append(Zone([rect],
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
#                 seance.GetDocument().zones_sens.append(Zone([(x-r, y-r, 2*r, 2*r)],
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
#                 seance.GetDocument().zones_sens.append(Zone([(x-wColSysteme/2, y-r, wColSysteme, 2*r)],
#                                                                  obj = seance))
#                 
# #                seance.rect.append((x-wColSysteme/2, y-r, wColSysteme, 2*r))
        
        



######################################################################################  
def DrawLigne(ctx, x, y, c = (0, 0.0, 0.2, 0.6)):
    dashes = [ 0.010 * COEF,   # ink
               0.002 * COEF,   # skip
               0.005 * COEF,   # ink
               0.002 * COEF,   # skip
               ]
    
    ctx.set_source_rgba (c[0], c[1], c[2], 0.5)
    ctx.set_line_width (0.0006 * COEF)
    ctx.set_dash(dashes, 0)
    ctx.move_to(posZOrganis[0]+tailleZOrganis[0], y)
    ctx.line_to(x, y)
    ctx.stroke()
    ctx.set_dash([], 0)
          

#####################################################################################  
def DrawCroisementsDemarche(ctx, seance, y, w):
        
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
                rect =    (posZDemarche[0] + dx, y - w/2 + dx, w, w)
                image(ctx, posZDemarche[0] + dx, y - w/2 + dx, w, w, bmp, marge = 0.1)
#     _x = xDemarche[seance.demarche]
# #        if self.typeSeance in ["AP", "ED", "P"]:
# #    r = 0.008 * COEF
#     boule(ctx, _x, y, r)
    
            seance.GetDocument().zones_sens.append(Zone([rect], obj = seance))
    
    
#    seance.rect.append((_x -r , y - r, 2*r, 2*r))


#####################################################################################  
def DrawDomaines(ctx, seq, x, y, r = 0.008 * COEF):
    """ Tracé des logos des Domaines
        x : centre de la zone
        y : haut de la zone
    """
    p = 0.8
    ctx.set_line_width (0.0006 * COEF)
    y += r
    
    def draw(x, y, t, c):
        ctx.set_source_rgba (c[0]/3, c[1]/3, c[2]/3, 0.4)
        ctx.arc(x, y, r, 0, 2*pi)
        ctx.fill_preserve ()
        ctx.set_source_rgba (c[0], c[1], c[2], 1)
        show_text_rect(ctx, t, (x-r, y-r, 2*r, 2*r),
                               wrap = False, couper = False)
        ctx.stroke ()
    
    dx = p*r
    dy = p*r*1.732
    
    ref = seq.GetReferentiel()
    for i, d in enumerate(seq.domaine):
        X = x + [0, -1, 1][i%3]*dx
        c = 2 * (i//3) + (i%3 + 1)//2
        Y = y + c*dy
        draw(X, Y, d, ref.domaines[d][3])
    
    if len(seq.domaine) > 0:
        rect = x-r-dx, y-r, 2*(r+dx), Y-y+2*r
        seq.zones_sens.append(Zone([rect], param = "DOM"))
        
        
        

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



