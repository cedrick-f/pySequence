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

from constantes import Effectifs, NomsEffectifs, listeDemarches, Demarches, getSavoir, getCompetence, DemarchesCourt
import constantes

# Pour dessiner la cible ...
import os
import tempfile
import wx

#
# Données pour le tracé
#

minFont = 0.008
maxFont = 0.1

font_family = "arial"

# Marges
margeX = 0.02
margeY = 0.04

# Ecarts
ecartX = 0.03
ecartY = 0.03

LargeurTotale = 0.72414 # Pour faire du A4



# Support du projet
tailleSup = (0.17, 0.085)
posSup = (margeX, margeY)
IcoulSup = (0.9, 0.8, 0.8, 0.85)
BcoulSup = (0.3, 0.2, 0.25, 1)
fontSup = 0.014


# Equipe pédagogique
tailleEqu = (0.29, 0.18 - tailleSup[1] - ecartY/2)
posEqu = (margeX, posSup[1] + tailleSup[1] + ecartY/2)
IcoulEqu = (0.8, 0.8, 0.9, 0.85)
BcoulEqu = (0.2, 0.25, 0.3, 1)
fontEqu = 0.014

# Position dans l'année
posPos = [None, margeY - ecartY/2]
taillePos = [None, 0.04]
IcoulPos = (0.8, 0.8, 1, 0.85)
BcoulPos = (0.1, 0.1, 0.25, 1)
AcoulPos = (1, 0.4, 0, 1)
fontPos = 0.014


# Problématique
posPro = [posEqu[0] + tailleEqu[0] + ecartX/2, margeY + taillePos[1] + ecartY/2]
taillePro = [LargeurTotale - margeX - posPro[0], posEqu[1] + tailleEqu[1] - posPro[1]]
IcoulPro = (0.8, 0.9, 0.8, 0.85)
BcoulPro = (0.25, 0.3, 0.2, 1)
fontPro = 0.014

# Image du support
posImg = [posSup[0] + tailleSup[0] + ecartX/4, margeY - ecartY/2]
tailleImg = [posPro[0] - posSup[0] - tailleSup[0] - ecartX/2, None]
tailleImg[1] = tailleImg[0] 
IcoulImg = (0.8, 0.8, 1, 0.85)
BcoulImg = (0.1, 0.1, 0.25, 1)
centreImg = (posImg[0] + tailleImg[0] / 2 + 0.0006, posImg[1] + tailleImg[0] / 2 - 0.004)

# Zone d'organisation du projet (grand cadre)
posZOrganis = (margeX, 0.24)
bordureZOrganis = 0.01
tailleZOrganis = (LargeurTotale-2*margeX, 1-ecartY-posZOrganis[1]-bordureZOrganis)

# Zone de déroulement du projet
posZDeroul = [margeX, None]
tailleZDeroul = [None, None]
IcoulZDeroul = (1, 1, 0.7, 0.85)
BcoulZDeroul = (0.4, 0.4, 0.03, 1)
fontZDeroul = 0.014
wPhases = 0.02      # Taille du label "phases"
wDuree = 0.015       # Taille de la fleche "duree"


# Zones des tableaux des éléves
posZElevesV = [None, 0.24]
tailleZElevesV = [None, None]
posZElevesH = [posZDeroul[0], posZElevesV[1]]
tailleZElevesH = [None, None]
wColEleves = 0.020
xEleves = []
yEleves = []

# Zone du tableau des compétences
posZComp = [None, None]
tailleZComp = [None, None]
wColComp = 0.018
xComp = {}
ICoulCompR = (0.85, 0.7, 0.95, 0.2)      # couleur "Revue"
ICoulCompS = (0.95, 0.7, 0.85, 0.2)      # couleur "Soutenance"
BCoulCompR = (0.3, 0.2, 0.4, 1)      # couleur "Revue"
BCoulCompS = (0.4, 0.2, 0.3, 1)      # couleur "Soutenance"


# Zone des tâches
posZTaches = [posZDeroul[0] + wPhases + wDuree + ecartX*3/4, None]
tailleZTaches = [None, None]
hHoraire = None
ecartTacheY = None  # Ecartement entre les tâches de phase différente
BCoulTache = {'Ana' : (0.3,0.5,0.5), 
              'Con' : (0.5,0.3,0.5), 
              'Rea' : (0.5,0.5,0.3), 
              'Val' : (0.3,0.3,0.7)}

ICoulTache = {'Ana' : (0.6, 0.8, 0.8), 
              'Con' : (0.8, 0.6, 0.8), 
              'Rea' : (0.8, 0.8, 0.6), 
              'Val' : (0.6, 0.6, 1.0)}

ecartYElevesTaches = 0.05


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
    config.set(section, "pos", coord2str(posSup))
    config.set(section, "dim", coord2str(tailleSup))
    config.set(section, "coulInt", coul2str(IcoulSup))
    config.set(section, "coulBord", coul2str(BcoulSup))
    
    section = "Objectifs"
    config.add_section(section)
    config.set(section, "pos", coord2str(posPro))
    config.set(section, "dim", coord2str(taillePro))
    config.set(section, "coulInt", coul2str(IcoulPro))
    config.set(section, "coulBord", coul2str(BcoulPro))

    section = "Prerequis"
    config.add_section(section)
    config.set(section, "pos", coord2str(posEqu))
    config.set(section, "dim", coord2str(tailleEqu))
    config.set(section, "coulInt", coul2str(IcoulEqu))
    config.set(section, "coulBord", coul2str(BcoulEqu))

    section = "Zone d'organisation"
    config.add_section(section)
    config.set(section, "pos", coord2str(posZOrganis))
    config.set(section, "dim", coord2str(tailleZOrganis))

    section = "Zone de deroulement"
    config.add_section(section)
    config.set(section, "pos", coord2str(posZDeroul))

    section = "Tableau systemes"
    config.add_section(section)
    config.set(section, "posY", str(posZComp[1]))
    config.set(section, "col", str(wColComp))

    section = "Tableau demarche"
    config.add_section(section)
    config.set(section, "posY", str(posZElevesV[1]))
    config.set(section, "dimX", str(tailleZElevesV[0]))
    
    section = "Intitule des seances"
    config.add_section(section)
    config.set(section, "posX", str(posZIntTaches[0]))
    config.set(section, "dimX", str(tailleZIntTaches[0]))
    config.set(section, "haut", str(hIntTache))

    section = "Seances"
    config.add_section(section)
    config.set(section, "pos", coord2str(posZTaches))
    for k, v in BCoulTache.items():
        config.set(section, "Bcoul"+k, coul2str(v))
    for k, v in ICoulTache.items():
        config.set(section, "Icoul"+k, coul2str(v))
        
    config.write(open(nomFichier,'w'))
    
    
    
    
    
    
def ouvrirConfigFiche(nomFichier):
#    print "ouvrirConfigFiche"
    global posIntitule, tailleIntitule, IcoulIntitule, BcoulIntitule, \
           posSup, tailleSup, IcoulSup, BcoulSup, \
           posPro, taillePro, IcoulPro, BcoulPro, \
           posZOrganis, tailleZOrganis, \
           posZDeroul, wColComp, hIntTache, posZTaches, \
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
    posSup = str2coord(config.get(section,"pos"))
    tailleSup = str2coord(config.get(section,"dim"))
    IcoulSup = str2coul(config.get(section,"coulInt"))
    BcoulSup = str2coul(config.get(section,"coulBord"))
    
    section = "Objectifs"
    posPro = str2coord(config.get(section,"pos"))
    taillePro = str2coord(config.get(section,"dim"))
    IcoulPro = str2coul(config.get(section,"coulInt"))
    BcoulPro = str2coul(config.get(section,"coulBord"))

    section = "Prerequis"
    posEqu = str2coord(config.get(section,"pos"))
    tailleEqu = str2coord(config.get(section,"dim"))
    IcoulEqu = str2coul(config.get(section,"coulInt"))
    BcoulEqu = str2coul(config.get(section,"coulBord"))
    
    section = "Zone d'organisation"
    posZOrganis = str2coord(config.get(section,"pos"))
    tailleZOrganis = str2coord(config.get(section,"dim"))
    
    section = "Zone de deroulement"
    posZDeroul = str2coord(config.get(section,"pos"))

    section = "Tableau systemes"
    posZComp[1] = config.getfloat(section,"posY")
    wColComp = config.getfloat(section,"col")

    section = "Tableau demarche"
    posZElevesV[1] = config.getfloat(section,"posY")
    tailleZElevesV[0] = config.getfloat(section,"dimX")
    
    section = "Intitule des seances"
    posZIntTaches[0] = config.getfloat(section,"posX")
    tailleZIntTaches[0] = config.getfloat(section,"dimX")
    hIntTache = config.getfloat(section,"haut")
    
    section = "Seances"
    posZTaches = str2coord(config.get(section,"pos"))
    for k in BCoulTache.keys():
        BCoulTache[k] = str2coul(config.get(section, "Bcoul"+k))
    for k in ICoulTache.keys():
        ICoulTache[k] = str2coul(config.get(section, "Icoul"+k))
    
    

######################################################################################  
def DefinirZones(prj, ctx):
    """ Calcule les positions et dimensions des différentes zones de tracé
        en fonction du nombre d'éléments (élèves, tâches, compétences)
    """
    global hHoraire, ecartTacheY, intituleTaches, fontIntTaches, xEleves, yEleves
    
    #
    # Zone du tableau des compétences - X
    #
    competences = prj.GetCompetencesUtil()
    tailleZComp[0] = wColComp * len(competences)
    posZComp[0] = posZOrganis[0] + tailleZOrganis[0] - tailleZComp[0]
    for i, s in enumerate(competences):
        xComp[s] = posZComp[0] + (i+0.5) * wColComp
    
    #
    # Zone du tableau des élèves
    #
    tailleZElevesV[0] = wColEleves * len(prj.eleves)
    tailleZElevesH[1] = tailleZElevesV[0]
    posZElevesV[0] = posZComp[0] - tailleZElevesV[0] - ecartX/2
    tailleZElevesH[0] = posZElevesV[0]-posZElevesH[0]
    tailleZElevesV[1] = posZOrganis[1] + tailleZOrganis[1] - posZElevesV[1]
    xEleves = []
    yEleves = []
    for i in range(len(prj.eleves)):
        xEleves.append(posZElevesV[0] + (i+0.5) * wColEleves)
        yEleves.append(posZElevesH[1] + (i+0.5) * wColEleves)


    # Zone du tableau des compétences - Y
    posZComp[1] = posZElevesH[1] + tailleZElevesH[1]
    tailleZComp[1] = ecartYElevesTaches            
                 
                 
    # Zone de déroulement du projet
    posZDeroul[1] = posZElevesH[1] + tailleZElevesH[1] + tailleZComp[1]
    tailleZDeroul[0] = posZElevesV[0] - posZDeroul[0] - ecartX/2
    tailleZDeroul[1] = posZOrganis[1] + tailleZOrganis[1] - posZDeroul[1]
    
    
    # Zone des tâches
    posZTaches[1] = posZDeroul[1] + ecartY/2
    tailleZTaches[0] = posZDeroul[0] + tailleZDeroul[0] - posZTaches[0] - ecartX/2
    tailleZTaches[1] = tailleZDeroul[1] - ecartY - 0.05    # écart pour la durée totale
    
    
    hHoraire = tailleZTaches[1] / (prj.GetDureeGraph() + 0.25*(prj.GetNbrPhases()-1))
    ecartTacheY = hHoraire/4
    if ecartTacheY > 0.02:
        ecartTacheY = 0.02
        hHoraire = (tailleZTaches[1] - (prj.GetNbrPhases()-1)*ecartTacheY) / prj.GetDureeGraph()


#######################################################################################
#curseur = None 
#def InitCurseur():
#    global cursY
##    curseur = [posZTaches[0], posZTaches[1]]
#    cursY = posZTaches[1]
    
    
def getPts(lst_rect):
        lst = []
        for rect in lst_rect:
            lst.append(rect[:2])
        return lst
    
######################################################################################  
def Draw(ctx, prj, mouchard = False):
    """ Dessine une fiche de séquence de la séquence <prj>
        dans un contexte cairo <ctx>
    """
    
    
#        print "Draw séquence"
#    InitCurseur()
    
    
    #
    # Options générales
    #
    options = ctx.get_font_options()
    options.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    options.set_hint_style(cairo.HINT_STYLE_NONE)#cairo.HINT_STYLE_FULL)#
    options.set_hint_metrics(cairo.HINT_METRICS_OFF)#cairo.HINT_METRICS_ON)#
    ctx.set_font_options(options)
    
    DefinirZones(prj, ctx)

    prj.pt_caract = []
    prj.rect = []
    
    #
    # Type d'enseignement
    #
    ctx.set_font_size(0.04)
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_BOLD)
    xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(prj.classe.typeEnseignement)
#    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    ctx.move_to (posPro[0] , posSup[1] - ybearing - 0.01)
    ctx.text_path (prj.classe.typeEnseignement)
    ctx.set_source_rgb (0.6, 0.6, 0.9)
    ctx.fill_preserve ()
    ctx.set_source_rgb (0, 0, 0)
    ctx.set_line_width (0.0015)
    ctx.stroke ()
    tailleTypeEns = width
    
   
    #
    # Position dans l'année
    #
    posPos[0] = posEqu[0] + tailleEqu[0] + ecartX + tailleTypeEns
    taillePos[0] =  0.72414 - posPos[0] - margeX
    ctx.set_line_width (0.0015)
    prj.rectPos = DrawPeriodes(ctx, prj.position, tailleTypeEns = tailleTypeEns)
    prj.rect.append(posPos+taillePos)
    
    
    #
    # Image
    #
    prj.support.rect = []
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
        
        prj.support.rect.append(posImg + tailleImg)
            
    
    

    #
    #  Equipe
    #
    rectEqu = posEqu + tailleEqu
    prj.pt_caract.append(curve_rect_titre(ctx, u"Equipe pédagogique",  rectEqu, BcoulEqu, IcoulEqu, fontEqu))
    
    lstTexte = []
    for p in prj.equipe:
        lstTexte.append(p.GetNomPrenom())
    lstCodes = ["*"] * len(lstTexte)

    if len(lstTexte) > 0:
        r = liste_code_texte(ctx, lstCodes, lstTexte, posEqu[0], posEqu[1], tailleEqu[0], tailleEqu[1]+0.0001, 0.008)

    prj.rect.append(rectEqu)
#        prj.pts_caract.append(getPts(r))
        

    #
    #  Problématique
    #
    prj.pt_caract.append(posPro)
    rectPro = posPro + taillePro
    prj.pt_caract.append(curve_rect_titre(ctx, u"Problématique",  rectPro, BcoulPro, IcoulPro, fontPro))
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_NORMAL)
    show_text_rect(ctx, prj.problematique, 
                   rectPro, ha = 'g', b = 0.2,
                   fontsizeMinMax = (-1, 0.016))
    prj.rect.append(rectPro)
    
    #
    #  Support
    #
    prj.support.pt_caract = []
    rectSup = posSup+tailleSup
    prj.support.pt_caract.append(curve_rect_titre(ctx, u"Support",  rectSup, BcoulSup, IcoulSup, fontSup))
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_NORMAL)
    show_text_rect(ctx, prj.support.nom, 
                   rectSup, ha = 'c', b = 0.2,
                   fontsizeMinMax = (-1, 0.016))
    
    prj.support.rect.append(rectSup)
    
    
        
        
    #
    #  Tableau des compétenecs
    #    
    competences = prj.GetCompetencesUtil()
    
    if competences != []:
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.001)
        tableauV(ctx, competences, posZComp[0], posZComp[1], 
                tailleZComp[0], tailleZComp[1], 
                0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', coul = BCoulCompS)
        
        wc = tailleZComp[0]/len(competences)
        _x = posZComp[0]
        _y0, _y1 = posZElevesH[1], posZDeroul[1] + tailleZDeroul[1]
        for s in competences:
#            s.rect=((_x, _y, wc, posZTaches[1] - posZComp[1]),)
            ctx.set_source_rgb(0, 0, 0)
            ctx.move_to(_x, _y0)# + posZTaches[1] - posZComp[1])
            ctx.line_to(_x, _y1)
            ctx.stroke()
            if len(constantes.dicCompetences_prj_simple[prj.classe.typeEnseignement][s]) > 2:
                ctx.set_source_rgba(ICoulCompS[0], ICoulCompS[1], ICoulCompS[2], 0.2)
            else:
                ctx.set_source_rgba(ICoulCompR[0], ICoulCompR[1], ICoulCompR[2], 0.2)
            ctx.rectangle(_x, _y0,  
                          wc, _y1-_y0)
            ctx.fill()
            _x += wc
        ctx.set_source_rgb(0, 0, 0)
        ctx.move_to(_x, _y0)# + posZTaches[1] - posZComp[1])
        ctx.line_to(_x, _y1)   
        ctx.stroke()

    


    #
    #  Tableau des élèves
    #    
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(0.001)
    l=[]
    for e in prj.eleves : 
        l.append(e.GetNomPrenom())
    
    if len(l) > 0:
        
        r = tableauH(ctx, l, posZElevesH[0], posZElevesH[1], 
                     tailleZElevesH[0], 0, tailleZElevesH[1], 
                     va = 'c', ha = 'g', orient = 'h', coul = constantes.COUL_ELEVES)
        
        for i, e in enumerate(prj.eleves):
            
            e.rect = [r[i]]
            
            Ic = constantes.COUL_ELEVES[i][0]
            Bc = constantes.COUL_ELEVES[i][1]
            x = posZElevesV[0]+(i+0.5)*tailleZElevesV[0]/len(prj.eleves)
            y = posZElevesH[1]+(i+0.5)*tailleZElevesH[1]/len(prj.eleves)
            
            ctx.set_source_rgb(Ic[0],Ic[1],Ic[2])
            ctx.set_line_width(0.003)
            
            ctx.move_to(posZElevesH[0]+tailleZElevesH[0], y)
            ctx.line_to(posZComp[0]+tailleZComp[0], y)
            
            ctx.stroke()
            
            
        for i, e in enumerate(prj.eleves):
            Ic = constantes.COUL_ELEVES[i][0]
            Bc = constantes.COUL_ELEVES[i][1]
            x = posZElevesV[0]+(i+0.5)*tailleZElevesV[0]/len(prj.eleves)
            y = posZElevesH[1]+(i+0.5)*tailleZElevesH[1]/len(prj.eleves)
            
            ctx.set_source_rgb(Ic[0],Ic[1],Ic[2])
            ctx.set_line_width(0.003)
            
            ctx.move_to(x, y)
            ctx.line_to(x, posZElevesV[1] + tailleZElevesV[1])
            
            ctx.stroke()
            
            DrawCroisementsElevesCompetences(ctx, e, y)
            
        
        e = 0.003
        ctx.set_line_width(0.003)
        for i in range(len(prj.eleves)) :
            x = posZElevesV[0]+(i+0.5)*tailleZElevesV[0]/len(prj.eleves)
            y = posZElevesH[1]+(i+0.5)*tailleZElevesH[1]/len(prj.eleves)+e
            ctx.set_source_rgb(1,1,1)
            ctx.move_to(x+e, y)
            ctx.line_to(x+e, posZElevesV[1] + tailleZElevesV[1])
            ctx.move_to(x-e, y)
            ctx.line_to(x-e, posZElevesV[1] + tailleZElevesV[1])
        ctx.stroke()
        
    
    
    
    
    #
    #  Tâches
    #
    curve_rect_titre(ctx, u"Tâches à réaliser",  
                     (posZDeroul[0], posZDeroul[1], 
                      tailleZDeroul[0], tailleZDeroul[1]), 
                     BcoulZDeroul, IcoulZDeroul, fontZDeroul)
    y = posZTaches[1]
    yh_phase = {}
    phase = None
    yp = y
    for t in prj.taches:
        if not t.phase in yh_phase.keys():
            yh_phase[t.phase] = [y,None]
            
        if phase != t.phase:
            if phase != None:
                yh_phase[t.phase][1] = y - yh_phase[t.phase][0]
                hp = y-yp
                
                ctx.set_source_rgb(BCoulTache[phase][0],BCoulTache[phase][1],BCoulTache[phase][2])
                ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                                                   cairo.FONT_WEIGHT_NORMAL)
                show_text_rect(ctx, constantes.NOM_PHASE_TACHE[phase], 
                       (posZDeroul[0] + ecartX/4, yp, 
                        wPhases, hp), ha = 'c', orient = 'v', b = 0.1) 
            
            y += ecartTacheY
            yp = y
            
        
        if t.phase != '':  
            y = DrawTacheRacine(ctx, t, y)    
            phase = t.phase
        
    if phase != None:
        yh_phase[t.phase][1] = y - yh_phase[t.phase][0]
        hp = y-yp
        ctx.set_source_rgb(BCoulTache[phase][0],BCoulTache[phase][1],BCoulTache[phase][2])
        ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                                           cairo.FONT_WEIGHT_NORMAL)
        show_text_rect(ctx, constantes.NOM_PHASE_TACHE[phase], 
               (posZDeroul[0] + ecartX/4, yp, 
                wPhases, hp), ha = 'c', orient = 'v', b = 0.1)    
        
        
    #
    # Durée de la séquence
    #
    ctx.set_source_rgb(0.5,0.8,0.8)
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_BOLD)
    show_text_rect(ctx, getHoraireTxt(prj.GetDuree()), 
                   (posZTaches[0] - wDuree*3/2 - ecartX/2, posZTaches[1] + tailleZTaches[1] + ecartY/2, 
                    wDuree*2, wDuree), ha = 'c', b = 0)    
    
    
    
    
    
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
    ctx.move_to(x, posZElevesV[1] + tailleZElevesV[1])
    ctx.line_to(x, y)
    ctx.stroke()
    ctx.set_dash([], 0)

######################################################################################  
def DrawPeriodes(ctx, pos = None, tailleTypeEns = 0, origine = False):
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
    
    pm = show_text_rect_fix(ctx, u"1", x, y, wt/2, ht*2/3, fontPos, 1)#, outPosMax = True)
 
    ctx.stroke ()
    show_text_rect_fix(ctx, u"ère", pm+0.002, y, wt/2, ht/3, fontPos*0.9, 1, ha = 'g')
    ctx.stroke ()
    
    pm = show_text_rect_fix(ctx, u"T", x+wt/2, y, wt/2, ht*2/3, fontPos, 1)#, outPosMax = True)

    ctx.stroke ()
    show_text_rect_fix(ctx, u"ale", pm+0.002, y, wt/2, ht/3, fontPos*0.9, 1, ha = 'g')
    ctx.stroke ()
    
    dx = 0.005
    x += dx
    h = ht/2-2*dx
    w = (wt - 10 * dx)/8
    rect = []
    for p in range(5):
        ctx.rectangle (x, y+ht/2+dx, w, h)
        rect.append((x, y+ht/2+dx, w, h))
        if pos == p:
            ctx.set_source_rgba (AcoulPos[0], AcoulPos[1], AcoulPos[2], AcoulPos[3])
        else:
            ctx.set_source_rgba (IcoulPos[0], IcoulPos[1], IcoulPos[2], IcoulPos[3])
        ctx.fill_preserve ()
        ctx.set_source_rgba (BcoulPos[0], BcoulPos[1], BcoulPos[2], BcoulPos[3])
        ctx.stroke ()
        if p == 3:
            x += dx
        x+= dx + w
        
    p = 5
    ctx.rectangle (x, y+ht/2+dx, w*3+dx*2, h)
    rect.append((x, y+ht/2+dx, w*3+dx*2, h))
    if pos == p:
        ctx.set_source_rgba (AcoulPos[0], AcoulPos[1], AcoulPos[2], AcoulPos[3])
    else:
        ctx.set_source_rgba (IcoulPos[0], IcoulPos[1], IcoulPos[2], IcoulPos[3])
    ctx.fill_preserve ()
    ctx.set_source_rgba (BcoulPos[0], BcoulPos[1], BcoulPos[2], BcoulPos[3])
    ctx.stroke ()
    
    return rect
    
    
######################################################################################  
def Draw_CI(ctx, CI):
    # Rectangle arrondi
    x0, y0 = posSup
    rect_width, rect_height  = tailleSup
    if len(CI.numCI) <= 1:
        t = u"Centre d'intérêt"
    else:
        t = u"Centres d'intérêt"
    CI.pt_caract = (curve_rect_titre(ctx, t,  (x0, y0, rect_width, rect_height), BcoulSup, IcoulSup, fontSup), 
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
        r = liste_code_texte(ctx, lstCodes, lstIntit, x0, y0+0.0001, rect_width, rect_height, e)
        CI.pts_caract = getPts(r)
        



#class Cadre():  
#    def __init__(self, ctx, tache): 
#        self.tache = tache
#        self.ctx = ctx
#        self.w = wTache
#        self.h = hHoraire * tache.GetDureeGraph()
#        self.xd = None
#        self.y = None
#        self.dy = None
#        self.tache.rect = []
#        
#        
#    def __repr__(self):
#        return self.tache.code
#    
#    def Draw(self, x, y):
#        
#        alpha = 1
#        self.tache.pts_caract.append((x, y))
#            
#        self.ctx.set_line_width(0.002)
#        rectangle_plein(self.ctx, x, y, self.w, self.h, 
#                        BCoulTache[self.tache.phase], ICoulTache[self.tache.phase], alpha)
#        
#        if hasattr(self.tache, 'code'):
#            self.ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
#                                  cairo.FONT_WEIGHT_BOLD)
#            self.ctx.set_source_rgb (0,0,0)
#            hc = max(hHoraire/4, 0.01)
#            show_text_rect(self.ctx, self.tache.code, (x, y, wTache, hc), ha = 'g', 
#                           wrap = False, fontsizeMinMax = (minFont, -1), b = 0.2)
#        
#        if self.tache.intituleDansDeroul and self.tache.intitule != "":
#            self.ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
#                                  cairo.FONT_WEIGHT_NORMAL)
#            self.ctx.set_source_rgb (0,0,0)
#            show_text_rect(self.ctx, self.tache.intitule, (x, y + hc, 
#                           self.w, self.h-hc), ha = 'g', fontsizeMinMax = (minFont, 0.015))
#            
#        # Sauvegarde de la position du bord droit pour les lignes de croisement
#        self.xd = x+self.w
#        self.y = y
#        
#        self.tache.rect.append([x, y, self.w, self.h])
#        

#class Bloc():
#    def __init__(self):
#        self.contenu = []
#        
#        
#    def Draw(self, y):
#        
#        for ligne in self.contenu:
#            x = posZTaches[0]
#            for cadre in ligne:
#                cadre.Draw(x, y)
#                x += cadre.w
#            if len(ligne) > 0:
#                y += cadre.h
#        y += ecartTacheY
#        return y
#    
#    def DrawCoisement(self):
#        for ligne in self.contenu:
#            for cadre in ligne:
#                DrawCroisementsEleves(cadre.ctx, cadre.tache, cadre.xd, cadre.y + cadre.dy)
#                DrawCroisementsCompetences(cadre.ctx, cadre.tache, cadre.y + cadre.dy) 
               
    
######################################################################################  
def DrawTacheRacine(ctx, tache, y):
    
    
    #
    # Flèche indiquant la durée
    #
    h = hHoraire * tache.GetDureeGraph()
    fleche_verticale(ctx, posZTaches[0] - wDuree/2 - ecartX/4, y, 
                     h, wDuree, (0.9,0.8,0.8,0.5))
    ctx.set_source_rgb(0.5,0.8,0.8)
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
    show_text_rect(ctx, getHoraireTxt(tache.GetDuree()), 
                   (posZTaches[0] - wDuree - ecartX/4, y, wDuree, h), 
                   orient = 'v', b = 0.1)
    
    #
    # Rectangles actifs et points caractéristiques
    #
    tache.pts_caract = []
    tache.rect = []
    
    
    #
    # Tracé du cadre de la tâche
    #
    x = posZTaches[0]
    h = hHoraire * tache.GetDureeGraph()
    tache.pts_caract.append((x, y))
        
    ctx.set_line_width(0.002)
    rectangle_plein(ctx, x, y, tailleZTaches[0], h, 
                    BCoulTache[tache.phase], ICoulTache[tache.phase], 1)
    
    if hasattr(tache, 'code'):
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
        ctx.set_source_rgb (0,0,0)
        hc = max(hHoraire/4, 0.01)
        show_text_rect(ctx, tache.code, (x, y, tailleZTaches[0], hc), ha = 'g', 
                       wrap = False, fontsizeMinMax = (minFont, -1), b = 0.2)
    
    if tache.intituleDansDeroul and tache.intitule != "":
        ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb (0,0,0)
        show_text_rect(ctx, tache.intitule, (x, y + hc, 
                       tailleZTaches[0], h-hc), ha = 'g', fontsizeMinMax = (minFont, 0.015))
        
    
    tache.rect.append([x, y, tailleZTaches[0], h])
        
        
    #
    # Tracé des croisements "Tâches" et "Eleves"
    #
    DrawCroisementsElevesTaches(ctx, tache, x + tailleZTaches[0], y + h/2)
    DrawCroisementsCompetencesTaches(ctx, tache, y + h/2)
    
    y += h
    return y
        
        
        
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
    
    
     
        
######################################################################################  
def DrawCroisementsCompetencesTaches(ctx, tache, y):
#        if self.typeSeance in ["AP", "ED", "P"]:
#            and not (self.EstSousSeance() and self.parent.typeSeance == "S"):
    r = wColComp/3
    ns = tache.competences
    for s in ns:
        x = xComp[s]
        ctx.arc(x, y, r, 0, 2*pi)
        ctx.set_source_rgba (1,0.2,0.2,1.0)
        ctx.fill_preserve ()
        ctx.set_source_rgba (0,0,0,1)
        ctx.stroke ()
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
#        show_text_rect(ctx, str(n), (x-r, y-r, 2*r, 2*r))
        tache.rect.append((x-r, y-r, 2*r, 2*r)) 
          

#####################################################################################  
def DrawCroisementsElevesTaches(ctx, tache, x, y):

    #
    # Les lignes horizontales
    #
    DrawLigne(ctx, x, y)
        
    #
    # Croisements Tâche/Eleves
    #
    r = 0.008
    for i in tache.eleves:
        _x = xEleves[i]
        boule(ctx, _x, y, r, constantes.COUL_ELEVES[i][0], constantes.COUL_ELEVES[i][1])
        tache.rect.append((_x -r , y - r, 2*r, 2*r))


######################################################################################  
def DrawCroisementsElevesCompetences(ctx, eleve, y):
#        if self.typeSeance in ["AP", "ED", "P"]:
#            and not (self.EstSousSeance() and self.parent.typeSeance == "S"):
    r = wColComp/3
    ns = eleve.GetCompetences()
    ctx.set_line_width(0.001)
    for s in ns:
        x = xComp[s]
        ctx.arc(x, y, r, 0, 2*pi)
        ctx.set_source_rgba (1,0.2,0.2,1.0)
        ctx.fill_preserve ()
        ctx.set_source_rgba (0,0,0,1)
        ctx.stroke ()
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
#        show_text_rect(ctx, str(n), (x-r, y-r, 2*r, 2*r))
#        tache.rect.append((x-r, y-r, 2*r, 2*r)) 
        

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
   
    
    
def show_text_rect(ctx, texte, rect, va = 'c', ha = 'c', b = 0.4, orient = 'h', 
                   fontsizeMinMax = (-1, -1), wrap = True):
    """ Affiche un texte en adaptant la taille de police et sa position
        pour qu'il rentre dans le rectangle
        x, y, w, h : position et dimensions du rectangle
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        b : écart mini du texte par rapport au bord (relativement aux dimensionx du rectangle)
        orient : orientation du texte ('h', 'v')
        max_font : taille maxi de la font
        min_font : le texte peut être tronqué (1 ligne)
    """
#    print "show_text_rect", texte

    if texte == "":
        return
#    print rect
    x, y, w, h = rect
    
    fontsizeMinMax = [fontsizeMinMax[0], fontsizeMinMax[1]]
    if fontsizeMinMax[0] == -1:
        fontsizeMinMax = [minFont, fontsizeMinMax[1]]
    if fontsizeMinMax[1] == -1:
        fontsizeMinMax = [fontsizeMinMax[0], maxFont]
#    print "fontsizeMinMax", fontsizeMinMax
    
    if orient == 'v':
        ctx.rotate(-pi/2)
        r = (-y-h, x, h, w)
        show_text_rect(ctx, texte, r, va, ha, b, fontsizeMinMax = fontsizeMinMax, wrap = wrap)
        ctx.rotate(pi/2)
        return
    
    
#    #
#    # "réduction" du réctangle
#    #
##    ecart = min(w*b/2, h*b/2)
#    ecartX, ecartY = w*b/2, h*b/2
#    x, y = x+ecartX, y+ecartY
#    w, h = w-2*ecartX, h-2*ecartY
 
#    if min_font:
    ctx.set_font_size(fontsizeMinMax[0])
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    hf = fascent + fdescent
    fontsizeMinMax[0] = min(fontsizeMinMax[0], fontsizeMinMax[0]*(h/hf))#-int(b*5)))
    ctx.set_font_size(fontsizeMinMax[0])
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    nLignesMaxi = max(1,int(h // hf))
        
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
                if wrap == 0:
                    continuer = False
        wrap += 1
        lt = []
        for l in texte.split("\n"):
            lt.extend(textwrap.wrap(l, wrap))
        nLignes = len(lt)
        
    else:
        nLignes = 1
        lt = [texte]
    
        
    #
    # Calcul de la taille de police nécessaire pour que ça rentre
    #
    maxw = 0
#    et = "." * int(b*5)
    for t in lt:
        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
        maxw = max(maxw, width)
    hTotale = (fascent+fdescent)*(nLignes)#+int(b*5))
#    print "hTotale", hTotale
    fontSize = min(w/maxw, h/(hTotale))
#    print "fontSize 1", fontSize
    
    #
    # "réduction" du réctangle
    #
    ctx.set_font_size(fontSize)
    ecart = min(w*b/2, h*b/2)
    ecart = min(ecart, ctx.font_extents()[2])
#    ecart = min(w*b/2, h*b/2)
#    ecartX, ecartY = w*b/2, h*b/2
    x, y = x+ecart, y+ecart
    w, h = w-2*ecart, h-2*ecart
    fontSize = min(w/maxw, h/(hTotale))
    
    if fontSize > fontsizeMinMax[1]:
        show_text_rect_fix(ctx, texte, x, y, w, h, fontsizeMinMax[1], 100, va = va, ha = ha)
        return
    
    fontSize = min(fontSize, fontsizeMinMax[1])
#    print "fontSize", fontSize
    
    if fontSize < fontsizeMinMax[0]:
#        print "FIX"
        show_text_rect_fix(ctx, texte, x, y, w, h, fontsizeMinMax[0], nLignesMaxi, va, ha)
        return
            
#    print lt, nLignes    
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
    
    show_lignes(ctx, lt, x, y, w, h, ha, va)
    
    return fontSize


def show_text_rect2(ctx, texte, rect, va = 'c', ha = 'c', b = 0.4, orient = 'h', 
                   fontsize = (-1, -1), wrap = True):
    """ Affiche un texte en adaptant la taille de police et sa position
        pour qu'il rentre dans le rectangle
        rect = (x, y, w, h) : position et dimensions du rectangle
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        b : écart mini du texte par rapport au bord (en fraction de caractère)
        orient : orientation du texte ('h', 'v')
        fontsize : taille maxi/mini de la font (-1 = auto)
    """
#    print "show_text_rect", texte

#    print "show_text_rect", texte
    
    if texte == "":
        return
    
    x, y, w, h = rect
    
    fontsize = [fontsize[0], fontsize[1]]
    if fontsize[0] == -1:
        fontsize = [minFont, fontsize[1]]
    if fontsize[1] == -1:
        fontsize = [fontsize[0], 0.1]
    
    if orient == 'v':
        ctx.rotate(-pi/2)
        r = (-y-h, x, h, w)
        show_text_rect(ctx, texte, r, va, ha, b, fontsize = fontsize, wrap = wrap)
        ctx.rotate(pi/2)
        return
    
    def ajuster_text_rect(txt, _w, _h, fsize):
#        print "   ajuster_text_rect", txt, fsize
        
        ctx.set_font_size(fsize)
        fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
        
        dx = ctx.text_extents("a")[2] * b
        
        #
        # Découpage du texte
        #
        continu = True
        wr = 0
        for l in txt.split("\n"):
            wr = max(wr, len(l))
        i = 0
#        trop = False
        while continu:
            i += 1
            # On fait une découpe à "wrap" ...
            lt = []
            for l in txt.split("\n"):
                lt.extend(textwrap.wrap(l, wr))
            
            # On teste si ça rentre ...
            maxw = 0
            for t in lt:
                xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
                maxw = max(maxw, width+2*dx)
        
            if maxw <= _w: # Ca rentre !
                continu = False
            else: # Ca ne rentre pas --> on coupe plus raz.
                wr += -1
#                if wr <= 0:
#                    trop = True
#                    continu == False
        
        #
        # Calcul du nombre de lignes nécessaires
        #
#        print "    ",fascent , fdescent
        hf = fascent + fdescent
        Nlignes = int(_h // hf)
        rapport = hf*len(lt) / _h
#        print "    ", len(lt), "*", hf, "/", _h, "=", rapport
#        print "    ", Nlignes, fsize/hf
        

#        if rapport > 1:
#            Nlignes = max(len(lt), Nlignes + 1)
        #
        # Tronquage du texte
        #
        tronque = False
        if len(lt) > Nlignes:
            tronque = True
            dl = lt[Nlignes-1]
            continu = True
            while continu:
    #            print "   ", dl
                width = ctx.text_extents(dl+" ...")[2]
                if width <= w:
                    continu = False
                else:
                    dll = dl.split()
                    if len(dll) > 1:
                        dl = " ".join(dll[:-1])
                    else:
                        continu = False
                    
            lt[Nlignes-1] = dl + " ..."
            
        lt = lt[:Nlignes]
    

        return lt, tronque, rapport, dx, hf*b
    
    continuer = True
    size = min(fontsize[1], min(w, h))
    old_size = size
    c = 0
    while continuer:
        lst_lgn, tronq, rapp, dx, dy = ajuster_text_rect(texte, w, h, size)
        c += 1
        if abs(rapp - 1) < 0.01 or abs(size - fontsize[0]) < 0.001 or c>10:
            continuer = False
        else:
#            old_old_size = old_size
            old_size = size
#            size = max(fontsize[0], size/rapp)
            size = size/sqrt(rapp)
#            if size == fontsize[0]:
#                continuer = False
#            print old_old_size, old_size, size
#            if abs(old_old_size - size) < 0.001:
##                size = (size+old_size)/2
#                size = min(size,old_size)
#                continuer = False
            
    ctx.set_font_size(size)
    
    show_lignes(ctx, lst_lgn, x+dx, y+dy, w-2*dx, h-2*dy, ha, va)
    
    return size


def show_text_rect_fix(ctx, texte, x, y, w, h, fontSize, Nlignes, va = 'c', ha = 'c'):#, outPosMax = False):
    """ Affiche un texte en tronquant sa longueur
        pour qu'il rentre dans le rectangle
        x, y, w, h : position et dimensions du rectangle
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        
        Si outFont : Renvoie la position la plus extrème à droite (pour éventuellement écrire une suite au texte)
        Sinon : Renvoie le point caractéristique du rectangle encadrant
    """
#    print "show_text_rect_fix", fontSize, Nlignes, texte

    if texte == "":
        return 0
         
    ctx.set_font_size(fontSize)

    #
    # Découpage du texte
    #
    continuer = True
    wrap = 0
    for l in texte.split("\n"):
        wrap = max(wrap, len(l))
    i = 0
    while continuer:
        i += 1
        # On fait une découpe à "wrap" ...
        lt = []
        for l in texte.split("\n"):
            lt.extend(textwrap.wrap(l, wrap))
        
        # On teste si ça rentre ...
        maxw = 0
        for t in lt:
            xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
            maxw = max(maxw, width)
    
        if maxw <= w: # Ca rentre !
            continuer = False
        else: # Ca ne rentre pas --> on coupe plus raz.
            wrap += -1
#    wrap += 1
#    lt = []
#    for l in texte.split("\n"):
#        lt.extend(textwrap.wrap(l, wrap))
#    print lt
#    print w
    
    #
    # Tronquage du texte
    #
    if len(lt) > Nlignes:
        dl = lt[Nlignes-1]
        continuer = True
        while continuer:
#            print "   ", dl
            width = ctx.text_extents(dl+" ...")[2]
            if width <= w:
                continuer = False
            else:
                dll = dl.split()
                if len(dll) > 1:
                    dl = " ".join(dll[:-1])
                else:
                    continuer = False
                
        lt[Nlignes-1] = dl + " ..."
        
    lt = lt[:Nlignes]
    
    show_lignes(ctx, lt, x, y, w, h, ha, va)
    
#    
#    if outPosMax: 
    return show_lignes(ctx, lt, x, y, w, h, ha, va)
#    else:
#        return x, y
    
     
   




def show_lignes(ctx, lignes, x, y, w, h, ha, va):
    """ Affiche une série de lignes de texte
        Renvoie la position la plus extrème à droite (pour éventuellement écrire une suite au texte)
    """
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    # pour centrer verticalement
    
    if va == 'c':
        dy = (h-(fascent+fdescent)*len(lignes))/2
    else:
        dy = 0
        
#    # Un rectangle invisible pour la séléction
#    e = ctx.get_line_width ()
#    ctx.set_line_width(0.0001)
#    ctx.rectangle(x, y, w, h)
#    ctx.stroke()
#    ctx.set_line_width(e)
#    
     
    #
    # On dessine toutes les lignes de texte
    #
    posmax = x
#    print "dy", dy
#    print "show_lignes", lignes
    for l, t in enumerate(lignes):
#        print "  ",t
        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
        
        if ha == 'c':
            xt = x+xbearing+(w-width)/2
        elif ha == 'g':
            xt = x
        
        yt = y + (fascent+fdescent)*l - fdescent + fheight + dy

        ctx.move_to(xt, yt)
        ctx.show_text(t)
        
        posmax = max(posmax, xt+width)
    
    ctx.stroke()

    return posmax
    

def curve_rect_titre(ctx, titre, rect, coul_bord, coul_int, taille_font = 0.01, rayon = 0.025, epaiss = 0.003):
    ctx.set_line_width(epaiss)
    x0, y0, rect_width, rect_height = rect
    
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(taille_font)
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(titre)
#    if width > rect_width-2*rayon:
#    
#    continuer = True
      
    c = curve_rect(ctx, x0, y0, rect_width, rect_height, rayon, 
               ouverture = min(width + fheight, rect_width-2*rayon))
    ctx.set_source_rgba (coul_int[0], coul_int[1], coul_int[2], coul_int[3])
    ctx.fill_preserve ()
    ctx.set_source_rgba (coul_bord[0], coul_bord[1], coul_bord[2], coul_bord[3])
    ctx.stroke ()
    
    xc = x0 + rayon
    yc = y0 + height/2
    mask = cairo.LinearGradient (xc, y0, xc, y0 - height*1.5)
    mask.add_color_stop_rgba (1, 1, 1, 1, 0)
    mask.add_color_stop_rgba (0, coul_int[0], coul_int[1], coul_int[2], coul_int[3])
    ctx.rectangle (xc, y0 - height, min(width + fheight, rect_width-2*rayon), height)
    ctx.set_source (mask) 
    ctx.fill ()
#    ctx.stroke ()
    
    xc = x0 + rayon + fheight/2
    yc = y0 - height
    
    ctx.move_to(xc, yc)
    ctx.set_source_rgb(0, 0, 0)
#    ctx.show_text(titre)
    
    show_text_rect_fix(ctx, titre, xc, yc, rect_width-2*rayon, fheight, taille_font, 1, ha = "g")
    
    return c

def curve_rect(ctx, x0, y0, rect_width, rect_height, radius, ouverture = 0):
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
            ctx.line_to (x1 - radius, y0)
            ctx.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
            ctx.curve_to (x1, y1, x1, y1, x1 - radius, y1)
            ctx.line_to (x0 + radius, y1)
            ctx.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
            ctx.line_to  (x0, (y0 + y1)/2)
            ctx.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
            
        else:
            ctx.move_to  (x0 + radius + ouverture, y0)
            ctx.line_to (x1 - radius, y0)
            ctx.curve_to (x1, y0, x1, y0, x1, y0 + radius)
            ctx.line_to (x1 , y1 - radius)
            ctx.curve_to (x1, y1, x1, y1, x1 - radius, y1)
            ctx.line_to (x0 + radius, y1)
            ctx.curve_to (x0, y1, x0, y1, x0, y1- radius)
            ctx.line_to (x0, y0+radius)
            ctx.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
    
    return x0 + radius + ouverture, y0 # Renvoie les coordonnées du 1er point = caractéristique du path SVG
#            ctx.move_to  (x0, y0 + radius)
#            ctx.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
#            ctx.move_to  (x0 + radius + ouverture, y0)
#            ctx.line_to (x1 - radius, y0)
#            ctx.curve_to (x1, y0, x1, y0, x1, y0 + radius)
#            ctx.line_to (x1 , y1 - radius)
#            ctx.curve_to (x1, y1, x1, y1, x1 - radius, y1)
#            ctx.line_to (x0 + radius, y1)
#            ctx.curve_to (x0, y1, x0, y1, x0, y1- radius)
    
    #ctx.close_path ()
    
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
        show_text_rect(ctx, titre, (_x, y, wc, ht), va = va, ha = ha, orient = orient)
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
    
    rect = []
    hc = h/len(titres)
    _y = y
    _coul = ctx.get_source().get_rgba()

    for i, titre in enumerate(titres):
        ctx.rectangle(x, _y, wt, hc)
        if type(coul) == dict :
            col = coul[titre.rstrip("1234567890.")]
        else:
            if type(coul[0]) == tuple:
                col = coul[i]
            else:
                col = coul
        ctx.set_source_rgb (col[0][0], col[0][1], col[0][2])
        ctx.fill_preserve ()
        ctx.set_source_rgba (_coul[0], _coul[1], _coul[2], _coul[3])
        show_text_rect(ctx, titre, (x, _y, wt, hc), va = va, ha = ha, orient = orient)
        rect.append((x, _y, wt, hc))
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
            show_text_rect(ctx, l, (_x, _y, wc, hc), va = va, ha = ha, orient = orient)
            _y += hc
        _x += wc
        _y = y
        
    ctx.stroke ()
    
    return rect

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
        show_text_rect(ctx, titre, (x, _y, wt, hl[i]), va = va, ha = ha, orient = orient, fontsizeMinMax = (-1, taille))
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
    
    
def boule(ctx, x, y, r, color0 = (1, 1, 1, 1), color1 = (0, 0, 0, 1)):
    pat = cairo.RadialGradient (x-r/2, y-r/2, r/4,
                                x-r/3, y-r/3, 3*r/2)
    pat.add_color_stop_rgba (0, color0[0], color0[1], color0[2], color0[3])
    pat.add_color_stop_rgba (1, color1[0], color1[1], color1[2], color1[3])
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
        wt = 0
        fs = None
        for i, t in enumerate(lstCodes):
            if t.strip() != "":
                ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_BOLD)
                show_text_rect(ctx, t, (x+e, y+i*hl, 
                               w/6-e, hl), b = 0.2, ha = 'g', fontsizeMinMax = (-1, 0.012), wrap = False)
                width = ctx.text_extents(t)[2]
                wt = max(wt, width)
        
        for i, t in enumerate(lstCodes):
            if lstTexte[i].strip() != "":
                ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_NORMAL)
                show_text_rect(ctx, lstTexte[i], (x+wt+2*e, y+i*hl, 
                               w-wt-3*e, hl), b = 0.4, ha = 'g', fontsizeMinMax = (-1, 0.012))
    
                rect = (x, y+i*hl, w, hl)
                lstRect.append(rect)
                
                # Un rectangle invisible pour la séléction
                ep = ctx.get_line_width()
                co = ctx.get_source().get_rgba()
                ctx.set_line_width(0.0001)
                ctx.set_source_rgba (0.5, 0.5, 0.5, 0)
                ctx.rectangle(rect[0], rect[1], rect[2], rect[3])
                
                ctx.fill_preserve()
                
                ctx.stroke()
                ctx.set_line_width(ep)
                ctx.set_source_rgba (co[0],co[1],co[2],co[3])
    #            ctx.restore()
    
    return lstRect
    
    
def show_texte(ctx, texte, x, y):
    glyphs = []
    _x, _y = x, y
    for c in texte:
        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(c)
        glyphs.append((ord(c), _x, _y))
        _x += width
    ctx.show_glyphs(glyphs)
    
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step    
    
    



def testRapport(ctx):
    f = open("testRapport.txt", 'w')
    for i in drange(0.008, 0.1, 0.0001):
        ctx.set_font_size(i)
        fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
        f.write(str(i)+ " " + str(fascent+fdescent)+"\n")
    f.close()
        
        
        
        
#    no = len(lstCodes)
#    e = 0.01
#    for i, t in enumerate(lstCodes):
#        hl = (rect_height-htitre-0.015)/no
#        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
#                              cairo.FONT_WEIGHT_BOLD)
#        show_text_rect(ctx, t, x0+e, ytitre+i*hl, 
#                       rect_width/6-e, hl, b = 0.2, ha = 'g', max_font = 0.012, wrap = False)
#        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
#                              cairo.FONT_WEIGHT_NORMAL)
#        show_text_rect(ctx, lstTexte[i], x0+rect_width/6, ytitre+i*hl, 
#                       rect_width*5/6-e, hl, b = 0.2, ha = 'g')
#
#        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
#                              cairo.FONT_WEIGHT_BOLD)
    
