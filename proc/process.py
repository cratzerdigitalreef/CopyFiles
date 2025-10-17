# -*- coding: UTF-8 -*-

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(current)
sys.path.append(parent_directory+"/libs")
sys.path.append(parent_directory+"/constants")

from pathlib import Path
from libs.str import *
from libs.log import *
from libs.files import *

# process_CopyFiles ----------------------------------------------------------------------------------------------------------
def process_CopyFiles(logFile, lstSource, lstDestination):
    
    bProcess = True
    sError = ""
    sWarning = "WARNING !!! "
    if len(lstSource) <= 0:
       bProcess = False
       sError = "There is nothing to process for 'SOURCE'."

    if bProcess:
       if len(lstDestination) <= 0:
          bProcess = False
          sError = "There is nothing to process for 'DESTINATION'."
           
    if not bProcess:   
       sWarning = sWarning + sError
       return False, sWarning

    bDuplicated, sError = file_AreFilesDuplicated(lstSource, lstDestination)
    if bDuplicated:
       sWarning = sWarning + sError
       return False, sWarning

    
    n = 0
    while n < len(lstSource):
          lstFiles = file_getDirsAndFiles(lstSource[n], logFile)

          nFound = len(lstFiles)
          print("process_CopyFiles - found for " + str(n) + " = " + str(nFound))

          #IT IS CREATED A DICTIONARY
          dict_df_file = file_createPandaDicWithFileLstAddingStats(lstFiles)
          sPrint = "process_CopyFiles - dict_df_file " + str(n) + " = " + str(dict_df_file)
          log_write_Normal(logFile, sPrint)
          dict_df_file_size =file_PandasDicSortedBySize(dict_df_file, False)
          sPrint = "process_CopyFiles - dict_df_file_size " + str(n) + " = " + str(dict_df_file_size)
          log_write_Normal(logFile, sPrint)

          #PROCESSING
          m = 0   
          while m < nFound:
                
                #print("process_CopyFiles - lstFiles[m] = " + str(lstFiles[m]))
                sPrint, sFileSize, sFileDateCreation, sFileDateModif, sFieDateAccess = process_CopyFiles_DirFileStatus(lstFiles[m], logFile)
                sPrint = "\n" + str(n) + "." + str(m) + " File: " + sPrint
                #log_write_Normal(logFile, sPrint)
                m = m + 1

          n = n + 1 

    return True, ""

# process_CopyFiles ----------------------------------------------------------------------------------------------------------
def process_CopyFiles_DirFileStatus(sFile, logFile=""):

    sFileSize, sFileDateCreation, sFileDateModif, sFieDateAccess = file_getFileState(sFile, logFile)
    
    sPrint = sFile
    sPrint = sPrint + "\nSize: " + sFileSize + " bytes"
    sPrint = sPrint + "\nCreation Date: " + sFileDateCreation
    sPrint = sPrint + "\nLast Modification Date: " + sFileDateModif
    sPrint = sPrint + "\nLast Access Date: " + sFieDateAccess

    sPrint = sPrint + "\nDirectory: " + str(file_Is_a_Directory(sFile))
    
    return sPrint, sFileSize, sFileDateCreation, sFileDateModif, sFieDateAccess
   


# --------------------------------------------------------------------------------------------------------------------------------------------------------
