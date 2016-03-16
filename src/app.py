#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                single                                   ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2016 Cédrick FAURY

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


import wx
import threading
import socket
import select
import os, sys

FILE_ENCODING = sys.getfilesystemencoding()

class SingleInstApp(wx.App):
    """ App baseclass that only allows a single instance to
        exist at a time.
    """
    def __init__(self, *args, **kwargs):
        super(SingleInstApp, self).__init__(*args, **kwargs)
        self.splash = None
        
        # Setup (note this will happen after subclass OnInit)
        instid = u"%s-%s" % (self.GetAppName(), wx.GetUserId())
        print "instid", instid
        self._checker = wx.SingleInstanceChecker(instid)
        if self.IsOnlyInstance():
            # First instance so start IPC server
            try:
                self._ipc = IpcServer(self, instid, 27115)
                self._ipc.start()
            except socket.error:
                pass
            
            # Open a window
            self.ShowSplash()
            #self.DoOpenNewWindow()
        else:
            # Another instance so just send a message to
            # the instance that is already running.
            cmd = u"OpenWindow.%s.%s" % (instid, GetArgFile())
            if not SendMessage(cmd, port=27115):
                print u"Failed to send message!"
#            wx.CallAfter(sys.exit)

    def __del__(self):
        self.Cleanup()

    def ShowSplash(self):
        self.splash = wx.SplashScreen(self.GetSplash(), wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_NO_TIMEOUT, 3000, None, -1,
                             style = wx.BORDER_NONE)
        self.splash.Show()
        wx.Yield()
        
    def DestroySplashScreen(self):
        if self.splash is not None:
            self.splash.Show(False)
            self.splash.Destroy()
            self.splash = None
            
    def Cleanup(self):
        # Need to cleanup instance checker on exit
        if hasattr(self, '_checker'):
            del self._checker
        if hasattr(self, '_ipc'):
            self._ipc.Exit()
    
    def Destroy(self):
        self.Cleanup()
        super(SingleInstApp, self).Destroy()
    
    def IsOnlyInstance(self):
        return not self._checker.IsAnotherRunning()

    def DoOpenNewWindow(self):
        """ Interface for subclass to open new window
            on ipc notification.
        """
        pass

    def DoOpenFile(self, arg):
        """ Interface for subclass to open new window
            on ipc notification.
        """
        pass
    
    def GetFlash(self):
        """ 
        """
        return wx.NullBitmap()


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
    """ Vérifie si un fichier a été passé comme 1er argument
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
