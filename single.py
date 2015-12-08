'''
Created on 5 déc. 2015

@author: Cedrick
'''

import wx
import threading
import socket
import select

class SingleInstApp(wx.App):
    """App baseclass that only allows a single instance to
    exist at a time.
    """
    def __init__(self, *args, **kwargs):
        super(SingleInstApp, self).__init__(*args, **kwargs)
        # Setup (note this will happen after subclass OnInit)
        instid = "%s-%s" % (self.GetAppName(), wx.GetUserId())
        self._checker = wx.SingleInstanceChecker(instid)
        if self.IsOnlyInstance():
            # First instance so start IPC server
            self._ipc = IpcServer(self, instid, 27115)
            self._ipc.start()
            # Open a window
            self.DoOpenNewWindow()
        else:
            # Another instance so just send a message to
            # the instance that is already running.
            cmd = "OpenWindow.%s" % instid
            if not SendMessage(cmd, port=27115):
                print "Failed to send message!"


    def __del__(self):
        self.Cleanup()


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
        """Interface for subclass to open new window
        on ipc notification.
        """
        pass
    



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
                if recieved.endswith(self.session):
                    if recieved.startswith('OpenWindow'):
                        wx.CallAfter(self.app.DoOpenNewWindow)
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


