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

## Copyright (C) 2011-2016 Cédrick FAURY

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

'''
Created on 26 oct. 2011 

@author: Cedrick FAURY
'''
# Pour débuggage
#import time
import sys

#import rsvg
import cairo
import wx.lib.wxcairo
import images

from draw_cairo import LargeurTotale, font_family, curve_rect_titre, show_text_rect, \
                        boule, getHoraireTxt, liste_code_texte, rectangle_plein, barreH, tableauV, minFont, maxFont, tableauH, \
                        DrawPeriodes, DrawCalendrier, COEF, info, Zone, \
                        BcoulPos, IcoulPos, ICoulComp, CoulAltern, ligne, rectangle_plein_biseau, \
                        rectangle_plein_fleche, rectangle_plein_doigt

from math import log, pi


#from constantes import Effectifs, NomsEffectifs, listeDemarches, Demarches, getSavoir, getCompetence, \
#                        DemarchesCourt, estCompetenceRevue
import constantes
from widgets import getSingulier, getPluriel, getSingulierPluriel

# Les constantes partagées
from Referentiel import REFERENTIELS
import Referentiel


## Pour dessiner la cible ...
import os
import tempfile
import wx

#
# Données pour le tracé
#

# Marges
margeX = 0.02 * COEF
margeY = 0.04 * COEF

# Ecarts
ecartX = 0.02 * COEF
ecartY = 0.02 * COEF

# Titre de la progression
tailleNom = (0.29 * COEF, 0.04 * COEF)
posNom = (margeX, margeY)
IcoulNom = (0.85, 0.8, 0.8, 0.85)
BcoulNom = (0.28, 0.2, 0.25, 1)
fontNom = 0.016 * COEF

# Equipe pédagogique
tailleEqu = (0.17 * COEF, 0.07 * COEF)
posEqu = (margeX, posNom[1] + tailleNom[1] + ecartY)
IcoulEqu = (0.8, 0.8, 0.9, 0.85)
BcoulEqu = (0.2, 0.25, 0.3, 1)
fontEqu = 0.012 * COEF

# CI/Thèmes
IcoulCI = (0.9, 0.8, 0.8, 0.85)
BcoulCI = (0.3, 0.2, 0.25, 1)
fontCI = 0.013 * COEF

## Equipe pédagogique
#tailleEqu = (0.17 * COEF, 0.18 * COEF - tailleSup[1]- tailleNom[1] - 3*ecartY/2)
#posEqu = (margeX, posSup[1] + tailleSup[1] + ecartY)
#IcoulEqu = (0.8, 0.8, 0.9, 0.85)
#BcoulEqu = (0.2, 0.25, 0.3, 1)
#fontEqu = 0.011 * COEF

# Position dans l'année
posPos = [None, margeY - ecartY/2]
taillePos = [None, 0.03 * COEF]

# Calendrier
posPro = [posNom[0] + tailleNom[0] + ecartX/2, margeY + taillePos[1] + ecartY/2]
taillePro = [LargeurTotale - margeX - posPro[0], 0.19 * COEF - posPro[1] - ecartY/2]
IcoulPro = (0.8, 0.9, 0.8, 0.85)
BcoulPro = (0.25, 0.3, 0.2, 1)
fontPro = 0.012 * COEF

# Image
posImg = [posEqu[0] + tailleEqu[0] + ecartX/4, posNom[1] + tailleNom[1] + ecartY]
tailleImg = [posPro[0] - posImg[0] - ecartX/4, None]
tailleImg[1] = posEqu[1] + tailleEqu[1] - posEqu[1]
IcoulImg = (0.8, 0.8, 1, 0.85)
BcoulImg = (0.1, 0.1, 0.25, 1)
centreImg = (posImg[0] + tailleImg[0] / 2 + 0.0006 * COEF, posImg[1] + tailleImg[0] / 2 - 0.004 * COEF)

# Zone d'organisation (grand cadre)
posZOrganis = (margeX, 0.19 * COEF)
bordureZOrganis = 0.01 * COEF
tailleZOrganis = (LargeurTotale-2*margeX, 1 * COEF-ecartY-posZOrganis[1]-bordureZOrganis)

# Zone de déroulement du projet
posZDeroul = [margeX, None]
tailleZDeroul = [None, None]
IcoulZDeroul = (1, 1, 0.7, 0.85)
BcoulZDeroul = (0.4, 0.4, 0.03, 1)
fontZDeroul = 0.016 * COEF
wPhases = 0.02 * COEF      # Taille du label "phases"
wDuree = 0.012 * COEF       # Taille de la fleche "duree"



# Zones des tableaux Thématiques
posZThV = [None, posZOrganis[1]]
tailleZThV = [None, None]
posZThH = [posZDeroul[0], posZThV[1]]
tailleZThH = [None, None]
wTh = 0.015 * COEF
hTh = 0.020 * COEF
xTh = []
yTh = []



# Zones des tableaux des CI/thèmes de séquence
posZCIV = [None, None]
tailleZCIV = [None, None]
posZCIH = [posZDeroul[0], None]
tailleZCIH = [None, None]
wCI = 0.010 * COEF
hCI = 0.020 * COEF
xCI = []
yCI = []


# Zone du tableau des compétences
posZComp = [None, None]
tailleZComp = [None, None]
wColCompBase = 0.018 * COEF

xComp = {}
cComp = {}


# Zone des tâches
posZTaches = [posZDeroul[0] + wPhases + wDuree + ecartX*3/6, None]
tailleZTaches = [None, None]
hTacheMini = ecartY
hRevue = ecartY/3
hPeriode = None
# yTaches = []
# ecartTacheY = None  
ecartTacheY = ecartY/3 # Ecartement entre les tâches de phase différente

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

def calcH(t, a, b):
    if t != 0:
        return a*log(t+2)+b
    return hTacheMini

ecartyCITaches = 0.05 * COEF


    
    

######################################################################################  
def DefinirZones(prg, ctx):
    """ Calcule les positions et dimensions des différentes zones de tracé
        en fonction du nombre d'éléments (élèves, tâches, compétences)
    """
    global ecartTacheY, intituleTaches, fontIntTaches, xCI, yCI, hCI, hTh, \
           wColComp, xTh, yTh, hPeriode
    
    #
    # Zone du tableau des compétences - X
    #
    ref = prg.classe.referentiel
#     competences = ref._listesCompetences_simple["S"]
    competences = ref.dicoCompetences["S"].get2Niveaux()
    
    if ref.dicoCompetences["S"].getProfondeur() == 3:
        wColComp = wColCompBase
    else:
        wColComp = wColCompBase/2
    
    tailleZComp[0] = 0
    for i, (k1, l1) in enumerate(competences):
        dx = wColComp/3
        if len(l1) == 0:
            l1 = [k1]
            dx = 0
            
        for k2 in l1:
            xComp[k2] = tailleZComp[0] #- 0.5 * wColComp  # position "gauche" de la colonne (relative)
            cComp[k2] = i
            tailleZComp[0] += wColComp
        tailleZComp[0] += dx
        
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
        
        
    tailleZComp[0] -= dx
    posZComp[0] = posZOrganis[0] + tailleZOrganis[0] - tailleZComp[0]
    
    for s in list(xComp.keys()):
        xComp[s] += posZComp[0] # positions -> absolues
    
    
    #
    # Zone du tableau des Thématiques
    #
    lstTh = prg.GetListeTh()
    hTh = (-0.001*len(lstTh)+0.025) * COEF
#     print "hTh", hTh
    tailleZThV[0] = wTh * len(lstTh)
    if len(lstTh) == 0:
        tailleZThH[1] = 0
        e = 0
    else:
        tailleZThH[1] = hTh * len(lstTh) + ecartY
        e = 1
    posZThV[0] = posZComp[0] - tailleZThV[0] - ecartX/2
    tailleZThH[0] = posZThV[0]-posZThH[0]- ecartX/2
    tailleZThV[1] = posZOrganis[1] + tailleZOrganis[1] - posZThV[1]
    xTh = []
    yTh = []
    for i in range(len(lstTh)):
        xTh.append(posZThV[0] + (i+0.5) * wTh)
        yTh.append(posZThH[1] + (i+0.5) * hTh)
        
        
    #
    # Zone du tableau des thèmes/CI
    #
    lstCI = prg.GetListeCI()
    hCI = (-0.001*len(lstCI)+0.025) * COEF
#     print "hCI", hCI
    tailleZCIV[0] = wCI * len(lstCI)
    if len(lstCI) == 0:
        tailleZCIH[1] = 0
    else:
        tailleZCIH[1] = hCI * len(lstCI) + ecartY
    posZCIV[0] = posZComp[0] - tailleZCIV[0] - tailleZThV[0] - ecartX/2
    posZCIV[1] = posZThH[1] + tailleZThH[1] + ecartY/2 * e
    posZCIH[1] = posZCIV[1]
    tailleZCIH[0] = posZCIV[0] - posZCIH[0] - ecartX/2
    tailleZCIV[1] = posZOrganis[1] + tailleZOrganis[1] - posZCIV[1]
    xCI = []
    yCI = []
    for i in range(len(lstCI)):
        xCI.append(posZCIV[0] + (i+0.5) * wCI)
        yCI.append(posZCIV[1] + (i+0.5) * hCI)


    # Zone du tableau des compétences (entête - uniquement selon y)
    posZComp[1] = posZThV[1] + tailleZThH[1] + tailleZCIH[1]
    tailleZComp[1] = ecartyCITaches            
                 
                 
    # Zone de déroulement de la progression (cadre arrondi)
    posZDeroul[1] = posZThV[1] + tailleZThH[1] + tailleZCIH[1] + tailleZComp[1]
    tailleZDeroul[0] = posZCIV[0] - posZDeroul[0] - ecartX/2
    tailleZDeroul[1] = posZOrganis[1] + tailleZOrganis[1] - posZDeroul[1]
    
    
    # Zone des séquences et Projets
#     yTaches = []
    posZTaches[1] = posZDeroul[1] + ecartY/2
    tailleZTaches[0] = posZDeroul[0] + tailleZDeroul[0] - posZTaches[0] - ecartX/2
    tailleZTaches[1] = tailleZDeroul[1] - ecartY/2 - 0.03 * COEF    # écart fixe pour la durée totale

    # Hauteur des périodes
    hPeriode = (tailleZTaches[1]-ecartTacheY)/ref.getNbrPeriodes()-ecartTacheY

#     # Hauteurs des Sequences-Projets par période
#     a = [0.0]*ref.getNbrPeriodes()
#     b = a[:]

#     print ref.getPeriodesListe()
#     for p in range(ref.getNbrPeriodes()):
#         calculCoefCalcH(prg, ctx, hTacheMini, p)
#     for creneau in range(constantes.NBR_CRENEAU):
#         calculCoefCalcH(prg, ctx, hTacheMini, creneau)
#         if a < 0: # Trop de séquences -> on réduit !
#             calculCoefCalcH(prg, ctx, hTacheMini/2, creneau)

    
def Arranger(prg):
    """ Calcul les zones de chaque Séquence/Projet
        de la Progression <prg>
    
        Renvoie :
         - une liste (ordre des prg.sequences_projets) de rectangles encadrant les prg.sequences_projets
         - une liste des rectangles encadrant les titres des positions
    
    """
    
#     doc = lienDoc.GetDoc()
#     h = calcH_doc(doc, doc.position[0])
    ref = prg.classe.referentiel
    
    # Nombre de creneaux utilisés dans la progression
    nc = prg.nbrCreneaux
    
    # Nombre de périodes utilisés dans la progression
    np = ref.getNbrPeriodes()
    
    # Largeur de chaque colonne (créneau)
    wc = tailleZTaches[0]/nc
    
    # Hauteur de chaque période
    hp = tailleZTaches[1]/np
#     print "hp", hp
#     print "hPeriode", hPeriode
    
    # Tableau Creneau/Position contenant des lienDoc
    tableau = [[[] for p in range(np)] for c in range(nc)]
    for lienDoc in prg.sequences_projets:
        doc = lienDoc.GetDoc()
        tableau[lienDoc.creneaux[0]][doc.position[0]].append(lienDoc)
        if doc.position[0] != doc.position[1]:
            tableau[lienDoc.creneaux[0]][doc.position[1]].append(lienDoc)
#     print 
    # Tableau Creneau/Position contenant les coef a et b
    ab = [[getCoefCalcH(tableau[c][p]) for p in range(np)] for c in range(nc)]
#     print "a,b", ab[0][0]
    # Tableau Creneau/Position des "piles" de y
    yc = [[posZTaches[1] + hp*p for p in range(np)] for c in range(nc)]

    rects = []
    for lienDoc in prg.sequences_projets:
        doc = lienDoc.GetDoc()
        c = lienDoc.creneaux[0]
        p = doc.position[0]
        x = posZTaches[0] + c * wc
        w = (lienDoc.creneaux[1]-c+1) * wc - ecartTacheY
        y = yc[c][p]
        
        r = doc.getRangePeriode()
#         print "r =", r
#         print tableau[c][p]
        if len(r) == 1:
            a, b = ab[c][p]
            h = calcH(doc.GetDuree(), a, b)
#             print doc.GetDuree(), h
            yc[c][p] += h
        else:
            n = len(tableau[c][p])
            h = hPeriode/n
            yc[c][p] += h
            yc[c][r[-1]] += hPeriode/len(tableau[c][r[-1]])
            for pp in r[1:-1]:
                h += hp
            h += hp-hPeriode
            h += hPeriode/len(tableau[c][r[-1]])
        
        rects.append((x, y, w, h))
    
    
    rec_pos = [(posZDeroul[0], posZTaches[1] + hp*p,
                wPhases, hp) for p in range(np)]
    
    
    
    return rects, rec_pos


def getCoefCalcH(case):
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
            h += calcH(doc.GetDuree(), a, b)
            nt += 1
        else:
            hFixe += hPeriode/len(case)

    b = hTacheMini # Hauteur mini
    if h != 0:
        a = (hPeriode - hFixe - b*nt) / h
    return a, b





# def calculCoefCalcH2(prg, ctx, hm, periode):
#     global a, b
# #    print "calculCoefCalcH", hm
#     
# #     sommeEcarts = (prg.GetNbrPeriodesEffectif()-1)*ecartTacheY
# #    print "sommeEcarts", sommeEcarts
#     # Calcul des paramètres de la fonction hauteur = f(durée)
#     # hauteur = a * log(durée) + b
#     b[periode] = 0.0
#     a[periode] = 1.0
#     h = 0.0 #ecartTacheY
#     nt = 0 # nombre de tâches de hauteur variable ( = calculée par calcH() )
# 
#     for t in prg.sequences_projets:
#         h += calcH_doc(t.GetDoc(), periode)
# #        print "    ", t, t.GetDoc().GetDuree(), h
#         nt += 1
# 
#     b[periode] = hm # Hauteur mini
#     
#     hFixe = 0.0 #sommeEcarts
#     if h != 0:
#         a[periode] = (hPeriode - hFixe - b[periode]*nt) / h

#    print ">>> a,b :", a, b
    
    
#######################################################################################  
#def getCoulComp(partie, alpha = 1.0):
#    if partie in ICoulComp.keys():
#        return (ICoulComp[partie][0], ICoulComp[partie][1], ICoulComp[partie][2], alpha)  
#    return (ICoulComp[''][0], ICoulComp[''][1], ICoulComp[''][2], alpha)
    
######################################################################################  
def getPts(lst_rect):
        lst = []
        for rect in lst_rect:
            lst.append(rect[:2])
        return lst
    
######################################################################################  
def Draw(ctx, prg, mouchard = False, surRect = None):
    """ Dessine une fiche de progression <prg>
        dans un contexte cairo <ctx>
    """

#        print "Draw progression"
#    InitCurseur()
    
#    tps = time.time()
    #
    # Options générales
    #
    options = ctx.get_font_options()
    options.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    options.set_hint_style(cairo.HINT_STYLE_NONE)#cairo.HINT_STYLE_FULL)#
    options.set_hint_metrics(cairo.HINT_METRICS_OFF)#cairo.HINT_METRICS_ON)#
    ctx.set_font_options(options)
    
    DefinirZones(prg, ctx)
    
    # Essai ...
#     prg.GetOrganisation()
    
#     gabarit() # à virer (pour générer image gabarit
    
#    DefinirCouleurs(prg.GetNbrPeriodes())
#    print "DefinirCouleurs", IcoulPos

    #
    #    pour stocker des zones caractéristiques (à cliquer, ...)
    #
    
    # Zones sensibles, depuis pySéquence
    prg.zones_sens = []
    # Points caractéristiques des rectangles
    prg.pt_caract = []   # Contenu attendu : ((x,y), code)
    # Points caractéristiques des rectangles (sans code)
    prg.pts_caract = [] 
    
#    prg.rect = []
#    prg.rectComp = {}
    
    
    #
    # variables locales
    #
    ref = prg.classe.referentiel
    classe = prg.classe
    
    #
    # Type d'enseignement
    #
    tailleTypeEns = taillePro[0]/2
    t = prg.classe.GetLabel()
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_BOLD)
    ctx.set_source_rgb (0.6, 0.6, 0.9)
    
    h = taillePos[1] * 0.8
    show_text_rect(ctx, t, (posPro[0] , posPos[1], tailleTypeEns, h), 
                   va = 'c', ha = 'c', b = 0, orient = 'h', 
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = False, couper = False,
                   coulBord = (0, 0, 0))
    
    t = prg.classe.GetLabelComplet()
    ctx.set_source_rgb (0.3, 0.3, 0.8)
    show_text_rect(ctx, t, (posPro[0] , posPos[1] + h, tailleTypeEns, taillePos[1] - h), 
                   va = 'c', ha = 'c', b = 0, orient = 'h', 
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = False, couper = False)





    #
    # Positions dans l'année
    #
    posPos[0] = posNom[0] + tailleNom[0] + ecartX + tailleTypeEns

    taillePos[0] = taillePro[0]/2
    ctx.set_line_width (0.0015 * COEF)
    r = (posPos[0], posPos[1], taillePos[0], taillePos[1])
    rects = DrawPeriodes(ctx, r, prg.GetPositions(), ref.periodes,
                               tailleTypeEns = tailleTypeEns)
#    prg.rect.append(posPos+taillePos)
    
    for i, re in enumerate(rects):
        prg.zones_sens.append(Zone([re], param = "POS"+str(i)))
    prg.zones_sens.append(Zone([r], param = "POS"))
    





    #
    # Etablissement
    #
    if classe.etablissement != "":
        t = classe.etablissement + " (" + classe.ville + ")"
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                          cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, t, (posPos[0] , posPos[1]+taillePos[1], taillePos[0], posPro[1]-posPos[1]-taillePos[1]), 
                       va = 'c', ha = 'g', b = 0.2, orient = 'h', 
                       fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                       coulBord = (0, 0, 0))

    
    #
    # Image
    #
    bmp = prg.image
    if bmp != None:
        ctx.save()
        tfname = tempfile.mktemp()
        try:
            bmp.SaveFile(tfname, wx.BITMAP_TYPE_PNG)
            image = cairo.ImageSurface.create_from_png(tfname)
        finally:
            if os.path.exists(tfname):
                os.remove(tfname)  
                
        w = image.get_width()*1.1
        h = image.get_height()*1.1
        
        s = min(tailleImg[0]/w, tailleImg[1]/h)
        dx = (tailleImg[0] - s*image.get_width())/2
        dy = (tailleImg[1] - s*image.get_height())/2
        ctx.translate(posImg[0] + dx, posImg[1] + dy)
        ctx.scale(s, s)
        ctx.set_source_surface(image, 0, 0)
        ctx.paint ()
        ctx.restore()

    


    #
    #  Equipe
    #
    rectEqu = posEqu + tailleEqu
    prg.pt_caract.append((curve_rect_titre(ctx, "Equipe pédagogique",  rectEqu, 
                                          BcoulEqu, IcoulEqu, fontEqu),
                        'Equ'))
    
    lstTexte = []
    g = None
    c = []
    for i, p in enumerate(prg.equipe):
        lstTexte.append(p.GetNomPrenom(disc = constantes.AFFICHER_DISC_FICHE))
        if p.referent:
            g = i
        c.append(constantes.COUL_DISCIPLINES[p.discipline])
    lstCodes = [" \u25CF"] * len(lstTexte)

    if len(lstTexte) > 0:
        r = liste_code_texte(ctx, lstCodes, lstTexte, 
                             (posEqu[0], posEqu[1], tailleEqu[0], tailleEqu[1]+0.0001 * COEF),
                             0.1*tailleEqu[1]+0.0001 * COEF, 0.1,
                             gras = g, lstCoul = c, va = 'c')

    for i, p in enumerate(prg.equipe):
        prg.zones_sens.append(Zone([r[i]], obj = p))
    prg.zones_sens.append(Zone([rectEqu], param = "EQU"))
#        p.rect = [r[i]]
#        prj.pts_caract.append(getPts(r))





    #
    #  Calendrier
    #
#     prg.pt_caract.append((posPro, "Cal"))
    rectPro = posPro + taillePro
    pt = curve_rect_titre(ctx, "Calendrier",  rectPro, BcoulPro, IcoulPro, fontPro)
    prg.pt_caract.append((pt, "Cal"))
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_NORMAL)
    show_text_rect(ctx, constantes.ellipsizer("", constantes.LONG_MAX_PROBLEMATIQUE), 
                   rectPro, ha = 'g', b = 0.5,
                   fontsizeMinMax = (-1, 0.016 * COEF))
    DrawCalendrier(ctx, rectPro, prg.calendrier)
#    prg.rect.append(rectPro)
    prg.zones_sens.append(Zone([rectPro], param = "CAL"))






    #
    #  Années
    #
#    prg.pts_caract = []
    rectNom = posNom+tailleNom
    pt = curve_rect_titre(ctx, "Progression pédagogique",  
                          rectNom, BcoulNom, IcoulNom, fontNom)
    prg.pt_caract.append((pt, 'Ann'))
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_NORMAL)
    show_text_rect(ctx, "Années scolaires " + prg.GetAnnees(), 
                   rectNom, ha = 'c', b = 0.2,
                   fontsizeMinMax = (-1, 0.017 * COEF),
                   wrap = False, couper = False)
    
    prg.zones_sens.append(Zone([rectNom], param = "ANN"))
#    prg.pt_caract.append(posNom)






    #
    #  Tableau des compétences
    #    
    
    # Titre
    htitre = 0.017 * COEF
    show_text_rect(ctx, ref.dicoCompetences["S"]._nom.Plur_(),
                   (posZComp[0], posZOrganis[1] + ecartY/2,
                    tailleZComp[0], htitre), 
                   va = 'c', ha = 'c', b = 0, orient = 'h', 
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = False, couper = False,
                   coulBord = (0, 0, 0))
    
    
#     competences = ref._listesCompetences_simple["S"]
    competences = ref.dicoCompetences["S"].get2Niveaux()
#     print "competences", competences
    
    ctx.set_line_width(0.001 * COEF)
    _x = _x0 = posZComp[0]
    _y0, _y1 = posZComp[1], posZDeroul[1] + tailleZDeroul[1]
    h = 1.5*wColComp
    
    for i, g1 in enumerate(competences):
        k1, l1 = g1
        dx = wColComp/3
        if len(l1) == 0:
            l1 = [k1]
            dx = 0
        
        coul = list(ICoulComp[i][:3])+[0.2]
        n = 0
        for k2 in l1:
            #
            # Lignes verticales et rectangles clairs
            #
            rect = (_x, _y0, wColComp, _y1 -_y0)
            ligne(ctx, _x, _y0, _x, _y1, (0, 0, 0))
            ctx.set_source_rgba(*coul)
            ctx.rectangle(*rect[:4])
            ctx.fill()
                
            n += 1
            _x += wColComp
            
        
        # Dernière ligne
        ligne(ctx, _x, _y0, _x, _y1, (0, 0, 0))

        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.001 * COEF)
        
#        # Titre famille de compétences
#        ht = tailleZComp[1] / 4
#        show_text_rect(ctx, k1, (_x0, posZComp[1], _x-_x0, ht), va = 'c', ha = 'c', b = 0.3, orient = 'h')

        rects = tableauV(ctx, l1, _x0, posZComp[1], 
                         _x-_x0, tailleZComp[1], 
                         0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', 
                         coul = ICoulComp[i], b = 0.3)
        
        for i, r in enumerate(rects):
            prg.zones_sens.append(Zone([r], param = "CMP"+l1[i]))
            
        _x += dx
        _x0 = _x
    
    
    
    
    
    #
    # Bilan des compétences abordées
    #
    dicComp, nbrComp = prg.GetCompetencesAbordees()
    DrawBoutonCompetence(ctx, prg, None, dicComp, posZOrganis[1] + htitre, 
                         h = posZComp[1] - posZOrganis[1] - ecartY*3/2 - htitre, nbr = nbrComp)
        
      
        
        

    
    #
    #  Tableau des Thématiques
    #   
    lstTh = prg.GetListeTh()

    
    if len(lstTh) > 0:
        rectTh = (posZThH[0], posZThV[1], 
                  tailleZThH[0], tailleZThH[1])
        curve_rect_titre(ctx, ref._nomTh.Plur_(),
                         rectTh, BcoulCI, IcoulCI, fontCI)
        
        ctx.select_font_face(font_family, cairo.FONT_SLANT_NORMAL,
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
        x, y = posZThV[0] + ecartX /2, posZThV[1] + ecartY /2
        w, h = tailleZThH[0] - ecartX, tailleZThH[1] - ecartY
        
    
        
        if len(l) > 0:
            rec = tableauH(ctx, l, x, y, 
                         w, 0, h, 
                         va = 'c', ha = 'd', orient = 'h', coul = CoulAltern,
                         tailleFixe = True)
            
            
            
            #
            # Lignes horizontales
            #
            for i, e in enumerate(lstTh):
                prg.zones_sens.append(Zone([rec[i]], param = "Th"+str(i)))
                
                Ic = CoulAltern[i][0]
                
                ctx.set_line_width(0.003 * COEF)
                ligne(ctx, posZThV[0]+tailleZThH[0]- ecartX /2, yTh[i]+ ecartY /2,
                      posZComp[0]+tailleZComp[0], yTh[i]+ ecartY /2, Ic)
                
                prg.pt_caract.append((rec[i][:2], "Th"+str(i)))
                
                
            #
            # Lignes verticales
            #
            for i, e in enumerate(lstTh):
                Ic = CoulAltern[i][0]
                ctx.set_line_width(0.003 * COEF)
                
                ligne(ctx, xTh[i], yTh[i]+ ecartY /2,
                      xTh[i], posZTaches[1] + tailleZTaches[1],
                      Ic)

    #            DrawCroisementsElevesCompetences(ctx, prg, e, yCI[i])
            
            #
            # Ombres des lignes verticales
            #
            e = 0.003 * COEF
            ctx.set_line_width(0.003 * COEF)
            for i in range(len(lstTh)) :
                y = posZTaches[1] + tailleZTaches[1] + (i % 2)*(ecartY/2) + ecartY/2
                ctx.set_source_rgb(1,1,1)
                ctx.move_to(xTh[i]+e, yTh[i]+e+ ecartY /2)
                ctx.line_to(xTh[i]+e, y)
                ctx.move_to(xTh[i]-e, yTh[i]+e+ ecartY /2)
                ctx.line_to(xTh[i]-e, y)
            ctx.stroke()




    #
    #  Tableau des CI/Thèmes de séquence
    #   
    lstCI = prg.GetListeCI()
    
    if len(lstCI) > 0:
        rectCI = (posZCIH[0], posZCIH[1], 
                  tailleZCIH[0], tailleZCIH[1])
        curve_rect_titre(ctx, getPluriel(ref.nomCI),
                         rectCI, BcoulCI, IcoulCI, fontCI)
        
        ctx.select_font_face(font_family, cairo.FONT_SLANT_NORMAL,
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
        x, y = posZCIH[0] + ecartX /2, posZCIH[1] + ecartY /2
        w, h = tailleZCIH[0] - ecartX, tailleZCIH[1] - ecartY
        
    
        
        if len(l) > 0:
            rec = tableauH(ctx, l, x, y, 
                         w, 0, h, 
                         va = 'c', ha = 'd', orient = 'h', 
                         coul = CoulAltern,
                         tailleFixe = True)
            
            
            
            #
            # Lignes horizontales
            #
            for i, e in enumerate(lstCI):
                prg.zones_sens.append(Zone([rec[i]], param = "CI"+str(i)))
                
                ctx.set_line_width(0.003 * COEF)
                ligne(ctx, posZCIH[0]+tailleZCIH[0] - ecartX/2, yCI[i] + ecartY/2,
                           xCI[i], yCI[i] + ecartY/2,
                      CoulAltern[i][0][:-1])
                
                prg.pt_caract.append((rec[i][:2], "CI"+str(i)))
                
            #
            # Lignes verticales
            #
            for i, e in enumerate(lstCI):
                ctx.set_line_width(0.003 * COEF)
                ligne(ctx, xCI[i], yCI[i] + ecartY /2, 
                           xCI[i], posZTaches[1] + tailleZTaches[1], 
                      CoulAltern[i][0][:-1])
                 
    #            DrawCroisementsElevesCompetences(ctx, prg, e, yCI[i])
            
            #
            # Ombres des lignes verticales
            #
            e = 0.003 * COEF
            ctx.set_line_width(0.003 * COEF)
            for i in range(len(lstCI)) :
                y = posZTaches[1] + tailleZTaches[1]
                ctx.set_source_rgb(1,1,1)
                ctx.move_to(xCI[i]+e, yCI[i]+e+ ecartY /2)
                ctx.line_to(xCI[i]+e, y)
                ctx.move_to(xCI[i]-e, yCI[i]+e+ ecartY /2)
                ctx.line_to(xCI[i]-e, y)
            ctx.stroke()

    
    
    DrawSequencesEtProjets(ctx, prg)
#     DrawSequencesEtProjets2(ctx, prg)
    
    
    
#     ###################################################################################
#     #  Séquences et Projets
#     #
#      
#     curve_rect_titre(ctx, u"Séquences et Projets",  
#                      (posZDeroul[0], posZDeroul[1], 
#                       tailleZDeroul[0], tailleZDeroul[1]), 
#                      BcoulZDeroul, IcoulZDeroul, fontZDeroul)
#      
#     y = posZTaches[1] - ecartTacheY
#  
#     rects, rec_pos = Arranger(prg)
#  
#     #
#     # Ligne séparatrices
#     #
#     for rec in rec_pos[1:]:
#         ctx.set_source_rgba(*BcoulZDeroul)
#         ctx.move_to(posZDeroul[0], rec[1] - ecartTacheY/2)
#         ctx.line_to(posZDeroul[0] + tailleZDeroul[0], rec[1]-ecartTacheY/2)
#         ctx.stroke()
#  
#     #
#     # Les cadres
#     #
#     yTaches = []
#     for i, lienDoc in enumerate(prg.sequences_projets):
#         y = rects[i][1] + ecartX/5
# #         if len(yTaches) > 0 and y-yTaches[-1] < ecartX/6:
# #             y = yTaches[-1] + ecartX/6
#         yTaches.append(y)
#         yb = DrawSequenceProjet(ctx, prg, lienDoc, rects[i], y)
#      
#     # Ajustement des yTaches
#     yt = zip(yTaches, range(len(yTaches)))
#  
#     yt.sort(key=lambda x:x[0])
#  
#      
#     i = 1
#     while i < len(yt):
#         if yt[i][0] - yt[i-1][0] < (ecartX/5):
#             yt[i] = (yt[i-1][0] + ecartX/5, yt[i][1])
#         i += 1
#      
#      
# #     for j, (y, i) in enumerate(yt[1:]):
# #         y_1 = yt[j-1][0]
# #         if y - y_1 < (ecartX/5):
# #             print " !! ", y , y_1
# #             yt[j] = (y_1 + ecartX/5, yt[j][1])
#     yt.sort(key=lambda x:x[1])
#  
#     try:
#         yTaches, i = zip(*yt)
#     except:
#         pass
#      
#     #
#     # Les lignes horizontales en face des sequences
#     # et les croisements Séquences/Competences
#     #
#     for i, y in enumerate(yTaches): 
#         x = rects[i][0] + rects[i][2]
#         doc = prg.sequences_projets[i].GetDoc()
#         DrawLigne(ctx, x, y)
#         DrawCroisementsCompetencesTaches(ctx, prg, doc, y)
#         if hasattr(doc, 'CI'):
#             DrawCroisementsCISeq(ctx, prg, doc, y)
#      
#     # Nom des périodes
# #    print "yh_phase", yh_phase
#      
#     fontsize = wPhases
#       
#     for i, rec in enumerate(rec_pos):
#            
#         c = BcoulPos[i]
#         ctx.set_source_rgb(c[0],c[1],c[2])
#         ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
#                               cairo.FONT_WEIGHT_NORMAL)
#          
#         show_text_rect(ctx, str(i+1), 
#                        rec, fontsizeMinMax = (fontsize, fontsize),
#                        ha = 'c', orient = "h", b = 0.2, le = 0.7,
#                        wrap = False, couper = False
#                        ) 
#  
 
 


    
    #
    # Durée Totale
    #
    ctx.set_source_rgb(0.5,0.8,0.8)
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
    
    show_text_rect(ctx, getHoraireTxt(prg.GetDuree()), 
                   (posZDeroul[0], posZTaches[1]+tailleZTaches[1],
                    posZTaches[0]-posZDeroul[0], posZDeroul[1]+tailleZDeroul[1] - posZTaches[1]-tailleZTaches[1]), 
                   ha = 'c', 
                   orient = 'h', b = 0.3, couper = False)






    #
    # Informations
    #
    info(ctx, margeX, margeY)
    

    

######################################################################################  
def DrawLigneEff(ctx, x, y):
    dashes = [ 0.010 * COEF,   # ink
               0.002 * COEF,   # skip
               0.005 * COEF,   # ink
               0.002 * COEF,   # skip
               ]
    ctx.set_line_width (0.001 * COEF)
    ctx.set_dash(dashes, 0)
    ligne(ctx, x, posZCIV[1] + tailleZCIV[1],
          x, y, (0.6, 0.8, 0.6))
    ctx.set_dash([], 0)
         
            
            
######################################################################################  
def DrawSequencesEtProjets(ctx, prg):
    ###################################################################################
    #  Séquences et Projets
    #
    

    # Nombre de creneaux utilisés dans la progression
    nc = prg.nbrCreneaux
#     
#     # Nombre de périodes utilisés dans la progression
#     np = ref.getNbrPeriodes()    
#     
#     
# #     rect = []
# #     l = 0           # Ligne "courante"
# #     for i, lienDoc in enumerate(prg.sequences_projets):
# #         r = [None] * 4
# #         p = lienDoc.GetPeriodes()
# #         c = lienDoc.GetCrenaux()
# #         r[0] = c[0]
# #         r[1] = p[0]
# #         r[2] = len(c)
# #         r[3] = len(p)
# #         
# #         if i >0 and r[1] <= rect[i-1]:
# #             l += 
# #         
# #         rect.append(r)
# #          
# #      
# #     print "rect", rect    
#     
#     
#     # Grille niveau 1
#     grille = [[[] for c in range(nc)] for l in range(np)]
#     for i, lienDoc in enumerate(prg.sequences_projets):
#         p = lienDoc.GetPosition()   # Première et dernière période
#         c = lienDoc.GetCrenaux()    # Liste des créneaux
# 
#         for lig in p:
#             for col in c:
#                 grille[lig][col].append(i)
#     
#     
# #     print grille
# 
# #     grille_c = []
# #     N = range(len(prg.sequences_projets))
# #     for per in grille:
# #         p = []
# #         for lst in per:
# #             c = []
# #             for sp in N:
# #                 if sp in lst:
# #                     c.append(sp)
# #                 else:
# #                     c.append(None)
# #             p.append(c)
# #         grille_c.append(p)
# #         
#     
#     
#     
# 
#     N = range(len(prg.sequences_projets))
#     grilles_p = []
#     for lig in grille:
#         lig2 = []
#         for c, cre in enumerate(lig):
#             cre2 = []
#             for n in N:
#                 if n in cre:
#                     cre2.append(n)
#                 else:
#                     cre2.append(None)
#             lig2.append(cre2)
#         lig2 = zip(*lig2)
#         grilles_p.append([l for l in lig2])# if not all(v is None for v in l)]) 
#         
#     
# #     print "grilles_p", grilles_p
#     
#     # Compactage de la grille
#     for g in grilles_p:
#         l = 1
#         while l < len(g):
#             z = zip(g[l-1], g[l])
#             if  all(x is None or y is None for x, y in z):
#                 g[l-1] = tuple(x or y for x, y in z)
#                 del g[l]
#             else:
#                 l+=1
#     
# #     print "grilles_p", grilles_p
#     
#     
#     
# #     # 2ème passage
# #     for p, g in enumerate(grilles_p[1:-1]):
# #         if len(g) > 1 and any([None in c for c in g]):
# #              for c in zip(*g):
# #                  if not None in 
#         
#     
#     # Rectangles des sequences_projets
#     rect = [[None,None,0,0] for i in prg.sequences_projets] # Rectangles en mode "lignes/colonnes"
#     l_per = []                                              # Lignes marquant les débuts des périodes
#     l = 0
#     for p in grilles_p:
#         l_per.append(l) 
#         for lig in p:
#            
#             for c, sp in enumerate(lig):
#                 if sp is not None:
#                     if rect[sp][0] is None:      # X
#                         rect[sp][0] = c
#                     if rect[sp][1] is None:      # Y
#                         rect[sp][1] = l
#                     rect[sp][2] = c - rect[sp][0] + 1
#                     rect[sp][3] = l - rect[sp][1] + 1
#             l += 1
        
    rect, l_per, y_lig = prg.GetRectangles()[:3]

    
    # Mise des rectangles à l'échelle de la fiche
    rects = [[0,0,0,0] for i in prg.sequences_projets]  # Rectangles à l'échelle du dessin
    for sp, r in enumerate(rect):
        # suivant X : position, largeur
        rects[sp][0] = posZTaches[0] + tailleZTaches[0]/nc * r[0]
        rects[sp][2] = r[2] * tailleZTaches[0]/nc
        
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
        r[0] += ecartX / 2
        r[2] -= ecartX / 2
        
       
    # On ajuste en hauteur 
#     print "bas:", posZTaches[1] + tailleZTaches[1]
#     ly = [_y+_h for _x, _y, _w, _h in rects]            # Liste des positions basses de chaque rectangle
#     if len(ly) >0:
#         Y = max(ly)
#         print Y,
    Y = y_lig[-1]   # Position de la dernière ligne = bas de la zone
    if Y > 0:
        a = (tailleZTaches[1] ) / Y  # Coefficient multiplicateur- n_ecarts*ecartY
        
        # On met à l'échelle les positions des lignes
        for l in range(len(y_lig)):
            y_lig[l] = posZTaches[1] + y_lig[l]*a
            
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
    
    curve_rect_titre(ctx, "Séquences et Projets",  
                     (posZDeroul[0], posZDeroul[1], 
                      tailleZDeroul[0], tailleZDeroul[1]), 
                     BcoulZDeroul, IcoulZDeroul, fontZDeroul)
    
    


    #
    # Ligne séparatrices
    #
    for rec in y_per[1:]:
        
        ctx.set_source_rgba(*BcoulZDeroul)
        ctx.move_to(posZDeroul[0], rec)
        ctx.line_to(posZDeroul[0] + tailleZDeroul[0], rec)
        ctx.stroke()

    #
    # Les cadres
    #
    yTaches = []
    for i, lienDoc in enumerate(prg.sequences_projets):
        y = rects[i][1] + ecartX/5
#         if len(yTaches) > 0 and y-yTaches[-1] < ecartX/6:
#             y = yTaches[-1] + ecartX/6
        yTaches.append(y)
        yb = DrawSequenceProjet(ctx, prg, lienDoc, rects[i], y)
    
    # Ajustement des yTaches
    yt = list(zip(yTaches, list(range(len(yTaches)))))

    yt.sort(key=lambda x:x[0])

    
    i = 1
    while i < len(yt):
        if yt[i][0] - yt[i-1][0] < (ecartX/5):
            yt[i] = (yt[i-1][0] + ecartX/5, yt[i][1])
        i += 1
    
    
#     for j, (y, i) in enumerate(yt[1:]):
#         y_1 = yt[j-1][0]
#         if y - y_1 < (ecartX/5):
#             print " !! ", y , y_1
#             yt[j] = (y_1 + ecartX/5, yt[j][1])
    yt.sort(key=lambda x:x[1])

    try:
        yTaches, i = list(zip(*yt))
    except:
        pass
    
    #
    # Les lignes horizontales en face des sequences
    # et les croisements Séquences/Competences
    #
    for i, y in enumerate(yTaches): 
        x = rects[i][0] + rects[i][2]
        doc = prg.sequences_projets[i].GetDoc()
        DrawLigne(ctx, x, y)
        DrawCroisementsCompetencesTaches(ctx, prg, doc, y)
        if hasattr(doc, 'CI'):
            DrawCroisementsCISeq(ctx, prg, doc, y)
    
    # Nom des périodes
#    print "yh_phase", yh_phase
     
    fontsize = wPhases
    for i, y_p in enumerate(y_per[:-1]):
        if y_p is None or y_per[i+1]-y_p <= 0:
            continue
        h = y_per[i+1]-y_p
        r = (posZDeroul[0], y_p,
             wPhases, h)
        c = BcoulPos[i]
        ctx.set_source_rgb(c[0],c[1],c[2])
        ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                              cairo.FONT_WEIGHT_NORMAL)
        if ctx.font_extents()[2] < h:
            show_text_rect(ctx, str(i+1), 
                           r, fontsizeMinMax = (fontsize, fontsize),
                           ha = 'c', orient = "h", b = 0.2, le = 0.7,
                           wrap = False, couper = False
                           ) 





######################################################################################  
def DrawSequencesEtProjets2(ctx, prg):
    ###################################################################################
    #  Séquences et Projets
    #
    
    curve_rect_titre(ctx, "Séquences et Projets",  
                     (posZDeroul[0], posZDeroul[1], 
                      tailleZDeroul[0], tailleZDeroul[1]), 
                     BcoulZDeroul, IcoulZDeroul, fontZDeroul)
    
    y = posZTaches[1] - ecartTacheY


    
    rects, rec_pos = Arranger(prg)

    #
    # Ligne séparatrices
    #
    for rec in rec_pos[1:]:
        ctx.set_source_rgba(*BcoulZDeroul)
        ctx.move_to(posZDeroul[0], rec[1] - ecartTacheY/2)
        ctx.line_to(posZDeroul[0] + tailleZDeroul[0], rec[1]-ecartTacheY/2)
        ctx.stroke()

    #
    # Les cadres
    #
    yTaches = []
    for i, lienDoc in enumerate(prg.sequences_projets):
        y = rects[i][1] + ecartX/5
#         if len(yTaches) > 0 and y-yTaches[-1] < ecartX/6:
#             y = yTaches[-1] + ecartX/6
        yTaches.append(y)
        yb = DrawSequenceProjet(ctx, prg, lienDoc, rects[i], y)
    
    # Ajustement des yTaches
    yt = list(zip(yTaches, list(range(len(yTaches)))))

    yt.sort(key=lambda x:x[0])

    
    i = 1
    while i < len(yt):
        if yt[i][0] - yt[i-1][0] < (ecartX/5):
            yt[i] = (yt[i-1][0] + ecartX/5, yt[i][1])
        i += 1
    
    
#     for j, (y, i) in enumerate(yt[1:]):
#         y_1 = yt[j-1][0]
#         if y - y_1 < (ecartX/5):
#             print " !! ", y , y_1
#             yt[j] = (y_1 + ecartX/5, yt[j][1])
    yt.sort(key=lambda x:x[1])

    try:
        yTaches, i = list(zip(*yt))
    except:
        pass
    
    #
    # Les lignes horizontales en face des sequences
    # et les croisements Séquences/Competences
    #
    for i, y in enumerate(yTaches): 
        x = rects[i][0] + rects[i][2]
        doc = prg.sequences_projets[i].GetDoc()
        DrawLigne(ctx, x, y)
        DrawCroisementsCompetencesTaches(ctx, prg, doc, y)
        if hasattr(doc, 'CI'):
            DrawCroisementsCISeq(ctx, prg, doc, y)
    
    # Nom des périodes
#    print "yh_phase", yh_phase
    
    fontsize = wPhases
     
    for i, rec in enumerate(rec_pos):
          
        c = BcoulPos[i]
        ctx.set_source_rgb(c[0],c[1],c[2])
        ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                              cairo.FONT_WEIGHT_NORMAL)
        
        show_text_rect(ctx, str(i+1), 
                       rec, fontsizeMinMax = (fontsize, fontsize),
                       ha = 'c', orient = "h", b = 0.2, le = 0.7,
                       wrap = False, couper = False
                       ) 




######################################################################################  
def DrawSequenceProjet(ctx, prg, lienDoc, rect, yd):
    """ Dessine le cadre d'une séquence ou d'un projet
        Avec une petite flèche pour démarrer le croisement avec les compétences
    """
    global yTaches
    doc = lienDoc.GetDoc()
    
    e = 0.0015 * COEF   # épaisseur du cadre
    x, y, w, h = rect
    
    y += e/4
    h -= e/2
    
    #
    # Flèche verticale indiquant la durée de la séquence/Projet
    #
    ctx.set_source_rgba (0.9,0.8,0.8,0.9)
       
    ctx.rectangle(x, y, wDuree, h)
    ctx.fill_preserve ()    
    ctx.set_source_rgba(0.4, 0.4, 0.4, 1)
    ctx.set_line_width(0.0006 * COEF)
    ctx.stroke ()
    
    ctx.set_source_rgb(0.5, 0.8, 0.8)
    ctx.select_font_face(font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
    
    if h > wDuree:
        orient = 'v'
    else:
        orient = 'h'
        
    show_text_rect(ctx, getHoraireTxt(doc.GetDuree()), 
               (x, y, wDuree, h), 
               orient = orient, b = 0.1)
    
    
    #
    # Tracé du cadre de la tâche
    #
    x += wDuree + ecartX/6
    w -= wDuree + ecartX/6
    

    
#    lienSeq.pts_caract.append((x, y))
        
    ctx.set_line_width(e)
#    print "BcoulPos", BcoulPos
    rectangle_plein_doigt(ctx, x, y, w, h, ecartX/5, yd-y, 
                          BcoulPos[doc.position[0]], 
                          IcoulPos[doc.position[0]], 
                          0.9)
    
    #
    # Icone du type de document
    #
    if h > hTacheMini:
        ctx.save()
    #     if doc.nom_obj == u"Séquence":
    #         bmp = images.Icone_sequence.GetBitmap()
    #     else:
    #         bmp = images.Icone_projet.GetBitmap()
        bmp = doc.getIconeDraw()
        image = wx.lib.wxcairo.ImageSurfaceFromBitmap(bmp) 
        ctx.translate(x+ecartX/5, y+ecartY/5)
        ctx.scale(hTacheMini/120, hTacheMini/120)
        ctx.set_source_surface(image, 0, 0)
        ctx.paint ()
        ctx.restore()
        
    
    #
    # Affichage de l'intitulé de la Séquence ou du Projet
    #
    ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                          cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgb (0,0,0)
    
    # Si on ne peut pas afficher l'intitulé dessous, on le met à coté
    rect = (x + hTacheMini, y, w - hTacheMini, h)
    if rect[2] > 0:
        show_text_rect(ctx, doc.intitule, rect, 
                       ha = 'g', fontsizeMinMax = (minFont, 0.015 * COEF))
    
    
#    lienSeq.rect.append([x, y, tailleZTaches[0], h])
    prg.zones_sens.append(Zone([rect], obj = lienDoc))
    lienDoc.pt_caract = [(rect[:2], "Seq")]
    
    #
    # Tracé des croisements "Tâches" et "Eleves"
    #
#     yTaches.append([doc, y+h/2])
    
#    DrawCroisementsCompetencesTaches(ctx, tache, y + h/2)
    
#     y += h
#     return y
        
        
        
######################################################################################  
def DrawLigne(ctx, x, y, gras = False):
    dashes = [ 0.002 * COEF,   # ink
               0.002 * COEF,   # skip
               0.002 * COEF,   # ink
               0.002 * COEF,   # skip
               ]
    
    if gras:
        ctx.set_line_width (0.002 * COEF)
    else:
        ctx.set_line_width (0.001 * COEF)
    ctx.set_dash(dashes, 0)
    ligne(ctx, posZOrganis[0]+tailleZOrganis[0], y,
          x, y, (0, 0.0, 0.2, 0.6))
    ctx.set_dash([], 0)       


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
    
    
######################################################################################  
def DrawCroisementsCompetencesTaches(ctx, prg, seq, y):
    DrawBoutonCompetence(ctx, prg, seq, seq.GetCompetencesVisees(), y)
    

    
#####################################################################################  
def DrawCroisementsCISeq(ctx, prg, seq, y):
    """ Dessine les "ronds" à cliquer
    """ 
    #
    # Croisements Sequence/CI
    #
    ref = prg.GetReferentiel()
    lstCI = prg.GetListeCI()
#    print "DrawCroisementsCISeq", lstCI
    dy = 0
    r = 0.004 * COEF
        
    for num, CI in enumerate(lstCI):
        color0 = CoulAltern[num][0]
        color1 = CoulAltern[num][1]

        _x = xCI[num]
        
        if num in seq.CI.numCI or CI in seq.CI.CI_perso:
            boule(ctx, _x, y, r, 
                  color0 = color0, color1 = color1,
                  transparent = False)
        elif num < len(ref.CentresInterets):
            ctx.set_source_rgba (0,0,0,1)
            ctx.arc (_x, y, r, 0, 2*pi)
            ctx.stroke()
            boule(ctx, _x, y, r, 
                  color0 = color0, color1 = (1,1,1),
                  transparent = False)
        
        prg.zones_sens.append(Zone([(_x -r , y - r, 2*r, 2*r)], obj = seq, param = "CI"+str(num)))
#        tache.projet.eleves[i].rect.append((_x -r , y - r, 2*r, 2*r))
#        tache.projet.eleves[i].pts_caract.append((_x,y))
        y += dy
        

    

    
######################################################################################  
def DrawBoutonCompetence(ctx, prg, seq, listComp, y, h = None, nbr = None):
    """ Dessine les petits rectangles des compétences abordées dans la Séquence
    
    : nbr : nombre de fois que chaque compétence est abordée (pour bilan seulement)
    
    """
#     print "DrawBoutonCompetence", seq, listComp, nbr
    
    if seq == None and len(listComp) == 0:
        return
    
    if h == None: # Toujours sauf pour les revues
        h = 0.6*wColComp
        
    if nbr == None:
        nbr = [1] * (len(listComp)+1)
        lig = True
    else:
        lig = False
        
    dh = h / max(nbr)    
    
    ctx.set_line_width(0.0004 * COEF)
    listComp = [k[1:] for k in listComp]
    
    ref = prg.GetReferentiel()
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
            x = xComp[k2]
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
                
            dx = wColComp/len(lc)
            for a, i in enumerate(lc):
                if i in listComp:
                    H = nbr[listComp.index(i)] * dh
                    rect = (x+a*dx, y+h-H, dx, H)
                    ctx.set_source_rgba(*ICoulComp[cComp[k2]])
                    ctx.rectangle(*rect)
                    ctx.fill_preserve ()
                    ctx.set_source_rgba (0, 0 , 0, 1)
                    ctx.stroke()
                else:
                    if lig:
                        rect = (x+a*dx, y, dx, h)
                        ctx.set_source_rgba (1, 1, 1, 0)
                        ctx.move_to(rect[0], rect[1])
                        ctx.rel_line_to(0, rect[3])
                        ctx.move_to(rect[0]+rect[2], rect[1])
                        ctx.rel_line_to(0, rect[3])
                        ctx.set_source_rgba (0, 0 , 0, 1)
                        ctx.stroke()
                    else:
                        rect = None
                        
                if rect is not None:
                    prg.zones_sens.append(Zone([rect], obj = seq, param = "CMP"+i))
                
    
    
    return
    
    
    
    
    
    
#     
#     ctx.set_line_width(0.0004 * COEF)
#     listComp = [k[1:] for k in listComp]
#     for s in l:
#         x = xComp[s] #- wColComp/2
#         e = h/5
# #        print "h", h
#         rect = (x+e/2, y-h/2+e/2, wColComp-e, h-e)
#         prg.zones_sens.append(Zone([rect], obj = seq, param = "CMP"+s))
#         
#         ctx.set_source_rgba(*ICoulComp[cComp[s]])
#         
#         coul = [c*0.6 for c in ICoulComp[cComp[s]][:3]]+[0.4]
#         
#         if s in listComp:
#             relief(ctx, rect, e, color = ICoulComp[cComp[s]])
#         else:
# #            ctx.set_source_rgba (0,0,0,1)
# #            ctx.rectangle(*rect)
# #            ctx.stroke()
#             relief(ctx, rect, e, color = coul, bosse = False)
# #        ctx.set_source_rgba(0, 0, 0, 1)
# #        ctx.stroke()





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
    
    