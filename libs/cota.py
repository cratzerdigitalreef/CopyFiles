# -*- coding: UTF-8 -*-
import os
import sys
import colorama
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
  
sys.path.append(parent_directory)
sys.path.append(f"{parent_directory}/libs")

from str import *
from bytes import *
from smartcard.util import toBytes
from log import *
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.Exceptions import CardRequestTimeoutException
import smartcard.util
from smartcard.util import toBytes, toASCIIBytes, toASCIIString
from colorama import Back, Fore, Style
from simcard import *


#------------------------------------------------------------------------------------
# COTA Commands dictionaries
#------------------------------------------------------------------------------------

# Commands Dictionary

cmd_dic = {"F0" : "Display Text", 
           "F1" : "Change Text of DisplayText",
           "F2" : "Change URL Of DisplayText",
           "F4" : "Launch URL without DisplayText",
           "F5" : "DisplayText Without URL",
           "F6" : "Generic SIM Tookit",
           "F7" : "Get SMS buffer",
           "F8" : "Request IMEI",
           "F9" : "Init Timer for DisplayText",
           "FA" : "Save data (MSISDN) for APK",
           "FB" : "Request COTA Version and IMEI",
           "FC" : "Manage Counters for APK Notification",
           "FD" : "Manage SHA-1",
           "FE" : "Manage LOCI to Notify for Server",
           "E0" : "Manage LOCI for APK",
           "E1" : "Manage TPDA Validation",
           "E2" : "Manage SDK ID",
           "D1" : "Manage SDK ID (D1)",
           "D2" : "Manage Play Tone (D2)",
           "D3" : "Manage Duration (D3)",
           "D4" : "Get ICCID and IMSI (D4)",
           "D5" : "Switch off applet (D5)",
           "D6" : "Call SMPP push from SDK (D6)",
           "D8" : "Change DEFAULT Text of DisplayText",
           "D9" : "Change DEFAULT URL Of DisplayText",
           "DC" : "Get Date Time from SDKs/APKs"
           }

# --------------------------------------------------------------------------------
# MSISDN - FIRST 2 DIGITS FOR COUNTRIES
countries_dic_block = 4
#Each block consists on:
# - international Telecom Phone number
# - Country
# - UTC (GMT time)
# - Country extension
countries_dic = [
    "52",     "Mexico",                 "-6", "MX"
    ,"54",    "Argentina",              "-3", "AR"
    ,"55",    "Brasil",                 "-3", "BR"
    ,"56",    "Chile",                  "-4", "CL"
    ,"57",    "Colombia",               "-5", "CO"
    ,"506",   "Costa Rica",             "-6", "CR"
    ,"593",   "Ecuador",                "-5", "EC"
    ,"503",   "El Salvador",            "-6", "SV"
    ,"502",   "Guatemala",              "-6", "GT"
    ,"504",   "Honduras",               "-6", "HN"
    ,"505",   "Nicaragua",              "-6", "NI"
    ,"507",   "Panama",                 "-5", "PA"
    ,"595",   "Paraguay",               "-3", "PY"
    ,"51",    "Peru",                   "-5", "PE"
    ,"1829",  "Republica Dominicana",   "-4", "DO"
    ,"1",     "Puerto Rico",            "-4", "PR"
    ,"598",   "Uruguay",                "-3", "UY"
    ,"60104", "AMX DRONE",              "0",  "NN"
]
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# COTA - SAP POPUP VALUES
sCOTA_COTA = sSimcard_sDefTAR_COTA_Name
sCOTA_AUTH = sSimcard_sDefTAR_SAPAUTH_Name 
sCOTA_SARM = sSimcard_sDefTAR_SAPROAM_Name
sCOTA_PopUpOK = "31"
sCOTA_PopUpNOK = "30"
sCOTA_PopUpOK_des = "OK"
sCOTA_PopUpCANCEL = sCOTA_PopUpNOK + "10"
sCOTA_PopUpCANCEL_des = "CANCEL"      
sCOTA_PopUpBACK = sCOTA_PopUpNOK + "11"
sCOTA_PopUpBACK_des = "BACK"      
sCOTA_PopUpNOACTION = sCOTA_PopUpNOK + "12"
sCOTA_PopUpNOACTION_des = "NO ACTION" 
sCOTA_PopUpNOTSupported = sCOTA_PopUpNOK + sCOTA_PopUpNOK
sCOTA_PopUpNOTSupported_des = "NOT SUPPORTED"  

sCOTA_LaunchBrowser_des = "LAUNCH BROWSER"
sCOTA_LaunchBrowserSupported = sCOTA_PopUpOK
sCOTA_LaunchBrowserSupported_des = "SUPPORTED"
sCOTA_LaunchBrowserSupportedNOT = sCOTA_PopUpNOK
sCOTA_LaunchBrowserSupportedNOT_des = "NOT SUPPORTED"
# --------------------------------------------------------------------------------

    
#------------------------------------------------------------------------------------
# COTACmd => process data according what it is needed
#------------------------------------------------------------------------------------
def COTACmd(sLogFile, sCMD, sDataType, sDatat):

    sCMDF1 = "F1"
    sCMDF5 = "F5"

    sCMD = str_SpacesOut(sCMD)
    sCMD = sCMD.upper()

    sDataType = str_SpacesOut(sDataType)
    sDataType = sDataType.upper()
    
    bReturn = True
    
    sDataStruct = COTACmdProcessDataOnly(sLogFile, sCMD, sDataType, sDatat)
    sData = sDataStruct[0]
    sCMD = sDataStruct[1]
    bASCII = sDataStruct[2]
    
    if str_left(sCMD, 2) == sCMDF1 or str_left(sCMD, 2) == sCMDF5:   
       if bASCII:
          sCMD = sCMD + "04"
       else:
          # UCS2
          sCMD = sCMD + "08"

    sData = str_SpacesOut(sData)
    sData = sData.upper()   
    
    # ADD BYTECODE LENGTH
    nLenData = len(sData)//2
    if nLenData > 127:
       sCMD = sCMD + "81" 
    #print("nLenData: " + str(nLenData) + " - 0x: " + bytes_NroToHexa(nLenData))
    sCMD = sCMD + bytes_NroToHexa(nLenData)
    
    # ADD DATA
    sCMD = sCMD + sData
    sCMD = str_TrimCleanSpaces(sCMD)
    sPrint = "COTACmd. CMD result: " + sCMD

    #LOG DATA
    file2write=open(sLogFile,'a')
    file2write.write(sPrint + "\n")
    file2write.close()
    
    return sCMD

#------------------------------------------------------------------------------------
# COTACmdProcessDataOnly => process data only according what it is needed to bytecode
#------------------------------------------------------------------------------------
def COTACmdProcessDataOnly(sLogFile, sCMD, sDataType, sDatat):

    sCMDF1 = "F1"
    sCMDF2 = "F2"
    sCMDF4 = "F4"
    sCMDF5 = "F5"
    sCMDF0 = "F0"
    sCMDNONE = "NONE"
    sURLDataBegin = "http"
        
    sCMD = str_SpacesOut(sCMD)
    sCMD = sCMD.upper()

    sDataType = str_SpacesOut(sDataType)
    sDataType = sDataType.upper()
    
    bReturn = True
    
    sPrint = "sCMD: " + sCMD
    sPrint = sPrint + "\n" + "sDataType: " + sDataType
    sPrint = sPrint + "\n" + "sData: " + sDatat

    #LOG DATA
    #file2write=open(sLogFile,'a')
    #file2write.write(sPrint + "\n")
    #file2write.close()

    #CHECK DATA WHETHER IT IS AN URL OR DATA
    if sCMD == sCMDNONE:
       sPrint = "As there is no command predefined (" + sCMDNONE + "), and data is for "
       print(str_left(sDatat.lower(), len(sURLDataBegin)))
       print(sURLDataBegin)
       if str_left(sDatat.lower(), len(sURLDataBegin)) == sURLDataBegin:
          # IT IS AN URL
          sCMD = sCMDF2 + sCMDF0
          sPrint = sPrint + "URL"
       else:
          sCMD = sCMDF1 + sCMDF0
          sPrint = sPrint + "PopUp Text"
      #LOG DATA
       sPrint = sPrint + ", assume command to process is " + sCMD + "."
       file2write=open(sLogFile,'a')
       file2write.write(sPrint + "\n")
       file2write.close()
          
           
    # VERIFY URL WHETHER IT IS OK 
    if str_left(sCMD, 2) == sCMDF2 or str_left(sCMD, 2) == sCMDF4:
       sDatat = COTAURLSpecialChars(sDatat)      
       #LOG DATA
       file2write=open(sLogFile,'a')
       file2write.write("URL after processing: " + sDatat + "\n")
       file2write.close()
    
    sData = sDatat
    bASCII = False
    if sDataType=="ASCII":
       bASCII = True
       if bytes_IsHexaValid(sDatat)==False:
          #print("sDataT: " + sDatat) 
          sData = bytes_StrToHexa(sDatat)
          sDataTASCII = sDatat
       else:
          sDataTASCII = bytes_HexaToASCII(str_SpacesOut(sDatat))          
          #print("sDataTASCII: " + sDataTASCII)
    else: 
       if bytes_IsHexaValid(sDatat)==False:
          #print("sDatat: " + sDatat)
          # CHECK WHETHER IT IS ASCII OR UCS2
          if bytes_isASCIIText(sDatat):
             bASCII = True
             sData = bytes_StrToHexa(sDatat)
             #sDataTASCII = sDatat
          else:
             # DATA IS UCS2 BECAUSE IT IS NOT POSSIBLE TO TRANSLATE TO ASCII   
             sData = to_ucs2(sDatat)
       
    #print("bASCII: " + str(bASCII) + " - Data: " + sDatat + " - Translation: " + sData)
    
    return sData,sCMD,bASCII

#------------------------------------------------------------------------------------
# COTAURLSpecialChars => process and remove special characters in URL for COTA
#------------------------------------------------------------------------------------
def COTAURLSpecialChars(sURL):
    return simcard_URLSpecialChars(sURL)
		
#------------------------------------------------------------------------------------
# COTAManageEmojis => process UCS2 bytecode removing emojis with 0x
#------------------------------------------------------------------------------------
def COTAManageEmojis(sOriginal, sBytecode):
    
    s0X = "0x"
    #0x27 0B
    nEmojiCodeLen = 5

    #print("Original: " + sOriginal)
    #print("Bytecode: " + sBytecode)
    str_TrimCleanSpaces(sBytecode.upper())
    sReturn = sBytecode

    n0X = str_CountPattern(sOriginal, s0X)
    if n0X > 0:
       #THERE ARE EMOJIS
       n = 0
       while n < n0X:
             sBefore = str_getSubStringFromOcur(sOriginal, s0X, n)
             sAfter = str_getSubStringFromOcur(sOriginal, s0X, n+1)
             #print("Before: " + sBefore)
             #print("After: " + sAfter)
             if len(sAfter) >= nEmojiCodeLen:
                #0x27 0B
                sEmoji = str_left(sAfter, nEmojiCodeLen)
                sEmojiNew = str_TrimCleanSpaces(sEmoji)
                
                #print("sEmoji: " + sEmoji)
                #print("sEmoji New: " + sEmojiNew)
                
                sUCS2Emoji = to_ucs2(s0X + sEmoji)
                #print("sEmoji UCS2: " + sUCS2Emoji)
                
                #print("Before Replace Return: " + sReturn)
                #print("Before Replace sUCS2Emoji: " + sUCS2Emoji)
                #print("Before Replace sEmojiNew: " + sEmojiNew)
                sReturn = str_ReplaceWord(sReturn, sUCS2Emoji, sEmojiNew)
                #print("Return: " + sReturn)
                
             n = n + 1

    #print("sReturn: " + sReturn)
    
    return sReturn
	  
	   
#------------------------------------------------------------------------------------
# COTAGetCampaignIDFromCmd => Get Campaign ID from command
#------------------------------------------------------------------------------------
def COTAGetCampaignIDFromCmd(cmd):
    # Maximum ID = 7F FF => 32767
    # Check if cmd is pair
    cmd = str_SpacesOut(cmd).upper()
    
    length = len(cmd)
    if len(cmd) % 2 != 0:
       return False, "This command is not valid, check it and try again: " + cmd
       
    IDdecimal = int(cmd[0:4],16)
    maxBytesID = 32767

    if IDdecimal <= maxBytesID and not cmd_dic.get(cmd[0:2]):
        if len(cmd) < 6:
            #return None, cmd
            return "", cmd
        return cmd[0:4],cmd[4:]
    else:
        return False, cmd
	   
#------------------------------------------------------------------------------------
# COTAgetCampaignID => Get Campaign ID
#------------------------------------------------------------------------------------
def COTAgetCampaignID(sLogFile,cmd):

    cmd = str_SpacesOut(cmd).upper()
    bResponse, sResponse = COTAGetCampaignIDFromCmd(cmd)

    if str(bResponse) == "False" and sResponse != cmd:    
       log_write_ErrorInRed(sLogFile, sResponse)

    #print("COTAgetCampaignID - bResponse = " + str(bResponse) + " - cmd=" + str(cmd))
    return bResponse, sResponse
    
#------------------------------------------------------------------------------------
# COTAgetFeatSupported => Get whether it is supported or not a command taking into account the COTA version
#------------------------------------------------------------------------------------
def COTAgetFeatSupported(lFeatNotSupported, sCotaVer, dic_feat):
   for i in lFeatNotSupported:
      i=i.upper()
      dic_feat[i] = True
      #dic_feat.update({i:True})
   dic_feat.update({'COTAVERSION':sCotaVer}) 
   return dic_feat

#------------------------------------------------------------------------------------
# COTASelectApplet => Select Applet
#------------------------------------------------------------------------------------
# REQUEST IF COTA EXIST
def COTASelectApplet(sLogFileName, oCardService, sAID = 'A0 00 00 01 51 41 43 4C 00'): #00 A4 04 En realidad es el comando APDU, 09 son los bytes que mide el AID
   apdu = []
   bHeader = '00 A4 04 02'
   sAID = sAID.replace(" ","")
   bAIDLen = int(len(sAID)/2)
   bAIDLen = bytes_NroToHexa(bAIDLen)
   apdu = bHeader + bAIDLen + sAID

   sLog = 'Finding COTA applet by SELECT Command...'
   response = simcard_processAPDU(oCardService,apdu,sLogFileName)
   sw1 = response[-4:-2]
   sw2 = response[-2:]
   if sw1 == '90':
      sLog = 'COTA APPLET FOUND \nstatus words: ' + str(sw1) + ' ' + str(sw2)
      log_write (sLogFileName, sLog, 'success')
   else:
      sLog = 'The COTA Applet was not found \nError Code: ' +  str(sw1) + '' + str(sw2)
      log_write(sLogFileName, sLog, 'error')
   
   return sw1, sw2


#------------------------------------------------------------------------------------
#  COTA PROFILE
#  Return a dictionary with supported features according COTA Version
#  For include feature supported, write the feature in "listFeatSupported[]" list
#     1. The feature should be writed in the same way that "dic_feat{}" dictionary
#------------------------------------------------------------------------------------
def COTAProfile(sLogFileName,oCardservice, sTPDA = "", sCota_ver = ""):
   #sCota_ver = COTACmd_sendEnvelopeFB(oCardservice, sLogFileName, sTPDA, sVerbose = False)
   #Defining the dictionary to return
   dic_feat={}

   if sCota_ver != "":
      log_write_OKInGreen(sLogFileName, "Applet Version: " + sCota_ver)

   match sCota_ver:
      case 'COTA0205':
         listFeatSupported = ['F0', 'F1', 'MCCMNC', 'PopUpRetries', 'FA']
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA0206':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'MCCMNC', 
                              'F1F0', 'F2F0', 'UCS2', 'PopUpRetries',]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA0207':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC',
                              'MCCMNC', 'F1F0', 'F2F0', 'UCS2', 'PopUpRetries']
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA0208':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC',
                              'FD', 'FE', 'MCCMNC', 'F1F0', 'F2F0', 'UCS2', 'PopUpRetries']
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat

      case 'COTA0208R5':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC',
                                'FD', 'FE', 'MCCMNC', 'F1F0', 'F2F0', 'UCS2', 'PopUpRetries']
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA0209':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC',
                              'FD', 'FE', 'E0', 'E1', 'MCCMNC', 'F1F0', 'F2F0', 'UCS2',
                              'PopUpRetries', 'AutoPopUpbyIMEI']
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA0291':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC',
                              'FD', 'FE', 'E0', 'E1', 'E2', 'D1', 'MCCMNC', 'F1F0', 'F2F0',
                              'UCS2', 'PopUp_Retries', 'AutoPopUpbyIMEI']
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA0292':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD',
                              'F1F0', 'F2F0', 'UCS2', 'PopUpRetries',
                              'AutoPopUpbyIMEI']
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA0293':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD',
                              'F1F0', 'F2F0', 'UCS2', 'PopUpRetries', 'F0Priority']
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA0294':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD',
                              'F1F0', 'F2F0', 'UCS2', 'PopUpRetries',"AutoPopUpbyIMEI","CampaignID","F6"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      case 'COTA0295':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD',
                              'F1F0', 'F2F0', 'UCS2', 'PopUpRetries',"AutoPopUpbyIMEI","CampaignID","F6"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA0296R5':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD',
                              'F1F0', 'F2F0', 'UCS2', 'PopUpRetries',"AutoPopUpbyIMEI","CampaignID","F6"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat

      case 'COTA0297':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD',
                              'F1F0', 'F2F0', 'UCS2', 'PopUpRetries', "AutoPopUpbyIMEI", "CampaignID", "F6", "D6",
                              "D7"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
         
      case 'COTA0298':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD',
                              'F1F0', 'F2F0', 'UCS2', 'PopUpRetries',"AutoPopUpbyIMEI","CampaignID","F6","D6", "D7"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
         
      case 'COTA0299':
         listFeatSupported = ['F0', 'F1', 'F2', 'F4', 'F5', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD',
                              'F1F0', 'F2F0', 'UCS2', 'PopUpRetries',"AutoPopUpbyIMEI","CampaignID","F6","D4","D6", "D7", "D8", "D9", "DC"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
         
      case 'COTA020A':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E0", "E1",
                              "E2", "D1", "MCCMNC", "F1F0", "F2F0", "UCS2", "PopUpRetries", "MultiSHA1",
                              "AutoPopUpbyIMEI", "F0PRIORITY"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA020B':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E0", "E1",
                                 "E2", "D1", "MCCMNC", "F1F0", "F2F0", "UCS2", "PopUpRetries", "MultiSHA1", "F0Priority",
                                 "AutoPopUpbyIMEI", "F0PRIORITY"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA0300':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E0", "E1",
                                 "E2", "D1", "MCCMNC", "F1F0", "F2F0", "UCS2", "PopUpRetries", "MultiSHA1", "F0Priority",
                                 "AutoPopUpbyIMEI", "CampaignID"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      
      case 'COTA0301':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E0", "E1",
                                 "E2", "D1", "MCCMNC", "F1F0", "F2F0", "UCS2", "PopUpRetries", "MultiSHA1", "F0Priority",
                                 "AutoPopUpbyIMEI", "CampaignID", "F6"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat

      case 'COTA0302':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "E1",
                                 "E2", "D1", "F1F0", "F2F0", "UCS2", "PopUpRetries", "MultiSHA1", "F0Priority",
                                 "AutoPopUpbyIMEI", "CampaignID", "F6"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat

      case 'COTA0303':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E2",
                              "F1F0", "F2F0", "UCS2", "PopUpRetries", "AutoPopUpbyIMEI", "CampaignID", "F6", "MultiSHA1", "F0Priority",]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat            
            
      case 'COTA0400':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E2",
                              "F1F0", "F2F0", "UCS2", "PopUpRetries", "AutoPopUpbyIMEI", "CampaignID", "F6", "MultiSHA1", "F0Priority",]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat            
         
      case 'COTA0500':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E2",
                              "F1F0", "F2F0", "UCS2", "PopUpRetries", "AutoPopUpbyIMEI", "CampaignID", "F6", "MultiSHA1", "F0Priority", "FULL"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat            
         
      case 'COTA0501':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E2",
                              "F1F0", "F2F0", "UCS2", "PopUpRetries", "AutoPopUpbyIMEI", "CampaignID", "F6", "MultiSHA1", "F0Priority",
                              "D4","D5", "FULL"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat            
         
      case 'COTA0502':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E2",
                              "F1F0", "F2F0", "UCS2", "PopUpRetries", "AutoPopUpbyIMEI", "CampaignID", "F6", "MultiSHA1", "F0Priority",
                              "D4","D5", "FULL"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat            
         
      case 'COTA0504':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E2",
                              "F1F0", "F2F0", "UCS2", "PopUpRetries", "AutoPopUpbyIMEI", "CampaignID", "F6", "MultiSHA1", "F0Priority",
                              "D4","D5","D6", "D7", "FULL"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      case 'COTA0505':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E2",
                                "F1F0", "F2F0", "UCS2", "PopUpRetries", "AutoPopUpbyIMEI", "CampaignID", "F6",
                                "MultiSHA1", "F0Priority",
                                "D4", "D5", "D6", "D7", "FULL"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      case 'COTA0506':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E2",
                                "F1F0", "F2F0", "UCS2", "PopUpRetries", "AutoPopUpbyIMEI", "CampaignID", "F6",
                                "MultiSHA1", "F0Priority",
                                "D4", "D5", "D6", "D7", "FULL", "F7", "D8", "D9", "DC"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      case 'COTA0507':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E2",
                                "F1F0", "F2F0", "UCS2", "PopUpRetries", "AutoPopUpbyIMEI", "CampaignID", "F6",
                                "MultiSHA1", "F0Priority",
                                "D4", "D5", "D6", "D7", "FULL", "F7", "D8", "D9", "DC", "DE"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      case 'COTA0508':
         listFeatSupported = ["F0", "F1", "F2", "F4", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E2",
                                "F1F0", "F2F0", "UCS2", "PopUpRetries", "AutoPopUpbyIMEI", "CampaignID", "F6",
                                "MultiSHA1", "F0Priority",
                                "D4", "D5", "D6", "D7", "FULL", "F7", "D8", "D9", "DC", "DE"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      case 'SARM0100':
         listFeatSupported = ["F8", "FA", "FB", "FE", "CampaignID", "F6",
                                "MultiSHA1", 
                                "D4", "D5", "D6", "D7", "FULL", "F7", "DD", "DE"]
         COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)
         return dic_feat
      case _:
         if not sCota_ver:
            sLog = 'The Applet Version is empty!'
            log_write_ErrorInRed(sLogFileName, sLog)
            return False
         else:
            sLog = 'The version ' + sCota_ver + ' is not supported in the QA Framework.'
            log_write(sLogFileName, sLog, sType='warning')

            # IT IS ASSUMED THAT ALL VERSIONS ARE SUPPORTED
            listFeatSupported = ["F0", "F1", "F2", "F4", "F3", "F5", "F8", "F9", "FA", "FB", "FC", "FD", "FE", "E2",
                              "F1F0", "F2F0", "UCS2", "PopUpRetries", "AutoPopUpbyIMEI", "CampaignID", "F6", "MultiSHA1", "F0Priority",]
            COTAgetFeatSupported(listFeatSupported, sCota_ver, dic_feat)

            sLog = 'Supported: ' + str(listFeatSupported)
            log_write(sLogFileName, sLog, sType='warning')

            return dic_feat
            
#------------------------------------------------------------------------------------
# -
#------------------------------------------------------------------------------------
#COTAProfile()

#------------------------------------------------------------------------------------
# COTACmdAnalyzer
#------------------------------------------------------------------------------------
def COTAProactiveCMDProcess(sLog,sBERTLV_Value,sTexttoValidate=''):
   sCommndType = sBERTLV_Value[6:8]
   sProactiveCMD_DATA = ""
   sLog += '\n\tCOMMAND TYPE: ' + sCommndType + ' => '
   # DISPLAYTEXT
   if sCommndType == '21':
      sLog += 'DISPLAY TEXT\n'
      sPriority = sBERTLV_Value[8:10]
      sLog += '\tPRIORITY: '+sPriority
      if sPriority == '81':
         sLog += ' (High)\n'
      elif sPriority == '80':
         sLog += ' (Normal)\n'
      else: 
         sLog += ' (UNKNOWN)\n'
      # Validate if TAG 81 for inform text bigger than 127 bytes is present
      if sBERTLV_Value[20:22] == '81':
         sTextLen = sBERTLV_Value [22:24]
         nTextLenChars = int(sTextLen, base=16) * 2
         # -2 becuause DCS byte is included in textlength
         sText = sBERTLV_Value[26:26+(nTextLenChars-2)]
         sDCS = sBERTLV_Value[24:26]
      else:
         sTextLen = sBERTLV_Value [20:22]
         nTextLenChars = int(sTextLen, base=16) * 2
         # -2 becuause DCS byte is included in textlength
         sText = sBERTLV_Value[24:24+(nTextLenChars-2)]
         sDCS = sBERTLV_Value[22:24]


      # Decoding text
      sText = bytes_get_UTFByteDecode(sText)
      sText = sText[1]
      sProactiveCMD_DATA = sText

      sLog += '\tTEXT: ' + sText + '\n'
      if sDCS == '04':
         sLog += '\tDCS: ' + sDCS + ' (ASCII)'
      elif sDCS == '08':
         sLog += '\tDCS: ' + sDCS + ' (UCS2)'
      else:
         sLog += '\tDCS: ' + sDCS + ' (UNRECOGNIZED)'
      
      if sTexttoValidate:
         sLog +='\n\tTEXT IN INPUT PARAMETER: ' +  sTexttoValidate
         if sTexttoValidate == sText:
            sLog +=' (MATCH)'
         else:
            sLog +=' (NO MATCH!!!)'
            
       

   # LAUNCH BROWSER
   if sCommndType == '15':
      sLog += 'LAUNCH BROWSER\n'
      nURLLenChars = int(sBERTLV_Value[20:22], base=16) * 2
      sURL = sBERTLV_Value[22:22+nURLLenChars]
      sLog += '\tURL: ' + bytes_HexaToASCII(sURL)
      sProactiveCMD_DATA = bytes_HexaToASCII(sURL)

   # SEND SMS
   if sCommndType == '13': 
       sLog += 'SEND SHORT MESSAGE\n' # D0 16 81 03 01 13 00 82 02 81 83 0B 0B 05 00 05 81 06 01 F4 00 04 01 31 
       nTPDULengthChar = int(sBERTLV_Value [20:22], base=16) * 2 # 
       sBERTLV_Message_Detail = sBERTLV_Value [22:22 + nTPDULengthChar] # 05 00 05 81 06 01 F4 00 04 01 31 

       nTPDALenghtChar = int(sBERTLV_Message_Detail [4:6])
       if nTPDALenghtChar % 2 != 0:
          nTPDALenghtChar = nTPDALenghtChar + 1
       sTPDA = sBERTLV_Message_Detail [8:8+nTPDALenghtChar]
       sTPDA = str_reverse(sTPDA)
       sTPDA_Interpreted = ''
       for caracter in sTPDA:
          if caracter.isdigit():
             sTPDA_Interpreted += caracter
       sLog += '\tTPDA: ' + sTPDA_Interpreted + '\n'
       sMessageDetail = sBERTLV_Message_Detail [8 + nTPDALenghtChar + 1 :]
       nLengthMessageChar = int(sMessageDetail [3:5],base=16) * 2
       sMessageText = sMessageDetail[5:5+nLengthMessageChar]
       sProactiveCMD_DATA = sMessageText
       sMessageTextNoSpaces = sMessageText.replace(" ", "")

      # TODO: I don�t know how manage the campaign ID in a Message
      #  if len(sMessageTextNoSpaces) > 4 and len(sMessageTextNoSpaces) <= 8: # That Means that Campaign ID is present
      #    sCampaignID = sMessageTextNoSpaces[:4]
      #    sMessageText = sMessageTextNoSpaces[4:]                    
      #    sLog += '\tCampaign ID: ' + sCampaignID + '\n'

       sLog += '\tMessage: 0x' + str_SpaceHexa(sMessageText)
       if sMessageText == '31':
          sLog += ' => User Response: OK'
       elif sMessageText == '3010':
          sLog += ' => User Response: CANCEL'
       elif sMessageText == '3011':
          sLog += ' => User Response: BACKWARD'           
       elif sMessageText == '3012':
          sLog += ' => User Response: NO ACTION'       
       elif sMessageText == '3020':
          sLog += ' =>  ME currently unable to process command'
       elif sMessageText == '3030':
          sLog += ' =>  Command NOT supported'
       else:
          sMessageBytes = smartcard.util.toBytes(sMessageText[2:])
          sMessageDecode = smartcard.util.toASCIIString(sMessageBytes)
          sLog += f'\n\tInterpreted message: {sMessageDecode}' 
   return sLog, sProactiveCMD_DATA


# COTATerminalResponseProcess ---------------------------------------------------------------------------------------------------------------------------------------------------------
def COTATerminalResponseProcess (sLog, sBERTLV_Value):
   nTerminalResponseLenChars = int(sBERTLV_Value[5:7], base=16) * 2
   
   sLog += '\n\tTERMINAL RESPONSE\n\tCOMMAND TYPE: ' + str( sBERTLV_Value[12:14]) + ' => ' 
   
   #TERMINAL RESPONSE FOR LAUNCH BROWSER
   if sBERTLV_Value[12:14] == '15':
      sLog += 'LAUNCH BROWSER\n'
      sLog += '\tRESULT BYTE: ' + str(sBERTLV_Value[15:17]) + ' => '
      if str(sBERTLV_Value[14:16]) == '00':
         sLog += 'COMMAND PERFORMED SUCCESSFULLY'
      elif str(sBERTLV_Value[14:16]) == '01':
         sLog += 'COMMAND PERFORMED WITH PARTIAL COMPREHENSION'
      elif str(sBERTLV_Value[14:16]) == '01':
         sLog += 'COMMAND PERFORMED WITH MISSING INFORMATION'
      elif str(sBERTLV_Value[14:16]) == '01':
         sLog += 'COMMAND PERFORMED WITH PARTIAL COMPREHENSION'
      else:
         sLog += 'THE FRAMEWORK DOES NOT SUPPORT TERMINAL RESPONSE VALUE'


   if sBERTLV_Value[12:14] == '21':
      sLog += 'DISPLAY TEXT\n'
      sLog += '\tRESULT BYTE: ' + str(sBERTLV_Value[15:17]) + ' => '
      if str(sBERTLV_Value[14:16]) == '00':
         sLog += 'COMMAND PERFORMED SUCCESSFULLY'
      elif str(sBERTLV_Value[14:16]) == '01':
         sLog += 'COMMAND PERFORMED WITH PARTIAL COMPREHENSION'
      elif str(sBERTLV_Value[14:16]) == '01':
         sLog += 'COMMAND PERFORMED WITH MISSING INFORMATION'
      elif str(sBERTLV_Value[14:16]) == '01':
         sLog += 'COMMAND PERFORMED WITH PARTIAL COMPREHENSION'
      else:
         sLog += 'THE FRAMEWORK DOES NOT SUPPORT TERMINAL RESPONSE VALUE'

      sLog += '\n\tUSER EVENT IN DISPLAY TEXT: ' + str(sBERTLV_Value[28:])
      if str(sBERTLV_Value[28:]) == '00':
         sLog += ' => OK'
      elif str(sBERTLV_Value[28:]) == '10':
         sLog += ' => CANCEL'
      elif str(sBERTLV_Value[28:]) == '11':
         sLog += ' => BACKWARD'
      elif str(sBERTLV_Value[28:]) == '12':
         sLog += ' => NO ACTION'
   return sLog


# COTACmdAnalyzer ---------------------------------------------------------------------------------------------------------------------------------------------------------
# This method receives a list with proactive commands or terminal response commands and returns a string with the interpretation.
# The structure of list must be: 
# COMMAND(Terminal response or Proactive), Status Word 1, Status word 2.
# [D0 8D 81 03 01 21 81 82 02 81 02 8D 60 08 01 23 45 67 89 01 23 45 67 89
# 01 23 45 67 89 01 23 45 67 89 01 23 45 67 89 01 23 45 67 89 01 23 45 67 89
# 01 23 45 67 89 01 23 45 67 89 01 23 45 67 89 01 23 45 67 89 01 23 45 67 89
# 01 23 45 67 89 01 23 45 67 89 01 23 45 67 89 01 23 45 67 89 01 23 45 67 89
# 01 23 45 67 89 01 23 45 67 89 04 02 00 02, 90, 00]
# indice indicates the iteration number in cmd AND IS OPTIONAl
# in case sText is present, when analyzer founds a Display Text, check if text is equal
def COTACmdAnalyzer(lCommand='',sText=''):

   sLog = ''
   if len(lCommand) == 0:
      sLog += 'Command Empty'
      return sLog
   
   # if len(lCommand) % 2 != 0:
   #    sLog += 'The command is not correctly structured'
   #    return sLog
   
   # Cleaning spaces from the list
   lCommandnoSpaces = []
   for cmd in lCommand:
      sCmdnoSpaces = cmd.replace(' ', '')
      lCommandnoSpaces.append(sCmdnoSpaces)

   sLog += 'COMMAND: \n'
   #print("len(lCommandnoSpaces): " + str(len(lCommandnoSpaces)))
   if len(lCommandnoSpaces) < 3:
      sLog += str(lCommandnoSpaces)
   else:   
      sLog += 'APDU: 0x' + str_SpaceHexa(str(lCommandnoSpaces[0]))
      sLog += '\nSW1: 0x' + str_SpaceHexa(str(lCommandnoSpaces[1]))
      sLog += '\nSW2: 0x' + str_SpaceHexa(str(lCommandnoSpaces[2]))

   sLog += '\n\nINTERPRETING...'

   for indexPos, element in enumerate(lCommandnoSpaces):
      if indexPos == 0:
         sByte = element[:2]
         #Checking accordign first byte 
         match sByte:
            case 'D0':
               sLog += '\n\tCOMMAND HEADER: 0xD0 - SIM To Mobile Equipment direction - Proactive UICC command tag'
               # Counter to useful cases
               nCounter = 0

               sBERTLV_L = element[2:4]
               nCounter = 4
               if sBERTLV_L == '81':
                  #print('Length coded in 2 bytes according to ISO/IEC 7816: 0x81 - length is coded from 128 to 255 bytes')
                  sBERTLV_L = element[4:6]
                  nCounter = 6
               #Getting all BER TLV Values
               sBERTLV_Value = element [nCounter:]

               if sText:
                  sLog, _= COTAProactiveCMDProcess(sLog, sBERTLV_Value,sText) 
               else:
                  sLog, _= COTAProactiveCMDProcess(sLog, sBERTLV_Value)

            case '80':
               sByte = element[2:4]
               sBERTLV_Value = element[4:]
               if sByte == '14':
                  sLog = COTATerminalResponseProcess(sLog, sBERTLV_Value)
               elif sByte == '12':
                  print(str(element)+'\nInstruction Byte of the Commands for a telecom application - FETCH 0x80 12 - Mobile Equipment to SIM direction - Proactive UICC command tag')
            case _:
               sLog += '\n\tCOMMAND:\n\t' +  str(element)
               sLog += '\n\tThe Byte TAG ' + str(sByte)+ ' is not supported by the QA FRAMEWORK ANALYZER METHOD'

               return sLog
      else:
         sLog += '\n\tSW'+str(indexPos) + ' = '+element
         if indexPos == 2:
            elementint = int(element, base=16)
            sLog+= f'(in decimal = {elementint})'

   
   return sLog         

# lista = ['D081C18103012181820281028D81B50800A1004200690065006E00760065006E00690064006F0020006100200045006E00740065006C0021002000560069007600650020006C00610020006D0065006A006F007200200065007800700065007200690065006E006300690061002C00200054006F0064006F002000640065007300640065002000740075002000410070007000200045006E00740065006C002E0020263A002000A1004400650073006300E1007200670061006C006100200079006100219000']
# result=COTACmdAnalyzer(lista)
# print(result)
# def COTATextChecker(textinBytes,text):
#    #Decoding text in bytes
#     stextDecoded = bytes_DecodeText(textinBytes)

#     if stextDecoded == text:
#        return True
#     else:
#        return False
    
# result=COTATextChecker('27 0B 00 20 00 42 00 65 00 6D 00 2D 00 76 00 69 00 6E 00 64 00 6F 00 20 00 E0 00 20 00 72 00 65 00 64 00 65 00 20 00 4F 00 70 00 65 00 72 00 61 00 64 00 6F 00 72 00 2E 00 20 00 56 00 6F 00 63 00 EA 00 20 00 71 00 75 00 65 00 72 00 20 00 6D 00 65 00 6C 00 68 00 6F 00 72 00 61 00 72 00 20 00 6F 00 20 00 73 00 75 00 61 00 20 00 65 00 78 00 70 00 65 00 72 00 69 00 EA 00 6E 00 63 00 69 00 61 00 20 00 63 00 6F 00 6E 00 6F 00 73 00 63 00 6F 00 3F','? Bem-vindo � rede Operador. Voc� quer melhorar o sua experi�ncia conosco?')
# print(str(result))    
    

# COTA_GetVersionNumber ------------------------------------------------------------------------------------------------------
def COTA_GetVersionNumber(sCOTAVer):
    sReturn = ""
    sCOTA = sCOTA_COTA
    if str_instrBool(sCOTAVer, sCOTA):
       sReturn = str_getSubStringFromOcur(sCOTAVer,sCOTA,1)
       if len(sReturn) >= 4:
          sReturn = str_left(sReturn,4)
       
    return sReturn
    
# COTA_ProcessEmojisExtended ------------------------------------------------------------------------------------------------------
def COTA_ProcessEmojisExtended(emoji):
    
    hexflag = False

    if len(emoji) > 1:
       
       emoji = str_CleanWord(emoji,"U+")

       if len(emoji) <= 1:
          return "The argument " + str(emoji) + " is invalid, please check."
          
       #So, possible hexadecimal
       if is_valid_Hex(emoji) and int(emoji,16) < 0xFFFFF:
          code_point = int(emoji, 16)
       else:
           return "The argument " + str(emoji) + " is invalid, please check. The value in hexadecimal should be lower than 0xFFFFF."
    else:
       #print(emoji)
       #ord() function in Python is used to convert a single Unicode character into its integer representation.
       code_point = ord(emoji)
       #print(bytes_NroToHexa(code_point))

    if code_point < 0xFFFF:
        try:
            print(f'For the emoji {emoji} it is not necessary to do the calculation because it is in the UTF-16 range: {ord(emoji):X}\n')
        except Exception as e:
            print(f'For the emoji {emoji} it is not necessary to do the calculation because it is in the UTF-16 range: {emoji}\n')
        return  bytes_NroToHexa(code_point)
        
    sLog = "For the emoji " + str(emoji) + " : Unicode = U+{code_point:X}"
    #Convertir a un número de 20 bits (Bajo el rango de 0xFFFFF)
    code_point -=0x10000

    #Obtener los pares sustitutos (Surrogates pairs)

    """
    Para la operacion de obtener los 'Surrogates pairs' el rango de bytes D800 - DF FF se ha reservado.
    este rango se divide en dos bloques: (D8 00 - DBFF) y (DC 00 - DF FF)
    Para calcular el Unicode Transformation Format - 16 bits (UTF-16) se deben sumar los valores D800 y DC00 
    a los bits más significativos y menos signficativos, respectivamente.
    Antes de esta operación los bits del emoji original se les debe restar el hexadecimal 0x10000 (Linea 18 de este codigo)
    esta resta asegura que el valor del emoji baje al rango de 8 bits 0x000 - 0xFFFF para posteriormente poder calcular
    Su valor en el rango de 16 bits. 
    """
    # (code_point >> 10) realiza el desplazamiento de bits (Obtiene los bits más significativos). 
    # La expresión "& 0x3FF" después del desplazamiento a la derecha se utiliza para enmascarar 
    # (bitwise AND) los bits resultantes para asegurarse de que solo se toman en cuenta los 10 bits más bajos después del desplazamiento.
    high_surrogate = 0xD800 + ((code_point >> 10) & 0x3FF)
    low_surrogate = 0xDC00 + (code_point & 0x3FF)

    # Representar en UTF-16 Big Endian ()
    utf16_big_endian = high_surrogate.to_bytes(2, 'big') + low_surrogate.to_bytes(2, 'big')

    # Convertir a cadena hexadecimal y poner en mayúsculas
    utf16_big_endian_hex = utf16_big_endian.hex().upper()

    # Imprimir el valor hexadecimal
    sLog += f'UTF-16 Big Endian = {utf16_big_endian_hex}\n'
    print(sLog)
    
    return str(utf16_big_endian_hex)
    
# is_valid_Hex ------------------------------------------------------------------------------------------------------
#Validate if is valid hexadecimal
def is_valid_Hex(sHex):
    # delete 0x Prefix if is present
    if sHex.startswith('0x') or sHex.startswith('0X'):
        sHex = sHex[2:]

    # Verificar si la cadena es no vacía y contiene solo caracteres hexadecimales
    if sHex and all(caracter.isdigit() or caracter.lower() in 'abcdef' for caracter in sHex):
        return True
    else:
        return False

# COTA_validate_tpda ------------------------------------------------------------------------------------------------------
def COTA_validate_tpda(tpda):
    raw_tpda = str_SpacesOut(tpda)
    if len(tpda) >= 6 :
       tpda_decimal_len = int(bytes_HexaToNro(raw_tpda[0:2]))
       tpda = raw_tpda[4:]
       tpda = bytes_reverse(tpda).upper()
       if "F" in tpda:
          tpda = tpda.replace("F", "")
       if len(tpda) == tpda_decimal_len:
          return True
       else:
          return False
    else:
        return False      

# COTA_validate_time ------------------------------------------------------------------------------------------------------
def COTA_validate_time(sLogFileName, time_str):
    if len(time_str) != 6:
        sLog = "TIME received as PARAMETER: " + time_str + \
            " is not valid."
        log_write_ErrorInRed(sLogFileName, sLog)
        sys.exit(0)
    if int(time_str[0:2]) > 23:
        sLog = "TIME received as PARAMETER: " + time_str + \
            " is not valid. Hours must be less than 24"
        log_write_ErrorInRed(sLogFileName, sLog)
        sys.exit(0)
    if int(time_str[2:4]) > 59:
        sLog = "TIME received as PARAMETER: " + time_str + \
            " is not valid. Minutes must be less than 60"
        log_write_ErrorInRed(sLogFileName, sLog)
        sys.exit(0)
    if int(time_str[4:6]) > 59:
        sLog = "TIME received as PARAMETER: " + time_str + \
            " is not valid. Seconds must be less than 60"
        log_write_ErrorInRed(sLogFileName, sLog)
        sys.exit(0)
    return bytes_reverse(time_str)
    
# COTACampiagnID_Des ---------------------------------------------------------------------------------------------------------------------------------------------------------
def COTACampiagnID_Des(sCampaignID):
    return simcardCampaignID_Des(sCampaignID)

# COTA Validate status counter -----------------------------------------------------------------------------------------------------------------------------------------------
def COTA_validate_status_counter(str_log_file_name, status_counter):
    try:
        status_value = int(status_counter.replace(" ", ""), 16)
    except ValueError:
        log_write_ErrorInRed(str_log_file_name, f"Invalid status counter: {status_counter}")
        sys.exit(1)

    if 0 <= status_value <= 32767:
        return True
    return False


# cota_validate_proactive_command -----------------------------------------------------------------------------------------------------------------------------------------------
def cota_validate_proactive_command(log_file_name, response, cmd, tpda):
    """
    Validates if the response is a proactive command. If not, it logs an error and exits the program.
    :param log_file_name: Name of the log file
    :param response: Response received from the card
    :param cmd: Command sent to the card
    :param tpda: TPDA used
    :return: None
    """
    proactive_tag = response[0:2]
    if not proactive_tag == "D0":
        #log_write_ErrorInRed(
        log_write_WarningInYellow(
            log_file_name,
            f"""
                    We should be receiving a proactive command as a response... Exiting now. 
                    Command sent: {cmd}
                    TPDA used: {tpda}
                    Response reveived: {response} 
                    """
        )
        str = "If the command sent"
        if tpda != "N/A":
            str += f" and the TPDA used ({tpda}) are"
        else:
            str += " is"
        str += " correct, this may mean that the current version of the applet (2.5/2.6) does not support the command sent."

        log_write_WarningInYellow(log_file_name, str)
        #sys.exit()
        return False

    return True


# COTACmd_sendEnvelope_ResponseFirstByteCommand ---------------------------------------------------------------------------------------------------------------------------------------------------------
def COTACmd_sendEnvelope_ResponseFirstByteCommand(cardservice, sLogFileName, sCmd, sTPDAParam, sAPDU, sTAR=sSimcard_sDefTAR_COTA, bNetworkOKOrChangeIMEIOrChangeMCCMNC=True, sMCC="", sMNC=""):
    return simcardCmd_sendEnvelope_ResponseFirstByteCommand(cardservice, sLogFileName, sCmd, sTPDAParam, sAPDU, sTAR, bNetworkOKOrChangeIMEIOrChangeMCCMNC, sMCC, sMNC)

# COTACmd_sendEnvelopeConcat -----------------------------------------------------------------------------------------------------------------------------------------------
def COTACmd_sendEnvelopeConcat(cardservice, sLogFileName, sTPDAParam , sCMD):
    sReturn, sReturnDes = simcardCmd_sendEnvelopeConcat(cardservice, sLogFileName, sCMD, sTPDAParam)
    return sReturn

        
# SAPCmdF7_Interpret -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCmdF7_Interpret(sData, sTPDA=""):
    
    sCmd = "F7"
    sDataT, sReturnSMS, nCmdLenTotal = SAPCOTASMS_Interpret_GetData(sData, sTPDA, sCmd)

    sReturn = "Data in hexadecimal: 0x" +  str_AddSpaceHexa(sData) 
    if sReturnSMS != "":
       sReturn = sReturn + str_GetENTER() + sReturnSMS

    n = 0
    
    #Because it is taken each character per analysis
    nCmdLenTotal = nCmdLenTotal * 2
          
    nCmd = 0

    while n < nCmdLenTotal:
               
          nCmd = nCmd + 1
          #print("n: " + str(n))
               
          #Next byte is Cmd Nro - length
          sCmdLen = str_mid(sDataT, n, 2)
          n = n + 2
          nCmdLen = int(bytes_HexaToNro(sCmdLen))
          sTemp = str_mid(sDataT, n, nCmdLen * 2)
          sReturn = sReturn + str_GetENTER() + str_GetENTER() + "Command " + str(nCmd) + " - length: 0x" + sCmdLen + " - Decimal: " + str(nCmdLen) + " bytes."
          sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - total data: 0x" + str_AddSpaceHexa(sTemp) + " - ASCII: " + bytes_HexaToASCII(sTemp)
          
          # PLoci response for date/time is always 7 bytes
          sDateTime = str_left(sTemp, 14)
          sSMS = str_midToEnd(sTemp, 14)
          sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - date-time: 0x" + str_AddSpaceHexa(sDateTime) + " - Interpreted: " + fPLociGetDateTimeFromSIM(sDateTime)
          sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - data: 0x" + str_AddSpaceHexa(sSMS) + " - ASCII: " + bytes_HexaToASCII(sSMS)
          
          sCOTA = bytes_StrToHexa(sCOTA_COTA)
          if str_instrBool(sSMS, sCOTA):
             #IMEI SENT REFERENCE
             sTemp = str_getSubStringFromOcur(sSMS, sCOTA, 0)
             #print("sTemp: " + sTemp + " - Length: " + str(len(sTemp)))
             
             if len(sTemp) == 18:
                # Total 9 bytes => IMEI (8 bytes) + Launch Browser supported
                sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - COTA/SAP Provisioning: 0x" + str_AddSpaceHexa(sSMS) + " - Interpretation: " + SAPCOTASMSProvisioning_Interpret(sSMS)
             
          n = n + (nCmdLen * 2)

    sReturn = sReturn + str_GetENTER() + str_GetENTER() + "Total commands processed: " + str(nCmd) + "."
    sReturn = sReturn + str_GetENTER() 
           
    return sReturn    

# SAPCmdDD_Interpret -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCmdDD_Interpret(sData, sTPDA=""):
    
    sDataT = str_SpacesOut(sData).upper()
    sTPDA = str_SpacesOut(sTPDA).upper()
    
    sCmd = "DD"
    
    tMSISDNs = []

    sDataT, sReturnSMS, nCmdLenTotal = SAPCOTASMS_Interpret_GetData(sData, sTPDA, sCmd)

    sReturn = "Data in hexadecimal: 0x" +  str_AddSpaceHexa(sData) 
    if sReturnSMS != "":
       sReturn = sReturn + str_GetENTER() + sReturnSMS

    #Example for Data
    #Received:
    #SMPP  9. *** 0. SMS Data: 0x01 02 DD 45 17 00 00 00 00 00 00 00 0F 00 04 00 04 83 81 08 91 45 19 31 80 05 16 F9 17 00 00 00 00 00 00 00 0F 00 03 00 03 83 81 08 91 45 19 31 80 05 16 F8 14 00 00 00 00 00 00 00 0C 00 02 00 02 83 81 05 91 51 42 33 F6 - length: 73 bytes (0x49) (characters: 146) - ASCII: ___E_________________E_1_____________________E_1_____________________QB3_ 
    #Where:
    #01 02 = Campaign Number
    #DD = Command
    #45 = Lenth = 69 bytes
    #17 = Length = 23 bytes
    #00 00 00 00 00 00 00 = Date Time and Time Zone
    #0F = Length = 15 bytes
    #00 04 = Counter Call Connected
    #00 04 = Counter Call Disconnecte
    #83 81 = Source and Origin => 83 = network, 81 = uicc
    #08 91 45 19 31 80 05 16 F9 = MSISDN
    #17 = Length = 23 bytes
    #00 00 00 00 00 00 00 = Date Time and Time Zone
    #0F = Length = 15 bytes
    #00 03 = Counter Call Connected
    #00 03 = Counter Call Disconnected
    #83 81 = Source and Origin => 83 = network, 81 = uicc
    #08 91 45 19 31 80 05 16 F8 = MSISDN
    #14 = Length = 20 bytes
    #00 00 00 00 00 00 00 = Date Time and Time Zone
    #0C = length = 12 bytes
    #00 02 = Counter Call Connected
    #00 02 = Counter Call Disconnecte
    #83 81 = Source and Origin => 83 = network, 81 = uicc
    #05 91 51 42 33 F6 = MSISDN
    
    #Next byte is length
    if nCmdLenTotal > 0:
       sReturn = sReturn + str_GetENTER() + "IMPORTANT: All calls are informed like LIFO - last in/first out - first call is the last one executed."

    #Because it is taken each character per analysis
    nCmdLenTotal = nCmdLenTotal * 2
          
    n = 0
    nCmd = 0

    while n < nCmdLenTotal:
               
          nCmd = nCmd + 1
          #print("n: " + str(n))
               
          #Next byte is Cmd Nro - length
          sCmdLen = str_mid(sDataT, n, 2)
          n = n + 2
          nCmdLen = int(bytes_HexaToNro(sCmdLen))
          sTemp = str_mid(sDataT, n, nCmdLen * 2)
          sReturn = sReturn + str_GetENTER() + str_GetENTER() + "Call " + str(nCmd) + " - length with Date Time: 0x" + sCmdLen + " - Decimal: " + str(nCmdLen) + " bytes."
          sReturn = sReturn + str_GetENTER() + "Call " + str(nCmd) + " - total data: 0x" + str_AddSpaceHexa(sTemp) + " - ASCII: " + bytes_HexaToASCII(sTemp)
          
          # PLoci response for date/time is always 7 bytes
          sDateTime = str_left(sTemp, 14)
          sCall = str_midToEnd(sTemp, 14)
          if sDateTime != "":
             sReturn = sReturn + str_GetENTER() + "Call " + str(nCmd) + " - date-time: 0x" + str_AddSpaceHexa(sDateTime) + " - Interpreted: " + fPLociGetDateTimeFromSIM(sDateTime)
          if sCall != "":   
             sReturn = sReturn + str_GetENTER() + "Call " + str(nCmd) + " - data: 0x" + str_AddSpaceHexa(sCall) + " - ASCII: " + bytes_HexaToASCII(sCall)

          if sCall != "":
             m = 0
             #Call data length
             sCallLen = str_mid(sCall, m, 2)
             m = m + 2
             nCallLen = int(bytes_HexaToNro(sCallLen))
             sReturn = sReturn + str_GetENTER() + "Call " + str(nCmd) + " - length: 0x" + sCallLen + " - Decimal: " + str(nCallLen) + " bytes."

             #Counter Call Connected
             sCallConn = str_mid(sCall, m, 4)
             sReturn = sReturn + str_GetENTER() + "Call " + str(nCmd) + " - Call Connected Counter: 0x" + str_AddSpaceHexa(sCallConn) + " - Decimal: " + str_AddThousandToNumber(str(bytes_HexaToNro(sCallConn))) + "."
             m = m + 4

             #Counter Call Diconnected
             sCallDisConn = str_mid(sCall, m, 4)
             sReturn = sReturn + str_GetENTER() + "Call " + str(nCmd) + " - Call Disconnected Counter: 0x" + str_AddSpaceHexa(sCallDisConn) + " - Decimal: " + str_AddThousandToNumber(str(bytes_HexaToNro(sCallDisConn))) + "."
             m = m + 4
          
             #Source and Destination Call
             sCallSourceDest = str_mid(sCall, m, 4)
             sReturn = sReturn + str_GetENTER() + "Call " + str(nCmd) 
             sReturn = sReturn + " - Source " + simcard_deviceIdentities_Des(str_left(sCallSourceDest, 2), True) 
             sReturn = sReturn + str_GetENTER() + "Call " + str(nCmd) 
             sReturn = sReturn + " - Destination " + simcard_deviceIdentities_Des(str_right(sCallSourceDest, 2), True) 
             m = m + 4
             
             #Call MSISDN
             sCallMSISDN = str_midToEnd(sCall, m)
             sReturn = sReturn + str_GetENTER() + "Call " + str(nCmd) 
             sMSISDNDes, sMSISDNNro = simcard_MSISDN_TPDA_InterpretOnlyDes(sCallMSISDN, True)
             sReturn = sReturn + " - " + sMSISDNDes
             if sMSISDNNro != "":
                tMSISDNs.append(sMSISDNNro)


          n = n + (nCmdLen * 2)

    if nCmd > 0:
      sReturn = sReturn + str_GetENTER() + str_GetENTER() + "Total calls processed: " + str(nCmd) + "."
    
    sReturn = sReturn + str_GetENTER() 
           
    return sReturn, tMSISDNs    

# SAPCmdDE_Interpret -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCmdDE_Interpret(sData, sTPDA=""):
    
    sCmd = "DE"
    sDataT, sReturnSMS, nCmdLenTotal = SAPCOTASMS_Interpret_GetData(sData, sTPDA, sCmd)

    sReturn = "Data in hexadecimal: 0x" +  str_AddSpaceHexa(sData) 
    if sReturnSMS != "":
       sReturn = sReturn + str_GetENTER() + sReturnSMS

    n = 0

    if nCmdLenTotal > 0:
      
      nIncrement = 2
      sRepeatTimes = str_mid(sDataT, n, nIncrement)
      n = n + nIncrement
      sRepeatTimesExec = str_mid(sDataT, n, nIncrement)
      n = n + nIncrement

      nIncrement = 4
      sRepeatStatusCommands = str_mid(sDataT, n, nIncrement)
      n = n + nIncrement
      sRepeatStatusCommandsExec = str_mid(sDataT, n, nIncrement)
      n = n + nIncrement

      nIncrement = 2
      sRepeatSendSMSNot = str_mid(sDataT, n, nIncrement)
      n = n + nIncrement

      sRepeatCmd = ""
      sRepeatCmd = str_midToEnd(sDataT, n)

      if sRepeatTimes != "":
         sReturn = sReturn + str_GetENTER() + bytes_LengthDescription(sRepeatTimes, "Repeat Times")
      if sRepeatTimesExec != "":
         sReturn = sReturn + str_GetENTER() + bytes_LengthDescription(sRepeatTimesExec, "Repeat Times Executed")
      if sRepeatStatusCommands != "":
         sReturn = sReturn + str_GetENTER() + bytes_LengthDescription(sRepeatStatusCommands, "Status Commands")
      if sRepeatStatusCommandsExec != "":
         sReturn = sReturn + str_GetENTER() + bytes_LengthDescription(sRepeatStatusCommandsExec, "Status Commands Executed")

      if sRepeatSendSMSNot != "":
         sReturn = sReturn + str_GetENTER() + "Send SMS for command in each repetition: 0x" + sRepeatSendSMSNot + " - "
         if sRepeatSendSMSNot == "31":
            sReturn = sReturn + "No"
         else:
            sReturn = sReturn + "Yes"

      if sRepeatCmd != "":
         sReturn = sReturn + str_GetENTER() + "Command to be repeated: 0x" + str_SpaceHexa(sRepeatCmd) + " - Command length: " + str(len(sRepeatCmd)//2) + " bytes."

    return sReturn, sRepeatTimes, sRepeatTimesExec, sRepeatStatusCommands, sRepeatStatusCommandsExec, sRepeatSendSMSNot, sRepeatCmd

# SAPCmdD4_Interpret -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCmdD4_Interpret(sData, sTPDA=""):
    sCmdInterpret, sICCID, sIMSI, sLOCI, sACCTECH, sAppletCompleteinHexa = SAPCmdD4_InterpretComplete(sData, sTPDA)
    return sCmdInterpret

# SAPCmdD4_InterpretComplete -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCmdD4_InterpretComplete(sData, sTPDA=""):
    
    sCmd = "D4"
    sReturnSMS = ""
    nCmdLenTotal = 0

    if sTPDA != "":
      sDataT, sReturnSMS, nCmdLenTotal = SAPCOTASMS_Interpret_GetData(sData, sTPDA, sCmd)
    else:
       nCmdLenTotal = len(sData) // 2
       sDataT = sData

    if str_left(sDataT, 2) != sCmd:
       # IT MAY BE THE CAMPAIGN REFERENCE
       sDataT = str_midToEnd(sDataT, 4)

    sReturn = "Data in hexadecimal: 0x" +  str_AddSpaceHexa(sData) 
    if sReturnSMS != "":
       sReturn = sReturn + str_GetENTER() + sReturnSMS

    sAppletName, sAppletCompleteinHexa, sAppletVersionOnly = simcard_processSMSData_AutoProvisioning_AppletVersion(sData)

    sICCID = ""
    sIMSI = ""
    sLOCI = ""
    sACCTECH = ""
    sAppletCompleteinHexa = ""

    n = 0

    if nCmdLenTotal > 0 and sAppletName == sSimcard_sDefTAR_COTA_Name:

      #print("sDataT = " + str(sDataT))

      nIncrement = 2
      sCmd = str_mid(sDataT, n, nIncrement)
      n = n + nIncrement

      nIncrement = 20
      sICCID = str_mid(sDataT, n, nIncrement)
      if sICCID != "":
         sReturn = sReturn + str_GetENTER() + simcard_EF_ICCID_Interpret(sICCID, True)
      n = n + nIncrement

      nIncrement = 18
      sIMSI = str_mid(sDataT, n, nIncrement)
      if sIMSI != "":
         sReturn = sReturn + str_GetENTER() + simcard_EF_IMSI_Interpret(sIMSI, True)
      n = n + nIncrement

      nIncrement = 18
      sLOCI = str_mid(sDataT, n, nIncrement)
      if sLOCI != "":
         sReturn = sReturn + str_GetENTER() + "LOCI: " + sLOCI + str_GetENTER() + "LOCI INTERPRETED: " + str_GetENTER() + loci_lociFromHexa(sLOCI, True)
      n = n + nIncrement

      nIncrement = 2
      sACCTECH = str_mid(sDataT, n, nIncrement)
      if sACCTECH != "":
         sReturn = sReturn + str_GetENTER() + "ACCESS TECHNOLOGY: " + sACCTECH + " - INTERPRETED: " + str_GetENTER() + fPLociACCTECHDes(sACCTECH)
      n = n + nIncrement

      sAppletName, sAppletCompleteinHexa, sAppletVersionOnly = simcard_processSMSData_AutoProvisioning_AppletVersion(sData)

      sReturn = sReturn + str_GetENTER() + "APPLET '" + sAppletName + "' VERSION: " + sAppletVersionOnly + " - HEXA: 0x" + str_SpaceHexa(sAppletCompleteinHexa)

    else:
      if nCmdLenTotal > 0 and sAppletName == sSimcard_sDefTAR_SAPROAM_Name:
         sDataT = str_midToEnd(sDataT, 2)
         sIMEI, sLaunchSupported, sIMEIOld, sLaunchSupportedOld, sICCID, sIMSI, sIMSIOld, sAD, sADOld, sSPN, sSPNOld, sLOCI, sACCTECH, sAPPLETVersionCompleteInHexa, sDes = simcard_processSMSData_AutoProvisioning(sDataT, True, str_GetENTER())
         sReturn = sDes

    return sReturn, sICCID, sIMSI, sLOCI, sACCTECH, sAppletCompleteinHexa

# SAPCmdC0_Interpret -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCmdC0_Interpret(sData, sTPDA=""):
    
    sCmd = "C0"
    sReturnSMS = ""
    nCmdLenTotal = 0

    if sTPDA != "":
      sDataT, sReturnSMS, nCmdLenTotal = SAPCOTASMS_Interpret_GetData(sData, sTPDA, sCmd)
    else:
       nCmdLenTotal = len(sData) // 2
       sDataT = sData

    if str_left(sDataT, 2) != sCmd:
       # IT MAY BE THE CAMPAIGN REFERENCE
       sDataT = str_midToEnd(sDataT, 4)

    sReturn = "Data in hexadecimal: 0x" +  str_AddSpaceHexa(sData) 
    if sReturnSMS != "":
       sReturn = sReturn + str_GetENTER() + sReturnSMS

    if nCmdLenTotal > 0:

      if sCmd in str(sDataT):
            sTemp = str_getSubStringFromOcurFirst(sDataT, sCmd)
            sTerminalProfile = str_midToEnd(sDataT, len(sTemp) + len(sCmd))
            sTerminalProfileDes = bytes_LengthDescriptionAndData(sTerminalProfile)
            sReturn = sReturn + str_GetENTER() + "\nTerminal Profile Data in SMS:\n" + sTerminalProfileDes

            sInterpreted = simcardTerminalProfileParser.parse(sTerminalProfile)

            sReturn = sReturn + str_GetENTER() + "\nInterpreted Terminal Profile:\n" + sInterpreted
      
    return sReturn

# SAPCmdC1_Interpret -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCmdC1_Interpret(sData, sTPDA=""):
    
    sCmd = "C1"
    sReturnSMS = ""
    nCmdLenTotal = 0

    nPollingInterval = 0
    sStatusSettingPollingInterval = ""

    if sTPDA != "":
      sDataT, sReturnSMS, nCmdLenTotal = SAPCOTASMS_Interpret_GetData(sData, sTPDA, sCmd)
    else:
       nCmdLenTotal = len(sData) // 2
       sDataT = sData

    if str_left(sDataT, 2) != sCmd:
       # IT MAY BE THE CAMPAIGN REFERENCE
       sDataT = str_midToEnd(sDataT, 4)

    sReturn = "Data in hexadecimal: 0x" +  str_AddSpaceHexa(sData) 
    if sReturnSMS != "":
       sReturn = sReturn + str_GetENTER() + sReturnSMS

    if nCmdLenTotal > 0:

      if sCmd in str(sDataT):
            sTemp = str_getSubStringFromOcurFirst(sDataT, sCmd)
            sPollingInterval = str_midToEnd(sDataT, len(sTemp))
            sPollingIntervalDes = bytes_LengthDescriptionAndData(sPollingInterval)
            sReturn = sReturn + str_GetENTER() + "Polling Interval Data:\n" + sPollingIntervalDes

            sReturn = sReturn + str_GetENTER() + "Tag: 0x" + str(str_left(sPollingInterval, 2))

            sPollingInterval = str_midToEnd(sDataT, len(sCmd))
            sPollingIntervalHexa = str_left(sPollingInterval, 2) 
            nPollingInterval = int(bytes_HexaToNro(sPollingIntervalHexa))

            sAppletName, sAppletCompleteinHexa, sAppletVersionOnly = simcard_processSMSData_AutoProvisioning_AppletVersion(sPollingInterval)

            sStatusSettingPollingInterval = str_getSubStringFromOcurFirst(sPollingInterval, sAppletCompleteinHexa)
            if sStatusSettingPollingInterval != "":
               sStatusSettingPollingInterval = str_right(sStatusSettingPollingInterval, 4)
               if len(str(sStatusSettingPollingInterval)) != 4:
                  sStatusSettingPollingInterval = ""

            sReturn = sReturn + str_GetENTER() + "Interpreted Polling Interval response:" 
            sReturn = sReturn + str_GetENTER() + "Polling Interval: 0x" + str(sPollingIntervalHexa) + " (decimal: " + str(nPollingInterval) + ") seconds." 
            if sStatusSettingPollingInterval != "":
               sReturn = sReturn + str_GetENTER() + "Status Setting Polling Interval: 0x" + str_SpaceHexa(sStatusSettingPollingInterval) + " - ASCII: " + str(bytes_HexaToASCII(sStatusSettingPollingInterval))

            if sAppletCompleteinHexa != "":
               sReturn = sReturn + str_GetENTER() + "Applet Version: 0x" + str_SpaceHexa(sAppletCompleteinHexa) + " - ASCII: " + str(bytes_HexaToASCII(sAppletCompleteinHexa))
      
    return sReturn, nPollingInterval, sStatusSettingPollingInterval

# SAPCOTASMS_Interpret_GetData -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCOTASMS_Interpret_GetData(sData, sTPDA="", sCmd=""):
    
    sReturn = ""

    sDataT = str_SpacesOut(sData).upper()
    sTPDA = str_SpacesOut(sTPDA).upper()

    if sTPDA!="":
       #D0 49 81 03 01 13 00 82 02 81 83 0B 3E 05 00 05 81 06 01 F4 00 04 34 F7 32 18 42 11 62 21 64 21 29 4A 41 31 41 81 41 41 45 31 43 4F 54 41 30 35 30 36 18 42 11 62 21 54 94 29 4A 41 31 41 81 41 41 45 31 43 4F 54 41 30 35 30 36
       
       #Getting data after TPDA
       sTemp = str_getSubStringFromOcur(sDataT, sTPDA, 1)
       sReturn = sReturn + str_GetENTER() + "TPDA: 0x" + str_AddSpaceHexa(sTPDA)
       
       #Next 2 bytes are PID and DCS
       n = 0
       sReturn = sReturn + str_GetENTER() + "PID - Protocol ID: 0x" + str_mid(sTemp, n, 2)
       n = n + 2
       sReturn = sReturn + str_GetENTER() + "DCS - Data Coding Scheme: 0x" + str_mid(sTemp, n, 2)
       n = n + 2
       
       #Next byte is length
       sReturn = sReturn + str_GetENTER() + "SMS length: 0x" + str(str_mid(sTemp, n, 2)) + " - Decimal: " + str(bytes_HexaToNro(str_mid(sTemp, n, 2))) + " bytes."
       n = n + 2
       
       sDataT = str_midToEnd(sTemp, n)

    if sCmd != "":
      if str_left(sDataT, 2) != sCmd:
         #There is campaign id
         sReturn = sReturn + str_GetENTER() + "Command campaign ID: " + str_SpaceHexa(str_left(sDataT, 4))
         sDataT = str_midToEnd(sDataT, 4)

      if str_left(sDataT, 2) == sCmd:   
         sReturn = sReturn + str_GetENTER() + "Command 0x" + sCmd + " received."
         sDataT = str_midToEnd(sDataT, 2)

    #Next byte is length
    sCmdLenTotal = str_mid(sDataT, 0, 2)
    nCmdLenTotal = int(bytes_HexaToNro(sCmdLenTotal))
    sReturn = sReturn + str_GetENTER() + "Total Command length: 0x" + sCmdLenTotal + " - Decimal: " + str(nCmdLenTotal) + " bytes."
    if nCmdLenTotal == 0:
       sReturn = sReturn + " - Applet buffer is empty, cleanned."
    else:
       sDataT = str_midToEnd(sDataT, 2)

    return sDataT, sReturn, nCmdLenTotal

# SAPCOTASMSProvisioning_Interpret -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCOTASMSProvisioning_Interpret(sData):
    return COTA_processSMS(sData)

#------------------------------------------------------------------------------------
# COTA_MSISDN_get_Country_TelecomPrefix_And_Des => Get Country Telecom Prefix and Description from MSISDN
#------------------------------------------------------------------------------------
def COTA_MSISDN_get_Country_TelecomPrefix_And_Des(sMSISDN):

    sReturn = COTA_MSISDN_get_Country_Block(sMSISDN)
    
    if len(sReturn) >= 2:
       return len(sReturn[0]), sReturn[1]
    
    return 2, ""
       
#------------------------------------------------------------------------------------
# COTA_MSISDN_get_Country_Block => Get the whole data block from countries_dic from MSISDN Prefix
#------------------------------------------------------------------------------------
def COTA_MSISDN_get_Country_Block(sMSISDN):

    sReturn = []

    sMSISDN = str_SpacesOut(sMSISDN)    
    if sMSISDN == "":
       return sReturn

    nItems = len(countries_dic)
    n = 0
    
    while n < nItems:

          sPrefix = countries_dic[n]

          if str_left(sMSISDN, len(sPrefix)) == sPrefix:

             # PREFIX MSISDN FOUND
             m = 0
             while m < countries_dic_block:
                   sReturn.append(countries_dic[n+m])
                   m = m + 1

             return sReturn
 
          n = n + countries_dic_block
    
    return sReturn


#------------------------------------------------------------------------------------
# COTA_APDU_SMPP_general_validations => Performs general validations of an APDU / SMPP
#------------------------------------------------------------------------------------
def COTA_APDU_SMPP_general_validations(cmd, is_apdu = True):
    """Perform general validations of an APDU / SMPP
    If validation passes, it returns: True, cmd
    If validation fails, it returns: False, error_list
    """
    cmd = cmd.replace(" ", "")
    expected_cmd_len = 8
    conditions_ok = True
    error_message_list = []

    cmd_type = "APDU"
    if not is_apdu:
        expected_cmd_len = 2
        cmd_type = "SMPP"
        # cmd_temp = cmd
        # campaign_id, cmd = COTAGetCampaignIDFromCmd(cmd)
        #
        # if not campaign_id and cmd != cmd_temp:
        #     error_message_list.append(cmd)
        #     return False, error_message_list

    """
    To simplify multiple conditions, a tuple is used where the first value is the conditional and the
    second is the error message if the condition is not met.
    """
    critical_conditions = [
        (len(cmd) % 2 == 0,             f"Invalid {cmd_type}. Should be of even length, but instead has: {len(cmd)} chars. Input value:\n{cmd}"),
        (len(cmd) >= expected_cmd_len,  f"Invalid {cmd_type}, it must have at least {expected_cmd_len} bytes, that is, {expected_cmd_len * 2}  characters, but instead has: {len(cmd)//2}. Input value:\n{cmd}"),
        (bytes_IsHexaValid(cmd),        f"Invalid {cmd_type}. Must be a hexadecimal string. Input value:\n{cmd}")
    ]


    # Loop that goes through the critical conditions that the message must meet
    for critical_condition, error_message in critical_conditions:
        if not critical_condition:
            conditions_ok = False
            error_message_list.append(error_message)
            return conditions_ok, error_message_list

    return conditions_ok, cmd


# ------------------------------------------------------------------------------------
# cota_SAP_CampaignResponse_Interpret => Process Data from hexadecimal
# ------------------------------------------------------------------------------------
def cota_SAP_CampaignResponse_Interpret(sHex):
    sHex = str_SpacesOut(sHex)
    sHex = sHex.upper()

    # print("sHex: " + sHex)

    # sReturn = sHex
    sSepara = " - "

    # ---------------------------------------------------------------------------------
    # MOVED THEM TO constants.py
    # sCOTA = "COTA"
    # sPopUpOK = "31"
    # sPopUpNOK = "30"
    # sPopUpCANCEL = sPopUpNOK + "10"
    # sPopUpBACK = sPopUpNOK + "11"
    # sPopUpNOACTION = sPopUpNOK + "12"
    # sPopUpERROR = sPopUpNOK + sPopUpNOK

    sAscii = bytes_HexaToASCII(sHex)

    sIMEIHex = ""
    sIMEIAscii = ""
    sLAUNCHBROWSERHex = ""
    sLAUNCHBROWSER = ""
    sCOTAVer = ""
    sPopUpResult = ""

    if str_instrBool(sAscii.upper(), sCOTA_COTA):
        # GET COTA VERSION
        sCOTAVer = str_getSubStringFromOcur(sAscii.upper(), sCOTA_COTA, 1)

        # GET DATA BEFORE COTA VERSION
        # print("sHex: " + sHex)
        # print("bytes_StrToHexa(sCOTA): " + bytes_StrToHexa(sCOTA_COTA))
        sIMEIHex = str_getSubStringFromOcur(sHex, bytes_StrToHexa(sCOTA_COTA).upper(), 0)
        # print("sIMEIHex: " + sIMEIHex)

        if len(sIMEIHex) >= 18:
            sLAUNCHBROWSERHex = str_right(sIMEIHex, 2)
            sIMEIHex = str_right(sIMEIHex, 18)
            sIMEIHex = str_left(sIMEIHex, 16)
        else:
            if len(sIMEIHex) >= 16:
                sIMEIHex = str_left(sIMEIHex, 16)
    else:
        # CHECK POPUP RESULT
        sTemp = str_left(sHex, 2)
        if sTemp == sCOTA_PopUpOK:
            sPopUpResult = sTemp + sSepara + sCOTA_PopUpOK_des
        if sTemp == sCOTA_PopUpNOK:
            sTemp = str_left(sHex, 4)
            if sTemp == sCOTA_PopUpCANCEL:
                sPopUpResult = sTemp + sSepara + sCOTA_PopUpCANCEL_des
            if sTemp == sCOTA_PopUpBACK:
                sPopUpResult = sTemp + sSepara + sCOTA_PopUpBACK_des
            if sTemp == sCOTA_PopUpNOACTION:
                sPopUpResult = sTemp + sSepara + sCOTA_PopUpNOACTION_des
            if sTemp == sCOTA_PopUpNOTSupported:
                sPopUpResult = sTemp + sSepara + sCOTA_PopUpNOTSupported_des
                if len(sHex) >= 20:
                    sIMEIHex = str_mid(sHex, 4, 16)

    if sIMEIHex != "":
        # PROCESS IMEI
        # print("sIMEIHex: " + sIMEIHex)
        sIMEIAscii = loci_imeiFromHexa(sIMEIHex, False)

    if sLAUNCHBROWSERHex != "":
        if sLAUNCHBROWSERHex == sCOTA_LaunchBrowserSupported:
            sLAUNCHBROWSERHex = sLAUNCHBROWSERHex + sSepara + sCOTA_LaunchBrowserSupported_des
        if sLAUNCHBROWSERHex == sCOTA_LaunchBrowserSupportedNOT:
            sLAUNCHBROWSERHex = sLAUNCHBROWSERHex + sSepara + sCOTA_LaunchBrowserSupportedNOT_des

    sReturn = ""
    if sCOTAVer != "":
        sReturn = sReturn + sCOTA_COTA + " version: " + sCOTAVer + sSepara
    if sPopUpResult != "":
        sReturn = sReturn + "PopUp Result: " + sPopUpResult + sSepara
    if sIMEIHex != "":
        sReturn = sReturn + "IMEI Hexadecimal: 0x" + str_SpaceHexa(sIMEIHex)
        if sIMEIAscii != "" and sIMEIAscii != sIMEIHex:
            sReturn = sReturn + sSepara + sIMEIAscii + sSepara
    if sLAUNCHBROWSERHex != "":
        sReturn = sReturn + "Launch Browser: " + sLAUNCHBROWSERHex + sSepara

    if str_right(sReturn, len(sSepara)) == sSepara:
        sReturn = str_left(sReturn, len(sReturn) - len(sSepara))

    #ADDED Autoprovisioning data
    sIMEI, sLaunchSupported, sIMEIOld, sLaunchSupportedOld, sICCID, sIMSI, sIMSIOld, sAD, sADOld, sSPN, sSPNOld, sLOCI, sACCTECH, sAppletVersion, sDes = simcard_processSMSData_AutoProvisioning(sHex, True)
    if sDes != "" and sICCID != "":
       #NOT FOR COTA0209
       sReturn = sDes    
    else:
       if sDes != "" and sLaunchSupported != "":
           sReturn = sReturn + str_GetENTER() + sDes 

    return sReturn

# COTA_GetAppletVersion ------------------------------------------------------------------------------------------------------
def COTA_GetAppletVersion(sHexa):
    sReturn = ""

    sHexa = str_SpacesOut(sHexa)
    sHexa = sHexa.upper()

    sHexaASCII = bytes_HexaToASCII(sHexa)

    sApplet = ""
    if str_instrBool(sHexaASCII, sCOTA_COTA):
       sApplet = sCOTA_COTA

    if str_instrBool(sHexaASCII, sCOTA_AUTH):
       sApplet = sCOTA_AUTH

    if str_instrBool(sHexaASCII, sCOTA_SARM):
       sApplet = sCOTA_SARM

    if sApplet != "":
       sReturn = str_getSubStringFromOcur(sHexaASCII, sApplet, 1)
       if len(sReturn) >= 4:
          sReturn = sApplet + sReturn

    return sReturn

# COTA_processCmd_FC_DC ------------------------------------------------------------------------------------------------------
def COTA_processCmd_FC_DC(sHexa):
    
    sResponse = ""

    sDC = "DC"
    sFC = "FC"

    sHexa = str_SpacesOut(sHexa)
    sHexa = sHexa.upper()

    if sHexa != "" and sHexa!="9000":

       sHexa = simcard_Clean9000(sHexa)

       #DATE TIME IS ALWAYS 7 BYTES
       nDateTimeLen = 7 * 2

       n = 0
       nA = 2
       sCmd = str_mid(sHexa, n, nA) 

       sResponse = sResponse + "Command: " + sCmd
       n = n + nA

       bOnlyDateTimeInformed = False
       if sCmd == sDC or sCmd == sFC:
          sResto = str_midToEnd(sHexa, n)
          #print("sResto: " + sResto + " - " + simcard_LengthReference(sResto))
          if len(sResto) % nDateTimeLen == 0:
             #THERE IS ONLY INFORMED DATE TIMEs
             bOnlyDateTimeInformed = True

       nA = nDateTimeLen
       sVal = str_mid(sHexa, n, nA)
       sResponse = sResponse + str_GetENTER() + fPLociGetDateTimeFromSIM(sVal, True, "Default")
       n = n + nA

       sResto = str_midToEnd(sHexa, n)
       #print("sResto: " + sResto + " - " + simcard_LengthReference(sResto))

       if len(sResto) > 0:
          
          #Get Time Zone for SDK/APKs ID   
          m = 0
          n = 0
          while n < len(sResto):
                sReference = "SDK/APK ID reference: " + str(m+1)
                m = m + 1

                nA = nDateTimeLen
                sVal = str_mid(sResto, n, nA)
                n = n + nA
                sResponse = sResponse + str_GetENTER() + fPLociGetDateTimeFromSIM(sVal, True, sReference)

                if not bOnlyDateTimeInformed:
                   nA = 2
                   sSDKIDLen = str_mid(sResto, n, nA)
                   nSDKIDLen = bytes_HexaToNro(sSDKIDLen)
                   n = n + nA
                   sResponse = sResponse + str_GetENTER() + sReference + " - SDK ID/APK Length: 0x" + sSDKIDLen + " (decimal: " + str(nSDKIDLen) + ")"
               
                   if sSDKIDLen != "00":
                      #THERE IS A SDK ID REFERENCES
                      nA = int(nSDKIDLen) * 2
                      sSDKID = str_mid(sResto, n, nA)
                      #print("nA = " + str(nA) + " - sSDKID: " + sSDKID)
                      n = n + nA
                      sResponse = sResponse + str_GetENTER() + sReference + " - SDK ID/APK: 0x" + str_SpaceHexa(sSDKID) + " (ASCII: " + bytes_HexaToASCII(sSDKID) + ")"

    return sResponse

# SAPCmdDF_Interpret -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCmdDF_Interpret(sData, sTPDA=""):
    
    sDataT = str_SpacesOut(sData).upper()
    sTPDA = str_SpacesOut(sTPDA).upper()
    nCmdLenTotal = len(sDataT)
    
    sCmd = "DF"

    sReturn = "Data in hexadecimal: 0x" +  str_AddSpaceHexa(sData) 

    if sTPDA != "":

         sDataT, sReturnSMS, nCmdLenTotal = SAPCOTASMS_Interpret_GetData(sData, sTPDA, sCmd)

         if sReturnSMS != "":
            sReturn = sReturn + str_GetENTER() + sReturnSMS

         #Because it is taken each character per analysis
         nCmdLenTotal = nCmdLenTotal * 2
    else:
       #Go to command length
       sDataT = str_midToEnd(sDataT, 2)
          
    n = 0
    nCmd = 0

    while n < nCmdLenTotal:
               
          #Next byte is Cmd Nro - length
          sCmdLen = str_mid(sDataT, n, 2)
          n = n + 2
          nCmdLen = int(bytes_HexaToNro(sCmdLen))
          #print("sCmdLen = " + str(sCmdLen) + " - nCmdLen = " + str(nCmdLen))

          if nCmdLen == 0:
             break

          nCmd = nCmd + 1
          #print("n: " + str(n))

          sDFDataItem = str_mid(sDataT, n, nCmdLen * 2)
          sReturn = sReturn + str_GetENTER() + str_GetENTER() + "Response " + str(nCmd) + " - length: 0x" + sCmdLen + " - Decimal: " + str(nCmdLen) + " bytes."
          sReturn = sReturn + str_GetENTER() + "Response " + str(nCmd) + " - total data: 0x" + str_AddSpaceHexa(sDFDataItem) + " - ASCII: " + bytes_HexaToASCII(sDFDataItem)
          
          if nCmdLen == 4 and sDFDataItem == str_right(sDataT, 8):
             sFile = str_left(sDFDataItem, 4)
             #IT MAY BE AN UICC ERROR
             sUICCException = str_right(sDFDataItem, 2)
             sUICCException = simcard_UICCException_GetDes(sUICCException)
             if sUICCException != "":
                sReturn  = sReturn + str_GetENTER() + "For File: '" + str_AddSpaceHexa(sFile) + "' - " + sUICCException

          #print("SAPCmdDF_Interpret - sDFDataItem: " + str(sDFDataItem))

          sFCP = simcard_File_FCPAnalysis(sDFDataItem, nCmd)
          if sFCP != "":
               sReturn = sReturn + str_GetENTER() + sFCP
          else:
             
             nSubItem = 0
             m = 0

             #print("nCmdLen: " + str(nCmdLen))

             while m < (nCmdLen * 2):
                  sCmdLenSubItem = str_mid(sDataT, n + m, 2)
                  m = m + 2
                  nCmdLenSubItem = int(bytes_HexaToNro(sCmdLenSubItem))
                  sDFDataSubItem = str_mid(sDataT, n + m, nCmdLenSubItem * 2)

                  #print("nCmdLenSubItem: " + str(nCmdLenSubItem))

                  nSubItem = nSubItem + 1
                  sReturn = sReturn + str_GetENTER() + "Response " + str(nCmd) + " - subitem " + str(nSubItem) + " - length: 0x" + sCmdLenSubItem + " - Decimal: " + str(nCmdLenSubItem) + " bytes."
                  sReturn = sReturn + str_GetENTER() + "Response " + str(nCmd) + " - subitem " + str(nSubItem) + " - total data: 0x" + str_AddSpaceHexa(sDFDataSubItem) + " - ASCII: " + bytes_HexaToASCII(sDFDataSubItem)

                  m = m + (nCmdLenSubItem * 2)

          n = n + (nCmdLen * 2)

    if nCmd > 0:
      sReturn = sReturn + str_GetENTER() + str_GetENTER() + "Total Responses processed: " + str(nCmd) + "."
    
    sReturn = sReturn + str_GetENTER() 
           
    return sReturn

# SAPCmdDF_InterpretToBeSent -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCmdDF_InterpretToBeSent(sData):
   sReturn = ""

   bUpdFile = False

   sData = str_SpacesOut(sData).upper()

   if sData == "":
      return ""
   
   n = 0

   sReturn = sReturn + str_GetENTER() + "Command to be sent: 0x" + str_AddSpaceHexa(sData) + " - Length: " + str(len(sData)//2) + " bytes."

   sDF = "DF"
   sEF = "EF"
   sAID = "AD"
   sD6 = "D6"

   if str_left(sData, 2) == sDF:
      sReturn = sReturn + str_GetENTER() + "SMPP Command: 0x" + sDF + " - Read SIM files."
      n = n + 2

   if str_left(sData, 1) == "8" and str_mid(sData, 2, 2) == sDF:
      sReturn = sReturn + str_GetENTER() + "APDU Command: 0x" + sDF + " - Read SIM files."
      n = n + 8

   sCmdLenTotal = str_mid(sData, n, 2)
   nCmdLenTotal = int(bytes_HexaToNro(sCmdLenTotal))
   sReturn = sReturn + str_GetENTER() + "Command length: 0x" + sCmdLenTotal + " - Decimal: " + str(nCmdLenTotal) + " bytes."
   n = n + 2

   nCmd = 1

   while n < len(sData) and n < (nCmdLenTotal * 2):

      sByte = str_mid(sData, n, 2)
      n = n + 2
      #print("sByte: " + str(sByte))

      bFound = False

      if sByte == sDF:
         bFound = True

         #DEDICATED FILE
         sReturn = sReturn + str_GetENTER() + str_GetENTER() + "Command " + str(nCmd) + " - Select DF - Dedicated File: " + sByte

         sCmdLen = str_mid(sData, n, 2)
         nCmdLen = int(bytes_HexaToNro(sCmdLen))
         sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - length: 0x" + sCmdLen + " - Decimal: " + str(nCmdLen) + " bytes."
         n = n + 2

         sFile = str_mid(sData, n, (nCmdLen + 2))
         sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - Select DF - Dedicated File: " +str_AddSpaceHexa(sFile)
         n = n + (nCmdLen * 2)

      if sByte == sEF:
         bFound = True

         #ELEMENTARY FILE
         sReturn = sReturn + str_GetENTER() + str_GetENTER() + "Command " + str(nCmd) + " - Select EF - Elementary File: " + sByte

         sCmdLen = str_mid(sData, n, 2)
         nCmdLen = int(bytes_HexaToNro(sCmdLen))
         sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - length: 0x" + sCmdLen + " - Decimal: " + str(nCmdLen) + " bytes."
         n = n + 2

         sFile = str_mid(sData, n, 4)
         sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd)
         n = n + 4

         if nCmdLen == 2:
            sReturn = sReturn + " - Get Response"
         else:   

            sFileType = "Transparent"
            if nCmdLen == 5:
               sFileType = "Linear/Cyclic"

            sFile = "'" + str_AddSpaceHexa(sFile) + " (" + sFileType + ")'"

            sReturn = sReturn + " - Process"
            
            sReturn = sReturn + " for EF: " + sFile

            sOffset = str_mid(sData, n, 2)
            sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - Start position for processing file " + sFile + ": 0x" +  sOffset + " - Decimal: " + str(bytes_HexaToNro(sOffset))
            n = n + 2
            
            sReadLen = str_mid(sData, n, 2)
            sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - Bytes to process for file " + sFile + ": 0x" +  sReadLen + " - Decimal: " + str(bytes_HexaToNro(sReadLen))
            n = n + 2

            if nCmdLen == 5:
               sReadRecord = str_mid(sData, n, 2)
               sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - Record to process for file " + sFile + ": 0x" +  sReadRecord + " - Decimal: " + str(bytes_HexaToNro(sReadRecord))
               n = n + 2

            sByte = str_mid(sData, n, 2)
            if sByte == sD6:
               bUpdFile  = True
               n = n + 2
               sUpdLen = str_mid(sData, n, 2)
               nUpdLen = int(bytes_HexaToNro(sUpdLen))
               n = n + 2
               sUpdData = str_mid(sData, n, nUpdLen * 2)
               n = n + (nUpdLen * 2)

               sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - Update " + sFile + " with TAG 0x" + sD6
               sReturn = sReturn + " - Data length: 0x" + sUpdLen + " (decimal: " + str(nUpdLen) + ")"
               sReturn = sReturn + " - Data: 0x" + str_AddSpaceHexa(sUpdData) + " (ASCII: " + bytes_HexaToASCII(sUpdData) + ")"

         nCmd = nCmd + 1

      if sByte == sAID:
         bFound = True

         #APPLET AID
         sReturn = sReturn + str_GetENTER() + str_GetENTER() + "Command " + str(nCmd) + " - Select AID - Application Dedicated File: " + sByte

         sCmdLen = str_mid(sData, n, 2)
         nCmdLen = int(bytes_HexaToNro(sCmdLen))
         sReturn = sReturn + str_GetENTER() + str_GetENTER() + "Command " + str(nCmd) + " length: 0x" + sCmdLen + " - Decimal: " + str(nCmdLen) + " bytes."
         n = n + 2

         sFile = str_mid(sData, n, (nCmdLen * 2))
         sReturn = sReturn + str_GetENTER() + "Command " + str(nCmd) + " - Select ADF - Application Dedicated File: " + str_AddSpaceHexa(sFile)
         n = n + (nCmdLen * 2)

      if not bFound:
         n = n + 2

   if sReturn != "":
      sReturn = sReturn + str_GetENTER()

   return sReturn, bUpdFile

# SAPCmd_InterpretSMSData -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCmd_InterpretSMS_APDU_Data(sData, sAPDU=""):
   sReturn = ""

   #print("SAPCmd_InterpretSMS_APDU_Data - sData: " + str(sData))
   #print("SAPCmd_InterpretSMS_APDU_Data - sAPDU: " + str(sAPDU))

   sCmdAPDU = ""
   sCmdAPDUSMPP = ""
   sCmdWithCampaignIDAPDU = ""
   if sAPDU != "":
      if str_left(sAPDU, 1) == "8":
         #IT IS AN APDU FROM SDK STARTING WITH 0x8X for example 0x80 with channel 0.
         sCmdAPDU = str_mid(sAPDU, 2, 2)
      else:
         #IT IS A SMPP
         sCmdAPDUSMPP = str_left(sAPDU, 2)   
         nTemp = bytes_HexaToNro(sCmdAPDUSMPP)
         if nTemp <= bytes_HexaToNro("7F"):
            #THERE IS THE CAMPAIGN ID FOR APDU IN SMPP
            sCmdWithCampaignIDAPDU = str_left(sAPDU, 4)   
            sCmdAPDUSMPP = str_mid(sAPDU, 4, 2)

      #print("SAPCmd_InterpretSMS_APDU_Data - sCmdAPDU: " + str(sCmdAPDU) + " - sCmdWithCampaignID: " + str(sCmdWithCampaignID))

   tData = sData.split(sSimcard_SendSMSDATAPattern)
   if sSimcard_SendSMSDATAPattern in sData:
      n = 1
   else:
      n = 0

   #print("SAPCmd_InterpretSMS_APDU_Data - tData: " + str(tData))

   while n < len(tData):

      sTemp = str_SpacesOut(tData[n])
      if str_left(sTemp, 2).upper() == "0x":
         sTemp = str_midToEnd(sTemp, 2)

      sTemp = str_getSubStringFromOcur(sTemp.upper(), "-length".upper(), 0)

      #print("SAPCmd_InterpretSMSData - sTemp 1: " + str(sTemp))

      if sTemp != "":
         #sReturn = sReturn + str_GetENTER() + "SMS Data " + str(n) + ": 0x" + sTemp
         #print(sReturn)

         #ANALYSIS FOR COMMAND INTERPRETATION WHEN THERE IS THE CASE
         sCmdInterpret = ""
         sCmd = str_left(sTemp, 2)

         #POSSIBLE CAMPAIGN ID FOR SMS COMMAND
         sCmdWithCampaignID = str_mid(sTemp, 4, 2)

         sCmdWithCampaignIDRef = ""

         bProcessed = False

         sTag = "C0"
         if not bProcessed and (sCmd == sTag or sCmdWithCampaignID == sTag or sCmdAPDU == sTag):
            # Interpret command C0 for getting Terminal Profile.

            if sCmdWithCampaignID == sTag:
               sCmdWithCampaignIDRef = str_left(sTemp, 4)
               sTemp = str_midToEnd(sTemp, 4)

            sCmdInterpret = SAPCmdC0_Interpret(sTemp)
            bProcessed = True

         sTag = "C1"
         if not bProcessed and (sCmd == sTag or sCmdWithCampaignID == sTag or sCmdAPDU == sTag):
            # Interpret command C1 for getting/setting polling interval.

            if sCmdWithCampaignID == sTag:
               sCmdWithCampaignIDRef = str_left(sTemp, 4)
               sTemp = str_midToEnd(sTemp, 4)

            sCmdInterpret, nPollingInterval, sStatusSettingPollingInterval = SAPCmdC1_Interpret(sTemp)
            bProcessed = True

         sTag = "D4"
         if not bProcessed and (sCmd == sTag or sCmdWithCampaignID == sTag or sCmdAPDU == sTag):
            # Interpret command D4 for analyzing ICCID, IMSI, etc.

            if sCmdWithCampaignID == sTag:
               sCmdWithCampaignIDRef = str_left(sTemp, 4)
               sTemp = str_midToEnd(sTemp, 4)

            sCmdInterpret = SAPCmdD4_Interpret(sTemp)
            bProcessed = True

         sTag = "DE"
         if not bProcessed and (sCmd == sTag or sCmdWithCampaignID == sTag or sCmdAPDU == sTag):
            # Interpret command DE for repetitions

            if sCmdWithCampaignID == sTag:
               sCmdWithCampaignIDRef = str_left(sTemp, 4)
               sTemp = str_midToEnd(sTemp, 4)

            if sCmdAPDU!= "":
               #IT IS AN APDU FROM SDK
               sTemp = sCmdAPDU + sTemp

            sCmdInterpret, sRepeatTimes, sRepeatTimesExec, sRepeatStatusCommands, sRepeatStatusCommandsExec, sRepeatSendSMSNot, sRepeatCmd = SAPCmdDE_Interpret(sTemp)
            bProcessed = True

         sTag = "DD"
         if not bProcessed and (sCmd == sTag or sCmdWithCampaignID == sTag or sCmdAPDU == sTag):
            # Interpret command DD for last calls sent

            if sCmdWithCampaignID == sTag:
               sCmdWithCampaignIDRef = str_left(sTemp, 4)
               sTemp = str_midToEnd(sTemp, 4)

            if sCmdAPDU!= "":
               #IT IS AN APDU FROM SDK
               sTemp = sCmdAPDU + sTemp

            sCmdInterpret, tMSISDNs = SAPCmdDD_Interpret(sTemp)
            bProcessed = True

         sTag = "DF"
         if sCmd == sTag or sCmdWithCampaignID == sTag or sCmdAPDU == sTag or sCmdAPDUSMPP == sTag:
            # Interpret command DF for managing files
            
            if sCmdWithCampaignID == sTag:
               sCmdWithCampaignIDRef = str_left(sTemp, 4)
               sTemp = str_midToEnd(sTemp, 4)

            if sCmdAPDU!= "":
               #IT IS AN APDU FROM SDK
               sTemp = sCmdAPDU + sTemp

            #print("SAPCmd_InterpretSMSData - sTemp: " + str(sTemp))

            sCmdInterpret = SAPCmdDF_Interpret(sTemp)
            bProcessed = True

         sTag = "F7"
         if not bProcessed and (sCmd == sTag or sCmdWithCampaignID == sTag or sCmdAPDU == sTag):
            # Interpret command F7 for SMS sent

            if sCmdWithCampaignID == sTag:
               sCmdWithCampaignIDRef = str_left(sTemp, 4)
               sTemp = str_midToEnd(sTemp, 4)

            if sCmdAPDU!= "":
               #IT IS AN APDU FROM SDK
               sTemp = sCmdAPDU + sTemp

            sCmdInterpret = SAPCmdF7_Interpret(sTemp)
            bProcessed = True

         sTag = "FB"
         sTag2 = "F8"
         if not bProcessed and (sCmd == sTag or sCmdWithCampaignID == sTag or sCmdAPDU == sTag or sCmd == sTag2 or sCmdWithCampaignID == sTag2 or sCmdAPDU == sTag2 or sCmdAPDUSMPP == sTag or sCmdAPDUSMPP == sTag2):
            # Interpret command FB and F8 the same as autoprovisioning

            if (sCmdWithCampaignID == sTag or sCmdWithCampaignID == sTag2) or sCmdWithCampaignIDAPDU != "":
               sCmdWithCampaignIDRef = str_left(sTemp, 4)
               sTemp = str_midToEnd(sTemp, 4)

            #print("FB - sTemp = " + str(sTemp) + " - sCmdWithCampaignID = " + str(sCmdWithCampaignID))
            sCmdInterpret = simcard_processSMSData_AutoProvisioningGetDesOnly(sTemp)
            #print("FB - sCmdInterpret = " + str(sCmdInterpret))

            bProcessed = True

         #if not bProcessed and (sCmd == "FC" or sCmdWithCampaignID == "FC" or sCmd == "DC" or sCmdWithCampaignID == "DC"):
         #   # Interpret command DC or FC for SDK management
         #   sCmdInterpret = COTA_processCmd_FC_DC(sTemp)
         #   bProcessed = True


         if sCmdInterpret != "":

            if n > 1:
               sReturn = sReturn + str_GetENTER()

            #sReturn = sReturn + str_GetENTER() + "Process Data " + str(n) + ": 0x" + str_AddSpaceHexa(sTemp)
            sReturn = sReturn + str_GetENTER() + "Process Data " + str(n) + ": " 

            if sCmdWithCampaignIDRef != "":
               sReturn = sReturn + str_GetENTER() + "Campaign ID: 0x" + str_AddSpaceHexa(sCmdWithCampaignIDRef) + " - Decimal: " + str(bytes_HexaToNro(sCmdWithCampaignIDRef))
            
            sReturn = sReturn + str_GetENTER() + sCmdInterpret

      n = n + 1
   
   return sReturn

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
