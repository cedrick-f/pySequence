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
import cairo

def show_text_rect(ctx, texte, x, y, w, h, va = 'c', ha = 'c', b = 0.2, orient = 'h'):
    """ Renvoie la taille de police et la position du texte
        pour qu'il rentre dans le rectangle
        x, y, w, h : position et dimensions du rectangle
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        b : écart du texte par rapport au bord (relativement aux dimension du rectangle)
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
        if ha == 'c':
            ctx.move_to(xt, yt)
        elif ha == 'g':
            ctx.move_to(x, yt)
        
        ctx.show_text(t)
        l += 1
    
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
        ctx.set_source_rgb (coul[0], coul[1], coul[2])
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
    
def rectangle_plein(ctx, x, y, w, h, coulBord, coulInter):
    ctx.rectangle(x, y, w, h)
    ctx.set_source_rgba (coulInter[0], coulInter[1], coulInter[2], coulInter[3])
    ctx.fill_preserve ()
    ctx.set_source_rgb (coulBord[0], coulBord[1], coulBord[2])
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
    
    
    
    
    
    
    
    