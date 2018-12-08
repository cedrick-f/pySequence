#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               getEtab                               ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2015 C�drick FAURY - Jean-Claude FRICOU

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

'''
Created on 1 févr. 2015

@author: Cedrick
'''


# A revoir avec
# http://telechargement.index-education.com/vacances.xml
# https://www.data.gouv.fr/s/resources/adresse-et-geolocalisation-des-etablissements-denseignement-du-premier-et-second-degres/20160526-143453/DEPP-etab-1D2D.csv

# https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education/api/



import xml.etree.ElementTree as ET
import util_path
import os
import time


#############################################################################################
def GetFeries(win):
    print("GetFeries")
    from bs4 import BeautifulSoup
    import urllib.request, urllib.error, urllib.parse
    from objects_wx import myProgressDialog

    MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 
        'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
    
    message = "Recherche des jours fériés\n\n"
    
    ETABLISSEMENTS = ouvrir()
    lstAcad = sorted([a[0] for a in list(ETABLISSEMENTS.values())])
    
    
    urlCal = 'http://www.education.gouv.fr/pid25058/le-calendrier-scolaire.html' #?annee=160&search_input=cancale'
    try:
        downloadPage = BeautifulSoup(urllib.request.urlopen(urlCal, timeout = 10), "html5lib")
    except IOError:
        print("pas d'accès Internet")
        return   
    
    list_feries = {}
    
    
    
    
    annees = {}
    tag_annee = downloadPage.find(id="annee")
    for a in tag_annee.find_all('option'):
#        print "     a:", a['label'].split("-")[0].split()[-1], annee
        annees[int(a['label'].split("-")[0].split()[-1])] = a['value']
            
    print("  annees:", annees)
    
    
    dlg = myProgressDialog("Recherche des jours fériés",
                                   message,
                                   len(annees),
                                   parent=win
                                    )
    dlg.Show()
    count = 1
    
    
    for annee, code in list(annees.items()):
        count += 1
        message += "Année : "+ str(annee) + "\n"
        dlg.update(count, message)
        list_crenaux = {"A" : [], "B" : [], "C" : []} # Les créneaux de jours féries
        list_zones = {"A" : [], "B" : [], "C" : []} # Les académies rangées par zone
    
        url = urlCal + '?annee=%s' %code
    
        page = BeautifulSoup(urllib.request.urlopen(url, timeout = 10), "html5lib")
        
        tag_cal = page.find(id="calendrier-v2-detail")
        for z, tag_acad in enumerate(tag_cal.find_all(headers="academie")):
            for i, acad in enumerate(lstAcad):
                if tag_acad.text is not None and acad in tag_acad.text:
                    list_zones[chr(65+z)].append(i)
        print("  zones:", list_zones)


        for tr in tag_cal.find_all('tr'):
            creneaux = tr.find_all('td', headers="creneau")
            for z, creneau in enumerate(creneaux):
                for p in creneau.find_all('p'):
                    l = p.text.split("\n")
                    l = [t.strip() for t in l]
                    l = [t for t in l if len(t) > 0]
                    
                    if len(l) == 1:
                        if l[0][0] == "R":
                            l = ["", l [0]]
                        else:
                            l = [l [0],  ""]
                    l = [t.split(":")[-1].strip() for t in l]
                    v = []
                    for d in l:
                        
                        if d == "":
                            v.append([])
                        else:
                            js, j, m, a = d.split()
                            a = int(a)
                            m = MOIS.index(m)+1
                            if j == "1er":
                                j = 1
                            else:
                                j = int(j)
                            v.append([a, m, j])
                    
                    if v[0] == []:
                        v[0] = [v[1][0], 7, 31]
                    elif v[1] == []:
                        v[1] = [v[0][0], 7, 31]
                            
                    list_crenaux[chr(65+z)].append(v)
                    if len(creneaux) == 1:
                        list_crenaux["B"].append(v)
                        list_crenaux["C"].append(v)
        
        print("   crenaux:",list_crenaux)
        list_feries[annee] = [list_zones, list_crenaux]
        
        wx.Yield()
        if dlg.stop:
            dlg.Destroy()
            print("STOP")
            return []
        
    print(list_feries)
    return list_feries


import wx

#############################################################################################
def GetEtablissements(win):
    
    from bs4 import BeautifulSoup
    import urllib.request, urllib.error, urllib.parse
    from objects_wx import myProgressDialog
    
    # titre, message, maximum, parent, style = 0, btnAnnul = True, msgAnnul = u"Annuler l'opération"
    message = "Recherche des établissements\n\n"
    
    errmsg = ""
    
    tentatives = 0
    
    
#    def getEtabVille(page):
#        lst = []
#        for v in page.find_all('div', attrs={'class':"annuaire-resultats-entete"}):
#            ville = v.contents[0].split(',')[1].lstrip('\n')
#            print "   ville =", v
#            pagev = BeautifulSoup(v, 'xml')
#            for divEtab in pagev.find_all('div', attrs={'class':"annuaire-etablissement-label"}):
#                etab = divEtab.a.string
#                print "     etab =", etab
#                lst.append([etab, ville])
#        return lst
    
    def getEtabVille(page, message):
        lst = []
        for v in page.find_all('div'):
#            print v.attrs.keys(), v['class']
#            print type(v)
            if ('class' in list(v.attrs.keys())) and v['class'][0] == "annuaire-resultats-entete":
                ville = v.contents[0].split(',')[1].lstrip('\n').lstrip()
#                 print "   ville :", ville
                message += "     ville : "+ ville + "\n"
                dlg.update(count, message)
            if ('class' in list(v.attrs.keys())) and v['class'][0] == "annuaire-etablissement-label":
                etab = str(v.a.string)
#                 print "       etab :", etab
#                 message += u"      établissement : "+ etab + u"\n"
#                 dlg.Update(0, message)
                lst.append([etab, ville])
        return lst, message
    
    
                
##        lst = [[e.a.string, []] for e in page.find_all('div', attrs={'class':"annuaire-etablissement-label"})]
#        try:
#            lst = [[e.a['title'].split(' - ')[1], e.a['title'].split(' - ')[-1]] for e in page.find_all('div', attrs={'class':"annuaire-etablissement-autres-liens"})]
#            return lst
#        except:
#            lst = [[e.a.string, u""] for e in page.find_all('div', attrs={'class':"annuaire-etablissement-label"})]
#            return lst
        
    def getNbrEtab(page):
        """ Renvoie le nombre d'établissements dans les résultats de la recherche
        """
        try:
            return str(page.find_all('div', attrs={'class':"annuaire-nb-results"})[0].contents[-2]).strip("<>b/")
        except IndexError:
            return "0"
        
#    def getTousEtabVilleAcad(page):
#        liste_etab = {}
#        for acad, num in liste_acad:
#            liste_etab[num] = [acad, [], []]
#        urlCol = urlEtab + "?college=2&lycee_name=&localisation=4&ville_name=&nbPage=20000"
#        urlLyc = urlEtab + "?lycee=3&lycee_name=&localisation=4&ville_name=&nbPage=20000"
#        
#        return liste_etab
    
    # url = 'https://code.google.com/p/pysequence/downloads/list'
#     print "GetEtablissements"
    urlEtab = 'http://www.education.gouv.fr/pid24302/annuaire-resultat-recherche.html'
    urlAcad = 'http://www.education.gouv.fr/pid24301/annuaire-accueil-recherche.html'
    
    try:
        downloadPage = BeautifulSoup(urllib.request.urlopen(urlAcad, timeout = 10), "html5lib")
    except IOError:
#         message += u"pas d'accès Internet"
#         dlg.Update(0, message)
        print("pas d'accès Internet")
        return   

    acad_select = downloadPage.find(id="acad_select")
    liste_acad = [[o['label'], o['value']] for o in acad_select.find_all('option')]
    liste_acad_txt = [l+"\t"+str(v) for l, v in liste_acad]
#     message += u"Liste des académies :\n   "+ u"\n   ".join(liste_acad_txt)
#     dlg.Update(0, message)
#     print liste_acad
    
    liste_etab = {}
    
    dlg = myProgressDialog("Recherche des établissements",
                                   message,
                                   len(liste_acad)*2,
                                   parent=win
                                    )
    dlg.Show()
#     dlg.maximum = len(liste_acad)*2
    count = 1
    
    for acad, num in liste_acad:
        message += "Académie : "+ acad+ "\t" + str(num) + "\n"
        dlg.update(count, message)
#         print "  ",acad, num
        
        liste_etab[num] = [acad, [], []]
        
        #
        # Collèges
        #
        
#            urlCol = urlEtab + '?'+ 'acad_select[]=' + str(num) + '&critere_gene_2=1&valid_aff=Chercher'
#        urlCol = urlEtab + '?college=2&lycee_name=&ville_name=&localisation=3&nbPage=1000&acad_select[]='+num
#        urlCol = urlEtab + "?college=2&lycee_name=&localisation=2&dept_select[]=01"
#        page = BeautifulSoup(urllib2.urlopen(urlCol, timeout = 5))
        urlCol = urlEtab + '?college=2&localisation=3&nbPage=1000&acad_select[]='+num
        message += "  Collèges :\n  ----------\n"
        dlg.update(count, message)
#         print "  ", urlCol
        
        continuer = True
        n = 0
        while continuer:
            try:
                page = BeautifulSoup(urllib.request.urlopen(urlCol, timeout = 5), "html5lib")
                tentatives = 0
            except urllib.error.HTTPError:
                time.sleep(1)
                tentatives += 1
                message += "+"
                dlg.update(count, message)
                if tentatives > 10:
                    break
                else:
                    continue
#            print page.find_all('a', attrs={'class':"annuaire-modif-recherche"})[0]['href']
            if "select[]="+str(num) in page.find_all('a', attrs={'class':"annuaire-modif-recherche"})[0]['href'] \
                or n>10:
                continuer = False
            n += 1
#             message += u"."
#             dlg.Update(0, message)
#             print "   .",
        l, message = getEtabVille(page, message)
        liste_etab[num][1].extend(l)
        
        r = len(liste_etab[num][1]) # Récupérés
        t = int(getNbrEtab(page))        # Trouvés
        if r < t:
            errmsg += "Académie "+acad+" : manque "+str(t-r)+" Collèges !\n"
            
        count += 1
        message += "  " + str(r) + " / " + str(t) + " collèges récupérés\n\n"
        dlg.update(count, message)
        
#         print "   ", len(liste_etab[num][1]),"/",
#         print getNbrEtab(page)
        
#        tt = tt.replace('<b>', '')
#        tt = tt.replace('</b>', '')
#        print tt.split()[-1]

#        <div class="annuaire-nb-results">
#Résultats <b>1 à 43</b> sur <b>43</b>
#</div>
        
        # Lycées
#            urlLyc = urlEtab + '?'+ 'acad_select[]=' + str(num) + '&critere_gene_3=1&valid_aff=Chercher'
#        urlLyc = urlEtab + '?lycee=3&lycee_name=&ville_name=&localisation=3&nbPage=1000&acad_select[]='+num
#        urlLyc = urlEtab + "?lycee=3&lycee_name=&localisation=2&dept_select[]=01"
#        page = BeautifulSoup(urllib2.urlopen(urlLyc, timeout = 5))
        urlLyc = urlEtab + '?lycee=3&localisation=3&nbPage=1000&acad_select[]='+num
        message += "  Lycées :\n  --------\n"
        dlg.update(count, message)
#         print "  ", urlLyc

        continuer = True
        n = 0
        while continuer:
            try:
                page = BeautifulSoup(urllib.request.urlopen(urlLyc, timeout = 5), "html5lib")
                tentatives = 0
            except urllib.error.HTTPError:
                time.sleep(1)
                tentatives += 1
                message += "+"
                dlg.update(count, message)
                if tentatives > 10:
                    break
                else:
                    continue
#            print page.find_all('a', attrs={'class':"annuaire-modif-recherche"})[0]['href']
            if "select[]="+str(num) in page.find_all('a', attrs={'class':"annuaire-modif-recherche"})[0]['href'] \
                or n>10:
                continuer = False
            n += 1
#             message += u"."
#             dlg.Update(0, message)
#             print "   .",
        l, message = getEtabVille(page, message)
        liste_etab[num][2].extend(l)
        
        r = len(liste_etab[num][2]) # Récupérés
        t = int(getNbrEtab(page))        # Trouvés
        
        if r < t:
            errmsg += "Académie "+acad+" : manque "+str(t-r)+" Lycées !\n"
        count += 1
        message += "  " + str(r) + " / " + str(t) + " lycées récupérés\n\n"
        dlg.update(count, message)
        
        
        wx.Yield()
        if dlg.stop:
            dlg.Destroy()
            print("STOP")
            return []
        
#         print "   ", len(liste_etab[num][2]),"/",
#         print getNbrEtab(page)
#         print 

    message += "\nOpération Terminée !\n"
    if errmsg != "":
        message += "ERREURS de récupération :\n"
        message += errmsg
    dlg.update(count, message)
#    print liste_etab
    return liste_etab
        

######################################################################################  
def insert_branche(branche, val, nom):
    nom = nom.replace("\n", "--")
#        print nom, type(val)
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
    elif type(val) == list:
        sub = ET.SubElement(branche, "l_"+nom)
        for i, sv in enumerate(val):
            insert_branche(sub, sv, nom+format(i, "02d"))
    elif type(val) == dict:
        sub = ET.SubElement(branche, "d_"+nom)
        for k, sv in list(val.items()):
            if type(k) != str and type(k) != str:
                k = "_"+format(k, "03d")
            insert_branche(sub, sv, k)


######################################################################################  
def getBranche(item, titre = "Etablissements"):
    """ Construction et renvoi d'une branche XML
        (enregistrement de fichier)
    """
    ref = ET.Element(titre)

    insert_branche(ref, item, "Etablissement")
        
    return ref


######################################################################################
def setBranche(branche, nom = "d_Etablissement"):
    """ Lecture de la branche XML
        (ouverture de fichier)
    """
    nomerr = []
    
    def lect(branche, nom = ""):
        
        if nom[:2] == "S_":
            return str(branche.get(nom)).replace("--", "\n")
        elif nom[:2] == "I_":
            return int(eval(branche.get(nom)))
        elif nom[:2] == "L_":
            return int(eval(branche.get(nom)))
        elif nom[:2] == "F_":
            return float(eval(branche.get(nom)))
        elif nom[:2] == "B_":
            if branche.get(nom) == None: # Pour corriger un bug (version <=5.0beta3)
                nomerr.append(nom)
                return False 
            return branche.get(nom)[0] == "T"
        elif nom[:2] == "l_":
            sbranche = branche.find(nom)
            if sbranche == None: return []
            dic = {}
            for k, sb in list(sbranche.items()):
                _k = k[2:]
                if isinstance(_k, str) and "--" in _k:
                    _k = _k.replace("--", "\n")
                dic[_k] = lect(sbranche, k)
            for sb in list(sbranche):
                k = sb.tag
                _k = k[2:]
                if isinstance(_k, str) and "--" in _k:
                    _k = _k.replace("--", "\n")
                dic[_k] = lect(sbranche, k)
#                print dic.values()
            liste = [dic[v] for v in sorted(dic)]
#                print " >", liste
            return liste
#                liste = [lect(sbranche, k) for k, sb in sbranche.items()]
#                return liste + [lect(sb, k) for k, sb in list(sbranche)]
        elif nom[:2] == "d_":
            sbranche = branche.find(nom)
            d = {}
            if sbranche != None:
                for k, sb in list(sbranche.items()):
                    _k = k[2:]
                    if isinstance(_k, str) and "--" in _k:
                        _k = _k.replace("--", "\n")
                    d[_k] = lect(sbranche, k)
                for sb in list(sbranche):
                    k = sb.tag
                    
                    _k = k[2:]
                    if _k[0] == "_":
                        _k = eval(_k[1:])
                    if isinstance(_k, str) and "--" in _k:
                        _k = _k.replace("--", "\n")
                    d[_k] = lect(sbranche, k)
            return d

    return lect(branche, nom)


def ouvrir():
    fichier = open(os.path.join(util_path.PATH, r"Etablissements.xml"),'r')
    root = ET.parse(fichier).getroot()
    ETABLISSEMENTS = setBranche(root)
    fichier.close()
    return ETABLISSEMENTS

def ouvrir_jours_feries():
    fichier = open(os.path.join(util_path.PATH, r"JoursFeries.xml"),'r')
    root = ET.parse(fichier).getroot()
    JOURS_FERIES = setBranche(root, "d_Jours_feries")
    fichier.close()
    return JOURS_FERIES


#    
# Fonction pour indenter les XML générés par ElementTree
#
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i




def SauvEtablissements(win, path):
    liste_etab = GetEtablissements(win)
    if len(liste_etab) > 0:
        nomF = os.path.join(path, "Etablissements.xml")
#         fichier = open(nomF, 'w', encoding = "utf-8")
        root = getBranche(liste_etab)
        indent(root)
        ET.ElementTree(root).write(nomF)#, encoding = "utf-8")
#         fichier.close()
        return nomF



def SauvFeries(win, path):
    list_feries = GetFeries(win)
    if len(list_feries) > 0:
        nomF = os.path.join(path, "JoursFeries.xml")
#         fichier = open(nomF, 'w', encoding = "utf-8")
        root = getBranche(list_feries)
        indent(root)
        ET.ElementTree(root).write(nomF)
#         fichier.close()
        return nomF
    
    
if __name__ == '__main__':
    pass
    
#     liste_etab = GetEtablissements(None)
    
#     
#     fichier = file("JoursFeries.xml", 'w')
#     root = ET.Element("Jours_feries")
#     list_feries = GetFeries()
#     insert_branche(root, list_feries, "Jours_feries")
#     indent(root)
# #    print ET.tostring(root, encoding='utf8', method='xml')
#     ET.ElementTree(root).write(fichier)
#     fichier.close()


    
    
    
    
    
    