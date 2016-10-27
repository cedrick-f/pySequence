#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                   error                                 ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014 Cédrick FAURY - Jean-Claude FRICOU

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
error.py

pySéquence : aide à la réalisation de fiches  de séquence pédagogiques
et à la validation de projets

Copyright (C) 2011-2015
@author: Cedrick FAURY

"""

import traceback

import sys

from widgets import messageErreur

import wx

import version

import time


def MyExceptionHook(etype, value, trace):
    """
    Handler for all unhandled exceptions.
 
    :param `etype`: the exception type (`SyntaxError`, `ZeroDivisionError`, etc...);
    :type `etype`: `Exception`
    :param string `value`: the exception error message;
    :param string `trace`: the traceback header, if any (otherwise, it prints the
     standard Python header: ``Traceback (most recent call last)``.
    """
    tmp = traceback.format_exception(etype, value, trace)
    mes = u"pySéquence %s a rencontré une erreur et doit fermer !\n\n"\
         u"Merci de copier le message ci-dessous\n" \
         u"et de l'envoyer à l'équipe de développement :\n"\
         u"cedrick point faury arobase ac-clermont point fr\n\n" %version.__version__
    exception = mes + "".join(tmp)
    
    try:
        wx.GetApp().GetTopWindow()
        messageErreur(None, "Erreur !", exception, wx.ICON_ERROR)
    except:
        print exception
        time.sleep(6)
    sys.exit()

if not "beta" in version.__version__:
    sys.excepthook = MyExceptionHook
    
    
    