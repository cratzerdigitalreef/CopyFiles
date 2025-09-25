# -*- coding: UTF-8 -*-

# valid_nro ----------------------------------------------------------------------------------------------------------------------
def valid_nro(nro):
    
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

# valid_nro_param ----------------------------------------------------------------------------------------------------------------------
def valid_nro_param(nro, type):
    
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
    

# valid_nro_int ----------------------------------------------------------------------------------------------------------------------
def valid_nro_int(nro):
    return valid_nro_param(nro, int)

# valid_nro_float ----------------------------------------------------------------------------------------------------------------------
def valid_nro_float(nro):
    return valid_nro_param(nro, float)

# valid_nro_IsCharValidNro ----------------------------------------------------------------------------------------------------------------------
def valid_nro_IsCharValidNro(schar, bBiggerThan0=False):
    if schar=="":
       return False

    if bBiggerThan0:
       if schar == "0":
          return False
       
    schar = schar.upper()
    nLen = len(schar)
    n = 0
    for i in schar:
        #print("Hexa Char: " + i)
        if i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
           n = n + 1
           
    if n==nLen:
       return True
    else:
       return False                  

 # validaNro_ReplaceLetterByNro ----------------------------------------------------------------------------------------------------------------------
def validaNro_ReplaceLetterByNro(sVal, sNewNro):
    if sVal=="":
       return sVal
       
    sReturn = ""
       
    sVal = sVal.upper()
    nLen = len(sVal)
    n = 0
    for i in sVal:
        #print("Hexa Char: " + i)
        if i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
           sReturn = sReturn + i
        else:
           sReturn = sReturn + sNewNro  
           
    return sReturn

