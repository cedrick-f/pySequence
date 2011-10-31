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
f1colonne4 = sh1.col_values(3)
f1colonne2 = sh1.col_values(1)

#test sur une colonne (4)

m = []
for Numlign in range(9,124,1):
    if f1colonne4[Numlign] == 1 :
        m.append(f1colonne2[Numlign])
        
print m



    
    