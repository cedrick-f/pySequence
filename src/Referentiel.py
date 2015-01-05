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

# Pour enregistrer en xml
import xml.etree.ElementTree as ET
Element = type(ET.Element(None))


#########################################################################################
DOSSIER_REF = "referentiels"
REFERENTIELS = {}
ARBRE_REF = {}    

#################################################################################################################################
#
#        Référentiel
#
#################################################################################################################################
class Referentiel():
    
    def __init__(self, nomFichier = r""):
        # Enseignement       Famille,    Nom    , Nom complet
        
        self.initParam()

        if nomFichier != r"":
            self.importer(nomFichier)

    ######################################################################################  
    def __repr__(self):
        print "*********************"
        print self.Code, self.projet
        print "positions_CI", self.positions_CI
#        print "CI_BO :", self.CI_BO
#        print "CI  :", self.CentresInterets
#        print "Sav :", self.dicSavoirs
#        print "cellulesInfo_prj = ", self.cellulesInfo_prj
#        print "dicSavoirs_Math", self.dicSavoirs_Math
        print "_dicCompetences_prj", self._dicCompetences_prj
#        print "_dicCompetences_prj_simple", self._dicCompetences_prj_simple
#        for p in self.getParams():
#            v = getattr(self, p)
#            if type(v) == dict:
#                print p, v
#        print "dicCompetences :", self.dicCompetences
#        print "CoP :", self.dicCompetences_prj
#        print "_dicIndicateurs_prj_simple :", self._dicIndicateurs_prj_simple.keys()
#        print "_dicIndicateurs_prj :", self._dicIndicateurs_prj
#        print "Poi :", self.dicPoidsIndicateurs_prj
#        print "Lig :", self.dicLignesIndicateurs_prj
#        print "Mat :", self.dicSavoirs_Math
#        print "Phy :", self.dicSavoirs_Phys
        print "Dem :", self.demarches
#        print "Act :", self.activites
#        print "Sea :", self.seances
        print "DeS :", self.demarcheSeance
#        print self.phases_prj
#        print self.listPhasesEval_prj
#        print "listPhases_prj =", self.listPhases_prj
#        print
#        print "colonneNON", self.colonneNON
#        print "feuilleNON", self.feuilleNON
        return ""
    
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
        
        #
        # Centre d'intérêt
        #
        self.CentresInterets = []       #
        self.CI_BO = True               # les ci sont donnés par le B.O. (pas modifiables)
        self.CI_cible = False           # les ci se placent sur une cible MEI FSC
        self.positions_CI = []          # positions sur la cible MEI FSC
        
        
        #
        # Savoirs ou capacités
        #
        self.nomSavoirs = u"Savoirs"    # nom donnés aux savoirs : "Savoirs", "Capacités", ...
        self.dicSavoirs = {}

        #
        # Compétences
        #
        self.nomCompetences = u"Compétences"    # nom donnés aux compétences : "Compétences", ...
#        self.prof_Comp = 0              # compteur de profondeur de l'arborescence des compétences
        self.dicCompetences = {}
        self.projet = False             # si l'enseignement fait l'objet d'une épreuve de projet
        self.duree_prj = 0
        self.periode_prj = []
        self.aColNon = {'R' : True,  'S' : False}
#        self.dicCompetences_prj = {}
#        self.dicIndicateurs_prj = {}
#        self.dicPoidsIndicateurs_prj = {}
#        self.dicLignesIndicateurs_prj = {}

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
        
        self.dicSavoirs_Math = {}
        self.dicSavoirs_Phys = {}
        
        #
        # grilles d'évaluation de projet
        #
        self.grilles_prj = {}
        self.nomParties_prj = {}
        self.cellulesInfo_prj = {}

        #
        # phases de projet
        #
        self.phases_prj = {}
        self.listPhasesEval_prj = []
        self.listPhases_prj = []
        self.posRevues = {2 : [], 3 : []}
        
        
        #
        # Bulletins Officiels
        #
        self.BO_dossier = u""
        self.BO_URL = u""
        
        
        #
        # tableau de synthèse
        #
        # Nom Fichier
#        self.fichierProgressionProgramme = r""
#        self.dicCellSavoirs = {}
    
    
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
    def getBranche(self):
        """ Construction et renvoi d'une branche XML
            (enregistrement de fichier)
        """
        ref = ET.Element("Referentiel")

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
                    sauv(sub, sv, nom+format(i, "02d"))
            elif type(val) == dict:
                sub = ET.SubElement(branche, "d_"+nom)
                for k, sv in val.items():
                    if type(k) != str and type(k) != unicode:
                        k = "_"+format(k, "02d")
                    sauv(sub, sv, k)
        
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
#        print "setBranche référentiel"
        self.initParam()

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
#                if branche.get(nom) == None: return False # Pour corriger un bug (version <=5.0beta3)
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
            
        self.postTraiter()
        self.completer()

        return
        
    
    
    ######################################################################################  
    def __eq__(self, ref):
        """ Comparaison de deux référentiels
        """
        if not isinstance(ref, Referentiel):
            return False
        
        def egal(val1, val2):
            if isinstance(val1, (str, unicode)) and isinstance(val2, (str, unicode)):
                if val1 != val2:#.replace("\n", "--"):
                    print "Erreur s : xml =", val1, "      xls =", val2#.replace("\n", "--")
                return val1 == val2#.replace("\n", "--")
            elif isinstance(val1, (int, long, float)) and isinstance(val2, (int, long, float)):
                if val1 != val2:
                    print "Erreur : xml =", val1, "      xls =", val2
                return val1 == val2
            elif type(val1) == bool and type(val2) == bool:
                if val1 != val2:
                    print "Erreur : xml =", val1, "      xls =", val2
                return val1 == val2
            
            elif type(val1) == list:
                if len(val1) != len(val2):
                    print "Erreur : xml =", val1, "      xls =", val2
                    return False
                e = True
                for sval1, sval2 in zip(val1, val2):
                    e = e and egal(sval1, sval2)
                return e
            
            elif type(val1) == dict and type(val2) == dict:
                if not egal(sorted(val1), sorted(val2)):
                    print "Erreur : xml =", val1, "      xls =", val2
                    return False
                e = True
                for k, v in val1.items():
#                    if isinstance(k, (str, unicode)):
#                        k = k.replace("--", "\n")
                    e = e and egal(v, val2[k])
                return e
            
            else:
                print "Erreur : xml =", val1, "      xls =", val2
                return False
        
        for attr in dir(self):
            if attr[0] != "_":
                val1 = getattr(self, attr)
                if isinstance(val1, (str, unicode, int, long, float, bool, list, dict)) :
                    val2 = getattr(ref, attr)
                    if not egal(val1, val2):
                        print "Différence"
                        print "  ", attr
                        print "  ", val1
                        print "  ", val2
#                        break
                        return False
        return True
                    
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
        def int0(txt):
            try:
                return int(txt)
            except:
                return 0
            
        ###########################################################
        def getArbre(sh, rng, col, prems = False, debug = False):
            """ Construit le structure en arbre de "compétences"
            """
            dic = {}
            lstLig = [l  for l in rng if sh.cell(l,col).value != u""]
            if debug: print "  **",lstLig
            for i, l in enumerate(lstLig):
                code = str(sh.cell(l,col).value)
                intitule = unicode(sh.cell(l,col+1).value)
                if debug: print "-> ",l, code, intitule
                
                if i < len(lstLig)-1:
                    ssRng = range(l+1, lstLig[i+1])
                else:
                    ssRng = range(l+1, rng[-1]+1)
                
                if debug: print "   ", ssRng
                if len(ssRng) > 0 and col < 2 and [li  for li in ssRng if sh.cell(li,col+1).value != u""] != []:
                    dic[code] = [intitule, getArbre(sh, ssRng, col+1, debug = debug)]
                    if prems:
                        poids = [int0(sh.cell(l,7).value),  # poids Ecrit
                                 int0(sh.cell(l,8).value),  # poids Conduite projet
                                 int0(sh.cell(l,9).value)]  # poids Soutenance projet
                        dic[code].append(poids)
                else:
                    dic[code] = [intitule, []]
                    for ll in [l] + ssRng:
                        indic = unicode(sh.cell(ll,5).value)
                        poids = [int0(sh.cell(ll,7).value),  # poids Ecrit
                                 int0(sh.cell(ll,8).value),  # poids Conduite projet
                                 int0(sh.cell(ll,9).value)]  # poids Soutenance projet
                        ligne = int0(sh.cell(ll,10).value)   # ligne dans la grille
                        if ligne != 0:
                            if poids[1] != 0:
                                self.aColNon['R'] = True
                            elif poids[2] != 0:
                                self.aColNon['S'] = True
                        dic[code][1].append([indic, poids, ligne])
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

        lig = [l  for l in range(10, 17) if sh_g.cell(l,3).value != u""]
        for l in lig:
            self.periodes.append([sh_g.cell(l,2).value, int(sh_g.cell(l,3).value)])
            
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
        sh_g = wb.sheet_by_name(u"Généralités")
        if sh_g.cell(21,0).value != u"":
            self.tr_com = [sh_g.cell(21,0).value, sh_g.cell(21,1).value]
           
        #
        # projet
        #
        sh_g = wb.sheet_by_name(u"Généralités")
        self.projet = sh_g.cell(23,1).value[0].upper() == "O"
        if self.projet:
            self.duree_prj = int(sh_g.cell(24,1).value)
            self.periode_prj = [int(i) for i in sh_g.cell(25,1).value.split()]
#            print ">>", self.periode_prj
        #
        # Bulletins Officiels
        #
        if sh_g.nrows > 28:
            self.BO_dossier = sh_g.cell(29,0).value
            self.BO_URL = sh_g.cell(29,1).value
        
        
        #
        # CI
        #
        sh_ci = wb.sheet_by_name(u"CI")
        self.CI_BO = sh_ci.cell(0,1).value[0].upper() == "O"
        self.CI_cible = sh_ci.cell(1,1).value[0].upper() == "O"
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
        self.dicSavoirs = remplir(sh_va, 0, range(1, sh_va.nrows))
            
        #
        # Compétences
        #
        sh_va = wb.sheet_by_name(u"Compétences")
        self.nomCompetences =   sh_va.cell(0,0).value 
#        self.prof_Comp = 0 # compteur de profondeur 
#        self.dicCompetences = remplir(sh_va, 0, range(1, sh_va.nrows), mode = 2)
#        print ">>>", self.Code
        
        # Pour enregistrer s'il y a des colonnes "non" dans les grilles 'R' ou 'S'
#        self.aColNon = {'R' : False,  'S' : False}
        self.dicCompetences = getArbre(sh_va, range(1, sh_va.nrows), 0, prems = True, debug = False)
#        print "_aColNon", self.Code, ":", self._aColNon
         
            
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
            self.dicSavoirs_Math = remplir(sh_va, 0, range(1, sh_va.nrows))
        
        #
        # Savoirs Physique
        #
        if u"Phys" in wb.sheet_names():
            sh_va = wb.sheet_by_name(u"Phys")     
            self.dicSavoirs_Phys = remplir(sh_va, 0, range(1, sh_va.nrows))
        
        #
        # Grilles d'évaluation projet
        #
        if self.projet:
            sh_g = wb.sheet_by_name(u"Grille_PRJ")
            for l in range(2,4):
                if sh_g.cell(l,0).value != u"":
                    self.grilles_prj[str(sh_g.cell(l,0).value)] = [sh_g.cell(l,2).value, sh_g.cell(l,3).value]
                    self.nomParties_prj[str(sh_g.cell(l,0).value)] = sh_g.cell(l,1).value
                    
            for l in range(7, sh_g.nrows):
                k = str(sh_g.cell(l,0).value)
                if k != u"":                                                                  
                    i = [sh_g.cell(l,1).value, # Classeur
                         sh_g.cell(l,2).value, # Feuille
                         [int0(sh_g.cell(l,3).value), # Ligne
                          int0(sh_g.cell(l,4).value), # Colonne
                          int0(sh_g.cell(l,5).value)], #Période
                         sh_g.cell(l,6).value]  # Préfixe
                    if k in self.cellulesInfo_prj.keys():
                        self.cellulesInfo_prj[k].append(i)
                    else:
                        self.cellulesInfo_prj[k] = [i]
        
        #
        # Phases du projet
        #
        if self.projet:
            shp = wb.sheet_by_name(u"Phase_PRJ")
            for l in range(2, shp.nrows):
                if shp.cell(l,0).value != u"":
                    if shp.cell(l,1).value != u"":
                        self.phases_prj[str(shp.cell(l,0).value)] = [shp.cell(l,1).value, shp.cell(l,2).value, shp.cell(l,3).value]
                        if shp.cell(l,4).value != "":
                            self.listPhasesEval_prj.append(shp.cell(l,0).value)
                        self.listPhases_prj.append(shp.cell(l,0).value)
                        if shp.cell(l,5).value != "":
                            self.posRevues[2].append(shp.cell(l,0).value)
                        if shp.cell(l,6).value != "":
                            self.posRevues[3].append(shp.cell(l,0).value)
                            
                            
                            
        
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
        
    ###########################################################
    def getDernierNiveauArbre(self, dic):
        sdic = {}
        for k0, v0 in dic.items():
            if len(v0) > 1 and  type(v0[1]) == dict:
                sdic.update(self.getDernierNiveauArbre(v0[1]))
            else:
                sdic[k0] = v0
        return sdic
        
    ###########################################################
    def getPremierEtDernierNiveauArbre(self, dic):
        sdic = {}
        for k0, v0 in dic.items():
            if len(v0) > 1 and  type(v0[1]) == dict:
                if len(v0) == 3: # premier niveau
                    sdic[k0] = [v0[0], self.getDernierNiveauArbre(v0[1]), v0[2]]
                else:
                    sdic.update(self.getDernierNiveauArbre(v0[1]))
            else:
                sdic[k0] = v0
        return sdic
    
    
    #########################################################################
    def postTraiter(self):
        """ Complète les données selon que le référentiel ait un tronc commun ou des options
            
            --> le "_" évite que les attributs ne soient sauvegardés dans les XML
            
        """
        ###########################################################
        def getArbreProjet(dic, debug = False):
            sdic = {}
            for k0, v0 in dic.items():
                if debug: print k0
                if len(v0) > 1 and type(v0[1]) == dict:
                    if debug: print "   ", v0[0]
                    if len(v0) == 2:
                        sdic[k0] = [v0[0], getArbreProjet(v0[1], debug = debug)]
                    else:
                        if debug: print "   prem's", v0[2]
                        if v0[2][1] != 0 or v0[2][2] != 0: # Conduite ou Soutenance
                            sdic[k0] = [v0[0], getArbreProjet(v0[1], debug = debug), v0[2]]
                else:
                    lst = []
                    for l in v0[1]:
                        if debug: print l[1]
                        if l[1][1] != 0 or l[1][2] != 0: # Conduite ou Soutenance
                            lst.append([l[0], l[1], l[2]])
                    if lst != []:
                        sdic[k0] = [v0[0], lst]
            return sdic
        
        
        
        
        
        
        ###########################################################
        def getDernierNiveauArbre2(dic):
            sdic = {}
            for k0, v0 in dic.items():
                if type(v0) == dict:
                    sdic.update(self.getDernierNiveauArbre(v0))
                else:
                    sdic[k0] = v0
            return sdic
        
        
        
        ###########################################################
        def getDeuxiemeNiveauArbre(dic):
            sdic = {}
            for k0, v0 in dic.items():
                for k1, v1 in v0[1].items():
                    if len(v1) > 1 and  type(v1[1]) == dict: # pas fini = 3ème niveau
                        self._niveau = 3
                        sdic[k1] = {}
                        for k2, v2 in v1[1].items():
                            sdic[k1][k2] = v2[1]
                    else:   # Niveau "indicateur"
                        self._niveau = 2
                        sdic[k1] = v1[1]
            return sdic
        
        
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
                        if debug: print l[0]
                        if "idem" in l[0]:
                            if debug: print "    idem"
                            codeindic = str(l[0].split(" ")[1])
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
            
        ###########################################################
        def normaliserPoids(dic, debug = False):
            for k0, v0 in dic.items():
                poids_tot = v0[2][1:]
                tot = [0,0]
                for v1 in v0[1].values():
                    if debug: print " ", v1
                    for indic in v1[1]:
                        tot = [tot[0] + indic[1][1], tot[1] + indic[1][2]]
                if debug: print "  tot", tot
                coef = [1.0*tot[0]/100, 1.0*tot[1]/100]
                if debug: print "  coef", coef
                for v1 in v0[1].values():
                    for indic in v1[1]:
                        if coef[0] != 0:
                            indic[1][1] = round(indic[1][1] / coef[0], 6)
                        if coef[1] != 0:
                            indic[1][2] = round(indic[1][2] / coef[1], 6)
                    
            
        
#        print "dicCompetences", self.dicCompetences
        self._dicCompetences_prj = getArbreProjet(self.dicCompetences, debug = False)
        
        # On regroupe les compétences qui ont les mêmes indicateurs dans la grille (cas de STI2D EE !!)
        lst_codeindic = chercherIndicIdem(self._dicCompetences_prj, debug = False)
#        print "lst_codeindic", lst_codeindic
        if type(lst_codeindic) == tuple:
            dic = chercherDicIndic(self._dicCompetences_prj, lst_codeindic[2])
#            print "   >>", dic
            new_code = lst_codeindic[1]+"\n"+lst_codeindic[2]
            dic[new_code] = [dic[lst_codeindic[1]][0]+"\n"+dic[lst_codeindic[2]][0], dic[lst_codeindic[1]][1]]
            del dic[lst_codeindic[2]]
            del dic[lst_codeindic[1]]
#        print "_dicCompetences_prj", self._dicCompetences_prj
#        print self.getCompetence('A')
#        print self.getCompetence('A1')
#        print self.getCompetence('B2')
#        print self.getCompetence('A1.4')
        
        self._dicIndicateurs_prj = self.getPremierEtDernierNiveauArbre(self._dicCompetences_prj)
        
#        print "_dicIndicateurs_prj", self._dicIndicateurs_prj
        normaliserPoids(self._dicIndicateurs_prj, debug = False)
#        print "                   ", self._dicIndicateurs_prj
        
        self._niveau = 0
        self._dicIndicateurs_prj_famille = getDeuxiemeNiveauArbre(self._dicCompetences_prj)
#        print "_dicIndicateurs_prj_famille", self._dicIndicateurs_prj_famille
#        print "_niveau", self._niveau
#        print 
        
        self._dicIndicateurs_prj_simple = getDernierNiveauArbre2(self._dicIndicateurs_prj_famille)
#        print "_dicIndicateurs_prj_simple", self._dicIndicateurs_prj_simple
        
#        lst.extend()
        
        
    #########################################################################
    def completer(self):
        """ Complète les données selon que le référentiel ait un tronc commun ou des options
            Exécuté lorsque tous les référentiels sont chargés !
            
            --> le "_" évite que les attributs ne soient sauvegardés dans les XML
            
        """
        
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
        def getDernierNiveauArbre2(dic):
            sdic = {}
            for k0, v0 in dic.items():
                if type(v0) == dict:
                    sdic.update(getDernierNiveauArbre(v0))
                else:
                    sdic[k0] = v0
            return sdic

        ###########################################################
        def getDernierNiveauArbre(dic):
            sdic = {}
            for k0, v0 in dic.items():
                if len(v0) > 1 and  type(v0[1]) == dict:
                    sdic.update(getDernierNiveauArbre(v0[1]))
                else:
                    sdic[k0] = v0
            return sdic
                
        if self.tr_com != []:
            t = self.tr_com[0]
            if t in REFERENTIELS.keys():
#                print "Add"
#                print self._dicCompetences_prj
#                print REFERENTIELS[t]._dicCompetences_prj
                self._dicCompetences_prj.update(REFERENTIELS[t]._dicCompetences_prj)
                self._dicIndicateurs_prj.update(REFERENTIELS[t]._dicIndicateurs_prj)
#                if 'O8s' in self._dicIndicateurs_prj.keys():
#                    self._dicIndicateurs_prj['O8'][1].update(self._dicIndicateurs_prj['O8s'][1])
#                    del self._dicIndicateurs_prj['O8s']
                self._dicIndicateurs_prj_simple.update(REFERENTIELS[t]._dicIndicateurs_prj_simple)
#                print ">>", self._dicCompetences_prj
        
        if self.projet:
            self._lstGrpIndicateurRevues = []
            self._lstGrpIndicateurSoutenance = []
#            print "_dicIndicateurs_prj", self._dicIndicateurs_prj
            for comp, dic in self._dicIndicateurs_prj.items():
                for indics in getDernierNiveauArbre2(dic[1]).values():
                    for indic in indics[1]:
#                        print "   ", indic
                        poids = indic[1]
                        if poids[1] != 0:
                            self._lstGrpIndicateurRevues.append(comp)
                        if poids[2] != 0:
                            self._lstGrpIndicateurSoutenance.append(comp)
                                
            self._lstGrpIndicateurSoutenance = list(set(self._lstGrpIndicateurSoutenance))
            self._lstGrpIndicateurRevues = list(set(self._lstGrpIndicateurRevues))
#            if "O8s" in self._lstGrpIndicateurSoutenance:
#                self._lstGrpIndicateurSoutenance.remove("O8s")
#                self._lstGrpIndicateurSoutenance.append("O8")
        
#            print "_lstGrpIndicateurRevues", self._lstGrpIndicateurRevues
#            print "_lstGrpIndicateurSoutenance", self._lstGrpIndicateurSoutenance
        
            if self.tr_com != []:
                self.grilles_prj.update(REFERENTIELS[self.tr_com[0]].grilles_prj)
                
                
#        self._dicCompetences_prj_simple = aplatir(self._dicCompetences_prj)
        
        
    #########################################################################
    def getIndicateur(self, codeIndic):
        if '_' in codeIndic:
            code, i = codeIndic.split('_')
            i = int(i)
            if code in self._dicIndicateurs_prj_simple.keys():
                indics = self._dicIndicateurs_prj_simple[code]
                if len(indics) >= i:
                    indic = indics[i-1]
                    return indic
        else:
            comp = self.getCompetence_prj(codeIndic)
            if type(comp[1]) == dict:
                return self.getPremierEtDernierNiveauArbre(comp[1])
            else: 
                return comp[1]


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
    def getCompetence_prj(self, comp):
        if comp in self._dicCompetences_prj.keys():
            return self._dicCompetences_prj[comp]
        else:
            for k0, v0 in self._dicCompetences_prj.items():
                if type(v0[1]) == dict:
                    if comp in v0[1].keys():
                        return v0[1][comp]
                    else:
                        for k1, v1 in v0[1].items():
                            if type(v1[1]) == dict and comp in v1[1].keys():
                                return v1[1][comp]
                            
    #########################################################################
    def getTypeIndicateur(self, codeIndic):
#        print "getTypeIndicateur", codeIndic
        if type(codeIndic) == str:
            indic = self.getIndicateur(codeIndic)
        else:
            indic = codeIndic
        if indic != None:
            if len(indic)>1:
                if len(indic[1])>2:
                    if indic[1][0] != 0:
                        return "E"
                    elif indic[1][1] != 0:
                        return "C"
                    elif indic[1][2] != 0:
                        return "S"
        
    
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
    def getClefDic(self, dicattr, nom, num = None):
        dic = getattr(self, dicattr)
        for k,v in dic.items():
            if num != None:
                v = v[num]
            if v == nom:
                return k
        return None
    
    
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
    ref.setBranche(root)
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
    
    for fich_ref in liste:#["Ref_SSI.xls", "Ref_STI2D-EE.xls", "Ref_STI2D-ETT.xls"]:#["Ref_6CLG.xls"]:#
        
        if os.path.splitext(fich_ref)[1] == ".xls":
#            print
#            print fich_ref
            ref = Referentiel(os.path.join(constantes.PATH, r"..", DOSSIER_REF, fich_ref))
            ref.postTraiter()
            REFERENTIELS[ref.Code] = ref
            
    
    for r in REFERENTIELS.values():
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







