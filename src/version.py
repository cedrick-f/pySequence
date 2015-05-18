#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                  version                                ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2015 Cédrick FAURY - Jean-Claude FRICOU

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
Sequence.py
Aide à la réalisation de fiches  de séquence pédagogiques
et à la validation de projets

Copyright (C) 2011-2015
@author: Cedrick FAURY

"""

from bs4 import BeautifulSoup
import urllib2
import webbrowser
from widgets import messageErreur
import wx

__appname__= "pySequence"
__author__ = u"Cédrick FAURY"
__version__ = "6.0-beta.16"
print __version__


###############################################################################################
def GetVersion_cxFreeze():
    return __version__.replace("-beta", ".0")


###############################################################################################
def GetNewVersion(win):  
    # url = 'https://code.google.com/p/pysequence/downloads/list'
    print "Recherche nouvelle version ..."
    url = 'https://github.com/cedrick-f/pySequence/releases'
    try:
        downloadPage = BeautifulSoup(urllib2.urlopen(url, timeout = 5))
    except IOError:
        print "pas d'accès Internet"
        return
    
    # Dernière version
    div_latest = downloadPage.find_all('div', attrs={'class':"release label-latest"})
    try:
        latest = div_latest[0].contents[1].find_all('span', attrs={'class':"css-truncate-target"})[0].contents[0]
    except:
        print "aucune"
        return
    latest = latest.lstrip('v')
    
    # Version actuelle
    a = __version__.split('.')
    
    # Comparaison
    new = True
    for i, l in enumerate(latest.split('.')):
        nl = int(l.rstrip("-beta"))
        na = int(a[i].rstrip("-beta"))
        if nl < na:
            new = False
            break
    if new:
        print latest
    else:
        print

    if new:
        dialog = wx.MessageDialog(win, u"Une nouvelle version de pySéquence est disponible\n\n" \
                                        u"\t%s\n\n" \
                                        u"Voulez-vous visiter la page de téléchargement ?" % latest, 
                                      u"Nouvelle version", wx.YES_NO | wx.ICON_INFORMATION)
        retCode = dialog.ShowModal()
        if retCode == wx.ID_YES:
            try:
                webbrowser.open(url,new=2)
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'ouvrir l'url\n\n%s\n" %url)


    return
