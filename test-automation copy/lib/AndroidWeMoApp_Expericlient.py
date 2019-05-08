#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import logging
import traceback
from ExperitestClient import Client
from Logger import *
from AndroidWeMoApp_Generic import *

class AndroidWeMoApp_Expericlient:

    def __init__(self,host,port,smartPhoneDeviceName):    
        """
        Initialization function for the AndroidWeMoApp_AirPurifier 
        @param smartPhoneDeviceName: The name of the Smart Phone under test
        @type smartPhoneDeviceName: String
        @param smartPhoneDeviceName: The name of the Smart Phone under test
        @type smartPhoneDeviceName: String
        """
        self.ExperitestClient = Client() 
        self.ExperitestClient.init(host,port)
        #self.ExperitestClient.setApplicationTitle(smartPhoneDeviceName)
        self.SmartPhoneInfo = self.ExperitestClient.getDevicesInformation() 
        #self.ExperitestClient.setProjectBaseDirectory(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("AndroidWeMoApp_Generic.py")), os.pardir)), "lib", "AndroidWeMoImages"))
        self.WeMoAppLog = Logger(os.path.basename("AndroidWeMoApp_Generic.py").replace(".py","_%s_"%smartPhoneDeviceName.split(":")[-1].strip()+strftime("%Y-%m-%d_%H-%M-%S")+".log"))
        #self.AndroidGeneric = AndroidWeMoApp_Generic(smartPhoneDeviceName,smartPhonePort)
               
        
    ###################
    #Generic Functions#
    ###################    
         
    def _verifyElementFoundbyClickingRefresh(self,zone,element,index=0,refresh=True):
        """
        Verify the element is found after clicking on the Refresh button
        @param zone:The zone to search for an element
        @type zone:String
        @param element:The element to be searched for
        @type element:String
        @param index:The index at which the element lies in the page
        @type index:Integer
        """
  
        self.result = None
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Verify whether the element:%s is found in zone:%s at index:%d after clicking the Refresh Button"%(element,zone,index))
        try:
            for i in range(15):
                if(self.ExperitestClient.isElementFound(zone, element, index)):
                    time.sleep(1)
                    if self.WeMoAppLog != None:
                        self.WeMoAppLog.Info("The element:%s is found."%element)
                    self.result = True
                    break
                time.sleep(1) 
                if refresh==True:
                    self._clickOnRefreshButton()
                    assert self.result == True
            else:
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the element:%s could not be found."%element)
                raise Exception("Raising the Exception as the element:%s could not be found."%element)
        except: 
            self.result = False
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _verifyElementFoundbyClickingRefresh() encountered and Error")
                self.WeMoAppLog.LogException()
                 
    def _verifyElementNotFound(self,zone,element,index=0):
        """
        Verify whether the element is not found
        @param zone:The zone to search for an element
        @type zone:String
        @param element:The element to be searched for
        @type element:String
        @param index:The index at which the element lies in the page
        @type index:Integer
        """
        self.result = None
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Verify whether the element:%s is not found in zone:%s at index:%d"%(element,zone,index))
        try:
            for i in range(15):
                if not (self.ExperitestClient.isElementFound(zone, element,index)):
                    time.sleep(1)
                    if self.WeMoAppLog != None:
                        self.WeMoAppLog.Info("The element:%s is not found."%element)
                    self.result = True
                    break
                time.sleep(1)
            else:
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the element:%s is found."%element)
                raise Exception("Raising the Exception as the element:%s is found."%element)
        except: 
            self.result = False
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _verifyElementNotFound() encountered and Error")
                self.WeMoAppLog.LogException()

    def _verifyElementFound(self,zone,element,index=0):
        """
        Verify whether the element is found
        @param zone:The zone to search for an element
        @type zone:String
        @param element:The element to be searched for
        @type element:String
        @param index:The index at which the element lies in the page
        @type index:Integer
        """
        self.result = None
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Verify whether the element:%s is found in zone:%s at index:%d"%(element,zone,index))
        try:
            for i in range(15):
                try:
                    if(self.ExperitestClient.isElementFound(zone, element,index)):                        
                        if self.WeMoAppLog != None:
                            self.WeMoAppLog.Info("The element:%s is found."%element)
                        self.result = True
                        return True
                        break    
                    else:
                        self.result = False
                        return False 
                        break 
                except:
                    time.sleep(60)
                self.result = True     
            else:                
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the element:%s could not be found."%element)
                raise Exception("Raising the Exception as the element:%s could not be found."%element)
        except: 
            self.result = False
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _verifyElementFound() encountered and Error")
                self.WeMoAppLog.LogException()

    def _verifyElementFoundInContainer(self,zone,element,index=0):
        """
        Verify whether the element is found
        @param zone:The zone to search for an element
        @type zone:String
        @param element:The element to be searched for
        @type element:String
        @param index:The index at which the element lies in the page
        @type index:Integer
        """
        self.result = None
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Verify whether the element:%s is found in zone:%s at index:%d"%(element,zone,index))
        try:
            for i in range(15):
                try:
                    self.ExperitestClient.verifyElementFound(zone, element,index)                        
                    if self.WeMoAppLog != None:
                        self.WeMoAppLog.Info("The element:%s is found."%element)
                    self.result = True
                    #return True
                    break    

                except:
                    time.sleep(60)
                self.result = True     
            else:                
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the element:%s could not be found."%element)
                raise Exception("Raising the Exception as the element:%s could not be found."%element)
        except: 
            self.result = False
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _verifyElementFound() encountered and Error")
                self.WeMoAppLog.LogException()
                
                
                
                

    def _verifyTheElementFoundIn (self,zone, searchElement, index, direction, elementFindZone, elementToFind, width=0, height=0):
        """
        Verify the Element is Found Inside the Main element which is being searched
        @param zone:The zone to search for an element
        @type zone:String
        @param searchElement:The searchElement is the element to be search.
        @type searchElement:String
        @param index:The index is value of the position 
        @type index:int
        @param direction: The direction of the search 
        @type element:String
        """    
        self.result = None
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Verify the Element is Found Inside the Main element which is being searched")
        try:
            for i in range(10):
                try:
                    if (self.ExperitestClient.isFoundIn(zone,searchElement, index, direction, elementFindZone, elementToFind, width, height)):
                        if self.WeMoAppLog != None:
                            self.WeMoAppLog.Info("The element :%s is found in %s  "%(elementToFind,searchElement))
                        self.result = True                        
                        return True  
                        break
                    else:
                        return False
                        break
                except:
                    time.sleep(60)

            else:                 
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the element:%s is found."%element)
                raise Exception("Raising the Exception as the element:%s is found."%element)
        except: 
            self.result = False
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _verifyTheElementFoundIn() encountered and Error")
                self.WeMoAppLog.LogException()            
        
                   
    def _clickOnAnElement(self,zone,element,index=0,clickCount=1):
        """
        Click on an element
        @param zone:The zone to search for an element
        @type zone:String
        @param element:The element to be searched for
        @type element:String
        @param index:The index at which the element lies in the page
        @type index:Integer
        @param clickCount:The number of clicks to be performed on an element
        @type index:Integer
        """
        self.result = None
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Click on the element:%s"%element)
        try:
            for i in range(10):
                if (self.ExperitestClient.isElementFound(zone, element,index)):
                    time.sleep(1)
                    if self.WeMoAppLog != None:
                        self.WeMoAppLog.Info("The element:%s is not found."%element)
                    try:    
                        self.ExperitestClient.click(zone, element, index, clickCount)
                        time.sleep(1)
                        self.result = True
                        return True
                        break
                    except:
                        time.sleep(60)
                self.result = True        
            else:
                return False 
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the element:%s is found."%element)
                raise Exception("Raising the Exception as the element:%s is found."%element)
        except: 
            self.result = False
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _clickOnAnElement() encountered and Error")
                self.WeMoAppLog.LogException()
                
                
                
    def _clickInsideAnElement(self, zone, searchElement, index, direction, clickElementZone, clickElement, width=0, height=0):
        """
        Click on an element
        @param zone:The zone to search for an element
        @type zone:String
        @param searchElement:The element to be searched for
        @type element:String
        @param index:The index at which the element lies in the page
        @type index:Integer
        @param direction:The direction in which the Click has to performed 
        @type index:string
        @param clickElementZone:The clickElementZone is the Zone of the Click element
        @type index:String
        """
        self.result = None
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Click inside the element:%s"%searchElement)
        try:
            for i in range(10):
                if (self.ExperitestClient.isElementFound(zone, searchElement,index)):
                    time.sleep(1)
                    if self.WeMoAppLog != None:
                        self.WeMoAppLog.Info("The element:%s is not found."%searchElement)
                    try:    
                        self.ExperitestClient.clickIn2(zone, searchElement, index, direction, clickElementZone, clickElement)
                        time.sleep(1)
                        return True
                        break
                    except:
                        time.sleep(60)
            else:
                return False 
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the element:%s is found."%searchElement)
                raise Exception("Raising the Exception as the element:%s is found."%searchElement)
        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _clickInsideAnElement() encountered and Error")
                self.WeMoAppLog.LogException()                
       
       
    def _clickInsideAnElement2_5(self, zone, searchElement, index, direction, clickElementZone, clickElement, width=0, height=0, clickCount=1):
        """
        Click on an element
        @param zone:The zone to search for an element
        @type zone:String
        @param searchElement:The element to be searched for
        @type element:String
        @param index:The index at which the element lies in the page
        @type index:Integer
        @param direction:The direction in which the Click has to performed 
        @type index:string
        @param clickElementZone:The clickElementZone is the Zone of the Click element
        @type index:String
        """
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Click inside the element:%s"%searchElement)
        try:
            for i in range(10):
                if (self.ExperitestClient.isElementFound(zone, searchElement,index)):
                    time.sleep(1)
                    if self.WeMoAppLog != None:
                        self.WeMoAppLog.Info("The element:%s is not found."%searchElement)
                    try:    
                        self.ExperitestClient.clickIn2_5(zone, searchElement, index, direction, clickElementZone, clickElement,width, height, clickCount)
                        time.sleep(1)
                        return True
                        break
                    except:
                        time.sleep(60)
            else:
                return False 
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the element:%s is found."%searchElement)
                raise Exception("Raising the Exception as the element:%s is found."%searchElement)
        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _clickInsideAnElement2_5() encountered and Error")
                self.WeMoAppLog.LogException()                
       


    def _clickInsideAnElement3(self, zone, searchElement, index, direction, clickElementZone, clickElement, clickElementIndex=0, width=0, height=0, clickCount=1):
        """
        Click on an element
        @param zone:The zone to search for an element
        @type zone:String
        @param searchElement:The element to be searched for
        @type element:String
        @param index:The index at which the element lies in the page
        @type index:Integer
        @param direction:The direction in which the Click has to performed 
        @type index:string
        @param clickElementZone:The clickElementZone is the Zone of the Click element
        @type index:String
        """
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Click inside the element:%s"%searchElement)
        try:
            for i in range(10):
                if (self.ExperitestClient.isElementFound(zone, searchElement,index)):
                    time.sleep(1)
                    if self.WeMoAppLog != None:
                        self.WeMoAppLog.Info("The element:%s is not found."%searchElement)
                    try:    
                        self.ExperitestClient.clickIn3(zone, searchElement, index, direction, clickElementZone, clickElement, clickElementIndex, width, height, clickCount)
                        time.sleep(1)
                        return True
                        break
                    except:
                        time.sleep(60)
            else:
                return False 
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the element:%s is found."%searchElement)
                raise Exception("Raising the Exception as the element:%s is found."%searchElement)
        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _clickInsideAnElement3() encountered and Error")
                self.WeMoAppLog.LogException()

       
       
    def _swipeToCheckForElement(self, direction, offset, swipeTime, zone, elementtofind, elementtofindindex=0, delay=1000, rounds=5, click=True):
        """
        Swipe to check for an element
        @param zone:The zone to search for an element
        @type zone:String
        @param element:The element to be searched for
        @type element:String
        @param direction:The direction in which the element is to be searched for
        @type direction:String
        """
        
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Swipe to check for the element:%s"%elementtofind)
        try:
            for i in range(5):
                try:
                    if(self.ExperitestClient.swipeWhileNotFound2(direction, offset, swipeTime, zone, elementtofind, elementtofindindex, delay, rounds, click)):
                        time.sleep(1)
                        return True 
                        break
                    else:
                        return False 
                        break
                except: 
                    time.sleep(60) 
            else:
                return False 
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the Swipe function was unsuccessful in swipeing the element :%s is found."%elementtofind)
                raise Exception("Raising the Exception as the Swipe function was unsuccessful in swipeing the element :%s is found."%elementtofind)                                 
        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _swipeToCheckForElement() encountered and Error")
                self.WeMoAppLog.LogException()
                 

     
    def _getTheTextInsideTheElement(self, zone, element, index, textZone, direction, width=0, height=0):
        """
        Gets the text inside the Element being passed
        @@Param Element : Is a string inside which the text has to extracted
        @@type          : String                  
        """
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info ("Gets the text inside the Element being passed") 
        
        try:
            for i in range(5):
                try:
                    TEXT_VALUE = self.ExperitestClient.getTextIn2(zone, element, index, textZone, direction, width, height)
                    if TEXT_VALUE != None:
                        return TEXT_VALUE                        
                        break                         
                except:
                    time.sleep(60) 
            else:
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the Gettext Command could not get the text from the Element %s"%element)
                raise Exception("Raising the Exception as the Gettext Command could not get the text from the Element %s"%element)         

        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _getTheTextInsideTheElement() encountered and Error")
                self.WeMoAppLog.LogException()                
                 
    def _sendText(self,text):
        """
        Send text to the text box
        @param text:The text to be sent
        @type text:String
        """
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Sending the text:%s"%text)
        try:
            time.sleep(1)
            self.ExperitestClient.sendText(text)
            time.sleep(1)
        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _sendText() encountered and Error")
                self.WeMoAppLog.LogException()
                
                
    def _sendTheTextIntoTextBox(self, zone, element, index, text):
        """
        This function will Send the Text to the Element specified 
        """
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("This function will Send the Text to the Element specified ") 
           
        try:
            for i in range(5):
                try:
                    self.ExperitestClient.elementSendText(zone, element, index, text) 
                    return True 
                    break
                except:
                    time.sleep(60) 
            else:
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the elementSendText Command could not send the text inside the Element %s"%element)
                raise Exception("Raising the Exception as the elementSendText Command could not send the text inside the Element %s"%element)   

        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _sendTheTextIntoTextBox() encountered and Error")
                self.WeMoAppLog.LogException()  
               
            
    def _getText(self,zone):
        """
        Get the text of the Zone
        @param zone:The text in the zone
        @type zone:String
        """
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("Getting the Text on the Page for zone:%s"%zone)
        try:
            for i in range(5):
                try:
                    text = self.ExperitestClient.getText(zone)
                    time.sleep(1)
                    return text
                except:
                    time.sleep(60) 
            else:
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the getText Command could not get the text ")
                raise Exception("Raising the Exception as the getText Command could not get the text ")
        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _getText() encountered and Error")
                self.WeMoAppLog.LogException()
                
    def _getTheTextFromTextBox(self,  zone, element, index=0):
        """
        This function will Get the Text inside the  Element specified 
        """
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("This function will Get the Text inside the  Element specified") 
           
        try:
            for i in range(5):
                try:
                    GET_TEXT_VALUE =self.ExperitestClient.elementGetText(zone, element, index) 
                    return GET_TEXT_VALUE 
                    break
                except:
                    time.sleep(60) 
            else:
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the elementGetText Command could get the text inside the Element %s"%element)
                raise Exception("Raising the Exception as the elementGetText Command could get the text inside the Element %s"%element)   

        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _getTheTextFromTextBox() encountered and Error")
                self.WeMoAppLog.LogException()             
    


    def _swipeTheElementToSpecifiedOffset(self,zone, element, index, direction, offset=0, time=2000):
        """
        This function will Swipe the element to the specified offset
        """
        if self.WeMoAppLog != None:
            self.WeMoAppLog.Info("This function will Swipe the element to the specified offset") 
           
        try:
            for i in range(5):
                try:
                    self.ExperitestClient.elementSwipe(zone, element, index, direction, offset, time)  
                    return True 
                    break
                except:
                    time.sleep(60) 
            else:
                if self.WeMoAppLog != None:
                    self.WeMoAppLog.Error("Raising the Exception as the elementSwipe Command could not swipe to the required offset")
                raise Exception("Raising the Exception as the elementSwipe Command could not swipe to the required offset")   

        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _swipeTheElementToSpecifiedOffset() encountered and Error")
                self.WeMoAppLog.LogException()  

    
    def _getAllValues(self,zone, element, property):
        """
        Gets All the Values for the Element specified 
        """
        
        try:
            for i in range(10):
                try:
                    GET_VALUES= self.ExperitestClient.getAllValues(zone, element, property)
                    return GET_VALUES
                    break
                except:
                    time.sleep(60) 
            else:
                if self.WeMoAppLog != None :
                    self.WeMoAppLog.Info("Raising an Exception as Get All values function failed to get all the values ") 
                raise Exception("Raising an Exception as Get All values function failed to get all the values ")             
        
        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _getAllValues() encountered and Error")
                self.WeMoAppLog.LogException()
        
    def _elementGetProperty(self,zone, element, index, property):
        """
        Gets All the Values for the Element specified 
        """
        
        try:
            for i in range(10):
                try:
                    ELEMENT_VALUE= self.ExperitestClient.elementGetProperty(zone, element, index, property)
                    return ELEMENT_VALUE
                    break
                except:
                    time.sleep(60) 
            else:
                if self.WeMoAppLog != None :
                    self.WeMoAppLog.Info("Raising an Exception as Element property failed to get all the values of the  element ") 
                raise Exception("Raising an Exception as Element property failed to get all the values of the  element ")             
        
        except: 
            if self.WeMoAppLog != None:
                self.WeMoAppLog.Error("The method _elementGetProperty() encountered and Error")
                self.WeMoAppLog.LogException()
        
    
    
    
if __name__ == "__main__":
  pass 
  #a = AndroidWeMoApp_Expericlient("localhost","8888",8888,"adb:S3")
  #a.ExperitestClient.isElementFound("WEB","xpath=//*[@text='Setting Up your Switch or Sensor']",0)
  #a._clickOnAnElement("WEB","css=DIV.owl-page",2,1) 

 