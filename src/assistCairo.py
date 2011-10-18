#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
assistCairo.py
Fonctions d'assistance au dessin avec Cairo

Copyright (C) 2011  
@author: Cedrick FAURY
"""
import textwrap
from math import sqrt, pi

def show_text_rect(ctx, texte, x, y, w, h, va = 'c', ha = 'c', b = 0.2, orient = 'h'):
    """ Renvoie la taille de police et la position du texte
        pour qu'il rentre dans le rectangle
        x, y, w, h : position et dimensions du rectangle
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        b : écart du texte par rapport au bord (relativement aux dimension du rectangle)
        orient : orientation du texte ('h', 'v')
    """
#    print "show_text_rect", texte

    if orient == 'v':
        ctx.rotate(-pi/2)
        show_text_rect(ctx, texte, -y-h, x, h, w, va, ha, b)
        ctx.rotate(pi/2)
        return
    
    #
    # "réduction" du réctangle
    #
    x, y = x+w*b/2, y+h*b/2
    w, h = w*(1-b), h*(1-b)
 
    
    #
    # Estimation de l'encombrement du texte (pour une taille de police de 1)
    # 
    ctx.set_font_size(1)
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(texte)
    volumeTexte = 1.0*width*fheight

    ratioRect = 1.0*h/w
    W = sqrt(volumeTexte/ratioRect)
    H = ratioRect*W
    
    #
    # Découpage du texte
    #
    nLignes = max(1,int(width/W))
    wrap = len(texte)/nLignes
    lt = textwrap.wrap(texte, wrap)
    nLignes = len(lt)
    
    #
    # Calcul de la taille de police nécessaire pour que ça rentre
    #
    maxw = 0
    for t in lt:
        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
        maxw = max(maxw, width)
    hTotale = (fheight+fdescent)*nLignes
#    print "hTotale", hTotale
    fontSize = min(w/maxw, h/(hTotale))
#    print "fontSize", fontSize
    ctx.set_font_size(fontSize)
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    
    
    #
    # On dessine toutes les lignes de texte
    #
    l = 0
    dy = (h-(fheight+fdescent)*nLignes)/2
#    print "dy", dy
    
    for t in lt:
#        print "  ",t
        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
        xt, yt = x+xbearing+(w-width)/2, y-ybearing+fheight*l+dy+height/2
#        print "  ",xt, yt
        ctx.move_to(xt, yt)
        
        ctx.show_text(t)
        l += 1
    
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
    