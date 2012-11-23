#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 24 oct. 2011

@author: jc
"""

#import du module permettant la liaison avec excel
#import xlrd
import win32com.client
import wx
#import excel

xl = None
def lancerExcel():
    global xl
    xl = win32com.client.Dispatch("Excel.Application")
    


def ouvrirFichierExcel(nomFichier = None):
    if xl == None:
        lancerExcel()
    
#    print xl.ActiveWorkbook
    if xl.ActiveWorkbook == None:
        mesFormats = u"Classeur Excel (.xls)|*.xls|" \
                           u"Tous les fichiers|*.*'"
      
        if nomFichier == None:
            dlg = wx.FileDialog(
                                None, message=u"Ouvrir un classeur Excel",
    #                                defaultDir = self.DossierSauvegarde, 
                                defaultFile = "",
                                wildcard = mesFormats,
                                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                                )
            
            if dlg.ShowModal() == wx.ID_OK:
                paths = dlg.GetPaths()
                nomFichier = paths[0]
            else:
                nomFichier = ''
            
            dlg.Destroy()
    
        if nomFichier != '':
            wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
            xl.Workbooks.Open(nomFichier)
            xl.Visible = 1
            wx.EndBusyCursor()
            return True
        else:
            return False
    return True


def getSelectionExcel():
    return xl.Selection()
#    return xl.ActiveCell()
#    return xl.ActiveWorkbook.ActiveSheet.ActiveCell()

def getColonne(sel = None, c = None, close = True):
    """ Renvoie les colonnes (ou seulement la colonne <c>
        depuis une selection dans une feuille Excel
    """
    if sel == None:
        sel = getSelectionExcel()
    if sel != None:
        if c == None:
            lst = zip(*sel) 
        else:
            lst = zip(*sel)[c]
    else:
        lst = None
    if close:
        xl.ActiveWorkbook.Close(SaveChanges=0)
         
        

## ouverture du fichier Excel 
#wb = xlrd.open_workbook('CI_savoirs.xls')
# 
## lecture des donnï¿½es dans les feuilles
#sh1 = wb.sheet_by_name(u'Feuil1')
#
## lecture par colonne feuil1
#f1colonne2 = sh1.col_values(1)
#
#CI = ['CI1','CI2','CI3','CI4','CI5','CI6','CI7','CI8','CI9','CI10','CI11','CI12','CI13','CI14','CI15']
## Cellule de dÃ©part D7(excel) - col3 lig6(python)
#Numcol = 3
#for n in range (1,14,1): # boucle sur colonnes
#    CI[n] = []
#    for Numlign in range(6,124,1): # boucle sur lignes
#        if sh1.col_values(Numcol)[Numlign] == 1 :
#            CI[n].append(f1colonne2[Numlign])
#    Numcol = Numcol + 1
#       
#premiere_col = 3 
#premiere_lig = 7
#nbr_lig = 117
#def get_savoir(ci):
#    lst = []
#    for Numlign in range(nbr_lig): # boucle sur nbr_lig lignes
#        if sh1.col_values(premiere_col+ci-1)[premiere_lig+Numlign] != "" :
#            lst.append(f1colonne2[premiere_lig+Numlign])
#    
#    return lst
#
#print get_savoir(3)
##print CI[1]
##print CI[2]
##print CI[3]





    
    