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
sys.path.append(parent_directory+"/services")

import customtkinter as ctk

################################################################################
# ADDED: Make the app follow the system’s light/dark settings:
################################################################################
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

from customtkinter import CTkScrollbar
from customtkinter import CTkCheckBox

import tkinter as tk
from customtkinter import filedialog

from pathlib import Path
from apk import *
from str import *
from files import *
from ctk_utils import *

import sys

from general import *

class SMPPTransmitterScreenAbout:

    def __init__(self, client, log_file):

        self.log_file = log_file
        self.str_client = client + " - About"

        #FRAME BORDER WITH
        self.FrameBorderWith = nDef_FrameBroderWidth

        ############################################################################
        # CHANGED color variables so they adapt:
        ############################################################################
        self.app_label_color = ("blue", "white")  # was just "blue"
        self.app_button_color = ("orange", color_dark_button)  # was just "orange"
        self.app_button_color_text = ("black", "white")
        self.app_background_color = (color_app_background_light, color_app_background_dark)  # was "darkgrey"

        self.def_color_OK = ("green", color_green_dark)
        self.def_color_NOK = ("red", color_red_dark)
        self.def_color_INFO = ("blue", color_green_dark)

        self.sdtFormat = sDef_dtFormat
        self.sdtString = str_RepeatString(100,sDef_Minus)

        #------------------------------------------------------------------------------------
        #Create service for Util
        self.util = homeUtil()

        # Crear la interfaz de usuario

        # Crear la ventana principal
        self.about_window = ctk.CTk()
        # Obtener la ruta absoluta del icono basado en la ubicación del script

        #SET .ICO FOR WINDOWS
        ctk_utils_WindowsSetBitmap(self.about_window, app_ico)

        self.about_window.title("About...")
	
        # GET WINDOW SIZE
        self.nWindowHeight = self.about_window.winfo_screenheight()
        self.nWindowWidth = self.about_window.winfo_screenwidth()
        print("Windows Height About: " + str(self.nWindowHeight))
        print("Windows Width About: " + str(self.nWindowWidth))

        self.nMaxLenAPDU = 100
        self.nMaxConfig = 300
        self.nMaxConfigMSLKeySet = 500
        self.nMaxConfigMSLCount = self.nMaxConfigMSLKeySet // 2
        self.sFont = "Courier New"
        self.nResponseHeight = 10
        self.nFontSize = 12
        self.nButtonHeight = 1
        self.nButtonWidth = 15
        #self.nWindowHeightPor = 1
        self.nWindowHeightPor = 0.3
        self.nWindowWidthPor = self.nWindowHeightPor

        if self.nWindowWidth >= 1900:
           self.nMaxLenAPDU = self.nMaxLenAPDU * 15
           self.nResponseHeight = self.nResponseHeight * 20
           self.nFontSize = 14
           self.nWindowHeightPor = 0.3
           self.nWindowWidthPor = self.nWindowHeightPor
        else:
           if self.nWindowWidth >= 1600:
              self.nMaxLenAPDU = self.nMaxLenAPDU * 12
              self.nResponseHeight = self.nResponseHeight * 15
              self.nFontSize = 12
           else:
              self.nMaxLenAPDU = self.nMaxLenAPDU * 10
              self.nResponseHeight = self.nResponseHeight * 10


        self.create_widgets()
        # *************

    #---------------------------------------------------------------------------------------------------------
    def create_widgets(self):

        #---------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------
        # APP DATA
        sHeader = "App Name: " + str(app_name) + "\n" + str(app_name_des)
        sVersion = "Version: " + app_ver + " - " + app_ver_date + ".\nWindow Size - Width: " + str(self.nWindowWidth) + " - Height: " + str(self.nWindowHeight)
        ############################################################################
        # Notice we pass the 2-tuple color variables. They adapt automatically.
        ############################################################################
        #self.connect_label = ctk.CTkLabel(self.main_window,text=sHeader,font=(self.sFont, self.nFontSize),text_color=self.app_label_color,fg_color=self.app_background_color)
        #self.connect_label.pack(padx=5)

        #self.connect_label = ctk.CTkLabel(self.main_window,text=sVersion,font=(self.sFont, self.nFontSize),text_color=self.app_label_color,fg_color=self.app_background_color)
        #self.connect_label.pack(padx=5)

        # ABOUT

        self.about_frame = ctk.CTkFrame(self.about_window, border_width=self.FrameBorderWith)  # Contenedor para agrupar los widgets
        self.about_frame.pack(side="top", fill="x", padx=10, pady=10)  

        # Create the 1st inner frame
        self.about_frame_1 = ctk.CTkFrame(self.about_frame, border_width=self.FrameBorderWith)
        self.about_frame_1.pack(side="left", padx=5, pady=5)

        sAbout = sHeader + "\n\n" + sVersion
        self.about_txt = ctk.CTkTextbox(self.about_frame_1, height=int(self.nResponseHeight//1.5), width=self.nMaxLenAPDU//1.15, wrap="word", font=(self.sFont, self.nFontSize), fg_color=self.app_background_color)
        self.about_txt.insert(ctk.END, sAbout)
        self.about_txt.configure(state=ctk.DISABLED)
        self.about_txt.pack(side="left", padx=4)

        #---------------------------------------------------------------------------------------------------------
        # EXIT

        # Create the 2nd inner frame
        #self.about_frame_2 = ctk.CTkFrame(self.about_frame, border_width=self.FrameBorderWith)
        #self.about_frame_2.pack(side="left", padx=5, pady=5)

        self.button_exit_frame = ctk.CTkFrame(self.about_window, border_width=self.FrameBorderWith)  # Contenedor para agrupar los widgets
        self.button_exit_frame.pack(anchor="e")  # Alinear el frame a la izquierda
        self.button_exit = ctk.CTkButton(self.button_exit_frame, text="Exit", command=self.exit, fg_color=self.app_button_color, text_color=self.app_button_color_text)
        #self.button_exit = ctk.CTkButton(self.about_frame_2, text="Exit", command=self.exit, fg_color=self.app_button_color, text_color=self.app_button_color_text)

        #self.button_exit.pack(side="right", padx=5)
        self.button_exit.pack(padx=5)

        #---------------------------------------------------------------------------------------------------------
        # Actualiza tareas pendientes y ajusta el tamaño
        self.about_window.update_idletasks()
        width = self.nWindowWidth * self.nWindowWidthPor
        height = self.nWindowHeight * self.nWindowHeightPor
        print("width: " + str(width))
        print("height: " + str(height))

        #self.about_window.geometry(f"{width}x{height}")

        x = 0
        y = 0
        self.about_window.geometry('%dx%d+%d+%d' % (width, height, x, y))
        #exit(0)


    #---------------------------------------------------------------------------------------------------------
    def run(self):

        """Inicia la interfaz gráfica."""

        try:

            dateStart = datetime.now()
            today_f = dateStart.strftime(self.sdtFormat)
            #print(self.sdtString + "\n" + "Started APP '" + self.str_client + "' at: " + today_f + "\n" + self.sdtString + "\n")

            self.about_window.protocol("WM_DELETE_WINDOW", self.exit)
            self.about_window.mainloop()

        finally:

            dateStart = datetime.now()
            today_f = dateStart.strftime(self.sdtFormat)
            #print(self.sdtString + "\n" + "Finished APP '" + self.str_client + "' at: " + today_f + "\n" + self.sdtString + "\n")

    #---------------------------------------------------------------------------------------------------------
    def exit(self):
        ctk_utils_WindowsClose(self.about_window)

    #---------------------------------------------------------------------------------------------------------
