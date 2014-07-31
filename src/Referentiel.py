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
        print self.Code
#        print "CI_BO :", self.CI_BO
#        print "CI  :", self.CentresInterets
#        print "Sav :", self.dicSavoirs
        print "cellulesInfo_prj = ", self.cellulesInfo_prj
#        print "dicSavoirs_Math", self.dicSavoirs_Math
        print "dicCompetences_prj", self.dicCompetences_prj
#        print "_dicCompetences_prj_simple", self._dicCompetences_prj_simple
#        for p in self.getParams():
#            v = getattr(self, p)
#            if type(v) == dict:
#                print p, v
#        print "Com :", self.dicCompetences
#        print "CoP :", self.dicCompetences_prj
#        print "CoS :", self._dicCompetences_prj_simple
#        print "Ind :", self.dicIndicateurs_prj
#        print "Poi :", self.dicPoidsIndicateurs_prj
#        print "Mat :", self.dicSavoirs_Math
#        print "Phy :", self.dicSavoirs_Phys
#        print "Dem :", self.demarches
#        print "Act :", self.activites
#        print "Sea :", self.seances
#        print "DeS :", self.demarcheSeance
#        print self.phases_prj
#        print self.listPhasesEval_prj
#        print "listPhases_prj =", self.listPhases_prj
        print
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
        self.tr_com = None              # tronc commun de l'enseignement : Code
        
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
        self.prof_Comp = 0              # compteur de profondeur de l'arborescence des compétences
        self.dicCompetences = {}
        self.projet = False             # si l'enseignement fait l'objet d'une épreuve de projet
        self.duree_prj = 0
        self.dicCompetences_prj = {}
        self.dicIndicateurs_prj = {}
        self.dicPoidsIndicateurs_prj = {}

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
#            if u"é" in nom:
            if type(val) == str or type(val) == unicode:
                branche.set("S_"+nom, val)
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
        self.initParam()
        
        def lect(branche, nom = ""):
            if nom[:2] == "S_":
                return unicode(branche.get(nom))
            elif nom[:2] == "I_":
                return int(eval(branche.get(nom)))
            elif nom[:2] == "L_":
                return long(eval(branche.get(nom)))
            elif nom[:2] == "F_":
                return float(eval(branche.get(nom)))
            elif nom[:2] == "B_":
                return branche.get(nom)[0] == "T"
            elif nom[:2] == "l_":
                sbranche = branche.find(nom)
                dic = {}
                for k, sb in sbranche.items():
                    dic[k[2:]] = lect(sbranche, k)
                for sb in list(sbranche):
                    k = sb.tag
                    dic[k[2:]] = lect(sbranche, k)
#                print dic.values()
                liste = [dic[v] for v in sorted(dic)]
#                print " >", liste
                return liste
#                liste = [lect(sbranche, k) for k, sb in sbranche.items()]
#                return liste + [lect(sb, k) for k, sb in list(sbranche)]
            elif nom[:2] == "d_":
                sbranche = branche.find(nom)
                d = {}
                for k, sb in sbranche.items():
                    d[k[2:]] = lect(sbranche, k)
                for sb in list(sbranche):
                    k = sb.tag
                    _k = k[2:]
                    if _k[0] == "_":
                        _k = eval(_k[1:])
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
                    setattr(self, attr, lect(branche, _attr))
        
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
                if val1 != val2:
                    print "Erreur", val1, val2
                return val1 == val2
            elif isinstance(val1, (int, long, float)) and isinstance(val2, (int, long, float)):
                if val1 != val2:
                    print "Erreur", val1, val2
                return val1 == val2
            elif type(val1) == bool and type(val2) == bool:
                if val1 != val2:
                    print "Erreur", val1, val2
                return val1 == val2
            
            elif type(val1) == list:
                if len(val1) != len(val2):
                    print "Erreur", val1, val2
                    return False
                e = True
                for sval1, sval2 in zip(val1, val2):
                    e = e and egal(sval1, sval2)
                return e
            
            elif type(val1) == dict and type(val2) == dict:
                if not egal(sorted(val1), sorted(val2)):
                    print "Erreur", val1, val2
                    return False
                e = True
                for k, v in val1.items():
                    e = e and egal(v, val2[k])
                return e
            
            else:
                print "Erreur", val1, val2
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
            self.prof_Comp = max(self.prof_Comp, col)
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
        def listItemCol(sh, col, rng):
            return [[l, sh.cell(l,col).value]    for l in rng    if sh.cell(l,col).value != u""]
        
        
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
        self.Enseignement[0] = sh_g.cell(6,0).value
        self.Enseignement[1] = sh_g.cell(6,1).value
        self.Enseignement[2] = sh_g.cell(6,2).value

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
        self.prof_Comp = 0 # compteur de profondeur 
        self.dicCompetences = remplir(sh_va, 0, range(1, sh_va.nrows), mode = 2)
       
        #
        # dicIndicateurs_prj
        #     
#        if self.projet:
        sh_va = wb.sheet_by_name(u"Indicateurs_PRJ")     
        lig = [l  for l in range(1, sh_va.nrows) if sh_va.cell(l,1).value != u""]
        llig = lig + [sh_va.nrows]
        dic = {}
        for i, p in enumerate(lig):
            dic[str(sh_va.cell(p,1).value)] = [[sh_va.cell(l,2).value, sh_va.cell(l,3).value == "R"] for l in range(p, llig[i+1]) if sh_va.cell(l,2).value != u""]
        self.dicIndicateurs_prj =  dic
        
        #
        # dicPoidsIndicateurs_prj
        #
#        if self.projet:
        sh_va = wb.sheet_by_name(u"Indicateurs_PRJ")     
        lig = [l  for l in range(1, sh_va.nrows) if sh_va.cell(l,0).value != u""]
        llig = lig + [sh_va.nrows]
        for i, p in enumerate(lig):
            lig2 = [l for l in range(p, llig[i+1]) if sh_va.cell(l,1).value != u""]
            self.dicPoidsIndicateurs_prj[str(sh_va.cell(p,0).value)] = [sh_va.cell(p,4).value, {}]
            llig2 = lig2 + [llig[i+1]]
            for ii, l in enumerate(lig2):
                self.dicPoidsIndicateurs_prj[str(sh_va.cell(p,0).value)][1][sh_va.cell(l,1).value] = [sh_va.cell(pp,4).value for pp in range(l, llig2[ii+1])]
        
        #
        # Compétences pour projet
        #
#        if self.projet:
        sh_va = wb.sheet_by_name(u"Compétences")     
        self.dicCompetences_prj = remplir(sh_va, 0, range(1, sh_va.nrows), mode = 2, condition = "P")
        for c in self.dicCompetences_prj.keys():
            if not c in self.dicPoidsIndicateurs_prj.keys():
                del self.dicCompetences_prj[c]
        
        
            
            
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
                    self.grilles_prj[str(sh_g.cell(l,0).value)] = sh_g.cell(l,2).value
                    self.nomParties_prj[str(sh_g.cell(l,0).value)] = sh_g.cell(l,1).value
                    
            
            for l in range(7,sh_g.nrows):
                k = str(sh_g.cell(l,0).value)
                if k != u"":
                    #    Classeur                Feuille                Ligne                        Colonne
                    i = [sh_g.cell(l,1).value, sh_g.cell(l,2).value, [int(sh_g.cell(l,3).value), int(sh_g.cell(l,4).value)]]
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
        
        
    #########################################################################
    def completer(self):
        """ Complète les données selon que le référentiel ait un tronc commun ou des options
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
        
        
        if self.tr_com:
            t = self.tr_com[0]
            if t in REFERENTIELS.keys():
                self.dicPoidsIndicateurs_prj.update(REFERENTIELS[t].dicPoidsIndicateurs_prj)
                self.dicCompetences_prj.update(REFERENTIELS[t].dicCompetences_prj)
                self.dicIndicateurs_prj.update(REFERENTIELS[t].dicIndicateurs_prj)
        
        if self.projet:
            self._lstGrpIndicateurRevues = []
            self._lstGrpIndicateurSoutenance = []
            for grp, poids in self.dicPoidsIndicateurs_prj.items():
                poidsGrp, dicIndicGrp = poids
                for comp, poidsIndic in dicIndicGrp.items():
                    if comp in self.dicIndicateurs_prj.keys():
                        for i, indic in enumerate(self.dicIndicateurs_prj[comp]):
                            if self.dicIndicateurs_prj[comp][i][1]:
                                self._lstGrpIndicateurRevues.append(grp)
                            else:
                                self._lstGrpIndicateurSoutenance.append(grp)
                                
            self._lstGrpIndicateurSoutenance = list(set(self._lstGrpIndicateurSoutenance))
            self._lstGrpIndicateurRevues = list(set(self._lstGrpIndicateurRevues))
            if "O8s" in self._lstGrpIndicateurSoutenance:
                self._lstGrpIndicateurSoutenance.remove("O8s")
                self._lstGrpIndicateurSoutenance.append("O8")
        
            if self.tr_com:
                self.grilles_prj.update(REFERENTIELS[self.tr_com[0]].grilles_prj)
                
                
        self._dicCompetences_prj_simple = aplatir(self.dicCompetences_prj)
        

        
    

    #########################################################################
    def getSavoir(self, code, dic = None, c = 1, gene = None):
        if dic == None:
            if gene == "M":
                dic = self.dicSavoirs_Math
            elif gene == "P":
                dic = self.dicSavoirs_Phys
            else:
                dic = self.dicSavoirs
        if dic.has_key(code):
            return dic[code][0]
        else:
            cd = ".".join(code.split(".")[:c])
            return self.getSavoir(code, dic[cd][1], c+1)




    #########################################################################    
    def getCompetence(self, code, dic = None, c = None):
        """ Pour obtenir l'intitulé d'une compétence à partir de son code 
                    fonction recursive
        """
#        print "getCompetence", code, dic, c
        if dic == None:
            dic = self.dicCompetences
            
        if dic.has_key(code):
            if type(dic[code]) == list:
                return dic[code][0]
            else:
                return dic[code]
            
        else:
            for c, v in dic.items():
                if type(v) == list:
                    co = self.getCompetence(code, v[1])
                    if co != None:
                        return co
            return
                    
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
    ref.completer()
    fichier.close()
    return ref
    
#    print REFERENTIELS["SSI"] == ref
    
#ouvrir("testSauvRef.xml")


##########################################################################################
def chargerReferentiels():
    global REFERENTIELS, ARBRE_REF
    
    #
    # Chargement des fichiers .xls
    #
    liste = os.listdir(os.path.join(constantes.PATH, r"..", DOSSIER_REF))
    
    for fich_ref in liste:#["Ref_STI2D-ETT.xls"]:#["Ref_6CLG.xls"]:#
        
        if os.path.splitext(fich_ref)[1] == ".xls":
#            print
#            print fich_ref
            ref = Referentiel(os.path.join(constantes.PATH, r"..", DOSSIER_REF, fich_ref))
            REFERENTIELS[ref.Code] = ref
    
    
    for r in REFERENTIELS.values():
        r.completer()
        print r
    
    print
    
    #
    # Vérification intégrité
    #
    dicOk = {}
    for k, r in REFERENTIELS.items():
#        print "Verification", k
        f = os.path.join(constantes.PATH, r"..", DOSSIER_REF, "Ref_"+r.Enseignement[0]+".xml")
        dicOk[k] = False
        if os.path.exists(f):
            ref = ouvrir(f)
            print r
#            print ref
            if ref == r:
                dicOk[k] = True
    print dicOk
    
    #
    # Construction de la structure en arbre
    #
    for k, r in REFERENTIELS.items():
        if not r.tr_com:
            ARBRE_REF[k] = []
    d = []
    for k, r in REFERENTIELS.items():
        if r.tr_com:
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
            
#    print ARBRE_REF
    
    
chargerReferentiels()




##########################################################################################
def sauvegarderOriginaux():
    for r in REFERENTIELS.values():
        f = os.path.join(constantes.PATH, r"..", DOSSIER_REF, "Ref_"+r.Enseignement[0]+".xml")
        enregistrer(r.Code, f)

#sauvegarderOriginaux()


