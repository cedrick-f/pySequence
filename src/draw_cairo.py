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

## Copyright (C) 2012 Cédrick FAURY

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

@author: Cedrick
'''


import textwrap
from math import sqrt, pi, cos, sin
import cairo
import time

from widgets import getHoraireTxt

#
# Données pour le tracé
#

minFont = 0.008
maxFont = 0.1

LargeurTotale = 0.72414 # Pour faire du A4

font_family = "arial"



#def str2coord(str):
#    l = str.split(',')
#    return [eval(l[0]), eval(l[1])]
#
#def coord2str(xy):
#    return str(xy[0])+","+str(xy[1])
#
#def str2coul(str):
#    l = str.split(',')
#    return eval(l[0]), eval(l[1]), eval(l[2]), eval(l[3])
#
#def coul2str(rgba):
#    if len(rgba) == 3:
#        a = 1
#    else:
#        a = rgba[3]
#    return str(rgba[0])+","+str(rgba[1])+","+str(rgba[2])+","+str(a)



#def enregistrerConfigFiche(nomFichier):
#    config = ConfigParser.ConfigParser()
#
#    section = "General"
#    config.add_section(section)
#    config.set(section, "margeX", str(margeX))
#    config.set(section, "margeY", str(margeY))
#    config.set(section, "ecartX", str(ecartX))
#    config.set(section, "ecartY", str(ecartY))
#    
#    section = "Intitule de la sequence"
#    config.add_section(section)
#    config.set(section, "pos", coord2str(posIntitule))
#    config.set(section, "dim", coord2str(tailleIntitule))
#    config.set(section, "coulInt", coul2str(IcoulIntitule))
#    config.set(section, "coulBord", coul2str(BcoulIntitule))
#    
#    section = "Centre d'interet"
#    config.add_section(section)
#    config.set(section, "pos", coord2str(posCI))
#    config.set(section, "dim", coord2str(tailleCI))
#    config.set(section, "coulInt", coul2str(IcoulCI))
#    config.set(section, "coulBord", coul2str(BcoulCI))
#    
#    section = "Objectifs"
#    config.add_section(section)
#    config.set(section, "pos", coord2str(posObj))
#    config.set(section, "dim", coord2str(tailleObj))
#    config.set(section, "coulInt", coul2str(IcoulObj))
#    config.set(section, "coulBord", coul2str(BcoulObj))
#
#    section = "Prerequis"
#    config.add_section(section)
#    config.set(section, "pos", coord2str(posPre))
#    config.set(section, "dim", coord2str(taillePre))
#    config.set(section, "coulInt", coul2str(IcoulPre))
#    config.set(section, "coulBord", coul2str(BcoulPre))
#
#    section = "Zone d'organisation"
#    config.add_section(section)
#    config.set(section, "pos", coord2str(posZOrganis))
#    config.set(section, "dim", coord2str(tailleZOrganis))
#
#    section = "Zone de deroulement"
#    config.add_section(section)
#    config.set(section, "pos", coord2str(posZDeroul))
#
#    section = "Tableau systemes"
#    config.add_section(section)
#    config.set(section, "posY", str(posZSysteme[1]))
#    config.set(section, "col", str(wColSysteme))
#
#    section = "Tableau demarche"
#    config.add_section(section)
#    config.set(section, "posY", str(posZDemarche[1]))
#    config.set(section, "dimX", str(tailleZDemarche[0]))
#    
#    section = "Intitule des seances"
#    config.add_section(section)
#    config.set(section, "posX", str(posZIntSeances[0]))
#    config.set(section, "dimX", str(tailleZIntSeances[0]))
#    config.set(section, "haut", str(hIntSeance))
#
#    section = "Seances"
#    config.add_section(section)
#    config.set(section, "pos", coord2str(posZSeances))
#    for k, v in BCoulSeance.items():
#        config.set(section, "Bcoul"+k, coul2str(v))
#    for k, v in ICoulSeance.items():
#        config.set(section, "Icoul"+k, coul2str(v))
#        
#    config.write(open(nomFichier,'w'))
#    
#    
#    
#    
#    
#    
#def ouvrirConfigFiche(nomFichier):
##    print "ouvrirConfigFiche"
#    global posIntitule, tailleIntitule, IcoulIntitule, BcoulIntitule, \
#           posCI, tailleCI, IcoulCI, BcoulCI, \
#           posObj, tailleObj, IcoulObj, BcoulObj, \
#           posZOrganis, tailleZOrganis, \
#           posZDeroul, wColSysteme, hIntSeance, posZSeances, \
#           margeX, margeY, ecartX, ecartY
#           
#           
#    config = ConfigParser.ConfigParser()
#    config.read(nomFichier)
#    
#    section = "General"
#    margeX = eval(config.get(section,"margeX"))
#    margeY = eval(config.get(section,"margeY"))
#    ecartX = eval(config.get(section,"ecartX"))
#    ecartY = eval(config.get(section,"ecartY"))
#    
#    
#    section = "Intitule de la sequence"
#    posIntitule = str2coord(config.get(section,"pos"))
#    tailleIntitule = str2coord(config.get(section,"dim"))
#    IcoulIntitule = str2coul(config.get(section,"coulInt"))
#    BcoulIntitule = str2coul(config.get(section,"coulBord"))
#    
#    section = "Centre d'interet"
#    posCI = str2coord(config.get(section,"pos"))
#    tailleCI = str2coord(config.get(section,"dim"))
#    IcoulCI = str2coul(config.get(section,"coulInt"))
#    BcoulCI = str2coul(config.get(section,"coulBord"))
#    
#    section = "Objectifs"
#    posObj = str2coord(config.get(section,"pos"))
#    tailleObj = str2coord(config.get(section,"dim"))
#    IcoulObj = str2coul(config.get(section,"coulInt"))
#    BcoulObj = str2coul(config.get(section,"coulBord"))
#
#    section = "Prerequis"
#    posPre = str2coord(config.get(section,"pos"))
#    taillePre = str2coord(config.get(section,"dim"))
#    IcoulPre = str2coul(config.get(section,"coulInt"))
#    BcoulPre = str2coul(config.get(section,"coulBord"))
#    
#    section = "Zone d'organisation"
#    posZOrganis = str2coord(config.get(section,"pos"))
#    tailleZOrganis = str2coord(config.get(section,"dim"))
#    
#    section = "Zone de deroulement"
#    posZDeroul = str2coord(config.get(section,"pos"))
#
#    section = "Tableau systemes"
#    posZSysteme[1] = config.getfloat(section,"posY")
#    wColSysteme = config.getfloat(section,"col")
#
#    section = "Tableau demarche"
#    posZDemarche[1] = config.getfloat(section,"posY")
#    tailleZDemarche[0] = config.getfloat(section,"dimX")
#    
#    section = "Intitule des seances"
#    posZIntSeances[0] = config.getfloat(section,"posX")
#    tailleZIntSeances[0] = config.getfloat(section,"dimX")
#    hIntSeance = config.getfloat(section,"haut")
#    
#    section = "Seances"
#    posZSeances = str2coord(config.get(section,"pos"))
#    for k in BCoulSeance.keys():
#        BCoulSeance[k] = str2coul(config.get(section, "Bcoul"+k))
#    for k in ICoulSeance.keys():
#        ICoulSeance[k] = str2coul(config.get(section, "Icoul"+k))
#    
    

    
    
def getPts(lst_rect):
    """ Renvoie la liste des points Haut-Gauche des rectangles contenus dans <lst_rect>
    """
    lst = []
    for rect in lst_rect:
        lst.append(rect[:2])
    return lst
    


def permut(liste):
    l = []
    for a in liste[1:]:
        l.append(a)
    l.append(liste[0])
    return l
    
    



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
                    lt[i:j] = textwrap.wrap(lt[i], max(1,int(1.0*len(lt)*w/width)))
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
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = True,
                   bordure = None):
    """ Affiche un texte en adaptant la taille de police et sa position
        pour qu'il rentre dans le rectangle
        x, y, w, h : position et dimensions du rectangle
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        b : écart mini du texte par rapport au bord (relativement aux dimensionx du rectangle)
        orient : orientation du texte ('h', 'v')
        max_font : taille maxi de la font
        min_font : le texte peut être tronqué (1 ligne)
    """
#    print "show_text_rect", texte, rect

    if texte == "":
        return 0, 0, 0
    
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
        fontSize, maxw, r = show_text_rect(ctx, texte, r, va, ha, b, fontsizeMinMax = fontsizeMinMax, fontsizePref = fontsizePref,
                       wrap = wrap, couper = couper, bordure = bordure)
        ctx.rotate(pi/2)
        return fontSize, maxw, r

    
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
    fascent, fdescent = ctx.font_extents()[:2]
    hl = fascent+fdescent
    
    # On vérifie dans le cache qu'on n'a pas déja fait le boulot
    calculer = False
    if texte in CACHE.keys():
        www, hhh, ttt, fff, mmm = CACHE[texte]
        if www == w and hhh == h:
            lt, fontSize, maxw = ttt, fff, mmm
        else:
            
            calculer = True
    else:
#        print " pas cache",texte
        calculer = True
    
    if calculer:
        lt, fontSize, maxw = wrapp(ctx, texte, w, h, wrap, couper)
        CACHE[texte] = (w, h, lt, fontSize, maxw)
    nLignes = len(lt)
    
    
#    width = ctx.text_extents(texte)[2]
#
#    ratioRect = 1.0*w/h
#    W = sqrt(1.0*width*hl*ratioRect)
##    H = W/ratioRect
#    
#    #
#    # Découpage du texte
#    #
#    i = 0
##    tps = time.time()
#    if wrap:
#        continuer = True
#        
#        wrap1 = 0
#        st = texte.split("\n")
#        for l in st:
#            wrap1 = max(wrap1, len(l))
#            
##        print len(texte), texte
#        wrap = min(wrap1, int(len(texte)*W/width)*2)
##        print "   wrap initial :", wrap, "(brut :",int(len(texte)*W/width),")"
#        
#        ancienWrap = wrap
#        ancienFontSize = 0
#        ancienLt = []
#        ancienMaxw = 0
#        i = 0
#        while continuer:
#            lt = []
#            
#            # On découpe le texte
#            i += 1
#            for l in texte.split("\n"):
#                lt.extend(textwrap.wrap(l, wrap, break_long_words = couper))
#                
#            # On mémorise la longueur de la plus longue ligne 
#            #    (en caractères et en unité Cairo)
#            maxw = maxl = 0
#            for t in lt:
#                maxw = max(maxw, ctx.text_extents(t)[2])
#                maxl = max(maxl, len(t))
#            
#            # On calcule la taille de police nécessaire pour que ça rentre
#            fontSize = min(w/maxw, h/(hl*len(lt)))  
#            
#            # On calcul le rapport des rapports h/w
#            rapport = maxw / (hl*len(lt)) / ratioRect
#            if rapport <= 1:  # on a passé le cap ...
#                continuer = False
#                if fontSize <= ancienFontSize:
#                    wrap = ancienWrap
#                    lt = ancienLt
#                    maxw = ancienMaxw
#                    fontSize = ancienFontSize
#
#            else:
#                ancienWrap = wrap
#                wrap = min(wrap-1, maxl-1)
#                if wrap <= 1:# or (maxw == ancienMaxw and wrap < maxl) :
#                    continuer = False
#                    
#                ancienFontSize = fontSize
#                ancienLt = lt
#                ancienMaxw = maxw
#            
#        nLignes = len(lt)
#        
#    else:
#        nLignes = 1
#        lt = [texte]
#        maxw = ctx.text_extents(texte)[2]
#        fontSize = min(w/maxw, h/(hl*nLignes))
        
#        CACHE[texte] = (w,h,lt)    
    
    hTotale = hl*nLignes
    
    #
    # "réduction" du réctangle
    #
    ctx.set_font_size(fontSize)
    ecart = min(w*b/2, h*b/2)
    ecart = min(ecart, ctx.font_extents()[2])
    if va == 'c':
        x, y = x+ecart, y+ecart
    elif va == 'h':
        x, y = x+ecart, y
    elif va == 'b':
        x, y = x+ecart, y+2*ecart
    w, h = w-2*ecart, h-2*ecart
    fontSize = min(w/maxw, h/(hTotale))
    
    if fontSize > fontsizeMinMax[1]:
        # Réglage taille selon taille préférée
        if fontsizePref > 0:
            fontSize = max(fontsizeMinMax[1] * fontsizePref/100, fontsizeMinMax[0])
        else:
            fontSize = fontsizeMinMax[1]
        wc, yh = show_text_rect_fix(ctx, texte, x, y, w, h, fontSize, 100, va = va, ha = ha, bordure = bordure, wrap = wrap)
        return fontSize, wc, yh
    
    fontSize = min(fontSize, fontsizeMinMax[1])
#    print "fontSize", fontSize
    
    if fontSize < fontsizeMinMax[0]:
        wc, yh = show_text_rect_fix(ctx, texte, x, y, w, h, fontsizeMinMax[0], nLignesMaxi, va, ha, bordure = bordure, wrap = wrap)
        return fontSize, wc, yh
            
#    print lt, nLignes
    ctx.set_font_size(fontSize)
    
    # 2 ème tour
#    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    maxw = 0
    for t in lt:
        width = ctx.text_extents(t)[2]
        maxw = max(maxw, width)
    fontSize = min(fontSize, fontSize*w/maxw)
    
    # Réglage taille selon taille préférée
    if fontsizePref > 0:
        fontSize = max(fontSize * fontsizePref/100, fontsizeMinMax[0])
#    print "fontSize 2", fontSize
    
#    print "fontSize", fontSize

    ctx.set_font_size(fontSize)
    wc, yh = show_lignes(ctx, lt, x, y, w, h, ha, va, bordure = bordure)
    
    return fontSize, wc, yh


#def show_text_rect2(ctx, texte, rect, va = 'c', ha = 'c', b = 0.4, orient = 'h', 
#                   fontsize = (-1, -1), wrap = True):
#    """ Affiche un texte en adaptant la taille de police et sa position
#        pour qu'il rentre dans le rectangle
#        rect = (x, y, w, h) : position et dimensions du rectangle
#        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
#        b : écart mini du texte par rapport au bord (en fraction de caractère)
#        orient : orientation du texte ('h', 'v')
#        fontsize : taille maxi/mini de la font (-1 = auto)
#    """
##    print "show_text_rect", texte
#
#    print "show_text_rect", texte
#    
#    if texte == "":
#        return
#    
#    x, y, w, h = rect
#    
#    fontsize = [fontsize[0], fontsize[1]]
#    if fontsize[0] == -1:
#        fontsize = [minFont, fontsize[1]]
#    if fontsize[1] == -1:
#        fontsize = [fontsize[0], 0.1]
#    
#    if orient == 'v':
#        ctx.rotate(-pi/2)
#        r = (-y-h, x, h, w)
#        show_text_rect(ctx, texte, r, va, ha, b, fontsize = fontsize, wrap = wrap)
#        ctx.rotate(pi/2)
#        return
#    
#    def ajuster_text_rect(txt, _w, _h, fsize):
#        print "   ajuster_text_rect", txt, fsize
#        
#        ctx.set_font_size(fsize)
#        fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
#        
#        dx = ctx.text_extents("a")[2] * b
#        
#        #
#        # Découpage du texte
#        #
#        continu = True
#        wr = 0
#        for l in txt.split("\n"):
#            wr = max(wr, len(l))
#        i = 0
##        trop = False
#        while continu:
#            i += 1
#            # On fait une découpe à "wrap" ...
#            lt = []
#            for l in txt.split("\n"):
#                lt.extend(textwrap.wrap(l, wr))
#            
#            # On teste si ça rentre ...
#            maxw = 0
#            for t in lt:
#                xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
#                maxw = max(maxw, width+2*dx)
#        
#            if maxw <= _w: # Ca rentre !
#                continu = False
#            else: # Ca ne rentre pas --> on coupe plus raz.
#                wr += -1
##                if wr <= 0:
##                    trop = True
##                    continu == False
#        
#        #
#        # Calcul du nombre de lignes nécessaires
#        #
#        print "    ",fascent , fdescent
#        hf = fascent + fdescent
#        Nlignes = int(_h // hf)
#        rapport = hf*len(lt) / _h
#        print "    ", len(lt), "*", hf, "/", _h, "=", rapport
#        print "    ", Nlignes, fsize/hf
#        
#
##        if rapport > 1:
##            Nlignes = max(len(lt), Nlignes + 1)
#        #
#        # Tronquage du texte
#        #
#        tronque = False
#        if len(lt) > Nlignes:
#            tronque = True
#            dl = lt[Nlignes-1]
#            continu = True
#            while continu:
#    #            print "   ", dl
#                width = ctx.text_extents(dl+" ...")[2]
#                if width <= w:
#                    continu = False
#                else:
#                    dll = dl.split()
#                    if len(dll) > 1:
#                        dl = " ".join(dll[:-1])
#                    else:
#                        continu = False
#                    
#            lt[Nlignes-1] = dl + " ..."
#            
#        lt = lt[:Nlignes]
#    
#
#        return lt, tronque, rapport, dx, hf*b
#    
#    continuer = True
#    size = min(fontsize[1], min(w, h))
#    old_size = size
#    c = 0
#    while continuer:
#        lst_lgn, tronq, rapp, dx, dy = ajuster_text_rect(texte, w, h, size)
#        c += 1
#        if abs(rapp - 1) < 0.01 or abs(size - fontsize[0]) < 0.001 or c>10:
#            continuer = False
#        else:
##            old_old_size = old_size
#            old_size = size
##            size = max(fontsize[0], size/rapp)
#            size = size/sqrt(rapp)
##            if size == fontsize[0]:
##                continuer = False
##            print old_old_size, old_size, size
##            if abs(old_old_size - size) < 0.001:
###                size = (size+old_size)/2
##                size = min(size,old_size)
##                continuer = False
#            
#    ctx.set_font_size(size)
#    
#    show_lignes(ctx, lst_lgn, x+dx, y+dy, w-2*dx, h-2*dy, ha, va)
#    
#    return size


def show_text_rect_fix(ctx, texte, x, y, w, h, fontSize, Nlignes, va = 'c', ha = 'c', bordure = None, wrap = True):#, outPosMax = False):
    """ Affiche un texte en tronquant sa longueur
        pour qu'il rentre dans le rectangle
        x, y, w, h : position et dimensions du rectangle
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        
        Si outFont : Renvoie la position la plus extrème à droite (pour éventuellement écrire une suite au texte)
        Sinon : Renvoie le point caractéristique du rectangle encadrant
    """
#    if texte == "Th 10":
#        print "show_text_rect_fix", fontSize, Nlignes, texte

    if texte == "":
        return 0, 0
         
    ctx.set_font_size(fontSize)

    #
    # Découpage du texte
    #
    if wrap:
        # Longueur maxi des lignes (nbr de caractères)
        wmax = 0
        for l in texte.split("\n"):
            wmax = max(wmax, len(l))
        i = 0
        
        continuer = len(texte) > 0
        while continuer:
            i += 1
            # On fait une découpe à "wmax" ...
            lt = []
            for l in texte.split("\n"):
                if wmax > 0:
                    lt.extend(textwrap.wrap(l, wmax))
                else:
                    lt.extend(l)
            
            # On teste si ça rentre ...
            maxw = 0
            for t in lt:
                width = ctx.text_extents(t)[2]
                maxw = max(maxw, width)
        
            if maxw <= w: # Ca rentre !
                continuer = False
            else: # Ca ne rentre pas --> on coupe plus ras.
                wmax += -1
    else:
        lt = [texte]
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
    
#    show_lignes(ctx, lt, x, y, w, h, ha, va)
    
#    
#    if outPosMax: 
    return show_lignes(ctx, lt, x, y, w, h, ha, va)
#    else:
#        return x, y
    
     
   




def show_lignes(ctx, lignes, x, y, w, h, ha, va, bordure = None):
    """ Affiche une série de lignes de texte
        Renvoie la position la plus extrème à droite (pour éventuellement écrire une suite au texte)
    """
    fascent, fdescent, fheight = ctx.font_extents()[:3]
    hl = fascent+fdescent
    # pour centrer verticalement
    
    if va == 'c':
        dy = (h-hl*len(lignes))/2
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
        elif ha == 'd':
            xt = x+xbearing+w-width
        
        yt = y + hl*l - fdescent + fheight + dy

        ctx.move_to(xt, yt)
        
        if bordure == None:
    #        print t
            ctx.show_text(t)
        else:
            ctx.text_path(t)
            ctx.fill_preserve()
            ctx.set_source_rgb(bordure[0], bordure[1], bordure[2])
            ctx.set_line_width(fheight/30)
           
        posmax = max(posmax, xt + width)
    
    ctx.stroke()

    return posmax, y+dy




BcoulPos = (0.1, 0.1, 0.25, 1)
AcoulPos = (1, 0.4, 0, 1)
IcoulPos = (0.8, 0.8, 1, 0.85)
fontPos = 0.014
######################################################################################  
def DrawPeriodes(ctx, rect, pos = None, periodes = [[u"Année", 5]], projets = {}, tailleTypeEns = 0):
#    print "DrawPeriodes", pos
#    print "   ", periodes, periodes_prj
    ctx.set_line_width (0.001)
#    if origine:
#        x = 0
#        y = 0
#        wt = 0.04*7
#        ht = 0.04
#    else:
    x = rect[0]# + ecartX
    y = rect[1]
    wt = rect[2]# - ecartX
    ht = rect[3]
    
    # Toutes le périodes de projet
    periodes_prj = [p.periode for p in projets.values()]
    
    # Les noms des projets par période
    noms_prj = {}
    for n, p in projets.items():
        for per in p.periode:
            noms_prj[per] = n
    
    
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
    
    # Ecart entre les cases
    dx = 0.02 * wt
    # Hauteur des cases
    h = ht/2-2*dx
    
    # Les rectangles à cliquer
    rect = []
    
    # Les différentes positions des cases
    posc = []

    # Nombre d'années
    na = len(periodes)
    
    # Nombre total de périodes
    nt = 0
    for a in periodes:
        nt += a[1]
        
    # Largeur d'une case "simple"
    w = (wt-(nt+na)*dx)/nt
    
#    # Largeur d'une année
#    wi = (wt+dx)/len(periodes) - dx
    
    pa = 0
    
    # Abscisses des cases "simples"
    xcs = []
    
    # Curseur "année"
    xi = x
    for i, (an, np) in enumerate(periodes):
        # Largeur de l'année
        wa = np*w + (np+1) * dx
        
        # Nom de l'année
        annee = an.split("_")
        ctx.set_font_size(fontPos)
        w0 = ctx.text_extents(annee[0])[2]
#        xi = x + wi/2 + (dx+wi)*i
        if len(annee) > 1:
            ctx.set_font_size(fontPos*0.9)
            w1 = ctx.text_extents(annee[1])[2]
            show_text_rect_fix(ctx, annee[0], xi+wa/2-(w0+w1)/2, y, w0, ht*2/3, fontPos, 1)
            ctx.stroke ()
            show_text_rect_fix(ctx, annee[1], xi+wa/2-(w0+w1)/2 + w0 +0.01, y, w1, ht/3, fontPos*0.9, 1, ha = 'c')
            ctx.stroke ()
        else:
            show_text_rect_fix(ctx, annee[0], xi+wa/2-w0/2, y, w0, ht*2/3, fontPos, 1)
            ctx.stroke ()
        
        for c in range(np):
            pa += 1
            if pa in noms_prj.keys():
                n = noms_prj[pa]
            else:
                n = ""
            xcs.append((xi + c*(w+dx) + dx, pos == pa-1, i, n))
            
        xi += np*w + (np+1)*dx
        
    # Liste des positions qui fusionnent avec leur position précédente
    lstGrp = []
    for periode_prj in periodes_prj:  
        lstGrp.extend(range(periode_prj[0]+1, periode_prj[-1]+1))
#    print lstGrp
    
    for p in reversed(sorted(lstGrp)):
        del xcs[p-1]
        

    for p, xc in enumerate(xcs):
        
        if p < len(xcs)-1:
            w = xcs[p+1][0] - xc[0] - dx
            if xcs[p+1][2] != xc[2]:
                w -= dx
        else:
            w = x+wt - xc[0] - dx
        

        ctx.rectangle (xc[0], y+ht/2+dx, w, h)
        rect.append((xc[0], y+ht/2+dx, w, h))
        if xc[1]:
            ctx.set_source_rgba (AcoulPos[0], AcoulPos[1], AcoulPos[2], AcoulPos[3])
        else:
            ctx.set_source_rgba (IcoulPos[0], IcoulPos[1], IcoulPos[2], IcoulPos[3])
        ctx.fill_preserve ()
        ctx.set_source_rgba (BcoulPos[0], BcoulPos[1], BcoulPos[2], BcoulPos[3])
        ctx.stroke ()    
        
        if xc[3] != "":
            show_text_rect(ctx, xc[3], 
                           rect[-1], ha = 'c', b = 0.2, wrap = False, couper = False)
            ctx.stroke ()
            
    return rect




            
def curve_rect_titre(ctx, titre, rect, coul_bord, coul_int, taille_font = 0.01, rayon = 0.02, epaiss = 0.002):
    ctx.set_line_width(epaiss)
    x0, y0, rect_width, rect_height = rect
    
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(taille_font)
    fheight = ctx.font_extents()[2]
    xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(titre)
      
    c = curve_rect(ctx, x0, y0, rect_width, rect_height, rayon, 
               ouverture = min(width + fheight, rect_width-2*rayon))
    
    ctx.set_source_rgba (coul_int[0], coul_int[1], coul_int[2], coul_int[3])
    ctx.fill_preserve ()
    ctx.set_source_rgba (coul_bord[0], coul_bord[1], coul_bord[2], coul_bord[3])
    ctx.stroke ()
    
    xc = x0 + rayon
    mask = cairo.LinearGradient (xc, y0, xc, y0 - height)
    mask.add_color_stop_rgba (1, 1, 1, 1, 0)
    mask.add_color_stop_rgba (0, coul_int[0], coul_int[1], coul_int[2], coul_int[3])
    ctx.rectangle (xc, y0 - height, min(width + fheight, rect_width-2*rayon), height)
    ctx.set_source (mask) 
    ctx.fill ()
    
    xc = x0 + rayon + fheight/2
    yc = y0 + ybearing - fheight/3#height
    
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



    
def tableauV(ctx, titres, x, y, w, ht, hl, nlignes = 0, va = 'c', ha = 'c', orient = 'h', coul = (0.9,0.9,0.9)):
    
    rect = []
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
        if orient == 'h':
            rect.append((_x, y, wc, ht))
        else:
            rect.append((-y, _x, wc, ht))
        ctx.stroke ()
        _x += wc
    
    _x = x
    _y = y+ht
    for l in range(nlignes):
        ctx.rectangle(_x, _y, wc, hl)
        _x += wc
        _y += hl
        
    ctx.stroke ()
    return rect
    
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
        ctx.set_source_rgba (col[0][0], col[0][1], col[0][2], col[0][3])
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
    """ Dessine un tableau horizontal :
        ------------------------------------------------------------------
        |    titre    |    contenu col1    |    contenu col2    |    ...
        ------------------------------------------------------------------
        |    titre    |    contenu col1    |    contenu col2    |    ...
        ------------------------------------------------------------------
        |     ...     |      ...           |      ...           |    ...
        
        hl : liste des hauteurs de lignes
        nCol : nombre de colonnes
    """
#    hc = h/len(titres)
    _y = y
    _coul = ctx.get_source().get_rgba()
#    print "tableauH", _coul
    for i, titre in enumerate(titres):
        ctitre = titre.rstrip("1234567890.")
#        print "    ",ctitre
        
        ctx.rectangle(x, _y, wt, hl[i])
        if type(coul) == dict:# and len(ctitre) > 0:
            col = coul[ctitre]
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
#    print
    for c in contenu:
#        print "    ", c
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
    
def boule(ctx, x, y, r, 
          color0 = (1, 1, 1, 1), color1 = (0, 0, 0, 1), 
          transparent = True):
    pat = cairo.RadialGradient (x-r/2, y-r/2, r/4,
                                x-r/3, y-r/3, 3*r/2)
    if transparent:
        alpha0 = color0[3]
        alpha1 = color1[3]
    else:
        alpha0 = 1
        alpha1 = 1
    pat.add_color_stop_rgba (0, color0[0], color0[1], color0[2], alpha0)
    pat.add_color_stop_rgba (1, color1[0], color1[1], color1[2], alpha1)
    ctx.set_source (pat)
    ctx.arc (x, y, r, 0, 2*pi)
    ctx.fill ()
      
def barreH(ctx, x, y, w, r, a, e, coul0, coul1, coul):
    """ Dessine une barre horizontale de poucentage/progression
        x, y : position
        w : longueur maxi (100%)
        r : taux
        e = épaisseur
        a : acceptable (a==True : coul0  - a==False = coul1)
    """
    src = ctx.get_source()
    
    if a:
        coulEtat = coul1
    else:
        coulEtat = coul0
        
    ctx.set_source_rgba(coul[0],  coul[1],  coul[2],  coul[3])
    ctx.rectangle (x, y-e/2, w*r, e)
    ctx.fill_preserve ()    
    ctx.set_source_rgba(0.4,  0.4,  0.4,  1)
    ctx.set_line_width(0.001)
    ctx.stroke()
    
    ctx.set_source_rgba(coulEtat[0], coulEtat[1], coulEtat[2], coulEtat[3])
    ctx.rectangle (x+w*r-e, y-e/2, e, e)
    ctx.fill ()
    
    
    
    ctx.set_source(src)
    
    
#    src = ctx.get_source()
#    pat = cairo.LinearGradient (x, y-e/2,  x, y+e/2)
#    
#    if r > 0.5:
#        pat.add_color_stop_rgba (0.0, coul1[0], coul1[1], coul1[2], coul1[3])
#        pat.add_color_stop_rgba (0.5, coul[0],  coul[1],  coul[2],  coul[3])
#        pat.add_color_stop_rgba (1.0, coul1[0], coul1[1], coul1[2], coul1[3])
#    else:
#        pat.add_color_stop_rgba (0.0, coul0[0], coul0[1], coul0[2], coul0[3])
#        pat.add_color_stop_rgba (0.5, coul[0],  coul[1],  coul[2],  coul[3])
#        pat.add_color_stop_rgba (1.0, coul0[0], coul0[1], coul0[2], coul0[3])
#    
#    ctx.rectangle (x,y-e/2,w*r,e)
#    ctx.set_source (pat)
#    ctx.fill ()
#    ctx.set_source(src)
    
    
        
def fleche_verticale(ctx, x, y, h, e, coul):
    ctx.set_source_rgba (coul[0], coul[1], coul[2], coul[3])
    he = min(e/2, h/3)
    ctx.move_to(x-e/2, y)
    ctx.line_to(x-e/2, y+h-he)
    ctx.line_to(x, y+h)
    ctx.line_to(x+e/2, y+h-he)
    ctx.line_to(x+e/2, y)
    ctx.close_path ()
    ctx.fill_preserve ()    
    ctx.set_source_rgba(0.4,  0.4,  0.4,  1)
    ctx.set_line_width(0.0006)
    ctx.stroke ()
    

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
    
    
    
def liste_code_texte(ctx, lstCodes, lstTexte, x, y, w, h, e, b = 0.4, gras = None, lstCoul = None, va = 'h'):
    lstRect = []
    no = len(lstCodes)
    maxFontSize = 0.012
    if no > 0:
        hl = h/no
        wt = 0
        #
        # Calcul de la largeur maxi des codes
        #
        ctx.set_font_size(maxFontSize)
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
        for i, t in enumerate(lstCodes):
            if t.strip() != "":
                width = ctx.text_extents(t)[2]
                wt = max(wt, width)
                
        #
        # Textes
        #
        ly = []
        for i, t in enumerate(lstCodes):
            if lstTexte[i].strip() != "":
                if i == gras:
                    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_BOLD)
                else:
                    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                          cairo.FONT_WEIGHT_NORMAL)
                if lstCoul != None:
                    ctx.set_source_rgb (lstCoul[i][0], lstCoul[i][1], lstCoul[i][2])
#                else:
#                    ctx.set_source_rgb (0, 0, 0)
                    
                fm, wc, yh = show_text_rect(ctx, lstTexte[i], 
                               (x+wt+2*e, y+i*hl, 
                                w-wt-3*e, hl), b = b, ha = 'g', va = 'c', fontsizeMinMax = (-1, maxFontSize))
                ly.append(yh)
                
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
    
    
        #
        # Codes
        #
        ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
        for i, t in enumerate(lstCodes):
            if t.strip() != "":
                if lstCoul != None:
                    ctx.set_source_rgb (lstCoul[i][0], lstCoul[i][1], lstCoul[i][2])
#                else:
#                    ctx.set_source_rgb (0, 0, 0)
                    
                show_text_rect(ctx, t, 
                               (x+e, ly[i], w/6-e, hl), #y+i*hl, 
                               b = 0.2, ha = 'g', va = va, fontsizeMinMax = (-1, maxFontSize), wrap = False)
        
    
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
    
def get_apercu(doc, mult = 3):
    """ Renvoi un apercu du document <doc>
        sous la forme d'une cairo.ImageSurface
    
    """
    imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  210*mult, 297*mult)#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
    ctx = cairo.Context(imagesurface)
    ctx.scale(297*mult, 297*mult) 
    doc.draw.Draw(ctx, doc)
    return imagesurface



##########################################################################################
#
#  Un système de "cache" pour les textes wrappés
#
##########################################################################################
class maxdict(dict):
    """
    from Matplotlib.cbook :
    A dictionary with a maximum size; this doesn't override all the
    relevant methods to contrain size, just setitem, so use with
    caution
    """
    def __init__(self, maxsize):
        dict.__init__(self)
        self.maxsize = maxsize
        self._killkeys = []
    def __setitem__(self, k, v):
        if k not in self:
            if len(self)>=self.maxsize:
                del self[self._killkeys[0]]
                del self._killkeys[0]
            self._killkeys.append(k)
        dict.__setitem__(self, k, v)

CACHE = maxdict(500)


#import collections
#import functools

#class memoized(object):
#   '''Decorator. Caches a function's return value each time it is called.
#   If called later with the same arguments, the cached value is returned
#   (not reevaluated).
#   '''
#   def __init__(self, func):
#      self.func = func
#      self.cache = {}
#   def __call__(self, *args):
#      if not isinstance(args, collections.Hashable):
#         # uncacheable. a list, for instance.
#         # better to not cache than blow up.
#         return self.func(*args)
#      if args in self.cache:
#         return self.cache[args]
#      else:
#         value = self.func(*args)
#         self.cache[args] = value
#         return value
#   def __repr__(self):
#      '''Return the function's docstring.'''
#      return self.func.__doc__
#   def __get__(self, obj, objtype):
#      '''Support instance methods.'''
#      return functools.partial(self.__call__, obj)
#
#class memoize(dict):
#    def __init__(self, func):
#        self.func = func
#
#    def __call__(self, *args):
#        return self[args]
#
#    def __missing__(self, key):
#        result = self[key] = self.func(*key)
#        return result
##########################################################################################
#
#  Un système de "cache" pour les textes wrappés
#
##########################################################################################
#@memoize
def wrapp(ctx, texte, w, h, wrap = True, couper = True):
    """ Renvoie la liste des lignes et la taille de police et la longueur de la plus longue ligne
        pour que <texte> rentre dnas le rectangle (w,h)
        Options :
            wrap = False : le texte reste sur une ligne
            couper = False : les mots ne sont jamais coupés
            
    """
#    print "wrapp", texte, w, h
    #
    # Estimation de l'encombrement du texte (pour une taille de police de 1)
    # 
    ctx.set_font_size(1.0)
    fascent, fdescent = ctx.font_extents()[:2]
    hl = fascent+fdescent
    
    #
    # Découpage du texte
    #
    i = 0
#    tps = time.time()
    if wrap:
        width = ctx.text_extents(texte)[2]
        ratioRect = 1.0*w/h
        W = sqrt(1.0*width*hl*ratioRect)
        
        continuer = True
        
        wrap1 = 0
        st = texte.split("\n")
        for l in st:
            wrap1 = max(wrap1, len(l))
        
#        print len(texte), texte
        wrap = min(wrap1, max(1,int(len(texte)*W/width)*2))
#        print "   wrap initial :", wrap, "(brut :",int(len(texte)*W/width),")"
        
        ancienWrap = wrap
        ancienFontSize = 0
        ancienLt = []
        ancienMaxw = 0
        i = 0
        while continuer:
            lt = []
            
            # On découpe le texte
            i += 1
            for l in texte.split("\n"):
                lt.extend(textwrap.wrap(l, wrap, break_long_words = couper))
                
            # On mémorise la longueur de la plus longue ligne 
            #    (en caractères et en unité Cairo)
            maxw = maxl = 0
            for t in lt:
                maxw = max(maxw, ctx.text_extents(t)[2])
                maxl = max(maxl, len(t))
            
            # On calcule la taille de police nécessaire pour que ça rentre
            fontSize = min(w/maxw, h/(hl*len(lt)))  
            
            # On calcul le rapport des rapports h/w
            rapport = maxw / (hl*len(lt)) / ratioRect
            if rapport <= 1:  # on a passé le cap ...
                continuer = False
                if fontSize <= ancienFontSize:
                    wrap = ancienWrap
                    lt = ancienLt
                    maxw = ancienMaxw
                    fontSize = ancienFontSize

            else:
                ancienWrap = wrap
                wrap = min(wrap-1, maxl-1)
                if wrap <= 1:# or (maxw == ancienMaxw and wrap < maxl) :
                    continuer = False
                    
                ancienFontSize = fontSize
                ancienLt = lt
                ancienMaxw = maxw
            
        nLignes = len(lt)
        
    else:
        nLignes = 1
        lt = [texte]
        maxw = ctx.text_extents(texte)[2]
        fontSize = min(w/maxw, h/hl)
        
    return lt, fontSize, maxw





#def testRapport(ctx):
#    f = open("testRapport.txt", 'w')
#    for i in drange(0.008, 0.1, 0.0001):
#        ctx.set_font_size(i)
#        fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
#        f.write(str(i)+ " " + str(fascent+fdescent)+"\n")
#    f.close()
        
        
        
        
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
    
