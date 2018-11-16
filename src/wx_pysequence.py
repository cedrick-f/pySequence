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
Module ``wx_pysequence``
*************************

Module de demarrage de **pySéquence**.

**pySéquence** : aide à la réalisation de fiches de **Séquences** et **Progressions** pédagogiques
et à la validation de **Projets**.


"""


####################################################################################
#
#   Imports minimum et SplashScreen
#
####################################################################################
# Outils système
import os, sys
import threading
import socket
import select

import util_path

print(sys.version_info)

# à décommenter pour forcer l'utilisation de wxpython 2.8 (ubuntu 14)
# if sys.platform != "win32":
#     import wxversion
#    wxversion.select('2.8')

import wx

import version


# Sources :
# https://stackoverflow.com/questions/12471772/what-is-better-way-of-getting-windows-version-in-python
# https://stackoverflow.com/questions/44398075/can-dpi-scaling-be-enabled-disabled-programmatically-on-a-per-session-basis

def get_winver():
    wv = sys.getwindowsversion()
    if hasattr(wv, 'service_pack_major'):  # python >= 2.7
        sp = wv.service_pack_major or 0
    else:
        import re
        r = re.search("\s\d$", wv.service_pack)
        sp = int(r.group(0)) if r else 0
    return (wv.major, wv.minor, sp)


  
  
SSCALE = 1.0
if 'win' in sys.platform:
    import ctypes
#     import platform
#     print "platform", platform.platform()
    # Query DPI Awareness (Windows 10 and 8)
#     awareness = ctypes.c_int()
#     errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.addressof(awareness))
#     print "awareness", awareness.value
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#     print "screensize", screensize
    
    WIN_8 = (6, 2, 0)
    WIN_7 = (6, 1, 0)
    WIN_SERVER_2008 = (6, 0, 1)
    WIN_VISTA_SP1 = (6, 0, 1)
    WIN_VISTA = (6, 0, 0)
    WIN_SERVER_2003_SP2 = (5, 2, 2)
    WIN_SERVER_2003_SP1 = (5, 2, 1)
    WIN_SERVER_2003 = (5, 2, 0)
    WIN_XP_SP3 = (5, 1, 3)
    WIN_XP_SP2 = (5, 1, 2)
    WIN_XP_SP1 = (5, 1, 1)
    WIN_XP = (5, 1, 0)
    
#     print "windows", get_winver()
    
    if get_winver() >= WIN_8:
        # Set DPI Awareness  (Windows 10 and 8)
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
        # the argument is the awareness level, which can be 0, 1 or 2:
        # for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)
    elif get_winver() >= WIN_VISTA:
        # Set DPI Awareness  (Windows 7 and Vista)
        success = user32.SetProcessDPIAware()
        # behaviour on later OSes is undefined, although when I run it on my Windows 10 machine, it seems to work with effects identical to SetProcessDpiAwareness(1)

    screensize2 = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#     print "screensize2", screensize2
    
    # Facteur d'échelle : 
    # tout ce qui est sensé être en PIXEL doit être multiplié par ce facteur
    SSCALE = 1.0*screensize2[0]/screensize[0]
    print(("Facteur d'echelle :", SSCALE))
    


FILE_ENCODING = sys.getfilesystemencoding()


class SingleInstApp(wx.App):
    """Application à instance unique :
        Vérifie qu'aucune autre instance de pySéquence n'est lancée.
        Si une autre instance est déjà lancée
        et qu'un nom de fichier est passé en argument
        envoie un message à l'instance lancée pour qu'elle ouvre le fichier.
        
        Source d'inspiration :
        Cody Precord : "wxPythyon 2.8 Application Development Cookbook - 2010"
    """
    
    PORT = 27115

    def OnInit(self):
        self.locale = wx.Locale(wx.LANGUAGE_FRENCH) # Sans ça, il y a des erreurs sur certains PC ...
#         wx.Log.SetLogLevel(0) # ?? Pour éviter le plantage de wxpython 3.0 avec Win XP pro ???
        
        self.name = "pySéquence-%s" % wx.GetUserId()
        self.instance = wx.SingleInstanceChecker(self.name)

        if self.instance.IsAnotherRunning():
            # Another instance so just send a message to
            # the instance that is already running.
            options, fichier = GetArgs()
            
            if os.path.isfile(fichier):
                cmd = "OpenWindow.%s.%s" % (self.name, fichier)
                if not SendMessage(cmd, port = self.PORT):
                    print("Failed to send message!")
            else:
                wx.MessageBox("pySéquence semble être déjà lancé !", "pySéquence")
                
            return False

        else:
            # First instance so start IPC server
            try:
                self._ipc = IpcServer(self, self.name, self.PORT)
                self._ipc.start()
            except socket.error:
                print("Erreur création serveur")
            except:
                pass
        
            self.splash = MySplashScreen(self)
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
        print("DestroySplashScreen")
        if self.splash is not None:
            self.splash.Show(False)
            self.splash.Destroy()
            self.splash = None
            
    def Cleanup(self):
        print("Cleanup")
        
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
        print("DoOpenNewWindow", arg)
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
# try:
#     from agw import advancedsplash as AS
# except ImportError: # if it's not there locally, try the wxPython lib.
#     import wx.lib.agw.advancedsplash as AS

# Pour passage Python 3
try:
    import wx.adv as adv
except:
    adv = wx

class MySplashScreen(adv.SplashScreen):
    def __init__(self, parent):
        bmp = self.GetSplash()
        adv.SplashScreen.__init__(self, bmp,
                                 adv.SPLASH_CENTRE_ON_SCREEN | adv.SPLASH_TIMEOUT,
                                 6000, None, -1,
                                 style = wx.BORDER_NONE | wx.STAY_ON_TOP)
        
#         AS.AdvancedSplash.__init__(self, None, bitmap=bmp, timeout=6000,
#                                       agwStyle=AS.AS_TIMEOUT |
#                                       AS.AS_CENTER_ON_PARENT)# |
# #                                       AS.AS_SHADOW_BITMAP,
# #                                       shadowcolour=wx.WHITE)
        
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.OnClose)
#         self.ShowMain()
        self.fc = wx.CallLater(2, self.ShowMain) #viré au passage à py3


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
#         self.locale = wx.Locale(wx.LANGUAGE_FRENCH)

        options, fichier = GetArgs()

        self.frame = objects_wx.FenetrePrincipale(None, fichier, SSCALE, options)
        self.frame.Show()
        self.parent.frame = self.frame
        
#        self.SetTopWindow(self.frame)
#        
#        wx.CallAfter(self.Destroy)
        
#        wx.CallAfter(frame.ShowTip)
        
    
    ######################################################################################  
    def GetSplash(self):
        txt = "Version : "+version.__version__

        bmp = wx.Bitmap(os.path.join(util_path.PATH, "splash.png"), wx.BITMAP_TYPE_PNG)
        return bmp
    
#         w, h = bmp.GetWidth(), bmp.GetHeight()
#         if w > 0: # w, h = -1, -1 sous Linux ... allez savoir pourquoi !
#             dc = wx.MemoryDC(bmp)
#             bmpv = wx.EmptyBitmapRGBA(w, h, 0,0,0, 0)
#             dcv = wx.MemoryDC(bmpv)
#             dcv.Clear()
#         #    dcv.SetTextForeground(wx.Colour(255,30,30, 0))
#             dcv.DrawText(txt, 50, 308)
#             
#         #    dc.DrawBitmap(bmpv, 0,0, False)
#             dc.Blit(0,0,w,h,dcv,0,0) 
#             
#             dc.SelectObject(wx.NullBitmap)
#             dcv.SelectObject(wx.NullBitmap)
#         return bmp
        



######################################################################################  
def AddRTCHandlers():
    import wx.richtext as rt
    # make sure we haven't already added them.
    if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is not None:
        print("AddRTCHandlers : déja fait")
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
            
                path = arg
                
                if ses == self.session:
                    if cmd == 'OpenWindow' and len(path) > 0:
                        wx.CallAfter(self.app.DoOpenNewWindow, path)
                    else:
                        # unknown command message
                        pass
                recieved = ''
            except socket.error as msg:
                print("TCP error! %s" % msg)
                break

        # Shutdown the socket
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.socket.close()


    def Exit(self):
        self.keeprunning = False



def GetArgs():
    """ Vérifie si un fichier a été passé comme 1er argument
        au lancement du programme
        Et renvoi son nom
    """
    fichier = ""
    options = []
    if len(sys.argv)>1: # un paramètre a été passé
        for parametre in sys.argv[1:]:

            if parametre[0] == "-" and len(parametre) > 1: # Il y a une option
                options.extend(list(parametre[1:]))
            
            # on verifie que le fichier passé en paramètre existe
            if os.path.isfile(parametre):
                fichier = parametre.decode(FILE_ENCODING)
                fichier = fichier.encode('utf-8')
                fichier = util_path.verifierPath(fichier)
    return options, fichier


# # https://stackoverflow.com/questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp
# def Get_HWND_DPI(window_handle):
#     #To detect high DPI displays and avoid need to set Windows compatibility flags
#     import os
#     if os.name == "nt":
#         from ctypes import windll, pointer, wintypes
#         try:
#             windll.shcore.SetProcessDpiAwareness(1)
#         except Exception:
#             pass  # this will fail on Windows Server and maybe early Windows
#         DPI100pc = 96  # DPI 96 is 100% scaling
#         DPI_type = 0  # MDT_EFFECTIVE_DPI = 0, MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2
#         winH = wintypes.HWND(window_handle)
#         monitorhandle = windll.user32.MonitorFromWindow(winH, wintypes.DWORD(2))  # MONITOR_DEFAULTTONEAREST = 2
#         X = wintypes.UINT()
#         Y = wintypes.UINT()
#         try:
#             windll.shcore.GetDpiForMonitor(monitorhandle, DPI_type, pointer(X), pointer(Y))
#             return X.value, Y.value, (X.value + Y.value) / (2 * DPI100pc)
#         except Exception:
#             return 96, 96, 1  # Assume standard Windows DPI & scaling
#     else:
#         return None, None, 1  # What to do for other OSs?




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
    except Exception as msg:
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

# Suite utile pour débugger (davantage de messages !)
import traceback
class LogPrintStackStderr(wx.Log):
    def doPrint( self, *args, **kwargs ):
        sys.stderr.write( u': '.join(u'{}'.format(a) for a in args) )
        sys.stderr.write( '\n' )
        for k, v in kwargs.items():
            sys.stderr.write( u'{}: {}\n'.format(k,v) )
      
    def DoLogText( self, *args, **kwargs ):
        sys.stderr.write( '*' * 78 + '\n' )
        traceback.print_stack( file=sys.stderr )
        self.doPrint( *args, **kwargs )
  
    def DoLogRecord( self, *args, **kwargs ):
        sys.stderr.write( '*' * 78 + '\n' )
        traceback.print_stack( file=sys.stderr )
        self.doPrint( *args, **kwargs )
          
    def DoLogTextAtLevel( self, *args, **kwargs ):
        sys.stderr.write( '*' * 78 + '\n' )
        traceback.print_stack( file=sys.stderr )
        self.doPrint( *args, **kwargs )
#         
if __name__ == '__main__':
    try:
        app = SingleInstApp(False)
        
#         wx.Log.SetActiveTarget( LogPrintStackStderr() ) # Pour débug
        app.MainLoop()
    except SystemExit:
        sys.exit(0)
    