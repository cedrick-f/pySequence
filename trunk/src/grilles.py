#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               draw_cairo_prj                            ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2012 Cédrick FAURY

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

import wx
#import des modules permettant la liaison avec excel
#import xlrd
#import xlwt
#from xlutils.copy import copy

COCHE = u"X"

GRILLE ={'SSI' : "Grille_evaluation_SSI_projet.xls",
         'STI' : "Grille_evaluation_STI2D_projet.xls"
         }

Cellules_NON_SSI = {  "B3" : [(5,4), (6,4)],
                      "B4" : [(7,4), (8,4), (9,4), (10,4)],
                      "C1" : [(12,4), (13,4), (14,4), (15,4),  (16,4)],
                      "C2" : [(17,4), (18,4), (19,4), (20,4), (21,4), (22,4), (23,4)],
                      "D1" : [(25,4), (26,4), (27,4), (28,4)],
                      "D2" : [(29,4), (30,4), (31,4), (32,4)]
                    }

Cellules_INFO_SSI = {"Tit" : (12,1),
                     "Nom" : (7,2),
                     "Pro" : (43,1),
                     "Pre" : (8,2)}

############
#  Identification des indicateurs non évalués en ETT
############

Cellules_NON_ETT =  {"CO1.1" : [(5,3), (6,3), (7,3), (8,3), (9,3)],
                     "CO1.2" : [(10,3), (11,3), (12,3)],
                     "CO2.1" : [(14,3), (15,3), (16,3), (17,3)],
                     "CO2.2" : [(18,3), (19,3), (20,3), (21,3), (22,3)],
                     "CO6.1" : [(24,3), (25,3), (26,3)],
                     "CO6.2" : [(27,3), (28,3), (29,3)],
                     "CO6.3" : [(30,3), (31,3), (32,3), (33,3), (34,3)],
                     "CO8.es" : [(36,3), (37,3), (38,3), (39,3), (40,3)]
                     }

############
#  Identification des indicateurs non évalués en AC
############
       
Cellules_NON_AC =   {"CO7.ac1" : [(5,3), (6,3), (7,3), (8,3), (9,3)],
                     "CO7.ac2" : [(10,3), (11,3), (12,3), (13,3), (14,3), (15,3), (16,3)],
                     "CO7.ac3" : [(17,3), (18,3), (19,3), (20,3)],
                     "CO8.ac1" : [(22,3), (23,3), (24,3), (25,3)],
                     "CO8.ac2" : [(26,3), (27,3), (28,3), (29,3)],
                     "CO8.ac3" : [(30,3), (31,3), (32,3), (33,3)],
                     "CO9.ac1" : [(35,3), (36,3), (37,3), (38,3), (39,3)],
                     "CO9.ac2" : [(40,3), (41,3), (42,3)],
                     "CO9.ac3" : [(43,3), (44,3), (45,3)]}

############
#  Identification des indicateurs non évalués en ITEC
############
                                 
Cellules_NON_ITEC =   {"CO7.itec1" : [(5,3), (6,3), (7,3), (8,3), (9,3)],
                       "CO7.itec2" : [(10,3), (11,3), (12,3), (13,3), (14,3), (15,3)],
                       "CO7.itec3" : [(16,3), (17,3), (18,3)],
                       "CO7.itec4" : [(19,3), (20,3)],
                       "CO8.itec1" : [(22,3), (23,3), (24,3)],
                       "CO8.itec2" : [(25,3), (26,3), (27,3), (28,3)],
                       "CO8.itec3" : [(29,3), (30,3), (31,3), (32,3), (33,3)],
                       "CO8.itec4" : [(34,3), (35,3), (36,3)],
                       "CO9.itec1" : [(38,3), (39,3), (40,3)],
                       "CO9.itec2" : [(41,3), (42,3), (43,3), (44,3)],
                       "CO9.itec3" : [(45,3), (46,3), (47,3), (48,3)]}
                    
############
#  Identification des indicateurs non évalués en EE
############

Cellules_NON_EE = {"CO7.ee1" : [(5,3),
                                (6,3),
                                (7,3),
                                (8,3),
                                (9,3),
                                (10,3),
                                (11,3)
                                    ],
                   "CO7.ee2" : [(12,3),
                                (13,3),
                                (14,3),
                                (15,3),
                                (16,3),
                                (17,3)
                                    ],
                     "CO7.ee3" : [(18,3),
                                  (19,3),
                                  (20,3),
                                  (21,3)
                                    ],
                     "CO7.ee4" : [(22,3),
                                  (23,3),
                                  (24,3),
                                  (25,3)
                                    ],
                     "CO8.ee1" : [(27,3),
                                  (28,3),
                                  (29,3)
                                    ],
                     "CO8.ee2" : [(30,3),
                                  (31,3),
                                  (32,3),
                                  (33,3)                            
                                    ],
                     "CO8.ee3" : [(34,3),
                                  (35,3),
                                  (36,3)
                                    ],
                     "CO8.ee4" : [(37,3),
                                  (38,3),
                                  (39,3),
                                  (40,3),
                                  (41,3)
                                    ],
                     "CO9.ee1" : [(43,3),
                                  (44,3),
                                  (45,3)
                                    ],
                     "CO9.ee2" : [(46,3),
                                  (47,3),
                                  (48,3),
                                  (49,3)
                                    ],
                     "CO9.ee3" : [(50,3),
                                  (51,3),
                                  (52,3),
                                  (53,3)
                                    ]}

############
#  Identification des indicateurs non évalués en SIN
############                                 
  
dicIndicateurs_prj_SIN = {"CO7.sin1" : [(5,3),
                                        (6,3),
                                        (7,3),
                                        (8,3)
                                        ],
                         "CO7.sin2" : [(9,3),
                                       (10,3),
                                       (11,3),
                                       (12,3),
                                       (13,3)
                                        ],
                         "CO7.sin3" : [(14,3),
                                       (15,3),
                                       (16,3),
                                       (17,3)
                                        ],
                         "CO8.sin1" : [(19,3),
                                       (20,3),
                                       (21,3)
                                        ],
                         "CO8.sin2" : [(22,3),
                                       (23,3),
                                       (24,3),
                                       (25,3)
                                        ],
                         "CO8.sin3" : [(26,3),
                                       (27,3),
                                       (28,3)
                                        ],
                         "CO8.sin4" : [(29,3),
                                       (30,3),
                                       (31,3),
                                       (32,3)
                                        ],
                         "CO9.sin1" : [(34,3),
                                       (35,3),
                                       (36,3)
                                        ],
                         "CO9.sin2" : [(37,3),
                                       (38,3),
                                       (39,3),
                                       (40,3),
                                       (41,3)
                                        ],
                         "CO9.sin3" : [(42,3),
                                       (43,3),
                                       (44,3),
                                       (45,3)
                                        ],
                         "CO9.sin4" : [(46,3),
                                       (47,3),
                                       (48,3),
                                       (49,3),
                                       (50,3)
                                       ]}
                  
Cellules_INFO_STI2 = {"NomProjet" : (3,2),
                     "NomEleve" : (4,2),
                     "PrenomEleve" : (5,2)
                     }
 

####################################################################################
def getCell_NON(dic):
    d = {"CO1.1" : Cellules_NON_ETT["CO1.1"],
         "CO1.2" : Cellules_NON_ETT["CO1.2"],
         "CO2.1" : Cellules_NON_ETT["CO2.1"],
         "CO2.2" : Cellules_NON_ETT["CO2.2"],
         "CO6.1" : Cellules_NON_ETT["CO6.1"],
         "CO6.2" : Cellules_NON_ETT["CO6.2"],
         "CO6.3" : Cellules_NON_ETT["CO6.3"],
         "CO8.es" : Cellules_NON_ETT["CO8.es"]
         }
    d.update(dic)
    return d
    
Cellules_NON  =  {'ITEC'   : getCell_NON(Cellules_NON_SSI), 
                  'AC'     : getCell_NON(Cellules_NON_AC), 
#                  'EE'     : getCell_NON(Cellules_NON_EE), 
#                  'SIN'    : getCell_NON(Cellules_NON_SIN),
                  'SSI'    : Cellules_NON_SSI}    

         
import win32com.client,win32com.client.dynamic
from pywintypes import UnicodeType, TimeType
from constantes import PATH
import os


def getTableau(doc):
    typ = doc.GetTypeEnseignement(simple = True)
    tableau = PyExcel(os.path.join(PATH, GRILLE[typ]))
    return tableau


def modifierGrille(doc, tableur, eleve):
    print "modifierGrille"
    
    tableur.show()
    
    shts = tableur.getSheets()
   
#    for i, e in enumerate(doc.eleves):
#        tableur.copySheet(u'Identification', Before=u'Identification')
#        tableur.copySheet(u'Notation', Before=u'Identification')
        
    # On efface la feuille "Notation"
#    tableur.delSheet(2)   


#    noms = prenoms = ''
#    for i, e in enumerate(doc.eleves):
#        noms += e.GetNomPrenom()
#        prenoms += e.prenom + " ; "
#    tableur.renameSheet(i*2+2, u'Notation ' + e.GetNomPrenom())

    dic = Cellules_NON[doc.GetTypeEnseignement()]
    
#    print eleve, eleve.GetDicIndicateurs()
    
    dicIndic = eleve.GetDicIndicateurs()
    for comp, cells in dic.items():
        for j, cell in enumerate(cells):
            if comp in dicIndic.keys():
                indic = dicIndic[comp][j]
            else:
                indic = False
            if not indic:
                l, c = cell
                tableur.setCell(2, l, c, COCHE)
        
        
        
#    for comp, ii in eleve.GetDicIndicateurs().items():
#        for j, indic in enumerate(ii):
#            if not indic:
#                l, c = dic[comp][j]
#                tableur.setCell(2, l, c, COCHE)
    
    l,c = Cellules_INFO_SSI["Tit"]
    tableur.setCell(1, l, c, doc.intitule + "\n" + doc.problematique)
    
    l,c = Cellules_INFO_SSI["Nom"]
    tableur.setCell(1, l, c, eleve.nom)
    
    l,c = Cellules_INFO_SSI["Pre"]
    tableur.setCell(1, l, c, eleve.prenom)
    
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
        sht.Delete()
 
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
 
 

    
    
        
        
        
#def exporterGrille(typeDoc):
#    rb = xlrd.open_workbook(GRILLE[typeDoc])
#    wb = copy(rb)
#    l,c = Cellules_NON_SSI["B3"][0]
#    wb.get_sheet(1).write(l,c,'x')
#    
#    wb.save('output.xls')
#    
#exporterGrille('SSI')
    
    
    
    
    
    