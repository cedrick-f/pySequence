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
import scipy

import time
import  wx.lib.scrolledpanel as scrolled



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
                 expression = None, multiple = False):
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
        
        # Si la variable fait partie d'une expression
        self.expression = expression
        
    def __repr__(self):
        return self.n+" = "+str(self.v)+"("+str(self.t)+")"
    
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

from numpy import abs, ceil, cos, cosh, degrees, \
             exp, fabs, floor, fmod, frexp, hypot, ldexp, log, log10, modf, \
             pi, radians, sin, sinh, sqrt, tan, tanh, errstate 
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
        if not type(v) == float and not type(v) == scipy.float64 and not type(v) == int:
            return False
        elif scipy.isinf(v) or scipy.isnan(v):
            return None
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
    def __init__(self, parent, variable, coef = None, labelMPL = True, signeEgal = True, 
                 slider = False, fct = None, help = ""):
        wx.Panel.__init__(self, parent, -1)
        
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
        txt = self.variable.n
        if signeEgal:
            txt += " ="
        if labelMPL:
            txtnom = wx.StaticBitmap(self, -1, mathtext_to_wxbitmap(txt, taille = FONT_SIZE_VARIABLE))
        else:
            txtnom = wx.StaticText(self, -1, txt)
            
        if len(help) > 0:
            txtnom.SetToolTipString(help)
            
        #
        # Valeur de la variable
        #
        self.text = wx.TextCtrl(self, -1, self.lstToText(self.variable.v))#,
        if self.variable.nn == "":
            txtn = u"de la variable "+self.variable.n
        else:
            txtn = self.variable.nn
        self.text.SetToolTipString(_(u"Saisir la valeur ")+txtn)
        
        self.Bind(wx.EVT_TEXT, self.OnChar, self.text)
#        self.Bind(wx.EVT_CHAR, self.OnChar, self.text)
        
        # Contrôle de la variable
        self.spin = wx.SpinButton(self, -1, size = (15,25), style = wx.SP_VERTICAL | wx.SP_ARROW_KEYS)
        
        self.spin.SetRange(-100, 100)
        self.spin.SetValue(0)
        self.spin.SetToolTipString(_(u"Agir ici pour augmenter/diminuer la valeur ")+txtn)

        self.Bind(wx.EVT_SPIN_UP, self.OnSpinUp, self.spin)
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown, self.spin)
        
        vs = wx.BoxSizer( wx.HORIZONTAL)
        vs.Add( txtnom, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT, 4 )
        vs.Add(self.text, 1, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT, 5 )
        vs.Add(self.spin, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT, 5 )
        
        sizer = wx.BoxSizer( wx.VERTICAL)
        sizer.Add(vs)
        
        if slider:
            self.sli = wx.Slider(self, -1, 0, -100, 100, 
                                 size = (self.text.GetSize()[0] + self.spin.GetSize()[0] + 20, 20),
                                 style = wx.SL_TOP)
            self.sli.SetToolTipString(_(u"Agir ici pour augmenter/diminuer la valeur ")+txtn)

#            self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
            self.Bind(wx.EVT_SCROLL_CHANGED, self.OnScroll, self.sli)
            self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnScroll, self.sli)
            self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnScrollRelease, self.sli)
            sizer.Add(self.sli, flag = wx.ALIGN_RIGHT|wx.BOTTOM, border = 4)
            self.lastPos = 0
        
        self.SetSizerAndFit(sizer)
    
    
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
        
###################################################################################################
##
##  Une bitmap dans un ScrolledPanel qui n'affiche qu'une seule ScrollBar : horizontale
##  avec possibilité de faire glisser l'image à la souris
##
###################################################################################################    
myEVT_BITMAP_CHANGED = wx.NewEventType()
EVT_BITMAP_CHANGED = wx.PyEventBinder(myEVT_BITMAP_CHANGED, 1)
class BmpEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.num = None
        self.obj = None

    def SetNum(self, num):
        self.num = num

    def GetNum(self):
        return self.num
    
    def SetObj(self, obj):
        self.obj = obj

    def GetObj(self):
        return self.obj
    
class ScrolledBitmap(wx.ScrolledWindow):
    def __init__(self, parent, id, lstBmp = [], event = True, synchroAvec = []):
        self.tip = u""
        self.num = 0
        self.event = event
        self.synchroAvec = synchroAvec
        
        wx.ScrolledWindow.__init__(self, parent, id)#, style = wx.BORDER_SIMPLE)
        self.SetScrollRate(1,0)
        
        self.sb = wx.StaticBitmap(self, -1, wx.NullBitmap)
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        psizer.Add(self.sb, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)# | wx.EXPAND)
        self.SetSizer(psizer)
        
        if type(lstBmp) != list:
            lstBmp = [lstBmp]
            
        if lstBmp != []:
            self.SetBitmap(lstBmp[0])
        
        self.lstBmp = lstBmp
        
        self.mouseInfo = None
        
        #wx.CURSOR_HAND))

        self.sb.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.sb.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.sb.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.sb.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.sb.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
#        wx.GetApp().Bind(wx.EVT_MOUSEWHEEL, self.OnWheel)
#        self._processingEvents = False
        
        self.SetToolTipString()
       
    def __repr__(self):
        return str(self.GetId())
    
    #########################################################################################################
    def synchroniserAvec(self, lstScroBmp):
        self.synchroAvec.extend(lstScroBmp)
        for ScroBmp in lstScroBmp:
            ScroBmp.synchroAvec.append(self)
            ScroBmp.nettoyerLstSynchro()
        self.nettoyerLstSynchro()
        
    #########################################################################################################
    def nettoyerLstSynchro(self):
        self.synchroAvec = list(set(self.synchroAvec))
        
    #########################################################################################################
    def sendEvent(self):
        if self.event:
            evt = BmpEvent(myEVT_BITMAP_CHANGED, self.GetId())
            evt.SetNum(self.num)
            evt.SetObj(self)
            self.GetEventHandler().ProcessEvent(evt)
        
    ######################################################################################################    
    def OnWheel(self, event = None):
        return
        """Watch all app mousewheel events, looking for ones from descendants.
        
        If we see a mousewheel event that was unhandled by one of our
        descendants, we'll take it upon ourselves to handle it.
        
        @param  event  The mouse wheel event.
        """
        # By default, we won't eat events...
        wantSkip = True
        
        # Avoid recursion--this function will get called during 'ProcessEvent'.
        if not self._processingEvents:
            print "Mousewheel event received at app level"
            
            self._processingEvents = True
            
            # Check who the event is targetting
            evtObject = event.GetEventObject()
            print "...targetting '%s'" % evtObject
            
            # We only care about passing up events that were aimed at our
            # descendants, not us, so only search if it wasn't aimed at us.
            if evtObject != self:
                toTest = evtObject.GetParent()
                while toTest:
                    if toTest == self:
                        print "...detected that we are ancestor"
                        
                        # We are the "EventObject"'s ancestor, so we'll take
                        # the event and pass it to our event handler.  Note:
                        # we don't change the coordinates or evtObject.
                        # Technically, we should, but our event handler doesn't
                        # seem to mind.
                        self.GetEventHandler().ProcessEvent(event)
                        
                        # We will _not_ skip here.
                        wantSkip = False
                        break
                    toTest = toTest.GetParent()
            self._processingEvents = False
        else:
            print "...recursive mousewheel event"
        
        # Usually, we skip the event and let others handle it, unless it's a
        # mouse event from our descendant...
        if wantSkip:
            event.Skip()
            
#        evtObject = event.GetEventObject()
#        print "OnWheel", event.GetWheelRotation(), evtObject
#        if evtObject == self.sb:
#            print "OnWheel"
        
        
        
    ######################################################################################################    
    def OnRightClick(self, event = None):
#        print "OnRightClick"
        
        def copierImg(event):
            if self.GetBmpHD == None:
                bmp = self.sb.GetBitmap()
            else:
                bmp = self.GetBmpHD()
            CopierBitmap(bmp)
            
        def copierTeX(event):
            if self.GetTeX == None:
                tex = ""
            else:
                tex = self.GetTeX()
            CopierTeX(tex)
            
        menu = wx.Menu()
        itemImg = wx.MenuItem(menu, 0,_(u"Copier comme une image"))
        menu.AppendItem(itemImg)
        self.Bind(wx.EVT_MENU, copierImg, id=0)
        itemTeX = wx.MenuItem(menu, 1,_(u"Copier comme une equation LaTeX"))
        menu.AppendItem(itemTeX)
        self.Bind(wx.EVT_MENU, copierTeX, id=1)
        
        self.PopupMenu(menu)
        menu.Destroy()
        
       
            
        
        
        
    ######################################################################################################    
    def OnSize(self, event = None):
#        print "OnSize ScrolledBitmap"
        w, h = self.sb.GetSize()
        wx.CallAfter(self.SetVirtualSize, (w,h))
        wx.CallAfter(self.SetVirtualSizeHints, w, h)#, w, h)

        if self.GetScrollThumb(wx.HORIZONTAL) > 0:
            self.sb.SetCursor(wx.StockCursor(wx.CURSOR_SIZEWE))
        else:
            self.sb.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            
        self.SetToolTipStringComplet()
        self.Refresh()
        wx.CallAfter(self.Parent.Layout)
        self.Parent.Refresh()
#        self.Layout()
#        self.Refresh()
        
    ######################################################################################################    
    def SetToolTipString(self, s = ""):
        self.tip = s
        self.SetToolTipStringComplet()
        
    ######################################################################################################    
    def SetToolTipStringComplet(self):
        if self.GetScrollThumb(wx.HORIZONTAL) > 0:
            t = _(u"Faire glisser pour visualiser")+u"\n"
        else:
            t = u""
            
        t += _(u"Click droit pour copier dans le presse-papier")
        
        if len(self.lstBmp) > 1:
            t += "\n" + _(u"Click gauche pour choisir une autre fonction")
        
        if self.tip != "":
            t = self.tip + "\n\n("+ t + u")"

        self.sb.SetToolTipString(t)
        
    
    ######################################################################################################    
    def OnMouseDown(self, event):
        x0, y0 = self.GetViewStart()
        x, y = self.CalcScrolledPosition(event.m_x, event.m_y)
        self.mouseInfo = (x,y, x0, y0)
        
    
    ######################################################################################################    
    def OnMouseUp(self, event):
        x0, y0 = self.GetViewStart()
        x, y = self.CalcScrolledPosition(event.m_x, event.m_y)
        mouseInfo = (x,y, x0, y0)
        if self.mouseInfo == None or self.mouseInfo[0] == mouseInfo[0]:
            self.AugmenterNum()
            for sb in self.synchroAvec:
                if sb != self:
                    sb.AugmenterNum(sendEvent = False)
#                    print sb.GetId()
        self.mouseInfo = None
        
    
    ######################################################################################################    
    def OnMouseMove(self, event):
        if self.mouseInfo == None: return
        
        x = self.CalcScrolledPosition(event.m_x, event.m_y)[0]
        dx = -x+self.mouseInfo[0]
#        dy = -y+self.mouseInfo[1]
        xu = self.GetScrollPixelsPerUnit()[0]
        
        x0 = self.mouseInfo[2]
#        y0 = self.mouseInfo[3]
        
        self.Scroll(x0+dx/xu,0)
     
     
    ######################################################################################################    
    def OnLeave(self, event):
        self.mouseInfo = None
    
    ######################################################################################################    
    def AugmenterNum(self, sendEvent = True):
        self.num += 1
        self.num = self.num % len(self.lstBmp)
        self.AffBitmap(self.num, sendEvent = sendEvent)
        
    ######################################################################################################    
    def SetBitmap(self, lstBmp, GetBmpHD = None, GetTeX = None, num = None):
#        print "SetBitmap"
        if type(lstBmp) != list:
            lstBmp = [lstBmp]
            
        #
        # Fonction pour obtenir l'image en HD
        #
        self.GetBmpHD = GetBmpHD
        
        self.GetTeX = GetTeX
        
        #
        # On modifie l'image
        #
        self.lstBmp = lstBmp
        
        if num != None:
            self.num = num
            
        if self.num+1 > len(self.lstBmp):
            self.num = 0

        self.AffBitmap(self.num, sendEvent = False)
        
        
    ######################################################################################################    
    def AffBitmap(self, num, sendEvent = True):
        if self.num+1 > len(self.lstBmp):
            return
        
        self.Freeze()
#        print num, self.lstBmp
        bmp = self.lstBmp[num]
        self.sb.SetBitmap(bmp)
        
        #
        # On règle la taille viruelle
        #
        w, h = bmp.GetWidth(), bmp.GetHeight()
        self.SetVirtualSize((w, h))
        self.SetVirtualSizeHints(w, h, w, h)
        
        #
        # On fixe la hauteur
        #
        self.SetClientSize((self.GetClientSize()[0], h))
        self.SetMinSize((-1, self.GetSize()[1]))
        self.SetMaxSize((-1, self.GetSize()[1]))
        
        self.OnSize()

        self.Thaw()
        
        if sendEvent:
            self.sendEvent()
        
    
##########################################################################################################
# Fonctions min et max améliorées
##########################################################################################################
def _max(lst, defaut):
    if lst == []:
        return defaut
    else:
        return max(lst)
    
def _min(lst, defaut):
    if lst == []:
        return defaut
    else:
        return min(lst) 
    
# Pour calcul des mini, maxi sans tenir compte des None
def _m(a, b, m): 
    if a == None:
        return b
    elif b == None:
        return a
    else:
        return m(a,b)
            
##########################################################################################################
def sign(v):
    if v == 0:
        return v
    elif v > 0 :
        return 1
    else:
        return -1
    
        
##########################################################################################################
def decade(n):
    """ Retourne la decade dans laquelle se trouve <n>
    """
#    print "decade",n,
    with errstate(invalid='ignore'): 
        l = scipy.log10(abs(n))
        if l == 0.0:
            s = 0
        else:
            s = (scipy.sign(l)-1)/2
#        print int(l) + s
        return int(l) + s

##########################################################################################################
##########################################################################################################
# Approximation sur les complexes
##########################################################################################################
##########################################################################################################

##########################################################################################################
def aproxComplexes(lst):
    lst2 = []
    for c in lst:
        if estReel(c):
            lst2.append(c.real)
        elif estImag(c):
            lst2.append(c.imag*1j)
        else:
            lst2.append(c)
    return lst2

##########################################################################################################
def estImag(n, precision = EPSILON):
    with errstate(invalid='ignore'): 
        if abs(n.real) < precision:
            return True
        elif n.imag == 0.0:
            return False
        elif abs(n.real / n.imag) < precision:
            return True
        return False

##########################################################################################################
def estReel(n, precision = EPSILON):
    with errstate(invalid='ignore'): 
        if abs(n.imag) < precision:
            return True
        elif n.real == 0.0:
            return False
        elif abs(n.imag / n.real) < precision:
            return True
        return False

##########################################################################################################
def roundN(v, nc = NB_CHIFFRES):
    """ Arrondi à <nc> chiffres significatifs
    """
    # Passage en NB_CHIFFRES chiffres significatifs
#    print "Pas arrondi :", v
    if v == 0.0: return 0.0, 1
    dec = decade(v)
    mult = 10**dec

    vv = round(float(v)/mult, nc-1)*mult
#    print "    arrondi :", vv
    return vv, dec

#############################################################################################################
def form(x, nc = NB_CHIFFRES):
    """ Renvoie un string formaté du nombre <v> (réel !)
        MERCI à tyrtamos pour ce code !!
    """
    
    f =  '%.' + ('%d' % (nc-1)) + 'e'
    z = float(f % (x.real))
    if z%1 == 0:
        return int(z)
    else:
        return z

#############################################################################################################
def strSc(x, nc = NB_CHIFFRES):
    return str(form(x, nc))


def strScCx(v, nbChiffres = NB_CHIFFRES, lettre = "j"):
    """ Renvoie un string formaté du nombre <v>
        sous forme complexe
    """
    with errstate(invalid='ignore'): 
        if scipy.imag(v) == 0.0:
            return strSc(v, nbChiffres)
        s = strSc(scipy.real(v), nbChiffres)
        i = scipy.imag(v)
        if i > 0.0:
            s += "+"
        
        s += strSc(i, nbChiffres)
        s += lettre
        return s
    
def strList(lst, sep = " "):
    """ Renvoie une chaine à partir de <lst>
    """
    st = ""
    for v in lst:
        st += str(v)+sep
    return st.rstrip(sep)

def listStr(st, sep = " "):
    """ Renvoie une liste de nombres
        à partir de la chaine <str>
    """
    lst = []
    for e in st.split(sep):
        lst.append(eval(e))
    return lst


#############################################################################################################
def chronometrer(fct, *args, **kargs):
    tps1 = time.clock()
    result = fct(*args, **kargs)
    tps2 = time.clock()    
    return tps2 - tps1, result

#############################################################################################################
############################################################
# This is where the "magic" happens.
from matplotlib.mathtext import MathTextParser
#import matplotlib
mathtext_parser = MathTextParser("Bitmap")
def mathtext_to_wxbitmap(s, taille = 100, color =  None):
#    print s
    global mathtext_parser
    if s == "":
        return wx.NullBitmap
    
    if s[0] <> r"$":
        s = mathText(s)
    
    
#    color = matplotlib.rcParams['text.color']
#    print color, 
#    matplotlib.rcParams['text.color'] ='r'
#    print matplotlib.rcParams['text.color']
    ftimage, depth = mathtext_parser.parse(s, taille)
#    ftimage, depth = mathtext_parser.to_rgba(s, 'r')
#    print ftimage
#    matplotlib.rc('text', color=color)
#    color = wx.Colour(255,0,0)

    if color != None:
        x = ftimage.as_array()
        
        # Create an RGBA array for the destination, w x h x 4
        rgba = scipy.zeros((x.shape[0], x.shape[1], 4), dtype=scipy.uint8)
        rgba[:,:,0:3] = color

        # set the RGB components to the constant value passed in
#        rgba[:,:,0] = x
#        rgba[:,:,1] = 0
#        rgba[:,:,2] = 0
#        rgba[:,:,0:3] = x * scipy.array(255,0,0)
        rgba[:,:,3] = x
        # set the A component to the shape of the text
#        rgba[:,:,3] = x
       
        bmp = wx.BitmapFromBufferRGBA(
            ftimage.get_width(), ftimage.get_height(),
            rgba.tostring())
#        bmpmask = bmp.ConvertToImage().ConvertToGreyscale().ConvertToBitmap()
#        mask = wx.Mask(bmpmask)
#        bmp.SetMask(mask)
#        bmp = bmp.ConvertToImage().AdjustChannels(1.0, 0.0, 0.0, 1.0).ConvertToBitmap()
        
    else:
        bmp = wx.BitmapFromBufferRGBA(
            ftimage.get_width(), ftimage.get_height(),
            ftimage.as_rgba_str())
    
#    print bmp.GetDepth()
#    bmp2 = wx.EmptyBitmap(bmp.GetWidth(), bmp.GetHeight())
#    mdc2 = wx.MemoryDC()
#    mdc2.SelectObject(bmp2)
#    mdc2.SetBackgroundMode(wx.SOLID)
#    mdc2.SetBackground(wx.BLACK_BRUSH)
#    mdc2.Clear()
#    
##    bmp3 = wx.EmptyBitmap(bmp.GetWidth(), bmp.GetHeight())
##    mask = wx.Mask(bmp3)
##    bmp.SetMask(mask)
#    
#    mdc = wx.MemoryDC()
#    mdc.SelectObject(bmp)
##    mdc.SetBackground(wx.WHITE_BRUSH)
##    mdc.Clear()
##    mdc.DrawBitmap(bmp, 0,0)
#    
##    print bmp.GetMask()
#    mdc2.Blit(0,0, bmp.GetWidth(), bmp.GetHeight(), mdc, 0,0, wx.SRC_INVERT)
#    
#    mdc.SelectObject(wx.NullBitmap)
#    mdc2.SelectObject(wx.NullBitmap)
#    bmp = bmp.ConvertToImage().AdjustChannels(1.0, 0.1, 0.1, 1.0).ConvertToBitmap()
#    img = bmp.ConvertToImage()
#    img = not img
#    img = img.AdjustChannels(1.0, 0.1, 0.1, 1.0)
#    bmp = img.ConvertToBitmap()
    return bmp
    

def tester_mathtext_to_wxbitmap(s):
    if len(s) == 0:
        return False
    if s[0] <> r"$":
        s = mathText(s)
    try:    
        ftimage, depth = mathtext_parser.parse(s)
        return True
    except:
        print "Erreur MathText", s
        return False


def mathText(s):
    return r'$'+s+'$'
#    f = '\mathsf{'
#    f = '{'
#    return r'$'+f+s+'}$'


def getMathTextPoly(p, varComplexe = "p"):
    """ Renvoie la forme 'MathText' du polynôme <p>
    """
    if type(p) == list:
        return getMathTextList(p, varComplexe)
    elif type(p) == scipy.poly1d:
        return getMathTextArray(p, varComplexe)
    
    
def getMathTextArray(p, varComplexe = "p"):
    s = ''
    o = len(p.c)-1
    for i, c in enumerate(p.c):
        if i != 0:
            if c > 0:
                s += '+'
        
        if c <> 0.0:
            if c <> 1.0  or o == i or o == 0:
                s += strSc(c)
            
            if o-i != 0:
                s += varComplexe
        
                if o-i > 1:
                    s += r'^'+str(o-i)
    return s


def getMathTextList(p, varComplexe = "p"):
#    print "getMathTextList", p
    s = ''
    o = len(p)-1
    for i, c in enumerate(p):
        if i != 0:
            if c > 0:
                s += '+'
        
        if c <> 0.0:
            if c <> 1.0  or o == i or o == 0:
                if type(c) == str or type(c) == unicode:
                    if c in GREEK:
                        c = r""+"\\"+c
                    s += c+' '
                    
                elif isinstance(c, Expression):
                    if i == len(p)-1:
                        s += c.math
                    else:
                        s += c.parentheses()

                else:
                    s += strSc(c)
            
            if o-i != 0:
                s += varComplexe
        
                if o-i > 1:
                    s += r'^'+str(o-i)
    return s
      
def CopierTeX(TeX):
    obj = wx.TextDataObject(TeX)
    wx.TheClipboard.Open()
    wx.TheClipboard.SetData(obj)
    wx.TheClipboard.Close()    
      
def CopierBitmap(bmp):
    bmp2 = wx.EmptyBitmap(bmp.GetWidth(), bmp.GetHeight())
    mdc = wx.MemoryDC()
    mdc.SelectObject(bmp2)
    mdc.SetBackgroundMode(wx.SOLID)
    mdc.SetBackground(wx.WHITE_BRUSH)
    mdc.Clear()
    mdc.DrawBitmap(bmp, 0,0)
    mdc.SelectObject(wx.NullBitmap)
        
    obj = wx.BitmapDataObject()
    obj.SetBitmap(bmp2)
    wx.TheClipboard.Open()
    wx.TheClipboard.SetData(obj)
    wx.TheClipboard.Close()    
        
#############################################################################################################
#
#
#
#############################################################################################################
myEVT_CHOICEBTN_CTRL = wx.NewEventType()
EVT_CHOICEBTN_CTRL = wx.PyEventBinder(myEVT_CHOICEBTN_CTRL, 1)        
class ChoiceBtnEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.choice = None

    def SetChoice(self, choice):
        self.choice = choice

    def GetChoice(self):
        return self.choice
    
class ChoiceButton(wx.Control):
    """ Classe définissant un bouton associé à un menu de choix d'actions
        <choice> : liste des titres du menu
    """
    from wx.lib.embeddedimage import PyEmbeddedImage
    #----------------------------------------------------------------------
    SmallDnArrow = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEhJ"
    "REFUOI1jZGRiZqAEMFGke9QABgYGBgYWdIH///7+J6SJkYmZEacLkCUJacZqAD5DsInTLhDR"
    "bcPlKrwugGnCFy6Mo3mBAQChDgRlP4RC7wAAAABJRU5ErkJggg==")
    
    def __init__(self, parent, id, bmp, choice):
        wx.Control.__init__(self, parent, id)
        
        panel = wx.Panel(self, -1)
        self.button = wx.BitmapButton(panel, -1, bmp)
        self.choicBtn = wx.BitmapButton(panel, -1, self.SmallDnArrow.GetBitmap())
        
        self.choice = choice
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.button)
        self.sizer.Add(self.choicBtn)
        panel.SetSizerAndFit(self.sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.choicBtn)
        
        
    #########################################################################################################
    def sendEvent(self, choice = 0):
        evt = ChoiceBtnEvent(myEVT_CHOICEBTN_CTRL, self.GetId())
        evt.SetChoice(choice)
        self.GetEventHandler().ProcessEvent(evt)
        
        
    #########################################################################################################
    def CreateMenu(self, event):
        # make a menu
        self.menu = wx.Menu()
        # Show how to put an icon in the menu
        for i in self.choice.keys():
            id = wx.NewId()
            self.menu.Append(id, i)
            self.Bind(wx.EVT_MENU, self.OnMenuClick, id = id)
          
          
    #########################################################################################################
    def OnMenu(self, event):  
        pos = (self.button.GetPosition()[0],
               self.button.GetPosition()[1] + self.button.GetSize()[1])
        self.PopupMenu(self.menu, pos)
        self.menu.Destroy()
        
        
    #########################################################################################################
    def OnClick(self, event):
        if event.GetId() == 1:
            self.sendEvent()
        else:
            self.OnMenu(event)
            
    
    #########################################################################################################
    def OnMenuClick(self, event):
        self.sendEvent(event.GetId())
        

def setAlpha(bmp, alpha = 0.3):
    return bmp.ConvertToImage().AdjustChannels(1.0, 1.0, 1.0, alpha).ConvertToBitmap()

def setToggled(bmp, back):
    bmpc = bmp.ConvertToImage().Copy().ConvertToBitmap()
    bmp2 = wx.EmptyBitmap(bmp.GetWidth(), bmp.GetHeight())
    
    memdc = wx.MemoryDC(bmp2)
    memdc.SetBackground(wx.Brush(wx.Color(200,200,255)))
    memdc.Clear()
    

    
#    memdc2 = wx.MemoryDC(bmp2)
#    memdc.Blit(1, 1, bmp.GetWidth()-1, bmp.GetHeight()-1, memdc2, 1, 1)

#    
    
    memdc.DrawBitmap(bmp, 0,0, 1)
#    memdc.SetPen(wx.BLACK_PEN)
#    
#
#
#    memdc.SetBrush(wx.TRANSPARENT_BRUSH)
#    memdc.DrawRectangle(0,0, bmp.GetWidth(), bmp.GetHeight())
    memdc.SelectObject(wx.NullBitmap)
#    memdc2.SelectObject(wx.NullBitmap)
    
    return bmp2
    
import os
try:
    import globdef
except:
    def identity(txt):
        return txt
    _ = identity

def changeEchelle(img, echelle):
    return img.Scale(echelle[0], echelle[1], wx.IMAGE_QUALITY_HIGH)

def changeEchelleBmp(bmp, echelle):
    return changeEchelle(wx.Image(bmp), echelle).ConvertToBitmap()

#def getBitmap(fich, echelle = None):
#    if echelle == None:
#        return wx.Image(os.path.join(globdef.DOSSIER_IMAGES, fich), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
#    else:
#        return wx.Image(os.path.join(globdef.DOSSIER_IMAGES, fich), 
#                        wx.BITMAP_TYPE_PNG).Scale(echelle[0], echelle[1], wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()

#def addTextToBitmap(bmp, texte, pos):
#    bmp = wx.EmptyBitmap(self.zoneMtg.maxWidth, self.zoneMtg.maxHeight)
#    memdc = wx.MemoryDC(bmp)
#    memdc.SetBackground(wx.Brush(wx.Colour(255,255,254))) #wx.TRANSPARENT_BRUSH)
#    memdc.Clear()
#    memdc.DrawBitmap(self.GetBmp(), self.pos[0], self.pos[1])
#    return bmp


##########################################################################################################
class PopPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.SetAutoLayout(True)
        
#        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
#        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
#        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
#        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
#        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
#        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        
#    def OnEnter(self, event):
#        self.SetCursor(wx.StockCursor(globdef.CURSEUR_MAIN))
#        
#    def OnLeave(self, event):
#        self.SetCursor(wx.StockCursor(globdef.CURSEUR_DEFAUT))
        
        
    def DetBind(self):    
        for w in self.GetChildren():
            w.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
            w.Bind(wx.EVT_MOTION, self.OnMouseMotion)
            w.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
            w.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
            w.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
            w.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        
    def OnMouseLeftDown(self, evt):
        self.Refresh()
        self.ldPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        self.wPos = self.GetPosition()#self.pop.ClientToScreen((0,0))
        self.CaptureMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            dPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
            nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
                    self.wPos.y + (dPos.y - self.ldPos.y))
            self.Move(nPos)

    def OnMouseLeftUp(self, evt):
        self.ReleaseMouse()

    def OnRightUp(self, evt):
        self.Show(False)
#        self.pop.Destroy()

    def RendreVisible(self):
        self.Raise()
        self.Show(True)
        self.Move((0,0))
        self.Refresh()
        self.CaptureMouse()
        self.ReleaseMouse()



#############################################################################################################
#############################################################################################################
try:
    from agw import aui
except ImportError:
    import wx.lib.agw.aui as aui
    

class PrintoutWx(wx.Printout):
    """Simple wrapper around wx Printout class -- all the real work
    here is scaling the matplotlib canvas bitmap to the current
    printer's definition.
    """
    def __init__(self, zone, app, 
                 bottommargin = 0,
                 rightmargin = 0,
                 topmargin = 0,
                 leftmargin = 0, 
                 titre = ""):
        wx.Printout.__init__(self, titre)
        
        if isinstance(zone, aui.AuiNotebook):
            auiManager = zone.GetAuiManager()
            
            lstCanvas = []
            lstPages = []
            for i in range(zone.GetPageCount()):
                page = zone.GetPage(i)
                if page.IsShown():
                    lstPages.append(page)
                    lstCanvas.append(page.child[0])
#                print auiManager.GetPanePart(page)
#        elif isinstance(zone, graph.ZoneGraphBase):
        else:
            lstCanvas = [zone]
            lstPages = lstCanvas
                
        self.lstCanvas = lstCanvas
        self.lstPages = lstPages
#        print len(lstCanvas)
        self.app = app
        
        # Marges et dimension d'impression (en mm)
        self.bottommargin  = bottommargin
        self.rightmargin  = rightmargin
        self.topmargin = topmargin
        self.leftmargin = leftmargin
        

    def HasPage(self, page):
        #current only supports 1 page print
        return page == 1

    def GetPageInfo(self):
        return (1, 1, 1, 1)

    def OnPrintPage(self, page):
        print "PrintPage", self.lstCanvas

        # On récupère le DC
        dc = self.GetDC()
        
        # La zone graphique de référence
        zoneGraph = self.lstCanvas[0]
        
        # On sauvegarde la couleur de fond et le dpi du canvas    
        bgcolor   = zoneGraph.canvas.figure.get_facecolor()
        fig_dpi   = zoneGraph.canvas.figure.dpi
#        print "fig_dpi", fig_dpi
        # Dimensions des 2 zones en pixels
#        (grw,grh) = self.zoneGraph.canvas.GetSizeTuple()
        (pgw,pgh) = self.GetPageSizePixels()
        
#        print "   PageSizePixels", pgw, pgh
        
        # On réduit un peu la définition pour accélérer ...
#        print "   GetPPIPrinter", self.GetPPIPrinter(),
#        PPIPrinter = (min(300, self.GetPPIPrinter()[0]), min(300, self.GetPPIPrinter()[1]))
        coefPPI = min(1, float(globdef.MAX_PRINTER_DPI)/self.GetPPIPrinter()[0], float(globdef.MAX_PRINTER_DPI)/self.GetPPIPrinter()[1])
        
#        print " (x",coefPPI,")"
        
        (dcw,dch) = dc.GetSize()
#        print "   DCSizePixels", dcw, dch
        
        # On traduit les marges : mm --> pixels
        (psw, psh) = self.GetPageSizeMM()
#        print "   PageSizeMM", psw, psh
        _pgw, _pgh = int(pgw * coefPPI), int(pgh * coefPPI)
#        print "   _PageSizePixels", _pgw, _pgh
        page_scale_w = float(_pgw) / psw
        page_scale_h = float(_pgh) / psh
        top_margin  = int(self.topmargin * page_scale_h)
        left_margin = int(self.leftmargin * page_scale_w)
        bottom_margin  = int(self.bottommargin * page_scale_h)
        right_margin = int(self.rightmargin * page_scale_w)
        width = _pgw - left_margin - right_margin
        height = _pgh - top_margin - bottom_margin
        
#        print "page_scale_h", page_scale_h
#        print "width, height :", width, height
        
        # On règle la taille de la police : 
        #  indispensable pour que SetUserScale ait de l'effet sur les textes !!!
        dc.SetFont(wx.Font(2*page_scale_w, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        # On détermine s'il y a un en-tête ou un pied de page ...
        enTete = pdePage = [0, 0]
        
        if globdef.TEXTE_TITRE == None:
            titre = self.app.fichierCourant
        else:
            titre = globdef.TEXTE_TITRE
            
        if globdef.TEXTE_NOM == None:
            nom = globdef.NOM
        else:
            nom = globdef.TEXTE_NOM
            
        for txt, pos in [(titre, globdef.POSITION_TITRE),
                         (nom,   globdef.POSITION_NOM)]:
            if len(txt)>0:
                wt, ht = dc.GetTextExtent(txt)
                if pos[0] == "T":
                    enTete.append(ht)
                elif pos[0] == "B":
                    pdePage.append(ht)
        enTete = max(enTete)
        pdePage = max(pdePage)

        n = len(self.lstCanvas)
        # Détermination des bornes de la zone en pixels
        X0, Y0 = "", ""
        X1, Y1 = None, None
        etatAff = []
        for zg in self.lstCanvas:
            zg.Freeze()
            etatAff.append(zg.SetAffComplet(False))
            
        for zg in self.lstPages:
            px, py = zg.GetScreenPosition()
            sx, sy = zg.GetSize()
            
            X0 = min(X0, px)
            Y0 = min(Y0, py)
            X1 = max(X1, px+sx)
            Y1 = max(Y1, py+sy)
        
        # Conversion des positions et tailles en (0-1)
        
        posX, posY = [0.0]*n, [0.0]*n
        sizX, sizY = [0.0]*n, [0.0]*n
        for i, zg in enumerate(self.lstPages):
            px, py = zg.GetScreenPosition()
            sx, sy = zg.GetSize()
            
            posX[i] = float(px-X0)/(X1-X0)
            posY[i] = float(py-Y0)/(Y1-Y0)
            sizX[i] = float(sx) / (X1-X0)
            sizY[i] = float(sy) / (Y1-Y0)
        
        # On calcul le nouveau dpi pour que la bitmap soit de dimension (w,h)
        iw, ih = zoneGraph.canvas.figure.get_size_inches()
        (giw,gih) = iw / sizX[0], ih / sizY[0]
        
        w, h = width, height - enTete - pdePage
        new_dpi = min(int(w/giw), int(h/gih))
        for zg in self.lstCanvas:
            # On affecte le nouveau dpi
            zg.canvas.figure.dpi = new_dpi
            
            # On passe le fond en blanc
            zg.canvas.figure.set_facecolor('#FFFFFF')
            
            # On redessine le canvas...
            self.drawCanvas(zg)
        
        
        # On calcul les dimensions de l'image bitmap des tracés
        w, h = zoneGraph.canvas.bitmap.GetWidth(), zoneGraph.canvas.bitmap.GetHeight()
        w, h = w / sizX[0], h / sizY[0]
        
        # On calcul les dimensions de l'image bitmap ENTIERE
        we, he = w, h + dc.GetTextExtent(self.app.fichierCourant)[1] + dc.GetTextExtent(globdef.NOM)[1]
#        print "we, he :", we, he
        
#        # On calcul les dimensions UTILES de la page, en pixels
#        r = we/he
#        if dcw/r <= dch:
#            dcwu, dchu = dcw, dcw/r
#        else:
#            dcwu, dchu = dch * r, dch
#            
#        print "dcwu, dchu =", dcwu, dchu 
        
        # Echelle pour la prévisualisation
        user_scalew = float(dcw) / we
        user_scaleh = float(dch) / he
        if globdef.PRINT_PROPORTION:
            user_scalew = user_scaleh = min(user_scalew, user_scaleh)
        
#        print user_scalew, user_scaleh
        dc.SetUserScale(user_scalew, user_scaleh)
    
        # On défini l'origine de tracé du DC
        dc.SetDeviceOrigin(left_margin*user_scalew, top_margin*user_scaleh)
                        
        # Ajout des "titres"
        def ajouter(texte, pos):
            if len(texte)>0:
                wt, ht = dc.GetTextExtent(texte)
                if pos[1] == "C":
                    xt = (w-wt)/2
                elif pos[1] == "R":
                    xt = w-wt
                else:
                    xt = 0
    
                if pos[0] == "B":
                    yt = enTete + h
                else:
                    yt = 0
#                print "Ajout", texte, xt, yt
                dc.DrawText(texte, xt, yt)
        
        ajouter(titre, globdef.POSITION_TITRE)
        ajouter(nom,   globdef.POSITION_NOM)
            
        # On met l'image dans dans le DC
        for i, zg in enumerate(self.lstCanvas):
            bmp = zg.canvas.bitmap
            dc.DrawBitmap(bmp, posX[i]*w, enTete+posY[i]*h)
                
        for i, zg in enumerate(self.lstCanvas):
            wx.CallAfter(zg.SetAffComplet,etatAff[i])
            
        for zg in self.lstCanvas:
            # On restaure le canvas
            zg.canvas.figure.set_facecolor(bgcolor)
            zg.canvas.figure.dpi = fig_dpi
            self.drawCanvas(zg)
            
            zg.Thaw()
            

        return True
    

    def getBitmap(self):
        return
    
    def drawCanvas(self, zoneGraph):
        try:
            zoneGraph.drawCanvas()
        except:
            t = u"Informations sur l'impression :\n"
            t += u"  PageSizePixel : "+str(self.GetPageSizePixels()[0])+"  "+str(self.GetPageSizePixels()[1])+"\n"
            t += u"  CanvasDPI : "+str(zoneGraph.canvas.figure.dpi)+"\n"
            t += u"  CanvasSize : "+str(zoneGraph.canvas.bitmap.GetWidth())+"  "+str(zoneGraph.canvas.bitmap.GetHeight())
            dlg = wx.MessageDialog(self.app, t, _(u"Erreur d'impression"),
                                   wx.OK | wx.ICON_ERROR
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()



class PrintHandler():
    def initPrintHandler(self, printout, app, PRINT_PAPIER_DEFAUT, PRINT_MODE_DEFAUT):
        ###############################################
        ###############################################
        # Tout ce qu'il faut pour imprimer ...
        ###############################################
        ###############################################
        self.printData = wx.PrintData()
        self.printData.SetPaperId(PRINT_PAPIER_DEFAUT)
        self.printData.SetPrintMode(PRINT_MODE_DEFAUT)
        self.data = wx.PageSetupDialogData(self.printData)
        self.printData = self.data.GetPrintData()
        self.ComputeWidthMargin()
        self.Printout = printout
        self.app = app
        
        
    def OnPageSetup(self):
        if not hasattr(self, 'data'):
            self.init()

        psdd = wx.PageSetupDialogData(self.data)
        psdd.CalculatePaperSizeFromId()
        dlg = wx.PageSetupDialog(self, psdd)
        dlg.ShowModal()

        # this makes a copy of the wx.PrintData instead of just saving
        # a reference to the one inside the PrintDialogData that will
        # be destroyed when the dialog is destroyed
        self.data = wx.PageSetupDialogData(dlg.GetPageSetupData())
        
#        self.printData = self.data.GetPrintData()
        self.printData = wx.PrintData( self.data.GetPrintData() )
    
        self.ComputeWidthMargin()
       
        dlg.Destroy()


    def OnPrintPreview(self, lstCanvas = None, titre = ""):
#        print "PrintPreview",
        if lstCanvas == None:
            lstCanvas = self.getZonesGraphVisiblesNoteBook()
#        print "1", 
        data = wx.PrintDialogData(self.printData)
#        print "2", 
        self.ComputeWidthMargin()
#        print "3", 
        printout = self.Printout(lstCanvas, self.app, 
                                 self.bottommargin,
                                 self.rightmargin,
                                 self.topmargin,
                                 self.leftmargin, 
                                 titre)
        printout2 = self.Printout(lstCanvas, self.app,
                                  self.bottommargin,
                                  self.rightmargin,
                                  self.topmargin,
                                  self.leftmargin, 
                                  titre)
        
#        print "4",
        self.preview = wx.PrintPreview(printout, printout2, data)
#        print "5",
        if not self.preview.Ok():
            return
        
        pfrm = MyPreviewFrame(self.preview, self, title = _(u"Aperçu avant impression"))
#        print "6",
        pfrm.Initialize()
#        print "7",
        pfrm.PersonaliserControlBar()
#        pfrm.SetPosition(self.GetPosition())
#        pfrm.SetSize(self.frame.GetSize())
        pfrm.Show(True)
#        print "Fin PrintPreview"


    def OnDoPrint(self, mplcanvas = None, titre = ""):
        if mplcanvas == None:
            mplcanvas = self.getZoneGraph()
            
        pdd = wx.PrintDialogData(self.printData)
#        print self.printData.GetPaperId()

#        pdd.SetToPage(2)
        printer = wx.Printer(pdd)
        printout = self.Printout(mplcanvas, self.app, 
                                 self.bottommargin,
                                 self.rightmargin,
                                 self.topmargin,
                                 self.leftmargin,
                                 titre)

        ok = printer.Print(self, printout, True)
        if not ok:
            err = printer.GetLastError()
            if err > 1: # Annulé par l'utilisateur
#            self.printData = printer.GetPrintDialogData().GetPrintData()
#            self.printData = wx.PrintData( printer.GetPrintDialogData().GetPrintData() )
                wx.MessageBox(_(u"Il y a eu un problème d'impression.\n"
                                u"Votre imprimante n'est probablement pas réglée correctement.\n") \
                                + str(err),
                                _(u"Problème d'impression"), wx.OK)
#        else:
#            
        printout.Destroy()
        
    ########################################################################################################
    def ComputeWidthMargin(self):
        """ Calcul les dimensions et les marges d'impression
            ... en mm ...
        """
#        if self.printData.GetOrientation() == wx.LANDSCAPE:
#            ps = [self.data.GetPaperSize()[1], self.data.GetPaperSize()[0]]
#        else:
#            ps = self.data.GetPaperSize()
#        print "Papier :", ps
#        print "Marges :", self.data.GetMarginTopLeft(), self.data.GetMarginBottomRight()
#        width = ps[0]-self.data.GetMarginTopLeft()[0]-self.data.GetMarginBottomRight()[0]
#        height = ps[1]-self.data.GetMarginTopLeft()[1]-self.data.GetMarginBottomRight()[1]
        topmargin = self.data.GetMarginTopLeft()[1]
        leftmargin = self.data.GetMarginTopLeft()[0]
        bottommargin = self.data.GetMarginBottomRight()[1]
        rightmargin = self.data.GetMarginBottomRight()[0]
        
#        # Il faut imposer des marges supplémentaires ...
#        width = width - 10
#        height = height - 10
        
#        self.width = width
#        self.height = height
        self.topmargin = topmargin
        self.leftmargin = leftmargin
        self.bottommargin = bottommargin
        self.rightmargin = rightmargin

        # Passage en pouces
#        self.width = width/25.4
#        self.height = height/25.4
#        self.topmargin = topmargin/25.4
#        self.leftmargin = leftmargin/25.4
        
        
#############################################################################################################
class MyPreviewFrame(wx.PreviewFrame):
    def __init__(self, *args, **kwargs):
        wx.PreviewFrame.__init__(self, *args, **kwargs)
        self.SetClientSize((647, 400))
        
    def PersonaliserControlBar(self):
        buttons = self.GetControlBar().GetChildren()
        buttons[0].SetLabel(_(u"Fermer"))
        buttons[1].SetLabel(_(u"Imprimer"))
        buttons[6].Destroy()
        buttons[5].Destroy()
        buttons[4].Destroy()
        buttons[3].Destroy()
        buttons[2].Destroy()
#        print buttons
#        for b in buttons:
#            print b.GetLabel()
        
#    def OnToolClick(self, event):
##        print "Click Setup"
#        self.PageSetup()
#        self.initPreview()
    
    
#    ########################################################################################################
#    def initPreview(self):
#        po1  = PrintoutWx(self.mplcanvas, self.Parent, self.Parent, self.width, self.margin)
#        self.preview.SetPrintout(po1)
#        self.preview.SetZoom(self.preview.GetZoom())
#        self.Layout()
#        self.Refresh()

    
        
    ########################################################################################################
    def OnToolClick(self, event):
        id = event.GetId()
        if id == 10:
            self.preview.Print(True)
        elif id == 11:
            self.PageSetup()
            self.initPreview()
            
            
    ########################################################################################################
    def OnCombo(self, event):
        ech = eval(event.GetString())
        self.preview.SetZoom(ech)
        
        
#    ########################################################################################################
#    def PageSetup(self):
##        psdd = wx.PageSetupDialogData(self.printData)
##        psdd.CalculatePaperSizeFromId()
#        dlg = wx.PageSetupDialog(self, self.data)
#        dlg.ShowModal()
#
#        # this makes a copy of the wx.PrintData instead of just saving
#        # a reference to the one inside the PrintDialogData that will
#        # be destroyed when the dialog is destroyed
#        data = dlg.GetPageSetupData()
#        self.printData = wx.PrintData( data.GetPrintData() )
#        self.ComputeWidthMargin()
#        
#        dlg.Destroy()
        
        
#    ########################################################################################################
#    def ComputeWidthMargin(self):
#        print "Papier :", self.data.GetPaperSize()
#        print "Marges :", self.data.GetMarginTopLeft()
#        width = self.data.GetPaperSize()[0]-self.data.GetMarginTopLeft()[1]-self.data.GetMarginBottomRight()[1]
#        w
#        margin = self.data.GetMarginTopLeft()[1]
#        self.width = width/25.4
#        self.margin = margin/25.4
#        print "width, margin", self.width, self.margin
        
        
    ########################################################################################################
    def OnCloseWindow(self, event):
        self.MakeModal(False)
        event.Skip()
    
##################################################################################################
#
#  Un ScrolledPanel qui n'affiche qu'une seule ScrollBar : verticale
#
##################################################################################################    
class VerticalScrolledPanel(wx.ScrolledWindow):
    """ Un ScrolledPanel qui n'affiche qu'une seule ScrollBar (verticale)
        
    """
    def __init__(self, *args, **kwargs):
        wx.ScrolledWindow.__init__(self, *args, **kwargs)
        self.SetScrollRate(10,10)
        self.EnableScrolling(True, True)
#        self.SetupScrolling()#scroll_x = False)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
#        print dir(self)
        
    
    def OnEnter(self, event):
        self.SetFocus()
        
    def OnSize(self, event = None):
        self.SetVirtualSizeHints(self.GetClientSize()[0],-1, self.GetClientSize()[0],-1)
        event.Skip()
#        self.SetVirtualSize((self.GetClientSize()[0], -1))
#        _x, _y = self.GetScrollPixelsPerUnit()
#        self.Scroll(self.GetClientSize()[0]/_x, -1)
#        event.Skip()









##########################################################################################################
#def getVariables(expr):
#    """ Analyse d'une chaine <expr> (prétendue expression mathématique)
#        et renvoie :
#         - un dictionnaire 
#    """
#    new_expr = expr
#    
#    # Adaptation à la syntaxe "mathtext"
#    new_expr = expr.replace('^', '**')
#    
#    # Découpage le la chaine autour des opérateurs
#    for i in math_list:
#        expr = expr.replace(i,'#')
#    expr = expr.split('#')
#    
#    # Création du dictionnaire de variables
#    b={}
#    for i in expr:
#        try:
#            int(i)      # C'est une constante
#        except:         # C'est une variable
#            if i.strip()!='':
#                b[i] = 1. # On lui affecte la valeur 1.0
#                
#    return b, new_expr

#def getVariables(expr):
#    from math import *
#    #use the list to filter the local namespace 
#    safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])
#    
#    v = {}
#    continuer = True
#    error = False
#    while continuer:
#        try:
#            eval(expr, {"__builtins__": None}, safe_dict)
#            continuer = False
#        except NameError as err:
#            vari = err.args[0].split("'")[1]
#            v[vari] = safe_dict[vari] = 1.0
#        except:
#            error = True
#            continuer = False
#            
#    return v, error
        
try:
    from agw import supertooltip as STT
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.supertooltip as STT
    
def SetSuperToolTip(Cible, Texte, headerText = None, headerBmp = None, bodyImage = None, \
                    footerText = None, footerBmp = None):
          
    tip = STT.SuperToolTip(Texte)
    
    if bodyImage != None:
        tip.SetBodyImage(bodyImage)
    
    if headerText != None:
        tip.SetHeader(headerText)
        tip.SetDrawHeaderLine(True)
        
    if headerBmp != None:
        tip.SetHeaderBitmap(headerBmp)
    
    if footerText != None:
        tip.SetFooter(footerText)
        tip.SetDrawFooterLine(True)
    
    if footerBmp != None:
        tip.SetFooterBitmap(footerBmp)
                
#    print STT.GetStyleKeys()
    tip.ApplyStyle('Office 2007 Blue')
    
    tip.SetTarget(Cible)

#    tip.SetDropShadow(self.dropShadow.GetValue())
#    tip.SetUseFade(self.useFade.GetValue())
#    tip.SetEndDelay(self.endTimer.GetValue())
    
    