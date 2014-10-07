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

import constantes
import os.path
#from textwrap import wrap
#import csv

from reportlab.platypus import SimpleDocTemplate, Paragraph, doctemplate, KeepTogether
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



#
#
#
def italic(s):
    return "<i>"+s+"</i>"

def gras(s):
    return "<strong>"+s+"</strong>"

def splitParagraph(text, style):
    pp = []
    for l in text.split("\n"):
#        pp.append(KeepTogether(Paragraph(l, style)))
        pp.append(Paragraph(l, style))
    return pp

#
#
#
def genererFicheValidation(nomFichier, projet):
    """
    """
    
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
                                 alignment=TA_LEFT,
                                 )
    
    entete_style = ParagraphStyle(name="EnteteStyle",
                                 fontName="Helvetica",
                                 textColor = colors.gray,
                                 fontSize=9,
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
    
    
    #
    # Entête
    #
    story.append(Paragraph(u"Fiche de validation du projet",
                           title_style
                           )
                 )
    story.append(Spacer(1, 5*mm))
    
    
    if projet.GetTypeEnseignement() == 'SSI':
        story.append(Paragraph(u"Bulletin officiel n°1 du 3 janvier 2013",
                               entete_style
                               ))
        story.append(Spacer(1, 1*mm))
        story.append(Paragraph(u"Annexe 3 à la note de service n° 2011-152 du 3 octobre 2011",
                               entete_style))
        story.append(Spacer(1, 1*mm))
        story.append(Paragraph(u"Baccalauréat général, série S, sciences de l'ingénieur - Épreuve de projet",
                               entete_style))
    elif projet.GetReferentiel().Famille == 'STI':
        story.append(Paragraph(u"Bulletin officiel n° 45 du 6 décembre 2012",
                               entete_style))
        story.append(Spacer(1, 1*mm))
        story.append(Paragraph(u"Annexe 8 à la note de service n° 2012-037 du 5 mars 2012",
                               entete_style))
        story.append(Spacer(1, 1*mm))
        story.append(Paragraph(u"Série STI2D - Épreuve de projet en enseignement spécifique à la spécialité",
                               entete_style))
    
    story.append(Spacer(1, 5*mm))
    
    
    #
    # Première zone
    #
    NP = []
    for p in projet.equipe:
        if p.referent:
            np = "<strong>"+p.GetNomPrenom()+"</strong>"
        else:
            np = p.GetNomPrenom()
            
        if p.discipline != 'Tec':
#            constantes.COUL_DISCIPLINES[p.discipline]
            np = "<i>"+np+"</i>"
            
        NP.append(Paragraph(np, normal_style))
        
    data= [[[Paragraph(gras(u'Établissement : '), normal_style), Paragraph(projet.classe.etablissement, normal_style)], [Paragraph(gras(u"Année scolaire : ")+constantes.getAnneeScolaireStr(), normal_style),
                                                                                                                         Paragraph(gras(u"Nombre d’élèves concernés : ")+str(len(projet.eleves)), normal_style)]],
           [Paragraph(gras(u"Spécialité : ")+ projet.GetReferentiel().Enseignement[0], normal_style), Paragraph(gras(u"Nombre de groupes d’élèves : ")+str(projet.nbrParties), normal_style)],
           [Paragraph(gras(u"Noms et prénoms des enseignants responsables :"), normal_style),NP]]
    t=Table(data,style=[('VALIGN',      (0,0),(-1,-1),'TOP')])
    
    story.append(t)
    
    
#    story.append(Paragraph(u"La présente fiche est établie en vue de la validation des projets au niveau académique, en début d’année de\n" \
#                           u"classe terminale. Elle est complétée par un document précisant la répartition prévisionnelle des tâches\n" \
#                           u"collectives, individuelles et sous-traitées, par groupe d’élèves. Les groupes sont désignés par des lettres (A, B, C,\n" \
#                           u"etc.) et leur effectif est indiqué.\n" \
#                           u"Le projet présenté est celui sur lequel est évalué le candidat dans le cadre de l’épreuve de projet en\n" \
#                           u"enseignement spécifique à la spécialité. Il est prévu pour être conduit en 70 heures environ.",
#                           normal_style
#                           )
#                 )
    # A Spacer flowable is fairly obvious. It is used to ensure that an empty space
    # of a given size is left in the frame. This spacer leaves a 25mm gap before
    # this next paragraph.
    story.append(Spacer(1, 15*mm))
    
    styleSheet = getSampleStyleSheet()
    
#    P0 = Paragraph('''<b>A pa<font color=red>r</font>a<i>graph</i></b><super><font color=yellow>1</font></super>''',
#                   styleSheet["BodyText"])
#    P = Paragraph('''<para align=center spaceb=3>The<b>ReportLab Left<font color=red>Logo</font></b>Image</para>''',
#                  styleSheet["BodyText"])

    #
    # Deuxième zone
    #
    ppb = [Paragraph(gras(u'Problématique - Énoncé général du besoin'),normal_style)]
    for l in constantes.TIP_PROBLEMATIQUE.split("\n"):
        ppb.append(Paragraph(l, entete_style))

    pco = [Paragraph(gras(u'Contraintes imposées au projet'),normal_style)]
    for l in constantes.TIP_CONTRAINTES.split("\n"):
        pco.append(Paragraph(l, entete_style))
        
    ppr = [Paragraph(gras(u'Production finale attendue'),normal_style)]
    for l in constantes.TIP_PRODUCTION.split("\n"):
        ppr.append(Paragraph(l, entete_style))
        
    data= [[Paragraph(gras(u'Intitulé du projet'),normal_style),                splitParagraph(projet.intitule, normal_style)],
           [Paragraph(gras(u'Origine de la proposition'),normal_style),         splitParagraph(projet.origine, normal_style)],
           [ppb,                                                                splitParagraph(projet.problematique, normal_style)],
           [pco,                                                                splitParagraph(projet.contraintes, normal_style)],
           [Paragraph(gras(u'Intitulé des parties du projet confiées à chaque groupe'),normal_style),               splitParagraph(projet.intituleParties, normal_style)],
           [Paragraph(gras(u'Énoncé du besoin pour la partie du projet confiée à chaque groupe'),normal_style),     splitParagraph(projet.besoinParties, normal_style)],
           [ppr,                                                                splitParagraph(projet.production,normal_style)]]
           
    t=Table(data,style=[('GRID',        (0,0),(-1,-1),  1,colors.black),
                        ('VALIGN',      (0,0),(-1,-1),'TOP')])

    
    story.append(t)
    
    
    #
    # Zone des signatures
    #
    story.append(Spacer(1, 15*mm))
    V1 = [Paragraph(u"Visa du chef d’établissement", normal_style),
          Paragraph(u"(Nom, prénom, date et signature)", entete_style)]
    V2 = [Paragraph(u"Visa du ou des IA-IPR", normal_style),
          Paragraph(u"(Noms, prénoms, qualités, dates et signatures)", entete_style)]
    data= [[V1, V2]]
    t=Table(data,style=[('VALIGN',      (0,0),(-1,-1),'TOP')])
    story.append(t)
    try:
        doc.build(story)
    except doctemplate.LayoutError, err:
        print "Paragraphe trop grand"
#        print err.message
#        print type(err)
#        print dir(err)
        return False
    return True
    
#genererFicheValidation(u"Intitulé du projet")
    
    
    
def genererDossierValidation(nomFichier, projet, fenDoc):
    dosstemp = tempfile.mkdtemp()
    fichertempV = os.path.join(dosstemp, "pdfvalid.pdf")
    fichertempF = os.path.join(dosstemp, "pdffiche.pdf")
#    fichertemp = os.path.join(dosstemp, "pdfdoss.pdf")
    
    wx.BeginBusyCursor()
    Ok = genererFicheValidation(fichertempV, projet)
    if not Ok:
        shutil.rmtree(dosstemp)
        wx.EndBusyCursor()
        return False
    fenDoc.exporterFichePDF(fichertempF)
    
    merger = PdfFileMerger()
    input1 = open(fichertempV, "rb")
    input2 = open(fichertempF, "rb")
    merger.append(input1)
    merger.append(input2)
    
    output = open(nomFichier, "wb")
    merger.write(output)
    output.close()
    input1.close()
    input2.close()
    
    shutil.rmtree(dosstemp)
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
if wx.Platform == '__WXMSW__':
    from wx.lib.pdfwin import PDFWindow, get_min_adobe_version
elif wx.Platform == '__WXMAC__':
    print "MAC !!"
    
#    from wx.lib.pdfviewer import pdfViewer
import tempfile
import shutil
from PyPDF2 import PdfFileMerger

def getPDFViewer():
    return get_min_adobe_version()

class PdfPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=-1)
        self.pdf = None
        sizer = wx.BoxSizer(wx.VERTICAL)
        if constantes.ADOBE_VERSION[:3] == (11, 0, 7) or constantes.ADOBE_VERSION[:3] == (11, 0, 8):
            self.pdf = wx.StaticText(self, -1, u"Cette fonctionnalité n'est pas compatible Adobe Acrobat Reader version 11.0.07 !!\n\n"\
                                               u"Pour visualiser le dossier de validation :\n"\
                                               u" - Passer à la version 10.0.09 - si disponible (http://get.adobe.com/fr/reader)\n" \
                                               u" - Utiliser la version 11.0.06 (http://www.adobe.com/support/downloads/product.jsp?product=10&platform=Windows)\n" \
                                               u" - Utiliser la version 10 (http://get.adobe.com/fr/reader/otherversions)\n" \
                                               u" - Générer le fichier .pdf : menu Fichier/Générer le dossier de validation projet")
        elif get_min_adobe_version() != None:
            self.pdf = PDFWindow(self, style=wx.SUNKEN_BORDER)
        else:
            self.pdf = wx.StaticText(self, -1, u"Cette fonctionnalité n'est disponible qu'avec Adobe Acrobat Reader")
#        else:
#            self.pdf = pdfViewer( self, -1, wx.DefaultPosition,
#                                wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
        sizer.Add(self.pdf, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.sizer = sizer
        self.SetAutoLayout(True)
        
    def MiseAJour(self, projet, fenDoc):
        if isinstance(self.pdf, wx.StaticText):
#        if get_min_adobe_version() == None:
            print "Problème version Adobe"
            return
#        if hasattr(self, 'dosstemp') and get_min_adobe_version() == None:
#            shutil.rmtree(self.dosstemp)
        self.dosstemp = tempfile.mkdtemp()
        fichertemp = os.path.join(self.dosstemp, "pdfdoss.pdf")

        wx.BeginBusyCursor()
        Ok = genererDossierValidation(fichertemp, projet, fenDoc)
        if Ok:
            self.pdf.LoadFile(fichertemp)
        if True:#get_min_adobe_version() != None:
            shutil.rmtree(self.dosstemp)
        wx.EndBusyCursor()
        if not Ok:
            self.pdf = wx.StaticText(self, -1, u"Un des textes descriptifs du projet est trop grand !")
            self.sizer.Add(self.pdf, proportion=1, flag=wx.EXPAND)
            
        
        
        
        
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
