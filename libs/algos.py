# -*- coding: UTF-8 -*-
import sys
global str
from str import *
from pyDes import *
from bytes import *

# get library from: pip install pycryptodome 
# https://onboardbase.com/blog/aes-encryption-decryption
#COMENTED SO THAT EXE FILE CAN BE GENERATED
#from Crypto.Cipher import AES
#from Crypto.Random import get_random_bytes

import binascii
import os
import base64

# algo_Luhn ----------------------------------------------------------------------------------------------------------------------
def algo_Luhn(data):
    
    data = str_TrimCleanSpaces(data)
    #print("Data for Luhn: " + str(data))
    if str_IsNnro0To9FromString(data) == False:
       return 0
       
    nLen = len(data) - 1
    i = nLen
    m = 0
    while i >= 0:
          c = data[i:i+1]
          n = (int(c) * algo_LuhnMat2or1(data, i+1))
          if n>= 10:
             nS = str(n)
             n1 = int(nS[:1])
             n2 = int(nS[1:])
             n = n1 + n2
          m = m + n   
          i = i-1
    
    #print("algo_LuhnDecSup(m): " + str(algo_LuhnDecSup(m)) + ". m=" + str(m))
    
    sLuhn = algo_LuhnDecSup(m) - m
    return sLuhn
    
# algo_LuhnMat2or1 ----------------------------------------------------------------------------------------------------------------------
def algo_LuhnMat2or1(sChaine, nEnt):
    nReturn=0
    if len(sChaine) % 2 == 0:
       if nEnt % 2 == 0:
          nReturn = 2
       else:
          nReturn = 1
    else:
       if nEnt % 2 == 1:
          nReturn = 2
       else:
          nReturn = 1
    
    return nReturn

# algo_LuhnDecSup ----------------------------------------------------------------------------------------------------------------------
def algo_LuhnDecSup(nExpnum):
    nReturn = 0
    nResto = nExpnum % 10

    if nResto == 0:
       nReturn = nExpnum
    if nResto == 1:
       nReturn = nExpnum + 9
    if nResto == 2:
       nReturn = nExpnum + 8
    if nResto == 3:
       nReturn = nExpnum + 7
    if nResto == 4:
       nReturn = nExpnum + 6
    if nResto == 5:
       nReturn = nExpnum + 5
    if nResto == 6:
       nReturn = nExpnum + 4
    if nResto == 7:
       nReturn = nExpnum + 3
    if nResto == 8:
       nReturn = nExpnum + 2
    if nResto == 9:
       nReturn = nExpnum + 1
    
    return nReturn

# algo_desOutputFiles ----------------------------------------------------------------------------------------------------------------------
def algo_desOutputFiles(bEncrypt, sData, sKey):

    bDecrypt = True
    if bEncrypt:
       bDecrypt = False
    
    sReturn = ""   
    bResult, sResult = algo_des_TransportKey_EncryptDecrypt(sData, sKey, bDecrypt)
    if bResult:
       sReturn = sResult
       
    return sResult   

# algo_desAnd3desTesting ----------------------------------------------------------------------------------------------------------------------
def algo_desAnd3desTesting():
    sData = "00 11 22 33 44 55 66 77"
    sKey = "00 11 22 33 44 55 66 77"
    s = algo_desOutputFiles(True, sData, sKey)
    print("Encrypt Output Files - Data 8 bytes: " + s)
    s = algo_desOutputFiles(False, s, sKey)
    print("Decrypt Output Files - Data 8 bytes: " + s)

    sData = "00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF"
    sKey = "00 11 22 33 44 55 66 77"
    s = algo_desOutputFiles(True, sData, sKey)
    print("Encrypt Output Files - Data 16 bytes: " + s)
    s = algo_desOutputFiles(False, s, sKey)
    print("Decrypt Output Files - Data 16 bytes: " + s)

    sKey = "00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF"
    sData = "00 11 22 33 44 55 66 77"
    s = algo_3des(True, sData, sKey)
    print("Encrypt 3DES: " + s)
    s = algo_3des(False, s, sKey)
    print("Decrypt 3DES: " + s)
    exit(0)

    
# algo_des ----------------------------------------------------------------------------------------------------------------------
def algo_des(bEncrypt, sData, sKey):

    sData = str_TrimCleanSpaces(sData)
    sKey = str_TrimCleanSpaces(sKey)

    sDataBytes = bytes_HexaStrToListNumbers(sData, "")
    sKeyBytes = bytes_HexaStrToListNumbers(sKey, "")
    #print("DataBytes: " + str(sDataBytes) + " Length: " + str(len(sDataBytes))) # ensure it is byte representation
    #print("KeyBytes: " + str(sKeyBytes) + " Length: " + str(len(sKeyBytes))) # ensure it is byte representation
    
    k = des(sKeyBytes, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_NORMAL)
    if bEncrypt == True:
        d = k.encrypt(sDataBytes)
    else:    
        d = k.decrypt(sDataBytes)
    #print(k)
    #print(d)
    
    s = str(bytes_ListNumbersToHexa(d)).upper()

    if len(sData) <= 16:
       s = str_left(s, 16)

    return s
    
# algo_3des ----------------------------------------------------------------------------------------------------------------------
def algo_3des(bEncrypt, sData, sKey):

    sData = str_TrimCleanSpaces(sData)
    sKey = str_TrimCleanSpaces(sKey)

    sDataBytes = bytes_HexaStrToListNumbers(sData, "")
    sKeyBytes = bytes_HexaStrToListNumbers(sKey, "")
    #print("algo_3des - DataBytes: " + str(sDataBytes) + " Length: " + str(len(sDataBytes))) # ensure it is byte representation
    #print("algo_3des - sKey = " + str(sKey) + " - Key Length= " + str(len(sKey)) + " - KeyBytes: " + str(sKeyBytes) + " Length: " + str(len(sKeyBytes))) # ensure it is byte representation
    
    try:
        k = triple_des(sKeyBytes, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_NORMAL)
        if bEncrypt == True:
           d = k.encrypt(sDataBytes)
        else:    
           d = k.decrypt(sDataBytes)
        #print("k=" + str(k))
        #print("d=" + str(d))
    
        s = str(bytes_ListNumbersToHexa(d)).upper()

        if len(sData) <= 16:
           s = str_left(s, 16)

        #print("s=" + str(s))
    
        return s
    except Exception as e:
        sError = "algo_3des - Exception = " + str(e)
        print(sError)
        return sError
         

# algo_3desECB ----------------------------------------------------------------------------------------------------------------------
def algo_3desECB(bEncrypt, sData, sKey):

    sData = str_TrimCleanSpaces(sData)
    sKey = str_TrimCleanSpaces(sKey)

    sDataBytes = bytes_HexaStrToListNumbers(sData, "")
    sKeyBytes = bytes_HexaStrToListNumbers(sKey, "")

    try:

        k = triple_des(sKeyBytes, ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_NORMAL)
        if bEncrypt == True:
           d = k.encrypt(sDataBytes)
        else:    
           d = k.decrypt(sDataBytes)
    
        s = str(bytes_ListNumbersToHexa(d)).upper()

        if len(sData) <= 16:
           s = str_left(s, 16)

        return s
    except Exception as e:
        sError = "algo_3desECB - Exception = " + str(e)
        print(sError)
        return sError

# algo_3desCBC ----------------------------------------------------------------------------------------------------------------------
def algo_3desCBC(bEncrypt, sData, sKey):
    return algo_3des(bEncrypt, sData, Key)

# algo_aes128 ----------------------------------------------------------------------------------------------------------------------
def algo_aes(bEncrypt, sData, sKey):

    try:
        sData = str_TrimCleanSpaces(sData)
        sKey = str_TrimCleanSpaces(sKey)

        key = binascii.unhexlify(sKey)
        text = binascii.unhexlify(sData)
        #IV = os.urandom(16)
    
        #https://techtutorialsx.com/2018/04/09/python-pycrypto-using-aes-128-in-ecb-mode/ 
        mode = AES.MODE_ECB
        cipher = AES.new(key, mode)
    
        s = ""
        if bEncrypt == True:
           d = cipher.encrypt(text)
           #print(d) 
        else:
           d =  cipher.decrypt(text)
           #print(d) 
       
        s = str(bytes_ListNumbersToHexa(d)).upper()
    
        #print(s)
        return s
    except ex:
        sError = "algo_aes - Error: " + str(ex)
        print(sError)
        return sError

# algo_aesTesting ----------------------------------------------------------------------------------------------------------------------
def algo_aesTesting():
    sData = "00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF"
    sKey = "00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF"
    s = algo_aes(True, sData, sKey)
    print("Encrypt AES: " + s)
    s = algo_aes(False, s, sKey)
    print("Decrypt AES: " + s)

    exit(0)
    
# algo_DES_CBC_MAC_ISO9797M1 ----------------------------------------------------------------------------------------------------------------------
def algo_DES_CBC_MAC_ISO9797M1(bCipher, sKey8Bytes, sData):
    bResult, sResult = algo_3DES_CBC_MAC1(True, bCipher, sKey8Bytes + sKey8Bytes, sData)
    return bResult, sResult

# algo_3DES_CBC_MAC_ISO9797M1 ----------------------------------------------------------------------------------------------------------------------
def algo_3DES_CBC_MAC_ISO9797M1(bCipher, sKey16Bytes, sData):
    bResult, sResult = algo_3DES_CBC_MAC1(True, bCipher, sKey16Bytes, sData)
    return bResult, sResult
 
# algo_3DES_CBC_MAC1 ----------------------------------------------------------------------------------------------------------------------
def algo_3DES_CBC_MAC1(bCBC, bCipher, sKey16Bytes, sData):
    bReturn, sResult = algo_3DES_CBC_ECB(bCBC, bCipher, sKey16Bytes, sData)
    if len(sResult) >= 16:
        sResult = str_right(sResult, 16)
    return bReturn, sResult

# algo_3DES_CBC_ISO9797M1 ----------------------------------------------------------------------------------------------------------------------
def algo_3DES_CBC_ISO9797M1(bCipher, sKey24Bytes, sData):
    sPadding = algo_DES_Padding_ISO9797M1(sData)
    sData = sData + sPadding
    bResult, sResult = algo_3DES_CBC_ECB(True, bCipher, sKey24Bytes, sData)
    return bResult, sResult

# algo_3DES_CBC_ISO9797M2 ----------------------------------------------------------------------------------------------------------------------
def algo_3DES_CBC_ISO9797M2(bCipher, sKey24Bytes, sData):
    sPadding = algo_DES_Padding_ISO9797M2(sData)
    sData = sData + sPadding
    bResult, sResult = algo_3DES_CBC_ECB(True, bCipher, sKey24Bytes, sData)
    return bResult, sResult

# algo_DES_Padding_ISO9797M1 ----------------------------------------------------------------------------------------------------------------------
def algo_DES_Padding_ISO9797M1(sData):
    return algo_DES_Padding_ISO9797(sData, True)

# algo_DES_Padding_ISO9797M2 ----------------------------------------------------------------------------------------------------------------------
def algo_DES_Padding_ISO9797M2(sData):
    return algo_DES_Padding_ISO9797(sData, False)

# algo_DES_Padding_ISO9797 ----------------------------------------------------------------------------------------------------------------------
def algo_DES_Padding_ISO9797(sData, bM1=True):
    sReturn = ""

    #print("algo_DES_Padding_ISO9797 sData = " + str(sData) + " - bM1 = " + str(bM1))
    
    if bM1 == False:
        # PADDING FOR ISO 9797 M2
        sData = sData & "80"
        sReturn = "80"

    #print("algo_DES_Padding_ISO9797 sData = " + str(sData) + " - sReturn = " + str(sReturn))
    
    if len(sData) > 16:
        n = ((len(sData) // 2) % 8)
        
        if n == 0 and bM1:
            nPad = 0
            sPad = ""
        else:
            nPad = 8 - n
            sPad = "00"
        
    else:
        nPad = (16 - len(sData)) // 2
        sPad = "00"
    
    #print("algo_DES_Padding_ISO9797 sPad = " + str(sPad) + " - nPad = " + str(nPad))

    m = 0
    while m < nPad:
         sReturn = sReturn + sPad
         m = m + 1

    #print("algo_DES_Padding_ISO9797 sReturn = " + str(sReturn))
    return sReturn    

# algo_3DES_CBC_ECB ----------------------------------------------------------------------------------------------------------------------
def algo_3DES_CBC_ECB(bCBC, bCipher, sKey24Bytes, sData, sPadding=""):
    bReturn = True
    sResult = ""
    sError = ""

    #print("algo_3DES_CBC_ECB - sKey24Bytes = " + str(sKey24Bytes) + " - sData = " + str(sData))
    
    sKey24Bytes = str_SpacesOut(sKey24Bytes)
    sData = str_SpacesOut(sData)
    sPadding = str_SpacesOut(sPadding)
    
    if False == (len(sKey24Bytes) == 32 or len(sKey24Bytes) == 48):
        sError = "Wrong length for key: " + sKey24Bytes + " = " + str(len(sKey24Bytes)) + ". It must be 32 or 48 hexadecimal characters."
        return False, sError
    
    mvarsPadding = ""
    if sPadding != "":
       sData = sData + sPadding
       mvarsPadding = sPadding
    if len(sData) % 16 != 0 and sPadding == "":
       sData = sData + str_RepeatString(16 - (len(sData) % 16), "0")

    if bytes_IsHexaValid(sKey24Bytes)==False:
       return False, "Wrong type for key: " + sKey24Bytes + ". It must be 32 hexadecimal characters."
    if bytes_IsHexaValid(sData)==False:
       return False, "Wrong type for data: " + sData + ". It must be hexadecimal characters."
    
    #'CALCULATE
    
    sResultAuxi = ""
    sTemp = str_left(sData, 16)
    sTempA = ""
    n = 0
    bReturn = True
    while sTemp != "" and bReturn and n < len(sData):
          
          #print("\n" + str(n) + ". algo_3DES_CBC_ECB - Before algo_3des, sKey24Bytes=" + sKey24Bytes + " - Length sKey24Bytes=" + str(len(sKey24Bytes)) + " - sTemp=" + str(sTemp) + " - Length sTemp= " + str(len(sTemp)))
          
          #'CALCULATE 3DES
          sResultAuxi = algo_3des(bCipher, sTemp, sKey24Bytes)

          #print("\n" + str(n) + ".algo_3DES_CBC_ECB - After algo_3des, sKey24Bytes=" + sKey24Bytes + " - Length sKey24Bytes=" + str(len(sKey24Bytes)) + " - sTemp=" + str(sTemp) + " - Length sTemp= " + str(len(sTemp)) + " - sResultAuxi= " + str(sResultAuxi) + " - Length sResultAuxi=" + str(len(sResultAuxi)))

          if sResultAuxi=="":
             return False, "Error with algo_3des. bCipher = " + str(bCipher) + " - sKey24Bytes = " + str(sKey24Bytes) + " - sTemp = " + str(sTemp)
          
          else:
             n = n + 16
             #print(str(n) + ".algo_3DES_CBC_ECB - sTemp=" + str(sTemp) + " - len sTemp = " + str(len(sTemp)))
             if n + 16 <= len(sData):
                sTemp = str_mid(sData, n, 16)
             else:
                if len(sData) >= n:
                   sTemp = str_midToEnd(sData, n)
      
                   if len(sTemp) != 16:
                      sTemp = sTemp + str_RepeatString(16 - len(sTemp), "0")
             
             #print(str(n) + ".algo_3DES_CBC_ECB - sTemp=" + str(sTemp) + " - len sTemp = " + str(len(sTemp)))
             #print(str(n) + ".algo_3DES_CBC_ECB - algo_XORAlgorithm - sTemp=" + str(sTemp) + " - len sData = " + str(len(sData)))
                
             if bCBC:
                if bCipher:
                   #'CALCULATE XOR
                   bReturn, sTemp = algo_XORAlgorithm(sTemp, sResultAuxi)
                   if bReturn == False:
                      #print("algo_3DES_CBC_ECB - algo_XORAlgorithm=" + str(bReturn) + " - sTemp=" + str(sTemp))
                      return bReturn, sTemp
                else:
                   if n > 17:
                      #'CALCULATE XOR
                      bReturn, sResultAuxi = algo_XORAlgorithm(sTempA, sResultAuxi)
                      if bReturn == False:
                         #print("algo_3DES_CBC_ECB - algo_XORAlgorithm=" + str(bReturn) + " - sTemp=" + str(sResultAuxi))
                         return bReturn, sTemp
                      sTempA = str_mid(sData, n - 16, 16)
                   else:
                      sTempA = str_left(sData, 16)
                
                sResult = sResult + sResultAuxi
                #print("algo_3DES_CBC_ECB - sResult=" + str(sResult) + " - Len sResult=" + str(len(sResult)) + " - bCipher= " + str(bCipher) + " - n= " + str(n))
                
    #print("algo_3DES_CBC_ECB - sResult=" + str(sResult) + " - Len sResult=" + str(len(sResult)) + " - bCipher= " + str(bCipher) + " - n= " + str(n))
    
    return True, sResult
    
# algo_XORAlgorithm ----------------------------------------------------------------------------------------------------------------------
def algo_XORAlgorithm(sValue1, sValue2):
    sResult = algo_ORInclusiveExclusiveHexa(sValue1, sValue2, False)
    if sResult == "":
        return False, "Null result. Value1: " + str(sValue1) + ", Value2: " + str(sValue2)
    
    return True, sResult    

# algo_ORInclusiveExclusiveHexa ----------------------------------------------------------------------------------------------------------------------
def algo_ORInclusiveExclusiveHexa(sIn1, sIn2, bInclusive):
    return algo_ORInclusiveExclusiveHexaSub(sIn1, sIn2, False, bInclusive)

# algo_ORInclusiveExclusiveHexaSub ----------------------------------------------------------------------------------------------------------------------
def algo_ORInclusiveExclusiveHexaSub(sIn1, sIn2, bSIM, bInclusive):
    bReturn = True
    sReturn = ""
    
    sIn1 = str_SpacesOut(sIn1)
    sIn2 = str_SpacesOut(sIn2)
    
    if bytes_IsHexaValid(sIn1)==False:
       return ""
    if bytes_IsHexaValid(sIn2)==False:
       return ""
           
    sIn1 = bytes_fBinaryByHex(sIn1)
    sIn2 = bytes_fBinaryByHex(sIn2)
        
    sReturn = algo_ORInclusiveExclusiveBinarySub(sIn1, sIn2, bSIM, bInclusive)
    sReturn = bytes_fHexaByBinary(sReturn)
    
    #print("algo_ORInclusiveExclusiveHexaSub - sReturn = " + str(sReturn))
    
    return sReturn    

# algo_ORInclusiveExclusiveBinarySub ----------------------------------------------------------------------------------------------------------------------
def algo_ORInclusiveExclusiveBinarySub(sIn1, sIn2, bSIM, bInclusive):
    sReturn = ""
    bReturn = True
    sIn1 = str_SpacesOut(sIn1)
    sIn2 = str_SpacesOut(sIn2)

    #print("algo_ORInclusiveExclusiveBinarySub - sIn1=" + str(sIn1) + " - sIn2=" + str(sIn2) + "- bSIM=" + str(bSIM) + " - bInclusive=" + str(bInclusive))
    
    if bytes_IsBinaryValid(sIn1) == False:
       return ""
    if bytes_IsBinaryValid(sIn2) == False:
       return ""

    if len(sIn1) < len(sIn2):
        sIn1 = sIn1 + str_RepeatString(len(sIn2) - len(sIn1), "0")
    else:
        if len(sIn2) < len(sIn1):
            sIn2 = sIn2 + str_RepeatString(len(sIn1) - len(sIn2), "0")
    
    n = 0
    while n < len(sIn1):
          if bSIM:
             if bInclusive:
                if str_mid(sIn1, n, 1) == "1" or str_mid(sIn2, n, 1) == "1":
                   sReturn = sReturn + "1"
                else:
                    sReturn = sReturn + "0"
             else:       
                if str_mid(sIn1, n, 1) == "1" and str_mid(sIn2, n, 1) == "1":
                   sReturn = sReturn + "1"
                else:
                   sReturn = sReturn + "0"
          else:
             if str_mid(sIn1, n, 1) == str_mid(sIn2, n, 1):
                if bInclusive:
                   if str_mid(sIn1, n, 1) == "1":
                      sReturn = sReturn + "1"
                   else:
                      sReturn = sReturn + "0"
                else:
                   sReturn = sReturn + "0"
             else:
                sReturn = sReturn + "1"
          n = n + 1  

    #print("\n1.algo_ORInclusiveExclusiveBinarySub - sIn1=" + str(sIn1) + " - sIn1 Len=" + str(len(sIn1)) + " - sIn2=" + str(sIn2) + " - sIn2 Len= " + str(len(sIn2)) + " - bSIM=" + str(bSIM) + " - bInclusive=" + str(bInclusive))
    #print("\n2.algo_ORInclusiveExclusiveBinarySub sReturn= " + str(sReturn) + " - Len=" + str(len(sReturn)))
    
    return sReturn
 
# algo_Test_SMPP_MACGenration ----------------------------------------------------------------------------------------------------------------------
def algo_Test_SMPP_MACGenration(sAPDU, sMSL="02211515", sKID="33333333333333334444444444444444", sTAR="435041"):

    # TESTING:
    #sAPDU = "FB"
    #sAPDU = "F1 0B 48 65 6C 6C 6F 20 77 6F 72 6C 64"
    #sAPDU = "F2 18 68 74 74 70 73 3A 2F 2F 64 69 67 69 74 61 6C 72 65 65 66 2E 63 6F 6D 2F"
    #sReturn = algo_Test_SMPP_MACGenration(sAPDU)
    #print("algo_Test_SMPP_MACGenration - sAPDU=" + str(sAPDU) + " - sMAC=" + str(sReturn))
    #exit(0)

    sAPDU = str_SpacesOut(sAPDU)
    
    nHeaderLength = 22
    sHeaderLength = "15"
    sLen = bytes_NroToHexa((len(sAPDU)//2) + nHeaderLength)
    if len(sLen) <= 2:
       sLen = "00" + sLen
    
    sCounter = "00 00 00 00 01 00"   

    sDataForMAC = str_SpacesOut(sLen + sHeaderLength + sMSL + sTAR + sCounter + sAPDU)
    
    print("algo_Test_SMPP_MACGenration - sDataForMAC=" + str(sDataForMAC) + " - sKID=" + str(sKID) + " - sMSL=" + str(sMSL) + " - sTAR=" + str(sTAR) + " - sAPDU=" + str(sAPDU))
    bReturn, sMACPython = algo_3DES_CBC_MAC_ISO9797M1(True, sKID, sDataForMAC)
    
    print("algo_Test_SMPP_MACGenration - sDataForMAC=" + str(sDataForMAC) + " - sKID=" + str(sKID) + " - bReturn=" + str(bReturn) + " - sMACPython=" + str(sMACPython))
    
    return sMACPython

# algo_des_TransportKey_EncryptDecrypt ----------------------------------------------------------------------------------------------------------------------
# Example:
# sData = D4 E5 80 AC C6 77 98 E4 3C 84 CA 95 C1 68 F2 2A (16 bytes)
# sTK = 36 32 38 34 34 30 33 33 (8 bytes)
# Cypher: 69 55 19 E2 84 66 C1 BD 31 0A 8F F6 14 7E 40 B6 (16 bytes)
# Decypher: E0 3C D5 2E A4 00 92 D1 06 A8 27 8B 73 25 BB B3 (16 bytes)
def algo_des_TransportKey_EncryptDecrypt(sData, sTK, bDecrypt=True):
    
    sData = str_SpacesOut(sData)
    sTK = str_SpacesOut(sTK)
    
    nMultiple = 16
    
    if len(sTK) != nMultiple:
       return False, "Transport Key must be 8 bytes, " + str(nMultiple) + " characteres hexadecimal. TK received = " + sTK + " - Length = " + str(len(sTK))
    
    if (len(sData) % nMultiple) != 0:
       return False, "Data must be multiple of 8 bytes, " + str(nMultiple) + " characters hexadecimal. Data received = " + sData + " - Length = " + str(len(sData))
        
    sResult = ""
        
    n = 0
    while n < len(sData):
          sDataForDes = str_mid(sData, n, nMultiple)
          
          if bDecrypt:
             sResult = sResult + algo_des(False, sDataForDes, sTK)
          else:
             sResult = sResult + algo_des(True, sDataForDes, sTK)
          
          n = n + nMultiple
              
    return True, sResult

# algo_des_TransportKey_EncryptDecrypt ----------------------------------------------------------------------------------------------------------------------
# Example:
# sData = D4 E5 80 AC C6 77 98 E4 3C 84 CA 95 C1 68 F2 2A (16 bytes)
# sTK = 36 32 38 34 34 30 33 33 (8 bytes)
# Cypher: 69 55 19 E2 84 66 C1 BD 31 0A 8F F6 14 7E 40 B6 (16 bytes)
# Decypher: E0 3C D5 2E A4 00 92 D1 06 A8 27 8B 73 25 BB B3 (16 bytes)
def algo_des_TransportKey_EncryptDecrypt_Test():
    
    sData = "D4 E5 80 AC C6 77 98 E4 3C 84 CA 95 C1 68 F2 2A"
    sTK = "36 32 38 34 34 30 33 33"
    bResult1, sResult1 = algo_des_TransportKey_EncryptDecrypt(sData, sTK, True)
    bResult2, sResult2 = algo_des_TransportKey_EncryptDecrypt(sData, sTK, False)
    sPrint = "algo_des_TransportKey_EncryptDecrypt_Test: "
    sPrint = sPrint + "\n - sData = " + str(sData) + " length = " + str(len(str_SpacesOut(sData)))
    sPrint = sPrint + "\n - sTK = " + str(sTK) + " length = " + str(len(str_SpacesOut(sTK))) 
    sPrint = sPrint + "\n - Encrypted Result = " + str(bResult2) + " - Data = " + str(sResult2) + " length = " + str(len(sResult2)) 
    sPrint = sPrint + "\n - Decrypted Result = " + str(bResult1) + " - Data = " + str(sResult1) + " length = " + str(len(sResult1)) 
    print(sPrint)

    sData = "00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF"
    sTK = "00 11 22 33 44 55 66 77"
    bResult1, sResult1 = algo_des_TransportKey_EncryptDecrypt(sData, sTK, True)
    bResult2, sResult2 = algo_des_TransportKey_EncryptDecrypt(sData, sTK, False)
    sPrint = "algo_des_TransportKey_EncryptDecrypt_Test: "
    sPrint = sPrint + "\n - sData = " + str(sData) + " length = " + str(len(str_SpacesOut(sData)))
    sPrint = sPrint + "\n - sTK = " + str(sTK) + " length = " + str(len(str_SpacesOut(sTK))) 
    sPrint = sPrint + "\n - Encrypted Result = " + str(bResult2) + " - Data = " + str(sResult2) + " length = " + str(len(sResult2)) 
    sPrint = sPrint + "\n - Decrypted Result = " + str(bResult1) + " - Data = " + str(sResult1) + " length = " + str(len(sResult1)) 
    print(sPrint)

    sData = "00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF 00 11 22 33 44 55 66 77"
    sTK = "00 11 22 33 44 55 66 77"
    bResult1, sResult1 = algo_des_TransportKey_EncryptDecrypt(sData, sTK, True)
    bResult2, sResult2 = algo_des_TransportKey_EncryptDecrypt(sData, sTK, False)
    sPrint = "algo_des_TransportKey_EncryptDecrypt_Test: "
    sPrint = sPrint + "\n - sData = " + str(sData) + " length = " + str(len(str_SpacesOut(sData)))
    sPrint = sPrint + "\n - sTK = " + str(sTK) + " length = " + str(len(str_SpacesOut(sTK))) 
    sPrint = sPrint + "\n - Encrypted Result = " + str(bResult2) + " - Data = " + str(sResult2) + " length = " + str(len(sResult2)) 
    sPrint = sPrint + "\n - Decrypted Result = " + str(bResult1) + " - Data = " + str(sResult1) + " length = " + str(len(sResult1)) 
    print(sPrint)
    
    sData = "00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF 00 11 22 33 44 55 66 77"
    sTK = "00 11 22 33 44 55 66 77"
    sResult3 = algo_desOutputFiles(True, sData, sTK)
    sResult4 = algo_desOutputFiles(False, sData, sTK)
    sPrint = "algo_desOutputFiles: "
    sPrint = sPrint + "\n - sData = " + str(sData) + " length = " + str(len(str_SpacesOut(sData)))
    sPrint = sPrint + "\n - sTK = " + str(sTK) + " length = " + str(len(str_SpacesOut(sTK))) 
    sPrint = sPrint + "\n - Encrypted Result = " + str(sResult3) + " length = " + str(len(sResult3)) 
    sPrint = sPrint + "\n - Decrypted Result = " + str(sResult4) + " length = " + str(len(sResult4)) 
    print(sPrint)
    
    return
    
# ----------------------------------------------------------------------------------------------------------------------
    
