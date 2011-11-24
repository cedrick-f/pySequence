#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               draw_cairo                                ##
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


import textwrap
from math import sqrt, pi, cos, sin
import cairo

import ConfigParser

from constantes import Effectifs, listeDemarches, Demarches, getSavoir, getCompetence

#
# Données pour le tracé
#
# Marges
margeX = 0.04
margeY = 0.04

# Ecarts
ecartX = 0.03
ecartY = 0.03

# CI
tailleCI = (0.16, 0.07)
#posCI = (posPre[0] + taillePre[0]+ecartX, 0.1)
posCI = (margeX, margeY)
IcoulCI = (0.9,0.8,0.8)
BcoulCI = (0.3,0.2,0.25)

# Rectangle des prerequis
taillePre = (0.28, 0.16 - tailleCI[1] - ecartY/2)
posPre = (margeX, posCI[1] + tailleCI[1] + ecartY/2)
IcoulPre = (0.8,0.8,0.9)
BcoulPre = (0.2,0.25,0.3)

# Rectangle des objectifs
posObj = (posPre[0] + taillePre[0] + ecartX, margeY)
tailleObj = (0.72414-posObj[0]-margeX, 0.16)
IcoulObj = (0.8,0.9,0.8)
BcoulObj = (0.25,0.3,0.2)

# Zone de commentaire
fontIntComm = 0.01
posComm = [0.05, None]
tailleComm = [0.72414-0.1, None]
intComm = []

# Zone d'organisation de la séquence (grand cadre)
posZOrganis = (0.05, 0.26)
tailleZOrganis = [0.72414-0.1, None]
bordureZOrganis = 0.01

# Rectangle de l'intitulé
tailleIntitule = [0.4, 0.04]
posIntitule = [(0.72414-tailleIntitule[0])/2, posZOrganis[1]-tailleIntitule[1]]
IcoulIntitule = (0.2,0.8,0.2)
BcoulIntitule = (0.2,0.8,0.2)

# Zone de déroulement de la séquence
posZDeroul = (0.06, 0.3)
tailleZDeroul = [None, None]

# Zone du tableau des Systèmes
posZSysteme = [None, 0.265]
tailleZSysteme = [None, None]
wColSysteme = 0.025
xSystemes = {}

# Zone du tableau des démarches
posZDemarche = [None, 0.265]
tailleZDemarche = [0.07, None]
xDemarche = {"I" : None,
             "R" : None,
             "P" : None}

# Zone des intitulés des séances
fontIntSeances = 0.01
posZIntSeances = [0.06, None]
tailleZIntSeances = [0.72414-0.12, None]
hIntSeance = 0.02
intituleSeances = []

# Zone des séances
posZSeances = (0.08, 0.35)
tailleZSeances = [None, None]
wEff = {"C" : None,
             "G" : None,
             "D" : None,
             "E" : None,
             "P" : None,
             }
hHoraire = None
ecartSeanceY = None
BCoulSeance = {"ED" : (0.3,0.5,0.5), 
               "AP" : (0.5,0.3,0.5), 
               "P"  : (0.5,0.5,0.3), 
               "C"  : (0.3,0.3,0.7), 
               "SA" : (0.3,0.7,0.3), 
               "SS" : (0.4,0.5,0.4), 
               "E"  : (0.7,0.3,0.3), 
               "R"  : (0.45,0.35,0.45), 
               "S"  : (0.45,0.45,0.35)}
ICoulSeance = {"ED" : (0.6, 0.8, 0.8), 
               "AP" : (0.8, 0.6, 0.8), 
               "P"  : (0.8, 0.8, 0.6), 
               "C"  : (0.6, 0.6, 1.0), 
               "SA" : (0.6, 1.0, 0.6), 
               "SS" : (0.7, 0.8, 0.7), 
               "E"  : (1.0, 0.6, 0.6), 
               "R"  : (0.75, 0.65, 0.75), 
               "S"  : (0.75, 0.75, 0.65)}

def str2coord(str):
    l = str.split(',')
    return [eval(l[0]), eval(l[1])]

def coord2str(xy):
    return str(xy[0])+","+str(xy[1])

def str2coul(str):
    l = str.split(',')
    return eval(l[0]), eval(l[1]), eval(l[2]), eval(l[3])

def coul2str(rgba):
    if len(rgba) == 3:
        a = 1
    else:
        a = rgba[3]
    return str(rgba[0])+","+str(rgba[1])+","+str(rgba[2])+","+str(a)



def enregistrerConfigFiche(nomFichier):
    config = ConfigParser.ConfigParser()

    section = "General"
    config.add_section(section)
    config.set(section, "margeX", str(margeX))
    config.set(section, "margeY", str(margeY))
    config.set(section, "ecartX", str(ecartX))
    config.set(section, "ecartY", str(ecartY))
    
    section = "Intitule de la sequence"
    config.add_section(section)
    config.set(section, "pos", coord2str(posIntitule))
    config.set(section, "dim", coord2str(tailleIntitule))
    config.set(section, "coulInt", coul2str(IcoulIntitule))
    config.set(section, "coulBord", coul2str(BcoulIntitule))
    
    section = "Centre d'interet"
    config.add_section(section)
    config.set(section, "pos", coord2str(posCI))
    config.set(section, "dim", coord2str(tailleCI))
    config.set(section, "coulInt", coul2str(IcoulCI))
    config.set(section, "coulBord", coul2str(BcoulCI))
    
    section = "Objectifs"
    config.add_section(section)
    config.set(section, "pos", coord2str(posObj))
    config.set(section, "dim", coord2str(tailleObj))
    config.set(section, "coulInt", coul2str(IcoulObj))
    config.set(section, "coulBord", coul2str(BcoulObj))

    section = "Prerequis"
    config.add_section(section)
    config.set(section, "pos", coord2str(posPre))
    config.set(section, "dim", coord2str(taillePre))
    config.set(section, "coulInt", coul2str(IcoulPre))
    config.set(section, "coulBord", coul2str(BcoulPre))

    section = "Zone d'organisation"
    config.add_section(section)
    config.set(section, "pos", coord2str(posZOrganis))
    config.set(section, "dim", coord2str(tailleZOrganis))

    section = "Zone de deroulement"
    config.add_section(section)
    config.set(section, "pos", coord2str(posZDeroul))

    section = "Tableau systemes"
    config.add_section(section)
    config.set(section, "posY", str(posZSysteme[1]))
    config.set(section, "col", str(wColSysteme))

    section = "Tableau demarche"
    config.add_section(section)
    config.set(section, "posY", str(posZDemarche[1]))
    config.set(section, "dimX", str(tailleZDemarche[0]))
    
    section = "Intitule des seances"
    config.add_section(section)
    config.set(section, "posX", str(posZIntSeances[0]))
    config.set(section, "dimX", str(tailleZIntSeances[0]))
    config.set(section, "haut", str(hIntSeance))

    section = "Seances"
    config.add_section(section)
    config.set(section, "pos", coord2str(posZSeances))
    for k, v in BCoulSeance.items():
        config.set(section, "Bcoul"+k, coul2str(v))
    for k, v in ICoulSeance.items():
        config.set(section, "Icoul"+k, coul2str(v))
        
    config.write(open(nomFichier,'w'))
    
    
    
    
    
    
def ouvrirConfigFiche(nomFichier):
    print "ouvrirConfigFiche"
    global posIntitule, tailleIntitule, IcoulIntitule, BcoulIntitule, \
           posCI, tailleCI, IcoulCI, BcoulCI, \
           posObj, tailleObj, IcoulObj, BcoulObj, \
           posZOrganis, tailleZOrganis, \
           posZDeroul, wColSysteme, hIntSeance, posZSeances, \
           margeX, margeY, ecartX, ecartY
           
           
    config = ConfigParser.ConfigParser()
    config.read(nomFichier)
    
    section = "General"
    margeX = eval(config.get(section,"margeX"))
    margeY = eval(config.get(section,"margeY"))
    ecartX = eval(config.get(section,"ecartX"))
    ecartY = eval(config.get(section,"ecartY"))
    
    
    section = "Intitule de la sequence"
    posIntitule = str2coord(config.get(section,"pos"))
    tailleIntitule = str2coord(config.get(section,"dim"))
    IcoulIntitule = str2coul(config.get(section,"coulInt"))
    BcoulIntitule = str2coul(config.get(section,"coulBord"))
    
    section = "Centre d'interet"
    posCI = str2coord(config.get(section,"pos"))
    tailleCI = str2coord(config.get(section,"dim"))
    IcoulCI = str2coul(config.get(section,"coulInt"))
    BcoulCI = str2coul(config.get(section,"coulBord"))
    
    section = "Objectifs"
    posObj = str2coord(config.get(section,"pos"))
    tailleObj = str2coord(config.get(section,"dim"))
    IcoulObj = str2coul(config.get(section,"coulInt"))
    BcoulObj = str2coul(config.get(section,"coulBord"))

    section = "Prerequis"
    posPre = str2coord(config.get(section,"pos"))
    taillePre = str2coord(config.get(section,"dim"))
    IcoulPre = str2coul(config.get(section,"coulInt"))
    BcoulPre = str2coul(config.get(section,"coulBord"))
    
    section = "Zone d'organisation"
    posZOrganis = str2coord(config.get(section,"pos"))
    tailleZOrganis = str2coord(config.get(section,"dim"))
    
    section = "Zone de deroulement"
    posZDeroul = str2coord(config.get(section,"pos"))

    section = "Tableau systemes"
    posZSysteme[1] = config.getfloat(section,"posY")
    wColSysteme = config.getfloat(section,"col")

    section = "Tableau demarche"
    posZDemarche[1] = config.getfloat(section,"posY")
    tailleZDemarche[0] = config.getfloat(section,"dimX")
    
    section = "Intitule des seances"
    posZIntSeances[0] = config.getfloat(section,"posX")
    tailleZIntSeances[0] = config.getfloat(section,"dimX")
    hIntSeance = config.getfloat(section,"haut")
    
    section = "Seances"
    posZSeances = str2coord(config.get(section,"pos"))
    for k in BCoulSeance.keys():
        BCoulSeance[k] = str2coul(config.get(section, "Bcoul"+k))
    for k in ICoulSeance.keys():
        ICoulSeance[k] = str2coul(config.get(section, "Icoul"+k))
    
    

######################################################################################  
def DefinirZones(seq, ctx):
    """ Calcule les positions et dimensions des différentes zones de tracé
        en fonction du nombre d'éléments (séances, systèmes)
    """
    global wEff, hHoraire, ecartSeanceY, intituleSeances, fontIntSeances, fontIntComm, intComm
    
    # Zone de commentaire
    if seq.commentaire == "":
        tailleComm[1] = 0
    else:
        
        tailleComm[1], intComm = calc_h_texte(ctx, u"Commentaires : " + seq.commentaire, tailleComm[0], fontIntComm)

    posComm[1] = 1-tailleComm[1]-margeY
    
    # Zone d'organisation de la séquence (grand cadre)
    tailleZOrganis[1] = posComm[1]-posZOrganis[1]-bordureZOrganis

    # Rectangle de l'intitulé
    posIntitule[1] = posZOrganis[1]-tailleIntitule[1]

    # Zone des intitulés des séances
    intituleSeances = []
    tailleZIntSeances[1] = 0
    for intS in seq.GetIntituleSeances()[1]:
        h, t = calc_h_texte(ctx, intS, tailleZIntSeances[0], fontIntSeances)
        intituleSeances.append([intS[0],h,t])
        tailleZIntSeances[1] += h
#    tailleZIntSeances[1] = len(seq.GetIntituleSeances()[0])* hIntSeance
    posZIntSeances[1] = posZOrganis[1] + tailleZOrganis[1] - tailleZIntSeances[1]
    
    # Zone du tableau des Systèmes
    tailleZSysteme[0] = wColSysteme * len(seq.systemes)
    tailleZSysteme[1] = tailleZOrganis[1] - ecartY - tailleZIntSeances[1]
    posZSysteme[0] = posZOrganis[0] + tailleZOrganis[0] - tailleZSysteme[0]
    for i, s in enumerate(seq.systemes):
        xSystemes[s.nom] = posZSysteme[0] + (i+0.5) * wColSysteme
    
    
    # Zone du tableau des démarches
    posZDemarche[0] = posZSysteme[0] - tailleZDemarche[0] - ecartX
    tailleZDemarche[1] = tailleZSysteme[1]
    xDemarche["I"] = posZDemarche[0] + tailleZDemarche[0]/6
    xDemarche["R"] = posZDemarche[0] + tailleZDemarche[0]*3/6
    xDemarche["P"] = posZDemarche[0] + tailleZDemarche[0]*5/6
                 
    # Zone de déroulement de la séquence
    tailleZDeroul[0] = posZDemarche[0] - posZDeroul[0] - ecartX
    tailleZDeroul[1] = tailleZSysteme[1]
    
    
    # Zone des séances
    tailleZSeances[0] = tailleZDeroul[0] - 0.05 # écart pour les durées
    tailleZSeances[1] = tailleZSysteme[1] - posZSeances[1] + posZDeroul[1] - 0.05
    wEff = {"C" : tailleZSeances[0],
             "G" : tailleZSeances[0]*6/7,
             "D" : tailleZSeances[0]*3/7,
             "E" : tailleZSeances[0]*Effectifs["E"][1]/Effectifs["G"][1]*6/7,
             "P" : tailleZSeances[0]*Effectifs["P"][1]/Effectifs["G"][1]*6/7,
             }
    ecartSeanceY = 0.02
    hHoraire = (tailleZSeances[1] - (len(seq.seance)-1)*ecartSeanceY) / seq.GetHoraireTotal()


######################################################################################
curseur = None 
def InitCurseur():
    global cursY
#    curseur = [posZSeances[0], posZSeances[1]]
    cursY = posZSeances[1]
    
######################################################################################  
def Draw(ctx, seq):
    """ Dessine une fiche de séquence de la séquence <seq>
        dans un contexte cairo <ctx>
    """
#        print "Draw séquence"
    InitCurseur()
    
    DefinirZones(seq, ctx)
    
    #
    # Options générales
    #
    options = ctx.get_font_options()
    options.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    options.set_hint_style(cairo.HINT_STYLE_NONE)
    options.set_hint_metrics(cairo.HINT_METRICS_OFF)
    ctx.set_font_options(options)
    
    #
    # Flèche
    #
    rayon = 0.30
    alpha0 = 55
    alpha1 = 155
    y = posObj[1]+tailleObj[1] - rayon*sin(alpha0*pi/180)
    fleche_ronde(ctx, 0.72414/2, y, rayon, alpha0, alpha1, 0.035, 0.06, (0.8, 0.9, 0.8, 1))
    
    #
    # Type d'enseignement
    #
    ctx.set_font_size(0.05)
#    ctx.set_source_rgb(0.1,0.1,0.1)
    ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_BOLD)
#    show_text_rect(ctx, seq.classe.typeEnseignement, posCI[0], posCI[1] - 0.08, tailleCI[0], tailleCI[1], ha = 'c', wrap = False, max_font = 0.04)
    
    xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(seq.classe.typeEnseignement)
    ctx.move_to (posCI[0] + tailleCI[0] + ecartX/2 , posCI[1] + height)
    ctx.text_path (seq.classe.typeEnseignement)
    ctx.set_source_rgb (0.5, 0.5, 1)
    ctx.fill_preserve ()
    ctx.set_source_rgb (0, 0, 0)
    ctx.set_line_width (0.002)
    ctx.stroke ()
    
    
    
    
    
    #
    # Commentaires
    #
    print posComm[1], 
    if tailleComm[1] > 0:
        ctx.set_source_rgb(0.1,0.1,0.1)
        ctx.select_font_face ("Sans", cairo.FONT_SLANT_ITALIC,
                                          cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(fontIntComm)
        _x, _y = posComm
        fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
        #
        # On dessine toutes les lignes de texte
        #
        for i, t in enumerate(intComm):
    #        print "  ",t
#            xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
            yt = _y + (fascent+fdescent)*i  + fheight #- fdescent
    #        print "  ",xt, yt
            ctx.move_to(_x, yt)
            ctx.show_text(t)
                
                
#        show_text_rect(ctx, u"Commentaires : " + seq.commentaire, posComm[0], posComm[1], tailleComm[0], tailleComm[1], ha = 'g', max_font = 0.02)
    
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
        show_text_rect(ctx, Effectifs[e][2], x, y, w, h)
        ctx.stroke()
        DrawLigneEff(ctx, x+w, y+h)
        
    
#        #
#        #  Bordure
#        #
#        ctx.set_line_width(0.005)
#        ctx.set_source_rgb(0, 0, 0)
#        ctx.rectangle(0, 0, 0.724, 1)
#        ctx.stroke()
    
    #
    #  Intitulé de la séquence
    #
    x, y = posIntitule
    w, h = tailleIntitule
    ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_BOLD)
    ctx.set_source_rgb(0, 0, 0)
    if len(seq.intitule) > 0:
        show_text_rect(ctx, seq.intitule, x, y, w, h)
    ctx.set_line_width(0.005)
    ctx.set_source_rgb(BcoulIntitule[0], BcoulIntitule[1], BcoulIntitule[2])
    ctx.rectangle(x, y, w, h)
    ctx.stroke()

    #
    #  Bordure Organisation
    #
    ctx.set_line_width(0.005)
    ctx.set_source_rgb(BcoulIntitule[0], BcoulIntitule[1], BcoulIntitule[2])
    ctx.rectangle(posZOrganis[0]-bordureZOrganis, posZOrganis[1], tailleZOrganis[0]+bordureZOrganis*2, tailleZOrganis[1]+bordureZOrganis)
    ctx.stroke()


    #
    #  Prerequis
    #
    
    # Rectangle arrondi
    x0, y0 = posPre
    rect_width, rect_height  = taillePre
    curve_rect(ctx, x0, y0, rect_width, rect_height, 0.05)
    ctx.set_source_rgb (IcoulPre[0], IcoulPre[1], IcoulPre[2])
    ctx.fill_preserve ()
    ctx.set_source_rgba (BcoulPre[0], BcoulPre[1], BcoulPre[2])
    ctx.stroke ()
    
    # Titre
    ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(0.016)
    xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(u"Prérequis")
    xc=x0+rect_width/2-width/2
    yc=y0+height+0.008
    ctx.move_to(xc, yc)
    ctx.set_source_rgb(0, 0, 0)
    ctx.show_text(u"Prérequis")
    
    #
    # Codes prerequis
    #
    lstTexte = []
    for c in seq.prerequis.savoirs:
        lstTexte.append(getSavoir(seq, c))
        
    lstTexteS = []   
    for c in seq.prerequisSeance:
        lstTexteS.append(c.GetNomFichier())    
        
    hl = rect_height-height-0.015   
    if len(lstTexte) + len(lstTexteS) > 0:
        e = 0.01
        hC = hl*len(lstTexte)/(len(lstTexte) + len(lstTexteS))
        hS = hl*len(lstTexteS)/(len(lstTexte) + len(lstTexteS))
        liste_code_texte(ctx, seq.prerequis.savoirs, lstTexte, x0, yc, rect_width, hC, e)
        ctx.set_source_rgba (0.0, 0.0, 0.5, 1.0)
        lstRect = liste_code_texte(ctx, ["Seq."]*len(lstTexteS), lstTexteS, x0, yc+hC, rect_width, hS, 0.01)
        for i, c in enumerate(seq.prerequisSeance): 
            c.rect = [lstRect[i]]
    else:
        show_text_rect(ctx, u"Aucun", x0, yc, rect_width, hl, max_font = 0.015)
    
    
        
#    if len(seq.prerequis.savoirs) > 0:
#        no = len(seq.prerequis.savoirs)
#        e = 0.01
#        for i, t in enumerate(seq.prerequis.savoirs):
#            hl = (rect_height-height-0.015)/no
#            ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                  cairo.FONT_WEIGHT_BOLD)
#            show_text_rect(ctx, t.split()[0], x0+e, yc+i*hl, 
#                           rect_width/6-e, hl, b = 0.2, ha = 'g', max_font = 0.012, wrap = False)
#            ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                  cairo.FONT_WEIGHT_NORMAL)
#            show_text_rect(ctx, getSavoir(t.split()[0]), x0+rect_width/6, yc+i*hl, 
#                           rect_width*5/6-e, hl, b = 0.2, ha = 'g')
#
#            ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                  cairo.FONT_WEIGHT_BOLD)
    
    #
    #  Objectifs
    #
    
    # Rectangle arrondi
    x0, y0 = posObj
    rect_width, rect_height  = tailleObj
    curve_rect(ctx, x0, y0, rect_width, rect_height, 0.05)
    ctx.set_source_rgb (IcoulObj[0], IcoulObj[1], IcoulObj[2])
    ctx.fill_preserve ()
    ctx.set_source_rgba (BcoulObj[0], BcoulObj[1], BcoulObj[2])
    ctx.stroke ()
    
    # Titre
    ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(0.016)
    xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(u"Objectifs")
    xc=x0+rect_width/2-width/2
    yc=y0+height+0.008
    ctx.move_to(xc, yc)
    ctx.set_source_rgb(0, 0, 0)
    ctx.show_text(u"Objectifs")
    
    #
    # Codes objectifs
    #
    lstTexteC = []
    for c in seq.obj["C"].competences:
        lstTexteC.append(getCompetence(seq, c))
    lstTexteS = []   
    for c in seq.obj["S"].savoirs:
        lstTexteS.append(getSavoir(seq, c))
    h = rect_height-height-0.015  
    
    if len(lstTexteS) > 0 or len(lstTexteC) > 0:
        hC = h*len(lstTexteC)/(len(lstTexteC) + len(lstTexteS))
        hS = h*len(lstTexteS)/(len(lstTexteC) + len(lstTexteS))
        liste_code_texte(ctx, seq.obj["C"].competences, lstTexteC, x0, yc, rect_width, hC, 0.01) 
        ctx.set_source_rgba (0.0, 0.0, 0.5, 1.0)
        liste_code_texte(ctx, seq.obj["S"].savoirs, lstTexteS, x0, yc+hC, rect_width, hS, 0.01)
    
    
    
#    lstCS = seq.obj["C"].competences + seq.obj["S"].savoirs
#    print "Draw objectifs", lstCS
#    if len(lstCS) > 0:
#        no = len(lstCS)
#        e = 0.01
#        txtObj = ''
#        hl = (rect_height-height-0.015)/no
#        for i, t in enumerate(lstCS):
#            if hasattr(t, 'code'):
#                txtObj += " " + t.code
#                ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                      cairo.FONT_WEIGHT_BOLD)
#                show_text_rect(ctx, t.code, x0+e, yc+i*hl, 
#                               rect_width/5-e, hl, max_font = 0.012, ha = 'g', wrap = False)
#                ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                      cairo.FONT_WEIGHT_NORMAL)
#                show_text_rect(ctx, Competences[t.code], x0+rect_width/5, yc+i*hl, 
#                               rect_width*4/5-e, hl, ha = 'g')
#        
##            x, y = posObj
##            w, h = tailleObj
#                ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                      cairo.FONT_WEIGHT_BOLD)
#        

    #
    #  CI
    #
    Draw_CI(ctx, seq.CI)
    
    
    #
    #  Séances
    #
    for s in seq.seance:
#        Draw_seance(ctx, s, curseur)
        DrawSeanceRacine(ctx, s)
        
    #
    #  Tableau des systèmes
    #    
    nomsSystemes = []
    for s in seq.systemes:
        nomsSystemes.append(s.nom)
    if nomsSystemes != []:
        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.001)
        tableauV(ctx, nomsSystemes, posZSysteme[0], posZSysteme[1], 
                tailleZSysteme[0], posZSeances[1] - posZSysteme[1], 
                0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', coul = (0.8,0.8,0.8))
        
        wc = tailleZSysteme[0]/len(nomsSystemes)
        _x = posZSysteme[0]
        _y = posZSysteme[1]
        for s in seq.systemes:
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
    ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(0.001)
    l=[]
    for d in listeDemarches : 
        l.append(Demarches[d])
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
    nomsSeances, intSeances = seq.GetIntituleSeances()
#        print nomsSeances
    if nomsSeances != []:
        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.001)
        tableauH_var(ctx, nomsSeances, posZIntSeances[0], posZIntSeances[1], 
                0.05, tailleZIntSeances[0]-0.05, zip(*intituleSeances)[1], fontIntSeances, 
                nCol = 1, va = 'c', ha = 'g', orient = 'h', coul = ICoulSeance, 
                contenu = [zip(*intituleSeances)[2]])
        

#        tableauH(ctx, nomsSeances, posZIntSeances[0], posZIntSeances[1], 
#                0.05, tailleZIntSeances[0]-0.05, tailleZIntSeances[1], 
#                nCol = 1, va = 'c', ha = 'g', orient = 'h', coul = ICoulSeance, 
#                contenu = [intSeances])
    
    
    

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
def Draw_CI(ctx, CI):
    # Rectangle arrondi
    x0, y0 = posCI
    rect_width, rect_height  = tailleCI
    
    curve_rect(ctx, x0, y0, rect_width, rect_height, 0.05)
    ctx.set_source_rgb (IcoulCI[0], IcoulCI[1], IcoulCI[2])
    ctx.fill_preserve ()
    ctx.set_source_rgba (BcoulCI[0], BcoulCI[1], BcoulCI[2])
    ctx.stroke ()
    
    #
    # code
    #
    if CI.num != None:
        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(0.02)
        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(CI.code)
        xc=x0+rect_width/2-width/2
        yc=y0+height+0.01
        ctx.move_to(xc, yc)
        ctx.set_source_rgb(0, 0, 0)
        ctx.show_text(CI.code)
    
        #
        # intitulé
        #
        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, CI.CI, x0, yc, rect_width, rect_height - height-0.01)



class Cadre():  
    def __init__(self, ctx, seance, filigrane = False): 
        self.seance = seance
        self.ctx = ctx
        self.w = wEff[seance.effectif]
        self.h = hHoraire * seance.GetDuree()
        self.filigrane = filigrane
        self.xd = None
        self.y = None
        self.dy = None
        self.seance.rect = []
        
    def __repr__(self):
        return self.seance.code
    
    def Draw(self, x, y):
        if self.filigrane:
            alpha = 0.2
        else:
            alpha = 1
            
        self.ctx.set_line_width(0.002)
        rectangle_plein(self.ctx, x, y, self.w, self.h, 
                        BCoulSeance[self.seance.typeSeance], ICoulSeance[self.seance.typeSeance], alpha)
        
        if not self.filigrane and hasattr(self.seance, 'code'):
            self.ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
            self.ctx.set_source_rgb (0,0,0)
            show_text_rect(self.ctx, self.seance.code, x, y, wEff["P"], hHoraire/4, ha = 'g', wrap = False)
        
        if not self.filigrane and self.seance.intituleDansDeroul and self.seance.intitule != "":
            self.ctx.select_font_face ("Sans", cairo.FONT_SLANT_ITALIC,
                                  cairo.FONT_WEIGHT_NORMAL)
            self.ctx.set_source_rgb (0,0,0)
            show_text_rect(self.ctx, self.seance.intitule, x, y + hHoraire/4, 
                           self.w, self.h-hHoraire/4, ha = 'g')
            
        # Sauvegarde de la position du bord droit pour les lignes de croisement
        self.xd = x+self.w
        self.y = y
        
        self.seance.rect.append([x, y, self.w, self.h])
        

class Bloc():
    def __init__(self):
        self.contenu = []
        
        
    def Draw(self, y):
        for ligne in self.contenu:
            x = posZSeances[0]
            for cadre in ligne:
                cadre.Draw(x, y)
                x += cadre.w
            if len(ligne) > 0:
                y += cadre.h
        y += ecartSeanceY
        return y
    
    def DrawCoisement(self):
        for ligne in self.contenu:
            for cadre in ligne:
                if cadre.seance.typeSeance in ["AP", "ED", "P"] and not cadre.filigrane and cadre.dy:
                    DrawCroisements(cadre.ctx, cadre.seance, cadre.xd, cadre.y + cadre.dy)
                    DrawCroisementSystemes(cadre.ctx, cadre.seance, cadre.y + cadre.dy) 
               
    
######################################################################################  
def DrawSeanceRacine(ctx, seance):
    global cursY
    
    #
    # Flèche indiquant la durée
    #
    h = hHoraire * seance.GetDuree()
    fleche_verticale(ctx, posZDeroul[0], cursY, 
                     h, 0.02, (0.9,0.8,0.8,0.5))
    ctx.set_source_rgb(0.5,0.8,0.8)
    ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
    show_text_rect(ctx, getHoraireTxt(seance.GetDuree()), posZDeroul[0]-0.01, cursY, 
                   0.02, h, orient = 'v')
        
    #
    # Fonction pour obtenir les lignes de séances du bloc
    #
    def getLigne(s, filigrane = False):
        l = []
        if s.typeSeance == "S":
            for j,ss in enumerate(s.sousSeances):
                if ss.typeSeance != '':
                    for i in range(int(ss.nombre.v[0])):
                        l.append(Cadre(ctx, ss, filigrane = filigrane))
                    
                    # On en profite pour calculer les positions des lignes de croisement
                    if not filigrane:
                        l[-1].dy = (j+1) * l[-1].h/(len(s.sousSeances)+1)
        
        else:
            if s.typeSeance != '':
                for i in range(int(s.nombre.v[0])):
                    l.append(Cadre(ctx, s, filigrane = filigrane))
                
                # On en profite pour calculer les positions des lignes de croisement
                if not filigrane:
                    l[-1].dy = l[-1].h/2
        
        
        return l
    
    
    
    #
    # Remplissage du bloc
    #
    bloc = Bloc()
    if not seance.typeSeance in ["R", "S", ""]:
        if seance.typeSeance in ["AP", "ED", "P"]:
            l = []
            for i in range(int(seance.nombre.v[0])):
                l.append(Cadre(ctx, seance))
            bloc.contenu.append(l)
        else:
            bloc.contenu.append([Cadre(ctx, seance)])
    else:
        if seance.typeSeance == "R":
            for s in seance.sousSeances:
                bloc.contenu.append(getLigne(s))
                
            #
            # Aperçu en filigrane de la rotation
            #
            if seance.IsEffectifOk() < 2:
                l = seance.sousSeances
                eff = seance.GetEffectif()
                if eff == 16:
                    codeEff = "C"
                elif eff == 8:
                    codeEff = "G"
                elif eff == 4:
                    codeEff = "D"
                elif eff == 2:
                    codeEff = "E"
                elif eff == 1:
                    codeEff = "P"
                
                for t in range(len(seance.sousSeances)-1):
                    l = permut(l)
                    for i, s in enumerate(l):
                        bloc.contenu[i].extend(getLigne(s, filigrane = True))

        elif seance.typeSeance == "S":
            bloc.contenu.append(getLigne(seance))
    #
    # Tracé des cadres de séance
    #
    cursY = bloc.Draw(cursY)
    
    #
    # Tracé des croisements "Démarche" et "Systèmes"
    #
    bloc.DrawCoisement() 
    
#######################################################################################  
#def Draw_seance2(ctx, seance, curseur, typParent = "", rotation = False, ):
#    if not seance.EstSousSeance():
#        h = hHoraire * seance.GetDuree()
#        fleche_verticale(ctx, posZDeroul[0], curseur[1], 
#                         h, 0.02, (0.9,0.8,0.8,0.5))
#        ctx.set_source_rgb(0.5,0.8,0.8)
#        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
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
#                ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                                      cairo.FONT_WEIGHT_BOLD)
#                ctx.set_source_rgb (0,0,0)
#                show_text_rect(ctx, seance.code, x+w*i, y, wEff["P"], hHoraire/4, ha = 'g', wrap = False)
#            
#            if not rotation and seance.intituleDansDeroul and seance.intitule != "":
#                ctx.select_font_face ("Sans", cairo.FONT_SLANT_ITALIC,
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
#            DrawCroisements(ctx, seance, x+w*seance.nombre.v[0], ys)
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
def DrawCroisementSystemes(ctx, seance, y):
#        if self.typeSeance in ["AP", "ED", "P"]:
#            and not (self.EstSousSeance() and self.parent.typeSeance == "S"):
    r = wColSysteme/3
    ns = seance.GetNbrSystemes()
    for s, n in ns.items():
        if n > 0:
            x = xSystemes[s]
            ctx.arc(x, y, r, 0, 2*pi)
            ctx.set_source_rgba (1,0.2,0.2,1.0)
            ctx.fill_preserve ()
            ctx.set_source_rgba (0,0,0,1)
            ctx.stroke ()
            ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
            show_text_rect(ctx, str(n), x-r, y-r, 2*r, 2*r)
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
def DrawCroisements(ctx, seance, x, y):

    #
    # Les lignes horizontales
    #
    if seance.typeSeance in ["AP", "ED", "P"]:
        DrawLigne(ctx, x, y)
        
    #
    # Croisements Séance/Démarche
    #
    _x = xDemarche[seance.demarche]
#        if self.typeSeance in ["AP", "ED", "P"]:
    r = 0.008
    boule(ctx, _x, y, r)
    seance.rect.append((_x -r , y - r, 2*r, 2*r))




def permut(liste):
    l = []
    for a in liste[1:]:
        l.append(a)
    l.append(liste[0])
    return l
    
    
def getHoraireTxt(v): 
    h, m = divmod(v*60, 60)
    h = str(int(h))
    if m == 0:
        m = ""
    else:
        m = str(int(m))
    return h+"h"+m


######################################################################################
#
#   Fonction générales de tracé de figures avancées
#
######################################################################################           
def calc_h_texte(ctx, texte, w, taille, va = 'c', ha = 'c', b = 0.1, orient = 'h'):
    """ Renvoie la hauteur du rectangle et le texte wrappé
        x, y, w : position et dimensions du rectangle
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        b : écart mini du texte par rapport au bord (relativement aux dimensionx du rectangle)
        orient : orientation du texte ('h', 'v')
    """
    if texte == "":
        return
#    if orient == 'v':
#        ctx.rotate(-pi/2)
#        calc_h_texte(ctx, texte, -y-h, x, h, w, va, ha, b)
#        ctx.rotate(pi/2)
#        return
    
    #
    # "réduction" du réctangle
    #
    ecart = w*b/2
#    x, y = x+ecart, y+ecart
    w = w-2*ecart
    
    ctx.set_font_size(taille)
    
    ll = []
    lt = texte.split()
    i = 0
    j = 1
    continuer = True
    while continuer:
        if j > len(lt):
            continuer = False
            ll.append(" ".join(lt[i:j-1]))
        else:
            t = " ".join(lt[i:j])
            width = ctx.text_extents(t)[2]
            if width > w:
                if j - i == 1:
                    lt[i:j] = textwrap.wrap(lt[i], int(1.0*len(lt)*w/width))
                else:
                    ll.append(" ".join(lt[i:j-1]))
                    i = j-1
            else:
                j += 1
#    print texte
#    print "-->", ll
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    return (fascent+fdescent)*len(ll), ll
#    #
#    # On dessine toutes les lignes de texte
#    #
#    
#    h = (fascent+fdescent)*len(ll)
#    for l, t in enumerate(ll):
##        print "  ",t
#        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
#        xt, yt = x+xbearing+(w-width)/2, y + (fascent+fdescent)*l - fdescent + fheight
##        print "  ",xt, yt
#        if ha == 'c':
#            ctx.move_to(xt, yt)
#        elif ha == 'g':
#            ctx.move_to(x, yt)
#        
#        ctx.show_text(t)
#        
#    
#    ctx.stroke()
   
    
    
def show_text_rect(ctx, texte, x, y, w, h, va = 'c', ha = 'c', b = 0.2, orient = 'h', 
                   max_font = None, wrap = True):
    """ Affiche un texte en adaptant la taille de police et sa position
        pour qu'il rentre dans le rectangle
        x, y, w, h : position et dimensions du rectangle
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        b : écart mini du texte par rapport au bord (relativement aux dimensionx du rectangle)
        orient : orientation du texte ('h', 'v')
    """
#    print "show_text_rect", texte

    if texte == "":
        return
    if orient == 'v':
        ctx.rotate(-pi/2)
        show_text_rect(ctx, texte, -y-h, x, h, w, va, ha, b)
        ctx.rotate(pi/2)
        return
    
    #
    # "réduction" du réctangle
    #
    ecart = min(w*b/2, h*b/2)
    x, y = x+ecart, y+ecart
    w, h = w-2*ecart, h-2*ecart
 
    
    #
    # Estimation de l'encombrement du texte (pour une taille de police de 1)
    # 
    ctx.set_font_size(1.0)
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(texte)
    volumeTexte = 1.0*width*(fascent-fdescent)

    ratioRect = 1.0*h/w
    W = sqrt(volumeTexte/ratioRect)
    H = ratioRect*W
    
    #
    # Découpage du texte
    #
    if wrap:
        continuer = True
        wrap = 0
        for l in texte.split("\n"):
            wrap = max(wrap, len(l))
        i = 0
        while continuer:
            lt = []
            i += 1
            for l in texte.split("\n"):
                lt.extend(textwrap.wrap(l, wrap))
            maxw = 0
            for t in lt:
                xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
                maxw = max(maxw, width)
            _w, _h = maxw, (fascent+fdescent) * len(lt)
            if _w/_h <= w/h:
                continuer = False
            else:
                wrap += -1
        wrap += 1
        lt = []
        for l in texte.split("\n"):
            lt.extend(textwrap.wrap(l, wrap))
        nLignes = len(lt)
        
        
        
        
        
        
#        r1 = round(H/(fascent-fdescent))
#        r2 = round(width/W)
#        print r1, r2
#        nLignes = max(1,int((r1+r2)/2))
#    #    nLignes += texte.count("\n")
#        print nLignes
#        
#        wrap = len(texte)/nLignes
#        continuer = True
#        i = 0
#        while continuer:
#            lt = []
#            i += 1
#            for l in texte.split("\n"):
#                lt.extend(textwrap.wrap(l, wrap))
#            nL = len(lt)
#            if nL == nLignes or i > len(texte):
#                continuer = False
#            elif nL > nLignes:
#                wrap += 1
#            else:
#                wrap += -1
#        nLignes = nL
    else:
        nLignes = 1
        lt = [texte]
    #
    # Calcul de la taille de police nécessaire pour que ça rentre
    #
    maxw = 0
    for t in lt:
        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
        maxw = max(maxw, width)
    hTotale = (fascent+fdescent)*nLignes
#    print "hTotale", hTotale
    fontSize = min(w/maxw, h/(hTotale))
#    print "fontSize 1", fontSize
    if max_font != None:
        fontSize = min(fontSize, max_font)
    ctx.set_font_size(fontSize)
    
    # 2 ème tour
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    maxw = 0
    for t in lt:
        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
        maxw = max(maxw, width)
    fontSize = min(fontSize, fontSize*w/maxw)
#    print "fontSize 2", fontSize
    
#    print "fontSize", fontSize
    ctx.set_font_size(fontSize)
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    
    
    #
    # On dessine toutes les lignes de texte
    #
    
    dy = (h-(fascent+fdescent)*nLignes)/2
    
#    print "dy", dy
    
    for l, t in enumerate(lt):
#        print "  ",t
        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
        xt, yt = x+xbearing+(w-width)/2, y + (fascent+fdescent)*l - fdescent + fheight + dy
#        print "  ",xt, yt
        if ha == 'c':
            ctx.move_to(xt, yt)
        elif ha == 'g':
            ctx.move_to(x, yt)
        
        ctx.show_text(t)
        
    
    ctx.stroke()
    return


def curve_rect(ctx, x0, y0, rect_width, rect_height, radius):
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
    
def tableauV(ctx, titres, x, y, w, ht, hl, nlignes = 0, va = 'c', ha = 'c', orient = 'h', coul = (0.9,0.9,0.9)):
    wc = w/len(titres)
    _x = x
    _coul = ctx.get_source().get_rgba()
#    print "tableau", _coul
    for titre in titres:
#        print "    ",titre
        ctx.rectangle(_x, y, wc, ht)
        ctx.set_source_rgb (coul[0], coul[1], coul[2])
        ctx.fill_preserve ()
        ctx.set_source_rgba (_coul[0], _coul[1], _coul[2], _coul[3])
        show_text_rect(ctx, titre, _x, y, wc, ht, va = va, ha = ha, orient = orient)
        ctx.stroke ()
        _x += wc
    
    _x = x
    _y = y+ht
    for l in range(nlignes):
        ctx.rectangle(_x, _y, wc, hl)
        _x += wc
        _y += hl
        
    ctx.stroke ()
    
def tableauH(ctx, titres, x, y, wt, wc, h, nCol = 0, va = 'c', ha = 'c', orient = 'h', 
             coul = (0.9,0.9,0.9), contenu = []):
    hc = h/len(titres)
    _y = y
    _coul = ctx.get_source().get_rgba()
#    print "tableauH", _coul
    for titre in titres:
#        print "    ",titre
        ctx.rectangle(x, _y, wt, hc)
        if type(coul) == dict :
            col = coul[titre.rstrip("1234567890.")]
        else:
            col = coul
        ctx.set_source_rgb (col[0], col[1], col[2])
        ctx.fill_preserve ()
        ctx.set_source_rgba (_coul[0], _coul[1], _coul[2], _coul[3])
        show_text_rect(ctx, titre, x, _y, wt, hc, va = va, ha = ha, orient = orient)
        ctx.stroke ()
        _y += hc
    
    _x = x+wt
    _y = y
    for c in range(nCol):
        for l in range(len(titres)):
            ctx.rectangle(_x, _y, wc, hc)
            _y += hc
        _x += wc
        _y = y
    
    _y = y
    _x = x+wt
    for c in contenu:
        for l in c:
            show_text_rect(ctx, l, _x, _y, wc, hc, va = va, ha = ha, orient = orient)
            _y += hc
        _x += wc
        _y = y
        
    ctx.stroke ()

def tableauH_var(ctx, titres, x, y, wt, wc, hl, taille, nCol = 0, va = 'c', ha = 'c', orient = 'h', 
             coul = (0.9,0.9,0.9), contenu = []):
#    hc = h/len(titres)
    _y = y
    _coul = ctx.get_source().get_rgba()
#    print "tableauH", _coul
    for i, titre in enumerate(titres):
#        print "    ",titre
        ctx.rectangle(x, _y, wt, hl[i])
        if type(coul) == dict :
            col = coul[titre.rstrip("1234567890.")]
        else:
            col = coul
        ctx.set_source_rgb (col[0], col[1], col[2])
        ctx.fill_preserve ()
        ctx.set_source_rgba (_coul[0], _coul[1], _coul[2], _coul[3])
        show_text_rect(ctx, titre, x, _y, wt, hl[i], va = va, ha = ha, orient = orient, max_font = taille)
        ctx.stroke ()
        _y += hl[i]
    
    _x = x+wt
    _y = y
    for c in range(nCol):
        for l in range(len(titres)):
            ctx.rectangle(_x, _y, wc, hl[c])
            _y += hl[c]
        _x += wc
        _y = y
    
    _y = y
    _x = x+wt
    ctx.set_font_size(taille)
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    for c in contenu:
        for j, l in enumerate(c):
            #
            # On dessine toutes les lignes de texte
            #
            
#            h = (fascent+fdescent)*len(ll)
            for i, t in enumerate(l):
        #        print "  ",t
                xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
                xt, yt = _x+xbearing+(wc-width)/2, _y + (fascent+fdescent)*i - fdescent + fheight
        #        print "  ",xt, yt
                if ha == 'c':
                    ctx.move_to(xt, yt)
                elif ha == 'g':
                    ctx.move_to(_x, yt)
                
                ctx.show_text(t)
            
            
            
            
#            show_text_rect(ctx, l, _x, _y, wc, hl[c], va = va, ha = ha, orient = orient, max_font = taille)
            _y += hl[j]
        _x += wc
        _y = y
        
    ctx.stroke ()
    
    
def rectangle_plein(ctx, x, y, w, h, coulBord, coulInter, alpha = 1):
    ctx.rectangle(x, y, w, h)
    ctx.set_source_rgba (coulInter[0], coulInter[1], coulInter[2], alpha)
    ctx.fill_preserve ()
    ctx.set_source_rgba (coulBord[0], coulBord[1], coulBord[2], alpha)
    ctx.stroke ()
    
def boule(ctx, x, y, r):
    pat = cairo.RadialGradient (x-r/2, y-r/2, r/4,
                                x-r/3, y-r/3, 3*r/2)
    pat.add_color_stop_rgba (0, 1, 1, 1, 1)
    pat.add_color_stop_rgba (1, 0, 0, 0, 1)
    ctx.set_source (pat)
    ctx.arc (x, y, r, 0, 2*pi)
    ctx.fill ()
        
        
def fleche_verticale(ctx, x, y, h, e, coul):
    ctx.set_source_rgba (coul[0], coul[1], coul[2], coul[3])
    ctx.move_to(x-e/2, y)
    ctx.line_to(x-e/2, y+h-e/2)
    ctx.line_to(x, y+h)
    ctx.line_to(x+e/2, y+h-e/2)
    ctx.line_to(x+e/2, y)
    ctx.close_path ()
    ctx.fill ()
    

def fleche_ronde(ctx, x, y, r, a0, a1, e, f, coul):
    """ Dessine une flèche
        x, y = centre
        r = rayon
        a0, a1 = angles de départ et d'arrivée (en degrés)
        e = épaisseur
        f = taille du bout de flèche
    """
    ctx.set_line_width (e)
    ctx.set_source_rgba (coul[0], coul[1], coul[2], coul[3])
#    a0 = (90-a/2) * pi/180 + f/r/2
#    a1 = (90+a/2) * pi/180 + f/r/2
    a2 = (90-a0) * pi/180
    a0 = a0 * pi/180+ f/r/2
    a1 = a1 * pi/180 
    
#    a2 = a/2 * pi/180
    
    ctx.arc (x, y, r, a0, a1)
    ctx.stroke ()

    # angle du bout de flèche
    af = pi/5
    _x, _y = x+r*sin(a2), y+r*cos(a2)
    ctx.move_to(_x, _y)
    ctx.line_to(_x-f*cos(af-a2), _y-f*sin(af-a2))
    ctx.line_to(_x-f*cos(-a2-af), _y-f*sin(-a2-af))

    ctx.close_path ()
    ctx.fill ()
    
    
    
def liste_code_texte(ctx, lstCodes, lstTexte, x, y, w, h, e):
    lstRect = []
    no = len(lstCodes)
    if no > 0:
        hl = h/no
        for i, t in enumerate(lstCodes):
            ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
            show_text_rect(ctx, t, x+e, y+i*hl, 
                           w/6-e, hl, b = 0.2, ha = 'g', max_font = 0.012, wrap = False)
            ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_NORMAL)
            show_text_rect(ctx, lstTexte[i], x+w/6, y+i*hl, 
                           w*5/6-e, hl, b = 0.2, ha = 'g')
    
            ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
            lstRect.append((x+e, y+i*hl, w, hl))
    return lstRect
    
    
#    no = len(lstCodes)
#    e = 0.01
#    for i, t in enumerate(lstCodes):
#        hl = (rect_height-htitre-0.015)/no
#        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                              cairo.FONT_WEIGHT_BOLD)
#        show_text_rect(ctx, t, x0+e, ytitre+i*hl, 
#                       rect_width/6-e, hl, b = 0.2, ha = 'g', max_font = 0.012, wrap = False)
#        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                              cairo.FONT_WEIGHT_NORMAL)
#        show_text_rect(ctx, lstTexte[i], x0+rect_width/6, ytitre+i*hl, 
#                       rect_width*5/6-e, hl, b = 0.2, ha = 'g')
#
#        ctx.select_font_face ("Sans", cairo.FONT_SLANT_NORMAL,
#                              cairo.FONT_WEIGHT_BOLD)
    
