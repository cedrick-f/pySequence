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
import os, io, sys
import tempfile
# import cairo
import wx.lib.wxcairo
import cairo
# import cairocffi as cairo

# import time
try:
    import constantes
except:
    pass

## Pour afficher des images

import wx

from widgets import getHoraireTxt

import couleur
import configparser
import util_path
from proprietes import *
                                     
#
# Coefficient de multiplication global
#
COEF = 1000.0

DEBUG = False
LOG = False
FSIZE_BASE = 10


#
# Données pour le tracé
#

minFont = 0.006 * COEF
maxFont = 0.1 * COEF
# font_family = "sans-serif"##"Purisa"#"DejaVu Sans Mono"#"arial"#



# def my_except_hook(exctype, value, traceback):
#     if exctype == cairo.CairoError:
#         print("cairocffi.CairoError")
#     else:
#         sys.__excepthook__(exctype, value, traceback)
# sys.excepthook = my_except_hook



    
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




##########################################################################################
#
#  Conversion des imagesSurfaces
#
##########################################################################################

##########################################################################################
def getBitmapFromImageSurface(imagesurface):
    """ Renvoi une wx.Bitmap en fonction d'une cairo.ImageSurface
    """
    # On fait une copie sinon ça s'efface ...
#     bmp = wx.lib.wxcairo.BitmapFromImageSurface(imagesurface)
#     return bmp.GetSubBitmap(wx.Rect(0, 0, bmp.GetWidth(), bmp.GetHeight()))
    return wx.lib.wxcairo.BitmapFromImageSurface(imagesurface).ConvertToImage().ConvertToBitmap()


##########################################################################################
def getBase64PNG(surface):
    data = io.BytesIO()
    surface.write_to_png(data)
    return data.getvalue()




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
    fascent, fdescent = ctx.font_extents()[:2]
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
   
def reduire_rect(x, y, w, h, b, maxi = 0.3):
    """ Réduction d'un rectangle : suppression de la bordure
    
        :x, y, w, h: rectangle
        :b: coefficient de bordure : float de 0 à maxi
        
        Renvoie :
            rectangle réduit
    """
    if b > maxi:
        b = maxi
    ecartx = w * b
    ecarty = h * b
    x += ecartx
    y += ecarty
    w -= 2*ecartx
    h -= 2*ecarty
    return x, y, w, h




def calcul_hauteur(fheight, descent, le, nl):
    """ Calcul la hauteur effective d'un texte
    
        :fheight: hauteur de la police
        :descent: espace sous la ligne de référence
        :le: coefficient d'inter-ligne
        :nl: nombre de lignes du texte
    """
    return fheight*le*nl+descent




def calcul_largeur(ctx, lt):
    """ Calcul la largeur effective d'un texte
        :lt: liste des lignes du texte
    """
    return max([text_extents(ctx, t)[2] for t in lt])



def show_text_rect(ctx, texte, rect, \
                   va = 'c', ha = 'c', le = 0.8, pe = 1.0, \
                   b = 0.05, orient = 'h', \
                   fontsizeMinMax = (-1, -1), fontsizePref = -1,
                   coulBord = None, ext = "...",
                   tracer = True, forcer = True, wrap = True, couper = True, 
                   ):
    """ Affiche un texte en adaptant la taille de police et sa position
        pour qu'il rentre dans le rectangle
        x, y, w, h : position et dimensions du rectangle
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        b : écart mini du texte par rapport au bord (relativement aux dimensionx du rectangle)
        orient : orientation du texte ('h', 'v')
        max_font : taille maxi de la font
        min_font : le texte peut être tronqué (1 ligne)
        
        :tracer: pour tracé en différé (quand taille fixe par exemple)
        :forcer: mettre à False pour éviter les débordements quand pas la place --> pas d'affichage
        
        
        le, pe : coefficient d'inter-ligne et inter-paragraphe
        
        Retourne : 
            Rectangle "effectif" (encadrant le texte au plus près)
            Liste des lignes de texte
    """
#     DEBUG = "Fabrication" in texte
    #texte[:3] ==u'Ést'
    if DEBUG:
        print("show_text_rect", texte[:20]+"...", rect)
    
    if texte == "":
        return 0, rect, [texte]
    
    #
    #    Retournement Horizontal >> Vertical
    #
    if orient == 'v':
        ctx.rotate(-pi/2)
        x, y, w, h = rect
        r = (-y-h, x, h, w)
        f, r, lt = show_text_rect(ctx, texte, r, va, ha, le, pe, 
                               b, fontsizeMinMax = fontsizeMinMax, fontsizePref = fontsizePref, 
                               wrap = wrap, couper = couper, coulBord = coulBord, tracer = tracer)
        ctx.rotate(pi/2)
        return f, r, lt
    
    
    # Réduction du rectangle
    x, y, w, h = reduire_rect(*rect, b)
    
    # Intervalle de taille de font
    fontsizeMinMax = [fontsizeMinMax[0], fontsizeMinMax[1]]
    if fontsizeMinMax[0] == -1:
        fontsizeMinMax = [minFont, fontsizeMinMax[1]]
    if fontsizeMinMax[1] == -1:
        fontsizeMinMax = [fontsizeMinMax[0], maxFont]
        
    if DEBUG: print("   fontsizeMinMax :", fontsizeMinMax)
    
    
#     if ctx.get_font_matrix().xx != FSIZE_BASE:
#         text_extents.cache.Clear()
    ctx.set_font_size(FSIZE_BASE) # FSIZE_BASE : valeur arbitraire
    
    fascent, fdescent, fheight = ctx.font_extents()[:3]
    
    
#     # Calcul du nombre maximum de lignes
#     nLignesMaxi = max(1, h // (fheight * le))

    fontsizeMin, fontsizeMax = fontsizeMinMax
    
    #
    # Calcul ...
    #
    
    lt, W, H = ajuster_texte(ctx, texte, w, h,
                             fdescent, fheight,
                             le, pe, 
                             wrap, couper)
    
    if lt == []: # pas de texte
        return 0, (x, y, 0,0), lt
        
    if DEBUG: print("lignes :", lt)
    # Coefficient de mise à l'échelle
    coef = min(h/H, w/W)
    if DEBUG: print("coef :", coef)
    
    #
    # Vérification que la taille de la police est dans l'intervale
    #
    fontSize = FSIZE_BASE*coef
#     
    if fontSize > fontsizeMax:
#         print("   fontSize maxi !", fontSize, fontsizeMax, texte)
        
        # Réglage taille selon taille préférée
        if fontsizePref > 0:
            fontSize = max(fontsizeMax * fontsizePref/100, fontsizeMin)
        else:
            fontSize = fontsizeMax
          
        if not tracer:
            return 0, (x, y, 0, 0), []
          
        rect_eff, lt = show_text_rect_fix(ctx, texte, rect, 
                                          fontSize = fontSize, b = b, 
                                          va = va, ha = ha, le = le, pe = pe,
                                          coulBord = coulBord, wrap = wrap, couper = couper,
                                          ext = ext)
        return fontSize, rect_eff, lt

    if fontSize < fontsizeMin:
#         print("   fontSize mini !", fontSize, fontsizeMin)
        if not tracer or not forcer:
            return 0, (x, y, 0, 0), []
          
        rect_eff, lt = show_text_rect_fix(ctx, texte, rect, 
                                          fontSize = fontSize, b = b,
                                          va = va, ha = ha, le = le, pe = pe,
                                          coulBord = coulBord, wrap = wrap, couper = couper,
                                          ext = ext)
        return fontSize, rect_eff, lt
    
    
    
    #
    # Positionnement du rectangle englobant effectif dans le rectangle contenant
    #
    
    # Position (haut, bas, gauche, droite, centré)
    # --> rectangle englobant échelle réelle
    ecartx = (w-coef*W)/2
    ecarty = (h-coef*H)/2
    if DEBUG: print("ecartx, ecarty :", ecartx, ecarty)
    
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
        
    if DEBUG: print("rect :", x, y, coef*W, coef*H)
    
            
#    if DEBUG: print "   nLignes :", nLignes
#     ctx.set_font_size(fontSize)
    
#     #
#     # 2 ème tour
#     #
#     maxw = 0
#     for t in lt:
#         width = ctx.text_extents(t)[2]
#         maxw = max(maxw, width)
#     fontSize = min(fontSize, fontSize*w/maxw)
#     
#     # Réglage taille selon taille préférée
#     if fontsizePref > 0:
#         fontSize = max(fontSize * fontsizePref/100, fontsizeMinMax[0])
#     if DEBUG: print("   fontSize 4 :", fontSize, va)
#     
    if not tracer:
        return fontSize, (x, y, W,H), lt
# 
#     if DEBUG: print("   H", h)
    
    
    # Affichage des lignes sur un calque séparé
    ctx.save()
    ctx.translate(x, y)  
    ctx.scale(coef, coef)
    
    
    X = show_lignes(ctx, lt, W, H, 
                       fascent, fheight, 
                       le, ha = ha, coulBord = coulBord)
    
    ctx.restore()
    
    
    if DEBUG: print("FIN show_text_rect\n")
    
    return fontSize, (x+X, y, coef*W, coef*H), lt



    

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




##########################################################################################################################
def show_text_rect_fix(ctx, texte, rect, fontSize, \
                   va = 'c', ha = 'c', le = 0.8, pe = 1.0, \
                   b = 0.05, orient = 'h', \
                   coulBord = None, ext = "...",
                   wrap = True, couper = True, 
                   ):#, outPosMax = False):
    """ Affiche un texte 
            (en tronquant sa longueur s'il le faut
             pour qu'il rentre dans le rectangle)
             
        rect : position et dimensions du rectangle
        fontSize : taille de la police
        va, ha : alignements vertical et horizontal ('h', 'c', 'b' et 'g', 'c', 'd')
        coulBord : coulBord = couleur de la bordure (pas de bordure si None)
        
        
        Retourne :
            Rectangle "effectif" (encadrant le texte au plus près)
            Liste des lignes de texte
    """
#     print "show_text_rect_fix", texte

    if texte == "":
        return rect, [texte]
    
#     DEBUG = texte == "Séchoir solaire autonome"
    if DEBUG: print("!!! ", texte)
    if DEBUG: print("    ", fontSize)
    
    #
    #    Retournement Horizontal >> Vertical
    #
    if orient == 'v':
        ctx.rotate(-pi/2)
        x, y, w, h = rect
        r = (-y-h, x, h, w)
        r, lt = show_text_rect_fix(ctx, texte, r, 
                                   va, ha, le, pe, 
                                   b, fontsize = fontSize, 
                                   wrap = wrap, couper = couper, 
                                   coulBord = coulBord)
        ctx.rotate(pi/2)
        return r, lt
    
    
    # Réduction du rectangle
    x, y, w, h = reduire_rect(*rect, b)
    
#     if ctx.get_font_matrix().xx != fontSize:
#         text_extents.cache.Clear()
    ctx.set_font_size(fontSize)
    fascent, fdescent, fheight = ctx.font_extents()[:3]
    
    # Période entre 2 lignes
#     hl = fheight * le
    
    if DEBUG: print(w, h)
    lt, W, H = ajuster_texte_fixe(ctx, texte, w, h, 
                                  fdescent, fheight,
                                  le = le, pe = pe, 
                                  wrap = wrap, couper = couper)
    
    if DEBUG: print(W, H)
    
    
    #
    # Ajustement du rectange "ajusté" dans le rectangle
    #
    # taille du rectangle "ajusté"
    ecartx = (w-W)/2
    ecarty = (h-H)/2
#     w, h = wh
    
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
    
    
    # Affichage des lignes sur un calque séparé
    ctx.save()
      
#     ctx.scale(coef, coef)
    ctx.translate(x, y)
    
    X = show_lignes(ctx, lt, W, H, 
                       fascent, fheight, 
                       le, ha = ha, coulBord = coulBord,
                       cacher = False)
    
    ctx.restore()
    
    
    return (x+X, y, W, H), lt





#########################################################################################################################
def show_lignes(ctx, lignes, w, h,
                fascent, fheight,
                le, ha = 'g', 
                coulBord = None, 
                cacher = True):
    """ Affiche une série de lignes de texte
        Renvoie la position la plus extrème à droite
        (pour éventuellement écrire une suite au texte)
        
        w, h : dimensions du rectangle "effectif" englobant
        le : espacement relatif des lignes
        ha : alignements horizontal ('g', 'c', 'd')

        coulBord = couleur de la bordure (pas de bordure si None)
        
        La taille de la police doit être définie au préalable.
        
        Renvoie : 
        Position du rectangle effectif (encadrant le texte au plus juste)
    """

    # Période entre 2 lignes
    hl = fheight * le
    
#     DEBUG = "Fabrication" in lignes[0]
#     if DEBUG: print(lignes)
    #
    # On dessine toutes les lignes de texte
    #
    X = 0
    for l, t in enumerate(lignes):
#        print "  ",t
        if cacher:
            xbearing, _, width, *_ = text_extents(ctx, t)
        else:
            xbearing, _, width, *_ = ctx.text_extents(t)
        # Position du rectangle encadrant la ligne
        if ha == 'c' or ha == 'j':
            xt = (w-width)/2
        elif ha == 'g':
            xt = 0
        elif ha == 'd':
            xt = w-width

        
        yt = hl*l
        
        X = min(X, xt)
        
        # Coordonnées du point de référence
        xt -= xbearing
        yt += fascent
        ctx.move_to(xt, yt)
        
        if coulBord == None:
            ctx.show_text(t)
          
        else:
            ctx.text_path(t)
            ctx.fill_preserve()
            ctx.set_source_rgb(*coulBord)
            ctx.set_line_width(fheight/30)
        
    ctx.stroke()
    #########
    
    return X





#########################################################################################################  
#
#    Représentation des périodes d'un enseignement (années, trimestres, ...)
#
######################################################################################################### 
# BcoulPos = []
# IcoulPos = []
# ICoulComp = []
# CoulAltern = []
# fontPos = 0.014 * COEF 
# 
# ######################################################################################  
# def DefinirCouleurs(n1, n2, n3):
#     global IcoulPos, BcoulPos, CoulAltern
#     couleur.generate(IcoulPos, [0xFFC3D0E2, 0xFFF2C5B5], n1)
#     couleur.generate(BcoulPos, [0xFF82AAE0, 0xFFEF825D], n1)
#     
#     couleur.generate(ICoulComp, [0xFFFF6666, 0xFFFFFF66, 0xFF75FF66, 0xFF66FFF9, 0xFFFF66F4], n2)
#     
#     del CoulAltern[:]
#     for n in range(n3//2+1):
#         CoulAltern += [((0.85, 0.85, 0.95, 0.3),    (0, 0, 0, 1)),
#                        ((0.7,  0.7,  0.8,  0.2),    (0, 0, 0, 1))]


import calendar
from datetime import date

######################################################################################  
def est_ferie(Date, creneaux):
    for c in creneaux:
        if c[0] < Date < c[1]:
            return True
    return False


######################################################################################  
#
# Fiche cairo Document de base
#
######################################################################################  
class Base_Fiche_Doc():
    def __init__(self):
        # Marges
        self.margeX = 0.02 * COEF
        self.margeY = 0.04 * COEF
        
        # Ecarts
        self.ecartX = 0.02 * COEF
        self.ecartY = 0.02 * COEF

        self.LargeurTotale = 0.72414 * COEF# Pour faire du A4

        self.font_family = "arial"#"sans-serif"##"Purisa"#"DejaVu Sans Mono"#"Georgia"#
    
        self.surRect = None
    
    
    ######################################################################################  
    def getGroupes(self):
        return {}
    
    
    ######################################################################################  
    def getSSGroupes(self):
        return {}
    
    
    
    ########################################################################################            
    def initOptions(self, ctx):#
        # Options générales
        #
        options = ctx.get_font_options()
        options.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        options.set_hint_style(cairo.HINT_STYLE_NONE)#cairo.HINT_STYLE_FULL)#
        options.set_hint_metrics(cairo.HINT_METRICS_OFF)#cairo.HINT_METRICS_ON)#
        ctx.set_font_options(options)


    #########################################################################################################################
    def info(self, ctx):
        #
        # Informations
        #
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_ITALIC, #"Sans"
                         cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size (0.007 * COEF)
        ctx.set_source_rgb(0.6, 0.6, 0.6)
        ctx.move_to (self.margeX, 1 * COEF - self.margeY + 0.02 * COEF)
        ctx.show_text ("Fiche créée avec le logiciel pySequence (https://github.com/cedrick-f/pySequence)")


#     #######################################################################################
#     # Gestion des paramètres sauvegardables
#     #####################################################################################
#     def getParametres(self):
#         """ Renvoi un dict {nom: valeur} des paramètres à sauvegarder
#              - couleurs
#              - ...
#         """
#         d = {}
#         for n, v in globals().items():
#     #         print(n)
#             if "coul_" in n:
#                 d[n] = couleur.CouleurFloat2CSS(v)
#         return d
    
    
    ##########################################################################################
    def getImageSurface(self, larg, prop = 0.7071, **kargs):
        """ Renvoi un apercu du document <doc>
            sous la forme d'une cairo.ImageSurface
        
        """
    #    print "get_apercu", larg, prop
        w, h = 0.04*prop * COEF, 0.04 * COEF
        imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  int(larg), int(1.0*larg/prop))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        ctx = cairo.Context(imagesurface)
        s = 1.0*larg/prop/COEF
        ctx.scale(s, s) 
    #    ctx.scale(mult, mult) 
#         doc.DefinirCouleurs()
#         doc.draw.Draw(ctx, doc, entete = entete)
        self.rect = (0,0,w,h)
        self.draw(ctx, **kargs)
        del ctx
             
        return imagesurface


    ########################################################################################            
    def getBitmap(self, *args, **kargs):
        i = self.getImageSurface(*args, **kargs)
        return getBitmapFromImageSurface(i)
    
    
    ########################################################################################            
    def getBase64PNG(self, *args, **kargs):
        return getBase64PNG(self.getImageSurface(*args, **kargs))
    

    ##########################################################################################
    def chargerParametres(self):
#         print("chargerParametres", self.__dict__)
        if self.getDocument() is not None:
            
            for code, prop in self.getDocument().proprietes.proprietes.items():
                code = "p_"+code
#                 print("   ", prop)
                if len(code.split(".")) == 2:
                    code, sgrp = code.split(".")
                    d = getattr(self, code+"_")
                    d[sgrp] = prop.value
                    
                elif code in self.__dict__ and hasattr(prop, 'value'):
#                     print("      ", code, prop.value)
                    setattr(self, code, prop.value)
                
#                 elif "." in code:
#                     code, k = code.split(".", 1)
#                     if code in self.__dict__ and hasattr(prop, 'value'):
#                         print("      ++", code, k, prop.value)
#                         d = getattr(self, code)
#                         d[k] = prop.value



    #####################################################################################
    def getParametres(self):
        """ Renvoi une dict de {code : proprietes.Propriete}
            des paramètres à sauvegarder
             - couleurs
             - ...
        """
        l = {}
        
#         noms_grp = {"CI" : "Centres d'intêret",
#                     "Obj" : "Objectifs",
#                     }
        
        for n, v in self.__dict__.items():
            if len(n) > 2 and n[:2] =="p_":   # attribut à mettre en "paramètres réglables"
                typ, grp = n[2:].split("_", 1)
                if grp[-1] == "_":
                    grp = grp[:-1]
                    cod = n[2:-1]+"."
                    for sgrp, sv in v.items():
                        l[cod+sgrp] = Propriete(cod+sgrp, 
                                                  cod+sgrp, sv, typ, 
                                                  cat = "1", 
                                                  grp = grp, sgrp = sgrp)
                
                else:
                    l[n[2:]] = Propriete(n[2:], n[2:], v, typ, 
                                 cat = "1", grp = grp)
                
        return l




    ##########################################################################################
    def associerParametres(self):
        """ Renvoi une lite de proprietes.PropPropriete des paramètres à sauvegarder
             - couleurs
             - ...
        """
#         print("associerParametres")
#         print("   proprietes2", self.seq.proprietes.proprietes)

        if self.getDocument() is not None:
            self.getDocument().proprietes.update(self.getParametres(),
                                                 self.getGroupes(),
                                                 self.getSSGroupes())

        
    #############################################################################            
    def getRects(self, obj):
        """ Renvoie la liste des rectangles encadrant l'objet <obj>
        """
        r = []
        for z in self.getDocument().zones_sens:
            if z.obj == obj:
                r.extend(z.rect)
        return r
    
    
    ##########################################################################################
    def surBrillance(self, ctx, surObj):
        
        def surbrillance(rect = None):
            if rect is not None:
                ctx.rectangle(*rect)
                ctx.set_source_rgba (1,1,0.3, 0.3)
                ctx.fill_preserve ()
                ctx.set_source_rgba (1,1,0.3, 1)
                ctx.stroke ()
                
        if surObj is not None:
            self.surRect = self.getRects(surObj)
            
        if self.surRect is not None:
#             print("Surbrillance", self.surRect)
            if type(self.surRect) == list:
                for r in self.surRect:
        #             print("   ", r)
                    surbrillance(r)
            elif hasattr(self.surRect, 'rect'):
                for r in self.surRect.rect:
        #             print("   ", r)
                    surbrillance(r)
        
    
            
            
            
#     #######################################################################################
#     # Gestion des paramètres sauvegardables
#     #####################################################################################
#     def getParametres(self):
#         """ Renvoi un dict {nom: valeur} des paramètres à sauvegarder
#              - couleurs
#              - ...
#         """
#         return {n : couleur.CouleurFloat2CSS(v) for n, v in globals().items() if "coul" in n}
# 
#     ##########################################################################################
#     def chargerParametres(self):
#         chargerParametres(self.getParametres().keys(), 
#                           self.nom_module, 
#                           os.path.join(util_path.PATH, self.nom_fichparam))



######################################################################################  
#
# Élement de base d'un dessin
#
######################################################################################  
class Elem_Dessin():
    def __init__(self, parent, rect = None):
        self.parent = parent
        self.rect = rect
        
        if self.parent is None:
            self.font_family = "sans-serif"##"Purisa"#"DejaVu Sans Mono"#"arial"#
        else:
            self.font_family = self.parent.font_family
    
    
    ########################################################################################            
    def draw(self, ctx = None, **kargs):
        if ctx is None:
            self.ctx = self.parent.ctx
        else:
            self.ctx = ctx
        
        return self._draw(ctx = self.ctx, **kargs)
        
    
    
    ########################################################################################            
    def getBitmap(self, *args, **kargs):
        i = self.getImageSurface(*args, **kargs)
        return getBitmapFromImageSurface(i)
    
    
    ########################################################################################            
    def getBase64PNG(self, *args, **kargs):
        return getBase64PNG(self.getImageSurface(*args, **kargs))
    
    
    




######################################################################################  
class Calendrier(Elem_Dessin):
    def __init__(self, parent, rect = None, 
                 calendrier = None):
        Elem_Dessin.__init__(self, parent, rect)
        self.calendrier = calendrier
        
    def _draw(self, ctx = None):
        """ Dessine un calendrier
             >> Renvoie la liste des rectangles des semaines
        """
        x, y, wt, ht = self.rect
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
#         dx_a = (wt-wj)/self.calendrier.GetNbrAnnees() + ea
        
        # liste des années
        lannees = self.calendrier.GetListeAnnees()
        
        # listes des mois   
        lmois, nmois = self.calendrier.GetMois()
        
        
        # Période entre deux mois
        dx_m = (wt - wj - (self.calendrier.GetNbrAnnees()-1)*ev - self.calendrier.GetNbrAnnees()*ea) / nmois
        
        # Période entre deux jours
        dy_j = (ht-ha-hm) / 31
        
        # largueur des zones année
        wa = {}   
        for ia, annee in enumerate(lannees):
            wa[annee] = 0
            for per in lmois[annee]:
                    for mois in per:
                        wa[annee] += dx_m
                    
    #         if ia == 0:
    #             wa[annee] = dx_m*len(lmois[annee])
    #         elif ia == calendrier.GetNbrAnnees():
    #             wa[annee] = dx_m*len(lmois[annee])
    #         else:
            if ia != 0 and ia != self.calendrier.GetNbrAnnees():
                wa[annee] += ev
        
        
        # Coef polide
        cp = 0.7
        
        
        #
        # Les noms des années, mois et jours
        #
        X = x
        
        jours_feries = constantes.JOURS_FERIES
        lstAcad = sorted([a[0] for a in list(constantes.ETABLISSEMENTS.values())])
        creneaux = self.calendrier.GetCreneauxFeries()
    #     print "creneaux", creneaux
        
        for ia, annee in enumerate(lannees):      
                
            show_text_rect_fix(ctx, str(annee), (X+wj, y, wa[annee], ha),
                               cp*ha, ha = 'c', va = 'c')
            
    #         
    #         show_text_rect(ctx, str(annee), 
    #                        (X+wj, y, wa[annee], ha), 
    #                        wrap = False,
    #                        orient = 'h', ha = 'c', va = 'c', b = 0.1)
            
            Y = y+ha+hm
            for jour in range(31):
                show_text_rect_fix(ctx, str(jour+1), 
                               (X, Y, ea, dy_j), 
                               cp*dy_j, 
                               ha = 'd', va = 'c')
    #             show_text_rect(ctx, str(jour+1), 
    #                            (X, Y, ea, dy_j), 
    #                            wrap = False,
    #                            orient = 'h', ha = 'd', va = 'c', b = 0.1)
                Y += dy_j
            
            for per in lmois[annee]:
                for mois in per:
                    show_text_rect_fix(ctx, constantes.MOIS[mois-1], 
                                   (X+wj, y+ha, dx_m, hm), cp*hm,
                                   ha = 'c', va = 'c')
    #                 show_text_rect(ctx, constantes.MOIS[mois-1], 
    #                                (X+wj, y+ha, dx_m, hm),
    #                                orient = 'h', ha = 'c', va = 'c', b = 0.1, ext = "")
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
                            show_text_rect_fix(ctx, str(S+1), 
                                               rs, cp*hs, 
                                               ha = 'c', va = 'c')
    #                         show_text_rect(ctx, str(S+1), 
    #                                        rs, couper = False, wrap = False, ext = "",
    #                                        orient = 'h', ha = 'c', va = 'c', b = 0.1)
                        
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


    def getImageSurface(self, larg):
    
        prop = self.calendrier.GetNbrAnnees()
        w, h = 0.04*larg*prop * COEF, 0.04 *larg* COEF
    #    print w, h
        imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  larg, int(h/w*larg))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        ctx = cairo.Context(imagesurface)
        ctx.scale(larg/w, larg/w)
        self.rect = (0,0,w,h)
        self.draw(ctx)
    
        return imagesurface


def getBitmapCalendrier(calendrier,
                        larg = 1, prop = 7):
    
    return Calendrier(None, None, 
                      calendrier).getBitmap(larg)



######################################################################################  
class Periodes(Elem_Dessin):
    def __init__(self, parent = None, rect = None, 
                 pos = None, 
                 periodes = [["Année", 5]], 
                 projets = {}):
        Elem_Dessin.__init__(self, parent, rect)  
         
        self.pos = pos
        if not isinstance(self.pos, list):
            self.pos = [self.pos]
            
        self.periodes = periodes
        self.projets = projets
        
        self.BcoulPos = []
        self.IcoulPos = []
        self.fontPos = 0.014 * COEF 


    ######################################################################################  
    def definirCouleurs(self):
        
        n = sum([p for _, p in self.periodes])
        couleur.generate(self.IcoulPos, [0xFFC3D0E2, 0xFFF2C5B5], n)
        couleur.generate(self.BcoulPos, [0xFF82AAE0, 0xFFEF825D], n)
        
        
        
        
    ######################################################################################  
    def _draw(self, ctx = None):
        """ Dessine les périodes de l'enseignements
             >> Renvoie la liste des rectangles des positions
        """
    #    print "DrawPeriodes", pos
        self.definirCouleurs()
        ctx.set_line_width (0.001 * COEF)
        
        x, y, wt, ht = self.rect
        
        # Toutes le périodes de projet
        periodes_prj = [p.periode for p in self.projets.values()]
    #    print "   ", periodes, periodes_prj
        
        # Les noms des projets par période
        noms_prj = {}
        for n, p in self.projets.items():
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
        
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_NORMAL)
        
        # Ecart entre les cases
        dx = 0.02 * wt
        # Hauteur des cases
        h = ht/2-2*dx
        
        # Les rectangles à cliquer
        rects = []
        
#         # Les différentes positions des cases
#         posc = []
    
        # Nombre d'années
        na = len(self.periodes)
        
        # Nombre total de périodes
        nt = 0
        for a in self.periodes:
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
        for i, (an, np) in enumerate(self.periodes):
            # Largeur de l'année
            wa = np*w + (np+1) * dx
            
            # Nom de l'année
            annee = an.split("_")
            ctx.set_font_size(self.fontPos)
            w0 = ctx.text_extents(annee[0])[2]
    #        xi = x + wi/2 + (dx+wi)*i
            if len(annee) > 1: # Exposant
                ctx.set_font_size(self.fontPos*0.9)
                w1 = ctx.text_extents(annee[1])[2]
                show_text_rect_fix(ctx, annee[0],
                                   (xi+wa/2-(w0+w1)/2, y, w0, ht*2/3), 
                                   self.fontPos, b = 0.01, ha = 'd')
                ctx.stroke ()
                show_text_rect_fix(ctx, annee[1], 
                                   (xi+wa/2-(w0+w1)/2 + w0 +self.fontPos/10, y, w1, ht/3), 
                                   self.fontPos*0.8, b = 0.01, ha = 'g')
                ctx.stroke ()
            else:
                show_text_rect_fix(ctx, annee[0], 
                                   (xi+wa/2-w0/2, y, w0, ht*2/3), 
                                   self.fontPos, b = 0.01)
                ctx.stroke ()
            
            for c in range(np):
                pa += 1
                if pa in list(noms_prj.keys()):
                    n = noms_prj[pa]
                else:
                    n = ""
                xcs.append((xi + c*(w+dx) + dx, (pa-1) in self.pos, i, n))
                
            xi += np*w + (np+1)*dx
            
        # Liste des positions qui fusionnent avec leur position précédente
        lstGrp = []
        for periode_prj in periodes_prj:
            if len(periode_prj) > 0:
                lstGrp.extend(list(range(periode_prj[0]+1, periode_prj[-1]+1)))
    #    print lstGrp
        
#         print("BcoulPos", self.BcoulPos)
#         print("lstGrp", lstGrp)
        for p in reversed(sorted(lstGrp)):
            del xcs[p-1]
            
#         print("xcs", xcs)
        
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
                ctx.set_source_rgba(*self.BcoulPos[p])
                ctx.fill_preserve ()
                ctx.set_source_rgba(0, 0, 0, 1)
            else:
                ctx.set_source_rgba(*(self.IcoulPos[p]))
                ctx.fill_preserve ()
                ctx.set_source_rgba(*self.BcoulPos[p])
            ctx.stroke ()    
            
            if xc[3] != "":
                show_text_rect(ctx, xc[3], 
                               rects[-1], ha = 'c', b = 0.02, wrap = False, couper = False)
                ctx.stroke ()
                
        return rects


    ########################################################################################
    #
    #    Image des périodes de l'enseignement , position et projets
    #          
    ########################################################################################            
    def getImageSurface(self, larg, prop = 7):
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
        self.rect = (0,0,w,h)
        try:
            self.draw(ctx)
        except:
            try:
                self.draw(ctx)
            except:
                print("cairocffi.CairoError")
#         try:
#             self.draw((0,0,w,h))
#         except: # 2ème tentative
#             time.sleep(0.01)
#             try:
#                 self.draw((0,0,w,h))
#             except:
#                 pass
    
        return imagesurface
    
    
    
    


    
def getBitmapPeriode(pos = None, 
                     periodes = [["Année", 5]], 
                     projets = {},
                     larg = 1, prop = 7):
    
    return Periodes(None, None, 
                    pos = pos, periodes = periodes, 
                    projets = projets).getBitmap(larg, prop)




def getBase64Periode(pos = None, 
                     periodes = [["Année", 5]], 
                     projets = {},
                     larg = 1, prop = 7):
    
    return Periodes(None, None, 
                    pos = pos, periodes = periodes, 
                    projets = projets).getBase64PNG(larg, prop)



######################################################################################  
class Classe(Elem_Dessin):
    def __init__(self, parent = None, rect = None, 
                 classe = None):
        Elem_Dessin.__init__(self, parent, rect)  
        self.classe = classe

            
            
    ######################################################################################  
    def _draw(self, ctx = None, complet = True):
        """ Dessine la répartition des élèves dans la classe
             >> Renvoie la liste des rectangles des groupes
        """
    #     print("DrawClasse")
    #     print(classe.effectifs)
    #     print(classe.nbrGroupes)
    #     print(rect)
        
        ref = self.classe.GetReferentiel()
        
        ctx.set_line_width(0.001 * COEF)
        
        x, y, wt, ht = self.rect 
        
        rap = wt/ht
        
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                           cairo.FONT_WEIGHT_NORMAL)
        
        ##########################################################################
        # Dimentions (relatif)
        #
        # Ecart entre les cases
        dy = 0.04
        dx = dy/rap
    #     dz = 0.005/640*wt
        
        # Hauteur mini pour les rectangles
        H = 0.1#*45800/ht
        
        # Espace pour écrire le texte au dessus des zones
        htxt = 0.1
        
        
        ###########################################################################
        # Calcul de la structure :
        #
        #  - format (exemple STI2D) :
    #     [{'G': [[{'D': [[],[(x,y,w,h), ...]]}, 
    #              {'E': [[],[(x,y,w,h), ...]]}, 
    #              {'P': [[],[(x,y,w,h), ...]]}],
    #             [(x,y,w,h), ...]]}, 
    #      {'S': [[],[(x,y,w,h), ...]]}]
    #     
    #     ref._effectifs :
    #         [{'G': [{'D': []}, 
    #                 {'E': []}, 
    #                 {'P': []}]}, 
    #          {'S': []}]
        #classe.effectifs
    #     {'C': 36, 
    #      'G': [18, 18], 
    #      'D': [[9, 9], [9, 9]], 
    #      'S': [9, 9, 9, 9], 
    #      'E': [[5, 5, 4, 4], [5, 5, 4, 4]], 
    #      'P': [[3, 3, 2, 2, 2, 2, 2, 2], [3, 3, 2, 2, 2, 2, 2, 2]]}
    
    #     classe.divisions
    # [{'C': [[36, [{'G': [[18, [{'D': [[9, []], [9, []]]}, 
    #                            {'E': [[5, []], [5, []], [4, []], [4, []]]}, 
    #                            {'P': [[3, []], [3, []], [2, []], [2, []], [2, []], [2, []], [2, []], [2, []]]}
    #                            ]
    #                      ], 
    #                      [18, [{'D': [[9, []], [9, []]]}, 
    #                            {'E': [[5, []], [5, []], [4, []], [4, []]]}, 
    #                            {'P': [[3, []], [3, []], [2, []], [2, []], [2, []], [2, []], [2, []], [2, []]]}]]]}, 
    #             {'S': [[9, []], [9, []], [9, []], [9, []]]}]]]}]
    
    #     [{'C': [[36, [{'G': [[18, [{'D': [[9, []], [9, []]]}, 
    #                                {'E': [[5, []], [5, []], [4, []], [4, []]]}, 
    #                                {'P': [[3, []], [3, []], [2, []], [2, []], [2, []], [2, []], [2, []], [2, []]]}]], 
    #                          [18, [{'D': [[9, []], [9, []]]}, 
    #                                {'E': [[5, []], [5, []], [4, []], [4, []]]}, 
    #                                {'P': [[3, []], [3, []], [2, []], [2, []], [2, []], [2, []], [2, []], [2, []]]}]]]}, 
    #                   {'S': [[9, []], [9, []], [9, []], [9, []]]}]]]}]
    
        #
        # - largeur : 1.0, hauteur : auto
        # 
        rectangles = []
        
        def calcRect(lstdiv, rect, lstrec):
            _x, _y, _w = rect   # position et largeur du rectangle contenant
            _h = 0      # Hauteur (mini) du rectangle contenant
            
            for dic in lstdiv:
                k, grp = list(dic.items())[0] # code et groupe (list)
                rg = [] # liste de rectangles
                lg = [] # liste de code (sous-groupe)
                _h += dy
                if complet: _h += htxt
                
                sh = 0
                for n, g in enumerate(grp):
                    if len(ref.effectifs[k]) >= 6 and ref.effectifs[k][5] == "O": # Mêmes activités --> superposition
                        R = [_x+dx+n*(dx), _y + _h, _w-2*dx-dx*(len(grp)-1)]
                        
                        _h += dy
                    else:                                                         # Activités différentes --> juxtaposition
                        wg = (_w-2*dx)/self.classe.nbrGroupes[k]
                        R = [_x+dx+n*wg, _y + _h, wg]
                            
                    # Si superposition, on ne gerde que la couche du dessus
                    if len(ref.effectifs[k]) >= 6 and ref.effectifs[k][5] == "O" and n != len(grp)-1:
                        lp = []
                    else:
                        lp = lg
                    sh = max(H, calcRect(g[1], R[:3], lp))
                    
                    R.append(sh)
                    rg.append((g[0], R))
                
                _h += sh
                        
                _h += dy 
            
                lstrec.append({k: [lg, rg]})
                
    #         maxy[0] = max(maxy[0], _y+_h)
            
            return _h
    #     print("divisions", classe.divisions)
        h = calcRect(self.classe.divisions, [0, 0, 1.0], rectangles)
    #     print(h, "!= ?", maxy[0])
    #     rectangles = [{'C' : [rectangles, [(36,[0, htxt, 1.0, h])]]}]
        
        scale = wt, ht/h
        
    #     print(scale, maxy[0])
    #     print(rectangles)
        
    #     [{'C': [[{'G': [[{'D': [[], [(0.1, 0.74, 0.4, 0.2), (0.5, 0.74, 0.4, 0.2)]]}, 
    #                      {'E': [[], [(0.1, 0.74, 0.2, 0.2), (0.3, 0.74, 0.2, 0.2), (0.5, 0.74, 0.2, 0.2), (0.7, 0.74, 0.2, 0.2)]]}, 
    #                      {'P': [[], [(0.1, 0.74, 0.1, 0.2), (0.2, 0.74, 0.1, 0.2), (0.3, 0.74, 0.1, 0.2), (0.4, 0.74, 0.1, 0.2), (0.5, 0.74, 0.1, 0.2), (0.6, 0.74, 0.1, 0.2), (0.7, 0.74, 0.1, 0.2), (0.8, 0.74, 0.1, 0.2)]]}], 
    #                      [(0.05, 0.25, 0.9, 0.2), (0.07, 0.27, 0.9, 0.2)]]}, 
    #              {'S': [[], [(0.05, 0.25, 0.225, 0.2), (0.275, 0.25, 0.225, 0.2), (0.5, 0.25, 0.225, 0.2), (0.725, 0.25, 0.225, 0.2)]]}], [(0, 0.1, 1.0, 0.9)]]}]
        
        def rectanglePlein(x, y, w, h, coul):
            ctx.set_line_width(e)
            ctx.rectangle(x, y, w, h)
            ctx.set_source_rgb(*[c*3.0 for c in coul[:3]])
            ctx.fill_preserve ()
            ctx.set_source_rgb(*coul[:3])      
            ctx.stroke()
        
        ####################################################################################
        # Tracé
        
        # Les rectangles à cliquer
        rects = {}
        
        # Les premiers rectangles des effectifs
        
        rEff = {#"C" : (dx, y+dy, wt, ht),
                "I" : [(x+dx, y+dy, wt, ht)]
                 }
        
        
        # Epaisseur de ligne
        e = 0.01*scale[1]
        
        # Taille de la police
        f = htxt * scale[1]
        
        coulGrp = {k : couleur.CouleurInt2Float(ref.effectifs[k][3]) for k in ref.effectifs.keys() if ref.effectifs[k] is not None}
    #     print("coulGrp", coulGrp)
        def tracRect(lst):
            for dic in lst:
                k, gr = list(dic.items())[0] # code et groupe-rect (list)
                g, lstrl = gr
    #             print("   ", k, g, lstrl)
                r0 = lstrl[0][1]    # premier rectangle
                r1 = lstrl[-1][1]   # dernier rectangle
                
                # Grand rectangle pour titre
                R = (x + r0[0]*scale[0],     y + (r0[1]-htxt)*scale[1], 
                     (r1[0]+r1[2])*scale[0], htxt*scale[1])
                
                rects[k] = [] 
                if complet:
                    ctx.set_source_rgb(*coulGrp[k][:3])
                    eff = self.classe.effectifs[k]
    #                 if type(eff) != list : eff = [eff]
                    t = ref.effectifs[k][1]# + " (" + "+".join([str(n) for n in eff])+ ")"
                    if type(eff) != list :
                        t += " (" +str(eff)+ ")"
                    elif len(g) > 0:
                        t += " (" + "+".join([str(n) for n in eff])+ ")"
                    show_text_rect_fix(ctx, t, R,
                                       f, ha = 'g')
                
                for lab, r in lstrl: # label + rectangle
                    R = (r[0]*scale[0]+x, r[1]*scale[1]+y, 
                         r[2]*scale[0],   r[3]*scale[1])
                    
                    # On récupère les premiers rectangles
                    
                    if not k in rEff:
                        rEff[k] = [(R[0], R[1], R[2], R[3])]
                    else:
                        if len(ref.effectifs[k]) >= 6 and ref.effectifs[k][5] != "O":
                            rEff[k].append((R[0], R[1], R[2], R[3]))
                        
                    rectanglePlein(*R, coulGrp[k])
                    rects[k].append(R)
                    if complet and len(g) == 0:
                        ctx.set_source_rgb(*coulGrp[k][:3])
                        show_text_rect_fix(ctx, str(lab), 
                                           R, f*0.8)
                    
                tracRect(g)
                
        tracRect(rectangles)
        
        return rEff, rects
    
    
    ##########################################################################################
    def getImageSurface(self, W, H):
    #     print("getBitmapClasse", W, H)
        w, h = 0.04*W * COEF, 0.04 *H* COEF
    #     print(w, h)
    #     imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32,  larg, int(h/w*larg))#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        imagesurface = cairo.ImageSurface(cairo.FORMAT_RGB24,  W, H)#cairo.FORMAT_ARGB32,cairo.FORMAT_RGB24
        ctx = cairo.Context(imagesurface)
        ctx.scale(W/w, W/w) 
        ctx.set_source_rgba(1,1,1,1)
        ctx.paint()
        
        self.rect = (0,0,w,h)
        self.draw(ctx)
    #     ctx.paint()
#         try:
#             self.draw((0,0,w,h))
#         except: # 2ème tentative
#             time.sleep(0.01)
#             try:
#                 self.draw((0,0,w,h))
#             except:
#                 pass
        
        return imagesurface


def getBitmapClasse(W, H, classe):
    return Classe(None, None, classe).getBitmap(W, H)


def getBase64Classe(W, H, classe):
    return Classe(None, None, classe).getBase64PNG(W, H)








class Curve_rect_titre(Elem_Dessin):
    def __init__(self, parent, rect, titre, 
                     coul_bord, coul_int, 
                     taille_font = 0.01 * COEF, 
                     rayon = 0.02 * COEF, 
                     epaiss = 0.002 * COEF):
        Elem_Dessin.__init__(self, parent, rect) 
        
        self.titre = titre
        self.coul_bord = coul_bord
        self.coul_int = coul_int
        self.taille_font = taille_font
        self.rayon = rayon
        self.epaiss = epaiss
    
    
    def _draw(self, ctx = None):
        """    Dessine une zone de texte aux bords arrondis
                avec un titre au dessus
                
                >> Renvoie le point caractéristique (svg)
        """
        ctx.set_line_width(self.epaiss)
        x0, y0, rect_width, rect_height = self.rect
        
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(self.taille_font)
        fheight = ctx.font_extents()[2]
        _, ybearing, width, height,*_ = ctx.text_extents(self.titre)
          
        c = Curve_rect_coin(self.parent, (x0, y0, rect_width, rect_height), self.rayon, 
                   ouverture = min(width + fheight, rect_width-2*self.rayon)).draw(ctx)
        
        ctx.set_source_rgba(*self.coul_int)
        ctx.fill_preserve()
        ctx.set_source_rgba(*self.coul_bord)
        ctx.stroke()
        
        xc = x0# + rayon
        mask = cairo.LinearGradient(xc, y0, xc, y0 - height)
        mask.add_color_stop_rgba(1, 1, 1, 1, 0)
        mask.add_color_stop_rgba(0, *self.coul_int)
        ctx.rectangle(xc, y0 - height, min(width + fheight, rect_width-2*self.rayon), height)
        ctx.set_source(mask) 
        ctx.fill()
        
        xc = x0 + fheight/2# + rayon
        yc = y0 + ybearing - fheight/3#height
        
        ctx.move_to(xc, yc)
        ctx.set_source_rgb(0, 0, 0)
    #    ctx.show_text(titre)
        
        show_text_rect_fix(ctx, self.titre, 
                           (xc, yc, rect_width-2*self.rayon, fheight),
                           self.taille_font, b = 0, ha = "g")
        
        return c

                   
                   
                   

class Curve_rect_coin(Elem_Dessin):
    def __init__(self, parent, rect, radius, ouverture = 0):
        Elem_Dessin.__init__(self, parent, rect) 
        
        self.radius = radius
        self.ouverture = ouverture
        
        
    ##################################################################################
    def _draw(self, ctx = None):
        """    Dessine une zone de texte aux bords arrondis
                avec un coin "carré" (en haut à gauche)
                >> Renvoie le point caractéristique (svg)
        """
        
        x, y, w, h = self.rect
        
        x1=x+w
        y1=y+h
        #if (!rect_width || !rect_height)
        #    return
        if w/2 < self.radius:
            if h/2<self.radius:
                ctx.move_to  (x, (y + y1)/2)
                ctx.line_to (x ,y)
                ctx.line_to ((x + x1)/2, y)
                ctx.curve_to (x1, y, x1, y, x1, (y + y1)/2)
                ctx.curve_to (x1, y1, x1, y1, (x1 + x)/2, y1)
                ctx.curve_to (x, y1, x, y1, x, (y + y1)/2)
            else:
                ctx.move_to  (x, y + self.radius)
                ctx.line_to (x ,y)
                ctx.line_to ((x + x1)/2 ,y)
                ctx.curve_to (x1, y, x1, y, x1, y + self.radius)
                ctx.line_to (x1 , y1 - self.radius)
                ctx.curve_to (x1, y1, x1, y1, (x1 + x)/2, y1)
                ctx.curve_to (x, y1, x, y1, x, y1- self.radius)
        
        else:
            if h/2 < self.radius:
                ctx.move_to  (x + self.ouverture, y)
                ctx.line_to (x1 - self.radius, y)
                ctx.curve_to (x1, y, x1, y, x1, (y + y1)/2)
                ctx.curve_to (x1, y1, x1, y1, x1 - self.radius, y1)
                ctx.line_to (x + self.radius, y1)
                ctx.curve_to (x, y1, x, y1, x, (y + y1)/2)
                ctx.line_to (x ,y)
                
            else:
                ctx.move_to  (x + self.ouverture, y)
                ctx.line_to (x1 - self.radius, y)
                ctx.curve_to (x1, y, x1, y, x1, y + self.radius)
                ctx.line_to (x1 , y1 - self.radius)
                ctx.curve_to (x1, y1, x1, y1, x1 - self.radius, y1)
                ctx.line_to (x + self.radius, y1)
                ctx.curve_to (x, y1, x, y1, x, y1- self.radius)
                ctx.line_to (x, y)
        
        # Renvoie les coordonnées du 1er point = caractéristique du path SVG
        return x + self.ouverture, y 






class Curve_rect(Elem_Dessin):
    def __init__(self, parent, rect, radius, ouverture = 0):
        Elem_Dessin.__init__(self, parent, rect) 
        
        self.radius = radius
        self.ouverture = ouverture


    ##################################################################################
    def _draw(self, ctx = None):
        """    Dessine une zone de texte aux bords arrondis
                >> Renvoie le point caractéristique (svg)
        """
        x, y, w, h = self.rect
        
        x1 = x + w
        y1 = y + h
        
        #if (!rect_width || !rect_height)
        #    return
        if w/2<self.radius:
            if h/2 < self.radius:
                ctx.move_to  (x, (y + y1)/2)
                ctx.curve_to (x ,y, x, y, (x + x1)/2, y)
                ctx.curve_to (x1, y, x1, y, x1, (y + y1)/2)
                ctx.curve_to (x1, y1, x1, y1, (x1 + x)/2, y1)
                ctx.curve_to (x, y1, x, y1, x, (y + y1)/2)
            else:
                ctx.move_to  (x, y + self.radius)
                ctx.curve_to (x ,y, x, y, (x + x1)/2, y)
                ctx.curve_to (x1, y, x1, y, x1, y + self.radius)
                ctx.line_to (x1 , y1 - self.radius)
                ctx.curve_to (x1, y1, x1, y1, (x1 + x)/2, y1)
                ctx.curve_to (x, y1, x, y1, x, y1- self.radius)
        
        else:
            if h/2 < self.radius:
                ctx.move_to  (x, (y + y1)/2)
                ctx.line_to (x1 - self.radius, y)
                ctx.curve_to (x1, y, x1, y, x1, (y + y1)/2)
                ctx.curve_to (x1, y1, x1, y1, x1 - self.radius, y1)
                ctx.line_to (x + self.radius, y1)
                ctx.curve_to (x, y1, x, y1, x, (y + y1)/2)
                ctx.line_to  (x, (y + y1)/2)
                ctx.curve_to (x , y, x , y, x + self.radius, y)
                
            else:
                ctx.move_to  (x + self.radius + self.ouverture, y)
                ctx.line_to (x1 - self.radius, y)
                ctx.curve_to (x1, y, x1, y, x1, y + self.radius)
                ctx.line_to (x1 , y1 - self.radius)
                ctx.curve_to (x1, y1, x1, y1, x1 - self.radius, y1)
                ctx.line_to (x + self.radius, y1)
                ctx.curve_to (x, y1, x, y1, x, y1- self.radius)
                ctx.line_to (x, y+self.radius)
                ctx.curve_to (x , y, x , y, x + self.radius, y)
        
        # Renvoie les coordonnées du 1er point = caractéristique du path SVG
        return x + self.radius  + self.ouverture, y 



class Image(Elem_Dessin):
    def __init__(self, parent, rect, bmp, marge = 0):
        Elem_Dessin.__init__(self, parent, rect)
        self.bmp = bmp
        self.marge = marge # Coefficient 0-1
        
        
    def _draw(self, ctx = None):
        """ Dessine une image
        
        """
        x, y, w, h = self.rect
        
        x = x + self.marge*w
        y = y + self.marge*h
        w = w - 2*self.marge*w
        h = h - 2*self.marge*h
        
        # Ancienne méthode
#         tfname = tempfile.mktemp()
#         try:
#             self.bmp.SaveFile(tfname, wx.BITMAP_TYPE_PNG)
#             image = cairo.ImageSurface.create_from_png(tfname)
#         except:
#             return
#         finally:
#             if os.path.exists(tfname):
#                 os.remove(tfname)  

        image = wx.lib.wxcairo.ImageSurfaceFromBitmap(self.bmp)
        
        
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



class TableauV(Elem_Dessin):
    def __init__(self, parent, titres, x, y, w, ht, hl, 
                 nlignes = 0, va = 'c', ha = 'c', 
                 orient = 'h', coul = (0.9,0.9,0.9), b = 0.06):
        Elem_Dessin.__init__(self, parent)
        self.titres = titres
        self.x = x
        self.y = y
        self.w = w
        self.ht = ht
        self.hl = hl
        self.nlignes = nlignes
        self.va = va
        self.ha = ha
        self.orient = orient
        self.coul = coul
        self.b = b
    
    
    
    def _draw(self, ctx = None):
        """    Dessine un tableau vertical (entêtes à l'horizontale)
                x, y = position du coin haut-gauche
                ht = hauteur de la ligne d'entête
                hl = hauteur de chaque ligne
                
                >> Renvoie la liste des rectangles des entêtes
        """
        rect = []
        wc = self.w/len(self.titres)
        _x = self.x
        _coul = ctx.get_source().get_rgba()
    #    print "tableau", _coul
        for titre in self.titres:
    #        print "    ",titre
            ctx.rectangle(_x, self.y, wc, self.ht)
            ctx.set_source_rgb (*self.coul[:3])
            ctx.fill_preserve ()
            ctx.set_source_rgba (*_coul)
            show_text_rect(ctx, titre, (_x, self.y, wc, self.ht), 
                           va = self.va, ha = self.ha, 
                           b = self.b, orient = self.orient, 
                           couper = True, wrap = True)
            
    #        if orient == 'h':
            rect.append((_x, self.y, wc, self.ht))
    #        else:
    #            rect.append((-y, _x, wc, ht))
            ctx.stroke ()
            _x += wc
        
        _x = self.x
        _y = self.y+self.ht
        
        for _ in range(self.nlignes):
            ctx.rectangle(_x, _y, wc, self.hl)
            _x += wc
            _y += self.hl
            
        ctx.stroke ()
        
        self.rect = self.x, self.y, self.w, _y-self.y
        return rect




class TableauH(Elem_Dessin):
    def __init__(self, parent, titres, x, y, wt, wc, h, 
                 nCol = 0, va = 'c', ha = 'c', orient = 'h', 
                 coul = (0.9,0.9,0.9), 
                 contenu = [], tailleFixe = False):
        Elem_Dessin.__init__(self, parent)
        self.titres = titres
        self.x = x
        self.y = y
        self.wc = wc
        self.h = h
        self.wt = wt
        self.nCol = nCol
        self.va = va
        self.ha = ha
        self.orient = orient
        self.coul = coul
        self.contenu = contenu
        self.tailleFixe = tailleFixe


    def _draw(self, ctx = None):
        
        rect = []
        hc = self.h/len(self.titres)
        _y = self.y
        _coul = ctx.get_source().get_rgba()
    
        taillesFont = []
        for i, titre in enumerate(self.titres):
            ctx.rectangle(self.x, _y, self.wt, hc)
            if type(self.coul) == dict :
                col = self.coul[titre.rstrip("1234567890.")]
            elif type(self.coul[0]) == tuple:
                col = self.coul[i]
            else:
                col = self.coul
            ctx.set_source_rgba (*col[0])
            ctx.fill_preserve ()
            ctx.set_source_rgba (*_coul)
            f, _, l = show_text_rect(ctx, titre, (self.x, _y, self.wt, hc), 
                                              va = self.va, ha = self.ha, 
                                              b = 0.02, orient = self.orient, 
                                              tracer = not self.tailleFixe)
            taillesFont.append(f)
            rect.append((self.x, _y, self.wt, hc))
            ctx.stroke ()
            _y += hc
        
        
        if self.tailleFixe: # Tracé en différé
            tailleFont = min(taillesFont)
            _y = self.y
            for i, titre in enumerate(self.titres):
                ctx.set_source_rgba (*_coul)
                show_text_rect(ctx, titre, (self.x, _y, self.wt, hc), 
                               va = self.va, ha = self.ha, 
                                b = 0.02, orient = self.orient, 
                                fontsizeMinMax = (tailleFont, tailleFont))
                _y += hc
    
        _x = self.x+self.wt
        _y = self.y
        for c in range(self.nCol):
            for l in range(len(self.titres)):
                ctx.rectangle(_x, _y, self.wc, hc)
                _y += hc
            _x += self.wc
            _y = self.y
        
        _y = self.y
        _x = self.x+self.wt
        for c in self.contenu:
            for l in c:
                show_text_rect(ctx, l, (_x, _y, self.wc, hc), 
                               va = self.va, ha = self.ha, 
                               b = 0.02, orient = self.orient)
                _y += hc
            _x += self.wc
            _y = self.y
            
        ctx.stroke ()
        self.rect = self.x, self.y, _x-self.x, self.h
        return rect



class TableauH_var(Elem_Dessin):
    def __init__(self, parent, titres, x, y, wt, wc, hl, 
                 taille, nCol = 0, va = 'c', ha = 'c', orient = 'h', 
                 coul = (0.9,0.9,0.9), contenu = []):
        Elem_Dessin.__init__(self, parent)
        self.titres = titres
        self.x = x
        self.y = y
        self.wc = wc
        self.hl = hl
        self.wt = wt
        self.nCol = nCol
        self.va = va
        self.ha = ha
        self.orient = orient
        self.coul = coul
        self.contenu = contenu
        self.taille = taille



    def _draw(self, ctx = None):
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
        _y = self.y
        _coul = ctx.get_source().get_rgba()
    #     print "tableauH", _coul
        for i, titre in enumerate(self.titres):
            ctitre = titre.rstrip("1234567890.")
    #        print "    ",ctitre
            
            ctx.rectangle(self.x, _y, self.wt, self.hl[i])
            if type(self.coul) == dict:# and len(ctitre) > 0:
                col = self.coul[ctitre]
            else:
                col = self.coul
            ctx.set_source_rgb (col[0], col[1], col[2])
            ctx.fill_preserve ()
            ctx.set_source_rgba (*_coul)
            show_text_rect(ctx, titre, (self.x, _y, self.wt, self.hl[i]),
                           va = self.va, ha = self.ha, 
                           orient = self.orient, fontsizeMinMax = (-1, self.taille))
            ctx.stroke ()
            _y += self.hl[i]
        
        _x = self.x+self.wt
        _y = self.y
        for c in range(self.nCol):
            for l in range(len(self.titres)):
                ctx.rectangle(_x, _y, self.wc, self.hl[c])
                _y += self.hl[c]
            _x += self.wc
            _y = self.y
        
        _y = self.y
        _x = self.x+self.wt
        ctx.set_font_size(self.taille)
        fascent, fdescent, fheight = ctx.font_extents()[:3]
    #    print
        for c in self.contenu:
    #        print "    ", c
            for j, l in enumerate(c):
                #
                # On dessine toutes les lignes de texte
                #
                
    #            h = (fascent+fdescent)*len(ll)
                for i, t in enumerate(l):
            #        print "  ",t
                    xbearing, _, width, *_ = ctx.text_extents(t)
                    xt, yt = _x+xbearing+(self.wc-width)/2, _y + (fascent+fdescent)*i - fdescent + fheight
            #        print "  ",xt, yt
                    if self.ha == 'c':
                        ctx.move_to(xt, yt)
                    elif self.ha == 'g':
                        ctx.move_to(_x, yt)
                    
                    ctx.show_text(t)
    #            show_text_rect(ctx, l, _x, _y, wc, hl[c], va = va, ha = ha, orient = orient, max_font = taille)
                _y += self.hl[j]
            _x += self.wc
            _y = self.y
            
        ctx.stroke ()
        self.rect = self.x, self.y, _x-self.x, sum(self.hl)



class Rectangle_plein(Elem_Dessin):
    def __init__(self, parent, rect, coulBord, coulInter, alpha = 1):
        Elem_Dessin.__init__(self, parent, rect)
        self.coulBord = coulBord
        self.coulInter = coulInter
        self.alpha = alpha


    def _draw(self, ctx = None):
        ctx.rectangle(*self.rect)
    #     ctx.set_source_rgba (*coulInter[:3], alpha)
        ctx.set_source_rgba (*[c*self.alpha for c in self.coulInter[:3]], 1)
        ctx.fill_preserve ()
    #     ctx.set_source_rgba (*coulBord[:3], alpha)
        ctx.set_source_rgba (*[c*self.alpha for c in self.coulBord[:3]], 1)
        ctx.stroke ()




class Rectangle_plein_biseau(Elem_Dessin):
    def __init__(self, parent, rect, b, coulBord, coulInter, alpha = 1):
        Elem_Dessin.__init__(self, parent, rect)
        self.coulBord = coulBord
        self.coulInter = coulInter
        self.alpha = alpha
        self.b = b
        
        
    def _draw(self, ctx = None):
        x, y, w, h = self.rect
        ctx.move_to(x+self.b, y)
        ctx.line_to(x+w, y)
        ctx.line_to(x+w-self.b, y+h)
        ctx.line_to(x, y+h)
        ctx.line_to(x+self.b, y)
        
        ctx.set_source_rgba (*self.coulInter[:3], self.alpha)
        ctx.fill_preserve ()
        ctx.set_source_rgba (*self.coulBord[:3], self.alpha)
        ctx.stroke ()
    


class Rectangle_plein_fleche(Elem_Dessin):
    def __init__(self, parent, rect, b, coulBord, coulInter, alpha = 1):
        Elem_Dessin.__init__(self, parent, rect)
        self.coulBord = coulBord
        self.coulInter = coulInter
        self.alpha = alpha
        self.b = b
        
        
    def _draw(self, ctx = None):
        x, y, w, h = self.rect
        ctx.move_to(x, y)
        ctx.line_to(x+w-self.b, y)
        ctx.line_to(x+w, y+h/2)
        ctx.line_to(x+w-self.b, y+h)
        ctx.line_to(x, y+h)
        ctx.line_to(x+self.b, y+h/2)
        ctx.line_to(x, y)
    
    
class Rectangle_plein_doigt(Elem_Dessin):
    def __init__(self, parent, rect, b, yd, coulBord, coulInter, alpha = 1):
        Elem_Dessin.__init__(self, parent, rect)
        self.coulBord = coulBord
        self.coulInter = coulInter
        self.alpha = alpha
        self.b = b
        self.yd = yd
        
    def _draw(self, ctx = None):
        x, y, w, h = self.rect
        if self.b > h:
            self.b = h
        if self.yd < self.b:
            self.yd = self.b
        elif self.yd > h-self.b:
            self.yd = h-self.b
        ctx.move_to(x,     y)
        ctx.line_to(x+w-self.b, y)
        ctx.line_to(x+w-self.b, y+self.yd-self.b)
        ctx.line_to(x+w,   y+self.yd)
        ctx.line_to(x+w-self.b, y+self.yd+self.b)
        ctx.line_to(x+w-self.b, y+h)
        ctx.line_to(x,     y+h)
        ctx.line_to(x,     y)
        
        
        ctx.set_source_rgba (*self.coulInter[0:3], self.alpha)
        ctx.fill_preserve ()
        ctx.set_source_rgba (*self.coulBord[0:3], 1)
        ctx.stroke ()




class Boule(Elem_Dessin):
    def __init__(self, parent, x, y, r, p = 100, 
                  color0 = (1, 1, 1, 1), color1 = (0, 0, 0, 1),
                  transparent = True):
        Elem_Dessin.__init__(self, parent)
        self.x = x
        self.y = y
        self.r = r
        self.p = p
        self.color0 = color0
        self.color1 = color1
        self.transparent = transparent
        
        
    def _draw(self, ctx = None):
        
        mask = 0.01*self.p
        pat = cairo.RadialGradient (self.x-self.r/2, self.y-self.r/2, self.r/4,
                                    self.x-self.r/3, self.y-self.r/3, 3*self.r/2)
        if self.transparent:
            alpha0 = self.color0[3]
            alpha1 = self.color1[3]
        else:
            alpha0 = 1
            alpha1 = 1
        
        pat.add_color_stop_rgba(0, *self.color0[:3], alpha0)
        pat.add_color_stop_rgba(1, *self.color1[:3], alpha1)
        
        ctx.set_line_width (0.0003 * COEF)
        ctx.set_source_rgba (1, 1, 1, 1)
        ctx.arc (self.x, self.y, self.r, 0, 2*pi)
        ctx.fill_preserve()
        ctx.set_source_rgba (0, 0, 0, 1)
        ctx.stroke ()
        
        ctx.set_source (pat)
        ctx.move_to (self.x, self.y)
        ctx.line_to (self.x, self.y-self.r)
        ctx.arc (self.x, self.y, self.r, 3*pi/2, 2*pi*mask + 3*pi/2)
        ctx.fill()



class BarreH(Elem_Dessin):
    def __init__(self, parent, x, y, w, r, a, e, coul0, coul1, coul):
        Elem_Dessin.__init__(self, parent)
        self.x = x
        self.y = y
        self.w = w
        self.r = r
        self.a = a
        self.e = e
        self.coul0 = coul0
        self.coul1 = coul1
        self.coul = coul


    def _draw(self, ctx = None):
        """ Dessine une barre horizontale de poucentage/progression
            :param x,y: position
            :param w: longueur maxi (100%)
            :param r: taux
            :param e: épaisseur
            :param a: acceptable (a==True : coul0  - a==False = coul1)
        """
        src = ctx.get_source()
        
        if self.a:
            coulEtat = self.coul1
        else:
            coulEtat = self.coul0
            
        ctx.set_source_rgba(*self.coul)
        ctx.rectangle (self.x, self.y-self.e/2, self.w*self.r, self.e)
        ctx.fill_preserve ()    
        ctx.set_source_rgba(0.4,  0.4,  0.4,  1)
        ctx.set_line_width(0.001 * COEF)
        ctx.stroke()
        
        ctx.set_source_rgba(*coulEtat)
        ctx.rectangle (self.x+self.w*self.r-self.e, self.y-self.e/2, self.e, self.e)
        ctx.fill ()
        
        
        
        ctx.set_source(src)
    

    
def ligne(ctx, x1, y1, x2, y2, coul):
#     if len(coul) < 4:
#         coul = list(coul)+[1]
    ctx.set_source_rgba(*coul)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()


class Fleche_verticale(Elem_Dessin):
    def __init__(self, parent, x, y, h, e, coul):
        Elem_Dessin.__init__(self, parent)
        self.x = x
        self.y = y
        self.h = h
        self.e = e
        self.coul = coul
        
        
    def _draw(self, ctx = None):
        ctx.set_source_rgba(*self.coul)
        he = min(self.e/2, self.h/3)
        ctx.move_to(self.x-self.e/2, self.y)
        ctx.line_to(self.x-self.e/2, self.y+self.h-he)
        ctx.line_to(self.x, self.y+self.h)
        ctx.line_to(self.x+self.e/2, self.y+self.h-he)
        ctx.line_to(self.x+self.e/2, self.y)
        ctx.close_path ()
        ctx.fill_preserve ()    
        ctx.set_source_rgba(0.4,  0.4,  0.4,  1)
        ctx.set_line_width(0.0006 * COEF)
        ctx.stroke ()
    


class Fleche_ronde(Elem_Dessin):
    def __init__(self, parent, x, y, r, a0, a1, e, f, coul):
        Elem_Dessin.__init__(self, parent)
        self.x = x
        self.y = y
        self.r = r
        self.a0 = a0
        self.a1 = a1
        self.e = e
        self.f = f
        self.coul = coul
        

    def _draw(self, ctx = None):
        """ Dessine une flèche
            :param x, y: centre
            :param r: rayon
            :param a0, a1: angles de départ et d'arrivée (en degrés)
            :param e: épaisseur
            :param f: taille du bout de flèche
        """
        ctx.set_line_width (self.e)
        ctx.set_source_rgba (*self.coul)
    #    a0 = (90-a/2) * pi/180 + f/r/2
    #    a1 = (90+a/2) * pi/180 + f/r/2
        a2 = (90-self.a0) * pi/180
        self.a0 = self.a0 * pi/180+ self.f/self.r/2
        self.a1 = self.a1 * pi/180 
        
    #    a2 = a/2 * pi/180
        
        ctx.arc (self.x, self.y, self.r, self.a0, self.a1)
        ctx.stroke ()
    
        # angle du bout de flèche
        af = pi/5
        _x, _y = self.x+self.r*sin(a2), self.y+self.r*cos(a2)
    
        ctx.move_to(_x, _y)
        ctx.line_to(_x-self.f*cos(af-a2), _y-self.f*sin(af-a2))
        ctx.line_to(_x-self.f*cos(-a2-af), _y-self.f*sin(-a2-af))
    
        ctx.close_path()
        ctx.fill ()
    



class Liste_code_texte2(Elem_Dessin):
    def __init__(self, parent, rect, lstCodes, lstTexte, 
                     dx, gras = None, lstCoul = None, va = 'h', 
                     coulFond = None):
        Elem_Dessin.__init__(self, parent, rect)
        self.lstCodes = lstCodes
        self.lstTexte = lstTexte
        self.dx = dx
        self.lstCoul = lstCoul
        self.gras = gras
        self.coulFond = coulFond
        self.va = va
        
        
    ########################################################################################
    def _draw(self, ctx = None):
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
        x, y, w, h = self.rect
        
        no = len(self.lstCodes)
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
        c = [len(t) for t in self.lstTexte]
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
                    self.dx = -1
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
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
        for i, t in enumerate(self.lstCodes):
            if t.strip() != "":
                
                # Un rectangle pour la séléction
                rect = (x, y + sum(ht[:i]) + i*hc, w, hc+ht[i])
                lstRect.append(rect)
                ctx.set_line_width(0.0001 * COEF)
                ctx.set_source_rgba (*self.coulFond[:3], 0.01)
                ctx.rectangle(*rect)
                ctx.fill_preserve()
                ctx.stroke()
                
                
                if self.lstCoul != None:
                    ctx.set_source_rgb (*self.lstCoul[i])
    #                else:
    #                    ctx.set_source_rgb (0, 0, 0)

                _, r , _ = show_text_rect(ctx, t,
                                        (x, y + sum(ht[:i]) + i*hc, w, hc), #y+i*hl, 
                                        b = 0, ha = 'g', va = va, 
                                        fontsizeMinMax = (-1, maxFontSize), wrap = False)
    #             ctx.set_line_width(0.0001 * COEF)
    #             ctx.rectangle(*re)
    #             ctx.stroke()
                wc.append(r[2])
                
        if acote:
            self.dx = max(wc) + minfheight
        if self.dx > w:
            self.dx = 0
        #
        # Textes
        #
    #     ly = []
        for i, t in enumerate(self.lstCodes):
            if self.lstTexte[i].strip() != "":
                if i == self.gras:
                    ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_BOLD)
                else:
                    ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                          cairo.FONT_WEIGHT_NORMAL)
                if self.lstCoul != None:
                    ctx.set_source_rgb (*self.lstCoul[i])
    #                else:
    #                    ctx.set_source_rgb (0, 0, 0)
                if acote:
                    re = (x + self.dx, y + i*hc, w - self.dx, hc)
                    va = 'c'
                else:
                    re = (x + self.dx, y + (i+1)*hc + sum(ht[:i]), 
                          w - self.dx, ht[i])
                    va = 'h'  
#                 print(w, self.dx)
                show_text_rect(ctx, self.lstTexte[i], 
                               re, 
                               b = 0, ha = 'g', va = va, 
                               fontsizeMinMax = (-1, maxFontSize))
        
        return lstRect


class Liste_code_texte(Elem_Dessin):
    def __init__(self, parent, rect, lstCodes, lstTexte, 
                     eh, b = 0.1, gras = None, lstCoul = None, va = 'h'):
        Elem_Dessin.__init__(self, parent, rect)
        self.lstCodes = lstCodes
        self.lstTexte = lstTexte
        self.eh = eh
        self.lstCoul = lstCoul
        self.gras = gras
        self.b = b
        self.va = va


    ########################################################################################    
    def _draw(self, ctx = None):
        """ Affiche une liste d'élément sous la forme :
            code texte
            code texte
            ...
            :param eh: écart horizontal entre le code et le texte
            :param b: bordure latérale totale (en relatif : 0 à 1)
            :return: Renvoie une liste de rectangles
        """
        x, y, w, h = self.rect
        
        #
        # Réduction du rectangle
        #
        e = min(w*self.b, h*self.b)
        x, y = x+e, y+e
        w, h = w-2*e, h-2*e
        
        no = len(self.lstCodes)
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
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
        
        wt = max([ctx.text_extents(t)[2] for t in self.lstCodes if t.strip() != ""])
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
        for i, t in enumerate(self.lstCodes):
            if self.lstTexte[i].strip() != "":
                if i == self.gras:
                    ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                      cairo.FONT_WEIGHT_BOLD)
                else:
                    ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                                          cairo.FONT_WEIGHT_NORMAL)
                if self.lstCoul != None:
                    ctx.set_source_rgb (*self.lstCoul[i][:3])
    #                else:
    #                    ctx.set_source_rgb (0, 0, 0)
    #             print("show", w,wt,eh)
                if w - wt - self.eh > 0:
                    show_text_rect(ctx, self.lstTexte[i], 
                                   (x + wt + self.eh, y+i*hl, 
                                    w - wt - self.eh, hl), 
                                   b = 0, ha = 'g', va = self.va, 
                                   fontsizeMinMax = (-1, maxFontSize))
                    
                    
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
                ctx.set_source_rgba (*co)
                
                ly.append(y+i*hl)
                
    #            ctx.restore()
    
    
        #
        # Codes
        #
        ctx.select_font_face (self.font_family, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
        for i, t in enumerate(self.lstCodes):
            if t.strip() != "":
                if self.lstCoul != None:
                    ctx.set_source_rgb (*self.lstCoul[i][:3])
    #                else:
    #                    ctx.set_source_rgb (0, 0, 0)
                    
                show_text_rect(ctx, t, 
                               (x, ly[i], wt, hl), #y+i*hl, 
                               b = 0, ha = 'd', va = self.va, 
                               fontsizeMinMax = (-1, maxFontSize), wrap = False)
            
        
        return lstRect
    
    
# def show_texte(ctx, texte, x, y):
#     glyphs = []
#     _x, _y = x, y
#     for c in texte:
#         xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(c)
#         glyphs.append((ord(c), _x, _y))
#         _x += width
#     ctx.show_glyphs(glyphs)
    
# def drange(start, stop, step):
#     r = start
#     while r < stop:
#         yield r
#         r += step    
    

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
#  Un système de "cache" pour la fonction de découpe de lignes de texte
#
##########################################################################################
import functools


    



# Une autre cache pour les méthodes text_extent et font_extent qui provoquent des 'out of memory'
# CACHE_EXTENTS = maxdict(200)


class memoized_extents(object):
    """ Décorateur. 
        Cache la valeur de retour d'une fonction chaque fois qu'elle est appelée.
        
        Si elle est appelée plus tard avec les mêmes arguments, la valeur mise en cache est renvoyée
       (non réévaluée).
       
       Source : https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    """
    def __init__(self, func):
        self.func = func
        self.cache = {} #maxdict(200)
    
    def __call__(self, ctx, texte):
        """ Fonction appelée quand la fonction memoïzée est appelée
        """
        if texte in self.cache.keys():
            return self.cache[texte]
        else:
            self.cache[texte] = self.func(ctx, texte)
            return self.cache[texte]

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


@memoized_extents
def text_extents(ctx, t):
    return ctx.text_extents(t)

# @memoized_extents
# def text_extents_set(ctx, t, fontsize):
#     ctx.set_fontsize(fontsize)
#     return ctx.text_extents(t)


    
    
    




def egal(x, y, epsilon = 0.1):
    """ Test d'égalité de réeles POSITIFS
        epsilon : en % du plus grand nombre
    """
    return abs(y-x) < epsilon*max(x,y)/100


def ajuster_texte(ctx, texte, w, h,
                  fdescent, fheight, 
                  le = 0.8, pe = 1.0,
                  wrap = True, couper = True):
    """ Ajuste le <texte> dans un rectangle <w,h>
        
        w, h = proportions "visées"
        le = espacement vertical des lignes (1.0 = "normal") = période en Y
        (pe = espacement vertical des paragraphes (1.0 = "normal")) pas utilisé !
        fdescent, fheight = hauteurs (sous baseline et totale) de la police

        
        Options :
            wrap = False : le texte conserve son nombre de lignes original
            couper = False : les mots ne sont jamais coupés
            
        Renvoie :
            liste des lignes
            proportions du rectangle englobant effectif (W, H)
    """
    
    #
    # Options de débuggage
    #
#     global DEBUG
#     DEBUG = "Fabrication" in texte
    if DEBUG: print("ajuster_texte :", texte[:20]+"...", w, h)
    if DEBUG: print("  couper :", couper)


    hl = fheight * le
    if DEBUG: print("  hl :", hl)

    
    # Ratio du rectangle, écarts compris

    ratioRect = (w)/(h)
    if DEBUG: print("  ratio :", ratioRect)
    #
    # Découpage du texte
    #
    i = 0
#    tps = time.time()
    if wrap:
        # Largeur initiale (sans aucun wrap)
        w_min = text_extents(ctx, texte.replace(" ", "").replace("\n", ""))[2]
        w_max = text_extents(ctx, texte)[2]

        if DEBUG: print("  w_min :", w_min)
        
        pas = text_extents(ctx, 'a')[2] # Largeur "type"

            
        # Estimation "à la louche" de la largeur de départ
        #  Calcul basé sur l'hypothèse d'un texte parfaitement ajusté
        
        # 1ere méthode : ?????????
#         delta = (1.0-1.0/le)**2 + 4*w_min/(ratioRect*hl)
#         width1 = 0.5*((1.0/le-1.0) + sqrt(delta))*ratioRect*hl
        
        # 2ème méthode
#         width2 = sqrt(w_min*hl*ratioRect)
        
        # 3ème méthode
        n0 = len(texte.split("\n"))
#         width0 = width0-(n0-1)*pas*2
#         print(hl, n0, w_min, ratioRect)
        delta = (hl*(n0-1))**2 + 4*hl*w_min/ratioRect
        width = 0.5*(hl*(n0-1) + sqrt(delta))*ratioRect
        
#         print(w_min, "::", width, "(", width1, width2, ")")
        
        if width > w_min:
            width = 0.9*w_min
        if DEBUG: print("  width0 :", width)
        
           
        ancienWrap = width
        ancienLt = []
        ancienMaxw = 0
        ancienRapport = 0
        
        continuer = True
        
        # Calcul des largeur des mots du texte
#         lignes, ptes = calcul_largeurs_lignes(ctx, texte)
        lignes = texte.splitlines()
        if DEBUG: print("  ", lignes)
        i = 0
        while continuer:
            lt = []
            
            # On découpe le texte
            i += 1
            
#             t2 = []
            for l in lignes:
                lt.extend(wordwrap(ctx, l, width, breakLongWords = couper))
                
            if lt == []:
                return lt, 0, 0
            
#             if DEBUG: print()
#             if DEBUG: print("  lt", lt)
            
            # On mémorise la longueur de la plus longue ligne 
            #    (en caractères et en unité Cairo)
            maxw = calcul_largeur(ctx, lt)
            if DEBUG: print("    maxw", maxw)
            
            ht = calcul_hauteur(fheight, fdescent, le, len(lt))
            W, H = maxw, ht        # Echelle "1"

            
            rapport = (W/H) / ratioRect
#             if DEBUG: print("  rapports", maxw/ht, "/", ratioRect)
            if DEBUG: print("  W/H", W/H)
            
            if rapport > 1:  # on a passé le cap ...
                continuer = False
                
                if i > 1 and abs(ancienRapport-1) < abs(rapport-1):
                    width = ancienWrap
                    lt = ancienLt
                    maxw = ancienMaxw
 
            else:
                ancienWrap = width
                
                if width >= w_max:#<= pas:# or (maxw == ancienMaxw and wrap < maxl) :
                    continuer = False
                    
                width += pas
                ancienLt = lt
                ancienMaxw = maxw
                ancienRapport = rapport
                
#             print(width)
    #
    # Pas de découpage du texte
    #
    else:
        lt = texte.splitlines()
        maxw = calcul_largeur(ctx, lt)

    
#     if DEBUG: print("   >>", i)
    
    #
    # Calcul des proportions effectives
    #
    ht = calcul_hauteur(fheight, fdescent, le, len(lt))
    W, H = maxw, ht
    
    #
    # On met le résultat du calcul dans le cache
    #
#     if CACHER:
#         CACHE[texte] = (w, h, le, pe, lt, W, H, fdescent, fheight)
    
    return lt, W, H




# def ajuster_texte2(ctx, texte, w, h, le = 0.8, pe = 1.0, b = 0.4, 
#                   wrap = True, couper = True, debug = False):
#     """ Ajuste le <texte> dans un rectangle <w,h>
#         
#         le = espacement vertical des lignes (1.0 = "normal") = période en Y
#         (pe = espacement vertical des paragraphes (1.0 = "normal")) pas utilisé !
#         b = écart avec les bords du rectangle (1.0 = 1em)
#         
#         Options :
#             wrap = False : le texte reste sur une ligne
#             couper = False : les mots ne sont jamais coupés
#             
#         Renvoie :
#             liste des lignes
#             taille de la police
#             taille du rectangle effectif (W, H) SANS BORDURE
#     """
#     
#     
#     #
#     # On vérifie dans le cache qu'on n'a pas déja fait le boulot
#     #
#     if texte in CACHE.keys():
#         www, hhh, bbb, lee, pee, lt, fontSize, wh = CACHE[texte]
# #         if www == w and hhh == h and lee == le and pee == pe and bbb == b:
#         if egal(www, w) and egal(hhh, h) and egal(lee, le) and egal(pee, pe) and egal(bbb, b):
# #             print("CACHE", www, hhh, bbb, lee, pee)
#             return lt, fontSize, wh
#             
#     #
#     # Options de débuggage
#     #
# #     debug = texte == u'Les projets pédagogiques et technologiques'
#     if debug: print("ajuster_texte", texte, w, h)
#     if debug: print("  couper :", couper)
# 
# 
#     #
#     # Estimation de l'encombrement du texte (pour une taille de police de 1)
#     # 
#     ctx.set_font_size(1.0 * COEF)
#     fheight = font_extents(ctx, 1.0 * COEF)[2]
# 
#     hl = fheight * le
#     if debug: print("  hl", hl)
#     
#     ecart = b * fheight * 2     # écart "total" (gauche + droite)
#     if debug: print("  ecart", ecart)
#     
#     # Ratio du rectangle, écarts compris
#     ratioRect = w/h
#     
#     #
#     # Découpage du texte
#     #
#     i = 0
# #    tps = time.time()
#     if wrap:
#         width = ctx.text_extents(texte)[2]              
#         if debug: print("  width", width)
#         
#         pas = ctx.text_extents('a')[2] # Largeur "type"
#         lignes = texte.splitlines()
#         
#         ancienWrap = width
#         ancienLt = []
#         ancienMaxw = 0
#         ancienRapport = 0
#         
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
#                 lt.extend(wordwrap(l, width, pte, breakLongWords = couper))
#                 
#             if lt == []:
#                 return lt, 1, 0
#             
#             if debug: print()
#             if debug: print("  lt", lt)
#             
#             # On mémorise la longueur de la plus longue ligne 
#             #    (en caractères et en unité Cairo)
#             maxw = calcul_largeur(ctx, lt)
#             if debug: print("  maxw", maxw)
#             
#             ht = calcul_hauteur(fheight, le, len(lt))
#             W, H = maxw + ecart, ht + ecart         # Echelle "1"
#             rapport = (W/H) / ratioRect
#             if debug: print("  rapports", maxw/ht, "/", ratioRect)
#              
#             if rapport <= 1:  # on a passé le cap ...
#                 continuer = False
# #                if debug: print "  fontSize", fontSize, ancienFontSize
#                 
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
#     #
#     # Pas de découpage du texte
#     #
#     else:
#         lt = texte.splitlines()
#         maxw = calcul_largeur(ctx, lt)
# 
# #         c = max((maxw+ecart)/w, (hl*len(lt)+ecart)/h)
# #         ratioRect = (w*c)/(h*c)
#     
#     if debug: print("   >>", i)
#     
# 
#     #
#     # Ajustement de la taille de police
#     #
#     ht = calcul_hauteur(fheight, le, len(lt))
#     W, H = maxw + ecart, ht + ecart         # Echelle "1"
#     fontSize = min(w/W, h/H)
#     
# #     W, H = W*fontSize, H*fontSize          # Echelle "reele"
#     W, H = maxw*fontSize, ht*fontSize        # Echelle "reele"
#     
#     fontSize *= COEF
#     if debug: print("  >>> fontSize :", fontSize)
#     
#     #
#     # On met le résultat du calcul dans le cache
#     #
#     CACHE[texte] = (w, h, b, le, pe, lt, fontSize, (W, H))
#     
#     return lt, fontSize, (W, H)


def ajuster_texte_fixe(ctx, texte, w, h, 
                       fdescent, fheight,
                       le = 0.8, pe = 1.0, 
                       wrap = True, couper = True):
    """ Ajuste le <texte> dans un rectangle <w,h>
        pour une taille de police fixée
        
        le = espacement vertical des lignes (1.0 = "normal") = période en Y
        (pe = espacement vertical des paragraphes (1.0 = "normal")) pas utilisé !
        
        Options :
            wrap = False : le texte reste sur une ligne
            couper = False : les mots ne sont jamais coupés
            
        Renvoie :
            liste des lignes
            proportions du rectangle englobant effectif (W, H)
    """
            
    #
    # Options de débuggage
    #
#     DEBUG = texte == "Séchoir solaire autonome"
#     DEBUG = texte == u'Les projets pédagogiques et technologiques'
    if DEBUG: print("ajuster_texte_fixe :", texte[:20]+"...", w, h)
    if DEBUG: print("  couper :", couper)

    hl = fheight * le
    if DEBUG: print("  hl", hl)
    
    #
    # Découpage du texte
    #
    if wrap:
        # Calcul des largeur des mots du texte
#         lignes, ptes = calcul_largeurs_lignes(ctx, texte)
        lignes = texte.splitlines()
        lt = []
        for l in lignes:
            lt.extend(wordwrap(ctx, l, w, breakLongWords = couper, 
                               cacher = False))
        

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
        ht = calcul_hauteur(fheight, fdescent, le, len(lt))
        if ht <= h:
            continuer = False
        elif len(lt) == 1:
            continuer = False # à gérer !!!
        else:
            lt = lt[:-1]
        
#     maxw = calcul_largeur(ctx, lt)
    maxw = max([ctx.text_extents(t)[2] for t in lt])
    
    return lt, maxw, ht





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




#----------------------------------------------------------------------
#
# wordwrap
#
# Adaptation du code :
# Name:        wx.lib.wordwrap
# Author:      Robin Dunn
#----------------------------------------------------------------------

def wordwrap(ctx, text, width, breakLongWords=True, cacher = True):
    """
    Returns a copy of text with newline characters inserted where long
    lines should be broken such that they will fit within the given
    width, with the given margin left and right, on the given `wx.DC`
    using its current font settings.  By default words that are wider
    than the margin-adjusted width will be broken at the nearest
    character boundary, but this can be disabled by passing ``False``
    for the ``breakLongWords`` parameter.
    """
    if DEBUG: print("wordwrap", width, text[:20]+"...")

#     if DEBUG: print("<<", text.splitlines())
#     if DEBUG: print("<<", text.split("\n"))
    #if DEBUG: print(type(text.splitlines()[0]), type(text.split("\n")[0]))

    wrapped_lines = []
#     for line in text.splitlines():
    line = text
    
    if DEBUG: print("     +", line)
    idx = 1
#     start = 0
    startIdx = 0
    spcIdx = -1
#         if DEBUG: print("  line", type(line), line)
#         if DEBUG: print("  pte", pte)
    while idx < len(line):
#             if DEBUG: print("  idx", idx)
        # remember the last seen space
        if line[idx] == ' ':
            spcIdx = idx

        # have we reached the max width?
        if cacher:
            ll = text_extents(ctx, line[startIdx:idx+1])[2]
        else:
            ll = ctx.text_extents(line[startIdx:idx+1])[2]
        if ll > width and (spcIdx != -1 or breakLongWords):
            if spcIdx != -1:
                idx = min(spcIdx + 1, len(line) - 1)
            wrapped_lines.append(line[startIdx : idx])
            
            spcIdx = -1
            startIdx, idx = idx, idx + max(1, (idx-startIdx)*4//5)
#                 idx += (idx-startIdx)*4//5

        idx += 1

    wrapped_lines.append(line[startIdx : idx])

    return wrapped_lines




##########################################################################################
#
#  Une zone sensible sur le dessin
#
##########################################################################################
class Zone_sens():
    def __init__(self, rect, pt_caract = None, obj = None, param = None):
        self.rect = rect                # Liste des des rectangles sensibles
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
    
    ######################################################################################  
    def estClicable(self):
        if self.obj is not None:
            return True
                        
        elif self.param is not None:
            if len(self.param) > 3 and self.param[:3] == "POS" :
                return True
            
            elif self.param == "PB":
                return True
            
            elif self.param == "EQU":
                return True
            
        return False
    
# ##########################################################################################
# #
# #  Une zone du dessin
# #
# ##########################################################################################
# class Zone():
#     def __init__(self, rect, pt_caract = None, obj = None, param = None):
#         self.rect = rect                # Liste des des rectangles sensibles
#         if pt_caract == None:
#             pt_caract = self.rect[:2]
#         self.pt_caract = pt_caract      # Un point caractéristique (pour identification svg)
#         self.obj = obj                  # L'objet concerné
#         self.param = param              # Paramètre(s) supplémentaire(s)
#         
#     def __repr__(self): 
#         return "%s (%s)" %(self.obj, self.param)
#     
#     def dansRectangle(self, X, Y):
#         """ Renvoie True si le point X, Y est dans la zone
#         """
#         for r in self.rect:
#             x, y, w, h = r
#             if X > x and Y > y and X < x + w and Y < y + h:
#                 return True
#         return False
#   
#     ######################################################################################  
#     def estClicable(self):
#         if self.obj is not None:
#             return True
#                         
#         elif self.param is not None:
#             if len(self.param) > 3 and self.param[:3] == "POS" :
#                 return True
#             
#             elif self.param == "PB":
#                 return True
#             
#             elif self.param == "EQU":
#                 return True
#             
#         return False
#     
    
    
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



def chargerParametres(lst, module, fichier):
    """ Charge les paramètres depuis un fichier de configuration
         - couleurs : nom en "*coul*", titre cfg - "Couleurs", format #FFFFFF
    
        :lst: liste des noms de variable
        :module: module d'origine des variables (globales)
        :fichier: nom du fichier de configuration
    """
#     print("chargerParametres", lst, module, fichier)
    if os.path.isfile(fichier):
        import importlib
        importlib.import_module(module)
        m = sys.modules[module]
    
        config = configparser.ConfigParser()
        
        with io.open(fichier, 'r', encoding="utf-8") as fp:
            config.readfp(fp)
            
#         print(config["Couleurs"])
        for nom in lst:
            if nom.lower() in config["Couleurs"]:
                c = couleur.CouleurCSS2Float(config.get("Couleurs", nom.lower()))
                if c is not None:
                    setattr(m, nom, c)
#                 print("  ", nom, c)


#########################################################################################################
def sauverParametres(lst, module, fichier):
    """ Sauvegarde des paramètres dans un fichier de configuration
         - couleurs : nom en "*coul*", titre cfg - "Couleurs", format #FFFFFF
    """
    print("sauverParametres", lst, module, fichier)
    
    import importlib
    importlib.import_module(module)
    m = sys.modules[module]
    
    config = configparser.ConfigParser()
    config.add_section("Couleurs")
    
    d = {}
    for nom in lst:
        print(nom)
        if hasattr(m, nom):
            l = getattr(m, nom)
        else:
            l = getattr(sys.modules[__name__], nom)

        c = couleur.CouleurFloat2CSS(l)
        print(l, ">>>", c)
        
        if len(l) != 3:
            d[nom] = c
        
    config["Couleurs"] = d
            
    config.write(open(fichier,'w', encoding="utf-8"))
        
        
        