# -*- coding: UTF-8 -*-

import sys
import os

import sys

#PYQT IMPORTS
#from PyQt5.QtWidgets import QApplication
#from PyQt5.QtWidgets import QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox, QTextEdit, QFileDialog

from PySide6.QtCore import QFile, QIODevice

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
from str import *
from pyqt import *
from general import *

import sys

from general import *
from about import *

class CopyFilesHomeScreen:

    def __init__(self, client, log_file):

        self.log_file = log_file
        self.str_client = client
        self.status = "Success"
        self.is_error = False

        self.sLineMark = str_RepeatString(100, sDef_Asterisc) + "\n"

        self.sdtFormat = sDef_dtFormat
        self.sdtString = str_RepeatString(100,sDef_Minus)

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
        
        # Crear la interfaz de usuario
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
        pyqt_getAllObjectsFromMainWindow(self.window)

        #---------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------
        # SOURCE 
        #---------------------------------------------------------------------------------------------------------
        # BUTTON SOURCE 
        self.btn_source_get = self.window.findChild(QPushButton, "pbSourceGet") 
        if self.btn_source_get: # Check if the object exists
           self.btn_source_get.clicked.connect(self.CmdSource_get)

        # BUTTON SOURCE REMOVE
        self.btn_source_del = self.window.findChild(QPushButton, "pbSourceRemove") 
        if self.btn_source_del: # Check if the object exists
           self.btn_source_del.clicked.connect(self.CmdSource_del)

        #---------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------
        # DESTINATION
        #---------------------------------------------------------------------------------------------------------
        # BUTTON DESTINATION
        self.btn_destination_get = self.window.findChild(QPushButton, "pbDestinationGet") 
        if self.btn_destination_get: # Check if the object exists
           self.btn_destination_get.clicked.connect(self.CmdDestination_get)

        # BUTTON SOURCE REMOVE
        self.btn_destination_del = self.window.findChild(QPushButton, "pbDestinationRemove") 
        if self.btn_destination_del: # Check if the object exists
           self.btn_destination_del.clicked.connect(self.CmdDestination_del)

        #---------------------------------------------------------------------------------------------------------
        # BUTTON PROCESS
        self.btn_process = self.window.findChild(QPushButton, "pbProcess") 
        if self.btn_process: # Check if the object exists
           self.btn_process.clicked.connect(self.CmdProcess)

        #---------------------------------------------------------------------------------------------------------
        # BUTTON CLEAN
        self.btn_clean = self.window.findChild(QPushButton, "pbClean") 
        if self.btn_clean: # Check if the object exists
           self.btn_clean.clicked.connect(self.CmdClean)

        #---------------------------------------------------------------------------------------------------------
        # TEXT SOURCE
        #self.txt_source = self.window.findChild(TableView, "tvSource") 
        #if self.txt_source: # Check if the object exists
        #   pyqt_TextEditable(self.txt_source, False)

        #---------------------------------------------------------------------------------------------------------
        # TEXT DESTINATION
        #self.txt_destination = self.window.findChild(QTextEdit, "txtDestination") 
        #if self.txt_destination: # Check if the object exists
        #   pyqt_TextEdit(self.txt_destination, False)

        #---------------------------------------------------------------------------------------------------------
        # TEXT ABOUT
        self.txt_about = self.window.findChild(QTextEdit, "txtAbout") 
        if self.txt_about: # Check if the object exists
           pyqt_TextEditable(self.txt_about)

        #---------------------------------------------------------------------------------------------------------
        # TEXT LOG
        self.txt_log = self.window.findChild(QTextEdit, "txtLog") 
        if self.txt_log: # Check if the object exists
           pyqt_TextEditable(self.txt_log)

        #---------------------------------------------------------------------------------------------------------
        # EXIT BUTTON
        # Inside MyWindow's __init__ or a method called after load_ui
        self.btn_exit = self.window.findChild(QPushButton, "CmdExit") 
        if self.btn_exit: # Check if the button was found
           self.btn_exit.clicked.connect(self.CmdExit)


        #---------------------------------------------------------------------------------------------------------
        # APP DATA
        sHeader = "App Name: " + str(app_name) + " - " + str(app_name_des)
        sVersion = "Version: " + app_ver + " - " + app_ver_date + ". Window Size - Width: " + str(self.nWindowWidth) + " - Height: " + str(self.nWindowHeight)
        pyqt_TextBoxSetText(self.txt_about, sHeader + "\n" + sVersion)

        #GET XML DATA
        self.xml(True)

        dateStart = datetime.now()
        today_f = dateStart.strftime(self.sdtFormat)
        print(self.sdtString + "\n" + "Started APP '" + self.str_client + "' at: " + today_f + "\n" + self.sdtString + "\n")

    #---------------------------------------------------------------------------------------------------------
    def CmdSource_get(self):
        sFile = self.openFilesDlg(True)
        print("sFile = " + str(sFile))
        #pyqt_TextBoxSetText(self.txt_source, sFile)
        return

    #---------------------------------------------------------------------------------------------------------
    def CmdSource_del(self):
        return

    #---------------------------------------------------------------------------------------------------------
    def CmdDestination_get(self):
        sFile = self.openFilesDlg(False)
        #pyqt_TextBoxSetText(self.txt_destination, sFile)
        return 
    
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

        sFile = pyqt_OpenFileDlgDirOnly(self.window, app_name_des + " - " + sTitle, sPath, "", True)

        print("openFilesDlg = " + str(sFile))

        return sFile


    #---------------------------------------------------------------------------------------------------------
    def save_ui_state(self):

        #self.util.util_XML_Save_Default_Value(self.util.sXML_APDU, self.apdu_input_GetValue(True))
        return

    #---------------------------------------------------------------------------------------------------------
    def xml(self, bSetVersion=False):
    
        #self.apdu_input.set(self.util.util_XML_Load_Default_Value(self.util.sXML_APDU, self.def_apdu))
        #ctk_utils_TextBoxSet(self.apdu_many_txt, ctk_utils_CTkComboBoxGetData(self.apdu_input))
        #self.show_description(self.sAPDUName, "")
        
        #self.tar_input.set(self.util.util_XML_Load_Default_Value(self.util.sXML_APDU_TAR, self.def_tar))
        #self.tpda_input.set(self.util.util_XML_Load_Default_Value(self.util.sXML_APDU_TPDA, self.def_tpda))
        #self.msl_input.set(self.util.util_XML_Load_Default_Value(self.util.sXML_APDU_MSL, self.def_msl))
        #self.msl_kic_input.set(self.util.util_XML_Load_Default_Value(self.util.sXML_APDU_MSL_KIC, self.def_msl_kic))
        #self.msl_kid_input.set(self.util.util_XML_Load_Default_Value(self.util.sXML_APDU_MSL_KID, self.def_msl_kid))
        #self.MSL_CounterSet(self.util.util_XML_Load_Default_Value(self.util.sXML_APDU_MSL_COUNTER, self.def_msl_count))
        return

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

        self.save_ui_state()
        self.window.destroy()
        sys.exit(0)

    #---------------------------------------------------------------------------------------------------------
