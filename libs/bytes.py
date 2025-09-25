# -*- coding: UTF-8 -*-
from validanro import *
from str import *
import struct
import binascii

# bytes_HexaToNro ----------------------------------------------------------------------------------------------------------------------
def bytes_HexaToNro(hexa):
    if hexa=="":
       return 0
    if not bytes_IsHexaValid(hexa):
       return 0
    ret = str(int(hexa, 16))
    return ret

# bytes_NroToHexaAdd0x ----------------------------------------------------------------------------------------------------------------------
def bytes_NroToHexaAdd0x(nro, bAdd0x):
    ret="00"
    #print("bytes_NroToHexaAdd0x: " + str(nro))
    
    if valid_nro(nro):
       ret = nro_to_hex(nro)
       #print(ret)

    ret = ret.upper()
    
    if ret[:2]=='0X':
       t = ret[2:]
       if len(t) % 2 != 0:
          t="0"+t
       if bAdd0x:   
          t = "0X" + t
       return t
    else:         
       if len(ret) % 2 != 0:
          ret = "0" + ret
       return ret

# bytes_NroToHexa ----------------------------------------------------------------------------------------------------------------------
def bytes_NroToHexa(nro):
    return bytes_NroToHexaAdd0x(nro, False)
     
# bytes_StrToHexa ----------------------------------------------------------------------------------------------------------------------
def bytes_StrToHexa(val):
    #print("bytes_StrToHexa: " + str(val))
    ascii = val
     # Initialize final String
    hexa = ""
 
    # Make a loop to iterate through
    # every character of ascii string
    for i in range(len(ascii)):
 
        # take a char from
        # position i of string
        ch = ascii[i]
 
        # cast char to integer and
        # find its ascii value
        in1 = ord(ch)
   
        # change this ascii value
        # integer to hexadecimal value
        part = hex(in1).lstrip("0x").rstrip("L")
 
        # add this hexadecimal value
        # to final string.
        hexa += part
        
    #ret = binascii.unhexlify(val)
    #return ret
    return hexa.upper()

# bytes_StrBytesToHexa ----------------------------------------------------------------------------------------------------------------------
def bytes_StrBytesToHexa(val, b2CharsTogether):
    #print("bytes_StrToHexa: " + str(val))
    ascii = val
     # Initialize final String
    hexa = ""
 
    if b2CharsTogether == True:
       if len(val) % 2 != 0:
          val = val + "0"
    
    if bytes_IsCharValidHex(val) == False:
       return ""
             
    # Make a loop to iterate through
    # every character of ascii string
    nMax = len(ascii)
    i = 0
    while i < nMax:
 
        # take a char from
        # position i of string
        if b2CharsTogether == True:
           ch = ascii[i] + ascii[i+1]
           ch = int(bytes_HexaToNro(ascii[i])) << 4
           ch = ch | int(bytes_HexaToNro(ascii[i+1]))
           i = i + 2
        else:
           ch = ascii[i]
           i = i + 1
        
        print(ch) 
   
        # integer to hexadecimal value
        part = hex(ch).lstrip("0x").rstrip("L")
        print(part) 
 
        # add this hexadecimal value
        # to final string.
        hexa += part
        
    #ret = binascii.unhexlify(val)
    #return ret
    return hexa

# bytes_HexaToASCII ----------------------------------------------------------------------------------------------------------------------
def bytes_HexaToASCII(val, bIfAllCharNotPrintableReturnNothing=False):
    #print("bytes_HexaToASCII: " + str(val))
    val = bytes_Clean0x(val)
    #print("bytes_HexaToASCII: " + str(val))
    nLen = len(val)
    sOut = ""
    i = 0
    while i < nLen:
          sChar = val[i:i+2]
          #print("bytes_HexaToASCII: " + sChar)
          if bytes_IsPrintableASCII(sChar, True):
             sOut = sOut + chr(bytes_NumberFromHex(sChar))
          else:
             sOut = sOut + str("_")   
          i = i+2
    #print(sOut)      
    
    if bIfAllCharNotPrintableReturnNothing:
       sTemp = str_Replace(sOut, "_", "")
       if sTemp == "":
          return sTemp
    
    return sOut
 
#from bytes import bytes_NroToHexa
#from bytes import bytes_StrToHexa
#from bytes import bytes_HexaToASCII
#
#print("Nro en hexa: " + str(bytes_NroToHexa(1234)))
#print("Str en hexa: " + str(bytes_StrToHexa("1234")))
#print("Str en hexa: " + str(bytes_HexaToASCII("31323334")))

# bytes_HexaStrArrayToListNumbers ----------------------------------------------------------------------------------------------------------------------
def bytes_HexaStrArrayToListNumbers(val):
    for i in range(0, len(val)):
        val[i] = str_TrimCleanSpaces(val[i])
        if bytes_IsCharValidHex(val[i]):
           val[i] = int(val[i], base=16)
        else:	
           val[i] = 0   
    return val

# bytes_HexaStrToListNumbers ----------------------------------------------------------------------------------------------------------------------
def bytes_HexaStrToListNumbers(val, sSepara):
    if sSepara == "":
       val = str_StringToList(val, 2)
    else:   
       val = val.split(sSepara)
    val = bytes_HexaStrArrayToListNumbers(val)
    return val

# bytes_IsHexaValid ----------------------------------------------------------------------------------------------------------------------
def bytes_IsHexaValid(hexa):
    #print("Hexa: " + hexa)
    if hexa is None:
       return False
    hexa = str_TrimCleanSpaces(hexa).upper()   
    
    if len(hexa) % 2 != 0:
       return False
       
    nLen = len(hexa)
    i=0
    while i < nLen:
          s = hexa[i:i+1]
          if not bytes_IsCharValidHex(s):
             return False
          i=i+1
    return True

# bytes_IsCharValidHex ----------------------------------------------------------------------------------------------------------------------
def bytes_IsCharValidHex(schar):
    schar = schar.upper()
    nLen = len(schar)
    n = 0
    for i in schar:
        #print("Hexa Char: " + i)
        if i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']:
           n = n + 1
           
    if n==nLen:
       return True
    else:
       return False                  

# bytes_ListNumbersToHexa ----------------------------------------------------------------------------------------------------------------------
def bytes_ListNumbersToHexa(lstNros):
    out = ""
    for i in lstNros:
        out = out + bytes_NroToHexa(i)
    
    out = out.upper()
    out = bytes_Clean0x(out)    
    return out
    
# bytes_Clean0x ----------------------------------------------------------------------------------------------------------------------
def bytes_Clean0x(sin):
    out = str_CleanPattern(sin, "0x")
    out = str_CleanPattern(out, "0X")
    return out
    
    
# bytes_IsPrintableASCII ----------------------------------------------------------------------------------------------------------------------
def bytes_IsPrintableASCII(val, bHexa):
    #print("bytes_IsPrintableASCII: " + str(val))
    
    if bHexa:
       
       if str_left(str(val),1) == "X" and len(val) == 2:
          val = "0" + str_right(str(val),1)

       #print("bytes_IsPrintableASCII HEXA: " + str(val))
          
       if bytes_IsCharValidHex(val):
          nVal = bytes_NumberFromHex(val)
       else:
          nVal = 0
    else:
       nVal = char(val)

    #print("bytes_IsPrintableASCII: " + str(nVal))
       
    #32 = [SPACE]
    #126 = [~]
    if nVal >= 32 and nVal <= 126:
       return True
    else:
       return False 
 
# bytes_NumberFromHex ----------------------------------------------------------------------------------------------------------------------
def bytes_NumberFromHex(sHex):
    if sHex == "":
       return 0
    #print("bytes_NumberFromHex - sHex: " + sHex)   
    if bytes_IsCharValidHex(sHex):
       return int(sHex, 16)
    else:   
       return 0

# bytes_RemoveLast2bytes ----------------------------------------------------------------------------------------------------------------------
def bytes_RemoveLast2bytes(sValue):
    sOut = str_TrimCleanSpaces(sValue)
    sOut = str_CleanEnter(sOut)
    if sOut != "":
       nLen = len(sOut)
       sOut = sOut[:nLen-4]
    return sOut

# nro_to_hex ----------------------------------------------------------------------------------------------------------------------
def nro_to_hex(nro):
    sReturn = "00"
    
    #print("nro_to_hex: " + str(nro))
    
    #FOR TESTING METHODS
    #n1 = float_to_hex(10)
    #print("n1: " + str(n1))
    #n2 = float_to_hex(32767)
    #print("n2: " + str(n2))
    #n3 = float_to_hex(65535)
    #print("n3: " + str(n3))
    #n4 = float_to_hex(100000)
    #print("n4: " + str(n4))

    #if valid_nro_float(nro):
    #   if float(nro) >= 32767:
    #      sReturn = str(float_to_hex(nro))
    #   else:
    #       sReturn = str(hex(int(nro)))
    #else:       
    #     if valid_nro_int(nro):
    #        sReturn = str(hex(int(nro)))

    #print("nro: " + str(nro))
    
    if float(nro) >= 32767:
       #print("nro_to_hex: " + str(nro))
       sReturn = str(float_to_hex(nro))
    else:
       sReturn = str(hex(int(nro)))

    
    sReturn = str_TrimCleanSpaces(sReturn)
    sReturn = sReturn.upper()
    
    if len(sReturn) < 2:
       sReturn = "0" + sReturn

    #print("nro_to_hex - sReturn: " + sReturn + ". Len: " + str(len(sReturn)) + ". Left 2: " + str_left(sReturn, 2))

    if str_left(sReturn, 2) == "0X" and len(sReturn) == 3:
       sReturn = "0X0" + str_right(sReturn, 1)

    #print("nro_to_hex - sReturn2: " + sReturn)
        
    return sReturn

# float_to_hex ----------------------------------------------------------------------------------------------------------------------
def float_to_hex(nro):
    #print(nro)
    f = float(nro)
    #print(f)
    nMod = 16
    
    #THESE OPTIONS DO NOT WORK AS EXPECTED
    #sReturn = hex(struct.unpack('<I', struct.pack('<f', f))[0])
    #sReturn = hex(struct.unpack('<Q', struct.pack('<d', f))[0])
    #sReturn = (float.hex(f)).lstrip("0x").rstrip("L")
    #sReturn = str(hex(struct.unpack('<I', struct.pack('<f', f))[0]))
    #sReturn = str('{0:x}'.format(fnro))
    
    sReturn = ""
    
    bContinue = True
    n=f
    while bContinue:
          sRest = n % nMod
          sReturn = float_to_hex_translate(sRest) + sReturn
          n=n//nMod
          #print("sReturn: " + sReturn + " - sRest: " + str(sRest) + " - n: " + str(n))
          if n<=0:
             bContinue=False
          
    
    sReturn = sReturn.upper()
    #print(sReturn)
    
    return sReturn
 
# float_to_hex_translate ----------------------------------------------------------------------------------------------------------------------
def float_to_hex_translate(sNro):
    
    sNro = str_getSubStringFromOcurFirst(str(sNro),".")
    
    sReturn = sNro
    if sNro == "10":
       sReturn = "A"
    if sNro == "11":
       sReturn = "B"
    if sNro == "12":
       sReturn = "C"
    if sNro == "13":
       sReturn = "D"
    if sNro == "14":
       sReturn = "E"
    if sNro == "15":
       sReturn = "F"
    
    return sReturn   

 
# to_ucs2 ----------------------------------------------------------------------------------------------------------------------
def to_ucs2(txt):

    sData = txt
    if bytes_IsHexaValid(txt)==True:
       sData = bytes_HexaToASCII(str_SpacesOut(txt))          

    sUCS2 = "00"
    sReturn = ""
    
    nLen = len(sData)
    n = 0
    while n < nLen:
          sByte = bytes_StrToHexa(sData[n:n+1])   
          sReturn = sReturn + sUCS2 + sByte
          n = n + 1

    sReturn = str_SpacesOut(sReturn)
    return sReturn              
       
# bytes_FromHexaToStringPRN(sIn) ----------------------------------------------------------------------------------------------------------------------
def bytes_FromHexaToStringPRN(sIn):

    sIn = str(sIn)
    #print("sIn: " + sIn)
    
    sReturn = ""
    
    nLen = len(sIn)
    n = 0
    while n < nLen:
          sByte = sIn[n:n+2]
          nByte = int(sByte, 16)
          sReturn = sReturn + nro_to_hexNo0X(nByte)
          n = n + 2

    return sReturn              

# nro_to_hexNo0X ----------------------------------------------------------------------------------------------------------------------
def nro_to_hexNo0X(nro):
    sReturn = "00"
    
    if float(nro) >= 32767:
        sReturn = str(float_to_hex(nro))
    else:
        sReturn = str(hex(nro))
    
    sReturn = str_CleanPattern(sReturn, " ")
    sReturn = sReturn.upper()
    sReturn = str_CleanPattern(sReturn, "0X")

    #print(sReturn)    
    if len(sReturn) < 2:
       sReturn = "0" + sReturn

    #print("nro_to_hex - sReturn2: " + sReturn)
        
    return sReturn
    
# bytes_isASCIIText ----------------------------------------------------------------------------------------------------------------------
def bytes_isASCIIText(text):
    result = bytes_get_UTFTextEncode(text)
    if result[0] == 'ascii':
        return True
    else: 
        return False

# bytes_isUCS2Text ----------------------------------------------------------------------------------------------------------------------
def bytes_isUCS2Text(text):
    result = bytes_get_UTFTextEncode(text)
    if result[0] == 'utf-16be':
        return True
    else: 
        return False
        
# bytes_encodeText ----------------------------------------------------------------------------------------------------------------------
def bytes_encodeText(text):
    result = bytes_get_UTFTextEncode(text)
    return result[1]

# bytes_get_UTFTextEncode ----------------------------------------------------------------------------------------------------------------------
# Return a string with encode type of a text
def bytes_get_UTFTextEncode(text):
    #print("text: " + text)
    try:
        text.encode('ascii').decode('ascii')
        bytecode = text.encode('ascii').hex()
        bytecode = str(bytecode)
        return 'ascii', bytecode
    except UnicodeEncodeError as error:
        try:
            text.encode('utf-16be').decode('utf-16be')
            bytecode = text.encode('utf-16be').hex()
            bytecode = str(bytecode)
            return 'utf-16be', bytecode
        except UnicodeEncodeError:
            return '', ''

# bytes_get_UTFByteDecode ----------------------------------------------------------------------------------------------------------------------
# Return a string with encode type of a bytecode and decoded text
def bytes_get_UTFByteDecode(textbytes):
    """
    Receives a string with bytes and returns the decoded in ASCII or UCS2\n
    Example:
    1. Input => '48 6F 6C 61 20 6D 75 6E 64 6F 20' 
    2. Output => 'Hola Mundo'
    """
    #print("textbytes: " + textbytes)
    sFormat = ''
    
    if bytes_IsHexaValid(textbytes)==False:
       return '04',textbytes

    textinBytes = bytes.fromhex(textbytes)
    
    try:
        sReturn = textinBytes.decode('ascii')
        sFormat = '04'
        return sFormat,sReturn 
    except UnicodeDecodeError as error:
        try:
            sReturn = textinBytes.decode('utf-16be')
            sFormat = '08'
            return sFormat, sReturn
        except UnicodeDecodeError:
            return '',''




# bytes_get_UTFTextEncodeToUCS2 ----------------------------------------------------------------------------------------------------------------------
def bytes_get_UTFTextEncodeToUCS2(text):
    text.encode('utf-16be').decode('utf-16be')
    bytecode = text.encode('utf-16be').hex()
    bytecode = str(bytecode)
    return bytecode

# bytes_nroToPhoneFormatForSetUpCall ----------------------------------------------------------------------------------------------------------------------
def bytes_nroToPhoneFormatForSetUpCall(text):
    return bytes_nroToPhoneFormat(text, True)

# bytes_nroToPhoneFormatForSendSMS ----------------------------------------------------------------------------------------------------------------------
def bytes_nroToPhoneFormatForSendSMS(text):
    return bytes_nroToPhoneFormat(text, False)
     
# bytes_nroToPhoneFormat ----------------------------------------------------------------------------------------------------------------------
def bytes_nroToPhoneFormat(text, bSetUpCall):
    sData = str_SpacesOut(text).upper()
    if sData == "":
       return ""
    
    sTONNPI = "81"
    if str_left(sData,1) == "+":
       # international number
       sTONNPI = "91"
       sData = str_midToEnd(sData,1)
    
    sData = str_Replace(sData,"*","A")
    sData = str_Replace(sData,"#","B")
       
    nDigits = len(sData)
    if bSetUpCall==False:
       sDigits = bytes_NroToHexa(nDigits)
       
    if (nDigits%2)!=0:
        #IMPAR - Added padding "F"
        sData = sData + "F"    
        #print("IMPAR DIGITS: " + str(nDigits))
        nDigits = nDigits + 1

    if bSetUpCall:    
       nDigits = nDigits//2
       #+1 for TON/NPI
       sDigits = bytes_NroToHexa((nDigits+1))
    
    sReturn = sDigits + sTONNPI + str_reverse(sData)
    
    return sReturn

    
# bytes_fHexa7BitsByAscii ----------------------------------------------------------------------------------------------------------------------
def bytes_fHexa7BitsByAscii(sAscii8Bits):
    sAscii8Bits = str_SpacesOut(sAscii8Bits).upper()
    if sAscii8Bits == "":
       return ""
    
    #print("sAscii8Bits: " + sAscii8Bits)
       
    sReturn = ""
    sBits = ""
    n = 0
    while n < len(sAscii8Bits):
          sBit = str_mid(sAscii8Bits, n, 1)
          #print("sBit: " + sBit)
          sBits = sBits +	 bytes_fAlphabetAsciiTo7BitsHexaInBits(sBit)
          n = n + 1
        
    #print("bytes_fHexa7BitsByAscii - sBits: " + sBits)
    
    sAuxi = ""
    n = 0
    while n < len(sBits):
          sAuxi = sAuxi + str_right(str_mid(sBits, n, 8), 7)
          n = n + 8
    
        
    sAuxi = str_AddCharToString(sAuxi, 7, " ")
    #print("bytes_fHexa7BitsByAscii - sAuxi: " + sAuxi)
    sStrAux = str_getListFromStringPattern(sAuxi, " ")
    #print(sStrAux)
    nStrAux = len(sStrAux)
    #print("bytes_fHexa7BitsByAscii - nStrAux: " + str(nStrAux))

    n = 0 
    while n < nStrAux:
          if n + 1 < nStrAux:
             sReturn = sReturn + str_right(sStrAux[n + 1], 1) + sStrAux[n]
             if n + 2 < nStrAux:
                sReturn = sReturn + str_right(sStrAux[n + 2], 2) + str_left(sStrAux[n + 1], 6)
                if n + 3 < nStrAux:
                   sReturn = sReturn + str_right(sStrAux[n + 3], 3) + str_left(sStrAux[n + 2], 5)
                   if n + 4 < nStrAux:
                      sReturn = sReturn + str_right(sStrAux[n + 4], 4) + str_left(sStrAux[n + 3], 4)
                      if n + 5 < nStrAux:
                         sReturn = sReturn + str_right(sStrAux[n + 5], 5) + str_left(sStrAux[n + 4], 3)
                         if n + 6 < nStrAux:
                            sReturn = sReturn + str_right(sStrAux[n + 6], 6) + str_left(sStrAux[n + 5], 2)
                            if n + 7 < nStrAux:
                               sReturn = sReturn + sStrAux[n + 7] + str_left(sStrAux[n + 6], 1)
                               n = n + 7
                            else:
                               sReturn = sReturn + str_RepeatString(7, "0") + str_left(sStrAux[n + 6], 1)
                               n = n + 6
                         else:
                              sReturn = sReturn + str_RepeatString(6, "0") + str_left(sStrAux[n + 5], 2)
                              n = n + 5
                      else:
                           sReturn = sReturn + str_RepeatString(5, "0") + str_left(sStrAux[n + 4], 3)
                           n = n + 4
                   else:
                        sReturn = sReturn + str_RepeatString(4, "0") + str_left(sStrAux[n + 3], 4)
                        n = n + 3
                else:
                     sReturn = sReturn + str_RepeatString(3, "0") + str_left(sStrAux[n + 2], 5)
                     n = n + 2
             else:
                  sReturn = sReturn + str_RepeatString(2, "0") + str_left(sStrAux[n + 1], 6)
                  n = n + 1
          else:
               sReturn = sReturn + "0" + sStrAux[n]
          n = n + 1
        
    sReturn = bytes_fHexaByBinary(sReturn)
    
    return sReturn       


# bytes_fHexaByBinary ----------------------------------------------------------------------------------------------------------------------
def bytes_fHexaByBinary(sBytes):
    sBytes = str_SpacesOut(sBytes).upper()
    if sBytes == "":
       return ""

    sReturn = ""
    n = 0
    while n < len(sBytes):
        sByte = str_mid(sBytes, n, 4)
        if sByte != "":
            sReturn = sReturn + bytes_fHexaFromNibleBinary(sByte)
        n = n + 4
    
    return sReturn

# bytes_fHexaFromNibleBinary ----------------------------------------------------------------------------------------------------------------------
def bytes_fHexaFromNibleBinary(sNible):
    sNible = str_SpacesOut(sNible).upper()
    if sNible == "":
       return ""
  
    sReturn = ""
    
    if len(sNible)== 4:
       
       if sNible == "0000":
          sReturn = "0"
       if sNible == "0001":
          sReturn = "1"
       if sNible == "0010":
          sReturn = "2"
       if sNible == "0011":
          sReturn = "3"
       if sNible == "0100":
          sReturn = "4"
       if sNible == "0101":
          sReturn = "5"
       if sNible == "0110":
          sReturn = "6"
       if sNible == "0111":
          sReturn = "7"
       if sNible == "1000":
          sReturn = "8"
       if sNible == "1001":
          sReturn = "9"
       if sNible == "1010":
          sReturn = "A"
       if sNible == "1011":
          sReturn = "B"
       if sNible == "1100":
          sReturn = "C"
       if sNible == "1101":
          sReturn = "D"
       if sNible == "1110":
          sReturn = "E"
       if sNible == "1111":
          sReturn = "F"
   
    return sReturn

# bytes_getNroFromASCIIChar ----------------------------------------------------------------------------------------------------------------------
def bytes_getNroFromASCIIChar(sASCIIChar):
    if sASCIIChar == "":
       return 0
       
    #print("bytes_getNroFromASCIIChar - sASCIIChar: " + str(sASCIIChar))
    nNro = ord(sASCIIChar)
    #print("bytes_getNroFromASCIIChar - nNro: " + str(nNro))
    return nNro


# bytes_fAlphabetAsciiTo7BitsHexaInBits ----------------------------------------------------------------------------------------------------------------------
def bytes_fAlphabetAsciiTo7BitsHexaInBits(sASCII):
    
    if sASCII == "":
       return ""
       
    sReturn = ""
    
    #print("bytes_fAlphabetAsciiTo7BitsHexaInBits - sASCII: " + sASCII)
    nHexa = bytes_getNroFromASCIIChar(sASCII)
    if nHexa < 0:
       sReturn = ""
    #print("bytes_fAlphabetAsciiTo7BitsHexaInBits - nHexa: " + str(nHexa))
    
    if (nHexa >= 0 and nHexa <= 9) or nHexa == 11 or nHexa == 12:
       sReturn = ""
    if nHexa == 10 or nHexa == 13:
        sReturn = bytes_fBinaryByHex(bytes_NroToHexa(nHexa))
    if nHexa == 64:
        #@
        sReturn = bytes_fBinaryByHex("00")
    if nHexa == 163:
        #�
        sReturn = bytes_fBinaryByHex("01")
    if nHexa == 36:
        #$
        sReturn = bytes_fBinaryByHex("02")
    if nHexa == 232:
        #�
        sReturn = bytes_fBinaryByHex("04")
    if nHexa == 233:
        #�
        sReturn = bytes_fBinaryByHex("05")
    if nHexa == 249:
        #�
        sReturn = bytes_fBinaryByHex("06")
    if nHexa == 236:
        #�
        sReturn = bytes_fBinaryByHex("07")
    if nHexa == 242:
        #�
        sReturn = bytes_fBinaryByHex("08")
    if nHexa == 231:
        #�
        sReturn = bytes_fBinaryByHex("09")
    if nHexa == 216:
        #�
        sReturn = bytes_fBinaryByHex("0B")
    if nHexa == 12:
        #f
        sReturn = bytes_fBinaryByHex("0C")
    if nHexa == 197:
        #�
        sReturn = bytes_fBinaryByHex("0D")
    if nHexa == 229:
        #�
        sReturn = bytes_fBinaryByHex("0E")
    if nHexa == 198:
        #�
        sReturn = bytes_fBinaryByHex("1C")
    if nHexa == 230:
        #�
        sReturn = bytes_fBinaryByHex("1D")
    if nHexa == 223:
        #�
        sReturn = bytes_fBinaryByHex("1E")
    if nHexa == 201:
        #�
        sReturn = bytes_fBinaryByHex("1F")
    if (nHexa >= 32 and nHexa <= 35) or (nHexa >= 37 and nHexa <= 63) or (nHexa >= 65 and nHexa <= 90) or (nHexa >= 97 or nHexa <= 122):
        sReturn = bytes_fBinaryByHex(bytes_NroToHexa(nHexa))
    if nHexa == 105:
        #i
        sReturn = bytes_fBinaryByHex("40")
    if nHexa == 196:
        #�
        sReturn = bytes_fBinaryByHex("5B")
    if nHexa == 214:
        #�
        sReturn = bytes_fBinaryByHex("5C")
    if nHexa == 209:
        #�
        sReturn = bytes_fBinaryByHex("5D")
    if nHexa == 220:
        #�
        sReturn = bytes_fBinaryByHex("5E")
    if nHexa == 167:
        #�
        sReturn = bytes_fBinaryByHex("5F")
    if nHexa == 191:
        sReturn = bytes_fBinaryByHex("60")
    if nHexa == 228:
        #�
        sReturn = bytes_fBinaryByHex("7B")
    if nHexa == 246:
        #�
        sReturn = bytes_fBinaryByHex("7C")
    if nHexa == 241:
        #�
        sReturn = bytes_fBinaryByHex("7D")
    if nHexa == 252:
        #�
        sReturn = bytes_fBinaryByHex("7E")
    if nHexa == 224:
        #�
        sReturn = bytes_fBinaryByHex("7F")

    #print("bytes_fAlphabetAsciiTo7BitsHexaInBits - sReturn: " + sReturn)
    
    return sReturn
        

# bytes_fBinaryOneByHex ----------------------------------------------------------------------------------------------------------------------
def bytes_fBinaryOneByHex(sNible):
    sReturn = "0000"
    
    if len(sNible) >= 1:
       sNible = str_left(sNible, 1).upper()
       if sNible == "0":
          sReturn = "0000"
       if sNible == "1":
          sReturn = "0001"
       if sNible == "2":
          sReturn = "0010"
       if sNible == "3":
          sReturn = "0011"
       if sNible == "4":
          sReturn = "0100"
       if sNible == "5":
          sReturn = "0101"
       if sNible == "6":
          sReturn = "0110"
       if sNible == "7":
          sReturn = "0111"
       if sNible == "8":
          sReturn = "1000"
       if sNible == "9":
          sReturn = "1001"
       if sNible == "A":
          sReturn = "1010"
       if sNible == "B":
          sReturn = "1011"
       if sNible == "C":
          sReturn = "1100"
       if sNible == "D":
          sReturn = "1101"
       if sNible == "E":
          sReturn = "1110"
       if sNible == "F":
          sReturn = "1111"

    return sReturn

# bytes_fBinaryByHex ----------------------------------------------------------------------------------------------------------------------
def bytes_fBinaryByHex(sInput):
    sInput = str_SpacesOut(sInput).upper()
    if sInput == "":
       return ""

    sReturn = ""

    #print("bytes_fBinaryByHex - sInput: " + sInput)
    
    n = 0
    while n < len(sInput):
          sReturn = sReturn + bytes_fBinaryOneByHex(str_mid(sInput, n, 1))
          #print("bytes_fBinaryByHex - sReturn: " + sReturn)
          n = n + 1

    return sReturn

# bytes_reverse ----------------------------------------------------------------------------------------------------------------------
def bytes_reverse(bytecode_str):
    # Split the input string into chunks of 2 characters each
    chunks = [bytecode_str[i:i + 2] for i in range(0, len(bytecode_str), 2)]

    # Reverse each chunk and join them back together
    reversed_chunks = [chunk[::-1] for chunk in chunks]
    result = ''.join(reversed_chunks)

    return result

# bytes_fHexaWithPaddingZerosToTheLeft ----------------------------------------------------------------------------------------------------------------------
def bytes_fHexaWithPaddingZerosToTheLeft(sHexa, nBytesLength):
    sReturn = ""
    
    sHexa = str_SpacesOut(sHexa)
    if sHexa != "":
        sReturn = bytes_fStrBytesLengthWithZerosToTheLeft(bytes_HexaToNro(sHexa), nBytesLength)

    return sReturn    

# bytes_fNumberToHexaWithPaddingZerosToTheLeft ----------------------------------------------------------------------------------------------------------------------
def bytes_fDesNumberToHexaWithPaddingZerosToTheLeft(nLen, nBytesLength):
    return bytes_fDesStrBytesLengthWithZerosToTheLeft(nLen, nBytesLength)

# bytes_fStrBytesLengthWithZerosToTheLeft ----------------------------------------------------------------------------------------------------------------------
def bytes_fStrBytesLengthWithZerosToTheLeft(nLen, nBytesLength):
    sLen = ""
    
    if valid_nro(nLen)==False:
       return ""

    nLen = int(nLen)
           
    if nLen >= 0 and nBytesLength > 0:
        
        #'//Because it is managed as bytes, 2 characters = 1 byte
        nBytesLength = nBytesLength * 2
            
            
        sLen = bytes_NroToHexa(nLen)
        if len(sLen) < nBytesLength:
            sLen = str_RepeatString(nBytesLength - len(sLen), "0") + sLen
    
    return sLen

# bytes_IsBinaryValid ----------------------------------------------------------------------------------------------------------------------
def bytes_IsBinaryValid(sValue):
    
    sValue = str_SpacesOut(sValue)
    
    if sValue == "":
       return False

    n = 1
    while n < len(sValue):
          sChar = str_mid(sValue, n, 1).upper()
          if False == (sChar == "0" or sChar == "1"):
             return False
          n = n + 1
          
    return True      
          

# bytes_LengthInHexaWithZerosToTheLeft_FromHexaData ----------------------------------------------------------------------------------------------------------------------
# Example: bytes_LengthInHexaWithZerosToTheLeft_FromHexaData("C4 82 01 02 03 04 05 06 07 08 09",2) 
# bytes_LengthInHexaWithZerosToTheLeft_FromHexaData - sHexaData=C4 82 01 02 03 04 05 06 07 08 09 - nBytesLength=2 => response = "000B"
def bytes_LengthInHexaWithZerosToTheLeft_FromHexaData(sHexaData, nBytesLength):

    #print("bytes_LengthInHexaWithZerosToTheLeft_FromHexaData - sHexaData=" + str(sHexaData) + " - nBytesLength=" + str(nBytesLength))
    
    sReturn = ""
    sHexaData = str_SpacesOut(sHexaData)
    if len(sHexaData) > 0:
       nLen = len(sHexaData) // 2
       sReturn = bytes_LengthInHexaWithZerosToTheLeft(nLen, nBytesLength)
       
    return sReturn

# bytes_LengthInHexaWithZerosToTheLeft_FromHexaLen ----------------------------------------------------------------------------------------------------------------------
# Example: bytes_LengthInHexaWithZerosToTheLeft_FromHexaLen(bytes_NroToHexa(nPackageDataLen),3) 
# bytes_LengthInHexaWithZerosToTheLeft_FromHexaLen => nLen=01BB - nBytesLength=3 => Response = 0001BB
def bytes_LengthInHexaWithZerosToTheLeft_FromHexaLen(sHexaLen, nBytesLength):
    
    #print("bytes_LengthInHexaWithZerosToTheLeft_FromHexaLen - sHexaLen=" + str(sHexaLen) + " - nBytesLength=" + str(nBytesLength))
    sReturn = ""
    sHexaLen = str_SpacesOut(sHexaLen)
    if len(sHexaLen) > 0:
       nLen = bytes_HexaToNro(sHexaLen)
       sReturn = bytes_LengthInHexaWithZerosToTheLeft(nLen, nBytesLength)
       
    return sReturn

# bytes_LengthInHexaWithZerosToTheLeft ----------------------------------------------------------------------------------------------------------------------
# Example: bytes_LengthInHexaWithZerosToTheLeft(nPackageDataLen,2) 
# bytes_LengthInHexaWithZerosToTheLeft => nLen=443 - nBytesLength=2 => Response = 01BB
def bytes_LengthInHexaWithZerosToTheLeft(nLen, nBytesLength):
    sLen = ""
    
    #print("bytes_LengthInHexaWithZerosToTheLeft - nLen=" + str(nLen) + " - nBytesLength=" + str(nBytesLength))
    
    nLen = int(nLen)
    nBytesLength = int(nBytesLength)
        
    if nLen >= 0 and nBytesLength > 0:
        
        #'//Because it is managed as bytes, 2 characters = 1 byte
        nBytesLength = nBytesLength * 2
            
        sLen = bytes_NroToHexa(nLen)
        if len(sLen) < nBytesLength:
            sLen = str_RepeatString(nBytesLength - len(sLen), "0") + sLen
    else:
        if nLen >= 0:
           return bytes_NroToHexa(nLen)
    
    #print("bytes_LengthInHexaWithZerosToTheLeft - sLen = " + str(sLen))
    
    return sLen    


# bytes_BinaryDataFromFileToHEXA ----------------------------------------------------------------------------------------------------------------------
def bytes_BinaryDataFromFileToHEXA(sBinary):
    sData = sBinary.hex()
    sData = str(sData).upper()
    return sData
    
# bytes_LengthDescription ------------------------------------------------------------------------------------------------------
def bytes_LengthDescription(sLenInHexa):
    sLenInHexa = str_SpacesOut(sLenInHexa)
    sReturn = ""
    if len(sLenInHexa) > 0:
       sReturn = "Length = 0x" + str_SpaceHexa(str(sLenInHexa))
       sReturn = sReturn + " - in decimal = " + str(bytes_HexaToNro(sLenInHexa))
    return sReturn

# bytes_LengthDescriptionAndData ------------------------------------------------------------------------------------------------------
def bytes_LengthDescriptionAndData(sDataBytes, bAddData=True):
    sDataBytes = str_SpacesOut(sDataBytes)
    
    sReturn = ""
    nLen = len(sDataBytes)
    
    if int(nLen) > 0:
       sLen = bytes_NroToHexa(int(nLen // 2))
    
       if bAddData:
          sReturn = "0x" + str_SpaceHexa(sDataBytes) 
          sReturn = sReturn + " - "
          
       sReturn = sReturn + bytes_LengthDescription(sLen)
       
    return sReturn
    

# bytes_str_getSubStringFromOcur ------------------------------------------------------------------------------------------------------
def bytes_str_getSubStringFromOcur(sData, sBytes, nOccurrence):

    sData = str_SpacesOut(sData)
    sBytes = str_SpacesOut(sBytes)
    sReturn = sData
    
    if len(sData) > 0 and len(sBytes) > 0:
       
       if (len(sData) % 2) == 0 and (len(sBytes) % 2) == 0:
       
           sDataPrep = " " + str_SpaceHexa(sData) + " "
           sBytesPrep = " " + str_SpaceHexa(sBytes) + " "
           
           sReturn = str_getSubStringFromOcur(sDataPrep, sBytesPrep, nOccurrence)
           sReturn = str_SpacesOut(sReturn)
           
           #print("bytes_str_getSubStringFromOcur - sDataPrep = " + str(sDataPrep) + " - sBytesPrep = " + str(sBytesPrep) + " - sReturn = " + str(sReturn))
            
    return sReturn
    
#----------------------------------------------------------------------------------------------------------------------
          