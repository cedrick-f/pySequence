#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 24 oct. 2011

@author: jc
"""

#import du module permettant la liaison avec excel
import xlrd

# ouverture du fichier Excel 
wb = xlrd.open_workbook('CI_savoirs.xls')
 
# lecture des donn�es dans les feuilles
sh1 = wb.sheet_by_name(u'Feuil1')

# lecture par colonne feuil1
f1colonne2 = sh1.col_values(1)

CI = ['CI1','CI2','CI3','CI4','CI5','CI6','CI7','CI8','CI9','CI10','CI11','CI12','CI13','CI14','CI15']
# Cellule de départ D7(excel) - col3 lig6(python)
Numcol = 3
for n in range (1,14,1): # boucle sur colonnes
    CI[n] = []
    for Numlign in range(6,124,1): # boucle sur lignes
        if sh1.col_values(Numcol)[Numlign] == 1 :
            CI[n].append(f1colonne2[Numlign])
    Numcol = Numcol + 1
        
print CI[1]
print CI[2]
print CI[3]





    
    