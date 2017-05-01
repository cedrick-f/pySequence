#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                             wx_pysequence                                ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2017 Cédrick FAURY

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

# Source :
# Cody Precord : "wxPythyon 2.8 Application Development Cookbook - 2010"


u"""
wx_pysequence.py

pySéquence : aide à la réalisation de fiches de séquence pédagogiques
et à la validation de projets

Copyright (C) 2011-2016
@author: Cedrick FAURY

"""


####################################################################################
#
#   Imports minimum et SplashScreen
#
####################################################################################
# Outils système
import os, sys
import util_path

print sys.version_info

# à décommenter pour forcer l'utilisation de wxpython 2.8 (ubuntu 14)
# if sys.platform != "win32":
#     import wxversion
#    wxversion.select('2.8')

import wx
    
import version

import threading
import socket
import select


FILE_ENCODING = sys.getfilesystemencoding()


class SingleInstApp(wx.App):
    u"""Application à instance unique :
        Vérifie qu'aucune autre instance de pySéquence n'est lancée.
        Si une autre instance est déjà lancée
        et qu'un nom de fichier est passé en argument
        envoie un message à l'instance lancée pour qu'elle ouvre le fichier.
        
        Source d'inspiration :
        Cody Precord : "wxPythyon 2.8 Application Development Cookbook - 2010"
    """
    PORT = 27115
    
    def OnInit(self):

        self.name = u"pySéquence-%s" % wx.GetUserId()
        self.instance = wx.SingleInstanceChecker(self.name)
    
        if self.instance.IsAnotherRunning():
            # Another instance so just send a message to
            # the instance that is already running.
            cmd = u"OpenWindow.%s.%s" % (self.name, GetArgFile())
            if not SendMessage(cmd, port = self.PORT):
                print u"Failed to send message!"
            return False
        
        else:
            # First instance so start IPC server
            try:
                self._ipc = IpcServer(self, self.name, self.PORT)
                self._ipc.start()
            except socket.error:
                print u"Erreur création serveur"
                pass
        
            self.splash = MySplashScreen()
            self.splash.Show()
            
            AddRTCHandlers()
            
#            frame = SingleAppFrame(None, "SingleApp")
#            frame.Show()
            return True
        
    def __del__(self):
        self.Cleanup()

#    def ShowSplash(self):
#        try:
#            self.splash = wx.SplashScreen(self.GetSplash(), wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_NO_TIMEOUT, 3000, None, -1,
#                             style = wx.BORDER_NONE | wx.STAY_ON_TOP)
#        except:
#            self.splash = wx.adv.SplashScreen(self.GetSplash(), wx.adv.SPLASH_CENTRE_ON_SCREEN|wx.adv.SPLASH_NO_TIMEOUT, 3000, None, -1,
#                             style = wx.BORDER_NONE | wx.STAY_ON_TOP)
##        self.splash.Show()
#        wx.Yield()
        
    def DestroySplashScreen(self):
        print "DestroySplashScreen"
        if self.splash is not None:
            self.splash.Show(False)
            self.splash.Destroy()
            self.splash = None
            
    def Cleanup(self):
        print "Cleanup"
        # Need to cleanup instance checker on exit
        if hasattr(self, '_checker'):
            del self._checker
        if hasattr(self, '_ipc'):
            self._ipc.Exit()
    
#    def Destroy(self):
#        self.Cleanup()
#        super(SingleInstApp, self).Destroy()
    
#    def IsOnlyInstance(self):
#        return not self._checker.IsAnotherRunning()


    def DoOpenFile(self, arg):
        """ Interface for subclass to open new window
            on ipc notification.
        """
        pass
    
    def GetFlash(self):
        """ 
        """
        return wx.NullBitmap()


    def DoOpenNewWindow(self, arg):
        """ Interface for subclass to open new window
            on ipc notification.
        """
        print u"DoOpenNewWindow", arg
        self.frame.AppelOuvrir(arg)
        

# class SingleInstApp2(wx.App):
#     """ App baseclass that only allows a single instance to
#         exist at a time.
#     """
#     def __init__(self, *args, **kwargs):
#         super(SingleInstApp, self).__init__(*args, **kwargs)
#         self.splash = None
#         
#         # Setup (note this will happen after subclass OnInit)
#         instid = u"%s-%s" % (self.GetAppName(), wx.GetUserId())
#         print "instid", instid
#         self._checker = wx.SingleInstanceChecker(instid)
#         if self.IsOnlyInstance():
#             # First instance so start IPC server
#             try:
#                 self._ipc = IpcServer(self, instid, 27115)
#                 self._ipc.start()
#             except socket.error:
#                 pass
#             
#             # Open a window
#             self.ShowSplash()
#             #self.DoOpenNewWindow()
#         else:
#             # Another instance so just send a message to
#             # the instance that is already running.
#             cmd = u"OpenWindow.%s.%s" % (instid, GetArgFile())
#             if not SendMessage(cmd, port=27115):
#                 print u"Failed to send message!"
# #            wx.CallAfter(sys.exit)
# 
#     def __del__(self):
#         self.Cleanup()
# 
#     def ShowSplash(self):
#         self.splash = wx.SplashScreen(self.GetSplash(), wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_NO_TIMEOUT, 3000, None, -1,
#                              style = wx.BORDER_NONE)
#         self.splash.Show()
#         wx.Yield()
#         
#     def DestroySplashScreen(self):
#         if self.splash is not None:
#             self.splash.Show(False)
#             self.splash.Destroy()
#             self.splash = None
#             
#     def Cleanup(self):
#         # Need to cleanup instance checker on exit
#         if hasattr(self, '_checker'):
#             del self._checker
#         if hasattr(self, '_ipc'):
#             self._ipc.Exit()
#     
#     def Destroy(self):
#         self.Cleanup()
#         super(SingleInstApp, self).Destroy()
#     
#     def IsOnlyInstance(self):
#         return not self._checker.IsAnotherRunning()
# 
#     def DoOpenNewWindow(self):
#         """ Interface for subclass to open new window
#             on ipc notification.
#         """
#         pass
# 
#     def DoOpenFile(self, arg):
#         """ Interface for subclass to open new window
#             on ipc notification.
#         """
#         pass
#     
#     def GetFlash(self):
#         """ 
#         """
#         return wx.NullBitmap()

###############################################################################
#
###############################################################################
class MySplashScreen(wx.SplashScreen):
    def __init__(self):
        bmp = self.GetSplash()
        wx.SplashScreen.__init__(self, bmp,
                                     wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                     6000, None, -1,
                                     style = wx.BORDER_NONE | wx.STAY_ON_TOP)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.CallLater(2, self.ShowMain)


    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the
        # main frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()


    def ShowMain(self):
        import objects_wx
        
        if self.fc.IsRunning():
            self.Raise()

#        wx.Log.SetLogLevel(0) # ?? Pour éviter le plantage de wxpython 3.0 avec Win XP pro ???
        self.locale = wx.Locale(wx.LANGUAGE_FRENCH)

        fichier = GetArgFile()

        self.frame = objects_wx.FenetrePrincipale(None, fichier)
        self.frame.Show()
        
#        self.SetTopWindow(self.frame)
#        
#        wx.CallAfter(self.Destroy)
        
#        wx.CallAfter(frame.ShowTip)
        
    
    ######################################################################################  
    def GetSplash(self):
        txt = u"Version : "+version.__version__
        
        bmp = wx.Bitmap(os.path.join(util_path.PATH, "splash.png"), wx.BITMAP_TYPE_PNG)
        w, h = bmp.GetWidth(), bmp.GetHeight()
        if w > 0: # w, h = -1, -1 sous Linux ... allez savoir pourquoi !
            dc = wx.MemoryDC(bmp)
            bmpv = wx.EmptyBitmapRGBA(w, h, 0,0,0, 0)
            dcv = wx.MemoryDC(bmpv)
            dcv.Clear()
        #    dcv.SetTextForeground(wx.Colour(255,30,30, 0))
            dcv.DrawText(txt, 50, 308)
            
        #    dc.DrawBitmap(bmpv, 0,0, False)
            dc.Blit(0,0,w,h,dcv,0,0) 
            
            dc.SelectObject(wx.NullBitmap)
            dcv.SelectObject(wx.NullBitmap)
        return bmp
        



######################################################################################  
def AddRTCHandlers():
    import wx.richtext as rt
    # make sure we haven't already added them.
    if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is not None:
        print u"AddRTCHandlers : déja fait"
        return
    
    # This would normally go in your app's OnInit method.  I'm
    # not sure why these file handlers are not loaded by
    # default by the C++ richtext code, I guess it's so you
    # can change the name or extension if you wanted...
    rt.RichTextBuffer.AddHandler(rt.RichTextHTMLHandler())
    rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())

    # ...like this
    rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler(name="Autre XML",
                                                       ext="ox",
                                                       type=99))

    # This is needed for the view as HTML option since we tell it
    # to store the images in the memory file system.
    wx.FileSystem.AddHandler(wx.MemoryFSHandler())
        
        
        
        
        
class IpcServer(threading.Thread):
    """Simple IPC Server"""
    def __init__(self, app, session, port):
        super(IpcServer, self).__init__()
        # Attributes
        self.keeprunning = True
        self.app = app
        self.session = session
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
        # Setup TCP socket
        self.socket.bind(('127.0.0.1', port))
        self.socket.listen(5)
        self.setDaemon(True)



    def run(self):
        """Run the server loop"""
        while self.keeprunning:
            try:
                client, addr = self.socket.accept()
                # Read from the socket
                # blocking up to 2 seconds at a time
                ready = select.select([client,],[], [],2)
                if ready[0]:
                    recieved = client.recv(4096)
                if not self.keeprunning:
                    break
                # If message ends with correct session
                # ID then process it.
                r = recieved.split(".")
                cmd = r[0]
                ses = r[1]
                arg = ".".join(r[2:])
                arg = arg.decode('utf-8')

                if ses == self.session:
                    if cmd == u'OpenWindow' and len(arg) > 0:
                        wx.CallAfter(self.app.DoOpenNewWindow, arg)
                    else:
                        # unknown command message
                        pass
                recieved = ''
            except socket.error, msg:
                print "TCP error! %s" % msg
                break
            
        # Shutdown the socket
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.socket.close()
    
    
    def Exit(self):
        self.keeprunning = False



def GetArgFile():
    u""" Vérifie si un fichier a été passé comme 1er argument
        au lancement du programme
        Et renvoi son nom
    """
    fichier = u""
    if len(sys.argv)>1: # un param�tre a �t� pass�
        parametre = sys.argv[1]

#           # on verifie que le fichier pass� en param�tre existe
        if os.path.isfile(parametre):
            fichier = parametre.decode(FILE_ENCODING)
            fichier = fichier.encode('utf-8')
          
    return fichier



def SendMessage(message, port):
    """Send a message to another instance of the app"""
    try:
        # Setup the client socket
        client = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM)
        client.connect(('127.0.0.1', port))
        client.send(message)
        client.shutdown(socket.SHUT_RDWR)
        client.close()
    except Exception, msg:
        return False
    else:
        return True

# Pour obtenir les log en cas d'erreur 
#  * iCCP: known incorrect sRGB profile
#         Pour corriger :
#             GIMP
#             To remove the embedded profile, go to the menu Image > Mode > Assign Color Profile and set it to RGB workspace(sRGB built-in).
#             To change the embedded profile, go to Image > Mode > Convert to Color Profile where you can choose a profile you already have loaded or load a new one from disk. 
#
#  * ou autre type d'erreur qui n'apparait pas dans le traceback

# import traceback
# class LogPrintStackStderr(wx.PyLog):
#     def doPrint( self, *args, **kwargs ):
#         sys.stderr.write( u': '.join(u'{}'.format(a) for a in args) )
#         sys.stderr.write( '\n' )
#         for k, v in kwargs.iteritems():
#             sys.stderr.write( u'{}: {}\n'.format(k,v) )
#      
#     def DoLogText( self, *args, **kwargs ):
#         sys.stderr.write( '*' * 78 + '\n' )
#         traceback.print_stack( file=sys.stderr )
#         self.doPrint( *args, **kwargs )
#  
#     def DoLogRecord( self, *args, **kwargs ):
#         sys.stderr.write( '*' * 78 + '\n' )
#         traceback.print_stack( file=sys.stderr )
#         self.doPrint( *args, **kwargs )
#          
#     def DoLogTextAtLevel( self, *args, **kwargs ):
#         sys.stderr.write( '*' * 78 + '\n' )
#         traceback.print_stack( file=sys.stderr )
#         self.doPrint( *args, **kwargs )
#         
if __name__ == '__main__':
    app = SingleInstApp(False)
#     wx.Log.SetActiveTarget( LogPrintStackStderr() )
    app.MainLoop()