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
from PyQt5.QtWidgets import QMessageBox, QTextEdit, QFileDialog, QTableView, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QFile, QIODevice


# from ..constants.general import color_dark_button, color_app_background_light, color_app_background_dark, \
#     color_red_dark, color_green_dark

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(current)
sys.path.append(parent_directory+"/libs")
sys.path.append(parent_directory+"/constants")
sys.path.append(parent_directory+"/iu")

import customtkinter as ctk
import threading

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

import sys

from about import *

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

        self.sXML_APDU_VERSION = "APP_VERSION"
        self.sXML_PATH_SOURCE = "XML_PATH_SOURCE_"
        self.sXML_PATH_DESTINATION = "XML_PATH_DESTINATION_"

        #print("self.sApp_XML_PathAndFile = " + str(self.sApp_XML_PathAndFile))
        #---------------------------------------------------------------------------------------

        self.sLineMark = str_RepeatString(100, sDef_Asterisc) + "\n"

        self.sdtFormat = sDef_dtFormat
        self.sdtString = str_RepeatString(100,sDef_Minus)

        self.nSourceRows = 0
        self.nDestinationRows = 0
        self.nRowLen = 300
        self.nColWidth = self.nRowLen
        self.nColPath = 0

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
        self.ui_file_name = parent_directory + app_ui_file_name
        bReturn, self.window = pyqt_open_ui_file(self.ui_file_name)

        if not (bReturn or self.window):
           sys.exit(-1)

        self.nWindowWidth = self.app.primaryScreen().size().width()
        self.nWindowHeight = self.app.primaryScreen().size().height()
        print(f"Width: {self.nWindowWidth}")
        print(f"Height: {self.nWindowHeight}")
        self.create_widgets()

        self.sPathSource = parent_directory
        self.sPathDestination = parent_directory
        
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
        # TEXT LOG
        self.txt_log = self.window.findChild(QTextEdit, "txtLog") 
        if self.txt_log: # Check if the object exists
           pyqt_TextEditableReadOnly(self.txt_log)
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
    def CmdSource_del(self):
        return

    #---------------------------------------------------------------------------------------------------------
    def CmdDestination_get(self):
        self.CmdPathGet(False)
        return
    
    def CmdPathGet(self, bSource=True):
        lstFiles = self.openFilesDlg(True)
        print("CmdPathGet - sFile = " + str(lstFiles))

        if len(lstFiles) > 0:
           n = 0
           nRow = 0

           while n < len(lstFiles):
           
                 self.grid_AddRow(str(lstFiles[n]), bSource)

                 n = n + 1

        self.tvGrid_set_totals(bSource)
        return


    #---------------------------------------------------------------------------------------------------------
    def grid_AddRow(self, sData, bSource=True):

        lst = []
        lst.append(sData)
        if len(lst) > 0:
           if bSource:
              nRow = self.modelSource.addRow(lst)
              self.modelSource.setDataCell(self.nSourceRows-1, self.nColPath, lst)
              self.tv_source.resizeRowsToContents() 
           else:
              nRow = self.modelDestination.addRow(lst)
              self.modelDestination.setDataCell(self.nDestinationRows-1, self.nColPath, lst)
              self.tv_destination.resizeRowsToContents() 
        
        return nRow
                           


    #---------------------------------------------------------------------------------------------------------
    def CmdDestination_del(self):
        return


    #---------------------------------------------------------------------------------------------------------
    def CmdProcess(self):
        return 

    #---------------------------------------------------------------------------------------------------------
    def CmdClean(self):
        return 

    #---------------------------------------------------------------------------------------------------------
    def openFilesDlg(self, bSource):

        sPath = self.sPathSource
        sTitle = "Source"
        if not bSource:
           sTitle = "Destination"
           sPath = self.sPathDestination

        lstFiles = pyqt_OpenFileDlgDirOnly(self.window, app_name_des + " - " + sTitle, sPath, "", True)

        #print("openFilesDlg = " + str(lstFiles))

        return lstFiles

    #---------------------------------------------------------------------------------------------------------
    def tvGrid_on_cell_double_clicked_Source(self, index):

        #print("index = " + str(index))

        #row = index.row
        #col = index.column
        #print("row = " + str(row) + " - column = " + str(col))
        return self.tvGrid_on_cell_double_clicked(self.tv_source, index)

    #---------------------------------------------------------------------------------------------------------
    def tvGrid_on_cell_double_clicked_Destination(self, index):

        return self.tvGrid_on_cell_double_clicked(self.tv_destination, index)

    #---------------------------------------------------------------------------------------------------------
    def tvGrid_on_cell_double_clicked(self, tv, index):
            # Access the data using the model associated with the QTableView
        model = tv.model()
        #cell_data = model.getData(row, col)
        cell_data = model.getDataByIndex(index)

        #row = index.row
        #col = index.column

       #print("tvGrid_on_cell_double_clicked_Source - cell at Row: " + str(row) + " - col = " + str(col) + " - Data: " + str(cell_data))
        print("tvGrid_on_cell_double_clicked_Source - Data: " + str(cell_data))

        return

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

        #SOURCE 
        nCountSource = self.modelSource.rowCount()
        n = 0
        while n < nCountSource:
              sData = self.modelSource.getDataByRowCol(n, 0)
              sHeader = self.sXML_PATH_SOURCE + str(n)
              self.util_XML_Save_Default_Value(sHeader, sData)
              n = n + 1

        #DESTINATION
        nCountDestination = self.modelDestination.rowCount()
        n = 0
        while n < nCountDestination:
              sData = self.modelDestination.getDataByRowCol(n, 0)
              sHeader = self.sXML_PATH_DESTINATION + str(n)
              self.util_XML_Save_Default_Value(sHeader, sData)
              n = n + 1

        self.util_XML_Save_Default_Value(self.sXML_APDU_VERSION, app_ver + "_" + app_ver_date)

        return

    #---------------------------------------------------------------------------------------------------------
    def xml_get(self):

        #SOURCE 
        self.xml_get_grid(True)
                     
        #DESTINATION
        self.xml_get_grid(False)

        return

    #---------------------------------------------------------------------------------------------------------
    def xml_get_grid(self, bSource=True):

        bOut = False
        n = 0
        while not bOut and n < 100:
              if bSource:
                 sHeader = self.sXML_PATH_SOURCE + str(n)
              else:
                 sHeader = self.sXML_PATH_DESTINATION + str(n)
                     
              sData = self.util_XML_Load_Default_Value(sHeader, "")
              if sData == "":
                 bOut = True
              else:
                 self.grid_AddRow(sData, bSource)
              n = n + 1

        self.tvGrid_set_totals(bSource)

    #---------------------------------------------------------------------------------------------------------
    def util_XML_Load_Default_Value(self, sTag, sDefault):
        success, data, _ = xml_utils_get_nodes(self.sApp_XML_PathAndFile, sTag)
        
        if success and len(data) > 0:
           return data[0].get("value", "")
        else:   
           return sDefault

    #---------------------------------------------------------------------------------------------------------
    def util_XML_Save_Default_Value(self, sTag, sValue):
        if not os.path.exists(self.sApp_XML_PathAndFile):
        
            bReturn, xml_pretty, xml_path =  xml_utils_create_file(
                                                                 header_name=app_name,
                                                                 header_attrs={"Description": app_name_des},
                                                                 child_node_name=sTag,
                                                                 child_nodes_data=[{"value": sValue}],
                                                                 dir_path=os.path.dirname(self.sApp_XML_PathAndFile),
                                                                 name=os.path.basename(self.sApp_XML_PathAndFile)
                                                                 )
        else:   
            bReturn, xml_pretty, xml_path =  xml_utils_replace_node(self.sApp_XML_PathAndFile, sTag, sValue)

        sPrint = ""
        if bReturn:
           sPrint = sPrint + "[XML SAVED SUCCESSFULLY] TAG = " + str(sTag) + " - VALUE = " + str(sValue)
        else:
           sPrint = sPrint + "[XML NOT SAVED] ERROR = " + str(xml_pretty)
        
        sPrint = sPrint + ". XML Path and File Name: [" + str(self.sApp_XML_PathAndFile) + "]"   
        print(sPrint)
           
        return bReturn

    #---------------------------------------------------------------------------------------------------------
    def CmdExit(self):

        reply = pyqt_MsgBoxYesNo(self.window, app_name_des, "Are you sure you want to quit?")

        if reply == QMessageBox.Yes:
            print("Window to be closed.")
            self.exit()
        else:
            print("Close event ignored.")

        return reply
        
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
