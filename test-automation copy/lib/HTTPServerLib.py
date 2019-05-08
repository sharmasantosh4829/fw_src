import os 
import sys
import time
from datetime import datetime
from time import strftime
import traceback
import threading
import thread
import signal

SERVER_DIR = ""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class startThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    
    def run(self):
        self._target(*self._args)


class HTTPServerHandler(BaseHTTPRequestHandler):
            
    def do_GET(self):
        buildFileName = ""
        print "do_GET", self.path
        try:

            if self.path.find("?") > -1:
                buildFileName = self.path.split("?")[0]
            else:
                buildFileName = self.path
            buildFileName = buildFileName.strip("/")
            fp = open(os.path.join(SERVER_DIR, buildFileName), "rb")
            self.send_response(200)
            partFile = fp.read()                
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Length', '%d'%len(partFile))
            self.end_headers()
            self.wfile.write(partFile)
            fp.close()
            return
        
        except IOError:
            print sys.exc_info()
        except:
            print sys.exc_info()
    
    def do_HEAD(self):
        buildFileName = ""
        try:
            if self.path.find("?") > -1:
                buildFileName = self.path.split("?")[0]
                buildFileName = buildFileName.strip("/")
                fp = open(os.path.join(SERVER_DIR, buildFileName), "rb")
                
                self.send_response(200)
                partFile = fp.read()                
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Length', '%d'%len(partFile))
                self.end_headers()
                self.wfile.write(partFile)
                fp.close()
                return
        
        except IOError:
            print sys.exc_info()
        except:
            print sys.exc_info()


class HTTPServerLib():

    def __init__(self, serverPort = 8005, serverDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("HTTPServerLib.py")), os.pardir)), "builds")):
        self.log = False
        self.serverPort = serverPort
        global SERVER_DIR
        SERVER_DIR = serverDir
        self.serverRunning = False
        self.httpServerThread = None
        self.handler = HTTPServerHandler
        
    def setLogger(self, loggerObject):
        self.log = loggerObject
            
    def start_server(self):
        try:
            self.server = HTTPServer(("", self.serverPort), self.handler)
            self.threadId = thread.get_ident()
            if self.log:
                self.log.Log("started HTTP server on port %s..."%self.serverPort)
            self.server.serve_forever()
        except KeyboardInterrupt:
            if self.log:
                self.log.Log("^C received, shutting down HTTP server")
                print "^C received, shutting down HTTP server"
            self.server.socket.close()

        
    def startHttpServer(self):
        if self.serverRunning == False:
            self.httpServerThread = startThread(self.start_server)
            self.httpServerThread.start()
            self.serverRunning = True
        else:
            print "Http Server is already running"
            self.log.Log("Http Server is already running")
    
    def stopHttpServer(self):
        if self.serverRunning == True:
            self.server.shutdown()
            self.serverRunning = False
            self.httpServerThread = None
        else:
            pass

    def setServerHandler(self,handler):
        self.handler = handler

if __name__ == '__main__':
    pass