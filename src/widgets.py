#!/usr/bin/env python
# -*- coding: utf-8 -*-


##This file is part of pySequence

#############################################################################
#############################################################################
##                                                                         ##
##                                  widgets                                ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2009-2010 Cédrick FAURY
##
## pySéquence : aide à la construction
## de Séquences et Progressions pédagogiques
## et à la validation de Projets

#    pySequence is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
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
Module ``widgets``
******************

Différents widgets perso pour wx


"""
import re
import wx
import wx.adv as adv
import md_util
import util_path
import time, os, sys
import  wx.lib.scrolledpanel as scrolled
from wx.lib.wordwrap import wordwrap
import images
from pathvalidate import sanitize_filepath

import version
DEBUG = version.DEBUG

#############################################################################################################
#
# Pour convertir les images en texte
# 
#############################################################################################################
import base64, io
from wx.lib.embeddedimage import PyEmbeddedImage
try:
    b64encode = base64.b64encode
except AttributeError:
    b64encode = base64.encodestring
    
# import tempfile

def img2str(img):
    """
    """
    # Ca ne marche pas : pas en PNG, str trop longue !
    #return b64encode(img.GetData())
    
    # Version BytesIO : plus rapide que la version fichier (-20%)
    s = io.BytesIO()
    img.SaveFile(s, wx.BITMAP_TYPE_PNG)
    s.seek(0)
#     str(img2str(self.icone.ConvertToImage()), 'utf-8')
    return str(b64encode(s.read()), 'utf-8')


def str2img(data):
    if data is not None and data != "":
        try:
            return PyEmbeddedImage(data).GetBitmap()
        except:
            pass

            

def b64(img):
    return str(b"data:image/png;base64,"+base64.b64encode(img), 'utf-8')
        
        
    
    
######################################################################################  
#
#   Fonctions de passage en locale EN momentané
#    (pendant le chargement d'images PNG)
#
######################################################################################  
loc = None
def locale2EN():
    """ Passage momentané en Anglais (bug de wxpython)
    """
    global loc
    loc = wx.GetApp().locale.GetSystemLanguage()
    wx.GetApp().locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        
def locale2def():
    """ Retour au locale par défaut
    """
    wx.GetApp().locale = wx.Locale(loc)
        
######################################################################################  
#
#   Classe permettant de gérer la grammaire des éléments
#
######################################################################################  
class Grammaire():
    def __init__(self, nom_code):
        """ :nom_code: nom de l'objet au format "nom(s)$g"
                        avec g = "f", "m", "q"
            
        """ 
        
        self.SetNomCode(nom_code)
        
        
    def egal(self, gra):
        if hasattr(self, 'nom_obj') and hasattr(gra, 'nom_obj'):
            return self.nom_obj == gra.nom_obj and self.genre == gra.genre
        else:
            return id(self) == id(gra)
    
    
    def SetNomCode(self, nom_code):
        ng = nom_code.split("$")
        
        self.nom_obj = ng[0]     # le nom (pluriel)
        if len(ng) > 1 and ng[1] in ["f", "m", "q"]:
            self.genre = ng[1]              # "m", "f" ou "q" pour une quantité
        else:
            self.genre = "f"                # "m", "f" ou "q" pour une quantité 
        

#     def __repr__(self):
#         return self.nom_obj
    
    def getRacine(self, mot):
        i = mot.find("(")
        if i == -1:
            return mot
        return mot[:mot.find("(")]
        
    def getFormeSP(self, mot):
        f = re.search('\(([^)]+)', mot)
        if f is None:
            return ["", ""]
        l = f.group(1).split('-')
        if len(l) == 1:
            l = [""]+l
        return l

    def getSingulier(self, txt):
        return " ".join([self.getRacine(mot) + self.getFormeSP(mot)[0] for mot in txt.split()])
        
    def getPluriel(self, txt):
        return " ".join([self.getRacine(mot) + self.getFormeSP(mot)[1] for mot in txt.split()])
    
    def voyelle(self, c):
        return c.lower() in "aeiouhéèàêîëïùû"
    
    
    def du_(self, adj = ""):
        """ article partitif singulier + nom
        """
        if self.genre == "f":
            if self.voyelle(self.nom_obj[0]):
                a = "de l'"
            else:
                a = "de la "
        
        elif self.genre in ["q","m"]:
            if self.voyelle(self.nom_obj[0]):
                a = "de l'"
            else:
                a = "du "
        
        else:
            a = ""
        
        if adj != "":
            adj += " "
        return a + self.getSingulier(adj+self.nom_obj.lower())
    
    def au_(self, adj = ""):
        """ 
        """
        if self.genre == "f":
            if self.voyelle(self.nom_obj[0]):
                a = "à l'"
            else:
                a = "à la "
        
        elif self.genre in ["q","m"]:
            if self.voyelle(self.nom_obj[0]):
                a = "à l'"
            else:
                a = "au "
        
        else:
            a = ""
        
        if adj != "":
            adj += " "
        return a + self.getSingulier(adj+self.nom_obj.lower())
    
    
    def ce_(self, adj = ""):
        """ 
        """
        if self.genre == "f":
            a = "cette "
        
        elif self.genre in ["q","m"]:
            if self.voyelle(self.nom_obj[0]):
                a = "cet "
            else:
                a = "ce "
        
        else:
            a = ""
        
        if adj != "":
            adj += " "
        return a + self.getSingulier(adj+self.nom_obj.lower())
    
    
    def de_(self, adj = ""):
        """ article ??? singulier + nom
        """
        if self.voyelle(self.nom_obj[0]) and adj == "":
            a = "d'"
        else:
            a = "de "
        
        if adj != "":
            adj += " "
        return a + self.getSingulier(adj+self.nom_obj.lower())
    
    
    def de_plur_(self, adj = ""):
        """ article ??? singulier + nom
        """
        if self.voyelle(self.nom_obj[0]) and adj == "":
            a = "d'"
        else:
            a = "de "
        
        if adj != "":
            adj += " "
        return a + self.getPluriel(adj+self.nom_obj.lower())
    
    def des_(self, adj = ""):
        """ article partitif pluriel + nom
        """
        if adj != "":
            adj += " "
        return "des "+self.getPluriel(adj+self.nom_obj.lower())
    
    
    def les_(self, adj = ""):
        """ article défini pluriel + nom
        """
        if adj != "":
            adj += " "
        return "les "+self.getPluriel(adj+self.nom_obj.lower())
    
    
    def le_(self, adj = ""):
        """ article défini singulier + nom
        """
        if self.voyelle(self.nom_obj[0]) and adj == "":
            a = "l'"
        else:
            if self.genre == "f":
                a = "la "
            else:
                a = "le "
        
        if adj != "":
            adj += " "
        return a + self.getSingulier(adj+self.nom_obj.lower())
     
    
    
    def un_(self, adj = ""):
        """ article indéfini pluriel + nom
        """
        if self.genre == "f":
            a = "une "
        elif self.genre == "m":
            a = "un "
        elif self.genre == "q":
            a = "du "
        else:
            a = ""
        if adj != "":
            adj += " "
        return a + self.getSingulier(adj+self.nom_obj.lower())
    

    def sing_(self):
        return self.getSingulier(self.nom_obj.lower())
    
    def Sing_(self):
        return self.getSingulier(self.nom_obj.capitalize())
    
    
    def plur_(self):
        return self.getPluriel(self.nom_obj.lower())
    
    def Plur_(self):
        return self.getPluriel(self.nom_obj.capitalize())
    
    
    
    
    
    
    
    
    
    
######################################################################################
def getSingulierPluriel(txt, pluriel):
    if pluriel:
        return getPluriel(txt)
    else:
        return getSingulier(txt)

def getMots(txt):
    return txt.split()

def getPluriel(txt):
    return txt.replace("(", "").replace(")", "")

def getSingulier(txt):
    return txt.replace("(s)", "").replace("(x)", "")
    
def et2ou(txt):
    return txt.replace(" et ", " ou ")




######################################################################################  
def isstring(s):
    return isinstance(s, str)


######################################################################################  
def getNomFichier(prefixe, intitule, extension = r""):
    nomFichier = prefixe+"_"+intitule
    for c in ["\t", "\n", "\"", "/", "\\", "?", "<", ">", "|", ":", "."]:
        nomFichier = nomFichier.replace(c, r"_")
    return sanitize_filepath(nomFichier+extension)

######################################################################################  
def rallonge(txt):
    return " "+txt+" "


######################################################################################  
def sublist(sub, lst):
    l = [e for e in sub if e in lst]
    return len(l) == len(sub)

######################################################################################  
def pourCent(v, ajuster = False):
    if ajuster:
        return str(int(round(v*100))).rjust(3)+"%"
    else:
        return str(int(round(v*100)))+"%"

######################################################################################  
def pourCent2(v, ajuster = False):
    if ajuster:
        return str(int(v*100)).rjust(3)+"%"
    else:
        return str(int(v*100))+"%"

######################################################################################  
def remplaceLF2Code(txt):
#     print("remplaceLF2Code", txt)
    d = {"##13##" : ["\n",
                      "\u000D\u000A", #CRLF
                      "\u000A", #LF
                      "\u000D", #CR
                      "\u000B", #VT
                      "\u000C", #FF
                      "\u2028", #LS
                      "\u2029", #LS
                      ]}
    for k, lv in d.items():
        for v in lv:
            txt = txt.replace(v, k)
#     print("  >>", txt)
    return txt
    
    
######################################################################################  
def remplaceCode2LF(txt):
    return txt.replace("##13##", "\n")#&#13")
    


#####################################################################################
# Fonction statistiques
# (http://stackoverflow.com/questions/15389768/standard-deviation-of-a-list)
#####################################################################################
def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5


#
# Fonction pour réaliser l'intersection de deux filtres
#
def intersection(f1, f2):
    """ Fonction pour réaliser l'intersection de deux filtres
        None = pas de filtrage
    """
    if f1 is None:
        return f2
    if f2 is None:
        return f1
    return list(set(f1).intersection(f2))




#
# Fonction pour vérifier si un point x, y est dans un rectangle (x0, y0, x1, y1)
#
def dansRectangle(x, y, rect):
    """ Renvoie True si le point x, y est dans un des rectangles de la liste de rectangles r(xr, yr, wr, hr)
    """
    for i, r in enumerate(rect):
        if x > r[0] and y > r[1] and x < r[0] + r[2] and y < r[1] + r[3]:
            return True, i
    return False, 0


def getAncreFenetre(x, y, w, h, W, H, e = 0):
    """ Renvoie la meilleure position (maximum de visibilité dans l'écran)
        x, y : position de référence (pointeur, ...)
        w, h : dimension de la fenêtre à afficher
        W, H : dimension de l'écran
        e : ecart (pour que x, y soit à l'intérieur de la fenêtre
    """
    if w-x < x+w-W:
        X = x-w +e
    else:
        X = x -e
        
        
    if h-y < y+h-H:
        Y = y-h +e
    else:
        Y = y -e
        
    return X, Y




#########################################################################################################
#########################################################################################################
#
#  Variable
#
#########################################################################################################
#########################################################################################################  

#
# Types de variable
#
VAR_ENTIER = 0
VAR_ENTIER_POS = 1
VAR_REEL = 2
VAR_REEL_POS = 4
VAR_REEL_SUPP1 = 8
VAR_REEL_POS_STRICT = 16

FONT_SIZE_VARIABLE = 100

#
# Nombre de chiffres significatifs retenus
#
NB_CHIFFRES = 4
EPSILON = 1E-6

#
# Correcteur de variable (pour contourner un bug de scipy concernant le calcul des r�ponses)
#
CORRECTEUR_VARI = 1.0#1.000000001

class Variable:
    def __init__(self, nom, lstVal = [0.0], nomNorm = "", typ = VAR_REEL, 
                 bornes = [None,None], modeLog = True,
                 expression = None, multiple = False, 
                 data = None):
        self.n = nom
        self.nn = nomNorm
        if type(lstVal) != list:
            self.v = [lstVal]
        else:
            self.v = lstVal
        self.t = typ
        self.bornes = bornes
        self.modeLog = modeLog
        self.multiple = multiple
        self.data = data
        # Si la variable fait partie d'une expression
        self.expression = expression
        
    
    #########################################################################################################
    def __repr__(self):
        return self.n+" = "+str(self.v)+"("+str(self.t)+")"


    #########################################################################################################
    def GetData(self):
        return self.data
        
        
    #########################################################################################################
    def redefBornes(self, bornes):
        self.bornes = bornes
        for n in range(len(self.v)):
            if self.v[n] > self.bornes[1]:
                self.v[n]  = self.bornes[1]
            elif self.v[n] < self.bornes[0]:
                self.v[n]  = self.bornes[0]


    #########################################################################################################
    def Augmenter(self, coef = 1):
        if self.t == VAR_ENTIER or self.t == VAR_ENTIER_POS or not self.modeLog:
            for n in range(len(self.v)):
                if self.EstValide(self.v[n] + coef):
                    self.v[n] += coef
            
    #########################################################################################################
    def Diminuer(self, coef = 1):
        if self.t == VAR_ENTIER or self.t == VAR_ENTIER_POS or not self.modeLog:
            for n in range(len(self.v)):
                if self.EstValide(self.v[n] - coef):
                    self.v[n] += -coef

                
    #########################################################################################################
    def setValeur(self, val, num = 0):
        if self.EstValide(val):
            self.v[num] = val
        
        
    #########################################################################################################
    def ChangerSigne(self):
        for n in range(len(self.v)):
            self.v[n] = -self.v[n]
            
            
    #########################################################################################################
    def EstValideStr(self, val):
#        print "validStr?",val, type(val), eval(val)
        
        try:
            if len(val) > 1:
                val = val.lstrip('0')
            v = eval(val)
            return self.EstValide(v), v
        except NameError:
            return False, None
        except SyntaxError:
            return False, None
        except:
            return False, None    
        
        
    #########################################################################################################
    def EstValide(self, val):
#        print "valid?",val, type(val), self.t
        v = val
        
        if self.t == VAR_ENTIER:
            if type(v) == int:
                return self.EstDansBornes(v)
        elif self.t == VAR_ENTIER_POS:
            if type(v) == int and v >= 0:
                return self.EstDansBornes(v)
        elif self.t == VAR_REEL:
            return self.EstDansBornes(v)
        elif self.t == VAR_REEL_POS:
            if v >= 0:
                return self.EstDansBornes(v)
        elif self.t == VAR_REEL_SUPP1:
            if v >= 1:
                return self.EstDansBornes(v)
        elif self.t == VAR_REEL_POS_STRICT:
            if v > 0:
                return self.EstDansBornes(v)    
        
        return False
    
    
    #########################################################################################################
    def EstDansBornes(self, v):
        return      (self.bornes[0] == None or v >= self.bornes[0]) \
                and (self.bornes[1] == None or v <= self.bornes[1])
   
   
#########################################################################################################
#########################################################################################################
#
#  Expression math�matique avec variables
#
#########################################################################################################
#########################################################################################################  
GREEK = ['alpha', 'beta', 'chi', 'delta', 'epsilon', 'gamma', 'lambda', 'mu', 'nu', 'omega',\
         'phi', 'psi', 'rho', 'sigma', 'tau', 'theta', 'xi', 'Delta', 'Gamma', 'Lambda', 'Omega', \
         'Phi', 'Psi', 'Sigma', 'Theta', 'Xi', 'Nabla', 'pi']

#make a list of safe functions
safe_list = ['math', 'abs', 'ceil', 'cos', 'cosh', 'degrees', \
             'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', \
             'pi', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']

#d�sactivation de numpy
#from numpy import abs, ceil, cos, cosh, degrees, \
#             exp, fabs, floor, fmod, frexp, hypot, ldexp, log, log10, modf, \
#             pi, radians, sin, sinh, sqrt, tan, tanh, errstate 

#use the list to filter the local namespace 
safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])

math_list = safe_list + ['*', '/', '+', '^', '-', '(', ')']



class Expression():
    """ Expression mathématique 
    """
    def __init__(self, expr = ''):
        self.MiseAJour(expr)
        
        
    ######################################################################################################
    def MiseAJour(self, expr = ''):
        # Une chaine apte à subir un 'eval'
        #    (une expression évaluable par python)
        self.py_expr = expr.replace('^', '**')
        
        
        # Cr�ation d'un dictionnaire de Variables : {'nom' : Variable}
        vari = self.getVariables()
#        print "vari =",vari
        self.vari = {}
        for n, v in list(vari.items()):
            if n in GREEK:
                nn = r""+"\\"+n
            else:
                nn = n
            self.vari[n] = Variable(nn, lstVal = [v], typ = VAR_REEL, expression = self)

        # Une chaine mathText
        self.math = self.getMplText()
        

    ######################################################################################################
    def IsConstante(self):
        return len(self.vari) == 0
    
    
    
    ######################################################################################################
    def evaluer(self):
        """ Renvoie une valeur numérique de l'expression
        """
        
        # On cr�e un dictionnaire de variables : {'nom' : valeur}
        #    (nécessaire pour "eval")

#         dict = {}
        for n, v in self.vari.items():
            print(" ", n, v)
            dict[n] = v.v[0]
        
        global safe_dict
        dict.update(safe_dict)
        
        # On fait l'évaluation
        try:
            v = eval(self.py_expr, {"__builtins__": None}, dict)
        except:
            return False
#        print type (v)
        # On analyse le résultat
        if not type(v) == float  and not type(v) == int:
            return False
        else:
            return v
    
    
    ######################################################################################################
    def parentheses(self):
        """ Renvoie l'expression mise entre parenth�ses
            si cela se doit !!
        """
        if '+' in self.math or '-' in self.math or '/' in self.math:
            return r"\left({"+self.math+r"}\right)"
        else:
            return self.math
     
     
        
    ######################################################################################################
    def getMplText(self):
        """ Renvoie une chaine compatible mathtext de Matplotlib
        """
        expr = self.py_expr
        
        def getMath(expr):
            continuer = True
            i = 0
            p = 0
            while continuer:
                if i >= len(expr) - 1:
                    continuer = False
                    return expr
                
                # Séparation des principaux termes de l'expression
                elif expr[i] == '+' or expr[i] == '-':
                    continuer = False
                    a, _, c = expr.partition(expr[i])
                    return '{'+a+'}'+expr[i]+getMath(c)
                
                
                
                # Traitement des sous-expressions entre parenthèses
                elif expr[i] == '(':
                    p = 1
                    j = i+1
                    continuer2 = True
                    while continuer2:
                        if j > len(expr) - 1:
                            continuer2 = False
                            ssex = '#'
                        elif expr[j] == '(':
                            p += 1
                        elif expr[j] == ')':
                            p += -1
                        if p == 0:
                            continuer2 = False
                            ssex = getMath(expr[i+1:j])
                        j += 1
                    continuer2 = False
                    
                    # On fait si besoin des paquets entre crochets {} ou traits verticaux ||
                    if i>0 and (expr[i-1] == '^' or expr[i-1] == '_') \
                        or i>3 and expr[i-4:i] == 'sqrt' \
                        or i>2 and expr[i-3:i] == 'exp':
                        expr = expr[0:i] + '{' + ssex + '}' + expr[j:]
                        i = j-1
                    elif i>2 and expr[i-3:i] == 'abs':
                        expr = expr[0:i] + '\vert' + ssex + '\vert' + expr[j:]
                        i = j+7
                    else:
                        expr = expr[0:i] + '({' + ssex + '})' + expr[j:]
                        i = j+1
        
                # Séparation des produits
                elif expr[i] == '*':
                    continuer = False
                    a, _, c = expr.partition(expr[i])
                    return a+expr[i]+getMath(c)
                
                # Séparation des quotients
                elif expr[i] == '/':
                    continuer = False
                    a, _, c = expr.partition(expr[i])
                    j = 0
                    p = 0
                    continuer3 = True
                    while continuer3:
                        if j > len(c) - 1:
                            continuer3 = False
                            c1 = c
                            c2 = ""
                        elif c[j] == '(':
                            p += 1
                        elif c[j] == ')':
                            p += -1
                        
                        elif p == 0 and (c[j] == "+" or c[j] == "*" or c[j] == "-"):
                            continuer3 = False
                            c1 = c[:j]
                            c2 = c[j:]
                            
                        elif p == 0 and c[j] == "/":
                            c = c[:j]+'*'+c[j+1:]
                            
                            
                        j += 1
                    continuer3 = False
                    
                    return r'\frac{' + a + r'}{' + getMath(c1)+r'}'+getMath(c2)
                
#                # Traitement des fractions
#                elif expr[i] == '/':
#                    a, b, c = expr.partition(expr[i])
#                    continuer = False
#                    return r'\frac{' + a + r'}{' + getMath(c)+r'}'
                
                    
                i += 1
        
        
        
        ex1 = getMath(expr)
        
        
        
        # Traitement global de l'expression pour la rendre compatible avec mathtext
        ex1 = ex1.replace('(', r"\left(")
        ex1 = ex1.replace(')', r"\right)")
        
        for m in ['abs', 'ceil', 'cos', 'cosh', \
             'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', \
             'pi', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']:
            ex1 = ex1.replace(r"*"+m, r""+m)
            
            
        ex1 = ex1.replace('sqrt', r"\sqrt")
        for g in GREEK:
            ex1 = ex1.replace(g, r""+"\\"+g)
        
            
        ex1 = ex1.replace('exp', r"e^")
        
        
#        print ex1
        
        return ex1
        
        
    #########################################################################################################
    def getVariables(self):
        """ Analyse de la chaine (prétendue expression mathématique)
            et renvoie un dictionnaire {nom : valeur}
        """
        expr = self.py_expr

        # Découpage le la chaine autour des opérateurs
        for i in math_list:
            expr = expr.replace(i,'#')
        expr = expr.split('#')
        
        # Création du dictionnaire de variables
        b={}
        for i in expr:
            try:
                float(i)      # C'est une constante
            except:         # C'est une variable
                if i.strip()!='':
                    b[i] = 1. # On lui affecte la valeur 1.0
  
        return b
    
    
    
    
    
    
#########################################################################################################
#########################################################################################################
#
#  Le Crtl pour controler une variable
#
#########################################################################################################    
##########################################################################################################
myEVT_VAR_CTRL = wx.NewEventType()
EVT_VAR_CTRL = wx.PyEventBinder(myEVT_VAR_CTRL, 1)

#----------------------------------------------------------------------

class VarEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.var = None

    def SetVar(self, var):
        self.var = var

    def GetVar(self):
        return self.var


class VariableCtrl(wx.Panel):
    def __init__(self, parent, variable, coef = None, signeEgal = True, 
                 slider = False, fct = None, help = "", sizeh = -1, color = wx.BLACK, 
                 unite = "", sliderAGauche = False, scale = 1.0):
        wx.Panel.__init__(self, parent, -1)#, style = wx.BORDER_SIMPLE)
        
        if coef == None:
            if variable.t == VAR_ENTIER or variable.t == VAR_ENTIER_POS:
                self.coef = 1
            else:
                sensibilite = 20
                self.coef = 10**(1.0/sensibilite)
        else:
            self.coef = coef
        
        # Une fonction d'activation/désactivation du zoomauto à l'utilisation du slider
        self.fct = fct
        self.etatInit = None
        
        self.multiple = variable.multiple
        #
        # Nom de la variable (titre)
        #
        self.variable = variable
        self.help = help
        self.signeEgal = signeEgal
        
        txt = self.variable.n
        if signeEgal:
            txt += " ="

        txtnom = wx.StaticText(self, -1, txt, style = wx.ALIGN_RIGHT)
        txtnom.SetForegroundColour(color)
        self.txtnom = txtnom
            
        if len(help) > 0:
            txtnom.SetToolTip(help)
            
        #
        # Valeur de la variable
        #
        self.text = wx.TextCtrl(self, -1, self.lstToText(self.variable.v), 
                                size = (sizeh, -1))#,
        
        if len(help) > 0:
            self.text.SetToolTip(help)
        else:
            if self.variable.nn == "":
                txtn = "de la variable "+self.variable.n
            else:
                txtn = self.variable.nn
            self.text.SetToolTip("Saisir la valeur "+txtn)
            
        self.Bind(wx.EVT_TEXT, self.OnChar, self.text)
#        self.Bind(wx.EVT_CHAR, self.OnChar, self.text)
        
        #
        # Contrôle de la variable
        #
        h = self.text.GetSize()[1]*1.1
        self.spin = wx.SpinButton(self, -1, size = (2*h/3, h), style = wx.SP_VERTICAL | wx.SP_ARROW_KEYS)#
        
        self.spin.SetRange(-100, 100)
        self.spin.SetValue(0)
        if len(help) > 0:
            self.spin.SetToolTip(help)
        else:
            self.spin.SetToolTip("Agir ici pour augmenter/diminuer la valeur "+txtn)

        self.Bind(wx.EVT_SPIN_UP, self.OnSpinUp, self.spin)
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown, self.spin)
        
        #
        # Unité
        #
        self.unite = wx.StaticText(self, -1, unite)#,
        self.unite.SetForegroundColour(color)
        if len(help) > 0:
            self.unite.SetToolTip(help)
            
        # Mise en place
        sizer = wx.BoxSizer( wx.HORIZONTAL)
        sizer.Add(txtnom, 0, wx.ALIGN_CENTRE_VERTICAL|wx.LEFT, 3)
        if sliderAGauche:
            sizer.Add(self.spin, 0, wx.ALIGN_CENTRE|wx.LEFT, 4)
            sizer.Add(self.text, 0, wx.ALIGN_CENTRE|wx.RIGHT, 4)
        else:
            sizer.Add(self.text, 0, wx.ALIGN_CENTRE|wx.LEFT, 4)
            sizer.Add(self.spin, 0, wx.ALIGN_CENTRE|wx.RIGHT, 4)
        sizer.Add(self.unite, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.RIGHT, 3)
        self.SetSizer(sizer)
    
    
    #########################################################################################################
    def SetHelp(self, text):
        self.help = text
        if len(self.help) > 0:
            self.txtnom.SetToolTip(self.help)
            self.text.SetToolTip(self.help)
            self.spin.SetToolTip(self.help)
        
        
    #########################################################################################################
    def SetForegroundColour(self, color):
        self.txtnom.SetForegroundColour(color)
        
    #########################################################################################################
    def SetMin(self, m):
        self.spin.SetMin(m)
        self.variable.bornes[0] = m
         
    #########################################################################################################
    def SetVariable(self, variable):
        self.multiple = variable.multiple
        self.variable = variable
        
        txt = self.variable.n
        if self.signeEgal:
            txt += " ="

        self.txtnom.SetLabel(txt)
        
        if len(self.help) == 0:
            if self.variable.nn == "":
                txtn = "de la variable "+self.variable.n
            else:
                txtn = self.variable.nn
            self.text.SetToolTip("Saisir la valeur "+txtn)
        
        
    #########################################################################################################
    def Renommer(self, nom):
        self.txtnom.SetLabel(nom)
#        self.vs.Layout()
        self.Layout()
        self.Fit()
        
    
    #########################################################################################################
    def sendEvent(self):
        # Pour contourner un bug de scipy ...
        for i in range(len(self.variable.v)-1):
            self.variable.v[i] = self.variable.v[i]
#        print "Variable :",self.variable.n, self.variable.v[0]
        evt = VarEvent(myEVT_VAR_CTRL, self.GetId())
        evt.SetVar(self.variable)
        self.GetEventHandler().ProcessEvent(evt)
    
    
#    #########################################################################################################
#    def OnLeave( self, event ):    
#        print "Leave"
#        self.Parent.SetFocus()
        
    #########################################################################################################
    def OnScroll( self, event ):
#        if self.release: 
#            self.release = False
#            return
#        
#        print "OnScroll", event.GetPosition()
        
        pos = event.GetPosition()
        if pos != self.lastPos:
            
            # Quand on commence le Scroll, on "désactive"
            if self.etatInit == None:
                self.etatInit = self.fct() # Etat d'activation initial
                self.fct(False) # Désactivation
            
            # Effet du Scroll ...
            coef = 10.0 **((pos-self.lastPos) / 100.0)
            self.variable.Augmenter(coef)
        
            self.mofifierValeurs()
            self.lastPos = pos
        
            # On remet dans l'état d'activation initial (avant Scroll)
            self.fct(self.etatInit) # Etat d'activation initial
            self.etatInit = None
        
        
    #########################################################################################################
    def OnScrollRelease( self, event ):
#        print "ScrollRelease"
        # On remet le slider au milieu
#        self.release = True
        self.sli.SetValue(0)
        self.lastPos = 0
        
#        # On remet dans l'�tat d'activation initial (avant Scroll)
#        self.fct(self.etatInit) # Etat d'activation initial
#        self.etatInit = None
        
    #########################################################################################################
    def redefBornes(self, bornes):
        self.variable.redefBornes(bornes)
        self.mofifierValeursSsEvt()

    #########################################################################################################
    def setValeur(self, val):
        self.variable.setValeur(val)
        self.mofifierValeursSsEvt()
        
    #########################################################################################################
    def OnSpinUp( self, event ):
#        print "SpinUp", self.coef
        self.variable.Augmenter(self.coef)
        self.mofifierValeurs()
        
        
    #########################################################################################################
    def OnSpinDown( self, event ):
#        print "SpinDown", self.coef
        self.variable.Diminuer(self.coef)
        self.mofifierValeurs()
       
        
    #########################################################################################################
    def mofifierValeurs(self):
        self.text.ChangeValue(self.lstToText(self.variable.v))
        
        # On teste si la variable permet une valeur d'expression valide
        valid = True
        if self.variable.expression != None:
            try:
                e = self.variable.expression.evaluer()
            except:
                valid = False
            if e == None:
                valid = False
        if valid:
            self.sendEvent()
            self.marquerValid(True)
        else:
            self.marquerValid(False)
        
    
    #########################################################################################################
    def mofifierValeursSsEvt(self):
        self.text.ChangeValue(self.lstToText(self.variable.v))


    #########################################################################################################
    def lstToText(self, lst):
        s = ""
        for v in lst:
            s += str(v) + ' '
        return s[:-1]
        
        
    #########################################################################################################
    def getLstValeurs(self, text):
        valid = True
        lst = text.split()
        lstValeurs = []
        for t in lst:
            try:
                v = eval(t)
            except:
                v = t
                
            if type(v) == int or type(v) == float:
                lstValeurs.append(v)
            else:
                valid = False
                continue
            
        return valid, lstValeurs


    #########################################################################################################
    def OnChar(self, event):
#        val = self.text.GetValue()
        val = event.GetString()
#        key = event.GetKeyCode()

#        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
#            event.Skip()
#            return
        
#        print val#+chr(key)
        vals = val.split()
        if len(vals) > 1 and not self.multiple:
            valid = False
        elif val == "" or vals == []:
            valid = False
        else:
            valid = True
            v = []
            for vv in vals:
                valid0, v0 = self.variable.EstValideStr(vv)#+chr(key))
                valid = valid and valid0
                v.append(v0)
#            print valid, v
        
        
        # On teste si la variable permet une valeur d'expression valide
        if valid and self.variable.expression != None:
            self.variable.v = []
            for vv in v:
                self.variable.v.append(vv)
                try:
                    e = self.variable.expression.evaluer()
                except:
                    valid = valid and False
                if e == None:
                    valid = valid and False
            
        if not valid :
            self.marquerValid(False)
             
        else:
            self.variable.v = []
            for vv in v:
                self.variable.v.append(vv)
            self.marquerValid(True)
            self.sendEvent()
        event.Skip()
        
        return
    
    def marquerValid(self, etat):
        if etat:
            self.text.SetBackgroundColour(
                 wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            
        else:
            self.text.SetBackgroundColour("pink")
            self.text.SetFocus()
        
        self.Refresh()
    
    def Activer(self, etat):
        self.text.Enable(etat)
        self.spin.Enable(etat)
        

#########################################################################################################
#########################################################################################################
#
#  Tootip évolué utilisé dans divers TxtCtrl et dérivés
#
#########################################################################################################
#########################################################################################################  
# import wx.lib.agw.balloontip as BT
#  
# class ToolTip:
#  
#     def __init__(self):
#         self.tip = BT.BalloonTip(topicon=None, toptitle=u"",
#                                    message=u"a",
#                                    shape=BT.BT_RECTANGLE,
#                                    tipstyle=BT.BT_LEAVE)
#  
#         # Set the BalloonTip target
#         self.tip.SetTarget(self)
#         # Set the BalloonTip background colour
#         self.tip.SetBalloonColour(wx.WHITE)
#         # Set the font for the balloon title
#         self.tip.SetTitleFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
#         # Set the colour for the balloon title
#         self.tip.SetTitleColour(wx.BLACK)
#         # Leave the message font as default
#         self.tip.SetMessageFont()
#         # Set the message (tip) foreground colour
#         self.tip.SetMessageColour(wx.NamedColour("SLATEGREY"))
#         # Set the start delay for the BalloonTip
#         self.tip.SetStartDelay(800)
#         # Set the time after which the BalloonTip is destroyed
#         self.tip.SetEndDelay(3000)
#  
#          
#  
#     def SetToolTip(self, message):
#         """ Surcharge de la fonction du TextCtrl
#         """
# #         print message, len(message)
#         if len(message.strip()) == 0:
#             message = u"_"
#          
#         self.tip.SetBalloonMessage(message)
#  
#     def SetTitre(self, titre, bmp = None):
#         self.tip.SetBalloonTitle(titre)
#  
#  
#     def OnWidgetMotion(self, event):
#         self.tip.Destroy()
#          
#     def OnKey(self, event):
#         self.tip.Destroy()
#         event.Skip()




import wx.lib.agw.supertooltip as STT

class ToolTip():
    # ATTENTION il faut modifier supertooltip.py
    # ligne 499 : OnDestroy() 1ere ligne --> rajouter event.Skip()

    def initToolTip(self):
        
        self.tip = STT.SuperToolTip("")
        


#         self.tip.SetBodyImage(bodyImage)  
#         self.tip.SetFooter(footerText)
#         self.tip.SetFooterBitmap(footerBmp)
                    
        self.tip.SetTarget(self)
#         self.tip.SetDrawHeaderLine(drawHLine)
#         self.tip.SetDrawFooterLine(drawFLine)
# 
#         self.tip.SetDropShadow(self.dropShadow.GetValue())
#         self.tip.SetUseFade(self.useFade.GetValue())
#         self.tip.SetEndDelay(self.endTimer.GetValue())
#         
#         if self.stylesRadio.GetValue():
        self.tip.ApplyStyle('Office 2007 Blue')
        self.tip.SetEndDelay(3)
#         else:
#             self.tip.SetTopGradientColour(topColour)
#             self.tip.SetMiddleGradientColour(middleColour)
#             self.tip.SetBottomGradientColour(bottomColour)
#         self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
#         # Set the BalloonTip target
#         self.tip.SetTarget(self)
#         # Set the BalloonTip background colour
#         self.tip.SetBalloonColour(wx.WHITE)
#         # Set the font for the balloon title
#         self.tip.SetTitleFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
#         # Set the colour for the balloon title
#         self.tip.SetTitleColour(wx.BLACK)
#         # Leave the message font as default
#         self.tip.SetMessageFont()
#         # Set the message (tip) foreground colour
#         self.tip.SetMessageColour(wx.NamedColour("SLATEGREY"))
#         # Set the start delay for the BalloonTip
#         self.tip.SetStartDelay(800)
#         # Set the time after which the BalloonTip is destroyed
#         self.tip.SetEndDelay(3000)

#     def OnKillFocus(self, event):
#         print "OnKillFocus"
#         event.Skip()
# 
    def SetToolTip(self, message):
        """ Surcharge de la fonction du TextCtrl
        """
#         print message, len(message)
#         if len(message.strip()) == 0:
#             message = u"_"
         
        self.tip.SetMessage(message)
         

 
    def SetTitre(self, titre, bmp = None):
        if len(titre.strip()) == 0:
            titre = "_"
        self.tip.SetHeader(titre)
        if bmp is not None:
            self.tip.SetHeaderBitmap(bmp)

#     def OnWidgetMotion(self, event):
#         self.tip.Destroy()
        
#     def OnKey(self, event):
#         self.tip.Destroy()
#         event.Skip()


##################################################################################################################################################################
#
#    Classe pour gérer le plein écran
#
##################################################################################################################################################################

class FullScreenWin():
    """ Classe pour gérer le plein écran
        A attribuer aux fenêtres qui doivent être mises en plein écran
        
        winToBind : fenetre qui recoit les Bind()
        masterWin : fenetre qui possède la fonction OnKey()
    """
    def __init__(self, winToBind):
        winToBind.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        
    ######################################################################################################
    def OnResize(self, event = None):
        pass
    
    ######################################################################################################
    def OnKey(self, event = None):
        wx.GetApp().GetTopWindow().OnKey(event)
#         self.masterWin.OnKey(event)

##################################################################################################################################################################
#
#    Des widgets avec un bouton Help
#
##################################################################################################################################################################

# Une fenêtre d'aide unique
FenHelp = None

# Echelle
SSCALE = 1.0

def GetImgHelp(size):
#     return wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_MESSAGE_BOX, (16, 16))
    return scaleImage(images.Bouton_Aide.GetBitmap(), *size)

def GetIconHelp(size):
#     return wx.ArtProvider.GetIcon(wx.ART_HELP, wx.ART_FRAME_ICON, (16, 16))
    return scaleImage(images.Bouton_Aide.GetBitmap(), *size)

def CloseFenHelp():
    global FenHelp
#    print "FenHelp", FenHelp
    if FenHelp is not None:
        try:
            FenHelp.Close()
            FenHelp.Destroy()
        except:
            print("Erreur Fermeture FenHelp")
    FenHelp = None
    
class BaseGestionFenHelp():
    def OnButton(self, evt):
        global FenHelp
        
        CloseFenHelp()
        
        w = 400
        ws, hs = wx.ClientDisplayRect()[2:]
        FenHelp = md_util.MDFrame(wx.GetActiveWindow(), self.titre, self.md, 
                                  pos = (ws-w, 0), size = (w, hs))
        FenHelp.SetIcon(wx.Icon(GetIconHelp((16*SSCALE, 16*SSCALE))))
        FenHelp.Bind(wx.EVT_CLOSE, self.OnClose)
#        print self.titre
#        print FenHelp.GetBestHeight()
#        self.Fit()
#        print self.GetClientSize ()
        FenHelp.Show()
        FenHelp.Fit()
    
    def MiseAJour(self, titre, md):
        self.md = md
        self.titre = titre
        
    def OnClose(self, evt):
        global FenHelp
        FenHelp = None
        evt.Skip()
        
        
class StaticBoxButton(wx.StaticBox, BaseGestionFenHelp):
    def __init__(self, parent, Id, titre, img = None, md = ""):
        wx.StaticBox.__init__(self, parent, Id, titre)
        if img == None:
            img = GetImgHelp((16*SSCALE, 16*SSCALE))
        self.md = md
        self.titre = titre
        self.bouton = wx.BitmapButton(self, -1, img, style=wx.BORDER_NONE| wx.TAB_TRAVERSAL |wx.WS_EX_TRANSIENT)

        self.Bind(wx.EVT_BUTTON, self.OnButton, self.bouton)
        
#        self.bouton = wx.BitmapButton(parent, -1, img)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnSize(self, evt):
        w, _ = self.GetSize()
        self.bouton.SetPosition((w-22, 2))
        

class ImageButtonTransparent(wx.StaticBitmap):
    def __init__(self, parent, Id, bmp, bmp2 = wx.NullBitmap, pos = wx.DefaultPosition):
        wx.StaticBitmap.__init__(self, parent, Id, bmp, pos = pos)
        self.bmp = bmp
        self.bmp2 = bmp2
        
        if self.bmp2 == wx.NullBitmap:
            self.bmp2 = self.bmp.ConvertToImage().ConvertToGreyscale().ConvertToBitmap()
            
        self.state = False
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.Bind(wx.EVT_ENTER_WINDOW, self.enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.leave)
        
    def OnClick(self, event):
        self.state = not self.state
        event.Skip()
        
    def SetValue(self, state):
        self.state = state
        
    def MaJImage(self):
        if self.state:
            self.SetBitmap(self.bmp2)
        else:
            self.SetBitmap(self.bmp)
                
    def enter(self, event):
        self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.SetBitmap(self.bmp.ConvertToImage().Scale(self.bmp.GetWidth()*1.1, self.bmp.GetHeight()*1.1).ConvertToBitmap())
        
    def leave(self, event):
        self.SetCursor(wx.Cursor(wx.CURSOR_DEFAULT))
        self.SetBitmap(self.bmp)
        
# import  wx.lib.buttons  as  buttons


class PlaceholderTextCtrl(wx.TextCtrl):
    def __init__(self,*args,**kwargs):
        print(kwargs)
        self.default_text = kwargs.pop("placeholder","")
        kwargs["value"] = self.default_text
        print(">>", kwargs)
        wx.TextCtrl.__init__(self,*args,**kwargs)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
    
    def OnFocus(self,evt):
        if self.GetValue() == self.default_text:
            self.SetValue("")
        evt.Skip()
    
    def OnKillFocus(self,evt):
        if self.GetValue().strip() == "":
            self.SetValue(self.default_text)
        evt.Skip()


# Utilisé dans PopupInfo
class CheckBoxValue(wx.CheckBox):
    def __init__(self, *args, **kargs):
        value = eval(kargs["value"])
        del kargs["value"]
        wx.CheckBox.__init__(self, *args, **kargs)
        self.SetValue(value)


#########################################################################################################
#########################################################################################################
#
#  Un TextCrtl avec bouton d'aide d�taiil� apparaissant quand la souris est dans le ctrl
#
#########################################################################################################
#########################################################################################################  

import orthographe

class TextCtrl_Help(orthographe.STC_ortho, BaseGestionFenHelp):
    def __init__(self, parent, titre = "", md = "", scale = 1.0):
        global SSCALE
        SSCALE = scale
        
        orthographe.STC_ortho.__init__(self, parent, -1)#, u"", style=wx.TE_MULTILINE)
        
        img = GetImgHelp((16*SSCALE, 16*SSCALE))
        img.SetMaskColour("white")
        self.bouton = wx.BitmapButton(self, -1, img, style=wx.BORDER_NONE)
#        self.bouton = buttons.GenBitmapButton(self, -1, img, style=wx.BORDER_NONE)
        self.bouton.SetBackgroundColour("white")
        self.bouton.Hide()
        self.md = md
        self.titre = titre
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.bouton)
        
        self.bouton.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.bouton.SetToolTip("Obtenir de l'aide supplémentaire")
        
#        self.bouton.Bind(wx.EVT_ENTER_WINDOW, self.OnButtonEnter)
        self.bouton.Bind(wx.EVT_LEAVE_WINDOW, self.OnButtonLeave)
    
    def OnEnter(self, evt):
        if len(self.md) > 0:
            self.bouton.Show()
        evt.Skip()
        
        
    def OnMotion(self, evt):
        t = self.GetToolTip()
        if t is not None:
#             print "OnMotion"
            t.SetAutoPop(0)
            t.SetAutoPop(3)
#         t = self.GetToolTipString()
#         self.SetToolTip(t)
#             print dir(t)
#             print t.Tip
            
        evt.Skip()
        
        
    def OnLeave(self, evt):
        w, h = self.GetSize()
        if evt.x > w-3 or evt.y < 2 or evt.x < 2 or evt.y > h-2:
            self.bouton.Hide()
        evt.Skip()

#    def OnButtonEnter(self, evt):
#        self.bouton.Show()
#        evt.Skip()

    def OnButtonLeave(self, evt):
        w, _ = self.GetSize()
        if evt.x > w-3 or evt.y < 2:
            self.bouton.Hide()
        evt.Skip()


    def OnSize(self, evt):
        w, _ = self.GetSize()
#        print self.md
#        print w, h , self.GetSize()[0]-self.GetClientSize()[0]
        if self.GetSize()[0]-self.GetClientSize()[0] > 10 :
            d = 22 + 15
        else:
            d = 22
        self.bouton.SetPosition((w-d, 2))
        evt.Skip()

###############################################################################################
# source : https://wiki.wxpython.org/DoubleBufferedDrawing
###############################################################################################
class BufferedWindow(wx.Window):
    '''
     A Buffered window class.

     To use it, subclass it and define a Draw() method that takes a DC
     to draw to. In that method, put the code needed to draw the picture
     you want. The window will automatically be double buffered, and the
     screen will be automatically updated when a Paint event is received
     (USE_BUFFERED_DC = True).

     When the drawing needs to change, your app needs to call the
     UpdateDrawing() method. Since the drawing is stored in a bitmap, you
     can also save the drawing to file by calling the SaveToFile() method.
    '''
    def __init__(self, *args, **kwargs):
        # Make sure the NO_FULL_REPAINT_ON_RESIZE style flag is set.
        # And define a new kwargs entry for wx.python
        kwargs['style'] = kwargs.setdefault('style', wx.NO_FULL_REPAINT_ON_RESIZE) | wx.NO_FULL_REPAINT_ON_RESIZE
        super().__init__( *args, **kwargs)

        # Setup event handlers for drawing 
        self.Bind(wx.EVT_PAINT,self.OnPaint)       
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None)
        self.paint_count = 0

    def Draw(self, dc):
        '''
         just here as a place holder.
         This method must be over-ridden when subclassed
        '''
        pass

    def OnPaint(self, event):
        '''
          All that is needed here is to move the buffer to the screen
        '''
        dc = wx.BufferedPaintDC(self, self._Buffer)


    def OnSize(self,event):
        '''
         The Buffer init is done here, to make sure the buffer is always
         the same size as the Window
        '''
        Size  = self.ClientSize

        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._Buffer = wx.Bitmap(*Size)
        self.UpdateDrawing()

    def SaveToFile(self, FileName, FileType=wx.BITMAP_TYPE_PNG):
        '''
         This will save the contents of the buffer
         to the specified file. See the wx.Windows docs for 
         wx.Bitmap::SaveFile for the details
        '''
        self._Buffer.SaveFile(FileName, FileType)

    def UpdateDrawing(self):
        '''
         This would get called if the drawing is changed, for whatever reason.

         The idea here is that the drawing is based on some data generated
         elsewhere in the system. If that data changes, the drawing needs to
         be updated.

         This code re-draws the buffer, then calls Update, which forces a paint event.
        '''
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.Draw(dc)
        del dc      # need to get rid of the MemoryDC before Update() is called.
        self.Refresh()
        self.Update()
        
        

#########################################################################################################
#########################################################################################################
#
#  Un slider à deux positions
# source : https://gist.github.com/gabrieldp/e19611abead7f6617872d33866c568a3
#########################################################################################################
#########################################################################################################  

def fraction_to_value(fraction, min_value, max_value):
    return int((max_value - min_value) * fraction + min_value+0.5)


def value_to_fraction(value, min_value, max_value):
    return float(value - min_value) / (max_value - min_value)


class SliderThumb:
    def __init__(self, parent, value, decal = 0):
        self.parent = parent
        self.decal = decal
        self.dragged = False
        self.mouse_over = False
#         self.thumb_poly = ((0, 0), (0, 13), (5, 18), (10, 13), (10, 0))
#         self.thumb_shadow_poly = ((0, 14), (4, 18), (6, 18), (10, 14))
        self.thumb_poly = ((0, 5), (5, 0), (10, 5), (10, 18), (0, 18))
        self.thumb_shadow_poly = ((0, 4), (4, 0), (6, 0), (10, 4))
        
        min_coords = [float('Inf'), float('Inf')]
        max_coords = [-float('Inf'), -float('Inf')]
        for pt in list(self.thumb_poly) + list(self.thumb_shadow_poly):
            for i_coord, coord in enumerate(pt):
                if coord > max_coords[i_coord]:
                    max_coords[i_coord] = coord
                if coord < min_coords[i_coord]:
                    min_coords[i_coord] = coord
        self.size = (max_coords[0] - min_coords[0],
                     max_coords[1] - min_coords[1])

        self.value = value
        self.normal_color = wx.Colour((0, 120, 215))
        self.normal_shadow_color = wx.Colour((120, 180, 228))
        self.dragged_color = wx.Colour((204, 204, 204))
        self.dragged_shadow_color = wx.Colour((222, 222, 222))
        self.mouse_over_color = wx.Colour((23, 23, 23))
        self.mouse_over_shadow_color = wx.Colour((132, 132, 132))

    def GetPosition(self):
        min_x = self.GetMin()
        max_x = self.GetMax()
        parent_size = self.parent.GetSize()
        min_value = self.parent.GetMin()
        max_value = self.parent.GetMax()
        fraction = value_to_fraction(self.value, min_value, max_value)
        pos = (fraction_to_value(fraction, min_x, max_x), parent_size[1] / 2 + 1)
        return pos

    def SetPosition(self, pos, minDelta = 0):
        pos_x = pos[0]
        # Limit movement by the position of the other thumb
        who_other, other_thumb = self.GetOtherThumb()
        other_pos = other_thumb.GetPosition()
        if who_other == 'low':
            pos_x = max(other_pos[0] + other_thumb.size[0]/2 + self.size[0]/2, pos_x)
        else:
            pos_x = min(other_pos[0] - other_thumb.size[0]/2 - self.size[0]/2, pos_x)
        # Limit movement by slider boundaries
        min_x = self.GetMin()
        max_x = self.GetMax()
        pos_x = min(max(pos_x, min_x), max_x)

        fraction = value_to_fraction(pos_x, min_x, max_x)
        last_value = self.value
        new_value = fraction_to_value(fraction, self.parent.GetMin(), self.parent.GetMax())
        if abs(other_thumb.value-new_value) >= minDelta:
            self.value = new_value
        # Post event notifying that position changed
        if self.value != last_value:
            self.PostEvent()
            return True
        return False

    def GetValue(self):
        return self.value

    def SetValue(self, value):
        self.value = int(value)
        # Post event notifying that value changed
#         self.PostEvent()

    def PostEvent(self):
#         print("PostEvent")
        event = wx.PyCommandEvent(wx.EVT_SLIDER.typeId, self.parent.GetId())
        event.SetEventObject(self.parent)
        wx.PostEvent(self.parent.GetEventHandler(), event)

    def GetMin(self):
        min_x = self.parent.border_width + self.size[0] / 2 + self.decal
        return min_x

    def GetMax(self):
        parent_size = self.parent.GetSize()
        max_x = parent_size[0] - self.parent.border_width - self.size[0] / 2 + self.decal
        return max_x

    def IsMouseOver(self, mouse_pos):
        in_hitbox = True
        my_pos = self.GetPosition()
        for i_coord, mouse_coord in enumerate(mouse_pos):
            boundary_low = my_pos[i_coord] - self.size[i_coord] / 2
            boundary_high = my_pos[i_coord] + self.size[i_coord] / 2
            in_hitbox = in_hitbox and (boundary_low <= mouse_coord <= boundary_high)
        return in_hitbox

    def GetOtherThumb(self):
        if self.parent.thumbs['low'] != self:
            return 'low', self.parent.thumbs['low']
        else:
            return 'high', self.parent.thumbs['high']

    def OnPaint(self, dc):
#         print("OnPaint")
        if self.dragged or not self.parent.IsEnabled():
            thumb_color = self.dragged_color
            thumb_shadow_color = self.dragged_shadow_color
        elif self.mouse_over:
            thumb_color = self.mouse_over_color
            thumb_shadow_color = self.mouse_over_shadow_color
        else:
            thumb_color = self.normal_color
            thumb_shadow_color = self.normal_shadow_color
        my_pos = self.GetPosition()

        # Draw thumb shadow (or anti-aliasing effect)
        dc.SetBrush(wx.Brush(thumb_shadow_color, style=wx.BRUSHSTYLE_SOLID))
        dc.SetPen(wx.Pen(thumb_shadow_color, width=1, style=wx.PENSTYLE_SOLID))
        dc.DrawPolygon(points=self.thumb_shadow_poly,
                       xoffset=my_pos[0] - self.size[0]/2,
                       yoffset=my_pos[1] - self.size[1]/2)
        # Draw thumb itself
        dc.SetBrush(wx.Brush(thumb_color, style=wx.BRUSHSTYLE_SOLID))
        dc.SetPen(wx.Pen(thumb_color, width=1, style=wx.PENSTYLE_SOLID))
        dc.DrawPolygon(points=self.thumb_poly,
                       xoffset=my_pos[0] - self.size[0] / 2,
                       yoffset=my_pos[1] - self.size[1] / 2)










class RangeSlider(BufferedWindow):
    def __init__(self, parent, ID=wx.ID_ANY, lowValue=None, highValue=None, minValue=0, maxValue=100, 
                 minDelta = 0, zones = [],
                 pos=wx.DefaultPosition, size=wx.DefaultSize, 
                 style=wx.SL_HORIZONTAL| wx.NO_FULL_REPAINT_ON_RESIZE, validator=wx.DefaultValidator,
                 name='rangeSlider'):
        
        self.zones = zones
        self.minDelta = minDelta
        
        if minValue > maxValue:
            minValue, maxValue = maxValue, minValue
        self.min_value = minValue
        self.max_value = maxValue
        if lowValue is None:
            lowValue = self.min_value
        if highValue is None:
            highValue = self.max_value
        if lowValue > highValue:
            lowValue, highValue = highValue, lowValue
        lowValue = max(lowValue, self.min_value)
        highValue = min(highValue, self.max_value)

        self.border_width = 4

        self.thumbs = {
            'low': SliderThumb(parent=self, value=lowValue, decal = -0),
            'high': SliderThumb(parent=self, value=highValue, decal = 0)
        }
        self.thumb_width = self.thumbs['low'].size[0]

        # Aesthetic definitions
        self.slider_background_color = wx.Colour((231, 234, 234))
        self.slider_outline_color = wx.Colour((214, 214, 214))
        self.selected_range_color = wx.Colour((0, 120, 215))
        self.selected_range_outline_color = wx.Colour((0, 120, 215))
        
        
        super().__init__(parent, ID, pos=pos, size=size, style=style)
        self.SetMinSize(size=(max(50, size[0]), max(26, size[1])))
        
        # Bind events
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.OnMouseLost)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
#         self.Bind(wx.EVT_PAINT, self.OnPaint)
#         self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
#         self.Bind(wx.EVT_SIZE, self.OnResize)

    def Enable(self, enable=True):
        super().Enable(enable)
        self.Refresh()

    def Disable(self):
        super().Disable()
        self.Refresh()

    def SetValueFromMousePosition(self, click_pos):
        for thumb in self.thumbs.values():
            if thumb.dragged:
                changed = thumb.SetPosition(click_pos, minDelta = self.minDelta)
                if changed:
                    self.SetZone(thumb)
                return changed
            
        return False

    def OnMouseDown(self, evt):
        
        if not self.IsEnabled():
            return
#         print("OnMouseDown")
        click_pos = evt.GetPosition()
        for thumb in self.thumbs.values():
            if thumb.IsMouseOver(click_pos):
                thumb.dragged = True
                thumb.mouse_over = False
                break
#         refresh_needed = self.SetValueFromMousePosition(click_pos)
        self.CaptureMouse()
#         if refresh_needed:
        self.Refresh()
        self.UpdateDrawing()


    def OnMouseUp(self, evt):
        
        if not self.IsEnabled():
            return
#         print("OnMouseUp")
#         refresh_needed = self.SetValueFromMousePosition(evt.GetPosition())
        for thumb in self.thumbs.values():
            thumb.dragged = False
        if self.HasCapture():
            self.ReleaseMouse()
#         if refresh_needed:
        self.Refresh()
        self.UpdateDrawing()

    def OnMouseLost(self, evt):
#         print("OnMouseLost")
        for thumb in self.thumbs.values():
            thumb.dragged = False
            thumb.mouse_over = False
        self.Refresh()

    def OnMouseMotion(self, evt):
        if not self.IsEnabled():
            return
        refresh_needed = False
        mouse_pos = evt.GetPosition()
        if evt.Dragging() and evt.LeftIsDown():
            refresh_needed = self.SetValueFromMousePosition(mouse_pos)
        else:
            for thumb in self.thumbs.values():
                old_mouse_over = thumb.mouse_over
                thumb.mouse_over = thumb.IsMouseOver(mouse_pos)
                if old_mouse_over != thumb.mouse_over:
                    refresh_needed = True
        
        if refresh_needed:
            self.Refresh()
            self.UpdateDrawing()

    def OnMouseEnter(self, evt):
#         print("OnMouseEnter")
        if not self.IsEnabled():
            return
        mouse_pos = evt.GetPosition()
        for thumb in self.thumbs.values():
            if thumb.IsMouseOver(mouse_pos):
                thumb.mouse_over = True
                self.Refresh()
                break

    def OnMouseLeave(self, evt):
#         print("OnMouseLeave")
        if not self.IsEnabled():
            return
        for thumb in self.thumbs.values():
            thumb.mouse_over = False
        self.Refresh()

#     def OnResize(self, evt):
#         print("OnResize")
#         Size  = self.ClientSize
#         self._buffer = wx.Bitmap(*Size)
#         self.UpdateDrawing()

#     def OnPaint(self, evt):
#         dc = wx.BufferedPaintDC(self, self._buffer)
# #         evt.Skip()
    
    def Draw(self, dc):
        w, h = self.GetClientSize()
        
        background_brush = wx.Brush(self.GetBackgroundColour(), wx.SOLID)
        dc.SetBackground(background_brush)
        dc.Clear()
        
        # Draw slider
        track_height = 12
        dc.SetPen(wx.Pen(self.slider_outline_color, width=1, style=wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.Brush(self.slider_background_color, style=wx.BRUSHSTYLE_SOLID))
        dc.DrawRectangle(self.border_width, h/2 - track_height/2, w - 2 * self.border_width, track_height)
        # Draw selected range
        if self.IsEnabled():
            dc.SetPen(wx.Pen(self.selected_range_outline_color, width=1, style=wx.PENSTYLE_SOLID))
            dc.SetBrush(wx.Brush(self.selected_range_color, style=wx.BRUSHSTYLE_SOLID))
        else:
            dc.SetPen(wx.Pen(self.slider_outline_color, width=1, style=wx.PENSTYLE_SOLID))
            dc.SetBrush(wx.Brush(self.slider_outline_color, style=wx.BRUSHSTYLE_SOLID))
        low_pos = self.thumbs['low'].GetPosition()[0]
        high_pos = self.thumbs['high'].GetPosition()[0]
        dc.DrawRectangle(low_pos, h / 2 - track_height / 4, high_pos - low_pos, track_height / 2)
        # Draw thumbs
        for thumb in self.thumbs.values():
            thumb.OnPaint(dc)
        
#         del dc
#         self.Refresh(eraseBackground=False)
#         self.Update()

#     def OnEraseBackground(self, evt):
#         # This should reduce flickering
#         pass

    def GetZone(self, slider):
#         print("zones", self.zones)
        
        for z in self.zones:
            if slider == self.thumbs['high']:
                if slider.value > z[0] and slider.value <= z[-1]:
                    return z
            else:
                if slider.value >= z[0] and slider.value < z[-1]:
                    return z
        return
    
    def SetZone(self, slider):
#         print("SetZone")
        if slider == self.thumbs['low']:
            zoneMin = self.GetZone(slider)
            zoneMax = self.GetZone(self.thumbs['high'])
#             print("   l ", zoneMin, zoneMax)
            if zoneMin is not None and zoneMin == zoneMax:
                self.thumbs['low'].SetValue(zoneMin[0])
                self.thumbs['high'].SetValue(zoneMin[-1])
            elif zoneMin is not None and zoneMax is None:
                self.thumbs['low'].SetValue(zoneMin[0])
                self.thumbs['high'].SetValue(zoneMin[-1])
            elif zoneMin is None and zoneMax is not None:
                self.thumbs['high'].SetValue(self.thumbs['low'].value + self.minDelta)
        
        else:
            zoneMax = self.GetZone(slider)
            zoneMin = self.GetZone(self.thumbs['low'])
#             print("   h ", zoneMin, zoneMax)
            if zoneMax is not None and zoneMin == zoneMax:
                self.thumbs['low'].SetValue(zoneMax[0])
                self.thumbs['high'].SetValue(zoneMax[-1])
            elif zoneMax is not None and zoneMin is None:
                self.thumbs['low'].SetValue(zoneMax[0])
                self.thumbs['high'].SetValue(zoneMax[-1])
            elif zoneMax is None and zoneMin is not None:
                self.thumbs['low'].SetValue(self.thumbs['high'].value - self.minDelta)
    
    def GetValues(self):
        return [self.thumbs['low'].value, self.thumbs['high'].value]

    def SetValues(self, lowValue, highValue):
        if lowValue > highValue:
            lowValue, highValue = highValue, lowValue
        lowValue = max(lowValue, self.min_value)
        highValue = min(highValue, self.max_value)
        self.thumbs['low'].SetValue(lowValue)
        self.thumbs['high'].SetValue(highValue)
        self.Refresh()

    def GetMax(self):
        return self.max_value

    def GetMin(self):
        return self.min_value

    def SetMax(self, maxValue):
        print("SetMin", maxValue , self.min_value)
        if maxValue < self.min_value+self.minDelta:
            maxValue = self.min_value
        _, old_high = self.GetValues()
        if old_high > maxValue:
            self.thumbs['high'].SetValue(maxValue)
        self.max_value = maxValue
        self.Refresh()

    def SetMin(self, minValue):
        print("SetMin", minValue , self.max_value)
        if minValue > self.max_value-self.minDelta:
            minValue = self.max_value
        old_low, _ = self.GetValues()
        if old_low < minValue:
            self.thumbs['low'].SetValue(minValue)
        self.min_value = minValue
        self.Refresh()









# class RangeSlider2(wx.Slider):
#     def __init__(self, left_gap, right_gap, *args, **kwargs):
#         wx.Slider.__init__(self, *args, **kwargs)
#         self.SetWindowStyle(wx.SL_SELRANGE)
#         self.left_gap = left_gap
#         self.right_gap = right_gap
#         self.Bind(wx.EVT_LEFT_UP, self.on_left_click)
#         self.Bind(wx.EVT_RIGHT_UP, self.on_right_click)
#         self.Bind(wx.EVT_SCROLL_PAGEUP, self.on_pageup)
#         self.Bind(wx.EVT_SCROLL_PAGEDOWN, self.on_pagedown)
#         self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.on_slide)
#     
#         self.slider_value=self.Value
#         self.is_dragging=False
#     
#     def linapp(self, x1, x2, y1, y2, x):
#         proportion=float(x - x1) / (x2 - x1)
#         length = y2 - y1
#         return round(proportion*length + y1)
#     
#     # if left click set the start of selection
#     def on_left_click(self, e):
#     
#         if not self.is_dragging: #if this wasn't a dragging operation
#             position = self.get_position(e)
#             if position <= self.SelEnd:
#                 self.SetSelection(position, self.SelEnd)
#             else:
#                 self.SetSelection(self.SelEnd, position)
#         else:
#             self.is_dragging = False
#         e.Skip()
#     
#     # if right click set the end of selection
#     def on_right_click(self, e):
#         position = self.get_position(e)
#         if position >= self.SelStart:
#             self.SetSelection(self.SelStart, position)
#         else:
#             self.SetSelection(position, self.SelStart)
#         e.Skip()
#         
#         
#         wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_SLIDER.typeId, self.GetId()))
#     
#     # drag the selection along when sliding
#     def on_slide(self, e):
#         self.is_dragging=True
#         delta_distance=self.Value-self.slider_value
#         self.SetSelection(self.SelStart+delta_distance, self.SelEnd+delta_distance)
#         self.slider_value=self.Value
#     
#     # disable pageup and pagedown using following functions
#     def on_pageup(self, e):
#         self.SetValue(self.Value+self.PageSize)
#     
#     def on_pagedown(self, e):
#         self.SetValue(self.Value-self.PageSize)
#     
#     # get click position on the slider scale
#     def get_position(self, e):
#         click_min = self.left_gap #standard size 9
#         click_max = self.GetSize()[0] - self.right_gap #standard size 55
#         click_position = e.GetX()
#         result_min = self.GetMin()
#         result_max = self.GetMax()
#         if click_position > click_min and click_position < click_max:
#             result = self.linapp(click_min, click_max,
#                                  result_min, result_max,
#                                  click_position)
#         elif click_position <= click_min:
#             result = result_min
#         else:
#             result = result_max
#     
#         return result
# 
#     def GetRange(self):
#         return [self.SelStart, self.SelEnd]
# 
# 
# 
# class RangeSlider3(wx.Panel):
#     def __init__ (self, parent, pos, minPos, maxPos, zones = [], h = 18):
#         super(RangeSlider, self).__init__(parent, wx.ID_ANY)
# 
#         self.minPos = minPos
#         self.maxPos = maxPos
#         self.zones = zones
#         
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         
#         self.sldMax = wx.Slider(self, value=pos[1], minValue=minPos, maxValue=maxPos,
#                                 size = (-1, h), 
#                                 style=wx.SL_HORIZONTAL | wx.SL_TOP|wx.SL_SELRANGE)
#         self.sldMin = wx.Slider(self, value=pos[0], minValue=minPos, maxValue=maxPos,
#                                 size = (-1, h),
#                                 style =wx.SL_HORIZONTAL | wx.SL_BOTTOM|wx.SL_SELRANGE)
#         self.sldMax.SetMaxSize((-1, h))
#         self.sldMin.SetMaxSize((-1, h))
#         self.sldMax.Bind(wx.EVT_SCROLL, self.OnSliderScrollMax)
#         self.sldMin.Bind(wx.EVT_SCROLL, self.OnSliderScrollMin)
#         
#         sizer.Add (self.sldMin, 1, wx.EXPAND)
#         sizer.Add (self.sldMax, 1, wx.EXPAND)
#         
#         self.SetSizer (sizer)
#         
#         self.ShowRange()
#     
#     def GetRange(self):
#         return [self.sldMin.GetValue(), self.sldMax.GetValue()]
# 
# 
#     def SetValue(self, pos):
#         if pos[0] <= pos[1]:
#             self.sldMin.SetValue(pos[0])
#             self.sldMax.SetValue(pos[1])
#     
#     
#     def GetZone(self, slider):
# #         print("zones", self.zones)
#         for z in self.zones:
#             if slider.GetValue() >= z[0] and slider.GetValue() <= z[-1]:
#                 return z
#         return 
# 
# 
#     def SetZone(self, slider):
#         if slider == self.sldMin:
#             zoneMin = self.GetZone(slider)
#             zoneMax = self.GetZone(self.sldMax)
# 
#             if zoneMin is not None and zoneMin == zoneMax:
#                 self.sldMin.SetValue(zoneMin[0])
#                 self.sldMax.SetValue(zoneMin[-1])
#             elif zoneMin is not None and zoneMax is None:
#                 self.sldMin.SetValue(zoneMin[0])
#                 self.sldMax.SetValue(zoneMin[-1])
#             elif zoneMin is  None and zoneMax is not None:
#                 self.sldMax.SetValue(self.sldMin.GetValue())
#         
#         else:
#             zoneMax = self.GetZone(slider)
#             zoneMin = self.GetZone(self.sldMin)
# 
#             if zoneMax is not None and zoneMin == zoneMax:
#                 self.sldMin.SetValue(zoneMax[0])
#                 self.sldMax.SetValue(zoneMax[-1])
#             elif zoneMax is not None and zoneMin is None:
#                 self.sldMin.SetValue(zoneMax[0])
#                 self.sldMax.SetValue(zoneMax[-1])
#             elif zoneMax is  None and zoneMin is not None:
#                 self.sldMin.SetValue(self.sldMax.GetValue())
#                 
#     
#     def OnSliderScrollMax(self, e):
#         val = self.sldMax.GetValue()
#         valMin = self.sldMin.GetValue()
#         if valMin > val:
#             self.sldMin.SetValue(val)
#             
#         self.SetZone(self.sldMax)
#         self.ShowRange()
#         
#         e.Skip()
# 
#     
#     def OnSliderScrollMin(self, e):
#         val = self.sldMin.GetValue()
#         valMax = self.sldMax.GetValue ()
#         if valMax < val:
#             self.sldMax.SetValue (val)
#         
#         self.SetZone(self.sldMin)
#         self.ShowRange()
#         e.Skip()
# 
#     
#     def ShowRange(self):
#         r = self.GetRange()
#         self.sldMin.SetSelection(*r)
#         self.sldMax.SetSelection(*r)
#         self.Update()
#         self.Refresh()



#
# http://www.pythonismus.com/2013/12/wxpython-listcontrols-and-colum-sorting.html
#
import locale
import  wx.lib.mixins.listctrl  as  listmix
class ColumnSorterMixinNextGen(object):
    '''
    Self contained version of ColumnSorterMixin

    As a user you just need to use it in conjunction with ListCtrl to create a child class
    and call the constructor

    In comparison with the original there is no need to keep an itemDataMap or define the
    GetListCtrl (the latter because it is asumed the Mixin will only be used with a ListCtrl)

    I have tried to keep the interface of the ColumSorterMixin as it was. Any error can be
    assigned to me.

    Additionally I have removed the __ mangling code (may anyone be willing to subclass in the future?)
    '''

    def __init__(self):
        self.col = -1 # Keeps a reference to the last sorte column
        self.sortflags = list() # Keeps ascending/descending reference for columns
        self.sortdata = dict() # Holder for column text for he sort process

        # Assumption: always mixin with a ListCtrl
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self) # Bind to column header click

        # Replace ListCtrl.InsertColumn with own method and keep a reference
        setattr(self, 'InsertColumnOrig', self.InsertColumn)
        setattr(self, 'InsertColumn', self.InsertColumnMixin)

        # Replace ListCtrl.DeleteColumn with own method and keep a reference
        setattr(self, 'DeleteColumnOrig', self.DeleteColumn)
        setattr(self, 'DeleteColumn', self.DeleteColumnMixin)

    def OnSortOrderChanged(self):
        ''' Callback execute after the sorting process is over'''
        pass

    def OnColClick(self, event):
        '''
        When the event happens a list of column text is gathered on the fly to use it
        during the sorting process.

        This is key to avoid the user keeping external data sync'ed: the data is already in the
        control

        The rest from the original
        '''
        event.Skip()
        oldcol = self.col # refernce to last sorted column
        self.col = col = event.GetColumn() # current column to be sorted
        self.sortflags[col] = not self.sortflags[col] # invert the last sorting order

        self.sortdata = dict() # prepare the data holder
        for index in range(0, self.GetItemCount()):
            # loop over all items and gather the ItemData and ColumnText
            itemdata = self.GetItemData(index)
            item = self.GetItem(index, col)
            self.sortdata[itemdata] = item.GetText()

        self.SortItems(self.GetColumnSorter()) # Sort
        if wx.Platform != "__WXMAC__" or \
           wx.SystemOptions.GetOptionInt("mac.listctrl.always_use_generic") == 1:
            # If needed and possible update the images
            self.UpdateImages(oldcol)
            
        self.OnSortOrderChanged() # go to the notification callback


    def GetColumnSorter(self):
        """Returns a callable object to be used for comparing column values when sorting."""
        return self.ColumnSorter

    def GetSecondarySortValues(self, col, key1, key2):
        """Returns a tuple of 2 values to use for secondary sort values when the
           items in the selected column match equal.  The default just returns the
           item data values."""
        return (key1, key2)

    def ColumnSorter(self, key1, key2):
        '''
        In comparison with the original we don't need the column, because the
        data for the specific column has been already gathered and saved along the key (item data)
        '''
        ascending = self.sortflags[self.col]
        item1 = self.sortdata[key1]
        item2 = self.sortdata[key2]

        #--- Internationalization of string sorting with locale module
        if type(item1) == str and type(item2) == str:
            cmpVal = locale.strcoll(item1, item2)
        elif type(item1) == str or type(item2) == str:
            cmpVal = locale.strcoll(str(item1), str(item2))
        else:
            cmpVal = cmp(item1, item2)

        # If the items are equal then pick something else to make the sort value unique
        if not cmpVal:
            cmpVal = cmp(*self.GetSecondarySortValues(self.col, key1, key2))

        return cmpVal if ascending else -cmpVal

    def InsertColumnMixin(self, col, heading, format=wx.LIST_FORMAT_LEFT, width=-1):
        '''
        Replaces ListCtrl InsertColumn to keep the ascending/descending sort flags sync'ed
        with column insertion

        The reason to do this: if put on the right hand side of the "base classes" list
        a plain InsertColumn method would not be found and Mixins are usually put on the right
        hand side
        '''
        index = self.InsertColumnOrig(col, heading, format, width)
        if index != -1:
            # Colum inserte: Insert a sorting flag in the returned index
            self.sortflags.insert(index, False)
            if self.col >= index:
                # Fix the index of the last sorted column because we added to the left
                self.col += 1

        return index

    def DeleteColumnMixin(self, col):
        '''
        Replaces ListCtrl DeleteColumn to keep the ascending/descending sort flags sync'ed
        with column insertion

        The reason to do this: if put on the right hand side of the "base classes" list
        a plain InsertColumn method would not be found and Mixins are usually put on the right
        hand side
        '''
        deleted = self.DeleteColumnOrig(col)
        if deleted:
            self.sortflags.pop(col)
            if self.col == col:
                # Last sorted column ... removed ... invalidate index
                self.col = -1
            elif self.col > col:
                # Keep the index sync'ed, since we removed from the left
                self.col -= 1

    def GetSortState(self):
        """
        Return a tuple containing the index of the column that was last sorted
        and the sort direction of that column.
        Usage:
        col, ascending = self.GetSortState()
        # Make changes to list items... then resort
        self.SortListItems(col, ascending)
        """
        return (self.col, self.sortflags[self.col])

    def GetSortImages(self):
        """
        Returns a tuple of image list indexesthe indexes in the image list for an image to be put on the column
        header when sorting in descending order.
        """
        return (-1, -1)  # (decending, ascending) image IDs

    def UpdateImages(self, oldcol):
        sortImages = self.GetSortImages()
        if self.col != -1 and sortImages[0] != -1:
            img = sortImages[self.sortflags[self.col]]
            if oldcol != -1:
                self.ClearColumnImage(oldcol)
            self.SetColumnImage(self.col, img)

    def GetColumnWidths(self):
        """
        Returns a list of column widths.  Can be used to help restore the current
        view later.
        """
        rv = list()
        for col in range(self.GetColumnCount()):
            rv.append(self.GetColumnWidth(col))
        return rv

    def SortListItems(self, col=-1, ascending=True):
        """Sort the list on demand.  Can also be used to set the sort column and order."""
        oldcol = self.col
        if col != -1:
            self.col = col
            self.sortflags[col] = ascending
        self.SortItems(self.GetColumnSorter())
        self.UpdateImages(oldcol)

class ListCtrlMixed(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin, ColumnSorterMixinNextGen):
    def __init__(self, parent, ID):
        wx.ListCtrl.__init__(self, parent, ID, style = wx.LC_REPORT| wx.LC_EDIT_LABELS| wx.LC_SORT_ASCENDING)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.TextEditMixin.__init__(self)
        ColumnSorterMixinNextGen.__init__(self)

class EditableListCtrl(wx.Panel):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size = wx.DefaultSize,
                 img = (wx.NullBitmap, wx.NullBitmap), 
                 hlp = ("Ajouter", "Supprimer la selection")):
        
        wx.Panel.__init__(self, parent, ID)
        self.listCtrl = ListCtrlMixed(self, -1)
#         self.Bind(wx.EVT_UPDATE_UI, self.OnUpdate)
        
        self.tb = wx.ToolBar(self, -1)
        
        tsize = (20,20)
        self.tb.SetToolBitmapSize(tsize)
        
      
        self.IDajout = wx.NewId()
        self.tb.AddTool(self.IDajout, "Ajouter", scaleImage(img[0], *tsize), wx.NullBitmap,
                             shortHelp = hlp[0], 
                             longHelp  = hlp[0])
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=self.IDajout)
        

        self.IDsuppr = wx.NewId()
        self.tb.AddTool(self.IDsuppr, "Supprimer", scaleImage(img[1], *tsize),  wx.NullBitmap,
                             shortHelp = hlp[1], 
                             longHelp  = hlp[1])
        self.tb.Realize()
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=self.IDsuppr)
        
        
        #
        # Mise en place
        #
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.tb, 1, flag = wx.EXPAND)
        self.sizer.Add(self.listCtrl, flag = wx.EXPAND)
        
        self.SetSizer(self.sizer)
        
    
    def InsertColumn(self, *args, **kargs):
        self.listCtrl.InsertColumn(*args, **kargs)
        
        
    def OnToolClick(self, event):
#         print "OnToolClick", self.listCtrl.GetItemCount()
        if event.GetId() == self.IDajout:
            n = self.listCtrl.GetItemCount()
            newindex = self.listCtrl.InsertItem(n, self.listCtrl.GetColumn(0).GetText() + str(n))
            
            for col in range(self.listCtrl.GetColumnCount()-1):
                self.listCtrl.SetItem(newindex, col + 1, self.listCtrl.GetColumn(col+1).GetText() + str(n))
    
            self.listCtrl.SetItemData(newindex, wx.NewId())
            
        else:
            for i in self.GetSelectedItems():
                self.listCtrl.DeleteItem(i)
        event.Skip()
    
    
    def SetListItem(self, items):
        for data in items:
            n = self.listCtrl.GetItemCount()
            newindex = self.listCtrl.InsertItem(n, data[0])
            for col in range(self.listCtrl.GetColumnCount()-1):
                self.listCtrl.SetItem(newindex, col + 1, data[col+1])
    
            self.listCtrl.SetItemData(newindex, wx.NewId())
    
    
    def GetListItem(self):
        count = self.listCtrl.GetItemCount()
        cols = self.listCtrl.GetColumnCount()
        l = []
        for row in range(count):
            l.append([])
            for col in range(cols):
                item = self.listCtrl.GetItem(itemIdx=row, col=col)
                l[-1].append(item.GetText())
        return l
    
    
    def GetSelectedItems(self):
        """    Gets the selected items for the list control.
        Selection is returned as a list of selected indices,
        low to high.
        """
        selection = []
        index = self.listCtrl.GetFirstSelected()
        if index == -1:
            return selection
        selection.append(index)
        while len(selection) != self.listCtrl.GetSelectedItemCount():
            index = self.listCtrl.GetNextSelected(index)
            selection.append(index)
    
        return selection
#     def SetToolBitmapSize(self.tsize):
#         self.tb.SetToolBitmapSize(tsize)
#         
#     def AddLabelTool(self, *args, **kargs):
#         self.tb.AddLabelTool(*args, **kargs)
#         
#     def OnUpdate(self, event):
#         print 'OnUpdate', self.GetColumnCount()
#         self.SetColumnCount(self.GetColumnCount())
#         event.Skip()

    
try:
    import wx.combo as combo
except:
    import wx.adv as combo
    
class CustomComboBox(combo.BitmapComboBox):
    def __init__(self, *args, **kargs):
        combo.BitmapComboBox.__init__(self, *args, **kargs)




import xml.etree.ElementTree as ET
from util_path import SYSTEM_ENCODING
##################################################################################################    
def enregistrer_root(root, nomFichier, dialog = True, xml_declaration = False):
#     fichier = open(nomFichier, 'w')
    try:
        ET.ElementTree(root).write(nomFichier, 
                                   xml_declaration=xml_declaration, 
                                   encoding = SYSTEM_ENCODING)
        return True
    
    except IOError:
        if dialog:
            messageErreur(None, "Accès refusé", 
                                  "L'accès au fichier %s a été refusé !\n\n"\
                                  "Essayer de faire \"Enregistrer sous...\"" %nomFichier)
    
    except UnicodeDecodeError:
        if dialog:
            messageErreur(None, "Erreur d'encodage", 
                                  "Un caractère spécial empêche l'enregistrement du fichier !\n\n"\
                                  "Essayer de le localiser et de le supprimer.\n"\
                                  "Merci de reporter cette erreur au développeur.")
    return False
#     fichier.close()
    




def safeParse(nomFichier, toplevelwnd, silencieux = False):
    if not os.path.isfile(nomFichier):
        return
    
    fichier = open(nomFichier,'r', encoding='utf-8')
    parser = ET.XMLParser(encoding="utf-8")
#     print(nomFichier)
#     root = ET.parse(fichier, parser = parser).getroot()
#     fichier.close()
#     return root
    
    
    try:
        root = ET.parse(fichier, parser = parser).getroot()
        fichier.close()
        return root
     
    except:# ET.ParseError:
        if not silencieux:
            messageErreur(toplevelwnd, "Fichier corrompu", 
                              "Le fichier suivant est corrompu !!\n\n"\
                              "%s\n\n" \
                              "Il est probablement tronqué suite à un echec d'enregistrement." %util_path.toSystemEncoding(nomFichier))
        fichier.close()
#         if DEBUG: raise



#############################################################################################################
def messageErreur(parent, titre, message, icon = wx.ICON_WARNING):
    dlg = wx.MessageDialog(parent, message, titre,
                           wx.OK | icon)
    dlg.ShowModal()
    dlg.Destroy()

#############################################################################################################
def messageWarning(parent, titre, message, icon = wx.ICON_WARNING):
    dlg = wx.MessageDialog(parent, message, titre,
                           wx.OK | icon)
    dlg.ShowModal()
    dlg.Destroy()
    
#############################################################################################################
def messageInfo(parent, titre, message, icon = wx.ICON_INFORMATION):
    dlg = wx.MessageDialog(parent, message, titre,
                           wx.OK | icon)
    dlg.ShowModal()
    dlg.Destroy()
    
#############################################################################################################
def messageYesNo(parent, titre, message, icon = wx.ICON_INFORMATION):
    dlg = wx.MessageDialog(parent, message, titre,
                           wx.YES_NO | icon)
    retCode = dlg.ShowModal()
    dlg.Destroy()
    if retCode == wx.ID_YES:
        return True
    else:
        return False

#############################################################################################################
def chronometrer(fct, *args, **kargs):
    tps1 = time.clock()
    result = fct(*args, **kargs)
    tps2 = time.clock()    
    return tps2 - tps1, result


def getHoraireTxt(v, prefixe = ""): 
    h, m = divmod(v*60, 60)
    h = str(int(h))
    if m == 0:
        m = ""
    else:
        m = "%02d" %m
    if h == "0":
        return prefixe+m+"'"
    else:
        return prefixe+h+"h"+m
    
#############################################################################################################
def rognerImage(image, wf = 800.0 , hf = 600.0): 
#     print "rognerImage"
    w, h = image.GetSize()
#     print "   ", w, h
    r = max(w/float(wf), h/float(hf), 1)
    _w, _h = w/r, h/r
#     print "   >>", _w, _h
    return image.ConvertToImage().Scale(_w, _h).ConvertToBitmap()

#############################################################################################################
def scaleImage(image, wf = 24 , hf = None):
    if hf is None:
        hf = wf
    return image.ConvertToImage().Scale(int(wf), int(hf), quality = wx.IMAGE_QUALITY_HIGH ).ConvertToBitmap()


#############################################################################################################
def scaleIcone(image, wf = 20 , hf = 20): 
    i = wx.Icon()
    bmp = image.ConvertToImage().Scale(wf, hf, quality = wx.IMAGE_QUALITY_HIGH ).ConvertToBitmap()
    i.CopyFromBitmap(bmp)
    return i

#############################################################################################################
import textwrap
def tronquer_(texte, taille):
    if len(texte) == 0:
        return texte
    ligne1 = textwrap.wrap(texte, taille, break_long_words = False)[0]
    if len(ligne1) > taille:
        ligne1 = ligne1[:taille-3]+'...'
    return ligne1

# Source : http://stackoverflow.com/questions/250357/truncate-a-string-without-ending-in-the-middle-of-a-word
def tronquer(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

def tronquerDC(texte, taille, wnd, suffix = '...'):
#     print "tronquerDC", taille
#     print "   ", texte
    
    dc = wx.ClientDC(wnd)
    t = wordwrap(texte, taille, dc).split("\n")[0]
    if len(t) < len(texte):
        ts = t + suffix
    else:
        return texte
#     print "   ", ts
#     print "   >", dc.GetTextExtent(ts)[0]
    
    # V�rification
    if dc.GetTextExtent(ts)[0] > taille:
#         print "  __", dc.GetTextExtent(t)[0]
        s = dc.GetTextExtent(suffix)[0]
        return wordwrap(t, taille-s, dc).split()[0] + suffix
    else:
        return ts
    


# Source : http://stackoverflow.com/questions/8302301/limiting-statictext-width
class EllipticStaticText(wx.StaticText):

    def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, name="ellipticstatictext"):
        """
        Default class constructor.

        :param `parent`: the L{EllipticStaticText} parent. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `label`: the text label;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the static text style;
        :param `name`: the window name.
        """

        wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for L{EllipticStaticText}.

        :param `event`: a `wx.SizeEvent` event to be processed.
        """

        event.Skip()
        self.Refresh()


    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for L{EllipticStaticText}.

        :param `event`: a `wx.EraseEvent` event to be processed.

        :note: This is intentionally empty to reduce flicker.
        """

        pass


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for L{EllipticStaticText}.

        :param `event`: a `wx.PaintEvent` to be processed.
        """

        dc = wx.BufferedPaintDC(self)        
        width, height = self.GetClientSize()

        if not width or not height:
            return

        clr = self.GetBackgroundColour()

        backBrush = wx.Brush(clr, wx.SOLID)

        dc.SetBackground(backBrush)
        dc.Clear()

        if self.IsEnabled():
            dc.SetTextForeground(self.GetForegroundColour())
        else:
            dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))

        dc.SetFont(self.GetFont())

        label = self.GetLabel()
        text = self.ChopText(dc, label, width)

        dc.DrawText(text, 0, 0)


    def ChopText(self, dc, text, max_size):
        """
        Chops the input `text` if its size does not fit in `max_size`, by cutting the
        text and adding ellipsis at the end.

        :param dc: a `wx.DC` device context;
        :param text: the text to chop;
        :param max_size: the maximum size in which the text should fit.
        """

        # first check if the text fits with no problems
        x, _ = dc.GetTextExtent(text)

        if x <= max_size:
            return text

        textLen = len(text)
        last_good_length = 0

        for i in range(textLen, -1, -1):
            s = text[0:i]
            s += "..."

            x, _ = dc.GetTextExtent(s)
            last_good_length = i

            if x < max_size:
                break

        ret = text[0:last_good_length] + "..."    
        return ret









class MyEditableListBox(adv.EditableListBox):
    def __init__(self, *args, **kargs):
        adv.EditableListBox.__init__(self, *args, **kargs)
        
#         self.GetEditButton().SetToolTip("Éditer")
    
    def AppendColumn(self, *args, **kargs):
        self.GetListCtrl().AppendColumn(*args, **kargs)









class DisplayChoice(wx.Dialog):
    def __init__(self, parent):
        
        
#         s = (600,600)
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, "Choisir un écran")
        
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#FFB6C1")
#         panel.SetMinSize(s)
        
#         st = wx.StaticText(panel, -1,
#                           u"Choisir un écran", pos = (0,0))
        
#         bsizer = wx.BoxSizer(wx.HORIZONTAL)
        # Détection multiples écrans
        X, Y = [], []
        W, H = [], []
        for idx in range(wx.Display.GetCount()):
            d = wx.Display(idx)
            c = 10
            X.append(d.GetGeometry()[0]/c)
            Y.append(d.GetGeometry()[1]/c)
            W.append(d.GetGeometry()[2]/c)
            H.append(d.GetGeometry()[3]/c)
            
        xm, ym = 0, 0
        for idx in range(wx.Display.GetCount()):
            d = wx.Display(idx)
#             print d.IsPrimary(), d.GetGeometry()
            x, y, w, h = X[idx]-min(X), Y[idx]-min(Y), W[idx], H[idx]
            
#             print x, y, w, h
            b = wx.Button(panel, 100+idx, str(idx+1), pos = (x,y+30), size = (w,h), style=wx.NO_BORDER)
            t = "Ecran %s" %str(idx+1)
            if d.IsPrimary():
                t += "\nprincipal"
            b.SetToolTip(t)
            
            self.Bind(wx.EVT_BUTTON, self.OnClick, b)
#             bsizer.Add(b, 1)
            
            xm = max(xm, x+w)
            ym = max(ym, y+30+h)
        
        panel.SetSize((xm, ym))
            
        self.Fit()
        self.Layout()
        
        x, y, w, h = parent.GetRect().Get()
        self.SetPosition((x+w/2-panel.GetSize()[0]/2,
                          y+h/2-panel.GetSize()[1]/2))
        
        self.res = None
        
    def OnClick(self, event):
       
        d = wx.Display(event.GetId()-100)
        self.res = d.GetGeometry()[0:2]
        self.Close()

    def GetValue(self):
        return self.res
    
#     def OnPaint(self, evt):
#         print "OnPaint"
#         pdc = wx.PaintDC(self)
#         try:
#             dc = wx.GCDC(pdc)
#         except:
#             dc = pdc
#         rect = wx.Rect(0,0, 100, 100)
#         for RGB, pos in [((178,  34,  34), ( 50,  90)),
#                          (( 35, 142,  35), (110, 150)),
#                          ((  0,   0, 139), (170,  90))
#                          ]:
#             r, g, b = RGB
#             penclr   = wx.Colour(r, g, b, wx.ALPHA_OPAQUE)
#             brushclr = wx.Colour(r, g, b, 128)   # half transparent
#             dc.SetPen(wx.Pen(penclr))
#             dc.SetBrush(wx.Brush(brushclr))
#             rect.SetPosition(pos)
#             dc.DrawRoundedRectangleRect(rect, 8)
            

##########################################################################################
#
#    Elément au format XML enregistrable
#        les attributs commençant par "_" sont ignorés
#
##########################################################################################        
class XMLelem():
    ######################################################################################  
    def getBranche(self, nomb = ""):
        """ Construction et renvoi d'une branche XML
            (enregistrement de fichier)
        """
#        print "getBranche", self._codeXML, self
        if nomb != "":
            nomb = "_" + nomb
        ref = ET.Element(str(self._codeXML+nomb))

        def sauv(branche, val, nom = None):
            nom = nom.replace("\n", "--")
            if type(val) == str or type(val) == str:
                branche.set("S_"+nom, val.replace("\n", "--"))
            elif type(val) == int:
                branche.set("I_"+nom, str(val))
            elif type(val) == int:
                branche.set("L_"+nom, str(val))
            elif type(val) == float:
                branche.set("F_"+nom, str(val))
            elif type(val) == bool:
                branche.set("B_"+nom, str(val))
            elif type(val) == list or type(val) == tuple:
                sub = ET.SubElement(branche, "l_"+nom)
                for i, sv in enumerate(val):
                    sauv(sub, sv, format(i, "02d"))
            elif type(val) == dict:
                sub = ET.SubElement(branche, "d_"+nom)
                for k, sv in list(val.items()):
                    if type(k) != str and type(k) != str:
                        k = "_"+format(k, "02d")
                    sauv(sub, sv, k)
            elif isinstance(val, XMLelem):
                branche.append(val.getBranche(nom))
                
                
        for attr in dir(self):
            if attr[0] != "_":
                val = getattr(self, attr)
                sauv(ref, val, attr)
            
        return ref
        
    
        
        
    ######################################################################################
    def setBranche(self, branche, module = ""):
        """ Lecture de la branche XML
            (ouverture de fichier)
        """
        print("setBranche", self._codeXML, self)
    
        nomerr = []
        
        def lect(branche, nom = ""):
            if nom[:2] == "S_":
                return str(branche.get(nom)).replace("--", "\n")
            
            elif nom[:2] == "I_":
                return int(branche.get(nom))
            
            elif nom[:2] == "L_":
                return int(branche.get(nom))
            
            elif nom[:2] == "F_":
                return float(branche.get(nom))
            
            elif nom[:2] == "B_":
                return branche.get(nom)[0] == "T"
            
            elif nom[:2] == "l_":
                sbranche = branche.find(nom)
                if sbranche == None: return []
                dic = {}
                
                # éléments "simples" : dans les items
                for k, sb in list(sbranche.items()):
#                     _k = k[2:]
                    _k = k.split("_")[-1]
                    if isinstance(_k, str) and "--" in _k:
                        _k = _k.replace("--", "\n")
                    dic[_k] = lect(sbranche, k)
                
                
                
                # éléments plus complexes : comme sous-élément
                for sb in list(sbranche):
                    k = sb.tag
#                     _k = k[2:]
                    _k = k.split("_")[-1]
                    if isinstance(_k, str) and "--" in _k:
                        _k = _k.replace("--", "\n")
                    dic[_k] = lect(sbranche, k)
                    
                liste = [dic[v] for v in sorted(dic)]
#                 print nom, liste
#                 print "   ", sorted(dic)
                
          
                return liste
#                liste = [lect(sbranche, k) for k, sb in sbranche.items()]
#                return liste + [lect(sb, k) for k, sb in list(sbranche)]
            elif nom[:2] == "d_":
                sbranche = branche.find(nom)
                d = {}
                if sbranche != None:
                    for k, sb in sbranche.items():
#                        print k, sb
#                        _k = k[2:]
                        _k = k.split("_")[1]
                        if isinstance(_k, str) and "--" in _k:
                            _k = _k.replace("--", "\n")
                        d[_k] = lect(sbranche, k)
                    
                    for sb in list(sbranche):
                        k = sb.tag
#                        _k = k[2:]
                        _k = k.split("_")#[1]
                        if len(_k) == 3:#k =="":#_k[0] == "_":
                            try:
                                _k = int(_k[2])
                            except:
                                _k = "_".join(_k[1:])
                        else:
                            _k = _k[1]
                        if isinstance(_k, str) and "--" in _k:
                            _k = _k.replace("--", "\n")
                        d[_k] = lect(sbranche, k)
                return d
            
            else:
                sbranche = branche.find(nom)
#                 print(nom)
                classe = get_class(nom.split("_")[0], module = module)
#                 print(classe)
                obj, err = classe().setBranche(sbranche)
                print(">>>", obj)
                nomerr.extend(err)
                return obj

 

        for attr in dir(self):
            if attr[0] != "_":
                val = getattr(self, attr)
                if type(val) == str or type(val) == str:
                    _attr = "S_"+attr
                elif type(val) == int:
                    _attr = "I_"+attr
                elif type(val) == int:
                    _attr = "L_"+attr
                elif type(val) == float:
                    _attr = "F_"+attr
                elif type(val) == bool:
                    _attr = "B_"+attr
                elif type(val) == list:
                    _attr = "l_"+attr
                elif type(val) == dict:
                    _attr = "d_"+attr
                else:
                    _attr = None
                print("attr:",_attr)
                if _attr != None:
                    v = lect(branche, _attr.replace("\n", "--"))
                    setattr(self, attr, v)

        return self, nomerr


    ######################################################################################  
    def __eq__(self, ref):
        """ Comparaison de deux référentiels
        """
        if not isinstance(ref, type(self)):
            return False
        
        def egal(val1, val2):
            if isinstance(val1, str) and isinstance(val2, str):
#                if val1 != val2:#.replace("\n", "--"):
#                    print "Erreur str : xml =", val1, "      xls =", val2#.replace("\n", "--")
                return val1 == val2#.replace("\n", "--")
            
            elif type(val1) == bool and type(val2) == bool:
#                if val1 != val2:
#                    print "Erreur bool: xml =", val1, "      xls =", val2
                return val1 == val2
            
            elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
#                if val1 != val2:
#                    print "Erreur num: xml =", val1, "      xls =", val2
                return val1 == val2
            
            elif type(val1) == list:
                if len(val1) != len(val2):
#                    print "Erreur list: xml =", val1, "      xls =", val2
                    return False
                
                return all([egal(sval1, sval2) for sval1, sval2 in zip(val1, val2)])
                
#                 e = True
#                 for sval1, sval2 in zip(val1, val2):
#                     e = e and egal(sval1, sval2)
#                 return e
            
            elif type(val1) == dict and type(val2) == dict:
                if not egal(sorted(val1), sorted(val2)):
#                    print "Erreur dict : xml =", val1, "      xls =", val2
                    return False
                return all([egal(v, val2[k]) for k, v in list(val1.items())])
                
#                 e = True
#                 for k, v in val1.items():
# #                    if isinstance(k, (str, unicode)):
# #                        k = k.replace("--", "\n")
#                     e = e and egal(v, val2[k])
#                 return e
            
            elif isinstance(val1, XMLelem) and isinstance(val2, XMLelem):
#                print "XMLelem", val1 == val2
                return val1 == val2
            
            else:
#                print "Erreur : xml =", val1, "      xls =", val2
                return False
        
        for attr in dir(self):
            if attr[0] != "_":
                val1 = getattr(self, attr)
                if isinstance(val1, (str, int, float, bool, list, dict, XMLelem)) :
                    val2 = getattr(ref, attr)
                    if not egal(val1, val2):
#                         print u"Différence", ""
#                         print "  ", attr
#                         print "  xml:", val1
#                         print "  xls:", val2
                        break
                        return False
        return True


def get_class( kls ,module = "" ):
    parts = kls.split('.')
    if module == "":
        module = ".".join(parts[:-1])
        parts = parts[1:]
    
#     print("  ", parts)
    
    m = __import__( module )
    for comp in parts:
        m = getattr(m, comp)            
    return m

##########################################################################################
#
#    Classe permettant le traitement d'action avec délai
#        (pour limiter la fréquence des actions longues ...)
#
##########################################################################################        
from wx.lib.delayedresult import startWorker
class DelayedResult():
    def __init__(self, func):
        self.t = None
        self.func = func
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

    #-------------------------------------------------------------------------
    def OnTimer(self, event):
        # Start another thread which will update the bitmap
        # But only if another is not still running!
        if self.t is None:
            self.timer.Stop()
            self.t = startWorker(self.ComputationDone, self.func)
            
#     def Compute(self):
#         """ Fonction à surcharger
#         """
#         pass
#     
    #-------------------------------------------------------------------------
    def ComputationDone(self, r):
        # source : https://stackoverflow.com/questions/5732952/draw-on-image-buffer-memorydc-in-separate-thread
        # When done, take bitmap and place it to the drawing buffer
        # Invalidate panel, so it is redrawn
        # But not if the later thread is waiting!
#         temp = r.get()
#         try:
        if not self.timer.IsRunning():
#             print("ComputationDone")
#             self.buffer = temp
            self.Refresh()
            self.Update()
#         except:
#             print("Erreur Computation")
        self.t = None


