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


    #GETTING ALL PATHs AND FILEs    
    lstFiles = []
    n = 0
    while n < len(lstSource):
          lstFilesTemp = []
          lstFilesTemp = file_getDirsAndFiles(lstSource[n], logFile)
         
          lstFiles.extend(lstFilesTemp)

          nFound = len(lstFiles)
          print("process_CopyFiles - found for path " + str(n) + " = " + str(nFound))

          n = n + 1 

    #PREPARING A PANDAS DICT WITH THE PREVIOUS LIST
    dict_df_file = file_createPandaDicWithFileLstAddingStats(lstFiles, False)
    dict_df_file_cols = dict_df_file.columns.tolist()
    rows, cols = dict_df_file.shape 
    print("Columns header = " + str(dict_df_file_cols) + " Total Columns=" + str(cols))
    print("Total records = " + str(rows))

    nCols = 0
    n = 0
    for row1 in dict_df_file.itertuples():

          print("File: " + str(n) + " - " + str(row1))          
          sPrint, sFileSize, sFileDateCreation, sFileDateModif, sFieDateAccess = process_CopyFiles_DirFileStatus(row1[1], logFile)
          sPrint = "\n" + str(n) + " File: " + sPrint
          log_write_Normal(logFile, sPrint)
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
