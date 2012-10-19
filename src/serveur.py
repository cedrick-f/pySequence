#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                serveur                                  ##
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
import sys
import os
import SocketServer
import socket
import threading
    
    
class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(320, 350))

        getfile = os.path.abspath(sys.argv[1])
#        print getfile
        fopen = open (getfile, 'r')
        fread = fopen.read()

        panel = wx.Panel(self, -1)
        self.static = wx.StaticText(panel, -1, fread, (45, 25), style=wx.ALIGN_CENTRE)
        self.Centre()
        
FILE_ENCODING = sys.getfilesystemencoding()

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
#        print "ThreadedTCPRequestHandler"
        data = self.request.recv(1024)
        cur_thread = threading.currentThread()

#        print "data =",data
        gfile = unicode(data, FILE_ENCODING)
#        data = data.split()
#        gfile = os.path.abspath(data[-1])
#        gfile = unicode(gfile, 'cp1252')
#        print gfile
        
        
        
        self.server.app.AppelOuvrir(gfile)
#        fopen = open(gfile, 'r')
#        fread = fopen.read()
#        self.server.app.static.SetLabel(fread)
        #Note to the self.server.app
        response = 'string length: %d' % len(data)

        print 'responding to',data,'with',response
        self.request.send(response)
        
    
        
        
        
        
        
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    stopped = False
    allow_reuse_address = True

    def serve_forever(self):
        while not self.stopped:
            self.handle_request()

    def force_stop(self):
        self.server_close()
        self.stopped = True


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(message)
    response = sock.recv(1024)
    print "Received: %s" % response
    sock.close()


def start_server(host, port):

    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.setDaemon(True)
    server_thread.start()

    return server


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'test')
        frame.Show(True)
        server.app = frame
        #Note the server.app
        self.SetTopWindow(frame)
        return True



def main():
    app = MyApp(0)
    app.MainLoop()

if __name__ == '__main__':
    HOST, PORT = socket.gethostname(), 61955

    server = None
    try:
        client(HOST, PORT, ' '.join(sys.argv))
        sys.exit()
    except socket.error:
        server = start_server(HOST, PORT)
        main()
