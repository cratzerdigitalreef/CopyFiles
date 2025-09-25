# -*- coding: UTF-8 -*-
import sys
global str

from validanro import *
import binascii

# ----------------------------------------------------------------------------------------------------------------------------------
# Taking into account the method: str_CleanNotPrintableASCIIChar, list of characters to be accepted:
# Example:
# 32 = [SPACE]
# 126 = [~]
# 9 = [TAB]
# 8226 => [•]
# Values must be in decimal
#if (nVal >= 32 and nVal <= 126 or (nVal == 10 or nVal == 13 or nVal == 9 or nVal == 8226)):
str_lst_NotPrintableASCIICharExceptions = [
    9            #[TAB]
    ,10          #[ENTER - 10 - Line Feed]
    ,13          #[ENTER - 13 - Carriage Return]
    ,32          #[SPACE]
    ,126         #[~]
    ,8226        #[•]
]



# str_ExitEjecution ----------------------------------------------------------------------------------------------------------------------
def str_ExitEjecution():
    exit(0)
    
# str_instr ----------------------------------------------------------------------------------------------------------------------
def str_instr(str, pattern):
    
    index = -1

    if str is None:
       return index
    if pattern is None:
       return index

    if pattern in str:
       index = str.find(pattern)
   
    return index

# str_instrBool ----------------------------------------------------------------------------------------------------------------------
def str_instrBool(str, pattern):
    
    #isInSTR = True
    #if str_instr(str,pattern) <= -1:
    #   isInSTR = False
    #return isInSTR
    
    if pattern in str:
       return True
    else:
       return False   

# str_getSubStringFrom ----------------------------------------------------------------------------------------------------------------------
def str_getSubStringFrom(str, pattern):
    #index = str_instr(str, pattern)
    #if index >= 0:
    #    return str[index+1:]
    #return str
    return str_getSubStringFromWord(str, pattern, False)

# str_getSubStringFromWord ----------------------------------------------------------------------------------------------------------------------
def str_getSubStringFromWord(str, pattern, bGetPatternToo):
    index = str_instr(str, pattern)
    sReturn = str
    if index >= 0:
       sReturn = str[index+1:]
       if len(pattern)>1:
          if bGetPatternToo:
             sReturn = str[index:]
          else:   
             sReturn = str[index+len(pattern)-1:]
           
    return sReturn

# str_getSubStringFromWithoutPattern ----------------------------------------------------------------------------------------------------------------------
def str_getSubStringFromWithoutPattern(str, pattern):
    #index = str_instr(str, pattern)
    #if index >= 0:
    #    return str[index+len(pattern)-1:]
    #return str
    return str_getSubStringFromWord(str, pattern, False)

# str_getSubStringTo ----------------------------------------------------------------------------------------------------------------------
def str_getSubStringTo(st, pattern):
    index = str_instr(st, pattern)
    if index >= 0:
        return st[0:index]
    return st
        
# str_getSubString ----------------------------------------------------------------------------------------------------------------------
def str_getSubString(st, patternFrom, patterTo):
     #print("STRING: " + st)
     #print("PATTERN FROM: " + patternFrom)
     #print("PATTERN TO: " + patterTo)
     
     stemp1 = str_getSubStringFrom(st, patternFrom)
     #print("AFTER PATTERN FROM: " + stemp1)
     sreturn = str_getSubStringTo(stemp1, patterTo)
     #print("RETURN: " + sreturn)
     
     return sreturn
     
     
# str_mid ----------------------------------------------------------------------------------------------------------------------
def str_mid(st, nFrom, nLen):
#s = s[ beginning : beginning + LENGTH]
     if st is None:
        return st

     if nFrom is None:
        nFrom = 0
     if nLen is None:
        return st
        
# start: The starting index of the substring. The character at this index is included in the substring. If start is not included, it is assumed to equal to 0.
# end: The terminating index of the substring. The character at this index is not included in the substring. If end is not included, or if the specified value exceeds the string length, it is assumed to be equal to the length of the string by default.
     
     nFrom = int(nFrom)
     nLen = int(nLen)
     #print("nFrom: " + str(nFrom) + ". nLen: " + str(nLen))
     
     return st[nFrom: nFrom + nLen]

# str_left ----------------------------------------------------------------------------------------------------------------------
def str_left(st, ln):
     if st is None:
        return st

     st = str(st)
     
     if ln > 0:
        return st[:ln] 
     else:
        return st       

# str_midToEnd ----------------------------------------------------------------------------------------------------------------------
def str_midToEnd(st, nFrom):
     if st is None:
        return st

     return st[nFrom:] 
    

# str_right ----------------------------------------------------------------------------------------------------------------------
def str_right(st, ln):
     if st is None:
        return st
     st = str(st)
     
     if int(len(st) - ln) <= 0:
        return st
        
     n=int(len(st) - ln)
     if n > 0:
        return st[n:] 
     else:
        return st       

     
# str_reverse ----------------------------------------------------------------------------------------------------------------------
def str_reverse(data):
    datarev = ""
    n=0
    while n < len(data):
          l=data[n:n+1]
          r=data[n+1:n+2]
          datarev+=r+l
          n+=2
         
    return datarev


# str_getSubStringFromOcurFirst ----------------------------------------------------------------------------------------------------------------------
def str_getSubStringFromOcurFirst(st, pattern):
    return str_getSubStringFromOcur(st, pattern, 0)

# str_getSubStringFromOcurLast ----------------------------------------------------------------------------------------------------------------------
def str_getSubStringFromOcurLast(st, pattern):
    return str_getSubStringFromOcur(st, pattern, -1)

# str_getSubStringFromOcur ----------------------------------------------------------------------------------------------------------------------
def str_getSubStringFromOcur(st, pattern, nOccurence=0):
    
    if st == "":
       return ""
    
    if pattern == "":
       return st
       
    sSplit = st.split(pattern)
    nTokens = len(sSplit)
    
    #print("str_getSubStringFromOcur - st = " + str(st) + " - pattern=" + str(pattern))
    #print("str_getSubStringFromOcur - nOccurence = " + str(nOccurence))
    #print("str_getSubStringFromOcur - sSplit = " + str(sSplit) + " - nTokens = " + str(nTokens))
    
    if nOccurence >= nTokens:
       return ""
    if nOccurence >= 0 and nOccurence < nTokens:
       return sSplit[nOccurence]
    if nOccurence == -1:
       return sSplit[nTokens-1]
    
    # FOR TESTING
    #n = 0
    #sModel = "5491130850618"
    #sW = "MSISDN"
    #sT = "'Bienvenido MSISDN. Disfruta los nuevos servicios y promociones para ti',https://www.google.com/MSISDN"
    #s = str_CountPattern(sT, sW)
    #print("str_CountPattern = " + str(s))
    #s = str_getSubStringFromOcur(sT, sW, n)
    #print("str_getSubStringFromOcur = " + str(s) + " - n = " + str(n))
    #n = n + 1
    #s = str_getSubStringFromOcur(sT, sW, n)
    #print("str_getSubStringFromOcur = " + str(s) + " - n = " + str(n))
    #s = str_getSubStringFromOcur(sT, sW, -1)
    #print("str_getSubStringFromOcur = " + str(s) + " - n = " + str(-1))

    #n = 0
    #sT = "MSISDN Bienvenido. Disfruta los nuevos servicios y promociones para ti',https://www.google.com/MSISDN TEST"
    #s = str_CountPattern(sT, sW)
    #print("str_CountPattern = " + str(s))
    #s = str_getSubStringFromOcur(sT, sW, n)
    #print("str_getSubStringFromOcur = " + str(s) + " - n = " + str(n))
    #n = n + 1
    #s = str_getSubStringFromOcur(sT, sW, n)
    #print("str_getSubStringFromOcur = " + str(s) + " - n = " + str(n))
    #s = str_getSubStringFromOcur(sT, sW, -1)
    #print("str_getSubStringFromOcur = " + str(s) + " - n = " + str(-1))
    #exit(0)

    return st   
                
# str_getSubStringFromOcurAfterFirstOnly ----------------------------------------------------------------------------------------------------------------------
def str_getSubStringFromOcurAfterFirstOnly(st, pattern, bAddPatternInResponse=False):

    if not pattern in st:
       return st
       
    sRet = str_getSubStringFromOcur(st, pattern, 0)
    #print("str_getSubStringFromOcurAfterFirstOnly - sRet = " + str(sRet))

    if bAddPatternInResponse:
       sRet = str_midToEnd(st, len(sRet))
    else:
       sRet = str_midToEnd(st, len(sRet)+len(pattern))

    #print("str_getSubStringFromOcurAfterFirstOnly - sRet = " + str(sRet))
    return sRet
    
    
# str_getSubStringFromOcurOLD ----------------------------------------------------------------------------------------------------------------------
def str_getSubStringFromOcurOLD(st, pattern, ocur):
    
    nPatterns = str_CountPattern(st, pattern)
    #print("str_getSubStringFromOcur: For String '" + st + "', amount of pattern '" + pattern + "': " + str(nPatterns) + ", ocur=" + str(ocur))

    nLen = len(st)
    nLenPat = len(pattern)
    #print("str_getSubStringFromOcur. Len st '" + st + "': " + str(nLen))
    #print("str_getSubStringFromOcur. Len pattern '" + pattern + "': " + str(nLenPat))
    
    out = ""
    n = 0
    i = 0
    j = i
    s = ""
    while i < nLen:
          s = st[i:i+nLenPat]
          if len(s)<nLenPat:
             s=st[i-1:]
             out=out[:len(out)-1]
             #print("A.str_getSubStringFromOcur. Check " + str(i) + " : " + s + " - len: " + str(len(s)))
             
          #print("B.str_getSubStringFromOcur. Check " + str(i) + " : s=" + s + " - len st: " + str(len(st)) + " - pattern= " + pattern + " - out: " + str(out) + " - len out: " + str(len(out)))
          if s==pattern and s!="":

             if n==ocur:
                #print("C.str_getSubStringFromOcur. Out: " + out + ", ocur=" + str(ocur))
                #print("D.str_getSubStringFromOcur. RETURN BEFORE out: " + out + " - i: " + str(i) 	+ " - Len out: " + str(len(out)) + " - Len pattern: " + str(len(pattern)))

                if len(pattern) > 1:
                   if (i+nLenPat)>=nLen:
                       out=st[j:i]
                       #print("E.str_getSubStringFromOcur. RETURN MIDLE out: " + out + " - j: " + str(j) + " - Len out: " + str(len(out)) + " - Len pattern-1: " + str((len(pattern)-1)))
                       
                   else:
                       #print("F.str_getSubStringFromOcur. RETURN MIDLE out: " + out + " - j: " + str(j) + " - Len out: " + str(len(out)) + " - Len pattern-1: " + str((len(pattern)-1)))
                       if ocur==0:
                          out = out[:i]   
                          #print("K.str_getSubStringFromOcur. RETURN MIDLE out: " + out + " - j: " + str(j) + " - Len out: " + str(len(out)) + " - Len pattern-1: " + str((len(pattern)-1)))
                       else:
                          if out!="":
                             out = out[:len(out)-len(pattern)+1]
                             #print("L.str_getSubStringFromOcur. RETURN MIDLE out: " + out + " - j: " + str(j) + " - Len out: " + str(len(out)) + " - Len pattern-1: " + str((len(pattern)-1)))
                       #print("F.str_getSubStringFromOcur. RETURN MIDLE out: " + out + " - j: " + str(j) + " - Len out: " + str(len(out)) + " - Len pattern-1: " + str((len(pattern)-1)))

                #print("G.str_getSubStringFromOcur. RETURN AFTER out: " + out + " - i: " + str(i) 	+ " - Len out: " + str(len(out)) + " - Len pattern: " + str(len(pattern)))
                
                return out

                
             else:
                #print("H.str_getSubStringFromOcur. Out " + str(n) + " : " + out + ", ocur=" + str(ocur))
                out = ""
                i=i+nLenPat-1
                j=i+1   
             
             n = n + 1
             
          else:
             out=st[j:i+nLenPat]
             #print("J.str_getSubStringFromOcur. Out " + str(i) + " : " + out + " - j: " + str(j) + " - i+nLenPat: " + str(i+nLenPat))
          #i = i+nLenPat
          i = i+1
    
    #print("str_getSubStringFromOcur. out: " + str(out) + " - ocur: " + str(ocur) + " - n: " + str(n))
    
    if ocur==-1 or n==ocur:
       return out
    else:
       return ""
       

# str_CountPattern ----------------------------------------------------------------------------------------------------------------------
def str_CountPattern(st, pattern):
    if st == "":
       return 0
    
    if pattern == "":
       return 0
       
    sSplit = st.split(pattern)
    nTokens = len(sSplit)
    
    return nTokens
    
# str_CountCharInStr ----------------------------------------------------------------------------------------------------------------------
def str_CountCharInStr(st, sChar):
    if st == "":
       return 0
    
    if sChar == "":
       return 0
    
    if sChar not in st:
       return 0
          
    sSplit = st.split(sChar)
    nTokens = len(sSplit)
    
    return nTokens-1

# str_CountPatternOLD ----------------------------------------------------------------------------------------------------------------------
def str_CountPatternOLD(st, pattern):
    n = 0
    st = str(st)
    pattern = str(pattern)
    nLen = len(st)
    nLenPat = len(pattern)
    #print("str_CountPattern. Len st '" + st + "': " + str(nLen))
    #print("str_CountPattern. Len pattern '" + pattern + "': " + str(nLenPat))
    
    i = 0
    while i < nLen:
          s = st[i:i+nLenPat]
          #print("str_CountPattern. Check: " + s)
          if s==pattern:
             n = n + 1
          i = i+1
           
    #print("str_CountPattern. For String '" + st + "', count of pattern '" + pattern + "': " + str(n))
    return n           


# str_getListFromStringPattern ----------------------------------------------------------------------------------------------------------------------
def str_getListFromStringPattern(st, pattern):
    out = []
    
    nPatterns = str_CountPattern(st, pattern)
    #print("str_getListFromStringPattern: For String '" + st + "', amount of pattern '" + pattern + "': " + str(nPatterns))
    
    n=0
    while n <= nPatterns:
          t = str_getSubStringFromOcur(st,pattern,n)
          #		print("str_getListFromStringPattern: " + t)
          if t!="":
             out.append(t)
          n=n+1 
          
    #print("str_getListFromStringPattern: Result=" + str(out))        
    return out

# str_RemoveLastPattern ----------------------------------------------------------------------------------------------------------------------
def str_RemoveLastPattern(st, pattern):
    nlenst = len(st)
    nlenpattern = len(pattern)
    out=st
    if st[nlenst-nlenpattern:]==pattern:
       out = st[:nlenst-nlenpattern]
    return out

# str_RemoveFirstPattern ----------------------------------------------------------------------------------------------------------------------
def str_RemoveFirstPattern(st, pattern):
    nlenst = len(st)
    nlenpattern = len(pattern)
    out=st
    if st[:nlenpattern]==pattern:
       out = st[nlenpattern:]
    return out

# str_RemoveItemFromPatternList ----------------------------------------------------------------------------------------------------------------------
def str_RemoveItemFromPatternList(st, pattern, nItem, bTransformToStr):
    outret = []
    out = str_getListFromStringPattern(st, pattern)
    print(out)
    n = 0
    for i in out:
        if n!=nItem:
           outret.append(i)
        n = n +1   
    
    if nItem==-1:
       del outret[-1]

    print(outret)       
    
    if bTransformToStr:
       out = ""
       for i in outret:
           out = out + i + pattern
       out = str_RemoveLastPattern(out, pattern)    
       return out
    else:   
       return outret

# str_ReplaceComillaDobleOld ----------------------------------------------------------------------------------------------------------------------
def str_ReplaceComillaDobleOld(st, new):
    # decimal 34 = "
    # https://ascii.cl/
    return str_Replace(st, str_GetComillaDoble(), new)

# str_ReplaceComillaDobleNew ----------------------------------------------------------------------------------------------------------------------
def str_ReplaceComillaDobleNew(st, old):
    # decimal 34 = "
    # https://ascii.cl/
    return str_Replace(st, old, str_GetComillaDoble())
    
# str_Replace ----------------------------------------------------------------------------------------------------------------------
def str_Replace(st, old, new):
    
    #CHANGED WITH METHOD REPLACE
    out = str_ReplaceWord(st, old, new)
    
    #out=""
    #for i in st:
    #    if i==old:
    #       out = out + str(new)
    #    else:
    #       out = out + i
    
    return out

# str_ReplaceWord ----------------------------------------------------------------------------------------------------------------------
def str_ReplaceWord(st, old, new):
   
    if st == "":
       return ""
    
    if old == "":
       return st
    
    sReturn = st.replace(old, new)
     
    # CHANGED WITH METHOD REPLACE   
    #sSplit = st.split(old)
    #nTokens = len(sSplit)

    #print("str_ReplaceWord - sSplit = " + str(sSplit) + " - nTokens = " + str(nTokens))
    
    #n = 0
    #sReturn = ""
    #while n < nTokens:
    #      if n+1 < nTokens:
    #         if sSplit[n] != "":
    #            sReturn = sReturn + sSplit[n]
    #         sReturn = sReturn + new 
    #      else:
    #         if sSplit[n] != "":
    #            sReturn = sReturn + sSplit[n]
    #      n = n + 1

    return sReturn    


# str_ReplaceWordOLD ----------------------------------------------------------------------------------------------------------------------
def str_ReplaceWordOLD(st, old, new):
    st_t=st
    
    out_final = st_t
    
    #print("str_ReplaceWord st: " + st)
    #print("str_ReplaceWord old: " + old)
    #print("str_ReplaceWord new: " + new)
    
    n0X = str_CountPattern(st, old)
    #print("str_ReplaceWord count: " + str(n0X))
    
    if n0X > 0:
    
       n = 0
       out = ""
       while n <= n0X:
             sBefore = str_getSubStringFromOcur(st_t, old, n)
             
             out = out + sBefore
             if n<n0X:
                out = out + new

             #print("str_ReplaceWord. " + str(n) + ": out = " + str(out) + " - len: " + str(len(out)) + " - Before: " + str(sBefore))

             n = n + 1
       
       #if str_right(st_t,len(old))==old:
       #   out = out + new   
       
       #print("str_ReplaceWord out final: " + out)
       out_final = out      

         #Testing:
    
         #n = 0
         #sModel = "5491130850618"
         #sW = "MSISDN"
         #sT = "'Bienvenido MSISDN. Disfruta los nuevos servicios y promociones para ti',https://www.google.com/MSISDN"
         #sR = str_ReplaceWord(sT, sW, sModel)
         #print("\nstr_ReplaceWord " + str(n) + ". sT: " + sT + " - sW: " + sW + " - sR: " + sR + " - SR Len: " + str(len(sR)) + "\n")
         
         #n = n + 1
         #sT = "MSISDN Bienvenido. Disfruta los nuevos servicios y promociones para ti',https://www.google.com/MSISDN"
         #sR = str_ReplaceWord(sT, sW, sModel)
         #print("\nstr_ReplaceWord " + str(n) + ". sT: " + sT + " - sW: " + sW + " - sR: " + sR + " - SR Len: " + str(len(sR)) + "\n")
         
         #n = n + 1
         #sT = "MSISDN Bienvenido. Disfruta los nuevos servicios y promociones para ti',https://www.google.com/MSISDN TEST"
         #sR = str_ReplaceWord(sT, sW, sModel)
         #print("\nstr_ReplaceWord " + str(n) + ". sT: " + sT + " - sW: " + sW + " - sR: " + sR + " - SR Len: " + str(len(sR)) + "\n")
         
         #n = n + 1
         #sT = "MSISDN Bienvenido MSISDNMSISDN. Disfruta los nuevos servicios y promociones para ti',https://www.google.com/MSISDN TEST MSISDNMSISDN"
         #sR = str_ReplaceWord(sT, sW, sModel)
         #print("\nstr_ReplaceWord " + str(n) + ". sT: " + sT + " - sW: " + sW + " - sR: " + sR + " - SR Len: " + str(len(sR)) + "\n")

         #exit(0)
             
    return out_final
    
# str_CleanWord ----------------------------------------------------------------------------------------------------------------------
def str_CleanWord(st, old):
    return str_ReplaceWord(st, old, "")
    
# str_TrimCleanSpaces ----------------------------------------------------------------------------------------------------------------------
def str_TrimCleanSpaces(st):
    st = str_CleanEnter(st)
    return str_CleanPattern(st, " ")

# str_SpacesOut ----------------------------------------------------------------------------------------------------------------------
def str_SpacesOut(st):
    return str_TrimCleanSpaces(st)

# str_CleanEnter ----------------------------------------------------------------------------------------------------------------------
def str_CleanEnter(st):
    sReturn = str_CleanPattern(st, chr(13))
    sReturn = str_CleanPattern(sReturn, chr(10))
    return sReturn

# str_CleanPattern ----------------------------------------------------------------------------------------------------------------------
def str_CleanPattern(st, sPattern):
    st = str(st)
    sPattern = str(sPattern)
    
    if st == "" or len(st)==0:
       return st
    out=""
    nLen = len(st)
    nLenPat = len(sPattern)
    i = 0
    s = ""
    while i < nLen:
          s = st[i:i+nLenPat]
          if len(s)<nLenPat:
             s=st[i-1:]
             out=out[:len(out)-1]
             
          if not s==sPattern:
             out=out+st[i:i+nLenPat]
             #print("str_CleanPattern. Out: " + out)
          i = i+nLenPat
    
    return out
          
# str_StringToList ----------------------------------------------------------------------------------------------------------------------
def str_StringToList(st, delimiter):
    li = list(st.split(delimiter))
    return li
    
# str_ListToString ----------------------------------------------------------------------------------------------------------------------
def str_ListToString(lst):
    return ''.join(lst)
    
# str_ListToStringWithSeparator ----------------------------------------------------------------------------------------------------------------------
def str_ListToStringWithSeparator(lst, ssep):
    out=""
    for i in lst:
        out = out + i + ssep
    out = str_RemoveLastPattern(out, ssep)    
    return out
     
# str_AddSpaceHexa ----------------------------------------------------------------------------------------------------------------------
def str_AddSpaceHexa(sstr):
    nTogether = 2
    sstr = str(sstr)
    if sstr[:2].upper() == "0X":
       nTogether = 4
    
    sOut = str_AddCharToString(sstr, nTogether, " ")
    return sOut

# str_SpaceHexa ----------------------------------------------------------------------------------------------------------------------
def str_SpaceHexa(sstr):
    sstr =str_SpacesOut(sstr)
    #print("sstr: " + sstr)
    return str_AddSpaceHexa(sstr)

# str_AddCharToString ----------------------------------------------------------------------------------------------------------------------
def str_AddCharToString(sstr, nTogether, sChar):
    if nTogether <= 0:
       return sstr
    
    sstr = str_TrimCleanSpaces(sstr)
    #print("str_AddCharToString: sstr = " + sstr)
        
    nLen = len(sstr)
    sOut = ""
    n = 0
    while n < nLen:
          if (n % nTogether) == 0:
             if n > 0:
                sOut = sOut + sChar
          sOut = sOut + sstr[n:n+1]      
          #print("str_AddCharToString: " + sOut)
          n = n + 1
    
    return sOut      

# str_formatNro ----------------------------------------------------------------------------------------------------------------------
def str_formatNro(nNro, nPaddingLeft):
    sNro = ("{:0>" + str(nPaddingLeft) + "}").format(nNro)
    return sNro
    
# str_RepeatString ----------------------------------------------------------------------------------------------------------------------
def str_RepeatString(nNro, sChar):
    sReturn = ""
    #print("valid_nro_int: " + str(valid_nro_int(nNro)))
    if valid_nro_int(nNro):
       nNro = int(nNro)
    else:
       return ""
          
    if nNro > 0 and sChar != "":
       n = 0
       while n < nNro:
             sReturn = sReturn + sChar
             n = n + 1
    
    #print("sReturn: " + sReturn + " - Len: " + str(len(sReturn)))
             
    return sReturn
  
# str_StringToNumberFloat ----------------------------------------------------------------------------------------------------------------------
def str_StringToNumberFloat(sIn):
    nReturn = 0
    if sIn != "" and valid_nro(sIn):
       nReturn = float(sIn)         
    return nReturn
   
# str_StringToNumberInt ----------------------------------------------------------------------------------------------------------------------
def str_StringToNumberInt(sIn):
    nReturn = 0
    if sIn != "" and valid_nro(sIn):
       nReturn = int(sIn)         
    return nReturn
  
# str_GetComillaDoble ----------------------------------------------------------------------------------------------------------------------
def str_GetComillaDoble():
    return chr(34)    
    
# str_GetComillaItalic ----------------------------------------------------------------------------------------------------------------------
def str_GetComillaItalic():
    return chr(44)    

# str_GetENTER ----------------------------------------------------------------------------------------------------------------------
def str_GetENTER():
    return chr(13) + chr(10)    

# str_GetENTERChar ----------------------------------------------------------------------------------------------------------------------
def str_GetENTERChar():
    return "\n"

# str_GetTAB ----------------------------------------------------------------------------------------------------------------------
def str_GetTAB():
    return chr(9)    

# str_GetTABChar ----------------------------------------------------------------------------------------------------------------------
def str_GetTABChar():
    return "\t"    

# str_GetBETWEENPARAM ----------------------------------------------------------------------------------------------------------------------
def str_GetBETWEENPARAM():
    return chr(1)    


# str_AddThousandToNumber ----------------------------------------------------------------------------------------------------------------------
def str_AddThousandToNumber(sNro, sSepara="."):

    sNro = str(sNro)
    sNro = str_SpacesOut(sNro)
    
    nMod = 3
    
    sSepara = str_SpacesOut(sSepara)
    if sSepara == "":
       sSepara = "."

    sSeparaDecimal = ","
    if sSepara == ",":
       sSeparaDecimal = "."

    #FOR THOSE CASES WHERE IT IS, FOR EXAMPLE, IN FLOAT 12345.0, REMOVING THE FLOAT PART
    sNrot = sNro
    sNro = str_RemoveFromNumberDecimals(sNro, sSepara)
       
    #print("Nro: " + sNro + ", Separator: " + sSepara)
       
    sOut = ""
    nMax = len(sNro)
    n = 0
    while nMax >= 0:
          sChr = str_mid(sNro, nMax, 1)

          if n >= nMod:
             sChr = sChr + sSepara
             n = 0          
          n = n + 1
       
          sOut = sOut + sChr
          nMax = nMax - 1
    
    #print("Out to reverse: " + sOut)
    
    sOut = str_reverseAll(sOut)      
    
    if sOut[:1] == sSepara:
       sOut = sOut[1:]

    if len(sNro) < len(sNrot):
       #print("sNro: " + str(sNro) + " - sNrot: " + str(sNrot))
       sT = str_midToEnd(sNrot, len(sNro)+1)
       #print("sT: " + sT)
       sOut = sOut + sSeparaDecimal + sT
       #print("sOut: " + str(sOut))
       
    #print("Out reversed: " + sOut)
    
    if str_right(sOut, 2) == ",0":
       sOut = str_left(sOut, len(sOut)-2)
    
    return sOut


# str_formatNumberFloatToPrint(nvalue) ----------------------------------------------------------------------------------------------------------------------
def str_formatNumberFloatToPrint(nvalue):
    svalue = '{:,.2f}'.format(nvalue)
    svalue = str(svalue)
    #print("str_formatNumberFloatToPrint: " + svalue)
    return svalue
 
 
# str_reverseAll ----------------------------------------------------------------------------------------------------------------------
def str_reverseAll(data):
    sOut = ""
    nMax = len(data)
    n = 0
    while nMax >= 0:
          sChr = str_mid(data, nMax, 1)
          sOut = sOut + sChr
          nMax = nMax - 1

    return sOut

# str_RemoveFromNumberDecimals ----------------------------------------------------------------------------------------------------------------------
def str_RemoveFromNumberDecimals(sNro, sSeparaComa):

    #print("sNro: " + str(sNro) + ", sSeparaComa: " + str(sSeparaComa))
    sNro = str_SpacesOut(str(sNro))
    
    if sSeparaComa != "":
       if str_instrBool(sNro, sSeparaComa):
          sNro = str_getSubStringFromOcurFirst(sNro, sSeparaComa)
       
    return sNro
    
    
# str_nro0To9FromString ----------------------------------------------------------------------------------------------------------------------
def str_nro0To9FromString(sData):
    sValue = str_nro0To9FromStringRemoveOtherChars(sData)
    
    if sValue == sData:
       return True
    else:
       return False

    return True

# str_nro0To9FromString ----------------------------------------------------------------------------------------------------------------------
def str_nro0To9FromStringRemoveOtherChars(sData):
    sReturn = ""
    sData = str(sData)
    nLen = len(str(sData))
    n = 0
    while n < nLen:
          sChar = sData[n:n+1]
          #print("Char: " + sChar)
          if sChar == "0" or sChar == "1" or sChar == "2" or sChar == "3" or sChar == "4" or sChar == "5" or sChar == "6" or sChar == "7" or sChar == "8" or sChar == "9":
             sReturn = sReturn + sChar
          
          n = n + 1
    
    return sReturn

# str_IsNnro0To9FromString ----------------------------------------------------------------------------------------------------------------------
def str_IsNnro0To9FromString(sData):
 
    sData = str(sData)
    sClean = str_nro0To9FromStringRemoveOtherChars(sData)
    if len(sClean) != len(sData):
       return False
    else:
       return True

# str_FloatToString ----------------------------------------------------------------------------------------------------------------------
def str_FloatToString(Nro, Decimals):
    sReturn = round(Nro, Decimals)
    #print(sReturn)
    return str(sReturn)

# str_GetPorcentageToString ----------------------------------------------------------------------------------------------------------------------
def str_GetPorcentageToString(NroBaseFrom100, Nro, Decimals):
    nNro100 = Nro * 100
    #print(nNro100)
    nReturn = float(nNro100 / NroBaseFrom100)
    #print(nReturn)
    sReturn = str_FloatToString(nReturn, Decimals)
    #print(sReturn)
    return sReturn
    
# str_StringToList ----------------------------------------------------------------------------------------------------------------------
def str_StringToList(sData, nTogether):
    
    if nTogether == 0:
       nTogether = 1

    nMax = len(sData)    
    lst = []
    n = 0
    while n < nMax:
          s = sData[n:n+nTogether]
          lst.append(s)
          n = n + nTogether
    
    return lst
           
# str_GetTimer ----------------------------------------------------------------------------------------------------------------------
def str_GetTimer(interval):
    interval = str_reverse(interval)
    hours =  int(interval[:-4])*60*60
    minutes = int(interval[2:-2])*60
    seconds = int(interval[4:])
    timer = hours+minutes+seconds
    timer = float(timer)
    stimer = str(timer)
    return stimer

# bytes_CleanPrintableASCII ----------------------------------------------------------------------------------------------------------------------
def str_CleanNotPrintableASCII(sData, sReplace):

    nMax = len(sData)
    sReturn = ""    
    n = 0
    while n < nMax:
          s = sData[n:n+1]
          #print("n: " + str(n) + " - s: " + s)
          sReturn = sReturn + str_CleanNotPrintableASCIIChar(s, sReplace)
          n = n + 1
          
    return sReturn

# str_CleanNotPrintableASCIIChar ----------------------------------------------------------------------------------------------------------------------
def str_CleanNotPrintableASCIIChar(sChar, sReplace):

    if sChar == "":
       return ""
       
    #print("sChar: " + sChar)
    #print("ord(sChar): " + str(ord(sChar)))
       
    nVal = str_CharToNumber(sChar)
    #print("nVal: " + str(nVal))
    
    nVal = int(nVal)
    #32 = [SPACE]
    #126 = [~]
    #9 = [TAB]
    #8226 => [•]
    
    nLst = len(str_lst_NotPrintableASCIICharExceptions)
    n = 0
    while n < nLst:
          if nVal == str_lst_NotPrintableASCIICharExceptions[n]:
             return sChar
          n = n + 1   
    
    #if (nVal >= 32 and nVal <= 126 or (nVal == 10 or nVal == 13 or nVal == 9 or nVal == 8226)):
    if (nVal >= 32 and nVal <= 126):
       return sChar
    else:
       return sReplace
 
# str_CharToNumber ----------------------------------------------------------------------------------------------------------------------
def str_CharToNumber(sChar):
    if sChar == "":
       return 0
    return ord(sChar)

# str_NumberToChar ----------------------------------------------------------------------------------------------------------------------
def str_NumberToChar(nVal):
    return chr(int(nVal))
 
# str_CSVRowClean ----------------------------------------------------------------------------------------------------------------------
def str_CSVRowClean(row):
    sReturn = str(row)
    sReturn = str_Replace(sReturn, "[", "")
    sReturn = str_Replace(sReturn, "]", "")
    sReturn = str_Replace(sReturn, "'", "")
    return sReturn

# str_CleanCharLeft ----------------------------------------------------------------------------------------------------------------------
def str_CleanCharLeft(sData, sCSVSepara):
    return str_CleanCharRightOrLeft(sData, sCSVSepara, True)

# str_CleanCharRight ----------------------------------------------------------------------------------------------------------------------
def str_CleanCharRight(sData, sCSVSepara):
    return str_CleanCharRightOrLeft(sData, sCSVSepara, False)

# str_CleanCharRightOrLeft ----------------------------------------------------------------------------------------------------------------------
def str_CleanCharRightOrLeft(sData, sCSVSepara, bLeft):
 
    if len(sData) > 0 :
       if bLeft:
          if str_left(sData,len(sCSVSepara)) == sCSVSepara:
             sData = str_midToEnd(sData,len(sCSVSepara))
       else:
          if str_right(sData,len(sCSVSepara)) == sCSVSepara:
             sData = str_left(sData,len(sData)-len(sCSVSepara))
    
    return sData

    
# str_DataWithSeparatorInLines ----------------------------------------------------------------------------------------------------------------------
def str_DataWithSeparatorInLines(sData, sSepara):
    n = 0
    nPat = str_CountPattern(sData, sSepara)
    sReturn = ""
    
    while n < nPat:
          sReturn = sReturn + str_GetENTER() + str_getSubStringFromOcur(sData, sSepara, n)
          n = n + 1
    
    sReturn = str_CleanCharLeft(sReturn, str_GetENTER())
    return sReturn
    
# str_ListToStrClean ----------------------------------------------------------------------------------------------------------------------
def str_ListToStrClean(sData, bCleanENTER):
    if sData=="":
       return sData

    #print("str_ListToStrClean sData: " + sData)
    sT = str_CleanPattern(sData, "[")
    #print("str_ListToStrClean sT 1: " + sT)
    sT = str_CleanPattern(sT, "]")
    #print("str_ListToStrClean sT 2: " + sT)
    sT = str_CleanPattern(sT, "'")
    #print("str_ListToStrClean sT 3: " + sT)
    
    #print("str_ListToStrClean bCleanENTER: " + str(bCleanENTER))
    
    if bCleanENTER:
       sT = str_CleanPattern(sT, "\\r")
       #print("str_ListToStrClean sT 4: " + sT)
       sT = str_CleanPattern(sT, "\\n")
       #print("str_ListToStrClean sT 5: " + sT)
    else:
       sT = str_Replace(sT, "\\r", str_GetENTER())
       #print("str_ListToStrClean sT 6: " + sT)
       sT = str_Replace(sT, "\\n", str_GetENTER())
       #print("str_ListToStrClean sT 7: " + sT)
          
    #print("str_ListToStrClean sT 8: " + sT)
          
    return sT

# str_IsNro ----------------------------------------------------------------------------------------------------------------------
def str_IsNro(nro):
    
    isValidNro = True
    
    if nro is None:
       return False

    try:
        #val = int(userInput)
        isinstance(nro, (int, float))
    except ValueError:
        isValidNro = False    
    
    #print("NRO: " + str(nro) + " = RESULT: " + str(isValidNro))    
    
    return isValidNro

# str_IsNro_Type ----------------------------------------------------------------------------------------------------------------------
def str_IsNro_Type(nro, type):
    
    isValidNro = True
    
    if nro is None:
       return False

    try:
        #val = int(userInput)
        isinstance(nro, type)
    except ValueError:
        isValidNro = False    
    
    #print("NRO: " + str(nro) + ", TYPE: " + str(type) + " = RESULT: " + str(isValidNro))    
    return isValidNro
    

# str_IsNroInt ----------------------------------------------------------------------------------------------------------------------
def str_IsNroInt(nro):
    return str_IsNro_Type(nro, int)

# str_IsNroFloat ----------------------------------------------------------------------------------------------------------------------
def str_IsNroFloat(nro):
    return str_IsNro_Type(nro, float)

# str_IsStrNumeric ----------------------------------------------------------------------------------------------------------------------
def str_IsStrNumeric(sData):
    sData = str(sData)
    nLen = len(str(sData))
    n = 0
    bReturn = True
    while n < nLen and bReturn:
          sChar = sData[n:n+1]
          #print("Char: " + sChar)
          if not (sChar == "0" or sChar == "1" or sChar == "2" or sChar == "3" or sChar == "4" or sChar == "5" or sChar == "6" or sChar == "7" or sChar == "8" or sChar == "9"):
             bReturn = False
          n = n + 1
    
    return bReturn
 
# str_Porcentage ----------------------------------------------------------------------------------------------------------------------
def str_Porcentage(s100, sAvance):

    n100 = float(s100)
    nAvance = float(sAvance)
    
    # https://openstax.org/books/introduction-python-programming/pages/2-5-dividing-integers
    # True division (/) converts numbers to floats before dividing. Ex: 7 / 4 becomes 7.0 / 4.0, resulting in 1.75.
    # Floor division (//) computes the quotient, or the number of times divided. Ex: 7 // 4 is 1 because 4 goes into 7 one time, remainder 3. The modulo operator (%) computes the remainder. Ex: 7 % 4 is 3.
 
    nResult = 0
    if n100 != 0:
       nResult = round(float((nAvance * 100)/n100),2) 
    
    #print("porcentage - nResult: " + str(nResult) + " - nAvance: " + str(nAvance) + " - n100: " + str(n100))
    #exit(0)
    
    return str(nResult)
 
# str_CleanThousands ----------------------------------------------------------------------------------------------------------------------
def str_CleanThousands(sVal):
    sVal = str_Replace(sVal, ".", "")
    sVal = str_Replace(sVal, ",", "")
    return sVal

# str_CleanSpaceFromLeft ----------------------------------------------------------------------------------------------------------------------
def str_CleanSpaceFromLeft(sVal):
    return str_CleanPatternFromLeftOrRight(sVal, " ", True)
    
# str_CleanSpaceFromRight ----------------------------------------------------------------------------------------------------------------------
def str_CleanSpaceFromRight(sVal):
    return str_CleanPatternFromLeftOrRight(sVal, " ", False)

# str_CleanPatternFromLeft ----------------------------------------------------------------------------------------------------------------------
def str_CleanPatternFromLeft(sVal, sPattern):
    return str_CleanPatternFromLeftOrRight(sVal, sPattern, True)
    
# str_CleanPatternFromRight ----------------------------------------------------------------------------------------------------------------------
def str_CleanPatternFromRight(sVal, sPattern):
    return str_CleanPatternFromLeftOrRight(sVal, sPattern, False)

# str_CleanPatternFromLeftOrRight ----------------------------------------------------------------------------------------------------------------------
def str_CleanPatternFromLeftOrRight(sVal, sPattern, bLeft=True):
    
    if sPattern == "":
       return sVal
    if sVal == "":
       return sVal   

    if bLeft:
       return sVal.removeprefix(sPattern)       
    else:
       return sVal.removesuffix(sPattern)          

#------------------------------------------------------------------------------------
# str_PaddingAddSpacesToTheRight => Add spaces to the right taking into account nMaxRef - len(sValue)
# nMaxCharLenDes = 15
# sCountryDes = Argentina
# Example Input: "(" + str_PaddingAddSpacesToTheRight(nMaxCharLenDes, sCountryDes + ")")
# Example Output: "(Argentina)    " => String Length = 15 characters
#------------------------------------------------------------------------------------
def str_PaddingAddSpacesToTheRight(nMaxRef, sValue):
    sValue = str_CleanSpaceFromRight(sValue)
    sSpaces = str_PaddingAddSpacesToTheRightByNro(nMaxRef, len(str(sValue)))
    return sValue + sSpaces    

#------------------------------------------------------------------------------------
# str_PaddingAddSpacesToTheRightByNro => Add spaces to the right taking into account nMaxRef - nValue
# nMaxCharLenPrefix = 7
# nCountryPrefixDigits = 3
# Example Input: str_PaddingAddSpacesToTheRightByNro(nMaxCharLenPrefix, nCountryPrefixDigits)
# Example Output: "    " => returned 4 spaces.
#------------------------------------------------------------------------------------
def str_PaddingAddSpacesToTheRightByNro(nMaxRef, nValue):
    sValue = str_RepeatString(nValue, "a")
    return str_PaddingAddCharToTheRightByNro(nMaxRef, sValue, " ")
    
#------------------------------------------------------------------------------------
# str_PaddingAddSpacesToTheRightByNro => Add character to the right taking into account nMaxRef - len(sValue)
# nMaxRef = 7
# nValue = "tes" => 3 characters length
# sChar = ' ' (space)
# bAddValue = False
# Example Input: str_PaddingAddSpacesToTheRightByNro(nMaxRef, sValue, sChar)
# Example Output: "    " => returned 4 spaces.
#------------------------------------------------------------------------------------
def str_PaddingAddCharToTheRightByNro(nMaxRef, sValue, sChar=" ", bAddValue=False):
    nStrSpaces =  int(nMaxRef) - int(len(sValue))
    sSpaces = ""
    if nStrSpaces > 0:
       sSpaces = str_RepeatString(nStrSpaces, sChar)
       
    if bAddValue:
       sSpaces = sSpaces + sValue
          
    return sSpaces    

#------------------------------------------------------------------------------------
# str_PaddingAddSpacesToTheRightPorcentage 
#------------------------------------------------------------------------------------
def str_PaddingAddSpacesToTheRightPorcentage(sValue):
    return str_PaddingAddSpacesToTheRight(5, sValue)

#------------------------------------------------------------------------------------
# str_getNroPartInt 
#------------------------------------------------------------------------------------
def str_getNroPartInt(sValue):
    sEntero, sDecimnal = str_getNroPartIntAndDecimal(sValue)
    return sEntero
    
#------------------------------------------------------------------------------------
# str_getNroPartDecimal 
#------------------------------------------------------------------------------------
def str_getNroPartDecimal(sValue):
    sEntero, sDecimnal = str_getNroPartIntAndDecimal(sValue)
    return sDecimnal
    
#------------------------------------------------------------------------------------
# str_getNroPartIntAndDecimal 
#------------------------------------------------------------------------------------
def str_getNroPartIntAndDecimal(sValue):
    
    sPunto = "."
    sComa = ","
    
    sValue = str(sValue)
    sEntero = sValue
    sDecimal = ""
    
    #print("str_getNroPartIntAndDecimal - sValue = " + str(sValue))
    
    nPuntos = str_CountCharInStr(sValue, sPunto)

    #print("str_getNroPartIntAndDecimal - nPuntos = " + str(nPuntos))
    
    if nPuntos == 1:
       sEntero = str_getSubStringFromOcur(sValue, sPunto, 0)
       sDecimal = str_getSubStringFromOcur(sValue, sPunto, 1)
    
    else:
    
       nComas = str_CountCharInStr(sValue, sComa)

       #print("str_getNroPartIntAndDecimal - nComas = " + str(nComas))

       if nComas == 1:
          sEntero = str_getSubStringFromOcur(sValue, sComa, 0)
          sDecimal = str_getSubStringFromOcur(sValue, sComa, 1)

    #print("str_getNroPartIntAndDecimal - sEntero = " + str(sEntero))
    #print("str_getNroPartIntAndDecimal - sDecimal = " + str(sDecimal))
     
    return sEntero, sDecimal

#------------------------------------------------------------------------------------
# str_getListFromStringInHexa 
#------------------------------------------------------------------------------------
def str_getListFromStringInHexa(sStr, nBytesTogether=1):
    return str_getListFromString(sStr, nBytesTogether*2)
    
#------------------------------------------------------------------------------------
# str_getListFromString 
#------------------------------------------------------------------------------------
def str_getListFromString(sStr, nCharsTogether=1):
    
    lst = []
    if sStr != "":
       n = 0
       while n < len(sStr):
             sVal = str_mid(sStr, n, nCharsTogether)
             lst.append(sVal)
             n = n + nCharsTogether
    
    return lst   


#------------------------------------------------------------------------------------
# str_DoubleWithEPlusToString 
# Example: 3,73762E+13
# Return:  37376200000000
# Exmaple: 4.36892E+13
# Return:  43689200000000
#------------------------------------------------------------------------------------
def str_DoubleWithEPlusToString(sVal):
    
    #TESTING
    #sVal = "3,73762E+13"
    #print("str_DoubleWithEPlusToString - sVal: " + str(sVal) + " - Return: " + str(str_DoubleWithEPlusToString(sVal)))
    #sVal = "4.36892E+13"
    #print("str_DoubleWithEPlusToString - sVal: " + str(sVal) + " - Return: " + str(str_DoubleWithEPlusToString(sVal)))
    
    sEPlus = "E+"
    sReturn = sVal

    if sEPlus in sVal:
       
       sEPlusNro = str_getSubStringFromOcur(sVal, sEPlus, 1)
       sValNoEPlus = str_getSubStringFromOcur(sVal, sEPlus, 0)
       
       sValNoEPlusInit = ""
       sChar = ","
       if sChar in sValNoEPlus:
          sValNoEPlusInit = str_getSubStringFromOcur(sValNoEPlus, sChar, 0)
       else:
          sChar = "."   
          if sChar in sValNoEPlus:
             sValNoEPlusInit = str_getSubStringFromOcur(sValNoEPlus, sChar, 0)
       
       sValNoEPlusInitThen = str_getSubStringFromOcur(sValNoEPlus, sChar, 1)
       
       nEPlusNro = int(sEPlusNro)
       
       if len(sValNoEPlusInitThen) < nEPlusNro:
          sValNoEPlusInitThen = sValNoEPlusInitThen + str_RepeatString(nEPlusNro - len(sValNoEPlusInitThen), "0")
          
       sReturn = sValNoEPlusInit + sValNoEPlusInitThen  
       
    return sReturn

#------------------------------------------------------------------------------------
