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
           "D9" : "Change DEFAULT URL Of DisplayText"
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
sCOTA = "COTA"
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
    sReturn = ""
    
    n = 0 
    nLen = len(sURL)
    
    #print("COTAURLSpecialChars. URL: " + sURL)
      
    #https://www.w3schools.com/tags/ref_urlencode.ASP
    sPorcentage = "%"
   
    while n < nLen:
          sChar = str_mid(sURL, n, 1)
          sCharCh = sPorcentage
          sCharCh = ""
          
          if sChar == " ":
             sCharCh = "20"
             
          #if sChar == "!":
          #   sCharCh = "21"
             
          if sChar == str_GetComillaDoble():
             sCharCh = "22"
             
          #if sChar == "#":
          #   sCharCh = "23"
             
          #if sChar == "$":
          #   sCharCh = "24"
             
          #if sChar == "%":
          #   sCharCh = "25"
             
          #if sChar == "&":
          #   sCharCh = "26"
             
          if sChar == "'":
             sCharCh = "27"
             
          if sChar == "(":
             sCharCh = "28"
             
          if sChar == ")":
             sCharCh = "29"
             
          if sChar == "*":
             sCharCh = "2A"
             
          if sChar == "*":
             sCharCh = "2A"
             
          if sChar == "+":
             sCharCh = "2B"
             
          if sChar == str_GetComillaItalic():
             sCharCh = "2C"
             
          if sChar == "-":
             sCharCh = "2D"
             
          #if sChar == ".":
          #   sCharCh = "2E"
             
          #if sChar == "/":
          #   sCharCh = "2F"
             
          #if sChar == ":":
          #   sCharCh = "3A"
             
          #if sChar == ";":
          #   sCharCh = "3B"
             
          if sChar == "<":
             sCharCh = "3C"
             
          #if sChar == "=":
          #   sCharCh = "3D"
             
          if sChar == ">":
             sCharCh = "3E"
             
          #if sChar == "?":
          #   sCharCh = "3F"
             
          if sChar == "@":
             sCharCh = "40"
             
          if sChar == "[":
             sCharCh = "5B"
             
          if sChar == "]":
             sCharCh = "5D"
             
          if sChar == "^":
             sCharCh = "5E"
             
          if sChar == "_":
             sCharCh = "5F"
             
          if sChar == "{":
             sCharCh = "7B"
             
          if sChar == "|":
             sCharCh = "7C"
             
          if sChar == "}":
             sCharCh = "7D"
             
          if sChar == "~":
             sCharCh = "7E"

          if sCharCh != "":
            sChar = sPorcentage + sCharCh
        
          sReturn = sReturn + sChar
        
          n = n + 1

    #print("COTAURLSpecialChars. URL return: " + sReturn)
    return sReturn

		
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
                              'F1F0', 'F2F0', 'UCS2', 'PopUpRetries',"AutoPopUpbyIMEI","CampaignID","F6","D4","D6", "D7", "D8", "D9"]
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
                                "D4", "D5", "D6", "D7", "FULL", "F7", "D8", "D9"]
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
    sCOTA = "COTA"
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
        log_write_ErrorInRed(
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
        sys.exit()

# COTACmd_sendEnvelope_ResponseFirstByteCommand ---------------------------------------------------------------------------------------------------------------------------------------------------------
def COTACmd_sendEnvelope_ResponseFirstByteCommand(cardservice, sLogFileName, sCmd, sTPDAParam, sAPDU, sTAR="43 50 41", bNetworkOKOrChangeIMEIOrChangeMCCMNC=True, sMCC="", sMNC=""):
    return simcardCmd_sendEnvelope_ResponseFirstByteCommand(cardservice, sLogFileName, sCmd, sTPDAParam, sAPDU, sTAR, bNetworkOKOrChangeIMEIOrChangeMCCMNC, sMCC, sMNC)
         
# COTACmd_sendEnvelopeConcat -----------------------------------------------------------------------------------------------------------------------------------------------
def COTACmd_sendEnvelopeConcat(cardservice, sLogFileName, sTPDAParam , sCMD):
    sReturn, sReturnDes = simcardCmd_sendEnvelopeConcat(cardservice, sLogFileName, sCMD, sTPDAParam)
    return sReturn

        
# SAPCmdF7_Interpret -----------------------------------------------------------------------------------------------------------------------------------------------
def SAPCmdF7_Interpret(sData, sTPDA=""):
    
    sDataT = str_SpacesOut(sData).upper()
    sTPDA = str_SpacesOut(sTPDA).upper()
    
    sCmd = "F7"
    
    sReturn = "Data in hexadecimal: 0x" +  str_AddSpaceHexa(sData) 

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

    n = 0
    sTemp = str_left(sDataT, 2)
    #print("sTemp: " + sTemp)
    n = n + 2	
    if sTemp == sCmd:
       sReturn = sReturn + str_GetENTER() + "Command " + sCmd + " received OK."     
    else:
       #This is because APK called. The command "F7" is not in the data returned.
       n = 0   
    
    #Next byte is length
    sCmdLenTotal = str_mid(sDataT, n, 2)
    nCmdLenTotal = int(bytes_HexaToNro(sCmdLenTotal))
    sReturn = sReturn + str_GetENTER() + "Total Command length: 0x" + sCmdLenTotal + " - Decimal: " + str(nCmdLenTotal) + " bytes."
    if nCmdLenTotal == 0:
       sReturn = sReturn + " - Applet SMS buffer is empty, cleanned."
    n = n + 2

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
          
          sCOTA = bytes_StrToHexa("COTA")
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

    if str_instrBool(sAscii.upper(), sCOTA):
        # GET COTA VERSION
        sCOTAVer = str_getSubStringFromOcur(sAscii.upper(), sCOTA, 1)

        # GET DATA BEFORE COTA VERSION
        # print("sHex: " + sHex)
        # print("bytes_StrToHexa(sCOTA): " + bytes_StrToHexa(sCOTA))
        sIMEIHex = str_getSubStringFromOcur(sHex, bytes_StrToHexa(sCOTA).upper(), 0)
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
        sReturn = sReturn + sCOTA + " version: " + sCOTAVer + sSepara
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

    return sReturn