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

## Copyright (C) 2011 Cédrick FAURY

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import constantes
from os.path import join
from textwrap import wrap
#import csv

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER,TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

def italic(s):
    return "<i>"+s+"</i>"

def gras(s):
    return "<strong>"+s+"</strong>"

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
                            leftMargin=15*mm,
                            rightMargin=15*mm,
                            topMargin=15*mm,
                            bottomMargin=15*mm)
    
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
        story.append(Paragraph(u"Bulletin officiel n° 45 du 6 décembre 2012",
                               entete_style
                               ))
        story.append(Spacer(1, 1*mm))
        story.append(Paragraph(u"Annexe 8 à la note de service n° 2012-037 du 5 mars 2012 - série STI2D - Épreuve de projet en " \
                               u"enseignement spécifique à la spécialité",
                               entete_style
                               ))
    else:
        story.append(Paragraph(u"Bulletin officiel n° 45 du 6 décembre 2012",
                               entete_style
                               ))
        story.append(Spacer(1, 1*mm))
        story.append(Paragraph(u"Annexe 8 à la note de service n° 2012-037 du 5 mars 2012 - série STI2D - Épreuve de projet en" \
                               u"enseignement spécifique à la spécialité",
                               entete_style
                               ))
    
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
            
        print p, p.discipline
        if p.discipline != 'Tec':
#            constantes.COUL_DISCIPLINES[p.discipline]
            np = "<i>"+np+"</i>"
            
        NP.append(Paragraph(np, normal_style))
        
    data= [[[Paragraph(gras(u'Établissement : '), normal_style), Paragraph(projet.classe.etablissement, normal_style)], [Paragraph(gras(u"Année scolaire : ")+constantes.getAnneeScolaire(), normal_style),
                                                                                                                         Paragraph(gras(u"Nombre d’élèves concernés : ")+str(len(projet.eleves)), normal_style)]],
           [Paragraph(gras(u"Spécialité : ")+ projet.GetTypeEnseignement(), normal_style), Paragraph(gras(u"Nombre de groupes d’élèves : "), normal_style)],
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
        
    data= [[Paragraph(gras(u'Intitulé du projet'),normal_style),                Paragraph(projet.intitule, normal_style)],
           [Paragraph(gras(u'Origine de la proposition'),normal_style),         Paragraph(projet.origine, normal_style)],
           [ppb,                                                                Paragraph(projet.problematique, normal_style)],
           [pco,                                                                Paragraph(projet.contraintes, normal_style)],
           [Paragraph(gras(u'Intitulé des parties du projet confiées à chaque groupe'),normal_style),               Paragraph(projet.intituleParties, normal_style)],
           [Paragraph(gras(u'Énoncé du besoin pour la partie du projet confiée à chaque groupe'),normal_style),     Paragraph(projet.besoinParties, normal_style)],
           [ppr,                                                                Paragraph(projet.production,normal_style)]]
           
    t=Table(data,style=[('GRID',        (0,0),(-1,-1),  1,colors.black),
                        ('VALIGN',      (0,0),(-1,-1),'TOP')])
    #                    ('BOX',         (0,0),(1,-1),   2,colors.red)])
    #                    ('LINEABOVE',   (1,2),(-2,2),   1,colors.blue),
    #                    ('LINEBEFORE',  (2,1),(2,-2),   1,colors.pink),
    #                    ('BACKGROUND',  (0, 0), (0, 1), colors.pink),
    #                    ('BACKGROUND',  (1, 1), (1, 2), colors.lavender),
    #                    ('BACKGROUND',  (2, 2), (2, 3), colors.orange),
    #                    ('BOX',         (0,0),(-1,-1),  2,colors.black),
    #                    ('GRID',        (0,0),(-1,-1),  0.5,colors.black),
#                        ('VALIGN',      (3,0),(3,0),'BOTTOM'),
    #                    ('BACKGROUND',  (3,0),(3,0),colors.limegreen),
    #                    ('BACKGROUND',  (3,1),(3,1),colors.khaki),
    #                    ('ALIGN',       (3,1),(3,1),'CENTER'),
    #                    ('BACKGROUND',  (3,2),(3,2),colors.beige),
    #                    ('ALIGN',       (3,2),(3,2),'LEFT'),
    #                    ])
    
    
    #datafile = csv.reader(open("02_02_kiwipycon_wifi_details.csv"))
    #table_data = list(datafile)
    #
    ## Prepare the TableStyle.
    #myTableStyle = TableStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.green),
    #                           ('LINEBELOW', (0,0), (-1,0), 2, colors.green),
    #                           ('LINEBELOW', (0,1), (-1,-1), 0.25, colors.black),
    #                           ('LINEBELOW', (0,-1), (-1,-1), 2, colors.green),
    #                           ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
    #                          )
    #
    ## add some conditional formatting to the table style
    #for i, data in enumerate(table_data):
    #    if not i:
    #        continue # skip header row
    #    for col in range(1,3):
    #        mb = int(data[col]) # megabytes uploaded or downloaded
    #        # color each cell from white at 0MB to a maximum of full red at 1000MB
    #        myTableStyle.add('BACKGROUND', (col, i), (col, i),
    #                         lerp(colors.white, colors.red, 0, 1000, min(mb, 1000)))
    #
    ## The table flowables. A couple of points to note:
    ## - repeatRows=1 means that 1 row (the header) will repeat at the top of each
    ## page that the table flows on to.
    ## - colWidths needs to be defined manually if you want the table to span the
    ## entire width of the frame.
    #myTable = Table(table_data, repeatRows=1,
    #                colWidths=[170/3.*mm]*3, style=myTableStyle)
    
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
    
    doc.build(story)
    
    print "done"
    
#genererFicheValidation(u"Intitulé du projet")
    
    
    



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
