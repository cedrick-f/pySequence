#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 24 oct. 2011

@author: jc
"""

import xlrd

# ouverture du fichier Excel 
wb = xlrd.open_workbook('CI_savoirs.xls')
 
# feuilles dans le classeur
[u'Feuil1', u'Feuil2', u'Feuil3']
 
# lecture des donn�es dans la premiere feuille
sh = wb.sheet_by_name(u'Feuil1')

#[u'id', u'x', u'y', u'test']
#[1.0, 235.0, 424.0, u'a']
#[2.0, 245.0, 444.0, u'b']
#[3.0, 255.0, 464.0, u'c']
#[4.0, 265.0, 484.0, u'd']
#[5.0, 275.0, 504.0, u'e']
#[6.0, 285.0, 524.0, u'f']
#[7.0, 295.0, 544.0, u'g']
 
# lecture par colonne
colonne1 = sh.col_values(0)
[u'id', 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
 
colonne2=sh.col_values(1)
[u'x', 235.0, 245.0, 255.0, 265.0, 275.0, 285.0, 295.0]

colonne3=sh.col_values(2)
[u'x', 235.0, 245.0, 255.0, 265.0, 275.0, 285.0, 295.0]
 
# extraction d'un �l�ment particulier
#numéro de colonne et numéro de ligne entre crochet
print colonne1[0],colonne3[2]

