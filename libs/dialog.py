#! /usr/bin/env python3

from str import *
import ctypes  # An included library with Python install.   
import sys

# db_inputYesNo --------------------------------------------------------------------------------------------------
def db_inputYesNo(sMsg):
    sReturn = input(sMsg)
    if str(sReturn).upper() == "YES" or str(sReturn).upper() == "1":
       return True
    else:
       return False   

# db_input --------------------------------------------------------------------------------------------------
def db_input(sMsg):
    return input(sMsg)

# db_show_Info --------------------------------------------------------------------------------------------------
def db_show_Info(sTitle, sMsg):
    return db_show(sTitle, sMsg, "0", "64")

# db_show_Error --------------------------------------------------------------------------------------------------
def db_show_Error(sTitle, sMsg):
    return db_show(sTitle, sMsg, "0", "16")

# db_show_Warning --------------------------------------------------------------------------------------------------
def db_show_Warning(sTitle, sMsg):
    return db_show(sTitle, sMsg, "0", "48")

# db_show_Question_OkCancel --------------------------------------------------------------------------------------------------
def db_show_Question_OkCancel(sTitle, sMsg):
    return db_show_Question(sTitle, sMsg, "1")

# db_show_Question_AbortRetryIgnore --------------------------------------------------------------------------------------------------
def db_show_Question_AbortRetryIgnore(sTitle, sMsg):
    return db_show_Question(sTitle, sMsg, "2")

# db_show_Question_YesNoCancel --------------------------------------------------------------------------------------------------
def db_show_Question_YesNoCancel(sTitle, sMsg):
    return db_show_Question(sTitle, sMsg, "3")

# db_show_Question_YesNo --------------------------------------------------------------------------------------------------
def db_show_Question_YesNo(sTitle, sMsg):
    return db_show_Question(sTitle, sMsg, "4")

# db_show_Question_RetryNo --------------------------------------------------------------------------------------------------
def db_show_Question_RetryNo(sTitle, sMsg):
    return db_show_Question(sTitle, sMsg, "5")

# db_show_Question_CancelTryagainContinue --------------------------------------------------------------------------------------------------
def db_show_Question_CancelTryagainContinue(sTitle, sMsg):
    return db_show_Question(sTitle, sMsg, "6")

# db_show_Question --------------------------------------------------------------------------------------------------
def db_show_Question(sTitle, sMsg, sButton):
    return db_show(sTitle, sMsg, sButton, "32")
    
# db_show --------------------------------------------------------------------------------------------------
def db_show(sTitle, sMsg, sStyle, sIcon):
    
    sTitle = str(sTitle)
    sMsg = str(sMsg)
    sStyle = str(sStyle)
    sIcon = str(sIcon)
    
    if sTitle == "":
       sTitle = "INFORMATION"
       
    if sMsg == "":
       return ""

    nStyle = 0
    if valid_nro(sStyle):
       nStyle = int(sStyle)
    
    nIcon = 64   
    if valid_nro(sIcon):
       nIcon = int(sIcon)
              
##  Styles:
##  0 : OK
##  1 : OK | Cancel
##  2 : Abort | Retry | Ignore
##  3 : Yes | No | Cancel
##  4 : Yes | No
##  5 : Retry | Cancel 
##  6 : Cancel | Try Again | Continue

## To also change icon, add these values to previous number
# 16 Stop-sign icon
# 32 Question-mark icon
# 48 Exclamation-point icon
# 64 Information-sign icon consisting of an 'i' in a circle
      
    #print("nStyle: " + str(nStyle))
    #print("sMsg: " + sMsg)
    #print("sTitle: " + sTitle)
    #print("nIcon: " + str(nIcon))
    
    #https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxw
    nStyle |= nIcon
    
    sReturn = ctypes.windll.user32.MessageBoxW(0, sMsg, sTitle, nStyle)
    sReturn = str(sReturn)
    #print("Return: " + str(sReturn))
    
#IDABORT = 3
#IDCANCEL = 2
#IDCONTINUE = 11
#IDIGNORE = 5
#IDNO = 7
#IDOK = 1
#IDRETRY = 4
#IDTRYAGAIN = 10
#IDYES = 6
    
    return sReturn
    
# db_show_response --------------------------------------------------------------------------------------------------
def db_show_response(sResponse):
    return str_SpacesOut(str(sResponse))

# db_show_response_OK --------------------------------------------------------------------------------------------------
def db_show_response_OK(sResponse):
    if db_show_response(sResponse)=="1":
       return True
    else:
       return False

# db_show_response_CANCEL --------------------------------------------------------------------------------------------------
def db_show_response_CANCEL(sResponse):
    if db_show_response(sResponse)=="2":
       return True
    else:
       return False

# db_show_response_ABORT --------------------------------------------------------------------------------------------------
def db_show_response_ABORT(sResponse):
    if db_show_response(sResponse)=="3":
       return True
    else:
       return False

# db_show_response_RETRY --------------------------------------------------------------------------------------------------
def db_show_response_RETRY(sResponse):
    if db_show_response(sResponse)=="4":
       return True
    else:
       return False

# db_show_response_IGNORE --------------------------------------------------------------------------------------------------
def db_show_response_IGNORE(sResponse):
    if db_show_response(sResponse)=="5":
       return True
    else:
       return False

# db_show_response_YES --------------------------------------------------------------------------------------------------
def db_show_response_YES(sResponse):
    if db_show_response(sResponse)=="6":
       return True
    else:
       return False

# db_show_response_NO --------------------------------------------------------------------------------------------------
def db_show_response_NO(sResponse):
    if db_show_response(sResponse)=="7":
       return True
    else:
       return False

# db_show_response_TRYAGAIN --------------------------------------------------------------------------------------------------
def db_show_response_TRYAGAIN(sResponse):
    if db_show_response(sResponse)=="10":
       return True
    else:
       return False

# db_show_response_CONTINUE --------------------------------------------------------------------------------------------------
def db_show_response_CONTINUE(sResponse):
    if db_show_response(sResponse)=="11":
       return True
    else:
       return False

    
    