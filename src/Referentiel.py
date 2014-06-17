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





#################################################################################################################################
#
#        Référentiel
#
#################################################################################################################################
class Referentiel():
    def __init__(self, nomFichier = r""):
        # Enseignement       Famille,    Nom    , Nom complet
        self.Enseignement = [u""    ,   u""]
        
        self.CentresInterets = []

        self.dicSavoirs = {}

        self.dicCompetences = {}
        
        self.dicCompetences_prj = {}
        
        self.dicIndicateurs_prj = {}

        self.dicPoidsIndicateurs_prj = {}

        #
        # grilles d'évaluation de projet
        #
        # Nom Fichier          .xlsx    , .xls
        self.Fichier_GRILLE = [r""      , r""]

        self.Cellules_NON = {}

        #
        # tableau de synthèse
        #
        # Nom Fichier
        self.fichierProgressionProgramme = r""
        self.dicCellSavoirs = {}

        if nomFichier != r"":
            self.importer(nomFichier)

    def importer(self, nomFichier):
        """
        """
        self.cpt = 0 # compteur de profondeur
        
        def remplir(sh, col, rng, mode = 1, condition = None):
            """ Mode = 1 : on finit par une liste
                Mode = 2 : on finit par un dict
            """
            self.cpt = max(self.cpt, col)
#            print "***", col, rng
            lig = [l  for l in rng if sh.cell(l,col).value != u""]
            
            if lig == rng:
#                print "FIN"
                if mode == 1:
                    return [sh.cell(l,col).value for l in lig]
                else:
                    if condition == None or sh.cell(l,4).value == condition:
                        d = {}
                        for l in lig:
                            d[sh.cell(l,col).value] = sh.cell(l,col+1).value
                        return d
                    else:
                        return None
            else:
#                if len(lig) > 0:
#                print "-> ",lig
                llig = lig + [rng[-1]+1]
                dic = {}
                for i, p in enumerate(lig):
                    sdic = remplir(sh, col+1, range(p+1, llig[i+1]), mode = mode, condition = condition)
                    if sdic != None:
                        dic[sh.cell(p,col).value] = [sh.cell(p,col+1).value, sdic]
                return dic
            
            
        ###########################################################
        def listItemCol(sh, col, rng):
            return [[l, sh.cell(l,col).value]    for l in rng    if sh.cell(l,col).value != u""]
        
        
                
        
        
        
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

        #
        # options
        #
        self.options = {}
        sh_g = wb.sheet_by_name(u"Généralités")
        lig = [l  for l in range(10, 17) if sh_g.cell(l,0).value != u""]
        for l in lig:
            self.options[sh_g.cell(l,0).value] = sh_g.cell(l,1).value
        
        #
        # tronc commun
        #
        self.tr_com = None
        sh_g = wb.sheet_by_name(u"Généralités")
        if sh_g.cell(21,0).value != u"":
            self.tr_com = [sh_g.cell(21,0).value, sh_g.cell(21,1).value]
            
        #
        # CI
        #
        sh_ci = wb.sheet_by_name(u"CI")
        self.CI_BO = sh_ci.cell(0,1).value[0].upper() == "O"
        self.CI_cible = sh_ci.cell(1,1).value[0].upper() == "O"
        self.CentresInterets = []
        self.positions_CI = []
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
                        print t
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
        self.cpt = 0 # compteur de profondeur 
        self.dicCompetences = remplir(sh_va, 0, range(1, sh_va.nrows), mode = 2)
        self.prof_Comp = self.cpt
        print self.prof_Comp
       
        #
        # dicIndicateurs_prj
        #     
        sh_va = wb.sheet_by_name(u"Indicateurs_PRJ")     
        lig = [l  for l in range(1, sh_va.nrows) if sh_va.cell(l,1).value != u""]
        llig = lig + [sh_va.nrows]
        dic = {}
        for i, p in enumerate(lig):
            dic[sh_va.cell(p,1).value] = [[sh_va.cell(l,2).value, sh_va.cell(l,3).value == "R"] for l in range(p, llig[i+1]) if sh_va.cell(l,2).value != u""]
        self.dicIndicateurs_prj =  dic
        
        
        
        #
        # dicPoidsIndicateurs_prj
        #
        sh_va = wb.sheet_by_name(u"Indicateurs_PRJ")     
        lig = [l  for l in range(1, sh_va.nrows) if sh_va.cell(l,0).value != u""]
#        l_i = listItemCol(sh_va, 0, range(1, sh_va.nrows))
        llig = lig + [sh_va.nrows]
        for i, p in enumerate(lig):
            lig2 = [l for l in range(p, llig[i+1]) if sh_va.cell(l,1).value != u""]
            self.dicPoidsIndicateurs_prj[sh_va.cell(p,0).value] = [sh_va.cell(p,4).value, {}]
            llig2 = lig2 + [llig[i+1]]
            for ii, l in enumerate(lig2):
                self.dicPoidsIndicateurs_prj[sh_va.cell(p,0).value][1][sh_va.cell(l,1).value] = [sh_va.cell(pp,4).value for pp in range(l, llig2[ii+1])]
        
        #
        # Compétences pour projet
        #
        sh_va = wb.sheet_by_name(u"Compétences")     
        self.dicCompetences_prj = remplir(sh_va, 0, range(1, sh_va.nrows), mode = 2, condition = "P")
        for c in self.dicCompetences_prj.keys():
            if not c in self.dicPoidsIndicateurs_prj.keys():
                del self.dicCompetences_prj[c]
        
        #
        # projet
        #
        sh_g = wb.sheet_by_name(u"Généralités")
        self.projet = sh_g.cell(23,1).value[0].upper() == "O"
        
        
        #
        # démarches et séances
        #
        sh_g = wb.sheet_by_name(u"Activité-Démarche")
        self.demarches = {}
        self.listeDemarches = []
        for l in range(2, 5):
            if sh_g.cell(l,0).value != u"":
                self.demarches[sh_g.cell(l,0).value] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value]
                self.listeDemarches.append(sh_g.cell(l,0).value)
                
        self.activites = {}
        self.listeTypeActivite = []
        for l in range(8, 11):
            if sh_g.cell(l,0).value != u"":
                self.activites[sh_g.cell(l,0).value] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value]
                self.listeTypeActivite.append(sh_g.cell(l,0).value)
                
        self.seances = {}
        self.seances.update(self.activites)
        self.listeTypeSeance = self.listeTypeActivite[:]
        for l in range(14, 21):
            if sh_g.cell(l,0).value != u"":
                self.seances[sh_g.cell(l,0).value] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value]
                self.listeTypeSeance.append(sh_g.cell(l,0).value)
        
        self.demarcheSeance = {}
        for l, s in enumerate(self.listeTypeActivite):
            l = l + 3
            self.demarcheSeance[s] = [sh_g.cell(2,c).value for c in range(5,8) if sh_g.cell(l,c).value != u""]
        
        #
        # effectifs
        #
        sh_g = wb.sheet_by_name(u"Activité-Effectif")
        self.effectifs = {}
        self.listeEffectifs = []
        for l in range(2, 7):
            if sh_g.cell(l,0).value != u"":
                self.effectifs[sh_g.cell(l,0).value] = [sh_g.cell(l,1).value, sh_g.cell(l,2).value]
                self.listeEffectifs.append(sh_g.cell(l,0).value)
                
        
        self.effectifsSeance = {"" : []}
        for l, s in enumerate(self.listeTypeSeance):
            l = l + 3
            self.effectifsSeance[s] = [sh_g.cell(2,c).value for c in range(5,10) if sh_g.cell(l,c).value != u""]
        
        #
        # Savoirs Math
        #
        self.dicSavoirs_Math = None
        if u"Math" in wb.sheet_names():
            sh_va = wb.sheet_by_name(u"Math")     
            self.dicSavoirs_Math = remplir(sh_va, 0, range(1, sh_va.nrows))
        
        #
        # Savoirs Math
        #
        self.dicSavoirs_Phys = None
        if u"Phys" in wb.sheet_names():
            sh_va = wb.sheet_by_name(u"Phys")     
            self.dicSavoirs_Phys = remplir(sh_va, 0, range(1, sh_va.nrows))
        
        #
        # Grilles d'évaluation projet
        #
        sh_g = wb.sheet_by_name(u"Grille_PRJ")
        self.grilles_prj = {}
        self.nomParties_prj = {}
        for l in range(2,4):
            if sh_g.cell(l,0).value != u"":
                self.grilles_prj[sh_g.cell(l,0).value] = sh_g.cell(l,2).value
                self.nomParties_prj[sh_g.cell(l,0).value] = sh_g.cell(l,1).value
                
        self.cellulesInfo_prj = {}
        for l in range(7,sh_g.nrows):
            if sh_g.cell(l,0).value != u"":
                self.cellulesInfo_prj[sh_g.cell(l,0).value] = [sh_g.cell(l,1).value, (sh_g.cell(l,2).value, sh_g.cell(l,3).value)]
        
        
    def completer(self):
        """ Complète les données selon que le référentiel ait un tronc commun ou des options
        """
        
        ###########################################################
        def aplatir(dic, niv=1):
            ddic = {}
            for k0, v0 in dic.items():
                for k1, v1 in v0[1].items():
                    ddic[k1] = [v1[0]]
                    if type(v1[1]) == dict:
                        ddic[k1].extend(v1[1].values())
            return ddic
        
        if self.tr_com:
            t = self.tr_com[0]
            if t in REFERENTIELS.keys():
                self.dicPoidsIndicateurs_prj.update(REFERENTIELS[t].dicPoidsIndicateurs_prj)
                self.dicCompetences_prj.update(REFERENTIELS[t].dicCompetences_prj)
                self.dicIndicateurs_prj.update(REFERENTIELS[t].dicIndicateurs_prj)
        
        if self.projet:
            self.lstGrpIndicateurRevues = []
            self.lstGrpIndicateurSoutenance = []
            for grp, poids in self.dicPoidsIndicateurs_prj.items():
                poidsGrp, dicIndicGrp = poids
                for comp, poidsIndic in dicIndicGrp.items():
                    if comp in self.dicIndicateurs_prj.keys():
                        for i, indic in enumerate(self.dicIndicateurs_prj[comp]):
                            if self.dicIndicateurs_prj[comp][i][1]:
                                self.lstGrpIndicateurRevues.append(grp)
                            else:
                                self.lstGrpIndicateurSoutenance.append(grp)
                                
            self.lstGrpIndicateurSoutenance = list(set(self.lstGrpIndicateurSoutenance))
            self.lstGrpIndicateurRevues = list(set(self.lstGrpIndicateurRevues))
            if "O8s" in self.lstGrpIndicateurSoutenance:
                self.lstGrpIndicateurSoutenance.remove("O8s")
                self.lstGrpIndicateurSoutenance.append("O8")
        
            if self.tr_com:
                self.grilles_prj.update(REFERENTIELS[self.tr_com[0]].grilles_prj)
                
                
        self.dicCompetences_prj_simple = aplatir(self.dicCompetences_prj)
        
        
        
#        self.dicIndicateurs_prj_simple = {}
#        for c, d in self.dicIndicateurs_prj.items():
#            self.dicIndicateurs_prj_simple[c] =(d[1])
        
    
    
    
    def getSavoir(self, code, dic = None, c = 1, gene = None):
        print "getSavoir", code, dic
        if dic == None:
            if gene == "M":
                dic = self.dicSavoirs_Math
            elif gene == "P":
                dic = self.dicSavoirs_Phys
            else:
                dic = self.dicSavoirs
    #    print dic
    #    if c == None:
    #        c = len(code.split("."))
    #        c = 1
        if dic.has_key(code):
            return dic[code][0]
        else:
    #        cd = code[:-2*(c-1)]
    #        cd = ".".join(code.split(".")[:c-1])
            cd = ".".join(code.split(".")[:c])
    #        print "  ", cd
    #        return getSavoir(typeEns, code, dic[cd][1], c-1)
            return self.getSavoir(code, dic[cd][1], c+1)
        
        
    # Pour obtenir l'intitulé d'une compétence à partir de son code 
    #        fonction recursive    
    def getCompetence(self, code, dic = None, c = None):
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
                    

#########################################################################################
def getEnseignementLabel(label):
    """ Renvoie le code et la famille d'enseignement
        à partir de son label
    """
    for r in REFERENTIELS.values():
        if r.Enseignement[0] == label:
            return r.Code, r.Famille


#########################################################################################
DOSSIER_REF = "referentiels"
REFERENTIELS = {}
def chargerReferentiels():
    global REFERENTIELS
    liste = os.listdir(os.path.join(constantes.PATH, r"..", DOSSIER_REF))
    
    for fich_ref in liste:
        ref = Referentiel(os.path.join(constantes.PATH, r"..", DOSSIER_REF, fich_ref))
        REFERENTIELS[ref.Code] = ref
        

chargerReferentiels()

for r in REFERENTIELS.values():
    r.completer()
    print "*********************"
    print r.Code
    print "CI  :", r.CentresInterets
    print "Sav :", r.dicSavoirs
    print "Com :", r.dicCompetences
    print "CoP :", r.dicCompetences_prj
    print "CoS :", r.dicCompetences_prj_simple
    print "Ind :", r.dicIndicateurs_prj
    print "Poi :", r.dicPoidsIndicateurs_prj
    print "Mat :", r.dicSavoirs_Math
    print "Phy :", r.dicSavoirs_Phys
    print "Dem :", r.demarches
    print "Act :", r.activites
    print "Sea :", r.seances
    print "DeS :", r.demarcheSeance
    
    print


