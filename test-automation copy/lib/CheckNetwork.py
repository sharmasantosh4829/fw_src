import time, os, re
import sys, threading, thread, platform
import xmlrpclib, socket, ssl, traceback
import signal
sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("CheckNetwork.py")), os.pardir)), "header"))
sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("CheckNetwork.py")), os.pardir)), "lib"))

from Logger import *

from WirelessProfiler import *
import httplib
import urllib
import urllib2, cookielib
import SerialCommunication
from urllib2 import HTTPError
from TestHouseAutomationConsts import *
from LocalDiscovery import *


class CheckNetwork():
    def __init__(self):
        self.MAIN_ROUTER_SSID = ""
        self.ROUTERS_LIST = []
        self.WEMO_SWITCHES_LIST = []
        self.WEMO_INSIGHTS_LIST = []
        self.EXTENDERS_LIST = []
        self.WEMO_SLOWCOOKER_LIST = []
        self.DOUBLE_NAT_ROUTER_LIST = []
        self.wiPro = WirelessProfiler()
        self.logger = False
        self.homeConfig = {}

    def setLogger(self, logObject):
        if logObject != None:
            self.logger = logObject
        else:
            raise Exception("None type LogObject sent as Input")


    def GetNetworkDevices(self):
        if isinstance(self.homeConfig, dict) and self.homeConfig != {}:
            for devices in self.homeConfig:
                if self.homeConfig[devices]["DeviceType"] == "MAIN_ROUTER":
                    self.MAIN_ROUTER_FRIENDLY_NAME = devices
                    self.MAIN_ROUTER_SSID = self.homeConfig[devices]["SSID"]
                if self.homeConfig[devices]["DeviceType"] == "EXTENDER":
                    self.EXTENDERS_LIST.append(devices)
                if self.homeConfig[devices]["DeviceType"] == "WEMO_SWITCH":
                    self.WEMO_SWITCHES_LIST.append(devices)
                if self.homeConfig[devices]["DeviceType"] == "WEMO_INSIGHT":
                    self.WEMO_INSIGHTS_LIST.append(devices)
                if self.homeConfig[devices]["DeviceType"] == "WEMO_SLOWCOOKER":
                    self.WEMO_SLOWCOOKER_LIST.append(devices)
                if self.homeConfig[devices]["DeviceType"] == "DOUBLE_NAT_ROUTER":
                    self.WEMO_SLOWCOOKER_LIST.append(devices)

    def CheckNetworkHealth(self, homeConfig):
        try:
            self.homeConfig = homeConfig
            if self.logger != False:
                self.logger.Log("Dict:",self.homeConfig)
            if isinstance(self.homeConfig, dict) and self.homeConfig != {}:
                #self.GetNetworkDevices()
                for devices in self.homeConfig:
                    if self.homeConfig[devices]["DeviceType"] == "MAIN_ROUTER":
                        self.MAIN_ROUTER_FRIENDLY_NAME = devices
                        self.MAIN_ROUTER_SSID = self.homeConfig[devices]["SSID"]
            else:
                raise Exception("Parameter passed is not a Dict or Dict is empty")
            #self.logger.Log self.homeConfig
            #Finding Main Router
            if self.MAIN_ROUTER_SSID != "":
                if self.logger != False:
                    self.logger.Log( "Found Main Router")
            else:
                self.homeConfig[self.MAIN_ROUTER_FRIENDLY_NAME]["result"] = "ERROR"
                return self.homeConfig
            if self.logger != False:
                self.logger.Log( "Checking Network Health of MAIN_ROUTER")
            if self.CheckNetworkRouterHealth(self.homeConfig[self.MAIN_ROUTER_FRIENDLY_NAME]):
                self.homeConfig[self.MAIN_ROUTER_FRIENDLY_NAME]["result"] = "OK"
            else:
                self.homeConfig[self.MAIN_ROUTER_FRIENDLY_NAME]["result"] = "ERROR"
                #self.homeConfig["result"] = False
                if self.logger != False:
                    self.logger.Log("Returned Dict: \n%s"%self.homeConfig)
                return self.homeConfig
            '''
            if self.logger != False:
                self.logger.Log( "Checking Network Health of Extender's")
            if self.EXTENDERS_LIST == []:
                if self.logger != False:
                    self.logger.Log( "No Extenders found in this Setup")
            else:
                for list in self.EXTENDERS_LIST:
                    if self.CheckNetworkRouterHealth(self.homeConfig[list]):
                        self.homeConfig[list]["NPR"] = "OK"
                    else:
                        self.homeConfig[list]["NPR"] = "ERROR"
            if self.logger != False:
                self.logger.Log( "Checking Network Health of DOUBLE_NAT_ROUTER's")
            if self.DOUBLE_NAT_ROUTER_LIST == []:
                if self.logger != False:
                    self.logger.Log( "No DOUBLE_NAT_ROUTER'S found in this Setup")
            else:
                for list in self.DOUBLE_NAT_ROUTER_LIST:
                    if self.CheckNetworkRouterHealth(self.homeConfig[list]):
                        self.homeConfig[list]["NPR"] = "OK"
                    else:
                        self.homeConfig[list]["NPR"] = "ERROR"
            '''
            #self.homeConfig["result"] = True
            if self.logger != False:
                self.logger.Log("Returned Dict: \n%s"%self.homeConfig)
            return self.homeConfig
        except:
            if self.logger != False:
                self.logger.Log(sys.exc_info()[0])
                self.logger.Log(sys.exc_info()[1])
                self.logger.Log(traceback.extract_tb(sys.exc_info()[2]))
            raise Exception("Unable to Check Network Health")
        finally:
            pass

    def CheckNetworkRouterHealth(self,routerDict):
        if self.logger != False:
            self.logger.Log( "connecting to the  Router %s" %routerDict["SSID"])
        if routerDict["SSID"] != "" and routerDict["SecurityMode"] != "" and routerDict["WirelessPassphrase"] != "":
            try:
                self.wiPro.createWirelessProfile(routerDict["SSID"],routerDict["SecurityMode"], routerDict["WirelessPassphrase"], None, None)
            except:
                raise Exception("Unable to Connect to the Wireless Profile")
            try:
                self.wiPro.addWirelessProfile(routerDict["SSID"])
            except:
                raise Exception("Unable to add Wireless Profile")
            try:
                connectionStatus, ipAddress = self.wiPro.connectToWirelessProfile(routerDict["SSID"], WIRELESS_INTERFACE_NAME)
                if connectionStatus == True:
                    self.logger.Log( "Successfully Connected to %s" %self.homeConfig[self.MAIN_ROUTER_SSID]["SSID"])
                    self.logger.Log( "IP: %s"%ipAddress)
                    time.sleep(10)
                    self.wiPro.disconnectNetwork()
                    return True
                else:
                    return False
            except:
                if self.logger != False:
                    self.logger.Log(sys.exc_info()[0])
                    self.logger.Log(sys.exc_info()[1])
                    self.logger.Log(traceback.extract_tb(sys.exc_info()[2]))
                raise Exception("Unable to Check Router Health")
        else:
            return False
