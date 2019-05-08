import socket,struct,sys,time
import threading
from threading import Thread
import thread
import select

from Logger import *
from WirelessProfiler import *

class startThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    
    def run(self):
        self._target(*self._args)



class MulticastListener (WirelessProfiler):
    def __init__(self):
        WirelessProfiler.__init__(self)
        self.BUFFER_SIZE = 1500
        self.result = ""
        self.serverThreadLock = thread.allocate_lock()
        self.stopServer = False # This is a shared variable .. guard it with serverThreadLock
        self.serverThread = None
        self.logger = False
        self.localIP = ""
        
    def setLogger(self, loggerObject):
        self.logger = loggerObject
        
    def Connect(self, ssidName, securityMode = "OPEN", passPhrase = "", wirelessInterface = "Wireless Network Connection"):
        self.ssidName = ssidName
        self.passPhrase = passPhrase
        self.securityMode = securityMode
        self.wirelessInterface =  wirelessInterface
        if self.securityMode == "WPA2PSK":
            self.createWirelessProfile(self.ssidName, "WPA2PSK", self.passPhrase)
        elif self.securityMode == "OPEN":
            self.createWirelessProfile(self.ssidName, "none")
        time.sleep(3)
        self.addWirelessProfile(self.ssidName)
        time.sleep(3)
        (result, message) = self.connectToWirelessProfile(self.ssidName, self.wirelessInterface)
        time.sleep(10)
        if result == True:
            self.localIP = message
            return True
        else:
            if self.logger:
                self.logger.Log("Could not connect to ", self.ssidName)
                self.logger.LogException()
            else:
                print "Could not connect to ", self.ssidName
            return False

            
    def Disconnect(self):
        self.disconnectNetwork()
        return True
        

    def start_server(self, group = "239.255.255.250", Port = 1900):
        self.group = group
        self.Port = Port
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.logger:
            self.logger.Log("Socket Created")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mreq = struct.pack('=4sL', socket.inet_aton(self.group), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        try:
            sock.bind((self.localIP, self.Port))
        except socket.error:
            if self.logger:
                self.logger.Log("Bind failed")
                self.logger.LogException()
            self.serverThread = None
            return
        if self.logger:
            self.logger.Log("Socket bind complete")

        if self.logger:
            self.logger.Log("Socket now waiting to receive on port ", self.Port)

        read_list = [sock]
        while True:
            try:
                self.serverThreadLock.acquire()
                stopFlag = self.stopServer
                self.serverThreadLock.release()
                if stopFlag == True:
                    if self.logger:
                        self.logger.Log("stop server request received, shutting down MulticastListener")
                    sock.close()
                    break

                readable, writable, errored = select.select(read_list, [], [], 5)
                for s in readable:
                    if s is sock:
                        data, srv_sock = s.recvfrom(self.BUFFER_SIZE)
                        srv_addr, srv_srcport = srv_sock[0], srv_sock[1]
                        if self.logger:
                            self.logger.Log("From", srv_addr, ":", data)
            except:
                if self.logger:
                    self.logger.LogException()
                sock.close()
    
    def startMulticastListener(self):
        if self.serverThread != None:
            if self.logger:
                self.logger.Log("Receiver is already running .. so stopping it first")
            self.stopMulticastListener()
        if self.serverThread == None:
            self.logFileName = "MulticastListener" + strftime("%Y-%m-%d_%H-%M-%S") + ".log"
            self.logger = Logger(self.logFileName)
            self.serverThreadLock.acquire()
            self.stopServer = False
            self.serverThreadLock.release()
            self.serverThread = startThread(self.start_server)
            self.serverThread.start()
        return True

    def stopMulticastListener(self):
        self.serverThreadLock.acquire()
        self.stopServer = True
        self.serverThreadLock.release()
        self.serverThread.join(60)
        self.serverThread = None
        return True


if __name__=='__main__':
    pass
    
