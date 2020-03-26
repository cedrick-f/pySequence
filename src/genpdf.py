#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                  genpdf                                 ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2011-2013 Cédrick FAURY
##
## pySéquence : aide à la construction
## de Séquences et Progressions pédagogiques
## et à la validation de Projets

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


"""
Module genpdf
*************
Génération de documents PDF.

"""

from  constantes import ellipsizer, getAnneeScolaireStr, \
                        LONG_MAX_PROBLEMATIQUE, LONG_MAX_FICHE_VALID, LIMITE_GRAND_PETIT_CARACT
import util_path
import os.path
from itertools import zip_longest

import sys
from xhtml2pdf import pisa

from file2bmp import *

#from textwrap import wrap
#import csv

from reportlab.platypus import SimpleDocTemplate, Paragraph, doctemplate#, KeepTogether
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER,TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4


# workaround
from reportlab.pdfbase import _fontdata_widths_courier
from reportlab.pdfbase import _fontdata_widths_courierbold
from reportlab.pdfbase import _fontdata_widths_courieroblique
from reportlab.pdfbase import _fontdata_widths_courierboldoblique
from reportlab.pdfbase import _fontdata_widths_helvetica
from reportlab.pdfbase import _fontdata_widths_helveticabold
from reportlab.pdfbase import _fontdata_widths_helveticaoblique
from reportlab.pdfbase import _fontdata_widths_helveticaboldoblique
from reportlab.pdfbase import _fontdata_widths_timesroman
from reportlab.pdfbase import _fontdata_widths_timesbold
from reportlab.pdfbase import _fontdata_widths_timesitalic
from reportlab.pdfbase import _fontdata_widths_timesbolditalic
from reportlab.pdfbase import _fontdata_widths_symbol
from reportlab.pdfbase import _fontdata_widths_zapfdingbats
 
from reportlab.pdfbase import _fontdata_enc_winansi
from reportlab.pdfbase import _fontdata_enc_macroman
from reportlab.pdfbase import _fontdata_enc_standard
from reportlab.pdfbase import _fontdata_enc_symbol
from reportlab.pdfbase import _fontdata_enc_zapfdingbats
from reportlab.pdfbase import _fontdata_enc_pdfdoc
from reportlab.pdfbase import _fontdata_enc_macexpert
# end of workaround

from widgets import messageErreur, FullScreenWin
import time

if sys.platform == "win32" :
    from register import EnableProtectedModeReader, GetProtectedModeReader



#
# Elements HTML
#
def encap(s, t, att = []):
    return "<"+t+" "+" ".join(att)+">"+s+"</"+t+">"
    
def italic(s):
    return "<i>"+s+"</i>"

def gras(s):
    return "<strong>"+s+"</strong>"

def parag(s):
    return "<p>"+s+"</p>"

def listeeee(l, classe = "b"):
    s = ""
    for e in l:
        s += "<li>"+e+"</li>"
    return "<ul class=\""+classe+"\">"+s+"</ul>"

def case(etat = False):
    return "<span style=\"font-family:wingdings\">&#253;</span>"

def checkbox(etat = False, size = 20):
    if etat:
        c = "CheckBox_checked.png"
    else:
        c = "CheckBox_unchecked.png"
    return "<img src=\"{{MEDIA_URL}}/" + c + "\" height=\""+str(size)+"\" width=\""+str(size)+"\">&nbsp;&nbsp;"


def image(src, s = "width:100%; height=auto;"):
    return "<img src=\"" + src + "\" style=\""+s+"\">"


def remplaceCR(txt):
    return txt.replace("\n", "<br>")

    
def splitParagraph(text, style, Italic = False, Bold = False):
    pp = []
    for l in text.split("\n"):
#        pp.append(KeepTogether(Paragraph(l, style)))
        if Italic:
            l = italic(l)
        if Bold:
            l = gras(l)
        pp.append(Paragraph(l, style))
    return pp

def table_taches(taches, eleves, projet):

    p = None
    h = """<th style="width:6%">Tâches</th>  <th>Contrats de tâche</th>  <th  style="width:30%">Compétences</th>"""
    for e in eleves:
        h += """<th style="width:6%%" class = "verticalTableHeader">%s</th>""" %e.GetNomPrenom()
    h = encap(h, "tr")
    for c in projet.listTaches:
        nm = taches[c][1]
        ph = taches[c][0]
        cp = taches[c][2]

        if ph != p:
            phase = projet.phases[ph][1]
            h += """<tr><td colspan = "%s"><b>%s</b></td></tr>""" %(str(3+len(eleves)), phase)
            p = ph

        h += "<tr> <td>%s</td> <td>%s</td> <td>%s</td> %s </tr>" %(c, nm, " ".join(cp), "<td></td>"*len(eleves))
            
    return h

def case_a_cocher(labels, etats, size = 16):
    """
    :param labels: chaine de caractères comportant l'ensemble des libellé des cases
                    colonnes séparées par "\n\n"
                    libélés séparés par "\n"
    :type labels: string
    
    :param etats: 
    :type etats: list
    
    """
    e = 0
    cells = []
    for c in labels.split("\n\n"):
        col = []
        cells.append(col)
        for t in c.split("\n"):
            col.append([checkbox(e in etats, size = size)] + t.split(":"))
            e += 1
    lignes = list(map(list, zip_longest(*cells, fillvalue = [""]*3)))
    
    html = ""
    
    for l in lignes:
        tr = ""
        for c in l:
#             tr += encap(c[0], "td", ['style="width:16px"']) \
#                 + encap(c[1], "td", ['style="width:36px ; vertical-align:middle"'])
            tr += encap(c[0], "td", [f'style="width:{int(size*1.4)}px"']) \
                + encap(c[1], "td", ['style="vertical-align:middle;"'])
            if len(c) > 2:
                tr += encap(c[2], "td")
        html += encap(tr, "tr")
    
    return encap(html, "table", ['class="typologie"'])#, ['style="border: 1px solid black"'])
    
    
    
    colonnes = labels.split("\n\n")
    html = ""
    e = 0
    for c in colonnes:
        typo = c.split("\n")
        hc = []
        for i, t in enumerate(typo):
            hc.append(checkbox(e in etats) + t)
            e += 1
        html += encap("<br>".join(hc), "td")
    
    return encap(html, "table")

#######################################################################################################################
#
#    
#
#######################################################################################################################
import logging


class PisaNullHandler(logging.Handler):
    def emit(self, record):
        pass
logging.getLogger("xhtml2pdf").addHandler(PisaNullHandler())


# Pour cx_freeze !!
#from html5lib import trie
##print serializer
#from xhtml2pdf import w3c
#from xhtml2pdf.w3c import cssDOMElementInterface
#from xhtml2pdf.w3c import css
#print w3c.cssDOMElementInterface
#print css
#print cssDOMElementInterface


#



def genererFicheValidationHTML(nomFichierPDF, nomFichierHTML, projet):
#     print("genererFicheValidationHTML", nomFichierHTML)
    Err = []
    with open(nomFichierHTML,'r', encoding='utf-8') as f:
        sourceHtml = f.read()

    
    # Equipe pédagogique
    le = []
    for p in projet.equipe:
        np = p.GetNomPrenom()
        if p.referent:
            np = gras(np)  
        if p.discipline != 'Tec':
            np = italic(np)
        le.append(np)
    NP = listeeee(le) 
    
    # Elèves
    le = []
    for p in projet.eleves:
        np = p.GetNomPrenom()
        le.append(np)
    NE = listeeee(le) 
    
    # Typologie (cases à cocher)
#     typo = projet.GetProjetRef().attributs['TYP'][2].split(u"\n")
#     TY = "<br>".join([checkbox(i in projet.typologie) + t for i, t in enumerate(typo)])
    TY = case_a_cocher(projet.GetProjetRef().attributs['TYP'][2], projet.typologie)
    
    etab = projet.classe.etablissement+"<br>("+italic(projet.classe.ville)+")"
    
    champs = {'ACA' : projet.classe.academie,
              'SES' : str(projet.annee+1),
              'TIT' : remplaceCR(projet.intitule),
              'ETA' : etab,
              'PAR' : remplaceCR(projet.partenariat),
              'NBE' : str(len(projet.eleves)),
              'PRX' : projet.montant,
              'SRC' : remplaceCR(projet.src_finance),
              'TYP' : TY,
              'PRE' : remplaceCR(projet.problematique),
              'PB'  : remplaceCR(projet.problematique),
              'EQU' : NP,
              'ELE' : NE,
              'OBJ' : remplaceCR(projet.production),
              'SYN' : remplaceCR(projet.synoptique),
              'ORI' : remplaceCR(projet.origine),
              'CCF' : remplaceCR(projet.contraintes),
              'TCH' : table_taches(projet.GetProjetRef().taches, projet.eleves, projet.GetProjetRef()),
              'EFG' : str(len(projet.eleves)),
              'RTE' : ""
              }
    
#    print champs['TCH']
    
    # Les champs standards
    for code, val in champs.items():
        sourceHtml = sourceHtml.replace("[["+code+"]]", val)
    
    asupp = []
    # Les diagrammes sysML
    prj = projet.GetProjetRef()
    if prj.attributs['SML'][0] != "":
        for i, n in enumerate(prj.attributs['SML'][2]):
            code = "SML"+str(i)
            if code in projet.sysML:
                nf = file2imgfile(os.path.abspath(projet.sysML[code].GetAbsPath(projet.GetPath())))
                if nf is not None:
                    sourceHtml = sourceHtml.replace("[[ML"+str(i+1)+"]]", 
                                                    image(nf[0]))
                    if nf[1]:
                        asupp.append(nf[0])
                
        
    # Le dossier "media"
    sourceHtml = sourceHtml.replace("{{MEDIA_URL}}", os.path.join(util_path.PATH, r"..", DOSSIER_REF))
    
    # Conversion en PDF
    with open(nomFichierPDF, "w+b") as resultFile:
        # convert HTML to PDF
#         print(sourceHtml)
        try:
            pisaStatus = pisa.CreatePDF(sourceHtml,                # the HTML to convert
                                        dest=resultFile,
                                        show_error_as_pdf = True)           # file handle to recieve result
            if pisaStatus.err != 0:
                Err.append("Un des textes descriptifs du projet est peut-être trop grand !")
        except:
            Err.append("Le fichier HTML n'a pas pu être converti en PDF !\n\n" \
                       "\tVeillez à en vérifier la syntaxe, notamment celle des style CSS.")
        
    for f in asupp:
        os.remove(f)
        
        
        
#    print pisaStatus.err
    # return True on success and False on errors
    
        
    return Err

#
#
#
def genererFicheValidation(nomFichier, projet):
    """
    """
    Err = []
#     print("genererFicheValidation")
    #
    # Styles
    #
    title_style = ParagraphStyle(name="TitleStyle",
                                 fontName="Helvetica",
                                 textColor = colors.red,
                                 fontSize=20,
                                 alignment=TA_LEFT,
                                 )
    
    normal_style = ParagraphStyle(name="NormalStyle",
                                 fontName="Helvetica",
                                 fontSize=10,
                                 leading = 12,
                                 alignment=TA_LEFT,
                                 )
    

    
    entete_style = ParagraphStyle(name="EnteteStyle",
                                 fontName="Helvetica",
                                 textColor = colors.gray,
                                 fontSize=9,
                                 alignment=TA_LEFT,
                                 )
    
    info_style = ParagraphStyle(name="InfoStyle",
                                 fontName="Helvetica",
                                 textColor = colors.gray,
                                 fontSize=8,
                                 alignment=TA_LEFT,
                                 )
    
    # To make a SimpleDocTemplate, just supply a file name for your PDF, and the
    # page margins. You can optionally supply non-flowing elements such as headers
    # and footers. I will introduce that feature in a later demonstration.
    doc = SimpleDocTemplate(nomFichier,
                            pagesize=A4,
                            leftMargin=10*mm,
                            rightMargin=10*mm,
                            topMargin=10*mm,
                            bottomMargin=10*mm)
    
    story = [] # Fill this list with flowable objects
    
    ref = projet.GetReferentiel()
    prj = projet.GetProjetRef()
    #
    # En-tête
    #
    story.append(Paragraph("Fiche de validation du projet",
                           title_style
                           ))
    story.append(Spacer(1, 5*mm))
    
    if projet.GetTypeEnseignement() == 'SSI':
        en_tete = ["Bulletin officiel n°39 du 23 octobre 2014",
                   "Annexe 4 à la note de service n° 2014-131 du 9-10-2014",
                   "Baccalauréat général, série S, sciences de l'ingénieur - Épreuve orale, projet interdisciplinaire"]
        
    elif ref.Enseignement[0][:6] == 'STI2D-':
        en_tete = ["Bulletin officiel n°39 du 23 octobre 2014",
                   "Annexe 9 à la note de service n° 2014-132 du 13-10-2014",
                   "Baccalauréat technologique, série STI2D - Épreuve de projet en enseignement spécifique à la spécialité"]
        
    else:
        Err.append("Impossible de trouver le fichier HTML")
        return Err
        
        
    for l in en_tete:
        story.append(Paragraph(l, entete_style))
        story.append(Spacer(1, 1*mm))
    
    story.append(Spacer(1, 4*mm))
    
    
    #
    # Première zone
    #
    NP = []
    for p in projet.equipe:
        np = p.GetNomPrenom()
        if p.referent:
            np = gras(np)  
        if p.discipline != 'Tec':
            np = italic(np)
        NP.append(Paragraph(np, normal_style))
        
    data= [[[Paragraph(gras('Établissement : '), normal_style), Paragraph(projet.classe.etablissement, normal_style)], [Paragraph(gras("Année scolaire : ")+getAnneeScolaireStr(), normal_style),
                                                                                                                         Paragraph(gras("Nombre d’élèves concernés : ")+str(len(projet.eleves)), normal_style)]],
           [Paragraph(gras("Spécialité : ")+ ref.Enseignement[0], normal_style), Paragraph(gras("Nombre de groupes d’élèves : ")+str(projet.nbrParties), normal_style)],
           [Paragraph(gras("Noms et prénoms des enseignants responsables :"), normal_style), NP]]
    t = Table(data, style = [('VALIGN',      (0,0),(-1,-1),'TOP')])
    
    story.append(t)
    
    story.append(Spacer(1, 5*mm))
    
#     styleSheet = getSampleStyleSheet()


    #
    # Deuxième zone (tableau)
    #
#    print ref.attributs_prj
    # Colonne de gauche
    ppi = Paragraph(gras('Intitulé du projet'),normal_style)
    
    ppo = Paragraph(gras('Origine de la proposition'),normal_style)
    
    ppb = [Paragraph(gras('Problématique - Énoncé général du besoin'),normal_style)]
    ppb.append(splitParagraph(prj.attributs['PB'][1], info_style, Italic = True))

    pco = [Paragraph(gras('Contraintes imposées au projet'),normal_style)]
    pco.append(splitParagraph(prj.attributs['CCF'][1], info_style, Italic = True))

    ppig = Paragraph(gras('Intitulé des parties du projet confiées à chaque groupe'),normal_style)
    
    ppbg = Paragraph(gras('Énoncé du besoin pour la partie du projet confiée à chaque groupe'),normal_style)
    
    ppr = [Paragraph(gras('Production finale attendue'),normal_style)]
    ppr.append(splitParagraph(prj.attributs['OBJ'][1], info_style, Italic = True))
    
    
    # Colonne de droite
    contenu = [projet.intitule,
               projet.origine,
               projet.problematique,
               projet.contraintes,
               projet.intituleParties,
               projet.besoinParties,
               projet.production]
    p = []
    tot = 0
    for c in contenu:
        t = ellipsizer(c, LONG_MAX_FICHE_VALID)
        tot += len(t)
        normal_style.fontSize = max(8, 11 - int(len(t)/250))
        normal_style.leading = normal_style.fontSize * 1.2
        p.append(splitParagraph(t, normal_style))
        normal_style.fontSize = 10
        normal_style.leading = 12
    
    larg = max(50, min(150, 190*tot/800))*mm
    
    data= [[ppi, p[0]],
           [ppo, p[1]],
           [ppb, p[2]],
           [pco, p[3]],
           [ppig, p[4]],
           [ppbg, p[5]],
           [ppr, p[6]]]
           
    t=Table(data, style=[('GRID',        (0,0),(-1,-1),  1,colors.black),
                         ('VALIGN',      (0,0),(-1,-1), 'TOP')],
            colWidths = [None, larg])

    story.append(t)
    
    
    #
    # Zone des signatures
    #
    story.append(Spacer(1, 5*mm))
    V1 = [Paragraph("Visa du chef d’établissement", normal_style),
          Paragraph("(Nom, prénom, date et signature)", info_style)]
    V2 = [Paragraph("Visa du ou des IA-IPR", normal_style),
          Paragraph("(Noms, prénoms, qualités, dates et signatures)", info_style)]
    data= [[V1, V2]]
    t=Table(data,style=[('VALIGN',      (0,0),(-1,-1),'TOP')])
    story.append(t)
    
    try:
        doc.build(story)
    except doctemplate.LayoutError as err:
        Err.append("Paragraphe trop grand")

    return Err
    
#genererFicheValidation(u"Intitulé du projet")
    
from Referentiel import DOSSIER_REF

import constantes

def genererDossierValidation(nomFichier, projet, fenDoc):
    Err = []
#     print("genererDossierValidation")
    dosstemp = tempfile.mkdtemp()
    fichertempV = os.path.join(dosstemp, "pdfvalid.pdf")
    fichertempF = os.path.join(dosstemp, "pdffiche.pdf")
#    fichertemp = os.path.join(dosstemp, "pdfdoss.pdf")
#     print("   ", fichertempV)
#     print("   ", fichertempF)
    wx.BeginBusyCursor()
    
    nomFichierHTML = os.path.join(util_path.PATH, r"..", DOSSIER_REF, 
                                  projet.GetProjetRef().ficheValid)
    
    if os.path.isfile(nomFichierHTML):
        Err = genererFicheValidationHTML(fichertempV, nomFichierHTML, projet)
    else:
        Err = genererFicheValidation(fichertempV, projet)
    
#     print("      ",Err)
    
    if len(Err) > 0:
        shutil.rmtree(dosstemp)
        wx.EndBusyCursor()
        return Err
#     print("Ok1")
    
    fenDoc.exporterFichePDF(fichertempF, pourDossierValidation = True)
    
    doc1 = fitz.open(fichertempV)
    doc2 = fitz.open(fichertempF)
    
    doc = fitz.open()
    doc.insertPDF(doc1) 
    doc.insertPDF(doc2)
    try:
        doc.save(nomFichier)
    except:
        Err.append("Impossible d'enregistrer le fichier :\n%s" %nomFichier)
    finally:
        doc.close()
#     print("Ok2")
    doc1.close()
    doc2.close()
    
    
#     merger = PdfFileMerger()
#     input1 = open(fichertempV, "rb")
#     input2 = open(fichertempF, "rb")
#     merger.append(input1)
#     merger.append(input2)
#      
#     output = open(nomFichier, "wb")
#     merger.write(output)
#      
#      
#     input1.close()
#     input2.close()
#     output.close()
    
    shutil.rmtree(dosstemp)
    wx.EndBusyCursor()
    return Err




if sys.platform == "win32":  
    import grilles





def genererGrillePDF(nomFichier, grilles_feuilles):
#    print "genererGrillePDF" 
#    print grilles_feuilles
    
    wx.BeginBusyCursor()
    dosstemp = tempfile.mkdtemp()
    
    doc = fitz.open()
    
    
#     merger = PdfFileMerger()
#     print "temp :", dosstemp
    
    Ok = True
    g = []
    for i, grille_feuille in enumerate(grilles_feuilles):
        grille, feuille = grille_feuille
        try:
            grille = grilles.PyExcel(grille)
        except Exception as err:
            wx.EndBusyCursor()
            messageErreur(self, "Erreur !", err.args[0])
            return False
            
        g.append(grille)
        if feuille is None:
            feuille = grille.getSheets()[-1]
#        print "   ", feuille
        # Création du fichier temporaire PDF
        nomGrille = "grille"+str(i)+".pdf"
        fichertempV = os.path.join(dosstemp, nomGrille)
        
        # Activation des feuilles "grilles"
        grille.setActiveSheet(grille.getSheetNum(feuille))
#        grille.setActiveSheet(i+1)

        # Génération de la grille en PDF
        try:
            grille.save_pdf(fichertempV)
#             grille.close()
        except:
            Ok = False
            print("Erreur save_pdf 1")
        
        try:
            doc1 = fitz.open(fichertempV)
            doc.insertPDF(doc1) 
            doc1.close()
            
#             f = open(fichertempV, "rb")
#             merger.append(f)
#             f.close()
        except:
            Ok = False
            print("Erreur save_pdf 2")  
        
    for grille in g:
        try:
            grille.close()
        except:
            pass
        
        
        
    if not Ok:
        shutil.rmtree(dosstemp)
        wx.EndBusyCursor()
        messageErreur(self, "Erreur !",
                            "Impossible de générer le fichier PDF des grilles")
        return False
    
    doc.save(nomFichier)
    doc.close()
#     output = open(nomFichier, "wb")
#     merger.write(output)
    
    try:
        shutil.rmtree(dosstemp)
    except:
        print("Grilles temporaires non supprimées :", dosstemp)
        
    wx.EndBusyCursor()
    return True
    # read PDF files (.pdf) with wxPython
    # using wx.lib.pdfwin.PDFWindow class ActiveX control
    # from wxPython's new wx.activex module, this allows one
    # to use an ActiveX control, as if it would be wx.Window
    # it embeds the Adobe Acrobat Reader
    # as far as HB knows this works only with Windows
    # tested with Python24 and wxPython26 by HB



import wx


# Détermination du lecteur de PDF à utiliser
ADOBE_VERSION = None
if  wx.PlatformInfo[1] == 'wxMSW':
    import comtypes.client as cc
    
    try:            # Adobe Reader >= 7.0
        dllpath = cc.GetModule( ('{05BFD3F1-6319-4F30-B752-C7A22889BCC4}', 1, 0) ).typelib_path
    except:
        try:        # Adobe Reader 5 or 6
            dllpath = cc.GetModule( ('{CA8A9783-280D-11CF-A24D-444553540000}', 1, 0) ).typelib_path
        except:
            dllpath = r""
            pass    # Adobe Reader not installed
    
    from win32api import GetFileVersionInfo, LOWORD, HIWORD
    
    def get_version_number (filename):
        info = GetFileVersionInfo (filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD (ms), LOWORD (ms), HIWORD (ls), LOWORD (ls)
    
    try:
        ADOBE_VERSION = get_version_number(dllpath)
    except:
        ADOBE_VERSION = None
        
    print("Version Adobe Reader", ADOBE_VERSION)

from wx.lib.pdfwin import get_min_adobe_version
NOT_USE_ADOBE = ADOBE_VERSION is None or ADOBE_VERSION[:3] == (11, 0, 7) or ADOBE_VERSION[:3] == (11, 0, 8) or get_min_adobe_version() is None
# NOT_USE_ADOBE = True
if sys.platform != "win32" :
    NOT_USE_ADOBE = True
    
HAS_PDFVIEWER = True
# if NOT_USE_ADOBE:
try:
    from wx.lib.pdfviewer import pdfViewer
except:
    HAS_PDFVIEWER = False
# HAS_PDFVIEWER = False # désactivé ... ça marche pas !
    
if not NOT_USE_ADOBE:
    from wx.lib.pdfwin import PDFWindow

# print "HAS_PDFVIEWER", HAS_PDFVIEWER


#if wx.Platform == '__WXMSW__':
#    from wx.lib.pdfwin import PDFWindow, get_min_adobe_version
#elif wx.Platform == '__WXMAC__':
#    print "MAC !!"

#    from wx.lib.pdfviewer import pdfViewer
import tempfile
import shutil
# from PyPDF2 import PdfFileMerger
import fitz


def getPDFViewer():
    return get_min_adobe_version()

class PdfPanel(wx.Panel, FullScreenWin):
    def __init__(self, parent):

        wx.Panel.__init__(self, parent, id=-1)
        
        
        self.pdf = None
        sizer = wx.BoxSizer(wx.VERTICAL)

        if True:#NOT_USE_ADOBE:
            if HAS_PDFVIEWER:
                self.pdf = pdfViewer( self, -1, wx.DefaultPosition,
                                    wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
            else:
                self.pdf = PanelBoutonPdf(self)
        else:
            m = GetProtectedModeReader()
            EnableProtectedModeReader(0)
            self.pdf = PDFWindow(self, style=wx.SUNKEN_BORDER)
            EnableProtectedModeReader(m)
        
        
#        if ADOBE_VERSION == None:
#            self.pdf = wx.StaticText(self, -1, u"Cette fonctionnalité n'est disponible qu'avec Adobe Acrobat Reader\n"\
#                                                   u"Pour obtenir le dossier de validation, passer par le menu Fichier/Générer le dossier de validation.")
#        else:
#            if ADOBE_VERSION[:3] == (11, 0, 7) or ADOBE_VERSION[:3] == (11, 0, 8):
#                self.pdf = wx.StaticText(self, -1, u"Cette fonctionnalité n'est pas compatible Adobe Acrobat Reader version 11.0.07 !!\n\n"\
#                                                   u"Pour visualiser le dossier de validation :\n"\
#                                                   u" - Passer à la version 10.0.09 - si disponible (http://get.adobe.com/fr/reader)\n" \
#                                                   u" - Utiliser la version 11.0.06 (http://www.adobe.com/support/downloads/product.jsp?product=10&platform=Windows)\n" \
#                                                   u" - Utiliser la version 10 (http://get.adobe.com/fr/reader/otherversions)\n" \
#                                                   u" - Générer le fichier .pdf : menu Fichier/Générer le dossier de validation projet")
#            elif get_min_adobe_version() != None:
#                self.pdf = PDFWindow(self, style=wx.SUNKEN_BORDER)
#            else:
#                self.pdf = wx.StaticText(self, -1, u"Cette fonctionnalité n'est disponible qu'avec Adobe Acrobat Reader\n"\
#                                                   u"Pour obtenir le dossier de validation, passer par le menu Fichier/Générer le dossier de validation.")
#        else:
#            self.pdf = pdfViewer( self, -1, wx.DefaultPosition,
#                                wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
        sizer.Add(self.pdf, proportion=1, flag=wx.EXPAND)
        
        self.mess = wx.StaticText(self, -1, "")
        sizer.Add(self.mess, proportion=1, flag=wx.EXPAND)
        sizer.Show(self.mess, False)
            
        self.SetSizer(sizer)
        self.sizer = sizer
        self.SetAutoLayout(True)
    
        self.pdf.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        
    
        FullScreenWin.__init__(self, self.pdf)
        
        
        
#         self.Bind(wx.EVT_CLOSE, self.OnClose )
#         self.pdf.Bind(wx.EVT_WINDOW_DESTROY, self.OnClose)
#         self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroyWindow)

#     ######################################################################################################
#     def OnDestroyWindow(self, event):
#         print "OnDestroy pdf"
#         self.pdf.Unbind(wx.EVT_ENTER_WINDOW)
#         self.pdf.FreeDlls()
#         print "...FAIT"
# 
    ######################################################################################################
    def PreClose(self):
        print("PreClose pdf")
        try:
            self.pdf.LoadFile(None)
            self.pdf.FreeDlls()
        except:
            pass
        
#         
# #         self.sizer.Detach(self.pdf)
# #         self.pdf.Unbind(wx.EVT_ENTER_WINDOW)
#         
#         
#         self.pdf.Close()
# #         self.sizer.Remove(self.pdf)
# #         self.pdf.Destroy()
# #         time.sleep(3)
# #         wx.CallAfter(self.pdf.Close)
# #         self.Destroy()
# #         self.pdf.Destroy()
# #         evt.Skip()

    ######################################################################################################
    def OnEnter(self, event):
#         print "OnEnter PDF"
        self.pdf.SetFocus()
        event.Skip()
        

    
    ######################################################################################################
    def MiseAJour(self, projet, fenDoc):
        """ Génération d'un fichier PDF temporaire pour affichage
              - Dossier de validation
              - ...
        """
        self.dosstemp = tempfile.mkdtemp()
        fichertemp = os.path.join(self.dosstemp, "pdfdoss.pdf")
        
        wx.BeginBusyCursor()
        Err = genererDossierValidation(fichertemp, projet, fenDoc)
        wx.EndBusyCursor()
#         print("1")
        if len(Err) == 0:
            Err = self.chargerFichierPDF(fichertemp)
#         print("2")
#         self.sizer.Show(self.pdf, len(Err) == 0)
        self.sizer.Show(self.mess, len(Err) > 0)
#         print("3")
        if len(Err) > 0:
            m = "Une erreur s'est porduite lors de la création ou l'affichage du fichier PDF.\n\n"
            m += "\n".join(Err)
            self.mess.SetLabel(m)
            
            self.sizer.Layout()
    
    
    ######################################################################################################
    def supprimerDossierTemp(self):
        """ Suppression  du dossier temporaire
             Méthode brute
        """
        if True:#get_min_adobe_version() != None:
            try:
                shutil.rmtree(self.dosstemp)
            except:
                time.sleep(.5)
                try:
                    shutil.rmtree(self.dosstemp)
                except:
                    pass
                
    ######################################################################################################
    def chargerFichierPDF(self, nomFichier):
        """ Affichage en interne du fichier PDF
             ou bien mise à jour du bouton d'affichage externe
        """
        Err = []
        
        if isinstance(self.pdf, PanelBoutonPdf):
            self.pdf.MiseAJour(nomFichier)

        elif isinstance(self.pdf, pdfViewer):
            wx.BeginBusyCursor()
            try:
                self.pdf.LoadFile(nomFichier)
            except:
                Err.append("ERREUR pdfViewer")
            finally:
                wx.EndBusyCursor()    
                
        elif isinstance(self.pdf, PDFWindow):
            wx.BeginBusyCursor()
            try:
                self.pdf.LoadFile(nomFichier)
            except:
                Err.append("ERREUR PDFWindow")
            finally:
                wx.EndBusyCursor()
        
        return Err


class PanelBoutonPdf(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.nomFichier = ''
        
        self.mess = wx.StaticText(self, -1, "L'affichage des fichiers PDF\nn'est disponible qu'avec Adobe Acrobat Reader\n")
        
        self.bouton = wx.Button(self, -1, "Ouvrir le fichier PDF")
        
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.bouton)
        
        self.sizer.Add(self.mess)
        self.sizer.Add(self.bouton)
        
        self.SetSizer(self.sizer)
        
    
    def OnClick(self, event):
        try:
            os.startfile(self.nomFichier)
        except:
            pass
        
    def MiseAJour(self, nomFichier):
        self.nomFichier = nomFichier
        self.bouton.SetToolTip("Ouvrir le fichier PDF avec un lecteur externe\n\t%s" %self.nomFichier)



#from pgmagick import Image
#im = Image('D:\\Developpement\\pysequence\\BO\\SSI\\candidats-individuels.pdf')     
#im.write('D:\\Developpement\\pysequence\\BO\\SSI\\candidats-individuels.png')    
#        
#        if isinstance(self.pdf, wx.StaticText):
##        if get_min_adobe_version() == None:\
#            print "Problème version Adobe"
#            return
#        try:
#            self.pdf.LoadFile(nomFichier)
#        except:
#            print "ERREUR PDF", self.pdf
        
        
#    def OnOpenButton(self, event):
#        # make sure you have PDF files available on your drive
#        dlg = wx.FileDialog(self, wildcard="*.pdf")
#        if dlg.ShowModal() == wx.ID_OK:
#        wx.BeginBusyCursor()
#        self.pdf.LoadFile(dlg.GetPath())
#        wx.EndBusyCursor()
#        dlg.Destroy()
#    def OnPrevPageButton(self, event):
#        self.pdf.gotoPreviousPage()
#    def OnNextPageButton(self, event):
#        self.pdf.gotoNextPage()
    




#
#
#
#
#
#
#from reportlab.pdfgen import canvas
#def hello (c):
#    c.drawString(100,100,"Hello World")
#    c = canvas.Canvas("hello.pdf")
#
#hello(c)
#c.showPage()
#c.save()
#
#
#I = Image('../images/replogo.gif')
#I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
#I.drawWidth = 1.25*inch
#P0 = Paragraph('''<b>A pa<font color=red>r</font>a<i>graph</i></b><super><font color=yellow>1</font></super>''',
#               styleSheet["BodyText"])
#P = Paragraph('''<para align=center spaceb=3>The<b>ReportLab Left<font color=red>Logo</font></b>Image</para>''',
#              styleSheet["BodyText"])
#data= [['A', 'B', 'C', P0,'D'],
#       ['00','01','02', [I,P],'04'],
#       ['10','11','12', [P,I],'14'],
#       ['20','21','22','23','24'],
#       ['30','31','32','33','34']]
#t=Table(data,style=[('GRID',(1,1),(-2,-2),1,colors.green),
#                    ('BOX',(0,0),(1,-1),2,colors.red),
#                    ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
#                    ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
#                    ('BACKGROUND', (0, 0), (0, 1), colors.pink),
#                    ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
#                    ('BACKGROUND', (2, 2), (2, 3), colors.orange),
#                    ('BOX',(0,0),(-1,-1),2,colors.black),
#                    ('GRID',(0,0),(-1,-1),0.5,colors.black),
#                    ('VALIGN',(3,0),(3,0),'BOTTOM'),
#                    ('BACKGROUND',(3,0),(3,0),colors.limegreen),
#                    ('BACKGROUND',(3,1),(3,1),colors.khaki),
#                    ('ALIGN',(3,1),(3,1),'CENTER'),
#                    ('BACKGROUND',(3,2),(3,2),colors.beige),
#                    ('ALIGN',(3,2),(3,2),'LEFT'),
#                    ])
#t._argW[3]=1.5*inch


