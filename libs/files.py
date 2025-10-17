# -*- coding: UTF-8 -*-

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
  
sys.path.append(parent_directory+"/libs")
sys.path.append(parent_directory)

sys.path.append('../libs')

import datetime

from str import *
from bytes import *
from log import *
import csv
from validanro import *

file_slashdouble = "\\" 
file_slash = "/" 

import pandas as pd

#-------------------------------------------------------------------------
#FOR FILE DICTIONARY
file_dic_path_file = "path_file"
file_dic_size = "file_size"
file_dic_creation_date = "creation_date"
file_dic_modification_date = "modification_date"
file_dic_access_date = "access_date"
file_dic_directory_type = "directory_type"
#-------------------------------------------------------------------------


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
# file_getFileSlash => get whether path is with "\"" or with "//"
#---------------------------------------------------------------------------------------------------------
def file_getFileSlash(sPathAndFile):

    if file_slashdouble in sPathAndFile:
        return sPathAndFile
    
    return file_slash

#---------------------------------------------------------------------------------------------------------
# file_PathAndFile_GetSeparated
# Path and File Name to process
#---------------------------------------------------------------------------------------------------------
def file_PathAndFile_GetSeparated(sPathAndFile):
    
    tFiles = []
    
    sPath = ""
    sFile = ""
    
    sSepara = file_getFileSlash(sPathAndFile)
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

#---------------------------------------------------------------------------------------------------------
# file_osSeparator
# On Unix-like systems (Linux, macOS), os.sep will return /.
# On Windows, os.sep will return `\` ("\\")
#---------------------------------------------------------------------------------------------------------
def file_osSeparator():
    return os.sep


#---------------------------------------------------------------------------------------------------------
# ffile_AreDirDuplicatedx
#---------------------------------------------------------------------------------------------------------
def file_AreFilesDuplicated(lstSource, lstDestination, bCleanSpaces=False):

    sDuplicated = ""

    n = 0
    while n < len(lstSource):
          m = 0
          while m < len(lstDestination):
                
                if bCleanSpaces:
                    lstSource[n] = str_SpacesOut(lstSource[n])
                    lstDestination[m] = str_SpacesOut(lstDestination[m])
                    
                if str(lstSource[n]) == str(lstDestination[m]):
                    sDuplicated = "Source duplicated with Destination.\n"
                    sDuplicated += "Source occurence = " + str(n) + ": '" + str(lstSource[n]) + "'"
                    sDuplicated += " duplicated with Destination occurence = " + str(m)
                    return True, sDuplicated
                m = m + 1
          n = n + 1

    return False, ""

#---------------------------------------------------------------------------------------------------------
# file_Error_handler
#---------------------------------------------------------------------------------------------------------
def file_Error_handler(err):
    return file_Error_handlerWithDes(err, "", "")

#---------------------------------------------------------------------------------------------------------
# file_Error_handlerWithDes
#---------------------------------------------------------------------------------------------------------
def file_Error_handlerWithDes(err, sLogFile="", sMsgOptional=""):

    if sMsgOptional == "":
       sMsgOptional = "Error encountered." 

    sError = sMsgOptional
    if str(err) != "":
       sError = sError + str(err)

    # You could also log the error, or raise a different exception
    # For example, to stop the walk on any error:
    # raise err

    bLogFile=False
    if sLogFile != "":
        if file_FileExists(sLogFile):
           log_write_ErrorInRed(sLogFile, sError)
           bLogFile=True

    if not bLogFile:
       log_writePrintOnlyError(sError)

    return 


#---------------------------------------------------------------------------------------------------------
# file_getDirsAndFiles
#---------------------------------------------------------------------------------------------------------
def file_getDirsAndFiles(sStartingPath, sLogFile=""):

    if sStartingPath == "":
       #GET CURRENT DIRECTORY
       sStartingPath = os.getcwd()

    sSlash = file_osSeparator()

    lstFiles = []

    for sRoot, dirs, files in os.walk(sStartingPath, onerror=file_Error_handler):
        # Process root, dirs, and files here
        #print(str(nTotalFound) + ". file_getDirsAndFiles - lstDirs = " + str(dirs))
        #print(str(nTotalFound) + ". file_getDirsAndFiles - lstFiles = " + str(files))
        #print(str(nTotalFound) + ". file_getDirsAndFiles - sRoot = " + str(sRoot))

        if len(dirs) > 0:
            m = 0
            while m < len(dirs):
                sTemp = file_formatFilePathWithSlash(sRoot + sSlash + str(dirs[m]))
                #print("file_getDirsAndFiles - DRECTORIES sTemp = " + str(sTemp))
                lstFiles.append(sTemp)
                m = m + 1

        if len(files) > 0:
            m = 0
            while m < len(files):
                sTemp = file_formatFilePathWithSlash(sRoot + str(files[m]))
                #print("file_getDirsAndFiles - FILES sTemp = " + str(sTemp))
                lstFiles.append(sTemp)
                m = m + 1

    return sorted(lstFiles)

#---------------------------------------------------------------------------------------------------------
# file_getFileState
#---------------------------------------------------------------------------------------------------------
def file_getFileState(sPathAndFile, sLogFile=""):

    try:
       file_stats = os.stat(sPathAndFile)

       file_size = file_stats.st_size
       creation_date = datetime.fromtimestamp(file_stats.st_ctime)
       modification_date = datetime.fromtimestamp(file_stats.st_mtime)
       access_date = datetime.fromtimestamp(file_stats.st_atime)

       return str(file_size), str(creation_date), str(modification_date), str(access_date)

    except FileNotFoundError:
       file_Error_handlerWithDes("", sLogFile, "Error: File not found at " + str(sPathAndFile))
       return "", "", "", ""

    except Exception as e:
       file_Error_handlerWithDes(e, sLogFile, "Getting stats for " + str(sPathAndFile))
       return "", "", "", ""

#---------------------------------------------------------------------------------------------------------
# file_createPandaDicWithFileLstAddingStats
#---------------------------------------------------------------------------------------------------------
def file_createPandaDicWithFileLstAddingStats(lstFiles, bSortByName=True):
    
    files = []

    n = 0
    while n < len(lstFiles):

         if file_FileExists(lstFiles[n]):
             
             file_size, creation_date, modification_date, access_date = file_getFileState(lstFiles[n])

             if file_size != "":
               # SAVE IN A DICT 
               file_record = {}
               file_record[file_dic_path_file] = str(lstFiles[n])
               file_record[file_dic_size] = str(file_size)
               file_record[file_dic_creation_date] = str(creation_date)
               file_record[file_dic_modification_date] = str(modification_date)
               file_record[file_dic_access_date] = str(access_date)
               file_record[file_dic_directory_type] = str(file_Is_a_Directory(lstFiles[n])   )
               files.append(file_record)

         n = n + 1
    
    dfFiles = pd.DataFrame(files)

    if bSortByName and len(files) > 0:
        dfFiles = dfFiles.sort_values(by=file_dic_path_file)
        
    return dfFiles

#---------------------------------------------------------------------------------------------------------
# file_dicSortedBySize
#---------------------------------------------------------------------------------------------------------
def file_PandasDicSortedBySize(df, bSortMaxToMin=True):

    bAscending = False
    if bSortMaxToMin:
       bAscending = True
        
    df_sorted = df
    if len(df) > 0:
        df_sorted = df.sort_values(by=file_dic_size, ascending=bAscending)

    return df_sorted

#---------------------------------------------------------------------------------------------------------
# file_IsFileADirectory
#---------------------------------------------------------------------------------------------------------
def file_Is_a_Directory(sPathAndFile):
    
    if file_FileExists(sPathAndFile):
        if os.path.isdir(sPathAndFile):
            return True
    
    return False    
        

#---------------------------------------------------------------------------------------------------------
# file_formatFilePathWithSlash => set the same slash for the whole path
#---------------------------------------------------------------------------------------------------------
def file_formatFilePathWithSlash(sPathAndFileToFormat):

    sSlash = file_osSeparator()

    sReturn = sPathAndFileToFormat

    if sSlash == file_slashdouble:
       sReturn = str_Replace(sPathAndFileToFormat, file_slash, sSlash) 
       #print("file_formatFilePathWithSlash - file_slashdouble => " +  file_slash + " - sReturn = " + sReturn)
    if sSlash == file_slash:
       sReturn = str_Replace(sPathAndFileToFormat, file_slashdouble, sSlash) 
       #print("file_formatFilePathWithSlash - file_slash => " +  file_slash + " - sReturn = " + sReturn)
                
    return sReturn        
#------------------------------------------------------------------------------------
