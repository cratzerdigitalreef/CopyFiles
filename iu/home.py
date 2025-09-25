# -*- coding: UTF-8 -*-

import sys
import os

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
from ctk_utils import *

import sys

from general import *
from .about import *

class CopyFilesHomeScreen:

    def __init__(self, client, log_file):

        self.log_file = log_file
        self.str_client = client
        self.status = "Success"
        self.is_error = False

        self.nInnerFrame = 200
        self.nInnerFramePadxPady = 5

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
        
        #FRAME BORDER WITH
        self.FrameBorderWith = nDef_FrameBroderWidth

        # Crear la interfaz de usuario

        # Crear la ventana principal
        self.main_window = ctk.CTk()
        # Obtener la ruta absoluta del icono basado en la ubicación del script

        self.main_window.title(app_name + " - Python")
	
        # GET WINDOW SIZE
        self.nWindowWidth, self.nWindowHeight = ctk_utils_GetWindowWidthHeight(self.main_window)
        
        print("Windows Height: " + str(self.nWindowHeight))
        print("Windows Width: " + str(self.nWindowWidth))

        self.nMaxLenAPDU = 100
        self.nMaxConfig = 300
        self.nMaxConfigMSLKeySet = 500
        self.nMaxConfigMSLCount = self.nMaxConfigMSLKeySet // 2
        self.sFont = "Courier New"
        self.nResponseHeight = 10
        self.nFontSize = 12
        self.nButtonHeight = 1
        self.nButtonWidth = 15
        self.nFontSizeButton = 10
        self.nWindowHeightPor = 1
        self.nWindowWidthPor = self.nWindowHeightPor 

        if self.nWindowWidth >= 1900:
           self.nMaxLenAPDU = self.nMaxLenAPDU * 15
           self.nResponseHeight = self.nResponseHeight * 20
           self.nFontSize = 14
           self.nWindowHeightPor = 0.9
           self.nWindowWidthPor = self.nWindowHeightPor * 1.5
           self.nFontSizeButton = 12
        else:
           if self.nWindowWidth >= 1600:
              self.nMaxLenAPDU = self.nMaxLenAPDU * 12
              self.nResponseHeight = self.nResponseHeight * 15
              #self.nFontSize = 12
              self.nFontSizeButton = 12
           else:
              self.nMaxLenAPDU = self.nMaxLenAPDU * 10
              self.nResponseHeight = self.nResponseHeight * 10


        self.create_widgets()
        # *************

    #---------------------------------------------------------------------------------------------------------
    def create_widgets(self):

        #---------------------------------------------------------------------------------------------------------
        # APP DATA
        sHeader = "App Name: " + str(app_name) + " - " + str(app_name_des)
        sVersion = "Version: " + app_ver + " - " + app_ver_date + ". Window Size - Width: " + str(self.nWindowWidth) + " - Height: " + str(self.nWindowHeight)

        #---------------------------------------------------------------------------------------------------------
        # EXIT
        
        #self.button_exit = ctk.CTkButton(self.toolbar_frame_8, text="Exit", command=self.exit, fg_color=self.app_button_color, text_color=self.app_button_color_text, font=(self.sFont, self.nFontSizeButton))
        #self.button_exit.pack(side="right", padx=self.nInnerFramePadxPady, pady=self.nInnerFramePadxPady)

        #---------------------------------------------------------------------------------------------------------
        # Actualiza tareas pendientes y ajusta el tamaño
        self.main_window.update_idletasks()
        width = self.nWindowWidth * self.nWindowWidthPor
        height = self.nWindowHeight * self.nWindowHeightPor
        print("width: " + str(width))
        print("height: " + str(height))

        #self.main_window.geometry(f"{width}x{height}")

        x = 0
        y = 0
        self.main_window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        #GET XML DATA
        self.xml(True)

    #---------------------------------------------------------------------------------------------------------
    def run(self):

        """Inicia la interfaz gráfica."""

        try:

            dateStart = datetime.now()
            today_f = dateStart.strftime(self.sdtFormat)
            print(self.sdtString + "\n" + "Started APP '" + self.str_client + "' at: " + today_f + "\n" + self.sdtString + "\n")

            self.main_window.protocol("WM_DELETE_WINDOW", self.exit)
            self.main_window.mainloop()

        finally:

            dateStart = datetime.now()
            today_f = dateStart.strftime(self.sdtFormat)
            print(self.sdtString + "\n" + "Finished APP '" + self.str_client + "' at: " + today_f + "\n" + self.sdtString + "\n")


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
    def about(self):
        smpp_about = SMPPTransmitterScreenAbout(self.str_client, self.log_file)
        smpp_about.run()
        return

    #---------------------------------------------------------------------------------------------------------
    def exit(self):
        self.save_ui_state()
        self.main_window.destroy()
        sys.exit(0)

    #---------------------------------------------------------------------------------------------------------
