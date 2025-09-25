# -*- coding: UTF-8 -*-

import sys
from str import *
from algos import *
from dt import *
from bytes import *

# loci_imei ----------------------------------------------------------------------------------------------------------
def loci_imeiFromHexa(sIMEIHex, bDes=False, bLuhnCheck=True):
    
    imei=str_SpacesOut(sIMEIHex)
    imei=imei.upper()
 
    if len(imei) != 16:
       return ""
    
    #faffffffffffff0f
    if str_mid(imei,2,4) == "FFFF":
       #WRONG IMEI
       return sIMEIHex
    
    sLog = "IMEI to be pocessed: 0x" + str_AddSpaceHexa(imei)
    
    imei = str_reverse(imei)
    
    if bDes==False and bLuhnCheck==False:
       return imei
    
    imeiForLuhn = imei[:len(imei)-1]

    sLog = sLog + "\nIMEI reversed: " + str(imei)

    #ETSI 124.008
    #Type of identity (octet 3)
    #Bits
    #3 2 1
    #0 0 1 IMSI
    #0 1 0 IMEI
    #0 1 1 IMEISV
    #1 0 0 TMSI/P-TMSI/M-TMSI
    #1 0 1 TMGI and optional MBMS Session Identity
    #0 0 0 No Identity (note 1)
    #All other values are reserved.
    #Odd/even indication (octet 3)
    #Bit
    #4
    #0 even number of identity digits and also when the TMSI/P-TMSI or TMGI
    #and optional MBMS Session Identity is used
    #1 odd number of identity digits
    sBits = bytes_fBinaryByHex(imei[0:2])
    sBits = str_left(sBits, 4)
     
    imeiForLuhn = imeiForLuhn[1:]

    Luhn = 0
    if str_IsNnro0To9FromString(imeiForLuhn) and bLuhnCheck==True:
       Luhn = algo_Luhn(imeiForLuhn)

    sIMEIt = str(imei[1:len(imei)-1]) + str(Luhn)
    if bDes==False and bLuhnCheck==True:
       return sIMEIt
    
    sBit = str_left(sBits, 1)
    sBits = str_right(sBits, 3)
    sLog = sLog + "\nType of Identity (ETSI 124.008): " + imei[0:1] + " = " + bytes_fBinaryByHex(imei[0:1]) + " - bits [321] = " + sBits + " - Type = "
    sIMEIType = "reserved"
    if sBits == "001":
       sIMEIType = "IMSI"
    if sBits == "010":
       sIMEIType = "IMEI"
    if sBits == "011":
       sIMEIType = "IMEISV"
    if sBits == "100":
       sIMEIType = "TMSI/P-TMSI/M-TMSI"
    if sBits == "101":
       sIMEIType = "TMGI and optional MBMS Session Identity"
    if sBits == "100":
       sIMEIType = "No Identity"
    sLog = sLog + sIMEIType   
    sLog = sLog + " - First Bit [4] = " + sBit + " - "
    if sBit == "0":
       sLog = sLog + "even number of identity digits and also when the TMSI/P-TMSI or TMGI and optional MBMS Session Identity is used"
    else:   
       sLog = sLog + "odd number of identity digits"

    #print("loci_imeiFromHexa - sLog=" + str(sLog))
    
    
    #if imei[0:1] == "A" or imei[0:1] == "a":
    #   imeiForLuhn = imeiForLuhn[1:]
    #   sLog = sLog + "\nType of Identity (ETSI 124.008): A - bits: 1010 - Type: IMEI"

    sLog = sLog + "\nIMEI (International Mobile Equipment Identity): " + str(imei[1:]) + " (Length: " + str(len(imei[1:])) + " digits)"
    sLog = sLog + "\nTAC (Type Allocation Code): " + str(imei[1:9])
    sLog = sLog + "\nSNR (Serial Number): " + str(imei[9:15])
    sLog = sLog + "\nCD (Check Digit): " + str(imei[len(imei)-1:])

    sLog = sLog + "\nCD (Check Digit) calculated with Luhn algoritm: " + str(Luhn) + " - data: " + str(imeiForLuhn)

    sLog = sLog + "\nIMEI to be compared to the one from Mobile with '*#06#': " + str(sIMEIt) + " - length: " + str(len(sIMEIt)) + " digits"

    #print(sLog)
    if bDes:
       return sLog
    else:
       return sIMEIt
   

# loci_imei ----------------------------------------------------------------------------------------------------------
def loci_lociFromHexa(sLOCIHex, bDes=False):

    loci=str_SpacesOut(sLOCIHex)
    loci=loci.upper()

    sLog = "LOCI to be processed: 0x" + str_AddSpaceHexa(loci)

    loci3Bytes = loci[0:6]
    #print(loci3Bytes)
    loci = str_reverse(loci3Bytes) + loci[6:]
    #print(loci)

    sLog = sLog + "\nLOCI prepared: " + str(loci) + " (Length: " + str(len(loci)) + " hexadecimal characters - " + str(len(loci)/2) + " bytes)"

    mcc=loci[0:4]
    mnc=loci[4:6]
    lac=loci[6:10]
    cellid=loci[10:14]
    subcellid=""
    if len(loci) > 14:
       subcellid=loci[14:]

    if mcc[len(mcc)-1:]!="F":
       mnc+=loci[len(mcc)-1:len(mcc)]
   
    mcc=mcc[0:len(mcc)-1]
   
    sLog = sLog + "\nMobile Country Code (MCC): " + str(mcc)
    sLog = sLog + "\nMobile Network Code (MNC): " + str(mnc)
    sLog = sLog + "\nLocation Area (LAC): " + str(lac) + " - Decimal: " + str(int(lac, 16))
    sLog = sLog + "\nCell ID: " + str(cellid)
    sLog = sLog + "\nSubcell ID: " + str(subcellid)

    #print("Right: " + str_right(subcellid,1))
    #print("Left: " + str_left(subcellid,1))

    if subcellid!="":
       sF="F"
       #print(str_mid(subcellid, 3, 1))
       if str_right(subcellid,1)==sF:
          #print(subcellid)   
          subcellid = str_RemoveLastPattern(subcellid, sF)
      
       #print(subcellid)   
       cell = cellid + subcellid   
    else:
       cell = cellid

    if (len(cell) % 2) != 0:
       cell = "0" + cell
       
    nCellID = int(cell, 16)
    sLog = sLog + "\nCell ID calculated: " + str(cell) + " - Decimal: " + str(nCellID)

    neNodeB = int(nCellID) // 256
    sLog = sLog + "\neNodeB calculated by Cell ID (Cell ID " + str(nCellID) + " / 256): 0x" + str(bytes_NroToHexa(neNodeB)) + " - Decimal: " + str(neNodeB)

    if bDes:
       return sLog
    else:
       return loci
       

# loci_MCC_MNC_To_Hexa ----------------------------------------------------------------------------------------------------------
# loci_MCC_MNC_From_Hexa ----------------------------------------------------------------------------------------------------------
# TESTING:
#sReturn = loci_MCC_MNC_To_Hexa("722", "310")
#print("loci_MCC_MNC_To_Hexa: " + sReturn)
#sReturn = loci_MCC_MNC_From_Hexa(sReturn)
#print("loci_MCC_MNC_From_Hexa: MCC=" + sReturn[0] + " - MNC=" + sReturn[1])
#sReturn = loci_MCC_MNC_To_Hexa("722", "40")
#print("loci_MCC_MNC_To_Hexa: " + sReturn)
#sReturn = loci_MCC_MNC_From_Hexa(sReturn)
#print("loci_MCC_MNC_From_Hexa: MCC=" + sReturn[0] + " - MNC=" + sReturn[1])
   
# loci_MCC_MNC_To_Hexa ----------------------------------------------------------------------------------------------------------
def loci_MCC_MNC_To_Hexa(sMCC, sMNC):
    
    nLen = 3
    
    # Example: MCC=722 MNC=310
    
    sMCC = str_SpacesOut(sMCC)
    sMNC = str_SpacesOut(sMNC)
    
    if sMCC=="":
       sMCC = str_RepeatString(nLen,"0")
    if sMNC=="":
       sMNC = str_RepeatString(nLen,"0")
    
    if len(sMCC)>=nLen:
       sMCC = str_left(sMCC, nLen)
    else:
       sMCC = str_RepeatString(nLen - len(sMCC),"0") + sMCC

    #1st Byte     
    sReturn = str_mid(sMCC, 1, 1)
    sReturn = sReturn + str_mid(sMCC, 0, 1)
    
    #2nd Byte     
    if len(sMNC)<=(nLen-1):
       sReturn = sReturn + "F"
    if len(sMNC)>=nLen:
       sMNC = str_left(sMNC, nLen)
       sReturn = sReturn + str_mid(sMNC, 2, 1)

    sReturn = sReturn + str_mid(sMCC, 2, 1)

    #3rd Byte     
    if len(sMNC)<(nLen-1):
       sMNC = str_RepeatString(nLen - len(sMNC),"0") + sMNC
       
    sReturn = sReturn + str_mid(sMNC, 1, 1)
    sReturn = sReturn + str_mid(sMNC, 0, 1)
    
    return sReturn
         
# loci_MCC_MNC_From_Hexa ----------------------------------------------------------------------------------------------------------
def loci_MCC_MNC_From_Hexa(sMCCMNCHexa):
    
    nLen = 6
    
    # Example:270213 => MCC=722 MNC=310
    
    sMCCMNCHexa = str_SpacesOut(sMCCMNCHexa)
    
    if sMCCMNCHexa=="":
       return "", ""

    if len(sMCCMNCHexa)!=nLen:
       return "", ""

    sMCC = str_mid(sMCCMNCHexa, 1, 1)
    sMCC = sMCC + str_mid(sMCCMNCHexa, 0, 1)
    sMCC = sMCC + str_mid(sMCCMNCHexa, 3, 1)
    
    sMNC = str_mid(sMCCMNCHexa, 5, 1)
    sMNC = sMNC + str_mid(sMCCMNCHexa, 4, 1)
    if str_mid(sMCCMNCHexa, 2, 1) == "F":
       sMNC = "0" + sMNC
    else:
       sMNC = sMNC + str_mid(sMCCMNCHexa, 2, 1)
              
    return sMCC, sMNC
    
# fPLociGetDateTimePreparedForSIM ---------------------------------------------------------------------------------------------------------------------------------------------------------
def fPLociGetDateTimePreparedForSIM():

    sDateTime = ""
    
    # GET DATETIME NOW
    sdtFormat = "%Y/%m/%d-%H:%M:%S"
    datet = datetime.now()    
    sdatet = str(datet.strftime(sdtFormat))
    #sdatet: 2024/11/22-14:51:30
    #print("sdatet: " + sdatet)
    
    #GET YEAR BUT TURNED
    n = 3
    sDateTime = str_mid(sdatet,n,1)
    sDateTime = sDateTime + str_mid(sdatet,n-1,1)
    
    #GET MONTH BUT TURNED
    n = n + 3
    sDateTime = sDateTime + str_mid(sdatet,n,1)
    sDateTime = sDateTime + str_mid(sdatet,n-1,1)
    
    #GET DAY BUT TURNED
    n = n + 3
    sDateTime = sDateTime + str_mid(sdatet,n,1)
    sDateTime = sDateTime + str_mid(sdatet,n-1,1)
    
    #GET HOUR BUT TURNED
    n = n + 3
    sDateTime = sDateTime + str_mid(sdatet,n,1)
    sDateTime = sDateTime + str_mid(sdatet,n-1,1)
    
    #GET MINUTES BUT TURNED
    n = n + 3
    sDateTime = sDateTime + str_mid(sdatet,n,1)
    sDateTime = sDateTime + str_mid(sdatet,n-1,1)
    
    #GET SECONDS BUT TURNED
    n = n + 3
    sDateTime = sDateTime + str_mid(sdatet,n,1)
    sDateTime = sDateTime + str_mid(sdatet,n-1,1)
    
    sDateTime = str_left(sDateTime, 12)

    #ADDED TIME STAMP
    tz = str(dt_getCurrentTimeZone())
    #print("Current time zone: " + str(tz))
    sTZ = str(fPLociTimeZoneForSIM(tz))
    #print("fSIMTimeZoneForSIM: " + sTZ)
    #print("fSIMTimeZoneFromSIM: " + str(fPLociTimeZoneFromSIM(sTZ)))

    if sTZ != "":
       sDateTime = sDateTime + sTZ
    else:
       sDateTime = sDateTime + "FF"

    return sDateTime

# fPLociGetDateTimeFromSIM ---------------------------------------------------------------------------------------------------------------------------------------------------------
def fPLociGetDateTimeFromSIM(sHexa):

    sHexa = str_SpacesOut(sHexa)
    if len(sHexa) < 14:
       return "Wrong data for processing Date/Time: 0x" + sHexa
       
    sDateTime = ""

    n = 0
    #GET YEAR BUT TURNED
    sTemp = str_mid(sHexa, n, 2)
    sDateTime = sDateTime + str_right(sTemp,1)
    sDateTime = sDateTime + str_left(sTemp,1)
    sDateTime = sDateTime + "\\"
    n = n + 2
    
    #GET MONTH BUT TURNED
    sTemp = str_mid(sHexa, n, 2)
    sDateTime = sDateTime + str_right(sTemp,1)
    sDateTime = sDateTime + str_left(sTemp,1)
    sDateTime = sDateTime + "\\"
    n = n + 2
        
    #GET DAY BUT TURNED
    sTemp = str_mid(sHexa, n, 2)
    sDateTime = sDateTime + str_right(sTemp,1)
    sDateTime = sDateTime + str_left(sTemp,1)
    n = n + 2
    
    #GET HOUR BUT TURNED
    sDateTime = sDateTime + " "
    sTemp = str_mid(sHexa, n, 2)
    sDateTime = sDateTime + str_right(sTemp,1)
    sDateTime = sDateTime + str_left(sTemp,1)
    sDateTime = sDateTime + ":"
    n = n + 2

    #GET MIN BUT TURNED
    sTemp = str_mid(sHexa, n, 2)
    sDateTime = sDateTime + str_right(sTemp,1)
    sDateTime = sDateTime + str_left(sTemp,1)
    sDateTime = sDateTime + ":"
    n = n + 2
    
    #GET SEC BUT TURNED
    sTemp = str_mid(sHexa, n, 2)
    sDateTime = sDateTime + str_right(sTemp,1)
    sDateTime = sDateTime + str_left(sTemp,1)
    n = n + 2

    #GET TIME ZONE BUT TURNED
    sDateTime = sDateTime + " GMT 0x"
    sTemp = str_mid(sHexa, n, 2)
    sDateTime = sDateTime + str_right(sTemp,1)
    sDateTime = sDateTime + str_left(sTemp,1)
    sDateTime = sDateTime + "="
    if sTemp == "FF":
       sDateTime = sDateTime + "Unknown"
    else:   
       sDateTime = sDateTime + fPLociTimeZoneFromSIM(sTemp)

    #sVal = "29"
    #sTemp = fSIMTimeZoneFromSIM(sVal)
    #print("fSIMTimeZoneFromSIM = " + sVal + ": " + sTemp)
    #sTemp1 = fSIMTimeZoneForSIM(sTemp)
    #print("fSIMTimeZoneForSIM = " + sTemp + ": " + sTemp1)
    
    return sDateTime

# fPLociTimeZoneForSIM ---------------------------------------------------------------------------------------------------------------------------------------------------------
# EXAMPLE: fPLociTimeZoneForSIM("-6") => response "4A"
def fPLociTimeZoneForSIM(sTZ):

    #Example:
    #Offset in the timestamp:        4A
    #Reverse nibble it:                   A4
    #Convert to binary:                  1010 0100
    #"1" equals negative:               -010 0100
    #Convert digits to decimal:      -24
    #Multiply by .25 hours:            -24 x .25 = -6 hours offset from UTC

    #Argentina = 0x29
    #92
    #1001 0010
    #first bit = 1 => negative
    #12
    #12 x 0.25 => 3

    #sVal = "-3"
    #sTemp1 = fSIMTimeZoneForSIM(sVal)
    #print("fSIMTimeZoneForSIM = " + sVal + ": " + sTemp1)
    #sVal = sTemp1
    #sTemp = fSIMTimeZoneFromSIM(sVal)
    #print("fSIMTimeZoneFromSIM = " + sVal + ": " + sTemp)

    if len(sTZ)==1:
       sTZ = "0" + sTZ

    if not (str_left(sTZ,1)=="-" or str_left(sTZ,1)=="+"):
       sTZ = "+" + sTZ
    else:
       if len(sTZ) == 2:
          sTZ = str_left(sTZ, 1) + "0" + str_right(sTZ, 1)   
       
    if len(sTZ) < 3:
       return "FF"
    
    sTZ = str_left(sTZ, 3)
    sSign = str_left(sTZ, 1)
    sTZ = str_right(sTZ, 2)
    nTZ = str(int(int(sTZ)//0.25))
    #print("nTZ: " + str(nTZ))
    
    sReturn = bytes_fBinaryOneByHex(str_left(nTZ, 1))
    sReturn = sReturn + bytes_fBinaryOneByHex(str_right(nTZ, 1))
    #print("sReturn: " + sReturn)
    
    if sSign == "-":
       sReturn = "1" + str_mid(sReturn, 1, 7)

    #print("sReturn: " + sReturn)
    
    sReturn = bytes_fHexaByBinary(sReturn)
    sReturn = str_right(sReturn, 1) + str_left(sReturn, 1)

    #print("sReturn: " + sReturn)
    
    return sReturn
    
# fPLociTimeZoneFromSIM ---------------------------------------------------------------------------------------------------------------------------------------------------------
# EXAMPLE: fPLociTimeZoneFromSIM("4A") => response "-6"
def fPLociTimeZoneFromSIM(sTZ):

    #Example:
    #Offset in the timestamp:        4A
    #Reverse nibble it:                   A4
    #Convert to binary:                  1010 0100
    #"1" equals negative:               -010 0100
    #Convert digits to decimal:      -24
    #Multiply by .25 hours:            -24 x .25 = -6 hours offset from UTC

    #Argentina = 0x29
    #92
    #1001 0010
    #first bit = 1 => negative
    #12
    #12 x 0.25 => 3

    if len(sTZ) < 2:
       return "FF"
    
    sTZ = str_left(sTZ, 2)
    sTZ = str_right(sTZ, 1) + str_left(sTZ, 1)
    #print("sTZ: " + sTZ)

    sSign = "+"
    if str_left(bytes_fBinaryByHex(sTZ), 1) == "1":
       sSign = "-"
    
    nTZ = bytes_fBinaryByHex(sTZ)
    #print("nTZ 1: " + nTZ)
    nTZ = bytes_fHexaByBinary("0" + str_mid(nTZ, 1, 7))
    #print("nTZ 2: " + nTZ)
        
    nTZ = str(int(int(nTZ)*0.25))
    #print("nTZ 3: " + str(nTZ))

    if len(nTZ) < 2:
       nTZ = "0" + nTZ
           
    sReturn = sSign + nTZ

    #print("sReturn: " + sReturn)
    
    return sReturn
    
# fPLociTimeZoneFromSIM ---------------------------------------------------------------------------------------------------------------------------------------------------------
def fPLociACCTECHDes(sByte):
    
    sByte = str_SpacesOut(sByte)
    
#    Access Technology:
#-------------
#ts_102223v140000p.pdf
#
#Coding:
#- '00' = GSM;
#- '01' = TIA/EIA-553 [49];
#- '02' = TIA/EIA-136-270 [25];
#- '03' = UTRAN;
#- '04' = TETRA;
#- '05' = TIA/EIA-95-B [50];
#- '06' = cdma2000 1x (TIA-2000.2 [51]);
#- '07' = cdma2000 HRPD (TIA-856 [52]);
#- '08' = E-UTRAN;
#- '09' = eHRPD [54];
#- '0A' = 3GPP NG-RAN;
#- '0B' = 3GPP Satellite NG-RAN;

    sDes = "Reserved for future use"

    if sByte == "00":
        sDes = "GSM"
    if sByte == "01":
        sDes = "TIA/EIA-553"
    if sByte == "02":
        sDes = "TIA/EIA-136-C"
    if sByte == "03":
        sDes = "UTRAN"
    if sByte == "04":
        sDes = "TETRA"
    if sByte == "05":
        sDes = "TIA/EIA-95-B"
    if sByte == "06":
        sDes = "cdma2000 1x (TIA/EIA/IS-2000"
    if sByte == "07":
        sDes = "cdma2000 HRPD (TIA/EIA/IS-856 "
    if sByte == "08":
        sDes = "E-UTRAN"
    if sByte == "09":
        sDes = "eHRPD"
    if sByte == "0A":
        sDes = "3GPP NG-RAN"
    if sByte == "0B":
        sDes = "3GPP Satellite NG-RAN"
    
    sReturn = "Provide Location Information with flag 6 for 'ACCESS TECHNOLOGY': 0x" + sByte
    sReturn = sReturn + " - " + sDes
    
    return sReturn
    


# --------------------------------------------------------------------------------------------------------------------------------------------------------
