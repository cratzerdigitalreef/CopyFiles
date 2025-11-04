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
def process_CopyFiles(logFile, lstSource, lstDestination, bCancelByError=False):
    
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

    sSlash = ""

    #GETTING ALL PATHs AND FILEs    
    lstFiles = []
    lstFilesPathNext = []
    n = 0
    nSource = len(lstSource)

    while n < nSource:

          lstSource[n]= file_fNormalPathForWindowsLinux(lstSource[n])
          print("Processing source: " + str(n) + " - " + str(lstSource[n]))

          lstFilesTemp = process_CopyFiles_GetDirsAndFiles(lstSource[n], logFile)
          if len(lstFilesTemp) > 0:

              m = 0
              while m < len(lstFilesTemp):
                    if lstFilesTemp[m] not in lstFiles:

                       #ADDED FOR FILES TO BE PROCESSED
                       lstFilesTemp[m] = file_fNormalPathForWindowsLinux(lstFilesTemp[m])
                       lstFiles.append(lstFilesTemp[m])

                       if file_Is_a_Directory(lstFilesTemp[m]):
                          #print("process_CopyFiles - Added new directory for source: " + str(lstFilesTemp[m]))
                          lstSource.append(lstFilesTemp[m])
                          nSource = len(lstSource)

                       sPath, sPathNext = file_GetPath_From_Next(lstFilesTemp[m], lstSource[n])
                       #ADDED FOR SOURTH PATH FOR FILES TO BE PREOCESSED
                       #print("process_CopyFiles - file " + str(m) + ": " + str(lstFilesTemp[m]) + " - Directory for source " + str(n) + ": " + str(sPathNext))
                       lstFilesPathNext.append(sPathNext) 

                    m = m + 1
    
          n = n + 1 

    log_write_Normal(logFile, "Total Files records before Pandas = " + str(len(lstFiles)) + " from: " + str(len(lstFilesPathNext)))

    #PREPARING A PANDAS DICT WITH THE PREVIOUS LIST
    dict_df_file = file_createPandaDicWithFileLstAddingStats(lstFiles, lstFilesPathNext)

    #GENERATE A CSV FILE WITH PANDAS DF
    today = datetime.now()
    today_prn = today.strftime("%Y-%m-%d")
    sDFFile = "CopyFiles" + "_" + today_prn + "csv"
    if logFile != "":
         sDFFile = logFile + "_DF.csv"
    dict_df_file.to_csv(sDFFile, index=True)

    #START PROCESS
    dict_df_file_cols = dict_df_file.columns.tolist()
    rows, cols = dict_df_file.shape 
    log_write_Normal(logFile, "Pandas Columns header = " + str(dict_df_file_cols) + " Total Columns=" + str(cols))
    log_write_Normal(logFile, "Total records with Pandas = " + str(rows))

    nCols = 0
    n = 0
    for row1 in dict_df_file.itertuples():

          if sSlash == "":
             #GET SLASH ONLY ONCE
             sSlash = file_getFileSlash(lstSource[n])

          #FIRST FIELD IS THE RECORD NUMBER, NEXT RECORD IS THE PATH/FILE
          #LAST FIELD IS THE PATH FROM WHERE IT IS ANALIZED
          sPathFileFrom = str(row1[1])
          sPathFileNext = str(row1[len(row1)-1])

          print("\nFile " + str(n) + ": " + sPathFileFrom + " - Path From: " + sPathFileNext)
          sPrint, sFileSize, sFileDateCreation, sFileDateModif, sFieDateAccess = process_CopyFiles_DirFileStatus(sPathFileFrom, logFile)
          sPrint = "\n" + str(n) + " File: " + sPrint
          log_write_Normal(logFile, sPrint)

          m = 0
          while m < len(lstDestination):

              sPathFileTo = lstDestination[m]
              print("\nCopying File " + str(n) + ": " + sPathFileFrom + " - to: " + sPathFileTo)
              
              bError, sError = process_CopyFiles_CopyFromTo(sPathFileFrom, sPathFileTo, sPathFileNext, logFile)
              if bError and bCancelByError:
                  m = len(lstDestination)

              m = m + 1

          n = n + 1 


    return True, ""

# process_CopyFiles_GetDirsAndFiles ----------------------------------------------------------------------------------------------------------
def process_CopyFiles_GetDirsAndFiles(sPathFile, logFile=""):
    lstFilesTemp = []
    if file_Is_a_Directory(sPathFile):
       lstFilesTemp = file_getDirsAndFiles(sPathFile, logFile)
       nFound = len(lstFilesTemp)
       print("process_CopyFiles_GetDirsAndFiles - found for path: " + str(sPathFile) + "' = " + str(nFound))
    else:
       print("process_CopyFiles_GetDirsAndFiles - path: '" + str(sPathFile) + "' not a DIRECTORY!")
           
    return lstFilesTemp

    
# process_CopyFiles_DirFileStatus ----------------------------------------------------------------------------------------------------------
def process_CopyFiles_DirFileStatus(sFile, logFile=""):

    bExists, sFileSize, sFileDateCreation, sFileDateModif, sFieDateAccess = file_getFileState(sFile, logFile)
    
    sPrint = sFile
    if bExists:
       sPrint = sPrint + "\nSize: " + sFileSize + " bytes"
       sPrint = sPrint + "\nCreation Date: " + sFileDateCreation
       sPrint = sPrint + "\nLast Modification Date: " + sFileDateModif
       sPrint = sPrint + "\nLast Access Date: " + sFieDateAccess

       sPrint = sPrint + "\nDirectory: " + str(file_Is_a_Directory(sFile))
    else:
        sPrint = sPrint + "\nIt does not exist or there is an error."   
    
    return sPrint, sFileSize, sFileDateCreation, sFileDateModif, sFieDateAccess
   
# process_CopyFiles_CopyFromTo ----------------------------------------------------------------------------------------------------------
def process_CopyFiles_CopyFromTo(sFilePath, sPathTo, sPathNext, logFile=""):

    bReturn = True
    sError = ""

    bFromExists, sFromFileSize, sFromFileDateCreation, sFromFileDateModif, sFromFieDateAccess = file_getFileState(sFilePath, logFile)
    
    if not bFromExists:
        sError = "File 'FROM' does not exist. File From: " + sFilePath
        if logFile != "":
           log_write_Normal(logFile, sError)
        else:
           print(sError)    
        return False, ""

    sPath, sFileName, sExt = file_PathAndFile_GetSeparated(sFilePath)

    sPathTo = file_addSlashToPathIfNeeded(sPathTo)
    if sPathNext != "":
        sPathTo = sPathTo + sPathNext
    sPathTo = file_addSlashToPathIfNeeded(sPathTo)

    sToPathFile = sPathTo + sFileName

    bToExists, sToFileSize, sToFileDateCreation, sToFileDateModif, sToFieDateAccess = file_getFileState(sToPathFile, logFile)
    
    bToCopy = False

    if bToExists:
        #FILE in DESTINATION EXISTS. It must be analized size and date
        sPrint = "File 'TO' DOES exist. File To: " + sToPathFile
        if logFile != "":
           log_write_Normal(logFile, sPrint)

        bEqual, sError = file_compare(sFilePath, sToPathFile)   
        if not bEqual:
           if logFile != "":
              log_write_Normal(logFile, sError)

           bReturn, sError = file_delete(sToPathFile)
           if not bReturn and logFile != "":
              log_write_Normal(logFile, sError)
           else:
               bToCopy = True 
    else:
        #FILE IN DESTINATION DOES NOT EXIST. It is copied.
        sPrint = "File 'TO' does not exist. File To: " + sToPathFile
        if logFile != "":
           log_write_Normal(logFile, sPrint)
        bToCopy = True 

    if bToCopy:
        bReturn, sError = file_copy(sFilePath, sToPathFile) 
        if not bReturn and logFile != "":
           log_write_Normal(logFile, sError)

    return bReturn, sError
   

# --------------------------------------------------------------------------------------------------------------------------------------------------------
