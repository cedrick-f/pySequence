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
version
*******

Gestion des numéros de version


"""

import urllib.request#, urllib.error, urllib.parse
import json
import webbrowser
import wx



__appname__= "pySéquence 8"
__author__ = "Cédrick FAURY"
__version__ = "8.3.3"
__urlapi__ = "https://api.github.com/repos/cedrick-f/pySequence"
__url__ = "https://github.com/cedrick-f/pySequence"
__mail__ = "cedrick.faury#ac-clermont.fr"
print(__version__)


###############################################################################################
def GetVersion_cxFreeze():
    return __version__.replace("-beta", "")

###############################################################################################
def GetVersion_short():
    return __version__.split('.')[0]

###############################################################################################
def GetAppnameVersion():
    return __appname__#+" "+GetVersion_short()

################################################################################################
#def GetNewVersion_old(win):  
#    # url = 'https://code.google.com/p/pysequence/downloads/list'
#    print "Recherche nouvelle version ..."
#    url = 'https://github.com/cedrick-f/pySequence/releases'
#    try:
#        downloadPage = BeautifulSoup(urllib2.urlopen(url, timeout = 5))
#    except IOError:
#        print "pas d'accès Internet"
#        return
#    
#    # Dernière version
#    div_latest = downloadPage.find_all('div', attrs={'class':"release label-latest"})
#    try:
#        latest = div_latest[0].contents[1].find_all('span', attrs={'class':"css-truncate-target"})[0].contents[0]
#    except:
#        print "aucune"
#        return
#    latest = latest.lstrip('v')
#    
#    # Version actuelle
#    a = __version__.split('.')
#    
#    # Comparaison
#    new = True
#    for i, l in enumerate(latest.split('.')):
#        nl = int(l.rstrip("-beta"))
#        na = int(a[i].rstrip("-beta"))
#        if nl < na:
#            new = False
#            break
#    if new:
#        print latest
#    else:
#        print
#
#    if new:
#        dialog = wx.MessageDialog(win, u"Une nouvelle version de pySéquence est disponible\n\n" \
#                                        u"\t%s\n\n" \
#                                        u"Voulez-vous visiter la page de téléchargement ?" % latest, 
#                                      u"Nouvelle version", wx.YES_NO | wx.ICON_INFORMATION)
#        retCode = dialog.ShowModal()
#        if retCode == wx.ID_YES:
#            try:
#                webbrowser.open(url,new=2)
#            except:
#                messageErreur(None, u"Ouverture impossible",
#                              u"Impossible d'ouvrir l'url\n\n%s\n" %url)
#
#
#    return


#########################################################################################
def sup(v1, v2):
    u""" Comparaison de deux versions
    """
#     print "sup", v1, v2
    for i, l in enumerate(v1.split('.')):
#         print "  ", l
        nl = int(l.rstrip("-beta"))
        na = int(v2[i].rstrip("-beta"))

        if nl > na:
            return True
        elif nl < na:
            break

    return False
    
    
###############################################################################################
def GetNewVersion(win):
    print("Recherche nouvelle version ...")
    
    # getsion des proxies
    proxy_handler = urllib.request.ProxyHandler()
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)
    print("  proxies :",proxy_handler.proxies)
    
    
    url1 = __urlapi__ + "/releases/latest"
    url2 = __urlapi__ + "/releases"
    
    ##########################################################################################
    def getVerNumId(url):
        req = urllib.request.Request(url)
        try:
            handler = urllib.request.urlopen(req)
        except:
            print("Pas d'accès à Internet")
            return None, None
        
        dic = json.loads(handler.read())
        if type(dic) == list:
            dic = dic[0]
        
        id = dic['id']
        ver = dic['tag_name'].lstrip('v')
        return ver, id


    

    
    #########################################################################################
    latest, id1 = getVerNumId(url1)
    last_ver, id2 = getVerNumId(url2)
    
    if latest is None or last_ver is None:
        return
    
    # Version actuelle
    a = __version__.split('.')
    
    print("   locale  :", __version__)
    print("   serveur :", latest)
    print("   serveur_beta :", last_ver)
    
    # Comparaison
#     new = False
#     for i, l in enumerate(latest.split('.')):
#         nl = int(l.rstrip("-beta"))
#         na = int(a[i].rstrip("-beta"))
# #        print nl,na
#         if nl > na:
#             new = True
#             break
#         elif nl < na:
#             break
#     if new:
#         print latest
#     else:
#         print
    
    new = sup(latest, a)
    newbeta = sup(last_ver, a)
    
    if new:
        dialog = wx.MessageDialog(win, "Une nouvelle version de pySéquence est disponible\n\n" \
                                        "\t%s\n\n" \
                                        "Voulez-vous visiter la page de téléchargement ?" % latest, 
                                      "Nouvelle version", wx.YES_NO | wx.ICON_INFORMATION)
        retCode = dialog.ShowModal()
        if retCode == wx.ID_YES:
            try:
                url = __url__ + "/releases/latest"
                webbrowser.open(url,new=2)
            except:
                from widgets import messageErreur
                messageErreur(None, "Ouverture impossible",
                              "Impossible d'ouvrir l'url\n\n%s\n" %url)

    elif newbeta:
        dialog = wx.MessageDialog(win, "Une nouvelle version de pySéquence est disponible\n\n" \
                                        "\t%s\n\n" \
                                        "... Il s'agit d'une version beta ...\n\n" \
                                        "Voulez-vous visiter la page de téléchargement ?" % last_ver, 
                                      "Nouvelle version beta", wx.YES_NO | wx.ICON_INFORMATION)
        retCode = dialog.ShowModal()
        if retCode == wx.ID_YES:
            try:
                url = __url__ + "/releases/tag/v"+last_ver
                webbrowser.open(url,new=2)
            except:
                from widgets import messageErreur
                messageErreur(None, "Ouverture impossible",
                              "Impossible d'ouvrir l'url\n\n%s\n" %url)
                
    return


    
def test():
    import json
    import urllib.request, urllib.error, urllib.parse
    url = __urlapi__ + "/releases/latest"
    
    req = urllib.request.Request(url)
    print(req)
    print(dir(req))
    handler = urllib.request.urlopen(req)
 
    
    print(dir(handler))
    dic = json.loads(handler.read())
    print(dic['tag_name'])
    print(dic['name'])
    print(dic['draft'])
    print(dic['published_at'])
    for assets in dic['assets']:
        print("   ", assets)
        print("   ", assets['browser_download_url'])
        print("   ", assets['download_count'])
    
    
    
    print(handler.getcode())
    print(req.get_data())
    print(handler.headers.getheader('content-type'))
    
#    repoItem = json.loads(handler.text or handler.content)
#    print repoItem
    

if __name__ == '__main__':
    GetNewVersion(None)

    
    
    
    