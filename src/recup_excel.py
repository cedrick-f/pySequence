#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 24 oct. 2011

@author: jc
"""

import xlrd

# ouverture du fichier Excel 
wb = xlrd.open_workbook('CI_savoirs.xls')
 
# lecture des donn�es dans la premiere feuille
sh = wb.sheet_by_name(u'Feuil1')

# lecture par colonne
colonne1 = sh.col_values(0)
 
colonne2=sh.col_values(1)

colonne3=sh.col_values(2)

 
# extraction d'un �l�ment particulier
#numéro de colonne et numéro de ligne entre crochet
print colonne1[0],colonne3[2]

