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
##
## pySéquence : aide à la construction
## de Séquences et Progressions pédagogiques
## et à la validation de Projets

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

"""
Module ``draw_cairo``
*********************

Fonctionnalités avancées de dessin avec cairo

"""


import textwrap
from math import sqrt, pi, cos, sin
import os
import tempfile
import cairo
import time
try:
    import constantes
except:
    pass

## Pour afficher des images

import wx

from widgets import getHoraireTxt



                                     
                                     
#
# Coefficient de multiplication global
#
COEF = 1000.0

#
# Données pour le tracé
#

minFont = 0.008 * COEF
maxFont = 0.1 * COEF

LargeurTotale = 0.72414 * COEF# Pour faire du A4

font_family = "sans-serif"##"Purisa"#"DejaVu Sans Mono"#"arial"#
    
def getPts(lst_rect):
    """Renvoie la liste des points Haut-Gauche des rectangles contenus dans <lst_rect>
    """
    lst = []
    for rect in lst_rect:
        lst.append(rect[:2])
    return lst
    


def permut(liste):
    u""" Permutation circulaire d'une liste
         <<<
    """
    return liste[1:]+liste[:1]
#     l = []
#     for a in liste[1:]:
#         l.append(a)
#     l.append(liste[0])
#     return l
    
    



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
   
def reduire_rect(x, y, w, h, f, b):
    """ Réduction d'un rectangle : suppression de la bordure
        :f: hauteur de la police
        :b: coefficient de bordure
        
        Renvoie :
            rectangle réduit
    """
    ecart = f * b
    x += ecart
    y += ecart
    w -= 2*ecart
    h -= 2*ecart
    return x, y, w, h
    

def calcul_hauteur(fheight, le, nl):
    """ Calcul la hauteur effective d'un texte
        :fheight: hauteur de la police
        :le: coefficient d'inter-ligne
        :nl: nombre de lignes du texte
    """
    return fheight*nl + fheight*(le-1.0)*(nl-1)



def calcul_largeur(ctx, lt):
    """ Calcul la largeur effective d'un texte
        :lt: lignes du texte
    """
    return max([ctx.text_extents(t)[2] for t in lt])



def show_text_rect(ctx, texte, rect, \
                   va = 'c', ha = 'c', le = 0.8, pe = 1.0, \
                   b = 0.4, orient = 'h', \
                   fontsizeMinMax = (-1, -1), fontsizePref = -1, wrap = True, couper = True, 
                   coulBord = None, tracer = True, ext = "...", debug = False):
    """ Affiche un texte en adaptant la taille de police et sa position
        pour qu'il rentre dans le rectangle
        x, y, w, h : position et dimensions du rectangle
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        b : écart mini du texte par rapport au bord (relativement aux dimensionx du rectangle)
        orient : orientation du texte ('h', 'v')
        max_font : taille maxi de la font
        min_font : le texte peut être tronqué (1 ligne)
        
        le, pe : coefficient d'inter-ligne et inter-paragraphe
        
        Retourne : 
            Taille de police, 
            Rectangle "effectif" (encadrant le texte au plus près)
    """
    #texte[:3] ==u'Ést'
    if debug:
        print("show_text_rect", texte[:20], rect)

    if texte == "":
        return 0, rect
    
    x, y, w, h = rect
    
    #
    #    Retournement Horizontal >> Vertical
    #
    if orient == 'v':
        ctx.rotate(-pi/2)
        r = (-y-h, x, h, w)
        fontSize, r = show_text_rect(ctx, texte, r, va, ha, le, pe, 
                                           b, fontsizeMinMax = fontsizeMinMax, fontsizePref = fontsizePref,
                                           wrap = wrap, couper = couper, coulBord = coulBord, tracer = tracer)
        ctx.rotate(pi/2)
        return fontSize, r
    
    
    
    # Intervalle de taille de font
    fontsizeMinMax = [fontsizeMinMax[0], fontsizeMinMax[1]]
    if fontsizeMinMax[0] == -1:
        fontsizeMinMax = [minFont, fontsizeMinMax[1]]
    if fontsizeMinMax[1] == -1:
        fontsizeMinMax = [fontsizeMinMax[0], maxFont]
        
    if debug: print("   fontsizeMinMax :", fontsizeMinMax)
    
    ctx.set_font_size(fontsizeMinMax[0])
    fheight = ctx.font_extents()[2]
    hf = fheight * le
#     fontsizeMinMax[0] = min(fontsizeMinMax[0], fontsizeMinMax[0]*(h/hf))
    nLignesMaxi = max(1, h // hf)

    fontsizeMin, fontsizeMax = fontsizeMinMax
    
    
    
    
    #
    # Calcul ...
    #
    lt, fontSize, wh = ajuster_texte(ctx, texte, w, h, 
                                     le, pe, b, 
                                     wrap, couper, debug = debug)
    if lt == []:
        return 0, (x, y, 0,0)
    if debug: print("   fontSize 1:", fontSize, "H", wh[1])
    W, H = wh
    
    
    
    
    #
    # Vérification que la taille de la police est dans l'intervale
    #
    if fontSize > fontsizeMax:
        if debug: print("   fontSize maxi !", fontSize, fontsizeMax, texte)
        # Réglage taille selon taille préférée
        if fontsizePref > 0:
            fontSize = max(fontsizeMax * fontsizePref/100, fontsizeMin)
        else:
            fontSize = fontsizeMax
        
        if not tracer:
            return fontSize, (x, y, 0, 0)
        
        ctx.set_font_size(fontSize)
        fheight = ctx.font_extents()[2]
        x, y, w, h = reduire_rect(x, y, w, h, fheight, b)
        
        rect_eff = show_text_rect_fix(ctx, texte, x, y, w, h, 
                                    fontSize, None, va = va, ha = ha, le = le, pe = pe,
                                    coulBord = coulBord, wrap = wrap, couper = couper,
                                    ext = ext)
        return fontSize, rect_eff
    
    
    
    if fontSize < fontsizeMin:
        if debug: print("   fontSize mini !", fontSize, fontsizeMin, texte)
        if not tracer:
            return fontsizeMin, (x, y, 0, 0)
        
        ctx.set_font_size(fontsizeMin)
        fheight = ctx.font_extents()[2]
        x, y, w, h = reduire_rect(x, y, w, h, fheight, b)
        
        rect_eff = show_text_rect_fix(ctx, texte, x, y, w, h, 
                                    fontsizeMin, nLignesMaxi, va = va, ha = ha, le = le, pe = pe,
                                    coulBord = coulBord, wrap = wrap, couper = couper,
                                    ext = ext)
        return fontsizeMin, rect_eff
    
    
    
    #
    # "réduction" du rectangle (rectangle - bordure)
    #
    ctx.set_font_size(fontSize)
    fheight = ctx.font_extents()[2]
    # Période entre 2 lignes
    hl = fheight * le
    x, y, w, h = reduire_rect(x, y, w, h, fheight, b)

    
    #
    # Ajustement du rectange "ajusté" dans le rectangle
    #
    # taille du rectangle "ajusté"
    W, H = wh
    ecartx = (w-W)/2
    ecarty = (h-H)/2
    w, h = wh
    
    if va == 'h':
        y = y
    elif va == 'c':
        y = y + ecarty
    elif va == 'b':
        y = y + 2*ecarty
    
    if ha == 'c':
        x = x + ecartx
    elif ha == 'g':
        x = x
    elif ha == 'd':
        x = x + 2*ecartx
        
#     print "y", y
    
            
#    if debug: print "   nLignes :", nLignes
    ctx.set_font_size(fontSize)
    
    #
    # 2 ème tour
    #
    maxw = 0
    for t in lt:
        width = ctx.text_extents(t)[2]
        maxw = max(maxw, width)
    fontSize = min(fontSize, fontSize*w/maxw)
    
    # Réglage taille selon taille préférée
    if fontsizePref > 0:
        fontSize = max(fontSize * fontsizePref/100, fontsizeMinMax[0])
    if debug: print("   fontSize 4 :", fontSize, va)
    
    if not tracer:
        return fontSize, (x, y, W,H)

    if debug: print("H", h)
    ctx.set_font_size(fontSize)
    X, Y = show_lignes(ctx, lt, x, y, w, h, 
                       le, hl, ha = ha, coulBord = coulBord)
#                          va = va, ha = ha, le = le, pe = pe, coulBord = coulBord)
    
    return fontSize, (X, Y, W, H)




    

def decoupe_text(ctx, texte, w, nLignesMax, ext = "..."):
    """ Découpe un texte en une liste de lignes
        de telle sorte qu'il rentre dans la largeur <w> (unités cairo)
        et tronquage à <nLignesMax> lignes maximum
    """
    
    # Découpage du texte en lignes
    lignes = texte.splitlines()
    
    # Longueur maxi des lignes (nbr de caractères)
    wmax = max([len(l) for l in lignes])
    
    i = 0
    continuer = len(texte) > 0
    while continuer:
        i += 1
        if wmax <= 0:
            continuer = False
            
        else:
            if i > 1:
                lt = []
                # On fait une découpe à "wmax" ...
                for l in lignes:
                    if wmax > 0:
                        lt.extend(textwrap.wrap(l, wmax))
                    else:
                        lt.append(l)
            else:
                lt = lignes


            # On teste si ça rentre ...
            if nLignesMax != None and len(lt) > nLignesMax:
                lt = lt[:nLignesMax]
                lt[-1] += ext
            maxw = max([ctx.text_extents(t)[2] for t in lt])
            if maxw <= w: # Ca rentre !
                continuer = False
            else: # Ca ne rentre pas --> on coupe plus ras.
                wmax -= 1

    return lt


#def decoupe_text(ctx, texte, w, nLignesMax):
#    """ Découpe un texte en une liste de lignes
#        de telle sorte qu'il rentre dans la largeur w
#        et tronquage à nLignesMax lignes maximum
#    """
#    
#    # Découpages du texte en lignes
#    lignes = texte.split("\n")
#    
#    # Longueur maxi des lignes (nbr de caractères)
#    wmax = max([len(l) for l in lignes])
#    
#    i = 0
#    continuer = len(texte) > 0
#    while continuer:
#        i += 1
#        
#        lt = []
#        # On fait une découpe à "wmax" ...
#        for l in lignes:
#            if wmax > 0:
#                lt.extend(textwrap.wrap(l, wmax))
#            else:
#                lt.append(l)
#        
#        if wmax <= 0:
#            continuer = False
#        else:
#            # On teste si ça rentre ...
#            if nLignesMax != None and len(lt) > nLignesMax:
#                lt = lt[:nLignesMax]
#                lt[-1] += "..."
#            maxw = max([ctx.text_extents(t)[2] for t in lt])
#            if maxw <= w: # Ca rentre !
#                continuer = False
#            else: # Ca ne rentre pas --> on coupe plus ras.
#                wmax += -1
#                
#            if wmax == 0:
#                continuer = False
#            
#    return lt

##########################################################################################################################
def show_text_rect_fix(ctx, texte, x, y, w, h, fontSize,
                       Nlignes = 1, va = 'c', ha = 'c', le = 0.8, pe = 1.0, 
                       coulBord = None, wrap = True, couper = True, ext = "..."):#, outPosMax = False):
    """ Affiche un texte 
            (en tronquant sa longueur s'il le faut
             pour qu'il rentre dans le rectangle)
             
        x, y, w, h : position et dimensions du rectangle
        fontSize : taille de la police
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        coulBord : coulBord = couleur de la bordure (pas de bordure si None)
        Nlignes : coupe le texte en Nlignes maxi (None pour "pas de limite")
        
        Retourne :
            Dimentions du rectangle "effectif" (encadrant le texte au plus près)
    """
#     print "show_text_rect_fix", texte
    if texte == "":
        return 0.0, 0.0

    ctx.set_font_size(fontSize)
    
    fheight = ctx.font_extents()[2]
    # Période entre 2 lignes
    hl = fheight * le
    
    
    lt, fontSize, wh = ajuster_texte_fixe(ctx, texte, w, h, 
                                              fontSize,
                                              le = le, pe = pe, 
                                              wrap = wrap, couper = couper)

    ctx.set_font_size(fontSize)
    
#     #
#     # Découpage du texte en lignes, de telle sorte qu'il rentre dans la largeur w
#     # et tronquage en même temps
#     #
#     if wrap:
#         lt = decoupe_text(ctx, texte, w, Nlignes, ext = ext)
#     else:
#         lt = [texte]
    
    #
    # Ajustement du rectange "ajusté" dans le rectangle
    #
    # taille du rectangle "ajusté"
    W, H = wh
    ecartx = (w-W)/2
    ecarty = (h-H)/2
    w, h = wh
    
    if va == 'h':
        y = y
    elif va == 'c':
        y = y + ecarty
    elif va == 'b':
        y = y + 2*ecarty
    
    if ha == 'c':
        x = x + ecartx
    elif ha == 'g':
        x = x
    elif ha == 'd':
        x = x + 2*ecartx
    
    X, Y = show_lignes(ctx, lt, x, y, w, h, 
                       le, hl, ha, 
                       coulBord = coulBord)
    
    return X, Y, W, H




#########################################################################################################################
def show_lignes(ctx, lignes, x, y, w, h, 
                le, hl, ha = 'g', 
#                 va = 'h', ha = 'g', le = 0.8, pe = 1.0, \
                coulBord = None):
    """ Affiche une série de lignes de texte
        Renvoie la position la plus extrème à droite
        (pour éventuellement écrire une suite au texte)
        
        x, y, w, h : position et dimensions du rectangle "effectif"
        ha : alignements horizontal ('g', 'c', 'd')
        hl : période des lignes
        coulBord = couleur de la bordure (pas de bordure si None)
        
        La taille de la police doit être définie au préalable.
        
        Renvoie : 
        Position du rectangle effectif (encadrant le texte au plus juste)
    """
#     x = x/echelle
#     y = y/echelle
#     w = w/echelle
#     h = h/echelle
#     ctx.save()
#     ctx.scale(echelle, echelle)

    
    # Caractéristiques verticales de la police
    fascent, fdescent, fheight = ctx.font_extents()[:3]
#     hl = fheight * le
#     print 'hl', hl
    # Espacement vertical entre les lignes
#     hl = fheight * le   ###fascent+fdescent
    
#     ht = fheight*len(lignes) + fheight*(le-1.0)*(len(lignes)-1)
#     print "y", y
#     print "ht", ht
#     ht = hl*len(lignes)
    # Décalage vertical (pour centrer verticalement)
#     if va == 'c':
#         dy = (h-ht)/2
#     elif va == 'b':
#         dy = h-ht
#     else:
#         dy = 0
#     print "dy", dy
    
    #########
    ctx.save()
    ht = calcul_hauteur(fheight, le, len(lignes))
    coef = h/ht
#     print "coef", coef
    ctx.translate(0, (1-coef)*y)
    ctx.scale(1.0, coef)
#     
    #########
    
    
    #
    # On dessine toutes les lignes de texte
    #
    X = x
    for l, t in enumerate(lignes):
#        print "  ",t
        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(t)
        
        # Position du rectangle encadrant la ligne
        if ha == 'c':
            xt = x + (w-width)/2
        elif ha == 'g':
            xt = x
        elif ha == 'd':
            xt = x + w-width
        
        yt = y + hl*l
        
        X = min(X, xt)
        
        # Coordonnées du point de référence
        xt -= xbearing
        yt += fascent
        ctx.move_to(xt, yt)
        
        if coulBord == None:
    #        print t
            ctx.show_text(t)
          
        else:
            ctx.text_path(t)
            ctx.fill_preserve()
            ctx.set_source_rgb(*coulBord)
            ctx.set_line_width(fheight/30)
        
#     print 'yt', yt
    ctx.stroke()
    #########
#     
    ctx.restore()
    #########
    

    return X, y





#########################################################################################################  
#
#    Représentation des périodes d'un enseignement (années, trimestres, ...)
#
######################################################################################################### 
BcoulPos = []
IcoulPos = []
ICoulComp = []
CoulAltern = []
fontPos = 0.014 * COEF 
import couleur

######################################################################################  
def DefinirCouleurs(n1, n2, n3):
    global IcoulPos, BcoulPos, CoulAltern
    couleur.generate(IcoulPos, [0xFFC3D0E2, 0xFFF2C5B5], n1)
    couleur.generate(BcoulPos, [0xFF82AAE0, 0xFFEF825D], n1)
    
    couleur.generate(ICoulComp, [0xFFFF6666, 0xFFFFFF66, 0xFF75FF66, 0xFF66FFF9, 0xFFFF66F4], n2)
    
    del CoulAltern[:]
    for n in range(n3//2+1):
        CoulAltern += [((0.85, 0.85, 0.95, 0.3),    (0, 0, 0, 1)),
                       ((0.7,  0.7,  0.8,  0.2),    (0, 0, 0, 1))]


import calendar
from datetime import date

######################################################################################  
def est_ferie(Date, creneaux):
    for c in creneaux:
        if c[0] < Date < c[1]:
            return True
    return False


######################################################################################  
def DrawCalendrier(ctx, rect, calendrier):
    """ Dessine un calendrier
         >> Renvoie la liste des rectangles des semaines
    """
    x, y, wt, ht = rect
    ctx.set_line_width (0.0005 * wt)
        
    # Les rectangles à cliquer
    rects = []
    
    cal = calendar.Calendar()
    
    # Espace pour les noms des années
    ha = 0.12 * ht
    
    # Espace pour les noms des jours
    wj = 0.02 * wt
    
    # Espace pour le nom des mois
    hm = 0.08 * ht
    
    # Ecart entre les années
    ea = 0.02 * wt
    wt = wt - 2*ea
    x += ea
    
    # Ecart vertical
    ey = 0.02 * ht
    ht -= 2*ey
    y += ey
    
    # Ecart "vacances"
    ev = 0.005 * wt
    
    # Période entre deux années
    dx_a = (wt-wj)/calendrier.GetNbrAnnees() + ea
    
    # liste des années
    lannees = calendrier.GetListeAnnees()
    
    # listes des mois   
    lmois, nmois = calendrier.GetMois()
    
    
    # Période entre deux mois
    dx_m = (wt - wj - (calendrier.GetNbrAnnees()-1)*ev - calendrier.GetNbrAnnees()*ea) / nmois
    
    # Période entre deux jours
    dy_j = (ht-ha-hm) / 31
    
    # largueur des zones année
    wa = {}
    for ia, annee in enumerate(lannees):
        if ia == 0:
            wa[annee] = dx_m*len(lmois[annee])
        elif ia == calendrier.GetNbrAnnees():
            wa[annee] = dx_m*len(lmois[annee])
        else:
            wa[annee] = dx_m*len(lmois[annee])+ev
    
    #
    # Les noms des années, mois et jours
    #
    X = x
    
    jours_feries = constantes.JOURS_FERIES
    lstAcad = sorted([a[0] for a in list(constantes.ETABLISSEMENTS.values())])
    creneaux = calendrier.GetCreneauxFeries()
#     print "creneaux", creneaux
    
    for ia, annee in enumerate(lannees):

#         if annee in jours_feries.keys():
#             list_zones, list_crenaux = jours_feries[annee]
#             acad = calendrier.GetClasse().academie
#             
#             try:
#                 num_acad = lstAcad.index(acad)
#             except:
#                 num_acad = None
# 
#             
#             zone = None
#             if num_acad is not None:
#                 for z, l in list_zones.items():
#                     if num_acad in l:
#                         zone = z
#                         break
# 
#             if zone in list_crenaux.keys():
#                 creneaux.extend(list_crenaux[zone])
#         
            
        
        show_text_rect(ctx, str(annee), 
                       (X+wj, y, wa[annee], ha), 
                       wrap = False,
                       orient = 'h', ha = 'c', va = 'c', b = 0.1)
        
        Y = y+ha+hm
        for jour in range(31):
            show_text_rect(ctx, str(jour+1), 
                           (X, Y, ea, dy_j), 
                           wrap = False,
                           orient = 'h', ha = 'd', va = 'c', b = 0.1)
            Y += dy_j
        
        for per in lmois[annee]:
            for mois in per:
                show_text_rect(ctx, constantes.MOIS[mois-1], 
                               (X+wj, y+ha, dx_m, hm),
                               orient = 'h', ha = 'c', va = 'c', b = 0.1, ext = "")
                X += dx_m
            X += ev
        
        X += ea-ev
    
    
    
    for c in creneaux:
        if type(c[0]) == list :
            c[0] = date(*c[0])
        if type(c[1]) == list:
            c[1] = date(*c[1])
    
    #
    # Les cases des jours
    #
    X = x+wj
    S = 0   # Numéro de la semaine
    for annee in lannees:
        
                
        for per in lmois[annee]:
            for mois in per:
                Y = y+ha+hm
                for semaine in cal.monthdayscalendar(annee, mois):
                    lj = [j for j in semaine if j != 0]
                    if len(lj) > 3 or len(rects) == 0:
                        rects.append((X, Y, dx_m, len(lj)*dy_j))
                        hs = dx_m*0.6
                        ys = Y+(len(lj)*dy_j - hs)/2
                        rs = (X, ys, dx_m, hs)
                        
                        # Numéro de la semaine
                        ctx.set_source_rgba(0.4,  0.6,  0.4,  1)
                        show_text_rect(ctx, str(S+1), 
                                       rs, couper = False, wrap = False, ext = "",
                                       orient = 'h', ha = 'c', va = 'c', b = 0.1)
                    
                    for jour in semaine:
                        if jour != 0:
                            ctx.set_source_rgba(1, 0.9, 1, 0.5)
                            if est_ferie(date(annee, mois, jour), creneaux):
                                ctx.set_source_rgba(0.3, 0.3, 0.3, 1)
                            if calendar.weekday(annee, mois, jour) > 5:
                                ctx.set_source_rgba(0, 0, 0, 1)
                                
                            ctx.rectangle (X, Y, dx_m, dy_j)
                            ctx.fill_preserve ()
                            ctx.set_source_rgba(0, 0, 0, 1)
                            ctx.stroke()
                            Y += dy_j
                            if calendar.weekday(annee, mois, jour) == 6:
                                S += 1
                    
                X += dx_m
            X += ev
        X += ea-ev
    return rects


def getBitmapCalendrier(larg, calendrier):

    prop = calendrier.GetNbrAnnees()
    w, h = 0.04*prop * COEF, 0.04 * COEF
#    print w, h
    imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  larg, int(h/w*larg))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
    ctx = cairo.Context(imagesurface)
    ctx.scale(larg/w, larg/w) 
    DrawCalendrier(ctx, (0,0,w,h), calendrier)

    return imagesurface


                 
######################################################################################  
def DrawPeriodes(ctx, rect, pos = None, periodes = [["Année", 5]], projets = {}, 
                 tailleTypeEns = 0):
    """ Dessine les périodes de l'enseignements
         >> Renvoie la liste des rectangles des positions
    """
#    print "DrawPeriodes", pos
    
    ctx.set_line_width (0.001 * COEF)
    if not isinstance(pos, list):
        pos = [pos]

    x, y, wt, ht = rect
    
    # Toutes le périodes de projet
    periodes_prj = [p.periode for p in list(projets.values())]
#    print "   ", periodes, periodes_prj
    
    # Les noms des projets par période
    noms_prj = {}
    for n, p in list(projets.items()):
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
    rects = []
    
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
        if len(annee) > 1: # Exposant
            ctx.set_font_size(fontPos*0.9)
            w1 = ctx.text_extents(annee[1])[2]
            show_text_rect_fix(ctx, annee[0], xi+wa/2-(w0+w1)/2, y, 
                               w0, ht*2/3, fontPos, 1, ha = 'd')
            ctx.stroke ()
            show_text_rect_fix(ctx, annee[1], xi+wa/2-(w0+w1)/2 + w0 +fontPos/10, y, 
                               w1, ht/3, fontPos*0.9, 1, ha = 'g')
            ctx.stroke ()
        else:
            show_text_rect_fix(ctx, annee[0], xi+wa/2-w0/2, y, w0, ht*2/3, fontPos, 1)
            ctx.stroke ()
        
        for c in range(np):
            pa += 1
            if pa in list(noms_prj.keys()):
                n = noms_prj[pa]
            else:
                n = ""
            xcs.append((xi + c*(w+dx) + dx, (pa-1) in pos, i, n))
            
        xi += np*w + (np+1)*dx
        
    # Liste des positions qui fusionnent avec leur position précédente
    lstGrp = []
    for periode_prj in periodes_prj:
        if len(periode_prj) > 0:
            lstGrp.extend(list(range(periode_prj[0]+1, periode_prj[-1]+1)))
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
        rects.append((xc[0], y+ht/2+dx, w, h))
        if xc[1]:
            ctx.set_source_rgba(*BcoulPos[p])
            ctx.fill_preserve ()
            ctx.set_source_rgba(0, 0, 0, 1)
        else:
            ctx.set_source_rgba(*(IcoulPos[p]))
            ctx.fill_preserve ()
            ctx.set_source_rgba(*BcoulPos[p])
        ctx.stroke ()    
        
        if xc[3] != "":
            show_text_rect(ctx, xc[3], 
                           rects[-1], ha = 'c', b = 0.2, wrap = False, couper = False)
            ctx.stroke ()
            
    return rects





########################################################################################
#
#    Image des périodes de l'enseignement , position et projets
#          
########################################################################################            
def getBitmapPeriode(larg, position, periodes, projets = {}, prop = 7):
#     print("getBitmapPeriode", larg)
#        print "  ", self.projet.position
#        print "  ", self.projet.GetReferentiel().periodes
#        print "  ", self.projet.GetReferentiel().periode_prj
    
    w, h = 0.04*prop * COEF, 0.04 * COEF
#    print w, h
    imagesurface = cairo.ImageSurface(cairo.FORMAT_RGB24,  int(larg), int(h/w*larg))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
    ctx = cairo.Context(imagesurface)
    ctx.scale(larg/w, larg/w) 
#     ctx.set_source_rgba(1,1,1,1)
#     ctx.paint()
    try:
        DrawPeriodes(ctx, (0,0,w,h), position, periodes, projets)
    except:
        pass

    return imagesurface


    



######################################################################################  
def DrawClasse(ctx, rect, classe):
    """ Dessine la répartition des élèves dans la classe
         >> Renvoie la liste des rectangles des groupes
    """
#     print "DrawClasse"
#     print classe.effectifs
#     print classe.nbrGroupes
    
    ref = classe.GetReferentiel()
    
    
    ctx.set_line_width (0.001 * COEF)
    
    x, y, wt, ht = rect 
    
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                       cairo.FONT_WEIGHT_NORMAL)
    
    # Ecart entre les cases
    dy = 0.01 * ht
    dx = 0.05 * wt
    d = 0.03 * ht
    
    # Espace pour écrire le texte sur les cotés
    wtxt = wt*1/10
    
    # Taille de la police
    f = wt/50
    
    # Epaisseur de ligne
    e = wt/500
    
    wEff = {"C" : wt,
             "G" : wt*6/7,
             "D" : wt*5/7,
             "E" : wt/classe.nbrGroupes['E']*6/7,
             "P" : wt/classe.nbrGroupes['P']*6/7
             }
    
    # Les rectangles à cliquer
    rects = []
    
    def empiler(texte, x, y, w, h, nbr, coul):
        W = w - (nbr-1)*dx
        H = h - (nbr-1)*dy
        for n in range(nbr-1, -1, -1):
            X = x + n*dx
            Y = y + n*dy
            rectanglePlein(X, Y, W, H, coul)
        show_text_rect_fix(ctx, texte, 
                           X, Y, W, H,
                           f)
        
            
    def rectanglePlein(x, y, w, h, coul):
        ctx.set_line_width(e)
        ctx.rectangle(x, y, w, h)
        ctx.set_source_rgb(*[c*3.0 for c in coul])
        ctx.fill_preserve ()
        ctx.set_source_rgb(*coul)      
        ctx.stroke()
    
    # Classe entière
    X = x + d
    Y = y + d
    W = wt - 2*d
    H = ht - 2*d
        
    ctx.set_line_width(e)
    coul = constantes.CouleursGroupes["C"]
#     print(coul)
#     print(ref.effectifs["C"][3])
    coul = couleur.CouleurInt2Float(ref.effectifs["C"][3])
#     print(coul)
    rectanglePlein(X, Y, W, H, coul)
    rects.append((X, Y, W, H))
    show_text_rect_fix(ctx, ref.effectifs["C"][1], 
                           X+W-wtxt , Y, wtxt, H,
                           f, Nlignes = 2)
    
    
        
    # Effectif réduit
    n = classe.nbrGroupes["G"]
    X = X + d
    Y = Y + d
    W = W - wtxt - 2*d
    H = H - 2*d
    
    wEff["G"] = W - (n-1) * dx
    
    ctx.set_line_width(e)
#     coul = constantes.CouleursGroupes["G"]
    coul = couleur.CouleurInt2Float(ref.effectifs["G"][3])
    empiler("", X, Y, W, H, n, coul)
    rects.append((X, Y, W, H))
    
    show_text_rect_fix(ctx, ref.effectifs["G"][1], 
                           X+wEff["G"]-wtxt, Y, wtxt, H,
                           f, Nlignes = 2)
    
    
    # Nombre total de groupes à loger
    N = 2+classe.nbrGroupes["E"]+classe.nbrGroupes["P"]
    
    # Hauteurs des cases
    Hc = (H-(n-1)*d - 4*d - (N-3) * dy)/3
    
    # Demi groupe
    X = X + d
    Y = Y + d
    W = wEff["G"] - wtxt - 2*d
    h = Hc + dy
    
    
    wEff["D"] = wEff["G"] /2 
    
    ctx.set_line_width(e)
#     coul = constantes.CouleursGroupes["D"]
    coul = couleur.CouleurInt2Float(ref.effectifs["D"][3])
    empiler(ref.effectifs["D"][1],
             X, Y, W, h, 2, coul)
    rects.append((X, Y, W, h))
    
    
    # Etudes et Projets
    n = classe.nbrGroupes["E"]
    dx = min(dx, (W - wt/ 7) / n)
    Y = Y + h + d
    h = Hc + (n-1)*dy
    
    ctx.set_line_width(e)
#     coul = constantes.CouleursGroupes["E"]
    coul = couleur.CouleurInt2Float(ref.effectifs["E"][3])
    empiler(ref.effectifs["E"][1],
             X, Y, W, h, n, coul)
    rects.append((X, Y, W, h))
    wEff["E"] = wEff["G"] / n
    
    
    # Activités Pratiques
    n = classe.nbrGroupes["P"]
    dx = min(dx, (W - wt/ 7) / n)
    Y = Y + h + d
    h = Hc + (n-1)*dy
    
    ctx.set_line_width(e)
#     coul = constantes.CouleursGroupes["P"]
    coul = couleur.CouleurInt2Float(ref.effectifs["P"][3])
    empiler(ref.effectifs["P"][1],
             X, Y, W, h, n, coul)
    rects.append((X, Y, W, h))
    wEff["P"] = wEff["G"] / n
    
    
    return wEff, rects






def getBitmapClasse(larg, classe):
#     print("getBitmapClasse", larg)
    prop = 7.0
    w, h = 0.04*prop * COEF, 0.04 * COEF
#    print w, h
#     imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  larg, int(h/w*larg))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
    imagesurface = cairo.ImageSurface(cairo.FORMAT_RGB24,  larg, int(h/w*larg))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
    ctx = cairo.Context(imagesurface)
    ctx.scale(larg/w, larg/w) 
    ctx.set_source_rgba(1,1,1,1)
    ctx.paint()
#     ctx.paint()
    DrawClasse(ctx, (0,0,w,h), classe)
    
    
    
    return imagesurface


##########################################################################################
def get_apercu(doc, larg, prop = 0.7071, entete = False):
    """ Renvoi un apercu du document <doc>
        sous la forme d'une cairo.ImageSurface
    
    """
#    print "get_apercu", larg, prop
#    w, h = 0.04*prop * COEF, 0.04 * COEF
    imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  int(larg), int(1.0*larg/prop))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
    ctx = cairo.Context(imagesurface)
    s = 1.0*larg/prop/COEF
    ctx.scale(s, s) 
#    ctx.scale(mult, mult) 
    doc.draw.Draw(ctx, doc, entete = entete)
    
    del ctx
         
    return imagesurface


            
def curve_rect_titre(ctx, titre, rect, 
                     coul_bord, coul_int, 
                     taille_font = 0.01 * COEF, 
                     rayon = 0.02 * COEF, epaiss = 0.002 * COEF):
    """    Dessine une zone de texte aux bords arrondis
            avec un titre au dessus
            
            >> Renvoie le point caractéristique (svg)
    """
    ctx.set_line_width(epaiss)
    x0, y0, rect_width, rect_height = rect
    
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(taille_font)
    fheight = ctx.font_extents()[2]
    xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(titre)
      
    c = curve_rect_coin(ctx, x0, y0, rect_width, rect_height, rayon, 
               ouverture = min(width + fheight, rect_width-2*rayon))
    
    ctx.set_source_rgba(*coul_int)
    ctx.fill_preserve()
    ctx.set_source_rgba(*coul_bord)
    ctx.stroke()
    
    xc = x0# + rayon
    mask = cairo.LinearGradient(xc, y0, xc, y0 - height)
    mask.add_color_stop_rgba(1, 1, 1, 1, 0)
    mask.add_color_stop_rgba(0, coul_int[0], coul_int[1], coul_int[2], coul_int[3])
    ctx.rectangle(xc, y0 - height, min(width + fheight, rect_width-2*rayon), height)
    ctx.set_source(mask) 
    ctx.fill()
    
    xc = x0 + fheight/2# + rayon
    yc = y0 + ybearing - fheight/3#height
    
    ctx.move_to(xc, yc)
    ctx.set_source_rgb(0, 0, 0)
#    ctx.show_text(titre)
    
    show_text_rect_fix(ctx, titre, xc, yc, rect_width-2*rayon, fheight,
                       taille_font, 1, ha = "g")
    
    return c


##################################################################################
def curve_rect_coin(ctx, x0, y0, rect_width, rect_height, radius, ouverture = 0):
    """    Dessine une zone de texte aux bords arrondis
            avec un coin "carré" (en haut à gauche)
            >> Renvoie le point caractéristique (svg)
    """
    x1=x0+rect_width
    y1=y0+rect_height
    #if (!rect_width || !rect_height)
    #    return
    if rect_width/2<radius:
        if rect_height/2<radius:
            ctx.move_to  (x0, (y0 + y1)/2)
            ctx.line_to (x0 ,y0)
            ctx.line_to ((x0 + x1)/2, y0)
            ctx.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
            ctx.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
            ctx.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
        else:
            ctx.move_to  (x0, y0 + radius)
            ctx.line_to (x0 ,y0)
            ctx.line_to ((x0 + x1)/2 ,y0)
            ctx.curve_to (x1, y0, x1, y0, x1, y0 + radius)
            ctx.line_to (x1 , y1 - radius)
            ctx.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
            ctx.curve_to (x0, y1, x0, y1, x0, y1- radius)
    
    else:
        if rect_height/2<radius:
            ctx.move_to  (x0 + ouverture, y0)
            ctx.line_to (x1 - radius, y0)
            ctx.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
            ctx.curve_to (x1, y1, x1, y1, x1 - radius, y1)
            ctx.line_to (x0 + radius, y1)
            ctx.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
            ctx.line_to (x0 ,y0)
            
        else:
            ctx.move_to  (x0 + ouverture, y0)
            ctx.line_to (x1 - radius, y0)
            ctx.curve_to (x1, y0, x1, y0, x1, y0 + radius)
            ctx.line_to (x1 , y1 - radius)
            ctx.curve_to (x1, y1, x1, y1, x1 - radius, y1)
            ctx.line_to (x0 + radius, y1)
            ctx.curve_to (x0, y1, x0, y1, x0, y1- radius)
            ctx.line_to (x0, y0)
    
    # Renvoie les coordonnées du 1er point = caractéristique du path SVG
    return x0 + ouverture, y0 



##################################################################################
def curve_rect(ctx, x0, y0, rect_width, rect_height, radius, ouverture = 0):
    """    Dessine une zone de texte aux bords arrondis
            >> Renvoie le point caractéristique (svg)
    """
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
    
    # Renvoie les coordonnées du 1er point = caractéristique du path SVG
    return x0 + radius  + ouverture, y0 



def image(ctx, x, y, w, h, bmp, marge = 0):
    """ Dessine une image
    
    """
    
    x = x + marge*w
    y = y + marge*h
    w = w - 2*marge*w
    h = h - 2*marge*h
    
    tfname = tempfile.mktemp()
    try:
        bmp.SaveFile(tfname, wx.BITMAP_TYPE_PNG)
        image = cairo.ImageSurface.create_from_png(tfname)
    finally:
        if os.path.exists(tfname):
            os.remove(tfname)  
    W = image.get_width()
    H = image.get_height()
    s = min(w/W, h/H)
    
    dx = max(0,(w-s*W)/2)
    dy = max(0,(h-s*H)/2)
    
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.set_source_surface(image, dx, dy)
    ctx.paint()
    ctx.restore()

    
def tableauV(ctx, titres, x, y, w, ht, hl, nlignes = 0, va = 'c', ha = 'c', orient = 'h', coul = (0.9,0.9,0.9), b = 0.2):
    """    Dessine un tableau vertical (entêtes à l'horizontale)
            x, y = position du coin haut-gauche
            ht = hauteur de la ligne d'entête
            hl = hauteur de chaque ligne
            
            >> Renvoie la liste des rectangles des entêtes
    """
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
        ctx.set_source_rgba (*_coul)
        show_text_rect(ctx, titre, (_x, y, wc, ht), va = va, ha = ha, b = b, orient = orient, 
                       couper = True, wrap = True)
        
#        if orient == 'h':
        rect.append((_x, y, wc, ht))
#        else:
#            rect.append((-y, _x, wc, ht))
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
             coul = (0.9,0.9,0.9), contenu = [], tailleFixe = False):
    
    rect = []
    hc = h/len(titres)
    _y = y
    _coul = ctx.get_source().get_rgba()

    taillesFont = []
    for i, titre in enumerate(titres):
        ctx.rectangle(x, _y, wt, hc)
        if type(coul) == dict :
            col = coul[titre.rstrip("1234567890.")]
        elif type(coul[0]) == tuple:
            col = coul[i]
        else:
            col = coul
        ctx.set_source_rgba (*col[0])
        ctx.fill_preserve ()
        ctx.set_source_rgba (*_coul)
        taillesFont.append(show_text_rect(ctx, titre, (x, _y, wt, hc), va = va, ha = ha, 
                                          b = 0.2, orient = orient, tracer = not tailleFixe)[0])
        
        rect.append((x, _y, wt, hc))
        ctx.stroke ()
        _y += hc
    
    
    if tailleFixe: # Tracé en différé
        tailleFont = min(taillesFont)
        _y = y
        for i, titre in enumerate(titres):
            ctx.set_source_rgba (*_coul)
            show_text_rect(ctx, titre, (x, _y, wt, hc), va = va, ha = ha, 
                            b = 0.2, orient = orient, fontsizeMinMax = (tailleFont, tailleFont))
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
            show_text_rect(ctx, l, (_x, _y, wc, hc), va = va, ha = ha, b = 0.2, orient = orient)
            _y += hc
        _x += wc
        _y = y
        
    ctx.stroke ()
    
    return rect

def tableauH_var(ctx, titres, x, y, wt, wc, hl, taille, nCol = 0, va = 'c', ha = 'c', orient = 'h', 
             coul = (0.9,0.9,0.9), contenu = []):
    """Dessine un tableau horizontal :
    
    +-------------+--------------------+--------------------+---------+
    |    titre    |    contenu col1    |    contenu col2    |    ...  |
    +-------------+--------------------+--------------------+---------+
    |    titre    |    contenu col1    |    contenu col2    |    ...  |
    +-------------+--------------------+--------------------+---------+
    |     ...     |      ...           |      ...           |    ...  |
    +-------------+--------------------+--------------------+---------+
        
        :param hl: liste des hauteurs de lignes
        :param nCol: nombre de colonnes
    """
#    hc = h/len(titres)
    _y = y
    _coul = ctx.get_source().get_rgba()
#     print "tableauH", _coul
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
        ctx.set_source_rgba (*_coul)
        show_text_rect(ctx, titre, (x, _y, wt, hl[i]), va = va, ha = ha, 
                       orient = orient, fontsizeMinMax = (-1, taille))
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


def rectangle_plein_biseau(ctx, x, y, w, h, b, coulBord, coulInter, alpha = 1):
    ctx.move_to(x+b, y)
    ctx.line_to(x+w, y)
    ctx.line_to(x+w-b, y+h)
    ctx.line_to(x, y+h)
    ctx.line_to(x+b, y)
    
    
    ctx.set_source_rgba (coulInter[0], coulInter[1], coulInter[2], alpha)
    ctx.fill_preserve ()
    ctx.set_source_rgba (coulBord[0], coulBord[1], coulBord[2], alpha)
    ctx.stroke ()
    
    
def rectangle_plein_fleche(ctx, x, y, w, h, b, coulBord, coulInter, alpha = 1):
    ctx.move_to(x, y)
    ctx.line_to(x+w-b, y)
    ctx.line_to(x+w, y+h/2)
    ctx.line_to(x+w-b, y+h)
    ctx.line_to(x, y+h)
    ctx.line_to(x+b, y+h/2)
    ctx.line_to(x, y)
    
def rectangle_plein_doigt(ctx, x, y, w, h, b, yd, coulBord, coulInter, alpha = 1):
    if b > h:
        b = h
    if yd < b:
        yd = b
    elif yd > h-b:
        yd = h-b
    ctx.move_to(x,     y)
    ctx.line_to(x+w-b, y)
    ctx.line_to(x+w-b, y+yd-b)
    ctx.line_to(x+w,   y+yd)
    ctx.line_to(x+w-b, y+yd+b)
    ctx.line_to(x+w-b, y+h)
    ctx.line_to(x,     y+h)
    ctx.line_to(x,     y)
    
    
    ctx.set_source_rgba (coulInter[0], coulInter[1], coulInter[2], alpha)
    ctx.fill_preserve ()
    ctx.set_source_rgba (coulBord[0], coulBord[1], coulBord[2], 1)
    ctx.stroke ()


def boule(ctx, x, y, r, p = 100, 
          color0 = (1, 1, 1, 1), color1 = (0, 0, 0, 1),
          transparent = True):
    
    mask = 0.01*p
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
    
    ctx.set_line_width (0.0003 * COEF)
    ctx.set_source_rgba (1, 1, 1, 1)
    ctx.arc (x, y, r, 0, 2*pi)
    ctx.fill_preserve()
    ctx.set_source_rgba (0, 0, 0, 1)
    ctx.stroke ()
    
    ctx.set_source (pat)
    ctx.move_to (x, y)
    ctx.line_to (x, y-r)
    ctx.arc (x, y, r, 3*pi/2, 2*pi*mask + 3*pi/2)
    ctx.fill()




# def relief(ctx, (x, y, w, h), e, color = (1, 1, 1, 1), bosse = True):
#     
#     if bosse:
#         k = [1.3, 1.5, 0.7, 0.5, 1.0]
#     else:
#         k = [0.5, 0.5, 1.3, 1.5, 1.0]
#     
#     
#     
#     coul = [c*k[0] for c in color[:3]]+[color[3]]
#     ctx.set_source_rgba(*coul)
#     
#     ctx.move_to(x, y)
#     ctx.line_to(x+e, y+e)
#     ctx.line_to(x+e, y+h-e)
#     ctx.line_to(x, y+h)
#     ctx.line_to(x, y)
#     ctx.fill()
#     
#     coul = [c*k[1] for c in color[:3]]+[color[3]]
#     ctx.set_source_rgba(*coul)
#     ctx.move_to(x, y)
#     ctx.line_to(x+e, y+e)
#     ctx.line_to(x+w-e, y+e)
#     ctx.line_to(x+w, y)
#     ctx.line_to(x, y)
#     ctx.fill()
#     
#     coul = [c*k[2] for c in color[:3]]+[color[3]]
#     ctx.set_source_rgba(*coul)
#     ctx.move_to(x+w, y)
#     ctx.line_to(x+w-e, y+e)
#     ctx.line_to(x+w-e, y+h-e)
#     ctx.line_to(x+w, y+h)
#     ctx.line_to(x+w, y)
#     ctx.fill()
#     
#     coul = [c*k[3] for c in color[:3]]+[color[3]]
#     ctx.set_source_rgba(*coul)
#     ctx.move_to(x+w, y+h)
#     ctx.line_to(x+w-e, y+h-e)
#     ctx.line_to(x+e, y+h-e)
#     ctx.line_to(x, y+h)
#     ctx.line_to(x+w, y+h)
#     ctx.fill()
#     
#     coul = [c*k[4] for c in color[:3]]+[color[3]]
#     ctx.set_source_rgba(*coul)
#     ctx.rectangle(x+e, y+e, w-2*e, h-2*e)
#     ctx.fill()




def barreH(ctx, x, y, w, r, a, e, coul0, coul1, coul):
    """ Dessine une barre horizontale de poucentage/progression
        :param x,y: position
        :param w: longueur maxi (100%)
        :param r: taux
        :param e: épaisseur
        :param a: acceptable (a==True : coul0  - a==False = coul1)
    """
    src = ctx.get_source()
    
    if a:
        coulEtat = coul1
    else:
        coulEtat = coul0
        
    ctx.set_source_rgba(*coul)
    ctx.rectangle (x, y-e/2, w*r, e)
    ctx.fill_preserve ()    
    ctx.set_source_rgba(0.4,  0.4,  0.4,  1)
    ctx.set_line_width(0.001 * COEF)
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
    
def ligne(ctx, x1, y1, x2, y2, coul):
#     if len(coul) < 4:
#         coul = list(coul)+[1]
    ctx.set_source_rgba(*coul)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

        
def fleche_verticale(ctx, x, y, h, e, coul):
    ctx.set_source_rgba(*coul)
    he = min(e/2, h/3)
    ctx.move_to(x-e/2, y)
    ctx.line_to(x-e/2, y+h-he)
    ctx.line_to(x, y+h)
    ctx.line_to(x+e/2, y+h-he)
    ctx.line_to(x+e/2, y)
    ctx.close_path ()
    ctx.fill_preserve ()    
    ctx.set_source_rgba(0.4,  0.4,  0.4,  1)
    ctx.set_line_width(0.0006 * COEF)
    ctx.stroke ()
    

def fleche_ronde(ctx, x, y, r, a0, a1, e, f, coul):
    """ Dessine une flèche
        :param x, y: centre
        :param r: rayon
        :param a0, a1: angles de départ et d'arrivée (en degrés)
        :param e: épaisseur
        :param f: taille du bout de flèche
    """
    ctx.set_line_width (e)
    ctx.set_source_rgba (*coul)
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
    

########################################################################################
def liste_code_texte2(ctx, lstCodes, lstTexte, rect, 
                     dx, gras = None, lstCoul = None, va = 'h', 
                     coulFond = None):
    """ Affiche une liste d'élément sous la forme :
        code
        texte
        code 
        texte
        ...
        
        :param dx: décalage horizontal entre le bord et le texte
        :param b: bordure latérale totale (en relatif : 0 à 1)
        
        :return: Renvoie une liste de rectangles
    """
    x, y, w, h = rect
    
    no = len(lstCodes)
    if no == 0:
        return []
    
#     print "liste_code_texte2", h
    
    lstRect = []

#     maxFontSize = min(h / no * .7, 0.011 * COEF)
    
    # Equilibrage des tailles de font entre code et texte (approximatif)
#    nc = [len(c) for c in lstCodes]
#    nt = [len(t) for t in lstTexte]
    
    ctx.set_font_size(minFont)
    minfheight = ctx.font_extents()[2]
    
    # Hauteur des codes
    maxFontSize = 0.011 * COEF
    ctx.set_font_size(maxFontSize)
    hc = ctx.font_extents()[2]
    
#     print "   min-max", minfheight, "-", hc
    
    # Hauteurs des textes
    c = [len(t) for t in lstTexte]
    tot = sum(c)
    c = [float(l)/tot for l in c]   # Normalisation des longueurs des textes
    ht = h - no*hc                  # Reste de hauteur pour les textes
    ht = [ht*cc for cc in c]        # Répartition des hauteurs en fonction de la longueur des textes
#     print "   ", hc, ht
    
    # On réduit les codes
    acote = False
    va = 'b'
    if min(ht) < minfheight:    # Pas la place en hauteur pour le texte (moins d'une ligne !)
        ht = [max(minfheight, hh) for hh in ht]
        if sum(ht) <= h:
            hc = (h - sum(ht))/no
#             print "      .", hc, ht
            # On déplace les textes sur le codé
            if hc < minfheight:
                hc = h/no
                acote = True
                va = 'c'
                ht = [0] * no
#                 print "         ..", hc, ht
                dx = -1
        else:
            hc = h/no
            acote = True
            va = 'c'
            ht = [0] * no
#             print "            ...", hc, ht
    
    
    
    
    
    #
    # Codes
    #
    wc = []
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_BOLD)
    for i, t in enumerate(lstCodes):
        if t.strip() != "":
            
            # Un rectangle pour la séléction
            rect = (x, y + sum(ht[:i]) + i*hc, w, hc+ht[i])
            lstRect.append(rect)
            ctx.set_line_width(0.0001 * COEF)
            ctx.set_source_rgba (*coulFond[:3], 0.01)
            ctx.rectangle(*rect)
            ctx.fill_preserve()
            ctx.stroke()
            
            
            if lstCoul != None:
                ctx.set_source_rgb (*lstCoul[i])
#                else:
#                    ctx.set_source_rgb (0, 0, 0)
            re = (x, y + sum(ht[:i]) + i*hc, w, hc)
            r = show_text_rect(ctx, t,
                           re, #y+i*hl, 
                           b = 0, ha = 'g', va = va, 
                           fontsizeMinMax = (-1, maxFontSize), wrap = False)[1]
#             ctx.set_line_width(0.0001 * COEF)
#             ctx.rectangle(*re)
#             ctx.stroke()     
            wc.append(r[2])
            
    if acote:
        dx = max(wc) + minfheight
            
    #
    # Textes
    #
#     ly = []
    for i, t in enumerate(lstCodes):
        if lstTexte[i].strip() != "":
            if i == gras:
                ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
            else:
                ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_NORMAL)
            if lstCoul != None:
                ctx.set_source_rgb (*lstCoul[i])
#                else:
#                    ctx.set_source_rgb (0, 0, 0)
            if acote:
                re = (x + dx, y + i*hc, w - dx, hc)
                va = 'c'
            else:
                re = (x + dx, y + (i+1)*hc + sum(ht[:i]), 
                      w - dx, ht[i])
                va = 'h'  
            
            show_text_rect(ctx, lstTexte[i], 
                           re, 
                           b = 0, ha = 'g', va = va, 
                           fontsizeMinMax = (-1, maxFontSize))
            
            
            
#             ctx.set_line_width(ep)
#             ctx.set_source_rgba (*co)
#            ctx.restore()


    
        
    
    return lstRect



########################################################################################    
def liste_code_texte(ctx, lstCodes, lstTexte, rect, 
                     eh, b = 0.1, gras = None, lstCoul = None, va = 'h'):
    """ Affiche une liste d'élément sous la forme :
        code texte
        code texte
        ...
        :param eh: écart horizontal entre le code et le texte
        :param b: bordure latérale totale (en relatif : 0 à 1)
        :return: Renvoie une liste de rectangles
    """
    x, y, w, h = rect
    
    #
    # Réduction du rectangle
    #
    e = min(w*b, h*b)
    x, y = x+e, y+e
    w, h = w-2*e, h-2*e
    
    no = len(lstCodes)
    if no == 0:
        return []
    
    lstRect = []
#    maxFontSize = 0.012 * COEF
    maxFontSize = min(h / no * .8, 0.012 * COEF)
    # Equilibrage des tailles de font entre code et texte (approximatif)
#    nc = [len(c) for c in lstCodes]
#    nt = [len(t) for t in lstTexte]
    
    hl = h/no
    #
    # Calcul de la largeur maxi des codes
    #
    ctx.set_font_size(maxFontSize)
    ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_BOLD)
    
    wt = max([ctx.text_extents(t)[2] for t in lstCodes if t.strip() != ""])
#     wt = 0
#     for i, t in enumerate(lstCodes):
#         if t.strip() != "":
#             ctx.select_font_face (font_family, cairo.FONT_SLANT_NORMAL,
#                           cairo.FONT_WEIGHT_BOLD)
#             width = ctx.text_extents(t)[2]
#             wt = max(wt, width)
            
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
                
            show_text_rect(ctx, lstTexte[i], 
                           (x + wt + eh, y+i*hl, 
                            w - wt - eh, hl), 
                           b = 0, ha = 'g', va = va, 
                           fontsizeMinMax = (-1, maxFontSize))
            ly.append(y+i*hl)
            
            rect = (x, y+i*hl, w, hl)
            lstRect.append(rect)
            
            # Un rectangle invisible pour la séléction
            ep = ctx.get_line_width()
            co = ctx.get_source().get_rgba()
            ctx.set_line_width(0.0001 * COEF)
            ctx.set_source_rgba (0.5, 0.5, 0.5, 0.01)
            ctx.rectangle(*rect)
            
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
                           (x, ly[i], wt, hl), #y+i*hl, 
                           b = 0, ha = 'd', va = va, 
                           fontsizeMinMax = (-1, maxFontSize), wrap = False)
        
    
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
    

#def get_apercu_bmp(doc, mult = 3):
#    """ Renvoi un apercu du document <doc>
#        sous la forme d'une cairo.ImageSurface
#    
#    """
#    print "get_apercu", doc.draw
#    imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  210*mult, 297*mult)#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
#    ctx = cairo.Context(imagesurface)
#    ctx.scale(297*mult, 297*mult) 
#    doc.draw.Draw(ctx, doc)
#    bmp = wx.lib.wxcairo.BitmapFromImageSurface(imagesurface)
#        
#    # On fait une copie sinon ça s'efface ...
#    img = bmp.ConvertToImage()
#    bmp = img.ConvertToBitmap()
#        
#    return imagesurface

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
#  Un système de "cache" pour la fonction de découpe de lignes de texte
#
##########################################################################################
import functools

class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
       If called later with the same arguments, the cached value is returned
       (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, ctx, texte, w, break_long_words):
        
        if texte in list(self.cache.keys()) \
                and w >= max(self.cache[texte][0]) and w <= self.cache[texte][1] \
                and self.cache[texte][3] == break_long_words :
            if texte[:3] =='Syn': print("CACHE", self.cache[texte])
            return self.cache[texte][2], self.cache[texte][0]
        
        else:
            ll, lw = self.func(ctx, texte, w, break_long_words)
            self.cache[texte] = (lw, w, ll, break_long_words)
            return ll, lw
    
    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


@memoized
def decoupe_ligne(ctx, texte, w = None, couper = True):
    """ Découpe une ligne de texte en une liste de lignes
        de telle sorte qu'il rentre dans la largeur w
    """
    ll = []
    lw = []
    wrap = len(texte)
    continuer = wrap > 1
    while continuer:
        ll = textwrap.wrap(texte, wrap, break_long_words = couper)
        lw = [ctx.text_extents(t)[2] for t in ll]
        wmin = max(lw)

        if w == None or wmin <= w:
            continuer = False
        else:
            wrap -= 1#int((wmin-w)/2)
            if wrap <= 1:
                continuer = False
    return ll, lw


    
    
#def ajuster_texte3(ctx, texte, w, h, le = 0.8, pe = 1.0, wrap = True, couper = True):
#    """ Renvoie la liste des lignes et la taille de police et la longueur de la plus longue ligne
#        pour que <texte> rentre dnas le rectangle (w,h)
#        le = espacement vertical des lignes (1.0 = "normal")
#        pe = espacement vertical des paragraphes (1.0 = "normal")
#        
#        Options :
#            wrap = False : le texte reste sur une ligne
#            couper = False : les mots ne sont jamais coupés
#            
#        Renvoie : 
#            liste des lignes de texte
#            taille de police
#            largeur totale finale
#    """
#    debug = True#texte[:3] ==u'Les'
#    
#    #
#    # Estimation de l'encombrement du texte (pour une taille de police de 1)
#    # 
#    baseFontSize = min(w, h)
#    ctx.set_font_size(baseFontSize)
#    fheight = ctx.font_extents()[2]
#    hl = fheight * le
#
#    # Cas où on ne découpe pas le texte
#    if not wrap:
#        lt = [texte]
#        maxw = ctx.text_extents(texte)[2]
#        fontSize = min(w/maxw, h/hl) * COEF
#        
#        return lt, fontSize, maxw
#    
#    ratioRect = 1.0*w/h
#    lignes = texte.split("\n")
#    wmax = None
#    continuer = len(lignes) > 0
#    
#    old_fs = None
#    while continuer:
#        lt = []
#        wt = []
#        for l in lignes:
#            ll, lw = decoupe_ligne(ctx, l, wmax, couper)
#            lt.extend(ll)
#            wt.extend(lw)
#        
#        wobj = hl * len(lt) * ratioRect
#        
#        if wmax == wobj:
#            continuer = False
#        
#        wmax = max(wt)
#        
#        if debug: print lt, wt
#        if debug: print "   ", wmax, wobj
#        
#        ht = hl * len(lt)
#        fontSize = baseFontSize * min(h/ht, w/wmax)
#        if debug: print "   fontSize :", fontSize
#        
#        if abs(wmax - wobj) / wobj < 0.1:
#            continuer = False
#        
#        elif wobj > wmax:
#            continuer = False
#
#        else:
#            wmax = (wobj + wmax)/2
#            
#            if old_fs != None and fontSize < old_fs:
#                if debug: print "   <<", old_fs
#                fontSize = old_fs
#                lt = old_lt
#                wmax = max(old_wt)
#                continuer = False
#            else:
#                old_lt = list(lt)
#                old_wt = list(wt)
#                old_fs = fontSize
#        
#    
#    return lt, fontSize, wmax
#
#
#def ajuster_texte2(ctx, texte, w, h, le = 0.8, pe = 1.0, wrap = True, couper = True):
#    """ Renvoie la liste des lignes et la taille de police et la longueur de la plus longue ligne
#        pour que <texte> rentre dnas le rectangle (w,h)
#        le = espacement vertical des lignes (1.0 = "normal")
#        pe = espacement vertical des paragraphes (1.0 = "normal")
#        
#        Options :
#            wrap = False : le texte reste sur une ligne
#            couper = False : les mots ne sont jamais coupés
#            
#    """
#    debug = texte[:3] ==u'Syn'
#    if debug: print "wrapp", texte, w, h
#    if debug: print "  couper", couper
#    
#
#    #
#    # Estimation de l'encombrement du texte (pour une taille de police de 1)
#    # 
#    ctx.set_font_size(1.0 * COEF)
#    fheight = ctx.font_extents()[2]
#    hl = fheight * le
#
#    #
#    # Découpage du texte
#    #
#    i = 0
##    tps = time.time()
#    if wrap:
#        
#        ratioRect = 1.0*w/h
##        W = sqrt(1.0*width*hl*ratioRect)
#        
#        
#        
#        lignes = texte.split("\n")
#        
#        
#        #
#        # Calcul de la première largeur de coupe
#        #
#        lwrap = ctx.text_extents(texte)[2]
##        wrap1 = 0
##        
##        for l in lignes:
##            wrap1 = max(wrap1, len(l))
#        
##        print len(texte), texte
##        wrap = min(wrap1, max(1, int(len(texte)*W/width)*2))
##        print "   wrap initial :", wrap, "(brut :",int(len(texte)*W/width),")"
#        
#        ancienWrap = lwrap
#        ancienFontSize = 0
#        ancienLt = []
#        ancienMaxw = 0
#        i = 0
#        continuer = True
#        while continuer:
#            lt = []
#            wt = []
#            
#            # On découpe le texte
#            i += 1
#            for l in lignes:
#                ll, lw = decoupe_ligne(ctx, l, lwrap, couper)
#                lt.extend(ll)
#                wt.extend(lw)
#                
#            if lt == []:
#                return lt, 1, 0
#            if debug: print lt
#            if debug: print wt
#            # On mémorise la longueur de la plus longue ligne 
#            #    (en caractères et en unité Cairo)
#            maxw = max(wt)
##            maxl = max([len(t) for t in lt])
#
#            # On calcule la taille de police nécessaire pour que ça rentre
##            print lt, maxw, hl*len(lt)
#            fontSize = min(w/maxw, h/(hl*len(lt)))  * COEF
#            if debug: print "fontSize", fontSize
#            # On calcul le rapport des rapports h/w
#            rapport = maxw / (hl*len(lt)) / ratioRect
#            if debug: print maxw / (hl*len(lt))
#            
#            if not couper:
#                mot = lt[wt.index(maxw)]
#                if len(mot.split()) == 1:
#                    if debug: print "mot", mot
#                    continuer = False
#            
#            if rapport <= 1:  # on a passé le cap ...
#                continuer = False
#                if fontSize <= ancienFontSize:
#                    wrap = ancienWrap
#                    lt = ancienLt
#                    maxw = ancienMaxw
#                    fontSize = ancienFontSize
#            
#            else:
#                ancienWrap = lwrap
#                
#                lwrap = lwrap-fontSize
#                if debug: print "lwrap", lwrap
#                if lwrap <= fontSize:# or (maxw == ancienMaxw and wrap < maxl) :
#                    continuer = False
#                    
#                ancienFontSize = fontSize
#                ancienLt = lt
#                ancienMaxw = maxw
#            
#        
#    else:
#        lt = [texte]
#        maxw = ctx.text_extents(texte)[2]
#        fontSize = min(w/maxw, h/hl) * COEF
#        
#    if debug: print "   >>", i
#    return lt, fontSize, maxw
#
#
#def ajuster_texte4(ctx, texte, w, h, le = 0.8, pe = 1.0, wrap = True, couper = True):
#    """ Renvoie la liste des lignes et la taille de police et la longueur de la plus longue ligne
#        pour que <texte> rentre dnas le rectangle (w,h)
#        le = espacement vertical des lignes (1.0 = "normal")
#        pe = espacement vertical des paragraphes (1.0 = "normal")
#        
#        Options :
#            wrap = False : le texte reste sur une ligne
#            couper = False : les mots ne sont jamais coupés
#            
#    """
##    print "wrapp", texte, w, h
#
#    #
#    # Estimation de l'encombrement du texte (pour une taille de police de 1)
#    # 
#    ctx.set_font_size(1.0 * COEF)
#    fheight = ctx.font_extents()[2]
#    hl = fheight * le
#    
#    #
#    # Découpage du texte
#    #
#    i = 0
##    tps = time.time()
#    if wrap:
#        width = ctx.text_extents(texte)[2]
#        ratioRect = 1.0*w/h
#        W = sqrt(1.0*width*hl*ratioRect)
#        
#        continuer = True
#        
#        wrap1 = 0
#        st = texte.split("\n")
#        
#        
#        
#        for l in st:
#            wrap1 = max(wrap1, len(l))
#        
##        print len(texte), texte
#        wrap = min(wrap1, max(1, int(len(texte)*W/width)*2))
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
#            if lt == []:
#                return lt, 1, 0
#        
#            # On mémorise la longueur de la plus longue ligne 
#            #    (en caractères et en unité Cairo)
#            maxw = maxl = 0
#            for t in lt:
#                maxw = max(maxw, ctx.text_extents(t)[2])
#                maxl = max(maxl, len(t))
#            
#            # On calcule la taille de police nécessaire pour que ça rentre
##            print lt, maxw, hl*len(lt)
#            fontSize = min(w/maxw, h/(hl*len(lt)))  * COEF
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
#        
#    else:
#        lt = [texte]
#        maxw = ctx.text_extents(texte)[2]
#        fontSize = min(w/maxw, h/hl) * COEF
#        
#    return lt, fontSize, maxw




def ajuster_texte(ctx, texte, w, h, le = 0.8, pe = 1.0, b = 0.4, 
                  wrap = True, couper = True, debug = False):
    """ Ajuste le <texte> dans un rectangle <w,h>
        
        le = espacement vertical des lignes (1.0 = "normal") = période en Y
        (pe = espacement vertical des paragraphes (1.0 = "normal")) pas utilisé !
        b = écart avec les bords du rectangle (1.0 = 1em)
        
        Options :
            wrap = False : le texte reste sur une ligne
            couper = False : les mots ne sont jamais coupés
            
        Renvoie :
            liste des lignes
            taille de la police
            taille du rectangle effectif (W, H) SANS BORDURE
    """
    
    
    #
    # On vérifie dans le cache qu'on n'a pas déja fait le boulot
    #
    if texte in list(CACHE.keys()):
        www, hhh, bbb, lee, pee, lt, fontSize, wh = CACHE[texte]
        if www == w and hhh == h and lee == le and pee == pe and bbb == b:
            return lt, fontSize, wh
            
    #
    # Options de débuggage
    #
#     debug = texte == u'Les projets pédagogiques et technologiques'
    if debug: print("ajuster_texte", texte, w, h)
    if debug: print("  couper :", couper)


    #
    # Estimation de l'encombrement du texte (pour une taille de police de 1)
    # 
    ctx.set_font_size(1.0 * COEF)
    fheight = ctx.font_extents()[2]

    hl = fheight * le
    if debug: print("  hl", hl)
    
    ecart = b * fheight * 2     # écart "total" (gauche + droite)
    if debug: print("  ecart", ecart)
    
    # Ratio du rectangle, écarts compris
    ratioRect = w/h
    
    #
    # Découpage du texte
    #
    i = 0
#    tps = time.time()
    if wrap:
        width = ctx.text_extents(texte)[2]              
        if debug: print("  width", width)
        
        pas = ctx.text_extents('a')[2] # Largeur "type"
        lignes = texte.splitlines()
        
        ancienWrap = width
        ancienLt = []
        ancienMaxw = 0
        ancienRapport = 0
        
        continuer = True
        ptes = [[ctx.text_extents(l[:i+1])[2] for i in range(len(l))] for l in lignes] 
        i = 0
        while continuer:
            lt = []
            
            # On découpe le texte
            i += 1
            
            for l, pte in zip(lignes, ptes):
                lt.extend(wordwrap(ctx, l, width, pte, breakLongWords = couper))
                
            if lt == []:
                return lt, 1, 0
            
            if debug: print()
            if debug: print("  lt", lt)
            
            # On mémorise la longueur de la plus longue ligne 
            #    (en caractères et en unité Cairo)
            maxw = calcul_largeur(ctx, lt)
            if debug: print("  maxw", maxw)
            
            ht = calcul_hauteur(fheight, le, len(lt))
            W, H = maxw + ecart, ht + ecart         # Echelle "1"
            rapport = (W/H) / ratioRect
            if debug: print("  rapports", maxw/ht, "/", ratioRect)
             
            if rapport <= 1:  # on a passé le cap ...
                continuer = False
#                if debug: print "  fontSize", fontSize, ancienFontSize
                
                if i > 1 and abs(ancienRapport-1) < abs(rapport-1):#fontSize <= ancienFontSize:
                    width = ancienWrap
                    lt = ancienLt
                    maxw = ancienMaxw
#                    fontSize = ancienFontSize
 
            else:
                ancienWrap = width
                width = width-pas
                if width <= pas:# or (maxw == ancienMaxw and wrap < maxl) :
                    continuer = False
                     
#                ancienFontSize = fontSize
                ancienLt = lt
                ancienMaxw = maxw
                ancienRapport = rapport
            
    #
    # Pas de découpage du texte
    #
    else:
        lt = texte.splitlines()
        maxw = calcul_largeur(ctx, lt)

#         c = max((maxw+ecart)/w, (hl*len(lt)+ecart)/h)
#         ratioRect = (w*c)/(h*c)
    
    if debug: print("   >>", i)
    

    #
    # Ajustement de la taille de police
    #
    ht = calcul_hauteur(fheight, le, len(lt))
    W, H = maxw + ecart, ht + ecart         # Echelle "1"
    fontSize = min(w/W, h/H)
    
#     W, H = W*fontSize, H*fontSize          # Echelle "reele"
    W, H = maxw*fontSize, ht*fontSize        # Echelle "reele"
    
    fontSize *= COEF
    if debug: print("  >>> fontSize :", fontSize)
    
    #
    # On met le résultat du calcul dans le cache
    #
    CACHE[texte] = (w, h, b, le, pe, lt, fontSize, (W, H))
    
    return lt, fontSize, (W, H)




def ajuster_texte_fixe(ctx, texte, w, h, 
                       fontSize,
                       le = 0.8, pe = 1.0, 
                       wrap = True, couper = True, debug = False):
    """ Ajuste le <texte> dans un rectangle <w,h>
        pour une taille de police fixée
        
        le = espacement vertical des lignes (1.0 = "normal") = période en Y
        (pe = espacement vertical des paragraphes (1.0 = "normal")) pas utilisé !
        
        Options :
            wrap = False : le texte reste sur une ligne
            couper = False : les mots ne sont jamais coupés
            
        Renvoie :
            liste des lignes
            taille de la police
            taille du rectangle effectif (W, H) SANS BORDURE
    """
            
    #
    # Options de débuggage
    #
#     debug = texte == u'Les projets pédagogiques et technologiques'
    if debug: print("ajuster_texte", texte, w, h)
    if debug: print("  couper :", couper)


    #
    # Estimation de l'encombrement du texte (pour une taille de police de 1)
    # 
    ctx.set_font_size(fontSize)
    fheight = ctx.font_extents()[2]

    hl = fheight * le
    if debug: print("  hl", hl)
        
    #
    # Découpage du texte
    #
    if wrap:
        lignes = texte.splitlines()
#         print(lignes)
        ptes = [[ctx.text_extents(l[:i+1])[2] for i in range(len(l))] for l in lignes]
#         ptes = []
#         for l in lignes:
#             ll = []
#             for i in range(len(l)):
#                 try:
#                     ll.append(ctx.text_extents(l[:i+1])[2])
#                 except:
#                     ll.append(0)
#                     print("E", l[:i+1])
#             ptes.append(ll)
#         print(ptes)
        lt = []
        for l, pte in zip(lignes, ptes):
            lt.extend(wordwrap(ctx, l, w, pte, breakLongWords = couper))
    
    #
    # Pas de découpage du texte
    #
    else:
        lt = texte.splitlines()

    
    #
    # Tronquage éventuel du texte
    #
    continuer = True
    while continuer:
        ht = calcul_hauteur(fheight, le, len(lt))
        if ht <= h:
            continuer = False
        elif len(lt) == 1:
            continuer = False # à gérer !!!
        else:
            lt = lt[:-1]
        
    maxw = calcul_largeur(ctx, lt)
    
    return lt, fontSize, (maxw, ht)



# def ajuster_texte(ctx, texte, w, h, le = 0.8, pe = 1.0, b = 0.4, wrap = True, couper = True):
#     """ Renvoie la liste des lignes, la taille de police et la longueur de la plus longue ligne
#         pour que <texte> rentre dans le rectangle (w,h)
#         le = espacement vertical des lignes (1.0 = "normal")
#         pe = espacement vertical des paragraphes (1.0 = "normal")
#         
#         Options :
#             wrap = False : le texte reste sur une ligne
#             couper = False : les mots ne sont jamais coupés
#             
#     """
#     debug = False#texte[:3] ==u'Lyc'
#     if debug: print "ajuster_texte", texte, w, h
#     if debug: print "  couper", couper
# 
# 
#     #
#     # Estimation de l'encombrement du texte (pour une taille de police de 1)
#     # 
#     ctx.set_font_size(1.0 * COEF)
#     fheight = ctx.font_extents()[2]
# 
#     hl = fheight * le
#     if debug: print "  hl", hl
#     ecart = b * hl
#     if debug: print "  ecart", ecart
#     ratioRect = 1.0*w/h
#     
#     #
#     # Découpage du texte
#     #
#     i = 0
# #    tps = time.time()
#     if wrap:
#         width = ctx.text_extents(texte)[2]
#         if debug: print "  width", width
#         
#         pas = ctx.text_extents('a')[2]
#         lignes = texte.splitlines()#("\n")
#         
#         ancienWrap = width
# #        ancienFontSize = 0
#         ancienLt = []
#         ancienMaxw = 0
#         ancienRapport = 0
#         continuer = True
#         ptes = [[ctx.text_extents(l[:i+1])[2] for i in range(len(l))] for l in lignes] 
#         i = 0
#         while continuer:
#             lt = []
#             
#             # On découpe le texte
#             i += 1
#             
#             for l, pte in zip(lignes, ptes):
#                 lt.extend(wordwrap(ctx, l, width, pte, breakLongWords = couper))
#                 
#             if lt == []:
#                 return lt, 1, 0
#             if debug: print
#             if debug: print "  lt", lt
#             # On mémorise la longueur de la plus longue ligne 
#             #    (en caractères et en unité Cairo)
#             maxw = max([ctx.text_extents(t)[2] for t in lt])
# #            maxw = 0
# #            for t in lt:
# #                maxw = max(maxw, ctx.text_extents(t)[2])
# #                maxl = max(maxl, len(t))
#             if debug: print "  maxw", maxw
#             # On calcule la taille de police nécessaire pour que ça rentre
# #            print lt, maxw, hl*len(lt)
# #            fontSize = min(w/maxw, h/(hl*len(lt))) * COEF
# #            if debug: print "  fontSize", fontSize
#             # On calcul le rapport des rapports h/w
#             
#             
#             c = max(maxw/w, hl*len(lt)/h)
# #            c = 1
#             if debug: print "  c, w, h", c, w, h
#             ratioRect = (w*c-ecart)/(h*c-ecart)
#             if debug: print "  r", w/h, ratioRect
#             rapport = (maxw / (hl*len(lt))) / ratioRect
# #            fontSize = min(w/maxw, h/(hl * len(lt))) * COEF
#             
#             if debug: print "  rapports", maxw / (hl*len(lt)), "/", ratioRect
#             if rapport <= 1:  # on a passé le cap ...
#                 continuer = False
# #                if debug: print "  fontSize", fontSize, ancienFontSize
#                 
#                 
# #                if i > 1 and fontSize < ancienFontSize:
#                 if i > 1 and abs(ancienRapport-1) < abs(rapport-1):#fontSize <= ancienFontSize:
#                     width = ancienWrap
#                     lt = ancienLt
#                     maxw = ancienMaxw
# #                    fontSize = ancienFontSize
# 
#             else:
#                 ancienWrap = width
#                 width = width-pas
#                 if width <= pas:# or (maxw == ancienMaxw and wrap < maxl) :
#                     continuer = False
#                     
# #                ancienFontSize = fontSize
#                 ancienLt = lt
#                 ancienMaxw = maxw
#                 ancienRapport = rapport
#             
#         
#     else:
#         lt = texte.splitlines()
#         maxw = max([ctx.text_extents(t)[2] for t in lt])
#         c = max(maxw/w, hl*len(lt)/h)
#         ratioRect = (w*c-ecart)/(h*c-ecart)
# #        fontSize = min(w/maxw, h/hl) * COEF
#     
#     if debug: print "   >>", i
#     
#     return lt, ratioRect, maxw

#########################################################################################################################
def info(ctx, margeX, margeY):
    #
    # Informations
    #
    ctx.select_font_face (font_family, cairo.FONT_SLANT_ITALIC, #"Sans"
                     cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size (0.007 * COEF)
    ctx.set_source_rgb(0.6, 0.6, 0.6)
    ctx.move_to (margeX, 1 * COEF - margeY + 0.02 * COEF)
    ctx.show_text ("Fiche créée avec le logiciel pySequence (https://github.com/cedrick-f/pySequence)")



#----------------------------------------------------------------------
#
# wordwrap
#
# Adaptation du code :
# Name:        wx.lib.wordwrap
# Author:      Robin Dunn
#----------------------------------------------------------------------

def wordwrap(ctx, text, width, pte, breakLongWords=True):
    """
    Returns a copy of text with newline characters inserted where long
    lines should be broken such that they will fit within the given
    width, with the given margin left and right, on the given `wx.DC`
    using its current font settings.  By default words that are wider
    than the margin-adjusted width will be broken at the nearest
    character boundary, but this can be disabled by passing ``False``
    for the ``breakLongWords`` parameter.
    """
    debug = False#text[:3] ==u'Ést'
#    if debug: print "wordwrap", width, text
   
#    pas = ctx.text_extents('a')[2]
    
#    wid = width - pas - max([0] + [pte[i]-pte[i-1] for i in range(1,len(pte))])
#    width += 3*pas
    wid = width

    wrapped_lines = []
    if debug: print("<<", text.splitlines())
    if debug: print("<<", text.split("\n"))
    if debug: print(type(text.splitlines()[0]), type(text.split("\n")[0]))
    text = text.splitlines()
    
#    text = text.split("\n")
    
    for line in text:
        idx = 0
        start = 0
        startIdx = 0
        spcIdx = -1
        if debug: print("  line", type(line), line)
        if debug: print("  pte", pte)
        while idx < len(pte):
            if debug: print("  idx", idx)
            # remember the last seen space
            if line[idx] == ' ':
                spcIdx = idx

            # have we reached the max width?
            if pte[idx] - start > wid and (spcIdx != -1 or breakLongWords):
                if spcIdx != -1:
                    idx = min(spcIdx + 1, len(pte) - 1)
                wrapped_lines.append(line[startIdx : idx])
                start = pte[idx]
                startIdx = idx
                spcIdx = -1

            idx += 1

        wrapped_lines.append(line[startIdx : idx])

    return wrapped_lines




##########################################################################################
#
#  Une zone active sur le dessin
#
##########################################################################################
class Zone():
    def __init__(self, rect, pt_caract = None, obj = None, param = None):
        self.rect = rect                # Le(s) rectangle(s) sensible(s) (liste)
        if pt_caract == None:
            pt_caract = self.rect[:2]
        self.pt_caract = pt_caract      # Un point caractéristique (pour identification svg)
        self.obj = obj                  # L'objet concerné
        self.param = param              # Paramètre(s) supplémentaire(s)
        
    def __repr__(self): 
        return "%s (%s)" %(self.obj, self.param)
    
    def dansRectangle(self, X, Y):
        """ Renvoie True si le point X, Y est dans la zone
        """
        for r in self.rect:
            x, y, w, h = r
            if X > x and Y > y and X < x + w and Y < y + h:
                return True
        return False
    
    
    
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


