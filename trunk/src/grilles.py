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


from constantes import Cellules_NON, Fichier_GRILLE, TABLE_PATH, dicIndicateurs

# Caractère utilisé pour cocher les cases :
COCHE = u"X"

############
#  Identification des indicateurs non évalués en ETT
############
Feuille_ETT = u"Soutenance"


Cellules_INFO_STI =  {"Tit" : (13,1),
                      "Des" : (13,1),
                      "Nom" : (8,2),
                      "Pre" : (9,2),
#                      "Pro" : (5,2)
                      }
 
Cellules_INFO_SSI =  {"Tit" : (12,1),
                      "Des" : (12,1),
                      "Nom" : (7,2),
                      "Pre" : (8,2),
#                      "Pro" : (5,2)
                      }

COL_REVUE = 10 # Colonne "J" pour désigner la revue

Cellules_NON  =  {'ITEC'   : [[Feuille_ETT, Cellules_NON['ET']], ['ITEC', Cellules_NON['ITEC']]], 
                  'AC'     : [[Feuille_ETT, Cellules_NON['ET']], ['AC', Cellules_NON['AC']]], 
                  'EE'     : [[Feuille_ETT, Cellules_NON['ET']], ['EE', Cellules_NON['EE']]], 
                  'SIN'    : [[Feuille_ETT, Cellules_NON['ET']], ['SIN', Cellules_NON['SIN']]],
                  'SSI'    : [['Notation', Cellules_NON['SSI']]]}    


# Module utilisé pour accéder au classeur Excel
# (Windows seulement)
import sys
if sys.platform == "win32":         
    import win32com.client.dynamic#win32com.client, 



import os
from widgets import messageErreur

def getTableau(parent, doc):
    typ = doc.GetTypeEnseignement()
    if typ == 'SSI':
        fichiers = Fichier_GRILLE[typ]
    else:
        fichiersR = Fichier_GRILLE[typ]
        fichiersS = Fichier_GRILLE['ET']
    
    fichierPB = []
    
    def ouvrir(fichier):
        fichier = os.path.join(TABLE_PATH, fichier)
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
    
    if typ == 'SSI':
        err, tableau = ouvrir(fichiers[0])
        if err != 0:
            err, tableau = ouvrir(fichiers[1])
    else:
        errR, tableauR = ouvrir(fichiersR[0])
        if errR != 0:
            errR, tableauR = ouvrir(fichiersR[1])
        errS, tableauS = ouvrir(fichiersS[0])
        if errS != 0:
            errS, tableauS = ouvrir(fichiersS[1])
        err = errR + errR
        tableau = [tableauR, tableauS]
        
    if err == 0:
        return tableau
    elif err&1 != 0:
        messageErreur(parent, u"Ouverture d'Excel impossible !",
                      u"L'application Excel ne semble pas installée !")
    elif err&2 != 0:
        messageErreur(parent, u"Fichier non trouvé !",
                              u"Le fichier original de la grille,\n    " + fichierPB[0] + u"\n" \
                              u"n'a pas été trouvé ! \n")
    else:
        print "Erreur", err


def modifierGrille(doc, tableur, eleve):
    print "modifierGrille"
    
   
    
    #
    # On coche les cellules "non"
    #     
    dic = Cellules_NON[doc.GetTypeEnseignement()]
    
    #clef = code compétence
    #valeur = liste [True False ...] des indicateurs à mobiliser
    dicIndic = eleve.GetDicIndicateurs()
#    print eleve.nom, dicIndic
    
    for feuille, cellules in dic:
        for comp, cells in cellules.items():
            for j, cell in enumerate(cells):
                
                # indic = l'indicateur "comp" doit être évalué
                if comp in dicIndic.keys():
                    indic = dicIndic[comp][j]
                else:
                    indic = False
                
                
                if not indic: # indicateur pas évalué --> on coche NON !
                    l, c = cell
#                    print feuille, l, c
                    if doc.GetTypeEnseignement() == 'SSI':
                        tableur.setCell(feuille, l, c, COCHE)
                    else:
                        if feuille == Feuille_ETT:
                            t = tableur[1]
                        else:
                            t = tableur[0]
                        t.setCell(2, l, c, COCHE)
                
#                else: # indicateur évalué --> on rempli la colonne "Revues" (J) !
#                    if doc.GetTypeEnseignement(simple = True) == "STI" and feuille != Feuille_ETT:
#                        l, c = cell
#                        c = COL_REVUE
#                        for r in eleve.parent.getTachesRevue()[:-1]:
#                            if comp+"_"+str(j+1) in r.indicateurs:
#                                tableur[0].setCell(2, l, c, r.phase[1])
#                    
#                    elif doc.GetTypeEnseignement(simple = True) == "SSI":
#                        l, c = cell
#                        c = COL_REVUE
#                        for r in eleve.parent.getTachesRevue()[:-1]:
#                            if comp+"_"+str(j+1) in r.indicateurs:
#                                tableur.setCell(2, l, c, r.phase[1])

    #
    # On rempli les cellules "Revue" (colonne J)
    #     
    dic = Cellules_NON[doc.GetTypeEnseignement()]
    
    if eleve.projet.nbrRevues == 2:
        lstRevues = ["R1", "R2"]
    else:
        lstRevues = ["R1", "R2", "R3"]
    #clef = code compétence
    #valeur = liste [True False ...] des indicateurs à mobiliser
    dicIndic = [eleve.GetDicIndicateurs(limite = r) for r in lstRevues]

#    print eleve.nom
    
    for feuille, cellules in dic:
        for comp, cells in cellules.items():
            for j, cell in enumerate(cells):
                for i, r in enumerate(lstRevues):
                    # indic = l'indicateur "comp" doit être évalué
#                    print dicIndic[i]
                    if comp in dicIndic[i].keys():
                        indic = dicIndic[i][comp][j]
                    else:
                        indic = False
                    rev = eleve.projet.getTachesRevue()[i]
#                    print rev
                    if indic: # indicateur évalué --> on rempli la colonne "Revues" (J) !
                        l, c = cell
                        c = COL_REVUE
                        if doc.GetTypeEnseignement(simple = True) == "STI" and feuille != Feuille_ETT:
                            if comp+"_"+str(j+1) in rev.indicateursEleve[eleve.id]:
                                tableur[0].setCell(2, l, c, str(i+1))
                                break
                        elif doc.GetTypeEnseignement(simple = True) == "SSI":
                            if comp+"_"+str(j+1) in rev.indicateursEleve[eleve.id]:
                                tableur.setCell(2, l, c,  str(i+1))
                                break
                    
#                if doc.GetTypeEnseignement(simple = True) == "SSI" and dicIndicateurs['SSI'][comp][j][1]:
#                    l, c = cell
#                    tableur.setColor(feuille, l, c, 5)

    #
    # On rajoute quelques informations
    #
    if doc.GetTypeEnseignement(simple = True) == "SSI":
        dicInfo = Cellules_INFO_SSI
        tb = [tableur]
    else:
        dicInfo = Cellules_INFO_STI
        tb = tableur
    
    for t in tb:
        l,c = dicInfo["Tit"]
        t.setCell(1, l, c, doc.intitule)
        
        l,c = dicInfo["Des"]
        t.setCell(1, l, c, doc.intitule + "\n" + doc.problematique)
        
        l,c = dicInfo["Nom"]
        t.setCell(1, l, c, eleve.GetNom())
        
        l,c = dicInfo["Pre"]
        t.setCell(1, l, c, eleve.GetPrenom())
    
#    l,c = Cellules_INFO_SSI["Pro"]
#    tableur.xlBook.Worksheets(1).Cells(l, c).Activate()
#    tableur.xlBook.Worksheets(1).Cells(l, c).Value2 = p.GetNomPrenom()
#    .Value2 = doc.equipe[0].GetNomPrenom()
        
#    for p in doc.equipe:
##        tableur.xlBook.Worksheets(1).Cells(l, c).Value2 = p.GetNomPrenom()
#        tableur.setCell(1, l, c, p.prenom)
#        l += 1


class PyExcel:
    def __init__(self,filename=None):
        self.xlApp = win32com.client.dynamic.Dispatch('Excel.Application')
        if filename:
                self.filename = filename
                self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
                self.xlBook = self.xlApp.Workbooks.Add()
                self.filename=''
 
    def save(self, newfilename=None):
        if newfilename:
                self.filename = newfilename
                self.xlBook.SaveAs(newfilename)
        else:
                self.xlBook.Save()
 
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
            self.xlBook.Worksheets.Add(Before=pos)
        elif After:
            pos=self.xlBook.Worksheets(After)
            self.xlBook.Worksheets.Add(After=pos)
        else:
            self.xlBook.Worksheets.Add()
 
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
        print ran
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

class PyOOo(object):

    wdReplaceNone=0
    wdReplaceOne=1
    wdReplaceAll=2
    wdFindContinue=1

    #pour close/save :
    wdDoNotSaveChanges=0
    wdSaveChanges=-1

    wdCharacter=1
    wdCell=12
    wdLine=5

    wdAlignLeft=0
    wdAlignCenter=1
    wdAlignRight=2



    def __init__(self, fichier=None, visible=True):
        self.objServiceManager = win32com.client.Dispatch("com.sun.star.ServiceManager")

        #self.propert=self.objServiceManager.Bridge_GetStruct("com.sun.star.beans.PropertyValue")

        self.w = self.objServiceManager.CreateInstance("com.sun.star.frame.Desktop")

        if fichier!=None:
            time.sleep(1)
            self.open(fichier, visible)


    def u1252(self, chu):
        try:
            if type(chu) is unicode:
                return chu.encode('cp1252','replace')
            else:
                return chu
        except:
            return repr(chu)


    def open(self, fichier, visible=True):
        """Ouvre un document word
        """
        self.doc=self.w.loadComponentFromURL("file:///"+fichier, "_blank", 0, [])
        #self.visible(visible)


    def wnew(self, visible=True):
        """Nouveau document writer
        """
        self.doc=self.w.loadComponentFromURL("private:factory/swriter", "_blank", 0, [])
        self.visible(True)


    def close(self):
        """ferme le document, en sauvegardant, sans demander
        """
        #---
        print"close"
        self.w.store()
        self.w.Terminate(1)


    def docclose(self):
        """ferme le document, en sauvegardant, sans demander
        """
        self.doc.Close(True)  #True ?  False ?


    def saveas(self,fichier, typ=0):
        """Appel de 'Enregistrer sous', avec le nom du fichier
        """#---
        self.doc.storeAsURL("file:///"+fichier, [])


    def savepdf(self):

        def createStruct(nom):
            objCoreReflection= self.objServiceManager.createInstance("com.sun.star.reflection.CoreReflection")
            classSize = objCoreReflection.forName(nom)
            aStruct=[1,2]
            classSize.createObject(aStruct)
            return aStruct

        par=createStruct("com.sun.star.beans.PropertyValue")
        par.append([])
        par[0].Name = "URL"
        par[0].Value = "file:///C:/let01.odt"

        par=["FilterName", "writer_pdf_Export"]
        self.prop = self.objServiceManager.CreateInstance("com.sun.star.beans.PropertyValue")
        self.prop[0].Name = "URL"
        self.prop[0].Value = "file:///C:/let01.odt"
        self.prop[1].Name = "FilterName"
        self.prop[1].Value = "writer_pdf_Export"
        self.doc.storeAsURL("file:///C:/let01.pdf", self.prop)


    def saveas2(self,fichier, typ=0):

        def createStruct(nom):
            objCoreReflection= self.objServiceManager.createInstance("com.sun.star.reflection.CoreReflection")
            classSize = objCoreReflection.forName(nom)
            aStruct=[]
            classSize.createObject(aStruct)
            return aStruct

        #args1= self.objServiceManager.createInstance("com.sun.star.beans.PropertyValue")
        #args1 = createStruct("com.sun.star.beans.NamedValue")
        #print args1

        print "Titre :",self.doc.getDocumentInfo()

        args1=["file:///c:/titi.rtf"]

        self.doc.storeAsURL("",0,args1)


        """
        #args1= 
self.objServiceManager.createInstance("com.sun.star.beans.PropertyValue")
        #dispatcher = 
self.objServiceManager.createInstance('com.sun.star.frame.DispatchHelper')
        args1=createStruct("com.sun.star.beans.PropertyValue")
        print len(args1)
        prop.Name='Pages'
        prop.Value='3-5'
        args[0]=prop

        args1[0].Name = "URL"
        args1[0].Value = "file:///c:/titi.rtf"
        args1[1].Name = "FilterName"
        args1[1].Value = "Rich Text Format"
        args1[4].Name = "SelectionOnly"
        args1[4].Value = true
        """
        #sel=self.doc.SaveAs("",0,args1)

    def quit(self):
        """Ferme OOoW
        """
        self.w.Terminate()


    def quitSaveChange(self):
        """Ferme OooW, en sauvant les changements
        """
        self.w.store()
        self.w.Terminate()


    def quitCancel(self):
        """Ferme word, SANS sauver les changements
        """
        self.doc.storeAsURL("file:///C:/null__.odt", [])
        self.w.Terminate()
        os.remove("C:/null__.odt")


    def visible(self, par=True):
        """Rend Word visible (True), ou invisible (False) ; True par défaut
        Note : c'est plus rapide en invisible
        """
        """
        if par:
            self.objServiceManager.Visible(True)
        else:
            self.objServiceManager.Visible=False
        """
        win = self.doc.CurrentController.Frame.ContainerWindow
        if par:
            win.Visible = True
        else:
            win.Visible = False


    def hide(self):
        """Cache Word
        """
        win = self.doc.CurrentController.Frame.ContainerWindow
        win.Visible = False


    def show(self):
        """Montre la fenêtre
        """
        win = self.doc.CurrentController.Frame.ContainerWindow
        win.Visible = True


    def wprint(self):
        """Imprime le document
        """
        warg=[]
        self.doc.Print(warg)


    def wprint2(self,printer='PDFCreator'):
        """Imprime le document
        """
        warg=['Name','PDFCreator']
        self.doc.Print(warg)

# prop.Name='Name'
# prop.Value='PDFCreator'
# args[2]=prop


    def preview(self):
        """Pré-visualise le document
        """
        self.doc.PrintPreview()


    def previewclose(self):
        """Ferme la prévisdualisation du document
        """
        self.doc.ClosePrintPreview()


    def text(self, txt):
        """Remplace le texte sélectionné, par le paramètre
        """
        newchaine=txt.replace('\n','\r')
        self.position.Text = newchaine


    def TypeText(self, chaine):
        """ 'Tape' le texte à la position courante
        """
        self.position.TypeText(chaine)


    def chExist(self, chaine):
        """Cherche l'existence d'une chaine dans le document.
        Retourne True ou False, selon le résultat.
        """
        och=self.doc.createSearchDescriptor()
        och.SearchString=chaine
        och.SearchWords = False  #mots entiers seulement ?
        position=self.doc.findFirst(och)
        if position:
            return True
        else:
            return False


    def macroRun(self, name):
        """Lance la macro-word (VBA) 'name'
        """
        print "Non supporté _ àcf"
        print "Non supporté _ àcf"
        print "Non supporté _ àcf"


    def language(self):
        """Retourne la langue de Writer
        """
        print "Non supporté _ àcf"
        print "Non supporté _ àcf"
        print "Non supporté _ àcf"


    def filterTxt(self):
        """Interne - Convertit une sélection en texte
        """
        ss=self.u1252(self.doc.GetText().String)
        ss=ss.replace(chr(7)+chr(13),'   ')
        ss=ss.replace(chr(13),'\r\n')
        ss=ss.replace(chr(7),' ')
        ss=ss.replace(chr(9),'')
        ss=ss.replace(chr(26),'')
        return ss


    def eSelAll(self):
        """sélectionne, et retourne, tout le document
        """
        sel=self.doc.GetText()
        return self.filterTxt()


    def eSelWord(self, nb=1):
        """étend la sélection aux nb mots à droite, et retourne la sélection
        """
        self.w.Selection.WordRightSel(self.wdWord, nb, self.wdExtend)
        return self.filterTxt()


    def eSelLine(self, nb=1):
        """étend la sélection aux nb lignes en-dessous, et retourne la 
            sélection
        """
        args2= self.doc.createInstance("com.sun.star.beans.PropertyValue")
        args2[0].Name= "Count"
        args2[0].Value= 1
        args2[1].Name= "Select"
        args2[1].Value= False

        self.doc.GoDown("", 0, args2)
        return self.filterTxt()


    def eSelEndLine(self):
        """étend la sélection jusqu'à la fin de la ligne, et retourne la 
            sélection
        """
        self.w.Selection.EndKey(self.wdLine, self.wdExtend)
        return self.filterTxt()


    def chRemplAll(self, oldchaine, newchaine=''):
        """
        oldchaine = chaine a remplacer / string to replace
        newchaine = chaine de remplacement / string for replace
        """
        orempl=self.doc.createReplaceDescriptor()
        orempl.SearchString=oldchaine
        orempl.ReplaceString=newchaine
        orempl.SearchWords = False  #mots entiers seulement ?
        orempl.SearchCaseSensitive = True    #sensible à la casse ?
        nb = self.doc.replaceAll(orempl)


    def chRemplLstAll(self, lst=[[]]):
        """
        oldchaine = chaine a remplacer / string to replace
        newchaine = chaine de remplacement / string for replace
        """
        nb=0
        for oldchaine, newchaine in lst:
            orempl=self.doc.createReplaceDescriptor()
            orempl.SearchString=oldchaine
            orempl.ReplaceString=newchaine
            orempl.SearchWords = False  #mots entiers seulement ?
            orempl.SearchCaseSensitive = True    #sensible à la casse ?
            nb += self.doc.replaceAll(orempl)


    def chRemplOne(self, oldchaine, newchaine=''):
        """
        oldchaine = chaine a remplacer / string to replace
        newchaine = chaine de remplacement / string for replace
        """
        sel = self.w.Selection
        #sel.ClearFormatting()
        sel.Find.Text = oldchaine
        sel.Find.Forward = True
        newchaine=newchaine.replace('\n','\r')
        sel.Find.Execute(oldchaine,False,False,False,False,False,True,self.wdFindContinue,False,newchaine,self.wdReplaceOne)
        self.position=sel


    def chRemplClipboard(self, oldchaine):
        """
        oldchaine = chaine a remplacer / string to replace
        """
        sel = self.w.Selection
        #sel.ClearFormatting()
        sel.Find.Text = oldchaine
        sel.Find.Forward = True

        sel.Find.Execute(oldchaine,False,False,False,False,False,True,self.wdFindContinue,False,'XXX',self.wdReplaceOne)
        sel.Paste()
        self.position=sel


    def chRemplGraf(self, oldchaine, fichier):
        """
        oldchaine = chaine a remplacer / string to replace
        """
        sel = self.w.Selection
        #sel.ClearFormatting()
        sel.Find.Text = oldchaine
        sel.Find.Forward = True

        sel.Find.Execute(oldchaine,False,False,False,False,False,True,self.wdFindContinue,False,'',self.wdReplaceOne)
        sel.InlineShapes.AddPicture(fichier, False, True)
        self.position=sel


    def TableauInsLigApres(self, oldchaine, nblig=1):
        """
        oldchaine = chaine a remplacer / string to replace
        """
        sel = self.w.Selection
        #sel.ClearFormatting()
        sel.Find.Text = oldchaine
        sel.Find.Forward = True

        sel.Find.Execute(oldchaine,False,False,False,False,False,True,self.wdFindContinue,False,'',self.wdReplaceOne)
        sel.InsertRowsBelow(nblig)


    def TableauDelLig(self, oldchaine):
        """
        oldchaine = chaine a remplacer / string to replace
        """
        sel = self.w.Selection
        #sel.ClearFormatting()
        sel.Find.Text = oldchaine
        sel.Find.Forward = True

        sel.Find.Execute(oldchaine,False,False,False,False,False,True,self.wdFindContinue,False,'',self.wdReplaceOne)
        sel.Rows.Delete()


    def MoveRight(self, nb=1):
        self.position.MoveRight(self.wdCharacter, nb)


    def MoveLeft(self, nb=1):
        self.position.MoveLeft(self.wdCharacter, nb)


    def TableauMoveRight(self, nb=1):
        sel = self.w.Selection
        sel.MoveRight(self.wdCell, nb)


    def TableauMoveLeft(self, nb=1):
        sel = self.w.Selection
        sel.MoveLeft(self.wdCell, nb)


    def TableauMoveLine(self, nb=1):
        sel = self.w.Selection
        if nb>0:
            sel.MoveDown(self.wdLine, nb)
        else:
            sel.MoveUp(self.wdLine, -nb)


    def TableauCellule(self, lig=1, col=1, txt='', align=0):
        tbl = self.doc.Tables[0]
        cellule = tbl.Cell(lig, col)
        cellule.Range.Text = txt
        cellule.Range.ParagraphFormat.Alignment = align  #0,1,2, left, center, right


    def landscape(self):
        """Met le document en mode paysage
        """
        self.wdOrientLandscape=1
        self.wdOrientPortrait=0
        self.w.ActiveDocument.PageSetup.Orientation = self.wdOrientLandscape


    def portrait(self):
        """Met le document en mode portrait
        """
        self.wdOrientLandscape=1
        self.wdOrientPortrait=0
        self.w.ActiveDocument.PageSetup.Orientation = self.wdOrientPortrait


    def changePrinter(self, printerName):
        """Change l'imprimante active de Word
        """
        self.w.ActivePrinter = printerName

        
#def exporterGrille(typeDoc):
#    rb = xlrd.open_workbook(GRILLE[typeDoc])
#    wb = copy(rb)
#    l,c = Cellules_NON_SSI["B3"][0]
#    wb.get_sheet(1).write(l,c,'x')
#    
#    wb.save('output.xls')
#    
#exporterGrille('SSI')
    
    
    
    
    
    