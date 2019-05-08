import time, os 
import sys, traceback
import smtplib
import email
from email.mime.text import MIMEText


""" find out the parent directory of the "lib" folder .. which is 'automation'"""       
sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("EmailUtility.py")), os.pardir)), "header"))


from EmailUtilityConsts import *

from Trace import *

def getEmailAddresses(self):
    self.To = ""
    self.MailingList = {}
    #read the "TO" email addresses from the file "EmailListFile" in the config folder
    if not os.path.exists(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("EmailUtility.py")), os.pardir)), "config", self.EmailListFile)):
        self.trace.Critical("No EmailList file:", self.EmailListFile)
        return False
    fp = open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("EmailUtility.py")), os.pardir)), "config", self.EmailListFile), "r")
    lines = fp.readlines()
    fp.close()
    
    if len(lines) == 0:
        return False
    for line in lines:
        if line.find("#") == 0:
            continue
        if line.find(":") > -1:
            mailingGroupName = line.split(":")[0].strip()
            mailingGroupName = mailingGroupName.split(",")
            mailingAddresses = line.split(":")[1].strip()
            if mailingAddresses.find(",") > -1:
                #More than one email id is given for this mailing group .. handle this
                mailingAddresses = mailingAddresses.replace(" ", "")
                mailingAddresses = mailingAddresses.replace(",", ", ")
            for groupName in mailingGroupName:
                if groupName in self.MailingList:
                    self.MailingList[groupName] += ", " + mailingAddresses
                else:
                    self.MailingList[groupName] = mailingAddresses
            continue
        else:
            if self.To == "":
                self.To = self.To + line.strip()
            else:
                self.To = self.To + ", " + line.strip()
    return True


class EmailUtility():

    # ====================================================
    def __init__(self, **arguments):
        self.trace = Trace("EmailUtility.py")
        self.From = ""
        self.To = ""
        self.MailingList = {}
        
        self.From = "automation@belkin.com"

        if 'EmailListFile' in arguments:
            ''' This EmailListFile must exist in the 'config' folder '''
            self.EmailListFile = arguments['EmailListFile']
            #read the EmailListFile and populate other fields: To and MailingList
            getEmailAddresses(self)
            
        else:
            #If no EmailListFile is given, then process the constructor parameters for 'To' and 'MailingList'
            if 'To' in arguments:
                self.To = arguments['To']
                self.To = self.To.replace(" ", "")
                self.To = self.To.replace(",", ", ")
            if 'Administrators' in arguments:
                self.MailingList['administrator'] = arguments['Administrators']
                self.MailingList['administrator'] = self.MailingList['administrator'].replace(" ", "")
                self.MailingList['administrator'] = self.MailingList['administrator'].replace(",", ", ")

    '''
    def sendEmail(self, subject, emailBody, groupName = None, attachment = None):

        if groupName == None and (self.To == "" and self.MailingList == {}):
            #There are no recipients for the email .. so return
            return

        if groupName != None and self.MailingList == {}:
            #There are no recipients for the email .. so return
            return
        
        msg = email.MIMEMultipart.MIMEMultipart()
        msg["From"] = self.From
        if 'administrator' in self.MailingList:
            toAddress = self.MailingList['administrator']
        else:
            toAddress = ""
        
        if groupName != None:
            if groupName != "administrator":
                if groupName in self.MailingList and self.MailingList[groupName] != "":
                    if toAddress != "":
                        toAddress += ", " + self.MailingList[groupName]
                    else:
                        toAddress = self.MailingList[groupName]
        else:
            if self.To != "":
                if toAddress != "":
                    toAddress += ", " + self.To
                else:
                    toAddress = self.To
                
        msg["To"] = toAddress
        msg["Subject"] = subject
        msg["Date"]    = email.Utils.formatdate(localtime=True)

        #fill body with the summary
        part1 = MIMEText(emailBody + "\n\n\nThanks\nAutomation Team @ Belkin", 'plain')
        msg.attach(part1)

        if attachment != None and attachment != "":
            # attach a file
            part2 = email.MIMEBase.MIMEBase('application', "octet-stream")
            part2.set_payload( open(attachment,"rb").read() )
            email.Encoders.encode_base64(part2)
            part2.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
            msg.attach(part2)

        try:
            server = smtplib.SMTP(EMAILHOST)
        except:
            self.trace.Critical(sys.exc_info()[0])
            self.trace.Critical(sys.exc_info()[1])
            self.trace.Critical(traceback.extract_tb(sys.exc_info()[2]))
            raise Exception("Unable to connect to EmailHost: ", EMAILHOST)
        try:
            print msg
            failed = server.sendmail(self.From, msg["To"].split(", "), msg.as_string())
            server.close()
        except Exception, e:
            raise Exception("Unable to send email. Error: %s"%str(e))

        self.trace.Debug("email sent successfully")
    '''



    def sendEmail(self, subject, emailBody, groupName = None, attachment = None):

        if groupName == None and (self.To == "" and self.MailingList == {}):
            #There are no recipients for the email .. so return
            return

        if groupName != None and self.MailingList == {}:
            #There are no recipients for the email .. so return
            return
        
        msg = email.MIMEMultipart.MIMEMultipart()
        msg["From"] = self.From
        if 'administrator' in self.MailingList:
            toAddress = self.MailingList['administrator']
        else:
            toAddress = ""
        
        if groupName != None:
            if groupName != "administrator":
                if groupName in self.MailingList and self.MailingList[groupName] != "":
                    if toAddress != "":
                        toAddress += ", " + self.MailingList[groupName]
                    else:
                        toAddress = self.MailingList[groupName]
        else:
            if self.To != "":
                if toAddress != "":
                    toAddress += ", " + self.To
                else:
                    toAddress = self.To
                
        msg["To"] = toAddress
        msg["Subject"] = subject
        msg["Date"]    = email.Utils.formatdate(localtime=True)

        #fill body with the summary
        part1 = MIMEText(emailBody + "\n\n\nThanks\nAutomation Team @ Belkin", 'plain')
        msg.attach(part1)

        if attachment != None and attachment != "":
            # attach a file
            part2 = email.MIMEBase.MIMEBase('application', "octet-stream")
            part2.set_payload( open(attachment,"rb").read() )
            email.Encoders.encode_base64(part2)
            part2.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
            msg.attach(part2)

        try:
            #server = smtplib.SMTP(EMAILHOST)

            server = smtplib.SMTP()
            server.connect(SMTPEMAILHOST,SMTPEMAILPORT)
            server.ehlo()
            server.starttls()
            server.login(SMTPUSERNAME,SMTPPASSWORD)
        except:
            self.trace.Critical(sys.exc_info()[0])
            self.trace.Critical(sys.exc_info()[1])
            self.trace.Critical(traceback.extract_tb(sys.exc_info()[2]))
            raise Exception("Unable to connect to EmailHost: ", SMTPEMAILHOST)
        try:
            print msg
            failed = server.sendmail(self.From, msg["To"].split(", "), msg.as_string())
            server.close()
        except Exception, e:
            raise Exception("Unable to send email. Error: %s"%str(e))

        self.trace.Debug("email sent successfully")

if __name__ == "__main__":
    emailUtil = EmailUtility(From = "tewemoqa@tataelxsi.co.in",EmailListFile = "WeMoAppAutomation.EmailList")
    emailUtil.sendEmail("Hello Test Email","Checking in what's going on","administrator")