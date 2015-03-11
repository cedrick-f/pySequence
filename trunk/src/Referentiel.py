#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               Referentiel                               ##
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


'''
Created on 15-06-2014

@author: Cedrick
'''

import xlrd
from xlrd import open_workbook

import constantes
import os
 
import wx   # Juste pour la fonction GetBitmap()

# Pour enregistrer en xml
import xml.etree.ElementTree as ET
Element = type(ET.Element(None))


#########################################################################################
DOSSIER_REF = "referentiels"
REFERENTIELS = {}
ARBRE_REF = {}    

###########################################################
def int0(txt):
    try:
        return int(txt)
    except:
        return 0
    
###########################################################
def includeElem(pl, gl):
    """ Teste si un élément de la petite liste <pl>
        est inclu dans la grande liste <gl>
    """
    for e in pl:
        if e in gl: return True
    return False



                                
                                
class XMLelem():
    ######################################################################################  
    def getBranche(self, nomb = ""):
        """ Construction et renvoi d'une branche XML
            (enregistrement de fichier)
        """
        if nomb != "":
            nomb = "_" + nomb
        ref = ET.Element(str(self._codeXML+nomb))

        def sauv(branche, val, nom = None):
            nom = nom.replace("\n", "--")
            if type(val) == str or type(val) == unicode:
                branche.set("S_"+nom, val.replace("\n", "--"))
            elif type(val) == int:
                branche.set("I_"+nom, str(val))
            elif type(val) == long:
                branche.set("L_"+nom, str(val))
            elif type(val) == float:
                branche.set("F_"+nom, str(val))
            elif type(val) == bool:
                branche.set("B_"+nom, str(val))
            elif type(val) == list:
                sub = ET.SubElement(branche, "l_"+nom)
                for i, sv in enumerate(val):
                    sauv(sub, sv, format(i, "02d"))
            elif type(val) == dict:
                sub = ET.SubElement(branche, "d_"+nom)
                for k, sv in val.items():
                    if type(k) != str and type(k) != unicode:
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
    def setBranche(self, branche):
        """ Lecture de la branche XML
            (ouverture de fichier)
        """
#        print "setBranche", self._codeXML
    
        nomerr = []
        
        def lect(branche, nom = ""):
            if nom[:2] == "S_":
                return unicode(branche.get(nom)).replace(u"--", u"\n")
            elif nom[:2] == "I_":
                return int(eval(branche.get(nom)))
            elif nom[:2] == "L_":
                return long(eval(branche.get(nom)))
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
                for k, sb in sbranche.items():
                    _k = k[2:]
                    if isinstance(_k, (str, unicode)) and "--" in _k:
                        _k = _k.replace("--", "\n")
                    dic[_k] = lect(sbranche, k)
                for sb in list(sbranche):
                    k = sb.tag
                    _k = k[2:]
                    if isinstance(_k, (str, unicode)) and "--" in _k:
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
                    for k, sb in sbranche.items():
#                        print k, sb
#                        _k = k[2:]
                        _k = k.split("_")[1]
                        if isinstance(_k, (str, unicode)) and "--" in _k:
                            _k = _k.replace("--", "\n")
                        d[_k] = lect(sbranche, k)
                    for sb in list(sbranche):
                        k = sb.tag
#                        _k = k[2:]
                        _k = k.split("_")#[1]
                        if len(_k) == 3:#k =="":#_k[0] == "_":
                            _k = eval(_k[2])
                        else:
                            _k = _k[1]
                        if isinstance(_k, (str, unicode)) and "--" in _k:
                            _k = _k.replace("--", "\n")
                        d[_k] = lect(sbranche, k)
                return d
            
            elif nom.split("_")[0] == "Indicateur":
                sbranche = branche.find(nom)
                return Indicateur().setBranche(sbranche)[0]
            
            elif nom.split("_")[0] == "Projet":
                sbranche = branche.find(nom)
                return Projet().setBranche(sbranche)[0]
            

        for attr in dir(self):
            if attr[0] != "_":
                val = getattr(self, attr)
                if type(val) == str or type(val) == unicode:
                    _attr = "S_"+attr
                elif type(val) == int:
                    _attr = "I_"+attr
                elif type(val) == long:
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
                    
                if _attr != None:
                    setattr(self, attr, lect(branche, _attr.replace("\n", "--")))
                

        return self, nomerr

    ######################################################################################  
    def __eq__(self, ref):
        """ Comparaison de deux référentiels
        """
        if not isinstance(ref, type(self)):
            return False
        
        def egal(val1, val2):
            if isinstance(val1, (str, unicode)) and isinstance(val2, (str, unicode)):
#                if val1 != val2:#.replace("\n", "--"):
#                    print "Erreur s : xml =", val1, "      xls =", val2#.replace("\n", "--")
                return val1 == val2#.replace("\n", "--")
            elif isinstance(val1, (int, long, float)) and isinstance(val2, (int, long, float)):
#                if val1 != val2:
#                    print "Erreur : xml =", val1, "      xls =", val2
                return val1 == val2
            elif type(val1) == bool and type(val2) == bool:
#                if val1 != val2:
#                    print "Erreur : xml =", val1, "      xls =", val2
                return val1 == val2
            
            elif type(val1) == list:
                if len(val1) != len(val2):
#                    print "Erreur : xml =", val1, "      xls =", val2
                    return False
                e = True
                for sval1, sval2 in zip(val1, val2):
                    e = e and egal(sval1, sval2)
                return e
            
            elif type(val1) == dict and type(val2) == dict:
                if not egal(sorted(val1), sorted(val2)):
#                    print "Erreur : xml =", val1, "      xls =", val2
                    return False
                e = True
                for k, v in val1.items():
#                    if isinstance(k, (str, unicode)):
#                        k = k.replace("--", "\n")
                    e = e and egal(v, val2[k])
                return e
            
            elif isinstance(val1, XMLelem) and isinstance(val2, XMLelem):
                return val1 == val2
            
            else:
#                print "Erreur : xml =", val1, "      xls =", val2
                return False
        
        for attr in dir(self):
            if attr[0] != "_":
                val1 = getattr(self, attr)
                if isinstance(val1, (str, unicode, int, long, float, bool, list, dict, XMLelem)) :
                    val2 = getattr(ref, attr)
                    if not egal(val1, val2):
                        print "Différence"
                        print "  ", attr
                        print "  ", val1
                        print "  ", val2
                        break
                        return False
        return True



    ###########################################################
    def normaliserPoids(self, dic, debug = False):
        for k0, v0 in dic.items():
            if len(v0) > 2:
    #                    print self.parties.keys()
                tot = {}
                for p in self.parties.keys():
                    tot[p] = 0
                    
                if type(v0[1]) == dict :
                    lstindic = []
                    for v1 in v0[1].values():
                        for ii in v1[1]:
                            lstindic.append(ii)
                else:
                    lstindic = v0[1]
                    
                if debug: print "   ", lstindic
                
                for indic in lstindic:
                    for part, poids in indic.poids.items():
                        if part in tot.keys():
                            tot[part] = tot[part] + poids
                if debug: print "  tot", tot
                
                coef = {}
                for p in self.parties.keys():
                    coef[p] = 1.0*tot[p]/100
                if debug: print "  coef", coef
                
                for indic in lstindic:
                    for part, poids in indic.poids.items():
                        if part in coef.keys() and coef[part] != 0:
                            indic.poids[part] = round(indic.poids[part] / coef[part], 6)


    ###########################################################
    def getPremierEtDernierNiveauArbre(self, dic):
        sdic = {}
        for k0, v0 in dic.items():
            if len(v0) > 1 and  type(v0[1]) == dict:
                if len(v0) == 3: # premier niveau = [intitule, dict ou liste, poids]
                    sdic[k0] = [v0[0], self.getDernierNiveauArbre(v0[1]), v0[2]]
                else:
                    sdic.update(self.getDernierNiveauArbre(v0[1]))
            else:
                sdic[k0] = v0
        return sdic
    
    
    ###########################################################
    def getArbreProjet(self, dic, debug = False):
#        print "getArbreProjet", self.parties.keys()
        sdic = {}
        for k0, v0 in dic.items():
            if debug: print k0
            if len(v0) > 1 and type(v0[1]) == dict:
                if debug: print "   ", v0
                if len(v0) == 2:
                    sdic[k0] = [v0[0], self.getArbreProjet(v0[1], debug = debug)]
                else:
                    if debug: print "   prem's", v0[2]
                    
                    if includeElem(self.parties.keys(), v0[2].keys()):
#                        if len(v0[2]) > 0 and not v0[2].keys() == ['E']:
#                        if v0[2][1] != 0 or v0[2][2] != 0: # Conduite ou Soutenance
                        sdic[k0] = [v0[0], self.getArbreProjet(v0[1], debug = debug), v0[2]]
            else:
                lst = []
                for l in v0[1]:
                    if debug: print l
                    if l.estProjet(): # Conduite ou Soutenance
                        lst.append(l)
                if lst != []:
                    if len(v0) > 2:
                        sdic[k0] = [v0[0], lst, v0[2]]
                    else:
                        sdic[k0] = [v0[0], lst]
        return sdic
    
    ###########################################################
    def getDernierNiveauArbre2(self, dic):
        sdic = {}
        for k0, v0 in dic.items():
            if type(v0) == dict:
                sdic.update(self.getDernierNiveauArbre(v0))
            else:
                sdic[k0] = v0
        return sdic
    
    
    ###########################################################
    def getDeuxiemeNiveauArbre(self, dic):
        sdic = {}
#            if len(dic) > 0 and type(dic.values()[0][1]) == dict:
        for k0, v0 in dic.items():
            if type(v0[1]) == dict:
                for k1, v1 in v0[1].items():
                    if len(v1) > 1 and  type(v1[1]) == dict: # pas fini = 3ème niveau
                        self._niveau = 3
                        sdic[k1] = {}
                        for k2, v2 in v1[1].items():
                            sdic[k1][k2] = v2[1]
                    else:   # Niveau "indicateur"
                        self._niveau = 2
                        sdic[k1] = v1[1]
            else:
                sdic[k0] = v0[1]
#            else:
#                return dic
        return sdic
    
    ###########################################################
    def getDernierNiveauArbre(self, dic):
        sdic = {}
        for k0, v0 in dic.items():
            if len(v0) > 1 and  type(v0[1]) == dict:
                sdic.update(self.getDernierNiveauArbre(v0[1]))
            else:
                sdic[k0] = v0
        return sdic
    
#################################################################################################################################
#
#        Référentiel
#
#################################################################################################################################
class Referentiel(XMLelem):
    
    def __init__(self, nomFichier = r""):
        # Enseignement       Famille,    Nom    , Nom complet
        
        self._codeXML = "Referentiel"
        self.initParam()
        self._bmp = None
        
        if nomFichier != r"":
            self.importer(nomFichier)

    ######################################################################################  
    def __repr__(self):
#        print "*********************"
#        print self.Code
#        print "positions_CI", self.positions_CI
##        print "CI_BO :", self.CI_BO
##        print "CI  :", self.CentresInterets
##        print "Sav :", self.dicSavoirs
##        print "dicSavoirs_Math", self.dicSavoirs_Math
##        for p in self.getParams():
##            v = getattr(self, p)
##            if type(v) == dict:
##                print p, v
##        print "dicCompetences :", self.dicCompetences
##        print "Mat :", self.dicSavoirs_Math
##        print "Phy :", self.dicSavoirs_Phys
#        print "Dem :", self.demarches
##        print "Act :", self.activites
##        print "Sea :", self.seances
#        print "DeS :", self.demarcheSeance

        return self.Code
    
    ######################################################################################  
    def initParam(self):
        #
        # Généralités
        #
        self.Famille = u""
        self.Code = u""
        self.Enseignement = [u""    ,   u"",    u""]
        self.options = {}               # options de l'enseignement : {Code : nomFichier}
        self.tr_com = []                # tronc commun de l'enseignement : [Code, nomFichier]
        
        self.periodes = []              # découpage de l'enseignement en années/périodes
        self.FichierLogo = r""          # Fichier désignant l'image du Logo de l'enseignement
        
        
        #
        # Projets
        #
        self.projets = {}
        self.aColNon = {}               # Pour indiquer si les différentes parties d'un projet ont une colonne "NON" dans leur grille
        self.compImposees = {}          # Indique que les competences sont imposées pour chaque revue
        self.parties = {}
        
        #
        # Centre d'intérêt
        #
        self.nomCI = u"Centres d'intérêt"
        self.abrevCI = u"CI"
        self.CentresInterets = []       #
        self.CI_BO = True               # les ci sont donnés par le B.O. (pas modifiables)
        self.CI_cible = False           # les ci se placent sur une cible MEI FSC
        self.positions_CI = []          # positions sur la cible MEI FSC
        
        
        #
        # Savoirs ou capacités
        #
        self.nomSavoirs = u"Savoirs"    # nom donnés aux savoirs : "Savoirs", "Capacités", ...
        self.surnomSavoirs = u""
        self.dicSavoirs = {}

        #
        # Compétences
        #
        self.nomCompetences = u"Compétences"    # nom donnés aux compétences : "Compétences", ...
        self.nomIndicateurs = u"Indicateurs de performance" 
        self.dicCompetences = {}
        
        
#        self.dicCompetences_prj = {}
#        self.dicIndicateurs_prj = {}
#        self.dicPoidsIndicateurs_prj = {}
#        self.dicLignesIndicateurs_prj = {}

        #
        # Fonctions/Tâches
        #
        self.nomFonctions = u"Fonctions"    # nom donnés aux Fonctions : "Fonctions", ...
        self.nomTaches = u"Tâches"          # nom donnés aux Tâches : "Tâches", ...
        self.dicFonctions = {}
        
        
        #
        # Pratique pédagogiques
        #
        self.demarches = {}
        self.listeDemarches = []
        self.seances = {}
        self.activites = {}
        self.listeTypeSeance = []
        self.listeTypeActivite = []
        self.demarcheSeance = {}
        
        #
        # Effectifs
        #
        self.effectifs = {}
        self.listeEffectifs = []
        self.effectifsSeance = {} #{"" : []}
        
        self.nomSavoirs_Math = u"Mathématiques"
        self.dicSavoirs_Math = {}
        self.objSavoirs_Math = False
        self.preSavoirs_Math = True
            
        self.nomSavoirs_Phys = u"Sciences Physiques"
        self.dicSavoirs_Phys = {}
        self.objSavoirs_Phys = False
        self.preSavoirs_Phys = True
        
        
        
        
        #
        # Bulletins Officiels
        #
        self.BO_dossier = []
        self.BO_URL = []
        
        

    
    ######################################################################################
    def setBrancheCodeV5(self, branche):
        try:
            return branche.get("S_Code")
        except:
            return
        
    ######################################################################################
    def setBrancheV5(self, branche):
        """ Lecture de la branche XML
            (ouverture de fichier)
        """
        print "setBranche référentiel V5"
        self.initParam()

        nomerr = []
        
        def lect(branche, nom = ""):
            if nom[:2] == "S_":
                return unicode(branche.get(nom)).replace(u"--", u"\n")
            elif nom[:2] == "I_":
                return int(eval(branche.get(nom)))
            elif nom[:2] == "L_":
                return long(eval(branche.get(nom)))
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
                for k, sb in sbranche.items():
                    _k = k[2:]
                    if isinstance(_k, (str, unicode)) and "--" in _k:
                        _k = _k.replace("--", "\n")
                    dic[_k] = lect(sbranche, k)
                for sb in list(sbranche):
                    k = sb.tag
                    _k = k[2:]
                    if isinstance(_k, (str, unicode)) and "--" in _k:
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
                    for k, sb in sbranche.items():
                        _k = k[2:]
                        if isinstance(_k, (str, unicode)) and "--" in _k:
                            _k = _k.replace("--", "\n")
                        d[_k] = lect(sbranche, k)
                    for sb in list(sbranche):
                        k = sb.tag
                        
                        _k = k[2:]
                        if _k[0] == "_":
                            _k = eval(_k[1:])
                        if isinstance(_k, (str, unicode)) and "--" in _k:
                            _k = _k.replace("--", "\n")
                        d[_k] = lect(sbranche, k)
                return d


        for attr in dir(self):
            if attr[0] != "_":
                val = getattr(self, attr)
                if type(val) == str or type(val) == unicode:
                    _attr = "S_"+attr
                elif type(val) == int:
                    _attr = "I_"+attr
                elif type(val) == long:
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
                if _attr:
                    setattr(self, attr, lect(branche, _attr.replace("\n", "--")))
        
        # Pour corriger une erreur de jeunesse de la 5.0beta1
        if len(self.aColNon) == 0:
            self.aColNon = {'R' : True,  'S' : False}

#        # Pour corriger une erreur de jeunesse de la 5.0beta3
#        if self.Code in ['SIN', 'ITEC', 'AC', 'EE']:
#            self.tr_com == True
        
        # Pour rajouter les periodes aux fichiers < 5.7
        if self.periodes == []:
            self.periodes = self.defPeriode()
#            print ">>>", self.periode_prj
            
        # Pour ajouter les noms des CI < 5.8
        if self.nomCI == "None":
            self.nomCI = u"Centres d'intérêt"
            self.abrevCI = u"CI"
        
        # Pour ajouter savoirs prérequis/objectifs < 5.9
        if "B_objSavoirs_Math" in nomerr:
            self.nomSavoirs_Math = u"Mathématiques"
            self.nomSavoirs_Phys = u"Sciences Physiques"
            self.objSavoirs_Math = False
            self.preSavoirs_Math = True
            self.objSavoirs_Phys = False
            self.preSavoirs_Phys = True
        
        # Pour mettre à jour les généralités sur le projet
        if self.attributs_prj == {}:
            self.attributs_prj = REFERENTIELS[self.Code].attributs_prj
            
        ###########################################################
        def corrigeArbreProjet(dic, debug = False):
            for k0, v0 in dic.items():
                if debug: print k0
                if len(v0) > 1 and type(v0[1]) == dict:
                    if debug: print "   ", v0[0]
                    if len(v0) == 2:
                        corrigeArbreProjet(v0[1], debug = debug)
                    else:
                        if debug: print "   prem's", v0[2]
                        if v0[2][1] != 0 or v0[2][2] != 0: # Conduite ou Soutenance
                            corrigeArbreProjet(v0[1], debug = debug)
                else:
                    lst = []
                    for l in v0[1]:
                        if debug: print l
                        if l != None and not isinstance(l, Indicateur):
                            if debug: print "Correction"
                            lst.append(Indicateur(l[0], l[1], l[2]))
                    v0[1] = lst
            return
        
        corrigeArbreProjet(self.dicCompetences, debug = False)
#        print "dicCompetences Corr", self.dicCompetences
        self.postTraiter()
        self.completer()

        return
    ######################################################################################  
    def getParams(self):
        l = []
        for attr in dir(self):
            if attr[0] != "_":
                val = getattr(self, attr)
                if isinstance(val, (str, unicode, int, long, float, bool, list, dict)):
                    l.append(attr)
        return l
        
    
    
        
    
        
        
    ######################################################################################
    def corrigerVersion(self, nomerr):
        """ Lecture de la branche XML
            (ouverture de fichier)
        """
#        print "corrigerVersion"
#        print self.projets
#        print 
        
        
        # Pour corriger une erreur de jeunesse de la 5.0beta1
#        if len(self.aColNon) == 0:
#            self.aColNon = {'R' : True,  'S' : False}

#        # Pour corriger une erreur de jeunesse de la 5.0beta3
#        if self.Code in ['SIN', 'ITEC', 'AC', 'EE']:
#            self.tr_com == True
        
        # Pour rajouter les periodes aux fichiers < 5.7
        if self.periodes == []:
            self.periodes = self.defPeriode()
#            print ">>>", self.periode_prj
            
        # Pour ajouter les noms des CI < 5.8
        if self.nomCI == "None":
            self.nomCI = u"Centres d'intérêt"
            self.abrevCI = u"CI"
        
        # Pour ajouter savoirs prérequis/objectifs < 5.9
        if "B_objSavoirs_Math" in nomerr:
            self.nomSavoirs_Math = u"Mathématiques"
            self.nomSavoirs_Phys = u"Sciences Physiques"
            self.objSavoirs_Math = False
            self.preSavoirs_Math = True
            self.objSavoirs_Phys = False
            self.preSavoirs_Phys = True
        
#        # Pour mettre à jour les généralités sur le projet
#        if self.attributs_prj == {}:
#            self.attributs_prj = REFERENTIELS[self.Code].attributs_prj
            
#        print "self.BO_dossier", self.BO_dossier
#        # Pour les BO
#        if type(self.BO_dossier) != list:
#            self.BO_dossier = [self.BO_dossier]
        
        return
        
    
    
    
                    
    ######################################################################################  
    def importer(self, nomFichier):
        """
        """
        self.initParam()
        
        ###########################################################
        def remplir(sh, col, rng, mode = 1, condition = None, debug = False):
            """ Mode = 1 : on finit par une liste
                Mode = 2 : on finit par un dict
            """
            if debug: print "***", col, rng
            if rng == [] and mode == 2:
                return None
#            self.prof_Comp = max(self.prof_Comp, col)
            lig = [l  for l in rng if sh.cell(l,col).value != u""]
            if debug: print lig
            if lig == rng:
                if debug: print "FIN"
                if mode == 1:
                    if col+1 >= sh.ncols or sh.cell(lig[0],col+1).value == u"":
                        return [sh.cell(l,col).value for l in lig]
                    else:
                        d = {}
                        for l in lig:
                            if condition == None or sh.cell(l,4).value == condition:
                                d[str(sh.cell(l,col).value)] = [sh.cell(l,col+1).value, []]
                        return d
                        
                else:
#                    if condition == None or sh.cell(l,4).value == condition:
                    d = {}
                    for l in lig:
                        if condition == None or sh.cell(l,4).value == condition:
                            d[str(sh.cell(l,col).value)] = sh.cell(l,col+1).value
                    if condition == None or len(d) > 0:
                        return d
                    else:
                        return None
            else:
#                if len(lig) > 0:
                
                llig = lig + [rng[-1]+1]
                dic = {}
                for i, p in enumerate(lig):
                    if debug: print "-> ",lig
                    sdic = remplir(sh, col+1, range(p+1, llig[i+1]), mode = mode, condition = condition, debug = debug)
                    if sdic != None:
                        dic[str(sh.cell(p,col).value)] = [sh.cell(p,col+1).value, sdic]
                return dic
          
        
            
        ###########################################################
        def getArbre(sh, rng, col, prems = False, fonction = False, debug = False):
            """ Construit la structure en arbre des "compétences"
            """
            dic = {}
            # Liste des lignes comportant un code dans la colonne <col>, dans l'intervalle <rng>
            lstLig = [l  for l in rng if sh.cell(l,col).value != u""]
            if debug: print "  **",lstLig
            
            for i, l in enumerate(lstLig):
                code = str(sh.cell(l,col).value)
                intitule = unicode(sh.cell(l,col+1).value)
                if debug: print "-> ",l, code, intitule
                
                # Toutes les lignes entre chaque code
                if i < len(lstLig)-1:
                    ssRng = range(l+1, lstLig[i+1])
                else:
                    ssRng = range(l+1, rng[-1]+1)
                if debug: print "   ", ssRng

                # Il y a encore des items à droite ...
                if len(ssRng) > 0 and col < 2 and [li  for li in ssRng if sh.cell(li,col+1).value != u""] != []:
                    dic[code] = [intitule, getArbre(sh, ssRng, col+1, fonction = fonction, debug = debug)]
                    if not fonction:
                        if prems:
                            poids = {}
                            for p, c in self._colParties:
                                v = int0(sh.cell(l,c).value)
                                if v > 0:
                                    poids[p] = v
#                            poids = [int0(sh.cell(l,7).value),  # poids Ecrit
#                                     int0(sh.cell(l,8).value),  # poids Conduite projet
#                                     int0(sh.cell(l,9).value)]  # poids Soutenance projet
                            dic[code].append(poids)
                    else:
                        lstComp = [sh.cell(1,co).value for co in range(5, sh.ncols) if sh.cell(l,co).value != u""]
#                        print "   lstComp1 =", lstComp
                        dic[code].append(lstComp)
                        

                # Il n'y a plus d'item à droite => Indicateur()
                else:
                    dic[code] = [intitule, []]
                    for ll in [l] + ssRng:
                        indic = unicode(sh.cell(ll,5).value)
                        
                        if not fonction:
                            poids = {}
                            lignes = {}
                            revues = {}
                            for p, c in self._colParties:
                                v = int0(sh.cell(ll,c).value)
                                if v > 0:
                                    poids[p] = v
                                    lignes[p] = int0(sh.cell(ll,c+1).value)
                                    revues[p] = int0(sh.cell(ll,c+2).value)
                                    if lignes[p] != 0:
                                        self.aColNon[p] = True
                                    if revues[p] != 0:
                                        self.compImposees[p] = True
                                        
#                            poids = [int0(sh.cell(ll,7).value),  # poids Ecrit
#                                     int0(sh.cell(ll,8).value),  # poids Conduite projet
#                                     int0(sh.cell(ll,9).value)]  # poids Soutenance projet
                            if indic == u"":
    #                            print "code", code, poids
                                dic[code].append(poids)
                            else:
#                                ligne = int0(sh.cell(ll,10).value)   # ligne dans la grille
#                                if ligne != 0:
#                                    if poids[1] != 0:
#                                        self.aColNon['R'] = True
#                                    elif poids[2] != 0:
#                                        self.aColNon['S'] = True
#                                revue = 0
#                                if sh.ncols > 11:
#                                    revue = int0(sh.cell(ll,11).value)
                                
                                dic[code][1].append(Indicateur(indic, poids, lignes, revues))
                        else:
                            lstComp = [sh.cell(1,co).value for co in range(5, sh.ncols) if sh.cell(ll,co).value != u""]
#                            print "   lstComp2 =", lstComp
                            dic[code][1] = lstComp
            
            if debug: print 
            return dic

                
        ###########################################################
        def listItemCol(sh, col, rng):
            return [[l, sh.cell(l,col).value]    for l in rng    if sh.cell(l,col).value != u""]
        
        ###########################################################
        def aplatir2(dic, niv=1):
            ddic = {}
            for k0, v0 in dic.items():
                ddic.update(v0[1])
            return ddic
        
        #
        # Ouverture fichier EXCEL
        #
        wb = open_workbook(nomFichier)
        sh = wb.sheets()
        
        #
        # Généralités
        #
        sh_g = wb.sheet_by_name(u"Généralités")
        self.Famille = sh_g.cell(2,0).value
        self.Code = sh_g.cell(2,1).value
        self.Enseignement[0] = sh_g.cell(6,0).value #Abréviation    
        self.Enseignement[1] = sh_g.cell(6,1).value #Nom complet    
        self.Enseignement[2] = sh_g.cell(6,2).value #Famille

        if sh_g.ncols > 3:
            lig = [l  for l in range(10, 17) if sh_g.cell(l,3).value != u""]
            for l in lig:
                self.periodes.append([sh_g.cell(l,2).value, int(sh_g.cell(l,3).value)])
            
        self.FichierLogo = sh_g.cell(6,3).value
        
        #
        # Projets
        #
        col = [c  for c in range(1, sh_g.ncols) if sh_g.cell(24,c).value != u""]
        for c in col:
            self.projets[sh_g.cell(25,c).value] = Projet(sh_g.cell(25,c).value,
                                                         intitule = sh_g.cell(24,c).value, 
                                                         duree = int0(sh_g.cell(26,c).value), 
                                                         periode = [int(i) for i in sh_g.cell(27,c).value.split()])
#        print self.projets
        
        #
        # options
        #
        sh_g = wb.sheet_by_name(u"Généralités")
        lig = [l  for l in range(10, 17) if sh_g.cell(l,0).value != u""]
        for l in lig:
            self.options[str(sh_g.cell(l,0).value)] = sh_g.cell(l,1).value
        
        #
        # tronc commun
        #
        if sh_g.cell(21,0).value != u"":
            self.tr_com = [sh_g.cell(21,0).value, sh_g.cell(21,1).value]
           
#        #
#        # projet
#        #
#        self.projet = sh_g.cell(23,1).value[0].upper() == "O"
#        if self.projet:
#            self.duree_prj = int(sh_g.cell(24,1).value)
#            self.periode_prj = [int(i) for i in sh_g.cell(25,1).value.split()]

        #
        # Bulletins Officiels
        #
#        print self.Code, sh_g.nrows
        self.BO_dossier = [sh_g.cell(l,0).value for l in range(31, sh_g.nrows) if sh_g.cell(l,0).value != u""]
        self.BO_URL = [[sh_g.cell(l,1).value, sh_g.cell(l,2).value] for l in range(32, sh_g.nrows) if sh_g.cell(l,1).value != u""]
        
#        self.BO_URL = sh_g.cell(29,1).value
#        
#        if sh_g.nrows > 28:
#            self.BO_dossier = [sh_g.cell(ll,0).value for l in [29, 30, 31]]
#            self.BO_URL = sh_g.cell(29,1).value
        
        
        #
        # CI
        #
        sh_ci = wb.sheet_by_name(u"CI")
        self.CI_BO = sh_ci.cell(0,1).value[0].upper() == "O"
        self.CI_cible = sh_ci.cell(1,1).value[0].upper() == "O"
        self.nomCI = sh_ci.cell(2,0).value
        self.abrevCI = sh_ci.cell(2,1).value
        continuer = True
        l = 4
        while continuer:
            if l < sh_ci.nrows:
                ci = sh_ci.cell(l,0).value
                if ci != u"": 
                    self.CentresInterets.append(ci)
                    if self.CI_cible:
                        t = ''
                        for c in range(2,8):
                            if sh_ci.cell(l,c).value != u"":
                                t += sh_ci.cell(3,c).value
                            else:
                                t += ' '
                            if c == 4:
                                t += '_'
                        self.positions_CI.append(t)
                    l += 1
                else:
                    continuer = False
            else:
                continuer = False
           
        #
        # Savoirs
        #     
        sh_va = wb.sheet_by_name(u"Savoirs")  
        self.nomSavoirs =   sh_va.cell(0,0).value 
        self.surnomSavoirs =   sh_va.cell(1,0).value 
        self.dicSavoirs = remplir(sh_va, 0, range(2, sh_va.nrows))
            
        #
        # Compétences
        #
        sh_va = wb.sheet_by_name(u"Compétences")
        self.nomCompetences =   sh_va.cell(0,0).value
        self.nomIndicateurs = sh_va.cell(0,5).value
        

        # Décomposition des projets en parties
        self._colParties = []
        col = [c  for c in range(8, sh_va.ncols) if sh_va.cell(1,c).value != u""]
#        print ">>>", col
        for i, c in enumerate(col):
            if i == len(col)-1:
                n = sh_va.ncols
            else:
                n = col[i+1]
            
            for j in range((n-c)/3):
                cp = c+j*3
                part = sh_va.cell(3,cp).value
                self._colParties.append((part, cp))
                t = sh_va.cell(1,c).value
                for p in self.projets.values():
                    if t == p.intitule:
                        p.parties[part] = sh_va.cell(2,cp).value
                self.compImposees[part] = False
            
#            t = sh_va.cell(1,c).value
#            for p in self.projets.values():
#                if t == p.intitule:
#                    if i == len(col)-1:
#                        n = sh_va.ncols
#                    else:
#                        n = col[i+1]
#        #                    print "     ",n, t
#                    for j in range((n-c)/3):
#                        cp = c+j*3
#        #                        print "         --", cp
#                        part = sh_va.cell(3,cp).value
#                        p.parties[part] = sh_va.cell(2,cp).value
#                        self._colParties.append((part, cp))
#                        self.compImposees[part] = False
#        #                print "   >", p.parties
#        print "_colParties :", self, self._colParties
#        print "compImposees :", self, self.compImposees
        
        for part, col in list(set([cp for cp in self._colParties])):
            self.parties[part] = sh_va.cell(2,col).value
            
        for p in self.projets.values():
            p.importer(wb)
            
#        self.prof_Comp = 0 # compteur de profondeur 
#        self.dicCompetences = remplir(sh_va, 0, range(1, sh_va.nrows), mode = 2)
#        print ">>>", self.Code
        
        # Pour enregistrer s'il y a des colonnes "non" dans les grilles 'R' ou 'S'
#        self.aColNon = {'R' : False,  'S' : False}
        self.dicCompetences = getArbre(sh_va, range(2, sh_va.nrows), 0, prems = True, debug = False)
#        print "dicCompetences", self.dicCompetences
#        print "_aColNon", self.Code, ":", self._aColNon
         
        #
        # Fonctions
        #
        if u"Fonctions" in wb.sheet_names():
            sh_va = wb.sheet_by_name(u"Fonctions")
            self.nomFonctions =   sh_va.cell(0,0).value
            self.nomTaches = sh_va.cell(0,5).value
            self.dicFonctions = getArbre(sh_va, range(2, sh_va.nrows), 0, prems = True, fonction = True, debug = False)
#            print "dicFonctions", self.dicFonctions
            
        #
        # Pratique pédagogiques
        #
        sh_g = wb.sheet_by_name(u"Activité-Démarche")
        for l in range(2, 5):
            if sh_g.cell(l,1).value != u"":
                self.demarches[str(sh_g.cell(l,0).value)] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value]
                self.listeDemarches.append(sh_g.cell(l,0).value)

        for l in range(8, 11):
            if sh_g.cell(l,0).value != u"":
                self.activites[str(sh_g.cell(l,0).value)] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value]
                self.listeTypeActivite.append(sh_g.cell(l,0).value)
                
        self.seances.update(self.activites)
        self.listeTypeSeance = self.listeTypeActivite[:]
        for l in range(14, 21):
            if sh_g.cell(l,0).value != u"":
                self.seances[str(sh_g.cell(l,0).value)] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value]
                self.listeTypeSeance.append(sh_g.cell(l,0).value)
        
        for l, s in enumerate(self.listeTypeActivite):
            l = l + 3
            self.demarcheSeance[str(s)] = [sh_g.cell(2,c).value for c in range(5,8) if sh_g.cell(l,c).value != u""]
        
        #
        # effectifs
        #
        sh_g = wb.sheet_by_name(u"Activité-Effectif")
        for l in range(2, 7):
            if sh_g.cell(l,0).value != u"":
                self.effectifs[str(sh_g.cell(l,0).value)] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value]
                self.listeEffectifs.append(sh_g.cell(l,0).value)
                
        for l, s in enumerate(self.listeTypeSeance):
            l = l + 3
            self.effectifsSeance[str(s)] = [sh_g.cell(2,c).value for c in range(5,10) if sh_g.cell(l,c).value != u""]

        #
        # Savoirs Math
        #
        if u"Math" in wb.sheet_names():
            sh_va = wb.sheet_by_name(u"Math")   
            self.nomSavoirs_Math = sh_va.cell(0,0).value
            self.dicSavoirs_Math = remplir(sh_va, 0, range(1, sh_va.nrows))
            self.objSavoirs_Math = 'O' in sh_va.cell(0,5).value
            self.preSavoirs_Math = 'P' in sh_va.cell(0,5).value
        
        #
        # Savoirs Physique
        #
        if u"Phys" in wb.sheet_names():
            sh_va = wb.sheet_by_name(u"Phys")
            self.nomSavoirs_Phys = sh_va.cell(0,0).value
            self.dicSavoirs_Phys = remplir(sh_va, 0, range(1, sh_va.nrows))
            self.objSavoirs_Phys = 'O' in sh_va.cell(0,5).value
            self.preSavoirs_Phys = 'P' in sh_va.cell(0,5).value
        
        
        
    ###########################################################
    def defPeriode(self):
        """ Définit les periodes
             (dans le cas ou elles ne sont pas définies dans le référentiel intégré
              versions < 5.7)
        """
#        print "defPeriode"
        self.periode_prj = []
        if self.Famille == 'CLG':
            return [[u"Année", 6]]
        elif self.Famille in ['STI', 'SSI']:
            self.periode_prj = [7, 10]
            return [[u"1_ère", 5], [u"T_ale", 5]]
        return [[u"Année", 6]]

#    ###########################################################
#    def getNbrPeriodes(self):
#        if self.Famille == 'CLG':
#            return 5
#        elif self.Famille in ['STI', 'SSI']:
#            return 10
#        return 10
        
    
        
    
    
    
    #########################################################################
    def postTraiter(self):
        """ Complète les données selon que le référentiel ait un tronc commun ou des options
            
            --> le "_" évite que les attributs ne soient sauvegardés dans les XML
            
        """
#        print "postTraiter", self, self.parties
        
#        self._parties = []
#        for proj in self.projets.values():
#            for part in proj.parties:
#                if not part in self._parties:
#                    self._parties.append(part)
                    
                    
        
            
        
        
        
                    
        for p in self.projets.values():
            p.postTraiter(self)
                    

        
        
    #########################################################################
    def completer(self, forcer = False):
        """ Complète les données selon que le référentiel ait un tronc commun ou des options
            Exécuté lorsque tous les référentiels sont chargés !
            
            --> le "_" évite que les attributs ne soient sauvegardés dans les XML
            
        """
        
        # C'est une option (il y a un tronc commun) ==> on complète plus tard
        if not forcer and len(self.tr_com) != 0:
            return
        
#        print "completer ref :", self, self.options
        
        if len(self.options) != 0:
            self.parties = {}
            for ro in self.options.keys():
                for proj in REFERENTIELS[ro].projets.values():
                    for part, n in proj.parties.items():
                        if not part in self.parties.keys():
                            self.parties[part] = n
                
#            print "    ", self.parties
#            print "    ", self.dicCompetences
            self._dicCompetences = self.getArbreProjet(self.dicCompetences, debug = False)
#            print "   >", self._dicCompetences
            self._dicIndicateurs = self.getPremierEtDernierNiveauArbre(self._dicCompetences)
            
            self.normaliserPoids(self._dicIndicateurs, debug = False)
    #        print "                   ", self._dicIndicateurs_prj
            
            self._niveau = 0
            self._dicIndicateurs_famille = self.getDeuxiemeNiveauArbre(self._dicCompetences)
    
            self._dicIndicateurs_simple = self.getDernierNiveauArbre2(self._dicIndicateurs_famille)
        
            for ro in self.options:
                REFERENTIELS[ro].completer(forcer = True)
            
        for p in self.projets.values():
            p.completer(self) 
        
        
        
        
    

    #########################################################################
    def getNbrRevuesDefaut(self, codePrj):
        return self.projets[codePrj].getNbrRevuesDefaut()
    
    #########################################################################
    def getPosRevuesDefaut(self, codePrj):
        return self.projets[codePrj].getPosRevuesDefaut()
    
    #########################################################################
    def getIntituleIndicateur(self, comp):
        sep = "\n\t"+constantes.CHAR_POINT
        indicateurs = self.getIndicateur(comp)
        if type(indicateurs) == list:
            return  "\t"+constantes.CHAR_POINT + sep.join([i[0] for i in indicateurs])
        else:
            t = u""
            for k, v in indicateurs.items():
                t += k + u" : " + v[0]


    #########################################################################
    def getNbrPeriodes(self):
        n = 0
        for p in self.periodes:
            n += p[1]
        return n
    
    
    #############################################################################
    def getPeriodeEval(self, codePrj):
        return self.projets[codePrj].getPeriodeEval()


    #############################################################################
    def getAnnee(self, position):
        n = 0
        for a, p in enumerate(self.periodes):
            if position+n in  range(p[1]):
                return a
            n += p[1]
        return

    #############################################################################
    def getProjetEval(self, position):
        """ Renvoie l'épreuve de projet (évaluation)
            situé à la position <position>
        """
#        print "getProjetEval", position
        for k, p in self.projets.items():
#            print "   ", p.periode
            if position in p.periode:
                return k

    #############################################################################
    def getCodeProjetDefaut(self):
        """ Renvoie l'épreuve de projet (évaluation)
            par défaut (pour les projets d'"entrainement" en cours d'année)
        """
        pos = []
        prj = []
        for k, p in self.projets.items():
            prj.append(k)
            pos.append(max(p.periode))

        return prj[pos.index(max(pos))]
    
    #############################################################################
    def getProjetDefaut(self):
        """ Renvoie l'épreuve de projet (évaluation)
            par défaut (pour les projets d'"entrainement" en cours d'année)
        """
        return self.projets[self.getCodeProjetDefaut()]
        
        
    #############################################################################
    def estPeriodeEval(self, position):
        pp = self.periode_prj
        return position+1 in range(pp[0], pp[1]+1)
    
    
    #########################################################################
    def getIntituleCompetence(self, comp, sousComp = False):
        sep = "\n\t"+constantes.CHAR_POINT
        competence = self.getCompetence_prj(comp)
        if sousComp and type(competence[1]) == dict:
            return sep.join([competence[0]] + [v for v in competence[1]])
        else:
            competence

    
        

    #########################################################################
    def getCompetence(self, comp):
#        print "getCompetence", comp
#        print "   ", self.dicCompetences
        if comp in self.dicCompetences.keys():
#            print "   1>>"
            return self.dicCompetences[comp]
        else:
            for k0, v0 in self.dicCompetences.items():
#                print "  ", k0, type(v0[1])
                if type(v0[1]) == dict:
                    if comp in v0[1].keys():
#                        print "   2>>"
                        return v0[1][comp]
                    else:
                        for k1, v1 in v0[1].items():
                            if type(v1[1]) == dict and comp in v1[1].keys():
#                                print "   3>>"
                                return v1[1][comp]

    

    
            
       
    
    #########################################################################
    def calculerLargeurCompetences(self, tailleReference):
        t = 1
        for k, v in self._dicIndicateurs_prj_simple.items():
            t = float(max(t, len(v)))
        r = t/5 # 5 = nombre max d'indicateurs à loger dans tailleReference
        return r*tailleReference


    #########################################################################
    def getSavoir(self, code, dic = None, c = 1, gene = None):
#        print "getSavoir", code, 
        if dic == None:
            if gene == "M":
                if self.tr_com != []:
                    dic = REFERENTIELS[self.tr_com[0]].dicSavoirs_Math
                else:
                    dic = self.dicSavoirs_Math
            elif gene == "P":
                if self.tr_com != []:
                    dic = REFERENTIELS[self.tr_com[0]].dicSavoirs_Phys
                else:
                    dic = self.dicSavoirs_Phys
            else:
                dic = self.dicSavoirs
#        print dic
        if dic.has_key(code):
            return dic[code][0]
        else:
            cd = ".".join(code.split(".")[:c])
            return self.getSavoir(code, dic[cd][1], c+1)


    #########################################################################
    def getLogo(self):
        if self._bmp == None:
            if self.CI_cible:
                self._bmp = constantes.images.Cible.GetBitmap()
            elif self.Code == "AC":
                self._bmp = constantes.images.ImageAC.GetBitmap()
            elif self.Code == "SIN":
                self._bmp = constantes.images.ImageSIN.GetBitmap()
            elif self.Code == "ITEC":
                self._bmp = constantes.images.ImageITEC.GetBitmap()
            elif self.Code == "EE":
                self._bmp = constantes.images.ImageEE.GetBitmap()
            elif self.Code == "SSI":
                self._bmp = constantes.images.SSI_ASR.GetBitmap()
            elif self.FichierLogo != r"":
                self._bmp = wx.Bitmap(os.path.join(constantes.PATH, r"..", DOSSIER_REF, self.FichierLogo))
#                try:
#                    self._bmp = wx.Bitmap(os.path.join(constantes.PATH, r"..", DOSSIER_REF, self.FichierLogo))
#                except:
#                    self._bmp = self._bmp = constantes.images.SSI_ASR.GetBitmap()
            else:
                self._bmp = constantes.images.SSI_ASR.GetBitmap()
        return self._bmp

    #########################################################################
    def getTypeEtab(self):
        if self.Famille in ["STI", "SSI", "STS"]:
            return 'L'  # Lycée
        else:
            return 'C'  # Collège

    
#    #########################################################################    
#    def getCompetence(self, code, dic = None, c = None):
#        """ Pour obtenir l'intitulé d'une compétence à partir de son code 
#                    fonction recursive
#        """
##        print "getCompetence", code, dic, c
#        if dic == None:
#            dic = self.dicCompetences
#            
#        if dic.has_key(code):
#            if type(dic[code]) == list:
#                return dic[code][0]
#            else:
#                return dic[code]
#            
#        else:
#            for c, v in dic.items():
#                if type(v) == list:
#                    co = self.getCompetence(code, v[1])
#                    if co != None:
#                        return co
#            return
                    
    
    
    
    #########################################################################    
    def findEffectif(self, lst, eff):
        continuer = True
        i = 0
        while continuer:
            if i > len(lst):
                continuer = False
            else:
                if lst[i][:2] == self.effectifs[eff][0][:2]:
                    continuer = False
                else:
                    i += 1 
        return i

#################################################################################################################################
#
#        Projet
#
#################################################################################################################################
class Projet(XMLelem):
    def __init__(self, code = "", intitule = u"", duree = 0, periode = [], importer = None):
        self._codeXML = "Projet"
        self.code = code
        self.intitule = intitule
        self.duree = duree
        self.periode = periode
        self.parties = {}
        
        
        #
        # grilles d'évaluation de projet
        #
        self.grilles = {}
        self.cellulesInfo = {}

        #
        # phases de projet
        #
        self.phases = {}
        self.listPhasesEval = []
        self.listPhases = []
        self.posRevues = {}
        
        
        #
        # Généralités sur le projet
        #
        self.ficheValid = r""
        self.attributs = {}
        
        
        if importer != None:
            self.importer(importer)



    ##################################################################################################################
    def __repr__(self):
        return self.code + " : " + self.intitule + u" (" + str(self.duree) + u"h)"


    #########################################################################
    def getNbrRevuesDefaut(self):
        return min(self.posRevues.keys())
    
    #########################################################################
    def getPosRevuesDefaut(self):
        return self.posRevues[self.getNbrRevuesDefaut()]
    
    #############################################################################
    def getPeriodeEval(self):
        return self.periode[0]-1
    
    #########################################################################
    def getIndicateur(self, codeIndic):
        if '_' in codeIndic:
            code, i = codeIndic.split('_')
            i = int(i)
            if code in self._dicIndicateurs_simple.keys():
                indics = self._dicIndicateurs_simple[code]
                if len(indics) >= i:
                    indic = indics[i-1]
                    return indic
        else:
            comp = self.getCompetence(codeIndic)
            if type(comp[1]) == dict:
                return self.getPremierEtDernierNiveauArbre(comp[1])
            else: 
                return comp[1]
            
    #########################################################################
    def getTypeIndicateur(self, codeIndic):
#        print "getTypeIndicateur", codeIndic, type(codeIndic)
        if type(codeIndic) == str:
            indic = self.getIndicateur(codeIndic)
        else:
            indic = codeIndic
        if indic != None:
            return indic.getType()
        
    
    #########################################################################
    def getCompetence(self, comp):
        if comp in self._dicCompetences.keys():
            return self._dicCompetences[comp]
        else:
            for k0, v0 in self._dicCompetences.items():
                if type(v0[1]) == dict:
                    if comp in v0[1].keys():
                        return v0[1][comp]
                    else:
                        for k1, v1 in v0[1].items():
                            if type(v1[1]) == dict and comp in v1[1].keys():
                                return v1[1][comp]


    ##################################################################################################################
    def importer(self, wb):
        for part in self.parties.keys():
            #
            # Grilles d'évaluation projet
            #
            sh_g = wb.sheet_by_name(u"Grille_"+self.code+"_"+part)
            for l in range(2,3):
#                print sh_g.cell(l,0).value
                if sh_g.cell(l,0).value != u"":
                    self.grilles[part] = [sh_g.cell(l,0).value, sh_g.cell(l,3).value]
#            print "self.grilles", self.grilles
            
            self.cellulesInfo[part] = {}
            for l in range(6, sh_g.nrows):
                k = str(sh_g.cell(l,0).value)
                if k != u"":                                                                  
                    i = [sh_g.cell(l,1).value, # Feuille
                         [int0(sh_g.cell(l,2).value), # Ligne
                          int0(sh_g.cell(l,3).value), # Colonne
                          int0(sh_g.cell(l,4).value)], #Période
                          sh_g.cell(l,5).value]  # Préfixe
                    if k in self.cellulesInfo[part].keys():
                        self.cellulesInfo[part][k].append(i)
                    else:
                        self.cellulesInfo[part][k] = [i]
            
        #
        # Phases du projet
        #
        shp = wb.sheet_by_name(u"Phase_"+self.code)
#            print self.Code
        for co in range(5, shp.ncols):
            if shp.cell(1,co).value != "":
#                    print "   ", shp.cell(1,co).value
                self.posRevues[int(shp.cell(1,co).value)] = []
        
        for l in range(2, shp.nrows):
            if shp.cell(l,0).value != u"":
                if shp.cell(l,1).value != u"":
                    self.phases[str(shp.cell(l,0).value)] = [shp.cell(l,1).value, shp.cell(l,2).value, shp.cell(l,3).value]
                    if shp.cell(l,4).value != "":
                        self.listPhasesEval.append(shp.cell(l,0).value)
                    self.listPhases.append(shp.cell(l,0).value)
                    for co in range(len(self.posRevues)):
                        if shp.cell(l,5+co).value != "":
                            self.posRevues[int(shp.cell(1,co+5).value)].append(shp.cell(l,0).value)
#                            if shp.cell(l,6).value != "":
#                                self.posRevues[3].append(shp.cell(l,0).value)
        
        
        #
        # Généralités sur le projet
        #         
        shp = wb.sheet_by_name(u"Généralités_"+self.code)
        if shp.nrows > 16:
            self.ficheValid = shp.cell(16,0).value
        for l in range(2, 13):
            self.attributs[str(shp.cell(l,0).value)] = [shp.cell(l,1).value, shp.cell(l,2).value, shp.cell(l,3).value]
                            



    ##################################################################################################################
    def postTraiter(self, ref):
#        print " postTraiter", self, ref
        
        
        
#        ###########################################################
#        def getArbreProjet(dic, debug = False):
#            sdic = {}
#            for k0, v0 in dic.items():
#                if debug: print k0
#                if len(v0) > 1 and type(v0[1]) == dict:
#                    if debug: print "   ", v0[0]
#                    if len(v0) == 2:
#                        sdic[k0] = [v0[0], getArbreProjet(v0[1], debug = debug)]
#                    else:
#                        if debug: print "   prem's", v0[2]
#                        
#                        if includeElem(self.parties.keys(), v0[2].keys()):
##                        if len(v0[2]) > 0 and not v0[2].keys() == ['E']:
##                        if v0[2][1] != 0 or v0[2][2] != 0: # Conduite ou Soutenance
#                            sdic[k0] = [v0[0], getArbreProjet(v0[1], debug = debug), v0[2]]
#                else:
#                    lst = []
#                    for l in v0[1]:
#                        if debug: print l[1]
#                        if l.estProjet(): # Conduite ou Soutenance
#                            lst.append(l)
#                    if lst != []:
#                        if len(v0) > 2:
#                            sdic[k0] = [v0[0], lst, v0[2]]
#                        else:
#                            sdic[k0] = [v0[0], lst]
#            return sdic
 
        
        
        
        
        ###########################################################
        def chercherIndicIdem(dic, debug = False):
            ii = None
            for k0, v0 in dic.items():
                if debug: print k0
                if len(v0) > 1 and type(v0[1]) == dict:
                    if debug: print "   ", v0[0]
                    ii = chercherIndicIdem(v0[1], debug = debug)
                    if debug: print "   ii", ii
                    if ii != None : return ii
                else:
                    lst = []
                    for l in v0[1]:
                        if isinstance(l, Indicateur) and "idem" in l.intitule:
                            if debug: print l.intitule
                            if debug: print "    idem"
                            codeindic = str(l.intitule.split(" ")[1])
                            return l, codeindic, k0
                    
            if ii != None:
                return ii
        
        ###########################################################
        def chercherDicIndic(dic, code, debug = False):
            if code in dic.keys():
                return dic
            else:
                for k0, v0 in dic.items():
                    if debug: print k0
                    if len(v0) > 1 and type(v0[1]) == dict:
                        if debug: print "   ", v0[0]
                        sdic = chercherDicIndic(v0[1], code, debug = debug)
                        if sdic != None : return sdic
            return
            
        
                                
                                
                                
        
#        print "dicCompetences", ref.dicCompetences
        self._dicCompetences = self.getArbreProjet(ref.dicCompetences, debug = False)
#        print "_dicCompetences", self._dicCompetences
        
        # On regroupe les compétences qui ont les mêmes indicateurs dans la grille (cas de STI2D EE !!)
        lst_codeindic = chercherIndicIdem(self._dicCompetences, debug = False)
#        print "lst_codeindic", lst_codeindic
        if type(lst_codeindic) == tuple:
            dic = chercherDicIndic(self._dicCompetences, lst_codeindic[2])
#            print "   >>", dic
            new_code = lst_codeindic[1]+"\n"+lst_codeindic[2]
            dic[new_code] = [dic[lst_codeindic[1]][0]+"\n"+dic[lst_codeindic[2]][0], dic[lst_codeindic[1]][1]]
            del dic[lst_codeindic[2]]
            del dic[lst_codeindic[1]]

        
        self._dicIndicateurs = ref.getPremierEtDernierNiveauArbre(self._dicCompetences)
        
        
        self.normaliserPoids(self._dicIndicateurs, debug = False)
#        print "                   ", self._dicIndicateurs_prj
        
        self._niveau = 0
        self._dicIndicateurs_famille = self.getDeuxiemeNiveauArbre(self._dicCompetences)

        self._dicIndicateurs_simple = self.getDernierNiveauArbre2(self._dicIndicateurs_famille)
#        print "_dicIndicateurs_prj_simple", self._dicIndicateurs_prj_simple
        
#        lst.extend()


    #########################################################################    
    def getClefDic(self, dicattr, nom, num = None):
        dic = getattr(self, dicattr)
        for k,v in dic.items():
            if num != None:
                v = v[num]
            if v == nom:
                return k
        return None

    ##################################################################################################################
    def completer(self, ref):
        """
        """
#        print " completer", ref, self
        
        ###########################################################
        def aplatir(dic, niv=1):
            ddic = {}
            for k0, v0 in dic.items():
                for k1, v1 in v0[1].items():
                    if type(v1) == list:
                        ddic[k1] = [v1[0]]
                        if type(v1[1]) == dict:
                            for i in sorted(v1[1].keys()):
                                ddic[k1].append(v1[1][i])
#                            ddic[k1].extend(v1[1].values())
                    else:
                        ddic[k1] = [v1]
            return ddic
        

        ###########################################################
        def getListeIndic(dic):
#            print "getListeIndic"
#            print dic
            
            if type(dic) == dict:
                l = []
                sdic = {}
                for k0, v0 in dic.items():
                    if type(v0) == dict:
                        sdic.update(getDernierNiveauArbre(v0))
                    else:
                        sdic[k0] = v0
                        
                for indics in sdic.values():
                    for indic in indics[1]:
                        l.append(indic)


#                l = [indics[1] for indics in sdic.values()]
            
            else:
                l = []
                for i, v0 in enumerate(dic):
                    l.append(v0)
                    
#            print "  >>>", l
            return l
            
            
        ###########################################################
        def getDernierNiveauArbre(dic):
            sdic = {}
            for k0, v0 in dic.items():
                if len(v0) > 1 and  type(v0[1]) == dict:
                    sdic.update(getDernierNiveauArbre(v0[1]))
                else:
                    sdic[k0] = v0
            return sdic
        
        
        #
        # Ajout des compétences du tronc commun
        #
        if ref.tr_com != []:
            t = ref.tr_com[0]
#            print "   ++", t, REFERENTIELS.keys()
            if t in REFERENTIELS.keys():
#                print "         ",REFERENTIELS[t]._dicCompetences
                self._dicCompetences.update(REFERENTIELS[t]._dicCompetences)
                self._dicIndicateurs.update(REFERENTIELS[t]._dicIndicateurs)
                self._dicIndicateurs_simple.update(REFERENTIELS[t]._dicIndicateurs_simple)
        

        self._lstGrpIndicateur = {}
        for p in self.parties.keys():
            self._lstGrpIndicateur[p] = []

        for comp, dic in self._dicIndicateurs.items():
            for indic in getListeIndic(dic[1]):
                for part in indic.poids.keys():
                    if part in self._lstGrpIndicateur.keys():
                        self._lstGrpIndicateur[part].append(comp)

        for p in self.parties.keys():
            self._lstGrpIndicateur[p] = list(set(self._lstGrpIndicateur[p]))

    
#        if ref.tr_com != []:
#            self.grilles.update(REFERENTIELS[ref.tr_com[0]].projets[self.code].grilles)
                
                


#################################################################################################################################
#
#        Indicateur
#
#################################################################################################################################
class Indicateur(XMLelem):
    def __init__(self, intitule = u"", poids = {}, ligne = {}, revue = {}):
        self._codeXML = "Indicateur"
        self.poids = poids
        self.ligne = ligne
        self.intitule = intitule
        self.revue = revue

    def estProjet(self):
        return self.getType() != 'E'
#        return self.poids[1] != 0 or self.poids[2] != 0
    
    def getType(self):
        """ E : écrit
            C : conduite
            S : soutenance
            ...
        """
        for t, p in self.poids.items():
            if p !=0:
                return t
        
#        if self.poids[0] != 0:
#            return "E"
#        elif self.poids[1] != 0:
#            return "C"
#        elif self.poids[2] != 0:
#            return "S"

    def getRevue(self):
        return 'R'+str(self.revue[self.getType()])

#################################################################################################################################
#
#        Compétence
#
#################################################################################################################################
class Competence(XMLelem):
    def __init__(self, intitule = u"", indicateurs = []):
        self._codeXML = "Competence"
        self.intitule = intitule
        self.indicateurs = indicateurs







#########################################################################################
def getEnseignementLabel(label):
    """ Renvoie le code et la famille d'enseignement
        à partir de son label
    """
    for r in REFERENTIELS.values():
        if r.Enseignement[0] == label:
            return r.Code, r.Famille



##########################################################################################
def enregistrer(code, nomFichier):

    fichier = file(nomFichier, 'w')
    root = REFERENTIELS[code].getBranche()
    constantes.indent(root)
    ET.ElementTree(root).write(fichier)
    fichier.close()
    
#enregistrer("SSI", "testSauvRef.xml")


##########################################################################################
def ouvrir(nomFichier):
    fichier = open(nomFichier,'r')
    root = ET.parse(fichier).getroot()
    ref = Referentiel()
    ref.initParam()
    err = ref.setBranche(root)[1]
    ref.corrigerVersion(err)
    ref.postTraiter()
    ref.completer()
    fichier.close()
    return ref
    
#    print REFERENTIELS["SSI"] == ref
    
#ouvrir("testSauvRef.xml")


##########################################################################################
SAUVEGARDE = False


##########################################################################################
def chargerReferentiels():
    global REFERENTIELS, ARBRE_REF
    
    #
    # Chargement des fichiers .xls
    #
    liste = os.listdir(os.path.join(constantes.PATH, r"..", DOSSIER_REF))
    
    for fich_ref in liste:#["Ref_STS-SN_EC-1.xls", "Ref_SSI.xls"]:#, "Ref_STI2D-EE.xls", "Ref_STI2D-ETT.xls"]:#["Ref_6CLG.xls"]:#
        
        if os.path.splitext(fich_ref)[1] == ".xls":
#            print
#            print fich_ref
            ref = Referentiel(os.path.join(constantes.PATH, r"..", DOSSIER_REF, fich_ref))
            ref.postTraiter()
            REFERENTIELS[ref.Code] = ref
            

    for r in REFERENTIELS.values():
#        print r
        r.completer()
#        if r.Code == "ITEC":
#        print r
    

    #
    # Vérification intégrité en comparant avec le fichier .xml (s'il existe)
    #
    if not SAUVEGARDE:
        dicOk = {}
        for k, r in REFERENTIELS.items():
            f = os.path.join(constantes.PATH, r"..", DOSSIER_REF, "Ref_"+r.Enseignement[0]+".xml")
            dicOk[k] = False
            if os.path.exists(f):
                ref = ouvrir(f)
#                for p in ref.projets.values():
#                    print p.grilles
                if ref == r:
                    dicOk[k] = True
            else:
                enregistrer(r.Code, f)
                dicOk[k] = None
                
        print u"Intégrité référentiels :", dicOk
    
    #
    # Construction de la structure en arbre
    #
    
    #  Types d'enseignement qui n'ont pas de tronc commun (parents)
    for k, r in REFERENTIELS.items():
        if r.tr_com == []:
            ARBRE_REF[k] = []
    
    #  Types d'enseignement qui ont un tronc commun (enfants)
    d = []
    for k, r in REFERENTIELS.items():
        if r.tr_com != []:
            ARBRE_REF[r.tr_com[0]].append(k)
            d.append(r.tr_com[0])
    
    for k, r in REFERENTIELS.items():
        if "_"+r.Famille in ARBRE_REF.keys():
            ARBRE_REF["_"+r.Famille].append(k)
        else:
            ARBRE_REF["_"+r.Famille] = [k]
    
    for k, r in ARBRE_REF.items():
        if k[0] == "_":
            if len(r) == 1:
                del ARBRE_REF[k]
                
    for k, r in ARBRE_REF.items():
        if k[0] == "_":
            for kk in ARBRE_REF.keys():
                if kk in r:
                    if ARBRE_REF[kk] == []:
                        del ARBRE_REF[kk]
                    else:
                        del ARBRE_REF[k]
                        break
        r.sort()
        r.reverse()
#    print ARBRE_REF
    
    
chargerReferentiels()

def sauvegarderOriginaux():
    global SAUVEGARDE
    SAUVEGARDE = True
    for r in REFERENTIELS.values():
        f = os.path.join(constantes.PATH, r"..", DOSSIER_REF, "Ref_"+r.Enseignement[0]+".xml")
        enregistrer(r.Code, f)
        
#
# Ligne à décommenter pour faire une sauvegarde XML des référentiels "originaux"
#   Commenter en parallèle la partie "Vérification" de chargerReferentiels()
#
#sauvegarderOriginaux()







