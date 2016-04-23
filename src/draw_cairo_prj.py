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

## Copyright (C) 2011-2013 Cédrick FAURY

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

import cairo
from draw_cairo import *
#from draw_cairo import LargeurTotale, font_family, curve_rect_titre, show_text_rect_fix, show_text_rect, \
#                        boule, getHoraireTxt, liste_code_texte, rectangle_plein, barreH, tableauV, minFont, maxFont, tableauH, \
#                        DrawPeriodes, COEF, info

from math import log


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

#
# Données pour le tracé
#

# Marges
margeX = 0.02 * COEF
margeY = 0.04 * COEF

# Ecarts
ecartX = 0.02 * COEF
ecartY = 0.02 * COEF

# Nom du projet
tailleNom = (0.29 * COEF, 0.04 * COEF)
posNom = (margeX, margeY)
IcoulNom = (0.9, 0.8, 0.8, 0.85)
BcoulNom = (0.3, 0.2, 0.25, 1)
fontNom = 0.014 * COEF

# Support du projet
tailleSup = (0.17 * COEF, 0.06 * COEF)
posSup = (margeX, posNom[1] + tailleNom[1] + ecartY)
IcoulSup = (0.85, 0.8, 0.8, 0.85)
BcoulSup = (0.28, 0.2, 0.25, 1)
fontSup = 0.012 * COEF

# Equipe pédagogique
tailleEqu = (0.17 * COEF, 0.18 * COEF - tailleSup[1]- tailleNom[1] - 3*ecartY/2)
posEqu = (margeX, posSup[1] + tailleSup[1] + ecartY)
IcoulEqu = (0.8, 0.8, 0.9, 0.85)
BcoulEqu = (0.2, 0.25, 0.3, 1)
fontEqu = 0.011 * COEF

# Position dans l'année
posPos = [None, margeY - ecartY/2]
taillePos = [None, 0.03 * COEF]

# Problématique
posPro = [posNom[0] + tailleNom[0] + ecartX/2, margeY + taillePos[1] + ecartY/2]
taillePro = [LargeurTotale - margeX - posPro[0], posEqu[1] + tailleEqu[1] - posPro[1]]
IcoulPro = (0.8, 0.9, 0.8, 0.85)
BcoulPro = (0.25, 0.3, 0.2, 1)
fontPro = 0.014 * COEF

# Image du support
posImg = [posSup[0] + tailleSup[0] + ecartX/4, posNom[1] + tailleNom[1] + ecartY]
tailleImg = [posPro[0] - posSup[0] - tailleSup[0], None]
tailleImg[1] = posEqu[1] + tailleEqu[1] - posSup[1]
IcoulImg = (0.8, 0.8, 1, 0.85)
BcoulImg = (0.1, 0.1, 0.25, 1)
centreImg = (posImg[0] + tailleImg[0] / 2 + 0.0006 * COEF, posImg[1] + tailleImg[0] / 2 - 0.004 * COEF)

# Zone d'organisation du projet (grand cadre)
posZOrganis = (margeX, 0.24 * COEF)
bordureZOrganis = 0.01 * COEF
tailleZOrganis = (LargeurTotale-2*margeX, 1 * COEF-ecartY-posZOrganis[1]-bordureZOrganis)

# Zone de déroulement du projet
posZDeroul = [margeX, None]
tailleZDeroul = [None, None]
IcoulZDeroul = (1, 1, 0.7, 0.85)
BcoulZDeroul = (0.4, 0.4, 0.03, 1)
fontZDeroul = 0.014 * COEF
wPhases = 0.04 * COEF      # Taille du label "phases"
wDuree = 0.012 * COEF       # Taille de la fleche "duree"


# Zones des tableaux des éléves
posZElevesV = [None, 0.24 * COEF]
tailleZElevesV = [None, None]
posZElevesH = [posZDeroul[0], posZElevesV[1]]
tailleZElevesH = [None, None]
wEleves = 0.015 * COEF
hEleves = 0.020 * COEF
xEleves = []
yEleves = []

# Zone du tableau des compétences
posZComp = [None, None]
tailleZComp = [None, None]
wColCompBase = 0.018 * COEF
wColComp = wColCompBase
xComp = {}
ICoulComp = {'C' : (1, 0.6, 0.7, 0.2),      # couleur "Revue"
             'S' : (0.598, 0.7, 1, 0.2),
             ''  : (0.598, 0.7, 0.7, 0.2)}    # couleur "Soutenance"
#ICoulComp['S'] = (0.598, 0.7, 1, 0.2)      
#ICoulComp['C'] = (1, 0.6, 0.7, 0.2)      
#BCoulCompR = (0.3, 0.2, 0.4, 1)      # couleur "Revue"
BCoulCompS = (0.7, 0.7, 0.7, 0.2)      # couleur "Soutenance"


# Zone des tâches
posZTaches = [posZDeroul[0] + wPhases + wDuree + ecartX*3/6, None]
tailleZTaches = [None, None]
hTacheMini = ecartY/2
hRevue = ecartY/3
yTaches = []
ecartTacheY = None  # Ecartement entre les tâches de phase différente

# paramètres pour la fonction qui calcule la hauteur des tâches 
# en fonction de leur durée
a = b = None
def calcH_tache(tache):
    if (tache.phase in ["R1", "R2", "R3", "S"] and tache.DiffereSuivantEleve()):
        return max(len(tache.projet.eleves) * hRevue, hRevue)
    else:
        return calcH(tache.GetDuree())
        

def calcH(t):
    if t != 0:
        return a*log(t/constantes.DUREE_REVUES)+b
    return 2*ecartTacheY




BCoulTache = {'Sup' : (0.3,0.4,0.4), 
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

ICoulTache = {'Sup' : (0.6, 0.7, 0.7,1),
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


ecartYElevesTaches = 0.05 * COEF



######################################################################################  
def DefinirZones(prj, ctx):
    """ Calcule les positions et dimensions des différentes zones de tracé
        en fonction du nombre d'éléments (élèves, tâches, compétences)
    """
    global ecartTacheY, intituleTaches, fontIntTaches, xEleves, yEleves, a, b, yTaches, wColComp
    
    #
    # Zone du tableau des compétences - X
    #

#    wColComp = prj.GetReferentiel().calculerLargeurCompetences(wColCompBase)
    competences = regrouperLst(prj, prj.GetCompetencesUtil())
    tailleZComp[0] = wColComp * len(competences)
    posZComp[0] = posZOrganis[0] + tailleZOrganis[0] - tailleZComp[0]
    for i, s in enumerate(competences):
        xComp[s] = posZComp[0] + (i+0.5) * wColComp
    
    #
    # Zone du tableau des élèves
    #
    tailleZElevesV[0] = wEleves * len(prj.eleves)
    tailleZElevesH[1] = hEleves * len(prj.eleves)
    posZElevesV[0] = posZComp[0] - tailleZElevesV[0] - ecartX/2
    tailleZElevesH[0] = posZElevesV[0]-posZElevesH[0]- ecartX/2
    tailleZElevesV[1] = posZOrganis[1] + tailleZOrganis[1] - posZElevesV[1]
    xEleves = []
    yEleves = []
    for i in range(len(prj.eleves)):
        xEleves.append(posZElevesV[0] + (i+0.5) * wEleves)
        yEleves.append(posZElevesH[1] + (i+0.5) * hEleves)


    # Zone du tableau des compétences - Y
    posZComp[1] = posZElevesH[1] + tailleZElevesH[1]
    tailleZComp[1] = ecartYElevesTaches            
                 
                 
    # Zone de déroulement du projet
    posZDeroul[1] = posZElevesH[1] + tailleZElevesH[1] + tailleZComp[1] - ecartY/2
    tailleZDeroul[0] = posZElevesV[0] - posZDeroul[0] - ecartX/2
    tailleZDeroul[1] = posZOrganis[1] + tailleZOrganis[1] - posZDeroul[1]
    
    
    # Zone des tâches
    yTaches = []
    posZTaches[1] = posZDeroul[1] + ecartY/2
    tailleZTaches[0] = posZDeroul[0] + tailleZDeroul[0] - posZTaches[0] - ecartX/2
    tailleZTaches[1] = tailleZDeroul[1] - ecartY/2 - 0.04 * COEF    # écart pour la durée totale
    
    calculCoefCalcH(prj, ctx, hTacheMini)
    if a < 0:   # Trop de tâches -> on réduit !
        calculCoefCalcH(prj, ctx, hTacheMini/2)



def calculCoefCalcH(prj, ctx, hm):
    global ecartTacheY, a, b
    ecartTacheY = ecartY/3
    sommeEcarts = (prj.GetNbrPhases()-1)*ecartTacheY
    
    # Calcul des paramètres de la fonction hauteur = f(durée)
    # hauteur = a * log(durée) + b
    b = 0
    a = 1
    h = 0#ecartTacheY
    nt = 0 # nombre de tâches de hauteur variable ( = calculée par calcH() )
    hrv = 0 # Hauteur totale des revues différenciant les élèves
    hrf = 0 # Hauteur totale des revues de taille fixe
    for t in prj.taches:
        if t.phase in ["R1", "R2", "R3", "S"]:
            if t.DiffereSuivantEleve():
                hrv += max(len(t.projet.eleves) * hRevue, hRevue)
            else:
                hrf += hRevue
        else:
            h += calcH(t.GetDuree())
            nt += 1
    
#    hr = (prj.nbrRevues+1)*len(prj.eleves)*hRevue
    
    
#    hr = (len(prj.taches)-nt)*len(prj.eleves)*hRevue

    b = hm # Hauteur mini
    
    hFixe = sommeEcarts + hrv + hrf

    if h != 0:
        a = (tailleZTaches[1] - hFixe - b*nt) / h

    

    
    
    
######################################################################################  
def getCoulComp(partie, alpha = 1.0):
    if partie in ICoulComp.keys():
        return (ICoulComp[partie][0], ICoulComp[partie][1], ICoulComp[partie][2], alpha)  
    return (ICoulComp[''][0], ICoulComp[''][1], ICoulComp[''][2], alpha)
    
######################################################################################  
def getPts(lst_rect):
        lst = []
        for rect in lst_rect:
            lst.append(rect[:2])
        return lst
    
######################################################################################  
def Draw(ctx, prj, mouchard = False, pourDossierValidation = False):
    """ Dessine une fiche de séquence de la séquence <prj>
        dans un contexte cairo <ctx>
    """
    
#        print "Draw séquence"
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
    
    DefinirZones(prj, ctx)

    #
    #    pour stocker des zones caractéristiques (à cliquer, ...)
    #
    prj.zones_sens = []
    prj.pt_caract = []

    
    #
    # Type d'enseignement
    #
    tailleTypeEns = taillePro[0]/2
    t = prj.classe.referentiel.Enseignement[0]
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_BOLD)
    ctx.set_source_rgb (0.6, 0.6, 0.9)
    
    h = taillePos[1] * 0.8
    show_text_rect(ctx, t, (posPro[0] , posPos[1], tailleTypeEns, h), 
                   va = 'c', ha = 'g', b = 0, orient = 'h', 
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                   coulBord = (0, 0, 0))
    
    t = prj.classe.referentiel.Enseignement[1]
    ctx.set_source_rgb (0.3, 0.3, 0.8)
    show_text_rect(ctx, t, (posPro[0] , posPos[1] + h, tailleTypeEns, taillePos[1] - h), 
                   va = 'c', ha = 'g', b = 0, orient = 'h', 
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False)
    

    #
    # Position dans l'année
    #
#    posPos[0] = posEqu[0] + tailleEqu[0] + ecartX + tailleTypeEns
    posPos[0] = posNom[0] + tailleNom[0] + ecartX + tailleTypeEns
#    taillePos[0] =  0.72414 - posPos[0] - margeX
    taillePos[0] = taillePro[0]/2
    ctx.set_line_width (0.0015 * COEF)
    r = (posPos[0], posPos[1], taillePos[0], taillePos[1])
    rects = DrawPeriodes(ctx, r, prj.position, prj.classe.referentiel.periodes,
#                               [p.periode for p in prj.classe.referentiel.projets.values()],  
                               prj.classe.referentiel.projets,
                               tailleTypeEns = tailleTypeEns)
    
    for i, re in enumerate(rects):
        prj.zones_sens.append(Zone([re], param = "POS"+str(i)))
    prj.zones_sens.append(Zone([r], param = "POS"))



    #
    # Etablissement
    #
    if prj.classe.etablissement != u"":
        t = prj.classe.etablissement + u" (" + prj.classe.ville + u")"
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                          cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, t, (posPos[0] , posPos[1]+taillePos[1], taillePos[0], posPro[1]-posPos[1]-taillePos[1]), 
                       va = 'c', ha = 'g', b = 0.2, orient = 'h', 
                       fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                       coulBord = (0, 0, 0))

    
    #
    # Image
    #
#    prj.support.rect = []
    prj.support.pts_caract = []
    bmp = prj.support.image
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
        ctx.translate(posImg[0], posImg[1])
        ctx.scale(s, s)
        ctx.set_source_surface(image, 0, 0)
        ctx.paint ()
        ctx.restore()
        
        prj.zones_sens.append(Zone([posImg + tailleImg], obj = prj.support))
        prj.support.pts_caract.append(posImg)
    


    #
    #  Equipe
    #
    rectEqu = posEqu + tailleEqu
    prj.pt_caract.append(curve_rect_titre(ctx, u"Equipe pédagogique",  rectEqu, 
                                          BcoulEqu, IcoulEqu, fontEqu))
    
    lstTexte = []
    g = None
    c = []
    for i, p in enumerate(prj.equipe):
        lstTexte.append(p.GetNomPrenom(disc = constantes.AFFICHER_DISC_FICHE))
        if p.referent:
            g = i
        c.append(constantes.COUL_DISCIPLINES[p.discipline])
    lstCodes = [u" \u25CF"] * len(lstTexte)

   
    if len(lstTexte) > 0:
        r = liste_code_texte(ctx, lstCodes, lstTexte, 
                             posEqu[0], posEqu[1], tailleEqu[0], tailleEqu[1]+0.0001 * COEF,
                             0.1*tailleEqu[1]+0.0001 * COEF, 0.1,
                             gras = g, lstCoul = c, va = 'c')

    
    for i, p in enumerate(prj.equipe):
        prj.zones_sens.append(Zone([r[i]], obj = p))
    prj.zones_sens.append(Zone([rectEqu], param = "EQU"))
    

    #
    #  Problématique
    #
    prj.pt_caract.append(posPro)
    rectPro = posPro + taillePro
    prj.pt_caract.append(curve_rect_titre(ctx, u"Problématique",  rectPro, BcoulPro, IcoulPro, fontPro))
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_NORMAL)
    show_text_rect(ctx, constantes.ellipsizer(prj.problematique, constantes.LONG_MAX_PROBLEMATIQUE), 
                   rectPro, ha = 'g', b = 0.5,
                   fontsizeMinMax = (-1, 0.016 * COEF))
    prj.zones_sens.append(Zone([rectPro], param = "PB"))
    
#    print "     6 ", time.time() - tps


    #
    #  Projet
    #
    prj.pt_caract = []
    prj.pts_caract = []
    rectNom = posNom+tailleNom
    prj.pts_caract.append(curve_rect_titre(ctx, prj.GetCode(),  
                                                   rectNom, BcoulNom, IcoulNom, fontNom))
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_NORMAL)
    show_text_rect(ctx, prj.GetNom(), 
                   rectNom, ha = 'c', b = 0.2,
                   fontsizeMinMax = (-1, 0.016 * COEF))
    
    prj.zones_sens.append(Zone([rectNom], obj = prj))
    prj.pts_caract.append(posNom)

    
    
    #
    #  Support
    #
    prj.support.pt_caract = []
    rectSup = posSup+tailleSup
    prj.support.pts_caract.append(curve_rect_titre(ctx, prj.support.GetCode(),  
                                                   rectSup, BcoulSup, IcoulSup, fontSup))
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_NORMAL)
    show_text_rect(ctx, prj.support.GetNom(), 
                   rectSup, ha = 'c', b = 0.2,
                   fontsizeMinMax = (-1, 0.016 * COEF))
    
    prj.zones_sens.append(Zone([rectSup], obj = prj.support))
    prj.support.pts_caract.append(posSup)



    #
    #  Tableau des compétenecs
    #    
    competences = regrouperLst(prj, prj.GetCompetencesUtil())
    prj.pt_caract_comp = []
    
    if competences != []:
        
        ctx.set_line_width(0.001 * COEF)
        wc = tailleZComp[0]/len(competences)
        _x = posZComp[0]
        _y0, _y1 = posZElevesH[1], posZDeroul[1] + tailleZDeroul[1]
        
        for s in competences:
#            s.rect=((_x, _y, wc, posZTaches[1] - posZComp[1]),)
            ctx.set_source_rgb(0, 0, 0)
            ctx.move_to(_x, _y0)# + posZTaches[1] - posZComp[1])
            ctx.line_to(_x, _y1)
            ctx.stroke()
            ctx.set_source_rgba(0.5, 0.5, 0.5, 0.2)
            ctx.rectangle(_x, _y0,  
                          wc, _y1-_y0)
            ctx.fill()
            _x += wc
        ctx.set_source_rgb(0, 0, 0)
        ctx.move_to(_x, _y0)# + posZTaches[1] - posZComp[1])
        ctx.line_to(_x, _y1)   
        ctx.stroke()
        
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.001 * COEF)
        p = tableauV(ctx, competences, posZComp[0], posZComp[1], 
                tailleZComp[0], tailleZComp[1], 
                0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', coul = BCoulCompS)
        
        prj.pt_caract_comp = getPts(p)

#    print "compétences", time.time() - tps


    #
    #  Tableau des élèves
    #   
#    tps = time.time()
    ctx.select_font_face(font_family, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(0.001 * COEF)
    l=[]
    for i,e in enumerate(prj.eleves) : 
        e.pts_caract = []
        if pourDossierValidation:
            l.append(u"Elève "+str(i+1))
        else:
            l.append(e.GetNomPrenom())
    
    
    #
    # Graduation
    #
    y = posZElevesH[1] + tailleZElevesH[1]
    w = tailleZElevesH[0]
    h = hEleves/2
    for t, ha in [("0%", 'g'), ("50%", 'c'), ("100%", 'd')]:
        show_text_rect(ctx, t, 
                       (posZElevesH[0], y, w, h), ha = ha, b = 0.1,
                       fontsizeMinMax = (-1, 0.016 * COEF))
    
    prj.pt_caract_eleve = []
    if len(l) > 0:
        
        #
        # Barres d'évaluabilité
        #
        for i, e in enumerate(prj.eleves):
            ev = e.GetEvaluabilite(compil = True)[1]
            y = posZElevesH[1] + i*hEleves
#            wr = tailleZElevesH[0]*r
#            ws = tailleZElevesH[0]*s
            hb = hEleves/(len(prj.GetProjetRef().parties)+1)
#            y = posZElevesH[1] + (2*i*hb)+hb/2
            

            
            for j, part in enumerate(prj.GetProjetRef().parties.keys()):
                
                barreH(ctx, posZElevesH[0], y+(j+1)*hb, tailleZElevesH[0], ev[part][0], ev[part][1], hb, 
                       (1, 0, 0, 0.7), (0, 1, 0, 0.7), 
                       getCoulComp(part))
            
            

        rec = tableauH(ctx, l, posZElevesH[0], posZElevesH[1], 
                     tailleZElevesH[0], 0, tailleZElevesH[1], 
                     va = 'c', ha = 'd', orient = 'h', coul = CoulAltern)
        
        prj.pt_caract_eleve = getPts(rec)
        
        #
        # Lignes horizontales
        #
        for i, e in enumerate(prj.eleves):
            prj.zones_sens.append(Zone([rec[i]], obj = e))
            Ic = CoulAltern[i][0]
            
            ctx.set_source_rgb(Ic[0],Ic[1],Ic[2])
            ctx.set_line_width(0.003 * COEF)
            ctx.move_to(posZElevesH[0]+tailleZElevesH[0], yEleves[i])
            ctx.line_to(posZComp[0]+tailleZComp[0], yEleves[i])
            ctx.stroke()
        
        #
        # Lignes verticales
        #
        for i, e in enumerate(prj.eleves):
            Ic = CoulAltern[i][0]
            
            ctx.set_source_rgb(Ic[0],Ic[1],Ic[2])
            ctx.set_line_width(0.003 * COEF)
            ctx.move_to(xEleves[i], yEleves[i])
            ctx.line_to(xEleves[i], posZTaches[1] + tailleZTaches[1] + (i % 2)*(ecartY/2) + ecartY/2)
            ctx.stroke()    
            DrawCroisementsElevesCompetences(ctx, e, yEleves[i])
        
        #
        # Ombres des lignes verticales
        #
        e = 0.003 * COEF
        ctx.set_line_width(0.003 * COEF)
        for i in range(len(prj.eleves)) :
            y = posZTaches[1] + tailleZTaches[1] + (i % 2)*(ecartY/2) + ecartY/2
            ctx.set_source_rgb(1,1,1)
            ctx.move_to(xEleves[i]+e, yEleves[i]+e)
            ctx.line_to(xEleves[i]+e, y)
            ctx.move_to(xEleves[i]-e, yEleves[i]+e)
            ctx.line_to(xEleves[i]-e, y)
        ctx.stroke()
    
#    print "élèves", time.time() - tps
    
    #
    #  Tâches
    #
#    tps = time.time()
    curve_rect_titre(ctx, u"Tâches à réaliser",  
                     (posZDeroul[0], posZDeroul[1], 
                      tailleZDeroul[0], tailleZDeroul[1]), 
                     BcoulZDeroul, IcoulZDeroul, fontZDeroul)
    
    y = posZTaches[1] - ecartTacheY
    
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
    for t in prj.taches:
        if t.phase == "R1":
            y1 = y
        elif t.phase == "R2":
            y2 = y
        elif t.phase == "R3":
            y3 = y
            
        if phase != t.phase:
            y += ecartTacheY

        if t.phase != '':  
            yb = DrawTacheRacine(ctx, t, y)
            if t.phase in ["Ana", "Con", "DCo", "Rea", "Val", 'XXX'] :
                yh_phase[t.phase][0].append(y)
                yh_phase[t.phase][1].append(yb)
            y = yb
            
        
        phase = t.phase
#    print "    ", time.time() - tps
    #
    # Les lignes horizontales en face des taches
    # et les croisements Tâche/Competences
    #
    x = posZTaches[0] + tailleZTaches[0]
    for t, y in yTaches: 
        if not t.phase in ["R1", "R2", "R3", "S", "Rev"]:
            DrawLigne(ctx, x, y)
        if (t.phase in ["R1", "R2", "R3", "S"] and t.DiffereSuivantEleve()) or t.estPredeterminee():
            dy = hRevue
            y = y - ((len(prj.eleves)-1)*dy)/2
#            print "phase = ", t.phase
            h = 0.006 * COEF
            for eleve in prj.eleves:
                DrawCroisementsCompetencesRevue(ctx, t, eleve, y, h)
                y += dy
        else:
            DrawCroisementsCompetencesTaches(ctx, t, y)
    
    # Nom des phases
    for phase, yh in yh_phase.items():
#        print phase, yh
        if len(yh[0]) > 0:
            yh[0] = min(yh[0])
            yh[1] = max(yh[1])
            ctx.set_source_rgb(BCoulTache[phase][0],BCoulTache[phase][1],BCoulTache[phase][2])
            ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                                                cairo.FONT_WEIGHT_NORMAL)
            if wPhases > yh[1]-yh[0]:
                orient = "h"
            else:
                orient = "v"
            try:
                n = prj.GetProjetRef().phases[phase][1]
            except KeyError:
                n = ""
            show_text_rect(ctx, n, 
                           (posZDeroul[0] + ecartX/6, yh[0], 
                            wPhases, yh[1]-yh[0]), 
                           ha = 'c', orient = orient, b = 0.1, le = 0.7,
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
#    tps = time.time()
    posEpreuve = prj.GetProjetRef().periode[0] - 1
    if prj.position == posEpreuve:
        y0 = posZTaches[1]
        y4 = y1+len(prj.eleves) * hRevue + 2*ecartTacheY
#        y4 = y1+2*ecartTacheY + 0.015
#        y5 = y2+2*ecartTacheY + 0.015
        y5 = y2+len(prj.eleves) * hRevue + 2*ecartTacheY
        md1 = md2 = md3 = 0
        for i, e in enumerate(prj.eleves):
            md1 = max(e.GetDuree(phase = "R1"), md1)
            md2 = max(e.GetDuree(phase = "R2"), md2)
            md3 = max(e.GetDuree(phase = "R3"), md3)
            
        for i, e in enumerate(prj.eleves):
            d1 = e.GetDuree(phase = "R1")
            d2 = e.GetDuree(phase = "R2")
            d3 = e.GetDuree(phase = "R3")
            Ic = CoulAltern[i][0]
            ctx.set_source_rgb(Ic[0],Ic[1],Ic[2])
            ctx.set_line_width(0.005 * COEF)
            if md1 > 0:
                ctx.move_to(xEleves[i], y0)
                ctx.line_to(xEleves[i], y0+(y1-y0)*d1/md1)
                ctx.stroke()
            if md2 > 0:
                ctx.move_to(xEleves[i], y4)
                ctx.line_to(xEleves[i], y4+(y2-y4)*d2/md2)
                ctx.stroke()
            if md3 > 0:
                ctx.move_to(xEleves[i], y5)
                ctx.line_to(xEleves[i], y5+(y3-y5)*d3/md3)
                ctx.stroke()
    
#    print "durées", time.time() - tps
    
    
    
    #
    # Croisements élèves/tâches
    #
#    tps = time.time()
    for t, y in yTaches: 
        DrawCroisementsElevesTaches(ctx, t, y)
        
#    print "CroisementsElevesTaches", time.time() - tps
    
    #
    # Durées du projet (durées élèves)
    #
#    tps = time.time()
    for i, e in enumerate(prj.eleves):
#        x = posZElevesV[0]+i*tailleZElevesV[0]/len(prj.eleves)-wEleves/2
        x = xEleves[i]-wEleves*3/4
        y = posZTaches[1] + tailleZTaches[1] + (i % 2)*(ecartY/2)+ecartY/2
        d = e.GetDuree()
        dureeRef = prj.GetProjetRef().duree
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
                       (x, y, wEleves*3/2, ecartY/2), ha = 'c', b = 0)
    
#    print "dureeProjet", time.time() - tps
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
    ctx.set_source_rgba (0.6, 0.8, 0.6)
    ctx.set_line_width (0.001 * COEF)
    ctx.set_dash(dashes, 0)
    ctx.move_to(x, posZElevesV[1] + tailleZElevesV[1])
    ctx.line_to(x, y)
    ctx.stroke()
    ctx.set_dash([], 0)

    


    
######################################################################################  
def DrawTacheRacine(ctx, tache, y):
    global yTaches
    
    h = calcH_tache(tache)
    
    #
    # Flèche verticale indiquant la durée de la tâche
    #
    if not tache.phase in ["R1", "R2", "R3", "S", "Rev"]:
#        fleche_verticale(ctx, posZTaches[0] - wDuree/2 - ecartX/4, y, 
#                         h, wDuree, (0.9,0.8,0.8,0.5))
        
        ctx.set_source_rgba (0.9,0.8,0.8,0.5)
        x = posZTaches[0] - wDuree - ecartX/4
        ctx.rectangle(x, y, wDuree, h)
        ctx.fill_preserve ()    
        ctx.set_source_rgba(0.4,  0.4,  0.4,  1)
        ctx.set_line_width(0.0006 * COEF)
        ctx.stroke ()
        
        ctx.set_source_rgb(0.5,0.8,0.8)
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
        
        if h > wDuree:
            show_text_rect(ctx, getHoraireTxt(tache.GetDuree()), 
                       (x, y, wDuree, h), 
                       orient = 'v', b = 0.1)
        else:
            show_text_rect(ctx, getHoraireTxt(tache.GetDuree()), 
                       (x, y, wDuree, h), 
                       orient = 'h', b = 0.1)
    
    #
    # Indication du délai pour revue
    #
    elif tache.phase in ["R1", "R2", "R3", "Rev"]:
        ctx.set_source_rgba (0.9,0.8,0.8,0.5)
        if tache.phase == "Rev":
            x = posZTaches[0] - wDuree - ecartX/4
            w = wDuree*3
        else:
            x = posZTaches[0] - wDuree*4 - ecartX/4
            w = wDuree*3
        ctx.rectangle(x, y, w, h)
        ctx.fill_preserve ()    
        ctx.set_source_rgba(0.4,  0.4,  0.4,  1)
        ctx.set_line_width(0.0006 * COEF)
        ctx.stroke ()
        
        ctx.set_source_rgb(0.5,0.8,0.8)
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
        show_text_rect(ctx, getHoraireTxt(tache.GetDelai(), constantes.CHAR_FLECHE), 
                       (x, y, w, h), 
                       orient = 'h', fontsizeMinMax = (minFont, 0.015 * COEF), b = 0.1, couper = False)
    

    
    #
    # Rectangles actifs et points caractéristiques : initialisation
    #
    tache.pts_caract = []
    
    
    
    #
    # Tracé du cadre de la tâche
    #
    if tache.phase == "Rev":
        x = posZTaches[0] + wDuree*2
        w = posZComp[0] + tailleZComp[0] + ecartX/4 - x
    elif not tache.phase in ["R1", "R2", "R3", "S"]:
        x = posZTaches[0]
        w = tailleZTaches[0]
    else:
        x = posZTaches[0] - wDuree/2 - ecartX/4
        w = posZComp[0] + tailleZComp[0] + ecartX/4 - x

    tache.pts_caract.append((x, y))
        
    ctx.set_line_width(0.002 * COEF)
    rectangle_plein(ctx, x, y, w, h, 
                    BCoulTache[tache.phase], ICoulTache[tache.phase], ICoulTache[tache.phase][3])
    
    
    #
    # Affichage du code de la tâche
    #
    if hasattr(tache, 'code'):
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
        ctx.set_source_rgb (0,0,0)
        
        if not tache.phase in ["R1", "R2", "R3", "S"]:
            t = tache.code
            hc = max(hTacheMini/2, 0.01 * COEF)
        else:
            t = tache.intitule
            hc = h
        show_text_rect(ctx, t, (x, y, tailleZTaches[0], hc), ha = 'g', 
                       wrap = False, fontsizeMinMax = (minFont, 0.02 * COEF), b = 0.2)
    
    
    #
    # Affichage de l'intitulé de la tâche
    #
    if tache.intituleDansDeroul and tache.intitule != "" and not tache.phase in ["R1", "R2", "R3", "S"]:
        ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb (0,0,0)
        
        # Si on ne peut pas afficher l'intitulé dessous, on le met à coté
        if h-hc < minFont:
            width = ctx.text_extents(t)[2]*1.2
            rect = (x + width, y, tailleZTaches[0] - width, hc)
        else:
            rect = (x, y + hc, tailleZTaches[0], h-hc)
        if rect[2] > 0:
            show_text_rect(ctx, tache.GetIntit(), rect, 
                           ha = 'g', fontsizeMinMax = (minFont, 0.015 * COEF))
        
    tache.GetDocument().zones_sens.append(Zone([(x, y, tailleZTaches[0], h)], obj = tache))
#    tache.rect.append([x, y, tailleZTaches[0], h])
        
        
    #
    # Tracé des croisements "Tâches" et "Eleves"
    #
    yTaches.append([tache, y+h/2])
#    DrawCroisementsCompetencesTaches(ctx, tache, y + h/2)
    
    
    
    y += h
    return y
        
        
        
######################################################################################  
def DrawLigne(ctx, x, y, gras = False):
    dashes = [ 0.002 * COEF,   # ink
               0.002 * COEF,   # skip
               0.002 * COEF,   # ink
               0.002 * COEF,   # skip
               ]
    ctx.set_source_rgba (0, 0.0, 0.2, 0.6)
    if gras:
        ctx.set_line_width (0.002 * COEF)
    else:
        ctx.set_line_width (0.001 * COEF)
    ctx.set_dash(dashes, 0)
    ctx.move_to(posZOrganis[0]+tailleZOrganis[0], y)
    ctx.line_to(x, y)
    ctx.stroke()
    ctx.set_dash([], 0)       
    
######################################################################################  
def regrouperDic(obj, dicIndicateurs):
#    print "regrouperDic", dicIndicateurs
#    print "   _dicoCompetences", obj.GetProjetRef()._dicoCompetences
    if obj.GetProjetRef()._niveau == 3:
        dic = {}
        typ = {}
        for disc, tousIndicateurs in obj.GetProjetRef()._dicoCompetences.items():
            for k0, v0 in tousIndicateurs.items():
                for k1, v1 in v0[1].items():
                    dic[disc+k1] = []
                    typ[disc+k1] = []
                    lk2 = v1[1].keys()
                    lk2.sort()
    #                print "  ", lk2
                    for k2 in lk2:
                        if disc+k2 in dicIndicateurs.keys():
                            dic[disc+k1].extend(dicIndicateurs[disc+k2])
    #                        print "   **", v1[1][k2]
                            typ[disc+k1].extend([p.poids for p in v1[1][k2][1]])
                        else:
                            l = len(v1[1][k2][1])
                            dic[disc+k1].extend([False]*l)
                            typ[disc+k1].extend(['']*l)
                    
                    if dic[disc+k1] == [] or not (True in dic[disc+k1]):
                        del dic[disc+k1]
                        del typ[disc+k1]
                    
#        print "  >>", dic
#        print "    ", typ
        return dic, typ
    else:
        typ = {}
        for k in dicIndicateurs.keys():
            typ[k] = [p.poids for p in obj.GetProjetRef().getIndicateur(k)]
#        print "  >>>", dicIndicateurs, typ
        return dicIndicateurs, typ
     
######################################################################################  
def regrouperLst(obj, lstCompetences):
#    print "regrouperLst", lstCompetences
#    print "   _dicoCompetences", obj.GetProjetRef()._dicoCompetences["S"]
    lstCompetences.sort()
    if obj.GetProjetRef()._niveau == 3:
        lstGrpCompetences = []
        for disc, tousIndicateurs in obj.GetProjetRef()._dicoCompetences.items():
            dic = []
            for k0, v0 in tousIndicateurs.items():
                for k1, v1 in v0[1].items():
                    for k2 in sorted(v1[1].keys()):
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
def DrawCroisementsCompetencesTaches(ctx, tache, y):
    DrawBoutonCompetence(ctx, tache, regrouperDic(tache, tache.GetDicIndicateurs()), y)
    

######################################################################################  
def DrawCroisementsCompetencesRevue(ctx, revue, eleve, y, h):
#    print "DrawCroisementsCompetencesRevue", eleve, revue.phase
#    print "   ", revue.GetDicIndicateursEleve(eleve)
    DrawBoutonCompetence(ctx, revue, regrouperDic(revue, revue.GetDicIndicateursEleve(eleve)), y, h)
    
#####################################################################################  
def DrawCroisementsElevesTaches(ctx, tache, y):
    """ Dessine les "boules"
    """ 
    #
    # Croisements Tâche/Eleves
    #
    if tache.phase in ["R1", "R2", "R3", "S"]:
        differeSuivantEleve = tache.DiffereSuivantEleve()
    else:
        differeSuivantEleve = tache.estPredeterminee()
        
#    if tache.phase in ["R1", "R2", "R3", "S"] and differeSuivantEleve: 
    if differeSuivantEleve: 
        lstElv = range(len(tache.projet.eleves))
    else:
        lstElv = tache.eleves
    
#    if tache.phase in ["R1", "R2", "R3", "S"] and differeSuivantEleve:
    if differeSuivantEleve: 
        dy = hRevue
        y = y - ((len(tache.projet.eleves)-1)*dy)/2
        r = 0.005 * COEF
    else:
        dy = 0
        r = 0.006 * COEF
        
    for i in lstElv:
#        if tache.phase in ["R1", "R2", "R3", "S"] and differeSuivantEleve:
        if differeSuivantEleve: 
            color1 = BCoulTache[tache.phase]
            color0 = (1, 1, 1, 1)
        else:
            color0 = CoulAltern[i][0]
            color1 = CoulAltern[i][1]

        _x = xEleves[i]
        boule(ctx, _x, y, r, 
              color0 = color0, color1 = color1,
              transparent = False)
        
        tache.GetDocument().zones_sens.append(Zone([(_x -r , y - r, 2*r, 2*r)], 
                                                   obj = [tache.projet.eleves[i], tache]))
        
#        tache.projet.eleves[i].rect.append((_x -r , y - r, 2*r, 2*r))
        tache.projet.eleves[i].pts_caract.append((_x,y))
        y += dy
        

######################################################################################  
def DrawCroisementsElevesCompetences(ctx, eleve, y):
    #
    # Boutons
    #
    DrawBoutonCompetence(ctx, eleve, regrouperDic(eleve, eleve.GetDicIndicateurs()), y)
    

    
######################################################################################  
def DrawBoutonCompetence(ctx, objet, dicIndic, y, h = None):
    """ Dessine les petits rectangles des indicateurs (en couleurs R et S)
         ... avec un petit décalage vertical pour que ce soit lisible en version N&B
    """
#    print "DrawBoutonCompetence", objet, dicIndic
    if h == None: # Toujours sauf pour les revues
        r = wColComp/3
        h = 2*r
    
    # Un petit décalage pour distinguer R et S en N&B    
    dh = h/10
    ctx.set_line_width (0.0004 * COEF)
    dicIndic, dictype = dicIndic
 
    for s in dicIndic.keys():
        
        x = xComp[s]-wColComp/2
        
        rect = (x, y-h/2, wColComp, h)
        
        objet.GetDocument().zones_sens.append(Zone([rect], obj = objet, param = s))
        
#        if s in objet.GetDocument().rectComp.keys() and objet.GetDocument().rectComp[s] != None:
#            objet.GetDocument().rectComp[s].append(rect)
#        else:
#            objet.GetDocument().rectComp[s] = [rect]
        
        objet.pts_caract.append((x,y))
        
        indic = dicIndic[s]
#            dangle = 2*pi/len(indic)
        dx = wColComp/len(indic)
        for a, i in enumerate(indic):
            if i: # Rose ou bleu
#                print "   ", s, a
                part = dictype[s][a].keys()[0]
                if part == 'S':
#                if dictype[s][a][1] != 0:   #objet.projet.classe.GetReferentiel().getTypeIndicateur(s+'_'+str(a+1)) == "C": # Conduite     #dicIndicateurs_prj[s][a][1]:
                    d = -1
                else:
                    d = 1
                ctx.set_source_rgba (*getCoulComp(part))
            else: # Rien => Transparent
                d = 0
                ctx.set_source_rgba (1, 1, 1, 0)
            if d != 0:
                ctx.rectangle(x+a*dx, y-h/2+d*dh, dx, h-dh)
                ctx.fill_preserve ()
            else:
                ctx.move_to(x+a*dx, y-h/2+dh)
                ctx.rel_line_to(0, h-4*dh)
                ctx.move_to(x+a*dx+dx, y-h/2+dh)
                ctx.rel_line_to(0, h-4*dh)

            
            ctx.set_source_rgba (0, 0 , 0, 1)
            ctx.stroke()


       
