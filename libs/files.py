# -*- coding: UTF-8 -*-

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
  
sys.path.append(parent_directory+"/libs")
sys.path.append(parent_directory)

sys.path.append('../libs')
 
from str import *
from bytes import *
import csv
from validanro import *

#------------------------------------------------------------------------------------
# fFileToList => MSISDNs to List
#------------------------------------------------------------------------------------
def FileToList(sData, sCSVSepara, nColForSort, bValidateNumber=False):
    reader1 = csv.reader(open(sData, 'r'), delimiter=sCSVSepara)
    
    if nColForSort=="":
       nColForSort="0"
    nColForSort = int(nColForSort)   
       
    nCols = fFileGetMaxCols(sData, sCSVSepara)
    if int(nCols) >= int(nColForSort):
       reader1 = sorted(reader1, key=lambda row: int(nColForSort), reverse=False)
    
    #print("reader1: " + str(reader1))
    sListReturn = []
    
    sMSISDNListCommas = ""
    
    n = 0
    for row1 in reader1:
        sMSISDN = row1[0]
        #print("sMSISDN: " + str(sMSISDN))
        
        bProcess = True
        if bValidateNumber:
           if str_IsNnro0To9FromString(sMSISDN)==False:
              bProcess = False
        
        if bProcess:               
           #print("sMSISDN: " + sMSISDN)
           sListReturn.append(sMSISDN)
           sMSISDNListCommas = sMSISDNListCommas + sCSVSepara + sMSISDN
           n = n + 1

    if len(sMSISDNListCommas) > 0 :
       if str_left(sMSISDNListCommas,1) == sCSVSepara:
          sMSISDNListCommas = str_midToEnd(sMSISDNListCommas,1)
       sPrint = "\nList separated by '" + sCSVSepara + "': \n" + sMSISDNListCommas   
       print(sPrint)

    #print("sListReturn: " + str(sListReturn))
    print("Records processed: " + str(n) + " for file " + sData)
    
    return sListReturn
  
#------------------------------------------------------------------------------------
# fFileGetMaxCols => Get maximum columns
#------------------------------------------------------------------------------------
def fFileGetMaxCols(sData, sCSVSepara):
    readerT = csv.reader(open(sData, 'r'), delimiter=sCSVSepara)
    
    for row1 in readerT:
        nLen = len(row1)
        #print("fFileGetMaxCols: " + str(nLen))
        return nLen        

    return 0

#------------------------------------------------------------------------------------
# fFileSaveLogAndPrint => Open and Write file for log data
#------------------------------------------------------------------------------------
def fFileOpenAndSaveLogAndPrint(bFileOpensLog, sFileName, bFileAppend, file2write, sLog, bFileCloseAfterWrite):
    try:
       if str(bFileOpensLog) == "True":
          if str(bFileAppend) == "True":
             file2write=open(sFileName,'a')
          else:
             file2write=open(sFileName,'w')
       
       if sLog != "":      
          file2write.write(sLog + "\n")
          print(sLog)
       
       if str(bFileCloseAfterWrite)=="True":
          fFileClose(file2write)
          
       return file2write
       
    except IOError(err):
       print(str(err))
       return file2write
       

#------------------------------------------------------------------------------------
# fFileSaveLogAndPrint => Write file for log data
#------------------------------------------------------------------------------------
def fFileSaveLogAndPrint(file2write, sLog):
    return fFileOpenAndSaveLogAndPrint(False, "", False, file2write, sLog, False)

#------------------------------------------------------------------------------------
# fFileOpenForWrite => Open file for Write
#---------------------------------------------------------
def fFileOpenForWrite(sFileName):
    file2write = ""
    return fFileOpenAndSaveLogAndPrint(True, sFileName, False, file2write, "", False)

#------------------------------------------------------------------------------------
# fFileOpenForAppend => Open file for Append
#---------------------------------------------------------
def fFileOpenForAppend(sFileName):
    file2write = ""
    return fFileOpenAndSaveLogAndPrint(True, sFileName, True, file2write, "", False)

#------------------------------------------------------------------------------------
# fFileClose => Close File
#---------------------------------------------------------
def fFileClose(file2write):
    file2write.close()
    return 

#------------------------------------------------------------------------------------
# fFileGetCSVHeader => Get header from CSV file
#---------------------------------------------------------
def fFileGetCSVHeader(sFile, sCSVSepara=","):
    reader1 = csv.reader(open(sFile, 'r'), delimiter=sCSVSepara)
    #GET HEADER
    sHeader = ""
    for row1 in reader1:
        nCols = len(row1)
        m = 0
        while m < nCols:
            sHeader = sHeader + sCSVSepara + str(row1[m]) 
            m = m + 1
        break
        
    if str_left(sHeader, len(sCSVSepara))== sCSVSepara:
       sHeader = str_midToEnd(sHeader, len(sCSVSepara))
       
    #print("sHeader = " + str(sHeader))
    return sHeader
    
#------------------------------------------------------------------------------------
# fFileOpenBinaryMode => Open file in Binary Mode for Reading
#---------------------------------------------------------
def fFileOpenBinaryMode(sPathAndFile):
    
    if sPathAndFile=="":
       return ""

    err = ""   

    try:
       fileBin=open(sPathAndFile,'rb')
       return fileBin
       
    except Exception as e:
       sError = "An unexpected error has occurred. " + str(e)    
       print("fFileOpenBinaryMode - Error: " + sError)
       return ""

#------------------------------------------------------------------------------------
# fFileOpenBinaryMode => Open file in Binary Mode for Reading
#---------------------------------------------------------
def fFileOpenBinaryModeAndRead(sPathAndFile):
    
    file = fFileOpenBinaryMode(sPathAndFile)
    if file is None or str(file) == "":
       return ""
    
    err = ""   
    try:
       binary_data = file.read()
       #print("fFileOpenBinaryModeAndRead - binary_data = " + str(binary_data))
       sData = bytes_BinaryDataFromFileToHEXA(binary_data)
       file.close()
       
       return str(sData).upper()
       
    except IOError(err):
       sError = str(err)
       print("fFileOpenBinaryModeAndRead - Error: " + sError)
       return ""

#---------------------------------------------------------------------------------------------------------
# file_fFileIsExe => Check whether it is an exe file or script to be executed by run.bat
#---------------------------------------------------------------------------------------------------------
def file_fFileIsExe():
    # Asegura que la ruta sea correcta si el ejecutable est� empaquetado
    if hasattr(sys, '_MEIPASS'):  # Si es un ejecutable
       return True
    else:  # Si est� corriendo como script
       return False
    
#---------------------------------------------------------------------------------------------------------
# file_fNormalPathForWindowsLinux => 
# Path Manipulation: 
# When constructing file paths, you might encounter situations where you accidentally include "//" in the path string. 
# Python's os.path module provides functions to normalize paths, effectively collapsing multiple forward slashes into single ones.
#---------------------------------------------------------------------------------------------------------
def file_fNormalPathForWindowsLinux(sPath):
    return os.path.normpath(sPath)     


#---------------------------------------------------------------------------------------------------------
# file_FileExists
#---------------------------------------------------------------------------------------------------------
def file_FileExists(sPathFile):
    if os.path.exists(sPathFile):
       return True
    else:
       return False
          
#---------------------------------------------------------------------------------------------------------
# file_OpenFileExplorer
# Path to be opened
#---------------------------------------------------------------------------------------------------------
def file_OpenFileExplorer(sPath):

    current = os.path.dirname(os.path.realpath(__file__))
    parent_directory = os.path.dirname(current)
    
    if not file_FileExists(sPath):
       sPath = parent_directory
       
    # To open a specific folder
    #sPath = r + sPath  # Use 'r' for raw string to handle backslashes
    
    os.startfile(sPath)
    
    return

#---------------------------------------------------------------------------------------------------------
# file_PathAndFile_GetPath
#---------------------------------------------------------------------------------------------------------
def file_PathAndFile_GetPath(sPathAndFile):
    sPath, sFile = file_PathAndFile_GetSeparated(sPathAndFile)
    return sPath

#---------------------------------------------------------------------------------------------------------
# file_PathAndFile_GetFileName
#---------------------------------------------------------------------------------------------------------
def file_PathAndFile_GetFileName(sPathAndFile):
    sPath, sFile = file_PathAndFile_GetSeparated(sPathAndFile)
    return sFile
    
#---------------------------------------------------------------------------------------------------------
# file_PathAndFile_GetSeparated
# Path and File Name to process
#---------------------------------------------------------------------------------------------------------
def file_PathAndFile_GetSeparated(sPathAndFile):
    
    tFiles = []
    
    sPath = ""
    sFile = ""
    
    sSepara = "/"
    if sSepara in sPathAndFile:
       tFiles = sPathAndFile.split(sSepara)
    else:   
       sSepara = "\\"
       if sSepara in sPathAndFile:
          tFiles = sPathAndFile.split(sSepara)
    
    if len(tFiles) > 0:
       n = 0 
       while n < len(tFiles)-1:
             sPath = sPath + tFiles[n] + sSepara
             n = n + 1
       sFile = tFiles[len(tFiles)-1]    
     
    #print("file_PathAndFile_GetSeparated - sPathAndFile = " + str(sPathAndFile))
    #print("file_PathAndFile_GetSeparated - sPath = " + str(sPath))
    #print("file_PathAndFile_GetSeparated - sFile = " + str(sFile))
       
    return sPath, sFile      
    
#---------------------------------------------------------------------------------------------------------
# file_IsOSWindows
#---------------------------------------------------------------------------------------------------------
def file_IsOSWindows():
    if os.name == "nt" or sys.platform == "win32":
       return True
    else:
       return False

#---------------------------------------------------------------------------------------------------------
# file_IsOSMac
#---------------------------------------------------------------------------------------------------------
def file_IsOSMac():
    if sys.platform == "darwin":
       return True
    else:
       return False

#---------------------------------------------------------------------------------------------------------
# file_IsOSLinux
#---------------------------------------------------------------------------------------------------------
def file_IsOSLinux():
    if os.name == "posix" or sys.platform == "linux":
       return True
    else:
       return False
           
#------------------------------------------------------------------------------------
