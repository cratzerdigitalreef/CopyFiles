#! /usr/bin/env python3
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
#sys.path.append(parent_directory+"/libs")
sys.path.append(parent_directory+"/libs")

from bytes import *
from simcard import *
from loci import *

from log import *

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.Exceptions import CardRequestTimeoutException


# define the apdus used in this script
# apk_sha1_process_aram ------------------------------------------------------------------------------------------------
def apk_sha1_process_aram(cardservice, channel, sLogFileName, sSHA1):
    
    sSHA1 = str_TrimCleanSpaces(sSHA1)
    
    sLog = "apk_Connect - Channel value: " + channel
    log_write(sLogFileName, sLog)

    bReturn = True
    bReturnSHA1 = False
    
    if channel == "" or channel == "False":
       bReturn = False
   
    if bReturn:
       sResAndSW1SW2 = simcard_Select_ARAM_GetDataSHA1s(cardservice, sLogFileName, channel)
       #print("apk_Connect - sResAndSW1SW2: " + sResAndSW1SW2)
    
       bReturnSHA1 = apk_processSHA1(sLogFileName, sResAndSW1SW2, sSHA1)
       #print("apk_Connect - bReturnSHA1: " + str(bReturnSHA1) + ". Channel: " + sChannel)
    
    sLog = "CALL ARA-M AND ANALYZE SHA-1 - Channel value: " + str(channel)
    log_write(sLogFileName, sLog)
       
    sLog = str_RepeatString(10, "*")
    sLog = sLog + " - ENDED"
    
    if bReturn==False:
       sLog = sLog + " NOT"

    sLog = sLog + " OK"
    sLog = sLog + " " + str_RepeatString(10, "*")
    log_write(sLogFileName, sLog)

    sLog = str_RepeatString(100, "-")
    log_write(sLogFileName, sLog + "\n")
    
    if bReturnSHA1 == True:
       return True
       
    return False


# apk_Connect -----------------------------------------------------------------------------------------------------------
def apk_Connect(cardservice, sLogFileName, sSHA1):
    
    sSHA1 = str_TrimCleanSpaces(sSHA1)
    
    sChannel = simcard_OpenChannel(cardservice, sLogFileName)
    sLog = "apk_Connect - Channel value: " + sChannel
    log_write(sLogFileName, sLog)

    bReturn = True
    bReturnSHA1 = False
    
    if sChannel == "" or sChannel == "False":
       bReturn = False
   
    if bReturn:
       sResAndSW1SW2 = simcard_Select_ARAM_GetDataSHA1s(cardservice, sLogFileName, sChannel)
       #print("apk_Connect - sResAndSW1SW2: " + sResAndSW1SW2)
    
       bReturnSHA1 = apk_processSHA1(sLogFileName, sResAndSW1SW2, sSHA1)
       #print("apk_Connect - bReturnSHA1: " + str(bReturnSHA1) + ". Channel: " + sChannel)
    
    sLog = "CALL ARA-M AND ANALYZE SHA-1 - Channel value: " + str(sChannel)
    log_write(sLogFileName, sLog)
       
    sLog = str_RepeatString(10, "*")
    sLog = sLog + " - ENDED"
    
    if bReturn==False:
       sLog = sLog + " NOT"

    sLog = sLog + " OK"
    sLog = sLog + " " + str_RepeatString(10, "*")
    log_write(sLogFileName, sLog)

    sLog = str_RepeatString(100, "-")
    log_write(sLogFileName, sLog + "\n")
    
    if bReturnSHA1 == True:
       return sChannel
       
    return False

# apk_processSHA1 -----------------------------------------------------------------------------------------------------------
def apk_processSHA1(sLogFileName, sRes, sSHA1):
    
#9000 Normal processing
#   Data Object, Tag = ' FF40 ', Length =  104
#      Data Object, Tag = ' E2 ', Length =  24
#         Data Object, Tag = ' E1 ', Length =  22
#            Data Object, Tag = ' C1 ', Length =  20
#               Data 'F4 65 3B EE 3D 83 F5 EF E1 89 60 B5 35 94 43 8E B1 E3 B2 99'
#      Data Object, Tag = ' E2 ', Length =  24
#         Data Object, Tag = ' E1 ', Length =  22
#            Data Object, Tag = ' C1 ', Length =  20
#               Data 'DA 5C 07 3B A0 77 FD 86 B7 CB 42 34 33 1D E5 FC C4 49 F4 60'
#      Data Object, Tag = ' E2 ', Length =  24
#         Data Object, Tag = ' E1 ', Length =  22
#            Data Object, Tag = ' C1 ', Length =  20
#               Data '79 B1 75 84 41 44 F5 FC 97 3C 34 23 6C 44 8A ED 36 D4 7F 46'
#      Data Object, Tag = ' E2 ', Length =  24
#         Data Object, Tag = ' E1 ', Length =  22
#            Data Object, Tag = ' C1 ', Length =  20
#               Data '00 11 22 33 44 55 66 77 00 11 22 33 44 55 66 77 00 11 22 33'
#Response
#   Response Data FF 40 68 E2 18 E1 16 C1 14 F4 65 3B EE 3D 83 F5 
#                 EF E1 89 60 B5 35 94 43 8E B1 E3 B2 99 E2 18 E1 
#                 16 C1 14 DA 5C 07 3B A0 77 FD 86 B7 CB 42 34 33 
#                 1D E5 FC C4 49 F4 60 E2 18 E1 16 C1 14 79 B1 75 
#                 84 41 44 F5 FC 97 3C 34 23 6C 44 8A ED 36 D4 7F 
#                 46 E2 18 E1 16 C1 14 00 11 22 33 44 55 66 77 00 
#                 11 22 33 44 55 66 77 00 11 22 33
#   Status Word 90 00

       sRes = str_SpacesOut(sRes)
       sData = sRes
       n = 4
       sLog = "Data Object, Tag = 0x" + str_left(sData, n)
       if str_mid(sData, n, 2) == "81":
          #LONG TEXT
          n = n + 2
       
       sLen =  str_mid(sData, n, 2)
       n = n + 2
       sLog = sLog + ", Length = 0x" + str(sLen) + " - Decimal: " + str(bytes_HexaToNro(sLen))
      
       #TAG E2
       sLog = sLog + "\nData Object, Tag = 0x" + str_mid(sData, n, 2)
       n = n + 2
       sLen =  str_mid(sData, n, 2)
       n = n + 2
       sLog = sLog + ", Length = 0x" + str(sLen) + " - Decimal: " + str(bytes_HexaToNro(sLen))
      
       #TAG E1
       sLog = sLog + "\nData Object, Tag = 0x" + str_mid(sData, n, 2)
       n = n + 2
       sLen =  str_mid(sData, n, 2)
       n = n + 2
       sLog = sLog + ", Length = 0x" + str(sLen) + " - Decimal: " + str(bytes_HexaToNro(sLen))
      
       #TAG C1
       sLog = sLog + "\nData Object, Tag = 0x" + str_mid(sData, n, 2)
       n = n + 2
       sLen =  str_mid(sData, n, 2)
       sLog = sLog + " Length = 0x" + str(sLen) + " - Decimal: " + str(bytes_HexaToNro(sLen))

       
       log_write(sLogFileName, sLog)
       
       sTagDataObject = "C1"
       nOcur = 1
       sData = str_getSubStringFromOcur(sRes, sTagDataObject, nOcur)
       #print("sData nOcur=" + str(nOcur) + ": " + sData)

       sSHA1Found = ""
       nSHA1Found = 0
       bReturn = False
       bFound = False
       #while sData != "" and bReturn==False:
       bOut = False
       while sData != "" and bOut==False:
             
             sLen = str_left(sData, 2)
             nLen = bytes_HexaToNro(sLen)
             #print("nLen: " + str(nLen))
             
             nLen = int(nLen)
             nLen = nLen * 2
             sSHA1Data = str_mid(sData, 2, nLen)
             
             log_write(sLogFileName, "SHA-1 in the applet COTA/SAP: '" + sSHA1Data + ". Reference from Response: " + str(nOcur))
             
             if sSHA1Data == "":
                return False
             else:
                sLog = "SHA-1 in the applet COTA/SAP: '" + sSHA1Data + "' is"
                if sSHA1Data == sSHA1:
                   # SHA-1 IS IN DATA RETRIEVED FROM APPLET COTA
                   bFound = True
                else:
                   sLog = sLog + " NOT"
                sLog = sLog + " the same to the one for comparison: '" + sSHA1 + "'."  
                if bFound:
                   sLog = "*** GREAT !!! It was found in reference: " + str(nOcur) + " *** " + sLog 
                   sSHA1Found = sSHA1Found + "\n" + sLog
                   nSHA1Found = nSHA1Found + 1
                log_write(sLogFileName, sLog)
                bFound = False
                
             #if bReturn == False:
             nOcur = nOcur + 1
             sData = str_getSubStringFromOcur(sRes, sTagDataObject, nOcur)

             if len(sData) < int(nLen):
                bOut = True
             else: 
                sLog = "Data Object, Tag = 0x" + sTagDataObject
                sLen = str_left(sData, 2)
                sLog = sLog + " Length = 0x" + str(sLen) + " - Decimal: " + str(bytes_HexaToNro(sLen))
                log_write(sLogFileName, sLog)

       
       sLog = "\nSHA-1 = '" + str_AddSpaceHexa(sSHA1) + "'"
       
       if nSHA1Found > 0 and sSHA1Found!="":
          bReturn = True
          sLog = sLog + " - Total SHA-1 found in the applet the same as SHA-1 as parameter = " + str(nSHA1Found) + ". Details: \n" + sSHA1Found
       else:
          sLog = sLog + " NOT found in the applet."
          
       sLog = sLog + "\n\nTotal SHA-1 defined in the applet = " + str(nOcur-1) + ".\n\n"
       
       if bReturn:
          log_write_OKInGreen(sLogFileName, sLog)
       else:
          log_write_WarningInYellow(sLogFileName, sLog)
       
       return bReturn

# apk_APDU_FC -----------------------------------------------------------------------------------------------------------
def apk_APDU_FC(cardservice, sLogFileName, sChannel, sP2, sSDKID):
    
   #Command '82 02 FC AA 00'
   #Class '82'
   #Instruction '02'
   #P1 'FC'
   #P2 'AA'
   #Le '00'

   sAPDU = " 02 FC " + sP2
   if sSDKID != "":
      sLen = len(sSDKID)
      sLenHexa = bytes_NroToHexa(sLen)
      sSDKIDHexa = bytes_StrToHexa(sSDKID).upper()
      sAPDU = sAPDU + sLenHexa + sSDKIDHexa
      #print("sSDKIDHexa: " + sSDKIDHexa + " - LenHexa: " + sLenHexa)
      
   sLog = "APDU to be sent from APK to Applet COTA/SAP: 0x" + str_SpaceHexa(sAPDU)
   log_write(sLogFileName, sLog)
      
   sResAndSW1SW2 = apk_APDU(cardservice, sLogFileName, sChannel, sAPDU, "apk_APDU_FC")
   sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
   sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

   sLog = "APDU Sent from APK to Applet COTA/SAP: " + simcard_DataResponseDesHexaAndASCII(sResAndSW1SW2, True)
   sLog = sLog + ". Response: " + sResAndSW1SW2
   log_write(sLogFileName, sLog)

   bReturn = False
   if sSW1 == '90' and sSW2 == '00':
      bReturn = True
         
   return bReturn
 
   
# apk_APDU_FA -----------------------------------------------------------------------------------------------------------
def apk_APDU_FA(cardservice, sLogFileName, sChannel, sMSISDN=""):
    
   sDes = "apk_APDU_FA"
   
   sAPDU = " FA 00 00"
   
   sMSISDNHexa = ""
   if sMSISDN!="":
      sMSISDNHexa = bytes_StrToHexa(sMSISDN)
      #print("sMSISDNHexa: " + sMSISDNHexa)
      sMSISDNHexaLen = bytes_NroToHexa(len(sMSISDN))
      #print("sMSISDNHexaLen: " + sMSISDNHexaLen)
      
   if sMSISDNHexa!="":
      sAPDU = sAPDU + sMSISDNHexaLen + sMSISDNHexa
      sDes = sDes + "_MSISDN_" + sMSISDN
   
   sResAndSW1SW2 = apk_APDU(cardservice, sLogFileName, sChannel, sAPDU, sDes)
   sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
   sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

   if len(sResAndSW1SW2) > 8:
      #print("sResAndSW1SW2: " + sResAndSW1SW2)
      nA = 2
      n = 0
      sVal = str_mid(sResAndSW1SW2, n, nA) 
      sResponse = "MSISDN Length Data: 0x" + sVal + " - NRO: " + bytes_HexaToNro(sVal)
      nA = int(bytes_HexaToNro(sVal)) * 2
      n = n + 2
      sVal = str_mid(sResAndSW1SW2, n, nA) 
      sMSISDNResponse = bytes_HexaToASCII(sVal)
      sResponse = sResponse + str_GetENTER() + "MSISDN Data: 0x" + sVal + " - ASCII: " +  sMSISDNResponse
      log_write_OKInGreen(sLogFileName, sResponse)
      if sMSISDN!="":
         if sMSISDNResponse == sMSISDN:
            log_write_OKInGreen(sLogFileName, "MSISDN received " + sMSISDNResponse + " is the same as the one sent: " + sMSISDN)
         else:   
            log_write_ErrorInRed(sLogFileName, "MSISDN received " + sMSISDNResponse + " is NOT the same as the one sent: " + sMSISDN)
       
   bReturn = False
   if sSW1 == '90' and sSW2 == '00':
      bReturn = True
         
   return bReturn
 
# apk_APDU -----------------------------------------------------------------------------------------------------------
def apk_APDU(cardservice, sLogFileName, sChannel, sAPDU, sDes):
    
   #Command '82 02 FC AA 00'
   #Class '82'
   #Instruction '02'
   #P1 'FC'
   #P2 'AA'
   #Le '00'

   sCLA = simcard_ARAM_CLA(sChannel)
   if (len(sAPDU) > 6):
      sAPDU = sCLA + sAPDU[2:]
   else:
      sAPDU = sCLA + sAPDU
         
   sLog = "APDU "
   if sDes != "":
      sLog = sLog + "for " + sDes + " " 
   sLog = sLog + "to be sent from APK to Applet COTA/SAP: 0x" + str_SpaceHexa(sAPDU)
   sAPDUASCII = bytes_HexaToASCII(sAPDU)
   if sAPDUASCII != "":
      sLog = sLog + " - ASCII: " + bytes_HexaToASCII(sAPDU) 
   print(sLog)
   
   log_write_InfoInBlue(sLogFileName, sLog)
      
   sResAndSW1SW2 = simcard_Select_ARAM_SendAPDU(cardservice, sLogFileName, sChannel, sAPDU)
   sLog = "APDU Response from Applet COTA/SAP to APK: " + simcard_DataResponseDesHexaAndASCII(sResAndSW1SW2, True)
   log_write_InfoInBlue(sLogFileName, sLog)

   return sResAndSW1SW2
   

# apk_APDU_F8 -----------------------------------------------------------------------------------------------------------
def apk_APDU_F8(cardservice, sLogFileName, sChannel):
    
   #Command '82 02 FC AA 00'
   #Class '82'
   #Instruction '02'
   #P1 'FC'
   #P2 'AA'
   #Le '00'

   bReturn = True
   sAPDU = "F8 00 00"
   
   sResAndSW1SW2 = apk_APDU(cardservice, sLogFileName, sChannel, sAPDU, "apk_APDU_F8")
   sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
   sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
   
   nIMEILen = 16
   sIMEI = str_left(sResAndSW1SW2, nIMEILen)
   sCOTA = str_mid(sResAndSW1SW2, nIMEILen, len(sResAndSW1SW2) - nIMEILen)
   sLog = "IMEI: " + sIMEI + ". COTA VER: " + sCOTA + " - ASCII: " + bytes_HexaToASCII(sCOTA)
   log_write(sLogFileName, sLog)
   sLog = loci_imeiFromHexa(sIMEI, True)
   log_write(sLogFileName, sLog)
   
   return bReturn

# apk_APDU_FE -----------------------------------------------------------------------------------------------------------
def apk_APDU_FE(cardservice, sLogFileName, sChannel):
    
   #Command '82 02 FC AA 00'
   #Class '82'
   #Instruction '02'
   #P1 'FC'
   #P2 'AA'
   #Le '00'

   bReturn = True
   sAPDU = "FE 00 00"
   
   sResAndSW1SW2 = apk_APDU(cardservice, sLogFileName, sChannel, sAPDU, "apk_APDU_FE")
   sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
   sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

   nLOCILen = 18
   sLOCI = str_left(sResAndSW1SW2, nLOCILen)
   if sLOCI == "6E00":
       return False
   sCOTA = str_mid(sResAndSW1SW2, nLOCILen, len(sResAndSW1SW2) - nLOCILen)
   sLog = "LOCI: " + sLOCI + ". COTA VER: " + sCOTA + " - ASCII: " + bytes_HexaToASCII(sCOTA)
   log_write(sLogFileName, sLog)

   sLog = loci_lociFromHexa(sLOCI, True)
   log_write(sLogFileName, sLog)

   return bReturn

# apk_APDU_E2 -----------------------------------------------------------------------------------------------------------
def apk_APDU_D1(cardservice, sLogFileName, sChannel, sSDKID):
    return apk_APDU_E2(cardservice, sLogFileName, sChannel, sSDKID)
    
def apk_APDU_E2(cardservice, sLogFileName, sChannel, sSDKID):
    
   #Command '82 D1 00 00'
   #Class '82'
   #Instruction 'D1'
   #P1 '00'
   #P2 '00'
   #Le '00'

   sAPDU = "D1 00 00" 
   if sSDKID != "":
      sLen = len(sSDKID)
      sLenHexa = bytes_NroToHexa(sLen)
      sSDKIDHexa = bytes_StrToHexa(sSDKID).upper()
      sAPDU = sAPDU + sLenHexa + sSDKIDHexa
      #print("sSDKIDHexa: " + sSDKIDHexa + " - LenHexa: " + sLenHexa)
      
   sLog = "APDU to be sent from APK to Applet COTA/SAP: 0x" + str_SpaceHexa(sAPDU)
   log_write(sLogFileName, sLog)
      
   sResAndSW1SW2 = apk_APDU(cardservice, sLogFileName, sChannel, sAPDU, "apk_APDU_D1")
   sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
   sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

   sLog = "APDU Sent from APK to Applet COTA/SAP: " + simcard_DataResponseDesHexaAndASCII(sResAndSW1SW2, True)
   sLog = sLog + ". Response: " + sResAndSW1SW2
   log_write(sLogFileName, sLog)

   bReturn = False
   if sSW1 == '90' and sSW2 == '00':
      bReturn = True
       
   return bReturn
 
# apk_StatusCommands -----------------------------------------------------------------------------------------------------------
def apk_StatusCommands(cardservice, sLogFileName, sSTATUSCOMMAND_MAX):
    tReturn = apk_StatusCommandsGetLastCommandProcess(cardservice, sLogFileName, sSTATUSCOMMAND_MAX, str_GetENTER())
    return tReturn[0]

# apk_StatusCommandsGetLastCommand -----------------------------------------------------------------------------------------------------------
def apk_StatusCommandsGetLastCommand(cardservice, sLogFileName, sSTATUSCOMMAND_MAX, sSeparaAPDU):
    tReturn = apk_StatusCommandsGetLastCommandProcess(cardservice, sLogFileName, sSTATUSCOMMAND_MAX, sSeparaAPDU)
    return tReturn[1]
    
# apk_StatusCommandsGetLastCommandProcess -----------------------------------------------------------------------------------------------------------
def apk_StatusCommandsGetLastCommandProcess(cardservice, sLogFileName, sSTATUSCOMMAND_MAX, sSeparaAPDU):
    return simcard_StatusCommandsGetLastCommandProcess(cardservice, sLogFileName, sSTATUSCOMMAND_MAX, sSeparaAPDU)

# apk_APDU_D6_LaunchBrowser -----------------------------------------------------------------------------------------------------------
def apk_APDU_D6_LaunchBrowser(cardservice, sLogFileName, sChannel):
    
   #Command '80 D6 00 00 1A 01 01 F4 16 68 74 74 70 73 3A 2F 2F 77 77 77 2E 67 6F 6F 67 6C 65 2E 63 6F 6D
   #Class '80'
   #Instruction 'D6'
   #P1 '00'
   #P2 '00'
   #Len '1A'
   #APDU FOR D6 '01 01 F4 16 68 74 74 70 73 3A 2F 2F 77 77 77 2E 67 6F 6F 67 6C 65 2E 63 6F 6D'

   #Send APDU for:
   #- Launch Browser, F4 command. URL: www.google.com

   bReturn = True
   #sAPDU = "D6 00 00 1A 01 01 F4 16 68 74 74 70 73 3A 2F 2F 77 77 77 2E 67 6F 6F 67 6C 65 2E 63 6F 6D"
   sAPDU = "D6 00 00 1D 01 01 D4 01 01 F4 16 68 74 74 70 73 3A 2F 2F 77 77 77 2E 67 6F 6F 67 6C 65 2E 63 6F 6D"
   #sAPDU = "D6 00 00 03 01 01 D4"
   
   sResAndSW1SW2 = apk_APDU(cardservice, sLogFileName, sChannel, sAPDU, "apk_APDU_D6")
   sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
   sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
   
   sLog = "APDU to be sent from APK to Applet COTA/SAP: 0x" + str_SpaceHexa(sAPDU)
   log_write(sLogFileName, sLog)
      
   sLog = "APDU Sent from APK to Applet COTA/SAP: " + simcard_DataResponseDesHexaAndASCII(sResAndSW1SW2, True)
   sLog = sLog + ". Response: " + sResAndSW1SW2
   log_write(sLogFileName, sLog)

   bReturn = False
   if sSW1 == '90' and sSW2 == '00':
      bReturn = True
       
   return bReturn

# apk_APDU_D6_PopUp -----------------------------------------------------------------------------------------------------------
def apk_APDU_D6_PopUp(cardservice, sLogFileName, sChannel):
    
   #Command '80 D6 00 00 9B F1 F0 08 81 96 00 54 00 65 00 73 00 74 00 20 00 44 00 36 00 3A 00 20 00 42 00 69 00 65 00 6E 00 76 00 65 00 6E 00 69 00 64 00 6F 00 2E 00 20 00 44 00 69 00 73 00 66 00 72 00 75 00 74 00 61 00 20 00 6C 00 6F 00 73 00 20 00 6E 00 75 00 65 00 76 00 6F 00 73 00 20 00 73 00 65 00 72 00 76 00 69 00 63 00 69 00 6F 00 73 00 20 00 79 00 20 00 70 00 72 00 6F 00 6D 00 6F 00 63 00 69 00 6F 00 6E 00 65 00 73 00 20 00 70 00 61 00 72 00 61 00 20 00 74 00 69 00 20 00 20 27 28
   #Class '80'
   #Instruction 'D6'
   #P1 '00'
   #P2 '00'
   #Len '9C'
   #APDU FOR D6 'F1 F0 08 81 96 00 54 00 65 00 73 00 74 00 20 00 44 00 36 00 3A 00 20 00 42 00 69 00 65 00 6E 00 76 00 65 00 6E 00 69 00 64 00 6F 00 2E 00 20 00 44 00 69 00 73 00 66 00 72 00 75 00 74 00 61 00 20 00 6C 00 6F 00 73 00 20 00 6E 00 75 00 65 00 76 00 6F 00 73 00 20 00 73 00 65 00 72 00 76 00 69 00 63 00 69 00 6F 00 73 00 20 00 79 00 20 00 70 00 72 00 6F 00 6D 00 6F 00 63 00 69 00 6F 00 6E 00 65 00 73 00 20 00 70 00 61 00 72 00 61 00 20 00 74 00 69 00 20 00 20 27 28

   #Send APDU for:
   #- Update Welcome Text and Call PopUp.   #Send APDU for:

   bReturn = True
   sAPDU = "D6 00 00 9b F1 F0 08 81 96 00 54 00 65 00 73 00 74 00 20 00 44 00 36 00 3A 00 20 00 42 00 69 00 65 00 6E 00 76 00 65 00 6E 00 69 00 64 00 6F 00 2E 00 20 00 44 00 69 00 73 00 66 00 72 00 75 00 74 00 61 00 20 00 6C 00 6F 00 73 00 20 00 6E 00 75 00 65 00 76 00 6F 00 73 00 20 00 73 00 65 00 72 00 76 00 69 00 63 00 69 00 6F 00 73 00 20 00 79 00 20 00 70 00 72 00 6F 00 6D 00 6F 00 63 00 69 00 6F 00 6E 00 65 00 73 00 20 00 70 00 61 00 72 00 61 00 20 00 74 00 69 00 20 00 20 27 28"
   
   sResAndSW1SW2 = apk_APDU(cardservice, sLogFileName, sChannel, sAPDU, "apk_APDU_D6")
   sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
   sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
   
   sLog = "APDU to be sent from APK to Applet COTA/SAP: 0x" + str_SpaceHexa(sAPDU)
   log_write(sLogFileName, sLog)
      
   sLog = "APDU Sent from APK to Applet COTA/SAP: " + simcard_DataResponseDesHexaAndASCII(sResAndSW1SW2, True)
   sLog = sLog + ". Response: " + sResAndSW1SW2
   log_write(sLogFileName, sLog)

   bReturn = False
   if sSW1 == '90' and sSW2 == '00':
      bReturn = True
       
   return bReturn

# APK_Start -----------------------------------------------------------------------------------------------------------
def APK_Start(cardservice, sLogFileName, sSHA1):

    # ANALIZE COMMAND
    bReturn = False

    sChannel = apk_Connect(cardservice, sLogFileName, sSHA1)
    if sChannel:
        bReturn = True
    else:
        sChannel = "01"

    sLog = "CALL ARA-M AND ANALYZE SHA-1 - Channel value: " + str(sChannel)
    log_write(sLogFileName, sLog)

    sLog = str_RepeatString(10, "*")
    sLog = sLog + " - ENDED"

    if bReturn == False:
        sLog = sLog + " NOT"

    sLog = sLog + " OK"
    sLog = sLog + " " + str_RepeatString(10, "*")
    log_write(sLogFileName, sLog)

    sLog = str_RepeatString(100, "-")
    log_write(sLogFileName, sLog + "\n")

    return sChannel

# apk_ARAM_Process_Interpret -----------------------------------------------------------------------------------------------------------
def apk_ARAM_Process_Interpret(sResultARAMRules):

    #sReturn = sResultARAMRules
    sReturn = ""
    
    sValue = str_SpacesOut(sResultARAMRules)
    sValue = simcard_Clean9000(sValue)

    if sValue != "":
    
       sReturn = sReturn + "ARA-M Value: " + str_AddSpaceHexa(sValue) + " - Length: " + bytes_LengthDescriptionAndData(sValue, False)
       sReturn = sReturn + "\n(Standard: GlobalPlatform Device Technology - Secure Element Access Control - GPD_SPE_013)"
       sReturn = sReturn + "\n\n"
               
       sBytes = sValue
       sReturn = sReturn + "Interpreted:\n" 
        
       n = 2
       if str_left(sBytes, n) == "D7":
          sReturn = sReturn + "D7 = Command for getting or sending ARA-M rules"
            
          sByte = str_mid(sBytes, n, 2)
          n = n + 2
          sReturn = sReturn + " - " + bytes_LengthDescription(sByte)
       else:
           n = 0

       sByte = ""
       if str_mid(sBytes, n, 4) == "FF40":
          sReturn = sReturn + "\nFF 40 = ALL - Request to obtain al access rules"

          n = n + 4
          sByte = str_mid(sBytes, n, 2)
          if sByte == "81":
             #Length bigger than 127 bytes
             n = n + 2
             sByte = str_mid(sBytes, n, 2)
             n = n + 2
            
          sReturn = sReturn + " - " + bytes_LengthDescription(sByte)

       else:
          n = 0

       i = n
       nLen = 0
       nE2 = 0

       while i < len(sBytes):
        
              sByte = str_mid(sBytes, i, 2)

              if sByte == "E2":
                 nE2 = nE2 + 1

                 sReturn = sReturn + "\n\nSHA-1 Ocurrence = " + str(nE2)

                 #REF-AR-DO
                 sReturn = sReturn + "\n" + str(nE2) + ". 0x" + sByte + " = REF-AR-DO"
                 i = i + 2
                 sByte = str_mid(sBytes, i, 2)
                 sReturn = sReturn + " - Next byte " + sByte + " = " + bytes_LengthDescription(sByte)

              if sByte == "E1":
                 #REF-DO
                 sReturn = sReturn + "\n" + str(nE2) + ". 0x" + sByte + " = REF-DO"
                 i = i + 2
                 sByte = str_mid(sBytes, i, 2)
                 sReturn = sReturn + " - Next byte " + sByte + " = " + bytes_LengthDescription(sByte)

              if sByte == "C1":
                 #HASH REF-DO
                 sReturn = sReturn + "\n" + str(nE2) + ". 0x" + sByte + " = Hash-REF-DO"
                 i = i + 2
                 sByte = str_mid(sBytes, i, 2)
                 sReturn = sReturn + " - Next byte " + sByte + " = " + bytes_LengthDescription(sByte)

                 i = i + 2
                 nLen = int(bytes_HexaToNro(sByte))
                 nLen = nLen * 2
                 sByteSHA1 = str_mid(sBytes, i, nLen)
                 sReturn = sReturn + "\n" + str(nE2) + ". SHA1 Value = 0x" + str_AddSpaceHexa(sByteSHA1) + " - " + sByteSHA1 + " - " + bytes_LengthDescription(sByte)
                 i = i + (nLen - 2)

                 sDes = apk_ARAM_Process_Interpret_GetProviderDes(sByteSHA1)
                 if sDes != "":
                    sReturn = sReturn + "\n" + str(nE2) + ". Description: " + sDes
            
              i = i + 2

    return sReturn

# apk_ARAM_Process_Interpret_GetProviderDes -----------------------------------------------------------------------------------------------------------
def apk_ARAM_Process_Interpret_GetProviderDes(sSHA1):
    
    sReturn = ""
    sSHA1 = str_SpacesOut(sSHA1)

    if sSHA1 == "F4653BEE3D83F5EFE18960B53594438EB1E3B299":
       sReturn = "AMX"

    if sSHA1 == "29B01C92BFBBE00140D7E6B286E274641CE2D47E":
       sReturn = "Amazonia"

    if sSHA1 == "D9D0C546902E4B4404FC3E335B2DBC583D13AB91":
       sReturn = "DRONE SDK"

    if sSHA1 == "DA5C073BA077FD86B7CB4234331DE5FCC449F460":
       sReturn = "IMOX"

    if sSHA1 == "82C7ED81E373F9D3274520A7880EBB55FBBF3497" or sSHA1 == "64818859B57C04EA08E23075283EA9731E1241EA":
       sReturn = "CARLOS R."
    
    if sReturn != "":
       sReturn = sReturn + " SHA-1"

    return sReturn

# -----------------------------------------------------------------------------------------------------------
