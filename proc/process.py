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
from libs.pyqt import *
from libs.files import *
from libs.dt import *

from PyQt5.QtWidgets import QMessageBox, QTextEdit, QFileDialog, QTableView, QPushButton, QVBoxLayout, QProgressBar, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QProgressBar, QVBoxLayout, QWidget

nProcessGblRecord = 0
dtProcessGblStarted = ""
dtProcessGblFinished = ""
dtProcessGblDateTimeFormat = "%Y-%m-%d %H.%M.%S.%f"
#dtProcessGblDateTimeFormat = "%Y-%m-%d %H.%M.%S"
sProcessGblMsg = ""
sProcessEmit = ""
bProcessGblStop = False
bProcessGblRunning = False
nProcessLogNro= 0
sProcessFlagEnded = "ENDED:"


class Worker(QThread):
    """
    A QThread subclass to perform a long-running task.
    Emits signals for progress updates and completion.
    Includes a flag for cancellation.
    """
    signalProgress = pyqtSignal(int, str)
    signalFinished = pyqtSignal(int, bool, str)

    def __init__(self):
        super().__init__()
        self._is_canceled = False

    def config(self, logFile, mainWindow, procWindows, lstSource, lstDestination, bCancelByError=False):
        self._logFile = logFile
        self._mainWindow = mainWindow
        self._procWindows = procWindows
        self._lstSource = lstSource
        self._lstDestination = lstDestination
        self._bCancelByError = bCancelByError

    def progress(self, sMsg):
        self.signalProgress.emit(1, sMsg)

    def run(self):
        """
        The main execution method for the thread.
        Simulates a long-running task with progress updates and cancellation checks.
        """
        #for i in range(1, 101):
        #    if self._is_canceled:
        #        break
        #    time.sleep(0.1)  # Simulate work
        #    self.progress.emit(i)
        #self.finished.emit()
        
        #print("Before process_CopyFiles_sub")

        #print("run:  self._logFile = " + str( self._logFile))
        #print("run:  self._mainWindow = " + str( self._mainWindow))
        #print("run:  self._procWindows = " + str( self._procWindows))
        #print("run:  self._lstSource = " + str( self._lstSource))

        bFinishResult, sFinishResult = process_CopyFiles_sub(self._logFile, self._mainWindow, self._procWindows, self._lstSource, self._lstDestination, self._bCancelByError)
        #print("After process_CopyFiles_sub")
        
        print("run finished: sFinishResult = " + str(sFinishResult))
        self.signalFinished.emit(1, bFinishResult, sFinishResult)

    def cancel(self):
        """
        Sets the internal flag to request cancellation of the task.
        """
        sMsg = "Stop processing ?"
        sMsg = sMsg + "\nRecords: " + str(nProcessGblRecord) + " - at: " + process_GetDateTimeNow()
        sReturn = pyqt_MsgBoxQuestionWithoutParent("Processing", sMsg, False)
        if str(sReturn).upper() == "YES":
           self._is_canceled = True

class processWindow(QMainWindow):
    """
    The main application window, managing the GUI and interacting with the worker thread.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Process Threding")
        self.setGeometry(100, 100, 400, 200)
        pyqt_centerWindow(self)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        #self.label = QLabel("Ready to start task.")
        self.txt = QTextEdit("Ready to start task.")
        self.txt.setReadOnly(True)

        #self.progress_bar = QProgressBar()
        #self.progress_bar.setRange(0, 100)

        #self.start_button = QPushButton("Start Task")
        self.cancel_button = QPushButton("Cancel Process")
        self.cancel_button.setEnabled(True) # Initially enabled

        #self.layout.addWidget(self.label)
        self.layout.addWidget(self.txt)
        #self.layout.addWidget(self.progress_bar)
        #self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.cancel_button)

        self.worker_thread  = Worker()
        self.worker_thread.signalProgress.connect(self.update_progress)
        self.worker_thread.signalFinished.connect(self.task_finished)

        #self.start_button.clicked.connect(self.start_task)
        self.cancel_button.clicked.connect(self.cancel_task)

        self.bFinishResult = True
        self.sFinishResult = ""


    @pyqtSlot()
    def start_task(self, logFile, mainWindow, procWindows, lstSource, lstDestination, bCancelByError=False):
        """
        Initiates the long-running task in the worker thread.
        Updates GUI elements accordingly.
        """
        self.show()

        #self.label.setText("Task running...")
        sMsg = "Task running... at " + process_GetDateTimeNow()
        self.txt.setText(sMsg)
        print(sMsg)
        #self.progress_bar.setValue(0)
        #self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

        #START WORKER
        #print("Before starting worker")

        #print("run:  self._logFile = " + str( logFile))
        #print("run:  self._mainWindow = " + str( mainWindow))
        #print("run:  self._procWindows = " + str(procWindows))
        #print("run:  self._lstSource = " + str( lstSource))

        self.worker_thread.config(logFile, mainWindow, procWindows, lstSource, lstDestination, bCancelByError)
        self.worker_thread.start()
        #print("After starting worker")
        self.update()

    @pyqtSlot(int, str)
    def update_progress(self, value, sMsg):
        """
        Receives progress updates from the worker thread and updates the progress bar.
        """
        #self.progress_bar.setValue(value)
        value = str(value)
        if sMsg == "":
            sMsg = sProcessGblMsg

        print("Before setText - update_progress : sMsg = " + str(sMsg))    
        self.txt.setText(sMsg)
        print("After setText - update_progress : sMsg = " + str(sMsg))    
        print(sMsg)
        #self.update()

    @pyqtSlot(int, bool, str)
    def task_finished(self, number, bFinishResult, sFinishResult):
        """
        Handles the completion of the task, whether naturally or by cancellation.
        Resets GUI elements.
        """
        sTask = ""
        
        print("task_finished")

        if self.worker_thread._is_canceled:
            #self.label.setText("Task canceled.")
            sTask = "canceled"
            self.worker_thread._is_canceled = False # Reset for next run
        else:
            #self.label.setText("Task finished.")
            sTask = "finished"
        #self.start_button.setEnabled(True)
        #self.cancel_button.setEnabled(False)
        sMsg = "Task " + sTask + " ... at " + process_GetDateTimeNow()
        print(sMsg)
        self.txt.setText(sMsg)

        self.bFinishResult = bFinishResult
        self.sFinishResult = sFinishResult

        self.hide()

    @pyqtSlot()
    def cancel_task(self):
        """
        Requests cancellation of the running task in the worker thread.
        """
        self.worker.cancel()
        #self.label.setText("Cancelling task...")
        self.txt.setText("Cancelling task... at " + process_GetDateTimeNow())
        process_GbStop_True()
        #self.cancel_button.setEnabled(False) # Disable while waiting for cancellation


# process_CopyFiles ----------------------------------------------------------------------------------------------------------
def process_CopyFiles(logFile, mainWindow, procWindows, lstSource, lstDestination, bCancelByError=False):
    procWindows.start_task(logFile, mainWindow, procWindows, lstSource, lstDestination, bCancelByError)
    return

# process_CopyFiles_sub ----------------------------------------------------------------------------------------------------------
def process_CopyFiles_sub(logFile, mainWindow, procWindows, lstSource, lstDestination, bCancelByError=False):

    process_GblRecord_Clean()
    process_GblMessage_Clean()
    
    process_GbDateTimeStartedFinished_CleanBoth()
    process_GbDateTimeStartedFinished_Set(True)

    process_GbStop_False()
    process_GbRunning_True()
    
    logFile = file_fNormalPathForWindowsLinux(logFile)

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

    pyqt_windowRefresh(mainWindow)

    #GETTING ALL PATHs AND FILEs    
    lstFiles = []
    lstFilesPathSubdir = []
    n = 0
    nSource = len(lstSource)

    while n < nSource and not bProcessGblStop:

          lstSource[n]= file_fNormalPathForWindowsLinux(lstSource[n])
          sProcessing = "Processing source: " + process_CalculateNofTotal(n, nSource) + " - " + str(lstSource[n])

          print(sProcessing)
          process_EmitMsgProcessing(procWindows, sProcessing)

          process_GblRecord_SumValue()
          process_GblMessage_Set(sProcessing)

          sProcessing = "Processing source: " + process_CalculateNofTotal(n, nSource) + " - " + str(lstSource[n])
          print(sProcessing)

          lstFilesTemp = process_CopyFiles_GetDirsAndFiles(lstSource[n], logFile)
          if len(lstFilesTemp) > 0:

              m = 0
              while m < len(lstFilesTemp) and not bProcessGblStop:
                    if lstFilesTemp[m] not in lstFiles:

                       #ADDED FOR FILES TO BE PROCESSED
                       lstFilesTemp[m] = file_fNormalPathForWindowsLinux(lstFilesTemp[m])
                       lstFiles.append(lstFilesTemp[m])

                       if file_Is_a_Directory(lstFilesTemp[m]):
                          #print("process_CopyFiles - Added new directory for source: " + str(lstFilesTemp[m]))
                          lstSource.append(lstFilesTemp[m])
                          nSource = len(lstSource)

                       sPath, sPathSubdir = file_GetPath_From_Next(lstFilesTemp[m], lstSource[n])
                       #ADDED FOR SOURTH PATH FOR FILES TO BE PREOCESSED
                       #print("process_CopyFiles - file " + str(m) + ": " + str(lstFilesTemp[m]) + " - Directory for source " + str(n) + ": " + str(sPathNext))
                       lstFilesPathSubdir.append(sPathSubdir) 

                       sProcessing = "process_CopyFiles - file " + process_CalculateNofTotal(m, len(lstFilesTemp)) + " : " + str(lstFilesTemp[m]) + " - Directory for source " + str(n) + ": " + str(sPathSubdir)
                       process_GblMessage_Set(sProcessing, True)

                    
                    pyqt_windowRefresh(mainWindow)
                    m = m + 1
    
          pyqt_windowRefresh(mainWindow)
          n = n + 1 

    log_write_Normal(logFile, "Total Files records before Pandas = " + str(len(lstFiles)) + " from: " + str(len(lstFilesPathSubdir)))

    process_GblRecord_Clean()
    process_GblMessage_Clean()
    sProcessing = "Preparing Pandas Data Frame with founded files..."
    process_GblMessage_Set(sProcessing)

    #PREPARING A PANDAS DICT WITH THE PREVIOUS LIST
    dict_df_file = file_pandasFileRecord_CreateDicWithFileLstAddingStats(lstFiles, lstFilesPathSubdir)

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

          pyqt_windowRefresh(mainWindow)

          if bProcessGblStop:
             break
                 
          if sSlash == "":
             #GET SLASH ONLY ONCE
             sSlash = file_getFileSlash(lstSource[n])

          #FIRST FIELD IS THE RECORD NUMBER, NEXT RECORD IS THE PATH/FILE
          #LAST FIELD IS THE PATH FROM WHERE IT IS ANALIZED
          sPathFileFrom = str(file_dic_pandasFileRecord_get_path_file(row1))
          sPathFileSubdir = str(file_dic_pandasFileRecord_get_path_subdir(row1))

          #print("\nFile " + str(n) + ": " + sPathFileFrom + " - Path Subdir: " + sPathFileSubdir)
          sPrint, sFileSize, sFileDateCreation, sFileDateModif, sFieDateAccess = process_CopyFiles_DirFileStatus(sPathFileFrom, logFile)
          #sPrint = "\n" + str(n) + " File: " + sPrint
          #log_write_Normal(logFile, sPrint)

          sProcessing = "File " + process_CalculateNofTotal(n, rows) + ": " + sPathFileFrom + " - Path Subdir: " + sPathFileSubdir + " - Data: " + sPrint
          process_GblMessage_Set(sProcessing, True)
          process_GblRecord_SumValue()
          process_EmitMsgProcessing(procWindows, sProcessing)

          m = 0
          while m < len(lstDestination) and not bProcessGblStop:

              sPathFileTo = lstDestination[m]
              print("\nCopying File " + process_CalculateNofTotal(m, len(lstDestination)) + ": " + sPathFileFrom + " - to: " + sPathFileTo + " - Subdir: " + str(sPathFileSubdir))
              
              bError, sError = process_CopyFiles_CopyFromTo(dict_df_file, n, sPathFileFrom, sPathFileTo, sPathFileSubdir, logFile)
              if bError and bCancelByError:
                  m = len(lstDestination)

              m = m + 1

          n = n + 1 

    #VER EL TEMA DE LOS HILOS - THREAD
    #n = 0
    #while n < 10000000 and not bProcessGblStop:
    #      sProcessing = "processing n: " + str(n)
    #      process_GblMessage_Set(pyqtTxtLog, sProcessing, True)
    #      print("process n: " + str(n))
    #      mainWindow.update()
    #      #pyqt_windowRefresh(mainWindow)
    #      n = n + 1

    #UPDATE CSV FILE
    dict_df_file.to_csv(sDFFile, index=True)

    process_GbRunning_False()
    process_GbDateTimeStartedFinished_Set(False)

        #ENDED PROCESS
    sProcessing = sProcessFlagEnded + " Process for Copying Files "
    if bProcessGblStop:
        sProcessing = sProcessing + "stopped"
    else:
        sProcessing = sProcessing + "finished"
            
    sProcessing = sProcessing + " !\nStarted at: " + dtProcessGblStarted + "\nFinished at: " + dtProcessGblFinished 
    delta = dt_difference(dtProcessGblDateTimeFormat, dtProcessGblStarted, dtProcessGblFinished, False)
    sProcessing = sProcessing + "\nElapsed: " + delta
    sProcessing = sProcessing + "\n\nTotal files processed: " + str(rows) + "\nOutput File:\n" + sDFFile
    if logFile != "":
       sProcessing = sProcessing + "\nLog File:\n" + logFile
    process_GblMessage_Set(sProcessing, True)
    if logFile != "":
         log_write_Normal(logFile, sProcessing)

    return True, sProcessGblMsg

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

    bExists, sFileSize, sFileDateCreation, sFileDateModif, sFieDateAccess, bDirectory = file_getFileState(sFile, logFile)
    
    sPrint = sFile
    if bExists:
       sPrint = sPrint + "\nSize: " + sFileSize + " bytes"
       sPrint = sPrint + "\nCreation Date: " + sFileDateCreation
       sPrint = sPrint + "\nLast Modification Date: " + sFileDateModif
       sPrint = sPrint + "\nLast Access Date: " + sFieDateAccess

       sPrint = sPrint + "\nDirectory: " + str(bDirectory   )
    else:
        sPrint = sPrint + "\nIt does not exist or there is an error."   
    
    return sPrint, sFileSize, sFileDateCreation, sFileDateModif, sFieDateAccess
   
# process_CopyFiles_CopyFromTo ----------------------------------------------------------------------------------------------------------
def process_CopyFiles_CopyFromTo(df, nRecord, sFilePath, sPathTo, sPathSubdir, logFile=""):

    bReturn = True
    sError = ""

    bFromExists, sFromFileSize, sFromFileDateCreation, sFromFileDateModif, sFromFieDateAccess, bFromDirectory = file_getFileState(sFilePath, logFile)
    
    if not bFromExists:
        sError = "File 'FROM' does not exist. File From: " + sFilePath
        if logFile != "":
           log_write_Normal(logFile, sError)
        else:
           print(sError)    
        return False, ""

    sPath, sFileName, sExt = file_PathAndFile_GetSeparated(sFilePath)

    sPathTo = file_addSlashToPathIfNeeded(sPathTo)
    #print("process_CopyFiles_CopyFromTo - sPathTo=" + str(sPathTo)) 
    if sPathSubdir != "":
        sPathTo = sPathTo + sPathSubdir
    sPathTo = file_addSlashToPathIfNeeded(sPathTo)

    #print("process_CopyFiles_CopyFromTo - sPathTo=" + str(sPathTo)) 

    sToPathFile = file_fNormalPathForWindowsLinux(sPathTo + sFileName)
    file_dic_pandasFileRecord_set_path_to(df, nRecord, sToPathFile)
     
    #print("process_CopyFiles_CopyFromTo - sToPathFile=" + str(sToPathFile)) 
    bToCopy = False
    bToExists = False
    if file_FileExists(sToPathFile):
       bToExists, sToFileSize, sToFileDateCreation, sToFileDateModif, sToFieDateAccess, bToDirectory = file_getFileState(sToPathFile, logFile)

    sStatus = ""
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
              sStatus = sError      
              log_write_Normal(logFile, sError)
           else:
               sPrint = "File was deleted. File: " + sToPathFile
               if logFile != "":
                  log_write_Normal(logFile, sPrint)
               bToCopy = True 
        else:
           sStatus = file_dic_status_equal      
    else:
        #FILE IN DESTINATION DOES NOT EXIST. It is copied.
        sPrint = "File 'TO' does not exist. File To: " + sToPathFile
        if logFile != "":
           log_write_Normal(logFile, sPrint)
        bToCopy = True 

    if bToCopy:
        bReturn, sError = file_copy(sFilePath, sToPathFile) 
        if not bReturn and logFile != "":
           sStatus = sError      
           log_write_Normal(logFile, sError)
        else:
           sPrint = "File was copied. File From: " + sFilePath + " - File To: " + sToPathFile
           if logFile != "":
              log_write_Normal(logFile, sPrint)
           sStatus = file_dic_status_copied      

    file_dic_pandasFileRecord_set_status(df, nRecord, sStatus)
    sPrint = "From: '" + sFilePath + "' - To: '" + sToPathFile + "' - Status = " + sStatus 
    if logFile != "":
       log_write_Normal(logFile, sPrint)

    return bReturn, sError
   
# process_GblRecord_Clean ----------------------------------------------------------------------------------------------------------
def process_GblRecord_Clean():
    # GLOBAL VARIABLE
    global nProcessGblRecord
    nProcessGblRecord = 0
    return nProcessGblRecord

# process_GblRecord_SumValue ----------------------------------------------------------------------------------------------------------
def process_GblRecord_SumValue(nSum=1):
    # GLOBAL VARIABLE
    global nProcessGblRecord
    nProcessGblRecord = nProcessGblRecord + nSum
    return nProcessGblRecord

# process_GblMessage_Clean ----------------------------------------------------------------------------------------------------------
def process_GblMessage_Clean():
    # GLOBAL VARIABLE
    global sProcessGblMsg
    sProcessGblMsg = ""
    return sProcessGblMsg

# process_GblMessage_Set ----------------------------------------------------------------------------------------------------------
def process_GblMessage_Set(sText="", bAppend=False, bSetTime=True):
    # GLOBAL VARIABLE
    global sProcessGblMsg
    global nProcessLogNro

    if not bAppend:
       nProcessLogNro = 0
       sProcessGblMsg = sText
    else:
       #REVERSE ORDER - VIEW LAST FIRST
       if sText != "":
          sProcessGblMsg = sText + "\n\n" + sProcessGblMsg
    
    if bSetTime and sProcessGblMsg != "":
       nProcessLogNro = nProcessLogNro + 1
       sProcessLogNro = str_formatNro(nProcessLogNro, 5)

       today_prn = process_GetDateTimeNow()
       sProcessGblMsg =  sProcessLogNro + ". " + today_prn + ": " + sProcessGblMsg

    return sProcessGblMsg

# process_GbStop_True ----------------------------------------------------------------------------------------------------------
def process_GbStop_True():
    process_GbRunning_False()
    return process_GbStop_Set(True)

# process_GbStop_False ----------------------------------------------------------------------------------------------------------
def process_GbStop_False():
    return process_GbStop_Set(False)

# process_GbStop_Set ----------------------------------------------------------------------------------------------------------
def process_GbStop_Set(bStop=False):
    # GLOBAL VARIABLE
    global bProcessGblStop
    bProcessGblStop = bStop
    return bProcessGblStop

# process_GbRunning_True ----------------------------------------------------------------------------------------------------------
def process_GbRunning_True():
    return process_GbRunning_Set(True)

# process_GbRunning_False ----------------------------------------------------------------------------------------------------------
def process_GbRunning_False():
    return process_GbRunning_Set(False)

# process_GbRunning_Set ----------------------------------------------------------------------------------------------------------
def process_GbRunning_Set(bRunnung=False):
    # GLOBAL VARIABLE
    global bProcessGblRunning
    bProcessGblRunning = bRunnung
    return bProcessGblRunning

# process_GbDateTimeStartedFinished_CleanBoth ----------------------------------------------------------------------------------------------------------
def process_GbDateTimeStartedFinished_CleanBoth():
    process_GbDateTimeStartedFinished_Clean(True)
    process_GbDateTimeStartedFinished_Clean(False)

# process_GbDateTimeStartedFinished_Clean ----------------------------------------------------------------------------------------------------------
def process_GbDateTimeStartedFinished_Clean(bStarted=True):
    # GLOBAL VARIABLE
    global dtProcessGblStarted
    global dtProcessGblFinished

    if bStarted:
       dtProcessGblStarted = ""
       return dtProcessGblStarted
    else:
       dtProcessGblFinished = ""
       return dtProcessGblFinished

# process_GbDateTimeStartedFinished_Set ----------------------------------------------------------------------------------------------------------
def process_GbDateTimeStartedFinished_Set(bStarted=True):
    # GLOBAL VARIABLE
    global dtProcessGblStarted
    global dtProcessGblFinished

    today_prn = process_GetDateTimeNow()
    if bStarted:
       dtProcessGblStarted = today_prn
       return dtProcessGblStarted
    else:
       dtProcessGblFinished = today_prn
       return dtProcessGblFinished

# process_GetDateTimeNow ----------------------------------------------------------------------------------------------------------
def process_GetDateTimeNow():
    today = datetime.now()
    today_prn = str(today.strftime(dtProcessGblDateTimeFormat))
    return str(today_prn)

# process_CalculateNofTotal ----------------------------------------------------------------------------------------------------------
def process_CalculateNofTotal(nItem, nTotal):
    
    #BECAUSE IT STARTS WITH 0 (zero)
    nItem = nItem + 1

    sPorcentage = str_GetPorcentageToString(nTotal, nItem, 2)
    sTotal = str(nItem) + " of total " + str(nTotal) + " - processing = % " + sPorcentage
    log_writeWordsInColorBlue(sTotal)
    return sTotal


# --------------------------------------------------------------------------------------------------------------------------------------------------------
def process_EmitMsgProcessing(procWindow, sMsg):      
    global sProcessGblMsg 
    sProcessGblMsg = sMsg
    print("process_EmitMsgProcessing: sProcessGblMsg"+ str(sProcessGblMsg))
    #procWindow.worker_thread.signalProgress(1, sMsg)
    #procWindow.update_progress(1, sMsg)
    print("process_EmitMsgProcessing: sProcessGblMsg"+ str(sProcessGblMsg))

# --------------------------------------------------------------------------------------------------------------------------------------------------------
       
