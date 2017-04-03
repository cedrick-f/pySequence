#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

#############################################################################
#############################################################################
##                                                                         ##
##                               CedWidgets                                ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2009-2010 Cédrick FAURY

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import wx

import time, os
import  wx.lib.scrolledpanel as scrolled
from wx.lib.wordwrap import wordwrap


######################################################################################  
def isstring(s):
    return isinstance(s, (str, unicode))


######################################################################################  
def getNomFichier(prefixe, intitule, extension = r""):
    nomFichier = prefixe+"_"+intitule
    for c in [u"\t", u"\n", "\"", "/", "\\", "?", "<", ">", "|", ":", "."]:
        nomFichier = nomFichier.replace(c, r"_")
    return nomFichier+extension

######################################################################################  
def rallonge(txt):
    return u" "+txt+" "


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
    return txt.replace("\n", "##13##")#.replace("\n", "##13##")#&#13")
    
    
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
# Correcteur de variable (pour contourner un bug de scipy concernant le calcul des réponses)
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
        
    def __repr__(self):
        return self.n+" = "+str(self.v)+"("+str(self.t)+")"

    #########################################################################################################
    def redefBornes(self, bornes):
        self.bornes = bornes
        for n in range(len(self.v)):
            if self.v[n] > self.bornes[1]:
                self.v[n]  = self.bornes[1]
            elif self.v[n] < self.bornes[0]:
                self.v[n]  = self.bornes[0]


    def Augmenter(self, coef = 1):
        if self.t == VAR_ENTIER or self.t == VAR_ENTIER_POS or not self.modeLog:
            for n in range(len(self.v)):
                if self.EstValide(self.v[n] + coef):
                    self.v[n] += coef

        else:
            for n in range(len(self.v)):
                v, d = roundN(self.v[n] * coef, nc = 2)
                if self.EstValide(v):
                    self.v[n] = v
            
    def Diminuer(self, coef = 1):
        if self.t == VAR_ENTIER or self.t == VAR_ENTIER_POS or not self.modeLog:
            for n in range(len(self.v)):
                if self.EstValide(self.v[n] - coef):
                    self.v[n] += -coef
        else:
            for n in range(len(self.v)):
                v, d = roundN(self.v[n] / coef, nc = 2)
                if self.EstValide(v):
                    self.v[n] = v
                
    #########################################################################################################
    def setValeur(self, val, num = 0):
        if self.EstValide(val):
            self.v[num] = val
        
    def ChangerSigne(self):
        for n in range(len(self.v)):
            self.v[n] = -self.v[n]
            
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
    
    def EstDansBornes(self, v):
        return      (self.bornes[0] == None or v >= self.bornes[0]) \
                and (self.bornes[1] == None or v <= self.bornes[1])
   
   
#########################################################################################################
#########################################################################################################
#
#  Expression mathématique avec variables
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

#désactivation de numpy
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
        
        
        # Création d'un dictionnaire de Variables : {'nom' : Variable}
        vari = self.getVariables()
#        print "vari =",vari
        self.vari = {}
        for n, v in vari.items():
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
        
        # On crée un dictionnaire de variables : {'nom' : valeur}
        #    (nécessaire pour "eval")

        dict = {}
        for n, v in self.vari.items():
            print " ", n, v
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
        """ Renvoie l'expression mise entre parenthèses
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
                    a, b, c = expr.partition(expr[i])
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
                    a, b, c = expr.partition(expr[i])
                    return a+expr[i]+getMath(c)
                
                # Séparation des quotients
                elif expr[i] == '/':
                    continuer = False
                    a, b, c = expr.partition(expr[i])
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
        
        
        
        # Traitement global de l'expression pour la remdre compatible avec mathtext
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
                 slider = False, fct = None, help = "", sizeh = -1, color = wx.BLACK, unite = u"", sliderAGauche = False):
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
            txtnom.SetToolTipString(help)
            
        #
        # Valeur de la variable
        #
        self.text = wx.TextCtrl(self, -1, self.lstToText(self.variable.v), size = (sizeh, -1))#,
        
        if len(help) > 0:
            self.text.SetToolTipString(help)
        else:
            if self.variable.nn == "":
                txtn = u"de la variable "+self.variable.n
            else:
                txtn = self.variable.nn
            self.text.SetToolTipString(u"Saisir la valeur "+txtn)
            
        self.Bind(wx.EVT_TEXT, self.OnChar, self.text)
#        self.Bind(wx.EVT_CHAR, self.OnChar, self.text)
        
        #
        # Contrôle de la variable
        #
        self.spin = wx.SpinButton(self, -1, size = (15,25), style = wx.SP_VERTICAL | wx.SP_ARROW_KEYS)
        
        self.spin.SetRange(-100, 100)
        self.spin.SetValue(0)
        if len(help) > 0:
            self.spin.SetToolTipString(help)
        else:
            self.spin.SetToolTipString(u"Agir ici pour augmenter/diminuer la valeur "+txtn)

        self.Bind(wx.EVT_SPIN_UP, self.OnSpinUp, self.spin)
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown, self.spin)
        
        #
        # Unité
        #
        self.unite = wx.StaticText(self, -1, unite)#,
        
        sizer = wx.BoxSizer( wx.HORIZONTAL)
        sizer.Add(txtnom, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT, 3)
        if sliderAGauche:
            sizer.Add(self.spin, 0, wx.ALIGN_CENTRE|wx.LEFT, 4)
            sizer.Add(self.text, 0, wx.ALIGN_CENTRE|wx.RIGHT, 4)
        else:
            sizer.Add(self.text, 0, wx.ALIGN_CENTRE|wx.LEFT, 4)
            sizer.Add(self.spin, 0, wx.ALIGN_CENTRE|wx.RIGHT, 4)
        sizer.Add(self.unite, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.RIGHT, 3)
        self.SetSizer(sizer)
    
    
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
                txtn = u"de la variable "+self.variable.n
            else:
                txtn = self.variable.nn
            self.text.SetToolTipString(u"Saisir la valeur "+txtn)
        
        
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
        
#        # On remet dans l'état d'activation initial (avant Scroll)
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
                 wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            
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
#     def SetToolTipString(self, message):
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
    # ligne 499 : rajouter event.Skip()

    def initToolTip(self):
        
        self.tip = STT.SuperToolTip(u"")
        


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
    def SetToolTipString(self, message):
        """ Surcharge de la fonction du TextCtrl
        """
#         print message, len(message)
#         if len(message.strip()) == 0:
#             message = u"_"
         
        self.tip.SetMessage(message)
         

 
    def SetTitre(self, titre, bmp = None):
        if len(titre.strip()) == 0:
            titre = u"_"
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
#    Des widgets avec un bouton Help
#
##################################################################################################################################################################

# Une fenêtre d'aide unique
FenHelp = None

def GetImgHelp():
    return wx.ArtProvider_GetBitmap(wx.ART_HELP, wx.ART_MESSAGE_BOX, (16, 16))

def GetIconHelp():
    return wx.ArtProvider_GetIcon(wx.ART_HELP, wx.ART_FRAME_ICON, (16, 16))

def CloseFenHelp():
    global FenHelp
#    print "FenHelp", FenHelp
    if FenHelp is not None:
        try:
            FenHelp.Close()
        except:
            print "Erreur Fermeture FenHelp"
    FenHelp = None
    
class BaseGestionFenHelp():
    def OnButton(self, evt):
        global FenHelp
        
        CloseFenHelp()
        
        w = 400
        ws, hs = wx.ClientDisplayRect()[2:]
        FenHelp = md_util.MDFrame(wx.GetActiveWindow(), self.titre, self.md, 
                                  pos = (ws-w, 0), size = (w, hs))
        FenHelp.SetIcon(GetIconHelp())
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
    def __init__(self, parent, Id, titre, img = None, md = u""):
        wx.StaticBox.__init__(self, parent, Id, titre)
        if img == None:
            img = GetImgHelp()
        self.md = md
        self.titre = titre
        self.bouton = wx.BitmapButton(self, -1, img, style=wx.BORDER_NONE| wx.TAB_TRAVERSAL |wx.WS_EX_TRANSIENT)

        self.Bind(wx.EVT_BUTTON, self.OnButton, self.bouton)
        
#        self.bouton = wx.BitmapButton(parent, -1, img)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnSize(self, evt):
        w, h = self.GetSize()
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
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.SetBitmap(self.bmp.ConvertToImage().Scale(self.bmp.GetWidth()*1.1, self.bmp.GetHeight()*1.1).ConvertToBitmap())
        
    def leave(self, event):
        self.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
        self.SetBitmap(self.bmp)
        
# import  wx.lib.buttons  as  buttons


class PlaceholderTextCtrl(wx.TextCtrl):
    def __init__(self,*args,**kwargs):
        print kwargs
        self.default_text = kwargs.pop("placeholder","")
        kwargs["value"] = self.default_text
        print ">>", kwargs
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
#  Un TextCrtl avec bouton d'aide détaiilé apparaissant quand la souris est dans le ctrl
#
#########################################################################################################
#########################################################################################################  

import orthographe
import md_util
class TextCtrl_Help(orthographe.STC_ortho, BaseGestionFenHelp):
    def __init__(self, parent, titre = u"", md = u""):
        orthographe.STC_ortho.__init__(self, parent, -1)#, u"", style=wx.TE_MULTILINE)
        
        img = GetImgHelp()
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
        
        self.bouton.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.bouton.SetToolTipString(u"Obtenir de l'aide supplémentaire")
        
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
#         self.SetToolTipString(t)
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
        w, h = self.GetSize()
        if evt.x > w-3 or evt.y < 2:
            self.bouton.Hide()
        evt.Skip()


    def OnSize(self, evt):
        w, h = self.GetSize()
#        print self.md
#        print w, h , self.GetSize()[0]-self.GetClientSize()[0]
        if self.GetSize()[0]-self.GetClientSize()[0] > 10 :
            d = 22 + 15
        else:
            d = 22
        self.bouton.SetPosition((w-d, 2))
        evt.Skip()



#########################################################################################################
#########################################################################################################
#
#  Un slider à deux positions
#
#########################################################################################################
#########################################################################################################  

class RangeSlider2(wx.Slider):
    def __init__(self, left_gap, right_gap, *args, **kwargs):
        wx.Slider.__init__(self, *args, **kwargs)
        self.SetWindowStyle(wx.SL_SELRANGE)
        self.left_gap = left_gap
        self.right_gap = right_gap
        self.Bind(wx.EVT_LEFT_UP, self.on_left_click)
        self.Bind(wx.EVT_RIGHT_UP, self.on_right_click)
        self.Bind(wx.EVT_SCROLL_PAGEUP, self.on_pageup)
        self.Bind(wx.EVT_SCROLL_PAGEDOWN, self.on_pagedown)
        self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.on_slide)
    
        self.slider_value=self.Value
        self.is_dragging=False
    
    def linapp(self, x1, x2, y1, y2, x):
        proportion=float(x - x1) / (x2 - x1)
        length = y2 - y1
        return round(proportion*length + y1)
    
    # if left click set the start of selection
    def on_left_click(self, e):
    
        if not self.is_dragging: #if this wasn't a dragging operation
            position = self.get_position(e)
            if position <= self.SelEnd:
                self.SetSelection(position, self.SelEnd)
            else:
                self.SetSelection(self.SelEnd, position)
        else:
            self.is_dragging = False
        e.Skip()
    
    # if right click set the end of selection
    def on_right_click(self, e):
        position = self.get_position(e)
        if position >= self.SelStart:
            self.SetSelection(self.SelStart, position)
        else:
            self.SetSelection(position, self.SelStart)
        e.Skip()
        
        
        wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_SLIDER.typeId, self.GetId()))
    
    # drag the selection along when sliding
    def on_slide(self, e):
        self.is_dragging=True
        delta_distance=self.Value-self.slider_value
        self.SetSelection(self.SelStart+delta_distance, self.SelEnd+delta_distance)
        self.slider_value=self.Value
    
    # disable pageup and pagedown using following functions
    def on_pageup(self, e):
        self.SetValue(self.Value+self.PageSize)
    
    def on_pagedown(self, e):
        self.SetValue(self.Value-self.PageSize)
    
    # get click position on the slider scale
    def get_position(self, e):
        click_min = self.left_gap #standard size 9
        click_max = self.GetSize()[0] - self.right_gap #standard size 55
        click_position = e.GetX()
        result_min = self.GetMin()
        result_max = self.GetMax()
        if click_position > click_min and click_position < click_max:
            result = self.linapp(click_min, click_max,
                                 result_min, result_max,
                                 click_position)
        elif click_position <= click_min:
            result = result_min
        else:
            result = result_max
    
        return result

    def GetRange(self):
        return [self.SelStart, self.SelEnd]



class RangeSlider(wx.Panel):
    def __init__ (self, parent, pos, minPos, maxPos, zones = []):
        super(RangeSlider, self).__init__(parent, wx.ID_ANY)

        self.minPos = minPos
        self.maxPos = maxPos
        self.zones = zones
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.sldMax = wx.Slider(self, value=pos[1], minValue=minPos, maxValue=maxPos,
                                size = (-1, 18), 
                                style=wx.SL_HORIZONTAL | wx.SL_TOP )
        self.sldMin = wx.Slider(self, value=pos[0], minValue=minPos, maxValue=maxPos,
                                size = (-1, 18),
                                style =wx.SL_HORIZONTAL )

        self.sldMax.Bind(wx.EVT_SCROLL, self.OnSliderScrollMax)
        self.sldMin.Bind(wx.EVT_SCROLL, self.OnSliderScrollMin)
        
        sizer.Add (self.sldMin, 1, wx.EXPAND)
        sizer.Add (self.sldMax, 1, wx.EXPAND)
        
        self.SetSizer (sizer)
        
        self.ShowRange()
    
    def GetRange(self):
        return [self.sldMin.GetValue(), self.sldMax.GetValue()]


    def SetValue(self, pos):
        if pos[0] <= pos[1]:
            self.sldMin.SetValue(pos[0])
            self.sldMax.SetValue(pos[1])
    
    
    def GetZone(self, slider):
        for z in self.zones:
            if slider.GetValue() >= z[0] and slider.GetValue() <= z[1]:
                return z
        return 


    def SetZone(self, slider):
        if slider == self.sldMin:
            zoneMin = self.GetZone(slider)
            zoneMax = self.GetZone(self.sldMax)

            if zoneMin is not None and zoneMin == zoneMax:
                self.sldMin.SetValue(zoneMin[0])
                self.sldMax.SetValue(zoneMin[1])
            elif zoneMin is not None and zoneMax is None:
                self.sldMin.SetValue(zoneMin[0])
                self.sldMax.SetValue(zoneMin[1])
            elif zoneMin is  None and zoneMax is not None:
                self.sldMax.SetValue(self.sldMin.GetValue())
        
        else:
            zoneMax = self.GetZone(slider)
            zoneMin = self.GetZone(self.sldMin)

            if zoneMax is not None and zoneMin == zoneMax:
                self.sldMin.SetValue(zoneMax[0])
                self.sldMax.SetValue(zoneMax[1])
            elif zoneMax is not None and zoneMin is None:
                self.sldMin.SetValue(zoneMax[0])
                self.sldMax.SetValue(zoneMax[1])
            elif zoneMax is  None and zoneMin is not None:
                self.sldMin.SetValue(self.sldMax.GetValue())
                
    
    def OnSliderScrollMax(self, e):
        val = self.sldMax.GetValue()
        valMin = self.sldMin.GetValue()
        if valMin > val:
            self.sldMin.SetValue(val)
            
        self.SetZone(self.sldMax)
        self.ShowRange()
        
        e.Skip()

    
    def OnSliderScrollMin(self, e):
        val = self.sldMin.GetValue()
        valMax = self.sldMax.GetValue ()
        if valMax < val:
            self.sldMax.SetValue (val)
        
        self.SetZone(self.sldMin)
        self.ShowRange()
        e.Skip()

    
    def ShowRange(self):
        r = self.GetRange()
        self.sldMin.SetSelection(*r)
        self.sldMax.SetSelection(*r)
        self.Update()
        self.Refresh()













import xml.etree.ElementTree as ET
from util_path import SYSTEM_ENCODING
##################################################################################################    
def enregistrer_root(root, nomFichier):
    fichier = file(nomFichier, 'w')
    try:
        ET.ElementTree(root).write(fichier, xml_declaration=False, encoding = SYSTEM_ENCODING)
    except IOError:
        messageErreur(None, u"Accés refusé", 
                              u"L'accés au fichier %s a été refusé !\n\n"\
                              u"Essayer de faire \"Enregistrer sous...\"" %nomFichier)
    except UnicodeDecodeError:
        messageErreur(None, u"Erreur d'encodage", 
                              u"Un caractère spécial empêche l'enregistrement du fichier !\n\n"\
                              u"Essayer de le localiser et de le supprimer.\n"\
                              u"Merci de reporter cette erreur au développeur.")
    fichier.close()
    
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


def getHoraireTxt(v, prefixe = u""): 
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
def scaleImage(image, wf = 24 , hf = 24): 
    return image.ConvertToImage().Scale(wf, hf, quality = wx.IMAGE_QUALITY_HIGH ).ConvertToBitmap()


#############################################################################################################
def scaleIcone(image, wf = 20 , hf = 20): 
    i = wx.EmptyIcon()
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
    t = wordwrap(texte, taille, dc).split(u"\n")[0]
    if len(t) < len(texte):
        ts = t + suffix
    else:
        return texte
#     print "   ", ts
#     print "   >", dc.GetTextExtent(ts)[0]
    
    # Vérification
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

        :param `dc`: a `wx.DC` device context;
        :param `text`: the text to chop;
        :param `max_size`: the maximum size in which the text should fit.
        """

        # first check if the text fits with no problems
        x, y = dc.GetTextExtent(text)

        if x <= max_size:
            return text

        textLen = len(text)
        last_good_length = 0

        for i in xrange(textLen, -1, -1):
            s = text[0:i]
            s += "..."

            x, y = dc.GetTextExtent(s)
            last_good_length = i

            if x < max_size:
                break

        ret = text[0:last_good_length] + "..."    
        return ret
