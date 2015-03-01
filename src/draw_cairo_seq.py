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

from constantes import Effectifs,COUL_COMPETENCES, mergeDict, getSingulierPluriel
                        #getSavoir, getCompetence, \ NomsEffectifs, listeDemarches, Demarches, \
                        #DemarchesCourt, 
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
margeX = 0.02
margeY = 0.03

# Ecarts
ecartX = 0.02
ecartY = 0.02




# CI
tailleCI = (0.17, 0.085)
#posCI = (posPre[0] + taillePre[0]+ecartX, 0.1)
posCI = (margeX, margeY)
IcoulCI = (0.9, 0.8, 0.8, 0.85)
BcoulCI = (0.3, 0.2, 0.25, 1)
fontCI = 0.014


# Rectangle des prerequis
taillePre = (0.29, 0.18 - tailleCI[1] - ecartY)
posPre = (margeX, posCI[1] + tailleCI[1] + ecartY)
IcoulPre = (0.8, 0.8, 0.9, 0.85)
BcoulPre = (0.2, 0.25, 0.3, 1)
fontPre = 0.014

# Position dans l'année
posPos = [None, margeY - ecartY/2]
taillePos = [None, 0.04]
IcoulPos = (0.8, 0.8, 1, 0.85)
BcoulPos = (0.1, 0.1, 0.25, 1)
AcoulPos = (1, 0.4, 0, 1)
fontPos = 0.014


# Rectangle des objectifs
posObj = (posPre[0] + taillePre[0] + ecartX/2, margeY + taillePos[1] + ecartY/2)
tailleObj = [LargeurTotale - margeX - posObj[0], posPre[1] + taillePre[1] - posObj[1]]
IcoulObj = (0.8, 0.9, 0.8, 0.85)
BcoulObj = (0.25, 0.3, 0.2, 1)
fontObj = 0.014

# Cible
posCib = [posCI[0] + tailleCI[0] + ecartX/4, margeY - ecartY/2]
tailleCib = [posObj[0] - posCI[0] - tailleCI[0] - ecartX/2, None]
tailleCib[1] = tailleCib[0] 
IcoulCib = (0.8, 0.8, 1, 0.85)
BcoulCib = (0.1, 0.1, 0.25, 1)
centreCib = (posCib[0] + tailleCib[0] / 2 + 0.0006, posCib[1] + tailleCib[0] / 2 - 0.004)


# Zone de commentaire
fontIntComm = 0.01
posComm = [margeX, None]
tailleComm = [LargeurTotale-2*margeX, None]
intComm = []

# Zone d'organisation de la séquence (intérieur du grand cadre vert - bordure)
bordureZOrganis = 0.01
posZOrganis = (margeX+bordureZOrganis, 0.24)
tailleZOrganis = [LargeurTotale-2*(margeX+bordureZOrganis), None]


# Rectangle de l'intitulé
tailleIntitule = [0.4, 0.04]
posIntitule = [(LargeurTotale-tailleIntitule[0])/2, posZOrganis[1]-tailleIntitule[1]]
IcoulIntitule = (0.98, 0.99, 0.98, 0.8)
BcoulIntitule = (0.2, 0.8, 0.2, 1)
FontIntitule = 0.02

# Zone de déroulement de la séquence
posZDeroul = (margeX+ecartX, posZOrganis[1]+0.06)
tailleZDeroul = [None, None]

# Zone du tableau des Systèmes
posZSysteme = [None, posZOrganis[1]+0.01]
tailleZSysteme = [None, None]
wColSysteme = 0.025
xSystemes = {}

# Zone du tableau des démarches
posZDemarche = [None, posZSysteme[1]]
tailleZDemarche = [0.07, None]
xDemarche = {"I" : None,
             "R" : None,
             "P" : None}

# Zone des intitulés des séances
fontIntSeances = 0.01
posZIntSeances = [0.06, None]
tailleZIntSeances = [LargeurTotale-0.12, None]
hIntSeance = 0.02
intituleSeances = []

# Zone des séances
largeFlecheDuree = 0.02
posZSeances = (margeX+ecartX+largeFlecheDuree, posZOrganis[1]+0.08)
tailleZSeances = [None, None]
wEff =  {"C" : None,
         "G" : None,
         "D" : None,
         "E" : None,
         "P" : None,
         }
#hHoraire = None
ecartSeanceY = None
BCoulSeance = {"ED" : (0.3,0.5,0.5), 
               "AP" : (0.5,0.3,0.5), 
               "P"  : (0.5,0.5,0.3), 
               "C"  : (0.3,0.3,0.7), 
               "TD" : (0.3,0.5,0.7),
               "SA" : (0.3,0.7,0.3), 
               "SS" : (0.4,0.5,0.4), 
               "E"  : (0.7,0.3,0.3), 
               "R"  : (0.45,0.35,0.45), 
               "S"  : (0.45,0.45,0.35)}
ICoulSeance = {"ED" : (0.6, 0.8, 0.8), 
               "AP" : (0.8, 0.6, 0.8), 
               "P"  : (0.8, 0.8, 0.6), 
               "C"  : (0.6, 0.6, 1.0),
               "TD" : (0.6,0.8,1.0),
               "SA" : (0.6, 1.0, 0.6), 
               "SS" : (0.7, 0.8, 0.7), 
               "E"  : (1.0, 0.6, 0.6), 
               "R"  : (0.75, 0.65, 0.75), 
               "S"  : (0.75, 0.75, 0.65),
               ""   : (1.0, 1.0, 1.0)}


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
    if seq.commentaires == u"":
        tailleComm[1] = 0
    else:
        tailleComm[1], intComm = calc_h_texte(ctx, u"Commentaires : " + seq.commentaires, tailleComm[0], fontIntComm)

    posComm[1] = 1-tailleComm[1]-margeY
    
    # Zone d'organisation de la séquence (grand cadre)
    tailleZOrganis[1] = posComm[1]-posZOrganis[1]-bordureZOrganis

    # Rectangle de l'intitulé
    posIntitule[1] = posZOrganis[1]-tailleIntitule[1]

    # Zone des intitulés des séances
#    print "Zone des intitulés des séances"
    #                  titres    contenus    hauteurs de ligne
    intituleSeances = [[],      [],         []]
    tailleZIntSeances[1] = 0
    
    intituleSeances[0], lstInt = seq.GetIntituleSeances()
    for intS in lstInt:
#        print "   ", intS
        h, t = calc_h_texte(ctx, intS, tailleZIntSeances[0], fontIntSeances)
        intituleSeances[2].append(h)
        intituleSeances[1].append(t)
#        intituleSeances.append([intS[0],h,t])
        tailleZIntSeances[1] += h
    

#    tailleZIntSeances[1] = len(seq.GetIntituleSeances()[0])* hIntSeance
    posZIntSeances[1] = posZOrganis[1] + tailleZOrganis[1] - tailleZIntSeances[1]
    
    # Zone du tableau des Systèmes
    systemes = seq.GetSystemesUtilises()
    tailleZSysteme[0] = wColSysteme * len(systemes)
    tailleZSysteme[1] = tailleZOrganis[1] - ecartY - tailleZIntSeances[1]
    posZSysteme[0] = posZOrganis[0] + tailleZOrganis[0] - tailleZSysteme[0]
    for i, s in enumerate(systemes):
        xSystemes[s.nom] = posZSysteme[0] + (i+0.5) * wColSysteme
    
    
    # Zone du tableau des démarches
    if len(seq.classe.GetReferentiel().listeDemarches) > 0:
        tailleZDemarche[0] = 0.07
        posZDemarche[0] = posZSysteme[0] - tailleZDemarche[0] - ecartX
        tailleZDemarche[1] = tailleZSysteme[1]
        xDemarche["I"] = posZDemarche[0] + tailleZDemarche[0]/6
        xDemarche["R"] = posZDemarche[0] + tailleZDemarche[0]*3/6
        xDemarche["P"] = posZDemarche[0] + tailleZDemarche[0]*5/6
    else:
        tailleZDemarche[0] = 0
        tailleZDemarche[1] = tailleZSysteme[1]
        posZDemarche[0] = posZSysteme[0] - tailleZDemarche[0] - ecartX
                 
    # Zone de déroulement de la séquence
    tailleZDeroul[0] = posZDemarche[0] - posZDeroul[0] - ecartX
    tailleZDeroul[1] = tailleZSysteme[1]
    
    
    # Zone des séances
    tailleZSeances[0] = tailleZDeroul[0] - ecartX# - largeFlecheDuree - ecartX - bordureZOrganis#0.05 # écart pour les durées
    tailleZSeances[1] = tailleZSysteme[1] - posZSeances[1] + posZDeroul[1] - 0.05
    wEff = {"C" : tailleZSeances[0],
             "G" : tailleZSeances[0]*6/7,
             "D" : tailleZSeances[0]*3/7,
             "E" : tailleZSeances[0]/seq.classe.nbrGroupes['E']*6/7,
             "P" : tailleZSeances[0]/seq.classe.nbrGroupes['P']*6/7,
#             "E" : tailleZSeances[0]*Effectifs["E"][1]/Effectifs["G"][1]*6/7,
#             "P" : tailleZSeances[0]*Effectifs["P"][1]/Effectifs["G"][1]*6/7,
             }
    
    ecartSeanceY = 0.006    # écart mini entre deux séances
    hmin = 0.016             # hauteur minimum d'une séance
    tmin = seq.GetDureeGraphMini() # durée minimale de séance
    n = len(seq.seances)
    d = seq.GetDureeGraph()- n*tmin
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
def Draw(ctx, seq, mouchard = False):
    """ Dessine une fiche de séquence de la séquence <seq>
        dans un contexte cairo <ctx>
    """
    
#        print "Draw séquence"
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
    
    
    #
    # Flèche
    #
    rayon = 0.30
    alpha0 = 55
    alpha1 = 155
    y = posObj[1]+tailleObj[1] - rayon*sin(alpha0*pi/180)
    fleche_ronde(ctx, 0.72414/2, y, rayon, alpha0, alpha1, 0.035, 0.06, (0.8, 0.9, 0.8, 1))
    
    
    #
    #  Cadre et Intitulé de la séquence
    #
    seq.rect = [(posZOrganis[0]-bordureZOrganis, posZOrganis[1], 
                 tailleZOrganis[0]+bordureZOrganis*2, tailleZOrganis[1]+bordureZOrganis)]
    seq.pt_caract = curve_rect_titre(ctx, seq.intitule,  
                                     seq.rect[0], 
                                     BcoulIntitule, IcoulIntitule, FontIntitule)

    
    #
    # Type d'enseignement
    #
    tailleTypeEns = tailleObj[0]/2
    t = seq.classe.referentiel.Enseignement[0]
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_BOLD)
    ctx.set_source_rgb (0.6, 0.6, 0.9)
    show_text_rect(ctx, t, (posObj[0] , posPos[1], tailleTypeEns, taillePos[1]), 
                   va = 'c', ha = 'g', b = 0, orient = 'h', 
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                   bordure = (0, 0, 0))




    #
    # Position dans l'année
    #
    posPos[0] = posPre[0] + taillePre[0] + ecartX + tailleTypeEns
    taillePos[0] =  0.72414 - posPos[0] - margeX
    ctx.set_line_width (0.0015)
    seq.rectPos = DrawPeriodes(ctx, seq.position, 
                               seq.classe.referentiel.periodes,
                               tailleTypeEns = tailleTypeEns)
    seq.rect.append(posPos+taillePos)


    #
    # Etablissement
    #
    if seq.classe.etablissement != u"":
        t = seq.classe.etablissement + u" (" + seq.classe.ville + u")"
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                          cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, t, (posPos[0] , posPos[1]+taillePos[1], taillePos[0], posObj[1]-posPos[1]-taillePos[1]), 
                       va = 'c', ha = 'g', b = 0.15, orient = 'h', 
                       fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = False,
                       bordure = (0, 0, 0))
    
    
    #
    # Cible ou Logo
    #
    seq.CI.rect = []
    
    # Affichage du Logo
    tfname = tempfile.mktemp()
    bmp = seq.classe.referentiel.getLogo()
    try:
        bmp.SaveFile(tfname, wx.BITMAP_TYPE_PNG)
        image = cairo.ImageSurface.create_from_png(tfname)
    finally:
        if os.path.exists(tfname):
            os.remove(tfname)  
    w = image.get_width()
    h = image.get_height()
    ctx.save()
    ctx.translate(posCib[0], posCib[1])
    ctx.scale(tailleCib[0]/w, tailleCib[0]/w)
    ctx.set_source_surface(image, 0, 0)
    ctx.paint ()
    ctx.restore()
        
    # Affichage des CI sur la cible
    if seq.classe.referentiel.CI_cible:
        seq.CI.rect.append((posCib+tailleCib))
        
        rayons = {"F" : tailleCib[0] * 0.28, 
                  "S" : tailleCib[0] * 0.19, 
                  "C" : tailleCib[0] * 0.1,
                  "_" : tailleCib[0] * 0.45}
        angles = {"M" : 0,
                  "E" : 120,
                  "I" : -120,
                  "_" : -98}
        
        for i, ci in enumerate(seq.CI.numCI):
            mei, fsc = seq.CI.GetPosCible(i).split("_")
            mei = mei.replace(" ", "")
            fsc = fsc.replace(" ", "")
            
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
            boule(ctx, pos[0], pos[1], 0.005, (0.95, 1, 0.9, 1), (0.1, 0.3, 0.05, 1))




    #
    # Durée de la séquence
    #
    ctx.set_source_rgb(0.5,0.8,0.8)
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_BOLD)
    show_text_rect(ctx, getHoraireTxt(seq.GetDuree()), 
                   (posZDeroul[0]-0.01, posZDemarche[1] + tailleZDemarche[1] , #- 0.015
                   0.1, 0.015), ha = 'g', b = 0)




    #
    # Commentaires
    #
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
    for i, e in enumerate(["C", "G", "D", "E", "P"]):
        x = posZSeances[0]
        h = (posZSeances[1]-posZDemarche[1]-0.01) / 5
        y = posZDemarche[1] + i * h
        w = wEff[e]
        ctx.set_line_width(0.001)
        ctx.set_source_rgb(0.8, 0.9, 0.8)
        ctx.rectangle(x, y, w, h)
        ctx.stroke()
        ctx.set_source_rgb(0.6, 0.8, 0.6)
        show_text_rect(ctx, seq.GetReferentiel().effectifs[e][1], (x, y, w, h), b=0.2)
        ctx.stroke()
        DrawLigneEff(ctx, x+w, y+h)




    #
    #  Prerequis
    #
    
    # Rectangle arrondi
    x0, y0 = posPre
    rect_width, rect_height  = taillePre
    seq.prerequis.pt_caract = (curve_rect_titre(ctx, u"Prérequis",  (x0, y0, rect_width, rect_height), BcoulPre, IcoulPre, fontPre),
                               'pre')
    
    
    #
    # Codes prerequis
    #
    lstTexte = []
    lstCodes = []
    lstCoul = []
    for c in seq.prerequis.savoirs:
        typ, cod = c[0], c[1:]
        if typ == "S": # Savoir spécialité STI2D
            lstTexte.append(seq.GetReferentiel().getSavoir(cod))
            lstCodes.append(cod)
            lstCoul.append((0,0,0))
        elif typ == "M": # Savoir Math
            lstTexte.append(seq.GetReferentiel().getSavoir(cod, gene = "M"))
            lstCodes.append("Math "+cod)
            lstCoul.append(constantes.COUL_DISCIPLINES['Mat'])
        elif typ == "P": # Savoir Physique
            lstTexte.append(seq.GetReferentiel().getSavoir(cod, gene = "P"))
            lstCodes.append("Phys "+cod)
            lstCoul.append(constantes.COUL_DISCIPLINES['Phy'])
        else:
            if seq.GetReferentiel().tr_com == []:
#            if seq.classe.typeEnseignement == 'SSI':
                lstTexte.append(seq.GetReferentiel().getSavoir(cod))
                lstCodes.append(cod)
            else:
                lstTexte.append(REFERENTIELS[seq.GetReferentiel().tr_com[0]].getSavoir(cod))
                lstCodes.append(seq.GetReferentiel().tr_com[0]+" "+cod)
            lstCoul.append((0.3,0.3,0.3))
            
        
    lstTexteS = []   
    for c in seq.prerequisSeance:
        lstTexteS.append(c.GetNomFichier())    
        
    hl = rect_height+0.0001
    
    if len(lstTexte) + len(lstTexteS) > 0:
        e = 0.008
        hC = hl*len(lstTexte)/(len(lstTexte) + len(lstTexteS))
        hS = hl*len(lstTexteS)/(len(lstTexte) + len(lstTexteS))
        r = liste_code_texte(ctx, lstCodes, lstTexte, 
                             x0, y0, rect_width, hC, e,
                             lstCoul = lstCoul)
        ctx.set_source_rgba (0.0, 0.0, 0.5, 1.0)
        seq.prerequis.pts_caract = getPts(r)
        lstRect = liste_code_texte(ctx, ["Seq."]*len(lstTexteS), lstTexteS, x0, y0+hC, rect_width, hS, 0.01)
        for i, c in enumerate(seq.prerequisSeance): 
            c.rect = [lstRect[i]]
    else:
        show_text_rect(ctx, u"Aucun", (x0, y0, rect_width, hl), fontsizeMinMax = (-1, 0.015))
    
    
    #
    #  Objectifs
    #
    x0, y0 = posObj
#    tailleObj[0] =  taillePos[0]
    rect_width, rect_height  = tailleObj
    seq.obj["S"].pt_caract = (curve_rect_titre(ctx, u"Objectifs",  (x0, y0, rect_width, rect_height), BcoulObj, IcoulObj, fontObj),
                              'obj')
    seq.obj["C"].pt_caract = seq.obj["S"].pt_caract

    
    
    #
    # Codes objectifs
    #
    lstTexteC = []
    for c in seq.obj["C"].competences:
#        print "   ", c
        lstTexteC.append(seq.GetReferentiel().getCompetence(c)[0])
#    print "lstTexteC", lstTexteC
    
    lstTexteS = []
    lstCodes = []
    lstCoul = []
    for c in seq.obj["S"].savoirs:
        typ, cod = c[0], c[1:]
#        print typ, cod
        if typ == "S": # Savoir spécialité STI2D
            lstTexteS.append(seq.GetReferentiel().getSavoir(cod))
            lstCodes.append(cod)
            lstCoul.append((0,0,0))
        elif typ == "M": # Savoir Math
            lstTexteS.append(seq.GetReferentiel().getSavoir(cod, gene = "M"))
            lstCodes.append("Math "+cod)
            lstCoul.append(constantes.COUL_DISCIPLINES['Mat'])
        elif typ == "P": # Savoir Physique
            lstTexteS.append(seq.GetReferentiel().getSavoir(cod, gene = "P"))
            lstCodes.append("Phys "+cod)
            lstCoul.append(constantes.COUL_DISCIPLINES['Phy'])
        else:
            if seq.GetReferentiel().tr_com == []:
                lstTexteS.append(seq.GetReferentiel().getSavoir(cod))
                lstCodes.append(cod)
            else:
                lstTexteS.append(REFERENTIELS[seq.GetReferentiel().tr_com[0]].getSavoir(cod))
                lstCodes.append(seq.GetReferentiel().tr_com[0]+" "+cod)
            lstCoul.append((0.3,0.3,0.3))
            
    h = rect_height+0.0001
    hC = hS = h/2
    if len(lstTexteS) > 0 or len(lstTexteC) > 0:
        hC = h*len(lstTexteC)/(len(lstTexteC) + len(lstTexteS))
        hS = h*len(lstTexteS)/(len(lstTexteC) + len(lstTexteS))
        
        
        ctx.set_source_rgba (COUL_COMPETENCES[0], COUL_COMPETENCES[1], COUL_COMPETENCES[2], COUL_COMPETENCES[3])
        r = liste_code_texte(ctx, seq.obj["C"].competences, lstTexteC, x0, y0, rect_width, hC, 0.008) 
        seq.obj["C"].pts_caract = getPts(r)
        
        ctx.set_source_rgba (0.0, 0.0, 0.0, 1.0)
#        r = liste_code_texte(ctx, [s[1:] for s in seq.obj["S"].savoirs], 
#                             lstTexteS, x0, y0+hC, rect_width, hS, 0.008)
        r = liste_code_texte(ctx, lstCodes, lstTexteS, 
                             x0, y0+hC, rect_width, hS, 0.008, lstCoul = lstCoul)
        seq.obj["S"].pts_caract = getPts(r)
    
    seq.obj["C"].rect = [(x0, y0, rect_width, hC)]
    seq.obj["S"].rect = [(x0, y0+hC, rect_width, hS)]
    
    
    #
    #  CI
    #
#    Draw_CI(ctx, seq.classe.ci_ET)
    Draw_CI(ctx, seq.CI)
    
    
    #
    #  Séances
    #
    for s in seq.seances:
#        Draw_seance(ctx, s, curseur)
        DrawSeanceRacine(ctx, s)
        
    #
    #  Tableau des systèmes
    #    
    
    nomsSystemes = []
    systemes = seq.GetSystemesUtilises()
    for s in systemes:
        nomsSystemes.append(s.nom)
    if nomsSystemes != []:
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.001)
        tableauV(ctx, nomsSystemes, posZSysteme[0], posZSysteme[1], 
                tailleZSysteme[0], posZSeances[1] - posZSysteme[1], 
                0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', coul = (0.8,0.8,0.8))
        
        wc = tailleZSysteme[0]/len(nomsSystemes)
        _x = posZSysteme[0]
        _y = posZSysteme[1]
        for s in systemes:
            s.rect=((_x, _y, wc, posZSeances[1] - posZSysteme[1]),)
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
    if len(seq.GetReferentiel().listeDemarches) > 0:  
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.001)
        l=[]
        for d in seq.GetReferentiel().listeDemarches : 
            l.append(seq.GetReferentiel().demarches[d][0])
        tableauV(ctx, l, posZDemarche[0], posZDemarche[1], 
                tailleZDemarche[0], posZSeances[1] - posZSysteme[1], 
                0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', coul = (0.8,0.75,0.9))
        ctx.move_to(posZDemarche[0], posZDemarche[1] + posZSeances[1] - posZSysteme[1])
        ctx.line_to(posZDemarche[0], posZDemarche[1] + tailleZDemarche[1])
        ctx.move_to(posZDemarche[0]+tailleZDemarche[0]/3, posZDemarche[1] + posZSeances[1] - posZSysteme[1])
        ctx.line_to(posZDemarche[0]+tailleZDemarche[0]/3, posZDemarche[1] + tailleZDemarche[1])
        ctx.move_to(posZDemarche[0]+tailleZDemarche[0]*2/3, posZDemarche[1] + posZSeances[1] - posZSysteme[1])
        ctx.line_to(posZDemarche[0]+tailleZDemarche[0]*2/3, posZDemarche[1] + tailleZDemarche[1])
        ctx.move_to(posZDemarche[0]+tailleZDemarche[0], posZDemarche[1] + posZSeances[1] - posZSysteme[1])
        ctx.line_to(posZDemarche[0]+tailleZDemarche[0], posZDemarche[1] + tailleZDemarche[1])
        ctx.stroke()
    
    #
    #  Tableau des séances (en bas)
    #
#    nomsSeances, intSeances = seq.GetIntituleSeances()
#        print nomsSeances
    if intituleSeances[0] != []:
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.001)
        tableauH_var(ctx, intituleSeances[0], posZIntSeances[0], posZIntSeances[1], 
                0.05, tailleZIntSeances[0]-0.05, intituleSeances[2], fontIntSeances, 
                nCol = 1, va = 'c', ha = 'g', orient = 'h', coul = ICoulSeance, 
                contenu = [intituleSeances[1]])
        
    #
    # Informations
    #
    ctx.select_font_face ("Sans", cairo.FONT_SLANT_ITALIC,
                     cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size (0.006)
    ctx.set_source_rgb(0.6, 0.6, 0.6)
    ctx.move_to (margeX, 1 - margeY + 0.02)
    ctx.show_text ("Fiche créée avec le logiciel pySequence (http://code.google.com/p/pysequence)")

    
    
    

######################################################################################  
def DrawLigneEff(ctx, x, y):
    dashes = [ 0.010,   # ink
               0.002,   # skip
               0.005,   # ink
               0.002,   # skip
               ]
    ctx.set_source_rgba (0.6, 0.8, 0.6)
    ctx.set_line_width (0.001)
    ctx.set_dash(dashes, 0)
    ctx.move_to(x, posZDemarche[1] + tailleZDemarche[1])
    ctx.line_to(x, y)
    ctx.stroke()
    ctx.set_dash([], 0)

######################################################################################  
def DrawPeriodes(ctx, pos = None, periodes = [[u"Année", 5]], tailleTypeEns = 0, origine = False):
    ctx.set_line_width (0.001)
    if origine:
        x = 0
        y = 0
        wt = 0.04*5
        ht = 0.04
    else:
        x = posPos[0]# + ecartX
        y = posPos[1]
        wt = taillePos[0]# - ecartX
        ht = taillePos[1]
    
    pat = cairo.LinearGradient (x, y,  x + wt, y)
    pat.add_color_stop_rgba (1, 0.90, 0.55, 0.65, 1)
    pat.add_color_stop_rgba (0, 0.98, 0.88, 0.98, 1)
    ctx.rectangle (x, y, wt, ht)
    src = ctx.get_source()
    ctx.set_source (pat)
    ctx.fill ()
    ctx.set_source(src)
    
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_NORMAL)
    
    dx = 0.02 * wt
    h = ht/2-2*dx
    
    rect = []
#    print "Périodes", periodes
#    wi = wt/len(periodes) - dx*(len(periodes)-1)
    wi = (wt+dx)/len(periodes) - dx
    pa = 0
    for i, (an, np) in enumerate(periodes):
        annee = an.split("_")
#        print "   ", annee
        ctx.set_font_size(fontPos)
        w0, h0 = ctx.text_extents(annee[0])[2:4]
        xi = x + wi/2 + (dx+wi)*i
#        print "   ", w0, h0, xi
        if len(annee) > 1:
            ctx.set_font_size(fontPos*0.9)
            w1, h1 = ctx.text_extents(annee[1])[2:4]
#            print "   ", w1, h1
            show_text_rect_fix(ctx, annee[0], xi-(w0+w1)/2, y, w0, ht*2/3, fontPos, 1)
            ctx.stroke ()
            show_text_rect_fix(ctx, annee[1], xi-(w0+w1)/2 + w0 + 0.01, y, w1, ht/3, fontPos*0.9, 1, ha = 'g')
            ctx.stroke ()
        else:
            show_text_rect_fix(ctx, annee[0], xi-w0/2, y, w0, ht*2/3, fontPos, 1)
            ctx.stroke ()
        
        w = (wi-dx)/np-dx
        xi = x + (dx+wi)*i + dx
        for p in range(np):
            pa += 1
            ctx.rectangle (xi, y+ht/2+dx, w, h)
            rect.append((xi, y+ht/2+dx, w, h))
            if pos == pa - 1:
                ctx.set_source_rgba (AcoulPos[0], AcoulPos[1], AcoulPos[2], AcoulPos[3])
            else:
                ctx.set_source_rgba (IcoulPos[0], IcoulPos[1], IcoulPos[2], IcoulPos[3])
            ctx.fill_preserve ()
            ctx.set_source_rgba (BcoulPos[0], BcoulPos[1], BcoulPos[2], BcoulPos[3])
            ctx.stroke ()
#            if p == 3:
#                x += dx
            xi += dx + w
            
#    if niv == 'lyc':
#        pm = show_text_rect_fix(ctx, u"1", x, y, wt/2, ht*2/3, fontPos, 1)#, outPosMax = True)
#     
#        ctx.stroke ()
#        show_text_rect_fix(ctx, u"ère", pm+0.002, y, wt/2, ht/3, fontPos*0.9, 1, ha = 'g')
#        ctx.stroke ()
#        
#        pm = show_text_rect_fix(ctx, u"T", x+wt/2, y, wt/2, ht*2/3, fontPos, 1)#, outPosMax = True)
#    
#        ctx.stroke ()
#        show_text_rect_fix(ctx, u"ale", pm+0.002, y, wt/2, ht/3, fontPos*0.9, 1, ha = 'g')
#        ctx.stroke ()
#        
#        dx = wt/4 / (nbr+2) # Ecart entre les cases
#        x += dx
#        h = ht/2-2*dx
#        w = 3*wt/4 / nbr
#        rect = []
#        for p in range(10):
#            ctx.rectangle(x, y+ht/2+dx, w, h)
#            rect.append((x, y+ht/2+dx, w, h))
#            if pos == p:
#                ctx.set_source_rgba (AcoulPos[0], AcoulPos[1], AcoulPos[2], AcoulPos[3])
#            else:
#                ctx.set_source_rgba (IcoulPos[0], IcoulPos[1], IcoulPos[2], IcoulPos[3])
#            ctx.fill_preserve ()
#            ctx.set_source_rgba (BcoulPos[0], BcoulPos[1], BcoulPos[2], BcoulPos[3])
#            ctx.stroke ()
#            if p == nbr/2-1:
#                x += dx
#            x+= dx + w
#    
#    else:
#        dx = wt/4 / (nbr+1) # Ecart entre les cases
#        x += dx
#        h = ht/2-2*dx
#        w = 3*wt/4 / nbr
#        rect = []
#        for p in range(5):
#            pm = show_text_rect_fix(ctx, str(p+1), x, y, w, ht*2/3, fontPos, 1)#, outPosMax = True)
#            ctx.stroke ()
#        
#            ctx.rectangle (x, y+ht/2+dx, w, h)
#            rect.append((x, y+ht/2+dx, w, h))
#            if pos == p:
#                ctx.set_source_rgba (AcoulPos[0], AcoulPos[1], AcoulPos[2], AcoulPos[3])
#            else:
#                ctx.set_source_rgba (IcoulPos[0], IcoulPos[1], IcoulPos[2], IcoulPos[3])
#            ctx.fill_preserve ()
#            ctx.set_source_rgba (BcoulPos[0], BcoulPos[1], BcoulPos[2], BcoulPos[3])
#            ctx.stroke ()
#            
#            x+= dx + w
            
    return rect
    
    
######################################################################################  
def Draw_CI(ctx, CI):
    # Rectangle arrondi
    x0, y0 = posCI
    rect_width, rect_height  = tailleCI
    t = getSingulierPluriel(CI.GetReferentiel().nomCI, len(CI.numCI) > 1)
    
    
    
#    if len(CI.numCI) <= 1:
#        t = u"Centre d'intérêt"
#    else:
#        t = u"Centres d'intérêt"
    CI.pt_caract = (curve_rect_titre(ctx, t,  (x0, y0, rect_width, rect_height), BcoulCI, IcoulCI, fontCI), 
                    'CI')
    
    CI.rect.append((x0, y0, rect_width, rect_height))
    
    
    #
    # code et intitulé des CI
    #
    lstCodes = []
    lstIntit = []
    for i, c in enumerate(CI.numCI):
        lstCodes.append(CI.GetCode(i))
        lstIntit.append(CI.GetIntit(i))
        
    if CI.numCI != []:
        e = 0.008
        r = liste_code_texte(ctx, lstCodes, lstIntit, x0, y0+0.0001, rect_width, rect_height, e, b = 0.2)
        CI.pts_caract = getPts(r)
        



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
        self.y = None
        self.dy = None
        self.seance.rect = []
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
        
        #
        # Le cadre
        #
        epaisseurTrait = 0.002
        self.ctx.set_line_width(epaisseurTrait)
        rectangle_plein(self.ctx, x, y, self.w, self.h, 
                        BCoulSeance[self.seance.typeSeance], ICoulSeance[self.seance.typeSeance], alpha)
        
        
        wc = 0
        #
        # Le code (en haut à gauche)
        #
        if hasattr(self.seance, 'code'):
            self.ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
            self.ctx.set_source_rgba (0,0,0, alpha)
#            hc = max(hHoraire/4, 0.01)
            hc = max(ecartY/4, 0.01)
            f, wc, r = show_text_rect(self.ctx, self.seance.code, (x, y, wEff["P"], hc), ha = 'g', 
                                   wrap = False, fontsizeMinMax = (minFont, -1), b = 0.2)
            wc += ecartX/2
        
        #
        # L'intitulé (si intituleDansDeroul)
        #
        if self.seance.intituleDansDeroul and self.seance.intitule != "" and self.h-hc > 0:#not self.filigrane and 
            self.ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                                  cairo.FONT_WEIGHT_NORMAL)
            self.ctx.set_source_rgba (0,0,0, alpha)
            if self.h < 0.02: # h petit -> on écrit à coté du code !
                rct = (wc, y, self.w - wc-x, self.h)
            else:
                rct = (x, y + hc, self.w, self.h-hc)
            
            show_text_rect(self.ctx, self.seance.intitule, rct, 
                           ha = 'g', b = 0.2, fontsizeMinMax = (minFont, 0.015), 
                           fontsizePref = self.seance.taille.v[0])
        
        #
        # L'intitulé (si intituleDansDeroul)
        #
        if  self.signEgal:# not self.filigrane and
            dx = wEff["P"]/16
#            dy = hHoraire/32
            dy = b/4
            self.ctx.set_source_rgba (0, 0.0, 0.2, alpha)
            self.ctx.set_line_width (0.002)
            self.ctx.move_to(x-dx, y+self.h/2 - dy)
            self.ctx.line_to(x+dx, y+self.h/2 - dy)
            self.ctx.move_to(x-dx, y+self.h/2 + dy)
            self.ctx.line_to(x+dx, y+self.h/2 + dy)
            self.ctx.stroke()
            
        # Sauvegarde de la position du bord droit pour les lignes de croisement
        self.xd = x+self.w
        self.y = y
        
        self.seance.rect.append([x, y, self.w, self.h])
        
        return x + self.w, y + self.h




class Bloc():
    """ Ensemble de cadres.
        contenu = [[], [], ...]
                    lignes
    """
    def __init__(self):
        self.contenu = []
        self.x = None
        self.y = None
        
#    def __repr__(self):
#        print self.contenu
#        return ""
    
    def Draw(self, x, y):
        print self.contenu
        self.x = x
        self.y = y
        for ligne in self.contenu:
            print 
            x = self.x
#            x = posZSeances[0]
            for elem in ligne:
                print "  > ", elem
                if isinstance(elem, Cadre):
                    xf, yf = elem.Draw(x, y)
                    
                elif isinstance(elem, Bloc):
                    xf, yf = elem.Draw(x, y)
                    
                x = xf
                    
            if len(ligne) > 0:
                y = yf

        return x, y
    
    
    def DrawCoisement(self, estRotation):
        for ligne in self.contenu:
            for cadre in ligne:
                if isinstance(cadre, Cadre):
                    if not cadre.filigrane:
#                    if cadre.seance.typeSeance in ["AP", "ED", "P"]:#  and cadre.dy: #and 
                        if len(cadre.seance.GetReferentiel().listeDemarches) > 0:
    #                    if cadre.seance.GetClasse().typeEnseignement != "SSI":
                            DrawCroisementsDemarche(cadre.ctx, cadre.seance, cadre.y + cadre.dy)
                        if not estRotation:
                            DrawCroisementSystemes(cadre.ctx, cadre.seance, cadre.xd, cadre.y + cadre.dy, cadre.seance.GetNbrSystemes())
                else:
                    cadre.DrawCoisement(estRotation)
                          
            if estRotation:
                NS = {}
                cadreOk = False
                for cadre in ligne:
                    if isinstance(cadre, Cadre):
                        ns = cadre.seance.GetNbrSystemes(simple = True)
                        mergeDict(NS, ns)
                        
                        if cadre.dy:
                            cadreOk = cadre
                    else:
                        cadre.DrawCoisement(estRotation)
                if cadreOk:
                    DrawCroisementSystemes(cadreOk.ctx, cadreOk.seance, cadre.xd, cadreOk.y + cadreOk.dy, NS)
            
    
######################################################################################  
def DrawSeanceRacine(ctx, seance):
    global cursY
    if seance.GetDureeGraph() == 0:
        return
        
    #
    # Flèche indiquant la durée
    #
    h = calcH(seance.GetDureeGraph())
    e = largeFlecheDuree
    fleche_verticale(ctx, posZDeroul[0], cursY, 
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
                   (posZDeroul[0]-e/2, cursY, e, h-he), 
                   orient = o, b = 0.2)

    #
    # Fonction pour obtenir les lignes de séances du bloc
    #
    def getLigne(s, hc, filigrane = False):
        l = []
#        if s.typeSeance == "S":
#            for j,ss in enumerate(s.sousSeances):
#                if ss.typeSeance != '':
#                    ss.pts_caract = []
#                    for i in range(int(ss.nombre.v[0])):
#                        l.append(Cadre(ctx, ss, hc, filigrane = filigrane, signEgal = (i>0)))
#                    
#                    # On en profite pour calculer les positions des lignes de croisement
#                    if not filigrane:
#                        l[-1].dy = (j+1) * l[-1].h/(len(s.sousSeances)+1)
#        
#        else:
        if s.typeSeance != '':
            s.pts_caract = []
#            for i in range(int(s.nombre.v[0])):
            l.append(Cadre(ctx, s, hc, filigrane = filigrane))#, signEgal = (i>0)))
            
            # On en profite pour calculer les positions des lignes de croisement
            if not filigrane:
                l[-1].dy = l[-1].h/2
        return l
    

    #
    # Remplissage du tableau de blocs : [[], [], ...]
    #
    def getBloc(seance, h, filigrane = False, decal = 0, rotation = False):
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
            if not filigrane:
                if decal == 0 :
                    l[-1].dy = l[-1].h/2
                else:
                    l[-1].dy = decal * l[-1].h
            else:
                l[-1].dy = decal * l[-1].h
#            else:
#                bloc.contenu.append([Cadre(ctx, seance, h, filigrane = filigrane)])
#                if not filigrane:
#                    bloc.contenu[0][-1].dy = decal * bloc.contenu[0][-1].h
#            # On en profite pour calculer les positions des lignes de croisement
#            if not filigrane:
#                bloc.contenu.dy = bloc.contenu.h/2
                
            return bloc
            
            
        # Séance "complexe"    
        else:
            # Rotation : plusieurs lignes
            if seance.typeSeance == "R":           
                bloc = Bloc()
                l0 = seance.GetListSousSeancesRot() # Liste des sous séances de la première colonne (têtes de ligne - foncé)
                print "l0 =", l0
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
                    print "  l =", l
                    for t in range(len(l)-1): # Colonnes
                        l = permut(l)
                        print "   ", l
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
                    bloc.contenu[0].append(getBloc(ss, h*ss.GetDuree()/seance.GetDuree(), decal = 1.0*(j+1)/(len(seance.seances)+1)))
                
                return bloc
            
            return Bloc()
        return Bloc()

    bloc = getBloc(seance, h)
    
#    print "bloc :", bloc
#    print "  ", cursY,
#    y = cursY
    x, cursY = bloc.Draw(posZSeances[0], cursY)
    bloc.DrawCoisement(seance.typeSeance == "R") 
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
#            bloc.DrawCoisement(seance.typeSeance == "R")
#        print "..", yf, 
#        y = yf
#    print 
    cursY += ecartSeanceY





#######################################################################################  
#def DrawSeanceRacine(ctx, seance):
#    global cursY
#    if seance.GetDureeGraph() == 0:
#        return
#        
#    #
#    # Flèche indiquant la durée
#    #
#    h = calcH(seance.GetDureeGraph())
#    e = largeFlecheDuree
#    fleche_verticale(ctx, posZDeroul[0], cursY, 
#                     h, e, (0.9,0.8,0.8,0.5))
#    ctx.set_source_rgb(0.5,0.8,0.8)
#    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
#                              cairo.FONT_WEIGHT_BOLD)
#    he = min(e/2, h/3)
#    
#    if h-he < e:
#        o = 'h'
#    else:
#        o = 'v'
#    show_text_rect(ctx, getHoraireTxt(seance.GetDuree()), 
#                   (posZDeroul[0]-e/2, cursY, e, h-he), 
#                   orient = o, b = 0.2)
#
#    #
#    # Fonction pour obtenir les lignes de séances du bloc
#    #
#    def getLigne(s, hc, filigrane = False):
#        l = []
#        if s.typeSeance == "S":
#            for j,ss in enumerate(s.sousSeances):
#                if ss.typeSeance != '':
#                    ss.pts_caract = []
#                    for i in range(int(ss.nombre.v[0])):
#                        l.append(Cadre(ctx, ss, hc, filigrane = filigrane, signEgal = (i>0)))
#                    
#                    # On en profite pour calculer les positions des lignes de croisement
#                    if not filigrane:
#                        l[-1].dy = (j+1) * l[-1].h/(len(s.sousSeances)+1)
#        
#        else:
#            if s.typeSeance != '':
#                s.pts_caract = []
#                for i in range(int(s.nombre.v[0])):
#                    l.append(Cadre(ctx, s, hc, filigrane = filigrane, signEgal = (i>0)))
#                
#                # On en profite pour calculer les positions des lignes de croisement
#                if not filigrane:
#                    l[-1].dy = l[-1].h/2
#        return l
#    
#
#    #
#    # Remplissage du(des) bloc(s)
#    #
#    def getBlocs(seance):
#        # Séance "simple" --> un seul bloc d'une ligne de un ou plusieurs cadres 
#        if not seance.typeSeance in ["R", "S", ""]:
#            bloc = Bloc()
#            seance.pts_caract = []
#            if seance.typeSeance in ["AP", "ED", "P"]:
#                l = []
#                for i in range(int(seance.nombre.v[0])):
#                    l.append(Cadre(ctx, seance, h, signEgal = (i>0)))
#                bloc.contenu.append(l)
#                l[-1].dy = l[-1].h/2
#            else:
#                bloc.contenu.append([Cadre(ctx, seance, h)])
#                
#            return [bloc]
#            
#            
#        # Séance "complexe"    
#        else:
#            bloc = Bloc()
#            # Rotation : plusieurs lignes
#            if seance.typeSeance == "R":
#                hl = h / seance.nbrRotations.v[0]
#                for i in range(seance.nbrRotations.v[0]):
#                    s = seance.sousSeances[i]
#                    bloc.contenu.append(getLigne(s, hl))
#                    
#                #
#                # Aperçu en filigrane de la rotation
#                #
#                if seance.IsEffectifOk() <= 3:
#                    l = seance.sousSeances
#                    for t in range(len(seance.sousSeances)-1):
#                        l = permut(l)
#                        for i, s in enumerate(l[:seance.nbrRotations.v[0]]):
#                            bloc.contenu[i].extend(getLigne(s, hl, filigrane = True))
#                
#            elif seance.typeSeance == "S":
#                n = len(seance.sousSeances)
#                bloc.contenu.append(getLigne(seance, h))
#            
#            return [bloc]
#
#
#    blocs = getBlocs(seance)
#    for bloc in blocs:
#        # Tracé des blocs
#        cursY = bloc.Draw(posZSeances[0], cursY)
#    
#        # Tracé des croisements "Démarche" et "Systèmes"
#        bloc.DrawCoisement(seance.typeSeance == "R") 


#######################################################################################  
#def Draw_seance2(ctx, seance, curseur, typParent = "", rotation = False, ):
#    if not seance.EstSousSeance():
#        h = hHoraire * seance.GetDuree()
#        fleche_verticale(ctx, posZDeroul[0], curseur[1], 
#                         h, 0.02, (0.9,0.8,0.8,0.5))
#        ctx.set_source_rgb(0.5,0.8,0.8)
#        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
#                                  cairo.FONT_WEIGHT_BOLD)
#        show_text_rect(ctx, getHoraireTxt(seance.GetDuree()), posZDeroul[0]-0.01, curseur[1], 
#                       0.02, h, orient = 'v')
#        
#        
#    if not seance.typeSeance in ["R", "S", ""]:
##            print "Draw", self
#        x, y = curseur
#        w = wEff[seance.effectif]
#        h = hHoraire * seance.GetDuree()
#        if rotation:
#            seance.rect.append((x, y, w, h))
#        else:
#            seance.rect=[(x, y, w, h),] # Rectangles pour clic
#        
#        if rotation:
#            alpha = 0.2
#        else:
#            alpha = 1
#        
#        for i in range(int(seance.nombre.v[0])):
#            ctx.set_line_width(0.002)
#            rectangle_plein(ctx, x+w*i, y, w, h, 
#                            BCoulSeance[seance.typeSeance], ICoulSeance[seance.typeSeance], alpha)
#            
#            if not rotation and hasattr(seance, 'code'):
#                ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
#                                      cairo.FONT_WEIGHT_BOLD)
#                ctx.set_source_rgb (0,0,0)
#                show_text_rect(ctx, seance.code, x+w*i, y, wEff["P"], hHoraire/4, ha = 'g', wrap = False)
#            
#            if not rotation and seance.intituleDansDeroul and seance.intitule != "":
#                ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
#                                      cairo.FONT_WEIGHT_NORMAL)
#                ctx.set_source_rgb (0,0,0)
#                show_text_rect(ctx, seance.intitule, x+w*i, y + hHoraire/4, 
#                               w, h-hHoraire/4, ha = 'g')
#        
#        
#        # Les croisements "Démarche" et "Systèmes"
#        if not rotation and seance.typeSeance in ["AP", "ED", "P"]:
#            if seance.EstSousSeance() and seance.parent.typeSeance == "S":
#                ns = len(seance.parent.sousSeances)
#                ys = y+(seance.ordre+1) * h/(ns+1)
##                    print ns, ys, self.ordre
#            else:
#                ys = y+h/2           
#                
#            DrawCroisementsDemarche(ctx, seance, x+w*seance.nombre.v[0], ys)
#            DrawCroisementSystemes(ctx, seance, ys)      
#                
#            
#        if typParent == "R":
#            curseur[1] += h
#        elif typParent == "S":
#            curseur[0] += w
#        else:
#            curseur[1] += h + ecartSeanceY
#    else:
#        if seance.typeSeance in ["R", "S"]:
#            for s in seance.sousSeances:
#                Draw_seance(ctx, s, curseur, typParent = seance.typeSeance, rotation = rotation)
##                    if self.typeSeance == "S":
#            
#            #
#            # Aperçu en filigrane de la rotation
#            #
#            if seance.typeSeance == "R" and seance.IsEffectifOk() < 2:
#                l = seance.sousSeances
#                eff = seance.GetEffectif()
#                if eff == 16:
#                    codeEff = "C"
#                elif eff == 8:
#                    codeEff = "G"
#                elif eff == 4:
#                    codeEff = "D"
#                elif eff == 2:
#                    codeEff = "E"
#                elif eff == 1:
#                    codeEff = "P"
#                
#                for t in range(len(seance.sousSeances)-1):
#                    curs = [curseur[0]+wEff[codeEff]*(t+1), curseur[1]-hHoraire * seance.GetDuree()]
#                    l = permut(l)
#                    for i, s in enumerate(l):
##                        print "filigrane", s, curs
#                        Draw_seance(ctx, s, curs, typParent = "R", rotation = True)
#                        if s.typeSeance == "S":
#                            curs[0]  += wEff[codeEff]*(i+1)
##                    curs[0] += wEff[codeEff]
##                    curs[1] = curseur[1]-hHoraire * seance.GetDuree()
#            
#            curseur[0] = posZSeances[0]
#            if typParent == "":
#                curseur[1] += ecartSeanceY
#            if seance.typeSeance == "S":
#                curseur[1] += hHoraire * seance.GetDuree()
#
##        elif seance.typeSeance in ["AP", "ED"] and seance.Nombre.v[0]>0:
##            curs = [curseur[0]+wEff[codeEff]*(t+1), curseur[1]-hHoraire * seance.GetDuree()]
##            for i in range(seance.Nombre.v[0] -1):
##                Draw_seance(ctx, s, curseur, typParent = seance.typeSeance, rotation = rotation)
#        
        
######################################################################################  
def DrawCroisementSystemes(ctx, seance, x, y, ns):
#        if self.typeSeance in ["AP", "ED", "P"]:
#            and not (self.EstSousSeance() and self.parent.typeSeance == "S"):
    #
    # Les lignes horizontales
    #
    if seance.typeSeance in ["AP", "ED", "P"]:
        DrawLigne(ctx, x, y)
        
        
    r = wColSysteme/3
#    ns = seance.GetNbrSystemes(posDansRot = posDansRot)
    for s, n in ns.items():
        if n > 0:
            x = xSystemes[s]
            ctx.arc(x, y, r, 0, 2*pi)
            ctx.set_source_rgba (1,0.2,0.2,1.0)
            ctx.fill_preserve ()
            ctx.set_source_rgba (0,0,0,1)
            ctx.stroke ()
            ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
            show_text_rect(ctx, str(n), (x-r, y-r, 2*r, 2*r))
            seance.rect.append((x-r, y-r, 2*r, 2*r)) 
            
######################################################################################  
def DrawLigne(ctx, x, y):
    dashes = [ 0.010,   # ink
               0.002,   # skip
               0.005,   # ink
               0.002,   # skip
               ]
    ctx.set_source_rgba (0, 0.0, 0.2, 0.6)
    ctx.set_line_width (0.001)
    ctx.set_dash(dashes, 0)
    ctx.move_to(posZOrganis[0]+tailleZOrganis[0], y)
    ctx.line_to(x, y)
    ctx.stroke()
    ctx.set_dash([], 0)
          

#####################################################################################  
def DrawCroisementsDemarche(ctx, seance, y):
        
    #
    # Croisements Séance/Démarche
    #
    _x = xDemarche[seance.demarche]
#        if self.typeSeance in ["AP", "ED", "P"]:
    r = 0.008
    boule(ctx, _x, y, r)
    seance.rect.append((_x -r , y - r, 2*r, 2*r))




