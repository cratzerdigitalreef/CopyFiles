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
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QCloseEvent

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
sProcessStoppedWord = "stopped"
nProcessRefresh=100
nProcessLineZeros = 5
sPrintAsterics = str_RepeatString(nProcessLineZeros, "*") + " "

sSlashDefault = file_slashdouble

#THIS VARIABLE IS FOR SAVING PROCESSING DATA IN LOG FILE
#bProcessingDEBUG = True
bProcessingDEBUG = False


class Worker(QThread):
    """
    A QThread subclass to perform a long-running task.
    Emits signals for progress updates and completion.
    Includes a flag for cancellation.
    """
    signalProgress = pyqtSignal(str)
    signalProgressBar = pyqtSignal(int)
    signalFinished = pyqtSignal(bool, str)
    signalCancel = pyqtSignal()

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
        self.signalProgress.emit(sMsg)

    def progress_bar(self, nValue):
        self.signalProgressBar.emit(nValue)

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
        
        #print("run finished: sFinishResult = " + str(sFinishResult))
        self.signalFinished.emit(bFinishResult, sFinishResult)

    def cancel(self):
        """
        Sets the internal flag to request cancellation of the task.
        """
        sMsg = "Stop processing ?"
        sMsg = sMsg + "\nRecords: " + str(nProcessGblRecord) + " - at: " + process_GetDateTimeNow()
        sReturn = pyqt_MsgBoxQuestionWithoutParent("Processing", sMsg, False)
        if str(sReturn).upper() == "YES":
           self._is_canceled = True
           self.signalCancel.emit()

class processWindow(QMainWindow, QThread):
    """
    The main application window, managing the GUI and interacting with the worker thread.
    """

    #SIGNAL FOR MAIN WINDOW
    signal_task_finished = pyqtSignal(bool, str)
    signal_task_close = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Process Threding")
        self.setGeometry(100, 100, 600, 400)
        pyqt_centerWindow(self)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        #self.label = QLabel("Ready to start task.")
        self.txt = QTextEdit("Ready to start task.")
        self.txt.setReadOnly(True)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        #self.start_button = QPushButton("Start Task")
        self.cancel_button = QPushButton("Cancel Process")
        self.cancel_button.setEnabled(True) # Initially enabled

        #self.layout.addWidget(self.label)
        self.layout.addWidget(self.txt)
        self.layout.addWidget(self.progress_bar)
        #self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.cancel_button)

        #WORKER FOR PROCESSING
        self.worker_thread  = Worker()
        #LINK TO WORKER SIGNAL
        self.worker_thread.signalProgress.connect(self.update_progress)
        self.worker_thread.signalProgressBar.connect(self.update_progress_bar)
        self.worker_thread.signalFinished.connect(self.task_finished)
        self.worker_thread.signalCancel.connect(self.cancel_task)

        #self.start_button.clicked.connect(self.start_task)
        self.cancel_button.clicked.connect(self.cancel_task)

        self.bFinishResult = True
        self.sFinishResult = ""

   #---------------------------------------------------------------------------------------------------------
    def closeEvent(self, event: QCloseEvent):
        log_writeWordsInColorRed("While processing it CANNOT BE closed this Window. If you want, you should just cancel the process and then close the Window!")
        log_writeWordsInColorRed("Close Window Event is IGNORED!")
        event.ignore()
        return

   #---------------------------------------------------------------------------------------------------------
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
        #print(sMsg)
        self.txt.update()

        #self.progress_bar.setValue(0)
        #self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

        self.progress_bar.setRange(0, 100)

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

   #---------------------------------------------------------------------------------------------------------
    @pyqtSlot(str)
    def update_progress(self, sMsg):
        """
        Receives progress updates from the worker thread and updates the progress bar.
        """
        #self.progress_bar.setValue(value)
        #sMsg = sProcessGblMsg

        #print("Before setText - update_progress : sMsg = " + str(sMsg))    
        self.txt.setText(sMsg)
        self.txt.update()

        #print("After setText - update_progress : sMsg = " + str(sMsg))    
        #self.update()

   #---------------------------------------------------------------------------------------------------------
    @pyqtSlot(int)
    def update_progress_bar(self, nValue):
        """
        Receives progress updates from the worker thread and updates the progress bar.
        """
        self.progress_bar.setValue(nValue)
        self.progress_bar.update()

   #---------------------------------------------------------------------------------------------------------
    @pyqtSlot(bool, str)
    def task_finished(self, bFinishResult, sFinishResult):
        """
        Handles the completion of the task, whether naturally or by cancellation.
        Resets GUI elements.
        """
        sTask = ""
        #print("task_finished")

        #if self.worker_thread._is_canceled:
        if bProcessGblStop:    
            #self.label.setText("Task canceled.")
            sTask = "canceled"
        else:
            #self.label.setText("Task finished.")
            sTask = "finished"
        #self.start_button.setEnabled(True)
        #self.cancel_button.setEnabled(False)

        self.bFinishResult = bFinishResult
        self.sFinishResult = sFinishResult

        sMsg = "Task " + sTask + " ... at " + process_GetDateTimeNow()
        if self.sFinishResult != "":
            sMsg = sMsg + "\n\n" + self.sFinishResult

        if bProcessGblStop:    
            log_writeWordsInColorYellow(sMsg)
        else:    
            log_writeWordsInColorGreen(sMsg)
        self.txt.setText(sMsg)

        pyqt_ButtonSetText(self.cancel_button, "Close")

        if sProcessFlagEnded in self.sFinishResult:
            sMsgEnded = str_getSubStringFromOcur(self.sFinishResult, sProcessFlagEnded, 1)
            sMsgEnded = sProcessFlagEnded + sMsgEnded
            pyqt_MsgBox_Info("Copying Files", sMsgEnded)
        else:
            sMsgEnded = sMsg    

        self.worker_thread._is_canceled = False # Reset for next run
        self.signal_task_finished.emit(bFinishResult, str(sMsgEnded))

        #self.hide()

   #---------------------------------------------------------------------------------------------------------
    @pyqtSlot()
    def cancel_task(self):
        """
        Requests cancellation of the running task in the worker thread.
        """
        #self.worker_thread.cancel()
        #self.label.setText("Cancelling task...")
        sProcess = "Cancelling task"
        bClose = False
        if pyqt_ButtonGetText(self.cancel_button).upper() == "CLOSE":
            sProcess = "Close process"
            bClose = True
            self.hide()

        self.txt.setText(sProcess + " ... at " + process_GetDateTimeNow())
        process_GbStop_True()
        #self.cancel_button.setEnabled(False) # Disable while waiting for cancellation
        
        if bClose:
           self.signal_task_close.emit()

        return

# process_CopyFiles ----------------------------------------------------------------------------------------------------------
def process_CopyFiles(logFile, mainWindow, procWindows, lstSource, lstDestination, bCancelByError=False):
    #print("process_CopyFiles - Before start_task")
    procWindows.start_task(logFile, mainWindow, procWindows, lstSource, lstDestination, bCancelByError)
    #print("process_CopyFiles - After start_task")

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

    #THIS IS BECAUSE  
    # if you copy a list using a simple assignment operator (=), appending to the first list will affect the second list because both variables point to the same object in memory. 
    # In Python, the assignment operator (=) does not create a new list; it merely creates a new reference (or name) for the existing list object. 
    #lstSourceAtInit = lstSource
    lstSourceAtInit = lstSource.copy()
    lstDestinationAtInit = lstDestination.copy()

    if not bProcess:   
       sWarning = sWarning + sError
       return False, sWarning

    bDuplicated, sError = file_AreFilesDuplicated(lstSource, lstDestination)
    if bDuplicated:
       sWarning = sWarning + sError
       return False, sWarning

    pyqt_windowRefresh(mainWindow)

    sMsg = "Process Started at: " + str(process_GetDateTimeNow())
    sMsg = sMsg + "\nTotal Source Directories: " + str(len(lstSource))
    sMsg = sMsg + "\nTotal Destination Directories: " + str(len(lstDestination))
    if logFile != "":
        log_write(logFile, sMsg)

    process_EmitMsgProcessing(procWindows, sMsg)

    #GETTING ALL PATHs AND FILEs    
    lstFiles = []
    lstFilesPathSubdir = []

    #PANDAS DATA FRAME FOR MANAGING FILES DATA
    dict_df_file = pd.DataFrame()

    n = 0
    nSource = len(lstSource)
    sSourceOld = ""
    sSourceLast = ""

    nStartAddingFromInit = 0

    #------------------------------------------------------------------------------------------------------------------
    #PREPARING DICTONARY GETTING ALL FILES AND DIRECTORIES FROM SOURCE LIST
    while n < nSource and not bProcessGblStop:

          #FOR CHECKING WHETHER TO ADD SOURCES FROM INIT
          if nStartAddingFromInit < len(lstSourceAtInit):
             if lstSource[n] == lstSourceAtInit[nStartAddingFromInit]:
                nStartAddingFromInit = nStartAddingFromInit + 1

          lstSource[n]= file_fNormalPathForWindowsLinux(lstSource[n])
          sProcessing = "Processing source: " + process_CalculateNofTotal(n, nSource) + " - " + str(lstSource[n])
          if len(dict_df_file) > 0:
             sProcessing = sProcessing + " - Pandas Data Frame Length: " + str_AddThousandToNumber(str(len(dict_df_file)))

          process_PrintColor(n, sProcessing)
          process_RefreshShowTextInDialog(procWindows, n, sProcessing)

          process_GblRecord_SumValue()
          process_GblMessage_Set(sProcessing)

          lstFilesTemp = process_CopyFiles_GetDirsAndFiles(lstSource[n], logFile)
          if len(lstFilesTemp) > 0:

              m = 0
              sLastPath = ""
              while m < len(lstFilesTemp) and not bProcessGblStop:

                    # Managed duplicates later with PANDAS: drop_duplicates
                    #if lstFilesTemp[m] not in lstFiles:

                       #ADDED FOR FILES TO BE PROCESSED
                       lstFilesTemp[m] = file_fNormalPathForWindowsLinux(lstFilesTemp[m])
                       lstFiles.append(lstFilesTemp[m])

                       if file_Is_a_Directory(lstFilesTemp[m]):
                          #print("process_CopyFiles - Added new directory for source: " + str(lstFilesTemp[m]))
                          lstSource.append(lstFilesTemp[m])
                          nSource = len(lstSource)
                          sLastPath = lstFilesTemp[m]

                       #sPath, sPathSubdir, sSlash = file_GetPath_From_Next(lstFilesTemp[m], lstSource[n])
                       sPathSubdir = file_getSubDirFromPath(lstFilesTemp[m], lstSource[n]) 
                       #ADDED FOR SOURCE PATH FOR FILES TO BE PREOCESSED
                       sProcessing = "Getting files - Iteration: " + process_CalculateNofTotal(n, nSource)
                       sProcessing = sProcessing + " - Files found [" + str_AddThousandToNumber(str(m+1)) + "]:"
                       sProcessing = sProcessing + "\n" + str(lstFilesTemp[m])
                       sProcessing = sProcessing + " - Directory for source [" + str(str_AddThousandToNumber(n)) + "]: " + str(lstSource[n])
                       if sPathSubdir != "":
                          sProcessing = sProcessing + " - sPathSubdir: " + str(sPathSubdir)

                       process_PrintColor(m, "\n" + sPrintAsterics + sProcessing)

                       #DEBUGGING
                       process_DEBUG(logFile, sProcessing)

                       lstFilesPathSubdir.append(sPathSubdir) 

                       process_GblMessage_Set(sProcessing)

                       #SIGNALs to PROCESS WINDOW
          
                    # TRYNING TO BE FASTER ADDING DUPLICATES AND REMOVING THEM LATER WITH PANDAS
                    #else:
                    #   sProcessingT = sProcessing
                    #   sProcessing = sProcessing + "\nItem [" + str(m) + "]: " + lstFilesTemp[m] + " already exists under source list 'lstFiles'"
                    #   process_PrintDebug(m, sProcessing)

                    #   #DEBUGGING
                    #   process_DEBUG(logFile, sProcessing)

                    #   sProcessing = sProcessingT

                       process_RefreshShowTextInDialog(procWindows, m, sProcessing)

                    #pyqt_windowRefresh(mainWindow)
                       m = m + 1
          else:
              sProcessingT = sProcessing
              sProcessingT = sProcessingT + "\n" + "There are NO files or directories under item [" + str(n) + "]: " + lstSource[n]
              process_PrintDebug(n, sProcessingT)

              if bProcessingDEBUG:
                 log_write_Normal(logFile, sProcessingT)     
    
          #------------------------------------------------------------------------------------------------------------------
          #PREPARING A PANDAS DICT WITH THE PREVIOUS LIST
          #DONE NOW BECAUSE MEMORY PROBLEMS WITH LARGE DATA
          if (n & file_nRefresh) == 0:
             dict_df_file = file_pandasFileRecord_CreateDicWithFileLstAddingStats(dict_df_file, lstFiles, lstFilesPathSubdir)
             sSourceLast = lstSource[n-1]
             lstSource = []

             if len(lstSourceAtInit) > 1:
                 #IT IS NEEDED TO BE ADDED THE OTHER SOURCES
                 j = nStartAddingFromInit
                 while j < len(lstSourceAtInit):
                     if lstSourceAtInit[j] not in str(lstSource):
                        lstSource.append(lstSourceAtInit[j])
                     j = j + 1

             lstSource.append(sSourceLast)
             #print("REFRESH - sSourceLast: " + str(sSourceLast) + " - lstSourceAtInit[len(lstSourceAtInit)-1]: " + lstSourceAtInit[len(lstSourceAtInit)-1] + " - sSourceOld=" + str(sSourceOld))

             nSource = len(lstSource)

             #print("REFRESH - lstSource length: " + str(len(lstSource)) + "\n" + str(lstSource))

             log_writeWordsInColorYellow("Flush data to Pandas Data Frame. Iteraction: " + str(n) + " - last data: " + sSourceLast + " - Source Length: " + str(nSource))
             n = 0

             if (sSourceOld == sSourceLast and sSourceLast != "" and len(lstSource) <= 1) or (sSourceLast == lstSourceAtInit[len(lstSourceAtInit)-1] and sSourceOld!=""):
                 #STOP PROCESS
                 n = nSource
             else:
                 sSourceOld = sSourceLast    
          else:
             n = n + 1 
   
          pyqt_windowRefresh(mainWindow)


    #------------------------------------------------------------------------------------------------------------------

    log_write_OKInGreen(logFile, "Total Files records before Pandas = " + str_AddThousandToNumber(str(len(lstFiles))) + " from: " + str_AddThousandToNumber(str(len(lstFilesPathSubdir))))

    sDFFile = ""
    rows = 0
    cols = 0

    #TOTALs
    nfile_dic_status_copied = 0
    nfile_dic_status_equal = 0
    nfile_dic_status_error = 0
    nfile_dic_status_warning = 0
    nfile_dic_status_warning_dir = 0
    sfile_dic_status_warning = ""
    sfile_dic_status_error = ""

    if not bProcessGblStop:

       #print("LAST - lstFiles length: " + str(len(lstFiles)) + "\n" + str(lstFiles))
       #ADD THE LAST REMANENT
       dict_df_file = file_pandasFileRecord_CreateDicWithFileLstAddingStats(dict_df_file, lstFiles, lstFilesPathSubdir)

       process_GblRecord_Clean()
       process_GblMessage_Clean()
       sProcessing = "Preparing Pandas Data Frame with founded files..."
       process_GblMessage_Set(sProcessing)

       #------------------------------------------------------------------------------------------------------------------
       #PREPARING A PANDAS DICT WITH THE PREVIOUS LIST
       #DONE BEFORE BECAUSE MEMORY PROBLEMS WITH LARGE DATA
       #dict_df_file = file_pandasFileRecord_CreateDicWithFileLstAddingStats(lstFiles, lstFilesPathSubdir)

       #GENERATE A CSV FILE WITH PANDAS DF
       today = datetime.now()
       today_prn = today.strftime("%Y-%m-%d")
       sDFFile = "CopyFiles" + "_" + today_prn + "csv"
       if logFile != "":
          sDFFile = logFile + "_DF.csv"
       dict_df_file.to_csv(sDFFile, index=True)
       #------------------------------------------------------------------------------------------------------------------

       #START PROCESS
       dict_df_file_cols = dict_df_file.columns.tolist()
       rows, cols = dict_df_file.shape 
       log_write_Normal(logFile, "Pandas Columns header = " + str(dict_df_file_cols) + " Total Columns=" + str(cols))
       log_write_Normal(logFile, "Total records with Pandas = " + str(rows))

       #SET PROGRESS BAR RANGE
       procWindows.progress_bar.setRange(0, rows)

       nCols = 0
       n = 0
       sSlash = ""
    
       #------------------------------------------------------------------------------------------------------------------
       # READING PANDAS DATA FRAME

       for row1 in dict_df_file.itertuples():

          #pyqt_windowRefresh(mainWindow)

          if bProcessGblStop:
             break
                 
          if sSlash == "":
             #GET SLASH ONLY ONCE
             sSlash = file_getFileSlash(lstSource[n])

          #FIRST FIELD IS THE RECORD NUMBER, NEXT RECORD IS THE PATH/FILE
          #LAST FIELD IS THE PATH FROM WHERE IT IS ANALIZED
          sPathFileFrom = str(file_dic_pandasFileRecord_get_path_file(row1))
          sPathFileSubdir = str(file_dic_pandasFileRecord_get_path_subdir(row1))
          sPathFileFromParent = str(file_dic_pandasFileRecord_get_file_parent(row1))

          sMsg = "\nFile [" + str(n) + "]: " + sPathFileFrom + " - Path Subdir: " + sPathFileSubdir + " - Parent: " + sPathFileFromParent
          sPrint, sFileSize, sFileDateCreation, sFileDateModif, sFieDateAccess = process_CopyFiles_DirFileStatus(sPathFileFrom, logFile)
          sPrint = "\n" + str(n) + " File: " + sPrint

          #DEBUGGING
          process_DEBUG(logFile, sMsg + "\n" + sPrint)

          #SIGNAL TO PROCESS WINDOW FOR PROGRESS BAR
          process_EmitMsgProcessingProgressBar(procWindows, n+1)

          #--------------------------------------------------------------------------------------------------------------------------------
          # PROCESS EACH RECORD IN DATA FRAME
          m = 0
          while m < len(lstDestination) and not bProcessGblStop:

              sProcessing = "Processing item from Data Frame: " + process_CalculateNofTotal(n, rows)
              sProcessing = sProcessing + str_GetENTER() + str_GetENTER() + "Source File:" + str_GetENTER() + sPathFileFrom
              sProcessing = sProcessing + " - Path Subdir: " + sPathFileSubdir
              sProcessing = sProcessing + " - Parent: " + sPathFileFromParent
              sProcessing = sProcessing + str_GetENTER() + str_GetENTER() + "Data from Sourth File:" + sPrint

              sProcessing = sProcessing + str_GetENTER() + str_GetENTER() + "Destination without processing: " +  lstDestination[m]
              sPathFileTo = process_CopyFiles_CopyFromTo_PreparePathTo(lstDestination[m], sPathFileFrom, sPathFileSubdir, sSlash)
              sProcessing = sProcessing + str_GetENTER() + "Destination after processing: " +  sPathFileTo

              #if n > 50:
              #   process_GbStop_Set(True)

              bError, sError = process_CopyFiles_CopyFromTo(dict_df_file, n, sPathFileFrom, sPathFileTo, logFile)
              sFileStatus = str(file_dic_pandasFileRecord_get_status(dict_df_file, n))

              sProcessing = sProcessing + str_GetENTER() + "Status: " +  sFileStatus
              if sError != "":
                 sProcessing = sProcessing + str_GetENTER() + "Error: " +  sError
                  
              process_PrintColor(n, sProcessing)

              process_GblMessage_Set(sProcessing)
              process_GblRecord_SumValue()

              process_RefreshShowTextInDialog(procWindows, n, sProcessing)

              sMsg = "\nCopying File for Destination " + process_CalculateNofTotal(m, len(lstDestination)) + ": " + sPathFileFrom + " - to: " + sPathFileTo + " - Subdir: " + str(sPathFileSubdir)
              #DEBUGGING
              process_DEBUG(logFile, sMsg)

              #print("Status: " + str(sFileStatus))
              #-------------------------------------------------------------------------------------------------------------------------
              #TOTALs
              if file_dic_status_copied in sFileStatus:
                  nfile_dic_status_copied = nfile_dic_status_copied+ 1
              else:    
                  if file_dic_status_equal in sFileStatus:
                     nfile_dic_status_equal = nfile_dic_status_equal+ 1
                  else:
                      if file_dic_status_dir in sFileStatus: 
                          #TO IS A DIRECTORY
                          nfile_dic_status_warning_dir = nfile_dic_status_warning_dir + 1
                      else:    
                          #ANALIZE WARNINGS
                          if file_dic_status_warning in sFileStatus:
                             if file_dic_status_warning_dir in sFileStatus:
                                nfile_dic_status_warning_dir = nfile_dic_status_warning_dir + 1
                             else:
                                nfile_dic_status_warning = nfile_dic_status_warning + 1   
                             sfile_dic_status_warning = sfile_dic_status_warning + "\n"
                             sfile_dic_status_warning = sfile_dic_status_warning + "Item [" + str_AddThousandToNumber(str(n)) + "] - Status: " + sFileStatus    
                          else:    
                             nfile_dic_status_error = nfile_dic_status_error + 1
                             sfile_dic_status_error = sfile_dic_status_error + "\n"
                             sfile_dic_status_error = sfile_dic_status_error + "Item [" + str_AddThousandToNumber(str(n)) + "] - Status: " + sFileStatus    
              #-------------------------------------------------------------------------------------------------------------------------
                         
              if bError and bCancelByError:
                  m = len(lstDestination)

              m = m + 1
          #--------------------------------------------------------------------------------------------------------------------------------

          n = n + 1 
    #------------------------------------------------------------------------------------------------------------------

    #UPDATE CSV FILE
    if sDFFile != "":
       dict_df_file.to_csv(sDFFile, index=True)

    process_GbRunning_False()
    process_GbDateTimeStartedFinished_Set(False)

    #ENDED PROCESS
    sProcessing = sProcessFlagEnded + " Process for Copying Files "
    if bProcessGblStop:
        sProcessing = sProcessing + sProcessStoppedWord
    else:
        sProcessing = sProcessing + "finished"
            
    sProcessing = sProcessing + " !\nStarted at: " + dtProcessGblStarted + "\nFinished at: " + dtProcessGblFinished 
    delta = dt_difference(dtProcessGblDateTimeFormat, dtProcessGblStarted, dtProcessGblFinished, False)
    sProcessing = sProcessing + "\nElapsed: " + delta
    sProcessing = sProcessing + "\n\nTotal files processed: " + str_AddThousandToNumber(str(rows))

    #DETAILS FOR SOURCE AND DESTINATION
    sProcessing = sProcessing + "\n\nTotal Path Source at Init: " + str_AddThousandToNumber(str(len(lstSourceAtInit)))
    n = 0
    while n < len(lstSourceAtInit):
          sProcessing = sProcessing + "\nPath Source at Init [" + str(n+1) + "]: " + str(lstSourceAtInit[n])
          n = n + 1
    sProcessing = sProcessing + "\n\nTotal Path Destination at Init: " + str_AddThousandToNumber(str(len(lstDestinationAtInit)))
    n = 0
    while n < len(lstDestinationAtInit):
          sProcessing = sProcessing + "\nPath Destination at Init [" + str(n+1) + "]: " + str(lstDestinationAtInit[n])
          n = n + 1

    #ADDING TOTALs
    sProcessing = sProcessing + "\n" 

    sWarningDestinationPath = ""
    if len(lstDestinationAtInit) > 1:
        sWarningDestinationPath = ". It should be taken into account that there are more than 1 (one) destination path, and the comparison may not be the real one."

    sProcessing = sProcessing + process_TotalsPrepare("Total files copied" + sWarningDestinationPath, rows, nfile_dic_status_copied)
    sProcessing = sProcessing + process_TotalsPrepare("Total files equal", rows, nfile_dic_status_equal) 
    if nfile_dic_status_error > 0:
       sProcessing = sProcessing + process_TotalsPrepare("Total files with problems/errors", rows, nfile_dic_status_error)
    if nfile_dic_status_warning > 0:   
       sProcessing = sProcessing + process_TotalsPrepare("Total files with WARNINGs", rows, nfile_dic_status_warning)
    if nfile_dic_status_warning_dir > 0:
       sProcessing = sProcessing + process_TotalsPrepare("Total files with WARININGs because DIRECTORY", rows, nfile_dic_status_warning_dir)

    sProcessingWarningErrors = ""
    if len(sfile_dic_status_warning) > 0:
       sProcessingWarningErrors = sProcessingWarningErrors + "\nWARNINGs: " + str(sfile_dic_status_warning)
    if len(sfile_dic_status_error) > 0:
       sProcessingWarningErrors = sProcessingWarningErrors + "\nERRORs: " + str(sfile_dic_status_error)

    if sProcessingWarningErrors != "" and logFile != "":
        sProcessing = sProcessing + "\nGOTO LOG File '" + logFile + "' for WARNING/ERROR details."

    sProcessing = sProcessing + "\n\nOutput File:\n" + sDFFile

    if logFile != "":
       sProcessing = sProcessing + "\nLog File:\n" + logFile

    process_GblMessage_Set(sProcessing)

    if logFile != "":
         log_write_InfoInBlue(logFile, sProcessing + sProcessingWarningErrors)
    else:
        log_writePrintOnlyInfo(sProcessing + sProcessingWarningErrors)     

    return True, sProcessing

# process_TotalsPrepare ----------------------------------------------------------------------------------------------------------
def process_TotalsPrepare(sDes, nTotal, nValue):
    sProcessing = "\n" + sDes + ": " + str_AddThousandToNumber(str(nValue)) + " (% " + str_GetPorcentageToString(nTotal, nValue) + ")"
    return sProcessing

# process_CopyFiles_GetDirsAndFiles ----------------------------------------------------------------------------------------------------------
def process_CopyFiles_GetDirsAndFiles(sPathFile, logFile=""):
    lstFilesTemp = []
    if file_Is_a_Directory(sPathFile):
       lstFilesTemp = file_getDirsAndFiles(sPathFile, logFile)
       nFound = len(lstFilesTemp)
       log_writePrintOnlyDebug("process_CopyFiles_GetDirsAndFiles - Total files found for path: " + str(sPathFile) + "' = " + str(nFound))
    else:
       log_writePrintOnlyDebug("process_CopyFiles_GetDirsAndFiles - Path '" + str(sPathFile) + "' is not a DIRECTORY.")
           
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
def process_CopyFiles_CopyFromTo(df, nRecord, sFilePath, sPathTo, logFile=""):

    bReturn = True
    sError = ""

    bFromExists, sFromFileSize, sFromFileDateCreation, sFromFileDateModif, sFromFieDateAccess, bFromDirectory = file_getFileState(sFilePath, logFile)
    
    if not bFromExists:
        sError = "File 'FROM' does not exist. File From: " + sFilePath
        if logFile != "":
           log_write_ErrorInRed(logFile, sError)
        else:
           log_writePrintOnlyError(sError)    
        return False, ""

    sPath, sFileName, sExt, sParent = file_PathAndFile_GetSeparated(sFilePath)

    sPathTo = file_addSlashToPathIfNeeded(sPathTo)

    #print("process_CopyFiles_CopyFromTo - sPathTo=" + str(sPathTo)) 

    sToPathFile = file_fNormalPathForWindowsLinux(sPathTo + sFileName)

    sToPathFileTemp = file_dic_pandasFileRecord_get_path_toByRowNro(df, nRecord)
    if sToPathFileTemp != "":
        sToPathFileTemp = sToPathFileTemp + file_sSeparaFileTo + sToPathFile
        #MORE THAN ONE DESTINATION
        file_dic_pandasFileRecord_set_path_to(df, nRecord, sToPathFileTemp)
    else:    
        #ONE DESTINATION
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

           if bToDirectory:
              #DESTINATION IS A DIRECTORY AND IT IS NOT DELETED
              sError = "File is a directory, not to be deleted. File: " + sToPathFile
              log_write_WarningInYellow(logFile, sError)
              file_dic_pandasFileRecord_set_status(df, nRecord, file_dic_status_dir)
              return True, sError

           bReturn, sError = file_delete(sToPathFile)
           if not bReturn and logFile != "":
              sStatus = sError      
              if file_dic_status_warning in sError:
                  log_write_WarningInYellow(logFile, sError)
              else:    
                 log_write_ErrorInRed(logFile, sError)
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
           log_write_ErrorInRed(logFile, sError)
        else:
           sPrint = "File was copied. File From: " + sFilePath + " - File To: " + sToPathFile
           if logFile != "":
              log_write_OKInGreen(logFile, sPrint)
           sStatus = file_dic_status_copied      

    if sToPathFileTemp != "":
        sStatusTemp = file_dic_pandasFileRecord_get_statusByRowNro(df, nRecord)
        if sStatusTemp != "":
           sStatusTemp = sStatusTemp + file_sSeparaFileTo + sStatus
        else:
           sStatusTemp = sStatus  
        #MORE THAN ONE DESTINATION - DIFFERENT STATUS
        file_dic_pandasFileRecord_set_status(df, nRecord, sStatusTemp)
    else:    
        #ONE DESTINATION - ONE STATUS
        file_dic_pandasFileRecord_set_status(df, nRecord, sStatus)

    sPrint = "From: '" + sFilePath + "' - To: '" + sToPathFile + "' - Status = " + sStatus 
    if logFile != "":
       log_write_Normal(logFile, sPrint)

    return bReturn, sError
   
# process_CopyFiles_CopyFromTo_PreparePathTo ----------------------------------------------------------------------------------------------------------
def process_CopyFiles_CopyFromTo_PreparePathTo(sPathTo, sFilePath, sPathFileSubdir, sSlash=sSlashDefault):

    #bExit = False

    #print("process_CopyFiles_CopyFromTo_PreparePathTo - sPathTo: " + str(sPathTo) + " - sFilePath: " + str(sFilePath) + " - sPathFileSubdir: " + str(sPathFileSubdir))

    sPathToParent = file_PathAndFile_GetParent(sPathTo)
    sFilePathParent = file_PathAndFile_GetParent(sFilePath)

    #print("process_CopyFiles_CopyFromTo_PreparePathTo - sPathToParent: " + str(sPathToParent) + " - sFilePathParent: " + str(sFilePathParent))

    #EXAMPLE 1
    #sFilePath: D:\Temp\vbp\7Bits\7Bits.exe
    #sFilePathParent: "7Bits"
    #sPathTo: g:\Temp
    #sPathToParent: Temp
    #Final destination path desired: g:\temp\7Bits for 7Bits.exe

    #EXAMPLE 2
    #sFilePath: D:\Temp\vbp\7Bits\7Bits.exe
    #sFilePathParent: "7Bits"
    #sPathTo: g:\Temp\7Bits
    #sPathToParent: 7Bits
    #Final destination path desired: g:\temp\7Bits for 7Bits.exe

    if sPathFileSubdir != "":

        #EXAMPLE 3
        #sFilePath: D:\Temp\vbp\DLLs\ADO\Cls\clsADO.cls
        #sFilePathParent: "Cls"
        #sPathTo: g:\Temp
        #sPathToParent: Temp
        #sPathSubdir: \ADO\Cls\
        #Final destination path desired: g:\temp\DLLs\ADO\Cls for clsADO.cls

        #EXAMPLE 4 
        #sFilePath:  D:\Temp\vbp\AgendaC\vbp\DLLs
        #sFilePathParent: "vbp"
        #sPathTo: g:\Temp
        #sPathToParent: Temp
        #sPathSubdir: \vbp\AgendaC\
        #Final destination path desired: g:\temp\vbp\AgendaC\ for DLLs path

        sTemp = files_getPathFromLastOcurrencePattern(sFilePath, sPathFileSubdir)

        #sTemp = D:\Temp\vbp\DLLs\
        #sFilePathParent = file_PathAndFile_GetParent(sTemp)
        sFilePathParent = file_PathAndFile_GetFileName(sTemp)

        #print("process_CopyFiles_CopyFromTo_PreparePathTo - sTemp: " + str(sTemp) + " - sFilePathParent: " + str(sFilePathParent))

    if (sFilePathParent not in sPathToParent) and (sFilePathParent not in sPathTo):
       sPathTo = sPathTo + sSlash + sFilePathParent
       #print("process_CopyFiles_CopyFromTo_PreparePathTo - sPathTo: " + str(sPathTo) + " - sFilePathParent: " + str(sFilePathParent) + " - sPathToParent: " + str(sPathToParent))

    if sPathFileSubdir != "":
        sPathTo =  sPathTo + sSlash + sPathFileSubdir
        #print("process_CopyFiles_CopyFromTo_PreparePathTo - sPathTo: " + str(sPathTo) + " - sPathFileSubdir: " + str(sPathFileSubdir))

    #print("process_CopyFiles_CopyFromTo_PreparePathTo - sPathTo: " + str(sPathTo))
    sPathTo = file_fNormalPathForWindowsLinux(sPathTo)
    sPathTo = file_addSlashToPathIfNeeded(sPathTo)
    #print("process_CopyFiles_CopyFromTo_PreparePathTo - sPathTo: " + str(sPathTo))

    #if bExit:
    #    exit(0)

    return sPathTo

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
       sProcessLogNro = str_formatNro(nProcessLogNro, nProcessLineZeros)

       today_prn = process_GetDateTimeNow()
       if bAppend:
          sProcessGblMsg = sProcessGblMsg + sProcessLogNro + ". "
       else:   
          sProcessGblMsg =  ""
       sProcessGblMsg = sProcessGblMsg + today_prn + ": \n\n" + sProcessGblMsg

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
    return str_CalculateNofTotal(nItem, nTotal)

# --------------------------------------------------------------------------------------------------------------------------------------------------------
def process_EmitMsgProcessing(procWindow, sMsg):      
    global sProcessGblMsg 
    sProcessGblMsg = sMsg
    #print("process_EmitMsgProcessing: sProcessGblMsg"+ str(sProcessGblMsg))
    procWindow.worker_thread.signalProgress.emit(sMsg)
    #print("process_EmitMsgProcessing: sProcessGblMsg"+ str(sProcessGblMsg))

# --------------------------------------------------------------------------------------------------------------------------------------------------------
def process_EmitMsgProcessingProgressBar(procWindow, nValue):      
    procWindow.worker_thread.signalProgressBar.emit(nValue)
    return

# --------------------------------------------------------------------------------------------------------------------------------------------------------
def process_Time(nSleepSeconds=1):
    time.sleep(nSleepSeconds)  # Pause for 1 second

# --------------------------------------------------------------------------------------------------------------------------------------------------------
def process_PrintDebug(nAvance, sMsg):
    if (nAvance % nProcessRefresh) == 0 and sMsg != "":
        log_writePrintOnlyDebug(sMsg)     

# --------------------------------------------------------------------------------------------------------------------------------------------------------
def process_PrintColor(nAvance, sMsg, bBlue=True):
    if (nAvance % nProcessRefresh) == 0 and sMsg != "":
        if bBlue:
           log_writeWordsInColorBlue(sMsg)
        else:
           process_PrintDebug(nAvance, sMsg)     

# --------------------------------------------------------------------------------------------------------------------------------------------------------
def process_RefreshShowTextInDialog(procWindows, nAvance, sMsg):
    if (nAvance % nProcessRefresh) == 0 and sMsg != "":
       #SHOW REFRESH 
       process_EmitMsgProcessing(procWindows, sMsg)

# --------------------------------------------------------------------------------------------------------------------------------------------------------
def process_DEBUG(logFile, sMsg):
    if bProcessingDEBUG:
       log_write_Normal(logFile, sMsg)

# --------------------------------------------------------------------------------------------------------------------------------------------------------
       
