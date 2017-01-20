#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                  grilles                                ##
##             génération des grilles d'évaluation des projets             ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2012 Cédrick FAURY - Jean-Claude FRICOU

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

# Dossier contenant les grilles
from util_path import TABLE_PATH, toFileEncoding

# Caractère utilisé pour cocher les cases :
COCHE = u"X"

# Module utilisé pour accéder au classeur Excel
# (Windows seulement)
import sys
if sys.platform == "win32":         
    import win32com.client.dynamic#win32com.client, 

# Autre module (essai en cours)
import xlwt
from xlwt import Workbook


import os
from widgets import messageErreur


def getFullNameGrille(fichier):
    return os.path.join(TABLE_PATH, toFileEncoding(fichier))


def ouvrirXLS(fichier):
    """ Ouvre la grille XLS nommée <fichier>
        renvoie le classeur PyExcel
    """
    fichierPB = []      # Liste des fichiers dont l'ouverture aura échoué
    fichier = getFullNameGrille(fichier)
    tableau = None
    err = 0
    
    if os.path.isfile(fichier):
        try:
            tableau = PyExcel(fichier)
        except:
            err = 1
    else:
        err = 2
        fichierPB.append(fichier)
        
    return tableau, err, fichierPB
    


def getTableau(parent, nomFichier):
    """ Ouvre et renvoie le classeur
        contenant la grille d'évaluation
    """

    tableau, err, fichierPB = ouvrirXLS(nomFichier)
                                      
    #
    # Gestion des éventuelles erreurs
    #
    if err == 0:
        return tableau
    
    elif err&1 != 0:
        messageErreur(parent, u"Lancement d'Excel impossible !",
                      u"L'application Excel ne semble pas installée !")
        
#    elif err&2 != 0:
#        messageErreur(parent, u"Fichier non trouvé !",
#                      u"Le fichier original de la grille,\n    " + fichierPB[0] + u"\n" \
#                      u"n'a pas été trouvé ! \n")
        
    else:
        print "Erreur", err


import threading


def getExentionExcel():
    global EXT_EXCEL
    import pythoncom
    pythoncom.CoInitialize()
    try:
        xlApp = win32com.client.Dispatch('Excel.Application')
        print xlApp,
    except :
        print "pas Excel"
        return
    
    if xlApp.Version < 12:
        EXT_EXCEL = ".xls"
    else:
        EXT_EXCEL = ".xlsx"
    
    
    del xlApp       # Parfois très lent, d'où le thread ...

    print EXT_EXCEL


EXT_EXCEL = None
try:
#     EXT_EXCEL = getExentionExcel()
    a = threading.Thread(None, getExentionExcel, None)
    a.start()
    
except:
    EXT_EXCEL = None # ya pas Excel !



def getTableaux(parent, doc):
    """ Ouvre et renvoie les classeurs 
        contenant les grilles d'évaluation : revues + soutenance
    """
    typ = doc.GetTypeEnseignement()
    ref = doc.GetReferentiel()
    prj = doc.GetProjetRef()
    fichiers = prj.grilles
#    print "grilles :", fichiers
    fichierPB = []
    
    def ouvrir(fichier):
        fichier = os.path.join(TABLE_PATH, toFileEncoding(fichier))
        tableau = None
        err = 0
        
        if os.path.isfile(fichier):
            try:
                tableau = PyExcel(fichier)
            except:
                err = 1
        else:
            err = 2
            fichierPB.append(fichier)
            
        return err, tableau
    
    tableaux = {}
    ff = r""
    for k, f in fichiers.items():
        nomFichier = f[0]
        if nomFichier != ff:
            if EXT_EXCEL != os.path.splitext(nomFichier)[1]:
                nomFichier = os.path.splitext(nomFichier)[0] + EXT_EXCEL
            err, tableaux[k] = [ouvrir(nomFichier), f[1]]
    
#    if typ == 'SSI':
#        err, tableau = ouvrir(fichiers[0])
#        if err != 0:
#            err, tableau = ouvrir(fichiers[1])
#    else:
#        errR, tableauR = ouvrir(fichiersR[0])
#        if errR != 0:
#            errR, tableauR = ouvrir(fichiersR[1])
#        errS, tableauS = ouvrir(fichiersS[0])
#        if errS != 0:
#            errS, tableauS = ouvrir(fichiersS[1])
#        err = errR + errR
#        tableau = [tableauR, tableauS]
        
    if err == 0:
        return tableaux
    elif err&1 != 0:
        messageErreur(parent, u"Lancement d'Excel impossible !",
                      u"L'application Excel ne semble pas installée !")
    elif err&2 != 0:
        messageErreur(parent, u"Fichier non trouvé !",
                              u"Le fichier original de la grille,\n    " + fichierPB[0] + u"\n" \
                              u"n'a pas été trouvé ! \n")
    else:
        print "Erreur", err


def modifierGrille(doc, tableaux, eleve):
#    print "modifierGrille", eleve
    
    log = []
    ref = doc.GetReferentiel()
    prj = doc.GetProjetRef()
    
    #
    # On coche les cellules "non" (uniquement grilles "Revues" STI2D)
    #     
    for part, grille in prj.grilles.items():
        dicInfo = prj.cellulesInfo[part]
        if part in ref.aColNon.keys() and ref.aColNon[part]:
            feuilNON = dicInfo["NON"][0][0]
            dicIndic = eleve.GetDicIndicateurs()
            dicNon = doc.GetProjetRef()._dicoIndicateurs_simple['S']
#            print dicInfo["NON"]
            colNON = dicInfo["NON"][0][1][1]
            
            # On rajoute la feuille du cadidat si elle n'existe pas encore
            if grille[1] == 'C': # fichier "Collectif"
                feuille = feuilNON+str(eleve.id+1)
            else:
                feuille = feuilNON
            
            for i, indics in dicNon.items():
#                print "   ", indics
                lignes = [ind.ligne[part] for ind in indics if part in ind.ligne.keys() and ind.ligne[part] != 0]
#                 print "keys", part, dicIndic.keys() 
                for j, ligne in enumerate(lignes):
#                     print "    ", i
                    # indic = l'indicateur "i" doit être évalué
                    if 'S'+i in dicIndic.keys():
                        indic = dicIndic['S'+i][j]
                    else:
                        indic = False
                    if part in tableaux.keys() and tableaux[part] != None:
                        if feuille in tableaux[part].getSheets():
                            nf = tableaux[part].getSheetNum(feuille)
                            if not indic: # indicateur pas évalué --> on coche NON !
                                tableaux[part].setCell(nf, ligne, colNON, COCHE)
                            else:
                                tableaux[part].setCell(nf, ligne, colNON, '')
                        else:
                            log.append(u"Feuille " + feuille + u" non trouvée")
                            
    

    #
    # On rajoute quelques informations
    #
    schem = {"Tit" : doc.intitule,
             "Des" : doc.intitule + "\n" + doc.problematique,
             "Nom" : eleve.GetNom(),
             "Pre" : eleve.GetPrenom(),
             "Etab": doc.classe.etablissement,
             "N-P" : eleve.GetNomPrenom(),
             "Sess": str(doc.annee+1)
             }

    
    for ct, t in tableaux.items():
        dicInfo = prj.cellulesInfo[ct]
#        print "  ", dicInfo
#        print "  ", ct, t
        for k, v in schem.items():
            if k in dicInfo.keys() and t != None:
#                print "    ", k
                for d in dicInfo[k]:
                    f = d[0]   # Feuille
                    if f in t.getSheets():
                        nf = t.getSheetNum(f)
                        l, c, p = d[1] # ligne , colonne
                        pre = d[2]
                        if p > 0: # Période - pour classeurs collectifs
                            l += eleve.id * p
                        t.setCell(nf, l, c, pre+v)
                    else:
                        log.append(u"Feuille " + f + u" non trouvée")
    
    #
    # On rajoute les noms des professeurs
    #
    for part, grille in prj.grilles.items():
        dicInfo = prj.cellulesInfo[part]
        if "Prof" in dicInfo.keys() and part in tableaux.keys() and tableaux[part] != None:
            f, lcp , pre = dicInfo["Prof"][0] 
            l, c, p = lcp # ligne, colonne, période
            if grille[1] == 'C': # fichier "Collectif"
                f = f+str(eleve.id+1)
            if f in tableaux[part].getSheets():
                nf = tableaux[part].getSheetNum(f)
                profs = [pr.GetNomPrenom() for pr in doc.equipe]
                for i in range(5):
                    try:
                        if i < len(profs):
                            tableaux[part].setCell(nf, l, c, profs[i])
                        else:
                            tableaux[part].setCell(nf, l, c, '')
                    except:
                        pass
#                        log.append(u"Impossible d'écrire dans la cellule "\
#                                   + part + str(nf) + " " + str(l) + " " + str(c))
                    l += p
            else:
                log.append(u"Feuille " + f + u" non trouvée")
        
        if "EtabPrf" in dicInfo.keys() and part in tableaux.keys() and tableaux[part] != None:
            f, lcp , pre = dicInfo["EtabPrf"][0] 
            l, c, p = lcp # ligne, colonne, période
            if grille[1] == 'C': # fichier "Collectif"
                f = f+str(eleve.id+1)
            if f in tableaux[part].getSheets():
                nf = tableaux[part].getSheetNum(f)
                profs = [doc.classe.etablissement for pr in doc.equipe]
                for i in range(5):
                    try:
                        if i < len(profs):
                            tableaux[part].setCell(nf, l, c, profs[i])
                        else:
                            tableaux[part].setCell(nf, l, c, '')
                    except:
                        pass
#                        log.append(u"Impossible d'écrire dans la cellule "\
#                                   + part + str(nf) + " " + str(l) + " " + str(c))
                    l += p
            else:
                log.append(u"Feuille " + f + u" non trouvée")
                
#    print "log",log
    return list(set(log))
    
    
    


###############################################################################################################################
import shutil

def copierClasseurs(doc, nomFichiers):
#    typ = doc.GetTypeEnseignement()
#    ref = doc.GetReferentiel()
    prj = doc.GetProjetRef()
    fichiers = prj.grilles
    
#    fichierPB = []
    
    for k, f in fichiers.items():
        shutil.copyfile(os.path.join(TABLE_PATH, toFileEncoding(f[0])), toFileEncoding(nomFichiers[k]))

#    err = 0
#    if err == 0:
#        return
#    elif err&1 != 0:
#        messageErreur(None, u"Ouverture d'Excel impossible !",
#                      u"L'application Excel ne semble pas installée !")
#    elif err&2 != 0:
#        messageErreur(None, u"Fichier non trouvé !",
#                              u"Le fichier original de la grille,\n    " + fichierPB[0] + u"\n" \
#                              u"n'a pas été trouvé ! \n")
#    else:
#        print "Erreur", err



#from xlrd import open_workbook
#def modifierGrille2(doc, nomFichiers, eleve):
#    """
#    """
#    #
#    # On renseigne quelques informations
#    #
#    dicInfo = doc.GetReferentiel().cellulesInfo_prj
#
#    schem = {"Tit" : doc.intitule,
#             "Des" : doc.intitule + "\n" + doc.problematique,
#             "Nom" : eleve.GetNom(),
#             "Pre" : eleve.GetPrenom(),
#             "Etab": doc.classe.etablissement,
#             "N-P" : eleve.GetNomPrenom()
#             }
#    
#    for c, nf in nomFichiers.items():
#        wb = open_workbook(nf)
#        sh = wb.sheet_by_index(0)
#        for k, v in schem.items():
#            if k in dicInfo.keys():
#                l,c = dicInfo[k][1]
#                sh.write(l-1, c-1, v)
#                
#    wb.save()
        
    
xlTypePDF = 0
xlQualityStandard = 0
xlLandscape = 1

class PyExcel:
    def __init__(self,filename=None):
        self.xlApp = win32com.client.dynamic.Dispatch('Excel.Application')  # voir aussi avec DispatchEx ? ou bien win32com.client.gencache.EnsureDispatch("Excel.Application")
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename=''
        self.xlBook.Application.DisplayAlerts = False

    def save(self, newfilename=None, ConflictResolution = 1):
        if newfilename:
            self.filename = newfilename
            self.xlBook.SaveAs(newfilename, ConflictResolution = ConflictResolution)
        else:
            self.xlBook.Save()
 
    def save_pdf(self, nomFichier, orientation = xlLandscape):
        ws = self.xlBook.ActiveSheet
#        ws.PageSetup.Orientation = orientation
        ws.ExportAsFixedFormat(Type = xlTypePDF, 
                               Filename=nomFichier, 
                               Quality=xlQualityStandard,
                               IncludeDocProperties=True,
                               IgnorePrintAreas= False,
                               OpenAfterPublish=False)
        
        
        
    def close(self):
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp
 
    def show(self):
        self.xlApp.Visible=1
 
    def hide(self):
        self.xlApp.Visible=0
 
    def getCell(self, sheet, row, col):
        sht = self.xlBook.Worksheets(sheet)
        return sht.Cells(row, col).Value
 
    def setCell(self, sheet, row, col, value):
        sht = self.xlBook.Worksheets(sheet)
        sht.Cells(row, col).Value = value
        
    def setLink(self, sheet, row, col, value):
        sht = self.xlBook.Worksheets(sheet)
        hl = sht.Cells(row, col).Hyperlinks
        hl.Add(sht.Cells(row, col), value)
 
    def getRange(self, sheet, row1, col1, row2, col2):
        sht = self.xlBook.Worksheets(sheet)
        return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value
 
    def setRange(self, sheet, leftCol, topRow, data):
        bottomRow = topRow + len(data) - 1
        rightCol = leftCol + len(data[0]) - 1
        sht = self.xlBook.Worksheets(sheet)
        sht.Range(
            sht.Cells(topRow, leftCol), 
            sht.Cells(bottomRow, rightCol)
            ).Value = data
 
    def getContiguousRange(self, sheet, row, col):
        sht = self.xlBook.Worksheets(sheet)
        # trouve la ligne du bas
        bottom = row
        while sht.Cells(bottom + 1, col).Value not in [None, '']:
            bottom = bottom + 1
        #trouve la col de droite
        right = col
        while sht.Cells(row, right + 1).Value not in [None, '']:
            right = right + 1
        return sht.Range(sht.Cells(row, col), sht.Cells(bottom, right)).Value
 
    def getActiveCell(self):
        r=self.xlApp.ActiveCell
        return r
 
    def mergeCells(self,sheet,row1,col1,row2,col2):
        sht = self.xlBook.Worksheets(sheet)
        sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Merge()
 
    def addSheet(self,Before='',After=''):
        if Before :
            pos=self.xlBook.Worksheets(Before)
            print self.xlBook.Worksheets.Add(Before=pos)
        elif After:
            pos=self.xlBook.Worksheets(After)
            print self.xlBook.Worksheets.Add(After=pos)
        else:
            print self.xlBook.Worksheets.Add()
            
    def addSheetName(self, name, Before='', After=''):
        self.renameSheet(self.addSheet(Before = Before, After = After), name)
        
    def getActiveSheet(self):
        sheet=self.xlBook.ActiveSheet.Name
        return sheet
 
    def setActiveSheet(self,sheet):
        sht = self.xlBook.Worksheets(sheet)
        sht.Activate()
 
    def delSheet(self,sheet):
        sht = self.xlBook.Worksheets(sheet)
        self.xlApp.DisplayAlerts = False
        sht.Delete()
        self.xlApp.DisplayAlerts = True
 
    def renameSheet(self,sheet,newName):
        sht = self.xlBook.Worksheets(sheet)
        sht.Name=newName
 
    def moveSheet(self,sheet,Before='',After=''):
        sht = self.xlBook.Worksheets(sheet)
        if Before :
            pos=self.xlBook.Worksheets(Before)
            sht.Move(Before=pos)
        else:
            pos=self.xlBook.Worksheets(After)
            sht.Move(After=pos)
 
    def getSheets(self):
        lstSheets=[sheet.Name for sheet in self.xlBook.Worksheets]
        return lstSheets
 
    def getSheetNum(self, nom):
        return self.getSheets().index(nom)+1
    
    def copySheet(self,sheet,Before='',After=''):
        sht = self.xlBook.Worksheets(sheet)
        if Before :
            pos=self.xlBook.Worksheets(Before)
            newSht=sht.Copy(pos, None)
        elif After:
            pos=self.xlBook.Worksheets(After)
            newSht=sht.Copy(None, pos)
        else:
            newSht=sht.Copy(None, sht)
 
    def setBorder(self,sheet,row1,col1,row2,col2,weight):
        sht = self.xlBook.Worksheets(sheet)
        ran=sht.Range(sht.Cells(row1,col1),sht.Cells(row2,col2))
        ran.Borders.Weight=weight
        
        
    def setColor(self,sheet,row,col,color):
        sht = self.xlBook.Worksheets(sheet)
        print sht.Cells(row, col).Interior.ColorIndex
        # Feuille vérrouillé : modification impossible !
        #sht.Cells(row, col).Interior.ColorIndex = color
 
    def insertPasteCol(self, sheet, col):
        sht = self.xlBook.Worksheets(sheet)
        c = sht.Columns(col).EntireColumn
        c.Copy()
        c = sht.Columns(col+1).EntireColumn
        c.Insert()

# https://mail.python.org/pipermail/python-win32/2008-January/006676.html

#class PyOOo(object):
#
#    wdReplaceNone=0
#    wdReplaceOne=1
#    wdReplaceAll=2
#    wdFindContinue=1
#
#    #pour close/save :
#    wdDoNotSaveChanges=0
#    wdSaveChanges=-1
#
#    wdCharacter=1
#    wdCell=12
#    wdLine=5
#
#    wdAlignLeft=0
#    wdAlignCenter=1
#    wdAlignRight=2
#
#
#
#    def __init__(self, fichier=None, visible=True):
#        self.objServiceManager = win32com.client.Dispatch("com.sun.star.ServiceManager")
#
#        #self.propert=self.objServiceManager.Bridge_GetStruct("com.sun.star.beans.PropertyValue")
#
#        self.w = self.objServiceManager.CreateInstance("com.sun.star.frame.Desktop")
#
#        if fichier!=None:
#            time.sleep(1)
#            self.open(fichier, visible)
#
#
#    def u1252(self, chu):
#        try:
#            if type(chu) is unicode:
#                return chu.encode('cp1252','replace')
#            else:
#                return chu
#        except:
#            return repr(chu)
#
#
#    def open(self, fichier, visible=True):
#        """Ouvre un document word
#        """
#        self.doc=self.w.loadComponentFromURL("file:///"+fichier, "_blank", 0, [])
#        #self.visible(visible)
#
#
#    def wnew(self, visible=True):
#        """Nouveau document writer
#        """
#        self.doc=self.w.loadComponentFromURL("private:factory/swriter", "_blank", 0, [])
#        self.visible(True)
#
#
#    def close(self):
#        """ferme le document, en sauvegardant, sans demander
#        """
#        #---
#        print"close"
#        self.w.store()
#        self.w.Terminate(1)
#
#
#    def docclose(self):
#        """ferme le document, en sauvegardant, sans demander
#        """
#        self.doc.Close(True)  #True ?  False ?
#
#
#    def saveas(self,fichier, typ=0):
#        """Appel de 'Enregistrer sous', avec le nom du fichier
#        """#---
#        self.doc.storeAsURL("file:///"+fichier, [])
#
#
#    def savepdf(self):
#
#        def createStruct(nom):
#            objCoreReflection= self.objServiceManager.createInstance("com.sun.star.reflection.CoreReflection")
#            classSize = objCoreReflection.forName(nom)
#            aStruct=[1,2]
#            classSize.createObject(aStruct)
#            return aStruct
#
#        par=createStruct("com.sun.star.beans.PropertyValue")
#        par.append([])
#        par[0].Name = "URL"
#        par[0].Value = "file:///C:/let01.odt"
#
#        par=["FilterName", "writer_pdf_Export"]
#        self.prop = self.objServiceManager.CreateInstance("com.sun.star.beans.PropertyValue")
#        self.prop[0].Name = "URL"
#        self.prop[0].Value = "file:///C:/let01.odt"
#        self.prop[1].Name = "FilterName"
#        self.prop[1].Value = "writer_pdf_Export"
#        self.doc.storeAsURL("file:///C:/let01.pdf", self.prop)
#
#
#    def saveas2(self,fichier, typ=0):
#
#        def createStruct(nom):
#            objCoreReflection= self.objServiceManager.createInstance("com.sun.star.reflection.CoreReflection")
#            classSize = objCoreReflection.forName(nom)
#            aStruct=[]
#            classSize.createObject(aStruct)
#            return aStruct
#
#        #args1= self.objServiceManager.createInstance("com.sun.star.beans.PropertyValue")
#        #args1 = createStruct("com.sun.star.beans.NamedValue")
#        #print args1
#
#        print "Titre :",self.doc.getDocumentInfo()
#
#        args1=["file:///c:/titi.rtf"]
#
#        self.doc.storeAsURL("",0,args1)
#
#
#        """
#        #args1= 
#self.objServiceManager.createInstance("com.sun.star.beans.PropertyValue")
#        #dispatcher = 
#self.objServiceManager.createInstance('com.sun.star.frame.DispatchHelper')
#        args1=createStruct("com.sun.star.beans.PropertyValue")
#        print len(args1)
#        prop.Name='Pages'
#        prop.Value='3-5'
#        args[0]=prop
#
#        args1[0].Name = "URL"
#        args1[0].Value = "file:///c:/titi.rtf"
#        args1[1].Name = "FilterName"
#        args1[1].Value = "Rich Text Format"
#        args1[4].Name = "SelectionOnly"
#        args1[4].Value = true
#        """
#        #sel=self.doc.SaveAs("",0,args1)
#
#    def quit(self):
#        """Ferme OOoW
#        """
#        self.w.Terminate()
#
#
#    def quitSaveChange(self):
#        """Ferme OooW, en sauvant les changements
#        """
#        self.w.store()
#        self.w.Terminate()
#
#
#    def quitCancel(self):
#        """Ferme word, SANS sauver les changements
#        """
#        self.doc.storeAsURL("file:///C:/null__.odt", [])
#        self.w.Terminate()
#        os.remove("C:/null__.odt")
#
#
#    def visible(self, par=True):
#        """Rend Word visible (True), ou invisible (False) ; True par défaut
#        Note : c'est plus rapide en invisible
#        """
#        """
#        if par:
#            self.objServiceManager.Visible(True)
#        else:
#            self.objServiceManager.Visible=False
#        """
#        win = self.doc.CurrentController.Frame.ContainerWindow
#        if par:
#            win.Visible = True
#        else:
#            win.Visible = False
#
#
#    def hide(self):
#        """Cache Word
#        """
#        win = self.doc.CurrentController.Frame.ContainerWindow
#        win.Visible = False
#
#
#    def show(self):
#        """Montre la fenêtre
#        """
#        win = self.doc.CurrentController.Frame.ContainerWindow
#        win.Visible = True
#
#
#    def wprint(self):
#        """Imprime le document
#        """
#        warg=[]
#        self.doc.Print(warg)
#
#
#    def wprint2(self,printer='PDFCreator'):
#        """Imprime le document
#        """
#        warg=['Name','PDFCreator']
#        self.doc.Print(warg)
#
## prop.Name='Name'
## prop.Value='PDFCreator'
## args[2]=prop
#
#
#    def preview(self):
#        """Pré-visualise le document
#        """
#        self.doc.PrintPreview()
#
#
#    def previewclose(self):
#        """Ferme la prévisdualisation du document
#        """
#        self.doc.ClosePrintPreview()
#
#
#    def text(self, txt):
#        """Remplace le texte sélectionné, par le paramètre
#        """
#        newchaine=txt.replace('\n','\r')
#        self.position.Text = newchaine
#
#
#    def TypeText(self, chaine):
#        """ 'Tape' le texte à la position courante
#        """
#        self.position.TypeText(chaine)
#
#
#    def chExist(self, chaine):
#        """Cherche l'existence d'une chaine dans le document.
#        Retourne True ou False, selon le résultat.
#        """
#        och=self.doc.createSearchDescriptor()
#        och.SearchString=chaine
#        och.SearchWords = False  #mots entiers seulement ?
#        position=self.doc.findFirst(och)
#        if position:
#            return True
#        else:
#            return False
#
#
#    def macroRun(self, name):
#        """Lance la macro-word (VBA) 'name'
#        """
#        print "Non supporté _ àcf"
#        print "Non supporté _ àcf"
#        print "Non supporté _ àcf"
#
#
#    def language(self):
#        """Retourne la langue de Writer
#        """
#        print "Non supporté _ àcf"
#        print "Non supporté _ àcf"
#        print "Non supporté _ àcf"
#
#
#    def filterTxt(self):
#        """Interne - Convertit une sélection en texte
#        """
#        ss=self.u1252(self.doc.GetText().String)
#        ss=ss.replace(chr(7)+chr(13),'   ')
#        ss=ss.replace(chr(13),'\r\n')
#        ss=ss.replace(chr(7),' ')
#        ss=ss.replace(chr(9),'')
#        ss=ss.replace(chr(26),'')
#        return ss
#
#
#    def eSelAll(self):
#        """sélectionne, et retourne, tout le document
#        """
#        sel=self.doc.GetText()
#        return self.filterTxt()
#
#
#    def eSelWord(self, nb=1):
#        """étend la sélection aux nb mots à droite, et retourne la sélection
#        """
#        self.w.Selection.WordRightSel(self.wdWord, nb, self.wdExtend)
#        return self.filterTxt()
#
#
#    def eSelLine(self, nb=1):
#        """étend la sélection aux nb lignes en-dessous, et retourne la 
#            sélection
#        """
#        args2= self.doc.createInstance("com.sun.star.beans.PropertyValue")
#        args2[0].Name= "Count"
#        args2[0].Value= 1
#        args2[1].Name= "Select"
#        args2[1].Value= False
#
#        self.doc.GoDown("", 0, args2)
#        return self.filterTxt()
#
#
#    def eSelEndLine(self):
#        """étend la sélection jusqu'à la fin de la ligne, et retourne la 
#            sélection
#        """
#        self.w.Selection.EndKey(self.wdLine, self.wdExtend)
#        return self.filterTxt()
#
#
#    def chRemplAll(self, oldchaine, newchaine=''):
#        """
#        oldchaine = chaine a remplacer / string to replace
#        newchaine = chaine de remplacement / string for replace
#        """
#        orempl=self.doc.createReplaceDescriptor()
#        orempl.SearchString=oldchaine
#        orempl.ReplaceString=newchaine
#        orempl.SearchWords = False  #mots entiers seulement ?
#        orempl.SearchCaseSensitive = True    #sensible à la casse ?
#        nb = self.doc.replaceAll(orempl)
#
#
#    def chRemplLstAll(self, lst=[[]]):
#        """
#        oldchaine = chaine a remplacer / string to replace
#        newchaine = chaine de remplacement / string for replace
#        """
#        nb=0
#        for oldchaine, newchaine in lst:
#            orempl=self.doc.createReplaceDescriptor()
#            orempl.SearchString=oldchaine
#            orempl.ReplaceString=newchaine
#            orempl.SearchWords = False  #mots entiers seulement ?
#            orempl.SearchCaseSensitive = True    #sensible à la casse ?
#            nb += self.doc.replaceAll(orempl)
#
#
#    def chRemplOne(self, oldchaine, newchaine=''):
#        """
#        oldchaine = chaine a remplacer / string to replace
#        newchaine = chaine de remplacement / string for replace
#        """
#        sel = self.w.Selection
#        #sel.ClearFormatting()
#        sel.Find.Text = oldchaine
#        sel.Find.Forward = True
#        newchaine=newchaine.replace('\n','\r')
#        sel.Find.Execute(oldchaine,False,False,False,False,False,True,self.wdFindContinue,False,newchaine,self.wdReplaceOne)
#        self.position=sel
#
#
#    def chRemplClipboard(self, oldchaine):
#        """
#        oldchaine = chaine a remplacer / string to replace
#        """
#        sel = self.w.Selection
#        #sel.ClearFormatting()
#        sel.Find.Text = oldchaine
#        sel.Find.Forward = True
#
#        sel.Find.Execute(oldchaine,False,False,False,False,False,True,self.wdFindContinue,False,'XXX',self.wdReplaceOne)
#        sel.Paste()
#        self.position=sel
#
#
#    def chRemplGraf(self, oldchaine, fichier):
#        """
#        oldchaine = chaine a remplacer / string to replace
#        """
#        sel = self.w.Selection
#        #sel.ClearFormatting()
#        sel.Find.Text = oldchaine
#        sel.Find.Forward = True
#
#        sel.Find.Execute(oldchaine,False,False,False,False,False,True,self.wdFindContinue,False,'',self.wdReplaceOne)
#        sel.InlineShapes.AddPicture(fichier, False, True)
#        self.position=sel
#
#
#    def TableauInsLigApres(self, oldchaine, nblig=1):
#        """
#        oldchaine = chaine a remplacer / string to replace
#        """
#        sel = self.w.Selection
#        #sel.ClearFormatting()
#        sel.Find.Text = oldchaine
#        sel.Find.Forward = True
#
#        sel.Find.Execute(oldchaine,False,False,False,False,False,True,self.wdFindContinue,False,'',self.wdReplaceOne)
#        sel.InsertRowsBelow(nblig)
#
#
#    def TableauDelLig(self, oldchaine):
#        """
#        oldchaine = chaine a remplacer / string to replace
#        """
#        sel = self.w.Selection
#        #sel.ClearFormatting()
#        sel.Find.Text = oldchaine
#        sel.Find.Forward = True
#
#        sel.Find.Execute(oldchaine,False,False,False,False,False,True,self.wdFindContinue,False,'',self.wdReplaceOne)
#        sel.Rows.Delete()
#
#
#    def MoveRight(self, nb=1):
#        self.position.MoveRight(self.wdCharacter, nb)
#
#
#    def MoveLeft(self, nb=1):
#        self.position.MoveLeft(self.wdCharacter, nb)
#
#
#    def TableauMoveRight(self, nb=1):
#        sel = self.w.Selection
#        sel.MoveRight(self.wdCell, nb)
#
#
#    def TableauMoveLeft(self, nb=1):
#        sel = self.w.Selection
#        sel.MoveLeft(self.wdCell, nb)
#
#
#    def TableauMoveLine(self, nb=1):
#        sel = self.w.Selection
#        if nb>0:
#            sel.MoveDown(self.wdLine, nb)
#        else:
#            sel.MoveUp(self.wdLine, -nb)
#
#
#    def TableauCellule(self, lig=1, col=1, txt='', align=0):
#        tbl = self.doc.Tables[0]
#        cellule = tbl.Cell(lig, col)
#        cellule.Range.Text = txt
#        cellule.Range.ParagraphFormat.Alignment = align  #0,1,2, left, center, right
#
#
#    def landscape(self):
#        """Met le document en mode paysage
#        """
#        self.wdOrientLandscape=1
#        self.wdOrientPortrait=0
#        self.w.ActiveDocument.PageSetup.Orientation = self.wdOrientLandscape
#
#
#    def portrait(self):
#        """Met le document en mode portrait
#        """
#        self.wdOrientLandscape=1
#        self.wdOrientPortrait=0
#        self.w.ActiveDocument.PageSetup.Orientation = self.wdOrientPortrait
#
#
#    def changePrinter(self, printerName):
#        """Change l'imprimante active de Word
#        """
#        self.w.ActivePrinter = printerName

        
#def exporterGrille(typeDoc):
#    rb = xlrd.open_workbook(GRILLE[typeDoc])
#    wb = copy(rb)
#    l,c = Cellules_NON_SSI["B3"][0]
#    wb.get_sheet(1).write(l,c,'x')
#    
#    wb.save('output.xls')
#    
#exporterGrille('SSI')
    
    
#xlApp = win32com.client.dynamic.Dispatch('Excel.Application')
#print dir(xlApp)
#print xlApp.Version
    
    
    