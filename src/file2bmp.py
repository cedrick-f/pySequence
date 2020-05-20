#!/usr/bin/env python
# -*- coding: utf-8 -*-


##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                 pysequence                              ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014 Cédrick FAURY - Jean-Claude FRICOU
##
## pySéquence : aide à la construction
## de Séquences et Progressions p�dagogiques
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
module file2bmp
***********
"""

import os, sys, subprocess
import wx
import fitz
import tempfile
from xhtml2pdf import pisa


file_types = {"img" : (".jpg", ".png"),
              "pdf" : ('.pdf',),
              "html" : ('.html',),
            }

def img2bmp(nf, defaut = wx.NullBitmap):
    try:
        bmp = wx.Image(nf).ConvertToBitmap()
    except:
        bmp = defaut
    return bmp



def pdf2bmp(nf, defaut = wx.NullBitmap):
    # source : https://pymupdf.readthedocs.io/en/latest/tutorial/
#     print(nf)
    try:
        doc = fitz.open(nf)
        page = doc.loadPage(0)
        pix = page.getPixmap()
        if pix.alpha:
            bmp = wx.Bitmap.FromBufferRGBA(pix.width, pix.height, pix.samples)
        else:
            bmp = wx.Bitmap.FromBuffer(pix.width, pix.height, pix.samples)
    except:
        bmp = defaut
    return bmp



def html2bmp(nf , defaut = wx.NullBitmap):
    with open(nf,'r', encoding='utf-8') as f:
        sourceHtml = f.read()
        
    with tempfile.NamedTemporaryFile() as resultFile:
#     with open(nomFichierPDF, "w+b") as resultFile:
        # convert HTML to PDF
#         print(sourceHtml)
        try:
            pisaStatus = pisa.CreatePDF(sourceHtml,                # the HTML to convert
                                        dest=resultFile,
                                        show_error_as_pdf = True)           # file handle to recieve result
            return pdf2bmp(resultFile.name, defaut)
        except:
            return defaut
      
    
#############################################################################
def file2bmp(nf, defaut = wx.NullBitmap):
    ext = os.path.splitext(nf)[1]
    if ext.lower() in file_types['img']:
        return img2bmp(nf, defaut)
    elif ext in file_types['pdf']:
        return pdf2bmp(nf, defaut)
    elif ext in file_types['html']:
        return pdf2bmp(nf, defaut)
    else:
        return defaut






def pdf2imgfile(nf, defaut = wx.NullBitmap, ext = ".png"):
    # source : https://pymupdf.readthedocs.io/en/latest/tutorial/
    of = os.path.splitext(nf)[0]+ext
    try:
        doc = fitz.open(nf)
        page = doc.loadPage(0)
        pix = page.getPixmap()
        pix.writeImage(of)
    except:
        return 
    return of


def html2imgfile(nf , defaut = wx.NullBitmap, ext = ".png"):
    with open(nf,'r', encoding='utf-8') as f:
        sourceHtml = f.read()
        
    with tempfile.NamedTemporaryFile() as resultFile:
#     with open(nomFichierPDF, "w+b") as resultFile:
        try:
            pisaStatus = pisa.CreatePDF(sourceHtml,                # the HTML to convert
                                        dest=resultFile,
                                        show_error_as_pdf = True)           # file handle to recieve result
            return pdf2imgfile(resultFile.name, defaut)
        except:
            return defaut
        
        
        
def wximg2file(img):
    temp_name = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()))
#     print(temp_name)
#     with tempfile.NamedTemporaryFile() as resultFile:
    img.SaveFile(temp_name, wx.BITMAP_TYPE_PNG)
    return temp_name, True
    
    
#############################################################################
def file2imgfile(nf, defaut = ""):
    """ Renvoie le noms du fichier image obtenu
        et un booléen indiquant s'il s'agit d'un fichier temporaire
        
        ATTENTION : les fichiers temporaires doivent être effacés
    """
    ext = os.path.splitext(nf)[1].lower()
    if ext in file_types['img']:
        return nf, False
    
    elif ext in file_types['pdf']:
        return pdf2imgfile(nf), True
    
    elif ext in file_types['html']:
        return html2imgfile(nf), True
    
