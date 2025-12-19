# -*- coding: UTF-8 -*-

import os
import sys
import stat
import ctypes
import getpass

import shutil

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
file_nRefresh = 100

import pandas as pd

from pathlib import Path
import subprocess
import argparse

#-------------------------------------------------------------------------
# FOR FILE DICTIONARY
# ORDER AND REFERENCES ARE ACCORDING METHOD: file_pandasFileRecord_CreateDicWithFileLstAddingStats - Line 677

n = 0
file_dic_path_file = "file_dic_path_file"
file_dic_path_file_nro = n
n = n + 1
file_dic_size = "file_dic_file_size"
file_dic_size_nro = n
n = n + 1
file_dic_creation_date = "file_dic_creation_date"
file_dic_creation_date_nro = n
n = n + 1
file_dic_modification_date = "file_dic_modification_date"
file_dic_modification_date_nro = n
n = n + 1
file_dic_access_date = "file_dic_access_date"
file_dic_access_date_nro = n
n = n + 1
file_dic_directory_type = "file_dic_directory_type"
file_dic_directory_type_nro = n
n = n + 1
file_dic_path = "file_dic_path"
file_dic_path_nro = n
n = n + 1
file_dic_fileparent = "file_dic_file_parent"
file_dic_fileparent_nro = n
n = n + 1
file_dic_filename = "file_dic_filename"
file_dic_filename_nro = n
n = n + 1
file_dic_fileext = "file_dic_fileext"
file_dic_fileext_nro = n
n = n + 1
file_dic_path_subdir = "file_dic_path_subdir"
file_dic_path_subdir_nro = n
n = n + 1
file_dic_path_to = "file_dic_path_to"
file_dic_path_to_nro = n
n = n + 1
file_dic_status = "file_dic_status"
file_dic_status_nro = n
n = n + 1

file_dic_status_copied = "file_status_copied"
file_dic_status_equal = "file_status_equal"
file_dic_status_dir = "file_status_directory"
file_dic_status_warning = "WARNING"
file_dic_status_warning_dir = "WARNING - DIRECTORY"

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
# fFileOpenTextMode => Open file in Text Mode for Reading
#---------------------------------------------------------
def fFileOpenTextMode(sPathAndFile):
    
    if sPathAndFile=="":
       return ""

    if not file_FileExists(sPathAndFile):
       return ""

    err = ""   

    try:
       file=open(sPathAndFile,'r')
       return file
       
    except Exception as e:
       sError = "An unexpected error has occurred. " + str(e)    
       print("fFileOpenTextMode - Error: " + sError)
       return ""

#------------------------------------------------------------------------------------
# fFileOpenTextModeAndRead => Open file in Text Mode for Reading
#---------------------------------------------------------
def fFileOpenTextModeAndRead(sPathAndFile):
    
    file = fFileOpenTextMode(sPathAndFile)
    if file is None or str(file) == "":
       return ""
    
    err = ""   
    try:
       sData = file.read()
       file.close()
       
       return str(sData)
       
    except IOError(err):
       sError = str(err)
       print("fFileOpenTextModeAndRead - Error: " + sError)
       return ""

#------------------------------------------------------------------------------------
# fFileOpenBinaryMode => Open file in Binary Mode for Reading
#---------------------------------------------------------
def fFileOpenBinaryMode(sPathAndFile):
    
    if sPathAndFile=="":
       return ""

    if not file_FileExists(sPathAndFile):
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
# file_joinPaths => 
# Add slash if it is needed, depening on OS 
#---------------------------------------------------------------------------------------------------------
def file_joinPaths(sPath1, sPath2):
    if sPath1 == "":
        return sPath2
    
    if sPath2 == "":
        return sPath1
    
    return os.path.join(sPath1, sPath2)

#---------------------------------------------------------------------------------------------------------
# file_joinPathList => 
# Add slash if it is needed, depening on OS for a LIST of Paths
#---------------------------------------------------------------------------------------------------------
def file_joinPathList(lstPaths):
    sReturn = ""

    if len(lstPaths) == 1:
        return lstPaths[0]

    if len(lstPaths) < 1:
        return sReturn
    
    if len(lstPaths) % 2 != 0:
        lstPaths.append(sReturn)
     
    n = 0
    while n < len(lstPaths):
          sReturn = sReturn + file_joinPaths(lstPaths[n], lstPaths[n+1])
          n = n + 2

    return sReturn

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
    sPath, sFileName, sExt, sParent = file_PathAndFile_GetSeparated(sPathAndFile)
    return sPath

#---------------------------------------------------------------------------------------------------------
# file_PathAndFile_GetParent
#---------------------------------------------------------------------------------------------------------
def file_PathAndFile_GetParent(sPathAndFile):
    sPath, sFileName, sExt, sParent = file_PathAndFile_GetSeparated(sPathAndFile)
    return sParent

#---------------------------------------------------------------------------------------------------------
# file_GetPath_From_Next
# This method separates the following:
# Example 1:
#           sPathAndOrFile => D:\Temp\Outputs\Siprocal\loci_answers_2025-09-05_10-26_Mexico_V3.txt
#           sPathFrom => D:\Temp\Outputs\
#           Returns => 
#                     sPath = D:\Temp\Outputs\Siprocal
#                     sNext = Siprocal\
#                     sSlash = \
# Example 2:
#           sPathAndOrFile => D:/Temp/vbp/GSMApp/Digitel-Ricardo/Backup/DIG00071.inp
#           sPathFrom => D:/Temp/vbp/GSMApp
#           Returns => 
#                     sPath = D:/Temp/vbp/GSMApp/Digitel-Ricardo/Backup/
#                     sNext = Digitel-Ricardo/Backup/
#                     sSlash = /
#---------------------------------------------------------------------------------------------------------
def file_GetPath_From_Next(sPathAndOrFile, sPathFrom):
    sPath, sFileName, sExt, sParent = file_PathAndFile_GetSeparated(sPathAndOrFile)

    sSlash = file_getFileSlash(sPath)

    #print("file_PathAndFile_GetPath_From - sPathAndFile: " + str(sPathAndFile) + " - sPathFrom = " + str(sPathFrom) + " - sPath: " + str(sPath))
    if str_right(sPath, len(sSlash)) == sSlash:
       if str_right(sPathFrom, len(sSlash)) != sSlash:
          sPathFrom = sPathFrom + sSlash

    sNext = ""
    if sPathFrom in sPath and sPathFrom != sPath:
       sNext = str_right(sPath, len(sPath) - len(sPathFrom))
       #print("file_PathAndFile_GetPath_From - len(sPath): " + str(len(sPath)) + " - len(sPathFrom): " + str(len(sPathFrom)))

    #print("file_PathAndFile_GetPath_From - sPath: " + str(sPath))

    return sPath, sNext, sSlash

#---------------------------------------------------------------------------------------------------------
# file_PathAndFile_GetFileName
#---------------------------------------------------------------------------------------------------------
def file_PathAndFile_GetFileName(sPathAndFile):
    sPath, sFileName, sExt, sParent = file_PathAndFile_GetSeparated(sPathAndFile)
    return sFileName

#---------------------------------------------------------------------------------------------------------
# file_PathAndFile_GetFileNameExtension
#---------------------------------------------------------------------------------------------------------
def file_PathAndFile_GetFileNameExtension(sPathAndFile):
    sPath, sFileName, sExt, sParent = file_PathAndFile_GetSeparated(sPathAndFile)
    return sExt

#---------------------------------------------------------------------------------------------------------
# file_getFileSlash => get whether path is with "\"" or with "//"
#---------------------------------------------------------------------------------------------------------
def file_getFileSlash(sPathAndFile):

    if file_slashdouble in sPathAndFile:
        return file_slashdouble
    
    return file_slash

#---------------------------------------------------------------------------------------------------------
# file_checkSlashDuplicated => check whethere there is slash "////" or "\\" so that 1 is removed.
#---------------------------------------------------------------------------------------------------------
def file_checkSlashDuplicated(sPath):

    sSlash = file_getFileSlash(sPath)

    sDoubleSlash = sSlash + sSlash

    #print("file_checkSlashDuplicated - sPath: " + str(sPath) + " - Slash: " + str(sSlash) + " - Double Slash: " + str(sDoubleSlash))

    if sDoubleSlash in sPath:
        sPath = str_Replace(sPath, sDoubleSlash, sSlash)

    #print("file_checkSlashDuplicated - sPath: " + str(sPath))
    return sPath

#---------------------------------------------------------------------------------------------------------
# file_addSlashToPathIfNeeded => add slash "//" or "\" at the end of path if there is not
#---------------------------------------------------------------------------------------------------------
def file_addSlashToPathIfNeeded(sPath):

    sSlash = file_getFileSlash(sPath)

    if str_right(sPath, len(sSlash)) != sSlash:
       sPath = sPath + sSlash

    #CLEAN DUPLICATED SLASH IF IT IS NEEDED
    sPath = file_checkSlashDuplicated(sPath)

    return sPath             

#---------------------------------------------------------------------------------------------------------
# file_PathAndFile_GetSeparated
# Path and File Name to process
# Returns for input "D:\Temp\Outputs\CTI20444.sec.xml":
#         sPath => D:\Temp\Outputs\
#         sFileName => CTI20444.sec.xml
#         sExt => xml
#         sParent => Outputs\
#---------------------------------------------------------------------------------------------------------
def file_PathAndFile_GetSeparated(sPathAndFile):
    
    tFiles = []
    
    sPath = ""
    sFileName = ""
    
    sSepara = file_getFileSlash(sPathAndFile)
    #print("file_PathAndFile_GetSeparated - sSepara = " + str(sSepara))
    tFiles = sPathAndFile.split(sSepara)
    
    sParent = ""
    if len(tFiles) > 0:
       n = 0 
       while n < len(tFiles)-1:
             sPath = sPath + tFiles[n] + sSepara
             sParent = tFiles[n]
             n = n + 1
       sFileName = tFiles[len(tFiles)-1]    
     
    #print("file_PathAndFile_GetSeparated - sPathAndFile = " + str(sPathAndFile))
    #print("file_PathAndFile_GetSeparated - sPath = " + str(sPath))
    #print("file_PathAndFile_GetSeparated - sFile = " + str(sFile))

    sExt = ""
    if sFileName != "":
       lstExt = sFileName.split(".")
       if len(lstExt) > 1:
           sExt = lstExt[len(lstExt)-1]

    #print("file_PathAndFile_GetSeparated - sExt = " + str(sExt))

    return sPath, sFileName, sExt, sParent      
    
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
       sError = sError + str(err).upper()

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

    return sError


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
                sTemp = file_formatFilePathWithSlash(sRoot + sSlash + str(files[m]))
                #print("file_getDirsAndFiles - FILES sTemp = " + str(sTemp))
                lstFiles.append(sTemp)
                m = m + 1

    return sorted(lstFiles)

#---------------------------------------------------------------------------------------------------------
# file_getFileState
#---------------------------------------------------------------------------------------------------------
def file_getFileState(sPathAndFile, sLogFile=""):

    bReturn = True
    file_size = ""
    creation_date = ""
    modification_date = ""
    access_date = ""
    bDirectory = False

    try:
       
       if file_FileExists(sPathAndFile):
          file_stats = os.stat(sPathAndFile)

          file_size = file_stats.st_size
          creation_date = datetime.fromtimestamp(file_stats.st_ctime)
          modification_date = datetime.fromtimestamp(file_stats.st_mtime)
          access_date = datetime.fromtimestamp(file_stats.st_atime)

          if file_Is_a_Directory(sPathAndFile):
             bDirectory = True

       else:
           file_Error_handlerWithDes("", sLogFile, "Error: File not found at " + str(sPathAndFile))
           bReturn = False   

       return bReturn, str(file_size), str(creation_date), str(modification_date), str(access_date), bDirectory

    except FileNotFoundError:
       file_Error_handlerWithDes("", sLogFile, "Error: File not found at " + str(sPathAndFile))
       return False, str(file_size), str(creation_date), str(modification_date), str(access_date), bDirectory

    except Exception as e:
       file_Error_handlerWithDes(e, sLogFile, "Getting stats for " + str(sPathAndFile))
       return False, str(file_size), str(creation_date), str(modification_date), str(access_date), bDirectory

#---------------------------------------------------------------------------------------------------------
# file_createPandaDicWithFileLstAddingStats
#---------------------------------------------------------------------------------------------------------
def file_pandasFileRecord_CreateDicWithFileLstAddingStats(lstFiles, lstFilesFrom, bSort=False, bSortByName=True):
    
    files = []

    n = 0
    while n < len(lstFiles):

         if (n % file_nRefresh) == 0:
             log_writeWordsInColorMagenta("Preparing data for Pandas Data Frame: " + str_CalculateNofTotal(n, len(lstFiles)))

         #print("file_createPandaDicWithFileLstAddingStats = file " + str(n) + " : " + str(lstFiles[n]))

         if file_FileExists(lstFiles[n]):
             
             #print("file_createPandaDicWithFileLstAddingStats = file " + str(n) + " : " + str(lstFiles[n]) + " - EXISTS = TRUE")
             bFound, file_size, creation_date, modification_date, access_date, bDirectory = file_getFileState(lstFiles[n])

             if bFound and file_size != "":
               # SAVE IN A DICT 
               file_record = {}
               file_record[file_dic_path_file] = str(lstFiles[n])
               file_record[file_dic_size] = str(file_size)
               file_record[file_dic_creation_date] = str(creation_date)
               file_record[file_dic_modification_date] = str(modification_date)
               file_record[file_dic_access_date] = str(access_date)
               file_record[file_dic_directory_type] = str(bDirectory)

               sPath, sFileName, sExt, sParent = file_PathAndFile_GetSeparated(file_record[file_dic_path_file])
               file_record[file_dic_path] = str(sPath)
               file_record[file_dic_fileparent] = str(sParent)
               file_record[file_dic_filename] = str(sFileName)
               file_record[file_dic_fileext] = str(sExt)

               #USED FOR COPY FILES SO THAT IT IS SAVED WHETHER IT STARTS FROM SUBDIRECTORY
               file_record[file_dic_path_subdir] = ""
               #print("file_createPandaDicWithFileLstAddingStats - lstFilesFrom: " + str(lstFilesFrom[n]))
               if len(lstFilesFrom) > 0 and n < len(lstFilesFrom):
                   file_record[file_dic_path_subdir] = str(lstFilesFrom[n])

               #USED FOR COPY FILES SO THAT IT IS SAVED THE DESTINATION PATH WHEN IT IS COPIED
               file_record[file_dic_path_to] = ""
               file_record[file_dic_status] = ""

               files.append(file_record)

         n = n + 1
    
    log_writePrintOnlyWarning("Creating Pandas Data Frame with files list. Total items: " + str(len(files)))
    dfFiles = pd.DataFrame(files)
    #DROP DUPLICATES
    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html
    # inplace=True => Remove duplicates in the original DataFrame
    # subset=[file_dic_path_file] => Keep the first occurrence of rows with duplicate 'Name' and 'City'
    # keep='last' => Keep the last occurrence of entirely duplicate rows - if subset is defined, this should not be defined.
    nItemsBefore = len(dfFiles)
    log_writePrintOnlyWarning("Removing Pandas Data Frame duplicates. Total items BEFORE: " + str(len(dfFiles)))
    dfFiles.drop_duplicates(subset=[file_dic_path_file],inplace=True)
    nItemsAfter = len(dfFiles)
    log_writePrintOnlyWarning("Removing Pandas Data Frame duplicates. Total items AFTER: " + str(len(dfFiles)) + " - Removed: " + str(nItemsAfter - nItemsBefore))

    if bSort:
       if bSortByName and len(files) > 0:
          dfFiles = file_PandasDicSorted(dfFiles, file_dic_path_file, True)
       else:
          dfFiles = file_PandasDicSorted(dfFiles, file_dic_size)
            
        
    return dfFiles

#---------------------------------------------------------------------------------------------------------
# file_pandasFileRecord_get
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_get(df_row, nItem):
    #print("nItem [ " + str(nItem) + ": file_pandasFilefile_pandasFileRecord_getRecord_get - df_row = " + str(df_row) + " - nItem = " + str(nItem))
    # For a row, the first item is the index
    if nItem >= 0 and nItem < len(df_row):
        #print("file_pandasFilefile_pandasFileRecord_getRecord_get - nItem [ " + str(nItem) + "]: df_row[nItem] = " + str(df_row[nItem]) + " - nItem = " + str(nItem))
        #It starts with 1 for nItem because of index is zero reference df_row[0]
        #print("file_pandasFilefile_pandasFileRecord_getRecord_get - nItem [ " + str(nItem) + "]: df_row[0]: " + str(df_row[0]))
        nItem = nItem + 1
        #print("file_pandasFilefile_pandasFileRecord_getRecord_get - df_row[nItem+1] = " + str(df_row[nItem+1]) +  " - df_row[nItem-1] = " + str(df_row[nItem-1]))
        sReturn = df_row[nItem]
        #print("file_pandasFilefile_pandasFileRecord_getRecord_get - sReturn: " + str(sReturn))
        return sReturn
    else:
        return ""

#---------------------------------------------------------------------------------------------------------
# file_dic_pandasFileRecord_getByDF
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_getByDF(df, nRowIndex, nColumn):
    tShape = df.shape
    nRows = tShape[0]
    nCols = tShape[1]
    nRowIndex = int(nRowIndex)
    nColumn = int(nColumn)

    #For a column, to set a value it is not being taken into account the index because it is not updatable
    #Column starts with 0 (zero)

    #print("file_pandasFileRecord_set - nRows = " + str(nRows) + " - nCols = " + str(nCols) + " - nRowIndex = " + str(nRowIndex) + " - nColumn = " + str(nColumn) + " sValue = " + str(sValue))
    if nColumn >= 0 and nColumn <= nCols and nRowIndex >= 0 and nRowIndex <= nRows:
        #print("df before: " + str(df.iloc[nRowIndex, nColumn]))
        sReturn = df.iloc[nRowIndex, nColumn]
        return sReturn
        #print("df after: " + str(df.iloc[nRowIndex, nColumn]))
    return ""

#---------------------------------------------------------------------------------------------------------
# file_pandasFileRecord_set
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_set(df, nRowIndex, nColumn, sValue):
    tShape = df.shape
    nRows = tShape[0]
    nCols = tShape[1]
    nRowIndex = int(nRowIndex)
    nColumn = int(nColumn)

    #For a column, to set a value it is not being taken into account the index because it is not updatable
    #Column starts with 0 (zero)

    #print("file_pandasFileRecord_set - nRows = " + str(nRows) + " - nCols = " + str(nCols) + " - nRowIndex = " + str(nRowIndex) + " - nColumn = " + str(nColumn) + " sValue = " + str(sValue))
    if nColumn >= 0 and nColumn <= nCols and nRowIndex >= 0 and nRowIndex <= nRows:
        #print("df before: " + str(df.iloc[nRowIndex, nColumn]))
        df.iloc[nRowIndex, nColumn] = sValue
        #print("df after: " + str(df.iloc[nRowIndex, nColumn]))
        return True
    return False   

#---------------------------------------------------------------------------------------------------------
# file_pandasFileRecord_get_path_file
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_get_path_file(df_row):
    return file_dic_pandasFileRecord_get(df_row, file_dic_path_file_nro)

#---------------------------------------------------------------------------------------------------------
# file_pandasFileRecord_get_path_to
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_get_path_to(df_row):
    return file_dic_pandasFileRecord_get(df_row, file_dic_path_to_nro)

#---------------------------------------------------------------------------------------------------------
# file_pandasFileRecord_get_path_from
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_get_path_subdir(df_row):
    return file_dic_pandasFileRecord_get(df_row, file_dic_path_subdir_nro)

#---------------------------------------------------------------------------------------------------------
# file_pandasFileRecord_get_fileext
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_get_fileext(df_row):
    return file_dic_pandasFileRecord_get(df_row, file_dic_fileext_nro)

#---------------------------------------------------------------------------------------------------------
# file_dic_pandasFileRecord_get_path_file_parent
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_get_file_parent(df_row):
    return file_dic_pandasFileRecord_get(df_row, file_dic_fileparent_nro)

#---------------------------------------------------------------------------------------------------------
# file_dic_pandasFileRecord_get_status
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_get_status(df, nRow):
    return file_dic_pandasFileRecord_getByDF(df, nRow, file_dic_status_nro)

#---------------------------------------------------------------------------------------------------------
# file_pandasFileRecord_set_status
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_set_status(df, nRow, sValue):
    return file_dic_pandasFileRecord_set(df, nRow, file_dic_status_nro, sValue)

#---------------------------------------------------------------------------------------------------------
# file_dic_pandasFileRecord_set_file_dic_path_subdir
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_set_file_dic_path_subdir(df, nRow, sValue):
    return file_dic_pandasFileRecord_set(df, nRow, file_dic_path_subdir_nro, sValue)

#---------------------------------------------------------------------------------------------------------
# file_pandasFileRecord_set_path_to
#---------------------------------------------------------------------------------------------------------
def file_dic_pandasFileRecord_set_path_to(df, nRow, sValue):
    return file_dic_pandasFileRecord_set(df, nRow, file_dic_path_to_nro, sValue)

#---------------------------------------------------------------------------------------------------------
# file_dicSortedBySize
#---------------------------------------------------------------------------------------------------------
def file_PandasDicSorted(df, sSortField, bSortMaxToMin=True):

    bAscending = False
    if bSortMaxToMin:
       bAscending = True
        
    df_sorted = df
    if len(df) > 0:
        df_sorted = df.sort_values(by=sSortField, ascending=bAscending)

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

#---------------------------------------------------------------------------------------------------------
def file_OpenNotePadInMac(sText, sPath=""):
    return file_OpenNotePadInWindows(sText, sPath)

#---------------------------------------------------------------------------------------------------------
def file_OpenNotePadInWindows(sText, sPath=""):
    if sText != "":
       try:
           if file_IsOSLinux():
              print("file_OpenNotePadInWindows - OS: Linux. sText:\n\n" + str(sText))
           else:    
              
              temp_filename = "temp_data.txt"
              if sPath!="":
                 temp_filename = os.path.join(sPath,temp_filename)

              #print("temp_filename = " + str(temp_filename))
           
              with open(temp_filename, "w") as f:
                  f.write(sText)

              file_OpenFileWithNotepadInWindows(temp_filename)

           return True
       
       except Exception as e:
             sError = "An unexpected error has occurred. " + str(e)    
             print("file_OpenNotePadInWindows - Error: " + sError)
             return False
        
#---------------------------------------------------------------------------------------------------------
def file_OpenFileWithNotepadInWindows(sPathFileName):

    if file_IsOSWindows():    
       subprocess.Popen(["notepad.exe", sPathFileName])
    else:
       if file_IsOSMac():
          subprocess.run(["open", str(sPathFileName)], check=False)
       else:
           #LINUX OS NOT SUPPORTED FOR OPENING NOTEPAD.EXE
           return False

    return True      

#---------------------------------------------------------------------------------------------------------
# file_mkDir
#---------------------------------------------------------------------------------------------------------
def file_mkDir(sPathSource):

    sProcess = "Creating Directory: "

    try:

        if sPathSource == "":
            return False, sProcess + "No path to create. Path: '" + sPathSource + "'"

        if file_Is_a_Directory(sPathSource):
            return False, sProcess + "Path already exists. Source: '" + sPathSource + "'"

        os.makedirs(sPathSource)

        return True, ""
    
    except Exception as e:
       sError = file_Error_handlerWithDes(e, "", sProcess + "Trying to create a directory. Path: '" + sPathSource + "'")
       return False, sError


#---------------------------------------------------------------------------------------------------------
# file_rmDir
#---------------------------------------------------------------------------------------------------------
def file_rmDir(sPathSource):

    sProcess = "Deleting Directory: "

    try:

        if sPathSource == "":
            return False, sProcess + "No path to remove. Path: '" + sPathSource + "'"

        if not file_Is_a_Directory(sPathSource):
            return False, sProcess + "File is not a directory. Source: '" + sPathSource + "'"

        # Change the file permission to allow writing (removes read-only flag)
        os.chmod(sPathSource, stat.S_IWRITE)

        # Now attempt to remove the file
        os.rmdir(sPathSource)

        return True, ""
    
    except Exception as e:
       sError = file_Error_handlerWithDes(e, "", sProcess + "Trying to remove a directory. Path: '" + sPathSource + "'")
       return False, sError
#---------------------------------------------------------------------------------------------------------
# file_copy
#---------------------------------------------------------------------------------------------------------
def file_copy(sPathFileSource, sPathFileDestination):

    sProcess = "Copying Files: "
    try:

        if sPathFileSource == "" or sPathFileDestination == "":
            return False, sProcess + "No file for copy. Source: '" + sPathFileSource + "', Destination: '" + sPathFileDestination + "'"

        if not file_FileExists(sPathFileSource):
            return False, sProcess + "File to copy does not exist. Source: '" + sPathFileSource + "', Destination: '" + sPathFileDestination + "'"

        bReturn = True
        sError = ""

        if file_Is_a_Directory(sPathFileSource):
           bReturn, sError = file_mkDir(sPathFileDestination)
        else:

           sPathDestination = file_PathAndFile_GetPath(sPathFileDestination)
           if not file_FileExists(sPathDestination):
              bReturn, sError = file_mkDir(sPathDestination)
              if not bReturn:
                  return False, sProcess + "Destination path does not exist and it cannot be created. Destination Path: " + sPathDestination + ". ERROR: " + sError
 
           #https://stackoverflow.com/questions/123198/how-do-i-copy-a-file
           shutil.copy2(sPathFileSource, sPathFileDestination)

        return bReturn, sError
    
    except Exception as e:
       sError = file_Error_handlerWithDes(e, "", sProcess + "Trying to copy file. From: '" + sPathFileSource + "' - To: '" + sPathFileDestination + "'")
       return False, sError


#---------------------------------------------------------------------------------------------------------
# file_delete
#---------------------------------------------------------------------------------------------------------
def file_delete(sPathFileSource):

    sProcess = "Deleting File: "

    try:
   
        if sPathFileSource == "":
            return False, sProcess + "Delete File: No file for deletion. File: '" + sPathFileSource + '"'
        
        if file_Is_a_Directory(sPathFileSource):
            return False, sProcess + file_dic_status_warning_dir + ": It is a directory. It must be removed as a directory with rmdir, not delete command. Path: '" + sPathFileSource + "'"
        
        if os.path.exists(sPathFileSource):
           
           # Change the file permission to allow writing (removes read-only flag)
           os.chmod(sPathFileSource, stat.S_IWRITE)

           # Now attempt to remove the file
           os.remove(sPathFileSource)

        return True, ""
    
    except Exception as e:
       sError = file_Error_handlerWithDes(e, "", sProcess + "Delete File: Trying to delete file '" + sPathFileSource + "'")
       return False, sError

#---------------------------------------------------------------------------------------------------------
# file_compare
# Returns:
#         True => They are equal
#         False => They are different
#         Difference  
#---------------------------------------------------------------------------------------------------------
def file_compare(sPathFileSource, sPathFileDestination, bValidateDateCreation=False):

    sProcess = "Compating Files: "
    sError = sProcess + "Source = '" + sPathFileSource + "', Destination = '" + sPathFileDestination + "'. ERROR: "

    try:

        if sPathFileSource == "" or sPathFileDestination == "":
            return False, sError + "No file for comparing"

        bFromExists, sFromFileSize, sFromFileDateCreation, sFromFileDateModif, sFromFileDateAccess, bFromDirectory = file_getFileState(sPathFileSource, "")
        bToExists, sToFileSize, sToFileDateCreation, sToFileDateModif, sToFileDateAccess, bToDirectory = file_getFileState(sPathFileDestination, "")

        if not bFromExists:
            return False, sError + "Source file '" + sPathFileSource + "' does not exist."

        if not bToExists:
            return False, sError + "Destination file '" + sPathFileDestination + "' does not exist."

        if bFromDirectory:
            return False, sError + "Source '" + sPathFileSource + "' is a direcory not to be compared."
        if bToDirectory:
            return False, sError + "Destination '" + sPathFileDestination + "' is a direcory not to be compared."

        sDif = ""
        if sFromFileSize != sToFileSize:
            sDif = sDif + " Source file Size '" + sFromFileSize + "' is different from Destination file Size '" + sToFileSize + "'."
        if bValidateDateCreation:    
           if sFromFileDateCreation != sToFileDateCreation:
              sDif = sDif + " Source file Date Creation '" + sFromFileDateCreation + "' is different from Destination file Date Creation '" + sToFileDateCreation + "'."
        if sFromFileDateModif != sToFileDateModif:
            sDif = sDif + " Source file Date Modification '" + sFromFileDateModif + "' is different from Destination file Date Modification '" + sToFileDateModif + "'."
        if sFromFileDateAccess != sToFileDateAccess:
            sDif = sDif + " Source file Date Access '" + sFromFileDateAccess + "' is different from Destination file Date Access '" + sToFileDateAccess + "'."

        if sDif != "":
            return False, sError + sDif
            
        return True, ""
    
    except Exception as e:
       sError = file_Error_handlerWithDes(e, "", sProcess + "Trying to copy file. From: '" + sPathFileSource + "' - To: '" + sPathFileDestination + "'")
       return False, sError

#---------------------------------------------------------------------------------------------------------
# file_getSubDirFromPath
# Example:
#         1)
#         sPathFile: D:\Temp\vbp\GSMApp\Temp\DatabaseRead\mdbplus.ini
#         sPattern: D:\Temp\vbp\GSMApp\
#         bRemoveFileName = True
#         2)
#         sPathFile: D:/Temp/vbp/GSMApp/Digitel-Ricardo/Backup/DIG00071.inp
#         sPattern: D:/Temp/vbp/GSMApp
#         bRemoveFileName = True        
# Returns:
#         1)
#         Temp\DatabaseRead\
#         2)
#         /Digitel-Ricardo/Backup/
#---------------------------------------------------------------------------------------------------------
def file_getSubDirFromPath(sPathFile, sPattern, bRemoveFileName=True):
    sReturn = ""

    sSlash = file_getFileSlash(sPathFile)

    #print("file_getSubDirFromPath - sPathFile: " + str(sPathFile) + " - sPattern: " + str(sPattern))
    if sPattern in sPathFile:
       sReturn = str_midToEnd(sPathFile, len(sPattern))
       #print("file_getSubDirFromPath - sReturn: " + str(sReturn))

       if bRemoveFileName and sReturn != "":
           sReturnT = file_PathAndFile_GetFileName(sReturn)
           if sReturnT != "":
               sReturn = str_getSubStringFromOcur(sReturn, sReturnT, 0)

    #print("file_getSubDirFromPath - sReturn: " + str(sReturn))

    #FOR TESTING
    #sFile = str("D:/Temp/vbp/GSMApp/Digitel-Ricardo/Backup/DIG00071.inp")
    #sPattern = str("D:/Temp/vbp/GSMApp")
    #sTemp = file_getSubDirFromPath(sFile, sPattern)
    #print("sFile: " + str(sFile) + " - sPattern: " + str(sPattern) + " - sResult: " + str(sTemp))
    #exit(0)

    if sReturn == sSlash:
        sReturn = ""

    return sReturn

#---------------------------------------------------------------------------------------------------------
# files_IsUserAdmin_OnlyWindows
# Verifies whether the final user is Administrator
# Returns:
#        True => Is Administrator
#        False => Not Administrator or not in Windows.
#---------------------------------------------------------------------------------------------------------
def files_IsUserAdmin_OnlyWindows():

    bAdmin = False
    try:

        if file_IsOSWindows():
           
           #Return Values
           # Non-zero integer (e.g., 1): The current user context has administrative privileges (is an admin).
           # Zero (0): The current user context does not have administrative privileges. 
           bAdmin = ctypes.windll.shell32.IsUserAnAdmin()
           
           #print("files_IsUserAdmin_OnlyWindows - bAdmin: " + str(bAdmin))

        return bAdmin != 0, ""
    
    except Exception as e:
       sError = file_Error_handlerWithDes(e, "", "User '" + files_getUserName() + "' is NOT Administrator. This works only in Windows.")
       return False, sError

#---------------------------------------------------------------------------------------------------------
# files_getUserName
# Get user name in all platforms
# Returns: Username
#---------------------------------------------------------------------------------------------------------
def files_getUserName():
    username = getpass.getuser()
    return username

#---------------------------------------------------------------------------------------------------------
# check_admin_group_membership
# Check whether username is member of administrators
# Returns: True is member, False is not member
#---------------------------------------------------------------------------------------------------------
#python -m pip install pywin32
import win32net
import platform
import getpass
def check_admin_group_membership():
    hostname = platform.uname()[1]
    username = getpass.getuser()
    is_admin = False

    # Iterate through the local groups the user belongs to
    for group_info in win32net.NetUserGetLocalGroups(hostname, username):
        if group_info[0].lower() == 'administrators':
            is_admin = True
            break
            
    if is_admin:
        print(f"User '{username}' is a member of the Administrators group.")
    else:
        print(f"User '{username}' is a Standard user (not in Administrators group).")

    return is_admin    

#------------------------------------------------------------------------------------
