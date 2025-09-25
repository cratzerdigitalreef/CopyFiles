#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
from bytes import *
from str import *
from log import *
from validanro import *
from loci import *
from files import *
from ota import *

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
#from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.Exceptions import *

import sys
from time import sleep

# --------------------------------------------------------------------------------
# SIMCARD - CONSTANT VALUES - MSL (Minimum Security Level)
sSimcard_MSLDefNoSecurity = "00000000"
sSimcard_MSLDefMAC = "02211515"
sSimcard_MSLDefMACAndEncrypt = "16211515"
sSimcard_MSLDefTPDA = "05 81 06 01 F4"
sSimcard_MSLDefSMSC_TPDA = "04 81 06 01 F5"
sSimcard_MSLDefTAR_RAM = "000000"
sSimcard_MSLDefTAR_RAM_Alternative = "B20100"
sSimcard_MSLDefTAR_RFM_SIM = "B00010"
sSimcard_MSLDefTAR_RFM_USIM = "B00001"
sSimcard_MSLDefTAR_RFM_ISIM = "B00002"
sSimcard_MSLDefCounter = "0000000001"
sSimcard_MSLDefKIC = "11111111111111112222222222222222"
sSimcard_MSLDefKID = "33333333333333334444444444444444"
sSimcard_MSLDefCounterName = "COUNTER"
sSimcard_MSLDefKICName = "KIC"
sSimcard_MSLDefKIDName = "KID"
sSimcard_MSLDefMSLName = "MSL"
sSimcard_StatusCommand = "80 F2 00 00"
sSimcard_MSL_SP1_MAC = "2"
sSimcard_MSL_SP1_MACAndEncryption = "6"
sSimcard_MSL_SP1_CounterBigger = "1"
sSimcard_LastEnvelope = ""
sSimcard_LastEnvelopeHeader = "Last Envelope sent:"
sSimcard_SendSMSTPDAPattern = "TPDA: 0x"
sSimcard_SendSMSDATAPattern = "SMS Data: 0x"
sSimcard_SendSMSDATAPatternASCII = "- ASCII:"
sSimcard_ResponseForTAR = "3GPP 23.048 response for TAR"
sSimcard_Header3GPP23040 = "3GPP 23.040"
sSimcard_HeaderAPDUDescription = "APDU details"
sSimcard_9000 = "9000"
sSimcard_0000 = "0000"
sSimcard_6101_AppletOK = "6101"
sSimcard_6310_MoreData = "6310"
sSimcard_9300 = "9300"
sSimcard_6A86_IncorrectPIP2 = "6A86"
sSimcard_Asterics = "*** "
sSimcard_ReserveForFutureUse = "Reserved for future use"
sSimcard_ErrorList = []
sSimcard_ErrorListSepara = "#"
sSimcard_lstItemsSepara = sSimcard_ErrorListSepara

sSimcard_SeparaAPDUForLastAPDUs = str_GetBETWEENPARAM()
sSimcard_SeparaAPDUForLastAPDUs_Visible = "-"
sSimcard_BERTV_SIMtoME = "D0"

#3GPP 23.040 SMS TP-UD User Data: 0x02 71 00
sSimcard_SMSAnswerForSPI2Request_Pattern = "027100"

sSimcard_SMSAnswerForSPI2Request_Pattern_LastData = ""

# --------------------------------------------------------------------------------
sSimcard_LengthBiggerThan127 = "81"

#3GPP 23.040 - TP-UDL User Data Header Length: 0x02
#3GPP 23.040 - IEI - Information Element Identifier: 0x70 (70 to 7F = (U)SIM Toolkit Security Headers)
#3GPP 23.048 - IEIDL - Information Element Identifier Data Length: 0x00
sSimcard_3GPP23040_UDH = "027000"

#3GPP 23.040 - TP-UDL User Data Header Length: 0x07
#3GPP 23.040 - IEI - Information Element Identifier: 0x00
#3GPP 23.048 - IEIDL - Information Element Identifier Data Length: 0x03
#3GPP 23.048 - IEID - Information Element Identifier Data - Octet 1 Concatenated short message reference number: 0x01
#3GPP 23.048 - IEID - Information Element Identifier Data - Octet 2 Maximum number of short messages in the concatenated short message: 0x02
#3GPP 23.048 - IEID - Information Element Identifier Data - Octet 3 Sequence number of the current short message: 0x01
#3GPP 23.048 - IEIb - CPI - Command Package Identifier: 0x70
sSimcard_3GPP23040_UDH_SMPPConcat_First = "070003" 
# 6 bytes because => sSimcard_3GPP23040_UDH_SMPPConcat_First (3 bytes) + "010201" (3 bytes)
nSimcard_3GPP23040_UDH_SMPPConcat_First_Len = 6

sSimcard_PackageBlocks = 100
#sSimcard_PackageBlocks = 104
#sSimcard_PackageBlocks = 80
#sSimcard_3GPP23040_MaxAPDULenForSplit = 114
sSimcard_3GPP23040_MaxAPDULenForSplit = int(sSimcard_PackageBlocks + 4)

sSimcard_PackageBlocks_Delay = 1

#3GPP 23.040 - TP-UDL User Data Header Length: 0x05
#3GPP 23.040 - IEI - Information Element Identifier: 0x00
#3GPP 23.048 - IEIDL - Information Element Identifier Data Length: 0x03
sSimcard_3GPP23040_UDH_SMPPConcat_Next = "050003"

sSimcard_3GPP23048_DesBefore = "Before 3GPP 23.048 MSL processing"
sSimcard_3GPP23048_DesAfter = "After 3GPP 23.048 MSL processing"

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# SIMCARD - CONSTANT VALUES - MSL (Minimum Security Level)
sSimcard_sDefTAR_COTA = "435041" # COTA = 0x43 50 41 = 'CPA'
sSimcard_sDefTAR_COTA_Name = "COTA"
sSimcard_sDefTAR_SAPAUTH = "415448" # SAPAUTH = 0x41 54 48 = 'ATH'
sSimcard_sDefTAR_SAPAUTH_Name = "AUTH"
sSimcard_sDefTPDA = "05 81 06 01 F4" # COTA AMX = 60104
sSimcard_3GPP51014_SMS_TPDU_tag = "0B"
sSimcard_BERTLV_SMPP_download_tag = "D1"

# --------------------------------------------------------------------------------
#sTerminalResponseAPDU2 = "80 F2 00 00"
sTerminalResponseAPDU2 = sSimcard_StatusCommand
sProactiveCommandPattern = "810301"

# GET ATR --------------------------------------------------------------------------------------------------
def simcard_GetATR(cardservice, sLogFileName):
   log_write(sLogFileName, "GET ATR:")
   sATR = cardservice.connection.getATR()
   print("ATR: " + str(sATR))
   sATR = str(bytes_ListNumbersToHexa(sATR)).upper()
   log_write(sLogFileName, "ATR: " + str_SpaceHexa(str(sATR)))
   return sATR

# TERMINAL PROFILE --------------------------------------------------------------------------------------------------
def simcard_TerminalProfile(cardservice, sTerminalProfile, sLogFileName):
    # TERMINAL PROFILE with 0xFF = 33 decimal (0x21)
    
    sTerminalProfileAPDU = ""
    
    if sTerminalProfile == "":
       sTerminalProfileAPDU = "80 10 00 00 21"
       sTerminalProfileAPDU += " FF" * 33
       sLog = "TERMINAL PROFILE: " + str(sTerminalProfileAPDU)
       log_write(sLogFileName, sLog)

    return simcard_processAPDU(cardservice, sTerminalProfileAPDU, sLogFileName)

# TERMINAL PROFILE RESPONSE -----------------------------------------------------------------------------------------
def simcard_TerminalProfileResponse(cardservice, sSW1, sSW2, sLogFileName):

    sFETCH_RESPONSE = "80 12 00 00"
    
    # FETCH RESPONSE FROM SIM: Terminal Profile
    if sSW1 == '91' and sSW2!="00":
        log_write(sLogFileName, "FETCH RESPONSE FROM SIM: Terminal Profile")
        sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
        sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    # TERMINAL APDU TO SIM: 1 - 0x25 - SETUP MENU
    if sSW1 == '90' and sSW2=="00":
        log_write(sLogFileName, "TERMINAL APDU TO SIM: 1 - 0x25 - SETUP MENU")
        sTerminalResponseAPDU1 = "80 14 00 00 0C 81 03 01 25 00 82 02 82 81 83 01 00"
        log_write(sLogFileName, sTerminalResponseAPDU1)
        sResAndSW1SW2 = simcard_Response(cardservice, sTerminalResponseAPDU1, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    # FETCH RESPONSE FROM SIM: 1
    if sSW1 == '91' and sSW2!="00":
        log_write(sLogFileName, "FETCH RESPONSE FROM SIM: 1")
        sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
        log_write(sLogFileName, sTempFetchResponse)
        sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    # TERMINAL APDU TO SIM: 2 - 0x05 - SETUP EVENT LIST
    if sSW1 == '90' and sSW2=="00":
        log_write(sLogFileName, "TERMINAL APDU TO SIM: 2 - 0x05 - SETUP EVENT LIST")
        sTerminalResponseAPDU2t = "80 14 00 00 0C 81 03 01 05 00 82 02 82 81 83 01 00"
        log_write(sLogFileName, sTerminalResponseAPDU2t)
        sResAndSW1SW2 = simcard_Response(cardservice, sTerminalResponseAPDU2t, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    # FETCH RESPONSE FROM SIM: 2
    if sSW1 == '91' and sSW2!="00":
        log_write(sLogFileName, "FETCH RESPONSE FROM SIM: 2")
        sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
        log_write(sLogFileName, sTempFetchResponse)
        sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    # TERMINAL APDU TO SIM: 3 - POLL INTERVAL: 0x1E = 30 seconds 
    if sSW1 == '90' and sSW2=="00":
        log_write(sLogFileName, "TERMINAL APDU TO SIM: 3 - POLL INTERVAL: 0x1E = 30 seconds")
        sTerminalResponseAPDU2t = "80 14 00 00 10 81 03 01 03 00 82 02 82 81 83 01 00 84 02 01 1E"
        log_write(sLogFileName, sTerminalResponseAPDU2t)
        sResAndSW1SW2 = simcard_Response(cardservice, sTerminalResponseAPDU2t, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    # FETCH RESPONSE FROM SIM: 3
    if sSW1 == '91' and sSW2!="00":
        log_write(sLogFileName, "FETCH RESPONSE FROM SIM: 3")
        sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
        log_write(sLogFileName, sTempFetchResponse)
        sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
        
    # TERMINAL APDU TO SIM: 4 - STATUS COMMAND
    #log_write(sLogFileName, "TERMINAL APDU TO SIM: 4 - STATUS COMMAND")
    #sSW1SW2 = simcard_StatusCommand(cardservice, sLogFileName)
    
    return sSW1 + sSW2

# STATUS COMMAND: simcard_StatusCommand ----------------------------------------------------------------------------------------------------------
def simcard_StatusCommand(cardservice, sLogFileName):
    #sTerminalResponseAPDU2 = "80 F2 00 00"
    
    # Updated according standard ETSI 102.221
    #Le Empty, '00', or maximum length of data expected in response
    #sSW2_1F = "1F"
    sSW2_1F = "00"
    
    log_write(sLogFileName, sTerminalResponseAPDU2)
    sResAndSW1SW2 = simcard_Response(cardservice, sTerminalResponseAPDU2 + sSW2_1F, sLogFileName)
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    # FETCH STATUS COMMAND
    if sSW1 == '91':
        sFETCH_RESPONSE = "80 12 00 00"
        sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
        log_write(sLogFileName, sTempFetchResponse)
        sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    if sSW1 == '6C' or sSW1 == '61':
       # ETSI 102.221
       # 7.3.1.1.5 Use of procedure bytes '61xx' and '6Cxx'
       log_write(sLogFileName, "STATUS COMMAND twice because of 0x" + sSW1 + ": " + sSW2 + ". ")
       sResAndSW1SW2 = simcard_Response(cardservice, sTerminalResponseAPDU2 + sSW2, sLogFileName)
       sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
       sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
        
    return sSW1 + sSW2

# STATUS COMMAND: simcard_StatusCommandALLResponses ----------------------------------------------------------------------------------------------------------
def simcard_StatusCommandALLResponses(cardservice, sLogFileName, bNetworkOKOrChangeIMEI):
    sSeparaAPDUForLastAPDUs = ""
    sReturn = simcard_StatusCommandALLResponsesWithLastAPDUs_List(cardservice, sLogFileName, bNetworkOKOrChangeIMEI, sSeparaAPDUForLastAPDUs)
    
    return sReturn[0]

# STATUS COMMAND: simcard_StatusCommandALLResponsesinList ----------------------------------------------------------------------------------------------------------
def simcard_StatusCommandALLResponsesWithLastAPDUs_List(cardservice, sLogFileName, bNetworkOKOrChangeIMEI, sSeparaAPDUForLastAPDUs=str_GetBETWEENPARAM(), sMCC="", sMNC=""):
    """
    Process the STATUS COMMAND and all responses from SIM card.

    :param cardservice: Connection to the reader + SIM.
    :param sLogFileName: Log Name (String)
    :param bNetworkOKOrChangeIMEI: whether it is simulated that there is network or not, and also to change the possible IMEI response.
    :param sSeparaAPDUForLastAPDUs: One character for separating each Response. Example: "#", "*", or BETWEENPARAM
    :return: sw1+sw2, last APDU, all responses
    """
    allResponses_List = []
    #sTerminalResponseAPDU2 = "80 F2 00 00"

    # Updated according standard ETSI 102.221
    #Le Empty, '00', or maximum length of data expected in response
    #sSW2_1F = "1F"
    sSW2_1F = "00"

    if sSeparaAPDUForLastAPDUs=="":
       sSeparaAPDUForLastAPDUs = sSimcard_SeparaAPDUForLastAPDUs
    
    sLastAPDU = ""
       
    log_write(sLogFileName, sTerminalResponseAPDU2)
    sResAndSW1SW2 = simcard_Response(cardservice, sTerminalResponseAPDU2 + sSW2_1F, sLogFileName)
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
    allResponses_List.append(sResAndSW1SW2)

    sWhileMsg = "\nInside while for Status Command Processing"
    
    n = 0
    bExit = False
    while not bExit and n < 100:
       
          # FETCH STATUS COMMAND
          if sSW1 == '91':
             sFETCH_RESPONSE = "80 12 00 00"
             sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
             log_write_InfoInBlue(sLogFileName, "0x" + str_SpaceHexa(sTempFetchResponse) + ". " + sWhileMsg + ": " + str(n))
             sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
             sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
             sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
             allResponses_List.append(sResAndSW1SW2)
             
             if sLastAPDU != "":
                sLastAPDU = sLastAPDU + sSeparaAPDUForLastAPDUs
             sLastAPDU = sLastAPDU + sTempFetchResponse 
             if len(sResAndSW1SW2) > 4:
                sLastAPDU = sLastAPDU + sSeparaAPDUForLastAPDUs + sResAndSW1SW2 
                 
             
             #PROCESS TERMINAL RESPONSE ACCORDING TO STATUS COMMAND
             sTempFetchResponse = simcard_StatusCommandALLResponses_TerminalResponse(cardservice, sLogFileName, sResAndSW1SW2, bNetworkOKOrChangeIMEI, sMCC, sMNC)
             log_write_InfoInBlue(sLogFileName, "0x" + str_SpaceHexa(sTempFetchResponse) + ". " + sWhileMsg + ": " + str(n))
             sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
             sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
             sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
             allResponses_List.append(sResAndSW1SW2)
             
             sLastAPDU = sLastAPDU + sSeparaAPDUForLastAPDUs + sTempFetchResponse
             sLastAPDU = sLastAPDU + sSeparaAPDUForLastAPDUs + sResAndSW1SW2
             
          if sSW1 == '6C' or sSW1 == '61':
             # ETSI 102.221
             # 7.3.1.1.5 Use of procedure bytes '61xx' and '6Cxx'
             log_write_InfoInBlue(sLogFileName, "STATUS COMMAND twice because of 0x" + sSW1 + ": " + sSW2 + ". " + sWhileMsg + ": " + str(n))
             sResAndSW1SW2 = simcard_Response(cardservice, sTerminalResponseAPDU2 + sSW2, sLogFileName)
             sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
             sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
             allResponses_List.append(sResAndSW1SW2)

             sLastAPDU = sLastAPDU + sSeparaAPDUForLastAPDUs + sResAndSW1SW2

          if sSW1 == '90':
             bExit = True
        
          n = n + 1
          
    return sSW1 + sSW2, sLastAPDU, allResponses_List

# STATUS COMMAND: simcard_StatusCommandALLResponses_TerminalResponse ----------------------------------------------------------------------------------------------------------
def simcard_StatusCommandALLResponses_TerminalResponse(cardservice, sLogFileName, sResponse, bNetworkOKOrChangeIMEI, sMCC="", sMNC=""):
    sTemp = simcard_StatusCommandALLResponses_TerminalResponseDes(sLogFileName, sResponse, bNetworkOKOrChangeIMEI, sMCC, sMNC)
    #print("Len: " + str(len(sTemp)))
    #print("sTemp[0]: " + str(sTemp[0]))
    #print("sTemp[1]: " + str(sTemp[1]))
    
    if len(sTemp) >= 0:
       return sTemp[0]
    else:
       return sTemp   

# STATUS COMMAND: simcard_StatusCommandALLResponses_TerminalResponse ----------------------------------------------------------------------------------------------------------
def simcard_StatusCommandALLResponses_TerminalResponseGetDesOnly(sResponse, bNetworkOKOrChangeIMEI=True, sMCC="", sMNC=""):
    sTemp = simcard_StatusCommandALLResponses_TerminalResponseDes("", sResponse, bNetworkOKOrChangeIMEI, sMCC, sMNC)
    #print("Len: " + str(len(sTemp)))
    #print("sTemp[0]: " + str(sTemp[0]))
    #print("sTemp[1]: " + str(sTemp[1]))
    
    if len(sTemp) >= 1:
       return sTemp[1]
    else:
       return sTemp   

# STATUS COMMAND: simcard_StatusCommandALLResponses_TerminalResponse ----------------------------------------------------------------------------------------------------------
def simcard_StatusCommandALLResponses_TerminalResponseGetCmd(sResponse):

    sResponse = str_SpacesOut(sResponse)
    nLenResponse = len(sResponse)
    
    sCmd = ""
    sCmdQualif = ""
    n = 0
    sSent = ""    
    
    #print("simcard_StatusCommandALLResponses_TerminalResponseGetCmd - sResponse: " + sResponse)
    
    if str_left(sResponse,2) == sSimcard_BERTV_SIMtoME and nLenResponse > 10:
       #D0 30 81 03 01 13 00 82 02 81 83 0B 25 05 00 05 81 06 01 F4 00 04 1B 09 27 02 13 FF FE AA 29 05 82 8A 16 49 01 94 33 75 59 31 43 4F 54 41 30 35 30 31 90 00
       n = 10
       if str_mid(sResponse,2,2) == sSimcard_LengthBiggerThan127:
          # IT IS A LENGTH BIGGER THAN 127 -> D0 81 [LEN]
          n = n + 2
          
       #sSent = sSent + "to be "
    
    if str_left(sResponse,2) == "80" and nLenResponse>16:
       #80 14 00 00 0C 01 03 01 13 00 02 02 82 81 03 01 00
       n = 16
       sSent = sSent + "sent"

    if n>0:
       sCmd = str_mid(sResponse, n, 2)
       #print("sCmd: " + sCmd)
       n = n + 2
       sCmdQualif = str_mid(sResponse, n, 2)
       #print("sCmdQualif: " + sCmdQualif)
    
    return sCmd, sCmdQualif, sSent


# STATUS COMMAND: simcard_StatusCommandALLResponses_TerminalResponseDes ----------------------------------------------------------------------------------------------------------
def simcard_StatusCommandALLResponses_TerminalResponseDes(sLogFileName, sResponseParam, bNetworkOKOrChangeIMEIOrChangeMCCMNC, sMCC="", sMNC=""):
    sReturn = ""
    sResponse = str_TrimCleanSpaces(sResponseParam)

    #print("simcard_StatusCommandALLResponses_TerminalResponseDes - sResponse: " + sResponse)
    
    sTemp = simcard_StatusCommandALLResponses_TerminalResponseGetCmd(sResponse)
    sCmd = sTemp[0]
    sCmdQualif = sTemp[1]
    sOK = ""          
    if sTemp[2] != "":
       sOK = sOK + " - Response " + sTemp[2] + " OK "
    
    sLog = ""
    if sResponse!="" and sCmd!="" and sCmdQualif!="":
       sLog = sLog + "TERMINAL RESPONSE APDU: 0x" + str_SpaceHexa(sResponse) + ". CMD: " + sCmd + ". Qualifier: " + sCmdQualif

    #D0 2B 81 03 01 13 00 82 02 81 83 0B 20 05 00 05 81 06 01 F4 00 04 16 270213FFFEAA07080300010002434F544130323041449000
    #3GPP 51.014 SMS TPDU tag: 0x0B
    #3GPP 51.014 SMS TPDU Length: 0x20 - Decimal: 32 bytes

    sDes = simcard_STKCmdGetDes(sCmd, True)
    if sDes != "":
       sLog = sLog + ". Description: 0x" + sCmd + " => "
       sLog = sLog + sDes
    
    bDataInASCII = True
    
    if sCmd == simcard_STKCmdGetCmdSendSMS() and sCmdQualif == "00":
       #0x13 = SEND SMS RESPONSE
       #0x03 01 00 = SEND SMS OK
       #0x03 01 21 = SEND SMS NOT OK - Network currently unable to process the command 21
       sReturn = "80 14 00 00 0C 01 03 01 13 00 02 02 82 81 03 01 00"
       
       if bNetworkOKOrChangeIMEIOrChangeMCCMNC == False:
          sReturn = "80 14 00 00 0C 01 03 01 13 00 02 02 82 81 03 01 21"
       sLog = sLog + sOK
       sSMSProc = simcard_SendSMSCmd_Process(sLogFileName, sResponse)
       #if sDes in sSMSProc:
       #   sSMSProc = str_midToEnd(sSMSProc, len(sDes))
       sLog = sLog + sSMSProc
       #print("simcard_StatusCommandALLResponses_TerminalResponseDes - sSMSProc = " + str(sSMSProc) + " - sLog = " + str(sLog))
       bDataInASCII = False
       
    if sCmd == "15" and sCmdQualif == "00":
       #0x15 = LAUNCH BROWSER RESPONSE
       #0x03 01 00 = OK
       sReturn = "80 14 00 00 0C 01 03 01 15 00 02 02 82 81 03 01 00"
       sLog = sLog + sOK

    if sCmd == "21" and sCmdQualif == "00":
       #0x21 = DISPLAY TEXT RESPONSE
       #0x03 01 00 = OK
       sReturn = "80 14 00 00 0C 01 03 01 21 00 02 02 82 81 03 01 00"
       sLog = sLog + sOK

    if sCmd == "22" and sCmdQualif == "0C":
       #0x22 = GET INKEY
       #0x0C = FLAG FOR YES/NO
       #0x03 01 00 0D 02 04 01 = OK - YES
       #0x03 01 00 0D 02 04 00 = OK - NO
       sReturn = "80 14 00 00 10 01 03 01 22 00 02 02 82 81 03 01 00 0D 02 04 01"
       sLog = sLog + sOK + " - Answering: YES"
       
    if sCmd == "26" and sCmdQualif == "00":
       #0x26 = PROVIDE LOCI RESPONSE. Flag: LOCI
       #LOCI = 27 02 13 FF FE AA BB CC DD => MCC: 722, MNC: 310, LAC: FFFE, Cell ID: AABB, SubCell ID: CCDD
       #sReturn = "80 14 00 00 17 01 03 01 26 00 02 02 82 81 03 01 00 93 09 27 02 13 FF FE AA BB CC DD"
       sLog = sLog + " - LOCI"
       sRandom = simcard_GenerateRandom(12)
       #print("sRandom: " + sRandom)
       sReturn = "80 14 00 00 17 01 03 01 26 00 02 02 82 81 03 01 00 93 09 "
       sLOCI = "27 02 13"
       if sMCC != "" and sMNC != "":
          #HOME
          sLOCI = loci_MCC_MNC_To_Hexa(sMCC, sMNC)
       if sMCC != "" and sMNC == "":
          #ROAMING NATIONAL
          sLOCI = loci_MCC_MNC_To_Hexa(sMCC, str_right(sRandom,3))
       if bNetworkOKOrChangeIMEIOrChangeMCCMNC == True:
          #ROAMING INTERNATIONAL - IT (bNetworkOKOrChangeIMEIOrChangeMCCMNC) HAS MORE PRIORITY THAN MCC-MNC
          sLOCI = str_left(sRandom,6) 
       sLOCI = sLOCI + " FF FE AA" + str_right(sRandom, 6)   
       sReturn = sReturn + sLOCI
       #sLog = sLog + ". LOCI answered: 0x" + str_SpaceHexa(sLOCI + " FF FE AA" + sRandom)
       sLog = sLog + ". LOCI answered: 0x" + str_SpaceHexa(sReturn) + ". Interpreted: " + loci_lociFromHexa(sLOCI, True)
       
       #print("sLog LOCI: " + sLog + " - sReturn: " + sReturn)
       
    if sCmd == "26" and sCmdQualif == "01":
       #0x26 = PROVIDE LOCI RESPONSE. Flag: IMEI
       #IMEI = 8A 16 49 01 94 73 95 08
       #sReturn = "80 14 00 00 16 01 03 01 26 01 02 02 82 81 03 01 00 94 08 8A 16 49 01 94 73 95 08"
       sLog = sLog + " - IMEI"
       sIMEI = str_SpaceHexa("8A 16 49 01 94 73 95 08")
       if bNetworkOKOrChangeIMEIOrChangeMCCMNC == True:
          sIMEI = simcard_generate_random_imei()
       # ToDo: We changed from 80 14 00 00 16 01 03 01 26 01 to 80 14 00 00 16 01 03 01 26 00 temporarily
       sReturn = "80 14 00 00 16 01 03 01 26 01 02 02 82 81 03 01 00 94 08 " + sIMEI
       sLog = sLog + ". IMEI answered: 0x" + sIMEI + " - bNetworkOKOrChangeIMEIOrChangeMCCMNC: " + str(bNetworkOKOrChangeIMEIOrChangeMCCMNC)
       print(sLog)

    if sCmd == "26" and sCmdQualif == "06":
       #0x26 = PROVIDE LOCI RESPONSE. Flag: ACCESS TECHNOLOGY
       #ACCORDING TRACER
       #sReturn = "80 14 00 00 0F 81 03 01 26 06 02 02 82 81 03 01 00 3F 01 08"
       sReturn = "80 14 00 00 0F 81 03 01 26 06 02 02 82 81 03 01 00 3F 01 08"
       sLog = sLog + " - " + fPLociACCTECHDes("08")
          
    if sCmd == "26" and sCmdQualif == "03":
       #0x26 = PROVIDE LOCI RESPONSE. Flag: DATE AND TIME
       #sReturn = "80 14 00 00 15 01 03 01 26 03 02 02 82 81 03 01 00 A6 07 32 01 01 51 74 21 FF"
       sReturn = "80 14 00 00 15 01 03 01 26 03 02 02 82 81 03 01 00 A6 07"
       sDateTime = fPLociGetDateTimePreparedForSIM()
       if sDateTime == "":
          sDateTime = "42 11 52 41 34 00 FF"
       sReturn = sReturn + sDateTime   
       #print("simcard_StatusCommandALLResponses_TerminalResponseDes: " + sReturn)
       sLog = sLog + " - DATE AND TIME answered: 0x07 " + str_SpaceHexa(sDateTime) + " - " + fPLociGetDateTimeFromSIM(sDateTime)
       
    if sCmd == "27" and sCmdQualif == "00":
       #0x27 = TIMER MANAGEMENT RESPONSE
       #Timer identifier: 0x01 - Timer 1
       sReturn = "80 14 00 00 0F 01 03 01 27 00 02 02 82 81 03 01 00 24 01 01"
       sLog = sLog + " - Timer 0x01"

    if sCmd == "12" and sCmdQualif == "00":
       #0x12 = SEND USSD
       # AMSWER OK FOR USSD NUMBER, EXAMPLE: *611# - 0x2A 5B 2C 36 02
       sReturn = "80 14 00 00 14 01 03 01 12 00 02 02 82 81 0A 06 0F 2A 5B 2C 36 02 03 01 00"
       sLog = sLog + " - USSD answered: *611# - 0x2A 5B 2C 36 02" 

    if sCmd == "24" and sCmdQualif == "00":
       #0x24 = SELECT ITEM
       #0x03 01 00 10 01 01 = 1st item
       #0x03 01 00 10 01 02 = 2nd item
       sReturn = "80 14 00 00 0F 01 03 01 24 00 02 02 82 81 03 01 00 10 01 01"
       sLog = sLog + " - Selecting first option: 01"

    if sCmd == "23":
       #0x22 = GET INPUT
       # sReponse = D01C8103012301820281810D0D04496E73657274204E616D653A110201149000
       sData = str_left(sResponse, len(sResponse)-4)
       sMinMax = str_getSubStringFromOcur(sData, simcard_getTAG_GETINPUT_MINMAX() + "02",1)
       #print("sMinMax: " + sMinMax)
       sInput = "1" 
       nMax = 0
       if sMinMax != "":
          sMin = str_left(sMinMax,2)
          sMax = str_mid(sMinMax,2,2)
          nMax = bytes_HexaToNro(sMax)
          sInput = str_RepeatString(nMax, "1")
       #print("nMax: " + str(nMax))
       #print("sInput: " + sInput)   
       if nMax == 0:
          #          80 14 00 00 13 01 03 01 23 01                 02 02 82 81 03 01 00 0D 05 04 31 32 33 34
          sReturn = "80 14 00 00 13 01 03 01 23 " + sCmdQualif + " 02 02 82 81 03 01 00 0D 05 04 31 32 33 34"
       else:
          # Terminal Response - 80 14 00 00 23 01 03 01 23 01 02 02 82 81 03 01 00 0D 15 04 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31
          sReturn = "01 03 01 23 " + sCmdQualif + " 02 02 82 81 03 01 00 0D " + str(bytes_NroToHexa(int(nMax)+1)) + " 04 " + bytes_StrToHexa(sInput)
          sReturn = str_SpacesOut(sReturn)
          #print("GETINPUT: " + sReturn)   
          sReturn = "80 14 00 00 " + bytes_NroToHexa(len(sReturn)//2) + sReturn
       #print("GETINPUT: " + sReturn)   
       nInput = len(sInput)
       sLog = sLog + sOK + " - Answering: " + sInput + " (0x" + str_AddSpaceHexa(bytes_StrToHexa(sInput)) + " - Length: decimal=" + str(nInput) + " hexa=0x" + bytes_NroToHexa(nInput) + ")"
       #print("sLog: " + sLog)
       
    if sReturn != "":
       sReturn = str_TrimCleanSpaces(sReturn)
    else:
       # ANSWER AT LEAST OK FOR RETURN
       sReturn = "80 14 00 00 0C 01 03 01 " + sCmd + " " + sCmdQualif + " 02 02 82 81 03 01 00"
       
    if bDataInASCII:   
       sLog = sLog + "\n" + simcard_DataResponseDesHexaAndASCII(sResponseParam, True) 
    
    if sLog != "":
       if sLogFileName != "":   
          log_write(sLogFileName, sLog)
       print(sLog)
    
    return sReturn, sLog

# Get STK Command Type or Terminal Response Type----------------------------------------------------------------------------------------------------------
def simcard_getCommandType(sBERTLV_Value, sLogFilename=''):
   sBERTLV_Value=sBERTLV_Value.replace(" ","")
   sCommandType = 'UNKNOWN'
   sCommandTag = sBERTLV_Value[0:2]
   if sCommandTag == sSimcard_BERTV_SIMtoME:
    nCounter = 0

    sBERTLV_L = sBERTLV_Value[2:4]
    nCounter = 4
    if sBERTLV_L == '81':
      #print('Length coded in 2 bytes according to ISO/IEC 7816: 0x81 - length is coded from 128 to 255 bytes')
      sBERTLV_L = sBERTLV_Value[4:6]
      nCounter = 6
      #Getting all BER TLV Values
    sBERTLV_Value = sBERTLV_Value [nCounter:]
      # sLog = COTAProactiveCMDProcess(sLog, sBERTLV_Value)      


    sCommndType = sBERTLV_Value[6:8]
    sCommandType = simcard_STKCmdGetDes(sCommndType)

   # Terminal response and fetch
   elif sCommandTag == '80':
    if sBERTLV_Value[2:4] == '12':
       psCommandType= 'FETCH'
    elif sBERTLV_Value[2:4] == '14':
       sCommandTypeTR = sBERTLV_Value[16:18]
       sCommandTypeTR = str_SpacesOut(simcard_STKCmdGetDes(sCommandTypeTR, False) + "TERMINALRESPONSE")
       
   return sCommandType

# SW1 + SW2 Process: simcard_SW1SW2ProcessReturnSW1 ----------------------------------------------------------------------------------------------------------
def simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName):
    return simcard_SW1SW2Process(sResAndSW1SW2, True, False, sLogFileName)
    
# SW1 + SW2 Process: simcard_SW1SW2ProcessReturnSW2 ----------------------------------------------------------------------------------------------------------
def simcard_SW1SW2ProcessReturnSW2(sResAndSW1SW2, sLogFileName):
    return simcard_SW1SW2Process(sResAndSW1SW2, False, True, sLogFileName)

# SW1 + SW2 Process: simcard_SW1SW2ProcessRetunrSW1SW2 ----------------------------------------------------------------------------------------------------------
def simcard_SW1SW2ProcessReturnSW1SW2(sResAndSW1SW2, sLogFileName):
    return simcard_SW1SW2Process(sResAndSW1SW2, False, False, sLogFileName)
    
# SW1 + SW2 Process: simcard_SW1SW2Process ----------------------------------------------------------------------------------------------------------
def simcard_SW1SW2Process(sResAndSW1SW2, bGetSW1Only, bGetSW2Only, sLogFileName):
    sSW1 = ""
    sSW2 = ""
    if sResAndSW1SW2!="":
       sSW1 = simcard_SW1SW2GetSW1(sResAndSW1SW2)
       sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
       #sLog = "simcard_SW1SW2Process = SW1: " + sSW1 + " - SW2: " + sSW2
       #log_write(sLogFileName, sLog)
       sSW1 = sSW1.upper()   
       sSW2 = sSW2.upper()   
    
    if bGetSW1Only:
       return sSW1
    if bGetSW2Only:
       return sSW2
    return sSW1 + sSW2


# RESPONSE: simcard_Response ----------------------------------------------------------------------------------------------------------
def simcard_Response(cardservice, sAPDU, sLogFileName):
    sReturn = simcard_processAPDU(cardservice, sAPDU, sLogFileName)
    if bytes_IsHexaValid(sReturn):
       return sReturn
    else:
       print("simcard_Response sReturn: " + sReturn)   
    return ""

# RESPONSE simcard_sendAPDU ----------------------------------------------------------------------------------------------------------
def simcard_sendAPDU(cardservice, sAPDU, sLogFileName = ''):
    return simcard_processAPDU(cardservice, sAPDU, sLogFileName)

# PROCESS APDU simcard_processAPDU ------------------------------------------------------------------------------------------------------
def simcard_processAPDU(cardservice, sAPDU, sLogFileName):
    #print(sAPDU)
    
    sAPDU = str_TrimCleanSpaces(sAPDU)
    if len(sAPDU) < 8:
       return "WRONG LENGTH FOR APDU: " + sAPDU + " - Length: " + str(len(sAPDU)) 
       
    sAPDU = str_SpaceHexa(sAPDU)
    
    log_write(sLogFileName, "APDU to be sent: " + str(sAPDU))
    apdu = bytes_HexaStrToListNumbers(sAPDU, ' ')

    sw1 = ""
    sw2 = ""
    #print('APDU (in decimal): [%s]' % ', '.join(map(str, apdu)))
    #print("cardservice: " + str(cardservice))
    try:
        response, sw1, sw2 = cardservice.connection.transmit(apdu)
        sSW1 = bytes_NroToHexa(sw1).upper()
        sSW2 = bytes_NroToHexa(sw2).upper()
        sResponse = str(bytes_ListNumbersToHexa(response)).upper()
    except Exception as e:
        sError = "An unexpected error has occurred. " + str(e) 
        log_write_ErrorInRed(sLogFileName, sError)
        return str(e)
        # sys.exit()

    sLog = ""
    sSW1SW2 = ""
    
    if sSW1!="" and sSW2!="":
       sLog = sLog + "RESPONSE APDU: " + "SW1=" + sSW1 + " - SW2=" + sSW2 + "."
       sSW1SW2 = bytes_Clean0x(sSW1+sSW2)
       sSW1SW2 = sSW1SW2.upper()
    if sResponse != "":
       sLog = sLog + " " + simcard_DataResponseDesHexaAndASCII(sResponse, True)
       sResponse = sResponse.upper()
    
    log_write(sLogFileName, sLog + "\n")
    return sResponse + sSW1SW2



# GET SW1 simcard_SW1SW2GetSW1 ------------------------------------------------------------------------------------------------------
def simcard_SW1SW2GetSW1(sSW1SW2):
    return simcard_SW1SW2Get(sSW1SW2, True)

# GET SW2 simcard_SW1SW2GetSW2 ------------------------------------------------------------------------------------------------------
def simcard_SW1SW2GetSW2(sSW1SW2):
    return simcard_SW1SW2Get(sSW1SW2, False)
    
# GET SW1 and SW2 simcard_SW1SW2Get ----------------------------------------------------------------------------------------------
def simcard_SW1SW2Get(sSW1SW2, bSW1):
    sSW1SW2=bytes_Clean0x(sSW1SW2)
    nLen = len(sSW1SW2)

    #print(sSW1SW2)
    if nLen > 4:
       sSW1SW2 = sSW1SW2[nLen-4:]
    #print(sSW1SW2)
       
    if nLen >= 4:
       if bSW1:
          return sSW1SW2[:2]
       else:
          return sSW1SW2[2:4]
    else:
       return sSW1SW2      

# simcard_sendEnvelopePrepareAPDULower127 ------------------------------------------------------------------------------------------------------
def simcard_sendEnvelopePrepareAPDULower127(sTPDA, sCMD, sTAR=sSimcard_sDefTAR_COTA, sMSL=sSimcard_MSLDefNoSecurity, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter, bGet3GPP23040Only=False):
    #Envelope
    #C - 80 C2 00 00 32 D1 30 02 02 83 81 06 04 81 06 01 F5 0B 24 40 
    #    05 81 06 01 F4 
    #    7F F6 00 00 00 00 00 00 00 14 02 70 00 00 
    #    0F 0D 00 00 00 00 43 50 41 00 00 00 00 00 00 
    #    F0
    #SW - 91 7D

    if sTAR=="":
       sTAR = sSimcard_sDefTAR_COTA
       
    sCMD = str_TrimCleanSpaces(sCMD)
    nCMDLen = (len(sCMD)//2)
    sCMDLen = simcard_GetLengthInHexa(sCMD)

    sMSL_SMPP = "0D " + sMSL + sTAR + " 00 00 00 00 01 00"
    sMSL_SMPP = str_TrimCleanSpaces(sMSL_SMPP)
    nMSLLen = (len(sMSL_SMPP)//2)
    
    #EXAMPLES FOR CMD + HEADER LENGTH: 
    #"7F F6 00 00 00 00 00 00 00 14 02 70 00 00 0F"
    #"7F F6 00 00 00 00 00 00 00 29 02 70 00 00 24"
    nCMDAndHeaderLen = nMSLLen + nCMDLen + 5
    sCMDAndHeaderLen = str(bytes_NroToHexa(nCMDAndHeaderLen))
     
    sEnvelope = str(bytes_NroToHexa(nMSLLen + nCMDLen)) + sMSL_SMPP + sCMD
    
    sEnvelopeAPDU = "80 C2 00 00"
    sEnvelopeAPDU = str_TrimCleanSpaces(sEnvelopeAPDU)
    if sTPDA == "":
       sTPDA = sSimcard_sDefTPDA

    #EXAMPLE FOR CMD + HEADER LENGTH + TPDA: 
    #"39 40 05 81 06 01 F4 7F F6 00 00 00 00 00 00 00 29"
    nCMDAndHeaderLenAndTPDA = nCMDAndHeaderLen + (len(str_TrimCleanSpaces("40" + sTPDA + "7F F6 00 00 00 00 00 00 00 "))//2) + 1
    sCMDAndHeaderLenAndTPDA = str(bytes_NroToHexa(nCMDAndHeaderLenAndTPDA))

    # SIMULATING SMSC WITH NUMBER = 04 81 21 43 F5 => 4 bytes
    sEnvelopeAPDUHeader = "02 02 83 81 06 04 81 21 43 F5 " + sSimcard_3GPP51014_SMS_TPDU_tag + sCMDAndHeaderLenAndTPDA + "40" + sTPDA + "7F F6 00 00 00 00 00 00 00 " + sCMDAndHeaderLen + "02 70 00 00"
    sEnvelopeAPDUHeader = str_TrimCleanSpaces(sEnvelopeAPDUHeader)
    
    sEnvelope = sEnvelopeAPDUHeader + sEnvelope
    #print("1:" + sEnvelope)
    sEnvelopeLen = simcard_GetLengthInHexa(sEnvelope)
    sEnvelope = sSimcard_BERTLV_SMPP_download_tag + sEnvelopeLen + sEnvelope
    #print("2:" + sEnvelope)
    sEnvelopeLen = simcard_GetLengthInHexa(sEnvelope)
    sEnvelope = sEnvelopeAPDU + sEnvelopeLen + sEnvelope
    #print("3:" + sEnvelope)
    sEnvelope = sEnvelope.upper()
    
    # ----------------------------------------------------------------------------------------------------------------------
    #ANALIZE MSL
    sMSL = str_TrimCleanSpaces(sMSL)
    #print("simcard_sendEnvelopePrepareAPDULower127 - sMSL = " + sMSL)

    bReturn = True
    
    sEnvelopeNoMSL = sEnvelope 
    sEnvelopeWithMSL = sEnvelopeNoMSL

    #print("simcard_sendEnvelopePrepareAPDULower127 - sEnvelope Before Analyzing MSL - sEnvelopeNoMSL: " + str(sEnvelopeNoMSL))
    
    if str_left(sMSL,2) != "00":
       #print("simcard_sendEnvelopePrepareAPDULower127 - sMSL = " + sMSL)
       # IT MUST BE PREPARED THE MESSAGE WITH SECURITY ACCORDING TO MSL
       bReturn, sEnvelopeWithMSL = simcard_PrepareAPDUWithSecurity(sEnvelope, sCMD, sTAR, sMSL, sKIC, sKID, sCounter)
       #print("simcard_sendEnvelope - bReturn = " + str(bReturn) + " - sEnvelopeWithMSL = " + str(sEnvelopeWithMSL))
       if bReturn == False or bytes_IsCharValidHex(sEnvelopeWithMSL)==False:
          return False, sEnvelopeNoMSL, ""

    # ----------------------------------------------------------------------------------------------------------------------

    if bGet3GPP23040Only:
       sEnvelopeNoMSL = simcard_APDU_Get3GPP23040(sEnvelopeNoMSL)
       sEnvelopeWithMSL = simcard_APDU_Get3GPP23040(sEnvelopeWithMSL)
       
    lstEnvelopeNoMSL = []
    lstEnvelopeNoMSL.append(sEnvelopeNoMSL)
    lstEnvelopeWithMSL = []
    lstEnvelopeWithMSL.append(sEnvelopeWithMSL)

    #print("simcard_sendEnvelopePrepareAPDULower127 - sEnvelope After Analyzing MSL - sEnvelopeWithMSL: " + str(lstEnvelopeWithMSL))
       
    return bReturn, lstEnvelopeNoMSL, lstEnvelopeWithMSL

# simcard_sendEnvelopePrepareAPDU_Desciption ------------------------------------------------------------------------------------------------------
def simcard_sendEnvelopePrepareAPDU_WithDescription(sTPDA, sAPDU, sTAR=sSimcard_sDefTAR_COTA, sMSL=sSimcard_MSLDefNoSecurity, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter):
    
    bReturn, lstEnvelopeNoMSL, lstEnvelopeWithMSL = simcard_sendEnvelopePrepareAPDU(sTPDA, sAPDU, sTAR, sMSL, sKIC, sKID, sCounter)

    sDes = ""
    
    if bReturn:    
       sDes = sSimcard_HeaderAPDUDescription + ":\n" + sSimcard_3GPP23048_DesBefore

       n = 0
       while n < len(lstEnvelopeNoMSL):
             lstEnvelopeNoMSL[n] = str_TrimCleanSpaces(lstEnvelopeNoMSL[n])
             sAPDURef = "[" + str(n+1) + " of " + str(len(lstEnvelopeNoMSL)) + "]"
             sDes = sDes + "\n" + "APDU " + sAPDURef + ": 0x" + str_SpaceHexa(lstEnvelopeNoMSL[n]) + " - " + simcard_DescriptionLength(lstEnvelopeNoMSL[n])
             s23040 = simcard_APDU_Get3GPP23040(lstEnvelopeNoMSL[n])
             sDes = sDes + "\n" + sSimcard_Header3GPP23040 + " DATA for APDU " + sAPDURef + " '" + sSimcard_3GPP23048_DesBefore + "': 0x" + str_SpaceHexa(s23040) + " - " + simcard_DescriptionLength(s23040)
             n = n + 1
    
       sDes = sDes + "\n\n" + sSimcard_3GPP23048_DesAfter

       n = 0
       while n < len(lstEnvelopeWithMSL):
             lstEnvelopeNoMSL[n] = str_TrimCleanSpaces(lstEnvelopeWithMSL[n])
             sAPDURef = "[" + str(n+1) + " of " + str(len(lstEnvelopeWithMSL)) + "]"
             sDes = sDes + "\n" + "APDU " + sAPDURef + ": 0x" + str_SpaceHexa(lstEnvelopeWithMSL[n]) + " - " + simcard_DescriptionLength(lstEnvelopeWithMSL[n])
             s23040 = simcard_APDU_Get3GPP23040(lstEnvelopeWithMSL[n])
             sDes = sDes + "\n" + sSimcard_Header3GPP23040 + " DATA for APDU " + sAPDURef + " '" + sSimcard_3GPP23048_DesAfter + "' where MSL is '" + str_SpaceHexa(sMSL) + "': 0x" + str_SpaceHexa(s23040) + " - " + simcard_DescriptionLength(s23040)
             n = n + 1
    
    return bReturn, lstEnvelopeNoMSL, lstEnvelopeWithMSL, sDes
    
    
# simcard_sendEnvelopePrepareAPDU ------------------------------------------------------------------------------------------------------
def simcard_sendEnvelopePrepareAPDU(sTPDA, sAPDU, sTAR=sSimcard_sDefTAR_COTA, sMSL=sSimcard_MSLDefNoSecurity, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter):

    bReturn = True
    
    sAPDU = str_TrimCleanSpaces(sAPDU)
    nAPDULen = (len(sAPDU)//2)

    #print("simcard_sendEnvelopePrepareAPDU - sAPDU = " + str(sAPDU))

    # CHECK COMMAND LENGTH!
    # IF IT IS BIGGER THAN 0x7F = 127, THE COMMAND MUST BE SPLITTED
    if nAPDULen > sSimcard_3GPP23040_MaxAPDULenForSplit:

       bReturn, lstEnvelopeNoMSL, lstEnvelopeWithMSL = simcard_sendEnvelopePrepareAPDUBigger127(sTPDA, sAPDU, sTAR, sMSL, sKIC, sKID, sCounter)

    else: 
       bReturn, lstEnvelopeNoMSL, lstEnvelopeWithMSL = simcard_sendEnvelopePrepareAPDULower127(sTPDA, sAPDU, sTAR, sMSL, sKIC, sKID, sCounter)
    
    #print("simcard_sendEnvelopePrepareAPDU - lstEnvelopeNoMSL = " + str(lstEnvelopeNoMSL) + " - lstEnvelopeWithMSL = " + str(lstEnvelopeWithMSL))
    
    return bReturn, lstEnvelopeNoMSL, lstEnvelopeWithMSL


# SEND ENVELOPE simcard_sendEnvelope ------------------------------------------------------------------------------------------------------
def simcard_sendEnvelope(cardservice, sTPDA, sCMD, sLogFileName, sTAR=sSimcard_sDefTAR_COTA, sMSL=sSimcard_MSLDefNoSecurity, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter, b9000WithDescription=False):

    sCMD = str_TrimCleanSpaces(sCMD)

    sResAndSW1SW2  =""
    
    bReturn, lstEnvelopeNoMSL, lstEnvelopeWithMSL = simcard_sendEnvelopePrepareAPDU(sTPDA, sCMD, sTAR, sMSL, sKIC, sKID, sCounter)
    if not bReturn:
       return ""
        
    nEnvelopes = len(lstEnvelopeNoMSL)
    
    log_write(sLogFileName, "TOTAL SMPP to be sent: " + str(nEnvelopes))
    log_write(sLogFileName, "TOTAL Length for CMD: " + str((len(sCMD)//2)) +  " bytes (in hexadecimal 0x" + bytes_NroToHexa((len(sCMD)//2)) + ")")
    
    #print("simcard_sendEnvelope - lstEnvelopeNoMSL = " + str(lstEnvelopeNoMSL) + " - lstEnvelopeWithMSL = " + str(lstEnvelopeWithMSL))
    
    n = 0
    while n < nEnvelopes:
        
          sEnvelopeNoMSL = lstEnvelopeNoMSL[n]
          sEnvelopeWithMSL = lstEnvelopeWithMSL[n]
          
          # GLOBAL VARIABLE TO SAVE LAST ENVELOPE SENT
          global sSimcard_LastEnvelope
          sSimcard_LastEnvelope = sEnvelopeNoMSL
          sEnvelope = sEnvelopeWithMSL

          if sSimcard_LastEnvelope != sEnvelope:
             sSimcard_LastEnvelope = sSimcard_LastEnvelope + "\n" + sEnvelope

          sResAndSW1SW2 = simcard_sendAPDU(cardservice, sEnvelope, sLogFileName)
          sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
          sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

          #print("simcard_sendEnvelope - sResAndSW1SW2: " + str(sResAndSW1SW2))
    
          # FETCH RESPONSE FROM ENVELOPE
          if (sSW1 == '91' and sSW2!="00") or (sSW1 == '61' and sSW2!="00"):
             sFETCH_RESPONSE = "80 12 00 00"
             log_write(sLogFileName, "FETCH RESPONSE FROM ENVELOPE")
             sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
             log_write(sLogFileName, sTempFetchResponse)
             sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
             sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
             sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

             # BECAUSE PLAY TONE AND PROVIDE LOCI - 2025-02-14
             sCmd = simcard_STKCommand_Get(sResAndSW1SW2)
             sPrint = "sResAndSW1SW2: 0x" + str_SpaceHexa(sResAndSW1SW2) + " - Cmd: 0x" + sCmd + " - SW1: " + sSW1 + " - SW2: " + sSW2
             #print(sPrint)
             #log_write(sLogFileName, sPrint)
             
             if simcard_STKCmdIsPlayTone(sCmd) or simcard_STKCmdIsProvideLoci(sCmd):
                #0x20 = PLAY TONE
                #0x26 = PROVIDE LOCI
                
                #sResAndSW1SW2 = simcard_SendOKResponseAnyCmd(cardservice, sCmd, sLogFileName)
                sResAndSW1SW2 = simcard_StatusCommandALLResponses_TerminalResponse(cardservice, sLogFileName, sResAndSW1SW2, True)

          else:
        
             if b9000WithDescription:
                sTemp = simcard_3GPP23048_ResponseAnalisys_Others(sSW1 + sSW2)
                #print("simcard_sendEnvelope - simcard_3GPP23048_ResponseAnalisys_Others = " + str(sTemp))
                if sTemp != "":
                   log_write(sLogFileName, "Response analysis: " + sTemp)
                sResAndSW1SW2 = sTemp   
          
          n = n + 1
          
            
    return sResAndSW1SW2   

# simcard_sendEnvelopePrepareAPDUBigger127 ------------------------------------------------------------------------------------------------------
def simcard_sendEnvelopePrepareAPDUBigger127(sTPDA, sCMD, sTAR=sSimcard_sDefTAR_COTA, sMSL=sSimcard_MSLDefNoSecurity, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter):

    bReturn = True
    
    lstEnvelopes = []
    lstEnvelopesWithMSL = []

    if sTAR=="":
       sTAR = sSimcard_sDefTAR_COTA
    
    sCMD = str_TrimCleanSpaces(sCMD)

    #print("simcard_sendEnvelopePrepareAPDUBigger127 - sCMD: " + str(sCMD))
    
    nCMDLen = (len(sCMD)//2)
    sCMDLen = simcard_GetLengthInHexa(sCMD)
    nRESTO = sSimcard_3GPP23040_MaxAPDULenForSplit

    # 0x0D = 13 bytes. 0x00 = Padding
    sMSL23048 = "0D " + sMSL + sTAR + sCounter + "00"
    nMSLLen = (len(sMSL23048)//2)

    nMSL23048AndCMD = str_TrimCleanSpaces(sMSL23048 + sCMD)
    nMSL23048AndCMDLen = len(nMSL23048AndCMD)//2
    sMSL23048AndCMDLen = bytes_LengthInHexaWithZerosToTheLeft(nMSL23048AndCMDLen, 2)
    
    #sSimcard_3GPP23040_UDH = "027000"
    s3GPP23040_UDH_IEID = sSimcard_3GPP23040_UDH
    sEnvelope = s3GPP23040_UDH_IEID + sMSL23048AndCMDLen + nMSL23048AndCMD
    sEnvelope = str_TrimCleanSpaces(sEnvelope)

    #print("simcard_sendEnvelopePrepareAPDUBigger127 - sEnvelope: " + str(sEnvelope))
    
    # ----------------------------------------------------------------------------------------------------------------------
    sEnvelopeWithMSL = sEnvelope
    
    if str_left(sMSL,2) != "00":
       #print("simcard_sendEnvelopePrepareAPDUBigger127 - sMSL = " + sMSL + " - sEnvelope: " + str(sEnvelope))
       # IT MUST BE PREPARED THE MESSAGE WITH SECURITY ACCORDING TO MSL
       bReturn, sEnvelopeWithMSL = simcard_PrepareAPDUWithSecurity(sEnvelope, sCMD, sTAR, sMSL, sKIC, sKID, sCounter)
       if bReturn == False or bytes_IsCharValidHex(sEnvelopeWithMSL)==False:
          return bReturn, sEnvelope, sEnvelopeWithMSL
       #print("simcard_sendEnvelopePrepareAPDUBigger127 - sMSL = " + sMSL + " - sEnvelopeWithMSL: " + str(sEnvelopeWithMSL))
          
    # ----------------------------------------------------------------------------------------------------------------------

    lstEnvelopes = simcard_sendEnvelopePrepareAPDUBigger127_Process(sTPDA, sEnvelope)
    lstEnvelopesWithMSL = simcard_sendEnvelopePrepareAPDUBigger127_Process(sTPDA, sEnvelopeWithMSL)
    
    return True, lstEnvelopes, lstEnvelopesWithMSL   

# simcard_sendEnvelopePrepareAPDUBigger127_Process ------------------------------------------------------------------------------------------------------
def simcard_sendEnvelopePrepareAPDUBigger127_Process(sTPDA, sEnvelope):

#With MSL 00 00 00 00
#Envelope 1
#80 C2 00 00 AC 
#    D1 81 A9 02 02 83 81 06 04 81 06 01 F5 0B 
#    81 9C 40 05 81 06 01 F4 
#    7F F6 00 00 00 00 00 00 00 8C 
#    07 00 03 01 02 01 70 00 00 CF 
#    0D 00 00 00 00 43 50 41 00 00 00 00 06 00 
#    F1 F0 08 81 BC 00 22 00 A1 00 42 00 69 00 65 00 6E 00 76 00 65 00 6E 00 69 00 64 00 6F 00 20 00 61 00 20 00 45 00 6E 00 74 00 65 00 6C 00 21 00 20 00 56 00 69 00 76 00 65 00 20 00 6C 00 61 00 20 00 6D 00 65 00 6A 00 6F 00 72 00 20 00 65 00 78 00 70 00 65 00 72 00 69 00 65 00 6E 00 63 00 69 00 61 00 2C 00 20 00 54 00 6F 00 64 00 6F 00 20 00 64 00
#SW - 90 00
#Envelope 2
#80 C2 00 00 71 
#    D1 6F 02 02 83 81 06 04 81 06 01 F5 0B 63 40
#    05 81 06 01 F4 
#    7F F6 00 00 00 00 00 00 00 53 05 00 03 01 02 02
#    65 00 73 00 64 00 65 00 20 00 74 00 75 00 20 00 41 00 70 00 70 00 20 00 45 00 6E 00 74 00 65 00 6C 00 2E 00 20 26 3A 00 20 00 A1 00 44 00 65 00 73 00 63 00 E1 00 72 00 67 00 61 00 6C 00 61 00 20 00 79 00 61 00 21 00 22 00 0D 00 0A

#With MSL 02 21 15 15
#Envelope 1
#C - 80 C2 00 00 AC D1 81 A9 02 02 83 81 06 04 81 06 01 F5 0B 81 9C 40 
#    05 81 06 01 F4 
#    7F F6 00 00 00 00 00 00 00 8C 07 00 03 01 
#    02 01 70 00 00 99 15 02 21 15 15 43 50 41 00 00 00 00 02 00
#    5A 7F 1A 80 43 1C 03 01 
#    F6 24 00 82 05 0A 48 6F 72 6F 73 63 6F 70 6F 3A 8F 06 01 41 72 69 65 73 8F 06 02 54 61 75 72 6F 8F 08 03 47 65 6D 69 6E 69 73 8F 07 04 43 61 6E 63 65 72 8F 04 05 4C 65 6F 8F 06 06 56 69 72 67 6F 8F 06 07 4C 69 62 72 61 8F 09 08 45 73 63 6F 72 70 69 6F 8F 0A 09 53 61 67 69 74 61 72 69 6F 8F 0C 0A 43 61 70 72 69 63 6F 72 6E
#Envelope 2
#C - 80 C2 00 00 3B D1 39 02 02 83 81 06 04 81 06 01 F5 0B 2D 40 
#    05 81 06 01 F4 
#    7F F6 00 00 00 00 00 00 00 1D 
#    05 00 03 01 02 02 
#    69 6F 8F 08 0B 41 63 75 61 72 69 6F 8F 07 0C 50 69 73 63 69 73 F6 10
#SW - 91 2F

#SW - 90 00

    lstEnvelopes = []
    
    sMSL23048AndCMD = simcard_APDU_Get3GPP23040(sEnvelope, False, False)
    #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - sMSL23048AndCMD = " + str(sMSL23048AndCMD))
    sMSL23048AndCMD = simcard_APDU_Get3GPP23040(sMSL23048AndCMD, False, False)
    #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - sMSL23048AndCMD = " + str(sMSL23048AndCMD))
    
    sMSL23048AndCMDLen = str_left(sMSL23048AndCMD, 4)
    nMSL23048AndCMDLen = int(bytes_HexaToNro(sMSL23048AndCMDLen))
    
    nRESTO = sSimcard_3GPP23040_MaxAPDULenForSplit
    
    nSMPPTotally = nMSL23048AndCMDLen // nRESTO
    if (nMSL23048AndCMDLen % nRESTO) != 0:
        nSMPPTotally = nSMPPTotally + 1   

    nStart = 0
    nSMPP = 0
    while nSMPP < nSMPPTotally:
          nSMPP = nSMPP + 1
          
          sCMD_SMPP = str_mid(sMSL23048AndCMD, nStart, (nRESTO * 2)).upper()  
          nCMD_SMPP = (len(str_TrimCleanSpaces(sCMD_SMPP))//2)
          nStart = nStart + (nRESTO * 2)

          sEnvelopeAPDU = "80 C2 00 00"
          sEnvelopeAPDU = str_TrimCleanSpaces(sEnvelopeAPDU)
          if sTPDA == "":
             sTPDA = sSimcard_sDefTPDA
                    
          if nSMPP == 1:
             #FIRST SMPP
             #EXAMPLES FOR CMD + HEADER LENGTH: 
             #    7F F6 00 00 00 00 00 00 00 - [NEXT BYTES LENGTH-8C] 07 00 03 01 02 01 70 00 + CPL (COMMAND PACKET LENGTH)-CF
             #    7F F6 00 00 00 00 00 00 00 8C 07 00 03 01 02 01 70 00 00 CF

             #3GPP 23.040 - TP-UDL User Data Header Length: 0x07
             #3GPP 23.040 - IEI - Information Element Identifier: 0x00
             #3GPP 23.048 - IEIDL - Information Element Identifier Data Length: 0x03
             #3GPP 23.048 - IEID - Information Element Identifier Data - Octet 1 Concatenated short message reference number: 0x01
             #3GPP 23.048 - IEID - Information Element Identifier Data - Octet 2 Maximum number of short messages in the concatenated short message: 0x02
             #3GPP 23.048 - IEID - Information Element Identifier Data - Octet 3 Sequence number of the current short message: 0x01
             #3GPP 23.048 - IEIb - CPI - Command Package Identifier: 0x70
             #3GPP 23.048 - IEIDLb - CPI - Command Package Identifier Length: 0x00

             #07 00 03 01 + 01 [Concatenated short message reference number: 0x01] + [TOTAL SMPP] + 01 [Sequence number of the current short message: 0x01] + 70 00 
             sUDH = sSimcard_3GPP23040_UDH_SMPPConcat_First + " 01 " + str(bytes_NroToHexa(nSMPPTotally)) + "01" + " 70 00 "
             #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - sUDH: " + sUDH + " - sMSL23048AndCMDLen = " + str(sMSL23048AndCMDLen))
    
             nUDHL = (len(str_TrimCleanSpaces(sUDH))//2)
             nCMDAndHeaderLen = nUDHL + nCMD_SMPP
             sCMDAndHeaderLen = str(bytes_NroToHexa(nCMDAndHeaderLen)).upper()
             #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - sCMDAndHeaderLen: " + sCMDAndHeaderLen)
     
             #            7F F6 00 00 00 00 00 00 00 + [LEN NEXT BYTES] 8C + 07 00 03 01 02 01 70 + 0D + MSL + TAR + COUNTER + PADDING
             sEnvelope = "7F F6 00 00 00 00 00 00 00 " + sCMDAndHeaderLen + sUDH + sCMD_SMPP
             #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - sEnvelope: " + sEnvelope)
             
             #    81 9C 40 05 81 06 01 F4 
             nCMDAndHeaderLenAndTPDA = len(str_TrimCleanSpaces("40" + sTPDA + sEnvelope))//2 

             #EXAMPLE FOR CMD + HEADER LENGTH + TPDA: 
             #80 C2 00 00 AC 
             #    D1 81 A9 02 02 83 81 06 04 81 06 01 F5 0B 
             #    81 9C 40 05 81 06 01 F4 
             #    7F F6 00 00 00 00 00 00 00 8C 
             #    07 00 03 01 02 01 70 00 00 CF 
             #    0D 00 00 00 00 43 50 41 00 00 00 00 06 00 
             #    F1 F0 08 81 BC 00 22 00 A1 00 42 00 69 00 65 00 6E 00 76 00 65 00 6E 00 69 00 64 00 6F 00 20 00 61 00 20 00 45 00 6E 00 74 00 65 00 6C 00 21 00 20 00 56 00 69 00 76 00 65 00 20 00 6C 00 61 00 20 00 6D 00 65 00 6A 00 6F 00 72 00 20 00 65 00 78 00 70 00 65 00 72 00 69 00 65 00 6E 00 63 00 69 00 61 00 2C 00 20 00 54 00 6F 00 64 00 6F 00 20 00 64 00

             # BECAUSE nCMDAndHeaderLenAndTPDA > 127
             sCMDAndHeaderLenAndTPDA = sSimcard_LengthBiggerThan127 + str(bytes_NroToHexa(nCMDAndHeaderLenAndTPDA)).upper()
             #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - sCMDAndHeaderLenAndTPDA: " + sCMDAndHeaderLenAndTPDA)

             sEnvelopeAPDUHeader = "02 02 83 81 06 " + sSimcard_MSLDefSMSC_TPDA + "0B" + sCMDAndHeaderLenAndTPDA + "40" + sTPDA 
             sEnvelopeAPDUHeader = str_TrimCleanSpaces(sEnvelopeAPDUHeader)
             #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - sEnvelopeAPDUHeader: " + sEnvelopeAPDUHeader)
             
          else:
             # NEXT SMPP
             # 7F F6 00 00 00 00 00 00 00 53 05 00 03 01 02 02
             
             #05 00 03 01
             #3GPP 23.040 - TP-UDL User Data Header Length: 0x05
             #3GPP 23.040 - IEI - Information Element Identifier: 0x00
             #3GPP 23.048 - IEIDL - Information Element Identifier Data Length: 0x03
             #3GPP 23.048 - IEID - Information Element Identifier Data - Octet 1 Concatenated short message reference number: 0x01
             #3GPP 23.048 - IEID - Information Element Identifier Data - Octet 2 Maximum number of short messages in the concatenated short message: 0x02
             #3GPP 23.048 - IEID - Information Element Identifier Data - Octet 3 Sequence number of the current short message: 0x02

             sUDH = "05 00 03 01 " + str(bytes_NroToHexa(nSMPPTotally)) + " " + str(bytes_NroToHexa(nSMPP))
             #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - sUDH: " + sUDH)
             nUDHL = (len(str_TrimCleanSpaces(sUDH))//2)
             nCMDAndHeaderLen = nCMD_SMPP + nUDHL
             sCMDAndHeaderLen = str(bytes_NroToHexa(nCMDAndHeaderLen))
     
             sEnvelope = sCMD_SMPP

             #EXAMPLE FOR CMD + HEADER LENGTH + TPDA: 
             #"39 40 05 81 06 01 F4 7F F6 00 00 00 00 00 00 00 29"
             nCMDAndHeaderLenAndTPDA = nCMDAndHeaderLen + (len(str_TrimCleanSpaces("40" + sTPDA + "7F F6 00 00 00 00 00 00 00 "))//2) + 1
             sCMDAndHeaderLenAndTPDA = str(bytes_NroToHexa(nCMDAndHeaderLenAndTPDA))

             sEnvelopeAPDUHeader = "02 02 83 81 06 " + sSimcard_MSLDefSMSC_TPDA + "0B" + sCMDAndHeaderLenAndTPDA + "40" + sTPDA + "7F F6 00 00 00 00 00 00 00 "
             sEnvelopeAPDUHeader = sEnvelopeAPDUHeader + sCMDAndHeaderLen + sUDH
             sEnvelopeAPDUHeader = str_TrimCleanSpaces(sEnvelopeAPDUHeader)

          sEnvelope = sEnvelopeAPDUHeader + sEnvelope
          #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - 1:" + sEnvelope)
          sEnvelopeLen = simcard_GetLengthInHexaBiggerThan127(sEnvelope)
          #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - 1 sEnvelopeLen:" + sEnvelopeLen)
          sEnvelope = sSimcard_BERTLV_SMPP_download_tag + sEnvelopeLen + sEnvelope
          #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - 2:" + sEnvelope)
          sEnvelopeLen = simcard_GetLengthInHexa(sEnvelope)
          sEnvelope = sEnvelopeAPDU + sEnvelopeLen + sEnvelope
          #print("simcard_sendEnvelopePrepareAPDUBigger127_Process - 3:" + sEnvelope)
          sEnvelope = sEnvelope.upper()
    
          lstEnvelopes.append(str_TrimCleanSpaces(sEnvelope))
    
    return lstEnvelopes

# simcard_GetLengthInHexa ------------------------------------------------------------------------------------------------------
def simcard_GetLengthInHexa(sBytes):
    sBytes = str_TrimCleanSpaces(sBytes)
    nBytesLen = (len(sBytes)//2)
    sBytesLen = bytes_NroToHexa(nBytesLen)
    return sBytesLen

# simcard_LengthDescription ------------------------------------------------------------------------------------------------------
def simcard_LengthDescription(sBytes):
    return simcard_DescriptionLength(sBytes)
    
# simcard_DescriptionLength ------------------------------------------------------------------------------------------------------
def simcard_DescriptionLength(sBytes):
    sBytes = str_TrimCleanSpaces(sBytes)
    sReturn = "Length = " + str(len(sBytes)//2)
    sReturn = sReturn + " bytes ( Hexa 0x" + simcard_GetLengthInHexa(sBytes) + " )"
    return sReturn

# simcard_GetLengthInHexaBiggerThan127 ------------------------------------------------------------------------------------------------------
def simcard_GetLengthInHexaBiggerThan127(sBytes):
    sBytes = str_TrimCleanSpaces(sBytes)
    nBytesLen = (len(sBytes)//2)
    sPrevious = ""
    if nBytesLen > 127:
       #nBytesLen = nBytesLen + 1
       #ADDED BECAUSE IT IS BIGGER THAN 0x7F (127)
       sPrevious = sSimcard_LengthBiggerThan127
    sBytesLen = sPrevious + bytes_NroToHexa(nBytesLen)
    return sBytesLen

# simcard_DisplayTextCmd_GetText ------------------------------------------------------------------------------------------------------
def simcard_DisplayTextCmd_GetText(sLogFileName, sBytes):
    
    # Before with High Priority
    # sDT_CMD = "81 03 01 21 81 82 02 81 02 8D"
    # with Normal Priority
    # sDT_CMD = "81 03 01 21 80 82 02 81 02 8D"
    if len(sBytes) <= 4:
       return '' 
    sDT_CMD = "81 03 01 21"
    sDT_CMDRest = "82 02 81 02 8D"

    sBytes = str_TrimCleanSpaces(sBytes)
    sDT_CMD = str_TrimCleanSpaces(sDT_CMD)
    #print(sBytes)
    #print(sDT_CMD)

    #GETTING DT PRIORITY + DESTINATION + LENGTH + DCS + TEXT
    sDT_Text = str_getSubStringFromOcur(sBytes, str_TrimCleanSpaces(sDT_CMD),1)
    
    nStart = 0
    sDT_Priority = sDT_Text[nStart:2+nStart]
    nStart = nStart + 2
    nStart = nStart + len(str_TrimCleanSpaces(sDT_CMDRest))

    #print("sDT_Priority: " + sDT_Priority)
    
    #GETTING DT LENGTH + DCS + TEXT
    sDT_Text = str_getSubStringFromOcur(sBytes, str_TrimCleanSpaces(sDT_CMDRest),1)
    
    nStart = 0
    if (len(sDT_Text)//2) > 127:
       nStart = 2

    #print("sDT_Text: " + sDT_Text)
    
    sDT_LenTotal = sDT_Text[nStart:2+nStart]

    # We turn the sDT_LenTotal from hexa to num
    # Then, we turn it into an integer, as the function returns it as a string
    # Then, we substract 1 byte (the one that represents the data coding scheme)
    # Finally we multiply it by 2 to represent the value in characters
    nDT_LenTotalChars = (int(bytes_HexaToNro(sDT_LenTotal))-1)*2
    #print("sDT_LenTotal: " + sDT_LenTotal)
    sDT_DCS = str_mid(sDT_Text, 2+nStart, 2)
    #print("sDT_DCS: " + sDT_DCS)
    sDT_Text = str_midToEnd(sDT_Text, 4+nStart)
    #print("sDT_Text: " + sDT_Text)

    #REMOVING 90 00
    sDT_Text = simcard_RemoveSW1SW2(sDT_Text)
    # Here we make sure we only get the characters in the Display Text
    sDT_Text = sDT_Text[0:nDT_LenTotalChars]
    # sDT_Text = sDT_Text[0:nDT_LenTotal]

    # REMOVING THE LAST BYTE BECAUSE OF 0x81 WHEN IT IS BIGGER THAN 127 BYTES
    if nStart > 0:
       sDT_Text = str_left(sDT_Text, len(sDT_Text))
    
    log_write(sLogFileName, "Text Length: 0x" + sDT_LenTotal + " (decimal: " + str(bytes_HexaToNro(sDT_LenTotal)) + ")")
    log_write(sLogFileName, "Text DCS: 0x" + sDT_DCS)
    log_write(sLogFileName, "Display Text Priority: 0x" + sDT_Priority)
    
    return sDT_Text
    
# simcard_CmdDisplayText_SendUserResponse ------------------------------------------------------------------------------------------------------
def simcard_CmdDisplayText_SendUserResponse(cardservice, sLogFileName, sUserResponse):
    return simcard_STKCmd_SendUserResponse(cardservice, sLogFileName, "21", sUserResponse)

# simcard_CmdLaunchBrowser_SendUserResponse ------------------------------------------------------------------------------------------------------
def simcard_CmdLaunchBrowser_SendUserResponse(cardservice, sLogFileName):
    return simcard_STKCmd_SendUserResponse(cardservice, sLogFileName, "15", "00")

# ----------------------------------
# simcard_STKCmd_SendUserResponse ------------------------------------------------------------------------------------------------------
def simcard_CmdSTKtoAnalyze(cardservice, sLogFileName, sCmd, sUserResponse):
    lGeneralResponsestoAnalyze = []
    if sCmd=="":
       return ""
       
    sDT_CMDResponse = "80 14 00 00 0C 01 03 01 " + sCmd + " 00 02 02 82 81 03 01"

    sResponse = simcard_STKCmdResponseGetDesFromASCII(sUserResponse)
       
    sDT_CMDResponse = sDT_CMDResponse + sResponse
    #print("sDT_CMDResponse: " + sDT_CMDResponse)
    
    sResAndSW1SW2 = simcard_Response(cardservice, sDT_CMDResponse, sLogFileName)   
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
    # Append into list for analyze
    lGeneralResponsestoAnalyze.append([sDT_CMDResponse, sSW1, sSW2])

    # FETCH RESPONSE FROM ENVELOPE
    if sSW1 == '91' and sSW2!="00":
        sFETCH_RESPONSE = "80 12 00 00"
        log_write(sLogFileName, "FETCH RESPONSE FROM CMD " + sCmd + " ANSWER: " + str(sUserResponse))
        sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
        log_write(sLogFileName, sTempFetchResponse)
        sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
         # Append into list for analyze
        lGeneralResponsestoAnalyze.append([sResAndSW1SW2, sSW1, sSW2])
    
    return lGeneralResponsestoAnalyze   
# ----------------------------------

# simcard_STKCmd_SendUserResponse ------------------------------------------------------------------------------------------------------
def simcard_STKCmd_SendUserResponse(cardservice, sLogFileName, sCmd, sUserResponse):

    if sCmd=="":
       return ""
       
    sDT_CMDResponse = "80 14 00 00 0C 01 03 01 " + sCmd + " 00 02 02 82 81 03 01"

    sResponse = "00"
    sResponse = simcard_STKCmdResponseGetDesFromASCII(sUserResponse)
       
    sDT_CMDResponse = sDT_CMDResponse + sResponse
    sResAndSW1SW2 = simcard_Response(cardservice, sDT_CMDResponse, sLogFileName)   
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    # FETCH RESPONSE FROM ENVELOPE
    if sSW1 == '91' and sSW2!="00":
        sFETCH_RESPONSE = "80 12 00 00"
        log_write(sLogFileName, "FETCH RESPONSE FROM CMD " + sCmd + " ANSWER: " + sUserResponse)
        sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
        log_write(sLogFileName, sTempFetchResponse)
        sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
    
    return sResAndSW1SW2       
    
# simcard_STKCmd_SendUserResponse ------------------------------------------------------------------------------------------------------
def simcard_STKCmd_SendUserResponse(cardservice, sLogFileName, sCmd, sUserResponse):

    if sCmd=="":
       return ""
       
    sDT_CMDResponse = "80 14 00 00 0C 01 03 01 " + sCmd + " 00 02 02 82 81 03 01"

    sResponse = "00"
    sResponse = simcard_STKCmdResponseGetDesFromASCII(sUserResponse)
       
    sDT_CMDResponse = sDT_CMDResponse + sResponse
    sResAndSW1SW2 = simcard_Response(cardservice, sDT_CMDResponse, sLogFileName)   
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    # FETCH RESPONSE FROM ENVELOPE
    if sSW1 == '91' and sSW2!="00":
        sFETCH_RESPONSE = "80 12 00 00"
        log_write(sLogFileName, "FETCH RESPONSE FROM CMD " + sCmd + " ANSWER: " + sUserResponse)
        sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
        log_write(sLogFileName, sTempFetchResponse)
        sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
    
    return sResAndSW1SW2       

# simcard_SendOKResponseAnyCmd ------------------------------------------------------------------------------------------------------
def simcard_SendOKResponseAnyCmd(cardservice, sCmd, sLogFileName):

    if sCmd=="":
       return ""
       
    sDT_CMDResponse = str_SpacesOut("80 14 00 00 0C 01 03 01 " + sCmd + " 00 02 02 82 81 03 01 00")
    sResAndSW1SW2 = simcard_Response(cardservice, sDT_CMDResponse, sLogFileName)   
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    # FETCH RESPONSE FROM ENVELOPE
    if sSW1 == '91' and sSW2!="00":
        sFETCH_RESPONSE = "80 12 00 00"
        log_write(sLogFileName, "FETCH RESPONSE FROM CMD " + sCmd)
        sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
        log_write(sLogFileName, sTempFetchResponse)
        sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
    
    return sResAndSW1SW2       

# simcard_SendSMSCmd_Process ------------------------------------------------------------------------------------------------------
def simcard_SendSMSCmd_Process(sLogFileName, sSendSMS):
    return simcard_SendSMSCmd_Get(sLogFileName, sSendSMS, False)

# simcard_SendSMSCmd_GetInterpretation ------------------------------------------------------------------------------------------------------
def simcard_SendSMSCmd_GetInterpretation(sLogFileName, sBytecode):
    return simcard_SendSMSCmd_Process(sLogFileName, sBytecode)

# simcard_SendSMSCmd_GetData ------------------------------------------------------------------------------------------------------
def simcard_SendSMSCmd_GetData(sLogFileName, sSendSMS):
    return simcard_SendSMSCmd_Get(sLogFileName, sSendSMS, True)

# simcard_SendSMSCmd_Get ------------------------------------------------------------------------------------------------------
def simcard_SendSMSCmd_Get(sLogFileName, sSendSMS, bGetData):
    
    if sSendSMS == "":
       return ""
       
    tLog = simcard_SendSMSCmd_Interpret(sSendSMS)
    #print("tLog: " + str(tLog[0]))
    if len(tLog) > 1:
       sLog = tLog[0]
       sData = tLog[1]
    else:
       return str(tLog[0])
       
    #if sLogFileName != "":
    #   log_write(sLogFileName, sLog)

    if bGetData:
       return sData
    else:
       return sLog

# simcard_IsSTKProactiveCmdValid ------------------------------------------------------------------------------------------------------
def simcard_IsSTKProactiveCmdValid(sBytecode):
    
    sBytecode = str_SpacesOut(sBytecode)
    
    if sBytecode=="":
       return False
    
    if bytes_IsHexaValid(sBytecode)==False:
       return False
       
    #Check that it is a proactive command BER-TLV tags: 0xD0 - SIM TO ME direction - Proactive SIM command tag
    if str_left(sBytecode,2) != sSimcard_BERTV_SIMtoME:
       return False
    
    #Example Send SMS: D0 17 81 03 01 13 00 82 02 81 83 0B 0C 05 00 05 81 06 01 F4 00 04 02 30 12
    #Command details TAG Value: 0x81
    #Command details TAG Value Length: 0x03
    #Command Number: 0x01
    #Command Type: 0x13 - SEND SHORT MESSAGE
    
    n = 4
    #print("str_mid(sBytecode, n, len(sProactiveCommandPattern)) = " + str(str_mid(sBytecode, n, len(sProactiveCommandPattern))))
    
    if str_mid(sBytecode, n, len(sProactiveCommandPattern)) != sProactiveCommandPattern:
       n = n + 2

       if str_mid(sBytecode, n, len(sProactiveCommandPattern)) != sProactiveCommandPattern:          
          # Taking into account Proactive Commands with length bigger than 127 bytes => D0 81 80 81 03 01...
          
          #print("str_mid(sBytecode, n, len(sProactiveCommandPattern)) = " + str(str_mid(sBytecode, n, len(sProactiveCommandPattern))))
          # Example = "D0 81 A9 81 03 01 21 81 82 02 81 02 8D 81 99 08 27 28 00 20 00 42 00 65 00 6D 00 2D 00 76 00 69 00 6E 00 64 00 6F 00 20 00 E0 00 20 00 72 00 65 00 64 00 65 00 20 00 4F 00 70 00 65 00 72 00 61 00 64 00 6F 00 72 00 2E 00 20 00 56 00 6F 00 63 00 EA 00 20 00 71 00 75 00 65 00 72 00 20 00 6D 00 65 00 6C 00 68 00 6F 00 72 00 61 00 72 00 20 00 6F 00 20 00 73 00 75 00 61 00 20 00 65 00 78 00 70 00 65 00 72 00 69 00 EA 00 6E 00 63 00 69 00 61 00 20 00 63 00 6F 00 6E 00 6F 00 73 00 63 00 6F 00 3F 00 20 27 0B 04 02 00 02 90 00"
          
          return False
       
    return True

# simcard_SendSMSCmd_Interpret_GetTPDA ------------------------------------------------------------------------------------------------------
def simcard_SendSMSCmd_Interpret_GetTPDA(sSendSMSBytecode):
    sSendSMS = str_TrimCleanSpaces(sSendSMSBytecode)
    
    if str_left(sSendSMS,len(sSimcard_9000)) == sSimcard_9000:
       sSendSMS = str_midToEnd(sSendSMS, len(sSimcard_9000))
    
    #Address tag: 0x06
    #Address tag length + value: 0x04 81 06 01 F5 - TPDA Number Bytes: 0x04 - Decimal: 4 bytes
    sTPDA_SMSC = ""
    if "06" in sSendSMS:
       sSendSMS_t = str_getSubStringFromOcur(sSendSMS, "06", 1)
       nStart = 0
       sTPDA_SMSC = simcard_GetTPDAHexa(sSendSMS_t, nStart, False)

       #print("simcard_SendSMSCmd_Interpret_GetTPDA - sSendSMS = " + str(sSendSMS))
       #print("simcard_SendSMSCmd_Interpret_GetTPDA - sTPDA_SMSC = " + str(sTPDA_SMSC))

       if len(sTPDA_SMSC) < 8:
          sTPDA_SMSC = ""

       #print("simcard_SendSMSCmd_Interpret_GetTPDA - sTPDA_SMSC = " + str(sTPDA_SMSC))
    
    #3GPP 51.014 SMS TPDU tag: 0x8B or 0x0B
    sTPDA_TP_Message_Reference = ""
    if "8B" in sSendSMS or "0B" in sSendSMS:

       if "8B" in sSendSMS:
          sSendSMS_t = str_getSubStringFromOcurAfterFirstOnly(sSendSMS, "8B")
       else:   
          #0xD0 16 81 03 01 13 00 82 02 81 83 0B 0B 05 00 05 81 06 01 F4 00 04 01 31
          sSendSMS_t = str_getSubStringFromOcurAfterFirstOnly(sSendSMS, "0B")

       # NEXT BYTES ARE:
       # 3GPP 51.014 SMS TPDU Length
       # SMS TPDU tp-mti (TP-Message Type Indicator): 0x05
       # SMS TPDU - tp-mr (TP-Message Reference): 0x00 - Decimal: 0
       nStart = 6

       if str_left(sSendSMS_t, 2) == sSimcard_LengthBiggerThan127:
          # Because length is bigger than 127 bytes
          nStart = nStart + 2
       sTPDA_TP_Message_Reference = simcard_GetTPDAHexa(sSendSMS_t, nStart)

       #print("simcard_SendSMSCmd_Interpret_GetTPDA - sTPDA_TP_Message_Reference = " + str(sTPDA_TP_Message_Reference))
    
    sTPDA = sTPDA_TP_Message_Reference
    if sTPDA == "":
       sTPDA = sTPDA_SMSC
    
    # TPDA must be Len + TON/NPI + 2 bytes minimum => 4 bytes. Example: 04 81 21 43 where TPDA is 1234
    if len(sTPDA) < 8:
       sTPDA = ""
       
    return sTPDA

# simcard_SendSMSCmd_Interpret_GetTPDA_Exact ------------------------------------------------------------------------------------------------------
def simcard_SendSMSCmd_Interpret_GetTPDA_ExactNextBytes(sSendSMSBytecode, sTPDA):
    sSendSMS = str_TrimCleanSpaces(sSendSMSBytecode)
    nTokensTPDA = str_CountPattern(sSendSMS, sTPDA)
    
    sReturn = ""
    
    if nTokensTPDA > 1:
       sTemp = str_getSubStringFromOcur(sSendSMS, sTPDA, 0)
       sReturn = str_midToEnd(sSendSMS, len(sTemp) + len(sTPDA))
       
    else:
       sReturn = str_getSubStringFromOcurLast(sSendSMS, sTPDA)

    #print("simcard_SendSMSCmd_Interpret_GetTPDA_ExactNextBytes - sReturn: " + str(sReturn))
    
    return sReturn   


# simcard_SendSMSCmd_Interpret_GetPID ------------------------------------------------------------------------------------------------------
def simcard_SendSMSCmd_Interpret_GetPID(sSendSMSBytecode):
    sSendSMS = str_TrimCleanSpaces(sSendSMSBytecode)
    sTPDA = simcard_SendSMSCmd_Interpret_GetTPDA(sSendSMSBytecode)
    
    if sTPDA == "":
       return ""
    
    sTemp = simcard_SendSMSCmd_Interpret_GetTPDA_ExactNextBytes(sSendSMS, sTPDA)
    
    sPID = ""
    if len(sTemp)>=2:
       n = 0     
       sPID = sTemp[n:n+2]
    return sPID

# simcard_SendSMSCmd_Interpret_GetDCS ------------------------------------------------------------------------------------------------------
def simcard_SendSMSCmd_Interpret_GetDCS(sSendSMSBytecode):
    sSendSMS = str_TrimCleanSpaces(sSendSMSBytecode)
    sTPDA = simcard_SendSMSCmd_Interpret_GetTPDA(sSendSMSBytecode)

    if sTPDA == "":
       return ""

    sTemp = simcard_SendSMSCmd_Interpret_GetTPDA_ExactNextBytes(sSendSMS, sTPDA)

    sDCS = ""
    if len(sTemp) >= 4:
       n = 2     
       sDCS = sTemp[n:n+2]
    return sDCS

# simcard_SendSMSCmd_Interpret_GetTPUD ------------------------------------------------------------------------------------------------------
def simcard_SendSMSCmd_Interpret_GetTPUD(sSendSMSBytecode):
    sSendSMS = str_TrimCleanSpaces(sSendSMSBytecode)
    sTPDA = simcard_SendSMSCmd_Interpret_GetTPDA(sSendSMSBytecode)
    #print("simcard_SendSMSCmd_Interpret_GetTPUD - sTPDA = " + str(sTPDA) + " - len=" + str(len(sTPDA)))
    
    if sTPDA == "":
       return ""
       
    #print("simcard_SendSMSCmd_Interpret_GetTPUD - sSendSMS = " + str(sSendSMS) + " - len=" + str(len(sSendSMS)))
    sTemp = simcard_SendSMSCmd_Interpret_GetTPDA_ExactNextBytes(sSendSMS, sTPDA)
    #print("simcard_SendSMSCmd_Interpret_GetTPUD - sTemp = " + str(sTemp) + " - len= " + str(len(sTemp)))
    
    sSMS = ""
    if len(sTemp) >= 8:
       n = 4     
       sSMSLen = sTemp[n:n+2]
       n = n + 2
       sSMS = sTemp[n:]
       
    #print("simcard_SendSMSCmd_Interpret_GetTPUD - sSMS = " + str(sSMS) + " - len= " + str(len(sSMS)))
    return sSMS 

# simcard_SendSMSCmd_Interpret ------------------------------------------------------------------------------------------------------
def simcard_SendSMSCmd_Interpret(sSendSMSBytecode):
    #DATA: D0 17 81 03 01 13 00 82 02 81 83 0B 0C 05 00 05 81 06 01 F4 00 04 02 30 12
    
    if sSendSMSBytecode == "":
       return "", ""
    
    #print("simcard_SendSMSCmd_Interpret: sSendSMSBytecode = " + str(sSendSMSBytecode))
    
    sSendSMS = str_TrimCleanSpaces(sSendSMSBytecode)
    #print("simcard_SendSMSCmd_Interpret: sSMS 1 = " + str(sSendSMS))
    #sSendSMS = bytes_RemoveLast2bytes(sSendSMS)


    #print("sSendSMS: " + str(sSendSMS))
    
    if str_left(sSendSMS,len(sSimcard_9000)) == sSimcard_9000:
       sSendSMS = str_midToEnd(sSendSMS, len(sSimcard_9000))
   
    sCmd = simcard_STKCommand_Get(sSendSMS)
    
    sLog = simcard_STKCmdGetDes(sCmd, True)
    #print("simcard_SendSMSCmd_Interpret: sLog = " + str(sLog) + " - sCmd = " + str(sCmd))
    
    if sCmd != simcard_STKCmdGetCmdSendSMS():
        return sLog, ""
        
    #sTPDA = simcard_GetTPDAHexa(sSendSMS, 30)
    sTPDA = simcard_SendSMSCmd_Interpret_GetTPDA(sSendSMSBytecode)
    
    #print("simcard_SendSMSCmd_Interpret_GetTPDA = " + str(simcard_SendSMSCmd_Interpret_GetTPDA(sSendSMSBytecode)))
    #print("simcard_SendSMSCmd_Interpret_GetPID = " + str(simcard_SendSMSCmd_Interpret_GetPID(sSendSMSBytecode)))
    #print("simcard_SendSMSCmd_Interpret_GetDCS = " + str(simcard_SendSMSCmd_Interpret_GetDCS(sSendSMSBytecode)))
    #print("simcard_SendSMSCmd_Interpret_GetTPUD = " + str(simcard_SendSMSCmd_Interpret_GetTPUD(sSendSMSBytecode)))
    #print("simcard_IsSTKProactiveCmdValid = " + str(simcard_IsSTKProactiveCmdValid(sSendSMSBytecode)))
       
    #print(sTPDA)
    sTemp = simcard_SendSMSCmd_Interpret_GetTPDA_ExactNextBytes(sSendSMS, sTPDA)
    #print("sTemp: " + str(sTemp))
    n = 0     
    sPID = sTemp[n:n+2]
    n = n + 2
    sDCS = sTemp[n:n+2]
    n = n + 2

    sSMSLen = sTemp[n:n+2]
    n = n + 2
    if sSMSLen == "01" and "0270" in sTemp[n:]:
       sSMSLen = sTemp[n:n+2]
       n = n + 2 

    sSMS = sTemp[n:]

    #sSeparaField = " - "
    sSeparaField = "\n"
    
    sLog = sLog + sSeparaField + sSimcard_SendSMSTPDAPattern + str_AddSpaceHexa(sTPDA) 
    sTPDA_Int = simcard_TPDAHexaInterpret(sTPDA)
    if sTPDA_Int != "":
       sLog = sLog + " (interpreted: " + sTPDA_Int + ")"
       
    sLog = sLog + sSeparaField + "Protocol ID: 0x" + sPID
    sLog = sLog + sSeparaField + "Data Coding Scheme (DCS): 0x" + sDCS
    sLog = sLog + sSeparaField + "SMS Length: 0x" + sSMSLen 
    sLog = sLog + " (decimal: " + str(bytes_NumberFromHex(sSMSLen)) + ")"
    
    bIsResponseForPoR, sSMSData, sDataASCII = simcard_SendSMSCmd_InterpretData_IsResponseForPoR(sSMS)

    sLog = sLog + sSeparaField + sSMSData
       
    #if str_instrBool(sDataASCII, sSimcard_sDefTAR_COTA_Name):
    sTAR = simcard_processTAR_IsInSMSSiprocalAppletReference(sDataASCII)
    sData = ""
    
    if sTAR != "":
       
       sData = COTA_processSMS(sSMS, sTAR)
       if sData != "":
          sLog = sLog + sSeparaField + sData

    return sLog, sData

# simcard_SendSMSCmd_InterpretData_IsResponseForPoR ------------------------------------------------------------------------------------------------------
def simcard_SendSMSCmd_InterpretData_IsResponseForPoR(sSMSData):

    sSMS = str_TrimCleanSpaces(sSMSData)
    sData = str_AddSpaceHexa(sSMS)
    sDataASCII = bytes_HexaToASCII(sSMS)
    sSMSData = sSimcard_SendSMSDATAPattern + sData + " " + sSimcard_SendSMSDATAPatternASCII + " " + sDataASCII

    # 3GPP 23.048 RESPONSE FOR MSL WITH SPI2
    # sSimcard_SMSAnswerForSPI2Request_Pattern = "027100"
    #if sSimcard_SMSAnswerForSPI2Request_Pattern in sSMS and len(sSMS) > 18: 
    if simcard_IfInSMS_sSimcard_SMSAnswerForSPI2Request_Pattern(sSMS):
    
       sPoRDes, sTAR, sPoR = simcard_3GPP23048_ResponseAnalisys_GetPoRAndTAR(sSMS)
       
       if sTAR != "":
          sSMSData = sSMSData + " " + sSimcard_ResponseForTAR + " = " + str_AddSpaceHexa(sTAR)
       if sPoRDes != "":
          sSMSData = sSMSData + " => PoR: " + sPoRDes
          
       return True, sSMSData, sDataASCII
       
    else:
       return False, sSMSData, sDataASCII
    
# simcard_STKCommand_Get ------------------------------------------------------------------------------------------------------
def simcard_STKCommand_Get(sSTKCommand):
    #DATA: D0 17 81 03 01 13 00 82 02 81 83 0B 0C 05 00 05 81 06 01 F4 00 04 02 30 12
    #DATA: D0 81 97 81 03 01 13 00 82 02 81 83 05 00 06 04 81 06 01 F5 8B 81 83 41 00 05 81 06 01 F4 00 F6 79 02 71 00 00 74 0A 00 00 00 00 00 00 00 01 00 00 01 90 00 66 64 73 62 06 07 2A 86 48 86 FC 6B 01 60 0B 06 09 2A 86 48 86 FC 6B 02 02 02 63 09 06 07 2A 86 48 86 FC 6B 03 64 0B 06 09 2A 86 48 86 FC 6B 04 02 55 64 0B 06 09 2A 86 48 86 FC 6B 04 80 00 64 0B 06 09 2A 86 48 86 FC 6B 04 81 07 65 0A 06 08 2A 86 48 86 FC 6B 05 04 66 0C 06 0A 2B 06 01 04 01 2A 02 6E 01 02
    
    sSTKCommand = str_TrimCleanSpaces(sSTKCommand)
    
    sCmd = ""
    
    if sSTKCommand != "":
       nSTKCommandLen = len(sSTKCommand)

       nStart = 10
       if str_mid(sSTKCommand, 2, 2) == sSimcard_LengthBiggerThan127:
          #0x81 because the APDU size is bigger than 127 bytes
          nStart = nStart + 2
    
       if nSTKCommandLen > (nStart + 2):
          sCmd = str_mid(sSTKCommand,nStart,2)          
    
    sCmd = str(str_TrimCleanSpaces(sCmd))
    return sCmd

# simcard_GetTPDAHexa ------------------------------------------------------------------------------------------------------
def simcard_GetTPDAHexa(sValue, nPosFromTPDA, bFirstByteIsDigits=True):
    sTPDA = str_midToEnd(sValue, nPosFromTPDA)
    sTPDALen = str_left(sTPDA,2)
    
    nTPDALen = bytes_NumberFromHex(sTPDALen)
    #According standard, maximum is 24 digits for TPDA.
    nMaxDigitsForTPDA = 24
    if nTPDALen > nMaxDigitsForTPDA:
       return ""

    if bFirstByteIsDigits:
       # Example: 0x05 81 21 43 F5
       nTPDALenT = nTPDALen // 2
      
       #print("simcard_GetTPDAHexa - nTPDALenT=" + str(nTPDALenT))
       if bFirstByteIsDigits and nTPDALen % 2 != 0:
          nTPDALenT = nTPDALenT + 1

       #print("simcard_GetTPDAHexa - nTPDALenT= " + str(nTPDALenT))
       #TPDA LEN + TON/NPI
       nTPDALenT = nTPDALenT + 2   
       sTPDA = str_left(sTPDA,(nTPDALenT * 2))
      
    else:   
       # Example: 0x05 81 21 43 65 87
       sTPDA = str_left(sTPDA,((nTPDALen + 1) * 2))
    
    #print("simcard_GetTPDAHexa - sTPDA= " + str(sTPDA) + " - bFirstByteIsDigits=" + str(bFirstByteIsDigits))
    return sTPDA

# simcard_TPDAHexaInterpret ------------------------------------------------------------------------------------------------------
def simcard_TPDAHexaInterpret(sValue):
    sValue = str_SpacesOut(sValue)
    sTPDA = ""
    if len(sValue) > 4:
       sTPDA = str_reverse(str_midToEnd(sValue, 4))
       if str_mid(sValue,2,1) == "9":
          sTPDA = "+" + sTPDA     

       #print("simcard_TPDAHexaInterpret - sTPDA: " + sTPDA)
       
       if str_right(sTPDA, 1) == "F":
          sTPDA = str_left(sTPDA, len(sTPDA)-1)
          
    return sTPDA
    
# simcard_DF_EF_Select ------------------------------------------------------------------------------------------------------
def simcard_DF_EF_Select(cardservice, sLogFileName, sDF_EF):

    if sDF_EF=="":
       return ""
       
    sSELECT = "00 A4 00 04 02 " + sDF_EF
    sGET_RESPONSE = "00 C0 00 00"
    
    sResAndSW1SW2 = simcard_Response(cardservice, sSELECT, sLogFileName)   
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    # FETCH RESPONSE FROM ENVELOPE
    if sSW1 == '9F' or sSW1 == '61':
        log_write(sLogFileName, "GET RESPONSE FROM SELECT " + sSELECT)
        sTempFetchResponse = sGET_RESPONSE + " " + sSW2
        log_write(sLogFileName, sTempFetchResponse)
        sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    sName = simcard_SelectEF_GetFileName(sResAndSW1SW2)
    sSize = simcard_SelectEF_GetSize(sResAndSW1SW2)
    sLog = "SELECT DF/FILE: " + sName
    if len(sSize) > 4:
       sRecSize = sSize[4:6].upper()
       sRecs =  sSize[6:].upper()
       sLog = sLog + " - Length (bytes): 0x"
       sLog = sLog + sSize[:4].upper()
       sLog = sLog + " -  Record Size: 0x" + sRecSize + " (decimal: " + bytes_HexaToNro(sRecSize) + ")"
       sLog = sLog + " -  Records: 0x" + sRecs + " (decimal: " + bytes_HexaToNro(sRecs) + ")"
    else:
       sLog = " - Length (bytes): 0x"
       sLog = sLog + sSize
         
    log_write(sLogFileName, sLog)
    
    return sResAndSW1SW2       

# simcard_ReadBinary ------------------------------------------------------------------------------------------------------
def simcard_ReadBinary(cardservice, sLogFileName, nBytesDecimal):

    if valid_nro_int(nBytesDecimal) == False:
       sBytesHex = str(nBytesDecimal)
    else:
       if int(nBytesDecimal)<=0:
          return ""
       sBytesHex = bytes_NroToHexa(int(nBytesDecimal))   
       
    sREAD_BINARY = "00 B0 00 00 " + sBytesHex
    
    sResAndSW1SW2 = simcard_Response(cardservice, sREAD_BINARY, sLogFileName)   
    log_write(sLogFileName, "READ BINARY: " + sREAD_BINARY)
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    return sResAndSW1SW2       

# simcard_ReadRecord ------------------------------------------------------------------------------------------------------
def simcard_ReadRecord(cardservice, sLogFileName, nRec):

    print(str(nRec))
    
    if valid_nro_int(nRec) == False:
       sRecHex = str(nRec)
    else:
       if int(nRec)<=0:
          return ""
       sRecHex = bytes_NroToHexa(int(nRec))   
       
    sREAD_RECORD = "00 B2 " + sRecHex + " 04 "
    
    sResAndSW1SW2 = simcard_Response(cardservice, sREAD_RECORD + "00", sLogFileName)   
    log_write(sLogFileName, "READ RECORD 0x" + sRecHex + " : " + sREAD_RECORD + "00")
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
    
    if sSW1.upper() == '6C' or sSW1.upper() == '61':
       # ETSI 102.221
       # 7.3.1.1.5 Use of procedure bytes '61xx' and '6Cxx'
        log_write(sLogFileName, "READ RECORD 0x" + sRecHex + " twice because of 0x" + sSW1 + ": " + sREAD_RECORD + sSW2)
        sResAndSW1SW2 = simcard_Response(cardservice, sREAD_RECORD + sSW2, sLogFileName)   

    return sResAndSW1SW2       

# simcard_ReadRecordsALL ------------------------------------------------------------------------------------------------------
def simcard_ReadRecordsALL(cardservice, sLogFileName, nMaxRecs):
    nMaxRec = 0
    if valid_nro_int(nMaxRecs) == False:
       nMaxRec = bytes_HexaToNro(nMaxRecs)   
    else:   
       nMaxRec = int(nMaxRecs)
    
    #print("MAX RECS: " + str(nMaxRec))
    sRet = ""
    #READ ALL RECORDS
    i = 1
    while i <= nMaxRec:
          sRet = sRet + simcard_ReadRecord(cardservice, sLogFileName, i)
          print(sRet)
          i += 1

    return sRet      

# simcard_EF_ICCID_GET ------------------------------------------------------------------------------------------------------
def simcard_EF_ICCID_GET(cardservice, sLogFileName):
    sICCID = "2F E2"
    sRes = simcard_DF_EF_Select(cardservice, sLogFileName, sICCID)
    sName = simcard_SelectEF_GetFileName(sRes)
    sSize = simcard_SelectEF_GetSize(sRes)
    nSize = bytes_HexaToNro(sSize)
    sValue = simcard_ReadBinary(cardservice, sLogFileName, nSize)
    
    sValue = simcard_RemoveSW1SW2(sValue)
    sLog = simcard_EF_ICCID_Interpret(sValue, True)
    sICCIDInterp = simcard_EF_ICCID_Interpret(sValue, False)
    log_write(sLogFileName, sLog)
    
    return sICCIDInterp

# simcard_EF_ICCID_Interpret ------------------------------------------------------------------------------------------------------
def simcard_EF_ICCID_Interpret(sHexa, bAddDes):
    sICCIDInterp = str_reverse(str_TrimCleanSpaces(sHexa))
    sLuhn = str_right(sICCIDInterp, 2)
    
    if bAddDes:
       sICCIDInterp = "ICCID Value: 0x" + str_SpaceHexa(sHexa) + " - Length = " + str(len(sHexa)//2) + " bytes - interpreted: " + sICCIDInterp
       if str_right(sLuhn, 1) != "F" or str_left(sLuhn,1) != "F":
          sICCIDInterp = sICCIDInterp + " - Luhn digit: "
          if str_right(sLuhn, 1) != "F":
             sICCIDInterp = sICCIDInterp + str_right(sLuhn, 1)
          else: 
             sICCIDInterp = sICCIDInterp + str_left(sLuhn, 1)
             
    return sICCIDInterp
    
# simcard_EF_IMSI_GET ------------------------------------------------------------------------------------------------------
def simcard_EF_IMSI_GET(cardservice, sLogFileName):
    sIMSI = "6F 07"
    sRes = simcard_Select_GSM(cardservice, sLogFileName)
    if sRes=="":
       return sRes
       
    sRes = simcard_DF_EF_Select(cardservice, sLogFileName, sIMSI)
    sName = simcard_SelectEF_GetFileName(sRes)
    sSize = simcard_SelectEF_GetSize(sRes)
    nSize = bytes_HexaToNro(sSize)
    sValue = simcard_ReadBinary(cardservice, sLogFileName, nSize)

    sValue = simcard_RemoveSW1SW2(sValue)

    sLog = simcard_EF_IMSI_Interpret(sValue, True)
    sIMSIInterp = simcard_EF_IMSI_Interpret(sValue, False)
    log_write(sLogFileName, sLog)
    
    return sIMSIInterp

# simcard_EF_IMSI_Interpret ------------------------------------------------------------------------------------------------------
def simcard_EF_IMSI_Interpret(sHexa, bAddDes):
    sIMSIInterp = str_reverse(str_TrimCleanSpaces(sHexa))
    sIMSIInterp = sIMSIInterp[3:]
    if bAddDes:
       sIMSIInterp = "IMSI Value: 0x" + str_SpaceHexa(sHexa) + " - Length = " + str(len(sHexa)//2) + " bytes - interpreted: " + sIMSIInterp
    return sIMSIInterp

    
# simcard_Select_GSM ------------------------------------------------------------------------------------------------------
def simcard_Select_GSM(cardservice, sLogFileName):
    sGSM = "7F 20"
    sRes = simcard_DF_EF_Select(cardservice, sLogFileName, sGSM)
    return sRes

# simcard_Select_GSM ------------------------------------------------------------------------------------------------------
def simcard_Select_TELECOM(cardservice, sLogFileName):
    sGSM = "7F 10"
    sRes = simcard_DF_EF_Select(cardservice, sLogFileName, sGSM)
    return sRes

# simcard_SelectEF_GetFileName ------------------------------------------------------------------------------------------------------
def simcard_SelectEF_GetFileName(sResponse):
    sFile = simcard_GetDataFromTAGByExpectedBytes(sResponse, "83", 2)
    return sFile

# simcard_SelectEF_GetSize ------------------------------------------------------------------------------------------------------
def simcard_SelectEF_GetSize(sResponse):
    sSize = simcard_GetDataFromTAGByExpectedBytes(sResponse, "80", 2)
    sTemp = simcard_GetDataFromTAGByExpectedBytes(sResponse, "82", 5)
    #print("TAG = 82: " + sTemp)
    sRecordLen = "00"
    sRecords = "00"
    if len(sTemp) >= 8:
       sRecordLen = sTemp[6:8]
       #print("RECORD LEN: " + sRecordLen)
       sRecords = sTemp[8:10]
       #print("TEMP 9:10: " + sRecords)
       nSize = int(bytes_HexaToNro(sRecords)) * int(bytes_HexaToNro(sRecordLen))
       sSize = bytes_NroToHexa(nSize)
    
    #print("RECORD LEN: " + sRecordLen)
    #print("RECORDS: " + sRecords)
    #print("SIZE: " + sSize)
    
    if sRecordLen == "00":
       sRecordLen = ""    
    if sRecords == "00":
       sRecords = ""    
       
    return sSize + sRecordLen + sRecords
    
# simcard_GetDataFromTAGByExpectedBytes ------------------------------------------------------------------------------------------------------
def simcard_GetDataFromTAGByExpectedBytes(sResponse, sTAG, nBytes):
    sResponse = str_TrimCleanSpaces(sResponse)
    sTAG = str_TrimCleanSpaces(sTAG)
    sBytes = bytes_NroToHexa(nBytes)   
    
    nOcur = 0
    bWhile = True
    sTemp = "1"
    sValue = ""
    while bWhile or sTemp!="" :
          #print("RESPONSE: " + sResponse + " - TAG: " + sTAG + " - Ocur: " + str(nOcur))
          sTemp = str_getSubStringFromOcur(sResponse, sTAG, nOcur)
          #print("TEMP: " + sTemp)
          nOcur = nOcur + 1
          sLen = sTemp[:2]
          #print("LEN: " + sLen) 
          if sLen == sBytes:
             sValue = sTemp[2:]
             sValue = sTemp[2:((nBytes*2)+2)]
             #print("VALUE: " + sValue) 
             bWhile = False
             sTemp = ""
          
          if nOcur > 10:
             bWhile = False
             sTemp = ""
          
    return sValue

# simcard_RemoveSW1SW2 ------------------------------------------------------------------------------------------------------
def simcard_RemoveSW1SW2(sResponse):
    #REMOVING 90 00
    nLen = len(sResponse)
    if nLen > 0:
       sResponse = sResponse[:nLen-4]
    return sResponse

# simcard_EF_SMS_GET ------------------------------------------------------------------------------------------------------
def simcard_EF_SMS_GET(cardservice, sLogFileName, nRecords):
    sSMS = "6F 3C"
    sRes = simcard_Select_TELECOM(cardservice, sLogFileName)
    if sRes=="":
       return sRes
       
    sRes = simcard_DF_EF_Select(cardservice, sLogFileName, sSMS)
    sName = simcard_SelectEF_GetFileName(sRes)
    sSize = simcard_SelectEF_GetSize(sRes)
    sRecs = "00"
    sRecSize = "00"
    if len(sSize)>4:
       sRecs = sSize[6:]
       sRecSize = sSize[4:6]
    
    #print("RECS: " + sRecs)
    nRecs = bytes_HexaToNro(sRecs)

    if nRecords>0:
       if nRecords > nRecs:
          nRecords = nRecs
    else:
       nRecords = nRecs
       
    sValue = simcard_ReadRecordsALL(cardservice, sLogFileName, nRecords)

    return sValue


# simcard_STKCmd_SendTerminalResponseSendSMS ------------------------------------------------------------------------------------------------------
def simcard_STKCmd_SendTerminalResponseSendSMS(cardservice, sLogFileName):
    return simcard_STKCmd_SendTerminalResponse(cardservice, sLogFileName, simcard_STKCmdGetCmdSendSMS())

# simcard_STKCmd_SendTerminalResponse ------------------------------------------------------------------------------------------------------
def simcard_STKCmd_SendTerminalResponse(cardservice, sLogFileName, sCmd):

    if sCmd=="":
       return ""

    #Terminal Response
    #C - 80 14 00 00 0C 01 03 01 13 00 02 02 82 81 03 01 00
    #SW - 90 00

    # BECAUSE PROVIDELOCI AFTER SEND SMS
    sDT_CMDResponse = "80 14 00 00 0C 01 03 01 " + sCmd + " 00 02 02 82 81 03 01 00"
    #print("simcard_STKCmd_SendTerminalResponse - sDT_CMDResponse: " + str(sDT_CMDResponse))
    sResAndSW1SW2 = simcard_Response(cardservice, sDT_CMDResponse, sLogFileName)   

    # BECAUSE PROVIDELOCI AFTER SEND SMS
    #sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    #sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    #print("simcard_STKCmd_SendTerminalResponse - sResAndSW1SW2: " + str(sResAndSW1SW2))

    # FETCH RESPONSE FROM ENVELOPE
    #if sSW1 == '91' and sSW2!="00":

    #    sFETCH_RESPONSE = "80 12 00 00"
    #    log_write(sLogFileName, "FETCH RESPONSE FROM CMD " + sCmd)
    #    sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
    #    log_write(sLogFileName, sTempFetchResponse)
        
    sResAndSW1SW2 = simcard_SendResponseContinuos(cardservice, sLogFileName, sResAndSW1SW2)
    #print("simcard_STKCmd_SendTerminalResponse - sResAndSW1SW2: " + str(sResAndSW1SW2))
    
    if len(sResAndSW1SW2) > 4:
       sResAndSW1SW2 = str_left(sResAndSW1SW2, 4)

        #sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
    
    return sResAndSW1SW2       

# simcard_STKCmd_SendTerminalResponse_toanalyze ------------------------------------------------------------------------------------------------------
def simcard_STKCmd_SendTerminalResponse_toanalyze(cardservice, sLogFileName, sCmd, slots=None, tpda=None, bool_campaign_id=False, is_full=False, str_campaign_id=None):
    """
    This method shoots a terminal response to the SIM card and returns the response and SW1SW2 as a list.
    This method works with SEND SHORT MESSAGE, (keep filling the method's description with the rest of the
    commands when needed)
    """
    lGeneralResponse = []
    if sCmd=="":
       return ""
       
    #Terminal Response
    #C - 80 14 00 00 0C 01 03 01 13 00 02 02 82 81 03 01 00
    #SW - 90 00

    sResAndSW1SW2 = simcard_STKCmd_SendTerminalResponse(cardservice, sLogFileName, sCmd)
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
    lGeneralResponse.append([sResAndSW1SW2, sSW1, sSW2])
    
    #sDT_CMDResponse = "80 14 00 00 0C 01 03 01 " + sCmd + " 00 02 02 81 81 03 01 00"
    #sResAndSW1SW2 = simcard_Response(cardservice, sDT_CMDResponse, sLogFileName)   
    #sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    #sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
    #lGeneralResponse.append([sDT_CMDResponse, sSW1, sSW2])

    # FETCH RESPONSE FROM ENVELOPE
    #if sSW1 == '91' and sSW2!="00":
    #    sFETCH_RESPONSE = "80 12 00 00"
    #    log_write(sLogFileName, "FETCH RESPONSE FROM CMD " + sCmd)
        # Esto sucede porque pasaron "commands_to_send" Status Commands y el APK no informÃ³ su presencia previamente.
    #    if slots:
    #        log_write_OKInGreen(
    #            sLogFileName,
    #            f"This happens because X Status Commands were received and the APK did not previously report their presence. This is expected behaviour because the SDK_ID was previously defined in a slot.",
    #        )
    #        log_write_WarningInYellow(sLogFileName, "If there's no SDK_ID defined in a slot, omit the previous statement.")
    #    sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
    #    log_write(sLogFileName, sTempFetchResponse)
    #    sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
    #    interpret = simcard_interpret_dynamic_bytecode(
    #        sResAndSW1SW2,
    #        tpda if tpda else None,
    #        True if bool_campaign_id else False,
    #        True if is_full else False,
    #        str_campaign_id if str_campaign_id else None
    #    )
    #    if interpret:
    #        log_print_dict(sLogFileName, interpret)
    #    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    #    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)
    #    lGeneralResponse.append([sResAndSW1SW2, sSW1, sSW2])
    
    return lGeneralResponse   
    
# simcard_GenerateRandom ------------------------------------------------------------------------------------------------------
def simcard_GenerateRandom(nDigitsOut):
    sReturn = "0000"

    nLen = int(nDigitsOut)
    
    sdtFormat = "%f"
    if nLen > 6:
       #"%Y/%m/%d-%H:%M:%S.%f"
       sdtFormat = "%S" + sdtFormat
       if nLen > 8:
          sdtFormat = "%M" + sdtFormat
       if nLen > 10:
          sdtFormat = "%H" + sdtFormat
       if nLen > 12:
          sdtFormat = "%m" + sdtFormat
       if nLen > 14:
          sdtFormat = "%Y" + sdtFormat
       
    dateNow = datetime.now()    
    sdateNow = dateNow.strftime(sdtFormat)

    if len(sdateNow) % 2 != 0:
       sdateNow = "0" + sdateNow 
    
    #print("Date Now: " + sdateNow)
        
    if nLen > 0:   
       if len(sdateNow) > nLen:
          sdateNow = str_right(sdateNow, nLen)
       if len(sdateNow) < nLen:
          sdateNow = str_RepeatString(nLen - len(sdateNow), "0") + sdateNow
          
    sReturn = sdateNow
        
    #print("Random: " + sReturn)
    #sdateNowHexa = bytes_NroToHexa(sdateNow)
    #print("Random Hexa: " + sdateNowHexa)

    # TO TEST OUTSIDE METHOD
    #sOut= simcard_GenerateRandom(2)
    #print("Random 2: " + sOut)
    #sOut= simcard_GenerateRandom(10)
    #print("Random 10: " + sOut)
    #sOut= simcard_GenerateRandom(6)
    #print("Random 6: " + sOut)
        
    return sReturn

# simcard_Select_ARAM ------------------------------------------------------------------------------------------------------
def simcard_Select_ARAM(cardservice, sLogFileName, sChannel, aid_w_length = "09 A0 00 00 01 51 41 43 4C 00"):

#SELECT ARA-M  'A0 00 00 01 51 41 43 4C 00'
#   P1 Select by name
#   P2 First or only occurrence
#   AID 'A0 00 00 01 51 41 43 4C 00'
#Command
#   Header 02 A4 04 00
#   Lc 09
#   Command Data A0 00 00 01 51 41 43 4C 00

    if sChannel == "":
       sChannel = "02"
       
    sSelect = sChannel + " A4 04 00 " + aid_w_length
    log_write(sLogFileName, sSelect + ". Channel: " + sChannel)
    sResAndSW1SW2 = simcard_Response(cardservice, sSelect, sLogFileName)
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    if sSW1 == '6C':
       # ETSI 102.221
       # 7.3.1.1.5 Use of procedure bytes '61xx' and '6Cxx'
       log_write(sLogFileName, "SELECT ARA-M twice because of 0x" + sSW1 + ": " + sSW2 + ". ")
       sResAndSW1SW2 = simcard_Response(cardservice, sTerminalResponseAPDU2 + sSW2, sLogFileName)
       sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
       sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    return sSW1 + sSW2

# simcard_Select_ARAM_GetDataSHA1s ------------------------------------------------------------------------------------------------------
def simcard_Select_ARAM_GetDataSHA1s(cardservice, sLogFileName, sChannel):

#GET DATA
#   Request type Refresh tag
#Command
#   Header 82 CA DF 20
#   Le 00
#Response
#   Status Word 6C 6B
#GET DATA
#   Request type Refresh tag
#Command
#   Header 82 CA DF 20
#   Le 6B

    sSW1SW2 = simcard_Select_ARAM(cardservice, sLogFileName, sChannel)
    
    if sSW1SW2 == sSimcard_9000:
       #ARA-M Applet exists

       sResponse = simcard_ARAM_GetData(cardservice, sLogFileName, sChannel)
    else:
       sResponse = sSW1SW2
       
    return sResponse   

# simcard_GetData ----------------------------------------------------------------------------------------------------------
def simcard_ARAM_CLA(sChannel):
    #print("simcard_ARAM_CLA: " + str(sChannel))

    sCLA = "82"
    if sChannel != "" and str_IsNnro0To9FromString(sChannel):
       sCLA = "8" + str_right(sChannel, 1)
    
    return sCLA   

          
# simcard_GetData ----------------------------------------------------------------------------------------------------------
def simcard_ARAM_GetData(cardservice, sLogFileName, sChannel):

#GET DATA
#   Request type Refresh tag
#Command
#   Header 82 CA DF 20
#   Le 00
#Response
#   Status Word 61 6B
#GET DATA
#   Request type Refresh tag
#Command
#   Header 82 C0 00 00
#   Le 6B

    sTAGGetRefresh = "DF20"
    sTAGGetALL = "FF40"
    sTAGGetALLNext = "FF60"
    sTAGOK = sSimcard_9000
    
    log_writeWordsInColorBlue("Sending Get Data with REFRESH TAG 0x" + sTAGGetRefresh)
    sGetData = simcard_ARAM_CLA(sChannel) + " CA " + sTAGGetRefresh
    sResAndSW1SW2 = simcard_Select_ARAM_SendAPDU(cardservice, sLogFileName, sChannel, sGetData)
    
    #print("sResAndSW1SW2: " + str(sResAndSW1SW2))
    
    if str_left(sResAndSW1SW2,2)!=sTAGGetALL:
    
       # THIS MEANS THAT IT IS IMPLEMENTED THE REFRESH TAG IN THE APPLET
       # IT SHOULD BE SENT THE "FF40"
       log_writeWordsInColorBlue("Sending Get Data with ALL TAG 0x" + sTAGGetALL)
       sGetData = simcard_ARAM_CLA(sChannel) + " CA " + sTAGGetALL
       sResAndSW1SW2 = simcard_Select_ARAM_SendAPDU(cardservice, sLogFileName, sChannel, sGetData)
       
       #print("simcard_ARAM_GetData: BEFORE NEXT sResAndSW1SW2=" + str(sResAndSW1SW2))

       #BECAUSE THE RESPONSE IS BIGGER THAN 127
       if str_left(sResAndSW1SW2, len(sTAGGetALL)) == sTAGGetALL:

          #RESPONSE FF 40
          sTAGGetALLNextByte = str_mid(sResAndSW1SW2, len(sTAGGetALL), 2)
          #print("simcard_ARAM_GetData: Next Byte" + str(sTAGGetALLNextByte))

          if sTAGGetALLNextByte == sSimcard_LengthBiggerThan127:
             #THIS MEANS THAT THE KEYS ARE BIGGER THAN 127 BYTES
             #SENDING GET DATA NEXT, EXAMPLE = Header 82 CA FF 60

             sGetData = simcard_ARAM_CLA(sChannel) + " CA " + sTAGGetALLNext
             sResAndSW1SW2_2 = simcard_Select_ARAM_SendAPDU(cardservice, sLogFileName, sChannel, sGetData)
             
            #print("simcard_ARAM_GetData: sResAndSW1SW2_2 = " + str(sResAndSW1SW2_2))

             if len(sResAndSW1SW2_2) > 4:
                # > 4 BECAUSE 9000 AT THE END
                if str_right(sResAndSW1SW2, len(sTAGOK)) == sTAGOK:
                   sResAndSW1SW2 = str_left(sResAndSW1SW2, len(sResAndSW1SW2) - len(sTAGOK))
                sResAndSW1SW2 = sResAndSW1SW2 + sResAndSW1SW2_2

    print("simcard_ARAM_GetData: sResAndSW1SW2 = 0x" + str_AddSpaceHexa(str(sResAndSW1SW2)) + " - Length: " + str(len(sResAndSW1SW2)//2) + " bytes")
       
    return sResAndSW1SW2

# simcard_Send_APDU ------------------------------------------------------------------------------------------------------
def simcard_Select_ARAM_SendAPDU(cardservice, sLogFileName, sChannel, sAPDU):

#Command '82 02 FC AA 00'
#   Class '82'
#   Instruction '02'
#   P1 'FC'
#   P2 'AA'
#   Le '00'
    sAPDU = sAPDU.replace(" ", "")

    if len(sAPDU) % 2 != 0:
        log_write_ErrorInRed(
            sLogFileName,
            f"THE VALUE IS AN ODD NUMBER, CHECK THE COMMAND AND TRY AGAIN. LENGTH {len(sAPDU)}"
        )
        return "0000"

    # In case of receiving an APDU lacking of length such as
    # CLA INS P1 P2
    sSW2 = ""

    if len(sAPDU) == 8:
        sSW2 = "00"
       
    sGetData = sAPDU # 81 B1 04 00 00 FA
    sGET_RESPONSE = simcard_ARAM_CLA(sChannel) + " C0 00 00"
    
    #log_write(sLogFileName, "simcard_Select_ARAM_SendAPDU: 0x" + str(str_SpaceHexa(sGetData + " " + sSW2)) + ". Channel: " + str(sChannel))
    apdu_interpret = simcard_interpret_apdu_structure(sGetData, sLogFileName)
    log_print_dict(sLogFileName, apdu_interpret)
    sResAndSW1SW2 = simcard_Response(cardservice, sGetData + sSW2, sLogFileName)
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    if sSW1 == '6C':
        # ETSI 102.221
        # 7.3.1.1.5 Use of procedure bytes '61xx' and '6Cxx'
        if len(sGetData) >= 10 and sGetData[8:10] == "00":
            sGetData = sGetData[:8]
        log_write(sLogFileName, "APDU twice because of SW1 '" + sSW1 + ": " + sSW2 + ".")
        sResAndSW1SW2 = simcard_Response(cardservice, sGetData + sSW2, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

        # Here we'll be trying to get the data without the SDK ID
        # because it's possible that the applet version does not support this event

        if sSW1 == "6C":
            log_write_InfoInBlue(sLogFileName, f"Sending sGetData: {str_SpacesOut(sGetData)} with SW2: {sSW2} returned {sSW1} {sSW2}. "
                                               f"Trying again without data...")
            log_write(sLogFileName, "GET RESPONSE FROM APDU " + sGetData + " " + sSW2)
            sGetData = sGetData[:11]
            # sResAndSW1SW2 = simcard_Response(cardservice, f"{sGetData} 0", sLogFileName)
            sResAndSW1SW2 = simcard_Response(cardservice, f"{sGetData} {sSW2}", sLogFileName)
            sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
            sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

            if sSW1 == '6C':
                get_response = f"{sGetData} {sSW2}"
                sResAndSW1SW2 = simcard_Response(cardservice, get_response, sLogFileName)
                sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
                sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

                if sSW1 == "90":
                    log_write_WarningInYellow(sLogFileName, "Trying without data worked correctly. "
                                                            "There's a possibility that this version of the "
                                                            "applet does not support sending data from an APDU."
                                                            "The function 'apdu.setIncomingAndReceive()' may not be implemented.")

        
    # FETCH RESPONSE FROM ENVELOPE
    if sSW1 == '9F' or sSW1 == '61':
        log_write(sLogFileName, "GET RESPONSE FROM APDU " + sGetData + "\n" + simcard_DataResponseDesHexaAndASCII(sGetData, True))
        sTempFetchResponse = sGET_RESPONSE + " " + sSW2
        log_write(sLogFileName, sTempFetchResponse)
        sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
        sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
        sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    return sResAndSW1SW2


# simcard_DataDes ------------------------------------------------------------------------------------------------------
def simcard_DataResponseDesHexaAndASCII(sResponse, bDES):

    if sResponse=="":
       return sResponse
       
    sLog = ""
    if bDES:
       sLog = "DATA: " 
   
    sASCII = ""    
    if bytes_IsHexaValid(sResponse):   
       sLog = sLog + str_AddSpaceHexa(sResponse)
       sASCII = bytes_HexaToASCII(str(sResponse))
    else:
       sLog = sLog + sResponse
       
    if sASCII != "":
       if bDES:
          sLog = sLog + "\nDATA IN ASCII: "
       sLog = sLog + bytes_HexaToASCII(str(sResponse))
       
       #GET SEND SMS DESCRIPTION
       sInterpret, sData = simcard_SendSMSCmd_Interpret(sResponse)
       if sInterpret != "":
          sLog = sLog + "\n" + sInterpret

    if bDES == False:
       sLog = sASCII 

    return sLog

# simcard_OpenChannel -----------------------------------------------------------------------------------------------------------
def simcard_OpenChannel(cardservice, sLogFileName):
   
    #Command
    #Header 00 70 00 00
    #Le 01

    #MANAGE CHANNEL Open channel
    #Operation Open logical channel
    #Channel number Logical channel to be internally assigned by the UICC
    
    sAPDU = "00 70 00 00 01"
    sResAndSW1SW2 = simcard_sendAPDU(cardservice, sAPDU, sLogFileName)
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    #log_write(sLogFileName, "simcard_OpenChannel response: 0x" + sResAndSW1SW2)
   
    if sSW1 == '90' and sSW2 == '00':
       sChannel = str_left(sResAndSW1SW2, 2)
       return sChannel
    else:
       return ""
       
# simcard_CloseChannel -----------------------------------------------------------------------------------------------------------
def simcard_CloseChannel(cardservice, sLogFileName, sChannel):
   
    #Command
    #Header 00 70 80 02
    #Le 00

    #MANAGE CHANNEL Close channel 2
    #Operation Close logical channel
    #Channel number 2
    
    if len(str(sChannel))>2:
       return False
       
    sAPDU = "00 70 80 " + sChannel
    sResAndSW1SW2 = simcard_sendAPDU(cardservice, sAPDU, sLogFileName)
    sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
    sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    log_write(sLogFileName, "simcard_CloseChannel response: 0x" + str_AddSpaceHexa(sResAndSW1SW2) + ". Channel closed: " + sChannel)
    
    if sSW1 == '90' and sSW2 == '00':
       return True
    else:
       return False

# simcard_SendEnvelopeContinuosResponseList -----------------------------------------------------------------------------------------------------------
def simcard_SendEnvelopeContinuosResponseList(cardservice, sLogFileName, sTPDA, sAPDU, sSeparaAPDUForLastAPDUs="", sTAR=sSimcard_sDefTAR_COTA, bNetworkOKOrChangeIMEI=True, sMCC="", sMNC="", sMSL=sSimcard_MSLDefNoSecurity, sKIC=sSimcard_MSLDefKIC , sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter):

    sResp = simcard_SendEnvelopeContinuos(cardservice, sLogFileName, sTPDA, sAPDU, sSeparaAPDUForLastAPDUs, sTAR, bNetworkOKOrChangeIMEI, sMCC, sMNC, sMSL, sKIC, sKID, sCounter)
    sResp = str_SpacesOut(sResp)
    return sResp.split(sSeparaAPDUForLastAPDUs)

# simcard_SendEnvelopeContinuos -----------------------------------------------------------------------------------------------------------
def simcard_SendEnvelopeContinuos(cardservice, sLogFileName, sTPDA, sAPDU, sSeparaAPDUForLastAPDUs="", sTAR=sSimcard_sDefTAR_COTA, bNetworkOKOrChangeIMEI=True, sMCC="", sMNC="", sMSL=sSimcard_MSLDefNoSecurity, sKIC=sSimcard_MSLDefKIC , sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter):

    sResAndSW1SW2 = simcard_sendEnvelope(cardservice, sTPDA, sAPDU, sLogFileName, sTAR, sMSL, sKIC, sKID, sCounter)
    
    return simcard_SendResponseContinuos(cardservice, sLogFileName, sResAndSW1SW2, sSeparaAPDUForLastAPDUs, sTAR, bNetworkOKOrChangeIMEI, sMCC, sMNC, sMSL, sKIC, sKID, sCounter)

# simcard_SendResponseContinuos -----------------------------------------------------------------------------------------------------------
def simcard_SendResponseContinuos(cardservice, sLogFileName, sResAndSW1SW2, sSeparaAPDUForLastAPDUs="", sTAR=sSimcard_sDefTAR_COTA, bNetworkOKOrChangeIMEI=True, sMCC="", sMNC="", sMSL=sSimcard_MSLDefNoSecurity, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter):

    #print("simcard_SendResponseContinuos - sResAndSW1SW2: " + str(sResAndSW1SW2))
       
    sLog = "RESULT SW1 AND SW2: "
    if bytes_IsHexaValid(sResAndSW1SW2):
       sLog = sLog + str_AddSpaceHexa(sResAndSW1SW2)
    else:
       sLog = sLog + sResAndSW1SW2
    log_write(sLogFileName, sLog)
    
    sSW1 = ""
    sSW2 = ""
    if sResAndSW1SW2 != "":
       sSW1 = simcard_SW1SW2GetSW1(sResAndSW1SW2)
       sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

    if sSeparaAPDUForLastAPDUs == "":
       sSeparaAPDUForLastAPDUs = sSimcard_SeparaAPDUForLastAPDUs
       
    #sPattern = "D0 2A 81 03 01 13"
    #sPattern = str_SpacesOut(sPattern)
    
    sWhileMsg = "\nInside while for Processing Responses for continuos SIM Toolkit Commands"
    
    #print("simcard_SendResponseContinuos - sResAndSW1SW2 before while: " + sResAndSW1SW2)
    
    sLastAPDU = sResAndSW1SW2
    #print("sLastAPDU before while: " + sLastAPDU)
        
    n = 0
    bExit = False
    
    if sSimcard_9300 in str_SpacesOut(sResAndSW1SW2):
       # 0x93 00 = Smartcard: SIM Application Toolkit Busy.
       bExit = True
    
    while not bExit and n < 100:
       
          #print("simcard_SendResponseContinuos - sLastAPDU and/or SW1-SW2 - while n=" + str(n) + ": sLasAPDU = " + sLastAPDU)
          
          #if len(sResAndSW1SW2) > len(sPattern):
          #   if str_left(sResAndSW1SW2, len(sResAndSW1SW2)) == sResAndSW1SW2:
          #      bExit = False
          #else:
          #   if n== 0 and (sSW1 == "91" or sSW1 == "61"):
          #      bExit = False
          
          if not bExit:           
   
                sTempFetchResponse = ""
                if len(sResAndSW1SW2) != 4:
                   #PROCESS TERMINAL RESPONSE ACCORDING TO STATUS COMMAND
                   sTempFetchResponse = simcard_StatusCommandALLResponses_TerminalResponse(cardservice, sLogFileName, sResAndSW1SW2, bNetworkOKOrChangeIMEI, sMCC, sMNC)
                
                   bSendResponse = True   
 
                   log_write(sLogFileName, "0x" + str_SpaceHexa(sTempFetchResponse) + ". " + sWhileMsg + ": " + str(n))
                   sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
                
                if sResAndSW1SW2 == "":
                   return ""
                   
                sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
                sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

                if sLastAPDU != "":
                   sLastAPDU = sLastAPDU + sSeparaAPDUForLastAPDUs
                sLastAPDU = sLastAPDU + sTempFetchResponse 

                if sSW1 == '90':
                   bExit = True
                   if str_SpacesOut(sResAndSW1SW2)==str_SpacesOut(str_CleanPattern(sLastAPDU, sSeparaAPDUForLastAPDUs)):
                      sLastAPDU = ""
                   #print("simcard_SendResponseContinuos - sResAndSW1SW2=" + str(sResAndSW1SW2) + " Length: " + str(len(sResAndSW1SW2)) + " - sLastAPDU=" + str(sLastAPDU) + " Length: " + str(len(sLastAPDU)))
                   return sResAndSW1SW2 + sLastAPDU
                   
                if sSW1 == '91':
                   sFETCH_RESPONSE = "80 12 00 00"
                   sTempFetchResponse = sFETCH_RESPONSE + " " + sSW2
                   log_write(sLogFileName, "0x" + str_SpaceHexa(sTempFetchResponse) + ". " + sWhileMsg + ": " + str(n))
                   sResAndSW1SW2 = simcard_Response(cardservice, sTempFetchResponse, sLogFileName)
                   sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
                   sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

                   sLastAPDU = sLastAPDU + sSeparaAPDUForLastAPDUs + sResAndSW1SW2 
             
                if sSW1 == '6C' or sSW1 == '61' or sSW1 == '91':
                   # ETSI 102.221
                   # 7.3.1.1.5 Use of procedure bytes '61xx' and '6Cxx'
                   log_write(sLogFileName, "FETCH RESPONSE twice because of 0x" + sSW1 + ": " + sSW2 + ". " + sWhileMsg + ": " + str(n))
                   sResAndSW1SW2 = simcard_Response(cardservice, sTerminalResponseAPDU2 + sSW2, sLogFileName)
                   sSW1 = simcard_SW1SW2ProcessReturnSW1(sResAndSW1SW2, sLogFileName)
                   sSW2 = simcard_SW1SW2GetSW2(sResAndSW1SW2)

                   sLastAPDU = sLastAPDU + sSeparaAPDUForLastAPDUs + sResAndSW1SW2 
                   
          else:
             bExit = True
        
          n = n + 1
          
    #print("simcard_SendResponseContinuos - sResAndSW1SW2: " + str(sResAndSW1SW2) + " - sLastAPDU: " + str(sLastAPDU))
          
    return sResAndSW1SW2 + sLastAPDU


# simcard_SendEnvelopeContinuosSendSMS -----------------------------------------------------------------------------------------------------------
def simcard_SendEnvelopeContinuosSendSMS(cardservice, sLogFileName, sTPDA, sAPDU, sTAR=sSimcard_sDefTAR_COTA):
    sResAndSW1SW2 = simcard_SendEnvelopeContinuos(cardservice, sLogFileName, sTPDA, sAPDU, str_GetBETWEENPARAM(), sTAR)
    if len(sResAndSW1SW2)>4:
       sAPDU = str_left(sResAndSW1SW2, 4)
       return sAPDU
       
    return "" 
       

# simcard_SendEnvelopeContinuosAnalizeResponse -----------------------------------------------------------------------------------------------------------
def simcard_SendEnvelopeContinuosAnalizeResponse(sLogFileName, sSW1SW2AndLastAPDU, sCMD, sCMDQualif, sSeparaAPDUs):
    sAPDU = ""
    sMsg = ""
    
    if len(sSW1SW2AndLastAPDU)>4:
       sAPDU = str_midToEnd(sSW1SW2AndLastAPDU, 4)
       #print("sAPDU: " + sAPDU)
       
       tAPDUs = str_getListFromStringPattern(sSW1SW2AndLastAPDU, sSeparaAPDUs)
       sAPDU = tAPDUs[0]
       
       #n = 1
       #while n < len(tAPDUs):
       #      print("n: " + str(n) + " - APDU: " + tAPDUs[n])
       #      n = n + 1
             
       #print(tAPDUs)
       nAPDUs = len(tAPDUs)
       if nAPDUs <= 1:
          sTemp = simcard_StatusCommandALLResponses_TerminalResponseGetCmd(sAPDU)
       else:
          sTemp = simcard_StatusCommandALLResponses_TerminalResponseGetCmd(tAPDUs[nAPDUs-1])
          if nAPDUs >= 2:
             sPreviousAPDU = tAPDUs[nAPDUs-2]
             #print("sPreviousAPDU: " + sPreviousAPDU)
             sPreviousAPDUProcessed = simcard_StatusCommandALLResponses_TerminalResponseGetDesOnly(sPreviousAPDU, True)
             #print("sPreviousAPDUProcessed: " + sPreviousAPDUProcessed)
             sAPDU = sPreviousAPDUProcessed
             
       #print("sTemp: " + sTemp[0])
       
       sCmdInResponse = sTemp[0]
       sCmdQualifInResponse = sTemp[1]
       
       if sCMD!="" and sCMDQualif!="":
          sMsg = "CMD: " + sCMD + " - Qualifier: " + sCMDQualif + " - "

       if sCmdInResponse != sCMD or sCmdQualifInResponse!=sCMDQualif:
          sMsg = sMsg + "NOT "
       sMsg = sMsg + "OK - "   
          
       sMsg = sMsg + "taking into account PREVIOUS command "
       if bytes_IsHexaValid(sAPDU):
          sMsg = sMsg + str_SpaceHexa(sAPDU)
       else:
           sMsg = sMsg + sAPDU
      
    return sMsg   


# simcard_STKCmdGetDes -----------------------------------------------------------------------------------------------------------
def simcard_STKCmdGetDes(sCmd, bAddDes=False):

    sReturn = ""
    
    sCmd =str_SpacesOut(sCmd)
    if sCmd == "":
       return ""

    if sCmd == "01":
       sReturn = "REFRESH"
    if sCmd == "02":
       sReturn = "MORE TIME"
    if sCmd == "03":
       sReturn = "POLL INTERVAL"
    if sCmd == "04":
       sReturn = "POLLING OFF"
    if sCmd == "05":
       sReturn = "SETUP EVENT LIST"
    if sCmd == "10":
       sReturn = "SETUP CALL"
    if sCmd == "11":
       sReturn = "SEND SS"
    if sCmd == "12":
       sReturn = "SEND USSD"
    if sCmd == "13":
       sReturn = "SEND SHORT MESSAGE"
    if sCmd == "14":
       sReturn = "SEND DTMF"
    if sCmd == "15":
       sReturn = "LAUNCH BROWSER"
    if sCmd == "20":
       sReturn = "PLAY TONE"
    if sCmd == "21":
       sReturn = "DISPLAY TEXT"
    if sCmd == "22":
       sReturn = "GET INKEY"
    if sCmd == "23":
       sReturn = "GET INPUT"
    if sCmd == "24":
       sReturn = "SELECT ITEM"
    if sCmd == "25":
       sReturn = "SETUP MENU"
    if sCmd == "26":
       sReturn = "PROVIDE LOCAL INFO"
    if sCmd == "27":
       sReturn = "TIMER MANAGEMENT"
    if sCmd == "28":
       sReturn = "SETUP IDLE MODE TEXT"
    if sCmd == "30":
       sReturn = "CARD APDU"
    if sCmd == "31":
       sReturn = "POWER ON CARD"
    if sCmd == "32":
       sReturn = "POWER OFF CARD"
    if sCmd == "33":
       sReturn = "GET READER STATUS"
    if sCmd == "34":
       sReturn = "RUN AT COMMAND"
    if sCmd == "35":
       sReturn = "LANGUAGE NOTIFICATION"
    if sCmd == "40":
       sReturn = "OPEN CHANNEL"
    if sCmd == "41":
       sReturn = "CLOSE CHANNEL"
    if sCmd == "42":
       sReturn = "RECEIVE DATA"
    if sCmd == "43":
       sReturn = "SEND DATA"
    if sCmd == "44":
       sReturn = "GET CHANNEL STATUS"
    if sCmd == "45":
       sReturn = "SERVICE SEARCH"
    if sCmd == "46":
       sReturn = "GET SERVICE INFORMATION"
    if sCmd == "47":
       sReturn = "DECLARE SERVICE"
    if sCmd == "50":
       sReturn = "SET FRAMES"
    if sCmd == "51":
       sReturn = "GET FRAMES"

    if bAddDes == True:
       #ACCORDING ETSI 102.223
       sReturn = " ETSI 102.223 SIM TOOLKIT COMMAND: 0x" + sCmd + " - " + sReturn

    return sReturn

# simcard_STKCmdIsPlayTone -----------------------------------------------------------------------------------------------------------
def simcard_STKCmdIsPlayTone(sCmd):
    sCmd ==str_SpacesOut(sCmd)
    if sCmd == "":
       return False

    if sCmd=="20":
       return True
    else:   
       return False   

# simcard_STKCmdIsProvideLoci -----------------------------------------------------------------------------------------------------------
def simcard_STKCmdIsProvideLoci(sCmd):
    sCmd ==str_SpacesOut(sCmd)
    if sCmd == "":
       return False

    if sCmd=="26":
       return True
    else:   
       return False   

# simcard_STKCmdResponseGetDesFromASCII -----------------------------------------------------------------------------------------------------------
def simcard_STKCmdResponseGetDesFromASCII(sUserResponse):
    return simcard_STKCmdResponseGetDes(sUserResponse, False)

# simcard_STKCmdResponseGetDesFromHexa -----------------------------------------------------------------------------------------------------------
def simcard_STKCmdResponseGetDesFromHexa(sUserResponse):
    return simcard_STKCmdResponseGetDes(sUserResponse, True)

# simcard_STKCmdResponseGetDes -----------------------------------------------------------------------------------------------------------
def simcard_STKCmdResponseGetDes(sUserResponse, bHexa):
    sUserResponse =str_SpacesOut(sUserResponse).upper()
    if sUserResponse == "":
       return ""
    
    sResponse = "00"
    
    #ETSI 102.223
    
    if bHexa:
       if sUserResponse == "00":
          sResponse = "OK - Command performed successfully"
       if sUserResponse == "01":
          sResponse = "OK - Command performed with partial comprehension"
       if sUserResponse == "02":
          sResponse = "OK - Command performed, with missing information"
       if sUserResponse == "03":
          sResponse = "OK - REFRESH performed with additional EFs read"
       if sUserResponse == "04":
          sResponse = "OK - Command performed successfully, but requested icon could not be displayed"
       if sUserResponse == "05":
          sResponse = "OK - Command performed, but modified by call control by SIM"
       if sUserResponse == "06":
          sResponse = "OK - Command performed successfully, limited service"
       if sUserResponse == "07":
          sResponse = "OK - Command performed with modification (if class 'e' is supported)"
       if sUserResponse == "10":
          sResponse = "CANCEL - Proactive SIM session terminated by the user"
       if sUserResponse == "11":
          sResponse = "BACK - Backward move in the proactive SIM session requested by the user"
       if sUserResponse == "12":
          sResponse = "TIMEOUT - No response from user"
       if sUserResponse == "13":
          sResponse = "Help information required by the user"
       if sUserResponse == "14":
          sResponse = "CANCEL - USSD or SS transaction terminated by the user"
       if sUserResponse == "20":
          sResponse = "ERROR - ME currently unable to process command"
       if sUserResponse == "21":
          sResponse = "ERROR - Network currently unable to process command"
       if sUserResponse == "22":
          sResponse = "ERROR - User did not accept the proactive command"
       if sUserResponse == "23":
          sResponse = "ERROR - User cleared down call before connection or network release"
       if sUserResponse == "24":
          sResponse = "ERROR - Action in contradiction with the current timer state"
       if sUserResponse == "25":
          sResponse = "ERROR - Interaction with call control by SIM, temporary problem"
       if sUserResponse == "26":
          sResponse = "ERROR - Launch browser generic error code"
       if sUserResponse == "26":
          sResponse = "ERROR - Launch browser generic error code"
       if sUserResponse == "30":
          sResponse = "NOT SUPPORTED - Command beyond ME's capabilities"
       if sUserResponse == "31":
          sResponse = "NOT SUPPORTED - Command type not understood by ME"
       if sUserResponse == "32":
          sResponse = "NOT SUPPORTED - Command data not understood by ME"
       if sUserResponse == "33":
          sResponse = "NOT SUPPORTED - Command number not known by ME"
       if sUserResponse == "34":
          sResponse = "NOT SUPPORTED - SS Return Error"
       if sUserResponse == "35":
          sResponse = "NOT SUPPORTED - SMS RP-ERROR"
       if sUserResponse == "36":
          sResponse = "NOT SUPPORTED - Error, required values are missing"
       if sUserResponse == "37":
          sResponse = "NOT SUPPORTED - USSD Return Error"
       if sUserResponse == "38":
          sResponse = "NOT SUPPORTED - MultipleCard commands error, if class 'a' is supported"
       if sUserResponse == "39":
          sResponse = "NOT SUPPORTED - Interaction with call control by SIM or MO short message control by SIM, permanent problem"
       if sUserResponse == "3A":
          sResponse = "NOT SUPPORTED - Bearer Independent Protocol error (if class 'e' is supported)"

    else:
       if sUserResponse == "OK":
          sResponse = "00"
       if sUserResponse == "CANCEL":
          sResponse = "10"
       if sUserResponse == "BACK":
          sResponse = "11"
       if sUserResponse == "TIMEOUT":
          sResponse = "12"
       if sUserResponse == "NOTSUPPORTED":
          sResponse = "30"
       if sUserResponse == "ERROR":
          sResponse = "20"
          
    return sResponse


# simcard_STKCmdGetCmdSendSMS -----------------------------------------------------------------------------------------------------------
def simcard_STKCmdGetCmdSendSMS():
    return "13"
    
# simcard_STKCmdGetCmdSendSMSQualif -----------------------------------------------------------------------------------------------------------
def simcard_STKCmdGetCmdSendSMSQualif():
    return "00"

# simcard_getDCS_ASCII -----------------------------------------------------------------------------------------------------------
def simcard_getDCS_ASCII():
    return "04"
# simcard_getDCS_UCS2 -----------------------------------------------------------------------------------------------------------
def simcard_getDCS_UCS2():
    return "08"

# simcard_getTAG_TEXTSTRING -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_TEXTSTRING():
    return "8D"

# simcard_getTAG_ADDRESS -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_ADDRESS():
    return "86"
# simcard_getTAG_ADDRESS_7BITS -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_ADDRESS_7BITS():
    return "8A"

# simcard_getTAG_SELECTITEM_HEADER -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_SELECTITEM_HEADER():
    return "05"
# simcard_getTAG_SELECTITEM -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_SELECTITEM():
    return "8F"

# simcard_getTAG_URL -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_URL():
    return "31"

# simcard_getTAG_GETINPUT_QANUMBER -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_GETINPUT_QANUMBER():
    return "00"
# simcard_getTAG_GETINPUT_QATEXT -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_GETINPUT_QATEXT():
    return "01"
# simcard_getTAG_GETINPUT_QAUCS2 -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_GETINPUT_QAUCS2():
    return "03"
# simcard_getTAG_GETINPUT_QATEXTHIDDEN -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_GETINPUT_QATEXTHIDDEN():
    return "05"
# simcard_getTAG_GETINPUT_QANUMBERHIDDEN -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_GETINPUT_QANUMBERHIDDEN():
    return "04"
# simcard_getTAG_GETINPUT_HEADER -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_GETINPUT_HEADER():
    return "0D"
# simcard_getTAG_GETINPUT_MINMAX -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_GETINPUT_MINMAX():
    return "11"
# simcard_getTAG_GETINPUT_DEFAULT -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_GETINPUT_DEFAULT():
    return "17"

# simcard_getTAG_DESTINATION_UICC -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_DESTINATION_UICC():
    return "81"
# simcard_getTAG_DESTINATION_NETWORK -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_DESTINATION_NETWORK():
    return "83"
# simcard_getTAG_DESTINATION_DEVICE -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_DESTINATION_DEVICE():
    return "82"
# simcard_getTAG_DESTINATION_EARPIECE -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_DESTINATION_EARPIECE():
    return "03"

# simcard_getTAG_TONE_TYPE -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_TONE_TYPE():
    return "0E"
# simcard_getTAG_DURATION -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_DURATION():
    return "04"
# simcard_getTAG_DURATION_SECONDS -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_DURATION_SECONDS():
    return "01"

# simcard_getTAG_ASCII -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_ASCII():
    return "04"
# simcard_getTAG_UCS2 -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_UCS2():
    return "08"

# simcard_getTAG_PROVIDELOCI_LOCI -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_PROVIDELOCI_LOCI():
    return "00"
# simcard_getTAG_PROVIDELOCI_IMEI -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_PROVIDELOCI_IMEI():
    return "01"

# simcard_getTAG_DISPLAYTEXT_HIGHPRIORITY -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_DISPLAYTEXT_HIGHPRIORITY():
    #8 = Wait for user response
    #1 = High priority
    return "81"
# simcard_getTAG_DISPLAYTEXT_NORMALPRIORITY -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_DISPLAYTEXT_NORMALPRIORITY():
    #8 = Wait for user response
    #0 = Normal priority
    return "80"

# simcard_getTextIntoBytecodeWithDCSReturn -----------------------------------------------------------------------------------------------------------
def simcard_getTextIntoBytecodeWithDCSReturn(sText):
    return simcard_getTextIntoBytecode(sText, "", True)

# simcard_getTextIntoBytecodeWithDCSReturnAndDCSSetUCS2 -----------------------------------------------------------------------------------------------------------
def simcard_getTextIntoBytecodeWithDCSReturnAndDCSSetUCS2(sText):
    return simcard_getTextIntoBytecode(sText, "UCS2", True)

# simcard_getQUALIF_SENDSMS_ASCII -----------------------------------------------------------------------------------------------------------
def simcard_getQUALIF_SENDSMS_ASCII():
    return "01"
# simcard_getQUALIF_SENDSMS_BINARY -----------------------------------------------------------------------------------------------------------
def simcard_getQUALIF_SENDSMS_BINARY():
    return "00"
# simcard_getTAG_SMSTPDU -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_SMSTPDU():
    return "0B"
# simcard_getTAG_SMS_DCS_8BITS -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_SMS_DCS_8BITS():
    return "04"
# simcard_getTAG_SMS_DCS_7BITS -----------------------------------------------------------------------------------------------------------
def simcard_getTAG_SMS_DCS_7BITS():
    # Packed Required
    return "00"
    
# simcard_getTextIntoBytecode -----------------------------------------------------------------------------------------------------------
def simcard_getTextIntoBytecode(sText, sDCSSet, bAddDCSReturn):
    
    sData = sText
    if str_SpacesOut(sData)=="":
       return ""

    # DCS = DATA CODING SCHEME 
    sDCS = str_SpacesOut(sDCSSet).upper()   
    if sDCS=="UCS2":
       # FORCE TO UCS2 FORMAT
       sDCS = simcard_getDCS_UCS2()
       textinbytes = bytes_get_UTFTextEncodeToUCS2(sData)
    else:   
       # CHECK FORMAT, BY DEFAULT IS ASCII
       sDCS = simcard_getDCS_ASCII()
       bASCII = True
       if bytes_isASCIIText(sData)==False:
          if bytes_isUCS2Text(sData):
             sDCS = simcard_getDCS_UCS2()
             bASCII = False
          else:
             return "DATA CODING SCHEME UNKNOWN. Data: " + sText
       textinbytes = bytes_encodeText(sData)

    sCMD = ""
   
    textinbytes = textinbytes.replace(" ", "")
    
    if bAddDCSReturn:
       textinbytes = sDCS + textinbytes
    
    sCMD = sCMD + simcard_Add81ForLenBiggerThan127(textinbytes)
   
    return sCMD
   
# simcard_Add81ForLenBiggerThan127 -----------------------------------------------------------------------------------------------------------
def simcard_Add81ForLenBiggerThan127(sText):
    sText = str(sText)
    nLenData = len(sText)//2
    sCMD = sText
    sCMD = bytes_NroToHexa(nLenData) + sCMD
    if nLenData > 127:
       sCMD = sSimcard_LengthBiggerThan127 + sCMD
    
    #print("nLenData: " + str(nLenData) + " - 0x: " + bytes_NroToHexa(nLenData))
    
    sCMD = str_SpacesOut(sCMD).upper()
    return sCMD
       
  
# COTA_processSMS ---------------------------------------------------------------------------------------------------------------------------------------------------------
def COTA_processSMS(sSMS, sTAR=sSimcard_sDefTAR_COTA):
    #PROCESS COTA SMS
    #print("COTA_processSMS: sSMS = " + str(sSMS))
    sSMS = str_SpacesOut(sSMS)
    
    sLog = ""
    #sFieldSepara = " - "
    sFieldSepara = "\n"
    
    if sSMS == "":
       return ""
    
    # 0x43 4F 54 41 = COTA
    # 0x41 55 54 48 = AUTH
    
    sAppName = simcard_processTAR_GetAPPName(sTAR)
    sAppNameHexa = bytes_StrToHexa(sAppName)
    
    sCOTAVer = str_getSubStringFromOcur(sSMS,sAppNameHexa,1)
    #print("COTA_processSMS: sSMS = " + str(sSMS))
    #print("COTA_processSMS: sCOTAVer = " + str(sCOTAVer))
    
    
    #print("sSMS: " + str(sSMS))
       
    if sCOTAVer!= "":
       if str_right(sCOTAVer, len(sSimcard_9000)) == sSimcard_9000:
          sCOTAVer = str_left(sCOTAVer, len(sCOTAVer)-len(sSimcard_9000))
          
       sCOTAVer = bytes_HexaToASCII(sCOTAVer)
       sSMS = str_getSubStringFromOcur(sSMS,sAppNameHexa,0)
       #print("COTA_processSMS - sSMS: " + sSMS)
       
       bSAPAUTH = False
       if str_left(sSMS, 4) == "B100":
          #SAPAUTH DATA
          sLog = sLog + sFieldSepara + "SAPAUTH data: 0x" + str_AddSpaceHexa(sSMS) + " - Length = " + str(len(sSMS)//2) + " bytes"
          #B1 00 xx xx => 4 bytes
          sSMS = str_midToEnd(sSMS, 8)
          bSAPAUTH = True
       
       nIMEILen = 8
       nLBrowserLen = 1
       nICCIDLen = 10
       nIMSILen = 9

       sICCID = ""
       sIMSI = ""
              
       if (len(sSMS)//2) == (nIMEILen + nLBrowserLen + nICCIDLen + nIMSILen):
          if bSAPAUTH:
              sICCID = str_left(sSMS,nICCIDLen*2)
              sIMSI = str_mid(sSMS,(nICCIDLen*2),nIMSILen*2)
              sIMEI = str_mid(sSMS,(nICCIDLen*2)+(nIMSILen*2),nIMEILen*2)
              sLaunchSupported = str_mid(sSMS,(nICCIDLen*2)+(nIMSILen*2)+(nIMEILen*2),2)
          else:
              sIMEI = str_left(sSMS,nIMEILen*2)
              sLaunchSupported = str_mid(sSMS,nIMEILen*2,2)
              sICCID = str_mid(sSMS,(nIMEILen*2)+2,nICCIDLen*2)
              sIMSI = str_mid(sSMS,(nIMEILen*2)+2+(nICCIDLen*2),nIMSILen*2)
       else:
          sLaunchSupported = str_right(sSMS,2)
          sIMEI = str_left(str_right(sSMS,18),16)
       
       if sICCID != "" and sIMSI != "":
          sLog = sLog + sFieldSepara + simcard_EF_ICCID_Interpret(sICCID, True) 
          sLog = sLog + sFieldSepara + simcard_EF_IMSI_Interpret(sIMSI, True)
       
       if len(sIMEI) != 16:
          sIMEI = ""
          
       if sIMEI != "" and (sLaunchSupported=="31" or sLaunchSupported=="30")==False:
          #IMEI not found, it is not part of the data
          sIMEI = ""   
         
       sData = sSMS  
       if sIMEI != "":   
          sData = str_getSubStringFromOcur(sSMS,sIMEI,0)
             
       #print("sData: " + sData)
       
       sLog = sLog + sFieldSepara + "### APPLET " + sAppName + " version: " + sCOTAVer + " ###"
       if sIMEI != "" and (sLaunchSupported=="31" or sLaunchSupported=="30"):
          sLog = sLog + sFieldSepara + "Launch Browser Supported: 0x" + sLaunchSupported
          if sLaunchSupported=="31":
             sLog = sLog + " (Yes)"
          if sLaunchSupported=="30":
              sLog = sLog + " (No)"
       
       if sIMEI != "":       
          sLog = sLog + sFieldSepara + "IMEI: 0x" + str_AddSpaceHexa(sIMEI)
          sLog = sLog + " (Interpreted: " + loci_imeiFromHexa(sIMEI) + ")"
       
       if sData!="":
          sDataPrint = "Data or Campaign ID: 0x" + str_AddSpaceHexa(sData)   
          if sDataPrint != "":
             sLog = sLog + sFieldSepara + sDataPrint 
             
       #sLog = sLog + " ***"
       log_writeWordsInColorGreen(sLog)

       
    return sLog

# simcard_CardConnectCardServiceGet ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_CardConnectCardServiceGet():
    # request any card type
    cardtype = AnyCardType()
    
    cardrequest = CardRequest(timeout=10, cardType=cardtype)
    cardservice = cardrequest.waitforcard()
    
    return cardservice

# simcard_CardConnect ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_CardConnect(sLogFileName, num_status_commands=0, int_sleep=None, observer = ConsoleCardConnectionObserver()):
    """
    Connect to the SIM card and perform a few transmits.
    :param sLogFileName: the name of the log file to write to
    :param num_status_commands:  (Optional) The number of status commands to send to fully initialize the ME
    :param int_sleep: (Optional) Whether to sleep between status commands
    :return: Card Service
    """

    # request any card type
    cardtype = AnyCardType()

    try:
    
        # request card insertion
        sLog = 'insert a card (SIM card if possible) within 10s\n'
        log_write_OKInGreen(sLogFileName, sLog)
    
        cardrequest = CardRequest(timeout=10, cardType=cardtype)
        cardservice = cardrequest.waitforcard()
    
        # attach the console tracer
        # observer = ConsoleCardConnectionObserver()
        cardservice.connection.addObserver(observer)
    
        # connect to the card and perform a few transmits
        cardservice.connection.connect()
    
        #READ ICCID AND IMSI
        sLog = str_RepeatString(3, "+") + "READING ICCID" + str_RepeatString(3, "+")
        log_write_OKInGreen(sLogFileName, sLog)
        sICCID = simcard_EF_ICCID_GET(cardservice, sLogFileName)
        sLog = str_RepeatString(3, "+") + "FINISHED READING ICCID: " + sICCID + " " + str_RepeatString(3, "+")
        log_write_OKInGreen(sLogFileName, sLog)
        
        sLog = str_RepeatString(3, "+") + "READING IMSI" + str_RepeatString(3, "+")
        log_write_OKInGreen(sLogFileName, sLog)
        sIMSI = simcard_EF_IMSI_GET(cardservice, sLogFileName)
        sLog = str_RepeatString(3, "+") + "FINISHED READING IMSI: " + sIMSI + " " + str_RepeatString(3, "+")
        log_write_OKInGreen(sLogFileName, sLog)
    
        # TERMINAL PROFILE
        sSW1SW2 = simcard_TerminalProfile(cardservice, "", sLogFileName)
        sSW1 = simcard_SW1SW2GetSW1(sSW1SW2)
        sSW2 = simcard_SW1SW2GetSW2(sSW1SW2)
        sLog = "TERMINAL PROFILE. SW1: " + sSW1 + " - SW2: " + sSW2
        log_write_OKInGreen(sLogFileName, sLog)
    
        # TERMINAL PROFILE - RESPONSE
        sSW1SW2 = simcard_TerminalProfileResponse(cardservice, sSW1, sSW2, sLogFileName)
        sSW1 = simcard_SW1SW2GetSW1(sSW1SW2)
        sSW2 = simcard_SW1SW2GetSW2(sSW1SW2)
    
        sLog = "TERMINAL PROFILE RESPONSE. SW1: " + sSW1 + " - SW2: " + sSW2
        log_write_OKInGreen(sLogFileName, sLog)

        if num_status_commands > 0:
            log_write_InfoInBlue(sLogFileName, f"Sending {num_status_commands} status commands to fully initialize the ME...")
            for i in range(0, num_status_commands):
                # Sending i of num_status_commands status commands
                log_write_WarningInYellow(sLogFileName, f"Sending status command {i + 1} of {num_status_commands}...")
                if int_sleep:
                    sleep(int_sleep)
                simcard_StatusCommandALLResponsesWithLastAPDUs_List(
                    cardservice,
                    sLogFileName,
                    True,
                    str_GetBETWEENPARAM()
                )

        return cardservice
    
    except (CardRequestTimeoutException, CardConnectionException) as e:
        sLog = "ERROR: " + str(e) + "\nPossible error = time-out: no card inserted during last 10s."
        log_write_WarningInYellow(sLogFileName, sLog)
        return False
        #exit(0)

# simcard_status_command_get_responses ---------------------------------------------------------------------------------------------------------------------------------------------------------

def simcard_status_command_get_responses(cardservice, sLogFileName, itr):

    # Sending i of num_status_commands status commands
    log_write_WarningInYellow(sLogFileName, f"Sending status command {itr + 1}...")

    sw, last_apdu, res_dict = simcard_StatusCommandALLResponsesWithLastAPDUs_List(
        cardservice,
        sLogFileName,
        True,
        str_GetBETWEENPARAM()
    )
    return sw, last_apdu, res_dict
 
# simcard_CmdInitCheckAutomatic ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_InitCheckAutomaticProactiveCommand(cardservice, sLogFileName, bCardConnect, bCardDisconnect, nStatusCommandsToProcess, sCheckProactiveCommand, bERRORContinue=True):

    bSwitchOFFON_ChangeIMEI = True
    
    bReturn = True
    sLastAPDUs = ""
    
    nAsteriscs = 20
    sSeparaAPDUForLastAPDUs = sSimcard_SeparaAPDUForLastAPDUs 
    
    sLastAPDUsPrnFirstLast = []
    sLastAPDUsPrnFirstLastOcur = []
    nLastAPDUsPrnFirstLast = 0
    # IT IS = 3 BECAUSE THERE ARE MORE THAN 2 LINES - APDU + REPONSE (STATUS COMMAND)
    nLastAPDUsPrnFirstLastENTER = 3
    
    if bCardConnect:
       cardservice = simcard_CardConnect(sLogFileName)
    
    i = 0
    bReturn = True
    while i <= nStatusCommandsToProcess and bReturn:

          sLog = str_RepeatString(nAsteriscs, "*")
          sLog = sLog + " ITERACTION STATUS COMMAND: " + str(i) + " from " + str(nStatusCommandsToProcess) + "."
          sLog = sLog + " - STARTED"
          sLog = sLog + " " + str_RepeatString(nAsteriscs, "*")
          log_write(sLogFileName, sLog)
          
          sLog = str_RepeatString(nAsteriscs, "#")
          log_write(sLogFileName, sLog)
                 
          #SEND STATUS COMMAND
          tReturn = simcard_StatusCommandALLResponsesWithLastAPDUs_List(cardservice, sLogFileName, bSwitchOFFON_ChangeIMEI, sSeparaAPDUForLastAPDUs)
          sResult = tReturn[0]
          sLastAPDUs = tReturn[1]
          #sLastAPDUs = str_TrimCleanSpaces(str_DataWithSeparatorInLines(sLastAPDUs, sSeparaAPDUForLastAPDUs))
          sLastAPDUs = str_TrimCleanSpaces(sLastAPDUs)
                
          #print("sResult: " + sResult)
          #print("sLastAPDUs: " + sLastAPDUs)
                
          sLog = "nResult: 0x" + sResult
          sLog = sLog + "\nsLastAPDUs: " + sLastAPDUs
          log_write(sLogFileName, sLog)
                
          sLog = str_RepeatString(nAsteriscs, "*")
          sLog = sLog + "ITERACTION STATUS COMMAND: " + str(i) + " from " + str(nStatusCommandsToProcess) + "."
          sLog = sLog + " - ENDED"
          sLog = sLog + " " + str_RepeatString(nAsteriscs, "*")
          log_write(sLogFileName, sLog)

          sLog = str_RepeatString(nAsteriscs * 5, "-")
          log_write(sLogFileName, sLog + "\n")
                
          if sLastAPDUs!="":
             #INTERPRET APDUs
             h = 0
             sSepara = sSeparaAPDUForLastAPDUs
             nPat = str_CountPattern(sLastAPDUs, sSepara)
             # BECAUSE IT MAY BE 2 WORDS SEPARATED
             nPat = nPat + 1
             sLastAPDUsPrn = ""
             while h < nPat:
                   sAPDUt = str_getSubStringFromOcur(sLastAPDUs, sSepara, h)
                   sAPDUtDes = simcard_StatusCommandALLResponses_TerminalResponseGetDesOnly(sAPDUt, bSwitchOFFON_ChangeIMEI)
                   if sAPDUt!="":
                      sLastAPDUsPrn = sLastAPDUsPrn + str_GetENTER() + sAPDUt
                      if sAPDUtDes!="" and len(str_TrimCleanSpaces(sAPDUtDes))>2: 
                         sLastAPDUsPrn = sLastAPDUsPrn + " - " + sAPDUtDes
                   h = h + 1
    
             if sLastAPDUsPrn!="":
                log_write_WarningInYellow(sLogFileName, "sLastAPDUs: " + sLastAPDUsPrn + "\n")
                      
             if str_CountPattern(sLastAPDUsPrn, str_GetENTER())>nLastAPDUsPrnFirstLastENTER:
                #SAVE THE LIST OF APDUs WHEN THERE ARE NOT STATUS COMMAND ONLY
                m = 0
                bFound = False
                while m < nLastAPDUsPrnFirstLast and bFound==False:
                      if sLastAPDUsPrnFirstLast[m]==sLastAPDUsPrn:
                         sLastAPDUsPrnFirstLastOcur[m] = str(int(sLastAPDUsPrnFirstLastOcur[m])+1)
                         bFound = True
                      m = m + 1   
                if bFound==False:
                   sLastAPDUsPrnFirstLast.append(sLastAPDUsPrn)
                   sLastAPDUsPrnFirstLastOcur.append("0")
                   nLastAPDUsPrnFirstLast = nLastAPDUsPrnFirstLast + 1       
                   
       
          i = i + 1
          
    # CHECK WHETHER THERE DUPLICATED COMMANDS AFTER SWITCHING OFF MOBILE
    # EXAMPLE: AMX - SENDING THE SAME SMS WITH IMEI MORE THAN ONCE
    if nLastAPDUsPrnFirstLast>0:
       m = 0
       while m < nLastAPDUsPrnFirstLast:
             if int(sLastAPDUsPrnFirstLastOcur[m]) > 1:
                sError = "sLastAPDUsPrnFirstLast: \n" + sLastAPDUsPrnFirstLast[m]
                sError = sError + "\n*** sLastAPDUsPrnFirstLastOcur: " + str(sLastAPDUsPrnFirstLastOcur[m])
                if bERRORContinue==True:
                   log_write_WarningInYellow(sLogFileName, sError + "\n")
                else:   
                   log_write_ErrorInRed(sLogFileName, sError + "\n")
                   sys.exit(0)
             m = m + 1   

    if bCardDisconnect:
       cardservice.connection.disconnect()

    # VERIFY WHTHER THE PROACTIVE COMMAND IN PARAMETER IS FOUND OR NOT IN THE RESPONSES
    if sCheckProactiveCommand != "":
       sOut = simcard_CheckProactiveCommandInLastAPDUsResponse_Get_FromList(sLastAPDUsPrnFirstLast, sCheckProactiveCommand)
       if sOut != "":
          return sOut
           
      #  sPatternToSearchFor = sProactiveCommandPattern + sCheckProactiveCommand
      #  n = 0
      #  while n < nLastAPDUsPrnFirstLast:
      #        if str_instrBool(sLastAPDUsPrnFirstLast[n],sPatternToSearchFor):
      #           sOut = str_getSubStringFromWord(sLastAPDUsPrnFirstLast[n], sPatternToSearchFor, True)
      #           #print("sOut: " + str(sOut))
      #           return sOut
      #        n = n + 1
    
    #print("nLastAPDUsPrnFirstLast: " + str(nLastAPDUsPrnFirstLast))
    if nLastAPDUsPrnFirstLast==0:
       return ""
    else:
       #NO SEND SMS FOUND, FOR EXAMPLE
       return sLastAPDUsPrnFirstLast

# simcard_CheckSendSMSInLastAPDUsResponse_Get_FromList ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_CheckSendSMSInLastAPDUsResponse_Get_FromList(tLastAPDUs):
    return simcard_CheckProactiveCommandInLastAPDUsResponse_Get_FromList(tLastAPDUs, simcard_STKCmdGetCmdSendSMS())

# simcard_CheckProactiveCommandInLastAPDUsResponse_Get_FromList ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_CheckProactiveCommandInLastAPDUsResponse_Get_FromList(tLastAPDUs, sProactiveCommandToSearchFor):

    sSeparaAPDU = str_GetENTER()
    sLastAPDUs = ""
    nList = len(tLastAPDUs)
    n = 0
    while n < nList:
          sLastAPDUs = sLastAPDUs + sSeparaAPDU + tLastAPDUs[n]
          n = n + 1
    sLastAPDUs = str_RemoveFirstPattern(sLastAPDUs, sSeparaAPDU)
     
    return simcard_CheckProactiveCommandInLastAPDUsResponse(sLastAPDUs, sSeparaAPDU, sProactiveCommandToSearchFor)

# simcard_CheckSendSMSInLastAPDUsResponse_Get ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_CheckSendSMSInLastAPDUsResponse_Get(sLastAPDUs, sSeparaAPDU):
    return simcard_CheckProactiveCommandInLastAPDUsResponse_Get(sLastAPDUs, sSeparaAPDU, simcard_STKCmdGetCmdSendSMS())
    
# simcard_CheckProactiveCommandInLastAPDUsResponse_Get ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_CheckProactiveCommandInLastAPDUsResponse_Get(sLastAPDUs, sSeparaAPDU, sProactiveCommandToSearchFor):
    return simcard_CheckProactiveCommandInLastAPDUsResponse(sLastAPDUs, sSeparaAPDU, sProactiveCommandToSearchFor)

# simcard_CheckProactiveCommandInLastAPDUsResponse ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_CheckProactiveCommandInLastAPDUsResponse(sLastAPDUs, sSeparaAPDU, sProactiveCommandToSearchFor):
    
    if sSeparaAPDU=="":
       sSeparaAPDU = str_GetENTER()
       
    if str(sLastAPDUs) == "":
       return ""

    if str(sProactiveCommandToSearchFor) == "":
       return ""
    
    nSepara = str_CountPattern(sLastAPDUs, sSeparaAPDU)
    #print("nSepara: " + str(nSepara))
    
    #PATTERN TO SEARCH FOR "810301" + PROACTIVE COMMAND  
    sPatternToSearchFor = sProactiveCommandPattern + sProactiveCommandToSearchFor
    
    n = 0
    while n < nSepara:
          sAPDU = str_getSubStringFromOcur(sLastAPDUs, sSeparaAPDU, n)
          
          #print("sAPDU: " + sAPDU)
          #print("sPatternToSearchFor: " + sPatternToSearchFor)
          
          if str_instrBool(sAPDU,sPatternToSearchFor):
             #print("sAPDU str_instrBool: " + sAPDU)
             sOut = str_getSubStringFromWord(sAPDU, sPatternToSearchFor, True)
             #print("sOut 0: " + sOut)
             sOut = str_getSubStringFromOcur(sOut, sSeparaAPDU, 0)
             #print("sOut 1: " + sOut)
             
             sD0 = str_getSubStringFromOcur(sAPDU, sPatternToSearchFor, 0)
             
             return sD0 + sOut
          n = n + 1
    
    return ""


# simcard_coded_128_255 ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_coded_128_255(proactive_command):
    """
    Check if the proactive command's length is coded from 128 to 255 bytes to correctly extract the correct byte for
    type of command.
    :param proactive_command: the proactive command
    :return: Type of command in bytes
    """

    length_in_two_bytes = proactive_command[2:4]
    # Length coded in 2 bytes according to ISO/IEC 7816: 0x81 - length is coded from 128 to 255 bytes
    if length_in_two_bytes == sSimcard_LengthBiggerThan127:
        type_of_command = proactive_command[12:14]
    else:
        type_of_command = proactive_command[10:12]
    return type_of_command


# simcard_generate_random_imei ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_generate_random_imei():
    sRandom = simcard_GenerateRandom(6)
    sIMEI = str_SpaceHexa("8A 16 49 01 94" + sRandom)
    return sIMEI


# simcard_interpret_dynamic_bytecode -----------------------------------------------------------------------------------
def simcard_interpret_dynamic_bytecode(bytecode, tpda=None, bool_campaign_id=False, is_full=False, str_campaign_id=None):
    """
    This function interprets a dynamic bytecode gotten from a fetch that is not fixed in length or structure.
    The bytecode is expected to contain a series of tags and data objects, where each tag is followed by
    a length byte and the data object.

    :param bytecode: A string of hexadecimal characters representing the bytecode.
    :param tpda: for validation purposes.
    :param bool_campaign_id: for validation purposes.
    :param is_full: for validation purposes.
    :param str_campaign_id: for validation purposes.
    :returns: A dictionary containing interpreted elements of the bytecode [counter, apk apdu value, imei, launch browser support and COTA version].
    """
    # remove last four characters of the bytecode [sw1, sw2

    bytecode = bytecode[:-4].replace(" ", "")
    sdk_id_ascii = None
    str_cota = bytes_StrToHexa(sSimcard_sDefTAR_COTA_Name)
    # With this string, we can identify the sha1 in the bytecode
    str_sha1_identifier = "E218E116C114"
    # str_sha1_identifier_2 = "C114"
    str_request_all_access_rules = "FF40"
    # look for 43 4F 54 41 in the bytecode and get its index
    if str_cota in bytecode:
        index = bytecode.index("434F5441")
        cota_version = bytes_HexaToASCII(bytecode[index:])

        # Here we substract 24/26 characters or 12/13 bytes from the index to get the start of the data
        # APK_VALUE + COUNTER + IMEI + LAUNCH BROWSER SUPPORT
        # The data is expected to be 24/26 bytes long always
        data_index = index - 26 if "R5" in cota_version else index - 24

        data = bytecode[data_index:index]

        if "COTA02" in cota_version:
            # We consider that any COTA02 is a light version - 2024/04/23
            # If it isn't, then it is a full version of the applet
            imei = data[0:16]
            supports_launch_browser = data[16:18]
            apk_apdu_value = data[18:20]
            counter = data[20:24]

            if "R5" in cota_version:
                imei = data[2:18]
                supports_launch_browser = data[18:20]
                apk_apdu_value = data[20:22]
                counter = data[22:26]
        else:
            # Version 5.4, 5.1, 5.0, 4.0, 3.1 ... <keep adding when ecountering>
            apk_apdu_value = data[0:2]
            counter = data[2:6]
            imei = data[6:22]
            supports_launch_browser = data[22:24]

        if tpda:
            tpda = tpda.replace(" ", "")
            tpda_len = len(tpda)
            string = ''
            type_of_command = simcard_coded_128_255(bytecode)
            if type_of_command == "13":
                tpda_index = bytecode.index(tpda) + tpda_len
                pid_dcs = bytecode[tpda_index:tpda_index + 4]
                # We create a string of the data gotten so we can index the exact
                # sequence of hexa-values and get the exact spot of this data.
                string = string + pid_dcs
                pid_dcs_index = bytecode.index(pid_dcs) + len(pid_dcs)
                sms_len = bytecode[pid_dcs_index:pid_dcs_index + 2]
                string = string + sms_len
                sms_len_index = bytecode.index(string) + len(string)
                # Data only available in the full version of the applet
                sdk_id_len = ""
                sdk_id_len_index = ""
                if is_full:
                    sdk_id_len = bytecode[sms_len_index:sms_len_index + 2]
                    string = string + sdk_id_len
                    sdk_id_len_index = bytecode.index(string) + len(string)
                # Data varies depending on the presence of the campaign id, hence the need for a conditional statement
                imei_check = bytecode[sdk_id_len_index:sdk_id_len_index + 22] if is_full else bytecode[sms_len_index:sms_len_index + 22]
                # Validations for light and full versions respectively
                if bool_campaign_id:
                    imei_check = bytecode[sms_len_index + 2:sms_len_index + 28]
                if is_full and bool_campaign_id:
                    imei_check = bytecode[sdk_id_len_index+2:sdk_id_len_index + 28]


                if is_full and sdk_id_len == "00":
                    pass
                else:
                    present = False
                    if imei in imei_check:
                        present = True
                    if not present and is_full:
                        if bool_campaign_id:
                            check_campaign_id = bytecode[sms_len_index:sms_len_index + 4]
                            if check_campaign_id == str_campaign_id:
                                sdk_id_len = bytecode[sms_len_index + 4: sms_len_index + 6]
                            else:
                                sdk_id_len = bytecode[sms_len_index:sms_len_index + 2]
                        length_decimal = int(sdk_id_len, 16)*2
                        if bool_campaign_id:
                            sdk_id = bytecode[sdk_id_len_index+4:sdk_id_len_index + 4 + length_decimal]
                            if cota_version in ["COTA0505"]:
                                sdk_id = bytecode[sdk_id_len_index:sdk_id_len_index + length_decimal]
                        else:
                            sdk_id = bytecode[sdk_id_len_index:sdk_id_len_index + length_decimal]
                        sdk_id_ascii = bytes.fromhex(sdk_id).decode('utf-8')

        interpretation = {
            "Counter": counter,
            "APK APDU Value": apk_apdu_value,
            f"IMEI - 0x08 (16d)": imei,
            "Supports Launch Browser": supports_launch_browser,
            "COTA Version": cota_version
        }

        if sdk_id_ascii:
            # Calculete the lngth of characters in decimal and bytes
            sdk_id_len_bytes = sdk_id_len
            sdk_id_len = int(sdk_id_len, 16)
            interpretation[f"SDK ID - 0x{sdk_id_len_bytes} ({sdk_id_len}d)"] = sdk_id_ascii

        return interpretation
    elif str_request_all_access_rules in bytecode and str_sha1_identifier in bytecode:
        dict_rules_data = {}
        i = 1
        # Rule interpretation
        RULES = {
            "FF40": "Request All Access Rules",
            "E2": "REF-AR-DO",
            "E1": "REF-DO",
            "C1": "HASH-REF-DO"
        }
        cmd_index = bytecode.index("D7")
        # Here, we are removing the D7 byte and the length byte of it
        rules_bytecode = bytecode[cmd_index + 4:]
        for rule in RULES:
            if rule in rules_bytecode[:4]:
                length = len(rule)
                value_length = rules_bytecode[length:length + 2]
                dict_rules_data[f"{RULES[rule]} + Length"] = f"{rule} - 0x{value_length}({int(value_length, 16)}d) bytes"
                # Here, we are removing the rule and the length byte of it
                rules_bytecode = rules_bytecode[length + 2:]
        # Getting SAP SHA1 values to interpret
        identifier_len = len(str_sha1_identifier)
        sha1_len_hexa = str_sha1_identifier[-2:]
        sha1_len_decimal = int(sha1_len_hexa, 16)
        sha1_len = int(str_sha1_identifier[-2:], 16) * 2  # We multiply by two because we are trying to get the length in bytes
        index = bytecode.index(str_sha1_identifier)

        sha1 = bytecode[index + identifier_len:index + identifier_len + sha1_len]
        dict_rules_data[f'SHA1-{i} - 0x{sha1_len_hexa}({sha1_len_decimal}d) bytes'] = sha1
        bytecode = bytecode[index + identifier_len + sha1_len:]
        if bytecode:
            while str_sha1_identifier in bytecode:
                i += 1
                index = bytecode.index(str_sha1_identifier)
                dict_rules_data[f'SHA1-{i} - 0x{sha1_len_hexa}({sha1_len_decimal}d) bytes'] = bytecode[index + identifier_len:index + identifier_len + sha1_len]
                bytecode = bytecode[index + identifier_len + sha1_len:]
        return dict_rules_data
    else:
        return None


# simcard_interpret_apdu_structure ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_interpret_apdu_structure(apdu, sLogFileName=""):
    """
    This function interprets the structure of an APDU command and returns a dictionary containing the parsed elements.
    The APDU command is expected to be in the format: CLA INS P1 P2 [LC] [DATA] [LE]

    :param apdu: A string representing the APDU command.
    :returns: A dictionary containing the parsed elements of the APDU command.
    """
    apdu = apdu.replace(" ", "")

    if sLogFileName!="":
        log_write_InfoInBlue(sLogFileName, "apdu: " +  str_AddSpaceHexa(apdu))
    else:
        print("apdu: " + str_AddSpaceHexa(apdu))
    
    if len(apdu) < 8:
       apdu = apdu + str_RepeatString(8-len(apdu),"0")
    
    print("simcard_interpret_apdu_structure - apdu = " + str(apdu))
       
    # Split the APDU command into bytes
    bytes_list = [apdu[i:i+2] for i in range(0, len(apdu), 2)]

    #print("bytes_list: " + str(bytes_list))

    # Initialize a dictionary to store the interpreted APDU command
    interpreted = {}

    # Process the APDU command
    interpreted['CLA'] = bytes_list[0]
    interpreted['INS'] = bytes_list[1]
    interpreted['P1'] = bytes_list[2]
    interpreted['P2'] = bytes_list[3]

    # Check if there is a data field
    if len(bytes_list) > 5:
        interpreted['LC'] = bytes_list[4]
        interpreted['DATA'] = " ".join(bytes_list[5:])

        #interpreted['DATA IN ASCII'] = bytes.fromhex(interpreted['DATA']).decode('utf-8')

        sTemp = bytes.fromhex(interpreted['DATA'])
        #print(sTemp)        
        sTemp = str_CleanPattern(sTemp, "b")
        sTemp = str_CleanPattern(sTemp, "'")
        #print(sTemp)        
        
        #interpreted['DATA IN ASCII'] = bytes.fromhex(interpreted['DATA'])
        interpreted['DATA IN ASCII'] = sTemp
        print("interpreted['DATA']: " + str(interpreted['DATA']))
        #interpreted['DATA IN ASCII'] = bytes.fromhex(interpreted['DATA']).decode('utf-8')
        interpreted['DATA IN ASCII'] = bytes.fromhex(interpreted['DATA'])
    else:
        interpreted['LC'] = '00'
        interpreted['DATA'] = 'None'

    return interpreted


# simcard_processTAR_GetAPPName ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_processTAR_GetAPPName(sTAR=sSimcard_sDefTAR_COTA):
    sReturn = sSimcard_sDefTAR_COTA_Name
    
    sTAR = str_SpacesOut(sTAR).upper()
    if sTAR == sSimcard_sDefTAR_SAPAUTH:
       sReturn = sSimcard_sDefTAR_SAPAUTH_Name
       
    return sReturn
       
# simcard_processTAR_IsInSMSSiprocalAppletReference ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_processTAR_IsInSMSSiprocalAppletReference(sSMS, bASCII=True):
    sTAR = ""
    
    #print("simcard_processTAR_IsInSMSSiprocalAppletReference: sSMS=" + str(sSMS) + " - bASCII=" + str(bASCII))
    
    if bASCII == False:
       sSMS = bytes_HexaToASCII(sSMS)
       
    #COTA   
    sTAR = sSimcard_sDefTAR_COTA
    if str_instrBool(sSMS, sSimcard_sDefTAR_SAPAUTH_Name):
       #SAPAUTH
       sTAR = sSimcard_sDefTAR_SAPAUTH
          
    return sTAR          


# simcardCmd_sendEnvelopeConcat -----------------------------------------------------------------------------------------------------------------------------------------------
def simcardCmd_sendEnvelopeConcat(cardservice, sLogFileName, sCMD, sTPDAParam=sSimcard_sDefTPDA, sTAR=sSimcard_sDefTAR_COTA, bNetworkOKOrChangeIMEIOrChangeMCCMNC=True, sMCC="", sMNC="", sMSL=sSimcard_MSLDefNoSecurity, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter):

    sCMD = str_SpacesOut(sCMD)
    sTPDAParam = str_SpacesOut(sTPDAParam)
    sTAR = str_SpacesOut(sTAR)
    
    sMSL = str_SpacesOut(sMSL)
    sKIC = str_SpacesOut(sKIC)
    sKID = str_SpacesOut(sKID)
    sCounter = str_SpacesOut(sCounter)
    
    sAsteric = sSimcard_Asterics
    
    sReturn = ""
    sReturnDes = ""
        
    if sCMD=="":
       print("Command is NULL. CMD: " + sCMD)
       return ""

    if sTPDAParam=="":
       print("TPDA is NULL. TPDA: " + sTPDAParam)
       return ""
    
    sCampaignID = ""
    
    sSeparaAPDUForLastAPDUs = sSimcard_SeparaAPDUForLastAPDUs
    
    #print("simcardCmd_sendEnvelopeConcat - sMSL = " + sMSL)
    
    sReturnt = simcardCmd_sendEnvelope_ResponseFirstByteCommand(cardservice, sLogFileName, "", sTPDAParam, sCMD, sTAR, bNetworkOKOrChangeIMEIOrChangeMCCMNC, sMCC, sMNC, sMSL, sKIC, sKID, sCounter)
    sReturn = sReturnt[0]
    #print("simcardCmd_sendEnvelopeConcat - sReturn: " + sReturn)
    
    if len(sReturnt) > 1:
       sCampaignID = sReturnt[1]

    log_write_InfoInBlue(sLogFileName, "ANALYSIS RESULT: START ----------------------------------------------------------------")
    
    if sReturn != "":
       
       #print("sReturn: " + sReturn)

       nResp = str_CountPattern(sReturn, sSeparaAPDUForLastAPDUs)
       
       #print("simcardCmd_sendEnvelopeConcat - sReturn = " + str(sReturn))
       #print("simcardCmd_sendEnvelopeConcat - sSeparaAPDUForLastAPDUs = " + str(sSeparaAPDUForLastAPDUs))
       
       n = 0
       m = 0
       sAPDU = str_GetENTER()
       while n < nResp:
          sT = str_getSubStringFromOcur(sReturn, sSeparaAPDUForLastAPDUs, n) 
          if sT != "":
             sAPDU = sAPDU + str_GetENTER() + sAsteric + str(m) + ". " + sT
             sTDes = simcard_StatusCommandALLResponses_TerminalResponseGetDesOnly(sT, True)
             if sTDes != "":
                sAPDU = sAPDU + " - Description: " + sTDes
             sAPDU = sAPDU + str_GetENTER()
             m = m + 1
          n = n + 1                          
    
       sTemp = "Total answers received from the SIM and saved for reporting: " + str(m)
       sReturnDes = sReturnDes + sTemp 

       #print("simcardCmd_sendEnvelopeConcat - sAPDU = " + str(sAPDU))
          
       log_write_WarningInYellow(sLogFileName, sTemp)
       sReturnDes = sReturnDes + sAPDU + str_GetENTER()
       log_write_WarningInYellow(sLogFileName, sAPDU)
       
       sReturn = str_ReplaceWord(sReturn, sSeparaAPDUForLastAPDUs, sSimcard_SeparaAPDUForLastAPDUs_Visible)
       sReturn = str_ReplaceWord(sReturn, sSimcard_SeparaAPDUForLastAPDUs_Visible + sSimcard_SeparaAPDUForLastAPDUs_Visible, sSimcard_SeparaAPDUForLastAPDUs_Visible)
       log_write_OKInGreen(sLogFileName, "Reponse all Together, where each response is separated by '-': " + str_GetENTER() + sReturn)
                
    log_write_InfoInBlue(sLogFileName, "ANALYSIS RESULT: END ----------------------------------------------------------------")
        
    table = PrettyTable()

    if sReturn == "":
       table.add_column(sCMD + " COMMAND", ["ERROR"])
    else:   
       table.add_column(sCMD + " COMMAND", ["EXECUTED AND OK"])
 
    table_str = table.get_string()
    log_write(sLogFileName, "\n"+table_str)

    if sSimcard_LastEnvelope != "":
       sLastEnvelope = sSimcard_LastEnvelopeHeader  
       
       #print("simcardCmd_sendEnvelopeConcat - sLastEnvelope: " + str(sLastEnvelope))
       
       if "\n" in sSimcard_LastEnvelope:
       #if sSimcard_3GPP23048_DesBefore not in sLastEnvelope:
          
          sLastEnvelope = sLastEnvelope + "\n"
          sTemp = str_getSubStringFromOcur(sSimcard_LastEnvelope, "\n", 0)
          if sTemp != "":
             sLastEnvelope = sLastEnvelope +  sSimcard_3GPP23048_DesBefore + ": 0x" + simcard_BytesWithLenDes(sTemp)
             sLastEnvelope = sLastEnvelope +  " - " + sSimcard_Header3GPP23040 + " Format only: 0x" + simcard_BytesWithLenDes(simcard_APDU_Get3GPP23040(sTemp))
             
          sTemp = str_getSubStringFromOcur(sSimcard_LastEnvelope, "\n", 1)
          if sTemp != "":
             sLastEnvelope = sLastEnvelope + "\n"
             sLastEnvelope = sLastEnvelope + sSimcard_3GPP23048_DesAfter + ": 0x" + simcard_BytesWithLenDes(sTemp)
             sLastEnvelope = sLastEnvelope +  " - " + sSimcard_Header3GPP23040 + " Format only: 0x" + simcard_BytesWithLenDes(simcard_APDU_Get3GPP23040(sTemp))

          #print("simcardCmd_sendEnvelopeConcat - sTemp: " + str(sTemp))
             
       else:
          sLastEnvelope = sLastEnvelope + "0x" + simcard_BytesWithLenDes(sSimcard_LastEnvelope)
          sLastEnvelope = sLastEnvelope +  " - " + sSimcard_Header3GPP23040 + " Format only: 0x" + simcard_BytesWithLenDes(simcard_APDU_Get3GPP23040(sSimcard_LastEnvelope))
          
       sReturnDes = sReturnDes + sAsteric + sLastEnvelope + str_GetENTER()
       log_write_WarningInYellow(sLogFileName, sLastEnvelope)

    #print("sReturn: " + sReturn + " - sReturnDes: " + sReturnDes)
    
    return sReturn, sReturnDes
  
# simcardCmd_sendEnvelope_ResponseFirstByteCommand ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcardCmd_sendEnvelope_ResponseFirstByteCommand(cardservice, sLogFileName, sCmd, sTPDAParam, sAPDU, sTAR=sSimcard_sDefTAR_COTA, bNetworkOKOrChangeIMEIOrChangeMCCMNC=True, sMCC="", sMNC="", sMSL=sSimcard_MSLDefNoSecurity, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter):
    time()
    sCmd = str_SpacesOut(sCmd).upper()
    sAPDU = str_SpacesOut(sAPDU).upper()
    
    sCampaignID = ""
    if len(sAPDU) > 2 and (len(sCmd) > 0 and str_left(sAPDU, len(sCmd)) != sCmd):
       sCampaignID = str_left(sAPDU,4)
    
    sReturn = ""
    
    sSeparaAPDUForLastAPDUs = sSimcard_SeparaAPDUForLastAPDUs
    sResAndSW1SW2 = simcard_SendEnvelopeContinuos(cardservice, sLogFileName, sTPDAParam, sAPDU, sSeparaAPDUForLastAPDUs, sTAR, bNetworkOKOrChangeIMEIOrChangeMCCMNC, sMCC, sMNC, sMSL, sKIC, sKID, sCounter)
    
    #print("simcardCmd_sendEnvelope_ResponseFirstByteCommand - sResAndSW1SW2: " + str(sResAndSW1SW2))
    
    if sResAndSW1SW2 != "":
        sResAndSW1SW2 = str_SpacesOut(sResAndSW1SW2)
        sLog = str_ReplaceWord(sResAndSW1SW2, "_", "")
        sLog = "RESULT SW1 AND SW2: " + str_AddSpaceHexa(sLog)
        #log_write_Normal(sLogFileName, sLog)
        
        #VALIDATION 
        if len(sResAndSW1SW2) <= 4:
            sLog = "COULD NOT GET DATA FOR"
            if sCmd != "":
               sLog = sLog + " COMMAND '" + sCmd + "'"
            if sAPDU != "":
               if sCmd != "":
                  sLog = sLog + " and"
               sLog = sLog + " APDU '" + str_AddSpaceHexa(sAPDU) + "'"
            sLog = sLog + ". WRONG PARAMETER(S): Applet with TAR: 0x" + str_AddSpaceHexa(sTAR) + " does not support APDU"
            sLog = sLog + ", or TPDA is not correct: 0x" + str_AddSpaceHexa(sTPDAParam) 
            sLog = sLog + ", or the APPLET VERSION does not support command: 0x" + str_AddSpaceHexa(sCmd) + "." 
            log_write_WarningInYellow(sLogFileName, sLog)      

            return sResAndSW1SW2, ""
        
        else:
            log_write_OKInGreen(sLogFileName,"COMMAND SUCCESSFULLY EXECUTED")
           
            sAPDUt = ""
            sD = ""
            nPat = str_CountPattern(sResAndSW1SW2, sSeparaAPDUForLastAPDUs)
            if nPat<=0:
               nPat = 1

            #print("COTACmd_sendEnvelope_ResponseFirstByteCommand sResAndSW1SW2: " + str(sResAndSW1SW2))
            # ---------------------------------------------------------------------------------------------------
            #ADDED 2025-05-13: Because SMS Data: 0x02 71 00 00 0B 0A 99 99 99 00 00 00 00 01 00 09
            tsResAndSW1SW2 = sResAndSW1SW2.split(sSeparaAPDUForLastAPDUs)
            nsResAndSW1SW2 = len(tsResAndSW1SW2)
            sResAndSW1SW2 = ""
            n = 0
            while n < nsResAndSW1SW2:
                  tsResAndSW1SW2[n] = simcard_Clean9000(tsResAndSW1SW2[n])
                  sResAndSW1SW2 = sResAndSW1SW2 + sSeparaAPDUForLastAPDUs + tsResAndSW1SW2[n]
                  n = n + 1
            sResAndSW1SW2 = str_midToEnd(sResAndSW1SW2, len(sSeparaAPDUForLastAPDUs))
            #print("COTACmd_sendEnvelope_ResponseFirstByteCommand sResAndSW1SW2: " + str(sResAndSW1SW2))
            # ---------------------------------------------------------------------------------------------------
            
            sSendSMS = ""
            nSendSMS = 0
               
            if sCmd=="":
               sD = sResAndSW1SW2
            else:      
               n = 0
               while n < nPat:
                     print("simcardCmd_sendEnvelope_ResponseFirstByteCommand - n = " + str(n))   
                     
                     sAPDUt = str_getSubStringFromOcur(sResAndSW1SW2, sSeparaAPDUForLastAPDUs, n)
                     #print("simcardCmd_sendEnvelope_ResponseFirstByteCommand - sAPDUt: " + sAPDUt)
                     sAPDUtD = str_getSubStringFromWithoutPattern(sAPDUt, sCmd)
                     #print("simcardCmd_sendEnvelope_ResponseFirstByteCommand - sAPDUtD: " + sAPDUtD)

                     #GET SEND SMS
                     if sAPDUt != "":
                        #print("simcardCmd_sendEnvelope_ResponseFirstByteCommand - sAPDUt = " + str(sAPDUt))
                        stpud = simcard_SendSMSCmd_Interpret_GetTPUD(sAPDUt)
                        #print("stpud = " + str(stpud))
                        if stpud != "":
                           nSendSMS = nSendSMS + 1
                           sSendSMS = sSendSMS + sSeparaAPDUForLastAPDUs + str(nSendSMS) + ". " + str_AddSpaceHexa(stpud) + " " + sSimcard_SendSMSDATAPatternASCII + " " + bytes_HexaToASCII(stpud)
                           #print("nSendSMS = " + str(nSendSMS) + " - sSendSMS = " + str(sSendSMS))
                                    
                     if sAPDUtD != "":
                     
                        if str_left(sAPDUtD, 1) != str_left(sCmd, 1):
                           sAPDUtD = str_left(sCmd, 1) + sAPDUtD
                        
                        #print("sAPDUtD: " + sAPDUtD)
                        if str_left(sAPDUtD, 2) == sCmd:
                           #RESPONSE D COMMAND
                           #print("COTACmd_sendEnvelope_ResponseFirstByteCommand sAPDUtD: " + str(sAPDUtD))
                           sD = sAPDUtD
                     
                     n = n + 1
            
            #print("sD: " + sD)
            #print("sCmd: " + sCmd)
                 
            if sD == "" and sCmd!="":
               log_write_WarningInYellow(sLogFileName, "There is no response with the command 0x" + str_AddSpaceHexa(sCmd) + " in a SMS, APDU: " + str_AddSpaceHexa(sAPDU) + ". All Responses separated by character '" + sSeparaAPDUForLastAPDUs + "': " + sResAndSW1SW2)
               sD = sResAndSW1SW2
            else:
            
                 #print("COTACmd_sendEnvelope_ResponseFirstByteCommand sD: " + sD)
                 #if sD != "" and sCmd=="":
                 #   #sD = str_ReplaceWord(sD, sSimcard_9000, sSeparaAPDUForLastAPDUs)
                 #   print("COTACmd_sendEnvelope_ResponseFirstByteCommand sD: " + sD + " - sSeparaAPDUForLastAPDUs = " + str(sSeparaAPDUForLastAPDUs) + " sSeparaAPDUForLastAPDUs Len = " + str(len(sSeparaAPDUForLastAPDUs)) + " - sCmd=" + sCmd)
                 #else:
                 #   #sD = str_CleanWord(sD, sSimcard_9000)
                 #   print("COTACmd_sendEnvelope_ResponseFirstByteCommand sD: " + sD + " - str_CleanWord")
                 #print("COTACmd_sendEnvelope_ResponseFirstByteCommand sD: " + sD)
                 
                 sLog = ""
                 if sCmd!="":
                    sLog = sLog + sCmd + " "
                 sLog = sLog + "OK." 
                 if sCampaignID != "":
                    sLog = sLog + str_GetENTER() + simcardCampaignID_Des(sCampaignID)
                 sLog = sLog + str_GetENTER() + "Responses: "
                 
                 sResAndSW1SW2T = sResAndSW1SW2.split(sSeparaAPDUForLastAPDUs)
                 n = 0
                 while n < len(sResAndSW1SW2T):
                       if sResAndSW1SW2T[n] != "":
                          sLog = sLog + str_GetENTER() + "- Response " + str(n) + ": " + bytes_LengthDescriptionAndData(sResAndSW1SW2T[n])
                       n = n + 1
                 
                 log_write_InfoInBlue(sLogFileName, sLog)
                 
            if sSendSMS != "":
               #print("sSendSMS = " + str(sSendSMS))
               sLog = str_Replace(sSendSMS, sSeparaAPDUForLastAPDUs, str_GetENTER())
               sLog = "Total Send SMS sent: " + str(nSendSMS) + " - TP-UD sent: " + sLog
               log_write_InfoInBlue(sLogFileName, sLog)
                 
                 
            return sD, sCampaignID
                
    else:
        sLog = "COULD NOT DISPLAY DATA WRONG PARAMETER(S) CHECK THE SHORT NUMBER OR THE APPLET VERSION" 
        log_write_WarningInYellow(sLogFileName, sLog)

        return "", ""

# simcardCampaignID_Des ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcardCampaignID_Des(sCampaignID):
    sCampaignID = str_SpacesOut(str(sCampaignID)).upper()
    sReturn = ""
    if sCampaignID != "":
       sReturn = "Campaign ID: 0x" + str_SpaceHexa(sCampaignID) + " - Decimal: " + str(bytes_NumberFromHex(sCampaignID))
    return sReturn    

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MSL Methods with security
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# simcard_PrepareAPDUWithSecurity ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_PrepareAPDUWithSecurity(sEnvelope, sAPDU, sTAR=sSimcard_sDefTAR_COTA, sMSL=sSimcard_MSLDefMAC, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter):

    sAPDU = str_SpacesOut(sAPDU)
    sEnvelope = str_SpacesOut(sEnvelope)
    
    if sAPDU == "":
       return False, "APDU for SMPP is Null."
       
    bReturn = True
    
    #print("simcard_PrepareAPDUWithSecurity - sMSL=" + sMSL + " - sSimcard_MSLDefMAC=" + sSimcard_MSLDefMAC)
    
    if str_left(sMSL, 2) != str_left(sSimcard_MSLDefNoSecurity, 2):
       #print("simcard_PrepareAPDUWithSecurity - sAPDU = " + sAPDU + " - sTAR= " + sTAR + " - sMSL = " + sMSL + " - sKIC = " + sKIC + " - sKID = " + sKID + " - sCounter = " + sCounter)
       
       #CHECK KIC AND KID
       bReturn, sKIC = simcard_PrepareAPDUWithSecurity_KeyValidation(sKIC, 0, sSimcard_MSLDefKICName)
       if bReturn==False:
          return bReturn, sKIC

       #print("simcard_PrepareAPDUWithSecurity - sKIC = " + str(sKIC))
          
       bReturn, sKID = simcard_PrepareAPDUWithSecurity_KeyValidation(sKID, 0, sSimcard_MSLDefKIDName)
       if bReturn==False:
          return bReturn, sKID

       #print("simcard_PrepareAPDUWithSecurity - sKID = " + str(sKID))

       # Validate Counter       
       bReturn, sCounter = simcard_PrepareAPDUWithSecurity_KeyValidation(sCounter, 5, sSimcard_MSLDefCounterName)
       if bReturn==False:
          return bReturn, sCounter
       
       # Validate MSL
       bReturn, sMSL = simcard_PrepareAPDUWithSecurity_KeyValidation(sMSL, 4, sSimcard_MSLDefMSLName)
       if bReturn==False:
          return bReturn, sMSL

       sCounterPadding = "00"

       #print("simcard_PrepareAPDUWithSecurity - MSL = " + str(sMSL))
       
       # * Header Length + Header: 0x16 (22 bytes)
       # * Header Length: 0x15 (21 bytes)
       # * MSL = 4 bytes, example: 0x02 01 51 51
       # * TAR = 3 bytes, example: 0x00 00 00
       # * Counter = 5 bytes, example: 0x00 00 00 00 00 00
       # * Counter Padding = 1 byte, example: 00
       # * MAC = 8 bytes
       # * Total Header: 4 + 3 + 5 + 1 + 8 = 21 bytes

       sHeaderLength = "15"
       nHeaderLengh = 22

       # * When there is no MAC, the length is 14 bytes
       # * Header Length + Header: 0x0F (15 bytes)
       # * Header Length: 0x0E (14 bytes)
       # * MSL = 4 bytes, example: 0x00 00 51 51
       # * TAR = 3 bytes, example: 0x00 00 00
       # * Counter = 5 bytes, example: 0x00 00 00 00 00 00
       # * Counter Padding = 1 byte, example: 00
       # * Total Header: 4 + 3 + 5 + 1 = 13 bytes

       sSPI1 = str_left(sMSL, 2)
       if sSPI1 == "00":
          nHeaderLengh = nHeaderLengh - 8
          sHeaderLength = bytes_NroToHexa(nHeaderLengh - 1)

       # * MSG ALL LEN: 21 bytes for Header Length + APDU Length
       # * Example:
       # //   sDataForMAC = "0041 15 02015151 B00010 000000000000 A0A40000023F00A0A40000027F20A0A40000026F46A0D600001100545850FFFFFFFFFFFFFFFFFFFFFFFFFF";
       # //   sExpectedResultMAC="255C5A5CDDD5D95D";

       sMsgAllLen = bytes_NroToHexa((len(sAPDU) // 2) + nHeaderLengh)
       
       sMsgAllLen = bytes_fHexaWithPaddingZerosToTheLeft(sMsgAllLen, 2)
    
       sResult = sMsgAllLen + sHeaderLength + sMSL + sTAR + sCounter + sCounterPadding + sAPDU
        
       sDataForMAC = sResult
       sMAC = ""
    
       sResult = ""

       #print("simcard_PrepareAPDUWithSecurity - sDataForMAC = " + str(sDataForMAC) + " - MSL=" + str(sMSL))
       
       # 'MAC GENERATION
       if simcard_fPrepare_23_048_Msg_IsMSLSPI1WithCC(sMSL):
       
          #print("simcard_PrepareAPDUWithSecurity - MAC Generation = " + str(sMSL))
       
          # /*
          #  * NOTE:
          #  * Taking into account some testings with tools such as SIMAlliance Loader and/or Gemalto Loader
          #  * When the length is multiple of 8 bytes the MAC is generated with ALG_DES_MAC8_NOPAD
          #  * When the length is NOT multiple of 8 bytes the MAC is generated with ALG_DES_MAC8_ISO9797_M1
          #  */
          #if ((len(sDataForMAC) // 2) % 8) == 0: => NOT USED ANYMORE
          bReturn, sMAC = algo_3DES_CBC_MAC_ISO9797M1(True, sKID, sDataForMAC)
          if bReturn == False:
             return bReturn, sMAC  
            
          sResult = sMsgAllLen + sHeaderLength + sMSL + sTAR + sCounter + sCounterPadding + sMAC + sAPDU

          #print("simcard_PrepareAPDUWithSecurity - MAC = " + str(sMAC))
          

       # 'MAC GENERATION + ENCRYPTION
       if simcard_fPrepare_23_048_Msg_IsMSLSPI1WithCCAndEncryption(sMSL):

          #print("simcard_PrepareAPDUWithSecurity - sDataForMAC = " + str(sDataForMAC))
          
          sDataForMACWithPadding, sPadding = simcard_fPrepare_23_048_Msg_DataWithPaddingForMAC(sDataForMAC)

          #print("simcard_PrepareAPDUWithSecurity - sDataForMACWithPadding = " + str(sDataForMACWithPadding) + " sPadding = " + str(sPadding) + " - sDataForMAC = " + str(sDataForMAC))

          bReturn, sMAC = algo_3DES_CBC_MAC_ISO9797M1(True, sKID, sDataForMACWithPadding)
          if bReturn == False:
             return bReturn, sMAC  
          
          #print("simcard_PrepareAPDUWithSecurity - algo_3DES_CBC_MAC_ISO9797M1 sMAC = " + str(sMAC) + " - sKID = " + str(sKID) + " - sDataForMACWithPadding = " + str(sDataForMACWithPadding))

          #'//ADD MAC to DATA FOR ENCRYPTION, ALREADY PREPARED WITH PADDING
          #'//  Removing CPI + CPL + CHI + CHL + SPI + KIC + KID + TAR
          sRemoving = str_midToEnd(sDataForMACWithPadding, 20)
          #'//  Keeping CNTR + PCNTR + RC/CC/DS (MAC) + Data with Padding
          sDataForMACWithPadding = str_left(sRemoving, 12) + sMAC + str_midToEnd(sRemoving, 12)
          
          #print("simcard_PrepareAPDUWithSecurity - sDataForMACWithPadding = " + str(sDataForMACWithPadding) + " - sRemoving = " + str(sRemoving))
          
          #MSL = 0x06
          #A0 C2 00 00 6F D1 6D 02 02 83 81 06 06 98 33 11 11 11 11 0B 5F E4 0A 98 33 11 11 11 11 7F 16 10 03 07 12 41 38 92 4D 02 70 00 00 48 15 06 01 15 15 B0 00 10 04 68 42 93 41 09 4D 3C 16 D3 08 AB 88 DC D9 87 70 CC 3D FE 25 C6 00 7F 40 AF 00 EE 79 5C 12 E1 CA 48 63 31 2E 52 96 53 30 51 EC 73 AB 62 CC C3 B0 9C 76 C7 B2 3A 7E 53 0E 8F B2 ED CE 3C FF E2
          #  A0 C2 00 00 6F D1 6D 02 02 83 81 06 06 98 33 11 11 11 11 0B 5F E4 0A 98 33 11 11 11 11 7F 16 10 03 07 12 41 38 92 4D
          #  02 70 00
          #  00 48 = CPL => 0x48 = 72 bytes. After TAR, there are 72 bytes with encrypted data.
          #  15 = CHL (Command Header Length = 21 bytes (MSL + TAR + COUNTERS + MAC)
          #  06 01 15 15 = MSL
          #  B0 00 10 = TAR
          #  04 68 42 93 41 09 4D 3C 16 D3 08 AB 88 DC D9 87 70 CC 3D FE 25 C6 00 7F 40 AF 00 EE 79 5C 12 E1 CA 48 63 31 2E 52 96 53 30 51 EC 73 AB 62 CC C3 B0 9C 76 C7 B2 3A 7E 53 0E 8F B2 ED CE 3C FF E2
          #  For Encryption:
          #  KIC: 00112233445566770011223344556677
          #  KID: 00112233445566770011223344556677

          #print("simcard_PrepareAPDUWithSecurity - sDataForMACWithPadding = " + str(sDataForMACWithPadding) + " - sKIC = " + str(sKIC))
            
          bReturn, sDataResult = algo_3DES_CBC_ISO9797M1(True, sKIC, sDataForMACWithPadding)
          if bReturn == False:
             return bReturn, sDataResult  

          #print("simcard_PrepareAPDUWithSecurity - algo_3DES_CBC_ISO9797M1 sDataResult = " + str(sDataResult))

          #'//Taking into account the CPL, it is defined with the encrypted data, not the CHL (Command Header Length) and CH (Command Header)
          #'//00 48 = CPL => 0x48 = 72 bytes. After TAR, there are 72 bytes with encrypted data.

          sMsgAllLen = bytes_NroToHexa(len(sHeaderLength + sMSL + sTAR + sDataResult) // 2)
          sMsgAllLen = bytes_LengthInHexaWithZerosToTheLeft_FromHexaLen(sMsgAllLen, 2)
          sResult = sMsgAllLen + sHeaderLength + sMSL + sTAR + sDataResult

     
       # COMPLETE ENVELOPE TAKING INTO ACCOUNT RESULT ACCORDNG TO SPI1 FROM MSL
       if sResult != "":
     
          #print("simcard_PrepareAPDUWithSecurity - sEnvelope = " + str(sEnvelope))
          #print("simcard_PrepareAPDUWithSecurity - sResult = " + str(sResult))

          #Prepare Enelope
          # Example 1 Envelope: 
          # A0C200003AD138020283810604812143F50B2C4405810601F47FF6000000000000001C 0270000017150221151543504100000000010048E92A1C09DD0699FB
          # Example 2 - Evelope: 
          # 80C2000096D18193020283810607914306071901F00B818344098106071901F07FF60000000000000071027000006C1502211515000000000000000000937DB232A8AF4D6B80E60C00511043445241540201010120030048454C001043445241540201010120030048454C011043445241540201010120030048454C0101001AEF08C7020000C8020000EA0C800AFF001001000000000000C90000
          
          #s0270_Before = str_getSubStringFromOcur(sEnvelope, s0270, 0)
          
          #print("simcard_PrepareAPDUWithSecurity - sEnvelope = " + str(sEnvelope))
          
          s0270_Before, s0270 = simcard_APDU_Get3GPP23040_Process(sEnvelope, True)
          #print("simcard_PrepareAPDUWithSecurity - s0270_Before = " + str(s0270_Before) + " - " + str(s0270))

          #Removed length so that it is added with the MAC
          if s0270_Before!="":
             s0270_Before = str_left(s0270_Before, len(s0270_Before)-2)

             #print("simcard_PrepareAPDUWithSecurity - s0270_Before = " + str(s0270_Before))
          
             #APDU first 4 bytes
             sFirst4Bytes = str_left(s0270_Before, 8)
             # TAKE AFTER CLA + INS + P1 + P2 + Len
             s0270_BeforeNoAPDUFirst4Bytes = str_midToEnd(s0270_Before, 10)

             #Added 0x02 70 + data => Length and Concatenate bytecode
             #print("simcard_PrepareAPDUWithSecurity - s0270_BeforeNoAPDUFirst4Bytes = " + str(s0270_BeforeNoAPDUFirst4Bytes))
             #print("simcard_PrepareAPDUWithSecurity - len(s0270 + sResult) // 2 = " + str((len(s0270) + len(sResult)) // 2))
          
             sAPDUData = s0270_BeforeNoAPDUFirst4Bytes + bytes_NroToHexa(len(s0270 + sResult) // 2) + s0270 + sResult
             #print("simcard_PrepareAPDUWithSecurity - sAPDUData = " + str(sAPDUData))

             # Update data length after 3GPP 51-014 SMS TPDU Tag = 0x0B
          
             sAPDUData_Before = str_getSubStringFromOcur(sAPDUData, sSimcard_3GPP51014_SMS_TPDU_tag, 0)
             sAPDUData_After = str_midToEnd(sAPDUData, len(sAPDUData_Before))

             #print("simcard_PrepareAPDUWithSecurity - sAPDUData_Before = " + str(sAPDUData_Before))
             #print("simcard_PrepareAPDUWithSecurity - sAPDUData_After = " + str(sAPDUData_After))

             #Calculate Length after SMS TPDU Tag = 0x0B          
             if str_left(sAPDUData_After, len(sSimcard_3GPP51014_SMS_TPDU_tag)) == sSimcard_3GPP51014_SMS_TPDU_tag:
                #Remove SMS TPDU Tag = 0x0B + Data Length
                sAPDUData_After = str_midToEnd(sAPDUData_After, len(sSimcard_3GPP51014_SMS_TPDU_tag)+2)
             
             #print("simcard_PrepareAPDUWithSecurity - len(sAPDUData_After) = " + str(len(sAPDUData_After)))
          
             sAPDUData_After = sSimcard_3GPP51014_SMS_TPDU_tag + simcard_GetLengthInHexaBiggerThan127(sAPDUData_After) + sAPDUData_After
             sAPDUData = sAPDUData_Before +  sAPDUData_After 

             #Calculate Length after BER-TLV SMPP Download Tag = 0xD1          
             if str_left(sAPDUData,2) == sSimcard_BERTLV_SMPP_download_tag:
                #Remove BER-TLV SMPP Download Tag = 0xD1 + Data Length
                sAPDUData = str_midToEnd(sAPDUData, len(sSimcard_BERTLV_SMPP_download_tag)+2)
          
             sAPDUData = sSimcard_BERTLV_SMPP_download_tag + simcard_GetLengthInHexaBiggerThan127(sAPDUData) + sAPDUData

             #print("simcard_PrepareAPDUWithSecurity - sAPDUData = " + str(sAPDUData))

             #Finish new Envelope
             sEnvelope = sFirst4Bytes + bytes_NroToHexa(len(sAPDUData) // 2) + sAPDUData
          
          else:
             sEnvelope = bytes_NroToHexa(len(s0270 + sResult) // 2) + s0270 + sResult

    sEnvelope = str_SpacesOut(sEnvelope)

    #print("simcard_PrepareAPDUWithSecurity - sEnvelope = " + str(sEnvelope))
    
    return bReturn, sEnvelope


# simcard_PrepareAPDUWithSecurity_KeyValidation ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_PrepareAPDUWithSecurity_KeyValidation(sValue, nValueLen=0, sDes=""):

    sValue = str_SpacesOut(sValue)

    if sDes=="":
       sDes = "Key"

    if sDes.upper() == sSimcard_MSLDefKICName:
       sDes = sSimcard_MSLDefKICName
       if len(sValue) <= 0:
          sValue = sSimcard_MSLDefKIC

    if sDes.upper() == sSimcard_MSLDefKIDName:
       sDes = sSimcard_MSLDefKIDName
       if len(sValue) <= 0:
          sValue = sSimcard_MSLDefKID

    if sDes.upper() == sSimcard_MSLDefCounterName:
       sDes = sSimcard_MSLDefCounterName
       if len(sValue) <= 0:
          sValue = sSimcard_MSLDefCounter

    if sDes.upper() == sSimcard_MSLDefMSLName:
       sDes = sSimcard_MSLDefMSLName
       if len(sValue) <= 0:
          sValue = sSimcard_MSLDefMACAndEncrypt

    #print("simcard_PrepareAPDUWithSecurity_KeyValidation - sValue = " + str(sValue) + " - sDes = " + str(sDes))
    
    bReturn, sError = simcard_ValidateHexa(sValue, sDes)

    #print("simcard_PrepareAPDUWithSecurity_KeyValidation - bReturn = " + str(bReturn) + " - sDes = " + str(sError))

    if not bReturn:
       return bReturn, sError

    if nValueLen == 0:
       if (len(sValue) == 16 or len(sValue) == 32 or len(sValue) == 48) == False:
          return False, sDes + " must be an hexadecimal value with 8, 18 or 24 bytes. Value = " + sValue
   
       if len(sValue) == 16:
          sValue = sValue + sValue
    else:
       bReturn, sError = simcard_ValidateParamData(sValue, sDes)
       if not bReturn:
          return bReturn, sError
        
    return True, sValue
    
    
# simcard_fPrepare_23_048_Msg_IsMSLSPI1WithCC ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_fPrepare_23_048_Msg_IsMSLSPI1WithCC(sMSL):
    return simcard_fPrepare_23_048_Msg_IsMSLSPI1WithFlag(sMSL, sSimcard_MSL_SP1_MAC, False)

# simcard_fPrepare_23_048_Msg_IsMSLSPI1WithCCAndEncryption ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_fPrepare_23_048_Msg_IsMSLSPI1WithCCAndEncryption(sMSL):
    return simcard_fPrepare_23_048_Msg_IsMSLSPI1WithFlag(sMSL, sSimcard_MSL_SP1_MACAndEncryption, False)

# simcard_fPrepare_23_048_Msg_IsMSLSPI1WithCCAndEncryption ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_fPrepare_23_048_Msg_IsMSLSPI1WithCounterBigger(sMSL):
    return simcard_fPrepare_23_048_Msg_IsMSLSPI1WithFlag(sMSL, sSimcard_MSL_SP1_CounterBigger, True)
    
# simcard_fPrepare_23_048_Msg_IsMSLSPI1WithFlag ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_fPrepare_23_048_Msg_IsMSLSPI1WithFlag(sMSL, sFlag, bFisrtDigitCheck=False):
    
    bReturn = False
    
    sMSL = str_SpacesOut(sMSL)

    if len(sMSL) < 1:
       return False
       
    #print("1.simcard_fPrepare_23_048_Msg_IsMSLSPI1WithFlag - sMSL = " + str(sMSL) + " - sFlag = " + str(sFlag))
  
    nFlagStart = 0
    if bFisrtDigitCheck == False:
       #SPI1 len is 2 characers
       if len(sFlag)==1:
          #SPI1 len is 2 characers, but it is analized 2nd nibble
          nFlagStart = nFlagStart + 1

       #print("2.simcard_fPrepare_23_048_Msg_IsMSLSPI1WithFlag - sMSL = " + str(sMSL) + " - sFlag = " + str(sFlag))
       
    if len(sMSL) >= (nFlagStart + len(str(sFlag))):
       sDataProcess = str_mid(sMSL, nFlagStart, len(sFlag))

       #print("2.5.simcard_fPrepare_23_048_Msg_IsMSLSPI1WithFlag - sMSL = " + str(sMSL) + " - sFlag = " + str(sFlag) + " - sDataProcess=" + str(sDataProcess))

       if str(sDataProcess) == str(sFlag):
          #print("2.6.simcard_fPrepare_23_048_Msg_IsMSLSPI1WithFlag - sMSL = " + str(sMSL) + " - sFlag = " + str(sFlag) + " - sDataProcess=" + str(sDataProcess))
          bReturn = True

    #print("3.simcard_fPrepare_23_048_Msg_IsMSLSPI1WithFlag - sMSL = " + str(sMSL) + " - sFlag = " + str(sFlag) + " - bReturn=" + str(bReturn))
    
    return bReturn


# simcard_fPrepare_23_048_Msg_IsMSLSPI1WithFlag ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_fPrepare_23_048_Msg_DataWithPaddingForMAC(sData):
    sData = str_SpacesOut(sData)
    
    sDataT = sData

    #'//Removing  CPI + CPL + CHI + CHL + SPI + KIC + KID + TAR, for padding calculation
    sHeader = str_left(sDataT, 20)
    sDataT = str_midToEnd(sDataT, 20)

    #print("simcard_fPrepare_23_048_Msg_DataWithPaddingForMAC - sDataT=" + str(sDataT))
    
    #'//Padding of octects for encryption
    nPCNTR = (len(sDataT) // 2) % 8
    
    #print("simcard_fPrepare_23_048_Msg_DataWithPaddingForMAC - nPCNTR=" + str(nPCNTR))
    
    sReturn = ""
    sPadding = ""
    
    if nPCNTR == 0:
       nPCNTR = 8
        
    if nPCNTR > 0:
        
        nPadding = (8 - nPCNTR)
        sPCNTR = bytes_NroToHexa(nPadding)
        sTemp = str_left(sDataT, 10)
        
        sDataT = sTemp + sPCNTR + str_midToEnd(sDataT, 12)
        
        sPadding = str_RepeatString(nPadding * 2, "0")
        sReturn = sDataT + sPadding
        
        sLen = str_mid(sHeader, 2, 2)
        nLen = bytes_HexaToNro(sLen)
        
        nLenResult = int(nLen) + int(nPadding)
        
        sReturn = str_left(sHeader, 2) + bytes_NroToHexa(nLenResult) + str_midToEnd(sHeader, 4) + sReturn

    #print("simcard_fPrepare_23_048_Msg_DataWithPaddingForMAC - sReturn=" + str(sReturn) + " - sPadding=" + str(sPadding))
        
    return sReturn, sPadding            


# simcard_PrepareAPDUWithSecurity_Testing ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_PrepareAPDUWithSecurity_Testing():
    #TESTING
    sEnvelope = "80 C2 00 00 32 D1 30 02 02 83 81 06 04 81 06 01 F5 0B 24 40 05 81 06 01 F4 7F F6 00 00 00 00 00 00 00 14 02 70 00 00 0F 0D 00 00 00 00 43 50 41 00 00 00 00 01 00 FB"
    sAPDU = "FB"
    sTAR = sSimcard_sDefTAR_COTA
    #sMSL = "16211515"
    sMSL = "02211515"
    sKIC = "11111111111111112222222222222222"
    sKID = "33333333333333334444444444444444"
    sCounter = "0000000002"
    bReturn, sEnvelope = simcard_PrepareAPDUWithSecurity(sEnvelope, sAPDU, sTAR, sMSL, sKIC, sKID, sCounter)
    print("bReturn = " + str(bReturn) + " - Envelope = " + str(sEnvelope))
        

# simcard_3GPP23048_ResponseAnalisys ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_3GPP23048_ResponseAnalisys(sBytes):
    sAnalysis, sTAR, sPoR = simcard_3GPP23048_ResponseAnalisys_GetPoRAndTAR(sBytes)
    return sAnalysis

# simcard_3GPP23048_ResponseAnalisys_GetPoRAndTAR ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_3GPP23048_ResponseAnalisys_GetPoRAndTAR(sBytes):
    sBytes = str_SpacesOut(sBytes)
    
    #print("simcard_3GPP23048_ResponseAnalisys - sBytes = " + str(sBytes))
    
    if str_right(sBytes, len(sSimcard_9000)) == sSimcard_9000:
       sBytes = str_left(sBytes, len(sBytes) - len(sSimcard_9000))
    
    #print("simcard_3GPP23048_ResponseAnalisys_GetPoRAndTAR - Init - sBytes = " + str(sBytes))
    
    #02 71 00 00 0E 0A 00 00 00 00 00 00 00 01 00 00 01 6D 00
    #02 71 00 00 74 0A 00 00 00 00 00 00 00 01 00 00 01 90 00
    
    sPoR = ""
    sTAR = ""
    sResponse = ""

    if not bytes_IsHexaValid(sBytes):
       if sSimcard_ErrorListSepara in sBytes:
          sBytes = str_getSubStringFromOcurFirst(sBytes, sSimcard_ErrorListSepara)
    
    sByteRight = ""
    sByteLeft = ""

    sBytesASCII = bytes_HexaToASCII(sBytes)

    if len(sBytes) > 2:
    
       nLen = 10
       sLen = bytes_NroToHexa(nLen)
       if sLen in sBytes and not sSimcard_3GPP23040_UDH_SMPPConcat_Next in sBytes:

          #print("simcard_3GPP23048_ResponseAnalisys_GetPoRAndTAR - -0x0A exists - sBytes = " + str(sBytes))
       
          #Example 1: 0A 00 00 00 00 00 00 00 01 00 00 01 90 00...
          #Example 2: 0A 43 50 41 00 00 00 00 01 00 00
          #sTemp = str_getSubStringFromOcur(sBytes, sLen, 0)
          sTemp = bytes_str_getSubStringFromOcur(sBytes, sLen, 0)
          
          sTemp = str_midToEnd(sBytes, len(sTemp)+2)
          
          #00 00 00 00 00 00 00 01 00 00 + 01 6D 00
          sTemp = str_left(sTemp, (nLen * 2) + 6)
          #print("simcard_3GPP23048_ResponseAnalisys_GetPoRAndTAR - sTemp = " + str(sTemp))
          sTAR = str_left(sTemp, 6)
          #print("simcard_3GPP23048_ResponseAnalisys_GetPoRAndTAR - TAR = " + str(sTAR))
          sBytes = sTemp

          sByteLeft = str_left(str_right(sBytes,4), 2)
          sByteRight = str_right(sBytes,2).upper()

       else:
          if not sSimcard_3GPP23040_UDH_SMPPConcat_Next in sBytes:       
             if not (sSimcard_sDefTAR_COTA_Name in sBytesASCII or sSimcard_sDefTAR_SAPAUTH_Name in sBytesASCII) and "_" in sBytesASCII:
                sByteLeft = str_left(str_right(sBytes,4), 2)
                sByteRight = str_right(sBytes,2).upper()

       #print("simcard_3GPP23048_ResponseAnalisys_GetPoRAndTAR - Len > 2 - sBytes = " + str(sBytes))

    #else:
    #   sByteRight = sBytes
    #   sByteLeft = "00"  
           
    #print("simcard_3GPP23048_ResponseAnalisys_GetPoRAndTAR - End - sByteLeft=" + str(sByteLeft) +  " - sByteRight=" + str(sByteRight))
    
    if sByteLeft != "" and sByteRight != "":
       sPoR = sByteLeft + sByteRight
    
       sResponse = simcard_3GPP23048_ResponseAnalisys_Others(sPoR)
       if sResponse == "":
          sResponse = sSimcard_ReserveForFutureUse
     
    #print("simcard_3GPP23048_ResponseAnalisys - sByteLeft = " + str(sByteLeft) + " - sByteRight = " + str(sByteRight))
       
    return sResponse, sTAR, sPoR

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ERROR LIST MANAGEMENT - START
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# simcard_ErrorListAppend ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_ErrorListAppend(sBytes, sDes):

    global sSimcard_ErrorList
    
    if sBytes!="" and sDes!="":
       sSimcard_ErrorList.append(sBytes + sSimcard_ErrorListSepara + sDes)
    
    return len(sSimcard_ErrorList)   

# simcard_ErrorListSet ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_ErrorListSet():

    global sSimcard_ErrorList

    simcard_ErrorListAppend("0000", "Smartcard: 23.048 PoR OK.")
    simcard_ErrorListAppend("0001", "Smartcard: 23.048 RC/CC/DS failed.")
    simcard_ErrorListAppend("0002", "Smartcard: 23.048 CNTR low.")
    simcard_ErrorListAppend("0003", "Smartcard: 23.048 CNTR high.")
    simcard_ErrorListAppend("0004", "Smartcard: 23.048 CNTR Blocked.")
    simcard_ErrorListAppend("0005", "Smartcard: 23.048 Ciphering error.")
    simcard_ErrorListAppend("0006", "Smartcard: 23.048 Unidentified security error. This code is for the case where the Receiving Entity cannot correctly interpret the Command Header and the Response Packet is sent unciphered with no RC/CC/DS.")
    simcard_ErrorListAppend("0007", "Smartcard: 23.048 Insufficient memory to process incoming message.")
    simcard_ErrorListAppend("0008", "Smartcard: 23.048 This status code 'more time' should be used if the Receiving Entity/Application needs more time to process the Command Packet due to timing constraints. In this case a later Response Packet should be returned to the Sending Entity once processing has been completed.")
    simcard_ErrorListAppend("0009", "Smartcard: 23.048 TAR Unknown.")
    simcard_ErrorListAppend("000A", "Smartcard: 23.048 Insufficient security level.")

    simcard_ErrorListAppend("61XX", "Response data incomplete, 'XX' more bytes available.")

    simcard_ErrorListAppend("6200", "ISO 7816: Not information given according to ISO 7816-4.")
    simcard_ErrorListAppend("6281", "ISO 7816: Part of returned data may be corrupted according to ISO 7816-4.")
    simcard_ErrorListAppend("6282", "Contactless: End of data reached before Le bytes (Le is greater than data length).")
    simcard_ErrorListAppend("6283", "Smartcard: Selected applet blocked, or the Card Manager applet is selected and it is locked, or Card Life Cycle State is CARD_LOCKED.")
    simcard_ErrorListAppend("6284", "ISO 7816: FCI not right formatted according to ISO 7816-4.")
    simcard_ErrorListAppend("62XX", "ISO 7816: Warning processing according to ISO 7816-4. State of non-volatil memory unchanged.")

    simcard_ErrorListAppend("6300", "Smartcard: Cryptogram not verified.")
    simcard_ErrorListAppend("6310", "Smartcard: More data available.")
    simcard_ErrorListAppend("6381", "ISO 7816: File filled up by the last write according to ISO 7816-4.")
    simcard_ErrorListAppend("63CX", "ISO 7816: Verification failed. 0x63 CX where X indicates the number of further allowed retries.")
    simcard_ErrorListAppend("63XX", "ISO 7816: Warning processing according to ISO 7816-4. State of non-volatil memory unchanged.")

    simcard_ErrorListAppend("6400", "Smartcard or Global Platform: No specific diagnosis or for ISO Execution Error, State of Non-Volatil Memory unchanged.")
    simcard_ErrorListAppend("6408", "Smartcard: File is inconsistent with the command.")
    simcard_ErrorListAppend("64XX", "ISO 7816: Execution errors according to ISO 7816-4. State of non-volatil memory unchanged.")

    simcard_ErrorListAppend("6500", "ISO 7816: No information given according to ISO 7816-4.")
    simcard_ErrorListAppend("6510", "Smartcard: Memory failure.")
    simcard_ErrorListAppend("65XX", "ISO 7816: Execution errors according to ISO 7816-4. State of non-volatil memory unchanged.")

    simcard_ErrorListAppend("66XX", "ISO 7816: Reserved for security-related issues according to ISO 7816-4.")

    simcard_ErrorListAppend("6700", "Smartcard: Incorrect length parameter.")
    simcard_ErrorListAppend("6702", "Smartcard: Incorrect length parameter.")

    simcard_ErrorListAppend("6800", "ISO 7816: No information given according to ISO 7816-4.")
    simcard_ErrorListAppend("6804", "Smartcard: Access condition not met/fulfilled.")
    simcard_ErrorListAppend("6881", "Smartcard or Global Platform: Logical channel not supported or is not active.")
    simcard_ErrorListAppend("6882", "Smartcard or Global Platform: Secure messaging not supported.")
    simcard_ErrorListAppend("68XX", "ISO 7816: Functions in CLA not supported according to ISO 7816-4.")

    simcard_ErrorListAppend("6900", "ISO 7816: No information given according to ISO 7816-4.")
    simcard_ErrorListAppend("6981", "ISO 7816: Command inncompatible with file structure according to ISO 7816-4.")
    simcard_ErrorListAppend("6982", "Smartcard: Security status not satisfied. MAC not verified for example.")
    simcard_ErrorListAppend("6983", "Smartcard or Global Platform: Reader key not supported or Authentication/PIN method blocked.")
    simcard_ErrorListAppend("6984", "Smartcard: The presented license is incorrect, but it is not blocked yet (more attempts remain) or Referenced data invalidated.")
    simcard_ErrorListAppend("6985", "Smartcard or Global Platform: Secure transmission not supported or Address out of range or Conditions of use not satisfied.")
    simcard_ErrorListAppend("6986", "ISO 7816: Command not allowed according to ISO 7816-4.")
    simcard_ErrorListAppend("6987", "ISO 7816: Expected SM data objects missing according to ISO 7816-4.")
    simcard_ErrorListAppend("6988", "ISO 7816: SM data objects incorrect according to ISO 7816-4.")
    simcard_ErrorListAppend("6989", "Smartcard or Global Platform: Key length is not correct.")
    simcard_ErrorListAppend("69XX", "ISO 7816: Command not allowed according to ISO 7816-4.")

    simcard_ErrorListAppend("6A00", "ISO 7816: No information given according to ISO 7816-4.")
    simcard_ErrorListAppend("6A80", "Smartcard or Global Platform: Data field error: ASC is not coherent. Other possible error is data incorrect according to the sent command.")
    simcard_ErrorListAppend("6A81", "Smartcard or Global Platform: Function not supported.")
    simcard_ErrorListAppend("6A82", "Smartcard or Global Platform: File not found / Addressed block or byte does not exist.")
    simcard_ErrorListAppend("6A83", "Smartcard: Record not found.")
    simcard_ErrorListAppend("6A84", "Smartcard: Not enough memory space.")
    simcard_ErrorListAppend("6A85", "Smartcard: L inconsistent with TLV structure.")
    simcard_ErrorListAppend(sSimcard_6A86_IncorrectPIP2, "Smartcard or Global Platform: Incorrect P1 P2.")
    simcard_ErrorListAppend("6A87", "Smartcard: L inconsistent with P1-P2.")
    simcard_ErrorListAppend("6A88", "Smartcard or Global Platform: Referenced data not found.")
    simcard_ErrorListAppend("6AXX", "ISO 7816: Wrong parameter(s) P1-P2 according to ISO 7816-4.")

    simcard_ErrorListAppend("6B00", "Smartcard: Incorrect P1 or P2 parameter.")

    simcard_ErrorListAppend("6D00", "Smartcard: Invalid Instruction/Class.")

    simcard_ErrorListAppend("6E00", "Smartcard: CLASS byte es not correct.")

    simcard_ErrorListAppend("6F00", "Smartcard: Memory problem.")

    simcard_ErrorListAppend("9000", "Smartcard: Eveything OK or no response.")
    
    simcard_ErrorListAppend("9202", "Smartcard: Memory failure (after a Write_Block with verification).")
    simcard_ErrorListAppend("9210", "Smartcard: Not enough memory.")
    simcard_ErrorListAppend("9220", "Smartcard: File identifier already exists in the directory.")
    simcard_ErrorListAppend("9240", "Smartcard: Memory problem.")

    simcard_ErrorListAppend("9300", "Smartcard: SIM Application Toolkit Busy.")

    simcard_ErrorListAppend("9400", "Smartcard: No EF selected.")
    simcard_ErrorListAppend("9402", "Smartcard: Out of range.")
    simcard_ErrorListAppend("9404", "Smartcard: File identifier not found.")
    simcard_ErrorListAppend("9405", "Smartcard: Overflow during value block operation.")
    simcard_ErrorListAppend("9408", "Smartcard: File is inconsistent with the command.")
    simcard_ErrorListAppend("940A", "Smartcard: Invalid address value in data field.")
    simcard_ErrorListAppend("940B", "Smartcard: Invalid ASC value.")
    simcard_ErrorListAppend("940C", "Smartcard: Unauthorized transfer detected during combined Add, Substract or Copy command.")
    simcard_ErrorListAppend("9484", "Smartcard or Global Platform: Algorithm not supported.")
    simcard_ErrorListAppend("9485", "Smartcard or Global Platform: Invalid key check value.")

    simcard_ErrorListAppend("9802", "Smartcard: No secret code was initialized.")
    simcard_ErrorListAppend("9804", "Smartcard: Access condition not met/fulfilled.")
    simcard_ErrorListAppend("9808", "Smartcard: Command inconsistent with the secret code status.")
    simcard_ErrorListAppend("9810", "Smartcard: File has been invalidated.")
    simcard_ErrorListAppend("9820", "Smartcard: Authentication failure (key is not correct).")
    simcard_ErrorListAppend("9840", "Smartcard: Secret code is blocked.")
    simcard_ErrorListAppend("9862", "Smartcard: Authentication error, incorrect MAC.")
    simcard_ErrorListAppend("9864", "Smartcard: Authentication error, security context not supported.")
    simcard_ErrorListAppend("9865", "Smartcard: Key freshness failure.")
    simcard_ErrorListAppend("9866", "Smartcard: Authentication error, no memory space available.")
    simcard_ErrorListAppend("9867", "Smartcard: Authentication error, no memory space available in EF MUK.")
    simcard_ErrorListAppend("9EXX", "Smartcard: Command executed successfully with xxh bytes of data available for Get Response in case of Data Download Error.")

    return len(sSimcard_ErrorList)   

# simcard_ErrorListGet ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_ErrorListGetDes(sBytes):

    global sSimcard_ErrorList

    nItems = len(sSimcard_ErrorList)
    
    if nItems <= 0:
       nItems = simcard_ErrorListSet()

    sReturn = ""
    sX = "X"
    
    #print("simcard_ErrorListGetDes - sBytes=" + str(sBytes))
    
    if sBytes!="" and nItems > 0:

       #print("simcard_ErrorListGetDes - sBytes=" + str(sBytes) + " - nItems = " + str(nItems))

       n = 0
       while n < nItems:
             sItem = sSimcard_ErrorList[n]
             sItemBytes = str_getSubStringFromOcur(sItem, sSimcard_ErrorListSepara, 0)
             sItemBytesCheck = sItemBytes
             sItemDes = str_getSubStringFromOcur(sItem, sSimcard_ErrorListSepara, 1)

             #print("simcard_ErrorListGetDes - n=" + str(n) + " - sItemBytes = " + str(sItemBytes) + " - sItemDes=" + sItemDes)
             
             if sX in sItemBytesCheck:
                sItemBytesCheck = str_getSubStringFromOcur(sItemBytesCheck, sX, 0)
             
             if str_left(sBytes, len(sItemBytesCheck)) == sItemBytesCheck:
                #print("simcard_ErrorListGetDes - n=" + str(n) + " - sItemBytes = " + str(sItemBytesCheck) + " - sItemDes=" + sItemDes)
             
                if sX in sItemBytes:
                   nX = str_CountCharInStr(sItemBytes, sX)
                   #print("simcard_ErrorListGetDes - n=" + str(n) + " - nX = " + str(nX))

                   if nX > 0:
                      sItemDes = sItemDes + " " + sX + " represents bytes/items = '" + str_right(sBytes, nX) + "' (decimal=" + bytes_HexaToNro(str_right(sBytes, nX)) + ") processed."
                      
                return sItemDes    
                
             n = n + 1
             
    return ""         

# simcard_ErrorListGetAll ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_ErrorListGetAll():

    global sSimcard_ErrorList

    nItems = len(sSimcard_ErrorList)
    sItems = ""
    
    if nItems <= 0:
      nItems = simcard_ErrorListSet()
        
    if nItems > 0:
       n = 0
       while n < nItems:
             sItem = sSimcard_ErrorList[n]
             sItemBytes = str_getSubStringFromOcur(sItem, sSimcard_ErrorListSepara, 0)
             sItemDes = str_getSubStringFromOcur(sItem, sSimcard_ErrorListSepara, 1)
             sItems = sItems + "\n" + str(n) + ". [" + sItemBytes + "] " + sItemDes                
             n = n + 1
    
    sItems = "Total items in Error List = " + str(nItems) + sItems         
    return sItems

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ERROR LIST MANAGEMENT - END
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
# simcard_BytesWithLenDes ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_3GPP23048_ResponseAnalisys_Others(sBytes):
    sBytes = str_SpacesOut(sBytes)
  
    sResponse = ""
    sReturn = ""
    
    if bytes_IsHexaValid(sBytes):
       sResponse = "0x" + str_SpaceHexa(sBytes) + " = "
       sReturn = simcard_ErrorListGetDes(sBytes)

    if sReturn == "":
       sReturn = "Unknow, check standard"

    return sResponse + sReturn
    
# simcard_BytesWithLenDes ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_BytesWithLenDes(sBytes):
    sBytes = str_SpacesOut(sBytes)
    if sBytes == "":
       return ""
       
    nLen = len(sBytes)//2
    sReturn = str_SpaceHexa(sBytes) + " - Length = " + str(nLen) + " bytes"
    return sReturn
    

# simcard_Clean9000 ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_Clean9000(sValue):
    
    sValue = str_SpacesOut(sValue)
    
    if str_left(sValue, len(sSimcard_9000)) == sSimcard_9000:
       sValue = str_midToEnd(sValue, len(sSimcard_9000))
        
    if str_right(sValue, len(sSimcard_9000)) == sSimcard_9000:
       sValue = str_left(sValue, len(sValue) - len(sSimcard_9000))
        
    return sValue

# simcard_CheckMSLActivatingPoR ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_CheckMSLActivatingPoR(sMSL):
    sPoR = "21"
        
    sMSL = str_SpacesOut(sMSL).upper()
        
    if str_mid(sMSL, 2, 2) != sPoR:
       sMSL = str_left(sMSL, 2) + sPoR + str_right(sMSL, 4)
    
    return sMSL

# simcard_ValidateMSLParams ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_ValidateMSLParams(sTPDA, sTAR, sMSL, sMSL_KIC, sMSL_KID, sMSLCount, sAPDU):
    sTAR = str_SpacesOut(sTAR).upper()
    sTPDA = str_SpacesOut(sTPDA).upper()
    sMSL = str_SpacesOut(sMSL).upper()
    sMSL_KIC = str_SpacesOut(sMSL_KIC).upper()
    sMSL_KID = str_SpacesOut(sMSL_KID).upper()
    sMSLCount = str_SpacesOut(sMSLCount).upper()
    sAPDU = str_SpacesOut(sAPDU).upper()

    bReturn = True
    sError = ""
        
    bReturn, sError = simcard_ValidateParamData(sTAR, "TAR", 3)
    if not bReturn:
       return bReturn, sError
               
    bReturn, sError = simcard_ValidateTPDA(sTPDA)
    if not bReturn:
       return bReturn, sError

    bReturn, sError = simcard_ValidateParamData(sMSL, "MSL", 4)
    if not bReturn:
       return bReturn, sError

    bReturn, sError = simcard_ValidateParamDataMultipleOf8Bytes(sMSL_KIC, "sMSL_KIC")
    if not bReturn:
       return bReturn, sError

    bReturn, sError = simcard_ValidateParamDataMultipleOf8Bytes(sMSL_KID, "sMSL_KID")
    if not bReturn:
       return bReturn, sError

    bReturn, sError = simcard_ValidateParamData(sMSLCount, "Counter", 5)
    if not bReturn:
       return bReturn, sError
    
    if sAPDU!="":    
       bReturn, sError = simcard_ValidateHexa(sAPDU, "APDU")
       if not bReturn:
          return bReturn, sError
        
    return bReturn, ""
        
# simcard_ValidateParamData ---------------------------------------------------------------------------------------------------------------------------------------------------------
# nValueLen must be in bytes, not characters.
# Example for validating MSL where it is 4 bytes => nValueLen = 4
def simcard_ValidateParamData(sValue, sDes="", nValueLen=0):

    if sDes=="":
       sDes = "Data"

    sValue = str_TrimCleanSpaces(sValue).upper()  

    #print("simcard_ValidateParamData - sValue = " + str(sValue))
    bReturn, sError = simcard_ValidateHexa(sValue, sDes)

    #print("simcard_ValidateParamData - bReturn = " + str(bReturn) + " - sError = " + str(sError))
    
    if bReturn:

       #print("simcard_ValidateParamData - sValue = " + str(sValue) + " - sError = " + str(int(nValueLen*2)))
       if nValueLen > 0:
          if len(sValue) != int(nValueLen*2):
             return False, sDes + " must be an hexadecimal value with " + str(nValueLen*2) + " bytes.\n" + simcard_ValidateHexaErrorMsgValue(sValue)
    else:
       return False, sError

    #print("simcard_ValidateParamData - bReturn = " + str(bReturn) + " - sError = " + str(sError))
          
    return True, sValue
    

# simcard_ValidateBytes ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_ValidateHexa(sValue, sDes=""):

    if sDes=="":
       sDes = "Data"

    sValue = str_TrimCleanSpaces(sValue).upper()  
    
    if False == bytes_IsHexaValid(sValue):
       return False, sDes + " must be an hexadecimal value.\n" + simcard_ValidateHexaErrorMsgValue(sValue)
    
    return True, sValue

# simcard_ValidateParamDataMultipleOf8Bytes ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_ValidateParamDataMultipleOf8Bytes(sValue, sDes=""):

    if sDes=="":
       sDes = "Data"

    sValue = str_TrimCleanSpaces(sValue).upper()  

    bReturn, sError = simcard_ValidateHexa(sValue, sDes)
    
    if bReturn:
       if len(sValue) % 16 != 0:
          return False, sDes + " must be an hexadecimal value with bytes length multiple of 8 bytes minimum.\n" + simcard_ValidateHexaErrorMsgValue(sValue)
    else:
       return False, sError
          
    return True, sValue

# simcard_ValidateTPDA ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_ValidateTPDA(sValue, bValidateForSetUpCall=False):

    sName = "TPDA"
    sF = "F"
    sValue = str_TrimCleanSpaces(sValue).upper()  
    
    bReturn, sError = simcard_ValidateHexa(sValue, sName)
    if not bReturn:
       return bReturn, sError
    
    if len(sValue) < 8:
       return False, "The TPDA must be bigger or equal to 4 bytes because the minimum short number length is 3 digits. TPDA " + simcard_ValidateHexaErrorMsgValue(sValue)
       
    if False == bytes_IsCharValidHex(sValue):
       return False, "It	 must be an hexadecimal value." + simcard_ValidateHexaErrorMsgValue(sValue)

    nDigits = bytes_HexaToNro(str_left(sValue, 2))
    sTONNPI = str_mid(sValue,2,2)
    sNroHexa = str_midToEnd(sValue, 4)
    sNro = str_reverse(sNroHexa)
    
    if bValidateForSetUpCall:
       if (1+(len(sNroHexa)//2)) != int(nDigits): 
          sError = "The first byte for TPDA 0x" + str_left(sValue, 2) + " (digits: " + str(nDigits) + ")"
          sError = sError + ", must be the same amunt of bytes with TON NPI + Number"
          sError = sError + ".\nTON NPI: 0x" + sTONNPI + ", Number: 0x" + str_AddSpaceHexa(sNroHexa) + " (scrambled for interpretation: " + sNro + " - Number length in bytes: " + str(len(sNroHexa)//2)
          sError = sError + ".\nNumber of bytes expected: " + str(nDigits) + " - Number of bytes with TON NPI + Data: " + str(len(sNroHexa)//2) + " bytes."
          return False, sError
    else:
       if str_right(sNro, 1) == sF:
          sNro = str_left(sNro, len(sNro) - len(sF))
          
       if len(sNro) != int(nDigits): 
          sError = "The first byte for TPDA 0x" + str_left(sValue, 2) + " (digits: " + str(nDigits) + ")"
          sError = sError + ", must be the same amunt of digits for Number"
          sError = sError + ".\nTON NPI: 0x" + sTONNPI + ", Number: 0x" + str_AddSpaceHexa(sNroHexa) + " (scrambled for interpretation: " + sNro + " - Number of digits: " + str(len(sNro))
          sError = sError + ".\nNumber of digits expected: " + str(nDigits) + " - Number of digits in TPDA without TON NPI: " + str(len(sNro)) + " digits."
          return False, sError
    
    return True, sValue


# simcard_ValidateHexaErrorMsgValue ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_ValidateHexaErrorMsgValue(sValue):
    sValue = str_TrimCleanSpaces(sValue).upper()  
    
    sLenDecimal = str(len(sValue)//2)
    sLenFloat = str(len(sValue)/2)
    sLenFloatEntero = str_getNroPartInt(sLenFloat)
    sLenFloatDecimal = str_getNroPartDecimal(sLenFloat)
    
    print("simcard_ValidateHexaErrorMsgValue - sLenFloatEntero=" + str(sLenFloatEntero))
    print("simcard_ValidateHexaErrorMsgValue - sLenFloatDecimal=" + str(sLenFloatDecimal))
    
    sReturn = "Value = 0x" + str_AddSpaceHexa(sValue) + " - Length = "
    if sLenDecimal == sLenFloatEntero and (sLenFloatDecimal=="" or sLenFloatDecimal=="0"):
       sLen = sLenDecimal
    else:
       sLen = sLenFloatEntero + "." + sLenFloatDecimal
          
    sReturn = sReturn + sLen + " bytes (" + str(len(sValue)) + " characters)"  
     
    return sReturn

# simcard_APDUForDeleteApplet ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_APDUForDeleteApplet(sAID, bPackage=True):
    
    sAID = str_SpacesOut(sAID)
    if sAID == "":
       return ""
       
    #Example for delete package:
    #s00030.write("0x80 E4 00 80 12 4F 10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 00");   
    
    #Example for delete instance only
    #s00038.write("0x80 E4 00 00 12 4F 10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 01");

    #CLA: 0x80 - Global Platform Secure Channel Protocol
    #INS: 0xE4 - APPLET DELETE
    #P1: 0x00 (Bits: 00000000 - First Bit: 0 = Last or only command)
    #P2: 0x80 (Bits: 10000000 - First Bit: 1 = DELETE object and related object)

    sAPDU = "80 E4 00"
    if bPackage:
       sAPDU = sAPDU + "80"
    else:
       sAPDU = sAPDU + "00"
    
    sAIDLen = bytes_NroToHexa(len(sAID)//2)
    sData ="4F" #0x4F: Executable Load File or Application AID
    sData = sData + sAIDLen + sAID
    sDataLen = bytes_NroToHexa(len(sData)//2)
    
    sAPDU = sAPDU + sDataLen + sData
    
    return str_SpacesOut(sAPDU)
        
# simcard_sms_tpud_extraction  -----------------------------------------------------------------------------------------------------------------------------------------------------
# Returns tuples. If process succeeds, returns True followed by the complete_response_list
#                 Else, returns False, followed by a message indicating that the conditions defined in the process weren't met
def simcard_sms_tpud_extraction(log_file, card_service, str_tpda, str_cmd, complete_responses_list, has_campaign_id,
                                responses_wh_CID_joined_str, responses_wh_CID_list, str_tar):
    responses = simcard_SendEnvelopeContinuosResponseList(card_service, log_file, str_tpda, str_cmd,
                                                          "#", sTAR=str_tar)

    # Searching send short message proactive command and saving it
    for i, response in enumerate(responses):
        """ Because the simcard_SendEnvelopeContinuosResponseList() method always returns the first element 
        of the list with the concatenated SW9000, the first 4 characters of element 0 of the list are omitted.
        """
        if i == 0:
            response = response[4:]
        if response[0:2].upper() == sSimcard_BERTV_SIMtoME:
            type_of_cmd = simcard_coded_128_255(response)
            if type_of_cmd == simcard_STKCmdGetCmdSendSMS():
                tp_ud_sms = simcard_SendSMSCmd_Interpret_GetTPUD(response)
                complete_responses_list.append(tp_ud_sms)

                if has_campaign_id:
                    responses_wh_CID_joined_str += tp_ud_sms[4:]
                    responses_wh_CID_list.append(tp_ud_sms[4:])
                else:
                    responses_wh_CID_joined_str += tp_ud_sms
                    responses_wh_CID_list.append(tp_ud_sms)

    if complete_responses_list:
        responses_joined_str = " ".join(complete_responses_list)
        return True, responses_joined_str
    else:
        return False, f"Conditions not met..."


# simcard_APDUsForLoadingAppletPackage_ByBytecodeData ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_APDUsForLoadingAppletPackage_ByBytecodeData(sPackageAID, sPackageData):
    return simcard_APDUsForLoadingAppletPackage(sPackageAID, sPackageData, "")

# simcard_APDUsForLoadingAppletPackage_ByPathFile ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_APDUsForLoadingAppletPackage_ByPathFile(sPackageAID, sIJCCAPFilePathAndName):
    return simcard_APDUsForLoadingAppletPackage(sPackageAID, "", sIJCCAPFilePathAndName)

# simcard_APDUsForLoadingAppletPackage ---------------------------------------------------------------------------------------------------------------------------------------------------------
# It can be sent the data bytecode directly with the variable: sPackageData
# Or it can be sent the path and file name for IJC/CAP file to be prepared APDUs bytecode
def simcard_APDUsForLoadingAppletPackage(sPackageAID, sPackageData="", sIJCCAPFilePathAndName=""):
    
    lstAPDUs = []
    
    sPackageAID = str_SpacesOut(sPackageAID)

    # IT HAS MORE PRIORITY PATH AND FILE NAME    
    if sIJCCAPFilePathAndName!="":
       if os.path.exists(sIJCCAPFilePathAndName):
          sPackageData = fFileOpenBinaryModeAndRead(sIJCCAPFilePathAndName)
       else:
          log_writePrintOnlyError("File for loading package does not exist! File: " + str(sIJCCAPFilePathAndName))
          return ""
    else:        
       sPackageData = str_SpacesOut(sPackageData)
    
    if sPackageAID == "":
       return ""

    nPackageDataLen = (len(sPackageData)//2)
    
    if nPackageDataLen<=0:
       return ""

    # Example for first Install for Load:
    # 0x80 E6 02 00 15 10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 00 00 00 00 00
    # CLA: 0x80 - Global Platform Secure Channel Protocol
    # INS: 0xE6 - APPLET INSTALL
    # P1: 0x02
    # P2: 0x00
    # LENGTH: 0x15 (in decimal: 21)
    # P1: 0x02 (Bits: 00000010 - First Bit: 0 = Last or only command - Next bits interpretaion 'APPLET INSTALL, For load')
    # P2: 0x00 (indicates that no information is provided)
    # Data Block: 0x10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 00 00 00 00 00
    # Object-AID LENGTH: 0x10 (in decimal: 16)
    # Object-AID: 0x43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 00 (TAR: 0x48 45 4C: HEL)
    # Security Domaing AID LENGTH: 0x00 (in decimal: 0)
    # Load File Data Block Hash LENGTH: 0x00 (in decimal: 0)
    # Load Parameters field LENGTH: 0x00 (in decimal: 0)
    # Load Token LENGTH: 0x00 (in decimal: 0)

    # PREPARE APDU FOR INSTALL FOR LOAD
    sAPDU = "80 E6 02 00"
    nAIDLen = len(sPackageAID)//2
    # APDU Len is => AID Len + AID + 4 bytes with 0x00
    sAPDULen = bytes_NroToHexa(1+ nAIDLen + 4)
    sAIDLen = bytes_NroToHexa(nAIDLen)
    sAPDU = sAPDU + sAPDULen + sAIDLen + sPackageAID + str_RepeatString(8, "0")
    lstAPDUs.append(str_SpacesOut(sAPDU))
    
    # PREPARE BLOCKS
    # Example for 1st BLOCK
    # Processed: 80 E8 00 00 64 C4 82 01 BB 01 00 1A DE CA FF ED 01 02 04 00 01 10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 00 02 00 1F 00 1A 00 1F 00 14 00 31 00 36 00 20 00 97 00 20 00 15 00 00 00 CB 00 06 00 02 00 10 03 01 00 04 00 31 03 00 01 07 A0 00 00 00 62 01 01 00 01 10 A0 00 00 00 09 00 05 FF FF FF FF 89 12 00 00 00
    # CLA=0x80 - USIM, INS=0xE8 - APPLET LOAD. P1=0x00 (offset high), P2=0x00 (offset low) - Bytecode: 0xC4 82 01 BB 01 00 1A DE CA FF ED 01 02 04 00 01 10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 00 02 00 1F 00 1A 00 1F 00 14 00 31 00 36 00 20 00 97 00 20 00 15 00 00 00 CB 00 06 00 02 00 10 03 01 00 04 00 31 03 00 01 07 A0 00 00 00 62 01 01 00 01 10 A0 00 00 00 09 00 05 FF FF FF FF 89 12 00 00 00
    
    # Assuming block with 120 bytes
    nPackageBlocks = int(sSimcard_PackageBlocks)
    
    # It is minus 4 for the first block with C4 82 [Package Length - 2 bytes]
    lstBlocks = str_getListFromStringInHexa(sPackageData, nPackageBlocks-4)
    #print("simcard_APDUsForLoadingAppletPackage - lstBlocks=" + str(lstBlocks) + " - Blocks=" + str(len(lstBlocks)))
    
    nBlocks = len(lstBlocks)
    n = 0
    while n < nBlocks:
    
          sAPDU = "80 E8"
          
          if n == 0:
             #It is the first block
             sAPDU = sAPDU + "00"      
          else:   
             if n == (nBlocks-1)   :
                #It is the last block
                sAPDU = sAPDU + "80"      
             else:
                sAPDU = sAPDU + "00"      
                
          
          #Added Block Number   
          sAPDU = sAPDU + bytes_NroToHexa(n)
          
          sAPDUData = ""
          if n == 0:
             #C4 82 + Total bytes to load
             # C4 = Attribute information tag
             # 82 = length from 256 to 65535 bytes
             sAPDUData = "C4 82"
             sPackageLenInHexa = bytes_LengthInHexaWithZerosToTheLeft(nPackageDataLen,2) 
             #print("simcard_APDUsForLoadingAppletPackage - sPackageLenInHexa" + str(sPackageLenInHexa))
             sAPDUData = sAPDUData + sPackageLenInHexa
          
          sAPDUData = str_SpacesOut(sAPDUData + lstBlocks[n])
          
          sAPDU = sAPDU + bytes_NroToHexa(len(sAPDUData)//2) + sAPDUData
          
          #print("simcard_APDUsForLoadingAppletPackage - sAPDU for " + str(n) + " = " + sAPDU)
                       
          lstAPDUs.append(str_SpacesOut(sAPDU))
          
          n = n + 1
    
    
    return lstAPDUs

# simcard_AppletPackageGetAID_ByPathFilewithDes ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_AppletPackageGetAID_ByPathFilewithDes(sIJCCAPFilePathAndName):
    sAID, sDes = simcard_AppletPackageGetAID_ByPathFileProc(sIJCCAPFilePathAndName, True)
    return sAID, sDes
    
# simcard_AppletPackageGetAID_ByPathFile ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_AppletPackageGetAID_ByPathFile(sIJCCAPFilePathAndName):
    sAID, sDes = simcard_AppletPackageGetAID_ByPathFileProc(sIJCCAPFilePathAndName, True)
    return sAID

# simcard_AppletPackageGetAID_ByPathFileProc ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_AppletPackageGetAID_ByPathFileProc(sIJCCAPFilePathAndName, sDesOptional=False):

    sAID = ""
    sPackageData = ""
    if os.path.exists(sIJCCAPFilePathAndName):
       sPackageData = fFileOpenBinaryModeAndRead(sIJCCAPFilePathAndName)
       
    sMsg = ""   
    if sPackageData != "":
       
       sTemp = sPackageData
       
       #print("simcard_AppletPackageGetAID_ByPathFile - sTemp: " + str(sTemp))
       
       #Example: 01 00 1A DE CA FF ED 01 02 04 00 01 10 A0 00 00 01 51 41 43 4C 05 06 25 07 43 50 41 00
       # Move 12 bytes
       n = int(12 * 2)
       sTemp = str_midToEnd(sTemp, n)
       sLenAID = str_left(sTemp, 2)
       n = 2
       nLenAID = int(bytes_HexaToNro(sLenAID))
       sAID = str_mid(sTemp, n, nLenAID * 2)

       #print("simcard_AppletPackageGetAID_ByPathFile - sTemp: " + str(sTemp) + " - sAID: " + sAID + " - n = " + str(n))
       
       if sDesOptional:
          sMsg = "Package AID retrieved from file '" + sIJCCAPFilePathAndName + "'."
          sMsg = sMsg + "\nPackage AID: " + str_SpaceHexa(sAID)
          sMsg = sMsg + "\nPackage size: " + str(str_AddThousandToNumber(str(len(sPackageData)//2)))
          sMsg = sMsg + " bytes - hexadecimal characters: " + str(str_AddThousandToNumber(str(len(sPackageData))))
        
    return sAID, sMsg   

# simcard_StatusCommandsGetLastCommandProcess -----------------------------------------------------------------------------------------------------------
def simcard_StatusCommandsGetLastCommandProcess(cardservice, sLogFileName, sSTATUSCOMMAND_MAX="100", sSeparaAPDU=sSimcard_ErrorListSepara):

    if sSTATUSCOMMAND_MAX == "":
       sSTATUSCOMMAND_MAX = 100
    
    if sSeparaAPDU == "":
       sSeparaAPDU = sSimcard_ErrorListSepara
          
    sLog = "*** STATUS COMMANDS to be sent: " + sSTATUSCOMMAND_MAX + " ***"
    log_write(sLogFileName, sLog)
       
    nMAX = str_StringToNumberFloat(sSTATUSCOMMAND_MAX)
    i = 0
    bReturn = True
    sLastAPDUs = ""
    sLastAPDUsTotal = ""
    
    while i <= nMAX and bReturn:

       sLog = str_RepeatString(20, "#")
       sLog = sLog + "\nITERACTION: " + str(i) + " from " + str(nMAX) + ".\n"
       log_write(sLogFileName, sLog)
       sLog = str_RepeatString(20, "#")
       log_write(sLogFileName, sLog)
                 
       #SEND STATUS COMMAND
       tReturn = simcard_StatusCommandALLResponsesWithLastAPDUs_List(cardservice, sLogFileName, True, sSeparaAPDU)
       
       sResult = tReturn[0]
       if sResult == "":
          bReturn = False
          
       sLastAPDUs = tReturn[1]
       #print("tReturn[1]: " + str(tReturn[1]))
       sLastAPDUs = str_TrimCleanSpaces(sLastAPDUs)
       
       sLog = str_RepeatString(10, "*")
       sLog = sLog + "ITERACTION: " + str(i) + " from " + str(nMAX) + ". "
       sLog = sLog + " - ENDED"

       sLog = sLog + " " + str_RepeatString(10, "*")
       log_write(sLogFileName, sLog)

       sLog = str_RepeatString(100, "-")
       log_write(sLogFileName, sLog + "\n")
       
       sLastAPDUs = str_RemoveFirstPattern(sLastAPDUs, sSeparaAPDU)
       sLastAPDUsTotal = sLastAPDUsTotal + sSeparaAPDU + sLastAPDUs
       
       i = i + 1

    sLastAPDUsTotal = str_RemoveFirstPattern(sLastAPDUsTotal, sSeparaAPDU)
    #print("sLastAPDUsTotal: " + sLastAPDUsTotal)
    
    return bReturn, sLastAPDUsTotal

# simcard_AppletLoadPackage ---------------------------------------------------------------------------------------------------------------------------------------------------------
# It returns: bReturn, lstLastAPDUs, lstLastPoR, sCouter
# Where:
#       bReturn => True (Everything OK) or False (there is an error)
#       lstLastAPDUs => List of APDUs + response
#       lstLastPoR => List of PoR (Proof of Recepit) for each last APDU + response
#       sCounter => Last counter, incremented depending on MSL.
def simcard_AppletLoadPackage(CardService, sLogFileName, sFilePathAndName, sPackageAID, sTPDA=sSimcard_MSLDefTPDA, sTAR=sSimcard_MSLDefTAR_RAM, sMSL=sSimcard_MSLDefMAC, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter, bDelay=False, sSeparaResult=sSimcard_ErrorListSepara):

    lstLastAPDUs = []
    lstLastPoR = []
    bReturn = True
    
    sFilePathAndName = file_fNormalPathForWindowsLinux(sFilePathAndName)
    if len(sFilePathAndName) <= 0:
       return False, "No file path and name defined for loading package with AID: " + sPackageAID

    sPackageAID = str_SpacesOut(sPackageAID)
    if len(sPackageAID) <= 0:
       return False, lstLastAPDUs, lstLastPoR, sCounter, "No AID defined for loading package. AID: " + sPackageAID

    sAIDPackageFromFile = simcard_AppletPackageGetAID_ByPathFile(sFilePathAndName)
    if sAIDPackageFromFile != sPackageAID:
       sMsg = "AID Package from file '" + sFilePathAndName + "'"
       sMsg = sMsg + " is different compared to the one as parameter."
       sMsg = sMsg + "\nAID from package file: " + sAIDPackageFromFile 
       sMsg = sMsg + "\nAID package as parameter: " + sPackageAID
       return False, lstLastAPDUs, lstLastPoR, sCounter, sMsg
    
    # PREPARE APDUs WITH PACKAGE FILE
    lstAPDUs = simcard_APDUsForLoadingAppletPackage_ByPathFile(sPackageAID, sFilePathAndName)
    #print("simcard_AppletLoadPackage - APDUs List=" + str(lstAPDUs) + " - Total APDUs=" + str(len(lstAPDUs)))

    if len(lstAPDUs) > 0:

       # PRINT WHAT IT IS BEING DOING
       simcard_Applets_Debug("Load", sPackageAID, True, sTAR, sMSL, sKIC, sKID, sCounter)    
       
       #GET FREE SPACE BEFORE
       bReturn, lstLastAPDUs, lstLastPoR, sCounter, sAppInstalledBefore, sFreeNonVolatileMemoryBefore, sFreeVolatileMemoryBefore = simcard_GlobalPlatformGetData_FreeMemory(CardService, sLogFileName, sTPDA, sSimcard_MSLDefTAR_RAM, sMSL, sKIC, sKID, sCounter)

       # SEND LOAD PACKAGE APDUs
       bReturn, lstLastAPDUs, lstLastPoR, sCounter = simcard_AppletSendAPDUsList(CardService, sLogFileName, lstAPDUs, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, bDelay, sSeparaResult)
       
       sDes = ""
       
       if bReturn:
          #GET FREE SPACE AFTER
          bReturn, lstLastAPDUsT, lstLastPoRT, sCounter, sAppInstalledAfter, sFreeNonVolatileMemoryAfter, sFreeVolatileMemoryAfter = simcard_GlobalPlatformGetData_FreeMemory(CardService, sLogFileName, sTPDA, sSimcard_MSLDefTAR_RAM, sMSL, sKIC, sKID, sCounter)
       
          sProcess = "Load Package"
          sDes = simcard_GlobalPlatformGetData_FreeMemory_ProcessBeforeAndAfter(sProcess, sAppInstalledBefore, sFreeNonVolatileMemoryBefore, sFreeVolatileMemoryBefore, sAppInstalledAfter, sFreeNonVolatileMemoryAfter, sFreeVolatileMemoryAfter)

       if len(lstLastAPDUs) > 0:
          if sDes != "":
             lstLastAPDUs[len(lstLastAPDUs)-1] = lstLastAPDUs[len(lstLastAPDUs)-1] + sSeparaResult + sDes 
       
    else:
       bReturn = False   

    return bReturn, lstLastAPDUs, lstLastPoR, sCounter, ""

# simcard_AppletPoRCheckOK ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_AppletPoRCheckOK(sData):
    
    bReturn = False
    sData = str_SpacesOut(sData).upper()

    #print("simcard_AppletPoRCheckOK - sData = " + str(sData))

    sPoR, sPoRDes = simcard_APDUResponseGettingPoR(sData)
    
    #print("simcard_AppletPoRCheckOK - sPoR = " + str(sPoR))

    bReturn = simcard_AppletPoRCheckOK_List(sPoR)

    return bReturn

# simcard_AppletPoRCheckOK_List ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_AppletPoRCheckOK_List(sPoR):
     
    bOk = False
    if sPoR == sSimcard_9000:
       bOk = True
    if sPoR == sSimcard_6101_AppletOK:
       bOk = True
    if sPoR == sSimcard_0000:
       bOk = True
    if sPoR == sSimcard_6310_MoreData:
       bOk = True

    return bOk
    
# simcard_MSL_IncrementCounter ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_MSL_IncrementCounter(sMSL, sCounter):
    
    sCounter = str_SpacesOut(sCounter).upper()
    sReturn = sCounter
    
    #print("simcard_MSL_IncrementCounter - sMSL: " + str(sMSL) + " - Counter: " + str(sCounter))
    
    if simcard_fPrepare_23_048_Msg_IsMSLSPI1WithCounterBigger(sMSL):
       
       #Counter should be incremented after sending SMPP
       nCounter = bytes_HexaToNro(sCounter)
       #print("MSLCheckCounter - nCounter = " + str(nCounter))
       sCounter = bytes_NroToHexa(float(nCounter) + 1)
       sCounter = bytes_LengthInHexaWithZerosToTheLeft_FromHexaLen(sCounter, 5)
       #print("MSLCheckCounter - sCounter = " + str(sCounter))
  
    #print("simcard_MSL_IncrementCounter - Counter: " + str(sCounter))
    
    return sCounter         
     
# simcard_AppletLoadPackage_StatusCommand ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_AppletLoadPackage_StatusCommand(cardservice, sLogFileName, sMsg, nStatusCommands=1):

    sResult, sLastAPDUs = simcard_StatusCommandsGetLastCommandProcess(cardservice, sLogFileName, nStatusCommands)
    if sResult == "":
       return False, sLastAPDUs
        
    sLastAPDUs = str_TrimCleanSpaces(sLastAPDUs)
    sStatusCommand = sSimcard_StatusCommand
    sLastAPDUs = str_SpacesOut(sStatusCommand) + sSimcard_ErrorListSepara + sLastAPDUs
    
    if sMsg == "":
       sMsg = "Sent Status Command before sending spacific APDU"
       
    sLastAPDUs = sMsg + sSimcard_ErrorListSepara + sLastAPDUs 
    
    return True, sLastAPDUs

# simcard_AppletDeletePackageOrInstance ---------------------------------------------------------------------------------------------------------------------------------------------------------
# It returns: bReturn, sLastAPDUs, sCouter
# Where:
#       bReturn => True (Everything OK) or False (there is an error)
#       sLastAPDUs => List of APDUs + response
#       sCounter => Last counter, incremented depending on MSL.
def simcard_AppletDeletePackageOrInstance(CardService, sLogFileName, sAID, bPackage=True, sTPDA=sSimcard_MSLDefTPDA, sTAR=sSimcard_MSLDefTAR_RAM, sMSL=sSimcard_MSLDefMAC, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter, sSeparaResult=sSimcard_ErrorListSepara):

    lstAPDUs = []
    sLastAPDUs = ""
    sLastPoR = ""
    bReturn = True
    
    sAID = str_SpacesOut(sAID)
    if len(sAID) <= 0:
       return False, "No AID defined for deletinge. AID: " + sAID
    
    #GET FREE SPACE BEFORE
    bReturn, lstLastAPDUs, lstLastPoR, sCounter, sAppInstalledBefore, sFreeNonVolatileMemoryBefore, sFreeVolatileMemoryBefore = simcard_GlobalPlatformGetData_FreeMemory(CardService, sLogFileName, sTPDA, sSimcard_MSLDefTAR_RAM, sMSL, sKIC, sKID, sCounter)
     
    # PREPARE APDU FOR DELETE       
    sAPDU = simcard_APDUForDeleteApplet(sAID, bPackage)
    lstAPDUs.append(sAPDU)
    #print("simcard_AppletDeletePackageOrInstance - APDU=" + str(sAPDU))

    # PRINT WHAT IT IS BEING DOING
    simcard_Applets_Debug("Delete", sAID, bPackage, sTAR, sMSL, sKIC, sKID, sCounter)
    
    # SEND DELETE APDU 
    bReturn, lstLastAPDUs, lstLastPoR, sCounter = simcard_AppletSendAPDUsList(CardService, sLogFileName, lstAPDUs, sTPDA, sSimcard_MSLDefTAR_RAM, sMSL, sKIC, sKID, sCounter, False, sSeparaResult)

    sDes = ""
    if bReturn:
       #GET FREE SPACE AFTER 
       bReturn, lstLastAPDUsT, lstLastPoRT, sCounter, sAppInstalledAfter, sFreeNonVolatileMemoryAfter, sFreeVolatileMemoryAfter = simcard_GlobalPlatformGetData_FreeMemory(CardService, sLogFileName, sTPDA, sSimcard_MSLDefTAR_RAM, sMSL, sKIC, sKID, sCounter)
    
       sProcess = "Delete "
       if bPackage:
          sProcess = sProcess + " Package"
       sDes = simcard_GlobalPlatformGetData_FreeMemory_ProcessBeforeAndAfter(sProcess, sAppInstalledBefore, sFreeNonVolatileMemoryBefore, sFreeVolatileMemoryBefore, sAppInstalledAfter, sFreeNonVolatileMemoryAfter, sFreeVolatileMemoryAfter)
       
    sLastAPDU = ""
    if len(lstLastAPDUs) > 0:
       sLastAPDU = lstLastAPDUs[0]
       if sDes != "":
          sLastAPDU = sLastAPDU + sSeparaResult + sDes 

    if len(lstLastPoR) > 0:
       sLastPoR = lstLastPoR[0]

    return bReturn, sLastAPDU, sLastPoR, sCounter

# simcard_3GPP23048_AppletTARExists ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_3GPP23048_AppletTARExists(cardservice, sLogFileName, sAPDU="FF", sTPDA=sSimcard_MSLDefTPDA, sTAR=sSimcard_MSLDefTAR_RAM, sMSL=sSimcard_MSLDefMAC, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter, sSeparaResult=sSimcard_ErrorListSepara):

    lstAPDUs = []
    sLastAPDUs = ""
    sLastPoR = ""
    bReturn = True
    
    lstAPDUs.append(sAPDU)
    bReturn, lstLastAPDUs, lstLastPoR, sCounter = simcard_AppletSendAPDUsList(cardservice, sLogFileName, lstAPDUs, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, False, sSeparaResult)
    
    sLastAPDU = ""
    if len(lstLastAPDUs) > 0:
       sLastAPDU = lstLastAPDUs[0]

    #print("simcard_3GPP23048_AppletTARExists - sLastAPDU = " + str(sLastAPDU) + " - lstLastPoR = " + str(lstLastPoR))
    
    #GETTING PoR SMS            
    #SMS Data: 0x02 71 00 00 0B 0A 43 50 41 00 00 00 00 01 00 09 - ASCII: _q____CPA_______ - 3GPP 23.048 response for TAR = 43 50 41 : 0x00 09 = Smartcard: 23.048 TAR Unknown.
    if len(lstLastPoR) > 0:
       if lstLastPoR[len(lstLastPoR)-1] != "":
          sLastPoR = lstLastPoR[len(lstLastPoR)-1]
          sLastPoRDes = simcard_3GPP23048_ResponseAnalisys_Others(sLastPoR)
    else:      
        sLastPoR, sLastPoRDes = simcard_APDUResponseGettingPoR(sLastAPDU)
    
    #print("simcard_3GPP23048_AppletTARExists - sLastPoR = " + str(sLastPoR) + " - sLastPoRDes = " + str(sLastPoRDes))

    if sLastPoR != "":
       bReturn, sRespTAR, sRespByte = simcard_3GPP23048_ResponseAnalisysTARExists(sLastPoR, sTAR)
        
    return bReturn, sLastAPDU, sLastPoR, sCounter

# simcard_3GPP23048_AppletTARExists_Msg ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_3GPP23048_AppletTARExists_Msg(bTARExists, sTAR, sPoR):

    sMsg = "Applet does"
    if bTARExists == False:
       sMsg = sMsg + " NOT"
    sMsg = sMsg + " exist !!! TAR: 0x" + str_AddSpaceHexa(sTAR) + " (ASCII: " + bytes_HexaToASCII(sTAR) + ")"
    if sPoR != "":
      sMsg= sMsg + " - PoR (Proof of Receipt): "
      sMsgAnalisys = simcard_3GPP23048_ResponseAnalisys(sPoR)
      if sMsgAnalisys != "":
         sMsg = sMsg + sMsgAnalisys 
         	  
    return sMsg

    
# simcard_3GPP23048_ResponseAnalisysTARExists ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_3GPP23048_ResponseAnalisysTARExists(sResponse, sTAR=""):

    sTAR = str_SpacesOut(sTAR)
    sByte = ""
    sTARResp = ""
    
    #print("simcard_3GPP23048_ResponseAnalisysTARExists - sResponse = " + str(sResponse))
    #print("simcard_3GPP23048_ResponseAnalisysTARExists - sTAR = " + str(sTAR))
    
    sResp = ""
    if len(sResponse) > 0 and len(sResponse) <= 4:
       #IT IS DIRECTLY THE LAST BYTE OF RESPONSE
       sByte = str_right(sResponse, 4)
    else:
       # There is a text message with pattern: sSimcard_ResponseForTAR  
       # Example for sResponse: *** 0. SMS Data: 0x02 71 00 00 0B 0A 00 00 00 00 00 00 00 01 00 0A - ASCII: _q______________ - 3GPP 23.048 response for TAR = 00 00 00 : 0x0A = Insufficient security level.
       if sSimcard_ResponseForTAR in sResponse:
          sResp = str_getSubStringFromOcur(sResponse, sSimcard_ResponseForTAR, 1)
          sResp = str_SpacesOut(sResp)
          #=000000:0x0A=Insufficientsecuritylevel.TPDA:0x05810601F4(interpreted:60104)
          sTARResp = str_mid(sResp,1,6)
          sByte = str_mid(sResp,1+len(sTARResp)+3,2)

          sResp = str_getSubStringFromOcur(sResponse, sSimcard_ResponseForTAR, 0)
          sResp = str_SpacesOut(sResp)
          if "-ASCII:" in sResp:
             sByte = str_getSubStringFromOcur(sResp, "-ASCII:", 0)
             sByte = str_right(sByte, 4)
    
    #print("simcard_3GPP23048_ResponseAnalisysTARExists - sResp=" + str(sResp) + " - sTARResp = " + str(sTARResp) +  " - sByte = " + str(sByte))
          
    if sTAR != "" and sTARResp != "":
       if sTAR != sTARResp:
          #IT SHOULD BE ANALIZED THE SAME TAR
          return False, sTARResp, sByte
    
    #print("simcard_3GPP23048_ResponseAnalisysTARExists - sByte = " + sByte)
    if sByte != "":
       #TAR Unknown = 09
       if str_right(sByte,2) != "09":
          return True, sTARResp, sByte
          
    return False, sTARResp, sByte  

# simcard_AppletInstallForInstall ---------------------------------------------------------------------------------------------------------------------------------------------------------
# It returns: bReturn, sLastAPDUs, sCouter
# Where:
#       bReturn => True (Everything OK) or False (there is an error)
#       sLastAPDUs => List of APDUs + response
#       sCounter => Last counter, incremented depending on MSL.
def simcard_AppletInstallForInstall(CardService, sLogFileName, sPackageAID, sAppletAID, sInstanceAID, sInstance_Params="", sInstance_Params_UICC="", sInstance_Params_APP="", sTPDA=sSimcard_MSLDefTPDA, sTAR=sSimcard_MSLDefTAR_RAM, sMSL=sSimcard_MSLDefMAC, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter, sSeparaResult=sSimcard_ErrorListSepara):

    lstAPDUs = []
    sLastAPDUs = ""
    sLastPoR = ""
    bReturn = True
    
    sPackageAID = str_SpacesOut(sPackageAID)
    if len(sPackageAID) <= 0:
       return False, "No Package AID defined for deletinge. Package AID: " + sPackageAID

    sInstanceAID = str_SpacesOut(sInstanceAID)
    if len(sInstanceAID) <= 0:
       return False, "No Instance AID defined for deletinge. Instance AID: " + sInstanceAID
           
    # PREPARE APDUs FOR INSTALL FOR INSTALL       
    sAPDU = simcard_APDUForInstallForInstallApplet(sPackageAID, sAppletAID, sInstanceAID, sInstance_Params, sInstance_Params_UICC, sInstance_Params_APP)
    lstAPDUs.append(sAPDU)
    #print("simcard_AppletInstallForInstall - APDU=" + str(sAPDU))

    #print("simcard_AppletInstallForInstall - TPDA=" + str(sTPDA))
    #print("simcard_AppletInstallForInstall - TAR=" + str(sTAR))
    #print("simcard_AppletInstallForInstall - MSL=" + str(sMSL))
    #print("simcard_AppletInstallForInstall - KIC=" + str(sKIC))
    #print("simcard_AppletInstallForInstall - KID=" + str(sKID))
    #print("simcard_AppletInstallForInstall - Counter=" + str(sCounter))

    #GET FREE SPACE BEFORE
    bReturn, lstLastAPDUs, lstLastPoR, sCounter, sAppInstalledBefore, sFreeNonVolatileMemoryBefore, sFreeVolatileMemoryBefore = simcard_GlobalPlatformGetData_FreeMemory(CardService, sLogFileName, sTPDA, sSimcard_MSLDefTAR_RAM, sMSL, sKIC, sKID, sCounter)

    # PRINT WHAT IT IS BEING DOING
    simcard_Applets_Debug("Install", sInstanceAID, False, sTAR, sMSL, sKIC, sKID, sCounter)
    
    # SEND APDU INSTALL FOR INSTALL
    bReturn, lstLastAPDUs, lstLastPoR, sCounter = simcard_AppletSendAPDUsList(CardService, sLogFileName, lstAPDUs, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, False, sSeparaResult)

    sDes = ""
    if bReturn:
       #GET FREE SPACE AFTER
       bReturn, lstLastAPDUsT, lstLastPoRT, sCounter, sAppInstalledAfter, sFreeNonVolatileMemoryAfter, sFreeVolatileMemoryAfter = simcard_GlobalPlatformGetData_FreeMemory(CardService, sLogFileName, sTPDA, sSimcard_MSLDefTAR_RAM, sMSL, sKIC, sKID, sCounter)
    
       sProcess = "Install for Install"
       sDes = simcard_GlobalPlatformGetData_FreeMemory_ProcessBeforeAndAfter(sProcess, sAppInstalledBefore, sFreeNonVolatileMemoryBefore, sFreeVolatileMemoryBefore, sAppInstalledAfter, sFreeNonVolatileMemoryAfter, sFreeVolatileMemoryAfter)
    
    sLastAPDU = ""
    if len(lstLastAPDUs) > 0:
       sLastAPDU = lstLastAPDUs[0]
       if sDes != "":
          sLastAPDU = sLastAPDU + sSeparaResult + sDes 

    if len(lstLastPoR) > 0:
       sLastPoR = lstLastPoR[0]
    
    return bReturn, sLastAPDU, sLastPoR, sCounter


# simcard_APDUForInstallForInstallApplet ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_APDUForInstallForInstallApplet(sPackageAID, sAppletAID, sInstanceAID, sInstance_Params="", sInstance_Params_UICC="", sInstance_Params_APP=""):

    sPackageAID = str_SpacesOut(sPackageAID)
    if len(sPackageAID) <= 0:
       return False, "No AID defined for installing applet. Package AID: " + sPackageAID

    sInstanceAID = str_SpacesOut(sInstanceAID)
    if len(sInstanceAID) <= 0:
       return False, "No AID defined for installing applet. Instance AID: " + sInstanceAID
    
    sAppletAID = str_SpacesOut(sAppletAID)
    if sAppletAID == "":
       sAppletAID = sInstanceAID
           
    #' Install [for Install and Make Selectable]
    #-ENT 80 C2 00 00 A1 D1 81 9E 02 02 83 81 06 07 91 43 06 07 19 01 F0 0B 81 8E 44 09 81 06 07 19 01 F0 7F F6 00 00 00 00 00 00 00 7C 02 70 00 00 77 15 02 21 15 15 00 00 00 00 00 00 00 00 00 84 38 59 9C B7 4E 20 7E 80 E6 0C 00 5C 10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 00 10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 01 10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 01 03 00 00 00 23 EF 08 C7 02 00 00 C8 02 00 00 EA 15 80 0A FF 00 10 01 00 00 00 00 00 00 81 07 00 04 02 01 00 04 00 C9 00 00 
    #91 37
    
    #CLA: 0x80 - Global Platform Secure Channel Protocol
    #INS: 0xE6 - APPLET INSTALL
    #P1: 0x0C
    #P2: 0x00
    #LENGTH: 0x5C (in decimal: 92)
    #P1: 0x0C (Bits: 00001100 - First Bit: 0 = Last or only command - Next bits interpretaion 'For make selectable, For install')
    #P2: 0x00 (indicates that no information is provided)
    #Data Block: 0x10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 00 10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 01 10 43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 01 03 00 00 00 23 EF 08 C7 02 00 00 C8 02 00 00 EA 15 80 0A FF 00 10 01 00 00 00 00 00 00 81 07 00 04 02 01 00 04 00 C9 00 00
    #Package AID LENGTH: 0x10 (in decimal: 16)
    #Package AID: 0x43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 00 (TAR: 0x48 45 4C: HEL)
    #Applet AID LENGTH: 0x10 (in decimal: 16)
    #Applet AID: 0x43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 01 (TAR: 0x48 45 4C: HEL)
    #Applet Instance AID LENGTH: 0x10 (in decimal: 16)
    #Applet Instance AID: 0x43 44 52 41 54 02 01 01 01 20 03 00 48 45 4C 01 (TAR: 0x48 45 4C: HEL)
    #Priviledges LENGTH: 0x03 (in decimal: 3)
    #Priviledges: 0x00 00 00
    #Install Parameters LENGTH: 0x23 (in decimal: 35)
    #Install Parameters: 0xEF 08 C7 02 00 00 C8 02 00 00 EA 15 80 0A FF 00 10 01 00 00 00 00 00 00 81 07 00 04 02 01 00 04 00 C9 00
    #EF - System Specific Parameters LENGTH: 0x08 (in decimal: 8)
    #EF - System Specific Parameters: 0xC7 02 00 00 C8 02 00 00
    #C7 - Volatile Memory Quota LENGTH: 0x02 (in decimal: 2)
    #C7 - Volatile Memory Quota: 0x00 00
    #C8 - Non volatile Memory Quota LENGTH: 0x02 (in decimal: 2)
    #C8 - Non volatile Memory Quota: 0x00 00
    #EA - Global Platform Tag LENGTH: 0x15 (in decimal: 21)
    #EA - Global Platform Tag: 0x80 0A FF 00 10 01 00 00 00 00 00 00 81 07 00 04 02 01 00 04 00
    #C9 - Application Specific Parameters LENGTH: 0x00 (in decimal: 0)
    #Install Token LENGTH: 0x00 (in decimal: 0)

    # PREPARE APDU FOR INSTALL FOR INSTALL
    sAPDUHeader = "80 E6 0C 00"
    
    sAPDU = ""
    # PACKAGE
    nAIDLen = len(sPackageAID)//2
    sAPDU = sAPDU + bytes_NroToHexa(nAIDLen) + sPackageAID
    # APPLET
    nAIDLen = len(sAppletAID)//2
    sAPDU = sAPDU + bytes_NroToHexa(nAIDLen) + sAppletAID
    # INSTANCE
    nAIDLen = len(sInstanceAID)//2
    sAPDU = sAPDU + bytes_NroToHexa(nAIDLen) + sInstanceAID
    
    # PRIVILEGE = 0x00
    # BECAUSE SOME SIM SUPPLIERS IT IS SUGGESTED 0x00 and NOT 0x00 00 00
    sAPDU = sAPDU + "01" + "00"
    
    sAPDUSystem = ""
    # System Specific Parameters
    # Volatil Memory
    sAPDUSystem = sAPDUSystem + "C7 02 00 00"
    # Non Volatil Memory
    sAPDUSystem = sAPDUSystem + "C8 02 00 00"
    sAPDUSystem = str_SpacesOut(sAPDUSystem)
    sAPDUSystem = "EF" + bytes_NroToHexa(len(sAPDUSystem)//2) + sAPDUSystem
    
    # Another example for SAP:
    # 80 E6 0C 00 
    # 5F 
    # 10 A0 00 00 01 51 41 43 4C 05 06 25 03 43 50 41 00 
    # 09 A0 00 00 01 51 41 43 4C 00 
    # 09 A0 00 00 01 51 41 43 4C 00 
    # 01 00 
    # 36 EA 16 80 0B FF 01 00 00 00 00 03 43 50 41 00 81 07 00 04 02 01 00 04 00 C9 1C 05 81 06 01 F4 00 20 00 37 32 32 33 31 30 31 31 01 00 00 00 00 00 00 00 02 00 00 00 00

    #print("simcard_APDUForInstallForInstallApplet - sInstance_Params=" + str(sInstance_Params))
    #print("simcard_APDUForInstallForInstallApplet - sInstance_Params_UICC=" + str(sInstance_Params_UICC))
    #print("simcard_APDUForInstallForInstallApplet - sInstance_Params_APP=" + str(sInstance_Params_APP))
    
    sAPDUParams = "EA"
    if sInstance_Params == "":
       sInstance_Params = simcard_APDUForInstallForInstallApplet_PrepareParams_TagEA(sInstance_Params_UICC, sInstance_Params_APP)

    sInstance_Params = str_SpacesOut(sInstance_Params)
    if str_left(sInstance_Params, len(sAPDUParams)) != sAPDUParams:
       sInstance_Params = sAPDUParams + bytes_NroToHexa(len(str_SpacesOut(sInstance_Params))//2) + sInstance_Params

    sAPDUSystem = sAPDUSystem + sInstance_Params
    sAPDUSystem = str_SpacesOut(sAPDUSystem)
    sAPDUSystem =  bytes_NroToHexa(len(sAPDUSystem)//2) + sAPDUSystem      
    
    #print("simcard_APDUForInstallForInstallApplet - sAPDUSystem = " + str(sAPDUSystem))
    
    sAPDU = sAPDU + sAPDUSystem
    
    # Install Token LENGTH: 0x00 (in decimal: 0)
    sAPDU = sAPDU + "00"

    sAPDU = str_SpacesOut(sAPDU)
    sAPDUFinal = sAPDUHeader + bytes_NroToHexa(len(sAPDU)//2) + sAPDU

    #print("simcard_APDUForInstallForInstallApplet - sAPDUFinal = " + str(sAPDUFinal))
    
    return str_SpacesOut(sAPDUFinal)

# simcard_APDUForInstallForInstallApplet_PrepareParams_TagEA ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_APDUForInstallForInstallApplet_PrepareParams_TagEA(sInstance_Params_UICC="", sInstance_Params_APP=""):
    
    #Example SAP
    
    #UICC System Specific Parameters: 
    #800BFF01000000000343504100 
    
    #WITH ACCESSING FILES - ACCESS FOR APPLICATION PIN 1 (IMSI) AND ALWAYS (ICCID):
    #UICC System Specific Parameters: 
    #800BFF01000000000343504100810700040201000400

    #Application specific parameters:
    #05810601F4 002000 373232 333130 31 31 01 0000 0000 0000 00 02 00 0000

    sInstance_Params_UICC = str_SpacesOut(sInstance_Params_UICC)
    sInstance_Params_APP = str_SpacesOut(sInstance_Params_APP)

    # Result Expected
    # EA 16 80 0B FF 01 00 00 00 00 03 43 50 41 00 81 07 00 04 02 01 00 04 00 C9 1C 05 81 06 01 F4 00 20 00 37 32 32 33 31 30 31 31 01 00 00 00 00 00 00 00 02 00 00 00 00

    sAPDU = ""

    if sInstance_Params_UICC != "":
       if str_left(sInstance_Params_UICC, 2) != "80":
          sInstance_Params_UICC = "80" + bytes_NroToHexa(len(sInstance_Params_UICC)//2) + sInstance_Params_UICC
       sAPDU = sAPDU + sInstance_Params_UICC
    else:
       sAPDU = sAPDU + "80 00"
       
    sAPDU = "EA" + bytes_NroToHexa(len(sAPDU)//2) + sAPDU
    
    if sInstance_Params_APP != "":
       if str_left(sInstance_Params_APP, 2) != "C9":
          sInstance_Params_APP = "C9" + bytes_NroToHexa(len(sInstance_Params_APP)//2) + sInstance_Params_APP
       sAPDU = sAPDU + sInstance_Params_APP
    else:
       sAPDU = sAPDU + "C9 00"
          
    #print("simcard_APDUForInstallForInstallApplet_PrepareParams_TagEA - sAPDU = " + str(sAPDU))
    
    return sAPDU

# simcard_AppletLoadPackage ---------------------------------------------------------------------------------------------------------------------------------------------------------
# It returns: bReturn, lstLastAPDUs, lstLastPoR, sCouter
# Where:
#       bReturn => True (Everything OK) or False (there is an error)
#       lstLastAPDUs => List of APDUs + response
#       lstLastPoR => List of PoR (Proof of Receipt) for each last APDU + response
#       sCounter => Last counter, incremented depending on MSL.
def simcard_AppletSendAPDUsList(cardservice, sLogFileName, lstAPDUs, sTPDA=sSimcard_MSLDefTPDA, sTAR=sSimcard_MSLDefTAR_RAM, sMSL=sSimcard_MSLDefMAC, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter, bDelayAPDU=False, sSeparaResult=sSimcard_ErrorListSepara):

    lstLastAPDUs = []
    lstLastPoR = []
    bReturn = True
    
    #print("simcard_AppletSendAPDUsList - APDUs List=" + str(lstAPDUs) + " - Total APDUs=" + str(len(lstAPDUs)))
    #print("simcard_AppletSendAPDUsList - TPDA=" + str(sTPDA))
    #print("simcard_AppletSendAPDUsList - TAR=" + str(sTAR))
    #print("simcard_AppletSendAPDUsList - MSL=" + str(sMSL))
    #print("simcard_AppletSendAPDUsList - KIC=" + str(sKIC))
    #print("simcard_AppletSendAPDUsList - KID=" + str(sKID))
    #print("simcard_AppletSendAPDUsList - Counter=" + str(sCounter))

    bReturn = True
    bNetworkOKOrChangeIMEIOrChangeMCCMNC = True
    sMCC = ""
    sMNC = ""
    
    sReturn = ""
    
    n = 0
    while n < len(lstAPDUs) and bReturn:

          sMsg = "Sending APDU " + str(n+1) + " from total " + str(len(lstAPDUs)) + " ..."
          sMsg = sMsg + " TPDA: 0x" + str_AddSpaceHexa(sTPDA)
          sMsg = sMsg + " - TAR: 0x" + str_AddSpaceHexa(sTAR)
          sMsg = sMsg + " - MSL: 0x" + str_AddSpaceHexa(sMSL)
          sMsg = sMsg + " - Counter: 0x" + str_AddSpaceHexa(sCounter)
          log_writePrintOnlyWarning(sMsg)

          #ADDING A DELAY PER BLOCK
          if bDelayAPDU:
             simcard_TimeDelay("APDU " + str(n))
          
          if lstAPDUs[n] != "":
             sReturn, sReturnDes = simcardCmd_sendEnvelopeConcat(cardservice, sLogFileName, lstAPDUs[n], sTPDA, sTAR, bNetworkOKOrChangeIMEIOrChangeMCCMNC, sMCC, sMNC, sMSL, sKIC, sKID, sCounter)
             lstLastAPDUs.append(lstAPDUs[n] + sSeparaResult + sReturnDes)

             #GETTING PoR    
             sPoR, sPorDes = simcard_APDUResponseGettingPoR(sReturn)
                      
             lstLastPoR.append(sPoR)
             
             #print("simcard_AppletSendAPDUsList: PoR = " + sPoR + " - " + sMsg + " - sPorDes = " + sPorDes)
             
             if not simcard_AppletPoRCheckOK(sReturn):
                # NOT OK
                bReturn = False

          if sReturn == "":
             bReturn = False
          else:
             # Increment Counter when there is the case
             sCounter = simcard_MSL_IncrementCounter(sMSL, sCounter)
             
          n = n + 1

    #print("simcard_AppletSendAPDUsList - bReturn = " + str(bReturn))
    
    return bReturn, lstLastAPDUs, lstLastPoR, sCounter


# simcard_APDUResponseGettingPoR ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_APDUResponseGettingPoR(sAPDUResponse):

    sPoR = ""
    sPoRDes = ""
    
    sAPDU = sAPDUResponse
    
    #print("\n\nsimcard_APDUResponseGettingPoR - sAPDUResponse = " + str(sAPDUResponse) + "\n\n")
    
    lstAPDUCmds = sAPDU.split(sSimcard_SeparaAPDUForLastAPDUs_Visible)
    if len(lstAPDUCmds) > 1:
       sAPDU = lstAPDUCmds[0] 

    if sSimcard_Asterics in sAPDU:
       lstAPDUCmds = sAPDU.split(sSimcard_Asterics)
       n = 0 
       while n < len(lstAPDUCmds):
             #if sSimcard_SMSAnswerForSPI2Request_Pattern in lstAPDUCmds[n]:
             if simcard_IfInSMS_sSimcard_SMSAnswerForSPI2Request_Pattern(lstAPDUCmds[n]):
                sAPDU = lstAPDUCmds[n]
                if "." in sAPDU:
                   sAPDU = str_getSubStringFromOcur(sAPDU, ".", 1)
                n = len(lstAPDUCmds)
             n = n + 1    

    #print("\n\nsimcard_APDUResponseGettingPoR - sAPDU = " + str(sAPDU) + "\n\n")
    
    sSMSDataOnly = simcard_SendSMSCmd_Interpret_GetTPUD(sAPDU)
    if sSMSDataOnly != "":
       bIsResponseForPoR, sSMSData, sDataASCII = simcard_SendSMSCmd_InterpretData_IsResponseForPoR(sSMSDataOnly)
       sPoRDes = sSMSData    
        
    if len(str_SpacesOut(sAPDU)) >= 4:  
       sPoRDesT, sTAR, sPoR = simcard_3GPP23048_ResponseAnalisys_GetPoRAndTAR(sAPDU)          
       if sPoRDes == "" and sPoRDesT != "":
          sPoRDes = sPoRDesT

    #print("simcard_APDUResponseGettingPoR - sPoR = " + str(sPoR) + " - sPoRDes = " + str(sPoRDes))
    
    return sPoR, sPoRDes

           
# simcard_AppletLoadAndInstall ---------------------------------------------------------------------------------------------------------------------------------------------------------
# NOT BEING USED PER NOW - 2025-08-06
def simcard_AppletLoadAndInstall(CardService, sLogFileName, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, sAppletPathFile, sAIDPackage, sAIDApplet, sAIDInstance, sParamsUICC, sParamsAPP, bInstanceAIDDelete=False, bDelete=True, bLoadPackage=True, bInstallApplet=True):

    sTAR = str_SpacesOut(sTAR)
    sTPDA = str_SpacesOut(sTPDA)
    sMSL = str_SpacesOut(sMSL)
    sKIC = str_SpacesOut(sKIC)
    sKID = str_SpacesOut(sKID)
    sCounter = str_SpacesOut(sCounter)
    sCounterInit = sCounter
    sAIDPackage = str_SpacesOut(sAIDPackage)
    sAIDApplet = str_SpacesOut(sAIDApplet)
    sAIDInstance = str_SpacesOut(sAIDInstance)
    sParamsUICC = str_SpacesOut(sParamsUICC)
    sParamsAPP = str_SpacesOut(sParamsAPP)
    
    bReturn = True
    
    #print("simcard_AppletLoadAndInstall - bInstanceAIDDelete = " + str(bInstanceAIDDelete))
    #print("simcard_AppletLoadAndInstall - bDelete = " + str(bDelete))
    #print("simcard_AppletLoadAndInstall - bLoadPackage = " + str(bLoadPackage))
    #print("simcard_AppletLoadAndInstall - bInstallApplet = " + str(bInstallApplet))
    
    
    if sAIDApplet=="":
       sAIDApplet = sAIDInstance
    
    # IT IS BEING VALIDATED THE PARAMETERS
    sMsg = "Validating parameters:"
    sMsg = sMsg + "\nTAR: 0x" + str_AddSpaceHexa(sTAR)
    sMsg = sMsg + "\nTPDA: 0x" + str_AddSpaceHexa(sTPDA)
    sMsg = sMsg + "\nMSL: 0x" + str_AddSpaceHexa(sMSL)
    sMsg = sMsg + "\nKIC: 0x" + str_AddSpaceHexa(sKIC) + " - " + simcard_DescriptionLength(sKIC)
    sMsg = sMsg + "\nKID: 0x" + str_AddSpaceHexa(sKID) + " - " + simcard_DescriptionLength(sKID)
    sMsg = sMsg + "\nCounter: 0x" + str_AddSpaceHexa(sCounter)
    log_write_InfoInBlue(sLogFileName, sMsg)
    bReturn, sError = simcard_ValidateMSLParams(sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, "")
    if not bReturn:
       log_write_ErrorInRed(sLogFileName, sError)
       return False, sError

    if bDelete and bInstanceAIDDelete:
       # IT IS BEING REMOVE THE INSTANCE AID, BEFORE, JUST IN CASE. Example Thales chips.
       sMsg = "Deleting instance with: \nAID: " + str_SpaceHexa(sAIDInstance) + ", if it exists in the SIM."
       log_write_InfoInBlue(sLogFileName, sMsg)
       bReturn, sLastAPDUs, sLastPoR, sCounter = simcard_AppletDeletePackageOrInstance(CardService, sLogFileName, sAIDPackage, False, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter)
       sCounter = simcard_MSL_IncrementCounter(sMSL, sCounter)

       sMsg = "Last PoR, after deleting instance with AID '" + str_SpaceHexa(sAIDInstance) + "': 0x" + str_AddSpaceHexa(sLastPoR) + " - " + simcard_ErrorListGetDes(sLastPoR)
       if str(sCounter) != str(sCounterInit):
          sMsg = sMsg + "\nNew Counter = 0x" + str_AddSpaceHexa(sCounter) + " - Decimal = " + bytes_HexaToNro(sCounter)
       if bReturn:
          log_write_OKInGreen(sLogFileName, sMsg)
       else:
          log_write_ErrorInRed(sLogFileName, sMsg)    

    
    if bDelete:
       # IT IS BEING REMOVE THE PACKAGE, BEFORE, JUST IN CASE
       sMsg = "Deleting package with: \nAID: " + str_SpaceHexa(sAIDPackage) + ", if it exists in the SIM."
       log_write_InfoInBlue(sLogFileName, sMsg)
       bReturn, sLastAPDUs, sLastPoR, sCounter = simcard_AppletDeletePackageOrInstance(CardService, sLogFileName, sAIDPackage, True, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter)
       sCounter = simcard_MSL_IncrementCounter(sMSL, sCounter)

       sMsg = "Last PoR, after deleting package with AID '" + str_SpaceHexa(sAIDPackage) + "': 0x" + str_AddSpaceHexa(sLastPoR) + " - " + simcard_ErrorListGetDes(sLastPoR)
       if str(sCounter) != str(sCounterInit):
          sMsg = sMsg + "\nNew Counter = 0x" + str_AddSpaceHexa(sCounter) + " - Decimal = " + bytes_HexaToNro(sCounter)
       if bReturn:
          log_write_OKInGreen(sLogFileName, sMsg)
       else:
          log_write_ErrorInRed(sLogFileName, sMsg)    

    
    if bLoadPackage:
       # LOADING PACKAGE
       sMsg = "Started loading package with: \nAID: " + str_SpaceHexa(sAIDPackage) + "\nFile: '" + sAppletPathFile + "."
       if str(sCounter) != str(sCounterInit):
          sMsg = sMsg + "\nNew Counter = 0x" + str_AddSpaceHexa(sCounter)
       log_write_InfoInBlue(sLogFileName, sMsg)

       bReturn, lstLastAPDUs, lstLastPoR, sCounter = simcard_AppletLoadPackage(CardService, sLogFileName, sAppletPathFile, sAIDPackage, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter)

       sLastPoR = ""
       if len(lstLastPoR) > 0:
          sLastPoR = lstLastPoR[len(lstLastPoR)-1]
       sMsg = "Ended loading package with: \nAID: " + str_SpaceHexa(sAIDPackage) + "\nFile: '" + sAppletPathFile + "'\nTotal APDUs = " + str(len(lstLastAPDUs)) 
       sMsg = "Last PoR, after loading package: "
       if sLastPoR == "":
          sMsg = sMsg + "UNKOWN."
       else:
          sMsg = sMsg + " 0x" + str_AddSpaceHexa(sLastPoR) + " - " + simcard_ErrorListGetDes(sLastPoR)
       if str(sCounter) != str(sCounterInit):
          sMsg = sMsg + "\nNew Counter = 0x" + str_AddSpaceHexa(sCounter) + " - Decimal = " + bytes_HexaToNro(sCounter)
       #print("simcard_AppletLoadAndInstall - Load Package. Counter = " + str(sCounter) + " - sCounterInit = " + str(sCounterInit))
    
       if bReturn:
          log_write_OKInGreen(sLogFileName, sMsg)
       else:
          log_write_ErrorInRed(sLogFileName, sMsg)    
          return False

    if bInstallApplet:
    
       # INSTALLING APPLET
       sMsg = "Installing Applet:"
       sMsg = sMsg + "\nPackage AID: " + str_SpaceHexa(sAIDPackage) + " - " + simcard_DescriptionLength(sAIDPackage)
       sMsg = sMsg + "\nApplet AID: " + str_SpaceHexa(sAIDApplet) + " - " + simcard_DescriptionLength(sAIDApplet)
       sMsg = sMsg + "\nInstance AID: " + str_SpaceHexa(sAIDInstance) + " - " + simcard_DescriptionLength(sAIDInstance)
       sMsg = sMsg + "\nParameters UICC: " + str_SpaceHexa(sParamsUICC) + " - " + simcard_DescriptionLength(sParamsUICC)
       sMsg = sMsg + "\nParameters Application, tag 0xC9: " + str_SpaceHexa(sParamsAPP) + " - " + simcard_DescriptionLength(sParamsAPP)
       sCounter = simcard_MSL_IncrementCounter(sMSL, sCounter)
       if str(sCounter) != str(sCounterInit):
          sMsg = sMsg + "\nNew Counter = 0x" + str_AddSpaceHexa(sCounter) + " - Decimal = " + bytes_HexaToNro(sCounter)
       log_write_InfoInBlue(sLogFileName, sMsg)
       
       bReturn, sLastAPDUs, sLastPoR, sCounter = simcard_AppletInstallForInstall(CardService, sLogFileName, sAIDPackage, sAIDApplet, sAIDInstance, "", sParamsUICC, sParamsAPP, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter)
       
       sMsg = "Last PoR, after installing applet: 0x" + str_AddSpaceHexa(sLastPoR) + " - " + simcard_ErrorListGetDes(sLastPoR)
       #print("simcard_AppletLoadAndInstall - Install for Install. Counter = " + str(sCounter) + " - sCounterInit = " + str(sCounterInit))
       
       if str(sCounter) != str(sCounterInit):
          sMsg = sMsg + "\nNew Counter = 0x" + str_AddSpaceHexa(sCounter) + " - Decimal = " + bytes_HexaToNro(sCounter)

       if bReturn:
          log_write_OKInGreen(sLogFileName, sMsg)
       else:
          log_write_ErrorInRed(sLogFileName, sMsg)    
          return False

       
    return True

# simcard_Applet_CheckInstanceExists ---------------------------------------------------------------------------------------------------------------------------------------------------------
# THIS DOES NOT WORK THROUGH SMPP MESSAGES TO RAM
#def simcard_Applet_CheckInstanceExists(CardService, sLogFileName, sAIDInstance, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, sSeparaResult=sSimcard_ErrorListSepara):
# 
#    lstAPDUs = []
#    
#    sAIDInstance = str_SpacesOut(sAIDInstance)
#    if sAIDInstance == "":
#       return False, "", "", sCounter
#    
#    #SELECT APPLET INSTANCE
#    #00 A4 04 04 09 A0 00 00 01 51 41 43 4C 00
#    sAPDU = "00 A4 04 04 " + bytes_NroToHexa(len(sAIDInstance)//2) + sAIDInstance
#    lstAPDUs.append(sAPDU)
#
#    bReturn, lstLastAPDUs, lstLastPoR, sCounter = simcard_AppletSendAPDUsList(CardService, sLogFileName, lstAPDUs, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, sSeparaResult)
#
#    sLastAPDU = lstLastAPDUs[0]
#    sLastPoR = lstLastPoR[0]
#        
#    return bReturn, sLastAPDU, sLastPoR, sCounter

# simcard_GetData ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetData_FreeMemory(CardService, sLogFileName, sTPDA=sSimcard_MSLDefTPDA, sTAR=sSimcard_MSLDefTAR_RAM, sMSL=sSimcard_MSLDefMAC, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter, sSeparaResult=sSimcard_ErrorListSepara):
    bReturn, lstLastAPDUs, lstLastPoR, sCounter, sAppInstalled, sFreeNonVolatileMemory, sFreeVolatileMemory, sCardRecognitionData = simcard_GlobalPlatformGetData(CardService, sLogFileName, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, False)
    return bReturn, lstLastAPDUs, lstLastPoR, sCounter, sAppInstalled, sFreeNonVolatileMemory, sFreeVolatileMemory

# simcard_GetData ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetData_All(CardService, sLogFileName, sTPDA=sSimcard_MSLDefTPDA, sTAR=sSimcard_MSLDefTAR_RAM, sMSL=sSimcard_MSLDefMAC, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter, sSeparaResult=sSimcard_ErrorListSepara):
    bReturn, lstLastAPDUs, lstLastPoR, sCounter, sAppInstalled, sFreeNonVolatileMemory, sFreeVolatileMemory, sCardRecognitionData = simcard_GlobalPlatformGetData(CardService, sLogFileName, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter)
    return bReturn, lstLastAPDUs, lstLastPoR, sCounter
    
# simcard_GetData ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetData(CardService, sLogFileName, sTPDA=sSimcard_MSLDefTPDA, sTAR=sSimcard_MSLDefTAR_RAM, sMSL=sSimcard_MSLDefMAC, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter,  bGetAll=True, sSeparaResult=sSimcard_ErrorListSepara):
 
    lstAPDUs = []
    
    sDes = ""
    sAppInstalled = ""
    sFreeNonVolatileMemory = ""
    sFreeVolatileMemory = ""
    sCardRecognitionData = ""
    
    #GET DATA 
    if bGetAll == True:
       # 0xCA because 0x80
       # 0x66 = Card Data (or Security Domain Management Data);
       # Tag '66': Card Data => ETSI 102.226
       sAPDU = "80 CA 00 66 00"
       lstAPDUs.append(sAPDU)
   
    # 0xFF 21 = Extended Card Resources Information available for Card Content Management, as defined in ETSI TS 102 226.
    sAPDU = "80 CA FF 21 00"
    lstAPDUs.append(sAPDU)

    # 0x2F 00 = List of Applications associated with the Security Domain, or every application on the card if the Security Domain has Global Registry Privilege.
    #sAPDU = "80 CA 2F 00 00"
    #lstAPDUs.append(sAPDU)

    bReturn, lstLastAPDUs, lstLastPoR, sCounter = simcard_AppletSendAPDUsList(CardService, sLogFileName, lstAPDUs, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, False, sSeparaResult)
    
    n = 0
    while n < len(lstLastAPDUs):
    
          sDes = ""
          
          #print("\nsimcard_GlobalPlatformGetData - " + str(n) + ". lstLastAPDUs = " + str(lstLastAPDUs[n]) + " - Last PoR = " + str(lstLastPoR[n]))
          
          bTagFF21FreeMemory = True
          if len(lstLastAPDUs) > 1 and n == 0:
             #APDU with 0x66
             bTagFF21FreeMemory = False
            
          tlv, tlv_data, sAppInstalled, sFreeNonVolatileMemory, sFreeVolatileMemory, sCardRecognitionData = simcard_GlobalPlatformGetData_Response(lstLastAPDUs[n], bTagFF21FreeMemory)

          #print("simcard_GlobalPlatformGetData - sAppInstalled = " + str(sAppInstalled) + " - sFreeNonVolatileMemory = " + str(sFreeNonVolatileMemory) + " - sFreeVolatileMemory = " + str(sFreeVolatileMemory)) 
          #print("simcard_GlobalPlatformGetData - tlv = " + str(tlv) + " - tlv_data = " + str(tlv_data)) 
          
          if len(tlv) > 0:
             m = 0
             while m < len(tlv):
                   sDes = sDes + "\nTLV [" + str(m) + "] = 0x" + str(tlv[m])
                   sDes = sDes + "\nTLV [" + str(m) + "] data = 0x" + str_SpaceHexa(str(tlv_data[m]))
                   m = m + 1
          
          if sAppInstalled != "":
             sDes = "\n" + simcard_GlobalPlatformGetData_FreeMemory_Des(sAppInstalled, sFreeNonVolatileMemory, sFreeVolatileMemory)
          else:
             sDes = sDes + "\n" + sCardRecognitionData 
             
          lstLastAPDUs[n] = lstLastAPDUs[n] + sSeparaResult + sDes 
          
          n = n + 1

    return bReturn, lstLastAPDUs, lstLastPoR, sCounter, sAppInstalled, sFreeNonVolatileMemory, sFreeVolatileMemory, sCardRecognitionData

# simcard_GlobalPlatformGetStatus ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetStatus(CardService, sLogFileName, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, tAIDsToSearch, sSeparaResult=sSimcard_ErrorListSepara):

    tAIDs = []

    lstLastAPDUs = []
    lstLastPoR = []

    # GETTING SECURITY DOMAIN APPLETs    
    #P1 = GET STATUS - '80' – Issuer Security Domain
    #It is added the GET RESPONSE at the end for responses such as 0x61 XX
    #P2 - 0x02 => Response data structure according to Table 11-36 and 37
    sAPDU = "80 F2 80 02 02 4F 00 00 C0 00 00 00"        
    
    bReturn, lstLastAPDUsT, lstLastPoRT, sCounter, tAIDsT = simcard_GlobalPlatformGetStatus_Process(CardService, sLogFileName, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, tAIDsToSearch, sAPDU, sSeparaResult)

    lstLastAPDUs.extend(lstLastAPDUsT)
    lstLastPoR.extend(lstLastPoRT)
    tAIDs.extend(tAIDsT)       

    if bReturn:       
       # GETTING APPLICATIONS AND SUPPLEMENTARY APPLETs    
       #P1 = GET STATUS - '40' – Applications and Supplementary Security Domains only. - APPLETS
       sP1 = "40"
       bReturn, lstLastAPDUsT, lstLastPoRT, sCounter, tAIDsT = simcard_GlobalPlatformGetStatus_MoreDataExpected(CardService, sLogFileName, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, tAIDsToSearch, sP1, sSeparaResult)

       lstLastAPDUs.extend(lstLastAPDUsT)
       lstLastPoR.extend(lstLastPoRT)
       tAIDs.extend(tAIDsT)       
    
    if bReturn:
       #P1 = GET STATUS - '10' – Executable Load Files and their Executable Modules only.
       sP1 = "10"
       bReturn, lstLastAPDUsT, lstLastPoRT, sCounter, tAIDsT = simcard_GlobalPlatformGetStatus_MoreDataExpected(CardService, sLogFileName, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, tAIDsToSearch,  sP1, sSeparaResult)

       lstLastAPDUs.extend(lstLastAPDUsT)
       lstLastPoR.extend(lstLastPoRT)
       tAIDs.extend(tAIDsT)       
    
    #REMOVE DUPLICATES
    tAIDs = list(set(tAIDs))
    #SORT AIDs LIST
    tAIDs.sort()
    
    return bReturn, lstLastAPDUs, lstLastPoR, sCounter, tAIDs

# simcard_GlobalPlatformGetStatus_MoreDataExpected ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetStatus_MoreDataExpected(CardService, sLogFileName, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, tAIDsToSearch, sP1, sSeparaResult=sSimcard_ErrorListSepara):

    bReturn = True
    
    tAIDs = []

    lstLastAPDUs = []
    lstLastPoR = []

    # GETTING APPLICATIONS AND SUPPLEMENTARY APPLETs    
    #P1 = GET STATUS - '40' – Applications and Supplementary Security Domains only. - APPLETS
    #It is added the GET RESPONSE at the end for responses such as 0x61 XX
    sAPDU_CLAINSPI1 = "80 F2 " + sP1 

    sP1Des = "Applications and Supplementary Security Domains only"
    if sP1 == "10":
       sP1Des = "Executable Load Files and their Executable Modules only"
       
    #APDU Valid Propietary
    #sAPDU_NEXT = "0B 4F 00 5C 07 4F 9F 70 C5 CC C4 CF 00 C0 00 00 00"
    sAPDU_NEXT = "02 4F 00 00 C0 00 00 00"

    #P2 - 0x02 => Response data structure according to Table 11-36 and 37
    sAPDU_P2 = "02"
    bContinue = True
    n = 0
    sLastPoR = ""
    while bContinue and bReturn and n < 50:

          if n > 0:
             #P2 - 0x03 => Response data structure according to Table 11-36 and 37 + Get next occurrence(s)
             sAPDU_P2 = "03"

           #P2 - 0x02 => Response data structure according to Table 11-36 and 37
          sAPDU = sAPDU_CLAINSPI1 + sAPDU_P2 + sAPDU_NEXT

          sLog = "Get Status for '" + sP1 + "' - " + sP1Des + "."
          sLog = sLog + ". APDU: 0x" + str_SpaceHexa(sAPDU) + " - Ocurrence: " + str(n)
          log_writePrintOnlyWarning(sLog)

          bReturn, lstLastAPDUsT, lstLastPoRT, sCounter, tAIDsT = simcard_GlobalPlatformGetStatus_Process(CardService, sLogFileName, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, tAIDsToSearch, sAPDU, sSeparaResult)

          if bReturn:
             lstLastAPDUs.extend(lstLastAPDUsT)
             lstLastPoR.extend(lstLastPoRT)
    
             tAIDs.extend(tAIDsT)       
          
          sLastPoR = lstLastPoRT[len(lstLastPoRT)-1]
          if sLastPoR != "":
             if not simcard_AppletPoRCheckOK_List(sLastPoR):
                bContinue = False
             else:
                if sLastPoR == sSimcard_9000 and n == 0:
                   bContinue = False
          else:
             bContinue = False

          
          sLog = sLog + " - PoR: " + sLastPoR
          log_write_WarningInYellow(sLogFileName, sLog)

          n = n + 1

    if sLastPoR == sSimcard_6A86_IncorrectPIP2:
       #THIS IS BECAUSE THERE ARE NO MORE AIDs TO RETRIEVE
       lstLastPoR[len(lstLastPoR)-1] = sSimcard_6310_MoreData          
       bReturn = True

    return bReturn, lstLastAPDUs, lstLastPoR, sCounter, tAIDs

# simcard_GlobalPlatformGetStatus ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetStatus_Process(CardService, sLogFileName, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, tAIDsToSearch, sAPDUs, sSeparaResult=sSimcard_ErrorListSepara):
 
    tAIDs = []
    
    lstAPDUs = []
    lstAPDUs.append(str_SpacesOut(sAPDUs))

    bReturn, lstLastAPDUs, lstLastPoR, sCounter = simcard_AppletSendAPDUsList(CardService, sLogFileName, lstAPDUs, sTPDA, sTAR, sMSL, sKIC, sKID, sCounter, False, sSeparaResult)
    
    sResponse = ""
    sDes = ""
    sDesApplets = ""
    sDesAppletsSearchFor = ""
    
    n = 0
    while n < len(lstLastAPDUs):
    
          sDes = ""
          
          #log_writePrintOnlyInfo("\nGet Status Process - [" + str(n) + "]: simcard_GlobalPlatformGetStatus - " + str(n) + ". lstLastAPDUs = " + str(lstLastAPDUs[n]) + " - Last PoR = " + str(lstLastPoR[n]))
          #log_writePrintOnlyInfo("\nGet Status Process - [" + str(n) + "]: simcard_GlobalPlatformGetStatus - " + str(n) + ". Last PoR = " + str(lstLastPoR[n]))
          
          tlv, tlv_data, sResponse, tAIDst = simcard_GlobalPlatformGetStatus_Response(lstLastAPDUs[n], lstLastPoR[n])

          if len(tAIDst) > 0:
              tAIDs.extend(tAIDst) 
              
          if len(tlv) > 0:
             m = 0
             while m < len(tlv):
                   sDes = sDes + "\nTLV [" + str(m) + "] = 0x" + str(tlv[m])
                   sDes = sDes + "\nTLV [" + str(m) + "] data = 0x" + str_SpaceHexa(str(tlv_data[m]))
                   m = m + 1
          
          if sResponse != "":
             sDes = sDes + "\n" + sResponse 

          #log_writePrintOnlyInfo("\n[Response: " + str(n) + "]: simcard_GlobalPlatformGetStatus - " + str(n) + ". sDes = " + str(sDes))
          
          sDesApplets, sDesAppletsSearchFor = simcard_GetStatus_AppletsFound_Des(tAIDst, tAIDsToSearch)
          
          if sDesApplets != "":
             sDes = sDes + "\n\n" + sDesApplets
          
          if sDes != "":
             lstLastAPDUs[n] = lstLastAPDUs[n] + sSeparaResult + sDes 

          n = n + 1

    #log_writePrintOnlyInfo("\nsimcard_GlobalPlatformGetStatus - lstLastAPDUs = " + str(lstLastAPDUs) + " - lstLastPoR = " + str(lstLastPoR))

    return bReturn, lstLastAPDUs, lstLastPoR, sCounter, tAIDs

# simcard_TLVProcess ---------------------------------------------------------------------------------------------------------------------------------------------------------
# sBytecode => bytes with the format Tag + Length + Value
# It is returned 2 lists:
# tlv[] => each tag
# tlv_data[] => each data that belongs to each tag
# result => simcard_TLVProcess - tlv = ['81', '82', '83'] - tlv_data = ['0015', '000081BF', '0000050C']
def simcard_TLVProcess(sBytecode):
    
    tlv = []
    tlv_data = []
    
    sBytes = str_SpacesOut(sBytecode)
    
    #print("simcard_TLVProcess - sBytes = " + str(sBytes))
    
    n = 0
    while n < len(sBytes):
    
          sTag = str_mid(sBytes, n, 2)
          n = n + 2
          sLen = str_mid(sBytes, n, 2)
          n = n + 2
          nLen = bytes_HexaToNro(sLen)
          nLen = int(nLen) * 2
          sData = str_mid(sBytes, n, nLen)
          n = n + nLen

          #print("simcard_TLVProcess - sTag = " + str(sTag) + " - sData = " + str(sData) + " - n = " + str(n))

          if sTag != "" and sData != "":
             tlv.append(sTag)
             tlv_data.append(sData)
    
    #print("simcard_TLVProcess - tlv = " + str(tlv) + " - tlv_data = " + str(tlv_data))
                 
    return tlv, tlv_data
    

# simcard_APDU_Get3GPP23040_GetUDHFoundOnly ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_APDU_Get3GPP23040_GetUDHFoundOnly(sEnvelope):
    sReturn, sFoundUDH = simcard_APDU_Get3GPP23040_Process(sEnvelope, True)
    return sFoundUDH

# simcard_APDU_Get3GPP23040 ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_APDU_Get3GPP23040(sEnvelope, bGetBytecodeBefore=False, bAddPatternInReturn=True):
    sReturn, sFoundUDH = simcard_APDU_Get3GPP23040_Process(sEnvelope, bGetBytecodeBefore, bAddPatternInReturn)
    return sReturn
    
# simcard_APDU_Get3GPP23040_Process ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_APDU_Get3GPP23040_Process(sEnvelope, bGetBytecodeBefore=False, bAddPatternInReturn=True):
    
    sEnvelope = str_SpacesOut(sEnvelope)

    sReturn = ""    
    sFoundUDH = ""
    
    #sSimcard_3GPP23040_UDH = "027000"
    if sSimcard_3GPP23040_UDH in sEnvelope:
       sFoundUDH = sSimcard_3GPP23040_UDH
    
    #sSimcard_SMSAnswerForSPI2Request_Pattern = "027100"
    if sSimcard_SMSAnswerForSPI2Request_Pattern in sEnvelope:   
       sFoundUDH = sSimcard_SMSAnswerForSPI2Request_Pattern

    if sFoundUDH == "" and sSimcard_3GPP23040_UDH_SMPPConcat_First in sEnvelope:
       #sFoundUDH = sSimcard_3GPP23040_UDH_SMPPConcat_First
       
       #BECAUSE THERE ARE DIFFERENT SMPP CONCATENATED
       sTemp = str_getSubStringFromOcur(sEnvelope, sSimcard_3GPP23040_UDH_SMPPConcat_First, 1)
       sTemp = str_left(sTemp, nSimcard_3GPP23040_UDH_SMPPConcat_First_Len - (len(sSimcard_3GPP23040_UDH_SMPPConcat_First)//2))

       #print("simcard_APDU_Get3GPP23040_Process - sTemp = " + str(sTemp))

       sFoundUDH = sSimcard_3GPP23040_UDH_SMPPConcat_First + sTemp

    if sFoundUDH == "" and sSimcard_3GPP23040_UDH_SMPPConcat_Next in sEnvelope:
       sFoundUDH = sSimcard_3GPP23040_UDH_SMPPConcat_Next

    if bGetBytecodeBefore: 
       sReturn = str_getSubStringFromOcur(sEnvelope, sFoundUDH, 0)
    else:
       sReturn = str_getSubStringFromOcurAfterFirstOnly(sEnvelope, sFoundUDH, bAddPatternInReturn)

    #print("simcard_APDU_Get3GPP23040_Process - sFoundUDH = " + str(sFoundUDH) + " - sReturn = " + str(sReturn))
   
    if sReturn == "" and not bGetBytecodeBefore:          
       return sEnvelope, sFoundUDH
    else:       
       return sReturn, sFoundUDH

# simcard_GlobalPlatformGetData_ResponseGetStatus ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetStatus_Response(sSMS, sPoR):

    tlv = []
    tlv_data = []
    tAIDs = []
    
    sResponse = ""

    #log_writePrintOnlyInfo("simcard_GlobalPlatformGetStatus_Response - BEFORE sSMS = " + str(sSMS) + " - sPoR = " + str(sPoR))

    if sPoR == sSimcard_6310_MoreData or sPoR == sSimcard_9000:
       #PUT TOGETHER ALL SMS_DATA
       tSMSData = sSMS.split(sSimcard_SendSMSDATAPattern)
   
       sSMS = ""
       #IT IS STARTED FROM THE 2nd RECORD BECAUSE IN THE FISRT ONE THERE IS NO 'SMS DATA:'
       n = 1
       while n < len(tSMSData):
             
             if sSimcard_SendSMSDATAPatternASCII in tSMSData[n]:
                tSMSData[n] = str_getSubStringFromOcurFirst(tSMSData[n], sSimcard_SendSMSDATAPatternASCII)
             
             sSMS = sSMS + tSMSData[n]

             #print("simcard_GlobalPlatformGetStatus_Response - " + str(n) + ". tSMSData[n] = " + str(tSMSData[n]))
             
             n = n + 1

    #log_writePrintOnlyInfo("simcard_GlobalPlatformGetStatus_Response - AFTER sSMS = " + str(sSMS))
    
    sSMS = str_SpacesOut(sSMS)
    
    # sSimcard_SMSAnswerForSPI2Request_Pattern = "027100"
    #if sSimcard_SMSAnswerForSPI2Request_Pattern in sSMS and len(sSMS) > 18: 
    bFound, s027100 = simcard_Get_sSimcard_SMSAnswerForSPI2Request_Pattern(sSMS)
    if bFound and s027100 != "":
    
       #s027100 = str_getSubStringFromOcur(sSMS, sSimcard_SMSAnswerForSPI2Request_Pattern, 1)

       #print("simcard_GlobalPlatformGetStatus_Response - s027100 = " + str(s027100))
       
       #GlobalPlatform Registry related data = E3
       sTag = "E3"
       
       if sTag in s027100:
       
          tE3 = s027100.split(sTag)
          #print("simcard_GlobalPlatformGetStatus_Response - tE3 = " + str(tE3) + " - len(tE3) = " + str(len(tE3)))
          
          #n = 1 because it is not needed those bytes before the 1st 'E3'
          n = 1
          while n < len(tE3):
                
                #sData = str_TrimCleanSpaces(str_getSubStringFromOcur(s027100, sTag, 1))
                sData = tE3[n]

                #print("simcard_GlobalPlatformGetStatus_Response - [" + str(n) + ". sData BEFORE = " + str(sData))
          
                sDataLen = str_left(sData, 2)
                nDataLen = bytes_HexaToNro(sDataLen) 

                if int(nDataLen) > 0:
                   #print("simcard_GlobalPlatformGetStatus_Response - nDataLen = " + str(nDataLen))

                   sData = str_mid(sData, 2, int(nDataLen) * 2)

                   #SMS Data: 0x02 71 00 00 23 0A 00 00 00 00 00 00 00 01 00 00 02 90 00 E3 13 4F 08 A0 00 00 01 51 00 00 00 9F 70 01 0F C5 03 9A FD 80
                   #Data only = E3 13 4F 08 A0 00 00 01 51 00 00 00 9F 70 01 0F C5 03 9A FD 80
                   sData = sTag + sDataLen + sData

                   #print("simcard_GlobalPlatformGetStatus_Response - [" + str(n) + "] sData AFTER = " + str(sData))
                
                   #GET EACH VALUE
                   tlv, tlv_data = simcard_TLVProcess(sData)
          
                   if sData != "":
                      sResponset, tAIDst = simcard_GlobalPlatformGetStatus_ApplicationData(sData)         
                   
                      sResponse = sResponse + sResponset
                      
                      tAIDs.extend(tAIDst)     

                      #print("simcard_GlobalPlatformGetStatus_Response - [" + str(n) + "] tAIDs = " + str(tAIDs) + " - len tAIDs = " + str(len(tAIDs)))
                
                n = n + 1

    #REMOVE DUPLICATES
    tAIDs = list(set(tAIDs))

    return tlv, tlv_data, sResponse, tAIDs
    

# simcard_GlobalPlatformGetData_Response ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetData_Response(sSMS, bTagFF21FreeMemory=True):

    #Example for SMS:
    #0xD0 43 81 03 01 13 00 82 02 81 83 05 00 06 04 81 21 43 F5 8B 30 41 00 05 81 06 01 F4 00 F6 26 02 71 00 00 21 0A 00 00 00 00 00 00 00 01 00 00 01 90 00 FF 21 10 81 02 00 15 82 04 00 00 81 BF 83 04 00 00 05 0C. CMD: 13. Qualifier: 00. Description: 0x13 =>  ETSI 102.223 SIM TOOLKIT COMMAND: 0x13 - SEND SHORT MESSAGE ETSI 102.223 SIM TOOLKIT COMMAND: 0x13 - SEND SHORT MESSAGE
    #TPDA: 0x05 81 06 01 F4 (interpreted: 60104)
    #Protocol ID: 0x00
    #Data Coding Scheme (DCS): 0xF6
    #SMS Length: 0x26 (decimal: 38)
    #SMS Data: 0x02 71 00 00 21 0A 00 00 00 00 00 00 00 01 00 00 01 90 00 FF 21 10 81 02 00 15 82 04 00 00 81 BF 83 04 00 00 05 0C
 
    sSMS = str_SpacesOut(sSMS)

    sNumberInstalledApp = ""
    sFreeNonVolatileMemory = ""
    sFreeVolatileMemory = ""
    sCardRecognitionData = ""
    
    tlv = []
    tlv_data = []
    
    # sSimcard_SMSAnswerForSPI2Request_Pattern = "027100"
    #if sSimcard_SMSAnswerForSPI2Request_Pattern in sSMS and len(sSMS) > 18: 
    bFound, s027100 = simcard_Get_sSimcard_SMSAnswerForSPI2Request_Pattern(sSMS)
    if bFound and s027100 != "":
    
       #s027100 = str_getSubStringFromOcur(sSMS, sSimcard_SMSAnswerForSPI2Request_Pattern, 1)

       if bTagFF21FreeMemory:
          #'FF 21': Extended Card Resources Tag
          sTag = "FF21"
       else:   
          #'66': Card Data
          sTag = "66"
       
       if sTag in s027100:
          sData = str_TrimCleanSpaces(str_getSubStringFromOcur(s027100, sTag, 1))

          #print("simcard_GlobalPlatformGetData_Response - sData = " + str(sData))
          
          sDataLen = str_left(sData, 2)
          nDataLen = bytes_HexaToNro(sDataLen) 
          sData = str_mid(sData, 2, int(nDataLen) * 2)
          
          #print("simcard_GlobalPlatformGetData_Response - sData = " + str(sData) + " - sDataLen = " + str(sDataLen) + " - nDataLen = " + str(nDataLen))

          if sData != "":
             if not bTagFF21FreeMemory:
                #SMS Data: 0x02 71 00 00 74 0A 00 00 00 00 00 00 00 01 00 00 01 90 00 66 64 73 62 06 07 2A 86 48 86 FC 6B 01 60 0B 06 09 2A 86 48 86 FC 6B 02 02 02 63 09 06 07 2A 86 48 86 FC 6B 03 64 0B 06 09 2A 86 48 86 FC 6B 04 02 55 64 0B 06 09 2A 86 48 86 FC 6B 04 80 00 64 0B 06 09 2A 86 48 86 FC 6B 04 81 07 65 0A 06 08 2A 86 48 86 FC 6B 05 04 66 0C 06 0A 2B 06 01 04 01 2A 02 6E 01 02 - ASCII: _q__t______________fdsb__*_H__k_`___*_H__k___c___*_H__k_d___*_H__k__Ud___*_H__k___d___*_H__k___e___*_H__k__f___+____*_n__3GPP 23.048 response for TAR = 00 00 00 => PoR: 0x90 00 = Smartcard: Eveything OK or no response.
                #Data only = 66 64 73 62 06 07 2A 86 48 86 FC 6B 01 60 0B 06 09 2A 86 48 86 FC 6B 02 02 02 63 09 06 07 2A 86 48 86 FC 6B 03 64 0B 06 09 2A 86 48 86 FC 6B 04 02 55 64 0B 06 09 2A 86 48 86 FC 6B 04 80 00 64 0B 06 09 2A 86 48 86 FC 6B 04 81 07 65 0A 06 08 2A 86 48 86 FC 6B 05 04 66 0C 06 0A 2B 06 01 04 01 2A 02 6E 01 02
                sData = str_TrimCleanSpaces(str_getSubStringFromOcur(s027100, sTag, 1))
                sData = sTag + sData
                
          
          #GET EACH VALUE
          tlv, tlv_data = simcard_TLVProcess(sData)
          
          if len(tlv) > 0 and bTagFF21FreeMemory:
             
             n = 0 
             while n < len(tlv):
             
                   if tlv[n] == "81":
                      #Number of installed application tag
                      sNumberInstalledApp = tlv_data[n]
                   if tlv[n] == "82":
                      #Free non volatile memory tag
                      sFreeNonVolatileMemory = tlv_data[n]
                   if tlv[n] == "83":
                      #Free volatile memory tag
                      sFreeVolatileMemory = tlv_data[n]
                       
                   n = n + 1     
          else:
              if sData != "":
                 sCardRecognitionData = simcard_GlobalPlatformGetData_CardRecognitionData(sData)         

    return tlv, tlv_data, sNumberInstalledApp, sFreeNonVolatileMemory, sFreeVolatileMemory, sCardRecognitionData
    
# simcard_GlobalPlatformGetData_CardRecognitionData ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetData_CardRecognitionData(sData):

    #Example for SMS:
    #SMS Data: 0x02 71 00 00 74 0A 00 00 00 00 00 00 00 01 00 00 01 90 00 
    #66 64 73 62 06 07 2A 86 48 86 FC 6B 01 60 0B 06 09 2A 86 48 86 FC 6B 02 02 02 63 09 06 07 2A 86 48 86 FC 6B 03 64 0B 06 09 2A 86 48 86 FC 6B 04 02 55 64 0B 06 09 2A 86 48 86 FC 6B 04 80 00 64 0B 06 09 2A 86 48 86 FC 6B 04 81 07 65 0A 06 08 2A 86 48 86 FC 6B 05 04 66 0C 06 0A 2B 06 01 04 01 2A 02 6E 01 02 - ASCII: _q__t______________fdsb__*_H__k_`___*_H__k___c___*_H__k_d___*_H__k__Ud___*_H__k___d___*_H__k___e___*_H__k__f___+____*_n__3GPP 23.048 response for TAR = 00 00 00 => PoR: 0x90 00 = Smartcard: Eveything OK or no response.

    sData = str_SpacesOut(sData)

    #print("simcard_GlobalPlatformGetData_CardRecognitionData - sData = " + str(sData))
    
    sCardRecognitionData = ""
    
    tlv = []
    tlv_data = []
    
    # Standard Global Platform 2.3
    # Card Data tag = 0x66
    # Data objects identified in [ISO 7816-6], including tag '73'
    # Global Platform standard: Table H-1: Structure of Card Recognition Data (Format 1)
    
    n = 0
    sDes = "\n\nData according to standard Global Platform - Table H-1: Structure of Card Recognition Data (Format 1)"
    
    sDes = sDes + "\n0x" + str_mid(sData, n, 2)
    if str_mid(sData, n, 2) == "66":
       sDes = sDes + " - Card Data tag - Data objects identified in [ISO 7816-6], including tag '73'"
    n = n + 2

    #0x64 = length
    sLen = str_mid(sData, n, 2)
    sDes = sDes + "\n" + bytes_LengthDescription(sLen)
    n = n + 2
       
    sDes = sDes + "\n0x" + str_mid(sData, n, 2)
    if str_mid(sData, n, 2) == "73":
       sDes = sDes + " - Card Recognition Data tag"
    n = n + 2
          
    #0x62 = length
    sLen = str_mid(sData, n, 2)
    sDes = sDes + "\n" + bytes_LengthDescription(sLen)
    n = n + 2
    
    while n < len(sData):
          
          sTag = str_mid(sData, n, 2)
          n = n + 2
      
          sLen = str_mid(sData, n, 2)
          nLen = int(bytes_HexaToNro(sLen))
          n = n + 2
      
          sValue = str_mid(sData, n, int(nLen * 2))
          
          sDes = sDes + "\nTag: 0x" + sTag
          n = n + int(nLen * 2)
          
          if sTag == "06":
             sDes = sDes + " (OID tag - OID for Card Recognition Data, also identifies GlobalPlatform as the Tag Allocation Authority)"
          
          if str_left(sTag, 1) == "6":
             sDes = sDes + " (Application tag " + str_right(sTag, 1)
             
             if sTag == "65":
                sDes = sDes + " - Card configuration details"
             if sTag == "66":
                sDes = sDes + " - Card / chip details"
             if sTag == "67":
                sDes = sDes + " - Issuer Security Domain Trust Point certificate information"
             if sTag == "68":
                sDes = sDes + " - Issuer Security Domain certificate information"
                
             sDes = sDes + ")"

          sDes = sDes + " - " + bytes_LengthDescription(sLen)
          sDes = sDes + " - Value: 0x" + str_AddSpaceHexa(sValue)
          
          if sTag == "60" and len(sValue) >= 4:
             # Global Platform Version
             sDes = sDes + " - Global Platform Version: 0x" + str_AddSpaceHexa(str_right(sValue, 4)) + " (in decimal = " + bytes_HexaToNro(str_left(str_right(sValue, 4),2)) + "." + bytes_HexaToNro(str_right(sValue, 2)) + ")"

          if sTag == "64" and len(sValue) >= 4:
             # Global Platform SCPXX
             sDes = sDes + " - SCP" + str_left(str_right(sValue, 4),2) + " (Secure Channel Protocol Option): 0x" + str_right(sValue, 2)
              
    
    sCardRecognitionData = sDes
    
    return sCardRecognitionData

# simcard_GlobalPlatformGetStatus_ApplicationData ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetStatus_ApplicationData(sData):

    sData = str_SpacesOut(sData)

    #SMS Data: 0x02 71 00 00 23 0A 00 00 00 00 00 00 00 01 00 00 02 90 00 E3 13 4F 08 A0 00 00 01 51 00 00 00 9F 70 01 0F C5 03 9A FD 80
    
    #print("simcard_GlobalPlatformGetStatus_ApplicationData - sData = " + str(sData))
    
    sResponse = ""
    
    tlv = []
    tlv_data = []
    tAIDsInSIM = []

    # Standard Global Platform 2.3
    # Card Data tag = 0xE3
    # Global Platform standard: Table 11-36: GlobalPlatform Application Data (TLV)
    
    n = 0
    sDes = "\n\nData according to standard Global Platform - Table 11-36: GlobalPlatform Application Data (TLV)"
    
    while n < len(sData):
          
          sTag = str_mid(sData, n, 2)

          if str_left(sTag,2) == "E3":
   
             sDes = sDes + "\n\nTag: 0x"
             sDes = sDes + sTag + " (GlobalPlatform Registry related data)"
             n = n + 2
             sLen = str_mid(sData, n, 2)
             nLen = int(bytes_HexaToNro(sLen))
             sValue = str_mid(sData, n, int(nLen * 2))
   
             sDes = sDes + " - " + bytes_LengthDescription(sLen)
             sDes = sDes + " - Value: 0x" + str_AddSpaceHexa(sValue)
   
             n = n + 2
                       
             sTag = str_mid(sData, n, 2)

          sTagDes = "Not defined in standard"
          if sTag == "4F":
             #sDes = sDes + "\n"
             sTagDes = "AID"
          if sTag == "9F":
             sTagDes = "Life Cycle State"
             sTag = sTag + "70"
             #if str_right(str_SpacesOut(sDes), 2) != "70":
             #   sDes = sDes + " 70"
             n = n + 2
          if sTag == "C5":
             sTagDes = "Privileges"
          if sTag == "CF":
             sTagDes = "First Implicit Selection Parameter"
          if sTag == "C4":
             sTagDes = "Application Executable Load File AID"
          if sTag == "CC":
             sTagDes = "Associated Security Domain AID"
          if sTag == "CE":
             sTagDes = "Executable Load File Version Number"
          if sTag == "84":
             sTagDes = "Executable Module AID"

          sDes = sDes + "\nTag: 0x"
          sDes = sDes + str_SpaceHexa(sTag)
          sDes = sDes + " (" + sTagDes + " Tag)"
          n = n + 2
      
          sLen = str_mid(sData, n, 2)
          nLen = int(bytes_HexaToNro(sLen))
          n = n + 2
      
          sValue = str_mid(sData, n, int(nLen * 2))
          n = n + int(nLen * 2)
    
          sLenDes = bytes_LengthDescription(sLen)
          if sLenDes != "":
             sDes = sDes + " - " + sLenDes
          
          sValue = str_TrimCleanSpaces(sValue)
          if len(sValue) > 0:
             sDes = sDes + " - Value: 0x" + str_AddSpaceHexa(sValue)
          
             if sTag == "4F" or sTag == "84" or sTag == "C4" or sTag == "CC":

                if sTag == "84" and len(tAIDsInSIM) > 0:
                   tAIDsInSIM[len(tAIDsInSIM)-1] = tAIDsInSIM[len(tAIDsInSIM)-1] + sSimcard_SeparaAPDUForLastAPDUs_Visible + "Executable Module (Instance) AID: 0x" + str_SpaceHexa(sValue)

                if sTag == "C4" and len(tAIDsInSIM) > 0:
                   tAIDsInSIM[len(tAIDsInSIM)-1] = tAIDsInSIM[len(tAIDsInSIM)-1] + sSimcard_SeparaAPDUForLastAPDUs_Visible + "Application Executable Load File AID (Package) AID: 0x" + str_SpaceHexa(sValue)

                if sTag == "CC" and len(tAIDsInSIM) > 0:
                   tAIDsInSIM[len(tAIDsInSIM)-1] = tAIDsInSIM[len(tAIDsInSIM)-1] + sSimcard_SeparaAPDUForLastAPDUs_Visible + "Associated Security Domain AID (Instance) AID: 0x" + str_SpaceHexa(sValue)

                if not sValue in str(tAIDsInSIM):
                   tAIDsInSIM.append(sValue)

                #print("simcard_GlobalPlatformGetStatus_ApplicationData - sValue = " + str(sValue))
             
             if not (sTag == "4F" or sTag == "C4" or sTag == "CC" or sTag == "CE" or sTag == "84"):
                sCodingDes = simcard_GlobalPlatformGetStatus_ApplicationData_CodingDes(sTag, sValue)
                if sCodingDes != "":
                   sDes = sDes + " - " + sCodingDes
                   
                   if len(tAIDsInSIM) > 0:
                      tAIDsInSIM[len(tAIDsInSIM)-1] = tAIDsInSIM[len(tAIDsInSIM)-1] + sSimcard_SeparaAPDUForLastAPDUs_Visible + sCodingDes

             sValueLeft = str_left(sValue, 2)
             if sValueLeft == "9F" or sValueLeft == "C5" or sValueLeft == "CC" or sValueLeft == "03" or sValueLeft == "48" or sValueLeft == "05":
                #log_writePrintOnlyDebug("\nsimcard_GlobalPlatformGetStatus_ApplicationData - BEFORE sValue from n + 6 = " + str_mid(sData, n, 6))
                n = n - int(nLen * 2)
                #log_writePrintOnlyDebug("\nsimcard_GlobalPlatformGetStatus_ApplicationData - sValue = " + str(sValue) + " - n = " + str(n) + " - sData = " + str(sData))
                #log_writePrintOnlyDebug("\nsimcard_GlobalPlatformGetStatus_ApplicationData - AFTER 	sValue from n + 6 = " + str_mid(sData, n, 6))
          else:
              n = n + 2      
          
    sResponse = sDes

    #print("simcard_GlobalPlatformGetStatus_ApplicationData - sResponse = " + str(sResponse))
    #print("\nsimcard_GlobalPlatformGetStatus_ApplicationData - tAIDsInSIM = " + str(tAIDsInSIM))

    return sResponse, tAIDsInSIM

# simcard_GlobalPlatformGetStatus_ApplicationData_CodingDes ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetStatus_ApplicationData_CodingDes(sTag, sVal):
    
    sTag = str_SpacesOut(sTag)
    sVal = str_SpacesOut(sVal)
    sSepara = " - "
    sDes = ""
    tDes = []
    
    if sTag != "" and sVal != "":
       
       if sTag == "9F" or sTag == "9F70":
          #Life Cycle State Coding
          sBits = bytes_fBinaryByHex(sVal)
          if sBits == "00000001":
             sDes = "LOADED"
          if sBits == "00000011":
             sDes = "INSTALLED"
          if sBits == "00000111":
             sDes = "SELECTABLE"
          if sBits == "00001111":
             sDes = "PERSONALIZED"
          if sBits == "01111111":
             sDes = "CARD_LOCKED"
          if sBits == "11111111":
             sDes = "LOCKED"
          sDes = "Life Cycle State Coding: " + sDes   
             
       if sTag == "C5" and len(sVal) >= 6:
          sByte1 = str_left(sVal, 2)
          sByte2 = str_mid(sVal, 2, 2)
          sByte3 = str_mid(sVal, 4, 2)
          
          #Privileges Coding
          # Byte 1
          sBits = bytes_fBinaryByHex(sByte1)
          if str_left(sBits, 1) == "1":
             tDes.append("Security Domain [0]")
          if str_left(sBits, 2) == "11" and str_right(sBits, 1) == "0":
             tDes.append("DAP Verification [1]")
          if str_left(sBits, 1) == "1" and str_mid(sBits, 2, 1) == "1":
             tDes.append("Delegated Management [2]")
          if str_mid(sBits, 3, 1) == "1":
             tDes.append("Card Lock [3]")
          if str_mid(sBits, 4, 1) == "1":
             tDes.append("Card Terminate [4]")
          if str_mid(sBits, 5, 1) == "1":
             tDes.append("Card Reset [5]")
          if str_mid(sBits, 6, 1) == "1":
             tDes.append("CVM Management [6]")
          if str_left(sBits, 2) == "11" and str_right(sBits, 1) == "1":
             tDes.append("Mandated DAP Verification [7]")

          # Byte 2
          sBits = bytes_fBinaryByHex(sByte2)
          if str_mid(sBits, 0, 1) == "1":
             tDes.append("Trusted Path [8]")
          if str_mid(sBits, 1, 1) == "1":
             tDes.append("Authorized Management [9]")
          if str_mid(sBits, 2, 1) == "1":
             tDes.append("Token Management [10]")
          if str_mid(sBits, 3, 1) == "1":
             tDes.append("Global Delete [11]")
          if str_mid(sBits, 4, 1) == "1":
             tDes.append("Global Lock [12]")
          if str_mid(sBits, 5, 1) == "1":
             tDes.append("Global Registry [13]")
          if str_mid(sBits, 6, 1) == "1":
             tDes.append("Final Application [14]")
          if str_mid(sBits, 7, 1) == "1":
             tDes.append("Global Service [15]")
             
          # Byte 3
          sBits = bytes_fBinaryByHex(sByte3)
          if str_mid(sBits, 0, 1) == "1":
             tDes.append("Receipt Generation [16]")
          if str_mid(sBits, 1, 1) == "1":
             tDes.append("Ciphered Load File Data Block [17]")
          if str_mid(sBits, 2, 1) == "1":
             tDes.append("Contactless Activation [18]")
          if str_mid(sBits, 3, 1) == "1":
             tDes.append("Contactless Self-Activation [19]")

          if len(tDes) > 0:
             n = 0
             while n < len(tDes):
                   if str_TrimCleanSpaces(tDes[n]) != "":
                      sDes = sDes + sSepara + tDes[n]
                   n = n + 1   
             
             if str_left(sDes, len(sSepara)) == sSepara:
                sDes = "Privileges Coding: " + str_midToEnd(sDes, len(sSepara))      
          
       if sTag == "CF" and sVal != "":
          #Implicit Selection Parameter
          sBits = bytes_fBinaryByHex(sVal)
          if str_left(sBits,1) == "1":
             sDes = sDes + "Contactless I/O"
          if str_mid(sBits, 1, 1) == "1":
             sDes = sDes + "Contact I/O"
          sBits = bytes_fHexaByBinary("000" + str_midToEnd(sBits, 3))
          sDes = sDes + sSepara + "Logical channel number " + str(bytes_HexaToNro(sBits))
          
          
    return sDes

# simcard_GlobalPlatformGetData_FreeMemory_ProcessBeforeAndAfter ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetData_FreeMemory_ProcessBeforeAndAfter(sProcess, sAppInstalledBefore, sFreeNonVolatileMemoryBefore, sFreeVolatileMemoryBefore, sAppInstalledAfter, sFreeNonVolatileMemoryAfter, sFreeVolatileMemoryAfter):

    sAppInstalledBefore = str_SpacesOut(sAppInstalledBefore)
    sFreeNonVolatileMemoryBefore = str_SpacesOut(sFreeNonVolatileMemoryBefore)
    sFreeVolatileMemoryBefore = str_SpacesOut(sFreeVolatileMemoryBefore)
    
    sAppInstalledAfter = str_SpacesOut(sAppInstalledAfter)
    sFreeNonVolatileMemoryAfter = str_SpacesOut(sFreeNonVolatileMemoryAfter)
    sFreeVolatileMemoryAfter = str_SpacesOut(sFreeVolatileMemoryAfter)

    nAppInstalledBefore = int(bytes_HexaToNro(sAppInstalledBefore))
    nFreeNonVolatileMemoryBefore = int(bytes_HexaToNro(sFreeNonVolatileMemoryBefore))
    nFreeVolatileMemoryBefore = int(bytes_HexaToNro(sFreeVolatileMemoryBefore))

    nAppInstalledAfter = int(bytes_HexaToNro(sAppInstalledAfter))
    nFreeNonVolatileMemoryAfter = int(bytes_HexaToNro(sFreeNonVolatileMemoryAfter))
    nFreeVolatileMemoryAfter = int(bytes_HexaToNro(sFreeVolatileMemoryAfter))
    
    sDes = "\n"
    
    # INSTALLED APPLICATIONS
    if nAppInstalledBefore > nAppInstalledAfter:
       nAppInstalled = nAppInstalledBefore - nAppInstalledAfter
    else:
       nAppInstalled = nAppInstalledAfter - nAppInstalledBefore
    sDes = sDes + "Taking into account process '" + sProcess + "', applications processed: "
    sDes = sDes + str(nAppInstalled) + "."
    sDes = sDes + "\nBefore process '" + sProcess + "' there were = " + str(nAppInstalledBefore) + " applications." 
    sDes = sDes + "\nAfter process '" + sProcess + "' there were = " + str(nAppInstalledAfter) + " applications." 

    # FREE NON VOLATILE MEMORY
    if nFreeNonVolatileMemoryBefore > nFreeNonVolatileMemoryAfter:
       nFreeNonVolatileMemory = nFreeNonVolatileMemoryBefore - nFreeNonVolatileMemoryAfter
    else:
       nFreeNonVolatileMemory = nFreeNonVolatileMemoryAfter - nFreeNonVolatileMemoryBefore
    sDes = sDes + "\n\n'Non volatile memory' required by the applet after executing process '" + sProcess + "': "
    sDes = sDes + str_AddThousandToNumber(str(nFreeNonVolatileMemory)) + " bytes."
    sDes = sDes + "\nBefore process '" + sProcess + "' there were = " + str_AddThousandToNumber(str(nFreeNonVolatileMemoryBefore)) + " bytes." 
    sDes = sDes + "\nAfter process '" + sProcess + "' there are = " + str_AddThousandToNumber(str(nFreeNonVolatileMemoryAfter)) + " bytes." 

    # FREE NON VOLATILE MEMORY
    if nFreeVolatileMemoryBefore > nFreeVolatileMemoryAfter:
       nFreeVolatileMemory = nFreeVolatileMemoryBefore - nFreeVolatileMemoryAfter
    else:
       nFreeVolatileMemory = nFreeVolatileMemoryAfter - nFreeVolatileMemoryBefore
    sDes = sDes + "\n\n'Volatile memory' required by the applet after executing process " + sProcess + ": "
    sDes = sDes + str_AddThousandToNumber(str(nFreeVolatileMemory)) + " bytes."
    sDes = sDes + "\nBefore process '" + sProcess + "' there were = " + str_AddThousandToNumber(str(nFreeVolatileMemoryBefore)) + " bytes." 
    sDes = sDes + "\nAfter process '" + sProcess + "' there are = " + str_AddThousandToNumber(str(nFreeVolatileMemoryAfter)) + " bytes." 

    #print("simcard_GlobalPlatformGetData_FreeMemory_ProcessBeforeAndAfter - sDes = " + str(sDes))
    
    return sDes    


# simcard_GlobalPlatformGetData_FreeMemory_Des ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_GlobalPlatformGetData_FreeMemory_Des(sAppInstalled, sFreeNonVolatileMemory, sFreeVolatileMemory):

    sAppInstalled = str_SpacesOut(sAppInstalled)
    sFreeNonVolatileMemory = str_SpacesOut(sFreeNonVolatileMemory)
    sFreeVolatileMemory = str_SpacesOut(sFreeVolatileMemory)

    sDes = ""
    sDes = sDes + "\nNumber of installed application = 0x" + str_SpaceHexa(sAppInstalled) + " - " + str(bytes_HexaToNro(sAppInstalled)) + " applications"
    sDes = sDes + "\n" + "Free non volatile memory = 0x" + str_SpaceHexa(sFreeNonVolatileMemory) + " - " + str_AddThousandToNumber(str(bytes_HexaToNro(sFreeNonVolatileMemory))) + " bytes"
    sDes = sDes + "\n" + "Free volatile memory = 0x" + str_SpaceHexa(sFreeVolatileMemory) + " - " + str_AddThousandToNumber(str(bytes_HexaToNro(sFreeVolatileMemory))) + " bytes"
    
    return sDes

#simcard_AIDGetTAR --------------------------------------------------------------------------------------------------------------------------------------
def simcard_AIDGetTAR(sAID, bAddDes=True):
    sTAR = ""
    
    sAID = str_SpacesOut(sAID)
    if len(sAID) >= 30:
       
       sBytes131415 = str_mid(sAID, 24, 6)
       
       if bAddDes:
          sTAR = "TAR: 0x" + str_SpaceHexa(sBytes131415)
          sTAR = sTAR + " - ASCII: " + bytes_HexaToASCII(sBytes131415)
       else:
          sTAR = sBytes131415   
    
    return sTAR

#simcard_IfInSMS_sSimcard_SMSAnswerForSPI2Request_Pattern --------------------------------------------------------------------------------------------------------------------------------------
def simcard_IfInSMS_sSimcard_SMSAnswerForSPI2Request_Pattern(sSMS):
    bFound, sData = simcard_Get_sSimcard_SMSAnswerForSPI2Request_Pattern(sSMS)
    return bFound

#simcard_Get_sSimcard_SMSAnswerForSPI2Request_Pattern --------------------------------------------------------------------------------------------------------------------------------------
def simcard_Get_sSimcard_SMSAnswerForSPI2Request_Pattern(sSMS):
    
    sSMS = str_SpacesOut(sSMS)
    bFound = False

    #print("simcard_Get_sSimcard_SMSAnswerForSPI2Request_Pattern - sSMS = " + str(sSMS))
    
    sData, sFoundUDH = simcard_APDU_Get3GPP23040_Process(sSMS, False, False)

    if sData != "":    
       bFound = True

    #print("simcard_Get_sSimcard_SMSAnswerForSPI2Request_Pattern - sData = " + str(sData) + " - sFoundUDH = " + str(sFoundUDH) + " - bFound = " + str(bFound))
 
    return bFound, sData
    
#simcard_GetStatus_AppletsFound_Des --------------------------------------------------------------------------------------------------------------------------------------
def simcard_GetStatus_AppletsFound_Des(tAIDst, tAIDsToSearch):

    sDes = ""
    sDesAIDsFound = ""
    
    if len(tAIDst) > 0:
       sDes = sDes + "Global Platform Get Status - Total applets found: " + str(len(tAIDst))
       i = 0
       while i < len(tAIDst):
       
             sAID = tAIDst[i]
             sAIDType = ""
             sAIDInstance = ""
             if sSimcard_SeparaAPDUForLastAPDUs_Visible in sAID:
                sAID = str_SpacesOut(str_getSubStringFromOcur(tAIDst[i], sSimcard_SeparaAPDUForLastAPDUs_Visible, 0))
                sAIDType = str_getSubStringFromOcur(tAIDst[i], sSimcard_SeparaAPDUForLastAPDUs_Visible, 1)
                sAIDInstance = str_getSubStringFromOcur(tAIDst[i], sSimcard_SeparaAPDUForLastAPDUs_Visible, 2)
                
             sDes = sDes + "\n[" + str(str_formatNro(i,3)) + "] AID: 0x" + str_SpaceHexa(str(sAID))

             # ADD TAR Description
             sTAR = simcard_AIDGetTAR(sAID, True)
             if str_TrimCleanSpaces(sTAR) != "":
                sDes = sDes + " - " + sTAR
                
             if str_TrimCleanSpaces(sAIDType) != "":
                sDes = sDes + " - " + sAIDType

             # SEARCH FOUND AIDs IN AIDs to SEARCH FOR
             sAIDsToSearchDes = ""    
             j = 0
             while j < len(tAIDsToSearch):
                   sAIDsToSearch = str_SpacesOut(str_getSubStringFromOcur(tAIDsToSearch[j], sSimcard_SeparaAPDUForLastAPDUs_Visible, 0))
                   sAIDsToSearchDes = str_getSubStringFromOcur(tAIDsToSearch[j], sSimcard_SeparaAPDUForLastAPDUs_Visible, 1)

                   #log_writePrintOnlyInfo("\ntAIDsToSearch [" + str(j) + "]: sAIDsToSearch - " + str(sAIDsToSearch) + " - sAIDsToSearchDes = " + str(sAIDsToSearchDes))
                   #log_writePrintOnlyWarning("\tAIDst [" + str(i) + "]: tAIDst - " + str(tAIDst[i]))
                   
                   if str(str_SpacesOut(sAIDsToSearch)) == str(str_SpacesOut(sAID)):
                      #print("simcard_GlobalPlatformGetStatus - sAIDsToSearch = " + str(sAIDsToSearch))
                      j = len(tAIDsToSearch)
                   else:
                      sAIDsToSearchDes = ""    
                      
                   j = j + 1
                         
             if str_TrimCleanSpaces(sAIDsToSearchDes) != "":      
                sDes = sDes + " - " + sAIDsToSearchDes
                sDesAIDsFound = sDesAIDsFound + " - " + sAIDsToSearchDes

             if str_TrimCleanSpaces(sAIDInstance) != "":
                sDes = sDes + " - " + sAIDInstance
                         
             i = i + 1      
    
    return sDes, sDesAIDsFound         

#simcard_TimeDelay --------------------------------------------------------------------------------------------------------------------------------------
def simcard_TimeDelay(sDes, nDelay=sSimcard_PackageBlocks_Delay):

    # GET DATETIME NOW
    sdtFormat = "%Y/%m/%d-%H:%M:%S"
    dateToday = datetime.now()    
    sdateToday = dateToday.strftime(sdtFormat)
             
    #n = 0
    #nMax = 1000000
    #while n < nMax:
    #      n = n + 1
    
    sLog = ""      
    if sDes != "":
       sLog = sLog + sDes + " - "
             
    sLog = "Time Delay: " + str(nDelay) + ". Date and Time: " + str(sdateToday) 
    log_writeWordsInColorMagenta(sLog)    

    #sys.stdout.flush()
    sleep(nDelay)
    #sys.stdout.flush()
    

#simcard_Applets_Debug --------------------------------------------------------------------------------------------------------------------------------------
def simcard_Applets_Debug(sDes, sAID, bPackage=True, sTAR=sSimcard_MSLDefTAR_RAM, sMSL=sSimcard_MSLDefMAC, sKIC=sSimcard_MSLDefKIC, sKID=sSimcard_MSLDefKID, sCounter=sSimcard_MSLDefCounter):
    sMsg = sDes + " "
    if bPackage:
       sMsg = sMsg + "package"
    else:
       sMsg = sMsg + "instance"
    sMsg = sMsg + " with AID: " + str_AddSpaceHexa(sAID) + "."
    sMsg = sMsg + "\nParameters: "
    sMsg = sMsg + "\nTAR = 0x" + str_AddSpaceHexa(sTAR)
    sMsg = sMsg + "\nMSL = 0x" + str_AddSpaceHexa(sMSL)
    sMsg = sMsg + "\nKIC = 0x" + str_AddSpaceHexa(sKIC)
    sMsg = sMsg + "\nKID = 0x" + str_AddSpaceHexa(sKID)
    sMsg = sMsg + "\nCounter = 0x" + str_AddSpaceHexa(sCounter)
    log_writePrintOnlyDebug(sMsg)
    return


# simcard_OTAForAppletLoadAndInstall ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_OTAForAppletLoadAndInstall(OTAScriptsName, sOTAScriptsAmount, sPathOut, sPackagePathFile, sAIDPackage, sAIDApplet, sAIDInstance, sInstanceParamsUICC, sInstanceParamsAPP):

    sAIDPackage = str_SpacesOut(sAIDPackage)
    sAIDApplet = str_SpacesOut(sAIDApplet)
    sAIDInstance = str_SpacesOut(sAIDInstance)
    sInstanceParamsUICC = str_SpacesOut(sInstanceParamsUICC)
    sInstanceParamsAPP = str_SpacesOut(sInstanceParamsAPP)
    
    bReturn = True
    
    if sAIDApplet=="":
       sAIDApplet = sAIDInstance
    
    if OTAScriptsName == "":
       OTAScriptsName = ota_sDef_OTAScriptsName
    if sOTAScriptsAmount == "":
       sOTAScriptsAmount = ota_sDef_OTAScriptsAmount
    
    # GET TODAY DATE   
    today = datetime.now()
    today_prn = today.strftime("%Y%m%d")
    OTAScriptsName = OTAScriptsName + ota_sDef_FileNameSepara + today_prn
    
    # -------------------------------------------------------------------------------------------------------------------------------------
    # IT IS BEING GENERATED OTA SCRIPTS FOR REMOVING THE PACKAGE AND INSTANCE
    sMsg = "Generating script for deleting package with: \nAID: " + str_SpaceHexa(sAIDPackage) 
    log_writePrintOnlyInfo(sMsg)
    sDeleteAPDUPackage = simcard_APDUForDeleteApplet(sAIDPackage, True)
    
    sMsg = "Generating script for deleting instance with: \nAID: " + str_SpaceHexa(sAIDInstance) 
    log_writePrintOnlyInfo(sMsg)
    sDeleteAPDUInstance = simcard_APDUForDeleteApplet(sAIDInstance, False)

    if sDeleteAPDUPackage == "" or sDeleteAPDUInstance == "":
       log_writePrintOnlyError("No APDU generated for deleting package and instance. APDU for deleting Package: " + str(sDeleteAPDUPackage) + " - APDU for deleting Instance: " + str(sDeleteAPDUInstance))
       return False
    
    bReturn = ota_OTAForDeletePackageAndInstance(OTAScriptsName, sPathOut, sAIDPackage, sDeleteAPDUPackage, sAIDInstance, sDeleteAPDUInstance)      
    
    # -------------------------------------------------------------------------------------------------------------------------------------
    if bReturn:   
       # IT IS BEING GENERATED OTA SCRIPTS FOR LOADING PACKAGE AND INSTALL APPLET

       lstAPDUs = []
       
       sMsg = "Started loading package with: \nAID: " + str_SpaceHexa(sAIDPackage) + "\nFile: '" + sPackagePathFile + "."
       log_writePrintOnlyInfo(sMsg)
       
       sPackagePathFile = file_fNormalPathForWindowsLinux(sPackagePathFile)
       if len(sPackagePathFile) <= 0:
          log_writePrintOnlyError("No file path and name defined for loading package with AID: " + sAIDPackage)
          return False

       sAIDPackage = str_SpacesOut(sAIDPackage)
       if len(sAIDPackage) <= 0:
          log_writePrintOnlyError("No AID defined for loading package. AID: " + sAIDPackage)
          return False 

       # PREPARE APDUs WITH PACKAGE FILE
       lstAPDUs = simcard_APDUsForLoadingAppletPackage_ByPathFile(sAIDPackage, sPackagePathFile)

       # IT IS BEING GENERATED OTA SCRIPTS FOR INSTALLING APPLET
       sMsg = "Installing Applet:"
       sMsg = sMsg + "\nPackage AID: " + str_SpaceHexa(sAIDPackage) + " - " + simcard_DescriptionLength(sAIDPackage)
       sMsg = sMsg + "\nApplet AID: " + str_SpaceHexa(sAIDApplet) + " - " + simcard_DescriptionLength(sAIDApplet)
       sMsg = sMsg + "\nInstance AID: " + str_SpaceHexa(sAIDInstance) + " - " + simcard_DescriptionLength(sAIDInstance)
       sMsg = sMsg + "\nParameters UICC: " + str_SpaceHexa(sInstanceParamsUICC) + " - " + simcard_DescriptionLength(sInstanceParamsUICC)
       sMsg = sMsg + "\nParameters Application, tag 0xC9: " + str_SpaceHexa(sInstanceParamsAPP) + " - " + simcard_DescriptionLength(sInstanceParamsAPP)
       log_writePrintOnlyInfo(sMsg)
       
       # PREPARE APDUs FOR INSTALL FOR INSTALL       
       sAPDU = simcard_APDUForInstallForInstallApplet(sAIDPackage, sAIDApplet, sAIDInstance, "", sInstanceParamsUICC, sInstanceParamsAPP)

       if sAPDU == "":
          log_writePrintOnlyError("No APDU generated for 'install for install'. AID Package: " + str(sAIDPackage) + " - AID Instance: " + str(sAIDInstance))
          return False
 
       lstAPDUs.append(sAPDU)   
       bReturn = ota_OTAForLoadPackageAndInstallApplet(OTAScriptsName, sOTAScriptsAmount, sPathOut, sAIDPackage, sAIDInstance, lstAPDUs)      
       
       
    return True

# simcard_Clean9000 ---------------------------------------------------------------------------------------------------------------------------------------------------------
def simcard_Clean9000(sResAndSW1SW2):

    sResAndSW1SW2 = str_SpacesOut(sResAndSW1SW2)
    
    if str_right(sResAndSW1SW2, len(sSimcard_9000)) == sSimcard_9000:
       sResAndSW1SW2 = str_left(sResAndSW1SW2, len(sResAndSW1SW2)-len(sSimcard_9000))
       
    return sResAndSW1SW2   

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

