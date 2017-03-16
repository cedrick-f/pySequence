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

from version import __version__, sup

# Pour enregistrer en xml
import xml.etree.ElementTree as ET
Element = type(ET.Element(None))

import util_path
#########################################################################################
DOSSIER_REF = os.path.join(util_path.PATH, u"..", u"referentiels")
REFERENTIELS = {}
ARBRE_REF = {}

########################################################################################
#
#    Quelques constantes
#
########################################################################################
ACTIVITES = ["AP", "ED", "P"]
PERIODES = ['Pri', 'Sec', 'Sup']


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
#        print "getBranche", self._codeXML, self
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
            elif type(val) == list or type(val) == tuple:
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
#        print "setBranche", self._codeXML, self
    
        nomerr = []
        
        def lect(branche, nom = ""):
            if nom[:2] == "S_":
                return unicode(branche.get(nom)).replace(u"--", u"\n")
            
            elif nom[:2] == "I_":
                if branche.get(nom) == None: # Pour passage 6.0-beta19 à beta20
                    nomerr.append(nom)
                    return 0
                return int(branche.get(nom))
            
            elif nom[:2] == "L_":
                return long(branche.get(nom))
            
            elif nom[:2] == "F_":
                return float(branche.get(nom))
            
            elif nom[:2] == "B_":
#                print nom
                if branche.get(nom) == None: # Pour corriger un bug (version <=5.0beta3)
                    print u"Pas trouvé", nom, self._codeXML
                    nomerr.append(nom)
                    return False 
                return branche.get(nom)[0] == "T"
            
            elif nom[:2] == "l_":
                sbranche = branche.find(nom)
                if sbranche == None: return []
                dic = {}
                
                # éléments "simples" : dans les items
                for k, sb in sbranche.items():
#                     _k = k[2:]
                    _k = k.split("_")[-1]
                    if isinstance(_k, (str, unicode)) and "--" in _k:
                        _k = _k.replace("--", "\n")
                    dic[_k] = lect(sbranche, k)
                
                
                
                # éléments plus complexes : comme sous-élément
                for sb in list(sbranche):
                    k = sb.tag
#                     _k = k[2:]
                    _k = k.split("_")[-1]
                    if isinstance(_k, (str, unicode)) and "--" in _k:
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
                indic, err = Indicateur().setBranche(sbranche)
                nomerr.extend(err)
                return indic
            
            elif nom.split("_")[0] == "Projet":
                sbranche = branche.find(nom)
                proj, err = Projet(self).setBranche(sbranche)
                nomerr.extend(err)
                return proj
            
            elif nom.split("_")[0] == "Savoirs":
                sbranche = branche.find(nom)
                sav, err = Savoirs().setBranche(sbranche)
                nomerr.extend(err)
                return sav
            
            elif nom.split("_")[0] == "Competences":
                sbranche = branche.find(nom)
                comp, err = Competences().setBranche(sbranche)
                nomerr.extend(err)
                return comp
            
            elif nom.split("_")[0] == "Competence":
                sbranche = branche.find(nom)
                comp, err = Competence().setBranche(sbranche)
                nomerr.extend(err)
                return comp
            
            

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
            if isinstance(val1, (str, unicode)) and isinstance(val2, (str, unicode)):
#                if val1 != val2:#.replace("\n", "--"):
#                    print "Erreur str : xml =", val1, "      xls =", val2#.replace("\n", "--")
                return val1 == val2#.replace("\n", "--")
            
            elif type(val1) == bool and type(val2) == bool:
#                if val1 != val2:
#                    print "Erreur bool: xml =", val1, "      xls =", val2
                return val1 == val2
            
            elif isinstance(val1, (int, long, float)) and isinstance(val2, (int, long, float)):
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
                return all([egal(v, val2[k]) for k, v in val1.items()])
                
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
                if isinstance(val1, (str, unicode, int, long, float, bool, list, dict, XMLelem)) :
                    val2 = getattr(ref, attr)
                    if not egal(val1, val2):
#                         print u"Différence", ""
#                         print "  ", attr
#                         print "  xml:", val1
#                         print "  xls:", val2
                        break
                        return False
        return True



    ###########################################################
    def normaliserPoids(self, dic, debug = False):
        for k0, competence in dic.items():
            if competence.poids != {}:
    #                    print self.parties.keys()
                tot = {}
                for p in self.parties.keys():
                    tot[p] = 0
                    
                if competence.sousComp != {} :
                    lstindic = []
                    for v1 in competence.sousComp.values():
                        for ii in v1.indicateurs:
                            lstindic.append(ii)
                else:
                    lstindic = competence.indicateurs
                    
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
        for k0, competence in dic.items():
            if competence.sousComp != {}:
                if competence.poids != {}: # premier niveau = [intitule, dict ou liste, poids]
                    sdic[k0] = competence.copie()
                    sdic[k0].sousComp = self.getDernierNiveauArbre(competence.sousComp)
#                     sdic[k0] = [v0[0], self.getDernierNiveauArbre(competence.sousComp), v0[2]]
                else:
                    sdic.update(self.getDernierNiveauArbre(competence.sousComp))
            else:
                sdic[k0] = competence.copie()
                
        return sdic
    
    
    ###########################################################
    def getArbreProjet(self, dic, prj = None, debug = False):
#        print "getArbreProjet", self.parties.keys()
        sdic = {}
        for k0, v0 in dic.items():
            if debug: print k0
            competence = v0
#             print k0, v0
            if competence.sousComp != {}:
#             if len(v0) > 1 and type(v0[1]) == dict:
                if debug: print "   ", competence
                if competence.poids == {}:
#                 if len(v0) == 2:
                    sdic[k0] = competence.copie()
                    sdic[k0].sousComp = self.getArbreProjet(competence.sousComp, prj = prj,  debug = debug)
#                     sdic[k0] = [competence, self.getArbreProjet(competence.sousComp, prj = prj,  debug = debug)]
                else:
                    if debug: print "   prem's", competence.poids
                    
                    if includeElem(self.parties.keys(), competence.poids.keys()):
#                        if len(v0[2]) > 0 and not v0[2].keys() == ['E']:
#                        if v0[2][1] != 0 or v0[2][2] != 0: # Conduite ou Soutenance
                        sdic[k0] = competence.copie()
                        sdic[k0].sousComp = self.getArbreProjet(competence.sousComp, prj = prj,  debug = debug)
#                         sdic[k0] = [competence, self.getArbreProjet(competence.sousComp, prj = prj, debug = debug)]
            
            elif competence.indicateurs != []:
                lst = []
                for l in competence.indicateurs:
                    if debug: print l, l.getType(), l.poids, l.estProjet(), prj
#                    print v0
                    if l.estProjet(): # Conduite ou Soutenance
                        if prj == None or len([p for p in l.poids.keys() if p in prj.parties.keys()]) > 0:#or l.getType() in prj.parties.keys():
#                        if l.getType() == v0[2].keys():
                            lst.append(l)
                
                
                if lst != []:
                    sdic[k0] = competence.copie()
                    sdic[k0].indicateurs = lst 
#                     sdic[k0] = [competence, lst]
#                     if competence.poids is not None:
# #                     if len(v0) > 2:
#                         sdic[k0] = [v0[0], lst, v0[2]]
#                     else:
#                         sdic[k0] = [v0[0], lst]
        return sdic
    
    
    
#     ###########################################################
#     def getArbre(self, dic, prj = None, debug = False):
# #        print "getArbreProjet", self.parties.keys()
#         sdic = {}
#         for k0, v0 in dic.items():
#             if debug: print k0
#             if len(v0) > 1 and type(v0[1]) == dict:
#                 if debug: print "   ", v0
#                 if len(v0) == 2:
#                     sdic[k0] = [v0[0], self.getArbreProjet(v0[1], prj = prj,  debug = debug)]
#                 else:
#                     if debug: print "   prem's", v0[2]
#                     
#                     if includeElem(self.parties.keys(), v0[2].keys()):
# #                        if len(v0[2]) > 0 and not v0[2].keys() == ['E']:
# #                        if v0[2][1] != 0 or v0[2][2] != 0: # Conduite ou Soutenance
#                         sdic[k0] = [v0[0], self.getArbreProjet(v0[1], prj = prj, debug = debug), v0[2]]
#             else:
#                 lst = []
#                 for l in v0[1]:
#                     if debug: print l, l.getType(), l.poids, l.estProjet(), prj
# #                    print v0
#                     if l.estProjet(): # Conduite ou Soutenance
#                         if prj == None or len([p for p in l.poids.keys() if p in prj.parties.keys()]) > 0:#or l.getType() in prj.parties.keys():
# #                        if l.getType() == v0[2].keys():
#                             lst.append(l)
#                 if lst != []:
#                     if len(v0) > 2:
#                         sdic[k0] = [v0[0], lst, v0[2]]
#                     else:
#                         sdic[k0] = [v0[0], lst]
#         return sdic
#     
    
    
    
    
    ###########################################################
    def getDernierNiveauArbre2(self, dic):
        """ Renvoie un dictionnaire de listes d'Indicateurs
        """
        sdic = {}
        for k0, competence in dic.items():
            if competence.sousComp != {}:
                sdic.update(self.getDernierNiveauArbre2(competence.sousComp))
            else:
                sdic[k0] = competence.indicateurs
        return sdic
    
    
    ###########################################################
    def getDeuxiemeNiveauArbre(self, dic):
        sdic = {}
#            if len(dic) > 0 and type(dic.values()[0][1]) == dict:
        for k0, competence in dic.items():
            if competence.sousComp != {}:
                for k1, sousComp in competence.sousComp.items():
                    if sousComp.sousComp != {} : # pas fini = 3ème niveau
                        self._niveau = 3
                        sdic[k1] = sousComp.copie()
                        sdic[k1].sousComp = sousComp.sousComp
#                         sdic[k1]
# #                         sdic[k1] = {}
#                         for k2, v2 in sousComp.sousComp.items():
# #                             sdic[k1][k2]
#                             sdic[k1][k2] = v2.copie()
                    else:   # Niveau "indicateur"
                        self._niveau = 2
                        sdic[k1] = sousComp.copie()
#                         sdic[k1].indicateurs = sousComp.sousComp
            else:
                sdic[k0] = competence.copie()
#                 sdic[k0].indicateurs = competence.indicateurs
#            else:
#                return dic
        return sdic


    ###########################################################
    def getDernierNiveauArbre(self, dic):
        dicIndic = {}
        for k0, competence in dic.items():
            if competence.sousComp != {}:
                dicIndic.update(self.getDernierNiveauArbre(competence.sousComp))
            else:
                dicIndic[k0] = competence
        
        
        return dicIndic
        
        
#         sdic = {}
#         for k0, competence in dic.items():
#             if competence.sousComp != {}:
#                 sdic.update(self.getDernierNiveauArbre(competence.sousComp))
#             else:
#                 sdic[k0] = competence
#         return sdic
    
#################################################################################################################################
#
#        Référentiel
#
#################################################################################################################################
class Referentiel(XMLelem):
    
    def __init__(self, nomFichier = u""):
        # Enseignement       Famille,    Nom    , Nom complet
        
        self._codeXML = "Referentiel"
        self.initParam()
        self._bmp = None
        
        if nomFichier != u"":
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
        self.Enseignement = [u""    ,   u"",    u"", u""]
        self.options = {}               # options de l'enseignement : {Code : nomFichier}
        self.tr_com = []                # tronc commun de l'enseignement : [Code, nomFichier]
        self.AnneeDebut = ""            # Position de l'enseignement dans la scolarité (PERIODE+Année)
        
        self.periodes = []              # découpage de l'enseignement en années/périodes
        self.FichierLogo = u""          # Fichier désignant l'image du Logo de l'enseignement
        
        
        #
        # Projets "obligatoires" (au BO)
        #
        self.projets = {}
        self.aColNon = {}               # Pour indiquer si les différentes parties d'un projet ont une colonne "NON" dans leur grille
        self.compImposees = {}          # Indique que les competences sont imposées pour chaque revue
        self.parties = {}
        
        #
        # Domaines
        #
        self.nomDom = u"Domaine(s)"
        self.domaines = {}
        self.listeDomaines = []
        
        
        #
        # Thématiques
        #
        self.nomTh = u"Thématique(s)"
        self.thematiques = {}
        self.listeThematiques = []
        
        #
        # Labels (
        #
        self.labels = {}
        
        
        #
        # Centre d'intérêt
        #
        self.nomCI = u"Centre(s) d'intérêt"
        self.abrevCI = u"CI"
        self.CentresInterets = []           #
        self.CI_BO = True                   # les ci sont donnés par le B.O. (pas modifiables)
        self.CI_cible = False               # les ci se placent sur une cible MEI FSC
        self.positions_CI = []              # positions sur la cible MEI FSC
        self.listProblematiques = []        # problématiques (associées à un CI)
        self.nomPb = u"Problématique(s)"    # nom pour désigner les problématiques
        self.abrevPb = "Pb"
        self.maxCI = 0                   # Nombre maxi de CI (0 = réglable)
        
        #
        # Savoirs ou capacités
        #
#        self.nomSavoirs = u"Savoirs"    # nom donnés aux savoirs : "Savoirs", "Capacités", ...
#        self.surnomSavoirs = u""
        self.listSavoirs = []
        self.dicoSavoirs = {}

        #
        # Compétences
        #
#        self.nomCompetences = u"Compétences"    # nom donnés aux compétences : "Compétences", ...
#        self.nomIndicateurs = u"Indicateurs de performance" 
        self.listCompetences = []
        self.dicoCompetences = {}
        
        
#        self.dicCompetences_prj = {}
#        self.dicIndicateurs_prj = {}
#        self.dicPoidsIndicateurs_prj = {}
#        self.dicLignesIndicateurs_prj = {}

        #
        # Fonctions/Tâches
        #
        self.nomFonctions = u"Fonction(s)"    # nom donnés aux Fonctions : "Fonctions", ...
        self.nomTaches = u"Tâche(s)"          # nom donnés aux Tâches : "Tâches", ...
        self.dicFonctions = {}
        
        
        #
        # Pratique pédagogiques
        #
        self.demarches = {}
        self.listeDemarches = []
        
        self.seances = {}
        self.listeTypeSeance = []
        
        self.activites = {}
        self.listeTypeActivite = []
        
        self.horsClasse = {}
        self.listeTypeHorsClasse = []
                
        self.demarcheSeance = {}
    
    
        #
        # Effectifs
        #
        self.effectifs = {}
        self.listeEffectifs = []
        self.effectifsSeance = {} #{"" : []}
        
        
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
        """ Correction d'erreur de lecture de la branche XML
            pour cause de changement de version
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
        
        for p in self.projets.values():
#            print p.listeParties, p.parties
            if len(p.listeParties) <> len(p.parties):
                p.listeParties = p.parties.keys()
            p.corrigerVersion(nomerr, self.Code)
#            print p.listeParties, p.parties
        
        
        if "S_AnneeDebut" in nomerr:
            if self.Famille == "STS":
                self.AnneeDebut = "Sup1"
            elif self.Famille == "2nde":
                self.AnneeDebut = "Sec5"
            elif self.Famille == "STI" or self.Famille == "SSI":
                self.AnneeDebut = "Sec6"
            elif self.Famille == "CLG":
                self.AnneeDebut = "Sec1"
            print "Correction AnneeDebut:", self.AnneeDebut
        
        
        for k, v in REFERENTIELS[self.Code].labels.items():  # à partir de 7.0-beta12
            if not k in self.labels.keys():
                self.labels[k] = v
        
        
        # à partir de 7.1
#         print self.nomDom
        if self.nomDom == "None":
            self.nomDom = u"Domaine(s)"
            
            
        
        def corriger(dic):
            sdic = {}
            for k0, v0 in dic.items():
                sdic[k0] = Competence(v0[0])
                if len(v0) > 1 and type(v0[1]) == dict:
                    
                    sdic[k0].sousComp = corriger(v0[1])
                    if len(v0) > 2:
                        sdic[k0].poids = v0[2]

                else:
                    sdic[k0].indicateurs = v0[1]
            return sdic

        itemComp = self.dicoCompetences.items()
        for code, comp in itemComp: #
            dic = self.dicoCompetences[code]
            if len(dic.dicCompetences) > 0 and not isinstance(dic.dicCompetences.values()[0], Competence):
#                 print "Corriger compétences"
#                 print "  ", self.dicoCompetences[code].dicCompetences
                self.dicoCompetences[code].dicCompetences = corriger(self.dicoCompetences[code].dicCompetences)
#                 print ">>", self.dicoCompetences[code].dicCompetences


            # à partir de la version 7.1-beta.4
            if 'B_obj' in nomerr:
                comp.obj = True
        
    
        
        
        return
        
    
    
    
                    
    ######################################################################################  
    def importer(self, nomFichier):
        """ Procédure d'import de Référentiel depuis un fichier Excel
        """
        
#        print "IMPORTER" , 
        self.initParam()

        
        ###########################################################
        def remplir(sh, col, rng, mode = 1, condition = None, debug = False, niveau = 0):
            """ Mode = 1 : on finit par une liste
                Mode = 2 : on finit par un dict
            """
            if debug: print "  "*niveau+"remplir : col="+chr(65+col), "lignes=",[n+1 for n in rng]
            if rng == [] and mode == 2:
                return None
#            self.prof_Comp = max(self.prof_Comp, col)
            lig = [l  for l in rng if sh.cell(l,col).value != u""]
            if debug: print "  "*niveau+">> branches :", [n+1 for n in lig]
            
            if lig == rng:
                if debug: print "  "*niveau+"FIN"
                if mode == 1:
                    if  col+1 >= sh.ncols or (len(lig)>0 and sh.cell(lig[0],col+1).value) == u"":
                        return [sh.cell(l,col).value for l in lig]
                    else:
                        d = {}
                        for l in lig:
                            if condition == None or sh.cell(l,4).value == condition:
                                if debug: print "  "*niveau+str(sh.cell(l,col).value)
                                d[str(sh.cell(l,col).value)] = [sh.cell(l,col+1).value, []]
                        return d
                        
                else:
#                    if condition == None or sh.cell(l,4).value == condition:
                    d = {}
                    for l in lig:
                        if condition == None or sh.cell(l,4).value == condition:
                            if debug: print "  "*niveau+str(sh.cell(l,col).value)
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
                    if debug: print "  "*niveau+"-> ", i, [n+1 for n in lig], [n+1 for n in llig]
                    sdic = remplir(sh, col+1, range(p+1, llig[i+1]), mode = mode, condition = condition, debug = debug, niveau = niveau+1)
                    if sdic != None:
                        if debug: print "  "*niveau+"+++"+str(sh.cell(p,col).value)
                        dic[str(sh.cell(p,col).value)] = [sh.cell(p,col+1).value, sdic]
                return dic
          
        
            


        
        ###########################################################
        def getArbreFonc(sh, rng, col, prems = False, debug = False):
            """ Construit la structure en arbre :
                    utilisé pour les Fonctions
                (fonction récursive)
                
                <rng> : liste des lignes
                <col> : numéro de la colonne traitée (=0 au lancement)
                <prems> : racine de l'arbre (=True au lancement)
                <fonction> : cas spécifique du traitement des Fonctions
            """
            dic = {}
            
            ci = 8 # colonne "I" des indicateurs (cas des Compétences uniquement)
            
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

                    dic[code] = [intitule, getArbreFonc(sh, ssRng, col+1, debug = debug)]
                    lstComp = [sh.cell(1,co).value for co in range(5, sh.ncols) if sh.cell(l,co).value != u""]
#                        print "   lstComp1 =", lstComp
                    dic[code].append(lstComp)
                        

                # Il n'y a plus d'item à droite => Indicateur()
                else:
                    dic[code] = [intitule, []]
                    for ll in [l] + ssRng:
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
        
        
        ###########################################################
        def getbgcoul(wb, sh, l, c):
            xfx = sh.cell_xf_index(l, c)
            xf = wb.xf_list[xfx]
            bgx = xf.background.pattern_colour_index
            color_map = wb.colour_map[bgx]
#             if color_map and (color_map[0] != 255 or color_map[1] != 255 or color_map[2] != 255):
#                 print "coul", bgx
#                 print "coul", color_map
#             else:
                
#             print "coul", bgx
#             print "map", color_map
            if color_map is None:
                return (0,0,0)
            else:
                return color_map
        
        #
        # Ouverture fichier EXCEL
        #
        wb = open_workbook(nomFichier, formatting_info = True)
#        sh = wb.sheets()
        
        #
        # Généralités ##############################################################################
        #
        sh_g = wb.sheet_by_name(u"Généralités")
        self.Famille = sh_g.cell(2,0).value
        self.Code = sh_g.cell(2,1).value
        self.AnneeDebut = sh_g.cell(2,2).value
        self.Enseignement[0] = sh_g.cell(6,0).value # Abréviation    
        self.Enseignement[1] = sh_g.cell(6,1).value # Nom complet    
        self.Enseignement[2] = sh_g.cell(6,2).value # Famille : abréviation
        self.Enseignement[3] = sh_g.cell(6,3).value # Famille : Nom complet
        debug = False#self.Code == "STS_SN_EC"

        if sh_g.ncols > 3:
            lig = [l  for l in range(10, 17) if sh_g.cell(l,3).value != u""]
            for l in lig:
                self.periodes.append([sh_g.cell(l,2).value, int(sh_g.cell(l,3).value)])
            
        self.FichierLogo = sh_g.cell(19,1).value
        
        
        #
        # Projets
        #
        col = [c  for c in range(1, sh_g.ncols) if sh_g.cell(24,c).value != u""]
        for c in col:
            self.projets[sh_g.cell(25,c).value] = Projet(self, sh_g.cell(25,c).value,           # Code
                                                         intitule = sh_g.cell(24,c).value,      # Nom
                                                         duree = int0(sh_g.cell(26,c).value),   # Durée
                                                         periode = [int(i) for i in sh_g.cell(27,c).value.split()])     # Période
        if debug: print "  projets :", self.projets
        
        #
        # options
        #
        
        lig = [l  for l in range(10, 17) if sh_g.cell(l,0).value != u""]
        for l in lig:
            self.options[str(sh_g.cell(l,0).value)] = sh_g.cell(l,1).value
        
        #
        # tronc commun
        #
        if sh_g.cell(21,0).value != u"":
            self.tr_com = [sh_g.cell(21,0).value, sh_g.cell(21,1).value]
           


        #
        # Bulletins Officiels
        #
        Pligne = 30 # Numéro de ligne du titre "BO"
      
#        print self.Code, sh_g.nrows
        self.BO_dossier = [sh_g.cell(l,0).value for l in range(Pligne+1, sh_g.nrows) if sh_g.cell(l,0).value != u""]
        self.BO_URL = [[sh_g.cell(l,1).value, sh_g.cell(l,2).value] for l in range(Pligne+2, sh_g.nrows) if sh_g.cell(l,1).value != u""]



        #
        # Labels #############################################################################
        #
        if u"Labels" in wb.sheet_names():
            sh_lb = wb.sheet_by_name(u"Labels")
            for l in range(2, sh_lb.nrows):
                if sh_lb.cell(l,0).value != u"":
                    self.labels[str(sh_lb.cell(l,0).value)] = [sh_lb.cell(l,1).value, sh_lb.cell(l,2).value]


            
        #
        # CI  #################################################################################
        #
        sh_ci = wb.sheet_by_name(u"CI")
        self.CI_BO = sh_ci.cell(0,1).value[0].upper() == "O"
        self.CI_cible = sh_ci.cell(1,1).value[0].upper() == "O"
        self.nomCI = sh_ci.cell(2,0).value
        self.abrevCI = sh_ci.cell(2,1).value
        try:
            self.maxCI = int(sh_ci.cell(3,1).value)
        except:
            self.maxCI = 0
#         print "maxCI", self.maxCI
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
        # Problématiques #########################################################################
        #
        shnt = u"Pb"
        if shnt in [s.name for s in wb.sheets()]:
            self.listProblematiques = [[] for ci in self.CentresInterets]
            shp = wb.sheet_by_name(shnt)
            self.nomPb = shp.cell(0,0).value
            self.abrevPb = sh_ci.cell(0,1).value
            for l in range(2, shp.nrows) :
                self.listProblematiques[int(shp.cell(l,1).value)-1].append(shp.cell(l,0).value)
#            print "listProblematiques", self.listProblematiques
        
        
        
        
        
        
        #
        # Savoirs  ##############################################################################
        #
        for n in wb.sheet_names():
            if n[:4] == "Sav_":
                sh_sa = wb.sheet_by_name(n)
                code = n[4]
                self.dicoSavoirs[code] = Savoirs(sh_sa.cell(0,0).value, sh_sa.cell(2,0).value, sh_sa.cell(2,2).value, sh_sa.cell(2,1).value)
                self.dicoSavoirs[code].dicSavoirs = remplir(sh_sa, 0, range(4, sh_sa.nrows))
                self.dicoSavoirs[code].obj = 'O' in sh_sa.cell(0,5).value
                self.dicoSavoirs[code].pre = 'P' in sh_sa.cell(0,5).value
                self.listSavoirs.append(code)



            
        #
        # Compétences  ###############################################################################
        #
        debug = False#self.Code == "ITEC"
        
        
        lst_feuilles_codes = [(wb.sheet_by_name(n), n[5]) for n in wb.sheet_names() if n[:5] == "Comp_"]
        for sh_co, code in lst_feuilles_codes:
            self.dicoCompetences[code] = Competences(sh_co.cell(0,0).value,     # Nom générique ("Compétence", ...)
                                                     sh_co.cell(2,0).value,     # Code discipline "enseignant"
                                                     sh_co.cell(2,2).value,     # Code discipline "enseignement"
                                                     sh_co.cell(2,1).value,     # Nom discipline
                                                     sh_co.cell(0,8).value)     # Nom générique indicateur ("Indicateur de performance", ...)
            
            self.listCompetences.append(code)
            if debug:
                print "____", code, "obj:", self.dicoCompetences[code].obj, "pre:", self.dicoCompetences[code].pre
            
            #
            # Décomposition des projets en parties
            #    colonne de départ : 11 (colonne "L")
            #
            if code == "S": # Page principale des compétences = définition du découpage "projet"
                self._colParties = []
                col = [c  for c in range(11, sh_co.ncols) if sh_co.cell(1,c).value != u""]
                if debug: print ">>>", col
                
                for i, c in enumerate(col):
                    if i == len(col)-1:
                        n = sh_co.ncols
                    else:
                        n = col[i+1]
                    
                    for j in range((n-c)/3):
                        cp = c+j*3
                        part = str(sh_co.cell(3,cp).value)
                        self._colParties.append((part, cp))
                        t = sh_co.cell(1,c).value
                        for p in self.projets.values():
                            if t == p.intitule:
                                p.listeParties.append(part)
                                p.parties[part] = sh_co.cell(2,cp).value
                        self.compImposees[part] = False # Valeur par défaut
                
                if debug: print "colParties", self._colParties
                for part, col in list(set([cp for cp in self._colParties])):
                    self.parties[part] = sh_co.cell(2,col).value
                    
                for p in self.projets.values():
        #            print "  importer", self, p
                    p.importer(wb)
        
        
        # On fini l'importation après la création de tous les objets Competences
        # car références croisées
        for sh_co, code in lst_feuilles_codes:
            self.dicoCompetences[code].importer(sh_co, self, debug = debug)

                
                    
                


        #
        # Fonctions  ######################################################################################
        #
        if u"Fonctions" in wb.sheet_names():
            sh_va = wb.sheet_by_name(u"Fonctions")
            self.nomFonctions =   sh_va.cell(0,0).value
            self.nomTaches = sh_va.cell(0,5).value
            self.dicFonctions = getArbreFonc(sh_va, range(2, sh_va.nrows), 0, prems = True, debug = False)
#            print "dicFonctions", self.dicFonctions


        #
        # Domaines  ########################################################################################
        #
        sh_g = wb.sheet_by_name(u"Dom")
        self.nomDom = sh_g.cell(0,0).value
        for l in range(2, sh_g.nrows):
            code = str(sh_g.cell(l,0).value)
            
            if code == "":
                l += 3
                break
            if sh_g.cell(l,1).value != u"":
                self.domaines[code] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value, 
                                       sh_g.cell(l,3).value, getbgcoul(wb, sh_g, l, 4)]
                self.listeDomaines.append(code)
        
        
        #
        # Thématiques  ########################################################################################
        #
        sh_g = wb.sheet_by_name(u"Th")
        self.nomTh = sh_g.cell(0,0).value
        for l in range(2, sh_g.nrows):
            code = str(sh_g.cell(l,0).value)
            if code == "":
                l += 3
                break
            if sh_g.cell(l,1).value != u"":
                self.thematiques[code] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value, 
                                          sh_g.cell(l,3).value, getbgcoul(wb, sh_g, l, 4)]
                self.listeThematiques.append(code)
                
                
        #
        # Séances  ########################################################################################
        #
        sh_g = wb.sheet_by_name(u"Séance")
        
        # Démarches
        for l in range(2, sh_g.nrows):
            code = str(sh_g.cell(l,0).value)
            if code == "":
                l += 3
                break
            if sh_g.cell(l,1).value != u"":
                self.demarches[code] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value, 
                                        sh_g.cell(l,3).value, getbgcoul(wb, sh_g, l, 4)]
                self.listeDemarches.append(code)


        # Activités
        for l in range(l, sh_g.nrows):
            code = str(sh_g.cell(l,0).value)
            if code == "":
                l += 3
                break
            if sh_g.cell(l,1).value != u"":
                self.activites[code] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value,
                                        sh_g.cell(l,3).value, getbgcoul(wb, sh_g, l, 4)]
                self.listeTypeActivite.append(code)
                self.demarcheSeance[code] = sh_g.cell(l,6).value.split()
                self.effectifsSeance[code] = sh_g.cell(l,5).value.split()
                
        self.seances.update(self.activites)
        
        # Hors classe
        for l in range(l, sh_g.nrows):
            code = str(sh_g.cell(l,0).value)
            if code == "":
                l += 3
                break
            if sh_g.cell(l,1).value != u"":
                self.horsClasse[code] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value,
                                         sh_g.cell(l,3).value, getbgcoul(wb, sh_g, l, 4)]
                self.listeTypeHorsClasse.append(code)
        self.seances.update(self.horsClasse)
                
        # Autres Séances
        self.listeTypeSeance = self.listeTypeActivite[:] + self.listeTypeHorsClasse[:]
        for l in range(l, sh_g.nrows):
            code = str(sh_g.cell(l,0).value)
            if code == "":
                l += 3
                break
            if sh_g.cell(l,1).value != u"":
                self.seances[code] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value,
                                      sh_g.cell(l,3).value, getbgcoul(wb, sh_g, l, 4)]
                self.listeTypeSeance.append(code)
                self.effectifsSeance[code] = sh_g.cell(l,5).value.split()
                
        # Effectifs
        for l in range(l, sh_g.nrows):
            code = str(sh_g.cell(l,0).value)
            if code == "":
                l += 3
                break
            if sh_g.cell(l,0).value != u"":
                self.effectifs[code] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value,
                                        sh_g.cell(l,3).value, getbgcoul(wb, sh_g, l, 4)]
                self.listeEffectifs.append(code)






        
        
        
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


    
    
    
    #########################################################################
    def postTraiter(self):
        """ Complète les données selon que le référentiel ait un tronc commun ou des options
            
            --> le "_" évite que les attributs ne soient sauvegardés dans les XML
        """
        for p in self.projets.values():
            p.postTraiter(self)
                    

        
        
    #########################################################################
    def completer(self, forcer = False):
        """ Complète les données selon que le référentiel ait un tronc commun ou des options
            Exécuté lorsque tous les référentiels sont chargés !
            
            --> le "_" évite que les attributs ne soient sauvegardés dans les XML
        """
        
        debug = False#self.Code == "SSI"
        if debug: print "completer", self.Code, self.tr_com

        # C'est une option (il y a un tronc commun) ==> on complète plus tard
        if not forcer and len(self.tr_com) != 0:
            return
        
#        print "completer ref :", self, self.options

        itemComp = self.dicoCompetences.items()

        self._listesCompetences_simple = {}  # format : [[code compétence, intitulé compétence, [ sous compétences ]]]
        
#        print "ref", self
        for code, comp in itemComp:
#            print "   comp", code
            dic = self.getPremierEtDernierNiveauArbre(self.dicoCompetences[code].dicCompetences)
            liste = []
#            print "    dic", dic
            for k1, competence in dic.items():
#                print "      h1", h1
                liste.append([k1, competence.intitule, []])
                if competence.sousComp != {}:
                    for k2, sousComp in competence.sousComp.items(): 
                        liste[-1][2].append([k2, sousComp.intitule])
                    liste[-1][2].sort()
                    
            liste.sort()
            self._listesCompetences_simple[code] = liste
#        print "self._listesCompetences_simple", self._listesCompetences_simple['S']
#            self._dicoCompetences_simple[code] = self.getDernierNiveauArbre(self.dicoCompetences[code].dicCompetences)
#            for comp, value in self._dicoCompetences_simple[code].items():
#                self._dicoCompetences_simple[code][comp] = self._dicoCompetences_simple[code][comp][0]
        
        
        
        if len(self.options) != 0:
            self.parties = {}
            for ro in self.options.keys():
                for proj in REFERENTIELS[ro].projets.values():
                    for part, n in proj.parties.items():
                        if not part in self.parties.keys():
                            self.parties[part] = n
                
            if debug: print "    ", self.parties
            
            self._dicoCompetences = {}
            self._dicoIndicateurs = {}
            self._dicoIndicateurs_famille = {}
            self._dicoIndicateurs_simple = {}
            
            
            
            if self.tr_com != []:
                ref_tc = REFERENTIELS[self.tr_com[0]]
                itemComp.insert(1, ("B", ref_tc.dicoCompetences["S"]))
            
            for code, comp in itemComp:
                
                self._dicoCompetences[code] = self.getArbreProjet(self.dicoCompetences[code].dicCompetences, debug = debug)
                if debug:
                    print self._dicoCompetences[code]
                
#                print "self.dicoCompetences[code].dicCompetences", self.dicoCompetences[code].dicCompetences
                
#                print "_dicoCompetences_simple", code, self._dicoCompetences_simple[code]
                
                self._dicoIndicateurs[code] = self.getPremierEtDernierNiveauArbre(self._dicoCompetences[code])
                
                self.normaliserPoids(self._dicoIndicateurs[code], debug = False)
        #        print "                   ", self._dicIndicateurs_prj
                
                self._niveau = 0
                self._dicoIndicateurs_famille[code] = self.getDeuxiemeNiveauArbre(self._dicoCompetences[code])
        
                self._dicoIndicateurs_simple[code] = self.getDernierNiveauArbre2(self._dicoIndicateurs_famille[code])
        
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
        """ Renvoie le nombre de périodes  du Référentiel.
        """
        n = 0
        for p in self.periodes:
            n += p[1]
        return n


    #############################################################################
    def getPeriodeEval(self, codePrj):
        return self.projets[codePrj].getPeriodeEval()


    #############################################################################
    def getPeriodesListe(self):
        l = []
        for p in self.periodes:
            l.extend([p[0]]*p[1])
        return l
            
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
            pos.append(max(p.periode, 0))
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
    def getCompetence(self, code):
        if code[0] == "B" and self.tr_com != []: # Compétence de tronc commun
            r = REFERENTIELS[self.tr_com[0]]
            return r.dicoCompetences["S"].getCompetence(code[1:])
        else:
            return self.dicoCompetences[code[0]].getCompetence(code[1:])

#        for disc, comp in self.dicoCompetences.items():
#            cc = comp.getCompetence(comp)
#            if cc is not None:
#                return cc
           
    #########################################################################
    def getCompetenceEtGroupe(self, comp):
        return self.dicoCompetences[comp[0]].getCompetenceEtGroupe(comp[1:])
    
    
    #########################################################################
    def getTousSavoirs(self):
        """ Renvoie sous la forme [(code, Referentiel.Savoirs), ]
            tous les savoirs concernés par cet enseignement
        """
        dicSavoirs = [(c, self.dicoSavoirs[c]) for c in self.listSavoirs]
        if self.tr_com != []:
            # Il y a un tronc comun (ETT pour Spécialité STI2D par exemple)
            r = REFERENTIELS[self.tr_com[0]]
            dicSavoirs.insert(1, ("B", r.dicoSavoirs["S"]))
            dicSavoirs.extend([(c, r.dicoSavoirs[c]) for c in r.dicoSavoirs.keys() if c != "S"])
            
        return dicSavoirs
    
    #########################################################################
    def getToutesCompetences(self):
        """ Renvoie sous la forme [(code, Referentiel.Competences), ]
            toutes les competences concernés par cet enseignement
        """
        lstComp = [(c, self.dicoCompetences[c]) for c in self.listCompetences]
        if self.tr_com != []:
            # Il y a un tronc comun (ETT pour Spécialité STI2D par exemple)
            r = REFERENTIELS[self.tr_com[0]]
            lstComp.insert(1, ("B", r.dicoCompetences["S"]))
            lstComp.extend([(c, r.dicoCompetences[c]) for c in r.dicoCompetences.keys() if c != "S"])
            
        return lstComp
    
    #########################################################################
    def getDicTousSavoirs(self):
        """ Renvoie sous la forme {code : Referentiel.Savoirs), ...}
            tous les savoirs concernés par cet enseignement
        """
        dicSavoirs = {c : self.dicoSavoirs[c] for c in self.listSavoirs}
        if self.tr_com != []:
            # Il y a un tronc comun (ETT pour Spécialité STI2D par exemple)
            r = REFERENTIELS[self.tr_com[0]]
            dicSavoirs.update({"B": r.dicoSavoirs["S"]})
            dicSavoirs.update({c : r.dicoSavoirs[c] for c in r.dicoSavoirs.keys() if c != "S"})
             
        return dicSavoirs
    
    
    #########################################################################
    def getDicToutesCompetences(self):
        """ Renvoie sous la forme {code : Referentiel.Competences), ...}
            toutes les competences concernés par cet enseignement
        """
        dicComp = {c : self.dicoCompetences[c] for c in self.listCompetences}
        if self.tr_com != []:
            # Il y a un tronc comun (ETT pour Spécialité STI2D par exemple)
            r = REFERENTIELS[self.tr_com[0]]
            dicComp.update({"B": r.dicoCompetences["S"]})
            dicComp.update({c : r.dicoCompetences[c] for c in r.dicoCompetences.keys() if c != "S"})
             
        return dicComp
    
    
#     #########################################################################
#     def getSavoirs(self, code):
#         """ Renvoie sous la forme [(code, Referentiel.Savoirs), ]
#             tous les savoirs concernés par cet enseignement
#         """
#         if code in self.listSavoirs.keys():
#             return self.listSavoirs[code]
#         elif self.tr_com != []:
#             r = REFERENTIELS[self.tr_com[0]]
#             if code in 
#             
#         
#         if self.tr_com != []:
#             # Il y a un tronc comun (ETT pour Spécialité STI2D par exemple)
#             
#             dicSavoirs.insert(1, ("B", r.dicoSavoirs["S"]))
#             dicSavoirs.extend([(c, r.dicoSavoirs[c]) for c in r.dicoSavoirs.keys() if c != "S"])
#             
#         return savoirs
            
#    #########################################################################
#    def getCompetence(self, comp):
##        print "getCompetence", comp
##        print "   ", self.dicCompetences
#        if comp in self.dicCompetences.keys():
##            print "   1>>"
#            return self.dicCompetences[comp]
#        else:
#            for k0, v0 in self.dicCompetences.items():
##                print "  ", k0, type(v0[1])
#                if type(v0[1]) == dict:
#                    if comp in v0[1].keys():
##                        print "   2>>"
#                        return v0[1][comp]
#                    else:
#                        for k1, v1 in v0[1].items():
#                            if type(v1[1]) == dict and comp in v1[1].keys():
##                                print "   3>>"
#                                return v1[1][comp]

    

    
            
       
    
    #########################################################################
    def calculerLargeurCompetences(self, tailleReference):
        t = 1
        for k, v in self._dicIndicateurs_prj_simple.items():
            t = float(max(t, len(v)))
        r = t/5 # 5 = nombre max d'indicateurs à loger dans tailleReference
        return r*tailleReference


    #########################################################################
    def getDependant(self, elem, contexte):
        """ Vérifie si l'élément <elem> (Compétences, Savoir, Thématique, Domaine)
            est dépendant d'un autre dans le même <contexte>
            
            Renvoi l'élément dont il dépend ou None
        """
#         print "getDependant", contexte, "---", elem
#         listeTousElem = self.dicoCompetences + self.dicoSavoirs
#         if isinstance(elem, Competences):
        for code, comp in self.dicoCompetences.items():
#                 print "  :::", code, comp.asso_type
            if comp != elem and elem in comp.asso_type:
                i = comp.asso_type.index(elem)
                if contexte in comp.asso_contexte[i]:
#                     print "  >>", i, code, comp
                    return i, code, comp
        
#         print "Aucun"
        return
    
    
    #########################################################################
    def getSousSavoirs(self, code):
#         print "getSousSavoirs", code
        for codeDiscipline, savoirs in self.getTousSavoirs():
#             print "   ", codeDiscipline, savoirs
            if codeDiscipline == code[0]:
                return savoirs.getSousSavoirs(code[1:]) 
    
    
    #########################################################################
    def getSavoir(self, code):
        """ Renvoie un savoir d'après son code
        """
        
        for codeDiscipline, savoirs in self.getTousSavoirs():
            if codeDiscipline == code[0]:
                return savoirs.getSavoir(code[1:])
#         return self.dicoSavoirs[code[0]].getSavoir(code[1:])
    
##        print "getSavoir", code, 
#        if dic == None:
#            
#            
#            
#            if gene == "M":
#                if self.tr_com != []:
#                    dic = REFERENTIELS[self.tr_com[0]].dicSavoirs_Math
#                else:
#                    dic = self.dicSavoirs_Math
#            elif gene == "P":
#                if self.tr_com != []:
#                    dic = REFERENTIELS[self.tr_com[0]].dicSavoirs_Phys
#                else:
#                    dic = self.dicSavoirs_Phys
#            else:
#                dic = self.dicSavoirs
##        print dic
#        if dic.has_key(code):
#            return dic[code][0]
#        else:
#            cd = ".".join(code.split(".")[:c])
#            return self.getSavoir(code, dic[cd][1], c+1)


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
            elif self.FichierLogo != u"":
                self._bmp = wx.Bitmap(os.path.join(DOSSIER_REF, util_path.toFileEncoding(self.FichierLogo)))
#                try:
#                    self._bmp = wx.Bitmap(os.path.join(constantes.PATH, r"..", DOSSIER_REF, self.FichierLogo))
#                except:
#                    self._bmp = self._bmp = constantes.images.SSI_ASR.GetBitmap()
            else:
                self._bmp = constantes.images.SSI_ASR.GetBitmap()
        return self._bmp

    #########################################################################
    def getTypeEtab(self):
        if self.Famille in ["STI", "SSI", "STS", "2nde", "ISN"]:
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
#        print "findEffectif", lst, eff
        continuer = True
        i = 0
        while continuer:
            if i >= len(lst):
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
    def __init__(self, parent, code = "", intitule = u"", duree = 0, periode = [], importer = None):
        self._codeXML = "Projet"
        self._parent = parent # un référentiel
        self.code = code
        self.intitule = intitule
        self.duree = duree
        self.periode = periode  # une liste [début, fin] ou [debut-fin] ou [] en unité "période" de Référentiel
        self.parties = {}       # Le dictionnaire des parties (code, nom)
        self.listeParties = []  # La liste ordonnée des parties
        
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
        # tâches du projet (si imposées)
        #
        self.taches = {}
        self.listTaches = []
        self.tachesOnce = False # Pour indiquer que chaque tâche ne peut apparaitre qu'une seulle fois dans me projet
        
        #
        # Effectifs
        #
        self.maxEleves = 5
        self.minEleves = 3
        self.maxGroupes = 3
        
        #
        # Généralités sur le projet
        #
        self.ficheValid = u""
        self.attributs = {}
        
        
        if importer != None:
            self.importer(importer)



    ##################################################################################################################
    def __repr__(self):
        return "Prj_ :"+str(self.GetPosition()[0])+" > "+str(self.GetPosition()[-1]-self.GetPosition()[0])

#         return self.code + " : " + self.intitule + u" (" + str(self.duree) + u"h)"
    
    
    ######################################################################################  
    def __lt__(self, doc):
        if self.GetPosition()[0] == doc.GetPosition()[0]:
            return self.GetPosition()[-1]-self.GetPosition()[0] < doc.GetPosition()[-1]-doc.GetPosition()[0]
        else:
            return self.GetPosition()[0] < doc.GetPosition()[0]
        
        
    ##################################################################################################################
    def GetPosition(self):
        return self.periode
    
    
    ######################################################################################
    def corrigerVersion(self, nomerr, codeRef):
        """ Correction d'erreur de lecture de la branche XML
            pour cause de changement de version
        """
#        print "corrigerVersion", nomerr
        if "I_maxEleves" in nomerr:
            self.maxEleves = 5
        if "I_minEleves" in nomerr:
            self.minEleves = 3
            
        # A partir de la version 6.2 => nouvel attribut "Aide
#        print "Corriger", self.attributs
        for k, l in self.attributs.items():
            if len(l) == 3:
#                print "Corriger", k, l
                l.append(REFERENTIELS[codeRef].projets[self.code].attributs[k][3])
                if k == "DEC":
                    l[1] = REFERENTIELS[codeRef].projets[self.code].attributs[k][1]
#                print "  >>", l
        
        if not "FIC" in self.attributs.keys():
            self.attributs["FIC"] = [u"", u"", u"", u""]
        


    #########################################################################
    def getNbrRevuesDefaut(self):
        return min(self.posRevues.keys())
    
    #########################################################################
    def getPosRevuesDefaut(self):
        return self.posRevues[self.getNbrRevuesDefaut()]
    
    #############################################################################
    def getNbrPeriodes(self):
        """ Renvoie la durée (en nombre de périodes "référentiel") du projet.
        """
        if len(self.periode) >0 :
            return self.periode[-1] - self.periode[0] + 1
        return 1
        
    #############################################################################
    def getPeriodeEval(self):
        if len(self.periode) > 0:
            return [self.periode[0]-1, self.periode[-1]-1]
        return None
    
    #############################################################################
    def getPeriodeDefaut(self):
        p = self.getPeriodeEval()
        if p is None:
            return [0, 0]
        return p
    
    #########################################################################
    def getIndicateur(self, codeIndic):
#         print "getIndicateur", codeIndic
        
        disc, cod = codeIndic[0], codeIndic[1:]
#         print self._dicoIndicateurs_simple[disc]
        
        if '_' in cod:
            code, i = cod.split('_')
            i = int(i)
            if code in self._dicoIndicateurs_simple[disc].keys():
                indics = self._dicoIndicateurs_simple[disc][code]
                if len(indics) >= i:
                    indic = indics[i-1]
                    return indic
        else:
            comp = self.getCompetence(disc, cod)
            if comp.sousComp != {}: #type(comp[1]) == dict:
                return self.getPremierEtDernierNiveauArbre(comp.sousComp)
            else: 
                return comp.indicateurs
            
    #########################################################################
    def getTypeIndicateur(self, codeIndic):
#        print "getTypeIndicateur", codeIndic, type(codeIndic)
        if type(codeIndic) in [str, unicode]:
            indic = self.getIndicateur(codeIndic)
        else:
            indic = codeIndic
        if indic != None:
            return indic.getType()
        
    
    #########################################################################
    def getCompetence(self, disc, comp):
#         print "getCompetence", comp
        
#        competences = self._parent._dicoCompetences[disc]
#        return competences.getCompetence(comp)
        
        def getComp(dic):
#             print "   ", dic
            if comp in dic.keys():
                return dic[comp]
            else:
                for k, competence in dic.items():
                    c = getComp(competence.sousComp)
                    if c is not None: 
#                         print "   ", k, "!!!!!"
                        return c

        return getComp(self._dicoCompetences[disc])
         
        
#         if comp in dic.keys():
#             return dic[comp]
#         else:
#             for k, sousComp in dic.items():
#                 c = self.
#             
#             
#             
#             for k0, v0 in self._dicoCompetences[disc].items():
#                 if v0.sousComp != {}: #type(v0[1]) == dict:
#                     if comp in v0.sousComp.keys():
#                         return v0.sousComp[comp]
#                     else:
#                         for k1, v1 in v0.sousComp.items():
#                             if v1.sousComp != {}:
#                                 return v1.sousComp[comp]


        
    ##################################################################################################################
    def importer(self, wb):
#        print "importer", self.parties.keys()
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
        # Taches du projet (si imposées)
        #
        shnt = u"Taches_"+self.code
        if shnt in [s.name for s in wb.sheets()]:
            shp = wb.sheet_by_name(shnt)
            for l in range(2, shp.nrows) :
                if len(shp.cell(l,3).value) > 0 : # On ne prend que les tâches concernées par le projet
                    self.listTaches.append(str(shp.cell(l,0).value))
                    self.taches[str(shp.cell(l,0).value)] = [shp.cell(l,2).value, 
                                                             shp.cell(l,1).value, 
                                                             shp.cell(l,3).value.split()]
            self.tachesOnce = shp.cell(0,4).value[0].upper() == "O"
#            print self.tachesOnce
        
        #
        # Généralités sur le projet
        #         
        shp = wb.sheet_by_name(u"Généralités_"+self.code)
        if shp.nrows > 16:
            self.ficheValid = shp.cell(18,0).value
        for l in range(2, 15):
            try:
                aide = shp.cell(l,4).value
            except:
                aide = u""
            self.attributs[str(shp.cell(l,0).value)] = [shp.cell(l,1).value, 
                                                        shp.cell(l,2).value, 
                                                        shp.cell(l,3).value, 
                                                        aide]
                           



    ##################################################################################################################
    def postTraiter(self, ref):
        debug = False #ref.Code == "EE-CIT-SI-DIT"
#        if self._parent.Code == "EE-SI":
        if debug: print "postTraiter",  ref, self, self.parties
        
        
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
            for k0, competence in dic.items():
                if debug: print k0
                if competence.sousComp != {}:
                    if debug: print "   ", competence
                    ii = chercherIndicIdem(competence.sousComp, debug = debug)
                    if debug: print "   ii", ii
                    if ii != None : return ii
                else:
                    lst = []
                    for l in competence.indicateurs:
                        if isinstance(l, Indicateur) and "idem" in l.intitule:
                            if debug: print l.intitule
                            if debug: print "    idem"
                            codeindic = str(l.intitule.split(" ")[1])
                            return l, codeindic, k0
                    
            if ii != None:
                return ii
        
        ###########################################################
        def chercherDicIndic(dic, code, debug = False):
            """ Renvoie le dictionnaire de compétences qui contient le <code>
            """
            if code in dic.keys():
                return dic
            else:
                for k0, competence in dic.items():
                    if debug: print k0
                    if competence.sousComp != {}:
                        if debug: print "   ", competence
                        sdic = chercherDicIndic(competence.sousComp, code, debug = debug)
                        if sdic != None : return sdic
            return
            
        
                                
                                
       
                        
#        print "dicCompetences ref", ref.dicCompetences
        self._dicoCompetences = {}
        self._dicoIndicateurs = {}
        self._dicoIndicateurs_famille = {}
        self._dicoIndicateurs_simple = {}
#        self._dicoCompetences_simple = {}
        
        itemComp = ref.dicoCompetences.items()
#        if ref.tr_com != []:
#            ref_tc = REFERENTIELS[ref.tr_com[0]]
#            itemComp.insert(1, ("B", ref_tc.dicoCompetences["S"]))
        
        for code, comp in itemComp:
            if debug: print code,
            if debug: 
                print "    ", comp.dicCompetences   
                for typi, dico in comp.dicCompetences.items():
                    print "  typi", typi, " poids :", dico.poids
            self._dicoCompetences[code] = self.getArbreProjet(comp.dicCompetences, self, debug = False)
            
            
#            self._dicoCompetences_simple[code] = self.getDernierNiveauArbre(self.dicoCompetences[code].dicCompetences)
#            for comp, value in self._dicoCompetences_simple[code].items():
#                self._dicoCompetences_simple[code][comp] = self._dicoCompetences_simple[code][comp][0]
                    
                    
#            if self._parent.Code == "EE-SI": 
#                print "+++", self
#                print "   ", code, self._dicoCompetences
                
                
            if debug: 
                print "   >", self._dicoCompetences[code]
                
    #        print ">> _dicCompetences prj", self._dicCompetences
            
            # On regroupe les compétences qui ont les mêmes indicateurs dans la grille (cas de STI2D EE !!)
            lst_codeindic = chercherIndicIdem(self._dicoCompetences[code], debug = False)
            if type(lst_codeindic) == tuple:
                if debug: print "    lst_codeindic", lst_codeindic
                
                dic = chercherDicIndic(self._dicoCompetences[code], lst_codeindic[2])
                
                newCompetence = dic[lst_codeindic[2]].copie()
                newCompetence.intitule = dic[lst_codeindic[1]].intitule+"\n"+dic[lst_codeindic[2]].intitule
                newCompetence.sousComp = dic[lst_codeindic[2]].sousComp
                
    #            print "   >>", dic
#                 new_code = lst_codeindic[1]+"\n"+lst_codeindic[2]
#                 dic[new_code] = [dic[lst_codeindic[1]].intitule+"\n"+dic[lst_codeindic[2]].intitule, dic[lst_codeindic[1]][1]]
                
                del dic[lst_codeindic[2]]
                del dic[lst_codeindic[1]]
    
            
            self._dicoIndicateurs[code] = ref.getPremierEtDernierNiveauArbre(self._dicoCompetences[code])
            
            if debug:
                print self._dicoIndicateurs[code]
                for typi, dico in self._dicoIndicateurs.items():
                    for grp, grpComp in dico.items():
                        print "  poids :", grpComp.poids
                        
            self.normaliserPoids(self._dicoIndicateurs[code], debug = False)
    #        print "                   ", self._dicIndicateurs_prj
            
            
            self._niveau = 0
            self._dicoIndicateurs_famille[code] = self.getDeuxiemeNiveauArbre(self._dicoCompetences[code])
            if debug:
                print self._dicoIndicateurs_famille[code]
            
            self._dicoIndicateurs_simple[code] = self.getDernierNiveauArbre2(self._dicoIndicateurs_famille[code])
            
            
            
            if debug:
                print self._dicoIndicateurs_simple[code]
    #        print "_dicIndicateurs_prj_simple", self._dicIndicateurs_prj_simple
        
        
        #
        # Post-traitement des tâches (si prédéterminées)
        #
        
        # On ne prend que les tâches concernées par le projet
        for t in self.taches.values():
            l = []
            for code in ref.dicoCompetences.keys():
                l.extend(self._dicoCompetences[code].keys())
            t[2] = [cc for cc in t[2] if cc in l]
            
        # On trie par phase
        lt = []
        for p in self.listPhases:
            for t in self.listTaches:
                if self.taches[t][0] == p:
                    lt.append(t)
        self.listTaches = lt
                    
                    
        #
        #
        #
        if self.attributs["FIC"][0] == u"":
            self.attributs["FIC"][0] = u"Fiche de lots de travaux" # Noms des "fiches de lots de travaux" ou "tâches détaillées"

#        lst.extend()


    #########################################################################    
    def getClefDic(self, dicattr, nom, num = None):
        """ Renvoie la clef associée à une valeur dans un dictionnaire
            num est utilisé pour rechercher avec le numiemme élément d'une valeur de type liste
        """
        dic = getattr(self, dicattr)
        for k,v in dic.items():
            if num != None:
                v = v[num]
            if v == nom:
                return k
        return None

    ##################################################################################################################
    def completer(self, ref):
        """ Complète le projet
        """
#        if self._parent.Code == "EE-SI":
#            print "completer", ref, self
#            print "     ", self._dicoCompetences
            
        
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
        def getListeIndic(competence):
#            print "getListeIndic"
#            print dic
            l = competence.indicateurs
            if competence.sousComp != {}:
                for sousComp in competence.sousComp.values():
                    l.extend(getListeIndic(sousComp))
            return l
            
            
#             
#             if competence.sousComp != {}:
#                 l = []
#                 sdic = {}
#                 for k0, sousComp in competence.sousComp.items():
#                     if sousComp.sousComp != {}:
#                         sdic.update(getDernierNiveauArbre(sousComp))
#                     else:
#                         sdic[k0] = v0
#                         
#                 for indics in sdic.values():
#                     for indic in indics[1]:
#                         l.append(indic)
# 
# 
# #                l = [indics[1] for indics in sdic.values()]
#             
#             else:
#                 l.extend(competence.indicateurs)
# #                 l = []
# #                 for i, v0 in enumerate(dic):
# #                     l.append(v0)
#                     
# #            print "  >>>", l
#             return l
            
            
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
        self._dicoGrpIndicateur = {}
        for code, comp in self._dicoCompetences.items():
            if ref.tr_com != []:
                t = ref.tr_com[0]
    #            print "   ++", t, REFERENTIELS.keys()
                if t in REFERENTIELS.keys():
    #                print "         ",REFERENTIELS[t]._dicCompetences
    #                print "       ++", self._dicCompetences
                    self._dicoCompetences[code].update(REFERENTIELS[t]._dicoCompetences["S"])
                    self._dicoIndicateurs[code].update(REFERENTIELS[t]._dicoIndicateurs["S"])
                    self._dicoIndicateurs_simple[code].update(REFERENTIELS[t]._dicoIndicateurs_simple["S"])
            
    
            self._dicoGrpIndicateur[code] = {}
            for p in self.parties.keys():
                self._dicoGrpIndicateur[code][p] = []
    
            for comp, competence in self._dicoIndicateurs[code].items():
                for indic in getListeIndic(competence):
                    for part in indic.poids.keys():
                        if part in self._dicoGrpIndicateur[code].keys():
                            self._dicoGrpIndicateur[code][part].append(comp)
    
            for p in self.parties.keys():
                self._dicoGrpIndicateur[code][p] = list(set(self._dicoGrpIndicateur[code][p]))

#        if self._parent.Code == "EE-SI":
#            print "     ", self._dicoCompetences
#            print
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
        self.revue = revue          # Revue à laquelle cet indicateur doit être évalué (si imposé par le référentiel) - 0 = pas imposé

    def estProjet(self):
        return self.getType() != 'E'
#        return self.poids[1] != 0 or self.poids[2] != 0
    
    def getTypes(self):
        """ Renvoie la liste de toutes les parties de projet concernées par l'indicateur
        
        """
        return [t for t, p in self.poids.items() if p !=0]
    
    def getType(self):
        """ E : écrit
            C : conduite
            S : soutenance
            Sinon : None
            
            E, C ou S doit être exclusif !!
        """
        types = [t for t, p in self.poids.items() if p !=0 and t in ['E', 'C', 'S']]
        if len(types) > 0:
            return types[0]
        
#        for t, p in self.poids.items():
#            if p !=0:
#                return t
        
#        if self.poids[0] != 0:
#            return "E"
#        elif self.poids[1] != 0:
#            return "C"
#        elif self.poids[2] != 0:
#            return "S"

    
    def getRevue(self):
#        print self.getTypes(), self.revue
        return 'R'+str(self.revue[self.getTypes()[0]])


#################################################################################################################################
#
#        Compétence
#
#################################################################################################################################
class Competence(XMLelem):
    def __init__(self, intitule = u"", poids = {}):
        self._codeXML = "Competence"
        self.intitule = intitule
        self.domaines = []              # liste de codes de domaines
        self.thematiques = []           # liste de codes de thematiques
        self.poids = poids
        self.indicateurs = []           # liste de codes d'indicateurs
        self.sousComp = {}              # {code : Referentiel.Competences}
        self.elemAssocies = [[],[]]     # Liste des codes des éléments (sav, th, dom, ...) associées
        self.infos = []                 # des informations supplémentaires (str)

    def __repr__(self):
        return "Competence : " + self.intitule[:10] + "...\n   " #+ "\n   ".join(self.thematiques)
    
    def copie(self):
        c = Competence(self.intitule, self.poids)
        c.domaines = self.domaines[:]
        c.thematiques = self.thematiques[:]
        c.indicateurs = self.indicateurs[:]
        c.infos = self.infos[:]
        for i in range(len(self.elemAssocies)):
            c.elemAssocies[i] = self.elemAssocies[i][:]
        
        return c



#################################################################################################################################
#
#        Compétences (toutes)
#
#################################################################################################################################
class Competences(XMLelem):
    def __init__(self, nomGenerique = u"Compétences", codeDiscipline = "", nomDiscipline = u"", abrDiscipline = u"", 
                 nomGeneriqueIndic = u"Indicateurs de performance"):
        self._codeXML = "Competences"
        self.nomGenerique = nomGenerique
        self.codeDiscipline = codeDiscipline
        self.nomDiscipline = nomDiscipline          # Nom discipline
        self.abrDiscipline = abrDiscipline          # Abréviation discipline
        self.nomGeneriqueIndic = nomGeneriqueIndic
        self.dicCompetences = {}        # Dictionnaire de Compétences (arborescence)
        self.obj = self.pre = True
        
        self.asso_type = []     # liste (2 éléments !) de type d'éléments associés aux compétences
                                # peut être : Savoirs, Competence, liste de Th ou de Dom
        self.asso_contexte = []
        


#     #########################################################################
#     def __repr__(self):
#         competences = u"\n".join([c.__repr__() for c in self.dicCompetences.values()])
#         return "Referentiel.Competences"# + competences# str(self.obj)+str(self.pre)
    

    
    #########################################################################
    def importer(self, feuille, ref, debug = False):
        
        ###########################################################
        def getArbreComp(sh, rng, col, prems = False, debug = False):
            """ Construit la structure en arbre :
                    utilisé pour les Compétences
                (fonction récursive)
                
                <rng> : liste des lignes
                <col> : numéro de la colonne traitée (=0 au lancement)
                <prems> : racine de l'arbre (=True au lancement)
                <fonction> : cas spécifique du traitement des Fonctions
            """
            dic = {}
            
            ci = 8 # colonne "I" des indicateurs (cas des Compétences uniquement)
            
            # Liste des lignes comportant un code dans la colonne <col>, dans l'intervalle <rng>
            lstLig = [l  for l in rng if sh.cell(l,col).value != u""]
            if debug: print "  **",lstLig
            
            for i, l in enumerate(lstLig):
                code = str(sh.cell(l,col).value)
                intitule = unicode(sh.cell(l,col+1).value)
                competence = Competence(intitule)
                dic[code] = competence
                if len(self.asso_type) > 0: # Il y a des éléments associés à ces compétences
                    competence.elemAssocies[0] = sh.cell(l,5).value.split()
                    
                if debug: print "-> ",l, code, intitule
                
                # Toutes les lignes entre chaque code
                if i < len(lstLig)-1:
                    ssRng = range(l+1, lstLig[i+1])
                else:
                    ssRng = range(l+1, rng[-1]+1)
                if debug: print "   ", ssRng
        
                # Il y a encore des items à droite ... 
                if len(ssRng) > 0 and col < 2 and [li  for li in ssRng if sh.cell(li,col+1).value != u""] != []:
                    # Il y a une(des) nouvelle(s) branche(s) (code + intitulé)
                    if [li  for li in ssRng if sh.cell(li,col+2).value != u""] != []:
                        competence.sousComp = getArbreComp(sh, ssRng, col+1, debug = debug)
                    
                    # Il y a un(des) info(s) seulement
                    elif [li  for li in ssRng if sh.cell(li,col+1).value != u""] != []:
                        competence.infos = [sh.cell(li,col+1).value  for li in ssRng]
                    
                    
                    
        
                # Il n'y a plus d'item à droite => Indicateur()
                else:
                    for ll in [l] + ssRng:
                        indic = unicode(sh.cell(ll,ci).value)
        
                        poids = {}
                        lignes = {}
                        revues = {}
                        for p, c in ref._colParties:
                            v = int0(sh.cell(ll,c).value)                   # Colonne code partie projet
                            if v > 0:
                                poids[p] = v
                                lignes[p] = int0(sh.cell(ll,c+1).value)     # Colonne "l"
                                revues[p] = int0(sh.cell(ll,c+2).value)     # Colonne "r"
                                if lignes[p] != 0:
                                    ref.aColNon[p] = True
                                if revues[p] != 0:
                                    ref.compImposees[p] = True
        
                        if indic != u"":
                            competence.indicateurs.append(Indicateur(indic, poids, lignes, revues))
        
                if prems:
                    if debug:
                        print "prems", 
                    poids = {}
                    for p, c in ref._colParties:
                        if debug: print p, c, "--", 
                        v = int0(sh.cell(l,c).value)
                        if debug: print v
                        if v > 0:
                            poids[p] = v
                    if debug: print poids
                    competence.poids = poids
            
            if debug: print 
            return dic
        
        self.obj = 'O' in feuille.cell(0,6).value
        self.pre = 'P' in feuille.cell(0,6).value
        
        
        # Eventuels éléments associés à ces compétences
        if feuille.cell(2,5).value != "" and feuille.cell(3,5).value != "": # il y en a !
            t = feuille.cell(2,5).value
            erreur = False
            if t[:4] == "Comp":
                self.asso_type.append(ref.dicoCompetences[t[5:]])
            elif t[:3] == "Sav":
                self.asso_type.append(ref.dicoSavoirs[t[4:]])
            elif t == "Th":
                self.asso_type.append(ref.thematiques)
            elif t == "Dom":
                self.asso_type.append(ref.domaines)
            else:
                erreur = True
            
            if not erreur:
                self.asso_contexte.append(feuille.cell(3,5).value)
            
        
        self.dicCompetences = getArbreComp(feuille, range(4, feuille.nrows), 0, 
                                           prems = True, debug = debug)

        if debug: 
            print self.dicCompetences
            for typi, dico in self.dicCompetences.items():
                print " _poids :", dico.poids

        
        
    #########################################################################
    def getCompetence(self, comp):
#         print "getCompetence", comp
        def getComp(dic):
#             print "   ", dic
            if comp in dic.keys():
                return dic[comp]
            else:
                for k, competence in dic.items():
                    c = getComp(competence.sousComp)
                    if c is not None: 
#                         print "   ", k, "!!!!!"
                        return c

        return getComp(self.dicCompetences)
        
        
    #########################################################################
    def getCompetenceEtGroupe(self, comp):
#         print "getCompetenceEtGroupe", comp
        grp = []
        def getComp(dic):
#             print "   ", dic
            if comp in dic.keys():
                return dic[comp]
            else:
                for k, competence in dic.items():
                    c = getComp(competence.sousComp)
                    if c is not None:
                        grp.insert(0, (k,competence))
                        return c
        grp.append((comp, getComp(self.dicCompetences)))
#         print ">>>", grp
        return grp

#     #########################################################################
#     def getCompetenceEtGroupe(self, comp):
#         grp = [None]
#         def getComp(dic, prem = False):
# #             print "   ", dic
#             if comp in dic.keys():
#                 if prem:
#                     grp[0] = dic[comp]
#                 return dic[comp]
#             else:
#                 for k, competence in dic.items():
#                     if prem:
#                         grp[0] = dic[k]
#                     c = getComp(competence.sousComp)
#                     
#                     if c is not None:
#                         return c
#         cmp = getComp(self.dicCompetences, prem = True)
#         return grp[0], cmp
#     
    
    #########################################################################
    def get2Niveaux(self):
        """ Renvoie une liste de listes (2 premiers niveaux)
            format :
            [['A', ['A1', 'A2', 'A3']],
             ['B', ['B1', 'B2']],
             ...]
        """
        lst0 = []
        for k0, v0 in self.dicCompetences.items():
            lst1 = []
            for k1, v1 in v0.sousComp.items():
                lst1.append(k1)
            lst1.sort()
            lst0.append([k0, lst1])
        lst0.sort(key = lambda c:c[0])
        return lst0
            
    #########################################################################
    def getProfondeur(self):
        for k0, v0 in self.dicCompetences.items():
            for k1, v1 in v0.sousComp.items():
                if len(v1.sousComp) > 0:
                    return 3
                else:
                    return 2
            return 1




#################################################################################################################################
#
#        Savoirs
#
#################################################################################################################################
class Savoirs(XMLelem):
    def __init__(self, nomGenerique = u"Savoirs", codeDiscipline = "", nomDiscipline = u"", abrDiscipline = u""):
        self._codeXML = "Savoirs"
        self.nomGenerique = nomGenerique
        self.codeDiscipline = codeDiscipline
        self.nomDiscipline = nomDiscipline
        self.abrDiscipline = abrDiscipline
        self.dicSavoirs = {}
        self.obj = self.pre = True
    
    
    def getSavoir(self, code, dic = None, c = 1):
        if dic == None:
            dic = self.dicSavoirs

        if dic.has_key(code):
            return dic[code][0]
        else:
            cd = ".".join(code.split(".")[:c])
            return self.getSavoir(code, dic[cd][1], c+1)

    def getSousSavoirs(self, code):
        """ Renvoie la liste des code des sous-savoirs
            [] si on est au bout de la branche
        """
        
        if code in self.dicSavoirs.keys() and len(self.dicSavoirs[code]) > 1:
            return self.dicSavoirs[code][1].keys()
        return []
    
    
objets = {"Indicateur" : Indicateur,
          "Projet" : Projet,
          "Savoirs" : Savoirs,
          "Competences" : Competences}     

##########################################################################################
## source : http://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
#import re
#
#def atoi(text):
#    return int(text) if text.isdigit() else text
#
#def natural_keys(text):
#    '''
#    alist.sort(key=natural_keys) sorts in human order
#    http://nedbatchelder.com/blog/200712/human_sorting.html
#    (See Toothy's implementation in the comments)
#    '''
#    return [ atoi(c) for c in re.split('(\d+)', text) ]



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
    ET.ElementTree(root).write(fichier, xml_declaration=False, encoding = util_path.SYSTEM_ENCODING)
    fichier.close()
    
#enregistrer("SSI", "testSauvRef.xml")


##########################################################################################
def ouvrir(nomFichier):
    """ Ouvre un Referentiel au format .xml
    """
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
    
# print REFERENTIELS["SSI"] == ref
    
#ouvrir("testSauvRef.xml")


##########################################################################################
SAUVEGARDE = False


#######################################################################################  
#import sys
#FILE_ENCODING = sys.getfilesystemencoding()
#DEFAUT_ENCODING = "utf-8"
#def toFileEncoding(path):
#    try:
#        path = path.decode(DEFAUT_ENCODING)
#        return path.encode(FILE_ENCODING)
#    except:
#        return path

##########################################################################################
def chargerReferentiels():
    global REFERENTIELS, ARBRE_REF
    
    #
    # Chargement des fichiers .xls
    #
    
#    print path_ref
    liste = os.listdir(DOSSIER_REF)
    
    for fich_ref in [r for r in liste if r[0] != "_"]:# ["Ref_STS-SN_EC.xls", "Ref_SSI.xls", "Ref_STI2D-AC.xls", "Ref_STI2D-SIN.xls", "Ref_STI2D-ITEC.xls", "Ref_STI2D-EE.xls", "Ref_STI2D-ETT.xls",
#                     "Ref_2nde-EE-CIT.xls", "Ref_2nde-EE-DIT.xls", "Ref_2nde-EE-SI.xls"]:#liste:#["Ref_STS-SN_EC-1.xls", "Ref_SSI.xls"]:#, "Ref_STI2D-EE.xls", "Ref_STI2D-ETT.xls"]:#["Ref_6CLG.xls"]:#
        
        if os.path.splitext(fich_ref)[1] == ".xls":
#            print
            
            ref = Referentiel(os.path.join(DOSSIER_REF, fich_ref))
            ref.postTraiter()
            REFERENTIELS[ref.Code] = ref
#            print ref.Code

    for k, r in REFERENTIELS.items():
#        print r
        r.completer()
#         print "############################"+ k
#         print r.dicoCompetences
#         print 
#        if r.Code == "ITEC":
#        print r
    

    #
    # Vérification intégrité en comparant avec le fichier .xml (s'il existe)
    #
    if not SAUVEGARDE:
        dicOk = {}
        for k, r in REFERENTIELS.items():
#             print DOSSIER_REF
            f = os.path.join(DOSSIER_REF, util_path.toFileEncoding(u"Ref_"+r.Enseignement[0]+u".xml"))
            dicOk[k] = False
            if os.path.exists(f):
#                 print ">>",f
                ref = ouvrir(f)
#                print "<<", f
#                for p in ref.projets.values():
#                    print p.grilles
                
                if ref == r:
                    dicOk[k] = True
            else:
                enregistrer(r.Code, f)
                dicOk[k] = None
                
        print u"Référentiels modifiés :", [k for k, v in dicOk.items() if not v]
    
    #
    # Construction de la structure en arbre
    #
    
    # Tri des items par période scolaire (AnneeDebut)
    def num(k, r):
        if len(r) > 0:
            p = REFERENTIELS[r[0]].AnneeDebut
        else:
            p = REFERENTIELS[k].AnneeDebut
        if p[:3] in PERIODES:
            i = (PERIODES.index(p[:3])+1) * 100
        else:
            i = 0
        try:
            a = int(p[3:])
        except:
            a = 0
        return i+a
    
    def comp_per(ref1, ref2):
        k1, r1 = ref1
        k2, r2 = ref2
        return num(k1, r1) - num(k2, r2)
    
    
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
#         r = sorted(r.items(), cmp = comp_per)
#         r.reverse()
    
    
    
    
    
    ARBRE_REF = sorted(ARBRE_REF.items(), cmp = comp_per)

    
    
chargerReferentiels()


def sauvegarderOriginaux():
    global SAUVEGARDE
    SAUVEGARDE = True
    for r in REFERENTIELS.values():
        f = os.path.join(DOSSIER_REF, "Ref_"+r.Enseignement[0]+".xml")
        enregistrer(r.Code, f)
        
#
# Ligne à décommenter pour faire une sauvegarde XML des référentiels "originaux"
#   Commenter en parallèle la partie "Vérification" de chargerReferentiels()
#
#sauvegarderOriginaux()







