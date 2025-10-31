# -*- coding: UTF-8 -*-

import sys
import os

#PYQT IMPORTS
#from PySide6.QtUiTools import QUiLoader
#from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
#from PySide6.QtWidgets import QMessageBox, QTextEdit, QFileDialog, QTableView
#from PySide6.QtCore import QFile, QIODevice

#from PyQt5.QtGui import QIcon
#from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableView, QHeaderView, QMessageBox, QProgressBar,QLineEdit
#from PyQt5.uic import loadUi
#from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QThread, QPropertyAnimation, QAbstractTableModel

#from PySide2.QtUiTools import QUiLoader
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtWidgets import QMessageBox, QTextEdit, QFileDialog, QTableView, QTableWidget, QTableWidgetItem, QGroupBox
from PyQt5.QtCore import QFile, QIODevice


# from ..constants.general import color_dark_button, color_app_background_light, color_app_background_dark, \
#     color_red_dark, color_green_dark

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(current)
sys.path.append(parent_directory+"/libs")
sys.path.append(parent_directory+"/constants")
sys.path.append(parent_directory+"/proc")
sys.path.append(parent_directory+"/iu")

import customtkinter as ctk

################################################################################
# ADDED: Make the app follow the system’s light/dark settings:
################################################################################
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

from customtkinter import CTkScrollbar
from customtkinter import CTkCheckBox

from pathlib import Path
from libs.str import *
from libs.pyqt import *
from libs.pyqt_grid import *
from libs.xml_utils import *
from constants.general import *
from proc.process import *
from libs.log import *

import sys

class CopyFilesHomeScreen:

    def __init__(self, client, log_file):

        self.log_file = log_file
        self.str_client = client
        self.status = "Success"
        self.is_error = False


        #---------------------------------------------------------------------------------------
        #FOR XML SAVING - LOADING DATA
        current = os.path.dirname(os.path.realpath(__file__))
        parent_directory = os.path.dirname(current)
        self.sApp_Path = parent_directory

        self.sApp_XML = sDef_App_XML

        self.sApp_XML_PathAndFile = self.sApp_Path + "\\" + self.sApp_XML  
        self.sApp_XML_Path = file_fNormalPathForWindowsLinux(self.sApp_Path)
        if file_fFileIsExe():
           self.sApp_XML_PathAndFile = os.path.join(sys._MEIPASS, self.sApp_XML)

        self.sXML_PATH_DEFAULT_SOURCE = "APP_PATH_DEFAULT_SOURCE"
        self.sXML_PATH_DEFAULT_DESTINATION = "APP_PATH_DEFAULT_DESTINATION"
        self.sXML_APDU_VERSION = "APP_VERSION"
        self.sXML_PATH_SOURCE = "XML_PATH_SOURCE_"
        self.sXML_PATH_DESTINATION = "XML_PATH_DESTINATION_"
        self.sXML_PATH_SOURCE_TOTAL = "XML_PATH_SOURCE_TOTAL"
        self.sXML_PATH_DESTINATION_TOTAL = "XML_PATH_DESTINATION_TOTAL"

        #print("self.sApp_XML_PathAndFile = " + str(self.sApp_XML_PathAndFile))
        #---------------------------------------------------------------------------------------

        self.sPathSource = self.sApp_Path
        self.sPathDestination = self.sApp_Path
        self.nPathSourceTotal = 0
        self.nPathDestinationTotal = 0
        self.sPathSourceTotal = str(self.nPathSourceTotal)
        self.sPathDestinationTotal = str(self.nPathDestinationTotal)

        self.sLineMark = str_RepeatString(100, sDef_Asterisc) + "\n"

        self.sdtFormat = sDef_dtFormat
        self.sdtString = str_RepeatString(100,sDef_Minus)

        self.nSourceRows = 0
        self.nDestinationRows = 0
        self.nRowLen = 300
        self.nColWidth = self.nRowLen
        self.nColPath = 0
        self.nRowCurrentSource = -1
        self.nRowCurrentDestination = -1
        self.sTVDesSource = ""
        self.sTVDesDestination = ""

        ############################################################################
        # CHANGED these to 2‑tuples so each color can adapt in Light or Dark mode.
        # (left color is for Light, right color is for Dark)
        ############################################################################
        self.def_color_OK = ("green", color_green_dark)
        self.def_color_NOK = ("red", color_red_dark)
        self.def_color_INFO = ("blue", color_green_dark)
        self.def_enabled = "normal"
        self.def_disabled = "disabled"
        self.def_Available = "Available"
        self.def_AvailableNOT = "NOT " + self.def_Available
        self.def_Description = "Description"
        self.def_Separa = " - "
        self.def_DosPuntos = sDef_DosPuntos
        
        ############################################################################
        # CHANGED color variables so they adapt:
        ############################################################################
        self.app_label_color = ("blue", "white")  # was just "blue"
        self.app_button_color = ("orange", color_dark_button)  # was just "orange"
        self.app_button_color_text = ("black", "white")
        self.app_background_color = (color_app_background_light, color_app_background_dark)  # was "darkgrey"

        self.list_separa = sDef_Minus
        self.list_separaNroItem = sDef_list_separaNroItem
        
        self.app = QApplication(sys.argv) # Construct QApplication first
        self.ui_file_name = os.path.join(parent_directory,app_ui_file_name)
        bReturn, self.window = pyqt_open_ui_file(self.ui_file_name)

        if not (bReturn or self.window):
           sys.exit(-1)

        self.nWindowWidth = self.app.primaryScreen().size().width()
        self.nWindowHeight = self.app.primaryScreen().size().height()
        print(f"Width: {self.nWindowWidth}")
        print(f"Height: {self.nWindowHeight}")
        self.create_widgets()

        self.window.show()
        
        sys.exit(self.app.exec()) # Start the event loop 

        #---------------------------------------------------------------------------------------------------------
    def create_widgets(self):

        # GET ALL OBJECTS FROM PYQT
        lstObjs = pyqt_getAllObjectsFromMainWindow(self.window)

        sErrorNotExist = "ERROR in create_widgets taking into accout '" + self.ui_file_name + "'. The following object does not exist: "
        #---------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------
        # SOURCE 
        #---------------------------------------------------------------------------------------------------------
        # BUTTON SOURCE 
        self.btn_source_get = self.window.findChild(QPushButton, "pbSourceGet") 
        if self.btn_source_get: # Check if the object exists
           self.btn_source_get.clicked.connect(self.CmdSource_get)
        else:
            print(sErrorNotExist + "QPushButton pbSourceGet")   

        # BUTTON SOURCE REMOVE
        self.btn_source_del = self.window.findChild(QPushButton, "pbSourceRemove") 
        if self.btn_source_del: # Check if the object exists
           self.btn_source_del.clicked.connect(self.CmdSource_del)
        else:
            print(sErrorNotExist + "QPushButton pbSourceRemove")   

        # GROUP BOX SOURCE 
        self.gbox_source = self.window.findChild(QGroupBox, "groupBoxSource") 
        if self.gbox_source: # Check if the object exists
           self.sTVDesSource = self.gbox_source.title()
        else:
            print(sErrorNotExist + "QGroupBox groupBoxSource")   
        
        #---------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------
        # DESTINATION
        #---------------------------------------------------------------------------------------------------------
        # BUTTON DESTINATION
        self.btn_destination_get = self.window.findChild(QPushButton, "pbDestinationGet") 
        if self.btn_destination_get: # Check if the object exists
           self.btn_destination_get.clicked.connect(self.CmdDestination_get)
        else:
            print(sErrorNotExist + "QPushButton pbDestinationGet")   

        # BUTTON SOURCE REMOVE
        self.btn_destination_del = self.window.findChild(QPushButton, "pbDestinationRemove") 
        if self.btn_destination_del: # Check if the object exists
           self.btn_destination_del.clicked.connect(self.CmdDestination_del)
        else:
            print(sErrorNotExist + "QPushButton pbDestinationRemove")   

        # GROUP BOX SOURCE 
        self.gbox_destination = self.window.findChild(QGroupBox, "groupBoxDestination") 
        if self.gbox_destination: # Check if the object exists
           self.sTVDesDestination = self.gbox_destination.title()
        else:
            print(sErrorNotExist + "QGroupBox groupBoxDestination")   

        #---------------------------------------------------------------------------------------------------------
        # BUTTON PROCESS
        self.btn_process = self.window.findChild(QPushButton, "pbProcess") 
        if self.btn_process: # Check if the object exists
           self.btn_process.clicked.connect(self.CmdProcess)
        else:
            print(sErrorNotExist + "QPushButton pbProcess")   

        #---------------------------------------------------------------------------------------------------------
        # BUTTON CLEAN
        self.btn_clean = self.window.findChild(QPushButton, "pbClean") 
        if self.btn_clean: # Check if the object exists
           self.btn_clean.clicked.connect(self.CmdClean)
        else:
            print(sErrorNotExist + "QPushButton pbClean")   

        #---------------------------------------------------------------------------------------------------------
        # BUTTON CLEAN LOG
        self.btn_clean_log = self.window.findChild(QPushButton, "pbCleanLog") 
        if self.btn_clean_log: # Check if the object exists
           self.btn_clean_log.clicked.connect(self.CmdCleanLog)
        else:
            print(sErrorNotExist + "QPushButton pbCleanLog")   

        #---------------------------------------------------------------------------------------------------------
        # DATA MODEL
        # Sample data
        #data = [
        #    ["Apple", 1.20, 100],
        #    ["Banana", 0.75, 150],
        #    ["Orange", 1.50, 80],
        #    ["Grape", 2.10, 200]
        #]
        #headers = ["Fruit", "Price ($)", "Quantity"]
        #data = [[1], [2], [3]]
        dataSource = []
        dataDestination = []
        headers = ["Path"]

        #---------------------------------------------------------------------------------------------------------
        # Create the model
        self.modelSource = pyqtTableModel(dataSource, headers)
        self.modelDestination = pyqtTableModel(dataDestination, headers)

        #---------------------------------------------------------------------------------------------------------
        # SOURCE GRID 
        self.layout_tv_source = self.window.findChild(QVBoxLayout, "verticalLayoutSource") 

        # setting table properties -------------------------------------------------------------------------------------
        self.tv_source: QTableView = QTableView()
        self.tv_source.setModel(self.modelSource)
        self.layout_tv_source.addWidget(self.tv_source)
        
        header = self.tv_source.horizontalHeader()
        self.tv_source.resizeRowsToContents()
        self.tv_source.setWordWrap(True)
        self.tv_source.setModel(self.modelSource)
        self.tv_source.setColumnWidth(self.nColPath, self.nColWidth)
        self.modelSource.setGridSelectionSingle(self.tv_source)
        self.tv_source.doubleClicked.connect(self.tvGrid_on_cell_double_clicked_Source)
        self.tv_source.clicked.connect(self.tvGrid_on_cell_double_clicked_Source)

        #---------------------------------------------------------------------------------------------------------
        # TEXT TOTAL SOURCE
        self.txt_total_source = self.window.findChild(QTextEdit, "txtTotalSource") 
        if self.txt_total_source: # Check if the object exists
           pyqt_TextEditableReadOnly(self.txt_total_source)
        else:
            print(sErrorNotExist + "QTextEdit txtTotalSource")   

        #---------------------------------------------------------------------------------------------------------
        # DESTINATION GRID 
        #---------------------------------------------------------------------------------------------------------

        self.layout_tv_destination = self.window.findChild(QVBoxLayout, "verticalLayoutDestination") 

        # setting table properties -------------------------------------------------------------------------------------
        self.tv_destination: QTableView = QTableView()
        self.tv_destination.setModel(self.modelDestination)
        self.layout_tv_destination.addWidget(self.tv_destination)
        
        header = self.tv_destination.horizontalHeader()
        self.tv_destination.resizeRowsToContents()
        self.tv_destination.setWordWrap(True)
        self.tv_destination.setModel(self.modelDestination)
        self.tv_destination.setColumnWidth(self.nColPath, self.nColWidth)
        self.modelSource.setGridSelectionSingle(self.tv_destination)
        self.tv_destination.doubleClicked.connect(self.tvGrid_on_cell_double_clicked_Destination)
        self.tv_destination.clicked.connect(self.tvGrid_on_cell_double_clicked_Destination)

        #---------------------------------------------------------------------------------------------------------
        # TEXT TOTAL DESTINATION
        self.txt_total_destination = self.window.findChild(QTextEdit, "txtTotalDestination") 
        if self.txt_total_destination: # Check if the object exists
           pyqt_TextEditableReadOnly(self.txt_total_destination)
        else:
            print(sErrorNotExist + "QTextEdit txtTotalDestination")   

        #---------------------------------------------------------------------------------------------------------
        # TEXT ABOUT
        self.txt_about = self.window.findChild(QTextEdit, "txtAbout") 
        if self.txt_about: # Check if the object exists
           pyqt_TextEditableReadOnly(self.txt_about)
        else:
            print(sErrorNotExist + "QTextEdit txtAbout")   

        #---------------------------------------------------------------------------------------------------------
        # TEXT LOG FILE
        self.layout_txt_logFile = self.window.findChild(QVBoxLayout, "verticalLayoutLogFile") 
        self.txt_logFile = customPyQt_TextEdit()
        self.layout_txt_logFile.addWidget(self.txt_logFile)
        if self.txt_logFile: # Check if the object exists
           pyqt_TextEditableReadOnly(self.txt_logFile)
           pyqt_TextBoxSetText(self.txt_logFile, self.log_file)
        else:
            print(sErrorNotExist + "QTextEdit txtLogFile")   

        #---------------------------------------------------------------------------------------------------------
        # TEXT LOG
        self.layout_txt_log = self.window.findChild(QVBoxLayout, "verticalLayoutLog") 
        self.txt_log = customPyQt_TextEdit()
        self.layout_txt_log.addWidget(self.txt_log)
        if self.txt_log: # Check if the object exists
           pyqt_TextEditableReadOnly(self.txt_log)
           pyqt_TextBoxSetText(self.txt_log, "LOG")
        else:
            print(sErrorNotExist + "QTextEdit txtLog")   

        #---------------------------------------------------------------------------------------------------------
        # EXIT BUTTON
        # Inside MyWindow's __init__ or a method called after load_ui
        self.btn_exit = self.window.findChild(QPushButton, "CmdExit") 
        if self.btn_exit: # Check if the button was found
           self.btn_exit.clicked.connect(self.CmdExit)
        else:
            print(sErrorNotExist + "QPushButton CmdExit")   


        #---------------------------------------------------------------------------------------------------------
        # APP DATA
        sHeader = "App Name: " + str(app_name) + " - " + str(app_name_des)
        sVersion = "Version: " + app_ver + " - " + app_ver_date + ". Window Size - Width: " + str(self.nWindowWidth) + " - Height: " + str(self.nWindowHeight)
        pyqt_TextBoxSetText(self.txt_about, sHeader + "\n" + sVersion)

        #GET XML DATA
        self.xml_get()

        dateStart = datetime.now()
        today_f = dateStart.strftime(self.sdtFormat)
        print(self.sdtString + "\n" + "Started APP '" + self.str_client + "' at: " + today_f + "\n" + self.sdtString + "\n")

    #---------------------------------------------------------------------------------------------------------
    def CmdSource_get(self):
        self.CmdPathGet()
        return

    #---------------------------------------------------------------------------------------------------------
    def CmdDestination_get(self):
        self.CmdPathGet(False)
        return
    
    def CmdPathGet(self, bSource=True):
        lstFiles = self.openFilesDlg(bSource)
        #print("CmdPathGet - sFile = " + str(lstFiles))

        if len(lstFiles) > 0:
           n = 0
           nRow = 0

           while n < len(lstFiles):
           
                 if bSource:
                    nCount = self.modelSource.rowCount()
                    self.sPathSource = str(lstFiles[n])
                 else:
                    nCount = self.modelDestination.rowCount()
                    self.sPathDestination = str(lstFiles[n])
                        
                 nRow = self.grid_AddRow(str(lstFiles[n]), bSource, True)
                 if nRow <= nCount:
                     sWarning = "WARNING!!! Data '" + str(lstFiles[n]) + "' already exists in Row = " + str(nRow)
                     log_writeWordsInColorYellow(sWarning)
                     pyqt_MsgBox_Warning("Add Directory", sWarning)

                 n = n + 1

        self.tvGrid_set_totals(bSource)
        return


    #---------------------------------------------------------------------------------------------------------
    def grid_AddRow(self, sData, bSource=True, bValidateExists=True):

        lst = []
        lst.append(sData)
        nRow = -1

        if len(lst) > 0:
           if bSource:
              if bValidateExists:
                 nRow = self.modelSource.getRowByData(0, sData)

              if nRow == -1:
                 nRow = self.modelSource.addRow(lst)
                 self.modelSource.setDataCell(self.nSourceRows-1, self.nColPath, lst)
                 self.tv_source.resizeRowsToContents() 
                 self.nRowCurrentSource = nRow - 1
                 self.tv_source.selectRow(nRow)
           else:
              if bValidateExists:
                 nRow = self.modelDestination.getRowByData(0, sData)

              if nRow == -1:
                 nRow = self.modelDestination.addRow(lst)
                 self.modelDestination.setDataCell(self.nDestinationRows-1, self.nColPath, lst)
                 self.tv_destination.resizeRowsToContents() 
                 self.nRowCurrentDestination = nRow - 1
                 self.tv_destination.selectRow(nRow)
        
        #print("grid_AddRow - nRow = " + str(nRow))
        return nRow
                           

    #---------------------------------------------------------------------------------------------------------
    def CmdSource_del(self):
        self.Cmd_del(True)
        return


    #---------------------------------------------------------------------------------------------------------
    def CmdDestination_del(self):
        self.Cmd_del(False)
        return

    #---------------------------------------------------------------------------------------------------------
    def Cmd_del(self, bSource=True):

        nRow = self.nRowCurrentSource
        sTVDes = self.sTVDesSource
        sData = self.modelSource.getDataByRowCol(nRow, 0)
        if not bSource:
           nRow = self.nRowCurrentDestination
           sTVDes = self.sTVDesDestination
           sData = self.modelDestination.getDataByRowCol(nRow, 0)

        bResult = False
        #print("Cmd_del - nRow = " + str(nRow))

        if nRow >= 0 and sData != "":
            sMsg = "Are you sure you need to delete '" + sTVDes + "' row: " + str(nRow) + " ?"
            sMsg += "\nData: " + sData

            sResponse, bResponse = pyqt_MsgBoxYesNo(self.window, "Delete Row for " + sTVDes, sMsg)
            #print("Cmd_del - sResponse = " + str(sResponse) + " - bResponse = " + str(bResponse))

            if not bResponse:
                return bResponse
            
            if bSource:
                bResult = self.modelSource.delRowByRow(nRow)
                if bResult:
                   self.nRowCurrentSource = self.nRowCurrentSource - 1
            else:
                bResult = self.modelDestination.delRowByRow(nRow)
                if bResult:
                   self.nRowCurrentDestination = self.nRowCurrentDestination - 1
                    
            self.tvGrid_set_totals(bSource)   

        else:
            pyqt_MsgBox_Error("Delete Row", "No row selected for " + sTVDes + ". Row: " + str(nRow) + " - Data: " + str(sData))

        return bResult    

    #---------------------------------------------------------------------------------------------------------
    def CmdProcess(self):

        lstSource = self.modelSource.getALLDataByCol(self.nColPath)
        lstDestination = self.modelDestination.getALLDataByCol(self.nColPath)
        bResult, sError = process_CopyFiles(self.log_file, lstSource, lstDestination)

        if not bResult:   
           log_writeWordsInColorYellow(sError)
           pyqt_MsgBox_Warning("Process", sError)

        return bResult

    #---------------------------------------------------------------------------------------------------------
    def CmdClean(self):

        if self.modelSource.rowCount() <= 0 and self.modelDestination.rowCount() <= 0:
           sWarning = "WARNING!!! There is nothing to clean in both Grids."
           log_writeWordsInColorYellow(sWarning)
           pyqt_MsgBox_Warning("Clean Grids", sWarning)
           return

        self.modelSource.clean_table(self.tv_source)
        self.modelDestination.clean_table(self.tv_destination)
        self.tvGrid_set_totals(True)
        self.tvGrid_set_totals(False)

        return 

    #---------------------------------------------------------------------------------------------------------
    def CmdCleanLog(self):
        pyqt_TextBoxSetText(self.txt_log, "")
        return

    #---------------------------------------------------------------------------------------------------------
    def openFilesDlg(self, bSource):

        sPath = self.sPathSource
        sTitle = "Source"
        if not bSource:
           sTitle = "Destination"
           sPath = self.sPathDestination

        print("openFilesDlg - Default Path = " + str(sPath))
        lstFiles = pyqt_OpenFileDlgDirOnly(self.window, app_name_des + " - " + sTitle, sPath, "", True)

        #print("openFilesDlg = " + str(lstFiles))

        return lstFiles

    #---------------------------------------------------------------------------------------------------------
    def tvGrid_on_cell_double_clicked_Source(self, index):

        #print("index = " + str(index))

        #row = index.row
        #col = index.column
        #print("row = " + str(row) + " - column = " + str(col))
        return self.tvGrid_on_cell_double_clicked(index, True)

    #---------------------------------------------------------------------------------------------------------
    def tvGrid_on_cell_double_clicked_Destination(self, index):

        return self.tvGrid_on_cell_double_clicked(index, False)

    #---------------------------------------------------------------------------------------------------------
    def tvGrid_on_cell_double_clicked(self, index, bSource=True):
            # Access the data using the model associated with the QTableView

        model = self.modelSource
        if not bSource:
           model = self.modelDestination

        #print("tvGrid_on_cell_double_clicked_Source - index: " + str(index) + " - index.row = " + str(index.row()))

        row = index.row()
        col = index.column()

        #cell_data = model.getData(row, col)
        cell_data = model.getDataByIndex(index)
        #cell_data = model.getDataByRowCol(row, col)

        if bSource:
           self.nRowCurrentSource = row
        else:
           self.nRowCurrentDestination = row

       #print("tvGrid_on_cell_double_clicked - cell at Row: " + str(row) + " - col = " + str(col) + " - Data: " + str(cell_data))
        print("tvGrid_on_cell_double_clicked - Data: " + str(cell_data) + " Row: " + str(row))

        return

    #---------------------------------------------------------------------------------------------------------
    def tvGrid_on_cell_clicked_Destination(self, index):

        return self.tvGrid_on_cell_double_clicked(self.tv_source, index)

    #---------------------------------------------------------------------------------------------------------
    def tvGrid_set_totals(self, bSource=True):
        if bSource:
            nCount = self.modelSource.rowCount()
            sTotal = "Total: " + str(nCount)
            pyqt_TextBoxSetText(self.txt_total_source, sTotal)
        else:
            nCount = self.modelDestination.rowCount()
            sTotal = "Total: " + str(nCount)
            pyqt_TextBoxSetText(self.txt_total_destination, sTotal)

        return nCount    

    #---------------------------------------------------------------------------------------------------------
    # XML SAVE AND GET
    #---------------------------------------------------------------------------------------------------------
    def xml_save(self):

        #APP REFERENCE
        xml_Save_Default_Value(self.sApp_XML_PathAndFile, self.sXML_APDU_VERSION, app_ver + "_" + app_ver_date, app_name, app_name_des)

        #SOURCE 
        nCountSource = self.modelSource.rowCount()
        xml_Save_Default_Value(self.sApp_XML_PathAndFile, self.sXML_PATH_SOURCE_TOTAL, str(nCountSource))
        #self.sPathSource  = self.sApp_Path 
        n = 0
        while n < nCountSource:
              sData = self.modelSource.getDataByRowCol(n, 0)
              sHeader = self.sXML_PATH_SOURCE + str(n)
              xml_Save_Default_Value(self.sApp_XML_PathAndFile, sHeader, sData)
              self.sPathSource = sData
              n = n + 1

        #DESTINATION
        nCountDestination = self.modelDestination.rowCount()
        xml_Save_Default_Value(self.sApp_XML_PathAndFile, self.sXML_PATH_DESTINATION_TOTAL, str(nCountDestination))
        #self.sPathDestination  = self.sApp_Path 
        n = 0
        while n < nCountDestination:
              sData = self.modelDestination.getDataByRowCol(n, 0)
              sHeader = self.sXML_PATH_DESTINATION + str(n)
              xml_Save_Default_Value(self.sApp_XML_PathAndFile, sHeader, sData)
              self.sPathDestination = sData
              n = n + 1

        #APP LAST PATH USED - SOURCE
        xml_Save_Default_Value(self.sApp_XML_PathAndFile, self.sXML_PATH_DEFAULT_SOURCE, self.sPathSource )
        #APP LAST PATH USED - DESTINATION
        xml_Save_Default_Value(self.sApp_XML_PathAndFile, self.sXML_PATH_DEFAULT_DESTINATION, self.sPathDestination )

        return

    #---------------------------------------------------------------------------------------------------------
    def xml_get(self):

        #SOURCE TOTALS
        self.nPathSourceTotal = 0 
        self.sPathSourceTotal = xml_Load_Default_Value(self.sApp_XML_PathAndFile, self.sXML_PATH_SOURCE_TOTAL, str(self.nPathSourceTotal))
        if valid_nro_IsCharValidNro(self.sPathSourceTotal, True):
           self.nPathSourceTotal = int(self.sPathSourceTotal)

        #print("xml_get - Total Source: " + str(self.nPathSourceTotal))
        self.xml_get_grid(True, self.nPathSourceTotal)

        #DESTINATION TOTALS
        self.nPathDestinationTotal = 0 
        self.sPathDestinationTotal = xml_Load_Default_Value(self.sApp_XML_PathAndFile, self.sXML_PATH_DESTINATION_TOTAL, str(self.nPathDestinationTotal))
        if valid_nro_IsCharValidNro(self.sPathDestinationTotal, True):
           self.nPathDestinationTotal = int(self.sPathDestinationTotal)

        #print("xml_get - Total Destination: " + str(self.nPathDestinationTotal))
        self.xml_get_grid(False, self.nPathDestinationTotal)

        #GET LAST PATHS
        self.sPathSource = xml_Load_Default_Value(self.sApp_XML_PathAndFile, self.sXML_PATH_DEFAULT_SOURCE, self.sApp_Path)
        self.sPathDestination = xml_Load_Default_Value(self.sApp_XML_PathAndFile, self.sXML_PATH_DEFAULT_DESTINATION, self.sApp_Path)

        return

    #---------------------------------------------------------------------------------------------------------
    def xml_get_grid(self, bSource=True, nTotal=0):

        #print("xml_get_grid - Total: " + str(nTotal))
        bOut = False
        n = 0
        while not bOut and n < nTotal:
              if bSource:
                 sHeader = self.sXML_PATH_SOURCE + str(n)
              else:
                 sHeader = self.sXML_PATH_DESTINATION + str(n)

              #print("xml_get_grid - sHeader: " + str(sHeader))

              sData = xml_Load_Default_Value(self.sApp_XML_PathAndFile, sHeader, "")
              #print("xml_get_grid - sData: " + str(sData))

              if sData == "":
                 bOut = True
              else:
                 self.grid_AddRow(sData, bSource, False)
              n = n + 1

        self.tvGrid_set_totals(bSource)

    #---------------------------------------------------------------------------------------------------------
    def CmdExit(self):

        sReply, bReply = pyqt_MsgBoxYesNo(self.window, app_name_des, "Are you sure you want to quit?")

        if bReply:
            print("Window to be closed.")
            self.exit()
        else:
            print("Close event ignored.")

        return sReply
        
    #---------------------------------------------------------------------------------------------------------
    def about(self):
        smpp_about = SMPPTransmitterScreenAbout(self.str_client, self.log_file)
        smpp_about.run()
        return

    #---------------------------------------------------------------------------------------------------------
    def exit(self):
        dateStart = datetime.now()
        today_f = dateStart.strftime(self.sdtFormat)
        print(self.sdtString + "\n" + "Finished APP '" + self.str_client + "' at: " + today_f + "\n" + self.sdtString + "\n")

        self.xml_save()
        self.window.destroy()
        sys.exit(0)

    #---------------------------------------------------------------------------------------------------------
