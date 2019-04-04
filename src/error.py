#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                   error                                 ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014 Cédrick FAURY - Jean-Claude FRICOU
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
Module error
************

Gestion des erreurs

"""

import traceback

import sys, os
import util_path

from widgets import messageInfo
# 
import wx

import version



def MyExceptionHook(typ, value, traceb):
    """
    Handler for all unhandled exceptions.
  
    :param `etype`: the exception type (`SyntaxError`, `ZeroDivisionError`, etc...);
    :type `etype`: `Exception`
    :param string `value`: the exception error message;
    :param string `trace`: the traceback header, if any (otherwise, it prints the
     standard Python header: ``Traceback (most recent call last)``.
    """
#     frame = traceb.tb_frame
    print("\n", file=sys.stderr)
    traceback.print_tb(traceb)
    print("\nType : ",typ,"\n", file=sys.stderr)
    print("ValueError : ",value, file=sys.stderr)
#     print "".join(traceback.format_exception(typ, value, traceb))
    SendBugReport("%0A".join(traceback.format_exception(typ, value, traceb)))
    sys.exit()
    







# class RedirectErr:
#     #
#     # Redirige la sortie des erreurs pour envoyer l'erreur par mail
#     #
#     def __init__(self,stderr):
#         self.stderr=stderr
#         self.content = ""
#         self.error_occured=False
#         self.file_error=None
# 
#     def write(self,text):
#         #
#         # A la premiere erreur, on enregistrer la fonction de sortie
#         #
#         if not self.error_occured:
#             #
#             # Première erreur
#             # D'abord on enregistre la fonction atexit
#             import atexit
#             
#             atexit.register(SendBugReport)
#             # puis on ouvre le fichier qui contient les erreurs
#             self.file_error = open(util_path.ERROR_FILE,'w')
#             self.error_occured=True
#         if self.file_error is not None:
#             self.file_error.write(text)
#             self.file_error.flush()


# sys.stdout = open(util_path.LOG_FILE, "w")
# print ("test sys.stdout")


if True:#not "beta" in version.__version__:
    sys.excepthook = MyExceptionHook
#     sys.stderr=RedirectErr(sys.stderr)





def SendBugReport(traceb = ""):
    """
    Fonction qui envoie le rapport de bug par mail.
    """
    #
    # On ouvre le fichier qui contient les erreurs
    #
    import webbrowser, datetime

    message= "%s a rencontré une erreur et doit être fermé.\n\n" \
             "Voulez-vous envoyer un rapport d'erreur ?" %version.__appname__
    dlg=wx.MessageDialog(None,message,"Erreur", wx.YES_NO| wx.ICON_ERROR).ShowModal()
    if dlg==5103:#YES, on envoie le mail
        #
        # Définition du mail
        #
        
        messageInfo(None, "Rapport d'erreur", 
                    "Rédaction du rapport d'erreur\n\n" \
                    "Votre logiciel de messagerie va s'ouvrir\n" \
                    "pour rédiger un courrier de rapport d'erreur.\n\n" \
                    "Merci d'y indiquer le plus précisément possible\n" \
                    "comment s'est produite cette erreur\n" \
                    "ainsi que le moyen de la reproduire.\n" \
                    "Ne pas hesiter à joindre un fichier .prj, .seq ou .prg.\n\n" \
                    "L'équipe de développement de %s vous remercie pour votre participation." %version.__appname__)
        
        
        import util_path
        e_mail="cedrick.faury@ac-clermont.fr"
        now = str(datetime.datetime.now())
        subject = version.__appname__
        subject += " : rapport d'erreur du " + now
#        body="<HTML><BODY><P>"
        
        body = f"{version.__appname__} a rencontré une erreur le {now}"
        body += f"%0AVersion : {version.__version__}"
        body += "%0A%0ADescription d'une méthode pour reproduire l'erreur :"
        body += "%0A%0A%0A%0A%0A"
        body += "=================TraceBack====================%0A"
        #
        # Parcours du fichier
        #
        if os.path.isfile(util_path.ERROR_FILE):
            with open(util_path.ERROR_FILE,'r') as file_error:
                for line in file_error.readlines():
                    body+=line+"%0A"
        else:
            body+=traceb
        body += "==============================================%0A%0A"
        
#         sys.stdout.close()
#         file_log = open(util_path.LOG_FILE,'r')
# #         sys.stdout.seek(0, 0)
#         body += "%0A".join(file_log.readlines())
#         file_log.close()
#         sys.stdout = open(util_path.LOG_FILE, "w")

#         body += u"L'équipe de développement de %s vous remercie pour votre participation." %version.__appname__
#        body+="</P></BODY></HTML>"
#         file_error.close()
        print(body)
        body = body.replace('\n', '%0A')
        body = body.replace(' ', '%20')
        to_send="""mailto:%s?subject=%s&body=%s"""%(e_mail, subject, body)

        print("Envoi ...",to_send)
        print(webbrowser.open(to_send))

    