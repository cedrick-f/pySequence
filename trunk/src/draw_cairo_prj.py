#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               draw_cairo_prj                            ##
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
from math import log
#import cairo
#
#import ConfigParser

from constantes import Effectifs, NomsEffectifs, listeDemarches, Demarches, getSavoir, getCompetence, DemarchesCourt
import constantes

## Pour dessiner la cible ...
import os
import tempfile
import wx

#
# Données pour le tracé
#

# Marges
margeX = 0.02
margeY = 0.04

# Ecarts
ecartX = 0.02
ecartY = 0.03



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
wPhases = 0.03      # Taille du label "phases"
wDuree = 0.012       # Taille de la fleche "duree"


# Zones des tableaux des éléves
posZElevesV = [None, 0.24]
tailleZElevesV = [None, None]
posZElevesH = [posZDeroul[0], posZElevesV[1]]
tailleZElevesH = [None, None]
wEleves = 0.015
hEleves = 0.020
xEleves = []
yEleves = []

# Zone du tableau des compétences
posZComp = [None, None]
tailleZComp = [None, None]
wColComp = 0.018
xComp = {}
ICoulCompR = (0.7, 0.6, 1, 0.2)      # couleur "Revue"
ICoulCompS = (1, 0.6, 0.7, 0.2)      # couleur "Soutenance"
#BCoulCompR = (0.3, 0.2, 0.4, 1)      # couleur "Revue"
BCoulCompS = (0.7, 0.7, 0.7, 0.2)      # couleur "Soutenance"


# Zone des tâches
posZTaches = [posZDeroul[0] + wPhases + wDuree + ecartX*3/4, None]
tailleZTaches = [None, None]
hTacheMini = ecartY/2
# paramètres pour la fonction qui calcule la hauteur des tâches 
# en fonction de leur durée
a = b = None 

ecartTacheY = None  # Ecartement entre les tâches de phase différente
BCoulTache = {'Ana' : (0.3,0.5,0.5), 
              'Con' : (0.5,0.3,0.5), 
              'DCo' : (0.55,0.3,0.45),
              'Rea' : (0.5,0.5,0.3), 
              'Val' : (0.3,0.3,0.7),
              'Rev' : (0.6,0.3,0.3),
              'R1'  : (0.8,0.3,0.2),
              'R2'  : (0.8,0.3,0.2),
              'S'   : (0.3,0.1,0.8)}

ICoulTache = {'Ana' : (0.6, 0.8, 0.8), 
              'Con' : (0.8, 0.6, 0.8),
              'DCo' : (0.9, 0.6, 0.7),
              'Rea' : (0.8, 0.8, 0.6), 
              'Val' : (0.6, 0.6, 1.0),
              'Rev' : (0.9,0.6,0.6),
              'R1'  : (1,0.6,0.5),
              'R2'  : (1,0.6,0.5),
              'S'   : (0.6,0.5,1)}


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
    

def calcH(t):
    return a*log(t*2)+b

######################################################################################  
def DefinirZones(prj, ctx):
    """ Calcule les positions et dimensions des différentes zones de tracé
        en fonction du nombre d'éléments (élèves, tâches, compétences)
    """
    global ecartTacheY, intituleTaches, fontIntTaches, xEleves, yEleves, a, b
    
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
    tailleZElevesV[0] = wEleves * len(prj.eleves)
    tailleZElevesH[1] = hEleves * len(prj.eleves)
    posZElevesV[0] = posZComp[0] - tailleZElevesV[0] - ecartX/2
    tailleZElevesH[0] = posZElevesV[0]-posZElevesH[0]
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
    posZDeroul[1] = posZElevesH[1] + tailleZElevesH[1] + tailleZComp[1]
    tailleZDeroul[0] = posZElevesV[0] - posZDeroul[0] - ecartX/2
    tailleZDeroul[1] = posZOrganis[1] + tailleZOrganis[1] - posZDeroul[1]
    
    
    # Zone des tâches
    posZTaches[1] = posZDeroul[1] + ecartY/2
    tailleZTaches[0] = posZDeroul[0] + tailleZDeroul[0] - posZTaches[0] - ecartX/2
    tailleZTaches[1] = tailleZDeroul[1] - ecartY/2 - 0.03    # écart pour la durée totale
    
    
#    hHoraire = tailleZTaches[1] / (prj.GetDureeGraph() + 0.25*(prj.GetNbrPhases()-1))
#    ecartTacheY = hHoraire/4
#    if ecartTacheY > 0.02:
    ecartTacheY = ecartY/3
    sommeEcarts = (prj.GetNbrPhases()-1)*ecartTacheY
    
    # Calcul des paramètres de la fonction hauteur = f(durée)
    # hauteur = a * log(durée) + b
    b = 0
    a = 1
    h = ecartTacheY
    for t in prj.taches:
        h += calcH(t.GetDuree())
    
    b = hTacheMini
    a = (tailleZTaches[1] - sommeEcarts - b*len(prj.taches)) / h
    
#    if prj.GetDureeGraph() > 0:
#        hHoraire = (tailleZTaches[1] - sommeEcarts) / prj.GetDureeGraph()


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
    prj.rectComp = {}
    
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
        
        prj.support.rect.append(posImg + tailleImg)
        prj.support.pts_caract.append(posImg)
    
    

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
    prj.support.pts_caract.append(curve_rect_titre(ctx, u"Support",  rectSup, BcoulSup, IcoulSup, fontSup))
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_NORMAL)
    show_text_rect(ctx, prj.support.nom, 
                   rectSup, ha = 'c', b = 0.2,
                   fontsizeMinMax = (-1, 0.016))
    
    prj.support.rect.append(rectSup)
    prj.support.pts_caract.append(posSup)
    
    
        
        
    #
    #  Tableau des compétenecs
    #    
    competences = prj.GetCompetencesUtil()
    
    if competences != []:
        
        ctx.set_line_width(0.001)
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
        
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_NORMAL)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.001)
        p = tableauV(ctx, competences, posZComp[0], posZComp[1], 
                tailleZComp[0], tailleZComp[1], 
                0, nlignes = 0, va = 'c', ha = 'g', orient = 'v', coul = BCoulCompS)
        
        prj.pt_caract_comp = getPts(p)




    #
    #  Tableau des élèves
    #    
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(0.001)
    l=[]
    for e in prj.eleves : 
        e.pts_caract = []
        l.append(e.GetNomPrenom())
    
    if len(l) > 0:
        
        
        # Barres d'évaluabilité
        for i, e in enumerate(prj.eleves):
            r, s = e.GetEvaluabilite()
            y = posZElevesH[1] + i*hEleves
#            wr = tailleZElevesH[0]*r
#            ws = tailleZElevesH[0]*s
            hb = hEleves/4
#            y = posZElevesH[1] + (2*i*hb)+hb/2
            
            barreH(ctx, posZElevesH[0], y+hb, tailleZElevesH[0], r, hb, 
                   (1, 0, 0, 0.7), (0, 1, 0, 0.7), 
                   (ICoulCompR[0], ICoulCompR[1], ICoulCompR[2], 0.7))
            
            barreH(ctx, posZElevesH[0], y+3*hb, tailleZElevesH[0], s, hb, 
                   (1, 0, 0, 0.7), (0, 1, 0, 0.7), 
                   (ICoulCompR[0], ICoulCompR[1], ICoulCompR[2], 0.7))
            
            
#            src = ctx.get_source()
#            pat = cairo.LinearGradient (0.0, y,  0.0, y+hEleves/2)
#            pat.add_color_stop_rgba (1, ICoulCompR[0], ICoulCompR[1], ICoulCompR[2], 0.5)
#            if r > 0.5:
#                pat.add_color_stop_rgba (0.5, 0, 1, 0, 0.2)
#            else:
#                pat.add_color_stop_rgba (0.5, 1, 0, 0, 0.2)
#            pat.add_color_stop_rgba (0, ICoulCompR[0], ICoulCompR[1], ICoulCompR[2], 0.5)
#            ctx.rectangle (posZElevesH[0],y,wr,hEleves/2)
#            ctx.set_source (pat)
#            ctx.fill ()
#            pat = cairo.LinearGradient (0.0, y+hEleves/2,  0.0, y+hEleves)
#            pat.add_color_stop_rgba (1, ICoulCompS[0], ICoulCompS[1], ICoulCompS[2], 0.5)
#            if s > 0.5:
#                pat.add_color_stop_rgba (0.5, 0, 1, 0, 0.2)
#            else:
#                pat.add_color_stop_rgba (0.5, 1, 0, 0, 0.2)
#            pat.add_color_stop_rgba (0, ICoulCompS[0], ICoulCompS[1], ICoulCompS[2], 0.5)
#            ctx.rectangle (posZElevesH[0],y+hEleves/2,ws,hEleves/2)
#            ctx.set_source (pat)
#            ctx.fill ()
#            ctx.set_source(src)
        
        
        rec = tableauH(ctx, l, posZElevesH[0], posZElevesH[1], 
                     tailleZElevesH[0], 0, tailleZElevesH[1], 
                     va = 'c', ha = 'd', orient = 'h', coul = constantes.COUL_ELEVES)
        
        prj.pt_caract_eleve = getPts(rec)
        
        
        # Lignes horizontales
        for i, e in enumerate(prj.eleves):
            e.rect = [rec[i]]
            Ic = constantes.COUL_ELEVES[i][0]
            
            ctx.set_source_rgb(Ic[0],Ic[1],Ic[2])
            ctx.set_line_width(0.003)
            ctx.move_to(posZElevesH[0]+tailleZElevesH[0], yEleves[i])
            ctx.line_to(posZComp[0]+tailleZComp[0], yEleves[i])
            ctx.stroke()
            
        # Lignes verticales
        for i, e in enumerate(prj.eleves):
            Ic = constantes.COUL_ELEVES[i][0]
            
            ctx.set_source_rgb(Ic[0],Ic[1],Ic[2])
            ctx.set_line_width(0.003)
            ctx.move_to(xEleves[i], yEleves[i])
            ctx.line_to(xEleves[i], posZTaches[1] + tailleZTaches[1] + (i % 2)*(ecartY/2))
            ctx.stroke()
            
            DrawCroisementsElevesCompetences(ctx, e, yEleves[i])
            
        # Ombres des lignes verticales
        e = 0.003
        ctx.set_line_width(0.003)
        for i in range(len(prj.eleves)) :
            y = posZTaches[1] + tailleZTaches[1] + (i % 2)*(ecartY/2)
            ctx.set_source_rgb(1,1,1)
            ctx.move_to(xEleves[i]+e, yEleves[i]+e)
            ctx.line_to(xEleves[i]+e, y)
            ctx.move_to(xEleves[i]-e, yEleves[i]+e)
            ctx.line_to(xEleves[i]-e, y)
        ctx.stroke()
        
        
            
    
    
    
    #
    #  Tâches
    #
    curve_rect_titre(ctx, u"Tâches à réaliser",  
                     (posZDeroul[0], posZDeroul[1], 
                      tailleZDeroul[0], tailleZDeroul[1]), 
                     BcoulZDeroul, IcoulZDeroul, fontZDeroul)
    y = posZTaches[1]
    
    # Les positions en Y haut et bas des phases
    yh_phase = {'Ana' : [[], []], 
                'Con' : [[], []], 
                'DCo' : [[], []],
                'Rea' : [[], []], 
                'Val' : [[], []]}

    phase = None
    for t in prj.taches:
        if phase != t.phase:
            y += ecartTacheY
#        print "tache", t, t.phase
        if t.phase != '':  
            yb = DrawTacheRacine(ctx, t, y)
            if t.phase in ["Ana", "Con", "DCo", "Rea", "Val"] :
                yh_phase[t.phase][0].append(y)
                yh_phase[t.phase][1].append(yb)
            y = yb
            
        phase = t.phase
    
    # Nom des phases
    for phase, yh in yh_phase.items():
#        print phase, yh
        if len(yh[0]) > 0:
            yh[0] = min(yh[0])
            yh[1] = max(yh[1])
            ctx.set_source_rgb(BCoulTache[phase][0],BCoulTache[phase][1],BCoulTache[phase][2])
            ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC,
                                               cairo.FONT_WEIGHT_NORMAL)
            show_text_rect(ctx, constantes.NOM_PHASE_TACHE[phase], 
                   (posZDeroul[0] + ecartX/4, yh[0], 
                    wPhases, yh[1]-yh[0]), ha = 'c', orient = 'v', b = 0) 

        
        
    #
    # Durées du projet (durées élèves)
    #
#    ctx.set_source_rgb(0.5,0.8,0.8)
#    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
#                                       cairo.FONT_WEIGHT_BOLD)
#    y = posZTaches[1] + tailleZTaches[1] + ecartY/4
#    
#    show_text_rect(ctx, getHoraireTxt(prj.GetDuree()), 
#                   (posZTaches[0] - wDuree*3/2 - ecartX/2, y, 
#                    wDuree*2, ecartY/2), ha = 'c', b = 0)    
    
    for i, e in enumerate(prj.eleves):
        x = posZElevesV[0]+i*tailleZElevesV[0]/len(prj.eleves)
        y = posZTaches[1] + tailleZTaches[1] + (i % 2)*(ecartY/2)
        d = e.GetDuree()
        if d < constantes.DUREE_PRJ:
            ctx.set_source_rgb(1,0.1,0.1)
        else:
            ctx.set_source_rgb(0.1,1,0.1)
        show_text_rect(ctx, getHoraireTxt(d), 
                       (x, y, wEleves, ecartY/2), ha = 'c', b = 0)
    
    
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
#    h = hHoraire * tache.GetDureeGraph()
    h = calcH(tache.GetDuree())
    if not tache.phase in ["R1", "R2", "S", "Rev"]:
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
    if not tache.phase in ["R1", "R2", "S", "Rev"]:
        x = posZTaches[0]
    else:
        x = posZTaches[0] - wDuree/2 - ecartX/4

    tache.pts_caract.append((x, y))
        
    ctx.set_line_width(0.002)
    rectangle_plein(ctx, x, y, tailleZTaches[0], h, 
                    BCoulTache[tache.phase], ICoulTache[tache.phase], 1)
    
    if hasattr(tache, 'code'):
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
        ctx.set_source_rgb (0,0,0)
        hc = max(hTacheMini, 0.01)
        if not tache.phase in ["R1", "R2", "S"]:
            t = tache.code
        else:
            t = tache.intitule
        show_text_rect(ctx, t, (x, y, tailleZTaches[0], hc), ha = 'g', 
                       wrap = False, fontsizeMinMax = (minFont, -1), b = 0.2)
    
    if tache.intituleDansDeroul and tache.intitule != "" and not tache.phase in ["R1", "R2", "S"]:
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
            show_text_rect(ctx, tache.intitule, rect, 
                           ha = 'g', fontsizeMinMax = (minFont, 0.015))
        
    
    tache.rect.append([x, y, tailleZTaches[0], h])
        
        
    #
    # Tracé des croisements "Tâches" et "Eleves"
    #
    if tache.phase != "S":
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
        if len(constantes.dicCompetences_prj_simple[tache.parent.classe.typeEnseignement][s]) > 2:
            ctx.set_source_rgba (ICoulCompS[0],ICoulCompS[1],ICoulCompS[2],1.0)
        else:
            ctx.set_source_rgba (ICoulCompR[0],ICoulCompR[1],ICoulCompR[2],1.0)
        ctx.fill_preserve ()
        ctx.set_source_rgba (0,0,0,1)
        ctx.stroke ()
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
        if s in tache.parent.rectComp.keys() and tache.parent.rectComp[s] != None:
            tache.parent.rectComp[s].append((x-r, y-r, 2*r, 2*r))
        else:
            tache.parent.rectComp[s] = [(x-r, y-r, 2*r, 2*r)]
        

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
        boule(ctx, _x, y, r, 
              constantes.COUL_ELEVES[i][0], constantes.COUL_ELEVES[i][1],
              transparent = False)
        tache.parent.eleves[i].rect.append((_x -r , y - r, 2*r, 2*r))
        tache.parent.eleves[i].pts_caract.append((_x,y))
        

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
        if len(constantes.dicCompetences_prj_simple[eleve.parent.classe.typeEnseignement][s]) > 2:
            ctx.set_source_rgba (ICoulCompS[0],ICoulCompS[1],ICoulCompS[2],1.0)
        else:
            ctx.set_source_rgba (ICoulCompR[0],ICoulCompR[1],ICoulCompR[2],1.0)
        ctx.fill_preserve ()
        ctx.set_source_rgba (0,0,0,1)
        ctx.stroke ()
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
#        show_text_rect(ctx, str(n), (x-r, y-r, 2*r, 2*r))
#        tache.rect.append((x-r, y-r, 2*r, 2*r)) 
        if s in eleve.parent.rectComp.keys():
            eleve.parent.rectComp[s].append((x-r, y-r, 2*r, 2*r))
        else:
            eleve.parent.rectComp[s] = [(x-r, y-r, 2*r, 2*r)]
        
        eleve.pts_caract.append((x,y))
            

